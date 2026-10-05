## Symbols

PaceCalculator.segmentPace — modified, now falls back on a zero or
negative correctionFactor and on a zero or negative resulting speed
PaceCalculator.smoothedPace — modified, window filter now retains ages
in 0..WINDOW_MS inclusive (drops a sample timestamped after now), and
falls back on a zero or negative correctionFactor and on a zero or
negative resulting speed
LapDeltaCalculator.compute — modified, now falls back on a
PaceResult.Value carrying a zero or negative speed, without relying on
segmentPace/smoothedPace having guarded it

## Build

analyze: n/a — no ktlint/detekt task wired for :core-domain
test: :core-domain:check — 159 passed, 0 failed
:app-phone:compileDebugKotlin fails project-wide `./gradlew check` on
ProfileViewModel.kt, unrelated to this lot — see architecte request

## State

Added: —
Removed: —
(PaceCalculator and LapDeltaCalculator entries in
docs/CURRENT_TECHNICAL_STATE.md rewritten to state the new fallback
conditions)

## Requests

architecte/realisateur-lot-04.md
