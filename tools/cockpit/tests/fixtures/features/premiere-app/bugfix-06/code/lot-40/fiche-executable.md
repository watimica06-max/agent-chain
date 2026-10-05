## Signatures

### ControlViewModel — modification (`:app-wear`)

After the change:

    @HiltViewModel(assistedFactory = ControlViewModel.Factory::class)
    class ControlViewModel @AssistedInject constructor(
      @Assisted initialRace: Race,
      undoMarkingController: UndoMarkingController,
      stopRaceController: StopRaceController,
      navigator: WatchRaceNavigator,
      savedStateHandle: SavedStateHandle
    ) : ViewModel()

      @AssistedFactory
      interface Factory {
        fun create(initialRace: Race): ControlViewModel
      }
        — unchanged. `SavedStateHandle` is supplied by Hilt, not by the
          factory, so `MainActivity`'s CONTROL branch call site
          `hiltViewModel<ControlViewModel, ControlViewModel.Factory>(
          key = "control-${race.id}") { factory -> factory.create(race) }`
          is unchanged and is not edited by this lot.

    val uiState: StateFlow<ControlUiState>
      — never null. Its first value is computed before the constructor
        returns, from `initialRace` and from what the `SavedStateHandle`
        carries. No coroutine has run at that point and neither controller
        has been reached.

    fun onUndoClicked(): Unit
      — not `suspend`; returns before the undo completes. A no-op, reaching
        nothing, while `UndoMarkingController.canUndo(heldRace)` is false —
        no rejection is set, no message changes.

    fun onStopClicked(): Unit
      — not `suspend`, reaches no controller. Opens the confirmation and
        clears any stop rejection standing from an earlier attempt, then
        recomputes `uiState` before returning.

    fun onStopCancelled(): Unit
      — not `suspend`, reaches no controller. Closes the confirmation and
        clears any stop rejection, then recomputes `uiState` before
        returning.

    fun onStopConfirmed(atInstant: Instant): Unit
      — signature unchanged, not `suspend`; returns before the stop
        completes.

### ControlUiState — modification (`:app-wear`)

After the change:

    data class ControlUiState(
      val undoLabel: LabelRef?,
      val undoEnabled: Boolean,
      val stopConfirmVisible: Boolean,
      val undoRejectionMessage: LabelRef?,
      val stopRejectionMessage: LabelRef?
    )

    undoLabel, undoEnabled, stopConfirmVisible
      — unchanged in type and in meaning.

    undoRejectionMessage: LabelRef?
      — `WatchStringResources.Control.undoRejected` while the last undo
        attempt on this instance failed; null when none has been made, when
        the last one succeeded, and after a rebuild whose handle carries no
        rejection. Never a text this class builds itself (R64).

    stopRejectionMessage: LabelRef?
      — `WatchStringResources.StopConfirm.rejected` while the last stop
        attempt failed and the confirmation is still open; null when none
        has been made, when the last one succeeded, and once the
        confirmation is cancelled or reopened. The message is scoped to the
        open confirmation, so it never outlives the state it describes.

### ControlScreen — modification (`:app-wear`)

    @Composable fun ControlScreen(viewModel: ControlViewModel)

      — signature unchanged. Its body renders the two added fields: the
        undo rejection on the control page itself, below the undo pill;
        the stop rejection inside `StopConfirmOverlay`, which stays open.
        Each is resolved through
        `stringResource(ref.id, *ref.args.toTypedArray())`, the way every
        other `LabelRef` on this screen already is, and rendered only when
        non-null.

### ControlViewModelTest, ControlScreenTest — modification (`:app-wear`)

- Every construction of `ControlViewModel` in `:app-wear` passes the added
  `savedStateHandle` argument. Both test classes construct it directly
  (`ControlViewModelTest` twice, `ControlScreenTest` twice) and both are
  this lot's own scope under R74 — same module as the changed constructor,
  never deferred to a later lot.
- `ControlViewModel` reaches `android.util.Log` after this lot.
  `ControlViewModelTest` is a plain JVM test today: it carries
  `@RunWith(RobolectricTestRunner::class)` after this lot (R81), the way
  `PreparationViewModelTest` already does. `isReturnDefaultValues` is not
  set on the module (R82).
- The existing `Dispatchers.setMain(UnconfinedTestDispatcher())` /
  `Dispatchers.resetMain()` pair stays: the state document's trap names
  `ControlViewModel` among the classes needing it, through its injected
  `StopRaceController`.

### What changes

1. One constructor parameter is appended: `savedStateHandle:
   SavedStateHandle` (§12.2). The `@Assisted initialRace: Race` parameter
   keeps its name, its type and its lack of a string identifier — this
   class carries one `Race` parameter only, so the `Race`/`Race?`
   identifier trap does not reach it.

2. §7.1's call sites are already carried: lot-43 of this cycle moved
   `undoMarkingController.undo` and `stopRaceController.stop`, with their
   outcome handling and their `recompute()`, inside
   `viewModelScope.launch`, both controllers having become `suspend`.
   This lot keeps them there and adds nothing outside a coroutine.
   `UndoMarkingController.canUndo` stays where it is: it is not `suspend`,
   reaches no repository and no manager, and computes from the held race
   alone.

3. `onUndoClicked` acts on `undo`'s `Result` (§9.4). Today only
   `onSuccess` is read. After the change, inside the same
   `viewModelScope.launch`, the `Result<Race>` is folded:
   - success — the held race is replaced, the undo rejection is cleared,
     `navigator.onUndo()` is called (CONTROL → MAIN);
   - failure — the held race and `navigator.current` are unchanged, the
     undo rejection is set to `WatchStringResources.Control.undoRejected`,
     and the failure is logged at ERROR naming the operation (R79),
     carrying no race name, no date and no duration (R54).
   `recompute()` runs on both branches, as it already does.

4. `onStopConfirmed` acts on `stop`'s `Result` (§9.4), inside the same
   `viewModelScope.launch`:
   - success — `stopConfirmVisible` goes false, the stop rejection is
     cleared, `navigator.onStopConfirmed()` is called (CONTROL → END);
   - failure — `stopConfirmVisible` stays true and `navigator.current`
     stays CONTROL, both already today's behaviour; the stop rejection is
     set to `WatchStringResources.StopConfirm.rejected`, and the failure
     is logged at ERROR naming the operation (R79, R54).

5. What the `SavedStateHandle` holds, and what it does not (§12.2):
   - held — the race id this instance works on (`Long`, written at
     construction from `initialRace.id` when the handle carries none);
     `stopConfirmVisible` (`Boolean`); whether the last undo was rejected
     (`Boolean`); whether the last stop was rejected (`Boolean`).
   - read back at construction — the retained race id. When the handle
     carries an id and it differs from `initialRace.id`, the three
     retained booleans are discarded, the state starts fresh and the id is
     rewritten from `initialRace.id`; when it matches, or when the handle
     carries none, the retained booleans stand. This is `ProjectionViewModel`'s
     own retained-id guard (lot-39), against the race `MainActivity`
     re-read rather than one this class reads itself.
   - not held — the `Race` object. §12.2's second gap settles that what
     these ViewModels retain is the identifying value, the object being
     re-read: `MainActivity`'s CONTROL branch already reads
     `raceRecordingRepository.findInProgress()` and hands the result to
     the factory, keyed `"control-${race.id}"`, so `initialRace` is the
     re-read race and this lot adds no repository dependency.
   - not held — the two `LabelRef`s. `LabelRef` is not Bundle-storable;
     each message is rebuilt from its boolean flag, exactly as
     `PreparationViewModel` rebuilds `Prep.launchRejected` from its own
     (lot-38).
   - not held — `undoLabel` and `undoEnabled`, recomputed from
     `UndoMarkingController.canUndo` and the held race on every state
     change, never cached.

6. `computeState()` is otherwise unchanged: the same `canUndo` call, the
   same `WatchStringResources.Control.undoLabel(index - 1)` on the enabled
   branch, the same null label on the disabled one.

## Acceptance criteria

Acting on the two `Result`s (§9.4)

- With a repository whose `undoLastMark` fails, `onUndoClicked()` on a
  race whose current segment index is 5: once the dispatcher runs,
  `uiState.value.undoRejectionMessage` is
  `WatchStringResources.Control.undoRejected`,
  `WatchRaceNavigator.current` still carries `CONTROL`, and
  `uiState.value.undoLabel` is the label for segment 4 — the held race is
  unchanged.
- Same setup, one failing attempt followed by a succeeding one:
  `uiState.value.undoRejectionMessage` is null once the second attempt
  completes, and `WatchRaceNavigator.current` carries `MAIN`.
- On a race whose current segment index is 1 (`canUndo` false),
  `onUndoClicked()`: `UndoMarkingController.undo` is never called and
  `uiState.value.undoRejectionMessage` is unchanged from before the tap.
- With a repository whose `stopRace` fails, `onStopClicked()` then
  `onStopConfirmed(instant)`: once the dispatcher runs,
  `uiState.value.stopRejectionMessage` is
  `WatchStringResources.StopConfirm.rejected`,
  `uiState.value.stopConfirmVisible` is true, and
  `WatchRaceNavigator.current` still carries `CONTROL`.
- With a repository whose `stopRace` succeeds, the same sequence:
  `uiState.value.stopConfirmVisible` is false,
  `uiState.value.stopRejectionMessage` is null, and
  `WatchRaceNavigator.current` carries `END`.
- After a failing `onStopConfirmed`, `onStopCancelled()`:
  `uiState.value.stopConfirmVisible` is false and
  `uiState.value.stopRejectionMessage` is null.
- After a failing `onStopConfirmed`, `onStopClicked()` again:
  `uiState.value.stopRejectionMessage` is null before the new attempt
  completes.
- A failing undo and a failing stop each write one ERROR entry naming the
  operation; neither message carries the race name, the race date, a
  segment duration or a start time.

Rendering the two rejections (§9.4)

- `ControlScreen` driven by a ViewModel whose last undo failed displays
  the text of `control_undo_rejected`; driven by one whose undo has never
  failed, no node carries that text.
- `ControlScreen` driven by a ViewModel whose last stop failed displays
  the text of `stop_confirm_rejected` while the confirmation is showing,
  alongside the confirmation's own title, body, cancel and confirm texts.
- Neither message is a literal in the composable: each resolves through
  its `LabelRef`'s resource id.

Repository and controller calls from a coroutine (§7.1)

- Constructing `ControlViewModel` calls no `suspend` method of
  `UndoMarkingController` and none of `StopRaceController` before the
  constructor returns; `uiState.value` is already a `ControlUiState` at
  that point.
- With `Dispatchers.Main` set to a paused test dispatcher,
  `onUndoClicked()` on an enabled undo returns with
  `UndoMarkingController.undo` not yet called; once the dispatcher runs,
  it has been called exactly once, with the held race's id.
- With that same paused dispatcher, `onStopConfirmed(instant)` returns
  with `StopRaceController.stop` not yet called; once the dispatcher runs,
  it has been called exactly once, with the held race's id and `instant`.
- `onStopClicked()` and `onStopCancelled()` each leave `uiState.value`
  updated by the time they return, with `Dispatchers.Main` paused —
  neither reaches a coroutine.

ViewModel state across a rebuild (§12.2)

- `onStopClicked()` called on one instance, then a second instance built
  from that same `SavedStateHandle` and the same `initialRace`: the second
  instance's `uiState.value.stopConfirmVisible` is true.
- A failing `onUndoClicked()` on one instance, then a second instance
  built from that same handle and the same `initialRace`: the second
  instance's `uiState.value.undoRejectionMessage` is
  `WatchStringResources.Control.undoRejected`.
- A failing `onStopConfirmed(instant)` on one instance, then a second
  instance built from that same handle and the same `initialRace`: the
  second instance's `uiState.value.stopConfirmVisible` is true and its
  `uiState.value.stopRejectionMessage` is
  `WatchStringResources.StopConfirm.rejected`.
- A fresh, empty `SavedStateHandle`: `uiState.value.stopConfirmVisible` is
  false and both rejection messages are null.
- A handle carrying the three flags set and a race id that differs from
  `initialRace.id`: `uiState.value.stopConfirmVisible` is false and both
  rejection messages are null.
- A second instance built from a handle whose flags are set, on an
  `initialRace` whose current segment index is 1:
  `uiState.value.undoEnabled` is false and `uiState.value.undoLabel` is
  null — neither is read from the handle.
- A second instance built from a handle whose flags are set, on an
  `initialRace` whose current segment index is 7:
  `uiState.value.undoLabel` is the label for segment 6 — the held race
  comes from `initialRace`, not from the handle.

Shape unchanged

- `ControlViewModel.Factory.create` still takes exactly `initialRace`;
  `MainActivity`'s CONTROL branch is not edited by this lot.
- `ControlScreen` keeps its single-parameter signature.

## Dependencies

UndoMarkingController.canUndo(race: Race): Boolean — pre-existing
  (`:app-wear`), **not `suspend`**, reaches no repository: false on a null
  `currentSegmentIndex` and on index 1, true above. Unchanged by lot-43.
UndoMarkingController.undo(raceId: Long): Result<Race> — pre-existing
  (`:app-wear`), **`suspend` since lot-43 of this cycle**, delegating to
  `RaceRecordingRepository.undoLastMark`. Reused, never redeclared.
StopRaceController.stop(raceId: Long, atInstant: Instant): Result<Race> —
  pre-existing (`:app-wear`), **`suspend` since lot-43 of this cycle**;
  awaits `recordingRepository.stopRace` only, launching
  `ExerciseSessionManager.close()` on its own scope without awaiting it.
  Reused, never redeclared.
WatchRaceNavigator.onUndo(): Unit, .onStopConfirmed(): Unit — pre-existing
  (`:app-wear`), modified by lot-34 of this cycle; not `suspend`.
  `onUndo` moves CONTROL to MAIN, `onStopConfirmed` moves CONTROL to END;
  each is a no-op on every other destination. Reused, never redeclared.
WatchStringResources.Control.undoRejected: LabelRef,
  WatchStringResources.StopConfirm.rejected: LabelRef — created by lot-18
  of this cycle; fixed keys (`control_undo_rejected`,
  `stop_confirm_rejected`), no args. Reused, never redeclared.
WatchStringResources.Control.undoLabel(index: Int): LabelRef,
  .title, .stop, StopConfirm.title/.body/.cancel/.confirm — pre-existing
  (`:app-wear`), unchanged by this lot.
LabelRef(id: Int, args: List<Any>) — pre-existing (`:core-domain`);
  resolved by the composable through
  `stringResource(ref.id, *ref.args.toTypedArray())`, never inside the
  ViewModel.
Race (`id`, `currentSegmentIndex`) — pre-existing (`:core-domain`)
android.util.Log — the project's one diagnostic channel (R53), reachable
  from `:app-wear`
SavedStateHandle — `androidx.lifecycle.SavedStateHandle`, framework;
  `decoupage.md` declares it pre-existing, lots 19–23 inject it into
  `:app-phone` ViewModels and lots 38–39 into `:app-wear` ones. ⚠️ No
  `lifecycle-viewmodel-savedstate` entry exists in
  `gradle/libs.versions.toml`; it is reachable as a transitive of
  `androidx.hilt.navigation.compose`, already on `:app-wear` — R77 and
  R78 apply, and the report names it.
viewModelScope, StateFlow, MutableStateFlow — AndroidX /
  kotlinx.coroutines
RobolectricTestRunner — `org.robolectric`, pinned 4.14 (R65); already used
  by `PreparationViewModelTest` and every `:app-wear` screen test.

Traps carried by these symbols:
- `@HiltViewModel` on an `@AssistedInject` class needs
  `assistedFactory = ControlViewModel.Factory::class` explicitly —
  already carried, and it stays once a Hilt-supplied parameter joins the
  assisted one.
- `viewModelScope`, or an injected collaborator's own scope, needs a
  stubbed Main dispatcher outside Robolectric: the state document names
  `ControlViewModel` through its injected `StopRaceController`. The
  `Dispatchers.setMain(...)` / `Dispatchers.resetMain()` pair stays in
  place alongside the Robolectric runner R81 adds.
- `:app-wear`'s plain `createComposeRule()` needs `ui-test-manifest` —
  already on the module; `ControlScreenTest` is built this way and stays.
- A Compose UI test's `performClick()` on a `ScalingLazyColumn` item
  beyond the viewport silently no-ops: the two added `Text`s lengthen
  `ControlScreen`'s list, and a click test on an item past the visible
  height needs `performScrollTo()` first.

## Conventions

§2 · R4 — `./gradlew check` exits 0, the one definition of done
§2 · R74 — a call site of the changed constructor inside `:app-wear` is
  this lot's own scope: `ControlViewModelTest` and `ControlScreenTest` are
  converted here, never deferred under R72
§4 · R12 — §9.14's watch half stays in `:app-wear`; nothing of this lot
  moves into `:core-domain`
§5 · R18 — data crossing a public boundary is immutable; the held race is
  replaced, never mutated
§5 · R19, R24 — what blocks or reaches outside the process is `suspend`;
  both controller calls stay inside a coroutine
§5 · R20 — missing data crosses as a nullable or a declared absence type;
  an absent rejection is null, never an empty string
§5 · R25 — what a signature promises, the body delivers: the retained id
  is read back, and every value that must outlive a rebuild is written
  where it does
§5 · R26 — no `!!` on a value coming from outside the function
§6 · R34 — a caller receiving a failure acts on it: both `Result`s are
  read and both failures surface
§6 · R79 — a failure this screen cannot propagate is logged at ERROR,
  naming the operation
§6 · R80 — no failure reported through a catalogue key written for
  another one: the undo failure uses `Control.undoRejected` and the stop
  failure `StopConfirm.rejected`, never each other's
§7 · R39 — dependencies passed as constructor arguments, never read from
  a top-level property or an `object`
§7 · R42 — cooperative async on Kotlin coroutines; the held fields are
  written from `viewModelScope` only
§7 · R44 — one state holder per journey; this screen holds no other
  screen's state
§7 · R45, R46 — what the user has in progress survives a system rebuild,
  and what must be found again is read back from where it survives
§7 · R47 — a screen reads a source once per entry, never in a composition
  body
§9 · R53, R54 — `android.util.Log` is the one channel, ERROR for what
  needs a human; no race name, no race date, no segment duration and no
  start time in a message
§10 · R55 — one nominal and one failure test per public function,
  delivered in this lot
§10 · R56 — no test reaches I/O or the system clock; instants are
  injected
§10 · R58 — each forbidden transition §4 names has its own test: a failing
  stop leaves `current` on CONTROL, a failing undo does the same
§10 · R81 — `ControlViewModelTest` carries
  `@RunWith(RobolectricTestRunner::class)` once the subject reaches
  `android.util.Log`
§10 · R82 — the Robolectric runner is the fix, never
  `isReturnDefaultValues = true` on the module
§11 · R62 — the lexicon: Race, Segment, Undo, Stop, Marking; no synonym
  and no abbreviation outside it
§11 · R63 — English identifiers and comments; every exported symbol
  carries one line saying what it guarantees and when it fails
§11 · R64 — no user-facing string is a literal in the code: both
  rejections go through their catalogue key
§12 · R66, R77, R78 — no new dependency inside a lot; the
  `SavedStateHandle` artifact no build file declares is named in the
  report

## Requests

—
