## Signatures

    sealed interface PreparationState {
        data class Resuming(val race: Race) : PreparationState
        data class Ready(val referenceLoaded: Boolean) : PreparationState
        object SensorConflict : PreparationState
        object OpenFailed : PreparationState
    }

    class RaceLaunchController(
        private val recordingRepository: RaceRecordingRepository,
        private val exerciseSessionManager: ExerciseSessionManager
    ) {
        /** Called when the preparation screen (§9.11) opens. */
        suspend fun openPreparation(referenceRace: Race?): PreparationState

        /** Called on "Lancer" while [PreparationState.Ready] is showing. */
        fun launch(startedAt: Instant, startedAtElapsedRealtime: Long): Result<Race>

        /**
         * Called on "Lancer" while [PreparationState.OpenFailed] is
         * showing: retries the session open once, then starts the clock
         * regardless of that retry's outcome.
         */
        suspend fun retryAndLaunch(startedAt: Instant, startedAtElapsedRealtime: Long): Result<Race>

        /** Called on "Continuer" in the sensor-conflict dialog (§9.11). */
        suspend fun confirmConflict(): PreparationState
    }

## Acceptance criteria

- `openPreparation` returns `Resuming(race)` when `RaceRecordingRepository.findInProgress` already holds a race, without calling `ExerciseSessionManager.open`
- `openPreparation` returns `Ready(referenceLoaded = true)` when no race is in progress, the session opens successfully, and a non-null `referenceRace` is supplied
- `openPreparation` returns `Ready(referenceLoaded = false)` when no race is in progress, the session opens successfully, and `referenceRace` is null
- `openPreparation` returns `SensorConflict` when `ExerciseSessionManager.open` reports `DeviceSlotTaken`
- `openPreparation` returns `OpenFailed` when `ExerciseSessionManager.open` reports `Failed`
- `launch` starts the monotonic clock and opens segment 1, returning the created race
- `retryAndLaunch` starts the race after a retried open that succeeds
- `retryAndLaunch` starts the race, without sensor data, after a retried open that fails again — with no further retry
- `confirmConflict` returns `Ready` when the retried session open now succeeds

## Dependencies

RaceRecordingRepository — pre-existing (lot-06)
Race — pre-existing (lot-04)
ExerciseSessionManager — pre-existing (lot-20)
ExerciseSessionOpenResult — pre-existing (lot-20)
PreparationState — produced by lot-14
