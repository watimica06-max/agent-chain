## Signatures

    // com.mgilli.hyroxtracker.ui.navigation
    @Singleton
    class PhoneNavigator @Inject constructor() {
      val current: StateFlow<PhoneDestination>
      // Was a plain `val current: PhoneDestination get() = backStack.last()`.
      // Every existing navigation method (toRaceDetail, toProfile,
      // toPasteResult, toImportPreview, toPasteError, backToPasteResult,
      // toRaceDetailAfterImport, back) keeps its own signature and the same
      // back-stack transitions; each one now also updates `current`'s value.
      // Initial value: PhoneDestination.RaceList, as the back stack's first
      // entry already was.
    }

    // com.mgilli.hyroxtracker — new
    @HiltAndroidApp
    class HyroxTrackerApplication : Application()

    // com.mgilli.hyroxtracker — modified
    @AndroidEntryPoint
    class MainActivity : ComponentActivity() {
      @Inject lateinit var navigator: PhoneNavigator
      @Inject lateinit var permissionHost: ActivityBoundPermissionHost

      // onCreate(savedInstanceState):
      // 1. registers an ActivityResultLauncher<String> on
      //    ActivityResultContracts.RequestPermission(), whose callback calls
      //    permissionHost.onPermissionResult(granted)
      // 2. permissionHost.bind(this, launcher, <a SharedPreferences instance>)
      // 3. enableEdgeToEdge()
      // 4. setContent { HyroxTrackerTheme { <dispatch below> } }
      //
      // Dispatch: collects `navigator.current` (collectAsStateWithLifecycle)
      // and renders, per PhoneDestination:
      //   RaceList        -> RaceListScreen(hiltViewModel())
      //   RaceDetail(id)   -> RaceDetailScreen(hiltViewModel(key = <distinct
      //                       per id>, creationCallback = { f: RaceDetailViewModel.Factory
      //                       -> f.create(id) }))
      //   Profile          -> ProfileScreen(hiltViewModel())
      //   PasteResult      -> PasteResultScreen(hiltViewModel())
      //   ImportPreview    -> reads pasteResultViewModel = hiltViewModel<PasteResultViewModel>()
      //                       (same instance already backing the PasteResult screen —
      //                       Activity-scoped ViewModelStore, no NavBackStackEntry
      //                       involved), then pasteResultViewModel.uiState.value
      //                       .lastParseResult as HyresultParseResult.Success, and
      //                       renders ImportPreviewScreen(hiltViewModel(creationCallback =
      //                       { f: ImportPreviewViewModel.Factory -> f.create(success) }),
      //                       raceName = pasteResultViewModel.uiState.value.raceName,
      //                       raceDate = pasteResultViewModel.uiState.value.raceDate)
      //   PasteError       -> same pasteResultViewModel read, lastParseResult as
      //                       HyresultParseResult.Failure, renders
      //                       PasteErrorScreen(hiltViewModel(creationCallback =
      //                       { f: PasteErrorViewModel.Factory -> f.create(failure) }))
      //
      // onDestroy(): permissionHost.unbind()
    }

    // com.mgilli.hyroxtracker.connectivity.permission — new, per Decision
    @Singleton
    class ActivityBoundPermissionHost @Inject constructor() : ConnectivityPermissionSystem {
      fun bind(activity: Activity, launcher: ActivityResultLauncher<String>, prefs: SharedPreferences)
      // Builds a new ConnectivityPermissionSystemImpl(activity, launcher, prefs)
      // and holds it as the current delegate, replacing any previous one.

      fun unbind()
      // Drops the current delegate. No Activity, launcher or SharedPreferences
      // reference is retained afterward.

      fun onPermissionResult(granted: Boolean)
      // Forwards to the currently bound delegate's onPermissionResult(granted).
      // No effect while unbound.

      override fun isGranted(): Boolean
      // Bound: delegate.isGranted(). Unbound: false.

      override fun canShowSystemPrompt(): Boolean
      // Bound: delegate.canShowSystemPrompt(). Unbound: false.

      override suspend fun requestPermission(): Boolean
      // Bound: delegate.requestPermission(), suspending the same way.
      // Unbound: false immediately, nothing launched.

      override fun openAppSettings()
      // Bound: delegate.openAppSettings(). Unbound: no-op.
    }

    // Hilt wiring implied by lot-10's declared Needs (no new project symbol —
    // each of the following is a binding the DI graph must supply so the
    // six @HiltViewModel/@AssistedFactory classes above construct):
    //   ConnectivityPermissionSystem -> the ActivityBoundPermissionHost singleton
    //   ConnectivityPermissionLaunchStore -> ConnectivityPermissionLaunchStoreImpl (app-phone, lot-04),
    //     built from a SharedPreferences instance
    //   HrHistoryReader -> HrHistoryReaderImpl(HealthConnectClient), the client
    //     built via HealthConnectClient.getOrCreate(context)
    //   RaceRepository -> RaceRepositoryImpl(HyroxDatabase(context).raceDao())
    //   ProfileRepository -> ProfileRepositoryImpl(HyroxDatabase(context).profileDao())
    //   ProfileSyncTransport -> WearableProfileSyncTransport(context)
    //   LinkStateMonitor -> built from WearableLinkStateSource(context).observeNodeConnected()
    //     as its rawLinkEstablished argument

## Acceptance criteria

- `PhoneNavigator.current` starts at `PhoneDestination.RaceList`
- After `toRaceDetail(id)`, `current.value` is `RaceDetail(id)`; after `back()`, it returns to `RaceList`
- After `toProfile()`, `toPasteResult()`, `toImportPreview()`, `toPasteError()`, `current.value` is `Profile`, `PasteResult`, `ImportPreview`, `PasteError` respectively
- MainActivity renders `RaceListScreen` when `navigator.current` is `RaceList`
- MainActivity renders `RaceDetailScreen` for the `raceId` carried by `RaceDetail(raceId)`; navigating from one race's detail to a different race's detail resolves a `RaceDetailViewModel` scoped to the new id, not the previous instance
- MainActivity renders `ProfileScreen` when `navigator.current` is `Profile`
- MainActivity renders `PasteResultScreen` when `navigator.current` is `PasteResult`
- MainActivity renders `ImportPreviewScreen` when `navigator.current` is `ImportPreview`, with `raceName`/`raceDate` and the `ImportPreviewViewModel`'s underlying `success` matching `PasteResultViewModel.uiState.value`'s `raceName`/`raceDate`/`lastParseResult`
- MainActivity renders `PasteErrorScreen` when `navigator.current` is `PasteError`, with the `PasteErrorViewModel`'s underlying `failure` matching `PasteResultViewModel.uiState.value.lastParseResult`
- MainActivity reaches the resumed state without throwing (the permission-result launcher is registered before `ActivityBoundPermissionHost.bind` is called, itself before the activity leaves the created state)
- Before any `bind`, `ActivityBoundPermissionHost.isGranted()` and `.canShowSystemPrompt()` return false, and `.requestPermission()`/`.openAppSettings()` perform no action
- After `bind(activity, launcher, prefs)`, `ActivityBoundPermissionHost.isGranted()`, `.canShowSystemPrompt()`, `.requestPermission()` and `.openAppSettings()` each match the outcome a directly-constructed `ConnectivityPermissionSystemImpl(activity, launcher, prefs)` would give for the same inputs
- After `unbind()`, `ActivityBoundPermissionHost.isGranted()`/`.canShowSystemPrompt()` return false again and `.requestPermission()`/`.openAppSettings()` no-op, even though the previously bound `Activity` is still reachable in memory
- Calling `onPermissionResult(granted)` while bound resolves the suspension started by that same delegate's `requestPermission()`; calling it while unbound, or after `unbind()`, has no effect
- `HyroxTrackerApplication` is declared as the `android:name` of `:app-phone`'s `<application>` in `AndroidManifest.xml`, and `MainActivity` is declared there as the launcher activity
- `app-phone/build.gradle.kts` declares the `play-services-wearable` dependency

## Dependencies

PhoneDestination — pre-existing, unchanged
RaceListScreen, RaceDetailScreen, ProfileScreen, ImportPreviewScreen, PasteErrorScreen, PasteResultScreen — pre-existing, unchanged
RaceListViewModel, RaceDetailViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel, PasteResultViewModel — pre-existing, @HiltViewModel (lot-11)
ConnectivityPermissionSystem, ConnectivityPermissionManager, ConnectivityPermissionLaunchStore — pre-existing (`:core-domain`)
ConnectivityPermissionSystemImpl (app-phone) — pre-existing (lot-19), constructed by `ActivityBoundPermissionHost.bind`
ConnectivityPermissionLaunchStoreImpl (app-phone) — pre-existing (lot-04)
HrHistoryReader, HrHistoryReaderImpl — pre-existing (lot-08)
HyroxDatabase, RaceDao, ProfileDao, RaceRepositoryImpl, ProfileRepositoryImpl, RaceRepository, ProfileRepository — pre-existing (lot-01)
WearableProfileSyncTransport, WearableLinkStateSource, LinkStateMonitor, ProfileSyncTransport — pre-existing (lot-09)
ProfileSyncPushService — pre-existing (`:core-domain`)
HealthConnectClient — framework (`androidx.health.connect.client`, already a dependency of `:app-phone`)
Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose, lifecycle-runtime-compose, hilt-navigation-compose (`creationCallback`, `collectAsStateWithLifecycle`) — added to `:app-phone` by lot-21, per its own blocked_detailleur.md decision for this lot (PhoneNavigator.current as a StateFlow, collected through collectAsStateWithLifecycle)
play-services-wearable — declared in the version catalogue, added to `app-phone/build.gradle.kts` by this lot (already a dependency of `:app-wear` and `:core-sync`)

## Conventions

§1 · Hilt is the sole DI mechanism; ViewModel + StateFlow drive state — no other framework
§2 · each application module carries its own entry point: an `Application` class for injection, a `MainActivity` hosting the root composable, both declared in its manifest
§3 · anything touching the device's OS lives in the application module using it — `ActivityBoundPermissionHost` and `ConnectivityPermissionSystemImpl` stay in `:app-phone`
§3 · `:app-phone` and `:app-wear` never import each other
§9 · identifiers and comments in English
§13 · never swallow an exception silently
§14 · `JAVA_HOME` set before any Gradle command; one verification command per module (`./gradlew :app-phone:check`); Compose UI tests live in `src/test` under Robolectric, `androidTest` is never used
