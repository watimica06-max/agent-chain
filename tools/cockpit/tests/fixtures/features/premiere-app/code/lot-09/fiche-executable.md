## Signatures

    sealed interface LapDeltaResult {
        data class Value(val projectedMs: Long, val deltaMs: Long) : LapDeltaResult
        object Fallback : LapDeltaResult
    }

    object LapDeltaCalculator {
        fun compute(
            pace: PaceResult,
            expectedDistanceM: Int,
            referenceDurationMs: Long,
            elapsedInSegmentMs: Long
        ): LapDeltaResult
    }

## Acceptance criteria

- A `PaceResult.Value` segment pace produces `projectedMs = expectedDistanceM ÷ speedMetersPerSecond` (converted to milliseconds) and `deltaMs = projectedMs − referenceDurationMs`
- A `projectedMs` that would fall below `elapsedInSegmentMs` is raised to `elapsedInSegmentMs`, and `deltaMs` is computed from that raised value
- A `PaceResult.Fallback` segment pace produces `LapDeltaResult.Fallback`

## Dependencies

PaceCalculator — produced by lot-08
PaceResult — produced by lot-08
Race — pre-existing (lot-04)
Segment — pre-existing (lot-01)
Profile — pre-existing (lot-05)
LapDeltaResult — produced by lot-09
