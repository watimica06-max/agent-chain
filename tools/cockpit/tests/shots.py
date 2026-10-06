"""Screenshots of the cockpit page against a fake application folder: the
real files of premiere-app-3 (tests/fixtures/features/), and a feature built
through the whole chain after the commands' templates (test_scan.build_chain).

    python tests/shots.py <out-dir>

Needs `playwright` and Microsoft Edge (driven through its channel, nothing
downloaded). Not a test: run by hand. No chain command runs — the SDK
client is a fake.
"""
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from playwright.sync_api import sync_playwright  # noqa: E402

import diagnostic  # noqa: E402
import nextline  # noqa: E402
import server  # noqa: E402
import stats  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_page_context import IDEAS, LEX, MODEL, PRODUCT  # noqa: E402
from test_statistics import fixture_store  # noqa: E402
from test_stats import two_agents  # noqa: E402

FEATURES = os.path.join(HERE, "fixtures", "features")
# 1.4.5: the cockpit runs the diagnostic on its own; here, a fake, all ✓.
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402
server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})


def snap(page, out, name, full=False):
    # The page scrolls inside #main: a whole flow needs a taller window.
    if full:
        page.set_viewport_size({"width": 1280, "height": 1460})
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    if full:
        page.set_viewport_size({"width": 1280, "height": 800})
    print("shot", name)


def with_feature(s, name):
    shutil.copytree(os.path.join(FEATURES, name), s.app_root / "docs" / "features" / name)
    (s.app_root / "docs" / "TECHNICAL_CONVENTIONS.md").write_text("# Conventions\n", encoding="utf-8")
    s.state.open_pair(str(s.app_root), name)


def with_chain(s, name="chaine"):
    """A feature through the whole chain, two corrections (test_scan.build_chain)."""
    from test_scan import build_chain
    build_chain(s.app_root, name)
    (s.app_root / "docs" / "TECHNICAL_CONVENTIONS.md").write_text("# Conventions\n", encoding="utf-8")
    s.state.open_pair(str(s.app_root), name)


def with_product_before_genres(s, name="produit"):
    """A product file with no behaviour block, the grid never run (4_grille.md:134-140)."""
    from test_scan import write
    write(s.app_root / "docs" / "features" / name / "desc-produit.md",
          "# Produit\n\n### B1 — Une règle\nGenre: règle\nNature: model\n\nTexte.\n")
    s.state.open_pair(str(s.app_root), name)


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        with tempfile.TemporaryDirectory() as t:
            # Start screen: nothing opened yet.
            with FakeServer(Path(t) / "a", opened=False) as s:
                page.goto(s.url)
                snap(page, out, "01-demarrage")
            # The fake folder of the « before » set, with the same relay on file.
            # 1.4: two measures on file, one 12 min old, one from the day before.
            from datetime import datetime, timedelta
            store = stats.Store(str(Path(t) / "stats-b.sqlite"))
            now = datetime.now()
            store.record_limit("r0", {"measured_at": (now - timedelta(minutes=12)).isoformat(timespec="seconds"),
                                      "source": "usage", "window": "five_hour", "utilization": 0.34,
                                      "resets_at": int((now + timedelta(hours=2, minutes=20)).timestamp())})
            store.record_limit("r0", {"measured_at": (now - timedelta(minutes=12)).isoformat(timespec="seconds"),
                                      "source": "usage", "window": "seven_day", "utilization": 0.61,
                                      "resets_at": int((now + timedelta(days=4)).timestamp())})
            with FakeServer(Path(t) / "b", stats=store) as s:
                (s.feat / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
                (s.feat / "convertisseur" / "model.md").write_text(MODEL, encoding="utf-8")
                line = "Next: answer questions, then run /4_grille f"
                s.state.set_relay(str(s.app_root), "f", "/4_grille f", "Fini.\n" + line,
                                  nextline.parse(line).to_dict(), "terminé")
                s.state.add_history(str(s.app_root), "f", {"command": "/4_grille f", "outcome": "terminé",
                                    "next": nextline.parse(line).to_dict(),
                                    "log_path": "tools/cockpit/logs/2026-10-05-1.jsonl", "at": "2026-10-05T17:12:36"})
                page.goto(s.url)
                page.wait_for_selector("#flow-main li.step", state="attached")
                snap(page, out, "02-tableau-de-bord")
                page.get_by_role("link", name="À répondre").first.click()
                snap(page, out, "03-repondre")
                page.locator('.entry[data-id="q:questions-sondeur-02.md#1"] .head').click()
                page.wait_for_function("document.getElementById('ctx-docname').textContent === 'desc-produit.md'")
                snap(page, out, "03b-repondre-bloc")
                page.locator('.entry[data-id="q:questions-sondeur-02.md#2"] .head').click()
                page.wait_for_function("document.getElementById('ctx-note').textContent.includes('B14')")
                snap(page, out, "03c-repondre-introuvable")
                page.get_by_role("link", name="Chaîne").first.click()
                snap(page, out, "04-chaine-repos")
                page.get_by_role("link", name="Paramètres").first.click()
                snap(page, out, "09-parametres")
            # A run going: the step « en cours », the run under it, the permission banner.
            with FakeServer(Path(t) / "c") as s:
                page.goto(s.url + "#chaine")
                page.wait_for_selector("#flow-main li.step")
                s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
                page.wait_for_selector("#perm-banner .perm", timeout=8000)
                page.wait_for_selector("#slot-main-1_lexique #run-panel")
                snap(page, out, "05-chaine-run-autorisation")
                page.get_by_role("link", name="Tableau de bord").first.click()
                snap(page, out, "05b-tableau-run")
                s.call(s.rn.stop_now(str(s.app_root)))
            # 1.4: the lexicographe's terms, occurrence 2 of 4, the keyboard legend.
            with FakeServer(Path(t) / "h") as s:
                feat = s.app_root / "docs" / "features" / "lex"
                feat.mkdir(parents=True)
                (feat / "idees.md").write_text(IDEAS, encoding="utf-8")
                (feat / "questions-lexicographe-01.md").write_text(LEX, encoding="utf-8")
                s.state.open_pair(str(s.app_root), "lex")
                page.goto(s.url + "#answer")
                page.wait_for_function("document.getElementById('ctx-count').textContent === '1 / 4'")
                page.keyboard.press("2")
                page.get_by_role("button", name="Suivante ›").click()
                snap(page, out, "03d-repondre-termes-clavier")
            # 1.4: a run that ended — each hand-back with its figures, the totals.
            with FakeServer(Path(t) / "i", script=two_agents, stats=stats.Store(str(Path(t) / "stats-i.sqlite")),
                            measure_limits=True) as s:
                page.goto(s.url + "#chaine")
                page.wait_for_selector("#flow-main li.step")
                s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
                page.wait_for_selector("#run-total")
                page.locator("#run-total").scroll_into_view_if_needed()
                snap(page, out, "05c-chaine-run-fini-consommation")
                page.get_by_role("link", name="Tableau de bord").first.click()
                page.wait_for_function("document.getElementById('gauge-five_hour').textContent.includes('5 %')")
                snap(page, out, "02b-tableau-apres-run", full=True)
            # A stored Next: the files contradict, after « Où on en est ? ».
            with FakeServer(Path(t) / "d") as s:
                page.goto(s.url)
                page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
                line = "Next: run /2_structure f"
                s.state.set_relay(str(s.app_root), "f", "/1_lexique f", "Fini.\n" + line, nextline.parse(line).to_dict())
                page.get_by_role("link", name="Chaîne").first.click()
                page.get_by_role("button", name="Où on en est ?").click()
                page.wait_for_function("!document.getElementById('next-message').classList.contains('hidden')")
                page.get_by_role("link", name="Tableau de bord").first.click()
                page.get_by_role("button", name="Pourquoi ?").first.click()
                snap(page, out, "06-tableau-contradiction")
            # A feature through the chain (a correction open), and a product file before genres.
            with FakeServer(Path(t) / "e") as s:
                with_chain(s)
                page.goto(s.url)
                page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
                page.get_by_role("button", name="Pourquoi ?").first.click()
                snap(page, out, "07-tableau-chaine")
                page.get_by_role("link", name="Chaîne").first.click()
                snap(page, out, "07b-chaine-chaine", full=True)
                page.get_by_role("link", name="Correction").first.click()
                snap(page, out, "08-correction-chaine")
            with FakeServer(Path(t) / "g") as s:
                with_product_before_genres(s)
                page.goto(s.url + "#chaine")
                page.wait_for_selector("#flow-main li.step")
                page.locator("#step-main-4_grille").get_by_role("button", name="Pourquoi ?").click()
                snap(page, out, "07c-chaine-produit-avant-les-genres", full=True)
            # 1.4.5: « Statistiques » on a fixture store, a run opened; the menu closed.
            with FakeServer(Path(t) / "k", stats=fixture_store(str(Path(t) / "stats-k.sqlite"))) as s:
                page.goto(s.url + "#stats")
                page.wait_for_selector("#st-tiles .tile")
                page.locator("#st-period button[data-p='30j']").click()
                page.wait_for_timeout(400)
                snap(page, out, "10-statistiques")
                page.locator("#st-feature").select_option("*")
                page.locator("#st-period button[data-p='tout']").click()
                page.wait_for_selector("#st-feat", state="visible")
                page.locator("#tbl-history tbody tr", has_text="/1_lexique f").click()
                page.set_viewport_size({"width": 1280, "height": 2300})
                page.wait_for_timeout(400)
                page.screenshot(path=str(out / "10b-statistiques-toutes-run-ouvert.png"), full_page=True)
                page.set_viewport_size({"width": 1280, "height": 800})
                print("shot 10b-statistiques-toutes-run-ouvert")
                page.get_by_role("link", name="Tableau de bord").first.click()
                page.evaluate("document.getElementById('main').scrollTo(0, 0)")
                page.get_by_role("button", name="Fermer le menu").click()
                snap(page, out, "11-menu-ferme-point")
                page.evaluate("location.hash = '#answer'")            # the menu is closed
                snap(page, out, "11b-repondre-menu-ferme")
                page.get_by_role("button", name="Ouvrir le menu").click()
            shots_1_5(page, out, Path(t))
        browser.close()
        print("js errors:", errors)


def shots_1_5(page, out, t):
    """1.5: the Code tab, a lot opened, a run of /8_code going, a correction's
    Code tab, Paramètres (notifications, stop), « Par lot », the stopped page."""
    from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock
    from test_page_code import store_with, with_lots
    from test_runner import script_until_interrupted

    lots = {"lot-01": 640, "lot-02": 1180, "lot-03": 900}
    with FakeServer(t / "m", stats=store_with(str(t / "stats-m.sqlite"), lots)) as s:
        with_lots(s, t / "m-src")
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        page.locator("#tab-main-code").click()
        page.wait_for_selector("#lots-main tbody tr[data-lot]")
        snap(page, out, "12-chaine-code", full=True)
        page.locator("#lot-main-lot-03").click()
        page.wait_for_selector(".lot-detail .mdoc .ln")
        page.evaluate("document.getElementById('lot-main-lot-03').scrollIntoView({block: 'start'})")
        snap(page, out, "12b-chaine-code-lot-ouvert")
        page.get_by_role("link", name="Paramètres").first.click()
        page.evaluate("document.getElementById('sec-notes').scrollIntoView({block: 'start'})")
        snap(page, out, "14-parametres-notifications")
        page.evaluate("document.getElementById('sec-quit').scrollIntoView({block: 'end'})")
        snap(page, out, "14b-parametres-arreter-le-cockpit")
        page.get_by_role("link", name="Statistiques").first.click()
        page.wait_for_selector("#st-lot", state="visible")
        page.evaluate("document.getElementById('st-lot').scrollIntoView({block: 'start'})")
        snap(page, out, "15-statistiques-par-lot")

    async def realisateur_on_lot_06(c):
        yield AssistantMessage(content=[TextBlock("Lot lot-06 : le testeur a rendu la main, je lance le réalisateur."),
                                        ToolUseBlock(id="r6", name="Agent", input={
                                            "subagent_type": "realisateur", "description": "Code lot-06",
                                            "prompt": "Working folder: docs/features/f. Your lot: lot-06."})], model="m")
        async for m in script_until_interrupted(c):
            yield m
    with FakeServer(t / "n", script=realisateur_on_lot_06,
                    stats=store_with(str(t / "stats-n.sqlite"), lots)) as s:
        with_lots(s, t / "n-src")
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        page.locator("#tab-main-code").click()
        s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
        page.wait_for_function("(document.getElementById('code-current') || {}).textContent?.includes('lot-06')")
        snap(page, out, "12c-chaine-code-run-en-cours")
        s.call(s.rn.stop_now(str(s.app_root)))

    with FakeServer(t / "o") as s:
        with_chain(s)
        page.goto(s.url + "#correction")
        page.wait_for_selector("#flow-corr li.step")
        page.locator("#corr-list button", has_text="bugfix-01").click()
        page.locator("#tab-corr-code").click()
        page.wait_for_selector("#lots-bugfix-01 tbody tr[data-lot]")
        snap(page, out, "13-correction-code-bugfix-01")
        page.locator("#lot-bugfix-01-lot-01").click()
        page.wait_for_selector(".lot-detail")
        page.evaluate("document.getElementById('lot-bugfix-01-lot-01').scrollIntoView({block: 'start'})")
        snap(page, out, "13b-correction-code-lot-01-ouvert")
        page.get_by_role("link", name="Paramètres").first.click()
        page.locator("#btn-quit").click()
        page.wait_for_selector("#stopped", state="visible")
        snap(page, out, "16-cockpit-arrete")
    # The tabs remembered by the browser: back to « Amont » for a later run of these shots.
    page.evaluate("localStorage.removeItem('cockpit-tabs')")


if __name__ == "__main__":
    main(sys.argv[1])
