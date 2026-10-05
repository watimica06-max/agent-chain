## Signatures

    enum class DeltaTone { AHEAD, BEHIND, ZERO }

    sealed interface ProjectionDeltaBlock {
        data class Value(val text: String, val tone: DeltaTone) : ProjectionDeltaBlock
        object Fallback : ProjectionDeltaBlock
        object Hidden : ProjectionDeltaBlock
    }

    sealed interface ProjectionArrivalBlock {
        data class Value(val text: String) : ProjectionArrivalBlock
        object Fallback : ProjectionArrivalBlock
        object Hidden : ProjectionArrivalBlock
    }

    data class ProjectionUiState(
        val cumulativeDelta: ProjectionDeltaBlock,
        val estimatedArrival: ProjectionArrivalBlock,
        val elapsedText: String,
        val position: String
    )

    class ProjectionViewModel(
        initialRace: Race,
        private val referenceRace: Race?,
        private val profile: Profile,
        private val markingController: SegmentMarkingController,
        private val navigator: WatchRaceNavigator
    ) {

        val uiState: StateFlow<ProjectionUiState>

        /**
         * The current segment's own lap delta (§3.4), recomputed upstream
         * (the Main race page's own pace pipeline) at pace-refresh cadence.
         * Null off a RUN segment or before a value is available.
         */
        fun onCurrentLapDeltaChanged(lapDelta: LapDeltaResult?)

        /**
         * Refreshes the continuously-recomputed blocks — the current
         * segment's own share of the cumulative delta/estimated arrival
         * (§3.5), and the total elapsed time — against
         * [nowElapsedRealtime].
         */
        fun onTick(nowElapsedRealtime: Long)

        /**
         * The advance control released (§4.3), staying active on this page.
         * Forwards to `markingController.onPressEnd(raceId,
         * touchDownAtElapsedRealtime, heldMs, profile.longPressMs,
         * slideExceeded)`. On `Marked(race)` with `race.completion ==
         * COMPLETE`, calls `navigator.onFinalMarking()`; on `Marked(race)`
         * otherwise, calls `navigator.onMarked()` — both update the held
         * race to the one returned. `Cancelled`/`Failed` leave the held
         * race and `navigator.current` unchanged.
         */
        fun onPressEnd(touchDownAtElapsedRealtime: Long, heldMs: Long, slideExceeded: Boolean)
    }

    @Composable
    fun ProjectionScreen(viewModel: ProjectionViewModel)

## Acceptance criteria

- With `referenceRace` null, `cumulativeDelta` and `estimatedArrival` are both `Hidden`, regardless of segment type or any `onCurrentLapDeltaChanged` call
- On a RUN segment with a reference loaded but no `LapDeltaResult.Value` yet (null or `Fallback`), `cumulativeDelta` and `estimatedArrival` are both `Fallback` — a dash, not a hidden block
- On a RUN segment with a reference loaded and a `LapDeltaResult.Value` current lap delta, `cumulativeDelta` is `Value` from `CumulativeDeltaEstimator.estimate`'s `cumulativeDeltaMs` (§10.1 `delta` format), toned AHEAD when negative, BEHIND when positive, ZERO at 0, and `estimatedArrival` is `Value` from `estimatedArrivalMs` (§10.1 `duration-elapsed` format)
- On a non-RUN segment with a reference loaded, `cumulativeDelta`/`estimatedArrival` compute from `CumulativeDeltaEstimator.estimate` without needing a current lap delta — never `Fallback` there
- `elapsedText` is the race's total elapsed time — closed segments' summed `durationMs` plus the current segment's own elapsed since it opened — formatted `duration-elapsed` (§10.1)
- `position` is `DisplayFormatter.formatPosition(currentSegmentIndex)` (§10.1 `position` format, "n/30")
- `onPressEnd` producing `Marked` with `race.completion` `INCOMPLETE` calls `navigator.onMarked()`; producing `Marked` with `COMPLETE` (the 30th segment) calls `navigator.onFinalMarking()` — either way the held race becomes the one `Marked` carries
- `onPressEnd` producing `Cancelled` or `Failed` leaves the held race and `navigator.current` unchanged

## Dependencies

Race — pre-existing (lot-04)
Segment, SegmentType — pre-existing (lot-01)
Profile — pre-existing (lot-05)
ProfileRepository — need only, `observe()` produced by lot-36
CumulativeDeltaEstimator, CumulativeDeltaResult — pre-existing (lot-10)
LapDeltaResult — pre-existing (lot-09, type only — this lot never calls `LapDeltaCalculator`)
SegmentMarkingController, MarkingOutcome — pre-existing (lot-15)
DurationTruncationService — pre-existing (lot-12)
DisplayFormatter — pre-existing (lot-42)
DesignTokens — pre-existing (lot-02)
WatchRaceNavigator, WatchDestination — pre-existing (lot-23)
WatchStringResources — pre-existing (lot-44), including `Projection.etaLabel`
