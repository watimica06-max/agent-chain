"""The routes, end to end on a fake application folder built from the
fixtures. No chain command runs: the SDK client is a fake."""
import asyncio
import json
import os
import shutil

from aiohttp.test_utils import TestClient, TestServer

import cmdtests
import runner as runner_mod
import server
from conftest import fixture_path
from state import State
from test_runner import FakeClient, script_until_interrupted


def build_app_folder(root):
    cmds = root / ".claude" / "commands"
    cmds.mkdir(parents=True)
    for name, hint in [("1_lexique", "<feature folder name>"), ("8_code", "<feature folder name> [N]"),
                       ("10_x", "<feature folder name>"), ("deploie", None), ("2_structure", "<f>")]:
        fm = f'---\ndescription: run {name}\n' + (f'argument-hint: "{hint}"\n' if hint else "") + "---\n"
        (cmds / f"{name}.md").write_text(fm + "body\n", encoding="utf-8")
    feat = root / "docs" / "features" / "f"
    (feat / "bugfix-01").mkdir(parents=True)
    (feat / "convertisseur").mkdir()
    (feat / "code").mkdir()
    for src, dst in [("hand/questions-sondeur-02.md", "questions-sondeur-02.md"),
                     ("hand/convertisseur/technique-model.md", "convertisseur/technique-model.md"),
                     ("hand/blocked_qualifieur.md", "blocked_qualifieur.md"),
                     ("hand/blocked_detailleur.md", "code/blocked_detailleur.md"),
                     ("hand/questions-hors-gabarit.md",
                      "questions-architecte-01.md")]:
        shutil.copyfile(fixture_path(*src.split("/")), feat / dst)
    return feat


def with_client(tmp_path, body, picker=None, script=script_until_interrupted):
    app_root = tmp_path / "app"
    feat = build_app_folder(app_root)
    state = State(str(tmp_path / "config.json"))

    def factory(cwd, can_use_tool, **kw):
        return FakeClient(script, can_use_tool)

    rn = runner_mod.Runner(client_factory=factory,
                           on_end=server.make_on_end(state), mode_getter=lambda: state.mode)
    app = server.make_app(state, rn, picker=picker or (lambda initial: str(app_root)))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            return await body(c, app_root, feat, rn)

    return asyncio.run(go())


async def post(c, path, data):
    return await c.post(path, data=json.dumps(data), headers={"Content-Type": "application/json"})


async def open_pair(c, app_root, work="f"):
    r = await post(c, "/api/open", {"app": str(app_root), "work": work})
    assert r.status == 200, await r.text()


def test_guards(tmp_path):
    async def body(c, app_root, feat, rn):
        r = await c.get("/api/state", headers={"Host": "evil.example:8765"})
        assert r.status == 403
        r = await c.post("/api/open", data="app=x", headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert r.status == 415
        r = await c.post("/api/open", data="{}", headers={"Content-Type": "application/json",
                                                         "Origin": "http://evil.example"})
        assert r.status == 403
        r = await c.get("/")
        assert r.status == 200 and "Cockpit de la chaîne" in await r.text()
    with_client(tmp_path, body)


def test_start_screen_then_open(tmp_path):
    async def body(c, app_root, feat, rn):
        s = await (await c.get("/api/state")).json()
        assert s["open"] is False
        r = await post(c, "/api/pick-folder", {})
        assert (await r.json())["path"] == str(app_root)
        r = await post(c, "/api/app-folder", {"path": str(app_root)})
        # 1.3: the features alone; their bugfix-NN/ live under « Correction ».
        assert (await r.json())["working_folders"] == ["f"]
        r = await post(c, "/api/app-folder", {"path": str(feat)})
        assert r.status == 400
        r = await post(c, "/api/open", {"app": str(app_root), "work": "f/bugfix-01"})
        assert r.status == 400
        await open_pair(c, app_root, "f")
        s = await (await c.get("/api/state")).json()
        assert s["open"] and s["feature"] == "f" and s["last"] is None and s["run"] is None
        assert [x["name"] for x in s["commands"]] == ["1_lexique", "2_structure", "8_code", "10_x", "deploie"]
        assert s["recent"][0] == {"app": str(app_root), "work": "f"}
        assert s["bugfixes"] == ["bugfix-01"] and s["scan"]["main"][0]["id"] == "1_lexique"
        assert s["decision"]["label"] == "déduite du dossier"
    with_client(tmp_path, body)


def test_picker_failure_is_reported(tmp_path):
    def broken(initial):
        raise RuntimeError("no display")

    async def body(c, app_root, feat, rn):
        r = await post(c, "/api/pick-folder", {})
        assert r.status == 500 and "collez le chemin" in (await r.json())["error"]
    with_client(tmp_path, body, picker=broken)


def test_forms_and_save(tmp_path):
    async def body(c, app_root, feat, rn):
        await open_pair(c, app_root)
        f = await (await c.get("/api/forms")).json()
        # sondeur-02: Q1 (default), Q2, Q3; technique-model: Q1
        assert sorted(q["id"] for q in f["questions"]) == [
            "q:convertisseur/technique-model.md#1", "q:questions-sondeur-02.md#1",
            "q:questions-sondeur-02.md#2", "q:questions-sondeur-02.md#3"]
        assert sorted(b["id"] for b in f["blocking"]) == [
            "b:blocked_qualifieur.md#2", "b:code/blocked_detailleur.md#1", "b:code/blocked_detailleur.md#3"]
        assert [e["rel"] for e in f["errors"]] == ["questions-architecte-01.md"]
        by = {x["id"]: x for x in f["questions"] + f["blocking"]}
        q2 = by["q:questions-sondeur-02.md#2"]
        items = [
            {"id": q2["id"], "fingerprint": q2["fingerprint"], "kind": "option", "option": q2["options"][2], "text": ""},
            {"id": "q:questions-sondeur-02.md#1", "fingerprint": by["q:questions-sondeur-02.md#1"]["fingerprint"],
             "kind": "default", "option": by["q:questions-sondeur-02.md#1"]["default"], "text": ""},
            {"id": "b:code/blocked_detailleur.md#3", "fingerprint": by["b:code/blocked_detailleur.md#3"]["fingerprint"],
             "kind": "free", "text": "delta-zero partout."},
            {"id": "q:questions-sondeur-02.md#3", "fingerprint": "stale", "kind": "free", "text": "x"},
            {"id": "q:gone.md#1", "fingerprint": "x", "kind": "free", "text": "x"},
            {"id": "b:blocked_qualifieur.md#2", "kind": "none"},
        ]
        res = (await (await post(c, "/api/save", {"items": items})).json())["results"]
        assert [(r["id"], r["status"]) for r in res] == [
            ("q:questions-sondeur-02.md#2", "saved"),
            ("q:questions-sondeur-02.md#1", "unchanged"),
            ("b:code/blocked_detailleur.md#3", "saved"),
            ("q:questions-sondeur-02.md#3", "error"),
            ("q:gone.md#1", "error"),
        ]
        assert cmdtests.unanswered_questions(str(feat / "questions-sondeur-02.md")) == [3]
        assert cmdtests.shape4_open(str(feat / "code" / "blocked_detailleur.md")) == [1]
        f = await (await c.get("/api/forms")).json()
        assert len(f["questions"]) == 3 and len(f["blocking"]) == 2
    with_client(tmp_path, body)


async def read_events(resp, kinds, limit=50):
    got = []
    while len(got) < limit:
        line = await asyncio.wait_for(resp.content.readline(), 3)
        if line.startswith(b"data: "):
            ev = json.loads(line[6:])
            got.append(ev)
            if ev["type"] in kinds:
                return got
    return got


def test_run_lock_stop_and_events(tmp_path):
    async def body(c, app_root, feat, rn):
        await open_pair(c, app_root)
        r = await post(c, "/api/run", {"command": "nope", "args": "f"})
        assert r.status == 400
        ev = await c.get("/api/events")
        r = await post(c, "/api/run", {"command": "8_code", "args": "f"})
        assert r.status == 200, await r.text()
        got = await read_events(ev, {"text"})
        assert [e["type"] for e in got][:2] == ["run_started", "status"]
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 409
        s = await (await c.get("/api/state")).json()
        assert s["run"]["status"] == "running" and s["run"]["stop_next_lot"]
        r = await post(c, "/api/stop-next-lot", {})
        assert r.status == 200 and os.path.exists(feat / "stop.md")
        assert (await (await c.get("/api/state")).json())["stop_file"]
        r = await post(c, "/api/stop-now", {})
        assert r.status == 200
        await read_events(ev, {"run_ended"})
        ev.close()
        s = await (await c.get("/api/state")).json()
        assert s["run"]["outcome"] == "interrompu"
        assert s["last"]["command"] == "/8_code f" and s["last"]["next"]["kind"] == "unknown"
        r = await post(c, "/api/disarm-stop", {})
        assert r.status == 200 and os.path.exists(feat / "stop1.md")
    with_client(tmp_path, body)


def test_continue_routes(tmp_path):
    async def body(c, app_root, feat, rn):
        await open_pair(c, app_root)
        r = await post(c, "/api/continue-wait", {})
        assert r.status == 409                       # nothing waits on a decision
        r = await post(c, "/api/continue-session", {})
        assert r.status == 409                       # no ended run yet
        ev = await c.get("/api/events")
        await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        await read_events(ev, {"text"})
        await post(c, "/api/stop-now", {})
        await read_events(ev, {"run_ended"})
        s = (await (await c.get("/api/state")).json())["run"]
        assert s["can_continue"] and s["session_id"] == "s" and s["log_path"]
        r = await post(c, "/api/continue-session", {})
        assert r.status == 200, await r.text()
        assert (await r.json())["run"]["continued"] is True
        await read_events(ev, {"text"})
        await post(c, "/api/stop-now", {})
        await read_events(ev, {"run_ended"})
        ev.close()
    with_client(tmp_path, body)


def test_permission_route(tmp_path):
    from test_runner import script_with_permission

    async def body(c, app_root, feat, rn):
        await open_pair(c, app_root)
        ev = await c.get("/api/events")
        await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        got = await read_events(ev, {"permission"})
        pid = got[-1]["data"]["id"]
        r = await post(c, "/api/permission", {"id": pid, "allow": True})
        assert r.status == 200
        await read_events(ev, {"run_ended"})
        ev.close()
        r = await post(c, "/api/permission", {"id": pid, "allow": True})
        assert r.status == 409
        s = await (await c.get("/api/state")).json()
        assert s["last"]["next"]["kind"] == "answer" and s["last"]["next"]["command"] == "1_lexique"
    with_client(tmp_path, body, script=script_with_permission)


def test_an_ignored_folder_is_never_shown(tmp_path):
    # 1.5.1 — config.json « ignored »: no feature list, no opening, no
    # statistics filter; Paramètres → Dossiers edits it.
    async def body(c, app_root, feat, rn):
        old = app_root / "docs" / "features" / "premiere-app"
        (old / "bugfix-06").mkdir(parents=True)
        # 1.6: a new application ignores nothing.
        r = await post(c, "/api/app-folder", {"path": str(app_root)})
        assert (await r.json())["working_folders"] == ["f", "premiere-app"]
        await open_pair(c, app_root, "f")
        s = await (await post(c, "/api/ignored", {"ignored": ["premiere-app", "premiere-app-2"]})).json()
        r = await post(c, "/api/app-folder", {"path": str(app_root)})
        assert (await r.json())["working_folders"] == ["f"]
        r = await post(c, "/api/open", {"app": str(app_root), "work": "premiere-app"})
        assert r.status == 400 and "ignoré" in (await r.json())["error"]
        s = await (await c.get("/api/state")).json()
        assert s["working_folders"] == ["f"] and s["all_folders"] == ["f", "premiere-app"]
        assert s["ignored"] == ["premiere-app", "premiere-app-2"]
        r = await c.get("/api/stats?feature=premiere-app")
        assert r.status == 400
        # Un-ticked: shown again.
        s = await (await post(c, "/api/ignored", {"ignored": ["premiere-app-2"]})).json()
        assert s["working_folders"] == ["f", "premiere-app"] and s["open"]
        # Ticking the feature open closes it.
        s = await (await post(c, "/api/ignored", {"ignored": ["f"]})).json()
        assert s["open"] is False and s["working_folders"] == ["premiere-app"]
        r = await post(c, "/api/ignored", {"ignored": "f"})
        assert r.status == 400
    with_client(tmp_path, body)
