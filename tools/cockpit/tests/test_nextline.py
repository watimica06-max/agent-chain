import pytest

import nextline

RELAY = "Le lexique est réglé.\n\nTrois termes retirés.\n\n"


@pytest.mark.parametrize("line,expect", [
    ("Next: run /2_structure premiere-app-3",
     dict(kind="run", command="2_structure", args="premiere-app-3")),
    ("Next: run /deploie", dict(kind="run", command="deploie", args="")),
    ("Next: answer questions", dict(kind="answer", what="questions", command=None)),
    ("Next: answer blocking", dict(kind="answer", what="blocking", command=None)),
    ("Next: answer questions and blocking",
     dict(kind="answer", what="questions and blocking", command=None)),
    ("Next: answer blocking, then run /8_code premiere-app",
     dict(kind="answer", what="blocking", command="8_code", args="premiere-app")),
    ("Next: answer questions and blocking, then run /6_convertit premiere-app-3",
     dict(kind="answer", what="questions and blocking", command="6_convertit", args="premiere-app-3")),
    ("Next: manual correct the product file",
     dict(kind="manual", text="correct the product file", command=None)),
    ("Next: manual écrire sa décision sous ## Décision du Product Owner dans code/redecoupage.md, then run /7_lots premiere-app",
     dict(kind="manual", command="7_lots", args="premiere-app",
          text="écrire sa décision sous ## Décision du Product Owner dans code/redecoupage.md")),
    ("Next: stop worktree dirty", dict(kind="stop", text="worktree dirty")),
    ("Next: stop input missing: code/decoupage.md — the step before it has to run again",
     dict(kind="stop", text="input missing: code/decoupage.md — the step before it has to run again")),
    ("Next: done", dict(kind="done")),
])
def test_every_form_of_the_grammar(line, expect):
    n = nextline.parse(RELAY + line)
    for k, v in expect.items():
        assert getattr(n, k) == v, k
    assert n.raw == line
    assert nextline.describe_fr(n)


def test_no_line_is_unknown():
    n = nextline.parse(RELAY)
    assert n.kind == "unknown" and n.raw == ""
    assert "inconnue" in n.to_dict()["french"]


def test_empty_relay():
    assert nextline.parse("").kind == "unknown"
    assert nextline.parse(None).kind == "unknown"


def test_outside_the_grammar_is_unknown_not_guessed():
    for body in ("Next: run 8_code x", "Next: answer everything", "Next: maybe /8_code",
                 "Next: manual", "Next: stopped"):
        assert nextline.parse(body).kind == "unknown", body


def test_last_next_line_wins():
    relay = "Next: run /1_lexique a\nquoted above\nNext: run /2_structure a"
    assert nextline.parse(relay).command == "2_structure"


def test_markdown_wrapping_tolerated():
    assert nextline.parse("**Next: done**").kind == "done"
    assert nextline.parse("`Next: run /9_controle f`").command == "9_controle"


def test_next_inside_a_sentence_is_not_a_line():
    assert nextline.parse("The Next: line is read by the cockpit.").kind == "unknown"


def test_french():
    assert nextline.parse("Next: answer questions, then run /1_lexique f").to_dict()["french"] == \
        "Répondre aux questions, puis lancer /1_lexique f."
