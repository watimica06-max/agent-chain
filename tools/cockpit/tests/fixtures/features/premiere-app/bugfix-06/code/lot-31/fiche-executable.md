## Signatures

RaceRepository (:core-domain) — modified interface

  suspend fun setAsReference(raceId: Long): Result<Unit>
    — after: suspend. Same outcomes as today — failure when no race is
      stored under raceId, success otherwise — plus Result.failure
      carrying the store's own failure instead of raising it. Clearing
      the flag on whichever race held the reference and setting it on
      raceId is one Room transaction: no reader ever observes a state
      with no reference between the two.

  suspend fun rename(raceId: Long, name: String): Result<Unit>
    — after: suspend. The trim-and-refuse rule is unchanged (trimmed
      name, refused when empty or longer than 40 characters, stored name
      left as it was on a refusal). A store failure comes back as
      Result.failure instead of raising.

  suspend fun delete(raceId: Long): Result<Unit>
    — after: suspend. Same outcomes; a store failure comes back as
      Result.failure instead of raising.

  suspend fun saveImportedRace(
    name: String, date: Instant, segments: List<Segment>
  ): Result<Race>
    — after: suspend, and the name is trimmed before anything is
      written. Result.failure, with nothing written, when the trimmed
      name is empty or longer than 40 characters — the same bound rename
      applies. On success the stored and returned Race carries the
      trimmed name, origin IMPORTED, completion COMPLETE, isReference
      false, no in-progress state. Result.failure when the row read back
      after the write is absent — never a force-unwrap. The write and
      the read-back are one transaction.

  suspend fun saveRecordedRace(
    raceId: Long, name: String, date: Instant, segments: List<Segment>,
    completion: RaceCompletion, retainedFactors: List<RetainedFactor>,
    rejectedCalibrations: List<RejectedCalibration>
  ): Result<Race>
    — after: suspend, and carries retainedFactors and
      rejectedCalibrations — two added parameters, stored on the created
      race and readable back on the returned Race in the order given.
      The same trim-and-refuse rule as saveImportedRace, checked before
      anything is written. The dedup lookup on raceId and the write are
      one transaction; a raceId already stored returns that stored race
      unchanged, writing nothing — its own retainedFactors and
      rejectedCalibrations left as they were. An INCOMPLETE completion
      still drops the segments carrying no duration. Result.failure when
      the row read back after the write is absent.

  suspend fun findById(raceId: Long): Result<Race?>
    — after: suspend, and the return carries the store's failure.
      Result.success(null) when no race is stored under raceId;
      Result.failure only when the store itself fails. Absence is never
      a failure and a failure is never null.

  suspend fun replaceReference(race: Race?): Result<Unit>
    — after: suspend, and returns the outcome of its own write instead
      of always succeeding. Clearing the previous reference and writing
      race as the sole reference are one transaction. Result.failure
      when the row read back after that write is absent, or when the
      store fails; Result.success, with the reference cleared and
      nothing written, when race is null.

  fun observeAll(): Flow<Result<List<Race>>>
    — after: the element type is Result<List<Race>>, not List<Race>. A
      success emission carries exactly today's list, order and empty
      case — Race.date descending, ties broken by insertion order
      descending, empty when nothing is stored — and emits again on
      every change to the stored races. A store failure is emitted once
      as Result.failure(RaceQueryFailure) naming the query, after which
      the flow completes: no later emission, no retry, no resubscribe.
      An empty list never stands for a failure, and a failure never
      passes as an empty list or as silence.

  fun observeReference(): Flow<Result<Race?>>
    — after: the element type is Result<Race?>, not Race?. A success
      emission carries the race flagged isReference, or null when none
      is set, and emits again whenever the reference changes. Same
      failure emission and same completion after it as observeAll. Null
      means "no reference set", never "the read failed".

RaceRepositoryImpl (:core-data) — modified

  Same nine signatures. Every RaceDao call runs on Dispatchers.IO from
  inside the method itself, never on the caller's thread, and whatever
  it raises comes back as that method's own Result.failure. Both flows
  map the stored entities as today, turn a failure of the underlying
  DAO flow into a single Result.failure(RaceQueryFailure) emission, and
  carry flowOn(Dispatchers.IO). No `!!` on a row read back from the
  store: the absence is the declared failure above. The class's
  constructor is unchanged — RaceRepositoryImpl(raceDao: RaceDao).

ProfileSyncPushService (:core-domain) — modified

  suspend fun push(permissionGranted: Boolean, at: Instant): ProfileSyncPushOutcome
    — after: same parameters, same return type, no new
      ProfileSyncPushOutcome variant. Reads
      raceRepository.observeReference().first() and
      raceRepository.observeAll().first(), both now Result-carrying. On
      a Result.failure from either, returns ProfileSyncPushOutcome
      .Failure without calling transport.send and without calling
      profileRepository.markSyncSuccess — a payload whose reference is
      absent and whose history is empty is never sent. On success from
      both, behaves exactly as today: the profile, the reference race in
      full, the 20 most recent races of observeAll's own order as
      RaceHistoryEntry, then delivery, then markSyncSuccess. applyIncoming
      is untouched.

RecordedRaceListenerService (:app-phone) — modified

  @Inject lateinit var profileRepository: ProfileRepository
    — added field, resolved from the binding RepositoryModule
      (:app-phone) already exposes

  override fun onMessageReceived(event: MessageEvent): Unit
    — after: for RECORDED_RACE_PATH, the only thing running on the
      thread Play Services delivers on is the path test and the launch
      into serviceScope; the decode, the save, the correction-factor
      write and the acknowledgement all run inside that launch. Whatever
      PayloadCodec.decodeRecordedRace raises is caught and represented as
      Result.failure(PayloadDecodingFailure(<message naming the
      recorded-race decode>, cause = <caught>)) — the payload is
      dropped, nothing is saved, no acknowledgement is sent, and no
      exception reaches the binder thread. On a decoded payload, calls
      raceRepository.saveRecordedRace passing payload.retainedFactors
      and payload.rejectedCalibrations through. On its Result.failure:
      logs at ERROR and sends no acknowledgement. On its success: writes
      the phone's correction factor — the factor of the last entry of
      payload.retainedFactors, converted to Float, and nothing at all
      when that list is empty — through
      profileRepository.updateCorrectionFactor, logs that call's own
      Result.failure at ERROR without letting it stop anything, then
      sends ackTransport.send(payload.raceId). Today's ordering holds:
      the acknowledgement follows the successful race write.

  override fun onDestroy(): Unit
    — added: cancels serviceScope, then calls super.onDestroy().

Call sites this lot adapts to the signatures above, changing nothing else
about them

  RaceRepositoryImplTest (:core-data), ProfileSyncPushServiceTest
  (:core-domain), RecordedRaceListenerServiceTest, ProfileViewModelTest,
  ProfileScreenTest, ImportPreviewViewModelTest, ImportPreviewScreenTest,
  MainActivityTest (:app-phone) — each carries a fake RaceRepository
  overriding all nine methods, or calls one of them directly; each is
  brought onto the new method set and the new flow element type. R74
  puts the two :core-domain files in this lot's scope by construction;
  the :app-phone test files sit in the same test source set as
  RecordedRaceListenerServiceTest, which this lot touches, so
  :app-phone:check cannot exit 0 without them.

## Acceptance criteria

- saveImportedRace given a name of spaces only stores no race and returns a failure, and observeAll's next success emission carries the same races as before the call
- saveImportedRace given a name of 41 trimmed characters stores no race and returns a failure
- saveImportedRace given a name padded with spaces stores and returns a race whose name is the trimmed value
- saveRecordedRace given a name of spaces only, or of 41 trimmed characters, stores no race and returns a failure
- saveRecordedRace given two retained factors and one rejected calibration returns a race carrying those same three values, and a repository rebuilt on the same database reads them back unchanged
- saveRecordedRace called twice with the same raceId creates one race only, and the second call returns the first one's retained factors and rejected calibrations unchanged
- saveImportedRace, saveRecordedRace and replaceReference each return a failure, rather than raising, when the row is absent at the read-back
- replaceReference returns a failure when the write it performs fails, and a success with no reference set when it is given null
- setAsReference on a database already holding a reference leaves exactly one reference race, and a reader collecting observeReference throughout never receives a success emission carrying null
- observeAll's first success emission after two races are stored carries both, most recent date first
- observeAll emits Result.failure carrying a RaceQueryFailure, and no further emission, when its underlying query fails
- observeAll emits a success carrying an empty list, not a failure, when no race is stored
- observeReference emits Result.failure carrying a RaceQueryFailure, and no further emission, when its underlying query fails
- observeReference emits a success carrying null, not a failure, when no reference is set
- findById returns a success carrying null for a raceId never stored, and a failure only when the store fails
- Every RaceRepository method that reaches the DAO returns a failure instead of raising when the DAO raises
- push returns Failure and calls neither the transport nor markSyncSuccess when observeReference's first emission is a failure
- push returns Failure and calls neither the transport nor markSyncSuccess when observeAll's first emission is a failure
- push, both flows succeeding, sends one payload carrying the reference race and at most 20 history entries and returns Success
- onMessageReceived, given a recorded-race message whose bytes fail to decode, does not throw, saves nothing, sends no acknowledgement, and reports the failure as a PayloadDecodingFailure
- onMessageReceived saves the received race through saveRecordedRace with the payload's retained factors and rejected calibrations
- onMessageReceived, on a payload carrying retained factors, calls ProfileRepository.updateCorrectionFactor with the last one's factor
- onMessageReceived, on a payload carrying no retained factor, calls updateCorrectionFactor not at all and still acknowledges
- onMessageReceived sends the acknowledgement after a successful save, and sends none when the save returns a failure
- onMessageReceived returns before the save reaches the database: nothing touches RaceRepository on the thread the message is delivered on
- onDestroy cancels serviceScope: a coroutine already launched into it before onDestroy is cancelled and does not complete

## Dependencies

RaceRepository, Race, Segment, RaceCompletion, RaceOrigin, RetainedFactor, RejectedCalibration — pre-existing (:core-domain)
RaceQueryFailure — produced by lot-55
RaceDao.upsertAndFind, RaceDao.findOrSaveRecordedRace, RaceDao.replaceReference, RaceDao.findInProgress — produced by lot-09
RaceEntity carrying the unique index on sourceRaceId — produced by lot-08
RecordedRacePayload carrying retainedFactors and rejectedCalibrations — produced by lot-53
PayloadDecodingFailure (:core-sync) — produced by lot-52
PayloadCodec.decodeRecordedRace — pre-existing, still synchronous at this point in the sequence (turned suspend by lot-11, later in the sequence)
ProfileRepository.updateCorrectionFactor — pre-existing, already suspend and already validating against 0.70..1.40
ProfileSyncPushOutcome, ProfileSyncPayload, RaceHistoryEntry, ProfileSyncTransport, WatchHistoryStore — pre-existing (:core-domain)
RecordedRaceAckTransport — pre-existing (:core-domain)
android.util.Log, kotlinx.coroutines, Room — framework and declared dependencies

## Conventions

R8 · no committed Room migration modified; a structural change adds a new one
R17 · no quantity carrying a unit, a scale or an identity as a bare primitive in a public signature
R19 · every public operation that can block is suspend
R20 · missing data crosses a public boundary as a nullable or a declared absence type
R21 · a value the corpus bounds is checked at every place it enters — the 1-to-40 trimmed name on both save paths, the correction factor taken from a sync payload
R22 · anything that computes states what it returns for every input it cannot compute on
R24 · an operation reaching outside the process says so by being suspend, and moves to the thread that work belongs on inside its own implementation
R25 · what a signature promises, the body delivers — an argument it takes is read
R26 · no `!!` on a value coming from outside the function
R30 · no empty and no generic catch
R31 · an error crossing a module boundary is of a type that module declares
R32 · data entering from outside the process is validated at the module that receives it
R33 · every call leaving the process returns its failure as a value, never a thrown exception crossing the boundary
R34 · a caller that receives a failure acts on it — never dropped
R37 · a write holding an invariant is atomic against a concurrent reader — clearing the previous reference and setting the new one is one write
R42 · cooperative async on Kotlin coroutines; no shared mutable state between coroutines
R46 · what must be found again after the process dies is written where it survives
R48 · anything one moment opens and another must end is released by the module that opened it, tied to that module's own scope
R53 · no direct write to standard output; android.util.Log, ERROR for what needs a human
R54 · no data attached to a person in a log message — not the race name, the race date, a segment duration, nor the correction factor's value
R55 · one nominal and one failure test per public function, in this lot
R56 · no test reaches the network, the data layer or a sensor
R57 · each fact the corpus states as always true has a test attempting to violate it — at most one reference race, a name of 1-40 trimmed characters
R61 · each write that must precede a return has a test interrupting between the write and the return — the imported-race save, the reference switch
R63 · every exported symbol carries one line saying what it guarantees and when it fails
R72 · deliverable while the only remaining project-wide failure is a call site another lot's sheet adapts
R73 · the report names the failing call site and the lot that adapts it — ProfileSyncListenerServiceTest (:app-wear), and the five collectors of the two guarded flows with their tests, RaceListViewModel, RaceDetailViewModel (:app-phone), HomeViewModel, PreparationViewModel and MainActivity (:app-wear), all of them lot-56's
R74 · a call site in the module the changed signature lives in is this lot's own scope — ProfileSyncPushService and ProfileSyncPushServiceTest (:core-domain)
R75 · a source failure never reads as the interface's ordinary success shape
R76 · `catch` does not resubscribe: no later success follows a failure emission unless the boundary retries
R81 · a unit test whose subject reaches android.util.Log carries @RunWith(RobolectricTestRunner::class)
R82 · such a test is fixed under R81, never with isReturnDefaultValues = true

## Requests

architecte/detailleur-lot-31.md
