"""1.19 — « Expliquer » on the page, in a headless browser (Microsoft Edge
through Playwright), desktop and phone: the button under a question, the
call going with « Annuler », the explanation under the question, folded once
read and given at once the second time, « Réexpliquer », dropped when the
file changes, and 1.17's threshold with « Lancer quand même ». The call's
client is a fake; no chain command runs.

With COCKPIT_SHOTS=<folder>, each step's screenshot is written there."""
import os

import pytest

pytest.importorskip("playwright")

import explain  # noqa: E402
import server  # noqa: E402
import stats as stats_mod  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_explain import ANSWER, LEXIQUE, PRODUCT, QUESTIONS, Factory, answering  # noqa: E402
from test_page import page, settled, until  # noqa: E402,F401
from test_page_phone import phone  # noqa: E402,F401
from test_usage import add_both  # noqa: E402

QID = "q:questions-sondeur-01.md#1"
CARD = f'.entry[data-id="{QID}"]'


def shot(pg, name, full=False):
    d = os.environ.get("COCKPIT_SHOTS")
    if d:
        os.makedirs(d, exist_ok=True)
        pg.screenshot(path=os.path.join(d, f"{name}.png"), full_page=full)


def errors(pg):
    return [e for e in pg.js_errors if "status of 409" not in e and "status of 502" not in e]


@pytest.fixture
def world(tmp_path, monkeypatch):
    def make(script=None):
        f = Factory(script or answering(wait=0.8))
        monkeypatch.setattr(server, "EXPLAIN_CLIENT", f)
        monkeypatch.setattr(explain, "SCRATCH", str(tmp_path / "scratch"))
        store = stats_mod.Store(str(tmp_path / "stats.sqlite"))
        s = FakeServer(tmp_path, stats=store)
        (s.feat / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
        (s.feat / "questions-sondeur-01.md").write_text(QUESTIONS, encoding="utf-8")
        (s.feat / "lexique.md").write_text(LEXIQUE, encoding="utf-8")
        return s, f, store
    return make


def to_question(pg, s):
    pg.goto(s.url + "#answer")
    pg.wait_for_selector(CARD)
    pg.locator(CARD).scroll_into_view_if_needed()


def test_explain_kept_folded_given_at_once_and_dropped(world, page):
    s, f, store = world()
    with s:
        to_question(page, s)
        card = page.locator(CARD)
        card.get_by_role("button", name="Expliquer").click()
        page.wait_for_selector(f"{CARD} .ex-going")
        assert "Explication en cours…" in card.locator(".ex-going").inner_text()
        assert card.get_by_role("button", name="Annuler").is_visible()
        shot(page, "1-expliquer-en-cours")
        page.wait_for_selector(f"{CARD} details.ex-text[open]")
        body = card.locator(".ex-body").inner_text()
        assert body.startswith("Ce que la question demande — Où ranger le temps passé entre deux épreuves.")
        assert card.locator(".ex-body b").first.inner_text() == "Ce que la question demande"
        assert card.locator(".ex-body li").count() == 2
        assert card.locator(".ex-meta").inner_text().startswith("D'après B2 de desc-produit.md · 3 entrées du lexique · ")
        shot(page, "2-expliquer-explication")
        # Folded once read.
        card.locator("details.ex-text > summary").click()
        assert card.locator("details.ex-text").get_attribute("open") is None
        # Kept: the page opened again shows it folded, and one tap opens it — no call.
        page.reload()
        page.wait_for_selector(f"{CARD} details.ex-text")
        card = page.locator(CARD)
        assert card.locator("details.ex-text").get_attribute("open") is None
        assert card.locator("details.ex-text > summary").inner_text().startswith("Explication — gardée ")
        card.locator("details.ex-text > summary").click()
        assert "Où ranger le temps passé" in card.locator(".ex-body").inner_text()
        assert len(f.clients) == 1
        shot(page, "3-expliquer-gardee")
        # « Réexpliquer »: asked again.
        card.get_by_role("button", name="Réexpliquer").click()
        until(page, lambda: len(f.clients) == 2)
        page.wait_for_selector(f"{CARD} details.ex-text[open]")
        # The file changes: dropped — « Expliquer » again.
        p = s.feat / "questions-sondeur-01.md"
        p.write_text(p.read_text(encoding="utf-8").replace("Answer:\n\n### Q3", "Answer: Non\n\n### Q3", 1), encoding="utf-8")
        page.get_by_role("button", name="Recharger").click()
        page.wait_for_selector(f'{CARD} .explain button.ex-btn')
        assert page.locator(f"{CARD} details.ex-text").count() == 0
        assert errors(page) == []


def test_annuler(world, page):
    s, f, _ = world(answering(wait=20))
    with s:
        to_question(page, s)
        card = page.locator(CARD)
        card.get_by_role("button", name="Expliquer").click()
        card.get_by_role("button", name="Annuler").click()
        page.wait_for_selector(f"{CARD} .ex-err")
        assert card.locator(".ex-err").inner_text() == "Explication annulée."
        assert card.get_by_role("button", name="Expliquer").is_visible()
        shot(page, "4-expliquer-annulee")
        assert errors(page) == []


def test_the_threshold_and_lancer_quand_meme(world, page):
    s, f, store = world()
    with s:
        add_both(store, 0.94, 0.20)
        asked = []
        page.on("dialog", lambda d: (asked.append(d.message), d.accept()))
        to_question(page, s)
        page.locator(CARD).get_by_role("button", name="Expliquer").click()
        page.wait_for_selector(f"{CARD} details.ex-text[open]")
        assert len(asked) == 1 and "Fenêtre de 5 heures : 94 % utilisés — seuil de blocage 90 %" in asked[0]
        assert "consommation.log" in os.listdir(s.tmp / "logs")
        assert errors(page) == []


def test_on_the_phone(world, phone):
    s, f, _ = world()
    with s:
        phone.goto(s.url + "#answer")
        phone.wait_for_selector(CARD)
        card = phone.locator(CARD)
        card.get_by_role("button", name="Expliquer").scroll_into_view_if_needed()
        card.get_by_role("button", name="Expliquer").tap()
        phone.wait_for_selector(f"{CARD} details.ex-text[open]")
        assert "Ce que change chaque option" in card.locator(".ex-body").inner_text()
        card.locator("details.ex-text").scroll_into_view_if_needed()
        shot(phone, "5-expliquer-telephone")
        assert errors(phone) == []
