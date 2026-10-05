## Symbols

WatchStringResources — modified, every member returns LabelRef instead of String
WatchStringResources.RaceName — removed
WatchStringResources.Home.referenceLine — modified, returns LabelRef, two distinct resource ids
WatchStringResources.Prep.referenceLoaded — modified, returns LabelRef
WatchStringResources.Control.undoLabel — modified, now `undoLabel(index: Int): LabelRef`
WatchStringResources.segmentName — modified, returns LabelRef, ROXZONE branches computed directly
ControlUiState.undoLabel — modified, LabelRef?
ControlViewModel.computeState — modified, builds undoLabel from `Control.undoLabel(index - 1)` directly
HomeUiState.referenceLineText — modified, LabelRef
HomeUiState.startLabel — modified, LabelRef
HomeUiState.historyLabel — modified, LabelRef
HomeUiState.syncLabel — modified, LabelRef
SensorPermissionUiState.title — modified, LabelRef
SensorPermissionUiState.explanation — modified, LabelRef
SensorPermissionUiState.actionLabel — modified, LabelRef
WaitingForPhoneUiState.title — modified, LabelRef
WaitingForPhoneUiState.explanation — modified, LabelRef
WaitingForPhoneUiState.retryLabel — modified, LabelRef
PreparationUiState.Ready.referenceLoadedText — modified, LabelRef?
MainRacePageUiState.stationLabel — modified, LabelRef?
RaceCenterBlock.NextStep.destinationName — modified, LabelRef
RaceRecordingRepositoryImpl.startClock — modified, names the race via DisplayFormatter.formatDateTime directly, no WatchStringResources dependency

## Build

analyze: clean (`:app-wear:check`, lint included)
test: 239 passed (`:app-wear`) — `ControlViewModelTest` now also asserts `undoLabel` is null alongside `undoEnabled` false, for both the null and the first-segment index

## State

Added: —
Removed: WatchStringResources.RaceName

## Convention

—
