## What I need

A way to get a deterministic, reproducible `:app-wear:check`/
`:app-wear:testDebugUnitTest` run in this worktree, or a documented
recovery step after a Gradle/Kotlin daemon is interrupted mid-test-run.

## Why the lot cannot proceed

It does proceed — this lot's own code and tests are complete and
verified in isolation. Only the full, unscoped `:app-wear:check` cannot
be trusted in this session: after one run hung (see below), every
subsequent attempt at the full module check fails on a different
infrastructure-level error uncorrelated with any specific test class —
a `ClassNotFoundException` on every test class uniformly, an
incremental-compiler "could not delete ... classes\com" clash, a build
reporting "Gradle build daemon has been stopped: stop command received"
with no `--stop` issued in that window, and a bare `java.io.EOFException`
failing in ~10s even at `--max-workers=1`. `./gradlew --stop` between
attempts changes which error appears next but never restores a clean
full run.

## Where I met it

Running `./gradlew :app-wear:check` for lot-43
(`docs/features/premiere-app/bugfix-06/code/lot-43`). The session's
first such run hung indefinitely (silently consuming a CPU core) on a
test this lot itself wrote that opened a session-backed `RaceTicker`
inside a `runTest` sharing `Dispatchers.Main` without ever closing it —
the trap already on record in `CURRENT_TECHNICAL_STATE.md` under
"A `RaceTicker` opened but never closed inside a `runTest` sharing
`Dispatchers.Main` hangs the whole test JVM, silently". That test is
fixed. Every full-module run attempted after stopping that hang shows
the symptoms above; `./gradlew :app-wear:testDebugUnitTest --tests`
scoped to only this lot's five test classes (42 tests) passes clean and
reproducibly on the same worktree, same daemon state.

## What I think it is

update — `CURRENT_TECHNICAL_STATE.md`'s existing `RaceTicker`/
`Dispatchers.Main` trap entry to add: once such a hang has occurred and
its daemon is stopped mid-run, the worktree's Gradle/Kotlin daemon and
incremental-compile state stay unreliable for the full module check
for the rest of the session — only a scoped `--tests` run against the
specific classes a lot touches is trustworthy afterward, until
something (a fresh worktree, a full daemon/cache reset outside this
role's permitted commands) clears it.

## Verdict

**Not a convention. It belongs to `CURRENT_TECHNICAL_STATE.md`, which
this agent does not write.** No rule added to
`docs/TECHNICAL_CONVENTIONS.md`.

It fails the same filter as `realisateur-lot-01.md`'s SDK-path request:

- 🔴 **It holds on one session only.** What is reported is not a
  portable build choice but the state of one Gradle/Kotlin daemon, in
  one worktree, after one specific hang — `ClassNotFoundException`
  uniformly, an incremental-compiler delete clash, a daemon stopping
  itself, a bare `EOFException`, none tied to a test's own content.
  Checked against Gradle's own troubleshooting guidance and its issue
  tracker rather than recalled: daemon-state corruption after an
  abnormal stop is a documented category of problem there, with `stop`
  and a fresh daemon as the standard remedy, and no stable rule to
  write down beyond that — the exact symptom sequence is a property of
  this daemon's corrupted state, not of the codebase.
- 🔴 **No platform mechanism turns it into a project choice.** Gradle
  does not offer a "scoped-tests-only, full-check-untrustworthy" mode
  to opt into; there is nothing here for the project to standardise on
  beyond what R4 already requires (`./gradlew check` exits 0).

**No tool of R65's table checks it either** — this is a build-tool
reliability report, not a rule about the code.

**Where it belongs.** The request's own "What I think it is" already
names the right destination: `CURRENT_TECHNICAL_STATE.md`'s existing
`RaceTicker`/`Dispatchers.Main` trap entry, which the Détailleur and
the Réalisateur read and write — not this file, and not this agent.
The addition it proposes (once that hang has happened, only a
`--tests`-scoped run against the touched classes is trustworthy for the
rest of the session) is exactly the shape of a runtime trap that file
already carries other entries for.
