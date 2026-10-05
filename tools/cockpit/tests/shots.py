"""Screenshots of the cockpit page against a fake application folder.

    python tests/shots.py <out-dir> before|after

Needs `playwright` and Microsoft Edge (driven through its channel, nothing
downloaded). Not a test: run by hand.
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from playwright.sync_api import sync_playwright  # noqa: E402

from fakeapp import FakeServer  # noqa: E402
import runner as runner_mod  # noqa: E402


PHASE = "before"


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"), full_page=(PHASE == "before"))
    print("shot", name)


def main(out_dir, phase):
    global PHASE
    PHASE = phase
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
            # Main screen, open questions, a relay on file.
            with FakeServer(Path(t) / "b") as s:
                nxt = {"kind": "answer", "raw": "Next: answer questions, then run /4_grille f",
                       "command": "4_grille", "args": "f", "what": "questions",
                       "french": "Répondre aux questions, puis lancer /4_grille f"}
                s.state.set_relay(str(s.app_root), "f", "/4_grille f", "Fini.\nNext: answer questions, then run /4_grille f", nxt, "terminé")
                s.state.add_history(str(s.app_root), "f", {"command": "/4_grille f", "outcome": "terminé", "next": nxt,
                                                           "log_path": "tools/cockpit/logs/2026-10-05-1.jsonl", "at": "2026-10-05T17:12:36"})
                page.goto(s.url)
                if phase == "before":
                    page.wait_for_selector("text=Q1", timeout=5000)
                    snap(page, out, "02-principal")
                else:
                    page.wait_for_selector("text=Prochaine étape", timeout=5000)
                    page.wait_for_timeout(500)
                    snap(page, out, "02-tableau-de-bord")
                    for name, label in [("03-repondre", "À répondre"), ("05-run-repos", "Run"), ("06-parametres", "Paramètres")]:
                        page.get_by_role("link", name=label).first.click()
                        snap(page, out, name)
            # A fake run waiting on a permission card.
            with FakeServer(Path(t) / "c") as s:
                page.goto(s.url)
                page.wait_for_timeout(500)
                s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
                page.wait_for_selector("text=Autoriser", timeout=8000)
                if phase == "after":
                    page.get_by_role("link", name="Run").first.click()
                    snap(page, out, "04-run-autorisation")
                    page.get_by_role("link", name="Tableau de bord").first.click()
                    snap(page, out, "04b-tableau-autorisation")
                else:
                    snap(page, out, "03-run-autorisation")
                s.call(s.rn.stop_now(str(s.app_root)))
        browser.close()
        print("js errors:", errors)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "before")
