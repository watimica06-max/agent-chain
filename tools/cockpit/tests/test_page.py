"""Cockpit 1.2-1.3 — the page in a headless browser (Microsoft Edge through
Playwright), served by the real cockpit server over a fake application
folder and a fake SDK client. Skipped when Playwright or Edge is missing.
No chain command runs."""
import pytest

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright  # noqa: E402

import diagnostic  # noqa: E402
import nextline  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402
from test_runner import script_until_interrupted  # noqa: E402

SCREENS = [("Tableau de bord", "scr-dashboard"), ("À répondre", "scr-answer"),
           ("Chaîne", "scr-chaine"), ("Correction", "scr-correction"), ("Statistiques", "scr-stats"),
           ("Paramètres", "scr-settings")]


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge")
        except Exception as e:                      # no Edge on this machine
            pytest.skip(f"Edge indisponible : {e}")
        yield b
        b.close()


@pytest.fixture
def page(browser):
    pg = browser.new_page(viewport={"width": 1280, "height": 800})
    pg.js_errors = []
    pg.on("pageerror", lambda e: pg.js_errors.append(str(e)))
    pg.on("console", lambda m: pg.js_errors.append(m.text) if m.type == "error" else None)
    yield pg
    pg.close()


def relay_of(text):
    return nextline.parse(text).to_dict()


def set_relay(s, text, command="/4_grille f"):
    s.state.set_relay(str(s.app_root), "f", command, text, relay_of(text), "terminé")


def go(page, name):
    page.get_by_role("link", name=name).first.click()


def start_run(s, page):
    s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
    page.wait_for_selector("#perm-banner .perm", timeout=8000)


async def _wait(task):
    await task


def stop_run(s):
    s.call(s.rn.stop_now(str(s.app_root)))


def no_real_errors(page):
    # `Failed to fetch` only comes from the server going away at the end of a test.
    return [e for e in page.js_errors if "Failed to fetch" not in e and "net::ERR" not in e]


def test_each_screen_loads_without_js_error(tmp_path, page):
    with FakeServer(tmp_path) as s:
        set_relay(s, "Fini.\nNext: answer questions, then run /4_grille f")
        page.goto(s.url)
        page.wait_for_selector("#side")
        for name, scr in SCREENS:
            go(page, name)
            page.wait_for_selector(f"#{scr}", state="visible")
            assert page.locator("#main section:visible").evaluate_all("els => els.map(e => e.id)") == [scr]
        # Six entries (1.4.5), « Paramètres » last in the menu, the count on « À répondre ».
        names = [t.split("\n")[0].strip() for t in page.locator("#side a").all_inner_texts()]
        assert names == ["Tableau de bord", "À répondre", "Chaîne", "Correction", "Statistiques", "Paramètres"]
        assert page.locator("#nav-answer-count").inner_text() == "7"
        assert " ".join(page.locator("#tb-mode").inner_text().split()) == "Mode : Auto"
        assert page.locator("#tb-run").inner_text() == "Au repos"
        assert no_real_errors(page) == []


def test_start_screen_without_a_folder(tmp_path, page):
    with FakeServer(tmp_path, opened=False) as s:
        page.goto(s.url)
        page.wait_for_selector("#start", state="visible")
        assert not page.locator("#side").is_visible()
        assert page.get_by_role("heading", name="Dossier de l'application").is_visible()
        assert no_real_errors(page) == []


def test_permission_card_is_a_banner_on_every_screen(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        page.wait_for_selector("#side")
        start_run(s, page)
        for name, scr in SCREENS:
            go(page, name)
            page.wait_for_selector(f"#{scr}", state="visible")
            banner = page.locator("#perm-banner")
            assert banner.is_visible()
            allow = banner.get_by_role("button", name="Autoriser")
            deny = banner.get_by_role("button", name="Refuser")
            for b in (allow, deny):
                box = b.bounding_box()
                assert box and 0 <= box["y"] and box["y"] + box["height"] <= 800 / 2   # in the top half
            assert page.locator("#perm-badge").is_visible()
            # Still there after scrolling the screen: it never leaves the top.
            page.locator("#main").evaluate("e => e.scrollTo(0, e.scrollHeight)")
            assert allow.is_visible()
        # The click resolves it, from any screen.
        allow.click()
        page.wait_for_selector("#perm-banner", state="hidden")
        assert not page.locator("#perm-badge").is_visible()
        s.call(_wait(s.rn.current(str(s.app_root)).task))                # the run goes on to its end
        assert no_real_errors(page) == []


def test_save_bar_stays_visible_while_the_form_scrolls(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        go(page, "À répondre")
        page.wait_for_selector(".entry")
        # 1.4: the questions scroll in their own pane, beside the document.
        main = page.locator("#answer-left")
        assert main.evaluate("e => e.scrollHeight > e.clientHeight + 400")        # the form does scroll
        for top in (0, 600, 100000):
            main.evaluate(f"e => e.scrollTo(0, {top})")
            page.wait_for_timeout(100)
            box = page.locator("#save-bar").bounding_box()
            assert box and box["y"] >= 0 and box["y"] + box["height"] <= 800 + 1, (top, box)
            assert page.get_by_role("button", name="Enregistrer").is_visible()
        # The count follows the choices: a free answer on one entry → one unsaved answer.
        main.evaluate("e => e.scrollTo(0, 0)")
        page.locator(".entry").first.locator("textarea").fill("Ma réponse")
        page.locator(".entry").first.locator("label.opt").nth(2).click()
        assert "1 réponse non enregistrée" in page.locator("#save-hint").inner_text()
        assert "répondues" in page.locator("#progress").inner_text()
        assert no_real_errors(page) == []


def test_answer_screen_groups_options_and_marks_the_default(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        go(page, "À répondre")
        page.wait_for_selector(".entry")
        groups = page.locator("details.grp")
        assert groups.count() >= 3
        assert all(groups.nth(i).get_attribute("open") is not None for i in range(groups.count()))  # open by default
        groups.first.locator("summary").click()                                                      # collapsible
        assert groups.first.get_attribute("open") is None
        # The default is pre-selected and marked « par défaut ».
        assert page.get_by_text("par défaut").first.is_visible()
        assert page.locator(".opt.chosen", has_text="par défaut").count() == 1
        # Filters.
        page.get_by_role("button", name="Blocages (3)").click()
        assert page.locator(".entry").count() == 3
        page.get_by_role("button", name="Questions (4)").click()
        assert page.locator(".entry").count() == 4


NEXT_FORMS = [
    # Opening the page checks the stored line (§2.3): in « f », 1_lexique waits on
    # answers, so a run of any later step would be dropped — /1_lexique holds.
    ("Fini.\nNext: run /1_lexique f", "run", "Lancer /1_lexique f"),
    ("Fini.\nNext: answer questions, then run /4_grille f", "answer", "Répondre (4)"),
    ("Fini.\nNext: manual installer l'application sur le téléphone", "manual", None),
    ("Fini.\nNext: stop le split n'est pas cohérent", "stop", None),
    ("Fini.\nNext: done", "done", None),
]


@pytest.mark.parametrize("relay,kind,button", NEXT_FORMS, ids=[f[1] for f in NEXT_FORMS])
def test_dashboard_button_for_each_next_form(tmp_path, page, relay, kind, button):
    with FakeServer(tmp_path) as s:
        set_relay(s, relay)
        assert relay_of(relay)["kind"] == kind
        page.goto(s.url)
        page.wait_for_selector("#next-text")
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        card = page.locator("#next-card")
        assert relay_of(relay)["french"] in page.locator("#next-text").inner_text()
        buttons = card.locator("#next-detail button").all_inner_texts()
        if button is None:
            assert buttons == []                          # the text, no button
        else:
            assert buttons == [button]                    # one primary button
        assert page.locator("#next-source").inner_text() == "dit par la chaîne"
        if kind == "answer":
            assert "Ensuite : /4_grille f" in card.inner_text()
            card.get_by_role("button", name="Répondre (4)").click()
            page.wait_for_selector("#scr-answer", state="visible")
            assert page.locator(".entry").count() == 4                     # the questions the line names
        if kind == "run":
            card.get_by_role("button", name="Lancer /1_lexique f").click()  # named by the relay: no confirmation
            page.wait_for_selector("#scr-chaine", state="visible")           # launching shows the chain…
            page.wait_for_selector("#perm-banner .perm")
            page.wait_for_selector("#slot-main-1_lexique #run-panel")       # …the run under its step
            assert s.clients[0].prompts == ["/1_lexique f"]
            stop_run(s)
        assert no_real_errors(page) == []


def test_dashboard_with_no_relay_shows_the_folders_proposal(tmp_path, page):
    # 1.3: no stored Next: → the scan's proposal, labelled. « f » holds an
    # empty bugfix-01/: the highest correction, its bug-list still to write.
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        assert page.locator("#next-source").inner_text() == "déduite du dossier"
        assert page.locator("#next-text").inner_text() == (
            "À faire à la main : écrire bugfix-01/bug-list.md, puis lancer /diagnostique f.")
        page.get_by_role("button", name="Écrire la bug-list").click()
        page.wait_for_selector("#scr-correction", state="visible")
        page.wait_for_selector("#buglist-text")
        assert no_real_errors(page) == []


def test_dashboard_counters_alerts_and_history(tmp_path, page):
    with FakeServer(tmp_path) as s:
        set_relay(s, "Fini.\nNext: run /7_lots f")
        s.state.add_history(str(s.app_root), "f", {"command": "/7_lots f", "outcome": "terminé",
                            "next": relay_of("x\nNext: run /8_code f"), "log_path": "logs/a.jsonl", "at": "2026-10-05T09:30:00"})
        (s.feat / "stop.md").write_text("stop")
        page.goto(s.url)
        page.wait_for_selector("#cnt-q")
        page.wait_for_function("document.getElementById('cnt-q').textContent === '4'")
        assert page.locator("#cnt-b").inner_text() == "3"
        alerts = page.locator("#alerts").inner_text()
        assert "stop.md est présent" in alerts and "Fichier illisible" in alerts       # parser error
        assert "diagnostic" not in alerts          # 1.4.5: run on its own, all ✓ — no alert
        row = page.locator("#history tbody tr").first.inner_text()
        assert "/7_lots f" in row and "09:30" in row and "Next: run /8_code f" in row and "logs/a.jsonl" in row
        page.get_by_role("button", name="Retirer stop.md").first.click()
        page.wait_for_function("!document.getElementById('alerts').textContent.includes('stop.md est présent')")
        assert (s.feat / "stop1.md").exists()
        # A counter is a link to the answer screen, filtered.
        page.locator("#cnt-blocking").click()
        page.wait_for_selector("#scr-answer", state="visible")
        assert page.locator(".entry").count() == 3


def test_settings_mode_diagnostic_commands(tmp_path, page):
    def fake_diag(app):
        return diagnostic.run_diagnostic(app, fake_exec(dict(ALL_GOOD, java=FileNotFoundError("java introuvable (PATH)"),
                                                            adb=(1, "adb: boom"))))

    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "gradlew.bat").write_text("@echo off")          # a Gradle wrapper: the hint applies
    with FakeServer(tmp_path, diag_runner=fake_diag) as s:
        page.goto(s.url)
        go(page, "Paramètres")
        page.wait_for_selector("#scr-settings", state="visible")
        # Mode: Auto by default; Manuel is remembered by the server and shown in the top bar.
        assert page.locator("#set-mode input[value=auto]").is_checked()
        page.locator("#set-mode label", has_text="Manuel").click()
        page.wait_for_function("document.getElementById('tb-mode').textContent.includes('Manuel')")
        assert s.state.mode == "manuel"
        # Commands under five headings, in order, each with an editable argument.
        heads = page.locator("#set-commands h3").all_inner_texts()
        assert heads == ["Amont", "Aval", "Correction", "Fusion", "Outils"]
        arg = page.get_by_label("argument de /1_lexique")
        assert arg.input_value() == "f"
        # Diagnostic: ✓ / ✗ / non concerné, the Java hint, kept with its date.
        page.get_by_role("button", name="Lancer le diagnostic").click()
        page.wait_for_selector("#diag-result li")
        txt = page.locator("#diag-result").inner_text()
        assert "✗ Java" in txt and "✗ adb" in txt and "✓ Git" in txt and "— Flutter" in txt and "non concerné" in txt
        assert "JAVA_HOME" in txt
        assert s.state.diagnostic()["at"]
        # An alert on the dashboard now: the last diagnostic has a failure.
        go(page, "Tableau de bord")
        assert "a un échec" in page.locator("#alerts").inner_text()
        assert no_real_errors(page) == []


def test_a_command_the_relay_did_not_name_asks_for_confirmation(tmp_path, page):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        set_relay(s, "Fini.\nNext: run /7_lots f")
        page.goto(s.url)
        go(page, "Paramètres")
        asked = []

        def on_dialog(d):
            asked.append(d.message)
            d.dismiss()

        page.on("dialog", on_dialog)
        page.get_by_role("button", name="/1_lexique").click()
        page.wait_for_timeout(300)
        assert len(asked) == 1 and "n'est pas l'étape" in asked[0]
        assert s.clients == []                                         # dismissed: nothing ran
        assert page.locator(".cmd.hl").count() == 1                    # the named one is highlighted


def test_a_guessed_entry_is_shown_with_what_the_guess_saw(tmp_path, page):
    """1.4.1: the Relecteur's « missing input » guess never hides an entry."""
    with FakeServer(tmp_path) as s:
        lot = s.feat / "code" / "lot-09"
        lot.mkdir(parents=True)
        (lot / "blocked_relecteur.md").write_text(
            "## What blocks\n\n`code/lot-09/tests.md` is missing.\n\n## Where\n\ncode/lot-09\n\n"
            "## To resume\n\nRun the testeur.\n\n## Decision\n\n", encoding="utf-8")
        page.goto(s.url)
        go(page, "À répondre")
        card = page.locator(".entry", has_text="is missing")
        card.wait_for()
        assert "8_code.md:770-772" in card.locator(".notice").inner_text()
        assert no_real_errors(page) == []
