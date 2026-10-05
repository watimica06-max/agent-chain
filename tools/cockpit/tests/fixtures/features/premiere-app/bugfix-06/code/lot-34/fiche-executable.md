## Signatures

WatchRaceNavigator(
  sensorPermissionGranted: () -> Boolean,
  profileAlreadySynced: suspend () -> Boolean,
  raceInProgress: suspend () -> Boolean,
  scope: CoroutineScope,
) — :app-wear
  — `profileAlreadySynced`/`raceInProgress` replace the previous fixed
    `profileAlreadySynced: Boolean`; each is read once, asynchronously, on
    `scope`, the first time `current` is accessed — never blocking the
    thread that constructs this instance or reads `current`

WatchRaceNavigator.current: StateFlow<WatchDestination>
  — its first access computes an initial value synchronously from
    `sensorPermissionGranted()` alone: SENSOR_PERMISSION when false,
    WAITING_FOR_PHONE otherwise — the same branches used today minus the
    profile-sync one, which is not yet known. That same first access
    launches, on `scope`, the asynchronous read of `raceInProgress()` and
    `profileAlreadySynced()`; once it resolves, `current` is overwritten
    to MAIN when a race is in progress (ahead of every other check), else
    to HOME when the profile has synced, else left unchanged

WatchRaceNavigator.onProfileSynced(): Unit
  — leaves WAITING_FOR_PHONE for HOME; a no-op on every other destination,
    the same pattern `onSensorPermissionResolved()` already follows

WatchRaceNavigator.checkInactivity(nowElapsedRealtime: Long): WatchDestination
  — moves PROJECTION/CONTROL to MAIN once elapsed time since the last
    interaction is strictly greater than the 8000ms timeout; an elapsed
    time exactly equal to the timeout leaves `current` unchanged, matching
    the freshness windows' inclusive-boundary rule

NavigationModule.provideWatchRaceNavigator(
  sensorPermissionSystem: SensorPermissionSystem,
  profileRepository: ProfileRepository,
  raceRecordingRepository: RaceRecordingRepository,
): WatchRaceNavigator
  — no longer calls `runBlocking`; supplies `profileAlreadySynced` as a
    suspend read of `profileRepository.observe().first().lastSyncSuccessAt
    != null` and `raceInProgress` as a suspend read of
    `raceRecordingRepository.findInProgress().getOrNull() != null`, each
    bounded by a timeout (R19)

## Acceptance criteria

- With `raceInProgress()` resolving true, `current` settles on MAIN once
  resolved, whatever `profileAlreadySynced()`/`sensorPermissionGranted()`
  report
- With `raceInProgress()` resolving false and `profileAlreadySynced()`
  resolving true, `current` settles on HOME once resolved
- With `raceInProgress()` and `profileAlreadySynced()` both resolving
  false and `sensorPermissionGranted()` false, `current`'s first read is
  SENSOR_PERMISSION and stays SENSOR_PERMISSION once the asynchronous
  checks resolve
- Constructing `WatchRaceNavigator` with a `profileAlreadySynced` supplier
  that never completes does not block: `current`'s first read still
  returns immediately, on its synchronously-computed value
- `onProfileSynced()` called while `current` is WAITING_FOR_PHONE moves it
  to HOME
- `onProfileSynced()` called while `current` is any other destination
  (HOME, MAIN, …) leaves it unchanged
- `checkInactivity` called with elapsed time exactly 8000ms since the last
  interaction, on PROJECTION or CONTROL, leaves `current` unchanged
- `checkInactivity` called with elapsed time of 8001ms since the last
  interaction, on PROJECTION or CONTROL, moves `current` to MAIN

## Dependencies

RaceRecordingRepository.findInProgress — pre-existing, `Result<Race?>`, not yet suspend at this point of the sequence (converts to suspend only in lot-50)
ProfileRepository — pre-existing
WatchDestination — pre-existing
SensorPermissionSystem — pre-existing

## Conventions

R19 · every await on a store carries a timeout — `profileAlreadySynced`'s and `raceInProgress`'s reads
R24 · an operation reaching outside the process says so by being suspend, and moves to the right thread inside its own implementation
R42 · cooperative async on coroutines, no shared mutable state between coroutines — the injected `scope` is the one coroutine touching `mutableCurrent` asynchronously
R47 · a screen reads a source once per entry, remembered or collected with the lifecycle, never once per frame
R63 · naming/comments in English, doc line stating what each symbol guarantees and when it fails

## Requests

—
