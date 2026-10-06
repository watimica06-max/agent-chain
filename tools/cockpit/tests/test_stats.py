"""Cockpit 1.4, 1.4.1, 1.4.3 — recording consumption (stats.py, runner.py).
The SDK client is a fake; no chain command runs."""
import asyncio
import json
import os
import shutil
import sqlite3
from datetime import datetime, timedelta, timezone

from claude_agent_sdk import (AssistantMessage, RateLimitEvent, RateLimitInfo, ResultMessage,
                              TaskNotificationMessage, TaskStartedMessage, TextBlock,
                              ToolResultBlock, ToolUseBlock, UserMessage)

import runner as runner_mod
import stats
from test_runner import FakeClient

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE_LOG = os.path.join(HERE, "fixtures", "logs", "2026-10-06-094500-probe.jsonl")
# The first real run from the cockpit: /1_lexique premiere-app-3, the
# lexicographe (Opus) in the background, the orchestrator on Sonnet.
LEXIQUE_LOG = os.path.join(HERE, "fixtures", "logs", "2026-10-06-111521-1_lexique.jsonl")
LEXICOGRAPHE = "toolu_014AQLWfFzCFr7tnqkCwpgYf"

# A placeholder output count, as the CLI sends it on every assistant message.
PLACEHOLDER = 7


def usage(i, cr=0, cc=0):
    return {"input_tokens": i, "cache_read_input_tokens": cr, "cache_creation_input_tokens": cc,
            "output_tokens": PLACEHOLDER}


def am(content, mid, u, parent=None, model="claude-opus-x"):
    return AssistantMessage(content=content, model=model, parent_tool_use_id=parent, usage=u, message_id=mid)


RELAY = "Fini.\nNext: run /2_structure f"


async def two_agents(c):
    """The orchestrator starts « lexicographe » in the background; it reads two
    files in parallel (one message id, two frames), then starts « pong », a
    nested foreground agent that only answers."""
    if c.prompts[-1] == "/usage":
        yield am([TextBlock("usage")], "u-synth", usage(0), model="<synthetic>")
        yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=0, is_error=False, num_turns=0,
                            session_id="s1", result="Current session: 5% used · resets Oct 6, 1:40pm (Asia/Singapore)\n"
                            "Current week (all models): 12% used · resets Oct 12, 7am (Asia/Singapore)\n")
        return
    yield am([ToolUseBlock(id="A", name="Agent", input={"subagent_type": "lexicographe", "description": "Sweep"})],
             "m1", usage(10, 100, 1000))
    yield TaskStartedMessage(subtype="task_started", data={}, task_id="ta", description="Sweep", uuid="u1",
                             session_id="s1", tool_use_id="A")
    yield UserMessage(content=[ToolResultBlock(tool_use_id="A", content="Async agent launched successfully.\nagentId: ta")])
    yield RateLimitEvent(rate_limit_info=RateLimitInfo(
        status="allowed", resets_at=1791265200, rate_limit_type="five_hour", utilization=0.04,
        raw={"status": "allowed", "unifiedWindows": {"five_hour": {"utilization": 0.04, "resetsAt": 1791265200},
                                                     "seven_day": {"utilization": 0.11, "resetsAt": 1791759600}}}),
        uuid="r1", session_id="s1")
    # Parallel tool calls: two frames, one message id, the same usage.
    yield am([ToolUseBlock(id="g1", name="Glob", input={"pattern": "*.md"})], "m2", usage(3000, 200, 50), parent="A")
    yield am([ToolUseBlock(id="g2", name="Glob", input={"pattern": "*.txt"})], "m2", usage(3000, 200, 50), parent="A")
    yield UserMessage(content=[ToolResultBlock(tool_use_id="g1", content="a.md")], parent_tool_use_id="A")
    yield UserMessage(content=[ToolResultBlock(tool_use_id="g2", content="none")], parent_tool_use_id="A")
    yield am([ToolUseBlock(id="B", name="Agent", input={"subagent_type": "pong", "description": "Say pong"})],
             "m3", usage(8, 5000, 400), parent="A")
    # The nested agent: its messages carry its own tool_use id.
    yield am([TextBlock("pong")], "m4", usage(1600, 0, 0), parent="B", model="claude-haiku-x")
    yield am([TextBlock("pong")], "m4", usage(1600, 0, 0), parent="B", model="claude-haiku-x")
    yield UserMessage(content=[ToolResultBlock(tool_use_id="B", content="pong\n<usage>subagent_tokens: 1668</usage>")],
                      parent_tool_use_id="A")
    yield am([TextBlock("done")], "m5", usage(8, 5200, 30), parent="A")
    yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False, num_turns=1,
                        session_id="s1", result="Waiting.",
                        usage={"input_tokens": 10, "output_tokens": 50},
                        model_usage={"claude-opus-x": {"inputTokens": 10, "outputTokens": 50,
                                                       "cacheReadInputTokens": 100, "cacheCreationInputTokens": 1000}})
    yield TaskNotificationMessage(subtype="task_notification", data={}, task_id="ta", status="completed",
                                  output_file="", summary="done", uuid="u2", session_id="s1", tool_use_id="A",
                                  usage={"total_tokens": 5765, "tool_uses": 3, "duration_ms": 7358})
    yield am([TextBlock(RELAY)], "m6", usage(10, 1100, 20))
    # The latest result is the call's running total, subagents included —
    # `usage` alone (the main loop) would undercount.
    yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False, num_turns=1,
                        session_id="s1", result=RELAY, usage={"input_tokens": 10, "output_tokens": 40},
                        model_usage={"claude-opus-x": {"inputTokens": 3046, "outputTokens": 700,
                                                       "cacheReadInputTokens": 11500, "cacheCreationInputTokens": 1500},
                                     "claude-haiku-x": {"inputTokens": 1600, "outputTokens": 68,
                                                        "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0}})


def run_with(tmp_path, script, measure=False, resume=None):
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    made = []

    def factory(cwd, can_use_tool, **kw):
        c = FakeClient(script, can_use_tool)
        made.append(c)
        return c

    rn = runner_mod.Runner(client_factory=factory, log_dir=str(tmp_path / "logs"), stats=store,
                           measure_limits=measure)

    async def go():
        q = rn.subscribe(str(tmp_path))
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f", resume=resume)
        await run.task
        return run
    run = asyncio.run(go())
    return store, run, made


def rows(store, sql, *args):
    db = sqlite3.connect(store.path)
    db.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in db.execute(sql, args)]
    finally:
        db.close()


def test_per_agent_figures_nested_and_deduplicated(tmp_path):
    store, run, _ = run_with(tmp_path, two_agents)
    passes = {p["agent"]: p for p in rows(store, "SELECT * FROM agent_passes WHERE run_id=?", run.id)}
    lex, pong = passes["lexicographe"], passes["pong"]
    # m2 counted once although sent twice; m3 and m5 are the lexicographe's own;
    # m4 is the nested agent's, never the lexicographe's.
    assert (lex["input_tokens"], lex["cache_read_tokens"], lex["cache_creation_tokens"]) == (3016, 10400, 480)
    assert (pong["input_tokens"], pong["cache_read_tokens"], pong["cache_creation_tokens"]) == (1600, 0, 0)
    assert pong["parent_tool_use_id"] == "A" and lex["parent_tool_use_id"] is None
    assert lex["tool_calls"] == 3 and pong["tool_calls"] == 0        # two Glob + one Agent
    assert pong["model"] == "claude-haiku-x"
    # The placeholder (7) is never stored. Pong alone used Haiku, and its sums
    # equal Haiku's model_usage: Haiku's output is its own. The lexicographe
    # shares Opus with the orchestrator: unknown.
    assert pong["output_tokens"] == 68 and lex["output_tokens"] is None
    assert {p["agent"]: p["output_tokens"] for p in run.snapshot()["passes"]} == {"lexicographe": None, "pong": 68}
    # Times: from the Agent call to its result (the background one: its notification).
    assert lex["started_at"] and lex["ended_at"] and lex["duration_s"] is not None
    assert pong["ended_at"] <= lex["ended_at"]


def test_run_totals_come_from_model_usage(tmp_path):
    store, run, _ = run_with(tmp_path, two_agents)
    (r,) = rows(store, "SELECT * FROM runs")
    assert (r["input_tokens"], r["cache_read_tokens"], r["cache_creation_tokens"], r["output_tokens"]) == \
        (4646, 11500, 1500, 768)
    assert r["next_line"] == "Next: run /2_structure f" and r["outcome"] == "terminé"
    assert r["command"] == "/1_lexique f" and r["feature"] == "f" and r["permission_mode"] == "auto"
    assert r["duration_s"] is not None and r["backfilled"] == 0 and r["log_path"] == run.log_path
    assert run.snapshot()["usage"]["output_tokens"] == 768


def test_the_hand_back_event_carries_the_agents_figures(tmp_path):
    _, run, _ = run_with(tmp_path, two_agents)
    ended = {e["data"]["agent"]: e["data"] for e in run.events if e["type"] == "agent_ended"}
    u = ended["pong"]["usage"]
    assert u["read_tokens"] == 1600 and u["output_tokens"] is None and u["duration_s"] is not None
    assert ended["lexicographe"]["usage"]["cache_read_tokens"] == 10400


def test_every_log_line_has_its_receive_time(tmp_path):
    _, run, _ = run_with(tmp_path, two_agents)
    with open(run.log_path, encoding="utf-8") as f:
        lines = [json.loads(l) for l in f]
    assert lines and all(datetime.fromisoformat(l["at"]) for l in lines)
    assert [l["at"] for l in lines] == sorted(l["at"] for l in lines)


def test_a_rate_limit_event_is_stored_with_its_time(tmp_path):
    store, run, _ = run_with(tmp_path, two_agents)
    got = rows(store, "SELECT * FROM rate_limits ORDER BY window")
    assert [(g["window"], g["utilization"], g["resets_at"], g["source"]) for g in got] == \
        [("five_hour", 0.04, 1791265200, "event"), ("seven_day", 0.11, 1791759600, "event")]
    assert all(g["measured_at"] and g["run_id"] == run.id for g in got)
    assert [e["data"]["window"] for e in run.events if e["type"] == "limits"] == ["five_hour", "seven_day"]


def test_usage_is_measured_once_at_the_end_of_the_run(tmp_path):
    store, run, made = run_with(tmp_path, two_agents, measure=True)
    assert made[0].prompts == ["/1_lexique f", "/usage"]
    # The relay is the run's, never the /usage report.
    assert run.relay == RELAY and run.next["kind"] == "run"
    latest = store.latest_limits()
    assert latest["five_hour"]["source"] == "usage" and latest["five_hour"]["utilization"] == 0.05
    assert latest["seven_day"]["utilization"] == 0.12
    expect = int(datetime(2026, 10, 6, 13, 40, tzinfo=timezone(timedelta(hours=8))).timestamp())
    assert latest["five_hour"]["resets_at"] == expect
    # Logged as a probe: the backfill would never count it as the run's work.
    with open(run.log_path, encoding="utf-8") as f:
        probes = [json.loads(l) for l in f if '"probe"' in l]
    assert probes and all(p["probe"] == "usage" for p in probes)


def test_no_usage_report_keeps_the_last_measure(tmp_path):
    async def silent(c):
        if c.prompts[-1] == "/usage":
            yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=0, is_error=False,
                                num_turns=0, session_id="s1", result="Unknown command")
            return
        async for m in two_agents(c):
            yield m
    store, run, _ = run_with(tmp_path, silent, measure=True)
    assert any(e["type"] == "limits_unavailable" for e in run.events)
    assert store.latest_limits()["five_hour"]["source"] == "event"      # the event's, with its own time


def test_a_resumed_run_counts_only_what_it_added(tmp_path):
    store, first, _ = run_with(tmp_path, two_agents)

    async def more(c):
        yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False, num_turns=1,
                            session_id="s1", result="Next: done",
                            model_usage={"m": {"inputTokens": 5000, "outputTokens": 800,
                                               "cacheReadInputTokens": 12000, "cacheCreationInputTokens": 1600}})
    # Same store: a continuation of the same session.
    made = []
    rn = runner_mod.Runner(client_factory=lambda cwd, cut, **kw: made.append(FakeClient(more, cut)) or made[-1],
                           log_dir=str(tmp_path / "logs"), stats=store, measure_limits=False)

    async def go():
        run = await rn.start(str(tmp_path), "f", "f", "1_lexique", "f", resume="s1")
        await run.task
        return run
    second = asyncio.run(go())
    (r,) = rows(store, "SELECT * FROM runs WHERE id=?", second.id)
    assert r["resumed"] == 1
    assert (r["input_tokens"], r["output_tokens"], r["cache_read_tokens"], r["cache_creation_tokens"]) == \
        (5000 - 4646, 800 - 768, 12000 - 11500, 1600 - 1500)


def test_parse_reset_and_usage_text():
    now = datetime(2026, 10, 6, 9, 42, tzinfo=timezone(timedelta(hours=8)))
    assert stats.parse_reset("Oct 12, 7am (Asia/Singapore)", now) == \
        int(datetime(2026, 10, 12, 7, 0, tzinfo=timezone(timedelta(hours=8))).timestamp())
    assert stats.parse_reset("Jan 2, 1:05pm (Asia/Singapore)", datetime(2026, 12, 30, tzinfo=timezone.utc)) == \
        int(datetime(2027, 1, 2, 13, 5, tzinfo=timezone(timedelta(hours=8))).timestamp())
    assert stats.parse_reset("bientôt") is None
    got = stats.limits_from_usage("Current session: 5% used · resets Oct 6, 1:40pm (Asia/Singapore)\n"
                                  "Current week (Fable): 0% used\n", "2026-10-06T09:42:28", now)
    assert [(g["window"], g["utilization"]) for g in got] == [("five_hour", 0.05)]


# ------------------------------------------------------------ backfill

def test_backfill_of_a_real_log(tmp_path):
    """The fixture is a real CLI stream (a probe session with an agent
    nesting another, its paths scrubbed), in the cockpit's log shape."""
    logs = tmp_path / "logs"
    logs.mkdir()
    shutil.copy(PROBE_LOG, logs)
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    path = str(logs / os.path.basename(PROBE_LOG))
    done = store.backfill(str(logs), {os.path.normcase(path): {"work": "premiere-app-3",
                                                                 "command": "/1_lexique premiere-app-3",
                                                                 "outcome": "terminé",
                                                                 "next": {"raw": "Next: done"}}})
    assert done == {"files": 1, "runs": 1, "passes": 2, "limits": 2, "skipped": 0}
    (r,) = rows(store, "SELECT * FROM runs")
    assert r["backfilled"] == 1 and r["feature"] == "premiere-app-3" and r["next_line"] == "Next: done"
    # The call's model_usage of the last result.
    assert (r["input_tokens"], r["output_tokens"], r["cache_read_tokens"], r["cache_creation_tokens"]) == \
        (5433, 817, 51371, 11190)
    passes = {p["agent"]: p for p in rows(store, "SELECT * FROM agent_passes")}
    # Deduplicated per message id, computed apart from the raw frames.
    assert (passes["outer"]["input_tokens"], passes["outer"]["cache_read_tokens"],
            passes["outer"]["cache_creation_tokens"]) == (3805, 5212, 5629)
    assert passes["inner"]["input_tokens"] == 1600 and passes["inner"]["parent_tool_use_id"] == passes["outer"]["tool_use_id"]
    # Input + every pass + the orchestrator's own (28) = the result's input.
    assert passes["outer"]["input_tokens"] + passes["inner"]["input_tokens"] + 28 == r["input_tokens"]
    # Both agents on Haiku, with the orchestrator: neither gets a figure.
    assert all(p["output_tokens"] is None and p["backfilled"] == 1 for p in passes.values())
    # This log carries a receive time on every line: its durations are known.
    assert passes["inner"]["duration_s"] is not None and r["duration_s"] is not None
    assert {l["window"] for l in rows(store, "SELECT * FROM rate_limits")} == {"five_hour", "seven_day"}
    # Once: a second load skips it.
    assert store.backfill(str(logs))["runs"] == 0


def test_backfill_without_receive_times_leaves_durations_unknown(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    with open(PROBE_LOG, encoding="utf-8") as f, open(logs / "2026-10-05-145401-1_lexique.jsonl", "w",
                                                      encoding="utf-8") as g:
        for line in f:
            d = json.loads(line)
            d.pop("at")
            g.write(json.dumps(d, ensure_ascii=False) + "\n")
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    store.backfill(str(logs))
    (r,) = rows(store, "SELECT * FROM runs")
    assert r["duration_s"] is None and r["started_at"] == "2026-10-05T14:54:01" and r["command"] == "/1_lexique"
    assert all(p["duration_s"] is None for p in rows(store, "SELECT * FROM agent_passes"))


# ------------------------------------- output per agent, by model (1.4.3)

def log_tally(path):
    t = stats.Tally()
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            if not d.get("probe"):
                t.feed(d["type"], d["message"], d.get("at"))
    return t


def test_the_real_runs_lexicographe_gets_its_models_output():
    t = log_tally(LEXIQUE_LOG)
    lex = t.passes[LEXICOGRAPHE]
    assert lex.agent == "lexicographe" and lex.model == "claude-opus-5-5" and len(t.passes) == 1
    # Its deduplicated sums from the stream equal Opus's in model_usage exactly.
    opus = t.model_usage["claude-opus-5-5"]
    assert (lex.input_tokens, lex.cache_read_tokens, lex.cache_creation_tokens) == (22, 975519, 137769) ==         (opus["inputTokens"], opus["cacheReadInputTokens"], opus["cacheCreationInputTokens"])
    assert stats.apply_model_usage(t) == 1
    assert lex.output_tokens == 58759
    # The orchestrator's own sums are Sonnet's, which no pass claims.
    son = t.model_usage["claude-sonnet-5-5"]
    assert (t.orchestrator["input_tokens"], t.orchestrator["cache_read_tokens"],
            t.orchestrator["cache_creation_tokens"]) == (son["inputTokens"], son["cacheReadInputTokens"],
                                                         son["cacheCreationInputTokens"])


def test_the_real_run_backfilled_stores_the_lexicographes_output(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    shutil.copy(LEXIQUE_LOG, logs)
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    assert store.backfill(str(logs))["passes"] == 1
    (p,) = rows(store, "SELECT * FROM agent_passes")
    assert (p["agent"], p["output_tokens"]) == ("lexicographe", 58759)
    (r,) = rows(store, "SELECT * FROM runs")
    assert r["output_tokens"] == 3030 + 58759        # the latest result, both models


def test_two_agents_on_one_model_are_both_unknown():
    t = log_tally(LEXIQUE_LOG)
    lex = t.passes[LEXICOGRAPHE]
    other = stats.Pass(tool_use_id="X", parent=None, agent="redacteur", description="", started_at=None,
                       model=lex.model)
    t.passes["X"] = other
    # Even sums that add up to the model's leave each pass unknown.
    other.input_tokens, lex.input_tokens = 2, 20
    assert stats.apply_model_usage(t) == 0
    assert lex.output_tokens is None and other.output_tokens is None


def test_a_models_input_not_matching_the_pass_leaves_it_unknown():
    for key in ("inputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"):
        t = log_tally(LEXIQUE_LOG)
        t.model_usage["claude-opus-5-5"][key] += 1     # something else used Opus too
        assert stats.apply_model_usage(t) == 0
        assert t.passes[LEXICOGRAPHE].output_tokens is None
    # A model the result does not name, or a pass with no model: unknown.
    t = log_tally(LEXIQUE_LOG)
    t.passes[LEXICOGRAPHE].model = "claude-other"
    assert stats.apply_model_usage(t) == 0 and t.passes[LEXICOGRAPHE].output_tokens is None


def test_runs_already_stored_are_filled_from_their_logs(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    shutil.copy(LEXIQUE_LOG, logs)
    store = stats.Store(str(tmp_path / "stats.sqlite"))
    store.backfill(str(logs))
    # A run stored before 1.4.3: its agents without a figure.
    db = sqlite3.connect(store.path)
    with db:
        db.execute("UPDATE agent_passes SET output_tokens=NULL")
    db.close()
    assert store.backfill_outputs() == {"runs": 1, "passes": 1, "unknown": 0}
    assert [p["output_tokens"] for p in rows(store, "SELECT * FROM agent_passes")] == [58759]
    # Once: a run whose agents have their figure is not read again.
    assert store.backfill_outputs()["runs"] == 0
    # A log gone, or one no pass matches: nothing written.
    db = sqlite3.connect(store.path)
    with db:
        db.execute("UPDATE agent_passes SET output_tokens=NULL")
    db.close()
    os.remove(logs / os.path.basename(LEXIQUE_LOG))
    assert store.backfill_outputs() == {"runs": 0, "passes": 0, "unknown": 1}
    assert all(p["output_tokens"] is None for p in rows(store, "SELECT * FROM agent_passes"))
