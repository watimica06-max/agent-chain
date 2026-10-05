# blocked_detailleur — lot-49

## What blocks

§4.4 requires a cold launch from a complication tap to open the
destination the extra carries, but `WatchRaceNavigator`'s first-access
asynchronous race-in-progress check — §4.3, built by lot-34 — sets
`current` to `MAIN` unconditionally once it resolves, and no entry says
which of the two wins, so a tap carrying `PROJECTION`, `CONTROL` or
`END` after a process death has no determined outcome.

## Where

Lot-49, anchor §4.4 read against §4.3.

- `desc-bug.md` §4.4: "`onCreate` reads the same extra off its own
  launch intent, navigating to the carried destination on both paths."
- `desc-bug.md` §4.3: the first-read destination "also accounts for a
  race in progress, chosen ahead of the profile-sync/sensor-permission
  checks."
- `app-wear/src/main/java/com/mgilli/app_wear/MainActivity.kt` —
  `onCreate`, and `onNewIntent`'s existing
  `navigator.navigateTo(WatchDestination.valueOf(extra))`.
- `app-wear/src/main/java/com/mgilli/app_wear/race/WatchRaceNavigator.kt`
  lines 40–52 — `mutableCurrent`'s `by lazy` initialiser launches, on
  `scope`, `if (raceInProgress()) flow.value = WatchDestination.MAIN`.
  `navigateTo` (line 141) writes the same `MutableStateFlow` and is
  itself a first access, so it triggers that launch and is then
  overwritten when the coroutine resolves.
- `app-wear/src/main/java/com/mgilli/app_wear/race/WatchComplicationEntry.kt`
  — `entryPoint(current).destination` mirrors whatever page was showing,
  so the extra can carry `PROJECTION`, `CONTROL` or `END`, not only
  `MAIN`.

The path is reachable: the complication is only published while a race
is in progress, so on every complication-tap cold start `raceInProgress()`
resolves true. It is masked today only because `findInProgress()` finds
nothing after a process death; lot-50 (§2.6, §2.7) makes it find the
race, and lot-50 runs after lot-49.

A criterion written on `navigator.current` immediately after `onCreate`
returns would pass under the module's test fakes — no race in progress,
so the check never fires — while the shipped application still opens
`MAIN`. That is a criterion that proves the wiring and not the
behaviour, so lot-49 cannot be detailed against it.

## To resume

State which wins on a cold launch carrying a destination extra, with a
race in progress:

1. the tapped destination — the complication resumes into the page it
   was showing, and §4.3's `MAIN` default applies only to a launch
   carrying no extra; or
2. `MAIN` — §4.3's race-in-progress default wins over the extra, and
   §4.4's "carried destination" holds for the `onNewIntent` path only.

If the answer is (1), also say whether `WatchRaceNavigator` is in
lot-49's scope for it: the lot declares `MainActivity`, `WatchApp`,
`AlwaysOnDisplayController`, `DisplayModule`, `AndroidManifest.xml` and
`MainActivityHomeAndRaceScreensTest` as modified, and `WatchRaceNavigator`
is not among them, so nothing in lot-49 can currently keep the tapped
destination from being overwritten.

## Decision

Take answer (1): a cold launch carrying a destination extra opens the
carried destination, and lot-49 carries `WatchRaceNavigator` and
`WatchRaceNavigatorTest` in its own sheet to make it hold. The
asynchronous check launched at `current`'s first access writes
`WatchDestination.MAIN` or `WatchDestination.HOME` only while
`mutableCurrent.value` is still the value the `by lazy` initialiser
computed — `SENSOR_PERMISSION` or `WAITING_FOR_PHONE` — and leaves
`current` unchanged on every other destination, so a `navigateTo` issued
from `onCreate` before the check resolves stands.

§4.4 states it: `onCreate` "reads the same extra off its own launch
intent, navigating to the carried destination on both paths" — a cold
launch is one of those two paths, and §4.3's `MAIN` answers the launch
that carries no extra, which is the case its own symptom describes
("a race that survives process death still opens on the home screen").
R46 says the same for the user: the application resumes from what it
read, and `WatchComplicationEntry.entryPoint(current).destination` is
that record. Guarding the write on the destination `current` currently
holds is how every other transition of the class already works —
`onSensorPermissionResolved`, `onProfileSynced`, `onMarked`, `onUndo`,
`launchRace` and `checkInactivity` each write only from a named source
destination; the `by lazy` block is the one unconditional writer.
Carrying the file here conflicts with nothing: `decoupage.md` line 559
is the only `Modifies:` line naming `WatchRaceNavigator`, lot-34 is
PASS, and `sequence.md` puts lot-49 alone in block-19.

This does not extend beyond that guard. `NavigationModule`, the
synchronous first-read computation, `navigateTo`'s signature,
`onSensorPermissionResolved`, `onProfileSynced` and `checkInactivity`
stay as lot-34 left them — `WAITING_FOR_PHONE` remains inside the
guarded set, so the check still moves a start-up flow on to `MAIN` or
`HOME` once it resolves, and `WatchRaceNavigatorTest`'s existing
race-in-progress case still settles on `MAIN`. The cold-launch
criterion for §4.4 goes in `WatchRaceNavigatorTest` — a race in
progress, `navigateTo(PROJECTION)` before the check resolves, `current`
still `PROJECTION` after — while `MainActivityHomeAndRaceScreensTest`
keeps proving only that `onCreate` reads the extra. `decoupage.md`'s
lot-49 `Modifies:` line takes the two added files.

## Applied

Applied by the Détailleur on 2026-09-06 in `fiche-executable.md`, and
`decoupage.md`'s lot-49 `Modifies:` line now names `WatchRaceNavigator`
and `WatchRaceNavigatorTest`.
