## What I need

Whether `RaceTicker` is meant to read the wall clock (`Clock`, the lot's
own declared dependency) for something specific, or whether `Clock` was
named in error.

## Why the lot cannot proceed

R49 states race timing reads the monotonic clock only, and the wall
clock is read once at the race's start and for dates. A periodic ticker
built on a plain `delay(intervalMs)` loop needs no `Clock` at all to
tick at a fixed cadence, and its consumer
(`MainRacePageViewModel.onTick(nowElapsedRealtime: Long)`) expects a
monotonic value that `Clock.now(): Instant` cannot supply without
breaking R49. I built `RaceTicker` without `Clock` — a bare `Flow<Unit>`
trigger, monotonic timing left to whoever collects it — but lot-47's own
declared Needs names `Clock`, and I cannot tell whether that reflects an
intended use I am missing or a listing carried over in error without
settling the point myself.

## Where I met it

`code/decoupage.md`, lot-47's entry (`Needs: Clock (pre-existing),
kotlinx.coroutines (pre-existing)`)

## What I think it is        add · update · remove

update — either drop `Clock` from lot-47's Needs, or state what
`RaceTicker` uses it for in a way that holds against R49

## Verdict

**Already carried, by R49 and R25 together. No rule written.**

The platform settles the half this request treats as open. `Clock.now():
Instant` is a wall-clock reading: the version catalogue declares no
`kotlinx-datetime`, so `Instant` here is the JDK 17 one, and
`java.time.Clock.instant()` is documented as an alternative to
`System.currentTimeMillis()` — non-monotonic, and free to jump when the
system time is set. Android's monotonic interval source is
`SystemClock.elapsedRealtime()`, which is what
`onTick(nowElapsedRealtime: Long)` names. `delay` likewise tracks time on
its dispatcher's own monotonic source and takes no clock. **There is no
reading of `Clock` that yields a monotonic value**, so no use of it in a
periodic ticker holds against R49 — the question of what it might have
been for has no answer that survives.

**Two rules in force already close it:**

- 🔴 **R49** — race timing reads the monotonic clock only; the wall clock
  is read once at the race's start and for dates. A ticker whose
  collector times a race is not one of those two readings.
- 🔴 **R25** — what a signature promises, the body delivers: an argument
  it takes is read. A `Clock` a ticker takes and never reads is exactly
  the first of R25's three ways a signature lies.

**The ticker built without `Clock` is what these two require.** The lot
proceeds as written; R2 covers the rest — the lot goes on against this
file as it stands.

⚠️ **The open half is not a convention.** Whether `code/decoupage.md`'s
`Needs:` line for lot-47 is corrected, and by whom, is a fact of the
split. **This agent does not settle the split** — it names no lot's
scope and no lot's dependencies. Carry the stale `Needs:` entry back
through lot-47's report, as a correction to the split, not as a
convention amendment.
