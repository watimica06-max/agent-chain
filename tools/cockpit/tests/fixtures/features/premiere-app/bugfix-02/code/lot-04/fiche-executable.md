## Signatures

    // :app-phone
    class ConnectivityPermissionLaunchStoreImpl(prefs: SharedPreferences) : ConnectivityPermissionLaunchStore {
      override fun isFirstLaunch(): Boolean   // true until recordLaunch() has ever completed, persisted across process death
      override fun recordLaunch()             // persists that a launch has been recorded
    }

## Acceptance criteria

- `ConnectivityPermissionLaunchStoreImpl` (app-phone)'s `isFirstLaunch()` returns true when backed by empty storage, before `recordLaunch()` has ever been called
- `ConnectivityPermissionLaunchStoreImpl` (app-phone)'s `isFirstLaunch()` returns false, from a newly constructed instance backed by the same persisted storage, after `recordLaunch()` has been called

## Dependencies

ConnectivityPermissionLaunchStore — pre-existing, interface unchanged (`:core-domain`)

## Conventions

§3 · anything touching the device's OS — permissions, sensors, preferences — lives in the application module using it
§9 · identifiers and comments in English
