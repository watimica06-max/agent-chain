"""The cockpit's local server — TECHNICAL_V1 §3. Listens on 127.0.0.1 only.

    python server.py [--port 8765] [--ouvrir]
"""
import argparse
import asyncio
import json
import os
import re
import sys
import webbrowser
from datetime import datetime

from aiohttp import web

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import blocking   # noqa: E402
import context as context_mod  # noqa: E402
import decide as decide_mod  # noqa: E402
import diagnostic  # noqa: E402
import gitref     # noqa: E402
import questions  # noqa: E402
import runner as runner_mod  # noqa: E402
import scan as scan_mod  # noqa: E402
import stats as stats_mod  # noqa: E402
import statsview  # noqa: E402
import textfile   # noqa: E402
import writer     # noqa: E402
from state import State  # noqa: E402

HOST = "127.0.0.1"
STATE_KEY = web.AppKey("state", State)
DEFAULT_PORT = 8765
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
    if not app or not os.path.isdir(app):
        return "dossier introuvable"
    if not os.path.isdir(os.path.join(app, ".claude")):
        return "pas de dossier .claude/ : ce n'est pas un dossier d'application de la chaîne"
    if not os.path.isdir(features_dir(app)):
        return "pas de dossier docs/features/"
    return None


def working_folders(app):
    """The features of `docs/features/`. Since 1.3 a feature's `bugfix-NN/`
    are not picked here: they live under « Correction »."""
    base = features_dir(app)
    return [name for name in sorted(os.listdir(base))
            if os.path.isdir(os.path.join(base, name)) and not name.startswith(".")]


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


# ------------------------------------------------------------- the scan

def where(state: State, rn, app, feature, reason=None):
    """The scan and §2's decision. `reason` names a scan trigger — the
    button, the opening, a save of answers: it ends the moment a run's
    `Next:` is trusted without a check. A dropped `Next:` is written to
    the run's log, once."""
    run = rn.current(app)
    snap = run.snapshot() if run and run.id else None
    sc = scan_mod.run_scan(app, feature, snap)
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


def ask_export_folder(initial):
    return ask_directory(initial, title="Où enregistrer les deux fichiers CSV ?")


def default_export_folder():
    for name in ("Downloads", "Documents"):
        p = os.path.join(os.path.expanduser("~"), name)
        if os.path.isdir(p):
            return p
    return os.path.expanduser("~")


def make_app(state: State, rn: runner_mod.Runner, picker=ask_directory,
             diag_runner=None, export_picker=ask_export_folder):
    store = rn.stats
    diag_runner = diag_runner or DIAG_RUNNER
    # The diagnostic run in the background (1.4.5): once, at the opening,
    # when no result is stored.
    diag = {"running": False, "auto_done": False, "task": None}
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

    app = web.Application(middlewares=[guard])
    app[STATE_KEY] = state

    def pair():
        a, w = state.app_folder, state.working_folder
        if not a or check_app_folder(a) or not w or not os.path.isdir(work_dir(a, w)):
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
        return web.FileResponse(os.path.join(HERE, "static", "index.html"),
                                headers={"Cache-Control": "no-store"})

    def state_payload(reason=None):
        a, w = pair()
        out = {"app_folder": state.app_folder, "working_folder": state.working_folder,
               "recent": state.recent(), "load_error": state.load_error,
               "open": bool(a), "mode": state.mode, "diagnostic": state.diagnostic(),
               "diagnostic_running": diag["running"],
               "logs_dir": rn.log_dir, "groups": GROUPS,
               # The two usage windows, each with when it was measured (§13.3).
               "limits": _limits(store), "now": datetime.now().isoformat(timespec="seconds")}
        if state.app_folder and not check_app_folder(state.app_folder):
            out["working_folders"] = working_folders(state.app_folder)
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
        return web.json_response({"path": path, "working_folders": working_folders(path)})

    async def open_pair(request):
        data = await body(request)
        a = os.path.normpath((data.get("app") or "").strip().strip('"'))
        w = (data.get("work") or "").strip().strip("/")
        err = check_app_folder(a)
        if err:
            return web.json_response({"error": err}, status=400)
        if w not in working_folders(a):
            return web.json_response({"error": "dossier de travail inconnu"}, status=400)
        state.open_pair(a, w)
        return web.json_response({"ok": True})

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
        try:
            r = await rn.start(a, w, feature_of(w), cmd, args)
        except runner_mod.Busy as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"run": r.snapshot()})

    async def stop_now(request):
        a, _ = need_pair()
        try:
            await rn.stop_now(a)
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"ok": True})

    async def set_mode(request):
        data = await body(request)
        try:
            state.set_mode(data.get("mode"))
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"mode": state.mode})

    async def diagnose(a):
        diag["running"] = True
        try:
            result = await asyncio.get_running_loop().run_in_executor(None, diag_runner, a)
            state.set_diagnostic(result)
            return result
        finally:
            diag["running"] = False

    def auto_diagnostic(a):
        """No result stored: the diagnostic runs once, in the background, and
        its result is kept. Paramètres → Diagnostic still runs it on demand."""
        if diag["auto_done"] or diag["running"] or state.diagnostic() is not None or not a:
            return
        diag["auto_done"] = True

        async def go():
            try:
                await diagnose(a)
            except Exception as e:      # reported, never raised into the loop
                print(f"Diagnostic automatique non abouti : {e}", flush=True)
        diag["task"] = asyncio.get_running_loop().create_task(go())

    async def opening(_app):
        a, _ = pair()
        if a:
            auto_diagnostic(a)

    async def run_diagnostic(request):
        a, _ = need_pair()
        return web.json_response(await diagnose(a))

    # ------------------------------------------------ statistics (1.4.5)
    def stats_args(request, data=None):
        a, w = need_pair()
        q = data if data is not None else request.query
        f = (q.get("feature") or "").strip()
        feature = None if f == "*" else (f or feature_of(w))
        return feature, q.get("period") or "tout"

    def stats_data(feature, period):
        return statsview.build(store.path if store else None, feature, period)

    async def stats_get(request):
        feature, period = stats_args(request)
        return web.json_response(stats_data(feature, period))

    async def stats_csv(request):
        feature, period = stats_args(request)
        kind = request.query.get("kind", "runs")
        files = statsview.csv_files(stats_data(feature, period))
        name, text = files[1] if kind == "passes" else files[0]
        return web.Response(text=text, content_type="text/csv", charset="utf-8",
                            headers={"Content-Disposition": f'attachment; filename="{name}"'})

    async def stats_export(request):
        """« Exporter »: the runs and the agent passes of the current filters,
        as two CSV files in the folder the Product Owner picks."""
        data = await body(request)
        feature, period = stats_args(request, data)
        loop = asyncio.get_running_loop()
        try:
            folder = await loop.run_in_executor(None, export_picker, default_export_folder())
        except Exception as e:
            return web.json_response({"error": f"le sélecteur n'a pas pu s'ouvrir ({e})"}, status=500)
        if not folder:
            return web.json_response({"cancelled": True})
        written = []
        try:
            for name, text in statsview.csv_files(stats_data(feature, period)):
                path = os.path.join(folder, name)
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
                written.append(path)
        except OSError as e:
            return web.json_response({"error": f"fichier non écrit : {e}", "files": written}, status=500)
        return web.json_response({"files": written})

    async def continue_wait(request):
        a, _ = need_pair()
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
        a, _ = need_pair()
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
        a, _ = need_pair()
        data = await body(request)
        try:
            rn.answer_permission(a, data.get("id", ""), bool(data.get("allow")))
        except runner_mod.NotRunning as e:
            return web.json_response({"error": str(e)}, status=409)
        return web.json_response({"ok": True})

    async def events(request):
        a, _ = need_pair()
        resp = web.StreamResponse(headers={"Content-Type": "text/event-stream",
                                           "Cache-Control": "no-cache",
                                           "X-Accel-Buffering": "no"})
        await resp.prepare(request)
        q = rn.subscribe(a)
        try:
            current = rn.current(a)
            for ev in list(current.events if current else [])[-1500:]:
                await resp.write(_sse(ev))
            while True:
                try:
                    ev = await asyncio.wait_for(q.get(), timeout=15)
                    await resp.write(_sse(ev))
                except asyncio.TimeoutError:
                    await resp.write(b": ping\n\n")
        except (ConnectionResetError, asyncio.CancelledError):
            pass
        finally:
            rn.unsubscribe(a, q)
        return resp

    r = app.router
    r.add_get("/", index)
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
    r.add_post("/api/diagnostic", run_diagnostic)
    r.add_post("/api/continue-wait", continue_wait)
    r.add_post("/api/continue-session", continue_session)
    r.add_post("/api/stop-next-lot", stop_next)
    r.add_post("/api/disarm-stop", disarm)
    r.add_post("/api/permission", permission)
    r.add_get("/api/events", events)
    r.add_get("/api/stats", stats_get)
    r.add_get("/api/stats/csv", stats_csv)
    r.add_post("/api/stats/export", stats_export)
    app.on_startup.append(opening)
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
    return done


def _sse(ev):
    return f"data: {json.dumps(ev, ensure_ascii=False)}\n\n".encode("utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description="Cockpit de la chaîne")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--ouvrir", action="store_true", help="ouvrir le navigateur")
    p.add_argument("--config", default=None)
    args = p.parse_args(argv)

    state = State(args.config) if args.config else State()

    store = stats_mod.Store()
    rn = runner_mod.Runner(on_end=make_on_end(state), mode_getter=lambda: state.mode, stats=store)
    done = backfill(store, state, rn.log_dir)
    if done["runs"]:
        print(f"Consommation : {done['runs']} journal(aux) ancien(s) chargé(s) dans stats.sqlite "
              f"({done['passes']} passage(s) d'agent, {done['limits']} mesure(s) d'usage).", flush=True)
    if done["outputs"]["runs"]:
        print(f"Consommation : tokens écrits retrouvés pour {done['outputs']['runs']} run(s) "
              f"({done['outputs']['passes']} passage(s) d'agent), d'après le model_usage des journaux.", flush=True)
    app = make_app(state, rn)
    url = f"http://{HOST}:{args.port}/"

    async def opened(_app):
        print(f"Cockpit : {url}  (Ctrl+C pour arrêter)", flush=True)
        if args.ouvrir:
            # on_startup runs just before the socket is bound.
            asyncio.get_running_loop().call_later(1.0, webbrowser.open, url)

    app.on_startup.append(opened)
    web.run_app(app, host=HOST, port=args.port, print=None)


if __name__ == "__main__":
    main()
