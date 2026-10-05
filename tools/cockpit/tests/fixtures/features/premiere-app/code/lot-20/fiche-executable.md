## Signatures

enum class SensorDataType { HEART_RATE, DISTANCE, SPEED }

sealed interface ExerciseSessionOpenResult {
  object Opened : ExerciseSessionOpenResult
  object DeviceSlotTaken : ExerciseSessionOpenResult
  object Failed : ExerciseSessionOpenResult
}

ExerciseSessionManager.open() → ExerciseSessionOpenResult

ExerciseSessionManager.close()

ExerciseSessionManager.isDataTypeAvailable(dataType: SensorDataType) → Boolean

ExerciseSessionManager.onInteractivityChanged(interactive: Boolean)

## Acceptance criteria

- Opening a session when no other app holds the device's exercise-session slot returns Opened
- Opening a session when another app already holds the device's exercise-session slot returns DeviceSlotTaken, distinct from any other failure
- Calling open() again while a session is already open for the current race leaves the existing session untouched — the race's 30 markings are never split across separate sessions
- isDataTypeAvailable returns false for a data type unsupported on the device and true for one that is, checked independently per type
- A missing reading from an available data type does not close or fail the open session
- Calling onInteractivityChanged(false) configures sensor data delivery as batched; calling onInteractivityChanged(true) configures it as continuous

## Dependencies

None — all types are produced by this lot.
