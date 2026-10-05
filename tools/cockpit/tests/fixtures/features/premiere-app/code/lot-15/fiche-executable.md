## Signatures

    interface HapticFeedback {
        /** One short pulse: a marking was taken into account. */
        fun confirmMarking()
        /** Two short pulses: a marking attempt was cancelled. */
        fun cancelMarking()
    }

    sealed interface MarkingOutcome {
        data class Marked(val race: Race) : MarkingOutcome
        object Cancelled : MarkingOutcome
        data class Failed(val error: Throwable) : MarkingOutcome
    }

    class SegmentMarkingController(
        private val recordingRepository: RaceRecordingRepository,
        private val haptics: HapticFeedback
    ) {
        fun onPressEnd(
            raceId: Long,
            touchDownAtElapsedRealtime: Long,
            heldMs: Long,
            longPressMs: Int,
            slideExceeded: Boolean
        ): MarkingOutcome
    }

## Acceptance criteria

- A press held for at least `longPressMs` with `slideExceeded` false calls `RaceRecordingRepository.markSegment` with `touchDownAtElapsedRealtime` as the mark instant, triggers one `confirmMarking` pulse, and returns `Marked`
- A press released before `longPressMs`, with `slideExceeded` false, writes nothing to the repository, triggers `cancelMarking`, and returns `Cancelled`
- A press with `slideExceeded` true returns `Cancelled` and triggers `cancelMarking`, whatever `heldMs` is
- Two markings issued one immediately after the other each independently return `Marked`, with no enforced delay between them
- A repository failure on `markSegment` returns `Failed`, without triggering either haptic pulse

## Dependencies

Profile — pre-existing (lot-05, longPressMs supplied by the caller)
RaceRecordingRepository — pre-existing (lot-06)
Race — pre-existing (lot-04)
HapticFeedback — produced by lot-15
MarkingOutcome — produced by lot-15
