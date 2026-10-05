## Signatures

HrHistoryReaderImpl(healthConnectClient: HealthConnectClient) : HrHistoryReader

  override suspend fun bpmValuesOverLast12Months(): List<Int>
  — every heart-rate bpm reading whose record falls within the twelve
  months trailing the call, read through the Health Connect client;
  empty when none is recorded in that window

## Acceptance criteria

- A heart-rate reading recorded within the trailing 12 months is present in the returned list
- A heart-rate reading recorded more than 12 months before the call is absent from the returned list
- No heart-rate reading recorded in Health Connect returns an empty list

## Dependencies

HrHistoryReader — pre-existing, interface unchanged
HealthConnectClient — pre-existing dependency (androidx.health.connect:connect-client)

## Conventions

§1 · Health Connect is phone-only, never used on the watch
§3 · a platform adapter touching Health Connect lives in the application module using it
§14 · sensor and sync code is tested against fakes, never real hardware in CI
