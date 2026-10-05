## Symbols

RaceDao.findInProgress — created
RaceDao.insertSegments — modified, `OnConflictStrategy` REPLACE → ABORT
RaceDao.upsertAndFind — created
RaceDao.findOrSaveRecordedRace — created
RaceDao.replaceReference — created
RaceDaoTest — created

## Build

analyze/test: cannot run. `./gradlew :core-data:check` (and any task
needing `:core-domain` compiled, since `:core-data` depends on it)
fails before reaching `:core-data` at all —
`RecordedRaceSyncService.kt:44` in `:core-domain`, `No value passed for
parameter 'retainedFactors'` / `'rejectedCalibrations'`. This is
pre-existing, unrelated to this lot's `RaceDao` changes, and already
documented in `architecte/detailleur-lot-53.md`: the call site is
lot-15's own scope, R74 rules it is not an R72 deferral since the
broken call site shares `:core-domain` with the signature that changed
it, and `:core-domain:check` cannot exit 0 until lot-15 runs — which
transitively blocks `:core-data:check` too, since Gradle compiles
`:core-domain` first. No ktlint or detekt task is currently registered
for `:core-data` (none found project-wide) to run in its place.
`RaceDao.kt` and `RaceDaoTest.kt` are reviewed by hand against the
existing call sites (`RaceRepositoryImpl`, `RaceRepositoryImplTest`)
for signature and type consistency.

## State

Added: RaceDao — atomic write-then-read transactions (entry); RaceDao
⚠️ the new atomic methods are not yet called anywhere (entry)
Removed: —

Open point (R16, ruled by architecte/detailleur-lot-09.md): findInProgress's
new lookup on RaceEntity.currentSegmentIndex carries no index. Out of this
lot's scope (RaceEntity, HyroxDatabase and RaceDatabaseMigrations are
excluded), so no migration is added here. The same gap already exists,
unaddressed, on RaceEntity.isReference, date and origin. For whichever
later lot's scope covers the schema files.

## Requests

—
