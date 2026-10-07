"""1.7 — « Nouvelle application » in a headless browser (Microsoft Edge
through Playwright): the form refusing a folder, normalising the names and
showing the idea file; the creation's progress, a step that fails and «
Reprendre »; the new application opened on /1_lexique, with « À fournir
avant le code », its « Déployer » opening « Déploiement » with no profile
yet (1.8). Skipped when Playwright or Edge is
missing. Every repository is a scratch one; no chain command runs."""
import pytest

pytest.importorskip("playwright")

import create  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_chain import write  # noqa: E402
from test_create import IDEA, chain_root, idea  # noqa: E402,F401
from test_page import browser, no_real_errors, page  # noqa: E402,F401

pytestmark = pytest.mark.real_chain


def open_form(page, s):
    page.goto(s.url + "#apps")
    page.wait_for_selector(".app-row")
    page.get_by_role("button", name="Nouvelle application").click()
    page.wait_for_selector("#new-app:not(.hidden)")


def fill(page, tmp_path, name="Mon Appli Été", feature="premiere-app"):
    page.locator("#nf-parent").fill(str(tmp_path / "dev"))
    page.locator("#nf-name").fill(name)
    page.get_by_role("button", name="Parcourir…").nth(1).click()
    page.wait_for_selector("#nf-idea-view:not(.hidden)")
    page.locator("#nf-feature").fill(feature)


def test_the_form_refuses_normalises_and_shows(tmp_path, page, chain_root, idea):
    (tmp_path / "dev" / "pleine").mkdir(parents=True)
    (tmp_path / "dev" / "pleine" / "x.txt").write_text("x")
    with FakeServer(tmp_path / "s", file_picker=lambda initial: str(idea)) as s:
        open_form(page, s)
        fill(page, tmp_path, feature="Ma Feature")
        # The folder's name comes from the application's; the feature is
        # normalised as it is typed.
        assert page.locator("#nf-folder").input_value() == "mon-appli-ete"
        assert page.locator("#nf-feature").input_value() == "ma-feature"
        page.wait_for_function("document.getElementById('nf-path').textContent.endsWith('mon-appli-ete')")
        # The idea file, shown read-only with « À répondre »'s renderer.
        view = page.locator("#nf-idea-view")
        assert view.locator(".ln.h1").inner_text() == "Mon appli"
        assert "des « tours », un chrono" in view.inner_text()
        assert page.locator("#nf-idea").input_value() == str(idea)
        page.wait_for_selector("#nf-summary li")
        assert page.locator("#nf-summary li").count() == 6
        assert "aucun dépôt distant" in page.locator("#nf-remote-note").inner_text()
        assert page.locator("#nf-create").is_enabled()
        # A folder that exists and is not empty: refused, « Créer » off.
        page.locator("#nf-folder").fill("pleine")
        page.wait_for_function("document.getElementById('nf-err-folder').textContent.includes(\"n'est pas vide\")")
        assert page.locator("#nf-create").is_disabled()
        # A remote: what it must be.
        page.locator("#nf-folder").fill("neuve")
        page.locator("#nf-remote").fill("https://github.com/moi/neuve.git")
        page.wait_for_function("document.getElementById('nf-remote-note').textContent.includes('vide')")
        page.wait_for_function("!document.getElementById('nf-create').disabled")
        assert no_real_errors(page) == []


def test_progress_failure_reprendre_then_lexique(tmp_path, page, chain_root, idea, monkeypatch):
    real = create.Creation.step_socle
    armed = {"on": True}

    def once(self):
        if armed["on"]:
            armed["on"] = False
            raise create.StepError("panne simulée du socle")
        return real(self)
    monkeypatch.setattr(create.Creation, "step_socle", once)
    (tmp_path / "dev").mkdir()
    with FakeServer(tmp_path / "s", file_picker=lambda initial: str(idea)) as s:
        open_form(page, s)
        fill(page, tmp_path)
        page.wait_for_function("!document.getElementById('nf-create').disabled")
        page.locator("#nf-create").click()
        card = page.locator(".mk[data-status='échec']")
        card.wait_for(timeout=60000)
        st = lambda i: card.locator(".mk-steps li").nth(i).get_attribute("data-status")
        assert [st(i) for i in range(6)] == ["fait", "sans objet", "fait", "échec", "à faire", "à faire"]
        assert "panne simulée du socle" in card.inner_text()
        assert ".claude/" in card.inner_text() and "Le cockpit ne supprime jamais" in card.inner_text()
        assert "rien n'est poussé" in card.locator("li[data-step='distant'] .dt").inner_text()
        # « Reprendre »: from the socle on; the application opens on its feature.
        card.get_by_role("button", name="Reprendre").click()
        page.wait_for_selector(".mk[data-status='fait']", timeout=60000)
        done = page.locator(".mk[data-status='fait']")
        assert all(done.locator(".mk-steps li").nth(i).get_attribute("data-status") in ("fait", "sans objet") for i in range(6))
        assert "Lancer /1_lexique premiere-app" in done.inner_text()
        page.wait_for_function("location.hash === '#dashboard'", timeout=10000)
        page.wait_for_function("document.getElementById('next-text').textContent.includes('/1_lexique premiere-app')")
        assert page.locator("#tb-app").inner_text().startswith("Mon Appli Été")
        # À fournir avant le code: the conventions ✗, read from the files.
        prov = page.locator("#provide-card")
        assert prov.is_visible() and prov.locator("li.ko").count() == 1
        # 1.8: « Déployer » opens « Déploiement », which says there is no
        # profile yet — a new application has none.
        page.get_by_role("link", name="Chaîne").first.click()
        page.wait_for_selector("#step-main-test")
        t = page.locator("#step-main-test")
        t.get_by_role("button", name="Déployer").click()
        page.wait_for_selector("#dp-no-profile")
        assert "pas de .claude/deploy.json" in page.locator("#dp-no-profile").inner_text()
        assert no_real_errors(page) == []


def test_the_provide_card_each_line_both_ways(tmp_path, page, chain_root):
    with FakeServer(tmp_path / "s") as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        prov = page.locator("#provide-card")
        assert prov.is_visible() and prov.locator("li.ko").count() == 1
        assert prov.locator("li.ko .mono").inner_text() == "docs/TECHNICAL_CONVENTIONS.md"
        write(s.app_root, "docs/TECHNICAL_CONVENTIONS.md", "# Conventions\n")
        page.reload()
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        assert prov.is_hidden()
        # « Déployer » stays on the test step (1.8: it opens « Déploiement »).
        page.get_by_role("link", name="Chaîne").first.click()
        page.wait_for_selector("#step-main-test")
        assert page.locator("#step-main-test").get_by_role("button", name="Déployer").count() == 1
        assert no_real_errors(page) == []
