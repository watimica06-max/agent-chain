"""1.6, 1.9 — the page with several applications, in a headless browser
(Microsoft Edge through Playwright): the home screen and its cards, a card's
menu, « Nouvelle application » as a page of its own, « Applications » in the
top bar, the notice when leaving with a run going, « Tout mettre à jour »'s
report, a run going in another application. Skipped when Playwright or Edge
is missing. No chain command runs, nothing is installed: the install is a
fake here — test_apps.py runs the real one on scratch repositories."""
import os

import pytest

pytest.importorskip("playwright")

import chain  # noqa: E402
import server  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_apps import second_app  # noqa: E402
from test_page import SCREENS, browser, go, no_real_errors, page  # noqa: E402,F401
from test_runner import script_until_interrupted  # noqa: E402

STATES = {"app": chain.UP_TO_DATE, "belivo": chain.ABSENT, "tardive": chain.BEHIND, "bricolee": chain.MODIFIED}


@pytest.fixture
def per_app_chain(monkeypatch):
    def fake(app):
        st = STATES.get(os.path.basename(app), chain.UP_TO_DATE)
        return {"state": st, "summary": {chain.UP_TO_DATE: "Chaîne à jour — 93d18fc du 2026-10-06",
                                         chain.ABSENT: "Chaîne absente — aucun .claude/chain-version.json",
                                         chain.BEHIND: "Chaîne en retard de 2 commits — installée : 5974c32 du 2026-10-05",
                                         chain.MODIFIED: "Chaîne modifiée sur place — 1 fichier : .claude/agents/b.md"}[st],
                "subjects": [], "modified": [], "chain_commit": "93d18fc", "chain_date": "2026-10-06"}
    monkeypatch.setattr(server, "chain_state", fake)


def with_belivo(s):
    b = s.tmp / "belivo"
    second_app(b)
    s.state.add_app(str(b))
    s.state.open_pair(str(b), "g")
    s.state.activate(str(s.app_root))
    return b


def card(page, name):
    return page.locator(f'.home-card[data-name="{name}"]')


def test_the_cockpit_opens_on_the_home_screen(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path) as s:
        b = with_belivo(s)
        page.goto(s.url)
        page.wait_for_selector(".home-card")
        # Never straight on a dashboard: no side menu, nothing of an application in the top bar.
        assert page.locator("#scr-accueil").is_visible() and not page.locator("#scr-dashboard").is_visible()
        assert not page.locator("#side").is_visible()
        for tb in ("#tb-home", "#tb-app", "#tb-folder", "#tb-mode", "#tb-menu"):
            assert not page.locator(tb).is_visible(), tb
        assert page.title() == "Applications — Cockpit"
        assert page.locator(".home-card").count() == 2
        # What « Applications » showed (1.6): name and folder, chain, feature and step, what waits, last run.
        t = card(page, "belivo").inner_text()
        assert "belivo" in t and str(b) in t and "absente" in t and "g" in t
        assert "1 question · 0 blocage" in t and "Répondre aux questions" in t and "aucun run mémorisé" in t
        assert card(page, "belivo").get_by_role("button", name="Installer la chaîne").is_visible()
        assert "chaîne à jour" in card(page, "app").inner_text()
        # « Tout mettre à jour » lives here.
        assert page.get_by_role("button", name="Tout mettre à jour").is_visible()
        # A click on a card opens the application on its dashboard.
        card(page, "belivo").click()
        page.wait_for_function("location.hash === '#dashboard' && document.getElementById('tb-app').textContent === 'belivo'")
        page.wait_for_function("document.getElementById('cnt-q').textContent === '1'")
        assert page.locator("#side").is_visible() and page.locator("#tb-home").is_visible()
        assert page.locator("#tb-folder").inner_text().startswith("g")
        assert s.state.app_folder.endswith("belivo")
        assert page.title().endswith("belivo — Cockpit")
        assert no_real_errors(page) == []


def test_new_application_is_a_page_of_its_own(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path) as s:
        page.goto(s.url)
        page.wait_for_selector(".home-card")
        page.get_by_role("button", name="Nouvelle application").click()
        # 1.12.2: the hash changes first, the screen on the `hashchange` that
        # follows — wait for the screen, not for the hash.
        page.wait_for_selector("#scr-nouvelle #new-app", state="visible")
        assert page.evaluate("location.hash") == "#nouvelle"
        assert page.locator("#scr-nouvelle #new-app").is_visible()
        assert not page.locator("#scr-accueil").is_visible() and not page.locator("#side").is_visible()
        # Full width: the form spans the screen, no side menu beside it.
        assert page.locator("#new-app").bounding_box()["width"] > 1000
        page.get_by_role("button", name="Retour").click()
        page.wait_for_selector("#scr-accueil", state="visible")
        assert page.locator(".home-card").count() == 1
        assert no_real_errors(page) == []


def test_add_and_the_card_menu(tmp_path, page, per_app_chain):
    b = tmp_path / "belivo"
    second_app(b)
    import subprocess
    subprocess.run(["git", "init", "-q", str(b)], check=True)
    with FakeServer(tmp_path, picker=lambda initial: str(b)) as s:
        page.on("dialog", lambda d: d.accept("Belivo") if d.type == "prompt" else d.accept())
        page.goto(s.url)
        page.wait_for_selector(".home-card")
        # « Ajouter une application »: the folder picker, as before.
        page.get_by_role("button", name="Ajouter une application").click()
        page.get_by_role("button", name="Parcourir…").click()
        page.wait_for_function("document.querySelectorAll('.home-card').length === 2")
        assert "ajoutée à la liste" in page.locator("#apps-msg").inner_text()
        # The card's small menu: « Renommer », « Retirer de la liste ».
        c = card(page, "belivo")
        c.get_by_role("button", name="Actions — belivo").click()
        menu = c.locator(".hc-menu")
        assert menu.is_visible()
        assert [x.strip() for x in menu.get_by_role("menuitem").all_inner_texts()] == ["Renommer", "Retirer de la liste"]
        menu.get_by_role("menuitem", name="Renommer").click()
        page.wait_for_selector('.home-card[data-name="Belivo"]')
        assert s.state.name_of(str(b)) == "Belivo"
        # Opening the menu opened nothing: still home.
        assert page.locator("#scr-accueil").is_visible()
        card(page, "Belivo").get_by_role("button", name="Actions — Belivo").click()
        page.keyboard.press("Escape")
        assert not card(page, "Belivo").locator(".hc-menu").is_visible()
        card(page, "Belivo").get_by_role("button", name="Actions — Belivo").click()
        card(page, "Belivo").get_by_role("menuitem", name="Retirer de la liste").click()
        page.wait_for_function("document.querySelectorAll('.home-card').length === 1")
        assert os.path.isdir(b / "docs" / "features" / "g") and len(s.state.apps()) == 1
        assert "Son dossier n'a pas été touché" in page.locator("#apps-msg").inner_text()
        assert no_real_errors(page) == []


def test_applications_in_the_side_menu_from_every_screen(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path) as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
        side = page.locator("#side").bounding_box()
        for name, scr in SCREENS:
            go(page, name)
            page.wait_for_selector(f"#{scr}", state="visible")
            # 1.11: at the foot of the side menu, under « Paramètres » (the right of the top bar until 1.10).
            box = page.locator("#tb-home").bounding_box()
            settings = page.locator("#nav-settings").bounding_box()
            assert box and box["x"] + box["width"] <= side["x"] + side["width"] and box["y"] > settings["y"] > 600, name
            page.locator("#tb-home").click()
            page.wait_for_selector("#scr-accueil", state="visible")
            assert not page.locator("#side").is_visible()
            card(page, "app").click()
            page.wait_for_selector("#scr-dashboard", state="visible")
        # No run going: no notice.
        page.locator("#tb-home").click()
        page.wait_for_selector(".home-card")
        assert not page.locator("#home-notice").is_visible()
        assert no_real_errors(page) == []


def test_leaving_with_a_run_going(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        b = with_belivo(s)
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#tb-stop", state="visible")
        run = s.rn.current(str(s.app_root))
        # Leaving: the notice, once; the run keeps going.
        page.locator("#tb-home").click()
        page.wait_for_selector("#home-notice", state="visible")
        assert page.locator("#home-notice").inner_text().startswith(
            "Une commande tourne dans app : elle continue. Tu la retrouves en rouvrant app.")
        assert s.rn.is_running(str(s.app_root)) and s.rn.current(str(s.app_root)) is run
        # Its card: « en cours », with its stop button.
        going = card(page, "app").locator(".hc-running")
        going.wait_for()
        assert "en cours" in going.inner_text() and "/1_lexique f" in going.inner_text()
        assert going.get_by_role("button", name="Arrêter").is_visible()
        # Another application opens while it runs — to read, to answer; launching there is refused, saying where.
        card(page, "belivo").click()
        page.wait_for_selector("#busy-banner", state="visible")
        assert "« app »" in page.locator("#busy-banner").inner_text()
        page.wait_for_function("document.getElementById('cnt-q').textContent === '1'")
        go(page, "Chaîne")
        page.get_by_role("tab", name="Amont").click()
        launch = page.locator("#flow-main").get_by_role("button", name="Lancer").first
        assert launch.is_disabled() and "« app »" in launch.get_attribute("title")
        go(page, "À répondre")
        page.wait_for_selector("#form .entry")
        # Back home again: the notice is not shown a second time for the same run.
        page.locator("#tb-home").click()
        page.wait_for_selector(".home-card .hc-running")
        page.wait_for_timeout(300)
        assert not page.locator("#home-notice").is_visible()
        assert s.rn.is_running(str(s.app_root))
        # The card's « Arrêter » stops it, asking first.
        card(page, "app").locator(".hc-running").get_by_role("button", name="Arrêter").click()
        page.wait_for_selector("#tb-stop", state="hidden")
        assert not s.rn.is_running(str(s.app_root))
        assert os.path.isdir(b)
        assert no_real_errors(page) == []


def test_update_all_report(tmp_path, page, per_app_chain, monkeypatch):
    installed = []

    def fake_install(app, root, confirm=False, push=True):
        assert not confirm                              # never in bulk
        installed.append(os.path.basename(app))
        return {"commit": "93d18fc", "date": "2026-10-06", "written": [], "removed": [], "app_commit": "4b1e0a2",
                "message": "chain: 93d18fc 2026-10-06", "pushed": True, "push_error": None}
    monkeypatch.setattr(chain, "install", fake_install)
    with FakeServer(tmp_path) as s:
        with_belivo(s)
        for name in ("tardive", "bricolee"):
            second_app(s.tmp / name)
            s.state.add_app(str(s.tmp / name))
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url)
        page.wait_for_selector(".home-card")
        page.get_by_role("button", name="Tout mettre à jour").click()
        page.wait_for_selector("#apps-report .line")
        lines = page.locator("#apps-report .line")
        assert lines.count() == 4
        got = {lines.nth(i).locator("b").inner_text(): lines.nth(i).get_attribute("data-outcome") for i in range(4)}
        assert got == {"app": "skipped", "belivo": "skipped", "tardive": "updated", "bricolee": "skipped"}
        assert installed == ["tardive"]
        rep = page.locator("#apps-report").inner_text()
        assert "4b1e0a2" in rep and "déjà à jour" in rep and "jamais en bloc" in rep
        for n in ("belivo", "bricolee"):
            assert page.locator("#apps-report .line", has_text=n).get_by_role("button", name="Ouvrir son installation").is_visible()
        assert page.locator("#apps-report .line", has_text="tardive").get_by_role("button").count() == 0
        assert no_real_errors(page) == []


def test_a_run_going_in_another_application(tmp_path, page, per_app_chain):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        b = with_belivo(s)
        s.state.activate(str(b))
        page.on("dialog", lambda d: d.accept())
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#flow-main li.step")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_selector("#busy-banner", state="visible")
        assert "« app »" in page.locator("#busy-banner").inner_text()
        assert page.locator("#tb-run").text_content().startswith("app · /1_lexique f")
        # Not its own: no step « en cours » here, every launch disabled and saying why.
        assert page.locator("#flow-main li.step[data-state='en cours']").count() == 0
        launch = page.locator("#flow-main").get_by_role("button", name="Lancer").first
        assert launch.is_disabled() and "« app »" in launch.get_attribute("title")
        # « Arrêter » acts on it from here.
        page.locator("#tb-stop").click()
        page.wait_for_selector("#busy-banner", state="hidden")
        assert not s.rn.is_running(str(s.app_root))
        assert page.locator("#tb-run").inner_text() == "Au repos"
        assert no_real_errors(page) == []


def test_every_command_keeps_a_way_in(tmp_path, page, per_app_chain):
    """1.9: « Paramètres → Commandes » is gone. A command no step launches is
    at the foot of « Amont » — the audits —, the fusion step carries its two
    halves, « Déploiement → Déployer » the application's /deploie."""
    with FakeServer(tmp_path) as s:
        cmds = s.app_root / ".claude" / "commands"
        for name, desc in (("audit_blocages", "Read a cycle's blocking files and report what recurs across them"),
                           ("audit_conventions", "Read what the conventions gained during a cycle and report what it costs"),
                           ("batir", "Build the skeleton"), ("fusion_applique", "Apply the merge plan")):
            (cmds / f"{name}.md").write_text(f'---\ndescription: {desc}\nargument-hint: "<f>"\n---\nbody\n', encoding="utf-8")
        page.goto(s.url + "#chaine")
        page.get_by_role("tab", name="Amont").click()
        page.wait_for_selector("#audits:not(.hidden)")
        assert page.locator("#settings-commands, #set-commands").count() == 0
        rows = page.locator("#audits .aud")
        got = {rows.nth(i).get_attribute("data-command"): rows.nth(i).locator(".d").inner_text() for i in range(rows.count())}
        assert got == {"audit_blocages": "Read a cycle's blocking files and report what recurs across them",
                       "audit_conventions": "Read what the conventions gained during a cycle and report what it costs",
                       "10_x": "run 10_x"}
        assert page.locator("#audits h3").inner_text() == "Audits"
        # Every command of the application is reachable from a flow, a tab or a button.
        names = page.evaluate("S.commands.map(c => c.name)")
        steps = page.evaluate("[...S.scan.main, ...S.scan.corrections.flatMap(c => c.steps)].filter(s => s.id !== 'test').map(s => s.command)")
        fusion = page.locator("#step-main-fusion .subcmds button").all_inner_texts()
        assert sorted(fusion) == ["/fusion_applique", "/fusion_compare"]
        page.get_by_role("link", name="Déploiement").first.click()
        page.get_by_role("tab", name="Déployer").click()
        page.wait_for_selector("#dp-own")
        assert page.locator("#dp-own").get_by_role("button", name="Lancer /deploie").is_visible()
        reached = set(steps) | set(got) | {f[1:] for f in fusion} | {"deploie"}
        assert set(names) <= reached, set(names) - reached
        assert no_real_errors(page) == []
