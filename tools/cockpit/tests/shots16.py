"""1.6 — the screens the version changes, at 1280 × 800, before and after.

    python tests/shots16.py <out-dir> avant
    python tests/shots16.py <out-dir> apres

« avant » runs against the code as it was before 1.6 and touches nothing
1.6 adds; « apres » takes the same screens again, then the new ones: the
Applications screen, the switcher, the bulk update's report, a run going in
another application. Not a test: run by hand, like shots.py. No chain
command runs — the SDK client is a fake — and every repository is a scratch
one under a temporary folder.
"""
import os
import subprocess
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
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402
from test_statistics import fixture_store  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
UP = {"state": "à jour", "summary": "Chaîne à jour — 93d18fc du 2026-10-06", "commit": "93d18fc", "date": "2026-10-06",
      "chain_commit": "93d18fc", "chain_date": "2026-10-06", "behind": None, "subjects": [], "modified": []}


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def screens(page, out, s, tag):
    """The screens every version has, the same way each time."""
    page.goto(s.url)
    page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
    snap(page, out, f"{tag}-02-tableau-de-bord")
    for link, name in [("À répondre", "03-repondre"), ("Chaîne", "04-chaine"), ("Correction", "05-correction"),
                       ("Statistiques", "06-statistiques"), ("Paramètres", "07-parametres")]:
        page.get_by_role("link", name=link).first.click()
        if link == "Statistiques":
            page.wait_for_selector("#st-tiles .tile")
        snap(page, out, f"{tag}-{name}")


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
            with FakeServer(t / "b", stats=fixture_store(str(t / "stats-b.sqlite"))) as s:
                line = "Next: answer questions, then run /4_grille f"
                s.state.set_relay(str(s.app_root), "f", "/4_grille f", "Fini.\n" + line,
                                  nextline.parse(line).to_dict(), "terminé")
                screens(page, out, s, phase)
                # A run going: the top bar says it.
                page.get_by_role("link", name="Tableau de bord").first.click()
                s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
                page.wait_for_selector("#perm-banner .perm", timeout=8000)
                snap(page, out, f"{phase}-08-run-en-cours")
                s.call(s.rn.stop_now(str(s.app_root)))
            if phase == "apres":
                import shots16_new
                shots16_new.main(page, out, t)
        browser.close()
        print("js errors:", errors)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "apres")
