## What I need

A rule for a lot whose change cannot compile on its own, because the
call site it breaks belongs to the next lot: what "deliverable" means
for the first of the pair, and what its report attests instead of a
green `check`.

## Why the lot cannot proceed

It proceeds — the signature and the criteria are written. What is
missing is the standard the Réalisateur and the Relecteur hold it to.
R4 makes `./gradlew check` exiting 0 the one definition of done, and
lot-03 cannot reach it: widening
`CumulativeDeltaEstimator.finalDelta`'s return from `Long` to `Long?`
leaves `:app-wear` uncompilable until lot-42 adapts
`EndOfRaceViewModel.computeState`. Two lots never modify the same
symbol, so lot-03 cannot fix the call site itself. Without a rule, the
Réalisateur either reaches into another lot's symbol to make `check`
pass, or reports a red build with nothing saying that is expected.

## Where I met it

lot-03 — `CumulativeDeltaEstimator.finalDelta`, technical document §3.4,
against the Product Owner's decision in
`code/lot-03/blocked_detailleur.md`, which settles the `Long?` return
and moves lot-42 immediately after lot-03 for that reason.

## What I think it is

add

## Verdict

**A convention. Written as R72 and R73, section 2 of
`docs/TECHNICAL_CONVENTIONS.md`.**

The project chooses what "deliverable" means for a lot whose change
breaks a call site it does not own; neither Gradle nor any tool imposes
that choice, and it holds on every machine. R72 makes lot-03 deliverable
on `./gradlew :core-domain:check` exiting 0 while the only remaining
project-wide failure is the `:app-wear` call site lot-42's sheet adapts.
R73 says what its report attests instead of a green project-wide
`check`: the failing call site, and the lot that adapts it.

⚠️ **R72 is conditional on a lot's sheet naming the owner.** A break no
lot's sheet adapts is not covered — that is a defect of the split, not a
gap in this file, and it goes back through the lot report.

