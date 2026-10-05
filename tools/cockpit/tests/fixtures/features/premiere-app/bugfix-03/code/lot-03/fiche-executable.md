## Signatures

RecordedRaceListenerService (app-phone) — extends `WearableListenerService`, `@AndroidEntryPoint`

    class RecordedRaceListenerService : WearableListenerService() {
      @Inject lateinit var raceRepository: RaceRepository
      @Inject lateinit var ackTransport: RecordedRaceAckTransport
      override fun onMessageReceived(event: MessageEvent)
    }

On a message whose path is `/recorded-race`: decodes `event.data` via
`PayloadCodec.decodeRecordedRace(bytes): RecordedRacePayload`, then calls
`raceRepository.saveRecordedRace(payload.raceId, payload.name, payload.date,
payload.segments, payload.completion)`. Once that call returns a success
`Result`, sends an acknowledgement carrying `payload.raceId` — the same
identifier the payload carried, not the `Race.id` `saveRecordedRace`
returns — through `ackTransport.send(payload.raceId)`. `saveRecordedRace`
is not `suspend`; `ackTransport.send` is, so the send runs on a coroutine
scope the service owns, since `onMessageReceived` itself is not `suspend`.

## Acceptance criteria

- A message on `/recorded-race` decoded into a `RecordedRacePayload` is saved through `RaceRepository.saveRecordedRace` with that payload's `raceId`, `name`, `date`, `segments` and `completion`.
- Once that save succeeds, `RecordedRaceAckTransport.send` is called once, with the same `raceId` the payload carried.
- A save failure calls `RecordedRaceAckTransport.send` zero times.
- The service is declared in `:app-phone`'s manifest, with an intent filter routing messages on path `/recorded-race` to it.

## Dependencies

PayloadCodec.decodeRecordedRace — modified by lot-02 (this cycle)
RaceRepository.saveRecordedRace — modified by lot-04 (this cycle)
RecordedRaceAckTransport — produced by lot-06 (this block)

## Conventions

§3 · anything touching the device's OS lives in the application module using it — a `WearableListenerService` belongs to `:app-phone`
§3 · `:app-phone` and `:app-wear` never import each other
§1 · DI: Hilt
§13 · never swallow an exception silently
§14 · sync code is tested against fakes, never real hardware in CI
