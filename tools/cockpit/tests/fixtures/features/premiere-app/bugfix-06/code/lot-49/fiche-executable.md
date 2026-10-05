# fiche-executable — lot-49

## Signatures

WatchRaceNavigator.current: StateFlow<WatchDestination>          modified
  — Type, first read and synchronous computation unchanged: at
    `current`'s first access the value comes from
    `sensorPermissionGranted()` alone — SENSOR_PERMISSION when false,
    WAITING_FOR_PHONE otherwise — and that same first access launches
    the `raceInProgress`/`profileAlreadySynced` check on `scope`.
    What changes: when that check resolves it writes
    `WatchDestination.MAIN` (race in progress) or
    `WatchDestination.HOME` (no race, profile already synced) only
    while the value it finds is still SENSOR_PERMISSION or
    WAITING_FOR_PHONE, and writes nothing on every other destination,
    leaving `current` as it stands. Never null; the check writes at
    most once.

WatchRaceNavigator.navigateTo(destination: WatchDestination) → Unit
                                                                unchanged
  — Signature and unconditional write unchanged. The call is itself a
    first access to `current`, so it starts the check above; the guard
    is what makes the destination it wrote stand once that check
    resolves.

WatchRaceNavigator — everything else                            unchanged
  — `NavigationModule.provideWatchRaceNavigator`, the constructor,
    `onSensorPermissionResolved`, `onProfileSynced`, `onMarked`,
    `onUndo`, `launchRace`, `checkInactivity`, `backGestureEnabled` and
    the forward-only swipe chain stay as lot-34 left them.

MainActivity.onCreate(savedInstanceState: Bundle?) → Unit        modified
  — Keeps its existing body (both permission launchers,
    `permissionHost.bind`, `ambientBinder.bind`, `setContent`) and adds
    a read of `WatchRaceComplicationDataSourceService
    .EXTRA_TAPPED_DESTINATION` off this activity's own `intent`:
    present and naming a `WatchDestination` constant → `navigator
    .navigateTo(that destination)`; absent, or naming no constant the
    enum declares → no navigation at all and no throw, `current` left
    on what its own first read produces. Same extra key and same effect
    as `onNewIntent`.

MainActivity.exerciseSessionManager: ExerciseSessionManager         added
  — `@Inject lateinit var`, resolved from `SensorModule`'s existing
    binding (and `FakeSensorModule`'s under test).

MainActivity.alwaysOnDisplayController: AlwaysOnDisplayController
                                                                 modified
  — Was `val alwaysOnDisplayController = AlwaysOnDisplayController()`,
    becomes an `@Inject lateinit var`. `AlwaysOnDisplayController`'s own
    API — `mode`, `refreshIntervalMs`, `enterPowerSave()`,
    `exitPowerSave()` — is unchanged.

MainActivity.displayMode: DisplayMode                            modified
  — Still a public `mutableStateOf` with a `private set`. Its initial
    value no longer comes from the controller at field-initialiser
    time: Hilt assigns `@Inject` fields inside the generated
    `onCreate`, after every field initialiser has run, so the property
    is initialised to `DisplayMode.NORMAL` and set from
    `alwaysOnDisplayController.mode` inside `onCreate`, before
    `setContent`.

MainActivity's `ambientBinder.bind` callbacks                    modified
  onEnterAmbient → Unit
    — Sets `displayMode` from
      `alwaysOnDisplayController.enterPowerSave()` as today, and calls
      `exerciseSessionManager.onInteractivityChanged(false)`.
  onExitAmbient → Unit
    — Sets `displayMode` from
      `alwaysOnDisplayController.exitPowerSave()` as today, and calls
      `exerciseSessionManager.onInteractivityChanged(true)`.
  — `onInteractivityChanged(interactive: Boolean): Boolean` is
    `suspend`, and `false` is a failure of the underlying Health
    Services call, not "no session". The call runs on a coroutine tied
    to the activity's lifecycle (`androidx.lifecycle.lifecycleScope`),
    so the callback returns Unit without waiting on it, whatever the
    outcome.

DisplayModule.provideAlwaysOnDisplayController(): AlwaysOnDisplayController
                                                                    added
  — `@Provides @Singleton`, returns `AlwaysOnDisplayController()`. One
    instance per process, so `mode` and `refreshIntervalMs` survive an
    activity recreation. The existing `provideAmbientBinder` binding is
    unchanged.

WatchApp(navigator, raceRepository, raceRecordingRepository,
         profileRepository, sensorPermissionManager,
         displayMode: DisplayMode, refreshIntervalMs: Long?) → Unit
                                                          modified body
  — MAIN / PROJECTION / CONTROL no longer call
    `raceRecordingRepository.findInProgress()` in the composition body.
    Each branch holds the in-progress race in a `produceState<Race?>`
    (initial value null) whose block performs the read: one read per
    entry into the branch, none on a recomposition, and a form that
    still compiles once lot-50 makes `findInProgress` `suspend`. The
    branch renders nothing while the value is null, exactly as the
    existing `race != null` guard already does.
  — MAIN holds `sensorPermissionManager.isGranted()` in a
    `remember { }`: read once on entry into the branch, not on every
    recomposition. It stays non-suspend.
  — MAIN calls `MainRacePageScreen` with `displayMode = displayMode`
    and `refreshIntervalMs = refreshIntervalMs` — the two values
    `WatchApp` already receives — instead of leaving both to their
    NORMAL/null defaults.
  — END's `observeRecorded()` collection, the `profile` `produceState`
    and the `referenceRace` `produceState` lot-56 built are unchanged.

AndroidManifest.xml (:app-wear) — MainActivity's `<activity>`    modified
  — Carries `android:launchMode="singleTop"` alongside its existing
    `android:name` and `android:exported="true"` and its MAIN/LAUNCHER
    intent filter.

## Acceptance criteria

- With a race in progress, `navigateTo(WatchDestination.PROJECTION)`
  issued at `current`'s first access, before the asynchronous check
  resolves, leaves `current` on PROJECTION after that check resolves
- With a race in progress and no `navigateTo`, `current` is MAIN once
  the check resolves
- With no race in progress, a synced profile and no `navigateTo`,
  `current` is HOME once the check resolves
- With the sensor permission not granted, `current`'s first read is
  SENSOR_PERMISSION and a race in progress still moves it to MAIN once
  the check resolves
- `onProfileSynced()` called before the check resolves leaves `current`
  on HOME after it resolves, even with a race in progress
- Launching `MainActivity` with an intent carrying
  `EXTRA_TAPPED_DESTINATION` = "CONTROL", with a race in progress,
  shows the control page — not the home page and not the main page
- Launching `MainActivity` with an intent carrying no
  `EXTRA_TAPPED_DESTINATION`, with a race in progress, shows the main
  page
- Launching `MainActivity` with `EXTRA_TAPPED_DESTINATION` set to a
  string no `WatchDestination` constant is named after leaves `current`
  on its first-read value and reaches composition without throwing
- `MainActivity`'s manifest entry declares
  `android:launchMode="singleTop"`
- Entering ambient mode reconfigures the running exercise session to
  batched data delivery
- Exiting ambient mode reconfigures it to continuous data delivery
- The `onEnterAmbient` callback returns while that reconfiguration is
  still pending — it never waits on Health Services
- While ambient mode is on and `current` is MAIN, the main race page is
  composed with `DisplayMode.POWER_SAVE` and `refreshIntervalMs` equal
  to `SensorFreshnessWindow.WINDOW_MS`; while ambient mode is off, with
  `DisplayMode.NORMAL` and null
- After entering ambient mode and recreating the activity, the
  recreated activity's `displayMode` is `DisplayMode.POWER_SAVE`
- Entering the MAIN branch calls `findInProgress()` exactly once; a
  recomposition of that branch adds no further call
- Entering the PROJECTION branch calls `findInProgress()` exactly once;
  a recomposition of that branch adds no further call
- Entering the CONTROL branch calls `findInProgress()` exactly once; a
  recomposition of that branch adds no further call
- Entering the MAIN branch calls `SensorPermissionManager.isGranted()`
  exactly once; a recomposition of that branch adds no further call
- Leaving MAIN and returning to it calls `findInProgress()` a second
  time — the read is once per entry, not once per process

## Dependencies

WatchRaceNavigator — modified by lot-34
WatchRaceNavigatorTest — modified by lot-34
WatchDestination — pre-existing
MainActivity (:app-wear) — pre-existing, modified by lot-56
WatchApp — pre-existing, modified by lot-56
MainActivityHomeAndRaceScreensTest — pre-existing
ManifestTest — pre-existing
WatchRaceComplicationDataSourceService.EXTRA_TAPPED_DESTINATION —
  modified by lot-48
WatchComplicationEntry.entryPoint — modified by lot-48
AlwaysOnDisplayController — pre-existing
DisplayMode — pre-existing
DisplayModule — pre-existing
AmbientBinder — pre-existing
ExerciseSessionManager.onInteractivityChanged — modified by lot-45
SensorModule / FakeSensorModule — modified by lot-45
MainRacePageScreen — modified by lot-41
SensorFreshnessWindow.WINDOW_MS — modified by lot-05
RaceRecordingRepository.findInProgress — pre-existing; made `suspend`
  by lot-50, which runs after this lot
SensorPermissionManager.isGranted — pre-existing
Race, Profile — pre-existing
androidx.lifecycle.lifecycleScope — declared dependency
  (`androidx.lifecycle:lifecycle-runtime-ktx`, `app-wear/build.gradle.kts`)

## Conventions

R4 · `./gradlew check` exits 0
R17 · no unit-carrying bare primitive in a new public signature
R19 · a public operation that can block is `suspend`
R24 · an operation reaching outside the process moves to its own thread
R30 · no empty and no generic catch
R32 · data entering from outside the process is validated where it is
  received — the launch intent's extra included
R34 · a caller that receives a failure acts on it —
  `onInteractivityChanged`'s Boolean
R39 · no mutable global state outside the entry point
R46 · the application resumes from what it read
R47 · a screen reads a source once per entry, never in a composition
  body
R48 · what one moment opens, the opening module releases on its own
  scope — the ambient binding
R53 · no direct write to standard output; `android.util.Log`
R54 · no data attached to a person in a log message
R55 · one nominal and one failure test per public function, this lot
R62 · the lexicon — PowerSave, Idle, Permission, Sensor,
  ExerciseSession
R63 · English identifiers; one line per exported symbol
R66 · no new dependency inside a lot
R77 · no new `libs.versions.toml` or `build.gradle.kts` entry
R79 · a failure neither carried into a state nor propagated is logged
  at ERROR, naming the operation
R81 · a unit test whose subject reaches an `android.*` method carries
  `@RunWith(RobolectricTestRunner::class)`
R84 · a `@TestInstallIn` fake whose value two test classes need to
  differ reads a mutable top-level `var`, set from the instance `init`
  block
R86 · a test file's owner is the lot whose scope covers the subject it
  exercises

## Requests

—
