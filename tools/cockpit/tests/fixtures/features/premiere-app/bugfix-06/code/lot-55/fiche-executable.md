## Signatures

class RaceQueryFailure(message: String, cause: Throwable? = null) : Exception(message, cause)
  — declared in :core-domain, beside RaceRepository; the type
    RaceRepository's guarded flows (lot-31) carry in a Result.failure
    when a race query fails while it is collected — a store read raising
    under observeAll() or observeReference(); [message] names the query
    that failed, [cause] is the exception that caused it when one is
    known and null otherwise; read by lot-56's five collectors, which
    act on it instead of letting a failure read as an empty list or an
    absent reference race
  — [message] names a query, never a race name, a race date or any
    other value attached to a person, since a collector logs it

## Acceptance criteria

- Constructing RaceQueryFailure(message, cause) exposes that exact message and that exact cause
- Constructing RaceQueryFailure(message) with no cause exposes a null cause
- RaceQueryFailure is a Throwable, usable as the failure value of a kotlin.Result<T>

## Dependencies

kotlin.Exception — language stdlib, not a project symbol
RaceRepository — pre-existing (:core-domain); lot-31 changes its two
  Flow-returning methods to carry this type

## Conventions

R31 · an error crossing a module boundary is of a type that module declares
R33 · a call leaving the process returns its failure as a value
R54 · no data attached to a person appears in a log message
R55 · one nominal and one failure test, delivered in this lot
R63 · English identifiers; one line saying what the symbol guarantees and when it fails
R75 · a guarded flow emits a failure of its own declared type, never the interface's success shape

## Requests

—
