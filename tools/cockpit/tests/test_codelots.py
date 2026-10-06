"""Cockpit 1.5 — the « Code » tab's reader (codelots.py, code_rules.md).

Real files first: the frozen copies of premiere-app and its bugfix-NN/
(tests/fixtures/features/). They are in an older shape than the current
8_code.md: three-field verdicts (no `## Attempts`, `## Findings`…), no
`conception.md` / `tests.md`, no `Round:` line, the Détailleur's blocking
files in the lot's folder — and every lot PASS. Every other state is a
hand-written folder following the templates of the command and its agents
(verificateur.md:107-115, cadreur.md:848-854, relecteur.md:140-170,
detailleur.md:328-352, arbitre.md:451-460). No command runs."""
import os
import shutil
import sqlite3
import subprocess

import pytest

import codelots
import scan
import stats

HERE = os.path.dirname(os.path.abspath(__file__))
FEATURES = os.path.join(HERE, "fixtures", "features")


def real_app(tmp_path):
    app = tmp_path / "app"
    (app / ".claude").mkdir(parents=True)
    (app / "docs" / "features").mkdir(parents=True)
    shutil.copytree(os.path.join(FEATURES, "premiere-app"), app / "docs" / "features" / "premiere-app")
    return app


# ------------------------------------------------------------------ real files

def test_real_folders_read_every_lot_passed_and_agree_with_the_scan(tmp_path):
    app = real_app(tmp_path)
    sc = scan.run_scan(str(app), "premiere-app")
    by_name = {c["name"]: c for c in sc["corrections"]}
    for folder in ["", "bugfix-01", "bugfix-02", "bugfix-03", "bugfix-04", "bugfix-05", "bugfix-06"]:
        r = codelots.read_lots(str(app), "premiere-app", folder)
        assert r["exists"] and r["passed"] == r["total"] > 0
        assert {l["state"] for l in r["lots"]} == {codelots.PASSE}
        steps = by_name[folder]["steps"] if folder else sc["main"]
        step8 = next(s for s in steps if s["id"] == "8_code")
        if r["defects"]:
            # bugfix-03 to 05: `## Defects` holds « None. », a line — /8_code would
            # stop (COD-2) and the scan counts nothing; the tab says why.
            assert folder in ("bugfix-03", "bugfix-04", "bugfix-05") and r["defects"] == ["None."] and step8["lots"] is None
            assert any(w["rule"] == "COD-2" for w in step8["why"])
            continue
        # The bar and « n / N en PASS » come from one reader.
        assert step8["lots"] == {"pass": r["passed"], "total": r["total"]}, folder
        # Old verdicts carry no `## Attempts`: read as 1, and said so.
        assert all(l["attempts"]["used"] == 1 and l["attempts"]["note"] for l in r["lots"])
        assert not r["estimate"]["shown"]
    r = codelots.read_lots(str(app), "premiere-app", "")
    assert r["lots"][0]["title"].startswith("§1.1") and r["lots"][0]["fields"]["Produces"].startswith("Segment")
    assert [b["name"] for b in r["blocks"]][:2] == ["block-1", "block-2"]
    # bugfix-07 has no split yet.
    assert not codelots.read_lots(str(app), "premiere-app", "bugfix-07")["exists"]


def test_real_marks_of_the_arbitre_and_the_architecte(tmp_path):
    app = real_app(tmp_path)
    r = codelots.read_lots(str(app), "premiere-app", "bugfix-06")
    lot20 = next(l for l in r["lots"] if l["lot"] == "lot-20")
    assert {f["rel"] for f in lot20["arbitre"]["files"]} >= {"code/lot-20/blocked_realisateur-01.md",
                                                           "code/lot-20/blocked_detailleur-01.md"}
    assert lot20["architecte"]["requests"] == [{"rel": "architecte/detailleur-lot-20.md", "by": "detailleur",
                                                "answered": True}]
    lot01 = next(l for l in r["lots"] if l["lot"] == "lot-01")
    assert lot01["arbitre"] is None and lot01["architecte"]["requests"][0]["rel"] == "architecte/realisateur-lot-01.md"
    assert sum(1 for l in r["lots"] if not l["arbitre"] and not l["architecte"]) > 20


def test_real_lot_detail_renders_the_sheet_and_the_verdict(tmp_path):
    app = real_app(tmp_path)
    d = codelots.lot_detail(str(app), "premiere-app", "bugfix-06", "lot-01")
    assert d["sheet"]["exists"] and any(l.startswith("## ") for l in d["sheet"]["lines"])
    assert d["verdict"]["status"] == "PASS" and d["verdict"]["findings"] is None   # an older verdict: no ## Findings
    assert codelots.lot_detail(str(app), "premiere-app", "bugfix-06", "lot-999") is None


# ------------------------------------------------------- hand-written shapes

SEQ = """Round: 1

## Order

lot-01, lot-02, lot-03, lot-04, lot-05, lot-06, lot-07, lot-08, lot-09, lot-10

## Blocks

block-1: lot-01, lot-02, lot-03
block-2: lot-04, lot-05, lot-06, lot-07
block-3: lot-08, lot-09, lot-10

## Defects

"""


def verdict(status, attempts=1, cause="—", causes="—", findings="—"):
    return (f"## Status\n\n{status}\n\n## Attempts\n\n{attempts}\n\n## Verified\n\n./gradlew test green, 12 tests\n\n"
            f"## Findings\n\n{findings}\n\n## Cause\n\n{cause}\n\n## Causes so far\n\n{causes}\n\n"
            "## Symbol divergences\n\n—\n")


SHEET = "## Signatures\n\n    fun f(): Int\n\n## Acceptance criteria\n\n1. f returns 1\n"
REALISATEUR_BLOCK = """## Blocking 1

### What blocks

The sheet's `f` cannot return an Int here.

### Where

code/lot-09/fiche-executable.md

### To resume

Say which type.

## Decision

"""


def hand_folder(tmp_path, feature="h"):
    """Ten lots, one per state, after the templates."""
    app = tmp_path / "app"
    f = app / "docs" / "features" / feature
    code = f / "code"
    code.mkdir(parents=True)
    (app / ".claude").mkdir(exist_ok=True)
    (code / "sequence.md").write_text(SEQ, encoding="utf-8")
    dec = "## Symbols\n\nX\n  y   §1.1\n\n" + "".join(
        f"## lot-{i:02d}\n\nAnchor: §{i}.1 — Entry {i}\nNeeds: —\nProduces: S{i} (called by lot-10)\nModifies: —\nTouches: —\n\n"
        for i in range(1, 11))
    (code / "decoupage.md").write_text(dec, encoding="utf-8")

    def lot(n, files):
        d = code / f"lot-{n:02d}"
        d.mkdir()
        for name, text in files.items():
            (d / name).write_text(text, encoding="utf-8")

    full = {"fiche-executable.md": SHEET, "conception.md": "## Declared\n", "tests.md": "## Tests\n",
            "compte-rendu.md": "## Symbols\n"}
    lot(1, {**full, "verdict.md": verdict("PASS")})
    lot(2, {**full, "verdict.md": verdict("PASS with reservation", findings="point 4 — R12 reserved")})
    lot(3, {**full, "verdict.md": verdict("FAIL mineur", 2, "reasoning", "understanding, reasoning",
                                          "point 2 — criterion 3 has no test")})
    lot(4, {**full, "verdict.md": verdict("FAIL structurel", 3, "reasoning", "reasoning, reasoning, reasoning")})
    lot(5, {"verdict.md": verdict("FAIL structurel", 1, "sheet", "sheet", "the sheet lacks ## Conventions")})
    lot(6, {"fiche-executable.md": SHEET, "conception.md": "## Declared\n"})
    lot(7, {})
    lot(8, dict(full))
    lot(9, {"fiche-executable.md": SHEET, "conception.md": "## Declared\n", "tests.md": "## Tests\n",
            "blocked_realisateur.md": REALISATEUR_BLOCK})
    lot(10, {"verdict.md": "## Status\n\n"})
    (f / "architecte").mkdir()
    (f / "architecte" / "realisateur-lot-09.md").write_text(
        "## What I need\n\nA rule.\n\n## Verdict\n\n", encoding="utf-8")
    (f / "architecte" / "arbitre-lot-03-blocking-1.md").write_text(
        "## What I need\n\nA rule.\n\n## Verdict\n\nR40 already carries it.\n", encoding="utf-8")
    return app, f


def states(r):
    return {l["lot"]: l["state"] for l in r["lots"]}


def test_each_state_from_the_hand_written_shapes(tmp_path):
    app, f = hand_folder(tmp_path)
    opens = [{"id": "b:code/lot-09/blocked_realisateur.md#1", "rel": "code/lot-09/blocked_realisateur.md", "lot": None}]
    r = codelots.read_lots(str(app), "h", "", opens=opens)
    assert states(r) == {
        "lot-01": codelots.PASSE, "lot-02": codelots.PASSE, "lot-03": codelots.ECHOUE,
        "lot-04": codelots.TROIS, "lot-05": codelots.ANNULE, "lot-06": codelots.ENTAME,
        "lot-07": codelots.PAS_COMMENCE, "lot-08": codelots.ENTAME, "lot-09": codelots.BLOQUE,
        "lot-10": codelots.INCONNU}
    by = {l["lot"]: l for l in r["lots"]}
    assert by["lot-02"]["detail"] == "avec réserve"
    assert "reprend au testeur" in by["lot-06"]["detail"]
    assert "pas encore relu" in by["lot-08"]["detail"]
    assert by["lot-03"]["attempts"] == {"used": 2, "cap": 3, "note": None}
    assert by["lot-07"]["attempts"]["used"] == 0
    assert by["lot-09"]["blocking"] == ["b:code/lot-09/blocked_realisateur.md#1"]
    # The Arbitre: the Réalisateur's blocking file; the Architecte: a request named by the lot.
    assert by["lot-09"]["arbitre"]["files"][0]["rel"] == "code/lot-09/blocked_realisateur.md"
    assert by["lot-09"]["architecte"]["requests"][0]["answered"] is False
    assert by["lot-03"]["architecte"]["requests"][0]["answered"] is True
    assert by["lot-03"]["title"] == "§3.1 — Entry 3"
    # The bar and the scan's « n / N en PASS » agree.
    sc = scan.run_scan(str(app), "h")
    assert next(s for s in sc["main"] if s["id"] == "8_code")["lots"] == {"pass": r["passed"], "total": r["total"]} \
        == {"pass": 2, "total": 10}
    for l in r["lots"]:
        assert l["rule"] in codelots.RULES


def test_a_redecoupage_sends_every_lot_without_pass_back(tmp_path):
    app, f = hand_folder(tmp_path)
    (f / "code" / "redecoupage.md").write_text("## Ce qui revient\n\nlot-06\n", encoding="utf-8")
    s = states(codelots.read_lots(str(app), "h", ""))
    assert s["lot-01"] == codelots.PASSE and s["lot-06"] == codelots.REDECOUPE and s["lot-03"] == codelots.REDECOUPE


def test_the_detailleurs_entry_names_its_lot(tmp_path):
    app, f = hand_folder(tmp_path)
    (f / "code" / "blocked_detailleur.md").write_text(
        "## Blocking 1 — lot-07\n\n### What blocks\n\nx\n\n## Decision\n\n", encoding="utf-8")
    r = codelots.read_lots(str(app), "h", "")
    lot7 = next(l for l in r["lots"] if l["lot"] == "lot-07")
    assert lot7["arbitre"]["files"] == [{"rel": "code/blocked_detailleur.md", "agent": "detailleur",
                                         "archived": False, "entries": [1]}]


def run_snapshot(active, command="8_code"):
    return {"id": "r1", "command": command, "work": "h", "status": "running", "active": active}


def test_the_lot_in_progress_from_the_stream_else_from_the_rule(tmp_path):
    app, f = hand_folder(tmp_path)
    snap = run_snapshot([{"id": "t1", "agent": "realisateur", "lot": "lot-06"},
                         {"id": "t2", "agent": "arbitre", "lot": "lot-06"}])
    r = codelots.read_lots(str(app), "h", "", run=snap)
    assert r["current"] == {"lot": "lot-06", "agent": "realisateur → arbitre", "from": "flux"}
    assert states(r)["lot-06"] == codelots.EN_COURS
    # The Détailleur names a block: the next lot by 8_code.md:80-82, said so.
    r = codelots.read_lots(str(app), "h", "", run=run_snapshot([{"id": "t1", "agent": "detailleur", "lot": None}]))
    assert r["current"] == {"lot": "lot-03", "agent": "detailleur", "from": "regle"}
    # Another command, or no run: nothing in progress.
    assert codelots.read_lots(str(app), "h", "", run=run_snapshot([], "9_controle"))["current"] is None


def stored(lot, agent, dur, parent=None, folder="", output=None, block=None):
    return {"lot": lot, "agent": agent, "duration_s": dur, "parent_tool_use_id": parent, "folder": folder,
            "input_tokens": 10, "cache_read_tokens": 100, "cache_creation_tokens": 5, "output_tokens": output,
            "started_at": "2026-10-06T10:00:00", "ended_at": "2026-10-06T10:10:00", "block": block}


def test_the_estimate_waits_for_two_passed_lots(tmp_path):
    app, f = hand_folder(tmp_path)
    one = [stored("lot-01", "concepteur", 300), stored("lot-01", "realisateur", 300),
           stored("lot-01", "arbitre", 999, parent="t9")]          # nested: inside its caller's time
    r = codelots.read_lots(str(app), "h", "", passes=one)
    assert r["lots"][0]["duration_s"] == 600 and not r["estimate"]["shown"] and r["estimate"]["lots_known"] == 1
    two = one + [stored("lot-02", "realisateur", 1200)]
    e = codelots.read_lots(str(app), "h", "", passes=two)["estimate"]
    assert e["shown"] and e["median_s"] == 900 and e["left"] == 8 and e["eta_s"] == 7200
    # A passed lot with a pass of unknown duration does not count.
    e = codelots.read_lots(str(app), "h", "", passes=one + [stored("lot-02", "realisateur", None)])["estimate"]
    assert not e["shown"]
    # Passes of another working folder are not this folder's.
    r = codelots.read_lots(str(app), "h", "", passes=[stored("lot-01", "realisateur", 5, folder="bugfix-01")])
    assert r["lots"][0]["passes"] == []
    # The Détailleur's passes sit on their block.
    r = codelots.read_lots(str(app), "h", "", passes=[stored(None, "detailleur", 50, block="block-2")])
    assert [p["agent"] for p in r["block_passes"]] == ["detailleur"]


def test_during_a_run_the_files_are_read_in_its_worktree(tmp_path):
    app, f = hand_folder(tmp_path)
    wt = app / ".claude" / "worktrees" / "h"
    shutil.copytree(f, wt / "docs" / "features" / "h")
    (wt / "docs" / "features" / "h" / "code" / "lot-03" / "verdict.md").write_text(verdict("PASS", 3), encoding="utf-8")
    main = codelots.read_lots(str(app), "h", "")
    live = codelots.read_lots(str(app), "h", "", worktrees=[str(wt)])
    assert main["source"] == "dossier" and states(main)["lot-03"] == codelots.ECHOUE
    assert live["source"] == "worktree" and live["worktree"] == str(wt) and states(live)["lot-03"] == codelots.PASSE


# --------------------------------------------------------------------- commits

def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                        "GIT_COMMITTER_EMAIL": "t@t"})


def commit(repo, message, *files):
    for p in files:
        path = repo / p
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(message + "\n", encoding="utf-8")
        git(repo, "add", p)
    git(repo, "commit", "-q", "-m", message)


@pytest.mark.skipif(shutil.which("git") is None, reason="git absent")
def test_a_lots_commits_are_this_folders_reverts_marked(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    commit(repo, "init", "README.md")
    commit(repo, "lot-01: declarations", "src/A.kt", "docs/features/h/code/lot-01/conception.md")
    commit(repo, "lot-01: another split's", "src/B.kt", "docs/features/h/bugfix-01/code/lot-01/conception.md")
    commit(repo, "lot-01: no report staged", "src/C.kt")
    commit(repo, "lot-02: not this lot", "src/D.kt", "docs/features/h/code/lot-02/tests.md")
    sha = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%H", "--grep=^lot-01: declarations"],
                         capture_output=True, text=True).stdout.strip()
    git(repo, "revert", "--no-edit", sha)
    c = codelots.commits(str(repo), "docs/features/h", "lot-01")
    assert c["error"] is None and c["elsewhere"] == 1
    subjects = [(k["subject"], k["where"], k["revert"], k["reverted"]) for k in c["list"]]
    assert subjects == [('Revert "lot-01: declarations"', "dossier", True, False),
                        ("lot-01: no report staged", "sans dossier", False, False),
                        ("lot-01: declarations", "dossier", False, True)]
    assert c["list"][2]["files"] == ["docs/features/h/code/lot-01/conception.md", "src/A.kt"]


# ------------------------------------------------------ which lot a pass is

def agent_call(tid, prompt, desc, agent, parent=None):
    return ("AssistantMessage", {"parent_tool_use_id": parent, "model": "m", "message_id": "m-" + tid,
                                 "content": [{"id": tid, "name": "Agent", "input": {
                                     "subagent_type": agent, "description": desc, "prompt": prompt}}]})


STREAM = [
    agent_call("t1", "Working folder: docs/features/h. Your block: block-2.", "Detail block-2, h", "detailleur"),
    agent_call("t2", "Working folder: docs/features/h. Your lot: lot-04.", "Declare lot-04", "concepteur"),
    agent_call("t3", "Working folder: docs/features/h/bugfix-02. Your lot: lot-04.\nVerdict: code/lot-04/verdict.md.",
               "Code lot-04", "realisateur"),
    agent_call("t4", "Working folder: docs/features/h/bugfix-02.\nBlocking file: code/lot-04/blocked_realisateur.md.",
               "Settle lot-04", "arbitre", parent="t3"),
    agent_call("t5", "Working folder: docs/features/h/bugfix-02. Invocation 3 — Requests.\nCalled by the Arbitre.",
               "Requests docs/features/h/bugfix-02", "architecte", parent="t4"),
    agent_call("t6", "Working folder: docs/features/h. Invocation 3 — Requests.\nCalled by the orchestration.",
               "Requests docs/features/h", "architecte"),
    agent_call("t7", "go", "Something else", "lexicographe"),
]


def test_each_pass_gets_the_lot_its_input_names_and_inconnu_otherwise():
    t = stats.Tally()
    for kind, body in STREAM:
        t.feed(kind, body, "2026-10-06T10:00:00")
    got = {tid: (p.lot, p.block, p.folder) for tid, p in t.passes.items()}
    assert got == {"t1": (None, "block-2", ""), "t2": ("lot-04", None, ""), "t3": ("lot-04", None, "bugfix-02"),
                   "t4": ("lot-04", None, "bugfix-02"), "t5": ("lot-04", None, "bugfix-02"),
                   "t6": (None, None, ""), "t7": (None, None, None)}


def test_the_lot_is_stored_and_backfilled_once_from_the_logs(tmp_path):
    import json
    log = tmp_path / "2026-10-06-100000-8_code.jsonl"
    with open(log, "w", encoding="utf-8") as fh:
        for kind, body in STREAM[:3]:
            fh.write(json.dumps({"at": "2026-10-06T10:00:00", "type": kind, "message": body}) + "\n")
    db = tmp_path / "old.sqlite"
    # A 1.4 store: agent_passes without lot, block, folder.
    con = sqlite3.connect(db)
    con.executescript(stats.SCHEMA.replace(",\n  lot TEXT, block TEXT, folder TEXT", "").replace(
        "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);", ""))
    con.execute("INSERT INTO runs (id, feature, log_path) VALUES ('r1', 'h', ?)", (str(log),))
    for tid in ("t1", "t2", "t3"):
        con.execute("INSERT INTO agent_passes (run_id, tool_use_id, agent) VALUES ('r1', ?, 'x')", (tid,))
    con.commit()
    assert "lot" not in {r[1] for r in con.execute("PRAGMA table_info(agent_passes)")}
    con.close()
    s = stats.Store(str(db))
    assert s.backfill_lots() == {"runs": 1, "passes": 2, "missing": 0, "done": False}
    rows = {p["tool_use_id"]: (p["lot"], p["block"], p["folder"]) for p in s.passes("r1")}
    assert rows == {"t1": (None, "block-2", ""), "t2": ("lot-04", None, ""), "t3": ("lot-04", None, "bugfix-02")}
    assert s.backfill_lots()["done"] is True               # once
    got = codelots.store_passes(str(db), "h")
    assert sorted(p["lot"] or "-" for p in got) == ["-", "lot-04", "lot-04"]
