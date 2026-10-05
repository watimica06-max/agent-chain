## Signatures

PaceCalculator.segmentPace(
  distanceCoveredM: Double, elapsedSinceSegmentStartMs: Long,
  correctionFactor: Float
) → PaceResult
  — modification, behaviour only; the signature is unchanged
  — Fallback when `correctionFactor` is zero or negative, and when the
    computed speed is zero or negative, on top of the two floors it
    already applies (distance below 50 m, elapsed at or below zero)
  — Value carries a strictly positive speed in metres per second; never
    an infinity, never a not-a-number

PaceCalculator.smoothedPace(
  speedSamples: List<SpeedSample>, now: Long, correctionFactor: Float
) → PaceResult
  — modification, behaviour only; the signature is unchanged
  — `now` and `SpeedSample.atElapsedRealtime` are monotonic instants in
    milliseconds
  — its own window filter retains a sample whose age `now - at` falls in
    0..WINDOW_MS inclusive; a sample of negative age — timestamped after
    `now` — is dropped, exactly as a sample past the window is
  — Fallback when no sample is retained, when the retained samples span
    less than 3 000 ms, when `correctionFactor` is zero or negative, and
    when the resulting speed is zero or negative
  — Value carries a strictly positive speed in metres per second

LapDeltaCalculator.compute(
  pace: PaceResult, expectedDistanceM: Int, referenceDurationMs: Long,
  elapsedInSegmentMs: Long
) → LapDeltaResult
  — modification, behaviour only; the signature is unchanged
  — Fallback when `pace` is not a Value, and when the Value's speed is
    zero or negative — it does not rely on segmentPace/smoothedPace
    having guarded it
  — Value keeps the existing floor: `projectedMs` is never below
    `elapsedInSegmentMs`; `deltaMs` is `projectedMs - referenceDurationMs`,
    milliseconds, signed, negative meaning ahead of the reference

## Acceptance criteria

- segmentPace over 100 m in 20 000 ms with a correction factor of 1.0
  yields a Value of 5.0 m/s
- segmentPace with a correction factor of 0.0 yields Fallback, whatever
  the distance and the elapsed time
- segmentPace with a negative correction factor yields Fallback
- smoothedPace over samples at now−9 000 ms and now−1 000 ms with a
  correction factor of 1.0 yields a Value equal to their average speed
- smoothedPace over samples at now−9 000 ms, now−1 000 ms and now+500 ms
  yields a Value equal to the average of the first two alone
- smoothedPace over one sample at now−1 000 ms and one at now+5 000 ms
  yields Fallback, the retained set spanning less than 3 000 ms
- smoothedPace retains a sample of age exactly 10 000 ms and drops one
  of age 10 001 ms
- smoothedPace with a correction factor of 0.0 or a negative one yields
  Fallback over samples that would otherwise yield a Value
- compute on a PaceResult.Value of speed 0.0 yields Fallback
- compute on a PaceResult.Value of a negative speed yields Fallback
- compute on a PaceResult.Value of 4.0 m/s, an expected distance of
  1 000 m, a reference duration of 240 000 ms and an elapsed time of
  10 000 ms yields a Value of projectedMs 250 000 and deltaMs 10 000
- compute whose projection falls below the elapsed time yields a
  projectedMs equal to that elapsed time

## Dependencies

PaceResult — pre-existing (Value(speedMetersPerSecond) | Fallback)
LapDeltaResult — pre-existing (Value(projectedMs, deltaMs) | Fallback)
SpeedSample — pre-existing (speedMetersPerSecond, atElapsedRealtime)
SensorFreshnessWindow.WINDOW_MS — pre-existing, 10 000; lot-05 changes
  `evaluate`'s outcome, not this constant

## Conventions

R4 · `./gradlew check` exits 0
R10 · the module realising an entry that consumes nothing imports no other
R20 · missing data as a declared absence, never an invented default
R22 · what it returns for every input it cannot compute on, no infinity
      and no not-a-number reaching a screen
R27 · a bound inclusive on both ends unless the entry states otherwise
R41 · a calculation entry is a pure function, its inputs passed in
R49 · the monotonic clock for race timing, the wall clock for dates
R55 · a nominal test and a failure test per public function, same lot
R57 · a test building a value violating "a projected time never below
      the elapsed time"
R59 · a test on the 50 m and 3 s floors the entry states
R62 · the lexicon — SegmentPace, SmoothedPace, CorrectionFactor,
      LapDelta, ProjectedTime, Fallback
R63 · English, and one line per exported symbol saying when it fails

## Requests

—
