## Intentions found

B1 Race segment structure — lot-01, `SegmentBlueprint`/`buildSegments` criteria
B2 Color tokens — lot-02, `DesignTokens.Color` criterion
B3 Typography tokens — lot-02, `DesignTokens.Typography` criteria
B4 Shape, spacing and zone-arc tokens — lot-02, `Shape`/`Spacing`/`ZoneArc` criteria
B5 Idle display token variants — lot-02, `DesignTokens.Idle` criterion
B6 Race list screen — lot-25, sort/reference/incomplete/add-button criteria
B7 Race detail screen — lot-26, 30-row/cycle-grouping/delta-visibility criteria
B8 Setting a race as the reference — lot-04 (`setAsReference`), lot-26 (`isSetReferenceVisible`)
B9 Renaming a race — lot-04 (trim/40-char rules), lot-26 (rename dialog flow)
B10 Deleting a race — lot-04 (delete, reference clears), lot-26 (confirm, back to previous screen — always RaceList in the stacks lot-24 builds)
B11 Paste-a-result screen — lot-27/lot-28, `isImportEnabled` criteria
B12 Reading and validating a pasted result — lot-18/lot-29, header-skip, scale, tab/space columns, 30-row and diff/order checks
B13 Preview before saving — lot-28, `ImportPreviewUiState`, Corriger/Enregistrer
B14 Saving an imported race — lot-04 (`saveImportedRace` criteria), lot-28 (wiring, opens detail directly)
B16 Profile screen (HR max, distance, long-press, sync) — lot-30, corresponding criteria
B17 Deriving maximum heart rate — lot-19, lot-30 (call-on-null-only, hand-entry precedence)
B18 Zone ranges from maximum heart rate — lot-07 (`determine`), lot-30 (`ranges()`)
B19 Editing profile settings (bounds, non-retroactive effect, long-press use) — lot-05 (validators, including the zone-threshold bounds), lot-15 (`longPressMs` use)
B20 Sensor permission request (first-launch, recheck, revocation, `requestAgain`) — lot-13, lot-31
B21 Waiting for the phone — lot-32, `hasReceivedProfile` criteria
B22 Home screen — lot-33, reference line/start/sync-state criteria
B23 Watch history screen — lot-34, read-only criteria
B24 Preparing and launching a race — lot-14, lot-35
B25 Starting when another app holds the sensor — lot-14 (`SensorConflict`), lot-35 (dialog wiring), lot-20 (`DeviceSlotTaken`)
B26 Resuming our own already-active race — lot-14 (`Resuming`, no session reopen), lot-35 (routes to MAIN)
B27 Marking a segment — lot-15 (press/slide/vibration), lot-23 (auto-return), lot-05 (`longPressMs` bounds)
B28 Main page, adapting to the current segment — lot-36, RUN/STATION/ROXZONE/segment-30 criteria
B29 Data freshness on the race pages — lot-03, lot-36 (10s fallback wiring), lot-40 (same threshold in power-save)
B30 Projection page — lot-37, delta/arrival/elapsed/position criteria
B31 Control page — lot-38, undo/stop layout and actions
B32 Undoing the last marking — lot-16, lot-38 (wiring)
B33 Stopping the race — lot-17, lot-38 (confirmation wiring)
B34 End-of-race screen — lot-39, total/delta/date-time/Terminer criteria
B35 Always-on display during the race — lot-40, mode/refresh-interval criteria
B36 allure-segment and allure-lissee — lot-08, lot-36 (baseline reset, only-RUN usage)
B39 Lap delta — lot-09, lot-36 (wiring)
B40 Cumulative delta and estimated arrival — lot-10, lot-37/lot-39 (wiring)
B41 Trend arrow — lot-11, lot-36 (wiring)
B42 Zone switching hysteresis — lot-07, lot-36 (wiring)
B45 Exercise session lifecycle — lot-20, lot-14, lot-39 (close), lot-41 (complication)
B46 Monotonic timing and recovery — lot-06, `findInProgress`/atomic-write criteria
B47 Duration formats — lot-42, `formatDurationSegment`/`Total`/`Elapsed`
B48 Delta format — lot-42, `formatDelta`
B49 Pace, heart rate, position and zone formats — lot-42
B50 Settings and range formats — lot-42
B51 Date formats — lot-42, `formatDate`/`formatDateTime`
B52 Rounding rule — lot-12, lot-26 (truncated-then-subtracted delta)
B53 Text resource rules — lot-43/lot-44, typed resource functions
B54 Dynamic texts and fallbacks (reference line, badge fallbacks, undo label, sync-date wording, delete title, zone-row hiding, failure catalogue) — lot-43/lot-44 (interpolated templates), lot-04 (name trim/cap), lot-36 (zone hidden without reading)
B55 Relative date wording — lot-42, `formatDateRelative`
B56 Fixed text catalogue — lot-43/lot-44, full catalogue criteria
B57 Phone navigation map — lot-24, lot-25/26/27/28/29 (wiring), back-stack collapse after import
B58 Watch navigation map — lot-23, lot-31/32/33/35/36/37/38/39 (wiring)
B59 Measured and displayed physiological data — unchanged scope boundary, nothing to build
B60 Heart-rate data consent — unchanged, relies solely on B17/B20 permissions, nothing to build
B61 Connectivity permission denied — lot-45, lot-30 (phone wiring), lot-33 (checked-at-launch, "Aucune référence" fallback)

## Intentions missing

B15 Paste error screen — the row as pasted must show alongside its illustrated expected form (in ahead); `PasteErrorUiState` (lot-29) carries only `rawRow`, no field for the expected-form illustration

B16 Profile screen / B19 Editing profile settings — the four zone thresholds are described as inline-edited fields validated on loss of focus; `ProfileViewModel` (lot-30) wires `hrMax`/`distance`/`longPress` handlers only, with no handler calling `ProfileRepository.updateZoneThreshold`

B20 Sensor permission request — the home-screen reminder that re-requests sensor access, or opens settings when the system no longer offers the prompt, is described; `HomeViewModel`/`HomeUiState` (lot-33) hold no field or handler referencing `SensorPermissionManager`

B37 Computing the correction factor — described as triggered "at the end of each kilometre"; no sheet calls `CorrectionFactorCalculator.compute` from a closing RUN segment, and no sheet writes its outcome into `Race.retainedFactors`/`rejectedCalibrations`

B38 Starting factor and fallback — the profile's `correctionFactor` is described as updated at the end of every race; no sheet calls `ProfileRepository.updateCorrectionFactor` from an ending race (lot-39's `EndOfRaceViewModel` does not)

B43 Sending profile and reference to the watch — the push described as triggering "automatically as soon as the link between the two devices is established"; every sheet only shows the manual, button-triggered push (lot-30/lot-33), with no listener tied to a connectivity event, and no retry-at-next-connection path for a refused push

B44 Receiving recorded races from the watch — the pull described as happening "automatically as soon as the link is established"; only the manual "Synchroniser" trigger (lot-33) is wired, with no retry-at-next-connection path for a failed attempt

B54 Dynamic texts and fallbacks — the watch-generated race name is described as applied automatically when a race is recorded on the watch; `WatchStringResources.RaceName.generated` (lot-44) is verified only as a pure formatter, and no sheet shows a watch race's `name` field ever assigned from it — `RaceRecordingRepository.startClock` (lot-06) and `RaceLaunchController.launch` (lot-14) take no name and produce none, though lot-06 lists `WatchStringResources` as a dependency it never otherwise uses

## Doubts

B12 Reading and validating a pasted result — the explicit station-label mapping table (Burpee BJ→Burpee Broad Jump, Row→Rameur, F. Carry→Farmers Carry, S. Lunges→Sandbag Lunges) is named only in lot-18's dependency note; no acceptance criterion in lot-18 or lot-29 observes a specific abbreviation resolving to its mapped station

B37 Computing the correction factor — described as stored "along with the kilometre number it came from"; lot-08's criteria show `RetainedFactor`/`RejectedCalibration` carrying a `station`, and neither lot-04 nor lot-08 declares that type's own fields, leaving unclear whether a kilometre number is present

B58 Watch navigation map — the sequencing between the permission screen, the waiting-for-phone screen and the home screen at first launch is described; `WatchDestination` (lot-23) holds no state for either screen, and no sheet shows what selects among `SensorPermissionScreen`/`WaitingForPhoneScreen`/`HomeScreen`
