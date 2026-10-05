## Symbols

ExerciseSessionSystemImpl — created
ExerciseSessionSystemImpl.startExerciseSession — created, checks the device-wide exercise slot via ExerciseClient.getCurrentExerciseInfoAsync() before starting

## Build

analyze: clean (lint required @Suppress("RestrictedApi") on startExerciseSession — see Convention)
test: 9 passed (ExerciseSessionSystemImplTest), 22 passed (RaceRecordingRepositoryImplTest, adapted per Decision), full :app-wear:check suite green

## State

Added: ExerciseSessionSystemImpl
Removed: ExerciseSessionManager's "unwired" trap (ExerciseSessionSystem now has a real implementation)

## Convention

health-services-client 1.0.0 marks `ExerciseTrackedStatus`'s constants
`@RestrictTo(LIBRARY)`, though `ExerciseInfo.exerciseTrackedStatus` (the
value they classify) is ordinary public API and the sheet's §6 device-wide
check has no other entry point in this SDK version. `startExerciseSession()`
carries `@Suppress("RestrictedApi")` to reference `OTHER_APP_IN_PROGRESS`,
or lint's `RestrictedApi` check fails `:app-wear:check`. Documented as a
trap in `CURRENT_TECHNICAL_STATE.md`.

Per the applied blocking-file Decision, `RaceRecordingRepositoryImplTest.kt`'s
assertion on the removed `Segment.cumulativeMs` (lot-05) is replaced with an
equivalent assertion on `cumulativeDurationMs(undone.segments, 1)` — the
computed-on-read function that replaced the stored field.
