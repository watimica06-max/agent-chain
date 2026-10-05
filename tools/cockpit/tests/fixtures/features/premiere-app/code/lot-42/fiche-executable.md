## Signatures

DisplayFormatter.formatDurationSegment(totalSeconds: Long) → String
// "m:ss", no leading zero on the minutes group

DisplayFormatter.formatDurationTotal(totalSeconds: Long) → String
// "h:mm:ss", hour group always present, even "0"

DisplayFormatter.formatDurationElapsed(totalSeconds: Long) → String
// "m:ss" while totalSeconds < 3600, else "h:mm:ss"; no leading zero on the first group

DisplayFormatter.formatDelta(totalSeconds: Long) → String
// signed "m:ss"; "+" for totalSeconds >= 0, "−" (U+2212) for < 0; stays "m:ss" past the hour

DisplayFormatter.formatPace(totalSeconds: Long) → String
// "m:ss" pace value only; the "/km" unit is rendered separately by the caller

DisplayFormatter.formatHr(bpm: Int) → String
// bare integer; the "bpm" unit is rendered separately by the caller

DisplayFormatter.formatPosition(rank: Int) → String
// "n/30", no spaces

DisplayFormatter.formatZone(zone: HeartRateZone) → String
// bare zone number ("1".."5"); the "Zone" word is supplied by the caller's own text, not by this formatter

DisplayFormatter.formatZonePercentage(percentage: Int) → String
// integer + non-breaking space + "%" ("50 %")

DisplayFormatter.formatZoneRange(lowerBpm: Int, upperBpm: Int) → String
// bounds separated by an en dash, with unit ("94–112 bpm")

enum class RangeOperator { BELOW, ABOVE }

DisplayFormatter.formatZoneRangeExtreme(operator: RangeOperator, bpm: Int) → String
// BELOW → "< 94 bpm", ABOVE → "> 150 bpm"

DisplayFormatter.formatDistance(meters: Int) → String
// integer + space + "m", no thousands separator ("1000 m")

DisplayFormatter.formatPressDuration(ms: Int) → String
// integer + space + "ms" ("700 ms")

DisplayFormatter.formatDate(instant: Instant) → String
// day, abbreviated month, year ("12 avr. 2026")

DisplayFormatter.formatDateTime(instant: Instant) → String
// formatDate(instant) + " · " + zero-padded "h:mm" ("12 avr. 2026 · 09:14")

sealed class DateDisplay {
  data class Today(val time: String) : DateDisplay()
  data class Yesterday(val time: String) : DateDisplay()
  data class Earlier(val dateTime: String) : DateDisplay()
}

DisplayFormatter.formatDateRelative(instant: Instant, now: Instant) → DateDisplay
// Today/Yesterday carry only the zero-padded "h:mm" time; Earlier carries the full formatDateTime string

## Acceptance criteria

- A duration-segment value under an hour formats as "m:ss" without a leading zero on the minutes (396 seconds → "6:36")
- A duration-total value formats as "h:mm:ss" with the hour group present even at zero (3138 seconds → "0:52:18")
- A duration-elapsed value under 60 minutes formats as "m:ss"
- A duration-elapsed value at or past 60 minutes formats as "h:mm:ss"
- A zero or positive delta formats with a leading "+" (0 seconds → "+0:00")
- A negative delta formats with a leading "−" (U+2212), never the ASCII hyphen
- A delta past the hour stays in "m:ss" (4334 seconds → "+72:14", never "+1:12:14")
- A pace value formats as "m:ss", with no unit text in the returned string
- A heart-rate value formats as a bare integer, with no unit text in the returned string
- A position formats as "n/30" with no spaces
- A heart-rate zone formats as its bare number, with no "Zone" word in the returned string
- A zone percentage formats as an integer, a non-breaking space, and "%" (50 → "50 %")
- A zone range formats as its two bounds separated by an en dash, with the "bpm" unit (94, 112 → "94–112 bpm")
- A BELOW zone-range-extreme formats as "<", a space, the bound and "bpm" (94 → "< 94 bpm")
- An ABOVE zone-range-extreme formats as ">", a space, the bound and "bpm" (150 → "> 150 bpm")
- A distance formats as an integer, a space, and "m", with no thousands separator (1000 → "1000 m")
- A press duration formats as an integer, a space, and "ms" (700 → "700 ms")
- A date formats as day, abbreviated month, year ("12 avr. 2026")
- A date-time formats as the date, " · ", and a zero-padded "h:mm" ("12 avr. 2026 · 09:14")
- A relative date on the same calendar day as now returns Today, carrying only the zero-padded time
- A relative date on the calendar day before now returns Yesterday, carrying only the zero-padded time
- A relative date earlier than yesterday returns Earlier, carrying the full date-time string

## Dependencies

DurationTruncationService — produced by lot-12 (its truncated seconds feed formatDurationSegment/formatDurationTotal/formatDurationElapsed/formatDelta/formatPace)
HeartRateZone — produced by lot-07 (found in code, confirmed via lot-07's compte-rendu; reused, not redeclared)
