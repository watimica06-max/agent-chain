import os

import blocking
import cmdtests
import textfile
from conftest import fixture_path


def parse(rel, as_name=None, work_dir=None):
    path = fixture_path(*rel.split("/"))
    lines = textfile.load(path).lines
    name_path = os.path.join(os.path.dirname(path), as_name) if as_name else path
    return blocking.parse_lines(lines, name_path, as_name or os.path.basename(path),
                                work_dir=work_dir), path


# ------------------------------------------------- decided, broken, empty

def test_shape1_decided_is_not_waiting():
    # agents/concepteur.md:150-166, its `## Decision` filled.
    p, path = parse("hand/blocked_concepteur-01.md", as_name="blocked_concepteur.md")
    (e,) = p.entries
    assert e.shape == 1 and not e.waiting
    assert e.what_blocks and e.where and e.to_resume and len(e.options) == 2
    assert cmdtests.a2_empty(path) == [False]


def test_an_empty_file_is_a_warning():
    p = blocking.parse_lines(["", ""], "x/blocked_testeur.md", "blocked_testeur.md")
    assert p.entries == [] and p.notices == [] and p.warnings


def test_a_file_without_decision_is_a_notice():
    p = blocking.parse_lines(["## What blocks", "", "x", "", "## Where", "", "y"],
                             "x/blocked_testeur.md", "blocked_testeur.md")
    assert p.entries == [] and p.notices


def test_an_option_list_holds_dash_items_only():
    # Every template: `Options:`, then `- ` items, one line each.
    lines = ["## What blocks", "", "x", "", "## Where", "", "y", "", "## To resume", "", "Say which.", "",
             "Options:", "- Une.", "- Deux.", "* pas une option", "", "## Decision", ""]
    (e,) = blocking.parse_lines(lines, "x/blocked_testeur.md", "blocked_testeur.md").entries
    assert e.options == ["Une.", "Deux."] and "* pas une option" in e.to_resume


# ---------------------------------------------------------- the shapes

def test_shape1_with_options():
    p, path = parse("hand/blocked_lexicographe.md")
    (e,) = p.entries
    assert e.shape == 1 and e.waiting
    assert e.to_resume == "Write the idea file, or say which file holds the idea."
    assert len(e.options) == 2


def test_shape2_invocation_is_routing_not_shown():
    p, path = parse("hand/blocked_architecte.md")
    (e,) = p.entries
    assert e.shape == 2 and e.waiting
    assert "1" not in e.what_blocks.split()
    assert len(e.options) == 2


def test_shape3_one_decision_per_entry():
    p, path = parse("hand/blocked_qualifieur.md")
    assert [(e.shape, e.number, e.waiting) for e in p.entries] == [(3, 1, False), (3, 2, True)]
    assert cmdtests.a2_empty(path) == [False, True]
    assert p.entries[1].options == ["transverse", "comportement", "Le bloc est à réécrire par le Rédacteur."]


def test_shape3_redacteur_invocation_3():
    p, path = parse("hand/blocked_redacteur.md")
    assert [(e.number, e.waiting) for e in p.entries] == [(1, True), (2, True)]
    assert p.entries[0].options == [] and len(p.entries[1].options) == 2


def test_shape4_open_numbers_are_the_absent_ones():
    p, path = parse("hand/blocked_detailleur.md")
    assert [(e.shape, e.number, e.lot, e.waiting) for e in p.entries] == [
        (4, 1, "lot-04", True), (4, 2, "lot-07", False), (4, 3, "lot-07", True)]
    assert cmdtests.shape4_open(path) == [1, 3]
    assert p.entries[0].options == ["Arrondi à la seconde la plus proche.", "Tronqué à la seconde."]


def test_shape4_single_entry():
    p, path = parse("hand/blocked_realisateur.md")
    (e,) = p.entries
    assert e.shape == 4 and e.waiting and e.number == 1 and len(e.options) == 2


def test_shape5_only_last_block_is_live():
    p, path = parse("hand/blocked_cadreur.md")
    (e,) = p.entries
    assert e.shape == 5 and e.waiting
    assert e.where == "spec-technique.md §7.2"
    assert cmdtests.a2_empty(path) == [False, True]


def cadreur_request(tmp_path):
    """The 1.0 fixtures: a cadreur block whose `## Where` names Request 2,
    beside `architecte/cadreur.md` (Request 1 granted, Request 2 empty)."""
    work = tmp_path / "w"
    (work / "code").mkdir(parents=True)
    (work / "architecte").mkdir()
    for src, dst in [("hand/cadreur-request/blocked_cadreur.md", "code/blocked_cadreur.md"),
                     ("hand/cadreur-request/architecte-cadreur.md", "architecte/cadreur.md")]:
        (work / dst).write_bytes(open(fixture_path(*src.split("/")), "rb").read())
    return work


def test_shape5_waiting_on_architecte_is_not_hers(tmp_path):
    work = cadreur_request(tmp_path)
    # Request 2's verdict is empty: the Architecte answers it (cmd/7_lots.md:210).
    shown, notices, _ = blocking.scan(str(work))
    assert shown == [] and notices == []
    # Without the request file, nothing lifts it: it is hers.
    os.remove(work / "architecte" / "cadreur.md")
    shown, _, _ = blocking.scan(str(work))
    assert len(shown) == 1 and shown[0].note == ""


def test_shape5_a_request_with_no_verdict_heading_is_not_hers(tmp_path):
    work = cadreur_request(tmp_path)
    req = work / "architecte" / "cadreur.md"
    req.write_text(req.read_text(encoding="utf-8").replace("## Verdict\n\n\n", "").rstrip()
                   .removesuffix("## Verdict").rstrip() + "\n", encoding="utf-8")
    assert "## Verdict" not in req.read_text(encoding="utf-8").split("# Request 2")[1]
    shown, _, _ = blocking.scan(str(work))
    assert shown == []                        # read as an empty one (cmd/7_lots.md:244-245)


def test_shape5_a_refused_verdict_is_shown(tmp_path):
    work = cadreur_request(tmp_path)
    req = work / "architecte" / "cadreur.md"
    req.write_text(req.read_text(encoding="utf-8").rstrip() +
                   "\n\nNot a convention: the domain module stays free of persistence. "
                   "Settle it in the split.\n", encoding="utf-8")
    shown, notices, _ = blocking.scan(str(work))
    (e,) = shown
    assert e.shape == 5 and e.waiting and notices == []
    # The refusal is hers; nothing on disk tells it from a verdict the Cadreur
    # has yet to read, so the entry says both.
    assert "Request 2" in e.note and "verdict refused" in e.note
    assert e.to_dict()["note"] == e.note


def test_shape5_only_the_request_its_where_names_counts(tmp_path):
    work = cadreur_request(tmp_path)
    # Request 1 is granted; the block names Request 2, still empty: not hers.
    shown, _, _ = blocking.scan(str(work))
    assert shown == []
    # Named Request 1, the filled one: shown, with the note.
    b = work / "code" / "blocked_cadreur.md"
    b.write_text(b.read_text(encoding="utf-8").replace("Request 2\n\n## To resume", "Request 1\n\n## To resume"),
                 encoding="utf-8")
    (e,) = blocking.scan(str(work))[0]
    assert "Request 1" in e.note


def test_shape5_once_applied_it_is_gone(tmp_path):
    work = cadreur_request(tmp_path)
    os.rename(work / "code" / "blocked_cadreur.md", work / "code" / "blocked_cadreur-01.md")
    assert blocking.scan(str(work))[0] == []  # renamed by /7_lots on « verdict applied »


def test_a_relecteur_entry_is_never_hidden():
    p, _ = parse("hand/blocked_relecteur-autre.md", as_name="blocked_relecteur.md")
    assert p.entries[0].waiting and p.entries[0].note == ""
    # The guess fires — an input named, said missing — and the entry stays,
    # carrying what the guess saw.
    p, _ = parse("hand/blocked_relecteur-acte.md", as_name="blocked_relecteur.md")
    (e,) = p.entries
    assert e.waiting
    assert "tests.md" in e.note and "missing" in e.note and "8_code.md:770-772" in e.note


def test_a_relecteur_entry_is_in_the_scan_whatever_it_says(tmp_path):
    for name in ("blocked_relecteur-acte.md", "blocked_relecteur-autre.md"):
        work = tmp_path / name / "w"
        (work / "code" / "lot-09").mkdir(parents=True)
        (work / "code" / "lot-09" / "blocked_relecteur.md").write_bytes(
            open(fixture_path("hand", name), "rb").read())
        shown, _, _ = blocking.scan(str(work))
        assert len(shown) == 1 and shown[0].agent == "relecteur"


def test_verificateur_never_shown():
    p, _ = parse("hand/blocked_verificateur.md")
    assert p.entries == [] and p.notices == []


# ---------------------------------------------------- discovery and scan

def _tree(tmp_path, files):
    for src, dst in files:
        target = tmp_path / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(open(fixture_path(*src.split("/")), "rb").read())


def test_scan_walks_the_working_folder(tmp_path):
    feat = tmp_path / "docs" / "features" / "f"
    _tree(feat, [
        ("hand/blocked_lexicographe.md", "blocked_lexicographe.md"),
        ("hand/blocked_qualifieur.md", "blocked_qualifieur.md"),
        ("hand/blocked_detailleur.md", "code/blocked_detailleur.md"),
        ("hand/blocked_realisateur.md", "code/lot-12/blocked_realisateur.md"),
        ("hand/blocked_architecte.md", "cadrage-produit/blocked_par-bloc.md"),
        ("hand/blocked_lexicographe.md", "blocked_lexicographe-01.md"),        # archived
        ("hand/blocked_lexicographe.md", "convertisseur/closed/blocked_x.md"),  # closed
        ("hand/blocked_lexicographe.md", "bugfix-01/blocked_diagnostiqueur.md"),  # its own folder
        ("hand/blocked_verificateur.md", "code/blocked_verificateur.md"),
    ])
    shown, notices, redec = blocking.scan(str(feat))
    assert notices == [] and redec is None
    assert sorted((e.rel, e.number) for e in shown) == [
        ("blocked_lexicographe.md", None),
        ("blocked_qualifieur.md", 2),
        ("cadrage-produit/blocked_par-bloc.md", None),
        ("code/blocked_detailleur.md", 1),
        ("code/blocked_detailleur.md", 3),
        ("code/lot-12/blocked_realisateur.md", 1),
    ]
    # A bugfix-NN working folder is scanned on its own.
    shown, _, _ = blocking.scan(str(feat / "bugfix-01"))
    assert [e.rel for e in shown] == ["blocked_diagnostiqueur.md"]


def test_worktree_shape4_files_are_read_there(tmp_path):
    main = tmp_path / "main" / "docs" / "features" / "f"
    wt = tmp_path / "wt"
    wt_work = wt / "docs" / "features" / "f"
    main.mkdir(parents=True)
    _tree(wt_work, [
        ("hand/blocked_detailleur.md", "code/blocked_detailleur.md"),
        ("hand/blocked_lexicographe.md", "blocked_lexicographe.md"),  # not shape 4: not read there
    ])
    shown, notices, _ = blocking.scan(str(main), [(str(wt), str(wt_work))])
    assert [(e.number, e.worktree) for e in shown] == [(1, str(wt)), (3, str(wt))]
    assert all(e.file.startswith(str(wt_work)) for e in shown)
    assert shown[0].id != blocking.scan(str(wt_work))[0][0].id


def test_redecoupage_shown_on_the_third_return(tmp_path):
    work = tmp_path / "w"
    _tree(work, [("hand/redecoupage/redecoupage.md", "code/redecoupage.md")])
    assert blocking.scan(str(work))[2] is None          # first return: /7_lots's
    _tree(work, [("hand/redecoupage/redecoupage-01.md", "code/redecoupage-01.md"),
                 ("hand/redecoupage/redecoupage-02.md", "code/redecoupage-02.md")])
    r = blocking.scan(str(work))[2]
    assert r is not None and r.count == 3 and r.waiting
    assert r.ce_qui_revient.startswith("lot-07 comes back a third time")


def test_redecoupage_count_restarts_after_her_decision(tmp_path):
    work = tmp_path / "w"
    _tree(work, [("hand/redecoupage/redecoupage.md", "code/redecoupage.md"),
                 ("hand/redecoupage/redecoupage-01.md", "code/redecoupage-01.md"),
                 ("hand/redecoupage/redecoupage-02.md", "code/redecoupage-02.md")])
    with open(work / "code" / "redecoupage-02.md", "a", encoding="utf-8") as f:
        f.write("\n## Décision du Product Owner\n\nCouper lot-07 par écran.\n")
    assert blocking.redecoupage_count(str(work)) == 1
    assert blocking.scan(str(work))[2] is None
