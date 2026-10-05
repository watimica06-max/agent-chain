## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

## §2 Persistence

## §3 Calculation

### §3.1 Watch typography renders at scaled-pixel size instead of the spec's pixel scale

Bearer: DesignTokens.Typography.Watch

DesignTokens.Typography.Watch declares its nine type-scale constants as
fixed `.sp` values, so each renders at the device's scaled-pixel
resolution instead of the pixel figures the spec's type scale names.
Each token resolves at render time from the watch face's own width, so
a token of N pixels renders at N times the face width over 480 pixels,
converted to the `sp` a `Text`'s `fontSize` expects, on any watch.

## §4 Transition

## §5 External source

## §6 Synchronisation

## §7 Background work

## §8 Journey

### §8.1 The profile screen is unreachable from the race list

Bearer: RaceListViewModel

`PhoneNavigator.toProfile()` exists and `RaceListHeader` renders only
the screen title and the "+" button, with no profile icon and nothing
calling it. `RaceListHeader` renders a profile icon next to the "+"
button, backed by a new `PhoneStringResources.RaceList` entry since the
screen carries no icon glyph today, and tapping it calls a new
`RaceListViewModel.onProfileClicked`, which calls `navigator.toProfile()`.

## §9 Screen

### §9.1 The paste screen's growing text field pushes the Importer action off screen

Bearer: PasteResultScreen

The `pastedText` `TextField` in `PasteResultScreen` grows to fit the
pasted content and pushes the "Importer" action below the bottom of the
screen, where it cannot be tapped. The `TextField` keeps a fixed height
and scrolls its own content once the pasted text exceeds it, so the
race name field, the date, and the "Importer" action keep a fixed,
reachable position regardless of how many rows are pasted.

### §9.2 A rejected zone-threshold or other profile setting is never reverted or explained

Bearer: ProfileViewModel

`ProfileViewModel`'s four settings handlers call their
`ProfileRepository` updater but discard the returned `Result`, so a
rejected value is never reverted on the profile screen and no
constraint message is shown; `ProfileUiState` carries no field for a
per-field rejection message and no `PhoneStringResources.Profile` entry
names the violated constraints. Losing focus on any of the four
settings inspects the returned `Result`, reverts the field's displayed
value to the profile's last stored value and shows a short message
naming the violated constraint on failure, drawn from a new
`PhoneStringResources.Profile` entry, cleared on the next successful
edit of the same field.

### §9.3 The race list's empty state has no standalone, testable criterion

Bearer: RaceListScreen

`RaceListScreen` renders its empty state from an inline
`uiState.races.isEmpty()` check, with no standalone function a test can
exercise, unlike `WatchHistoryScreen`'s `isHistoryEmpty`. `RaceListScreen`
exposes its empty-state switch as a standalone, testable criterion
mirroring `WatchHistoryScreen.isHistoryEmpty`, true when
`RaceListUiState.races` is empty and false when it holds at least one
race, while the rendered empty state itself — the catalogue's title,
body and the action opening the paste screen — stays unchanged.

### §9.4 The end-of-race screen never states a race is incomplete

Bearer: EndOfRaceViewModel

`EndOfRaceViewModel.computeState` never reads `Race.completion`, so
`EndOfRaceUiState` carries no field for an incomplete race and no
message key exists for it in the watch's text catalogue.
`computeState` reads `finalRace.completion`, and when it is
`INCOMPLETE`, `EndOfRaceUiState` carries that fact and
`EndOfRaceScreen` renders a dedicated message, drawn from a new string
resource, stating the race is incomplete.

## §10 Text

## §11 Access

## §12 Lifecycle

## Gaps set aside

- Correction factor computation: `RaceRecordingRepositoryImpl.markSegment`
  already calls `CorrectionFactorCalculator.compute` when closing a RUN
  segment and appends the outcome, with its kilometre, to
  `retainedFactors` or `rejectedCalibrations`.
- Profile correction factor update at end of race: `EndOfRaceViewModel.init`
  already calls `ProfileRepository.updateCorrectionFactor` with the last
  retained factor's value, guarded to leave the stored value unchanged
  when the finished race holds none.
- Race-name resource duplication: `WatchStringResources.RaceName` no
  longer exists — removed in bugfix-02/lot-17 for the same duplication
  this gap describes; `RaceRecordingRepositoryImpl.startClock` names
  races via `DisplayFormatter.formatDateTime` by design, recorded as
  the current shape in `CURRENT_TECHNICAL_STATE.md`.
- Paste error screen showing only the raw row: `PasteErrorUiState`
  already carries `expectedRow` beside `rawRow`, and `PasteErrorScreen`
  already renders both side by side, guarded by `rendersRowComparison`.
- Watch home screen sensor-permission reminder: `HomeViewModel` and
  `HomeUiState` already implement the reminder, its visibility from
  `SensorPermissionManager.isGranted()`, its click action requesting
  access again, and the redirect-to-settings fallback.
- Profile push retried on link established: `ProfileViewModel.init`
  already collects `linkStateMonitor.observeLinkEstablished()` and
  re-runs `pushProfile` on each emission, so a push refused or failed
  is retried at the next established link.
- Recorded-race pull retried on link established: `HomeViewModel`
  already calls `RecordedRaceSyncService.sync` on
  `linkStateMonitor.observeLinkEstablished()`, and a race whose send
  failed stays in `observeRecorded()` until acknowledged, so it is
  retried at the next established link.
