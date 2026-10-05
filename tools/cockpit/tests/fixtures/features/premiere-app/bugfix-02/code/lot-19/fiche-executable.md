## Signatures

class ConnectivityPermissionSystemImpl(
  activity: android.app.Activity,
  launcher: androidx.activity.result.ActivityResultLauncher<String>,
  requestHistory: android.content.SharedPreferences
) : ConnectivityPermissionSystem

- `isGranted(): Boolean` — `ContextCompat.checkSelfPermission(activity, <the chosen OS permission>) == PackageManager.PERMISSION_GRANTED`. Which permission stands for "reaching the paired device" is chosen while coding this lot — the entry (§11.2) leaves it open and the choice does not change this signature or the criteria below, since every one of them is phrased against "the chosen permission", not a name.
- `canShowSystemPrompt(): Boolean` — true when `requestHistory` records no prior call to `requestPermission()`, or when `ActivityCompat.shouldShowRequestPermissionRationale(activity, <the chosen permission>)` is true; false once a request has already happened and the rationale check is false.
- `suspend fun requestPermission(): Boolean` — records in `requestHistory` that a request has now happened, launches `launcher` (registered on `ActivityResultContracts.RequestPermission()`), suspends until the callback resolves, and returns the granted/denied outcome.
- `openAppSettings()` — opens an `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)` scoped to the app's own package.

`requestHistory` persists the "has this permission ever been requested" bit, the same way as `SensorPermissionSystemImpl` (§11.1, lot-18) — `shouldShowRequestPermissionRationale` alone cannot distinguish "never asked" from "permanently denied".

This is the `:app-phone` implementation only, per the lot's declaration; `ConnectivityPermissionSystemImpl (:app-wear)` is lot-20's, built the same way against its own Activity.

## Acceptance criteria

- `isGranted()` returns true once the OS reports the chosen permission granted, false otherwise
- Before `requestPermission()` has ever been called, `canShowSystemPrompt()` returns true
- After a `requestPermission()` call resolves to denied while the OS still offers a rationale, `canShowSystemPrompt()` returns true
- After a `requestPermission()` call resolves to denied and the OS reports no more rationale, `canShowSystemPrompt()` returns false
- `requestPermission()` returns true when the ensuing system dialog is resolved as granted, false when resolved as denied
- `openAppSettings()` opens an intent targeting the app's own permissions page in the system settings

## Dependencies

ConnectivityPermissionSystem — pre-existing (`core-domain/src/main/kotlin/com/mgilli/core/domain/connectivity/ConnectivityPermissionSystem.kt`)
Activity, ActivityResultLauncher, ActivityResultContracts.RequestPermission, ContextCompat, ActivityCompat, SharedPreferences — framework (androidx.activity:activity-compose, already a dependency of `:app-phone`)

## Conventions

§3 · anything touching the device's OS lives in the application module using it — `ConnectivityPermissionSystemImpl` (app-phone) stays in `:app-phone`, distinct from `:app-wear`'s own copy (lot-20)
§13 · never swallow an exception silently
§14 · sensor/sync-adjacent code is tested against fakes/shadows, never real hardware in CI; `androidTest` is never used
