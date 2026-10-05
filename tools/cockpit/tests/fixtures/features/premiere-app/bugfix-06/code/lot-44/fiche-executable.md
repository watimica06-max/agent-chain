## Signatures

RaceLaunchController.openPreparation(referenceRace: Race?): PreparationState
  — suspend, same shape as today; what changes is what it does before
    it answers
  — a race in progress: it reconciles first — awaits
    `exerciseSessionManager.open()`, then returns
    `PreparationState.Resuming(race)` whatever that open reported.
    `Adopted` means the session this application already owned at the
    OS level is now this instance's, and no second one starts
  — a race in progress with `DeviceSlotTaken` or `Failed`: still
    `Resuming(race)` — the in-progress race is resumed either way — and
    the outcome goes to the log at ERROR, naming the operation and
    carrying no race field (R79, R54)
  — no race in progress and `open()` reporting `Adopted`: that session
    is orphaned. It awaits `close()`, then `open()` once more, and maps
    that second outcome. One close, one reopen, in that order; a
    `close()` returning false goes to the log at ERROR and does not
    stop the reopen
  — no race in progress otherwise: today's mapping stands — `Opened`
    and `Adopted` → `Ready(referenceLoaded)`, `DeviceSlotTaken` →
    `SensorConflict`, `Failed` → `OpenFailed`
  — `referenceLoaded` comes from `referenceRace != null`, read before
    the session step and only on the no-race-in-progress path, as today
  — `findInProgress()`'s own failure keeps today's reading: no race in
    progress
  — never null: one of `PreparationState`'s four values, always

RaceLaunchController.launch(startedAt: Instant, startedAtElapsedRealtime: Long): Result<Race>
RaceLaunchController.retryAndLaunch(startedAt: Instant, startedAtElapsedRealtime: Long): Result<Race>
RaceLaunchController.confirmConflict(): PreparationState
  — unchanged, signature and behaviour

PreparationState
  — unchanged: `Resuming(race)`, `Ready(referenceLoaded)`,
    `SensorConflict`, `OpenFailed`. No cited rule adds a fifth value,
    and `PreparationViewModel.applyState` is exhaustive over this type
    in the same module, owned by lot-38 — a value added here stops
    `:app-wear` compiling, which R74 makes this lot's own scope

## Acceptance criteria

- Opening preparation while a race is in progress and the system reports a session this application already owns returns Resuming with that race, and the underlying session start is called exactly once
- Opening preparation while a race is in progress and the system reports a session this application already owns leaves the manager holding that session: a close afterwards reaches the underlying end call
- Opening preparation while a race is in progress and no session is owned returns Resuming with that race and starts one session
- Opening preparation while a race is in progress and the session start reports the device slot is held elsewhere returns Resuming with that race, never SensorConflict
- Opening preparation while a race is in progress and the session start fails returns Resuming with that race, never OpenFailed
- Opening preparation with no race in progress and a session this application already owns ends that session once and starts one again after that end, and returns Ready
- Opening preparation with no race in progress and no session owned returns Ready, starts one session, and reaches no end call
- Opening preparation with no race in progress and the device slot held elsewhere returns SensorConflict; the session start failing returns OpenFailed
- Ready carries referenceLoaded true when openPreparation is given a reference race, false when given null
- Opening preparation while findInProgress returns a failure answers by the session outcome — Ready, SensorConflict or OpenFailed — never Resuming

## Dependencies

ExerciseSessionManager.open(): ExerciseSessionOpenResult, ExerciseSessionManager.close(): Boolean (:app-wear) — created this cycle by lot-45
ExerciseSessionOpenResult — Opened, Adopted, DeviceSlotTaken, Failed; Adopted added by lot-45
RaceRecordingRepository.findInProgress(): Result<Race?> — pre-existing, still non-suspend until lot-50
PreparationState, Race — pre-existing
android.util.Log — pre-existing

No signature this lot changes reaches a call site outside it:
`openPreparation` is already suspend and `PreparationViewModel` already
awaits it inside `viewModelScope.launch`.

Two traps of `CURRENT_TECHNICAL_STATE.md` bear on this lot's tests: a
`RaceTicker` opened and never closed inside a `runTest` sharing
`Dispatchers.Main` hangs the JVM silently — `RaceLaunchControllerTest`
sets Main to the real `Dispatchers.Unconfined` for that reason, and the
orphan path's own `close()` stops the ticker it started; and a test
constructing this controller needs a stubbed Main dispatcher because of
`ExerciseSessionManager`'s injected `RaceTicker`.

## Conventions

R19 · a public operation that can block is suspend and cancellable
R24 · an operation reaching outside the process moves to its own thread inside its implementation, never on its caller's word
R34 · a caller that receives a failure acts on it — open()'s DeviceSlotTaken and Failed, close()'s false
R79 · a failure neither carried into a state this caller owns nor propagated is logged at ERROR, naming the operation
R80 · no catalogue key borrowed to report it
R53 · that log goes through android.util.Log
R54 · no race name, date or start instant in that message
R81 · a test whose subject reaches android.util.Log runs under RobolectricTestRunner
R55 · one nominal and one failure test per public function
R62 · the lexicon's terms — Race, ExerciseSession, Reference — no synonym
R63 · English, and one line per exported symbol saying what it guarantees and when it fails
R48 · what this module opens, this module releases, tied to its own scope
R12 · §5.4 is realised in :app-wear
R74 · a same-module call site broken by a signature change is this lot's own scope — this lot changes none

## Requests

—
