"""1.14 — « Mettre à jour le cockpit » in a temporary folder: agent-chain on
a bare repository playing GitHub, two clones playing the two computers; the
new server a fake process — one that answers on its trial port, one that
never does, one that dies at once —; pip a fake that records its arguments.
Nothing reaches the real GitHub, the real agent-chain or the real pip."""
import json
import os
import subprocess
import sys

import pytest

import selfupdate
import server

ANSWERS = r'''
import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
trial = int(sys.argv[sys.argv.index("--relais") + 1])
with open(os.environ["FAKE_SERVER_LOG"], "a", encoding="utf-8") as f:
    f.write(json.dumps(sys.argv[1:]) + "\n")
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"cockpit": True, "version": "9.9", "pid": os.getpid()}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass
HTTPServer(("127.0.0.1", trial), H).serve_forever()
'''

SILENT = r'''
import time
time.sleep(120)
'''

DIES = r'''
import sys
sys.stderr.write("Traceback (most recent call last):\nModuleNotFoundError: No module named 'aiohttp_nouveau'\n")
sys.exit(1)
'''

PIP = r'''
import json, os, sys
with open(os.environ["FAKE_PIP_LOG"], "a", encoding="utf-8") as f:
    f.write(json.dumps(sys.argv[1:]) + "\n")
code = int(os.environ.get("FAKE_PIP_CODE", "0"))
if code:
    sys.stderr.write("ERROR: Could not find a version that satisfies the requirement aiohttp>=9\n")
sys.exit(code)
'''


def script(tmp_path, name, text):
    p = tmp_path / "fakes" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return str(p)


def lines(path):
    try:
        with open(path, encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]
    except OSError:
        return []


class Fakes:
    """The new server and pip, faked; every process started, ended at the
    test's end."""

    def __init__(self, tmp_path, monkeypatch):
        self.tmp = tmp_path
        self.server_log = str(tmp_path / "fakes" / "server.jsonl")
        self.pip_log = str(tmp_path / "fakes" / "pip.jsonl")
        monkeypatch.setenv("FAKE_SERVER_LOG", self.server_log)
        monkeypatch.setenv("FAKE_PIP_LOG", self.pip_log)
        monkeypatch.setattr(selfupdate, "PIP_COMMAND", [sys.executable, script(tmp_path, "pip.py", PIP)])
        self.monkeypatch = monkeypatch
        self.procs = []
        self.spawned = []
        self.new_server(ANSWERS)

    def new_server(self, text):
        """The new server: this script, started by the real selfupdate.spawn
        — detached, its stderr in relais.log — in place of server.py."""
        path = script(self.tmp, f"server{len(self.spawned)}.py", text)

        def command(port, trial, extra=()):
            return [sys.executable, path, "--port", str(port), "--relais", str(trial), *extra], False

        def spawn(port, trial, extra=(), log_dir=None):
            self.spawned.append({"port": port, "trial": trial, "extra": list(extra), "log_dir": log_dir})
            p = selfupdate.spawn(port, trial, extra, log_dir)
            self.procs.append(p)
            return p
        self.monkeypatch.setattr(selfupdate, "server_command", command)
        self.monkeypatch.setattr(server, "SPAWN_SERVER", spawn)

    def pip_fails(self):
        self.monkeypatch.setenv("FAKE_PIP_CODE", "1")

    def pip_calls(self):
        return lines(self.pip_log)

    def server_calls(self):
        return lines(self.server_log)

    def end(self):
        for p in self.procs:
            if p.poll() is None:
                p.kill()
                try:
                    p.wait(5)
                except subprocess.TimeoutExpired:
                    pass


@pytest.fixture
def fakes(tmp_path, monkeypatch):
    f = Fakes(tmp_path, monkeypatch)
    yield f
    f.end()


def chain_files():
    """agent-chain's files: the chain, and the cockpit's requirements."""
    from test_chain import CHAIN_FILES
    files = dict(CHAIN_FILES)
    files["tools/cockpit/requirements.txt"] = "aiohttp>=3.9,<4\n"
    files["tools/cockpit/server.py"] = 'VERSION = "1.14"\n'
    return files


def chain_world(tmp_path):
    """agent-chain on GitHub and on two computers — `here`, where the
    cockpit runs, and `other`, where the chain moves on."""
    import chain
    from syncworld import world
    remote, here, other = world(tmp_path / "agent-chain", chain_files())
    chain._chain_cache.clear()
    chain._behind_cache.clear()
    chain._older_cache.clear()
    return remote, here, other


def is_alive(pid):
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
