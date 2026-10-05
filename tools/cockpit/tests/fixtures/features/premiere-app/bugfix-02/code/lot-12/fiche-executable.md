## Signatures

    // com.mgilli.app_wear.race — modified
    class WatchRaceNavigator(
      sensorPermissionGranted: Boolean,
      profileAlreadySynced: Boolean,
    ) {
      val current: StateFlow<WatchDestination>
      // Was a plain `var current: WatchDestination` with a private setter.
      // Every existing method (toPreparation, quitPreparation, launchRace,
      // swipeForward, onMarked, onFinalMarking, onUndo, onStopConfirmed,
      // finish, checkInactivity) keeps its own signature and the same
      // transition rules; each one now updates `current`'s value instead of
      // the backing var directly. backGestureEnabled, onInteraction,
      // onDialogOpened, onDialogClosed and the inactivity-timeout constant
      // are unchanged. Initial value: the same three-way rule already coded
      // (profileAlreadySynced -> HOME; else !sensorPermissionGranted ->
      // SENSOR_PERMISSION; else WAITING_FOR_PHONE).
    }

    // com.mgilli.app_wear — new
    @HiltAndroidApp
    class HyroxWearApplication : Application()

    // com.mgilli.app_wear.connectivity.permission — new
    // Bridges SensorPermissionSystem and ConnectivityPermissionSystem
    // (§9.1) from Activity-scoped implementations to the Singleton scope
    // Hilt resolves ViewModels against. A single class cannot implement
    // both interfaces directly: SensorPermissionSystem and
    // ConnectivityPermissionSystem declare the exact same four method
    // signatures (isGranted, canShowSystemPrompt, requestPermission,
    // openAppSettings), so one override would answer for both permissions
    // at once. Instead this class holds one delegate-holder per interface,
    // each independently bound/unbound.
    @Singleton
    class ActivityBoundPermissionHost @Inject constructor() {
      val sensorPermissionSystem: SensorPermissionSystem   // = SensorHost(), below
      val connectivityPermissionSystem: ConnectivityPermissionSystem   // = ConnectivityHost(), below

      fun bind(
        activity: Activity,
        sensorLauncher: ActivityResultLauncher<String>,
        connectivityLauncher: ActivityResultLauncher<String>,
        prefs: SharedPreferences
      )
      // Builds a new SensorPermissionSystemImpl(activity, sensorLauncher, prefs)
      // and a new ConnectivityPermissionSystemImpl(activity, connectivityLauncher, prefs),
      // and holds each as the current delegate behind sensorPermissionSystem/
      // connectivityPermissionSystem respectively, replacing any previous ones.

      fun unbind()
      // Drops both current delegates. No Activity, launcher or
      // SharedPreferences reference is retained afterward.

      fun onSensorPermissionResult(granted: Boolean)
      // Forwards to the currently bound SensorPermissionSystemImpl delegate's
      // onPermissionResult(granted). No effect while unbound.

      fun onConnectivityPermissionResult(granted: Boolean)
      // Forwards to the currently bound ConnectivityPermissionSystemImpl
      // delegate's onPermissionResult(granted). No effect while unbound.

      // sensorPermissionSystem and connectivityPermissionSystem each expose
      // isGranted/canShowSystemPrompt/openAppSettings as false/false/no-op
      // while unbound, and requestPermission() as false immediately, nothing
      // launched — same unbound behaviour as lot-10's ActivityBoundPermissionHost
      // (:app-phone). Bound, each matches its own delegate's outcome exactly.
    }

    // com.mgilli.app_wear — new
    @AndroidEntryPoint
    class MainActivity : ComponentActivity() {
      @Inject lateinit var navigator: WatchRaceNavigator
      @Inject lateinit var permissionHost: ActivityBoundPermissionHost
      @Inject lateinit var raceRecordingRepository: RaceRecordingRepository
      @Inject lateinit var raceRepository: RaceRepository
      @Inject lateinit var profileRepository: ProfileRepository

      // onCreate(savedInstanceState):
      // 1. registers two ActivityResultLauncher<String>, one on
      //    ActivityResultContracts.RequestPermission() for BODY_SENSORS
      //    (callback calls permissionHost.onSensorPermissionResult(granted)),
      //    one for the connectivity permission ConnectivityPermissionSystemImpl
      //    (app-wear, lot-20) checks (callback calls
      //    permissionHost.onConnectivityPermissionResult(granted))
      // 2. permissionHost.bind(this, sensorLauncher, connectivityLauncher,
      //    <a SharedPreferences instance>)
      // 3. setContent { <dispatch below> } — no HyroxTrackerTheme-equivalent
      //    exists on the watch (DesignTokens is applied per-composable, not
      //    through a MaterialTheme wrapper; unchanged by this lot)
      //
      // Dispatch: collects `navigator.current` (collectAsStateWithLifecycle),
      // `raceRepository.observeReference()` (collectAsStateWithLifecycle,
      // initialValue = null) and renders, per WatchDestination:
      //   SENSOR_PERMISSION  -> SensorPermissionScreen(hiltViewModel())
      //   WAITING_FOR_PHONE  -> WaitingForPhoneScreen(hiltViewModel(), onRetryClicked = {})
      //                         // no entry of this bugfix describes a retry
      //                         // action to wire (CURRENT_TECHNICAL_STATE.md:
      //                         // "this lot wires no retry action itself" —
      //                         // still true here, out of §9.1/§9.2/§9.4's scope)
      //   HOME               -> local `var showingHistory` (rememberSaveable,
      //                         reset to false whenever `current` leaves HOME):
      //                         false -> HomeScreen(hiltViewModel(),
      //                           onHistoryClicked = { showingHistory = true })
      //                         true  -> WatchHistoryScreen(
      //                           hiltViewModel<WatchHistoryViewModel>()
      //                             .uiState.collectAsStateWithLifecycle().value)
      //                           with a BackHandler(enabled = showingHistory)
      //                           { showingHistory = false } — WatchHistoryScreen
      //                           itself takes no navigation callback (reads
      //                           only WatchHistoryUiState)
      //   PREPARATION        -> PreparationScreen(hiltViewModel())
      //   MAIN               -> raceRecordingRepository.findInProgress().getOrNull()
      //                         (synchronous, non-suspend per its own signature);
      //                         null -> renders nothing (unreachable in practice:
      //                         WatchRaceNavigator only reaches MAIN through
      //                         PreparationViewModel.launchRace(), which only
      //                         calls navigator.launchRace() after RaceLaunchController
      //                         has started a race); non-null `race` ->
      //                         MainRacePageScreen(hiltViewModel(key = "main-${race.id}",
      //                         creationCallback = { f: MainRacePageViewModel.Factory ->
      //                         f.create(race, referenceRaceState.value, profile,
      //                         sensorPermissionManagerIsGranted) }) — `profile` and
      //                         `sensorPermissionManagerIsGranted` below
      //   PROJECTION         -> same `race` lookup as MAIN; non-null ->
      //                         ProjectionScreen(hiltViewModel(key = "projection-${race.id}",
      //                         creationCallback = { f: ProjectionViewModel.Factory ->
      //                         f.create(race, referenceRaceState.value, profile) })
      //   CONTROL            -> same `race` lookup; non-null ->
      //                         ControlScreen(hiltViewModel(key = "control-${race.id}",
      //                         creationCallback = { f: ControlViewModel.Factory ->
      //                         f.create(race) })
      //   END                -> the most recently finished race:
      //                         `raceRecordingRepository.observeRecorded()`
      //                         collected (collectAsStateWithLifecycle,
      //                         initialValue = emptyList()) — observeRecorded excludes
      //                         any race still in progress and orders the rest
      //                         most-recent-first (RaceRecordingRepository's own
      //                         contract), so its first entry is the race just
      //                         completed or stopped; null (list still empty at
      //                         first composition) -> renders nothing;
      //                         non-null `race` -> EndOfRaceScreen(hiltViewModel(
      //                         key = "end-${race.id}", creationCallback =
      //                         { f: EndOfRaceViewModel.Factory -> f.create(race,
      //                         referenceRaceState.value) })
      //
      // `profile` (MAIN/PROJECTION only): one-shot suspend read via
      // produceState(initialValue = null) { value = profileRepository.observe().first() },
      // gating MainRacePageScreen/ProjectionScreen's render until non-null —
      // `Profile` has no default constructor to fall back on synchronously.
      // `sensorPermissionManagerIsGranted` (MAIN only): SensorPermissionManager
      // .isGranted() — synchronous, side-effect-free, no prompt shown.
      //
      // onDestroy(): permissionHost.unbind()
    }

    // com.mgilli.app_wear.race — new, per Decision
    @Singleton
    class HapticFeedbackImpl @Inject constructor(
      @ApplicationContext context: Context
    ) : HapticFeedback {
      override fun confirmMarking()
      // One 50ms vibration pulse on the platform Vibrator obtained from
      // `context`. No-op when the device reports no vibrator.

      override fun cancelMarking()
      // Two 30ms vibration pulses, separated by an 80ms gap, on the same
      // Vibrator. No-op when the device reports no vibrator.
    }

    // Hilt wiring implied by lot-12's declared Needs (no new project symbol —
    // each of the following is a binding the DI graph must supply so the
    // nine @HiltViewModel/@AssistedFactory classes above construct):
    //   RaceRepository -> RaceRepositoryImpl(HyroxDatabase(context).raceDao())
    //   ProfileRepository -> ProfileRepositoryImpl(HyroxDatabase(context).profileDao())
    //     (same HyroxDatabase construction pattern as lot-10 (:app-phone);
    //     :app-wear opens its own instance of the same "hyrox-tracker.db"
    //     Room database, holding the reference race and the profile it reads
    //     and — for correctionFactor — writes)
    //   WatchHistoryStore -> WatchHistoryStoreImpl(WatchHistoryDatabase(context).raceHistoryDao())
    //     (:app-wear's own "watch-history.db" instance — lot-10 only built
    //     one on :app-phone because ProfileSyncPushService's constructor
    //     needed it there; :app-wear is the side WatchHistoryViewModel reads)
    //   RaceRecordingRepository -> RaceRecordingRepositoryImpl(profileRepository)
    //   RecordedRaceTransport -> WearableRecordedRaceTransport(context)
    //   LinkStateMonitor -> built from WearableLinkStateSource(context)
    //     .observeNodeConnected() as its rawLinkEstablished argument
    //   RecordedRaceSyncService -> RecordedRaceSyncService(raceRecordingRepository,
    //     raceRepository, recordedRaceTransport)
    //   ExerciseSessionSystem -> ExerciseSessionSystemImpl(HealthServices
    //     .getClient(context).exerciseClient)
    //   ExerciseSessionManager -> ExerciseSessionManager(exerciseSessionSystem)
    //   SensorPermissionSystem -> the ActivityBoundPermissionHost singleton's
    //     sensorPermissionSystem
    //   ConnectivityPermissionSystem -> the ActivityBoundPermissionHost
    //     singleton's connectivityPermissionSystem
    //   SensorPermissionLaunchStore -> SensorPermissionLaunchStoreImpl(prefs)
    //   ConnectivityPermissionLaunchStore -> ConnectivityPermissionLaunchStoreImpl(prefs)
    //     (app-wear's own copy, distinct from :app-phone's — lot-03)
    //   SensorPermissionManager -> SensorPermissionManager(sensorPermissionSystem,
    //     sensorPermissionLaunchStore)
    //   ConnectivityPermissionManager -> ConnectivityPermissionManager(
    //     connectivityPermissionSystem, connectivityPermissionLaunchStore)
    //   HapticFeedback -> the HapticFeedbackImpl singleton
    //   SegmentMarkingController -> SegmentMarkingController(raceRecordingRepository,
    //     hapticFeedback)
    //   RaceLaunchController -> RaceLaunchController(raceRecordingRepository,
    //     exerciseSessionManager)
    //   UndoMarkingController -> UndoMarkingController(raceRecordingRepository)
    //   StopRaceController -> StopRaceController(raceRecordingRepository,
    //     exerciseSessionManager)
    //   Clock -> SystemClock (same binding pattern as lot-10's TimingModule,
    //     :app-phone)
    //   WatchRaceNavigator -> built once, from:
    //     sensorPermissionGranted = sensorPermissionSystem.isGranted()
    //       (synchronous; by the time any ViewModel first requests this
    //       singleton, permissionHost.bind() has already run in onCreate,
    //       so the delegate answers for real)
    //     profileAlreadySynced = a one-shot synchronous read,
    //       runBlocking { profileRepository.observe().first() }.lastSyncSuccessAt != null
    //       — the same pattern RaceRecordingRepositoryImpl already relies on
    //       for its own synchronous profile read (CURRENT_TECHNICAL_STATE.md,
    //       RaceRecordingRepositoryImpl's ⚠️ note)

## Acceptance criteria

- `WatchRaceNavigator(sensorPermissionGranted = true, profileAlreadySynced = true).current.value` is `HOME`; with `profileAlreadySynced = false, sensorPermissionGranted = false`, `SENSOR_PERMISSION`; with `profileAlreadySynced = false, sensorPermissionGranted = true`, `WAITING_FOR_PHONE`
- After `toPreparation()`/`launchRace()`/`swipeForward()` (twice)/`onFinalMarking()`/`finish()` from a fresh `HOME`-starting navigator, `current.value` follows the same sequence (`PREPARATION` -> `MAIN` -> `PROJECTION` -> `CONTROL` -> ... ) already asserted by the existing behavioural tests — unaffected by `current` becoming a `StateFlow`
- MainActivity renders `SensorPermissionScreen` when `navigator.current` is `SENSOR_PERMISSION`, `WaitingForPhoneScreen` when `WAITING_FOR_PHONE`, `PreparationScreen` when `PREPARATION`
- MainActivity renders `HomeScreen` when `navigator.current` is `HOME`; tapping its history action renders `WatchHistoryScreen` instead, with the rows matching `WatchHistoryStore.observe()`'s current entries; a back gesture from there returns to `HomeScreen`
- MainActivity renders `MainRacePageScreen` when `navigator.current` is `MAIN` and a race is held by `RaceRecordingRepository.findInProgress()`, `ProjectionScreen` when `PROJECTION` under the same condition, both backed by the same `MainRacePageViewModel`/`ProjectionViewModel` construction inputs (the in-progress race, the current reference race, the current profile) — resolving a `MainRacePageViewModel`/`ProjectionViewModel` scoped to that race's id, not a previous race's instance
- MainActivity renders `ControlScreen` when `navigator.current` is `CONTROL`, scoped to the same in-progress race's id
- MainActivity renders `EndOfRaceScreen` when `navigator.current` is `END`, scoped to the most recently finished race reported by `RaceRecordingRepository.observeRecorded()`
- MainActivity reaches the resumed state without throwing (both permission-result launchers are registered before `ActivityBoundPermissionHost.bind` is called, itself before the activity leaves the created state)
- Before any `bind`, `ActivityBoundPermissionHost.sensorPermissionSystem.isGranted()`/`.canShowSystemPrompt()` and `.connectivityPermissionSystem.isGranted()`/`.canShowSystemPrompt()` all return false, and every `.requestPermission()`/`.openAppSettings()` on either performs no action
- After `bind(activity, sensorLauncher, connectivityLauncher, prefs)`, `sensorPermissionSystem`'s four operations each match a directly-constructed `SensorPermissionSystemImpl(activity, sensorLauncher, prefs)` for the same inputs, and `connectivityPermissionSystem`'s four operations independently match a directly-constructed `ConnectivityPermissionSystemImpl(activity, connectivityLauncher, prefs)` — resolving one does not resolve or affect the other
- After `unbind()`, both `sensorPermissionSystem` and `connectivityPermissionSystem` return to the before-`bind` behaviour, even though the previously bound `Activity` is still reachable in memory
- `onSensorPermissionResult(granted)` resolves only a pending `sensorPermissionSystem.requestPermission()` suspension, never a pending `connectivityPermissionSystem` one, and conversely for `onConnectivityPermissionResult`; either call while unbound, or after `unbind()`, has no effect
- `confirmMarking()` requests one 50ms vibration pulse from the wrapped `Vibrator`
- `cancelMarking()` requests two 30ms vibration pulses separated by an 80ms gap from the wrapped `Vibrator`
- On a `Vibrator` reporting `hasVibrator() == false`, neither `confirmMarking()` nor `cancelMarking()` makes any request to it
- `HyroxWearApplication` is declared as the `android:name` of `:app-wear`'s `<application>` in `AndroidManifest.xml`, and `MainActivity` is declared there as the launcher activity

## Dependencies

WatchRaceNavigator, WatchDestination — pre-existing, `WatchDestination` unchanged
WatchHistoryScreen, ControlScreen, PreparationScreen, ProjectionScreen, EndOfRaceScreen, HomeScreen, WaitingForPhoneScreen, MainRacePageScreen, SensorPermissionScreen — pre-existing, unchanged (lot-14)
HomeViewModel, ControlViewModel, EndOfRaceViewModel, PreparationViewModel, WatchHistoryViewModel, ProjectionViewModel, WaitingForPhoneViewModel, MainRacePageViewModel, SensorPermissionViewModel — pre-existing, `@HiltViewModel` (lot-13)
HapticFeedback — pre-existing (`app-wear/src/main/java/com/mgilli/app_wear/race/HapticFeedback.kt`), interface unchanged
SegmentMarkingController — pre-existing, unchanged; its `haptics: HapticFeedback` constructor parameter is what needs a production binding
SensorPermissionSystem, ConnectivityPermissionSystem — pre-existing (`:core-domain`/`:app-wear`)
SensorPermissionSystemImpl (lot-18), ConnectivityPermissionSystemImpl (app-wear, lot-20) — pre-existing, constructed by `ActivityBoundPermissionHost.bind`
SensorPermissionLaunchStoreImpl, ConnectivityPermissionLaunchStoreImpl (app-wear) — pre-existing (lot-03)
RaceRecordingRepository, RaceRecordingRepositoryImpl — pre-existing (`:core-domain`/`app-wear`)
RaceLaunchController, UndoMarkingController, StopRaceController, ExerciseSessionManager — pre-existing (`app-wear/src/main/java/com/mgilli/app_wear/race`, `.../sensor/session`)
ExerciseSessionSystem, ExerciseSessionSystemImpl — pre-existing (lot-07)
RaceRepository, ProfileRepository, RaceRepositoryImpl, ProfileRepositoryImpl, HyroxDatabase, RaceDao, ProfileDao — pre-existing (lot-01)
WatchHistoryStore, WatchHistoryStoreImpl, WatchHistoryDatabase, RaceHistoryDao — pre-existing (lot-02)
WearableRecordedRaceTransport, WearableLinkStateSource, LinkStateMonitor, RecordedRaceTransport — pre-existing (lot-09)
RecordedRaceSyncService, SensorPermissionManager, ConnectivityPermissionManager — pre-existing (`:core-domain`/`app-wear`)
Clock, SystemClock — pre-existing (`:core-domain`)
HealthConnectClient/HealthServices, ExerciseClient — framework (`androidx.health.services.client`, already a dependency of `:app-wear` since lot-07)
android.os.Vibrator, android.os.VibrationEffect — framework, no new dependency (`android.os` is part of the Android SDK)
Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose, lifecycle-runtime-compose, hilt-navigation-compose (`creationCallback`, `collectAsStateWithLifecycle`) — added to `:app-wear` by lot-21, per its own blocked_detailleur.md decision for this lot (WatchRaceNavigator.current as a StateFlow, collected through collectAsStateWithLifecycle)
androidx.activity:activity-compose, Wear Compose Material/Foundation — pre-existing (lot-14)

## Conventions

§1 · Hilt is the sole DI mechanism; ViewModel + StateFlow drive state — no other framework
§2 · each application module carries its own entry point: an `Application` class for injection, a `MainActivity` hosting the root composable, both declared in its manifest
§2 · `:app-phone` and `:app-wear` share the same `applicationId` and signing key
§3 · anything touching the device's OS lives in the application module using it — `ActivityBoundPermissionHost`, `HapticFeedbackImpl` and every `*SystemImpl`/`*LaunchStoreImpl` stay in `:app-wear`
§3 · `:app-phone` and `:app-wear` never import each other
§3 · a platform adapter lives in the module carrying its technology — Room stays in `:core-data`, the Data Layer in `:core-sync`; only the database/transport instance is opened by `:app-wear`
§5 · nothing syncs mid-race; the watch is autonomous once the race starts
§6 · one exercise session per race, opened at preparation, closed at race end — `ExerciseSessionManager` unchanged, only wired here
§9 · identifiers and comments in English
§11 · a `*ViewModel` extends `androidx.lifecycle.ViewModel` and runs in `viewModelScope` — unaffected by this lot, already true since lot-13
§13 · never swallow an exception silently
§14 · `JAVA_HOME` set before any Gradle command; one verification command per module (`./gradlew :app-wear:check`); Compose UI tests live in `src/test` under Robolectric, `androidTest` is never used
