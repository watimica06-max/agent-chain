## Signatures

    enum class SegmentType { RUN, ROXZONE_OUT, STATION, ROXZONE_IN, FINAL }

    enum class Station {
      SKI_ERG, SLED_PUSH, SLED_PULL, BURPEE_BROAD_JUMP,
      ROW, FARMERS_CARRY, SANDBAG_LUNGES, WALL_BALLS
    }

    object SegmentBlueprint {
      fun typeAt(index: Int): SegmentType     // index 1..30
      fun stationAt(index: Int): Station?     // non-null only where typeAt(index) == STATION
    }

    data class Segment(
      val index: Int,
      val type: SegmentType,
      val station: Station?,
      val durationMs: Long?,
      val cumulativeMs: Long?
    )

    fun buildSegments(durationsMs: List<Long?>): List<Segment>
    // durationsMs holds exactly 30 entries, durationsMs[0] for segment 1
    // through durationsMs[29] for segment 30.

## Acceptance criteria

- `SegmentBlueprint.typeAt` returns, in order, RUN, ROXZONE_OUT, STATION, ROXZONE_IN for each of the four-segment cycles at indices 1-4, 5-8, 9-12, 13-16, 17-20, 21-24, 25-28
- `SegmentBlueprint.typeAt(29)` returns RUN and `SegmentBlueprint.typeAt(30)` returns FINAL
- `SegmentBlueprint.stationAt` returns, in order, SKI_ERG, SLED_PUSH, SLED_PULL, BURPEE_BROAD_JUMP, ROW, FARMERS_CARRY, SANDBAG_LUNGES for indices 3, 7, 11, 15, 19, 23, 27, and null for every other index including 30
- `buildSegments` on a durations list where one entry is null produces a Segment with a null `durationMs` and a null `cumulativeMs` at that index and at every following index
- `buildSegments` on a fully populated durations list produces, for each segment, a `cumulativeMs` equal to the sum of `durationMs` for that segment and every preceding one

## Dependencies

None — first symbols of the feature.
