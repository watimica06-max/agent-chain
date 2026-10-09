"""1.13 — the cockpit on a phone screen: the screens the phone uses, and
those it leaves to the computer, at 390 × 844 and 412 × 915, with touch.

    python tests/shots113.py <out-dir> avant
    python tests/shots113.py <out-dir> apres

Each shot writes <out-dir>/<phase>/<w>x<h>/<name>.png, and one line per shot
into <out-dir>/<phase>/<w>x<h>/defilement.txt: whether the page scrolls
sideways there, and the widest element that overflows. A step on a control
the phone layout adds is skipped where it does not exist — « avant » shoots
the screen all the same. Not a test: run by hand, like shots111.py. No chain
command runs — the SDK client is a fake —, no real device is touched — adb
is a fake — and every repository is a scratch one.
"""
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

SIZES = ((390, 844), (412, 915))

# Whether the page scrolls sideways, and the elements wider than the screen.
OVERFLOW_JS = """() => {
  const w = document.documentElement.clientWidth;
  const doc = document.documentElement.scrollWidth > w;
  let worst = null;
  for (const el of document.querySelectorAll('body *')) {
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (!r.width || r.right <= w + 1) continue;
    let p = el.parentElement, clipped = false;
    while (p && p !== document.body) {
      const ps = getComputedStyle(p);
      if (/(auto|scroll|hidden|clip)/.test(ps.overflowX) && p.getBoundingClientRect().right <= w + 1) { clipped = true; break; }
      p = p.parentElement;
    }
    if (clipped) continue;
    if (!worst || r.right > worst.right) worst = {right: Math.round(r.right), tag: el.tagName.toLowerCase(),
      id: el.id, cls: [...el.classList].join('.')};
  }
  return {doc, worst};
}"""


def main(out_dir, phase):
    from playwright.sync_api import sync_playwright

    import diagnostic
    import nextline
    import server
    from deployworld import use_fake_adb  # noqa: F401  (world() uses it)
    from donneesworld import data_world
    from fakeapp import FakeServer
    from shots19 import per_app_chain, world
    from syncworld import app_world, change
    from test_flow import add_turn_feature
    from test_mode_diagnostic import ALL_GOOD, fake_exec
    from test_page_code import with_lots
    from test_page_context import MODEL, PRODUCT
    from test_statistics import fixture_store

    server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
    server.PROFILE_PUSH = False
    server.DONNEES_PUSH = False
    server.REVEAL = lambda path, select=False: None
    server.chain_state = per_app_chain
    diagnostic.FIND = lambda tool: None

    root = Path(out_dir) / phase
    shutil.rmtree(root, ignore_errors=True)
    failed = []

    def maybe(what, fn):
        """A step on a control the phone layout adds: skipped where it does not exist."""
        try:
            fn()
            return True
        except Exception as e:
            print(f"  ({phase}) étape sautée — {what} : {type(e).__name__}")
            return False

    def scenes(page, t, shots, lines):
        def snap(name):
            page.wait_for_timeout(600)
            page.screenshot(path=str(shots / f"{name}.png"))
            o = page.evaluate(OVERFLOW_JS)
            w = o["worst"]
            lines.append(f"{name}: " + ("défile de côté" if o["doc"] else "ne défile pas de côté")
                         + (f" — le plus large : {w['tag']}{'#' + w['id'] if w['id'] else ''}"
                            f"{'.' + w['cls'] if w['cls'] else ''}, bord droit à {w['right']} px" if w else ""))
            print("shot", shots.name, name)

        def nav(screen, hash_):
            """Reach a screen the way a thumb would: the phone's navigation
            when it exists, the hash otherwise."""
            if not maybe(f"navigation vers {screen}",
                         lambda: page.locator(f'#phone-nav a[href="{hash_}"]').click(timeout=1500)):
                page.evaluate(f"location.hash = '{hash_}'")

        # -------------------------------------------------- home, dashboard, chain, a run, the desktop-only screens
        with FakeServer(t / "w", stats=fixture_store(str(t / "stats-w.sqlite"))) as s:
            _, fa = world(s, t)
            with_lots(s, t / "w-src")
            page.goto(s.url)
            page.wait_for_selector(".home-card")
            snap("01-accueil")
            # « ⋯ » (Renommer, Retirer) is the computer's on the phone: the screen is shot all the same.
            if maybe("le menu d'une ligne", lambda: page.locator(
                    '.home-card[data-name="Belivo"] .hc-menu-btn').click(timeout=1500)):
                page.wait_for_selector(".hc-menu:not(.hidden)")
            snap("02-accueil-menu-d-une-ligne")
            page.keyboard.press("Escape")
            page.locator('.home-card[data-name="Hyrox Tracker"]').click()
            page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
            page.wait_for_timeout(800)
            snap("03-tableau-de-bord")
            page.locator("#tb-folder").click()
            snap("04-changer-de-fonctionnalite")
            page.keyboard.press("Escape")
            maybe("le menu du téléphone", lambda: page.locator("#phone-more").click(timeout=1500))
            snap("05-navigation")
            page.keyboard.press("Escape")
            nav("Chaîne", "#chaine")
            page.wait_for_selector("#flow-main li.step")
            page.get_by_role("tab", name="Amont").first.click()
            snap("06-chaine")
            page.locator("#step-main-8_code").evaluate("e => e.scrollIntoView({block: 'center'})")
            snap("07-lancer-lots-a-coder")
            # A run going, with a permission to give.
            s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
            page.wait_for_selector("#perm-banner .perm", timeout=8000)
            page.wait_for_selector("#slot-main-1_lexique #run-panel")
            snap("08-run-autorisation")
            page.locator("#slot-main-1_lexique #run-panel").evaluate("e => e.scrollIntoView({block: 'start'})")
            snap("09-run-en-cours")
            nav("Tableau de bord", "#dashboard")
            page.wait_for_timeout(500)
            snap("10-tableau-de-bord-run")
            s.call(s.rn.stop_now(str(s.app_root)))
            page.wait_for_timeout(800)
            for name, hash_ in (("30-deploiement", "#deploy"), ("31-statistiques", "#stats"),
                                ("32-parametres", "#settings"), ("33-correction", "#correction")):
                page.evaluate(f"location.hash = '{hash_}'")
                page.wait_for_timeout(900)
                snap(name)
            page.goto(s.url + "#nouvelle")
            page.wait_for_timeout(900)
            snap("34-nouvelle-application")
            page.goto(s.url)
            page.wait_for_selector(".home-card")
            maybe("Ajouter depuis GitHub", lambda: page.locator("#btn-app-clone").click(timeout=1500))
            snap("35-ajouter-une-application")
            s.app[server.DEPLOY_KEY].stop_all()
            fa.close()

        # -------------------------------------------------- « À répondre »: a question card
        with FakeServer(t / "b") as s:
            (s.feat / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
            (s.feat / "convertisseur" / "model.md").write_text(MODEL, encoding="utf-8")
            line = "Next: answer questions, then run /4_grille f"
            s.state.set_relay(str(s.app_root), "f", "/4_grille f", "Fini.\n" + line,
                              nextline.parse(line).to_dict(), "terminé")
            page.goto(s.url + "#answer")
            page.wait_for_selector(".entry")
            snap("11-a-repondre")
            page.locator('.entry[data-id="q:questions-sondeur-02.md#1"] .head').click()
            page.locator('.entry[data-id="q:questions-sondeur-02.md#1"]').evaluate(
                "e => e.scrollIntoView({block: 'start'})")
            snap("12-a-repondre-une-question")

        # -------------------------------------------------- « À répondre »: a blocking file
        with FakeServer(t / "st") as s:
            add_turn_feature(s.app_root, "t", ["questions-convertisseur-01.md"], blocked_classeur=True)
            s.state.open_pair(str(s.app_root), "t")
            page.goto(s.url + "#answer")
            page.wait_for_selector(".entry")
            blk = page.locator('.entry[data-id^="b:"]').first
            if not maybe("la carte du blocage", lambda: blk.evaluate("e => e.scrollIntoView({block: 'start'})", timeout=1500)):
                page.locator(".entry").last.evaluate("e => e.scrollIntoView({block: 'start'})")
            snap("13-a-repondre-un-blocage")

        # -------------------------------------------------- « Données », joining a file to an answer
        with FakeServer(t / "dn") as s:
            data_world(s.app_root)
            s.state.rename_app(str(s.app_root), "Budget")
            page.goto(s.url + "#donnees")
            page.get_by_role("tab", name="De la fonctionnalité").click()
            page.wait_for_selector("#dn-list tr[data-name='releve-2026-09-14.csv']")
            snap("14-donnees")
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-show").click()
            page.wait_for_selector("#dn-preview pre")
            page.locator("#dn-preview").evaluate("e => e.scrollIntoView({block: 'start'})")
            snap("15-donnees-apercu")
            page.goto(s.url + "#answer")
            page.wait_for_selector(".entry")
            card = page.locator(".entry", has=page.locator("b", has_text="Q4"))
            card.locator(".head").click()
            card.locator(".q-join-btn").evaluate("e => e.scrollIntoView({block: 'center'})")
            snap("16-a-repondre-joindre-un-fichier")

        # -------------------------------------------------- GitHub (1.12): answers to send, a divergence to reconcile
        _, carnet, _ = app_world(t, "carnet")
        change(carnet, "docs/features/f/notes.md", "notes\n", "notes: f")
        q = carnet / "docs" / "features" / "f" / "questions-lexicographe-01.md"
        q.write_bytes(q.read_bytes().replace(b"Answer:\n", b"Answer: Non, deux choses.\n", 1))
        _, budget, budget_b = app_world(t, "budget")
        change(budget_b, "README.md", "Budget, de l'autre ordinateur\n", push=True)
        change(budget, "README.md", "Budget, d'ici\n")
        with FakeServer(t / "srv", opened=False) as s:
            for folder, name in ((carnet, "Carnet de vélo"), (budget, "Budget")):
                s.state.add_app(str(folder))
                s.state.rename_app(str(folder), name)
                s.state.open_pair(str(folder), "f")
            for name, shot in (("Carnet de vélo", "17-tableau-de-bord-github-envoyer"),
                               ("Budget", "18-tableau-de-bord-github-reconcilier")):
                page.goto(s.url)
                page.wait_for_selector(".home-card")
                page.locator(f'.home-card[data-name="{name}"]').click()
                page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
                page.wait_for_timeout(2500)
                maybe("l'état GitHub", lambda: page.locator("#alerts .sync-alert").first.evaluate(
                    "e => e.scrollIntoView({block: 'center'})", timeout=1500))
                snap(shot)
            page.goto(s.url)
            page.wait_for_selector(".home-card")
            page.locator('.home-card[data-name="Carnet de vélo"]').click()
            page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
            page.wait_for_timeout(1500)            # the dashboard of the application opened, not the last one's
            page.evaluate("location.hash = '#answer'")

            page.wait_for_selector(".entry")
            page.locator("#btn-send-answers").evaluate("e => e.scrollIntoView({block: 'center'})")
            snap("19-a-repondre-envoyer-mes-reponses")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        for w, h in SIZES:
            shots = root / f"{w}x{h}"
            shots.mkdir(parents=True)
            lines = []
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2,
                                      is_mobile=True, has_touch=True)
            page = ctx.new_page()
            page.set_default_timeout(15000)
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("dialog", lambda d: d.accept())
            with tempfile.TemporaryDirectory() as t:
                try:
                    scenes(page, Path(t), shots, lines)
                except Exception:
                    failed.append(f"{w}x{h}")
                    traceback.print_exc()
            ctx.close()
            (shots / "defilement.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
            if errors:
                print(f"{w}x{h} erreurs de la page :", *errors, sep="\n  ")
        browser.close()
    print("en échec :", failed or "rien")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
