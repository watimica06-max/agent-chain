## What I need

Whether a caught `profileDao.observe()` failure inside
`ProfileRepositoryImpl.observe()` should resume emitting a value (and
which one — e.g. the same `defaultProfile()` fallback the interface
already documents for "no sync yet"), or complete the flow without
emitting further values.

## Why the lot cannot proceed

It is not blocked — the sheet's criterion ("no uncaught exception
reaches the collector") is decidable and testable regardless of which
choice is made. What §7.2 and TECHNICAL_CONVENTIONS.md leave open is
the recovery value/continuation itself: R20 bars inventing a default
for data that is not there, but a Room failure is not "data not
there," and neither the entry nor a convention states what `observe()`
is worth after catching one.

## Where I met it

lot-10, §7.2, ProfileRepositoryImpl.observe()'s new `.catch`.

## What I think it is        add · update · remove

add — a convention stating what a guarded Flow-returning boundary
method emits, if anything, after catching its source's failure, and
whether it stays subscribed for a later success. This will recur for
every other flow §7.2 touches later in the cycle (RaceRepositoryImpl,
RaceRecordingRepositoryImpl).

## Verdict

A convention, and a genuine gap: R20 answers what a value is worth when
data is not there, R33 and R34 answer what a suspend call returns and
what its caller does with a failure — none of the three settles what a
`Flow`-returning boundary emits after catching its *source's* failure,
which is neither "not there" nor a value a suspend function can hand
back in one shot. Confirmed against Kotlin's own documentation: `catch`
catches only what is upstream of it, and once it has caught, the
upstream flow does not resume on its own — nothing resubscribes it
without an explicit `retryWhen` (or equivalent). That platform fact
settles the "stays subscribed" half outright; the "what does it emit"
half is a project choice, not a platform-given one, and needed writing
down before it forks across `ProfileRepositoryImpl`, `RaceRepositoryImpl`
and `RaceRecordingRepositoryImpl`.

Written into `docs/TECHNICAL_CONVENTIONS.md`, section 6 (Errors and
failure), as R75 and R76: R75 bars reusing R20's absence fallback for a
genuine source failure and requires a declared failure value instead;
R76 states the platform fact — `catch` does not resubscribe, so a
boundary that must keep observing past a transient failure names its
own retry, none being presumed by this file.

