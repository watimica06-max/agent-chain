"""Cockpit 1.4.5 — the page in a headless browser (Microsoft Edge through
Playwright): the « Statistiques » screen on a fixture store, the side menu
that closes, « Où on en est ? » on « Chaîne », the diagnostic run on its own,
one text size and a lower save bar in « À répondre ». No chain command runs."""
import pytest

pytest.importorskip("playwright")

import diagnostic  # noqa: E402
import stats  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402
from test_page import browser, go, no_real_errors, page  # noqa: E402,F401
from test_statistics import R1_LOG, fixture_store  # noqa: E402


def stats_server(tmp_path, **kw):
    return FakeServer(tmp_path, stats=fixture_store(str(tmp_path / "stats.sqlite")), **kw)


def open_stats(page, s, period="tout"):
    page.goto(s.url + "#stats")
    page.wait_for_selector("#st-tiles .tile")
    page.locator(f"#st-period button[data-p='{period}']").click()
    page.wait_for_function(f"document.querySelector('#st-period button[data-p=\"{period}\"]').getAttribute('aria-pressed') === 'true'"
                           " && document.querySelectorAll('#tbl-history tbody tr').length > 0")


def test_statistics_screen_every_section(tmp_path, page):
    with stats_server(tmp_path) as s:
        open_stats(page, s)
        # Six in « Statistiques », between Correction and Paramètres.
        assert page.locator("#side a").evaluate_all("as => as.map(a => a.id)") == [
            "nav-dashboard", "nav-answer", "nav-chaine", "nav-correction", "nav-stats", "nav-apps", "nav-settings"]   # 1.6: « Applications »
        tiles = page.locator("#st-tiles .tile").all_inner_texts()
        assert len(tiles) == 6
        assert tiles[0].startswith("Runs\n2")
        assert "Tokens écrits\n500" in tiles[3] and "dont 1 run inconnu" in tiles[3]
        assert "≈ 5 %" in tiles[4] and "dont 1 run sans mesure" in tiles[4]
        # The limits over time: two lines, every measure a point, the runs on the axis.
        assert page.locator("#st-chart svg path").count() == 2
        # The limits are the account's: every measure of the period, whatever
        # the feature (8); the runs marked are the filter's (2).
        assert page.locator("#st-chart svg circle").count() == 8
        assert page.locator("#st-chart svg rect.runmark").count() == 2
        labels = page.locator("#st-chart svg text.dl").all_text_contents()
        assert labels == ["5 h · 25 %", "semaine · 41 %"]
        # Par commande, par agent; an unknown sum says so, never 0.
        cmd = page.locator("#tbl-cmd tbody tr").all_inner_texts()
        assert len(cmd) == 2 and any("/4_grille" in r and "inconnu" in r for r in cmd)
        agent = page.locator("#tbl-agent tbody tr", has_text="Sondeur").inner_text()
        assert "inconnu" in agent and "dont 3 passes inconnues" in agent
        # « Par fonctionnalité » only for « toutes ».
        assert page.locator("#st-feat").is_hidden()
        page.locator("#st-feature").select_option("*")
        page.wait_for_selector("#st-feat", state="visible")
        assert page.locator("#tbl-feat tbody tr").count() == 2
        # Les plus coûteux: r4 first, « inhabituel ».
        first = page.locator("#tbl-costly-runs tbody tr").first.inner_text()
        assert "/1_lexique g" in first and "inhabituel" in first
        assert "inhabituel" in page.locator("#tbl-costly-passes tbody tr").first.inner_text()
        assert page.locator("#tbl-history tbody tr").count() == 4
        assert no_real_errors(page) == []


def test_statistics_sort_open_a_run_and_remember_the_filters(tmp_path, page):
    with stats_server(tmp_path) as s:
        open_stats(page, s, "7j")
        firsts = lambda: page.locator("#tbl-cmd tbody tr td:first-child").all_inner_texts()  # noqa: E731
        assert firsts() == ["/4_grille", "/1_lexique"]                        # tokens read, most first
        head = page.locator("#tbl-cmd th", has_text="Commande")
        head.get_by_role("button").click()
        assert firsts() == ["/1_lexique", "/4_grille"]
        assert page.locator("#tbl-cmd th", has_text="Commande").get_attribute("aria-sort") == "ascending"
        page.locator("#tbl-cmd th", has_text="Commande").get_by_role("button").click()
        assert firsts() == ["/4_grille", "/1_lexique"]
        # A click opens a run: its agent passes and the path of its log.
        row = page.locator("#tbl-history tbody tr", has_text="/1_lexique f")
        row.click()
        detail = page.locator("#tbl-history tr.detail")
        detail.wait_for()
        txt = detail.inner_text()
        assert R1_LOG in txt and "Lexicographe" in txt and "Sondeur" in txt
        assert "20 % → 25 %" in txt and "≈ 5 %" in txt
        assert page.locator("#tbl-history tr[aria-expanded=true]").count() == 1
        # The other run: no start measure, said.
        page.locator("#tbl-history tbody tr", has_text="/4_grille f").first.click()
        assert "pas de mesure au début du run" in page.locator("#tbl-history").inner_text()
        # The filters are remembered.
        page.reload()
        page.wait_for_selector("#st-tiles .tile")
        assert page.locator("#st-period button[data-p='7j']").get_attribute("aria-pressed") == "true"
        assert no_real_errors(page) == []


def test_the_side_menu_closes_and_its_dot(tmp_path, page):
    with FakeServer(tmp_path) as s:
        empty = s.app_root / "docs" / "features" / "vide"
        empty.mkdir(parents=True)
        page.goto(s.url)
        page.wait_for_function("document.getElementById('nav-answer-count').textContent === '7'")
        menu = page.get_by_role("button", name="Fermer le menu")
        before = page.locator("#main").bounding_box()["width"]
        menu.click()
        assert page.locator("#side").is_hidden()
        assert page.locator("#main").bounding_box()["width"] >= before + 200        # the full width
        # Closed, with entries to answer: the dot.
        assert page.locator("#tb-menu-dot").is_visible()
        # Remembered across a reload.
        page.reload()
        page.wait_for_function("document.getElementById('nav-answer-count').textContent === '7'")
        assert page.locator("#side").is_hidden() and page.locator("#tb-menu-dot").is_visible()
        assert page.locator("#tb-menu").get_attribute("aria-expanded") == "false"
        # Nothing waits: no dot.
        s.state.open_pair(str(s.app_root), "vide")
        page.reload()
        page.wait_for_function("document.getElementById('tb-folder').textContent.startsWith('vide')")
        page.wait_for_timeout(300)
        assert page.locator("#tb-menu-dot").is_hidden()
        page.get_by_role("button", name="Ouvrir le menu").click()
        assert page.locator("#side").is_visible()
        assert no_real_errors(page) == []


def test_the_menu_dot_while_a_run_goes(tmp_path, page):
    with FakeServer(tmp_path) as s:
        (s.app_root / "docs" / "features" / "vide").mkdir(parents=True)
        s.state.open_pair(str(s.app_root), "vide")
        page.goto(s.url)
        page.wait_for_selector("#tb-menu", state="visible")
        page.get_by_role("button", name="Fermer le menu").click()
        page.wait_for_timeout(200)
        assert page.locator("#tb-menu-dot").is_hidden()
        s.call(s.rn.start(str(s.app_root), "vide", "vide", "1_lexique", "vide"))
        page.wait_for_selector("#tb-menu-dot", state="visible", timeout=8000)
        s.call(s.rn.stop_now(str(s.app_root)))
        assert no_real_errors(page) == []


def test_where_button_sits_on_chaine(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        page.wait_for_selector("#tb-folder", state="visible")
        assert page.locator("#topbar").get_by_role("button", name="Où on en est ?").count() == 0
        go(page, "Chaîne")
        btn = page.locator("#scr-chaine").get_by_role("button", name="Où on en est ?")
        assert btn.is_visible()
        assert btn.bounding_box()["y"] < page.locator("#flow-main").bounding_box()["y"]   # at the top
        btn.click()
        page.wait_for_function("!document.getElementById('chaine-where').disabled")
        assert no_real_errors(page) == []


def test_no_diagnostic_stored_it_runs_once_and_the_alert_waits_for_a_failure(tmp_path, page):
    calls = []

    def ok(app):
        calls.append(app)
        return diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD))

    with FakeServer(tmp_path, diag_runner=ok) as s:
        page.goto(s.url)
        page.wait_for_selector("#alerts", state="attached")
        for _ in range(100):
            if s.state.diagnostic():
                break
            page.wait_for_timeout(50)
        assert s.state.diagnostic()["ok"]
        page.reload()
        page.wait_for_selector("#cnt-q")
        page.wait_for_timeout(300)
        assert "diagnostic" not in page.locator("#alerts").inner_text()
        go(page, "Paramètres")
        assert "✓ Git" in page.locator("#diag-result").inner_text()
        assert len(calls) == 1
        assert no_real_errors(page) == []


def test_a_failed_diagnostic_run_on_its_own_raises_the_alert(tmp_path, page):
    def bad(app):
        return diagnostic.run_diagnostic(app, fake_exec(dict(ALL_GOOD, adb=(1, "adb: boom"))))

    with FakeServer(tmp_path, diag_runner=bad) as s:
        page.goto(s.url)
        page.wait_for_function("document.getElementById('alerts').textContent.includes('a un échec')", timeout=8000)
        assert "adb" in page.locator("#alerts").inner_text()
        assert no_real_errors(page) == []


def test_answer_screen_one_text_size_and_a_lower_save_bar(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url + "#answer")
        page.wait_for_selector(".entry .q")
        size = lambda sel: page.locator(sel).first.evaluate("e => getComputedStyle(e).fontSize")  # noqa: E731
        right = size("#ctx-doc")
        assert right == "15px"
        for sel in (".entry .q", ".entry .opt", ".entry textarea"):
            assert size(sel) == right, sel
        assert size(".entry .badge") == "12px"
        # Click targets keep their height.
        assert page.locator(".entry .opt:not(.later)").first.bounding_box()["height"] >= 52
        assert page.locator(".entry .opt.later").first.bounding_box()["height"] >= 44
        bar = page.locator("#save-bar").bounding_box()["height"]
        btn = page.locator("#btn-save").bounding_box()
        assert bar <= 42, bar                    # 77 px before 1.4.5
        assert btn["height"] >= 34 and btn["width"] >= 160
        assert no_real_errors(page) == []
