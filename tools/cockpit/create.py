"""« Nouvelle application » — TECHNICAL_V1 §22 (1.7).

A brand-new application, from an empty folder to /1_lexique, with no Claude
call: every step is deterministic, and each is shown ✓ or ✗.

1. the folder and its git repository (`git init -b master`), and a
   `.gitignore` with the worktrees and the local settings;
2. the remote, when a URL was given — refused when it already holds commits
   that are not this creation's own: never forced;
3. the chain, with chain.py's install — the repository's first commit;
4. `.claude/scripts/socle.py`, the chain's own script, which the install
   just brought;
5. the idea file, copied unchanged to `docs/features/<feature>/idees.md`
   and committed `feat: <feature> — idées`;
6. the application added to the list, made active, opened on the feature.

After 3, 4 and 5, a push when there is a remote: the first one sets the
branch's upstream. A step that fails stops the creation and says why; «
Reprendre » goes on from that step, and every step checks what is already
there and does not redo it. The folder is never deleted.

The creation is kept in config.json while it is not finished, so that «
Reprendre » survives the server's restart — and only a folder this cockpit
started creating can be resumed: an existing application is never touched.
"""
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime

import chain as chain_mod
import sync

GIT_TIMEOUT = 60
REMOTE_TIMEOUT = 90
SOCLE = ".claude/scripts/socle.py"
SOCLE_TIMEOUT = 120
GITIGNORE = (".claude/worktrees/", ".claude/settings.local.json")
IDEA_EXT = (".md", ".txt")
IDEA_MAX = 2_000_000
FEATURE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FOLDER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
BUGFIX_RE = re.compile(r"^bugfix-\d+$")
REMOTE_RE = re.compile(r"^(https?://|ssh://|git@|file://)\S+$")
WINDOWS_RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}

STEPS = (
    ("dossier", "Le dossier et son dépôt git"),
    ("distant", "Le dépôt distant"),
    ("chaine", "La chaîne — le premier commit"),
    ("socle", "Le socle — socle.py"),
    ("idees", "Le fichier d'idées"),
    ("liste", "L'application dans la liste"),
)
TODO, GOING, OK, FAILED, NONE = "à faire", "en cours", "fait", "échec", "sans objet"


class StepError(Exception):
    """A step that cannot go on: said in French, the creation stops there."""


def default_parent():
    for p in (r"C:\Dev", os.path.expanduser("~")):
        if os.path.isdir(p):
            return p
    return ""


def slug(text):
    """Lower case, hyphens: « Mon Appli ! » → « mon-appli »."""
    t = unicodedata.normalize("NFKD", text or "")
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def _key(path):
    return os.path.normcase(os.path.abspath(path))


# ------------------------------------------------------------- the form

def read_idea(path):
    """(bytes, text, error): the idea file, read as the form shows it."""
    if not path:
        return None, None, "aucun fichier choisi"
    if not os.path.isfile(path):
        return None, None, "fichier introuvable"
    if os.path.splitext(path)[1].lower() not in IDEA_EXT:
        return None, None, "un fichier .md ou .txt"
    try:
        with open(path, "rb") as f:
            raw = f.read(IDEA_MAX + 1)
    except OSError as e:
        return None, None, f"lecture impossible : {e.strerror or e}"
    if len(raw) > IDEA_MAX:
        return None, None, "plus de 2 Mo : ce n'est pas un fichier d'idées"
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None, None, "pas de l'UTF-8"
    if not text.strip():
        return None, None, "le fichier est vide"
    return raw, text, None


def check(form, listed=(), resumable=(), chain_root=chain_mod.CHAIN_ROOT):
    """The form as the Product Owner filled it: its values, normalised, and
    what refuses it, field by field. `listed` are the folders of the list,
    `resumable` those of the creations this cockpit has not finished."""
    g = lambda k: (form.get(k) or "").strip().strip('"').strip()
    name, parent, folder = g("name"), g("parent"), g("folder")
    idea, feature, remote = g("idea"), g("feature"), g("remote")
    errors, v = {}, {}
    if not name:
        errors["name"] = "le nom de l'application"
    elif len(name) > 60:
        errors["name"] = "60 caractères au plus"
    v["name"] = name
    folder = folder or slug(name)
    v["folder"] = folder
    if not parent:
        errors["parent"] = "le dossier où la créer"
    elif not os.path.isdir(parent):
        errors["parent"] = "ce dossier n'existe pas"
    if not folder:
        errors["folder"] = "le nom du dossier"
    elif not FOLDER_RE.match(folder) or folder.lower().split(".")[0] in WINDOWS_RESERVED:
        errors["folder"] = "lettres, chiffres, tirets, points ou soulignés ; ni espace ni accent"
    path = os.path.normpath(os.path.join(parent, folder)) if parent and folder else ""
    v["path"] = path
    v["resume"] = False
    if path and "parent" not in errors and "folder" not in errors:
        k = _key(path)
        if k in {_key(x) for x in listed}:
            errors["folder"] = "une application de la liste a déjà ce dossier"
        elif k == _key(chain_root) or k.startswith(_key(chain_root) + os.sep):
            errors["folder"] = "dans le dépôt de la chaîne : une application a son propre dossier"
        elif k in {_key(x) for x in resumable}:
            v["resume"] = True
        elif os.path.exists(path) and not os.path.isdir(path):
            errors["folder"] = "un fichier porte déjà ce nom"
        elif os.path.isdir(path) and os.listdir(path):
            errors["folder"] = "ce dossier existe et n'est pas vide : la création demande un dossier neuf ou vide"
    raw, text, err = read_idea(idea)
    v["idea"] = idea
    if err:
        errors["idea"] = err
    v["idea_text"] = text
    v["feature"] = feature
    if not feature:
        errors["feature"] = "le nom de la première fonctionnalité"
    elif not FEATURE_RE.match(feature):
        errors["feature"] = "minuscules, chiffres et tirets seulement — par exemple « " + (slug(feature) or "premiere-app") + " »"
    elif BUGFIX_RE.match(feature):
        errors["feature"] = "bugfix-NN est le nom d'une correction"
    v["feature_slug"] = slug(feature)
    v["remote"] = remote
    if remote and not (REMOTE_RE.match(remote) or os.path.isdir(remote)):
        errors["remote"] = "une adresse https://github.com/… ou git@github.com:…"
    return {"values": v, "errors": errors, "ok": not errors}


def summary(v):
    """What « Créer » will make, one line each."""
    out = [f"le dossier {v['path']}, un dépôt git sur la branche master, et son .gitignore",
           f"le dépôt distant {v['remote']} — vide, rien n'y est forcé" if v["remote"]
           else "aucun dépôt distant : rien n'est poussé",
           "la chaîne, installée depuis le dépôt de la chaîne — le premier commit",
           "le socle : docs/PRODUIT_GLOBAL.md, docs/features/, docs/CURRENT_TECHNICAL_STATE.md — "
           "« chore: scaffolding for the chain »",
           f"docs/features/{v['feature']}/idees.md, copie de {v['idea']} — « feat: {v['feature']} — idées »",
           f"« {v['name']} » dans la liste des applications, active, ouverte sur {v['feature']}"]
    return out


# ---------------------------------------------------------------- git

def _git(repo, *args, timeout=GIT_TIMEOUT, ok=(0,)):
    env = sync.env()
    try:
        p = subprocess.run(["git", "-C", repo, "-c", "core.quotepath=off", *args], capture_output=True,
                           timeout=timeout, env=env, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        raise StepError(f"git {args[0]} ne répond pas après {timeout} s")
    except OSError as e:
        raise StepError(f"git introuvable ({e})")
    if p.returncode not in ok:
        msg = (p.stderr or p.stdout).decode("utf-8", "replace").strip()
        raise StepError(f"git {args[0]} : {msg}")
    return p


def _out(p):
    return p.stdout.decode("utf-8", "replace").strip()


def contents(path):
    """What the folder holds, at its top: shown when a step fails — the
    cockpit never deletes it."""
    try:
        names = sorted(os.listdir(path))
    except OSError:
        return []
    return [n + ("/" if os.path.isdir(os.path.join(path, n)) else "") for n in names]


def python_exe():
    """The console Python next to the server's: under pythonw, a script's
    output is read all the same."""
    exe = sys.executable
    if os.path.basename(exe).lower() == "pythonw.exe":
        alt = os.path.join(os.path.dirname(exe), "python.exe")
        if os.path.isfile(alt):
            return alt
    return exe


# ---------------------------------------------------------- the creation

class Creation:
    """One creation, its values and its steps. `save(record)` keeps it in
    config.json at every change; `finish(values)` adds the application to the
    list and returns what the scan proposes there."""

    def __init__(self, values, save, finish, chain_root=chain_mod.CHAIN_ROOT, record=None):
        self.v = values
        self.save = save
        self.finish = finish
        self.chain_root = chain_root
        r = record or {}
        self.steps = r.get("steps") or [{"id": i, "label": t, "status": TODO, "detail": ""} for i, t in STEPS]
        self.status = r.get("status") or TODO
        self.started_at = r.get("started_at") or datetime.now().isoformat(timespec="seconds")
        self.error = r.get("error")
        self.contents = r.get("contents") or []

    @property
    def path(self):
        return self.v["path"]

    def record(self):
        v = {k: x for k, x in self.v.items() if k != "idea_text"}
        return {"values": v, "steps": [dict(s) for s in self.steps], "status": self.status,
                "started_at": self.started_at, "error": self.error,
                "contents": list(self.contents), "failed_at": self.failed_at()}

    def failed_at(self):
        return next((s["id"] for s in self.steps if s["status"] == FAILED), None)

    def first_undone(self):
        return next((i for i, s in enumerate(self.steps) if s["status"] not in (OK, NONE)), len(self.steps))

    def _set(self, i, status, detail=None):
        self.steps[i]["status"] = status
        if detail is not None:
            self.steps[i]["detail"] = detail
        self.save(self.record())

    def run(self):
        """From the first step not done to the last, or to the first that
        fails. Returns the record."""
        self.status, self.error, self.contents = GOING, None, []
        for i in range(self.first_undone(), len(self.steps)):
            self._set(i, GOING, "")
            try:
                status, detail = getattr(self, "step_" + self.steps[i]["id"])()
            except StepError as e:
                self.status, self.error, self.contents = FAILED, str(e), contents(self.path)
                self._set(i, FAILED, str(e))
                return self.record()
            except Exception as e:      # said, never hidden
                self.status, self.error, self.contents = FAILED, f"{type(e).__name__} : {e}", contents(self.path)
                self._set(i, FAILED, self.error)
                return self.record()
            self._set(i, status, detail)
        self.status = OK
        self.save(self.record())
        return self.record()

    # ----------------------------------------------------------- helpers

    def git(self, *args, **kw):
        return _git(self.path, *args, **kw)

    def tracked_clean(self, rel):
        """Committed, and the working tree as committed."""
        if self.git("ls-files", "--error-unmatch", "--", rel, ok=(0, 1)).returncode:
            return False
        return _out(self.git("status", "--porcelain", "--", rel)) == ""

    def has_commit(self):
        return self.git("rev-parse", "-q", "--verify", "HEAD", ok=(0, 1)).returncode == 0

    def push(self):
        """After a commit: pushed when there is a remote. Its failure stops
        the creation; the commit stays, and « Reprendre » pushes."""
        if not self.v["remote"]:
            return "pas de dépôt distant : rien n'est poussé"
        head = _out(self.git("rev-parse", "HEAD"))
        up = self.git("rev-parse", "-q", "--verify", "refs/remotes/origin/master", ok=(0, 1))
        if up.returncode == 0 and _out(up) == head:
            return "déjà poussé"
        try:
            chain_mod.push_branch(self.path)
        except chain_mod.InstallError as e:
            raise StepError(f"le commit est fait, le push a échoué — {e}")
        return "poussé"

    # ------------------------------------------------------------- steps

    def step_dossier(self):
        p, done = self.path, []
        if not os.path.isdir(p):
            if not os.path.isdir(os.path.dirname(p)):
                raise StepError(f"le dossier parent {os.path.dirname(p)} n'existe pas")
            os.mkdir(p)
            done.append("dossier créé")
        if not os.path.exists(os.path.join(p, ".git")):
            if os.listdir(p):
                raise StepError("le dossier n'est pas vide et n'est pas un dépôt git : rien n'y est écrit")
            self.git("init", "-q", "-b", "master")
            done.append("dépôt git créé, branche master")
        else:
            top = os.path.normpath(_out(self.git("rev-parse", "--show-toplevel")))
            if _key(top) != _key(p):
                raise StepError(f"le dossier est dans le dépôt {top} sans en être la racine")
        # Who commits, asked before the first commit — three steps need it.
        try:
            self.git("var", "GIT_COMMITTER_IDENT")
        except StepError:
            raise StepError("git ne sait pas qui commite : git config --global user.name « Votre nom » "
                            "et git config --global user.email « vous@exemple.fr », puis « Reprendre »")
        gi = os.path.join(p, ".gitignore")
        old = b""
        if os.path.exists(gi):
            with open(gi, "rb") as f:
                old = f.read()
        have = {l.strip() for l in old.decode("utf-8", "replace").splitlines()}
        add = [l for l in GITIGNORE if l not in have]
        if add:
            sep = b"" if not old or old.endswith(b"\n") else b"\n"
            with open(gi, "ab") as f:
                f.write(sep + "".join(l + "\n" for l in add).encode())
            done.append(".gitignore écrit")
        return OK, " ; ".join(done) or "déjà là"

    def step_distant(self):
        url = self.v["remote"]
        if not url:
            return NONE, "aucun : rien n'est poussé — les commandes de la chaîne diront leurs push en échec jusqu'à ce qu'un dépôt distant soit ajouté"
        remotes = _out(self.git("remote")).split()
        if "origin" in remotes:
            cur = _out(self.git("remote", "get-url", "origin"))
            if cur != url:
                raise StepError(f"origin pointe déjà vers {cur}, pas vers {url}")
        heads = [l.split()[0] for l in _out(self.git("ls-remote", url, timeout=REMOTE_TIMEOUT)).splitlines() if l.strip()]
        # A remote holding commits is refused — unless they are this
        # creation's own, pushed before a later step failed.
        foreign = [h for h in heads if not (self.has_commit()
                   and self.git("merge-base", "--is-ancestor", h, "HEAD", ok=(0, 1, 128)).returncode == 0)]
        if foreign:
            raise StepError("le dépôt distant contient déjà des commits : rien n'est forcé. "
                            "Donnez un dépôt vide — créé sur GitHub sans README, sans .gitignore, sans licence")
        if "origin" not in remotes:
            self.git("remote", "add", "origin", url)
            return OK, f"origin → {url}, vide"
        return OK, f"origin → {url}" + (", déjà poussé" if heads else ", vide")

    def step_chaine(self):
        if self.has_commit() and self.tracked_clean(chain_mod.VERSION_FILE):
            v = chain_mod.read_version(self.path)
            detail = f"déjà installée — {v['commit'][:7]}"
        else:
            try:
                res = chain_mod.install(self.path, self.chain_root, confirm=False, push=False)
            except chain_mod.NeedsConfirm as e:
                raise StepError("des fichiers de la chaîne sont déjà là et diffèrent : " + ", ".join(e.files))
            except chain_mod.InstallError as e:
                raise StepError(str(e))
            if not res["app_commit"]:
                raise StepError("l'installation n'a rien commité")
            detail = (f"{len(res['written'])} fichiers de la chaîne {res['commit']} du {res['date']} — "
                      f"commit {res['app_commit']} « {res['message']} »")
        return OK, detail + " — " + self.push()

    def _socle(self, *args):
        script = os.path.join(self.path, *SOCLE.split("/"))
        if not os.path.isfile(script):
            raise StepError(f"{SOCLE} manque : la chaîne installée ne le porte pas")
        try:
            p = subprocess.run([python_exe(), script, *args], cwd=self.path, capture_output=True,
                               timeout=SOCLE_TIMEOUT, stdin=subprocess.DEVNULL,
                               env=dict(os.environ, PYTHONIOENCODING="utf-8", GIT_TERMINAL_PROMPT="0"))
        except (OSError, subprocess.SubprocessError) as e:
            raise StepError(f"{SOCLE} n'a pas pu tourner ({e})")
        out = p.stdout.decode("utf-8", "replace")
        err = p.stderr.decode("utf-8", "replace").strip()
        if p.returncode:
            raise StepError(f"{SOCLE} : " + (err or out.strip() or f"code {p.returncode}"))
        return out

    def step_socle(self):
        rel = "docs/PRODUIT_GLOBAL.md"
        if self.tracked_clean(rel):
            detail = "déjà là"
        elif os.path.exists(os.path.join(self.path, *rel.split("/"))):
            raise StepError(f"{rel} existe sans être commité : socle.py refuserait — "
                            "le commiter, ou le retirer, puis « Reprendre »")
        else:
            self._socle()
            sha = _out(self.git("rev-parse", "--short", "HEAD"))
            detail = f"commit {sha} « chore: scaffolding for the chain »"
        return OK, detail + " — " + self.push()

    def step_idees(self):
        rel = f"docs/features/{self.v['feature']}/idees.md"
        target = os.path.join(self.path, *rel.split("/"))
        try:
            with open(self.v["idea"], "rb") as f:
                data = f.read()
        except OSError as e:
            raise StepError(f"le fichier d'idées {self.v['idea']} ne se lit plus : {e.strerror or e}")
        if os.path.exists(target):
            with open(target, "rb") as f:
                if f.read() != data:
                    raise StepError(f"{rel} existe et diffère du fichier d'idées : rien n'est écrasé")
            if self.tracked_clean(rel):
                return OK, "déjà là — " + self.push()
        else:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:      # unchanged: its bytes as they are
                f.write(data)
        msg = f"feat: {self.v['feature']} — idées"
        self.git("add", "--", rel)
        self.git("commit", "-q", "-m", msg, "--only", "--", rel)
        sha = _out(self.git("rev-parse", "--short", "HEAD"))
        return OK, f"{rel}, {len(data)} octets — commit {sha} « {msg} » — " + self.push()

    def step_liste(self):
        return OK, self.finish(self.v)
