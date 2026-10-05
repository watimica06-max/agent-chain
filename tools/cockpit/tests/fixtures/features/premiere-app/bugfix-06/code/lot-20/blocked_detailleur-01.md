## What blocks

§9.10 states that every row of the race-detail delta column must name the
calculation behind it for a finished race, then leaves open which
calculation — if any — backs a `RUN` row and what backs the twenty-two
non-run rows, so `buildRow`'s delta output has no rule to derive a
signature or a criterion from.

## Where

lot-20 — `RaceDetailViewModel.buildRow`, the `delta`/`deltaTone` fields of
`SegmentRowUiState`, and `RaceDetailUiState.isDeltaColumnVisible`
(anchor §9.10 of `desc-bug.md`).

## To resume

A decision naming, for a stored finished race, what the delta column
shows on each of the three row families, and what `isDeltaColumnVisible`
then means:

- a `RUN` row (8 rows) — the plain truncated `durationMs −
  referenceDurationMs` the code computes today, some other calculation,
  or nothing;
- a `STATION` row (8 rows) and a `ROXZONE_OUT`/`ROXZONE_IN`/`FINAL` row
  (14 rows) — the same three choices;
- whether the whole column disappears when no family is covered, since
  spec-technique §9.2 renders a delta column and §3.4 (lap delta) is a
  live projection over segment pace that exists only on `RUN` segments
  and is never computable on a stored race.

Nothing else in lot-20 is blocked: §3.4 (missing-value glyph instead of
`?: 0L`), §6.10 (push after each write), §7.1 (`viewModelScope.launch`),
§9.1 (`RaceDetailUiState.raceId` and `SegmentRowUiState.index` dropped),
§9.3 (non-throwing segment lookup), §9.4 and §10.1 (the three handlers
act on their `Result`, the rename dialog stays open on a refusal),
§9.8 (bounded title and delete confirmation) and §12.2
(`SavedStateHandle`) each have their rule and their symbols confirmed —
`PhoneStringResources.Rename.rejected`, `.DeleteConfirm.rejected`,
`ProfileSyncPushService.push(permissionGranted, at)`,
`Clock`, `cumulativeDurationMs(segments, throughIndex)`.

## Decision

Name `CumulativeDeltaEstimator.finalDelta` as the calculation backing the
delta column on all three row families: each row's delta is that
calculation's per-segment term, `durationMs − referenceDurationMs`
matched on `Segment.index`, so `buildRow` keeps the truncated
subtraction, `DisplayFormatter.formatDelta` and the AHEAD/BEHIND/ZERO
tone it computes today, and `isDeltaColumnVisible` keeps its present
meaning — a reference race exists and is not the race being viewed.

`CumulativeDeltaEstimator.finalDelta(raceSegments, referenceSegments)`
is the corpus's delta for a stored finished race — Σ(real − reference)
over every segment carrying a non-null `durationMs`, every
`SegmentType`, no `RUN` restriction and no live projection — and
`EndOfRaceViewModel.computeState` already solves this same problem with
it: `finalDelta`, then `DeltaTone` by sign, then
`DisplayFormatter.formatDelta(DurationTruncationService.truncateToSeconds(deltaMs))`,
and `null` text and tone when it cannot compute. No row family is left
uncovered, so §9.10's "shows nothing rather than a number" applies only
where the row's existing gate fails — a null `durationMs`, or no
reference segment duration at that index — and that gate stays as it is,
never falling a missing reference duration back to `0L` the way
`finalDelta`'s own sum does (R20).

This does not extend to calling `finalDelta` from `buildRow` — it is a
whole-race sum and has no per-row signature — nor to `LapDeltaCalculator`
or `CumulativeDeltaEstimator.estimate`, which lot-20 neither calls nor
touches, nor to `EndOfRaceViewModel`, `DisplayFormatter` or
`DurationTruncationService`, which lot-20 does not modify. The row's gate
gains nothing beyond what §3.4 already gives it in this lot.

## Applied

Applied on 2026-09-05, in `code/lot-20/fiche-executable.md` — the delta
column's rule under `SegmentRowUiState`, the meaning of
`isDeltaColumnVisible` under `RaceDetailUiState`, and the §9.10 block of
the acceptance criteria.
