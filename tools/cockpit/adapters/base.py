"""The frame every deploy adapter fits — TECHNICAL_V1 §23 (1.8).

The chain builds any kind of application; what is specific to a platform
lives in one adapter per kind of target, and the page never tests a type's
name: it shows what the adapter says it can do. An adapter says

- what a target of its type holds beyond the frame's three fields (`FIELDS`),
  and checks it (`check`);
- where it can deploy — its destinations, live (`destinations`), each with the
  actions it declares on it, and the panels it shows beside them (`panels`);
- whether a target goes to a destination (`accepts`);
- how to deploy a target on a destination (`deploy_steps`), how to follow its
  log (`journal`), and how to do each action it declared (`act`);
- which lines of a log are a crash (`CRASHES`).

This module also holds what every adapter shares: a live log with its
crashes, and running a shell command with its output followed line by line.
"""
import collections
import os
import re
import signal
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime

# A log keeps this many lines; older ones are dropped, the count goes on.
LOG_MAX = 20000
# A crash keeps at most this many lines under its first.
CRASH_MAX = 120
WINDOWS = os.name == "nt"


def now():
    return datetime.now().isoformat(timespec="milliseconds")


class ActionError(Exception):
    """An action that cannot be done, said in French."""


# ------------------------------------------------------------- the fields

def field_spec(key, label, kind="text", required=False, help="", choices=None, placeholder="", default=None):
    """One field of a target, as the page renders it and the profile checks
    it: `text`, `bool` or `choice` (with `choices`, [value, label] pairs)."""
    return {"key": key, "label": label, "kind": kind, "required": required, "help": help,
            "choices": choices or [], "placeholder": placeholder, "default": default}


def check_fields(fields, target):
    """{key: error} for the adapter's own fields: a required one empty, a
    choice not offered, a type that is not the field's."""
    errors = {}
    for f in fields:
        v = target.get(f["key"], f["default"])
        if f["kind"] == "bool":
            if v is not None and not isinstance(v, bool):
                errors[f["key"]] = "vrai ou faux attendu"
            continue
        if v is None:
            v = ""
        if not isinstance(v, str):
            errors[f["key"]] = "un texte attendu"
            continue
        if f["required"] and not v.strip():
            errors[f["key"]] = "obligatoire"
        elif f["kind"] == "choice" and v not in [c[0] for c in f["choices"]]:
            errors[f["key"]] = "une de ces valeurs : " + ", ".join(c[0] for c in f["choices"])
    return errors


# ---------------------------------------------------------- the actions

def action(id, label, kind="post", args=None, primary=False, confirm=None, fields=None, url=None, title=None):
    """One thing the page offers on a destination or in a panel. `kind` says
    how the page does it, never what it is: `post` sends it to the server
    and shows the answer; `image` shows what the server answers as an image;
    `link` opens `url`; `journal` opens « Journal » on the destination;
    `rename` asks for a name. `fields` turn it into a small form."""
    return {"id": id, "label": label, "kind": kind, "args": args or {}, "primary": primary,
            "confirm": confirm, "fields": fields or [], "url": url, "title": title}


# --------------------------------------------------------------- crashes

@dataclass
class CrashRule:
    """A crash starts on a line `start` matches; the lines right under it
    that `cont` matches belong to it, up to one `end` matches."""
    name: str
    start: str
    cont: str = ""
    end: str = ""

    def __post_init__(self):
        self.re_start = re.compile(self.start)
        self.re_cont = re.compile(self.cont) if self.cont else None
        self.re_end = re.compile(self.end) if self.end else None

    def to_dict(self):
        return {"name": self.name, "start": self.start, "cont": self.cont, "end": self.end}


class LogStream:
    """A live log: its lines, numbered from 1, each with the time it came,
    and its crashes, found by the adapter's rules as the lines come. Thread
    safe: the reader thread writes, the server reads."""

    def __init__(self, rules=(), on_crash=None, maxlen=LOG_MAX):
        self.rules = list(rules)
        self.on_crash = on_crash
        self.lines = collections.deque(maxlen=maxlen)
        self.crashes = []
        self.n = 0
        self.live = False
        self.ended = ""             # why it stopped, when it did
        self._cur = None            # (rule, crash) being read
        self._lock = threading.Lock()

    def continues(self, text):
        """True when `text` would belong to the crash being read — a reader
        that filters lines keeps it."""
        with self._lock:
            return bool(self._cur and self._cur[0].re_cont and self._cur[0].re_cont.search(text))

    def add(self, text, marker=False):
        text = text.rstrip("\r\n")
        started = None
        with self._lock:
            self.n += 1
            n, at, crash = self.n, now(), None
            if not marker:
                crash, started = self._detect(n, at, text)
            self.lines.append({"n": n, "at": at, "text": text, "crash": crash, "marker": marker})
        if started and self.on_crash:
            try:
                self.on_crash(started)
            except Exception:
                pass
        return n

    def _detect(self, n, at, text):
        if self._cur:
            rule, c = self._cur
            if rule.re_cont and rule.re_cont.search(text) and len(c["lines"]) < CRASH_MAX:
                c["lines"].append(text)
                if rule.re_end and rule.re_end.search(text):
                    # A Python traceback says what it is on its last line.
                    c["title"] = text.strip()[:200]
                    self._cur = None
                return c["id"], None
            self._cur = None
        for rule in self.rules:
            m = rule.re_start.search(text)
            if m:
                # Its title: from what the rule found, not the line's prefix.
                c = {"id": len(self.crashes) + 1, "n": n, "at": at, "rule": rule.name,
                     "title": text[m.start():].strip()[:200], "lines": [text]}
                self.crashes.append(c)
                self._cur = (rule, c)
                return c["id"], dict(c)
        return None, None

    def since(self, after=0, limit=3000):
        """The lines numbered above `after`, the last `limit` of them, and
        every crash (each with its lines so far)."""
        with self._lock:
            lines = [x for x in self.lines if x["n"] > after]
            dropped = max(0, len(lines) - limit)
            return {"lines": lines[dropped:], "skipped": dropped, "last": self.n,
                    "crashes": [dict(c, lines=list(c["lines"])) for c in self.crashes],
                    "live": self.live, "ended": self.ended}

    def text(self):
        with self._lock:
            return "\n".join(x["text"] for x in self.lines) + "\n"


# ----------------------------------------------------------- processes

def popen_flags():
    """No window, and a group of its own: a command and what it started
    stop together."""
    if WINDOWS:
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)}
    return {"start_new_session": True}


def kill_tree(proc):
    """Stops a process and every process it started."""
    if proc.poll() is not None:
        return
    try:
        if WINDOWS:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=20,
                           stdin=subprocess.DEVNULL)
        else:
            os.killpg(proc.pid, signal.SIGTERM)
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        proc.wait(10)
    except subprocess.TimeoutExpired:
        proc.kill()


def shell_popen(command, cwd, env=None):
    """A shell command run from `cwd`, its output and its errors as one
    stream, read as UTF-8 — what a command prints otherwise is kept,
    replaced where it is not UTF-8."""
    full = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8", **(env or {}))
    return subprocess.Popen(command, shell=True, cwd=cwd, env=full, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            encoding="utf-8", errors="replace", bufsize=1, **popen_flags())


@dataclass
class Outcome:
    code: int | None
    tail: list = field(default_factory=list)
    timed_out: bool = False


def run_shell(command, cwd, out, env=None, timeout=1800, tail=40):
    """Runs a shell command to its end, each line of its output written to
    `out` as it comes. Its exit code, and its last lines."""
    proc = shell_popen(command, cwd, env)
    last = collections.deque(maxlen=tail)
    expired = threading.Event()

    def expire():
        expired.set()
        kill_tree(proc)
    timer = threading.Timer(timeout, expire)
    timer.daemon = True
    timer.start()
    try:
        for line in proc.stdout:
            line = line.rstrip("\r\n")
            last.append(line)
            out(line)
        proc.wait()
    finally:
        timer.cancel()
    return Outcome(proc.returncode, list(last), expired.is_set())


def run_argv(argv, timeout=15, binary=False):
    """A short program, to its end: (exit code, output). Raises ActionError
    when it cannot start or does not end in time."""
    try:
        p = subprocess.run(argv, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        raise ActionError(f"{os.path.basename(argv[0])} introuvable")
    except subprocess.TimeoutExpired:
        raise ActionError(f"{os.path.basename(argv[-1] if len(argv) < 3 else argv[0])} : délai dépassé ({timeout} s)")
    except OSError as e:
        raise ActionError(f"{os.path.basename(argv[0])} : {e}")
    if binary:
        return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")
    return p.returncode, (p.stdout + b"\n" + p.stderr).decode("utf-8", "replace").strip()


def start_detached(argv):
    """A program that opens its own window — an emulator, a mirror — started
    and left running: the cockpit does not wait for it."""
    try:
        return subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, **popen_flags())
    except OSError as e:
        raise ActionError(f"{os.path.basename(argv[0])} ne démarre pas : {e}")


# -------------------------------------------------------------- the frame

@dataclass
class Step:
    """One step of a deploy on one destination: `kind` is `deploy` or
    `launch`; `run(out)` writes its output through `out`, line by line, and
    returns (ok, what to say, its last lines)."""
    kind: str
    label: str
    run: object


class Adapter:
    """What every adapter declares and does. The values here are the
    frame's defaults; each adapter overrides what it has."""
    TYPE = ""
    LABEL = ""
    FIELDS: list = []
    CRASHES: list = []
    DEPLOY_LABEL = "Installer"

    def __init__(self, hub):
        # hub: what the adapter reaches of the server — `devices`, the names
        # and addresses the Product Owner gave, kept in config.json; `crash`,
        # what it calls when a log shows one (deploy.Hub).
        self.hub = hub
        self.store = hub.devices

    def describe(self):
        """What the page and the profile read of this adapter."""
        return {"type": self.TYPE, "label": self.LABEL, "fields": self.FIELDS,
                "crashes": [r.to_dict() for r in self.CRASHES], "deploy_label": self.DEPLOY_LABEL}

    def check(self, target):
        return check_fields(self.FIELDS, target)

    def destinations(self, targets, app):
        """[{id, name, kind, state, connected, facts, note, actions}] — the
        targets are the profile's of this type, `app` the application's
        folder."""
        return []

    def panels(self, targets, app):
        """What the page shows beside the destinations: [{id, title, text,
        items, forms}]."""
        return []

    def accepts(self, target, dest):
        return True

    def deploy_steps(self, target, dest, app):
        return []

    def journal(self, target, dest, app):
        """What follows the target's log on the destination: an object with
        `stream` (a LogStream) and `stop()`. Raises ActionError."""
        return None

    def act(self, action_id, dest_id, args, app, targets):
        """Does an action this adapter declared: {"message": …} or raises
        ActionError."""
        raise ActionError(f"action inconnue : {action_id}")

    def image(self, action_id, dest_id, args):
        """An action of kind `image`: PNG bytes."""
        raise ActionError(f"action inconnue : {action_id}")

    def stop_all(self):
        """The server stops: what the adapter started that follows it."""
