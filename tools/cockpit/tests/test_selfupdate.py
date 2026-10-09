"""1.14 — « Mettre à jour le cockpit » and « Récupérer », through the
server: agent-chain behind GitHub → the notice and its commits, at start and
when the home screen opens; the update pulls; requirements.txt changed → pip
(a fake); the restart — a new server that answers (the old one exits), one
that never does and one that dies (the old one stays, and says why);
refused during a run, on an uncommitted overlapping file, when diverged.
« Récupérer »: behind → pulled, the chain block computed again; its
refusals. The relay itself: a server on its trial port takes the cockpit's
port once it is free. Bare repositories play GitHub; no chain command runs —
the SDK client is a fake."""
import asyncio
import json
import os
import socket
import sys
import threading
import time

import pytest
from aiohttp.test_utils import TestClient, TestServer

import chain
import runner as runner_mod
import selfupdate
import server
import startup
import sync
from selfupdateworld import chain_world, fakes, is_alive  # noqa: F401
from state import State
from syncworld import app_world, change, head
from test_chain import git, write
from test_runner import FakeClient, script_quick, script_until_interrupted
from test_server import post


def listed(tmp_path, *folders):
    st = State(str(tmp_path / "config.json"))
    for f in folders:
        st.add_app(str(f))
        st.open_pair(str(f), "f")
    if folders:
        st.activate(str(folders[0]))
    return st


def serve(tmp_path, body, state=None, script=script_quick):
    """The server, with « Arrêter le cockpit » recorded: `quit` holds how
    many times the server asked to exit."""
    st = state or State(str(tmp_path / "config.json"))
    quit = []

    def factory(cwd, can_use_tool, **kw):
        return FakeClient(script, can_use_tool)
    rn = runner_mod.Runner(client_factory=factory, on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"))
    app = server.make_app(st, rn, on_quit=lambda: quit.append(time.monotonic()))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            return await body(c, st, rn, quit)
    return asyncio.run(go())


async def state_of(c):
    return await (await c.get("/api/state")).json()


async def wait_for_state(c, pred, timeout=20.0):
    for _ in range(int(timeout / 0.1)):
        s = await state_of(c)
        if pred(s):
            return s
        await asyncio.sleep(0.1)
    raise AssertionError("jamais arrivé")


async def update(c):
    r = await post(c, "/api/cockpit/update", {})
    return r.status, await r.json()


@pytest.fixture
def here_behind(tmp_path, monkeypatch):
    """agent-chain behind GitHub by two commits; the cockpit runs from `here`."""
    remote, here, other = chain_world(tmp_path)
    change(other, "tools/cockpit/x.py", "cockpit 2\n", "cockpit : le bouton", push=True)
    change(other, ".claude/agents/a.md", "agent a, two\n", "chaîne : l'agent a", push=True)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    return remote, here, other


# ------------------------------------------------------------ the notice

def test_notice_and_its_commits_when_the_home_screen_opens(tmp_path, monkeypatch, here_behind):
    _, here, other = here_behind
    monkeypatch.setattr(server, "SYNC_CHAIN_ON_HOME", True)
    monkeypatch.setattr(server, "CHAIN_HOME_EVERY", 0.0)
    before = head(here)

    async def body(c, st, rn, quit):
        s = await state_of(c)
        assert s["chain_sync"]["cockpit"] is None            # nothing fetched yet
        await c.get("/api/apps")                               # the home screen opens
        s = await wait_for_state(c, lambda s: (s["chain_sync"]["cockpit"] or {}).get("state") == "disponible")
        ck = s["chain_sync"]["cockpit"]
        assert ck["count"] == 2 and ck["version"] == server.VERSION and ck["started"] == before[:7]
        assert [x.split(" ", 1)[1] for x in ck["subjects"]] == ["chaîne : l'agent a", "cockpit : le bouton"]
        assert (await (await c.get("/api/apps")).json())["chain_sync"]["cockpit"]["state"] == "disponible"
        assert (await (await c.get("/api/cockpit")).json())["cockpit"]["count"] == 2
    serve(tmp_path, body)
    assert head(here) == before                                # a fetch, never a pull


def test_pulled_at_start_then_the_update_restarts_without_pulling(tmp_path, monkeypatch, here_behind, fakes):
    _, here, other = here_behind
    monkeypatch.setattr(server, "SYNC_CHAIN_AT_START", True)
    new = head(other)

    async def body(c, st, rn, quit):
        s = await wait_for_state(c, lambda s: s["chain_sync"]["notice"])
        assert s["chain_sync"]["notice"] == server.CHAIN_RESTART and "Mettre à jour le cockpit" in server.CHAIN_RESTART
        assert head(here) == new
        ck = s["chain_sync"]["cockpit"]
        assert ck["state"] == "récupérée" and ck["count"] == 2
        code, r = await update(c)
        assert code == 200 and r["restarting"], r
        assert not any("git pull" in x for x in r["steps"])
        await asyncio.sleep(0.6)
        assert len(quit) == 1
    serve(tmp_path, body)


# ------------------------------------------------------------ the update

def test_update_pulls_then_restarts_and_the_old_server_exits(tmp_path, monkeypatch, here_behind, fakes):
    _, here, other = here_behind
    _, a, _ = app_world(tmp_path, "app")
    monkeypatch.setattr(server, "LAUNCH_ARGS", ["--config", "c.json"])

    async def body(c, st, rn, quit):
        port = c.server.port
        code, r = await update(c)
        assert code == 200 and r["ok"] and r["restarting"], r
        assert r["steps"][0] == "git pull --ff-only — 2 commits récupérés"
        assert r["steps"][-1].startswith("nouveau serveur prêt — cockpit 9.9")
        assert r["old_pid"] == os.getpid() and r["new_pid"] == fakes.procs[0].pid
        # The new server: on the cockpit's port, a trial port first, the arguments kept.
        sp = fakes.spawned[0]
        assert sp["port"] == port and sp["trial"] != port and sp["extra"] == ["--config", "c.json"]
        assert fakes.server_calls()[0][:4] == ["--port", str(port), "--relais", str(sp["trial"])]
        # The old one exits once the new one answered — and nothing launches meanwhile.
        await asyncio.sleep(0.6)
        assert len(quit) == 1
        r2 = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r2.status == 409 and "le cockpit se met à jour" in (await r2.json())["error"]
    serve(tmp_path, body, state=listed(tmp_path, a))
    assert head(here) == head(other)
    assert fakes.pip_calls() == []                              # requirements.txt did not change


def test_requirements_changed_then_pip(tmp_path, monkeypatch, here_behind, fakes):
    _, here, other = here_behind
    change(other, "tools/cockpit/requirements.txt", "aiohttp>=3.9,<4\nrich>=13\n", "cockpit : rich", push=True)

    async def body(c, st, rn, quit):
        code, r = await update(c)
        assert code == 200 and r["restarting"], r
        assert "pip install --user -r tools/cockpit/requirements.txt — fait" in r["steps"]
    serve(tmp_path, body)
    calls = fakes.pip_calls()
    assert calls == [["install", "--user", "-r", os.path.join(str(here), "tools", "cockpit", "requirements.txt")]]


def test_pip_fails_then_stops_with_its_error(tmp_path, monkeypatch, here_behind, fakes):
    _, here, other = here_behind
    change(other, "tools/cockpit/requirements.txt", "aiohttp>=9\n", "cockpit : aiohttp 9", push=True)
    fakes.pip_fails()

    async def body(c, st, rn, quit):
        code, r = await update(c)
        assert code == 409 and r["step"] == "pip"
        assert "pip a échoué (code 1)" in r["error"] and "aiohttp>=9" in r["error"]
        assert fakes.spawned == [] and quit == []
        # Pulled all the same: the cockpit says so, and the button tries again.
        assert r["cockpit"]["state"] == "récupérée" and r["cockpit"]["error"] == r["error"]
        fakes.monkeypatch.setenv("FAKE_PIP_CODE", "0")
        code, r = await update(c)
        assert code == 200 and r["restarting"]
    serve(tmp_path, body)
    assert len(fakes.pip_calls()) == 2


def test_new_server_never_answers_the_old_one_stays(tmp_path, monkeypatch, here_behind, fakes):
    from selfupdateworld import SILENT
    fakes.new_server(SILENT)
    monkeypatch.setattr(selfupdate, "RESTART_WAIT", 2.0)

    async def body(c, st, rn, quit):
        code, r = await update(c)
        assert code == 409 and r["step"] == "restart"
        assert "n'a pas répondu en 2 s" in r["error"] and "continue sur l'ancienne version" in r["error"]
        p = fakes.procs[0]
        assert p.poll() is not None                            # ended, never left behind
        assert quit == []
        ping = await (await c.get("/api/ping")).json()
        assert ping["pid"] == os.getpid() and not ping["restarting"] and ping["error"] == r["error"]
        # Nothing stays blocked: a launch goes again.
        r2 = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert "se met à jour" not in (await r2.json()).get("error", "")
    serve(tmp_path, body)


def test_new_server_dies_and_its_error_is_said(tmp_path, monkeypatch, here_behind, fakes):
    from selfupdateworld import DIES
    fakes.new_server(DIES)

    async def body(c, st, rn, quit):
        t0 = time.monotonic()
        code, r = await update(c)
        assert code == 409 and r["step"] == "restart"
        assert time.monotonic() - t0 < 20                     # it did not wait the whole delay
        assert "il s'est arrêté, code 1" in r["error"] and "aiohttp_nouveau" in r["error"]
        assert quit == []
    serve(tmp_path, body)


# ------------------------------------------------------------ refusals

def test_refused_during_a_run(tmp_path, here_behind, fakes):
    _, here, other = here_behind
    _, a, _ = app_world(tmp_path, "app")
    before = head(here)

    async def body(c, st, rn, quit):
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200
        code, out = await update(c)
        assert code == 409 and out["busy"] and "une commande tourne" in out["error"] and "/1_lexique f" in out["error"]
        await post(c, "/api/stop-now", {})
        await rn.wait_ended(str(a), 10)
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_until_interrupted)
    assert head(here) == before and fakes.spawned == []


def test_refused_on_an_uncommitted_overlapping_file(tmp_path, here_behind, fakes):
    _, here, other = here_behind
    write(here, "tools/cockpit/x.py", "mon essai\n")
    before = head(here)

    async def body(c, st, rn, quit):
        code, r = await update(c)
        assert code == 409 and r["files"] == ["tools/cockpit/x.py"]
        assert "écraserait des fichiers non commités ici : tools/cockpit/x.py" in r["error"]
    serve(tmp_path, body)
    assert head(here) == before and fakes.spawned == []
    assert (here / "tools/cockpit/x.py").read_text() == "mon essai\n"


def test_refused_when_diverged_and_reconcile_offered(tmp_path, here_behind, fakes):
    _, here, other = here_behind
    change(here, "notes.md", "ici\n")
    before = head(here)

    async def body(c, st, rn, quit):
        code, r = await update(c)
        assert code == 409 and r["reconcile"] and "Divergé" in r["error"] and "Réconcilier" in r["error"]
        assert r["cockpit"]["diverged"]
    serve(tmp_path, body)
    assert head(here) == before and fakes.spawned == []


def test_nothing_to_update(tmp_path, monkeypatch, fakes):
    _, here, _ = chain_world(tmp_path)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))

    async def body(c, st, rn, quit):
        code, r = await update(c)
        assert code == 200 and r["nothing"] and r["message"] == "Le cockpit est à jour : rien à récupérer."
        assert r["cockpit"]["state"] == "à jour"
    serve(tmp_path, body)
    assert fakes.spawned == []


# ------------------------------------------------------------ the relay

def _listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.listen(5)
    return s


def test_relay_answers_on_its_trial_port_then_takes_the_port(tmp_path):
    """The new server's side: on the trial port at once; the cockpit's port
    as soon as the old server lets it go; the trial port closed."""
    old = _listener()                                  # the old server, still on the port
    port, trial = old.getsockname()[1], selfupdate.free_port()
    st = State(str(tmp_path / "config.json"))
    rn = runner_mod.Runner(client_factory=lambda *a, **k: None, log_dir=str(tmp_path / "logs"))
    app = server.make_app(st, rn)
    box, done = {"event": None}, threading.Event()
    loop = asyncio.new_event_loop()

    def run():
        try:
            loop.run_until_complete(server.serve(app, port, f"http://127.0.0.1:{port}/", False, box, relay=trial))
        finally:
            done.set()
    threading.Thread(target=run, daemon=True).start()
    try:
        got = None
        for _ in range(100):
            got = startup.ping(trial, timeout=0.5)
            if got:
                break
            time.sleep(0.1)
        assert got and got["pid"] == os.getpid()
        old.close()                                    # the old server exits
        for _ in range(100):
            if startup.ping(port, timeout=0.5):
                break
            time.sleep(0.1)
        assert startup.ping(port, timeout=1)["cockpit"]
        for _ in range(50):
            if not startup.ping(trial, timeout=0.3):
                break
            time.sleep(0.1)
        assert startup.ping(trial, timeout=0.3) is None
    finally:
        old.close()
        if box["event"] is not None:
            loop.call_soon_threadsafe(box["event"].set)
        done.wait(10)


def test_server_command_is_lancer_bat_s(monkeypatch):
    monkeypatch.setattr(selfupdate.shutil, "which", lambda name: r"C:\Python\pythonw.exe" if name == "pythonw" else None)
    cmd, console = selfupdate.server_command(8765, 50123, ["--config", "c.json"])
    assert cmd == [r"C:\Python\pythonw.exe", selfupdate.SERVER, "--port", "8765", "--relais", "50123", "--config", "c.json"]
    assert not console and "--ouvrir" not in cmd
    monkeypatch.setattr(selfupdate.shutil, "which", lambda name: None)
    monkeypatch.setattr(selfupdate.sys, "executable", str(os.path.join("nowhere", "python.exe")))
    cmd, console = selfupdate.server_command(8765, 50123)
    assert console and cmd[0].endswith("python.exe")


# ------------------------------------------------------------ « Récupérer »

@pytest.mark.real_chain
def test_recuperer_behind_pulled_and_the_chain_block_updated(tmp_path, monkeypatch):
    _, here, _ = chain_world(tmp_path)
    _, a, b = app_world(tmp_path, "app")
    # The other computer installed the chain, and pushed it.
    chain.install(str(b), str(here), push=False)
    git(b, "push", "-q")
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    monkeypatch.setattr(server, "chain_state", lambda f: chain.state(f, str(here)))

    async def body(c, st, rn, quit):
        rows = (await (await c.get("/api/apps")).json())["apps"]
        assert rows[0]["sync"]["state"] == sync.BEHIND and rows[0]["chain"]["state"] == chain.ABSENT
        r = await post(c, "/api/sync/pull", {"folder": str(a)})
        data = await r.json()
        assert r.status == 200 and data["ok"] and data["pulled"] == 1
        assert data["sync"]["state"] == sync.UP_TO_DATE and data["chain"]["state"] == chain.UP_TO_DATE
        rows = (await (await c.get("/api/apps")).json())["apps"]
        assert rows[0]["sync"]["state"] == sync.UP_TO_DATE and rows[0]["chain"]["state"] == chain.UP_TO_DATE
        assert (await state_of(c))["chain"]["state"] == chain.UP_TO_DATE
    serve(tmp_path, body, state=listed(tmp_path, a))
    assert head(a) == head(b)


def test_recuperer_refusals(tmp_path):
    _, a, b = app_world(tmp_path, "app")
    change(b, "README.md", "B\n", push=True)
    write(a, "README.md", "mon brouillon\n")                  # uncommitted, and GitHub changed it
    _, d, d2 = app_world(tmp_path, "diverged")
    change(d2, "README.md", "B\n", push=True)
    change(d, "notes.md", "ici\n")
    _, u, _ = app_world(tmp_path, "uptodate")

    async def body(c, st, rn, quit):
        r = await post(c, "/api/sync/pull", {"folder": str(a)})
        data = await r.json()
        assert r.status == 409 and data["files"] == ["README.md"] and "non commités ici : README.md" in data["error"]
        r = await post(c, "/api/sync/pull", {"folder": str(d)})
        data = await r.json()
        assert r.status == 409 and data["reconcile"] and "Réconcilier" in data["error"]
        r = await post(c, "/api/sync/pull", {"folder": str(u)})
        assert r.status == 409 and "rien à récupérer : à jour avec github" in (await r.json())["error"]
    serve(tmp_path, body, state=listed(tmp_path, a, d, u))
    assert (a / "README.md").read_text() == "mon brouillon\n"


def test_recuperer_refused_during_a_run_there(tmp_path):
    _, a, b = app_world(tmp_path, "app")
    change(b, "README.md", "B\n", push=True)
    before = head(a)

    async def body(c, st, rn, quit):
        # Pulled before the launch (§2): GitHub moves on again during the run.
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200
        change(b, "README.md", "C\n", push=True)
        r = await post(c, "/api/sync/pull", {"folder": str(a)})
        assert r.status == 409 and "une commande tourne" in (await r.json())["error"]
        await post(c, "/api/stop-now", {})
        await rn.wait_ended(str(a), 10)
    serve(tmp_path, body, state=listed(tmp_path, a), script=script_until_interrupted)
    assert head(a) != before                                  # the launch's own pull
