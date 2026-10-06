import os

import pytest

import cmdtests
import questions
from conftest import fixture_path

# (fixture, entries, open) — open counted by the command's own grep. The real
# files of premiere-app-3, and hand-written files after the current templates
# (tests/fixtures/SOURCES.md).
OPEN = [
    ("real/premiere-app-3/questions-lexicographe-01.md", 32, 32),
    ("features/premiere-app-3/questions-lexicographe-01.md", 40, 8),
    ("context/premiere-app-3/questions-lexicographe-02.md", 13, 10),
    ("hand/questions-classeur-01.md", 4, 4),
    ("hand/questions-redacteur-01.md", 2, 1),
    ("hand/questions-sondeur-02.md", 3, 2),
    ("hand/questions-architecte-02.md", 2, 2),
]


def parse(rel):
    path = fixture_path(*rel.split("/"))
    return questions.parse_file(path, os.path.dirname(path)), path


@pytest.mark.parametrize("rel,count,open_count", OPEN)
def test_files_parse_like_the_commands_read_them(rel, count, open_count):
    parsed, path = parse(rel)
    assert parsed.errors == []
    assert len(parsed.entries) == count
    assert sorted(e.number for e in parsed.entries if e.open) == sorted(cmdtests.unanswered_questions(path))
    assert sum(e.open for e in parsed.entries) == open_count


def test_multiline_question_runs_until_answer():
    # agents/lexicographe.md:348-350: a `Question:` over several lines.
    parsed, _ = parse("real/premiere-app-3/questions-lexicographe-01.md")
    q1 = parsed.entries[0]
    assert q1.context == ["Terms: atelier, STATION"]
    assert q1.question.startswith("I read these as one same thing")
    assert q1.question.rstrip().endswith("(the exercise itself vs. the timed segment)?")
    assert q1.question.count("\n") == 6


def test_the_files_own_title_before_the_first_question_is_not_an_entry():
    # The lexicographe titles its file (premiere-app-3).
    parsed, path = parse("features/premiere-app-3/questions-lexicographe-01.md")
    assert open(path, encoding="utf-8").readline().startswith("# Questions")
    assert parsed.entries[0].number == 1 and parsed.entries[0].context == ["Terms: atelier, STATION"]


def test_title_on_the_block_line_and_kind():
    # agents/architecte.md:546-553: `Block: §3.2 — Reconciling two real entries`, `Kind:`.
    parsed, _ = parse("hand/questions-architecte-02.md")
    assert parsed.entries[0].context == ["Block: §3.2 — Reconciling two real entries", "Kind: replacement"]


def test_multiline_answers_are_kept_whole():
    parsed, _ = parse("hand/questions-redacteur-01.md")
    q1 = parsed.entries[0]
    assert q1.answer == "L'entrée est gardée et affichée à zéro.\n\nElle compte dans le total de la course."
    assert not q1.open


def test_unreadable_shape_is_an_error_never_no_questions():
    parsed, _ = parse("hand/questions-hors-gabarit.md")
    assert parsed.entries == []
    assert parsed.errors and "## Q1" in parsed.errors[0]


@pytest.mark.parametrize("lines,where", [
    # Every template: `Key: value` lines above `Question:`, nothing else.
    (["### Q1", "Race segment structure", "Block: B1", "Question: x", "Answer:"], "hors gabarit"),
    # Every template has a `Question:` line.
    (["### Q1", "Block: B1", "Answer:"], "Question:"),
    # `Options:` holds `- ` items (agents/redacteur.md:291-293 and the others).
    (["### Q1", "Block: B1", "Question: x", "Options:", "* une", "Answer:"], "Options:"),
    (["### Q1", "Block: B1", "Question: x", "Options:", "1. une", "Answer:"], "Options:"),
    # `Défaut:` is one line (agents/sondeur.md:420).
    (["### Q1", "Block: B1", "Question: x", "Défaut: a — B2", "suite", "Answer:"], "Défaut:"),
])
def test_what_no_template_writes_is_an_error(lines, where):
    parsed = questions.parse_lines(lines, "x", "x", "questions")
    assert parsed.entries == [] and where in parsed.errors[0]


def test_options_and_defaut():
    parsed, _ = parse("hand/questions-sondeur-02.md")
    q1, q2, q3 = parsed.entries
    assert q1.options == [
        "La course continue sur la montre seule et se synchronise au retour du lien.",
        "La course se met en pause jusqu'au retour du lien.",
    ]
    assert q1.default == q1.options[0]
    assert q1.default_source == "B3 « la montre est autonome pendant la course »"
    assert not q1.open and q1.answer_empty and questions.is_shown(q1)
    assert q2.open and q2.default is None and len(q2.options) == 3
    assert q3.open, "`Answer: ` with a trailing space is still empty"


def test_lexicographe_two_meanings_template():
    parsed, _ = parse("hand/questions-lexicographe-02.md")
    q2 = parsed.entries[1]
    assert "(b) the app being open" in q2.question
    assert len(q2.options) == 2
    q3 = parsed.entries[2]
    assert q3.open, "text starting on the next line reads as empty"
    assert q3.answer == "Oui, un tour est le segment de course."


def test_technique_file_is_open_on_an_empty_answer():
    # /6_convertit: answered when no `^Answer:\s*$` line is left.
    path = fixture_path("hand", "convertisseur", "technique-transversal.md")
    parsed = questions.parse_file(path, fixture_path("hand"))
    q = parsed.entries[0]
    assert q.kind == "technique" and q.default is None and q.open and len(q.options) == 2


def test_scan_finds_root_and_technique_files_only(place, tmp_path):
    place("hand/questions-classeur-01.md", "w/questions-classeur-01.md")
    place("hand/convertisseur/technique-model.md", "w/convertisseur/technique-model.md")
    # classed, closed and intermediate files are not answered by her
    place("real/premiere-app-3/questions-lexicographe-01.md", "w/questions/lexicographe/questions-lexicographe-01.md")
    place("hand/convertisseur/technique-model.md", "w/convertisseur/closed/technique-model-01.md")
    place("hand/questions-sondeur-02.md", "w/cadrage-produit/questions.md")
    shown, errors = questions.scan(str(tmp_path / "w"))
    assert errors == []
    assert {e.rel for e in shown} == {"questions-classeur-01.md", "convertisseur/technique-model.md"}
    assert len(shown) == 5


def test_scan_reports_unreadable_files(place, tmp_path):
    place("hand/questions-hors-gabarit.md", "w/questions-architecte-01.md")
    (tmp_path / "w" / "questions-redacteur-02.md").write_bytes(b"### Q1\nQuestion: \xff\xfe\nAnswer:\n")
    shown, errors = questions.scan(str(tmp_path / "w"))
    assert shown == []
    assert {e.rel for e in errors} == {"questions-architecte-01.md", "questions-redacteur-02.md"}


def test_missing_answer_line_is_an_error():
    parsed = questions.parse_lines(["### Q1", "Block: B1", "Question: why?"], "x", "x", "questions")
    assert parsed.entries == [] and "Answer:" in parsed.errors[0]


def test_duplicate_numbers_are_an_error():
    lines = ["### Q1", "Question: a?", "Answer:", "### Q1", "Question: b?", "Answer:"]
    parsed = questions.parse_lines(lines, "x", "x", "questions")
    assert any("deux fois" in e for e in parsed.errors)


def test_empty_questions_file_is_not_an_error():
    parsed = questions.parse_lines(["# Questions — rien"], "x", "x", "questions")
    assert parsed.entries == [] and parsed.errors == []
