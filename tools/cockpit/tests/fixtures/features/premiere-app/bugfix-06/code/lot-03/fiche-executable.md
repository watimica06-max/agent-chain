## Signatures

CumulativeDeltaEstimator.estimate(
  raceSegments: List<Segment>, currentSegmentIndex: Int,
  currentSegmentElapsedMs: Long, currentLapDelta: LapDeltaResult?,
  referenceSegments: List<Segment>
) → CumulativeDeltaResult
  — modification, behaviour only; the signature is unchanged
  — Fallback when `raceSegments` carries no entry whose `index` equals
    `currentSegmentIndex`; the lookup never throws
  — Fallback when `raceSegments` carries two entries of the same
    `index`, whatever that index and whatever `currentSegmentIndex`
  — otherwise unchanged: Value(cumulativeDeltaMs, estimatedArrivalMs),
    both milliseconds; `cumulativeDeltaMs` is signed, negative meaning
    ahead of the reference, `estimatedArrivalMs` is non-negative
  — Fallback when the current segment's type is RUN and
    `currentLapDelta` is not a Value — unchanged
  — a `referenceSegments` entry missing for an index still counts as a
    reference duration of 0, and a null `durationMs` still counts as 0:
    unchanged, neither is what §3.4 names

CumulativeDeltaEstimator.finalDelta(
  raceSegments: List<Segment>, referenceSegments: List<Segment>
) → Long?
  — modification: the return type becomes `Long?`, from `Long`
  — null when `raceSegments` carries two entries of the same `index`,
    whatever that index — the settled outcome, consistent with
    `estimate` returning Fallback on the same input
  — otherwise milliseconds, signed, negative meaning ahead of the
    reference: Σ(real − reference) over every entry of `raceSegments`
    carrying a non-null `durationMs`, matched to `referenceSegments` by
    `Segment.index`, with no current-index split and no per-segment
    clamp — unchanged
  — 0 when `raceSegments` is empty and when no entry carries a non-null
    `durationMs`: a computed zero, not an absence
  — a duplicate index withholds the total even when the duplicated
    entries carry a null `durationMs`
  — the milliseconds stay a bare `Long?`; the decision fixes that type

## Acceptance criteria

- estimate on a 30-entry race list whose current segment is a STATION,
  elapsed 5 000 ms against a reference of 3 000 ms, returns a Value
  whose cumulativeDeltaMs is the closed segments' signed sum plus 2 000
- estimate on a race list holding no entry of index 7, asked for
  current index 7, returns Fallback and raises nothing
- estimate on a race list holding index 5 twice returns Fallback, asked
  for current index 9
- estimate on a race list holding index 5 twice returns Fallback, asked
  for current index 5
- estimate whose current segment is a RUN and whose currentLapDelta is
  LapDeltaResult.Fallback returns Fallback
- finalDelta over a race list of distinct indices, each 1 000 ms slower
  than its reference over four entries, returns 4 000
- finalDelta over a race whose entries beat their references returns a
  negative total
- finalDelta over a race list holding index 5 twice returns null
- finalDelta over a race list holding index 5 twice, both entries
  carrying a null durationMs, returns null
- finalDelta over an empty race list returns 0
- finalDelta over a race list whose entries all carry a null durationMs
  returns 0
- finalDelta over an entry whose index has no matching reference entry
  adds that entry's own durationMs to the total

## Dependencies

Segment — pre-existing (index, type, station, durationMs)
SegmentType — pre-existing (RUN, ROXZONE_OUT, STATION, ROXZONE_IN, FINAL)
CumulativeDeltaResult — pre-existing (Value(cumulativeDeltaMs,
  estimatedArrivalMs) | Fallback)
LapDeltaResult — pre-existing (Value(projectedMs, deltaMs) | Fallback);
  lot-04 changes when compute returns Fallback, not this type
EndOfRaceViewModel.computeState — the one production caller of
  finalDelta (`app-wear/.../endofrace/EndOfRaceViewModel.kt:63`);
  it belongs to lot-42, which follows this lot, and this lot does not
  touch it — so `:app-wear` does not compile between the two lots. See
  the request in `architecte/`.

## Conventions

R4 · `./gradlew check` exits 0 — ⚠️ unreachable on this lot alone, see
     the request in `architecte/`
R10 · a module realising an entry that consumes nothing imports no other
R20 · missing data as a nullable, never an invented default
R22 · what it returns for every input it cannot compute on, never a
      value that reads as valid
R26 · no `!!` on a value coming from outside the function — the one at
      `CumulativeDeltaEstimator.kt:73` goes with the rewrite
R41 · every §3 entry is a pure function, its inputs passed in
R55 · a nominal test and a failure test per public function, same lot
R57 · a test building a race list violating "exactly 30 segments indexed
      1–30", the duplicate index being that violation
R62 · the lexicon — Segment, Delta, CumulativeDelta, EstimatedArrival,
      Fallback
R63 · English, and one line per exported symbol saying what it
      guarantees and when it fails

## Requests

architecte/detailleur-lot-03.md
