## Signatures

RecordedRaceAckTransport (core-domain, `com.mgilli.core.domain.sync`) — interface

    suspend fun send(raceId: Long): Boolean

Sends `raceId` to the watch on path `/recorded-race-ack`. Returns false
on any delivery failure — never throws.

WearableRecordedRaceAckTransport (core-sync, `com.mgilli.core.sync.transport`) — implements RecordedRaceAckTransport

    class WearableRecordedRaceAckTransport internal constructor(
      private val channel: MessageChannel,
    ) : RecordedRaceAckTransport {
      constructor(context: Context) : this(DataLayerMessageChannel(context))
      override suspend fun send(raceId: Long): Boolean
    }

Same shape as `WearableRecordedRaceTransport`/`WearableProfileSyncTransport`:
a public `Context` constructor for production, an `internal` `MessageChannel`
seam for tests. Encodes `raceId` as its 8-byte big-endian representation
(`ByteBuffer.allocate(Long.SIZE_BYTES).putLong(raceId).array()`) and calls
`channel.send("/recorded-race-ack", <those bytes>)`. `PayloadCodec` is not
involved — this payload is a raw identifier, not a `ProfileSyncPayload`/
`RecordedRacePayload` snapshot.

## Acceptance criteria

- `send(raceId)` calls `MessageChannel.send` with path `/recorded-race-ack` and data equal to `raceId`'s 8-byte big-endian encoding.
- `send(raceId)` returns true when `MessageChannel.send` returns true.
- `send(raceId)` returns false, without throwing, when `MessageChannel.send` returns false or throws.

## Dependencies

MessageChannel / DataLayerMessageChannel — pre-existing (core-sync)
RecordedRaceAckTransport — produced by this lot

## Conventions

§3 · a platform adapter lives in the module carrying its technology (Data Layer → `:core-sync`)
§1 · watch ↔ phone communication goes through the Wearable Data Layer only
§13 · never swallow an exception silently — a delivery failure returns false explicitly, not a silent catch
§14 · sync code is tested against fakes, never real hardware in CI
