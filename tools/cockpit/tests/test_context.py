"""Cockpit 1.4 — what a question is about (context.py, context_rules.md).
For each writer, a fixture question resolves to the right passage of a
fixture document."""
import os
import re

import pytest

import context
import questions

HERE = os.path.dirname(os.path.abspath(__file__))
COCKPIT = os.path.dirname(HERE)
CLAUDE = os.path.join(COCKPIT, "..", "..", ".claude")

PRODUCT = """# Produit

# Domain: Course

## Structure

### B1 — Une course
Genre: comportement

La course compte huit ateliers et un sas.

### B7 — Rejeter les durées nulles    MODIFIED
Genre: comportement

Une durée nulle est refusée.
- Le message dit pourquoi.

### B12 — L'heure de départ
Texte.
"""

TECH = """# Technical document

## §1 Model

### §1.1 Race structure
Rule one.

### §3.2 Reconciling two real entries
Rule two.
- detail

## §4 Other
"""

IDEAS = """# Idées

Chaque atelier a un nom. La STATION finale est la course.
Un Atelier peut être sauté ; les ateliers suivants restent.
"""


def q(qid=1, key="Block: B7"):
    return f"### Q{qid}\n{key}\nQuestion: what?\nOptions:\n- Oui, une option.\n- Non, une autre.\nAnswer:\n"


@pytest.fixture
def feat(tmp_path):
    f = tmp_path / "feat"
    (f / "convertisseur").mkdir(parents=True)
    (f / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
    (f / "desc-produit-fusion.md").write_text(PRODUCT.replace("Rejeter", "Refuser"), encoding="utf-8")
    (f / "spec-technique.md").write_text(TECH, encoding="utf-8")
    (f / "convertisseur" / "model.md").write_text(TECH, encoding="utf-8")
    (f / "idees.md").write_text(IDEAS, encoding="utf-8")
    return f


def entries(path, base):
    return questions.parse_file(str(path), str(base)).entries


def resolve_one(path, base, n=0):
    return context.resolve(entries(path, base)[n], str(base))


@pytest.mark.parametrize("agent,rule,doc", [
    ("redacteur", "CTX-RED", "desc-produit.md"),
    ("qualifieur", "CTX-GEN", "desc-produit.md"),
    ("classeur", "CTX-NAT", "desc-produit.md"),
    ("sondeur", "CTX-GRI", "desc-produit.md"),
    ("existant", "CTX-EXI", "desc-produit.md"),
    ("convertisseur", "CTX-CNV", "desc-produit.md"),
    ("fusionneur", "CTX-FUS", "desc-produit-fusion.md"),
])
def test_a_block_question_points_to_its_block(feat, agent, rule, doc):
    p = feat / f"questions-{agent}-01.md"
    p.write_text(q(1, "Block: B7, B12"), encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["status"] == "ok" and r["rule"] == rule and r["doc"] == doc and r["kind"] == "block"
    lines = r["lines"]
    b7, b12 = r["matches"]
    assert lines[b7["start"]].startswith("### B7 — ") and b7["label"] == "B7"
    # The whole block, down to the next heading, trailing blank lines left out.
    assert lines[b7["end"]] == "- Le message dit pourquoi."
    assert lines[b12["start"]].startswith("### B12") and lines[b12["end"]] == "Texte."
    if agent == "fusionneur":
        assert "Refuser" in lines[b7["start"]]          # desc-produit-fusion.md, never desc-produit.md


def test_lexicographe_alone_points_to_every_occurrence_in_idees(feat):
    p = feat / "questions-lexicographe-01.md"
    p.write_text(q(1, "Terms: atelier, STATION"), encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["rule"] == "CTX-LEX12" and r["doc"] == "idees.md" and r["kind"] == "terms"
    got = [(m["line"], r["lines"][m["line"]][m["start"]:m["end"]]) for m in r["matches"]]
    # Whole words, any case: « ateliers » is not « atelier ».
    assert got == [(2, "atelier"), (2, "STATION"), (3, "Atelier")]
    assert r["missing"] == []


def test_lexicographe_beside_an_answered_file_points_into_its_answers(feat):
    (feat / "questions-sondeur-02.md").write_text(
        "### Q1\nBlock: B1\nQuestion: is the atelier timed?\nAnswer: Oui, chaque atelier est chronométré.\n\n"
        "### Q2\nBlock: B7\nQuestion: and the atelier after?\nDéfaut: L'atelier suivant attend. — B7\nAnswer:\n\n"
        "### Q3\nBlock: B12\nQuestion: atelier?\nDéfaut: Un atelier refusé. — B12\nAnswer: Non.\n",
        encoding="utf-8")
    p = feat / "questions-lexicographe-02.md"
    p.write_text(q(1, "Terms: atelier"), encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["rule"] == "CTX-LEX34" and r["doc"] == "questions-sondeur-02.md"
    hit_lines = [r["lines"][m["line"]] for m in r["matches"]]
    # The Answer: fields, and the Défaut: of the empty one; never a Question:,
    # never the Défaut: an answer refused.
    assert hit_lines == ["Answer: Oui, chaque atelier est chronométré.", "Défaut: L'atelier suivant attend. — B7"]


def test_lexicographe_beside_two_other_files_has_no_context(feat):
    for a in ("sondeur", "redacteur"):
        (feat / f"questions-{a}-01.md").write_text(q(), encoding="utf-8")
    p = feat / "questions-lexicographe-02.md"
    p.write_text(q(1, "Terms: atelier"), encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["status"] == "none" and "deux fichiers" in r["reason"]


def test_architecte_points_to_entries_of_the_technical_document(feat):
    p = feat / "questions-architecte-01.md"
    p.write_text("### Q1\nBlock: §3.2 — Reconciling two real entries\nKind: conjunction\nQuestion: which?\nAnswer:\n",
                 encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["rule"] == "CTX-ARC" and r["doc"] == "spec-technique.md" and r["ids"] == ["§3.2"]
    (m,) = r["matches"]
    assert r["lines"][m["start"]] == "### §3.2 Reconciling two real entries" and r["lines"][m["end"]] == "- detail"


def test_technical_question_points_to_its_own_section(feat):
    p = feat / "convertisseur" / "technique-model.md"
    p.write_text("### Q1\nEntries: §1.1, [B12: recorded start time]\nQuestion: which?\nAnswer:\n", encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["rule"] == "CTX-TEC" and r["doc"] == "convertisseur/model.md"
    assert [x["label"] for x in r["matches"]] == ["§1.1"] and r["outside"] == ["[B12: recorded start time]"]
    t = feat / "convertisseur" / "technique-transversal.md"
    t.write_text("### Q1\nEntries: §3.2\nQuestion: which?\nAnswer:\n", encoding="utf-8")
    assert resolve_one(t, feat)["doc"] == "spec-technique.md"


def test_a_target_not_found_is_said(feat):
    p = feat / "questions-redacteur-01.md"
    p.write_text(q(1, "Block: B99"), encoding="utf-8")
    r = resolve_one(p, feat)
    assert r["status"] == "notfound" and r["matches"] == [] and r["reason"] == "B99 introuvable dans desc-produit.md"
    p2 = feat / "questions-lexicographe-01.md"
    p.unlink()
    p2.write_text(q(1, "Terms: vélo"), encoding="utf-8")
    r = resolve_one(p2, feat)
    assert r["status"] == "notfound" and "aucune occurrence de vélo dans idees.md" == r["reason"]
    (feat / "idees.md").unlink()
    r = resolve_one(p2, feat)
    assert r["status"] == "missing" and "idees.md n'existe pas" in r["reason"]


def test_block_dash_and_unknown_writers_have_no_context(feat):
    p = feat / "questions-sondeur-01.md"
    p.write_text(q(1, "Block: -"), encoding="utf-8")
    assert resolve_one(p, feat)["status"] == "none"
    a = feat / "questions-analyste-01.md"
    p.unlink()
    a.write_text(q(), encoding="utf-8")
    r = resolve_one(a, feat)
    assert r["status"] == "none" and r["rule"] == "CTX-?"


def test_resolve_never_writes(feat):
    p = feat / "questions-redacteur-01.md"
    p.write_text(q(), encoding="utf-8")
    before = {f: os.path.getmtime(f) for f in feat.rglob("*") if f.is_file()}
    context.resolve(entries(p, feat)[0], str(feat))
    assert before == {f: os.path.getmtime(f) for f in feat.rglob("*") if f.is_file()}


# -------------------------------------------------- context_rules.md holds

RULES = open(os.path.join(COCKPIT, "context_rules.md"), encoding="utf-8").read()

# What each cited line must still say.
SAYS = {
    "agents/lexicographe.md:311": "Terms:", "agents/lexicographe.md:318": "`Terms:` carries the terms",
    "agents/lexicographe.md:103": "The idea file", "commands/1_lexique.md:158": "idees.md",
    "agents/lexicographe.md:539": "Terms:", "agents/lexicographe.md:440": "You sweep the `Answer:` fields",
    "agents/lexicographe.md:445": "Such a line is an answer", "commands/1_lexique.md:62": "Another agent's, and `questions-lexicographe`",
    "commands/1_lexique.md:65": "the answered file", "commands/1_lexique.md:63": "Two files of other agents",
    "agents/redacteur.md:289": "Block: B7", "agents/redacteur.md:34": "`desc-produit.md`",
    "agents/redacteur.md:312": "Identifiers only", "agents/redacteur.md:318": "`Block: -` when the question is about the feature",
    "agents/qualifieur.md:197": "Block: B40", "agents/qualifieur.md:204": "`Block:` carries the identifier alone",
    "commands/3a_genre.md:169": "desc-produit.md", "agents/classeur.md:148": "Block: B40",
    "agents/classeur.md:155": "`Block:` carries the identifier alone", "commands/3b_nature.md:171": "desc-produit.md",
    "agents/sondeur.md:395": "Block: B7", "agents/sondeur.md:450": "the title is in the product file",
    "agents/assembleur.md:140": "`Block:` carries identifiers", "agents/assembleur.md:142": "not of a block",
    "commands/4_grille.md:568": "Copy `cadrage-produit/questions.md`", "commands/4_grille.md:388": "desc-produit.md",
    "agents/sondeur.md:276": "names the feature's block", "agents/sondeur.md:277": "never a block of the global",
    "commands/4_grille.md:395": "questions-existant-NN.md", "agents/sondeur.md:461": "`Block: -` for a pass C question",
    "agents/convertisseur.md:439": "Block: B7", "agents/convertisseur.md:450": "`Block:` names the blocks the answer will change",
    "agents/convertisseur.md:57": "`desc-produit.md`", "commands/6_convertit.md:355": "questions-convertisseur-NN.md",
    "commands/6_convertit.md:367": "Every entry copied as written", "agents/convertisseur.md:390": "Entries: §3.2",
    "agents/convertisseur.md:399": "`Entries:` names the entries", "agents/convertisseur.md:401": "inside your section",
    "agents/convertisseur.md:59": "`convertisseur/<nature>.md`", "agents/convertisseur.md:65": "`spec-technique.md`",
    "agents/convertisseur.md:299": "A reference inside your section is its number",
    "agents/convertisseur.md:300": "outside it is the block",
    "agents/architecte.md:547": "Block: §3.2", "agents/architecte.md:337": "`spec-technique.md`",
    "agents/architecte.md:582": "its `Block:`", "agents/fusionneur.md:116": "Block: B7",
    "agents/fusionneur.md:47": "`desc-produit-fusion.md`", "agents/fusionneur.md:174": "The title line",
}


def test_each_cited_line_still_says_what_the_rule_reads():
    cited = set(re.findall(r"((?:agents|commands)/[\w-]+\.md:\d+)", RULES))
    assert cited == set(SAYS), (cited ^ set(SAYS))
    for cite, words in SAYS.items():
        path, n = cite.rsplit(":", 1)
        with open(os.path.join(CLAUDE, *path.split("/")), encoding="utf-8") as f:
            line = f.read().splitlines()[int(n) - 1]
        assert words in line, (cite, line)


def test_every_rule_of_the_code_is_in_context_rules_md():
    code = open(os.path.join(COCKPIT, "context.py"), encoding="utf-8").read()
    used = set(re.findall(r'"(CTX-[A-Z0-9?]+)"', code)) - {"CTX-?"}
    in_md = set(re.findall(r"`(CTX-[A-Z0-9?]+)`", RULES))
    assert used and used <= in_md, used - in_md
