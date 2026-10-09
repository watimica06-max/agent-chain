"""« Mettre à jour le cockpit » — cockpit 1.14.

agent-chain's clone is what the cockpit runs from and what it installs in the
applications. The Product Owner works from two computers: when the cockpit
or the chain changes, each one takes the new version from the page, without
a terminal.

What the cockpit runs is the code of the commit its server started from
(`started`). It is behind when agent-chain's clone is behind GitHub
(« disponible »), or when the clone moved on since the server started — the
pull at start, 1.12 (« récupérée »). The update:

1. refused while a run goes — or an install, a deploy build, a creation;
2. `git pull --ff-only` in agent-chain (sync.py, every git call as 1.12 set
   them); refused with the file named when git would overwrite an
   uncommitted one; « divergé » refused, « Réconcilier » offered;
3. `python -m pip install --user -r tools/cockpit/requirements.txt` when that
   file changed between `started` and the new `HEAD`; stopped on its error;
4. the restart. A new server is started the way lancer.bat starts one
   (`pythonw server.py`, else `python server.py`), detached, with
   `--relais <trial port>`: it serves on that free trial port first. The old
   server waits until the new one answers there — its `/api/ping`, another
   pid — at most RESTART_WAIT seconds. No answer: the new process is ended,
   the old one keeps running, and says why (its exit code, the end of what
   it wrote). An answer: the old server exits; the new one takes the
   cockpit's port as soon as it is free, and closes the trial port. The page
   polls `/api/ping` and reloads once another pid answers.
"""
import os
import shutil
import socket
import subprocess
import sys
import time

import startup
import sync

HERE = os.path.dirname(os.path.abspath(__file__))
# The cockpit's requirements, in agent-chain's clone.
REQUIREMENTS = "tools/cockpit/requirements.txt"
SERVER = os.path.join(HERE, "server.py")
# What a new server writes to stderr: relais-<trial port>.log — its own
# file, the one it keeps for as long as it runs.
RESTART_LOG = "relais-{}.log"

PIP_TIMEOUT = 900
RESTART_WAIT = 60.0          # what the new server is given to answer on its trial port
TAKEOVER_WAIT = 30.0         # what it is given to take the cockpit's port once the old one exits
POLL = 0.25
SUBJECTS_MAX = 30

# The pip command, before its arguments; None: this Python's, as below. The
# tests put a fake here.
PIP_COMMAND = None

UP_TO_DATE, AVAILABLE, PULLED = "à jour", "disponible", "récupérée"


# ------------------------------------------------------------ the state

def _short(sha):
    return (sha or "")[:7]


def subjects(root, rng):
    """`git log` over a range, newest first, as « <id> <subject> »."""
    r = sync.git(root, "log", f"--max-count={SUBJECTS_MAX}", "--format=%h %s", rng)
    return [x for x in r.out.splitlines() if x.strip()] if r.ok else []


def status(root, started, st, head):
    """Where the running cockpit stands against agent-chain's clone and
    GitHub: `state` — « à jour », « disponible » (GitHub has commits the
    clone lacks), « récupérée » (the clone has commits the running server
    does not run) —, and the commits' subjects the cockpit does not run."""
    st = st or {}
    behind = st.get("state") == sync.BEHIND or (st.get("state") == sync.DIVERGED and st.get("behind"))
    pending = bool(started and head and started != head)
    out = {"state": UP_TO_DATE, "started": _short(started), "head": _short(head), "subjects": [],
           "count": 0, "sync": st.get("state"), "diverged": st.get("state") == sync.DIVERGED,
           "summary": st.get("summary") or ""}
    if st.get("state") == sync.DIVERGED:
        out["state"] = AVAILABLE
        out["subjects"] = subjects(root, f"HEAD..{st['upstream']}") if st.get("upstream") else []
    elif behind and st.get("upstream"):
        out["state"] = AVAILABLE
        out["subjects"] = subjects(root, f"{started or 'HEAD'}..{st['upstream']}")
    elif pending:
        out["state"] = PULLED
        out["subjects"] = subjects(root, f"{started}..{head}")
    out["count"] = len(out["subjects"])
    return out


# ------------------------------------------------------------ pip

def requirements_changed(root, base, head):
    """True when tools/cockpit/requirements.txt differs between the two
    commits."""
    if not base or not head or base == head:
        return False
    r = sync.git(root, "diff", "--name-only", base, head, "--", REQUIREMENTS)
    return bool(r.ok and r.out.strip())


def python_console():
    """`python`, beside the `pythonw` the cockpit may run under."""
    exe = sys.executable or "python"
    d, b = os.path.split(exe)
    if b.lower().startswith("pythonw"):
        cand = os.path.join(d, "python" + b[len("pythonw"):])
        if os.path.isfile(cand):
            return cand
    return exe


def pip_install(root):
    """`python -m pip install --user -r tools/cockpit/requirements.txt`, in
    agent-chain's clone: {"ok", "command", "message"} — the message, the end
    of what pip said when it failed."""
    path = os.path.join(root, *REQUIREMENTS.split("/"))
    cmd = list(PIP_COMMAND) if PIP_COMMAND else [python_console(), "-m", "pip"]
    cmd += ["install", "--user", "-r", path]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=PIP_TIMEOUT, stdin=subprocess.DEVNULL,
                           cwd=os.path.dirname(path))
    except subprocess.TimeoutExpired:
        return {"ok": False, "command": cmd, "message": f"pip : pas de fin en {PIP_TIMEOUT} s"}
    except OSError as e:
        return {"ok": False, "command": cmd, "message": f"pip : {e}"}
    if p.returncode:
        text = (p.stderr.decode("utf-8", "replace") + "\n" + p.stdout.decode("utf-8", "replace")).strip()
        tail = "\n".join(text.splitlines()[-8:])
        return {"ok": False, "command": cmd, "message": f"pip a échoué (code {p.returncode}) : {tail}"}
    return {"ok": True, "command": cmd, "message": ""}


# ------------------------------------------------------------ the restart

def free_port(host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]


def server_command(port, trial, extra=()):
    """The new server, as lancer.bat starts it: `pythonw server.py`, else
    `python server.py` — never `--ouvrir`: the page reloads on its own."""
    exe = shutil.which("pythonw")
    if not exe:
        d, b = os.path.split(sys.executable or "")
        cand = os.path.join(d, "pythonw.exe") if d else ""
        exe = cand if cand and os.path.isfile(cand) else None
    console = exe is None
    exe = exe or python_console()
    return [exe, SERVER, "--port", str(port), "--relais", str(trial), *extra], console


def _sweep_logs(log_dir):
    """The earlier restarts' logs, each but the one a running server still
    holds open — Windows refuses to delete that one."""
    try:
        names = os.listdir(log_dir)
    except OSError:
        return
    for n in names:
        if n.startswith("relais-") and n.endswith(".log"):
            try:
                os.remove(os.path.join(log_dir, n))
            except OSError:
                pass


def spawn(port, trial, extra=(), log_dir=None):
    """Starts the new server, detached: it outlives the old one. What it
    writes to stderr goes to <logs>/relais-<trial>.log — what is said when
    it does not answer. Returns the process."""
    cmd, console = server_command(port, trial, extra)
    log_dir = log_dir or os.path.join(HERE, "logs")
    os.makedirs(log_dir, exist_ok=True)
    _sweep_logs(log_dir)
    err = open(os.path.join(log_dir, RESTART_LOG.format(trial)), "wb")
    flags = 0
    if os.name == "nt":
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | (subprocess.CREATE_NEW_CONSOLE if console
                                                       else subprocess.DETACHED_PROCESS)
    try:
        return subprocess.Popen(cmd, cwd=HERE, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=err,
                                creationflags=flags, close_fds=True,
                                **({} if os.name == "nt" else {"start_new_session": True}))
    finally:
        err.close()


def wait_answer(proc, trial, me, timeout=None):
    """Polls the trial port until a cockpit other than `me` answers there:
    its ping, or None — when the process ended, or after `timeout`."""
    deadline = time.monotonic() + (RESTART_WAIT if timeout is None else timeout)
    while time.monotonic() < deadline:
        got = startup.ping(trial, timeout=1.0)
        if got and got.get("pid") != me:
            return got
        if proc is not None and proc.poll() is not None:
            # Ended: one last look, in case it answered just before.
            got = startup.ping(trial, timeout=1.0)
            return got if got and got.get("pid") != me else None
        time.sleep(POLL)
    return None


def log_tail(log_dir, trial, lines=8):
    try:
        with open(os.path.join(log_dir or os.path.join(HERE, "logs"), RESTART_LOG.format(trial)), "rb") as f:
            text = f.read().decode("utf-8", "replace").strip()
    except OSError:
        return ""
    return "\n".join(text.splitlines()[-lines:])


def give_up(proc):
    """The new server did not answer: ended, never left behind."""
    if proc is None or proc.poll() is not None:
        return
    try:
        proc.kill()
        proc.wait(5)
    except (OSError, subprocess.SubprocessError):
        pass


def why_not(proc, waited, log_dir, trial):
    code = proc.poll() if proc is not None else None
    said = log_tail(log_dir, trial)
    return (f"Le nouveau serveur du cockpit n'a pas répondu en {int(waited)} s"
            + (f" (il s'est arrêté, code {code})" if code is not None else " (arrêté)")
            + " : le cockpit continue sur l'ancienne version."
            + (f" Ce qu'il a écrit : {said}" if said else ""))
