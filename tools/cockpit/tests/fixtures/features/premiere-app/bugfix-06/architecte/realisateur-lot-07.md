## What I need

A confirmation of which lot's sheet adapts `app-phone`'s
`ProfileViewModel.kt` to add the `is DateDisplay.Future` branch this
lot's new `DateDisplay.Future` case requires.

## Why the lot cannot proceed

It proceeds — this is not a blocker. `./gradlew :core-domain:check`
exits 0 with this lot's changes: `DateDisplay` gains `Future` and
`DisplayFormatter.formatDateRelative` returns it. Running
`./gradlew :app-phone:compileDebugKotlin` afterwards fails on a new
line this lot's change causes — `ProfileViewModel.kt:237`, an exhaustive
`when` over `DateDisplay` that has no `is Future` branch — in addition
to the pre-existing, unrelated suspend-function-call failures on lines
121/128/135/143 that `realisateur-lot-01.md`, `realisateur-lot-04.md`
and `realisateur-lot-42.md` already report. No pending lot's sheet
(lot-08, lot-17, lot-18, lot-52, lot-53) names `ProfileViewModel` or
`DateDisplay`.

## Where I met it

Running `./gradlew :app-phone:compileDebugKotlin` after this lot's
`:core-domain` change was complete and `:core-domain:check` had already
passed on its own: `ProfileViewModel.kt:237:16 — 'when' expression must
be exhaustive. Add the 'is Future' branch or an 'else' branch.`

## What I think it is

add — a lot's sheet naming `ProfileViewModel.kt`'s `syncStatusText` as
adapting to `DateDisplay.Future`, so R73 can name it in a report.

## Verdict

Already carried — R73: "A red build no lot is named the owner of is not
deliverable." No pending lot's sheet (lot-08, lot-17, lot-18, lot-52,
lot-53) names `ProfileViewModel.kt` or `DateDisplay`, so this lot cannot
name an owner for the `app-phone:compileDebugKotlin` failure at
`ProfileViewModel.kt:237`. Under R73 that makes lot-07 not deliverable
until a lot is assigned to add the `is Future` branch.

Naming which lot's sheet adapts `ProfileViewModel.kt` is a split
decision, not a convention — architecte does not assign lots or name
which file or method carries the adaptation. Escalate the coverage gap
to the split; no rule is written here.

