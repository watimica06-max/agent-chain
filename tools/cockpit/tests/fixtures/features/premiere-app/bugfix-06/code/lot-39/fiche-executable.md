## Signatures

### ProjectionViewModel — modification (`:app-wear`)

After the change:

    @HiltViewModel(assistedFactory = ProjectionViewModel.Factory::class)
    class ProjectionViewModel @AssistedInject constructor(
      @Assisted("initialRace") initialRace: Race,
      @Assisted("referenceRace") referenceRace: Race?,
      @Assisted profile: Profile,
      markingController: SegmentMarkingController,
      navigator: WatchRaceNavigator,
      raceRecordingRepository: RaceRecordingRepository,
      savedStateHandle: SavedStateHandle
    ) : ViewModel()

      @AssistedFactory
      interface Factory {
        fun create(
          @Assisted("initialRace") initialRace: Race,
          @Assisted("referenceRace") referenceRace: Race?,
          profile: Profile
        ): ProjectionViewModel
      }
        — unchanged. The two added parameters are supplied by Hilt, not by
          the factory, so `MainActivity`'s
          `hiltViewModel<ProjectionViewModel, ProjectionViewModel.Factory>(
          key = "projection-${race.id}") { factory -> factory.create(race,
          referenceRace, requireNotNull(profile)) }` call site is unchanged.

    val uiState: StateFlow<ProjectionUiState>
      — never null. Its first value is computed before the constructor
        returns, from `initialRace` and from what the `SavedStateHandle`
        carries, with no repository read having happened yet.
      — carries the repository's race instead, recomputed, once the
        constructor-time read described below completes.

    fun onCurrentLapDeltaChanged(lapDelta: LapDeltaResult?) : Unit
      — signature unchanged, not `suspend`, reaches no repository, no
        controller and no manager. Sets the held lap delta, writes it to
        the `SavedStateHandle` and recomputes `uiState` before returning.

    fun onTick(nowElapsedRealtime: Long) : Unit
      — signature unchanged, not `suspend`, reaches no repository, no
        controller and no manager. Sets the held instant, writes it to the
        `SavedStateHandle` and recomputes `uiState` before returning.

    fun onPressEnd(
      touchDownAtElapsedRealtime: Long, heldMs: Long, slideExceeded: Boolean
    ) : Unit
      — signature unchanged, not `suspend`; returns immediately, before the
        marking completes.

What changes:

1. Two constructor parameters are appended, in that order (§12.2).
   `RaceRecordingRepository` is already bound in `:app-wear`
   (`RepositoryModule.provideRaceRecordingRepository`) and
   `SavedStateHandle` needs no `@Assisted`. The three `@Assisted`
   parameters keep their names, their types and their string identifiers —
   `"initialRace"` and `"referenceRace"` stay, the `Race`/`Race?` pair
   requiring them.

2. `onPressEnd` moves its call site inside `viewModelScope.launch` (§7.1).
   `lastKnownNow` is set from `touchDownAtElapsedRealtime` before the
   launch — it reads the argument only. Everything from
   `markingController.onPressEnd(raceId = <the held race's id>,
   touchDownAtElapsedRealtime, heldMs, longPressMs = profile.longPressMs,
   slideExceeded, segmentDistanceM = null)` onwards runs inside that
   coroutine: the outcome branch, the held-race update, the
   `SavedStateHandle` write and the `navigator.onFinalMarking()` /
   `navigator.onMarked()` call. The outcomes keep today's meanings —
   `Marked` with `completion == COMPLETE` navigates to END, `Marked`
   otherwise to MAIN, `Cancelled` and `Failed` leave the held race and
   `navigator.current` unchanged. `MarkingOutcome.Failed(error)` carries a
   `Throwable` this screen has no state to show it in and no caller to
   propagate it to: it is logged at ERROR naming the operation, with no
   race name and no date (R79, R80, R54).

3. A constructor-time repository read is added for the retained race
   (§12.2), and it never runs in a property initialiser (§7.1): inside a
   `viewModelScope.launch` in `init`, `raceRecordingRepository
   .findInProgress()` is read exactly once per instance. Its
   `Result<Race?>` is acted on (R34):
   - success carrying a race whose `id` equals the retained race id — that
     race replaces the held race, and `uiState` is recomputed from it;
   - success carrying `null`, or a race of another `id` — the held race
     stays `initialRace` and `uiState` is not recomputed;
   - failure — the held race stays `initialRace`, `uiState` is not
     recomputed, and the failure is logged at ERROR (R79); no `uiState`
     field carries it, this lot adding none.

4. What the `SavedStateHandle` holds, and what it does not (§12.2):
   - held — the race id the ViewModel works on (`Long`, written at
     construction from `initialRace.id` when the handle carries none, and
     again whenever the held race changes); `lastKnownNow` (`Long`); and
     the current lap delta as the primitives it is built from — its
     `projectedMs` and its `deltaMs`, written when it is a
     `LapDeltaResult.Value` and cleared when it is not. `LapDeltaResult` is
     not Bundle-storable, and §12.2's second gap settles that the
     primitives a value is built from are what gets saved.
   - not held — the race object itself, re-read from the repository as
     above; `referenceRace` and `profile`, re-supplied by `MainActivity`
     through the assisted factory; `uiState`, recomputed from the three
     held values.
   - a lap delta of `LapDeltaResult.Fallback` and no lap delta at all are
     not distinguished in the handle: both feed
     `CumulativeDeltaEstimator.estimate` as "not a `Value`" and produce the
     same `CumulativeDeltaResult.Fallback`, so nothing observable rests on
     telling them apart.
   - what the handle carries wins over `initialRace` for `lastKnownNow` and
     for the lap delta; an empty handle leaves today's initial values —
     `lastKnownNow = initialRace.currentSegmentOpenedAt ?: 0L`, no lap
     delta.

5. `computeState()` is otherwise unchanged: the same
   `CumulativeDeltaEstimator.estimate(raceSegments, currentSegmentIndex,
   currentSegmentElapsedMs, currentLapDelta, referenceSegments)` call, the
   same `ProjectionDeltaBlock` / `ProjectionArrivalBlock` mapping, the same
   `Hidden` pair when `referenceRace` is null, the same elapsed total and
   the same position. `estimate`'s signature is unchanged by lot-03; only
   its `Fallback` cases widened, and this file already renders `Fallback`.

### ProjectionUiState — no change (`:app-wear`)

    data class ProjectionUiState(
      cumulativeDelta: ProjectionDeltaBlock,
      estimatedArrival: ProjectionArrivalBlock,
      elapsedText: String,
      position: String
    )

- No field added, none dropped, none retyped; `ProjectionDeltaBlock`,
  `ProjectionArrivalBlock` and `DeltaTone` keep their variants. §7.1 and
  §12.2 carry no rule for this file, and neither the failed
  `findInProgress` nor `MarkingOutcome.Failed` becomes a rendered state
  here. `decoupage.md` lists it under `Modifies`; the lot leaves it as it
  stands.

### ProjectionScreen — no change (`:app-wear`)

    @Composable fun ProjectionScreen(viewModel: ProjectionViewModel)

- Signature unchanged, and its body unchanged: it collects `uiState` and
  renders the four blocks. It renders no race name, so §9.8 does not reach
  it, and it exposes no new handler. `decoupage.md` lists it under
  `Modifies`; the lot leaves it as it stands.

### ProjectionViewModelTest — modification (`:app-wear`)

- Every construction of `ProjectionViewModel` in this module passes the two
  added parameters (R74). A fake `RaceRecordingRepository` with a settable
  `findInProgress()` `Result` and a `SavedStateHandle()` built in the test
  are what the criteria below are written against.
- `ProjectionViewModel` touches `viewModelScope` after this lot — the state
  document's trap names it today as one of the three that need nothing.
  That stops holding: the test installs
  `Dispatchers.setMain(UnconfinedTestDispatcher())` in `@Before` and
  `Dispatchers.resetMain()` in `@After`.

## Acceptance criteria

Repository and controller calls from a coroutine (§7.1)

- Constructing `ProjectionViewModel` calls no method of
  `SegmentMarkingController` and no method of `RaceRecordingRepository`
  before the constructor returns.
- With `Dispatchers.Main` set to a paused test dispatcher, constructing the
  ViewModel returns with `findInProgress()` not yet called; once the
  dispatcher runs, it has been called exactly once.
- With that same paused dispatcher, `onPressEnd(t, heldMs, false)` returns
  with `SegmentMarkingController.onPressEnd` not yet called; once the
  dispatcher runs, it has been called exactly once, with `raceId` equal to
  the held race's id, `touchDownAtElapsedRealtime` equal to `t`,
  `longPressMs` equal to `profile.longPressMs` and `segmentDistanceM` null.
- With that same paused dispatcher and a controller returning
  `Marked(race)` on a race whose `completion` is `COMPLETE`,
  `WatchRaceNavigator.current` still carries `PROJECTION` when `onPressEnd`
  returns, and carries `END` once the dispatcher runs.
- With a controller returning `Marked(race)` whose `completion` is
  `INCOMPLETE`, `WatchRaceNavigator.current` carries `MAIN` once the
  dispatcher runs, and `uiState.value.position` is that returned race's
  current segment position.
- With a controller returning `MarkingOutcome.Cancelled`, and again with
  one returning `MarkingOutcome.Failed`, `WatchRaceNavigator.current` still
  carries `PROJECTION` once the dispatcher runs and `uiState.value` is
  unchanged from its value before the press.
- `onTick(t)` and `onCurrentLapDeltaChanged(...)` each leave
  `uiState.value` updated by the time they return, with `Dispatchers.Main`
  paused — neither reaches a coroutine.

The retained race, re-read from the repository (§12.2)

- A `SavedStateHandle` carrying the id of `initialRace`, a repository whose
  `findInProgress()` returns that same race with segment 4 open where
  `initialRace` carries segment 2 open: once the launched read completes,
  `uiState.value.position` is the position of segment 4.
- Same setup, the repository returning `Result.success(null)`:
  `uiState.value.position` is the position of segment 2.
- Same setup, the repository returning a race whose `id` differs from the
  retained one: `uiState.value.position` is the position of segment 2.
- Same setup, the repository returning a failed `Result`:
  `uiState.value.position` is the position of segment 2, and constructing
  and collecting the ViewModel raises nothing.
- A fresh, empty `SavedStateHandle` and a repository returning
  `initialRace` with segment 4 open: `uiState.value.position` is the
  position of segment 4 — the id is written from `initialRace` at
  construction.

ViewModel state across a rebuild (§12.2)

- `onTick(t)` called on an instance, then a second instance built from that
  same `SavedStateHandle`, the same `initialRace` and a repository
  returning `null`: the second instance's `uiState.value.elapsedText`
  equals the first's after the tick.
- On a race whose current segment is a `RUN` and a reference race present,
  `onCurrentLapDeltaChanged(LapDeltaResult.Value(projectedMs, deltaMs))`
  called on an instance, then a second instance built from that same
  `SavedStateHandle` and the same races: the second instance's
  `uiState.value.cumulativeDelta` is a `ProjectionDeltaBlock.Value`
  carrying the same text and the same tone as the first's.
- Same setup with a fresh, empty `SavedStateHandle`: the second instance's
  `uiState.value.cumulativeDelta` is `ProjectionDeltaBlock.Fallback`.
- A press marked on an instance, moving the held race from segment 2 to
  segment 3, then a second instance built from that same
  `SavedStateHandle` and a repository returning the race with segment 3
  open: the second instance's `uiState.value.position` is the position of
  segment 3.
- No reference race, whatever the handle carries:
  `uiState.value.cumulativeDelta` is `ProjectionDeltaBlock.Hidden` and
  `uiState.value.estimatedArrival` is `ProjectionArrivalBlock.Hidden`.

Shape unchanged

- `ProjectionUiState` exposes exactly `cumulativeDelta`,
  `estimatedArrival`, `elapsedText` and `position`; `ProjectionScreen`
  keeps its single-parameter signature.
- `ProjectionViewModel.Factory.create` still takes exactly `initialRace`,
  `referenceRace` and `profile`; `MainActivity`'s `PROJECTION` branch is
  not edited by this lot.

## Dependencies

RaceRecordingRepository.findInProgress(): Result<Race?> — pre-existing
  (`:core-domain`), bound in `:app-wear` by
  `RepositoryModule.provideRaceRecordingRepository`; **not `suspend` at
  this lot's turn**, returning the race carrying a non-null current
  segment, or `null` when none does. ⚠️ lot-50 makes it `suspend` later in
  the sequence and names its callers; wrapping this read in
  `viewModelScope.launch` compiles against either shape.
SegmentMarkingController.onPressEnd(raceId: Long,
  touchDownAtElapsedRealtime: Long, heldMs: Long, longPressMs: Int,
  slideExceeded: Boolean, segmentDistanceM: Double?): MarkingOutcome —
  pre-existing (`:app-wear`), not `suspend` at this lot's turn. ⚠️ lot-43
  makes it `suspend` later in the sequence and names `ProjectionViewModel`
  among the callers it converts; the call already sitting inside
  `viewModelScope.launch` is what lets that conversion land. This lot does
  not change it.
MarkingOutcome — pre-existing (`:app-wear`): `Marked(race: Race)`,
  `Cancelled`, `Failed(error: Throwable)`
WatchRaceNavigator.onMarked(): Unit, .onFinalMarking(): Unit — pre-existing
  (`:app-wear`), modified by lot-34 of this cycle; not `suspend`.
  `onMarked` moves PROJECTION or MAIN to MAIN, `onFinalMarking` moves MAIN
  or PROJECTION to END. Reused, never redeclared.
CumulativeDeltaEstimator.estimate(raceSegments: List<Segment>,
  currentSegmentIndex: Int, currentSegmentElapsedMs: Long,
  currentLapDelta: LapDeltaResult?, referenceSegments: List<Segment>):
  CumulativeDeltaResult — lot-03 of this cycle; signature unchanged,
  `Fallback` on a duplicate index, on an absent `currentSegmentIndex`, and
  on a `RUN` current segment whose `currentLapDelta` is not a `Value`.
  Reused, never redeclared.
CumulativeDeltaResult — pre-existing: `Value(cumulativeDeltaMs,
  estimatedArrivalMs)`, `Fallback`
LapDeltaResult — pre-existing (`:core-domain`):
  `Value(projectedMs: Long, deltaMs: Long)`, `Fallback`
Race (`id`, `segments`, `currentSegmentIndex`, `currentSegmentOpenedAt`,
  `completion`), Segment, RaceCompletion, Profile (`longPressMs`) —
  pre-existing (`:core-domain`)
DisplayFormatter.formatDelta / .formatDurationElapsed / .formatPosition,
  DurationTruncationService.truncateToSeconds — pre-existing
  (`:core-domain`), unchanged by this lot
android.util.Log — the project's one diagnostic channel (R53), reachable
  from `:app-wear`
SavedStateHandle — `androidx.lifecycle.SavedStateHandle`, framework;
  `decoupage.md` declares it pre-existing and lots 19–23 already inject it
  into `:app-phone` ViewModels. ⚠️ This is the first one in `:app-wear`;
  no `lifecycle-viewmodel-savedstate` entry exists in
  `gradle/libs.versions.toml` and it is reachable as a transitive of
  `androidx.hilt.navigation.compose`, already on `:app-wear` — R77 and R78
  apply, and the report names it.
viewModelScope, StateFlow, MutableStateFlow — AndroidX / kotlinx.coroutines

Traps carried by these symbols:
- `@HiltViewModel` on an `@AssistedInject` class needs `assistedFactory =
  ProjectionViewModel.Factory::class` explicitly — already carried, and it
  stays once two Hilt-supplied parameters join the assisted ones.
- an `@AssistedInject` constructor with two `@Assisted` parameters of the
  same base type needs string identifiers: `ProjectionViewModel` carries
  the `Race`/`Race?` pair, and `"initialRace"`/`"referenceRace"` must stay
  on both the constructor and the factory method.
- the state document lists `ProjectionViewModel` among the three
  ViewModels touching no coroutine scope, whose tests need no stubbed Main
  dispatcher. This lot ends that: its tests need
  `Dispatchers.setMain(...)`/`Dispatchers.resetMain()`, and the state
  document entry no longer describes the class.

## Conventions

§2 · R4 — `./gradlew check` exits 0, the one definition of done
§2 · R74 — a call site of the changed constructor inside `:app-wear` is
  this lot's own scope: `ProjectionViewModelTest`, and any other
  `:app-wear` file constructing the class, are converted here, never
  deferred
§4 · R12 — §9.x's watch half stays in `:app-wear`; nothing of this lot
  moves into `:core-domain`
§5 · R18 — data crossing a public boundary is immutable; the held race is
  replaced, never mutated
§5 · R19, R24 — what blocks or reaches outside the process is `suspend`;
  the repository read runs inside a coroutine whatever the interface's
  present shape
§5 · R20 — missing data crosses as a nullable or a declared absence type;
  an absent estimate stays `Fallback`, never a zero
§5 · R25 — what a signature promises, the body delivers: the retained id
  is read back, and a value that must outlive a rebuild is written where
  it does
§5 · R26 — no `!!` on a value coming from outside the function; the
  repository's `Result<Race?>` is handled, never force-unwrapped
§6 · R34 — a caller receiving a failure acts on it: the `findInProgress`
  `Result` and the `MarkingOutcome.Failed` outcome are both read
§6 · R79 — a failure this screen can neither carry into its own state nor
  propagate is logged at ERROR, naming the operation
§6 · R80 — no failure reported through a catalogue key written for
  another case; §10 names no key for a refused mark on this screen, so the
  log is the whole of the report
§7 · R39 — dependencies passed as constructor arguments, never read from a
  top-level property or an `object`
§7 · R42 — cooperative async on Kotlin coroutines; the held fields are
  written from `viewModelScope` only
§7 · R44 — one state holder per journey; this screen holds no other
  screen's state
§7 · R45, R46 — what the user has in progress survives a system rebuild,
  and what must be found again is read back from where it survives
§7 · R47 — a screen reads a source once per entry, never in a composition
  body
§9 · R53, R54 — `android.util.Log` is the one channel, ERROR for what
  needs a human; no race name, no date, no duration, no pace in a message
§10 · R55 — one nominal and one failure test per public function,
  delivered in this lot
§10 · R56 — no test reaches I/O or the system clock; instants are injected
§11 · R62 — the lexicon: Race, Segment, Reference, Delta, Cumulative,
  Elapsed, Marking, EstimatedArrival, LapDelta, Fallback; no synonym
§11 · R63 — English identifiers and comments; every exported symbol
  carries one line saying what it guarantees and when it fails
§11 · R64 — no user-facing string is a literal in the code
§12 · R66, R77, R78 — no new dependency inside a lot; the
  `SavedStateHandle` artifact no build file declares is named in the report

## Requests

—
