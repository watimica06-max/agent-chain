"""1.18 — « Pilote automatique » on the page, in a headless browser (Microsoft
Edge through Playwright), desktop and phone: the panel and its three ready
settings, the full form with every bound and the step to reach, a programme
scheduled (« L'ordinateur doit rester allumé… »), a programme running, one
waiting for a reset, and both stops — one from the phone. The run's client is
a fake; no chain command runs.

With COCKPIT_SHOTS=<folder>, each step's screenshot is written there."""
import os
from datetime import datetime, timedelta

import pytest

pytest.importorskip("playwright")

import stats as stats_mod  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_page import page, set_relay, settled, until  # noqa: E402,F401
from test_page_phone import phone  # noqa: E402,F401
from test_runner import script_until_interrupted  # noqa: E402
from test_usage import add_both, add_run  # noqa: E402


def shot(pg, name, full=False):
    d = os.environ.get("COCKPIT_SHOTS")
    if d:
        os.makedirs(d, exist_ok=True)
        pg.screenshot(path=os.path.join(d, f"{name}.png"), full_page=full)


def errors(pg):
    return [e for e in pg.js_errors if "status of 409" not in e]


def to_card(pg):
    pg.wait_for_selector("#pilot-card .pl-head")
    pg.evaluate("document.getElementById('pilot-card').scrollIntoView({block: 'start'})")


def test_the_panel_the_form_and_a_programme_scheduled(tmp_path, page):
    with FakeServer(tmp_path, stats=stats_mod.Store(str(tmp_path / "stats.sqlite"))) as s:
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#dashboard")
        to_card(page)
        presets = page.locator("#pilot-card .pl-preset").all_inner_texts()
        assert presets == ["Maintenant, jusqu'à ce qu'on ait besoin de moi", "Cette nuit, 1 h – 7 h", "Pendant 2 heures"]
        shot(page, "1-pilote-repos")
        page.locator("#pl-form-toggle").click()
        page.wait_for_selector("#pilot-form")
        # « Étape à atteindre »: before or once done, and the flow's steps in its order.
        opts = page.locator("#pl-step option").all_inner_texts()
        assert opts[:3] == ["— aucune —", "1. Fixer le vocabulaire (/1_lexique)", "2. Structurer la fiche produit (/2_structure)"]
        assert "13. Contrôler la feature (/9_controle)" in opts
        assert any(o.startswith("1. Diagnostiquer les écarts") for o in opts)        # the open correction's
        assert page.locator("#pl-step-when option").all_inner_texts() == ["S'arrêter avant", "S'arrêter une fois faite"]
        a, b = datetime.now() + timedelta(hours=3), datetime.now() + timedelta(hours=5)
        page.locator("input[name=pl-start][value=slot]").check()
        page.locator("#pl-from").fill(a.strftime("%H:%M"))
        page.locator("#pl-to").fill(b.strftime("%H:%M"))
        page.locator("#pl-lots").fill("4")
        page.locator("#pl-step").select_option("main:9_controle")
        page.locator("#pl-name").fill("Ma nuit de code")
        page.locator("#pl-save").check()
        page.evaluate("document.getElementById('pilot-form').scrollIntoView({block: 'start'})")
        shot(page, "2-pilote-programme-complet")
        page.locator("#pl-go").click()
        page.wait_for_selector('#pilot-live[data-status="programmé"]')
        assert page.locator("#pilot-notice").inner_text() == "L'ordinateur doit rester allumé et réveillé jusque-là."
        bound = page.locator("#pilot-bound").inner_text()
        assert "après 4 lots encore" in bound and "avant « Contrôler la feature »" in bound and bound.startswith("S'arrête ")
        assert page.locator("#tb-pilot").inner_text() == "Pilote : programmé"
        assert [x["name"] for x in s.state.programmes()] == ["Ma nuit de code"]
        to_card(page)
        shot(page, "3-pilote-programme")
        page.locator("#pilot-cancel").click()
        page.wait_for_selector("#pilot-last")
        assert "Annulé avant son démarrage" in page.locator("#pilot-last").inner_text()
        assert page.locator("#tb-pilot").is_hidden()
        assert page.locator(".pl-saved li[data-name='Ma nuit de code']").count() == 1
        assert s.clients == [] and errors(page) == []


def test_a_programme_running_then_stopped_from_the_phone(tmp_path, page, phone):
    with FakeServer(tmp_path, stats=stats_mod.Store(str(tmp_path / "stats.sqlite")), script=script_until_interrupted) as s:
        set_relay(s, "Fini.\nNext: run /1_lexique f")
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#dashboard")
        to_card(page)
        page.locator("#pilot-card .pl-preset[data-preset=besoin]").click()
        page.wait_for_selector('#pilot-live[data-status="en cours"] #pilot-stop-now')
        until(page, lambda: s.clients)
        page.wait_for_function("document.getElementById('pilot-doing').textContent.includes('/1_lexique f tourne')")
        assert page.locator("#pilot-bound").inner_text() == "S'arrête quand on a besoin de vous."
        assert page.locator("#pilot-stop-after").inner_text() == "Arrêter après la commande en cours"
        assert page.locator("#tb-pilot").inner_text() == "Pilote : en cours"
        assert s.clients[0].kw["mode"] == "auto"
        page.goto(s.url + "#dashboard")
        to_card(page)
        shot(page, "4-pilote-en-cours")
        # The phone: the same panel, its two stops.
        phone.goto(s.url + "#dashboard")
        phone.wait_for_selector('#pilot-live[data-status="en cours"]')
        phone.evaluate("document.getElementById('pilot-card').scrollIntoView({block: 'start'})")
        assert phone.locator("#pilot-stop-after").is_visible() and phone.locator("#pilot-stop-now").is_visible()
        shot(phone, "5-pilote-en-cours-telephone")
        phone.locator("#pilot-stop-now").tap()
        phone.wait_for_selector("#pilot-last")
        assert "Arrêté maintenant, à votre demande." in phone.locator("#pilot-last").inner_text()
        shot(phone, "6-pilote-arrete-telephone")
        # The computer's page is told.
        page.wait_for_selector("#pilot-last")
        last = page.locator("#pilot-last").inner_text()
        assert "Arrêté maintenant, à votre demande." in last and "1 commande, 0 lot codé" in last
        assert s.clients[0].interrupted.is_set()
        to_card(page)
        shot(page, "7-pilote-arrete")
        assert errors(page) == [] and errors(phone) == []


def test_a_programme_waiting_for_the_reset(tmp_path, page):
    store = stats_mod.Store(str(tmp_path / "stats.sqlite"))
    with FakeServer(tmp_path, stats=store) as s:
        for i, (a, b) in enumerate([(0.10, 0.16), (0.20, 0.26), (0.30, 0.36)]):
            add_run(store, f"l{i}", str(s.app_root), "/1_lexique f", a, b)
        add_both(store, 0.86, 0.30)                  # 86 % + ≈ 6 % for /1_lexique ≥ 90 %: wait
        set_relay(s, "Fini.\nNext: run /1_lexique f")
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#dashboard")
        to_card(page)
        page.locator("#pilot-card .pl-preset[data-preset=besoin]").click()
        page.wait_for_selector('#pilot-live[data-status="attend"]')
        doing = page.locator("#pilot-doing").inner_text()
        assert doing.startswith("Attend la réinitialisation de la fenêtre de 5 heures,") and s.clients == []
        assert page.locator("#tb-pilot").inner_text() == "Pilote : attend"
        to_card(page)
        shot(page, "8-pilote-attend-la-reinitialisation")
        page.locator("#pilot-cancel").click()
        page.wait_for_selector("#pilot-last")
        assert "Arrêté à votre demande." in page.locator("#pilot-last").inner_text()
        assert s.clients == [] and errors(page) == []
