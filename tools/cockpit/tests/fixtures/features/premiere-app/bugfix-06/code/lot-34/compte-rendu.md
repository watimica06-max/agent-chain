## Symbols

WatchRaceNavigator(sensorPermissionGranted, profileAlreadySynced, raceInProgress, scope) — modified, replaces the previous `(() -> Boolean, Boolean)` constructor and its two-Boolean secondary constructor (removed, no compatibility overload — Product Owner decision on the blocking file)
WatchRaceNavigator.current — modified, first read now settles synchronously on SENSOR_PERMISSION/WAITING_FOR_PHONE, then is asynchronously overwritten to MAIN or HOME once raceInProgress/profileAlreadySynced resolve
WatchRaceNavigator.onProfileSynced() — created
WatchRaceNavigator.checkInactivity(nowElapsedRealtime) — modified, boundary now strict (`>`) instead of inclusive (`>=`): exactly 8000ms leaves current unchanged, 8001ms moves it to MAIN
WatchRaceNavigator.onSensorPermissionResolved() — modified, always moves SENSOR_PERMISSION to WAITING_FOR_PHONE; no longer branches on profileAlreadySynced, which is no longer readable synchronously
NavigationModule.provideWatchRaceNavigator(sensorPermissionSystem, profileRepository, raceRecordingRepository) — modified, no longer calls runBlocking; supplies profileAlreadySynced/raceInProgress as suspend reads each bounded by a 5000ms timeout (R19), and a CoroutineScope(SupervisorJob() + Dispatchers.Default) singleton scope

## Build

analyze: clean (`./gradlew :app-wear:check` — no detekt/ktlint task registered in this project; lint and static checks wired into `check` pass)
test: 358 passed, 0 failed (`:app-wear:testDebugUnitTest`)
project-wide `./gradlew check` fails only on `:app-phone:compileDebugKotlin` (`ProfileViewModel.kt`, suspend calls outside a coroutine) — pre-existing, untouched by this lot, unrelated to `WatchRaceNavigator` or any symbol this lot changes

## State

Added: —
Removed: WatchRaceNavigator's two-Boolean secondary constructor

## Requests

—
