## Signatures

RecordedRaceAckListenerService (app-wear) — extends `WearableListenerService`, `@AndroidEntryPoint`

    class RecordedRaceAckListenerService : WearableListenerService() {
      @Inject lateinit var recordedRaceSyncService: RecordedRaceSyncService
      override fun onMessageReceived(event: MessageEvent)
    }

On a message whose path is `/recorded-race-ack`: decodes `event.data` as
its 8-byte big-endian representation (`ByteBuffer.wrap(event.data).long`,
the mirror of `WearableRecordedRaceAckTransport`'s encoding, lot-06) into a
`raceId: Long`, then calls `recordedRaceSyncService.acknowledge(raceId)`.

## Acceptance criteria

- A message on `/recorded-race-ack` whose data decodes to `raceId` calls `RecordedRaceSyncService.acknowledge` once, with that same `raceId`.
- The service is declared in `:app-wear`'s manifest, with an intent filter routing messages on path `/recorded-race-ack` to it.

## Dependencies

RecordedRaceSyncService.acknowledge — produced by lot-05 (this cycle)
The 8-byte big-endian raceId encoding — set by lot-06 (this block), on RecordedRaceAckTransport's real implementation

## Conventions

§3 · anything touching the device's OS lives in the application module using it — a `WearableListenerService` belongs to `:app-wear`
§3 · `:app-phone` and `:app-wear` never import each other
§1 · DI: Hilt
§5 · the watch never deletes a race it has not pushed — `acknowledge` is the only path that erases a recorded race, and only once this service calls it
§14 · sync code is tested against fakes, never real hardware in CI
