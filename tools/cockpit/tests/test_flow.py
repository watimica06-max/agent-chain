"""Cockpit 1.3 — « Chaîne » and « Correction » as flows, in a headless
browser over a fake application folder and a fake SDK client. No chain
command runs: the fake runner records the prompt it was sent."""
import os

import pytest

pytest.importorskip("playwright")

import nextline  # noqa: E402
from claude_agent_sdk import AssistantMessage, TextBlock  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_page import browser, page, no_real_errors, stop_run  # noqa: E402,F401
from test_runner import result, script_until_interrupted  # noqa: E402


def add_turn_feature(app_root, name, root_files=(), blocked_classeur=False):
    """A feature in a later upstream turn: vocabulary settled, grid run once,
    one block MODIFIED by the last integration."""
    feat = app_root / "docs" / "features" / name
    (feat / "questions" / "lexicographe").mkdir(parents=True)
    (feat / "questions" / "lexicographe" / "questions-lexicographe-03.md").write_text("# Lexique\n", encoding="utf-8")
    (feat / "questions" / "sondeur").mkdir(parents=True)
    (feat / "questions" / "sondeur" / "questions-sondeur-01.md").write_text(
        "### Q1\nQuestion: x\nAnswer: oui\n", encoding="utf-8")
    (feat / "desc-produit.md").write_text(
        "# Produit\n\n### B1 — Une course MODIFIED\nGenre: comportement\nNature: model\n\nTexte.\n", encoding="utf-8")
    for f in root_files:
        (feat / f).write_text("# rien à demander\n", encoding="utf-8")
    if blocked_classeur:
        (feat / "blocked_classeur.md").write_text(
            "## Blocking 1\n\n## What blocks\n\nDeux natures.\n\n## Where\n\nB1\n\n## To resume\n\nChoisir.\n\n## Decision\n\n",
            encoding="utf-8")
    return feat


def open_feature(s, page, name):
    s.state.open_pair(str(s.app_root), name)
    open_feature.n = getattr(open_feature, "n", 0) + 1
    page.goto(f"{s.url}?{open_feature.n}#chaine")          # a new URL: the page loads again
    page.wait_for_selector("#flow-main li.step")


def states_shown(page, flow="#flow-main"):
    return page.locator(f"{flow} li.step").evaluate_all(
        "els => Object.fromEntries(els.map(e => [e.id.replace(/^step-[^-]+-/, ''), e.dataset.state]))")


def dialogs(page, accept):
    """Answer every dialog the same way; returns what they said, and how to stop."""
    seen = []

    def on(d):
        seen.append(d.message)
        d.accept() if accept else d.dismiss()
    page.on("dialog", on)
    return seen, lambda: page.remove_listener("dialog", on)


def test_the_flow_shows_each_state(tmp_path, page):
    with FakeServer(tmp_path) as s:
        add_turn_feature(s.app_root, "t", ["questions-analyste-01.md"], blocked_classeur=True)
        open_feature(s, page, "t")
        got = states_shown(page)
        assert got["1_lexique"] == "faite" and got["2_structure"] == "faite"
        assert got["3_decoupe"] == "inconnu"            # a file out of the turn at the root (DEC-9)
        assert got["3b_nature"] == "t'attend"           # blocked_classeur.md, decision empty
        assert got["4_grille"] == "à faire"
        assert page.locator("#step-main-3_decoupe .stc").inner_text() == "inconnu"
        assert len(got) == 14
        # bloquée and en cours, on « f »: a worktree left, then a run going.
        (s.app_root / ".claude" / "worktrees" / "f").mkdir(parents=True)
        open_feature(s, page, "f")
        assert states_shown(page)["1_lexique"] == "bloquée"
        (s.app_root / ".claude" / "worktrees" / "f").rmdir()
        s.script = script_until_interrupted
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_function("document.querySelector('#step-main-1_lexique').dataset.state === 'en cours'")
        assert page.locator("#step-main-1_lexique.is-next .stc").inner_text() == "en cours"
        # The running step shows the live run under it, with its stop button.
        page.wait_for_selector("#slot-main-1_lexique #run-panel #stream")
        assert page.locator("#slot-main-1_lexique").get_by_role("button", name="Arrêter maintenant").is_enabled()
        stop_run(s)
        assert no_real_errors(page) == []


def test_why_shows_the_rule_and_the_files_for_each_state(tmp_path, page):
    with FakeServer(tmp_path) as s:
        add_turn_feature(s.app_root, "t", ["questions-analyste-01.md"], blocked_classeur=True)
        open_feature(s, page, "t")
        for sid, rule, file in [("1_lexique", "LEX-7", "questions-analyste-01.md"),
                                ("3_decoupe", "DEC-9", "questions-analyste-01.md"),
                                ("3b_nature", "G-ATT", "blocked_classeur.md"),
                                ("4_grille", "GRI-6", "questions/sondeur/questions-sondeur-01.md")]:
            row = page.locator(f"#step-main-{sid}")
            row.get_by_role("button", name="Pourquoi ?").click()
            box = row.locator(".whybox")
            assert box.is_visible()
            text = box.inner_text()
            assert rule in text and file in text and "Règle (scan_rules.md)" in text, (sid, text)
        (s.app_root / ".claude" / "worktrees" / "t").mkdir(parents=True)
        open_feature(s, page, "t")
        row = page.locator("#step-main-3_decoupe")
        row.get_by_role("button", name="Pourquoi ?").click()
        assert "G-WT" in row.locator(".whybox").inner_text() and ".claude/worktrees/t" in row.locator(".whybox").inner_text()
        assert no_real_errors(page) == []


def test_the_proposed_step_stands_out_and_one_click_launches_it(tmp_path, page):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        add_turn_feature(s.app_root, "t")               # the root is empty: /3_decoupe ran, /3a_genre is next
        open_feature(s, page, "t")
        nxt = page.locator("li.step.is-next")
        assert nxt.count() == 1 and nxt.get_attribute("id") == "step-main-3a_genre"
        assert "déduite du dossier" in nxt.locator(".next-tag").inner_text()
        asked, _ = dialogs(page, accept=False)
        nxt.get_by_role("button", name="Lancer").click()
        page.wait_for_selector("#slot-main-3a_genre #run-panel")
        assert asked == [] and s.clients[0].prompts == ["/3a_genre t"]
        stop_run(s)


def test_a_step_off_the_proposal_or_flagged_asks_first(tmp_path, page):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        add_turn_feature(s.app_root, "t")
        open_feature(s, page, "t")
        asked, off = dialogs(page, accept=False)
        # Neither named nor proposed: asks, and dismissed, nothing runs.
        page.locator("#step-main-3b_nature").get_by_role("button", name="Lancer").click()
        page.wait_for_timeout(200)
        assert len(asked) == 1 and "ni l'étape que la chaîne a nommée, ni celle que le dossier propose" in asked[0]
        # Flagged by §1.2: always asks, with the reason.
        page.locator("#step-main-9_controle").get_by_role("button", name="Lancer").click()
        page.wait_for_timeout(200)
        assert "demande toujours confirmation" in asked[1] and "9_controle.md:104" in asked[1]
        # /7_lots now tests before it acts: off the proposal it asks, but not as flagged.
        page.locator("#step-main-7_lots").get_by_role("button", name="Lancer").click()
        page.wait_for_timeout(200)
        assert "demande toujours confirmation" not in asked[2]
        assert s.clients == []
        off()

    with FakeServer(tmp_path / "b", script=script_until_interrupted) as s:
        add_turn_feature(s.app_root, "t", ["questions-redacteur-02.md"])   # /3_decoupe is the proposal…
        open_feature(s, page, "t")
        assert page.locator("li.step.is-next").get_attribute("id") == "step-main-3_decoupe"
        asked, _ = dialogs(page, accept=True)
        page.locator("#step-main-3_decoupe").get_by_role("button", name="Lancer").click()
        page.wait_for_selector("#slot-main-3_decoupe #run-panel")
        # …and no longer asks: every test of /3_decoupe now comes before its git mv.
        assert asked == []
        assert s.clients[0].prompts == ["/3_decoupe t"]
        stop_run(s)

    with FakeServer(tmp_path / "c", script=script_until_interrupted) as s:
        feat = add_turn_feature(s.app_root, "t")
        (feat / "blocked_redacteur.md").write_text(
            "## Invocation\n\n2\n\n## Blocking 1\n\n## What blocks\n\nx\n\n## Decision\n\nRéécrire B1.\n",
            encoding="utf-8")                                           # /2_structure is the proposal…
        open_feature(s, page, "t")
        assert page.locator("li.step.is-next").get_attribute("id") == "step-main-2_structure"
        asked, _ = dialogs(page, accept=True)
        page.locator("#step-main-2_structure").get_by_role("button", name="Lancer").click()
        page.wait_for_selector("#slot-main-2_structure #run-panel")
        # …and still asks: its root table reads the root after its git mv.
        assert len(asked) == 1 and "demande toujours confirmation" in asked[0] and "ni l'étape" not in asked[0]
        assert s.clients[0].prompts == ["/2_structure t"]
        stop_run(s)


def test_the_next_lines_own_arguments_are_used(tmp_path, page):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        page.goto(s.url + "#correction")
        page.wait_for_selector("#flow-corr li.step")
        line = "Next: run /8_code f 3"
        # Just ended (trusted); the page refreshes without a scan trigger.
        s.state.set_relay(str(s.app_root), "f", "/7_lots f", line, nextline.parse(line).to_dict())
        page.evaluate("refreshState()")
        page.wait_for_selector("#step-bugfix-01-8_code.is-next")
        asked, _ = dialogs(page, accept=True)
        page.locator("#step-bugfix-01-8_code").get_by_role("button", name="Lancer").click()
        page.wait_for_selector("#slot-bugfix-01-8_code #run-panel")
        # The step the chain named, and /8_code tests before it acts: no question asked.
        assert asked == []
        assert s.clients[0].prompts == ["/8_code f 3"]
        stop_run(s)


def test_a_waiting_step_opens_its_answers(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url + "#chaine")
        row = page.locator("#step-main-1_lexique")
        btn = row.get_by_role("button", name="Répondre (3)")    # the sondeur's three open questions
        btn.click()
        page.wait_for_selector("#scr-answer", state="visible")
        assert "Fixer le vocabulaire" in page.locator("#step-filter").inner_text()
        assert page.locator(".entry").count() == 3
        assert all("Fixer le vocabulaire" in t for t in page.locator(".entry .head").all_inner_texts())
        page.locator("#step-filter").get_by_role("button", name="✕ tout montrer").click()
        assert page.locator(".entry").count() == 7


async def script_no_next(c):
    yield AssistantMessage(content=[TextBlock("J'ai fini sans ligne.")], model="m")
    yield result("J'ai fini sans ligne.")


def test_a_run_ended_without_next_offers_to_continue_under_its_step(tmp_path, page):
    with FakeServer(tmp_path, script=script_no_next) as s:
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#slot-main-1_lexique #run-end button:has-text('Continuer la session')")
        assert no_real_errors(page) == []


def test_the_test_step_deploys_and_says_what_to_test(tmp_path, page):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        (s.feat / "bugfix-01" / "code").mkdir(parents=True)
        (s.feat / "bugfix-01" / "code" / "recette-ordonnee.md").write_text(
            "# Recette\n\n1. Lancer une course\n2. Marquer une station\n", encoding="utf-8")
        page.goto(s.url + "#chaine")
        row = page.locator("#step-main-test")
        row.wait_for()
        assert "À tester : bugfix-01/code/recette-ordonnee.md — 2 points" in row.inner_text()
        dialogs(page, accept=True)
        row.get_by_role("button", name="Déployer").click()
        page.wait_for_selector("#slot-main-test #run-panel")
        assert s.clients[0].prompts == ["/deploie"]
        stop_run(s)


def test_correction_lists_newest_first_and_starts_a_cycle(tmp_path, page):
    with FakeServer(tmp_path) as s:
        before = {os.path.relpath(os.path.join(r, f), s.feat) for r, _, fs in os.walk(s.feat) for f in fs}
        page.goto(s.url + "#correction")
        page.wait_for_selector("#flow-corr li.step")
        dialogs(page, accept=True)
        page.get_by_role("button", name="Nouvelle correction").click()
        page.wait_for_function("document.getElementById('corr-list').textContent.includes('bugfix-02')")
        page.wait_for_function("document.querySelector('#buglist-card h2').textContent.startsWith('bugfix-02')")
        assert page.locator("#corr-list button").all_inner_texts() == ["bugfix-02 · en cours", "bugfix-01"]
        page.locator("#buglist-text").fill("G01 Le chronomètre ne tourne pas\n\nAucun tick n'est émis.")
        page.get_by_role("button", name="Enregistrer bug-list.md").click()
        page.wait_for_function("document.getElementById('buglist-hint').textContent === 'Enregistré.'")
        after = {os.path.relpath(os.path.join(r, f), s.feat) for r, _, fs in os.walk(s.feat) for f in fs}
        assert after - before == {os.path.join("bugfix-02", "bug-list.md")} and before <= after   # those two things only
        assert (s.feat / "bugfix-02" / "bug-list.md").read_text(encoding="utf-8").startswith("G01 Le chronomètre")
        # The new one is the highest: launchable. The older is read-only.
        assert page.locator("#step-bugfix-02-diagnostique").get_by_role("button", name="Lancer").is_enabled()
        page.locator("#corr-list").get_by_role("button", name="bugfix-01").click()
        assert page.locator("#step-bugfix-01-diagnostique").get_by_role("button", name="Lancer").is_disabled()
        assert "Lecture seule" in page.locator("#corr-note").inner_text()
        assert no_real_errors(page) == []


def test_ou_on_en_est_rechecks_the_stored_next(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        line = "Next: run /2_structure f"
        s.state.set_relay(str(s.app_root), "f", "/1_lexique f", line, nextline.parse(line).to_dict())
        page.evaluate("refreshState()")                      # right after its run: trusted
        page.wait_for_function("document.getElementById('next-source').textContent === 'dit par la chaîne'")
        assert page.locator("#next-text").inner_text() == "Lancer /2_structure f."
        page.get_by_role("button", name="Où on en est ?").click()
        page.wait_for_function("document.getElementById('next-source').textContent === 'déduite du dossier'")
        msg = page.locator("#next-message").inner_text()
        assert msg.startswith("Le dernier relais disait « Next: run /2_structure f » ; les fichiers disent « ")
        page.get_by_role("button", name="Pourquoi ?").first.click()
        assert "X-AMONT" in page.locator("#next-why").inner_text()
        assert no_real_errors(page) == []


def test_settings_pick_a_feature_not_a_bugfix(tmp_path, page):
    with FakeServer(tmp_path) as s:
        add_turn_feature(s.app_root, "t")
        page.goto(s.url + "#settings")
        page.wait_for_selector("#feature-list button")
        assert page.locator("#feature-list button").all_inner_texts() == ["f", "t"]
        page.locator("#feature-list").get_by_role("button", name="t").click()
        page.wait_for_function("document.getElementById('tb-folder').textContent.startsWith('t')")
        assert s.state.working_folder == "t"
