## Signatures

    data class RecordedRacePayload(
        val name: String,
        val date: Instant,
        val segments: List<Segment>,
        val completion: RaceCompletion
    )

    sealed interface RecordedRaceSyncState {
        object InProgress : RecordedRaceSyncState
        object Failure : RecordedRaceSyncState
        data class Success(val at: Instant) : RecordedRaceSyncState
    }

    interface RecordedRaceTransport {
        /** Sends [payload] to the phone. False on any delivery failure. */
        suspend fun send(payload: RecordedRacePayload): Boolean
    }

    class RecordedRaceSyncService(
        private val raceRecordingRepository: RaceRecordingRepository,
        private val raceRepository: RaceRepository,
        private val transport: RecordedRaceTransport,
    ) {

        /** The current/last sync outcome. Null before any sync() call ever ran. */
        fun observe(): Flow<RecordedRaceSyncState?>

        /**
         * Transfers every race held by RaceRecordingRepository.observeRecorded()
         * to the phone, one at a time: sends it, saves it on the phone via
         * RaceRepository.saveRecordedRace, then erases it from the watch via
         * RaceRecordingRepository.eraseRecorded. Stops at the first race whose
         * send or save fails, leaving it and every race after it un-erased.
         * Does nothing — no send, no save, no erase, observe() unchanged —
         * when [raceInProgress] is true. Sets observe() to InProgress while
         * running, then Success(at) once every race has transferred and
         * erased, or Failure on a stop.
         */
        suspend fun sync(raceInProgress: Boolean, at: Instant)
    }

Modification — `RaceRecordingRepository` (interface in
`core-domain/src/main/kotlin/com/mgilli/core/domain/race/RaceRecordingRepository.kt`),
adds:

    /**
     * The watch's own recorded races not yet erased, most recent first —
     * the descending history (§6.2). Never includes the race currently
     * in progress. Emits again whenever a race completes or is erased.
     */
    fun observeRecorded(): Flow<List<Race>>

    /**
     * Removes [raceId] from the watch's recorded history — called once
     * the phone has confirmed receipt (§6.2). No-op, returning success,
     * when [raceId] is not held.
     */
    fun eraseRecorded(raceId: Long): Result<Unit>

Modification — `RaceRepository` (interface in
`core-domain/src/main/kotlin/com/mgilli/core/domain/race/RaceRepository.kt`),
adds:

    /**
     * Creates a new race recorded by the watch — origin RECORDED,
     * never the reference, with no in-progress state. An INCOMPLETE
     * [completion] keeps only [segments] already closed; a segment
     * never reached is absent from [segments] rather than carrying a
     * zero duration.
     */
    fun saveRecordedRace(
        name: String, date: Instant, segments: List<Segment>, completion: RaceCompletion
    ): Result<Race>

## Acceptance criteria

- `sync()` sends every race returned by `RaceRecordingRepository.observeRecorded()`, each as its own `name`/`date`/`segments`/`completion`, when `raceInProgress` is false
- A race successfully sent and saved on the phone is erased from the watch via `eraseRecorded`
- A race whose send fails is not erased from the watch, and neither it nor any race after it in that `sync()` call is saved or erased
- A race whose phone-side save fails is not erased from the watch, and no race after it in that `sync()` call is saved or erased
- `sync()` performs no send, no save and no erase, and leaves `observe()` unchanged, when `raceInProgress` is true
- `observe()` reports `InProgress` while a `sync()` call runs, then `Success(at)` once every recorded race has transferred and been erased
- `observe()` reports `Failure` after a `sync()` call that stops on a send or save failure
- `saveRecordedRace` stores an INCOMPLETE race with only its closed segments; a segment never reached is absent, not a zero duration
- `saveRecordedRace` never sets the created race as the reference

## Dependencies

Race — pre-existing (lot-04)
Segment — pre-existing (lot-01)
RaceCompletion — pre-existing (lot-04)
RaceRecordingRepository — pre-existing (lot-06), observeRecorded()/eraseRecorded(raceId) added by this lot
RaceRepository — pre-existing (lot-04), observeAll()/findById()/observeReference() added by lot-25, saveRecordedRace(...) added by this lot
RecordedRacePayload — produced by this lot
RecordedRaceSyncState — produced by this lot
RecordedRaceTransport — produced by this lot (interface only, no Data-Layer-backed implementation yet)
