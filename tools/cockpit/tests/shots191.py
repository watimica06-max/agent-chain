"""1.9.1 — the screens the version changes, at 1280 × 800, before and after.

    python tests/shots191.py <out-dir> avant
    python tests/shots191.py <out-dir> apres

The same places in both phases: « Chaîne → Amont » on the « Coder les lots »
step and the « Code » tab (« Lots à coder »); the end of a /8_code run, its
stream and « Fin du run »; « Derniers runs » on the dashboard; a run opened in
« Statistiques », and the foot of the screen (« Journaux bruts »); a deploy's
« Sortie complète »; the stop screen a second after « Arrêter le cockpit »
during a run, with the state request held back until it shows — the order
that made it vanish. Not a test: run by hand, like shots19.py. No chain
command runs — the SDK client is a fake —, no real device is touched — adb is
a fake — and every repository is a scratch one.
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from claude_agent_sdk import AssistantMessage, TextBlock  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

import diagnostic  # noqa: E402
import server  # noqa: E402
from deployworld import hyrox_targets, use_fake_adb, write_profile  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from shots19 import per_app_chain, snap  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402
from test_page_code import with_lots  # noqa: E402
from test_runner import result, script_until_interrupted  # noqa: E402
from test_statistics import fixture_store  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
server.PROFILE_PUSH = False
server.REVEAL = lambda path, select=False: None       # no window opened on this computer
diagnostic.FIND = lambda tool: None


async def one_lot(c):
    yield AssistantMessage(content=[TextBlock("lot-07 passe.")], model="m")
    yield result("lot-07 passe.\nNext: run /8_code f")


def shots(page, out, s, phase):
    p = phase + "-"
    page.goto(s.url + "#chaine")
    page.wait_for_selector("#step-main-8_code")
    page.locator("#step-main-8_code").evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, p + "01-chaine-etape-coder")
    page.locator("#tab-main-code").click()
    page.wait_for_selector("#lots-main tbody tr[data-lot]")
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
    snap(page, out, p + "02-chaine-code")
    # A /8_code run that ends: its stream, « Fin du run ».
    s.script = one_lot
    s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
    page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
    page.get_by_role("tab", name="Amont").first.click()
    page.wait_for_selector("#run-end .run-total")
    page.locator("#run-end").evaluate("e => e.scrollIntoView({block: 'end'})")
    snap(page, out, p + "03-fin-du-run")
    page.goto(s.url + "#dashboard")
    page.wait_for_selector("#history table")
    page.locator("#history").evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, p + "04-tableau-de-bord-derniers-runs")
    page.goto(s.url + "#stats")
    page.wait_for_selector("#st-tiles .tile")
    page.locator("#st-period button[data-p='tout']").click()
    page.wait_for_function("document.querySelectorAll('#tbl-history tbody tr').length > 0")
    page.locator("#tbl-history tbody tr").first.click()
    page.wait_for_selector(".st-detail")
    page.locator(".st-detail").evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, p + "05-statistiques-un-run")
    page.locator("#main").evaluate("m => m.scrollTo(0, m.scrollHeight)")
    snap(page, out, p + "06-statistiques-bas")
    # A deploy: « Sortie complète ».
    page.goto(s.url + "#deploy")
    page.wait_for_selector(".dp-card")
    page.get_by_role("tab", name="Déployer").click()
    page.wait_for_selector("#dp-targets")
    page.locator('.dp-target[data-target="Téléphone"] > label input').check()
    page.get_by_role("button", name="Construire et installer").click()
    page.wait_for_selector('#dp-job[data-status="fait"]', timeout=30000)
    page.locator("#dp-job").evaluate("e => e.scrollIntoView({block: 'end'})")
    snap(page, out, p + "07-deploiement-sortie-complete")
    # « Arrêter le cockpit » during a run, the state request answered only
    # once the stop screen shows.
    s.script = script_until_interrupted
    s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
    page.goto(s.url + "#settings")
    page.wait_for_selector("#btn-quit")
    held = []
    page.route("**/api/state*", lambda r: held.append(r))
    page.route("**/api/check*", lambda r: held.append(r))
    page.locator("#btn-quit").click()
    page.wait_for_selector("#stopped", state="visible", timeout=10000)
    for r in held:
        r.continue_()
    page.wait_for_timeout(1200)
    snap(page, out, p + "08-arret-du-cockpit")


def main(out_dir, phase):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    server.chain_state = per_app_chain
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("dialog", lambda d: d.accept())
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            with FakeServer(t / "w", stats=fixture_store(str(t / "stats.sqlite"))) as s:
                s.state.rename_app(str(s.app_root), "Hyrox Tracker")
                with_lots(s, t)
                fa = use_fake_adb(t / "adb")
                write_profile(s.app_root, hyrox_targets(fa))
                shots(page, out, s, phase)
                s.app[server.DEPLOY_KEY].stop_all()
                fa.close()
        browser.close()
        if errors:
            print("erreurs de la page :", *errors, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
