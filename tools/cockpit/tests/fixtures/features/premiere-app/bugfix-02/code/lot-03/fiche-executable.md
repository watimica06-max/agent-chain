## Signatures

    // :app-wear
    class SensorPermissionLaunchStoreImpl(prefs: SharedPreferences) : SensorPermissionLaunchStore {
      override fun isFirstLaunch(): Boolean   // true until recordLaunch() has ever completed, persisted across process death
      override fun recordLaunch()             // persists that a launch has been recorded
    }

    // :app-wear
    class ConnectivityPermissionLaunchStoreImpl(prefs: SharedPreferences) : ConnectivityPermissionLaunchStore {
      override fun isFirstLaunch(): Boolean
      override fun recordLaunch()
    }

## Acceptance criteria

- `SensorPermissionLaunchStoreImpl.isFirstLaunch()` returns true when backed by empty storage, before `recordLaunch()` has ever been called
- `SensorPermissionLaunchStoreImpl.isFirstLaunch()` returns false, from a newly constructed instance backed by the same persisted storage, after `recordLaunch()` has been called
- `ConnectivityPermissionLaunchStoreImpl` (app-wear)'s `isFirstLaunch()` returns true when backed by empty storage, before `recordLaunch()` has ever been called
- `ConnectivityPermissionLaunchStoreImpl` (app-wear)'s `isFirstLaunch()` returns false, from a newly constructed instance backed by the same persisted storage, after `recordLaunch()` has been called

## Dependencies

SensorPermissionLaunchStore — pre-existing, interface unchanged (`:app-wear`)
ConnectivityPermissionLaunchStore — pre-existing, interface unchanged (`:core-domain`)

## Conventions

§3 · anything touching the device's OS — permissions, sensors, preferences — lives in the application module using it
§9 · identifiers and comments in English
