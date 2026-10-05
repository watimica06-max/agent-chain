## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

## §2 Persistence

### §2.1 Race and profile data lost on restart

Bearer: RaceRepositoryImpl, ProfileRepositoryImpl

RaceRepositoryImpl and ProfileRepositoryImpl hold every race and the
profile in memory, so a race in progress, an imported race and the
profile's correction factor are all lost on restart. Both read from
and write to a Room database instead, with a race entity, a profile
entity, their DAOs, a database declaring both and its exported schema
added to `:core-data`.

### §2.2 First-launch flags never persisted

Bearer: SensorPermissionLaunchStore, ConnectivityPermissionLaunchStore

SensorPermissionLaunchStore and ConnectivityPermissionLaunchStore are
interfaces only, with no implementation beyond test fakes, so the
first-launch flag each should persist is never saved. Each gets a
SharedPreferences-backed implementation: SensorPermissionLaunchStore
in `:app-wear`, and ConnectivityPermissionLaunchStore separately in
`:app-wear` and in `:app-phone`, since it is consumed from both
modules and `:core-domain` cannot hold Android-dependent code.

### §2.3 Watch history never persisted

Bearer: WatchHistoryStore

WatchHistoryStore is an interface only, with no implementation, so the
summarised history that ProfileSyncPushService.applyIncoming writes
and WatchHistoryViewModel reads is never actually stored. A Room-backed
implementation in `:core-data` persists the entries passed to
replaceAll as a whole block, replacing any previously stored set, and
re-emits the stored list through observe on every replaceAll call.

## §3 Calculation

### §3.1 Cumulative duration stored instead of derived

Bearer: Segment

Segment.cumulativeMs is a stored field, computed once when the 30
segments are built, so it can disagree with the sum of the durations
it is derived from. Segment carries only durationMs, and every
reader — starting with RaceDetailViewModel.buildRow — obtains the
cumulative value from a derivation function added to `:core-domain`
that recomputes it on read, in place of the stored field.

## §4 Transition

## §5 External source

### §5.1 No real exercise session on the watch

Bearer: ExerciseSessionSystem

ExerciseSessionSystem is an interface only, with no implementation
beyond test fakes, so ExerciseSessionManager is never built against a
real session and no exercise session ever runs on a real device. A
real implementation wraps Health Services' ExerciseClient — its
capabilities back availableDataTypes, startExerciseAsync and
endExerciseAsync back startExerciseSession and endExerciseSession, and
the exercise config's batching interval backs setDataDeliveryMode —
using the Health Services SDK added to the version catalogue and to
`:app-wear`'s dependencies, and something in `:app-wear`'s main source
constructs ExerciseSessionManager with it.

### §5.2 No real heart-rate history on the phone

Bearer: HrHistoryReader

HrHistoryReader is an interface only, with no implementation beyond
test fakes, so ProfileViewModel's call to bpmValuesOverLast12Months
never returns real data. A Health-Connect-backed implementation lives
in `:app-phone`, reading every heart-rate reading recorded over the
last twelve months through the Health Connect client, using the Health
Connect client added to the version catalogue and to `:app-phone`'s
dependencies.

## §6 Synchronisation

### §6.1 No real link between phone and watch

Bearer: ProfileSyncTransport, RecordedRaceTransport, LinkStateMonitor

ProfileSyncTransport and RecordedRaceTransport are interfaces with no
implementation, and nothing feeds LinkStateMonitor's rawLinkEstablished
flow, so ProfileSyncPushService.push, ProfileSyncPushService.applyIncoming,
RecordedRaceSyncService.sync and LinkStateMonitor.observeLinkEstablished
never run against a real device. `:core-sync` gains a
WearableProfileSyncTransport implementing ProfileSyncTransport.send and
a WearableRecordedRaceTransport implementing RecordedRaceTransport.send,
both built on the Wearable Data Layer, and a production Flow<Boolean>
built on the Data Layer's node-connection signal wired into
LinkStateMonitor's rawLinkEstablished parameter; `:core-sync` and
`:app-phone` both depend on play-services-wearable, which only
`:app-wear` declares today.

## §7 Background work

## §8 Journey

## §9 Screen

### §9.1 No working application entry point

Bearer: MainActivity (app-wear, new), MainActivity (app-phone, existing)

Neither application module has a working entry point: `:app-wear`'s
manifest declares no activity at all, and `:app-phone`'s MainActivity
renders the Android Studio template's Greeting instead of the
application. Each module gets an Application class wired for
dependency injection and declared in its manifest, and a MainActivity
declared as the launcher activity, whose onCreate renders the screen
matching its navigator's current destination; this requires Hilt added
to the version catalogue and to both build files, and
androidx.activity:activity-compose added to `:app-wear`'s build file.

### §9.2 No root composable dispatching on the current destination

Bearer: MainActivity

`:app-phone`'s MainActivity.onCreate renders a hardcoded Greeting
instead of reading PhoneNavigator.current, and `:app-wear` has no
MainActivity at all despite WatchRaceNavigator and WatchDestination
already carrying the full navigation rule, including the first-launch
choice among the permission, waiting-for-phone and home screens.
MainActivity on the phone renders the composable matching
PhoneNavigator.current, and a new MainActivity on the watch renders the
composable matching WatchRaceNavigator.current.

### §9.3 activity-compose missing from app-wear

Bearer: app-wear/build.gradle.kts

`app-wear/build.gradle.kts` declares no androidx.activity:activity-compose
dependency, so no ComponentActivity can be built in the module. It
declares implementation(libs.androidx.activity.compose), using the
alias already present in the version catalogue.

### §9.4 Nothing constructs the ViewModels

Bearer: HyroxTrackerApplication (app-phone, new), HyroxWearApplication (app-wear, new)

Every ViewModel takes its dependencies as plain constructor parameters,
and no factory, container or graph exists to build any of them, so no
production call site ever instantiates one. The version catalogue and
both application build files declare Hilt, each application module
gets an Application class annotated for Hilt, each ViewModel is
annotated @HiltViewModel with @Inject on its constructor and resolved
through hiltViewModel() at the call site, and each module's
MainActivity is @AndroidEntryPoint.

### §9.5 Watch screens built with mobile Compose

Bearer: app-wear/build.gradle.kts

`:app-wear` is built with mobile Compose: its build file depends on
androidx.compose.material3, and every watch screen (WatchHistoryScreen,
ControlScreen, PreparationScreen, ProjectionScreen, EndOfRaceScreen,
HomeScreen, WaitingForPhoneScreen, MainRacePageScreen,
SensorPermissionScreen) lays out with Column or LazyColumn instead of a
round-screen-aware container. The version catalogue carries a Wear
Compose entry (androidx.wear.compose:compose-material and
compose-foundation), `app-wear/build.gradle.kts` depends on it, and
each of the nine screens draws from androidx.wear.compose.material.*
and androidx.wear.compose.foundation.lazy.ScalingLazyColumn instead of
the mobile components.

### §9.6 Unused instrumented test template

Bearer: ExampleInstrumentedTest

`app-phone/src/androidTest/.../ExampleInstrumentedTest.kt` is the
unmodified Android Studio template test, and nothing in the project's
task graph runs an androidTest variant. The file is deleted, and the
androidTest-only dependencies it required (androidx.test.ext.junit,
androidx.espresso.core) are removed from `app-phone/build.gradle.kts`,
since nothing else in the module uses them.

## §10 Text

### §10.1 User-facing strings not in resource files

Bearer: PhoneStringResources, WatchStringResources

Every user-facing string lives as a const val inside
PhoneStringResources and WatchStringResources, with interpolated
values built as Kotlin string templates, while each module's
strings.xml holds only app_name. Every string moves into its module's
own strings.xml — French only — resolved through a resource id with
%1$s/%1$d-style parameters instead of a string template, separately
for `:app-phone` and `:app-wear` since each keeps its own resource
file and a key needed on both sides is duplicated rather than shared.

## §11 Access

### §11.1 No real sensor permission implementation

Bearer: SensorPermissionSystem

SensorPermissionSystem is an interface only, with no implementation
beyond test fakes, so SensorPermissionManager never drives a real
permission grant. A real implementation wraps the body-sensors runtime
permission through the Android SDK: isGranted reads the current grant
state with ContextCompat.checkSelfPermission, canShowSystemPrompt reads
shouldShowRequestPermissionRationale combined with whether the
permission has ever been requested, requestPermission launches
ActivityResultContracts.RequestPermission and suspends until the user
resolves it, and openAppSettings opens an intent to the app's
permissions page in the system settings.

### §11.2 No real connectivity permission implementation

Bearer: ConnectivityPermissionSystem

ConnectivityPermissionSystem is an interface only, with no
implementation beyond test fakes, and which OS permission it stands
for has never been decided, so ConnectivityPermissionManager never
drives a real permission grant on either device. Each application
module — `:app-phone` and `:app-wear` — gets its own implementation,
backed by a decided OS permission for reaching the paired device: the
choice of permission is part of this fix. isGranted reads the current
state of that permission with no prompt shown, canShowSystemPrompt
reports whether the OS will still show its own dialog for it,
requestPermission triggers that system dialog and suspends for the
resolution, and openAppSettings opens the app's own page in the system
settings.

## §12 Lifecycle

### §12.1 ViewModel classes not retained across configuration change

Bearer: HomeViewModel, RaceDetailViewModel, RaceListViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel, PasteResultViewModel, ControlViewModel, EndOfRaceViewModel, PreparationViewModel, WatchHistoryViewModel, ProjectionViewModel, WaitingForPhoneViewModel, MainRacePageViewModel, SensorPermissionViewModel

No class named `*ViewModel` extends androidx.lifecycle.ViewModel: each
is a plain Kotlin class holding its own manually-managed
CoroutineScope, so none is retained across a configuration change or
the watch waking, and a race in progress loses its state on rotation
or on wake. The version catalogue and both build files declare
lifecycle-viewmodel-ktx and lifecycle-viewmodel-compose, and each of
the fifteen classes listed above extends ViewModel and replaces its
manual CoroutineScope with viewModelScope.

## Gaps set aside

