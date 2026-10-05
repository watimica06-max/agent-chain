## Signatures

class SensorPermissionSystemImpl(
  activity: android.app.Activity,
  launcher: androidx.activity.result.ActivityResultLauncher<String>,
  requestHistory: android.content.SharedPreferences
) : SensorPermissionSystem

- `isGranted(): Boolean` — `ContextCompat.checkSelfPermission(activity, Manifest.permission.BODY_SENSORS) == PackageManager.PERMISSION_GRANTED`.
- `canShowSystemPrompt(): Boolean` — true when `requestHistory` records no prior call to `requestPermission()`, or when `ActivityCompat.shouldShowRequestPermissionRationale(activity, Manifest.permission.BODY_SENSORS)` is true; false once a request has already happened and the rationale check is false (the OS will no longer show its own dialog).
- `suspend fun requestPermission(): Boolean` — records in `requestHistory` that a request has now happened, launches `launcher` (registered on `ActivityResultContracts.RequestPermission()`), suspends until the callback resolves, and returns the granted/denied outcome.
- `openAppSettings()` — opens an `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)` scoped to the app's own package.

`requestHistory` persists the "has this permission ever been requested" bit `ContextCompat`/`ActivityCompat` cannot report on their own — `shouldShowRequestPermissionRationale` alone cannot distinguish "never asked" from "permanently denied", both false. Same SharedPreferences-backed pattern as `SensorPermissionLaunchStoreImpl` in the same package, a distinct key from that store's first-launch flag.

## Acceptance criteria

- `isGranted()` returns true once the OS reports `BODY_SENSORS` granted, false otherwise
- Before `requestPermission()` has ever been called, `canShowSystemPrompt()` returns true
- After a `requestPermission()` call resolves to denied while the OS still offers a rationale, `canShowSystemPrompt()` returns true
- After a `requestPermission()` call resolves to denied and the OS reports no more rationale, `canShowSystemPrompt()` returns false
- `requestPermission()` returns true when the ensuing system dialog is resolved as granted, false when resolved as denied
- `openAppSettings()` opens an intent targeting the app's own permissions page in the system settings

## Dependencies

SensorPermissionSystem — pre-existing (`app-wear/src/main/java/com/mgilli/app_wear/sensor/permission/SensorPermissionSystem.kt`)
Activity, ActivityResultLauncher, ActivityResultContracts.RequestPermission, ContextCompat, ActivityCompat, SharedPreferences — framework (androidx.activity:activity-compose, already a dependency of `:app-wear` since lot-14)

## Conventions

§3 · anything touching the device's OS lives in the application module using it — `SensorPermissionSystemImpl` stays in `:app-wear`
§13 · never swallow an exception silently
§14 · sensor code is tested against fakes/shadows, never real hardware in CI; `androidTest` is never used
