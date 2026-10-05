## Signatures

RecordedRaceSyncState.Failure(raceId: Long) → RecordedRaceSyncState
  — replaces the bare `object Failure`; carries the id of the race
    sync stopped on, whether the stop came from a failed send or a
    failed markSent

RecordedRaceSyncService.sync(raceInProgress: Boolean, at: Instant) → Unit
  — suspend, signature unchanged. For each race from
    raceRecordingRepository.observeRecorded(), builds the
    RecordedRacePayload from that race's own retainedFactors and
    rejectedCalibrations (no longer emptyList()). On transport.send
    returning false, sets observe() to Failure(race.id) and stops. On
    a successful send, calls raceRecordingRepository.markSent(race.id,
    at) and reads its Result: a failure there also sets observe() to
    Failure(race.id) and stops, leaving that race and every race after
    it unmarked, the same as a send failure does today. observe()
    becomes Success(at) only once every race has been sent and marked
    sent without either call failing

## Acceptance criteria

- A race whose payload is built carries that race's own retainedFactors
  and rejectedCalibrations values, not an empty list, when either is
  non-empty
- A race whose send fails sets observe() to Failure carrying that
  race's own id, and every race after it stays unmarked
- A race whose send succeeds but whose markSent call fails sets
  observe() to Failure carrying that race's own id, and every race
  after it stays unmarked
- A sync where every race sends and marks successfully sets observe()
  to Success(at) only after the last one, never to a Failure

## Dependencies

RaceRecordingRepository — pre-existing
RecordedRaceTransport — pre-existing
RecordedRacePayload — carries retainedFactors and rejectedCalibrations, produced by lot-53 (already coded)
Race — pre-existing, carries retainedFactors and rejectedCalibrations
RecordedRaceAckListenerService — produced by lot-32 (this block); not referenced by sync's own signature

## Conventions

R34 · a caller that receives a failure acts on it — markSent's Result is now checked, never dropped
R37 · a write the corpus states must happen before a call returns is synchronous and its failure propagates
R62 · vocabulary: RetainedFactor / RejectedCalibration, no synonym

## Requests

—
