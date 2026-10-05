## Symbols

ConnectivityPermissionState — created
ConnectivityPermissionRequestOutcome — created
ConnectivityPermissionSystem — created
ConnectivityPermissionLaunchStore — created
ConnectivityPermissionManager — created

## Build

analyze: clean
test: 7 passed

## State

Added: ConnectivityPermissionManager, ConnectivityPermissionSystem, ConnectivityPermissionLaunchStore
Removed: —

## Convention

`TECHNICAL_CONVENTIONS.md` allows `:core-domain` to hold any interface
whose signatures take no `Context` (§3), which is where this lot's
symbols now live. The existing `SensorPermissionManager` in `:app-wear`
follows the same shape (first-launch prompt, later recheck, manual
re-request with a settings fallback) but sits in an app module instead,
for a permission concern that is arguably just as Context-free at the
interface level. The convention does not say whether a permission
manager's home is decided by its signatures alone or by where its
eventual OS-backed implementation will live — worth settling explicitly
so the two do not diverge on module placement for the same kind of
symbol.
