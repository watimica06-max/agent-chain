"""1.7 — the screens the version changes, at 1280 × 800, before and after.

    python tests/shots17.py <out-dir> avant
    python tests/shots17.py <out-dir> apres

« avant » takes the screens 1.7 changes as they were: the start screen, «
Applications », the dashboard, the test step of « Chaîne ». « apres » takes
them again, then the new ones: « Nouvelle application », its form refusing a
folder, the idea file shown, the creation going, a step that fails and «
Reprendre », the new application's dashboard with « À fournir avant le code ».
Not a test: run by hand, like shots16.py. No chain command runs — the SDK
client is a fake — and every repository is a scratch one under a temporary
folder.
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
import nextline  # noqa: E402
import server  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
UP = {"state": "à jour", "summary": "Chaîne à jour — 3f2e850 du 2026-10-06", "commit": "3f2e850", "date": "2026-10-06",
      "chain_commit": "3f2e850", "chain_date": "2026-10-06", "behind": None, "subjects": [], "modified": []}


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def screens(page, out, s, tag):
    """The screens every version has, the same way each time."""
    page.goto(s.url + "#apps")
    page.wait_for_selector(".app-row")
    snap(page, out, f"{tag}-02-applications")
    page.goto(s.url + "#dashboard")
    page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
    snap(page, out, f"{tag}-03-tableau-de-bord")
    page.get_by_role("link", name="Chaîne").first.click()
    page.wait_for_selector("#step-main-test")
    page.locator("#step-main-test").scroll_into_view_if_needed()
    snap(page, out, f"{tag}-04-chaine-etape-de-test")


def main(out_dir, phase):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    server.chain_state = lambda app: dict(UP)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            with FakeServer(t / "a", opened=False) as s:
                page.goto(s.url)
                page.wait_for_timeout(400)
                snap(page, out, f"{phase}-01-demarrage")
            with FakeServer(t / "b") as s:
                line = "Next: run /1_lexique f"
                s.state.set_relay(str(s.app_root), "f", "/socle", "Fini.\n" + line,
                                  nextline.parse(line).to_dict(), "terminé")
                screens(page, out, s, phase)
            if phase == "apres":
                import shots17_new
                shots17_new.main(page, out, t)
        browser.close()
        print("js errors:", errors)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "apres")
