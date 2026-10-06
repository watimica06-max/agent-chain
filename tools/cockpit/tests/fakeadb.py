"""A fake adb, for the tests and the screenshots (1.8) — no real device is
ever touched.

    python fakeadb.py <state.json> <adb arguments…>

The state file says which devices are there and how each answers; it is read
again on every call, so a test changes the world by rewriting it. Every call
is appended to `<state.json>.calls`, one JSON list per line.

Answers: `version`, `devices -l`, `-s S shell getprop`, `-s S shell dumpsys
battery`, `-s S shell pidof ID`, `-s S shell monkey -p ID …`, `-s S shell am
force-stop ID`, `-s S install …`, `-s S logcat …` (the file `logcat` names
for the device, then what is appended to it, until `<state.json>.stop`
exists), `-s S exec-out screencap -p`, `pair`, `connect`, `mdns check`, `mdns
services`.
"""
import json
import os
import struct
import sys
import time
import zlib


def png(w=270, h=480, rgb=(47, 107, 143)):
    """A plain PNG: a screen-shaped block of colour with a lighter band."""
    rows = []
    for y in range(h):
        c = (230, 238, 244) if h * 0.12 < y < h * 0.22 else rgb
        rows.append(b"\x00" + bytes(c) * w)
    raw = zlib.compress(b"".join(rows), 9)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", raw) + chunk(b"IEND", b""))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, st):
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    for _ in range(50):                 # a reader may hold it open for an instant (Windows)
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.02)
    os.replace(tmp, path)


def say(text="", code=0):
    sys.stdout.write(text + ("\n" if text and not text.endswith("\n") else ""))
    sys.stdout.flush()
    sys.exit(code)


def device(st, serial):
    d = next((x for x in st["devices"] if x["serial"] == serial), None)
    if d is None:
        say(f"adb: device '{serial}' not found", 1)
    if d["state"] != "device":
        say(f"adb: device {d['state']}", 1)
    return d


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")          # adb writes UTF-8, whatever the console
    path, args = argv[0], argv[1:]
    with open(path + ".calls", "a", encoding="utf-8") as f:
        f.write(json.dumps(args) + "\n")
    st = load(path)
    if args[:1] == ["version"]:
        say("Android Debug Bridge version 1.0.41\nVersion 37.0.1-fake\nInstalled as fakeadb.py")
    if args[:1] == ["devices"]:
        out = ["List of devices attached"]
        for d in st["devices"]:
            extra = "" if d["state"] != "device" else \
                f" product:{d.get('product', 'p')} model:{d.get('model', 'M')} device:{d.get('device', 'd')} transport_id:{d.get('tid', 1)}"
            out.append(f"{d['serial']:<22} {d['state']}" + (" usb:1-1" if d.get("usb") else "") + extra)
        say("\n".join(out) + "\n")
    if args[:2] == ["mdns", "check"]:
        if st.get("mdns_works", True):
            say("mdns daemon version [Openscreen discovery 0.0.0]")
        say("ERROR: mdns daemon unavailable", 1)
    if args[:2] == ["mdns", "services"]:
        say("List of discovered mdns services\n" + "".join(x + "\n" for x in st.get("mdns", [])))
    if args[:1] == ["pair"]:
        addr, code = args[1], args[2] if len(args) > 2 else ""
        if code == st.get("pair_code"):
            st.setdefault("paired", []).append(addr)
            save(path, st)
            say(f"Successfully paired to {addr} [guid=adb-FAKE-guid]")
        say("Failed: Wrong password or connection was dropped.", 1)
    if args[:1] == ["connect"]:
        addr = args[1]
        dev = (st.get("reachable") or {}).get(addr)
        if dev is None:
            say(f"failed to connect to '{addr}': Connection refused", 1)
        if not any(x["serial"] == addr for x in st["devices"]):
            st["devices"].append({**dev, "serial": addr})
            save(path, st)
        say(f"connected to {addr}")
    if args[:1] != ["-s"]:
        say(f"fakeadb: not understood: {args}", 1)
    serial, rest = args[1], args[2:]
    d = device(st, serial)
    if rest[:2] == ["shell", "getprop"]:
        say("".join(f"[{k}]: [{v}]\n" for k, v in d.get("props", {}).items()))
    if rest[:3] == ["shell", "dumpsys", "battery"]:
        say(f"Current Battery Service state:\n  AC powered: false\n  level: {d.get('battery', 50)}\n  scale: 100\n")
    if rest[:2] == ["shell", "pidof"]:
        pid = (d.get("pids") or {}).get(rest[2])
        say(pid or "", 0 if pid else 1)
    if rest[:2] == ["shell", "monkey"]:
        app = rest[rest.index("-p") + 1]
        if app not in d.get("apps", [app]):
            say("  bash arg: -p\n** No activities found to run, monkey aborted.", 251)
        d.setdefault("pids", {}).setdefault(app, str(4000 + len(d["serial"])))
        save(path, st)
        say("  bash arg: -p\n  bash arg: " + app + "\nEvents injected: 1\n## Network stats: elapsed time=12ms")
    if rest[:3] == ["shell", "am", "force-stop"]:
        (d.get("pids") or {}).pop(rest[3], None)
        save(path, st)
        say("")
    if rest[:1] == ["install"]:
        if serial in st.get("install_fails", []):
            say("Performing Streamed Install\nadb: failed to install app.apk: Failure [INSTALL_FAILED_INSUFFICIENT_STORAGE]", 1)
        d.setdefault("installed", []).append(rest[-1])
        save(path, st)
        say("Performing Streamed Install\nSuccess")
    if rest[:3] == ["exec-out", "screencap", "-p"]:
        sys.stdout.buffer.write(png())
        sys.stdout.flush()
        sys.exit(0)
    if rest[:1] == ["logcat"]:
        log = os.path.join(os.path.dirname(path), d.get("logcat", f"logcat-{serial.replace(':', '_')}.txt"))
        pos, tick = 0, 0
        stop = path + ".stop"
        while not os.path.exists(stop):
            tick += 1
            if os.path.exists(log):
                with open(log, encoding="utf-8") as f:
                    f.seek(pos)
                    chunk = f.read()
                    pos = f.tell()
                if chunk:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
            if tick % 10 == 0 and load(path).get("gone", {}).get(serial):
                sys.exit(1)
            time.sleep(0.05)
        sys.exit(0)
    say(f"fakeadb: not understood: {args}", 1)


# --------------------------------------------------------- for the tests

HYROX_PHONE = "R5CT10AB1234"
HYROX_WATCH = "192.168.1.42:41235"
APP_ID = "com.mgilli.hyroxtracker"


def world():
    """A phone over USB, a watch over Wi-Fi, an emulator, an unauthorized
    and an offline device — the models Hyrox's /deploie names."""
    return {
        "devices": [
            {"serial": HYROX_PHONE, "state": "device", "model": "SM_S928B", "usb": True, "battery": 76,
             "props": {"ro.serialno": HYROX_PHONE, "ro.product.model": "SM-S928B", "ro.build.characteristics": "phone",
                       "ro.build.version.release": "15", "ro.build.version.sdk": "35"},
             "pids": {APP_ID: "4321"}},
            {"serial": HYROX_WATCH, "state": "device", "model": "SM_L705F", "battery": 58,
             "props": {"ro.serialno": "RFAX20WATCH9", "ro.product.model": "SM-L705F",
                       "ro.build.characteristics": "nosdcard,watch", "ro.build.version.release": "14",
                       "ro.build.version.sdk": "34"}},
            {"serial": "emulator-5554", "state": "device", "model": "sdk_gphone64_x86_64", "battery": 100,
             "props": {"ro.serialno": "EMULATOR37X1X11X0", "ro.product.model": "sdk_gphone64_x86_64",
                       "ro.kernel.qemu": "1", "ro.build.characteristics": "emulator",
                       "ro.build.version.release": "16", "ro.build.version.sdk": "36"}},
            {"serial": "R3CN70UNAUTH", "state": "unauthorized", "usb": True},
            {"serial": "0123456789OFF", "state": "offline"},
        ],
        "pair_code": "123456",
        "reachable": {"192.168.1.42:39999": {"state": "device", "model": "SM_L705F", "battery": 57,
                                             "props": {"ro.serialno": "RFAX20WATCH9", "ro.product.model": "SM-L705F",
                                                       "ro.build.characteristics": "nosdcard,watch",
                                                       "ro.build.version.release": "14", "ro.build.version.sdk": "34"}}},
        "mdns": ["adb-RFAX20WATCH9-Xy12Ab\t_adb-tls-connect._tcp\t192.168.1.42:39999",
                 "adb-RFAX20WATCH9-Xy12Ab\t_adb-tls-pairing._tcp\t192.168.1.42:37011"],
        "mdns_works": True,
    }


class FakeAdb:
    """The fake adb of one test: its state file in `folder`, the argv the
    adapter runs, and the calls it got."""

    def __init__(self, folder, st=None):
        os.makedirs(folder, exist_ok=True)
        self.folder = str(folder)
        self.path = os.path.join(self.folder, "adb-state.json")
        save(self.path, st if st is not None else world())
        open(self.path + ".calls", "w").close()
        self.argv = [sys.executable, os.path.abspath(__file__), self.path]

    def state(self):
        return load(self.path)

    def update(self, fn):
        st = load(self.path)
        fn(st)
        save(self.path, st)

    def calls(self):
        with open(self.path + ".calls", encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]

    def logcat(self, serial, *lines):
        """Appends lines to the device's logcat, as the device writes them."""
        name = os.path.join(self.folder, f"logcat-{serial.replace(':', '_')}.txt")
        with open(name, "a", encoding="utf-8") as f:
            for x in lines:
                f.write(x + "\n")

    def command(self, *args):
        """A shell command running this fake adb — for a profile's install."""
        q = lambda x: f'"{x}"'
        return " ".join([q(sys.executable), q(os.path.abspath(__file__)), q(self.path), *args])

    def close(self):
        open(self.path + ".stop", "w").close()


def threadtime(pid, level, tag, msg, t="10-06 10:00:00.000"):
    return f"{t}  {pid:>5}  {pid:>5} {level} {tag}: {msg}"


if __name__ == "__main__":
    main(sys.argv[1:])
