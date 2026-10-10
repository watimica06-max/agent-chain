"""1.20 — the cycle journal's screens, at 1280 × 800 and on a phone (390 × 844).

    python tests/shots120.py <out-dir>

The « Journal » screen on a scratch application with a dated story
(journalworld.py): its top — the points à creuser and the totals —, the
timeline by step, the « Erreurs » filter, « Son temps »; « Rapport de fin de
cycle » shown before anything is written; « Reconstituer le passé » shown
before anything is written; the dashboard proposing the report once the
final step is done; Paramètres → Journal de cycle; the dark theme; the phone,
read only. Not a test: run by hand, like shots19.py. No chain command runs;
every repository is a scratch one.
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from playwright.sync_api import sync_playwright  # noqa: E402

import diagnostic  # noqa: E402
import journal  # noqa: E402
import journalworld  # noqa: E402
import nextline  # noqa: E402
import server  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_chain import git  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
diagnostic.FIND = lambda tool: None
# No usage measure: it would call Claude (usage.py).
server.MEASURE_USAGE = False
server.chain_state = lambda app: {"state": "à jour", "summary": "Chaîne à jour — 91a89a2 du 2026-10-10",
                                  "commit": "91a89a2", "date": "2026-10-10", "chain_commit": "91a89a2",
                                  "chain_date": "2026-10-10", "behind": None, "subjects": [], "modified": []}


def snap(page, out, name, full=False):
    page.wait_for_timeout(400)
    page.screenshot(path=str(out / f"{name}.png"), full_page=full)
    print("shot", name)


def scroll_to(page, sel):
    page.locator(sel).evaluate("e => e.scrollIntoView({block: 'start'})")


def open_journal(page, s):
    page.goto(s.url + "#journal")
    page.wait_for_selector("#jn-timeline .jn-step")
    page.wait_for_timeout(300)


def desk(page, out, s):
    open_journal(page, s)
    snap(page, out, "01-journal-haut-points-a-creuser")
    scroll_to(page, "#jn-timeline")
    snap(page, out, "02-journal-pas-a-pas")
    scroll_to(page, "#jn-timeline .jn-step[data-step='/8_code']")
    snap(page, out, "03-journal-pas-a-pas-code")
    page.locator("#jn-filter button[data-f='erreurs']").click()
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
    snap(page, out, "04-journal-filtre-erreurs")
    page.locator("#jn-filter button[data-f='tout']").click()
    scroll_to(page, "#jn-steps")
    snap(page, out, "05-journal-par-etape-et-son-temps")
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
    page.locator("#jn-report").click()
    page.wait_for_selector("#jn-panel pre")
    snap(page, out, "06-rapport-de-fin-de-cycle-apercu")
    page.get_by_role("button", name="Annuler").click()
    # The past: the journal set aside, its lines rebuilt from git and the stats.
    path = journal.journal_path(str(s.app_root), "f")
    keep = open(path, encoding="utf-8").read()
    os.remove(path)
    page.locator("#jn-rebuild").click()
    page.wait_for_selector("#jn-panel pre")
    snap(page, out, "07-reconstituer-le-passe-apercu")
    page.get_by_role("button", name="Annuler").click()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(keep)
    # The final step done: the dashboard proposes the report.
    line = "Next: done"
    s.state.set_relay(str(s.app_root), "f", "/fusion f", "Fusionné.\n" + line, nextline.parse(line).to_dict(), "terminé")
    page.goto(s.url + "#dashboard")
    page.reload()
    page.wait_for_selector("#next-report")
    snap(page, out, "08-tableau-de-bord-rapport-propose")
    page.goto(s.url + "#settings")
    page.wait_for_selector("#sec-journal")
    scroll_to(page, "#sec-journal")
    snap(page, out, "09-parametres-journal-de-cycle")
    page.evaluate("document.documentElement.dataset.theme = 'dark'")
    open_journal(page, s)
    page.evaluate("document.documentElement.dataset.theme = 'dark'")
    snap(page, out, "10-journal-sombre")


def on_phone(browser, out, s):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    ph = ctx.new_page()
    ph.goto(s.url + "#dashboard")
    ph.wait_for_selector("#phone-nav")
    ph.locator("#phone-more").click()
    ph.wait_for_selector("#phone-journal")
    snap(ph, out, "11-telephone-plus-journal")
    ph.locator("#phone-journal").click()
    ph.wait_for_selector("#jn-timeline .jn-step")
    snap(ph, out, "12-telephone-journal-haut")
    scroll_to(ph, "#jn-timeline")
    snap(ph, out, "13-telephone-journal-pas-a-pas")
    ctx.close()


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            with FakeServer(t / "w") as s:
                s.state.rename_app(str(s.app_root), "Hyrox Tracker")
                journalworld.make(s.app_root)
                git(s.app_root, "log", "-1")
                desk(page, out, s)
                on_phone(browser, out, s)
        browser.close()
        if errors:
            print("erreurs de la page :", *errors, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1])
