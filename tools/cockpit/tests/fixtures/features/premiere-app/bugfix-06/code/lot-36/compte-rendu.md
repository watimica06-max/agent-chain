## Symbols

HomeViewModel — modified, `raceRecordingRepository: RaceRecordingRepository` added to the constructor
HomeViewModel.onSyncClicked — modified, derives `raceInProgress` from `raceRecordingRepository.findInProgress()` instead of a hardcoded `false`
HomeViewModel.init (link-established collector) — modified, derives `raceInProgress` the same way before calling `sync`
HomeViewModel.init (sensor reminder read) — modified, `currentSensorPermissionReminderVisible` initializes to `false` and is filled by a launched read of `isGranted()`
HomeViewModel.toHomeSyncUiState — unchanged
HomeSyncUiState — unchanged
HomeUiState — unchanged
HomeScreen — modified, `referenceLineText`'s `Text` carries `maxLines = 1` and `overflow = TextOverflow.Ellipsis`

## Build

analyze: clean
test: 404 passed (:app-wear:check)

## State

Added: —
Removed: —

## Requests

—
