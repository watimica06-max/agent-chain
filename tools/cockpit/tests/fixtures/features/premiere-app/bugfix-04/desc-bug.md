## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

## §2 Persistence

## §3 Calculation

## §4 Transition

### §4.1 Back gesture not disabled during a race

Bearer: WatchApp

WatchApp renders every race destination without a `BackHandler` at
its root, so the system back gesture keeps its default effect on
MAIN, PROJECTION, CONTROL and END and can leave a running race by
accident. WatchApp installs a `BackHandler` that reads
`WatchRaceNavigator.backGestureEnabled` for every destination, letting
the gesture step back where it is true (HOME, PREPARATION) and
consuming it without effect where it is false (MAIN, PROJECTION,
CONTROL, END).

### §4.2 Back gesture does not leave the preparation screen

Bearer: WatchApp

The PREPARATION branch of WatchApp renders `PreparationScreen` with no
`BackHandler`, so only the "Quitter" tap reaches
`WatchRaceNavigator.quitPreparation()`. The PREPARATION branch wraps
`PreparationScreen` in a `BackHandler` that calls
`navigator.quitPreparation()`, returning to the home screen the same
way the tap already does.

## §5 External source

## §6 Synchronisation

## §7 Background work

### §7.1 No watch-face complication is published

Bearer: WatchRaceComplicationDataSourceService

No `ComplicationDataSourceService` is declared in `app-wear` and
`WatchComplicationEntry.entryPoint` has no caller, so no complication
is ever published and a tap on one cannot reach the app.
`WatchRaceComplicationDataSourceService` publishes a complication
while a race is in progress, is registered in the manifest, and opens
the app on the page `entryPoint` names when its complication is
tapped. This requires `WatchRaceNavigator` to gain a method that sets
`current` directly to an external target, since every existing
transition only advances one fixed step in the swipe/mark sequence,
and `MainActivity` to handle `onNewIntent`, reading the tapped
destination from the `PendingIntent` extra and passing it to that new
method.

## §8 Journey

## §9 Screen

### §9.1 A refused connectivity permission is never surfaced

Bearer: HomeViewModel

`HomeViewModel.init` discards the result of
`connectivityPermissionManager.onLaunch()` and `HomeUiState` carries
no field for it, so a refused connectivity permission is never shown
and `requestAgain()` is never called. `HomeViewModel` stores whether
connectivity is denied, `HomeUiState` gains a
`connectivityPermissionReminderVisible` field computed in
`computeState()` alongside `sensorPermissionReminderVisible`, and
`HomeViewModel` exposes an `onConnectivityPermissionReminderClicked()`
action that calls `requestAgain()` and updates the stored flag from
the `Resolved` outcome, the same shape as the existing sensor
reminder; `HomeScreen` renders the reminder line and its "Autoriser"
action next to the existing sensor reminder block. This requires a new
resource key pair, for the connectivity reminder's text and action
label, since the existing `permission_reminder`/`permission_action`
strings are heart-rate-sensor specific.

## §10 Text

## §11 Access

## §12 Lifecycle

### §12.1 Nothing enters or leaves ambient mode

Bearer: MainActivity

`MainActivity` implements no ambient-mode callback, so
`AlwaysOnDisplayController.enterPowerSave` and `exitPowerSave` are
never called and the race pages carry no power-save layout or
ten-second refresh cadence. `MainActivity` observes the watch entering
and leaving ambient mode (a wrist raise or a screen touch exits it)
and calls `enterPowerSave` / `exitPowerSave` accordingly, exposing the
current `mode` and `refreshIntervalMs` so the active race page
switches to a power-save layout in `POWER_SAVE` and refreshes on the
`refreshIntervalMs` beat instead of continuously.

## Gaps set aside

None.
