## Signatures

PlatformModule.provideHealthConnectClient(
  @ApplicationContext context: Context
) → HealthConnectClient?
  — modification: today it returns a non-null `HealthConnectClient`
    from `HealthConnectClient.getOrCreate(context)` unconditionally.
    After: it reads `HealthConnectClient.getSdkStatus(context)` first
    and builds the client only on `HealthConnectClient.SDK_AVAILABLE`;
    every other status, and a status call that itself raises, yield
    null. Never raises, never calls `getOrCreate` on an unavailable
    SDK. Null means "Health Connect is not usable on this device",
    never "not yet loaded".

PlatformModule.provideHrHistoryReader(
  healthConnectClient: HealthConnectClient?
) → HrHistoryReader
  — modification: its parameter becomes nullable; it returns an
    `HrHistoryReaderImpl` over that client, present or absent. Never
    null, never raises.

HrHistoryReaderImpl(healthConnectClient: HealthConnectClient?)
  — modification: the constructor parameter becomes nullable.

HrHistoryReaderImpl.bpmValuesOverLast12Months() → List<Int>
  — modification of the body, not of the signature. Still `suspend`,
    still returning the beats-per-minute of every `HeartRateRecord`
    sample in the last 12 months, in the order Health Connect returns
    them, empty when there are none. After: empty when
    `healthConnectClient` is absent, without reaching Health Connect at
    all; empty when the read raises, and that raise is logged first —
    one record naming the operation and carrying the caught exception,
    carrying no bpm value. `CancellationException` is still rethrown
    before the catch that returns empty.

MainActivity.healthConnectClient: HealthConnectClient?
  — modification: the injected field becomes optional (`lateinit` no
    longer applies to it). `onCreate` still registers its
    `PermissionController.createRequestPermissionResultContract()`
    launcher unconditionally, and calls
    `hrPermissionHost.bind(healthConnectClient, hrPermissionLauncher)`
    only when the field is non-null. Absent a client it binds nothing
    and reaches `setContent` as it otherwise would.

ActivityBoundHrPermissionHost.bind(
  healthConnectClient: HealthConnectClient,
  launcher: ActivityResultLauncher<Set<String>>
) → Unit
HrPermissionSystemImpl(
  healthConnectClient: HealthConnectClient,
  launcher: ActivityResultLauncher<Set<String>>
)
  — unchanged. §5.2 places the skip in `MainActivity`, so neither is
    ever constructed or called with an absent client. Unbound,
    `ActivityBoundHrPermissionHost.isGranted()` and
    `requestPermission()` already answer false and launch nothing —
    that answer becomes the device-without-Health-Connect answer, and
    is the observation criterion 5 bears on.

## Acceptance criteria

- `provideHealthConnectClient` yields a non-null client when
  `getSdkStatus` answers `SDK_AVAILABLE`.
- `provideHealthConnectClient` yields null, and raises nothing, when
  `getSdkStatus` answers any other status.
- `provideHealthConnectClient` yields null, and raises nothing, when
  the `getSdkStatus` call itself raises.
- `MainActivity` created with no client injected reaches its first
  composed screen: `onCreate` completes and the race-list screen
  renders, with no exception thrown.
- `MainActivity` created with no client injected leaves the HR
  permission host unbound — `HrPermissionSystem.isGranted()` answers
  false and `requestPermission()` answers false without any permission
  request being launched.
- `MainActivity` created with a client injected binds the host —
  `HrPermissionSystem.isGranted()` answers what that client's
  `PermissionController.getGrantedPermissions()` reports.
- `HrHistoryReaderImpl` built with no client answers an empty list from
  `bpmValuesOverLast12Months()`, raises nothing, and reaches no Health
  Connect call.
- `HrHistoryReaderImpl` built with a client whose `readRecords` returns
  heart-rate records answers those records' sample values, unchanged.
- `HrHistoryReaderImpl` built with a client whose `readRecords` raises
  answers an empty list and emits one log record naming the read and
  carrying the caught exception.
- That log record carries no bpm value, no heart-rate sample and no
  date.
- `bpmValuesOverLast12Months()` cancelled mid-read propagates the
  `CancellationException` instead of answering an empty list and
  logging.

## Dependencies

HealthConnectClient, PermissionController, HealthPermission — Health
  Connect Client 1.1, a declared dependency (R65)
android.util.Log — Android framework
ActivityResultLauncher — AndroidX Activity, pre-existing
HrHistoryReader — pre-existing, `:core-domain`; its signature does not
  change here
HrPermissionSystem — pre-existing, `:core-domain`
ActivityBoundHrPermissionHost, HrPermissionSystemImpl — pre-existing,
  `:app-phone`; unchanged by this lot
HealthHistoryAvailability — produced by lot-19; carries the same
  `getSdkStatus == SDK_AVAILABLE` rule, including the raising-status
  case, but is `suspend`, so a Hilt `@Provides` cannot call it —
  `provideHealthConnectClient` reads the status itself, to that same
  rule
ProfileUiState.isHealthHistoryUnavailable — produced by lot-19, already
  written by `ProfileViewModel` from `HealthHistoryAvailability` and
  rendered by `ProfileScreen`; nothing further is needed here
FakePlatformModule — pre-existing test module, `@TestInstallIn`-
  replacing `PlatformModule`; it supplies a non-null
  `HealthConnectClient`, which satisfies a nullable injection site, so
  it needs no change
HrHistoryReaderImplTest — pre-existing, modified by this lot

## Conventions

R4 · `./gradlew check` exits 0 — the only definition of done
R13 · every access to Health Connect stays confined to `:app-phone`
R20 · missing data crosses a boundary as a nullable, no invented default
R30 · no empty and no generic catch
R33 · what a call needs before it can run at all is checked before, not
  caught after
R53 · no direct write to standard output — `android.util.Log`, ERROR
  for what needs a human
R54 · no data attached to a person in a log message, not even truncated
R55 · one nominal and one failure test per public function, in this lot
R63 · English identifiers and comments; every exported symbol carries
  one line saying what it guarantees and when it fails
R66 · no new dependency inside a lot
R81 · a unit test whose subject reaches `android.util.Log` carries
  `@RunWith(RobolectricTestRunner::class)` — `HrHistoryReaderImplTest`
  carries none today
R82 · a test failing on an unimplemented `android.*` stub is fixed in
  the test, never with `isReturnDefaultValues = true`

## Requests

—
