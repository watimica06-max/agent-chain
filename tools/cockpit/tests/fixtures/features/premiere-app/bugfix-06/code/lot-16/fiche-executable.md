## Signatures

ProfileSyncPushService (:core-domain) — modified

  constructor(
    profileRepository: ProfileRepository,
    raceRepository: RaceRepository,
    watchHistoryStore: WatchHistoryStore,
    transport: ProfileSyncTransport,
    raceRecordingRepository: RaceRecordingRepository,
  )
    — adds raceRecordingRepository; read only by applyIncoming, never by push

  suspend fun push(permissionGranted: Boolean, at: Instant): ProfileSyncPushOutcome
    — same parameters and return type; now returns Failure, instead of
      Success, when profileRepository.markSyncSuccess(at) fails after
      the transport has confirmed delivery

  suspend fun applyIncoming(payload: ProfileSyncPayload, at: Instant): ProfileSyncApplyOutcome
    — drops the raceInProgress parameter; its first action is
      raceRecordingRepository.findInProgress(), read at the moment
      applyIncoming runs rather than supplied by the caller — Refused
      when that call returns a non-null race, whatever payload carries;
      otherwise replaces the reference (raceRepository.replaceReference),
      replaces the watch history (watchHistoryStore.replaceAll), writes
      the incoming profile through one call to
      profileRepository.applyIncomingProfile(payload.profile) — the
      five separate updater calls (updateHrMaxBpm, four x
      updateZoneThreshold, updateExpectedDistanceM, updateLongPressMs,
      updateCorrectionFactor) are removed — then checks
      markSyncSuccess(at)'s Result; Failure on a failure from
      replaceReference, applyIncomingProfile or markSyncSuccess; Applied
      only once all three succeed

ProfileSyncListenerService (:app-wear) — modified

  no longer declares a raceRecordingRepository field; no longer computes
  raceInProgress

  override fun onMessageReceived(event: MessageEvent): Unit
    — for PROFILE_SYNC_PATH, launches into serviceScope; the decode call
      moves inside that launch (today it runs before it, on the calling
      thread); inside the launch, decodes event.data via
      PayloadCodec.decodeProfileSync, and whatever that call raises is
      caught and represented as
      Result.failure(PayloadDecodingFailure(message, cause = <caught>)),
      dropping the payload without calling applyIncoming and without
      letting the exception reach the binder thread; on a successful
      decode, calls
      profileSyncPushService.applyIncoming(payload, clock.now()) — no
      raceInProgress argument

  override fun onDestroy(): Unit
    — cancels serviceScope, then calls super.onDestroy()

SyncModule (:app-wear), object — modified

  fun provideProfileSyncPushService(
    profileRepository: ProfileRepository,
    raceRepository: RaceRepository,
    watchHistoryStore: WatchHistoryStore,
    transport: ProfileSyncTransport,
    raceRecordingRepository: RaceRecordingRepository,
  ): ProfileSyncPushService
    — adds raceRecordingRepository and passes it through; resolved from
      the same binding provideRecordedRaceSyncService already consumes

SyncModule (:app-phone), object — modified

  fun provideProfileSyncPushService(
    profileRepository: ProfileRepository,
    raceRepository: RaceRepository,
    watchHistoryStore: WatchHistoryStore,
    transport: ProfileSyncTransport,
    raceRecordingRepository: RaceRecordingRepository,
  ): ProfileSyncPushService
    — adds raceRecordingRepository and passes it through; resolved from
      RaceRecordingModule (:app-phone)'s PhoneRaceRecordingRepository
      binding (lot-30) — this module never imports
      PhoneRaceRecordingRepository directly, only the
      RaceRecordingRepository interface

FakeSyncModule (:app-wear test), object — modified

  fun provideProfileSyncPushService(
    profileRepository: ProfileRepository,
    raceRepository: RaceRepository,
    watchHistoryStore: WatchHistoryStore,
    transport: ProfileSyncTransport,
    raceRecordingRepository: RaceRecordingRepository,
  ): ProfileSyncPushService
    — same added parameter, resolved from the same
      provideRecordedRaceSyncService binding already exposes

## Acceptance criteria

- applyIncoming returns Refused, performing no write, when its own call to RaceRecordingRepository.findInProgress() returns a race — with no raceInProgress parameter supplied by the caller
- applyIncoming, when findInProgress() returns null, replaces the reference, replaces the watch history, writes the incoming profile through a single call to ProfileRepository.applyIncomingProfile, and returns Applied
- applyIncoming returns Failure without calling markSyncSuccess when replaceReference or applyIncomingProfile fails
- applyIncoming returns Failure, instead of Applied, when every write succeeds but markSyncSuccess fails
- push returns Failure, instead of Success, when the transport delivers successfully but markSyncSuccess fails
- onMessageReceived, given a message whose bytes fail to decode, does not throw, wraps the failure as a PayloadDecodingFailure, and never calls applyIncoming for that message
- onDestroy cancels serviceScope: a coroutine already launched into it before onDestroy is cancelled and does not complete

## Dependencies

ProfileRepository, ProfileRepository.applyIncomingProfile, ProfileRepository.markSyncSuccess — pre-existing
RaceRepository, RaceRepository.replaceReference — pre-existing
WatchHistoryStore — pre-existing
ProfileSyncTransport, ProfileSyncPayload, ProfileSyncPushOutcome, ProfileSyncApplyOutcome — pre-existing
RaceRecordingRepository, RaceRecordingRepository.findInProgress — pre-existing
PhoneRaceRecordingRepository, RaceRecordingModule (:app-phone) — produced by lot-30
PayloadDecodingFailure — produced by lot-52
PayloadCodec.decodeProfileSync — pre-existing, still synchronous at this point in the sequence (turned suspend by lot-11, not yet coded)
Clock — pre-existing

## Conventions

R14 · no module of another nature imports :app-phone or :app-wear — ProfileSyncPushService reaches the phone's recording state only through the :core-domain RaceRecordingRepository interface
R30 · no empty and no generic catch — the decode catch handles and reports, never absorbs
R31 · an error crossing a module boundary is of a type that module declares — the caught decode exception is wrapped as PayloadDecodingFailure
R33 · a call leaving the process returns its failure as a value, never a thrown exception crossing the boundary
R34 · a caller that receives a failure acts on it — markSyncSuccess's Result, and applyIncomingProfile's/replaceReference's, are each checked
R37 · a write holding an invariant is atomic against a concurrent reader — the five profile fields are written through one call
R48 · a resource opened by a scope is released by the module that opened it, tied to that module's own scope — serviceScope cancelled in onDestroy
R53 · no direct write to standard output outside the entry point — go through android.util.Log
R54 · no data attached to a person appears in a log message

## Requests

—
