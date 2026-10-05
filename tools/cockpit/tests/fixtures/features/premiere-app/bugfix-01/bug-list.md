- The paste error screen shows the row as pasted, but not the
  illustrated expected form beside it. `PasteErrorUiState` carries
  `rawRow` and nothing for the expected form.

- The profile screen edits the HR max, the expected distance and the
  long-press duration inline, validated on loss of focus. The four zone
  thresholds are described the same way and have no handler:
  `ProfileViewModel` never calls `ProfileRepository.updateZoneThreshold`.

- The watch home screen shows no reminder to re-request sensor access,
  nor a way to open the system settings when the prompt is no longer
  offered. `HomeViewModel` and `HomeUiState` never reference
  `SensorPermissionManager`.

- The correction factor is never computed. It should be, at the end of
  each kilometre, from a closing RUN segment, and its outcome written
  into the race's `retainedFactors` or `rejectedCalibrations` along
  with the kilometre it came from — `RetainedFactor` and
  `RejectedCalibration` carry a station today, and it is unclear
  whether the kilometre is there.

- The profile's `correctionFactor` is never updated at the end of a
  race. `EndOfRaceViewModel` never calls
  `ProfileRepository.updateCorrectionFactor`.

- The push of the profile and the reference to the watch is only ever
  triggered by hand, from the button. It should also fire as soon as
  the link between the two devices is established, and a refused push
  should be retried at the next connection.

- The pull of recorded races from the watch is only ever triggered by
  hand, from the "Synchroniser" action. It should also fire as soon as
  the link is established, and a failed attempt should be retried at
  the next connection.

- Nothing selects between the sensor permission screen, the
  waiting-for-phone screen and the home screen at first launch on the
  watch. `WatchDestination` holds no state for the first two.
