## Signatures

RaceTicker()

  .ticks: SharedFlow<Unit>
    — one emission per configured interval while started; none before
      `start()` or after `stop()`

  .start(): Unit
    — begins ticking on this instance's own internally-owned coroutine
      scope; a call while already started is a no-op

  .stop(): Unit
    — cancels the ticking coroutine; a call while not started is a
      no-op

## Acceptance criteria

- `start()` then advancing time by the configured interval twice yields exactly two emissions on `ticks`, evenly spaced
- `stop()` called after `start()` — no further emission once the interval elapses again
- `start()` called twice in a row produces one emission per interval, not two overlapping ticking loops

## Dependencies

kotlinx.coroutines — pre-existing

## Conventions

§7 R42 · cooperative async on coroutines, no shared mutable state between coroutines
§7 R48 · a resource one moment opens is released by the module that opened it, tied to its own scope — the ticking job is `stop()`'s to end
§10 R55 · every public function has a nominal and a failure test
§10 R56 · no test reaches the system clock; time is driven by `kotlinx-coroutines-test`'s virtual scheduler

## Requests

architecte/detailleur-lot-47.md
