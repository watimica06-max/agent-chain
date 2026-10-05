## Signatures

    data class RaceHistoryEntry(
        val name: String,
        val date: Instant,
        val totalTimeMs: Long
    )

    data class ProfileSyncPayload(
        val profile: Profile,
        val reference: Race?,
        val history: List<RaceHistoryEntry>
    )

    sealed interface ProfileSyncPushOutcome {
        object Success : ProfileSyncPushOutcome
        object Failure : ProfileSyncPushOutcome
    }

    sealed interface ProfileSyncApplyOutcome {
        object Applied : ProfileSyncApplyOutcome
        object Refused : ProfileSyncApplyOutcome
        object Failure : ProfileSyncApplyOutcome
    }

    interface ProfileSyncTransport {
        /** Sends [payload] to the paired device. False on any delivery failure. */
        suspend fun send(payload: ProfileSyncPayload): Boolean
    }

    interface WatchHistoryStore {

        /** Replaces the stored history as a whole block with [entries]. */
        fun replaceAll(entries: List<RaceHistoryEntry>)

        /** The stored history, re-emitted on every replaceAll() call. */
        fun observe(): Flow<List<RaceHistoryEntry>>
    }

    class ProfileSyncPushService(
        private val profileRepository: ProfileRepository,
        private val raceRepository: RaceRepository,
        private val watchHistoryStore: WatchHistoryStore,
        private val transport: ProfileSyncTransport,
    ) {

        /**
         * Sends the current profile, the current reference race in full, and
         * the 20 most recent races (by RaceRepository.observeAll()'s own
         * order) summarized as [RaceHistoryEntry]. Does not call [transport]
         * when [permissionGranted] is false. Records [at] via
         * ProfileRepository.markSyncSuccess on a confirmed delivery.
         */
        suspend fun push(permissionGranted: Boolean, at: Instant): ProfileSyncPushOutcome

        /**
         * Applies an incoming [payload] on the watch side: replaces the
         * reference race (RaceRepository.replaceReference), replaces the
         * watch history as a whole block (WatchHistoryStore.replaceAll),
         * and writes the profile's five settable fields one by one through
         * ProfileRepository's existing updaters. Returns Refused, applying
         * nothing, when [raceInProgress] is true — whatever [payload]
         * carries. Records [at] via ProfileRepository.markSyncSuccess only
         * when every write above succeeds.
         */
        suspend fun applyIncoming(
            payload: ProfileSyncPayload, raceInProgress: Boolean, at: Instant
        ): ProfileSyncApplyOutcome
    }

Modification — `ProfileRepository` (interface in
`core-domain/src/main/kotlin/com/mgilli/core/domain/profile/ProfileRepository.kt`),
adds:

    /** Sets lastSyncSuccessAt to [at]. Always succeeds. */
    fun markSyncSuccess(at: Instant): Result<Unit>

Modification — `RaceRepository` (interface in
`core-domain/src/main/kotlin/com/mgilli/core/domain/race/RaceRepository.kt`),
adds:

    /**
     * Replaces the sole reference race with [race], or clears the
     * reference when [race] is null — used when applying an incoming
     * push (§6.1) on the watch side. No merge with whichever race held
     * the reference before.
     */
    fun replaceReference(race: Race?): Result<Unit>

## Acceptance criteria

- `push()` sends a payload carrying the current profile, the current reference race in full, and the 20 most recent races summarized as `{name, date, totalTimeMs}`
- `push()` includes the reference race in full even when it is not among the 20 most recent races
- `push()` sends a null reference when no race is currently flagged as reference, and still sends the summarized history
- A race no longer present in `RaceRepository` at push time is absent from the sent history, even if a previous push once included it
- `push()` returns `Success` and calls `ProfileRepository.markSyncSuccess(at)` when the transport confirms delivery
- `push()` returns `Failure`, without calling `markSyncSuccess`, when the transport reports a failed delivery
- `push()` returns `Failure` without calling the transport at all, when `permissionGranted` is false
- `applyIncoming()` returns `Refused` and performs no write — to `ProfileRepository`, `RaceRepository` or `WatchHistoryStore` — when `raceInProgress` is true, whatever the payload carries
- `applyIncoming()` returns `Applied`, replaces the reference race, replaces the whole watch history, writes the profile's five settable fields from the payload, and calls `markSyncSuccess(at)`, when `raceInProgress` is false and every write succeeds
- `applyIncoming()` returns `Failure`, without calling `markSyncSuccess`, when `raceInProgress` is false but one of its writes fails

## Dependencies

Profile — pre-existing (lot-05)
ProfileRepository — pre-existing (lot-05), observe() added by lot-36, markSyncSuccess(at) added by this lot
Race — pre-existing (lot-04)
RaceRepository — pre-existing (lot-04), observeAll()/findById()/observeReference() added by lot-25, replaceReference(race) added by this lot
RaceHistoryEntry — produced by this lot
ProfileSyncPayload — produced by this lot
ProfileSyncPushOutcome — produced by this lot
ProfileSyncApplyOutcome — produced by this lot
ProfileSyncTransport — produced by this lot (interface only, no Data-Layer-backed implementation yet)
WatchHistoryStore — produced by this lot
