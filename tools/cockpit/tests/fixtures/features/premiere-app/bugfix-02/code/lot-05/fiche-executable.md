## Signatures

cumulativeDurationMs(segments: List<Segment>, throughIndex: Int) → Long?
  the sum of `durationMs` over every segment whose `index` is in
  `1..throughIndex`. Null when any segment in that range — including one
  whose index is below `throughIndex` — has a null `durationMs`; once
  broken, stays broken (a partial-then-resumed range never resumes
  summing).

Segment(index: Int, type: SegmentType, station: Station?, durationMs: Long?)
  carries no cumulative value of its own — `durationMs` is the only
  timing field.

buildSegments(durationsMs: List<Long?>) → List<Segment>
  each returned `Segment.durationMs` mirrors its input entry exactly; no
  cumulative is computed or stored while building.

RaceDetailViewModel.buildRow(race: Race, index: Int, referenceSegment: Segment?) → SegmentRowUiState
  unchanged parameters and return type. The cumulative and
  previous-cumulative values it feeds to
  `DurationTruncationService.segmentDisplayedSeconds` and
  `DisplayFormatter.formatDurationElapsed` are obtained from
  `cumulativeDurationMs(race.segments, index)` and
  `cumulativeDurationMs(race.segments, index - 1)` (0L when `index == 1`)
  — never from `Segment.cumulativeMs`. Each falls back to `0L` when the
  derivation returns null, exactly as the prior stored-field read did.

RaceRecordingRepositoryImplTest (app-wear)
  every assertion that read `Segment.cumulativeMs` reads
  `cumulativeDurationMs(segments, index)` instead, on the same segments
  and indices as before.

## Acceptance criteria

- `cumulativeDurationMs` on a range where every segment from 1 through
  `throughIndex` has a non-null `durationMs` returns the sum of those
  `durationMs` values
- `cumulativeDurationMs` returns null when the segment at `throughIndex`
  has a null `durationMs`
- `cumulativeDurationMs` returns null when a segment before
  `throughIndex` has a null `durationMs`, even though the segment at
  `throughIndex` itself is non-null
- `Segment`'s constructor accepts only `index`, `type`, `station` and
  `durationMs` — no cumulative parameter
- `buildSegments` returns segments whose `durationMs` values equal the
  input list entry for entry, regardless of position
- A `RaceDetailViewModel.buildRow` row whose own `durationMs` is present
  and every segment from 1 through its index is present displays a
  cumulative time equal to the truncated-seconds sum of those durations
- A `RaceDetailViewModel.buildRow` row whose own `durationMs` is present
  but an earlier segment's `durationMs` is missing displays the same
  cumulative time as if the segments before the missing one summed to
  zero
- After `RaceRecordingRepositoryImpl.undoLastMark` clears a segment's
  duration, `cumulativeDurationMs` through that segment's index returns
  null

## Dependencies

Segment — pre-existing, modified by this lot
SegmentType — pre-existing, unchanged
Station — pre-existing, unchanged
SegmentBuilder (buildSegments) — pre-existing, modified by this lot
cumulativeDurationMs — produced by this lot
RaceDetailViewModel — pre-existing, modified by this lot
Race — pre-existing, unchanged
SegmentRowUiState — pre-existing, unchanged
DurationTruncationService — pre-existing, unchanged
DisplayFormatter — pre-existing, unchanged
RaceRecordingRepositoryImplTest (app-wear) — pre-existing, modified by this lot

## Conventions

§3 · `:core-domain` never imports Android — `cumulativeDurationMs` and `Segment`/`SegmentBuilder` stay Android-free
§4 · a segment is measured, never derived — the total is the sum of segments
§7 · every duration is stored in milliseconds, as `Long`
§8 · cumulative values are computed on read, never stored
§14 · `:core-domain` has unit tests, on the JVM
