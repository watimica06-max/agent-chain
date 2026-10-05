## Symbols

WatchRaceNavigator — modified, `current` is now `StateFlow<WatchDestination>`
HyroxWearApplication — created
ActivityBoundPermissionHost — created
MainActivity — created
HapticFeedbackImpl — created

## Build

analyze: clean (`:app-wear:check` — compile, lint, unit tests)
test: 289 passed

## State

Added: MainActivity (:app-wear), HyroxWearApplication, ActivityBoundPermissionHost (:app-wear), HapticFeedbackImpl, :app-wear's Hilt DI graph (RepositoryModule, SyncModule, SensorModule, PermissionModule, RaceControllerModule, NavigationModule, TimingModule)
Removed: the "no entry point" dead state; the "nothing wires SensorPermissionManager" trap; the ":app-wear still has no DI graph" notes on `:app-phone`'s DI graph, `ConnectivityPermissionManager` and `LinkStateMonitor`; "no platform implementation exists yet" on `HapticFeedback`

## Convention

—
