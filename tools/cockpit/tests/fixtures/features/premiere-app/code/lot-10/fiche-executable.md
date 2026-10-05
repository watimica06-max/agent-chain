## Signatures

    sealed interface CumulativeDeltaResult {
        data class Value(val cumulativeDeltaMs: Long, val estimatedArrivalMs: Long) : CumulativeDeltaResult
        object Fallback : CumulativeDeltaResult
    }

    object CumulativeDeltaEstimator {
        fun estimate(
            raceSegments: List<Segment>,
            currentSegmentIndex: Int,
            currentSegmentElapsedMs: Long,
            currentLapDelta: LapDeltaResult?,
            referenceSegments: List<Segment>
        ): CumulativeDeltaResult
    }

## Acceptance criteria

- With every segment before `currentSegmentIndex` closed, their (real − reference) durations sum correctly into `cumulativeDeltaMs`
- On a `RUN` current segment with `currentLapDelta` a `LapDeltaResult.Value`, its `deltaMs` is added to the closed segments' sum to produce `cumulativeDeltaMs`
- On a `RUN` current segment with `currentLapDelta` a `LapDeltaResult.Fallback`, `estimate` returns `CumulativeDeltaResult.Fallback`
- On a non-`RUN` current segment whose `currentSegmentElapsedMs` has not yet exceeded its reference duration, the current segment contributes zero to `cumulativeDeltaMs`
- On a non-`RUN` current segment whose `currentSegmentElapsedMs` exceeds its reference duration, the current segment contributes `(currentSegmentElapsedMs − referenceDurationMs)` to `cumulativeDeltaMs`
- `estimatedArrivalMs` equals the real elapsed time of every segment before `currentSegmentIndex`, plus the current segment's own reference duration, plus the reference durations of every segment after it

## Dependencies

LapDeltaCalculator — produced by lot-09
LapDeltaResult — produced by lot-09
Race — pre-existing (lot-04)
Segment — pre-existing (lot-01)
SegmentType — pre-existing (lot-01)
CumulativeDeltaResult — produced by lot-10
