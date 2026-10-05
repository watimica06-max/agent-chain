## Signatures

HomeViewModel(
  raceRepository: RaceRepository,
  profileRepository: ProfileRepository,
  recordedRaceSyncService: RecordedRaceSyncService,
  connectivityPermissionManager: ConnectivityPermissionManager,
  navigator: WatchRaceNavigator,
  linkStateMonitor: LinkStateMonitor,
  sensorPermissionManager: SensorPermissionManager,
  raceRecordingRepository: RaceRecordingRepository,
  clock: Clock
) : ViewModel
  — `@HiltViewModel`, `@Inject` constructor. `raceRecordingRepository`
    is the one added parameter; the eight others keep their name and
    type. Nothing in the constructor or in a property initialiser calls
    a repository, a service or a manager.

HomeViewModel.onSyncClicked(at: Instant) → Unit
  — not suspend; returns immediately. Sets `syncState` to
    `HomeSyncUiState.InProgress` and recomputes as today, then inside
    `viewModelScope.launch` reads
    `raceRecordingRepository.findInProgress().getOrNull() != null` and
    passes that value as `RecordedRaceSyncService.sync`'s
    `raceInProgress`, never a hardcoded `false`. `at` is passed through
    unchanged. Exactly one `findInProgress` read and one `sync` call per
    invocation, the read immediately before the call. A failed
    `Result` from `findInProgress` reads as no race in progress —
    exactly what `ProfileSyncPushService.applyIncoming` already does
    with the same expression.

HomeViewModel.init — the link-established collector
  — on each emission of `LinkStateMonitor.observeLinkEstablished()`,
    inside the existing `viewModelScope.launch`: sets `syncState` to
    `HomeSyncUiState.InProgress`, recomputes, then reads
    `raceRecordingRepository.findInProgress().getOrNull() != null` and
    calls `recordedRaceSyncService.sync(raceInProgress = <that value>,
    at = clock.now())`. One read and one `sync` call per emission, the
    read immediately before the call; a failed `Result` reads as no race
    in progress, as above.

HomeViewModel.init — the sensor reminder read
  — `currentSensorPermissionReminderVisible` initialises to `false`, and
    a `viewModelScope.launch` in `init` sets it to
    `!sensorPermissionManager.isGranted()` and recomputes — the way
    `currentConnectivityPermissionReminderVisible` already defaults to
    `false` and is filled by `connectivityPermissionManager.onLaunch()`.
    No property initialiser calls `isGranted()`. `uiState`'s first value
    therefore carries `sensorPermissionReminderVisible = false`
    whatever the permission is worth, and `isGranted()` is called
    exactly once per instance.

HomeViewModel.toHomeSyncUiState(RecordedRaceSyncState?) → HomeSyncUiState
  — unchanged: `null` → `Idle`, `InProgress` → `InProgress`, `Success`
    → `Idle`, `Failure` → `Failure`. The `raceId` that
    `RecordedRaceSyncState.Failure` now carries is not read here; the
    branch stays an `is` check. Never null.

HomeSyncUiState
  — unchanged. `Idle`, `InProgress` and `Failure` stay three bare
    objects; `Failure` carries no property.

HomeUiState
  — unchanged. `syncState: HomeSyncUiState` keeps its type, and no
    field is added or removed.

HomeScreen(viewModel: HomeViewModel, onHistoryClicked: () -> Unit)
  — signature unchanged. The `Text` rendering
    `uiState.referenceLineText` takes `maxLines = 1` and
    `overflow = TextOverflow.Ellipsis` — the label is the one-line
    `home_reference_line` ("Réf. — %1$s"), sized like `:app-phone`'s
    race-list and detail-title names. Every other `Text` is untouched,
    and the `HomeSyncUiState.Failure` branch keeps its fixed
    `WatchStringResources.Sync.failure` line, with no race name and no
    race id.

## Acceptance criteria

- `onSyncClicked(at)` with `findInProgress()` returning a race calls
  `RecordedRaceSyncService.sync` once, with `raceInProgress = true` and
  `at` equal to the instant given.
- `onSyncClicked(at)` with `findInProgress()` returning
  `Result.success(null)` calls `sync` once, with
  `raceInProgress = false`.
- `onSyncClicked(at)` with `findInProgress()` returning a failed
  `Result` calls `sync` once, with `raceInProgress = false`.
- An emission of `observeLinkEstablished()` with `findInProgress()`
  returning a race calls `sync` once, with `raceInProgress = true` and
  `at` equal to `clock.now()`.
- An emission of `observeLinkEstablished()` with `findInProgress()`
  returning `Result.success(null)` calls `sync` once, with
  `raceInProgress = false`.
- Constructing `HomeViewModel` and letting every launched coroutine run,
  with no link emission and no sync tap, calls `findInProgress()` never.
- With `Dispatchers.Main` set to a paused test dispatcher, constructing
  `HomeViewModel` returns with `SensorPermissionManager.isGranted()` not
  yet called; once the dispatcher runs, it has been called exactly once.
- With that same paused dispatcher and a refused sensor permission,
  `uiState.value.sensorPermissionReminderVisible` is `false` immediately
  after construction, and `true` once the dispatcher runs.
- With a granted sensor permission,
  `uiState.value.sensorPermissionReminderVisible` is `false` both
  immediately after construction and once the dispatcher runs.
- With that same paused dispatcher, `onSyncClicked(at)` returns with
  `findInProgress()` and `sync` both not yet called, while
  `uiState.value.syncState` is already `HomeSyncUiState.InProgress`;
  once the dispatcher runs, each has been called exactly once.
- A `RecordedRaceSyncState.Failure(raceId)` emitted by
  `RecordedRaceSyncService.observe()` sets `uiState.value.syncState` to
  `HomeSyncUiState.Failure`, whatever the `raceId` is worth.
- `HomeSyncUiState.Failure` carries no property, and no file of
  `:app-wear` reads a `raceId` from `HomeSyncUiState`, tests included.
- `HomeScreen` composed on a state whose `syncState` is
  `HomeSyncUiState.Failure` displays the text of `sync_failure` and no
  other sync text; `app-wear/src/main/res/values/strings.xml` gains no
  key and `WatchStringResources` gains no member.
- `HomeScreen` composed with a reference race whose name is 40
  characters long renders the reference line at the same height as the
  same screen composed with a three-character name.
- `HomeScreen` composed with no reference race renders the text of
  `home_reference_line_empty`, on one line.

## Dependencies

RaceRecordingRepository.findInProgress(): Result<Race?> — pre-existing
  (`:core-domain`); not suspend at this lot's turn, and bound to Hilt in
  `:app-wear` by `RepositoryModule.provideRaceRecordingRepository`.
  lot-50 makes it suspend later and names `HomeViewModel` in its own
  Needs — this lot leaves the interface alone.
RecordedRaceSyncService.sync(raceInProgress: Boolean, at: Instant): Unit
  — suspend; `observe(): Flow<RecordedRaceSyncState?>`. Modified by
  lot-15 of this cycle, signature unchanged. Reused, never redeclared.
RecordedRaceSyncState — modified by lot-15 of this cycle:
  `Failure` is now `data class Failure(val raceId: Long)`, alongside
  `InProgress` and `Success`. Reused, never redeclared; its `raceId` is
  not read in this lot.
SensorPermissionManager.isGranted(): Boolean — pre-existing
  (`:app-wear`), not suspend
ConnectivityPermissionManager — pre-existing: `suspend onLaunch()`,
  `suspend requestAgain()`
LinkStateMonitor.observeLinkEstablished() — pre-existing (`:core-sync`)
RaceRepository.observeReference(), ProfileRepository.observe() —
  pre-existing
WatchRaceNavigator.toPreparation() — modified by lot-34 of this cycle.
  Reused, never redeclared.
Clock.now(): Instant — pre-existing
WatchStringResources.Home.referenceLine(name: String?): LabelRef, and
  `.start` / `.sync` / `.history`; WatchStringResources.Sync.failure /
  `.inProgress`; WatchStringResources.Permission.reminder / `.action`;
  WatchStringResources.Connectivity.reminder / `.action` —
  pre-existing, all unchanged
LabelRef — pre-existing (`:core-domain`)
DisplayFormatter, DurationTruncationService — pre-existing, unchanged
TextOverflow, maxLines, viewModelScope, StateFlow, ScalingLazyColumn —
  Jetpack Compose / AndroidX / Wear Compose; not project symbols, and
  already on `:app-wear`'s classpath

Traps carried by these symbols:
- a plain JVM test constructing `HomeViewModel` needs
  `Dispatchers.setMain(...)` in `@Before` and `Dispatchers.resetMain()`
  in `@After` — the class touches `viewModelScope` in its own `init`.
- a `performClick()` on a `ScalingLazyColumn` item past the viewport
  silently no-ops; `HomeScreenTest`'s reminder-action tests need
  `performScrollTo()` first once `HomeScreen`'s items outgrow the
  visible height.
- `:app-wear`'s `createComposeRule()` relies on `ui-test-manifest`,
  already on the module — `HomeScreen`'s Robolectric Compose test is
  built this way.

## Conventions

R4 · `./gradlew check` exits 0, no other definition of done
R74 · `HomeViewModelTest` and `HomeScreenTest` construct
  `HomeViewModel` inside `:app-wear` — the added constructor parameter
  makes them this lot's own scope, never deferred
R12 · §8.3's home page and §9.8's watch half stay in `:app-wear`
R39 · `RaceRecordingRepository` is a constructor argument, never read
  from a top-level property or an `object`
R42 · cooperative async on coroutines, no shared mutable state between
  coroutines
R47 · a screen reads a source once per entry, never in a composition
  body
R55 · one nominal and one failure test per public function, in this lot
R62 · the lexicon — Sync, Reference, Permission, Sensor, Idle; no
  synonym
R63 · English identifiers and comments; every exported symbol carries
  one line saying what it guarantees and when it fails
R64 · no user-facing string literal in the code; the reference line and
  the failure line stay `LabelRef`s into the watch catalogue
R66 · no new dependency inside this lot
R80 · no failure reported through a catalogue key written for another
  case — the `HomeSyncUiState.Failure` branch keeps `sync_failure` and
  names no race

## Requests

—
