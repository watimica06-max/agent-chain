## Symbols

HyresultResultParser.parse — modified, reads columns [2]/[3] (cumulative, diff) by
  position instead of the old order, header recognised only on an exact
  `Split`/`Time of Day`/`Time`/`Diff` match, label vocabulary is the export's own
HyresultResultParser.buildExpectedLabels — modified, private, yields the export's
  30-label vocabulary, no `!!` on a null `stationAt`; on a STATION position where
  `stationAt` returns null it now yields that position's expected label from a
  fixed fallback table, not an empty station name plus " Out"

## Build

analyze: clean (`:core-domain:check`, per the applied blocking decision — no
  static-analysis plugin runs on `:core-domain`, so `check` here is `test`)
test: `:core-domain:test --tests HyresultResultParserTest --tests
  SegmentBlueprintTest` — 25 passed (21 in HyresultResultParserTest, 4 in
  SegmentBlueprintTest, the latter including the `stationAt`/`typeAt` pairing
  test)

`:app-phone` is not verified: `ProfileViewModel.kt` fails to compile at `HEAD`,
before this lot's change, on a pre-existing coroutine-scope defect this lot does
not touch (per the applied blocking decision). `:app-wear` is not exercised by
this lot and not re-verified.

## State

Added: —
Removed: —

## Requests

—
