## Symbols

SensorFreshnessWindow.evaluate — modified, Fresh only when the age
  (`now - lastReadingAt`) falls in 0..WINDOW_MS; a negative age
  (a reading timestamped after `now`) is now Stale, not Fresh

## Build

analyze: clean (`:core-domain:check`, per the standing bugfix-06 decision
  — `ProfileViewModel.kt` fails `:app-phone:compileDebugKotlin` at `HEAD`,
  before this lot's change, on a pre-existing coroutine-scope defect this
  lot does not touch; `git status` confirms no local modification to that
  file)
test: `:core-domain:check` — 8 passed (SensorFreshnessWindowTest)

## State

Added: —
Removed: —

## Requests

—
