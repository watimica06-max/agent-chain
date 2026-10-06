"""Cockpit 1.3, §2 — the next step: a run going, a run just ended, a stored
`Next:` that holds, `answer …, then run X` with nothing left, and a stored
`Next:` the files contradict — for each contradiction. No command runs."""
import asyncio
import json
import os
import re

import decide
import nextline
import scan
import server
from test_scan import code_folder, make_app
from test_server import with_client, post


def stored(line, command="/x", head=None, log_path=""):
    return {"command": command, "relay": "…\n" + line, "next": nextline.parse(line).to_dict(),
            "outcome": "terminé", "at": "2026-10-05T10:00:00", "head": head, "log_path": log_path}


def sc_of(tmp_path, feature, run=None, worktree=False):
    app = make_app(tmp_path, feature)
    if worktree:
        (app / ".claude" / "worktrees" / feature).mkdir(parents=True)
    return app, scan.run_scan(str(app), feature, run)


def test_a_run_going_is_the_next_step(tmp_path):
    run = {"status": "running", "command": "1_lexique", "args": "premiere-app-3", "work": "premiere-app-3",
           "prompt": "/1_lexique premiere-app-3", "started_at": "2026-10-05T10:00:00"}
    _, sc = sc_of(tmp_path, "premiere-app-3", run)
    d = decide.decide(sc, "premiere-app-3", run=run, stored=stored("Next: run /2_structure premiere-app-3"))
    assert d["source"] == "run" and d["step"] == "1_lexique" and d["chain"] == "main"
    assert d["next"]["french"] == "Une commande tourne : /1_lexique premiere-app-3"


def test_a_run_just_ended_is_trusted_without_a_check(tmp_path):
    _, sc = sc_of(tmp_path, "premiere-app-3")
    # The files contradict it (1_lexique waits on answers), but it has just been printed.
    d = decide.decide(sc, "premiere-app-3", stored=stored("Next: run /2_structure premiere-app-3"), fresh=True,
                      head_now="b" * 40)
    assert d["source"] == "chaine" and d["label"] == "dit par la chaîne" and d["fresh"]
    assert d["next"]["command"] == "2_structure" and d["dropped"] is None and d["message"] is None


def test_a_stored_next_that_holds(tmp_path):
    _, sc = sc_of(tmp_path, "premiere-app-3")
    st = stored("Next: answer questions, then run /1_lexique premiere-app-3", head="a" * 40)
    d = decide.decide(sc, "premiere-app-3", stored=st, head_now="a" * 40)
    assert d["source"] == "chaine" and d["label"] == "dit par la chaîne"
    assert d["next"]["kind"] == "answer" and d["step"] == "1_lexique" and d["dropped"] is None


def test_answer_then_run_x_with_nothing_left_is_x(tmp_path):
    app, _ = sc_of(tmp_path, "premiere-app-3")
    q = app / "docs" / "features" / "premiere-app-3" / "questions-lexicographe-01.md"
    q.write_text(re.sub(r"^Answer:\s*$", "Answer: oui", q.read_text(encoding="utf-8"), flags=re.M), encoding="utf-8")
    sc = scan.run_scan(str(app), "premiere-app-3")
    assert sc["opens"] == []
    d = decide.decide(sc, "premiere-app-3", stored=stored("Next: answer questions, then run /1_lexique premiere-app-3"))
    assert d["source"] == "chaine" and d["label"] == "dit par la chaîne"
    assert d["next"]["kind"] == "run" and d["next"]["command"] == "1_lexique" and d["next"]["args"] == "premiere-app-3"
    assert d["step"] == "1_lexique" and d["dropped"] is None


CONTRADICTIONS = [
    # (feature, stored line, worktree left, stored HEAD, rule, what the folder says)
    ("premiere-app-3", "Next: run /2_structure premiere-app-3", False, None, "X-AMONT",
     "Répondre aux questions de « Fixer le vocabulaire », puis lancer /1_lexique premiere-app-3."),
    # A split that holds, three lots to code: /7_lots already ran.
    ("c", "Next: run /7_lots c", False, None, "X-FAITE", "Lancer /8_code c."),
    ("premiere-app-3", "Next: run /1_lexique premiere-app-3", True, None, "X-BLOQUEE",
     None),
    ("premiere-app-3", "Next: answer questions, then run /1_lexique premiere-app-3", False, "a" * 40, "G-HEAD",
     "Répondre aux questions de « Fixer le vocabulaire », puis lancer /1_lexique premiere-app-3."),
]


def test_each_contradiction_drops_the_stored_next(tmp_path):
    for i, (feature, line, wt, head, rule, says) in enumerate(CONTRADICTIONS):
        if feature == "c":
            app = code_folder(tmp_path / str(i), {"lot-01": "PASS"})
            sc = scan.run_scan(str(app), "c")
        else:
            _, sc = sc_of(tmp_path / str(i), feature, worktree=wt)
        d = decide.decide(sc, feature, stored=stored(line, head=head), head_now="b" * 40)
        assert d["source"] == "dossier" and d["label"] == "déduite du dossier", rule
        assert d["dropped"]["rule"] == rule and d["dropped"]["reason"], rule
        assert d["next"] == d["scanned"], rule                      # the scan's proposal takes its place
        if says:
            assert d["next"]["french"] == says, rule
        assert d["message"] == (f"Le dernier relais disait « {line} » ; "
                                f"les fichiers disent « {d['next']['french']} ».")


def test_no_stored_next_is_the_scan_labelled(tmp_path):
    _, sc = sc_of(tmp_path, "premiere-app-3")
    d = decide.decide(sc, "premiere-app-3", stored=None)
    assert d["source"] == "dossier" and d["label"] == "déduite du dossier" and d["dropped"] is None
    assert d["next"]["kind"] == "answer" and d["step"] == "1_lexique"


def test_stop_and_manual_hold_unless_head_moved(tmp_path):
    _, sc = sc_of(tmp_path, "premiere-app-3")
    for line in ("Next: stop lot-07 failed three times",
                 "Next: manual lire le rapport de contrôle et la recette, décider d'une bug-list"):
        d = decide.decide(sc, "premiere-app-3", stored=stored(line, head="a" * 40), head_now="a" * 40)
        assert d["source"] == "chaine" and d["next"]["raw"] == line
        d = decide.decide(sc, "premiere-app-3", stored=stored(line, head="a" * 40), head_now="c" * 40)
        assert d["source"] == "dossier" and d["dropped"]["rule"] == "G-HEAD"


# -------------------------------------------------- the server: triggers, log

def test_the_check_drops_logs_once_and_only_after_a_trigger(tmp_path):
    log = tmp_path / "run.jsonl"
    log.write_text("", encoding="utf-8")

    async def body(c, app_root, feat, rn):
        r = await post(c, "/api/open", {"app": str(app_root), "work": "f"})
        assert r.status == 200
        state = c.server.app[server.STATE_KEY]
        line = "Next: run /2_structure f"
        # Just ended: trusted as printed, though « f » holds open questions upstream.
        state.set_relay(str(app_root), "f", "/1_lexique f", "…\n" + line, nextline.parse(line).to_dict(),
                        log_path=str(log))
        s = await (await c.get("/api/state")).json()
        assert s["decision"]["source"] == "chaine" and s["decision"]["fresh"]
        assert log.read_text(encoding="utf-8") == ""
        # « Où on en est ? » — the check runs, the line is dropped and logged.
        s = await (await post(c, "/api/check", {"reason": "bouton"})).json()
        d = s["decision"]
        assert d["source"] == "dossier" and d["dropped"]["rule"] == "X-AMONT"
        assert d["message"].startswith("Le dernier relais disait « Next: run /2_structure f »")
        # Refreshing again does not log twice.
        await c.get("/api/state")
        await post(c, "/api/check", {"reason": "bouton"})
        lines = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines()]
        assert len(lines) == 1 and lines[0]["type"] == "NextDropped"
        assert lines[0]["message"]["rule"] == "X-AMONT" and lines[0]["message"]["trigger"] == "bouton"
        assert lines[0]["message"]["said"] == line

    with_client(tmp_path, body)


def test_a_save_of_answers_ends_the_trust(tmp_path):
    async def body(c, app_root, feat, rn):
        await post(c, "/api/open", {"app": str(app_root), "work": "f"})
        state = c.server.app[server.STATE_KEY]
        line = "Next: run /2_structure f"
        state.set_relay(str(app_root), "f", "/1_lexique f", line, nextline.parse(line).to_dict())
        assert (await (await c.get("/api/state")).json())["decision"]["source"] == "chaine"
        await post(c, "/api/save", {"items": []})
        assert (await (await c.get("/api/state")).json())["decision"]["source"] == "dossier"

    with_client(tmp_path, body)


def test_a_run_end_stores_head_and_its_log(tmp_path, monkeypatch):
    import runner as runner_mod
    from state import State
    st = State(str(tmp_path / "config.json"))
    monkeypatch.setattr(server.gitref, "head", lambda repo: "f" * 40)

    class R:
        repo, work, prompt, relay, outcome, log_path = str(tmp_path), "f", "/1_lexique f", "Next: done", "terminé", "logs/x.jsonl"
        next = {"kind": "done"}
    server.make_on_end(st)(R)
    rel = st.relay(str(tmp_path), "f")
    assert rel["head"] == "f" * 40 and rel["log_path"] == "logs/x.jsonl" and st.is_fresh(str(tmp_path), "f")
    del runner_mod
