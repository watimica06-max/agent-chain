## Signatures

    sealed class HomeSyncUiState {
        object Idle : HomeSyncUiState()
        object InProgress : HomeSyncUiState()
        object Failure : HomeSyncUiState()
    }

    data class HomeUiState(
        val referenceLineText: String,
        val referenceTotalTime: String?,
        val hasReference: Boolean,
        val startLabel: String,
        val historyLabel: String,
        val syncLabel: String,
        val syncState: HomeSyncUiState
    )

    class HomeViewModel(
        raceRepository: RaceRepository,
        profileRepository: ProfileRepository,
        private val recordedRaceSyncService: RecordedRaceSyncService,
        private val connectivityPermissionManager: ConnectivityPermissionManager,
        private val navigator: WatchRaceNavigator
    ) {

        val uiState: StateFlow<HomeUiState>

        /**
         * "Démarrer" tapped (§8.3/§9.9): always active regardless of
         * reference/connectivity state. Opens the preparation screen.
         */
        fun onStartClicked()

        /**
         * "Synchroniser" tapped (§6.2/§9.9): in place, no navigation.
         * Sets `uiState.syncState` to `InProgress`, then calls
         * `RecordedRaceSyncService.sync(raceInProgress = false, at)`.
         */
        fun onSyncClicked(at: Instant)
    }

    @Composable
    fun HomeScreen(
        viewModel: HomeViewModel,
        onHistoryClicked: () -> Unit
    )

## Acceptance criteria

- On creation, `ConnectivityPermissionManager.onLaunch()` is called exactly once (§11.2's "checked at every launch")
- `uiState.referenceLineText` equals `WatchStringResources.Home.referenceLine(race.name)` when `RaceRepository.observeReference()` emits a race
- `uiState.referenceLineText` equals `WatchStringResources.Home.referenceLine(null)` when `observeReference()` emits null
- `uiState.hasReference` is true only when `observeReference()` emits a non-null race
- `uiState.referenceTotalTime` equals the reference race's reached segments' summed `durationMs`, truncated and formatted `duration-total` (§10.1) — never a stored cumulative field
- `uiState.referenceTotalTime` is null when there is no reference
- `uiState.startLabel` equals `WatchStringResources.Home.start`; `historyLabel` equals `Home.history`; `syncLabel` equals `Home.sync`
- `onStartClicked` calls `WatchRaceNavigator.toPreparation()`, regardless of `uiState.hasReference` or the connectivity permission's state
- `onSyncClicked(at)` sets `uiState.syncState` to `InProgress` before `RecordedRaceSyncService.sync` returns
- `onSyncClicked(at)` calls `RecordedRaceSyncService.sync(raceInProgress = false, at)`
- Given `RecordedRaceSyncService.observe()` reaches `Success`, `uiState.syncState` returns to `Idle` with no further message shown, leaving the reference line/badge to reflect whatever `observeReference()` and `ProfileRepository.observe()` next emit
- Given `RecordedRaceSyncService.observe()` reaches `Failure`, `uiState.syncState` becomes `Failure`
- Tapping "Historique" invokes the composable's `onHistoryClicked` callback, with no call into any repository or navigator (§8.3: returned from by the system gesture, outside `WatchRaceNavigator`'s race-flow map)

## Dependencies

Race, Segment — pre-existing (lot-01, lot-04)
RaceRepository — pre-existing, extended by lot-25 (`observeReference`)
DurationTruncationService — pre-existing (lot-12)
DisplayFormatter — pre-existing (lot-42)
Profile, ProfileRepository — pre-existing, extended by lot-21/lot-36 (`observe`)
RecordedRaceSyncService — pre-existing (lot-22, found in code, confirmed via lot-22's compte-rendu; reused, not redeclared)
ConnectivityPermissionManager — pre-existing (lot-45)
DesignTokens — pre-existing (lot-02)
WatchStringResources — pre-existing (lot-44), `Home.start`/`history`/`sync`/`referenceLine(name)` and `Sync.inProgress`/`failure` already defined
WatchRaceNavigator — pre-existing (lot-23), `toPreparation()` already defined
