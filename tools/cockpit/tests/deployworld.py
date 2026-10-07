"""The world of the 1.8 tests and screenshots: a fake adb with Hyrox's
devices, and an application whose profile deploys to them with commands that
touch nothing — the build prints, the install is the fake adb's."""
import json
import os
import sys

from adapters import android
from fakeadb import APP_ID, FakeAdb

PY = f'"{sys.executable}"'


def say(text, code=0):
    """A shell command that prints `text` and ends with `code`."""
    return f'{PY} -c "import sys; print({text!r}); sys.exit({code})"'


def hyrox_targets(fa, build_fails=False):
    """Hyrox's profile (docs/app/TECHNICAL_V1.md §23.1), its Gradle commands
    replaced by commands that only print, its install by the fake adb's."""
    return [
        {"name": "Téléphone", "type": "android",
         "build": say("BUILD app-phone: assembleDebug", 1 if build_fails else 0),
         "kind": "phone", "install": fa.command("-s", "{serial}", "install", "-r", "app-phone-debug.apk"),
         "app_id": APP_ID},
        {"name": "Montre", "type": "android", "build": say("BUILD app-wear: assembleDebug"),
         "kind": "watch", "install": fa.command("-s", "{serial}", "install", "-r", "app-wear-debug.apk"),
         "app_id": APP_ID},
    ]


def write_profile(app_root, targets):
    p = os.path.join(str(app_root), ".claude", "deploy.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"format": 1, "targets": targets}, f, ensure_ascii=False, indent=2)
    return p


def use_fake_adb(folder, monkeypatch=None, emulator=False, scrcpy=False):
    """The android adapter talks to a fake adb; the emulator and scrcpy are
    absent unless asked, and then fakes that only print."""
    fa = FakeAdb(folder)
    values = {"ADB": fa.argv,
              "EMULATOR": [sys.executable, "-c", "import sys; print('Pixel_8'); print('Wear_OS_Large_Round')"] if emulator else False,
              "SCRCPY": [sys.executable, "-c", "print('scrcpy')"] if scrcpy else False}
    for k, v in values.items():
        if monkeypatch is not None:
            monkeypatch.setattr(android, k, v)
        else:
            setattr(android, k, v)
    return fa
