## Symbols

RaceRepositoryImpl
  in-memory only (LinkedHashMap, no persistence) — gap: Room-backed reads and writes   §2.1

ProfileRepositoryImpl
  in-memory only (MutableStateFlow, no persistence) — gap: Room-backed reads and writes   §2.1

RaceEntity, RaceDao, ProfileEntity, ProfileDao, HyroxDatabase — piece
  do not exist — carry RaceRepositoryImpl's and ProfileRepositoryImpl's persistence, exported schema   §2.1

SensorPermissionLaunchStore
  interface only, no implementation — gap: SharedPreferences-backed implementation in :app-wear   §2.2

ConnectivityPermissionLaunchStore
  interface only, no implementation — gap: SharedPreferences-backed implementation, separately in :app-wear and :app-phone   §2.2

SensorPermissionLaunchStoreImpl (app-wear), ConnectivityPermissionLaunchStoreImpl (app-wear), ConnectivityPermissionLaunchStoreImpl (app-phone) — piece
  do not exist — carry the first-launch flag each store should persist   §2.2

WatchHistoryStore
  interface only, no implementation — gap: Room-backed implementation in :core-data, replaceAll persists as a whole block, observe re-emits on every replaceAll   §2.3

RaceHistoryEntryEntity, RaceHistoryDao, WatchHistoryDatabase — piece
  do not exist — carry WatchHistoryStoreImpl's persistence   §2.3

Segment.cumulativeMs
  stored field, computed once when the 30 segments are built — gap: remove the field, derive on read   §3.1

SegmentBuilder
  sets cumulativeMs when constructing a Segment — gap: stop computing and storing it   §3.1

RaceDetailViewModel.buildRow
  reads segment.cumulativeMs — gap: call the new derivation function instead   §3.1

RaceRecordingRepositoryImplTest (app-wear)
  asserts on segment.cumulativeMs — gap: assert on Segment's current shape   §3.1

ExerciseSessionSystem
  interface only, test fakes only — gap: implementation wrapping Health Services' ExerciseClient   §5.1

ExerciseSessionSystemImpl — piece
  does not exist — carries availableDataTypes, startExerciseSession, endExerciseSession, setDataDeliveryMode against Health Services   §5.1

HrHistoryReader
  interface only, test fakes only — gap: implementation reading Health Connect   §5.2

HrHistoryReaderImpl — piece
  does not exist — carries bpmValuesOverLast12Months against the Health Connect client   §5.2

ProfileSyncTransport
  interface only, no implementation — gap: implementation on the Wearable Data Layer   §6.1

RecordedRaceTransport
  interface only, no implementation — gap: implementation on the Wearable Data Layer   §6.1

LinkStateMonitor
  exists, constructed with rawLinkEstablished: Flow<Boolean> — gap: nothing feeds that parameter in production   §6.1

WearableProfileSyncTransport, WearableRecordedRaceTransport, WearableLinkStateSource — piece
  do not exist — carry ProfileSyncTransport.send, RecordedRaceTransport.send and the node-connection signal feeding LinkStateMonitor   §6.1

MainActivity (app-phone)
  exists, renders the Android Studio template Greeting — gap: renders the composable matching PhoneNavigator.current, is the launcher, is @AndroidEntryPoint   §9.1, §9.2

MainActivity (app-wear)
  does not exist — gap: new, renders the composable matching WatchRaceNavigator.current, is the launcher, is @AndroidEntryPoint   §9.1, §9.2

HyroxTrackerApplication (app-phone) — piece
  does not exist — carries Hilt's application graph, declared in the phone manifest   §9.1, §9.4

HyroxWearApplication (app-wear) — piece
  does not exist — carries Hilt's application graph, declared in the wear manifest   §9.1, §9.4

ActivityBoundPermissionHost (app-phone) — piece
  does not exist — bridges ConnectivityPermissionSystem from an Activity-scoped implementation to the Singleton scope Hilt resolves ViewModels against, bound by MainActivity's onCreate/onDestroy   §9.1

ActivityBoundPermissionHost (app-wear) — piece
  does not exist — bridges SensorPermissionSystem and ConnectivityPermissionSystem from Activity-scoped implementations to the Singleton scope Hilt resolves ViewModels against, bound by MainActivity's onCreate/onDestroy   §9.1

app-wear/build.gradle.kts
  no androidx.activity:activity-compose, no Wear Compose entries — gap: both added   §9.3, §9.5

WatchHistoryScreen, ControlScreen, PreparationScreen, ProjectionScreen, EndOfRaceScreen, HomeScreen, WaitingForPhoneScreen, MainRacePageScreen, SensorPermissionScreen
  lay out with Column or LazyColumn — gap: draw from androidx.wear.compose.material.* and ScalingLazyColumn   §9.5

HomeViewModel, RaceDetailViewModel, RaceListViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel, PasteResultViewModel, ControlViewModel, EndOfRaceViewModel, PreparationViewModel, WatchHistoryViewModel, ProjectionViewModel, WaitingForPhoneViewModel, MainRacePageViewModel, SensorPermissionViewModel
  plain Kotlin classes with a manually-managed CoroutineScope — gap: extend androidx.lifecycle.ViewModel, use viewModelScope, @HiltViewModel with @Inject on the constructor   §9.4, §12.1

ExampleInstrumentedTest
  unmodified Android Studio template test — gap: deleted, its androidTest-only dependencies removed from app-phone/build.gradle.kts   §9.6

PhoneStringResources
  Kotlin const vals, interpolation via string templates — gap: moved into app-phone's strings.xml, French only, %1$s/%1$d parameters   §10.1

WatchStringResources
  Kotlin const vals, interpolation via string templates — gap: moved into app-wear's strings.xml, French only, %1$s/%1$d parameters   §10.1

SensorPermissionSystem
  interface only, test fakes only — gap: implementation wrapping the body-sensors runtime permission (ContextCompat, ActivityResultContracts, settings intent)   §11.1

SensorPermissionSystemImpl — piece
  does not exist — carries isGranted, canShowSystemPrompt, requestPermission, openAppSettings against the Android SDK   §11.1

ConnectivityPermissionSystem
  interface only, test fakes only, no OS permission decided — gap: implementation per application module, backed by a decided OS permission   §11.2

ConnectivityPermissionSystemImpl (app-phone), ConnectivityPermissionSystemImpl (app-wear) — piece
  do not exist — carry isGranted, canShowSystemPrompt, requestPermission, openAppSettings against the chosen OS permission   §11.2

HapticFeedback
  interface only, no implementation — gap: implementation
  wrapping the platform Vibrator   §9.4

HapticFeedbackImpl — piece
  does not exist — carries confirmMarking and cancelMarking
  against the platform Vibrator   §9.4

## §1 Model

No entries — no lot.

## §4 Transition

No entries — no lot.

## §7 Background work

No entries — no lot.

## §8 Journey

No entries — no lot.

## lot-01

Anchor: §2.1 — Race and profile data lost on restart
Needs: RaceRepository, ProfileRepository (pre-existing, interfaces unchanged)
Produces: RaceEntity, RaceDao, ProfileEntity, ProfileDao, HyroxDatabase (constructed by app-phone's and app-wear's DI wiring, lot-10 and lot-12)
Modifies: RaceRepositoryImpl, ProfileRepositoryImpl, core-data/build.gradle.kts (Room dependencies and annotation-processing plugin), version catalogue (Room and its plugin)

## lot-02

Anchor: §2.3 — Watch history never persisted
Needs: WatchHistoryStore (pre-existing), Room dependency and plugin in :core-data (produced by lot-01)
Produces: RaceHistoryEntryEntity, RaceHistoryDao, WatchHistoryDatabase, WatchHistoryStoreImpl (constructed by app-wear's DI wiring, lot-12)
Modifies: —

## lot-03

Anchor: §2.2 — First-launch flags never persisted
Needs: SensorPermissionLaunchStore, ConnectivityPermissionLaunchStore (pre-existing, interfaces unchanged)
Produces: SensorPermissionLaunchStoreImpl (app-wear), ConnectivityPermissionLaunchStoreImpl (app-wear) (both constructed by app-wear's DI wiring, lot-12)
Modifies: —

## lot-04

Anchor: §2.2 — First-launch flags never persisted
Needs: ConnectivityPermissionLaunchStore (pre-existing, interface unchanged)
Produces: ConnectivityPermissionLaunchStoreImpl (app-phone) (constructed by app-phone's DI wiring, lot-10)
Modifies: —

## lot-05

Anchor: §3.1 — Cumulative duration stored instead of derived
Needs: —
Produces: a cumulative-duration derivation function in :core-domain
Modifies: Segment, SegmentBuilder, RaceDetailViewModel, RaceRecordingRepositoryImplTest (app-wear)

## lot-07

Anchor: §5.1 — No real exercise session on the watch
Needs: ExerciseSessionSystem (pre-existing, interface unchanged)
Produces: ExerciseSessionSystemImpl (constructed by app-wear's DI wiring, lot-12)
Modifies: app-wear/build.gradle.kts (Health Services SDK dependency), version catalogue (Health Services SDK)

## lot-08

Anchor: §5.2 — No real heart-rate history on the phone
Needs: HrHistoryReader (pre-existing, interface unchanged)
Produces: HrHistoryReaderImpl (constructed by app-phone's DI wiring, lot-10)
Modifies: app-phone/build.gradle.kts (Health Connect client dependency), version catalogue (Health Connect client)

## lot-09

Anchor: §6.1 — No real link between phone and watch
Needs: ProfileSyncTransport, RecordedRaceTransport, LinkStateMonitor (pre-existing, interfaces and constructor unchanged)
Produces: WearableProfileSyncTransport, WearableRecordedRaceTransport, WearableLinkStateSource (all constructed by app-phone's and app-wear's DI wiring, lot-10 and lot-12)
Modifies: core-sync/build.gradle.kts (play-services-wearable dependency)

## lot-10

Anchor: §9.1 — No working application entry point; §9.2 — No root composable dispatching on the current destination; §9.4 — Nothing constructs the ViewModels
Needs: PhoneNavigator, PhoneDestination (pre-existing), RaceListScreen, RaceDetailScreen, ProfileScreen, ImportPreviewScreen, PasteErrorScreen, PasteResultScreen (pre-existing), RaceDetailViewModel, RaceListViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel, PasteResultViewModel (produced @HiltViewModel by lot-11), Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose (produced by lot-21), ConnectivityPermissionLaunchStoreImpl (app-phone, lot-04), HrHistoryReaderImpl (lot-08), ConnectivityPermissionSystemImpl (app-phone, lot-19), WearableProfileSyncTransport, WearableLinkStateSource (lot-09), HyroxDatabase (lot-01)
Produces: HyroxTrackerApplication (mounted by the Android OS), ActivityBoundPermissionHost (app-phone, lié par MainActivity)
Modifies: MainActivity (app-phone), AndroidManifest.xml (app-phone), app-phone/build.gradle.kts (play-services-wearable dependency), PhoneNavigator

## lot-11

Anchor: §9.4 — Nothing constructs the ViewModels; §12.1 — ViewModel classes not retained across configuration change
Needs: Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose (produced by lot-21)
Produces: —
Modifies: RaceDetailViewModel, RaceListViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel, PasteResultViewModel

## lot-12

Anchor: §9.1 — No working application entry point; §9.2 — No root composable dispatching on the current destination; §9.4 — Nothing constructs the ViewModels
Needs: WatchRaceNavigator, WatchDestination (pre-existing), WatchHistoryScreen, ControlScreen, PreparationScreen, ProjectionScreen, EndOfRaceScreen, HomeScreen, WaitingForPhoneScreen, MainRacePageScreen, SensorPermissionScreen (pre-existing, converted by lot-14), HomeViewModel, ControlViewModel, EndOfRaceViewModel, PreparationViewModel, WatchHistoryViewModel, ProjectionViewModel, WaitingForPhoneViewModel, MainRacePageViewModel, SensorPermissionViewModel (produced @HiltViewModel by lot-13), Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose (produced by lot-21), androidx.activity:activity-compose dependency (lot-14), WatchHistoryStoreImpl (lot-02), SensorPermissionLaunchStoreImpl, ConnectivityPermissionLaunchStoreImpl (app-wear, lot-03), ExerciseSessionSystemImpl (lot-07), SensorPermissionSystemImpl (lot-18), ConnectivityPermissionSystemImpl (app-wear, lot-20), WearableRecordedRaceTransport, WearableLinkStateSource (lot-09), HyroxDatabase (lot-01)
Produces: HyroxWearApplication, MainActivity (app-wear) (both mounted by the Android OS), ActivityBoundPermissionHost (app-wear, lié par MainActivity), HapticFeedbackImpl (app-wear, wrapping the platform Vibrator)
Modifies: AndroidManifest.xml (app-wear), WatchRaceNavigator

## lot-13

Anchor: §9.4 — Nothing constructs the ViewModels; §12.1 — ViewModel classes not retained across configuration change
Needs: Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose (produced by lot-21)
Produces: —
Modifies: HomeViewModel, ControlViewModel, EndOfRaceViewModel, PreparationViewModel, WatchHistoryViewModel, ProjectionViewModel, WaitingForPhoneViewModel, MainRacePageViewModel, SensorPermissionViewModel

## lot-14

Anchor: §9.3 — activity-compose missing from app-wear; §9.5 — Watch screens built with mobile Compose
Needs: —
Produces: androidx.activity:activity-compose dependency in :app-wear (needed by lot-12), Wear Compose Material and Foundation dependency in :app-wear
Modifies: app-wear/build.gradle.kts, version catalogue (Wear Compose Material, Wear Compose Foundation), WatchHistoryScreen, ControlScreen, PreparationScreen, ProjectionScreen, EndOfRaceScreen, HomeScreen, WaitingForPhoneScreen, MainRacePageScreen, SensorPermissionScreen

## lot-15

Anchor: §9.6 — Unused instrumented test template
Needs: —
Produces: —
Modifies: ExampleInstrumentedTest (deleted), app-phone/build.gradle.kts (androidx.test.ext.junit and androidx.espresso.core removed)

## lot-16

Anchor: §10.1 — User-facing strings not in resource files
Needs: —
Produces: —
Modifies: PhoneStringResources, and every call site reading its constants, app-phone/res/values/strings.xml

## lot-17

Anchor: §10.1 — User-facing strings not in resource files
Needs: —
Produces: —
Modifies: WatchStringResources, and every call site reading its constants, app-wear/res/values/strings.xml

## lot-18

Anchor: §11.1 — No real sensor permission implementation
Needs: SensorPermissionSystem (pre-existing, interface unchanged)
Produces: SensorPermissionSystemImpl (constructed by app-wear's DI wiring, lot-12)
Modifies: —

## lot-19

Anchor: §11.2 — No real connectivity permission implementation
Needs: ConnectivityPermissionSystem (pre-existing, interface unchanged)
Produces: ConnectivityPermissionSystemImpl (app-phone) (constructed by app-phone's DI wiring, lot-10)
Modifies: —

## lot-20

Anchor: §11.2 — No real connectivity permission implementation
Needs: ConnectivityPermissionSystem (pre-existing, interface unchanged)
Produces: ConnectivityPermissionSystemImpl (app-wear) (constructed by app-wear's DI wiring, lot-12)
Modifies: —

## lot-21

Anchor: §9.1 — No working application entry point; §9.4 — Nothing constructs the ViewModels; §12.1 — ViewModel classes not retained across configuration change
Needs: —
Produces: Hilt, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose, lifecycle-runtime-compose dependency in :app-phone and :app-wear (needed by lot-10, lot-11, lot-12, lot-13)
Modifies: app-phone/build.gradle.kts (Hilt and its plugin, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose, lifecycle-runtime-compose), app-wear/build.gradle.kts (Hilt and its plugin, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose, lifecycle-runtime-compose), version catalogue (Hilt and its plugin, lifecycle-viewmodel-ktx, lifecycle-viewmodel-compose, lifecycle-runtime-compose)
