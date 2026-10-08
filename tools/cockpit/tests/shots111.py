"""1.11 — every screen and every state, at 1280 × 800, before and after the
restyle, with each screen's DOM beside its picture.

    python tests/shots111.py <out-dir> avant
    python tests/shots111.py <out-dir> apres
    python tests/shots111.py <out-dir> apres-sombre
    python tests/shots111.py <out-dir> diff
    python tests/shots111.py <out-dir> inventaire

Each shot writes <name>.png into <out-dir>/<phase>/ and the DOM it shows —
one line per element: tag, id, classes, its own text — into
<out-dir>/dom-<phase>/<name>.txt. « diff » reads both DOM folders and says,
screen by screen, what differs beyond a class added to an existing element:
the restyle's boundary until the 1.11 scope grew; « inventaire » then
replaced it: every text and every control of a screen before is still on it
after, wherever it moved. « apres-sombre » takes the same screens with the
computer set to dark. Not a test: run by hand, like shots191.py. No chain
command runs — the SDK client is a fake —, no real device is touched — adb is
a fake — and every repository is a scratch one.
"""
import os
import re
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

DOM_JS = """() => {
  const out = [];
  const walk = (el, d) => {
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
    const cls = [...el.classList].sort().join('.');
    const txt = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent)
      .join('').replace(/\\s+/g, ' ').trim();
    out.push(' '.repeat(d) + el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + '|' + cls + '|' + txt);
    for (const c of el.children) walk(c, d + 1);
  };
  walk(document.body, 0);
  return out.join('\\n');
}"""


def steady(text):
    """What changes from one run to the next by itself: the scratch folder's
    name, the clock."""
    text = re.sub(r"tmp[a-z0-9_]{6,}", "tmp…", text)
    text = re.sub(r"perm-[0-9a-f]{10}", "perm-…", text)
    text = re.sub(r"-[0-9a-f]{4}\.log\b", "-….log", text)
    text = re.sub(r"\d{4}-\d{2}-\d{2}[ T-]\d{2}[:]?\d{2}[:]?\d{2}", "<date-heure>", text)
    return re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", "<heure>", text)


def parse(line):
    depth = len(line) - len(line.lstrip(" "))
    head, cls, txt = line.strip().split("|", 2)
    return depth, steady(head), set(cls.split(".")) - {""}, steady(txt)


def diff(out):
    """The boundary: same elements, same order, same nesting, same ids and
    texts; each element's classes before all kept after."""
    a, b = out / "dom-avant", out / "dom-apres"
    bad = 0
    for f in sorted(a.glob("*.txt")):
        g = b / f.name
        if not g.exists():
            print(f"{f.stem}: pas de capture « après »")
            bad += 1
            continue
        la, lb = f.read_text(encoding="utf-8").splitlines(), g.read_text(encoding="utf-8").splitlines()
        added, problems = 0, []
        if len(la) != len(lb):
            problems.append(f"{len(la)} éléments avant, {len(lb)} après")
        for i, (x, y) in enumerate(zip(la, lb)):
            dx, hx, cx, tx = parse(x)
            dy, hy, cy, ty = parse(y)
            if (dx, hx, tx) != (dy, hy, ty) or not cx <= cy:
                problems.append(f"ligne {i + 1}:\n    avant {x.strip()}\n    après {y.strip()}")
            added += len(cy - cx)
        if problems:
            bad += 1
            print(f"{f.stem}: {len(problems)} écart(s)")
            for p in problems[:12]:
                print("  " + p)
        else:
            print(f"{f.stem}: identique, {len(la)} éléments, {added} classe(s) ajoutée(s)")
    print("écrans en écart :", bad)
    return bad


CONTROLS = ("button", "a", "input", "select", "textarea", "summary")


def inventory(out):
    """1.11, once the structure may change: every text and every control a
    screen showed before is still on it after — wherever it moved. A text is
    an element's own text; a control, its tag and id, else its text. What is
    missing is listed, screen by screen."""
    from collections import Counter
    a, b = out / "dom-avant", out / "dom-apres"

    def read(f):
        texts, ctrls = Counter(), Counter()
        for line in f.read_text(encoding="utf-8").splitlines():
            _, head, _, txt = parse(line)
            tag, _, ident = head.partition("#")
            if txt:
                texts[txt] += 1
            if tag in CONTROLS:
                ctrls[f"{tag}#{ident}" if ident else f"{tag} « {txt} »"] += 1
        return texts, ctrls

    bad = 0
    for f in sorted(a.glob("*.txt")):
        g = b / f.name
        if not g.exists():
            print(f"{f.stem}: pas de capture « après »")
            bad += 1
            continue
        (ta, ca), (tb, cb) = read(f), read(g)
        lost_t, lost_c = ta - tb, ca - cb
        if lost_t or lost_c:
            bad += 1
            print(f"{f.stem}: {sum(lost_t.values())} texte(s), {sum(lost_c.values())} contrôle(s) introuvables après")
            for t in list(lost_t)[:15]:
                print("    texte    ", t[:110])
            for c in list(lost_c)[:15]:
                print("    contrôle ", c[:110])
        else:
            print(f"{f.stem}: tout y est — {sum(ta.values())} textes, {sum(ca.values())} contrôles")
    print("écrans où il manque quelque chose :", bad)
    return bad


def main(out_dir, phase):
    out = Path(out_dir)
    if phase == "diff":
        sys.exit(1 if diff(out) else 0)
    if phase == "inventaire":
        sys.exit(1 if inventory(out) else 0)

    from playwright.sync_api import sync_playwright

    import diagnostic
    import nextline
    import server
    from claude_agent_sdk import AssistantMessage, TextBlock
    from deployworld import use_fake_adb
    from donneesworld import data_world
    from fakeapp import FakeServer
    from shots19 import per_app_chain, world
    from shots_batir import premiere
    import batirworld as bw
    from test_flow import add_turn_feature
    from test_mode_diagnostic import ALL_GOOD, fake_exec
    from test_page_code import with_lots
    from test_page_context import IDEAS, LEX, MODEL, PRODUCT
    from test_runner import result, script_until_interrupted
    from test_scan import build_chain
    from test_statistics import fixture_store

    good = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})  # noqa: E731
    server.DIAG_RUNNER = good
    server.PROFILE_PUSH = False
    server.DONNEES_PUSH = False
    server.REVEAL = lambda path, select=False: None
    server.chain_state = per_app_chain
    diagnostic.FIND = lambda tool: None

    shots = out / phase
    doms = out / f"dom-{phase}"
    for d in (shots, doms):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    failed = []

    def snap(page, name, full=False):
        if full:
            page.set_viewport_size({"width": 1280, "height": 1460})
        page.wait_for_timeout(600)
        page.screenshot(path=str(shots / f"{name}.png"))
        (doms / f"{name}.txt").write_text(page.evaluate(DOM_JS), encoding="utf-8")
        if full:
            page.set_viewport_size({"width": 1280, "height": 800})
        print("shot", name)

    def group(fn, *a):
        try:
            fn(*a)
        except Exception:
            failed.append(fn.__name__)
            traceback.print_exc()

    def go(page, s, hash_, sel):
        page.goto(s.url + hash_)
        page.wait_for_selector(sel)

    async def one_lot(c):
        yield AssistantMessage(content=[TextBlock("lot-07 passe.")], model="m")
        yield result("lot-07 passe.\nNext: run /8_code f")

    # ---------------------------------------------------------------- groups
    def g_empty(page, t):
        """No application at all: the home screen, empty."""
        with FakeServer(t / "vide", opened=False) as s:
            page.goto(s.url)
            page.wait_for_timeout(800)
            snap(page, "01-accueil-vide")

    def g_main(page, t):
        """Two applications, lots to code, a deploy profile, statistics."""
        with FakeServer(t / "w", stats=fixture_store(str(t / "stats-w.sqlite"))) as s:
            b, fa = world(s, t)
            with_lots(s, t / "w-src")
            page.goto(s.url)
            page.wait_for_selector(".home-card")
            snap(page, "02-accueil")
            page.locator('.home-card[data-name="Belivo"] .hc-menu-btn').click()
            page.wait_for_selector(".hc-menu:not(.hidden)")
            snap(page, "03-accueil-menu-d-une-carte")
            page.keyboard.press("Escape")
            page.get_by_role("button", name="Nouvelle application").click()
            page.wait_for_selector("#scr-nouvelle:not(.hidden)")
            page.locator("#nf-name").fill("Carnet de vélo")
            page.wait_for_function("document.getElementById('nf-path').textContent.includes('carnet-de-velo')")
            snap(page, "04-nouvelle-application")
            page.get_by_role("button", name="Retour").first.click()
            page.wait_for_selector(".home-card")
            page.locator('.home-card[data-name="Hyrox Tracker"]').click()
            page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
            snap(page, "05-tableau-de-bord")
            page.locator("#tb-folder").click()
            snap(page, "05b-tableau-de-bord-menu-fonctionnalite")
            page.keyboard.press("Escape")
            go(page, s, "#chaine", "#flow-main li.step")
            page.get_by_role("tab", name="Amont").first.click()
            page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
            snap(page, "06-chaine-amont")
            page.locator("#audits").scroll_into_view_if_needed()
            snap(page, "07-chaine-amont-audits")
            page.locator("#tab-main-code").click()
            page.wait_for_selector("#lots-main tbody tr[data-lot]")
            page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
            snap(page, "08-chaine-code")
            page.locator("#lot-main-lot-03").click()
            page.wait_for_selector(".lot-detail")
            page.evaluate("document.getElementById('lot-main-lot-03').scrollIntoView({block: 'start'})")
            snap(page, "09-chaine-code-lot-ouvert")
            page.get_by_role("tab", name="Version").click()
            page.wait_for_selector("#set-chain b")
            snap(page, "10-chaine-version")
            page.get_by_role("tab", name="Amont").first.click()
            go(page, s, "#deploy", ".dp-card")
            snap(page, "11-deploiement-destinations")
            page.get_by_role("tab", name="Profil").click()
            page.wait_for_selector(".dp-tgt")
            snap(page, "12-deploiement-profil")
            page.get_by_role("tab", name="Journal").click()
            page.wait_for_timeout(600)
            snap(page, "13-deploiement-journal")
            page.get_by_role("tab", name="Déployer").click()
            page.wait_for_selector("#dp-targets")
            snap(page, "14-deploiement-deployer")
            page.locator('.dp-target[data-target="Téléphone"] > label input').check()
            page.get_by_role("button", name="Construire et installer").click()
            page.wait_for_selector('#dp-job[data-status="fait"]', timeout=30000)
            page.locator("#dp-job").evaluate("e => e.scrollIntoView({block: 'end'})")
            snap(page, "15-deploiement-sortie-complete")
            page.get_by_role("tab", name="Destinations").click()
            go(page, s, "#stats", "#st-tiles .tile")
            page.locator("#st-period button[data-p='tout']").click()
            page.wait_for_function("document.querySelectorAll('#tbl-history tbody tr').length > 0")
            page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
            snap(page, "16-statistiques")
            page.locator("#tbl-history tbody tr").first.click()
            page.wait_for_selector("#scr-stats .st-detail")
            page.locator("#scr-stats .st-detail").evaluate("e => e.scrollIntoView({block: 'center'})")
            snap(page, "17-statistiques-un-run")
            page.locator("#main").evaluate("m => m.scrollTo(0, m.scrollHeight)")
            snap(page, "18-statistiques-bas")
            go(page, s, "#settings", "#diag-result li")
            page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
            snap(page, "19-parametres-haut")
            page.locator("#sec-notes").evaluate("e => e.scrollIntoView({block: 'start'})")
            snap(page, "20-parametres-notifications")
            page.locator("#sec-quit").evaluate("e => e.scrollIntoView({block: 'end'})")
            snap(page, "21-parametres-bas")
            # A run going, with a permission to give: the step « en cours », the banner.
            go(page, s, "#chaine", "#flow-main li.step")
            s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
            page.wait_for_selector("#perm-banner .perm", timeout=8000)
            page.wait_for_selector("#slot-main-1_lexique #run-panel")
            snap(page, "22-chaine-run-en-cours-autorisation")
            page.get_by_role("link", name="Tableau de bord").first.click()
            snap(page, "23-tableau-de-bord-run")
            page.locator("#tb-home").click()
            page.wait_for_selector('.home-card[data-name="Hyrox Tracker"] .hc-running')
            snap(page, "24-accueil-une-commande-tourne")
            page.locator('.home-card[data-name="Belivo"]').click()
            page.wait_for_selector("#busy-banner:not(.hidden)")
            page.get_by_role("link", name="Chaîne").first.click()
            page.wait_for_selector("#flow-main li.step")
            snap(page, "25-autre-application-lancer-refuse")
            s.call(s.rn.stop_now(str(s.app_root)))
            page.wait_for_timeout(800)
            # « Arrêter le cockpit »: the stopped page.
            go(page, s, "#settings", "#btn-quit")
            page.locator("#btn-quit").click()
            page.wait_for_selector("#stopped", state="visible", timeout=10000)
            snap(page, "27-cockpit-arrete")
            s.app[server.DEPLOY_KEY].stop_all()
            fa.close()

    def g_endrun(page, t):
        """A /8_code run that ended: its stream, « Fin du run »."""
        with FakeServer(t / "fin", script=one_lot) as s:
            s.state.rename_app(str(s.app_root), "Hyrox Tracker")
            with_lots(s, t / "fin-src")
            go(page, s, "#chaine", "#step-main-8_code")
            s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
            page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')")
            page.get_by_role("tab", name="Amont").first.click()
            page.wait_for_selector("#run-end .run-total")
            page.locator("#run-end").evaluate("e => e.scrollIntoView({block: 'end'})")
            snap(page, "26-chaine-fin-du-run")

    def g_answer(page, t):
        """« À répondre »: question cards, the context pane, the terms."""
        with FakeServer(t / "b") as s:
            (s.feat / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
            (s.feat / "convertisseur" / "model.md").write_text(MODEL, encoding="utf-8")
            line = "Next: answer questions, then run /4_grille f"
            s.state.set_relay(str(s.app_root), "f", "/4_grille f", "Fini.\n" + line,
                              nextline.parse(line).to_dict(), "terminé")
            go(page, s, "#answer", ".entry")
            snap(page, "30-a-repondre")
            page.locator('.entry[data-id="q:questions-sondeur-02.md#1"] .head').click()
            page.wait_for_function("document.getElementById('ctx-docname').textContent === 'desc-produit.md'")
            snap(page, "31-a-repondre-question-bloc")
            page.locator('.entry[data-id="q:questions-sondeur-02.md#2"] .head').click()
            page.wait_for_function("document.getElementById('ctx-note').textContent.includes('B14')")
            snap(page, "32-a-repondre-introuvable")
            page.locator(".filters button").last.click()
            snap(page, "33-a-repondre-filtre")
        with FakeServer(t / "h") as s:
            feat = s.app_root / "docs" / "features" / "lex"
            feat.mkdir(parents=True)
            (feat / "idees.md").write_text(IDEAS, encoding="utf-8")
            (feat / "questions-lexicographe-01.md").write_text(LEX, encoding="utf-8")
            s.state.open_pair(str(s.app_root), "lex")
            page.goto(s.url + "#answer")
            page.wait_for_function("document.getElementById('ctx-count').textContent === '1 / 4'")
            page.keyboard.press("2")
            page.get_by_role("button", name="Suivante ›").click()
            snap(page, "34-a-repondre-termes-clavier")
            page.evaluate("location.hash = '#dashboard'")
            page.wait_for_timeout(300)
            page.get_by_role("button", name="Fermer le menu").click()
            snap(page, "35-menu-ferme")
            page.get_by_role("button", name="Ouvrir le menu").click()

    def g_states(page, t):
        """The six step states, a blocking card, the why of a step."""
        with FakeServer(t / "st", script=script_until_interrupted) as s:
            add_turn_feature(s.app_root, "t", ["questions-convertisseur-01.md"], blocked_classeur=True)
            s.state.open_pair(str(s.app_root), "t")
            go(page, s, "#chaine", "#flow-main li.step")
            page.locator("#step-main-3b_nature").get_by_role("button", name="Pourquoi ?").click()
            page.locator("#main").evaluate("m => m.scrollTo(0, 0)")
            snap(page, "40-chaine-etats-faite-inconnu-attend-afaire", full=True)
            go(page, s, "#answer", ".entry")
            snap(page, "41-a-repondre-blocage")
            (s.app_root / ".claude" / "worktrees" / "f").mkdir(parents=True)
            s.state.open_pair(str(s.app_root), "f")
            page.goto(s.url + "?2#chaine")
            page.wait_for_selector("#flow-main li.step")
            page.locator("#step-main-1_lexique").get_by_role("button", name="Pourquoi ?").click()
            snap(page, "42-chaine-etat-bloquee")
            (s.app_root / ".claude" / "worktrees" / "f").rmdir()
            page.goto(s.url + "?3#chaine")
            page.wait_for_selector("#flow-main li.step")
            s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
            page.wait_for_function("document.querySelector('#step-main-1_lexique').dataset.state === 'en cours'")
            page.wait_for_selector("#slot-main-1_lexique #run-panel #stream")
            snap(page, "43-chaine-etat-en-cours")
            s.call(s.rn.stop_now(str(s.app_root)))

    def g_batir(page, t):
        """The Bâtisseur's tutorial, an empty « À répondre »."""
        with premiere(t, "ba") as s:
            go(page, s, "#answer", "#scr-answer")
            page.wait_for_timeout(600)
            snap(page, "44-a-repondre-vide")
            go(page, s, "#chaine", "#step-main-conventions")
            page.locator("#step-main-batir").get_by_role("button", name="Pourquoi ?").click()
            page.evaluate("document.querySelector('#step-main-batir').scrollIntoView({block: 'start'})")
            snap(page, "45-chaine-a-batir")
        with premiere(t, "bd") as s:
            feat = s.app_root / "docs" / "features" / "premiere"
            bw.report(feat, status="blocked")
            bw.blocked(feat)
            bw.request(feat)
            go(page, s, "#answer", "#form .entry")
            page.locator("#form .entry").first.scroll_into_view_if_needed()
            snap(page, "46-a-repondre-tutoriel")

    def g_errors(page, t):
        """An error: a diagnostic that fails; the files contradicting the relay."""
        def bad(app):
            return diagnostic.run_diagnostic(app, fake_exec(dict(ALL_GOOD, adb=(1, "adb: boom"))), env={})
        with FakeServer(t / "er", diag_runner=bad) as s:
            page.goto(s.url + "#dashboard")
            page.wait_for_function("document.getElementById('alerts').textContent.includes('a un échec')", timeout=8000)
            snap(page, "50-tableau-de-bord-erreur-diagnostic")
        with FakeServer(t / "d") as s:
            page.goto(s.url + "#dashboard")
            page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
            line = "Next: run /2_structure f"
            s.state.set_relay(str(s.app_root), "f", "/1_lexique f", "Fini.\n" + line, nextline.parse(line).to_dict())
            page.evaluate("location.hash = '#chaine'")
            page.get_by_role("button", name="Où on en est ?").click()
            page.wait_for_function("!document.getElementById('next-message').classList.contains('hidden')")
            page.evaluate("location.hash = '#dashboard'")
            page.get_by_role("button", name="Pourquoi ?").first.click()
            snap(page, "51-tableau-de-bord-contradiction")

    def g_correction(page, t):
        with FakeServer(t / "e") as s:
            build_chain(s.app_root, "chaine")
            (s.app_root / "docs" / "TECHNICAL_CONVENTIONS.md").write_text("# Conventions\n", encoding="utf-8")
            s.state.open_pair(str(s.app_root), "chaine")
            page.goto(s.url)
            page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
            snap(page, "52-tableau-de-bord-chaine-avancee")
            go(page, s, "#correction", "#flow-corr li.step")
            snap(page, "53-correction")
            page.locator("#corr-list button", has_text="bugfix-01").click()
            page.locator("#tab-corr-code").click()
            page.wait_for_selector("#lots-bugfix-01 tbody tr[data-lot]")
            snap(page, "54-correction-code")

    def g_donnees(page, t):
        with FakeServer(t / "dn0") as s:
            go(page, s, "#donnees", "#scr-donnees")
            page.wait_for_timeout(600)
            snap(page, "60-donnees-vide")
        with FakeServer(t / "dn") as s:
            data_world(s.app_root)
            s.state.rename_app(str(s.app_root), "Budget")
            page.goto(s.url + "#donnees")
            page.get_by_role("tab", name="De l'application").click()
            page.wait_for_selector("#dn-list tr[data-name='fleche.png']")
            page.locator("#dn-list tr[data-name='fleche.png'] button.dn-show").click()
            page.wait_for_selector("#dn-preview img")
            snap(page, "61-donnees-application-image")
            page.get_by_role("tab", name="De la fonctionnalité").click()
            page.wait_for_selector("#dn-list tr[data-name='releve-2026-09-14.csv']")
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-show").click()
            page.wait_for_selector("#dn-preview pre")
            snap(page, "62-donnees-fonctionnalite-texte")
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-edit").click()
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] input[name=private]").check()
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] .dn-history").wait_for()
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv']").evaluate(
                "e => e.scrollIntoView({block: 'center'})")
            snap(page, "63-donnees-modifier-prive")
            page.goto(s.url + "#answer")
            page.wait_for_selector(".entry")
            card = page.locator(".entry", has=page.locator("b", has_text="Q4"))
            card.locator(".head").click()
            card.evaluate("e => e.scrollIntoView({block: 'center'})")
            snap(page, "64-a-repondre-joindre-un-fichier")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            for g in (g_empty, g_main, g_endrun, g_answer, g_states, g_batir, g_errors, g_correction, g_donnees):
                page = browser.new_page(viewport={"width": 1280, "height": 800},
                                        color_scheme="dark" if phase.endswith("-sombre") else "light")
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("dialog", lambda d: d.accept())
                group(g, page, t)
                page.close()
                if errors:
                    print(g.__name__, "erreurs de la page :", *errors, sep="\n  ")
        browser.close()
    print("groupes en échec :", failed or "aucun")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
