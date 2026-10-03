---
description: Install both applications on the physical phone and watch
allowed-tools: PowerShell
---

Deploy both applications to the physical devices. **You install, you
report — you fix nothing.**

---

## 1. Find the devices

    adb devices -l

🔴 **Identify each one by its model, never by its position in the
list.**

| Device | Model |
|---|---|
| Phone | `model:SM_S928B` |
| Watch | `model:SM_L705F` |

📌 **The identifier is the first column.** ⚠️ **The watch's changes
every time wireless debugging restarts** — 🔴 **read it again every
run, never from memory or from an earlier report.**

**A device missing** — 🔴 **stop and say which one** — `Next: stop
<device> missing`. ⚠️ **Do not
install the other one alone**: a phone updated against an old watch
build fails in ways that read as code defects.

---

## 2. Install

🔴 **Every command below runs through the `PowerShell` tool** — ⚠️
**never Bash, which rejects each of them.**

🔴 **In PowerShell the variable goes on its own line, before the
command** — set on the same line it does not reach Gradle.

    $env:ANDROID_SERIAL = "<phone identifier>"
    .\gradlew :app-phone:installDebug

    $env:ANDROID_SERIAL = "<watch identifier>"
    .\gradlew :app-wear:installDebug

    Remove-Item Env:\ANDROID_SERIAL

📌 **One command at a time, in the foreground, and you wait for it.**
⚠️ **Never launch a build in the background and poll** — two runs fight
over the same lock, and a shell nobody awaits keeps running after you
are done.

🔴 **Clear the variable at the end**, whatever happened. ⚠️ **Left set,
it sends the next command in this session to the wrong device.**

---

## 3. Report

**One line per device**: which module, which identifier, build passed
or not.

🔴 **Name any error, do not correct it.** ⚠️ **A failed install is a
result** — the report says what failed and stops there.

🔴 **The report ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **`Next: done`**: what the Product Owner tests on the devices is
hers.
