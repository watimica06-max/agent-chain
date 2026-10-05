## Signatures

    data class SpeedSample(val speedMetersPerSecond: Double, val atElapsedRealtime: Long)

    sealed interface PaceResult {
        data class Value(val speedMetersPerSecond: Double) : PaceResult
        object Fallback : PaceResult
    }

    object PaceCalculator {
        fun segmentPace(
            distanceCoveredM: Double,
            elapsedSinceSegmentStartMs: Long,
            correctionFactor: Float
        ): PaceResult

        fun smoothedPace(
            speedSamples: List<SpeedSample>,
            now: Long,
            correctionFactor: Float
        ): PaceResult
    }

    sealed interface CorrectionFactorOutcome {
        data class Retained(val newFactor: Float, val entry: RetainedFactor) : CorrectionFactorOutcome
        data class Rejected(val entry: RejectedCalibration) : CorrectionFactorOutcome
        object NoCandidate : CorrectionFactorOutcome
    }

    object CorrectionFactorCalculator {
        fun compute(
            station: Station,
            previousFactor: Float,
            expectedDistanceM: Int,
            measuredDistanceM: Float?
        ): CorrectionFactorOutcome
    }

## Acceptance criteria

- `segmentPace` with distance covered of at least 50m and a positive elapsed time returns `Value` equal to (distance ÷ elapsed time) × `correctionFactor`, in metres per second
- `segmentPace` with distance covered below 50m returns `Fallback`, whatever the elapsed time
- `smoothedPace` given samples spanning at least 3 seconds within the trailing 10-second window returns `Value` equal to their average speed × `correctionFactor`
- `smoothedPace` given samples spanning less than 3 seconds returns `Fallback`
- `smoothedPace` excludes any sample older than 10 seconds before `now` from the average
- `compute` with a k_mesuré (`expectedDistanceM ÷ measuredDistanceM`) inside [0.70, 1.40] returns `Retained` with `newFactor = 0.6 × k_mesuré + 0.4 × previousFactor` and a `RetainedFactor` carrying that `station`
- `compute` with a k_mesuré outside [0.70, 1.40] returns `Rejected`, carrying a `RejectedCalibration` with that `station` and the rejected k_mesuré value
- `compute` with a zero or null `measuredDistanceM` returns `NoCandidate`, with no entry produced

## Dependencies

Segment — pre-existing (lot-01)
Station — pre-existing (lot-01)
Profile — pre-existing (lot-05)
RetainedFactor — pre-existing (lot-04)
RejectedCalibration — pre-existing (lot-04)
Health Services distance/speed data types — framework
SpeedSample — produced by lot-08
PaceResult — produced by lot-08
CorrectionFactorOutcome — produced by lot-08
