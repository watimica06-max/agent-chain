## Symbols

WatchRaceNavigator.navigateTo — created
MainActivity.onNewIntent — created, `public override` (widened from the framework's `protected`, for direct test access)
AmbientBinder — created
AmbientLifecycleObserverBinder — created
MainActivity.onCreate — modified, injects `ambientBinder`, exposes `alwaysOnDisplayController`/`displayMode`, calls `ambientBinder.bind`, passes `displayMode`/`refreshIntervalMs` into `WatchApp`
MainActivity.onDestroy — modified, additionally calls `ambientBinder.unbind()`
DisplayModule — created
RecordingAmbientBinder — created (test)
FakeDisplayModule — created (test)

## Build

analyze: clean (`:app-wear:lint` clean)
test: 325 passed

## State

Added: AmbientBinder, AmbientLifecycleObserverBinder, DisplayModule, FakeDisplayModule/RecordingAmbientBinder, `androidx.wear:wear` Gradle dependency (`libs.versions.toml` key `wear`, 1.4.0)
Removed: —

## Convention

—
