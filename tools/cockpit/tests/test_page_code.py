"""Cockpit 1.5 — the « Code » tab, the notifications and the title count,
in a headless Edge, against the real server over a fake application folder
and a fake SDK client. No chain command runs."""
import shutil
import sqlite3

import pytest

pytest.importorskip("playwright")
from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock, ToolResultBlock, UserMessage  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

import stats  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_codelots import hand_folder, verdict  # noqa: E402
from test_runner import result, script_with_permission  # noqa: E402

FAKE_NOTIFICATION = """
window.__notes = []; window.__vis = "visible"; window.__asked = 0;
Object.defineProperty(document, "visibilityState", {get: () => window.__vis, configurable: true});
Object.defineProperty(document, "hidden", {get: () => window.__vis !== "visible", configurable: true});
class FakeNotification {
  constructor(title, opts) { this.title = title; this.body = (opts || {}).body; window.__notes.push(this); }
  close() {}
}
FakeNotification.permission = "default";
FakeNotification.requestPermission = async () => { window.__asked++; FakeNotification.permission = "granted"; return "granted"; };
window.Notification = FakeNotification;
"""


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge")
        except Exception as e:
            pytest.skip(f"Edge indisponible : {e}")
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    ctx.add_init_script(FAKE_NOTIFICATION)
    pg = ctx.new_page()
    pg.js_errors = []
    pg.on("pageerror", lambda e: pg.js_errors.append(str(e)))
    yield pg
    ctx.close()


def with_lots(s, tmp_path):
    """The ten hand-written lots of test_codelots in the fake feature `f`,
    without the fake folder's empty bugfix-01/ (/8_code would act on it) nor
    its waiting Détailleur file (it names lot-04 and lot-07)."""
    shutil.rmtree(s.feat / "bugfix-01")
    (s.feat / "code" / "blocked_detailleur.md").unlink()
    _, src = hand_folder(tmp_path / "src")
    shutil.copytree(src / "code", s.feat / "code", dirs_exist_ok=True)
    shutil.copytree(src / "architecte", s.feat / "architecte", dirs_exist_ok=True)


def store_with(path, lots):
    """A store holding one /8_code run of `f` whose passes name `lots` {lot: seconds}."""
    st = stats.Store(str(path))
    db = sqlite3.connect(path)
    db.execute("INSERT INTO runs (id, feature, command, started_at, ended_at) VALUES "
               "('r1', 'f', '/8_code f', '2026-10-06T09:00:00', '2026-10-06T11:00:00')")
    for i, (lot, sec) in enumerate(lots.items()):
        db.execute("INSERT INTO agent_passes (run_id, tool_use_id, agent, description, started_at, ended_at, duration_s,"
                   " input_tokens, cache_read_tokens, cache_creation_tokens, output_tokens, lot, folder)"
                   " VALUES ('r1', ?, 'realisateur', ?, ?, ?, ?, 100, 2000, 50, NULL, ?, '')",
                   (f"t{i}", f"Code {lot}", f"2026-10-06T09:{10 * i:02d}:00", f"2026-10-06T09:{10 * i + 5:02d}:00", sec, lot))
    db.commit()
    db.close()
    return st


def open_code(page, url):
    page.goto(url + "#chaine")
    page.wait_for_selector("#flow-main li.step")
    page.locator("#tab-main-code").click()
    page.wait_for_selector("#lots-main tbody tr[data-lot]")


def test_both_tabs_the_lots_and_a_lot_opened(tmp_path, page):
    with FakeServer(tmp_path, stats=store_with(tmp_path / "s.sqlite", {"lot-01": 600})) as s:
        with_lots(s, tmp_path)
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        assert page.locator("#chaine-amont").is_visible() and not page.locator("#chaine-code").is_visible()
        # « 2 / 10 en PASS » on the /8_code step opens « Code ».
        page.locator("#step-main-8_code .lots-link").click()
        page.wait_for_selector("#lots-main tbody tr[data-lot]")
        assert page.locator("#tab-main-code").get_attribute("aria-selected") == "true"
        assert page.locator("#code-count").inner_text() == "2 / 10"
        rows = page.locator("#lots-main tbody tr[data-lot]")
        assert rows.count() == 10
        st = dict(zip(rows.evaluate_all("rs => rs.map(r => r.dataset.lot)"), rows.evaluate_all("rs => rs.map(r => r.dataset.state)")))
        assert st["lot-01"] == "passé" and st["lot-04"] == "échoué 3 fois" and st["lot-05"] == "annulé" \
            and st["lot-07"] == "pas commencé" and st["lot-09"] == "bloqué" and st["lot-10"] == "inconnu"
        assert "Entry 3" in page.locator("#lot-main-lot-03").inner_text()
        assert "Arbitre" in page.locator("#lot-main-lot-09").inner_text()
        assert "Architecte · en attente" in page.locator("#lot-main-lot-09").inner_text()
        assert "Realisateur" in page.locator("#lot-main-lot-01").inner_text()          # its pass, its time
        # The estimate waits for two passed lots with a time: one so far.
        assert "Pas encore d'estimation" in page.locator("#code-estimate").inner_text()
        # A lot opened: its sheet rendered read-only, its verdict and the Relecteur's findings, its commits, its passes.
        page.locator("#lot-main-lot-03").click()
        page.wait_for_selector(".lot-detail .mdoc .ln")
        det = page.locator(".lot-detail").inner_text()
        assert "Signatures" in det and "FAIL mineur" in det and "criterion 3 has no test" in det
        assert "Commits et fichiers changés" in det and "Passages d'agent" in det
        # A lot's blocking file → « À répondre », filtered on the lot.
        page.locator("#lot-main-lot-09").get_by_role("button", name="À répondre (1)").click()
        page.wait_for_selector("#lot-filter")
        assert page.locator("#form .entry").count() == 1
        assert "code/lot-09/blocked_realisateur.md" in page.locator("#form").inner_text()
        assert page.js_errors == []


def test_the_estimate_shows_once_two_lots_passed(tmp_path, page):
    with FakeServer(tmp_path, stats=store_with(tmp_path / "s.sqlite", {"lot-01": 600, "lot-02": 1200})) as s:
        with_lots(s, tmp_path)
        open_code(page, s.url)
        t = page.locator("#code-estimate").inner_text()
        assert t.startswith("Reste ≈ 2 h") and "8 lots × la médiane de 2 lots passés (15 min 00 s)" in t


def test_correction_has_the_same_tabs_on_its_own_lots(tmp_path, page):
    with FakeServer(tmp_path) as s:
        bf = s.feat / "bugfix-01"           # the fake folder's own, empty
        (bf / "bug-list.md").write_text("G01 x\n", encoding="utf-8")
        (bf / "desc-bug.md").write_text("### §1.1 — x\n", encoding="utf-8")
        (bf / "code" / "lot-01").mkdir(parents=True)
        (bf / "code" / "sequence.md").write_text("## Order\n\nlot-01\n\n## Blocks\n\nblock-1: lot-01\n\n## Defects\n\n",
                                                 encoding="utf-8")
        (bf / "code" / "lot-01" / "verdict.md").write_text(verdict("PASS"), encoding="utf-8")
        page.goto(s.url + "#correction")
        page.wait_for_selector("#flow-corr li.step")
        page.locator("#tab-corr-code").click()
        page.wait_for_selector("#lots-bugfix-01 tbody tr[data-lot]")
        assert page.locator("#corr-code #code-count").inner_text() == "1 / 1"
        assert page.locator("#tab-corr-code-n").inner_text() == "1 / 1"
        assert page.js_errors == []


def relecteur_passes(lot_dir):
    async def script(c):
        yield AssistantMessage(content=[ToolUseBlock(id="r1", name="Agent", input={
            "subagent_type": "relecteur", "description": "Review lot-07",
            "prompt": "Working folder: docs/features/f. Your lot: lot-07."})], model="m")
        (lot_dir / "verdict.md").write_text(verdict("PASS"), encoding="utf-8")
        yield UserMessage(content=[ToolResultBlock(tool_use_id="r1", content="PASS")])
        yield AssistantMessage(content=[TextBlock("lot-07 passe.\nNext: run /8_code f")], model="m")
        yield result("lot-07 passe.\nNext: run /8_code f")
    return script


def enable_notes(page):
    page.goto(page.url.split("#")[0] + "#settings")
    page.wait_for_selector("#set-notes input")
    for k in ("fin", "autorisation", "lot"):
        page.locator(f"#note-{k}").check()
    assert page.evaluate("window.__asked") == 1                # asked once, the first time one is turned on
    assert "autorise" in page.locator("#note-status").inner_text()


def test_notifications_only_when_the_tab_is_not_in_front(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        page.wait_for_selector("#side")
        enable_notes(page)
        # In front: the page shows it, no notification.
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#perm-banner .perm")
        assert page.evaluate("window.__notes.length") == 0
        page.locator("#perm-banner").get_by_role("button", name="Autoriser").click()
        page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
        assert page.evaluate("window.__notes.length") == 0
        # Not in front: the card and the end each notify; a click brings the tab back, on the screen concerned.
        page.evaluate("window.__vis = 'hidden'")
        page.evaluate("location.hash = '#settings'")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_function("window.__notes.length >= 1")
        n = page.evaluate("window.__notes.map(n => [n.title, n.body])")
        # 1.6: each names its application, and so does the tab's title.
        assert n[0][0] == "app — une autorisation attend" and "Write" in n[0][1]
        title = page.title()
        assert title.startswith("(") and title.endswith(") app — Cockpit")
        page.locator("#perm-banner").get_by_role("button", name="Autoriser").click()
        page.wait_for_function("window.__notes.length >= 2")
        n = page.evaluate("window.__notes.map(n => [n.title, n.body])")
        assert n[1][0] == "app — /1_lexique f — terminé" and n[1][1].startswith("Ensuite : ")
        page.evaluate("window.__notes[1].onclick()")
        page.wait_for_function("location.hash === '#chaine'")
        assert page.js_errors == []


def test_a_lot_that_passes_notifies_and_opens_the_code_tab(tmp_path, page):
    with FakeServer(tmp_path) as s:
        with_lots(s, tmp_path)
        s.script = relecteur_passes(s.feat / "code" / "lot-07")
        page.goto(s.url)
        page.wait_for_selector("#side")
        enable_notes(page)
        open_code(page, s.url)
        assert page.locator("#lot-main-lot-07").get_attribute("data-state") == "pas commencé"
        page.evaluate("window.__vis = 'hidden'")
        s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
        page.wait_for_function("window.__notes.some(n => n.title === 'app — lot-07 est passé')")
        n = page.evaluate("window.__notes.find(n => n.title === 'app — lot-07 est passé').body")
        assert n.startswith("3 / 10 lots en PASS")
        page.evaluate("location.hash = '#settings'")
        page.evaluate("window.__notes.find(n => n.title === 'app — lot-07 est passé').onclick()")
        page.wait_for_selector("#lot-main-lot-07[aria-expanded=true]")
        assert page.locator("#lot-main-lot-07").get_attribute("data-state") == "passé"
        assert page.js_errors == []


def test_stopping_the_cockpit_from_the_page(tmp_path, page):
    with FakeServer(tmp_path) as s:
        page.goto(s.url + "#settings")
        page.wait_for_selector("#btn-quit")
        page.locator("#btn-quit").click()                      # no run: no question
        page.wait_for_selector("#stopped", state="visible")
        assert "arrêté" in page.locator("#stopped").inner_text()


def test_stopping_the_cockpit_during_a_run_asks_first(tmp_path, page):
    from test_runner import script_until_interrupted
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        page.goto(s.url + "#settings")
        page.wait_for_selector("#btn-quit")
        s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
        asked = []

        def answer(d):
            asked.append(d.message)
            d.dismiss() if len(asked) == 1 else d.accept()
        page.on("dialog", answer)
        page.locator("#btn-quit").click()
        page.wait_for_timeout(500)
        assert "/8_code f" in asked[0] and "l'arrête maintenant" in asked[0]
        assert s.rn.is_running(str(s.app_root))               # dismissed: nothing stopped
        page.locator("#btn-quit").click()
        page.wait_for_selector("#stopped", state="visible", timeout=10000)
        assert not s.rn.is_running(str(s.app_root))
        assert "/8_code f" in page.locator("#stopped-text").inner_text()
