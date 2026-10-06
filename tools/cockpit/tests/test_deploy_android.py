"""1.8 — the `android` adapter over a fake adb (tests/fakeadb.py): a phone
over USB, a watch over Wi-Fi, an emulator, an unauthorized and an offline
device. Its destinations, the kind filter, a deploy — build once, install on
each device, launch —, a build failure, an install failure on one device of
two, Wi-Fi pairing and connecting, a crash marked in the log, the process
restarting. No real device is touched."""
import time

import pytest

import deploy
from adapters import android
from deployworld import hyrox_targets, say, use_fake_adb, write_profile
from fakeadb import APP_ID, HYROX_PHONE, HYROX_WATCH, threadtime
from state import State

PHONE, WATCH, EMU = "android:R5CT10AB1234", "android:RFAX20WATCH9", "android:EMULATOR37X1X11X0"


@pytest.fixture
def world(tmp_path, monkeypatch):
    fa = use_fake_adb(tmp_path / "adb", monkeypatch, emulator=True)
    app = tmp_path / "app"
    app.mkdir()
    write_profile(app, hyrox_targets(fa))
    dep = deploy.Deployer(State(str(tmp_path / "config.json")), str(tmp_path / "logs"))
    events = []
    dep.emit = lambda kind, data: events.append((kind, data))
    yield fa, str(app), dep, events
    dep.stop_all()
    fa.close()


def group(dep, app, typ="android"):
    return next(g for g in dep.destinations(app)["groups"] if g["type"] == typ)


def by_id(g):
    return {d["id"]: d for d in g["destinations"]}


def wait(pred, timeout=10.0):
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout:
        if pred():
            return True
        time.sleep(0.05)
    return False


def test_destinations_read_from_adb(world):
    fa, app, dep, _ = world
    d = by_id(group(dep, app))
    assert list(d) == [PHONE, WATCH, EMU, "android:R3CN70UNAUTH", "android:0123456789OFF"]
    facts = dict(d[PHONE]["facts"])
    assert (d[PHONE]["kind"], facts["Liaison"], facts["Android"], facts["Batterie"]) == \
        ("téléphone", "USB", "15 (API 35)", "76 %")
    assert d[PHONE]["name"] == "SM-S928B" and d[PHONE]["state"] == "device" and d[PHONE]["connected"]
    w = dict(d[WATCH]["facts"])
    assert d[WATCH]["kind"] == "montre" and w["Liaison"] == "Wi-Fi" and w["Série adb"] == HYROX_WATCH
    assert d[EMU]["kind"] == "émulateur" and dict(d[EMU]["facts"])["Liaison"] == "émulateur"
    un, off = d["android:R3CN70UNAUTH"], d["android:0123456789OFF"]
    assert un["state"] == "unauthorized" and not un["connected"] and "Autoriser le débogage" in un["note"]
    assert off["state"] == "offline" and "rebranchez" in off["note"]
    # What a connected device declares; scrcpy absent here: said on its button.
    acts = {a["id"]: a for a in d[PHONE]["actions"]}
    assert {"journal", "screenshot", "mirror", "launch", "stop", "rename"} <= set(acts)
    assert acts["screenshot"]["kind"] == "image" and acts["mirror"]["args"] == {"missing": True}
    assert "github.com/Genymobile/scrcpy" in acts["mirror"]["title"]
    assert [a["id"] for a in un["actions"]] == ["rename"]


def test_the_kind_filters_the_devices_offered(world):
    fa, app, dep, _ = world
    g = group(dep, app)
    d = by_id(g)
    # A phone target: the phone and the phone emulator; a watch target: the watch.
    assert d[PHONE]["targets"] == ["Téléphone"] and d[EMU]["targets"] == ["Téléphone"]
    assert d[WATCH]["targets"] == ["Montre"]
    a = dep.adapters["android"]
    assert a.accepts({"kind": "any"}, d[WATCH]) and a.accepts({"kind": "any"}, d[PHONE])


def test_a_name_is_kept_by_the_hardware_serial_and_a_lost_device_stays_greyed(world):
    fa, app, dep, _ = world
    dep.act(app, "android", "rename", WATCH, {"name": "Montre de Clara"})
    assert by_id(group(dep, app))[WATCH]["name"] == "Montre de Clara"
    # Wireless debugging restarts: the watch is gone, then back on another port.
    fa.update(lambda st: st.update(devices=[x for x in st["devices"] if x["serial"] != HYROX_WATCH]))
    gone = by_id(group(dep, app))[WATCH]
    assert gone["state"] == "déconnecté" and not gone["connected"] and gone["name"] == "Montre de Clara"
    assert dict(gone["facts"])["Dernière adresse"] == HYROX_WATCH
    assert [a["id"] for a in gone["actions"]][:1] == ["reconnect"]
    # « Reconnecter » tries the last address: the port changed, refused, said.
    with pytest.raises(android.ActionError) as e:
        dep.act(app, "android", "reconnect", WATCH, {})
    assert "le port change" in str(e.value)
    # « Connecter » on the new port: the same device, its name kept.
    assert "Connecté" in dep.act(app, "android", "connect", "", {"ip": "192.168.1.42", "port": "39999"})["message"]
    back = by_id(group(dep, app))[WATCH]
    assert back["connected"] and back["name"] == "Montre de Clara"
    assert dict(back["facts"])["Série adb"] == "192.168.1.42:39999"


def test_wifi_pairing_connecting_and_mdns(world):
    fa, app, dep, _ = world
    wifi = next(p for p in group(dep, app)["panels"] if p["id"] == "wifi")
    assert any("port de connexion change" in t for t in wifi["text"])
    assert any("Associer un nouvel appareil" in t for t in wifi["text"])
    assert [f["id"] for f in wifi["forms"]] == ["pair", "connect"]
    assert "prêts à connecter" in wifi["list_title"]
    assert [i["actions"][0]["id"] for i in wifi["items"]] == ["connect", "pair"]
    with pytest.raises(android.ActionError) as e:
        dep.act(app, "android", "pair", "", {"ip": "192.168.1.42", "port": "37011", "code": "12"})
    assert "six chiffres" in str(e.value)
    with pytest.raises(android.ActionError) as e:
        dep.act(app, "android", "pair", "", {"ip": "192.168.1.42", "port": "37011", "code": "654321"})
    assert "refusée" in str(e.value)
    assert "Associé" in dep.act(app, "android", "pair", "", {"ip": "192.168.1.42", "port": "37011", "code": "123456"})["message"]
    assert ["pair", "192.168.1.42:37011", "123456"] in fa.calls()
    with pytest.raises(android.ActionError):
        dep.act(app, "android", "connect", "", {"ip": "pas une ip!", "port": "1"})
    # adb's mDNS not working here: said, the form stays.
    fa.update(lambda st: st.update(mdns_works=False))
    dep.adapters["android"]._mdns = (0.0, None)
    wifi = next(p for p in group(dep, app)["panels"] if p["id"] == "wifi")
    assert "ne répond pas ici" in wifi["list_title"] and wifi["items"] == []


def test_emulators_listed_and_started(world, monkeypatch):
    fa, app, dep, _ = world
    emu = next(p for p in group(dep, app)["panels"] if p["id"] == "emulators")
    assert [i["label"] for i in emu["items"]] == ["Pixel_8", "Wear_OS_Large_Round"]
    started = []
    monkeypatch.setattr(android, "start_detached", lambda argv: started.append(argv))
    assert "démarre" in dep.act(app, "android", "start_avd", "", {"avd": "Pixel_8"})["message"]
    assert started[0][-2:] == ["-avd", "Pixel_8"]
    monkeypatch.setattr(android, "EMULATOR", False)
    emu = next(p for p in group(dep, app)["panels"] if p["id"] == "emulators")
    assert emu["items"] == [] and "n'est pas trouvé" in emu["text"][0]


def test_screenshot_is_a_png(world):
    fa, app, dep, _ = world
    png = dep.image(app, "android", "screenshot", PHONE, {})
    assert png.startswith(b"\x89PNG")
    with pytest.raises(android.ActionError):
        dep.image(app, "android", "screenshot", "android:R3CN70UNAUTH", {})


def run_job(dep, app, choice):
    job = dep.start(app, "hyrox", choice)
    assert wait(lambda: job.status != "en cours", 30)
    return job.record()


def steps(rec):
    return [(s["target"], s["kind"], s["dest_name"], s["status"]) for s in rec["steps"]]


def test_a_deploy_builds_once_installs_on_each_device_then_launches(world):
    fa, app, dep, events = world
    rec = run_job(dep, app, {"Téléphone": [PHONE, EMU], "Montre": [WATCH]})
    assert steps(rec) == [
        ("Téléphone", "build", "", "fait"),
        ("Téléphone", "deploy", "SM-S928B", "fait"), ("Téléphone", "launch", "SM-S928B", "fait"),
        ("Téléphone", "deploy", "sdk_gphone64_x86_64", "fait"), ("Téléphone", "launch", "sdk_gphone64_x86_64", "fait"),
        ("Montre", "build", "", "fait"),
        ("Montre", "deploy", "SM-L705F", "fait"), ("Montre", "launch", "SM-L705F", "fait")]
    assert rec["status"] == "fait" and all(s["duration_s"] is not None for s in rec["steps"])
    calls = fa.calls()
    assert ["-s", HYROX_PHONE, "install", "-r", "app-phone-debug.apk"] in calls
    assert ["-s", "emulator-5554", "install", "-r", "app-phone-debug.apk"] in calls
    assert ["-s", HYROX_WATCH, "install", "-r", "app-wear-debug.apk"] in calls
    assert ["-s", HYROX_WATCH, "shell", "monkey", "-p", APP_ID, "-c", "android.intent.category.LAUNCHER", "1"] in calls
    log = open(rec["log_path"], encoding="utf-8").read()
    out = log.splitlines()        # the output lines, not the « $ command » echoes
    assert out.count("BUILD app-phone: assembleDebug") == 1 and out.count("BUILD app-wear: assembleDebug") == 1
    assert events[-1][0] == "deploy_ended" and events[-1][1]["status"] == "fait"
    assert dep.job_for(app)["id"] == rec["id"]


def test_the_device_goes_in_android_serial_without_serial_placeholder(world, tmp_path):
    fa, app, dep, _ = world
    t = hyrox_targets(fa)
    t[0]["install"] = say_env()
    write_profile(app, t[:1])
    rec = run_job(dep, app, {"Téléphone": [PHONE]})
    assert rec["status"] == "fait"
    assert f"SERIAL={HYROX_PHONE}" in open(rec["log_path"], encoding="utf-8").read()


def say_env():
    import sys
    return f'"{sys.executable}" -c "import os; print(\'SERIAL=\' + os.environ[\'ANDROID_SERIAL\'])"'


def test_a_build_failure_skips_its_target_only(world):
    fa, app, dep, events = world
    write_profile(app, hyrox_targets(fa, build_fails=True))
    rec = run_job(dep, app, {"Téléphone": [PHONE], "Montre": [WATCH]})
    assert steps(rec) == [
        ("Téléphone", "build", "", "échec"),
        ("Téléphone", "deploy", "SM-S928B", "sans objet"), ("Téléphone", "launch", "SM-S928B", "sans objet"),
        ("Montre", "build", "", "fait"), ("Montre", "deploy", "SM-L705F", "fait"), ("Montre", "launch", "SM-L705F", "fait")]
    failed = rec["steps"][0]
    assert failed["detail"] == "code 1" and failed["tail"] == ["BUILD app-phone: assembleDebug"]
    assert rec["status"] == "échec" and "Téléphone" in events[-1][1]["summary"]
    assert not any(c[:3] == ["-s", HYROX_PHONE, "install"] for c in fa.calls())


def test_an_install_failure_on_one_device_of_two(world):
    fa, app, dep, _ = world
    fa.update(lambda st: st.update(install_fails=["emulator-5554"]))
    rec = run_job(dep, app, {"Téléphone": [PHONE, EMU]})
    assert steps(rec) == [
        ("Téléphone", "build", "", "fait"),
        ("Téléphone", "deploy", "SM-S928B", "fait"), ("Téléphone", "launch", "SM-S928B", "fait"),
        ("Téléphone", "deploy", "sdk_gphone64_x86_64", "échec"), ("Téléphone", "launch", "sdk_gphone64_x86_64", "sans objet")]
    bad = rec["steps"][3]
    assert any("INSTALL_FAILED_INSUFFICIENT_STORAGE" in x for x in bad["tail"])


def test_a_deploy_refuses_what_cannot_go(world):
    fa, app, dep, _ = world
    with pytest.raises(deploy.DeployError, match="ne va pas"):
        dep.start(app, "hyrox", {"Montre": [PHONE]})
    with pytest.raises(deploy.DeployError, match="n'est pas connecté"):
        dep.start(app, "hyrox", {"Téléphone": ["android:R3CN70UNAUTH"]})
    with pytest.raises(deploy.DeployError, match="aucune cible"):
        dep.start(app, "hyrox", {})
    with pytest.raises(deploy.DeployError, match="cible inconnue"):
        dep.start(app, "hyrox", {"Tablette": [PHONE]})


def journal(dep, app, dest=PHONE, after=0):
    return dep.journal(app, "android", dest, None, after)


def texts(j):
    return [x["text"] for x in j["lines"]]


def test_the_log_keeps_the_application_and_marks_a_crash(world):
    fa, app, dep, events = world
    j = journal(dep, app)
    assert j["live"] and texts(j) == [f"— {APP_ID} tourne : pid 4321 —"]
    fa.logcat(HYROX_PHONE,
              threadtime(4321, "I", "hyrox", "tour 1"),
              threadtime(999, "I", "bluetooth", "pas l'application"),
              threadtime(4321, "E", "AndroidRuntime", "FATAL EXCEPTION: main"),
              threadtime(4321, "E", "AndroidRuntime", f"Process: {APP_ID}, PID: 4321"),
              threadtime(4321, "E", "AndroidRuntime", "java.lang.IllegalStateException: boum"),
              threadtime(4321, "E", "AndroidRuntime", "\tat com.mgilli.hyroxtracker.Main.onCreate(Main.kt:12)"),
              threadtime(4321, "I", "hyrox", "après"),
              threadtime(1000, "E", "ActivityManager", f"ANR in {APP_ID} (com.mgilli.hyroxtracker/.Main)"),
              threadtime(1000, "E", "ActivityManager", "PID: 4321"),
              threadtime(1000, "E", "ActivityManager", "Reason: Input dispatching timed out"),
              threadtime(1000, "I", "ActivityManager", "unrelated"))
    assert wait(lambda: len(journal(dep, app)["lines"]) >= 10)
    j = journal(dep, app)
    t = texts(j)
    assert not any("bluetooth" in x or "unrelated" in x for x in t)
    assert any("ANR in" in x for x in t) and any("Reason: Input" in x for x in t)
    fatal, anr = j["crashes"]
    assert (fatal["rule"], fatal["title"]) == ("FATAL EXCEPTION", "FATAL EXCEPTION: main")
    assert len(fatal["lines"]) == 4 and "Main.kt:12" in fatal["lines"][-1]
    assert anr["rule"] == "ANR" and anr["title"].startswith(f"ANR in {APP_ID}") and len(anr["lines"]) == 3
    marked = [x["text"] for x in j["lines"] if x["crash"] == fatal["id"]]
    assert len(marked) == 4 and not any("après" in x for x in marked)
    crashes = [d for k, d in events if k == "deploy_crash"]
    assert [c["rule"] for c in crashes] == ["FATAL EXCEPTION", "ANR"] and crashes[0]["dest_name"] == "SM-S928B"
    # « after »: only what came since.
    assert journal(dep, app, after=j["last"])["lines"] == []


def test_the_log_follows_the_process_across_restarts(world, monkeypatch):
    fa, app, dep, _ = world
    monkeypatch.setattr(android, "PID_POLL", 0.2)
    journal(dep, app)
    # Android starts it again: ActivityManager says so, the new pid is followed.
    fa.logcat(HYROX_PHONE,
              threadtime(1000, "I", "ActivityManager", f"Start proc 5555:{APP_ID}/u0a321 for activity"),
              threadtime(5555, "I", "hyrox", "nouveau processus"))
    assert wait(lambda: any("nouveau processus" in x for x in texts(journal(dep, app))))
    t = texts(journal(dep, app))
    assert f"— {APP_ID} redémarre : pid 5555 (lancé par Android) —" in t
    # Started again from elsewhere: `pidof` finds it.
    fa.update(lambda st: st["devices"][0].update(pids={APP_ID: "6666"}))
    assert wait(lambda: f"— {APP_ID} redémarre : pid 6666 —" in texts(journal(dep, app)))
    fa.logcat(HYROX_PHONE, threadtime(6666, "I", "hyrox", "troisième"))
    assert wait(lambda: "troisième" in "".join(texts(journal(dep, app))))


def test_one_destination_at_a_time_and_a_device_that_goes(world):
    fa, app, dep, _ = world
    journal(dep, app)
    journal(dep, app, WATCH)
    assert len(dep.journals) == 1
    fa.update(lambda st: st.setdefault("gone", {}).update({HYROX_WATCH: True}))
    assert wait(lambda: not journal(dep, app, WATCH)["live"])
    j = journal(dep, app, WATCH)
    assert j["ended"] == "l'appareil ne répond plus" and "interrompu" in texts(j)[-1]


def test_launch_and_stop_from_the_card(world):
    fa, app, dep, _ = world
    assert "lancée" in dep.act(app, "android", "launch", PHONE, {"target": "Téléphone"})["message"]
    assert "arrêtée" in dep.act(app, "android", "stop", PHONE, {"target": "Téléphone"})["message"]
    assert ["-s", HYROX_PHONE, "shell", "am", "force-stop", APP_ID] in fa.calls()


def test_no_adb_said(world, monkeypatch):
    fa, app, dep, _ = world
    monkeypatch.setattr(android, "ADB", False)
    g = group(dep, app)
    assert g["destinations"][0]["state"] == "erreur" and "adb introuvable" in g["destinations"][0]["note"]
    assert g["panels"][0]["id"] == "adb" and "platform-tools" in g["panels"][0]["text"][0]


def test_build_command_unused_when_empty(world):
    fa, app, dep, _ = world
    t = hyrox_targets(fa)[:1]
    t[0]["build"] = ""
    write_profile(app, t)
    rec = run_job(dep, app, {"Téléphone": [PHONE]})
    assert [s["kind"] for s in rec["steps"]] == ["deploy", "launch"]


def test_parse_devices_states():
    out = android.parse_devices("List of devices attached\n"
                                "R5CT10AB1234           device usb:1-1 product:e3q model:SM_S928B device:e3q transport_id:1\n"
                                "R3CN70UNAUTH           unauthorized usb:1-2 transport_id:2\n"
                                "XYZ                    no permissions (user in plugdev group); see [http://x]\n")
    assert [(d["serial"], d["state"]) for d in out] == [("R5CT10AB1234", "device"), ("R3CN70UNAUTH", "unauthorized"),
                                                        ("XYZ", "no permissions")]
    assert out[0]["model"] == "SM_S928B"
    assert android.wifi("192.168.1.42:41235") and android.wifi("adb-RFAX-x._adb-tls-connect._tcp")
    assert not android.wifi("R5CT10AB1234") and not android.wifi("emulator-5554")
