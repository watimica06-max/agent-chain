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


# Which lot an agent pass works on (1.5) — from what /8_code puts in the
# Agent tool's input, never from timing (code_rules.md, « Le lot d'un
# passage »): the prompt's `Your lot:` line, else the description's lot
# (`Declare <lot>`, `Code <lot>`…, the Arbitre's `Settle <lot>`), else the
# lot folder of the Arbitre's `Blocking file:`. The Détailleur names a
# block; the Architecte of move 7 neither.
LOT_LINE = re.compile(r"\bYour lot:\s*(lot-[A-Za-z0-9]+)")
LOT_DESC = re.compile(r"^(?:Declare|Test|Code|Review|Settle)\s+(lot-[A-Za-z0-9]+)\b")
LOT_FILE = re.compile(r"\bBlocking file:\s*code/(lot-[A-Za-z0-9]+)/")
BLOCK_LINE = re.compile(r"\bYour block:\s*(block-[A-Za-z0-9]+)")
BLOCK_DESC = re.compile(r"^(?:Detail|Propagate|Settle)\s+(block-[A-Za-z0-9]+)\b")
FOLDER_LINE = re.compile(r"\bWorking folder:\s*(\S+)")
BUGFIX_PART = re.compile(r"^bugfix-\d+$")


def lot_of_input(inp):
    """{"lot", "block", "folder"} of one Agent tool input; None where the
    input does not say. `folder` is the working folder's `bugfix-NN`, or ""
    for the feature folder itself."""
    inp = inp if isinstance(inp, dict) else {}
    prompt, desc = str(inp.get("prompt") or ""), str(inp.get("description") or "").strip()
    lot = None
    for rx, text in ((LOT_LINE, prompt), (LOT_DESC, desc), (LOT_FILE, prompt)):
        m = rx.search(text)
        if m:
            lot = m.group(1)
            break
    m = BLOCK_LINE.search(prompt) or BLOCK_DESC.search(desc)
    block = m.group(1) if m else None
    folder = None
    m = FOLDER_LINE.search(prompt)
    if m:
        parts = [x for x in re.split(r"[\\/]+", m.group(1).rstrip(".,;")) if x]
        folder = parts[-1] if parts and BUGFIX_PART.match(parts[-1]) else ""
    return {"lot": lot, "block": block, "folder": folder}


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
    lot: str | None = None              # 1.5 — from its own input, else its caller's
    block: str | None = None
    folder: str | None = None

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
                "started_at": self.started_at, "ended_at": self.ended_at,
                "lot": self.lot, "block": self.block, "folder": self.folder,
                "tool_use_id": self.tool_use_id, "parent": self.parent}


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
                where = lot_of_input(inp)
                if p is not None:
                    # A nested agent — the Arbitre a Réalisateur calls, the
                    # Architecte the Arbitre calls — works for its caller:
                    # what its own input leaves out, its caller's says.
                    for k in ("lot", "block", "folder"):
                        if where[k] is None:
                            where[k] = getattr(p, k)
                self.passes[block["id"]] = Pass(
                    tool_use_id=block["id"], parent=parent,
                    agent=inp.get("subagent_type") or "agent",
                    description=inp.get("description") or "", started_at=at, **where)

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

def log_cwd(path):
    """The working directory a run's log says its session ran in — the
    first `cwd` of its messages (the CLI's init) — or None."""
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                m = re.search(r'"cwd":\s*"((?:[^"\\]|\\.)*)"', raw)
                if m:
                    try:
                        return json.loads('"' + m.group(1) + '"')
                    except ValueError:
                        return None
    except OSError:
        return None
    return None


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
  output_tokens INTEGER, tool_calls INTEGER, backfilled INTEGER NOT NULL DEFAULT 0,
  lot TEXT, block TEXT, folder TEXT);
CREATE TABLE IF NOT EXISTS rate_limits (
  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, measured_at TEXT, source TEXT,
  window TEXT, utilization REAL, resets_at INTEGER, status TEXT,
  backfilled INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS agent_passes_run ON agent_passes(run_id);
CREATE INDEX IF NOT EXISTS rate_limits_window ON rate_limits(window, measured_at);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS programmes (
  id TEXT PRIMARY KEY, app TEXT, feature TEXT, name TEXT, spec TEXT, created_at TEXT, started_at TEXT,
  ended_at TEXT, commands INTEGER, lots INTEGER, prompts TEXT, five_hour REAL, five_hour_unknown INTEGER,
  seven_day REAL, seven_day_unknown INTEGER, reason TEXT, reason_kind TEXT);
CREATE TABLE IF NOT EXISTS explanations (
  key TEXT PRIMARY KEY, file_sig TEXT, text TEXT, at TEXT, seconds REAL, run_id TEXT);
"""
# 1.5: the columns a 1.4 store lacks, added in place.
NEW_PASS_COLUMNS = ("lot", "block", "folder")
# 1.6: the application of each run, its folder; the runs stored before are
# given theirs at the server's start (backfill_apps). 1.17: `kind`, « mesure »
# for the usage measure (usage.py) — never a command's run.
NEW_RUN_COLUMNS = ("app", "kind", "programme")


class Store:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self._lock = threading.Lock()
        db = self._db()
        try:
            with db:
                db.executescript(SCHEMA)
                have = {r["name"] for r in db.execute("PRAGMA table_info(agent_passes)")}
                for c in NEW_PASS_COLUMNS:
                    if c not in have:
                        db.execute(f"ALTER TABLE agent_passes ADD COLUMN {c} TEXT")
                have = {r["name"] for r in db.execute("PRAGMA table_info(runs)")}
                for c in NEW_RUN_COLUMNS:
                    if c not in have:
                        db.execute(f"ALTER TABLE runs ADD COLUMN {c} TEXT")
        finally:
            db.close()

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
                   next_line, outcome, log_path, resumed=False, backfilled=False, app=None, kind=None,
                   programme=None):
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
                       " log_path, resumed, backfilled, app, kind, programme)"
                       " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (run_id, feature, work, command, mode, tally.session_id, started_at, ended_at,
                        dur, t.get("input_tokens"), t.get("cache_read_tokens"),
                        t.get("cache_creation_tokens"), t.get("output_tokens"), next_line, outcome,
                        log_path or None, int(resumed), int(backfilled), app, kind, programme))
            db.execute("DELETE FROM agent_passes WHERE run_id=?", (run_id,))
            for p in tally.passes.values():
                db.execute("INSERT INTO agent_passes (run_id, tool_use_id, parent_tool_use_id, agent,"
                           " description, model, started_at, ended_at, duration_s, input_tokens,"
                           " cache_read_tokens, cache_creation_tokens, output_tokens, tool_calls,"
                           " backfilled, lot, block, folder) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (run_id, p.tool_use_id, p.parent, p.agent, p.description, p.model,
                            p.started_at, p.ended_at, p.duration_s, p.input_tokens,
                            p.cache_read_tokens, p.cache_creation_tokens, p.output_tokens, p.tool_calls,
                            int(backfilled), p.lot, p.block, p.folder))
            return totals_summary(totals, dur)
        return self._exec(go)

    def record_programme(self, s):
        """1.18 — a programme's end summary."""
        u = s.get("usage") or {}
        f, w = u.get("five_hour") or {}, u.get("seven_day") or {}
        self._exec(lambda db: db.execute(
            "INSERT OR REPLACE INTO programmes (id, app, feature, name, spec, created_at, started_at, ended_at,"
            " commands, lots, prompts, five_hour, five_hour_unknown, seven_day, seven_day_unknown, reason,"
            " reason_kind) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (s["id"], s.get("app"), s.get("feature"), s.get("name"), json.dumps(s.get("spec"), ensure_ascii=False),
             s.get("created_at"), s.get("started_at"), s.get("ended_at"), s.get("commands"), s.get("lots"),
             json.dumps(s.get("prompts") or [], ensure_ascii=False), f.get("spent"), f.get("unknown"),
             w.get("spent"), w.get("unknown"), s.get("reason"), s.get("reason_kind"))))

    # 1.19 — « Expliquer »: each question's explanation, kept with the hash of
    # its file; a file that changed drops it.
    def explanation(self, key, file_sig):
        def go(db):
            r = db.execute("SELECT * FROM explanations WHERE key=?", (key,)).fetchone()
            if r is None:
                return None
            if r["file_sig"] != file_sig:
                db.execute("DELETE FROM explanations WHERE key=?", (key,))
                return None
            return dict(r)
        return self._exec(go)

    def keep_explanation(self, key, file_sig, text, at, seconds, run_id):
        self._exec(lambda db: db.execute(
            "INSERT OR REPLACE INTO explanations (key, file_sig, text, at, seconds, run_id) VALUES (?,?,?,?,?,?)",
            (key, file_sig, text, at, seconds, run_id)))

    def programmes(self, limit=20):
        def go(db):
            out = []
            for r in db.execute("SELECT * FROM programmes ORDER BY ended_at DESC LIMIT ?", (limit,)):
                d = dict(r)
                for k in ("spec", "prompts"):
                    try:
                        d[k] = json.loads(d[k]) if d[k] else None
                    except ValueError:
                        d[k] = None
                d["usage"] = {"five_hour": {"spent": d.pop("five_hour"), "unknown": d.pop("five_hour_unknown")},
                              "seven_day": {"spent": d.pop("seven_day"), "unknown": d.pop("seven_day_unknown")}}
                out.append(d)
            return out
        return self._exec(go)

    def spent(self, programme):
        """1.18 — what a programme's runs took from each window: the sum of
        each run's share (statsview.limit_delta), and how many runs it left
        out for want of a measure."""
        import statsview

        def go(db):
            ids = [r["id"] for r in db.execute("SELECT id FROM runs WHERE programme=?", (programme,))]
            if not ids:
                return {}
            q = "SELECT * FROM rate_limits WHERE run_id IN (%s) ORDER BY measured_at, id" % ",".join("?" * len(ids))
            ms = [dict(r) for r in db.execute(q, ids)]
            out = {}
            for w in WINDOWS:
                ds = [statsview.limit_delta([m for m in ms if m["run_id"] == i and m["window"] == w])["delta"]
                      for i in ids]
                known = [d for d in ds if d is not None]
                out[w] = {"spent": round(sum(known), 1) if known else None, "unknown": len(ds) - len(known)}
            return out
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

    def limits_of(self, run_id):
        """1.20 — one run's measures, for its journal line."""
        return self._exec(lambda db: [dict(r) for r in db.execute(
            "SELECT * FROM rate_limits WHERE run_id=? ORDER BY measured_at, id", (run_id,))])

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

    def backfill_apps(self, resolve):
        """1.6 — the application of every run stored without one: `resolve`
        is given the run (its log path and its log's working directory) and
        returns its folder. Returns how many were given one."""
        rows = self._exec(lambda db: [dict(r) for r in db.execute(
            "SELECT id, log_path, feature FROM runs WHERE (app IS NULL OR app = '')"
            " AND kind IS NULL")])
        done = 0
        for r in rows:
            app = resolve({**r, "cwd": log_cwd(r.get("log_path"))})
            if app:
                self._exec(lambda db, r=r, app=app: db.execute("UPDATE runs SET app=? WHERE id=?", (app, r["id"])))
                done += 1
        return done

    def backfill_lots(self):
        """1.5 — the lot of every pass already stored, read again from its
        run's log the way a live run reads it (lot_of_input). Once: a mark in
        `meta` says it was done. A log gone leaves its passes' lot unknown."""
        if self._exec(lambda db: db.execute("SELECT value FROM meta WHERE key='lots_read'").fetchone()):
            return {"runs": 0, "passes": 0, "missing": 0, "done": True}
        runs = self._exec(lambda db: [dict(r) for r in db.execute(
            "SELECT id, log_path FROM runs WHERE log_path IS NOT NULL")])
        done = {"runs": 0, "passes": 0, "missing": 0, "done": False}
        for r in runs:
            read = self._read_log(r["log_path"]) if os.path.isfile(r["log_path"]) else None
            if read is None:
                done["missing"] += 1
                continue
            rows = [(p.lot, p.block, p.folder, r["id"], tid) for tid, p in read[0].passes.items()]

            def go(db, rows=rows):
                for x in rows:
                    db.execute("UPDATE agent_passes SET lot=?, block=?, folder=?"
                               " WHERE run_id=? AND tool_use_id=?", x)
            self._exec(go)
            done["runs"] += 1
            done["passes"] += sum(1 for x in rows if x[0])
        self._exec(lambda db: db.execute("INSERT OR REPLACE INTO meta (key, value) VALUES ('lots_read', '1')"))
        return done

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
