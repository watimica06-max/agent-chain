## Symbols

SensorPermissionUiState — modified, `resolvedState` dropped, carries
`title`, `explanation`, `actionLabel` only
SensorPermissionViewModel — modified, unchanged constructor
SensorPermissionViewModel.uiState — modified, constant for the
screen's whole life, never re-emitted
SensorPermissionViewModel.init — modified, no longer stores
`onLaunch()`'s result; resolves the navigator only on a first-ever
launch
SensorPermissionViewModel.onActionClicked — modified, no longer
stores `requestAgain()`'s outcome state
SensorPermissionViewModel.onResumed — modified, not suspend, returns
immediately; the `isGranted()` read and the navigator call now run
inside `viewModelScope.launch`
SensorPermissionScreen — unchanged, signature and body untouched

## Build

analyze: clean
test: 392 passed (`:app-wear`), full project `./gradlew check` exits 0

## State

Added: —
Removed: —

## Requests

—
