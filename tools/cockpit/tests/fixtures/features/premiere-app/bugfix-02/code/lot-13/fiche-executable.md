## Signatures

    HomeViewModel — @HiltViewModel, extends androidx.lifecycle.ViewModel, runs in viewModelScope (replaces its manually-managed CoroutineScope)
      @Inject constructor(
        raceRepository: RaceRepository,
        profileRepository: ProfileRepository,
        recordedRaceSyncService: RecordedRaceSyncService,
        connectivityPermissionManager: ConnectivityPermissionManager,
        navigator: WatchRaceNavigator,
        linkStateMonitor: LinkStateMonitor,
        sensorPermissionManager: SensorPermissionManager,
        clock: Clock
      )
      — `clock` replaces the `now: () -> Instant = Instant::now` parameter, with no default.
        The link-established push (`recordedRaceSyncService.sync(raceInProgress = false, at = now())`)
        reads `clock.now()` instead.

    ControlViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @AssistedInject constructor(
        @Assisted initialRace: Race, undoMarkingController: UndoMarkingController,
        stopRaceController: StopRaceController, navigator: WatchRaceNavigator
      )

      interface Factory — @AssistedFactory
        create(initialRace: Race) → ControlViewModel

    EndOfRaceViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @AssistedInject constructor(
        @Assisted finalRace: Race, @Assisted referenceRace: Race?,
        exerciseSessionManager: ExerciseSessionManager, profileRepository: ProfileRepository,
        navigator: WatchRaceNavigator
      )

      interface Factory — @AssistedFactory
        create(finalRace: Race, referenceRace: Race?) → EndOfRaceViewModel

    PreparationViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(
        raceLaunchController: RaceLaunchController, raceRepository: RaceRepository, navigator: WatchRaceNavigator
      )
      — no per-navigation value; all three collaborators resolve from the Hilt graph.

    WatchHistoryViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(watchHistoryStore: WatchHistoryStore)

    ProjectionViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @AssistedInject constructor(
        @Assisted initialRace: Race, @Assisted referenceRace: Race?, @Assisted profile: Profile,
        markingController: SegmentMarkingController, navigator: WatchRaceNavigator
      )

      interface Factory — @AssistedFactory
        create(initialRace: Race, referenceRace: Race?, profile: Profile) → ProjectionViewModel

    WaitingForPhoneViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(profileRepository: ProfileRepository)

    MainRacePageViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @AssistedInject constructor(
        @Assisted initialRace: Race, @Assisted referenceRace: Race?, @Assisted profile: Profile,
        @Assisted sensorPermissionGranted: Boolean, markingController: SegmentMarkingController,
        navigator: WatchRaceNavigator
      )

      interface Factory — @AssistedFactory
        create(initialRace: Race, referenceRace: Race?, profile: Profile, sensorPermissionGranted: Boolean) → MainRacePageViewModel

    SensorPermissionViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(sensorPermissionManager: SensorPermissionManager)

## Acceptance criteria

- HomeViewModel, ControlViewModel, EndOfRaceViewModel, PreparationViewModel, WatchHistoryViewModel, ProjectionViewModel, WaitingForPhoneViewModel, MainRacePageViewModel and SensorPermissionViewModel each extend `androidx.lifecycle.ViewModel`
- `ControlViewModel.Factory.create(initialRace)`, called with a race mid-segment, returns a `ControlViewModel` whose `uiState.undoLabel`/`undoEnabled` match that race's current segment
- `EndOfRaceViewModel.Factory.create(finalRace, referenceRace)`, called with a finished race and a non-null reference, returns an `EndOfRaceViewModel` whose `uiState.totalTime`/`finalDeltaText`/`finalDeltaTone` are derived from those two races
- `EndOfRaceViewModel.Factory.create(finalRace, referenceRace = null)` returns an `EndOfRaceViewModel` whose `uiState.finalDeltaText` and `finalDeltaTone` are both null
- `ProjectionViewModel.Factory.create(initialRace, referenceRace, profile)`, called with a race, a non-null reference and a profile, returns a `ProjectionViewModel` whose `uiState.cumulativeDelta`/`estimatedArrival` are computed from those three
- `MainRacePageViewModel.Factory.create(initialRace, referenceRace, profile, sensorPermissionGranted = false)` returns a `MainRacePageViewModel` whose `uiState.heartRateText`/`zone` stay null after a heart-rate reading is delivered to it
- `MainRacePageViewModel.Factory.create(initialRace, referenceRace, profile, sensorPermissionGranted = true)` returns a `MainRacePageViewModel` whose `uiState.heartRateText`/`zone` reflect a fresh heart-rate reading delivered to it
- `HomeViewModel` built with a given `Clock` calls `RecordedRaceSyncService.sync` with that `Clock`'s `now()` when the watch link becomes established

## Dependencies

Race, Profile — pre-existing (:core-domain)
RaceRepository, ProfileRepository, WatchHistoryStore, RecordedRaceSyncService, ConnectivityPermissionManager — pre-existing (:core-domain)
LinkStateMonitor — pre-existing (:core-sync)
UndoMarkingController, StopRaceController, SegmentMarkingController, RaceLaunchController, ExerciseSessionManager, SensorPermissionManager, WatchRaceNavigator — pre-existing (:app-wear)
Clock — produced by lot-11, per the same Decision (`code/lot-11/blocked_detailleur.md`)
androidx.hilt:hilt-navigation-compose — already added to the catalogue and to `:app-wear` by lot-21 (amended, already coded); the `creationCallback` consuming the four `@AssistedFactory` types is a call-site concern for lot-12, not this lot

## Conventions

§3 · `:core-domain` never imports anything from Android — `Race`/`Profile` stay non-`Parcelable`; the per-navigation values reach the four affected ViewModels through `@AssistedInject`/`@AssistedFactory`, not a `SavedStateHandle`
§9 · identifiers and comments in English
§11 · a `*ViewModel` extends `androidx.lifecycle.ViewModel` and runs its work in `viewModelScope`
§11 · one `StateFlow` per screen, holding a single immutable UI state class — unchanged by this lot
