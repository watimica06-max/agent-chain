## Signatures

PreparationViewModel(
  raceLaunchController: RaceLaunchController,
  raceRepository: RaceRepository,
  navigator: WatchRaceNavigator,
  sensorReadingsSource: SensorReadingsSource,
  savedStateHandle: SavedStateHandle
) : ViewModel
  — `@HiltViewModel` with a plain `@Inject` constructor, as today; no
    `@Assisted` parameter is added.
  — Adds `sensorReadingsSource` and `savedStateHandle` to the three
    existing parameters, whose order and types are unchanged.
  — Collects `sensorReadingsSource.heartRate()` on `viewModelScope`,
    calling `onHeartRateReading(reading.bpm, reading.atElapsedRealtime)`
    for every emission. The collection starts at construction and ends
    when the scope is cleared; no reading is consumed after that.
  — `savedStateHandle` carries only what a rebuild cannot recover: the
    last formatted heart-rate text, and a boolean flag for whether the
    last launch attempt was rejected. `LabelRef` is not Bundle-storable,
    so the rejection is stored as that flag and the `LabelRef` rebuilt
    from it, the way `ProjectionViewModel` already stores the primitives
    of a `LapDeltaResult.Value`. The reference race, the `opened` guard
    and the `PreparationUiState` itself are not stored — `init`
    re-derives them from `raceRepository.observeReference()` and
    `raceLaunchController.openPreparation`.

PreparationViewModel.onHeartRateReading(bpm: Int, atElapsedRealtime: Long)
  → Unit
  — Signature unchanged. What changes: the formatted text it computes is
    written to `savedStateHandle` as well as held in memory, so it
    survives a rebuild.

PreparationViewModel.onLaunchClicked(startedAt: Instant, startedAtElapsedRealtime: Long)
  → Unit
  — Signature unchanged; stays non-suspend and returns before the
    outcome is known.
  — What changes, on the `PreparationUiState.Ready` branch: the
    `raceLaunchController.launch(startedAt, startedAtElapsedRealtime)`
    call moves inside `viewModelScope.launch`, joining the
    `OpenFailed` branch, which already launches one.
  — What changes, on both branches: the `Result<Race>` returned by
    `launch` / `retryAndLaunch` is read. On success,
    `navigator.launchRace()` is called and the rejection is cleared. On
    failure, `navigator.launchRace()` is **not** called, the state keeps
    a rejection message of `WatchStringResources.Prep.launchRejected`,
    the rejected flag is written to `savedStateHandle`, and the failure
    is logged at ERROR naming the operation, without the reading, the
    race name or the start instant.
  — A click while `PreparationUiState.SensorConflict` or a null state is
    showing stays a no-op, as today.

PreparationUiState.Ready(
  heartRateText: String?,
  referenceLoadedText: LabelRef?,
  rejectionMessage: LabelRef?
)
  — Adds `rejectionMessage`, third and last. Null when no launch attempt
    has been rejected since the last successful one; never an empty
    `LabelRef`.

PreparationUiState.OpenFailed(
  heartRateText: String?,
  rejectionMessage: LabelRef?
)
  — Adds `rejectionMessage`, with the same meaning as on `Ready`.

PreparationUiState.SensorConflict
  — Unchanged; carries no rejection.

PreparationScreen(viewModel: PreparationViewModel) — @Composable
  — Signature unchanged. What changes:
    · the `Text` rendering `referenceLoadedText` sets `maxLines = 1` and
      `overflow = TextOverflow.Ellipsis`, the way `WatchHistoryScreen`
      and `HomeScreen` already bound their own race-name text;
    · `rejectionMessage`, when non-null, renders as its own `Text`
      resolved through `stringResource(label.id, *label.args…)`, on both
      the `Ready` and the `OpenFailed` branches; when null nothing is
      rendered in its place.
  — The `OpenFailed` branch keeps passing `referenceLoadedText = null`,
    as today.

## Acceptance criteria

- A `HeartRateReading(bpm = 142, …)` emitted on
  `SensorReadingsSource.heartRate()` while the preparation screen is
  showing makes that reading's formatted value appear on the screen.
- With no reading emitted, the screen shows no heart-rate value at all,
  and shows the rest of its content unchanged.
- A second reading emitted after the first replaces the displayed value
  with the second one's.
- `onLaunchClicked` returns to its caller before `launchRace()` is
  observed on the navigator; the navigation is observed only once the
  ViewModel's coroutine has run.
- With `RaceLaunchController.launch` returning success, a click while
  `Ready` is showing navigates to the race and the screen shows no
  rejection message.
- With `RaceLaunchController.launch` returning a failure, a click while
  `Ready` is showing does not navigate, and the screen shows the text of
  `WatchStringResources.Prep.launchRejected`.
- With `RaceLaunchController.retryAndLaunch` returning a failure, a click
  while `OpenFailed` is showing does not navigate, and the screen shows
  the same rejection text.
- With `RaceLaunchController.retryAndLaunch` returning success, a click
  while `OpenFailed` is showing navigates to the race and the screen
  shows no rejection message.
- A rejected launch followed by a successful one navigates, and the
  rejection message is gone from the screen.
- A reference race whose name is sixty characters renders the
  reference-loaded label on a single line, ending in an ellipsis, with
  the launch and quit controls still on screen and clickable.
- After a saved-state rebuild of the ViewModel, the heart-rate value
  last displayed is displayed again with no new reading emitted.
- After a saved-state rebuild following a rejected launch, the rejection
  message is displayed again.
- A click while the sensor-conflict dialog is showing neither navigates
  nor calls `launch` or `retryAndLaunch`.

## Dependencies

RaceLaunchController.launch(Instant, Long): Result<Race> — modified by lot-44
RaceLaunchController.retryAndLaunch(Instant, Long): Result<Race> — modified by lot-44
RaceLaunchController.openPreparation(Race?): PreparationState — modified by lot-44
SensorReadingsSource.heartRate(): Flow<HeartRateReading> — produced by lot-46
HeartRateReading(bpm: Int, atElapsedRealtime: Long) — produced by lot-46
WatchStringResources.Prep.launchRejected: LabelRef — produced by lot-18
WatchStringResources.Prep.referenceLoaded(String): LabelRef — pre-existing
WatchRaceNavigator.launchRace() / quitPreparation() — pre-existing
RaceRepository.observeReference(): Flow<Result<Race?>> — pre-existing
DisplayFormatter.formatHr(Int): String — pre-existing
LabelRef(id: Int, args: List<Any>) — pre-existing
PreparationState — pre-existing, reshaped by lot-44
androidx.lifecycle.SavedStateHandle — framework
androidx.compose.ui.text.style.TextOverflow — framework

## Conventions

R4 · `./gradlew check` exits 0
R12 · one module per group of entries
R20 · missing data crosses as a nullable or a declared absence type
R30 · no empty and no generic catch
R34 · a caller that receives a failure acts on it
R44 · one state holder per journey
R45 · a screen keeps what the user has in progress across a rebuild
R47 · a screen reads a source once per entry, never once per frame
R53 · diagnostics through `android.util.Log`, ERROR for what needs a human
R54 · no data attached to a person in a log message
R55 · one nominal and one failure test per public function
R62 · the lexicon, no synonym and no abbreviation
R63 · English, one line per exported symbol
R64 · no user-facing string literal in the code
R79 · a failure neither carried into a state nor propagated is logged at ERROR
R80 · never report a failure through another one's catalogue key
R81 · a unit test whose subject reaches `android.*` runs under Robolectric

## Requests

—
