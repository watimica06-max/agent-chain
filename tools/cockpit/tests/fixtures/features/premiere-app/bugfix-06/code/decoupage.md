## Symbols

HyresultResultParser
  skips the export header and the closing "Total time" row      §1.1
  reads diff and cumulative from the real column layout         §1.1
  reads a duration with or without hours                        §1.1
  buildExpectedLabels drops its `!!` on stationAt               §2.5

SegmentBlueprint
  stationAt/typeAt pairing asserted by a test                   §2.5

SegmentBuilder
  buildSegments rejects a negative duration as null             §1.3
  cumulativeDurationMs returns null on a missing index          §3.4

CumulativeDeltaEstimator
  estimate finds the current segment without throwing           §3.1
  estimate/finalDelta reject a duplicate index                  §3.4

PaceCalculator
  segmentPace/smoothedPace return Fallback on a zero or
  negative factor or speed                                      §3.2
  smoothedPace's own window filter rejects a negative age       §3.3

LapDeltaCalculator
  compute returns Fallback on a zero or negative speed          §3.2

SensorFreshnessWindow
  evaluate rejects a negative age as stale                      §3.3

HeartRateZoneCalculator
  determine/ranges return null on a zero or negative hrMaxBpm,
  a non-increasing or wrongly-sized zoneThresholds              §3.5

DisplayFormatter
  formatMinutesSeconds/formatDurationTotal extract the sign     §9.7
  formatDateRelative distinguishes an instant after now         §9.9

HyroxTypeConverters
  toRaceOrigin/toRaceCompletion/toZoneThresholds fall back      §2.3

HyroxDatabase, RaceDatabaseMigrations
  a migration adding a unique index on sourceRaceId             §2.10
  version bump alongside it                                     §2.10
  MIGRATION_3_4 adds Race.stoppedAt, version bumped to 4        §1.4

RaceEntity
  sourceRaceId carries a unique index                           §2.10
  stoppedAt column mirrors the migration                        §1.4

RepositoryModule (:app-phone), RepositoryModule (:app-wear)
  provideHyroxDatabase guards a migration failure               §2.3
  both register MIGRATION_3_4 via addMigrations                 §1.4
  :app-wear binds RaceRecordingRepositoryImpl with RaceDao      §2.6

RaceDao
  a query finding a race with an open segment                   §2.7
  one transaction for the dedup lookup and the write            §2.10
  one transaction clearing the flag and writing the reference   §2.11
  one transaction writing and reading the row back              §2.12
  insertSegments refuses an index already stored                §3.4

RaceRepository, RaceRepositoryImpl
  saveImportedRace/saveRecordedRace trim and refuse a name      §1.5
  every method suspend, DAO calls on Dispatchers.IO,
  observeAll/observeReference carry flowOn                      §2.1
  persist surfaces an absent row as a failure                   §2.5, §2.12
  replaceReference propagates persist's outcome                 §2.12
  saveRecordedRace carries retainedFactors and
  rejectedCalibrations                                          §6.11
  boundary failures returned as values, flows guarded           §7.2

RaceQueryFailure
  the type RaceRepository's guarded flows emit on a failure,
  declared by :core-domain (lot-55), read by lot-31's
  RaceRepositoryImpl and by lot-56's five collectors            §7.2

ProfileRepositoryImpl
  boundary failures returned as values, observe() guarded       §7.2

RaceRecordingRepository, RaceRecordingRepositoryImpl
  stopRace reads atInstant and persists it on Race.stoppedAt    §1.4
  every method suspend, replacing the runBlocking profile read  §2.1
  no lock held across a suspension, findInProgress never waits  §2.2
  markSegment catches anything raised in its body               §2.4
  startClock/markSegment/undoLastMark/stopRace/markSent write
  the race before returning; findInProgress reads the database  §2.6, §2.7
  publishRecorded orders on an explicit id key                  §2.8
  the identifier startClock assigns survives the process        §2.9
  undoLastMark looks the closed segment up without throwing     §3.1
  boundary failures returned as values                          §7.2

ProfileSyncPushService
  applyProfile writes the five fields as one atomic call        §2.13
  applyIncoming determines raceInProgress itself                §6.8
  the two markSyncSuccess calls act on their Result             §9.4

ProfileSyncListenerService
  its applyIncoming call drops the stale boolean                §6.8
  its decode call moves inside serviceScope.launch              §6.2
  its findInProgress call moves inside serviceScope.launch      §2.2
  onMessageReceived catches its own read's failure              §6.3
  boundary failure returned as a value                          §7.2
  onDestroy cancels serviceScope                                §12.1

RecordedRaceListenerService
  the database write dispatches onto the IO scope               §6.1
  its decode call moves inside serviceScope.launch              §6.2
  onMessageReceived catches its own read's failure              §6.3
  derives the phone's correctionFactor from retainedFactors     §6.11
  boundary failure returned as a value                          §7.2
  onDestroy cancels serviceScope                                §12.1

RecordedRaceAckListenerService
  its own CoroutineScope                                        §6.1
  its decode call moves inside that scope                       §6.2
  onMessageReceived catches its own read's failure              §6.3

RecordedRaceSyncService, RecordedRaceSyncState
  sync checks markSent's Result and stops on failure            §6.4
  Failure carries the raceId it stopped on                      §6.4
  sync builds the payload from the race's retainedFactors and
  rejectedCalibrations — the only production construction of
  RecordedRacePayload, and the site that fills the two fields   §6.11

PayloadCodec
  SegmentSnapshot.toSegment rejects a negative durationMs       §1.3
  encode and the two decodes run on the IO dispatcher           §6.2
  each of the eight snapshot classes fixes serialVersionUID     §6.7
  RecordedRacePayloadSnapshot carries retainedFactors and
  rejectedCalibrations                                          §6.11
  toObject turns a cast mismatch into a decoding failure        §9.5

RecordedRacePayload
  carries retainedFactors and rejectedCalibrations              §6.11
  its two constructions follow — RecordedRaceSyncService.sync
  and PayloadCodec's RecordedRacePayloadSnapshot.toPayload      §6.11

PayloadDecodingFailure
  the type PayloadCodec returns on a decode it cannot
  complete, declared by :core-sync                              §9.5, §6.3, §7.2

DataLayerMessageChannel, WearableProfileSyncTransport,
WearableRecordedRaceTransport, WearableRecordedRaceAckTransport
  each rethrows CancellationException before its own catch      §6.5
  each logs what it caught                                      §6.6
  the encode call moves out of the send try                     §6.6
  MessageChannel.send's documentation follows                   §6.5

HrHistoryReaderImpl
  logs what it caught                                           §6.6
  its binding accommodates an absent HealthConnectClient        §5.2

WearableLinkStateSource, DataLayerCapabilitySource
  addLocalCapability awaited, out of init                       §5.1

ConnectivityPermissionSystemImpl
  compiled once, in a module both applications depend on        §11.1

ExerciseSessionSystem, ExerciseSessionSystemImpl
  endExerciseSession/setDataDeliveryMode suspend and awaited    §5.1
  an outcome variant for OWNED_EXERCISE_IN_PROGRESS             §5.4

ExerciseSessionManager
  close() awaits what it ends                                   §5.1
  registers for the available data types once open              §5.3
  adopts an already-running session, closes an orphaned one     §5.4

SensorReadingsSource — piece
  registers a MeasureCallback and forwards heart-rate,
  distance and speed samples                                    §5.3

RaceTicker
  a periodic tick independent of sensor delivery                §5.3

SegmentMarkingController, UndoMarkingController, StopRaceController
  onPressEnd and its siblings become suspend                    §2.2
  stop launches before awaiting close()                         §5.1

RaceLaunchController
  openPreparation reconciles an OS-level owned session          §5.4

WatchRaceComplicationDataSourceService
  onComplicationRequest gets its own coroutine scope            §2.2

WatchRaceNavigator, NavigationModule
  a method leaving WAITING_FOR_PHONE for HOME                   §4.1
  the sync condition re-evaluated, never read by blocking       §4.2
  the first destination accounts for a race in progress         §4.3
  checkInactivity treats the boundary instant as within         §4.5

MainActivity (:app-wear)
  onCreate reads the complication destination extra             §4.4
  manifest entry carries android:launchMode="singleTop"         §4.4
  onEnterAmbient/onExitAmbient call onInteractivityChanged      §5.5

WatchApp
  findInProgress and isGranted read once per branch entry       §9.2
  the suspend findInProgress collected with produceState        §2.2
  passes displayMode and refreshIntervalMs on                   §9.6

AlwaysOnDisplayController
  becomes a Hilt singleton                                      §9.6

MainRacePageScreen, MainRacePageViewModel, MainRacePageUiState
  the sixteen-call-site fix on its own handlers                 §7.1
  receives readings, samples and ticks                          §5.3
  renders its power-save layout                                 §9.6
  a "shown but dimmed" state distinct from fresh or absent      §9.11
  takes a SavedStateHandle                                      §12.2

ProjectionViewModel
  its call sites run inside viewModelScope.launch               §7.1
  takes a SavedStateHandle                                      §12.2

ControlViewModel
  its call sites run inside viewModelScope.launch               §7.1
  onUndoClicked/onStopConfirmed act on their Result             §9.4
  takes a SavedStateHandle                                      §12.2

PreparationViewModel, PreparationScreen
  its call sites run inside viewModelScope.launch               §7.1
  onHeartRateReading reached from the readings stream           §5.3
  onLaunchClicked acts on its Result                            §9.4
  takes a SavedStateHandle                                      §12.2
  the referenceLoaded label, second of the two reference-race
  labels, is bounded                                            §9.8

EndOfRaceViewModel
  computeState rejects a duplicate index                        §3.4
  init launches before awaiting close()                         §5.1
  its constructor-time read runs inside a scope                 §7.1

HomeViewModel, HomeScreen
  toHomeSyncUiState reads a Failure that now carries a raceId,
  and the screen shows the race the sync stopped on             §6.4
  both sync calls derive raceInProgress from findInProgress     §6.9
  RaceRecordingRepository injected                              §6.9
  its call sites run inside viewModelScope.launch               §7.1
  the referenceLine label, first of the two reference-race
  labels, is bounded                                            §9.8

WatchHistoryScreen, WatchHistoryViewModel
  the history's race names are bounded                          §9.8

SensorPermissionViewModel, SensorPermissionUiState
  its call sites run inside viewModelScope.launch               §7.1
  resolvedState dropped                                         §9.1

WaitingForPhoneViewModel, WaitingForPhoneUiState,
WaitingForPhoneScreen
  calls the navigator once the profile carries a sync date      §4.1
  hasReceivedProfile dropped                                    §9.1

WatchStringResources
  rejection texts for launch, undo and stop                     §9.4

PhoneStringResources
  rejection texts for import-save, delete and rename            §9.4
  a key naming the one-to-forty character bound                 §10.1

ProfileScreen, ProfileViewModel, ProfileUiState
  a state for "heart-rate history unavailable"                  §5.2
  the four setting handlers run inside viewModelScope.launch    §7.1
  distanceLabel and pressDurationLabel dropped                  §9.1
  its exhaustive when follows formatDateRelative                §9.9
  takes a SavedStateHandle                                      §12.2
  in-progress field values held in rememberSaveable             §12.4

RaceDetailScreen, RaceDetailViewModel, RaceDetailUiState,
SegmentRowUiState
  buildRow shows the glyph on a null cumulative                 §3.4
  pushes after each write succeeds                              §6.10
  ProfileSyncPushService and Clock injected                     §6.10
  its call sites run inside viewModelScope.launch               §7.1
  raceId and index dropped                                      §9.1
  buildRow looks a segment up without assuming it is present    §9.3
  onDeleteConfirmed/onRenameConfirmed act on their Result       §9.4
  the title and the delete confirmation are bounded             §9.8
  the delta column names its calculation, or shows nothing      §9.10
  a refused rename keeps the dialog open with its message       §10.1
  takes a SavedStateHandle                                      §12.2

ImportPreviewScreen, ImportPreviewViewModel, ImportPreviewUiState
  onSaveClicked reacts to saveImportedRace's failure            §1.5
  pushes after the write succeeds                               §6.10
  ProfileSyncPushService and Clock injected                     §6.10
  its call site runs inside viewModelScope.launch               §7.1
  onSaveClicked acts on its Result                              §9.4
  takes a SavedStateHandle                                      §12.2

PasteResultScreen, PasteResultViewModel, PasteResultUiState
  isImportEnabled tests for blankness                           §1.5
  its call sites run inside viewModelScope.launch               §7.1
  takes a SavedStateHandle                                      §12.2

PasteErrorViewModel
  takes a SavedStateHandle                                      §12.2

RaceListScreen, RaceListViewModel
  the row's name is bounded and weighted                        §9.8

PhoneNavigator
  the back stack written to and restored from a saved state     §12.3

PhoneNavigationStateStore — piece
  keeps the back stack across a process death                   §12.3

PhoneApp
  its three casts are guarded                                   §9.5

MainActivity (:app-phone), PlatformModule
  provideHealthConnectClient checks getSdkStatus first          §5.2
  the injected client becomes optional                          §5.2

HapticFeedbackImpl
  tolerates an absent system service                            §9.5

PhoneRaceRecordingRepository, RaceRecordingModule (:app-phone) — piece
  lets ProfileSyncPushService reach findInProgress on the phone §6.8
  fulfils the interface once its methods become suspend         §2.1, §2.2

Already carried, nothing to build:

ProfileRepository, ProfileRepositoryImpl, ProfileDao, WatchHistoryStore,
WatchHistoryStoreImpl
  updateCorrectionFactor already validates against 0.70..1.40   §1.2
  every method already suspend, already on Dispatchers.IO,
  observe() already carries flowOn, ProfileDao.upsert already
  suspend, WatchHistoryStoreImpl.replaceAll already suspend     §2.1
  applyIncomingProfile and ProfileDao.applyIncoming already
  write the five fields in one transaction                      §2.13

## lot-01

Anchor: §1.1 — The paste parser misreads the real Hyresult export; §2.5 — Two force-unwraps rest on invariants nothing enforces
Needs: SegmentBlueprint (pre-existing), Station (pre-existing), HyresultParseResult (pre-existing)
Produces: —
Modifies: HyresultResultParser, HyresultResultParserTest, SegmentBlueprintTest

## lot-02

Anchor: §1.3 — A negative segment duration is stored and displayed as-is; §3.4 — A missing or duplicate segment index corrupts a cumulative total
Needs: Segment (pre-existing), SegmentBlueprint (pre-existing)
Produces: —
Modifies: SegmentBuilder, SegmentBuilderTest

## lot-03

Anchor: §3.1 — Two segment lookups assume an index that may not exist; §3.4 — A missing or duplicate segment index corrupts a cumulative total
Needs: Segment (pre-existing), CumulativeDeltaResult (pre-existing)
Produces: —
Modifies: CumulativeDeltaEstimator, CumulativeDeltaEstimatorTest

## lot-04

Anchor: §3.2 — A correction factor or a speed of zero makes pace, delta and trend meaningless; §3.3 — Two freshness windows treat a future reading as fresh
Needs: PaceResult (pre-existing), LapDeltaResult (pre-existing), SpeedSample (pre-existing)
Produces: —
Modifies: PaceCalculator, LapDeltaCalculator, PaceCalculatorTest, LapDeltaCalculatorTest

## lot-05

Anchor: §3.3 — Two freshness windows treat a future reading as fresh
Needs: Freshness (pre-existing)
Produces: —
Modifies: SensorFreshnessWindow, FreshnessTest

## lot-06

Anchor: §3.5 — `HeartRateZoneCalculator` trusts a profile it never checks
Needs: Profile (pre-existing), HeartRateZone (pre-existing)
Produces: —
Modifies: HeartRateZoneCalculator, HeartRateZoneRange, HeartRateZoneCalculatorTest

## lot-07

Anchor: §9.7 — `DisplayFormatter` garbles every negative duration; §9.9 — A sync timestamp in the future reads as older than it is
Needs: DateDisplay (pre-existing)
Produces: —
Modifies: DisplayFormatter, DateDisplay, DisplayFormatterTest

## lot-08

Anchor: §2.3 — Room reads raise on data they wrote themselves; §2.10 — The recorded-race dedup check and write are not atomic
Needs: RaceOrigin (pre-existing), RaceCompletion (pre-existing), Room (pre-existing)
Produces: a new Room migration (applied by Room when the database opens)
Modifies: HyroxTypeConverters, HyroxDatabase, RaceDatabaseMigrations, RaceEntity, RepositoryModule (:app-phone), RepositoryModule (:app-wear), HyroxTypeConvertersTest

## lot-09

Anchor: §2.7 — Resuming a preparation depends on state that never survives a process death; §2.10 — The recorded-race dedup check and write are not atomic; §2.11 — Replacing the reference race exposes a moment with no reference at all; §2.12 — `persist` force-unwraps a row it has just written; §3.4 — A missing or duplicate segment index corrupts a cumulative total
Needs: RaceEntity (lot-08), SegmentEntity (pre-existing), the unique index on sourceRaceId (lot-08)
Produces: —
Modifies: RaceDao, RaceDaoTest

## lot-10

Anchor: §7.2 — Nothing in the project turns a boundary failure into a value
Needs: ProfileDao (pre-existing)
Produces: —
Modifies: ProfileRepositoryImpl, ProfileRepositoryImplTest

## lot-11

Anchor: §1.3 — A negative segment duration is stored and displayed as-is; §6.2 — `PayloadCodec` runs serialization on whatever thread calls it; §6.7 — The eight serialized snapshot classes declare no version id; §6.11 — A watch-computed correction factor is undone by the next sync; §9.5 — Five unchecked casts can fail on their own paths
Needs: RecordedRacePayload carrying retainedFactors (lot-53), PayloadDecodingFailure (lot-52), ProfileSyncPayload (pre-existing), SegmentBuilder (lot-02), RecordedRaceListenerService (lot-31), RecordedRaceAckListenerService (lot-32), ProfileSyncListenerService (lot-16), WearableProfileSyncTransport (lot-12), WearableRecordedRaceTransport (lot-12)
Produces: —
Modifies: PayloadCodec, PayloadCodecTest

## lot-12

Anchor: §6.5 — Cancellation is swallowed as a send failure; §6.6 — Five catch sites swallow their exception without a trace
Needs: MessageChannel (pre-existing), android.util.Log (pre-existing)
Produces: —
Modifies: MessageChannel, DataLayerMessageChannel, WearableProfileSyncTransport, WearableRecordedRaceTransport, WearableRecordedRaceAckTransport, and their tests

## lot-13

Anchor: §5.1 — Four system calls are made and their outcome never read
Needs: CapabilitySource (pre-existing), Play Services Wearable (pre-existing)
Produces: —
Modifies: WearableLinkStateSource, DataLayerCapabilitySource, WearableLinkStateSourceTest

## lot-14

Anchor: §11.1 — The connectivity permission implementation is duplicated per module
Needs: ConnectivityPermissionSystem (pre-existing), :core-platform (lot-54)
Produces: ConnectivityPermissionSystemImpl in :core-platform (constructed by both applications' ActivityBoundPermissionHost)
Modifies: ConnectivityPermissionSystemImpl (:app-phone, removed), ConnectivityPermissionSystemImpl (:app-wear, removed), ActivityBoundPermissionHost (:app-phone), ActivityBoundPermissionHost (:app-wear), ConnectivityModule (:app-phone), PermissionModule (:app-wear), and their tests

## lot-15

Anchor: §6.4 — A failed acknowledgement is never checked; §6.11 — A watch-computed correction factor is undone by the next sync
Needs: RaceRecordingRepository (pre-existing), RecordedRaceTransport (pre-existing), RecordedRaceAckListenerService (lot-32), RecordedRacePayload carrying retainedFactors (lot-53)
Produces: —
Modifies: RecordedRaceSyncService, RecordedRaceSyncState, RecordedRaceSyncServiceTest

## lot-16

Anchor: §2.2 — Marking a segment blocks and holds a lock across a suspension; §2.13 — Applying an incoming profile can silently lose a local edit; §6.2 — `PayloadCodec` runs serialization on whatever thread calls it; §6.3 — A malformed message from the paired device crashes the other one; §6.8 — A push refused because a race is running can still let one through; §7.2 — Nothing in the project turns a boundary failure into a value; §9.4 — Seven call sites drop a `Result` their caller should act on; §12.1 — A listener service's coroutine scope outlives the service
Needs: ProfileRepository.applyIncomingProfile (pre-existing), PhoneRaceRecordingRepository (lot-30), PayloadDecodingFailure (lot-52)
Produces: —
Modifies: ProfileSyncPushService, ProfileSyncListenerService, SyncModule (:app-wear), SyncModule (:app-phone), FakeSyncModule (:app-wear test), ProfileSyncPushServiceTest, ProfileSyncListenerServiceTest

## lot-17

Anchor: §9.4 — Seven call sites drop a `Result` their caller should act on; §10.1 — A bound violation shows a constraint message that does not exist
Needs: PhoneStringResources (pre-existing)
Produces: —
Modifies: PhoneStringResources, PhoneStringResourcesTest

## lot-18

Anchor: §9.4 — Seven call sites drop a `Result` their caller should act on
Needs: WatchStringResources (pre-existing)
Produces: —
Modifies: WatchStringResources, WatchStringResourcesTest

## lot-19

Anchor: §5.2 — The phone crashes at launch on a device without Health Connect; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.1 — Six UI-state fields are written and read nowhere; §9.9 — A sync timestamp in the future reads as older than it is; §12.2 — Fourteen ViewModel fields are lost on rotation; §12.4 — A field being edited is lost on rotation before the user saves
Needs: ProfileRepository (pre-existing), ProfileSyncPushService (lot-16), DateDisplay (lot-07), PhoneStringResources (lot-17), SavedStateHandle (pre-existing)
Produces: —
Modifies: ProfileViewModel, ProfileUiState, ProfileScreen, ProfileViewModelTest, ProfileScreenTest

## lot-20

Anchor: §3.4 — A missing or duplicate segment index corrupts a cumulative total; §6.10 — Nothing on the phone pushes when something changes; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.1 — Six UI-state fields are written and read nowhere; §9.3 — Opening a race detail crashes on any incomplete race; §9.4 — Seven call sites drop a `Result` their caller should act on; §9.8 — No text is bounded on screen; §9.10 — The lap-delta column shows a value no calculation covers; §10.1 — A bound violation shows a constraint message that does not exist; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: RaceRepository (pre-existing), SegmentBuilder (lot-02), ProfileSyncPushService (lot-16), PhoneStringResources (lot-17), Clock (pre-existing), SavedStateHandle (pre-existing)
Produces: —
Modifies: RaceDetailViewModel, RaceDetailUiState, SegmentRowUiState, RaceDetailScreen, RaceDetailViewModelTest, RaceDetailScreenTest

## lot-21

Anchor: §1.5 — A race name is validated on rename alone; §6.10 — Nothing on the phone pushes when something changes; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.4 — Seven call sites drop a `Result` their caller should act on; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: RaceRepository (pre-existing), ProfileSyncPushService (lot-16), PhoneStringResources (lot-17), Clock (pre-existing), SavedStateHandle (pre-existing)
Produces: —
Modifies: ImportPreviewViewModel, ImportPreviewUiState, ImportPreviewScreen, ImportPreviewViewModelTest, ImportPreviewScreenTest

## lot-22

Anchor: §1.5 — A race name is validated on rename alone; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: HyresultResultParser (lot-01), SavedStateHandle (pre-existing)
Produces: —
Modifies: PasteResultViewModel, PasteResultUiState, PasteResultScreen, PasteResultViewModelTest

## lot-23

Anchor: §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: SavedStateHandle (pre-existing)
Produces: —
Modifies: PasteErrorViewModel, PasteErrorUiState, PasteErrorViewModelTest

## lot-24

Anchor: §9.8 — No text is bounded on screen
Needs: RaceRepository (pre-existing)
Produces: —
Modifies: RaceListScreen, RaceListViewModel, RaceListScreenTest

## lot-25

Anchor: §12.3 — The phone's navigation stack does not survive a process death
Needs: PhoneDestination (pre-existing), PhoneNavigationStateStore (lot-26)
Produces: —
Modifies: PhoneNavigator, PhoneDestination, PhoneNavigatorTest

## lot-26

Anchor: §12.3 — The phone's navigation stack does not survive a process death
Needs: Context (pre-existing)
Produces: PhoneNavigationStateStore (called by lot-25)
Modifies: —

## lot-27

Anchor: §9.5 — Five unchecked casts can fail on their own paths
Needs: HyresultParseResult (pre-existing), PasteResultViewModel (lot-22)
Produces: —
Modifies: PhoneApp, MainActivityTest (:app-phone)

## lot-28

Anchor: §5.2 — The phone crashes at launch on a device without Health Connect; §6.6 — Five catch sites swallow their exception without a trace
Needs: Health Connect Client (pre-existing), android.util.Log (pre-existing), ProfileUiState (lot-19)
Produces: —
Modifies: PlatformModule, MainActivity (:app-phone), ActivityBoundHrPermissionHost, HrPermissionSystemImpl, HrHistoryReaderImpl, HrHistoryReaderImplTest

## lot-30

Anchor: §6.8 — A push refused because a race is running can still let one through
Needs: RaceRecordingRepository (pre-existing), Hilt (pre-existing)
Produces: PhoneRaceRecordingRepository and RaceRecordingModule (:app-phone) binding it (injected into ProfileSyncPushService, lot-16)
Modifies: —

## lot-31

Anchor: §1.5 — A race name is validated on rename alone; §2.1 — Four repositories reach the database synchronously; §2.5 — Two force-unwraps rest on invariants nothing enforces; §2.12 — `persist` force-unwraps a row it has just written; §6.1 — The recorded-race listeners write to the database on the binder thread; §6.2 — `PayloadCodec` runs serialization on whatever thread calls it; §6.3 — A malformed message from the paired device crashes the other one; §6.11 — A watch-computed correction factor is undone by the next sync; §7.2 — Nothing in the project turns a boundary failure into a value; §12.1 — A listener service's coroutine scope outlives the service
Needs: RaceDao (lot-09), RecordedRacePayload carrying retainedFactors (lot-53), ProfileRepository (pre-existing), android.util.Log (pre-existing), RaceDetailViewModel (lot-20), ImportPreviewViewModel (lot-21), RaceListViewModel (lot-24), ProfileSyncPushService (lot-16), RaceQueryFailure (lot-55)
Produces: RaceRepository's guarded flows carrying RaceQueryFailure (read by lot-56)
Modifies: RaceRepository, RaceRepositoryImpl, RaceRepositoryImplTest, RecordedRaceListenerService, RecordedRaceListenerServiceTest

## lot-32

Anchor: §6.1 — The recorded-race listeners write to the database on the binder thread; §6.2 — `PayloadCodec` runs serialization on whatever thread calls it; §6.3 — A malformed message from the paired device crashes the other one
Needs: RecordedRaceSyncService (pre-existing), android.util.Log (pre-existing)
Produces: —
Modifies: RecordedRaceAckListenerService, RecordedRaceAckListenerServiceTest

## lot-33

Anchor: §4.1 — The waiting-for-phone screen never gives way; §9.1 — Six UI-state fields are written and read nowhere
Needs: ProfileRepository (pre-existing), WatchRaceNavigator (lot-34)
Produces: —
Modifies: WaitingForPhoneViewModel, WaitingForPhoneUiState, WaitingForPhoneScreen, WaitingForPhoneViewModelTest

## lot-34

Anchor: §4.1 — The waiting-for-phone screen never gives way; §4.2 — Every cold start blocks on the database before the first frame; §4.3 — Nothing routes back to a race in progress at start-up; §4.5 — The inactivity timeout expires at the exact boundary every freshness window treats as valid
Needs: RaceRecordingRepository.findInProgress (pre-existing), ProfileRepository (pre-existing), WatchDestination (pre-existing)
Produces: —
Modifies: WatchRaceNavigator, NavigationModule, WatchRaceNavigatorTest

## lot-35

Anchor: §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.1 — Six UI-state fields are written and read nowhere
Needs: SensorPermissionManager (pre-existing), WatchRaceNavigator (lot-34)
Produces: —
Modifies: SensorPermissionViewModel, SensorPermissionUiState, SensorPermissionScreen, SensorPermissionViewModelTest

## lot-36

Anchor: §6.4 — A failed acknowledgement is never checked; §6.9 — `RecordedRaceSyncService.sync` is called with a hardcoded race-in-progress state; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.8 — No text is bounded on screen
Needs: RaceRecordingRepository (pre-existing), RecordedRaceSyncService (pre-existing), RecordedRaceSyncState.Failure carrying the raceId (lot-15)
Produces: —
Modifies: HomeViewModel, HomeUiState, HomeSyncUiState, HomeScreen, HomeViewModelTest

## lot-37

Anchor: §9.8 — No text is bounded on screen
Needs: WatchHistoryStore (pre-existing)
Produces: —
Modifies: WatchHistoryScreen, WatchHistoryViewModel, WatchHistoryScreenTest

## lot-38

Anchor: §5.3 — The watch never receives a single sensor reading; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.4 — Seven call sites drop a `Result` their caller should act on; §9.8 — No text is bounded on screen; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: RaceLaunchController (lot-44), SensorReadingsSource (lot-46), WatchStringResources (lot-18), SavedStateHandle (pre-existing)
Produces: —
Modifies: PreparationViewModel, PreparationUiState, PreparationScreen, PreparationViewModelTest, PreparationScreenTest

## lot-39

Anchor: §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: RaceRecordingRepository (pre-existing), CumulativeDeltaEstimator (lot-03), SavedStateHandle (pre-existing)
Produces: —
Modifies: ProjectionViewModel, ProjectionUiState, ProjectionScreen, ProjectionViewModelTest

## lot-40

Anchor: §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.4 — Seven call sites drop a `Result` their caller should act on; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: UndoMarkingController (lot-43), StopRaceController (lot-43), WatchStringResources (lot-18), SavedStateHandle (pre-existing)
Produces: —
Modifies: ControlViewModel, ControlUiState, ControlScreen, ControlViewModelTest

## lot-41

Anchor: §5.3 — The watch never receives a single sensor reading; §7.1 — Sixteen call sites reach a repository or service outside a coroutine; §9.6 — Ambient mode is computed and thrown away; §9.11 — Every sensor value hits its freshness boundary on every power-save refresh; §12.2 — Fourteen ViewModel fields are lost on rotation
Needs: SensorReadingsSource (lot-46), RaceTicker (lot-47), DisplayMode (pre-existing), PaceCalculator (lot-04), SensorFreshnessWindow (lot-05), HeartRateZoneCalculator (lot-06), SegmentMarkingController (lot-43), SavedStateHandle (pre-existing)
Produces: —
Modifies: MainRacePageViewModel, MainRacePageUiState, MainRacePageScreen, MainRacePageViewModelTest, MainRacePageScreenTest

## lot-42

Anchor: §3.4 — A missing or duplicate segment index corrupts a cumulative total; §5.1 — Four system calls are made and their outcome never read; §7.1 — Sixteen call sites reach a repository or service outside a coroutine
Needs: ExerciseSessionManager (lot-45), ProfileRepository (pre-existing), CumulativeDeltaEstimator (lot-03)
Produces: —
Modifies: EndOfRaceViewModel, EndOfRaceUiState, EndOfRaceScreen, EndOfRaceViewModelTest

## lot-43

Anchor: §2.2 — Marking a segment blocks and holds a lock across a suspension; §5.1 — Four system calls are made and their outcome never read
Needs: RaceRecordingRepository (pre-existing), ExerciseSessionManager (lot-45), HapticFeedback (pre-existing)
Produces: —
Modifies: SegmentMarkingController, UndoMarkingController, StopRaceController, and their tests

## lot-44

Anchor: §5.4 — A session this application already owns is opened a second time after process death
Needs: ExerciseSessionManager (lot-45), RaceRecordingRepository (pre-existing), PreparationState (pre-existing)
Produces: —
Modifies: RaceLaunchController, PreparationState, RaceLaunchControllerTest

## lot-45

Anchor: §5.1 — Four system calls are made and their outcome never read; §5.3 — The watch never receives a single sensor reading; §5.4 — A session this application already owns is opened a second time after process death
Needs: SensorReadingsSource (lot-46), RaceTicker (lot-47), Health Services Client (pre-existing)
Produces: —
Modifies: ExerciseSessionSystem, ExerciseSessionSystemImpl, ExerciseSessionManager, ExerciseSessionStartOutcome, ExerciseSessionOpenResult, SensorModule, and their tests

## lot-46

Anchor: §5.3 — The watch never receives a single sensor reading
Needs: SensorDataType (pre-existing), Health Services Client (pre-existing)
Produces: SensorReadingsSource (registered by lot-45, collected by lot-38 and lot-41)
Modifies: —

## lot-47

Anchor: §5.3 — The watch never receives a single sensor reading
Needs: Clock (pre-existing), kotlinx.coroutines (pre-existing)
Produces: RaceTicker (started by lot-45, collected by lot-41)
Modifies: —

## lot-48

Anchor: §2.2 — Marking a segment blocks and holds a lock across a suspension
Needs: RaceRecordingRepository (pre-existing), kotlinx.coroutines (pre-existing)
Produces: —
Modifies: WatchRaceComplicationDataSourceService, WatchComplicationEntry, WatchRaceComplicationDataSourceServiceTest

## lot-49

Anchor: §2.2 — Marking a segment blocks and holds a lock across a suspension; §4.4 — Tapping the complication does nothing after a process death; §5.5 — The watch never switches its data-delivery mode; §9.2 — `WatchApp` reads a repository and a permission on every recomposition; §9.6 — Ambient mode is computed and thrown away
Needs: ExerciseSessionManager (lot-45), MainRacePageScreen (lot-41), WatchRaceNavigator (lot-34), RaceRecordingRepository (pre-existing), AmbientBinder (pre-existing)
Produces: —
Modifies: MainActivity (:app-wear), WatchApp, AlwaysOnDisplayController, DisplayModule, AndroidManifest.xml (:app-wear), MainActivityHomeAndRaceScreensTest, WatchRaceNavigator, WatchRaceNavigatorTest

## lot-50

Anchor: §1.4 — `stopRace` ignores the instant it is given; §2.1 — Four repositories reach the database synchronously; §2.2 — Marking a segment blocks and holds a lock across a suspension; §2.4 — `markSegment` lets an exception escape its own `Result` contract; §2.6 — A race in progress is not written down; §2.7 — Resuming a preparation depends on state that never survives a process death; §2.8 — A race imported on the same day as another can reorder silently; §2.9 — A race recorded after a process restart can be lost as a false duplicate; §3.1 — Two segment lookups assume an index that may not exist; §7.2 — Nothing in the project turns a boundary failure into a value
Needs: RaceDao (lot-09), SegmentBuilder (lot-02), CorrectionFactorCalculator (pre-existing), ProfileRepository (pre-existing), SegmentMarkingController (lot-43), UndoMarkingController (lot-43), StopRaceController (lot-43), RaceLaunchController (lot-44), WatchApp (lot-49), WatchRaceComplicationDataSourceService (lot-48), ProfileSyncListenerService (lot-16), RecordedRaceSyncService (lot-15), HomeViewModel (lot-36), ProjectionViewModel (lot-39), EndOfRaceViewModel (lot-42), MainRacePageViewModel (lot-41), WatchRaceNavigator (lot-34)
Produces: —
Modifies: RaceRecordingRepository, RaceRecordingRepositoryImpl, Race, RaceRecordingRepositoryImplTest, PhoneRaceRecordingRepository (built by lot-30), RaceEntity, HyroxDatabase, RaceDatabaseMigrations, RaceDatabaseMigrationsTest, RepositoryModule (:app-wear), RepositoryModule (:app-phone)

## lot-51

Anchor: §9.5 — Five unchecked casts can fail on their own paths
Needs: HapticFeedback (pre-existing), Vibrator (pre-existing)
Produces: —
Modifies: HapticFeedbackImpl, HapticFeedbackImplTest

## lot-52

Anchor: §9.5 — Five unchecked casts can fail on their own paths
Needs: :core-sync (pre-existing)
Produces: PayloadDecodingFailure (returned by PayloadCodec, lot-11; read by ProfileSyncListenerService, lot-16)
Modifies: —

## lot-53

Anchor: §6.11 — A watch-computed correction factor is undone by the next sync
Needs: RetainedFactor (pre-existing), RejectedCalibration (pre-existing)
Produces: —
Modifies: RecordedRacePayload

## lot-54

Anchor: §11.1 — The connectivity permission implementation is duplicated per module
Needs: androidx.activity (pre-existing), androidx.core (pre-existing)
Produces: :core-platform (a new Gradle module, depended on by :app-phone and :app-wear the same way each already depends on :core-sync; hosts ConnectivityPermissionSystemImpl, built by lot-14)
Modifies: settings.gradle.kts, app-phone/build.gradle.kts (:app-phone), app-wear/build.gradle.kts (:app-wear)

## lot-55

Anchor: §7.2 — Nothing in the project turns a boundary failure into a
value
Needs: —
Produces: RaceQueryFailure (read by lot-31 and lot-56)
Modifies: —

## lot-56

Anchor: §7.2 — Nothing in the project turns a boundary failure into a
value
Needs: RaceQueryFailure (lot-55), RaceRepository's guarded flows
       (lot-31)
Produces: —
Modifies: RaceListViewModel, RaceListViewModelTest, RaceListScreenTest, RaceDetailViewModel, RaceDetailViewModelTest, RaceDetailScreenTest (:app-phone); HomeViewModel, HomeViewModelTest, HomeScreenTest, PreparationViewModel, PreparationViewModelTest, PreparationScreenTest, MainActivity, ProfileSyncListenerServiceTest (:app-wear)

## Entries with no lot

§1.2 — already carried: `ProfileRepositoryImpl.updateCorrectionFactor` validates against 0.70..1.40 and refuses an out-of-range value, nothing left to build

## Conventions requests

architecte/cadreur.md — R12's module table naming `:core-platform`, not
`:core-sync`, as the module realising §11.1
