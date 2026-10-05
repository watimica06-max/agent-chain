## Signatures

    interface ProfileRepository {
        // updateHrMaxBpm / updateZoneThreshold / updateExpectedDistanceM /
        // updateLongPressMs / updateCorrectionFactor unchanged.

        /**
         * The single profile row, as last synced from the phone. Emits on
         * every change. Before any sync has happened, emits the default
         * profile: hrMaxBpm unset, zoneThresholds [60, 70, 80, 90],
         * expectedDistanceM 1000, longPressMs 700, correctionFactor 1,
         * lastSyncSuccessAt unset.
         */
        fun observe(): Flow<Profile>
    }

    object WatchStringResources {
        // Permission / Waiting / Home / History / Prep / Projection /
        // Control / StopConfirm / ResumeDialog / End / Sync / RaceName
        // unchanged.

        /**
         * The display name for the segment at [index] (1..30), derived from
         * `SegmentBlueprint.typeAt`/`stationAt`: "Run n" for a RUN segment,
         * the station's name for a STATION segment, "Wall Balls" for
         * segment 30 (FINAL, treated as a station), and a Roxzone label
         * naming its destination for ROXZONE_OUT/ROXZONE_IN — the watch's
         * own fixed-text mapping, mirroring
         * `PhoneStringResources.segmentName`'s structure without sharing
         * its resource file (§10.2).
         */
        fun segmentName(index: Int): String
    }

    enum class DeltaTone { AHEAD, BEHIND, ZERO }

    sealed interface RaceTopBlock {
        data class LapDelta(val text: String, val tone: DeltaTone) : RaceTopBlock
        data class ReferenceTime(val text: String) : RaceTopBlock
        data class TransitionElapsed(val text: String) : RaceTopBlock
        object Hidden : RaceTopBlock
    }

    sealed interface RaceCenterBlock {
        data class Pace(val paceText: String?, val trend: TrendArrow) : RaceCenterBlock
        data class SegmentElapsed(val text: String) : RaceCenterBlock
        data class NextStep(val destinationName: String) : RaceCenterBlock
    }

    data class MainRacePageUiState(
        val stationLabel: String?,
        val top: RaceTopBlock,
        val center: RaceCenterBlock,
        val heartRateText: String?,
        val zone: HeartRateZone?
    )

    class MainRacePageViewModel(
        initialRace: Race,
        private val referenceRace: Race?,
        private val profile: Profile,
        private val sensorPermissionGranted: Boolean,
        private val markingController: SegmentMarkingController,
        private val navigator: WatchRaceNavigator
    ) {

        val uiState: StateFlow<MainRacePageUiState>

        /**
         * A Health Services heart-rate reading (§3.1), timestamped
         * monotonically. Ignored for zone/display purposes once
         * [sensorPermissionGranted] is false (§4.1's permanent fallback).
         */
        fun onHeartRateReading(bpm: Int, atElapsedRealtime: Long)

        /**
         * A Health Services distance/speed sample, as a cumulative distance
         * since the race started. The distance at the current segment's own
         * opening instant is this method's zero baseline for
         * `PaceCalculator.segmentPace` (§3.2) — a marking resets it.
         */
        fun onDistanceSample(
            cumulativeDistanceM: Double,
            speedMetersPerSecond: Double,
            atElapsedRealtime: Long
        )

        /**
         * Refreshes the continuously-recomputed blocks (segment elapsed
         * time, pace, lap delta, freshness fallback) against
         * [nowElapsedRealtime] — called on a display tick.
         */
        fun onTick(nowElapsedRealtime: Long)

        /**
         * The advance control released (§4.3). Forwards to
         * `markingController.onPressEnd(raceId, touchDownAtElapsedRealtime,
         * heldMs, profile.longPressMs, slideExceeded)`. On `Marked(race)`
         * with `race.completion == COMPLETE`, calls
         * `navigator.onFinalMarking()`; on `Marked(race)` otherwise, calls
         * `navigator.onMarked()` — both update the held race to the one
         * returned. `Cancelled`/`Failed` leave the held race and
         * `navigator.current` unchanged.
         */
        fun onPressEnd(touchDownAtElapsedRealtime: Long, heldMs: Long, slideExceeded: Boolean)
    }

    @Composable
    fun MainRacePageScreen(viewModel: MainRacePageViewModel)

## Acceptance criteria

- `observe()` emits the current stored `Profile` on subscription, and again after any of the five updaters succeeds
- Before any sync has happened, `observe()` emits the default profile: `hrMaxBpm` null, `zoneThresholds` [60, 70, 80, 90], `expectedDistanceM` 1000, `longPressMs` 700, `correctionFactor` 1
- `WatchStringResources.segmentName(index)` depends only on `SegmentBlueprint.typeAt(index)`/`stationAt(index)`, mirroring `PhoneStringResources.segmentName`'s type-to-name mapping for RUN/STATION/FINAL indices, and is defined for every index 1..30, ROXZONE included
- On a RUN segment with a reference loaded, `top` is `LapDelta` from `LapDeltaCalculator.compute`'s `deltaMs` against the reference race's same-index segment duration (§10.1 `delta` format), toned AHEAD when negative, BEHIND when positive, ZERO at 0; `center` is `Pace` from `PaceCalculator.segmentPace` (§10.1 `pace` format) with the trend from `TrendArrowCalculator.determine`
- On a RUN segment with no reference loaded, `top` is `Hidden`; `center` still renders the pace as above
- On a STATION or FINAL segment (segment 30 included) with a reference loaded, `stationLabel` is `WatchStringResources.segmentName(index)`, `top` is `ReferenceTime` from the reference race's same-index segment `durationMs` (§10.1 `duration-segment` format), `center` is `SegmentElapsed` from the time elapsed since the segment opened
- On a STATION or FINAL segment with no reference loaded, `top` is `Hidden`; `stationLabel` and `center` render as above — never 4 legible blocks at once
- On a ROXZONE_OUT or ROXZONE_IN segment, `top` is `TransitionElapsed` regardless of whether a reference is loaded, and `center` is `NextStep` naming `WatchStringResources.segmentName(index + 1)` — the upcoming station on ROXZONE_OUT, the next run on ROXZONE_IN
- `heartRateText` and `zone` are null before the first heart-rate reading, and once more than 10 seconds elapse since the last `onHeartRateReading` call relative to the tick's `nowElapsedRealtime` (§1.3) — the last reading is never kept displayed past that window
- With a reading within the freshness window and `sensorPermissionGranted` true, `heartRateText` is `DisplayFormatter.formatHr` of the reading and `zone` is `HeartRateZoneCalculator.determine`'s result against the previously active zone
- With `sensorPermissionGranted` false, `heartRateText` and `zone` stay null regardless of any `onHeartRateReading` call
- A zone reactivating after a stale gap (or the race's first reading) computes from the plain thresholds with no hysteresis, since the zone held through the gap is null
- `center`'s `paceText` is null whenever `PaceCalculator.segmentPace` returns `Fallback` (under 50m covered since the segment opened) or more than 10 seconds elapse since the last `onDistanceSample` (§1.3); otherwise the formatted pace
- A distance sample equal to the baseline captured when the current segment opened computes 0m covered so far — a marking resets the baseline, the previous segment's accumulated distance carries none of it forward
- `onPressEnd` producing `Marked` with `race.completion` `INCOMPLETE` calls `navigator.onMarked()`; producing `Marked` with `COMPLETE` (the 30th segment) calls `navigator.onFinalMarking()` — either way the held race becomes the one `Marked` carries
- `onPressEnd` producing `Cancelled` or `Failed` leaves the held race and `navigator.current` unchanged

## Dependencies

Race — pre-existing (lot-04)
Segment, SegmentType, Station, SegmentBlueprint — pre-existing (lot-01)
Profile — pre-existing (lot-05)
ProfileRepository — modified by this lot (adds `observe()`)
HeartRateZoneCalculator, HeartRateZone — pre-existing (lot-07)
PaceCalculator, PaceResult, SpeedSample — pre-existing (lot-08)
LapDeltaCalculator, LapDeltaResult — pre-existing (lot-09)
TrendArrowCalculator, TrendArrow — pre-existing (lot-11)
SegmentMarkingController, MarkingOutcome — pre-existing (lot-15)
SensorFreshnessWindow, Freshness — pre-existing (lot-03)
SensorPermissionState — pre-existing (lot-13); this screen receives the already-resolved Granted/Fallback state, never calls `SensorPermissionManager` itself
DurationTruncationService — pre-existing (lot-12)
DisplayFormatter — pre-existing (lot-42)
DesignTokens — pre-existing (lot-02)
WatchRaceNavigator, WatchDestination — pre-existing (lot-23)
WatchStringResources — pre-existing (lot-44); `segmentName(index)` produced by this lot
