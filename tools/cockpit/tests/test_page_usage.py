"""1.17 — la consommation on the page, in a headless browser (Microsoft Edge
through Playwright), desktop and phone: the banner of a threshold reached on
every screen, the block and « Lancer quand même » with its confirmation and
its log line, the estimate beside « Lancer », the cockpit's own measure under
the gauges — done, or failed and why —, and the thresholds of Paramètres.
The measure's client and the run's are fakes; no chain command runs.

With COCKPIT_SHOTS=<folder>, each step's screenshot is written there."""
import os

import pytest

pytest.importorskip("playwright")

import server  # noqa: E402
import stats as stats_mod  # noqa: E402
import usage  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_page import page, set_relay, settled, until  # noqa: E402,F401
from test_page_phone import H, W, phone  # noqa: E402,F401
from test_runner import script_quick  # noqa: E402
from test_usage import Factory, add_both, add_run, not_logged_in  # noqa: E402


def shot(pg, name, full=False):
    d = os.environ.get("COCKPIT_SHOTS")
    if d:
        os.makedirs(d, exist_ok=True)
        pg.screenshot(path=os.path.join(d, f"{name}.png"), full_page=full)


def errors(pg):
    return [e for e in pg.js_errors if "status of 409" not in e]


def store_of(tmp_path):
    return stats_mod.Store(str(tmp_path / "stats.sqlite"))


def banner(pg):
    b = pg.locator("#usage-banner")
    pg.wait_for_selector("#usage-banner:not(.hidden)")
    return b


def test_the_banner_on_every_screen_and_the_phone(tmp_path, page, phone):
    store = store_of(tmp_path)
    add_both(store, 0.95, 0.40)
    with FakeServer(tmp_path, stats=store) as s:
        s.state.add_app(str(s.app_root))
        page.goto(s.url + "#dashboard")
        b = banner(page)
        assert b.get_attribute("data-level") == "block"
        text = b.inner_text()
        assert "Seuil de blocage atteint : aucune commande ne se lance." in text
        assert "Fenêtre de 5 heures : 95 % — seuil de blocage 90 %, réinitialisation" in text
        assert "Semaine" not in text
        assert page.locator("#gauge-five_hour").get_attribute("data-level") == "block"
        shot(page, "1-bandeau-blocage-tableau-de-bord")
        for route in ("chaine", "answer", "stats", "settings", "accueil"):
            page.goto(s.url + "#" + route)
            banner(page)
            assert "Fenêtre de 5 heures : 95 %" in page.locator("#usage-banner").inner_text(), route
        shot(page, "2-bandeau-blocage-accueil")
        # The phone: the same banner, at the top of its screen.
        phone.goto(s.url + "#dashboard")
        pb = banner(phone)
        assert pb.get_attribute("data-level") == "block" and "95 %" in pb.inner_text()
        box = pb.bounding_box()
        assert box["width"] <= W and box["y"] < H / 2
        shot(phone, "3-bandeau-blocage-telephone")
        assert errors(page) == [] and errors(phone) == []


def test_a_warning_alone_is_a_warning_banner(tmp_path, page, phone):
    store = store_of(tmp_path)
    add_both(store, 0.30, 0.86)
    with FakeServer(tmp_path, stats=store) as s:
        s.state.set_usage_thresholds({"seven_day": {"warn": 80, "block": 95}})
        page.goto(s.url + "#dashboard")
        b = banner(page)
        assert b.get_attribute("data-level") == "warn"
        assert "Seuil d'alerte de consommation atteint." in b.inner_text()
        assert "Semaine : 86 % — seuil d'alerte 80 %" in b.inner_text()
        assert page.locator("#gauge-seven_day").get_attribute("data-level") == "warn"
        shot(page, "4-bandeau-alerte")
        phone.goto(s.url + "#dashboard")
        assert banner(phone).get_attribute("data-level") == "warn"
        shot(phone, "5-bandeau-alerte-telephone")
        # Below every threshold: no banner.
        s.state.set_usage_thresholds({"seven_day": {"warn": 90, "block": 95}})
        page.reload()
        page.wait_for_selector("#gauge-seven_day")
        settled(page)
        assert page.locator("#usage-banner").is_hidden()


def test_the_block_and_lancer_quand_meme(tmp_path, page):
    store = store_of(tmp_path)
    add_both(store, 0.93, 0.40)
    with FakeServer(tmp_path, stats=store, script=script_quick) as s:
        set_relay(s, "Fait.\nNext: run /1_lexique f")
        page.goto(s.url + "#dashboard")
        banner(page)
        asked = []
        answer = {"accept": False}

        def on_dialog(d):
            asked.append(d.message)
            d.accept() if answer["accept"] else d.dismiss()
        page.on("dialog", on_dialog)
        go = page.get_by_role("button", name="Lancer /1_lexique f")
        # Dismissed: nothing launched, nothing logged.
        go.click()
        until(page, lambda: asked)
        settled(page)
        assert len(asked) == 1 and s.clients == []
        q = asked[0]
        assert q.startswith("Seuil de blocage de la consommation atteint :")
        assert "Fenêtre de 5 heures : 93 % utilisés — seuil de blocage 90 %, réinitialisation" in q
        assert "Lancer quand même ? Ce sera noté dans le journal du cockpit." in q
        assert not (tmp_path / "logs" / usage.OVERRIDE_LOG).exists()
        # Accepted: « Lancer quand même » launches, and the log says so.
        answer["accept"] = True
        page.goto(s.url + "#dashboard")
        page.get_by_role("button", name="Lancer /1_lexique f").click()
        until(page, lambda: len(asked) == 2 and s.clients)
        settled(page)
        assert len(s.clients) == 1 and s.clients[0].prompts == ["/1_lexique f"]
        line = (tmp_path / "logs" / usage.OVERRIDE_LOG).read_text(encoding="utf-8")
        assert "« Lancer quand même » : /1_lexique f" in line and "Fenêtre de 5 heures à 93 %" in line
        shot(page, "6-lance-quand-meme")
        assert errors(page) == []


def test_the_estimate_beside_lancer(tmp_path, page, phone):
    store = store_of(tmp_path)
    with FakeServer(tmp_path, stats=store) as s:
        app = str(s.app_root)
        for i, (a, b) in enumerate([(0.10, 0.13), (0.20, 0.24), (0.30, 0.36)]):
            add_run(store, f"s{i}", app, "/1_lexique f", a, b)
        add_run(store, "l0", app, "/2_structure f", 0.10, 0.12)
        set_relay(s, "Fait.\nNext: run /1_lexique f")
        page.goto(s.url + "#dashboard")
        est = page.locator('#next-detail .est[data-command="1_lexique"]')
        est.wait_for()
        assert est.inner_text() == "≈ 4 % de la fenêtre · ≈ 1 % de la semaine"
        assert "Médiane de 3 runs de /1_lexique de cette application" in est.get_attribute("title")
        shot(page, "7-estimation-tableau-de-bord")
        page.goto(s.url + "#chaine")
        step = page.locator('#scr-chaine .est[data-command="1_lexique"]').first
        step.wait_for()
        assert step.inner_text() == "≈ 4 % de la fenêtre · ≈ 1 % de la semaine"
        unknown = page.locator('#scr-chaine .est[data-command="2_structure"]').first
        assert unknown.inner_text() == "coût : inconnu" and "Moins de trois runs" in unknown.get_attribute("title")
        shot(page, "8-estimation-chaine", full=True)
        phone.goto(s.url + "#dashboard")
        pe = phone.locator('#next-detail .est[data-command="1_lexique"]')
        pe.wait_for()
        assert pe.is_visible() and "≈ 4 % de la fenêtre" in pe.inner_text()
        shot(phone, "9-estimation-telephone")
        assert errors(page) == [] and errors(phone) == []


def test_the_measure_at_start_under_the_gauges(tmp_path, page, monkeypatch):
    monkeypatch.setattr(server, "MEASURE_USAGE", True)
    monkeypatch.setattr(server, "MEASURE_CLIENT", Factory())
    monkeypatch.setattr(usage, "SCRATCH", str(tmp_path / "mesure"))
    with FakeServer(tmp_path, stats=store_of(tmp_path), opened=False) as s:
        s.state.add_app(str(s.app_root))
        page.goto(s.url + "#accueil")
        line = page.locator("#home-usage-measure")
        page.wait_for_function("document.getElementById('home-usage-measure').textContent.includes('Dernière mesure')")
        assert "elle a coûté 14 tokens lus, 2 écrits" in line.inner_text()
        assert "(mesure du cockpit)" in page.locator("#hgauge-five_hour").inner_text()
        assert "42 %" in page.locator("#hgauge-five_hour").inner_text()
        assert page.locator("#usage-banner").is_hidden()
        shot(page, "10-mesure-accueil")
        assert errors(page) == []


def test_a_failed_measure_says_why_and_the_page_works(tmp_path, page, monkeypatch):
    monkeypatch.setattr(server, "MEASURE_USAGE", True)
    monkeypatch.setattr(server, "MEASURE_CLIENT", Factory(not_logged_in))
    monkeypatch.setattr(usage, "SCRATCH", str(tmp_path / "mesure"))
    with FakeServer(tmp_path, stats=store_of(tmp_path)) as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_function("document.querySelector('#usage-measure .measure-err')")
        assert "Claude Code n'est pas connecté sur cet ordinateur" in page.locator("#usage-measure").inner_text()
        page.get_by_role("link", name="Chaîne").first.click()
        page.wait_for_selector("#scr-chaine:not(.hidden)")
        shot(page, "11-mesure-echouee")
        assert errors(page) == []


def test_the_thresholds_of_parametres(tmp_path, page):
    store = store_of(tmp_path)
    add_both(store, 0.85, 0.20)
    with FakeServer(tmp_path, stats=store) as s:
        page.goto(s.url + "#settings")
        page.wait_for_selector("#sec-usage")
        assert page.locator("#th-five_hour-warn").input_value() == "90"
        assert page.locator("#th-seven_day-block").input_value() == "90"
        assert page.locator("#usage-banner").is_hidden()
        page.locator("#th-five_hour-warn").fill("80")
        page.locator("#th-five_hour-block").fill("95")
        page.locator("#btn-thresholds").click()
        page.wait_for_selector("#usage-banner:not(.hidden)")
        assert page.locator("#usage-banner").get_attribute("data-level") == "warn"
        assert page.locator("#thresholds-msg").inner_text() == "Enregistré."
        assert s.state.usage_thresholds["five_hour"] == {"warn": 80, "block": 95}
        page.evaluate("document.getElementById('sec-usage').scrollIntoView({block: 'start'})")
        shot(page, "12-parametres-consommation")
        page.locator("#th-seven_day-warn").fill("150")
        page.locator("#btn-thresholds").click()
        page.wait_for_function("document.getElementById('thresholds-msg').textContent.includes('de 1 à 100')")
        assert [e for e in errors(page) if "status of 400" not in e] == []
