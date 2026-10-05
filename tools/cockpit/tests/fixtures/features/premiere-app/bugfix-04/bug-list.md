- The back gesture is not disabled during a race. `WatchRaceNavigator`
  exposes `backGestureEnabled`, true only on the home and preparation
  screens, and nothing reads it: an accidental gesture on a race page
  leaves the running race. The root composable honours that property —
  the gesture steps back where it is true, and does nothing at all
  where it is false.

- The back gesture does not leave the preparation screen. Only the
  explicit "Quitter" text does. Outside a race the gesture works
  normally, and on preparation it returns to the home screen, the same
  way the tap does.

- Nothing enters or leaves ambient mode on the watch.
  `AlwaysOnDisplayController.enterPowerSave` and `exitPowerSave` exist
  and have no caller anywhere: the screen dims into the system's own
  ambient rendering and the race pages never switch to their power-save
  layout, never refresh on the ten-second beat. Something observes the
  watch going into and out of ambient and calls them — a wrist raise or
  a screen touch brings the normal display back.

- No watch-face complication exists. `WatchComplicationEntry.entryPoint`
  computes which race page a tap should land on and has no caller: no
  complication is published, and nothing routes a tap on one back into
  the app. The watch declares a complication data source that publishes
  during a race, and a tap on it opens the page `entryPoint` names.

- A refused connectivity permission on the watch is final and
  invisible. `HomeViewModel` calls `ConnectivityPermissionManager.onLaunch()`
  and drops its result; `requestAgain()` is never called and
  `HomeUiState` carries no field for it. The home screen shows a
  reminder when connectivity access is not granted, with an action that
  re-requests it — the same way the phone's profile screen already
  does, and the same way the watch's own sensor-permission reminder
  does.
