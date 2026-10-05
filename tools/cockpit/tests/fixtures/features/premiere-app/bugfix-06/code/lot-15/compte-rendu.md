## Symbols

RecordedRaceSyncState.Failure — modified, now `data class Failure(val raceId: Long)`
RecordedRaceSyncService.sync — modified, builds the payload from the race's own retainedFactors/rejectedCalibrations and stops on either a send failure or a markSent failure, both setting observe() to Failure(race.id)

## Build

analyze: clean
test: core-domain 11 passed, app-wear 26 passed (HomeViewModelTest)

## State

Added: —
Removed: —

## Requests

—
