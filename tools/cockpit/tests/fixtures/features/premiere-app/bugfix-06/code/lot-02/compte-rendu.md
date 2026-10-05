## Symbols

buildSegments — modified, a negative entry in `durationsMs` now maps to
  a null `durationMs` on that segment, same as a null entry; zero is
  kept as zero
cumulativeDurationMs — modified, now walks every index of
  `1..throughIndex` explicitly: an index with no matching entry in
  `segments` returns null, the same as an entry present with a null
  `durationMs`; an entry outside that range never withholds the sum

## Build

analyze: `:core-domain:check` — BUILD SUCCESSFUL (no static-analysis
  plugin runs on `:core-domain`, so `check` here is compile + test)
test: `:core-domain:test` — 143 passed, 0 failed (17 classes,
  `SegmentBuilderTest` carries 15 of them)

`:app-phone:compileDebugKotlin` fails on `ProfileViewModel.kt`, a file
this lot never touches — present at `HEAD` before this lot's change,
already reported and judged by the Product Owner on lot-01 of this same
bugfix ("check judged on `:core-domain`, report written"). `:app-wear`
is not exercised by this lot and not re-verified.

## State

Added: —
Removed: —

## Requests

—
