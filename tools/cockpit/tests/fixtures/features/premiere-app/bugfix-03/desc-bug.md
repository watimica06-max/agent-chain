## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

### §1.1 Race carries no sent state

Bearer: Race

Race carries no state distinguishing a sent-but-unacknowledged race from
one never sent, so an interruption between `transport.send` succeeding and
`eraseRecorded` running causes the race to be sent again on the next sync.
Race gains a sent state (e.g. `sentAt: Instant?`) that
`RaceRecordingRepository` can set right after `transport.send` succeeds and
before `saveRecordedRace`/`eraseRecorded` run, and `observeRecorded` keeps
returning the race regardless of that state until `eraseRecorded` runs on
the phone's acknowledgement.

## §2 Persistence

## §3 Calculation

## §4 Transition

## §5 External source

## §6 Synchronisation

### §6.1 Nothing receives a recorded race on the phone

Bearer: RecordedRaceListenerService

`WearableRecordedRaceTransport` sends a race payload to the phone's Data
Layer on path `/recorded-race`, and nothing on the phone receives it. A
`WearableListenerService` in `:app-phone` registers on that path, decodes
the payload, and calls `RaceRepository.saveRecordedRace` with the decoded
race. Decoding requires `PayloadCodec` to expose a public decode function
for `RecordedRacePayload`, which does not exist today.

### §6.2 Nothing receives a profile sync on the watch

Bearer: ProfileSyncListenerService

A profile and reference pushed on path `/profile-sync` reach the watch's
Data Layer, and nothing on the watch receives them. A
`WearableListenerService` in `:app-wear` registers on that path, decodes
the payload, and calls `ProfileSyncPushService.applyIncoming` with the
payload, the current `raceInProgress` state, and the current instant.
Decoding requires `PayloadCodec` to expose a public decode function for
`ProfileSyncPayload`, which does not exist today, and to be reachable from
`:app-wear` across the module boundary.

### §6.3 PayloadCodec never decodes

Bearer: PayloadCodec

`PayloadCodec` only encodes a `ProfileSyncPayload` or a `RecordedRacePayload`
into bytes for sending, and has no function to turn received bytes back
into either payload. `PayloadCodec` gains a decode function for each
payload type, reading the bytes with `ObjectInputStream` and mapping the
reconstructed snapshot back to the domain payload, so the phone's and the
watch's listener services can call it.

### §6.4 A race is erased before the phone confirms receipt

Bearer: RecordedRaceSyncService

`RecordedRaceSyncService` erases a recorded race as soon as `transport.send`
returns true, which only means the message left the watch, not that the
phone saved it. `RecordedRaceSyncService` marks the race as sent and keeps
it once `send` succeeds, and erases it only when a `/recorded-race-ack`
message carrying that race's identifier arrives from the phone.
`RecordedRacePayload` gains a race identifier so the phone can echo it
back, the phone gains a `WearableListenerService` decoding `/recorded-race`
and a transport sending `/recorded-race-ack` once
`RaceRepository.saveRecordedRace` succeeds, and
`RaceRepository.saveRecordedRace` gains an identifier-based idempotency
check so an acknowledgement resent for an already-held race does not save
it twice.

## §7 Background work

## §8 Journey

## §9 Screen

## §10 Text

## §11 Access

## §12 Lifecycle

## Gaps set aside
