## Signatures

enum class HeartRateZone { ZONE_1, ZONE_2, ZONE_3, ZONE_4, ZONE_5 }

HeartRateZoneCalculator.determine(
  reading: Int?, previousZone: HeartRateZone?, profile: Profile
) → HeartRateZone?

## Acceptance criteria

- With hrMaxBpm = 187 and default thresholds (60/70/80/90), a reading of 100bpm with no previous zone determines ZONE_1
- With hrMaxBpm = 187 and default thresholds, a reading of 140bpm with no previous zone determines ZONE_3
- With hrMaxBpm = 187 and default thresholds, a reading of 168bpm with no previous zone determines ZONE_5
- From an active ZONE_2 (zone2/3 boundary at 131bpm), a reading of 133bpm (boundary + 2) stays ZONE_2
- From an active ZONE_2, a reading of 134bpm (boundary + 3) moves to ZONE_3
- From an active ZONE_3, a reading of 129bpm (3bpm below the 131bpm boundary) drops back to ZONE_2
- From an active ZONE_3, a reading of 130bpm (2bpm below the boundary) stays ZONE_3
- After a gap with no reading (previousZone = null), a reading of 133bpm determines ZONE_3 directly from the plain threshold, with no hysteresis applied
- From an active ZONE_2, a reading of 150bpm (plain-threshold zone 4) jumps directly to ZONE_4, never passing through ZONE_3
- A null reading determines no active zone (null), whatever the previous zone
- A profile with hrMaxBpm unset determines no active zone (null), whatever the reading

## Dependencies

Profile — pre-existing (lot-05)
