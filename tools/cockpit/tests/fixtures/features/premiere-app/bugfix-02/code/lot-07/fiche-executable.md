## Signatures

    // :app-wear
    class ExerciseSessionSystemImpl(exerciseClient: ExerciseClient) : ExerciseSessionSystem {
      override suspend fun availableDataTypes(): Set<SensorDataType>
      // Built from exerciseClient.getCapabilitiesAsync()'s result: HEART_RATE,
      // DISTANCE, SPEED each included only when that capability is reported
      // supported for this device — never assumed.

      override suspend fun startExerciseSession(): ExerciseSessionStartOutcome
      // Started when exerciseClient's start call succeeds; DeviceSlotTaken
      // specifically when the device-wide exercise slot is already held by
      // another app; Failed on any other error starting the session.

      override fun endExerciseSession()
      // Ends the session this instance started.

      override fun setDataDeliveryMode(mode: DataDeliveryMode)
      // CONTINUOUS configures the running exercise config for unbatched
      // delivery; BATCHED configures it for batched delivery.
    }

## Acceptance criteria

- `availableDataTypes()` includes `HEART_RATE` when the queried capabilities report heart-rate support, and excludes it otherwise
- `availableDataTypes()` includes `DISTANCE` when the queried capabilities report distance support, and excludes it otherwise
- `availableDataTypes()` includes `SPEED` when the queried capabilities report speed support, and excludes it otherwise
- `startExerciseSession()` returns `Started` when starting the underlying exercise session succeeds
- `startExerciseSession()` returns `DeviceSlotTaken` when the device-wide exercise slot is already held by another app
- `startExerciseSession()` returns `Failed` when the underlying start call fails for any other reason
- `endExerciseSession()` ends the session this instance holds
- `setDataDeliveryMode(CONTINUOUS)` configures the running session for continuous (unbatched) delivery
- `setDataDeliveryMode(BATCHED)` configures the running session for batched delivery

## Dependencies

ExerciseSessionSystem, SensorDataType, DataDeliveryMode, ExerciseSessionStartOutcome — pre-existing, interface unchanged (`:app-wear`)
ExerciseClient — framework type, from the Health Services SDK dependency added by this lot
The Health Services SDK (`androidx.health:health-services-client`) — added by this lot to `app-wear/build.gradle.kts` and to `gradle/libs.versions.toml` (no such dependency exists in the project yet)

## Conventions

§1 · Sensors are read only through Health Services; no sensor read outside it
§3 · anything touching the device's OS — sensors included — lives in the application module using it
§6 · call `getCapabilitiesAsync()` before relying on any DataType — availability differs by device
§6 · only one exercise may run device-wide, across all apps
§14 · sensor code is tested against fakes, never against real hardware in CI
