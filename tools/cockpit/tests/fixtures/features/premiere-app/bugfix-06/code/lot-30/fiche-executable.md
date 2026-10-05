## Signatures

PhoneRaceRecordingRepository (:app-phone) : RaceRecordingRepository
  constructor() — no dependencies
  — findInProgress(): Result<Race?> always returns Result.success(null):
    the phone never itself records a race, so none is ever in progress
  — observeRecorded(): Flow<List<Race>> always emits an empty list to
    every collector: consistent with findInProgress(), no race is ever
    recorded on the phone
  — startClock(startedAt, startedAtElapsedRealtime),
    markSegment(raceId, markedAtElapsedRealtime, segmentDistanceM),
    undoLastMark(raceId), stopRace(raceId, atInstant),
    markSent(raceId, at), eraseRecorded(raceId) — unchanged interface
    signatures; each always returns Result.failure: the phone drives
    no recording, so a call reaching one of these is itself the defect
    to surface, never a silent no-op or a fabricated success

RaceRecordingModule (:app-phone), object, @Module @InstallIn(SingletonComponent::class)
  provideRaceRecordingRepository(): RaceRecordingRepository
    — binds PhoneRaceRecordingRepository, the same way :app-wear's
      RepositoryModule.provideRaceRecordingRepository binds
      RaceRecordingRepositoryImpl

## Acceptance criteria

- findInProgress() on PhoneRaceRecordingRepository returns Result.success(null)
- observeRecorded() on PhoneRaceRecordingRepository emits an empty list
- Each of startClock, markSegment, undoLastMark, stopRace, markSent, eraseRecorded on PhoneRaceRecordingRepository returns a Result.failure
- RaceRecordingModule (:app-phone) supplies a RaceRecordingRepository through Hilt's dependency graph

## Dependencies

RaceRecordingRepository, Race — pre-existing (:core-domain)
Hilt (@Module, @InstallIn(SingletonComponent::class), @Provides, @Singleton) — pre-existing dependency, R65

## Conventions

R12 · :app-phone realises whatever this piece needs, phone-only; PhoneRaceRecordingRepository and RaceRecordingModule stay in :app-phone
R14 · no module of another nature imports :app-phone — nothing outside it depends on this class directly, only through the RaceRecordingRepository interface
R25 · what a signature promises, the body delivers — every method here delivers a real Result/Flow value, never an unfulfilled promise
R33 · a call returns its failure as a value, never a thrown exception — the six write methods fail as values, not by throwing
R35 · a transition/call not named as reachable is a declared error, never a silent no-op — matches the six write methods' explicit failure

## Requests

—
