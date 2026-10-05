## Intentions found

B1 Race segment structure — lot-01, SegmentBlueprint/buildSegments criteria
B2 Color tokens — lot-02, DesignTokens.Color criterion
B3 Typography tokens — lot-02, DesignTokens.Typography criteria
B4 Shape, spacing and zone-arc tokens — lot-02, DesignTokens.Shape/Spacing/ZoneArc criteria
B5 Idle display token variants — lot-02, DesignTokens.Idle criterion
B7 Race detail screen — lot-26, RaceDetailUiState criteria
B8 Setting a race as the reference — lot-04 setAsReference, lot-26 isSetReferenceVisible
B9 Renaming a race — lot-04 rename, lot-26 rename dialog criteria
B10 Deleting a race — lot-04 delete, lot-21 push excludes deleted races, lot-26 onDeleteConfirmed
B11 Paste-a-result screen — lot-28, isImportEnabled criteria
B13 Preview before saving — lot-28, ImportPreviewUiState/onCorrectClicked/onSaveClicked
B14 Saving an imported race — lot-04 saveImportedRace, lot-28 onSaveClicked
B15 Paste error screen — lot-29, 8-cause catalogue and PasteErrorUiState criteria
B17 Deriving maximum heart rate — lot-19 HrMaxDerivationService, lot-30 wiring criteria
B18 Zone ranges from maximum heart rate — lot-07/lot-30 ranges() criteria
B21 Waiting for the phone — lot-32, WaitingForPhoneUiState criteria
B22 Home screen — lot-33, HomeUiState criteria
B23 Watch history screen — lot-34, read-only criteria
B24 Preparing and launching a race — lot-14/lot-35 criteria
B25 Starting when another app holds the sensor — lot-14/lot-35 SensorConflict criteria
B26 Resuming our own already-active race — lot-14/lot-35 Resuming criteria
B27 Marking a segment — lot-15, lot-23 onMarked, lot-36/lot-37 onPressEnd
B28 Main page, adapting to the current segment — lot-36, MainRacePageUiState criteria
B29 Data freshness on the race pages — lot-03 SensorFreshnessWindow, lot-36 freshness criteria
B30 Projection page — lot-37, ProjectionUiState criteria
B31 Control page — lot-38, ControlUiState criteria
B32 Undoing the last marking — lot-16 undoLastMark, lot-38 wiring
B33 Stopping the race — lot-16/lot-17/lot-38 criteria
B35 Always-on display during the race — lot-02 Idle tokens, lot-40 AlwaysOnDisplayController
B36 allure-segment and allure-lissee — lot-08, PaceCalculator criteria
B39 Lap delta — lot-09, LapDeltaCalculator criteria
B40 Cumulative delta and estimated arrival — lot-10, lot-37, lot-39 finalDelta
B41 Trend arrow — lot-11, lot-36 wiring
B42 Zone switching hysteresis — lot-07, HeartRateZoneCalculator.determine criteria
B43 Sending profile and reference to the watch — lot-21, lot-30 onSyncClicked
B44 Receiving recorded races from the watch — lot-22, lot-33 onSyncClicked
B45 Exercise session lifecycle — lot-14/lot-20/lot-41 criteria
B46 Monotonic timing and recovery — lot-06, startClock/markSegment/findInProgress criteria
B47 Duration formats — lot-42, formatDurationSegment/Total/Elapsed
B48 Delta format — lot-42, formatDelta criteria
B49 Pace, heart rate, position and zone formats — lot-42, criteria
B50 Settings and range formats — lot-42, criteria
B51 Date formats — lot-42/lot-30, formatDate/formatDateTime/lastSyncToday/lastSyncYesterday
B52 Rounding rule — lot-12/lot-09/lot-10/lot-26, truncation criteria
B53 Text resource rules — lot-43/lot-44, catalogue criteria
B55 Relative date wording — lot-42/lot-30, formatDateRelative criteria
B56 Fixed text catalogue — lot-43/lot-44, catalogue criteria
B57 Phone navigation map — lot-24, PhoneNavigator criteria
B59 Measured and displayed physiological data — unchanged, nothing to build: no calorie/step/cadence/altitude/route field appears in any sheet
B60 Heart-rate data consent — unchanged, nothing to build: no sheet's sync payload (ProfileSyncPayload, RaceHistoryEntry, RecordedRacePayload) carries a heart-rate reading
B61 Connectivity permission denied — lot-45/lot-30, ConnectivityPermissionManager and ProfileViewModel wiring

## Intentions missing

B6 Race list screen — the empty-list message ("Aucune course encore" catalogue, block B56) has string resources in lot-43, but RaceListUiState (lot-25) carries only a `races` list, and no criterion observes the screen switching to that empty state — unlike the watch's WatchHistoryScreen (lot-34), whose empty state is explicitly criterion-tested

B16 Profile screen / B19 Editing profile settings — described as four inline-edited settings (zone thresholds, distance, long-press) each validated on loss of focus, reverting with a short message on rejection; `ProfileViewModel` (lot-30) wires `onHrMaxUpdated`/`onExpectedDistanceChanged`/`onLongPressChanged` only — no handler ever calls `ProfileRepository.updateZoneThreshold` (lot-05), and no sheet defines a validation-failure message shown on a rejected edit

B20 Sensor permission request — described as a reminder on the home screen that re-requests the sensor permission (or opens system settings); `WatchStringResources.Permission.reminder` exists (lot-44) but no sheet — `HomeViewModel` (lot-33) included — ever calls `SensorPermissionManager.requestAgain()`

B34 End-of-race screen — described as stating the race is incomplete when stopped before the 30th segment; `EndOfRaceUiState` (lot-39) carries no incomplete-status field, and `WatchStringResources.End` (lot-44) defines only `finish`, no incomplete-race message

B37 Computing the correction factor — `CorrectionFactorCalculator.compute` (lot-08) implements the formula and guard-rail, but no other sheet ever calls it during a race (not in lot-06's `markSegment`, not in lot-36's `MainRacePageViewModel`); `RetainedFactor`/`RejectedCalibration` (referenced by lot-04 and lot-08) are never given a field-level definition anywhere, so the "kilometre number it came from" is not carried by any signature

B38 Starting factor and fallback — `ProfileRepository.updateCorrectionFactor` exists (lot-05) with a persistence criterion, but no sheet ever calls it at the end of a race, so the profile's starting factor is never updated from a retained factor

B54 Dynamic texts and fallbacks — described as a watch-generated race name following the date-and-time format; `WatchStringResources.RaceName.generated` is defined (lot-44) but never invoked by any sheet — `RaceRecordingRepository.startClock` (lot-06) sets no name, and nothing supplies one before `saveRecordedRace` (lot-22) or `RecordedRaceSyncService.sync` (lot-22) send a race's name to the phone

## Doubts

B12 Reading and validating a pasted result — the explicit label-to-segment mapping table (Burpee BJ → Burpee Broad Jump, Row → Rameur, F. Carry → Farmers Carry, S. Lunges → Sandbag Lunges) and the "Rox In"/"Wall Balls In" state-machine reading are named only in lot-18's dependency note; no acceptance criterion in lot-18 or lot-29 exercises the mapping or the state-machine order directly, only the row-count/diff-sum/order-of-labels checks in general terms

B58 Watch navigation map — the first-launch sequencing (permission screen shown once, then waiting screen, then home) is not modeled by any signature: `SensorPermissionManager.onLaunch()` (lot-13), `WaitingForPhoneViewModel` (lot-32) and `HomeViewModel` (lot-33) each stand alone, and no sheet decides when the permission screen is skipped on a later launch
