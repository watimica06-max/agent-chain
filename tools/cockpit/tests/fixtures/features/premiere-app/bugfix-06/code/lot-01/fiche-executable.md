## Signatures

HyresultResultParser.parse(pastedText: String) → HyresultParseResult
  — modification, behaviour only; the signature is unchanged
  — a line is trimmed and an empty line dropped before anything else;
    columns are split on a tab run or on a run of two or more spaces —
    unchanged, so `Time of Day`, `Sled Push In` and `F. Carry Out` each
    stay one column
  — a data row carries four columns, read by position: [0] the label,
    [1] the time of day, [2] the cumulative race time, [3] this
    segment's own diff. Columns [2] and [3] are the reverse of what the
    code reads today, and [1] is read by nothing
  — the first row is the export's header when its four columns read
    `Split`, `Time of Day`, `Time`, `Diff`; it is skipped, counts as no
    data row and shifts no position. A first row not carrying those four
    labels is a data row, at position 1. No later row is ever skipped,
    whatever it carries
  — a paste holds exactly 30 data rows; the closing `Total time` row is
    the thirtieth, and its diff closes segment 30
  — Success.segmentDurationsMs: the 30 diffs, milliseconds, in position
    order, index 0 being position 1; never empty on Success
  — Success.totalTimeMs: the cumulative read on the `Total time` row —
    the value of its third column, never a sum recomputed from the
    diffs
  — a time value reads as `m:ss` on two components and `h:mm:ss` on
    three, on either time column, row by row, in the same paste —
    unchanged
  — Failure(rowNumber, cause, rawRow, label): `rowNumber` counts the
    paste's non-empty lines, the header included, so data position *i*
    is row *i + 1* on a paste carrying a header — unchanged
  — the per-row order of checks is unchanged: column count, then the
    two time values, then the label, then the running sum
  — INSUFFICIENT_COLUMNS on a row of fewer than four columns;
    INVALID_TIME_VALUE when column [2] or column [3] does not parse;
    DIFF_SUM_MISMATCH when the running sum of the diffs read so far
    differs from that row's cumulative — each with `rawRow`, `label`
    null; unchanged but for which columns are read
  — UNKNOWN_LABEL when column [0] is none of the 30 expected labels,
    LABEL_OUT_OF_SEQUENCE when it is one of them but not the one
    expected at that position; both carry `rawRow` and `label`;
    both survive the change of vocabulary
  — the label is checked at positions 1..30 only; a 31st data row
    reaches TOO_FEW_SEGMENTS / TOO_MANY_SEGMENTS with the count read
    and `rawRow` null, and EMPTY_PASTE keeps `rowNumber` 0 — unchanged

The 30 expected labels, by position — the export's own vocabulary, the
point reached rather than the segment closed:

    1  Rox In            11 Sled Pull Out    21 Rox In
    2  SkiErg In         12 Rox Out          22 F. Carry In
    3  SkiErg Out        13 Rox In           23 F. Carry Out
    4  Rox Out           14 Burpee BJ In     24 Rox Out
    5  Rox In            15 Burpee BJ Out    25 Rox In
    6  Sled Push In      16 Rox Out          26 S. Lunges In
    7  Sled Push Out     17 Rox In           27 S. Lunges Out
    8  Rox Out           18 Row In           28 Rox Out
    9  Rox In            19 Row Out          29 Wall Balls In
    10 Sled Pull In      20 Rox Out          30 Total time

HyresultResultParser.buildExpectedLabels() → List<String>   *private*
  — modification: it yields the 30 labels above, in position order,
    never the `Run n` / `Roxzone n` / full-station vocabulary it yields
    today
  — it still reads `SegmentBlueprint.typeAt` and
    `SegmentBlueprint.stationAt`: a RUN position but 29 yields
    `Rox In`, a ROXZONE_OUT position yields `<station> In` for the
    station of the STATION position that follows it, a STATION position
    yields `<station> Out`, a ROXZONE_IN position yields `Rox Out`,
    position 29 yields `Wall Balls In` and position 30 `Total time`
  — the station names it writes are the export's: `SkiErg`,
    `Sled Push`, `Sled Pull`, `Burpee BJ`, `Row`, `F. Carry`,
    `S. Lunges`, `Wall Balls` — the three abbreviations are what the
    export writes, not `Burpee Broad Jump`, `Farmers Carry`,
    `Sandbag Lunges`
  — where `stationAt` returns null at a STATION position it yields that
    position's expected label and raises nothing: the `!!` at
    `HyresultResultParser.kt:148` goes
  — 30 entries, always, never empty

SegmentBlueprint.typeAt(index: Int) → SegmentType
SegmentBlueprint.stationAt(index: Int) → Station?
  — unchanged, neither is modified by this lot; the pairing they promise
    — `stationAt` non-null exactly at a STATION index of 1..30 — becomes
    a test of `SegmentBlueprintTest`

## Acceptance criteria

- A paste of the header row `Split · Time of Day · Time · Diff`
  followed by the export's 30 data rows returns Success carrying 30
  durations
- The same 30 data rows without that header row return a Success equal
  to the one above, the same 30 durations in the same order
- On that paste, `segmentDurationsMs[0]` is the first data row's fourth
  column in milliseconds, and `totalTimeMs` is the `Total time` row's
  third column in milliseconds
- The same paste with its third and fourth columns swapped on every row
  returns Failure DIFF_SUM_MISMATCH
- The same paste with different values in the second column only
  returns the same Success
- A paste whose first row's four columns are the header's labels but
  whose data rows number 30 after it returns Success — the header row
  shifts no position
- A paste of the header plus the 29 data rows up to `Wall Balls In`,
  without the `Total time` row, returns Failure TOO_FEW_SEGMENTS with
  the count 29
- A paste whose `Total time` row's label reads anything else, `Wall
  Balls Out` for instance, returns Failure UNKNOWN_LABEL on that row,
  carrying that label and the row's raw text
- A paste whose cumulative column crosses the hour (`1:01:40`) while
  its diff column stays `5:27` returns Success, both read in
  milliseconds
- A paste whose data position 14 reads `Burpee Broad Jump` returns
  Failure UNKNOWN_LABEL on that row, carrying that label
- A paste whose data positions 14, 22 and 26 read `Burpee BJ In`,
  `F. Carry In` and `S. Lunges In` returns Success
- A paste whose data position 6 reads `SkiErg In` returns Failure
  LABEL_OUT_OF_SEQUENCE on that row, carrying that label
- A paste whose first row reads `SkiErg In` returns Failure
  LABEL_OUT_OF_SEQUENCE on row 1 — a first row that is not the header
  is data, not a skipped row
- A paste of 31 data rows returns Failure TOO_MANY_SEGMENTS with the
  count 31
- A data row of three columns returns Failure INSUFFICIENT_COLUMNS on
  that row, carrying its raw text and no label
- A data row whose fourth column reads `abc` returns Failure
  INVALID_TIME_VALUE on that row, carrying its raw text and no label
- A blank or whitespace-only paste returns Failure EMPTY_PASTE with
  row number 0
- For every index 1 to 30, `SegmentBlueprint.stationAt` returns a
  station exactly where `SegmentBlueprint.typeAt` returns STATION, and
  null everywhere else

## Dependencies

HyresultParseResult — pre-existing (Success(totalTimeMs,
  segmentDurationsMs) | Failure(rowNumber, cause, rawRow, label));
  not modified by this lot
HyresultParseFailureCause — pre-existing (EMPTY_PASTE,
  INSUFFICIENT_COLUMNS, INVALID_TIME_VALUE, TOO_FEW_SEGMENTS,
  TOO_MANY_SEGMENTS, UNKNOWN_LABEL, LABEL_OUT_OF_SEQUENCE,
  DIFF_SUM_MISMATCH); the eight causes all stay
SegmentBlueprint — pre-existing (typeAt(index): SegmentType,
  stationAt(index): Station?); read, not modified
SegmentType — pre-existing (RUN, ROXZONE_OUT, STATION, ROXZONE_IN,
  FINAL)
Station — pre-existing (SKI_ERG, SLED_PUSH, SLED_PULL,
  BURPEE_BROAD_JUMP, ROW, FARMERS_CARRY, SANDBAG_LUNGES, WALL_BALLS);
  `SegmentBlueprint` pairs the first seven with the seven STATION
  indices, WALL_BALLS with none
`core-domain/src/test/resources/hyresult/*.txt` — the ten pre-existing
  fixtures carry the old four-column layout (rank · label · diff ·
  cumulative) and the old label vocabulary; every one of them is
  rewritten to the export's layout by this lot

## Conventions

R4 · `./gradlew check` exits 0
R12 · §1.1 and §2.5's parser half are realised in `:core-domain`
R22 · what it returns for every input it cannot compute on, never a
      value that reads as valid
R26 · no `!!` on a value coming from outside the function
R29 · a duration is carried in milliseconds, truncated only where it is
      displayed
R31 · an error crossing a module boundary is of a type that module
      declares
R32 · the pasted text is data from outside, validated at the module that
      receives it, no type of the outside crossing
R55 · a nominal test and a failure test per public function, same lot
R57 · a test building a paste violating "exactly 30 segments indexed
      1–30"
R62 · the lexicon — Segment, Cycle, Station, Duration, Cumulative,
      Total, Paste, Import
R63 · English, and one line per exported symbol saying what it
      guarantees and when it fails

## Requests

—
