## Symbols

HeartRateReading — created
DistanceReading — created
SensorReadingsSource — created

## Build

analyze: no ktlint or detekt task is registered project-wide (none
found in any module's build.gradle.kts) to run against this lot's code.
`:app-wear:check` (compile, lint, tests) passes clean.

`./gradlew check` fails only at `:app-phone:compileDebugKotlin` —
four pre-existing errors in `ProfileViewModel.kt` calling
`ProfileRepository`'s suspend `update*` functions outside a coroutine.
Untouched by this lot; per R72/R73, lot-17's own report already names
this call site as lot-19's owned scope.

test: 7 passed

## State

Added: SensorReadingsSource, HeartRateReading, DistanceReading (entries)
Removed: —

## Requests

—
