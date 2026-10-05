## What I need

A rule saying where a `:app-wear` state holder gets the monotonic instant
it has to stamp its work with, when the event triggering that work carries
none.

## Why the lot cannot proceed

It proceeds — the signature is written against the conventions as they
stand. But nothing in them settles this, and two lots will answer
differently.

`RaceTicker.ticks` is a `SharedFlow<Unit>`: a tick carries no instant.
`MainRacePageViewModel.onTick(nowElapsedRealtime: Long)` needs one.
R49 fixes the monotonic clock as one of the two clocks for race timing but
does not say who reads it; the injected `Clock` of `:core-domain` is the
wall clock, so R49 bars it here. R41 keeps `:core-domain` free of it. R56
bars a test from reaching the system clock, while the only established
pattern in the module — `PreparationScreen`, which reads
`SystemClock.elapsedRealtime()` in the composable and passes it into the
ViewModel — has no equivalent for a flow the ViewModel collects itself.

Written for now as: the ViewModel reads `android.os.SystemClock
.elapsedRealtime()` at each tick, and its test runs under Robolectric per
R81. An injected monotonic source would be the other answer, and no lot of
this cycle declares one.

## Where I met it

lot-41, §5.3 — the `RaceTicker.ticks` collection feeding
`MainRacePageViewModel.onTick`.

## What I think it is

add

## Verdict

**A convention. Written as R90, section 7 of
`docs/TECHNICAL_CONVENTIONS.md`.**

Checked in this order:

- **Does the platform impose it?** No. Android leaves both a direct
  `SystemClock.elapsedRealtime()` read and an injected monotonic-clock
  abstraction equally available inside a `ViewModel`; nothing about the
  platform picks one.
- **Does a tool already check it?** No tool of R65's table reads clock
  usage; this is architecture, not a mechanical property.
- **Does the project already declare it?** Not this exact case. R49
  fixes *which* clock race timing reads, never *who* reads it. R41
  confines the injected-clock discipline to `:core-domain` alone, and
  says nothing about `:app-wear`. R56 bars a test from reaching the
  system clock in general terms — but R81 already carries the answer
  for the identically-shaped case of `android.util.Log`: a call to an
  `android.*` framework method that is an empty stub off-device is
  reached directly and exercised under Robolectric, because Robolectric's
  own shadow is what makes that reach compliant with R56, not an
  injected wrapper. `SystemClock.elapsedRealtime()` is such a call, and
  nothing distinguishes it from `Log` for this purpose.

**The gap is a genuine conjunction** between R41 (scopes the
injected-clock rule to `:core-domain`), R49 (silent on the reading
mechanism outside it) and R56/R81 (settle the general tension between
"no test reaches the system clock" and "an unavoidable `android.*` call
is reached directly, under Robolectric" — but only in words general
enough to leave `SystemClock` unnamed). No entry of the grid could have
seen this edge, since it sits between three entries each complete on
its own.

**The resolution matches the pattern the project already uses for
`Log`, not the alternative of inventing a new injected monotonic-clock
type**, since no lot of this cycle declares one and R66 bars adding a
dependency inside a lot; extending an already-adopted pattern is the
smaller change. Verified against Robolectric's own handling of
`SystemClock` (its shadow gives a controllable, deterministic value
rather than the real wall-bound clock) rather than assumed.
