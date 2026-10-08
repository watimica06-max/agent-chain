"""1.8 — « Déploiement » in a headless browser (Microsoft Edge through
Playwright): the three tabs, a device renamed, the Wi-Fi form, a deploy's
progress, a crash in the journal, only the declared actions, Paramètres →
Déploiement. adb is a fake (tests/fakeadb.py); no real device is touched and
no chain command runs. Skipped when Playwright or Edge is missing."""
import os
import sys

import pytest

pytest.importorskip("playwright")

import server  # noqa: E402
from deployworld import hyrox_targets, use_fake_adb, write_profile  # noqa: E402
from fakeadb import APP_ID, HYROX_PHONE, threadtime  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_chain import commit, git, init  # noqa: E402
from test_page import browser, no_real_errors, page, stop_run  # noqa: E402,F401
from test_runner import script_until_interrupted  # noqa: E402

PY = f'"{sys.executable}"'


@pytest.fixture
def fa(tmp_path, monkeypatch):
    f = use_fake_adb(tmp_path / "adb", monkeypatch)
    monkeypatch.setattr(server, "PROFILE_PUSH", False)
    yield f
    f.close()


def card(page, name):
    return page.locator(".dp-card", has=page.locator(".nm", has_text=name))


def open_deploy(page, s, tab="Destinations"):
    page.goto(s.url + "#deploy")
    page.wait_for_selector(".dp-card")
    page.get_by_role("tab", name=tab).click()


def test_three_tabs_and_only_declared_actions(tmp_path, page, fa):
    with FakeServer(tmp_path / "s") as s:
        write_profile(s.app_root, hyrox_targets(fa) + [
            {"name": "Site", "type": "commande", "run": f"{PY} -m http.server 0", "keeps_running": True}])
        open_deploy(page, s)
        assert page.locator("#nav-deploy").get_attribute("aria-current") == "page"
        groups = page.locator(".dp-group")
        assert groups.count() == 2
        assert page.locator('.dp-group[data-type="android"] .dp-card').count() == 5
        phone = card(page, "SM-S928B")
        assert "connecté" in phone.inner_text() and "76 %" in phone.inner_text() and "Reçoit : Téléphone" in phone.inner_text()
        assert phone.get_by_role("button", name="Capture d'écran").count() == 1
        un = page.locator('.dp-card[data-dest="android:R3CN70UNAUTH"]')
        assert "non autorisé" in un.inner_text() and "Autoriser le débogage" in un.inner_text()
        # « cet ordinateur »: no screenshot, no mirror — its adapter does not declare them.
        here = page.locator('.dp-card[data-dest="commande:local"]')
        assert here.get_by_role("button", name="Capture d'écran").count() == 0
        assert here.get_by_role("button", name="Afficher l'écran").count() == 0
        assert here.get_by_role("button", name="Journal").count() == 1
        # A screenshot, shown in its card.
        phone.get_by_role("button", name="Capture d'écran").click()
        page.wait_for_selector('.dp-card[data-dest="android:R5CT10AB1234"] .dp-shot img')
        # scrcpy absent here: said, with where to get it.
        phone.get_by_role("button", name="Afficher l'écran").click()
        assert "Genymobile/scrcpy" in card(page, "SM-S928B").locator(".dp-msg").last.inner_text()
        for tab, panel in [("Déployer", "#dp-deployer"), ("Journal", "#dp-journal"), ("Destinations", "#dp-destinations")]:
            page.get_by_role("tab", name=tab).click()
            page.wait_for_selector(f"{panel}:not(.hidden)")
        assert no_real_errors(page) == []


def test_a_device_renamed(tmp_path, page, fa):
    with FakeServer(tmp_path / "s") as s:
        open_deploy(page, s)
        page.once("dialog", lambda d: d.accept("Montre de Clara"))
        card(page, "SM-L705F").get_by_role("button", name="Renommer").click()
        page.wait_for_selector('.dp-card[data-dest="android:RFAX20WATCH9"] .nm:text("Montre de Clara")')
        assert "Renommé" in page.locator('.dp-card[data-dest="android:RFAX20WATCH9"] .dp-msg.ok').inner_text()
        # Kept by the cockpit, in config.json — never in the application.
        assert s.state.deploy_devices()["RFAX20WATCH9"]["name"] == "Montre de Clara"
        assert no_real_errors(page) == []


def test_the_wifi_form(tmp_path, page, fa):
    with FakeServer(tmp_path / "s") as s:
        open_deploy(page, s)
        wifi = page.locator('.dp-panel[data-panel="wifi"]')
        assert "Le port de connexion change" in wifi.inner_text()
        assert "Associer un nouvel appareil" in wifi.inner_text()
        assert "prêts à connecter" in wifi.inner_text()
        pair = wifi.locator('form.dp-form[data-action="pair"]').last
        pair.get_by_label("Adresse IP").fill("192.168.1.42")
        pair.get_by_label("Port").fill("37011")
        pair.get_by_label("Code d'association").fill("654321")
        pair.get_by_role("button", name="Associer").click()
        page.wait_for_selector('.dp-panel[data-panel="wifi"] .dp-msg.warn')
        assert "refusée" in wifi.locator(".dp-msg").inner_text()
        pair = wifi.locator('form.dp-form[data-action="pair"]').last
        # What she typed is still there after the refusal.
        assert pair.get_by_label("Adresse IP").input_value() == "192.168.1.42"
        pair.get_by_label("Code d'association").fill("123456")
        pair.get_by_role("button", name="Associer").click()
        page.wait_for_selector('.dp-panel[data-panel="wifi"] .dp-msg.ok')
        assert "Associé à 192.168.1.42:37011" in wifi.locator(".dp-msg").inner_text()
        # The device mDNS found: one click connects it.
        found = wifi.locator(".dp-item", has_text="192.168.1.42:39999")
        found.get_by_role("button", name="Connecter").click()
        page.wait_for_function("document.querySelector('.dp-panel[data-panel=\"wifi\"] .dp-msg.ok')"
                               ".textContent.includes('Connecté à 192.168.1.42:39999')")
        assert ["connect", "192.168.1.42:39999"] in fa.calls()
        # The refused pairing answered 409: the browser logs it, nothing more.
        assert [e for e in no_real_errors(page) if "status of 409" not in e] == []


def test_a_deploys_progress(tmp_path, page, fa, revealed):
    with FakeServer(tmp_path / "s") as s:
        t = hyrox_targets(fa)
        t[0]["build"] = f'{PY} -c "import time; print(\'BUILD\'); time.sleep(2)"'
        write_profile(s.app_root, t)
        open_deploy(page, s, "Déployer")
        page.wait_for_selector("#dp-targets")
        go = page.get_by_role("button", name="Construire et installer")
        assert go.is_disabled()
        page.locator('.dp-target[data-target="Téléphone"] > label input').check()
        # Checked: its connected devices are chosen. A device adb cannot read
        # is no phone yet: not offered; the watch is not offered to the phone.
        tgt = page.locator('.dp-target[data-target="Téléphone"]')
        assert tgt.locator('input[data-dest="android:R5CT10AB1234"]').is_checked()
        assert tgt.locator('input[data-dest="android:R3CN70UNAUTH"]').count() == 0
        assert tgt.locator('input[data-dest="android:RFAX20WATCH9"]').count() == 0
        assert page.locator('.dp-target[data-target="Montre"] input[data-dest]').is_disabled()
        tgt.locator('input[data-dest="android:EMULATOR37X1X11X0"]').uncheck()
        assert s.state.deploy_choice(str(s.app_root)) == {"Téléphone": ["android:R5CT10AB1234"]}
        go.click()
        page.wait_for_selector('#dp-job[data-status="going"] li.going[data-kind="build"]')
        page.wait_for_selector('#dp-job[data-status="fait"]', timeout=20000)
        job = page.locator("#dp-job")
        assert job.locator("li.done").count() == 3
        assert "Téléphone — Installer sur SM-S928B" in job.inner_text()
        assert "réussi" in job.inner_text() and "deploy-" in job.inner_text()
        # 1.9.1: « Sortie complète » is a link — its folder opens, the file selected.
        out = job.locator("a.loglink")
        out.click()
        page.wait_for_timeout(300)
        assert revealed == [(os.path.normpath(out.inner_text()), True)]
        # A failure shows the end of its output.
        fa.update(lambda st: st.update(install_fails=[HYROX_PHONE]))
        page.get_by_role("button", name="Construire et installer").click()
        page.wait_for_selector('#dp-job[data-status="échec"]', timeout=20000)
        bad = page.locator("#dp-job li.failed")
        assert "INSTALL_FAILED_INSUFFICIENT_STORAGE" in bad.locator("pre").inner_text()
        assert page.locator("#dp-job li.skip").count() == 1
        assert no_real_errors(page) == []


def test_refused_while_a_chain_run_goes_here(tmp_path, page, fa):
    with FakeServer(tmp_path / "s", script=script_until_interrupted) as s:
        write_profile(s.app_root, hyrox_targets(fa))
        s.state.set_deploy_choice(str(s.app_root), {"Téléphone": ["android:R5CT10AB1234"]})
        s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
        open_deploy(page, s, "Déployer")
        page.wait_for_selector("#dp-run-refusal")
        assert "/8_code f" in page.locator("#dp-run-refusal").inner_text()
        assert page.get_by_role("button", name="Construire et installer").is_disabled()
        stop_run(s)
        assert no_real_errors(page) == []


def test_a_crash_in_the_journal(tmp_path, page, fa):
    with FakeServer(tmp_path / "s") as s:
        write_profile(s.app_root, hyrox_targets(fa))
        open_deploy(page, s)
        card(page, "SM-S928B").get_by_role("button", name="Journal").click()
        page.wait_for_selector("#dp-journal:not(.hidden) .dp-log .l.marker")
        assert page.locator("#dp-j-dest").input_value() == "android|android:R5CT10AB1234"
        assert "en direct" in page.locator("#dp-j-live").inner_text()
        fa.logcat(HYROX_PHONE, threadtime(4321, "I", "hyrox", "tour 1"),
                  threadtime(4321, "E", "AndroidRuntime", "FATAL EXCEPTION: main"),
                  threadtime(4321, "E", "AndroidRuntime", f"Process: {APP_ID}, PID: 4321"),
                  threadtime(4321, "E", "AndroidRuntime", "java.lang.IllegalStateException: boum"),
                  threadtime(4321, "I", "hyrox", "après"))
        page.wait_for_selector(".dp-crash")
        crash = page.locator(".dp-crash")
        assert "FATAL EXCEPTION: main" in crash.inner_text()
        assert page.locator("#dp-crash-n").inner_text() == "1"
        page.wait_for_function("document.querySelectorAll('#dp-j-log .l.crash').length === 3")
        crash.get_by_role("button", name="Copier le crash").click()
        copied = page.wait_for_function("window.cockpitLastCopy").json_value()
        assert copied.startswith("Crash sur « SM-S928B » (cible « Téléphone »)")
        assert "java.lang.IllegalStateException: boum" in copied and "après" not in copied
        # The filter, then « Effacer ».
        page.locator("#dp-j-filter").fill("tour 1")
        assert page.locator("#dp-j-log .l").count() == 1
        page.locator("#dp-j-filter").fill("")
        page.get_by_role("button", name="Effacer").click()
        assert page.locator(".dp-crash").count() == 0
        # « Enregistrer »: the whole log, in the logs folder.
        page.get_by_role("button", name="Enregistrer").click()
        page.wait_for_function("document.getElementById('dp-j-note').textContent.startsWith('Enregistré')")
        assert no_real_errors(page) == []


def test_parametres_deploiement(tmp_path, page, fa):
    # 1.9: « Déploiement → Profil », Paramètres → Déploiement in 1.8 — the same.
    with FakeServer(tmp_path / "s") as s:
        init(s.app_root)
        commit(s.app_root, "first")
        page.goto(s.url + "#deploy")
        page.get_by_role("tab", name="Profil").click()
        page.wait_for_selector("#dp-profil:not(.hidden) #dp-set-empty")
        page.locator("#dps-new-type").select_option("commande")
        page.get_by_role("button", name="Ajouter une cible").click()
        tgt = page.locator(".dp-tgt").first
        # The fields shown are the adapter's.
        assert tgt.get_by_label("Commande de lancement").count() == 1
        assert tgt.get_by_label("Commande d'installation").count() == 0
        page.get_by_role("button", name="Enregistrer le profil").click()
        page.wait_for_selector("#dps-msg.warn")
        assert "obligatoire" in tgt.inner_text()
        tgt = page.locator(".dp-tgt").first
        tgt.get_by_label("Nom").fill("Site")
        tgt.get_by_label("Commande de lancement").fill("python -m http.server 8000")
        tgt.get_by_label("Adresse à ouvrir").fill("http://127.0.0.1:8000/")
        page.locator("#dps-new-type").select_option("android")
        page.get_by_role("button", name="Ajouter une cible").click()
        tgt2 = page.locator(".dp-tgt").nth(1)
        assert tgt2.get_by_label("Commande d'installation").count() == 1
        tgt2.get_by_role("button", name="Retirer").click()
        page.get_by_role("button", name="Enregistrer le profil").click()
        page.wait_for_selector("#dps-msg.ok")
        assert "deploy: profil" in page.locator("#dps-msg").inner_text()
        assert git(s.app_root, "log", "-1", "--format=%s").strip() == "deploy: profil"
        data = (s.app_root / ".claude" / "deploy.json").read_text(encoding="utf-8")
        assert '"url": "http://127.0.0.1:8000/"' in data and '"keeps_running": false' in data
        # The first save refused (400, the fields said): the browser logs it, nothing more.
        assert [e for e in no_real_errors(page) if "status of 400" not in e] == []


# Counts the reads of /api/deploy the page has finished with — its `api()`
# returns once the body is read, and what follows runs before the next task.
COUNT_DEPLOY_READS = """
window.__deployReads = 0;
const realFetch = window.fetch;
window.fetch = (input, init) => realFetch(input, init).then((r) => {
  if (String(input) === "/api/deploy" && !(init && init.method)) {
    const json = r.json.bind(r);
    r.json = () => json().finally(() => { window.__deployReads += 1; });
  }
  return r;
});
"""


def test_a_target_added_survives_a_late_read_of_the_profile(tmp_path, page, fa):
    """1.12.2: « Profil » clicked while « Déploiement » is still being
    entered — two reads of the profile cross: the tab's, and the entry's own
    once its destinations are read. Forced: the tab's comes back first, a
    target is added, then the entry's comes back. The target stays."""
    held, holding = [], {"on": True}

    def hold(route):
        if holding["on"] and route.request.method == "GET":
            held.append(route)
        else:
            route.continue_()

    def until(n):
        for _ in range(200):
            if len(held) >= n:
                return
            page.wait_for_timeout(50)
        assert len(held) >= n, held
    with FakeServer(tmp_path / "s") as s:
        init(s.app_root)
        commit(s.app_root, "first")
        page.add_init_script(COUNT_DEPLOY_READS)
        page.route("**/api/deploy", hold)
        page.goto(s.url + "#deploy")
        until(1)                                       # the entry's read
        page.get_by_role("tab", name="Profil").click()
        until(2)                                       # the tab's
        held[0].continue_()
        until(3)                                       # the entry's second, for « Profil »
        held[1].continue_()
        page.wait_for_selector("#dp-profil:not(.hidden) #dp-set-empty")
        page.locator("#dps-new-type").select_option("commande")
        page.get_by_role("button", name="Ajouter une cible").click()
        assert page.locator(".dp-tgt").count() == 1
        holding["on"] = False
        held[2].continue_()
        page.wait_for_function("window.__deployReads === 3")
        assert page.locator(".dp-tgt").count() == 1
        assert page.locator(".dp-tgt").first.get_by_label("Commande de lancement").count() == 1
        assert no_real_errors(page) == []


def test_notifications_a_deploy_ends_and_a_crash_comes(tmp_path, browser, fa):
    # The tab behind: a deploy's end and a crash each make a notification.
    from test_page_code import FAKE_NOTIFICATION
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    ctx.add_init_script(FAKE_NOTIFICATION + 'localStorage.setItem("cockpit-notifications", JSON.stringify({deploiement: true, crash: true}));'
                        + "Notification.permission = 'granted';")
    pg = ctx.new_page()
    try:
        with FakeServer(tmp_path / "s") as s:
            write_profile(s.app_root, hyrox_targets(fa))
            s.state.set_deploy_choice(str(s.app_root), {"Téléphone": ["android:R5CT10AB1234"]})
            pg.goto(s.url + "#deploy")
            pg.get_by_role("tab", name="Journal").click()
            pg.wait_for_selector("#dp-j-log .l.marker")
            pg.evaluate("window.__vis = 'hidden'")
            fa.logcat(HYROX_PHONE, threadtime(4321, "E", "AndroidRuntime", "FATAL EXCEPTION: main"))
            pg.wait_for_function("window.__notes.length === 1")
            assert pg.evaluate("window.__notes[0].title").endswith("crash sur SM-S928B")
            pg.evaluate("window.__vis = 'visible'")
            pg.get_by_role("tab", name="Déployer").click()
            pg.wait_for_selector("#dp-targets")
            pg.get_by_role("button", name="Construire et installer").click()
            pg.evaluate("window.__vis = 'hidden'")
            pg.wait_for_function("window.__notes.length === 2", timeout=20000)
            assert pg.evaluate("window.__notes[1].title").endswith("déploiement réussi")
            assert "toutes réussies" in pg.evaluate("window.__notes[1].body")
    finally:
        ctx.close()
