## Symbols

DisplayFormatter.formatDurationSegment(totalSeconds: Long): String — modified, a negative totalSeconds renders the minus sign then its magnitude's m:ss
DisplayFormatter.formatDurationTotal(totalSeconds: Long): String — modified, a negative totalSeconds renders the minus sign then its magnitude's h:mm:ss
DisplayFormatter.formatDateRelative(instant: Instant, now: Instant): DateDisplay — modified, returns DateDisplay.Future when instant's local calendar date is after now's
DateDisplay — modified, gains the Future(val time: String) case

## Build

analyze: no ktlint/detekt task exists in this project (pre-existing, out of lot scope)
test: ./gradlew :core-domain:check — 181 passed, 0 failed (26 in DisplayFormatterTest)

## State

Added: —
Removed: —
Modified: DisplayFormatter entry under `## Display` — negative-duration rendering and DateDisplay.Future documented; ProfileViewModel's non-exhaustive when over DateDisplay noted

## Requests

architecte/realisateur-lot-07.md
