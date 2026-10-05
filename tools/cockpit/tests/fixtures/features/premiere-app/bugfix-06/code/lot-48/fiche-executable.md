## Signatures

WatchRaceComplicationDataSourceService.scope: CoroutineScope
  — CoroutineScope(SupervisorJob() + Dispatchers.IO), the same
    construction the sync listener services already use; owned by this
    service, not shared with anything else

WatchRaceComplicationDataSourceService.onComplicationRequest(
  request: ComplicationRequest, listener: ComplicationRequestListener
) → Unit
  — override signature unchanged (the platform interface it implements
    is not suspend). The raceRecordingRepository.findInProgress() read
    and everything that follows from it — building the
    WatchComplicationEntry-derived destination, the tap PendingIntent,
    and the ShortTextComplicationData — move inside a coroutine
    launched on scope; onComplicationRequest itself returns to its
    caller without waiting on that work, and listener.onComplicationData
    is called once from inside the launched coroutine, with the same
    non-null/null outcome the current synchronous logic produces

## Acceptance criteria

- onComplicationRequest returns to its caller before
  raceRecordingRepository.findInProgress()'s result is available, when
  that call is held open
- Once findInProgress() resolves to a race in progress,
  listener.onComplicationData is called exactly once with a
  ShortTextComplicationData carrying a tap action targeting
  MainActivity with EXTRA_TAPPED_DESTINATION set to the navigator's
  current destination — the same outcome today's synchronous call
  produces, just observed after that resolution
- Once findInProgress() resolves to no race in progress, or fails,
  listener.onComplicationData(null) is called exactly once

## Dependencies

RaceRecordingRepository — pre-existing, findInProgress() unchanged by this lot (still non-suspend, still Result<Race?>)
WatchComplicationEntry — pre-existing, called unchanged from inside the launched coroutine
MainActivity, WatchDestination, WatchRaceNavigator — pre-existing
ComplicationRequest, ComplicationRequestListener, ComplicationData, ShortTextComplicationData, PendingIntent, Intent — pre-existing (platform)
CoroutineScope, SupervisorJob, Dispatchers, launch — pre-existing (kotlinx.coroutines)

## Conventions

R42 · presumed execution model: cooperative coroutines, no shared mutable state between them
R48 · anything one moment opens and another must end is released by the module that opened it

## Requests

—
