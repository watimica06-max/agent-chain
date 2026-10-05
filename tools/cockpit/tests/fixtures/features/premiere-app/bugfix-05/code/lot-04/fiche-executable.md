## Signatures

ProfileViewModel.onHrMaxUpdated(value: Int) → Unit
Calls ProfileRepository.updateHrMaxBpm(value) and inspects the returned Result. On failure,
ProfileUiState.hrMaxRejectionMessage becomes PhoneStringResources.Profile.hrMaxRejected and
hrMaxBpm/hrMaxLabel stay at the profile's last stored value (unchanged, since the update did not
persist). On success, hrMaxRejectionMessage becomes null.

ProfileViewModel.onExpectedDistanceChanged(value: Int) → Unit
Calls ProfileRepository.updateExpectedDistanceM(value) and inspects the returned Result. On failure,
ProfileUiState.distanceRejectionMessage becomes PhoneStringResources.Profile.distanceRejected and
expectedDistanceM/distanceLabel stay at the profile's last stored value. On success,
distanceRejectionMessage becomes null.

ProfileViewModel.onLongPressChanged(value: Int) → Unit
Calls ProfileRepository.updateLongPressMs(value) and inspects the returned Result. On failure,
ProfileUiState.pressDurationRejectionMessage becomes PhoneStringResources.Profile.pressDurationRejected
and longPressMs/pressDurationLabel stay at the profile's last stored value. On success,
pressDurationRejectionMessage becomes null.

ProfileViewModel.onZoneThresholdChanged(index: Int, value: Int) → Unit
Calls ProfileRepository.updateZoneThreshold(index, value) and inspects the returned Result. On failure,
the ZoneRowUiState whose zone corresponds to `index` gets its rejectionMessage set to
PhoneStringResources.Profile.zoneThresholdRejected, and that row's percentLabel/bpmRangeLabel stay at
the profile's last stored value. On success, that row's rejectionMessage becomes null.

data class ProfileUiState(
  ..., // unchanged fields
  hrMaxRejectionMessage: LabelRef?,
  distanceRejectionMessage: LabelRef?,
  pressDurationRejectionMessage: LabelRef?
)
Each is null when no rejection is pending for that setting.

data class ZoneRowUiState(
  ..., // unchanged fields
  rejectionMessage: LabelRef?
)
Null when no rejection is pending for that zone's threshold.

PhoneStringResources.Profile.hrMaxRejected: LabelRef — static, names the max-heart-rate constraint
PhoneStringResources.Profile.distanceRejected: LabelRef — static, names the expected-distance constraint
PhoneStringResources.Profile.pressDurationRejected: LabelRef — static, names the long-press-duration constraint
PhoneStringResources.Profile.zoneThresholdRejected: LabelRef — static, names the zone-threshold constraint

## Acceptance criteria

- A rejected onHrMaxUpdated leaves ProfileUiState.hrMaxBpm and hrMaxLabel unchanged from the profile's last stored value and sets hrMaxRejectionMessage to PhoneStringResources.Profile.hrMaxRejected
- A successful onHrMaxUpdated occurring after a prior rejection clears hrMaxRejectionMessage to null
- ProfileScreen renders PhoneStringResources.Profile.hrMaxRejected's text when uiState.hrMaxRejectionMessage is non-null
- A rejected onExpectedDistanceChanged leaves ProfileUiState.expectedDistanceM and distanceLabel unchanged from the profile's last stored value and sets distanceRejectionMessage to PhoneStringResources.Profile.distanceRejected
- A successful onExpectedDistanceChanged occurring after a prior rejection clears distanceRejectionMessage to null
- ProfileScreen renders PhoneStringResources.Profile.distanceRejected's text when uiState.distanceRejectionMessage is non-null
- A rejected onLongPressChanged leaves ProfileUiState.longPressMs and pressDurationLabel unchanged from the profile's last stored value and sets pressDurationRejectionMessage to PhoneStringResources.Profile.pressDurationRejected
- A successful onLongPressChanged occurring after a prior rejection clears pressDurationRejectionMessage to null
- ProfileScreen renders PhoneStringResources.Profile.pressDurationRejected's text when uiState.pressDurationRejectionMessage is non-null
- A rejected onZoneThresholdChanged(index, value) leaves the corresponding ZoneRowUiState's percentLabel and bpmRangeLabel unchanged from the profile's last stored value and sets that row's rejectionMessage to PhoneStringResources.Profile.zoneThresholdRejected
- A successful onZoneThresholdChanged(index, value) occurring after a prior rejection at the same index clears that row's rejectionMessage to null
- ProfileScreen renders PhoneStringResources.Profile.zoneThresholdRejected's text for a zone row when that row's rejectionMessage is non-null

## Dependencies

ProfileRepository — pre-existing
ProfileViewModel — pre-existing, modified by this lot
ProfileUiState — pre-existing, modified by this lot
ZoneRowUiState — pre-existing, modified by this lot
ProfileScreen — pre-existing, modified by this lot
PhoneStringResources.Profile — pre-existing, new entries added by this lot
LabelRef — pre-existing

## Conventions

§10 · no hardcoded string
§10 · French only
§10 · interpolated values are passed as resource parameters, never concatenated
§11 · one StateFlow per screen, holding a single immutable UI state class
§11 · a value being typed belongs in `remember`, not the state class
§13 · a repository returns a result type, never null on failure
§13 · never swallow an exception silently
