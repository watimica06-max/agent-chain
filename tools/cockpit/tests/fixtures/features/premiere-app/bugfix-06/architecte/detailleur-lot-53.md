## What I need

Whether R72's "passing `./gradlew :<module>:check`" extends to a module
that cannot compile at all, because a sibling file in the *same* module
— owned by a later lot — calls the changed constructor; or whether this
case instead means the split needs correcting.

## Why the lot cannot proceed

It proceeds — the signature is written: `RecordedRacePayload` gains
`retainedFactors` and `rejectedCalibrations`, no default value, matching
§6.11 and `Race`'s own fields of the same name. What is missing is
knowing what "deliverable" means here. Unlike R72's own precedent
(`detailleur-lot-03.md`, `CumulativeDeltaEstimator.finalDelta` in
`:core-domain` versus `EndOfRaceViewModel.computeState` in `:app-wear` —
two different modules, so `:core-domain:check` still passes on its
own), `RecordedRacePayload` and the construction call this lot leaves
broken both sit in `:core-domain`:
`RecordedRaceSyncService.sync` (`core-domain/src/main/kotlin/com/mgilli/core/domain/sync/RecordedRaceSyncService.kt:39`)
constructs `RecordedRacePayload` with the old five-argument shape, and
is declared as lot-15's own scope, not this lot's. `./gradlew
:core-domain:check` compiles the whole module in one pass, so that
file's now-invalid call fails the same compile step this lot's own
change needs to pass — R72's module-scoped check cannot exit 0 at all,
not even from this lot's own change alone, until lot-15 runs.

A second, different-module call site — `PayloadCodec.kt`'s
`RecordedRacePayloadSnapshot.toPayload` (`:core-sync`, adapted by
lot-11) — fits R72 as already established and needs no new ruling.

## Where I met it

lot-53 — `RecordedRacePayload`, technical document §6.11, block-2 of
`code/sequence.md`. `RecordedRaceSyncService.kt` is lot-15's own scope
(anchors §6.4, §6.11), sequenced far later (block-5), yet lives in the
same Gradle module as `RecordedRacePayload`.

## What I think it is

add

## Verdict

Not an extension of R72 — a new rule, R74, marks the boundary R72 was
always implicitly resting on. R72's precedent (lot-03) works because the
touched module's own `:<module>:check` can exit 0 while a *different*
module still holds the broken call site. Here `RecordedRacePayload` and
`RecordedRaceSyncService.sync` share `:core-domain`; Kotlin compiles a
module's sources in one pass, so `:core-domain:check` cannot exit 0 at
all while that call site is unconverted — R72's precondition is never
met, whatever wording is added to it.

Per R74: a call site in the same module as the changed signature is this
lot's own scope by construction. The split assigning
`RecordedRaceSyncService.sync` to lot-15 while it shares `:core-domain`
with lot-53's change needs correcting — that correction is not
architecte's to make (it does not settle the split), so raise it there
rather than treating it as a deliverability question under R72/R73.

Rule written: R74, `docs/TECHNICAL_CONVENTIONS.md` §2.

