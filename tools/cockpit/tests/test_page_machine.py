"""1.16 — « État de l'ordinateur » on the page, in a headless browser
(Microsoft Edge through Playwright): the screen in Paramètres, a block and
its badge on the home screen and in the top bar, a repair (« Se connecter à
Claude », its address and its code), the install question and « Pas à pas »'s
cards, the phone's summary (« Réparer sur l'ordinateur »), a run that ended
on authentication_failed, and §0's install never green, unsent commits never
hidden. The computer is the fake one (machinefakes.py); GitHub a bare
repository in a temporary folder; no chain command runs.

With COCKPIT_SHOTS=<folder>, each step's screenshot is written there."""
import json
import os
import sys

import pytest

pytest.importorskip("playwright")

import installs  # noqa: E402
import machine  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from syncworld import app_world, change, offline  # noqa: E402
from test_defects_116 import not_signed_in  # noqa: E402
from test_installs import FAKE_LOGIN, ToolClient  # noqa: E402
from test_page import page  # noqa: E402,F401


def shot(page, name, full=False):
    d = os.environ.get("COCKPIT_SHOTS")
    if d:
        os.makedirs(d, exist_ok=True)
        page.screenshot(path=os.path.join(d, f"{name}.png"), full_page=full)


def errors(page):
    return [e for e in page.js_errors if "status of 409" not in e and "Failed to fetch" not in e and "net::ERR" not in e]


def post(page, s, path, data=None):
    r = page.request.post(s.url + path.lstrip("/"), data=json.dumps(data or {}), headers={"Content-Type": "application/json"})
    return r.status, r.json()


def to_machine(page, s):
    page.goto(s.url + "#settings")
    page.wait_for_selector("#machine-list .mc-group")
    page.wait_for_function("!machineChecking")
    page.evaluate("document.getElementById('sec-machine').scrollIntoView({block: 'start'})")


def test_the_screen_every_item_its_rule_and_its_age(tmp_path, page, fake_machine, monkeypatch):
    fake_machine.identity = "guessed"
    with FakeServer(tmp_path) as s:
        to_machine(page, s)
        heads = page.locator("#machine-list .mc-group h3").all_inner_texts()
        assert heads[:4] == ["Le cockpit", "Claude Code", "git et GitHub", "Android et builds"]
        line = page.locator('#machine-list li[data-id="claude_login"]')
        assert line.get_attribute("data-status") == "ok"
        assert "Règle : bloque : chaque lancement, « Installer avec Claude »" in line.inner_text()
        assert "vérifié à l'instant" in line.inner_text()
        ident = page.locator('#machine-list li[data-id="git_identity"]')
        assert ident.get_attribute("data-status") == "à voir" and "git la devine" in ident.inner_text()
        # The badge: in the top bar on every screen.
        page.wait_for_selector("#tb-machine:not(.hidden)")
        assert page.locator("#tb-machine").inner_text().startswith("Ordinateur : à voir")
        assert page.locator("#set-install-mode").input_value() == "demander"
        shot(page, "1-parametres-etat-de-l-ordinateur", full=True)
        # The manual entry, folded under « Utiliser mon compte GitHub » (1.21.1) — git's
        # global configuration a file of the test.
        monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "gitconfig"))
        assert ident.locator("button.mc-repair").inner_text() == "Utiliser mon compte GitHub"
        assert not ident.locator(".id-name").is_visible()
        ident.get_by_text("Saisir à la main").click()
        ident.locator(".id-name").fill("Product Owner")
        ident.locator(".id-email").fill("po@example.com")
        shot(page, "2-regler-identite")
        fake_machine.identity = "other"
        fake_machine.accounts = []
        page.locator("#machine-list").get_by_role("button", name="Enregistrer").click()
        page.wait_for_selector('#machine-list li[data-id="git_identity"][data-status="ok"]')
        page.wait_for_selector("#tb-machine.hidden", state="attached")
        assert "name = Product Owner" in (tmp_path / "gitconfig").read_text(encoding="utf-8")
        assert errors(page) == [], page.js_errors


def test_use_my_github_account_from_the_home_screen(tmp_path, page, fake_machine, monkeypatch):
    """1.21.1 — from the home screen, where 1.16's « Régler » showed nothing:
    the account, one click, what was set; several accounts, one button each;
    none, GitHub's sign-in. git's global configuration a file of the test."""
    cfg = tmp_path / "gitconfig"
    cfg.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(cfg))
    fake_machine.identity = "guessed"
    with FakeServer(tmp_path, opened=False) as s:
        post(page, s, "/api/machine/check")
        page.goto(s.url)
        line = page.locator('#machine-home li[data-id="git_identity"]')
        line.wait_for()
        assert "« Utiliser mon compte GitHub » la règle sur le compte quelqu-un" in line.inner_text()
        assert not line.locator(".id-name").is_visible()
        shot(page, "1-accueil-identite-devinee")
        # GitHub not answering: said on the line, nothing set.
        fake_machine.github_api = "offline"
        line.get_by_role("button", name="Utiliser mon compte GitHub").click()
        page.wait_for_selector('#machine-home li[data-id="git_identity"] .id-msg-github')
        assert "GitHub ne répond pas" in line.inner_text() and cfg.read_text(encoding="utf-8") == ""
        fake_machine.github_api = "ok"
        fake_machine.identity = "set"            # what git reads once set: the rule's own test is the server's
        line.get_by_role("button", name="Utiliser mon compte GitHub").click()
        page.wait_for_selector('#machine-home li[data-id="git_identity"][data-status="ok"] .id-set')
        text = line.inner_text()
        assert "user.name = quelqu-un" in text and "user.email = 4242+quelqu-un@users.noreply.github.com" in text
        assert "name = quelqu-un" in cfg.read_text(encoding="utf-8")
        assert line.locator(".id-msg-github").count() == 0
        shot(page, "2-accueil-identite-reglee")
        # Several accounts: one button each — never one guessed.
        fake_machine.identity, fake_machine.accounts = "guessed", ["quelqu-un", "autre-compte"]
        post(page, s, "/api/machine/check")
        page.evaluate("identitySet = null; loadMachine()")
        page.wait_for_selector('#machine-home li[data-id="git_identity"] button[data-login="autre-compte"]')
        assert line.locator("button.mc-repair").all_inner_texts() == ["Utiliser quelqu-un", "Utiliser autre-compte"]
        shot(page, "3-accueil-deux-comptes")
        # None signed in: GitHub's sign-in, and the manual entry still there, folded.
        fake_machine.accounts = []
        post(page, s, "/api/machine/check")
        page.evaluate("loadMachine()")
        page.wait_for_selector('#machine-home li[data-id="git_identity"] button[data-repair="github_login"]')
        assert "aucun compte GitHub connecté sur cet ordinateur" in line.inner_text()
        line.get_by_text("Saisir à la main").click()
        assert line.locator(".id-name").is_visible()
        shot(page, "4-accueil-aucun-compte")
        assert errors(page) == [], page.js_errors


def test_a_block_its_badge_and_the_claude_login(tmp_path, page, fake_machine, monkeypatch):
    p = tmp_path / "login.py"
    p.write_text(FAKE_LOGIN, encoding="utf-8")
    monkeypatch.setattr(installs, "CLAUDE_LOGIN", [sys.executable, str(p)])
    fake_machine.logged_in = False
    with FakeServer(tmp_path, opened=False) as s:
        s.state.add_app(str(s.app_root))
        post(page, s, "/api/machine/check")
        page.goto(s.url)
        # The home screen: the badge, and what blocks with its repair.
        page.wait_for_selector("#machine-badge:not(.hidden)")
        assert page.locator("#machine-badge").inner_text().startswith("Ordinateur : bloqué")
        home = page.locator("#machine-home")
        assert "Claude Code n'est pas connecté sur cet ordinateur" in home.inner_text()
        shot(page, "3-accueil-bloque")
        # A launch is refused, said with what to repair.
        s.state.open_pair(str(s.app_root), "f")
        code, r = post(page, s, "/api/run", {"command": "1_lexique", "args": "f"})
        assert code == 409 and r["machine"][0]["id"] == "claude_login"
        # « Se connecter à Claude »: the address of the page, then the code it shows.
        home.locator('button[data-repair="claude_login"]').click()
        page.wait_for_selector("#machine-session-home .mc-signin a")
        assert page.locator("#machine-session-home .mc-signin a").get_attribute("href").startswith("https://claude.com/cai/oauth")
        shot(page, "4-se-connecter-a-claude")
        fake_machine.logged_in = True
        page.locator("#machine-session-home .signin-code").fill("bon#etat")
        # A step arriving meanwhile draws the panel again: what she typed stays.
        page.evaluate("renderMachineSession()")
        assert page.locator("#machine-session-home .signin-code").input_value() == "bon#etat"
        page.locator("#machine-session-home").get_by_role("button", name="Envoyer le code").click()
        page.wait_for_selector('#machine-session-home .mc-session.done', timeout=20000)
        assert "connecté" in page.locator("#machine-session-home").inner_text()
        page.wait_for_selector("#machine-badge.hidden", state="attached", timeout=20000)
        shot(page, "5-connecte")
        code, r = post(page, s, "/api/run", {"command": "1_lexique", "args": "f"})
        assert code == 200, r
        assert errors(page) == [], page.js_errors


def test_the_install_question_then_pas_a_pas_and_a_refused_licence(tmp_path, page, fake_machine, monkeypatch):
    def make(workdir, can_use_tool, licence):
        return ToolClient(can_use_tool, licence, installs.ANDROID_SDK)
    monkeypatch.setattr(installs, "CLIENT_FACTORY", make)
    fake_machine.adb = None
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "gradlew.bat").write_text("@echo off")          # an Android application
    with FakeServer(tmp_path) as s:
        s.state.add_app(str(s.app_root))
        to_machine(page, s)
        adb = page.locator('#machine-list li[data-id="adb"]')
        assert adb.get_attribute("data-status") == "à voir"
        assert "bloque « Bâtir », l'écran Déploiement" in adb.inner_text()
        adb.locator("button.mc-repair").click()
        # One question first: what, the licences « Rapide » accepts, what no mode skips.
        page.wait_for_selector("#install-ask:not(.hidden) #ia-title")
        ask = page.locator("#install-ask").inner_text()
        assert "Ce qui sera installé : adb (Android SDK Platform-Tools)" in ask
        assert f"Licences acceptées : {installs.ANDROID_SDK}" in ask
        assert "la fenêtre d'administrateur de Windows (UAC)" in ask and "connexion dans le navigateur" in ask
        shot(page, "6-question-rapide-ou-pas-a-pas")
        page.locator("#ia-pas").click()
        page.wait_for_selector('#machine-session .mc-card.step')
        assert "winget show" in page.locator("#machine-session .mc-card").inner_text()
        shot(page, "7-pas-a-pas-etape")
        page.locator("#machine-session .mc-accept").click()
        page.wait_for_selector('#machine-session .mc-card.licence')
        assert "LICENSE AGREEMENT" in page.locator("#machine-session .mc-card pre").inner_text()
        shot(page, "8-pas-a-pas-licence")
        page.locator("#machine-session .mc-refuse").click()
        page.wait_for_selector('#machine-session .mc-session.failed', timeout=20000)
        rep = page.locator("#machine-session .mc-report").inner_text()
        assert "refusé" in rep and "Licence refusée" in rep and "Licences acceptées : aucune" in rep
        shot(page, "9-licence-refusee")
        # The default in Paramètres: « Rapide » — no question, the licences listed after.
        page.locator("#set-install-mode").select_option("rapide")
        page.wait_for_function("M && M.install_mode === 'rapide'")
        page.locator('#machine-list li[data-id="adb"] button.mc-repair').click()
        page.wait_for_function("t => (document.querySelector('#machine-session .mc-report') || {}).innerText"
                               "?.includes('Licences acceptées : ' + t)", arg=installs.ANDROID_SDK, timeout=20000)
        assert page.locator("#install-ask").is_hidden()
        rep = page.locator("#machine-session .mc-report").inner_text()
        assert f"Licences acceptées : {installs.ANDROID_SDK}" in rep
        assert s.state.install_mode == "rapide"
        assert errors(page) == [], page.js_errors


def test_the_phone_shows_the_summary_and_repairs_on_the_computer(tmp_path, page, fake_machine):
    fake_machine.github = "credentials"
    with FakeServer(tmp_path, opened=False) as s:
        s.state.add_app(str(s.app_root))
        post(page, s, "/api/machine/check")
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(s.url)
        page.wait_for_selector("#machine-badge:not(.hidden)")
        assert page.locator("#machine-badge").inner_text().startswith("Ordinateur : bloqué")
        assert "Réparer sur l'ordinateur" in page.locator("#machine-badge").inner_text()
        home = page.locator("#machine-home")
        assert home.locator("button.mc-repair").count() == 0
        assert "Réparer sur l'ordinateur" in home.locator('li[data-id="github"]').inner_text()
        shot(page, "10-telephone-resume")
        assert errors(page) == [], page.js_errors


def test_a_run_refused_for_authentication_offers_se_connecter(tmp_path, page):
    with FakeServer(tmp_path, script=not_signed_in) as s:
        page.goto(s.url + "#dashboard")
        page.wait_for_function("S.open")
        s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
        page.wait_for_function("S.run && S.run.status === 'ended'", timeout=20000)
        page.goto(s.url + "#chaine")
        page.wait_for_selector("#run-end .run-auth", timeout=20000)
        assert "erreur : Claude Code n'est pas connecté sur cet ordinateur" in page.locator("#run-status").inner_text()
        assert "success" not in page.locator("#run-status").inner_text()
        assert page.locator("#run-end .run-auth button").inner_text() == "Se connecter"
        page.locator("#run-end .run-auth").scroll_into_view_if_needed()
        shot(page, "11-fin-de-run-non-connecte")
        assert errors(page) == [], page.js_errors


def test_an_install_whose_push_failed_is_never_green(tmp_path, page):
    res = {"commit": "abc1234", "date": "2026-10-10", "app_commit": "def5678", "message": "chain: abc1234 2026-10-10",
           "pushed": False, "push_error": "GitHub a refusé le push", "written": [], "removed": []}
    with FakeServer(tmp_path, opened=False) as s:
        s.state.add_app(str(s.app_root))
        page.route("**/api/chain/install", lambda route: route.fulfill(
            status=200, content_type="application/json", body=json.dumps({"ok": True, "result": res})))
        page.goto(s.url)
        page.wait_for_selector(".home-card")
        page.evaluate("f => rowInstall(f)", str(s.app_root))
        page.wait_for_selector("#apps-msg:not(.hidden)")
        cls = page.locator("#apps-msg").get_attribute("class")
        assert "err" in cls and "ok" not in cls.split()
        assert "non poussé : GitHub a refusé le push" in page.locator("#apps-msg").inner_text()
        # « Tout mettre à jour »'s report: the line of an install not pushed.
        page.evaluate("""f => { A.report = {at: "2026-10-10T12:00:00", lines: [{name: "app", folder: f,
            outcome: "mise à jour", unpushed: true, text: "chaîne abc1234 — commit def5678, non poussé : GitHub a refusé le push"}]};
            renderReport(); }""", str(s.app_root))
        page.wait_for_selector('#apps-report .line[data-outcome="failed"]')
        assert page.locator("#apps-report .oc").inner_text() == "mise à jour, non poussée"
        shot(page, "12-installation-non-poussee")
        assert errors(page) == [], page.js_errors


def test_unsent_commits_stay_said_while_github_is_unreachable(tmp_path, page):
    _, a, _ = app_world(tmp_path, "carnet")
    change(a, "README.md", "ici\n", "un commit d'ici")
    offline(a)
    with FakeServer(tmp_path / "srv", opened=False) as s:
        s.state.add_app(str(a))
        s.state.rename_app(str(a), "Carnet")
        page.goto(s.url)
        page.wait_for_selector('.home-card[data-name="Carnet"] .cst.unsent', timeout=30000)
        card = page.locator('.home-card[data-name="Carnet"]')
        assert card.locator(".cst.unsent").inner_text() == "GitHub injoignable · 1 non envoyé"
        assert "1 commit de cet ordinateur pas encore sur GitHub" in card.inner_text()
        shot(page, "13-injoignable-non-envoye")
        assert errors(page) == [], page.js_errors
