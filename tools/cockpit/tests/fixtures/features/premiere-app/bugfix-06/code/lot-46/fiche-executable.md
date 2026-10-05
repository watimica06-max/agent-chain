## Signatures

HeartRateReading(bpm: Int, atElapsedRealtime: Long)
  — a Health Services heart-rate data point, converted to a domain type
    at the boundary (R32); `atElapsedRealtime` is the monotonic instant
    the platform reported the reading at

DistanceReading(cumulativeDistanceM: Double, atElapsedRealtime: Long)
  — a Health Services cumulative-distance data point, converted to a
    domain type at the boundary (R32)

SensorReadingsSource(measureClient: MeasureClient)

  .heartRate(): Flow<HeartRateReading>
    — one emission per heart-rate data point the platform delivers
      while this instance is registered for `SensorDataType.HEART_RATE`;
      nothing before `register` or after `unregister`

  .distance(): Flow<DistanceReading>
    — one emission per cumulative-distance data point delivered while
      registered for `SensorDataType.DISTANCE`

  .speed(): Flow<SpeedSample>
    — one emission per speed data point delivered while registered for
      `SensorDataType.SPEED`; reuses the pre-existing `SpeedSample`
      shape (`speedMetersPerSecond`, `atElapsedRealtime`)

  .register(dataTypes: Set<SensorDataType>): Boolean
    — suspend; registers one `MeasureCallback` with `measureClient` per
      type in `dataTypes`; true once every requested type is registered,
      false on any registration failure; a type absent from `dataTypes`
      is never forwarded on its flow even if the platform delivers one

  .unregister(): Boolean
    — suspend; clears every callback this instance registered; true on
      success, false on failure

## Acceptance criteria

- `register(setOf(HEART_RATE))` then a heart-rate data point delivered by the platform is forwarded on `heartRate()` carrying the same bpm and timestamp
- `register(setOf(DISTANCE))` then a cumulative-distance data point delivered is forwarded on `distance()` carrying the same value and timestamp
- `register(setOf(SPEED))` then a speed data point delivered is forwarded on `speed()` as a `SpeedSample` carrying the same value and timestamp
- `register(setOf(HEART_RATE))` (DISTANCE/SPEED excluded) — a distance data point delivered by the platform produces no emission on `distance()`
- `unregister()` called after `register()` — a data point delivered afterward produces no further emission on any of the three flows
- `register()` returns false when the underlying platform registration fails, true when every requested type registers successfully

## Dependencies

SensorDataType — pre-existing
SpeedSample — pre-existing
MeasureClient — Health Services Client, pre-existing framework dependency

## Conventions

§4 R13 · external-source access confined to the module realising its §5 entry
§5 R17 · a quantity carrying a unit or identity carries its own type
§6 R32 · data entering from outside the process is converted to a domain type at the receiving module
§5 R19 · a public operation that can block is suspend
§6 R33 · a call leaving the process returns its failure as a value
§7 R40 · an acquired resource (the registered callback) is released in the same scope it was acquired
§10 R55 · every public function has a nominal and a failure test
§10 R56 · no test reaches a real sensor; readings and I/O are injected

## Requests

—
