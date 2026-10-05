## Signatures

WatchDestination — adds two values:

  SENSOR_PERMISSION
  WAITING_FOR_PHONE

SensorPermissionManager.isGranted(): Boolean
  Side-effect-free read of the current OS grant state. Wraps
  SensorPermissionSystem.isGranted(); never prompts and never consumes
  the first-launch flag `onLaunch()` relies on.

WatchRaceNavigator(
  sensorPermissionGranted: Boolean,
  profileAlreadySynced: Boolean
)
  Sets the initial value of `current` at construction:
  - profileAlreadySynced → WatchDestination.HOME
  - !profileAlreadySynced && !sensorPermissionGranted → WatchDestination.SENSOR_PERMISSION
  - !profileAlreadySynced && sensorPermissionGranted → WatchDestination.WAITING_FOR_PHONE
  All other members of WatchRaceNavigator (toPreparation, swipeForward,
  checkInactivity, etc.) are unchanged.

## Acceptance criteria

- Constructing WatchRaceNavigator with profileAlreadySynced = true starts on HOME, whether or not sensorPermissionGranted is true
- Constructing WatchRaceNavigator with profileAlreadySynced = false and sensorPermissionGranted = false starts on SENSOR_PERMISSION
- Constructing WatchRaceNavigator with profileAlreadySynced = false and sensorPermissionGranted = true starts on WAITING_FOR_PHONE
- SensorPermissionManager.isGranted() returns the OS-reported grant state without invoking the system's permission prompt
- Calling SensorPermissionManager.isGranted() before the first-ever call to onLaunch() does not consume the first-launch flag: onLaunch() still prompts on that first-ever call, exactly as it does when isGranted() was never called

## Dependencies

SensorPermissionSystem — pre-existing
SensorPermissionManager — modified, per the Product Owner's decision recorded in
  docs/features/premiere-app/bugfix/code/lot-06/blocked_detailleur.md (applied and removed):
  adds isGranted()
WatchDestination — modified: adds SENSOR_PERMISSION, WAITING_FOR_PHONE
WatchRaceNavigator — modified: constructor gains sensorPermissionGranted and
  profileAlreadySynced, driving the initial `current`
ProfileRepository — pre-existing (observe(), Profile.lastSyncSuccessAt — non-null once a
  profile has synced from the phone)
SensorPermissionScreen — pre-existing
WaitingForPhoneScreen — pre-existing
