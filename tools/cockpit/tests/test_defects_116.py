"""1.16 §0 — four defects, each failing on 1.15's code:

1. adb looked for on the PATH only, while the deploy adapter finds it in the
   SDK's platform-tools;
2. a run whose assistant message carries `authentication_failed` said
   « erreur : success »;
3. a chain install whose push failed shown in the green « ok » style;
4. commits not yet sent hidden while GitHub cannot be reached.

GitHub is a bare repository in a temporary folder; no chain command runs."""
import asyncio
import json
import os

import pytest
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

import apps as apps_mod
import diagnostic
import runner as runner_mod
import sync
from syncworld import app_world, change, offline
from test_mode_diagnostic import ALL_GOOD, fake_exec
from test_runner import FakeClient

ADB = r"C:\Users\po\AppData\Local\Android\Sdk\platform-tools\adb.exe"


# ------------------------------------------------------------ 1. adb

def test_adb_is_found_where_the_deploy_adapter_finds_it(tmp_path):
    calls = []

    def ex(argv, cwd, timeout):
        calls.append(argv)
        if argv[0] == ADB:
            return 0, "Android Debug Bridge version 1.0.41"
        if argv[0] == "adb":
            raise FileNotFoundError("adb introuvable (PATH)")
        return fake_exec(ALL_GOOD)(argv, cwd, timeout)

    find = {"adb": [ADB], "emulator": None, "scrcpy": None}
    res = diagnostic.run_diagnostic(str(tmp_path), ex, find=lambda tool: find[tool])
    adb = next(r for r in res["results"] if r["id"] == "adb")
    assert [ADB, "version"] in calls
    assert adb["status"] == "ok" and adb["detail"] == "Android Debug Bridge version 1.0.41"


def test_adb_nowhere_still_says_it(tmp_path):
    def ex(argv, cwd, timeout):
        if argv[0] == "adb":
            raise FileNotFoundError("adb introuvable (PATH)")
        return fake_exec(ALL_GOOD)(argv, cwd, timeout)
    res = diagnostic.run_diagnostic(str(tmp_path), ex, find=lambda tool: None)
    adb = next(r for r in res["results"] if r["id"] == "adb")
    assert adb["status"] == "fail" and "introuvable" in adb["detail"]


def test_the_default_lookup_is_the_adapters(monkeypatch):
    from adapters import android
    monkeypatch.setattr(android, "ADB", [ADB])
    assert diagnostic.find_tool("adb") == [ADB]


# ------------------------------------------------------------ 2. authentication_failed

async def not_signed_in(c):
    yield AssistantMessage(content=[TextBlock("Not logged in · Please run /login")], model="<synthetic>",
                           error="authentication_failed")
    yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=0, is_error=True, num_turns=1,
                        session_id="s", result="Not logged in · Please run /login")


def test_a_run_refused_for_authentication_says_claude_is_not_signed_in(tmp_path):
    async def go():
        rn = runner_mod.Runner(client_factory=lambda cwd, cut, **kw: FakeClient(not_signed_in, cut),
                               log_dir=str(tmp_path / "logs"))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        await run.task
        return run.snapshot()
    snap = asyncio.run(go())
    assert snap["outcome"] == "erreur"
    assert snap["error"] == "Claude Code n'est pas connecté sur cet ordinateur"
    assert snap["error"] != "success" and snap["auth_failed"] is True and snap["api_error"] == "authentication_failed"


def test_a_failed_result_without_an_assistant_error_keeps_its_own_words(tmp_path):
    async def failed(c):
        yield ResultMessage(subtype="error_max_turns", duration_ms=1, duration_api_ms=0, is_error=True, num_turns=1,
                            session_id="s", result="")

    async def go():
        rn = runner_mod.Runner(client_factory=lambda cwd, cut, **kw: FakeClient(failed, cut),
                               log_dir=str(tmp_path / "logs"))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        await run.task
        return run.snapshot()
    snap = asyncio.run(go())
    assert snap["error"] == "error_max_turns" and snap["auth_failed"] is False


# ------------------------------------------------------------ 3. a failed push is never green

def test_the_bulk_report_marks_an_install_whose_push_failed(tmp_path):
    rows = [{"name": "Carnet", "folder": str(tmp_path)}]
    res = {"commit": "abc1234", "date": "2026-10-10", "app_commit": "def5678", "message": "chain: abc1234 2026-10-10",
           "pushed": False, "push_error": "GitHub injoignable"}
    lines = apps_mod.update_all(rows, lambda f: {"state": "en retard", "summary": "en retard"},
                                lambda f: res, lambda f: False)
    assert lines[0]["outcome"] == apps_mod.UPDATED and lines[0]["unpushed"] is True
    assert "non poussé : GitHub injoignable" in lines[0]["text"]
    res["pushed"], res["push_error"] = True, None
    lines = apps_mod.update_all(rows, lambda f: {"state": "en retard", "summary": "en retard"},
                                lambda f: res, lambda f: False)
    assert lines[0]["unpushed"] is False


# ------------------------------------------------------------ 4. not sent, GitHub unreachable

def test_unsent_commits_are_counted_while_github_is_unreachable(tmp_path):
    _, a, _ = app_world(tmp_path, "app")
    change(a, "README.md", "un\n", "un")
    change(a, "README.md", "deux\n", "deux")
    offline(a)
    st = sync.compute(str(a))
    assert st["state"] == sync.OFFLINE and st["ahead"] == 2
    assert st["summary"].startswith("GitHub injoignable · 2 non envoyés")
    # Nothing to send: said as before.
    _, b, _ = app_world(tmp_path / "b", "app")
    offline(b)
    st = sync.compute(str(b))
    assert st["state"] == sync.OFFLINE and st["ahead"] == 0 and st["summary"].startswith("GitHub injoignable — ")
