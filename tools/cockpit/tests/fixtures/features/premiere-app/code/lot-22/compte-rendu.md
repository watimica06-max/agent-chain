## Symbols

RecordedRacePayload — created
RecordedRaceSyncState — created
RecordedRaceTransport — created
RecordedRaceSyncService — created
RaceRecordingRepository.observeRecorded — created (interface addition), implemented in RaceRecordingRepositoryImpl
RaceRecordingRepository.eraseRecorded — created (interface addition), implemented in RaceRecordingRepositoryImpl
RaceRepository.saveRecordedRace — created (interface addition), implemented in RaceRepositoryImpl

## Build

analyze: clean (:core-domain:check, :core-data:check, :app-wear:check, :app-phone:check)
test: 7 passed (RecordedRaceSyncServiceTest), 2 passed (new RaceRepositoryImplTest cases, 22 total in that class), all pre-existing suites still green (RaceRecordingRepositoryImplTest, ProfileSyncPushServiceTest, RaceListViewModelTest, RaceDetailViewModelTest, ImportPreviewViewModelTest and the app-wear controller/view-model fakes adapted to the two new RaceRecordingRepository methods)

## State

Added: RecordedRaceSyncService (core-domain/src/main/kotlin/com/mgilli/core/domain/sync/RecordedRaceSyncService.kt), RecordedRacePayload, RecordedRaceSyncState, RecordedRaceTransport (same package)
Removed: —

## Convention

—
