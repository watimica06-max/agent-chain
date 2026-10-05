## Signatures

DisplayFormatter.formatDurationSegment(totalSeconds: Long): String
  — unchanged signature; a negative totalSeconds renders the minus sign
    (the same non-ASCII '−' formatDelta already uses) followed by the
    m:ss of its magnitude, never a per-field negative remainder; a
    non-negative totalSeconds is unaffected

DisplayFormatter.formatDurationTotal(totalSeconds: Long): String
  — unchanged signature; a negative totalSeconds renders the minus sign
    followed by the h:mm:ss of its magnitude, never a per-field negative
    remainder; a non-negative totalSeconds is unaffected

DisplayFormatter.formatDateRelative(instant: Instant, now: Instant): DateDisplay
  — unchanged signature; returns DateDisplay.Future(time: String) — the
    zero-padded time of day, the same shape Today already carries — when
    instant's local calendar date is after now's, distinct from Today,
    Yesterday and Earlier; Today/Yesterday/Earlier keep their existing
    cases and conditions unchanged

DateDisplay (sealed class)
  — gains one new data class, Future(val time: String), alongside the
    existing Today/Yesterday/Earlier

## Acceptance criteria

- formatDurationSegment(-96) returns "−1:36" (the minus sign, then 96 seconds' magnitude as m:ss) — never a per-field negative such as "-1:-36"
- formatDurationTotal(-3723) returns "−1:02:03" (the minus sign, then 3723 seconds' magnitude as h:mm:ss) — never a per-field negative
- formatDateRelative(instant, now) returns DateDisplay.Future when instant's local calendar date is after now's local calendar date (e.g. now = 2026-04-12T08:00 local, instant = 2026-04-13T08:00 local), never DateDisplay.Earlier
- The same future instant does not return DateDisplay.Today or DateDisplay.Yesterday either — Future is its own distinct case, carrying the zero-padded time of day

## Dependencies

DateDisplay — pre-existing sealed class in the same file; this lot adds its Future case

## Conventions

R22 · a format states what it returns for every input, including one it previously handled wrong instead of stating explicitly
R62 · the new case's name follows the file's own existing vocabulary (Today/Yesterday/Earlier); no synonym invented
R63 · identifiers and comments in English; every exported symbol documents what it guarantees

## Requests

—
