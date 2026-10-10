"""The cockpit's Python dependencies — cockpit 1.16.

The standard library only: this runs before the server can import anything
else, when one of them is missing (`at_start`).

- `check()` reads requirements.txt and each package installed
  (importlib.metadata): what is missing, what is too old or too new.
- `plan()` asks pip what it would install — `pip install --dry-run --report`:
  every package, the transitive ones included, with its version and the
  licence its metadata declares. Nothing is installed.
- `licence_text()` downloads one package without installing it and reads
  its licence file: what « Pas à pas » shows in full.
- `install()` runs `pip install --user -r requirements.txt`.
- `run()` is the install itself, in either mode the Product Owner chose
  (« Rapide », « Pas à pas »), each step and licence put to `decide` in
  « Pas à pas »; what it installed and every licence accepted end in the
  report, which `installs.py` keeps in the logs.
"""
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS = os.path.join(HERE, "requirements.txt")
PIP_TIMEOUT = 900
LICENCE_MAX = 60000          # a licence file past this is cut, and said
RAPIDE, PAS_A_PAS = "rapide", "pas_a_pas"

# The pip command, before its arguments; None: this Python's. The tests put
# a fake here.
PIP_COMMAND = None

_REQ = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(\[[^\]]*\])?\s*([^#;]*)")
_SPEC = re.compile(r"(===|==|!=|~=|>=|<=|>|<)\s*([^\s,]+)")


# ------------------------------------------------------------ versions

def _norm(name):
    return re.sub(r"[-_.]+", "-", (name or "").strip()).lower()


def _release(v):
    """A version's numbers: « 0.2.163 » → (0, 2, 163); a suffix ignored."""
    out = []
    for part in (v or "").split("."):
        m = re.match(r"\d+", part)
        if not m:
            break
        out.append(int(m.group()))
    return tuple(out)


def _cmp(a, b):
    a, b = list(_release(a)), list(_release(b))
    n = max(len(a), len(b))
    a += [0] * (n - len(a))
    b += [0] * (n - len(b))
    return (a > b) - (a < b)


def satisfies(version, spec):
    """`version` against « >=0.2,<0.3 » — the operators requirements.txt uses."""
    for op, want in _SPEC.findall(spec or ""):
        if want.endswith(".*"):
            base = _release(want[:-2])
            match = _release(version)[:len(base)] == base
            if (op in ("==", "===") and not match) or (op == "!=" and match):
                return False
            continue
        c = _cmp(version, want)
        ok = {"==": c == 0, "===": version == want, "!=": c != 0, ">=": c >= 0, "<=": c <= 0, ">": c > 0,
              "<": c < 0, "~=": c >= 0 and _release(version)[:max(1, len(_release(want)) - 1)]
              == _release(want)[:max(1, len(_release(want)) - 1)]}[op]
        if not ok:
            return False
    return True


def requirements(path=None):
    """[(name, spec, line)] of requirements.txt — comments and options left out."""
    out = []
    try:
        with open(path or REQUIREMENTS, encoding="utf-8-sig") as f:
            lines = f.read().splitlines()
    except OSError:
        return out
    for line in lines:
        text = line.split("#", 1)[0].strip()
        if not text or text.startswith("-"):
            continue
        m = _REQ.match(text)
        if m:
            out.append((m.group(1), m.group(3).strip(), text))
    return out


def installed(name):
    """The version installed, or None."""
    from importlib import metadata
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None
    except Exception:
        return None


def check(path=None, version_of=None):
    """{"ok", "missing": [{"name", "spec", "installed"}], "count"} — every
    requirement installed at a version it accepts."""
    version_of = version_of or installed
    reqs = requirements(path)
    missing = []
    for name, spec, _ in reqs:
        v = version_of(name)
        if v is None or not satisfies(v, spec):
            missing.append({"name": name, "spec": spec, "installed": v})
    return {"ok": not missing, "missing": missing, "count": len(reqs)}


def missing_text(res):
    return ", ".join(f"{m['name']}{m['spec']}" + (f" (installé : {m['installed']})" if m["installed"] else " (absent)")
                     for m in res["missing"])


# ------------------------------------------------------------ pip

def python_console():
    """`python`, beside the `pythonw` the cockpit may run under."""
    exe = sys.executable or "python"
    d, b = os.path.split(exe)
    if b.lower().startswith("pythonw"):
        cand = os.path.join(d, "python" + b[len("pythonw"):])
        if os.path.isfile(cand):
            return cand
    return exe


def pip(*args, timeout=PIP_TIMEOUT, cwd=None):
    """(code, text) of one pip command — never a window, never a prompt."""
    cmd = (list(PIP_COMMAND) if PIP_COMMAND else [python_console(), "-m", "pip"]) + list(args)
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL, cwd=cwd,
                           env=dict(os.environ, PIP_DISABLE_PIP_VERSION_CHECK="1", PIP_NO_INPUT="1"))
    except subprocess.TimeoutExpired:
        return 124, f"pip : pas de fin en {timeout} s"
    except OSError as e:
        return 127, f"pip : {e}"
    return p.returncode, (p.stdout.decode("utf-8", "replace") + "\n" + p.stderr.decode("utf-8", "replace")).strip()


def _tail(text, n=8):
    return "\n".join((text or "").strip().splitlines()[-n:])


def licence_name(meta):
    """The licence a package's metadata declares: its SPDX expression, else
    its short `License` field, else its classifiers."""
    meta = meta or {}
    if meta.get("license_expression"):
        return meta["license_expression"]
    lic = (meta.get("license") or "").strip()
    if lic and len(lic) <= 80 and "\n" not in lic:
        return lic
    cls = [c.split("::")[-1].strip() for c in meta.get("classifier") or [] if c.startswith("License ::")]
    if cls:
        return " / ".join(cls)
    return lic.splitlines()[0][:80] if lic else "non déclarée"


def plan(path=None):
    """What `pip install --user -r requirements.txt` would install:
    {"ok", "packages": [{"name", "version", "licence", "requested"}],
    "message"}. Nothing is installed."""
    with tempfile.TemporaryDirectory(prefix="cockpit-pip-") as d:
        report = os.path.join(d, "report.json")
        code, text = pip("install", "--user", "--dry-run", "--quiet", "--report", report, "-r", path or REQUIREMENTS)
        if code:
            return {"ok": False, "packages": [], "message": f"pip a échoué (code {code}) : {_tail(text)}"}
        try:
            with open(report, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            data = {}
    pkgs = []
    for x in data.get("install") or []:
        meta = x.get("metadata") or {}
        pkgs.append({"name": meta.get("name") or "?", "version": meta.get("version") or "?",
                     "licence": licence_name(meta), "requested": bool(x.get("requested"))})
    return {"ok": True, "packages": pkgs, "message": ""}


_LICENCE_FILE = re.compile(r"(^|/)(LICEN[CS]E|COPYING|NOTICE)[^/]*$", re.I)


def _read_licences(path):
    """The licence files inside a wheel or an sdist, joined."""
    texts = []
    try:
        if path.endswith(".whl") or path.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                for n in sorted(z.namelist()):
                    if _LICENCE_FILE.search(n) and not n.endswith("/"):
                        texts.append((n, z.read(n).decode("utf-8", "replace")))
        elif path.endswith((".tar.gz", ".tgz")):
            with tarfile.open(path) as t:
                for m in t.getmembers():
                    if m.isfile() and _LICENCE_FILE.search(m.name) and m.name.count("/") <= 2:
                        texts.append((m.name, t.extractfile(m).read().decode("utf-8", "replace")))
    except (OSError, zipfile.BadZipFile, tarfile.TarError):
        return ""
    return "\n\n".join(f"── {n} ──\n{t.strip()}" for n, t in texts)


def licence_text(name, version):
    """The full licence of one package, read in its own files — downloaded,
    not installed. (text, where)."""
    with tempfile.TemporaryDirectory(prefix="cockpit-licence-") as d:
        code, text = pip("download", "--no-deps", "--quiet", "-d", d, f"{name}=={version}")
        if code:
            return "", f"le paquet n'a pas pu être lu ({_tail(text, 2)})"
        files = [os.path.join(d, f) for f in os.listdir(d)]
        got = "\n\n".join(t for t in (_read_licences(f) for f in files) if t)
    if not got:
        return "", "le paquet ne contient aucun fichier de licence"
    if len(got) > LICENCE_MAX:
        got = got[:LICENCE_MAX] + f"\n\n[… coupé à {LICENCE_MAX} caractères]"
    return got, ""


def install(path=None):
    """`pip install --user -r requirements.txt`: {"ok", "message",
    "installed": [« name-version »]}."""
    code, text = pip("install", "--user", "-r", path or REQUIREMENTS)
    if code:
        return {"ok": False, "message": f"pip a échoué (code {code}) : {_tail(text)}", "installed": []}
    m = re.search(r"Successfully installed (.+)", text)
    return {"ok": True, "message": "", "installed": m.group(1).split() if m else []}


# ------------------------------------------------------------ the install

def run(mode, decide, say, path=None):
    """The install, in one mode. `decide(kind, title, text) -> bool`: a card
    in « Pas à pas » — `kind` « étape » or « licence »; never called in
    « Rapide ». `say(text)`: one line of what happens. Returns
    {"ok", "outcome", "installed", "licences", "message"}."""
    out = {"ok": False, "outcome": "échec", "installed": [], "licences": [], "message": ""}
    say("pip — ce qui serait installé (pip install --dry-run), rien n'est installé à ce stade")
    p = plan(path)
    if not p["ok"]:
        out["message"] = p["message"]
        return out
    pkgs = p["packages"]
    if not pkgs:
        out.update(ok=True, outcome="rien à installer", message="Toutes les dépendances sont déjà là.")
        return out
    names = sorted({x["licence"] for x in pkgs})
    if mode == RAPIDE:
        say("Rapide — installe : " + ", ".join(f"{x['name']} {x['version']} ({x['licence']})" for x in pkgs)
            + " — licences acceptées d'avance : " + ", ".join(names))
        accepted = [{"name": x["licence"], "package": f"{x['name']} {x['version']}"} for x in pkgs]
    else:
        accepted = []
        for x in pkgs:
            label = f"{x['name']} {x['version']}"
            if not decide("étape", f"Installer {label}", f"pip install --user — {label}"
                          + (" (demandé par requirements.txt)" if x["requested"] else " (une dépendance)")):
                out.update(outcome="refusé", message=f"Étape refusée : {label} — rien n'est installé.")
                return out
            text, why = licence_text(x["name"], x["version"])
            shown = text or f"Licence déclarée : {x['licence']} — {why}."
            if not decide("licence", f"Licence de {label} : {x['licence']}", shown):
                out.update(outcome="refusé", message=f"Licence refusée : {x['licence']} ({label}) — rien n'est installé.")
                return out
            accepted.append({"name": x["licence"], "package": label})
    say("pip install --user -r requirements.txt")
    r = install(path)
    if not r["ok"]:
        out["message"] = r["message"]
        return out
    out.update(ok=True, outcome="installé", installed=r["installed"] or [f"{x['name']}-{x['version']}" for x in pkgs],
               licences=accepted)
    return out


# ------------------------------------------------------------ at start

def _mode_of(config):
    try:
        with open(config, encoding="utf-8") as f:
            m = (json.load(f) or {}).get("install_mode")
    except (OSError, ValueError, AttributeError):
        m = None
    return m if m in (RAPIDE, PAS_A_PAS) else None


def _box(text, title, flags):
    """A Windows message box: what it answered (IDYES 6, IDNO 7, IDOK 1)."""
    try:
        import ctypes
        return ctypes.windll.user32.MessageBoxW(None, text, title, flags)
    except Exception:
        return 0


def at_start(config=None, log=None):
    """Before the server imports its dependencies: each one checked; when
    one is missing, installed — in the mode Paramètres sets, else after one
    question in a window (there is no page yet). Returns True when the
    server may go on."""
    res = check()
    if res["ok"]:
        return True
    config = config or os.path.join(HERE, "config.json")
    lines = []

    def say(t):
        lines.append(t)
        print(f"Dépendances Python — {t}", flush=True)
    say("manquantes : " + missing_text(res))
    mode = _mode_of(config)
    if mode is None:
        a = _box("Il manque des dépendances Python au cockpit : " + missing_text(res) + ".\n\n"
                 "Oui — Rapide : pip les installe sans rien demander d'autre ; les licences des paquets sont "
                 "acceptées d'avance et listées dans logs\\installations.jsonl.\n"
                 "Non — Pas à pas : une fenêtre par paquet, puis une par licence, en entier.\n"
                 "Annuler — rien n'est installé, et le cockpit ne démarre pas.",
                 "Cockpit — dépendances Python", 0x23)
        mode = RAPIDE if a == 6 else PAS_A_PAS if a == 7 else None
    if mode is None:
        say("installation refusée : le cockpit ne démarre pas")
        return False

    def decide(kind, title, text):
        return _box(f"{title}\n\n{text}", f"Cockpit — {kind}", 0x24) == 6
    r = run(mode, decide, say)
    record = {"at": datetime.now().isoformat(timespec="seconds"), "kind": "pip", "title": "Dépendances Python",
              "mode": mode, "outcome": r["outcome"], "installed": r["installed"], "licences": r["licences"],
              "message": r["message"], "steps": lines, "where": "au démarrage"}
    try:
        d = log or os.path.join(HERE, "logs")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "installations.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass
    if not r["ok"]:
        _box("Les dépendances Python n'ont pas été installées : " + (r["message"] or r["outcome"]),
             "Cockpit — dépendances Python", 0x10)
        return False
    refresh_paths()
    return check()["ok"]


def refresh_paths():
    """A `--user` install into a folder that did not exist when Python
    started: added to sys.path, so that this process imports it."""
    import importlib
    import site
    try:
        user = site.getusersitepackages()
        if os.path.isdir(user) and user not in sys.path:
            site.addsitedir(user)
    except Exception:
        pass
    importlib.invalidate_caches()


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
