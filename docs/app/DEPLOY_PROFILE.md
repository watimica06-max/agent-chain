# The deploy profile — `.claude/deploy.json`

The contract between an application and the cockpit's « Déploiement »
screen (cockpit 1.8, `TECHNICAL_V1.md` §23). Whoever writes a profile reads
this file: the Product Owner in Paramètres → Déploiement today, an agent of
the chain later, when it builds a new application's skeleton.

- **Where**: `.claude/deploy.json`, at the application's root. It belongs
  to the application: the chain's install never writes, removes or reads it
  (`tools/cockpit/chain.py` `PATHS`).
- **Who reads it**: `tools/cockpit/deploy_profile.py`, which checks every
  field below; the adapters in `tools/cockpit/adapters/`.
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
`ANDROID_SERIAL` (Hyrox's profile, §5):

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
      "app_id": "com.mgilli.hyroxtracker"
    },
    {
      "name": "Montre",
      "type": "android",
      "build": ".\\gradlew.bat :app-wear:assembleDebug",
      "kind": "watch",
      "install": ".\\gradlew.bat :app-wear:installDebug",
      "app_id": "com.mgilli.hyroxtracker"
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

## 5. Hyrox's profile, derived

From `C:\Dev\hyrox_tracker\.claude\commands\deploie.md` — the command the
profile replaces — and, where that file says nothing, from the modules'
Gradle files.

| Target · key | Value | From |
|---|---|---|
| Téléphone · `kind` | `phone` | deploie.md:20 — « Phone \| `model:SM_S928B` » |
| Téléphone · `install` | `.\gradlew.bat :app-phone:installDebug`, device in `ANDROID_SERIAL` | deploie.md:42-43 |
| Téléphone · `build` | `.\gradlew.bat :app-phone:assembleDebug` | not in deploie.md: `installDebug` builds before it installs. `assembleDebug` is the build `installDebug` depends on, run once so that a build failure is told apart from an install failure; `installDebug` then finds it up to date on each device |
| Téléphone · `app_id` | `com.mgilli.hyroxtracker` | not in deploie.md: `app-phone/build.gradle.kts:15` |
| Montre · `kind` | `watch` | deploie.md:21 — « Watch \| `model:SM_L705F` » |
| Montre · `install` | `.\gradlew.bat :app-wear:installDebug`, device in `ANDROID_SERIAL` | deploie.md:45-46 |
| Montre · `build` | `.\gradlew.bat :app-wear:assembleDebug` | as the phone's |
| Montre · `app_id` | `com.mgilli.hyroxtracker` | not in deploie.md: `app-wear/build.gradle.kts:15` — the same id as the phone's |

`.\gradlew` (deploie.md:43) becomes `.\gradlew.bat`: the command runs in
`cmd.exe`, not PowerShell. Three rules of deploie.md are not in the profile:
the model of each device (:18-21) — a target names a kind, and the page
shows each device's model; « never install one alone » (:28-30) — the
Product Owner chooses the devices; clearing `ANDROID_SERIAL` (:48, :55-56) —
the cockpit sets it on the install's process alone, never on its own.
