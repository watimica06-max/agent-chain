"""parse → answer through writer.py → re-parse → the command's own test
(tests/cmdtests.py, written apart from the parsers) reads it answered."""
import os

import pytest

import blocking
import cmdtests
import questions
import writer
from writer import Choice


def q_entry(path, number):
    parsed = questions.parse_file(path, os.path.dirname(path))
    assert parsed.errors == []
    return [e for e in parsed.entries if e.number == number][0]


def b_entries(path, base=None):
    base = base or os.path.dirname(path)
    parsed = blocking.parse_file(path, base)
    assert parsed.notices == []
    return parsed.entries


# ============================================================ questions

REAL_Q = [
    "real/premiere-app-3/questions-lexicographe-01.md",
    "real/premiere-app-2/questions-classeur-01.md",
    "real/premiere-app/questions-sondeur-01.md",
]


@pytest.mark.parametrize("src", REAL_Q)
def test_real_question_free_text_round_trip(place, src):
    path = place(src, os.path.basename(src))
    before = cmdtests.unanswered_questions(path)
    e = q_entry(path, 1)
    text = "Une seule et même chose.\nLa station est le segment qu'occupe l'atelier."
    r = writer.write_question(e, Choice("free", text=text))
    assert r.status == "saved", r.message
    after = cmdtests.unanswered_questions(path)
    assert 1 not in after and after == [n for n in before if n != 1]
    again = q_entry(path, 1)
    assert not again.open and again.answer == text
    raw = open(path, encoding="utf-8").read()
    assert "\nAnswer: Une seule et même chose.\nLa station est" in raw


def test_option_written_in_full(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    e = q_entry(path, 2)
    r = writer.write_question(e, Choice("option", option=e.options[1]))
    assert r.status == "saved"
    assert 2 not in cmdtests.unanswered_questions(path)
    assert q_entry(path, 2).answer == "Aucune date, et la course passe en fin de liste."


def test_option_and_remark(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    e = q_entry(path, 2)
    r = writer.write_question(e, Choice("option", option=e.options[0], text="seulement pour l'import"))
    assert r.status == "saved"
    assert q_entry(path, 2).answer == "La date du jour de l'import, signalée comme estimée. — seulement pour l'import"


def test_default_kept_leaves_answer_empty(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    original = open(path, "rb").read()
    e = q_entry(path, 1)
    r = writer.write_question(e, Choice("default", option=e.default))
    assert r.status == "unchanged"
    assert open(path, "rb").read() == original
    assert 1 not in cmdtests.unanswered_questions(path), "the chain reads the default as accepted"


def test_default_with_remark_is_written(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    e = q_entry(path, 1)
    r = writer.write_question(e, Choice("default", option=e.default, text="et la montre vibre"))
    assert r.status == "saved"
    assert q_entry(path, 1).answer == e.default + " — et la montre vibre"


def test_trailing_space_answer_is_answered(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    r = writer.write_question(q_entry(path, 3), Choice("free", text="Oui, la même échelle."))
    assert r.status == "saved"
    assert cmdtests.unanswered_questions(path) == [2]


def test_architecte_replacement_options(place):
    path = place("hand/questions-architecte-02.md", "questions-architecte-02.md")
    e = q_entry(path, 1)
    assert writer.write_question(e, Choice("option", option=e.options[1])).status == "saved"
    assert cmdtests.unanswered_questions(path) == [2]


def test_lexicographe_two_meanings_and_text_below_answer(place):
    path = place("hand/questions-lexicographe-02.md", "questions-lexicographe-02.md")
    e2 = q_entry(path, 2)
    assert writer.write_question(e2, Choice("option", option=e2.options[1], text="§B12 passe sous (a)")).status == "saved"
    e3 = q_entry(path, 3)
    r = writer.write_question(e3, Choice("free", text="Oui, un tour est le segment de course."))
    assert r.status == "saved"
    raw = open(path, encoding="utf-8").read()
    assert "Answer: Oui, un tour est le segment de course.\n\n---\n\n### Q4" in raw
    assert cmdtests.unanswered_questions(path) == [1, 4]


def test_technique_option(place, tmp_path):
    path = place("hand/convertisseur/technique-model.md", "w/convertisseur/technique-model.md")
    e = q_entry(path, 1)
    assert not cmdtests.technique_answered(path)
    assert writer.write_question(e, Choice("option", option=e.options[0])).status == "saved"
    assert cmdtests.technique_answered(path)


def test_technique_default_kept_is_written_out(place):
    """/6_convertit has no `Défaut:` exception: leaving `Answer:` empty would
    leave the file unanswered for it."""
    path = place("hand/convertisseur/technique-transversal.md", "w/convertisseur/technique-transversal.md")
    e = q_entry(path, 1)
    r = writer.write_question(e, Choice("default", option=e.default))
    assert r.status == "saved"
    assert cmdtests.technique_answered(path)
    assert q_entry(path, 1).answer == "Une seule table, avec une colonne de type."


# ======================================================== write safety

def test_crlf_and_bom_preserved(tmp_path):
    path = tmp_path / "questions-x-01.md"
    path.write_bytes(b"\xef\xbb\xbf### Q1\r\nBlock: B1\r\nQuestion: why?\r\nAnswer:\r\n")
    r = writer.write_question(q_entry(str(path), 1), Choice("free", text="Parce que."))
    assert r.status == "saved"
    assert path.read_bytes() == b"\xef\xbb\xbf### Q1\r\nBlock: B1\r\nQuestion: why?\r\nAnswer: Parce que.\r\n"


def test_failed_check_undoes_the_write(place, monkeypatch):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    original = open(path, "rb").read()

    def refuse(entry, text):
        raise writer.WriteError("après écriture la commande lirait encore la question comme ouverte")
    monkeypatch.setattr(writer, "_verify_question", refuse)
    r = writer.write_question(q_entry(path, 2), Choice("free", text="x"))
    assert r.status == "error" and "ouverte" in r.message
    assert open(path, "rb").read() == original


def test_file_changed_since_display(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    e = q_entry(path, 2)
    raw = open(path, encoding="utf-8").read().replace("What does the race list", "What does the list")
    open(path, "w", encoding="utf-8").write(raw)
    r = writer.write_question(e, Choice("free", text="x"))
    assert r.status == "error" and "changé" in r.message


def test_already_answered_in_file(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    e = q_entry(path, 2)
    assert writer.write_question(e, Choice("free", text="une")).status == "saved"
    r = writer.write_question(e, Choice("free", text="deux"))
    assert r.status == "error" and "déjà répondu" in r.message
    assert q_entry(path, 2).answer == "une"


def test_line_that_would_read_as_a_heading_is_refused(place):
    path = place("hand/questions-sondeur-02.md", "questions-sondeur-02.md")
    original = open(path, "rb").read()
    r = writer.write_question(q_entry(path, 2), Choice("free", text="oui\n### Q9 tiens"))
    assert r.status == "error"
    assert open(path, "rb").read() == original


def test_compose_rules():
    opts = ["A.", "B."]
    assert writer.compose(Choice("option", option="A."), opts) == "A."
    assert writer.compose(Choice("option", option="A.", text="  et puis\n"), opts) == "A. — et puis"
    assert writer.compose(Choice("default", option="A."), opts, "A.") is None
    assert writer.compose(Choice("free", text="\n\nlibre\n"), opts) == "libre"
    assert writer.compose(Choice("none"), opts) is None
    with pytest.raises(writer.WriteError):
        writer.compose(Choice("option", option="C."), opts)
    with pytest.raises(writer.WriteError):
        writer.compose(Choice("free", text="  "), opts)


# ============================================================= blocking

def test_real_shape1_round_trip(place):
    path = place("hand/blocked_realisateur-reel-ouvert.md", "code/lot-22/blocked_realisateur.md")
    (e,) = b_entries(path)
    text = "Le lot core-sync porte ces deux fichiers.\nLot-22 attend qu'il soit livré."
    r = writer.write_blocking(e, Choice("free", text=text))
    assert r.status == "saved", r.message
    assert cmdtests.a2_empty(path) == [False]
    assert open(path, encoding="utf-8").read().endswith("## Decision\n\n" + text + "\n")


def test_shape1_option_and_remark(place):
    path = place("hand/blocked_lexicographe.md", "blocked_lexicographe.md")
    (e,) = b_entries(path)
    r = writer.write_blocking(e, Choice("option", option=e.options[1], text="idees-v2.md"))
    assert r.status == "saved"
    assert cmdtests.a2_empty(path) == [False]
    (again,) = b_entries(path)
    assert again.decision == "L'idée est dans un autre fichier, nommé en remarque. — idees-v2.md"


def test_shape2_heading_at_end_of_file(place):
    path = place("hand/blocked_architecte.md", "blocked_architecte.md")
    (e,) = b_entries(path)
    assert writer.write_blocking(e, Choice("option", option=e.options[0])).status == "saved"
    assert cmdtests.a2_empty(path) == [False]
    assert "## Invocation\n\n1\n" in open(path, encoding="utf-8").read()


def test_shape3_each_entry_under_its_own_decision(place):
    path = place("hand/blocked_qualifieur.md", "blocked_qualifieur.md")
    waiting = [e for e in b_entries(path) if e.waiting]
    assert [e.number for e in waiting] == [2]
    assert writer.write_blocking(waiting[0], Choice("option", option="transverse")).status == "saved"
    assert cmdtests.a2_empty(path) == [False, False]
    assert [e.decision for e in b_entries(path)] == ["comportement", "transverse"]


def test_shape3_redacteur_two_entries(place):
    path = place("hand/blocked_redacteur.md", "blocked_redacteur.md")
    e1, e2 = b_entries(path)
    assert writer.write_blocking(e1, Choice("free", text="Elle va dans B20.\nB19 est supprimé.")).status == "saved"
    e2 = b_entries(path)[1]
    assert writer.write_blocking(e2, Choice("option", option=e2.options[0])).status == "saved"
    assert cmdtests.a2_empty(path) == [False, False]
    raw = open(path, encoding="utf-8").read()
    assert "## Decision\n\nElle va dans B20.\nB19 est supprimé.\n\n## Blocking 2" in raw


def test_shape4_numbered_lines_one_per_entry(place):
    path = place("hand/blocked_detailleur.md", "code/blocked_detailleur.md")
    waiting = [e for e in b_entries(path) if e.waiting]
    assert [e.number for e in waiting] == [1, 3]
    r1 = writer.write_blocking(waiting[0], Choice("option", option=waiting[0].options[1], text="comme\n2. ailleurs"))
    assert r1.status == "saved"
    e3 = [e for e in b_entries(path) if e.number == 3][0]
    r3 = writer.write_blocking(e3, Choice("free", text="delta-zero\npartout,\n\nsans exception"))
    assert r3.status == "saved"
    assert cmdtests.shape4_open(path) == []
    assert cmdtests.numbered_count(path) == 3, "one numbered line per entry, never more"
    tail = open(path, encoding="utf-8").read().split("## Decision\n")[1]
    assert tail == ("\n2. lot-05 produces it; the sheet cites lot-05.\n"
                    "1. Tronqué à la seconde. — comme 2. ailleurs\n"
                    "3. delta-zero partout, sans exception\n")


def test_shape4_empty_decision(place):
    path = place("hand/blocked_realisateur.md", "code/lot-12/blocked_realisateur.md")
    (e,) = b_entries(path)
    assert writer.write_blocking(e, Choice("option", option=e.options[0])).status == "saved"
    assert cmdtests.shape4_open(path) == []
    assert open(path, encoding="utf-8").read().endswith("## Decision\n\n1. L'horloge est injectée par le constructeur.\n")


def test_shape4_in_a_worktree_is_written_there(tmp_path):
    main = tmp_path / "main" / "docs" / "features" / "f"
    main.mkdir(parents=True)
    wt = tmp_path / "wt"
    wt_work = wt / "docs" / "features" / "f"
    (wt_work / "code").mkdir(parents=True)
    src = os.path.join(os.path.dirname(__file__), "fixtures", "hand", "blocked_detailleur.md")
    (wt_work / "code" / "blocked_detailleur.md").write_bytes(open(src, "rb").read())
    shown, _, _ = blocking.scan(str(main), [(str(wt), str(wt_work))])
    r = writer.write_blocking(shown[0], Choice("free", text="Arrondi."))
    assert r.status == "saved", r.message
    assert cmdtests.shape4_open(str(wt_work / "code" / "blocked_detailleur.md")) == [3]
    assert not (main / "code").exists()


def test_shape5_last_decision(place):
    path = place("hand/blocked_cadreur.md", "code/blocked_cadreur.md")
    (e,) = b_entries(path)
    assert writer.write_blocking(e, Choice("option", option=e.options[1])).status == "saved"
    assert cmdtests.a2_empty(path) == [False, False]
    assert not b_entries(path)[0].waiting


def test_relecteur_anything_else(place):
    path = place("hand/blocked_relecteur-autre.md", "code/lot-09/blocked_relecteur.md")
    (e,) = b_entries(path)
    assert writer.write_blocking(e, Choice("option", option=e.options[0])).status == "saved"
    assert cmdtests.a2_empty(path) == [False]


def test_blocking_undo_on_failed_check(place, monkeypatch):
    path = place("hand/blocked_qualifieur.md", "blocked_qualifieur.md")
    original = open(path, "rb").read()
    monkeypatch.setattr(writer, "_verify_blocking", lambda e: (_ for _ in ()).throw(writer.WriteError("encore en attente")))
    e = [x for x in b_entries(path) if x.waiting][0]
    r = writer.write_blocking(e, Choice("free", text="transverse"))
    assert r.status == "error"
    assert open(path, "rb").read() == original


def test_redecoupage_decision(place, tmp_path):
    for n in ("", "-01", "-02"):
        place(f"hand/redecoupage/redecoupage{n}.md", f"w/code/redecoupage{n}.md")
    work = str(tmp_path / "w")
    r = blocking.read_redecoupage(work)
    assert r.waiting
    res = writer.write_redecoupage(r, Choice("free", text="Couper lot-07 par écran."), work)
    assert res.status == "saved", res.message
    raw = open(os.path.join(work, "code", "redecoupage.md"), encoding="utf-8").read()
    assert raw.endswith("## Décision du Product Owner\n\nCouper lot-07 par écran.\n")
    assert blocking.scan(work)[2] is None
