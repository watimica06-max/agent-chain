"""1.13 — the cockpit on a phone screen, in a headless browser (Microsoft
Edge through Playwright) at 390 × 844 with touch: each thing the phone is
for done end to end — an application opened, a feature changed, an answer
and a decision saved, answers sent, a file joined, the proposed /8_code
launched with « Lots à coder », a permission granted, a run stopped, a file
joined in « Données » —; each screen of the computer says « Sur
l'ordinateur »; no phone screen scrolls sideways; every control is 44 px at
least. Above 720 px nothing of it exists. No chain command runs; every
repository is a scratch one, nothing reaches GitHub. Skipped when
Playwright or Edge is missing."""
import asyncio
import json

import pytest

pytest.importorskip("playwright")

import server  # noqa: E402
from cmdtests import unanswered_questions  # noqa: E402
from donneesworld import RELEVE, data_world  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from syncworld import app_world, change, head  # noqa: E402
from test_chain import git  # noqa: E402
from test_flow import add_turn_feature  # noqa: E402
from test_page import _wait, browser, no_real_errors, start_run  # noqa: E402,F401
from test_page_code import launched, with_lots  # noqa: E402
from test_scan import build_chain, split  # noqa: E402
from claude_agent_sdk import AssistantMessage, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage  # noqa: E402
from test_codelots import verdict  # noqa: E402
from test_runner import result, script_until_interrupted  # noqa: E402
from test_server import build_app_folder  # noqa: E402

W, H, NAV = 390, 844, 64
DESK = [("correction", "Correction"), ("deploy", "Déploiement"), ("stats", "Statistiques"), ("settings", "Paramètres")]


@pytest.fixture
def phone(browser):
    ctx = browser.new_context(viewport={"width": W, "height": H}, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.js_errors = []
    pg.on("pageerror", lambda e: pg.js_errors.append(str(e)))
    pg.on("console", lambda m: pg.js_errors.append(m.text) if m.type == "error" else None)
    pg.on("dialog", lambda d: d.accept())
    yield pg
    ctx.close()


@pytest.fixture(autouse=True)
def _no_push(monkeypatch):
    monkeypatch.setattr(server, "DONNEES_PUSH", False)


def errors(page):
    return [e for e in no_real_errors(page) if "status of 409" not in e]


def tab(page, name):
    page.locator("#phone-nav").get_by_role("link", name=name).tap()


def no_side_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"
                         " && document.getElementById('main').scrollWidth <= document.getElementById('main').clientWidth")


# Every visible control under 44 × 44 px — a radio or a box counts by its label.
SMALL_JS = """() => {
  const out = [];
  for (const e of document.querySelectorAll('button, a[href], input, select, textarea, summary, label.opt, label.dn-priv')) {
    if (e.type === 'hidden' || e.type === 'file') continue;
    const r = e.getBoundingClientRect(), st = getComputedStyle(e);
    if (!r.width || !r.height || st.visibility === 'hidden') continue;
    if ((e.type === 'radio' || e.type === 'checkbox') && e.closest('label')) continue;
    if (e.matches('#ctx-doc *, #stream *, pre *')) continue;
    if (r.width < 43.5 || r.height < 43.5) out.push(`${e.tagName.toLowerCase()}${e.id ? '#' + e.id : ''}.${[...e.classList].join('.')} « ${(e.textContent || e.value || '').trim().slice(0, 30)} » ${Math.round(r.width)}×${Math.round(r.height)}`);
  }
  return out;
}"""


def small(page):
    return page.evaluate(SMALL_JS)


def coder_at(code, stop, coded):
    """test_page_code.coder for a correction: the lots under `code`, stop.md
    at `stop` — the feature's root, not the bugfix folder."""
    go = asyncio.Event()

    async def script(c):
        words = c.prompts[0].split()
        n = int(words[2]) if len(words) > 2 else 1
        for lot in ("lot-07", "lot-08", "lot-10")[:n]:
            yield AssistantMessage(content=[ToolUseBlock(id="r-" + lot, name="Agent", input={
                "subagent_type": "realisateur", "description": f"Code {lot}", "prompt": f"Your lot: {lot}."})], model="m")
            await go.wait()
            go.clear()
            (code / lot / "verdict.md").write_text(verdict("PASS"), encoding="utf-8")
            coded.append(lot)
            yield UserMessage(content=[ToolResultBlock(tool_use_id="r-" + lot, content="PASS")])
            if stop.exists():
                text = f"Arrêté sur stop.md : {len(coded)} lot sur {n}.\nNext: run /8_code chaine"
                yield AssistantMessage(content=[TextBlock(text)], model="m")
                yield result(text)
                return
        yield AssistantMessage(content=[TextBlock("Fini.\nNext: run /9_controle chaine")], model="m")
        yield result("Fini.\nNext: run /9_controle chaine")
    return script, go


def test_home_open_an_application_change_feature_and_application(tmp_path, phone):
    with FakeServer(tmp_path, opened=False) as s:
        other = tmp_path / "other"
        build_app_folder(other)
        for folder, name in ((s.app_root, "Hyrox"), (other, "Belivo")):
            s.state.add_app(str(folder))
            s.state.rename_app(str(folder), name)
            s.state.open_pair(str(folder), "f")
        (s.app_root / "docs" / "features" / "g").mkdir(parents=True)
        (s.app_root / "docs" / "features" / "g" / "idees.md").write_text("# Idées\n", encoding="utf-8")
        page = phone
        page.goto(s.url)
        page.wait_for_selector(".home-card")
        # The home: one card per application, what stays on the computer said in one line.
        assert page.locator(".home-card").count() == 2
        assert "sur l'ordinateur" in page.locator("#phone-home-desk").inner_text()
        for sel in ("#btn-app-new", "#btn-app-add", "#btn-app-clone", "#btn-update-all", ".hc-menu-btn"):
            assert not page.locator(sel).first.is_visible(), sel
        assert not page.locator("#phone-nav").is_visible() and not page.locator("#side").is_visible()
        assert no_side_scroll(page) and small(page) == []
        # A tap opens it on its dashboard; the tabs appear, the side menu stays away.
        page.locator('.home-card[data-name="Hyrox"]').tap()
        page.wait_for_function("S.app_name === 'Hyrox' && document.getElementById('next-text').textContent !== '—'")
        assert page.locator("#scr-dashboard").is_visible() and page.locator("#phone-nav").is_visible()
        assert page.locator("#phone-tab-dashboard").get_attribute("aria-current") == "page"
        assert not page.locator("#side").is_visible()
        assert page.locator("#tb-app").inner_text() == "Hyrox"
        # The feature: from the top bar, a sheet within the screen.
        page.locator("#tb-folder").tap()
        menu = page.locator("#feat-menu")
        assert menu.is_visible()
        box = menu.bounding_box()
        assert box["x"] >= 0 and box["x"] + box["width"] <= W and box["y"] + box["height"] <= H - NAV
        menu.get_by_role("menuitem", name="g").tap()
        page.wait_for_function("S.feature === 'g'")
        # The application: « Plus » → « Changer d'application ».
        page.locator("#phone-more").tap()
        assert page.locator("#phone-sheet").is_visible()
        assert page.locator("#phone-feat-name").inner_text() == "g"
        page.locator("#phone-apps").tap()
        page.wait_for_selector("#scr-accueil:not(.hidden)")
        page.locator('.home-card[data-name="Belivo"]').tap()
        page.wait_for_function("S.app_name === 'Belivo'")
        assert errors(page) == []


def test_dashboard_whole_and_the_github_buttons(tmp_path, phone):
    remote, carnet, _ = app_world(tmp_path, "carnet")
    change(carnet, "notes.md", "notes\n")
    with FakeServer(tmp_path / "srv", opened=False) as s:
        s.state.add_app(str(carnet))
        s.state.rename_app(str(carnet), "Carnet")
        s.state.open_pair(str(carnet), "f")
        page = phone
        page.goto(s.url)
        page.locator('.home-card[data-name="Carnet"]').tap()
        page.wait_for_function("document.getElementById('next-text').textContent !== '—' && S.app_name === 'Carnet'")
        for sel in ("#next-card", "#next-text", "#next-detail button.primary", "#dash-wait", "#cnt-questions",
                    "#cnt-blocking", "#gauges"):
            assert page.locator(sel).first.is_visible(), sel
        push = page.locator("#alerts button.sync-push")
        push.wait_for(timeout=30000)
        assert page.locator("#alerts button.sync-reconcile").count() + push.count() >= 1
        assert no_side_scroll(page) and small(page) == []
        push.tap()
        page.wait_for_function("document.getElementById('sync-banner').textContent.includes('envoyé à GitHub')", timeout=30000)
        assert git(remote, "rev-parse", "master").strip() == head(carnet)
        assert errors(page) == []


def test_answer_and_decision_saved_then_sent(tmp_path, phone):
    remote, carnet, _ = app_world(tmp_path, "carnet")
    add_turn_feature(carnet, "t", blocked_classeur=True)
    git(carnet, "add", "-A")
    git(carnet, "commit", "-q", "-m", "t")
    git(carnet, "push", "-q")
    with FakeServer(tmp_path / "srv", opened=False) as s:
        s.state.add_app(str(carnet))
        s.state.rename_app(str(carnet), "Carnet")
        s.state.open_pair(str(carnet), "f")
        page = phone
        page.goto(s.url)
        page.locator('.home-card[data-name="Carnet"]').tap()
        page.wait_for_function("S.app_name === 'Carnet' && document.getElementById('next-text').textContent !== '—'")
        tab(page, "À répondre")
        page.wait_for_selector("#form .entry")
        assert page.locator("#phone-answer-count").inner_text() == "2"
        # A question: an option tapped, its document shown over the screen and closed.
        q1 = page.locator('.entry[data-id="q:questions-lexicographe-01.md#1"]')
        q1.locator(".phone-ctx").tap()
        assert page.locator("#ctx-pane").is_visible()
        assert page.locator("#ctx-docname").inner_text() != "—"
        page.locator("#phone-ctx-close").tap()
        assert not page.locator("#ctx-pane").is_visible()
        q1.locator(".opt", has_text="Non, deux choses.").tap()
        assert no_side_scroll(page) and small(page) == []
        # The save bar sits above the tabs, in reach of the thumb.
        save = page.locator("#btn-save").bounding_box()
        assert save["y"] + save["height"] <= H - NAV
        page.locator("#btn-save").tap()
        page.wait_for_function("!document.querySelector('.entry[data-id=\"q:questions-lexicographe-01.md#1\"]')", timeout=10000)
        assert 1 not in unanswered_questions(str(carnet / "docs" / "features" / "f" / "questions-lexicographe-01.md"))
        # Then a blocking file: the decision written under « ## Decision ».
        s.state.open_pair(str(carnet), "t")
        page.goto(s.url + "?2#answer")
        card = page.locator('.entry[data-id^="b:"]').first
        card.wait_for()
        card.locator(".opt", has_text="Décision libre").tap()
        card.locator("textarea").fill("Une seule nature : model.")
        page.locator("#btn-save").tap()
        page.wait_for_function("!document.querySelector('#form .entry[data-id^=\"b:\"]')", timeout=10000)
        text = (carnet / "docs" / "features" / "t" / "blocked_classeur.md").read_text(encoding="utf-8")
        assert text.rstrip().endswith("## Decision\n\nUne seule nature : model.")
        # « Envoyer mes réponses »: committed and pushed.
        page.locator("#btn-send-answers").wait_for(state="visible")
        page.locator("#btn-send-answers").tap()
        page.wait_for_selector("#answers-msg:not(:empty)", timeout=30000)
        assert git(carnet, "log", "-1", "--format=%s").strip() == "chore: answers"
        assert git(remote, "rev-parse", "master").strip() == head(carnet)
        assert errors(page) == []


def test_join_a_file_to_an_answer_and_in_donnees(tmp_path, phone):
    with FakeServer(tmp_path / "s") as s:
        data_world(s.app_root)
        page = phone
        page.goto(s.url + "#answer")
        page.wait_for_selector(".entry")
        card = page.locator(".entry", has=page.locator("b", has_text="Q4"))
        # The browser's file input: on a phone it offers the camera or the files.
        assert card.locator("input.q-join-input").get_attribute("type") == "file"
        f = tmp_path / "releve-2026-09-30.csv"
        f.write_text(RELEVE, encoding="utf-8")
        card.locator("input.q-join-input").set_input_files(str(f))
        card.locator(".dn-form").wait_for()
        card.locator("input[name=what]").fill("a statement of operations, as the bank's site exports it")
        card.locator("input[name=source]").fill("the bank's account page")
        assert no_side_scroll(page)
        card.locator("button.q-join-save").tap()
        page.wait_for_selector(".notice.ok.q-joined")
        assert (s.app_root / "docs/features/f/donnees/releve-2026-09-30.csv").read_text(encoding="utf-8") == RELEVE
        # « Données »: the list, a preview, a file joined and saved.
        tab(page, "Données")
        page.get_by_role("tab", name="De la fonctionnalité").tap()
        row = page.locator("#dn-list tr[data-name='releve-2026-09-14.csv']")
        row.wait_for()
        row.locator("button.dn-show").tap()
        page.wait_for_selector("#dn-preview pre")
        assert page.locator("#dn-preview").is_visible()
        assert no_side_scroll(page) and small(page) == []
        g = tmp_path / "photo.csv"
        g.write_text("a;b\n", encoding="utf-8")
        page.set_input_files("#dn-input", str(g))
        form = page.locator("#dn-list tr[data-name='photo.csv'] .dn-form")
        form.wait_for()
        form.locator("input[name=what]").fill("a photo of the receipt, typed")
        form.locator("input[name=source]").fill("the Product Owner's phone")
        page.locator("#dn-save").tap()
        page.wait_for_function("document.getElementById('dn-msg').textContent.includes('Enregistré')", timeout=10000)
        assert "## photo.csv" in (s.app_root / "docs/features/f/donnees/donnees.md").read_text(encoding="utf-8")
        assert errors(page) == []


def test_launch_the_proposed_code_with_lots_then_stop_at_the_next_lot(tmp_path, phone):
    """A correction cycle's /8_code — the dashboard proposes the highest
    bugfix-NN/ while it is open — launched from the phone with three lots."""
    coded = []
    with FakeServer(tmp_path) as s:
        f = build_chain(s.app_root, "chaine")
        (s.app_root / "docs" / "TECHNICAL_CONVENTIONS.md").write_text("# Conventions\n", encoding="utf-8")
        (f / "questions-sondeur-03.md").unlink()
        b2 = f / "bugfix-02"
        split(b2 / "code", ["lot-07", "lot-08", "lot-10"])     # the lots coder() codes
        for v in (b2 / "code").glob("lot-*/verdict.md"):
            v.unlink()
        s.state.open_pair(str(s.app_root), "chaine")
        # /8_code acts on bugfix-02/; its stop.md is at the feature's root (runner.stop_file).
        s.script, go = coder_at(b2 / "code", f / "stop.md", coded)
        page = phone
        page.goto(s.url + "#dashboard")
        page.wait_for_selector("#next-lots-n")
        btn = page.locator("#next-detail button.primary")
        assert btn.inner_text() == "Lancer /8_code chaine"
        page.locator("#next-lots-n").fill("3")
        page.locator("#next-lots-n").dispatch_event("change")
        assert btn.inner_text() == "Lancer /8_code chaine 3"
        assert no_side_scroll(page) and small(page) == []
        btn.tap()
        page.wait_for_selector("#btn-stop-next:not([disabled])")
        assert launched(s) == ["/8_code chaine 3"]
        # Watched in « Chaîne », where the stops are — « Correction » is the computer's.
        assert page.locator("#scr-chaine").is_visible() and page.locator("#run-panel").is_visible()
        assert page.locator("#phone-run-dot").is_visible()
        page.locator("#btn-stop-next").tap()
        page.wait_for_function("document.getElementById('stream').textContent.includes('Arrêt au prochain lot demandé')")
        s.loop.call_soon_threadsafe(go.set)
        page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
        assert coded == ["lot-07"]
        assert errors(page) == []


def test_a_permission_is_a_sheet_over_any_screen_then_the_run_stopped(tmp_path, phone):
    with FakeServer(tmp_path) as s:
        page = phone
        page.goto(s.url + "#dashboard")
        page.wait_for_selector("#phone-nav")
        start_run(s, page)
        for r in ("dashboard", "answer", "donnees"):
            page.evaluate(f"location.hash = '#{r}'")              # the sheet is modal: the tabs wait under it
            page.wait_for_selector(f"#scr-{r}:not(.hidden)")
            sheet = page.locator("#perm-banner")
            assert sheet.is_visible()
            for label in ("Autoriser", "Refuser"):
                b = sheet.get_by_role("button", name=label)
                box = b.bounding_box()
                assert box["y"] + box["height"] <= H and box["height"] >= 44
                # Nothing over it: the tabs stay under the sheet.
                assert page.evaluate("([x, y]) => !!document.elementFromPoint(x, y).closest('#perm-banner')",
                                     [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2]), label
        assert "perm" in page.locator("#phone-run-dot").get_attribute("class")
        sheet.get_by_role("button", name="Autoriser").tap()
        page.wait_for_selector("#perm-banner", state="hidden")
        s.call(_wait(s.rn.current(str(s.app_root)).task))
        # A second run, stopped from « Chaîne ».
        s.script = script_until_interrupted
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        tab(page, "Chaîne")
        page.wait_for_selector("#btn-stop-now:not([disabled])")
        assert page.locator("#btn-stop-now").is_visible()
        page.locator("#btn-stop-now").tap()
        page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')", timeout=15000)
        assert errors(page) == []


def test_chaine_is_read_only_and_the_computer_screens_say_so(tmp_path, phone):
    with FakeServer(tmp_path) as s:
        with_lots(s, tmp_path)
        page = phone
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        # Every step that launches says « Sur l'ordinateur »; no « Lancer », no « Lots à coder ».
        assert page.locator("#flow-main").get_by_role("button", name="Lancer").count() == 0
        assert not page.locator("#lots-n-main").is_visible()
        steps = page.locator("#flow-main li.step")
        for i in range(steps.count()):
            assert "Sur l'ordinateur" in steps.nth(i).locator(".acts").inner_text(), steps.nth(i).get_attribute("id")
        page.locator("#step-main-1_lexique").get_by_role("button", name="Pourquoi ?").tap()
        assert page.locator("#step-main-1_lexique .whybox").is_visible()
        assert no_side_scroll(page) and small(page) == []
        page.locator("#tab-main-code").tap()
        page.wait_for_selector("#chaine-code .code-actions")
        assert "Sur l'ordinateur" in page.locator("#chaine-code .code-actions").inner_text()
        assert page.get_by_role("button", name="Lancer /8_code").count() == 0
        assert no_side_scroll(page)
        page.locator("#tab-main-version").tap()
        assert not page.locator("#btn-chain").is_visible()
        assert "Sur l'ordinateur" in page.locator("#chaine-version").inner_text()
        # « Plus » lists the computer's screens; each says so, and nothing else of it shows.
        page.locator("#phone-more").tap()
        for r, label in DESK:
            assert "Sur l'ordinateur" in page.locator(f"#phone-desk-{r}").inner_text()
        assert no_side_scroll(page) and small(page) == []
        for r, label in DESK + [("nouvelle", "Nouvelle application")]:
            page.goto(f"{s.url}#{r}")
            scr = page.locator(f"#scr-{r}")
            scr.locator(".phone-desk").wait_for()
            assert scr.locator(".phone-desk h2").inner_text() == label
            assert "Sur l'ordinateur" in scr.locator(".phone-desk").inner_text()
            assert scr.evaluate("s => [...s.children].filter(c => !c.classList.contains('phone-desk') "
                                "&& getComputedStyle(c).display !== 'none').length") == 0, r
            assert no_side_scroll(page) and small(page) == [], r
        assert errors(page) == []


def test_desktop_side_has_none_of_it_and_crossing_the_width_rebuilds(tmp_path, browser):
    with FakeServer(tmp_path) as s:
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.js_errors = []
        page.on("pageerror", lambda e: page.js_errors.append(str(e)))
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        assert page.locator("[data-phone]").count() == 0
        assert page.locator(".on-desk, .phone-ctx, #next-lots-n").count() == 0
        assert page.locator("#side").is_visible()
        page.set_viewport_size({"width": W, "height": H})
        page.wait_for_selector("#phone-nav")
        assert not page.locator("#side").is_visible()
        assert page.locator("#flow-main .on-desk").count() > 0
        page.set_viewport_size({"width": 1280, "height": 800})
        page.wait_for_function("!document.getElementById('phone-nav')")
        assert page.locator("[data-phone], .on-desk").count() == 0
        assert page.locator("#side").is_visible()
        assert no_real_errors(page) == []
        page.close()


def test_manifest_and_icons_for_the_home_screen(tmp_path, phone):
    with FakeServer(tmp_path) as s:
        phone.goto(s.url)
        href = phone.locator("link[rel=manifest]").get_attribute("href")
        r = phone.request.get(s.url + href.lstrip("/"))
        assert r.ok and "manifest" in r.headers["content-type"]
        m = json.loads(r.text())
        assert m["display"] == "standalone" and m["start_url"] == "/"
        for icon in m["icons"]:
            got = phone.request.get(s.url + icon["src"].lstrip("/"))
            assert got.ok and got.headers["content-type"] == "image/png"
            assert got.body()[:8] == b"\x89PNG\r\n\x1a\n"
        assert phone.request.get(s.url + phone.locator("link[rel=apple-touch-icon]").get_attribute("href").lstrip("/")).ok
        assert phone.request.get(s.url + "icons/server.py").status == 404
