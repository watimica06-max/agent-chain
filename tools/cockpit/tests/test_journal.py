"""1.20 — the cycle journal, its own module: the line's format, written and
read back; each outcome; the files a run created; the questions and the
blocking files timed from a fixture history, and « by whom »; the points à
creuser, raised and not raised under their thresholds; the reconstruction
from the stats, the logs and git, and from git alone; the report. No chain
command runs: the history is made with git in a temporary folder."""
import os
import sqlite3
from datetime import datetime

import pytest

import journal
import stats as stats_mod
from test_chain import commit, git, init, write

F = "docs/features/f"
QFILE = ("### Q1\nTerms: séance\nQuestion: Une séance ?\nOptions:\n- Oui\n- Non\nAnswer:{a1}\n\n"
         "### Q2\nTerms: tour\nQuestion: Un tour ?\nOptions:\n- Oui\n- Non\nAnswer:{a2}\n")
BLOCKED = ("# Blocking — lot-01\n\n## What blocks\nLa fiche ne dit pas l'unité.\n\n## Where\ncode/lot-01\n\n"
           "## To resume\nDire l'unité.\n\nOptions:\n- km\n- m\n\n## Decision\n{d}\n")


def at(repo, when, msg, files=(), moves=(), deletes=()):
    """One commit at a given author and committer date."""
    for rel, text in files:
        write(repo, rel, text)
    for old, new in moves:
        (repo / new).parent.mkdir(parents=True, exist_ok=True)
        git(repo, "mv", old, new)
    for rel in deletes:
        git(repo, "rm", "-q", rel)
    git(repo, "add", "-A")
    env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    import subprocess
    p = subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg], capture_output=True, text=True, env=env)
    assert p.returncode == 0, p.stderr
    return git(repo, "rev-parse", "HEAD").strip()


def merge(repo, when, msg, side):
    import subprocess
    env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    p = subprocess.run(["git", "-C", str(repo), "merge", "--no-ff", "-q", "-m", msg, side], capture_output=True,
                       text=True, env=env)
    assert p.returncode == 0, p.stderr


def history_repo(tmp_path):
    """A feature's life: a questions file created by a run, answered two
    hours later; a blocking file the Arbitre settles inside a run; one she
    settles (« chore: answers »); a third renamed by the command with its
    decision written in a commit nobody can be told from."""
    r = tmp_path / "app"
    init(r)
    at(r, "2026-10-01T09:00:00+02:00", "first", [(f"{F}/idees.md", "# Idées\n")])
    at(r, "2026-10-01T10:00:00+02:00", "feat: f lexicon sweep 1",
       [(f"{F}/questions-lexicographe-01.md", QFILE.format(a1="", a2=""))])
    at(r, "2026-10-01T11:00:00+02:00", "chore: answers",
       [(f"{F}/questions-lexicographe-01.md", QFILE.format(a1=" Oui", a2=""))])
    at(r, "2026-10-01T12:00:00+02:00", "chore: answers",
       [(f"{F}/questions-lexicographe-01.md", QFILE.format(a1=" Oui", a2=" Non"))])
    at(r, "2026-10-01T12:05:00+02:00", "feat: f lexicon settling 1",
       moves=[(f"{F}/questions-lexicographe-01.md", f"{F}/questions/lexicographe/questions-lexicographe-01.md")])
    # The Arbitre: created and decided inside one run, renamed by the command.
    at(r, "2026-10-02T09:00:00+02:00", "feat: f lot-01 coded",
       [(f"{F}/code/lot-01/blocked_realisateur.md", BLOCKED.format(d="1. km — d'après la fiche"))])
    at(r, "2026-10-02T09:10:00+02:00", "feat: f lot-01 applied",
       moves=[(f"{F}/code/lot-01/blocked_realisateur.md", f"{F}/code/lot-01/blocked_realisateur-01.md")])
    # Hers: created waiting, decided in « chore: pre-code », renamed after.
    at(r, "2026-10-02T10:00:00+02:00", "feat: f lot-02 stopped",
       [(f"{F}/code/lot-02/blocked_realisateur.md", BLOCKED.format(d=""))])
    at(r, "2026-10-02T13:00:00+02:00", "chore: pre-code",
       [(f"{F}/code/lot-02/blocked_realisateur.md", BLOCKED.format(d="1. m"))])
    at(r, "2026-10-02T13:20:00+02:00", "feat: f lot-02 applied",
       moves=[(f"{F}/code/lot-02/blocked_realisateur.md", f"{F}/code/lot-02/blocked_realisateur-01.md")])
    # Still waiting.
    at(r, "2026-10-03T09:00:00+02:00", "feat: f lot-03 stopped",
       [(f"{F}/code/blocked_detailleur.md", BLOCKED.format(d=""))])
    # A correction cycle: its own files are not the main cycle's.
    at(r, "2026-10-04T09:00:00+02:00", "chore: answers", [(f"{F}/bugfix-01/bug-list.md", "- un écart\n")])
    at(r, "2026-10-04T10:00:00+02:00", "feat: diagnostic",
       [(f"{F}/bugfix-01/questions-diagnostiqueur-01.md", QFILE.format(a1="", a2=""))])
    return r


# ------------------------------------------------------------ §1 the line

def entry(**kw):
    e = {"at": "2026-10-10T14:03", "computer": "PC-SALON", "command": "/1_lexique f", "duration_s": 554.4,
         "read_tokens": 1555185, "output_tokens": 61789, "five_hour": 1.2, "seven_day": 0.4,
         "outcome": journal.QUESTIONS, "next": "répondre → /1_lexique", "created": ["questions-lexicographe-02.md"],
         "programme": None, "note": None}
    e.update(kw)
    return e


def test_a_line_is_written_human_readable_and_read_back(tmp_path):
    path = tmp_path / "journal.md"
    row = journal.append(str(path), entry(), "f")
    assert row == ("| 2026-10-10 14:03 | PC-SALON | /1_lexique f | 9 min 14 s | 1 555 185 lus · 61 789 écrits "
                   "| 1,2 % | 0,4 % | questions | répondre → /1_lexique | questions-lexicographe-02.md | — | — |")
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Journal de cycle — f\n") and "Aucun agent de la chaîne ne le lit." in text
    assert "| Quand | Ordinateur | Commande |" in text
    journal.append(str(path), entry(at="2026-10-10T15:00", duration_s=None, read_tokens=None, output_tokens=None,
                                    five_hour=None, seven_day=None, outcome=journal.ERROR, created=[],
                                    programme="Cette nuit, 1 h – 7 h", note="erreur : boom | pipe"), "f")
    back = journal.read(str(path))
    assert len(back) == 2
    assert back[0] == {**entry(), "duration_s": 554}
    b = back[1]
    assert b["duration_s"] is None and b["read_tokens"] is None and b["five_hour"] is None
    assert b["outcome"] == journal.ERROR and b["created"] == [] and b["programme"] == "Cette nuit, 1 h – 7 h"
    assert b["note"] == "erreur : boom | pipe"            # a pipe in a cell survives
    assert text.count("# Journal") == 1


@pytest.mark.parametrize("outcome,nxt,api,said", [
    ("terminé", {"kind": "run", "command": "2_structure"}, "", journal.DONE),
    ("terminé", {"kind": "done"}, "", journal.DONE),
    ("terminé", {"kind": "answer", "what": "questions", "command": "1_lexique"}, "", journal.QUESTIONS),
    ("terminé", {"kind": "answer", "what": "blocking", "command": "8_code"}, "", journal.BLOCKING),
    ("terminé", {"kind": "answer", "what": "questions and blocking"}, "", journal.BOTH),
    ("terminé", {"kind": "manual", "command": "diagnostique"}, "", journal.MANUAL),
    ("terminé", {"kind": "stop"}, "", journal.STOP),
    ("terminé", {"kind": "unknown"}, "", journal.NO_NEXT),
    ("erreur", None, "", journal.ERROR),
    ("erreur", None, "authentication_failed", journal.NOT_LOGGED),
    ("interrompu", {"kind": "run", "command": "8_code"}, "", journal.STOPPED),
])
def test_every_outcome(outcome, nxt, api, said):
    assert journal.outcome_of(outcome, nxt, api) == said


def test_next_text():
    assert journal.next_text({"kind": "run", "command": "2_structure"}) == "/2_structure"
    assert journal.next_text({"kind": "answer", "command": "1_lexique"}) == "répondre → /1_lexique"
    assert journal.next_text({"kind": "run", "command": "8_code"}, (3, 12)) == "/8_code (3/12 lots)"
    assert journal.next_text({"kind": "done"}) == "fini"
    assert journal.next_text(None) == "inconnu"


def test_the_files_a_run_created_main_and_correction(tmp_path):
    r = history_repo(tmp_path)
    def sha(when):
        return git(r, "rev-list", "-1", f"--before={when}", "HEAD").strip()
    assert journal.created_files(str(r), "f", "main", sha("2026-10-02T09:30:00+02:00"),
                                 sha("2026-10-02T12:00:00+02:00")) == ["code/lot-02/blocked_realisateur.md"]
    # Renamed -NN since: settled, no longer what the run left.
    assert journal.created_files(str(r), "f", "main", sha("2026-10-02T09:30:00+02:00"),
                                 sha("2026-10-03T10:00:00+02:00")) == ["code/blocked_detailleur.md"]
    first = git(r, "rev-list", "--max-parents=0", "HEAD").strip()
    head = git(r, "rev-parse", "HEAD").strip()
    # The correction's files belong to the correction; archived files to nobody.
    assert "bugfix-01/questions-diagnostiqueur-01.md" not in journal.created_files(str(r), "f", "main", first, head)
    assert journal.created_files(str(r), "f", "bugfix-01", first, head) == ["questions-diagnostiqueur-01.md"]
    # A file still on the disk, uncommitted, counts too.
    write(r, f"{F}/questions-redacteur-01.md", QFILE.format(a1="", a2=""))
    assert journal.created_files(str(r), "f", "main", head, head) == ["questions-redacteur-01.md"]


def test_commit_touches_the_journal_alone(tmp_path):
    r = tmp_path / "app"
    init(r)
    write(r, f"{F}/idees.md", "# Idées\n")
    commit(r, "first")
    write(r, f"{F}/questions-lexicographe-01.md", "### Q1\nAnswer: oui\n")    # an answer, not the journal's
    journal.append(journal.journal_path(str(r), "f"), entry(), "f")
    old, new = journal.commit(str(r), [f"{F}/journal.md"], "journal: /1_lexique f — questions")
    assert new and old != new
    assert git(r, "show", "--name-only", "--format=%s", "HEAD").split() == [
        "journal:", "/1_lexique", "f", "—", "questions", f"{F}/journal.md"]
    assert "questions-lexicographe-01.md" in git(r, "status", "--porcelain")
    # Nothing more to commit: no commit.
    assert journal.commit(str(r), [f"{F}/journal.md"], "x")[1] is None
    journal.append(journal.journal_path(str(r), "f"), entry(), "f")
    assert journal.dirty_journals(str(r)) == [f"{F}/journal.md"]


# ------------------------------------------------------------ §2 the history

def test_questions_timed_from_the_history(tmp_path):
    h = journal.history(str(history_repo(tmp_path)), "f")
    qs = h["questions"]
    assert len(qs) == 1
    q = qs[0]
    assert q["file"] == "questions-lexicographe-01.md" and q["agent"] == "lexicographe" and q["questions"] == 2
    assert q["created_at"] == "2026-10-01T10:00:00" or q["created_at"].endswith("00:00")
    # Answered when the last empty Answer: was filled — two hours after.
    assert q["seconds"] == 2 * 3600 and q["answered_by"] == "Product Owner"
    assert q["moved_to"] == "questions/lexicographe/questions-lexicographe-01.md"


def test_blocking_files_settled_and_by_whom(tmp_path):
    h = journal.history(str(history_repo(tmp_path)), "f")
    by = {b["file"]: b for b in h["blocking"]}
    arb = by["code/lot-01/blocked_realisateur.md"]
    assert arb["by"] == "Arbitre" and arb["settled_as"] == "code/lot-01/blocked_realisateur-01.md"
    assert arb["seconds"] == 0 and not arb["seen_waiting"]
    hers = by["code/lot-02/blocked_realisateur.md"]
    assert hers["by"] == "Product Owner" and hers["seconds"] == 3 * 3600
    assert hers["settled_at"] and hers["decided_sha"]
    waiting = by["code/blocked_detailleur.md"]
    assert waiting["by"] is None and waiting["decided_at"] is None and waiting["settled_at"] is None
    assert waiting["agent"] == "detailleur"


def test_by_whom_unknown_when_git_cannot_tell(tmp_path):
    r = tmp_path / "app"
    init(r)
    at(r, "2026-10-02T10:00:00+02:00", "feat: lot-02 stopped",
       [(f"{F}/code/lot-02/blocked_realisateur.md", BLOCKED.format(d=""))])
    # Decided in a merge's own content — no commit of hers, none of an agent's.
    at(r, "2026-10-02T11:00:00+02:00", "journal: /8_code f — blocage",
       [(f"{F}/code/lot-02/blocked_realisateur.md", BLOCKED.format(d="1. m"))])
    b = journal.history(str(r), "f")["blocking"][0]
    assert b["by"] == "inconnu"


def test_correction_cycle_history_is_its_own(tmp_path):
    r = history_repo(tmp_path)
    h = journal.history(str(r), "f", "bugfix-01")
    assert [q["file"] for q in h["questions"]] == ["questions-diagnostiqueur-01.md"] and not h["blocking"]
    assert journal.cycles(str(r), "f") == ["main", "bugfix-01"]


# ------------------------------------------------------------ §3 points à creuser

def test_points_raised_and_not_under_their_thresholds(tmp_path):
    hist = journal.history(str(history_repo(tmp_path)), "f")
    est = {"/1_lexique": {"five_hour": {"median": 1.0, "n": 4}}, "/8_code": {"five_hour": {"median": 3.0, "n": 5}}}
    es = [entry(at="2026-10-01T09:00", five_hour=2.5),                                  # 2.5 > 2 × 1
          entry(at="2026-10-01T10:00", outcome=journal.NOT_LOGGED, five_hour=None),
          entry(at="2026-10-02T09:00", command="/8_code f", next="/8_code (1/5 lots)", five_hour=3.0),
          entry(at="2026-10-02T10:00", command="/8_code f", next="/8_code (1/5 lots)", five_hour=3.0),
          entry(at="2026-10-02T11:00", command="/8_code f", next="/8_code (1/5 lots)", five_hour=3.0,
                programme="Cette nuit"),
          entry(at="2026-10-02T12:00", command="/8_code f", outcome=journal.ERROR, programme="Cette nuit",
                note="erreur : boom")]
    progs = [{"name": "Pendant 2 heures", "reason_kind": "erreur", "reason": "/7_lots a fini en erreur.",
              "ended_at": "2026-10-03T08:00:00"}, {"name": "Autre", "reason_kind": "besoin", "reason": "x"}]
    pts = journal.points(es, hist, est, None, progs)
    kinds = sorted(p["kind"] for p in pts)
    assert kinds == ["blocage", "coût", "erreur", "erreur", "programme", "programme", "sur place"]
    text = " ".join(p["text"] for p in pts)
    assert "n'était pas connecté" in text
    assert "3 fichiers de blocage de realisateur" not in text and "2 fichiers de blocage de realisateur" in text
    assert "lancée 3 fois de suite" in text and "« Cette nuit »" in text and "« Pendant 2 heures »" in text
    # Under the thresholds: nothing but the failures.
    th = {"cost_factor": 3, "repeat_runs": 4, "blocking_repeat": 3}
    pts = journal.points(es, hist, est, th, [])
    assert sorted(p["kind"] for p in pts) == ["erreur", "erreur", "programme"]
    # Under the threshold by a hair: 2.0 is not more than twice 1.0.
    assert not [p for p in journal.points([entry(five_hour=2.0)], {}, est, None) if p["kind"] == "coût"]
    # Moving: the same command, its proposal moving each time.
    moving = [entry(at=f"2026-10-02T0{i}:00", command="/8_code f", next=f"/8_code ({i}/5 lots)") for i in range(1, 5)]
    assert not journal.points(moving, {}, {}, None)


def test_thresholds_checked():
    assert journal.clean_thresholds(None) == journal.DEFAULT_THRESHOLDS
    assert journal.clean_thresholds({"cost_factor": "3", "repeat_runs": "5"})["repeat_runs"] == 5
    with pytest.raises(ValueError):
        journal.clean_thresholds({"repeat_runs": 1})
    with pytest.raises(ValueError):
        journal.clean_thresholds({"cost_factor": "beaucoup"})


# ------------------------------------------------------------ reconstruction

def stored_run(store, run_id, app, feature, command, started, ended, nxt, programme=None, limits=()):
    t = stats_mod.Tally()
    t.totals = {"input_tokens": 100, "cache_read_tokens": 900, "cache_creation_tokens": 0, "output_tokens": 50}
    store.record_run(run_id=run_id, feature=feature, work=feature, command=command, mode="auto", started_at=started,
                     ended_at=ended, tally=t, next_line=nxt, outcome="terminé", log_path=f"logs/{run_id}.jsonl",
                     app=app, programme=programme)
    for m in limits:
        store.record_limit(run_id, m)


def lim(at_, window, u, source, resets=1791265200):
    return {"measured_at": at_, "source": source, "window": window, "utilization": u, "resets_at": resets}


def reconstruct_repo(tmp_path):
    """Before 1.20: one run the stats remember (its merge), one merge they
    don't (the other computer's), one agent commit with no merge."""
    r = tmp_path / "app"
    init(r)
    at(r, "2026-10-01T09:00:00", "first", [(f"{F}/idees.md", "# Idées\n")])
    git(r, "checkout", "-q", "-b", "wt")
    at(r, "2026-10-01T10:05:00", "feat: lexicon sweep 1", [(f"{F}/questions-lexicographe-01.md", QFILE.format(a1="", a2=""))])
    git(r, "checkout", "-q", "master")
    merge(r, "2026-10-01T10:06:00", "Merge /1_lexique f", "wt")
    git(r, "checkout", "-q", "-b", "wt2")
    at(r, "2026-10-02T10:05:00", "feat: structure", [(f"{F}/produit.md", "# Produit\n"),
                                                    (f"{F}/questions-redacteur-01.md", QFILE.format(a1="", a2=""))])
    git(r, "checkout", "-q", "master")
    merge(r, "2026-10-02T10:06:00", "Merge /2_structure f", "wt2")
    at(r, "2026-10-03T10:00:00", "decoupeur: split", [(f"{F}/questions-decoupeur-01.md", QFILE.format(a1="", a2=""))])
    at(r, "2026-10-03T11:00:00", "chore: answers", [(f"{F}/questions-decoupeur-01.md", QFILE.format(a1=" a", a2=" b"))])
    return r


def test_reconstruction_from_stats_logs_and_git(tmp_path):
    r = reconstruct_repo(tmp_path)
    store = stats_mod.Store(str(tmp_path / "stats.sqlite"))
    stored_run(store, "r1", str(r), "f", "/1_lexique f", "2026-10-01T10:00:00", "2026-10-01T10:07:00",
               "Next: answer questions, then run /1_lexique f",
               limits=[lim("2026-10-01T10:01:00", "five_hour", 0.30, "event"),
                       lim("2026-10-01T10:07:00", "five_hour", 0.33, "usage"),
                       lim("2026-10-01T10:01:00", "seven_day", 0.10, "event"),
                       lim("2026-10-01T10:07:00", "seven_day", 0.11, "usage", resets=1791765200)])
    stored_run(store, "other", str(tmp_path / "ailleurs"), "f", "/3_decoupe f", "2026-10-03T09:59:00",
               "2026-10-03T10:01:00", "Next: done")         # another application: not this one's
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "consommation.log").write_text(
        "2026-10-01T09:59:58 · seuil de blocage passé outre — « Lancer quand même » : /1_lexique f dans « App » — x\n",
        encoding="utf-8")
    rec = journal.reconstruct(str(r), "f", store.path, str(logs), "App", computer="PC-SALON")
    lines = rec["main"]
    assert [e["command"] for e in lines] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]
    a, b, c = lines
    # From the stats: duration, tokens, shares, outcome, what it created.
    assert a["computer"] == "PC-SALON" and a["duration_s"] == 420 and a["read_tokens"] == 1000
    assert a["five_hour"] == 3.0 and a["outcome"] == journal.QUESTIONS
    assert a["created"] == ["questions-lexicographe-01.md"] and a["next"] == "répondre → /1_lexique"
    assert a["note"].startswith(journal.OVERRIDE_NOTE)
    # From git alone: the merge names the command; the cost is unknown.
    assert b["computer"] == "inconnu" and b["duration_s"] is None and b["five_hour"] is None
    assert b["created"] == ["questions-redacteur-01.md"] and "Merge /2_structure f" in b["note"]
    # An agent's commit with no merge: the command read from its file, said so.
    assert "commande déduite de questions-decoupeur-01.md" in c["note"]
    # Once written, nothing is built again.
    path = journal.journal_path(str(r), "f")
    journal.rewrite(path, lines, "f")
    assert journal.reconstruct(str(r), "f", store.path, str(logs), "App") == {}


def test_reconstruction_from_git_alone(tmp_path):
    r = reconstruct_repo(tmp_path)
    rec = journal.reconstruct(str(r), "f", None, None)
    assert [e["command"] for e in rec["main"]] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]
    assert all(e["duration_s"] is None and e["read_tokens"] is None for e in rec["main"])


def test_reconstruction_keeps_the_lines_after_its_first(tmp_path):
    r = reconstruct_repo(tmp_path)
    path = journal.journal_path(str(r), "f")
    journal.append(path, entry(at="2026-10-02T12:00", command="/3_decoupe f"), "f")
    rec = journal.reconstruct(str(r), "f", None, None)
    # Only what came before the journal's first line.
    assert [e["command"] for e in rec["main"]] == ["/1_lexique f", "/2_structure f"]
    journal.rewrite(path, journal.read(path) + rec["main"], "f")
    assert [e["command"] for e in journal.read(path)] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]


# ------------------------------------------------------------ the report

def test_the_report(tmp_path):
    r = history_repo(tmp_path)
    hist = journal.history(str(r), "f")
    es = [entry(at="2026-10-01T09:55"), entry(at="2026-10-02T08:55", command="/8_code f", outcome=journal.ERROR,
                                              note="erreur : boom", created=["code/lot-02/blocked_realisateur.md"])]
    pts = journal.points(es, hist, {}, None)
    text = journal.report_md("f", "main", es, hist, pts, now=datetime(2026, 10, 10, 18, 0))
    assert text.startswith("# Rapport de fin de cycle — f\n")
    for part in ("## En bref", "## Par étape", "## Où est passé son temps", "## Ce qui a échoué",
                 "## Points à creuser", "| /8_code | 1 |", "questions-lexicographe-01.md | lexicographe | 2 |",
                 "| code/lot-02/blocked_realisateur.md | realisateur |", "| Product Owner |", "| Arbitre |",
                 "/8_code f : erreur — erreur : boom", "Aucun agent de la chaîne ne le lit."):
        assert part in text, part
