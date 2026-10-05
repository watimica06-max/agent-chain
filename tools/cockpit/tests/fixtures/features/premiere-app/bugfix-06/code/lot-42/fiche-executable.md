## Signatures

EndOfRaceUiState(
  totalTime: String?, finalDeltaText: String?, finalDeltaTone: DeltaTone?,
  dateTime: String, isIncomplete: Boolean
)
  — modification: `totalTime` becomes `String?`, from `String`
  — `totalTime` null means the total cannot be computed; never an empty
    string, never a formatted zero, never a placeholder text
  — `finalDeltaText`, `finalDeltaTone`, `dateTime`, `isIncomplete`
    unchanged, `dateTime` still non-null on every input

EndOfRaceViewModel.uiState: StateFlow<EndOfRaceUiState>
  — modification, value only; the property's own type is unchanged
  — one value, computed at construction, never re-emitted

EndOfRaceViewModel.computeState(
  finalRace: Race, referenceRace: Race?
) → EndOfRaceUiState
  — private; observed through `uiState`
  — modification: `totalTime` is null when `finalRace.segments` carries
    two entries of the same `index`, whatever that index and whatever
    their `durationMs` — the settled outcome, consistent with lot-03's
    `finalDelta` returning null on the same input
  — otherwise unchanged:
    `DisplayFormatter.formatDurationTotal(DurationTruncationService.truncateToSeconds(Σ durationMs))`,
    a null `durationMs` still counting as 0 — a race of distinct indices
    all carrying a null `durationMs` yields a formatted zero, a computed
    value and not an absence
  — `finalDeltaText` and `finalDeltaTone` are both null when
    `referenceRace` is null — unchanged — and both null when
    `CumulativeDeltaEstimator.finalDelta` returns null, which covers the
    duplicate index; otherwise the formatted delta and its tone,
    AHEAD below 0, BEHIND above, ZERO at 0 — unchanged
  — `dateTime` and `isIncomplete` are produced on every input, the
    duplicate one included

EndOfRaceViewModel.init
  — modification: `exerciseSessionManager.close()` is called from inside
    `viewModelScope.launch`, exactly once per construction, and no
    longer from `init`'s own body
  — the `retainedFactors` write to `profileRepository` keeps its own
    existing `viewModelScope.launch`
  — the constructor stays `@AssistedInject` under
    `@HiltViewModel(assistedFactory = EndOfRaceViewModel.Factory::class)`,
    with the `@Assisted("finalRace")` / `@Assisted("referenceRace")`
    identifiers on both the constructor and `Factory.create`

EndOfRaceScreen(viewModel: EndOfRaceViewModel) → Unit
  — modification: the total item is composed only when
    `uiState.totalTime` is non-null, the way the final-delta item is
    already skipped when its text or its tone is null
  — the incomplete item, the date item and the "Terminer" item are
    unchanged, and each still renders on its own condition when the
    total is omitted
  — no new key and no new literal: the omitted line displays nothing

## Acceptance criteria

- A race of 30 distinct indices, three of them carrying 3 700 000 ms and
  the rest a null durationMs, produces a uiState whose totalTime is
  formatDurationTotal(truncateToSeconds(11 100 000))
- A race of 30 distinct indices all carrying a null durationMs produces
  a uiState whose totalTime is formatDurationTotal(0), non-null
- A race whose segments carry index 5 twice produces a uiState whose
  totalTime is null
- A race whose segments carry index 5 twice, both entries carrying a
  null durationMs, produces a uiState whose totalTime is null
- A race whose segments carry index 5 twice produces a uiState whose
  dateTime is formatDateTime of that race's date, and whose isIncomplete
  is true for a race of completion INCOMPLETE
- A race whose segments carry index 5 twice, with a reference race,
  produces finalDeltaText and finalDeltaTone both null
- A race of distinct indices with a reference race, its first segment
  10 000 ms against the reference's 8 000 ms, produces the formatted
  2 000 ms delta and DeltaTone.BEHIND
- A race with referenceRace null produces finalDeltaText and
  finalDeltaTone both null
- The screen built on a race of distinct indices displays the formatted
  total
- The screen built on a race whose segments carry index 5 twice displays
  no total, and still displays the race's date and "Terminer"
- The screen built on a race whose segments carry index 5 twice and
  whose completion is INCOMPLETE still displays "Course incomplète"
- Constructing the view model while the exercise session is open ends
  that session exactly once
- Constructing the view model on a Main dispatcher whose scheduler has
  not run leaves the exercise session unended until the scheduler runs

## Dependencies

Race — pre-existing (id, name, date, origin, isReference, completion,
  segments, retainedFactors, rejectedCalibrations, currentSegmentIndex,
  currentSegmentOpenedAt, sentAt)
Segment — pre-existing (index, type, station, durationMs)
RaceCompletion — pre-existing (COMPLETE, INCOMPLETE)
DeltaTone — pre-existing, in `EndOfRaceUiState.kt` (AHEAD, BEHIND, ZERO)
DisplayFormatter.formatDurationTotal / formatDelta / formatDateTime —
  pre-existing, untouched by this block
DurationTruncationService.truncateToSeconds — pre-existing
CumulativeDeltaEstimator.finalDelta(List<Segment>, List<Segment>) →
  `Long?` — lot-03, earlier in this block; null on a duplicate index in
  `raceSegments`, milliseconds otherwise, signed, negative meaning ahead
ExerciseSessionManager.close() — pre-existing, `fun close()` today;
  lot-45 makes it `suspend` later in the sequence, and a call site inside
  `viewModelScope.launch` compiles against either form
ProfileRepository.updateCorrectionFactor(Float) → Result<Unit> —
  pre-existing and already `suspend`, already called inside a launch
WatchRaceNavigator — pre-existing
WatchStringResources.End — pre-existing, untouched: the decision adds no
  text and no key
EndOfRaceViewModelTest — pre-existing, in the lot's Modifies list; it
  already installs `Dispatchers.setMain(UnconfinedTestDispatcher())`,
  which the added launch makes mandatory rather than incidental
EndOfRaceScreenTest — pre-existing; the rendering criteria land there,
  and the lot's Modifies list names `EndOfRaceScreen` without naming this
  file
architecte/detailleur-lot-03.md — open request: lot-03 leaves `:app-wear`
  uncompilable and this lot is what restores it

## Conventions

R4 · `./gradlew check` exits 0 — reachable here, this lot closing what
     lot-03 opened
R12 · the end-of-race page (§8.3) is realised in `:app-wear`
R20 · missing data as a nullable, never an invented default
R22 · what it returns for every input it cannot compute on, never a value
      that reads as valid
R25 · what a signature promises, the body delivers — a handle it is
      handed is awaited
R26 · no `!!` on a value coming from outside the function
R29 · a duration is truncated only at the point it is displayed
R42 · cooperative async on coroutines, no work outside a scope
R44 · one state holder per journey — the end-of-race page's state stays
      in this view model
R47 · a screen reads a source once per entry, never in a composition body
R48 · what one moment opens, another releases, tied to the module's own
      scope
R55 · a nominal test and a failure test per public function, same lot
R57 · a test building a race list violating "exactly 30 segments indexed
      1–30", the duplicate index being that violation
R62 · the lexicon — Race, Segment, Total, Delta, CumulativeDelta,
      ExerciseSession
R63 · English, and one line per exported symbol saying what it guarantees
      and when it fails
R64 · no user-facing string literal — the omitted total adds no key to
      `WatchStringResources`

## Requests

—
