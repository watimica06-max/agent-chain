- Every text on the watch renders two to three times too large. The
  spec gives the type scale in pixels on a 480×480 face — `w-display`
  110, `w-value` 48, `w-title` 33, down to `w-caption` 18 — and
  `DesignTokens.Typography.Watch` declares those same numbers in `sp`.
  A pixel is not a scaled pixel: on a 340 dpi face one `sp` covers
  2.125 pixels, so `110.sp` draws at 234 pixels. Each token resolves at
  run time from the face's own width, so the drawing keeps its
  proportions on any watch: a token of N pixels renders at N times the
  face width over 480. Nothing about the values changes — only how they
  reach the screen.

- The paste screen's text field grows with what is pasted, and pushes
  the "Importer" button off the bottom of the screen where it can no
  longer be tapped. A pasted result runs to thirty rows; the field
  keeps a fixed height and scrolls its own content, and the button
  stays where it is.

- The four zone thresholds have no editing path. `ProfileViewModel`
  exposes handlers for the HR max, the expected distance and the
  long-press duration, each calling its `ProfileRepository` updater;
  none calls `updateZoneThreshold`. The profile screen edits the four
  thresholds inline, validated on loss of focus, the same way the three
  other settings already are — and a rejected value reverts, with a
  short message stating the constraint.

- The correction factor is never computed.
  `CorrectionFactorCalculator.compute` implements the formula and its
  guard-rail, and nothing calls it.
  Closing a RUN segment calls it with the segment's measured distance
  and the profile's expected distance, and appends the outcome — with
  the kilometre it came from — to the race's `retainedFactors` or
  `rejectedCalibrations`.

- The profile's correction factor is never updated at the end of a
  race. `ProfileRepository.updateCorrectionFactor` exists and nothing
  calls it: when a finished race holds retained factors, the last one's
  value becomes the profile's; when it holds none, the stored value is
  left unchanged.

- `WatchStringResources.RaceName.generated` formats a race name and
  nothing calls it, while `RaceRecordingRepositoryImpl.startClock`
  builds that name in code with `DisplayFormatter`. The name a
  recorded race carries comes from the text resources, like every
  other displayed string, and the formatter that duplicates it goes.

- The profile screen is unreachable. `PhoneNavigator.toProfile()`
  exists and no production code calls it; the race list's header
  renders its title and the "+" button, with no profile icon. The
  header carries that icon, next to the add button, and tapping it
  opens the profile.

- The race list has no empty state. `RaceListUiState` carries a list of
  races and nothing else, and no criterion observes the screen when it
  is empty — unlike the watch's history screen, whose empty state is
  tested. The screen shows the catalogue's empty-list message, and the
  action that opens the paste screen from there.

- The end-of-race screen never says a race is incomplete.
  `EndOfRaceUiState` carries no field for it, and the watch's text
  catalogue defines no message for it. A race stopped before its
  thirtieth segment is stated as incomplete on that screen.

- The paste error screen shows the row as pasted and nothing beside it.
  `PasteErrorUiState` carries `rawRow` and no field for the expected
  form the row should have taken. The screen shows both, side by side.

- The watch home screen has no sensor-permission reminder.
  `WatchStringResources.Permission.reminder` is declared and never
  read; `HomeViewModel` and `HomeUiState` reference
  `SensorPermissionManager` nowhere. The screen shows a reminder when
  sensor access is not granted, with an action that requests it again —
  or opens the system settings when the system no longer offers the
  prompt.

- The push of the profile and reference to the watch fires only from a
  button. `ProfileSyncPushService.push` is called from
  `ProfileViewModel.onSyncClicked` and nowhere else: nothing observes
  the link between the two devices becoming established. It fires there
  too, and a push refused or failed at that moment is retried at the
  next established link.

- The pull of recorded races from the watch fires only from a button.
  `RecordedRaceSyncService.sync` is called from
  `HomeViewModel.onSyncClicked` and nowhere else. It fires when the
  link is established too, and an attempt that stopped on a failure is
  retried at the next established link.
