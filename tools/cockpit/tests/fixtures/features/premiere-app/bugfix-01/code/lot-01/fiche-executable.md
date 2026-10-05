## Signatures

RaceRecordingRepository.markSegment(
  raceId: Long, markedAtElapsedRealtime: Long, segmentDistanceM: Double?
) → Result<Race>

Change: gains `segmentDistanceM` — the distance in metres Health
Services measured over the segment being closed, or null when no
distance sample was received during it. `RaceRecordingRepositoryImpl`
gains a `ProfileRepository` constructor dependency. When the segment
being closed is a RUN segment (`SegmentBlueprint.typeAt(currentIndex)
== SegmentType.RUN`) and `segmentDistanceM` is non-null: derives the
kilometre from `currentIndex` — RUN segments 1, 5, 9, …, 29 map to
kilometres 1–8 via `(currentIndex - 1) / 4 + 1` — reads the profile's
current `correctionFactor` and `expectedDistanceM` from
`ProfileRepository`, calls `CorrectionFactorCalculator.compute(
kilometre, correctionFactor, expectedDistanceM,
segmentDistanceM.toFloat())`, and appends the resulting `Retained`
entry to `race.retainedFactors` or `Rejected` entry to
`race.rejectedCalibrations`. When `segmentDistanceM` is null, or the
segment being closed is not RUN, `compute` is not called and
`retainedFactors`/`rejectedCalibrations` are unchanged by that mark.

CorrectionFactorCalculator.compute(
  kilometre: Int, previousFactor: Float, expectedDistanceM: Int,
  measuredDistanceM: Float?
) → CorrectionFactorOutcome

Change: the `station: Station` parameter is replaced by `kilometre:
Int` (1–8, the RUN segment the measurement came from). `Retained.entry`
and `Rejected.entry` carry `kilometre` in place of `station`; the rest
of the computation (trusted range, blending) is unchanged.

RetainedFactor(kilometre: Int, factor: Double)

Change: the `station: Station` field is replaced by `kilometre: Int`.

RejectedCalibration(kilometre: Int, value: Double)

Change: the `station: Station` field is replaced by `kilometre: Int`.

SegmentMarkingController.onPressEnd(
  raceId: Long, touchDownAtElapsedRealtime: Long, heldMs: Long,
  longPressMs: Int, slideExceeded: Boolean, segmentDistanceM: Double?
) → MarkingOutcome

Change: gains `segmentDistanceM`, forwarded unchanged to
`recordingRepository.markSegment(raceId, touchDownAtElapsedRealtime,
segmentDistanceM)` whenever the press is not cancelled.

MainRacePageViewModel.onPressEnd(
  touchDownAtElapsedRealtime: Long, heldMs: Long, slideExceeded: Boolean
)

Change: before calling `markingController.onPressEnd`, computes
`segmentDistanceM = lastCumulativeDistanceM?.let { it -
baselineDistanceM }` and passes it as the new argument — null when no
distance sample has been received since the race started
(`lastCumulativeDistanceM == null`).

## Acceptance criteria

- Closing a RUN segment with a non-null `segmentDistanceM` whose
  implied k_mesuré falls inside `CorrectionFactorCalculator`'s trusted
  range appends a `RetainedFactor` carrying that segment's kilometre to
  `race.retainedFactors`
- Closing a RUN segment with a non-null `segmentDistanceM` whose
  implied k_mesuré falls outside that trusted range appends a
  `RejectedCalibration` carrying that segment's kilometre to
  `race.rejectedCalibrations`
- Closing a RUN segment with a null `segmentDistanceM` leaves
  `race.retainedFactors` and `race.rejectedCalibrations` unchanged
- Closing a non-RUN segment leaves `race.retainedFactors` and
  `race.rejectedCalibrations` unchanged, whatever `segmentDistanceM` is
- Closing the first RUN segment (index 1) records kilometre 1; closing
  the last RUN segment (index 29) records kilometre 8
- A press-end on `MainRacePageViewModel`, after at least one distance
  sample has been received, forwards `lastCumulativeDistanceM -
  baselineDistanceM` as `segmentDistanceM` down to `markSegment`
- A press-end on `MainRacePageViewModel`, before any distance sample
  has been received, forwards a null `segmentDistanceM` down to
  `markSegment`

## Dependencies

Race — pre-existing
ProfileRepository — pre-existing
CorrectionFactorOutcome — pre-existing
SegmentBlueprint — pre-existing
SegmentType — pre-existing
MarkingOutcome — pre-existing
