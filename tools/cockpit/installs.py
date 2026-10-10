"""The repairs that take a while — cockpit 1.16: signing in to Claude or to
GitHub, the Python dependencies, Claude Code itself, and « Installer avec
Claude » for a missing tool.

One at a time, each in its own thread: a `Session` says what it does, step by
step, to every page (`emit`). What only she can decide waits on her:

- a sign-in: the address of the browser page, and the code that page may
  show, pasted back (`claude auth login` reads it on its standard input —
  established with a throwaway CLAUDE_CONFIG_DIR: it needs no console);
- « Pas à pas »: a card for every step and every licence, shown in full,
  accepted or refused; a refused licence stops the install;
- « Rapide »: nothing after the start — one line before it names what will
  be installed and the licences this accepts; the report after lists both.

Every session ends in logs/installations.jsonl: what was installed, every
licence accepted, in which mode.
"""
import asyncio
import json
import os
import re
import subprocess
import threading
import time
import uuid
from datetime import datetime

import deps

RAPIDE, PAS_A_PAS, DEMANDER = deps.RAPIDE, deps.PAS_A_PAS, "demander"
MODES = (RAPIDE, PAS_A_PAS)
LOGIN_TIMEOUT = 600.0
INSTALL_TIMEOUT = 1800.0
LOG_NAME = "installations.jsonl"
HIDDEN = 0x08000000 if os.name == "nt" else 0          # CREATE_NO_WINDOW

# What neither mode can skip — said before an install starts.
UAC = "la fenêtre d'administrateur de Windows (UAC), si l'installation la demande"
BROWSER_SIGNIN = "la connexion dans le navigateur"

# The commands the sessions start; the tests put fakes here.
CLAUDE_LOGIN = None          # argv before nothing: [cli, "auth", "login"] when None
GCM_LOGIN = ["git", "credential-manager", "github", "login", "--browser"]
CLAUDE_INSTALL = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                  "irm https://claude.ai/install.ps1 | iex"]

# « Installer avec Claude »: one brief per tool. `licences`: those the install
# is expected to meet, named before it starts — the only ones « Rapide »
# accepts.
WINGET_SOURCE = "Contrat de la source winget (Microsoft)"
ANDROID_SDK = "Android Software Development Kit License Agreement"
TOOLS = {
    "java": {"label": "Java (JDK 17)", "proof": "java -version",
             "what": "Eclipse Temurin JDK 17 par winget (EclipseAdoptium.Temurin.17.JDK), puis JAVA_HOME dans les "
                     "variables d'environnement de l'utilisateur",
             "licences": [WINGET_SOURCE, "GPLv2 avec Classpath Exception (Eclipse Temurin)"], "uac": True},
    "adb": {"label": "adb (Android SDK Platform-Tools)", "proof": "adb version",
            "what": "les platform-tools du SDK Android — par sdkmanager s'il est là, sinon par winget "
                    "(Google.PlatformTools) —, et leur dossier dans le PATH de l'utilisateur",
            "licences": [ANDROID_SDK, WINGET_SOURCE], "uac": False},
    "sdkmanager": {"label": "sdkmanager (Android command-line tools)", "proof": "sdkmanager --version",
                   "what": "les command-line tools du SDK Android, téléchargés depuis dl.google.com dans "
                           "%LOCALAPPDATA%\\Android\\Sdk\\cmdline-tools\\latest",
                   "licences": [ANDROID_SDK], "uac": False},
    "android_sdk": {"label": "SDK Android (ANDROID_HOME)", "proof": "sdkmanager --list_installed",
                    "what": "le dossier du SDK Android (%LOCALAPPDATA%\\Android\\Sdk) avec ses command-line tools "
                            "et ses platform-tools, puis ANDROID_HOME dans les variables de l'utilisateur",
                    "licences": [ANDROID_SDK], "uac": False},
    "emulator": {"label": "Émulateur Android", "proof": "emulator -version",
                 "what": "le paquet « emulator » du SDK Android, par sdkmanager",
                 "licences": [ANDROID_SDK], "uac": False},
    "scrcpy": {"label": "scrcpy", "proof": "scrcpy --version",
               "what": "scrcpy par winget (Genymobile.scrcpy)",
               "licences": [WINGET_SOURCE, "Apache License 2.0 (scrcpy)"], "uac": False},
    "git": {"label": "Git pour Windows (avec Git Credential Manager)", "proof": "git credential-manager --version",
            "what": "Git pour Windows par winget (Git.Git), qui apporte Git Credential Manager",
            "licences": [WINGET_SOURCE, "GNU GPL v2 (Git pour Windows)"], "uac": True},
    "flutter": {"label": "Flutter", "proof": "flutter --version",
                "what": "le SDK Flutter, branche stable, cloné dans %LOCALAPPDATA%\\flutter, et son dossier bin dans "
                        "le PATH de l'utilisateur",
                "licences": ["BSD 3-Clause (Flutter)"], "uac": False},
}

BRIEF = """You are installing one tool on this Windows computer, for the cockpit of the agent chain. You run with no \
project: nothing else on this computer is yours to change.

The tool: {label}.
How: {what}.
Prove it answers once installed: `{proof}` — run it, and quote its first line.

Rules:
- Install this tool only, for the current user when the installer allows it. Never uninstall or upgrade anything \
else, never change a setting this install does not need.
- A licence or an agreement — a winget `--accept-package-agreements` / `--accept-source-agreements` flag, \
`sdkmanager --licenses`, an installer's EULA — is accepted only through the tool `mcp__cockpit__licence`: call it \
first with the licence's name and its FULL text (read it: `winget show --id <id>` gives the licence address, \
`sdkmanager --licenses` prints each one). Go on only when it answers « acceptée »; when it answers « refusée », stop \
at once, install nothing more, and say so.
- The licences named before this install started: {licences}. When the licence you meet is one of them, give its \
name exactly as written here.
- If a step will open the Windows administrator window (UAC), say so in one sentence just before that step.
- A tool added to the PATH or a variable such as JAVA_HOME or ANDROID_HOME: set it in the user's environment \
(the registry, `setx`), never only in this shell.
- End with one line, and nothing after it: `Résultat : installé — <the proof's first line>` or \
`Résultat : échec — <why>`.
"""


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


class Refused(Exception):
    pass


class Cancelled(Exception):
    pass


class Session:
    def __init__(self, kind, title, mode=None, target=None, emit=None):
        self.id = uuid.uuid4().hex[:10]
        self.kind, self.title, self.mode, self.target = kind, title, mode, target
        self.status = "going"            # going, waiting, ended
        self.outcome = ""                # installé, connecté, refusé, échec, annulé…
        self.message = ""
        self.steps = []
        self.card = None                 # {id, kind, title, text}
        self.url = ""
        self.code_wanted = False
        self.installed, self.licences = [], []
        self.started_at, self.ended_at = now_iso(), ""
        self.log_path = ""
        self.restart = False             # PATH or a dependency changed: the cockpit restarts
        self._emit = emit or (lambda s: None)
        self._answer = threading.Event()
        self._accepted = False
        self._cancel = threading.Event()
        self.proc = None
        self.seq = 0                     # each snapshot told: a page keeps the newest

    def snapshot(self):
        return {"id": self.id, "seq": self.seq, "kind": self.kind, "title": self.title, "mode": self.mode, "target": self.target,
                "status": self.status, "outcome": self.outcome, "message": self.message, "steps": self.steps[-60:],
                "card": self.card, "url": self.url, "code_wanted": self.code_wanted, "installed": self.installed,
                "licences": self.licences, "started_at": self.started_at, "ended_at": self.ended_at,
                "log_path": self.log_path, "restart": self.restart}

    def emit(self):
        self.seq += 1
        try:
            self._emit(self.snapshot())
        except Exception:
            pass

    def say(self, text):
        self.steps.append({"at": now_iso(), "text": text})
        print(f"État de l'ordinateur — {self.title} : {text}", flush=True)
        self.emit()

    @property
    def cancelled(self):
        return self._cancel.is_set()

    def decide(self, kind, title, text):
        """A card, and the wait for her answer: True when accepted. In
        « Rapide » never called for a step; a licence is then accepted only
        when it was named before the start."""
        if self.cancelled:
            raise Cancelled()
        self._answer.clear()
        self.card = {"id": uuid.uuid4().hex[:8], "kind": kind, "title": title, "text": text}
        self.status = "waiting"
        self.emit()
        while not self._answer.wait(0.5):
            if self.cancelled:
                self.card = None
                raise Cancelled()
        ok = self._accepted
        self.say(f"{'Accepté' if ok else 'Refusé'} — {title}")
        self.card = None
        self.status = "going"
        self.emit()
        return ok

    def answer(self, card_id, accept):
        if not self.card or self.card["id"] != card_id:
            return False
        self._accepted = bool(accept)
        self._answer.set()
        return True

    def cancel(self):
        self._cancel.set()
        p = self.proc
        if p is not None and p.poll() is None:
            try:
                p.kill()
            except OSError:
                pass


class Installs:
    """The one session going, and the last one ended."""

    def __init__(self, log_dir, emit=None):
        self.log_dir = log_dir
        self.emit = emit or (lambda s: None)
        self.current = None
        self.last = None
        self._lock = threading.Lock()

    def going(self):
        c = self.current
        return c if c is not None and c.status != "ended" else None

    def public(self):
        c = self.going() or self.last
        return c.snapshot() if c else None

    def start(self, kind, title, work, mode=None, target=None, after=None):
        """`work(session)` runs in a thread; `after(session)` once it ended —
        the check again, a restart."""
        with self._lock:
            if self.going():
                raise RuntimeError(f"« {self.current.title} » est en cours : une réparation à la fois")
            s = Session(kind, title, mode, target, self.emit)
            self.current = s

        def run():
            try:
                work(s)
            except Cancelled:
                s.outcome, s.message = "annulé", s.message or "Arrêté depuis le cockpit."
            except Refused as e:
                s.outcome, s.message = "refusé", str(e)
            except Exception as e:      # said, never raised
                s.outcome, s.message = "échec", f"{type(e).__name__}: {e}"
            finally:
                s.card, s.code_wanted = None, False
                s.status, s.ended_at = "ended", now_iso()
                self.record(s)
                self.last = s
                if after:
                    try:
                        after(s)
                    except Exception as e:
                        s.message += f" (vérification après : {e})"
                s.emit()
        threading.Thread(target=run, daemon=True, name=f"install-{kind}").start()
        s.emit()
        return s

    def record(self, s):
        """What was installed and every licence accepted, kept in the logs."""
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            with open(os.path.join(self.log_dir, LOG_NAME), "a", encoding="utf-8") as f:
                f.write(json.dumps({"at": s.ended_at or now_iso(), "kind": s.kind, "title": s.title, "mode": s.mode,
                                    "target": s.target, "outcome": s.outcome, "message": s.message,
                                    "installed": s.installed, "licences": s.licences,
                                    "steps": [x["text"] for x in s.steps], "log_path": s.log_path},
                                   ensure_ascii=False) + "\n")
        except OSError:
            pass


# ------------------------------------------------------------ the sign-ins

def _reader(proc, sink):
    def go():
        for chunk in iter(lambda: proc.stdout.read1(4096) if hasattr(proc.stdout, "read1") else proc.stdout.read(1),
                          b""):
            sink(chunk.decode("utf-8", "replace"))
    t = threading.Thread(target=go, daemon=True)
    t.start()
    return t


_URL = re.compile(r"https://\S+")


def _wait(s, proc, timeout):
    deadline = time.monotonic() + timeout
    while proc.poll() is None:
        if s.cancelled:
            proc.kill()
            raise Cancelled()
        if time.monotonic() > deadline:
            proc.kill()
            raise Refused(f"pas de connexion en {int(timeout / 60)} minutes : arrêtée")
        time.sleep(0.3)
    return proc.returncode


def claude_login(cli, env, verify):
    """`claude auth login` with the CLI the SDK runs, no window: it opens the
    browser and prints the address; a code the page shows comes back on its
    standard input. Then `claude auth status`."""
    def work(s):
        argv = list(CLAUDE_LOGIN) if CLAUDE_LOGIN else [cli, "auth", "login"]
        s.say("claude auth login — la page de connexion s'ouvre dans le navigateur")
        p = subprocess.Popen(argv, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             creationflags=HIDDEN)
        s.proc = p
        seen = {"text": ""}

        def sink(t):
            seen["text"] += t
            m = _URL.search(seen["text"])
            if m and not s.url:
                s.url = m.group(0)
                s.code_wanted = True
                s.status = "waiting"
                s.emit()
        _reader(p, sink)
        code = _wait(s, p, LOGIN_TIMEOUT)
        s.code_wanted = False
        s.status = "going"
        ok, detail = verify()
        tail = " ".join(seen["text"].split())[-300:]
        if code == 0 and ok:
            s.outcome, s.message = "connecté", detail
        else:
            s.outcome = "échec"
            s.message = (f"claude auth login a fini (code {code}) : {tail}" if code else "") \
                + ("" if ok else (" — " if code else "") + f"claude auth status : {detail}")
        s.say(s.message)
    return work


def send_code(s, code):
    """The code the sign-in page shows, written to `claude auth login`."""
    p = s.proc
    if p is None or p.poll() is not None or not s.code_wanted:
        return False
    try:
        p.stdin.write((code.strip() + "\n").encode("utf-8"))
        p.stdin.flush()
    except OSError:
        return False
    s.say("Code transmis à Claude Code")
    return True


def gcm_env():
    """Git Credential Manager allowed to open the browser: without
    GCM_INTERACTIVE=never, which every other git call of the cockpit sets."""
    return {k: v for k, v in os.environ.items() if k not in ("GCM_INTERACTIVE", "GIT_TERMINAL_PROMPT")}


def github_login(verify):
    """`git credential-manager github login --browser`, no window — it
    needs none: the browser page, then a push that sends nothing."""
    def work(s):
        s.say("git credential-manager github login --browser — la page de GitHub s'ouvre dans le navigateur")
        p = subprocess.Popen(list(GCM_LOGIN), env=gcm_env(), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, creationflags=HIDDEN)
        s.proc = p
        seen = {"text": ""}
        _reader(p, lambda t: seen.__setitem__("text", seen["text"] + t))
        code = _wait(s, p, LOGIN_TIMEOUT)
        s.say("git push --dry-run sur agent-chain")
        ok, detail = verify()
        if code == 0 and ok:
            s.outcome, s.message = "connecté", detail
        else:
            s.outcome = "échec"
            s.message = (f"Git Credential Manager a fini (code {code}) : {' '.join(seen['text'].split())[-300:]}"
                         if code else "") + ("" if ok else (" — " if code else "") + detail)
        s.say(s.message)
    return work


# ------------------------------------------------------------ the Python dependencies

def pip_install(mode, path=None):
    def work(s):
        r = deps.run(mode, s.decide, s.say, path)
        s.installed, s.licences = r["installed"], r["licences"]
        s.outcome, s.message = r["outcome"], r["message"]
        if r["ok"] and r["installed"]:
            s.restart = True
            s.message = s.message or "Installées : le cockpit redémarre pour les prendre."
        if not r["ok"] and r["outcome"] == "refusé":
            raise Refused(r["message"])
    return work


def describe_pip(path=None):
    p = deps.plan(path)
    if not p["ok"]:
        return {"error": p["message"]}
    return {"what": [f"{x['name']} {x['version']}" for x in p["packages"]],
            "licences": sorted({x["licence"] for x in p["packages"]}), "unskippable": []}


# ------------------------------------------------------------ Claude Code itself

def claude_code(mode, cli, verify):
    """Claude Code installed (its official installer), or updated
    (`claude update`). No licence to accept at the install: Anthropic's terms
    are accepted at the sign-in, in the browser."""
    def work(s):
        argv = [cli, "update"] if cli else list(CLAUDE_INSTALL)
        what = "claude update" if cli else "l'installateur officiel (irm https://claude.ai/install.ps1 | iex)"
        if mode == RAPIDE:
            s.say(f"Rapide — {what} ; aucune licence à accepter à l'installation")
        elif not s.decide("étape", "Mettre à jour Claude Code" if cli else "Installer Claude Code",
                          f"{' '.join(argv)}\n\nAucune licence à accepter à l'installation : les conditions "
                          "d'Anthropic s'acceptent à la connexion, dans le navigateur."):
            raise Refused("Étape refusée : rien n'est installé.")
        s.say(" ".join(argv))
        try:
            p = subprocess.run(argv, capture_output=True, timeout=INSTALL_TIMEOUT, stdin=subprocess.DEVNULL,
                               creationflags=HIDDEN)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(f"{argv[0]} : {e}")
        text = (p.stdout.decode("utf-8", "replace") + "\n" + p.stderr.decode("utf-8", "replace")).strip()
        if p.returncode:
            s.outcome, s.message = "échec", f"code {p.returncode} : {' '.join(text.split())[-300:]}"
            s.say(s.message)
            return
        ok, detail = verify()
        s.installed = ["Claude Code"]
        s.outcome, s.message = ("installé", detail) if ok else ("échec", detail)
        s.restart = ok and not cli
        s.say(s.message)
    return work


# ------------------------------------------------------------ « Installer avec Claude »

def _norm(name):
    return re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip()


def describe_tool(tool):
    t = TOOLS.get(tool)
    if not t:
        return {"error": f"outil inconnu : {tool}"}
    return {"what": [t["label"] + " — " + t["what"]], "licences": list(t["licences"]),
            "unskippable": [UAC] if t.get("uac") else []}


def brief(tool):
    t = TOOLS[tool]
    return BRIEF.format(label=t["label"], what=t["what"], proof=t["proof"],
                        licences="; ".join(f"« {x} »" for x in t["licences"]))


def sdk_client(workdir, can_use_tool, licence):
    """The SDK client of an install: no project settings loaded — nothing is
    pre-allowed, every step reaches `can_use_tool` — and one tool of the
    cockpit, `licence`."""
    from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, create_sdk_mcp_server, tool

    @tool("licence", "Ask the Product Owner to accept a licence or an agreement before accepting it. "
                     "Give its exact name and its full text. Answers « acceptée » or « refusée ».",
          {"nom": str, "texte": str, "source": str})
    async def licence_tool(args):
        ok = await licence(args.get("nom") or "", args.get("texte") or "", args.get("source") or "")
        return {"content": [{"type": "text", "text": "acceptée" if ok else
                             "refusée — arrête l'installation maintenant, n'installe rien de plus"}]}
    server = create_sdk_mcp_server("cockpit", tools=[licence_tool])
    return ClaudeSDKClient(options=ClaudeAgentOptions(
        cwd=workdir, can_use_tool=can_use_tool, permission_mode="default", setting_sources=[],
        mcp_servers={"cockpit": server}, env={"CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS": "1"}))


CLIENT_FACTORY = sdk_client


def _step_text(name, data):
    if name == "Bash":
        return data.get("command") or json.dumps(data, ensure_ascii=False)
    if name in ("Write", "Edit"):
        return f"{data.get('file_path', '')}"
    try:
        shown = json.dumps(data, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        shown = str(data)
    return shown[:4000]


def with_claude(tool, mode, workdir, log_path, verify):
    """A Claude run with the tool's brief. « Pas à pas »: every step it asks
    for is a card, every licence a card with its full text. « Rapide »: the
    steps go; a licence named before the start is accepted, any other is
    refused and the install stops."""
    t = TOOLS[tool]
    announced = {_norm(x): x for x in t["licences"]}

    def work(s):
        from runner import _body
        os.makedirs(workdir, exist_ok=True)
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        s.log_path = log_path
        if mode == RAPIDE:
            s.say(f"Rapide — installe : {t['label']} ({t['what']}) — licences acceptées d'avance : "
                  + ", ".join(t["licences"]))
        refused = {"licence": None}

        def licence_decide(name, text, source):
            if s.cancelled:
                raise Cancelled()
            if mode == RAPIDE:
                hit = announced.get(_norm(name))
                if hit:
                    s.licences.append({"name": hit, "source": source})
                    s.say(f"Licence acceptée (nommée avant le départ) : {hit}")
                    return True
                refused["licence"] = name
                s.say(f"Licence refusée : « {name} » n'a pas été nommée avant le départ — l'installation s'arrête")
                return False
            ok = s.decide("licence", f"Licence : {name}", (text or "(texte vide)")
                          + (f"\n\nSource : {source}" if source else ""))
            if ok:
                s.licences.append({"name": name, "source": source})
            else:
                refused["licence"] = name
            return ok

        async def drive():
            from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny
            loop = asyncio.get_running_loop()

            async def can_use_tool(name, data, ctx):
                if name.endswith("__licence"):
                    return PermissionResultAllow()
                if refused["licence"]:
                    return PermissionResultDeny(message="Licence refusée : l'installation s'arrête", interrupt=True)
                text = _step_text(name, data or {})
                if mode == RAPIDE:
                    s.say(f"Étape — {name} : {text.splitlines()[0][:200] if text else ''}")
                    return PermissionResultAllow()
                ok = await loop.run_in_executor(None, s.decide, "étape", f"{name}", text)
                return PermissionResultAllow() if ok else PermissionResultDeny(
                    message="Refusé par le Product Owner depuis le cockpit : arrête l'installation", interrupt=True)

            async def licence(name, text, source):
                return await loop.run_in_executor(None, licence_decide, name, text, source)

            last = ""
            client = CLIENT_FACTORY(workdir, can_use_tool, licence)
            async with client:
                await client.query(brief(tool))
                async for msg in client.receive_response():
                    body = _body(msg)
                    try:
                        with open(log_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps({"at": now_iso(), "type": type(msg).__name__, "message": body},
                                               ensure_ascii=False, default=str) + "\n")
                    except (OSError, TypeError, ValueError):
                        pass
                    if isinstance(body, dict):
                        for b in body.get("content") or []:
                            if isinstance(b, dict) and isinstance(b.get("text"), str) and b["text"].strip():
                                last = b["text"]
                                s.say(" ".join(b["text"].split())[:300])
                        if type(msg).__name__ == "ResultMessage":
                            last = body.get("result") or last
                    if s.cancelled:
                        await client.interrupt()
            return last

        before = path_now()
        last = asyncio.run(asyncio.wait_for(drive(), INSTALL_TIMEOUT))
        if refused["licence"]:
            raise Refused(f"Licence refusée : {refused['licence']} — l'installation s'est arrêtée.")
        m = re.search(r"Résultat\s*:\s*(installé|échec)\s*[—-]?\s*(.*)", last or "")
        ok, detail = verify()
        if m and m.group(1) == "installé" and ok:
            s.installed = [t["label"]]
            s.outcome, s.message = "installé", f"{m.group(2).strip()} — {detail}"
        else:
            s.outcome = "échec"
            s.message = (m.group(2).strip() if m else " ".join((last or "aucun résultat").split())[-300:]) \
                + (f" — {detail}" if not ok else "")
        s.restart = path_now() != before
        if s.restart:
            s.say("Le PATH de Windows a changé : le cockpit redémarre pour le prendre.")
        s.say(s.message)
    return work


# ------------------------------------------------------------ Windows' environment

def registry_env():
    """PATH and the variables a tool install sets, as Windows has them now —
    not as this process inherited them: {name: value}."""
    out = {}
    if os.name != "nt":
        return out
    try:
        import winreg
    except ImportError:
        return out
    paths = []
    for hive, sub in ((winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
                      (winreg.HKEY_CURRENT_USER, "Environment")):
        try:
            with winreg.OpenKey(hive, sub) as k:
                for name in ("Path", "JAVA_HOME", "ANDROID_HOME", "ANDROID_SDK_ROOT"):
                    try:
                        v, _ = winreg.QueryValueEx(k, name)
                    except OSError:
                        continue
                    v = os.path.expandvars(str(v))
                    if name == "Path":
                        paths.append(v)
                    else:
                        out[name] = v
        except OSError:
            continue
    if paths:
        out["PATH"] = ";".join(p.strip(";") for p in paths if p)
    return out


REGISTRY = registry_env


def path_now():
    return REGISTRY().get("PATH", "")


def fresh_env():
    """The environment a restarted cockpit gets: this one, with PATH and the
    tools' variables as Windows has them now."""
    env = dict(os.environ)
    env.update(REGISTRY())
    return env
