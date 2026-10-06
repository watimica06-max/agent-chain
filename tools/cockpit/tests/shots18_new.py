"""1.8 — the new screens, for shots18.py's « apres »: « Déploiement » over a
fake adb (Hyrox's devices), a `commande` target served for real by
`python -m http.server` on a free port, Paramètres → Déploiement. No real
device is touched; no chain command runs."""
import socket
import sys

import diagnostic
import server
from deployworld import hyrox_targets, use_fake_adb, write_profile
from fakeadb import APP_ID, HYROX_PHONE, threadtime
from test_mode_diagnostic import ALL_GOOD, fake_exec
from test_runner import script_until_interrupted

EMULATOR = r"C:\Users\vous\AppData\Local\Android\Sdk\emulator\emulator.exe"
STATE = {}


def snap(page, out, name):
    page.wait_for_timeout(600)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def prepare(s, t):
    """Before the shared screens: the diagnostic with the optional tools —
    the emulator found, scrcpy not —, the fake adb, the profile."""
    def ex(argv, cwd, timeout):
        if argv[0] == EMULATOR:
            return 0, "INFO    | Android emulator version 37.1.11.0 (build_id 15917651)"
        return fake_exec(ALL_GOOD)(argv, cwd, timeout)
    diagnostic.FIND = lambda tool: [EMULATOR] if tool == "emulator" else None
    s.state.set_diagnostic(diagnostic.run_diagnostic(str(s.app_root), ex, env={}), app=str(s.app_root))
    fa = use_fake_adb(t / "adb", emulator=True)
    port = free_port()
    (s.app_root / "www").mkdir()
    (s.app_root / "www" / "index.html").write_text("<h1>Site</h1>", encoding="utf-8")
    targets = hyrox_targets(fa)
    for x in targets:
        x["build"] = x["build"].replace("print(", "import time; time.sleep(1.5); print(")
    targets.append({"name": "Site", "type": "commande", "build": "",
                    "run": f'"{sys.executable}" -m http.server {port} --bind 127.0.0.1 --directory www',
                    "keeps_running": True, "url": f"http://127.0.0.1:{port}/"})
    write_profile(s.app_root, targets)
    STATE.update(fa=fa, port=port)


def main(page, out, s, t):
    fa = STATE["fa"]
    s.state.set_deploy_device("RFAX20WATCH9", name="Montre de Clara")
    s.state.set_deploy_device("R5CT10AB1234", name="Téléphone de Clara")
    # A device seen before, not there now.
    s.state.set_deploy_device("R58N30OLDTAB", name="Ancien téléphone", model="SM-A546B", form="phone",
                              emulator=False, last_address="192.168.1.57:40125")
    page.goto(s.url + "#deploy")
    page.wait_for_selector(".dp-card")
    page.get_by_role("tab", name="Destinations").click()
    page.wait_for_selector(".dp-card")
    card = page.locator('.dp-card[data-dest="android:R5CT10AB1234"]')
    card.get_by_role("button", name="Capture d'écran").click()
    page.wait_for_selector('.dp-card[data-dest="android:R5CT10AB1234"] .dp-shot img')
    snap(page, out, "apres-03-deploiement-destinations")
    page.locator('.dp-card[data-dest="android:R3CN70UNAUTH"]').scroll_into_view_if_needed()
    snap(page, out, "apres-04-destinations-non-autorise-deconnecte")
    wifi = page.locator('.dp-panel[data-panel="wifi"]')
    pair = wifi.locator('form.dp-form[data-action="pair"]').last
    pair.get_by_label("Adresse IP").fill("192.168.1.42")
    pair.get_by_label("Port").fill("37011")
    pair.get_by_label("Code d'association").fill("123456")
    pair.get_by_role("button", name="Associer").click()
    page.wait_for_selector('.dp-panel[data-panel="wifi"] .dp-msg.ok')
    wifi.scroll_into_view_if_needed()
    snap(page, out, "apres-05-wifi-associer-et-emulateurs")
    page.get_by_role("tab", name="Déployer").click()
    page.wait_for_selector("#dp-targets")
    for name in ("Téléphone", "Montre"):
        page.locator(f'.dp-target[data-target="{name}"] > label input').check()
    page.locator('.dp-target[data-target="Téléphone"] input[data-dest="android:EMULATOR37X1X11X0"]').uncheck()
    page.locator('.dp-target[data-target="Site"] > label input').check()
    snap(page, out, "apres-06-deployer-le-choix")
    page.get_by_role("button", name="Construire et installer").click()
    page.wait_for_selector('#dp-job[data-status="going"] li.going')
    page.locator("#dp-job").scroll_into_view_if_needed()
    snap(page, out, "apres-07-deploiement-en-cours")
    page.wait_for_selector('#dp-job[data-status="fait"]', timeout=30000)
    page.locator("#dp-job").scroll_into_view_if_needed()
    snap(page, out, "apres-08-deploiement-reussi")
    fa.update(lambda st: st.update(install_fails=["192.168.1.42:41235"]))
    page.get_by_role("button", name="Construire et installer").click()
    page.wait_for_selector('#dp-job[data-status="échec"]', timeout=30000)
    page.locator("#dp-job li.failed").scroll_into_view_if_needed()
    snap(page, out, "apres-09-deploiement-une-installation-en-echec")
    page.get_by_role("tab", name="Destinations").click()
    page.locator('.dp-card[data-dest="commande:local"]').scroll_into_view_if_needed()
    snap(page, out, "apres-10-cet-ordinateur-site-en-marche")
    page.get_by_role("tab", name="Journal").click()
    page.locator("#dp-j-dest").select_option("android|android:R5CT10AB1234")
    page.wait_for_selector("#dp-j-log .l.marker")
    fa.logcat(HYROX_PHONE,
              threadtime(4321, "I", "HyroxTracker", "Course démarrée : 8 stations", "10-06 18:42:10.114"),
              threadtime(4321, "D", "HyroxTracker", "Station 1 — SkiErg : 1000 m", "10-06 18:42:11.502"),
              threadtime(4321, "D", "WearSync", "Envoi à la montre : 312 octets", "10-06 18:42:11.630"),
              threadtime(4321, "E", "AndroidRuntime", "FATAL EXCEPTION: main", "10-06 18:42:12.007"),
              threadtime(4321, "E", "AndroidRuntime", f"Process: {APP_ID}, PID: 4321", "10-06 18:42:12.007"),
              threadtime(4321, "E", "AndroidRuntime", "java.lang.IllegalStateException: Station 2 sans chrono", "10-06 18:42:12.007"),
              threadtime(4321, "E", "AndroidRuntime", "\tat com.mgilli.hyroxtracker.race.RaceTimer.lap(RaceTimer.kt:88)", "10-06 18:42:12.007"),
              threadtime(4321, "E", "AndroidRuntime", "\tat com.mgilli.hyroxtracker.ui.RaceScreen.onStation(RaceScreen.kt:141)", "10-06 18:42:12.007"),
              threadtime(1000, "I", "ActivityManager", f"Start proc 5120:{APP_ID}/u0a321 for top-activity", "10-06 18:42:14.220"),
              threadtime(5120, "I", "HyroxTracker", "Reprise de la course : station 2", "10-06 18:42:14.871"))
    page.wait_for_selector(".dp-crash")
    page.wait_for_function("document.querySelectorAll('#dp-j-log .l').length >= 9")
    snap(page, out, "apres-11-journal-un-crash")
    page.get_by_role("link", name="Paramètres").click()
    page.wait_for_selector(".dp-tgt")
    page.locator("#sec-deploy").scroll_into_view_if_needed()
    snap(page, out, "apres-12-parametres-deploiement")
    page.locator('.dp-tgt[data-i="2"]').scroll_into_view_if_needed()
    snap(page, out, "apres-13-parametres-deploiement-commande")
    # A chain run going in this application: the deploy refused, said.
    s.script = script_until_interrupted
    s.call(s.rn.start(str(s.app_root), "f", "f", "8_code", "f"))
    page.goto(s.url + "#deploy")
    page.get_by_role("tab", name="Déployer").click()
    page.wait_for_selector("#dp-run-refusal")
    snap(page, out, "apres-14-refuse-pendant-un-run")
    s.call(s.rn.stop_now(str(s.app_root)))
    s.app[server.DEPLOY_KEY].stop_all()
    fa.close()
