## Signatures

### HealthHistoryAvailability — production (`:app-phone`)

    open class HealthHistoryAvailability @Inject constructor(
      @ApplicationContext context: Context
    )

    open suspend fun isAvailable(): Boolean
      — true only when HealthConnectClient.getSdkStatus(context) reports the
        SDK available; false for every other status, a provider update
        required included, and false for a status this class does not
        recognise
      — never raises: a failure of the status call is returned as false, so
        an unreadable status reads the same as an absent provider
      — open, and its class open, so a test hands ProfileViewModel another
        answer and both branches are reachable with no Health Connect
        installed

Scope note: this symbol is not on lot-19's `Modifies` line.
`blocked_detailleur-01.md`'s `## Decision` assigns it to lot-19, because
R74 makes a same-module call site this lot's own scope. It is named in the
lot report.

### PhoneStringResources.Profile.hrHistoryUnavailable — production (`:app-phone`)

    val hrHistoryUnavailable: LabelRef = LabelRef(R.string.profile_hr_history_unavailable)
      — no args, so ProfileScreen resolves it through the single-arg
        stringResource(id) overload

    R.string.profile_hr_history_unavailable — new entry in
    app-phone/src/main/res/values/strings.xml, French, one full sentence in
    the shape profile_sync_unavailable already carries, saying that the
    heart-rate history cannot be read because Health Connect is absent from
    this device. Any literal `%` escaped as `%%`.

Scope note: same as above — assigned here by the settled decision, not by
`decoupage.md`.

### ProfileUiState — modification (`:app-phone`)

After the change:

    data class ProfileUiState(
      hrMaxBpm: Int?,
      hrMaxLabel: String?,
      hrMaxRejectionMessage: LabelRef?,
      zoneRows: List<ZoneRowUiState>,
      expectedDistanceM: Int,
      distanceRejectionMessage: LabelRef?,
      longPressMs: Int,
      pressDurationRejectionMessage: LabelRef?,
      syncStatusText: LabelRef,
      isConnectivityDenied: Boolean,
      isSyncActionEnabled: Boolean,
      syncState: ProfileSyncUiState,
      isHealthHistoryUnavailable: Boolean
    )

What changes:

- `distanceLabel` and `pressDurationLabel` are dropped, and the two writes
  populating them in `ProfileViewModel.toUiState` and in `DEFAULT_UI_STATE`
  go with them (§9.1).
  ⚠️ `PhoneStringResources.Profile.distanceLabel` and
  `PhoneStringResources.Profile.pressDurationLabel` are different symbols
  and stay: `ProfileScreen` reads both and `PhoneStringResourcesTest`
  asserts both.
- `isHealthHistoryUnavailable` is added (§5.2) — true only once
  `HealthHistoryAvailability.isAvailable()` has answered false; false in
  `DEFAULT_UI_STATE`, false while that answer is pending, and false when
  Health Connect is present but the heart-rate permission is not granted.
  That last case is what makes it distinct from "permission not yet
  granted".

`ZoneRowUiState` and `ProfileSyncUiState` are unchanged.

### ProfileViewModel — modification (`:app-phone`)

After the change:

    @HiltViewModel
    class ProfileViewModel @Inject constructor(
      profileRepository: ProfileRepository,
      profileSyncPushService: ProfileSyncPushService,
      connectivityPermissionManager: ConnectivityPermissionManager,
      hrHistoryReader: HrHistoryReader,
      hrPermissionSystem: HrPermissionSystem,
      linkStateMonitor: LinkStateMonitor,
      clock: Clock,
      healthHistoryAvailability: HealthHistoryAvailability,
      savedStateHandle: SavedStateHandle
    ) : ViewModel()

    val uiState: StateFlow<ProfileUiState>
      — unchanged; starts at DEFAULT_UI_STATE and never emits null

    fun onHrMaxUpdated(value: Int)
    fun onExpectedDistanceChanged(value: Int)
    fun onLongPressChanged(value: Int)
    fun onZoneThresholdChanged(index: Int, value: Int)
      — the four signatures are unchanged, `Unit` included
      — each returns before its repository write completes: the write and
        the recompute() that follows it run inside viewModelScope.launch,
        so uiState carries the outcome only once that coroutine ends (§7.1)

    fun onSyncClicked(at: Instant)
    fun onAllowConnectivityClicked()
      — unchanged

What changes:

1. Two constructor parameters are appended, in that order (§5.2, §12.2).
   `SavedStateHandle` needs no `@Assisted`: Hilt supplies it to a
   `@HiltViewModel` on its own.

2. The four setting handlers move their `profileRepository.update*` call
   and the `recompute()` that follows it inside `viewModelScope.launch`
   (§7.1). This is the compile break `:app-phone` carries at HEAD —
   `ProfileRepository`'s five updaters are already `suspend` in
   `:core-domain`, and lot-14's report names lot-19 as the owner of these
   four call sites under R73/R74.

3. The init launch that derives `hrMaxBpm` from the heart-rate history
   first awaits `healthHistoryAvailability.isAvailable()` (§5.2):
   - false — `isHealthHistoryUnavailable` becomes true and neither
     `hrPermissionSystem` nor `hrHistoryReader` is called at all;
   - true — `isHealthHistoryUnavailable` stays false and the existing
     sequence runs unchanged: read the profile once, and only when
     `hrMaxBpm` is null ask the permission, then read the history.
   The check runs once per launch and is never repeated afterwards.

4. What the `SavedStateHandle` holds, and what it does not (§12.2):
   - held: one Boolean per rejection site — max heart rate, distance,
     long-press duration — and a `BooleanArray` of 4 for the editable zone
     thresholds, index 0 for zone 2 through index 3 for zone 5. Each of the
     four `LabelRef` values shown is a constant with no args, so it is
     derived from its Boolean on read and never stored: `LabelRef` is not
     Bundle-storable, and §12.2's second gap already settles that the
     primitives a value is built from are what gets saved.
   - not held: `latestProfile`, re-read from `profileRepository.observe()`;
     `isConnectivityDenied`, re-derived by
     `connectivityPermissionManager.onLaunch()` at each launch;
     `syncState`, which reads `Idle` after a rebuild;
     `isHealthHistoryUnavailable`, re-derived by the launch check of point 3.

5. `syncStatusText`'s `when` over `DateDisplay` is already exhaustive and
   already carries the `DateDisplay.Future` branch — lot-17 wrote it and
   its report records it. §9.9 leaves nothing to build here; what lot-19
   owes it is the test that has never yet run, `:app-phone:check` having
   been red since lot-17.

### ProfileScreen — modification (`:app-phone`)

    @Composable fun ProfileScreen(viewModel: ProfileViewModel)
      — signature unchanged

What changes:

- `hrMaxEditValue`, `ZoneThresholdField`'s `fieldValue`,
  `SettingsFields`'s `distanceFieldValue` and `longPressFieldValue` move
  from `remember` to `rememberSaveable`, each keeping the key it already
  carries — `row.percentLabel`, `uiState.expectedDistanceM`,
  `uiState.longPressMs`, and none for `hrMaxEditValue` (§12.4). All four
  hold a `String` or `String?`, both saveable as they stand.
- When `uiState.isHealthHistoryUnavailable` is true the screen renders
  `PhoneStringResources.Profile.hrHistoryUnavailable` as text, in the
  heart-rate section; when false it renders nothing in its place (§5.2).

### ProfileViewModelTest, ProfileScreenTest — modification (`:app-phone`)

- `FakeProfileRepository` follows `ProfileRepository`'s current interface:
  the five updaters and `markSyncSuccess` become `suspend`, and
  `applyIncomingProfile` is implemented.
- The four assertions on `uiState.value.distanceLabel` /
  `pressDurationLabel` (lines 366, 375, 797, 828) go with the dropped
  fields; the values they covered are still observable through
  `expectedDistanceM` and `longPressMs`.
- Both tests must install `Dispatchers.setMain(UnconfinedTestDispatcher())`
  — `ProfileViewModel` is named in the state document's trap on this.

## Acceptance criteria

Heart-rate history unavailable (§5.2)

- With Health Connect reporting its SDK unavailable, the profile screen
  shows the heart-rate-history-unavailable text.
- With Health Connect reporting its SDK unavailable, no heart-rate
  permission is ever requested and no heart-rate history is ever read.
- With Health Connect reporting its SDK available and the heart-rate
  permission not granted, the profile screen shows no
  heart-rate-history-unavailable text.
- With Health Connect reporting its SDK available, the permission granted
  and a stored profile whose max heart rate is unset, the max heart rate
  derived from the 12-month history is written to the profile.
- A status call that raises is treated as unavailable: the screen shows the
  same text as for an absent provider.

Settings written from a coroutine (§7.1)

- Confirming the max-heart-rate dialog with a value the repository accepts:
  the screen shows that value as the max heart rate and no rejection
  message.
- Confirming the max-heart-rate dialog with a value the repository refuses:
  the screen shows the max-heart-rate rejection message and the previously
  stored value.
- Blurring the distance field on a value the repository accepts: the screen
  shows no distance rejection message.
- Blurring the distance field on a value the repository refuses: the screen
  shows the distance rejection message.
- Blurring the long-press field on a value the repository refuses: the
  screen shows the long-press rejection message.
- Blurring zone 4's threshold field on a value the repository refuses: zone
  4's row shows a rejection message and the other three editable rows show
  none.
- With the repository's update suspended and not yet completed, each of the
  four handlers has returned and the screen still shows its previous state.

Dead UI-state fields (§9.1)

- `ProfileUiState` exposes no `distanceLabel` member and no
  `pressDurationLabel` member.
- The distance field and the long-press field on screen show the values the
  stored profile carries.

A sync timestamp in the future (§9.9)

- With a last successful sync whose date is after now's, the sync line
  reads the future-sync sentence.
- With a last successful sync before yesterday, the sync line reads the
  earlier-sync sentence.
- With no last successful sync recorded, the sync line reads the
  never-synced sentence.

ViewModel state across a rebuild (§12.2)

- A max-heart-rate rejection message shown, then a ProfileViewModel rebuilt
  from the same SavedStateHandle: the screen shows that rejection message
  again.
- A rejection message shown on zone 4's row, then a rebuild from the same
  SavedStateHandle: zone 4's row shows it again and the other three
  editable rows show none.
- A sync left in progress, then a rebuild from the same SavedStateHandle:
  the screen shows no in-progress and no failure line.
- A fresh SavedStateHandle carrying nothing: the screen shows no rejection
  message on any of the four settings.

A field being edited across a rotation (§12.4)

- The max-heart-rate dialog open on a typed but unconfirmed value, then a
  configuration change: the dialog is still open and still carries that
  value.
- The distance field carrying typed text that has not lost focus, then a
  configuration change: the field still carries that text.
- The long-press field carrying typed text that has not lost focus, then a
  configuration change: the field still carries that text.
- Zone 4's threshold field carrying typed text that has not lost focus,
  then a configuration change: that field still carries that text and the
  other three editable rows carry their stored values.

## Dependencies

ProfileRepository — pre-existing (`:core-domain`), its five updaters and
  `markSyncSuccess` already `suspend`, `applyIncomingProfile` already
  present
ProfileSyncPushService — pre-existing, already injected
ConnectivityPermissionManager, LinkStateMonitor, Clock, HrHistoryReader,
  HrPermissionSystem, HrMaxDerivationService, HeartRateZoneCalculator,
  DisplayFormatter, LabelRef — pre-existing, already injected or imported
DateDisplay.Future — created by lot-07, already branched on by lot-17
PhoneStringResources.Profile.lastSyncFuture — created by lot-17
PhoneStringResources.Profile.hrHistoryUnavailable — produced by this lot
HealthHistoryAvailability — produced by this lot
HealthConnectClient.getSdkStatus — Health Connect Client 1.1, a declared
  dependency of `:app-phone`; not a project symbol
SavedStateHandle — `androidx.lifecycle.SavedStateHandle`, framework;
  `decoupage.md` declares it pre-existing. ⚠️ It appears nowhere in this
  repository's code and no `lifecycle-viewmodel-savedstate` entry exists in
  `gradle/libs.versions.toml`; it is reachable only as a transitive of
  `androidx.hilt.navigation.compose`. See `## Requests`.

## Conventions

§2 · R4 — `./gradlew check` exits 0, the one definition of done
§2 · R74 — a same-module call site is this lot's own scope, never deferred
§2 · R73 — a deliverable-under-R72 lot names the failing call site and its owner
§4 · R12 — §5.2 is realised in `:app-phone` and in no other module
§4 · R13 — the Health Connect client is confined to `:app-phone`
§5 · R17 — no bare primitive carrying a unit in a public signature
§5 · R19, R24 — what blocks or reaches outside the process is `suspend`
§5 · R20 — missing data crosses as a nullable or a declared absence type
§5 · R22 — what computes states what it returns for every input it cannot compute on
§5 · R26 — no `!!` on a value coming from outside the function
§6 · R30 — no empty and no generic catch
§6 · R33 — a call leaving the process returns its failure as a value
§6 · R34 — a caller receiving a failure acts on it
§7 · R39 — dependencies passed as arguments, no mutable global state
§7 · R42 — cooperative async on Kotlin coroutines
§7 · R44 — one state holder per journey, the profile edit included
§7 · R45 — a screen keeps what the user has in progress across a system rebuild
§7 · R46 — what must be found again after a process death is written where it survives
§7 · R47 — a screen reads a source once per entry, never in a composition body
§8 · R52 — every launch-time prerequisite is checked at each launch, none stops the
  application, each failure enters its degraded state, the check is never auto-repeated
§10 · R55 — one nominal and one failure test per public function
§10 · R56 — no test reaches I/O; readings and time are injected
§11 · R62 — the lexicon: Profile, HrMax, Zone, Permission, HealthHistory, Sync
§11 · R63 — English identifiers, French only in the resource files, one doc line per
  exported symbol
§11 · R64 — no user-facing string is a literal in the code
§12 · R66 — no new dependency inside a lot

## Requests

architecte/detailleur-lot-19.md
