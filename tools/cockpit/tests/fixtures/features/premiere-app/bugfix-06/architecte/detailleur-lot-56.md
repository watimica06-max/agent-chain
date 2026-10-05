## What I need

What a state holder's own state is worth after the flow it collects
emits a declared failure value — kept at its last value, reset to an
initial value, or carried into a state of its own — when no §10
catalogue key exists to tell the user anything.

## Why the lot cannot proceed

It is not blocked. R79 settles the report (the failure is logged at
ERROR), R80 settles that nothing new reaches the user until §10 names a
key, and R75 bars letting the failure read as ordinary data. What none
of the three states is what the collector's *own* published state is
worth meanwhile. The sheet answers "kept at the value it last held, and
the initial value when no success has arrived", derived from R75 and
R80, but that is an inference, and the five collectors of this lot are
not the last: RaceRecordingRepositoryImpl's own §7.2 flows (lot-38) and
every ViewModel collecting them face the same question.

## Where I met it

lot-56, §7.2, the five collectors of RaceRepository's guarded flows —
RaceListViewModel, RaceDetailViewModel, HomeViewModel,
PreparationViewModel and MainActivity's WatchApp.

Two of the five make the consequence visible: a failure as the *first*
emission leaves RaceListViewModel showing the empty-list state, which
reads to the user exactly like "no races", and leaves
PreparationViewModel's uiState null, so the preparation screen never
appears at all — R76 saying no later success will follow.

## What I think it is        add · update · remove

add — a convention stating what a collector's published state is worth
after its source emits a failure it may not report, alongside R79 and
R80 which already cover the report itself.

## Verdict

**A convention, and a genuine gap. Written as R87 and R88, section 6 of
`docs/TECHNICAL_CONVENTIONS.md`.**

**The three filters leave it standing.** StateFlow imposes nothing on
what value a state holder chooses to publish; no tool reads meaning into
a UI state's shape; and it holds on no one machine. R79, R80 and R75
between them settle the *report* — the log, the barred literal, the
barred conflation with ordinary data — and none of the three says what
the collector's *own* downstream state is worth while no report reaches
the screen. **That is genuinely open, exactly as stated.**

**The sheet's inference does not survive its own two examples.** "Kept at
the last value, and the initial value when none has arrived" reduces, on
a *first* emission, to "the initial value" — which is indistinguishable
from ordinary emptiness. That is exactly what R75 already forbids for
the flow itself, and the two visible cases show why keeping the
inference would be wrong rather than merely imprecise:
`RaceListViewModel`'s empty-list state reads to the user as "no races,"
and `PreparationViewModel`'s `uiState` staying `null` — R76 already
holding that no later success will arrive to replace it — leaves the
preparation screen dark forever with nothing to distinguish "not loaded
yet" from "never will be." **R87 corrects the sheet's inference**: the
collector carries the failure into a state of its own kind, not into the
shape success would have produced, so the distinction exists in code
even on the days §10 names no key to show it. **R88 closes exactly the
`PreparationViewModel` case**: the failure state is reachable from
nothing, not only as a transition away from a prior success, because
R76's completion means a first-emission failure gets no second chance to
be represented later.

**Both are off-grid, citing §7.2** — the same entry R75 and R76 cite, for
the same reason: no C-entry of the grid reaches what a collector's
published state is worth after its source's flow completes on failure.

The five collectors of this lot proceed under R87/R88; `RaceDetailViewModel`,
`HomeViewModel` and `MainActivity`'s `WatchApp` most plainly, since each
starts from a value with no failure state of its own to distinguish from
a legitimate empty or default reading. 📌 The same two rules govern
`RaceRecordingRepositoryImpl`'s own §7.2 flows (lot-38) and every later
`ViewModel` collecting them — the recurrence the request names is why
this was written as a rule rather than answered once for this lot alone.

