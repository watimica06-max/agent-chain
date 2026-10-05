## Symbols

RaceRepository (:core-domain) — modified interface, all nine methods now
  suspend except observeAll/observeReference; saveRecordedRace gains
  retainedFactors/rejectedCalibrations parameters; observeAll/
  observeReference now Flow<Result<...>>
RaceRepositoryImpl (:core-data) — modified, every method moves to
  Dispatchers.IO and turns a raising RaceDao call into that method's own
  Result.failure; setAsReference/saveImportedRace/saveRecordedRace/
  replaceReference now go through RaceDao's atomic
  replaceReference/upsertAndFind/findOrSaveRecordedRace transactions
ProfileSyncPushService (:core-domain) — modified, push returns Failure
  without calling transport or markSyncSuccess when observeReference's
  or observeAll's first emission is a Result.failure
RecordedRaceListenerService (:app-phone) — modified, injects
  ProfileRepository, decodes/saves/writes the correction factor/
  acknowledges all inside the one serviceScope.launch, catches a decode
  failure as PayloadDecodingFailure logged at ERROR, adds onDestroy
  cancelling serviceScope

## Build

analyze: no ktlint or detekt Gradle task is registered in this project
  (verified via `./gradlew :app-phone:tasks --all`) — nothing to run.

test: `:core-domain:check` passes clean — 193 tests, 0 failures
  (ProfileSyncPushServiceTest: 15 tests covering the new
  observeReference/observeAll failure paths).
  `:core-data:check` passes clean — 94 tests, 0 failures
  (RaceRepositoryImplTest: 47 tests, one per acceptance criterion plus
  adapted regressions).
  `:app-phone:check` fails at `:app-phone:compileDebugKotlin` —
  `RaceListViewModel.kt:26` and `RaceDetailViewModel.kt:94,98` still
  collect `RaceRepository.observeAll()`/`observeReference()` as their
  pre-lot-31 `List<Race>`/`Race?` element type. Both files are named,
  in this lot's own R73 line, as lot-56's — the "five collectors of the
  two guarded flows" alongside `HomeViewModel`, `PreparationViewModel`
  and `MainActivity` (:app-wear). Verified with a temporary,
  uncommitted, local-only shim on those two files
  (`.getOrElse { emptyList() }` / `.getOrNull()`) reverted immediately
  after: with the shim in place, `:app-phone:compileDebugKotlin`
  succeeds and `:app-phone:compileDebugUnitTestKotlin` fails only on
  `RaceListViewModelTest.kt`, `RaceListScreenTest.kt`,
  `RaceDetailViewModelTest.kt`, `RaceDetailScreenTest.kt` — the same
  four test files R73 already names as lot-56's. No error is reported
  in `RecordedRaceListenerService.kt`, `RecordedRaceListenerServiceTest.kt`,
  `MainActivityTest.kt`, `ProfileViewModelTest.kt`, `ProfileScreenTest.kt`,
  `ImportPreviewViewModelTest.kt` or `ImportPreviewScreenTest.kt` in
  either run.

## State

Added: —
Removed: "RaceDao ⚠️ the new atomic methods are not yet called
  anywhere" (docs/CURRENT_TECHNICAL_STATE.md) — RaceRepositoryImpl now
  wires upsertAndFind/findOrSaveRecordedRace/replaceReference in

## Requests

—
