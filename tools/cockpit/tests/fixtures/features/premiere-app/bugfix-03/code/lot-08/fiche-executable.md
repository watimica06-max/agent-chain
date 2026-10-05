## Signatures

ProfileSyncListenerService (app-wear) — extends `WearableListenerService`, `@AndroidEntryPoint`

    class ProfileSyncListenerService : WearableListenerService() {
      @Inject lateinit var profileSyncPushService: ProfileSyncPushService
      @Inject lateinit var raceRecordingRepository: RaceRecordingRepository
      @Inject lateinit var clock: Clock
      override fun onMessageReceived(event: MessageEvent)
    }

On a message whose path is `/profile-sync`: decodes `event.data` via
`PayloadCodec.decodeProfileSync(bytes): ProfileSyncPayload`. Reads
`raceInProgress` as `raceRecordingRepository.findInProgress().getOrNull()
!= null` — true only when that call succeeds with a non-null race; a null
race or a failed `Result` both read as false. Calls
`profileSyncPushService.applyIncoming(payload, raceInProgress,
clock.now())`. `applyIncoming` is `suspend`; `onMessageReceived` is not, so
the call runs on a coroutine scope the service owns.

## Acceptance criteria

- A message on `/profile-sync` decoded into a `ProfileSyncPayload` is applied through `ProfileSyncPushService.applyIncoming` with that same payload.
- `applyIncoming` is called with `raceInProgress = true` when `RaceRecordingRepository.findInProgress()` returns a race.
- `applyIncoming` is called with `raceInProgress = false` when `findInProgress()` returns null, and when it fails.
- `applyIncoming` is called with the instant `Clock.now()` returns at the time the message is processed.
- The service is declared in `:app-wear`'s manifest, with an intent filter routing messages on path `/profile-sync` to it.

## Dependencies

PayloadCodec.decodeProfileSync — modified by lot-02 (this cycle)
ProfileSyncPushService.applyIncoming — pre-existing
RaceRecordingRepository.findInProgress — pre-existing
Clock — pre-existing

## Conventions

§3 · anything touching the device's OS lives in the application module using it — a `WearableListenerService` belongs to `:app-wear`
§3 · `:core-domain` never imports anything from Android — `ProfileSyncPushService`/`Clock` stay untouched, only the listener service is Android-facing
§3 · `:app-phone` and `:app-wear` never import each other
§1 · DI: Hilt
§5 · the downward payload replaces the watch state wholesale — enforced by `applyIncoming` already, nothing added here
§14 · sync code is tested against fakes, never real hardware in CI
