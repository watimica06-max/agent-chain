"""The cockpit's local server — TECHNICAL_V1 §3. Listens on 127.0.0.1 only.

    python server.py [--port 8765] [--ouvrir]
"""
import argparse
import asyncio
import base64
import json
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime

from aiohttp import web

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import apps as apps_mod  # noqa: E402
import blocking   # noqa: E402
import chain as chain_mod  # noqa: E402
import codelots   # noqa: E402
import context as context_mod  # noqa: E402
import create as create_mod  # noqa: E402
import decide as decide_mod  # noqa: E402
import deploy as deploy_mod  # noqa: E402
import deploy_profile  # noqa: E402
import diagnostic  # noqa: E402
import donnees as donnees_mod  # noqa: E402
import gitref     # noqa: E402
import questions  # noqa: E402
import runner as runner_mod  # noqa: E402
import scan as scan_mod  # noqa: E402
import startup  # noqa: E402
import stats as stats_mod  # noqa: E402
import statsview  # noqa: E402
import sync as sync_mod  # noqa: E402
import textfile   # noqa: E402
import writer     # noqa: E402
from state import State  # noqa: E402

HOST = "127.0.0.1"
STATE_KEY = web.AppKey("state", State)
DEPLOY_KEY = web.AppKey("deploy", deploy_mod.Deployer)
DEFAULT_PORT = 8765
VERSION = "1.12"
# « Arrêter le cockpit » with a run going: how long the run is given to end
# once it was told to stop now, before the server goes all the same.
STOP_GRACE = 30.0
# The chain's repository, which the cockpit installs into an application
# (§20), and whether an install pushes; the tests put a scratch one here.
CHAIN_ROOT = chain_mod.CHAIN_ROOT
CHAIN_PUSH = True
# Whether saving a deploy profile pushes (1.8); the tests put False here.
PROFILE_PUSH = True
# Whether « Données » pushes its commit (1.10); the tests put False here.
DONNEES_PUSH = True
# 1.12 — when the cockpit starts: agent-chain's own clone fetched, and pulled
# when « en retard »; every application of the list fetched. The tests put
# False here: none of them touches the real agent-chain.
SYNC_CHAIN_AT_START = True
SYNC_APPS_AT_START = True
CHAIN_RESTART = ("Nouvelle version du cockpit et de la chaîne récupérée — redémarre le cockpit pour "
                 "l'utiliser.")
# A joined file comes in the request, base64 in JSON: what one may weigh.
MAX_REQUEST = 256 * 1024 * 1024
# What opens the browser; the tests put a fake here.
OPEN_BROWSER = webbrowser.open
GROUPS = ["Amont", "Aval", "Correction", "Fusion", "Outils"]
# `.claude/CLAUDE.md`'s table: upstream cycle, downstream cycle, bug-fix entry,
# merge, and what is run by hand outside the chain. A command not listed is a tool.
COMMAND_GROUP = {
    **dict.fromkeys(["1_lexique", "2_structure", "3_decoupe", "3a_genre", "3b_nature",
                     "4_grille", "5_reclasse", "6_convertit"], "Amont"),
    **dict.fromkeys(["7_lots", "8_code"], "Aval"),
    "diagnostique": "Correction",
    **dict.fromkeys(["fusion", "fusion_compare", "fusion_applique"], "Fusion"),
}
BUGFIX = re.compile(r"^bugfix-\d+$")
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.S)


# ------------------------------------------------------------- folders

def features_dir(app):
    return os.path.join(app, "docs", "features")


def check_app_folder(app):
    """Why the application cannot be opened on a feature — or None. 1.6: a
    git repository where the chain is not installed yet is in the list all
    the same, « chaîne absente »; opening it on a feature needs
    `docs/features/` alone."""
    if not app or not os.path.isdir(app):
        return "dossier introuvable"
    if not os.path.isdir(features_dir(app)):
        return "pas de dossier docs/features/ : aucune feature à ouvrir"
    return None


def all_folders(app):
    """Every folder of `docs/features/`, ignored ones included."""
    base = features_dir(app)
    return [name for name in sorted(os.listdir(base))
            if os.path.isdir(os.path.join(base, name)) and not name.startswith(".")]


def working_folders(app, ignored=()):
    """The features of `docs/features/`, less the ignored ones (1.5.1): an
    ignored folder and its `bugfix-NN/` are never shown. Since 1.3 a
    feature's `bugfix-NN/` are not picked here: they live under « Correction »."""
    return [name for name in all_folders(app) if name not in ignored]


def bugfixes(app, feature):
    """The feature's `bugfix-NN/`, oldest first."""
    p = work_dir(app, feature)
    try:
        names = os.listdir(p)
    except OSError:
        return []
    return sorted((n for n in names if BUGFIX.match(n) and os.path.isdir(os.path.join(p, n))),
                  key=_natural)


def _natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def work_dir(app, work):
    return os.path.join(features_dir(app), *work.split("/"))


def feature_of(work):
    # The commands take the feature folder's name; they find the highest
    # bugfix-NN/ themselves (cmd/8_code.md:16-19).
    return work.split("/")[0]


def list_commands(app):
    cdir = os.path.join(app, ".claude", "commands")
    out = []
    if not os.path.isdir(cdir):
        return out
    for name in os.listdir(cdir):
        if not name.endswith(".md"):
            continue
        path = os.path.join(cdir, name)
        desc, hint = "", ""
        try:
            with open(path, encoding="utf-8") as f:
                head = f.read(2000)
            m = FRONTMATTER.match(head)
            if m:
                for line in m.group(1).splitlines():
                    if line.startswith("description:"):
                        desc = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("argument-hint:"):
                        hint = line.split(":", 1)[1].strip().strip('"')
        except OSError:
            pass
        out.append({"name": name[:-3], "description": desc, "argument_hint": hint,
                    "group": COMMAND_GROUP.get(name[:-3], "Outils")})
    out.sort(key=lambda c: (0 if c["name"][0].isdigit() else 1, _natural(c["name"])))
    return out


# --------------------------------------------------------------- forms

def _prefix(entries, prefix):
    """Entries read in a `bugfix-NN/` carry their path from the feature
    folder, so that one form holds both without two ids alike."""
    if prefix:
        for e in entries:
            old = e.rel
            e.rel = prefix + old
            if hasattr(e, "id"):
                e.id = e.id.replace(old, e.rel, 1)
    return entries


def form_folders(app, feature):
    """Where the form reads: the feature folder, and the highest
    `bugfix-NN/` — the one the commands act on (cmd/7_lots.md:19-21). The
    redécoupage is the last folder's alone, the working folder."""
    bf = bugfixes(app, feature)
    out = [("", work_dir(app, feature))]
    if bf:
        out.append((bf[-1] + "/", os.path.join(work_dir(app, feature), bf[-1])))
    return out


def collect_forms(app, work, rn):
    feature = feature_of(work)
    qs, qerr, bs, notices, wts_used = [], [], [], [], []
    redec = None
    folders = form_folders(app, feature)
    live = rn.live_worktrees(app)
    for prefix, wd in folders:
        q, qe = questions.scan(wd)
        qs += _prefix(q, prefix)
        qerr += _prefix(qe, prefix)
        wts = []
        for wt in live:
            wt_work = os.path.join(wt, "docs", "features", feature, *([prefix.rstrip("/")] if prefix else []))
            if os.path.isdir(wt_work):
                wts.append((wt, wt_work))
        b, n, r = blocking.scan(wd, wts)
        bs += _prefix(b, prefix)
        notices += _prefix(n, prefix)
        wts_used += [wt for wt, _ in wts]
        if (prefix, wd) == folders[-1] and r:
            redec = _prefix([r], prefix)[0]
    return qs, qerr, bs, notices, redec, sorted(set(wts_used))


def _owner(rel, kind, path):
    head, _, inner = rel.partition("/")
    inner = inner if scan_mod.BUGFIX.match(head) else rel
    try:
        lines = textfile.load(path).lines if kind == "blocking" else []
    except textfile.UnreadableFile:
        lines = []
    return scan_mod.owner(inner, kind, lines)[0]


def _chain(rel):
    head = rel.split("/")[0]
    return head if scan_mod.BUGFIX.match(head) else "main"


def forms_payload(app, work, rn):
    qs, qerr, bs, notices, redec, wts = collect_forms(app, work, rn)
    out_q, out_b = [], []
    for e in qs:
        d = e.to_dict()
        d.update(step=_owner(e.rel, e.kind, e.file), chain=_chain(e.rel))
        t = context_mod.target(e, work_dir(app, feature_of(work)))
        d["ctx"] = {k: t.get(k) for k in ("status", "rule", "reason", "kind")}
        d["folder"] = folder_of_question(app, e)
        out_q.append(d)
    for e in bs:
        d = e.to_dict()
        d.update(step=_owner(e.rel, "blocking", e.file), chain=_chain(e.rel))
        out_b.append(d)
    red = None
    if redec:
        red = redec.to_dict()
        red.update(step="7_lots", chain=_chain(redec.rel))
    return {
        "questions": out_q,
        "blocking": out_b,
        "redecoupage": red,
        "errors": [e.to_dict() for e in qerr] + [n.to_dict() for n in notices],
        "worktrees": wts,
    }


def folder_marker(e):
    """The value of a question's `Folder:` line, or None (§5)."""
    return next((c.split(":", 1)[1].strip() for c in e.context if c.startswith("Folder:")), None)


def folder_of_question(app, e):
    """What « Joindre un fichier » needs on a question with the marker: the
    folder, or why it is refused. None on a question whose answer is text."""
    marker = folder_marker(e)
    if marker is None:
        return None
    try:
        return {"folder": donnees_mod.folder_of_marker(app, marker) + "/", "error": None}
    except donnees_mod.DataError as err:
        return {"folder": None, "error": str(err)}


def question_context(app, work, rn, qid):
    """The document a question points to and its passages — read only
    (`context_rules.md`)."""
    qs, _, _, _, _, _ = collect_forms(app, work, rn)
    entry = next((q for q in qs if q.id == qid), None)
    if entry is None:
        return None
    return context_mod.resolve(entry, work_dir(app, feature_of(work)))


def save_items(app, work, rn, items):
    qs, _, bs, _, redec, _ = collect_forms(app, work, rn)
    by_id = {q.id: q for q in qs}
    by_id.update({b.id: b for b in bs})
    if redec:
        by_id[redec.id] = redec
    results = []
    for item in items:
        iid = item.get("id", "")
        entry = by_id.get(iid)
        choice = writer.Choice(kind=item.get("kind", "none"), option=item.get("option"),
                               text=item.get("text", "") or "")
        if choice.kind == "none":
            continue
        if entry is None:
            results.append(writer.Result(iid, "error", "n'attend plus de réponse — rechargez"))
            continue
        if item.get("fingerprint") != entry.fingerprint:
            results.append(writer.Result(iid, "error", "a changé depuis l'affichage — rechargez"))
            continue
        if isinstance(entry, questions.Question):
            results.append(writer.write_question(entry, choice))
        elif isinstance(entry, blocking.BlockingEntry):
            results.append(writer.write_blocking(entry, choice))
        else:
            results.append(writer.write_redecoupage(entry, choice, form_folders(app, feature_of(work))[-1][1]))
    return [r.to_dict() for r in results]


# ------------------------------------------------------------- the chain

def chain_state(app):
    """The chain's state in the application (§20); the tests put a stub here."""
    return chain_mod.state(app, CHAIN_ROOT)


# ------------------------------------------------------------- the scan

_conventions_cache = {}


def conventions_commit(app):
    """The commit that last changed `docs/TECHNICAL_CONVENTIONS.md` — the
    test /7_lots runs on the Bâtisseur's report (cmd/7_lots.md:87-92), which
    « Bâtir » reads too. The scan runs no git command: it is read here, once
    per `HEAD` — a commit is what changes it. None when git cannot say: not
    a repository, or no commit holds the file."""
    head = gitref.head(app)
    if not head:
        return None
    key = (os.path.normcase(os.path.abspath(app)), head)
    if key in _conventions_cache:
        return _conventions_cache[key]
    try:
        p = subprocess.run(["git", "-C", app, "log", "-1", "--format=%H", "--", "docs/TECHNICAL_CONVENTIONS.md"],
                           capture_output=True, timeout=20, stdin=subprocess.DEVNULL,
                           env=sync_mod.env())
    except (OSError, subprocess.SubprocessError):
        return None
    out = p.stdout.decode("utf-8", "replace").strip() if p.returncode == 0 else ""
    _conventions_cache[key] = out or None
    return _conventions_cache[key]


def scan_of(app, feature, snap=None):
    """The scan of one feature, with the conventions' last commit."""
    return scan_mod.run_scan(app, feature, snap, conventions_commit(app))

def where(state: State, rn, app, feature, reason=None):
    """The scan and §2's decision. `reason` names a scan trigger — the
    button, the opening, a save of answers: it ends the moment a run's
    `Next:` is trusted without a check. A dropped `Next:` is written to
    the run's log, once."""
    run = rn.current(app)
    snap = run.snapshot() if run and run.id else None
    sc = scan_of(app, feature, snap)
    if reason:
        state.clear_fresh(app, feature)
    stored = state.relay(app, feature)
    dec = decide_mod.decide(sc, feature, run=snap, stored=stored,
                            fresh=state.is_fresh(app, feature), head_now=gitref.head(app))
    if dec.get("dropped"):
        log_dropped(state, rn, stored, dec, reason)
    return sc, dec


def log_dropped(state, rn, stored, dec, reason):
    d = dec["dropped"]
    if not state.first_log((stored.get("at"), stored.get("command"), d["rule"])):
        return
    path = stored.get("log_path") or os.path.join(rn.log_dir, "next-ecarte.jsonl")
    line = {"at": datetime.now().isoformat(timespec="milliseconds"), "type": "NextDropped",
            "message": {**d, "trigger": reason or "rafraîchissement"}}
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    except OSError:
        pass
    d["logged_to"] = path


def new_bugfix(app, feature):
    """The next `bugfix-NN/` and its empty `bug-list.md` — the only two
    things this writes (§3.3)."""
    bf = bugfixes(app, feature)
    n = int(bf[-1].split("-")[1]) + 1 if bf else 1
    name = f"bugfix-{n:02d}"
    path = os.path.join(work_dir(app, feature), name)
    os.makedirs(path)
    with open(os.path.join(path, "bug-list.md"), "x", encoding="utf-8"):
        pass
    return name


def run_place(sc, run):
    if not run or not run.id:
        return None
    chain, step = decide_mod.chain_of(sc, run.command)
    return {"chain": chain, "step": step} if step else None


def recette(app, feature):
    """What to test by hand: `code/recette-ordonnee.md` of the working
    folder, when /9_controle wrote it (cmd/9_controle.md:362)."""
    bf = bugfixes(app, feature)
    base = os.path.join(work_dir(app, feature), *([bf[-1]] if bf else []))
    p = os.path.join(base, "code", "recette-ordonnee.md")
    if not os.path.isfile(p):
        return None
    try:
        lines = textfile.load(p).lines
    except textfile.UnreadableFile:
        return None
    rel = os.path.relpath(p, work_dir(app, feature)).replace(os.sep, "/")
    items = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
    return {"rel": rel, "count": len(items), "first": items[:3]}


# -------------------------------------------------------------- the app

def ask_directory(initial, title="Choisir le dossier de l'application"):
    """The native folder picker, run in a worker thread."""
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass
    try:
        path = filedialog.askdirectory(initialdir=initial or None, mustexist=True,
                                       title=title)
    finally:
        root.destroy()
    return path or ""


LOCAL_NAMES = {"127.0.0.1", "localhost"}
# What runs the diagnostic when make_app is given nothing; the tests put a
# fake here, so that no page test runs the real version commands.
DIAG_RUNNER = diagnostic.run_diagnostic


def _host_name(hostport):
    from urllib.parse import urlsplit
    try:
        return urlsplit("//" + (hostport or "")).hostname
    except ValueError:
        return None


def make_on_end(state: State):
    """What the server remembers of a run when it ends: the relay with its
    `Next:`, and one line of history."""
    def on_end(run):
        state.set_relay(run.repo, run.work, run.prompt, run.relay, run.next, run.outcome,
                        head=gitref.head(run.repo), log_path=run.log_path)
        state.add_history(run.repo, run.work, {
            "command": run.prompt, "outcome": run.outcome, "next": run.next,
            "log_path": run.log_path, "at": datetime.now().isoformat(timespec="seconds")})
    return on_end


def ask_idea_file(initial):
    """The native file picker, for the idea file (§22): .md and .txt."""
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass
    try:
        start = initial if initial and os.path.isdir(initial) else (os.path.dirname(initial) if initial else "")
        path = filedialog.askopenfilename(initialdir=start or None, title="Choisir le fichier d'idées",
                                          filetypes=[("Fichier d'idées", "*.md *.txt"), ("Markdown", "*.md"),
                                                     ("Texte", "*.txt")])
    finally:
        root.destroy()
    return os.path.normpath(path) if path else ""


def reveal(path, select=False):
    """The file explorer of this computer on `path` — its folder, the file
    selected, when `select`. Never runs the file."""
    if sys.platform == "win32":
        cmd = f'explorer /select,"{path}"' if select else f'explorer "{path}"'
    elif sys.platform == "darwin":
        cmd = ["open", "-R", path] if select else ["open", path]
    else:
        cmd = ["xdg-open", os.path.dirname(path) if select else path]
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# What opens a folder; the tests put a recorder here, so that no test opens
# a window on this computer.
REVEAL = reveal
LOG_EXTENSIONS = (".jsonl", ".log")


def ask_export_folder(initial):
    return ask_directory(initial, title="Où enregistrer les deux fichiers CSV ?")


def default_export_folder():
    for name in ("Downloads", "Documents"):
        p = os.path.join(os.path.expanduser("~"), name)
        if os.path.isdir(p):
            return p
    return os.path.expanduser("~")


def make_app(state: State, rn: runner_mod.Runner, picker=ask_directory,
             diag_runner=None, export_picker=ask_export_folder, on_quit=None, file_picker=ask_idea_file):
    store = rn.stats
    diag_runner = diag_runner or DIAG_RUNNER
    # The diagnostic run in the background (1.4.5): once, at the opening,
    # when no result is stored. 1.6: per application — each has its own
    # stack, its own result, and runs once on its own when it has none.
    diag = {"running": set(), "auto_done": set(), "tasks": {}}
    # « Tout mettre à jour » going (1.6): no launch, no other install meanwhile.
    bulk = {"going": False, "report": None}
    # « Nouvelle application » (1.7): the one going, and the last one this
    # server finished — config.json keeps those not finished.
    making = {"current": None, "last": None}
    # 1.12 — where each clone stands against GitHub (sync.py), and agent-chain's
    # own clone, fetched when the cockpit starts.
    book = sync_mod.Book()
    chain_sync = {"sync": None, "notice": "", "error": "", "checking": False}
    # The page as this server started: a pull of agent-chain changes the file
    # on disk, never the page this server serves.
    with open(os.path.join(HERE, "static", "index.html"), "rb") as f:
        page_bytes = f.read()
    # 1.6: a run stored with no application is given its own — main()'s
    # backfill did it already; this covers a store handed over as it is.
    if store:
        try:
            store.backfill_apps(app_resolver(state))
        except Exception as e:
            print(f"Consommation : application des anciens runs non retrouvée : {e}", flush=True)
    @web.middleware
    async def guard(request, handler):
        # Only this machine's browser, on this page: a foreign site cannot
        # reach the server through DNS rebinding or a cross-site request.
        if _host_name(request.host) not in LOCAL_NAMES:
            return web.json_response({"error": "hôte refusé"}, status=403)
        if request.method == "POST":
            origin = request.headers.get("Origin")
            if origin and _host_name(origin.split("://", 1)[-1]) not in LOCAL_NAMES:
                return web.json_response({"error": "origine refusée"}, status=403)
            if request.content_type != "application/json":
                return web.json_response({"error": "JSON attendu"}, status=415)
        return await handler(request)

    app = web.Application(middlewares=[guard], client_max_size=MAX_REQUEST)
    app[STATE_KEY] = state

    # « Déploiement » (1.8): its jobs and journals run in worker threads; what
    # they say reaches the page through the runs' stream, from the loop.
    loop_box = {"loop": None}

    def broadcast(kind, data):
        loop = loop_box["loop"]
        if loop is None:
            return
        ev = {"seq": next(rn._seq), "type": kind, "run": "", "app": data.get("app") or state.app_folder,
              "data": data, "at": runner_mod._now()}

        def put():
            for q in list(rn.watchers):
                q.put_nowait(ev)
        try:
            loop.call_soon_threadsafe(put)
        except RuntimeError:
            pass
    dep = deploy_mod.Deployer(state, rn.log_dir, emit=broadcast)
    app[DEPLOY_KEY] = dep

    # 1.12 §3: after every run, where the clone stands — a run whose final
    # push GitHub refused says so in its end panel.
    remember = rn.on_end

    def on_end(run):
        try:
            if remember:
                remember(run)
        finally:
            refresh_later(run.repo, run)
    rn.on_end = on_end

    def pair():
        a, w = state.app_folder, state.working_folder
        if not a or check_app_folder(a) or not w or not os.path.isdir(work_dir(a, w)) or state.is_ignored(w):
            return None, None
        return a, w

    def need_pair():
        a, w = pair()
        if not a:
            raise web.HTTPConflict(text=json.dumps({"error": "aucun dossier ouvert"}),
                                   content_type="application/json")
        return a, w

    async def body(request):
        try:
            data = await request.json()
        except ValueError:
            raise web.HTTPBadRequest(text=json.dumps({"error": "JSON illisible"}),
                                     content_type="application/json")
        return data if isinstance(data, dict) else {}

    async def index(request):
        return web.Response(body=page_bytes, content_type="text/html", charset="utf-8",
                            headers={"Cache-Control": "no-store"})

    # 1.13 — the web app manifest and its icons, so that a phone can put the
    # page on its home screen. Read from static/, nothing else served from there.
    ICONS = {"icon-192.png", "icon-512.png", "icon-maskable-512.png", "apple-touch-icon.png"}

    async def manifest(request):
        with open(os.path.join(HERE, "static", "manifest.webmanifest"), "rb") as f:
            return web.Response(body=f.read(), content_type="application/manifest+json", charset="utf-8")

    async def app_icon(request):
        name = request.match_info["name"]
        if name not in ICONS:
            raise web.HTTPNotFound()
        with open(os.path.join(HERE, "static", "icons", name), "rb") as f:
            return web.Response(body=f.read(), content_type="image/png", headers={"Cache-Control": "max-age=86400"})

    # ------------------------------------------------- GitHub (1.12, sync.py)
    def sync_said(folder, what, res):
        print(f"GitHub — {state.name_of(folder) or folder} : {what} — {res}", flush=True)

    told = {}

    def announce(folder, st, run_id=None):
        """The new state of a clone, to every page — only when it changed,
        or for a run's end panel."""
        k = sync_mod.Book.key(folder)
        seen = (st or {}).get("state"), (st or {}).get("ahead"), (st or {}).get("behind"), (st or {}).get("uncommitted")
        if run_id is None and (told.get(k) == seen or (k not in told and seen[0] is None)):
            return
        told[k] = seen
        broadcast("sync", {"app": folder, "sync": st, "run": run_id})

    def refresh_later(folder, run=None):
        """Fetched in the background — after a run, at an opening — then
        told to the page."""
        loop = loop_box["loop"]
        if loop is None or not folder or not os.path.isdir(folder):
            return

        async def go():
            try:
                st = await loop.run_in_executor(None, book.refresh, folder)
            except Exception as e:      # said, never raised into the loop
                print(f"GitHub — {folder} : état non calculé ({e})", flush=True)
                return
            if run is not None:
                run.sync = st
                if st.get("state") in (sync_mod.AHEAD, sync_mod.DIVERGED):
                    sync_said(folder, f"après {run.prompt}", st["summary"])
            announce(folder, st, run.id if run is not None else None)
        loop.create_task(go())

    async def synced_first(a):
        """§2 — before a launch, an « Enregistrer », an install: pulled when
        « en retard », pushed when « non envoyé », refused when « divergé ».
        (refusal response or None, the sync's result)."""
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, sync_mod.before_launch, book, a)
        for d in res["done"]:
            sync_said(a, "avant de lancer", d)
        announce(a, res["sync"])
        if not res["ok"]:
            sync_said(a, "lancement refusé", res["error"])
            return web.json_response({"error": res["error"], "sync_refused": res}, status=409), res
        return None, res

    async def resync(a):
        """After a git action of the cockpit: fetched again, told."""
        st = await asyncio.get_running_loop().run_in_executor(None, book.refresh, a)
        announce(a, st)
        return st

    def sync_target(data):
        """The clone an action names: an application of the list, or
        agent-chain's own (`chain`)."""
        if data.get("chain"):
            return CHAIN_ROOT
        return listed_folder(data) if data.get("folder") else state.app_folder

    def busy_payload():
        """The run going, whatever its application (1.6): the top bar says
        where it goes, and « Arrêter », its cards and its idle question act
        on it from any screen."""
        x = rn.going()
        if not x:
            return None
        return {"id": x.id, "app": x.repo, "app_name": state.name_of(x.repo), "prompt": x.prompt,
                "command": x.command, "work": x.work, "started_at": x.started_at, "status": x.status,
                "active": bool(state.app_folder) and runner_mod.repo_key(x.repo) == runner_mod.repo_key(state.app_folder),
                "permissions": [p.to_dict() for p in x.permissions.values()], "idle": x.idle,
                "agents": [x.agents.get(t, "agent") for t in x.active], "stop_next_lot": x.command == runner_mod.STOP_COMMAND}

    def apps_light():
        active = runner_mod.repo_key(state.app_folder) if state.app_folder else None
        return [{"name": x["name"], "folder": x["folder"], "last_feature": x["last_feature"],
                 "active": runner_mod.repo_key(x["folder"]) == active} for x in state.apps()]

    def diag_running(a):
        return bool(a) and runner_mod.repo_key(a) in diag["running"]

    def state_payload(reason=None):
        a, w = pair()
        out = {"app_folder": state.app_folder, "app_name": state.app_name, "working_folder": state.working_folder,
               "apps": apps_light(), "busy": busy_payload(), "bulk_going": bulk["going"],
               "recent": state.recent(), "load_error": state.load_error,
               "open": bool(a), "mode": state.mode, "diagnostic": state.diagnostic(),
               "diagnostic_running": diag_running(state.app_folder),
               "logs_dir": rn.log_dir, "groups": GROUPS,
               # The two usage windows, each with when it was measured (§13.3).
               "limits": _limits(store), "now": datetime.now().isoformat(timespec="seconds")}
        out["ignored"] = state.ignored
        out["creating"] = making["current"].path if making["current"] else None
        # 1.12: where the open application's clone stands against GitHub —
        # the last known state; agent-chain's own, with its notice.
        out["sync"] = book.peek(state.app_folder) if state.app_folder else None
        out["chain_sync"] = chain_sync
        out["chain_root"] = CHAIN_ROOT
        if state.app_folder and os.path.isdir(state.app_folder):
            # The chain installed in the application (§20) — 1.6: also where
            # it is not installed yet, and no feature can open.
            out["chain"] = chain_state(state.app_folder)
        if state.app_folder and not check_app_folder(state.app_folder):
            out["working_folders"] = working_folders(state.app_folder, state.ignored)
            out["all_folders"] = all_folders(state.app_folder)
        elif state.app_folder:
            out["open_error"] = check_app_folder(state.app_folder)
        if a:
            run = rn.current(a)
            feature = feature_of(w)
            sc, dec = where(state, rn, a, feature, reason)
            out.update({
                "feature": feature,
                "commands": list_commands(a),
                "last": state.relay(a, w),
                "run": run.snapshot() if run and run.id else None,
                "stop_file": os.path.exists(rn.stop_file(a, feature)),
                "history": _with_usage(store, state.history(a, w)),
                # Worktrees other than the main checkout, once nothing runs.
                "worktrees": [] if rn.is_running(a) else runner_mod.list_worktrees(a),
                "scan": sc,
                "decision": dec,
                # Where the run going, or the last one, sits in the flows.
                "run_place": run_place(sc, run),
                "bugfixes": bugfixes(a, feature),
                "recette": recette(a, feature),
                # 1.12 §5: what the next command's own commit would take.
                "answers_pending": sync_mod.answers_pending(a, feature),
            })
        return out

    async def get_state(request):
        return web.json_response(state_payload())

    async def check(request):
        """« Où on en est ? » — and the opening of the page: the stored
        `Next:` is checked against the files whatever just happened."""
        data = await body(request)
        a, _ = need_pair()
        if data.get("reason") == "ouverture":
            auto_diagnostic(a)
            if book.peek(a) is None:
                refresh_later(a)
        return web.json_response(state_payload(data.get("reason") or "bouton"))

    async def pick_folder(request):
        data = await body(request)
        loop = asyncio.get_running_loop()
        try:
            path = await loop.run_in_executor(None, picker, data.get("initial") or "")
        except Exception as e:
            return web.json_response({"error": f"le sélecteur n'a pas pu s'ouvrir ({e}) — "
                                               "collez le chemin dans le champ"}, status=500)
        return web.json_response({"path": path})

    async def app_folder(request):
        data = await body(request)
        path = os.path.normpath((data.get("path") or "").strip().strip('"'))
        err = check_app_folder(path)
        if err:
            return web.json_response({"error": err}, status=400)
        return web.json_response({"path": path, "working_folders": working_folders(path, state.ignored_for(path))})

    async def open_pair(request):
        """Opens a feature of an application. 1.6: the application is the
        listed one when its folder is; one not listed joins the list (the
        1.5 start screen's path — the page adds through /api/apps/add)."""
        data = await body(request)
        a = os.path.normpath((data.get("app") or "").strip().strip('"'))
        w = (data.get("work") or "").strip().strip("/")
        err = check_app_folder(a)
        if err:
            return web.json_response({"error": err}, status=400)
        if w not in working_folders(a, state.ignored_for(a)):
            return web.json_response({"error": "dossier ignoré : Paramètres → Dossiers ignorés" if state.is_ignored(w, a)
                                      else "dossier de travail inconnu"}, status=400)
        listed = state.app(a)
        state.open_pair(listed["folder"] if listed else a, w)
        return web.json_response({"ok": True})

    # ---------------------------------------------------- applications (1.6)
    def listed_folder(data):
        f = (data.get("folder") or "").strip().strip('"')
        x = state.app(f) if f else None
        if not x:
            raise web.HTTPNotFound(text=json.dumps({"error": "cette application n'est pas dans la liste"}),
                                   content_type="application/json")
        return x["folder"]

    def app_row(x):
        """One row of « Applications »: read-only, from the files and git."""
        folder = x["folder"]
        key = runner_mod.repo_key(folder)
        row = {"name": x["name"], "folder": folder, "exists": os.path.isdir(folder),
               "active": bool(state.app_folder) and key == runner_mod.repo_key(state.app_folder),
               "feature": None, "proposal": None, "questions": None, "blocking": None,
               "chain": None, "uncommitted": None, "last_run": None, "running": False, "errors": [],
               "sync": None, "answers_pending": 0}
        if not row["exists"]:
            row["errors"].append("dossier introuvable")
            return row
        try:
            row["chain"] = chain_state(folder)
        except Exception as e:
            row["errors"].append(f"état de la chaîne : {e}")
        row["uncommitted"] = apps_mod.uncommitted(folder)
        # 1.12: where it stands against GitHub — known, else fetched now.
        row["sync"] = book.get(folder)
        row["open_error"] = check_app_folder(folder)
        row["features"] = working_folders(folder, state.ignored_for(folder)) if not row["open_error"] else []
        run = rn.current(folder)
        snap = run.snapshot() if run and run.id else None
        row["running"] = bool(snap and snap["status"] != "ended")
        f = x.get("last_feature")
        if f and f in row["features"]:
            row["feature"] = f
            row["answers_pending"] = sync_mod.answers_pending(folder, f)
            try:
                sc = scan_of(folder, f, snap)
                prop = sc["proposal"]
                row["proposal"] = {"name": prop.get("name"), "state": prop.get("state"), "chain": prop.get("chain"),
                                   "french": decide_mod.proposal_next(sc, prop, f)["french"]}
                qs, _, bs, _, redec, _ = collect_forms(folder, f, rn)
                row["questions"], row["blocking"] = len(qs), len(bs) + (1 if redec else 0)
            except Exception as e:
                row["errors"].append(f"lecture de {f} : {e}")
        if row["running"]:
            row["last_run"] = {"command": snap["prompt"], "at": snap["started_at"], "outcome": "en cours",
                               "feature": (snap.get("work") or "").split("/")[0]}
        else:
            h = state.app_history(folder, 1)
            if h:
                row["last_run"] = {"command": h[0].get("command"), "at": h[0].get("at"),
                                   "outcome": h[0].get("outcome"), "feature": h[0].get("feature")}
        return row

    async def apps_get(request):
        loop = asyncio.get_running_loop()
        # 1.12: one application's fetch never waits for another's.
        rows = await asyncio.gather(*(loop.run_in_executor(None, app_row, x) for x in state.apps()))
        return web.json_response({"apps": list(rows), "busy": busy_payload(), "bulk_going": bulk["going"],
                                  "report": bulk["report"], "chain_sync": chain_sync})

    async def apps_add(request):
        """« Ajouter une application »: the folder picked or pasted joins the
        list — config.json alone. Refused, in French, when it is not the
        root of a git repository."""
        data = await body(request)
        path = (data.get("path") or "").strip().strip('"')
        path = os.path.normpath(path) if path else ""
        err = apps_mod.check_new_app(path)
        if err:
            return web.json_response({"error": err}, status=400)
        x, added = state.add_app(path, data.get("name"))
        # 1.12 §7: `core.longpaths=true` in its own git config — the one thing
        # « Ajouter » writes there.
        longpaths = None
        try:
            sync_mod.set_long_paths(x["folder"])
        except sync_mod.SyncError as e:
            longpaths = str(e)
        refresh_later(x["folder"])
        return web.json_response({"app": x, "added": added, "apps": apps_light(), "longpaths_error": longpaths})

    async def apps_rename(request):
        data = await body(request)
        folder = listed_folder(data)
        try:
            x = state.rename_app(folder, data.get("name"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"app": x, "apps": apps_light()})

    async def apps_remove(request):
        """« Retirer de la liste »: config.json alone, the folder never
        touched. The page asks first. Refused while a run goes there."""
        data = await body(request)
        folder = listed_folder(data)
        if rn.is_running(folder):
            return web.json_response({"error": "une commande tourne dans cette application : la retirer après"}, status=409)
        state.remove_app(folder)
        return web.json_response({"ok": True, "apps": apps_light()})

    async def apps_open(request):
        """« Ouvrir », and the top bar's list: the application becomes the
        active one, on its last feature — every screen works on it. Its
        diagnostic runs on its own when it has none."""
        data = await body(request)
        folder = listed_folder(data)
        state.activate(folder)
        a, _ = pair()
        if os.path.isdir(folder):
            auto_diagnostic(folder)
            # 1.12: an application that opens is fetched.
            refresh_later(folder)
        return web.json_response({"ok": True, "open": bool(a), "open_error": check_app_folder(folder)})

    # --------------------------------------------- Nouvelle application (1.7)
    def creation_args():
        return {"listed": [x["folder"] for x in state.apps()],
                "resumable": [r["values"]["path"] for r in state.creations()],
                "chain_root": CHAIN_ROOT}

    async def pick_file(request):
        data = await body(request)
        loop = asyncio.get_running_loop()
        try:
            path = await loop.run_in_executor(None, file_picker, data.get("initial") or "")
        except Exception as e:
            return web.json_response({"error": f"le sélecteur n'a pas pu s'ouvrir ({e}) — "
                                               "collez le chemin dans le champ"}, status=500)
        return web.json_response({"path": path})

    def checked(data):
        res = create_mod.check(data, **creation_args())
        v = res["values"]
        text = v.pop("idea_text")
        out = {"ok": res["ok"], "errors": res["errors"], "values": v,
               "idea_lines": text.splitlines() if text is not None else None,
               "summary": create_mod.summary(v) if res["ok"] else None,
               "default_parent": create_mod.default_parent()}
        return out, res

    async def create_check(request):
        """The form, checked as she types: each field's refusal, the idea
        file's lines for the read-only view, the summary when it holds."""
        data = await body(request)
        loop = asyncio.get_running_loop()
        out, _ = await loop.run_in_executor(None, checked, data)
        return web.json_response(out)

    def save_creation(record):
        # Finished: dropped from config.json — the list holds the application.
        if record["status"] == create_mod.OK:
            state.drop_creation(record["values"]["path"])
        else:
            state.set_creation(record)

    def finish_creation(v):
        """The last step: the application in the list, active, opened on
        its feature; what the scan proposes there."""
        state.add_app(v["path"], v["name"])
        folder = state.app(v["path"])["folder"]
        state.open_pair(folder, v["feature"])
        sc = scan_of(folder, v["feature"])
        nxt = decide_mod.proposal_next(sc, sc["proposal"], v["feature"])
        return (f"« {v['name']} » ajoutée à la liste, active, ouverte sur {v['feature']} — "
                f"le relevé du dossier propose : {nxt['french']}")

    def launch_creation(c):
        making["current"] = c
        loop = asyncio.get_running_loop()

        async def go():
            try:
                rec = await loop.run_in_executor(None, c.run)
            except Exception as e:      # said, never raised into the loop
                rec = c.record()
                rec.update(status=create_mod.FAILED, error=f"{type(e).__name__} : {e}")
            making["current"], making["last"] = None, rec
            print(f"Nouvelle application {c.path} : {rec['status']}"
                  + (f" — {rec['error']}" if rec.get("error") else ""), flush=True)
            if rec["status"] == create_mod.OK:
                auto_diagnostic(c.path)
        loop.create_task(go())

    def creation_busy():
        if making["current"]:
            return web.json_response({"error": f"une création est en cours : {making['current'].path}"}, status=409)
        return None

    async def create_start(request):
        """« Créer »: the form checked again, then the creation, in the
        background — the page follows it on GET /api/create."""
        data = await body(request)
        busy = creation_busy()
        if busy:
            return busy
        loop = asyncio.get_running_loop()
        out, res = await loop.run_in_executor(None, checked, data)
        if not res["ok"]:
            return web.json_response({"error": "le formulaire n'est pas complet", **out}, status=400)
        v = res["values"]
        if v["resume"]:
            return web.json_response({"error": "la création de ce dossier attend « Reprendre »"}, status=409)
        v.pop("idea_text", None)
        c = create_mod.Creation(v, save_creation, finish_creation, CHAIN_ROOT)
        state.set_creation(c.record())
        launch_creation(c)
        return web.json_response({"creation": c.record()})

    async def create_resume(request):
        """« Reprendre »: from the step that failed — each step checks what
        is already there. Only a creation this cockpit started."""
        data = await body(request)
        busy = creation_busy()
        if busy:
            return busy
        rec = state.creation((data.get("path") or "").strip())
        if not rec:
            return web.json_response({"error": "aucune création à reprendre pour ce dossier"}, status=404)
        if state.has_app(rec["values"]["path"]):
            state.drop_creation(rec["values"]["path"])
            return web.json_response({"error": "ce dossier est déjà une application de la liste"}, status=409)
        c = create_mod.Creation(rec["values"], save_creation, finish_creation, CHAIN_ROOT, record=rec)
        launch_creation(c)
        return web.json_response({"creation": c.record()})

    async def create_forget(request):
        """« Abandonner »: the creation leaves config.json; the folder stays
        as it is, never deleted."""
        data = await body(request)
        path = (data.get("path") or "").strip()
        if making["current"] and runner_mod.repo_key(making["current"].path) == runner_mod.repo_key(path):
            return web.json_response({"error": "cette création est en cours"}, status=409)
        state.drop_creation(path)
        return web.json_response({"ok": True, "contents": create_mod.contents(path)})

    def interrupted(r):
        """A creation the server stopped in the middle — closed, or crashed —
        is shown stopped at the step it was on, « Reprendre » offered."""
        if r.get("status") not in (create_mod.GOING, create_mod.TODO):
            return r
        r = {**r, "steps": [dict(x) for x in r["steps"]]}
        step = next((x for x in r["steps"] if x["status"] == create_mod.GOING), None) or             next((x for x in r["steps"] if x["status"] == create_mod.TODO), None)
        why = "interrompue : le cockpit s'est arrêté pendant cette étape — « Reprendre » regarde ce qui est déjà là"
        if step:
            step.update(status=create_mod.FAILED, detail=why)
        r.update(status=create_mod.FAILED, error=why, failed_at=step["id"] if step else None,
                 contents=create_mod.contents(r["values"]["path"]))
        return r

    async def create_get(request):
        cur = making["current"]
        going = cur.record() if cur else None
        pending = [interrupted(r) for r in state.creations()
                   if not (going and runner_mod.repo_key(r["values"]["path"]) == runner_mod.repo_key(going["values"]["path"]))]
        return web.json_response({"going": going, "pending": pending, "last": making["last"],
                                  "default_parent": create_mod.default_parent()})

    async def set_ignored(request):
        """Paramètres → Dossiers ignorés: the folders the cockpit never shows (1.5.1), those
        of the application open (1.6)."""
        data = await body(request)
        names = data.get("ignored")
        if not isinstance(names, list):
            return web.json_response({"error": "liste attendue"}, status=400)
        if not state.app_folder:
            return web.json_response({"error": "aucune application ouverte"}, status=409)
        state.set_ignored(names)
        return web.json_response(state_payload())

    async def close_pair(request):
        state.forget_pair()
        return web.json_response({"ok": True})

    async def forms(request):
        a, w = need_pair()
        return web.json_response(forms_payload(a, w, rn))

    async def question_ctx(request):
        a, w = need_pair()
        out = question_context(a, w, rn, request.query.get("id", ""))
        if out is None:
            return web.json_response({"error": "cette question n'est plus à répondre — rechargez"}, status=404)
        return web.json_response(out)

    async def save(request):
        a, w = need_pair()
        data = await body(request)
        items = data.get("items") or []
        results = save_items(a, w, rn, items)
        # A save of answers is a scan trigger (§2.3).
        state.clear_fresh(a, feature_of(w))
        return web.json_response({"results": results})

    async def bugfix_new(request):
        a, w = need_pair()
        if rn.is_running(a):
            return web.json_response({"error": "une commande tourne : pas de nouvelle correction maintenant"}, status=409)
        try:
            name = new_bugfix(a, feature_of(w))
        except OSError as e:
            return web.json_response({"error": f"dossier non créé : {e}"}, status=500)
        return web.json_response({"name": name})

    def buglist_path(a, w, name):
        if not BUGFIX.match(name or "") or name not in bugfixes(a, feature_of(w)):
            raise web.HTTPBadRequest(text=json.dumps({"error": "correction inconnue"}),
                                     content_type="application/json")
        return os.path.join(work_dir(a, feature_of(w)), name, "bug-list.md")

    async def buglist_get(request):
        a, w = need_pair()
        name = request.query.get("name", "")
        p = buglist_path(a, w, name)
        try:
            text = textfile.load(p).text() if os.path.exists(p) else ""
        except textfile.UnreadableFile as e:
            return web.json_response({"error": str(e)}, status=500)
        editable = not os.path.exists(os.path.join(os.path.dirname(p), "desc-bug.md"))
        return web.json_response({"name": name, "text": text, "editable": editable})

    async def buglist_put(request):
        """Writes `bug-list.md`, and nothing else, while the diagnostic has
        not read it yet (no `desc-bug.md`)."""
        a, w = need_pair()
        data = await body(request)
        p = buglist_path(a, w, data.get("name", ""))
        if os.path.exists(os.path.join(os.path.dirname(p), "desc-bug.md")):
            return web.json_response({"error": "desc-bug.md existe : le diagnostic a déjà lu cette bug-list"}, status=409)
        text = data.get("text") or ""
        try:
            old = textfile.load(p) if os.path.exists(p) else None
            nl = old.newline if old else "\n"
            body_text = nl.join(text.replace("\r\n", "\n").split("\n")).rstrip() + (nl if text.strip() else "")
            textfile.write_bytes(p, body_text.encode("utf-8"))
        except (OSError, textfile.UnreadableFile) as e:
            return web.json_response({"error": f"bug-list.md non écrit : {e}"}, status=500)
        return web.json_response({"ok": True})

    async def run(request):
        a, w = need_pair()
        data = await body(request)
        cmd = (data.get("command") or "").strip().lstrip("/")
        args = (data.get("args") or "").strip()
        if cmd not in {c["name"] for c in list_commands(a)}:
            return web.json_response({"error": f"commande inconnue : /{cmd}"}, status=400)
        if "\n" in args or "\r" in args:
            return web.json_response({"error": "l'argument tient sur une ligne"}, status=400)
        if bulk["going"]:
            return web.json_response({"error": "« Tout mettre à jour » installe la chaîne : lancer après"}, status=409)
        # One run at a time, whatever the application (1.6): said with where it goes.
        busy = busy_payload()
        if busy:
            return web.json_response({"error": busy_text(busy), "busy": busy}, status=409)
        # A deploy building in this application (1.8): its build and the run's
        # merge would race.
        if dep.going_in(a):
            return web.json_response({"error": "un déploiement construit dans cette application : lancer après sa fin"},
                                     status=409)
        # 1.12 §2: GitHub first — what the other computer pushed is pulled
        # before anything reads the files, the chain's version included.
        refused, synced = await synced_first(a)
        if refused:
            return refused
        # A chain not « à jour » (§20): the launch asks first.
        ch = chain_state(a)
        if ch.get("state") != chain_mod.UP_TO_DATE and not data.get("chain_ok"):
            return web.json_response({"error": ch["summary"], "chain": ch, "sync": synced}, status=409)
        try:
            r = await rn.start(a, w, feature_of(w), cmd, args)
        except runner_mod.Busy as e:
            b = busy_payload()
            return web.json_response({"error": busy_text(b) if b else str(e), "busy": b}, status=409)
        return web.json_response({"run": r.snapshot(), "sync": synced})

    def busy_text(b):
        return (f"une commande tourne déjà : {b['prompt']}" if b["active"]
                else f"une commande tourne déjà dans « {b['app_name']} » : {b['prompt']} — une seule à la fois, "
                     "toutes applications confondues")

    def going_repo():
        """The run going, wherever it goes (1.6) — « Arrêter », a card, the
        idle question act on it from any screen."""
        x = rn.going()
        if not x:
            raise web.HTTPConflict(text=json.dumps({"error": "aucune commande en cours"}),
                                   content_type="application/json")
        return x.repo

    async def stop_now(request):
        a = going_repo()
        try:
            await rn.stop_now(a)
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"ok": True})

    async def chain_install(request):
        """Paramètres → « Installer / mettre à jour la chaîne » (§20), and
        1.6 an application's row: `folder`, the active one by default — also
        one where no feature opens yet. Refused while a run goes there;
        files the chain did not leave as they are: 409 with the list, and
        the page asks before sending `confirm`."""
        data = await body(request)
        a = listed_folder(data) if data.get("folder") else state.app_folder
        if not a or not os.path.isdir(a):
            return web.json_response({"error": "aucune application ouverte"}, status=409)
        if rn.is_running(a):
            return web.json_response({"error": "une commande tourne : pas d'installation maintenant"}, status=409)
        if bulk["going"]:
            return web.json_response({"error": "« Tout mettre à jour » est en cours"}, status=409)
        refused, synced = await synced_first(a)
        if refused:
            return refused
        loop = asyncio.get_running_loop()
        try:
            res = await loop.run_in_executor(None, lambda: chain_mod.install(
                a, CHAIN_ROOT, confirm=bool(data.get("confirm")), push=CHAIN_PUSH))
        except chain_mod.NeedsConfirm as e:
            return web.json_response({"error": "fichiers à confirmer", "overwrite": e.files,
                                      "chain": chain_state(a)}, status=409)
        except chain_mod.InstallError as e:
            return web.json_response({"error": str(e)}, status=409)
        print(f"Chaîne installée dans {a} : {res['commit']} du {res['date']}"
              + (f", commit {res['app_commit']}" if res["app_commit"] else ", rien à commiter")
              + (" et poussé" if res["pushed"] else f" — push : {res['push_error']}" if res["push_error"] else "")
              + ".", flush=True)
        if res["app_commit"]:
            refresh_later(a)
        return web.json_response({"ok": True, "result": res, "chain": chain_state(a), "sync": synced})

    async def chain_install_all(request):
        """« Tout mettre à jour » (1.6): the chain installed in every
        application « en retard », one after the other — chain.py's install,
        its commit and push in each, its refusals unchanged. Never with
        `confirm`: « modifiée sur place » and « absente » are listed with
        their reason, for their own install. One with a run going is left,
        and said. One line per application."""
        if bulk["going"]:
            return web.json_response({"error": "« Tout mettre à jour » est déjà en cours"}, status=409)
        bulk["going"] = True
        loop = asyncio.get_running_loop()

        def prepare(folder):
            """1.12 §2, in each application before its install."""
            res = sync_mod.before_launch(book, folder)
            for d in res["done"]:
                sync_said(folder, "avant d'installer", d)
            announce(folder, res["sync"])
            return None if res["ok"] else res["error"]
        try:
            lines = await loop.run_in_executor(None, lambda: apps_mod.update_all(
                state.apps(), chain_state,
                lambda f: chain_mod.install(f, CHAIN_ROOT, confirm=False, push=CHAIN_PUSH),
                rn.is_running, prepare))
        finally:
            bulk["going"] = False
        for x in lines:
            if x.get("outcome") == apps_mod.UPDATED:
                refresh_later(x["folder"])
        bulk["report"] = {"at": datetime.now().isoformat(timespec="seconds"), "lines": lines}
        for x in lines:
            print(f"Tout mettre à jour — {x['name']} : {x['outcome']} — {x['text']}", flush=True)
        return web.json_response(bulk["report"])

    async def set_mode(request):
        data = await body(request)
        try:
            state.set_mode(data.get("mode"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"mode": state.mode})

    async def diagnose(a):
        key = runner_mod.repo_key(a)
        diag["running"].add(key)
        try:
            result = await asyncio.get_running_loop().run_in_executor(None, diag_runner, a)
            state.set_diagnostic(result, app=a)
            return result
        finally:
            diag["running"].discard(key)

    def auto_diagnostic(a):
        """No result stored for this application: its diagnostic runs once,
        in the background, and its result is kept — one per application, each
        its own stack (1.6). Paramètres → Outils sur cet ordinateur (1.9) still runs it on demand."""
        if not a:
            return
        key = runner_mod.repo_key(a)
        if key in diag["auto_done"] or key in diag["running"] or state.diagnostic(a) is not None:
            return
        diag["auto_done"].add(key)

        async def go():
            try:
                await diagnose(a)
            except Exception as e:      # reported, never raised into the loop
                print(f"Diagnostic automatique non abouti ({a}) : {e}", flush=True)
        diag["tasks"][key] = asyncio.get_running_loop().create_task(go())

    def sync_chain():
        """§6 — agent-chain's own clone, when the cockpit starts: fetched;
        « en retard », pulled (fast-forward only), and a restart asked."""
        chain_sync["checking"] = True
        notice = error = ""
        try:
            with book.lock(CHAIN_ROOT):
                st = book.put(CHAIN_ROOT, sync_mod.compute(CHAIN_ROOT))
                if st["state"] == sync_mod.BEHIND:
                    r = sync_mod.pull_ff(CHAIN_ROOT)
                    if r["ok"]:
                        notice = CHAIN_RESTART
                        sync_said(CHAIN_ROOT, "au démarrage", f"git pull --ff-only — {st['behind']} commit(s) récupéré(s)")
                    else:
                        error = ("La nouvelle version du cockpit et de la chaîne n'a pas pu être récupérée : "
                                 + r["message"])
                        sync_said(CHAIN_ROOT, "au démarrage", error)
                    st = book.put(CHAIN_ROOT, sync_mod.compute(CHAIN_ROOT, fetch=False))
                chain_sync.update(sync=st, notice=notice, error=error)
        finally:
            chain_sync["checking"] = False
        announce(CHAIN_ROOT, chain_sync["sync"])

    async def opening(_app):
        loop_box["loop"] = asyncio.get_running_loop()
        loop = loop_box["loop"]
        # 1.12: GitHub, when the cockpit opens — agent-chain's clone, then
        # every application, in the background.
        if SYNC_CHAIN_AT_START:
            loop.run_in_executor(None, sync_chain)
        if SYNC_APPS_AT_START:
            for x in state.apps():
                refresh_later(x["folder"])
        # 1.6: the active application's, a feature open or not.
        a = state.app_folder
        if a and os.path.isdir(a):
            auto_diagnostic(a)

    async def run_diagnostic(request):
        a = state.app_folder
        if not a or not os.path.isdir(a):
            return web.json_response({"error": "aucune application active"}, status=409)
        return web.json_response(await diagnose(a))

    # ------------------------------------------------ statistics (1.4.5)
    def stats_args(request, data=None):
        """(feature, period, app). 1.6: `app` — the active application by
        default (""), or « toutes » ("*"), every feature then."""
        a, w = need_pair()
        q = data if data is not None else request.query
        app = None if (q.get("app") or "").strip() == "*" else a
        f = (q.get("feature") or "").strip()
        feature = None if f == "*" or app is None else (f or feature_of(w))
        if feature is not None and state.is_ignored(feature):
            raise web.HTTPBadRequest(text=json.dumps({"error": "fonctionnalité ignorée : Paramètres → Dossiers ignorés"}),
                                     content_type="application/json")
        return feature, q.get("period") or "tout", app

    def stats_data(feature, period, app):
        names = {runner_mod.repo_key(x["folder"]): x["name"] for x in state.apps()}
        out = statsview.build(store.path if store else None, feature, period, app=app,
                              ignored_by_app=state.ignored_by_app(), names=names)
        out["apps"] = [{"name": x["name"], "folder": x["folder"]} for x in state.apps()]
        return out

    async def stats_get(request):
        feature, period, app = stats_args(request)
        data = stats_data(feature, period, app)
        # « Par lot »: its attempts are the verdict's (code_rules.md, T-ESSAIS),
        # read from the files — the store does not hold them.
        if feature and data.get("by_lot"):
            a, _ = need_pair()
            for row in data["by_lot"]:
                W = scan_mod.Folder(codelots.work_path(a, feature, row["folder"]))
                v = scan_mod.lot_verdict(W, row["lot"]) if W.has("code", row["lot"]) else None
                row["attempts"] = v["attempts"] if v else (0 if W.has("code", row["lot"]) else None)
                row["status"] = (v["status"] or None) if v else None
        return web.json_response(data)

    # ------------------------------------------------------ the Code tab (1.5)
    def code_args(request):
        a, w = need_pair()
        feature = feature_of(w)
        folder = (request.query.get("folder") or "").strip("/")
        if folder and folder not in bugfixes(a, feature):
            raise web.HTTPBadRequest(text=json.dumps({"error": "dossier de correction inconnu"}),
                                     content_type="application/json")
        return a, feature, folder

    def code_payload(a, feature, folder):
        run = rn.current(a)
        snap = run.snapshot() if run and run.id else None
        wts = rn.live_worktrees(a)
        _, _, bs, _, _, _ = collect_forms(a, feature, rn)
        opens = [{"id": b.id, "rel": b.rel, "lot": b.lot} for b in bs]
        passes = codelots.store_passes(store.path if store else None, feature, a) + live_passes(snap, feature)
        out = codelots.read_lots(a, feature, folder, wts, passes, snap, opens)
        bf = bugfixes(a, feature)
        out["acts_on"] = bf[-1] if bf else ""
        out["run"] = ({"command": snap["command"], "started_at": snap["started_at"], "status": snap["status"],
                       "prompt": snap["prompt"]} if snap else None)
        out["stop_file"] = os.path.exists(rn.stop_file(a, feature))
        return out

    async def code_get(request):
        a, feature, folder = code_args(request)
        loop = asyncio.get_running_loop()
        return web.json_response(await loop.run_in_executor(None, code_payload, a, feature, folder))

    def live_passes(snap, feature):
        """The passes of the run going that have handed back: stored only when
        the run ends, read from the runner meanwhile. Their written tokens are
        known at the end of the run alone."""
        if not snap or snap.get("status") == "ended" or (snap.get("work") or "").split("/")[0] != feature:
            return []
        return [{**p, "parent_tool_use_id": p.get("parent"), "run_id": snap["id"], "live": True,
                 "run_command": snap["prompt"], "output_tokens": None} for p in snap.get("passes") or []]

    async def code_lot(request):
        a, feature, folder = code_args(request)
        lot = request.query.get("lot", "")
        run = rn.current(a)
        snap = run.snapshot() if run and run.id else None
        passes = codelots.store_passes(store.path if store else None, feature, a) + live_passes(snap, feature)
        loop = asyncio.get_running_loop()
        out = await loop.run_in_executor(None, codelots.lot_detail, a, feature, folder, lot,
                                         rn.live_worktrees(a), passes)
        if out is None:
            return web.json_response({"error": f"{lot} n'est pas dans la séquence de ce dossier"}, status=404)
        return web.json_response(out)

    async def stats_csv(request):
        feature, period, app = stats_args(request)
        kind = request.query.get("kind", "runs")
        files = statsview.csv_files(stats_data(feature, period, app))
        name, text = files[1] if kind == "passes" else files[0]
        return web.Response(text=text, content_type="text/csv", charset="utf-8",
                            headers={"Content-Disposition": f'attachment; filename="{name}"'})

    async def stats_export(request):
        """« Exporter »: the runs and the agent passes of the current filters,
        as two CSV files in the folder the Product Owner picks."""
        data = await body(request)
        feature, period, app = stats_args(request, data)
        loop = asyncio.get_running_loop()
        try:
            folder = await loop.run_in_executor(None, export_picker, default_export_folder())
        except Exception as e:
            return web.json_response({"error": f"le sélecteur n'a pas pu s'ouvrir ({e})"}, status=500)
        if not folder:
            return web.json_response({"cancelled": True})
        written = []
        try:
            for name, text in statsview.csv_files(stats_data(feature, period, app)):
                path = os.path.join(folder, name)
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
                written.append(path)
        except OSError as e:
            return web.json_response({"error": f"fichier non écrit : {e}", "files": written}, status=500)
        return web.json_response({"files": written})

    async def continue_wait(request):
        a = going_repo()
        try:
            rn.continue_waiting(a)
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"ok": True})

    async def continue_session(request):
        a, _ = need_pair()
        try:
            r = await rn.continue_session(a)
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        except runner_mod.Busy as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"run": r.snapshot()})

    async def stop_next(request):
        a = going_repo()
        try:
            path = rn.stop_at_next_lot(a)
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        except OSError as e:
            return web.json_response({"error": f"stop.md non écrit : {e}"}, status=500)
        return web.json_response({"ok": True, "file": path})

    async def disarm(request):
        a, w = need_pair()
        try:
            target = rn.disarm_stop_file(a, feature_of(w))
        except OSError as e:
            return web.json_response({"error": str(e)}, status=500)
        return web.json_response({"ok": True, "file": target})

    async def permission(request):
        a = going_repo()
        data = await body(request)
        try:
            rn.answer_permission(a, data.get("id", ""), bool(data.get("allow")))
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"ok": True})

    async def events(request):
        # 1.6: every run's events, whatever its application — each carries
        # `app`; the stream so far is the active application's run.
        a = state.app_folder
        resp = web.StreamResponse(headers={"Content-Type": "text/event-stream",
                                           "Cache-Control": "no-cache",
                                           "X-Accel-Buffering": "no"})
        await resp.prepare(request)
        # 1.5 — a page opening during a run is given its stream so far,
        # rebuilt from the run's log, then everything after. Subscribing and
        # reading the log happen with no await between: what the log holds
        # has been emitted, what comes next is in the queue.
        # Replayed events carry `replay`, the first of them how many older
        # ones were left out; the page starts afresh on each connection.
        q = rn.watch()
        evs, dropped = rn.replay(a) if a else ([], 0)
        try:
            for i, ev in enumerate(evs):
                await resp.write(_sse({**ev, "replay": True, **({"dropped": dropped} if i == 0 and dropped else {})}))
            while True:
                try:
                    ev = await asyncio.wait_for(q.get(), timeout=15)
                    await resp.write(_sse(ev))
                except asyncio.TimeoutError:
                    await resp.write(b": ping\n\n")
        except (ConnectionResetError, asyncio.CancelledError):
            pass
        finally:
            rn.unwatch(q)
        return resp

    # ---------------------------------------------------- Déploiement (1.8)
    def deploy_app():
        a = state.app_folder
        if not a or not os.path.isdir(a):
            raise web.HTTPConflict(text=json.dumps({"error": "aucune application active"}),
                                   content_type="application/json")
        return a

    def run_here(a):
        """The chain run going in this application, or None."""
        x = rn.going()
        return x if x and runner_mod.repo_key(x.repo) == runner_mod.repo_key(a) else None

    def run_refusal(a, what):
        x = run_here(a)
        if not x:
            return None
        return web.json_response({"error": f"une commande de la chaîne tourne dans cette application : {x.prompt} — "
                                           f"{what}", "run": {"prompt": x.prompt, "started_at": x.started_at}},
                                 status=409)

    async def deploy_get(request):
        """The screen's frame: the adapters, the profile, the main checkout's
        commit, the run going here, the job, the choice remembered."""
        a = deploy_app()
        loop = asyncio.get_running_loop()
        head = await loop.run_in_executor(None, deploy_mod.head_of, a)
        x, j = run_here(a), dep.going()
        return web.json_response({
            "app": a, "app_name": state.app_name, "describe": dep.describe(), "profile": dep.profile(a),
            "head": head, "run": {"prompt": x.prompt, "started_at": x.started_at} if x else None,
            "job": dep.job_for(a),
            "elsewhere": {"app_name": j.app_name} if j and deploy_mod.app_key(j.app) != deploy_mod.app_key(a) else None,
            "choice": state.deploy_choice(a)})

    async def deploy_destinations(request):
        a = deploy_app()
        loop = asyncio.get_running_loop()
        return web.json_response(await loop.run_in_executor(None, dep.destinations, a))

    async def deploy_job(request):
        a = deploy_app()
        return web.json_response({"job": dep.job_for(a)})

    async def deploy_choice(request):
        a = deploy_app()
        data = await body(request)
        if not isinstance(data.get("choice"), dict):
            return web.json_response({"error": "choix attendu"}, status=400)
        return web.json_response({"choice": state.set_deploy_choice(a, data["choice"])})

    async def deploy_start(request):
        """« Construire et installer ». Refused while a chain run goes in this
        application: the build would race the run's merge."""
        a = deploy_app()
        data = await body(request)
        refused = run_refusal(a, "le build ferait la course avec son merge : déployer après sa fin")
        if refused:
            return refused
        choice = data.get("choice") if isinstance(data.get("choice"), dict) else {}
        state.set_deploy_choice(a, choice)
        loop = asyncio.get_running_loop()
        head = await loop.run_in_executor(None, deploy_mod.head_of, a)
        try:
            job = await loop.run_in_executor(None, dep.start, a, state.app_name, choice, head)
        except (deploy_mod.DeployError, deploy_mod.ActionError) as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"job": job.record()})

    async def deploy_action(request):
        a = deploy_app()
        data = await body(request)
        args = data.get("args") if isinstance(data.get("args"), dict) else {}
        loop = asyncio.get_running_loop()
        try:
            res = await loop.run_in_executor(None, dep.act, a, data.get("type", ""), data.get("action", ""),
                                             data.get("dest", ""), args)
        except deploy_mod.ActionError as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response(res)

    async def deploy_image(request):
        a = deploy_app()
        q = request.query
        loop = asyncio.get_running_loop()
        try:
            png = await loop.run_in_executor(None, dep.image, a, q.get("type", ""), q.get("action", ""),
                                             q.get("dest", ""), {})
        except deploy_mod.ActionError as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.Response(body=png, content_type="image/png", headers={"Cache-Control": "no-store"})

    async def deploy_journal(request):
        a = deploy_app()
        q = request.query
        try:
            after = int(q.get("after") or 0)
        except ValueError:
            after = 0
        loop = asyncio.get_running_loop()
        try:
            out = await loop.run_in_executor(None, lambda: dep.journal(
                a, q.get("type", ""), q.get("dest", ""), q.get("target") or None, after, q.get("reopen") == "1"))
        except deploy_mod.ActionError as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response(out)

    async def deploy_journal_save(request):
        a = deploy_app()
        data = await body(request)
        try:
            path = dep.journal_save(a, data.get("dest", ""), data.get("target") or None)
        except (deploy_mod.ActionError, OSError) as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"path": path})

    async def deploy_profile_save(request):
        """Déploiement → Profil (1.9; Paramètres → Déploiement in 1.8): the targets written to deploy.json,
        committed alone in the application and pushed. Refused while a run
        or a deploy goes there."""
        a = deploy_app()
        data = await body(request)
        refused = run_refusal(a, "le profil s'enregistre après sa fin")
        if refused:
            return refused
        if dep.going_in(a):
            return web.json_response({"error": "un déploiement est en cours dans cette application : "
                                               "le profil s'enregistre après sa fin"}, status=409)
        targets = data.get("targets")
        if not isinstance(targets, list):
            return web.json_response({"error": "liste de cibles attendue"}, status=400)
        refused, _ = await synced_first(a)
        if refused:
            return refused
        loop = asyncio.get_running_loop()
        try:
            res = await loop.run_in_executor(None, lambda: deploy_profile.save(a, targets, push=PROFILE_PUSH))
        except deploy_profile.ProfileError as e:
            return web.json_response({"error": str(e), "errors": e.errors}, status=400)
        print(f"Profil de déploiement de {a} : "
              + ((f"commit {res['commit']}" + (" et poussé" if res["pushed"] else
                                               f" — push : {res['push_error']}" if res["push_error"] else ""))
                 if res["commit"] else "rien n'avait changé") + ".", flush=True)
        if res["commit"]:
            refresh_later(a)
        return web.json_response({**res, "profile": dep.profile(a)})

    async def deploy_cleanup(_app):
        dep.stop_all()

    # ------------------------------------------------------ Données (1.10)
    # `.claude/formats/donnees.md`: the two folders, their index, the
    # private section of `.gitignore`. The files are joined at once; the
    # index, `.gitignore`, the removals and the commit wait for « Enregistrer »,
    # which a run going in the application refuses.
    def data_where(q):
        a, w = need_pair()
        try:
            return a, donnees_mod.folder_of(q.get("tab", ""), feature_of(w)), feature_of(w)
        except donnees_mod.DataError as e:
            raise web.HTTPBadRequest(text=json.dumps({"error": str(e)}), content_type="application/json")

    def data_bytes(data):
        try:
            return base64.b64decode(data.get("data") or "", validate=True)
        except ValueError:
            raise web.HTTPBadRequest(text=json.dumps({"error": "contenu du fichier illisible"}),
                                     content_type="application/json")

    async def data_get(request):
        a, _, feature = data_where(request.query)
        loop = asyncio.get_running_loop()
        out = await loop.run_in_executor(None, donnees_mod.listing, a, request.query.get("tab"), feature)
        out["running"] = bool(run_here(a))
        return web.json_response(out)

    async def data_preview(request):
        a, _, feature = data_where(request.query)
        try:
            out = donnees_mod.preview(a, request.query.get("tab"), feature, request.query.get("name", ""))
        except donnees_mod.DataError as e:
            return web.json_response({"error": str(e)}, status=404)
        return web.json_response(out)

    async def data_file(request):
        """The file itself, for an image's preview."""
        a, _, feature = data_where(request.query)
        try:
            p = donnees_mod.file_path(a, request.query.get("tab"), feature, request.query.get("name", ""))
        except donnees_mod.DataError as e:
            return web.json_response({"error": str(e)}, status=404)
        ctype = donnees_mod.IMAGE_TYPES.get(os.path.splitext(p)[1].lower(), "application/octet-stream")
        return web.Response(body=textfile.read_bytes(p), content_type=ctype,
                            headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
                                     "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'"})

    async def data_join(request):
        """« Joindre des fichiers »: one file, copied into the folder as it
        came. Its entry is the page's to fill, until « Enregistrer »."""
        data = await body(request)
        a, folder, _ = data_where(data)
        raw = data_bytes(data)
        try:
            name = donnees_mod.join(a, folder, data.get("name", ""), raw, replace=bool(data.get("replace")))
        except donnees_mod.DataError as e:
            exists = "déjà dans" in str(e)
            return web.json_response({"error": str(e), "exists": exists}, status=409 if exists else 400)
        except OSError as e:
            return web.json_response({"error": f"fichier non copié : {e}"}, status=500)
        print(f"Données : {name} joint dans {folder}/ ({len(raw)} octets).", flush=True)
        return web.json_response({"name": name, "folder": folder + "/"})

    def data_said(res, folder):
        print(f"Données {folder}/ : "
              + ((f"commit {res['commit']} « {res['message']} »" + (" et poussé" if res["pushed"] else
                  f" — push : {res['push_error']}" if res["push_error"] else ""))
                 if res["commit"] else "rien n'avait changé") + ".", flush=True)

    async def data_save(request):
        """« Enregistrer »: the index in the format, `.gitignore`'s private
        section, the removed files with their entries, one commit
        `donnees: <what changed>`, the push. Refused while a run goes here."""
        data = await body(request)
        a, folder, feature = data_where(data)
        refused = run_refusal(a, "les données s'enregistrent après sa fin")
        if refused:
            return refused
        entries, removed = data.get("entries"), data.get("removed") or []
        if not isinstance(entries, list) or not isinstance(removed, list):
            return web.json_response({"error": "entrées attendues"}, status=400)
        refused, _ = await synced_first(a)
        if refused:
            return refused
        loop = asyncio.get_running_loop()
        try:
            res = await loop.run_in_executor(None, lambda: donnees_mod.save(
                a, folder, entries, [str(r) for r in removed], push=DONNEES_PUSH))
        except (donnees_mod.DataError, TypeError) as e:
            return web.json_response({"error": str(e)}, status=400)
        except OSError as e:
            return web.json_response({"error": f"non écrit : {e}"}, status=500)
        data_said(res, folder)
        if res["commit"]:
            refresh_later(a)
        listing = await loop.run_in_executor(None, donnees_mod.listing, a, data.get("tab"), feature)
        return web.json_response({**res, "listing": listing})

    async def data_answer(request):
        """« À répondre » → « Joindre un fichier », on a question whose
        `Folder:` line names a folder (§5): the file saved there, its entry
        written in the index, the commit and the push — then the file's name
        written in `Answer:`, as the index names it."""
        a, w = need_pair()
        data = await body(request)
        refused = run_refusal(a, "le fichier se joint après sa fin")
        if refused:
            return refused
        qs = collect_forms(a, w, rn)[0]
        entry = next((q for q in qs if q.id == data.get("id")), None)
        if entry is None:
            return web.json_response({"error": "cette question n'attend plus de réponse — rechargez"}, status=404)
        if data.get("fingerprint") != entry.fingerprint:
            return web.json_response({"error": "la question a changé depuis l'affichage — rechargez"}, status=409)
        marker = folder_marker(entry)
        if marker is None:
            return web.json_response({"error": "cette question ne demande pas de fichier"}, status=400)
        raw = data_bytes(data)
        meta = data.get("entry") or {}
        try:
            folder = donnees_mod.folder_of_marker(a, marker)
            name = donnees_mod.check_name(data.get("name", ""))
            ent = donnees_mod.Entry(name=name, what=str(meta.get("what", "")).strip(),
                                    source=str(meta.get("source", "")).strip(),
                                    date=str(meta.get("date", "")).strip(), private=str(meta.get("private", "")))
            bad = donnees_mod.check_entry(ent)
            if bad:
                raise donnees_mod.DataError(f"{name} : {', '.join(bad)}")
        except donnees_mod.DataError as e:
            return web.json_response({"error": str(e)}, status=400)
        if os.path.exists(os.path.join(a, *folder.split("/"), name)) and not data.get("replace"):
            return web.json_response({"error": f"« {name} » est déjà dans {folder}/", "exists": True}, status=409)
        refused, _ = await synced_first(a)
        if refused:
            return refused
        loop = asyncio.get_running_loop()

        def go():
            donnees_mod.join(a, folder, name, raw, replace=True)
            return donnees_mod.add_entry(a, folder, ent, push=DONNEES_PUSH,
                                         answer_for=f"{os.path.basename(entry.file)} Q{entry.number}")
        try:
            res = await loop.run_in_executor(None, go)
        except donnees_mod.DataError as e:
            return web.json_response({"error": str(e)}, status=400)
        except OSError as e:
            return web.json_response({"error": f"non écrit : {e}"}, status=500)
        data_said(res, folder)
        if res["commit"]:
            refresh_later(a)
        written = writer.write_question(entry, writer.Choice(kind="free", text=name))
        state.clear_fresh(a, feature_of(w))
        return web.json_response({**res, "name": name, "folder": folder + "/", "answer": written.to_dict()})

    # ------------------------------------------------- GitHub (1.12)
    def sync_busy(folder):
        """Why nothing may touch this clone's git now, or None."""
        if bulk["going"]:
            return "« Tout mettre à jour » est en cours"
        if os.path.normcase(os.path.abspath(folder)) == os.path.normcase(os.path.abspath(CHAIN_ROOT)):
            return None
        if rn.is_running(folder):
            return "une commande tourne dans cette application : après sa fin"
        if dep.going_in(folder):
            return "un déploiement construit dans cette application : après sa fin"
        return None

    async def sync_get(request):
        """Where a clone stands — the known state, else fetched now."""
        folder = sync_target(dict(request.query))
        if not folder:
            return web.json_response({"error": "aucune application"}, status=409)
        st = await asyncio.get_running_loop().run_in_executor(None, book.get, folder)
        return web.json_response({"sync": st})

    async def sync_refresh(request):
        data = await body(request)
        folder = sync_target(data)
        if not folder:
            return web.json_response({"error": "aucune application"}, status=409)
        return web.json_response({"sync": await resync(folder)})

    async def sync_push(request):
        """« Envoyer » (§3): `git push`. Refused by GitHub: fetched again,
        and the new state said."""
        data = await body(request)
        folder = sync_target(data)
        if not folder:
            return web.json_response({"error": "aucune application"}, status=409)
        why = sync_busy(folder)
        if why:
            return web.json_response({"error": why}, status=409)
        loop = asyncio.get_running_loop()

        def go():
            with book.lock(folder):
                return sync_mod.push(folder)
        p = await loop.run_in_executor(None, go)
        sync_said(folder, "Envoyer", "envoyé" if p["ok"] else p["message"])
        st = await resync(folder)
        if not p["ok"]:
            return web.json_response({"error": p["message"] + (f" — {st['summary'].lower()}" if p["rejected"] else ""),
                                      "push": p, "sync": st}, status=409)
        return web.json_response({"ok": True, "push": p, "sync": st})

    async def sync_reconcile(request):
        """« Réconcilier » (§4): `git pull --rebase=merges`; a conflict aborted, the
        clone back as it was, the files named."""
        data = await body(request)
        folder = sync_target(data)
        if not folder:
            return web.json_response({"error": "aucune application"}, status=409)
        why = sync_busy(folder) or (("une commande tourne : agent-chain se réconcilie après sa fin" if rn.going() else None)
                                     if folder == CHAIN_ROOT else None)
        if why:
            return web.json_response({"error": why}, status=409)
        loop = asyncio.get_running_loop()

        def go():
            with book.lock(folder):
                return sync_mod.reconcile(folder)
        res = await loop.run_in_executor(None, go)
        sync_said(folder, "Réconcilier", res["message"])
        st = await resync(folder)
        res.pop("before", None)
        if not res["ok"]:
            res["error"] = res["message"]
        return web.json_response({**res, "sync": st}, status=200 if res["ok"] else 409)

    async def answers_send(request):
        """« Envoyer mes réponses » (§5): the commit the next command would
        make before its worktree — the feature folder, `chore: answers` —
        then the push. The open application's feature, or a row's: `folder`
        and its last feature."""
        data = await body(request)
        if data.get("folder"):
            folder = listed_folder(data)
            feature = state.app(folder).get("last_feature")
        else:
            folder, w = need_pair()
            feature = feature_of(w)
        if not feature:
            return web.json_response({"error": "aucune feature ouverte dans cette application"}, status=409)
        why = sync_busy(folder)
        if why:
            return web.json_response({"error": why}, status=409)
        loop = asyncio.get_running_loop()
        # GitHub first: what the other computer pushed comes in before the commit.
        res = await loop.run_in_executor(None, sync_mod.before_launch, book, folder)
        for d in res["done"]:
            sync_said(folder, "avant d'envoyer les réponses", d)
        if not res["ok"] and not res["reconcile"]:
            announce(folder, res["sync"])
            return web.json_response({"error": res["error"], "sync_refused": res}, status=409)

        def go():
            with book.lock(folder):
                sha = sync_mod.commit_answers(folder, feature)
                st = sync_mod.compute(folder, fetch=False)
                p = sync_mod.push(folder) if sha and st["state"] == sync_mod.AHEAD else None
                return sha, p
        try:
            sha, p = await loop.run_in_executor(None, go)
        except sync_mod.SyncError as e:
            return web.json_response({"error": str(e)}, status=409)
        sync_said(folder, "Envoyer mes réponses", (f"commit {sha} « {sync_mod.ANSWERS_MESSAGE} »" if sha else "rien à commiter")
                  + (", poussé" if p and p["ok"] else f", non poussé : {p['message']}" if p else ""))
        st = await resync(folder)
        state.clear_fresh(folder, feature)
        return web.json_response({"ok": True, "commit": sha, "message": sync_mod.ANSWERS_MESSAGE, "path": sync_mod.feature_path(feature),
                                  "pushed": bool(p and p["ok"]), "push": p, "sync": st,
                                  "diverged": res.get("reconcile", False)})

    async def apps_clone(request):
        """« Ajouter depuis GitHub » (§7): the repository's address and the
        parent folder; the clone, `core.longpaths=true` in it, then the list
        as « Ajouter » makes it."""
        data = await body(request)
        url = (data.get("url") or "").strip()
        parent = os.path.normpath((data.get("parent") or "").strip().strip('"')) if (data.get("parent") or "").strip() else ""
        name = sync_mod.repo_name(url)
        if not url or "\n" in url or not name:
            return web.json_response({"error": "l'adresse du dépôt manque"}, status=400)
        if not parent or not os.path.isdir(parent):
            return web.json_response({"error": "le dossier parent est introuvable"}, status=400)
        dest = os.path.join(parent, name)
        if os.path.exists(dest) and (not os.path.isdir(dest) or os.listdir(dest)):
            return web.json_response({"error": f"{dest} existe déjà et n'est pas vide : rien n'est cloné par-dessus"},
                                     status=409)
        res = await asyncio.get_running_loop().run_in_executor(None, sync_mod.clone, url, dest)
        sync_said(dest, "Ajouter depuis GitHub", "cloné" if res["ok"] else res["message"])
        if not res["ok"]:
            return web.json_response({"error": res["message"], "credentials": res["credentials"]}, status=409)
        err = apps_mod.check_new_app(dest)
        if err:
            return web.json_response({"error": f"cloné dans {dest}, mais : {err}"}, status=409)
        x, added = state.add_app(dest, data.get("name"))
        refresh_later(x["folder"])
        return web.json_response({"app": x, "added": added, "path": dest, "apps": apps_light()})

    async def longpaths_get(request):
        """« Outils sur cet ordinateur » (§7): `core.longpaths` of each
        application's own git config."""
        loop = asyncio.get_running_loop()

        def rows():
            return [{"name": x["name"], "folder": x["folder"],
                     "value": sync_mod.long_paths(x["folder"]) if os.path.isdir(x["folder"]) else None,
                     "exists": os.path.isdir(x["folder"])} for x in state.apps()]
        return web.json_response({"apps": await loop.run_in_executor(None, rows)})

    async def longpaths_set(request):
        data = await body(request)
        folder = listed_folder(data)
        try:
            await asyncio.get_running_loop().run_in_executor(None, sync_mod.set_long_paths, folder)
        except sync_mod.SyncError as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"ok": True, "value": sync_mod.long_paths(folder)})

    async def reveal_log(request):
        """1.9.1: a log's path is a link — its folder opens on this computer,
        the file selected. A log only: an existing .jsonl or .log file."""
        data = await body(request)
        given = str(data.get("path") or "")
        p = os.path.normpath(given) if given else ""
        if not p.lower().endswith(LOG_EXTENSIONS):
            return web.json_response({"error": f"ce n'est pas un journal : {given or '(vide)'}"}, status=400)
        if not os.path.isfile(p):
            return web.json_response({"error": f"le journal n'existe plus : {p}"}, status=404)
        try:
            REVEAL(p, True)
        except OSError as e:
            return web.json_response({"error": f"le dossier n'a pas pu s'ouvrir ({e})"}, status=500)
        return web.json_response({"ok": True})

    async def open_logs(request):
        """« Statistiques » → « Journaux bruts »: the logs folder — the runs',
        the deploys', server.log and next-ecarte.jsonl are all there."""
        try:
            os.makedirs(rn.log_dir, exist_ok=True)
            REVEAL(os.path.normpath(rn.log_dir), False)
        except OSError as e:
            return web.json_response({"error": f"le dossier n'a pas pu s'ouvrir ({e})"}, status=500)
        return web.json_response({"ok": True, "path": rn.log_dir})

    async def ping(request):
        """What a second start asks before starting a server of its own."""
        return web.json_response({"cockpit": True, "version": VERSION, "pid": os.getpid()})

    async def shutdown(request):
        """Paramètres → « Arrêter le cockpit ». With a run going, it asks
        first; confirmed, the run is stopped now, given STOP_GRACE seconds to
        end and record its relay, and the server stops."""
        data = await body(request)
        going = [x for x in rn.runs.values() if x.id and x.status != "ended"]
        if going and not data.get("confirm"):
            return web.json_response({"running": True, "prompt": going[0].prompt}, status=409)
        stopped = []
        for x in going:
            try:
                await rn.stop_now(x.repo)
            except runner_mod.NotRunning:
                continue
            ended = await rn.wait_ended(x.repo, STOP_GRACE)
            stopped.append({"prompt": x.prompt, "ended": ended})
        print("Arrêt du cockpit demandé depuis la page"
              + (f" ; run arrêté : {', '.join(x['prompt'] for x in stopped)}" if stopped else "") + ".",
              flush=True)
        if on_quit:
            asyncio.get_running_loop().call_later(0.3, on_quit)
        return web.json_response({"ok": True, "stopped": stopped})

    r = app.router
    r.add_get("/", index)
    r.add_get("/manifest.webmanifest", manifest)
    r.add_get("/icons/{name}", app_icon)
    r.add_get("/api/ping", ping)
    r.add_post("/api/reveal-log", reveal_log)
    r.add_post("/api/open-logs", open_logs)
    r.add_post("/api/shutdown", shutdown)
    r.add_get("/api/state", get_state)
    r.add_post("/api/check", check)
    r.add_post("/api/bugfix/new", bugfix_new)
    r.add_get("/api/bugfix/buglist", buglist_get)
    r.add_post("/api/bugfix/buglist", buglist_put)
    r.add_post("/api/pick-folder", pick_folder)
    r.add_post("/api/app-folder", app_folder)
    r.add_post("/api/open", open_pair)
    r.add_post("/api/close", close_pair)
    r.add_get("/api/forms", forms)
    r.add_get("/api/context", question_ctx)
    r.add_post("/api/save", save)
    r.add_post("/api/run", run)
    r.add_post("/api/stop-now", stop_now)
    r.add_post("/api/mode", set_mode)
    r.add_post("/api/chain/install", chain_install)
    r.add_post("/api/chain/install-all", chain_install_all)
    r.add_get("/api/apps", apps_get)
    r.add_post("/api/apps/add", apps_add)
    r.add_post("/api/apps/rename", apps_rename)
    r.add_post("/api/apps/remove", apps_remove)
    r.add_post("/api/apps/open", apps_open)
    r.add_post("/api/pick-file", pick_file)
    r.add_post("/api/create/check", create_check)
    r.add_get("/api/create", create_get)
    r.add_post("/api/create", create_start)
    r.add_post("/api/create/resume", create_resume)
    r.add_post("/api/create/forget", create_forget)
    r.add_post("/api/ignored", set_ignored)
    r.add_post("/api/diagnostic", run_diagnostic)
    r.add_post("/api/continue-wait", continue_wait)
    r.add_post("/api/continue-session", continue_session)
    r.add_post("/api/stop-next-lot", stop_next)
    r.add_post("/api/disarm-stop", disarm)
    r.add_post("/api/permission", permission)
    r.add_get("/api/events", events)
    r.add_get("/api/stats", stats_get)
    r.add_get("/api/code", code_get)
    r.add_get("/api/code/lot", code_lot)
    r.add_get("/api/stats/csv", stats_csv)
    r.add_post("/api/stats/export", stats_export)
    r.add_get("/api/deploy", deploy_get)
    r.add_get("/api/deploy/destinations", deploy_destinations)
    r.add_get("/api/deploy/job", deploy_job)
    r.add_post("/api/deploy/choice", deploy_choice)
    r.add_post("/api/deploy/start", deploy_start)
    r.add_post("/api/deploy/action", deploy_action)
    r.add_get("/api/deploy/image", deploy_image)
    r.add_get("/api/deploy/journal", deploy_journal)
    r.add_post("/api/deploy/journal/save", deploy_journal_save)
    r.add_post("/api/deploy/profile", deploy_profile_save)
    r.add_get("/api/donnees", data_get)
    r.add_get("/api/donnees/preview", data_preview)
    r.add_get("/api/donnees/file", data_file)
    r.add_post("/api/donnees/join", data_join)
    r.add_post("/api/donnees/save", data_save)
    r.add_post("/api/donnees/answer", data_answer)
    r.add_get("/api/sync", sync_get)
    r.add_post("/api/sync/refresh", sync_refresh)
    r.add_post("/api/sync/push", sync_push)
    r.add_post("/api/sync/reconcile", sync_reconcile)
    r.add_post("/api/answers/send", answers_send)
    r.add_post("/api/apps/clone", apps_clone)
    r.add_get("/api/longpaths", longpaths_get)
    r.add_post("/api/longpaths", longpaths_set)
    app.on_startup.append(opening)
    app.on_cleanup.append(deploy_cleanup)
    return app


def _limits(store):
    if not store:
        return {}
    try:
        return store.latest_limits()
    except Exception:
        return {}


def _with_usage(store, hist):
    """Each remembered run with its totals, read from the store by its log."""
    if not store or not hist:
        return hist
    try:
        found = store.runs_by_logs([h.get("log_path") for h in hist])
    except Exception:
        return hist
    for h in hist:
        r = found.get(h.get("log_path"))
        if r:
            h["usage"] = stats_mod.totals_summary(
                {k: r[k] for k in ("input_tokens", "cache_read_tokens", "cache_creation_tokens",
                                   "output_tokens")} if r["input_tokens"] is not None else None,
                r["duration_s"])
    return hist


def backfill(store, state, log_dir):
    """The logs written since 1.1, loaded once: a log already in the store is
    skipped. The feature and the `Next:` come from the remembered history."""
    hist = {}
    for h in state.all_history():
        if h.get("log_path"):
            hist[os.path.normcase(h["log_path"])] = {**h, "work": h.get("key", "").split("|", 1)[-1]}
    done = store.backfill(log_dir, hist)
    # The runs already stored: their agents' output, from their logs'
    # model_usage (1.4.3).
    done["outputs"] = store.backfill_outputs()
    # The lot of each pass already stored, once (1.5).
    done["lots"] = store.backfill_lots()
    # The application of each run stored before 1.6.
    done["apps"] = store.backfill_apps(app_resolver(state))
    return done


def app_resolver(state):
    """Which application a run stored without one belongs to (1.6): the
    working directory its log names — the application's folder, or a
    worktree under it —, else the application of its history entry, else
    the first application of the list, the one the cockpit knew before."""
    apps = state.apps()
    by_log = {os.path.normcase(h["log_path"]): h.get("key", "").split("|", 1)[0]
              for h in state.all_history() if h.get("log_path")}

    def listed(path):
        if not path:
            return None
        k = os.path.normcase(os.path.abspath(path))
        for x in apps:
            fk = os.path.normcase(os.path.abspath(x["folder"]))
            if k == fk or k.startswith(fk + os.sep):
                return x["folder"]
        return None

    def resolve(run):
        return (listed(run.get("cwd")) or listed(by_log.get(os.path.normcase(run.get("log_path") or "")))
                or (apps[0]["folder"] if apps else None))
    return resolve


def _sse(ev):
    return f"data: {json.dumps(ev, ensure_ascii=False)}\n\n".encode("utf-8")


async def serve(app, port, url, ouvrir, quit_box):
    """Serve until « Arrêter le cockpit » (or Ctrl+C in a console)."""
    quit_box["event"] = asyncio.Event()
    runner = web.AppRunner(app, shutdown_timeout=2)
    await runner.setup()
    site = web.TCPSite(runner, HOST, port)
    try:
        await site.start()
    except OSError:
        await runner.cleanup()
        raise
    print(f"Cockpit : {url}", flush=True)
    if ouvrir:
        asyncio.get_running_loop().call_later(0.3, OPEN_BROWSER, url)
    try:
        await quit_box["event"].wait()
    finally:
        print("Le cockpit s'arrête.", flush=True)
        await runner.cleanup()


def main(argv=None):
    """`pythonw server.py --ouvrir`, from lancer.bat. When a cockpit already
    answers on the port, only the browser opens on it. Returns the exit code."""
    p = argparse.ArgumentParser(description="Cockpit de la chaîne")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--ouvrir", action="store_true", help="ouvrir le navigateur")
    p.add_argument("--config", default=None)
    p.add_argument("--stats", default=None, help="la base de consommation (stats.sqlite par défaut)")
    p.add_argument("--journaux", default=None, help="le dossier des journaux (logs/ par défaut)")
    args = p.parse_args(argv)
    url = f"http://{HOST}:{args.port}/"
    log_dir = args.journaux or runner_mod.LOG_DIR

    startup.open_log(os.path.join(log_dir, startup.LOG_NAME))
    if startup.windowless():
        startup.hide_child_consoles()
    print(f"--- {datetime.now().isoformat(timespec='seconds')} · démarrage, pid {os.getpid()}, "
          + ("sans console" if startup.windowless() else "dans une console"), flush=True)

    other = startup.ping(args.port)
    if other:
        print(f"Un cockpit répond déjà sur {url} (pid {other.get('pid')}) : la page s'ouvre sur lui, "
              "aucun second serveur.", flush=True)
        if args.ouvrir:
            OPEN_BROWSER(url)
        return 0

    state = State(args.config) if args.config else State()
    store = stats_mod.Store(args.stats) if args.stats else stats_mod.Store()
    rn = runner_mod.Runner(on_end=make_on_end(state), mode_getter=lambda: state.mode, stats=store,
                           log_dir=log_dir)
    done = backfill(store, state, log_dir)
    if done["runs"]:
        print(f"Consommation : {done['runs']} journal(aux) ancien(s) chargé(s) dans stats.sqlite "
              f"({done['passes']} passage(s) d'agent, {done['limits']} mesure(s) d'usage).", flush=True)
    if done["outputs"]["runs"]:
        print(f"Consommation : tokens écrits retrouvés pour {done['outputs']['runs']} run(s) "
              f"({done['outputs']['passes']} passage(s) d'agent), d'après le model_usage des journaux.", flush=True)
    if done["apps"]:
        print(f"Consommation : l'application de {done['apps']} run(s) enregistré(s) avant 1.6 retrouvée.", flush=True)
    if state.migrated:
        print("config.json : migré en liste d'applications (1.6) — "
              + ", ".join(x["name"] for x in state.apps()) + ".", flush=True)
    if not done["lots"]["done"]:
        print(f"Consommation : le lot de chaque passage relu dans {done['lots']['runs']} journal(aux) "
              f"({done['lots']['passes']} passage(s) portent un lot).", flush=True)
    quit_box = {"event": None}

    def on_quit():
        if quit_box["event"] is not None:
            quit_box["event"].set()

    app = make_app(state, rn, on_quit=on_quit)
    try:
        asyncio.run(serve(app, args.port, url, args.ouvrir, quit_box))
    except KeyboardInterrupt:
        return 0
    except OSError as e:
        # Taken between the ping and the bind: by a cockpit started at the
        # same moment, or by another program.
        if startup.ping(args.port):
            print(f"Un cockpit a démarré sur {url} au même moment : la page s'ouvre sur lui.", flush=True)
            if args.ouvrir:
                OPEN_BROWSER(url)
            return 0
        msg = (f"Le port {args.port} est pris par un autre programme : le cockpit ne peut pas démarrer.\n"
               f"({e})")
        print(msg, flush=True)
        startup.error_box(msg)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
