## Signatures

SensorPermissionUiState(
  title: LabelRef, explanation: LabelRef, actionLabel: LabelRef
)
  — `resolvedState` dropped. The three labels are the whole state, are
    never null, and never change over the screen's life.

SensorPermissionViewModel(
  sensorPermissionManager: SensorPermissionManager,
  navigator: WatchRaceNavigator
) : ViewModel
  — `@HiltViewModel`, `@Inject` constructor; both parameters unchanged.

SensorPermissionViewModel.uiState: StateFlow<SensorPermissionUiState>
  — one value for the screen's whole life, carrying
    WatchStringResources.Permission.title / .explanation / .action;
    never null, and nothing in the class re-emits it.

SensorPermissionViewModel.init
  — inside `viewModelScope.launch`: reads
    `SensorPermissionManager.isFirstLaunch()`, then calls
    `SensorPermissionManager.onLaunch()`. The `SensorPermissionState`
    `onLaunch()` returns is no longer read. Calls
    `WatchRaceNavigator.onSensorPermissionResolved()` exactly when
    `isFirstLaunch()` returned true, never otherwise.

SensorPermissionViewModel.onActionClicked() → Unit
  — inside `viewModelScope.launch`: calls
    `SensorPermissionManager.requestAgain()`. On
    `SensorPermissionRequestOutcome.Resolved` — `Granted` and
    `Fallback` alike — calls
    `WatchRaceNavigator.onSensorPermissionResolved()`; `outcome.state`
    is no longer read. On
    `SensorPermissionRequestOutcome.RedirectedToSettings` calls
    nothing.

SensorPermissionViewModel.onResumed() → Unit
  — not suspend; returns immediately. Both the
    `SensorPermissionManager.isGranted()` read and the navigator call
    run inside `viewModelScope.launch`, never on the caller's thread.
    Calls `WatchRaceNavigator.onSensorPermissionResolved()` exactly
    when `isGranted()` returns true, and nothing at all otherwise.
    Never calls `SensorPermissionManager.requestAgain()`.

SensorPermissionScreen(viewModel: SensorPermissionViewModel)
  — signature unchanged; it renders the three labels and reaches
    `onActionClicked()` from the action pill and `onResumed()` from
    `LifecycleEventEffect(Lifecycle.Event.ON_RESUME)`. It reads no
    resolved permission state today and reads none after.

## Acceptance criteria

- With the ViewModel's `Dispatchers.Main` set to a paused test
  dispatcher, `onResumed()` returns with `SensorPermissionManager
  .isGranted` not yet called; once the dispatcher runs, it has been
  called exactly once.
- `onResumed()` on a granted permission calls
  `WatchRaceNavigator.onSensorPermissionResolved()` exactly once, once
  the dispatcher runs.
- `onResumed()` on a refused permission calls neither
  `onSensorPermissionResolved()` nor `SensorPermissionManager
  .requestAgain()`.
- `SensorPermissionUiState` carries exactly `title`, `explanation` and
  `actionLabel`; no file in `:app-wear` reads a resolved sensor
  permission state from it, tests included.
- `uiState.value` is equal to its initial value after each of: init
  completing on a first-ever launch, init completing on a later launch,
  `onActionClicked()` resolving to `Granted`, `onActionClicked()`
  resolving to `Fallback`, and `onResumed()` finding the permission
  granted.
- On a first-ever launch, init calls `SensorPermissionManager
  .onLaunch()` exactly once and `onSensorPermissionResolved()` exactly
  once.
- On a later launch, init calls `SensorPermissionManager.onLaunch()`
  exactly once and `onSensorPermissionResolved()` never.
- `onActionClicked()` on `Resolved(Granted)` and on
  `Resolved(Fallback)` each call `onSensorPermissionResolved()` exactly
  once.
- `onActionClicked()` on `RedirectedToSettings` calls
  `onSensorPermissionResolved()` never.
- `SensorPermissionScreen` renders the texts behind `title`,
  `explanation` and `actionLabel`; tapping the action pill reaches
  `onActionClicked()`, and an ON_RESUME lifecycle event reaches
  `onResumed()`.

## Dependencies

SensorPermissionManager — pre-existing:
  `isFirstLaunch(): Boolean`, `isGranted(): Boolean`,
  `suspend onLaunch(): SensorPermissionState`,
  `suspend requestAgain(): SensorPermissionRequestOutcome`
SensorPermissionState — pre-existing: `Granted`, `Fallback`
SensorPermissionRequestOutcome — pre-existing:
  `Resolved(state: SensorPermissionState)`, `RedirectedToSettings`
WatchRaceNavigator.onSensorPermissionResolved(): Unit — modified by
  lot-34 of this cycle; not suspend, moves SENSOR_PERMISSION to
  WAITING_FOR_PHONE and is a no-op on every other destination. Reused,
  never redeclared.
LabelRef — pre-existing (`:core-domain`)
WatchStringResources.Permission.title / .explanation / .action —
  pre-existing
StateFlow, viewModelScope, LifecycleEventEffect — framework

Trap carried by these symbols: a plain JVM test constructing
`SensorPermissionViewModel` needs `Dispatchers.setMain(...)` in
`@Before` and `Dispatchers.resetMain()` in `@After` — the class touches
`viewModelScope` in its own `init`.

## Conventions

R4 · `./gradlew check` exits 0, no other definition of done
R74 · a call site of a changed signature inside `:app-wear` is this
  lot's own scope — `SensorPermissionViewModelTest`,
  `SensorPermissionViewModelResumeTest` and any other reader of
  `resolvedState` are converted here, never deferred
R12 · §9.7's symbols stay in `:app-wear`
R42 · cooperative async on coroutines, no shared mutable state between
  coroutines
R47 · a screen reads a source once per entry, never once per frame
R55 · one nominal and one failure test per public function, in this lot
R62 · the lexicon — Permission, Sensor, Fallback; no synonym
R63 · English identifiers and comments; every exported symbol carries
  one line saying what it guarantees and when it fails
R64 · no user-facing string literal in the code; the three labels stay
  `LabelRef`s into the watch catalogue

## Requests

—
