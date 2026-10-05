## Symbols

No symbol is produced or modified — this lot only edits build configuration.

## Build

analyze: clean
test: `:app-phone:check` passed, `:app-wear:check` passed

## State

Added: Hilt Gradle plugin/version trap (`Traps — general`, `CURRENT_TECHNICAL_STATE.md`)
Removed: —

## Convention

The sheet leaves the Hilt version open ("a Hilt/Dagger release
compatible with Kotlin 2.2.10 / AGP 9.3.1"). 2.57.2 fails to apply
under AGP 9.3.1 (`Android BaseExtension not found` in
`HiltGradlePlugin.configureCompileClasspath`); 2.60.1 applies cleanly
and both module checks pass. `gradle/libs.versions.toml` pins `hilt` to
`2.60.1`.

The amendment leaves the `hiltNavigationCompose` version open ("an
androidx.hilt:hilt-navigation-compose release compatible with hilt
2.60.1 / composeBom 2026.02.01"). `gradle/libs.versions.toml` pins
`hiltNavigationCompose` to `1.3.0`; both module checks pass with it.

The second amendment adds `androidx-lifecycle-runtime-compose`, sharing
`lifecycleRuntimeKtx`'s version key as the sheet directs — no new
version to pick.
