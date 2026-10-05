## What I need

A working `local.properties` (`sdk.dir`) present, or an `ANDROID_HOME` /
`ANDROID_SDK_ROOT` environment variable set, before `./gradlew check` can
even configure the Android modules.

## Why the lot cannot proceed

`local.properties` is git-ignored and absent from a fresh worktree; no
environment variable names an SDK location either. Every Gradle task
touching `:app-phone` or `:app-wear` fails at configuration time with
"SDK location not found", before a single line of test code runs — this
blocks running `./gradlew check` at all, for this lot or any other.

## Where I met it

Running `./gradlew :app-phone:testDebugUnitTest` from this worktree's
root, right after implementing this lot's own `:core-domain` change.

## What I think it is

add — a documented, reproducible way to point Gradle at the machine's
Android SDK (an environment variable set for every session, or a
generated `local.properties` step) before any lot's `./gradlew check`
runs. I worked around it for this run by writing
`C:/Users/MGILLI/AppData/Local/Android/Sdk` into a local
`local.properties`, found by browsing the standard install path — this
is machine-specific and not something the next session can rely on
finding the same way.

## Verdict

**Not a convention. It belongs to the machine.** No rule written.

It fails two of the three filters at once:

- 🔴 **The platform imposes it.** The Android Gradle plugin reads the SDK
  location from `sdk.dir` in `local.properties` or from
  `ANDROID_HOME` / `ANDROID_SDK_ROOT`, and from nowhere else. There is no
  other way, so there is nothing for this project to choose.
- 🔴 **It holds on one machine only.** A filesystem path and an
  environment variable are the two examples the filter names. The value
  you found, `C:/Users/MGILLI/AppData/Local/Android/Sdk`, is true of one
  installation and of no other.

📌 **`local.properties` is git-ignored on purpose** — Android's own
documentation reserves that file for the plugin's machine-local values.
Committing it, or writing a rule that names a path, would put one
machine's layout into every checkout.

**Where it belongs**: the environment the agents run in — `ANDROID_HOME`
set once for the session, or a `local.properties` generated before the
first `./gradlew` call. That is a decision for the Product Owner's
machine setup and for the run harness, not for this file, and it is
worth raising there since it blocks every lot equally.
