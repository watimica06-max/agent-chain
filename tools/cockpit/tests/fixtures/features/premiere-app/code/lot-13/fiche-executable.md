## Signatures

sealed interface SensorPermissionState {
  object Granted : SensorPermissionState
  object Fallback : SensorPermissionState
}

sealed interface SensorPermissionRequestOutcome {
  data class Resolved(val state: SensorPermissionState) : SensorPermissionRequestOutcome
  object RedirectedToSettings : SensorPermissionRequestOutcome
}

SensorPermissionManager.onLaunch() → SensorPermissionState

SensorPermissionManager.requestAgain() → SensorPermissionRequestOutcome

## Acceptance criteria

- On the first-ever launch, onLaunch() requests sensor access once, showing the explanation, and returns Granted when the user grants it
- On the first-ever launch, onLaunch() returns Fallback when the user refuses
- On every launch after the first, onLaunch() rechecks the current permission state without prompting again
- A permission revoked from system settings since the last launch is reflected as Fallback on the next onLaunch() call
- After a refusal or revocation, onLaunch() never re-prompts automatically on a later launch — it only rechecks
- requestAgain() shows the system permission prompt again when the system still offers it, and returns Resolved with the outcome the user chose
- requestAgain() returns RedirectedToSettings, opening the app's own permissions page, when the system no longer offers the prompt

## Dependencies

None — all types are produced by this lot.
