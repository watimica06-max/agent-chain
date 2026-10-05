## Symbols

ProfileRepositoryImpl.observe() — modified, a `profileDao.observe()` failure raised while collecting is now caught and logged, never propagated uncaught

Out-of-scope, per the blocked_realisateur.md Decision: every `RecordedRacePayload(` occurrence across :core-domain (production and test) grepped — 6 total, one being `RecordedRacePayload.kt`'s own constructor declaration and 5 being call sites. All 5 call sites carry `retainedFactors = emptyList()` and `rejectedCalibrations = emptyList()`: 3 already fixed before the block (`RecordedRaceSyncService.kt`'s production call, and the 2 in `RecordedRacePayloadTest.kt`), 2 fixed in this run (`RecordedRaceSyncServiceTest.kt:118` and `:119`). File touched outside lot-10's scope: core-domain/src/test/kotlin/com/mgilli/core/domain/sync/RecordedRaceSyncServiceTest.kt

## Build

analyze: clean
test: :core-domain:check passed, :core-data:check passed

## State

Added: —
Removed: —

## Requests

—
