"""1.10 — « Données » in a headless browser (Microsoft Edge through
Playwright): both tabs, a text file's preview and an image's, files joined
through the real file input, an entry filled and saved, a file removed, a
committed file made private; « Joindre un fichier » from « À répondre ». No
chain command runs; every repository is a scratch one, nothing is pushed.
Skipped when Playwright or Edge is missing."""
import pytest

pytest.importorskip("playwright")

import server  # noqa: E402
from cmdtests import unanswered_questions  # noqa: E402
from donneesworld import RELEVE, data_world, png  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_chain import git  # noqa: E402
from test_page import browser, no_real_errors, page, stop_run  # noqa: E402,F401

F = "docs/features/f/donnees"


@pytest.fixture(autouse=True)
def _no_push(monkeypatch):
    monkeypatch.setattr(server, "DONNEES_PUSH", False)


def row(page, name):
    return page.locator(f"#dn-list tr[data-name='{name}']")


def test_both_tabs_and_their_previews(tmp_path, page):
    with FakeServer(tmp_path / "s") as s:
        data_world(s.app_root)
        page.goto(s.url + "#dashboard")
        page.get_by_role("link", name="Données").click()
        page.wait_for_selector("#scr-donnees", state="visible")
        assert page.locator("#nav-donnees").get_attribute("aria-current") == "page"
        page.get_by_role("tab", name="De l'application").click()
        row(page, "fleche.png").wait_for()
        assert page.locator("#dn-folder").inner_text() == "docs/donnees/"
        assert "the arrow shown beside each item of a list" in row(page, "fleche.png").inner_text()
        row(page, "fleche.png").locator("button.dn-show").click()
        img = page.locator("#dn-preview img")
        img.wait_for()
        page.wait_for_function("document.querySelector('#dn-preview img').naturalWidth > 0")
        assert img.evaluate("i => [i.naturalWidth, i.naturalHeight]") == [160, 96]
        page.get_by_role("tab", name="De la fonctionnalité").click()
        row(page, "releve-2026-09-14.csv").wait_for()
        assert page.locator("#dn-folder").inner_text() == F + "/"
        assert page.locator("#dn-tab-feature").get_attribute("aria-selected") == "true"
        row(page, "releve-2026-09-14.csv").locator("button.dn-show").click()
        pre = page.locator("#dn-preview pre")
        pre.wait_for()
        assert pre.inner_text().splitlines() == RELEVE.splitlines()
        assert no_real_errors(page) == []


def test_join_fill_save_remove_and_private(tmp_path, page):
    with FakeServer(tmp_path / "s") as s:
        data_world(s.app_root)
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#donnees")
        page.get_by_role("tab", name="De la fonctionnalité").click()
        row(page, "releve-2026-09-14.csv").wait_for()
        a, b = tmp_path / "export.csv", tmp_path / "capture.png"
        a.write_text("a;b\n1;2\n", encoding="utf-8")
        b.write_bytes(png(20, 10))
        # The real file input, several at once.
        assert page.locator("#dn-input").get_attribute("multiple") is not None
        page.set_input_files("#dn-input", [str(a), str(b)])
        row(page, "capture.png").locator(".dn-form").wait_for()
        assert (s.app_root / F / "export.csv").read_text(encoding="utf-8") == "a;b\n1;2\n"
        assert (s.app_root / F / "capture.png").read_bytes() == png(20, 10)
        # Today by default.
        form = row(page, "export.csv").locator(".dn-form")
        assert form.locator("input[name=date]").input_value() == page.evaluate("DN.data.today")
        form.locator("input[name=what]").fill("an export of the operations")
        form.locator("input[name=source]").fill("the bank's site")
        form.locator("input[name=private]").check()
        assert "hors de git" in form.inner_text()
        # Not filled: refused, said, nothing committed.
        page.locator("#dn-save").click()
        page.wait_for_selector("#dn-msg.err")
        assert "capture.png" in page.locator("#dn-msg").inner_text()
        f2 = row(page, "capture.png").locator(".dn-form")
        f2.locator("input[name=what]").fill("a screenshot of the bank's app")
        f2.locator("input[name=source]").fill("the Product Owner")
        # The committed one made private: the page says what stays in the history.
        row(page, "releve-2026-09-14.csv").locator("button.dn-edit").click()
        row(page, "releve-2026-09-14.csv").locator("input[name=private]").check()
        assert "reste dans l'historique" in row(page, "releve-2026-09-14.csv").locator(".dn-history").inner_text()
        page.locator("#dn-save").click()
        page.wait_for_function("document.getElementById('dn-msg').textContent.includes('Enregistré')")
        msg = page.locator("#dn-msg").inner_text()
        assert "donnees: export.csv joint, privé, capture.png joint, releve-2026-09-14.csv privé" in msg
        assert "releve-2026-09-14.csv : sorti de l'index de git, il reste dans l'historique" in msg
        assert git(s.app_root, "log", "-1", "--format=%s").startswith("donnees: ")
        files = git(s.app_root, "ls-files").split()
        assert F + "/capture.png" in files and F + "/export.csv" not in files and F + "/releve-2026-09-14.csv" not in files
        assert row(page, "export.csv").locator(".badge.warn").inner_text() == "privé"
        # Removed: it asks, and the file goes with its entry.
        row(page, "capture.png").locator("button.dn-remove").click()
        assert row(page, "capture.png").count() == 0
        assert "Changements non enregistrés" in page.locator("#dn-dirty").inner_text()
        page.locator("#dn-save").click()
        page.wait_for_function("document.getElementById('dn-msg').textContent.includes('capture.png retiré')")
        assert not (s.app_root / F / "capture.png").exists()
        assert "capture.png" not in (s.app_root / F / "donnees.md").read_text(encoding="utf-8")
        # The one refusal above is the browser's only complaint.
        assert [e for e in no_real_errors(page) if "status of 400" not in e] == []


def test_save_refused_while_a_run_goes(tmp_path, page):
    from test_runner import script_until_interrupted
    with FakeServer(tmp_path / "s", script=script_until_interrupted) as s:
        data_world(s.app_root)
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.goto(s.url + "#donnees")
        page.get_by_role("tab", name="De la fonctionnalité").click()
        row(page, "releve-2026-09-14.csv").wait_for()
        page.wait_for_function("document.getElementById('dn-save').disabled")
        assert page.locator("#dn-run-note").is_visible()
        stop_run(s)


def test_join_a_file_from_a_question(tmp_path, page):
    with FakeServer(tmp_path / "s") as s:
        data_world(s.app_root)
        page.goto(s.url + "#answer")
        page.wait_for_selector(".entry")
        card = page.locator(".entry", has=page.locator("b", has_text="Q4"))
        others = page.locator(".entry", has=page.locator("b", has_text="Q2"))
        assert others.locator(".q-join").count() == 0
        assert "docs/features/f/donnees/" in card.locator(".q-join").inner_text()
        # The question's other options stay.
        assert card.locator(".opt").count() == 3
        f = tmp_path / "releve-2026-09-30.csv"
        f.write_text(RELEVE, encoding="utf-8")
        card.locator("input.q-join-input").set_input_files(str(f))
        card.locator(".dn-form").wait_for()
        card.locator("input[name=what]").fill("a statement of operations, as the bank's site exports it")
        card.locator("input[name=source]").fill("the bank's account page")
        card.locator("input[name=private]").check()
        card.locator("button.q-join-save").click()
        page.wait_for_selector(".notice.ok.q-joined")
        note = page.locator(".notice.ok.q-joined").inner_text()
        assert "« releve-2026-09-30.csv » joint dans docs/features/f/donnees/" in note and "Answer: releve-2026-09-30.csv" in note
        assert (s.app_root / F / "releve-2026-09-30.csv").read_text(encoding="utf-8") == RELEVE
        qfile = s.feat / "questions-sondeur-02.md"
        assert "Answer: releve-2026-09-30.csv" in qfile.read_text(encoding="utf-8")
        assert 4 not in unanswered_questions(str(qfile))
        page.wait_for_function("!Array.from(document.querySelectorAll('.entry b')).some(b => b.textContent === 'Q4' && b.closest('.entry').querySelector('.q-join'))")
        assert F + "/releve-2026-09-30.csv" not in git(s.app_root, "ls-files")
        assert no_real_errors(page) == []
