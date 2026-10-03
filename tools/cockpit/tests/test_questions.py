import os

import pytest

import cmdtests
import questions
from conftest import fixture_path

REAL_OPEN = [
    # (fixture, entries, open) — open counted by the command's own grep
    ("real/premiere-app-3/questions-lexicographe-01.md", 32, 32),
    ("real/premiere-app-2/questions-classeur-01.md", 4, 4),
    ("real/premiere-app/questions-sondeur-01.md", 190, 190),
    ("real/premiere-app-2/questions/lexicographe/questions-lexicographe-01.md", 36, 0),
    ("real/premiere-app-2/questions/redacteur/questions-redacteur-01.md", 1, 0),
    ("real/premiere-app/questions/convertisseur/questions-convertisseur-02.md", 3, 0),
]


def parse(rel):
    path = fixture_path(*rel.split("/"))
    return questions.parse_file(path, os.path.dirname(path)), path


@pytest.mark.parametrize("rel,count,open_count", REAL_OPEN)
def test_real_files_parse_like_the_commands_read_them(rel, count, open_count):
    parsed, path = parse(rel)
    assert parsed.errors == []
    assert len(parsed.entries) == count
    assert sorted(e.number for e in parsed.entries if e.open) == sorted(cmdtests.unanswered_questions(path))
    assert sum(e.open for e in parsed.entries) == open_count


def test_multiline_question_runs_until_answer():
    parsed, _ = parse("real/premiere-app-3/questions-lexicographe-01.md")
    q1 = parsed.entries[0]
    assert q1.context == ["Terms: atelier, STATION"]
    assert q1.question.startswith("I read these as one same thing")
    assert q1.question.rstrip().endswith("(the exercise itself vs. the timed segment)?")
    assert q1.question.count("\n") == 6


def test_prose_before_first_question_is_ignored():
    parsed, _ = parse("real/premiere-app-2/questions/lexicographe/questions-lexicographe-01.md")
    assert parsed.entries[0].number == 1
    assert parsed.entries[0].answer == "Station"


def test_answer_with_no_space_after_colon_is_read():
    parsed, _ = parse("real/premiere-app-2/questions/redacteur/questions-redacteur-01.md")
    a = parsed.entries[0].answer
    assert a.startswith("L'autorisation d'accès")
    assert a.endswith("[integrated: B163, B164, B165]")
    assert not parsed.entries[0].open


def test_old_shape_title_on_block_line():
    parsed, _ = parse("real/premiere-app/questions-sondeur-01.md")
    assert parsed.entries[0].context == ["Block: B1 — Race segment structure"]


def test_multiline_answers_are_kept_whole():
    parsed, _ = parse("real/premiere-app/questions/convertisseur/questions-convertisseur-02.md")
    q2 = [e for e in parsed.entries if e.number == 2][0]
    assert q2.answer.startswith("Elle est saisie à l'import.")
    assert "\n\n" in q2.answer


def test_unreadable_shape_is_an_error_never_no_questions():
    parsed, _ = parse("real/premiere-app/questions/architecte/questions-architecte-01.md")
    assert parsed.entries == []
    assert parsed.errors and "## Q1" in parsed.errors[0]


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


def test_technique_file_ignores_defaut():
    path = fixture_path("hand", "convertisseur", "technique-transversal.md")
    parsed = questions.parse_file(path, fixture_path("hand"))
    q = parsed.entries[0]
    assert q.kind == "technique" and q.default and q.open


def test_scan_finds_root_and_technique_files_only(place, tmp_path):
    place("real/premiere-app-2/questions-classeur-01.md", "w/questions-classeur-01.md")
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
    place("real/premiere-app/questions/architecte/questions-architecte-01.md", "w/questions-architecte-01.md")
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
