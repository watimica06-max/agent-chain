"""Cockpit 1.3, §1 — the scan, on real copies of three features and on
small folders built for one rule each. Reads only: no command runs."""
import os
import re
import shutil
import time

import pytest

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
    (app / "docs" / "TECHNICAL_CONVENTIONS.md").write_text("# Conventions\n", encoding="utf-8")
    for f in features:
        shutil.copytree(os.path.join(FEATURES, f), app / "docs" / "features" / f)
    return app


def states(steps):
    return {s["id"]: s["state"] for s in steps}


def step(steps, sid):
    return next(s for s in steps if s["id"] == sid)


def corr(r, name):
    return next(c for c in r["corrections"] if c["name"] == name)


# ------------------------------------------------- the three real features

def test_premiere_app_main_and_corrections(tmp_path):
    app = make_app(tmp_path, "premiere-app")
    r = scan.run_scan(str(app), "premiere-app")
    assert states(r["main"]) == {
        # 190 unanswered questions of a sondeur file left at the root: 1_lexique stops on them.
        "1_lexique": A,
        # The split is cut: the upstream is closed (6_convertit.md:35-38).
        "2_structure": F, "3_decoupe": F, "3a_genre": F, "3b_nature": F,
        "4_grille": F, "5_reclasse": F, "6_convertit": F,
        "conventions": F, "7_lots": F, "8_code": F,
        # A correction is open: the feature was controlled and tested (9_controle.md:512-513).
        "9_controle": F, "test": F,
        "fusion": AF,
    }
    assert step(r["main"], "8_code")["lots"] == {"pass": 45, "total": 45}
    assert [c["name"] for c in r["corrections"]] == [f"bugfix-0{n}" for n in range(7, 0, -1)]
    assert states(corr(r, "bugfix-07")["steps"]) == {"diagnostique": F, "7_lots": AF, "8_code": AF, "9_controle": AF}
    assert states(corr(r, "bugfix-06")["steps"]) == {"diagnostique": F, "7_lots": F, "8_code": F, "9_controle": AF}
    assert step(corr(r, "bugfix-06")["steps"], "8_code")["lots"] == {"pass": 55, "total": 55}
    for old in ("bugfix-05", "bugfix-04", "bugfix-03"):
        # Their `## Defects` holds « None. »: a line, by 7_lots.md:208's own test.
        assert states(corr(r, old)["steps"]) == {"diagnostique": F, "7_lots": AF, "8_code": AF, "9_controle": AF}
    for old in ("bugfix-02", "bugfix-01"):
        assert states(corr(r, old)["steps"]) == {"diagnostique": F, "7_lots": F, "8_code": F, "9_controle": AF}
    # The highest correction is open: the dashboard proposes it, the main chain keeps its own.
    assert r["proposal"] == {"chain": "bugfix-07", "step": "7_lots", "command": "7_lots",
                             "name": "Découper en lots", "state": AF, "proposable": True}
    assert r["main_proposal"]["step"] == "1_lexique" and r["main_proposal"]["state"] == A
    assert len([o for o in r["opens"] if o["step"] == "1_lexique"]) == 190
    assert r["alerts"] == [] and r["unknown_owner"] == []


def test_premiere_app_2(tmp_path):
    app = make_app(tmp_path, "premiere-app-2")
    r = scan.run_scan(str(app), "premiere-app-2")
    assert states(r["main"]) == {
        "1_lexique": A,          # questions-classeur-01.md: four questions, no answer
        "2_structure": AF,       # that file, once answered, is the one to integrate
        "3_decoupe": AF, "3a_genre": AF, "3b_nature": AF,   # each stops on a root file holding questions
        "4_grille": BL,          # no `Genre: comportement` in a product file written before genres
        "5_reclasse": AF, "6_convertit": AF, "conventions": AF, "7_lots": AF,
        "8_code": AF, "9_controle": AF, "test": AF, "fusion": AF,
    }
    assert r["corrections"] == []
    assert r["proposal"]["step"] == "1_lexique" and r["proposal"]["state"] == A


def test_premiere_app_3(tmp_path):
    app = make_app(tmp_path, "premiere-app-3")
    r = scan.run_scan(str(app), "premiere-app-3")
    assert states(r["main"]) == {
        "1_lexique": A,          # questions-lexicographe-01.md: eight entries still open
        "2_structure": AF, "3_decoupe": AF, "3a_genre": AF, "3b_nature": AF, "4_grille": AF,
        "5_reclasse": AF, "6_convertit": AF, "conventions": AF, "7_lots": AF,
        "8_code": AF, "9_controle": AF, "test": AF, "fusion": AF,
    }
    assert len(r["opens"]) == 8
    assert r["proposal"]["step"] == "1_lexique"


def test_scan_under_a_second_on_premiere_app(tmp_path):
    app = make_app(tmp_path, "premiere-app")
    t0 = time.perf_counter()
    scan.run_scan(str(app), "premiere-app")
    assert time.perf_counter() - t0 < 1.0
    live = os.path.join(REPO, "docs", "features", "premiere-app")
    if os.path.isdir(live):                         # the repository's own copy, as the cockpit reads it
        t0 = time.perf_counter()
        scan.run_scan(REPO, "premiere-app")
        assert time.perf_counter() - t0 < 1.0


# ---------------------------------------------- « Pourquoi ? », per state

def test_why_names_the_rule_and_the_files_for_each_state(tmp_path):
    app = make_app(tmp_path, "premiere-app", "premiere-app-2", "premiere-app-3")
    r1 = scan.run_scan(str(app), "premiere-app")
    r2 = scan.run_scan(str(app), "premiere-app-2")
    r3 = scan.run_scan(str(app), "premiere-app-3")
    run = {"status": "running", "command": "1_lexique", "work": "premiere-app-3",
           "prompt": "/1_lexique premiere-app-3", "started_at": "2026-10-05T10:00:00"}
    r4 = scan.run_scan(str(app), "premiere-app-3", run)
    cases = [
        (step(r1["main"], "conventions"), F, "CON-7", ["couverture.md"], "conventions.md:86-88"),
        (step(r2["main"], "1_lexique"), A, "G-ATT", ["questions-classeur-01.md"], "« À qui est une réponse »"),
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
    # After /2_structure: the Rédacteur's file at the root (agents/redacteur.md:275).
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
    r = scan.run_scan(str(app), "t")
    got = states(r["main"])
    assert {k: got[k] for k in expect} == expect
    assert got["1_lexique"] == F
    first = next(k for k, v in got.items() if v != F)
    assert r["proposal"]["step"] == first


def test_a_file_out_of_the_turn_leaves_the_step_unknown(tmp_path):
    app = turn_folder(tmp_path, ["questions-analyste-01.md"])
    r = scan.run_scan(str(app), "t")
    s = step(r["main"], "3_decoupe")
    assert s["state"] == IN and s["why"][-1]["rule"] == "DEC-9"
    # The proposal never steps over an unknown step.
    assert r["proposal"]["step"] == "3_decoupe" and not r["proposal"]["proposable"]


def test_a_worktree_left_blocks_the_next_step(tmp_path):
    app = make_app(tmp_path, "premiere-app-3")
    (app / ".claude" / "worktrees" / "premiere-app-3").mkdir(parents=True)
    r = scan.run_scan(str(app), "premiere-app-3")
    s = step(r["main"], "1_lexique")
    assert s["state"] == BL and s["why"][-1]["rule"] == "G-WT"
    assert r["alerts"][0]["rule"] == "G-WT"
    # While a run goes, the worktree is its own.
    run = {"status": "running", "command": "1_lexique", "work": "premiere-app-3", "prompt": "/1_lexique x", "started_at": ""}
    r = scan.run_scan(str(app), "premiere-app-3", run)
    assert step(r["main"], "1_lexique")["state"] == EC and r["alerts"] == []


def test_an_unreadable_file_blocks_its_step(tmp_path):
    app = make_app(tmp_path, "premiere-app-3")
    (app / "docs" / "features" / "premiere-app-3" / "questions-lexicographe-01.md").write_bytes(b"### Q1\n\xff\xfe broken\n")
    r = scan.run_scan(str(app), "premiere-app-3")
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
    r = scan.run_scan(str(app), "c")
    s = step(r["main"], "8_code")
    assert s["state"] == AF and s["lots"] == {"pass": 2, "total": 3}
    assert "2 / 3 lots en PASS" in s["why"][-1]["text"]
    assert step(r["main"], "7_lots")["state"] == F and step(r["main"], "9_controle")["state"] == AF


def test_8_code_three_failures_is_blocked(tmp_path):
    app = code_folder(tmp_path, {"lot-01": "PASS", "lot-02": "FAIL"}, attempts={"lot-02": 3})
    s = step(scan.run_scan(str(app), "c")["main"], "8_code")
    assert s["state"] == BL and s["why"][-1]["rule"] == "COD-3"


def test_defects_send_back_to_7_lots(tmp_path):
    app = code_folder(tmp_path, {}, defects="lot-03 | hole | x\n")
    r = scan.run_scan(str(app), "c")
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
    r = scan.run_scan(str(app), "v")
    assert step(r["main"], "5_reclasse")["state"] == F
    assert step(r["main"], "6_convertit")["state"] == F and step(r["main"], "6_convertit")["why"][-1]["rule"] == "CNV-5"
    # A block changed since: the views no longer copy it, and the nature's part differs.
    (feat / "desc-produit.md").write_text("# P\n\n" + part.replace("Texte.", "Autre texte."), encoding="utf-8")
    r = scan.run_scan(str(app), "v")
    assert step(r["main"], "5_reclasse")["why"][-1]["rule"] == "REC-6"
    assert step(r["main"], "6_convertit")["state"] == AF          # downstream of a step not done


# --------------------------------------------------------- the rules file

def _used_rule_ids():
    src = open(os.path.join(COCKPIT, "scan.py"), encoding="utf-8").read()
    used = set(re.findall(r'"((?:G|OWN|LEX|STR|DEC|GRI|REC|CNV|CON|LOT|COD|CTL|TST|FUS|DIA)-[A-Z0-9?]+)"', src))
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
    "G-AMONT": ["code/decoupage.md` exists → stop", "does `code/decoupage.md` exist"],
    "G-BUGFIX": ["highest `bugfix-NN/`", "highest `bugfix-NN/`", "highest `bugfix-NN/`", "bug-list.md"],
    "G-WT": ["git worktree add .claude/worktrees/<name> HEAD"],
    "OWN-Q": ["then run /1_lexique"], "OWN-LEX": ["then run /1_lexique"], "OWN-RED1": ["then run /2_structure"],
    "OWN-RE3": ["says 3"], "OWN-DEC": ["then run /2_structure"], "OWN-GEN": ["then run /3a_genre"],
    "OWN-NAT": ["then run /3b_nature"], "OWN-GRI": ["then run /4_grille"],
    "OWN-TEC": ["then run /6_convertit", "then run /6_convertit"], "OWN-CNV": ["then run /6_convertit"],
    "OWN-ARC": ["then run /conventions"], "OWN-ARB": ["then run /conventions"], "OWN-AR3": ["blocked_architecte.md"],
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
    "CON-5": ["Deriving"], "CON-6": ["Completing"], "CON-7": ["/7_lots"],
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
    "E-REDEC": ["back\nto the split", "with no PASS"],
    "E-ENTAME": ["No `code/<lot>/fiche-executable.md`", "skipped when"],
    "E-AFAIRE": ["No `code/<lot>/fiche-executable.md`"],
    "E-ENCOURS": ["Name the lot", "The next lot is the first"],
    "T-ESSAIS": ["reaching 3", "read it as 1", "empty first\nattempt", "plus\none"],
    "P-ORDRE": ["`detailleur`", "`concepteur`", "`relecteur`"],
    "P-ECRIT": ["fiche-executable.md", "code/<lot>/verdict.md", "conception.md", "compte-rendu.md"],
    "P-ARBITRE": ["call it themselves", "Settle <lot>", "Settle <block>"],
    "P-ARCHITECTE": ["invocation 3", "Called by the Arbitre"],
    "P-DEMANDES": ["architecte/concepteur-<lot>.md", "architecte/realisateur-<lot>.md",
                   "architecte/detailleur-<lot>.md", "first lot of the block", "arbitre-<lot>-blocking-N.md"],
    "B-OU": ["three places", "## Blocking N — lot-NN"],
    "C-GREP": ["<working folder>/<lot>: <what the commit\ncarries>", "last revert"],
    "C-DOSSIER": ["code/<lot>/conception.md", "your report", "Write the report"],
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
