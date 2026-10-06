"""How the cockpit starts and stops — cockpit 1.5, TECHNICAL_V1 §16.

- The server runs without a console window (`pythonw`): closing that window
  by mistake killed a run. What it printed goes to `logs/server.log`.
- Started again while it answers on its port, it opens the browser on it
  and exits: the desktop shortcut always works, and never starts a second
  server.
- Without a console of its own, every program it starts — the Claude Code
  CLI, git, the diagnostic's version commands — is started with no window
  either; a console program started from a windowless one would otherwise
  open its own, and closing it would kill the run.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

LOG_NAME = "server.log"
LOG_MAX = 5 * 1024 * 1024        # past this, the log is kept once as server.log.1
PING_TIMEOUT = 1.5


class Tee:
    """Writes to the log file, and to the console when there is one."""

    def __init__(self, *streams):
        self.streams = [s for s in streams if s is not None]

    def write(self, text):
        for s in self.streams:
            try:
                s.write(text)
                s.flush()
            except (OSError, ValueError):
                pass
        return len(text)

    def flush(self):
        for s in self.streams:
            try:
                s.flush()
            except (OSError, ValueError):
                pass

    def isatty(self):
        return False


def open_log(path):
    """`server.log`, appended to; rotated once past LOG_MAX. stdout and
    stderr go there — and still to the console when one exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        if os.path.getsize(path) > LOG_MAX:
            os.replace(path, path + ".1")
    except OSError:
        pass
    f = open(path, "a", encoding="utf-8", buffering=1)
    sys.stdout = Tee(f, sys.__stdout__ if sys.__stdout__ is not None else None)
    sys.stderr = Tee(f, sys.__stderr__ if sys.__stderr__ is not None else None)
    return f


def windowless():
    """True when the process has no console: started by `pythonw`."""
    return sys.__stdout__ is None or os.path.basename(sys.executable).lower().startswith("pythonw")


def hide_child_consoles():
    """Every subprocess started from now on gets CREATE_NO_WINDOW unless it
    asks for its own flags: a console program started from a windowless
    process would open a window of its own. Windows only; idempotent."""
    if os.name != "nt" or getattr(subprocess.Popen, "_cockpit_quiet", False):
        return False
    flag = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    original = subprocess.Popen.__init__

    def __init__(self, *args, **kwargs):
        if not kwargs.get("creationflags"):
            kwargs["creationflags"] = flag
        original(self, *args, **kwargs)

    subprocess.Popen.__init__ = __init__
    subprocess.Popen._cockpit_quiet = True
    return True


def ping(port, host="127.0.0.1", timeout=PING_TIMEOUT):
    """The cockpit answering on this port: its `/api/ping`, or None — for
    nothing there, or something that is not the cockpit."""
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/api/ping", timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("cockpit") else None


def error_box(text, title="Cockpit"):
    """A message box when there is no console to read the error in."""
    if os.name != "nt" or not windowless():
        return
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, text, title, 0x10)
    except Exception:
        pass
