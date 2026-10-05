## Symbols

WatchApp
  root BackHandler reading WatchRaceNavigator.backGestureEnabled, stepping back where true (HOME, PREPARATION) and consuming the gesture where false (MAIN, PROJECTION, CONTROL, END)   §4.1
  PREPARATION branch BackHandler calling WatchRaceNavigator.quitPreparation()   §4.2

WatchRaceNavigator
  backGestureEnabled (read, already carries it)   §4.1
  quitPreparation() (called, already carries it)   §4.2
  a method setting current directly to an external target (gap)   §7.1

WatchComplicationEntry
  entryPoint(current) (read, already carries it)   §7.1

WatchRaceComplicationDataSourceService — does not exist
  publishes a complication while a race is in progress   §7.1
  registered as a ComplicationDataSourceService in the app-wear manifest   §7.1
  opens the app on the page entryPoint names when the complication is tapped   §7.1

MainActivity
  onNewIntent, reading the tapped destination from the PendingIntent extra and passing it to WatchRaceNavigator's new method (gap)   §7.1
  observes the watch entering/leaving ambient mode (wrist raise or screen touch exits it) and calls AlwaysOnDisplayController.enterPowerSave()/exitPowerSave() accordingly (gap)   §12.1
  exposes AlwaysOnDisplayController's current mode and refreshIntervalMs (gap)   §12.1

AlwaysOnDisplayController
  enterPowerSave() (already carries it)   §12.1
  exitPowerSave() (already carries it)   §12.1
  mode (already carries it)   §12.1
  refreshIntervalMs (already carries it)   §12.1

HomeViewModel
  stores whether connectivity is denied, from connectivityPermissionManager.onLaunch()'s result (gap)   §9.1
  onConnectivityPermissionReminderClicked(), calling requestAgain() and updating the stored flag from its Resolved outcome (gap)   §9.1

HomeUiState
  connectivityPermissionReminderVisible field, computed in computeState() alongside sensorPermissionReminderVisible (gap)   §9.1

HomeScreen
  renders the connectivity reminder line and its "Autoriser" action next to the existing sensor reminder block (gap)   §9.1

WatchStringResources
  connectivity reminder text + action label LabelRefs, over a new resource key pair (gap)   §9.1

ConnectivityPermissionManager
  onLaunch() (already carries it)   §9.1
  requestAgain() (already carries it)   §9.1

## Sections with no entries

§1 Model, §2 Persistence, §3 Calculation, §5 External source, §6 Synchronisation,
§8 Journey, §10 Text, §11 Access — no entries, no lot.

## lot-01

Anchor: §4.1 — Back gesture not disabled during a race; §4.2 — Back gesture does not leave the preparation screen
Needs: WatchRaceNavigator.backGestureEnabled (pre-existing), WatchRaceNavigator.quitPreparation() (pre-existing)
Produces: —
Modifies: WatchApp

## lot-02

Anchor: §7.1 — No watch-face complication is published
Needs: WatchComplicationEntry.entryPoint (pre-existing), RaceRecordingRepository (pre-existing, to detect a race in progress), MainActivity (pre-existing, target of the published PendingIntent)
Produces: WatchRaceComplicationDataSourceService (declared as a ComplicationDataSourceService in the app-wear manifest; mounted by the system, tapped by the user, its intent handled by lot-03's MainActivity.onNewIntent)
Modifies: —

## lot-03

Anchor: §7.1 — No watch-face complication is published; §12.1 — Nothing enters or leaves ambient mode
Needs: AlwaysOnDisplayController (pre-existing), WatchRaceComplicationDataSourceService (lot-02, for the tapped-destination extra it emits)
Produces: —
Modifies: MainActivity, WatchRaceNavigator

## lot-04

Anchor: §9.1 — A refused connectivity permission is never surfaced
Needs: ConnectivityPermissionManager.onLaunch() (pre-existing), ConnectivityPermissionManager.requestAgain() (pre-existing)
Produces: —
Modifies: HomeViewModel, HomeUiState, HomeScreen, WatchStringResources
