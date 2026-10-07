"""1.9 — the screens the version changes, at 1280 × 800, before and after.

    python tests/shots19.py <out-dir> avant
    python tests/shots19.py <out-dir> apres

« avant » takes the screens 1.9 changes as they were: the opening, «
Applications », « Nouvelle application » inside it, the dashboard and its top
bar, the foot of « Chaîne », « Déploiement », « Paramètres » section by
section. « apres » takes the same places again — the home screen, a card's
menu, « Nouvelle application » as its own page, the dashboard with «
Applications » in the top bar, the « Audits » block, « Chaîne → Version », «
Déploiement → Profil », the tidied « Paramètres » — then a run going: the
notice on leaving, the card « en cours », another application opened where
launching is refused. Not a test: run by hand, like shots18.py. No chain
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

from playwright.sync_api import sync_playwright  # noqa: E402

import chain  # noqa: E402
import diagnostic  # noqa: E402
import nextline  # noqa: E402
import server  # noqa: E402
from deployworld import hyrox_targets, use_fake_adb, write_profile  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_apps import second_app  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402
from test_runner import script_until_interrupted  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
diagnostic.FIND = lambda tool: None
STATES = {"hyrox_tracker": chain.UP_TO_DATE, "belivo": chain.BEHIND}
SUMMARY = {chain.UP_TO_DATE: "Chaîne à jour — 959eabd du 2026-10-07",
           chain.BEHIND: "Chaîne en retard de 2 commits — installée : fadf15a du 2026-10-06"}


def per_app_chain(app):
    st = STATES.get(os.path.basename(app), chain.UP_TO_DATE)
    return {"state": st, "summary": SUMMARY[st], "commit": "959eabd", "date": "2026-10-07",
            "chain_commit": "959eabd", "chain_date": "2026-10-07", "behind": 2 if st == chain.BEHIND else None,
            "subjects": ["Chaîne — le rapport du Bâtisseur, un par application", "Cockpit — Bâtir après le découpage"]
            if st == chain.BEHIND else [], "modified": []}


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def world(s, t):
    """Two applications — the one the fake server opens, renamed, and
    Belivo —, a relay, the deploy profile, the audits' commands."""
    s.state.rename_app(str(s.app_root), "Hyrox Tracker")
    for name, desc in (("audit_blocages", "Read a cycle's blocking files and report what recurs across them"),
                       ("audit_conventions", "Read what the conventions gained during a cycle and report what it costs"),
                       ("batir", "Build the project skeleton the conventions declare, and prove it builds"),
                       ("fusion_applique", "Apply the merge plan and write the report")):
        (s.app_root / ".claude" / "commands" / f"{name}.md").write_text(
            f'---\ndescription: {desc}\nargument-hint: "<feature folder name>"\n---\nbody\n', encoding="utf-8")
    line = "Next: run /3_decoupe f"
    s.state.set_relay(str(s.app_root), "f", "/2_structure f", "Fini.\n" + line, nextline.parse(line).to_dict(), "terminé")
    b = t / "belivo"
    second_app(b)
    s.state.add_app(str(b))
    s.state.rename_app(str(b), "Belivo")
    s.state.open_pair(str(b), "g")
    s.state.activate(str(s.app_root))
    fa = use_fake_adb(t / "adb")
    write_profile(s.app_root, hyrox_targets(fa))
    return b, fa


def avant(page, out, s):
    page.goto(s.url)
    page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
    snap(page, out, "avant-01-demarrage")
    page.goto(s.url + "#apps")
    page.wait_for_selector(".app-row")
    snap(page, out, "avant-02-applications")
    page.get_by_role("button", name="Nouvelle application").click()
    page.wait_for_selector("#new-app:not(.hidden)")
    snap(page, out, "avant-03-nouvelle-application")
    page.goto(s.url + "#dashboard")
    page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
    page.locator("#tb-app").click()
    snap(page, out, "avant-04-tableau-de-bord-barre-du-haut")
    page.keyboard.press("Escape")
    page.goto(s.url + "#chaine")
    page.wait_for_selector("#step-main-fusion")
    page.locator("#step-main-fusion").scroll_into_view_if_needed()
    snap(page, out, "avant-05-chaine-amont-en-bas")
    page.goto(s.url + "#deploy")
    page.get_by_role("tab", name="Déployer").click()
    page.wait_for_selector("#dp-targets")
    snap(page, out, "avant-06-deploiement")
    page.goto(s.url + "#settings")
    page.wait_for_selector("#diag-result li")
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
    snap(page, out, "avant-07-parametres-haut")
    for sec, name in (("sec-diag", "diagnostic"), ("sec-chain", "chaine"), ("sec-deploy", "deploiement"),
                      ("sec-commands", "commandes"), ("sec-notes", "notifications"), ("sec-maint", "maintenance")):
        page.locator("#" + sec).evaluate("e => e.scrollIntoView({block: 'start'})")
        snap(page, out, f"avant-08-parametres-{name}")


def apres(page, out, s, b):
    page.goto(s.url)
    page.wait_for_selector(".home-card")
    snap(page, out, "apres-01-demarrage-accueil")
    page.locator('.home-card[data-name="Belivo"] .hc-menu-btn').click()
    page.wait_for_selector(".hc-menu:not(.hidden)")
    snap(page, out, "apres-02-accueil-menu-d-une-carte")
    page.keyboard.press("Escape")
    page.get_by_role("button", name="Nouvelle application").click()
    page.wait_for_selector("#scr-nouvelle:not(.hidden)")
    page.locator("#nf-name").fill("Carnet de vélo")
    page.wait_for_function("document.getElementById('nf-path').textContent.includes('carnet-de-velo')")
    snap(page, out, "apres-03-nouvelle-application")
    page.get_by_role("button", name="Retour").first.click()
    page.wait_for_selector(".home-card")
    page.locator('.home-card[data-name="Hyrox Tracker"]').click()
    page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
    snap(page, out, "apres-04-tableau-de-bord-barre-du-haut")
    page.get_by_role("link", name="Chaîne").first.click()
    page.wait_for_selector("#audits")
    page.locator("#audits").scroll_into_view_if_needed()
    snap(page, out, "apres-05-chaine-amont-audits")
    page.get_by_role("tab", name="Version").click()
    page.wait_for_selector("#set-chain b")
    snap(page, out, "apres-06-chaine-version")
    page.get_by_role("link", name="Déploiement").first.click()
    page.get_by_role("tab", name="Profil").click()
    page.wait_for_selector(".dp-tgt")
    snap(page, out, "apres-07-deploiement-profil")
    page.get_by_role("link", name="Paramètres").click()
    page.wait_for_selector("#diag-result li")
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
    snap(page, out, "apres-08-parametres-haut")
    page.locator("#sec-quit").evaluate("e => e.scrollIntoView({block: 'end'})")
    snap(page, out, "apres-09-parametres-bas")
    # A run going in Hyrox Tracker: leaving it says so, once; it keeps going.
    s.script = script_until_interrupted
    s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
    page.get_by_role("link", name="Chaîne").first.click()
    page.wait_for_selector("#tb-stop:not(.hidden)")
    page.locator("#tb-home").click()
    page.wait_for_selector("#home-notice:not(.hidden)")
    page.wait_for_selector('.home-card[data-name="Hyrox Tracker"] .hc-running')
    snap(page, out, "apres-10-accueil-une-commande-tourne")
    page.locator('.home-card[data-name="Belivo"]').click()
    page.wait_for_selector("#busy-banner:not(.hidden)")
    page.get_by_role("link", name="Chaîne").first.click()
    page.get_by_role("tab", name="Amont").click()
    page.wait_for_selector("#flow-main li.step")
    snap(page, out, "apres-11-autre-application-lancer-refuse")
    s.call(s.rn.stop_now(str(s.app_root)))


def main(out_dir, phase):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    server.chain_state = per_app_chain
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("dialog", lambda d: d.accept())
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            with FakeServer(t / "w") as s:
                b, fa = world(s, t)
                avant(page, out, s) if phase == "avant" else apres(page, out, s, b)
                s.app[server.DEPLOY_KEY].stop_all()
                fa.close()
        browser.close()
        if errors:
            print("erreurs de la page :", *errors, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
