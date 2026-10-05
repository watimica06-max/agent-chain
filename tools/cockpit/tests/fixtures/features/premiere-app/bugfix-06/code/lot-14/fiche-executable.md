## Signatures

com.mgilli.core.platform.connectivity.permission.ConnectivityPermissionSystemImpl(
  activity: Activity,
  launcher: ActivityResultLauncher<String>,
  requestHistory: SharedPreferences,
) : ConnectivityPermissionSystem — declared once, in :core-platform
  — same body as the two copies it replaces (grepped identical in
    `app-phone/.../connectivity/permission/ConnectivityPermissionSystemImpl.kt`
    and `app-wear/.../connectivity/permission/ConnectivityPermissionSystemImpl.kt`):
    `isGranted()` reads `ContextCompat.checkSelfPermission` against
    `BLUETOOTH_CONNECT`; `canShowSystemPrompt()` reads the persisted
    "has ever been requested" bit from `requestHistory`, then
    `ActivityCompat.shouldShowRequestPermissionRationale`;
    `requestPermission()` suspends on a `CompletableDeferred<Boolean>`
    resolved by `onPermissionResult`, launching `launcher` on
    `BLUETOOTH_CONNECT`; `openAppSettings()` starts
    `ACTION_APPLICATION_DETAILS_SETTINGS` on the activity's own package
  — constructed by `bind(...)` on both `:app-phone`'s and `:app-wear`'s
    own `ActivityBoundPermissionHost`, replacing each module's own
    former copy

ActivityBoundPermissionHost (:app-phone), ActivityBoundPermissionHost
(:app-wear) — unchanged public signature; `bind(...)`, `unbind()`,
`onPermissionResult`/`onConnectivityPermissionResult` and the exposed
`ConnectivityPermissionSystem` surface are the same as today. Only what
they import changes: `ConnectivityPermissionSystemImpl` now resolves to
`com.mgilli.core.platform.connectivity.permission.ConnectivityPermissionSystemImpl`
instead of each module's own local class of that name, since that
local class is removed.

ConnectivityModule (:app-phone), PermissionModule (:app-wear) —
unchanged. Neither references `ConnectivityPermissionSystemImpl` by
name — both bind only `ConnectivityPermissionSystem` (the :core-domain
interface) to `ActivityBoundPermissionHost` (grepped: no import of the
Impl class in either file); nothing in them needs to change for the
relocation.

## Acceptance criteria

- Exactly one `ConnectivityPermissionSystemImpl` class exists in the
  project, declared in `:core-platform`; neither `:app-phone` nor
  `:app-wear` declares its own copy of that name any more
- `:app-phone`'s `ActivityBoundPermissionHost.bind(...)` constructs
  that same `:core-platform` class as its delegate, not a
  module-local copy
- `:app-wear`'s `ActivityBoundPermissionHost.bind(...)` constructs
  that same `:core-platform` class as its `connectivityDelegate`, not
  a module-local copy
- The relocated `ConnectivityPermissionSystemImplTest` lives once, in
  `:core-platform`; `:app-phone` and `:app-wear` no longer each carry
  their own copy of it

## Dependencies

ConnectivityPermissionSystem — pre-existing (:core-domain)
:core-platform — produced by lot-54 (same block)
ActivityBoundPermissionHost (:app-phone), ActivityBoundPermissionHost
  (:app-wear) — pre-existing, modified here (import only)
ConnectivityModule (:app-phone), PermissionModule (:app-wear) —
  pre-existing, unchanged

## Conventions

R15 · any adapter both applications need lives in a module they both
  depend on and that depends on neither
R12 · :core-platform realizes §11.1 in the module table
R14 · no module of another nature imports :app-phone or :app-wear
R63 · identifiers, comments and docs in English; one line per exported
  symbol saying what it guarantees and when it fails

## Requests

—
