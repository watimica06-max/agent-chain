## Signatures

SegmentMarkingController.onPressEnd — modification, becomes `suspend`

    suspend fun onPressEnd(
      raceId: Long,
      touchDownAtElapsedRealtime: Long,
      heldMs: Long,
      longPressMs: Int,
      slideExceeded: Boolean,
      segmentDistanceM: Double?
    ): MarkingOutcome
      — parameters, return type and outcomes unchanged: `Cancelled` when
        `slideExceeded` is true or `heldMs < longPressMs`, with two cancel
        pulses and no repository call; `Marked(race)` carrying the race
        `markSegment` returns, with one confirm pulse; `Failed(error)`
        carrying `markSegment`'s error, with no pulse. Never null.
      — `suspend` is the whole change. `recordingRepository.markSegment`
        is still non-`suspend` at this point in the sequence; lot-50
        converts it.

UndoMarkingController.undo — modification, becomes `suspend`

    suspend fun undo(raceId: Long): Result<Race>
      — returns `recordingRepository.undoLastMark(raceId)` unchanged,
        success and failure alike; no interpretation of either.

UndoMarkingController.canUndo — unchanged

    fun canUndo(race: Race): Boolean
      — stays non-`suspend`: true when `race.currentSegmentIndex` is
        non-null and greater than 1, false otherwise.

StopRaceController.stop — modification, becomes `suspend`

    suspend fun stop(raceId: Long, atInstant: Instant): Result<Race>
      — returns `recordingRepository.stopRace(raceId, atInstant)`
        unchanged; on success only, `exerciseSessionManager.close()` is
        launched on the controller's own `CoroutineScope` and not
        awaited. That shape is unchanged from lot-45 and stays as it is.
      — `suspend` is the whole change.

ControlViewModel.onUndoClicked — modification, same-module call site wrapped

    fun onUndoClicked()
      — signature unchanged. The `canUndo` guard and its early return
        stay outside; `undoMarkingController.undo(heldRace.id)`, its
        `onSuccess` block (held race replaced, `navigator.onUndo()`) and
        the `recompute()` that follows it move inside
        `viewModelScope.launch`.

ControlViewModel.onStopConfirmed — modification, same-module call site wrapped

    fun onStopConfirmed(atInstant: Instant)
      — signature unchanged. `stopRaceController.stop(heldRace.id,
        atInstant)`, its `onSuccess` block (`stopConfirmVisible` set
        false, `navigator.onStopConfirmed()`) and the `recompute()` that
        follows it move inside `viewModelScope.launch`.

MainRacePageViewModel.onPressEnd — modification, same-module call site wrapped

    fun onPressEnd(
      touchDownAtElapsedRealtime: Long, heldMs: Long, slideExceeded: Boolean
    )
      — signature unchanged. `lastKnownNow` and `segmentDistanceM` are
        still computed before the launch, from the values held at press
        end; `markingController.onPressEnd(...)` and its whole `when`
        over `MarkingOutcome` move inside `viewModelScope.launch`.
        `Cancelled` and `Failed` stay `Unit`.

## Acceptance criteria

- Each of `SegmentMarkingController.onPressEnd`, `UndoMarkingController.undo`
  and `StopRaceController.stop` is reached only from a suspending caller:
  a non-suspending function calling any of the three does not compile.
- A press with `slideExceeded` true produces `Cancelled`, two cancel
  pulses and no call to `markSegment`.
- A press with `heldMs` below `longPressMs` produces the same three
  observations.
- A press with `slideExceeded` false and `heldMs` at or above
  `longPressMs`, `markSegment` succeeding, produces `Marked` carrying the
  race `markSegment` returned and one confirm pulse.
- The same press with `markSegment` failing produces `Failed` carrying
  `markSegment`'s error and no pulse.
- `undo(raceId)` returns the exact `Result` `undoLastMark` returned, on
  success and on failure.
- `stop(raceId, atInstant)` returns the exact `Result` `stopRace`
  returned, on success and on failure.
- A `stop` whose `stopRace` succeeds reaches `ExerciseSessionManager.close()`
  exactly once; a `stop` whose `stopRace` fails never reaches it.
- `ControlViewModel.onUndoClicked` with `canUndo` false makes no call to
  `undoLastMark`.
- `ControlViewModel.onUndoClicked` with `canUndo` true and `undoLastMark`
  succeeding leaves, once the launched coroutine has completed,
  `uiState` computed from the race `undoLastMark` returned and
  `navigator.onUndo()` called once.
- `ControlViewModel.onUndoClicked` with `undoLastMark` failing leaves the
  held race, `uiState` and the navigator unchanged.
- `ControlViewModel.onStopConfirmed` with `stopRace` succeeding leaves,
  once the launched coroutine has completed, `uiState.stopConfirmVisible`
  false and `navigator.onStopConfirmed()` called once.
- `ControlViewModel.onStopConfirmed` with `stopRace` failing leaves
  `uiState.stopConfirmVisible` true and the navigator untouched.
- `MainRacePageViewModel.onPressEnd` producing `Marked` with a race whose
  completion is not COMPLETE leaves, once the launched coroutine has
  completed, `uiState` computed from that race and `navigator.onMarked()`
  called once.
- The same producing `Marked` with a race whose completion is COMPLETE
  calls `navigator.onFinalMarking()` once instead.
- `MainRacePageViewModel.onPressEnd` producing `Cancelled` leaves the
  held race, `uiState` and `navigator.current` unchanged.
- `MainRacePageViewModel.onPressEnd` producing `Failed` leaves the same
  three unchanged.
- `./gradlew :app-wear:check` exits 0 at the end of this lot, no call
  site of the three converted methods left unwrapped in `:app-wear`.

## Dependencies

RaceRecordingRepository — pre-existing; `markSegment`, `undoLastMark` and
  `stopRace` are still non-`suspend` at this point, lot-50 converts them
MarkingOutcome — pre-existing (`Marked(race)` / `Cancelled` / `Failed(error)`)
HapticFeedback — pre-existing (`confirmMarking()`, `cancelMarking()`;
  `HapticFeedbackImpl` modified by lot-51 of this cycle)
Race, RaceCompletion — pre-existing
ExerciseSessionManager.close(): Boolean, `suspend` — modified by lot-45
  of this cycle; reused, never redeclared
WatchRaceNavigator — modified by lot-34 of this cycle
ControlUiState, MainRacePageUiState — pre-existing, unchanged by this lot
viewModelScope — androidx.lifecycle, framework
Trap filed under StopRaceController and ControlViewModel: a plain JVM
  test whose subject touches `viewModelScope`, or holds a collaborator
  with its own `Dispatchers.Main` scope, needs `Dispatchers.setMain` /
  `resetMain`. `MainRacePageViewModelTest` carries neither today and
  needs both once `onPressEnd` launches.

## Conventions

R4 · `./gradlew check` exits 0
R74 · a same-module call site is this lot's own scope
R86 · a test file's owner
R12 · the module each entry is realised in
R19 · a public operation that can block is `suspend`
R24 · an operation reaching outside the process says so by being `suspend`
R25 · what a signature promises, the body delivers
R34 · a caller that receives a failure acts on it
R42 · the presumed execution model
R55 · one nominal and one failure test per public function
R56 · time, readings and I/O injected in a test
R62 · the code's vocabulary — Marking, Undo, Stop
R63 · English, and one line per exported symbol

## Requests

—
