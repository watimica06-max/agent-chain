## Signatures

    class StopRaceController(
        private val recordingRepository: RaceRecordingRepository,
        private val exerciseSessionManager: ExerciseSessionManager
    ) {
        /** Called on confirming §9.14's stop dialog. */
        fun stop(raceId: Long, atInstant: Instant): Result<Race>
    }

## Acceptance criteria

- Confirming stop calls `RaceRecordingRepository.stopRace(raceId, atInstant)`, saving the race as `INCOMPLETE`
- Confirming stop calls `ExerciseSessionManager.close()`, ending the running exercise session
- `stop` returns the race produced by `stopRace`
- A failure from `RaceRecordingRepository.stopRace` is returned as `stop`'s own failure

## Dependencies

Race — pre-existing (lot-04)
RaceRecordingRepository — pre-existing (lot-06), `stopRace` produced by lot-16
ExerciseSessionManager — pre-existing (lot-20)
