"""Cockpit 1.5, §0 — starting, starting again, stopping.

A real server process is started on a free port with its own config, store
and logs — never this machine's — and a second start is made against it.
No chain command runs: the run of the « with a run » case is the fake
client's."""
import asyncio
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

import pytest
from aiohttp.test_utils import TestClient, TestServer

import runner as runner_mod
import server
import startup
from state import State
from test_runner import FakeClient, script_until_interrupted
from test_server import build_app_folder, open_pair, post

COCKPIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def args_for(tmp_path, port):
    return ["--port", str(port), "--config", str(tmp_path / "config.json"), "--stats", str(tmp_path / "s.sqlite"),
            "--journaux", str(tmp_path / "logs")]


@pytest.fixture
def keep_streams(monkeypatch):
    """main() sends stdout and stderr to server.log: put them back after."""
    monkeypatch.setattr(sys, "stdout", sys.stdout)
    monkeypatch.setattr(sys, "stderr", sys.stderr)


def wait_ping(port, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        got = startup.ping(port, timeout=0.5)
        if got:
            return got
        time.sleep(0.2)
    return None


def test_a_second_start_opens_the_page_and_starts_no_second_server(tmp_path, monkeypatch, keep_streams):
    port = free_port()
    first = subprocess.Popen([sys.executable, "server.py", *args_for(tmp_path, port)], cwd=COCKPIT,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        info = wait_ping(port)
        assert info and info["cockpit"] and info["pid"] == first.pid
        opened = []
        monkeypatch.setattr(server, "OPEN_BROWSER", opened.append)
        t0 = time.time()
        assert server.main([*args_for(tmp_path, port), "--ouvrir"]) == 0
        assert time.time() - t0 < 5                                   # returned at once: no server of its own
        assert opened == [f"http://127.0.0.1:{port}/"]
        assert startup.ping(port)["pid"] == first.pid                 # still the first one answering
        log = (tmp_path / "logs" / "server.log").read_text(encoding="utf-8")
        assert "aucun second serveur" in log
        # « Arrêter le cockpit », no run going: the server goes.
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/shutdown", data=b"{}",
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            assert json.loads(r.read())["ok"] is True
        assert first.wait(timeout=20) == 0
        assert startup.ping(port, timeout=0.5) is None
        log = (tmp_path / "logs" / "server.log").read_text(encoding="utf-8")
        assert "Arrêt du cockpit demandé depuis la page" in log and "Le cockpit s'arrête." in log
    finally:
        if first.poll() is None:
            first.kill()


PYTHONW = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")


@pytest.mark.skipif(not os.path.isfile(PYTHONW), reason="pythonw absent")
def test_started_by_pythonw_it_runs_without_a_console_and_logs_to_its_file(tmp_path):
    port = free_port()
    p = subprocess.Popen([PYTHONW, "server.py", *args_for(tmp_path, port)], cwd=COCKPIT)
    try:
        assert wait_ping(port)["pid"] == p.pid
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/shutdown", data=b"{}",
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10).read()
        assert p.wait(timeout=20) == 0
        log = (tmp_path / "logs" / "server.log").read_text(encoding="utf-8")
        assert "sans console" in log and f"Cockpit : http://127.0.0.1:{port}/" in log
    finally:
        if p.poll() is None:
            p.kill()


def test_a_port_taken_by_another_program_is_said_and_starts_nothing(tmp_path, monkeypatch, keep_streams):
    port = free_port()
    other = socket.socket()
    other.bind(("127.0.0.1", port))
    other.listen()
    try:
        monkeypatch.setattr(startup, "PING_TIMEOUT", 0.3)
        monkeypatch.setattr(server, "OPEN_BROWSER", lambda url: pytest.fail("no page to open"))
        assert server.main(args_for(tmp_path, port) + ["--ouvrir"]) == 1
        log = (tmp_path / "logs" / "server.log").read_text(encoding="utf-8")
        assert f"Le port {port} est pris par un autre programme" in log
    finally:
        other.close()


def quit_client(tmp_path, body):
    app_root = tmp_path / "app"
    build_app_folder(app_root)
    state = State(str(tmp_path / "config.json"))
    rn = runner_mod.Runner(client_factory=lambda cwd, cut, **kw: FakeClient(script_until_interrupted, cut),
                           on_end=server.make_on_end(state), mode_getter=lambda: state.mode)
    quits = []
    app = server.make_app(state, rn, picker=lambda i: str(app_root), on_quit=lambda: quits.append(1))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            await open_pair(c, app_root)
            return await body(c, rn, app_root, quits)
    return asyncio.run(go())


def test_stopping_the_cockpit_without_a_run(tmp_path):
    async def body(c, rn, app_root, quits):
        r = await post(c, "/api/shutdown", {})
        assert r.status == 200 and (await r.json()) == {"ok": True, "stopped": []}
        await asyncio.sleep(0.5)
        assert quits == [1]
    quit_client(tmp_path, body)


def test_stopping_the_cockpit_with_a_run_asks_then_stops_the_run(tmp_path):
    async def body(c, rn, app_root, quits):
        r = await post(c, "/api/run", {"command": "8_code", "args": "f"})
        assert r.status == 200
        await asyncio.sleep(0.2)
        r = await post(c, "/api/shutdown", {})
        assert r.status == 409 and (await r.json()) == {"running": True, "prompt": "/8_code f"}
        await asyncio.sleep(0.5)
        assert quits == [] and rn.is_running(str(app_root))          # asked, nothing stopped
        r = await post(c, "/api/shutdown", {"confirm": True})
        assert r.status == 200
        got = await r.json()
        assert got["stopped"] == [{"prompt": "/8_code f", "ended": True}]
        run = rn.current(str(app_root))
        assert run.status == "ended" and run.outcome == "interrompu"
        await asyncio.sleep(0.5)
        assert quits == [1]
    quit_client(tmp_path, body)


@pytest.mark.skipif(os.name != "nt", reason="Windows only")
def test_without_a_console_every_child_starts_without_a_window(monkeypatch):
    seen = []

    class Stop(Exception):
        pass

    def record(self, *args, **kwargs):
        seen.append(kwargs.get("creationflags"))
        raise Stop()

    monkeypatch.setattr(subprocess.Popen, "__init__", record)
    monkeypatch.setattr(subprocess.Popen, "_cockpit_quiet", False, raising=False)
    assert startup.hide_child_consoles() is True
    for kw in ({}, {"creationflags": 0}, {"creationflags": 0x200}):
        with pytest.raises(Stop):
            subprocess.Popen(["x"], **kw)
    assert seen == [subprocess.CREATE_NO_WINDOW, subprocess.CREATE_NO_WINDOW, 0x200]
    assert startup.hide_child_consoles() is False                     # once


def test_the_log_is_appended_and_rotated(tmp_path, keep_streams, monkeypatch):
    p = tmp_path / "logs" / "server.log"
    p.parent.mkdir()
    p.write_text("x" * 50, encoding="utf-8")
    monkeypatch.setattr(startup, "LOG_MAX", 10)
    f = startup.open_log(str(p))
    print("une ligne")
    f.flush()
    assert (tmp_path / "logs" / "server.log.1").read_text(encoding="utf-8") == "x" * 50
    assert p.read_text(encoding="utf-8") == "une ligne\n"
    sys.stdout = sys.__stdout__ or sys.stdout
    f.close()
