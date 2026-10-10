"""1.20 — the « Journal » screen in a headless browser (Microsoft Edge
through Playwright): in « Mesure » beside « Statistiques »; the points à
creuser on top, the totals, the timeline by step and its filters; « Rapport
de fin de cycle » and « Reconstituer le passé » shown first, committed on
confirmation only; the report proposed on the dashboard once the final step
is done; the phone reads it and writes nothing; Paramètres → Journal. No
chain command runs; every repository is a scratch one."""
import os

import pytest

pytest.importorskip("playwright")

import journal  # noqa: E402
import journalworld  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_chain import git  # noqa: E402
from test_page import no_real_errors, page, set_relay, settled  # noqa: E402,F401
from test_page_phone import phone  # noqa: E402,F401

F = "docs/features/f"


def journal_server(tmp_path):
    s = FakeServer(tmp_path)
    journalworld.make(s.app_root)
    return s


def open_journal(pg, s):
    pg.goto(s.url + "#journal")
    pg.wait_for_selector("#jn-timeline .jn-step")
    settled(pg)


def subject(repo):
    return git(repo, "log", "-1", "--format=%s").strip()


def test_the_journal_screen(tmp_path, page):
    with journal_server(tmp_path) as s:
        open_journal(page, s)
        # In « Mesure », after « Statistiques ».
        ids = page.locator("#side a").evaluate_all("as => as.map(a => a.id)")
        assert ids[ids.index("nav-stats") + 1] == "nav-journal"
        assert page.locator("#tb-page").inner_text() == "Journal"
        assert "docs/features/f/journal.md — 8 lignes" in page.locator("#jn-note").inner_text()
        # The points à creuser, on top, each with its reason.
        points = page.locator("#jn-points .jn-point").all_inner_texts()
        text = "\n".join(points)
        assert "n'était pas connecté" in text and "Cette nuit, 1 h – 7 h" in text
        assert "lancée 3 fois de suite" in text and "2 fichiers de blocage de realisateur" in text
        assert page.locator("#jn-points-sec").bounding_box()["y"] < page.locator("#jn-timeline").bounding_box()["y"]
        tiles = page.locator("#jn-tiles .tile").all_inner_texts()
        assert len(tiles) == 6 and tiles[0].startswith("Commandes\n8") and "dont 1 en erreur" in tiles[0]
        assert "2 · 3" in tiles[4] and "1 fichier de questions" in tiles[4]
        # The timeline by step: /1_lexique, /2_structure, /8_code — runs and files under each.
        steps = page.locator("#jn-timeline .jn-step").evaluate_all("ss => ss.map(s => s.dataset.step)")
        assert steps == ["/1_lexique", "/2_structure", "/8_code"]
        lex = page.locator("#jn-timeline .jn-step[data-step='/1_lexique']").inner_text()
        assert "questions-lexicographe-01.md" in lex and "répondu" in lex and "par le Product Owner" in lex
        code = page.locator("#jn-timeline .jn-step[data-step='/8_code']").inner_text()
        assert "décidé" in code and "par l'Arbitre" in code and "programme « Cette nuit, 1 h – 7 h »" in code
        assert page.locator("#jn-timeline .jn-ev.run.failed").count() == 1
        # The filters.
        page.locator("#jn-filter button[data-f='erreurs']").click()
        assert page.locator("#jn-timeline .jn-ev").count() == 1
        page.locator("#jn-filter button[data-f='questions']").click()
        evs = page.locator("#jn-timeline .jn-ev").all_inner_texts()
        assert len(evs) == 3 and all("questions-lexicographe-01.md" in e for e in evs)
        page.locator("#jn-filter button[data-f='blocages']").click()
        assert all("blocked_" in e for e in page.locator("#jn-timeline .jn-ev").all_inner_texts())
        page.locator("#jn-filter button[data-f='tout']").click()
        # Son temps: her answer in 4 h 37 min, the Arbitre's in no time.
        assert "4 h 37 min" in page.locator("#tbl-jn-q").inner_text()
        b = page.locator("#tbl-jn-b").inner_text()
        assert "Arbitre" in b and "Product Owner" in b
        assert page.locator("#tbl-jn-steps tbody tr").count() == 3
        assert "Lancer quand même" in page.locator("#jn-prog").inner_text()
        assert no_real_errors(page) == []


def test_report_and_reconstruction_committed_only_on_confirmation(tmp_path, page):
    with journal_server(tmp_path) as s:
        r = s.app_root
        open_journal(page, s)
        before = git(r, "rev-parse", "HEAD").strip()
        page.locator("#jn-report").click()
        page.wait_for_selector("#jn-panel pre")
        assert page.locator("#jn-panel pre").inner_text().startswith("# Rapport de fin de cycle — f")
        assert not os.path.exists(journal.report_path(str(r), "f"))
        page.get_by_role("button", name="Annuler").click()
        assert page.locator("#jn-panel").is_hidden()
        assert git(r, "rev-parse", "HEAD").strip() == before
        page.locator("#jn-report").click()
        page.get_by_role("button", name="Enregistrer et commiter").click()
        page.wait_for_selector("#jn-msg.ok")
        assert "rapport-cycle.md écrit — commit" in page.locator("#jn-msg").inner_text()
        assert subject(r) == journal.REPORT_MESSAGE and os.path.exists(journal.report_path(str(r), "f"))
        # The reconstruction: nothing left before the journal's first line here.
        page.locator("#jn-rebuild").click()
        page.wait_for_function("document.querySelector('#jn-msg').textContent.includes('Rien à reconstituer')")
        assert no_real_errors(page) == []


def test_reconstruction_shown_then_committed(tmp_path, page):
    with journal_server(tmp_path) as s:
        r = s.app_root
        os.remove(journal.journal_path(str(r), "f"))
        git(r, "commit", "-q", "-am", "x")
        page.goto(s.url + "#journal")
        page.wait_for_selector("#jn-timeline")
        settled(page)
        assert "pas encore écrit" in page.locator("#jn-note").inner_text()
        page.locator("#jn-rebuild").click()
        page.wait_for_selector("#jn-panel pre")
        pre = page.locator("#jn-panel pre").inner_text()
        assert "reconstitué de git seul" in pre and "/1_lexique f" in pre
        assert not os.path.exists(journal.journal_path(str(r), "f"))
        n = page.locator("#jn-panel h3").inner_text()
        page.locator("#jn-panel button.primary").click()
        page.wait_for_selector("#jn-msg.ok")
        assert subject(r).startswith("journal: reconstitution du passé")
        assert journal.read(journal.journal_path(str(r), "f")) and "ligne" in n


def test_the_dashboard_proposes_the_report_once_the_final_step_is_done(tmp_path, page):
    with journal_server(tmp_path) as s:
        set_relay(s, "Fusionné.\nNext: done", command="/fusion f")
        page.goto(s.url + "#dashboard")
        page.wait_for_selector("#next-report")
        page.locator("#next-report").click()
        page.wait_for_selector("#jn-panel pre")
        assert page.locator("#jn-panel h3").inner_text().startswith("Rapport de fin de cycle")
        assert not os.path.exists(journal.report_path(str(s.app_root), "f"))


def test_the_phone_reads_the_journal_and_writes_nothing(tmp_path, phone):
    with journal_server(tmp_path) as s:
        phone.goto(s.url + "#dashboard")
        phone.wait_for_selector("#phone-nav")
        phone.locator("#phone-more").click()
        item = phone.locator("#phone-journal")
        assert "lecture seule" in item.inner_text()
        item.click()
        phone.wait_for_selector("#jn-timeline .jn-step")
        assert phone.locator("#jn-rebuild").is_hidden() and phone.locator("#jn-report").is_hidden()
        assert "Ici, en lecture seule." in phone.locator("#jn-note").inner_text()
        assert phone.locator("#jn-points .jn-point").count() >= 4
        # Nothing scrolls sideways.
        assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
        assert phone.locator("#phone-more").get_attribute("aria-current") == "page"
        assert no_real_errors(phone) == []


def test_parametres_journal_thresholds(tmp_path, page):
    with journal_server(tmp_path) as s:
        page.goto(s.url + "#settings")
        page.wait_for_selector("#sec-journal")
        assert page.locator("#jt-repeat_runs").input_value() == "3"
        page.locator("#jt-repeat_runs").fill("4")
        page.locator("#btn-journal-th").click()
        page.wait_for_selector("#journal-th-msg.ok")
        assert s.state.journal_thresholds["repeat_runs"] == 4
        # Four runs needed now: the three /8_code in place raise nothing.
        open_journal(page, s)
        assert "lancée 3 fois de suite" not in page.locator("#jn-points").inner_text()
