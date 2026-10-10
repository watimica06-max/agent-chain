"""1.17 — la consommation, mesurée et bornée: the measure (§1) against a fake
client — at start, on the home screen after 15 minutes, its failures, its
cost recorded and marked —; the thresholds (§2), each window, the block and
« Lancer quand même » with its log line, a stale measure refreshed before a
launch; the estimate (§3) from fixture stats. No chain command runs, no real
Claude Code is called."""
import asyncio
import json
import os
import sqlite3
from datetime import datetime, timedelta

import pytest
from aiohttp.test_utils import TestClient, TestServer
from claude_agent_sdk import AssistantMessage, RateLimitEvent, RateLimitInfo, ResultMessage, TextBlock

import runner as runner_mod
import server
import stats as stats_mod
import statsview
import usage
from state import State
from test_runner import FakeClient, script_quick
from test_server import build_app_folder, post

HAIKU = "claude-haiku-5-5"
R5 = int((datetime.now() + timedelta(hours=3)).timestamp())
R7 = int((datetime.now() + timedelta(days=4)).timestamp())


def iso(minutes_ago=0):
    return (datetime.now() - timedelta(minutes=minutes_ago)).isoformat(timespec="milliseconds")


def event(five=0.42, week=0.14):
    raw = {"status": "allowed", "resetsAt": R5, "rateLimitType": "five_hour",
           "unifiedWindows": {"five_hour": {"utilization": five, "resetsAt": R5},
                              "seven_day": {"utilization": week, "resetsAt": R7}}}
    return RateLimitEvent(rate_limit_info=RateLimitInfo(status="allowed", resets_at=R5, rate_limit_type="five_hour",
                                                        utilization=None, raw=raw), uuid="u1", session_id="s")


def answer(error=None):
    return AssistantMessage(content=[TextBlock("ok")], model=HAIKU, error=error, message_id="m1",
                            usage={"input_tokens": 14, "output_tokens": 1, "cache_read_input_tokens": 0,
                                   "cache_creation_input_tokens": 0})


def result(text="ok", is_error=False, model_usage=True):
    mu = {HAIKU: {"inputTokens": 14, "outputTokens": 2, "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0,
                  "costUSD": 0.00002}} if model_usage else None
    return ResultMessage(subtype="success", duration_ms=900, duration_api_ms=800, is_error=is_error, num_turns=1,
                         session_id="s", result=text, model_usage=mu)


USAGE_TEXT = ("Current session: 61% used · resets Oct 6, 1:40pm (Asia/Singapore)\n"
              "Current week (all models): 22% used · resets Oct 12, 7am (Asia/Singapore)\n")


def measure_script(five=0.42, week=0.14, with_event=True):
    async def script(c):
        if c.prompts[-1] == runner_mod.USAGE_COMMAND:
            yield ResultMessage(subtype="success", duration_ms=300, duration_api_ms=0, is_error=False, num_turns=0,
                                session_id="s", result=USAGE_TEXT)
            return
        if with_event:
            yield event(five, week)
        yield answer()
        yield result()
    return script


async def not_logged_in(c):
    yield answer(error="authentication_failed")
    yield result("Not logged in · Please run /login", is_error=True, model_usage=False)


class Factory:
    """The measure's client: a fake, with the folder it was opened in."""

    def __init__(self, script=None, fail=None):
        self.script = script or measure_script()
        self.fail = fail
        self.cwds = []
        self.clients = []

    def __call__(self, cwd):
        self.cwds.append(cwd)
        if self.fail:
            raise self.fail
        c = FakeClient(self.script, None)
        self.clients.append(c)
        return c


def measurer(tmp_path, factory, store=None):
    store = store or stats_mod.Store(str(tmp_path / "stats.sqlite"))
    return usage.Measurer(store, str(tmp_path / "logs"), client_factory=factory, scratch=str(tmp_path / "mesure"))


def add_limit(store, window, utilization, minutes_ago=0, resets_at=None, run_id="r0", source="event"):
    store.record_limit(run_id, {"measured_at": iso(minutes_ago), "source": source, "window": window,
                                "utilization": utilization,
                                "resets_at": resets_at if resets_at is not None else (R5 if window == "five_hour" else R7)})


def add_both(store, five, week, minutes_ago=0):
    add_limit(store, "five_hour", five, minutes_ago)
    add_limit(store, "seven_day", week, minutes_ago)


# ----------------------------------------------------------------- §1 measure

def test_the_measure_reads_both_windows_and_records_its_cost_marked(tmp_path):
    f = Factory()
    m = measurer(tmp_path, f)
    last = asyncio.run(m._measure("test"))
    assert last["ok"] and last["error"] == "" and last["windows"] == ["five_hour", "seven_day"]
    # In a scratch folder of its own, never an application's; one short prompt.
    assert f.cwds == [str(tmp_path / "mesure")] and f.clients[0].prompts == [usage.PROMPT]
    got = m.store.latest_limits()
    assert got["five_hour"]["utilization"] == 0.42 and got["five_hour"]["resets_at"] == R5
    assert got["seven_day"]["utilization"] == 0.14 and got["seven_day"]["resets_at"] == R7
    assert {got[w]["source"] for w in got} == {"mesure"}
    # Its cost, recorded like a run's, marked as a measure.
    db = sqlite3.connect(m.store.path)
    db.row_factory = sqlite3.Row
    row = dict(db.execute("SELECT * FROM runs").fetchone())
    db.close()
    assert row["kind"] == "mesure" and row["command"] == usage.COMMAND and row["app"] is None
    assert row["input_tokens"] == 14 and row["output_tokens"] == 2 and row["outcome"] == "terminé"
    assert last["cost"]["read_tokens"] == 14 and last["cost"]["output_tokens"] == 2 and last["cost"]["usd"] == 0.00002
    # Its log, beside the run logs; the statistics name it as itself.
    assert os.path.basename(row["log_path"]).endswith("-mesure.jsonl")
    data = statsview.build(m.store.path)
    assert [r["cmd"] for r in data["runs"]] == [usage.COMMAND] and data["runs"][0]["kind"] == "mesure"


def test_the_lightest_session_no_tool_no_setting_one_turn(tmp_path):
    o = usage.build_options(str(tmp_path))
    assert o.tools == [] and o.setting_sources == [] and o.max_turns == 1 and o.model == "haiku"
    assert o.strict_mcp_config and o.mcp_servers == {} and o.thinking == {"type": "disabled"}
    assert o.cwd == str(tmp_path)


def test_no_event_then_usage_in_the_same_session(tmp_path):
    f = Factory(measure_script(with_event=False))
    m = measurer(tmp_path, f)
    last = asyncio.run(m._measure("test"))
    assert last["ok"] and f.clients[0].prompts == [usage.PROMPT, "/usage"]
    got = m.store.latest_limits()
    assert got["five_hour"]["utilization"] == 0.61 and got["seven_day"]["utilization"] == 0.22
    assert got["five_hour"]["source"] == "mesure" and got["five_hour"]["resets_at"]


@pytest.mark.parametrize("factory, said", [
    (Factory(not_logged_in), "n'est pas connecté"),
    (Factory(fail=ConnectionError("getaddrinfo ENOTFOUND api.anthropic.com")), "hors ligne"),
    (Factory(fail=type("CLINotFoundError", (Exception,), {})("claude")), "introuvable"),
])
def test_a_failed_measure_says_why_and_stores_no_level(tmp_path, factory, said):
    m = measurer(tmp_path, factory)
    last = asyncio.run(m._measure("test"))
    assert last["ok"] is False and said in last["error"]
    assert m.store.latest_limits() == {}
    assert m.public()["going"] is False


def test_oldest_age_is_the_staler_window(tmp_path):
    store = stats_mod.Store(str(tmp_path / "s.sqlite"))
    assert usage.oldest_age(store.latest_limits()) is None
    add_limit(store, "five_hour", 0.1, minutes_ago=2)
    assert usage.oldest_age(store.latest_limits()) is None            # the week never measured
    add_limit(store, "seven_day", 0.1, minutes_ago=20)
    assert 19 * 60 < usage.oldest_age(store.latest_limits()) < 21 * 60


# ------------------------------------------------------------ server helpers

def served(tmp_path, body, factory=None, auto=True, run_script=script_quick, monkeypatch=None):
    app_root = tmp_path / "app"
    build_app_folder(app_root)
    st = State(str(tmp_path / "config.json"))
    st.add_app(str(app_root))
    st.open_pair(str(app_root), "f")
    store = stats_mod.Store(str(tmp_path / "stats.sqlite"))
    made = []

    def run_factory(cwd, can_use_tool, **kw):
        c = FakeClient(run_script, can_use_tool)
        made.append(c)
        return c
    rn = runner_mod.Runner(client_factory=run_factory, on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"), stats=store)
    meas = measurer(tmp_path, factory or Factory(), store)
    monkeypatch.setattr(server, "MEASURE_USAGE", auto)
    app = server.make_app(st, rn, picker=lambda initial: str(app_root), measurer=meas)

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            c.ctx = {"state": st, "store": store, "meas": meas, "made": made, "app": app_root, "rn": rn}
            return await body(c)
    return asyncio.run(go())


async def settle(meas):
    if meas.task:
        await asyncio.gather(meas.task, return_exceptions=True)


async def ended(rn, app):
    await rn.wait_ended(str(app), 5)


# ---------------------------------------------------- §1 through the server

def test_measured_when_the_cockpit_starts(tmp_path, monkeypatch):
    f = Factory()

    async def body(c):
        await settle(c.ctx["meas"])
        assert len(f.cwds) == 1 and c.ctx["meas"].last["why"] == "au démarrage du cockpit"
        u = (await (await c.get("/api/state")).json())["usage"]
        assert u["measure"]["ok"] and u["levels"]["five_hour"]["pct"] == 42.0 and u["levels"]["five_hour"]["level"] == "ok"
        assert u["thresholds"] == usage.DEFAULT_THRESHOLDS
    served(tmp_path, body, f, monkeypatch=monkeypatch)


def test_the_home_screen_measures_again_after_15_minutes_only(tmp_path, monkeypatch):
    f = Factory()

    async def body(c):
        meas, store = c.ctx["meas"], c.ctx["store"]
        await settle(meas)
        f.cwds.clear()
        # Fresh: the home screen opens, nothing is measured.
        await (await c.get("/api/apps")).json()
        await settle(meas)
        assert f.cwds == []
        # Older than 15 minutes: measured again, in the background.
        with sqlite3.connect(store.path) as db:
            db.execute("UPDATE rate_limits SET measured_at=?", (iso(16),))
        r = await (await c.get("/api/apps")).json()
        assert "usage" in r
        await settle(meas)
        assert len(f.cwds) == 1 and meas.last["why"] == "à l'ouverture de l'écran d'accueil"
        assert usage.oldest_age(store.latest_limits()) < 60
    served(tmp_path, body, f, monkeypatch=monkeypatch)


def test_a_failed_measure_never_blocks_the_page(tmp_path, monkeypatch):
    async def body(c):
        await settle(c.ctx["meas"])
        r = await c.get("/api/state")
        assert r.status == 200
        u = (await r.json())["usage"]
        assert u["measure"]["ok"] is False and "n'est pas connecté" in u["measure"]["error"]
        assert (await c.get("/api/apps")).status == 200
        # Nor a launch: the latest level is unknown, nothing blocks.
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200, await r.text()
        await ended(c.ctx["rn"], c.ctx["app"])
    served(tmp_path, body, Factory(not_logged_in), monkeypatch=monkeypatch)


# --------------------------------------------------------------- §2 levels

@pytest.mark.parametrize("window", ["five_hour", "seven_day"])
@pytest.mark.parametrize("pct, warn, block, level", [
    (0.50, 80, 95, "ok"), (0.80, 80, 95, "warn"), (0.94, 80, 95, "warn"), (0.95, 80, 95, "block"),
    (0.90, 90, 90, "block"), (0.89, 90, 90, "ok"),
])
def test_each_threshold_of_each_window(window, pct, warn, block, level):
    th = usage.clean_thresholds({window: {"warn": warn, "block": block}})
    other = "seven_day" if window == "five_hour" else "five_hour"
    lim = {window: {"utilization": pct, "resets_at": R5, "measured_at": iso(1)},
           other: {"utilization": 0.10, "resets_at": R7, "measured_at": iso(1)}}
    lv = usage.levels(lim, th)
    assert lv[window]["level"] == level and lv[other]["level"] == "ok"
    assert [x["window"] for x in usage.blocking(lv)] == ([window] if level == "block" else [])


def test_a_window_whose_reset_passed_neither_warns_nor_blocks():
    past = int((datetime.now() - timedelta(minutes=5)).timestamp())
    lv = usage.levels({"five_hour": {"utilization": 0.99, "resets_at": past, "measured_at": iso(300)}},
                      usage.clean_thresholds(None))
    assert lv["five_hour"]["level"] == "reset" and lv["seven_day"]["level"] == "inconnu"
    assert usage.blocking(lv) == []


def test_thresholds_default_90_and_out_of_range_refused(tmp_path):
    assert usage.clean_thresholds(None) == {"five_hour": {"warn": 90, "block": 90}, "seven_day": {"warn": 90, "block": 90}}
    assert usage.clean_thresholds({"seven_day": {"block": "95"}})["seven_day"] == {"warn": 90, "block": 95}
    for bad in (0, 101, "abc"):
        with pytest.raises(ValueError):
            usage.clean_thresholds({"five_hour": {"warn": bad}})
    st = State(str(tmp_path / "config.json"))
    assert st.usage_thresholds == usage.DEFAULT_THRESHOLDS
    st.set_usage_thresholds({"five_hour": {"warn": 70, "block": 85}})
    assert State(str(tmp_path / "config.json")).usage_thresholds["five_hour"] == {"warn": 70, "block": 85}


# ----------------------------------------------------- §2 through the server

def test_the_thresholds_saved_from_parametres(tmp_path, monkeypatch):
    async def body(c):
        r = await post(c, "/api/usage/thresholds", {"thresholds": {"five_hour": {"warn": 75, "block": 88},
                                                                   "seven_day": {"warn": 80, "block": 97}}})
        u = await r.json()
        assert r.status == 200 and u["thresholds"]["seven_day"] == {"warn": 80, "block": 97}
        assert c.ctx["state"].usage_thresholds["five_hour"] == {"warn": 75, "block": 88}
        r = await post(c, "/api/usage/thresholds", {"thresholds": {"five_hour": {"warn": 120}}})
        assert r.status == 400 and "de 1 à 100" in (await r.json())["error"]
    served(tmp_path, body, auto=False, monkeypatch=monkeypatch)


@pytest.mark.parametrize("window", ["five_hour", "seven_day"])
def test_the_block_and_lancer_quand_meme_logged(tmp_path, monkeypatch, window):
    async def body(c):
        store = c.ctx["store"]
        add_both(store, 0.95 if window == "five_hour" else 0.30, 0.92 if window == "seven_day" else 0.30)
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        b = await r.json()
        assert r.status == 409 and "Seuil de blocage atteint" in b["error"] and "Rien n'a été lancé" in b["error"]
        assert [x["window"] for x in b["usage_block"]["windows"]] == [window]
        assert c.ctx["made"] == []
        assert not (tmp_path / "logs" / usage.OVERRIDE_LOG).exists()
        # « Lancer quand même »: launched, and logged.
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f", "usage_ok": True})
        assert r.status == 200, await r.text()
        await ended(c.ctx["rn"], c.ctx["app"])
        assert len(c.ctx["made"]) == 1
        line = (tmp_path / "logs" / usage.OVERRIDE_LOG).read_text(encoding="utf-8")
        assert "seuil de blocage passé outre" in line and "/1_lexique f" in line and "« app »" in line
        assert usage.WINDOW_NAMES[window] in line and "(seuil de blocage 90 %)" in line
    served(tmp_path, body, auto=False, monkeypatch=monkeypatch)


def test_a_warning_alone_launches(tmp_path, monkeypatch):
    async def body(c):
        c.ctx["state"].set_usage_thresholds({"five_hour": {"warn": 80, "block": 99}})
        add_both(c.ctx["store"], 0.85, 0.10)
        u = (await (await c.get("/api/state")).json())["usage"]
        assert u["levels"]["five_hour"]["level"] == "warn"
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200, await r.text()
        await ended(c.ctx["rn"], c.ctx["app"])
    served(tmp_path, body, auto=False, monkeypatch=monkeypatch)


def test_continuing_a_session_is_gated_too(tmp_path, monkeypatch):
    async def body(c):
        add_both(c.ctx["store"], 0.97, 0.10)
        r = await post(c, "/api/continue-session", {})
        assert r.status == 409 and (await r.json())["usage_block"]
    served(tmp_path, body, auto=False, monkeypatch=monkeypatch)


def test_a_stale_measure_is_refreshed_before_a_launch(tmp_path, monkeypatch):
    f = Factory(measure_script(five=0.96, week=0.20))

    async def body(c):
        meas, store = c.ctx["meas"], c.ctx["store"]
        await settle(meas)                               # the start's measure: 96 %
        with sqlite3.connect(store.path) as db:          # …then 16 minutes old, and 50 %
            db.execute("UPDATE rate_limits SET measured_at=?, utilization=0.5", (iso(16),))
        f.cwds.clear()
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        # Measured again first — 96 % again: blocked on the new figure, not the old one.
        assert len(f.cwds) == 1 and meas.last["why"] == "avant de lancer /1_lexique f"
        assert r.status == 409 and (await r.json())["usage_block"]["windows"][0]["pct"] == 96.0
        # Fresh now: the next launch is not measured again.
        f.cwds.clear()
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f", "usage_ok": True})
        assert r.status == 200 and f.cwds == []
        await ended(c.ctx["rn"], c.ctx["app"])
    served(tmp_path, body, f, monkeypatch=monkeypatch)


# --------------------------------------------------------------- §3 estimate

def add_run(store, run_id, app, command, start, end, minutes_ago=30, week=None):
    t = stats_mod.Tally()
    store.record_run(run_id=run_id, feature="f", work="f", command=command, mode="auto",
                     started_at=iso(minutes_ago), ended_at=iso(minutes_ago - 5), tally=t, next_line=None,
                     outcome="terminé", log_path=None, app=app)
    for w, (a, b) in (("five_hour", (start, end)), ("seven_day", week or (0.10, 0.11))):
        add_limit(store, w, a, minutes_ago=minutes_ago, run_id=run_id, source="event")
        add_limit(store, w, b, minutes_ago=minutes_ago - 5, run_id=run_id, source="usage")


def test_the_median_per_application_else_all_else_unknown(tmp_path):
    store = stats_mod.Store(str(tmp_path / "s.sqlite"))
    here, there = str(tmp_path / "here"), str(tmp_path / "there")
    # /1_lexique: three runs here — 3, 4 and 6 points.
    for i, (a, b) in enumerate([(0.10, 0.13), (0.20, 0.24), (0.30, 0.36)]):
        add_run(store, f"l{i}", here, "/1_lexique f", a, b)
    # /4_grille: one here, two elsewhere — 10, 2, 5: across all.
    add_run(store, "g0", here, "/4_grille f", 0.10, 0.20)
    add_run(store, "g1", there, "/4_grille g", 0.10, 0.12)
    add_run(store, "g2", there, "/4_grille g", 0.10, 0.15)
    # /8_code: two runs — « inconnu ».
    add_run(store, "c0", here, "/8_code f", 0.10, 0.30)
    add_run(store, "c1", here, "/8_code f 2", 0.10, 0.40)
    # A measure is no command, and a run across a reset is left out.
    add_run(store, "x", here, "/1_lexique f", 0.50, 0.10, week=(0.50, 0.10))
    asyncio.run(usage.Measurer(store, str(tmp_path / "logs"), client_factory=Factory(),
                               scratch=str(tmp_path / "mesure"))._measure("test"))
    est = usage.estimates(store.path, here)
    assert est["/1_lexique"]["five_hour"] == {"median": 4.0, "n": 3, "scope": "app"}
    assert est["/1_lexique"]["seven_day"] == {"median": 1.0, "n": 3, "scope": "app"}
    assert est["/4_grille"]["five_hour"] == {"median": 5.0, "n": 3, "scope": "all"}
    assert est["/8_code"]["five_hour"] == {"median": None, "n": 2, "scope": None}
    assert usage.COMMAND not in est and "(mesure" not in json.dumps(est)
    # Another application: /1_lexique's three are not its own — across all.
    assert usage.estimates(store.path, there)["/1_lexique"]["five_hour"]["scope"] == "all"


def test_the_estimate_is_in_the_state(tmp_path, monkeypatch):
    async def body(c):
        for i, (a, b) in enumerate([(0.10, 0.13), (0.20, 0.24), (0.30, 0.36)]):
            add_run(c.ctx["store"], f"l{i}", str(c.ctx["app"]), "/1_lexique f", a, b)
        s = await (await c.get("/api/state")).json()
        assert s["estimates"]["/1_lexique"]["five_hour"]["median"] == 4.0
    served(tmp_path, body, auto=False, monkeypatch=monkeypatch)


def test_a_measure_is_never_given_an_application(tmp_path):
    f = Factory()
    m = measurer(tmp_path, f)
    asyncio.run(m._measure("test"))
    assert m.store.backfill_apps(lambda run: "C:/une-app") == 0
