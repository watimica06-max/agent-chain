## Signatures

    data class SensorPermissionUiState(
        val title: String,
        val explanation: String,
        val actionLabel: String,
        val resolvedState: SensorPermissionState?
    )

    class SensorPermissionViewModel(
        private val sensorPermissionManager: SensorPermissionManager
    ) {

        val uiState: StateFlow<SensorPermissionUiState>

        /**
         * The action pill tapped (§4.1/§9.7): requests sensor access via
         * `SensorPermissionManager.onLaunch()` and records the outcome.
         */
        fun onActionClicked()
    }

    @Composable
    fun SensorPermissionScreen(viewModel: SensorPermissionViewModel)

## Acceptance criteria

- `uiState.title` equals `WatchStringResources.Permission.title`
- `uiState.explanation` equals `WatchStringResources.Permission.explanation`
- `uiState.actionLabel` equals `WatchStringResources.Permission.action`
- `uiState.resolvedState` is null before the action is tapped
- Tapping the action, given `SensorPermissionManager.onLaunch()` resolves to `SensorPermissionState.Granted`, sets `uiState.resolvedState` to `Granted`
- Tapping the action, given `SensorPermissionManager.onLaunch()` resolves to `SensorPermissionState.Fallback`, sets `uiState.resolvedState` to `Fallback`

## Dependencies

SensorPermissionManager — pre-existing (lot-13)
SensorPermissionState — pre-existing (lot-13)
DesignTokens — pre-existing (lot-02)
WatchStringResources — pre-existing (lot-44)
