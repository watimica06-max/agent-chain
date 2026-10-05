## Symbols

MainRacePageViewModel — modified, constructor gains four parameters
  (SensorReadingsSource, RaceTicker, RaceRecordingRepository,
  SavedStateHandle); init collects heartRate()/distance()/speed()/
  ticks each on its own viewModelScope.launch and re-reads
  findInProgress() once
MainRacePageViewModel.onDisplayModeChanged — new
MainRacePageViewModel.onDistanceSample — modified, speedMetersPerSecond removed
MainRacePageViewModel.onSpeedSample — new
MainRacePageViewModel.onHeartRateReading, .onTick, .onPressEnd, .uiState — unchanged signatures
SensorValueDisplay — added to MainRacePageUiState.kt (Fresh/Stale/Fallback)
MainRacePageUiState — modified, heartRateText: String? becomes heartRate: SensorValueDisplay
RaceCenterBlock.Pace — modified, paceText: String? becomes pace: SensorValueDisplay
MainRacePageScreen — modified, displayMode and refreshIntervalMs parameters added

## Build

analyze: no ktlint or detekt task is registered project-wide (none
found in any module's build.gradle.kts) to run against this lot's code;
`:app-wear:check` (compile, lint) passes clean.

test: 500 passed, 0 failed (`:app-wear:testDebugUnitTest`, whole module).

## State

Added: `SensorValueDisplay` (Fresh/Stale/Fallback), and
  `MainRacePageViewModel`'s init-time collection of
  `SensorReadingsSource.heartRate()`/`.distance()`/`.speed()` and
  `RaceTicker.ticks`, its constructor-time `RaceRecordingRepository
  .findInProgress()` retained-race read, and its `SavedStateHandle`
  persistence (lastKnownNow, the heart-rate/distance raw components,
  the frozen last-Fresh pace text) — folded into the existing
  `MainRacePageViewModel` / `MainRacePageScreen` entry, which also
  gains `MainRacePageScreen`'s `displayMode`/`refreshIntervalMs`
  behaviour
Removed: the entry's prior description of `onDistanceSample` carrying
  `speedMetersPerSecond` and of a `MainRacePageViewModel` reaching no
  coroutine beyond `onPressEnd` — both superseded by the rewrite; the
  "needs a stubbed Main dispatcher" trap's own `MainRacePageViewModel`
  mention is updated to name `init` alongside `onPressEnd`

## Requests

architecte/realisateur-lot-41.md
