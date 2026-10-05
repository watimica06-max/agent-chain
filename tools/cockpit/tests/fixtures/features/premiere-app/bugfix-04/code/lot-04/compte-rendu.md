## Symbols

HomeViewModel.currentConnectivityPermissionReminderVisible — created
HomeViewModel's init block — modified, resolves `connectivityPermissionManager.onLaunch()` into `currentConnectivityPermissionReminderVisible`
HomeViewModel.onConnectivityPermissionReminderClicked() — created
HomeViewModel.computeState() — modified, now also sets `HomeUiState.connectivityPermissionReminderVisible`
HomeUiState.connectivityPermissionReminderVisible — created
HomeScreen — modified, renders the connectivity reminder line and its "Autoriser" action next to the sensor reminder block, gated on `uiState.connectivityPermissionReminderVisible`
showsConnectivityPermissionReminder — created
WatchStringResources.Connectivity — created

## Build

analyze: clean
test: 317 passed (`:app-wear:check`)

## State

Added: —
Removed: —

## Convention

—
