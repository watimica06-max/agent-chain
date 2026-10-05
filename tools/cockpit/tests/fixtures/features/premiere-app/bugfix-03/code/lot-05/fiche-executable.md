## Signatures

    RecordedRacePayload(
      raceId: Long, name: String, date: Instant, segments: List<Segment>, completion: RaceCompletion
    )

    RecordedRaceSyncService(
      raceRecordingRepository: RaceRecordingRepository, transport: RecordedRaceTransport
    )

    RecordedRaceSyncService.sync(raceInProgress: Boolean, at: Instant)   // suspend, parameters unchanged

    RecordedRaceSyncService.acknowledge(raceId: Long) → Result<Unit>

`sync` no longer takes a `RaceRepository`, and no longer calls
`saveRecordedRace`. For each race `observeRecorded()` holds, in order, it
sends a payload whose `raceId` is that race's own id; on a successful
send it calls `raceRecordingRepository.markSent(race.id, at)` instead of
saving or erasing; on a failed send it stops the loop, leaving that race
and every race after it un-marked. `acknowledge(raceId)` erases the
matching race from `raceRecordingRepository` — called by
`RecordedRaceAckListenerService` (lot-07) once a `/recorded-race-ack`
carrying that identifier arrives.

## Acceptance criteria

- For each recorded race whose send succeeds, `sync` sends a payload whose `raceId` equals that race's own id
- For each recorded race whose send succeeds, `sync` marks it sent through `RaceRecordingRepository`, at the instant passed to `sync`, instead of saving or erasing it
- A race marked sent by `sync` is still returned by `RaceRecordingRepository.observeRecorded()` afterwards
- The first race whose send fails stops `sync`: that race and every race after it in the order stay unmarked (`sentAt` still null), and `observe()` reports `Failure`
- Once every race sent is marked successfully, `observe()` reports `Success(at)`
- `acknowledge(raceId)` for a race the repository holds erases it, so it no longer appears in `observeRecorded()`
- `acknowledge(raceId)` for an id the repository does not hold returns success and changes nothing

## Dependencies

RaceRecordingRepository — pre-existing interface, gains `markSent` (lot-01)
RecordedRaceTransport — pre-existing
RecordedRacePayload — this lot, gains `raceId`

## Conventions

§5 · the watch never deletes a race it has not pushed — a race survives on the watch until the phone acknowledges it in full
§13 · a sync failure is never fatal; it retries, and the data stays where it is
§3 · `:core-domain` never imports Android — `RecordedRaceSyncService`/`RecordedRacePayload` stay JVM-pure
