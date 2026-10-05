## Symbols

RecordedRacePayload — modified, two required fields added:
retainedFactors (List<RetainedFactor>), rejectedCalibrations
(List<RejectedCalibration>)

## Build

analyze/test: `./gradlew :core-domain:compileKotlin` fails on
`RecordedRaceSyncService.kt:39-45`'s `RecordedRacePayload(...)` call —
`No value passed for parameter 'retainedFactors'` /
`'rejectedCalibrations'`, adapted by lot-15; no other error. `:core-domain`
is the only module this lot touches and its own module compiles no
further than that single call site, so `check` and the test task cannot
run — expected per R72/R73 and `architecte/detailleur-lot-53.md`.

## State

Added: —
Removed: —

## Requests

—
