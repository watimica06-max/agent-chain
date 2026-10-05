## Signatures

RaceRecordingRepository.startClock(
  startedAt: Instant, startedAtElapsedRealtime: Long
) → Result<Race>

RaceRecordingRepository.markSegment(
  raceId: Long, markedAtElapsedRealtime: Long
) → Result<Race>

RaceRecordingRepository.findInProgress() → Result<Race?>

## Acceptance criteria

- Calling `startClock` creates a `Race` with `origin = RECORDED`,
  `completion = INCOMPLETE`, `date` equal to `startedAt`,
  `currentSegmentIndex = 1`, `currentSegmentOpenedAt =
  startedAtElapsedRealtime`, and all 30 segments carrying no duration
- Calling `startClock` twice produces two distinct races, each keeping
  its own `date` fixed at the instant it was started — a later call
  never rewrites an earlier race's `date`
- Calling `markSegment` on the race's current segment writes that
  segment's `durationMs` as the elapsed time between its own opening
  instant and `markedAtElapsedRealtime`, never as a value derived from
  any other segment or from a total
- A single `markSegment` call closing segment N (N < 30) both writes
  segment N's `durationMs` and advances `currentSegmentIndex` to N+1
  with `currentSegmentOpenedAt` set to `markedAtElapsedRealtime`, in
  the same returned `Race` — never one without the other
- `markSegment` closing segment 30 writes its `durationMs`, sets
  `completion = COMPLETE`, and clears `currentSegmentIndex` and
  `currentSegmentOpenedAt` to null
- `markSegment` called for a race that carries no `currentSegmentIndex`
  (already ended, or unknown id) fails, leaving the stored race
  unchanged
- `findInProgress`, called after `startClock` and before the race
  ends, returns that race with its `currentSegmentIndex` and
  `currentSegmentOpenedAt` unchanged from the last write — enabling a
  restart to resume counting from `currentSegmentOpenedAt` rather than
  restart the segment
- `findInProgress`, called when no race carries a non-null
  `currentSegmentIndex`, returns null

## Dependencies

Race, RaceOrigin, RaceCompletion, Segment — produced by lot-04
buildSegments — produced by lot-01
WatchStringResources — produced by lot-44
DisplayFormatter — pre-existing (produced by lot-42, earlier in the sequence)
