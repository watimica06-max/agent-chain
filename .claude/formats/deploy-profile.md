# The deploy profile — `.claude/deploy.json`

The contract between an application and the cockpit's « Déploiement »
screen (cockpit 1.8, `docs/app/TECHNICAL_V1.md` §23 of the chain's
repository). Whoever writes a profile reads this file: the Product Owner in
Paramètres → Déploiement today, an agent of the chain later, when it builds
a new application's skeleton.

- **Where**: `.claude/deploy.json`, at the application's root. It belongs
  to the application: the chain's install never writes, removes or reads it
  (the cockpit's `chain.py`, `PATHS`). This format is the chain's, and the
  install brings it.
- **Who reads it**: the cockpit's `deploy_profile.py`, which checks every
  field below; its adapters, in `adapters/`.
- **Saved from the cockpit**: written as UTF-8 JSON, two-space indented, its
  keys in the order below; committed alone in the application —
  `deploy: profil` — and pushed. A file written by hand is read the same way.
- **Refused, said in French**: a key this contract does not name (a typo is
  never ignored), a required field empty, a value not offered, two targets
  of one name, a `format` other than 1.

---

## 1. The file

```
{
  "format": 1,
  "targets": [ … ]
}
```

| Key | Required | What it is |
|---|---|---|
| `format` | no — 1 when absent | The contract's version. This file describes format 1. |
| `targets` | yes | The targets, in the order the page lists them and a deploy runs them. Empty: nothing to deploy. |

## 2. A target — the frame

Every target holds these three fields, whatever its type.

| Key | Required | What it is |
|---|---|---|
| `name` | yes | The name the page shows — « Téléphone », « Montre », « Site ». 40 characters at most; two targets never share one (case ignored). |
| `type` | yes | The adapter: `android` or `commande`. It says which other fields the target holds. |
| `build` | no — empty when absent | The command that builds the target, run once per deploy from the application's root, before anything is deployed. Empty: nothing to build. It runs in `cmd.exe` on Windows: `.\gradlew.bat`, not `./gradlew`. A failed build skips that target's deploys and launches. |

Every other key belongs to the adapter.

## 3. `android`

A target installed on Android devices through adb — over USB, over Wi-Fi,
or on an emulator.

| Key | Required | What it is |
|---|---|---|
| `kind` | yes | Which devices are offered for this target: `phone` — a phone, or a phone emulator; `watch` — a device whose `ro.build.characteristics` holds `watch`, a watch emulator included; `any` — every device. |
| `install` | yes | The command that installs the target on one device, run from the application's root, once per device chosen. `{serial}` in it is replaced by the device's adb serial; a command without `{serial}` gets the device in the `ANDROID_SERIAL` environment variable, which Gradle's `install*` tasks and adb itself read. Exit code 0 is success. |
| `app_id` | no | The application's id — Gradle's `applicationId`. When given, the application is launched after its install (`adb shell monkey -p <app_id> -c android.intent.category.LAUNCHER 1`), « Lancer » and « Arrêter » are offered on each device, and the journal keeps the application's processes alone. Empty: nothing is launched, and the journal shows the whole device. |

Example — two modules, a phone and a watch, the device passed as
`ANDROID_SERIAL`:

```json
{
  "format": 1,
  "targets": [
    {
      "name": "Téléphone",
      "type": "android",
      "build": ".\\gradlew.bat :app-phone:assembleDebug",
      "kind": "phone",
      "install": ".\\gradlew.bat :app-phone:installDebug",
      "app_id": "com.exemple.application"
    },
    {
      "name": "Montre",
      "type": "android",
      "build": ".\\gradlew.bat :app-wear:assembleDebug",
      "kind": "watch",
      "install": ".\\gradlew.bat :app-wear:installDebug",
      "app_id": "com.exemple.application"
    }
  ]
}
```

Example — an APK built once, installed with adb and `{serial}`, on any
device:

```json
{
  "format": 1,
  "targets": [
    {
      "name": "Application",
      "type": "android",
      "build": "flutter build apk --debug",
      "kind": "any",
      "install": "adb -s {serial} install -r build\\app\\outputs\\flutter-apk\\app-debug.apk",
      "app_id": "com.exemple.application"
    }
  ]
}
```

## 4. `commande`

A target whose deploy is a command run on this computer — a web server, a
desktop program, a script. One destination: « cet ordinateur ».

| Key | Required | What it is |
|---|---|---|
| `run` | yes | The command, run from the application's root. Its output — standard output and errors — is the target's journal. |
| `keeps_running` | no — `false` | `true`: the command keeps running (a server, a program). Still running three seconds after its start, it is deployed; « Arrêter » stops it, with every process it started; deploying again stops it and starts it anew. `false`: the command ends (a script); it is waited for, an hour at most, and its exit code 0 is success. |
| `url` | no | An address in `http://` or `https://`. While the command runs, « Ouvrir » opens it in the browser. |

Example — a local web server:

```json
{
  "format": 1,
  "targets": [
    {
      "name": "Site",
      "type": "commande",
      "build": "npm run build",
      "run": "python -m http.server 8000 --directory dist",
      "keeps_running": true,
      "url": "http://127.0.0.1:8000/"
    }
  ]
}
```

Example — a Python tool, run once, nothing to build:

```json
{
  "format": 1,
  "targets": [
    {
      "name": "Outil",
      "type": "commande",
      "run": "python outil.py --verifier",
      "keeps_running": false
    }
  ]
}
```
