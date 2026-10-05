## Symbols

settings.gradle.kts — modified, gains `include(":core-platform")`
core-platform/build.gradle.kts — created
gradle/libs.versions.toml — modified, gains `androidxActivity`/`androidxCore`
  version entries and `androidx-activity`/`androidx-core` library entries
app-phone/build.gradle.kts — modified, gains `implementation(project(":core-platform"))`
app-wear/build.gradle.kts — modified, gains `implementation(project(":core-platform"))`

## Build

analyze: no ktlint/detekt Gradle task exists on `:core-platform` (verified
via `./gradlew :core-platform:tasks --all`) — nothing to run there
test: `./gradlew :core-platform:check` clean, no source in the module yet.
`./gradlew :app-wear:check` clean. `./gradlew :app-phone:check` fails —
`:app-phone:compileDebugKotlin` reports the same four pre-existing errors
in `ProfileViewModel.kt` (`onHrMaxUpdated`, `onExpectedDistanceChanged`,
`onLongPressChanged`, `onZoneThresholdChanged` calling `ProfileRepository`'s
suspend `update*` functions outside a coroutine) already named by lot-16
and lot-17's own reports, confirmed present on `HEAD` before this lot's
changes (verified via `git stash`) and untouched by anything this lot
adds. Per R72/R73: lot-19 (`ProfileScreen`, `ProfileViewModel`,
`ProfileUiState`) is the lot that adapts those four call sites; this
lot's own change to `app-phone/build.gradle.kts` (one added
`implementation(project(":core-platform"))` line) raises no compiler
error of its own.

## State

Added: —
Removed: —

## Requests

—
