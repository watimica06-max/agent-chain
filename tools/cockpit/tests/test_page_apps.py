"""1.6 — the page with several applications, in a headless browser
(Microsoft Edge through Playwright): « Applications », the top bar's
switcher, « Tout mettre à jour »'s report, a run going in another
application. Skipped when Playwright or Edge is missing. No chain command
runs, nothing is installed: the install is a fake here — test_apps.py runs
the real one on scratch repositories."""
import os

import pytest

pytest.importorskip("playwright")

import chain  # noqa: E402
import server  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_apps import second_app  # noqa: E402
from test_page import browser, no_real_errors, page  # noqa: E402,F401
from test_runner import script_until_interrupted  # noqa: E402

STATES = {"app": chain.UP_TO_DATE, "belivo": chain.ABSENT, "tardive": chain.BEHIND, "bricolee": chain.MODIFIED}


@pytest.fixture
def per_app_chain(monkeypatch):
    def fake(app):
        st = STATES.get(os.path.basename(app), chain.UP_TO_DATE)
        return {"state": st, "summary": {chain.UP_TO_DATE: "Chaîne à jour — 93d18fc du 2026-10-06",
                                         chain.ABSENT: "Chaîne absente — aucun .claude/chain-version.json",
                                         chain.BEHIND: "Chaîne en retard de 2 commits — installée : 5974c32 du 2026-10-05",
                                         chain.MODIFIED: "Chaîne modifiée sur place — 1 fichier : .claude/agents/b.md"}[st],
                "subjects": [], "modified": [], "chain_commit": "93d18fc", "chain_date": "2026-10-06"}
    monkeypatch.setattr(server, "chain_state", fake)


def with_belivo(s):
    b = s.tmp / "belivo"
    second_app(b)
    s.state.add_app(str(b))
    s.state.open_pair(str(b), "g")
    s.state.activate(str(s.app_root))
    return b


def test_applications_screen_rows_rename_remove(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path) as s:
        b = with_belivo(s)
        page.on("dialog", lambda d: d.accept("Belivo") if d.type == "prompt" else d.accept())
        page.goto(s.url + "#apps")
        page.wait_for_selector(".app-row")
        rows = page.locator(".app-row")
        assert rows.count() == 2
        first, second = rows.nth(0), rows.nth(1)
        assert "active" in first.inner_text() and "is-active" in first.get_attribute("class")
        t2 = second.inner_text()
        assert "belivo" in t2 and str(b) in t2 and "absente" in t2
        assert "1 question · 0 blocage" in t2 and "Répondre aux questions" in t2
        assert second.get_by_role("button", name="Installer la chaîne").is_visible()
        assert first.get_by_role("button", name="Ouverte").is_disabled()
        # Renommer: the name, in the list, the top bar's switcher, config.json.
        second.get_by_role("button", name="Renommer").click()
        page.wait_for_function("[...document.querySelectorAll('.app-row .nm')].some(e => e.textContent === 'Belivo')")
        assert s.state.name_of(str(b)) == "Belivo"
        # Retirer de la liste: asked first, the folder never touched.
        page.locator(".app-row", has_text="Belivo").get_by_role("button", name="Retirer de la liste").click()
        page.wait_for_function("document.querySelectorAll('.app-row').length === 1")
        assert os.path.isdir(b / "docs" / "features" / "g") and len(s.state.apps()) == 1
        assert "Son dossier n'a pas été touché" in page.locator("#apps-msg").inner_text()
        assert no_real_errors(page) == []


def test_the_top_bar_switches_without_going_through_the_screen(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path) as s:
        with_belivo(s)
        page.goto(s.url)
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        assert page.locator("#tb-app").inner_text().startswith("app")
        assert page.title().endswith("app — Cockpit")
        assert page.locator("#cnt-q").inner_text() != "1"
        page.locator("#tb-app").click()
        items = page.locator("#app-menu button[role=menuitem]")
        assert items.count() == 3 and items.nth(0).get_attribute("aria-current") == "true"
        page.locator("#app-menu button", has_text="belivo").click()
        page.wait_for_function("document.getElementById('tb-app').textContent.startsWith('belivo')")
        page.wait_for_function("document.getElementById('cnt-q').textContent === '1'")
        assert page.locator("#tb-folder").inner_text() == "g"
        assert page.title().endswith("belivo — Cockpit")
        # Every screen reads it: « Chaîne » shows its feature, « Statistiques » filters on it.
        page.get_by_role("link", name="Chaîne").first.click()
        page.wait_for_function("document.getElementById('chaine-feature').textContent === 'g'")
        page.get_by_role("link", name="Statistiques").first.click()
        page.wait_for_function("document.getElementById('st-app').options[0]?.text === 'belivo (active)'")
        assert page.locator("#st-feature option").first.inner_text() == "g (ouverte)"
        # The chain banner is the active application's: absent here.
        assert "Chaîne absente" in page.locator("#chain-banner").inner_text()
        assert s.state.app_folder.endswith("belivo")
        assert no_real_errors(page) == []


def test_update_all_report(tmp_path, page, per_app_chain, monkeypatch):
    installed = []

    def fake_install(app, root, confirm=False, push=True):
        assert not confirm                              # never in bulk
        installed.append(os.path.basename(app))
        return {"commit": "93d18fc", "date": "2026-10-06", "written": [], "removed": [], "app_commit": "4b1e0a2",
                "message": "chain: 93d18fc 2026-10-06", "pushed": True, "push_error": None}
    monkeypatch.setattr(chain, "install", fake_install)
    with FakeServer(tmp_path) as s:
        with_belivo(s)
        for name in ("tardive", "bricolee"):
            second_app(s.tmp / name)
            s.state.add_app(str(s.tmp / name))
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#apps")
        page.wait_for_selector(".app-row")
        page.get_by_role("button", name="Tout mettre à jour").click()
        page.wait_for_selector("#apps-report .line")
        lines = page.locator("#apps-report .line")
        assert lines.count() == 4
        got = {lines.nth(i).locator("b").inner_text(): lines.nth(i).get_attribute("data-outcome") for i in range(4)}
        assert got == {"app": "skipped", "belivo": "skipped", "tardive": "updated", "bricolee": "skipped"}
        assert installed == ["tardive"]
        rep = page.locator("#apps-report").inner_text()
        assert "4b1e0a2" in rep and "déjà à jour" in rep and "jamais en bloc" in rep
        for n in ("belivo", "bricolee"):
            assert page.locator("#apps-report .line", has_text=n).get_by_role("button", name="Ouvrir son installation").is_visible()
        assert page.locator("#apps-report .line", has_text="tardive").get_by_role("button").count() == 0
        assert no_real_errors(page) == []


def test_a_run_going_in_another_application(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        b = with_belivo(s)
        s.state.activate(str(b))
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#busy-banner", state="visible")
        assert "« app »" in page.locator("#busy-banner").inner_text()
        assert page.locator("#tb-run").text_content().startswith("app · /1_lexique f")
        # Not its own: no step « en cours » here, every launch disabled and saying why.
        assert page.locator("#flow-main li.step[data-state='en cours']").count() == 0
        launch = page.locator("#flow-main").get_by_role("button", name="Lancer").first
        assert launch.is_disabled() and "« app »" in launch.get_attribute("title")
        # « Arrêter » acts on it from here.
        page.locator("#tb-stop").click()
        page.wait_for_selector("#busy-banner", state="hidden")
        assert not s.rn.is_running(str(s.app_root))
        assert page.locator("#tb-run").inner_text() == "Au repos"
        assert no_real_errors(page) == []
