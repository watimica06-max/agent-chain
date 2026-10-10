"""1.20 — a feature's life in git, for the Journal's page tests and its
screenshots: the fake application of fakeapp.FakeServer made a repository,
with dated commits — questions created and answered, blocking files settled
by the Arbitre and by the Product Owner, one still waiting — and the journal
lines of the runs the cockpit made. No chain command runs."""
import journal
from test_chain import git
from test_journal import BLOCKED, QFILE, at

F = "docs/features/f"


def lines():
    def e(at_, cmd, dur, read, wrote, five, week, outcome, nxt, created=(), prog=None, note=None, pc="PC-SALON"):
        return {"at": at_, "computer": pc, "command": cmd, "duration_s": dur, "read_tokens": read,
                "output_tokens": wrote, "five_hour": five, "seven_day": week, "outcome": outcome, "next": nxt,
                "created": list(created), "programme": prog, "note": note}
    return [
        e("2026-10-06T09:00", "/1_lexique f", 534, 1505185, 61789, 3.0, 1.0, journal.QUESTIONS,
          "répondre → /1_lexique", ["questions-lexicographe-01.md"]),
        e("2026-10-06T14:10", "/1_lexique f", 312, 905000, 30120, 2.0, 0.6, journal.DONE, "/2_structure"),
        e("2026-10-07T09:00", "/2_structure f", 1210, 3101000, 90500, 4.0, 1.2, journal.DONE, "/3_decoupe",
          pc="PC-BUREAU"),
        e("2026-10-08T01:05", "/8_code f", 2700, 8800000, 210000, 14.0, 4.0, journal.BLOCKING,
          "répondre → /8_code", ["code/lot-02/blocked_realisateur.md"], prog="Cette nuit, 1 h – 7 h"),
        e("2026-10-08T02:00", "/8_code f", 60, None, None, None, None, journal.NOT_LOGGED, "inconnu",
          prog="Cette nuit, 1 h – 7 h", note="erreur : Claude Code n'est pas connecté sur cet ordinateur"),
        e("2026-10-08T15:00", "/8_code f", 2400, 7000000, 180000, 6.0, 2.0, journal.DONE, "/8_code (3/5 lots)"),
        e("2026-10-08T16:30", "/8_code f", 2300, 7100000, 170000, 6.0, 2.0, journal.DONE, "/8_code (3/5 lots)",
          note=journal.OVERRIDE_NOTE),
        e("2026-10-08T18:00", "/8_code f", 2350, 7050000, 175000, 6.0, 2.0, journal.BLOCKING, "/8_code (3/5 lots)",
          ["code/blocked_detailleur.md"]),
    ]


def make(app_root):
    """The application folder becomes a repository with a dated story, and
    its journal. Returns the journal's path."""
    r = app_root
    git(r, "init", "-q", "-b", "master")
    git(r, "config", "user.email", "t@example.com")
    git(r, "config", "user.name", "T")
    git(r, "config", "core.autocrlf", "false")
    # The fake application's own open files are not this story's.
    feat = r / "docs" / "features" / "f"
    for rel in ("questions-sondeur-02.md", "convertisseur/technique-model.md", "blocked_qualifieur.md",
                "code/blocked_detailleur.md", "questions-architecte-01.md"):
        p = feat / rel
        if p.exists():
            p.unlink()
    (feat / "bugfix-01").rmdir() if (feat / "bugfix-01").is_dir() and not any((feat / "bugfix-01").iterdir()) else None
    at(r, "2026-10-05T18:00:00", "chore: scaffolding for the chain", [(".gitkeep", "")])
    at(r, "2026-10-06T09:08:00", "feat: f lexicon sweep 1",
       [(f"{F}/questions-lexicographe-01.md", QFILE.format(a1="", a2=""))])
    at(r, "2026-10-06T13:45:00", "chore: answers",
       [(f"{F}/questions-lexicographe-01.md", QFILE.format(a1=" Oui", a2=" Non"))])
    at(r, "2026-10-08T01:30:00", "feat: f lot-01 coded",
       [(f"{F}/code/lot-01/blocked_realisateur.md", BLOCKED.format(d="1. km — d'après la fiche"))])
    at(r, "2026-10-08T01:40:00", "feat: f lot-01 applied",
       moves=[(f"{F}/code/lot-01/blocked_realisateur.md", f"{F}/code/lot-01/blocked_realisateur-01.md")])
    at(r, "2026-10-08T01:50:00", "feat: f lot-02 stopped",
       [(f"{F}/code/lot-02/blocked_realisateur.md", BLOCKED.format(d=""))])
    at(r, "2026-10-08T14:20:00", "chore: pre-code",
       [(f"{F}/code/lot-02/blocked_realisateur.md", BLOCKED.format(d="1. m"))])
    at(r, "2026-10-08T15:20:00", "feat: f lot-02 applied",
       moves=[(f"{F}/code/lot-02/blocked_realisateur.md", f"{F}/code/lot-02/blocked_realisateur-01.md")])
    at(r, "2026-10-08T18:30:00", "feat: f lot-03 stopped",
       [(f"{F}/code/blocked_detailleur.md", BLOCKED.format(d=""))])
    path = journal.journal_path(str(r), "f")
    journal.rewrite(path, lines(), "f")
    at(r, "2026-10-08T18:40:00", "journal: lignes", [])
    return path
