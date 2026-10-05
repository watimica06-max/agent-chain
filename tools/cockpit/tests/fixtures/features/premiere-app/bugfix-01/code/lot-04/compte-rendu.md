## Symbols

ProfileViewModel — modified, adds linkStateMonitor and onZoneThresholdChanged
ProfileViewModel.onZoneThresholdChanged — created
ProfileScreen — ZonesSection — modified, renders zones 2-5's threshold as an editable field
ProfileScreenTest — created

## Build

analyze: clean (`:app-phone:check`, `:app-wear:check`, both include lint)
test: 135 passed (app-phone), 188 passed (app-wear)

## State

Added: Traps — general / `Modifier.onFocusChanged` fires once at attach
Removed: —

## Convention

—
