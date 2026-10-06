"""Run one chain command through `ClaudeSDKClient` — TECHNICAL_V1 §5-§7.

- The command is sent as typed in a session: `/1_lexique premiere-app-3`.
- Project settings are loaded: `setting_sources` left at its default, never
  bare mode — `.claude/commands/`, `.claude/agents/` and `CLAUDE.md` load.
- `cwd` is the application folder.
- Every permission request becomes a card in the page; the run waits.
- One run at a time, whatever the application (1.6): a run going in one
  application blocks a launch in every other.
- Stop now = `interrupt()`. Stop at the next lot = `stop.md` in the main
  checkout, `/8_code` only.
- A run ends only when the orchestrator's turn has ended AND no background
  agent it started is still pending. The CLI starts subagents in the
  background by default and wakes the orchestrator when one finishes, so the
  first `ResultMessage` is the end of a turn, not of the run (cockpit 1.1).
"""
import asyncio
import itertools
import json
import os
import re
import subprocess
import uuid
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime

import nextline
import stats as stats_mod
import stream as stream_mod

MAX_EVENTS = 5000
# The events a run's log does not hold — the page's own and the server's —
# kept in memory and merged by time with the log's when a page opens (1.5).
CONTROL_EVENTS = {"run_started", "status", "permission", "permission_resolved", "stopping",
                  "error", "idle_wait", "limits", "limits_unavailable", "run_ended"}
# A reopened page is given at most this many events: it keeps no more.
REPLAY_MAX = 3000
STOP_COMMAND = "8_code"

# No message for this long while an agent is pending: the page asks.
IDLE_CEILING = 600.0
# Without the CLI's own session-state frames, how long to wait for a wake-up
# turn after a result with nothing pending, before calling the run over.
END_GRACE = 15.0
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
CONTINUE_PROMPT = "Continue the command where you stopped, and end with its Next: line."
# Asked once at the end of a run, in its own session: a local command, no
# model call (TECHNICAL_V1 §13.2). Its report gives both usage windows.
USAGE_COMMAND = "/usage"
USAGE_TIMEOUT = 30.0


class Busy(Exception):
    def __init__(self, msg, run=None):
        super().__init__(msg)
        self.run = run


class NotRunning(Exception):
    pass


def repo_key(path: str) -> str:
    return os.path.normcase(os.path.realpath(path))


# The cockpit's two modes, as the SDK's `permission_mode` names them. The
# mode is passed explicitly on every run, never left to the CLI's default.
PERMISSION_MODES = {"auto": "auto", "manuel": "default"}


def build_options(cwd: str, can_use_tool, resume: str | None = None, mode: str = "auto"):
    """The SDK options. `setting_sources` is left unset (all sources, the
    CLI default) and nothing asks for bare mode. The session-state frames are
    asked for: `idle` is how the CLI says no agent is live and no wake-up turn
    is owed. In auto mode a request still reaches `can_use_tool` when the
    classifier sends it back to a prompt: it becomes a card, as in manual.

    1.4: subagent text is forwarded. Without it, a subagent message holding
    no tool call never reaches the stream — a nested agent that only
    answers is missing, and its usage with it (TECHNICAL_V1 §13.1)."""
    from dataclasses import fields
    from claude_agent_sdk import ClaudeAgentOptions
    extra = {}
    if "forward_subagent_text" in {f.name for f in fields(ClaudeAgentOptions)}:
        extra["forward_subagent_text"] = True
    return ClaudeAgentOptions(cwd=cwd, can_use_tool=can_use_tool, resume=resume,
                              permission_mode=PERMISSION_MODES[mode],
                              env={"CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS": "1"}, **extra)


def sdk_client_factory(cwd: str, can_use_tool, resume: str | None = None, mode: str = "auto"):
    from claude_agent_sdk import ClaudeSDKClient
    return ClaudeSDKClient(options=build_options(cwd, can_use_tool, resume, mode))


@dataclass
class Permission:
    id: str
    tool: str
    input: dict
    title: str | None
    agent: str
    future: asyncio.Future = field(repr=False)

    def to_dict(self):
        try:
            shown = json.dumps(self.input, ensure_ascii=False, indent=2)
        except (TypeError, ValueError):
            shown = str(self.input)
        if len(shown) > 4000:
            shown = shown[:4000] + "\n…"
        return {"id": self.id, "tool": self.tool, "input": shown,
                "title": self.title, "agent": self.agent}


@dataclass
class Run:
    id: str
    repo: str
    work: str
    feature: str
    command: str
    args: str
    started_at: str
    status: str = "starting"          # starting, running, ended
    outcome: str = ""                 # terminé, interrompu, erreur
    relay: str = ""
    next: dict | None = None
    error: str = ""
    client: object = None
    task: asyncio.Task | None = None
    # What the stream says of the agents, the same reader the log is replayed
    # with (stream.py).
    reader: stream_mod.Reader = field(default_factory=stream_mod.Reader, repr=False)
    permissions: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    subscribers: set = field(default_factory=set)
    stop_requested: bool = False
    message: str = ""                 # what is sent; the command, or the continuation
    resume: str | None = None         # session id to continue
    session_id: str = ""
    log_path: str = ""
    mode: str = "auto"
    worktrees_left: list = field(default_factory=list)
    turn_ended: bool = False
    state: str | None = None          # the CLI's last session state, None if never sent
    idle: dict | None = None          # set while the page is asked to wait or stop
    idle_future: asyncio.Future | None = field(default=None, repr=False)
    tally: stats_mod.Tally = field(default_factory=stats_mod.Tally, repr=False)
    ended_at: str = ""
    usage: dict | None = None         # the run's totals, once it ended
    replay_cache: object = field(default=None, repr=False)
    logged: int = 0                   # the run's lines in its log, probes left out

    @property
    def prompt(self):
        return f"/{self.command} {self.args}".rstrip()

    @property
    def agents(self):
        return self.reader.agents

    @property
    def active(self):
        return self.reader.active

    @property
    def last_text(self):
        return self.reader.last_text

    def label(self, parent_id):
        return self.reader.label(parent_id)

    def active_inputs(self):
        """The Agent tool's input of each agent running, oldest first."""
        return [{"id": t, "agent": self.agents.get(t, "agent"), "input": self.reader.inputs.get(t) or {}}
                for t in self.active]

    def snapshot(self):
        return {
            "id": self.id, "command": self.command, "args": self.args,
            "prompt": self.prompt, "work": self.work, "status": self.status,
            "outcome": self.outcome, "error": self.error,
            "started_at": self.started_at,
            "agents": [self.agents.get(t, "agent") for t in self.active],
            "active": [{"id": a["id"], "agent": a["agent"],
                        "description": a["input"].get("description") or "",
                        "lot": stats_mod.lot_of_input(a["input"])["lot"]} for a in self.active_inputs()],
            "permissions": [p.to_dict() for p in self.permissions.values()],
            "relay": self.relay, "next": self.next,
            "stop_next_lot": self.command == STOP_COMMAND,
            "continued": bool(self.resume), "mode": self.mode, "session_id": self.session_id,
            "log_path": self.log_path, "worktrees_left": list(self.worktrees_left),
            "idle": self.idle,
            "usage": self.usage,
            "passes": [p.summary() for p in self.tally.passes.values() if p.ended],
            "can_continue": (self.status == "ended" and bool(self.session_id)
                             and bool(self.next) and self.next.get("kind") == "unknown"),
        }


class Runner:
    def __init__(self, client_factory=sdk_client_factory, on_end=None, log_dir=None,
                 mode_getter=lambda: "auto", stats=None, measure_limits=None):
        self.client_factory = client_factory
        self.on_end = on_end
        self.mode_getter = mode_getter
        self.log_dir = log_dir or LOG_DIR
        self.stats = stats                # a stats.Store, or None
        # The end-of-run /usage: on for the real SDK client, off for fakes
        # unless a test asks for it.
        self.measure_limits = (client_factory is sdk_client_factory
                               if measure_limits is None else measure_limits)
        self.runs: dict[str, Run] = {}
        # The page's stream (1.6): every run's events, whatever its application.
        self.watchers: set = set()
        self._seq = itertools.count(1)

    # -------------------------------------------------------------- query

    def current(self, repo: str) -> Run | None:
        return self.runs.get(repo_key(repo))

    def is_running(self, repo: str) -> bool:
        r = self.current(repo)
        return bool(r and r.status != "ended")

    def going(self) -> Run | None:
        """The run going, whatever its application — there is one at most."""
        return next((r for r in self.runs.values() if r.id and r.status != "ended"), None)

    # -------------------------------------------------------------- start

    async def start(self, repo: str, work: str, feature: str, command: str, args: str,
                    resume: str | None = None, message: str | None = None) -> Run:
        key = repo_key(repo)
        # Check and claim with no await in between: the lock is this line.
        # One run at a time, whatever the application (1.6).
        other = self.going()
        if other:
            raise Busy("une commande tourne déjà sur ce dépôt" if repo_key(other.repo) == key
                       else f"une commande tourne déjà dans une autre application : {other.prompt}", other)
        run = Run(id=uuid.uuid4().hex[:12], repo=repo, work=work, feature=feature,
                  command=command, args=args,
                  started_at=datetime.now().isoformat(timespec="seconds"),
                  resume=resume)
        run.message = message or run.prompt
        run.mode = self.mode_getter() if self.mode_getter() in PERMISSION_MODES else "auto"
        old = self.runs.get(key)
        if old:
            run.subscribers = old.subscribers
        self.runs[key] = run
        self._emit(run, "run_started", run.snapshot())
        run.task = asyncio.create_task(self._drive(run))
        return run

    async def _drive(self, run: Run):
        async def can_use_tool(tool_name, tool_input, ctx):
            return await self._ask_permission(run, tool_name, tool_input, ctx)

        try:
            self._open_log(run)
            kwargs = {"resume": run.resume} if run.resume else {}
            client = self.client_factory(run.repo, can_use_tool, mode=run.mode, **kwargs)
            run.client = client
            async with client:
                run.status = "running"
                self._emit(run, "status", run.snapshot())
                if run.stop_requested:
                    raise asyncio.CancelledError()
                await client.query(run.message)
                await self._read(run, client)
                if self.measure_limits and not run.stop_requested:
                    await self._measure_limits(run, client)
            run.outcome = "interrompu" if run.stop_requested else (run.outcome or "terminé")
        except asyncio.CancelledError:
            run.outcome = "interrompu"
        except Exception as e:  # the run ends, the page says why
            run.outcome = "erreur"
            run.error = f"{type(e).__name__}: {e}"
        finally:
            self._finish(run)

    async def _read(self, run: Run, client):
        """Read the whole stream. A `ResultMessage` ends a turn; the run ends
        when the turn has ended and nothing the orchestrator started is
        pending (see `_over`)."""
        queue: asyncio.Queue = asyncio.Queue()

        async def pump():
            try:
                async for msg in client.receive_messages():
                    # The time it was received: messages carry none of their own.
                    queue.put_nowait(("msg", (msg, _now())))
                    # Let the handler see this message before the stream moves
                    # on: a permission request is labelled from what it handled.
                    await asyncio.sleep(0)
                queue.put_nowait(("end", None))
            except asyncio.CancelledError:
                raise
            except Exception as e:
                queue.put_nowait(("err", e))

        reader = asyncio.create_task(pump())
        try:
            while True:
                timeout = self._timeout(run)
                try:
                    kind, payload = await asyncio.wait_for(queue.get(), timeout)
                except asyncio.TimeoutError:
                    if self._over(run, grace_elapsed=True):
                        return
                    if run.active and not run.permissions:
                        if await self._ask_idle(run) == "stop":
                            run.stop_requested = True
                            return
                    continue
                if kind == "end":
                    return
                if kind == "err":
                    raise payload
                msg, at = payload
                body = self._log(run, msg, at)
                self._count(run, msg, body, at)
                self._handle(run, msg, body, at)
                if self._over(run):
                    return
        finally:
            reader.cancel()
            await asyncio.gather(reader, return_exceptions=True)

    @staticmethod
    def _over(run: Run, grace_elapsed: bool = False) -> bool:
        if not run.turn_ended:
            return False
        if run.stop_requested:
            return True
        if run.state is not None:       # the CLI says: idle = nothing live, nothing owed
            return run.state == "idle"
        return not run.active and grace_elapsed

    @staticmethod
    def _timeout(run: Run):
        if run.permissions:             # waiting on the Product Owner, not on an agent
            return None
        if run.turn_ended and run.state is None and not run.active:
            return END_GRACE
        return IDLE_CEILING if run.active else None

    async def _ask_idle(self, run: Run) -> str:
        """The idle ceiling: the page says what the run waits on and asks."""
        loop = asyncio.get_running_loop()
        run.idle_future = loop.create_future()
        run.idle = {"agents": [run.agents.get(t, "agent") for t in run.active],
                    "since": datetime.now().isoformat(timespec="seconds"),
                    "minutes": round(IDLE_CEILING / 60, 1)}
        self._emit(run, "idle_wait", dict(run.idle))
        try:
            return await run.idle_future
        finally:
            run.idle = None
            run.idle_future = None

    def continue_waiting(self, repo: str):
        run = self.current(repo)
        if not run or not run.idle_future or run.idle_future.done():
            raise NotRunning("la commande n'attend plus de décision")
        run.idle_future.set_result("continue")

    async def continue_session(self, repo: str) -> Run:
        """Send one message into the SAME session of the run that ended
        without a `Next:` line."""
        old = self.current(repo)
        if not old or old.status != "ended" or not old.id:
            raise NotRunning("aucune commande terminée à continuer")
        if not old.session_id:
            raise NotRunning("pas d'identifiant de session pour cette commande")
        return await self.start(repo, old.work, old.feature, old.command, old.args,
                                resume=old.session_id, message=CONTINUE_PROMPT)

    def _finish(self, run: Run):
        for p in list(run.permissions.values()):
            if not p.future.done():
                p.future.set_result(False)
        run.permissions.clear()
        if run.idle_future and not run.idle_future.done():
            run.idle_future.set_result("stop")
        run.idle = None
        run.reader.active.clear()
        if not run.relay:
            run.relay = run.last_text
        run.next = nextline.parse(run.relay).to_dict()
        run.ended_at = _now()
        self._record(run)
        run.worktrees_left = list_worktrees(run.repo)
        run.status = "ended"
        run.client = None
        self._emit(run, "run_ended", run.snapshot())
        if self.on_end:
            try:
                self.on_end(run)
            except Exception as e:
                self._emit(run, "error", {"message": f"mémorisation du relais : {e}"})

    # ----------------------------------------------------------------- log

    def _open_log(self, run: Run):
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            name = re.sub(r"[^A-Za-z0-9_-]", "_", run.command) or "run"
            path = os.path.join(self.log_dir, f"{stamp}-{name}.jsonl")
            n = 1
            while os.path.exists(path):
                n += 1
                path = os.path.join(self.log_dir, f"{stamp}-{name}-{n}.jsonl")
            open(path, "w", encoding="utf-8").close()
            run.log_path = path
        except OSError as e:
            self._emit(run, "error", {"message": f"journal brut non ouvert : {e}"})

    def _log(self, run: Run, msg, at=None, probe=False):
        """One line per message, with the time it was received. Returns the
        body, which the count reads too."""
        body = _body(msg)
        if not run.log_path:
            return body
        try:
            entry = {"at": at or _now(), "type": type(msg).__name__, "message": body}
            if probe:
                entry["probe"] = "usage"     # the end-of-run /usage: not the run's work
            line = json.dumps(entry, ensure_ascii=False, default=str)
            with open(run.log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            if not probe:
                run.logged += 1
        except (OSError, TypeError, ValueError):
            pass
        return body

    # --------------------------------------------------------- consumption

    def _count(self, run: Run, msg, body, at):
        for kind, x in run.tally.feed(type(msg).__name__, body, at):
            if kind == "limit":
                self._store_limit(run, x)

    def _store_limit(self, run: Run, m):
        if self.stats:
            try:
                self.stats.record_limit(run.id, m)
            except Exception as e:
                self._emit(run, "error", {"message": f"mesure d'usage non enregistrée : {e}"})
        self._emit(run, "limits", m)

    async def _measure_limits(self, run: Run, client):
        """`/usage` in the run's own session, once it is over: a local
        command, no model call. Its lines are logged as a probe, never
        counted as the run's work, and its text never becomes the relay."""
        from claude_agent_sdk import ResultMessage

        async def ask():
            await client.query(USAGE_COMMAND)
            async for msg in client.receive_messages():
                self._log(run, msg, _now(), probe=True)
                if isinstance(msg, ResultMessage):
                    return msg.result or ""
            return ""
        try:
            text = await asyncio.wait_for(ask(), USAGE_TIMEOUT)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            self._emit(run, "limits_unavailable", {"reason": f"{type(e).__name__}: {e}"})
            return
        got = stats_mod.limits_from_usage(text, _now())
        if not got:
            self._emit(run, "limits_unavailable", {"reason": "le rapport /usage ne donne aucune fenêtre"})
        for m in got:
            self._store_limit(run, m)

    def _record(self, run: Run):
        """The run and its agents, into the store. The agents' output comes
        from the latest result's model_usage, read now: the run is over."""
        stats_mod.apply_model_usage(run.tally)
        run.usage = stats_mod.totals_summary(run.tally.totals,
                                             stats_mod._seconds(run.started_at, run.ended_at))
        if not self.stats or not run.id:
            return
        try:
            run.usage = self.stats.record_run(
                run_id=run.id, feature=run.feature, work=run.work, command=run.prompt,
                mode=run.mode, started_at=run.started_at, ended_at=run.ended_at,
                tally=run.tally, next_line=(run.next or {}).get("raw") or None,
                outcome=run.outcome, log_path=run.log_path, resumed=bool(run.resume), app=run.repo)
        except Exception as e:
            self._emit(run, "error", {"message": f"consommation non enregistrée : {e}"})

    # ------------------------------------------------------------ messages

    def _handle(self, run: Run, msg, body=None, at=None):
        """The message as the log holds it, read by the stream's reader —
        the one a reopened page's replay uses — then what ends a turn."""
        kind = type(msg).__name__
        body = body if isinstance(body, dict) else _body(msg)
        if not isinstance(body, dict):
            return
        if kind in ("AssistantMessage", "UserMessage"):
            run.turn_ended = False
        for t, d in run.reader.feed(kind, body, run.tally):
            self._emit(run, t, d, at)
        if kind == "ResultMessage":
            run.turn_ended = True
            if body.get("session_id"):
                run.session_id = body["session_id"]
            run.relay = body.get("result") or run.last_text
            if body.get("is_error"):
                run.outcome = "erreur"
                run.error = "; ".join(body.get("errors") or []) or (body.get("subtype") or "erreur")
            reason = body.get("terminal_reason") or ""
            if reason.startswith("aborted"):
                run.outcome = "interrompu"
        elif kind == "SystemMessage" and body.get("subtype") == "session_state_changed":
            run.state = (body.get("data") or {}).get("state")

    # --------------------------------------------------------- permissions

    async def _ask_permission(self, run: Run, tool_name, tool_input, ctx):
        from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny
        if run.stop_requested:
            return PermissionResultDeny(message="Arrêt demandé depuis le cockpit", interrupt=True)
        loop = asyncio.get_running_loop()
        agent = run.label(run.active[-1]) if run.active else "orchestrateur"
        perm = Permission(id=uuid.uuid4().hex[:10], tool=tool_name, input=tool_input or {},
                          title=getattr(ctx, "title", None), agent=agent,
                          future=loop.create_future())
        run.permissions[perm.id] = perm
        self._emit(run, "permission", perm.to_dict())
        try:
            allowed = await perm.future
        finally:
            run.permissions.pop(perm.id, None)
        self._emit(run, "permission_resolved", {"id": perm.id, "allowed": allowed})
        if allowed:
            return PermissionResultAllow()
        return PermissionResultDeny(message="Refusé par le Product Owner depuis le cockpit")

    def answer_permission(self, repo: str, perm_id: str, allow: bool):
        run = self.current(repo)
        if not run or perm_id not in run.permissions:
            raise NotRunning("cette demande d'autorisation n'attend plus")
        fut = run.permissions[perm_id].future
        if not fut.done():
            fut.set_result(bool(allow))

    # ------------------------------------------------------------ stopping

    async def stop_now(self, repo: str):
        run = self.current(repo)
        if not run or run.status == "ended":
            raise NotRunning("aucune commande ne tourne")
        run.stop_requested = True
        self._emit(run, "stopping", {"how": "maintenant"})
        for p in list(run.permissions.values()):
            if not p.future.done():
                p.future.set_result(False)
        if run.idle_future and not run.idle_future.done():
            run.idle_future.set_result("stop")
        if run.client is not None and run.status == "running":
            try:
                await run.client.interrupt()
                return
            except Exception as e:
                self._emit(run, "error", {"message": f"interrupt() a échoué : {e}"})
        if run.task:
            run.task.cancel()

    @staticmethod
    def stop_file(repo: str, feature: str) -> str:
        # cmd/8_code.md:444-447 — at the feature folder's root, in the main
        # checkout, never in the worktree.
        return os.path.join(repo, "docs", "features", feature, "stop.md")

    def stop_at_next_lot(self, repo: str) -> str:
        run = self.current(repo)
        if not run or run.status == "ended":
            raise NotRunning("aucune commande ne tourne")
        if run.command != STOP_COMMAND:
            raise NotRunning("« arrêter au prochain lot » ne vaut que pour /8_code")
        path = self.stop_file(repo, run.feature)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Arrêt au prochain lot demandé depuis le cockpit, "
                    f"{datetime.now().isoformat(timespec='seconds')}.\n")
        self._emit(run, "stopping", {"how": "prochain lot", "file": path})
        return path

    @staticmethod
    def disarm_stop_file(repo: str, feature: str) -> str | None:
        """`stop1.md` is the disarmed form (cmd/8_code.md:462-464)."""
        path = Runner.stop_file(repo, feature)
        if not os.path.exists(path):
            return None
        target = os.path.join(os.path.dirname(path), "stop1.md")
        if os.path.exists(target):
            os.remove(path)
        else:
            os.replace(path, target)
        return target

    # -------------------------------------------------------------- replay

    def replay(self, repo: str):
        """What a page opening now is given (1.5): the run's message events
        rebuilt from its log — the same reader as live — and the server's own
        events kept in memory, in time order. The last REPLAY_MAX of them,
        and how many were left out before."""
        run = self.current(repo)
        if not run or not run.id:
            return [], 0
        if run.log_path and os.path.isfile(run.log_path):
            msgs, run.replay_cache = stream_mod.replay(run.log_path, run.replay_cache)
            # Each server event sits after the log lines written when it was
            # emitted (`after`): its place among the log's events is exact.
            keyed = [((line, 1, k), {"seq": 0, "type": t, "run": run.id, "app": run.repo, "data": d, "at": at})
                     for k, (line, at, t, d) in enumerate(msgs)]
            keyed += [((e.get("after", 0), 0, e["seq"]), e) for e in run.events if e["type"] in CONTROL_EVENTS]
            keyed.sort(key=lambda x: x[0])
            evs = [e for _, e in keyed]
        else:
            evs = list(run.events)          # no log: what memory holds
        dropped = max(0, len(evs) - REPLAY_MAX)
        return evs[dropped:], dropped

    async def wait_ended(self, repo: str, timeout: float) -> bool:
        """True once the run's task is over, within `timeout` seconds."""
        run = self.current(repo)
        if not run or not run.task or run.task.done():
            return True
        try:
            await asyncio.wait_for(asyncio.shield(run.task), timeout)
        except asyncio.TimeoutError:
            return False
        except Exception:
            pass
        return True

    # ----------------------------------------------------------- worktrees

    def live_worktrees(self, repo: str) -> list[str]:
        """During a run, the worktrees other than the main checkout — where
        a shape-4 blocking file is answered while the Arbitre polls it."""
        if not self.is_running(repo):
            return []
        return list_worktrees(repo)

    # -------------------------------------------------------------- events

    def subscribe(self, repo: str) -> asyncio.Queue:
        key = repo_key(repo)
        run = self.runs.get(key)
        if run is None:
            run = Run(id="", repo=repo, work="", feature="", command="", args="",
                      started_at="", status="ended")
            self.runs[key] = run
        q = asyncio.Queue()
        run.subscribers.add(q)
        return q

    def unsubscribe(self, repo: str, q):
        run = self.runs.get(repo_key(repo))
        if run:
            run.subscribers.discard(q)

    def watch(self) -> asyncio.Queue:
        """Every run's events, whatever its application (1.6): a card, an
        end, an idle question reach the page from any screen."""
        q = asyncio.Queue()
        self.watchers.add(q)
        return q

    def unwatch(self, q):
        self.watchers.discard(q)

    def _emit(self, run: Run, kind: str, data: dict, at: str | None = None):
        ev = {"seq": next(self._seq), "type": kind, "run": run.id, "app": run.repo, "data": data,
              "at": at or _now(), "after": run.logged}
        run.events.append(ev)
        if len(run.events) > MAX_EVENTS:
            del run.events[: len(run.events) - MAX_EVENTS]
        for q in list(run.subscribers) + [w for w in self.watchers if w not in run.subscribers]:
            q.put_nowait(ev)


def _now() -> str:
    return datetime.now().isoformat(timespec="milliseconds")


def list_worktrees(repo: str) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", repo, "worktree", "list", "--porcelain"],
                             capture_output=True, text=True, timeout=15, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    paths = [l[len("worktree "):].strip() for l in out.splitlines() if l.startswith("worktree ")]
    main = repo_key(repo)
    return [p for p in paths if repo_key(p) != main]


def _body(msg):
    """The message as a dict — what the log writes and what the reader reads.
    A message `asdict` cannot copy is read one level down, field by field."""
    if not is_dataclass(msg):
        return repr(msg)
    try:
        return asdict(msg)
    except (TypeError, ValueError):
        out = {}
        for k, v in vars(msg).items():
            if isinstance(v, list):
                v = [_body(x) if is_dataclass(x) else x for x in v]
            out[k] = v
        return out
