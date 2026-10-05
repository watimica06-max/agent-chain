## Symbols

WatchRaceNavigator.current — modified, first-access asynchronous check now writes MAIN/HOME only while `current` is still SENSOR_PERMISSION or WAITING_FOR_PHONE, nothing otherwise
WatchRaceNavigator.navigateTo(destination: WatchDestination) → Unit — unchanged
WatchRaceNavigator — everything else — unchanged
MainActivity.onCreate(savedInstanceState: Bundle?) → Unit — modified, reads WatchRaceComplicationDataSourceService.EXTRA_TAPPED_DESTINATION off its own launch intent and calls navigator.navigateTo, sets displayMode from alwaysOnDisplayController.mode, ambient callbacks now also capture exerciseSessionManager.onInteractivityChanged's Boolean and log at ERROR, naming the operation, on a false result
MainActivity.exerciseSessionManager: ExerciseSessionManager — added
MainActivity.alwaysOnDisplayController: AlwaysOnDisplayController — modified, now `@Inject lateinit var`
MainActivity.displayMode: DisplayMode — modified, initial value DisplayMode.NORMAL, set from alwaysOnDisplayController.mode inside onCreate
DisplayModule.provideAlwaysOnDisplayController(): AlwaysOnDisplayController — added
WatchApp(navigator, raceRepository, raceRecordingRepository, profileRepository, sensorPermissionManager, displayMode, refreshIntervalMs) → Unit — modified body and visibility (private to internal, for direct test access)
AndroidManifest.xml (:app-wear) MainActivity's `<activity>` — modified, carries android:launchMode="singleTop"
tappedDestination(intent: Intent): WatchDestination? — added, private helper backing onCreate's safe extra parsing
FakeSensorModule.fakeExerciseSessionSystem — added, mutable top-level var (R84) letting a test observe/gate ExerciseSessionSystem calls
FakeDisplayModule.provideAlwaysOnDisplayController() — added, required once DisplayModule gained the same binding under a full-module @TestInstallIn replacement
ManifestTest — modified, one test added for the manifest's launchMode
WatchRaceNavigatorTest — modified, three tests added
MainActivityAmbientAndTapNavigationTest — modified, four tests added and an R84 init/@After pair
MainActivityHomeAndRaceScreensTest — modified, one test added
MainActivityColdLaunchNavigationTest — created
WatchAppReadOnceTest — created

## Build

analyze: no ktlint/detekt task is wired into this project's Gradle build (none found under any module or the root); `./gradlew :app-wear:check` is this project's actual verification command (R72 — only :app-wear is touched) and it exits 0
test: 517 passed

## State

Added: DisplayModule/AlwaysOnDisplayController singleton binding (survives a MainActivity recreation); WatchRaceNavigator's guarded first-access write; MainActivity's cold-launch EXTRA_TAPPED_DESTINATION handling; MainActivity/ExerciseSessionManager ambient wiring; AndroidManifest.xml singleTop
Removed: —

## Requests

—
