## Signatures

HomeViewModel(
  raceRepository: RaceRepository,
  profileRepository: ProfileRepository,
  recordedRaceSyncService: RecordedRaceSyncService,
  connectivityPermissionManager: ConnectivityPermissionManager,
  navigator: WatchRaceNavigator,
  linkStateMonitor: LinkStateMonitor,
  sensorPermissionManager: SensorPermissionManager,
  now: () -> Instant = Instant::now
)
  Adds linkStateMonitor, sensorPermissionManager, now. Collects
  linkStateMonitor.observeLinkEstablished() in init: on each emission,
  sets syncState to InProgress, recomputes, calls
  recordedRaceSyncService.sync(raceInProgress = false, at = now()) — the
  same sequence onSyncClicked already runs. No button tap needed to
  trigger it; a sync that stops on a send/save failure is retried on the
  next emission, since observeLinkEstablished() only fires again on the
  next established transition. Reads sensorPermissionManager.isGranted()
  once, at construction, to seed the reminder's visibility.

HomeViewModel.onSensorPermissionReminderClicked() → Unit
  Calls sensorPermissionManager.requestAgain(). On
  SensorPermissionRequestOutcome.Resolved(state), sets the reminder's
  visibility from state (visible exactly when state is Fallback) and
  recomputes. On RedirectedToSettings, leaves the visibility unchanged.

HomeUiState — adds a field:

  data class HomeUiState(
    val referenceLineText: String,
    val referenceTotalTime: String?,
    val hasReference: Boolean,
    val startLabel: String,
    val historyLabel: String,
    val syncLabel: String,
    val syncState: HomeSyncUiState,
    val sensorPermissionReminderVisible: Boolean
  )

  sensorPermissionReminderVisible — true exactly when the last-read
  sensor permission state is not granted.

HomeScreen(viewModel: HomeViewModel, onHistoryClicked: () -> Unit)
  Renders a reminder line and its action from
  uiState.sensorPermissionReminderVisible, whenever true; the action
  calls viewModel.onSensorPermissionReminderClicked(). Renders neither
  when false.

## Acceptance criteria

- The phone-watch link becoming established calls RecordedRaceSyncService.sync, with no button tap
- A sync that stops on a send/save failure when triggered by the link becoming established is retried the next time the link becomes established
- Constructing HomeViewModel when SensorPermissionManager.isGranted() is false produces a HomeUiState with sensorPermissionReminderVisible = true
- Constructing HomeViewModel when SensorPermissionManager.isGranted() is true produces a HomeUiState with sensorPermissionReminderVisible = false
- HomeScreen renders the reminder and its action when uiState.sensorPermissionReminderVisible is true
- HomeScreen renders neither the reminder nor its action when uiState.sensorPermissionReminderVisible is false
- Triggering the reminder's action calls SensorPermissionManager.requestAgain()
- A requestAgain() outcome of Resolved(Granted) sets sensorPermissionReminderVisible to false
- A requestAgain() outcome of Resolved(Fallback) leaves sensorPermissionReminderVisible true
- A requestAgain() outcome of RedirectedToSettings leaves sensorPermissionReminderVisible unchanged

## Dependencies

RecordedRaceSyncService — pre-existing (sync(raceInProgress, at))
LinkStateMonitor — produced by lot-03 this cycle (observeLinkEstablished(): Flow<Unit>)
SensorPermissionManager — pre-existing; isGranted() added by lot-06 this cycle;
  requestAgain() pre-existing
HomeViewModel — modified: adds linkStateMonitor, sensorPermissionManager, now,
  onSensorPermissionReminderClicked
HomeUiState — modified: adds sensorPermissionReminderVisible
HomeScreen — modified: renders the reminder and its action
