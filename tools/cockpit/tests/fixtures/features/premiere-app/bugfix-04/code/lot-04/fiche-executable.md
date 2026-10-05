## Signatures

HomeViewModel — gains:

  private var currentConnectivityPermissionReminderVisible: Boolean = false
    (starts false; resolved once `connectivityPermissionManager.onLaunch()`
    completes, the same shape as `app-phone`'s `ProfileViewModel.isConnectivityDenied`)

  init block — the existing discarded
    `viewModelScope.launch { connectivityPermissionManager.onLaunch() }`
    becomes:
      viewModelScope.launch {
        val state = connectivityPermissionManager.onLaunch()
        currentConnectivityPermissionReminderVisible = state == ConnectivityPermissionState.Fallback
        recompute()
      }

  fun onConnectivityPermissionReminderClicked(): Unit
    — calls `connectivityPermissionManager.requestAgain()`; a `Resolved`
    outcome sets `currentConnectivityPermissionReminderVisible` from
    `outcome.state == ConnectivityPermissionState.Fallback` and recomputes;
    a `RedirectedToSettings` outcome leaves it unchanged.

  computeState() → HomeUiState gains
    `connectivityPermissionReminderVisible = currentConnectivityPermissionReminderVisible`
    alongside the existing `sensorPermissionReminderVisible`

HomeUiState — gains:
  val connectivityPermissionReminderVisible: Boolean

HomeScreen(viewModel, onHistoryClicked) — renders, next to the existing
  sensor reminder block and gated on
  `uiState.connectivityPermissionReminderVisible`, a reminder line using
  `WatchStringResources.Connectivity.reminder` and an "Autoriser" action
  using `WatchStringResources.Connectivity.action`, the action's tap
  calling `viewModel.onConnectivityPermissionReminderClicked()`

WatchStringResources — gains:
  object Connectivity {
    val reminder = LabelRef(R.string.connectivity_permission_reminder)
    val action = LabelRef(R.string.connectivity_permission_action)
  }

## Acceptance criteria

- When `ConnectivityPermissionManager.onLaunch()` resolves to `Fallback`, `HomeUiState.connectivityPermissionReminderVisible` becomes true
- When `onLaunch()` resolves to `Granted`, `connectivityPermissionReminderVisible` stays false
- Calling `onConnectivityPermissionReminderClicked()` calls `ConnectivityPermissionManager.requestAgain()`; a `Resolved(Granted)` outcome sets `connectivityPermissionReminderVisible` to false
- A `Resolved(Fallback)` outcome from `requestAgain()` keeps `connectivityPermissionReminderVisible` true
- A `RedirectedToSettings` outcome from `requestAgain()` leaves `connectivityPermissionReminderVisible` unchanged
- `HomeScreen` renders the connectivity reminder line and its "Autoriser" action exactly when `connectivityPermissionReminderVisible` is true, and tapping the action calls `onConnectivityPermissionReminderClicked()`

## Dependencies

ConnectivityPermissionManager — pre-existing
ConnectivityPermissionManager.onLaunch() — pre-existing
ConnectivityPermissionManager.requestAgain() — pre-existing
ConnectivityPermissionState.Granted / Fallback — pre-existing
ConnectivityPermissionRequestOutcome.Resolved / RedirectedToSettings — pre-existing
LabelRef — pre-existing
R.string.connectivity_permission_reminder — new resource key, produced by this lot
R.string.connectivity_permission_action — new resource key, produced by this lot

## Conventions

§10 · no hardcoded user-facing string; a new resource key pair for the connectivity reminder, distinct from the sensor-specific `permission_reminder`/`permission_action`; French only; stays in `app-wear`'s own resource file, never shared with `app-phone`
§11 · one `StateFlow` per screen holding a single immutable UI state class — the new field joins the existing `HomeUiState`, not a second `StateFlow`
§13 · never swallow an exception silently — the `RedirectedToSettings` branch is an intentional no-op, the same precedent the existing sensor reminder already sets, not a swallowed error
