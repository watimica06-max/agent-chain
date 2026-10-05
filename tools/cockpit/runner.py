"""Run one chain command through `ClaudeSDKClient` — TECHNICAL_V1 §5-§7.

- The command is sent as typed in a session: `/1_lexique premiere-app-3`.
- Project settings are loaded: `setting_sources` left at its default, never
  bare mode — `.claude/commands/`, `.claude/agents/` and `CLAUDE.md` load.
- `cwd` is the application folder.
- Every permission request becomes a card in the page; the run waits.
- One run at a time per repository.
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

AGENT_TOOLS = {"Agent", "Task"}
MAX_EVENTS = 5000
STOP_COMMAND = "8_code"

# No message for this long while an agent is pending: the page asks.
IDLE_CEILING = 600.0
# Without the CLI's own session-state frames, how long to wait for a wake-up
# turn after a result with nothing pending, before calling the run over.
END_GRACE = 15.0
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
CONTINUE_PROMPT = "Continue the command where you stopped, and end with its Next: line."
# What the Agent tool's result says when the subagent was started in the background.
BACKGROUND_RESULT = re.compile(r"async_launched|in the background|agentId", re.I)
TERMINAL_STATUSES = {"completed", "failed", "stopped", "killed"}


class Busy(Exception):
    pass


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
    classifier sends it back to a prompt: it becomes a card, as in manual."""
    from claude_agent_sdk import ClaudeAgentOptions
    return ClaudeAgentOptions(cwd=cwd, can_use_tool=can_use_tool, resume=resume,
                              permission_mode=PERMISSION_MODES[mode],
                              env={"CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS": "1"})


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
    agents: dict = field(default_factory=dict)       # tool_use_id -> label
    active: list = field(default_factory=list)       # tool_use_ids running
    permissions: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    subscribers: set = field(default_factory=set)
    stop_requested: bool = False
    last_text: str = ""
    message: str = ""                 # what is sent; the command, or the continuation
    resume: str | None = None         # session id to continue
    session_id: str = ""
    log_path: str = ""
    mode: str = "auto"
    worktrees_left: list = field(default_factory=list)
    tasks: dict = field(default_factory=dict)        # task_id -> tool_use_id
    background: set = field(default_factory=set)     # tool_use_ids started in the background
    turn_ended: bool = False
    state: str | None = None          # the CLI's last session state, None if never sent
    idle: dict | None = None          # set while the page is asked to wait or stop
    idle_future: asyncio.Future | None = field(default=None, repr=False)

    @property
    def prompt(self):
        return f"/{self.command} {self.args}".rstrip()

    def label(self, parent_id):
        if not parent_id:
            return "orchestrateur"
        return self.agents.get(parent_id, "agent")

    def snapshot(self):
        return {
            "id": self.id, "command": self.command, "args": self.args,
            "prompt": self.prompt, "work": self.work, "status": self.status,
            "outcome": self.outcome, "error": self.error,
            "started_at": self.started_at,
            "agents": [self.agents.get(t, "agent") for t in self.active],
            "permissions": [p.to_dict() for p in self.permissions.values()],
            "relay": self.relay, "next": self.next,
            "stop_next_lot": self.command == STOP_COMMAND,
            "continued": bool(self.resume), "mode": self.mode, "session_id": self.session_id,
            "log_path": self.log_path, "worktrees_left": list(self.worktrees_left),
            "idle": self.idle,
            "can_continue": (self.status == "ended" and bool(self.session_id)
                             and bool(self.next) and self.next.get("kind") == "unknown"),
        }


class Runner:
    def __init__(self, client_factory=sdk_client_factory, on_end=None, log_dir=None,
                 mode_getter=lambda: "auto"):
        self.client_factory = client_factory
        self.on_end = on_end
        self.mode_getter = mode_getter
        self.log_dir = log_dir or LOG_DIR
        self.runs: dict[str, Run] = {}
        self._seq = itertools.count(1)

    # -------------------------------------------------------------- query

    def current(self, repo: str) -> Run | None:
        return self.runs.get(repo_key(repo))

    def is_running(self, repo: str) -> bool:
        r = self.current(repo)
        return bool(r and r.status != "ended")

    # -------------------------------------------------------------- start

    async def start(self, repo: str, work: str, feature: str, command: str, args: str,
                    resume: str | None = None, message: str | None = None) -> Run:
        key = repo_key(repo)
        # Check and claim with no await in between: the lock is this line.
        if self.is_running(repo):
            raise Busy("une commande tourne déjà sur ce dépôt")
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
                    queue.put_nowait(("msg", msg))
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
                self._log(run, payload)
                self._handle(run, payload)
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
        run.active.clear()
        if not run.relay:
            run.relay = run.last_text
        run.next = nextline.parse(run.relay).to_dict()
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

    def _log(self, run: Run, msg):
        if not run.log_path:
            return
        try:
            body = asdict(msg) if is_dataclass(msg) else repr(msg)
            line = json.dumps({"at": datetime.now().isoformat(timespec="milliseconds"),
                               "type": type(msg).__name__, "message": body},
                              ensure_ascii=False, default=str)
            with open(run.log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except (OSError, TypeError, ValueError):
            pass

    # ------------------------------------------------------------ messages

    def _handle(self, run: Run, msg):
        from claude_agent_sdk import (AssistantMessage, UserMessage, ResultMessage, SystemMessage,
                                      TextBlock, ToolUseBlock, ToolResultBlock,
                                      TaskStartedMessage, TaskNotificationMessage,
                                      TaskUpdatedMessage)
        if isinstance(msg, AssistantMessage):
            run.turn_ended = False
            who = run.label(msg.parent_tool_use_id)
            for block in msg.content:
                if isinstance(block, TextBlock):
                    if not msg.parent_tool_use_id:
                        run.last_text = block.text
                    self._emit(run, "text", {"agent": who, "text": block.text})
                elif isinstance(block, ToolUseBlock):
                    if block.name in AGENT_TOOLS:
                        inp = block.input or {}
                        name = inp.get("subagent_type") or "agent"
                        desc = inp.get("description") or ""
                        run.agents[block.id] = name
                        run.active.append(block.id)
                        self._emit(run, "agent_started", {"agent": name, "description": desc,
                                                          "by": who})
                    else:
                        self._emit(run, "tool", {"agent": who, "tool": block.name,
                                                 "summary": _summary(block.name, block.input)})
        elif isinstance(msg, UserMessage):
            run.turn_ended = False
            content = msg.content if isinstance(msg.content, list) else []
            for block in content:
                if isinstance(block, ToolResultBlock) and block.tool_use_id in run.active:
                    if BACKGROUND_RESULT.search(_text_of(block.content)):
                        # Started in the background: still pending until its
                        # completion notification.
                        run.background.add(block.tool_use_id)
                        self._emit(run, "agent_background",
                                   {"agent": run.agents.get(block.tool_use_id)})
                    else:
                        run.active.remove(block.tool_use_id)
                        self._emit(run, "agent_ended", {"agent": run.agents.get(block.tool_use_id)})
        elif isinstance(msg, TaskStartedMessage):
            if msg.tool_use_id:
                run.tasks[msg.task_id] = msg.tool_use_id
        elif isinstance(msg, (TaskNotificationMessage, TaskUpdatedMessage)):
            status = msg.status
            if status in TERMINAL_STATUSES:
                tid = getattr(msg, "tool_use_id", None) or run.tasks.get(msg.task_id)
                if tid in run.active:
                    run.active.remove(tid)
                    run.background.discard(tid)
                    self._emit(run, "agent_ended", {"agent": run.agents.get(tid), "late": True,
                                                    "status": status})
        elif isinstance(msg, ResultMessage):
            run.turn_ended = True
            if msg.session_id:
                run.session_id = msg.session_id
            run.relay = msg.result or run.last_text
            if msg.is_error:
                run.outcome = "erreur"
                run.error = "; ".join(getattr(msg, "errors", None) or []) or (msg.subtype or "erreur")
            reason = getattr(msg, "terminal_reason", None) or ""
            if reason.startswith("aborted"):
                run.outcome = "interrompu"
        elif isinstance(msg, SystemMessage) and msg.subtype == "session_state_changed":
            run.state = (msg.data or {}).get("state")

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
        # cmd/8_code.md:437-440 — at the feature folder's root, in the main
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
        """`stop1.md` is the disarmed form (cmd/8_code.md:455-457)."""
        path = Runner.stop_file(repo, feature)
        if not os.path.exists(path):
            return None
        target = os.path.join(os.path.dirname(path), "stop1.md")
        if os.path.exists(target):
            os.remove(path)
        else:
            os.replace(path, target)
        return target

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

    def _emit(self, run: Run, kind: str, data: dict):
        ev = {"seq": next(self._seq), "type": kind, "run": run.id, "data": data}
        run.events.append(ev)
        if len(run.events) > MAX_EVENTS:
            del run.events[: len(run.events) - MAX_EVENTS]
        for q in list(run.subscribers):
            q.put_nowait(ev)


def list_worktrees(repo: str) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", repo, "worktree", "list", "--porcelain"],
                             capture_output=True, text=True, timeout=15, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    paths = [l[len("worktree "):].strip() for l in out.splitlines() if l.startswith("worktree ")]
    main = repo_key(repo)
    return [p for p in paths if repo_key(p) != main]


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return str(content or "")


def _summary(tool, inp):
    inp = inp or {}
    for k in ("command", "file_path", "path", "pattern", "description", "url", "skill"):
        v = inp.get(k)
        if isinstance(v, str) and v:
            v = v.replace("\n", " ")
            return v if len(v) <= 160 else v[:160] + "…"
    return ""
