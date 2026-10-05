## Signatures

    sealed interface ConnectivityPermissionState {
        object Granted : ConnectivityPermissionState
        object Fallback : ConnectivityPermissionState
    }

    sealed interface ConnectivityPermissionRequestOutcome {
        data class Resolved(val state: ConnectivityPermissionState) : ConnectivityPermissionRequestOutcome
        object RedirectedToSettings : ConnectivityPermissionRequestOutcome
    }

    interface ConnectivityPermissionSystem {

        /** The current OS pairing-permission state, with no prompt shown. */
        fun isGranted(): Boolean

        /**
         * Whether the system still offers its own permission dialog. False
         * once the user has refused it enough times that the OS commits to
         * silently denying any further prompt.
         */
        fun canShowSystemPrompt(): Boolean

        /**
         * Shows the system's pairing-permission dialog and suspends until
         * the user resolves it.
         */
        suspend fun requestPermission(): Boolean

        /** Opens the app's own permissions page in the system settings. */
        fun openAppSettings()
    }

    interface ConnectivityPermissionLaunchStore {

        /** True until the first ConnectivityPermissionManager.onLaunch() call ever completes. */
        fun isFirstLaunch(): Boolean

        /** Records that a ConnectivityPermissionManager.onLaunch() call has completed. */
        fun recordLaunch()
    }

    class ConnectivityPermissionManager(
        private val system: ConnectivityPermissionSystem,
        private val launchStore: ConnectivityPermissionLaunchStore,
    ) {

        /**
         * Called once per app launch. Prompts for the pairing permission on
         * the first-ever launch; on every later launch, only rechecks the
         * current OS state without showing any dialog.
         */
        suspend fun onLaunch(): ConnectivityPermissionState

        /**
         * Called when the user asks to be prompted again. Shows the system
         * dialog again when it is still offered; otherwise redirects to the
         * app's own permissions page.
         */
        suspend fun requestAgain(): ConnectivityPermissionRequestOutcome
    }

## Acceptance criteria

- On the first-ever launch, `onLaunch()` requests the pairing permission and returns `Granted` when the system grants it
- On the first-ever launch, `onLaunch()` requests the pairing permission and returns `Fallback` when the system refuses it
- On any launch after the first, `onLaunch()` returns the current OS grant state without requesting the permission again
- A permission revoked after being granted on an earlier launch produces `Fallback` on the next `onLaunch()` call, the same as an initial refusal
- After the first-ever launch (granted or refused), no later `onLaunch()` call invokes `requestPermission()` — only `requestAgain()` does
- `requestAgain()` requests the permission again and returns `Resolved` carrying the outcome, when `canShowSystemPrompt()` is true
- `requestAgain()` opens the app's settings page and returns `RedirectedToSettings`, without requesting the permission, when `canShowSystemPrompt()` is false

## Dependencies

ConnectivityPermissionState — produced by this lot
ConnectivityPermissionRequestOutcome — produced by this lot
ConnectivityPermissionSystem — produced by this lot (interface only, no OS-backed implementation yet)
ConnectivityPermissionLaunchStore — produced by this lot (interface only, no persisted implementation yet)
