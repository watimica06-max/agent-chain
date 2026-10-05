## Signatures

RaceRecordingRepository — modification. Every operation becomes
`suspend`; the store behind the implementation becomes the database.

    suspend fun startClock(startedAt: Instant, startedAtElapsedRealtime: Long): Result<Race>
      — the returned Race carries the id the stored row was given, not an
        id assigned in the process; never an id a stored race already
        carries, whatever process stored it. The race, its segments and
        its (empty) calibration lists are written before the call returns

    suspend fun markSegment(raceId: Long, markedAtElapsedRealtime: Long, segmentDistanceM: Double?): Result<Race>
      — reads the race under raceId from the database, so a race a
        previous process started is markable; writes the closed segment's
        duration, the next segment's index and opening instant — or, past
        segment 30, completion COMPLETE with both current-segment fields
        null — and any calibration entry the closed RUN segment produced,
        before returning. Result.failure, the stored race unchanged, when
        raceId carries no stored race or no current segment; Result.failure
        for anything raised anywhere in the body, the profile read and the
        correction-factor computation included — never a thrown exception

    suspend fun findInProgress(): Result<Race?>
      — reads the database, never an in-process map: success carrying the
        stored race whose currentSegmentIndex is non-null, success
        carrying null when no stored race carries one. Never waits on a
        concurrent markSegment

    suspend fun undoLastMark(raceId: Long): Result<Race>
      — reopens the most recently closed segment and writes the result
        before returning. Success carrying the race unchanged, writing
        nothing, when currentSegmentIndex is 1 or null, when the segment
        it would reopen carries no duration, and when that segment is
        absent from race.segments altogether

    suspend fun stopRace(raceId: Long, atInstant: Instant): Result<Race>
      — reads atInstant and stores it as the race's stoppedAt; sets
        completion INCOMPLETE, clears currentSegmentIndex and
        currentSegmentOpenedAt, leaves segments and isReference untouched
        — the segment in progress stays abandoned, with no duration and
        never truncated to atInstant. Written before returning

    suspend fun markSent(raceId: Long, at: Instant): Result<Race>
      — sets sentAt to at, every other field unchanged, and writes it
        before returning. Result.failure, the stored race unchanged, on a
        raceId nothing is stored under. Never removes the race from
        observeRecorded

    fun observeRecorded(): Flow<List<Race>>
      — unchanged signature. Emits the recorded races this repository
        holds — currentSegmentIndex null, not yet erased — most recent
        first, ordered by date descending then by id descending, the
        second key explicit and never a sort's stability. Re-emitted after
        every mutating call. A race a previous process stored and this one
        has not touched is not re-emitted; a race a previous process
        started and this one stops is

    suspend fun eraseRecorded(raceId: Long): Result<Unit>
      — drops the race from observeRecorded's next emission and deletes
        its stored row and children in one transaction. Success, writing
        nothing, when nothing is stored under raceId

RaceRecordingRepositoryImpl — modification.

    class RaceRecordingRepositoryImpl(
      private val profileRepository: ProfileRepository,
      private val raceDao: RaceDao
    ) : RaceRecordingRepository

      — every DAO call runs on Dispatchers.IO, chosen inside this class
        and never on a caller's word; the profile is read as a plain
        suspend call, no runBlocking anywhere. Nothing that guards shared
        state is held across a suspension point, so findInProgress returns
        while another method is suspended on the database or the profile
      — internal fun findById(raceId: Long): Race? becomes
        `internal suspend fun findById(raceId: Long): Race?`, reading the
        database, null when no row carries that id

Race — modification, one field added.

    data class Race(
      …, val sentAt: Instant? = null, val stoppedAt: Instant? = null
    )

      — stoppedAt is the wall-clock instant stopRace was given; null on
        every race stopRace has not ended, a COMPLETE one included.
        Nothing reads it: a race's total stays the sum of its segments

RaceEntity — modification, two nullable columns added.

    data class RaceEntity(
      …, val sourceRaceId: Long? = null,
      val stoppedAtEpochMs: Long? = null,
      val sentAtEpochMs: Long? = null
    )

      — each is Instant.toEpochMilli() of the matching Race field, null
        when that field is null

HyroxDatabase — modification: `version = 4`.

RaceDatabaseMigrations — modification, one migration added beside the two
already committed.

    val MIGRATION_3_4: Migration  // 3 → 4
      — adds stoppedAtEpochMs and sentAtEpochMs to races, both nullable
        integers, both NULL on every row already stored. MIGRATION_1_2 and
        MIGRATION_2_3 keep the SQL they carry

RepositoryModule (:app-wear) — modification.

    provideHyroxDatabase — addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4)
    provideRaceRecordingRepository(
      profileRepository: ProfileRepository, raceDao: RaceDao
    ): RaceRecordingRepository

RepositoryModule (:app-phone) — modification: the same `addMigrations`
line, and nothing else in that module.

PhoneRaceRecordingRepository — modification: every method becomes
`suspend`, each keeping the outcome it already returns.

## Acceptance criteria

- startClock returns a race whose id the database assigned, and a read of
  that id returns a stored row once the call has returned
- A repository built on a database another instance already wrote to
  returns, from findInProgress(), that instance's race with the same id,
  currentSegmentIndex and currentSegmentOpenedAt
- startClock on a repository built on a database already holding a race
  returns a race whose id differs from every stored race's id
- findInProgress() returns success carrying null when no stored race
  carries a current segment
- markSegment on a raceId a previous repository instance stored succeeds,
  and the stored race then carries the closed segment's duration and the
  next segment open at the marking instant
- markSegment closing segment 30 stores completion COMPLETE with both
  current-segment fields null
- markSegment closing a RUN segment with a non-null distance stores the
  resulting calibration entry: a repository reading that race back
  carries it in retainedFactors or in rejectedCalibrations
- markSegment returns Result.failure, the stored race unchanged, when the
  profile read raises or completes with no emission
- markSegment returns Result.failure, the stored race unchanged, when
  raceId carries no stored race, and when it carries no current segment
- undoLastMark on a raceId a previous repository instance stored reopens
  the closed segment: the stored race then carries that segment's index
  as current, its opening instant restored, and its duration cleared
- undoLastMark returns success carrying the race unchanged, writing
  nothing, when the segment it would reopen is absent from race.segments
- stopRace(raceId, atInstant) returns a race whose stoppedAt is atInstant,
  and the stored row carries atInstant.toEpochMilli()
- stopRace stores completion INCOMPLETE with both current-segment fields
  null, and leaves the segment that was in progress with no duration
- A race completed by marking segment 30 carries stoppedAt null
- markSent(raceId, at) stores at.toEpochMilli(), leaves every other stored
  value unchanged, and returns Result.failure on a raceId nothing is
  stored under
- Each of startClock, markSegment, findInProgress, undoLastMark, stopRace,
  markSent and eraseRecorded returns a failed Result, throwing nothing,
  when the DAO call it makes raises
- findInProgress() returns while a markSegment call is still suspended on
  a profile flow that has not emitted
- A non-suspending function calling any method of the interface but
  observeRecorded does not compile
- observeRecorded emits two races sharing one date with the higher id
  first, and never emits a race carrying a current segment
- A race a previous repository instance started, and this one stops,
  appears in observeRecorded's next emission
- eraseRecorded(raceId) drops the race from observeRecorded's next
  emission and leaves nothing stored under that id; on an id nothing is
  stored under it returns success
- A races table at version 3 migrated by MIGRATION_3_4 accepts a write to
  stoppedAtEpochMs and to sentAtEpochMs
- A row written before MIGRATION_3_4 reads both new columns as NULL
  afterwards and keeps every other column value it carried
- PhoneRaceRecordingRepository, once suspend, returns success carrying
  null from findInProgress(), emits an empty list from observeRecorded(),
  and returns Result.failure from each of its six other methods

## Dependencies

RaceDao — produced by lot-09: findInProgress, findById, findSegments,
  findRetainedFactors, findRejectedCalibrations, upsert, upsertAndFind,
  delete. A Robolectric test reaching it needs `allowMainThreadQueries()`
  and a same-thread query/transaction executor — state document, Traps
RaceEntity, MIGRATION_1_2, MIGRATION_2_3, HyroxDatabase at version 3 —
  produced by lot-08
SegmentEntity, RetainedFactorEntity, RejectedCalibrationEntity —
  pre-existing
buildSegments, cumulativeDurationMs — SegmentBuilder, modified by lot-02
Race, Segment, RaceOrigin, RaceCompletion, RetainedFactor,
  RejectedCalibration — pre-existing
ProfileRepository.observe(): Flow<Profile> — modified by lot-10: a store
  failure is logged and the flow completes emitting nothing, so `.first()`
  on it raises rather than returning a profile
CorrectionFactorCalculator, CorrectionFactorOutcome,
  DisplayFormatter.formatDateTime, SegmentBlueprint — pre-existing
PhoneRaceRecordingRepository — built by lot-30
RaceRepositoryImpl (:core-data) — pre-existing, outside this lot: its own
  private Race-to-RaceEntity mapping leaves both new columns at their
  null default, and stays as it is
kotlinx.coroutines 1.10 — declared dependency: Dispatchers.IO,
  withContext, Mutex
Room 2.7 — declared dependency; the migration test drives MIGRATION_3_4
  through a raw SupportSQLiteOpenHelper, no migration-testing artifact

## Conventions

R4 · `./gradlew check` exits 0 — this lot is the last of the sequence
R8 · no committed migration is modified; a structural change adds a new one
R9 · a lot never writes a file a tool produces — the exported schema JSON
R19 · every public operation that can block is `suspend`
R24 · an operation reaching outside the process says so, and picks its own
  thread inside its implementation
R25 · an argument a signature takes is read; a value that must outlive the
  process is written where it does
R26 · no `!!` on a value coming from outside the function
R30 · no empty and no generic catch
R31 · an error crossing a module boundary is of a type that module declares
R33 · every call leaving the process returns its failure as a value
R34 · a caller that receives a failure acts on it
R37 · a write that must precede a return is synchronous, and a write
  holding an invariant is atomic against a concurrent reader
R42 · cooperative coroutines, no shared mutable state between coroutines
R43 · nothing holds a lock across a wait
R46 · what must be found again after the process dies is written where it
  survives, as it changes, and read back from there
R49 · two clocks and two types — the monotonic instant for timing, the
  wall clock for dates
R55 · one nominal and one failure test per public function
R56 · no test reaches the file system outside a temporary directory
R61 · each write that must precede a return has a test interrupting
  between the write and the return
R62 · the lexicon — Stop, Sync, Race, Segment
R63 · every exported symbol carries one line saying what it guarantees and
  when it fails
R66 · no new dependency inside a lot
R81 · a unit test whose subject reaches an `android.*` method carries
  `@RunWith(RobolectricTestRunner::class)`

## Requests

architecte/detailleur-lot-50.md
