## Symbols

WaitingForPhoneViewModel — modified, constructor gains `navigator: WatchRaceNavigator`; on a
  Profile whose `lastSyncSuccessAt` is non-null it calls `navigator.onProfileSynced()` instead
  of writing a UI-state field
WaitingForPhoneViewModel.uiState — modified, one value fixed at construction, never changes
WaitingForPhoneUiState — modified, `hasReceivedProfile: Boolean` dropped
WaitingForPhoneScreen — unchanged
WaitingForPhoneScreenTest — modified, same-module call site under R74; both constructor calls
  now pass a `WatchRaceNavigator`

## Build

analyze: clean (`./gradlew :app-wear:check`)
test: 385 passed

## State

Added: —
Removed: `WaitingForPhoneUiState.hasReceivedProfile` and its sticky-flag behaviour

## Requests

—
