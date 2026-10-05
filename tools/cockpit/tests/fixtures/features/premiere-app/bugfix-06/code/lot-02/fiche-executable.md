## Signatures

buildSegments(durationsMs: List<Long?>) → List<Segment>
  — modification, behaviour only; the signature is unchanged
  — exactly 30 entries required, durationsMs[0] for index 1 through
    durationsMs[29] for index 30; any other size is refused as it is
    today
  — a negative entry produces `durationMs = null` on that segment, the
    same as a null entry; zero is kept as zero
  — always 30 segments, indices 1..30 in order, type and station taken
    from SegmentBlueprint

cumulativeDurationMs(segments: List<Segment>, throughIndex: Int) → Long?
  — modification, behaviour only; the signature is unchanged
  — milliseconds, the sum of `durationMs` over the segments whose index
    is in 1..throughIndex
  — null as soon as one index of 1..throughIndex has no entry in
    `segments`, treated the same as an entry carrying a null
    `durationMs`; an entry outside that range never withholds the sum
  — 0 when the range is empty (throughIndex below 1)

## Acceptance criteria

- A durations list carrying a negative value at position 7 builds a
  segment 7 whose durationMs is null, the other 29 segments carrying
  the values given
- A durations list carrying null at position 7 builds a segment 7 whose
  durationMs is null
- A durations list carrying 0 at position 7 builds a segment 7 whose
  durationMs is 0
- A durations list of a size other than 30 is refused
- A 30-segment list with every duration present, asked through index
  10, returns the sum of the first ten durations
- A list from which the segment of index 4 is absent, asked through
  index 10, returns null
- A list from which the segment of index 12 is absent, asked through
  index 10, returns the sum of the first ten durations
- A list whose segment of index 4 carries a null durationMs, asked
  through index 10, returns null
- A complete 30-segment list asked through index 31 returns null

## Dependencies

Segment — pre-existing (index, type, station, durationMs)
SegmentBlueprint — pre-existing (typeAt, stationAt)
SegmentType, Station — pre-existing

## Conventions

R4 · `./gradlew check` exits 0
R10 · the module realising an entry that consumes nothing imports no other
R20 · missing data as a nullable, never an invented default
R22 · what it returns for every input it cannot compute on
R27 · a bound inclusive on both ends
R41 · a calculation entry is a pure function
R55 · a nominal test and a failure test per public function, same lot
R57 · a test building a value violating "exactly 30 segments indexed 1–30"
R62 · the lexicon — Segment, Duration, Cumulative
R63 · English, and one line per exported symbol saying when it fails

## Requests

—
