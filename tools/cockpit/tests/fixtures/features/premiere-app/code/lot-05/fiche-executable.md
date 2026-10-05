## Signatures

data class Profile(
  hrMaxBpm: Int?,
  zoneThresholds: List<Int>,
  expectedDistanceM: Int,
  longPressMs: Int,
  correctionFactor: Float,
  lastSyncSuccessAt: Instant?
)

ProfileRepository.updateHrMaxBpm(value: Int) → Result<Unit>

ProfileRepository.updateZoneThreshold(index: Int, value: Int) → Result<Unit>

ProfileRepository.updateExpectedDistanceM(value: Int) → Result<Unit>

ProfileRepository.updateLongPressMs(value: Int) → Result<Unit>

ProfileRepository.updateCorrectionFactor(value: Float) → Result<Unit>

## Acceptance criteria

- A freshly created Profile carries hrMaxBpm unset, zoneThresholds [60, 70, 80, 90], expectedDistanceM 1000, longPressMs 700, correctionFactor 1, and lastSyncSuccessAt unset
- Setting hrMaxBpm to a value within 100–230 updates the stored value
- Setting hrMaxBpm to a value outside 100–230 leaves the stored value unchanged and returns a failure
- Setting a zoneThreshold entry to a value within 30–99 that keeps all four thresholds strictly increasing updates that entry
- Setting a zoneThreshold entry to a value outside 30–99 leaves all four thresholds unchanged and returns a failure
- Setting a zoneThreshold entry to a value that breaks the strictly increasing order across the four thresholds leaves all four thresholds unchanged and returns a failure
- Setting expectedDistanceM to a value within 500–2000 updates the stored value
- Setting expectedDistanceM to a value outside 500–2000 leaves the stored value unchanged and returns a failure
- Setting longPressMs to a value within 300–2000 updates the stored value
- Setting longPressMs to a value outside 300–2000 leaves the stored value unchanged and returns a failure
- Updating the correction factor writes the given value as the new stored correctionFactor

## Dependencies

None — all types are produced by this lot.
