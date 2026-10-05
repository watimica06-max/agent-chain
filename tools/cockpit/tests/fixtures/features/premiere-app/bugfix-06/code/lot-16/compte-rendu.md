## Symbols

ProfileSyncPushService (:core-domain) — modified
ProfileSyncListenerService (:app-wear) — modified
SyncModule (:app-wear), object — modified
SyncModule (:app-phone), object — modified
FakeSyncModule (:app-wear test), object — modified

## Build

analyze/test: `:core-domain:check` clean, `:app-wear:check` clean
(including `ProfileSyncPushServiceTest`, `ProfileSyncListenerServiceTest`).
`:app-phone:compileDebugKotlin` fails on `ProfileViewModel.kt` calling
`ProfileRepository.updateHrMaxBpm`, `updateExpectedDistanceM`,
`updateLongPressMs` and `updateZoneThreshold` outside a coroutine —
pre-existing since `ProfileRepository` was made `suspend` (lot-01),
unrelated to any symbol this lot touches; `SyncModule.kt` (:app-phone)
itself raises no compiler error (`kspDebugKotlin` also ran clean over
it) and `decoupage.md`'s `ProfileScreen, ProfileViewModel, ProfileUiState`
entry (lot-19, "the four setting handlers run inside
viewModelScope.launch") is the lot that adapts those four call sites —
R72/R73.

## State

Added: —
Removed: —
(`ProfileSyncPushService`, `ProfileSyncListenerService`, the `:app-phone`
and `:app-wear` Hilt DI graph entries rewritten in place; new Traps —
general entry on testing a `@AndroidEntryPoint` `Service`'s
`onCreate`/`onDestroy` under Robolectric)

## Requests

—
