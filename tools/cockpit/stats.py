"""What every run and every agent consumes — cockpit 1.4, 1.4.1, 1.4.3.

Counting rules (TECHNICAL_V1 §13, the Agent SDK's « Track cost and usage »):
- per-step usage is read on assistant messages, **once per message id** —
  parallel tool calls repeat it;
- a message belongs to the agent its `parent_tool_use_id` names, nested
  agents included; no parent is the orchestrator;
- per-step `output_tokens` is a placeholder: **never stored**. A pass's
  output is its model's `outputTokens` in the latest result's
  `model_usage`, once the run is over, and only when that model's input
  and cache figures equal the pass's own exactly — the proof that nothing
  else used the model in the run; otherwise unknown (1.4.3). Never the
  transcripts: on a real run a subagent's keeps the placeholder on the
  last line of most of its messages;
- run totals come from the latest result's `model_usage`, which counts the
  subagents; its `usage` alone does not.

`Tally` reads the logged shape — the message's type name and its `asdict`
body — so a live run and the backfill of an old log count the same way.
"""
import json
import os
import re
import sqlite3
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta


AGENT_TOOLS = {"Agent", "Task"}
BACKGROUND_RESULT = re.compile(r"async_launched|in the background|agentId", re.I)
TERMINAL = {"completed", "failed", "stopped", "killed"}
WINDOWS = ("five_hour", "seven_day")
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.sqlite")


def _ts(at):
    try:
        return datetime.fromisoformat(at) if at else None
    except (TypeError, ValueError):
        return None


def _seconds(a, b):
    ta, tb = _ts(a), _ts(b)
    return round((tb - ta).total_seconds(), 3) if ta and tb else None


@dataclass
class Pass:
    tool_use_id: str
    parent: str | None
    agent: str
    description: str
    started_at: str | None
    model: str | None = None
    ended_at: str | None = None
    input_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    tool_calls: int = 0
    background: bool = False
    ended: bool = False
    output_tokens: int | None = None    # its model's, when it alone used it (apply_model_usage)

    @property
    def duration_s(self):
        return _seconds(self.started_at, self.ended_at)

    def summary(self):
        return {"agent": self.agent, "model": self.model, "duration_s": self.duration_s,
                "input_tokens": self.input_tokens, "cache_read_tokens": self.cache_read_tokens,
                "cache_creation_tokens": self.cache_creation_tokens,
                "read_tokens": self.input_tokens + self.cache_read_tokens + self.cache_creation_tokens,
                # Never the stream's placeholder: its model's figure, or
                # unknown (TECHNICAL_V1 §13.1).
                "output_tokens": self.output_tokens, "tool_calls": self.tool_calls,
                "started_at": self.started_at, "ended_at": self.ended_at}


@dataclass
class Tally:
    passes: dict = field(default_factory=dict)      # tool_use_id -> Pass, in start order
    seen_messages: set = field(default_factory=set)
    seen_tools: set = field(default_factory=set)
    tasks: dict = field(default_factory=dict)       # task_id -> tool_use_id
    orchestrator: dict = field(default_factory=lambda: {"input_tokens": 0, "cache_read_tokens": 0,
                                                         "cache_creation_tokens": 0, "tool_calls": 0})
    totals: dict | None = None                      # the latest result's model_usage, summed
    model_usage: dict | None = None                 # the latest result's model_usage, per model
    session_id: str | None = None
    first_at: str | None = None
    last_at: str | None = None

    def feed(self, kind: str, body, at: str | None):
        """One message, in arrival order. Returns what it produced:
        `("ended", Pass)` for an agent that handed back, `("limit", dict)`
        for a rate-limit measure."""
        if at:
            self.first_at = self.first_at or at
            self.last_at = at
        if not isinstance(body, dict):
            return []
        out = []
        if kind == "AssistantMessage":
            self._assistant(body, at)
        elif kind == "UserMessage":
            out += self._user(body, at)
        elif kind == "TaskStartedMessage":
            if body.get("tool_use_id"):
                self.tasks[body.get("task_id")] = body["tool_use_id"]
        elif kind in ("TaskNotificationMessage", "TaskUpdatedMessage"):
            status = body.get("status") or (body.get("patch") or {}).get("status")
            if status in TERMINAL:
                tid = body.get("tool_use_id") or self.tasks.get(body.get("task_id"))
                out += self._end(tid, at)
        elif kind == "ResultMessage":
            self._result(body)
        elif kind == "RateLimitEvent":
            out += [("limit", m) for m in limits_from_event(body, at)]
        return out

    def _bucket(self, parent):
        p = self.passes.get(parent) if parent else None
        return p

    def _assistant(self, body, at):
        parent = body.get("parent_tool_use_id")
        p = self._bucket(parent)
        mid = body.get("message_id") or body.get("uuid")
        usage = body.get("usage") or {}
        if p is not None and body.get("model") and not str(body.get("model")).startswith("<"):
            p.model = p.model or body.get("model")
        if usage and (mid is None or mid not in self.seen_messages):
            if mid is not None:
                self.seen_messages.add(mid)
            target = p if p is not None else None
            for key, name in (("input_tokens", "input_tokens"),
                              ("cache_read_input_tokens", "cache_read_tokens"),
                              ("cache_creation_input_tokens", "cache_creation_tokens")):
                n = usage.get(key) or 0
                if target is not None:
                    setattr(target, name, getattr(target, name) + n)
                else:
                    self.orchestrator[name] += n
        for block in body.get("content") or []:
            if not (isinstance(block, dict) and "name" in block and "id" in block and "input" in block):
                continue
            if block["id"] in self.seen_tools:
                continue
            self.seen_tools.add(block["id"])
            if p is not None:
                p.tool_calls += 1
            else:
                self.orchestrator["tool_calls"] += 1
            if block["name"] in AGENT_TOOLS:
                inp = block.get("input") or {}
                self.passes[block["id"]] = Pass(
                    tool_use_id=block["id"], parent=parent,
                    agent=inp.get("subagent_type") or "agent",
                    description=inp.get("description") or "", started_at=at)

    def _user(self, body, at):
        out = []
        content = body.get("content")
        for block in content if isinstance(content, list) else []:
            if not (isinstance(block, dict) and "tool_use_id" in block):
                continue
            p = self.passes.get(block["tool_use_id"])
            if p is None or p.ended:
                continue
            if BACKGROUND_RESULT.search(_text_of(block.get("content"))):
                p.background = True      # still running: ends on its task notification
            else:
                out += self._end(p.tool_use_id, at)
        return out

    def _end(self, tid, at):
        p = self.passes.get(tid)
        if p is None or p.ended:
            return []
        p.ended, p.ended_at = True, at
        return [("ended", p)]

    def _result(self, body):
        self.session_id = body.get("session_id") or self.session_id
        mu = body.get("model_usage")
        if not isinstance(mu, dict) or not mu:
            return
        t = {"input_tokens": 0, "cache_read_tokens": 0, "cache_creation_tokens": 0, "output_tokens": 0}
        for u in mu.values():
            if not isinstance(u, dict):
                continue
            t["input_tokens"] += u.get("inputTokens") or 0
            t["cache_read_tokens"] += u.get("cacheReadInputTokens") or 0
            t["cache_creation_tokens"] += u.get("cacheCreationInputTokens") or 0
            t["output_tokens"] += u.get("outputTokens") or 0
        # The running total of the call: the latest result, never a sum of results.
        self.totals = t
        self.model_usage = {m: u for m, u in mu.items() if isinstance(u, dict)}


def apply_model_usage(tally) -> int:
    """Each pass's output from the latest result's model_usage, as it came —
    never the figure a resumed run stores after subtraction. A pass gets its
    model's `outputTokens` only when that model's input, cache-read and
    cache-creation figures equal the pass's own deduplicated sums exactly:
    then nothing else — the orchestrator, another agent, an internal call
    of Claude Code, an earlier run of a resumed session — used that model.
    Otherwise unknown, never an estimate. Returns how many got a figure."""
    mu = tally.model_usage or {}
    models = [p.model for p in tally.passes.values()]
    got = 0
    for p in tally.passes.values():
        u = mu.get(p.model) if p.model else None
        if (u is not None and models.count(p.model) == 1
                and u.get("inputTokens") == p.input_tokens
                and u.get("cacheReadInputTokens") == p.cache_read_tokens
                and u.get("cacheCreationInputTokens") == p.cache_creation_tokens
                and isinstance(u.get("outputTokens"), int)):
            p.output_tokens = u["outputTokens"]
            got += 1
        else:
            p.output_tokens = None
    return got


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return str(content or "")


def totals_summary(totals, duration_s=None):
    if not totals:
        return None
    return {**totals, "duration_s": duration_s,
            "read_tokens": totals["input_tokens"] + totals["cache_read_tokens"] + totals["cache_creation_tokens"]}


# ------------------------------------------------------------------ limits

def limits_from_event(body, at):
    """A `RateLimitEvent`: both windows from `raw.unifiedWindows` when the CLI
    sends them, else the one window `rate_limit_type` names."""
    info = body.get("rate_limit_info") or {}
    raw = info.get("raw") or {}
    status = info.get("status")
    out = []
    uw = raw.get("unifiedWindows") if isinstance(raw, dict) else None
    if isinstance(uw, dict):
        for w in WINDOWS:
            v = uw.get(w)
            if isinstance(v, dict) and v.get("utilization") is not None:
                out.append({"window": w, "utilization": float(v["utilization"]),
                            "resets_at": v.get("resetsAt"), "status": status,
                            "measured_at": at, "source": "event"})
    elif info.get("rate_limit_type") in WINDOWS and info.get("utilization") is not None:
        out.append({"window": info["rate_limit_type"], "utilization": float(info["utilization"]),
                    "resets_at": info.get("resets_at"), "status": status,
                    "measured_at": at, "source": "event"})
    return out


USAGE_LINES = {
    "five_hour": re.compile(r"^Current session:\s*(\d+(?:\.\d+)?)% used(?:\s*\S\s*resets\s+(.+))?$", re.M),
    "seven_day": re.compile(r"^Current week \(all models\):\s*(\d+(?:\.\d+)?)% used(?:\s*\S\s*resets\s+(.+))?$", re.M),
}
RESET = re.compile(r"^(?:(?P<mon>[A-Z][a-z]{2})\s+(?P<day>\d{1,2}),\s*)?(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>am|pm)"
                   r"(?:\s*\((?P<tz>[^)]+)\))?\s*$", re.I)
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                                      "Sep", "Oct", "Nov", "Dec"], 1)}


def parse_reset(text, now=None):
    """`Oct 6, 1:40pm (Asia/Singapore)` → Unix seconds, or None."""
    m = RESET.match((text or "").strip())
    if not m:
        return None
    tz = None
    if m.group("tz"):
        try:
            from zoneinfo import ZoneInfo
            tz = ZoneInfo(m.group("tz"))
        except Exception:
            return None
    now = now or datetime.now(tz)
    h = int(m.group("h")) % 12 + (12 if m.group("ap").lower() == "pm" else 0)
    mi = int(m.group("m") or 0)
    if m.group("mon"):
        mon = MONTHS.get(m.group("mon").title())
        if not mon:
            return None
        cands = []
        for y in (now.year - 1, now.year, now.year + 1):
            try:
                cands.append(datetime(y, mon, int(m.group("day")), h, mi, tzinfo=tz or now.tzinfo))
            except ValueError:
                pass
        if not cands:
            return None
        ref = now if now.tzinfo else now.replace(tzinfo=cands[0].tzinfo)
        best = min(cands, key=lambda d: abs((d - ref).total_seconds()))
    else:
        best = now.replace(hour=h, minute=mi, second=0, microsecond=0)
        if best < now:
            best += timedelta(days=1)
    return int(best.timestamp())


def limits_from_usage(text, at, now=None):
    """The `/usage` report, read from its text — a local command, no model
    call. Both windows, with their reset when it parses."""
    out = []
    for w, rx in USAGE_LINES.items():
        m = rx.search(text or "")
        if m:
            out.append({"window": w, "utilization": float(m.group(1)) / 100.0,
                        "resets_at": parse_reset(m.group(2), now) if m.group(2) else None,
                        "status": None, "measured_at": at, "source": "usage"})
    return out


# ------------------------------------------------------------------ store

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY, feature TEXT, work TEXT, command TEXT, permission_mode TEXT,
  session_id TEXT, started_at TEXT, ended_at TEXT, duration_s REAL,
  input_tokens INTEGER, cache_read_tokens INTEGER, cache_creation_tokens INTEGER,
  output_tokens INTEGER, next_line TEXT, outcome TEXT, log_path TEXT UNIQUE,
  resumed INTEGER NOT NULL DEFAULT 0, backfilled INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS agent_passes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL REFERENCES runs(id),
  tool_use_id TEXT, parent_tool_use_id TEXT, agent TEXT, description TEXT, model TEXT,
  started_at TEXT, ended_at TEXT, duration_s REAL,
  input_tokens INTEGER, cache_read_tokens INTEGER, cache_creation_tokens INTEGER,
  output_tokens INTEGER, tool_calls INTEGER, backfilled INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS rate_limits (
  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, measured_at TEXT, source TEXT,
  window TEXT, utilization REAL, resets_at INTEGER, status TEXT,
  backfilled INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS agent_passes_run ON agent_passes(run_id);
CREATE INDEX IF NOT EXISTS rate_limits_window ON rate_limits(window, measured_at);
"""


class Store:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self._lock = threading.Lock()
        with self._db() as db:
            db.executescript(SCHEMA)

    def _db(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def _exec(self, fn):
        with self._lock:
            db = self._db()
            try:
                with db:
                    return fn(db)
            finally:
                db.close()

    # -------------------------------------------------------------- write

    def record_limit(self, run_id, m, backfilled=False):
        self._exec(lambda db: db.execute(
            "INSERT INTO rate_limits (run_id, measured_at, source, window, utilization, resets_at,"
            " status, backfilled) VALUES (?,?,?,?,?,?,?,?)",
            (run_id, m["measured_at"], m["source"], m["window"], m["utilization"],
             m.get("resets_at"), m.get("status"), int(backfilled))))

    def record_run(self, *, run_id, feature, work, command, mode, started_at, ended_at, tally,
                   next_line, outcome, log_path, resumed=False, backfilled=False):
        totals = dict(tally.totals) if tally.totals else None

        def go(db):
            if totals and resumed and tally.session_id:
                # A resumed session's results count its earlier spend too:
                # this run is what the session gained since its last run.
                prev = db.execute("SELECT input_tokens, cache_read_tokens, cache_creation_tokens,"
                                  " output_tokens FROM runs WHERE session_id=? AND id<>?"
                                  " ORDER BY ended_at DESC LIMIT 1",
                                  (tally.session_id, run_id)).fetchone()
                if prev:
                    for k in totals:
                        totals[k] = max(0, totals[k] - (prev[k] or 0))
            dur = _seconds(started_at, ended_at)
            t = totals or {}
            db.execute("INSERT OR REPLACE INTO runs (id, feature, work, command, permission_mode,"
                       " session_id, started_at, ended_at, duration_s, input_tokens,"
                       " cache_read_tokens, cache_creation_tokens, output_tokens, next_line, outcome,"
                       " log_path, resumed, backfilled) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (run_id, feature, work, command, mode, tally.session_id, started_at, ended_at,
                        dur, t.get("input_tokens"), t.get("cache_read_tokens"),
                        t.get("cache_creation_tokens"), t.get("output_tokens"), next_line, outcome,
                        log_path or None, int(resumed), int(backfilled)))
            db.execute("DELETE FROM agent_passes WHERE run_id=?", (run_id,))
            for p in tally.passes.values():
                db.execute("INSERT INTO agent_passes (run_id, tool_use_id, parent_tool_use_id, agent,"
                           " description, model, started_at, ended_at, duration_s, input_tokens,"
                           " cache_read_tokens, cache_creation_tokens, output_tokens, tool_calls,"
                           " backfilled) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (run_id, p.tool_use_id, p.parent, p.agent, p.description, p.model,
                            p.started_at, p.ended_at, p.duration_s, p.input_tokens,
                            p.cache_read_tokens, p.cache_creation_tokens, p.output_tokens, p.tool_calls,
                            int(backfilled)))
            return totals_summary(totals, dur)
        return self._exec(go)

    # --------------------------------------------------------------- read

    def latest_limits(self):
        """The newest measure of each window, whatever its source, with the
        time it was measured — never presented as newer than it is."""
        def go(db):
            out = {}
            for w in WINDOWS:
                r = db.execute("SELECT * FROM rate_limits WHERE window=? AND backfilled=0"
                               " ORDER BY measured_at DESC, id DESC LIMIT 1", (w,)).fetchone()
                if r is None:
                    r = db.execute("SELECT * FROM rate_limits WHERE window=?"
                                   " ORDER BY measured_at DESC, id DESC LIMIT 1", (w,)).fetchone()
                if r is not None:
                    d = dict(r)
                    if d["resets_at"] is None:
                        # The same window's reset, from the latest event that gave one.
                        e = db.execute("SELECT resets_at FROM rate_limits WHERE window=? AND"
                                       " resets_at IS NOT NULL ORDER BY measured_at DESC LIMIT 1",
                                       (w,)).fetchone()
                        d["resets_at"] = e["resets_at"] if e else None
                    out[w] = d
            return out
        return self._exec(go)

    def run_by_log(self, log_path):
        def go(db):
            r = db.execute("SELECT * FROM runs WHERE log_path=?", (log_path,)).fetchone()
            return dict(r) if r else None
        return self._exec(go)

    def runs_by_logs(self, paths):
        paths = [p for p in paths if p]
        if not paths:
            return {}

        def go(db):
            q = "SELECT * FROM runs WHERE log_path IN (%s)" % ",".join("?" * len(paths))
            return {r["log_path"]: dict(r) for r in db.execute(q, paths)}
        return self._exec(go)

    def passes(self, run_id):
        return self._exec(lambda db: [dict(r) for r in db.execute(
            "SELECT * FROM agent_passes WHERE run_id=? ORDER BY id", (run_id,))])

    def counts(self):
        def go(db):
            return {t: db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    for t in ("runs", "agent_passes", "rate_limits")}
        return self._exec(go)

    # ----------------------------------------------------------- backfill

    def backfill(self, log_dir, history=None):
        """Load every run log not yet in the store, once (by its path). Old
        logs are marked backfilled; their durations come from each line's
        `at` when it is there, and are unknown otherwise; their agents'
        output from the log's own model_usage."""
        history = history or {}
        done = {"files": 0, "runs": 0, "passes": 0, "limits": 0, "skipped": 0}
        try:
            names = sorted(n for n in os.listdir(log_dir) if n.endswith(".jsonl"))
        except OSError:
            return done
        for name in names:
            path = os.path.join(log_dir, name)
            if name.startswith("next-ecarte") or self.run_by_log(path):
                done["skipped"] += 1
                continue
            got = self._backfill_one(path, history.get(os.path.normcase(path)) or {})
            if got is None:
                done["skipped"] += 1
                continue
            done["files"] += 1
            done["runs"] += 1
            done["passes"] += got["passes"]
            done["limits"] += got["limits"]
        return done

    @staticmethod
    def _read_log(path):
        """A run log fed to a Tally, its probe lines left out: (tally,
        limits, lines, every line timed), or None when it cannot be read."""
        tally = Tally()
        limits = []
        at_all = True
        lines = 0
        try:
            with open(path, encoding="utf-8") as f:
                for raw in f:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        line = json.loads(raw)
                    except ValueError:
                        continue
                    if line.get("probe"):
                        continue
                    lines += 1
                    at = line.get("at")
                    at_all = at_all and bool(at)
                    for kind, x in tally.feed(line.get("type") or "", line.get("message"), at):
                        if kind == "limit":
                            limits.append(x)
        except OSError:
            return None
        return tally, limits, lines, at_all

    def _backfill_one(self, path, hist):
        read = self._read_log(path)
        if read is None:
            return None
        tally, limits, lines, at_all = read
        if not lines:
            return None
        apply_model_usage(tally)
        if not at_all:
            # No receive time on every line: durations are not known.
            tally.first_at = tally.last_at = None
            for p in tally.passes.values():
                p.started_at = p.ended_at = None
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})(\d{2})-(.+?)(?:-\d+)?\.jsonl$",
                     os.path.basename(path))
        run_id = "bf-" + os.path.basename(path)[:-6]
        command = hist.get("command") or ("/" + m.group(5) if m else None)
        started = tally.first_at or (f"{m.group(1)}T{m.group(2)}:{m.group(3)}:{m.group(4)}" if m else None)
        nxt = hist.get("next") or {}
        self.record_run(run_id=run_id, feature=(hist.get("work") or "").split("/")[0] or None,
                        work=hist.get("work"), command=command, mode=None, started_at=started,
                        ended_at=tally.last_at, tally=tally,
                        next_line=nxt.get("raw") if isinstance(nxt, dict) else None,
                        outcome=hist.get("outcome"), log_path=path, backfilled=True)
        for x in limits:
            self.record_limit(run_id, x, backfilled=True)
        return {"passes": len(tally.passes), "limits": len(limits)}

    def backfill_outputs(self):
        """The agents' output of the runs already stored, from their logs:
        each run read again (the model_usage it got, never the stored
        difference of a resumed run), each pass by apply_model_usage. A run
        any of whose agents already has a figure is skipped."""
        def todo(db):
            return [dict(r) for r in db.execute(
                "SELECT r.id, r.log_path FROM runs r WHERE r.session_id IS NOT NULL"
                " AND r.log_path IS NOT NULL AND EXISTS (SELECT 1 FROM agent_passes a"
                " WHERE a.run_id=r.id) AND NOT EXISTS (SELECT 1 FROM agent_passes a"
                " WHERE a.run_id=r.id AND a.output_tokens IS NOT NULL)")]
        done = {"runs": 0, "passes": 0, "unknown": 0}
        for r in self._exec(todo):
            read = self._read_log(r["log_path"]) if os.path.isfile(r["log_path"]) else None
            if read is None or not apply_model_usage(read[0]):
                done["unknown"] += 1
                continue
            figures = [(p.output_tokens, r["id"], tid) for tid, p in read[0].passes.items()
                       if p.output_tokens is not None]

            def go(db, figures=figures):
                for f in figures:
                    db.execute("UPDATE agent_passes SET output_tokens=? WHERE run_id=? AND tool_use_id=?", f)
            self._exec(go)
            done["runs"] += 1
            done["passes"] += len(figures)
        return done
