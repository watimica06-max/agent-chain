## Symbols

RaceRecordingRepository — modified, every operation but observeRecorded is now suspend
RaceRecordingRepositoryImpl — modified, Room-backed through RaceDao, constructor now takes RaceDao
Race — modified, stoppedAt: Instant? = null added
RaceEntity — modified, stoppedAtEpochMs: Long? = null and sentAtEpochMs: Long? = null added
HyroxDatabase — modified, version 4
RaceDatabaseMigrations — modified, MIGRATION_3_4 added
RepositoryModule (:app-wear) — modified, registers MIGRATION_3_4 and injects RaceDao into RaceRecordingRepositoryImpl
RepositoryModule (:app-phone) — modified, registers MIGRATION_3_4
PhoneRaceRecordingRepository — modified, every method is now suspend
RaceLaunchController.launch — modified, now suspend (call site RaceRecordingRepository.startClock became suspend; the sheet did not name this symbol)
RecordedRaceSyncService.acknowledge — modified, now suspend (call site RaceRecordingRepository.eraseRecorded became suspend; the sheet did not name this symbol)

## Build

analyze: clean — `./gradlew check` exits 0 project-wide; no ktlint or
detekt task is registered project-wide (none found in any module's
build.gradle.kts) to run against this lot's code

test: `./gradlew :core-domain:test :core-data:testDebugUnitTest
:app-phone:testDebugUnitTest :app-wear:testDebugUnitTest` — 1147
passed, 0 failed (core-domain 193, core-data 96, app-phone 338,
app-wear 520). `RaceRecordingRepositoryImplTest` (30 tests) and
`RaceDatabaseMigrationsTest`'s two added MIGRATION_3_4 tests exercise
this lot's own signatures; every other file listed under Symbols above
that is a test carries only the mechanical `suspend` a signature this
lot changed forces on it, to keep compiling.

## State

Added: RaceRecordingRepository's persistence — Room-backed through
RaceDao, MIGRATION_3_4, Race.stoppedAt/RaceEntity.stoppedAtEpochMs and
sentAtEpochMs — folded into the existing RaceRecordingRepository and
HyroxDatabase entries
Removed: the RaceRecordingRepositoryImpl in-memory-only entry,
superseded now that the repository is Room-backed

## Requests

—
