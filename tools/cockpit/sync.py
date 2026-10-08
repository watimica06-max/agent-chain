"""Always agreeing with GitHub — cockpit 1.12.

The Product Owner works on the same applications from two computers, never
at the same time. Each clone fetches, and says where it stands against
GitHub: « à jour », « en retard » (GitHub has commits this clone lacks),
« non envoyé » (this clone has commits GitHub lacks), « divergé » (both),
« GitHub injoignable » — or « sans GitHub », a repository with no remote.

The sync lives in the cockpit alone: no command of the chain changes, and a
command run outside the cockpit gets none.

Every git command here runs with GIT_TERMINAL_PROMPT=0 and Git Credential
Manager's prompts off (`env()`), under a timeout; never --force, never a
reset, never a stash, never a merge commit of its own — a pull is
`--ff-only`, a reconciliation a rebase that keeps the merges already made
(1.12.1: each command merges its worktree `--no-ff`, `Merge /<command>`).
"""
import os
import re
import subprocess
import threading
from datetime import datetime

GIT_TIMEOUT = 30
FETCH_TIMEOUT = 30
PULL_TIMEOUT = 120
PUSH_TIMEOUT = 180
CLONE_TIMEOUT = 900

UP_TO_DATE, BEHIND, AHEAD, DIVERGED, OFFLINE, NO_REMOTE = (
    "à jour", "en retard", "non envoyé", "divergé", "GitHub injoignable", "sans GitHub")
ANSWERS_MESSAGE = "chore: answers"

CREDENTIALS_TEXT = ("GitHub refuse : aucun identifiant GitHub utilisable sur cet ordinateur pour ce dépôt. "
                    "Se connecter une fois à GitHub avec git sur cet ordinateur (Git Credential Manager), "
                    "puis réessayer — le cockpit ne demande jamais de mot de passe.")


def env(extra=None):
    """Never a prompt: no terminal one, no Git Credential Manager window."""
    e = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    e.update(extra or {})
    return e


class Git:
    """One git command's outcome: its code, its two outputs, decoded."""

    def __init__(self, code, out, err):
        self.code, self.out, self.err = code, out, err

    @property
    def ok(self):
        return self.code == 0

    @property
    def text(self):
        return (self.err or self.out).strip()


def git(folder, *args, timeout=GIT_TIMEOUT):
    try:
        p = subprocess.run(["git", "-C", folder, "-c", "core.quotepath=off", *args], capture_output=True,
                           timeout=timeout, env=env(), stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return Git(124, "", f"git {args[0]} : pas de réponse en {timeout} s")
    except OSError as e:
        return Git(127, "", f"git {args[0]} : {e}")
    return Git(p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"))


# ------------------------------------------------------------ why git failed

_CREDENTIALS = re.compile(r"Authentication failed|could not read Username|could not read Password|"
                          r"terminal prompts disabled|Cannot prompt because|interactivity has been disabled|"
                          r"Permission denied \(publickey|Invalid username or password|HTTP Basic: Access denied|"
                          r"returned error: 40[13]|The requested URL returned error: 403", re.I)
_OFFLINE = re.compile(r"Could not resolve host|unable to access|Failed to connect|Connection refused|"
                      r"Connection timed out|timed out|Network is unreachable|Could not read from remote|"
                      r"pas de réponse en|unable to connect|Temporary failure", re.I)
_REJECTED = re.compile(r"\[rejected\]|non-fast-forward|fetch first|Updates were rejected", re.I)


def credentials(text):
    return bool(_CREDENTIALS.search(text or ""))


def explain(text):
    """What a failed network command means, in French — the credentials case
    said plainly, never as git's prompt."""
    text = (text or "").strip()
    if credentials(text):
        return CREDENTIALS_TEXT
    if "Repository not found" in text or "does not appear to be a git repository" in text:
        return ("GitHub ne trouve pas ce dépôt — l'adresse est fausse, ou il est privé et cet ordinateur "
                f"n'a pas d'identifiant GitHub pour lui ({text.splitlines()[-1] if text else ''})")
    if _OFFLINE.search(text):
        return f"GitHub injoignable — {text.splitlines()[-1] if text else ''}"
    return text


# ------------------------------------------------------------ the state

def _counts(text):
    a, b = (text.split() + ["0", "0"])[:2]
    return int(a), int(b)


def dirty_paths(folder, pathspec=()):
    """[(code, path)] git sees changed and not committed — untracked included."""
    r = git(folder, "--no-optional-locks", "status", "--porcelain", "-z", "--untracked-files=all",
            *(["--", *pathspec] if pathspec else []))
    if not r.ok:
        return None
    out, parts, i = [], r.out.split("\0"), 0
    while i < len(parts):
        e = parts[i]
        if e:
            out.append((e[:2], e[3:]))
            if e[:1] in ("R", "C"):
                i += 1          # the rename's source follows
        i += 1
    return out


def summary(st):
    s = st.get("state")
    n = lambda k, one, many: f"{st.get(k) or 0} {one if (st.get(k) or 0) <= 1 else many}"  # noqa: E731
    if s == UP_TO_DATE:
        return "À jour avec GitHub"
    if s == BEHIND:
        return f"En retard : GitHub a {n('behind', 'commit', 'commits')} que cet ordinateur n'a pas"
    if s == AHEAD:
        return f"Non envoyé : {n('ahead', 'commit', 'commits')} de cet ordinateur pas encore sur GitHub"
    if s == DIVERGED:
        return (f"Divergé : {n('ahead', 'commit', 'commits')} ici que GitHub n'a pas, "
                f"{n('behind', 'commit', 'commits')} sur GitHub qu'ici on n'a pas")
    if s == OFFLINE:
        return "GitHub injoignable — l'état n'est pas vérifié" + (f" ({st['detail']})" if st.get("detail") else "")
    if s == NO_REMOTE:
        return "Sans GitHub — ce dépôt n'a pas de dépôt distant"
    return st.get("detail") or "état inconnu"


def compute(folder, fetch=True):
    """Where this clone stands against GitHub — `git fetch` first."""
    st = {"state": None, "ahead": 0, "behind": 0, "branch": None, "remote": None, "upstream": None,
          "uncommitted": None, "detail": "", "credentials": False,
          "at": datetime.now().isoformat(timespec="seconds"), "fetched": False}
    if not folder or not os.path.isdir(folder):
        st["detail"] = "dossier introuvable"
        st["summary"] = summary(st)
        return st
    b = git(folder, "symbolic-ref", "-q", "--short", "HEAD")
    if not b.ok:
        inside = git(folder, "rev-parse", "--is-inside-work-tree")
        st["detail"] = ("HEAD détachée : aucune branche à comparer à GitHub" if inside.ok
                        else "pas un dépôt git")
        st["summary"] = summary(st)
        return st
    branch = st["branch"] = b.out.strip()
    d = dirty_paths(folder)
    st["uncommitted"] = len(d) if d is not None else None
    remote = git(folder, "config", "--get", f"branch.{branch}.remote").out.strip()
    remotes = git(folder, "remote").out.split()
    if not remote or remote == ".":
        remote = "origin" if "origin" in remotes else (remotes[0] if len(remotes) == 1 else "")
    if not remote:
        st["state"] = NO_REMOTE
        st["summary"] = summary(st)
        return st
    st["remote"] = remote
    if fetch:
        f = git(folder, "fetch", "-q", remote, timeout=FETCH_TIMEOUT)
        if not f.ok:
            st.update(state=OFFLINE, credentials=credentials(f.text), detail=explain(f.text))
            st["summary"] = summary(st)
            return st
        st["fetched"] = True
    up = git(folder, "rev-parse", "-q", "--verify", "--symbolic-full-name", f"{branch}@{{upstream}}")
    ref = up.out.strip() if up.ok and up.out.strip() else ""
    if not ref:
        cand = f"refs/remotes/{remote}/{branch}"
        ref = cand if git(folder, "rev-parse", "-q", "--verify", cand).ok else ""
    has_head = git(folder, "rev-parse", "-q", "--verify", "HEAD").ok
    if not ref:
        # GitHub has no such branch yet: everything here is « non envoyé ».
        st["ahead"] = int(git(folder, "rev-list", "--count", "HEAD").out.strip() or 0) if has_head else 0
        st["state"] = AHEAD if st["ahead"] else UP_TO_DATE
        st["summary"] = summary(st)
        return st
    st["upstream"] = ref.replace("refs/remotes/", "", 1)
    if not has_head:
        st.update(state=BEHIND, behind=int(git(folder, "rev-list", "--count", ref).out.strip() or 0))
        st["summary"] = summary(st)
        return st
    c = git(folder, "rev-list", "--left-right", "--count", f"HEAD...{ref}")
    st["ahead"], st["behind"] = _counts(c.out) if c.ok else (0, 0)
    st["state"] = (DIVERGED if st["ahead"] and st["behind"] else AHEAD if st["ahead"]
                   else BEHIND if st["behind"] else UP_TO_DATE)
    st["summary"] = summary(st)
    return st


# ------------------------------------------------------------ pull, push

_OVERWRITE = re.compile(r"would be overwritten by (?:merge|checkout)|untracked working tree files would be", re.I)


def _listed_files(text):
    """The files git lists, one per tab-indented line, under « would be
    overwritten »."""
    files, on = [], False
    for line in (text or "").splitlines():
        if _OVERWRITE.search(line):
            on = True
            continue
        if on and line.startswith(("\t", "    ")) and line.strip():
            files.append(line.strip())
        elif on and line.strip():
            on = False
    return files


def pull_ff(folder):
    """`git pull --ff-only`: {"ok", "files", "message"} — `files`, those
    git refused to overwrite."""
    r = git(folder, "pull", "-q", "--ff-only", "--no-rebase", timeout=PULL_TIMEOUT)
    if r.ok:
        return {"ok": True, "files": [], "message": ""}
    files = _listed_files(r.err + "\n" + r.out)
    if files:
        return {"ok": False, "files": files,
                "message": ("récupérer les commits de GitHub écraserait des fichiers non commités ici : "
                            + ", ".join(files) + " — les commiter (ou les retirer) d'abord")}
    return {"ok": False, "files": [], "message": explain(r.text), "credentials": credentials(r.text)}


def push(folder):
    """`git push` — a branch with no upstream yet is pushed to its remote
    and set to track it. {"ok", "rejected", "credentials", "message"}."""
    up = git(folder, "rev-parse", "-q", "--verify", "--symbolic-full-name", "@{upstream}")
    if up.ok and up.out.strip():
        r = git(folder, "push", "-q", timeout=PUSH_TIMEOUT)
    else:
        remotes = git(folder, "remote").out.split()
        if not remotes:
            return {"ok": False, "rejected": False, "credentials": False,
                    "message": "ce dépôt n'a pas de dépôt distant : rien où envoyer"}
        remote = "origin" if "origin" in remotes else remotes[0]
        r = git(folder, "push", "-q", "-u", remote, "HEAD", timeout=PUSH_TIMEOUT)
    if r.ok:
        return {"ok": True, "rejected": False, "credentials": False, "message": ""}
    rejected = bool(_REJECTED.search(r.text))
    return {"ok": False, "rejected": rejected, "credentials": credentials(r.text),
            "message": ("GitHub a refusé le push : il a des commits que cet ordinateur n'a pas"
                        if rejected else explain(r.text))}


# ------------------------------------------------------------ « Réconcilier »

def _rebasing(folder):
    gd = git(folder, "rev-parse", "--git-dir").out.strip()
    gd = gd if os.path.isabs(gd) else os.path.join(folder, gd)
    return any(os.path.exists(os.path.join(gd, d)) for d in ("rebase-merge", "rebase-apply"))


def reconcile(folder):
    """« divergé »: `git pull --rebase=merges` — the local commits replayed
    on GitHub's, each `Merge /<command>` kept as a merge with its subject
    (1.12.1; a plain `--rebase` flattened them). A conflict: `git rebase
    --abort`, the clone back as it was, and which files conflict. Refused
    while uncommitted files would be touched. Then the push."""
    st = compute(folder)
    out = {"ok": False, "conflicts": [], "files": [], "pushed": False, "message": "", "before": st}
    if st["state"] != DIVERGED:
        out["message"] = f"rien à réconcilier : {summary(st).lower()}"
        return out
    d = dirty_paths(folder) or []
    tracked = sorted(p for code, p in d if code != "??")
    if tracked:
        out["files"] = tracked
        out["message"] = ("Réconcilier réécrit les fichiers suivis par git ; il refuse tant que ceux-ci ont des "
                          "modifications non commitées : " + ", ".join(tracked)
                          + " — les commiter d'abord (« Envoyer mes réponses » pour des réponses)")
        return out
    base = git(folder, "merge-base", "HEAD", st["upstream"]).out.strip()
    touched = set()
    for rng in (f"{base}..HEAD", f"{base}..{st['upstream']}"):
        touched |= set(git(folder, "diff", "--name-only", rng).out.split("\n"))
    untracked = sorted(p for code, p in d if code == "??" and p in touched)
    if untracked:
        out["files"] = untracked
        out["message"] = ("Réconcilier écraserait des fichiers non suivis ici : " + ", ".join(untracked)
                          + " — les déplacer ou les commiter d'abord")
        return out
    head = git(folder, "rev-parse", "HEAD").out.strip()
    r = git(folder, "pull", "-q", "--rebase=merges", "--no-autostash", timeout=PULL_TIMEOUT)
    if not r.ok:
        if _rebasing(folder):
            conflicts = sorted(x for x in git(folder, "diff", "--name-only", "--diff-filter=U").out.split("\n") if x)
            git(folder, "rebase", "--abort")
            back = git(folder, "rev-parse", "HEAD").out.strip() == head and not _rebasing(folder)
            out["conflicts"] = conflicts
            out["message"] = ("Les commits d'ici et ceux de GitHub touchent les mêmes lignes"
                              + (" : " + ", ".join(conflicts) if conflicts else "")
                              + ". Rien n'a changé : le dépôt est revenu tel qu'il était"
                              + ("" if back else " — à vérifier : HEAD n'est pas revenu à " + head[:7])
                              + ". Une session Claude Code ouverte sur l'application réglera ce conflit.")
            return out
        out["message"] = explain(r.text)
        return out
    p = push(folder)
    out.update(ok=True, pushed=p["ok"], push=p,
               message="Réconcilié : les commits d'ici sont rejoués après ceux de GitHub"
                       + (", et envoyés." if p["ok"] else f" — envoi : {p['message']}"))
    return out


# ------------------------------------------------------------ « Envoyer mes réponses »

def feature_path(feature):
    return f"docs/features/{feature}/"


def answers_pending(folder, feature):
    """How many paths of the feature folder git sees changed and not
    committed — what the next command's `git add docs/features/<name>/`
    would commit."""
    if not feature:
        return 0
    d = dirty_paths(folder, [feature_path(feature)])
    return len(d) if d is not None else 0


def commit_answers(folder, feature):
    """The commit the commands make before their worktree
    (cmd/1_lexique.md:128-135 and the others): the feature folder,
    `chore: answers`. None when nothing was left to commit."""
    path = feature_path(feature)
    a = git(folder, "add", "--", path)
    if not a.ok:
        raise SyncError(f"git add : {a.text}")
    if not dirty_paths(folder, [path]):
        return None
    c = git(folder, "commit", "-q", "-m", ANSWERS_MESSAGE, "--only", "--", path)
    if not c.ok:
        raise SyncError(f"git commit : {c.text}")
    return git(folder, "rev-parse", "--short", "HEAD").out.strip()


class SyncError(Exception):
    pass


# ------------------------------------------------------------ a second computer

def set_long_paths(folder):
    r = git(folder, "config", "--local", "core.longpaths", "true")
    if not r.ok:
        raise SyncError(f"core.longpaths non réglé : {r.text}")


def long_paths(folder):
    """`core.longpaths` in the repository's own config: True, False, or
    None when it is not set."""
    r = git(folder, "config", "--local", "--get", "core.longpaths")
    if not r.ok:
        return None
    return r.out.strip().lower() == "true"


def repo_name(url):
    u = (url or "").strip().rstrip("/\\")
    name = re.split(r"[/\\:]", u)[-1] if u else ""
    return name[:-4] if name.lower().endswith(".git") else name


def clone(url, dest):
    """`git clone`, `core.longpaths=true` written in the new repository's
    config. {"ok", "credentials", "message"}."""
    parent = os.path.dirname(os.path.abspath(dest))
    try:
        p = subprocess.run(["git", "-c", "core.longpaths=true", "clone", "-q", "--config", "core.longpaths=true",
                            "--", url, dest], capture_output=True, timeout=CLONE_TIMEOUT, env=env(),
                           stdin=subprocess.DEVNULL, cwd=parent)
    except subprocess.TimeoutExpired:
        return {"ok": False, "credentials": False, "message": f"git clone : pas de réponse en {CLONE_TIMEOUT} s"}
    except OSError as e:
        return {"ok": False, "credentials": False, "message": f"git clone : {e}"}
    if p.returncode:
        text = p.stderr.decode("utf-8", "replace").strip() or p.stdout.decode("utf-8", "replace").strip()
        return {"ok": False, "credentials": credentials(text), "message": explain(text)}
    return {"ok": True, "credentials": False, "message": ""}


# ------------------------------------------------------------ the book

class Book:
    """The last state of each clone, and one lock per clone: a fetch, a
    pull, a push never run at once in the same repository."""

    def __init__(self):
        self._states = {}
        self._locks = {}
        self._guard = threading.Lock()

    @staticmethod
    def key(folder):
        return os.path.normcase(os.path.abspath(folder))

    def lock(self, folder):
        with self._guard:
            return self._locks.setdefault(self.key(folder), threading.RLock())

    def peek(self, folder):
        return self._states.get(self.key(folder)) if folder else None

    def put(self, folder, st):
        self._states[self.key(folder)] = st
        return st

    def refresh(self, folder, fetch=True):
        with self.lock(folder):
            return self.put(folder, compute(folder, fetch))

    def get(self, folder):
        """The state known, else computed now."""
        st = self.peek(folder)
        if st is not None:
            return st
        with self.lock(folder):
            st = self.peek(folder)
            return st if st is not None else self.put(folder, compute(folder))


def before_launch(book, folder):
    """§2 — before a launch: « en retard » pulled (fast-forward only);
    « divergé » refused; « non envoyé » pushed first; « GitHub injoignable »
    let through with a notice. {"ok", "error", "notice", "files",
    "reconcile", "sync", "done": [what git did]}."""
    out = {"ok": True, "error": "", "notice": "", "files": [], "reconcile": False, "done": []}
    with book.lock(folder):
        st = book.put(folder, compute(folder))
        s = st["state"]
        if s == BEHIND:
            r = pull_ff(folder)
            if not r["ok"]:
                out.update(ok=False, files=r["files"], error=r["message"])
                st = book.put(folder, compute(folder, fetch=False))
            else:
                out["done"].append(f"git pull --ff-only — {st['behind']} commit(s) récupéré(s)")
                out["notice"] = (f"{st['behind']} commit{'s' if st['behind'] > 1 else ''} récupéré"
                                 f"{'s' if st['behind'] > 1 else ''} de GitHub avant de lancer.")
                st = book.put(folder, compute(folder, fetch=False))
        elif s == DIVERGED:
            out.update(ok=False, reconcile=True,
                       error=summary(st) + " — rien ne se lance avant « Réconcilier »")
        elif s == OFFLINE:
            out["notice"] = "GitHub injoignable : lancé sans vérifier que cet ordinateur a tout"
            if st.get("credentials"):
                out["notice"] = "Lancé sans vérifier GitHub — " + CREDENTIALS_TEXT
        elif s == AHEAD:
            p = push(folder)
            if p["ok"]:
                out["done"].append(f"git push — {st['ahead']} commit(s) envoyé(s)")
                out["notice"] = (f"{st['ahead']} commit{'s' if st['ahead'] > 1 else ''} de cet ordinateur "
                                 "envoyé" + ("s" if st["ahead"] > 1 else "") + " à GitHub avant de lancer.")
                st = book.put(folder, compute(folder, fetch=False))
            elif p["rejected"]:
                st = book.put(folder, compute(folder))
                if st["state"] == DIVERGED:
                    out.update(ok=False, reconcile=True,
                               error="GitHub a refusé le push : " + summary(st).lower()
                                     + " — rien ne se lance avant « Réconcilier »")
                else:
                    out.update(ok=False, error=f"{p['message']} — {summary(st).lower()}")
            else:
                out["notice"] = f"Lancé sans envoyer : {p['message']}"
        out["sync"] = st
    return out
