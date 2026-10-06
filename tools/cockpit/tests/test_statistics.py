"""Cockpit 1.4.5 — the « Statistiques » screen's data (statsview.py) and its
routes, on a fixture store. No chain command runs."""
import asyncio
import json
import os
import sqlite3
from datetime import datetime, timedelta

import pytest
from aiohttp.test_utils import TestClient, TestServer

import runner as runner_mod
import server
import stats
import statsview
from state import State
from test_runner import FakeClient
from test_server import build_app_folder

R1_LOG = r"C:\logs\r1.jsonl"


def _iso(t):
    return t.isoformat(timespec="seconds")


def fixture_store(path, now=None):
    """Four runs over two features and forty days:
    - r1 `/1_lexique f`, today: two passes, the sondeur's output unknown;
      three limit measures, the window steady → ≈ 5 % of the 5-hour window;
    - r2 `/4_grille f`, 3 days ago: its own output unknown, two sondeurs both
      unknown; only the end-of-run `/usage` → no start, no difference;
    - r3 `/1_lexique g`, 20 days ago: the 5-hour window reset during the run;
    - r4 `/1_lexique g`, 40 days ago: ten times the read of the others, a
      lexicographe ten times its median → « inhabituel »."""
    now = now or datetime.now()
    store = stats.Store(path)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    t1 = max(now - timedelta(minutes=15), midnight + timedelta(seconds=1))
    runs = [
        ("r1", "f", "/1_lexique f", t1, 600, (10, 1000, 100), 500, "terminé", "Next: run /2_structure f", R1_LOG),
        ("r2", "f", "/4_grille f", now - timedelta(days=3), 1200, (20, 2000, 200), None, "terminé",
         "Next: answer questions, then run /4_grille f", r"C:\logs\r2.jsonl"),
        ("r3", "g", "/1_lexique g", now - timedelta(days=20), None, (10, 1200, 100), 400, "arrêté", None, None),
        ("r4", "g", "/1_lexique g", now - timedelta(days=40), 900, (100, 12000, 1000), 4000, "terminé", None, None),
    ]
    passes = [  # run, agent, model, offset s, duration, (input, cache read, cache creation), output, tools
        ("r1", "lexicographe", "claude-opus-5-5", 20, 400, (5, 700, 95), 400, 30),
        ("r1", "sondeur", "claude-sonnet-5-5", 30, 100, (1, 99, 0), None, 4),
        ("r2", "sondeur", "claude-opus-5-5", 10, 500, (5, 900, 95), None, 12),
        ("r2", "sondeur", "claude-opus-5-5", 10, 520, (5, 950, 45), None, 14),
        ("r3", "lexicographe", "claude-opus-5-5", 10, None, (5, 900, 95), 300, 20),
        ("r4", "lexicographe", "claude-opus-5-5", 10, 800, (50, 9950, 1000), 3500, 90),
    ]
    reset1 = int((t1 + timedelta(hours=3)).timestamp())
    limits = [  # run, offset s, source, window, utilization, resets_at
        ("r1", 5, "event", "five_hour", 0.20, reset1), ("r1", 5, "event", "seven_day", 0.40, reset1 + 86400 * 3),
        ("r1", 300, "event", "five_hour", 0.22, reset1),
        ("r1", 600, "usage", "five_hour", 0.25, reset1), ("r1", 600, "usage", "seven_day", 0.41, reset1 + 86400 * 3),
        ("r2", 1200, "usage", "five_hour", 0.50, None),
        ("r3", 5, "event", "five_hour", 0.80, int((now - timedelta(days=20) + timedelta(minutes=20)).timestamp())),
        ("r3", 3600, "usage", "five_hour", 0.05, int((now - timedelta(days=20) + timedelta(hours=5)).timestamp())),
    ]
    start = {r[0]: r[3] for r in runs}
    db = sqlite3.connect(path)
    with db:
        for rid, feat, cmd, t, dur, (i, cr, cc), out, outcome, nxt, log in runs:
            db.execute("INSERT INTO runs (id, feature, work, command, permission_mode, session_id, started_at,"
                       " ended_at, duration_s, input_tokens, cache_read_tokens, cache_creation_tokens,"
                       " output_tokens, next_line, outcome, log_path) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (rid, feat, feat, cmd, "auto", "s-" + rid, _iso(t),
                        _iso(t + timedelta(seconds=dur or 60)) if dur else None, dur, i, cr, cc, out,
                        nxt, outcome, log))
        for k, (rid, agent, model, off, dur, (i, cr, cc), out, tools) in enumerate(passes):
            st = start[rid] + timedelta(seconds=off)
            db.execute("INSERT INTO agent_passes (run_id, tool_use_id, agent, description, model, started_at,"
                       " ended_at, duration_s, input_tokens, cache_read_tokens, cache_creation_tokens,"
                       " output_tokens, tool_calls) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (rid, f"tu{k}", agent, f"{agent} {rid}", model, _iso(st),
                        _iso(st + timedelta(seconds=dur)) if dur else None, dur, i, cr, cc, out, tools))
        for rid, off, src, w, u, reset in limits:
            db.execute("INSERT INTO rate_limits (run_id, measured_at, source, window, utilization, resets_at)"
                       " VALUES (?,?,?,?,?,?)", (rid, _iso(start[rid] + timedelta(seconds=off)), src, w, u, reset))
    db.close()
    return store


@pytest.fixture
def store(tmp_path):
    return fixture_store(str(tmp_path / "stats.sqlite"))


def ids(data):
    return [r["id"] for r in data["runs"]]


def test_runs_and_passes_per_filter(store):
    assert ids(statsview.build(store.path, "f", "jour")) == ["r1"]
    assert ids(statsview.build(store.path, "f", "7j")) == ["r1", "r2"]          # newest first
    assert ids(statsview.build(store.path, "g", "30j")) == ["r3"]
    every = statsview.build(store.path, None, "tout")
    assert ids(every) == ["r1", "r2", "r3", "r4"]
    assert every["passes_count"] == 6 and every["features"] == ["f", "g"]
    d = statsview.build(store.path, "f", "7j")
    assert [p["agent"] for r in d["runs"] for p in r["passes"]] == ["lexicographe", "sondeur", "sondeur", "sondeur"]
    # « Par fonctionnalité » only for « toutes ».
    assert d["by_feature"] == [] and [x["feature"] for x in every["by_feature"]] == ["f", "g"]
    # The limit measures of the period, every one a point.
    assert len(statsview.build(store.path, "f", "jour")["limits"]) == 5
    # An unknown period reads as « tout ».
    assert statsview.build(store.path, None, "n'importe")["period"] == "tout"


def test_an_unknown_output_is_left_out_of_a_sum_and_counted(store):
    d = statsview.build(store.path, "f", "7j")
    t = d["totals"]
    assert t["runs"] == 2 and t["output_tokens"] == 500 and t["output_unknown"] == 1
    assert t["read_tokens"] == 1110 + 2220 and t["read_unknown"] == 0
    assert t["duration_s"] == 1800 and t["duration_unknown"] == 0
    agents = {a["agent"]: a for a in d["by_agent"]}
    # Three sondeur passes, none with a figure of its own: the sum is unknown, never 0.
    assert agents["sondeur"]["passes"] == 3
    assert agents["sondeur"]["output_tokens"] is None and agents["sondeur"]["output_unknown"] == 3
    assert agents["sondeur"]["models"] == ["claude-opus-5-5", "claude-sonnet-5-5"]
    assert agents["lexicographe"]["output_tokens"] == 400 and agents["lexicographe"]["output_unknown"] == 0
    cmds = {c["cmd"]: c for c in d["by_command"]}
    assert cmds["/4_grille"]["output_tokens"] is None and cmds["/4_grille"]["output_unknown"] == 1
    # A duration the store lacks: left out of the total, counted.
    g = statsview.build(store.path, "g", "tout")["totals"]
    assert g["duration_s"] == 900 and g["duration_unknown"] == 1


def test_what_a_run_took_from_the_limits(store):
    runs = {r["id"]: r for r in statsview.build(store.path, None, "tout")["runs"]}
    five = runs["r1"]["limits"]["five_hour"]
    assert five == {"start": 0.20, "end": 0.25, "delta": 5.0, "why": None}      # its first measure, its /usage
    assert runs["r1"]["limits"]["seven_day"]["delta"] == 1.0
    # A measure missing: empty, with the reason.
    assert runs["r2"]["limits"]["five_hour"]["delta"] is None
    assert runs["r2"]["limits"]["five_hour"]["why"] == "pas de mesure au début du run"
    assert runs["r4"]["limits"]["five_hour"]["why"] == "pas de mesure /usage en fin de run"
    # The window reset during the run: empty.
    assert runs["r3"]["limits"]["five_hour"]["delta"] is None
    assert "réinitialisée" in runs["r3"]["limits"]["five_hour"]["why"]
    # Summed over the runs that have it, the others counted.
    t = statsview.build(store.path, None, "tout")["totals"]
    assert t["five_hour"] == 5.0 and t["five_hour_unknown"] == 3


def test_limit_delta_never_across_a_reset():
    m = lambda at, src, u, reset: {"measured_at": at, "source": src, "utilization": u, "resets_at": reset}  # noqa: E731
    base = 1791265200
    ok = [m("2026-10-06T11:15:27", "event", .27, base), m("2026-10-06T11:24:14", "usage", .31, base + 20)]
    assert statsview.limit_delta(ok)["delta"] == 4.0                       # `/usage` reads the reset to the minute
    moved = [ok[0], m("2026-10-06T11:24:14", "usage", .31, base + 5 * 3600)]
    assert statsview.limit_delta(moved)["delta"] is None                   # resets_at changed
    dropped = [ok[0], m("2026-10-06T11:24:14", "usage", .02, None)]
    assert statsview.limit_delta(dropped)["delta"] is None                 # the figure went down
    passed = [m("2026-10-06T11:15:27", "event", .27, int(datetime(2026, 10, 6, 11, 20).timestamp())),
              m("2026-10-06T11:24:14", "usage", .31, None)]
    assert statsview.limit_delta(passed)["delta"] is None                  # its reset came before the end
    assert statsview.limit_delta([ok[1]])["delta"] is None
    assert statsview.limit_delta([ok[0]])["delta"] is None


def test_the_unusual_mark(store):
    d = statsview.build(store.path, None, "tout")
    runs = {r["id"]: r for r in d["runs"]}
    # /1_lexique: reads 1 110, 1 310, 13 100 — median 1 310; r4 is above twice it.
    assert runs["r4"]["unusual"] and runs["r4"]["group_median_read"] == 1310
    assert not runs["r1"]["unusual"] and not runs["r3"]["unusual"]
    lex = [p for r in d["runs"] for p in r["passes"] if p["agent"] == "lexicographe"]
    assert [p["unusual"] for p in lex] == [False, False, True]
    # Over the whole store, not the filter: r4 stays « inhabituel » seen alone.
    alone = statsview.build(store.path, "g", "tout")
    assert {r["id"]: r["unusual"] for r in alone["runs"]} == {"r3": False, "r4": True}
    # The ten most expensive, by tokens read.
    assert d["costly_runs"] == ["r4", "r2", "r3", "r1"]
    assert len(d["costly_passes"]) == 6 and d["costly_passes"][0]["run_id"] == "r4"


def test_the_store_is_read_only(store):
    before = os.path.getmtime(store.path), os.path.getsize(store.path)
    statsview.build(store.path, None, "tout")
    assert (os.path.getmtime(store.path), os.path.getsize(store.path)) == before
    with pytest.raises(sqlite3.OperationalError):
        statsview._connect(store.path).execute("DELETE FROM runs")
    missing = statsview.build(os.path.join(os.path.dirname(store.path), "absent.sqlite"))
    assert missing["runs"] == [] and missing["error"] == "aucune base stats.sqlite"
    assert not os.path.exists(os.path.join(os.path.dirname(store.path), "absent.sqlite"))


def test_the_csv_export(store):
    d = statsview.build(store.path, "f", "7j")
    (rname, rtext), (pname, ptext) = statsview.csv_files(d)
    assert rname.startswith("cockpit-runs-f-7j-") and pname.startswith("cockpit-passages-f-7j-")
    assert rtext.startswith("\ufeff")
    lines = rtext.lstrip("\ufeff").splitlines()
    head = lines[0].split(";")
    assert head[:5] == ["début", "fin", "application", "fonctionnalité", "commande"] and "≈ % de la fenêtre 5 h" in head
    rows = [dict(zip(head, ln.split(";"))) for ln in lines[1:]]
    assert [r["commande"] for r in rows] == ["/1_lexique f", "/4_grille f"]
    assert rows[0]["tokens écrits"] == "500" and rows[1]["tokens écrits"] == "inconnu"
    assert rows[0]["≈ % de la fenêtre 5 h"] == "5" and rows[0]["5 h au début (%)"] == "20"
    assert rows[1]["≈ % de la fenêtre 5 h"] == "pas de mesure au début du run"
    plines = ptext.lstrip("\ufeff").splitlines()
    assert len(plines) == 1 + 4
    phead = plines[0].split(";")
    prow = [dict(zip(phead, ln.split(";"))) for ln in plines[1:]]
    assert [p["tokens écrits"] for p in prow] == ["400", "inconnu", "inconnu", "inconnu"]


# ----------------------------------------------------------------- routes

def serve(tmp_path, store, body, export_picker=None):
    app_root = tmp_path / "app"
    build_app_folder(app_root)
    st = State(str(tmp_path / "config.json"))
    st.open_pair(str(app_root), "f")
    rn = runner_mod.Runner(client_factory=lambda cwd, cb, **kw: FakeClient(None, cb),
                           log_dir=str(tmp_path / "logs"), stats=store)
    app = server.make_app(st, rn, **({"export_picker": export_picker} if export_picker else {}))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            await body(c)
    asyncio.run(go())


def test_stats_routes(tmp_path, store):
    async def body(c):
        d = await (await c.get("/api/stats")).json()
        assert d["feature"] == "f" and d["period"] == "tout" and ids(d) == ["r1", "r2"]     # the open feature
        d = await (await c.get("/api/stats?feature=*&period=jour")).json()
        assert d["feature"] is None and ids(d) == ["r1"]
        d = await (await c.get("/api/stats?feature=g&period=tout")).json()
        assert ids(d) == ["r3", "r4"]
        r = await c.get("/api/stats/csv?kind=passes&feature=f&period=7j")
        assert r.status == 200 and r.content_type == "text/csv"
        assert "cockpit-passages-app-f-7j" in r.headers["Content-Disposition"]      # 1.6: the application named
        assert (await r.text()).count("\r\n") == 5
    serve(tmp_path, store, body)


def test_stats_export_writes_two_files_where_chosen(tmp_path, store):
    out = tmp_path / "choisi"
    out.mkdir()
    picked = []

    def picker(initial):
        picked.append(initial)
        return str(out)

    async def body(c):
        r = await c.post("/api/stats/export", data=json.dumps({"feature": "*", "period": "tout"}),
                         headers={"Content-Type": "application/json"})
        files = (await r.json())["files"]
        assert r.status == 200 and len(files) == 2
        assert sorted(os.listdir(out)) == sorted(os.path.basename(f) for f in files)
        runs = (out / os.path.basename(files[0])).read_text(encoding="utf-8-sig").splitlines()
        assert len(runs) == 1 + 4
    serve(tmp_path, store, body, export_picker=picker)
    assert picked and os.path.isdir(picked[0])


def test_stats_export_cancelled_writes_nothing(tmp_path, store):
    async def body(c):
        r = await c.post("/api/stats/export", data="{}", headers={"Content-Type": "application/json"})
        assert (await r.json()) == {"cancelled": True}
    serve(tmp_path, store, body, export_picker=lambda initial: "")


def test_stats_without_a_store(tmp_path):
    async def body(c):
        d = await (await c.get("/api/stats")).json()
        assert d["runs"] == [] and d["error"] and d["totals"]["runs"] == 0
    serve(tmp_path, None, body)


# ------------------------------------------------------------- 1.5: par lot

def test_by_lot_one_feature_filtered(tmp_path):
    """« Par lot »: the passes the store gives a lot, by working folder and
    lot; a lot's time its top-level passes', a nested one inside its
    caller's; no section for « Toutes »."""
    path = str(tmp_path / "s.sqlite")
    stats.Store(path)
    db = sqlite3.connect(path)
    db.execute("INSERT INTO runs (id, feature, command, started_at) VALUES ('r1', 'f', '/8_code f', ?)",
               (datetime.now().isoformat(timespec="seconds"),))
    rows = [("t1", None, "concepteur", 100, 5, "lot-01", ""), ("t2", None, "realisateur", 300, None, "lot-01", ""),
            ("t3", "t2", "arbitre", 120, 7, "lot-01", ""), ("t4", None, "realisateur", 50, 3, "lot-01", "bugfix-02"),
            ("t5", None, "detailleur", 400, 9, None, "")]
    for tid, parent, agent, dur, out, lot, folder in rows:
        db.execute("INSERT INTO agent_passes (run_id, tool_use_id, parent_tool_use_id, agent, duration_s, input_tokens,"
                   " cache_read_tokens, cache_creation_tokens, output_tokens, lot, folder) VALUES"
                   " ('r1', ?, ?, ?, ?, 10, 0, 0, ?, ?, ?)", (tid, parent, agent, dur, out, lot, folder))
    db.commit()
    db.close()
    d = statsview.build(path, "f", "tout")
    by = {(r["folder"], r["lot"]): r for r in d["by_lot"]}
    main = by[("", "lot-01")]
    assert main["passes"] == 3 and main["duration_s"] == 400 and main["read_tokens"] == 30
    assert main["output_tokens"] == 12 and main["output_unknown"] == 1 and main["codings"] == 1
    assert by[("bugfix-02", "lot-01")]["passes"] == 1
    assert d["by_lot_unknown"] == 1                          # the Détailleur's, on a block
    assert statsview.build(path, None, "tout")["by_lot"] == []


def test_an_ignored_feature_is_in_no_filter_no_table_no_total(store):
    # 1.5.1: config.json « ignored » — its runs and their passes leave the screen.
    every = statsview.build(store.path, None, "tout", ignored=("g",))
    assert every["features"] == ["f"] and ids(every) == ["r1", "r2"]          # r3, r4: g
    assert [x["feature"] for x in every["by_feature"]] == ["f"]
    assert {p["run_id"] for r in every["runs"] for p in r["passes"]} <= {"r1", "r2"}
