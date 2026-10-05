## Signatures

sealed interface PreparationUiState {
  data class Ready(heartRateText: String?, referenceLoadedText: String?) : PreparationUiState
  data class OpenFailed(heartRateText: String?) : PreparationUiState
  object SensorConflict : PreparationUiState
}

class PreparationViewModel(
  raceLaunchController: RaceLaunchController,
  raceRepository: RaceRepository,
  navigator: WatchRaceNavigator
)
  val uiState: StateFlow<PreparationUiState?>
  fun onHeartRateReading(bpm: Int, atElapsedRealtime: Long)
  fun onLaunchClicked(startedAt: Instant, startedAtElapsedRealtime: Long)
  fun onQuitClicked()
  fun onConflictContinueClicked()
  fun onConflictCancelClicked()

PreparationScreen(viewModel: PreparationViewModel) — Composable

## Acceptance criteria

- Given `RaceLaunchController.openPreparation()` resolves to `PreparationState.Ready(referenceLoaded = true)`, `uiState` becomes `Ready` with `referenceLoadedText` equal to `WatchStringResources.Prep.referenceLoaded(name)`, `name` being the race last emitted by `RaceRepository.observeReference()`.
- Given it resolves to `PreparationState.Ready(referenceLoaded = false)`, `uiState.referenceLoadedText` is null.
- Given it resolves to `PreparationState.OpenFailed`, `uiState` becomes `OpenFailed`.
- Given it resolves to `PreparationState.SensorConflict`, `uiState` becomes `SensorConflict`.
- Given it resolves to `PreparationState.Resuming(race)`, `uiState` never emits a value, `WatchRaceNavigator.current` becomes `MAIN`, and neither `RaceLaunchController.launch` nor `RaceLaunchController.retryAndLaunch` is called.
- Before any call to `onHeartRateReading`, `uiState`'s `heartRateText` (`Ready` or `OpenFailed`) is null.
- After a call to `onHeartRateReading(bpm, at)`, `uiState`'s `heartRateText` equals `DisplayFormatter.formatHr(bpm)`.
- `onLaunchClicked` while `uiState` is `Ready` calls `RaceLaunchController.launch(startedAt, startedAtElapsedRealtime)` and moves `WatchRaceNavigator.current` from `PREPARATION` to `MAIN`.
- `onLaunchClicked` while `uiState` is `OpenFailed` calls `RaceLaunchController.retryAndLaunch(startedAt, startedAtElapsedRealtime)` and moves `WatchRaceNavigator.current` to `MAIN` regardless of that call's outcome.
- `onQuitClicked` moves `WatchRaceNavigator.current` from `PREPARATION` to `HOME`, without calling any `RaceLaunchController` method.
- `onConflictContinueClicked` calls `RaceLaunchController.confirmConflict()` and sets `uiState` to whatever `PreparationState` it resolves to (`Ready`, `SensorConflict` again, or `OpenFailed`).
- `onConflictCancelClicked` moves `WatchRaceNavigator.current` from `PREPARATION` to `HOME`, without calling `RaceLaunchController.confirmConflict()`.

## Dependencies

RaceLaunchController — pre-existing (lot-14)
PreparationState — pre-existing (lot-14)
RaceRepository — pre-existing (lot-25, observeReference)
WatchRaceNavigator — pre-existing (lot-23, launchRace()/quitPreparation())
WatchStringResources — pre-existing (lot-44, `Prep`/`ResumeDialog`)
DesignTokens — produced by lot-02
DisplayFormatter — pre-existing (lot-42, formatHr)
Race — pre-existing (lot-04)
