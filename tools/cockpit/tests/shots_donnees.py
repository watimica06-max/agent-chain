"""1.10 — « Données », at 1280 × 800, before and after.

    python tests/shots_donnees.py <out-dir> avant
    python tests/shots_donnees.py <out-dir> apres

Before: the side menu, and « À répondre » on a question carrying `Folder:`,
which offered nothing but its options and free text. After: the menu's
« Données »; « De l'application » with an image's preview; « De la
fonctionnalité » with a text file's preview; files joined, their entries to
fill; a committed file made private, and what the page says of its history;
the save; « Joindre un fichier » on the question, and the question answered.
Not a test: run by hand, like shots191.py. No chain command runs — the SDK
client is a fake —, nothing is pushed, and every repository is a scratch one.
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from playwright.sync_api import sync_playwright  # noqa: E402

import server  # noqa: E402
from donneesworld import RELEVE, data_world, png  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from shots19 import per_app_chain, snap  # noqa: E402

server.DONNEES_PUSH = False
server.PROFILE_PUSH = False
server.REVEAL = lambda path, select=False: None
server.chain_state = per_app_chain


def focus_q4(page, s):
    page.goto(s.url + "#answer")
    page.wait_for_selector(".entry")
    card = page.locator(".entry", has=page.locator("b", has_text="Q4"))
    card.locator(".head").click()
    card.evaluate("e => e.scrollIntoView({block: 'center'})")
    return card


def avant(page, s, out):
    page.goto(s.url + "#dashboard")
    page.wait_for_selector("#nav-dashboard[aria-current=page]")
    snap(page, out, "avant-01-menu")
    focus_q4(page, s)
    snap(page, out, "avant-02-a-repondre-question-folder")


def apres(page, s, out, tmp):
    page.goto(s.url + "#dashboard")
    page.wait_for_selector("#nav-dashboard[aria-current=page]")
    snap(page, out, "apres-01-menu")
    page.goto(s.url + "#donnees")
    page.get_by_role("tab", name="De l'application").click()
    page.wait_for_selector("#dn-list tr[data-name='fleche.png']")
    page.locator("#dn-list tr[data-name='fleche.png'] button.dn-show").click()
    page.wait_for_selector("#dn-preview img")
    snap(page, out, "apres-02-donnees-application-image")
    page.get_by_role("tab", name="De la fonctionnalité").click()
    page.wait_for_selector("#dn-list tr[data-name='releve-2026-09-14.csv']")
    page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-show").click()
    page.wait_for_selector("#dn-preview pre")
    snap(page, out, "apres-03-donnees-fonctionnalite-texte")
    # Two files joined at once: each copied, its entry open to fill.
    a = Path(tmp) / "releve-2026-10-01.csv"
    a.write_bytes(RELEVE.replace("2026-09", "2026-10").encode("utf-8"))
    b = Path(tmp) / "capture-appli-banque.png"
    b.write_bytes(png(120, 80))
    page.set_input_files("#dn-input", [str(a), str(b)])
    page.wait_for_selector("#dn-list tr[data-name='capture-appli-banque.png'] .dn-form")
    form = page.locator("#dn-list tr[data-name='releve-2026-10-01.csv'] .dn-form")
    form.locator("input[name=what]").fill("a statement of operations, the October export")
    form.locator("input[name=source]").fill("exported from the bank's account page, by the Product Owner")
    form.locator("input[name=private]").check()
    page.locator("#dn-list").evaluate("e => e.scrollIntoView({block: 'start'})")
    snap(page, out, "apres-04-fichiers-joints-a-remplir")
    # A committed file made private: what stays in the history is said.
    page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-edit").click()
    page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] input[name=private]").check()
    page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] .dn-history").wait_for()
    page.locator("#dn-list tr[data-name='releve-2026-09-14.csv']").evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, "apres-05-prive-deja-commite")
    form2 = page.locator("#dn-list tr[data-name='capture-appli-banque.png'] .dn-form")
    form2.locator("input[name=what]").fill("what the bank's app shows for one operation")
    form2.locator("input[name=source]").fill("a screenshot of the bank's app, by the Product Owner")
    page.locator("#dn-save").click()
    page.wait_for_function("document.getElementById('dn-msg').textContent.includes('Enregistré')")
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
    snap(page, out, "apres-06-enregistre")
    # « À répondre »: the question with `Folder:` offers « Joindre un fichier ».
    card = focus_q4(page, s)
    snap(page, out, "apres-07-a-repondre-joindre")
    f = Path(tmp) / "releve-2026-09-30.csv"
    f.write_bytes(RELEVE.encode("utf-8"))
    card.locator("input.q-join-input").set_input_files(str(f))
    jf = card.locator(".dn-form")
    jf.locator("input[name=what]").fill("a statement of operations, as the bank's site exports it")
    jf.locator("input[name=source]").fill("exported from the bank's account page, by the Product Owner")
    card.evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, "apres-08-a-repondre-entree")
    card.locator("button.q-join-save").click()
    page.wait_for_selector(".notice.ok.q-joined")
    page.locator(".notice.ok.q-joined").evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, "apres-09-a-repondre-joint")


def main():
    out = Path(sys.argv[1])
    phase = sys.argv[2]
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        with FakeServer(Path(tmp) / "s") as s:
            data_world(s.app_root)
            s.state.rename_app(str(s.app_root), "Budget")
            with sync_playwright() as p:
                b = p.chromium.launch(channel="msedge")
                page = b.new_page(viewport={"width": 1280, "height": 800})
                page.on("dialog", lambda d: d.accept())
                if phase == "avant":
                    avant(page, s, out)
                else:
                    apres(page, s, out, tmp)
                b.close()


if __name__ == "__main__":
    main()
