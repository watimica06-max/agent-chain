"""La consommation, mesurée et bornée — cockpit 1.17.

§1 — the measure: the smallest call that makes Claude Code report both
usage windows. One short prompt, the lightest model, one turn, no tool, no
setting, no MCP server, in a scratch folder of its own — never an
application's. The CLI answers with a `RateLimitEvent` whose
`raw.unifiedWindows` holds both windows and their `resetsAt` (Unix seconds);
when it gives none, `/usage` is asked in the same session — a local command,
no model call. Its cost is recorded in the stats like a run's, marked
`kind = 'mesure'`; its measures carry the source `mesure`. A measure that
fails says why and never blocks anything.

§2 — two thresholds per window, a warning and a block, in percent: the level
of a window is its latest measure, unless its reset has passed since (then
nothing is known of it, and nothing warns or blocks on it).

§3 — what a command will cost: the median share of each window its past runs
took (statsview.limit_delta), from this application's runs when there are
three, else from every application's, else « inconnu ».
"""
import asyncio
import json
import os
import re
import statistics
import tempfile
import uuid
from datetime import datetime

import runner as runner_mod
import stats as stats_mod
import statsview

WINDOWS = stats_mod.WINDOWS
WINDOW_NAMES = {"five_hour": "Fenêtre de 5 heures", "seven_day": "Semaine"}
# A measure older than this is refreshed: at the home screen, before a launch.
STALE_S = 15 * 60
# Both thresholds of both windows: 90 % by default (the Product Owner's).
DEFAULT_THRESHOLDS = {w: {"warn": 90, "block": 90} for w in WINDOWS}
MIN_RUNS = 3              # under three measured runs, « inconnu »
OVERRIDE_LOG = "consommation.log"   # « Lancer quand même », one line each, beside the run logs
KIND = "mesure"
COMMAND = "(mesure d'usage)"
PROMPT = "Réponds seulement : ok"
MODEL = "haiku"
TIMEOUT = 90.0
SCRATCH = os.path.join(tempfile.gettempdir(), "cockpit-mesure")


# ------------------------------------------------------------- thresholds

def clean_thresholds(raw):
    """Four whole percentages, 1 to 100; what is missing or unreadable
    takes its default. Raises ValueError on a value given out of range."""
    out = json.loads(json.dumps(DEFAULT_THRESHOLDS))
    for w in WINDOWS:
        given = (raw or {}).get(w) if isinstance(raw, dict) else None
        for k in ("warn", "block"):
            v = given.get(k) if isinstance(given, dict) else None
            if v is None or v == "":
                continue
            try:
                n = int(round(float(v)))
            except (TypeError, ValueError):
                raise ValueError(f"seuil illisible : {v!r}")
            if not 1 <= n <= 100:
                raise ValueError(f"un seuil va de 1 à 100 % — {WINDOW_NAMES[w]} : {n} %")
            out[w][k] = n
    return out


def _local(ts):
    return datetime.fromtimestamp(ts)


def age_s(measured_at, now=None):
    t = stats_mod._ts(measured_at)
    if t is None:
        return None
    now = now or datetime.now()
    if t.tzinfo is not None:
        t = t.astimezone().replace(tzinfo=None)
    return max(0.0, (now - t).total_seconds())


def levels(limits, thresholds, now=None):
    """Each window's level from its latest measure: `ok`, `warn` or `block`,
    with its figure, its thresholds, its reset and its age. A window whose
    reset has passed since its measure is `reset`: its figure is gone."""
    now = now or datetime.now()
    out = {}
    for w in WINDOWS:
        m = (limits or {}).get(w)
        th = thresholds[w]
        x = {"window": w, "name": WINDOW_NAMES[w], "warn": th["warn"], "block": th["block"],
             "pct": None, "level": "inconnu", "resets_at": None, "measured_at": None, "age_s": None}
        if m and m.get("utilization") is not None:
            pct = round(float(m["utilization"]) * 100, 1)
            x.update(pct=pct, resets_at=m.get("resets_at"), measured_at=m.get("measured_at"),
                     age_s=age_s(m.get("measured_at"), now), source=m.get("source"))
            if m.get("resets_at") and m["resets_at"] <= now.timestamp():
                x["level"] = "reset"
            elif pct >= th["block"]:
                x["level"] = "block"
            elif pct >= th["warn"]:
                x["level"] = "warn"
            else:
                x["level"] = "ok"
        out[w] = x
    return out


def blocking(lv):
    return [x for x in lv.values() if x["level"] == "block"]


def oldest_age(limits, now=None):
    """The age of the older of the two windows' latest measures — None when
    either has none: the gauges are as fresh as their staler one."""
    ages = [age_s((limits or {}).get(w, {}).get("measured_at"), now) for w in WINDOWS]
    return None if any(a is None for a in ages) else max(ages)


def block_text(blocked):
    return " ; ".join(f"{x['name']} à {fmt_pct(x['pct'])} (seuil de blocage {x['block']} %)" for x in blocked)


def fmt_pct(p):
    return f"{int(p)} %" if p == int(p) else f"{p:.1f} %".replace(".", ",")


# ---------------------------------------------------------------- estimate

def _read(store_path):
    """The runs and the limit measures alone, read-only — never the passes."""
    import sqlite3
    if not store_path or not os.path.isfile(store_path):
        return [], []
    try:
        db = statsview._connect(store_path)
    except sqlite3.Error:
        return [], []
    try:
        db.row_factory = sqlite3.Row
        cols = {r["name"] for r in db.execute("PRAGMA table_info(runs)")}
        runs = [dict(r) for r in db.execute(
            "SELECT id, app, command" + (", kind" if "kind" in cols else "") + " FROM runs")]
        limits = [dict(r) for r in db.execute(
            "SELECT id, run_id, window, utilization, resets_at, measured_at, source FROM rate_limits"
            " ORDER BY measured_at, id")]
        return runs, limits
    except sqlite3.Error:
        return [], []
    finally:
        db.close()


def estimates(store_path, app=None):
    """{command: {window: {median, n, scope}}} — the median share of each
    window a command's past runs took, in percentage points. `scope` is
    `app` when this application has MIN_RUNS measured runs, `all` when every
    application together has, else the median is None (« inconnu »)."""
    runs, limits = _read(store_path)
    by_run = {}
    for m in limits:
        by_run.setdefault(m.get("run_id"), []).append(m)
    akey = statsview.app_key(app)
    rows = {}
    for r in runs:
        if r.get("kind") == KIND:
            continue
        cmd = statsview.command_of(r.get("command"))
        ms = by_run.get(r["id"], [])
        here = akey is not None and statsview.app_key(r.get("app")) == akey
        for w in WINDOWS:
            d = statsview.limit_delta([m for m in ms if m["window"] == w])["delta"]
            if d is not None:
                rows.setdefault(cmd, {}).setdefault(w, []).append((here, d))
    out = {}
    for cmd, per in rows.items():
        out[cmd] = {}
        for w in WINDOWS:
            got = per.get(w, [])
            mine = [d for h, d in got if h]
            if len(mine) >= MIN_RUNS:
                out[cmd][w] = {"median": round(statistics.median(mine), 1), "n": len(mine), "scope": "app"}
            elif len(got) >= MIN_RUNS:
                out[cmd][w] = {"median": round(statistics.median([d for _, d in got]), 1), "n": len(got),
                               "scope": "all"}
            else:
                out[cmd][w] = {"median": None, "n": len(got), "scope": None}
    return out


# ------------------------------------------------------------------ measure

def build_options(cwd):
    """The lightest session: no tool, no setting, no MCP server, no
    thinking, the lightest model, one turn, a one-line system prompt."""
    from claude_agent_sdk import ClaudeAgentOptions
    return ClaudeAgentOptions(cwd=cwd, tools=[], setting_sources=[], strict_mcp_config=True,
                              mcp_servers={}, model=MODEL, max_turns=1, thinking={"type": "disabled"},
                              system_prompt="Réponds en un mot.", permission_mode="default")


def sdk_client_factory(cwd):
    from claude_agent_sdk import ClaudeSDKClient
    return ClaudeSDKClient(options=build_options(cwd))


class Measurer:
    """One measure at a time: a second ask while one goes waits for it."""

    def __init__(self, store, log_dir, client_factory=None, scratch=None):
        self.store = store
        self.log_dir = log_dir
        self.client_factory = client_factory or sdk_client_factory
        self.scratch = scratch or SCRATCH
        self.task = None
        # The last measure: when it ended, whether it gave the windows, why
        # not, what it cost — shown beside the gauges.
        self.last = {"at": None, "ok": None, "error": "", "cost": None, "why": "", "run_id": None}
        self.going_since = None

    def public(self):
        return {**self.last, "going": bool(self.task and not self.task.done()), "going_since": self.going_since}

    def limits(self):
        if not self.store:
            return {}
        try:
            return self.store.latest_limits()
        except Exception:
            return {}

    def stale(self, now=None):
        a = oldest_age(self.limits(), now)
        return a is None or a > STALE_S

    def start(self, why):
        """In the background; the one going when one goes."""
        if self.task and not self.task.done():
            return self.task
        self.going_since = datetime.now().isoformat(timespec="seconds")
        self.task = asyncio.get_running_loop().create_task(self._measure(why))
        return self.task

    async def measure(self, why):
        return await asyncio.shield(self.start(why))

    async def _measure(self, why):
        run_id = "mesure-" + uuid.uuid4().hex[:10]
        tally = stats_mod.Tally()
        log_path = self._open_log()
        started = runner_mod._now()
        got, error, api_error = [], "", ""
        try:
            os.makedirs(self.scratch, exist_ok=True)

            async def go():
                nonlocal api_error
                client = self.client_factory(self.scratch)
                async with client:
                    await client.query(PROMPT)
                    result = None
                    async for msg in client.receive_messages():
                        at = runner_mod._now()
                        body = self._log(log_path, msg, at)
                        kind = type(msg).__name__
                        if kind == "AssistantMessage" and isinstance(body, dict) and body.get("error"):
                            api_error = str(body["error"])
                        for k, x in tally.feed(kind, body, at):
                            if k == "limit":
                                got.append({**x, "source": KIND})
                        if kind == "ResultMessage":
                            result = body
                            break
                    if {m["window"] for m in got} != set(WINDOWS) and not api_error \
                            and not (result or {}).get("is_error"):
                        # No event gave both windows: `/usage`, same session.
                        await client.query(runner_mod.USAGE_COMMAND)
                        async for msg in client.receive_messages():
                            body = self._log(log_path, msg, runner_mod._now(), probe=True)
                            if type(msg).__name__ == "ResultMessage":
                                text = body.get("result") if isinstance(body, dict) else ""
                                have = {m["window"] for m in got}
                                got.extend({**m, "source": KIND} for m in
                                           stats_mod.limits_from_usage(text or "", runner_mod._now())
                                           if m["window"] not in have)
                                break
                    return result
            result = await asyncio.wait_for(go(), TIMEOUT)
            if api_error:
                error = runner_mod.API_ERRORS.get(api_error, api_error)
            elif result and result.get("is_error"):
                error = "; ".join(result.get("errors") or []) or result.get("result") or "erreur"
            elif not got:
                error = "Claude Code n'a donné aucune des deux fenêtres"
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError:
            error = f"pas de réponse en {int(TIMEOUT)} s — hors ligne ?"
        except Exception as e:
            error = describe_failure(e)
        ended = runner_mod._now()
        stats_mod.apply_model_usage(tally)
        cost = stats_mod.totals_summary(tally.totals, stats_mod._seconds(started, ended))
        if self.store:
            try:
                cost = self.store.record_run(
                    run_id=run_id, feature=None, work=None, command=COMMAND, mode=None,
                    started_at=started, ended_at=ended, tally=tally, next_line=None,
                    outcome="erreur" if error else "terminé", log_path=log_path or None, kind=KIND) or cost
                for m in got:
                    self.store.record_limit(run_id, m)
            except Exception as e:
                error = error or f"mesure non enregistrée : {e}"
        if cost is not None and tally.model_usage:
            cost["usd"] = round(sum((u.get("costUSD") or 0) for u in tally.model_usage.values()), 6)
        self.last = {"at": ended, "ok": not error, "error": error, "cost": cost, "why": why,
                     "run_id": run_id, "windows": sorted({m["window"] for m in got})}
        self.going_since = None
        print(f"Consommation : mesure ({why}) — "
              + (f"non faite : {error}" if error else
                 ", ".join(f"{WINDOW_NAMES[m['window']]} {round(m['utilization'] * 100)} %" for m in got))
              + (f" · coût : {cost.get('read_tokens')} tokens lus, {cost.get('output_tokens')} écrits"
                 if cost else ""), flush=True)
        return self.last

    # ---------------------------------------------------------------- log

    def _open_log(self):
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            path = os.path.join(self.log_dir, f"{stamp}-mesure.jsonl")
            n = 1
            while os.path.exists(path):
                n += 1
                path = os.path.join(self.log_dir, f"{stamp}-mesure-{n}.jsonl")
            open(path, "w", encoding="utf-8").close()
            return path
        except OSError:
            return ""

    @staticmethod
    def _log(path, msg, at, probe=False):
        body = runner_mod._body(msg)
        if path:
            try:
                entry = {"at": at, "type": type(msg).__name__, "message": body}
                if probe:
                    entry["probe"] = "usage"
                with open(path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
            except (OSError, TypeError, ValueError):
                pass
        return body


def describe_failure(e):
    """An exception of the SDK, in French: what she can act on."""
    name = type(e).__name__
    text = str(e)
    if name == "CLINotFoundError":
        return "Claude Code est introuvable sur cet ordinateur"
    if re.search(r"log ?in|authenticat|unauthori[sz]ed|401", text, re.I):
        return "Claude Code n'est pas connecté sur cet ordinateur"
    if re.search(r"ENOTFOUND|ECONNREFUSED|getaddrinfo|network|offline|timed? ?out", text, re.I):
        return "Claude injoignable — hors ligne ?"
    return f"{name}: {text}"[:300]
