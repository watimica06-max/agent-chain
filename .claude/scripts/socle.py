#!/usr/bin/env python3
"""The scaffolding a brand-new application needs before the chain runs.

    python .claude/scripts/socle.py            # writes, commits, reports
    python .claude/scripts/socle.py --list     # the report alone, nothing written

The application is the folder holding the `.claude/` this script ships
in. It must be the root of a git repository — the chain's install, which
brings this script, made its first commit there.

It writes what the chain reads and nothing else:
- `docs/PRODUIT_GLOBAL.md`, `# Application` its only line — the
  Rédacteur, the sondeur at invocation 3 and the Fusionneur read it;
- `docs/features/`, empty — every command works under it;
- `docs/CURRENT_TECHNICAL_STATE.md`, `# Technical state` its only line —
  the Détailleur, the Réalisateur, the Arbitre and the Diagnostiqueur
  read it, the Réalisateur and the Arbitre write in it;
- in `.gitignore`, the lines below, appended when absent: `stop.md` and
  `stop1.md` are the Product Owner's halt and its disarmed form, never
  committed though the commands `git add` the feature folder; the
  worktrees and the local settings are the session's own.

It refuses when `docs/PRODUIT_GLOBAL.md` exists: overwriting the global
would lose every domain in it. Then it commits those files alone —
`chore: scaffolding for the chain` — and does not push: the cockpit
does, and says when it fails.

Last, it prints what the application still has to provide, one line
each: `PROVIDE`, read by the cockpit too. Neither blocks the upstream
chain; both are needed from `/7_lots` onward.

Exit code 0 when done, 2 when it refuses, 1 when git fails.
"""
import os
import subprocess
import sys

# The application: the folder holding the .claude/ this script ships in.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GLOBAL = "docs/PRODUIT_GLOBAL.md"
FEATURES = "docs/features"
STATE = "docs/CURRENT_TECHNICAL_STATE.md"
FILES = {GLOBAL: "# Application\n", STATE: "# Technical state\n"}
IGNORE = ("docs/features/*/stop.md", "docs/features/*/stop1.md",
          ".claude/worktrees/", ".claude/settings.local.json")
MESSAGE = "chore: scaffolding for the chain"

# What the application provides itself: (the path that says it is there,
# what it is and who writes it).
PROVIDE = (
    ("docs/TECHNICAL_CONVENTIONS.md",
     "les conventions techniques — écrites par /conventions, jamais à la main ; "
     "/conventions se lance après /6_convertit, avant /7_lots"),
    (".claude/skills/technical-state-format/SKILL.md",
     "la compétence technical-state-format — le Réalisateur et l'Arbitre la chargent "
     "avant d'écrire dans docs/CURRENT_TECHNICAL_STATE.md"),
)


class Refused(Exception):
    pass


def _path(root, rel):
    return os.path.join(root, *rel.split("/"))


def _git(root, *args):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True, stdin=subprocess.DEVNULL,
                       env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    if p.returncode:
        msg = (p.stderr or p.stdout).decode("utf-8", "replace").strip()
        raise RuntimeError(f"git {args[0]} : {msg}")
    return p.stdout.decode("utf-8", "replace")


def missing(root=ROOT):
    """The lines of PROVIDE the application does not have yet."""
    return [(rel, text) for rel, text in PROVIDE if not os.path.exists(_path(root, rel))]


def _ignore_text(root):
    p = _path(root, ".gitignore")
    if not os.path.exists(p):
        return None, b""
    with open(p, "rb") as f:
        return p, f.read()


def scaffold(root=ROOT):
    """Writes the scaffolding and commits it. Returns the paths written.
    Raises Refused when the global exists, RuntimeError when git fails."""
    if os.path.exists(_path(root, GLOBAL)):
        raise Refused(f"{GLOBAL} existe déjà : ce script est pour une application neuve, "
                      "et réécrire le global perdrait chaque domaine qu'il porte")
    top = _git(root, "rev-parse", "--show-toplevel").strip()
    if os.path.normcase(os.path.abspath(top)) != os.path.normcase(os.path.abspath(root)):
        raise Refused(f"{root} n'est pas la racine de son dépôt git ({top})")
    # Who commits, asked before anything is written: a commit that fails
    # would leave the global written, and the next run refused.
    _git(root, "var", "GIT_COMMITTER_IDENT")
    written = []
    for rel, text in FILES.items():
        # A technical state already there, with no global, is kept as it is.
        if os.path.exists(_path(root, rel)):
            continue
        os.makedirs(os.path.dirname(_path(root, rel)), exist_ok=True)
        with open(_path(root, rel), "x", encoding="utf-8", newline="\n") as f:
            f.write(text)
        written.append(rel)
    os.makedirs(_path(root, FEATURES), exist_ok=True)
    # .gitignore: the lines absent are appended, the file is never rewritten.
    p, old = _ignore_text(root)
    have = {l.strip() for l in old.decode("utf-8", "replace").splitlines()}
    add = [l for l in IGNORE if l not in have]
    if add:
        nl = b"\r\n" if b"\r\n" in old else b"\n"
        sep = b"" if not old or old.endswith(b"\n") else nl
        with open(p or _path(root, ".gitignore"), "ab") as f:
            f.write(sep + nl.join(l.encode() for l in add) + nl)
        written.append(".gitignore")
    _git(root, "add", "--", *written)
    _git(root, "commit", "-q", "-m", MESSAGE, "--only", "--", *written)
    return written


def report(root=ROOT):
    lines = missing(root)
    for rel, text in lines:
        print(f"À fournir : {rel} — {text}")
    return lines


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if argv == ["--list"]:
        report()
        return 0
    if argv:
        print("usage : python .claude/scripts/socle.py [--list]", file=sys.stderr)
        return 1
    try:
        written = scaffold()
    except Refused as e:
        print(f"Refusé : {e}", file=sys.stderr)
        return 2
    except (RuntimeError, OSError) as e:
        print(f"Échec : {e}", file=sys.stderr)
        return 1
    print(f"Commité « {MESSAGE} » : " + ", ".join(written + [FEATURES + "/"]))
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
