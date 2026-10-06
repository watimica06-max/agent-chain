"""The « Statistiques » screen — cockpit 1.4.5 (TECHNICAL_V1 §15).

Reads `stats.sqlite` and nothing else, through a read-only connection: the
runs, their agent passes and every limit measure, filtered by application
(1.6), feature and period, then summed, sorted and ranked here.

Never a figure the store does not hold:
- an unknown count (NULL) stays unknown — `None` in the payload — and is
  left out of every sum, which says how many it left out;
- what a run took from a usage window is derived from two stored measures,
  its first one and its end-of-run `/usage`, and only when both exist and
  the window did not reset in between (`limit_delta`).
"""
import csv
import io
import os
import sqlite3
import statistics
from datetime import datetime, timedelta
from pathlib import Path

WINDOWS = ("five_hour", "seven_day")
PERIODS = ("jour", "7j", "30j", "tout")
TOP = 10
UNUSUAL = 2.0          # above twice the median of its own command or agent
RESET_SLACK_S = 60     # `/usage` gives the reset to the minute, the event to the second


# ------------------------------------------------------------------ reading

def _connect(path):
    """Read-only: the screen never writes the store."""
    return sqlite3.connect(Path(os.path.abspath(path)).as_uri() + "?mode=ro", uri=True, timeout=10)


def read_store(path):
    """Every run, pass and limit measure, as dicts. An absent or unreadable
    store reads as empty, with its error."""
    if not path or not os.path.isfile(path):
        return [], [], [], "aucune base stats.sqlite"
    try:
        db = _connect(path)
    except sqlite3.Error as e:
        return [], [], [], f"stats.sqlite illisible : {e}"
    try:
        db.row_factory = sqlite3.Row
        runs = [dict(r) for r in db.execute("SELECT * FROM runs")]
        passes = [dict(r) for r in db.execute("SELECT * FROM agent_passes ORDER BY id")]
        limits = [dict(r) for r in db.execute("SELECT * FROM rate_limits ORDER BY measured_at, id")]
    except sqlite3.Error as e:
        return [], [], [], f"stats.sqlite illisible : {e}"
    finally:
        db.close()
    return runs, passes, limits, None


def _ts(at):
    try:
        return datetime.fromisoformat(at) if at else None
    except (TypeError, ValueError):
        return None


def period_start(period, now):
    """The first moment of the period, local time; None for « tout »."""
    if period == "jour":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "7j":
        return now - timedelta(days=7)
    if period == "30j":
        return now - timedelta(days=30)
    return None


def _in_period(at, since):
    if since is None:
        return True
    t = _ts(at)
    return t is not None and t.replace(tzinfo=None) >= since


def command_of(prompt):
    """`/1_lexique premiere-app-3` → `/1_lexique`."""
    word = (prompt or "").split()
    return word[0] if word else "(inconnue)"


def _read(x):
    """Tokens read: input, cache read and cache creation — unknown when the
    store holds no input count."""
    if x.get("input_tokens") is None:
        return None
    return (x["input_tokens"] or 0) + (x.get("cache_read_tokens") or 0) + (x.get("cache_creation_tokens") or 0)


# ------------------------------------------------------- the limits per run

def _epoch(at):
    t = _ts(at)
    if t is None:
        return None
    return t.timestamp() if t.tzinfo is None else t.timestamp()


def limit_delta(measures):
    """What one run took from one window: its first measure — the first of
    its session, at its first response — and its end-of-run `/usage`.
    Returns {start, end, delta, why}: `delta` in percentage points, or None
    with the reason. Never across a reset: `resets_at` changed, the start's
    reset passed before the end, or the figure went down."""
    ms = sorted(measures, key=lambda m: (m.get("measured_at") or "", m.get("id") or 0))
    end = next((m for m in reversed(ms) if m.get("source") == "usage"), None)
    start = next((m for m in ms if m is not end), None)
    out = {"start": start["utilization"] if start else None, "end": end["utilization"] if end else None,
           "delta": None, "why": None}
    if end is None:
        out["why"] = "pas de mesure /usage en fin de run"
        return out
    if start is None or (start.get("measured_at") or "") > (end.get("measured_at") or ""):
        out["why"] = "pas de mesure au début du run"
        return out
    a, b = start.get("resets_at"), end.get("resets_at")
    end_at = _epoch(end.get("measured_at"))
    if (a is not None and b is not None and abs(a - b) > RESET_SLACK_S) \
            or (a is not None and end_at is not None and a <= end_at) \
            or end["utilization"] < start["utilization"]:
        out["why"] = "la fenêtre s'est réinitialisée pendant le run"
        return out
    out["delta"] = round((end["utilization"] - start["utilization"]) * 100, 1)
    return out


# ------------------------------------------------------------------- sums

def _sum(values):
    """(sum of the known values, how many were unknown)."""
    known = [v for v in values if v is not None]
    if not values:
        return 0, 0
    # Nothing known: the sum is unknown, never a zero.
    return (sum(known) if known else None), len(values) - len(known)


def _median(values):
    known = [v for v in values if v is not None]
    return statistics.median(known) if known else None


def _totals(runs):
    dur, dur_u = _sum([r["duration_s"] for r in runs])
    read, read_u = _sum([r["read_tokens"] for r in runs])
    cache, _ = _sum([r["cache_read_tokens"] if r["read_tokens"] is not None else None for r in runs])
    wrote, wrote_u = _sum([r["output_tokens"] for r in runs])
    out = {"runs": len(runs), "duration_s": dur, "duration_unknown": dur_u,
           "read_tokens": read, "read_unknown": read_u, "cache_read_tokens": cache,
           "output_tokens": wrote, "output_unknown": wrote_u}
    for w in WINDOWS:
        out[w], out[w + "_unknown"] = _sum([r["limits"][w]["delta"] for r in runs])
    return out


def _by(items, key):
    groups = {}
    for x in items:
        groups.setdefault(key(x), []).append(x)
    return groups


def _mark_unusual(items, key, all_items):
    """« inhabituel »: above twice the median of its own group, the group
    taken over the whole store, not the filter."""
    medians = {k: _median([x["read_tokens"] for x in g]) for k, g in _by(all_items, key).items()}
    for x in items:
        m = medians.get(key(x))
        x["group_median_read"] = m
        x["unusual"] = bool(x["read_tokens"] is not None and m and x["read_tokens"] > UNUSUAL * m)


# ------------------------------------------------------------------- shape

def app_key(app):
    return os.path.normcase(os.path.abspath(app)) if app else None


def _run_view(r, limits_of, names):
    out = {k: r.get(k) for k in ("id", "app", "feature", "work", "command", "permission_mode", "session_id",
                                 "started_at", "ended_at", "duration_s", "input_tokens",
                                 "cache_read_tokens", "cache_creation_tokens", "output_tokens",
                                 "next_line", "outcome", "log_path", "resumed", "backfilled")}
    out["cmd"] = command_of(r.get("command"))
    out["app_name"] = names.get(app_key(r.get("app"))) or (os.path.basename(r["app"]) if r.get("app") else None)
    out["read_tokens"] = _read(r)
    ms = limits_of.get(r["id"], [])
    out["limits"] = {w: limit_delta([m for m in ms if m["window"] == w]) for w in WINDOWS}
    return out


def _pass_view(p, run):
    out = {k: p.get(k) for k in ("id", "run_id", "tool_use_id", "parent_tool_use_id", "agent", "description",
                                 "model", "started_at", "ended_at", "duration_s", "input_tokens",
                                 "cache_read_tokens", "cache_creation_tokens", "output_tokens", "tool_calls",
                                 "backfilled", "lot", "block", "folder")}
    out["read_tokens"] = _read(p)
    out["run_command"] = run["command"] if run else None
    out["run_cmd"] = run["cmd"] if run else None
    out["run_started_at"] = run["started_at"] if run else None
    out["feature"] = run["feature"] if run else None
    out["app_name"] = run["app_name"] if run else None
    return out


def build(path, feature=None, period="tout", now=None, ignored=(), app=None, ignored_by_app=None, names=None):
    """The whole screen's data for one filter: `feature` None is « toutes ».
    `ignored` (1.5.1): features never shown — their runs are in no filter,
    no table and no total. 1.6: `app`, an application's folder, None for
    « toutes »; `ignored_by_app`, {folder key: names}, each application's
    own ignored folders, in place of `ignored`; `names`, {folder key: name}."""
    now = now or datetime.now()
    period = period if period in PERIODS else "tout"
    since = period_start(period, now)
    raw_runs, raw_passes, raw_limits, error = read_store(path)
    names = names or {}

    def is_hidden(r):
        if ignored_by_app is not None:
            return r.get("feature") in ignored_by_app.get(app_key(r.get("app")), ())
        return r.get("feature") in ignored

    limits_of = _by(raw_limits, lambda m: m.get("run_id"))
    all_runs = [_run_view(r, limits_of, names) for r in raw_runs if not is_hidden(r)]
    by_id = {r["id"]: r for r in all_runs}
    hidden = {r["id"] for r in raw_runs if is_hidden(r)}
    all_passes = [_pass_view(p, by_id.get(p["run_id"])) for p in raw_passes if p["run_id"] not in hidden]
    _mark_unusual(all_runs, lambda r: r["cmd"], all_runs)
    _mark_unusual(all_passes, lambda p: p["agent"], all_passes)

    akey = app_key(app)
    in_app = [r for r in all_runs if akey is None or app_key(r.get("app")) == akey]
    runs = [r for r in in_app if (feature is None or r["feature"] == feature)
            and _in_period(r["started_at"], since)]
    runs.sort(key=lambda r: r["started_at"] or "", reverse=True)
    keep = {r["id"] for r in runs}
    passes = [p for p in all_passes if p["run_id"] in keep]
    for r in runs:
        r["passes"] = [p for p in passes if p["run_id"] == r["id"]]
        r["passes_unknown_output"] = sum(1 for p in r["passes"] if p["output_tokens"] is None)

    by_command = []
    for cmd, g in _by(runs, lambda r: r["cmd"]).items():
        t = _totals(g)
        by_command.append({**t, "cmd": cmd, "median_s": _median([r["duration_s"] for r in g]),
                           "five_hour_median": _median([r["limits"]["five_hour"]["delta"] for r in g]),
                           "five_hour_measured": sum(1 for r in g if r["limits"]["five_hour"]["delta"] is not None)})
    by_agent = []
    for agent, g in _by(passes, lambda p: p["agent"]).items():
        dur, dur_u = _sum([p["duration_s"] for p in g])
        read, read_u = _sum([p["read_tokens"] for p in g])
        wrote, wrote_u = _sum([p["output_tokens"] for p in g])
        calls, _ = _sum([p["tool_calls"] for p in g])
        by_agent.append({"agent": agent, "passes": len(g),
                         "models": sorted({p["model"] for p in g if p["model"]}),
                         "median_s": _median([p["duration_s"] for p in g]), "duration_s": dur,
                         "duration_unknown": dur_u, "read_tokens": read, "read_unknown": read_u,
                         "output_tokens": wrote, "output_unknown": wrote_u, "tool_calls": calls})
    # 1.5 — « Par lot », one feature filtered: the passes the store gives a
    # lot (code_rules.md §7), by working folder and lot. A lot's time is its
    # top-level passes' — a nested one runs inside its caller's.
    by_lot = []
    if feature is not None:
        for (folder, lot), g in _by([p for p in passes if p.get("lot")],
                                    lambda p: (p.get("folder") or "", p["lot"])).items():
            top = [p for p in g if not p["parent_tool_use_id"]]
            dur, dur_u = _sum([p["duration_s"] for p in top])
            read, read_u = _sum([p["read_tokens"] for p in g])
            wrote, wrote_u = _sum([p["output_tokens"] for p in g])
            by_lot.append({"folder": folder, "lot": lot, "passes": len(g),
                           "agents": sorted({p["agent"] for p in g if p["agent"]}),
                           "codings": sum(1 for p in g if p["agent"] == "realisateur"),
                           "duration_s": dur, "duration_unknown": dur_u, "read_tokens": read,
                           "read_unknown": read_u, "output_tokens": wrote, "output_unknown": wrote_u})
    by_lot_unknown = sum(1 for p in passes if not p.get("lot")) if feature is not None else 0
    by_feature = []
    if feature is None:
        # « Toutes » the applications: a feature is named with its application's.
        for (an, feat), g in _by(runs, lambda r: (r["app_name"] if akey is None else None,
                                                   r["feature"] or "(inconnue)")).items():
            by_feature.append({**_totals(g), "feature": feat, "app_name": an,
                               "label": f"{an or '(application inconnue)'} · {feat}" if akey is None else feat})

    measures = []
    for m in raw_limits:
        if _in_period(m["measured_at"], since):
            measures.append({k: m.get(k) for k in ("run_id", "measured_at", "source", "window", "utilization",
                                                   "resets_at", "backfilled")})
    starts = [t for t in (_ts(x) for x in [r["started_at"] for r in runs] + [m["measured_at"] for m in measures]) if t]
    first = min((t.replace(tzinfo=None) for t in starts), default=None)

    costly_runs = sorted((r for r in runs if r["read_tokens"] is not None),
                         key=lambda r: r["read_tokens"], reverse=True)[:TOP]
    costly_passes = sorted((p for p in passes if p["read_tokens"] is not None),
                           key=lambda p: p["read_tokens"], reverse=True)[:TOP]
    features = sorted({r["feature"] for r in in_app if r["feature"]})
    return {
        "app": app, "app_name": names.get(akey) if akey else None,
        "feature": feature, "period": period, "now": now.isoformat(timespec="seconds"),
        "since": since.isoformat(timespec="seconds") if since else None,
        "range": {"start": (since or first or now).isoformat(timespec="seconds"),
                  "end": now.isoformat(timespec="seconds")},
        "error": error, "features": features,
        "totals": _totals(runs),
        "passes_count": len(passes),
        "passes_unknown_output": sum(1 for p in passes if p["output_tokens"] is None),
        "by_command": sorted(by_command, key=lambda x: x["cmd"]),
        "by_agent": sorted(by_agent, key=lambda x: x["agent"] or ""),
        "by_feature": sorted(by_feature, key=lambda x: x["label"]),
        "by_lot": sorted(by_lot, key=lambda x: (x["folder"], x["lot"])),
        "by_lot_unknown": by_lot_unknown,
        "costly_runs": [r["id"] for r in costly_runs],
        "costly_passes": [{"run_id": p["run_id"], "id": p["id"]} for p in costly_passes],
        "runs": runs,
        "limits": measures,
    }


# -------------------------------------------------------------------- CSV

RUN_COLUMNS = [
    ("début", "started_at"), ("fin", "ended_at"), ("application", "app_name"), ("fonctionnalité", "feature"),
    ("commande", "command"), ("durée (s)", "duration_s"), ("tokens lus", "read_tokens"), ("dont entrée", "input_tokens"),
    ("dont cache lu", "cache_read_tokens"), ("dont cache créé", "cache_creation_tokens"),
    ("tokens écrits", "output_tokens"),
    ("5 h au début (%)", ("five_hour", "start")), ("5 h à la fin (%)", ("five_hour", "end")),
    ("≈ % de la fenêtre 5 h", ("five_hour", "delta")),
    ("semaine au début (%)", ("seven_day", "start")), ("semaine à la fin (%)", ("seven_day", "end")),
    ("≈ % de la semaine", ("seven_day", "delta")),
    ("inhabituel", "unusual"), ("fin du run", "outcome"), ("Next:", "next_line"), ("repris", "resumed"),
    ("rechargé d'un journal", "backfilled"), ("journal", "log_path"), ("id", "id"),
]
PASS_COLUMNS = [
    ("run", "run_id"), ("début du run", "run_started_at"), ("commande", "run_command"),
    ("application", "app_name"), ("fonctionnalité", "feature"), ("agent", "agent"), ("modèle", "model"), ("description", "description"),
    ("début", "started_at"), ("fin", "ended_at"), ("durée (s)", "duration_s"), ("tokens lus", "read_tokens"),
    ("dont entrée", "input_tokens"), ("dont cache lu", "cache_read_tokens"),
    ("dont cache créé", "cache_creation_tokens"), ("tokens écrits", "output_tokens"),
    ("appels d'outils", "tool_calls"), ("inhabituel", "unusual"), ("tool_use_id", "tool_use_id"),
]
# Unknown counts are written as such, never as an empty or a zero.
UNKNOWN_IF_NONE = {"duration_s", "read_tokens", "input_tokens", "cache_read_tokens", "cache_creation_tokens",
                   "output_tokens", "tool_calls"}


def _cell(x, key):
    if isinstance(key, tuple):
        lim = x["limits"][key[0]]
        v = lim[key[1]]
        if v is None:
            return lim["why"] if key[1] == "delta" else "inconnu"
        return _num(v * 100 if key[1] != "delta" else v)
    v = x.get(key)
    if v is None:
        return "inconnu" if key in UNKNOWN_IF_NONE else ""
    if isinstance(v, bool):
        return "oui" if v else ""
    if key in ("resumed", "backfilled"):
        return "oui" if v else ""
    return _num(v) if isinstance(v, (int, float)) else str(v)


def _num(v):
    # A French spreadsheet reads a decimal comma; integers stay as they are.
    if isinstance(v, float):
        v = round(v, 1)
        return str(int(v)) if v == int(v) else str(v).replace(".", ",")
    return str(v)


def to_csv(rows, columns):
    """`;`-separated, UTF-8 with its BOM: what a French Excel opens as columns."""
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\r\n")
    w.writerow([c[0] for c in columns])
    for x in rows:
        w.writerow([_cell(x, c[1]) for c in columns])
    return "﻿" + buf.getvalue()


def csv_files(data):
    """The two exports for the current filters: (name, text) for the runs
    and for their agent passes."""
    feat = data["feature"] or "toutes"
    if data.get("app_name"):
        feat = f"{data['app_name']}-{feat}"
    stamp = data["now"][:10]
    passes = [p for r in data["runs"] for p in r["passes"]]
    return [(f"cockpit-runs-{feat}-{data['period']}-{stamp}.csv", to_csv(data["runs"], RUN_COLUMNS)),
            (f"cockpit-passages-{feat}-{data['period']}-{stamp}.csv", to_csv(passes, PASS_COLUMNS))]
