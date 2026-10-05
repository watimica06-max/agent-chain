## Symbols

WatchRaceComplicationDataSourceService.scope — created
WatchRaceComplicationDataSourceService.onComplicationRequest — modified, now launches on scope and returns before findInProgress resolves
WatchRaceComplicationDataSourceService.onDestroy — created, cancels scope

## Build

analyze: clean (`./gradlew :app-wear:check` — ktlint/detekt tasks not registered in this project; lint + compile + unit tests all pass)
test: 4 tests in WatchRaceComplicationDataSourceServiceTest, all passed

## State

Added: —
Removed: —

## Requests

—
