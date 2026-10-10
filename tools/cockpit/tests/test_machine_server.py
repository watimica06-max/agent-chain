"""1.16 — « État de l'ordinateur » through the server: each rule of §2, what
it stops and what it does not; the repairs of §3 against fakes — a refused
one included —; the server's own restart, by « Redémarrer le cockpit », by
itself when nothing goes, and by lancer.bat finding an older server. GitHub
is a bare repository in a temporary folder; the computer is the fake one
(machinefakes.py); no chain command runs, no real login is touched."""
import asyncio
import json
import os
import subprocess
import time

import pytest
from aiohttp.test_utils import TestClient, TestServer

import diagnostic
import installs
import machine
import runner as runner_mod
import selfupdate
import server
import startup
from selfupdateworld import chain_world
from selfupdateworld import fakes as _fakes  # noqa: F401
from state import State
from syncworld import app_world, change, head, offline
from test_mode_diagnostic import ALL_GOOD, fake_exec
from test_runner import FakeClient, script_quick, script_until_interrupted
from test_server import post
from test_sync_server import wait_for


def listed(tmp_path, *folders):
    st = State(str(tmp_path / "config.json"))
    for f in folders:
        st.add_app(str(f))
        st.open_pair(str(f), "f")
    if folders:
        st.activate(str(folders[0]))
    return st


def serve(tmp_path, body, state=None, script=script_quick):
    st = state or State(str(tmp_path / "config.json"))
    quit = []

    def factory(cwd, can_use_tool, **kw):
        return FakeClient(script, can_use_tool)
    rn = runner_mod.Runner(client_factory=factory, on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"))
    app = server.make_app(st, rn, on_quit=lambda: quit.append(time.monotonic()))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            c.app_ = app
            return await body(c, st, rn, quit)
    return asyncio.run(go())


async def run(c, command="1_lexique"):
    r = await post(c, "/api/run", {"command": command, "args": "f"})
    return r.status, await r.json()


async def ended(rn, folder):
    await wait_for(lambda: not rn.is_running(str(folder)))


@pytest.fixture
def fakes(_fakes, monkeypatch):
    """1.14's fake new server; 1.16's restart hands it the environment
    Windows has now — recorded here."""
    spawn = server.SPAWN_SERVER
    _fakes.envs = []

    def with_env(port, trial, extra=(), log_dir=None, env=None):
        _fakes.envs.append(env)
        return spawn(port, trial, extra, log_dir)
    monkeypatch.setattr(server, "SPAWN_SERVER", with_env)
    return _fakes


@pytest.fixture
def chain_root(tmp_path, monkeypatch):
    """agent-chain: a scratch clone, never this computer's."""
    _, here, _ = chain_world(tmp_path)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    return here


@pytest.fixture
def global_git(tmp_path, monkeypatch):
    """git's global configuration: a file of the test, never this computer's."""
    p = tmp_path / "gitconfig-global"
    p.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(p))
    return p


# ------------------------------------------------------------ §2, what blocks and what does not

def test_claude_logged_out_blocks_every_launch_then_a_login_lets_it_go(tmp_path, chain_root, fake_machine):
    _, a, _ = app_world(tmp_path, "app")
    fake_machine.logged_in = False

    async def body(c, st, rn, quit):
        code, r = await run(c)
        assert code == 409 and "Claude Code n'est pas connecté sur cet ordinateur" in r["error"]
        assert "Paramètres → État de l'ordinateur" in r["error"]
        assert r["machine"][0]["id"] == "claude_login" and r["machine"][0]["repair"]["label"] == "Se connecter à Claude"
        assert not rn.is_running(str(a))
        # The summary the badge shows.
        s = await (await c.get("/api/state")).json()
        assert s["machine_summary"]["level"] == "block"
        fake_machine.logged_in = True
        code, r = await run(c)
        assert code == 200, r
        await ended(rn, a)
    serve(tmp_path, body, listed(tmp_path, a))


def test_cli_below_the_sdk_minimum_blocks_launches(tmp_path, chain_root, fake_machine):
    _, a, _ = app_world(tmp_path, "app")
    fake_machine.version = "1.0.2 (Claude Code)"

    async def body(c, st, rn, quit):
        code, r = await run(c)
        assert code == 409 and "sous le minimum du SDK (2.0.0)" in r["error"]
    serve(tmp_path, body, listed(tmp_path, a))


def test_github_credentials_missing_block_what_pushes_never_a_launch(tmp_path, chain_root, fake_machine):
    _, a, _ = app_world(tmp_path, "app")
    change(a, "README.md", "ici\n", "un commit d'ici")                   # « non envoyé »
    fake_machine.github = "credentials"

    async def body(c, st, rn, quit):
        code, r = await run(c)
        assert code == 200, r                                             # a launch: notified only
        await ended(rn, a)
        for path, data in (("/api/sync/push", {"folder": str(a)}), ("/api/chain/install", {"folder": str(a)}),
                           ("/api/answers/send", {"folder": str(a)}), ("/api/chain/install-all", {})):
            resp = await post(c, path, data)
            r = await resp.json()
            assert resp.status == 409 and r["error"].startswith("GitHub — identifiants"), (path, r)
            assert r["machine"][0]["repair"]["id"] == "github_login"
    serve(tmp_path, body, listed(tmp_path, a))


def test_chain_install_refused_while_github_is_unreachable(tmp_path, chain_root):
    _, a, _ = app_world(tmp_path, "app")
    offline(a)

    async def body(c, st, rn, quit):
        resp = await post(c, "/api/chain/install", {"folder": str(a)})
        r = await resp.json()
        assert resp.status == 409 and r["error"].startswith(server.OFFLINE_INSTALL)
        assert r["sync"]["state"] == "GitHub injoignable"
        # A launch still goes, with its notice (today).
        code, r = await run(c)
        assert code == 200, r
        await ended(rn, a)
    serve(tmp_path, body, listed(tmp_path, a))


def test_identity_missing_blocks_anything_that_commits(tmp_path, chain_root, fake_machine):
    _, a, _ = app_world(tmp_path, "app")
    fake_machine.identity = "missing"

    async def body(c, st, rn, quit):
        code, r = await run(c)
        assert code == 409 and r["machine"][0]["id"] == "git_identity"
        for path, data in (("/api/answers/send", {"folder": str(a)}), ("/api/chain/install", {"folder": str(a)}),
                           ("/api/deploy/profile", {"targets": []})):
            resp = await post(c, path, data)
            assert resp.status == 409 and (await resp.json())["error"].startswith("git — identité des commits"), path
        # Guessed by git: said, never a block.
        fake_machine.identity = "guessed"
        code, r = await run(c)
        assert code == 200, r
        await ended(rn, a)
    serve(tmp_path, body, listed(tmp_path, a))


def test_java_blocks_batir_and_the_deploy_screen_only(tmp_path, chain_root):
    _, a, _ = app_world(tmp_path, "app", commands=("1_lexique", "batir"))
    st = listed(tmp_path, a)
    st.set_diagnostic(diagnostic.run_diagnostic(str(a), fake_exec(dict(ALL_GOOD, java=FileNotFoundError("java introuvable")))),
                      app=str(a))

    async def body(c, st, rn, quit):
        code, r = await run(c, "batir")
        assert code == 409 and r["error"].startswith("Java : java introuvable")
        resp = await post(c, "/api/deploy/start", {"choice": {}})
        assert resp.status == 409 and (await resp.json())["machine"][0]["id"] == "java"
        code, r = await run(c)
        assert code == 200, r
        await ended(rn, a)
    serve(tmp_path, body, st)


def test_a_diverged_application_blocks_its_launch_as_today(tmp_path, chain_root):
    _, a, b = app_world(tmp_path, "app")
    change(b, "README.md", "B\n", "là-bas", push=True)
    change(a, "README.md", "A\n", "ici")

    async def body(c, st, rn, quit):
        code, r = await run(c)
        assert code == 409 and "Divergé" in r["error"] and r["sync_refused"]["reconcile"]
    serve(tmp_path, body, listed(tmp_path, a))


# ------------------------------------------------------------ the view, its routes

def test_check_route_report_and_install_mode(tmp_path, chain_root, fake_machine):
    _, a, _ = app_world(tmp_path, "app")
    fake_machine.identity = "guessed"

    async def body(c, st, rn, quit):
        r = await (await post(c, "/api/machine/check", {})).json()
        ids = [x["id"] for x in r["machine"]["items"]]
        for want in ("server", "chain", "python", "claude_cli", "claude_login", "git", "git_identity", "gcm", "github",
                     "github_reach", "longpaths", "java", "gradle", "flutter", "adb", "sdkmanager", "android_sdk",
                     "emulator", "scrcpy"):
            assert want in ids, want
        k = machine.key(str(a))
        assert {f"app:{k}:github", f"app:{k}:chain", f"app:{k}:build", f"app:{k}:longpaths"} <= set(ids)
        assert r["machine"]["at"] and r["machine"]["summary"]["level"] == "warn" and r["install_mode"] == "demander"
        g = await (await c.get("/api/machine")).json()
        assert g["machine"]["summary"] == r["machine"]["summary"]
        resp = await post(c, "/api/install-mode", {"mode": "rapide"})
        assert (await resp.json())["install_mode"] == "rapide" and st.install_mode == "rapide"
        assert State(str(tmp_path / "config.json")).install_mode == "rapide"
        resp = await post(c, "/api/install-mode", {"mode": "toujours"})
        assert resp.status == 400
    serve(tmp_path, body, listed(tmp_path, a))


def test_repairs_identity_and_longpaths(tmp_path, chain_root, fake_machine, global_git):
    _, a, _ = app_world(tmp_path, "app")
    subprocess.run(["git", "-C", str(a), "config", "--local", "--unset", "core.longpaths"], capture_output=True)

    async def body(c, st, rn, quit):
        resp = await post(c, "/api/machine/repair", {"id": "identity", "args": {"name": "Po", "email": "pas-un-mail"}})
        assert resp.status == 400
        resp = await post(c, "/api/machine/repair", {"id": "identity", "args": {"name": "Product Owner",
                                                                               "email": "po@example.com"}})
        assert resp.status == 200, await resp.text()
        text = global_git.read_text(encoding="utf-8")
        assert "name = Product Owner" in text and "email = po@example.com" in text
        resp = await post(c, "/api/machine/repair", {"id": "longpaths", "args": {"folder": str(a)}})
        assert resp.status == 200
        assert subprocess.run(["git", "-C", str(a), "config", "--local", "--get", "core.longpaths"],
                              capture_output=True, text=True).stdout.strip() == "true"
        resp = await post(c, "/api/machine/repair", {"id": "longpaths", "args": {"folder": str(tmp_path)}})
        assert resp.status == 400                                       # not a folder of the list
    serve(tmp_path, body, listed(tmp_path, a))


def test_tool_install_needs_claude_signed_in_first_and_its_mode(tmp_path, chain_root, fake_machine):
    fake_machine.logged_in = False

    async def body(c, st, rn, quit):
        resp = await post(c, "/api/machine/repair", {"id": "tool", "args": {"tool": "adb"}, "mode": "rapide"})
        r = await resp.json()
        assert resp.status == 409 and r["machine"][0]["id"] == "claude_login"       # no login, no Claude install
        fake_machine.logged_in = True
        # « Demander » by default: the page asks first.
        resp = await post(c, "/api/machine/repair", {"id": "tool", "args": {"tool": "adb"}})
        assert resp.status == 409 and (await resp.json())["ask"] is True
        resp = await post(c, "/api/machine/repair", {"id": "tool", "args": {"tool": "inconnu"}, "mode": "rapide"})
        assert resp.status == 400
        d = await (await post(c, "/api/machine/describe", {"kind": "tool", "tool": "adb"})).json()
        assert installs.ANDROID_SDK in d["licences"] and d["what"]
    serve(tmp_path, body)


def test_a_login_is_refused_while_a_run_goes(tmp_path, chain_root):
    _, a, _ = app_world(tmp_path, "app")

    async def body(c, st, rn, quit):
        code, r = await run(c)
        assert code == 200
        for rid in ("claude_login", "github_login"):
            resp = await post(c, "/api/machine/repair", {"id": rid})
            r = await resp.json()
            assert resp.status == 409 and r["error"].startswith("Pas maintenant : une commande tourne"), rid
        await post(c, "/api/stop-now", {})
        await ended(rn, a)
    serve(tmp_path, body, listed(tmp_path, a), script=script_until_interrupted)


def test_the_phone_sees_the_summary_and_cannot_repair(tmp_path, chain_root, fake_machine):
    """Through the phone's address, with its cookie: « État de l'ordinateur »
    is read — never repaired: « sur l'ordinateur »."""
    import test_phone as tp
    fake_machine.logged_in = False

    async def body(c, state, rn, app_root, feat):
        await tp.turn_on(c)
        r = await tp.post(c, "/api/phone/login", {"code": tp.CODE}, tp.ph_headers())
        token = r.cookies[tp.phone_mod.COOKIE].value
        await post(c, "/api/machine/check", {})                         # from the computer
        got = await (await c.get("/api/machine", headers=tp.ph_headers(cookie=token, origin=None))).json()
        assert got["machine"]["summary"]["level"] == "block"
        for path, data in (("/api/machine/repair", {"id": "claude_login"}), ("/api/cockpit/restart", {}),
                           ("/api/machine/session/answer", {"card": "x", "accept": True}),
                           ("/api/machine/session/code", {"code": "x"}), ("/api/machine/session/cancel", {}),
                           ("/api/install-mode", {"mode": "rapide"})):
            r = await tp.post(c, path, data, tp.ph_headers(cookie=token))
            assert r.status == 403 and (await r.json())["error"] == "sur l'ordinateur", path
    tp.serve(tmp_path, body)


# ------------------------------------------------------------ the restart

def test_ping_says_the_commit_the_server_started_from(tmp_path, chain_root):
    async def body(c, st, rn, quit):
        p = await (await c.get("/api/ping")).json()
        assert p["started"] == head(chain_root) and p["version"] == "1.16"
    serve(tmp_path, body)


def test_redemarrer_le_cockpit(tmp_path, chain_root, fakes):  
    async def body(c, st, rn, quit):
        resp = await post(c, "/api/cockpit/restart", {})
        r = await resp.json()
        assert resp.status == 200 and r["restarting"] and r["new_pid"] == fakes.procs[0].pid, r
        assert len(fakes.spawned) == 1 and fakes.spawned[0]["trial"] != fakes.spawned[0]["port"]
        assert fakes.envs[0] and "PATH" in fakes.envs[0]           # the environment Windows has now
        await wait_for(lambda: quit)
    serve(tmp_path, body)


def test_redemarrer_refused_while_a_run_goes(tmp_path, chain_root, fakes):  
    _, a, _ = app_world(tmp_path, "app")

    async def body(c, st, rn, quit):
        code, _ = await run(c)
        assert code == 200
        resp = await post(c, "/api/cockpit/restart", {})
        assert resp.status == 409 and "redémarre après sa fin" in (await resp.json())["error"]
        assert fakes.spawned == []
        await post(c, "/api/stop-now", {})
        await ended(rn, a)
    serve(tmp_path, body, listed(tmp_path, a), script=script_until_interrupted)


def test_older_than_the_disk_it_restarts_itself_when_nothing_goes(tmp_path, chain_root, fakes, monkeypatch):  
    _, a, _ = app_world(tmp_path, "app")
    monkeypatch.setattr(server, "AUTO_RESTART", True)
    monkeypatch.setattr(server, "RESTART_POLL", 0.2)

    async def body(c, st, rn, quit):
        c.app_[server.PORT_KEY]["port"] = c.server.port
        # A run going: notified, not restarted.
        code, _ = await run(c)
        assert code == 200
        change(chain_root, "tools/cockpit/x.py", "plus récent\n", "cockpit : plus récent")
        await asyncio.sleep(1.0)
        assert fakes.spawned == []
        r = await (await post(c, "/api/machine/check", {})).json()
        srv = next(x for x in r["machine"]["items"] if x["id"] == "server")
        assert srv["status"] == machine.WARN and "redémarre de lui-même après la fin de /1_lexique f" in srv["detail"]
        await post(c, "/api/stop-now", {})
        await ended(rn, a)
        # Nothing goes: it restarts by itself, once.
        await wait_for(lambda: fakes.spawned)
        await wait_for(lambda: quit)
        await asyncio.sleep(0.6)
        assert len(fakes.spawned) == 1
    serve(tmp_path, body, listed(tmp_path, a), script=script_until_interrupted)


def test_lancer_bat_asks_an_older_server_to_restart(tmp_path, chain_root, fakes, monkeypatch):  
    """lancer.bat runs `server.py --ouvrir`: a cockpit answers, started from
    an older commit than the disk — it is asked to restart, and the page
    opens once the new one answers."""
    from fakeapp import FakeServer
    opened = []
    monkeypatch.setattr(server, "OPEN_BROWSER", opened.append)
    with FakeServer(tmp_path / "srv") as s:
        port = int(s.url.rsplit(":", 1)[1].strip("/"))
        old = startup.ping(port)
        assert old["started"] == head(chain_root)
        # Same commit: nothing asked.
        assert server.older_server(old, port) is False and fakes.spawned == []
        change(chain_root, "tools/cockpit/x.py", "plus récent\n", "cockpit : plus récent")
        monkeypatch.setattr(startup, "wait_new_server", lambda port, pid, timeout: {"pid": 4242})
        assert server.older_server(old, port) is True
        assert len(fakes.spawned) == 1 and fakes.spawned[0]["port"] == port
    # A server older than 1.16 says no commit: only the page opens.
    assert server.older_server({"cockpit": True, "pid": 1}, port) is False


def test_new_python_dependencies_in_an_update_ask_rapide_or_pas_a_pas(tmp_path, monkeypatch, fakes):
    """« Mettre à jour le cockpit »: new requirements are an install — the
    page's request (`asked`) gets the question first, then « Rapide » goes."""
    _, here, other = chain_world(tmp_path)
    change(other, "tools/cockpit/requirements.txt", "aiohttp>=3.9,<4\nrich>=13\n", "cockpit : rich", push=True)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    monkeypatch.setattr(installs, "describe_pip", lambda path=None: {"what": ["rich 13.7.1"], "licences": ["MIT"],
                                                                     "unskippable": []})

    async def body(c, st, rn, quit):
        resp = await post(c, "/api/cockpit/update", {"asked": True})
        r = await resp.json()
        assert resp.status == 409 and r["ask"] is True and r["describe"]["licences"] == ["MIT"]
        assert fakes.pip_calls() == [] and fakes.spawned == []
        resp = await post(c, "/api/cockpit/update", {"asked": True, "mode": "rapide"})
        r = await resp.json()
        assert resp.status == 200 and r["restarting"], r
        assert "Rapide — installe : rich 13.7.1 — licences acceptées : MIT" in r["steps"]
        assert len(fakes.pip_calls()) == 1
    serve(tmp_path, body)
