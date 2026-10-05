## Signatures

ImportPreviewViewModel — modification, `:app-phone`
`androidx.lifecycle.ViewModel`, `@HiltViewModel(assistedFactory =
ImportPreviewViewModel.Factory::class)`, `@AssistedInject constructor`

    ImportPreviewViewModel(
      @Assisted success: HyresultParseResult.Success,
      raceRepository: RaceRepository,
      navigator: PhoneNavigator,
      profileSyncPushService: ProfileSyncPushService,
      clock: Clock,
      savedStateHandle: SavedStateHandle
    )

  — three constructor parameters added: `profileSyncPushService`, `clock`,
    `savedStateHandle`. `success`, `raceRepository` and `navigator` are
    unchanged, in that order first.
  — `ImportPreviewViewModel.Factory.create(success: HyresultParseResult.Success)`
    is unchanged: the three added parameters come from Hilt, not from the
    factory.
  — on construction it writes `success.totalTimeMs` and
    `success.segmentDurationsMs` into `savedStateHandle`; when the handle
    already carries that pair, `uiState.totalTime` and
    `uiState.segmentsCount` derive from the saved pair, not from
    `success`. A handle carrying neither leaves the pair derived from
    `success` as today.
  — no read of a repository, a service or the clock happens in a property
    initialiser or in `init`.

ImportPreviewViewModel.onSaveClicked(raceName: String, raceDate: LocalDate) → Unit
  — its whole body runs inside `viewModelScope.launch`; the function
    itself stays non-suspend and returns immediately.
  — calls `raceRepository.saveImportedRace(raceName, startOfDay, segments)`
    exactly as today — `startOfDay` being `raceDate` at the system zone's
    start of day, `segments` being `buildSegments(success.segmentDurationsMs)`.
  — on `Result` success, in this order: clears the rejection message,
    calls `profileSyncPushService.push(permissionGranted = true, at =
    clock.now())` exactly once, then
    `navigator.toRaceDetailAfterImport(race.id)`.
  — on `Result` failure: sets the rejection message to
    `PhoneStringResources.Preview.rejected`, writes that state into
    `savedStateHandle`, calls no push and does not navigate — the screen
    stays where it is.
  — `push`'s `ProfileSyncPushOutcome` is read; `Failure` reaches
    `android.util.Log` at ERROR (R79) naming the operation, carries no
    race name, race date or other personal value (R54), and changes
    neither `uiState` nor the navigation. `Success` changes nothing.
  — `saveImportedRace` is non-suspend today and becomes `suspend` in
    lot-31; the call site written here compiles against both.

ImportPreviewViewModel.onCorrectClicked() → Unit
  — unchanged: `navigator.backToPasteResult()`, no coroutine needed, no
    repository or service reached.

ImportPreviewUiState — modification, `:app-phone`

    ImportPreviewUiState(
      totalTime: String,
      segmentsCount: Int,
      rejectionMessage: LabelRef?
    )

  — `rejectionMessage` is null until a save is refused, and null again on
    a ViewModel rebuilt from a handle that carries no refusal. It is
    never a literal and never a key written for another failure (R80):
    the only value it ever takes is
    `PhoneStringResources.Preview.rejected`.
  — `totalTime` and `segmentsCount` keep their present meaning.

ImportPreviewScreen(
  viewModel: ImportPreviewViewModel, raceName: String, raceDate: LocalDate
) → Unit
  — parameter list unchanged.
  — renders `uiState.rejectionMessage` through `stringResource` when it is
    non-null, and renders nothing in its place when it is null — the
    refusal is distinguishable on screen from a save that was never
    attempted.
  — reads `uiState` through the collection it already uses, never in a
    composition body.

## Acceptance criteria

- `onSaveClicked` with a repository returning a successful `Result`
  leaves `uiState.rejectionMessage` null and moves `PhoneNavigator`'s
  current destination to `RaceDetail` of the saved race's id.
- `onSaveClicked` with a repository returning a failed `Result` sets
  `uiState.rejectionMessage` to `PhoneStringResources.Preview.rejected`
  and leaves `PhoneNavigator`'s current destination unchanged.
- `onSaveClicked` with a repository returning a successful `Result`
  calls `ProfileSyncPushService.push` exactly once, with
  `permissionGranted` true and `at` equal to the injected `Clock`'s
  instant.
- `onSaveClicked` with a repository returning a failed `Result` calls
  `ProfileSyncPushService.push` no times.
- `onSaveClicked` with a repository returning a successful `Result` and a
  push service returning `ProfileSyncPushOutcome.Failure` still moves the
  destination to `RaceDetail` of the saved race's id and still leaves
  `uiState.rejectionMessage` null.
- With the ViewModel's scope running on a dispatcher held unadvanced,
  `onSaveClicked` returns with the repository not yet called; advancing
  that dispatcher then produces the `saveImportedRace` call. The
  repository is never reached on `onSaveClicked`'s own return path.
- A ViewModel built from a `SavedStateHandle` that a previous instance
  refused a save on exposes `uiState.rejectionMessage` equal to
  `PhoneStringResources.Preview.rejected` without any save being
  attempted on it.
- A ViewModel built from a fresh, empty `SavedStateHandle` exposes
  `uiState.rejectionMessage` null.
- A ViewModel built from a `SavedStateHandle` that a previous instance
  wrote a different parsed result's total time and segment durations into
  exposes that saved pair's `totalTime` and `segmentsCount`, not the ones
  its `@Assisted` `HyresultParseResult.Success` carries.
- `ImportPreviewScreen` composed over a state whose `rejectionMessage` is
  `PhoneStringResources.Preview.rejected` displays that resource's text.
- `ImportPreviewScreen` composed over a state whose `rejectionMessage` is
  null displays neither that text nor any other rejection text.
- Tapping "Enregistrer" on `ImportPreviewScreen`, over a repository
  refusing the save, leaves the screen composed and shows the rejection
  text — the tap does not navigate away.

## Dependencies

HyresultParseResult.Success(totalTimeMs: Long, segmentDurationsMs: List<Long>)
  — pre-existing, `:core-domain`
RaceRepository.saveImportedRace(name, date, segments): Result<Race>
  — pre-existing, `:core-domain`; becomes `suspend` in lot-31
Race.id: Long — pre-existing, `:core-domain`
buildSegments(durationsMs: List<Long>) — pre-existing, `:core-domain`
DisplayFormatter.formatDurationTotal, DurationTruncationService.truncateToSeconds
  — pre-existing, `:core-domain`
ProfileSyncPushService.push(permissionGranted: Boolean, at: Instant):
ProfileSyncPushOutcome — pre-existing suspend member, `:core-domain`;
  the class is modified by lot-16 of this cycle, `push`'s signature is not
ProfileSyncPushOutcome.Success / .Failure — pre-existing, `:core-domain`
Clock.now(): Instant — pre-existing, `:core-domain`
LabelRef — pre-existing, `:core-domain`
PhoneStringResources.Preview.rejected — produced by lot-17 of this cycle,
  `:app-phone`; reused, never redeclared, and no new string key is added
PhoneNavigator.toRaceDetailAfterImport(raceId), .backToPasteResult()
  — pre-existing, `:app-phone`
SavedStateHandle, ViewModel, viewModelScope — androidx.lifecycle, framework
android.util.Log — framework

ImportPreviewScreenTest does not exist in the tree; the lot list names it
under Modifies. The lot creates it.

## Conventions

R4 · `./gradlew check` exits 0
R12 · a §9 entry is realised in `:app-phone`
R19 · a public operation that can block is `suspend`
R24 · an operation reaching outside the process says so, and moves to its
      own thread inside its own implementation
R25 · what a signature promises, the body delivers
R34 · a caller that receives a failure acts on it
R42 · cooperative async on Kotlin coroutines
R44 · one state holder per journey — the import journey
R45 · a screen keeps what the user has in progress across a system rebuild
R46 · written where it survives, and read back from there
R47 · a screen reads a source once per entry, never in a composition body
R53 · `android.util.Log`; ERROR is for what needs a human
R54 · no data attached to a person in a log message — a race name is one
R55 · one nominal and one failure test per public function
R63 · English identifiers; every exported symbol carries its line
R64 · no user-facing string literal in the code
R79 · a failure with no state to carry it and no caller to propagate to
      goes to the log of R53
R80 · a failure is never reported through a catalogue key written for
      another one

## Requests

—
