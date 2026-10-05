## Symbols

PlatformModule.provideHealthConnectClient — modified, now returns
  HealthConnectClient?, gated on HealthConnectClient.getSdkStatus
PlatformModule.provideHrHistoryReader — modified, parameter now
  HealthConnectClient?
HrHistoryReaderImpl — modified, constructor parameter now
  HealthConnectClient?
HrHistoryReaderImpl.bpmValuesOverLast12Months — modified body, empty on
  an absent client, logs (Log.e) and answers empty on a caught read
  failure, still rethrows CancellationException
MainActivity.healthConnectClient — modified, now HealthConnectClient?
  (@JvmField @Inject var, no longer lateinit); MainActivity.onCreate
  binds hrPermissionHost only when non-null
ActivityBoundHrPermissionHost.bind — unchanged
HrPermissionSystemImpl — unchanged

## Build

analyze: clean (no ktlint/detekt task wired in this project yet)
test: :app-phone:check exits 0 — all existing tests plus the new ones
  pass (PlatformModuleTest, HrHistoryReaderImplTest additions,
  MainActivityWithoutHealthConnectClientTest,
  MainActivityWithHealthConnectClientBoundTest)

## State

Added: PlatformModuleTest (app-phone/src/test/java/com/mgilli/hyroxtracker/di/PlatformModuleTest.kt)
Added: MainActivityWithoutHealthConnectClientTest,
  MainActivityWithHealthConnectClientBoundTest
  (app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityHealthConnectTest.kt)
Added: FakePlatformModule.fakeHealthConnectClient — mutable seam
  FakePlatformModule.provideHealthConnectClient reads, default identical
  to its former hardcoded value; a test needing a different one sets it
  in an init block and restores it in @After
Removed: —

## Requests

architecte/realisateur-lot-28.md
