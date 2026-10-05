## Signatures

WatchRaceNavigator.navigateTo(destination: WatchDestination): Unit
  — sets `current` directly to `destination`, unconditionally, bypassing
  the forward-only swipe/mark sequence every other transition method
  enforces.

MainActivity.onNewIntent(intent: Intent): Unit
  — reads `intent.getStringExtra(WatchRaceComplicationDataSourceService.EXTRA_TAPPED_DESTINATION)`;
  when present, calls `navigator.navigateTo(WatchDestination.valueOf(extra))`;
  when absent, does nothing.

interface AmbientBinder
  fun bind(activity: ComponentActivity, onEnterAmbient: () -> Unit, onExitAmbient: () -> Unit): Unit
    — installs whatever makes `activity` observe ambient-mode transitions;
    calls `onEnterAmbient()` when the watch enters ambient mode, `onExitAmbient()`
    when it leaves (wrist raise or screen touch)
  fun unbind(): Unit
    — reverses `bind`; no further call to either lambda follows, even if the
    bound activity is still reachable in memory

class AmbientLifecycleObserverBinder : AmbientBinder
  — the production implementation. `bind` installs a real
  `androidx.wear.ambient.AmbientLifecycleObserver` on `activity.lifecycle`
  (`lifecycle.addObserver(AmbientLifecycleObserver(activity, callback))`),
  whose callback's `onEnterAmbient`/`onExitAmbient` invoke the two lambdas
  `bind` was given. `unbind` removes that same observer from the lifecycle
  it was added to. Per the Decision: untestable under Robolectric — the
  observer's own `onCreate` reaches a device-populated stub
  (`WearableActivityController$AmbientCallback`) that throws
  `RuntimeException: Stub!` outside a real device — so no acceptance
  criterion exercises this class directly; a Robolectric-only `AmbientBinder`
  double stands in wherever `MainActivity` is launched under test.

MainActivity.onCreate — additionally:
  - `@Inject lateinit var ambientBinder: AmbientBinder`
  - constructs `alwaysOnDisplayController = AlwaysOnDisplayController()`
    directly (plain no-arg constructor, no DI — unchanged from the prior
    derivation, not implicated by the Decision)
  - holds a Compose-observable `displayMode` state, initialised to
    `alwaysOnDisplayController.mode`
  - calls `ambientBinder.bind(this, onEnterAmbient = { displayMode =
    alwaysOnDisplayController.enterPowerSave() }, onExitAmbient = {
    displayMode = alwaysOnDisplayController.exitPowerSave() })`
  - passes `displayMode` and `alwaysOnDisplayController.refreshIntervalMs`
    into the `WatchApp(...)` call as two new parameters, exposing them
    to the composable tree

MainActivity.onDestroy — additionally: calls `ambientBinder.unbind()`
  (alongside the existing `permissionHost.unbind()`)

Hilt wiring implied (no new project symbol beyond the two above):
`AmbientBinder` is bound, in a `SingletonComponent`-installed module, to
`AmbientLifecycleObserverBinder` — same `@Provides`/`impl: X` pattern
`SensorModule` already uses for `HapticFeedback` -> `HapticFeedbackImpl`.
A Robolectric-only test module replaces this binding with a double that
installs nothing and records/exposes the `onEnterAmbient`/`onExitAmbient`
lambdas it was given and its `unbind()` call count — the same
`@TestInstallIn` pattern `FakeSensorModule`/`FakeSyncModule` already use
for the other device-only bindings this module cannot resolve under
Robolectric.

## Acceptance criteria

- Calling `navigator.navigateTo(CONTROL)` from HOME sets `current` directly to CONTROL — a transition no forward-only method permits, demonstrating the bypass
- A tapped complication's `PendingIntent` extra, reaching `MainActivity.onNewIntent`, calls `navigator.navigateTo(WatchDestination.valueOf(extra))`, moving `current` to that destination
- An intent reaching `onNewIntent` with no `EXTRA_TAPPED_DESTINATION` leaves `navigator.current` unchanged
- With the Robolectric `AmbientBinder` double substituted, `MainActivity` reaches the resumed state without throwing — covering the four pre-existing `MainActivity`-launching tests and this lot's own
- Invoking the `onEnterAmbient` lambda the substituted double captured from `bind` sets `AlwaysOnDisplayController.mode` to `POWER_SAVE`, and `MainActivity`'s exposed `displayMode` reflects it
- Invoking the `onExitAmbient` lambda the substituted double captured from `bind` sets `AlwaysOnDisplayController.mode` to `NORMAL`, and `MainActivity`'s exposed `displayMode` reflects it
- `MainActivity`'s exposed `refreshIntervalMs` is null while `displayMode` is `NORMAL`, and equals `SensorFreshnessWindow.WINDOW_MS` while `displayMode` is `POWER_SAVE`
- After `MainActivity` is destroyed, the substituted `AmbientBinder` double's `unbind()` has been called exactly once

## Dependencies

WatchRaceNavigator — pre-existing, gains `navigateTo` in this lot
WatchDestination — pre-existing
AlwaysOnDisplayController, DisplayMode — pre-existing
SensorFreshnessWindow.WINDOW_MS — pre-existing
WatchRaceComplicationDataSourceService.EXTRA_TAPPED_DESTINATION — produced by lot-02 of this cycle
AmbientBinder, AmbientLifecycleObserverBinder — produced by this lot, per the Decision
androidx.wear.ambient.AmbientLifecycleObserver — framework, ships from `androidx.wear:wear` (1.4.0), not `androidx.wear:wear-ambient` (does not exist on Maven); not yet a declared Gradle dependency of `:app-wear`
androidx.activity.ComponentActivity — framework, already the base class of `MainActivity`
android.content.Intent — framework (Android SDK)

## Conventions

§1 · Hilt is the sole DI mechanism — `AmbientBinder` is bound through it, not constructed ad hoc where injected
§3 · anything touching the device's OS lives in the application module using it — `AmbientBinder`, `AmbientLifecycleObserverBinder` and the `onNewIntent`/ambient wiring stay in `:app-wear`'s `MainActivity`, no Android type leaks into `:core-domain`
§9 · the name of the rule, not of the structure — `navigateTo`, not e.g. `setCurrent`
§9 · identifiers and comments in English
§14 · Compose UI tests live in `src/test` under Robolectric; `androidTest` is never used — the reason `AmbientLifecycleObserverBinder` itself carries no acceptance criterion, only the `AmbientBinder` seam does
