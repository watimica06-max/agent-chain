"""The environment diagnostic — read-only. Runs a few version commands from
the application folder, with the server's own environment (the one every
run inherits). Runs no chain command.

Each check ends as `ok` (the first line of output), `fail` (the error) or
`skip` (« non concerné »: its file is absent).
"""
import os
import shutil
import subprocess
from datetime import datetime

DEFAULT_TIMEOUT = 30
GRADLE_TIMEOUT = 120      # the first call may download Gradle

JAVA_HINT = ("Java ne se lance pas alors que Gradle est présent : JAVA_HOME doit être défini dans "
             "les variables d'environnement de Windows, en général sur "
             "C:\\Program Files\\Android\\Android Studio\\jbr. Redémarrez ensuite le cockpit.")


def system_exec(argv, cwd, timeout):
    """Run one command: (returncode, output). Raises FileNotFoundError when
    the program cannot be found, subprocess.TimeoutExpired on a timeout."""
    exe = shutil.which(argv[0], path=None) if not os.path.isabs(argv[0]) else argv[0]
    if exe is None or (os.path.isabs(argv[0]) and not os.path.exists(argv[0])):
        raise FileNotFoundError(f"{argv[0]} introuvable (PATH)")
    p = subprocess.run([exe, *argv[1:]], cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout, stdin=subprocess.DEVNULL)
    return p.returncode, (p.stdout or "") + "\n" + (p.stderr or "")


def gradle_wrapper(app):
    for name in ("gradlew.bat", "gradlew"):
        p = os.path.join(app, name)
        if os.path.isfile(p):
            return p
    return None


def plan(app):
    """The checks for this folder: (id, label, argv or None, timeout)."""
    wrapper = gradle_wrapper(app)
    has_pubspec = os.path.isfile(os.path.join(app, "pubspec.yaml"))
    return [
        ("java", "Java", ["java", "-version"], DEFAULT_TIMEOUT),
        ("gradle", "Gradle", [wrapper, "--version"] if wrapper else None, GRADLE_TIMEOUT),
        ("flutter", "Flutter", ["flutter", "--version"] if has_pubspec else None, DEFAULT_TIMEOUT),
        ("adb", "adb", ["adb", "version"], DEFAULT_TIMEOUT),
        ("claude", "Claude Code", ["claude", "--version"], DEFAULT_TIMEOUT),
        ("git", "Git", ["git", "--version"], DEFAULT_TIMEOUT),
    ]


def first_line(text):
    for line in (text or "").splitlines():
        if line.strip():
            return line.strip()
    return ""


def run_diagnostic(app, exec_fn=system_exec, now=None):
    results = []
    for cid, label, argv, timeout in plan(app):
        if argv is None:
            results.append({"id": cid, "label": label, "status": "skip", "detail": "non concerné"})
            continue
        try:
            code, out = exec_fn(argv, app, timeout)
        except FileNotFoundError as e:
            results.append({"id": cid, "label": label, "status": "fail", "detail": str(e)})
        except subprocess.TimeoutExpired:
            results.append({"id": cid, "label": label, "status": "fail",
                            "detail": f"délai dépassé ({timeout} s)"})
        except OSError as e:
            results.append({"id": cid, "label": label, "status": "fail", "detail": f"{type(e).__name__}: {e}"})
        else:
            line = first_line(out)
            if code == 0:
                results.append({"id": cid, "label": label, "status": "ok", "detail": line})
            else:
                results.append({"id": cid, "label": label, "status": "fail",
                                "detail": f"code {code}" + (f" — {line}" if line else "")})
    by = {r["id"]: r for r in results}
    hints = []
    if by["java"]["status"] == "fail" and by["gradle"]["status"] != "skip":
        hints.append(JAVA_HINT)
    return {"at": (now or datetime.now()).isoformat(timespec="seconds"), "app": app,
            "results": results, "hints": hints,
            "ok": all(r["status"] != "fail" for r in results)}
