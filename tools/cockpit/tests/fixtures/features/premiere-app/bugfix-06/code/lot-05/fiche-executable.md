## Signatures

SensorFreshnessWindow.evaluate<T>(
  value: T, lastReadingAt: Long, now: Long
) → Freshness<T>
  — modification, behaviour only; the signature is unchanged
  — `lastReadingAt` and `now` are monotonic instants in milliseconds
  — Fresh(value) when the age `now - lastReadingAt` falls in
    0..WINDOW_MS, both ends included
  — Stale when the age is past WINDOW_MS and when the age is negative —
    a reading timestamped after `now` is stale, not fresh
  — WINDOW_MS stays 10 000; the outcome does not depend on the display
    mode

## Acceptance criteria

- A reading of age 0 ms is Fresh and carries its value
- A reading of age exactly 10 000 ms is Fresh
- A reading of age 10 001 ms is Stale
- A reading timestamped 1 ms after `now` is Stale
- A reading timestamped 60 000 ms after `now` is Stale

## Dependencies

Freshness — pre-existing (Fresh(value) | Stale)
SensorFreshnessWindow — pre-existing, in
  core-domain/.../sensor/Freshness.kt alongside Freshness
SensorFreshnessWindowTest — pre-existing; the lot names the test file
  FreshnessTest, and no file of that name exists

## Conventions

R4 · `./gradlew check` exits 0
R10 · the module realising an entry that consumes nothing imports no other
R22 · what it returns for every input it cannot compute on
R27 · a bound inclusive on both ends
R41 · a calculation entry is a pure function, its clock passed in
R49 · the monotonic clock for race timing, the wall clock for dates
R55 · a nominal test and a failure test per public function, same lot
R62 · the lexicon — Freshness, Reading
R63 · English, and one line per exported symbol saying when it fails

## Requests

—
