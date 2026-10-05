## Symbols

PhoneDestination.isRestorable — created (computed property)
PhoneNavigator — modified, constructor now takes `stateStore:
PhoneNavigationStateStore`; restores its back stack at construction and
persists it on every mutating call

## Build

analyze: no ktlint/detekt Gradle task exists in `:app-phone` (verified via
`./gradlew :app-phone:tasks --all`, same finding as lot-26) — nothing to
run there.
test: `./gradlew :app-phone:check` (and `:app-phone:compileDebugUnitTestKotlin`
directly) fail — `:app-phone:compileDebugKotlin` reports the same four
pre-existing errors in `ProfileViewModel.kt` (lines 121, 128, 135, 143)
already reported by lot-26: `onHrMaxUpdated`/`onExpectedDistanceChanged`/
`onLongPressChanged`/`onZoneThresholdChanged` call `ProfileRepository`'s
suspend `update*` methods outside a coroutine. `ProfileRepository`
(`:core-domain`) carries the changed signature, `ProfileViewModel`
(`:app-phone`) the broken call site — different modules, so R74's
condition for an R72 deferral is met, per the Product Owner's decision
already recorded against lot-26; lot-19 (block-8, after this lot's
block-6) is the lot that adapts those four call sites. No error is
reported against `PhoneDestination.kt`, `PhoneNavigator.kt`, or any test
file this lot touches — the compiler's single pass over `:app-phone`
surfaces no problem in any of them, only in the pre-existing, unrelated
`ProfileViewModel.kt`. `PhoneNavigatorTest` carries one test per each of
the five acceptance criteria (null-restore starts at RaceList, restores a
RaceDetail, restores past ImportPreview to PasteResult, restores past
PasteError to PasteResult, `back()` persisting to RaceList) plus its
existing push/pop tests adapted to the new constructor. Every other
`:app-phone` test file constructing `PhoneNavigator()` (a same-module call
site of the changed constructor, R74) is adapted to build a real
`PhoneNavigationStateStore` from a Robolectric `Context` instead:
`ImportPreviewViewModelTest`, `PasteResultViewModelTest`,
`RaceDetailViewModelTest`, `RaceListViewModelTest`, `PasteErrorViewModelTest`
(newly run under `RobolectricTestRunner`, `@Config(sdk = [34])`, alongside
their existing `Dispatchers.setMain` stubbing) and `PasteResultScreenTest`/
`RaceListScreenTest` (already Robolectric). The same pre-existing compile
failure blocks Gradle from actually running any of `:app-phone`'s tests,
as it already did for lot-26.

## State

Added: —
Removed: —

## Requests

—
