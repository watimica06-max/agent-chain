## Signatures

RaceListViewModel.uiState: StateFlow<RaceListUiState>
  — after: built from RaceRepository.observeAll(): Flow<Result<List<Race>>>
    (lot-31). A success emission maps to RaceListUiState exactly as
    today. A Result.failure(RaceQueryFailure) emits nothing new: uiState
    keeps the value it last held — the initial RaceListUiState(emptyList())
    when no success has been received — and the failure is written once
    to android.util.Log at ERROR. RaceListUiState gains no field and no
    catalogue key.

RaceDetailViewModel.uiState: StateFlow<RaceDetailUiState>
  — after: combine(observeAll(): Flow<Result<List<Race>>>,
    observeReference(): Flow<Result<Race?>>, dialogState) (lot-31). A
    success on both flows maps as today, lastKnownRace included. A
    Result.failure(RaceQueryFailure) on either flow leaves uiState at the
    value it last held and lastKnownRace unchanged, and is written once
    to android.util.Log at ERROR. RaceDetailUiState and SegmentRowUiState
    gain no field.

HomeViewModel (:app-wear) — its init observeReference collector
  — after: collects Flow<Result<Race?>> (lot-31). A success sets
    currentReference and recomputes as today. A
    Result.failure(RaceQueryFailure) leaves currentReference unchanged,
    triggers no recompute — so uiState keeps the referenceLineText it
    last carried — and is written once to android.util.Log at ERROR.
    HomeUiState gains no field.

PreparationViewModel (:app-wear) — its init observeReference collector
  — after: collects Flow<Result<Race?>> (lot-31). A success sets
    referenceRace and, on the first success only, calls
    raceLaunchController.openPreparation(race) as today. A
    Result.failure(RaceQueryFailure) leaves referenceRace unchanged, does
    not call openPreparation, leaves `opened` false, leaves uiState null,
    and is written once to android.util.Log at ERROR. PreparationUiState
    gains no field.

MainActivity.WatchApp (:app-wear) — its referenceRace read
  — after: collects RaceRepository.observeReference():
    Flow<Result<Race?>> (lot-31). The composable holds the Race? of the
    last success, null before any. A Result.failure(RaceQueryFailure)
    leaves that value unchanged and is written once to android.util.Log
    at ERROR from a side effect, never from the composition body.

ProfileSyncListenerServiceTest (:app-wear test) — its fake RaceRepository
  — after: overrides the nine methods on their new shapes (lot-31) —
    setAsReference, rename, delete, saveImportedRace, saveRecordedRace
    with its two added parameters, findById returning Result<Race?>,
    replaceReference, all suspend, and observeAll/observeReference
    returning Flow<Result<List<Race>>>/Flow<Result<Race?>>. It records
    replaceReference's argument and returns Result.success(Unit) exactly
    as today; every other override keeps throwing
    UnsupportedOperationException. The tests around it assert the same
    things they assert today — this lot adapts the fake to the changed
    interface and nothing else. Deferred here from lot-31 under R72,
    lot-31 touching no :app-wear source.

## Acceptance criteria

- After observeAll has emitted two races, a failure emission leaves the race list showing those same two races
- A failure emission as observeAll's first emission leaves the race list empty and adds no message on screen
- After the detail screen has shown a race, a failure emission on observeAll leaves that same race on screen, with its name, date and segment rows unchanged
- A failure emission on observeReference leaves the detail screen's reference marker as it was
- After the home screen has shown a reference race, a failure emission on observeReference leaves that same reference line on screen
- A failure emission as observeReference's first emission leaves the home screen with no reference line and adds no message on screen
- A failure emission as observeReference's first emission on the preparation screen calls raceLaunchController.openPreparation not at all and leaves the preparation state null
- After a first success, a failure emission on observeReference leaves PreparationViewModel's reference race at the one last received
- A failure emission on observeReference leaves the reference race the watch's screens receive at its last successful value, null when none has arrived
- Each of the five collectors writes exactly one ERROR log entry per failure emission, carrying the failure's message and no race name, race date or start time
- ProfileSyncListenerServiceTest's existing assertions on applyIncoming and on the decode failure still hold, its fake RaceRepository still recording every replaceReference call and returning success

## Dependencies

RaceQueryFailure — produced by lot-55
RaceRepository.observeAll(): Flow<Result<List<Race>>> — produced by lot-31
RaceRepository.observeReference(): Flow<Result<Race?>> — produced by lot-31
RaceRepository's nine methods on their new shapes — produced by lot-31
ProfileSyncListenerService, ProfileSyncPushService.applyIncoming — pre-existing, untouched by this lot
Race, RaceRepository — pre-existing (:core-domain)
RaceListUiState, RaceDetailUiState, SegmentRowUiState — pre-existing (:app-phone), unchanged
HomeUiState, PreparationUiState — pre-existing (:app-wear), unchanged
RaceLaunchController.openPreparation — pre-existing (:app-wear)
android.util.Log — framework, pre-existing
collectAsStateWithLifecycle — androidx.lifecycle, pre-existing

## Conventions

R34 · a caller that receives a failure acts on it, never drops it
R47 · a screen reads a source once per entry, never in a composition body
R53 · no direct write to standard output; android.util.Log, ERROR for what needs a human
R54 · no data attached to a person in a log message
R55 · one nominal and one failure test per public function, in this lot
R72 · deliverable while the only remaining project-wide failure is a call site another lot's sheet adapts — this lot closes lot-31's deferral on ProfileSyncListenerServiceTest (:app-wear)
R64 · no user-facing string as a literal in the code
R75 · a source failure never reads as the interface's ordinary success shape
R76 · `catch` does not resubscribe: no later success follows a failure emission unless the boundary retries
R79 · a failure a caller can neither carry into its own state nor propagate is logged at ERROR, naming the operation
R80 · no failure reported through a catalogue key written for another one; until §10 names a key, the R79 log is the whole report
R81 · a unit test whose subject reaches android.util.Log carries @RunWith(RobolectricTestRunner::class)
R82 · such a test is fixed under R81, never with isReturnDefaultValues = true

## Requests

architecte/detailleur-lot-56.md
