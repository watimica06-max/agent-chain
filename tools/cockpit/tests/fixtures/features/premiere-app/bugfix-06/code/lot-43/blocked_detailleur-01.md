## What blocks

Making `SegmentMarkingController.onPressEnd`, `UndoMarkingController.undo`
and `StopRaceController.stop` suspend, as §2.2 states, leaves three
production call sites uncompilable inside `:app-wear` — the module the
three controllers themselves live in — and the split assigns every one
of them to a later lot, which R74 forbids.

## Where

lot-43 — `Modifies: SegmentMarkingController, UndoMarkingController,
StopRaceController, and their tests`. Confirmed by grep, each call
sitting in a plain non-suspend function:

- `app-wear/src/main/java/com/mgilli/app_wear/control/ControlViewModel.kt:42`
  (`undoMarkingController.undo`) and `:63` (`stopRaceController.stop`) —
  lot-40, block-18, after this block
- `app-wear/src/main/java/com/mgilli/app_wear/race/MainRacePageViewModel.kt:132`
  (`markingController.onPressEnd`) — lot-41, block-18, after this block

`ProjectionViewModel.kt:142` already wraps its own call in
`viewModelScope.launch` (lot-39, coded) and survives the change.

Kotlin compiles `:app-wear`'s sources in one pass, so
`./gradlew :app-wear:check` cannot exit 0 at the end of this lot and
R72's precondition is never met — R74 names this the case R72's deferral
does not cover, and says the split assigning it to a later lot needs
correcting.

The Product Owner's decision in `code/lot-45/blocked_realisateur-01.md`
holds the two apart on purpose — "`stop()` becoming `suspend` under §2.2
stays lot-43's, and `ControlViewModel`'s move into
`viewModelScope.launch` under §7.1 stays lot-40's" — while
`code/sequence.md` runs lot-40 and lot-41 after lot-43.

§5.1's other item for this lot, "stop launches before awaiting
`close()`", is already carried: lot-45 gave `StopRaceController` its own
`CoroutineScope` under that same decision.

## To resume

Either move lot-40 and lot-41 before lot-43 in the sequence — each
wraps its own call in `viewModelScope.launch`, which compiles against
today's non-suspend controllers, and lot-43's conversion then breaks
nothing — or extend lot-43 to wrap those three call sites itself,
leaving §7.1's, §9.4's and §12.2's rework of both ViewModels with lot-40
and lot-41.

## Decision

Extend lot-43 to wrap the three same-module call sites itself —
`ControlViewModel.kt:42`, `ControlViewModel.kt:63` and
`MainRacePageViewModel.kt:132` — in `viewModelScope.launch`, each call
keeping its existing outcome handling inside the launch, and leave
`code/sequence.md` unchanged.

R74 names a call site sitting in the module the changed signature lives
in as this lot's own scope by construction, and says a split assigning
it to a later lot needs correcting, not deferring under R72.
`ProjectionViewModel.kt:139-142` already solves the identical problem in
the same module: the `markingController.onPressEnd` call and its
`when (val outcome = ...)` sit inside `viewModelScope.launch`. Moving
lot-40 and lot-41 earlier is not available — `code/decoupage.md` declares
both as needing lot-43's controllers.

This does not extend to §7.1's, §9.4's and §12.2's rework of
`ControlViewModel` and `MainRacePageViewModel`, which stays lot-40's and
lot-41's under the Product Owner's decision in
`code/lot-45/blocked_realisateur-01.md`, nor to their test files, whose
owner under R86 is the lot covering the subject they exercise: lot-43
adapts `ControlViewModelTest` and `MainRacePageViewModelTest` only as far
as `./gradlew :app-wear:check` exiting 0 requires.

## How it was applied

`code/lot-43/fiche-executable.md` is written against this decision:

- the three controller methods carry `suspend` in `## Signatures`, their
  parameters, return types and outcomes otherwise unchanged;
- `ControlViewModel.onUndoClicked`, `ControlViewModel.onStopConfirmed`
  and `MainRacePageViewModel.onPressEnd` appear as modifications whose
  own signatures do not change, each call and its existing outcome
  handling moving inside `viewModelScope.launch`, on
  `ProjectionViewModel`'s shape — the statements preceding the call stay
  outside it;
- `MainRacePageViewModel`'s `Cancelled` and `Failed` branches stay
  `Unit`: §9.4's ERROR log is lot-41's, not this lot's;
- `StopRaceController.stop` keeps lot-45's own-scope, non-awaited
  `exerciseSessionManager.close()` launch;
- an acceptance criterion bears on `./gradlew :app-wear:check` exiting 0
  with no unwrapped call site left in the module, and R74 and R86 are
  named in `## Conventions`.
