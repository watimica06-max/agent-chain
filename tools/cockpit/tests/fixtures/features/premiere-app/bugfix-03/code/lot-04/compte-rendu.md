## Symbols

RaceRepository — modified, `saveRecordedRace` gains `raceId`
RaceRepositoryImpl — modified, gains the idempotency check
RaceEntity — modified, gains `sourceRaceId: Long?`
RaceDao — modified, gains `findBySourceRaceId`
HyroxDatabase — modified, version bumped to 2
RaceDatabaseMigrations.MIGRATION_1_2 — created
RaceRepositoryImplTest — modified, adapted to the new signature, three tests added
every existing implementer of RaceRepository whose `saveRecordedRace` override now matches the new signature — modified: the fake in RaceListViewModelTest.kt (app-phone), the fake in RaceDetailViewModelTest.kt (app-phone), the fake in ProfileViewModelTest.kt (app-phone), the fake in ProfileScreenTest.kt (app-phone), the fake in ImportPreviewViewModelTest.kt (app-phone), the fake in ProfileSyncPushServiceTest.kt (core-domain), the fake in PreparationViewModelTest.kt (app-wear), the fake in PreparationScreenTest.kt (app-wear), the fake in HomeViewModelTest.kt (app-wear), the fake in HomeScreenTest.kt (app-wear)
app-phone/di/RepositoryModule.kt — modified, wires MIGRATION_1_2
app-wear/di/RepositoryModule.kt — modified, wires MIGRATION_1_2

## Build

analyze: clean
test: core-domain 124 passed, core-data 49 passed, app-phone 174 passed, app-wear 290 passed

## State

Added: HyroxDatabase's `sourceRaceId` column and `MIGRATION_1_2`; RaceRepositoryImpl's idempotency check via `RaceDao.findBySourceRaceId`
Removed: —

## Convention

—
