## Signatures

MessageChannel.send(path: String, data: ByteArray): Boolean (suspend)
  — unchanged signature; doc updated: false on any delivery failure —
    never throws, except a CancellationException, which is rethrown
    uncaught so the caller's own cancellation completes normally

DataLayerMessageChannel.send(path: String, data: ByteArray): Boolean (suspend)
  — unchanged signature; its catch now catches CancellationException
    first and rethrows it before its existing catch(Exception), which
    also logs what it caught before returning false

WearableProfileSyncTransport.send(payload: ProfileSyncPayload): Boolean (suspend)
  — unchanged signature; PayloadCodec.encode(payload) now runs outside
    the try that guards channel.send, so an exception it raises
    propagates uncaught instead of being reported as a delivery
    failure; the try around channel.send catches CancellationException
    first and rethrows it, then catches Exception, logs what it
    caught, and returns false

WearableRecordedRaceTransport.send(payload: RecordedRacePayload): Boolean (suspend)
  — the identical change, for RecordedRacePayload: PayloadCodec.encode
    moves outside the try; CancellationException caught first and
    rethrown; the remaining catch logs what it caught before returning
    false

WearableRecordedRaceAckTransport.send(raceId: Long): Boolean (suspend)
  — unchanged signature; PayloadCodec is not involved (it encodes
    raceId directly), so only the catch-site fix applies: catches
    CancellationException first and rethrows it, then catches
    Exception, logs what it caught, and returns false

## Acceptance criteria

- DataLayerMessageChannel.send rethrows a CancellationException raised while sending, instead of returning false
- DataLayerMessageChannel.send logs the exception it catches before returning false
- WearableProfileSyncTransport.send rethrows a CancellationException raised while channel.send runs, instead of returning false
- WearableProfileSyncTransport.send logs the exception it catches from channel.send before returning false
- WearableProfileSyncTransport.send lets an exception raised by PayloadCodec.encode propagate uncaught, distinct from a delivery failure
- WearableRecordedRaceTransport.send rethrows a CancellationException raised while channel.send runs, instead of returning false
- WearableRecordedRaceTransport.send logs the exception it catches from channel.send before returning false
- WearableRecordedRaceTransport.send lets an exception raised by PayloadCodec.encode propagate uncaught, distinct from a delivery failure
- WearableRecordedRaceAckTransport.send rethrows a CancellationException raised while sending, instead of returning false
- WearableRecordedRaceAckTransport.send logs the exception it catches before returning false

## Dependencies

MessageChannel, DataLayerMessageChannel, WearableProfileSyncTransport, WearableRecordedRaceTransport, WearableRecordedRaceAckTransport — pre-existing, all modified
PayloadCodec — pre-existing, unmodified, called by two of the four transports
android.util.Log — pre-existing (Android platform)

## Conventions

R30 · no empty and no generic catch — CancellationException no longer folds into the generic catch; the generic catch now logs instead of discarding silently
R53 · go through android.util.Log; ERROR is for what needs a human — pick the level per what's caught
R54 · no data attached to a person appears in a log message — the logged exception carries no race name, heart-rate, pace or similar
R63 · every exported symbol carries one line saying what it guarantees and when it fails — MessageChannel.send's doc line is updated to state the CancellationException exception

## Requests

—
