## Symbols

HeartRateZoneCalculator.determine — modified, now returns null on a
  profile whose hrMaxBpm is zero or negative, or whose zoneThresholds is
  not exactly four strictly increasing values, in addition to the
  existing null-hrMaxBpm and null-reading cases
HeartRateZoneCalculator.ranges — modified, same additional null cases as
  determine

## Build

analyze: clean (`:core-domain:check` — no static-analysis plugin runs on
  `:core-domain`, per the standing bugfix-06 finding on lot-01/lot-04;
  `./gradlew check` project-wide fails before this lot's change on an
  unrelated SDK-location issue on `:app-phone:lintReportDebug`)
test: `:core-domain:check` — 31 passed (HeartRateZoneCalculatorTest)

## State

Added: —
Removed: —
(HeartRateZoneCalculator entry in docs/CURRENT_TECHNICAL_STATE.md
rewritten to state the new validation conditions)

## Requests

—
