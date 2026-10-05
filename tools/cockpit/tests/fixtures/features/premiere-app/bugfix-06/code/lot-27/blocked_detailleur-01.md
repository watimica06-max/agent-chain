Settled and applied — `code/lot-27/fiche-executable.md` is written against
the `## Decision` below, not against §9.5 as the entry states it.

## What blocks

§9.5 says `PhoneApp` guards its two parse-result casts instead of
throwing, but never says what the phone shows once the guard holds — and
that state is reachable in ordinary use, so the answer is a visible
behaviour I cannot derive from any cited entry.

## Where

lot-27 — `desc-bug.md` §9.5, and
`app-phone/src/main/java/com/mgilli/hyroxtracker/MainActivity.kt`, the
`PhoneDestination.ImportPreview` and `PhoneDestination.PasteError`
branches of the private `PhoneApp` composable (lines 117–138).

Both branches read `PasteResultViewModel.uiState.value.lastParseResult`
and cast it to `HyresultParseResult.Success` / `.Failure`. Since lot-22,
`lastParseResult` is deliberately never saved — the file says so — so it
is null on every rebuild of that ViewModel. `PhoneNavigator` is a
`@Singleton` and keeps its back stack across a rotation, so rotating the
phone on the import-preview or paste-error screen lands `PhoneApp` on a
null `lastParseResult`. Today that throws; guarded, it renders something,
and no entry says what.

Neither fallback is derivable here: `ImportPreviewScreen` and
`PasteErrorScreen` cannot be built at all without their parse result, so
the branch either renders nothing at all or leaves the destination. lot-27
declares no string resource among its needs and §10 names no key for a
"lost import" message, so reporting the situation as text is not an option
within this lot either.

## To resume

Say what the phone shows when `PhoneApp` reaches `ImportPreview` or
`PasteError` and `lastParseResult` is not the expected variant — the same
answer covering both branches. The candidates:

- **a** — the branch renders nothing, and the user is left on a blank
  screen until they use the back gesture
- **b** — the branch returns to the paste screen, the way `PhoneNavigator`
  already trims a non-restorable destination when it restores its stack
  after a process death (`PhoneDestination.isRestorable`, lot-25)
- **c** — something else, named here

The third cast, `LocalContext.current as ComponentActivity` in the same
composable, needs no decision: guarded, the back gesture simply stops
short of `finish()` when the host is not a `ComponentActivity`. Only the
two parse-result branches are blocked, and the sheet follows within one
run of the decision below.

## Decision

Take candidate **b** for both branches: when `lastParseResult` is not the
expected `HyresultParseResult` variant, the `ImportPreview` and
`PasteError` branches of `PhoneApp` render nothing and call
`PhoneNavigator.backToPasteResult()`, so the phone lands on the paste
screen. Issue that call as a side effect of entering the branch, not from
the composition body, so it runs once per entry rather than once per
frame — the once-per-entry discipline R47 states for a read.

This is the same problem already solved in the same module: lot-25's
`PhoneDestination.isRestorable` is false for exactly `ImportPreview` and
`PasteError` because either "would restore into a screen with no state to
show," and `PhoneNavigator.restoreBackStack` trims such a destination down
to the nearest restorable entry beneath it — `PasteResult` in this flow,
as lot-25's own acceptance criteria state ("restores its `current` to
`PasteResult`, never `ImportPreview`"). `backToPasteResult()` is the exit
this pair already uses: `ImportPreviewViewModel.onCorrectClicked` and
`PasteErrorViewModel.onBackToPasteClicked` both call it, and
`PhoneNavigatorTest` asserts `current` becomes `PasteResult` from each.

This does not extend beyond the two branches of `PhoneApp`.
`PhoneNavigator`, `PhoneDestination` and `isRestorable` are untouched —
`backToPasteResult()` exists and needs no signature change, and lot-27
modifies only `PhoneApp` and `MainActivityTest`. No message is shown and
no string resource is added: §10 names no key for this case, and R64 and
R80 forbid inventing one or borrowing another entry's. The
`LocalContext.current as ComponentActivity` cast keeps the resolution the
block already states for it.

## How it was applied

- `PhoneApp`'s `ImportPreview` branch — renders the import preview only
  for a `HyresultParseResult.Success`; on any other value of
  `lastParseResult` (null, or a `Failure`) it renders nothing, builds no
  `ImportPreviewViewModel`, and calls `PhoneNavigator.backToPasteResult()`
  from a side effect entered with the branch, once per entry.
- `PhoneApp`'s `PasteError` branch — the same, mirrored on
  `HyresultParseResult.Failure`.
- `PhoneApp`'s `LocalContext.current as ComponentActivity` — a checked
  conversion; the back gesture stops short of `finish()` when the host is
  not a `ComponentActivity`, and raises nothing.
- `PhoneNavigator`, `PhoneDestination`, `PhoneDestination.isRestorable`,
  `PasteResultViewModel`, `ImportPreviewViewModel`, `PasteErrorViewModel` —
  untouched. No `PhoneStringResources` key is added and no message is
  shown.
