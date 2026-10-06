"""1.8 — the screens the version changes, at 1280 × 800, before and after.

    python tests/shots18.py <out-dir> avant
    python tests/shots18.py <out-dir> apres

« avant » takes the screens 1.8 changes as they were: the test step of «
Chaîne », with its « Déployer » running /deploie, and Paramètres → Diagnostic.
« apres » takes them again, then the new ones: « Déploiement » and its three
tabs over a fake adb — a phone, a watch over Wi-Fi, an emulator, an
unauthorized and an offline device —, the Wi-Fi form, a deploy going and done,
a crash in the journal, Paramètres → Déploiement. Not a test: run by hand, like
shots17.py. No chain command runs — the SDK client is a fake —, no real device
is touched — adb is a fake — and every repository is a scratch one.
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
diagnostic.FIND = lambda tool: None          # « apres » gives its own (shots18_new.prepare)
UP = {"state": "à jour", "summary": "Chaîne à jour — f1b473d du 2026-10-06", "commit": "f1b473d", "date": "2026-10-06",
      "chain_commit": "f1b473d", "chain_date": "2026-10-06", "behind": None, "subjects": [], "modified": []}


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def screens(page, out, s, tag):
    """The screens every version has, the same way each time."""
    page.goto(s.url + "#chaine")
    page.wait_for_selector("#step-main-test")
    page.locator("#step-main-test").scroll_into_view_if_needed()
    snap(page, out, f"{tag}-01-chaine-etape-de-test")
    page.goto(s.url + "#settings")
    page.wait_for_selector("#diag-result li")
    page.locator("#sec-diag").scroll_into_view_if_needed()
    snap(page, out, f"{tag}-02-parametres-diagnostic")


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
            with FakeServer(t / "b") as s:
                line = "Next: manual test the application on the devices, then run /fusion f"
                s.state.set_relay(str(s.app_root), "f", "/9_controle f", "Fini.\n" + line,
                                  nextline.parse(line).to_dict(), "terminé")
                if phase == "apres":
                    import shots18_new
                    shots18_new.prepare(s, t)
                screens(page, out, s, phase)
                if phase == "apres":
                    shots18_new.main(page, out, s, t)
        browser.close()
        if errors:
            print("erreurs de la page :", *errors, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
