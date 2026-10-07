"""Cockpit 1.5 — the « Code » tab, the notifications and the title count,
in a headless Edge, against the real server over a fake application folder
and a fake SDK client. No chain command runs."""
import asyncio
import os
import shutil
import sqlite3

import pytest

pytest.importorskip("playwright")
from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock, ToolResultBlock, UserMessage  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

import stats  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_codelots import hand_folder, verdict  # noqa: E402
from test_runner import result, script_quick, script_with_permission  # noqa: E402

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
        assert "Réalisateur" in page.locator("#lot-main-lot-01").inner_text()          # its pass, its time
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
        page.goto(s.url + "#dashboard")
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
        page.goto(s.url + "#dashboard")
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
        # 1.9.1: the order that made the screen vanish, forced — the refresh
        # the run's end starts is answered only once the stop screen shows.
        held, holding = [], {"on": True}

        def hold(route):
            held.append(route) if holding["on"] else route.continue_()
        page.route("**/api/state*", hold)
        page.route("**/api/check*", hold)
        page.locator("#btn-quit").click()
        page.wait_for_selector("#stopped", state="visible", timeout=10000)
        assert not s.rn.is_running(str(s.app_root))
        assert "/8_code f" in page.locator("#stopped-text").inner_text()
        holding["on"] = False
        for r in held:
            r.continue_()
        page.wait_for_timeout(1000)
        assert page.locator("#stopped").is_visible()
        assert page.locator("#stopped-title").inner_text() == "Le cockpit est arrêté"
        assert "arrêté" in page.locator("#stopped").inner_text()


def coder(feat, coded):
    """/8_code as its file says (8_code.md:19-20, :465): N lots from the
    second argument, one by default; `stop.md` looked for after each lot.
    Each lot waits until the test lets it end (`go`)."""
    go = asyncio.Event()

    async def script(c):
        words = c.prompts[0].split()
        n = int(words[2]) if len(words) > 2 else 1
        for lot in ("lot-07", "lot-08", "lot-10")[:n]:
            yield AssistantMessage(content=[ToolUseBlock(id="r-" + lot, name="Agent", input={
                "subagent_type": "realisateur", "description": f"Code {lot}",
                "prompt": f"Working folder: docs/features/f. Your lot: {lot}."})], model="m")
            await go.wait()
            go.clear()
            (feat / "code" / lot / "verdict.md").write_text(verdict("PASS"), encoding="utf-8")
            coded.append(lot)
            yield UserMessage(content=[ToolResultBlock(tool_use_id="r-" + lot, content="PASS")])
            if (feat / "stop.md").exists():
                text = f"Arrêté sur stop.md : {len(coded)} lot sur {n}.\nNext: run /8_code f"
                yield AssistantMessage(content=[TextBlock(text)], model="m")
                yield result(text)
                return
        yield AssistantMessage(content=[TextBlock("Fini.\nNext: run /8_code f")], model="m")
        yield result("Fini.\nNext: run /8_code f")
    return script, go


def launched(s):
    """The lines sent, every run since the server started."""
    return [p for c in s.clients for p in c.prompts]


def wait_until(page, cond):
    for _ in range(200):
        if cond():
            return True
        page.wait_for_timeout(50)
    return cond()


def test_lots_a_coder_beside_the_step_and_in_the_code_tab(tmp_path, page):
    """1.9.1: « Lots à coder », 1 by default, at most the lots not yet done;
    1 launches the line as it was, above 1 adds the second argument."""
    with FakeServer(tmp_path, script=script_quick) as s:
        with_lots(s, tmp_path)
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#step-main-8_code")
        f = page.locator("#lots-n-main")
        assert f.input_value() == "1" and f.get_attribute("min") == "1"
        assert f.get_attribute("max") == "8"                  # 2 / 10 in PASS
        assert page.locator("#step-main-8_code .lots-n").inner_text().startswith("Lots à coder")
        # No other step has one.
        assert page.locator(".lots-n").count() == 1
        page.locator("#step-main-8_code").get_by_role("button", name="Lancer").click()
        page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
        assert launched(s) == ["/8_code f"]
        # Above the lots left: brought back to them; 0: brought back to 1.
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#lots-n-main:not([disabled])")
        page.locator("#lots-n-main").fill("20")
        page.locator("#lots-n-main").press("Tab")
        assert page.locator("#lots-n-main").input_value() == "8"
        page.locator("#lots-n-main").fill("0")
        page.locator("#lots-n-main").press("Tab")
        assert page.locator("#lots-n-main").input_value() == "1"
        # The « Code » tab carries the same number.
        page.locator("#lots-n-main").fill("3")
        page.locator("#lots-n-main").press("Tab")
        page.locator("#tab-main-code").click()
        page.wait_for_selector("#code-lots-n-main")
        assert page.locator("#code-lots-n-main").input_value() == "3"
        page.get_by_role("button", name="Lancer /8_code").click()
        assert wait_until(page, lambda: len(launched(s)) == 2)
        assert launched(s) == ["/8_code f", "/8_code f 3"]
        assert page.js_errors == []


def test_stop_at_the_next_lot_with_three_lots_stops_after_the_current_one(tmp_path, page):
    coded = []
    with FakeServer(tmp_path) as s:
        with_lots(s, tmp_path)
        s.script, go = coder(s.feat, coded)
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#lots-n-main")
        page.locator("#lots-n-main").fill("3")
        page.locator("#step-main-8_code").get_by_role("button", name="Lancer").click()
        page.wait_for_selector("#btn-stop-next:not([disabled])")
        assert launched(s) == ["/8_code f 3"]
        page.locator("#btn-stop-next").click()
        page.wait_for_function("document.getElementById('stream').textContent.includes('Arrêt au prochain lot demandé')")
        assert (s.feat / "stop.md").exists()
        s.loop.call_soon_threadsafe(go.set)                      # the current lot ends
        page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
        assert coded == ["lot-07"]                                # not lot-08, nor lot-10
        assert "1 lot sur 3" in page.locator("#stream").inner_text()
        assert page.js_errors == []


def test_a_log_path_is_a_link_to_its_folder(tmp_path, page, revealed):
    """1.9.1: the stream's end, « Fin du run » and « Derniers runs » — a
    click opens the log's folder, the file selected."""
    with FakeServer(tmp_path, script=script_quick) as s:
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#run-end a.loglink")
        log = s.rn.current(str(s.app_root)).log_path
        assert page.locator("#stream a.loglink").inner_text() == log
        page.locator("#stream a.loglink").click()
        page.locator("#run-end a.loglink").click()
        page.evaluate("location.hash = '#dashboard'")
        page.wait_for_selector("#history a.loglink")
        assert page.locator("#history a.loglink").inner_text() == log
        page.locator("#history a.loglink").click()
        assert wait_until(page, lambda: len(revealed) == 3)
        assert revealed == [(os.path.normpath(log), True)] * 3
        assert page.js_errors == []
