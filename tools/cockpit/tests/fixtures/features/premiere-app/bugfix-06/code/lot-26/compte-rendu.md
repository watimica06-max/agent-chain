## Symbols

PhoneNavigationStateStore (:app-phone) — created

## Build

analyze: no ktlint/detekt Gradle task exists in `:app-phone` (verified via
`./gradlew :app-phone:tasks --all`) — nothing to run there.
test: `./gradlew :app-phone:check` fails — `:app-phone:compileDebugKotlin`
reports four pre-existing errors in `ProfileViewModel.kt` (lines 121, 128,
135, 143: `onHrMaxUpdated`, `onExpectedDistanceChanged`,
`onLongPressChanged`, `onZoneThresholdChanged`, calling `ProfileRepository`'s
suspend `update*` methods outside a coroutine). `ProfileRepository`
(`:core-domain`) carries the changed signature, `ProfileViewModel`
(`:app-phone`) the broken call site — different modules, so R74's condition
for an R72 deferral is met. Per the Product Owner's decision, R72/R73 apply;
lot-19 is the lot that adapts those four call sites (§7.1). No error is
reported against `PhoneNavigationStateStore.kt` or
`PhoneNavigationStateStoreTest.kt` themselves — the compiler's single pass
over `:app-phone` surfaces no problem in either file, only in the
pre-existing, unrelated `ProfileViewModel.kt`. `PhoneNavigationStateStoreTest`
carries a test per each of the three acceptance criteria (save-then-restore
on a reconstructed store, restore-never-saved, save-then-save-then-restore
picks the latest); the same compile failure blocks Gradle from actually
running them, as it blocks the rest of `:app-phone`'s test suite.

## State

Added: PhoneNavigationStateStore (:app-phone)
Removed: —

## Requests

—
