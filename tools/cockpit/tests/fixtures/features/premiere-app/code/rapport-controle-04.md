## Intentions found

B1 Race segment structure — lot-01
B2 Color tokens — lot-02
B3 Typography tokens — lot-02
B4 Shape, spacing and zone-arc tokens — lot-02
B5 Idle display token variants — lot-02
B6 Race list screen — lot-25
B7 Race detail screen — lot-26
B8 Setting a race as the reference — lot-04, lot-26
B9 Renaming a race — lot-04, lot-26
B10 Deleting a race — lot-04, lot-26
B11 Paste-a-result screen — lot-27, lot-28
B12 Reading and validating a pasted result — lot-18, lot-29
B13 Preview before saving — lot-28
B14 Saving an imported race — lot-04, lot-28
B15 Paste error screen — lot-29, lot-43
B17 Deriving maximum heart rate — lot-19, lot-30
B18 Zone ranges from maximum heart rate — lot-07, lot-30
B21 Waiting for the phone — lot-32
B22 Home screen — lot-33
B23 Watch history screen — lot-34
B24 Preparing and launching a race — lot-14, lot-35
B25 Starting when another app holds the sensor — lot-14, lot-35
B26 Resuming our own already-active race — lot-14, lot-35
B27 Marking a segment — lot-15, lot-36, lot-39
B28 Main page, adapting to the current segment — lot-36
B29 Data freshness on the race pages — lot-03, lot-36
B30 Projection page — lot-09, lot-10, lot-37
B31 Control page — lot-38
B32 Undoing the last marking — lot-16, lot-38
B33 Stopping the race — lot-16, lot-17, lot-38
B34 End-of-race screen — lot-39
B36 allure-segment and allure-lissee — lot-08
B39 Lap delta — lot-09
B40 Cumulative delta and estimated arrival — lot-10, lot-37
B41 Trend arrow — lot-11, lot-36
B42 Zone switching hysteresis — lot-07
B45 Exercise session lifecycle — lot-14, lot-20, lot-42
B46 Monotonic timing and recovery — lot-06
B47 Duration formats — lot-42
B48 Delta format — lot-42
B49 Pace, heart rate, position and zone formats — lot-42
B50 Settings and range formats — lot-42
B51 Date formats — lot-42
B52 Rounding rule — lot-12
B53 Text resource rules — lot-43, lot-44
B54 Dynamic texts and fallbacks — lot-04, lot-36, lot-43, lot-44
B55 Relative date wording — lot-30, lot-42
B56 Fixed text catalogue — lot-43, lot-44
B58 Watch navigation map — lot-14, lot-23, lot-31, lot-32, lot-33, lot-34, lot-35, lot-36, lot-37, lot-38, lot-39
B59 Measured and displayed physiological data — unchanged, no calorie, step, cadence, altitude or route feature appears in any sheet
B60 Heart-rate data consent — carried by B17/B20's permissions; no sheet adds a consent step or an export path for heart-rate data
B61 Connectivity permission denied — lot-30, lot-33, lot-45

## Intentions missing

B16 Profile screen / B19 Editing profile settings — ProfileViewModel (lot-30) wires onHrMaxUpdated, onExpectedDistanceChanged and onLongPressChanged only; no handler anywhere calls ProfileRepository.updateZoneThreshold (lot-05), so the four zone-threshold fields the screen describes have no editing path; no sheet also describes the reject-and-revert-with-message behaviour B19 requires when any of the four settings is rejected

B20 Sensor permission request — WatchStringResources.Permission.reminder (lot-44) is declared but never read by any sheet; no criterion renders the home-screen reminder badge or calls SensorPermissionManager.requestAgain from the home screen after a refusal or revocation

B37 Computing the correction factor — CorrectionFactorCalculator.compute (lot-08) is never called by any race-tracking sheet at a kilometre's close; no sheet writes a Retained or Rejected outcome into a race's retainedFactors or rejectedCalibrations

B38 Starting factor and fallback — ProfileRepository.updateCorrectionFactor (lot-05) is never called at the end of a race; EndOfRaceViewModel (lot-39) does not call it, so the profile's starting factor is never actually updated from a race's own calibration

B43 Sending profile and reference to the watch — ProfileSyncPushService.push (lot-21) is only ever called from ProfileViewModel.onSyncClicked (lot-30), a manual button; no sheet triggers a push automatically once the link between the two devices is established; HomeViewModel (lot-33) also exposes no last-successful-sync date, though this block states that date is visible on the watch too

B44 Receiving recorded races from the watch — RecordedRaceSyncService.sync (lot-22) is only ever called from HomeViewModel.onSyncClicked (lot-33), a manual button; no sheet triggers a pull automatically once the link between the two devices is established

B57 Phone navigation map — PhoneNavigator.toProfile() (lot-24) is tested in isolation only; RaceListViewModel (lot-25) exposes no handler observing a tap on the header's profile icon, so no sheet calls it

## Doubts

B35 Always-on display during the race — AlwaysOnDisplayController (lot-40) covers the power-save mode switch and its refresh interval only; no criterion anywhere states that an available value stays shown, dimmed, in power-save mode rather than being replaced by a dash, so it is unclear whether this stated deviation from the platform's own guidance is actually built
