## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

## §2 Persistence

## §3 Calculation

## §4 Transition

### §4.1 Correction factor never computed on a closing RUN segment

Bearer: RaceRecordingRepositoryImpl

`RaceRecordingRepositoryImpl.markSegment` closes the current segment
and writes its duration without ever calling
`CorrectionFactorCalculator.compute`; `race.retainedFactors` and
`race.rejectedCalibrations` stay empty for the whole race, and neither
`RetainedFactor` nor `RejectedCalibration` records the kilometre a
computation came from. Closing a RUN segment calls `compute` with the
segment's measured distance and the profile's expected distance, and
appends the resulting outcome — along with the kilometre it came
from — to `race.retainedFactors` or `race.rejectedCalibrations`.

### §4.2 Profile's correction factor never updated at the end of a race

Bearer: EndOfRaceViewModel

`EndOfRaceViewModel` has no `ProfileRepository` dependency and never
calls `ProfileRepository.updateCorrectionFactor`, so a race's retained
factors never carry into the profile. When the finished race's
`retainedFactors` is not empty, `EndOfRaceViewModel` calls
`ProfileRepository.updateCorrectionFactor` with the last retained
factor's value; when it is empty, the profile's stored
`correctionFactor` is left unchanged.

## §5 External source

## §6 Synchronisation

### §6.1 Profile and reference push only triggered by hand

Bearer: ProfileViewModel

`ProfileViewModel.onSyncClicked` is the only caller of
`ProfileSyncPushService.push`, fired solely by the "Synchroniser avec
la montre"/"Réessayer" tap; nothing observes the phone-watch link
becoming established, and a failed push stays failed until the user
taps again. Establishing the link between the phone and the watch also
calls `ProfileSyncPushService.push` without a button tap, and a push
refused or failed at that point is retried automatically the next time
the link is established.

### §6.2 Pull of recorded races only triggered by hand

Bearer: HomeViewModel

`HomeViewModel.onSyncClicked` is the only caller of
`RecordedRaceSyncService.sync`, fired solely by the "Synchroniser" tap
on the watch's home screen; nothing observes the phone-watch link
becoming established, and a pull that stopped on a failure stays
failed until the user taps again. Establishing the link between the
phone and the watch also calls `RecordedRaceSyncService.sync` without
a button tap, and a pull that stopped on a send or save failure at
that point is retried automatically the next time the link is
established.

## §7 Background work

## §8 Journey

### §8.1 No screen selection at first launch on the watch

Bearer: WatchDestination / WatchRaceNavigator

`WatchDestination` holds no state for the sensor permission screen or
the waiting-for-phone screen, and `WatchRaceNavigator.current` always
starts on `WatchDestination.HOME`, even though `SensorPermissionScreen`
and `WaitingForPhoneScreen` each exist and work on their own.
`WatchDestination` carries a state for each of those two screens, and
at first launch the navigator picks among the permission screen, the
waiting-for-phone screen and the home screen based on whether sensor
permission is already granted and whether a profile has already
synced, instead of always starting on HOME.

## §9 Screen

### §9.1 Paste error screen shows no illustrated expected form

Bearer: PasteErrorUiState

`PasteErrorUiState` carries only `title`, `body` and `rawRow`, and
`PasteErrorScreen` renders `rawRow` as the row-as-pasted text with no
counterpart showing an illustrated expected form beside it.
`PasteErrorUiState` carries a field for the illustrated expected form
alongside `rawRow`, populated by `PasteErrorViewModel.buildUiState`
from the failure, and `PasteErrorScreen` renders it beside the row as
pasted whenever it is present.

### §9.2 Zone thresholds on the profile screen are not editable

Bearer: ProfileViewModel

`ProfileViewModel` exposes handlers for the HR max, the expected
distance and the long-press duration, each calling the matching
`ProfileRepository` updater, but exposes none for the zone thresholds
and `ZonesSection` in `ProfileScreen` only renders each threshold as
static text with no editable field. `ProfileViewModel` exposes a
handler that calls `ProfileRepository.updateZoneThreshold` for a given
zone index, and `ProfileScreen`'s `ZonesSection` presents each
threshold inline as an editable field, validated on loss of focus like
the distance and long-press fields, calling that handler.

## §10 Text

## §11 Access

### §11.1 No sensor permission reminder on the watch home screen

Bearer: HomeViewModel

`HomeViewModel` never references `SensorPermissionManager` and
`HomeUiState` carries no field for a sensor-access reminder, even
though `SensorPermissionManager.requestAgain()` exists to reopen the
system prompt or open the app's settings page. The home screen shows a
reminder when sensor access is not granted, and an action that calls
`SensorPermissionManager.requestAgain()`; `HomeUiState` carries the
state needed to render that reminder and `HomeViewModel` reads
`SensorPermissionManager`'s current state and exposes the action.

## §12 Lifecycle

## Gaps set aside

None — every gap listed in bug-list.md was confirmed against the code.
