"""runner.py with the SDK client replaced by a fake."""
import asyncio
import os
import subprocess

import pytest
from claude_agent_sdk import (AssistantMessage, PermissionResultAllow, PermissionResultDeny,
                              ResultMessage, TextBlock, ToolPermissionContext, ToolResultBlock,
                              ToolUseBlock, UserMessage)

import runner as runner_mod

RELAY = "Le lexique est réglé.\nNext: answer questions, then run /1_lexique f"


class FakeClient:
    def __init__(self, script, can_use_tool):
        self.script = script
        self.can_use_tool = can_use_tool
        self.prompts = []
        self.interrupted = asyncio.Event()
        self.permission_result = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def query(self, prompt):
        self.prompts.append(prompt)

    def receive_response(self):
        return self.script(self)

    def receive_messages(self):
        return self.script(self)

    async def interrupt(self):
        self.interrupted.set()


def result(text, **kw):
    return ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False,
                         num_turns=1, session_id="s", result=text, **kw)


async def script_with_permission(c):
    yield AssistantMessage(content=[
        TextBlock("Je lance le lexicographe."),
        ToolUseBlock(id="t1", name="Agent",
                     input={"subagent_type": "lexicographe", "description": "Sweep the idea file"}),
    ], model="m")
    yield AssistantMessage(content=[TextBlock("Je balaie idees.md."),
                                    ToolUseBlock(id="t2", name="Read", input={"file_path": "idees.md"})],
                           model="m", parent_tool_use_id="t1")
    c.permission_result = await c.can_use_tool(
        "Write", {"file_path": "questions-lexicographe-01.md", "content": "### Q1"},
        ToolPermissionContext(tool_use_id="u1", title="Claude veut écrire questions-lexicographe-01.md"))
    yield UserMessage(content=[ToolResultBlock(tool_use_id="t1", content="fait")])
    yield AssistantMessage(content=[TextBlock(RELAY)], model="m")
    yield result(RELAY)


async def script_until_interrupted(c):
    yield AssistantMessage(content=[TextBlock("Lot 1…")], model="m")
    await c.interrupted.wait()
    yield result("", terminal_reason="aborted_streaming")


async def script_quick(c):
    yield result("Fait.\nNext: done")


def make_runner(script, ended=None):
    made = []

    def factory(cwd, can_use_tool):
        c = FakeClient(script, can_use_tool)
        c.cwd = cwd
        made.append(c)
        return c

    rn = runner_mod.Runner(client_factory=factory, on_end=(ended.append if ended is not None else None))
    return rn, made


async def next_event(q, kind, timeout=2):
    while True:
        ev = await asyncio.wait_for(q.get(), timeout)
        if ev["type"] == kind:
            return ev


def test_events_streamed_and_permission_allowed(tmp_path):
    async def go():
        ended = []
        rn, made = make_runner(script_with_permission, ended)
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        perm = await next_event(q, "permission")
        assert perm["data"]["tool"] == "Write"
        assert perm["data"]["agent"] == "lexicographe"
        assert "questions-lexicographe-01.md" in perm["data"]["input"]
        assert rn.current(str(tmp_path)).snapshot()["permissions"][0]["id"] == perm["data"]["id"]
        rn.answer_permission(str(tmp_path), perm["data"]["id"], True)
        await run.task
        return rn, made, ended, run

    rn, made, ended, run = asyncio.run(go())
    (client,) = made
    assert client.cwd == str(tmp_path)
    assert client.prompts == ["/1_lexique f"]
    assert isinstance(client.permission_result, PermissionResultAllow)
    kinds = [e["type"] for e in run.events]
    assert kinds == ["run_started", "status", "text", "agent_started", "text", "tool",
                     "permission", "permission_resolved", "agent_ended", "text", "run_ended"]
    texts = [(e["data"]["agent"], e["data"]["text"]) for e in run.events if e["type"] == "text"]
    assert texts[1] == ("lexicographe", "Je balaie idees.md.")
    assert run.outcome == "terminé" and run.relay == RELAY
    assert run.next["kind"] == "answer" and run.next["command"] == "1_lexique"
    assert ended == [run]


def test_permission_denied(tmp_path):
    async def go():
        rn, made = make_runner(script_with_permission)
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        perm = await next_event(q, "permission")
        rn.answer_permission(str(tmp_path), perm["data"]["id"], False)
        await run.task
        return made[0]

    client = asyncio.run(go())
    assert isinstance(client.permission_result, PermissionResultDeny)


def test_one_run_at_a_time_per_repository(tmp_path):
    other = tmp_path / "other"
    other.mkdir()

    async def go():
        rn, made = make_runner(script_until_interrupted)
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "8_code", "f")
        await next_event(q, "text")
        with pytest.raises(runner_mod.Busy):
            await rn.start(str(tmp_path), "f", "f", "9_controle", "f")
        # Another repository is not held by this lock.
        run_b = await rn.start(str(other), "g", "g", "8_code", "g")
        await rn.stop_now(str(tmp_path))
        await run.task
        assert made[0].interrupted.is_set()
        assert run.outcome == "interrompu"
        await rn.stop_now(str(other))
        await run_b.task
        rn.client_factory = make_runner(script_quick)[0].client_factory
        again = await rn.start(str(tmp_path), "f", "f", "9_controle", "f")
        await again.task
        return again

    again = asyncio.run(go())
    assert again.outcome == "terminé" and again.next["kind"] == "done"


def test_stop_now_denies_a_pending_permission(tmp_path):
    async def go():
        rn, made = make_runner(script_with_permission)
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        await next_event(q, "permission")
        await rn.stop_now(str(tmp_path))
        await run.task
        return made[0], run

    client, run = asyncio.run(go())
    assert isinstance(client.permission_result, PermissionResultDeny)
    assert run.outcome == "interrompu"


def test_stop_at_next_lot_writes_stop_md_for_8_code_only(tmp_path):
    feature = tmp_path / "docs" / "features" / "f"
    feature.mkdir(parents=True)

    async def go():
        rn, _ = make_runner(script_until_interrupted)
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f/bugfix-02", "f", "8_code", "f")
        await next_event(q, "text")
        path = rn.stop_at_next_lot(str(tmp_path))
        await rn.stop_now(str(tmp_path))
        await run.task
        run2 = await rn.start(str(tmp_path), "f", "f", "7_lots", "f")
        await next_event(q, "text")
        with pytest.raises(runner_mod.NotRunning):
            rn.stop_at_next_lot(str(tmp_path))
        await rn.stop_now(str(tmp_path))
        await run2.task
        return path

    path = asyncio.run(go())
    # At the feature folder's root, even when the working folder is a bugfix.
    assert path == str(feature / "stop.md") and os.path.exists(path)
    target = runner_mod.Runner.disarm_stop_file(str(tmp_path), "f")
    assert target == str(feature / "stop1.md") and not os.path.exists(path)


def test_client_failure_ends_the_run(tmp_path):
    async def broken(c):
        raise RuntimeError("CLI introuvable")
        yield  # pragma: no cover

    async def go():
        rn, _ = make_runner(broken)
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        await run.task
        return rn, run

    rn, run = asyncio.run(go())
    assert run.outcome == "erreur" and "CLI introuvable" in run.error
    assert run.next["kind"] == "unknown"
    assert not rn.is_running(str(tmp_path))


def test_options_load_project_settings_never_bare(tmp_path):
    async def cb(*a):
        return PermissionResultAllow()
    opts = runner_mod.build_options(str(tmp_path), cb)
    assert opts.cwd == str(tmp_path)
    assert opts.setting_sources is None          # all sources: commands, agents, CLAUDE.md
    assert opts.can_use_tool is cb
    assert opts.permission_mode is None
    assert "bare" not in " ".join(f"{k} {v}" for k, v in (opts.extra_args or {}).items())


def test_live_worktrees_listed_only_during_a_run(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(git[:3] + ["init", "-q"], check=True)
    (repo / "a.txt").write_text("a")
    subprocess.run(git + ["add", "."], check=True)
    subprocess.run(git + ["commit", "-qm", "a"], check=True)
    wt = tmp_path / "wt"
    subprocess.run(git + ["worktree", "add", "-q", str(wt), "HEAD"], check=True)

    async def go():
        rn, _ = make_runner(script_until_interrupted)
        assert rn.live_worktrees(str(repo)) == []
        q = rn.subscribe(str(repo))
        run = await rn.start(str(repo), "f", "f", "8_code", "f")
        await next_event(q, "text")
        live = rn.live_worktrees(str(repo))
        await rn.stop_now(str(repo))
        await run.task
        return live

    live = asyncio.run(go())
    assert [os.path.realpath(p) for p in live] == [os.path.realpath(wt)]
