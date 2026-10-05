## Signatures

    sealed interface TrendArrow {
        object Up : TrendArrow
        object Down : TrendArrow
        object None : TrendArrow
    }

    object TrendArrowCalculator {
        fun determine(smoothed: PaceResult, segment: PaceResult): TrendArrow
    }

## Acceptance criteria

- A `smoothed` speed more than 2% higher than `segment`'s speed returns `Up`
- A `smoothed` speed more than 2% lower than `segment`'s speed returns `Down`
- A difference at or below 2% in either direction (relative to `segment`'s speed) returns `None`
- Either pace being `PaceResult.Fallback` returns `None`, regardless of the other's value

## Dependencies

PaceCalculator — produced by lot-08
PaceResult — produced by lot-08
TrendArrow — produced by lot-11
