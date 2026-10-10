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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

if __name__ == "__main__":
    # 1.16: the Python dependencies, before anything imports them — installed
    # when one is missing, in the mode Paramètres sets (deps.py).
    import deps as _deps  # noqa: E402
    if not _deps.at_start(next((sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a == "--config"), None)):
        sys.exit(1)

import aiohttp  # noqa: E402,F811
from aiohttp import web  # noqa: E402,F811

import apps as apps_mod  # noqa: E402
import autopilot as pilot_mod  # noqa: E402
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
import installs   # noqa: E402
import machine    # noqa: E402
import phone as phone_mod  # noqa: E402
import questions  # noqa: E402
import runner as runner_mod  # noqa: E402
import scan as scan_mod  # noqa: E402
import selfupdate  # noqa: E402
import startup  # noqa: E402
import stats as stats_mod  # noqa: E402
import statsview  # noqa: E402
import sync as sync_mod  # noqa: E402
import textfile   # noqa: E402
import usage as usage_mod  # noqa: E402
import webpush   # noqa: E402
import writer     # noqa: E402
from state import State  # noqa: E402

HOST = "127.0.0.1"
STATE_KEY = web.AppKey("state", State)
# 1.16: the port this server serves the page on — what a restart it starts
# itself takes over.
PORT_KEY = web.AppKey("port", dict)
DEPLOY_KEY = web.AppKey("deploy", deploy_mod.Deployer)
DEFAULT_PORT = 8765
VERSION = "1.18"
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
# 1.14 — agent-chain's clone fetched again when the home screen opens, at
# most every CHAIN_HOME_EVERY seconds; the tests put False here.
SYNC_CHAIN_ON_HOME = True
CHAIN_HOME_EVERY = 60.0
# 1.16 — a chain install while GitHub cannot be reached: refused.
OFFLINE_INSTALL = ("GitHub injoignable : la chaîne ne s'installe pas tant que GitHub ne répond pas — l'autre "
                   "ordinateur a peut-être déjà fait ce commit")
CHAIN_RESTART = ("Nouvelle version du cockpit et de la chaîne récupérée — « Mettre à jour le cockpit » "
                 "la met en service.")
# 1.14 — « Mettre à jour le cockpit »: how the new server is started — the
# tests put a fake here —, and the arguments this one was started with that
# the new one takes again (--config, --stats, --journaux).
SPAWN_SERVER = selfupdate.spawn
LAUNCH_ARGS = []
# A joined file comes in the request, base64 in JSON: what one may weigh.
MAX_REQUEST = 256 * 1024 * 1024
# 1.15 — how long a push service is given to take one notification.
PUSH_TIMEOUT = 15.0
# What opens the browser; the tests put a fake here.
OPEN_BROWSER = webbrowser.open
# 1.16 — « État de l'ordinateur »: checked when the cockpit starts; the
# server restarts itself, when nothing goes, once the code on disk is newer
# than the one it runs — looked at every RESTART_POLL seconds. The tests put
# False here.
MACHINE_AT_START = True
AUTO_RESTART = True
RESTART_POLL = 15.0
# 1.17 — the usage measure (usage.py): when the cockpit starts, when its home
# screen opens on a measure older than usage.STALE_S, and before a launch on
# one as old. The tests put False here, or a fake client in MEASURE_CLIENT.
MEASURE_USAGE = True
MEASURE_CLIENT = None
# 1.18 — the automatic mode's clock: the real one; the tests put a fake here.
PILOT_CLOCK = None
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


LOCAL_NAMES = phone_mod.LOCAL_NAMES
# 1.15 — through the phone's address: what is served before the code (the
# code page itself is "/"), and what only this computer's page may do.
PHONE_LOCAL_ONLY = {"/api/phone/settings", "/api/phone/disconnect",
                    # 1.16: a repair of this computer is made on this computer.
                    "/api/machine/repair", "/api/machine/session/answer", "/api/machine/session/code",
                    "/api/machine/session/cancel", "/api/cockpit/restart", "/api/install-mode",
                    # 1.17: Paramètres → Consommation.
                    "/api/usage/thresholds"}


def phone_open(path):
    return path in ("/", "/manifest.webmanifest", "/api/phone/login") or path.startswith("/icons/")
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
             diag_runner=None, export_picker=ask_export_folder, on_quit=None, file_picker=ask_idea_file,
             measurer=None, pilot_clock=None):
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
    chain_sync = {"sync": None, "notice": "", "error": "", "checking": False, "cockpit": None}
    # 1.14 — the commit this server's code comes from: agent-chain's HEAD when
    # it started. « Mettre à jour le cockpit » going, and the last restart
    # that failed.
    started = gitref.head(CHAIN_ROOT)
    updating = {"going": False, "restarting": False, "error": "", "home_at": None}
    # The page as this server started: a pull of agent-chain changes the file
    # on disk, never the page this server serves.
    with open(os.path.join(HERE, "static", "index.html"), "rb") as f:
        page_bytes = f.read()
    # 1.15: the phone's code page, and the service worker.
    with open(os.path.join(HERE, "static", "code.html"), "rb") as f:
        code_bytes = f.read()
    with open(os.path.join(HERE, "static", "sw.js"), "rb") as f:
        sw_bytes = f.read()
    # 1.6: a run stored with no application is given its own — main()'s
    # backfill did it already; this covers a store handed over as it is.
    if store:
        try:
            store.backfill_apps(app_resolver(state))
        except Exception as e:
            print(f"Consommation : application des anciens runs non retrouvée : {e}", flush=True)
    # 1.15 — the phone, through Tailscale (phone.py).
    ph = phone_mod.Phone(state)

    @web.middleware
    async def guard(request, handler):
        # Only this machine's browser, on this page: a foreign site cannot
        # reach the server through DNS rebinding or a cross-site request.
        # 1.15: or the phone, at the address Paramètres names, once its code
        # was given — never a request a proxy forwarded under a local Host.
        where = ph.where(request.headers, request.host)
        if where is None:
            return web.json_response({"error": "hôte refusé"}, status=403)
        if request.method == "POST":
            origin = request.headers.get("Origin")
            if origin and not ph.origin_ok(origin, where):
                return web.json_response({"error": "origine refusée"}, status=403)
            if request.content_type != "application/json":
                return web.json_response({"error": "JSON attendu"}, status=415)
        if where == "phone":
            if request.path in PHONE_LOCAL_ONLY:
                return web.json_response({"error": "sur l'ordinateur"}, status=403)
            if not ph.signed_in(request.cookies.get(phone_mod.COOKIE)) and not phone_open(request.path):
                return web.json_response({"error": "code d'accès demandé", "code": True}, status=401)
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
    # 1.16 — « État de l'ordinateur »: the last check of each family, the
    # repair going (a sign-in, an install), and the server's own restart.
    mach = machine.Machine()
    inst = installs.Installs(rn.log_dir, emit=lambda snap: broadcast("machine_session", {"session": snap}))
    restart_box = {"error": "", "tried": None, "wanted": False}
    pip_box = {"going": False, "error": "", "restart": False}
    port_box = app[PORT_KEY] = {"port": None}
    watch_box = {"task": None}
    # 1.17 — the usage measure, the thresholds, the estimate (usage.py).
    meas = measurer or usage_mod.Measurer(store, rn.log_dir, client_factory=MEASURE_CLIENT)

    def usage_payload():
        limits = _limits(store)
        th = state.usage_thresholds
        return {"limits": limits, "thresholds": th, "levels": usage_mod.levels(limits, th),
                "measure": meas.public(), "stale_after_s": usage_mod.STALE_S, "auto": MEASURE_USAGE}

    def measured(_task):
        broadcast("usage", usage_payload())

    def measure_now(why):
        """In the background; the page is told when it starts and ends."""
        going = meas.task is not None and not meas.task.done()
        t = meas.start(why)
        if not going:
            t.add_done_callback(measured)
        broadcast("usage", usage_payload())
        return t

    def measure_if_stale(why):
        if MEASURE_USAGE and not rn.going() and meas.stale():
            measure_now(why)

    def override_line(text):
        """A launch past the blocking threshold: the server's log, and
        consommation.log beside the run logs."""
        line = f"{datetime.now().isoformat(timespec='seconds')} · {text}"
        print("Consommation : " + text, flush=True)
        try:
            os.makedirs(rn.log_dir, exist_ok=True)
            with open(os.path.join(rn.log_dir, usage_mod.OVERRIDE_LOG), "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError:
            pass

    async def usage_gate(data, what, a):
        """§2 — before a launch: a measure older than usage.STALE_S
        refreshed first (one that fails leaves the latest one); a window at
        its blocking threshold refuses, unless the launch says `usage_ok` —
        « Lancer quand même », confirmed on the page, and logged."""
        if MEASURE_USAGE and meas.stale():
            try:
                await asyncio.shield(measure_now(f"avant de lancer {what}"))
            except Exception as e:
                print(f"Consommation : mesure avant lancement non aboutie ({e})", flush=True)
        lv = usage_mod.levels(_limits(store), state.usage_thresholds)
        blocked = usage_mod.blocking(lv)
        if not blocked:
            return None
        text = usage_mod.block_text(blocked)
        if data.get("usage_ok"):
            override_line(f"seuil de blocage passé outre — « Lancer quand même » : {what} dans "
                          f"« {state.name_of(a)} » — {text}")
            return None
        return web.json_response({"error": f"Seuil de blocage atteint : {text}. Rien n'a été lancé.",
                                  "usage_block": {"windows": blocked, "text": text}}, status=409)

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
        # 1.15: through the phone's address with no cookie, the code page.
        if on_phone(request) and not ph.signed_in(request.cookies.get(phone_mod.COOKIE)):
            return web.Response(body=code_bytes, content_type="text/html", charset="utf-8",
                                headers={"Cache-Control": "no-store"})
        return web.Response(body=page_bytes, content_type="text/html", charset="utf-8",
                            headers={"Cache-Control": "no-store"})

    # ------------------------------------------------- the phone (1.15)
    def on_phone(request):
        return ph.where(request.headers, request.host) == "phone"

    async def service_worker(request):
        return web.Response(body=sw_bytes, content_type="text/javascript", charset="utf-8",
                            headers={"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"})

    def phone_said(what):
        print(f"Téléphone : {what}", flush=True)

    async def phone_get(request):
        return web.json_response({**ph.public(), "here": "phone" if on_phone(request) else "local"})

    async def phone_settings(request):
        """Paramètres → « Accès depuis le téléphone », on this computer only."""
        data = await body(request)
        try:
            out = ph.configure(bool(data.get("enabled")), data.get("address") or "",
                               data.get("code") if isinstance(data.get("code"), str) else None)
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        phone_said(("accès ouvert à " + out["address"] if out["enabled"] else "accès fermé")
                   + (" ; code d'accès changé" if data.get("code") else "") + ".")
        broadcast("phone", out)
        return web.json_response(out)

    async def phone_disconnect(request):
        n = ph.disconnect()
        phone_said(f"déconnecté ({n} cookie{'s' if n > 1 else ''} révoqué{'s' if n > 1 else ''}, abonnements retirés).")
        out = ph.public()
        broadcast("phone", out)
        return web.json_response({**out, "revoked": n})

    async def phone_login(request):
        """The code page's « Entrer ». Five wrong codes in a row: fifteen
        minutes refused, and the computer's page says it."""
        if not on_phone(request):
            return web.json_response({"error": "inutile sur l'ordinateur"}, status=400)
        data = await body(request)
        token, what = ph.try_code(data.get("code") if isinstance(data.get("code"), str) else "")
        if what == "ok":
            phone_said("code d'accès accepté, cookie donné.")
            resp = web.json_response({"ok": True})
            resp.set_cookie(phone_mod.COOKIE, token, max_age=phone_mod.COOKIE_AGE, path="/",
                            secure=True, httponly=True, samesite="Lax")
            broadcast("phone", ph.public())
            return resp
        pub = ph.public()
        if what in ("verrouillé", "bloqué"):
            if what == "verrouillé":
                phone_said(f"code d'accès faux {phone_mod.MAX_FAILS} fois de suite — refusé jusqu'à {pub['locked_until']}.")
                broadcast("phone", pub)
            return web.json_response({"error": f"trop de codes faux : réessayez après {pub['locked_until'][11:16]}",
                                      "locked_until": pub["locked_until"]}, status=429)
        left = phone_mod.MAX_FAILS - ph.fails
        return web.json_response({"error": f"code faux — encore {left} essai{'s' if left > 1 else ''} avant "
                                           f"{phone_mod.LOCK_SECONDS // 60} minutes de blocage"}, status=403)

    async def push_subscribe(request):
        data = await body(request)
        try:
            ph.subscribe(data.get("subscription"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        phone_said("notifications activées sur un téléphone.")
        out = ph.public()
        broadcast("phone", out)
        return web.json_response(out)

    async def push_unsubscribe(request):
        data = await body(request)
        n = ph.unsubscribe(data.get("endpoint") or "")
        out = ph.public()
        broadcast("phone", out)
        return web.json_response({**out, "removed": n})

    async def push_status(request):
        data = await body(request)
        return web.json_response({"subscribed": ph.subscribed(data.get("endpoint") or "")})

    # Web Push: each subscription, at once; a subscription its service says
    # is gone (404, 410) is removed.
    async def push_to(subs, message):
        if not subs:
            return 0
        vapid, subject = ph.vapid(), ph.address or "mailto:cockpit@localhost"

        async def one(session, sub):
            try:
                status = await webpush.send(session, sub, message, vapid, subject)
            except Exception as e:
                phone_said(f"notification non envoyée — {type(e).__name__}: {e}")
                return 0
            if status in (404, 410):
                ph.unsubscribe(sub["endpoint"])
                phone_said(f"abonnement disparu ({status}), retiré.")
                broadcast("phone", ph.public())
                return 0
            if status >= 400:
                phone_said(f"notification refusée par son service ({status}).")
                return 0
            return 1
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=PUSH_TIMEOUT)) as session:
            return sum(await asyncio.gather(*(one(session, s) for s in subs)))

    def entries_of(a, w):
        """What « À répondre » holds for the run's feature: {id: (kind, file)}."""
        try:
            qs, _, bs, _, redec, _ = collect_forms(a, w, rn)
        except Exception:
            return {}
        out = {e.id: ("question", e.rel) for e in qs}
        out.update({getattr(e, "id", e.rel): ("blocage", e.rel) for e in bs + ([redec] if redec else [])})
        return out

    push_box = {"task": None, "before": {}}

    def push_message(ev, kind, title, text, screen):
        d = ev.get("data") or {}
        return {"kind": kind, "title": title, "body": text, "app": ev.get("app") or "",
                "work": d.get("work") or (rn.current(ev["app"]).work if ev.get("app") and rn.current(ev["app"]) else ""),
                "screen": screen, "tag": f"cockpit-{kind}-{d.get('id') or ev.get('run') or ev.get('seq')}"}

    async def push_event(ev):
        """The three moments a push goes: a permission waits; a run ends —
        done, stopped or failed —, with the questions or blocking files it
        left for her when it left some."""
        kind, d, a = ev["type"], ev.get("data") or {}, ev.get("app")
        loop = asyncio.get_running_loop()
        if kind == "run_started":
            # Read before the run's task takes its first step — a few files,
            # here on the loop: what it leaves is what was not there yet.
            push_box["before"][ev["run"]] = entries_of(a, d.get("work") or "")
            return
        if kind == "pilot_push":
            subs = ph.subscriptions()
            if not subs:
                return
            msg = {"kind": "pilote", "title": d.get("title") or "Pilote automatique", "body": d.get("body") or "",
                   "app": a or "", "work": (pilot.p or {}).get("feature") or "", "screen": "dashboard",
                   "tag": f"cockpit-pilote-{d.get('event')}-{ev.get('seq')}"}
            sent = await push_to(subs, msg)
            print(f"Téléphone : notification « {msg['title']} » — {sent}/{len(subs)} envoyée{'s' if sent > 1 else ''}.",
                  flush=True)
            return
        if kind not in ("permission", "run_ended"):
            return
        # 1.18: a programme's run says nothing at its end — the programme
        # says when it stops, and why.
        if kind == "run_ended" and d.get("programme"):
            push_box["before"].pop(ev["run"], None)
            return
        before = push_box["before"].pop(ev["run"], None) if kind == "run_ended" else None
        subs = ph.subscriptions()
        if not subs:
            return
        name = state.name_of(a) if a else "Cockpit"
        if kind == "permission":
            msg = push_message(ev, "autorisation", f"{name} — une autorisation attend",
                               f"{d.get('tool')} — demandé par {d.get('agent') or 'orchestrateur'}. "
                               "Le run attend votre réponse.", "run")
        else:
            after = await loop.run_in_executor(None, entries_of, a, d.get("work") or "")
            fresh = [v for k, v in after.items() if before is not None and k not in before]
            n = d.get("next") or {"kind": "unknown"}
            if fresh:
                nq = sum(1 for k, _ in fresh if k == "question")
                nb = len(fresh) - nq
                files = list(dict.fromkeys(rel for _, rel in fresh))
                what = " et ".join(x for x in (
                    f"{nq} question{'s' if nq > 1 else ''}" if nq else "",
                    f"{nb} blocage{'s' if nb > 1 else ''}" if nb else "") if x)
                msg = push_message(ev, "reponse", f"{name} — " + (f"{len(fresh)} réponses vous attendent"
                                                                   if len(fresh) > 1 else "une réponse vous attend"),
                                   f"{d.get('prompt')} — {d.get('outcome')}. {what} : {', '.join(files[:3])}"
                                   + (" …" if len(files) > 3 else ""), "answer")
            elif d.get("outcome") == "erreur":
                msg = push_message(ev, "erreur", f"{name} — {d.get('prompt')} s'est arrêté sur une erreur",
                                   d.get("error") or "Erreur", "run")
            else:
                msg = push_message(ev, "fin", f"{name} — {d.get('prompt')} — {d.get('outcome')}",
                                   "Le relais ne finit pas par une ligne Next:." if n.get("kind") == "unknown"
                                   else "Ensuite : " + (n.get("french") or n.get("raw") or ""), "run")
        sent = await push_to(subs, msg)
        print(f"Téléphone : notification « {msg['title']} » — {sent}/{len(subs)} envoyée{'s' if sent > 1 else ''}.",
              flush=True)

    async def push_watch():
        q = rn.watch()
        try:
            while True:
                ev = await q.get()
                try:
                    await push_event(ev)
                except Exception as e:      # said, never raised into the loop
                    phone_said(f"notification non préparée — {type(e).__name__}: {e}")
        finally:
            rn.unwatch(q)

    async def push_cleanup(_app):
        # 1.18: a programme scheduled survives the cockpit's stop — kept in
        # config.json; one running is summed up as interrupted.
        if pilot.task and not pilot.task.done():
            keep = dict(pilot.p) if pilot.p and pilot.p["status"] == pilot_mod.PROGRAMME else None
            pilot.task.cancel()
            await asyncio.gather(pilot.task, return_exceptions=True)
            if keep:
                state.set_pilot_active(keep)
        for t in (push_box["task"], watch_box["task"]):
            if t and not t.done():
                t.cancel()
                await asyncio.gather(t, return_exceptions=True)
        s = inst.going()
        if s:
            s.cancel()

    async def push_test(request):
        """« Essayer », on the phone: one push to this subscription."""
        data = await body(request)
        sub = next((s for s in ph.subscriptions() if s["endpoint"] == data.get("endpoint")), None)
        if not sub:
            return web.json_response({"error": "ce téléphone n'est pas abonné"}, status=404)
        sent = await push_to([sub], {"kind": "essai", "title": "Cockpit", "body": "Les notifications arrivent.",
                                     "screen": "settings", "tag": "cockpit-essai"})
        return web.json_response({"sent": sent})

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

    def is_chain(folder):
        return bool(folder) and sync_mod.Book.key(folder) == sync_mod.Book.key(CHAIN_ROOT)

    def cockpit_status(st=None):
        """1.14 — where the running cockpit stands: the commit it runs, agent-
        chain's clone, GitHub; the commits it does not run yet."""
        st = st if st is not None else (book.peek(CHAIN_ROOT) or chain_sync.get("sync"))
        try:
            out = selfupdate.status(CHAIN_ROOT, started, st, gitref.head(CHAIN_ROOT))
        except Exception as e:          # said, never raised
            out = {"state": selfupdate.UP_TO_DATE, "subjects": [], "count": 0, "error_state": str(e)}
        out.update(version=VERSION, pid=os.getpid(), going=updating["going"], restarting=updating["restarting"],
                   error=updating["error"])
        return out

    def announce(folder, st, run_id=None):
        """The new state of a clone, to every page — only when it changed,
        or for a run's end panel. 1.14: agent-chain's own carries the
        cockpit's state with it."""
        k = sync_mod.Book.key(folder)
        seen = (st or {}).get("state"), (st or {}).get("ahead"), (st or {}).get("behind"), (st or {}).get("uncommitted")
        extra = {}
        if is_chain(folder):
            if st is not None:
                chain_sync["sync"] = st
            c = chain_sync["cockpit"] = cockpit_status(st)
            seen += (c["state"], c.get("head"), c["count"], chain_sync["notice"], chain_sync["error"])
            extra.update(cockpit=c, notice=chain_sync["notice"], error=chain_sync["error"])
        if run_id is None and (told.get(k) == seen or (k not in told and seen[0] is None)):
            return
        told[k] = seen
        broadcast("sync", {"app": folder, "sync": st, "run": run_id, **extra})

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
               "limits": _limits(store), "now": datetime.now().isoformat(timespec="seconds"),
               # 1.17: the thresholds, each window's level, the last measure.
               "usage": usage_payload(),
               # 1.18: the programme going, if any, and the last one's summary.
               **pilot_light()}
        out["ignored"] = state.ignored
        out["creating"] = making["current"].path if making["current"] else None
        # 1.12: where the open application's clone stands against GitHub —
        # the last known state; agent-chain's own, with its notice.
        out["sync"] = book.peek(state.app_folder) if state.app_folder else None
        out["chain_sync"] = chain_sync
        out["chain_root"] = CHAIN_ROOT
        # 1.15: the access from the phone — never its code nor a cookie.
        out["phone"] = ph.public()
        # 1.16: « État de l'ordinateur » — its summary, for the badge.
        out["machine_summary"] = mach.report()["summary"]
        out["machine_at"] = mach.at
        out["install_mode"] = state.install_mode
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
                # 1.17 §3: what each command will cost, from its past runs.
                "estimates": usage_mod.estimates(store.path if store else None, a),
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
        # 1.14: the home screen opening — agent-chain's clone fetched again,
        # in the background: « Nouvelle version du cockpit disponible ».
        if (SYNC_CHAIN_ON_HOME and not chain_sync["checking"] and not updating["going"]
                and (updating["home_at"] is None or loop.time() - updating["home_at"] > CHAIN_HOME_EVERY)):
            updating["home_at"] = loop.time()
            refresh_later(CHAIN_ROOT)
        # 1.17: a measure older than 15 minutes, taken again — in the background.
        measure_if_stale("à l'ouverture de l'écran d'accueil")
        # 1.12: one application's fetch never waits for another's.
        rows = await asyncio.gather(*(loop.run_in_executor(None, app_row, x) for x in state.apps()))
        return web.json_response({"apps": list(rows), "busy": busy_payload(), "bulk_going": bulk["going"],
                                  "report": bulk["report"], "chain_sync": chain_sync,
                                  "machine_summary": mach.report()["summary"], "usage": usage_payload()})

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
        refused = await machine_block(machine.COMMIT)
        if refused:
            return refused
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
        refused, synced = await launch_checks(a, cmd, args, data)
        if refused:
            return refused
        try:
            r = await rn.start(a, w, feature_of(w), cmd, args)
        except runner_mod.Busy as e:
            b = busy_payload()
            return web.json_response({"error": busy_text(b) if b else str(e), "busy": b}, status=409)
        return web.json_response({"run": r.snapshot(), "sync": synced})

    async def launch_checks(a, cmd, args, data):
        """What refuses a launch, in this order — a click's and a
        programme's alike (1.18): (refusal response or None, the sync's
        result). A programme passes no `usage_ok` and no `chain_ok`."""
        if bulk["going"]:
            return web.json_response({"error": "« Tout mettre à jour » installe la chaîne : lancer après"}, status=409), None
        if updating["going"]:
            return web.json_response({"error": "le cockpit se met à jour : lancer après son redémarrage"}, status=409), None
        # One run at a time, whatever the application (1.6): said with where it goes.
        busy = busy_payload()
        if busy:
            return web.json_response({"error": busy_text(busy), "busy": busy}, status=409), None
        # A deploy building in this application (1.8): its build and the run's
        # merge would race.
        if dep.going_in(a):
            return web.json_response({"error": "un déploiement construit dans cette application : lancer après sa fin"},
                                     status=409), None
        if inst.going():
            return web.json_response({"error": f"« {inst.going().title} » est en cours : lancer après sa fin"},
                                     status=409), None
        # 1.16 §2: what blocks a launch — Claude Code, its login, git's
        # identity —, checked again now; « Bâtir », Java and the Android tools.
        refused = await machine_block(machine.LAUNCH, a) or (
            await machine_block(machine.BATIR, a) if cmd == "batir" else None)
        if refused:
            return refused, None
        # 1.17 §2: the usage, measured again when old; its blocking threshold.
        refused = await usage_gate(data, f"/{cmd} {args}".rstrip(), a)
        if refused:
            return refused, None
        # 1.12 §2: GitHub first — what the other computer pushed is pulled
        # before anything reads the files, the chain's version included.
        refused, synced = await synced_first(a)
        if refused:
            return refused, synced
        # A chain not « à jour » (§20): the launch asks first.
        ch = chain_state(a)
        if ch.get("state") != chain_mod.UP_TO_DATE and not data.get("chain_ok"):
            return web.json_response({"error": ch["summary"], "chain": ch, "sync": synced}, status=409), synced
        return None, synced

    # ---------------------------------------- pilote automatique (1.18)
    class PilotHost:
        """What the programme asks of the server (autopilot.py)."""

        def decide(self, a, feature):
            return where(state, rn, a, feature)

        def busy(self):
            x = rn.going()
            return x.prompt if x and not x.programme else None

        async def wait_idle(self):
            x = rn.going()
            if x and x.task:
                await asyncio.gather(asyncio.shield(x.task), return_exceptions=True)

        async def refresh_usage(self, force):
            if MEASURE_USAGE and (force or meas.stale()):
                try:
                    await asyncio.shield(measure_now("pilote automatique"))
                except Exception as e:
                    print(f"Pilote automatique : mesure non aboutie ({e})", flush=True)

        def levels(self):
            return usage_mod.levels(_limits(store), state.usage_thresholds)

        def thresholds(self):
            return state.usage_thresholds

        def estimate(self, cmd):
            p = pilot.p or {}
            return usage_mod.estimates(store.path if store else None, p.get("app")).get("/" + cmd)

        async def launch(self, a, feature, cmd, args, pid):
            if cmd not in {c["name"] for c in list_commands(a)}:
                return None, (pilot_mod.CHAIN, f"/{cmd} n'est pas une commande de l'application.")
            refused, _ = await launch_checks(a, cmd, args, {})
            if refused:
                return None, refusal_kind(refused)
            try:
                r = await rn.start(a, feature, feature, cmd, args, mode="auto", programme=pid)
            except runner_mod.Busy as e:
                return None, (pilot_mod.BUSY, str(e))
            return r, None

        async def wait_run(self, r):
            if r.task:
                await asyncio.gather(asyncio.shield(r.task), return_exceptions=True)
            return r.snapshot()

        async def stop_run_now(self, a):
            try:
                await rn.stop_now(a)
            except runner_mod.NotRunning:
                pass

        def write_stop(self, a):
            return rn.stop_at_next_lot(a)

        def changed(self, public):
            broadcast("pilot", pilot_light())

        def push(self, event, title, text):
            broadcast("pilot_push", {"event": event, "title": title, "body": text,
                                     "app": (pilot.p or {}).get("app") or state.app_folder})

        def record(self, summary):
            if store:
                store.record_programme(summary)

        def spent(self, pid):
            return store.spent(pid) if store else {}

        def save(self, record):
            state.set_pilot_active(record)

    def refusal_kind(resp):
        try:
            b = json.loads(resp.text)
        except (TypeError, ValueError):
            b = {}
        text = b.get("error") or "lancement refusé"
        if b.get("usage_block"):
            return pilot_mod.USAGE, text + " Un programme ne passe jamais outre."
        if b.get("sync_refused"):
            return pilot_mod.GITHUB, "GitHub : " + text
        if b.get("machine"):
            return pilot_mod.MACHINE, "État de l'ordinateur : " + text
        if b.get("chain"):
            return pilot_mod.CHAIN, text + " — un programme ne lance rien sur une chaîne pas à jour."
        return pilot_mod.BUSY, text[:1].upper() + text[1:] + "."

    pilot = pilot_mod.Pilot(PilotHost(), clock=pilot_clock or PILOT_CLOCK)

    def pilot_light():
        """What the page shows of the automatic mode: the programme, the last
        summary, the ready settings and the saved programmes."""
        last = pilot.last
        if last is None and store:
            try:
                got = store.programmes(1)
                last = got[0] if got else None
            except Exception:
                last = None
        return {"pilot": pilot.public(), "pilot_last": last, "pilot_presets": pilot_mod.PRESETS,
                "pilot_saved": [{**x, "text": pilot_mod.spec_text(x["spec"])} for x in state.programmes()]}

    def pilot_payload():
        a, w = pair()
        light = pilot_light()
        last = light["pilot_last"]
        steps = None
        if a:
            try:
                sc = scan_of(a, feature_of(w))
                steps = {"main": [{"id": x["id"], "name": x["name"], "command": x.get("command")} for x in sc["main"]],
                         "correction": next(({"name": c["name"], "steps": [{"id": x["id"], "name": x["name"]}
                                                                            for x in c["steps"]]}
                                             for c in sc["corrections"] if c["highest"]), None)}
            except Exception:
                steps = None
        return {**light, "last": last, "steps": steps}

    async def pilot_get(request):
        return web.json_response(pilot_payload())

    async def pilot_start(request):
        """« Lancer le programme »: a ready setting, a saved one or the
        full form — on the application and the feature open."""
        a, w = need_pair()
        data = await body(request)
        spec = data.get("spec")
        if data.get("preset"):
            spec = next((x["spec"] for x in pilot_mod.PRESETS if x["id"] == data["preset"]), None)
            spec = {**spec, "name": next(x["name"] for x in pilot_mod.PRESETS if x["id"] == data["preset"])} if spec else None
        elif data.get("saved"):
            spec = next((x["spec"] for x in state.programmes() if x["name"] == data["saved"]), None)
        if not isinstance(spec, dict):
            return web.json_response({"error": "aucun programme"}, status=400)
        try:
            clean = pilot_mod.clean_spec(spec)
            if data.get("save"):
                if not clean["name"]:
                    return web.json_response({"error": "un nom, pour l'enregistrer"}, status=400)
                state.save_programme(clean["name"], clean)
            out = pilot.create(clean, a, feature_of(w), state.name_of(a))
        except (ValueError, pilot_mod.Refused) as e:
            return web.json_response({"error": str(e)}, status=409 if isinstance(e, pilot_mod.Refused) else 400)
        return web.json_response({**pilot_payload(), "created": out})

    async def pilot_stop(request):
        data = await body(request)
        try:
            await pilot.stop("maintenant" if data.get("how") == "maintenant" else "apres")
        except pilot_mod.Refused as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response(pilot_payload())

    async def pilot_save(request):
        data = await body(request)
        try:
            clean = pilot_mod.clean_spec(data.get("spec"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        if not clean["name"]:
            return web.json_response({"error": "un nom, pour l'enregistrer"}, status=400)
        state.save_programme(clean["name"], clean)
        return web.json_response(pilot_payload())

    async def pilot_forget(request):
        data = await body(request)
        state.forget_programme(str(data.get("name") or ""))
        return web.json_response(pilot_payload())

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
        refused = await machine_block(machine.CHAIN_INSTALL, a)
        if refused:
            return refused
        refused, synced = await synced_first(a)
        if refused:
            return refused
        # 1.16: never while GitHub cannot be reached — how the duplicate of
        # 9 October happened.
        if (synced.get("sync") or {}).get("state") == sync_mod.OFFLINE:
            return web.json_response({"error": OFFLINE_INSTALL + " — " + synced["sync"]["summary"],
                                      "sync": synced["sync"]}, status=409)
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
        refused = await machine_block(machine.CHAIN_INSTALL)
        if refused:
            return refused
        bulk["going"] = True
        loop = asyncio.get_running_loop()

        def prepare(folder):
            """1.12 §2, in each application before its install. 1.16: GitHub
            unreachable, nothing installed there."""
            res = sync_mod.before_launch(book, folder)
            for d in res["done"]:
                sync_said(folder, "avant d'installer", d)
            announce(folder, res["sync"])
            if res["ok"] and (res.get("sync") or {}).get("state") == sync_mod.OFFLINE:
                return OFFLINE_INSTALL
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

    async def usage_get(request):
        return web.json_response(usage_payload())

    async def usage_thresholds(request):
        """Paramètres → Consommation: the four thresholds."""
        data = await body(request)
        try:
            state.set_usage_thresholds(data.get("thresholds"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        out = usage_payload()
        broadcast("usage", out)
        return web.json_response(out)

    async def usage_measure(request):
        """« Mesurer maintenant »: the measure, waited for."""
        if rn.going():
            return web.json_response({"error": "une commande tourne : ses propres mesures tiennent les jauges à jour"},
                                     status=409)
        await asyncio.shield(measure_now("à la demande"))
        return web.json_response(usage_payload())

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
                chain_sync.update(sync=st, notice=notice, error=error, cockpit=cockpit_status(st))
        finally:
            chain_sync["checking"] = False
        announce(CHAIN_ROOT, chain_sync["sync"])

    async def opening(_app):
        loop_box["loop"] = asyncio.get_running_loop()
        loop = loop_box["loop"]
        # 1.15: the pushes to the phone, from every run's events.
        push_box["task"] = loop.create_task(push_watch())
        # 1.12: GitHub, when the cockpit opens — agent-chain's clone, then
        # every application, in the background.
        chain_done = loop.run_in_executor(None, sync_chain) if SYNC_CHAIN_AT_START else None
        # 1.16: « État de l'ordinateur », once agent-chain's state is known;
        # and the restart, when the code on disk gets newer.
        if MACHINE_AT_START:
            async def first_check():
                if chain_done is not None:
                    await asyncio.gather(chain_done, return_exceptions=True)
                try:
                    await machine_full()
                except Exception as e:
                    print(f"État de l'ordinateur : vérification au démarrage non aboutie ({e})", flush=True)
            loop.create_task(first_check())
        if AUTO_RESTART:
            watch_box["task"] = loop.create_task(restart_watch())
        # 1.17: the usage, measured when the cockpit starts.
        if MEASURE_USAGE:
            measure_now("au démarrage du cockpit")
        # 1.18: a programme kept when the cockpit stopped.
        kept = state.pilot_active
        if kept:
            try:
                pilot.restore(kept)
            except Exception as e:
                state.set_pilot_active(None)
                print(f"Pilote automatique : programme gardé non repris ({e})", flush=True)
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
        # 1.18: the automatic mode's programmes, for the same application and feature.
        progs = []
        if store:
            try:
                progs = store.programmes(200)
            except Exception:
                progs = []
        akey = statsview.app_key(app) if app else None
        out["programmes"] = [x for x in progs if (akey is None or statsview.app_key(x.get("app")) == akey)
                             and (feature is None or x.get("feature") == feature)]
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
        data = await body(request)
        old = rn.current(a)
        refused = await usage_gate(data, f"la suite de {old.prompt}" if old and old.id else "la suite", a)
        if refused:
            return refused
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
        refused = await machine_block(machine.DEPLOY, a)
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
        refused = await machine_block(machine.COMMIT, a)
        if refused:
            return refused
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
        refused = await machine_block(machine.COMMIT, a)
        if refused:
            return refused
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
        refused = await machine_block(machine.PUSH)
        if refused:
            return refused
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
        refused = await machine_block(machine.SEND, folder)
        if refused:
            return refused
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

    async def sync_pull(request):
        """« Récupérer » (1.14): an application « en retard » — the same
        `git pull --ff-only` a launch makes first (§2), refused the same
        ways. Then its state and its chain's, computed again: the chain block
        shows what was pulled."""
        data = await body(request)
        folder = sync_target(data)
        if not folder or is_chain(folder):
            return web.json_response({"error": "aucune application"}, status=409)
        why = sync_busy(folder)
        if why:
            return web.json_response({"error": why}, status=409)
        loop = asyncio.get_running_loop()

        def go():
            with book.lock(folder):
                st = book.put(folder, sync_mod.compute(folder))
                out = {"ok": False, "error": "", "files": [], "reconcile": False, "pulled": 0}
                if st["state"] == sync_mod.BEHIND:
                    r = sync_mod.pull_ff(folder)
                    if r["ok"]:
                        out.update(ok=True, pulled=st["behind"])
                    else:
                        out.update(error=r["message"], files=r["files"])
                    st = book.put(folder, sync_mod.compute(folder, fetch=False))
                elif st["state"] == sync_mod.DIVERGED:
                    out.update(reconcile=True, error=sync_mod.summary(st) + " — « Réconcilier » d'abord")
                else:
                    out["error"] = f"rien à récupérer : {sync_mod.summary(st).lower()}"
                out["sync"] = st
                return out
        res = await loop.run_in_executor(None, go)
        sync_said(folder, "Récupérer", f"git pull --ff-only — {res['pulled']} commit(s) récupéré(s)" if res["ok"]
                  else res["error"])
        announce(folder, res["sync"])
        res["chain"] = await loop.run_in_executor(None, chain_state, folder)
        return web.json_response(res, status=200 if res["ok"] else 409)

    # ------------------------------------------------- the cockpit itself (1.14)
    def update_busy():
        """Why the cockpit may not update now, or None."""
        x = rn.going()
        if x:
            return (f"une commande tourne dans « {state.name_of(x.repo) or x.repo} » : {x.prompt} — le cockpit "
                    "se met à jour après sa fin")
        if bulk["going"]:
            return "« Tout mettre à jour » est en cours : le cockpit se met à jour après sa fin"
        if dep.going():
            return "un déploiement construit : le cockpit se met à jour après sa fin"
        if making["current"]:
            return f"une création est en cours ({making['current'].path}) : le cockpit se met à jour après sa fin"
        if updating["going"]:
            return "la mise à jour du cockpit est déjà en cours"
        if inst.going():
            return f"« {inst.going().title} » est en cours : le cockpit se met à jour après sa fin"
        if pilot.active():
            return (f"le pilote automatique a un programme actif ({pilot.p['status']}) : le cockpit se met à jour "
                    "après sa fin")
        return None

    async def cockpit_get(request):
        return web.json_response({"cockpit": cockpit_status(), "chain_sync": chain_sync})

    def pull_chain():
        """agent-chain's clone: fetched; « en retard », pulled — fast-forward
        only; « divergé », refused."""
        with book.lock(CHAIN_ROOT):
            st = book.put(CHAIN_ROOT, sync_mod.compute(CHAIN_ROOT))
            out = {"ok": True, "error": "", "files": [], "reconcile": False, "pulled": 0}
            if st["state"] == sync_mod.BEHIND:
                r = sync_mod.pull_ff(CHAIN_ROOT)
                if r["ok"]:
                    out["pulled"] = st["behind"]
                else:
                    out.update(ok=False, error="agent-chain — " + r["message"], files=r["files"])
                st = book.put(CHAIN_ROOT, sync_mod.compute(CHAIN_ROOT, fetch=False))
            elif st["state"] == sync_mod.DIVERGED:
                out.update(ok=False, reconcile=True,
                           error="agent-chain — " + sync_mod.summary(st) + " — « Réconcilier » d'abord")
            out["sync"] = st
            return out

    async def cockpit_update(request):
        """« Mettre à jour le cockpit » (1.14): refused while something
        goes; agent-chain pulled, fast-forward only; pip when
        requirements.txt changed; then the restart — see selfupdate.py."""
        why = update_busy()
        if why:
            return web.json_response({"error": why, "busy": True, "cockpit": cockpit_status()}, status=409)
        data = await body(request) if request.can_read_body else {}
        updating.update(going=True, error="")
        loop = asyncio.get_running_loop()
        sock = request.transport.get_extra_info("sockname") if request.transport else None
        port = sock[1] if sock else None
        steps = []

        def refuse(error, **kw):
            updating.update(going=False, restarting=False, error=error)
            print(f"Mettre à jour le cockpit — arrêté : {error}", flush=True)
            return web.json_response({"error": error, "steps": steps, "cockpit": cockpit_status(), **kw}, status=409)
        try:
            p = await loop.run_in_executor(None, pull_chain)
            announce(CHAIN_ROOT, p["sync"])
            if not p["ok"]:
                return refuse(p["error"], files=p["files"], reconcile=p["reconcile"])
            if p["pulled"]:
                n = p["pulled"]
                steps.append(f"git pull --ff-only — {n} commit{'s' if n > 1 else ''} récupéré{'s' if n > 1 else ''}")
                sync_said(CHAIN_ROOT, "Mettre à jour le cockpit", steps[-1])
            head = gitref.head(CHAIN_ROOT)
            if not head or head == started:
                if p["sync"].get("state") == sync_mod.OFFLINE:
                    return refuse("agent-chain — " + sync_mod.summary(p["sync"]))
                updating.update(going=False, error="")
                return web.json_response({"ok": True, "nothing": True, "steps": steps, "cockpit": cockpit_status(),
                                          "message": "Le cockpit est à jour : rien à récupérer."})
            # The new code is on disk; this server still runs the old one.
            chain_sync.update(notice="", error="")
            if await loop.run_in_executor(None, selfupdate.requirements_changed, CHAIN_ROOT, started, head):
                # 1.16: an install the cockpit drives — the page asks « Rapide »
                # or « Pas à pas » first (`asked`), unless Paramètres says.
                mode = None
                if data.get("asked"):
                    mode = data.get("mode") if data.get("mode") in installs.MODES else resolve_mode({})
                    if mode is None:
                        updating.update(going=False, error="")
                        d = await loop.run_in_executor(None, installs.describe_pip)
                        return web.json_response({"error": "Rapide ou Pas à pas ?", "ask": True, "describe": d,
                                                  "steps": steps, "cockpit": cockpit_status()}, status=409)
                if mode == installs.PAS_A_PAS:
                    sess = start_pip(installs.PAS_A_PAS)
                    while sess.status != "ended":
                        await asyncio.sleep(0.3)
                    if sess.outcome not in ("installé", "rien à installer"):
                        return refuse(sess.message or sess.outcome, step="pip")
                    steps.append("pip, pas à pas — " + (", ".join(sess.installed) or sess.outcome)
                                 + " ; licences acceptées : " + (", ".join(l["name"] for l in sess.licences) or "aucune"))
                else:
                    if mode == installs.RAPIDE:
                        plan = await loop.run_in_executor(None, installs.describe_pip)
                        if plan.get("what"):
                            steps.append("Rapide — installe : " + ", ".join(plan["what"]) + " — licences acceptées : "
                                         + ", ".join(plan["licences"]))
                    r = await loop.run_in_executor(None, selfupdate.pip_install, CHAIN_ROOT)
                    print(f"Mettre à jour le cockpit — {' '.join(r['command'])} : {'fait' if r['ok'] else r['message']}",
                          flush=True)
                    if not r["ok"]:
                        return refuse(r["message"], step="pip")
                    steps.append("pip install --user -r tools/cockpit/requirements.txt — fait")
            if not port:
                return refuse("le port de ce serveur est inconnu : redémarrer le cockpit à la main")
            ok, got = await restart_server(port, "Mettre à jour le cockpit")
            if not ok:
                return refuse(got, step="restart")
            steps.append(f"nouveau serveur prêt — cockpit {got.get('version')}, pid {got.get('pid')}")
            return web.json_response({"ok": True, "restarting": True, "steps": steps, "old_pid": os.getpid(),
                                      "new_pid": got.get("pid"), "version": got.get("version")})
        except Exception as e:
            return refuse(f"mise à jour interrompue : {e}")

    async def restart_server(port, why, env=None):
        """1.14's restart: a new server on a trial port first; once it
        answers there, this one exits and lets it take the port. (True, its
        ping) or (False, why not) — then this one keeps running. 1.16: with
        `env`, the new server gets that environment — PATH as Windows has it
        now, after an install."""
        loop = asyncio.get_running_loop()
        updating["restarting"] = True
        announce(CHAIN_ROOT, book.peek(CHAIN_ROOT))
        trial = selfupdate.free_port(HOST)
        try:
            proc = SPAWN_SERVER(port, trial, list(LAUNCH_ARGS), rn.log_dir, **({"env": env} if env else {}))
        except OSError as e:
            updating["restarting"] = False
            return False, f"le nouveau serveur n'a pas pu démarrer : {e}"
        print(f"{why} — nouveau serveur lancé (pid {getattr(proc, 'pid', '?')}), port d'essai {trial}.", flush=True)
        t0 = loop.time()
        got = await loop.run_in_executor(None, selfupdate.wait_answer, proc, trial, os.getpid(),
                                         selfupdate.RESTART_WAIT)
        if not got:
            await loop.run_in_executor(None, selfupdate.give_up, proc)
            updating["restarting"] = False
            return False, selfupdate.why_not(proc, loop.time() - t0, rn.log_dir, trial)
        # The new server answers: every page waits for it, then reloads.
        broadcast("cockpit_restarting", {"why": why, "pid": os.getpid(), "version": got.get("version")})
        print(f"{why} — le nouveau serveur répond (pid {got.get('pid')}) : celui-ci s'arrête et lui laisse le port.",
              flush=True)
        if on_quit:
            loop.call_later(0.3, on_quit)
        return True, got

    def restart_busy():
        """Why the server may not restart now: a run, an install, a deploy,
        a creation, an update — or a repair of this computer going."""
        why = update_busy()
        return why.replace("le cockpit se met à jour après sa fin", "le cockpit redémarre après sa fin") if why else None

    async def cockpit_restart(request):
        """« Redémarrer le cockpit » (1.16), and lancer.bat when the server
        that answers is older than the code on disk: 1.14's restart, without
        pulling anything."""
        why = restart_busy()
        if why:
            return web.json_response({"error": why, "busy": True}, status=409)
        sock = request.transport.get_extra_info("sockname") if request.transport else None
        port = port_box["port"] or (sock[1] if sock else None)
        if not port:
            return web.json_response({"error": "le port de ce serveur est inconnu"}, status=409)
        ok, got = await restart_server(port, "Redémarrer le cockpit", env=installs.fresh_env())
        if not ok:
            restart_box["error"] = got
            await machine_refresh(["cockpit"])
            return web.json_response({"error": got}, status=409)
        return web.json_response({"ok": True, "restarting": True, "old_pid": os.getpid(), "new_pid": got.get("pid"),
                                  "version": got.get("version")})

    # ------------------------------------------- « État de l'ordinateur » (1.16)
    def machine_ctx(heavy=True):
        """What the checks are given: what this server already knows. Light
        (`heavy` False) before an action: no family it checks reads each
        application's chain or build report."""
        apps = []
        for x in state.apps():
            f = x["folder"]
            row = {"name": x["name"], "folder": f, "sync": book.peek(f), "chain": None, "build": None,
                   "conventions": None}
            if heavy and os.path.isdir(f):
                try:
                    row["chain"] = chain_state(f)
                except Exception as e:
                    row["chain"] = {"state": None, "summary": f"état de la chaîne inconnu — {e}"}
                try:
                    row["build"] = scan_mod.batir_report(f)
                    row["conventions"] = conventions_commit(f)
                except Exception:
                    pass
            apps.append(row)
        x = rn.going()
        why = restart_busy()
        return {"chain_root": CHAIN_ROOT, "started": started, "head": gitref.head(CHAIN_ROOT), "apps": apps,
                "chain_sync": chain_sync.get("sync") or book.peek(CHAIN_ROOT), "diagnostic": state.diagnostic(),
                "app_name": state.app_name, "restart": restart_box, "pip": pip_box,
                "busy": f"la fin de {x.prompt}" if x else ("la fin de ce qui est en cours" if why else None)}

    def machine_payload():
        return {"machine": mach.report(), "session": inst.public(), "install_mode": state.install_mode}

    told_machine = {"sig": None}

    def machine_told():
        """To every page — when what needs her changed: the badge's
        summary, the items that block or need her. All in order from the
        start, nothing is said: the page reads it when it opens."""
        p = machine_payload()
        sm = p["machine"]["summary"]
        sig = (sm["level"], tuple((x["id"], x["status"], x["detail"]) for x in p["machine"]["items"]
                                  if x["status"] in machine.NEEDS))
        before, told_machine["sig"] = told_machine["sig"], sig
        if sig == before or (before is None and sm["level"] == "ok"):
            return
        broadcast("machine", p)

    async def machine_full():
        loop = asyncio.get_running_loop()
        ctx = await loop.run_in_executor(None, machine_ctx)
        await loop.run_in_executor(None, mach.full, ctx)
        machine_told()
        await machine_after()
        return mach.report()

    async def machine_refresh(families):
        loop = asyncio.get_running_loop()
        ctx = await loop.run_in_executor(None, machine_ctx, "apps" in families)
        await loop.run_in_executor(None, mach.refresh, families, ctx)
        machine_told()

    async def machine_block(action, app_folder=None):
        """§2 — before an action, what blocks it, checked again: None, or the
        refusal, with what to repair."""
        loop = asyncio.get_running_loop()
        ctx = await loop.run_in_executor(None, machine_ctx, False)
        blockers = await loop.run_in_executor(None, mach.before, action, ctx, app_folder)
        machine_told()
        if not blockers:
            return None
        print(f"État de l'ordinateur — {machine.ACTION_TEXT.get(action, action)} refusé : "
              + "; ".join(f"{b['label']} ({b['detail']})" for b in blockers), flush=True)
        return web.json_response(machine.refusal(blockers), status=409)

    async def machine_after():
        """What a check finds that fixes itself: the Python dependencies,
        installed when Paramètres says « Rapide »; the restart, when the
        code on disk is newer."""
        miss = next((x for x in mach.items() if x["id"] == "python" and x["status"] == machine.WARN), None)
        if (miss and state.install_mode == installs.RAPIDE and not inst.going() and not pip_box["going"]
                and not pip_box["error"]):
            start_pip(installs.RAPIDE)
        await maybe_restart()

    def from_thread(coro_fn):
        """A coroutine of this server's loop, from a session's thread."""
        loop = loop_box["loop"]
        if loop is not None:
            asyncio.run_coroutine_threadsafe(coro_fn(), loop)

    def after_session(sess):
        if sess.kind == "pip":
            pip_box.update(going=False, error="" if sess.outcome in ("installé", "rien à installer") else sess.message,
                           restart=bool(sess.restart))
        if sess.restart:
            restart_box["wanted"] = True
        from_thread(machine_full)

    def start_pip(mode):
        pip_box.update(going=True, error="")
        return inst.start("pip", "Dépendances Python", installs.pip_install(mode), mode=mode, after=after_session)

    async def maybe_restart():
        """1.16 — the rule « fixes itself when idle »: the server older than
        the code on disk (agent-chain moved on), or an install that asked
        for it (PATH, the dependencies), and nothing going — restarted, once
        per reason."""
        if not AUTO_RESTART:
            return
        head = gitref.head(CHAIN_ROOT)
        older = bool(head and started and head != started)
        if not (older or restart_box["wanted"]) or updating["restarting"] or restart_busy():
            return
        token = (head, restart_box["wanted"])
        port = port_box["port"]
        if restart_box["tried"] == token or not port:
            return
        restart_box["tried"] = token
        ok, got = await restart_server(port, "Redémarrage de lui-même — " + (
            "le code sur le disque est plus récent" if older else "une installation l'a demandé"),
            env=installs.fresh_env())
        if not ok:
            restart_box["error"] = got
            await machine_refresh(["cockpit"])

    async def restart_watch():
        while True:
            await asyncio.sleep(RESTART_POLL)
            try:
                await maybe_restart()
            except Exception as e:      # said, never raised into the loop
                print(f"Redémarrage de lui-même non abouti : {e}", flush=True)

    async def machine_get(request):
        return web.json_response(machine_payload())

    async def machine_check(request):
        """When the screen opens, and « Vérifier maintenant »: every family —
        the button (`diagnostic`) runs the open application's diagnostic
        with them; the screen opening keeps the one stored."""
        data = await body(request)
        a = state.app_folder
        if data.get("diagnostic") and a and os.path.isdir(a) and not diag_running(a):
            try:
                await diagnose(a)
            except Exception as e:
                print(f"Diagnostic non abouti ({a}) : {e}", flush=True)
        await machine_full()
        return web.json_response(machine_payload())

    def resolve_mode(data):
        m = data.get("mode") or state.install_mode
        return m if m in installs.MODES else None

    async def machine_describe(request):
        """What an install would do — shown before its question: what it
        installs, the licences « Rapide » would accept, what no mode skips."""
        data = await body(request)
        kind = data.get("kind")
        loop = asyncio.get_running_loop()
        if kind == "pip":
            d = await loop.run_in_executor(None, installs.describe_pip)
        elif kind == "claude_code":
            cli, _ = machine.SDK_CLI()
            d = {"what": ["Claude Code — " + ("claude update" if cli else "l'installateur officiel d'Anthropic")],
                 "licences": [], "unskippable": [installs.BROWSER_SIGNIN + " ensuite, si Claude Code n'est pas connecté"]}
        elif kind == "tool":
            d = installs.describe_tool(data.get("tool"))
        else:
            return web.json_response({"error": f"rien à décrire : {kind}"}, status=400)
        if d.get("error"):
            return web.json_response(d, status=409)
        return web.json_response({**d, "kind": kind, "tool": data.get("tool"), "install_mode": state.install_mode})

    def repair_busy():
        x = rn.going()
        if x:
            return f"une commande tourne : {x.prompt} — après sa fin"
        if inst.going():
            return f"« {inst.going().title} » est en cours"
        if updating["going"] or updating["restarting"]:
            return "le cockpit se met à jour"
        return None

    def tool_verify(tool):
        def verify():
            ctx = machine_ctx(False)
            fam = ["identity", "github"] if tool == "git" else ["android"]
            mach.refresh(fam, ctx)
            want = {"git", "gcm"} if tool == "git" else {"android_sdk", "sdkmanager"} if tool == "android_sdk" else {tool}
            hit = [x for x in mach.items() if x["id"] in want]
            bad = [x for x in hit if x["status"] not in (machine.OK, machine.FIXED)]
            return (bool(hit) and not bad), ("; ".join(f"{x['label']} : {x['detail']}" for x in hit) or "rien à vérifier")
        return verify

    async def machine_repair(request):
        """One click, one repair (§3)."""
        data = await body(request)
        rid = data.get("id")
        args = data.get("args") or {}
        loop = asyncio.get_running_loop()
        if rid == "longpaths":
            folder = args.get("folder") or ""
            known = [x["folder"] for x in state.apps()] + [CHAIN_ROOT]
            if not any(machine.key(folder) == machine.key(k) for k in known):
                return web.json_response({"error": "ce dossier n'est pas dans la liste"}, status=400)
            try:
                await loop.run_in_executor(None, sync_mod.set_long_paths, folder)
            except sync_mod.SyncError as e:
                return web.json_response({"error": str(e)}, status=409)
            await machine_refresh(["longpaths"])
            return web.json_response({"ok": True, **machine_payload()})
        if rid == "identity":
            name, mail = (args.get("name") or "").strip(), (args.get("email") or "").strip()
            if not name or not mail or "@" not in mail or "\n" in name + mail:
                return web.json_response({"error": "un nom et une adresse e-mail"}, status=400)
            for k, v in (("user.name", name), ("user.email", mail)):
                r = await loop.run_in_executor(None, lambda k=k, v=v: sync_mod.git(CHAIN_ROOT, "config", "--global", k, v))
                if not r.ok:
                    return web.json_response({"error": f"git config --global {k} : {r.text}"}, status=409)
            print(f"État de l'ordinateur — identité git réglée : {name} <{mail}>", flush=True)
            await machine_refresh(["identity"])
            return web.json_response({"ok": True, **machine_payload()})
        if rid == "restart":
            return await cockpit_restart(request)
        busy = repair_busy()
        if busy:
            return web.json_response({"error": f"Pas maintenant : {busy}.", "busy": True}, status=409)
        cli, _ = machine.SDK_CLI()
        if rid == "claude_login":
            if not cli:
                return web.json_response({"error": "Claude Code d'abord : il n'est pas sur cet ordinateur"}, status=409)

            def verify():
                c, t, _ = machine._try([cli, "auth", "status"], env=machine.claude_env())
                return c == 0, ("connecté" if c == 0 else f"pas connecté (claude auth status : code {c})")
            inst.start("claude_login", "Se connecter à Claude",
                       installs.claude_login(cli, machine.claude_env(), verify), after=after_session)
            return web.json_response({"ok": True, **machine_payload()})
        if rid == "github_login":
            def verify():
                c, t, _ = machine.git_run(CHAIN_ROOT, "push", "--dry-run", "--porcelain", timeout=machine.PUSH_TIMEOUT)
                ok = c == 0 or bool(sync_mod._REJECTED.search(t or ""))
                return ok, ("GitHub accepte les identifiants de cet ordinateur" if ok else sync_mod.explain(t))
            inst.start("github_login", "Se connecter à GitHub", installs.github_login(verify), after=after_session)
            return web.json_response({"ok": True, **machine_payload()})
        if rid not in ("pip", "claude_code", "tool"):
            return web.json_response({"error": f"réparation inconnue : {rid}"}, status=400)
        tool = args.get("tool")
        if rid == "tool":
            if tool not in installs.TOOLS:
                return web.json_response({"error": f"outil inconnu : {tool}"}, status=400)
            # Order enforced: no Claude login, no Claude install.
            refused = await machine_block(machine.TOOL_INSTALL)
            if refused:
                return refused
        mode = resolve_mode(data)
        if mode is None:
            return web.json_response({"error": "Rapide ou Pas à pas ?", "ask": True}, status=409)
        if rid == "pip":
            start_pip(mode)
        elif rid == "claude_code":
            def verify():
                c2, _m = machine.SDK_CLI()
                if not c2:
                    return False, "Claude Code reste introuvable"
                c, t, _ = machine._try([c2, "--version"])
                return c == 0, (machine.first_line(t) if c == 0 else f"{c2} ne répond pas")
            inst.start("claude_code", "Claude Code", installs.claude_code(mode, cli, verify), mode=mode,
                       after=after_session)
        else:
            t = installs.TOOLS[tool]
            stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            work = os.path.join(rn.log_dir, "installations", tool)
            log = os.path.join(rn.log_dir, f"{stamp}-installer-{tool}.jsonl")
            inst.start("tool", f"Installer {t['label']}", installs.with_claude(tool, mode, work, log, tool_verify(tool)),
                       mode=mode, target=tool, after=after_session)
        return web.json_response({"ok": True, **machine_payload()})

    async def session_answer(request):
        data = await body(request)
        s = inst.going()
        if not s or not s.answer(data.get("card"), bool(data.get("accept"))):
            return web.json_response({"error": "cette carte n'attend plus"}, status=409)
        return web.json_response({"ok": True})

    async def session_code(request):
        data = await body(request)
        s = inst.going()
        code = (data.get("code") or "").strip()
        if not s or s.kind != "claude_login" or not code or "\n" in code:
            return web.json_response({"error": "aucune connexion n'attend de code"}, status=409)
        ok = await asyncio.get_running_loop().run_in_executor(None, installs.send_code, s, code)
        return web.json_response({"ok": ok}, status=200 if ok else 409)

    async def session_cancel(request):
        s = inst.going()
        if not s:
            return web.json_response({"error": "rien n'est en cours"}, status=409)
        s.cancel()
        return web.json_response({"ok": True})

    async def install_mode_set(request):
        data = await body(request)
        try:
            state.set_install_mode(data.get("mode"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"install_mode": state.install_mode})

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
        return web.json_response({"cockpit": True, "version": VERSION, "pid": os.getpid(), "started": started,
                                  "restarting": updating["restarting"], "error": updating["error"]})

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
    r.add_get("/sw.js", service_worker)
    r.add_get("/api/phone", phone_get)
    r.add_post("/api/phone/settings", phone_settings)
    r.add_post("/api/phone/disconnect", phone_disconnect)
    r.add_post("/api/phone/login", phone_login)
    r.add_post("/api/push/subscribe", push_subscribe)
    r.add_post("/api/push/unsubscribe", push_unsubscribe)
    r.add_post("/api/push/status", push_status)
    r.add_post("/api/push/test", push_test)
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
    r.add_get("/api/usage", usage_get)
    r.add_post("/api/usage/thresholds", usage_thresholds)
    r.add_post("/api/usage/measure", usage_measure)
    r.add_get("/api/pilot", pilot_get)
    r.add_post("/api/pilot/start", pilot_start)
    r.add_post("/api/pilot/stop", pilot_stop)
    r.add_post("/api/pilot/save", pilot_save)
    r.add_post("/api/pilot/forget", pilot_forget)
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
    r.add_post("/api/sync/pull", sync_pull)
    r.add_get("/api/cockpit", cockpit_get)
    r.add_post("/api/cockpit/update", cockpit_update)
    r.add_post("/api/longpaths", longpaths_set)
    r.add_post("/api/cockpit/restart", cockpit_restart)
    r.add_get("/api/machine", machine_get)
    r.add_post("/api/machine/check", machine_check)
    r.add_post("/api/machine/describe", machine_describe)
    r.add_post("/api/machine/repair", machine_repair)
    r.add_post("/api/machine/session/answer", session_answer)
    r.add_post("/api/machine/session/code", session_code)
    r.add_post("/api/machine/session/cancel", session_cancel)
    r.add_post("/api/install-mode", install_mode_set)
    app.on_startup.append(opening)
    app.on_cleanup.append(deploy_cleanup)
    app.on_cleanup.append(push_cleanup)
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


async def take_port(runner, port, wait):
    """1.14, a new server taking over: the cockpit's port, as soon as the
    old server has let it go — at most `wait` seconds."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + wait
    while True:
        site = web.TCPSite(runner, HOST, port)
        try:
            await site.start()
            return site
        except OSError:
            await site.stop()
            if loop.time() >= deadline:
                raise
            await asyncio.sleep(0.2)


async def serve(app, port, url, ouvrir, quit_box, relay=None):
    """Serve until « Arrêter le cockpit » (or Ctrl+C in a console). 1.14:
    `relay`, a trial port — the new server « Mettre à jour le cockpit »
    started answers there first, then takes the cockpit's port once the old
    server has exited, and closes the trial one."""
    quit_box["event"] = asyncio.Event()
    if PORT_KEY in app:
        app[PORT_KEY]["port"] = port
    runner = web.AppRunner(app, shutdown_timeout=2)
    await runner.setup()
    try:
        if relay:
            trial = web.TCPSite(runner, HOST, relay)
            await trial.start()
            print(f"Relève : le nouveau serveur répond sur le port d'essai {relay} ; il attend le port {port}.",
                  flush=True)
            await take_port(runner, port, selfupdate.TAKEOVER_WAIT)
            await trial.stop()
            print(f"Relève faite : le port {port} est à ce serveur, le port d'essai est fermé.", flush=True)
        else:
            await web.TCPSite(runner, HOST, port).start()
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


# 1.16 — how long lancer.bat waits for a restarted cockpit before opening
# the page anyway.
LANCER_WAIT = 75.0


def older_server(other, port):
    """1.16 — lancer.bat while a cockpit answers: the commit it started from
    against the code on disk; older, it is asked to restart — refused while
    something goes there, and the page then says so —, and the browser waits
    for the new one. True when it restarted."""
    head = gitref.head(CHAIN_ROOT)
    was = other.get("started")
    if not was or not head or was == head:
        return False
    print(f"Ce cockpit tourne sur {was[:7]}, le code sur le disque est à {head[:7]} : il est prié de redémarrer.",
          flush=True)
    r = startup.ask_restart(port)
    if not r.get("ok"):
        print(f"Redémarrage refusé : {r.get('error')} — la page s'ouvre sur l'ancien.", flush=True)
        return False
    got = startup.wait_new_server(port, other.get("pid"), LANCER_WAIT)
    print("Le nouveau serveur répond." if got else "Le nouveau serveur ne répond pas encore : la page s'ouvre quand même.",
          flush=True)
    return bool(got)


def main(argv=None):
    """`pythonw server.py --ouvrir`, from lancer.bat. When a cockpit already
    answers on the port, only the browser opens on it. Returns the exit code."""
    p = argparse.ArgumentParser(description="Cockpit de la chaîne")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--ouvrir", action="store_true", help="ouvrir le navigateur")
    p.add_argument("--config", default=None)
    p.add_argument("--stats", default=None, help="la base de consommation (stats.sqlite par défaut)")
    p.add_argument("--journaux", default=None, help="le dossier des journaux (logs/ par défaut)")
    p.add_argument("--relais", type=int, default=None,
                   help="1.14 — « Mettre à jour le cockpit » : le port d'essai où répondre d'abord, avant de "
                        "prendre --port une fois l'ancien serveur arrêté")
    args = p.parse_args(argv)
    # What a restart starts the new server with again (1.14).
    LAUNCH_ARGS[:] = [x for k, v in (("--config", args.config), ("--stats", args.stats),
                                     ("--journaux", args.journaux)) if v for x in (k, v)]
    url = f"http://{HOST}:{args.port}/"
    log_dir = args.journaux or runner_mod.LOG_DIR

    startup.open_log(os.path.join(log_dir, startup.LOG_NAME))
    if startup.windowless():
        startup.hide_child_consoles()
    print(f"--- {datetime.now().isoformat(timespec='seconds')} · démarrage, pid {os.getpid()}, "
          + ("sans console" if startup.windowless() else "dans une console"), flush=True)

    other = None if args.relais else startup.ping(args.port)
    if other:
        print(f"Un cockpit répond déjà sur {url} (pid {other.get('pid')}) : la page s'ouvre sur lui, "
              "aucun second serveur.", flush=True)
        older_server(other, args.port)
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
        asyncio.run(serve(app, args.port, url, args.ouvrir, quit_box, relay=args.relais))
    except KeyboardInterrupt:
        return 0
    except OSError as e:
        if args.relais:
            msg = (f"Mettre à jour le cockpit : le nouveau serveur n'a pas pu prendre le port {args.port} "
                   f"en {int(selfupdate.TAKEOVER_WAIT)} s ({e}). Relancer le cockpit par son raccourci.")
            print(msg, flush=True)
            startup.error_box(msg)
            return 1
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
