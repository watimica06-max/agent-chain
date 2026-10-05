## Signatures

class WatchRaceComplicationDataSourceService :
  androidx.wear.watchface.complications.datasource.ComplicationDataSourceService()

  @Inject lateinit var raceRecordingRepository: RaceRecordingRepository
  @Inject lateinit var navigator: WatchRaceNavigator

  override fun onComplicationRequest(
    request: ComplicationRequest,
    listener: ComplicationRequestListener
  ): Unit
    — when `raceRecordingRepository.findInProgress().getOrNull()` is a
    non-null `Race`, calls `listener.onComplicationData(data)` where
    `data`'s tap action is a `PendingIntent` targeting `MainActivity`
    carrying `EXTRA_TAPPED_DESTINATION` set to
    `WatchComplicationEntry.entryPoint(navigator.current.value).destination.name`;
    when `findInProgress().getOrNull()` is null (no race in progress,
    including on failure), calls `listener.onComplicationData(null)`.

  override fun getPreviewData(type: ComplicationType): ComplicationData?

  companion object {
    const val EXTRA_TAPPED_DESTINATION: String
  }

## Acceptance criteria

- While a race is in progress (`RaceRecordingRepository.findInProgress()` returns a non-null `Race`), `onComplicationRequest` publishes non-null complication data
- While no race is in progress (`findInProgress()` returns null, success or failure alike), `onComplicationRequest` publishes no data (calls the listener with null)
- When a race is in progress, the published data's tap `PendingIntent` targets `MainActivity` and carries `EXTRA_TAPPED_DESTINATION` set to `WatchComplicationEntry.entryPoint(navigator.current.value).destination`'s name
- `WatchRaceComplicationDataSourceService` is declared as a `<service>` in `app-wear`'s manifest, bound with `android.permission.BIND_COMPLICATION_PROVIDER` and the complication-update-request intent-filter, making it selectable from the watch face's complication picker

## Dependencies

RaceRecordingRepository — pre-existing
RaceRecordingRepository.findInProgress() — pre-existing
WatchComplicationEntry.entryPoint(current) — pre-existing
WatchRaceNavigator.current — pre-existing
WatchDestination — pre-existing
MainActivity — pre-existing, gains `onNewIntent` in lot-03
ComplicationDataSourceService, ComplicationRequest, ComplicationRequestListener, ComplicationType, ComplicationData — framework (androidx.wear.watchface complications-data-source-ktx / complications-data), not yet declared as a Gradle dependency in this project

## Conventions

§3 · anything touching the device's OS — permissions, sensors, preferences, Health Connect — lives in the application module using it: this service lives in `:app-wear`
§9 · files are named for the class they hold: `WatchRaceComplicationDataSourceService.kt`
§10 · no hardcoded user-facing string; any complication text goes through the resource files, French only
§13 · a repository returns a result type, never null on failure — `findInProgress()`'s `Result` is unwrapped through `getOrNull()`, the same idiom `MainActivity` already uses
