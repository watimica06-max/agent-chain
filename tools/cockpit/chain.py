"""The chain, installed into an application — TECHNICAL_V1 §20.

The chain is exactly the files under `.claude/CLAUDE.md`, `.claude/agents/`,
`.claude/commands/`, `.claude/scripts/` and `.claude/grids/` of this
repository, read at its `HEAD` — never its working tree. An install copies
them into an application, removes those the previous install wrote and the
chain no longer has, and writes `.claude/chain-version.json`: the chain's
commit, its date, and every installed file with its hash. Nothing else is
ever written in the application; its own files in those folders — its
`commands/deploie.md` — are never touched.

The chain's commit is the last commit of `HEAD` that changed one of its
files: a commit of the cockpit alone leaves every application « à jour ».

A file's hash is the SHA-256 of its bytes, CRLF read as LF: git's autocrlf
rewrites line ends at checkout, and that is not a change.
"""
import hashlib
import json
import os
import subprocess

import gitref

CHAIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PATHS = (".claude/CLAUDE.md", ".claude/agents", ".claude/commands", ".claude/scripts", ".claude/grids")
VERSION_FILE = ".claude/chain-version.json"
GIT_TIMEOUT = 60
PUSH_TIMEOUT = 180

UP_TO_DATE, BEHIND, MODIFIED, ABSENT = "à jour", "en retard", "modifiée sur place", "absente"


class InstallError(Exception):
    """The install refuses, or failed before writing anything."""


class NeedsConfirm(Exception):
    """Files the install would overwrite or remove that the chain did not
    leave as they are: it asks first."""

    def __init__(self, files):
        super().__init__(", ".join(files))
        self.files = files


def _git(repo, *args, data=None, timeout=GIT_TIMEOUT):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    try:
        p = subprocess.run(["git", "-C", repo, "-c", "core.quotepath=off", *args], input=data,
                           capture_output=True, timeout=timeout, env=env,
                           stdin=None if data is not None else subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError) as e:
        raise InstallError(f"git {args[0]} : {e}")
    if p.returncode:
        msg = p.stderr.decode("utf-8", "replace").strip() or p.stdout.decode("utf-8", "replace").strip()
        raise InstallError(f"git {args[0]} : {msg}")
    return p.stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def _file_digest(path):
    try:
        with open(path, "rb") as f:
            return digest(f.read())
    except OSError:
        return None


def _abs(app, rel):
    return os.path.join(app, *rel.split("/"))


# ------------------------------------------------------------ the chain

_chain_cache = {}


def chain_commit(root=CHAIN_ROOT):
    """{"commit", "date", "files": {path: blob id}} — the last commit of
    `HEAD` that changed the chain, and the chain's files there. Kept per
    `HEAD`: reading `HEAD` runs no command."""
    head = gitref.head(root)
    key = (os.path.normcase(root), head)
    if head and key in _chain_cache:
        return _chain_cache[key]
    out = _git(root, "log", "-1", "--format=%H%x00%cI", "HEAD", "--", *PATHS).decode("utf-8").strip()
    if not out:
        raise InstallError("le dépôt de la chaîne n'a aucun commit de la chaîne")
    commit, date = out.split("\0")
    files = {}
    for entry in _git(root, "ls-tree", "-r", "-z", commit, "--", *PATHS).split(b"\0"):
        if not entry:
            continue
        meta, path = entry.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        if kind == "blob":
            files[path.decode("utf-8")] = blob
    info = {"commit": commit, "date": date, "files": dict(sorted(files.items()))}
    if head:
        _chain_cache[key] = info
    return info


def chain_contents(info, root=CHAIN_ROOT):
    """Every file of the chain, its bytes as committed — one `cat-file`."""
    paths = list(info["files"])
    raw = _git(root, "cat-file", "--batch", data="".join(info["files"][p] + "\n" for p in paths).encode())
    out, i = {}, 0
    for p in paths:
        nl = raw.index(b"\n", i)
        size = int(raw[i:nl].split()[2])
        out[p] = raw[nl + 1:nl + 1 + size]
        i = nl + 1 + size + 1
    return out


_behind_cache = {}


def behind(installed, info, root=CHAIN_ROOT):
    """The chain's commits since `installed`, newest first, as « <id> <subject> »;
    None when `installed` is not in the chain's history."""
    key = (os.path.normcase(root), installed, info["commit"])
    if key in _behind_cache:
        return _behind_cache[key]
    try:
        _git(root, "merge-base", "--is-ancestor", installed, info["commit"])
        out = _git(root, "log", "--format=%h %s", f"{installed}..{info['commit']}", "--", *PATHS)
        res = [l for l in out.decode("utf-8", "replace").splitlines() if l.strip()]
    except InstallError:
        res = None
    _behind_cache[key] = res
    return res


# ------------------------------------------------------- the application

def read_version(app):
    """The application's `chain-version.json`: None when absent; raises
    ValueError when unreadable."""
    p = _abs(app, VERSION_FILE)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        v = json.load(f)
    if not (isinstance(v, dict) and isinstance(v.get("commit"), str) and isinstance(v.get("files"), dict)):
        raise ValueError("ni « commit » ni « files »")
    return v


def modified_files(app, version):
    """The installed files whose hash no longer matches, a missing one included."""
    return [p for p, h in sorted(version["files"].items()) if _file_digest(_abs(app, p)) != h]


def _day(iso):
    return (iso or "")[:10]


def state(app, root=CHAIN_ROOT):
    """The chain's state in the application, with the one line that says it."""
    try:
        info = chain_commit(root)
    except InstallError as e:
        return {"state": None, "summary": f"État de la chaîne inconnu — {e}", "error": str(e)}
    out = {"chain_commit": info["commit"][:7], "chain_date": _day(info["date"]),
           "commit": None, "date": None, "behind": None, "subjects": [], "modified": []}
    try:
        v = read_version(app)
    except (OSError, ValueError) as e:
        out.update(state=MODIFIED, modified=[VERSION_FILE],
                   summary=f"Chaîne modifiée sur place — {VERSION_FILE} illisible ({e})")
        return out
    if v is None:
        out.update(state=ABSENT, summary=f"Chaîne absente — aucun {VERSION_FILE}")
        return out
    out.update(commit=v["commit"][:7], date=_day(v.get("date")))
    if v["commit"] != info["commit"]:
        subjects = behind(v["commit"], info, root)
        out["subjects"] = subjects or []
        out["behind"] = len(subjects) if subjects is not None else None
    out["modified"] = modified_files(app, v)
    installed = f"{out['commit']} du {out['date']}"
    if out["modified"]:
        n = len(out["modified"])
        out.update(state=MODIFIED, summary=f"Chaîne modifiée sur place — {n} fichier{'s' if n > 1 else ''} : "
                   + ", ".join(out["modified"]))
    elif v["commit"] != info["commit"]:
        n = out["behind"]
        out.update(state=BEHIND, summary=(f"Chaîne en retard de {n} commit{'s' if n > 1 else ''} — installée : {installed}"
                                          if n is not None else
                                          f"Chaîne en retard — installée : {installed}, un commit que la chaîne n'a pas"))
    else:
        out.update(state=UP_TO_DATE, summary=f"Chaîne à jour — {installed}")
    return out


# ---------------------------------------------------------------- install

def _crlf(app):
    try:
        return _git(app, "config", "--get", "core.autocrlf").decode().strip().lower() == "true"
    except InstallError:
        return False


def _dirty(app, paths):
    """The paths, among `paths`, that git sees changed and not committed."""
    if not paths:
        return []
    out = _git(app, "status", "--porcelain", "-z", "--untracked-files=all", "--", *paths)
    res, parts, i = [], out.split(b"\0"), 0
    while i < len(parts):
        e = parts[i]
        if e:
            res.append(e[3:].decode("utf-8"))
            if e[:1] in (b"R", b"C"):
                i += 1          # the rename's source follows
        i += 1
    return sorted(set(res))


def plan(app, root=CHAIN_ROOT):
    """What an install would do, nothing written: the files to write, to
    remove, those it asks before overwriting, and why it would refuse."""
    app = os.path.abspath(app)
    if os.path.normcase(app) == os.path.normcase(os.path.abspath(root)):
        raise InstallError("c'est le dépôt de la chaîne lui-même")
    try:
        top = _git(app, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    except InstallError:
        raise InstallError("le dossier de l'application n'est pas un dépôt git")
    if os.path.normcase(os.path.abspath(top)) != os.path.normcase(app):
        raise InstallError(f"le dossier de l'application n'est pas la racine de son dépôt ({top})")
    try:
        prev = read_version(app)
    except (OSError, ValueError) as e:
        raise InstallError(f"{VERSION_FILE} illisible ({e}) : le corriger, ou le supprimer — "
                           "l'installation demandera alors avant de remplacer chaque fichier")
    managed = sorted(set(prev["files"]) | {VERSION_FILE}) if prev else []
    dirty = _dirty(app, managed)
    if dirty:
        raise InstallError("des fichiers de la chaîne ont des modifications non commitées dans "
                           "l'application : " + ", ".join(dirty))
    info = chain_commit(root)
    contents = chain_contents(info, root)
    new = {p: digest(b) for p, b in contents.items()}
    write = [p for p in contents if _file_digest(_abs(app, p)) != new[p]]
    remove = sorted(p for p in (prev["files"] if prev else {}) if p not in contents
                    and os.path.exists(_abs(app, p)))
    # What the chain did not leave as it is: changed in place since the last
    # install, or, with none, any file it would replace.
    if prev:
        changed = set(modified_files(app, prev))
        ask = [p for p in sorted(set(write) | set(remove)) if p in changed and os.path.exists(_abs(app, p))]
        ask += [p for p in write if p not in prev["files"] and os.path.exists(_abs(app, p))]
    else:
        ask = [p for p in write if os.path.exists(_abs(app, p))]
    return {"info": info, "contents": contents, "hashes": new, "write": write, "remove": remove,
            "ask": sorted(set(ask)), "previous": prev}


def version_text(info, hashes, crlf=False):
    text = json.dumps({"commit": info["commit"], "date": info["date"], "files": dict(sorted(hashes.items()))},
                      ensure_ascii=False, indent=2) + "\n"
    return text.replace("\n", "\r\n") if crlf else text


def install(app, root=CHAIN_ROOT, confirm=False, push=True):
    """Copies the chain into the application, commits those files alone —
    `chain: <id> <date>` — and pushes. Raises InstallError on a refusal,
    NeedsConfirm when it must ask first."""
    app = os.path.abspath(app)
    pl = plan(app, root)
    if pl["ask"] and not confirm:
        raise NeedsConfirm(pl["ask"])
    info, crlf = pl["info"], _crlf(app)
    for p in pl["write"]:
        data = pl["contents"][p]
        if crlf:
            data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        target = _abs(app, p)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)
    for p in pl["remove"]:
        os.remove(_abs(app, p))
    vpath = _abs(app, VERSION_FILE)
    text = version_text(info, pl["hashes"], crlf)
    old = None
    if os.path.exists(vpath):
        with open(vpath, "rb") as f:
            old = f.read()
    if old != text.encode("utf-8"):
        with open(vpath, "wb") as f:
            f.write(text.encode("utf-8"))
    touched = sorted(set(pl["contents"]) | set(pl["remove"]) | {VERSION_FILE})
    changed = _dirty(app, touched)
    result = {"commit": info["commit"][:7], "date": _day(info["date"]), "written": pl["write"],
              "removed": pl["remove"], "app_commit": None, "pushed": False, "push_error": None}
    if not changed:
        return result
    _git(app, "add", "-A", "--", *changed)
    message = f"chain: {info['commit'][:7]} {_day(info['date'])}"
    _git(app, "commit", "-q", "-m", message, "--only", "--", *changed)
    result["app_commit"] = _git(app, "rev-parse", "--short", "HEAD").decode().strip()
    result["message"] = message
    if push:
        try:
            _git(app, "push", "-q", timeout=PUSH_TIMEOUT)
            result["pushed"] = True
        except InstallError as e:
            result["push_error"] = str(e)
    return result
