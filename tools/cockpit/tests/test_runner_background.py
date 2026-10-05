"""Cockpit 1.1 — a run whose orchestrator starts agents in the background.

The fake client keeps its stream OPEN, as the real CLI does: messages are
pushed by the test, and the stream ends only when the client is closed. No
chain command runs.
"""
import asyncio
import json
import os
import subprocess

import pytest
from claude_agent_sdk import (AssistantMessage, ResultMessage, SystemMessage, TaskNotificationMessage,
                              TextBlock, ToolResultBlock, ToolUseBlock, UserMessage)

import runner as runner_mod

RELAY = "Le lexique est réglé.\nNext: answer questions, then run /1_lexique f"
LAUNCHED = ("Async agent launched successfully.\nagentId: a1b2c3 (internal ID)\n"
            "The agent is working in the background. You will be notified when it completes.")


class LiveClient:
    def __init__(self, can_use_tool, resume=None):
        self.can_use_tool = can_use_tool
        self.resume = resume
        self.prompts = []
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.closed = False
        self.interrupted = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        self.closed = True
        return False

    async def query(self, prompt):
        self.prompts.append(prompt)

    async def receive_messages(self):
        while True:
            msg = await self.inbox.get()
            if msg is None:
                return
            yield msg

    async def interrupt(self):
        self.interrupted = True

    def push(self, *msgs):
        for m in msgs:
            self.inbox.put_nowait(m)


def make_runner(log_dir, clients):
    def factory(cwd, can_use_tool, resume=None, mode=None):
        c = LiveClient(can_use_tool, resume)
        c.mode = mode
        clients.append(c)
        return c
    return runner_mod.Runner(client_factory=factory, log_dir=str(log_dir))


def result(text, session="sess-1", **kw):
    return ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False,
                         num_turns=1, session_id=session, result=text, **kw)


def launch():
    """The orchestrator starts the lexicographe; the tool result says it runs
    in the background; the orchestrator says it waits; the turn's result."""
    return [
        AssistantMessage(content=[ToolUseBlock(id="t1", name="Agent", input={
            "subagent_type": "lexicographe", "description": "Sweep the vocabulary"})], model="m"),
        UserMessage(content=[ToolResultBlock(tool_use_id="t1", content=LAUNCHED)]),
        AssistantMessage(content=[TextBlock("The lexicographe is sweeping the vocabulary. "
                                            "I'm waiting for it to report.")], model="m"),
        result("The lexicographe is sweeping the vocabulary. I'm waiting for it to report."),
    ]


def notification(task_id="task-9", tool_use_id="t1", status="completed"):
    return TaskNotificationMessage(subtype="task_notification", data={}, task_id=task_id, status=status,
                                   output_file="", summary="done", uuid="u", session_id="sess-1",
                                   tool_use_id=tool_use_id)


async def settle(n=5):
    for _ in range(n):
        await asyncio.sleep(0.02)


async def next_event(q, kind, timeout=2):
    while True:
        ev = await asyncio.wait_for(q.get(), timeout)
        if ev["type"] == kind:
            return ev


def test_run_survives_first_result_and_ends_on_the_final_next_line(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "END_GRACE", 0.1)

    async def go():
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        repo = str(tmp_path)
        run = await rn.start(repo, "f", "f", "1_lexique", "f")
        await settle()
        (c,) = clients
        c.push(*launch())
        await settle(15)
        mid = (run.status, list(run.active), run.relay)
        c.push(notification(),
               AssistantMessage(content=[TextBlock(RELAY)], model="m"),
               result(RELAY))
        await asyncio.wait_for(run.task, 3)
        return run, mid, c

    run, mid, c = asyncio.run(go())
    # The first ResultMessage did not end the run: an agent was still pending.
    assert mid[0] == "running" and mid[1] == ["t1"]
    assert c.prompts == ["/1_lexique f"]
    assert run.outcome == "terminé" and run.relay == RELAY
    assert run.next["kind"] == "answer" and run.next["command"] == "1_lexique"
    kinds = [e["type"] for e in run.events]
    assert "agent_background" in kinds
    late = [e for e in run.events if e["type"] == "agent_ended"]
    assert len(late) == 1 and late[0]["data"]["late"] is True
    # Everything is on the same page: one stream, one run_ended carrying the final relay.
    assert kinds.count("run_ended") == 1
    assert [e for e in run.events if e["type"] == "run_ended"][0]["data"]["next"]["kind"] == "answer"
    assert c.closed


def test_session_state_idle_ends_the_run(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "END_GRACE", 60)     # the grace path must not be the one used

    def state(s):
        return SystemMessage(subtype="session_state_changed", data={"state": s})

    async def go():
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        await settle()
        (c,) = clients
        c.push(state("running"), *launch())
        await settle(15)
        assert run.status == "running"
        c.push(notification(), state("running"),
               AssistantMessage(content=[TextBlock(RELAY)], model="m"),
               result(RELAY), state("idle"))
        await asyncio.wait_for(run.task, 3)
        return run

    run = asyncio.run(go())
    assert run.outcome == "terminé" and run.next["kind"] == "answer"


def test_idle_ceiling_asks_then_continue_or_stop(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "IDLE_CEILING", 0.15)

    async def go():
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        repo = str(tmp_path)
        q = rn.subscribe(repo)
        run = await rn.start(repo, "f", "f", "1_lexique", "f")
        await settle()
        clients[0].push(*launch())
        first = await next_event(q, "idle_wait")
        snap = run.snapshot()["idle"]
        rn.continue_waiting(repo)
        await settle()
        assert run.status == "running" and run.idle is None
        second = await next_event(q, "idle_wait")        # the wait starts over
        await rn.stop_now(repo)
        await asyncio.wait_for(run.task, 3)
        return run, first, second, snap

    run, first, second, snap = asyncio.run(go())
    assert first["data"]["agents"] == ["lexicographe"] and snap["agents"] == ["lexicographe"]
    assert second["data"]["agents"] == ["lexicographe"]
    assert run.outcome == "interrompu"
    with pytest.raises(runner_mod.NotRunning):
        runner_mod.Runner().continue_waiting(str(tmp_path))


def test_no_idle_question_while_a_permission_waits_on_the_product_owner(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "IDLE_CEILING", 0.1)

    async def go():
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        repo = str(tmp_path)
        q = rn.subscribe(repo)
        run = await rn.start(repo, "f", "f", "1_lexique", "f")
        await settle()
        c = clients[0]
        c.push(*launch())
        asking = asyncio.create_task(c.can_use_tool("Write", {"file_path": "x"}, None))
        await next_event(q, "permission")
        await asyncio.sleep(0.4)
        assert run.idle is None
        rn.answer_permission(repo, next(iter(run.permissions)), True)
        await asking
        await rn.stop_now(repo)
        await asyncio.wait_for(run.task, 3)

    asyncio.run(go())


def test_continue_session_sends_into_the_same_session(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "END_GRACE", 0.05)

    async def go():
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        repo = str(tmp_path)
        run = await rn.start(repo, "f", "f", "1_lexique", "f")
        await settle()
        clients[0].push(AssistantMessage(content=[TextBlock("Je m'arrête là.")], model="m"),
                        result("Je m'arrête là.", session="sess-42"))
        await asyncio.wait_for(run.task, 3)
        assert run.next["kind"] == "unknown"
        snap = run.snapshot()
        again = await rn.continue_session(repo)
        await settle()
        clients[1].push(AssistantMessage(content=[TextBlock(RELAY)], model="m"),
                        result(RELAY, session="sess-42"))
        await asyncio.wait_for(again.task, 3)
        # A run that ended with its Next: line offers no continuation.
        with pytest.raises(runner_mod.NotRunning):
            await runner_mod.Runner().continue_session(repo)
        return run, again, clients, snap

    run, again, clients, snap = asyncio.run(go())
    assert snap["can_continue"] is True and snap["session_id"] == "sess-42"
    assert clients[0].resume is None
    assert clients[1].resume == "sess-42"                      # the SAME session
    assert clients[1].prompts == [runner_mod.CONTINUE_PROMPT]
    assert runner_mod.CONTINUE_PROMPT == ("Continue the command where you stopped, "
                                          "and end with its Next: line.")
    assert again.snapshot()["continued"] is True
    assert again.outcome == "terminé" and again.next["kind"] == "answer"
    assert again.snapshot()["can_continue"] is False


def test_raw_log_holds_every_message(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "END_GRACE", 0.05)
    logs = tmp_path / "logs"

    async def go():
        clients = []
        rn = make_runner(logs, clients)
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f")
        await settle()
        clients[0].push(*launch(), notification(),
                        AssistantMessage(content=[TextBlock(RELAY)], model="m"), result(RELAY))
        await asyncio.wait_for(run.task, 3)
        return run

    run = asyncio.run(go())
    assert os.path.dirname(run.log_path) == str(logs)
    assert os.path.basename(run.log_path).endswith("-1_lexique.jsonl")
    lines = [json.loads(l) for l in open(run.log_path, encoding="utf-8")]
    assert [l["type"] for l in lines] == ["AssistantMessage", "UserMessage", "AssistantMessage",
                                          "ResultMessage", "TaskNotificationMessage",
                                          "AssistantMessage", "ResultMessage"]
    assert lines[1]["message"]["content"][0]["content"] == LAUNCHED
    assert run.snapshot()["log_path"] == run.log_path


def test_worktree_left_behind_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr(runner_mod, "END_GRACE", 0.05)
    repo = tmp_path / "repo"
    repo.mkdir()
    git = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(git[:3] + ["init", "-q"], check=True)
    (repo / "a.txt").write_text("a")
    subprocess.run(git + ["add", "."], check=True)
    subprocess.run(git + ["commit", "-qm", "a"], check=True)
    wt = tmp_path / "wt"
    subprocess.run(git + ["worktree", "add", "-q", str(wt), "HEAD"], check=True)

    async def go(path):
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        run = await rn.start(str(path), "f", "f", "1_lexique", "f")
        await settle()
        clients[0].push(result("Fait.\nNext: done"))
        await asyncio.wait_for(run.task, 3)
        return run

    run = asyncio.run(go(repo))
    assert [os.path.realpath(p) for p in run.worktrees_left] == [os.path.realpath(wt)]
    ended = [e for e in run.events if e["type"] == "run_ended"][0]["data"]
    assert [os.path.realpath(p) for p in ended["worktrees_left"]] == [os.path.realpath(wt)]
    # Nothing left once it is removed.
    subprocess.run(git + ["worktree", "remove", "--force", str(wt)], check=True)
    assert asyncio.run(go(repo)).worktrees_left == []


def test_stop_now_ends_even_with_an_agent_pending(tmp_path):
    async def go():
        clients = []
        rn = make_runner(tmp_path / "logs", clients)
        repo = str(tmp_path)
        run = await rn.start(repo, "f", "f", "1_lexique", "f")
        await settle()
        c = clients[0]
        c.push(*launch())
        await settle(10)
        await rn.stop_now(repo)
        c.push(result("", terminal_reason="aborted_streaming"))
        await asyncio.wait_for(run.task, 3)
        return run, c

    run, c = asyncio.run(go())
    assert c.interrupted and run.outcome == "interrompu"


def test_options_ask_for_session_state_and_can_resume(tmp_path):
    async def cb(*a):
        return None
    opts = runner_mod.build_options(str(tmp_path), cb, resume="sess-7")
    assert opts.resume == "sess-7"
    assert opts.env.get("CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS") == "1"
    assert opts.setting_sources is None
