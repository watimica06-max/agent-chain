## Signatures

    RaceDetailViewModel — @HiltViewModel, extends androidx.lifecycle.ViewModel, runs in viewModelScope (replaces its manually-managed CoroutineScope)
      @AssistedInject constructor(@Assisted raceId: Long, raceRepository: RaceRepository, navigator: PhoneNavigator)

      interface Factory — @AssistedFactory
        create(raceId: Long) → RaceDetailViewModel

    RaceListViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(raceRepository: RaceRepository, navigator: PhoneNavigator)

    ProfileViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(
        profileRepository: ProfileRepository,
        profileSyncPushService: ProfileSyncPushService,
        connectivityPermissionManager: ConnectivityPermissionManager,
        hrHistoryReader: HrHistoryReader,
        linkStateMonitor: LinkStateMonitor,
        clock: Clock
      )
      — `clock` replaces the `now: () -> Instant = Instant::now` parameter, with no default.
        Every `now()` call site (the link-established push, `syncStatusText`'s
        `DisplayFormatter.formatDateRelative`) reads `clock.now()` instead.

    ImportPreviewViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @AssistedInject constructor(
        @Assisted success: HyresultParseResult.Success, raceRepository: RaceRepository, navigator: PhoneNavigator
      )
      — replaces the `pasteResultViewModel: PasteResultViewModel` parameter; `success` is read
        once at construction, as `pasteResultViewModel.uiState.value.lastParseResult` was before.

      interface Factory — @AssistedFactory
        create(success: HyresultParseResult.Success) → ImportPreviewViewModel

      onSaveClicked(raceName: String, raceDate: LocalDate)
      — replaces the no-argument `onSaveClicked()`. Builds the imported race's start-of-day
        instant from `raceDate` and calls `raceRepository.saveImportedRace(raceName, startOfDay,
        buildSegments(success.segmentDurationsMs))` exactly as before; `raceName`/`raceDate` are
        no longer read from a `pasteResultViewModel` this class no longer holds — the caller
        supplies them.

    PasteErrorViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @AssistedInject constructor(@Assisted failure: HyresultParseResult.Failure, navigator: PhoneNavigator)
      — replaces the `pasteResultViewModel: PasteResultViewModel` parameter; `failure` is read
        once at construction, as `pasteResultViewModel.uiState.value.lastParseResult` was before.

      interface Factory — @AssistedFactory
        create(failure: HyresultParseResult.Failure) → PasteErrorViewModel

    PasteResultViewModel — @HiltViewModel, extends ViewModel, viewModelScope
      @Inject constructor(navigator: PhoneNavigator, clock: Clock)
      — `clock` replaces the `today: LocalDate = LocalDate.now()` parameter, with no default.
        `uiState`'s initial `raceDate`/`maxSelectableDate` are
        `LocalDate.ofInstant(clock.now(), ZoneId.systemDefault())`, evaluated once at
        construction — the same one-shot evaluation `today` gave before.

    Clock — new, :core-domain, package com.mgilli.core.domain.timing
      now(): Instant — the current instant

    SystemClock — new, :core-domain, package com.mgilli.core.domain.timing, implements Clock
      @Inject constructor()
      now(): Instant — `java.time.Instant.now()`

## Acceptance criteria

- RaceDetailViewModel, RaceListViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel and PasteResultViewModel each extend `androidx.lifecycle.ViewModel`
- `RaceDetailViewModel.Factory.create(raceId)`, called with the id of a stored race, returns a `RaceDetailViewModel` whose `uiState` carries that race's name, date, total and per-segment rows
- `ImportPreviewViewModel.Factory.create(success)`, called with a `HyresultParseResult.Success`, returns an `ImportPreviewViewModel` whose `uiState.totalTime` and `uiState.segmentsCount` are derived from that `success`'s `totalTimeMs` and `segmentDurationsMs`
- `ImportPreviewViewModel.onSaveClicked(raceName, raceDate)` saves a new race under the given `raceName` and `raceDate` and, on success, opens that race's detail screen
- `PasteErrorViewModel.Factory.create(failure)`, called with a `HyresultParseResult.Failure`, returns a `PasteErrorViewModel` whose `uiState.title`/`body`/`rawRow`/`expectedRow` match that `failure`'s cause
- `ProfileViewModel` built with a given `Clock` computes `syncStatusText`'s Today/Yesterday/Earlier relative display against that `Clock`'s `now()`, not against the real wall-clock time
- `ProfileViewModel` built with a given `Clock` pushes the profile with that `Clock`'s `now()` when the watch link becomes established
- `PasteResultViewModel` built with a given `Clock` initializes `uiState.raceDate` and `uiState.maxSelectableDate` to that `Clock`'s `now()`, converted to the system default zone's local date
- `SystemClock.now()` returns the current instant

## Dependencies

RaceRepository — pre-existing
ProfileRepository — pre-existing
PhoneNavigator — pre-existing
ProfileSyncPushService — pre-existing
ConnectivityPermissionManager — pre-existing
HrHistoryReader — pre-existing
LinkStateMonitor — pre-existing
HyresultParseResult.Success, HyresultParseResult.Failure — pre-existing (:core-domain)
Clock, SystemClock — produced by this lot, per the Decision (`decoupage.md`'s lot-11 entry said "Produces: —"; the Decision supersedes it on this point)
androidx.hilt:hilt-navigation-compose — already added to the catalogue and to `:app-phone` by lot-21 (amended, already coded); the `creationCallback` consuming the two `@AssistedFactory` types is a call-site concern for lot-10, not this lot

## Conventions

§3 · `:core-domain` never imports anything from Android — `Clock`/`SystemClock` use only `java.time.Instant`
§9 · identifiers and comments in English
§11 · a `*ViewModel` extends `androidx.lifecycle.ViewModel` and runs its work in `viewModelScope`
§11 · one `StateFlow` per screen, holding a single immutable UI state class — unchanged by this lot
