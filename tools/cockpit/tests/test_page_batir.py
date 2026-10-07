"""« Bâtir » in the page, in a headless browser (Microsoft Edge through
Playwright): the step in « Chaîne », between « Établir les conventions »
and « Découper en lots », its report once built; the Bâtisseur's tutorial
in « À répondre », « fait » chosen; a request to the Architecte never
shown there. No chain command runs."""
import pytest

pytest.importorskip("playwright")

import batirworld as bw  # noqa: E402
import server  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_page import browser, no_real_errors, page  # noqa: E402,F401


@pytest.fixture(autouse=True)
def _conventions_at(monkeypatch):
    """The commit that last changed the conventions: read with git by the
    server; a scratch folder is no repository."""
    monkeypatch.setattr(server, "conventions_commit", lambda app: bw.COMMIT)


def premiere(tmp_path):
    s = FakeServer(tmp_path)
    feat = bw.upstream_done(s.app_root)
    s.state.open_pair(str(s.app_root), "premiere")
    return s, feat


def flow_ids(page):
    return page.locator("#flow-main > li").evaluate_all("ls => ls.map(l => l.id.replace('step-main-', ''))")


def test_the_step_between_conventions_and_the_split(tmp_path, page):
    s, feat = premiere(tmp_path)
    with s:
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#step-main-batir")
        ids = flow_ids(page)
        assert ids[ids.index("conventions"):ids.index("conventions") + 3] == ["conventions", "batir", "7_lots"]
        st = page.locator("#step-main-batir")
        assert st.locator(".sname").inner_text() == "Construire le projet"
        assert st.locator(".scmd").inner_text() == "/batir premiere"
        assert st.get_attribute("data-state") == "à faire" and "is-next" in st.get_attribute("class")
        assert st.locator(".built").count() == 0                       # not built: no report
        st.get_by_role("button", name="Pourquoi ?").click()
        assert "BAT-5" in st.locator(".whybox").inner_text() and "7_lots.md:97" in st.locator(".whybox").inner_text()
        assert no_real_errors(page) == []


def test_its_report_once_built(tmp_path, page):
    s, feat = premiere(tmp_path)
    bw.report(feat)
    bw.profile(s.app_root)
    with s:
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#step-main-batir .built")
        st = page.locator("#step-main-batir")
        assert st.get_attribute("data-state") == "faite"
        # The application's report, one for every feature, and whose run wrote it.
        assert st.locator(".built > .muted").inner_text() == \
            "docs/BUILD_REPORT.md — le rapport de l'application, écrit par le run de « premiere »"
        rows = st.locator(".built tbody tr").all_inner_texts()
        assert len(rows) == 3
        assert "build" in rows[0] and ".\\gradlew.bat build" in rows[0] and "✓ code 0" in rows[0] and "84 s" in rows[0]
        assert "assemble app" in rows[2] and "12 s" in rows[2]
        assert st.locator(".built .targets").inner_text() == "Profil de déploiement : Téléphone · android · phone"
        # « Pourquoi ? »: the report's status line and its commit.
        st.get_by_role("button", name="Pourquoi ?").click()
        why = st.locator(".whybox").inner_text()
        assert "BAT-6" in why and "« ## Status: built »" in why and bw.COMMIT[:7] in why
        # The next step is the split.
        assert "is-next" in page.locator("#step-main-7_lots").get_attribute("class")
        assert no_real_errors(page) == []


def test_the_tutorial_and_fait_chosen(tmp_path, page):
    s, feat = premiere(tmp_path)
    bw.report(feat, status="blocked")
    bw.blocked(feat)
    bw.request(feat)                     # the Architecte's: never shown here
    with s:
        page.goto(s.url + "#answer")
        page.wait_for_selector("#form .entry")
        assert page.locator("#form .entry").count() == 1
        assert "architecte/" not in page.locator("#form").inner_text()
        e = page.locator("#form .entry").first
        assert "Construire le projet" in e.locator(".head").inner_text()
        # Numbered steps, one action each.
        steps = e.locator(".tuto ol > li")
        assert steps.count() == 7
        assert steps.nth(0).inner_text().startswith("Ouvrez https://adoptium.net/")
        # Paths and commands set apart: the command to type on its own line,
        # the paths, the file and the address in their own font.
        assert steps.nth(4).locator("pre.cmd").inner_text() == "java -version"
        codes = e.locator(".tuto code").all_inner_texts()
        assert ".msi" in codes and "C:\\Users\\vous\\Downloads" in codes and "/batir premiere" in codes
        assert "https://adoptium.net/fr/temurin/releases/?version=17" in codes
        assert "`" not in e.locator(".tuto").inner_text()
        # The decision: « fait », an option, chosen.
        chosen = e.locator(".opt.chosen")
        assert chosen.count() == 1 and chosen.inner_text().startswith("fait")
        page.get_by_role("button", name="Enregistrer").click()
        page.wait_for_function("() => !document.querySelector('#form .entry')", timeout=10000)
        text = (feat / "blocked_batisseur.md").read_text(encoding="utf-8")
        assert text.rstrip().endswith("## Decision\n\nfait")
        # Now the Bâtisseur applies it: « Bâtir » is to do again.
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#step-main-batir")
        st = page.locator("#step-main-batir")
        assert st.get_attribute("data-state") == "à faire"
        st.get_by_role("button", name="Pourquoi ?").click()
        assert "BAT-3" in st.locator(".whybox").inner_text()
        assert no_real_errors(page) == []
