## Symbols

SensorPermissionUiState — created
SensorPermissionViewModel — created
SensorPermissionScreen — created

## Build

analyze: clean
test: 6 passed

## State

Added: SensorPermissionViewModel / SensorPermissionScreen
Removed: —

## Convention

`app-wear/build.gradle.kts` had no Compose UI toolkit dependency —
`androidx.compose.material3` is added, matching how `app-phone` already
uses it (`Text` styled directly through `DesignTokens`, no
`MaterialTheme`). No conflicting instruction was proposed elsewhere; the
addition follows the existing sibling-module pattern rather than
introducing a new one.
