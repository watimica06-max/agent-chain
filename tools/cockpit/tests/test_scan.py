"""Cockpit 1.3, §1 — the scan, on the real files of premiere-app-3, on a
feature built through the whole chain after the commands' templates, and on
small folders built for one rule each. Reads only: no command runs."""
import os
import re
import shutil
import time

import pytest

import batirworld as bw
import scan

HERE = os.path.dirname(os.path.abspath(__file__))
COCKPIT = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(COCKPIT, "..", ".."))
FEATURES = os.path.join(HERE, "fixtures", "features")
RULES_MD = os.path.join(COCKPIT, "scan_rules.md")

F, A, AF, EC, BL, IN = scan.FAITE, scan.ATTEND, scan.A_FAIRE, scan.EN_COURS, scan.BLOQUEE, scan.INCONNU


def make_app(tmp_path, *features):
    app = tmp_path / "app"
    (app / ".claude").mkdir(parents=True)
    (app / "docs" / "features").mkdir(parents=True)
    (app / "docs" / "TECHNICAL_CONVENTIONS.md").write_text(bw.CONVENTIONS, encoding="utf-8")
    for f in features:
        shutil.copytree(os.path.join(FEATURES, f), app / "docs" / "features" / f)
    return app


def run_scan(app, feature, run=None, conventions_commit=bw.COMMIT):
    """The scan, the conventions last changed at `bw.COMMIT` — what the
    server reads with git (server.conventions_commit)."""
    return scan.run_scan(app, feature, run, conventions_commit)


def states(steps):
    return {s["id"]: s["state"] for s in steps}


def step(steps, sid):
    return next(s for s in steps if s["id"] == sid)


def corr(r, name):
    return next(c for c in r["corrections"] if c["name"] == name)


# ----------------------------- a feature through the whole chain, two corrections

VERDICT_PASS = ("## Status\n\nPASS\n\n## Attempts\n\n1\n\n## Verified\n\n./gradlew test green\n\n## Findings\n\n—\n\n"
                "## Cause\n\n—\n\n## Causes so far\n\n—\n\n## Symbol divergences\n\n—\n")


def write(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def split(code, lots):
    """A split that holds: `code/decoupage.md` (agents/cadreur.md:911-918) and
    `code/sequence.md` with an empty `## Defects` (agents/verificateur.md:107-119),
    every lot reviewed PASS (agents/relecteur.md:144-174)."""
    write(code / "decoupage.md", "".join(
        f"## {l}\n\nAnchor: §{k}.1 — Entry {k}\nNeeds: —\nProduces: S{k}\nModifies: —\nTouches: —\n\n"
        for k, l in enumerate(lots, 1)))
    write(code / "sequence.md", f"Round: 1\n\n## Order\n\n{', '.join(lots)}\n\n## Blocks\n\n"
                                f"block-1: {', '.join(lots)}\n\n## Defects\n\n")
    for l in lots:
        write(code / l / "verdict.md", VERDICT_PASS)


def chain_app(tmp_path):
    app = make_app(tmp_path)
    build_chain(app, "f")
    return app


def build_chain(app, name):
    """Feature `name`: split, coded and controlled; `bugfix-01/` diagnosed,
    coded and controlled; `bugfix-02/` diagnosed, not split yet. A sondeur
    question left open at the root. Every file after its command's template."""
    f = app / "docs" / "features" / name
    write(f / "idees.md", "# Idée\n")
    write(f / "desc-produit.md", "# Produit\n\n### B1 — Une course\nGenre: comportement\nNature: model\n\nTexte.\n")
    write(f / "spec-technique.md", "# Preamble\n\n### §1.1 — Entry 1\n")
    write(f / "couverture.md", "§1.1\n")
    bw.report(f)
    write(f / "questions-sondeur-03.md", "### Q1\nBlock: B1\nQuestion: what is missing?\nAnswer:\n")
    split(f / "code", ["lot-01", "lot-02"])
    # /9_controle's four files (9_controle.md:532-539).
    write(f / "code" / "rapport-controle.md", "# Rapport\n")
    write(f / "code" / "recette-ordonnee.md", "# Recette\n")
    write(f / "code" / "decisions-produit.md", "# Décisions\n")
    write(f / "registre-questions.md", "# Registre\n")
    b1 = f / "bugfix-01"
    write(b1 / "bug-list.md", "G01 Le chronomètre saute une seconde\n")
    write(b1 / "desc-bug.md", "# Preamble\n\n### §1 — G01\n")
    split(b1 / "code", ["lot-01"])
    write(b1 / "code" / "recette-ordonnee.md", "# Recette\n")
    write(b1 / "code" / "decisions-produit.md", "# Décisions\n")
    b2 = f / "bugfix-02"
    write(b2 / "bug-list.md", "G01 La liste ne se trie pas\n")
    write(b2 / "desc-bug.md", "# Preamble\n\n### §1 — G01\n")
    return f


def test_a_feature_through_the_chain_and_its_corrections(tmp_path):
    app = chain_app(tmp_path)
    r = run_scan(str(app), "f")
    assert states(r["main"]) == {
        # The sondeur question left at the root: 1_lexique stops on it (OWN-Q).
        "1_lexique": A,
        # The split is cut: the upstream is closed (6_convertit.md:35-38).
        "2_structure": F, "3_decoupe": F, "3a_genre": F, "3b_nature": F,
        "4_grille": F, "5_reclasse": F, "6_convertit": F,
        "conventions": F, "batir": F, "7_lots": F, "8_code": F,
        # A correction is open: the feature was controlled and tested (9_controle.md:556-557).
        "9_controle": F, "test": F,
        "fusion": AF,
    }
    assert step(r["main"], "8_code")["lots"] == {"pass": 2, "total": 2}
    assert [c["name"] for c in r["corrections"]] == ["bugfix-02", "bugfix-01"]
    assert states(corr(r, "bugfix-02")["steps"]) == {"diagnostique": F, "7_lots": AF, "8_code": AF, "9_controle": AF}
    assert states(corr(r, "bugfix-01")["steps"]) == {"diagnostique": F, "7_lots": F, "8_code": F, "9_controle": F}
    assert step(corr(r, "bugfix-01")["steps"], "8_code")["lots"] == {"pass": 1, "total": 1}
    # The highest correction is open: the dashboard proposes it, the main chain keeps its own.
    assert r["proposal"] == {"chain": "bugfix-02", "step": "7_lots", "command": "7_lots",
                             "name": "Découper en lots", "state": AF, "proposable": True}
    assert r["main_proposal"]["step"] == "1_lexique" and r["main_proposal"]["state"] == A
    assert [o["step"] for o in r["opens"]] == ["1_lexique"]
    assert r["alerts"] == [] and r["unknown_owner"] == []


def test_premiere_app_3(tmp_path):
    app = make_app(tmp_path, "premiere-app-3")
    r = run_scan(str(app), "premiere-app-3")
    assert states(r["main"]) == {
        "1_lexique": A,          # questions-lexicographe-01.md: eight entries still open
        "2_structure": AF, "3_decoupe": AF, "3a_genre": AF, "3b_nature": AF, "4_grille": AF,
        "5_reclasse": AF, "6_convertit": AF, "conventions": AF, "batir": AF, "7_lots": AF,
        "8_code": AF, "9_controle": AF, "test": AF, "fusion": AF,
    }
    assert len(r["opens"]) == 8
    assert r["proposal"]["step"] == "1_lexique"


def test_scan_under_a_second(tmp_path):
    app = chain_app(tmp_path)
    t0 = time.perf_counter()
    run_scan(str(app), "f")
    assert time.perf_counter() - t0 < 1.0


# ---------------------------------------------- « Pourquoi ? », per state

def test_why_names_the_rule_and_the_files_for_each_state(tmp_path):
    app = chain_app(tmp_path)
    shutil.copytree(os.path.join(FEATURES, "premiere-app-3"), app / "docs" / "features" / "premiere-app-3")
    # A product file written before any behaviour block, the grid never run
    # (4_grille.md:134-140).
    write(app / "docs" / "features" / "g" / "desc-produit.md",
          "# Produit\n\n### B1 — Une règle\nGenre: règle\nNature: model\n\nTexte.\n")
    r1 = run_scan(str(app), "f")
    r2 = run_scan(str(app), "g")
    r3 = run_scan(str(app), "premiere-app-3")
    run = {"status": "running", "command": "1_lexique", "work": "premiere-app-3",
           "prompt": "/1_lexique premiere-app-3", "started_at": "2026-10-05T10:00:00"}
    r4 = run_scan(str(app), "premiere-app-3", run)
    cases = [
        (step(r1["main"], "conventions"), F, "CON-7", ["couverture.md"], "conventions.md:95-97"),
        (step(r1["main"], "1_lexique"), A, "G-ATT", ["questions-sondeur-03.md"], "« À qui est une réponse »"),
        (step(r4["main"], "1_lexique"), EC, "G-RUN", [], "le run en cours"),
        (step(r2["main"], "4_grille"), BL, "GRI-5", ["desc-produit.md"], "4_grille.md:134-140"),
        (step(r3["main"], "2_structure"), AF, "STR-1", ["questions-lexicographe-01.md"], "2_structure.md:63-72"),
    ]
    for st, state, rule, files, cite in cases:
        assert st["state"] == state
        w = st["why"][-1]
        assert w["rule"] == rule and w["files"] == files and cite in w["cite"], (st["id"], w)
        assert w["text"]


def turn_folder(tmp_path, root_files=(), markers=True, filed_sondeur=True):
    """A feature in the middle of a later turn of the upstream: the vocabulary
    settled, the grid run once, a block MODIFIED by the last integration."""
    app = tmp_path / "app"
    feat = app / "docs" / "features" / "t"
    (app / ".claude").mkdir(parents=True, exist_ok=True)
    (feat / "questions" / "lexicographe").mkdir(parents=True)
    (feat / "questions" / "lexicographe" / "questions-lexicographe-03.md").write_text("# Lexique\n", encoding="utf-8")
    if filed_sondeur:
        (feat / "questions" / "sondeur").mkdir(parents=True)
        (feat / "questions" / "sondeur" / "questions-sondeur-01.md").write_text(
            "### Q1\nQuestion: x\nAnswer: oui\n", encoding="utf-8")
    title = "### B1 — Une course" + (" MODIFIED" if markers else "")
    (feat / "desc-produit.md").write_text(
        f"# Produit\n\n{title}\nGenre: comportement\nNature: model\n\nTexte.\n", encoding="utf-8")
    for name in root_files:
        (feat / name).write_text("# rien à demander\n", encoding="utf-8")
    return app


@pytest.mark.parametrize("root,expect", [
    # After /2_structure: the Rédacteur's file at the root (agents/redacteur.md:305).
    (["questions-redacteur-02.md"], {"2_structure": F, "3_decoupe": AF, "3a_genre": AF, "3b_nature": AF}),
    # After /3_decoupe: it filed that file (3_decoupe.md:66-69) — the root is empty.
    ([], {"2_structure": F, "3_decoupe": F, "3a_genre": AF, "3b_nature": AF}),
    # After /3a_genre: its own file (agents/qualifieur.md:3).
    (["questions-qualifieur-01.md"], {"3_decoupe": F, "3a_genre": F, "3b_nature": AF, "4_grille": AF}),
    # After /3b_nature: the classeur's.
    (["questions-classeur-01.md"], {"3_decoupe": F, "3a_genre": F, "3b_nature": F, "4_grille": AF}),
], ids=["apres-2", "apres-3", "apres-3a", "apres-3b"])
def test_the_turn_is_read_from_the_one_file_at_the_root(tmp_path, root, expect):
    app = turn_folder(tmp_path, root)
    r = run_scan(str(app), "t")
    got = states(r["main"])
    assert {k: got[k] for k in expect} == expect
    assert got["1_lexique"] == F
    first = next(k for k, v in got.items() if v != F)
    assert r["proposal"]["step"] == first


def test_a_file_out_of_the_turn_leaves_the_step_unknown(tmp_path):
    app = turn_folder(tmp_path, ["questions-convertisseur-01.md"])
    r = run_scan(str(app), "t")
    s = step(r["main"], "3_decoupe")
    assert s["state"] == IN and s["why"][-1]["rule"] == "DEC-9"
    # The proposal never steps over an unknown step.
    assert r["proposal"]["step"] == "3_decoupe" and not r["proposal"]["proposable"]


def test_a_worktree_left_blocks_the_next_step(tmp_path):
    app = make_app(tmp_path, "premiere-app-3")
    (app / ".claude" / "worktrees" / "premiere-app-3").mkdir(parents=True)
    r = run_scan(str(app), "premiere-app-3")
    s = step(r["main"], "1_lexique")
    assert s["state"] == BL and s["why"][-1]["rule"] == "G-WT"
    assert r["alerts"][0]["rule"] == "G-WT"
    # While a run goes, the worktree is its own.
    run = {"status": "running", "command": "1_lexique", "work": "premiere-app-3", "prompt": "/1_lexique x", "started_at": ""}
    r = run_scan(str(app), "premiere-app-3", run)
    assert step(r["main"], "1_lexique")["state"] == EC and r["alerts"] == []


def test_an_unreadable_file_blocks_its_step(tmp_path):
    app = make_app(tmp_path, "premiere-app-3")
    (app / "docs" / "features" / "premiere-app-3" / "questions-lexicographe-01.md").write_bytes(b"### Q1\n\xff\xfe broken\n")
    r = run_scan(str(app), "premiere-app-3")
    s = step(r["main"], "1_lexique")
    assert s["state"] == BL and s["why"][-1]["rule"] == "G-ERR"
    assert any(a["rule"] == "G-ERR" for a in r["alerts"])


# --------------------------------------------------------- downstream

def code_folder(tmp_path, verdicts, attempts=None, defects=""):
    app = make_app(tmp_path)
    feat = app / "docs" / "features" / "c"
    (feat / "code").mkdir(parents=True)
    (feat / "desc-produit.md").write_text("# P\n", encoding="utf-8")
    (feat / "spec-technique.md").write_text("# Preamble\n\n### §1 — x\n", encoding="utf-8")
    (feat / "couverture.md").write_text("x\n", encoding="utf-8")
    bw.report(feat)
    (feat / "code" / "decoupage.md").write_text("## lot-01\n## lot-02\n## lot-03\n", encoding="utf-8")
    (feat / "code" / "sequence.md").write_text(
        "## Order\n\nlot-01, lot-02,\nlot-03\n\n## Blocks\n\nblock-1: lot-01\n\n## Defects\n\n" + defects, encoding="utf-8")
    for lot, status in verdicts.items():
        (feat / "code" / lot).mkdir()
        att = (attempts or {}).get(lot, 1)
        (feat / "code" / lot / "verdict.md").write_text(
            f"## Status\n\n{status}\n\n## Attempts\n\n{att}\n", encoding="utf-8")
    return app


def test_8_code_counts_its_lots_the_way_8_code_reads_them(tmp_path):
    app = code_folder(tmp_path, {"lot-01": "PASS", "lot-02": "PASS with reservation", "lot-03": "FAIL"})
    r = run_scan(str(app), "c")
    s = step(r["main"], "8_code")
    assert s["state"] == AF and s["lots"] == {"pass": 2, "total": 3}
    assert "2 / 3 lots en PASS" in s["why"][-1]["text"]
    assert step(r["main"], "7_lots")["state"] == F and step(r["main"], "9_controle")["state"] == AF


def test_8_code_three_failures_is_blocked(tmp_path):
    app = code_folder(tmp_path, {"lot-01": "PASS", "lot-02": "FAIL"}, attempts={"lot-02": 3})
    s = step(run_scan(str(app), "c")["main"], "8_code")
    assert s["state"] == BL and s["why"][-1]["rule"] == "COD-3"


def test_defects_send_back_to_7_lots(tmp_path):
    app = code_folder(tmp_path, {}, defects="lot-03 | hole | x\n")
    r = run_scan(str(app), "c")
    assert step(r["main"], "7_lots")["state"] == AF and step(r["main"], "7_lots")["why"][-1]["rule"] == "LOT-8"
    assert r["main_proposal"]["step"] == "7_lots"


def test_conversion_stands_or_runs(tmp_path):
    app = make_app(tmp_path)
    feat = app / "docs" / "features" / "v"
    (feat / "convertisseur").mkdir(parents=True)
    (feat / "par-genre").mkdir()
    part = "### B1 — Une course\nGenre: comportement\nNature: model\n\nTexte.\n"
    (feat / "desc-produit.md").write_text("# P\n\n" + part, encoding="utf-8")
    for g in scan.GENRE_FILES:
        (feat / "par-genre" / f"{g}.md").write_text(part if g == "comportements" else "", encoding="utf-8")
    others = "".join(f"## {n}\n\n*(none)*\n\n" for n in scan.NATURES[1:])
    (feat / "desc-par-nature.md").write_text(f"# Product file by nature\n\n## model\n\n{part}\n{others}", encoding="utf-8")
    (feat / "convertisseur" / "model-input.md").write_text(part, encoding="utf-8")
    (feat / "convertisseur" / "model.md").write_text("## model\n\nR1.\n", encoding="utf-8")
    (feat / "spec-technique.md").write_text("# Preamble\n\n### §1 — x\n", encoding="utf-8")
    (feat / "tracabilite.md").write_text("B1 → §1\n", encoding="utf-8")
    for n in ("sondeur", "existant"):
        (feat / "questions" / n).mkdir(parents=True)
        (feat / "questions" / n / f"questions-{n}-01.md").write_text("", encoding="utf-8")
    r = run_scan(str(app), "v")
    assert step(r["main"], "5_reclasse")["state"] == F
    assert step(r["main"], "6_convertit")["state"] == F and step(r["main"], "6_convertit")["why"][-1]["rule"] == "CNV-5"
    # A block changed since: the views no longer copy it, and the nature's part differs.
    (feat / "desc-produit.md").write_text("# P\n\n" + part.replace("Texte.", "Autre texte."), encoding="utf-8")
    r = run_scan(str(app), "v")
    assert step(r["main"], "5_reclasse")["why"][-1]["rule"] == "REC-6"
    assert step(r["main"], "6_convertit")["state"] == AF          # downstream of a step not done


# ------------------------------------------------------------ « Bâtir »

def batir_app(tmp_path, conventions=bw.CONVENTIONS):
    """A feature at the end of /conventions (batirworld.upstream_done)."""
    app = tmp_path / "app"
    (app / ".claude").mkdir(parents=True)
    feat = bw.upstream_done(app, conventions=conventions)
    return app, feat


def why(st):
    return st["why"][-1]


def test_the_chain_order_conventions_batir_7_lots():
    """/conventions → /batir → /7_lots, as their Next: lines draw it, and
    /7_lots sends back to /batir (scan_rules.md §1)."""
    ids = [d.id for d in scan.MAIN]
    assert ids[ids.index("conventions"):ids.index("conventions") + 3] == ["conventions", "batir", "7_lots"]
    d = next(d for d in scan.MAIN if d.id == "batir")
    assert (d.command, d.name) == ("batir", "Construire le projet")
    md = open(RULES_MD, encoding="utf-8").read()
    base = os.path.join(REPO, ".claude", "commands")
    for f, line, anchor in [("conventions.md", 317, "Next: run /batir <name>"),
                            ("batir.md", 135, "Next: run /7_lots <name>"),
                            ("batir.md", 273, "Next: run /7_lots <name>"),
                            ("7_lots.md", 97, "Next: run /batir <name>")]:
        with open(os.path.join(base, f), encoding="utf-8") as fh:
            assert anchor in fh.read().splitlines()[line - 1], (f, line)
        assert f"{f}:{line}" in md or f":{line}" in md, (f, line)


def test_batir_the_four_states(tmp_path):
    # à faire: the conventions are written, nothing built yet.
    app, feat = batir_app(tmp_path)
    r = run_scan(str(app), "premiere")
    st = step(r["main"], "batir")
    assert step(r["main"], "conventions")["state"] == F and why(step(r["main"], "conventions"))["rule"] == "CON-7"
    assert st["state"] == AF and why(st)["rule"] == "BAT-5" and st["report"] is None
    assert r["proposal"]["step"] == "batir" and r["proposal"]["proposable"]
    # The steps after it wait on it (G-AVAL).
    assert step(r["main"], "7_lots")["state"] == AF
    # faite: built from the commit that last changed the conventions.
    bw.report(feat)
    bw.profile(app)
    r = run_scan(str(app), "premiere")
    st = step(r["main"], "batir")
    assert st["state"] == F and why(st)["rule"] == "BAT-6"
    # « Pourquoi ? »: the report's status line and its commit.
    assert "« ## Status: built »" in why(st)["text"] and bw.COMMIT[:7] in why(st)["text"]
    assert why(st)["files"] == ["docs/BUILD_REPORT.md"] and "7_lots.md:87-96" in why(st)["cite"]
    assert r["proposal"]["step"] == "7_lots"
    # Once built, the report's commands and the profile's targets.
    assert [(c["name"], c["result"], c["duration"]) for c in st["report"]["commands"]] == [
        ("build", "0", "84"), ("test", "0", "31"), ("assemble app", "0", "12")]
    assert st["report"]["commands"][0]["command"] == ".\\gradlew.bat build"
    assert st["report"]["targets"] == [{"name": "Téléphone", "type": "android", "kind": "phone"}]
    # t'attend: the Bâtisseur's blocking file, unanswered.
    bw.blocked(feat)
    r = run_scan(str(app), "premiere")
    st = step(r["main"], "batir")
    assert st["state"] == A and why(st)["rule"] == "G-ATT" and why(st)["files"] == ["blocked_batisseur.md"]
    assert [(o["rel"], o["step"], o["rule"]) for o in r["opens"]] == [("blocked_batisseur.md", "batir", "OWN-BAT")]
    assert r["unknown_owner"] == [] and r["proposal"]["step"] == "batir"
    # inconnu: the commit the conventions last changed at cannot be read.
    (feat / "blocked_batisseur.md").unlink()
    r = run_scan(str(app), "premiere", conventions_commit=None)
    st = step(r["main"], "batir")
    assert st["state"] == IN and why(st)["rule"] == "BAT-9"
    assert r["proposal"]["step"] == "batir" and not r["proposal"]["proposable"]
    # inconnu: a report with no status line.
    text = (app / "docs" / "BUILD_REPORT.md").read_text(encoding="utf-8").replace("## Status: built", "")
    (app / "docs" / "BUILD_REPORT.md").write_text(text, encoding="utf-8")
    st = step(run_scan(str(app), "premiere")["main"], "batir")
    assert st["state"] == IN and why(st)["rule"] == "BAT-9"


def test_batir_again_once_the_conventions_changed(tmp_path):
    """A `built` report from an older commit: /7_lots would stop and name
    /batir (7_lots.md:97) — « à faire » again."""
    app, feat = batir_app(tmp_path)
    bw.report(feat, commit=bw.OLDER)
    r = run_scan(str(app), "premiere")
    st = step(r["main"], "batir")
    assert st["state"] == AF and why(st)["rule"] == "BAT-7"
    assert bw.OLDER[:7] in why(st)["text"] and bw.COMMIT[:7] in why(st)["text"]
    assert st["report"] is not None                       # the last build stays shown
    assert step(r["main"], "7_lots")["state"] == AF and r["proposal"]["step"] == "batir"
    # Built again on the conventions in force: done.
    bw.report(feat)
    assert step(run_scan(str(app), "premiere")["main"], "batir")["state"] == F


def test_batir_a_filled_decision_is_applied(tmp_path):
    app, feat = batir_app(tmp_path)
    bw.blocked(feat, decision="fait")
    r = run_scan(str(app), "premiere")
    st = step(r["main"], "batir")
    assert st["state"] == AF and why(st)["rule"] == "BAT-3" and r["opens"] == []


def test_conventions_without_the_three_tables(tmp_path):
    """Conventions written before the grid declared the structure:
    /conventions walks them again (conventions.md:94), /batir sends there
    (batir.md:75)."""
    app, feat = batir_app(tmp_path, conventions=bw.CONVENTIONS_OLD)
    r = run_scan(str(app), "premiere")
    con, bat = step(r["main"], "conventions"), step(r["main"], "batir")
    assert con["state"] == AF and why(con)["rule"] == "CON-8" and "G2.1 ni de G4.4 ni de G12.6" in why(con)["text"]
    assert bat["state"] == AF and why(bat)["rule"] == "BAT-2"
    assert r["proposal"]["step"] == "conventions"


# One folder per `Next:` line of batir.md (:271-278 and the stops above
# them), as the run leaves it — what the scan reads there. `Next: stop
# argument missing` leaves no folder to read.
def test_next_run_conventions_no_conventions(tmp_path):
    app, feat = batir_app(tmp_path, conventions=None)
    r = run_scan(str(app), "premiere")
    assert why(step(r["main"], "batir"))["rule"] == "BAT-1"
    assert why(step(r["main"], "conventions"))["rule"] == "CON-5" and r["proposal"]["step"] == "conventions"


def test_next_run_conventions_the_architecte_blocked(tmp_path):
    """batir.md:148-151: the Architecte blocks on the Bâtisseur's request."""
    app, feat = batir_app(tmp_path)
    bw.report(feat, status="blocked")
    bw.request(feat)
    write(feat / "blocked_architecte.md", "## Invocation\n\n3\n\n## What blocks\n\nNo conventions.\n\n"
                                          "## Where\n\nG4.4\n\n## To resume\n\nRun /conventions.\n\n## Decision\n\n")
    r = run_scan(str(app), "premiere")
    assert why(step(r["main"], "conventions"))["rule"] == "CON-3"
    assert why(step(r["main"], "batir"))["rule"] == "G-ATT"     # its blocking file: OWN-BA3
    assert r["proposal"]["step"] == "conventions"
    # The request is the Architecte's: never an entry of the form.
    assert not any(o["rel"].startswith("architecte/") for o in r["opens"])


def test_next_answer_blocking_then_batir(tmp_path):
    app, feat = batir_app(tmp_path)
    bw.report(feat, status="blocked")
    bw.blocked(feat)
    r = run_scan(str(app), "premiere")
    assert step(r["main"], "batir")["state"] == A
    assert r["proposal"] == {"chain": "main", "step": "batir", "command": "batir", "name": "Construire le projet",
                             "state": A, "proposable": True}


def test_next_run_7_lots(tmp_path):
    app, feat = batir_app(tmp_path)
    bw.report(feat)
    r = run_scan(str(app), "premiere")
    assert step(r["main"], "batir")["state"] == F
    assert r["proposal"]["step"] == "7_lots" and r["proposal"]["proposable"]


def test_batir_stays_done_once_the_split_is_cut(tmp_path):
    """/7_lots tests the build before it cuts (7_lots.md:87-97); /8_code
    never does. The conventions changed after the split: « Bâtir » faite
    (`G-AMONT`), /8_code proposed — not /batir."""
    app, feat = batir_app(tmp_path)
    bw.report(feat, commit=bw.OLDER)                      # the conventions changed since
    assert why(step(run_scan(str(app), "premiere")["main"], "batir"))["rule"] == "BAT-7"
    split(feat / "code", ["lot-01", "lot-02"])
    (feat / "code" / "lot-02" / "verdict.md").unlink()    # one lot left to code
    r = run_scan(str(app), "premiere")
    st = step(r["main"], "batir")
    assert st["state"] == F and why(st)["rule"] == "G-AMONT" and why(st)["files"] == ["code/decoupage.md"]
    assert "7_lots.md:87-97" in why(st)["cite"]
    assert step(r["main"], "7_lots")["state"] == F and step(r["main"], "8_code")["state"] == AF
    assert r["proposal"]["step"] == "8_code" and r["proposal"]["proposable"]


ARCHITECTE_BLOCKED_3 = ("## Invocation\n\n3\n\n## What blocks\n\nNo conventions.\n\n## Where\n\nG4.4\n\n"
                        "## To resume\n\nRun /conventions.\n\n## Decision\n\n")


def test_blocked_architecte_3_is_batir_before_the_split_8_code_after(tmp_path):
    """batir.md:147-151 and 8_code.md:356-362 both run invocation 3; before
    `code/decoupage.md`, /8_code cannot have run (`OWN-BA3`)."""
    app, feat = batir_app(tmp_path)
    bw.report(feat)
    write(feat / "blocked_architecte.md", ARCHITECTE_BLOCKED_3)
    r = run_scan(str(app), "premiere")
    assert [(o["rel"], o["step"], o["rule"]) for o in r["opens"]] == [("blocked_architecte.md", "batir", "OWN-BA3")]
    st = step(r["main"], "batir")
    assert st["state"] == A and why(st)["rule"] == "G-ATT" and why(st)["files"] == ["blocked_architecte.md"]
    assert step(r["main"], "8_code")["state"] == AF and r["unknown_owner"] == []
    assert r["proposal"]["step"] == "batir"
    # The split cut: /8_code's.
    split(feat / "code", ["lot-01", "lot-02"])
    (feat / "code" / "lot-02" / "verdict.md").unlink()
    r = run_scan(str(app), "premiere")
    assert [(o["rel"], o["step"], o["rule"]) for o in r["opens"]] == [("blocked_architecte.md", "8_code", "OWN-AR3")]
    assert step(r["main"], "batir")["state"] == F and step(r["main"], "8_code")["state"] == A
    assert r["proposal"]["step"] == "8_code"


def test_one_build_report_for_the_application(tmp_path):
    """The Bâtisseur's report is the application's (agents/batisseur.md
    « Where you work »), and /7_lots reads that one in a feature and in a
    `bugfix-NN/` alike (7_lots.md:87-97): no detour through /batir while
    the conventions hold."""
    import decide
    app = chain_app(tmp_path)                               # built by f's run
    assert (app / "docs" / "BUILD_REPORT.md").is_file()
    assert not (app / "docs" / "features" / "f" / "batisseur.md").exists()
    # A new feature: built already, straight to /7_lots.
    bw.upstream_done(app, "g")
    r = run_scan(str(app), "g")
    st = step(r["main"], "batir")
    assert st["state"] == F and why(st)["rule"] == "BAT-6" and why(st)["files"] == ["docs/BUILD_REPORT.md"]
    assert r["proposal"]["step"] == "7_lots"
    # A correction cycle, the conventions unchanged: /diagnostique → /7_lots.
    r = run_scan(str(app), "f")
    assert r["proposal"]["chain"] == "bugfix-02" and r["proposal"]["command"] == "7_lots"
    assert decide.decide(r, "f")["next"]["command"] == "7_lots"
    # The conventions changed since the last build: the new feature goes
    # back to /batir (BAT-7); the correction's /7_lots names it, and that
    # stored line holds against « Bâtir » closed by the split (G-AMONT).
    r = run_scan(str(app), "g", conventions_commit=bw.OLDER)
    assert why(step(r["main"], "batir"))["rule"] == "BAT-7" and r["proposal"]["step"] == "batir"
    (app / "docs" / "features" / "f" / "questions-sondeur-03.md").unlink()   # else X-AMONT, on 1_lexique
    r = run_scan(str(app), "f", conventions_commit=bw.OLDER)
    assert why(step(r["main"], "batir"))["rule"] == "G-AMONT"
    line = "Next: run /batir f"
    import nextline
    d = decide.decide(r, "f", stored={"command": "/7_lots f", "relay": line, "next": nextline.parse(line).to_dict(),
                                      "at": "2026-10-07T10:00:00", "head": None})
    assert d["source"] == "chaine" and d["dropped"] is None and d["next"]["command"] == "batir", d["dropped"]


def test_next_stop_blocked_with_nothing_waiting(tmp_path):
    app, feat = batir_app(tmp_path)
    bw.report(feat, status="blocked")
    st = step(run_scan(str(app), "premiere")["main"], "batir")
    assert st["state"] == AF and why(st)["rule"] == "BAT-8" and st["report"] is None


def test_next_stop_requests_did_not_converge(tmp_path):
    """batir.md:158-161: a fourth request, the Architecte not invoked on it."""
    app, feat = batir_app(tmp_path)
    bw.report(feat, status="blocked")
    write(feat / "architecte" / "batisseur.md", "".join(
        f"# Request {n}\n\n## What I need\n\nx\n\n## Why the lot cannot proceed\n\nx\n\n## Where I met it\n\n"
        f"G4.4\n\n## What I think it is\n\nadd\n\n## Verdict\n\n{'Added.' if n < 4 else ''}\n\n" for n in range(1, 5)))
    r = run_scan(str(app), "premiere")
    assert why(step(r["main"], "conventions"))["rule"] == "CON-3"
    assert why(step(r["main"], "batir"))["rule"] == "BAT-4"


@pytest.mark.parametrize("built", [False, True], ids=["deja-la", "sale"])
def test_next_stop_worktree(tmp_path, built):
    """`stop worktree already there` (batir.md:77) and `stop worktree dirty`
    (:235-237): the worktree stays, and blocks the first step not done."""
    app, feat = batir_app(tmp_path)
    if built:
        bw.report(feat)            # merged and pushed before the remove refused
    (app / ".claude" / "worktrees" / "premiere").mkdir(parents=True)
    r = run_scan(str(app), "premiere")
    first = "7_lots" if built else "batir"
    assert step(r["main"], first)["state"] == BL and why(step(r["main"], first))["rule"] == "G-WT"
    assert step(r["main"], "batir")["state"] == (F if built else BL)


# --------------------------------------------------------- the rules file

def _used_rule_ids():
    src = open(os.path.join(COCKPIT, "scan.py"), encoding="utf-8").read()
    used = set(re.findall(r'"((?:G|OWN|LEX|STR|DEC|GRI|REC|CNV|CON|BAT|LOT|COD|CTL|TST|FUS|DIA)-[A-Z0-9?]+)"', src))
    for prefix, n in (("DEC", (1, 2, 5, 6, 7, 9)), ("GEN", range(1, 11)), ("NAT", range(1, 11))):
        used |= {f"{prefix}-{k}" for k in n if f"{prefix}-{k}" in scan.RULES}
    return used


def test_every_rule_is_in_scan_rules_md_and_the_reverse():
    md = open(RULES_MD, encoding="utf-8").read()
    in_md = set(re.findall(r"^\| `([A-Z]+-[A-Z0-9?]+)` \|", md, re.M))
    assert _used_rule_ids() <= set(scan.RULES)
    assert set(scan.RULES) == in_md
    # And each row of the table cites what the code cites.
    for rid, cite in scan.RULES.items():
        for part in cite.split(" · "):
            m = re.match(r"^((?:agents/)?\w+\.md:\d+(?:-\d+)?)", part)
            if m:
                assert m.group(1) in md, (rid, m.group(1))


# What each cited line must still say. When a command is edited, this fails
# on the rule to derive again — the scan never silently drifts from it.
ANCHORS = {
    "G-AMONT": ["code/decoupage.md` exists → stop", "does `code/decoupage.md` exist", "cut no split"],
    "G-BUGFIX": ["highest `bugfix-NN/`", "highest `bugfix-NN/`", "highest `bugfix-NN/`", "bug-list.md"],
    "G-WT": ["git worktree add .claude/worktrees/<name> HEAD"],
    "OWN-Q": ["then run /1_lexique"], "OWN-LEX": ["then run /1_lexique"], "OWN-RED1": ["then run /2_structure"],
    "OWN-RE3": ["says 3"], "OWN-DEC": ["then run /2_structure"], "OWN-GEN": ["then run /3a_genre"],
    "OWN-NAT": ["then run /3b_nature"], "OWN-GRI": ["then run /4_grille"],
    "OWN-TEC": ["then run /6_convertit", "then run /6_convertit"], "OWN-CNV": ["then run /6_convertit"],
    "OWN-ARC": ["then run /conventions"], "OWN-ARB": ["then run /conventions"], "OWN-AR3": ["blocked_architecte.md"],
    "OWN-BA3": ["`blocked_architecte.md` at the working folder's root → stop"],
    "OWN-BAT": ["then run /batir", "then run /batir"],
    "OWN-CAD": ["then run /7_lots"], "OWN-RED": ["then run /7_lots"],
    "OWN-COD": ["then run /8_code", "then run /8_code"], "OWN-FUS": ["then run /fusion"], "OWN-FUB": ["blocked_fusionneur.md"],
    "OWN-DIA": ["then run /diagnostique", "then run /diagnostique"],
    "LEX-1": ["It stops 1"], "LEX-2": ["Sweeping"], "LEX-3": ["the loop ended"], "LEX-4": ["Settling"],
    "LEX-5": ["Watching"], "LEX-6": ["filing failed", "filing failed"], "LEX-7": ["nothing to watch"],
    "LEX-8": ["3 asked nothing"], "LEX-9": ["Correcting"],
    "STR-1": ["Next: run"], "STR-2": ["is filled"], "STR-3": ["More than one questions file"],
    "STR-4": ["Integrating"], "STR-5": ["every `## Decision` filled"], "STR-6": ["nothing to integrate"],
    "STR-7": ["Structuring"], "STR-8": ["Clarification needed"], "STR-9": ["/3_decoupe"],
    "DEC-0": ["/2_structure"], "DEC-1": ["Clarification needed"], "DEC-2": ["waits"], "DEC-3": ["desc-produit.md"],
    "DEC-4": ["no `questions-sondeur-*.md` anywhere", "invoke nothing"],
    "DEC-5": ["git mv", "git mv", "git mv", "git mv"], "DEC-6": ["git mv"], "DEC-7": ["git mv", "even empty"],
    "GEN-1": ["Clarification needed"], "GEN-2": ["waits"], "GEN-3": ["Genre:", "Structuring"],
    "GEN-4": ["do not invoke"], "GEN-5": ["git mv", "git mv", "questions file on every run"],
    "GEN-6": ["git mv"], "GEN-7": ["git mv"], "GEN-8": ["^Genre:$"], "GEN-10": ["third trigger", "Name it in the prompt"],
    "NAT-1": ["Clarification needed"], "NAT-2": ["waits"], "NAT-3": ["^Nature:$", "Structuring"],
    "NAT-4": ["do not invoke"], "NAT-5": ["git mv", "questions file on every run"], "NAT-6": ["git mv"], "NAT-7": ["git mv"],
    "NAT-8": ["^Nature:$"], "NAT-10": ["third trigger", "Name it in the prompt"],
    "GRI-0": ["Genre: comportement", "Structuring"], "GRI-1": ["Clarification needed"], "GRI-2": ["/3b_nature"],
    "GRI-4": ["grid has to have closed", "second time is over"], "GRI-5": ["no behaviour block"], "GRI-6": ["closes the first time"],
    "REC-1": ["grid has to have closed"], "REC-2": ["^Genre:$"], "REC-3": ["/3b_nature"], "REC-4": ["waits"],
    "REC-5": ["par-genre/` absent"], "REC-6": ["copied", "count"], "REC-7": ["Six files", "desc-par-nature.md"],
    "CNV-2": ["par-genre/` absent"], "CNV-3": ["waits"], "CNV-4": ["Runs nowhere"], "CNV-5": ["Nothing to write"],
    "CNV-6": ["Skip to the assembly"],
    "CON-1": ["spec-technique.md` is absent"], "CON-2": ["filled"], "CON-3": ["Requests"], "CON-4": ["Integrating"],
    "CON-5": ["Deriving"], "CON-6": ["Completing"], "CON-7": ["/batir"], "CON-8": ["one of the three greps"],
    "BAT-1": ["No `docs/TECHNICAL_CONVENTIONS.md`"], "BAT-2": ["It lacks G2.1's, G4.4's or G12.6's table"],
    "BAT-3": ["is filled"], "BAT-4": ["opens the run on the Architecte"], "BAT-5": ["No `docs/BUILD_REPORT.md`"],
    "BAT-6": ["`## Status: built`, and the same commit", "The skeleton holds"], "BAT-7": ["another commit"],
    "BAT-8": ["nothing above", "`## Status: blocked`"],
    "LOT-1": ["spec-technique.md` or `desc-bug.md`", "the technical document has to be there"], "LOT-2": ["/fusion"], "LOT-3": ["blocked_verificateur.md"],
    "LOT-4": ["redecoupage.md"], "LOT-5": ["filled"], "LOT-6": ["Once the split holds"], "LOT-7": ["The split holds"],
    "LOT-8": ["/7_lots", "carries lines"], "LOT-9": ["first split"],
    "COD-1": ["PASS"], "COD-2": ["/7_lots"], "COD-3": ["reaching 3"], "COD-5": ["/9_controle"], "COD-6": ["PASS"],
    "CTL-1": ["desc-produit.md"], "CTL-3": ["four files", "four files"], "CTL-4": ["four files"],
    "TST-1": ["rapport-fusion.md"], "TST-2": ["décider d'une"], "TST-3": ["bug-list.md"], "TST-4": ["décider d'une"],
    "FUS-1": ["desc-produit.md"], "FUS-2": ["rapport-fusion.md"], "FUS-3": ["Rédacteur"],
    "DIA-1": ["bug-list.md"], "DIA-2": ["desc-bug.md", "desc-bug.md"], "DIA-3": ["Sort every gap"],
}


def test_each_cited_line_still_says_what_the_rule_reads():
    base = os.path.join(REPO, ".claude")
    for rid, cite in scan.RULES.items():
        parts = [p for p in cite.split(" · ") if re.match(r"^(?:agents/)?\w+\.md:\d", p)]
        if not parts:
            continue
        anchors = ANCHORS[rid]
        assert len(anchors) == len(parts), rid
        for part, anchor in zip(parts, anchors):
            m = re.match(r"^((?:agents/)?\w+\.md):(\d+)(?:-(\d+))?", part)
            f, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            path = os.path.join(base, f if f.startswith("agents/") else os.path.join("commands", f))
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            assert b <= len(lines), (rid, part)
            assert anchor in "\n".join(lines[a - 1:b]), (rid, part, anchor)


# 1.5 — code_rules.md and codelots.RULES: the same check, the same way.
CODE_RULES_MD = os.path.join(COCKPIT, "code_rules.md")
CODE_ANCHORS = {
    "L-ORDRE": ["the order, the blocks", "## Blocks"],
    "L-TITRE": ["Anchor:"],
    "E-PASSE": ["starts with `PASS`", "PASS with reservation"],
    "E-ECHOUE": ["On FAIL"],
    "E-TROIS": ["reaching 3 stops the lot"],
    "E-ANNULE": ["reverted the", "reverts the"],
    "E-BLOQUE": ["blocked_*.md", "three places"],
    "E-REDEC": ["## Ce qui ne l'est pas", "## Ce qui revient", "`## Redécoupage: archivable`", "carries lines",
                "block standing"],
    "E-ENTAME": ["No `code/<lot>/fiche-executable.md`", "skipped when"],
    "E-AFAIRE": ["No `code/<lot>/fiche-executable.md`"],
    "E-ENCOURS": ["Name the lot", "The next lot is the first"],
    "T-ESSAIS": ["reaching 3", "read it as 1", "empty first\nattempt", "plus\none"],
    "P-ORDRE": ["`detailleur`", "`concepteur`", "`relecteur`"],
    "P-ECRIT": ["fiche-executable.md", "code/<lot>/verdict.md", "conception.md", "compte-rendu.md"],
    "P-ARBITRE": ["call it themselves", "Settle <lot>", "Settle <block>", "the concepteur, the testeur"],
    "P-ARCHITECTE": ["invocation 3", "Called by the Arbitre"],
    "P-DEMANDES": ["architecte/concepteur-<lot>.md", "architecte/realisateur-<lot>.md",
                   "architecte/detailleur-<lot>.md", "first lot of the block", "arbitre-<lot>-blocking-N.md"],
    "B-OU": ["three places", "## Blocking N — lot-NN"],
    "C-GREP": ["<working folder>/<lot>: <what the commit\ncarries>", "<base>..HEAD | grep -E", "last revert"],
    "C-DOSSIER": ["Lot names are reused by every split", "that added the current `code/decoupage.md`", "never `--grep`",
                  "`<working folder>` is the folder the prompt gives", "`<working folder>` is the folder",
                  "never by what a commit stages"],
    "W-LIVE": ["git worktree add .claude/worktrees/<name> HEAD", "One worktree for the whole run",
               "she opens the worktree"],
    "A-LOT": ["Name the lot", "Your lot: <lot>", "Your lot: <lot>", "Your lot: <lot>", "Your lot: <lot>",
              "Your lot: <lot>"],
    "A-DESC": ['"Declare <lot>"', '"Test <lot>"', '"Code <lot>"', '"Review <lot>"', "Settle <lot>"],
    "A-BLOC": ["Your block: <block>", "Your block: <block>", "Settle <block>"],
    "A-DOSSIER": ["Pass the working folder"],
    "A-AUCUN": ["Invocation 3 — Requests"],
    "A-IMBRIQUE": ['subagent_type="arbitre"', 'subagent_type="architecte"'],
}


def _cite_parts(cite):
    return [p for p in cite.split(" · ") if re.match(r"^(?:agents/)?\w+\.md:\d", p)]


def test_every_code_rule_is_in_code_rules_md_and_cites_what_the_code_cites():
    import codelots
    md = open(CODE_RULES_MD, encoding="utf-8").read()
    in_md = set(re.findall(r"`([A-Z]-[A-Z]+)`", md))
    assert set(codelots.RULES) <= in_md
    src = open(os.path.join(COCKPIT, "codelots.py"), encoding="utf-8").read()
    used = set(re.findall(r'"([A-Z]-[A-Z]+)"', src))
    assert used <= set(codelots.RULES) | {"L-ORDRE"}, used - set(codelots.RULES)
    for rid, cite in codelots.RULES.items():
        for part in _cite_parts(cite):
            assert part in md, (rid, part)


def test_each_code_rule_cited_line_still_says_what_the_rule_reads():
    import codelots
    base = os.path.join(REPO, ".claude")
    for rid, cite in codelots.RULES.items():
        parts = _cite_parts(cite)
        if not parts:
            continue
        anchors = CODE_ANCHORS[rid]
        assert len(anchors) == len(parts), rid
        for part, anchor in zip(parts, anchors):
            m = re.match(r"^((?:agents/)?\w+\.md):(\d+)(?:-(\d+))?", part)
            f, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            path = os.path.join(base, f if f.startswith("agents/") else os.path.join("commands", f))
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            assert b <= len(lines), (rid, part)
            assert anchor in "\n".join(lines[a - 1:b]), (rid, part, anchor)


def test_confirmations_match_the_flagged_commands_of_scan_rules_md():
    md = open(RULES_MD, encoding="utf-8").read()
    flagged = set(re.findall(r"^\| `/(\w+)` \| ⚠️", md, re.M))
    assert flagged == set(scan.CONFIRM)
