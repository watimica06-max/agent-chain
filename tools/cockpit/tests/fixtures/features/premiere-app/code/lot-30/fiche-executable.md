## Signatures

    data class HeartRateZoneRange(
        val zone: HeartRateZone,
        val percent: Int,
        val bpmLow: Int?,
        val bpmHigh: Int?
    )

    // HeartRateZoneCalculator (object, pre-existing) gains:
    fun HeartRateZoneCalculator.ranges(profile: Profile): List<HeartRateZoneRange>?

    // PhoneStringResources.Profile (object, pre-existing) gains:
    fun Profile.lastSyncToday(time: String): String       // "aujourd'hui à {time}"
    fun Profile.lastSyncYesterday(time: String): String    // "hier à {time}"

    data class ZoneRowUiState(
        val zone: HeartRateZone,
        val label: String,
        val percentLabel: String,
        val bpmRangeLabel: String
    )

    sealed class ProfileSyncUiState {
        object Idle : ProfileSyncUiState()
        object InProgress : ProfileSyncUiState()
        object Failure : ProfileSyncUiState()
    }

    data class ProfileUiState(
        val hrMaxBpm: Int?,
        val hrMaxLabel: String?,
        val zoneRows: List<ZoneRowUiState>,
        val expectedDistanceM: Int,
        val distanceLabel: String,
        val longPressMs: Int,
        val pressDurationLabel: String,
        val syncStatusText: String,
        val isConnectivityDenied: Boolean,
        val isSyncActionEnabled: Boolean,
        val syncState: ProfileSyncUiState
    )

    /** Reads the phone's heart-rate health history (§5.2), Health-Connect-backed. */
    interface HrHistoryReader {
        suspend fun bpmValuesOverLast12Months(): List<Int>
    }

    class ProfileViewModel(
        private val profileRepository: ProfileRepository,
        private val profileSyncPushService: ProfileSyncPushService,
        private val connectivityPermissionManager: ConnectivityPermissionManager,
        private val hrHistoryReader: HrHistoryReader,
        private val now: () -> Instant = Instant::now,
    ) {

        val uiState: StateFlow<ProfileUiState>

        /** "Modifier" dialog confirmed (§9.6). */
        fun onHrMaxUpdated(value: Int)

        /** Distance field loses focus (§9.6, validated inline). */
        fun onExpectedDistanceChanged(value: Int)

        /** Long-press-duration field loses focus (§9.6, validated inline). */
        fun onLongPressChanged(value: Int)

        /**
         * "Synchroniser avec la montre" or "Réessayer" tapped (§9.6/§6.1).
         * No-op while `uiState.isConnectivityDenied` is true — the button
         * stays inactive (§9.18).
         */
        fun onSyncClicked(at: Instant)

        /** "Autoriser" tapped under the sync line while denied (§9.18). */
        fun onAllowConnectivityClicked()
    }

    @Composable
    fun ProfileScreen(viewModel: ProfileViewModel)

## Acceptance criteria

- `HeartRateZoneCalculator.ranges(profile)` returns null when `profile.hrMaxBpm` is null
- `HeartRateZoneCalculator.ranges(profile)` returns exactly 5 entries, in `ZONE_1`..`ZONE_5` order, when `profile.hrMaxBpm` is non-null
- `ranges(profile)`'s `ZONE_1` entry has `percent` 0, `bpmLow` null, `bpmHigh` equal to `profile.zoneThresholds[0]` converted to bpm the same way `determine` converts a threshold (`(threshold / 100.0 * hrMaxBpm).roundToInt()`)
- `ranges(profile)`'s `ZONE_2`/`ZONE_3`/`ZONE_4` entries have `percent` equal to `profile.zoneThresholds[0]`/`[1]`/`[2]` respectively, and `bpmLow`/`bpmHigh` equal to the adjacent converted thresholds (e.g. `ZONE_3`'s `bpmLow`/`bpmHigh` are `zoneThresholds[1]`/`[2]` converted)
- `ranges(profile)`'s `ZONE_5` entry has `percent` equal to `profile.zoneThresholds[3]`, `bpmLow` equal to that threshold converted, `bpmHigh` null
- `PhoneStringResources.Profile.lastSyncToday("09:02")` equals `"aujourd'hui à 09:02"`
- `PhoneStringResources.Profile.lastSyncYesterday("09:02")` equals `"hier à 09:02"`
- `uiState.hrMaxLabel` equals `DisplayFormatter.formatHr(hrMaxBpm)` when `Profile.hrMaxBpm` is non-null
- `uiState.hrMaxLabel` is null when `Profile.hrMaxBpm` is null
- `uiState.zoneRows` is empty when `Profile.hrMaxBpm` is null
- `uiState.zoneRows` holds 5 entries when `Profile.hrMaxBpm` is non-null, each `label` equal to `PhoneStringResources.Profile.zoneRow(n)` (1-indexed by zone)
- Each row's `percentLabel` equals `DisplayFormatter.formatZonePercentage` of its `HeartRateZoneRange.percent`
- The first row's `bpmRangeLabel` equals `DisplayFormatter.formatZoneRangeExtreme(RangeOperator.BELOW, bpmHigh)`
- The middle three rows' `bpmRangeLabel` equal `DisplayFormatter.formatZoneRange(bpmLow, bpmHigh)`
- The last row's `bpmRangeLabel` equals `DisplayFormatter.formatZoneRangeExtreme(RangeOperator.ABOVE, bpmLow)`
- `uiState.distanceLabel` equals `DisplayFormatter.formatDistance(expectedDistanceM)`
- `uiState.pressDurationLabel` equals `DisplayFormatter.formatPressDuration(longPressMs)`
- On construction, when `ProfileRepository.observe()`'s first emission has `hrMaxBpm` null, `HrHistoryReader.bpmValuesOverLast12Months()` is called
- On construction, when the first emission has `hrMaxBpm` non-null, `HrHistoryReader.bpmValuesOverLast12Months()` is never called
- Given `hrMaxBpm` was null and `HrHistoryReader.bpmValuesOverLast12Months()` returns a non-empty list, `ProfileRepository.updateHrMaxBpm` is called with `HrMaxDerivationService.derive(null, values)`'s result
- Given `hrMaxBpm` was null and `HrHistoryReader.bpmValuesOverLast12Months()` returns an empty list, `ProfileRepository.updateHrMaxBpm` is never called, and `uiState.hrMaxBpm` stays null
- `onHrMaxUpdated(value)` calls `ProfileRepository.updateHrMaxBpm(value)`
- `onExpectedDistanceChanged(value)` calls `ProfileRepository.updateExpectedDistanceM(value)`
- `onLongPressChanged(value)` calls `ProfileRepository.updateLongPressMs(value)`
- On creation, `ConnectivityPermissionManager.onLaunch()` is called exactly once
- `uiState.isConnectivityDenied` is true when `onLaunch()` resolves `Fallback`, false when it resolves `Granted`
- `uiState.isSyncActionEnabled` equals `!uiState.isConnectivityDenied`
- `onAllowConnectivityClicked()` calls `ConnectivityPermissionManager.requestAgain()`
- Given `requestAgain()` resolves `Resolved(Granted)`, `uiState.isConnectivityDenied` becomes false
- Given `requestAgain()` resolves `Resolved(Fallback)`, `uiState.isConnectivityDenied` stays true
- Given `requestAgain()` resolves `RedirectedToSettings`, `uiState.isConnectivityDenied` is unchanged
- Given `uiState.isConnectivityDenied` is true, `uiState.syncStatusText` equals `PhoneStringResources.Profile.syncUnavailable`, regardless of `lastSyncSuccessAt`
- Given `uiState.isConnectivityDenied` is false and `Profile.lastSyncSuccessAt` is null, `uiState.syncStatusText` equals `PhoneStringResources.Profile.lastSync(null)` ("Jamais synchronisé")
- Given `isConnectivityDenied` is false and `lastSyncSuccessAt` falls on `now()`'s calendar day, `uiState.syncStatusText` equals `PhoneStringResources.Profile.lastSync(PhoneStringResources.Profile.lastSyncToday(time))`, `time` being `DisplayFormatter.formatDateRelative(lastSyncSuccessAt, now())`'s `Today.time`
- Given `isConnectivityDenied` is false and `lastSyncSuccessAt` falls on the calendar day before `now()`, `uiState.syncStatusText` equals `PhoneStringResources.Profile.lastSync(PhoneStringResources.Profile.lastSyncYesterday(time))`
- Given `isConnectivityDenied` is false and `lastSyncSuccessAt` falls earlier than that, `uiState.syncStatusText` equals `PhoneStringResources.Profile.lastSync(dateTime)`, `dateTime` being `formatDateRelative`'s `Earlier.dateTime`, unwrapped
- `onSyncClicked(at)` makes no call to `ProfileSyncPushService.push` when `uiState.isConnectivityDenied` is true
- `onSyncClicked(at)`, when `isConnectivityDenied` is false, sets `uiState.syncState` to `InProgress` before `ProfileSyncPushService.push` returns, then calls `push(permissionGranted = true, at = at)`
- Given `push` returns `Success`, `uiState.syncState` becomes `Idle`
- Given `push` returns `Failure`, `uiState.syncState` becomes `Failure`

## Dependencies

Profile — pre-existing (lot-05)
ProfileRepository — pre-existing (lot-05), extended by lot-21 (`markSyncSuccess`) and lot-36 (`observe`)
HeartRateZone — pre-existing (lot-07)
HeartRateZoneCalculator — pre-existing (lot-07), modified by this lot (adds `ranges`)
HrMaxDerivationService — pre-existing (lot-19)
ConnectivityPermissionManager, ConnectivityPermissionState, ConnectivityPermissionRequestOutcome — pre-existing (lot-45)
ProfileSyncPushService, ProfileSyncPushOutcome — pre-existing (lot-21, found in code, confirmed via lot-21's compte-rendu; reused, not redeclared)
DisplayFormatter, DateDisplay, RangeOperator — pre-existing (lot-42)
DesignTokens — pre-existing (lot-02)
PhoneStringResources — pre-existing (lot-43), `Profile.hrMaxSource`/`hrMaxEdit`/`syncAction`/`syncUnavailable`/`syncAllowAction`/`zoneRow`/`distanceLabel`/`pressDurationLabel`/`lastSync` and `Sync.inProgress`/`failure`/`retry` already defined; modified by this lot (adds `Profile.lastSyncToday`/`lastSyncYesterday`, per the settled blocking decision)
PhoneNavigator — pre-existing (lot-24)
HeartRateZoneRange, ZoneRowUiState, ProfileSyncUiState, ProfileUiState, HrHistoryReader, ProfileViewModel, ProfileScreen — produced by this lot
