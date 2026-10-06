"""1.6 — several applications (TECHNICAL_V1 §21): the list in config.json and
its migration, adding, renaming, removing, switching, « Tout mettre à jour »
on scratch repositories, a run in one application seen from another, the
statistics per application and their backfill, the diagnostic per
application, a git folder where the chain is not installed yet. Every
repository is built in tmp_path; nothing reaches GitHub; no chain command
runs — the SDK client is a fake."""
import asyncio
import json
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime

import pytest
from aiohttp.test_utils import TestClient, TestServer

import chain
import diagnostic
import runner as runner_mod
import server
import stats
from state import State
from test_chain import CHAIN_FILES, commit, git, init, write
from test_mode_diagnostic import ALL_GOOD, fake_exec
from test_runner import FakeClient, script_until_interrupted, script_with_permission
from test_server import build_app_folder, post


def serve(tmp_path, body, state=None, script=script_until_interrupted, store=None, diag_runner=None):
    st = state or State(str(tmp_path / "config.json"))
    made = []

    def factory(cwd, can_use_tool, **kw):
        c = FakeClient(script, can_use_tool)
        c.cwd = cwd
        made.append(c)
        return c

    rn = runner_mod.Runner(client_factory=factory, on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"), stats=store)
    app = server.make_app(st, rn, **({"diag_runner": diag_runner} if diag_runner else {}))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            return await body(c, st, rn)
    return asyncio.run(go())


async def state_of(c):
    return await (await c.get("/api/state")).json()


def tree(folder):
    """Every file of a folder outside .git, with its bytes: what « never
    touched » is checked against."""
    out = {}
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            p = os.path.join(root, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, folder)] = fh.read()
    return out


def second_app(root):
    """Another application: its own feature « g », one open question."""
    (root / ".claude" / "commands").mkdir(parents=True)
    (root / ".claude" / "commands" / "1_lexique.md").write_text(
        '---\ndescription: run 1_lexique\nargument-hint: "<f>"\n---\nbody\n', encoding="utf-8")
    g = root / "docs" / "features" / "g"
    g.mkdir(parents=True)
    (g / "idees.md").write_text("# Idées\n", encoding="utf-8")
    (g / "questions-lexicographe-01.md").write_text(
        "### Q1\nTerms: a, b\nQuestion: One thing?\nAnswer:\n", encoding="utf-8")
    return g


# ------------------------------------------------------------ migration

TODAY = {
    "app_folder": "C:\\Dev\\hyrox_tracker",
    "working_folder": "premiere-app-3",
    "recent": [{"app": "C:\\Dev\\hyrox_tracker", "work": "premiere-app-3"}],
    "relays": {"c:\\dev\\hyrox_tracker|premiere-app-3": {
        "command": "/1_lexique premiere-app-3", "relay": "…\n\nNext: answer questions, then run /1_lexique premiere-app-3",
        "next": {"kind": "answer", "raw": "Next: answer questions, then run /1_lexique premiere-app-3"},
        "outcome": "terminé", "at": "2026-10-06T11:24:15", "head": "69fbfdc", "log_path": "C:\\logs\\x.jsonl"}},
    "mode": "manuel",
    "diagnostic": {"at": "2026-10-06T15:37:21", "app": "C:\\Dev\\hyrox_tracker", "results": [], "hints": [], "ok": True},
    "history": [{"key": "c:\\dev\\hyrox_tracker|premiere-app-3", "command": "/1_lexique premiere-app-3",
                 "outcome": "terminé", "log_path": "C:\\logs\\x.jsonl", "at": "2026-10-06T11:24:15"}],
    "ignored": {"c:\\dev\\hyrox_tracker": ["premiere-app", "premiere-app-2"]},
}


def test_todays_config_becomes_a_list_of_one_nothing_lost(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps(TODAY, ensure_ascii=False), encoding="utf-8")
    s = State(str(path))
    assert s.migrated
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert "app_folder" not in saved and "relays" not in saved and "ignored" not in saved
    assert saved["active"] == "C:\\Dev\\hyrox_tracker"
    [a] = saved["apps"]
    assert a["name"] == "hyrox_tracker" and a["folder"] == "C:\\Dev\\hyrox_tracker"
    assert a["ignored"] == ["premiere-app", "premiere-app-2"] and a["last_feature"] == "premiere-app-3"
    assert a["relays"]["premiere-app-3"] == TODAY["relays"]["c:\\dev\\hyrox_tracker|premiere-app-3"]
    assert a["diagnostic"] == TODAY["diagnostic"]
    assert saved["mode"] == "manuel" and saved["history"] == TODAY["history"] and saved["recent"] == TODAY["recent"]
    # Read back the way every screen reads it.
    again = State(str(path))
    assert not again.migrated
    assert again.app_folder == "C:\\Dev\\hyrox_tracker" and again.working_folder == "premiere-app-3"
    assert again.relay("C:/Dev/hyrox_tracker", "premiere-app-3")["head"] == "69fbfdc"
    assert again.ignored == ["premiere-app", "premiere-app-2"] and again.diagnostic()["ok"]
    assert again.history("C:\\Dev\\hyrox_tracker", "premiere-app-3")[0]["command"] == "/1_lexique premiere-app-3"
    assert again.last_relay("C:\\Dev\\hyrox_tracker")[0] == "premiere-app-3"


def test_a_1_5_1_ignored_list_and_another_recent_application(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"app_folder": "C:/a", "working_folder": "f/bugfix-02", "ignored": ["old"],
                                "recent": [{"app": "C:/a", "work": "f"}, {"app": "C:/b", "work": "g"}]}), encoding="utf-8")
    s = State(str(path))
    assert [(a["name"], a["last_feature"], a["ignored"]) for a in s.apps()] == [("a", "f", ["old"]), ("b", "g", [])]
    assert s.app_folder == "C:/a" and s.working_folder == "f"


# ---------------------------------------------------- add, rename, remove

def test_add_a_git_folder_refuse_another_rename_remove(tmp_path):
    git_app = tmp_path / "belivo"
    init(git_app)
    write(git_app, "lib/main.dart", "void main() {}\n")
    commit(git_app, "app")
    (git_app / "wip.txt").write_text("du travail en cours\n", encoding="utf-8")       # uncommitted, hers
    before = tree(git_app)
    plain = tmp_path / "pas-git"
    plain.mkdir()
    (git_app / "sub").mkdir()

    async def body(c, st, rn):
        r = await post(c, "/api/apps/add", {"path": str(plain)})
        assert r.status == 400 and "pas un dépôt git" in (await r.json())["error"]
        r = await post(c, "/api/apps/add", {"path": str(git_app / "sub")})
        assert r.status == 400 and "racine" in (await r.json())["error"]
        r = await post(c, "/api/apps/add", {"path": str(tmp_path / "nulle-part")})
        assert r.status == 400 and (await r.json())["error"] == "dossier introuvable"
        r = await post(c, "/api/apps/add", {"path": str(git_app)})
        j = await r.json()
        assert r.status == 200 and j["added"] and j["app"]["name"] == "belivo"
        r = await post(c, "/api/apps/add", {"path": str(git_app)})
        assert (await r.json())["added"] is False and len(st.apps()) == 1               # once in the list
        r = await post(c, "/api/apps/rename", {"folder": str(git_app), "name": "  Belivo  "})
        assert r.status == 200 and st.apps()[0]["name"] == "Belivo"
        r = await post(c, "/api/apps/rename", {"folder": str(git_app), "name": " "})
        assert r.status == 400
        rows = (await (await c.get("/api/apps")).json())["apps"]
        assert rows[0]["name"] == "Belivo" and rows[0]["uncommitted"] == 1           # wip.txt — information only; an empty sub/ is nothing to git
        r = await post(c, "/api/apps/remove", {"folder": str(git_app)})
        assert r.status == 200 and st.apps() == []
        r = await post(c, "/api/apps/remove", {"folder": str(git_app)})
        assert r.status == 404
    serve(tmp_path, body)
    after = tree(git_app)
    assert after == before                       # adding, renaming, removing never wrote in the folder
    assert git(git_app, "status", "--porcelain").splitlines() == ["?? wip.txt"]
    assert json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))["apps"] == []


# ---------------------------------------------------------------- switching

def test_switching_each_screen_reads_the_active_application(tmp_path, monkeypatch):
    a_root, b_root = tmp_path / "hyrox", tmp_path / "belivo"
    build_app_folder(a_root)
    second_app(b_root)
    monkeypatch.setattr(server, "chain_state", lambda app: {
        "state": "à jour", "summary": "Chaîne à jour — " + os.path.basename(app), "subjects": [], "modified": []})

    async def body(c, st, rn):
        st.open_pair(str(a_root), "f")
        st.open_pair(str(b_root), "g")
        st.activate(str(a_root))
        s = await state_of(c)
        assert s["app_name"] == "hyrox" and s["feature"] == "f" and s["chain"]["summary"].endswith("hyrox")
        assert [(x["name"], x["active"]) for x in s["apps"]] == [("hyrox", True), ("belivo", False)]
        fa = await (await c.get("/api/forms")).json()
        assert len(fa["questions"]) > 1
        r = await post(c, "/api/apps/open", {"folder": str(b_root)})
        assert r.status == 200 and (await r.json())["open"]
        s = await state_of(c)
        assert s["app_name"] == "belivo" and s["feature"] == "g" and s["working_folders"] == ["g"]
        assert s["chain"]["summary"].endswith("belivo")
        assert [x["name"] for x in s["commands"]] == ["1_lexique"]
        assert s["scan"]["feature"] == "g"
        fb = await (await c.get("/api/forms")).json()
        assert [q["id"] for q in fb["questions"]] == ["q:questions-lexicographe-01.md#1"]
        code = await c.get("/api/code")
        assert code.status == 200
        st_ = await (await c.get("/api/stats")).json()
        assert st_["feature"] == "g" and st_["app_name"] == "belivo"
        # Back: its last feature, as it was.
        await post(c, "/api/apps/open", {"folder": str(a_root)})
        s = await state_of(c)
        assert s["app_name"] == "hyrox" and s["feature"] == "f"
        # An application not in the list cannot be opened by its row.
        r = await post(c, "/api/apps/open", {"folder": str(tmp_path / "x")})
        assert r.status == 404
    serve(tmp_path, body)


# ------------------------------------------------- « Tout mettre à jour »

@pytest.mark.real_chain
def test_update_all_on_scratch_repositories(tmp_path, monkeypatch):
    """One « en retard » updated, committed and pushed; one « modifiée sur
    place » and one « absente » listed and untouched; one « en retard »
    with a run going, skipped. One line each."""
    root = tmp_path / "chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    commit(root, "chain one")
    monkeypatch.setattr(server, "CHAIN_ROOT", str(root))
    monkeypatch.setattr(server, "CHAIN_PUSH", True)
    chain._chain_cache.clear()
    chain._behind_cache.clear()

    def app(name, install):
        repo = tmp_path / name
        init(repo)
        write(repo, ".claude/commands/deploie.md", f"{name}'s own\n")
        write(repo, "docs/features/f/idees.md", "idea\n")
        commit(repo, "app")
        remote = tmp_path / f"{name}.git"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "-q", "-u", "origin", "master")
        if install:
            chain.install(str(repo), str(root), push=True)
        return repo, remote

    late, late_remote = app("late", True)
    modified, _ = app("modified", True)
    absent, _ = app("absent", False)
    busy, _ = app("busy", True)
    write(modified, ".claude/agents/b.md", "changed in the application\n")
    commit(modified, "edited the chain in place")
    write(root, ".claude/agents/a.md", "agent a, two\n")
    commit(root, "chain two")
    chain._chain_cache.clear()
    heads = {r: git(r, "rev-parse", "HEAD").strip() for r in (late, modified, absent, busy)}
    trees = {r: tree(r) for r in (modified, absent, busy)}

    async def body(c, st, rn):
        for r in (late, modified, absent, busy):
            st.add_app(str(r))
        st.open_pair(str(busy), "f")
        r = await post(c, "/api/run", {"command": "deploie", "args": "", "chain_ok": True})
        assert r.status == 200, await r.text()
        assert rn.is_running(str(busy))
        rows = {x["name"]: x["chain"]["state"] for x in (await (await c.get("/api/apps")).json())["apps"]}
        assert rows == {"late": chain.BEHIND, "modified": chain.MODIFIED, "absent": chain.ABSENT, "busy": chain.BEHIND}
        r = await post(c, "/api/chain/install-all", {})
        rep = await r.json()
        assert r.status == 200, rep
        lines = {x["name"]: x for x in rep["lines"]}
        assert [x["name"] for x in rep["lines"]] == ["late", "modified", "absent", "busy"]      # one per application
        assert lines["late"]["outcome"] == "mise à jour" and lines["late"]["result"]["pushed"]
        assert lines["late"]["result"]["app_commit"] in lines["late"]["text"]
        for n in ("modified", "absent"):
            assert lines[n]["outcome"] == "laissée" and lines[n]["own_install"] and "jamais en bloc" in lines[n]["text"]
        assert "modifiée sur place" in lines["modified"]["text"] and "absente" in lines["absent"]["text"]
        assert lines["busy"]["outcome"] == "laissée" and "tourne" in lines["busy"]["text"]
        # The report is kept for the screen.
        assert (await (await c.get("/api/apps")).json())["report"]["lines"] == rep["lines"]
        await rn.stop_now(str(busy))
        assert await rn.wait_ended(str(busy), 10)
        rows = {x["name"]: x["chain"]["state"] for x in (await (await c.get("/api/apps")).json())["apps"]}
        assert rows["late"] == chain.UP_TO_DATE and rows["busy"] == chain.BEHIND
    serve(tmp_path, body)
    # Updated: its commit, of the chain's files alone, pushed.
    subject = git(late, "log", "-1", "--format=%s").strip()
    assert subject.startswith("chain: ") and git(late, "rev-parse", "HEAD").strip() != heads[late]
    assert (late / ".claude/agents/a.md").read_text(encoding="utf-8") == "agent a, two\n"
    assert git(late_remote, "log", "-1", "--format=%s", "master").strip() == subject
    assert git(late, "status", "--porcelain") == ""
    # Untouched: same commit, same files, nothing uncommitted.
    for r in (modified, absent, busy):
        assert git(r, "rev-parse", "HEAD").strip() == heads[r]
        assert tree(r) == trees[r]
        assert git(r, "status", "--porcelain") == ""


@pytest.mark.real_chain
def test_a_git_folder_without_claude_added_absent_installed_from_its_row(tmp_path, monkeypatch):
    root = tmp_path / "chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    commit(root, "chain one")
    monkeypatch.setattr(server, "CHAIN_ROOT", str(root))
    monkeypatch.setattr(server, "CHAIN_PUSH", False)
    chain._chain_cache.clear()
    bare = tmp_path / "bare"
    init(bare)
    write(bare, "README.md", "une application\n")
    commit(bare, "app")

    async def body(c, st, rn):
        r = await post(c, "/api/apps/add", {"path": str(bare)})
        assert r.status == 200
        [row] = (await (await c.get("/api/apps")).json())["apps"]
        assert row["chain"]["state"] == chain.ABSENT and row["open_error"].startswith("pas de dossier docs/features/")
        assert row["feature"] is None and row["questions"] is None
        # Made active, it opens on no feature — said; its install is reachable all the same.
        r = await post(c, "/api/apps/open", {"folder": str(bare)})
        assert (await r.json())["open"] is False
        s = await state_of(c)
        assert s["open"] is False and s["app_name"] == "bare" and s["chain"]["state"] == chain.ABSENT
        assert s["open_error"].startswith("pas de dossier docs/features/")
        r = await post(c, "/api/chain/install", {"folder": str(bare)})
        j = await r.json()
        assert r.status == 200, j
        assert j["chain"]["state"] == chain.UP_TO_DATE and j["result"]["app_commit"]
        [row] = (await (await c.get("/api/apps")).json())["apps"]
        assert row["chain"]["state"] == chain.UP_TO_DATE
    serve(tmp_path, body)
    assert (bare / ".claude" / "CLAUDE.md").is_file()
    assert git(bare, "log", "-1", "--format=%s").startswith("chain: ")


# ------------------------------------------------- runs and applications

def test_a_run_in_one_application_seen_from_another(tmp_path):
    a_root, b_root = tmp_path / "hyrox", tmp_path / "belivo"
    build_app_folder(a_root)
    second_app(b_root)

    async def body(c, st, rn):
        st.open_pair(str(b_root), "g")
        st.open_pair(str(a_root), "f")
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200
        q = rn.watch()
        ev = await asyncio.wait_for(q.get(), 5)
        while ev["type"] != "permission":
            ev = await asyncio.wait_for(q.get(), 5)
        assert ev["app"] == str(a_root)                        # every event names its application
        s = await state_of(c)
        assert s["run"]["status"] != "ended" and s["busy"]["active"] and s["decision"]["source"] == "run"
        # The other application, active: the run is not its own.
        await post(c, "/api/apps/open", {"folder": str(b_root)})
        s = await state_of(c)
        assert s["app_name"] == "belivo" and s["run"] is None and s["decision"]["source"] != "run"
        assert s["busy"]["app_name"] == "hyrox" and not s["busy"]["active"] and s["busy"]["prompt"] == "/1_lexique f"
        assert [p["id"] for p in s["busy"]["permissions"]] == [ev["data"]["id"]]
        assert all(step["state"] != "en cours" for step in s["scan"]["main"])
        # No launch here while it goes: said with where it goes.
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "g"})
        j = await r.json()
        assert r.status == 409 and "« hyrox »" in j["error"] and j["busy"]["app"] == str(a_root)
        assert not rn.is_running(str(b_root))
        # Its card and « Arrêter » act on it from here.
        r = await post(c, "/api/permission", {"id": ev["data"]["id"], "allow": True})
        assert r.status == 200
        r = await post(c, "/api/stop-now", {})
        assert r.status == 200
        assert await rn.wait_ended(str(a_root), 10)
        s = await state_of(c)
        assert s["busy"] is None
        r = await post(c, "/api/stop-now", {})
        assert r.status == 409
        rn.unwatch(q)
    serve(tmp_path, body, script=script_with_permission)


def test_two_runs_never_go_at_once(tmp_path):
    a_root, b_root = tmp_path / "a", tmp_path / "b"
    build_app_folder(a_root)
    second_app(b_root)

    async def body(c, st, rn):
        st.open_pair(str(a_root), "f")
        assert (await post(c, "/api/run", {"command": "1_lexique", "args": "f"})).status == 200
        with pytest.raises(runner_mod.Busy):
            await rn.start(str(b_root), "g", "g", "1_lexique", "g")
        assert sum(1 for x in rn.runs.values() if x.id and x.status != "ended") == 1
        await rn.stop_now(str(a_root))
        await rn.wait_ended(str(a_root), 10)
    serve(tmp_path, body)


# ---------------------------------------------- statistics per application

def test_statistics_per_application_and_the_backfill(tmp_path):
    a_root, b_root = tmp_path / "hyrox", tmp_path / "belivo"
    build_app_folder(a_root)
    second_app(b_root)
    st = State(str(tmp_path / "config.json"))
    st.open_pair(str(a_root), "f")
    st.add_app(str(b_root))
    path = str(tmp_path / "stats.sqlite")
    store = stats.Store(path)
    logs = tmp_path / "old-logs"
    logs.mkdir()
    # r1's log says it ran in a worktree of belivo; r2's history says hyrox;
    # r3 has neither — the first application's, the one the cockpit knew.
    log1 = logs / "r1.jsonl"
    log1.write_text(json.dumps({"type": "SystemMessage", "message": {"data": {
        "cwd": str(b_root / ".claude" / "worktrees" / "g")}}}) + "\n", encoding="utf-8")
    st.add_history(str(a_root), "f", {"command": "/1_lexique f", "outcome": "terminé", "log_path": str(logs / "r2.jsonl"),
                                       "at": "2026-10-06T09:00:00"})
    now = datetime.now().isoformat(timespec="seconds")
    db = sqlite3.connect(path)
    for rid, feat, log in [("r1", "g", str(log1)), ("r2", "f", str(logs / "r2.jsonl")), ("r3", "f", None)]:
        db.execute("INSERT INTO runs (id, feature, work, command, started_at, input_tokens, cache_read_tokens,"
                   " cache_creation_tokens, log_path) VALUES (?,?,?,?,?,10,0,0,?)", (rid, feat, feat, f"/1_lexique {feat}", now, log))
    db.commit()
    db.close()
    assert {r: a for r, a in sqlite3.connect(path).execute("SELECT id, app FROM runs")} == {"r1": None, "r2": None, "r3": None}
    done = server.backfill(store, st, str(tmp_path / "no-logs"))
    assert done["apps"] == 3
    apps_of = dict(sqlite3.connect(path).execute("SELECT id, app FROM runs").fetchall())
    assert apps_of == {"r1": str(b_root), "r2": str(a_root), "r3": str(a_root)}
    assert server.backfill(store, st, str(tmp_path / "no-logs"))["apps"] == 0          # once

    async def body(c, st, rn):
        d = await (await c.get("/api/stats")).json()                           # the active one by default
        assert d["app_name"] == "hyrox" and sorted(r["id"] for r in d["runs"]) == ["r2", "r3"]
        d = await (await c.get("/api/stats?app=*")).json()
        assert d["app"] is None and d["feature"] is None and sorted(r["id"] for r in d["runs"]) == ["r1", "r2", "r3"]
        assert {r["id"]: r["app_name"] for r in d["runs"]} == {"r1": "belivo", "r2": "hyrox", "r3": "hyrox"}
        assert sorted(x["label"] for x in d["by_feature"]) == ["belivo · g", "hyrox · f"]
        r = await c.get("/api/stats/csv?kind=runs&app=*&period=tout")
        assert "application" in (await r.text()).splitlines()[0]
        # A new run is stored with its application.
        rn.client_factory = lambda cwd, cb, **kw: FakeClient(None, cb)
    serve(tmp_path, body, state=st, store=store)


def test_a_new_run_is_stored_with_its_application(tmp_path):
    a_root = tmp_path / "hyrox"
    build_app_folder(a_root)
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    from test_runner import script_quick

    async def body(c, st, rn):
        st.open_pair(str(a_root), "f")
        assert (await post(c, "/api/run", {"command": "1_lexique", "args": "f"})).status == 200
        await rn.wait_ended(str(a_root), 10)
    serve(tmp_path, body, script=script_quick, store=store)
    assert sqlite3.connect(store.path).execute("SELECT app FROM runs").fetchall() == [(str(a_root),)]


# ------------------------------------------------ the diagnostic per application

def test_the_diagnostic_per_application_two_applications_two_results(tmp_path):
    a_root, b_root = tmp_path / "gradle_app", tmp_path / "flutter_app"
    build_app_folder(a_root)
    second_app(b_root)
    (a_root / "gradlew").write_text("", encoding="utf-8")
    (b_root / "pubspec.yaml").write_text("name: b\n", encoding="utf-8")
    calls = []

    def fake(app):
        calls.append(app)
        return diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
    st = State(str(tmp_path / "config.json"))
    st.open_pair(str(b_root), "g")
    st.open_pair(str(a_root), "f")

    async def settle(c):
        for _ in range(300):
            s = await state_of(c)
            if not s["diagnostic_running"]:
                return s
            await asyncio.sleep(0.02)
        raise AssertionError("le diagnostic ne finit pas")

    async def body(c, st, rn):
        s = await settle(c)                                    # the server's opening: the active one's
        assert s["diagnostic"]["app"] == str(a_root)
        await post(c, "/api/apps/open", {"folder": str(b_root)})
        s = await settle(c)                                    # the other one has none: its own runs, once
        assert s["diagnostic"]["app"] == str(b_root)
        await post(c, "/api/apps/open", {"folder": str(a_root)})
        await post(c, "/api/check", {"reason": "ouverture"})
        s = await settle(c)
        assert s["diagnostic"]["app"] == str(a_root)
    serve(tmp_path, body, state=st, diag_runner=fake)
    assert calls == [str(a_root), str(b_root)]                 # one each, never run again
    again = State(st.path)
    da, db_ = again.diagnostic(str(a_root)), again.diagnostic(str(b_root))
    assert da["app"] == str(a_root) and db_["app"] == str(b_root)
    flutter = {r["id"]: r["status"] for r in db_["results"]}
    gradle = {r["id"]: r["status"] for r in da["results"]}
    assert flutter["gradle"] == "skip" and gradle["flutter"] == "skip"     # each its own stack
