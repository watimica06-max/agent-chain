"""Screenshots of the cockpit page against a fake application folder, and
against frozen copies of real features (tests/fixtures/features/).

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

import nextline  # noqa: E402
from fakeapp import FakeServer  # noqa: E402

FEATURES = os.path.join(HERE, "fixtures", "features")


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
            with FakeServer(Path(t) / "b") as s:
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
            # A stored Next: the files contradict, after « Où on en est ? ».
            with FakeServer(Path(t) / "d") as s:
                page.goto(s.url)
                page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
                line = "Next: run /2_structure f"
                s.state.set_relay(str(s.app_root), "f", "/1_lexique f", "Fini.\n" + line, nextline.parse(line).to_dict())
                page.get_by_role("button", name="Où on en est ?").click()
                page.wait_for_function("!document.getElementById('next-message').classList.contains('hidden')")
                page.get_by_role("button", name="Pourquoi ?").first.click()
                snap(page, out, "06-tableau-contradiction")
            # Real copies: premiere-app (a correction open) and premiere-app-2.
            with FakeServer(Path(t) / "e") as s:
                with_feature(s, "premiere-app")
                page.goto(s.url)
                page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
                page.get_by_role("button", name="Pourquoi ?").first.click()
                snap(page, out, "07-tableau-premiere-app")
                page.get_by_role("link", name="Chaîne").first.click()
                snap(page, out, "07b-chaine-premiere-app", full=True)
                page.get_by_role("link", name="Correction").first.click()
                snap(page, out, "08-correction-premiere-app")
            with FakeServer(Path(t) / "g") as s:
                with_feature(s, "premiere-app-2")
                page.goto(s.url + "#chaine")
                page.wait_for_selector("#flow-main li.step")
                page.locator("#step-main-4_grille").get_by_role("button", name="Pourquoi ?").click()
                snap(page, out, "07c-chaine-premiere-app-2", full=True)
        browser.close()
        print("js errors:", errors)


if __name__ == "__main__":
    main(sys.argv[1])
