## Symbols

PreparationViewModel — modified, constructor now takes `sensorReadingsSource: SensorReadingsSource` and `savedStateHandle: SavedStateHandle`
PreparationViewModel.onHeartRateReading(bpm: Int, atElapsedRealtime: Long) — modified, the formatted text is also written to `savedStateHandle`
PreparationViewModel.onLaunchClicked(startedAt: Instant, startedAtElapsedRealtime: Long) — modified, both branches run on `viewModelScope`, read the `Result<Race>`, navigate only on success and show/log the rejection on failure
PreparationUiState.Ready(heartRateText: String?, referenceLoadedText: LabelRef?, rejectionMessage: LabelRef?) — modified, adds `rejectionMessage`
PreparationUiState.OpenFailed(heartRateText: String?, rejectionMessage: LabelRef?) — modified, adds `rejectionMessage`
PreparationScreen(viewModel: PreparationViewModel) — modified, `referenceLoadedText` is bound to `maxLines = 1`/`TextOverflow.Ellipsis`, `rejectionMessage` renders as its own `Text` on both branches

## Build

analyze: clean (`./gradlew :app-wear:check`)
test: 466 passed

## State

Added: two `## Traps — general` entries — testing a `viewModelScope.launch` return-before-effect ordering needs `StandardTestDispatcher` + `runCurrent()`, and a `ScalingLazyColumn` item's `Text` reports no real line wrap under this project's Robolectric setup without `Modifier.fillMaxWidth()`, so `maxLines`/`overflow` are asserted through `TextLayoutResult.layoutInput` instead of `isLineEllipsized`
Removed: —

## Requests

—
