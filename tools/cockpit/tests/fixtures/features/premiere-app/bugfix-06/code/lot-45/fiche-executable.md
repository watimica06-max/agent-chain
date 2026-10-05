## Signatures

ExerciseSessionStartOutcome (Modification)
  Started / DeviceSlotTaken / AlreadyOwned / Failed
  — `AlreadyOwned` is new: returned by `startExerciseSession()` when the
    platform's tracked status names this app itself as the current
    holder of the device-wide slot, checked the same way
    `DeviceSlotTaken`'s own check already is, before any start attempt;
    mutually exclusive with the other three

ExerciseSessionOpenResult (Modification)
  Opened / Adopted / DeviceSlotTaken / Failed
  — `Adopted` is new: returned by `open()` when `startExerciseSession()`
    reports `AlreadyOwned` — this instance's in-memory state did not
    know of the session, but the OS does

ExerciseSessionSystem (Modification)
  suspend fun availableDataTypes(): Set<SensorDataType>            — unchanged
  suspend fun startExerciseSession(): ExerciseSessionStartOutcome   — unchanged signature, new outcome case (above)
  suspend fun endExerciseSession(): Boolean                        — was `fun ...: Unit`; awaits its platform Task, true on success, false on failure
  suspend fun setDataDeliveryMode(mode: DataDeliveryMode): Boolean  — was `fun ...: Unit`; awaits its platform Task, true on success, false on failure

ExerciseSessionManager (Modification)
  constructor(
    system: ExerciseSessionSystem,
    readingsSource: SensorReadingsSource,
    raceTicker: RaceTicker
  )

  suspend fun open(): ExerciseSessionOpenResult
    — `Opened` on a freshly-started session, `Adopted` on an OS-owned
      session this instance did not itself start; both register
      `readingsSource` for every type `availableDataTypes()` reports and
      call `raceTicker.start()`; `DeviceSlotTaken`/`Failed` touch
      neither; a call while this instance already holds a session
      (from either path) is a no-op returning `Opened`

  suspend fun close(): Boolean
    — was `fun close(): Unit`; stops `raceTicker`, unregisters
      `readingsSource`, then ends the session; true on success, false
      when the underlying end call fails; a call while this instance
      holds no session is a no-op returning true

  suspend fun isDataTypeAvailable(dataType: SensorDataType): Boolean  — unchanged

  suspend fun onInteractivityChanged(interactive: Boolean): Boolean
    — was `fun ...: Unit`; forwards `setDataDeliveryMode`'s outcome

SensorModule (Modification)
  — adds a `@Provides @Singleton` for `SensorReadingsSource`, built from
    `HealthServices.getClient(context).measureClient`
  — adds a `@Provides @Singleton` for `RaceTicker`, built with no
    platform input
  — `provideExerciseSessionManager` takes both as added parameters

## Acceptance criteria

- `open()` on a free device-wide slot returns `Opened`, and afterward `readingsSource.register` is called with exactly `availableDataTypes()`'s set, and `raceTicker.start()` is called
- `open()` when the platform reports this app already owns the session (this instance holding no in-memory record) returns `Adopted`, and also registers `readingsSource` and starts `raceTicker`
- `open()` when another app holds the device-wide slot returns `DeviceSlotTaken`, and neither `readingsSource` nor `raceTicker` is touched
- `open()` when the start attempt fails for any other reason returns `Failed`, and neither `readingsSource` nor `raceTicker` is touched
- `open()` called a second time while a session is already held (`Opened` or `Adopted`) is a no-op returning `Opened`, without a second registration or a second `start()`
- `close()` after a session was opened or adopted stops `raceTicker` and unregisters `readingsSource` before ending the session
- `close()` returns false when the underlying platform end call fails, true when it succeeds
- `close()` called while no session is held is a no-op returning true
- `onInteractivityChanged(true)`/`onInteractivityChanged(false)` forward `CONTINUOUS`/`BATCHED` to `setDataDeliveryMode` and return its outcome

## Dependencies

SensorReadingsSource — produced by lot-46
RaceTicker — produced by lot-47
Health Services Client (ExerciseClient, MeasureClient) — pre-existing framework dependency

## Conventions

§5 R19 · a public operation that can block is suspend — `endExerciseSession`/`setDataDeliveryMode`/`close`/`onInteractivityChanged`
§6 R33 · a call leaving the process returns its failure as a value, never a thrown exception crossing the boundary
§7 R48 · what one moment opens (the sensor registration, the ticker), another must end — `open()`/`close()` are the matching pair
§7 R42 · cooperative async on coroutines, one execution model
§10 R55 · every public function has a nominal and a failure test
§10 R56 · no test reaches real Health Services; `ExerciseClient`/`MeasureClient`/`RaceTicker` are faked

## Requests

—
