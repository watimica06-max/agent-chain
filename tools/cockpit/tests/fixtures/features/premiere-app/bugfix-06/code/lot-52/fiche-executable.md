## Signatures

class PayloadDecodingFailure(message: String, cause: Throwable? = null) : Exception(message, cause)
  — declared in :core-sync; the type PayloadCodec (lot-11) wraps in a
    Result.failure when a decode cannot complete — a cast mismatch on
    the deserialised object, a malformed stream; carries a message
    describing what failed to decode and, when known, the exception
    that caused it; read by ProfileSyncListenerService (lot-16) to
    report the failure without letting it escape to the binder thread

## Acceptance criteria

- Constructing PayloadDecodingFailure(message, cause) exposes that exact message and that exact cause
- Constructing PayloadDecodingFailure(message) with no cause exposes a null cause
- PayloadDecodingFailure is a Throwable, usable as the failure value of a kotlin.Result<T>

## Dependencies

kotlin.Exception — language stdlib, not a project symbol

## Conventions

R31 · an error crossing a module boundary is of a type that module declares
R33 · a call leaving the process returns its failure as a value, never a thrown exception crossing the boundary

## Requests

—
