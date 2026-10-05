## Symbols

RaceRecordingRepositoryImpl
  markSegment — call CorrectionFactorCalculator.compute and append the
    outcome, with the kilometre it came from, to race.retainedFactors
    or race.rejectedCalibrations        §4.1

CorrectionFactorCalculator
  compute(station, previousFactor, expectedDistanceM, measuredDistanceM) §4.1

RetainedFactor
  carry the kilometre a computation came from  §4.1

RejectedCalibration
  carry the kilometre a computation came from  §4.1

EndOfRaceViewModel
  call ProfileRepository.updateCorrectionFactor with the last retained
    factor's value when the finished race's retainedFactors is not
    empty                                §4.2

ProfileRepository
  updateCorrectionFactor(value)          §4.2
  expectedDistanceM / correctionFactor, read for CorrectionFactorCalculator.compute §4.1
  updateZoneThreshold(index, value)      §9.2
  observe(), read for "profile already synced"  §8.1

ProfileViewModel
  call ProfileSyncPushService.push when the phone-watch link is
    established, no button tap needed    §6.1
  collect LinkStateMonitor.observeLinkEstablished() to trigger that call §6.1
  handler calling ProfileRepository.updateZoneThreshold for a given
    zone index                           §9.2

ProfileSyncPushService
  push(permissionGranted, at) — called on the link becoming established,
    and retried automatically on the next established link after a
    refused/failed push                  §6.1

LinkStateMonitor
  observeLinkEstablished(): Flow<Unit>, emitting only on the transition
    to established, never at startup if already established  §6.1, §6.2

HomeViewModel
  call RecordedRaceSyncService.sync when the phone-watch link is
    established, no button tap needed    §6.2
  collect LinkStateMonitor.observeLinkEstablished() to trigger that call §6.2
  show a reminder when sensor access is not granted, with an action
    calling SensorPermissionManager.requestAgain()  §11.1
  read SensorPermissionManager's current state       §11.1

RecordedRaceSyncService
  sync(raceInProgress, at) — called on the link becoming established,
    and retried automatically on the next established link after a
    send/save failure                    §6.2

WatchDestination
  a state for the sensor permission screen           §8.1
  a state for the waiting-for-phone screen            §8.1

WatchRaceNavigator
  current — at first launch, picks among the permission screen, the
    waiting-for-phone screen and the home screen, based on sensor
    permission granted and whether a profile has already synced  §8.1

SensorPermissionScreen
  reachable as the navigator's first-launch destination  §8.1

WaitingForPhoneScreen
  reachable as the navigator's first-launch destination  §8.1

SensorPermissionManager
  current granted state, read to pick the first-launch destination §8.1
  current state, read by HomeViewModel                §11.1
  requestAgain(), called by the home screen's reminder action  §11.1

PasteErrorUiState
  a field for the illustrated expected form, alongside rawRow  §9.1

PasteErrorViewModel
  buildUiState populates the illustrated-expected-form field from the
    failure                              §9.1

PasteErrorScreen
  renders the illustrated expected form beside the row as pasted,
    whenever present                     §9.1

ProfileScreen
  ZonesSection presents each zone threshold inline as an editable
    field, validated on loss of focus, calling ProfileViewModel's
    handler                              §9.2

HomeUiState
  state needed to render the sensor-access reminder  §11.1

HomeScreen
  renders the sensor-access reminder and its action from HomeUiState,
    whenever present                     §11.1

## lot-01

Anchor: §4.1 — Correction factor never computed on a closing RUN segment
Needs: CorrectionFactorCalculator (pre-existing), ProfileRepository (pre-existing)
Produces: —
Modifies: RaceRecordingRepositoryImpl, RetainedFactor, RejectedCalibration

## lot-02

Anchor: §4.2 — Profile's correction factor never updated at the end of a race
Needs: ProfileRepository (pre-existing)
Produces: —
Modifies: EndOfRaceViewModel

## lot-03

Anchor: §6.1 — Profile and reference push only triggered by hand; §6.2 — Pull of recorded races only triggered by hand
Needs: —
Produces: LinkStateMonitor, in :core-sync (collected by ProfileViewModel and HomeViewModel in lot-04 and lot-05)
Modifies: —

## lot-04

Anchor: §6.1 — Profile and reference push only triggered by hand; §9.2 — Zone thresholds on the profile screen are not editable
Needs: ProfileSyncPushService (pre-existing), LinkStateMonitor (lot-03), ProfileRepository (pre-existing)
Produces: —
Modifies: ProfileViewModel, ProfileScreen

## lot-05

Anchor: §6.2 — Pull of recorded races only triggered by hand; §11.1 — No sensor permission reminder on the watch home screen
Needs: RecordedRaceSyncService (pre-existing), LinkStateMonitor (lot-03), SensorPermissionManager (pre-existing)
Produces: —
Modifies: HomeViewModel, HomeUiState, HomeScreen

## lot-06

Anchor: §8.1 — No screen selection at first launch on the watch
Needs: SensorPermissionScreen (pre-existing), WaitingForPhoneScreen (pre-existing), SensorPermissionManager (pre-existing), ProfileRepository (pre-existing)
Produces: —
Modifies: WatchDestination, WatchRaceNavigator

## lot-07

Anchor: §9.1 — Paste error screen shows no illustrated expected form
Needs: —
Produces: —
Modifies: PasteErrorUiState, PasteErrorViewModel, PasteErrorScreen
