## Signatures

DurationTruncationService.truncateToSeconds(ms: Long) → Long

DurationTruncationService.segmentDisplayedSeconds(
  cumulativeMs: Long, previousCumulativeMs: Long
) → Long

## Acceptance criteria

- A raw value of 1999ms truncates to 1 second, never rounding up to 2
- A raw value of exactly 2000ms truncates to 2 seconds
- Given previousCumulativeMs = 1900 and cumulativeMs = 3800, segmentDisplayedSeconds returns 2 — the difference of the two truncated cumulative totals (3 − 1) — not 1, which is what truncating the raw 1900ms segment duration alone would give
- For a race's first segment, segmentDisplayedSeconds(cumulativeMs, 0) equals truncateToSeconds(cumulativeMs)
- truncateToSeconds(-1999) returns -1, not -2 — truncation toward zero, not rounding, applies equally to a negative (delta) value

## Dependencies

None — all types are produced by this lot.
