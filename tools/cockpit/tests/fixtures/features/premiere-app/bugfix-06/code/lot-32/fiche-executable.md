## Signatures

RecordedRaceAckListenerService.serviceScope: CoroutineScope
  — CoroutineScope(SupervisorJob() + Dispatchers.IO), built the same way
    RecordedRaceListenerService's own serviceScope already is; every
    dispatch this service makes goes through it

RecordedRaceAckListenerService.onMessageReceived(event: MessageEvent) → Unit
  — override signature unchanged; the RECORDED_RACE_ACK_PATH guard still
    runs on the calling (binder) thread, but the ByteBuffer read of
    event.data and the recordedRaceSyncService.acknowledge(raceId) call
    it feeds move inside serviceScope.launch; a failure raised reading
    event.data is caught there, reported through android.util.Log, and
    drops the message — acknowledge is never called and nothing escapes
    to the binder thread

## Acceptance criteria

- A message on RECORDED_RACE_ACK_PATH carrying a well-formed 8-byte
  payload calls RecordedRaceSyncService.acknowledge exactly once with
  the decoded raceId, observable once the dispatched work completes
- onMessageReceived returns to its caller before that dispatched read
  and acknowledge call complete, when the underlying call is held open
- A message on RECORDED_RACE_ACK_PATH whose payload is fewer than 8
  bytes does not throw out of onMessageReceived, and
  RecordedRaceSyncService.acknowledge is never called

## Dependencies

RecordedRaceSyncService — pre-existing, unmodified by this lot
MessageEvent — pre-existing (Play Services Wearable)
CoroutineScope, SupervisorJob, Dispatchers, launch — pre-existing (kotlinx.coroutines)
android.util.Log — pre-existing

## Conventions

R30 · no empty and no generic catch — the read's failure is caught by its own type, handled in context
R42 · presumed execution model: cooperative coroutines, no shared mutable state between them
R53 · diagnostics go through android.util.Log; ERROR is for what needs a human
R54 · no data attached to a person in a log message

## Requests

—
