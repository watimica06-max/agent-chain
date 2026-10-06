"""Cockpit 1.2 — the permission mode and the diagnostic. No browser, no chain
command: the SDK client and the commands the diagnostic runs are fakes."""
import asyncio
import json
import os
import subprocess

import pytest

import diagnostic
import runner as runner_mod
import server
from state import State
from test_runner import FakeClient, script_quick
from test_server import post, with_client


# ---------------------------------------------------------------- mode

def test_mode_defaults_to_auto_and_is_remembered(tmp_path):
    path = str(tmp_path / "config.json")
    st = State(path)
    assert st.mode == "auto"
    st.set_mode("manuel")
    assert State(path).mode == "manuel"                # read back from config.json
    assert json.load(open(path, encoding="utf-8"))["mode"] == "manuel"
    with pytest.raises(ValueError):
        st.set_mode("bypassPermissions")                # only the two modes exist
    # A broken value in the file reads as the default, never as an unknown mode.
    open(path, "w", encoding="utf-8").write('{"mode": "nope"}')
    assert State(path).mode == "auto"


def test_mode_reaches_the_sdk_options_on_every_run(tmp_path):
    """Through the real client factory: the options carry the mode explicitly,
    run after run, and a change applies to the next run."""
    seen = []

    def factory(cwd, can_use_tool, **kw):
        real = runner_mod.sdk_client_factory(cwd, can_use_tool, **kw)   # builds options, connects nothing
        seen.append(real.options.permission_mode)
        return FakeClient(script_quick, can_use_tool)

    st = State(str(tmp_path / "config.json"))

    async def go():
        rn = runner_mod.Runner(client_factory=factory, log_dir=str(tmp_path / "logs"),
                               mode_getter=lambda: st.mode)
        modes = []
        for mode in ("auto", "manuel", "auto"):
            st.set_mode(mode)
            run = await rn.start(str(tmp_path), "f", "f", "9_controle", "f")
            await run.task
            modes.append(run.snapshot()["mode"])
        return modes

    assert asyncio.run(go()) == ["auto", "manuel", "auto"]
    assert seen == ["auto", "default", "auto"]          # Manuel is the SDK's `default`


def test_the_sdk_accepts_auto_in_this_version():
    from typing import get_args
    from claude_agent_sdk import ClaudeAgentOptions
    from claude_agent_sdk.types import PermissionMode
    assert "auto" in get_args(PermissionMode)
    assert ClaudeAgentOptions(permission_mode="auto").permission_mode == "auto"


def test_mode_route_and_state(tmp_path):
    async def body(c, app_root, feat, rn):
        r = await post(c, "/api/open", {"app": str(app_root), "work": "f"})
        assert r.status == 200
        s = await (await c.get("/api/state")).json()
        assert s["mode"] == "auto"
        r = await post(c, "/api/mode", {"mode": "manuel"})
        assert r.status == 200 and (await r.json())["mode"] == "manuel"
        assert (await (await c.get("/api/state")).json())["mode"] == "manuel"
        r = await post(c, "/api/mode", {"mode": "dontAsk"})
        assert r.status == 400
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert (await r.json())["run"]["mode"] == "manuel"
        await post(c, "/api/stop-now", {})
    with_client(tmp_path, body)


# ---------------------------------------------------------- diagnostic

def fake_exec(table):
    """`table`: program -> (returncode, output) | an exception to raise."""
    calls = []

    def run(argv, cwd, timeout):
        calls.append((argv, cwd, timeout))
        key = "gradle" if "gradlew" in argv[0] else argv[0]
        out = table[key]
        if isinstance(out, BaseException):
            raise out
        return out

    run.calls = calls
    return run


ALL_GOOD = {"java": (0, 'openjdk version "17.0.9"\nmore'), "gradle": (0, "\nGradle 8.7\n"),
            "flutter": (0, "Flutter 3.22"), "adb": (0, "Android Debug Bridge version 1.0.41"),
            "claude": (0, "2.1.285 (Claude Code)"), "git": (0, "git version 2.45")}


def app_with(tmp_path, gradle=False, pubspec=False):
    if gradle:
        (tmp_path / "gradlew.bat").write_text("@echo off")
    if pubspec:
        (tmp_path / "pubspec.yaml").write_text("name: x")
    return str(tmp_path)


def by_id(result):
    return {r["id"]: r for r in result["results"]}


def test_diagnostic_passing_with_first_line_of_output(tmp_path):
    fe = fake_exec(ALL_GOOD)
    res = diagnostic.run_diagnostic(app_with(tmp_path, gradle=True, pubspec=True), fe)
    r = by_id(res)
    assert [x["status"] for x in res["results"]] == ["ok"] * 6 and res["ok"] and res["hints"] == []
    assert r["java"]["detail"] == 'openjdk version "17.0.9"'      # the first line only
    assert r["gradle"]["detail"] == "Gradle 8.7"                  # blank lines skipped
    # Run from the application folder; Gradle gets 120 s, the others less.
    assert all(cwd == str(tmp_path) for _, cwd, _ in fe.calls)
    assert {a[0].split("\\")[-1] if "gradlew" in a[0] else a[0]: t for a, _, t in fe.calls}["gradlew.bat"] == 120
    assert min(t for _, _, t in fe.calls) < 120


def test_diagnostic_failing_and_missing(tmp_path):
    table = dict(ALL_GOOD, adb=(1, "adb: device offline"), git=FileNotFoundError("git introuvable (PATH)"))
    res = diagnostic.run_diagnostic(app_with(tmp_path), fake_exec(table))
    r = by_id(res)
    assert r["adb"]["status"] == "fail" and "device offline" in r["adb"]["detail"] and "code 1" in r["adb"]["detail"]
    assert r["git"]["status"] == "fail" and "introuvable" in r["git"]["detail"]
    assert not res["ok"]


def test_diagnostic_timeout(tmp_path):
    table = dict(ALL_GOOD, claude=subprocess.TimeoutExpired("claude", 30))
    res = diagnostic.run_diagnostic(app_with(tmp_path), fake_exec(table))
    c = by_id(res)["claude"]
    assert c["status"] == "fail" and "délai dépassé (30 s)" in c["detail"]


def test_diagnostic_skips_what_the_folder_does_not_hold(tmp_path):
    fe = fake_exec(ALL_GOOD)
    res = diagnostic.run_diagnostic(app_with(tmp_path), fe)
    r = by_id(res)
    assert r["gradle"] == {"id": "gradle", "label": "Gradle", "status": "skip", "detail": "non concerné"}
    assert r["flutter"]["status"] == "skip"
    assert [a[0] for a, _, _ in fe.calls] == ["java", "adb", "claude", "git"]   # nothing run for the skipped
    res = diagnostic.run_diagnostic(app_with(tmp_path, pubspec=True), fake_exec(ALL_GOOD))
    assert by_id(res)["flutter"]["status"] == "ok" and by_id(res)["gradle"]["status"] == "skip"


def test_java_failure_with_gradle_present_explains_java_home(tmp_path):
    table = dict(ALL_GOOD, java=FileNotFoundError("java introuvable (PATH)"),
                 gradle=(1, "ERROR: JAVA_HOME is not set"))
    res = diagnostic.run_diagnostic(app_with(tmp_path, gradle=True), fake_exec(table))
    (hint,) = res["hints"]
    assert "JAVA_HOME" in hint and r"C:\Program Files\Android\Android Studio\jbr" in hint
    assert "variables d'environnement de Windows" in hint and "Redémarrez" in hint


def _java_home(tmp_path, with_java=True):
    home = tmp_path / "jdk"
    (home / "bin").mkdir(parents=True)
    if with_java:
        (home / "bin" / ("java.exe" if os.name == "nt" else "java")).write_text("")
    return str(home)


def test_java_home_set_checks_its_java_not_the_path(tmp_path):
    # 1.5: Gradle runs %JAVA_HOME%\bin\java. That one works, the PATH has none: ✓, no hint.
    home = _java_home(tmp_path)
    seen = []

    def ex(argv, cwd, timeout):
        seen.append(argv[0])
        if argv[0] == "java":
            raise FileNotFoundError("java introuvable (PATH)")
        return ALL_GOOD["java"] if argv[0].startswith(home) else (0, "ok")
    (tmp_path / "app").mkdir()
    res = diagnostic.run_diagnostic(app_with(tmp_path / "app", gradle=True), ex, env={"JAVA_HOME": home})
    j = by_id(res)["java"]
    assert seen[0] == os.path.join(home, "bin", "java.exe" if os.name == "nt" else "java")
    assert j["status"] == "ok" and j["label"] == "Java (JAVA_HOME)" and home in j["detail"]
    assert res["hints"] == []


def test_java_home_set_but_failing_is_a_failure_without_the_java_home_hint(tmp_path):
    home = _java_home(tmp_path)
    (tmp_path / "app").mkdir()
    table = lambda argv, cwd, t: (1, "Error: could not open jvm.cfg") if argv[0].startswith(home) else (0, "ok")
    res = diagnostic.run_diagnostic(app_with(tmp_path / "app", gradle=True), table, env={"JAVA_HOME": home})
    assert by_id(res)["java"]["status"] == "fail" and res["hints"] == []


def test_java_home_pointing_to_nothing_says_so(tmp_path):
    home = _java_home(tmp_path, with_java=False)
    (tmp_path / "app").mkdir()
    res = diagnostic.run_diagnostic(app_with(tmp_path / "app", gradle=True), diagnostic.system_exec,
                                    env={"JAVA_HOME": home})
    assert by_id(res)["java"]["status"] == "fail"
    (hint,) = res["hints"]
    assert "JAVA_HOME pointe vers" in hint and home in hint


def test_java_home_unset_checks_the_path_and_keeps_the_hint(tmp_path):
    table = dict(ALL_GOOD, java=FileNotFoundError("java introuvable (PATH)"))
    fe = fake_exec(table)
    res = diagnostic.run_diagnostic(app_with(tmp_path, gradle=True), fe, env={})
    assert fe.calls[0][0][0] == "java" and by_id(res)["java"]["label"] == "Java (PATH)"
    assert res["hints"] == [diagnostic.JAVA_HINT]


def test_java_failure_without_gradle_has_no_hint(tmp_path):
    table = dict(ALL_GOOD, java=(1, "boom"))
    res = diagnostic.run_diagnostic(app_with(tmp_path), fake_exec(table))
    assert by_id(res)["java"]["status"] == "fail" and res["hints"] == []


def test_system_exec_runs_a_real_command_and_reports_a_missing_one(tmp_path):
    code, out = diagnostic.system_exec(["git", "--version"], str(tmp_path), 20)
    assert code == 0 and "git version" in out
    with pytest.raises(FileNotFoundError):
        diagnostic.system_exec(["programme-qui-n-existe-pas"], str(tmp_path), 5)


def test_diagnostic_route_keeps_the_last_result_with_its_date(tmp_path):
    def fake(app):
        return diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD))

    async def body(c, app_root, feat, rn, state):
        await post(c, "/api/open", {"app": str(app_root), "work": "f"})
        assert (await (await c.get("/api/state")).json())["diagnostic"] is None
        r = await post(c, "/api/diagnostic", {})
        res = await r.json()
        assert r.status == 200 and res["at"] and res["ok"]
        s = await (await c.get("/api/state")).json()
        assert s["diagnostic"]["at"] == res["at"]
        # In config.json, readable by a fresh State.
        assert State(state.path).diagnostic()["at"] == res["at"]

    from aiohttp.test_utils import TestClient, TestServer

    app_root = tmp_path / "app"
    from test_server import build_app_folder
    feat = build_app_folder(app_root)
    st = State(str(tmp_path / "config.json"))
    rn = runner_mod.Runner(client_factory=lambda cwd, cb, **kw: FakeClient(script_quick, cb),
                           log_dir=str(tmp_path / "logs"))
    app = server.make_app(st, rn, diag_runner=fake)

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            await body(c, app_root, feat, rn, st)

    asyncio.run(go())


# ------------------------------------------- the diagnostic on its own (1.4.5)

def _app_counting(tmp_path, table=ALL_GOOD, stored=None):
    from test_server import build_app_folder
    app_root = tmp_path / "app"
    build_app_folder(app_root)
    st = State(str(tmp_path / "config.json"))
    st.open_pair(str(app_root), "f")
    if stored:
        st.set_diagnostic(stored, app=str(app_root))      # 1.6: an application's own
    calls = []

    def fake(app):
        calls.append(app)
        return diagnostic.run_diagnostic(app, fake_exec(table))
    rn = runner_mod.Runner(client_factory=lambda cwd, cb, **kw: FakeClient(script_quick, cb),
                           log_dir=str(tmp_path / "logs"))
    return server.make_app(st, rn, diag_runner=fake), st, calls


async def _settle(c):
    for _ in range(200):
        s = await (await c.get("/api/state")).json()
        if not s["diagnostic_running"]:
            return s
        await asyncio.sleep(0.02)
    raise AssertionError("le diagnostic ne finit pas")


def test_no_result_stored_the_diagnostic_runs_once_and_is_kept(tmp_path):
    app, st, calls = _app_counting(tmp_path)

    async def go():
        from aiohttp.test_utils import TestClient, TestServer
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:       # the server's opening
            s = await _settle(c)
            for _ in range(3):                                                # the page opened again and again
                await post(c, "/api/check", {"reason": "ouverture"})
                s = await _settle(c)
            assert s["diagnostic"]["ok"]
            # On demand, unchanged.
            await post(c, "/api/diagnostic", {})
    asyncio.run(go())
    assert len(calls) == 2                       # once on its own, once on demand
    assert State(st.path).diagnostic()["ok"]     # kept in config.json


def test_a_stored_result_is_not_run_again(tmp_path):
    app, st, calls = _app_counting(tmp_path, stored={"at": "2026-10-01T09:00:00", "results": [], "ok": True})

    async def go():
        from aiohttp.test_utils import TestClient, TestServer
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            await post(c, "/api/check", {"reason": "ouverture"})
            assert not (await _settle(c))["diagnostic_running"]
    asyncio.run(go())
    assert calls == []


def test_first_line_skips_a_rule_of_dashes():
    out = "\n------------------------------------------------------------\nGradle 8.7\n----\n"
    assert diagnostic.first_line(out) == "Gradle 8.7"
