## Symbols

ConnectivityPermissionSystemImpl (:core-platform) — created
ActivityBoundPermissionHost (:app-phone) — modified, import only
ActivityBoundPermissionHost (:app-wear) — modified, import only

## Build

analyze: n/a (no ktlint task wired in this project)
test: core-platform 7 passed; app-wear 8 passed (ActivityBoundPermissionHostTest)
check: `:core-platform:check` PASS; `:app-wear:check` PASS;
  `:app-phone:check` FAILS only on `ProfileViewModel.kt` lines 121, 128,
  135, 143 — four pre-existing suspend-call-site errors against
  `ProfileRepository.updateHrMaxBpm`/`updateExpectedDistanceM`/
  `updateLongPressMs`/`updateZoneThreshold`, unrelated to this lot's
  changes and unrelated to any file this lot touches. The signature
  (`ProfileRepository`, `:core-domain`) and the call site
  (`ProfileViewModel`, `:app-phone`) sit in different modules, so R72's
  deferral applies (R74). `code/lot-17/fiche-executable.md` already
  names lot-19 as the owner of `ProfileViewModel`'s remaining rework
  that closes this gap.

## State

Added: ConnectivityPermissionSystemImpl (:core-platform)
Removed: ConnectivityPermissionSystemImpl (:app-phone),
  ConnectivityPermissionSystemImpl (:app-wear)

## Requests

—
