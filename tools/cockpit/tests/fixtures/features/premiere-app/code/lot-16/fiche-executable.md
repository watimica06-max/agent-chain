## Signatures

    RaceRecordingRepository.undoLastMark(raceId: Long): Result<Race>

    RaceRecordingRepository.stopRace(raceId: Long, atInstant: Instant): Result<Race>

    class UndoMarkingController(
        private val recordingRepository: RaceRecordingRepository
    ) {
        /** Whether §9.14's undo control is enabled for [race]. */
        fun canUndo(race: Race): Boolean

        /** Called on §9.14's undo control tap. */
        fun undo(raceId: Long): Result<Race>
    }

## Acceptance criteria

- `canUndo` returns false for a race whose `currentSegmentIndex` is 1 — no marking has closed a segment yet
- `canUndo` returns true for a race whose `currentSegmentIndex` is greater than 1
- `undo` calls `RaceRecordingRepository.undoLastMark` with the given `raceId` and returns its result
- `undoLastMark`, called on a race whose last mark closed segment N and opened segment N+1, clears segment N's `durationMs` and `cumulativeMs` and moves `currentSegmentIndex` back to N
- `undoLastMark` restores `currentSegmentOpenedAt` to the value it held immediately before that mark overwrote it — a single level of history, never the instant of the undo call itself
- `undoLastMark`, called a second time with no intervening mark, again reopens whichever segment is now the most recently closed one — never more than one segment per call
- `undoLastMark`, called on a race whose `currentSegmentIndex` is 1, is a no-op — the race comes back unchanged
- `stopRace` saves the race with `completion = INCOMPLETE`
- `stopRace` never sets `isReference` to true, whatever the race's prior state
- `stopRace` leaves the segment in progress with no `durationMs` — abandoned, never truncated to `atInstant` — and every segment after it stays unreached
- `stopRace` leaves every already-closed segment's `durationMs` unchanged
- `stopRace` clears `currentSegmentIndex` and `currentSegmentOpenedAt` to null, so the stopped race no longer surfaces through `RaceRecordingRepository.findInProgress`

## Dependencies

Race — pre-existing (lot-04)
RaceRecordingRepository — pre-existing (lot-06), modified here to add `undoLastMark` and `stopRace`
