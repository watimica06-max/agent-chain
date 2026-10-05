## Signatures

HrMaxDerivationService.derive(
  currentHrMaxBpm: Int?, historyBpmValues: List<Int>
) → Int?

## Acceptance criteria

- When currentHrMaxBpm is null and historyBpmValues is non-empty, the derived value equals the highest value in historyBpmValues
- When currentHrMaxBpm is null and historyBpmValues is empty, the derived value is null — hrMaxBpm stays unset
- When currentHrMaxBpm is non-null, the derived value equals currentHrMaxBpm unchanged, even when historyBpmValues contains a higher value
- Among several distinct values in historyBpmValues, the highest one is selected, never the most recent nor an average

## Dependencies

None — all types are produced by this lot (currentHrMaxBpm matches Profile.hrMaxBpm's type, pre-existing on lot-05).
