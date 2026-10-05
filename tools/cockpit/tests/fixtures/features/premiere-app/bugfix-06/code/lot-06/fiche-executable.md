## Signatures

HeartRateZoneCalculator.determine(
  reading: Int?, previousZone: HeartRateZone?, profile: Profile
) → HeartRateZone?
  — modification, behaviour only; the signature is unchanged
  — null when `reading` is null, and null for a profile it cannot
    compute on: `hrMaxBpm` null, `hrMaxBpm` zero or negative,
    `zoneThresholds` of a size other than 4, `zoneThresholds` not
    strictly increasing
  — never throws, and never a zone derived from those values
  — otherwise unchanged: the plain-threshold zone, with the existing
    3 bpm up and 2 bpm down hysteresis against `previousZone`

HeartRateZoneCalculator.ranges(profile: Profile) → List<HeartRateZoneRange>?
  — modification, behaviour only; the signature is unchanged, an
    extension function on HeartRateZoneCalculator
  — null on the same four profile cases as `determine`, for the same
    reasons
  — never throws
  — otherwise exactly five entries, in HeartRateZone order, the first
    carrying a null bpmLow and the last a null bpmHigh

HeartRateZoneRange(zone, percent, bpmLow, bpmHigh)
  — unchanged: no field added, removed or retyped

## Acceptance criteria

- A profile of hrMaxBpm 190 and zoneThresholds [60, 70, 80, 90], a
  reading of 140 and no previous zone, determines ZONE_3
- A null reading determines no zone
- A profile whose hrMaxBpm is null determines no zone and yields no
  ranges
- A profile whose hrMaxBpm is 0 determines no zone and yields no ranges
- A profile whose hrMaxBpm is negative determines no zone and yields no
  ranges
- A profile whose zoneThresholds holds three values determines no zone
  and yields no ranges
- A profile whose zoneThresholds holds five values determines no zone
  and yields no ranges
- A profile whose zoneThresholds is [60, 70, 70, 90] determines no zone
  and yields no ranges
- A profile whose zoneThresholds is [60, 80, 70, 90] determines no zone
  and yields no ranges
- A profile of hrMaxBpm 190 and zoneThresholds [60, 70, 80, 90] yields
  five ranges, the first with no bpmLow and the last with no bpmHigh

## Dependencies

Profile — pre-existing (hrMaxBpm: Int?, zoneThresholds: List<Int>)
HeartRateZone — pre-existing (ZONE_1..ZONE_5)
HeartRateZoneRange — pre-existing, declared in HeartRateZoneCalculator.kt

## Conventions

R4 · `./gradlew check` exits 0
R10 · the module realising an entry that consumes nothing imports no other
R20 · missing data as a nullable, never an invented default
R22 · what it returns for every input it cannot compute on
R27 · the zone upper bound is exclusive, every other bound inclusive
R28 · a percentage of hrMaxBpm converts to bpm by rounding, not truncating
R41 · a calculation entry is a pure function
R55 · a nominal test and a failure test per public function, same lot
R57 · a test building a value violating "strictly increasing zone
      thresholds"
R59 · a test on the 187 bpm ladder and the 3 bpm hysteresis
R62 · the lexicon — HrMax, ZoneThreshold, Zone, Profile
R63 · English, and one line per exported symbol saying when it fails

## Requests

—
