## Symbols

SegmentMarkingController.onPressEnd — modified, now suspend
UndoMarkingController.undo — modified, now suspend
UndoMarkingController.canUndo — unchanged, still non-suspend
StopRaceController.stop — modified, now suspend
ControlViewModel.onUndoClicked — modified, undo/onSuccess/recompute moved inside viewModelScope.launch
ControlViewModel.onStopConfirmed — modified, stop/onSuccess/recompute moved inside viewModelScope.launch
MainRacePageViewModel.onPressEnd — modified, the whole markingController.onPressEnd call and its when block moved inside viewModelScope.launch

## Build

analyze: no ktlint or detekt task is registered project-wide (none
found in any module's build.gradle.kts) to run against this lot's code.

test: `:app-wear:testDebugUnitTest --tests` scoped to this lot's five
test classes passes clean: `SegmentMarkingControllerTest` (5),
`UndoMarkingControllerTest` (4), `StopRaceControllerTest` (5),
`MainRacePageViewModelTest` (18), `ControlViewModelTest` (12, two added
for `onUndoClicked` with `canUndo` false and with `undoLastMark`
failing) — 44 tests, 0 failures.

## State

Added: —
Removed: —

## Requests

architecte/realisateur-lot-43.md
