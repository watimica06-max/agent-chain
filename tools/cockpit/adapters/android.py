"""The `android` adapter (1.8): devices through adb — USB, Wi-Fi, emulators.

- Destinations: `adb devices -l`, each device read once by `getprop` (its
  model, whether it is a watch, its Android version) and its battery by
  `dumpsys battery`. Its name is the Product Owner's, kept in config.json
  under its hardware serial (`ro.serialno`), which does not change between
  USB and Wi-Fi as adb's serial does. A device that disappears stays, greyed,
  « déconnecté », with its last Wi-Fi address.
- Wi-Fi: `adb pair`, `adb connect`, and what `adb mdns services` finds.
- Emulators: the emulator tool's `-list-avds`, « Démarrer ».
- Deploy: the target's install command, the device given by `{serial}` or by
  `ANDROID_SERIAL`; then the application launched by its id.
- Log: `adb logcat` (main, system, crash) on the application's processes,
  followed across restarts. Screenshot: `screencap -p`. Mirror: scrcpy.
"""
import os
import re
import shutil
import subprocess
import threading
import time

from .base import (ActionError, Adapter, CrashRule, LogStream, Step, WINDOWS, action, field_spec,
                   kill_tree, run_argv, run_shell, start_detached)

# The programs, found on the PATH or in the Android SDK. A test puts an argv
# list here (a fake adb), or False for « absent ».
ADB = None
EMULATOR = None
SCRCPY = None

FACTS_TTL = 60.0         # getprop, once a minute per device
BATTERY_TTL = 30.0
MDNS_TTL = 10.0
PID_POLL = 3.0           # how often the journal asks for the application's processes
INSTALL_TIMEOUT = 900

SCRCPY_HINT = ("scrcpy n'est pas installé : il se télécharge sur github.com/Genymobile/scrcpy (le zip Windows de "
               "la dernière version, décompressé, son dossier ajouté au PATH), puis redémarrer le cockpit.")
UNAUTHORIZED = ("L'appareil refuse cet ordinateur : déverrouillez-le et acceptez « Autoriser le débogage » "
                "(cochez « Toujours autoriser depuis cet ordinateur ») — sur une montre, l'invite s'affiche sur la montre.")
OFFLINE = ("adb voit l'appareil sans pouvoir lui parler : débranchez-le et rebranchez-le ; en Wi-Fi, "
           "reconnectez-le — le port a peut-être changé.")
WEAR_HELP = [
    "Sur la montre : Paramètres → Système (ou « À propos de la montre ») → Informations sur le logiciel, toucher "
    "plusieurs fois « Version du logiciel » jusqu'au message des options pour les développeurs. Puis Paramètres → "
    "Options pour les développeurs : activer « Débogage ADB » et « Débogage sans fil ».",
    "« Associer » — une fois par ordinateur : dans « Débogage sans fil », « Associer un nouvel appareil » affiche "
    "l'adresse IP, le port d'association et le code à six chiffres.",
    "« Connecter » — à chaque fois : l'écran « Débogage sans fil » lui-même affiche l'adresse IP et le port de "
    "connexion, qui n'est pas celui d'association.",
    "Le port de connexion change chaque fois que le débogage sans fil redémarre — la montre qui se met en veille, "
    "le Wi-Fi qui se coupe : il faut alors « Connecter » avec le nouveau port. L'association, elle, reste.",
]

KINDS = [["phone", "téléphone"], ["watch", "montre"], ["any", "tout appareil"]]
LINE = re.compile(r"^\s*\d\d-\d\d\s+\d\d:\d\d:\d\d\.\d+\s+(\d+)\s+\d+\s+[VDIWEFA]\s")
IPV4 = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
HOST = re.compile(r"^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$")
APP_ID = re.compile(r"^[A-Za-z][\w]*(\.[A-Za-z][\w]*)+$")
MDNS = re.compile(r"^(\S+)\s+(_adb[-\w]*\._tcp)\.?\s+(\[?[0-9A-Fa-f:.]+\]?):(\d+)\s*$")


def sdk_roots():
    out = []
    for k in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
        v = (os.environ.get(k) or "").strip().strip('"')
        if v:
            out.append(v)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        out.append(os.path.join(local, "Android", "Sdk"))
    return out


def _in_sdk(*parts):
    exe = parts[-1] + (".exe" if WINDOWS else "")
    for root in sdk_roots():
        p = os.path.join(root, *parts[:-1], exe)
        if os.path.isfile(p):
            return p
    return None


def adb_argv():
    if ADB is not None:
        return ADB or None
    p = shutil.which("adb") or _in_sdk("platform-tools", "adb")
    return [p] if p else None


def emulator_argv():
    """The emulator tool: on the PATH, else in the SDK (`emulator/`), where
    Android Studio puts it without adding it to the PATH."""
    if EMULATOR is not None:
        return EMULATOR or None
    p = shutil.which("emulator") or _in_sdk("emulator", "emulator")
    return [p] if p else None


def scrcpy_argv():
    if SCRCPY is not None:
        return SCRCPY or None
    p = shutil.which("scrcpy")
    return [p] if p else None


def parse_devices(text):
    """`adb devices -l`: [{serial, state, model, transport…}]."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices") or line.startswith("*"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        d = {"serial": parts[0], "state": parts[1]}
        rest = parts[2:]
        if d["state"] == "no" and rest[:1] == ["permissions"]:
            d["state"], rest = "no permissions", rest[1:]
        for p in rest:
            if ":" in p:
                k, _, v = p.partition(":")
                d[k] = v
        out.append(d)
    return out


def parse_props(text):
    props = {}
    for m in re.finditer(r"^\[([^\]]+)\]:\s*\[(.*)\]\s*$", text, re.M):
        props[m.group(1)] = m.group(2)
    return props


def parse_mdns(text):
    out = []
    for line in text.splitlines():
        m = MDNS.match(line.strip())
        if m:
            out.append({"name": m.group(1), "service": m.group(2), "ip": m.group(3).strip("[]"),
                        "port": m.group(4), "pairing": "pairing" in m.group(2)})
    return out


def wifi(serial):
    return bool(re.match(r"^[\w.\-\[\]:]+:\d+$", serial)) or "._adb-tls-connect." in serial


class AndroidAdapter(Adapter):
    TYPE = "android"
    LABEL = "Android"
    DEPLOY_LABEL = "Installer"
    FIELDS = [
        field_spec("kind", "Appareil", "choice", required=True, choices=KINDS, default="any",
                   help="Les appareils proposés pour cette cible : un téléphone (ou un émulateur de téléphone), "
                        "une montre, ou tout appareil."),
        field_spec("install", "Commande d'installation", required=True,
                   placeholder=r".\gradlew.bat :app:installDebug",
                   help="Lancée depuis la racine de l'application, une fois par appareil. {serial} y est remplacé "
                        "par l'appareil ; sans {serial}, l'appareil est passé dans ANDROID_SERIAL."),
        field_spec("app_id", "Identifiant de l'application",
                   placeholder="com.exemple.application",
                   help="Son applicationId : il lance l'application après l'installation et filtre son journal. "
                        "Vide : rien n'est lancé, et le journal montre tout l'appareil."),
    ]
    CRASHES = [
        CrashRule("FATAL EXCEPTION", r"FATAL EXCEPTION", r"\sE\s+AndroidRuntime\s*:"),
        CrashRule("ANR", r"\bANR in ", r"\sE\s+ActivityManager\s*:"),
    ]

    def __init__(self, hub):
        super().__init__(hub)
        self._facts = {}           # adb serial -> (time, props)
        self._battery = {}         # adb serial -> (time, level)
        self._serial_of = {}       # stable key -> adb serial, as last seen
        self._mdns = (0.0, None)
        self._lock = threading.Lock()

    # ------------------------------------------------------------- fields

    def check(self, target):
        errors = super().check(target)
        aid = (target.get("app_id") or "").strip()
        if aid and "app_id" not in errors and not APP_ID.match(aid):
            errors["app_id"] = "un identifiant comme com.exemple.application"
        return errors

    # ---------------------------------------------------------------- adb

    def adb(self, *args, timeout=15, binary=False):
        argv = adb_argv()
        if not argv:
            raise ActionError("adb introuvable : ni dans le PATH, ni dans le SDK Android")
        return run_argv([*argv, *args], timeout=timeout, binary=binary)

    def devices(self):
        code, out = self.adb("devices", "-l")
        if code:
            raise ActionError(f"adb devices : {out}")
        return parse_devices(out)

    def props(self, serial):
        hit = self._facts.get(serial)
        if hit and time.monotonic() - hit[0] < FACTS_TTL:
            return hit[1]
        code, out = self.adb("-s", serial, "shell", "getprop")
        props = parse_props(out) if code == 0 else {}
        if props:
            self._facts[serial] = (time.monotonic(), props)
        return props

    def battery(self, serial):
        hit = self._battery.get(serial)
        if hit and time.monotonic() - hit[0] < BATTERY_TTL:
            return hit[1]
        level = None
        try:
            code, out = self.adb("-s", serial, "shell", "dumpsys", "battery", timeout=10)
            m = re.search(r"^\s*level:\s*(\d+)", out, re.M)
            level = int(m.group(1)) if code == 0 and m else None
        except ActionError:
            pass
        self._battery[serial] = (time.monotonic(), level)
        return level

    def mdns(self):
        """What `adb mdns services` finds — None when adb's mDNS does not
        work here."""
        t, hit = self._mdns
        if time.monotonic() - t < MDNS_TTL and hit is not None:
            return hit
        try:
            code, out = self.adb("mdns", "check", timeout=8)
            if code or "mdns daemon" not in out.lower():
                found = {"works": False, "services": [], "detail": out.strip()[:200]}
            else:
                code, out = self.adb("mdns", "services", timeout=8)
                found = {"works": code == 0, "services": parse_mdns(out) if code == 0 else [], "detail": ""}
        except ActionError as e:
            found = {"works": False, "services": [], "detail": str(e)}
        self._mdns = (time.monotonic(), found)
        return found

    def resolve(self, dest_id):
        """The adb serial of a destination right now, or ActionError."""
        key = dest_id.split(":", 1)[1] if dest_id.startswith("android:") else dest_id
        for d in self.devices():
            stable = self._stable(d)
            if stable == key or d["serial"] == key:
                if d["state"] != "device":
                    raise ActionError(f"l'appareil est « {d['state']} »")
                return d["serial"], stable
        raise ActionError("l'appareil n'est pas connecté")

    def _stable(self, d):
        if d["state"] != "device":
            return self._known_stable(d["serial"])
        sn = (self.props(d["serial"]).get("ro.serialno") or "").strip()
        return sn if sn and sn.lower() != "unknown" else d["serial"]

    def _known_stable(self, serial):
        for k, s in self._serial_of.items():
            if s == serial:
                return k
        return serial

    # ------------------------------------------------------- destinations

    def destinations(self, targets, app):
        try:
            found = self.devices()
        except ActionError as e:
            return [{"id": "android:-", "name": "adb", "kind": "", "state": "erreur", "connected": False,
                     "facts": [], "note": str(e), "actions": []}]
        out, seen = [], set()
        for d in found:
            serial, st = d["serial"], d["state"]
            emulator = serial.startswith("emulator-")
            props = self.props(serial) if st == "device" else {}
            stable = self._stable(d)
            with self._lock:
                self._serial_of[stable] = serial
            seen.add(stable)
            watch = "watch" in (props.get("ro.build.characteristics") or "")
            emulator = emulator or props.get("ro.kernel.qemu") == "1" or props.get("ro.boot.qemu") == "1"
            model = props.get("ro.product.model") or d.get("model", "").replace("_", " ") or "?"
            known = self.store.get(stable) or {}
            if st == "device":
                upd = {"model": model, "form": "watch" if watch else "phone", "emulator": emulator}
                if wifi(serial) and ":" in serial and "._adb" not in serial:
                    upd["last_address"] = serial
                if any(known.get(k) != v for k, v in upd.items()):
                    self.store.set(stable, **upd)
                    known = {**known, **upd}
            if emulator:
                kind = "émulateur" + (" (montre)" if watch else "")
            else:
                kind = "montre" if watch else "téléphone" if st == "device" else "appareil"
            link = "émulateur" if emulator else "Wi-Fi" if wifi(serial) else "USB"
            facts = [["Modèle", model], ["Type", kind], ["Liaison", link], ["Série adb", serial]]
            if st == "device":
                rel = props.get("ro.build.version.release")
                facts.append(["Android", f"{rel} (API {props.get('ro.build.version.sdk', '?')})" if rel else "?"])
                lvl = self.battery(serial)
                facts.append(["Batterie", f"{lvl} %" if lvl is not None else "?"])
            dest = {"id": f"android:{stable}", "name": known.get("name") or (model if model != "?" else serial),
                    "named": bool(known.get("name")), "kind": kind, "state": st,
                    # A device adb cannot read is no kind yet — unless it was read before.
                    "form": ("watch" if watch else "phone") if st == "device" else known.get("form"),
                    "connected": st == "device", "facts": facts,
                    "note": UNAUTHORIZED if st == "unauthorized" else OFFLINE if st == "offline" else
                    (f"adb dit « {st} »" if st != "device" else ""),
                    "actions": []}
            dest["actions"] = self._actions(dest, targets, serial, known)
            out.append(dest)
        for key, info in self.store.all().items():
            if key in seen or info.get("adapter", "android") != "android" or not info.get("model"):
                continue
            kind = "montre" if info.get("form") == "watch" else "téléphone"
            if info.get("emulator"):
                kind = "émulateur"
            dest = {"id": f"android:{key}", "name": info.get("name") or info.get("model"), "named": bool(info.get("name")),
                    "kind": kind, "form": info.get("form", "phone"), "state": "déconnecté", "connected": False,
                    "facts": [["Modèle", info.get("model", "?")], ["Type", kind]]
                    + ([["Dernière adresse", info["last_address"]]] if info.get("last_address") else []),
                    "note": "", "actions": []}
            dest["actions"] = self._actions(dest, targets, None, info)
            out.append(dest)
        return out

    def _actions(self, dest, targets, serial, known):
        acts = []
        if dest["connected"]:
            acts.append(action("journal", "Journal", "journal"))
            acts.append(action("screenshot", "Capture d'écran", "image"))
            if scrcpy_argv():
                acts.append(action("mirror", "Afficher l'écran", title="scrcpy, dans une fenêtre à part"))
            else:
                acts.append(action("mirror", "Afficher l'écran", title=SCRCPY_HINT, args={"missing": True}))
            for t in targets:
                if self.accepts(t, dest) and (t.get("app_id") or "").strip():
                    acts.append(action("launch", f"Lancer « {t['name']} »", args={"target": t["name"]}))
                    acts.append(action("stop", f"Arrêter « {t['name']} »", args={"target": t["name"]}))
        elif known.get("last_address"):
            acts.append(action("reconnect", "Reconnecter", primary=True, args={"address": known["last_address"]},
                               title=f"adb connect {known['last_address']} — si le port a changé, « Connecter » avec le nouveau"))
        acts.append(action("rename", "Renommer", "rename"))
        if not dest["connected"] and dest["state"] == "déconnecté":
            acts.append(action("forget", "Oublier", confirm=f"Oublier « {dest['name']} » ? Son nom et sa dernière adresse sont effacés."))
        return acts

    def panels(self, targets, app):
        out = []
        if not adb_argv():
            out.append({"id": "adb", "title": "adb", "text": [
                "adb n'est pas trouvé : ni dans le PATH, ni dans le SDK Android (ANDROID_HOME, ou %LOCALAPPDATA%\\Android\\Sdk). "
                "Android Studio l'installe avec le SDK ; ajoutez son dossier platform-tools au PATH, puis redémarrez le cockpit."],
                "items": [], "forms": []})
            return out
        ip = field_spec("ip", "Adresse IP", placeholder="192.168.1.42")
        port = field_spec("port", "Port", placeholder="37000")
        code = field_spec("code", "Code d'association", placeholder="123456")
        md = self.mdns()
        items = []
        for s in md["services"]:
            if s["pairing"]:
                items.append({"label": f"{s['name']} — à associer", "sub": f"{s['ip']}:{s['port']}",
                              "actions": [action("pair", "Associer", args={"ip": s["ip"], "port": s["port"]},
                                                 fields=[code])]})
            else:
                items.append({"label": s["name"], "sub": f"{s['ip']}:{s['port']}",
                              "actions": [action("connect", "Connecter", primary=True,
                                                 args={"ip": s["ip"], "port": s["port"]})]})
        md_line = (("Trouvés sur le réseau par adb (mDNS) — prêts à connecter :" if items else
                    "adb cherche les appareils sur le réseau (mDNS) : aucun pour l'instant — le débogage sans fil "
                    "doit être allumé sur l'appareil.") if md["works"]
                   else "La recherche sur le réseau d'adb (mDNS) ne répond pas ici : saisissez l'adresse et le port.")
        out.append({"id": "wifi", "title": "Wi-Fi", "text": WEAR_HELP, "list_title": md_line, "items": items,
                    "forms": [action("pair", "Associer", fields=[ip, port, code]),
                              action("connect", "Connecter", primary=True, fields=[ip, port])]})
        emu = emulator_argv()
        if emu:
            try:
                code_, txt = run_argv([*emu, "-list-avds"], timeout=20)
                avds = [x.strip() for x in txt.splitlines() if x.strip() and not x.startswith(("INFO", "WARNING", "ERROR"))] if code_ == 0 else []
            except ActionError as e:
                avds, txt = [], str(e)
            out.append({"id": "emulators", "title": "Émulateurs",
                        "text": [f"L'émulateur Android : {emu[0]}." + ("" if avds else " Aucun appareil virtuel : Android Studio → Device Manager en crée un.")],
                        "items": [{"label": a, "sub": "appareil virtuel",
                                   "actions": [action("start_avd", "Démarrer", args={"avd": a})]} for a in avds],
                        "forms": []})
        else:
            out.append({"id": "emulators", "title": "Émulateurs", "text": [
                "L'émulateur Android n'est pas trouvé : Android Studio → SDK Manager → SDK Tools → « Android Emulator »."],
                "items": [], "forms": []})
        return out

    def accepts(self, target, dest):
        k = target.get("kind") or "any"
        return k == "any" or dest.get("form") == k

    # -------------------------------------------------------------- deploy

    def deploy_steps(self, target, dest, app):
        steps = [Step("deploy", "Installer", lambda out: self._install(target, dest, app, out))]
        if (target.get("app_id") or "").strip():
            steps.append(Step("launch", "Lancer", lambda out: self._launch(target, dest, out)))
        return steps

    def _install(self, target, dest, app, out):
        serial, _ = self.resolve(dest["id"])
        cmd = target["install"]
        env = None
        if "{serial}" in cmd:
            cmd = cmd.replace("{serial}", serial)
        else:
            env = {"ANDROID_SERIAL": serial}
        out(f"$ {cmd}" + ("" if env is None else f"   (ANDROID_SERIAL={serial})"))
        r = run_shell(cmd, app, out, env=env, timeout=INSTALL_TIMEOUT)
        if r.timed_out:
            return False, f"délai dépassé ({INSTALL_TIMEOUT // 60} min)", r.tail
        return r.code == 0, f"code {r.code}", r.tail

    def _launch(self, target, dest, out):
        serial, _ = self.resolve(dest["id"])
        aid = target["app_id"].strip()
        argv = ["-s", serial, "shell", "monkey", "-p", aid, "-c", "android.intent.category.LAUNCHER", "1"]
        out("$ adb " + " ".join(argv))
        code, text = self.adb(*argv, timeout=30)
        for line in text.splitlines():
            out(line)
        ok = code == 0 and "No activities found" not in text and "aborted" not in text
        return ok, ("lancée" if ok else "non lancée"), text.splitlines()[-10:]

    # ------------------------------------------------------------- journal

    def journal(self, target, dest, app):
        serial, _ = self.resolve(dest["id"])
        aid = ((target or {}).get("app_id") or "").strip()
        f = LogcatFollower(self, serial, aid, dest.get("name") or serial,
                           lambda c: self.hub.crash(dest, target, c))
        f.start()
        return f

    # ------------------------------------------------------------- actions

    def act(self, action_id, dest_id, args, app, targets):
        if action_id == "pair":
            return self._pair(args)
        if action_id == "connect":
            return self._connect(self._address(args))
        if action_id == "reconnect":
            key = dest_id.split(":", 1)[1]
            addr = (self.store.get(key) or {}).get("last_address") or args.get("address")
            if not addr:
                raise ActionError("aucune adresse gardée pour cet appareil")
            return self._connect(addr)
        if action_id == "start_avd":
            emu = emulator_argv()
            if not emu:
                raise ActionError("l'émulateur Android n'est pas trouvé")
            avd = (args.get("avd") or "").strip()
            if not re.match(r"^[\w.\-]+$", avd):
                raise ActionError("nom d'appareil virtuel illisible")
            start_detached([*emu, "-avd", avd])
            return {"message": f"« {avd} » démarre — il paraît dans la liste une fois prêt, en général en moins d'une minute."}
        if action_id == "rename":
            return self._rename(dest_id, args)
        if action_id == "forget":
            self.store.forget(dest_id.split(":", 1)[1])
            return {"message": "Oublié."}
        serial, stable = self.resolve(dest_id)
        if action_id == "mirror":
            sc = scrcpy_argv()
            if not sc:
                raise ActionError(SCRCPY_HINT)
            name = (self.store.get(stable) or {}).get("name") or serial
            start_detached([*sc, "-s", serial, "--window-title", name])
            return {"message": f"scrcpy s'ouvre dans sa propre fenêtre : l'écran de « {name} »."}
        if action_id in ("launch", "stop"):
            t = next((x for x in targets if x["name"] == args.get("target")), None)
            if not t or not (t.get("app_id") or "").strip():
                raise ActionError("cible inconnue, ou sans identifiant d'application")
            if action_id == "launch":
                ok, said, tail = self._launch(t, {"id": dest_id}, lambda line: None)
                if not ok:
                    raise ActionError("non lancée : " + " ".join(tail)[-300:])
                return {"message": f"« {t['name']} » lancée."}
            code, text = self.adb("-s", serial, "shell", "am", "force-stop", t["app_id"].strip())
            if code:
                raise ActionError(text[-300:])
            return {"message": f"« {t['name']} » arrêtée."}
        raise ActionError(f"action inconnue : {action_id}")

    def image(self, action_id, dest_id, args):
        if action_id != "screenshot":
            raise ActionError(f"action inconnue : {action_id}")
        serial, _ = self.resolve(dest_id)
        code, data, err = self.adb("-s", serial, "exec-out", "screencap", "-p", timeout=30, binary=True)
        if code or not data.startswith(b"\x89PNG"):
            raise ActionError(f"capture non obtenue : {err.strip() or 'pas une image PNG'}")
        return data

    def _address(self, args):
        if args.get("address"):
            return args["address"].strip()
        ip, port = (args.get("ip") or "").strip(), (args.get("port") or "").strip()
        if not (IPV4.match(ip) or HOST.match(ip)):
            raise ActionError("l'adresse IP est illisible — par exemple 192.168.1.42")
        if not port.isdigit() or not 0 < int(port) < 65536:
            raise ActionError("le port est un nombre — celui que l'appareil affiche")
        return f"{ip}:{port}"

    def _pair(self, args):
        addr = self._address(args)
        code = (args.get("code") or "").strip()
        if not re.fullmatch(r"\d{6}", code):
            raise ActionError("le code d'association a six chiffres")
        rc, out = self.adb("pair", addr, code, timeout=40)
        if rc == 0 and "Successfully paired" in out:
            return {"message": f"Associé à {addr}. Maintenant « Connecter », avec le port de l'écran « Débogage sans fil » "
                               "lui-même — pas celui d'association."}
        raise ActionError(f"association refusée : {out.strip()[-300:] or f'code {rc}'}")

    def _connect(self, addr):
        rc, out = self.adb("connect", addr, timeout=30)
        low = out.lower()
        if rc == 0 and ("connected to" in low) and "failed" not in low and "cannot" not in low:
            self._mdns = (0.0, None)
            return {"message": f"Connecté à {addr}."}
        raise ActionError(f"connexion refusée : {out.strip()[-300:] or f'code {rc}'} — le port change quand le débogage "
                          "sans fil redémarre : relisez-le sur l'appareil.")

    def _rename(self, dest_id, args):
        name = (args.get("name") or "").strip()
        if not name:
            raise ActionError("un nom vide")
        if len(name) > 40:
            raise ActionError("un nom de 40 caractères au plus")
        self.store.set(dest_id.split(":", 1)[1], name=name)
        return {"message": f"Renommé « {name} »."}


class LogcatFollower:
    """`adb logcat` on one device, kept to the application's processes: the
    lines of its pids, and those that name it (« ANR in », « Start proc »,
    « has died »). A new process of the application — a restart — is
    followed as it comes, from ActivityManager's « Start proc » and from a
    `pidof` every few seconds."""

    def __init__(self, adapter, serial, app_id, name, on_crash):
        self.adapter, self.serial, self.app_id, self.name = adapter, serial, app_id, name
        self.stream = LogStream(adapter.CRASHES, on_crash)
        self.pids = set()
        self.proc = None
        self._stop = threading.Event()

    def pidof(self):
        try:
            code, out = self.adapter.adb("-s", self.serial, "shell", "pidof", self.app_id, timeout=8)
        except ActionError:
            return set()
        return {p for p in out.split() if p.isdigit()} if code == 0 else set()

    def _new_pid(self, pid, how):
        if pid in self.pids:
            return
        first = not self.pids
        self.pids.add(pid)
        self.stream.add(f"— {self.app_id} {'tourne' if first else 'redémarre'} : pid {pid}{how} —", marker=True)

    def start(self):
        argv = adb_argv()
        if not argv:
            raise ActionError("adb introuvable")
        if self.app_id:
            pids = self.pidof()
            if pids:
                for p in sorted(pids):
                    self._new_pid(p, "")
            else:
                self.stream.add(f"— {self.app_id} ne tourne pas sur {self.name} : le journal l'attend —", marker=True)
        else:
            self.stream.add(f"— tout le journal de {self.name} : la cible n'a pas d'identifiant d'application —", marker=True)
        self.proc = subprocess.Popen([*argv, "-s", self.serial, "logcat", "-v", "threadtime", "-b", "main,system,crash",
                                      "-T", "500"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1)
        self.stream.live = True
        threading.Thread(target=self._read, daemon=True).start()
        if self.app_id:
            threading.Thread(target=self._poll, daemon=True).start()

    def _keep(self, line):
        if not self.app_id:
            return True
        m = LINE.match(line)
        if m and m.group(1) in self.pids:
            return True
        if self.app_id in line:
            return True
        return self.stream.continues(line)

    def _read(self):
        try:
            for line in self.proc.stdout:
                if self._stop.is_set():
                    break
                line = line.rstrip("\r\n")
                if line and self._keep(line):
                    self.stream.add(line)
                    # ActivityManager starting the application again: its new
                    # process is followed from here, said under the line.
                    m = re.search(r"Start proc (\d+):" + re.escape(self.app_id) + r"(?:[/:]|\b)", line) \
                        if self.app_id else None
                    if m:
                        self._new_pid(m.group(1), " (lancé par Android)")
        finally:
            self.stream.live = False
            if not self._stop.is_set():
                self.stream.ended = "l'appareil ne répond plus"
                self.stream.add("— journal interrompu : l'appareil ne répond plus —", marker=True)

    def _poll(self):
        while not self._stop.wait(PID_POLL):
            for p in sorted(self.pidof() - self.pids):
                self._new_pid(p, "")

    def stop(self):
        self._stop.set()
        if self.proc:
            kill_tree(self.proc)
        self.stream.live = False
        self.stream.ended = "arrêté"
