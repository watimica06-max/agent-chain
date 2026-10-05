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

from aiohttp import web

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import blocking   # noqa: E402
import questions  # noqa: E402
import runner as runner_mod  # noqa: E402
import writer     # noqa: E402
from state import State  # noqa: E402

HOST = "127.0.0.1"
DEFAULT_PORT = 8765
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
    base = features_dir(app)
    out = []
    for name in sorted(os.listdir(base)):
        p = os.path.join(base, name)
        if not os.path.isdir(p) or name.startswith("."):
            continue
        out.append(name)
        for sub in sorted(os.listdir(p), key=_natural):
            if BUGFIX.match(sub) and os.path.isdir(os.path.join(p, sub)):
                out.append(f"{name}/{sub}")
    return out


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
        out.append({"name": name[:-3], "description": desc, "argument_hint": hint})
    out.sort(key=lambda c: (0 if c["name"][0].isdigit() else 1, _natural(c["name"])))
    return out


# --------------------------------------------------------------- forms

def collect_forms(app, work, rn):
    wd = work_dir(app, work)
    qs, qerr = questions.scan(wd)
    wts = []
    for wt in rn.live_worktrees(app):
        wt_work = os.path.join(wt, "docs", "features", *work.split("/"))
        if os.path.isdir(wt_work):
            wts.append((wt, wt_work))
    bs, notices, redec = blocking.scan(wd, wts)
    return qs, qerr, bs, notices, redec, [wt for wt, _ in wts]


def forms_payload(app, work, rn):
    qs, qerr, bs, notices, redec, wts = collect_forms(app, work, rn)
    return {
        "questions": [q.to_dict() for q in qs],
        "blocking": [b.to_dict() for b in bs],
        "redecoupage": redec.to_dict() if redec else None,
        "errors": [e.to_dict() for e in qerr] + [n.to_dict() for n in notices],
        "worktrees": wts,
    }


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
            results.append(writer.write_redecoupage(entry, choice, work_dir(app, work)))
    return [r.to_dict() for r in results]


# -------------------------------------------------------------- the app

def ask_directory(initial):
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
                                       title="Choisir le dossier de l'application")
    finally:
        root.destroy()
    return path or ""


LOCAL_NAMES = {"127.0.0.1", "localhost"}


def _host_name(hostport):
    from urllib.parse import urlsplit
    try:
        return urlsplit("//" + (hostport or "")).hostname
    except ValueError:
        return None


def make_app(state: State, rn: runner_mod.Runner, picker=ask_directory):
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

    async def get_state(request):
        a, w = pair()
        out = {"app_folder": state.app_folder, "working_folder": state.working_folder,
               "recent": state.recent(), "load_error": state.load_error,
               "open": bool(a)}
        if state.app_folder and not check_app_folder(state.app_folder):
            out["working_folders"] = working_folders(state.app_folder)
        if a:
            run = rn.current(a)
            feature = feature_of(w)
            out.update({
                "feature": feature,
                "commands": list_commands(a),
                "last": state.relay(a, w),
                "run": run.snapshot() if run and run.id else None,
                "stop_file": os.path.exists(rn.stop_file(a, feature)),
            })
        return web.json_response(out)

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

    async def save(request):
        a, w = need_pair()
        data = await body(request)
        items = data.get("items") or []
        results = save_items(a, w, rn, items)
        return web.json_response({"results": results})

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
    r.add_post("/api/pick-folder", pick_folder)
    r.add_post("/api/app-folder", app_folder)
    r.add_post("/api/open", open_pair)
    r.add_post("/api/close", close_pair)
    r.add_get("/api/forms", forms)
    r.add_post("/api/save", save)
    r.add_post("/api/run", run)
    r.add_post("/api/stop-now", stop_now)
    r.add_post("/api/stop-next-lot", stop_next)
    r.add_post("/api/disarm-stop", disarm)
    r.add_post("/api/permission", permission)
    r.add_get("/api/events", events)
    return app


def _sse(ev):
    return f"data: {json.dumps(ev, ensure_ascii=False)}\n\n".encode("utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description="Cockpit de la chaîne")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--ouvrir", action="store_true", help="ouvrir le navigateur")
    p.add_argument("--config", default=None)
    args = p.parse_args(argv)

    state = State(args.config) if args.config else State()

    def on_end(run):
        state.set_relay(run.repo, run.work, run.prompt, run.relay, run.next, run.outcome)

    rn = runner_mod.Runner(on_end=on_end)
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
