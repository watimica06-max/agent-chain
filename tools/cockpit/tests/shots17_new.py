"""1.7 — the new screens, for shots17.py « apres »: « Nouvelle application »
filled, its idea file shown; a folder refused; the creation going; a step
that fails and « Reprendre »; the creation done; the new application's
dashboard with « À fournir avant le code »; its test step with no «
Déployer ». A scratch chain repository carrying the real socle.py; nothing
leaves the temporary folder."""
import os
import time

import chain
import create
import server
from fakeapp import FakeServer
from test_chain import CHAIN_FILES, commit, init, write
from test_create import IDEA


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


IDEA_LONG = IDEA + (
    "\r\n## Ce que je veux\r\n\r\n- Démarrer une séance d'un geste\r\n- Compter les tours, voir le temps de chacun\r\n"
    "- Revoir les séances passées, la meilleure en tête\r\n\r\n## Plus tard\r\n\r\n> Partager une séance avec un ami.\r\n")


def main(page, out, t):
    root = t / "agent-chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    socle = os.path.join(chain.CHAIN_ROOT, ".claude", "scripts", "socle.py")
    (root / ".claude" / "scripts" / "socle.py").write_bytes(open(socle, "rb").read())
    commit(root, "Chaîne — un")
    chain._chain_cache.clear()
    idea = t / "Mes idées" / "hyrox-idees.md"
    idea.parent.mkdir()
    idea.write_bytes(IDEA_LONG.encode("utf-8"))
    dev = t / "Dev"
    (dev / "deja-la").mkdir(parents=True)
    (dev / "deja-la" / "notes.txt").write_text("x")

    real_root, real_state = server.CHAIN_ROOT, server.chain_state
    real_chaine, real_socle = create.Creation.step_chaine, create.Creation.step_socle
    armed = {"on": True}

    def slow_chaine(self):
        time.sleep(3)
        return real_chaine(self)

    def socle_once(self):
        if armed["on"]:
            armed["on"] = False
            raise create.StepError("socle.py : git commit : simulé pour la capture — "
                                   "le dépôt était verrouillé par un autre programme")
        return real_socle(self)
    server.CHAIN_ROOT = str(root)
    server.chain_state = lambda app: chain.state(app, str(root))
    create.Creation.step_chaine, create.Creation.step_socle = slow_chaine, socle_once
    try:
        with FakeServer(t / "n", file_picker=lambda initial: str(idea),
                        picker=lambda initial: str(dev)) as s:
            page.goto(s.url + "#apps")
            page.wait_for_selector(".app-row")
            page.get_by_role("button", name="Nouvelle application").click()
            page.get_by_role("button", name="Parcourir…").nth(0).click()
            page.wait_for_function("document.getElementById('nf-parent').value !== ''")
            page.locator("#nf-name").fill("Hyrox Séances")
            page.get_by_role("button", name="Parcourir…").nth(1).click()
            page.wait_for_selector("#nf-idea-view:not(.hidden)")
            page.locator("#nf-feature").fill("premiere-app")
            page.wait_for_selector("#nf-summary li")
            page.evaluate("document.getElementById('new-app').scrollIntoView({block: 'start'})")
            snap(page, out, "apres-05-nouvelle-application")
            page.evaluate("document.getElementById('nf-summary').scrollIntoView({block: 'end'})")
            snap(page, out, "apres-05b-nouvelle-application-recapitulatif")
            page.locator("#nf-folder").fill("deja-la")
            page.wait_for_function("document.getElementById('nf-err-folder').textContent !== ''")
            page.evaluate("document.getElementById('new-app').scrollIntoView({block: 'start'})")
            snap(page, out, "apres-06-dossier-refuse")
            page.locator("#nf-folder").fill("hyrox-seances")
            page.wait_for_function("!document.getElementById('nf-create').disabled")
            page.locator("#nf-create").click()
            page.wait_for_selector(".mk[data-status='en cours'] li[data-step='chaine'][data-status='en cours']")
            page.evaluate("document.getElementById('main').scrollTo(0, 0)")
            snap(page, out, "apres-07-creation-en-cours")
            page.wait_for_selector(".mk[data-status='échec']", timeout=60000)
            page.evaluate("document.getElementById('main').scrollTo(0, 0)")
            snap(page, out, "apres-08-etape-en-echec")
            page.get_by_role("button", name="Reprendre").click()
            page.wait_for_selector(".mk[data-status='fait']", timeout=60000)
            page.evaluate("document.getElementById('main').scrollTo(0, 0)")
            snap(page, out, "apres-09-reprendre-creee")
            page.wait_for_function("location.hash === '#dashboard'", timeout=10000)
            page.wait_for_function("document.getElementById('next-text').textContent.includes('/1_lexique')")
            snap(page, out, "apres-10-tableau-de-bord-nouvelle-application")
            page.locator("#provide-card").scroll_into_view_if_needed()
            snap(page, out, "apres-10b-a-fournir-avant-le-code")
            page.get_by_role("link", name="Chaîne").first.click()
            page.wait_for_selector("#step-main-test")
            page.locator("#step-main-test").scroll_into_view_if_needed()
            snap(page, out, "apres-11-etape-de-test-sans-deployer")
    finally:
        server.CHAIN_ROOT, server.chain_state = real_root, real_state
        create.Creation.step_chaine, create.Creation.step_socle = real_chaine, real_socle
