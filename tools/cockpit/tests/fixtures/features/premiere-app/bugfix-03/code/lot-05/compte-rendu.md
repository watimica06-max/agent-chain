## Symbols

RecordedRacePayload — modified, gains `raceId: Long` as its first field
RecordedRaceSyncService — modified, constructor drops `RaceRepository`
RecordedRaceSyncService.sync — modified, marks races sent instead of saving/erasing them
RecordedRaceSyncService.acknowledge — created

## Build

analyze: clean
test: :core-domain:check passed, :core-sync:check passed, :app-wear:check passed

## State

Added: —
Removed: —

## Convention

—
