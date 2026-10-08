"""1.12 — always agreeing with GitHub: the screens it changes, at
1280 × 800, before and after.

    python tests/shots112.py <out-dir> avant <cockpit-dir-of-HEAD>
    python tests/shots112.py <out-dir> apres

« avant » runs the same scenes against the cockpit of another checkout —
a worktree of `HEAD` taken before 1.12 — where the new controls do not
exist: a scene's step that needs one is skipped, the screen is shot all the
same. Not a test: run by hand, like shots111.py. No chain command runs — the
SDK client is a fake —; GitHub is a bare repository in a temporary folder.
"""
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))


def main(out_dir, phase, cockpit=None):
    cockpit = os.path.abspath(cockpit or os.path.dirname(HERE))
    sys.path[:0] = [cockpit, os.path.join(cockpit, "tests"), HERE]
    from playwright.sync_api import sync_playwright
    from claude_agent_sdk import AssistantMessage, TextBlock

    import diagnostic
    import server
    from donneesworld import data_world
    from fakeapp import FakeServer
    from syncworld import app_world, change, offline, world
    from test_chain import commit, git
    from test_mode_diagnostic import ALL_GOOD, fake_exec
    from test_runner import result

    server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
    server.PROFILE_PUSH = False
    server.DONNEES_PUSH = False
    server.REVEAL = lambda path, select=False: None
    diagnostic.FIND = lambda tool: None

    newer = {"state": "plus récente", "commit": "7b1c2d4", "date": "2026-10-08", "chain_commit": "959eabd",
             "chain_date": "2026-10-07", "behind": None, "subjects": [], "modified": [], "newer": True,
             "summary": "Chaîne plus récente que celle de cet ordinateur — installée : 7b1c2d4 du 2026-10-08 ; "
                        "ici : 959eabd du 2026-10-07",
             "refused": "la chaîne installée (7b1c2d4 du 2026-10-08) est plus récente que celle de cet ordinateur "
                        "(959eabd du 2026-10-07) : l'installer remplacerait une chaîne plus récente par une plus "
                        "ancienne — récupérer agent-chain sur cet ordinateur (redémarrer le cockpit le fait), "
                        "puis réessayer"}
    fine = {"state": "à jour", "summary": "Chaîne à jour — 959eabd du 2026-10-07", "commit": "959eabd",
            "date": "2026-10-07", "chain_commit": "959eabd", "chain_date": "2026-10-07", "behind": None,
            "subjects": [], "modified": [], "newer": False}
    server.chain_state = lambda app: newer if os.path.basename(os.path.dirname(app)) == "velo" else fine

    shots = Path(out_dir) / phase
    shutil.rmtree(shots, ignore_errors=True)
    shots.mkdir(parents=True)
    failed = []

    def snap(page, name):
        page.wait_for_timeout(700)
        page.screenshot(path=str(shots / f"{name}.png"))
        print("shot", name)

    def maybe(what, fn):
        """A step on a control 1.12 adds: skipped where it does not exist."""
        try:
            fn()
            return True
        except Exception as e:
            print(f"  ({phase}) étape sautée — {what} : {type(e).__name__}")
            return False

    def home(page, s):
        page.goto(s.url)
        page.wait_for_selector(".home-card")

    def open_row(page, s, name):
        home(page, s)
        page.locator(f'.home-card[data-name="{name}"]').click()
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        page.wait_for_timeout(1500)

    def scenes(page, t):
        # The chain's own clone, behind GitHub: pulled when the cockpit starts.
        _, chain_a, chain_b = world(t / "chaine")
        change(chain_b, "tools/cockpit/x.py", "nouveau\n", push=True)
        server.CHAIN_ROOT = str(chain_a)
        server.SYNC_CHAIN_AT_START = True
        server.SYNC_APPS_AT_START = True
        # Five applications, one per state.
        _, hyrox, hyrox_b = app_world(t, "hyrox")
        git(hyrox, "config", "--local", "core.longpaths", "true")
        _, belivo, belivo_b = app_world(t, "belivo")
        change(belivo_b, "docs/features/f/lexique.md", "# Lexique\n", push=True)
        change(belivo_b, "README.md", "Belivo, de l'autre ordinateur\n", push=True)
        _, carnet, _ = app_world(t, "carnet")
        change(carnet, "docs/features/f/notes.md", "notes\n", "notes: f")
        q = carnet / "docs" / "features" / "f" / "questions-lexicographe-01.md"
        q.write_bytes(q.read_bytes().replace(b"Answer:\n", b"Answer: Non, deux choses.\n", 1))
        _, budget, budget_b = app_world(t, "budget")
        change(budget_b, "README.md", "Budget, de l'autre ordinateur\n", push=True)
        # Here, the answers given and committed with README.md: the next step launches /1_lexique.
        q = budget / "docs" / "features" / "f" / "questions-lexicographe-01.md"
        q.write_bytes(q.read_bytes().replace(b"Answer:\n", b"Answer: oui\n"))
        change(budget, "README.md", "Budget, d'ici\n")
        _, velo, _ = app_world(t, "velo")
        offline(velo)

        with FakeServer(t / "srv", opened=False) as s:
            for folder, name in ((hyrox, "Hyrox Tracker"), (belivo, "Belivo"), (carnet, "Carnet de vélo"),
                                 (budget, "Budget"), (velo, "Vélo-école")):
                s.state.add_app(str(folder))
                s.state.rename_app(str(folder), name)
                s.state.open_pair(str(folder), "f")
            home(page, s)
            page.wait_for_timeout(2500)
            home(page, s)
            snap(page, "01-accueil")

            open_row(page, s, "Belivo")
            snap(page, "02-tableau-de-bord-en-retard")

            open_row(page, s, "Budget")
            snap(page, "03-tableau-de-bord-diverge")
            page.locator("#next-detail button.primary").first.click()
            page.wait_for_timeout(2500)
            snap(page, "04-lancer-refuse-diverge")
            if s.rn.going():
                s.call(s.rn.stop_now(s.rn.going().repo))
                page.wait_for_timeout(1500)
            if maybe("Réconcilier", lambda: page.locator("button.sync-reconcile").first.click(timeout=3000)):
                page.wait_for_selector("#sync-banner .conflict", timeout=30000)
            snap(page, "05-reconcilier-conflit")

            open_row(page, s, "Carnet de vélo")
            snap(page, "06-tableau-de-bord-non-envoye")
            page.goto(s.url + "#answer")
            page.wait_for_selector(".entry")
            snap(page, "07-a-repondre-envoyer-mes-reponses")
            if maybe("Envoyer mes réponses", lambda: page.locator("#btn-send-answers").click(timeout=3000)):
                page.wait_for_selector("#answers-msg:not(:empty)", timeout=30000)
            snap(page, "08-a-repondre-reponses-envoyees")

            # A run whose final push GitHub refused: the other computer pushed meanwhile.
            async def rejected(c):
                change(hyrox, "docs/features/f/lexique.md", "# Lexique\n", "lexique: f — lexique")
                change(hyrox_b, "README.md", "Hyrox, de l'autre ordinateur\n", push=True)
                yield AssistantMessage(content=[TextBlock("Lexique écrit et commité. git push : rejected "
                                                          "(fetch first).")], model="m")
                yield result("Lexique écrit.\nNext: answer questions, then run /1_lexique f")
            s.script = rejected
            open_row(page, s, "Hyrox Tracker")
            page.goto(s.url + "#chaine")
            page.wait_for_selector("#flow-main li.step")
            s.call(s.rn.start(str(hyrox), "f", "f", "1_lexique", "f"))
            page.wait_for_function("document.getElementById('stream').textContent.includes('■ Fin')", timeout=20000)
            page.wait_for_selector("#run-end .run-total")
            maybe("le push vérifié", lambda: page.wait_for_selector("#run-end .run-sync.bad", timeout=30000))
            page.locator("#run-end").evaluate("e => e.scrollIntoView({block: 'end'})")
            snap(page, "09-chaine-fin-du-run-push-refuse")

            page.goto(s.url + "#settings")
            page.wait_for_selector("#diag-result li")
            maybe("chemins longs", lambda: page.wait_for_selector("#longpaths li", timeout=8000))
            page.locator("#sec-diag").evaluate("e => e.scrollIntoView({block: 'start'})")
            snap(page, "10-parametres-outils-chemins-longs")

            # « Ajouter depuis GitHub »: the second computer's clone.
            remote, _, _ = app_world(t, "plan")
            parent = t / "deuxieme-ordinateur"
            parent.mkdir()
            home(page, s)
            if maybe("Ajouter depuis GitHub", lambda: page.locator("#btn-app-clone").click(timeout=3000)):
                page.locator("#clone-url").fill(str(remote))
                page.locator("#clone-parent").fill(str(parent))
                page.wait_for_timeout(600)
            else:
                page.locator("#btn-app-add").click()
            snap(page, "11-ajouter-depuis-github")
            if maybe("Cloner", lambda: page.locator("#btn-clone").click(timeout=3000)):
                page.wait_for_selector('.home-card[data-name="app"]', timeout=30000)
            snap(page, "12-accueil-apres-clone")

        # « Données »: a private file the other computer holds.
        with FakeServer(t / "dn") as s:
            data_world(s.app_root)
            feat = s.app_root / "docs" / "features" / "f" / "donnees"
            (feat / "donnees.md").write_bytes((feat / "donnees.md").read_bytes() + (
                "\n## releve-compte-joint.csv\nWhat: the joint account's statement, as the bank exports it\n"
                "Source: exported by the Product Owner, on the other computer\nDate: 2026-10-07\nPrivate: yes\n"
            ).encode("utf-8"))
            (s.app_root / ".gitignore").write_bytes(
                b"build/\n\n# Donn\xc3\xa9es priv\xc3\xa9es \xe2\x80\x94 .claude/formats/donnees.md\n"
                b"docs/features/f/donnees/releve-compte-joint.csv\n")
            commit(s.app_root, "donnees: releve-compte-joint.csv joint, privé")
            s.state.rename_app(str(s.app_root), "Budget")
            page.goto(s.url + "#donnees")
            page.get_by_role("tab", name="De la fonctionnalité").click()
            page.wait_for_selector("#dn-list tr[data-name='releve-compte-joint.csv']")
            snap(page, "13-donnees-prive-absent")
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] button.dn-edit").click()
            page.locator("#dn-list tr[data-name='releve-2026-09-14.csv'] textarea, "
                         "#dn-list tr[data-name='releve-2026-09-14.csv'] input[name=what]").first.fill(
                "a statement of operations, as the bank's site exports it — September")
            page.locator("#dn-save").click()
            page.wait_for_timeout(2500)
            page.locator("#dn-msg").evaluate("e => e.scrollIntoView({block: 'start'})")
            page.locator("#dn-msg").evaluate("e => e.scrollIntoView({block: 'start'})")
            snap(page, "14-donnees-enregistrer")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        with tempfile.TemporaryDirectory() as t:
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.set_default_timeout(15000)
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("dialog", lambda d: d.accept())
            try:
                scenes(page, Path(t))
            except Exception:
                failed.append("scenes")
                traceback.print_exc()
            page.close()
            if errors:
                print("erreurs de la page :", *errors, sep="\n  ")
        browser.close()
    print("en échec :", failed or "rien")


if __name__ == "__main__":
    main(*sys.argv[1:4])
