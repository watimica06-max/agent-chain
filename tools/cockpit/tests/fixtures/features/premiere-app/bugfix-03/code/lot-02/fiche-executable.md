## Signatures

    PayloadCodec.decodeProfileSync(bytes: ByteArray) → ProfileSyncPayload

    PayloadCodec.decodeRecordedRace(bytes: ByteArray) → RecordedRacePayload

Both read `bytes` with `ObjectInputStream`, reconstruct the local
snapshot `encode` wrote, and map it back to the domain payload.
`PayloadCodec` itself loses its `internal` modifier — a public `object` —
so `:app-phone` and `:app-wear` can call `encode` and these two decode
functions across the module boundary.

## Acceptance criteria

- `decodeProfileSync` applied to the bytes `encode` produced from a `ProfileSyncPayload` returns a payload equal to the original, including when its `reference` is null
- `decodeRecordedRace` applied to the bytes `encode` produced from a `RecordedRacePayload` returns a payload equal to the original, including its `raceId`
- Code in `:app-phone` and code in `:app-wear` each compile a direct call to `PayloadCodec.decodeProfileSync` and to `PayloadCodec.decodeRecordedRace`

## Dependencies

ProfileSyncPayload — pre-existing
RecordedRacePayload — carries `raceId` (lot-05)
PayloadCodec — pre-existing object, gains the two decode functions and public visibility

## Conventions

§3 · anything `:app-phone` and `:app-wear` share lives in a `:core-*` module — `PayloadCodec` stays the single shared codec, in `:core-sync`
§3 · a platform adapter lives in the module carrying its technology — the Data Layer codec stays in `:core-sync`
§13 · never swallow an exception silently — a decode failure propagates rather than being caught and hidden
