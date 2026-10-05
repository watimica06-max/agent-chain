## Signatures

ProfileViewModel(
  profileRepository: ProfileRepository,
  profileSyncPushService: ProfileSyncPushService,
  connectivityPermissionManager: ConnectivityPermissionManager,
  hrHistoryReader: HrHistoryReader,
  linkStateMonitor: LinkStateMonitor,
  now: () -> Instant = Instant::now
)
  Adds linkStateMonitor. Collects linkStateMonitor.observeLinkEstablished()
  in init: on each emission, sets syncState to InProgress, recomputes,
  calls profileSyncPushService.push(permissionGranted = true, at = now()),
  then sets syncState to Idle on Success or Failure on Failure and
  recomputes — the same sequence onSyncClicked already runs, minus the
  isConnectivityDenied guard, which onSyncClicked keeps for its own tap
  path. No button tap needed to trigger it; a refused/failed push is
  retried on the next emission, since observeLinkEstablished() only
  fires again on the next established transition.

ProfileViewModel.onZoneThresholdChanged(index: Int, value: Int) → Unit
  Calls ProfileRepository.updateZoneThreshold(index, value).

ProfileScreen — ZonesSection(uiState: ProfileUiState, viewModel: ProfileViewModel)
  For every row but the first (HeartRateZoneCalculator.ranges' index 0
  carries no threshold — ZONE_1 is open-ended), presents the threshold
  inline as an editable numeric field, validated on loss of focus like
  the distance and long-press fields, calling
  viewModel.onZoneThresholdChanged(index, value) where index is
  zone.ordinal - 1 (0..3, ProfileRepository.updateZoneThreshold's own
  indexing). The first row keeps its current, non-editable rendering.

## Acceptance criteria

- The phone-watch link becoming established calls ProfileSyncPushService.push, with no button tap
- A push that returns Failure when triggered by the link becoming established is retried the next time the link becomes established
- Editing one of zones 2 through 5's threshold field and losing focus calls ProfileViewModel.onZoneThresholdChanged with that zone's threshold index (0 to 3) and the entered value
- ProfileViewModel.onZoneThresholdChanged calls ProfileRepository.updateZoneThreshold with the same index and value
- The first zone's row renders with no editable field

## Dependencies

ProfileRepository — pre-existing (observe(); updateZoneThreshold(index, value))
ProfileSyncPushService — pre-existing (push(permissionGranted, at))
LinkStateMonitor — produced by lot-03 this cycle (observeLinkEstablished(): Flow<Unit>)
ProfileViewModel — modified: adds linkStateMonitor, adds onZoneThresholdChanged
ProfileScreen — modified: ZonesSection renders each threshold but the first as an editable field
