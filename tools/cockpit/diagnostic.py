"""The environment diagnostic — read-only. Runs a few version commands from
the application folder, with the server's own environment (the one every
run inherits). Runs no chain command.

Each check ends as `ok` (the first line of output), `fail` (the error) or
`skip` (« non concerné »: its file is absent).

1.8 — `optional`: scrcpy and the Android emulator, which « Déploiement »
uses when they are here. Each is `ok` or `absent` (« non trouvé »), never a
failure: neither is needed, and neither makes an alert.
"""
import os
import re
import shutil
import subprocess
from datetime import datetime

DEFAULT_TIMEOUT = 30
GRADLE_TIMEOUT = 120      # the first call may download Gradle

JAVA_HINT = ("Java ne se lance pas alors que Gradle est présent : JAVA_HOME doit être défini dans "
             "les variables d'environnement de Windows, en général sur "
             "C:\\Program Files\\Android\\Android Studio\\jbr. Redémarrez ensuite le cockpit.")
JAVA_HOME_EMPTY = ("JAVA_HOME pointe vers {path}, où il n'y a pas de java : Gradle n'y trouve pas de Java. "
                   "Corrigez JAVA_HOME dans les variables d'environnement de Windows, en général sur "
                   "C:\\Program Files\\Android\\Android Studio\\jbr. Redémarrez ensuite le cockpit.")


def java_of(env=None):
    """The Java the builds use (1.5): Gradle runs `%JAVA_HOME%\\bin\\java`
    when JAVA_HOME is set, the `java` of the PATH otherwise.
    (argv, where, java_home, java_home_points_to_nothing)."""
    env = os.environ if env is None else env
    home = (env.get("JAVA_HOME") or "").strip().strip('"')
    if not home:
        return ["java", "-version"], "PATH", None, False
    exe = os.path.join(home, "bin", "java.exe" if os.name == "nt" else "java")
    return [exe, "-version"], "JAVA_HOME", home, not os.path.isfile(exe)


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


def _found(find, tool):
    """Where `find` says the tool is — None when it cannot say."""
    try:
        return find(tool)
    except Exception:
        return None


def plan(app, env=None, find=None):
    """The checks for this folder: (id, label, argv or None, timeout)."""
    wrapper = gradle_wrapper(app)
    has_pubspec = os.path.isfile(os.path.join(app, "pubspec.yaml"))
    java, where, _, _ = java_of(env)
    return [
        ("java", f"Java ({where})", java, DEFAULT_TIMEOUT),
        ("gradle", "Gradle", [wrapper, "--version"] if wrapper else None, GRADLE_TIMEOUT),
        ("flutter", "Flutter", ["flutter", "--version"] if has_pubspec else None, DEFAULT_TIMEOUT),
        # 1.16: adb where the deploy adapter finds it — the PATH, else the SDK's
        # platform-tools —, as the emulator below; « adb » on the PATH when
        # neither has it, which then says « introuvable ».
        ("adb", "adb", [*(_found(find or FIND, "adb") or ["adb"]), "version"], DEFAULT_TIMEOUT),
        ("claude", "Claude Code", ["claude", "--version"], DEFAULT_TIMEOUT),
        ("git", "Git", ["git", "--version"], DEFAULT_TIMEOUT),
    ]


# The optional tools (1.8): (id, label, the flag that prints its version).
OPTIONAL = [("scrcpy", "scrcpy — afficher l'écran d'un appareil", "--version"),
            ("emulator", "Émulateur Android", "-version")]


def find_tool(tool):
    """Where a tool is — the deploy adapter's own lookup — or None: scrcpy,
    the emulator, and 1.16 adb."""
    from adapters import android
    return {"scrcpy": android.scrcpy_argv, "adb": android.adb_argv}.get(tool, android.emulator_argv)()


# What finds them; the tests put a fake here.
FIND = find_tool


def optional_checks(app, exec_fn, find):
    out = []
    for tid, label, flag in OPTIONAL:
        argv = find(tid)
        if not argv:
            out.append({"id": tid, "label": label, "status": "absent", "detail": "non trouvé — facultatif"})
            continue
        try:
            code, text = exec_fn([*argv, flag], app, DEFAULT_TIMEOUT)
        except (OSError, subprocess.TimeoutExpired) as e:
            out.append({"id": tid, "label": label, "status": "absent",
                        "detail": f"trouvé ({argv[0]}), sans réponse : {e}"})
            continue
        line = first_line(text)
        if code == 0:
            out.append({"id": tid, "label": label, "status": "ok", "detail": f"{line} — {argv[0]}"})
        else:
            out.append({"id": tid, "label": label, "status": "absent",
                        "detail": f"trouvé ({argv[0]}), sans réponse : code {code}"})
    return out


def first_line(text):
    """The first line that says something: `gradlew --version` opens on a
    rule of dashes (1.4.5)."""
    for line in (text or "").splitlines():
        if line.strip() and not re.fullmatch(r"[-=_*\s]+", line):
            return line.strip()
    return ""


def run_diagnostic(app, exec_fn=system_exec, now=None, env=None, find=None):
    results = []
    _, where, home, nothing = java_of(env)
    for cid, label, argv, timeout in plan(app, env, find):
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
    if where == "JAVA_HOME":
        by["java"]["detail"] += f" — JAVA_HOME : {home}"
    hints = []
    # The JAVA_HOME hint only when JAVA_HOME is not set, or points to nothing:
    # set and pointing to a Java that fails, setting it is not the answer.
    if by["java"]["status"] == "fail" and by["gradle"]["status"] != "skip":
        if where == "PATH":
            hints.append(JAVA_HINT)
        elif nothing:
            hints.append(JAVA_HOME_EMPTY.format(path=home))
    return {"at": (now or datetime.now()).isoformat(timespec="seconds"), "app": app,
            "results": results, "hints": hints,
            "optional": optional_checks(app, exec_fn, find or FIND),
            "ok": all(r["status"] != "fail" for r in results)}
