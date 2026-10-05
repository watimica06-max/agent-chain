## lot-01

Anchor: §1.1 — Race and segment structure
Needs: —
Produces: Segment (type routing RUN/ROXZONE_OUT/STATION/ROXZONE_IN/FINAL, the 30-slot cycle blueprint and station names, durationMs/cumulativeMs fields)
Modifies: —

## lot-02

Anchor: §1.2 — Design tokens
Needs: —
Produces: DesignTokens (color, typography, shape/spacing, zone-arc geometry and idle-mode variants, phone and watch variants)
Modifies: —

## lot-03

Anchor: §1.3 — Sensor-derived value freshness
Needs: —
Produces: SensorFreshnessWindow (10-second freshness/fallback policy for a displayed sensor-derived value)
Modifies: —

## lot-04

Anchor: §2.1 — Race record operations
Needs: Segment (lot-01)
Produces: RetainedFactor, RejectedCalibration, Race (id, name, date, origin, isReference, completion, 30 Segments, retainedFactors[]: List<RetainedFactor>, rejectedCalibrations[]: List<RejectedCalibration>, the in-progress fields of §2.3), RaceRepository (set as reference, rename, delete, save an imported race)
Modifies: —

## lot-05

Anchor: §2.2 — Profile persistence
Needs: —
Produces: Profile (hrMaxBpm, zoneThresholds[4], expectedDistanceM, longPressMs, correctionFactor, lastSyncSuccessAt), ProfileRepository (validated edits, correction-factor update)
Modifies: —

## lot-06

Anchor: §2.3 — Race clock persistence and recovery
Needs: Race (lot-04), WatchStringResources (lot-44, watch-generated race name)
Produces: RaceRecordingRepository (monotonic clock start, atomic segment-close/open write, currentSegmentIndex/currentSegmentOpenedAt persistence, resume-mid-race read)
Modifies: —

## lot-07

Anchor: §3.1 — Heart-rate zone determination
Needs: Profile (lot-05, zoneThresholds, hrMaxBpm), SensorPermissionManager (lot-13, permanent-fallback state)
Produces: HeartRateZoneCalculator (five-zone determination with hysteresis)
Modifies: —

## lot-08

Anchor: §3.2, §3.3 — Pace calculation and correction factor
Needs: Segment (lot-01), Profile (lot-05, expectedDistanceM, correctionFactor), RetainedFactor, RejectedCalibration (lot-04), RaceRecordingRepository (lot-06, kilometre-close trigger, retainedFactors[]/rejectedCalibrations[] recording), ProfileRepository (lot-05, correctionFactor update), Health Services distance/speed data (framework)
Produces: PaceCalculator (allure-segment, allure-lissee), CorrectionFactorCalculator (k, fills retainedFactors[]/rejectedCalibrations[])
Modifies: —

## lot-09

Anchor: §3.4 — Lap delta
Needs: PaceCalculator (lot-08, allure-segment), Race (lot-04, reference race's stored segment duration), Profile (lot-05, expectedDistanceM)
Produces: LapDeltaCalculator (temps_projeté, écart)
Modifies: —

## lot-10

Anchor: §3.5 — Cumulative delta and estimated arrival
Needs: LapDeltaCalculator (lot-09), Race (lot-04, reference race's stored segment durations), SegmentMarkingController (lot-15, per-marking recompute)
Produces: CumulativeDeltaEstimator (écart_cumulé, arrivée)
Modifies: —

## lot-11

Anchor: §3.6 — Trend arrow
Needs: PaceCalculator (lot-08, allure-lissee and allure-segment)
Produces: TrendArrowCalculator
Modifies: —

## lot-12

Anchor: §3.7 — Duration and delta truncation
Needs: Segment (lot-01)
Produces: DurationTruncationService (truncated segment/cumulative/delta values for display)
Modifies: —

## lot-13

Anchor: §4.1 — Sensor permission (watch)
Needs: —
Produces: SensorPermissionManager (first-launch request, per-launch recheck, revocation fallback, no auto-repeat)
Modifies: —

## lot-14

Anchor: §4.2 — Race launch sequence
Needs: RaceRecordingRepository (lot-06, resume-mid-race detection, clock start), Race (lot-04, reference-loaded check), ExerciseSessionManager (lot-20, exercise session open/retry, single-slot conflict), SensorPermissionManager (lot-13, heart-rate fallback during wait)
Produces: RaceLaunchController (preparation flow, open-failure retry, sensor-conflict resolution, resume detection)
Modifies: —

## lot-15

Anchor: §4.3 — Marking a segment
Needs: Profile (lot-05, longPressMs), RaceRecordingRepository (lot-06, atomic close/open write)
Produces: SegmentMarkingController (long-press detection, threshold/slide cancellation, vibration feedback)
Modifies: —

## lot-16

Anchor: §4.4 — Undoing the last marking
Needs: RaceRecordingRepository (lot-06, reopen the closed segment), SegmentMarkingController (lot-15, last-marking state)
Produces: UndoMarkingController
Modifies: —

## lot-17

Anchor: §4.5 — Stopping the race
Needs: RaceRecordingRepository (lot-06, cut clock, save as incomplete), ExerciseSessionManager (lot-20, stop the running session)
Produces: StopRaceController
Modifies: —

## lot-18

Anchor: §5.1 — Parsing and validating a pasted result
Needs: Segment (lot-01, station/label mapping)
Produces: HyresultResultParser (positional 4-column reading, state machine over the 7-cycle pattern, error catalogue mapping)
Modifies: —

## lot-19

Anchor: §5.2 — Deriving maximum heart rate from health history
Needs: ProfileRepository (lot-05)
Produces: HrMaxDerivationService (12-month health-history read, hand-entry precedence)
Modifies: —

## lot-20

Anchor: §5.3 — Exercise session and sensor data availability
Needs: —
Produces: ExerciseSessionManager (single exercise session per recorded race, per-type sensor-availability check, batched-while-non-interactive delivery)
Modifies: —

## lot-21

Anchor: §6.1 — Sending profile and reference to the watch
Needs: ProfileRepository (lot-05, the profile to push), ProfileRepository (lot-36, observe), Race (lot-04, reference race and 20-entry summarized history), RaceRepository (lot-25, observeAll — the source of the summarized history; the 20-entry cap and the {name, date, total} shape are its own concern, not the repository's), ConnectivityPermissionManager (lot-45)
Produces: ProfileSyncPushService (full-replace push, mid-race refusal handling, result state), WatchHistoryStore (the 20 {name, date, totalTime} entries the watch receives, replaced as a whole block on each push, with observe() to read them)
Modifies: RaceRepository (lot-04, replacing the reference race received on the watch side); ProfileRepository — ajout de markSyncSuccess(at)

## lot-22

Anchor: §6.2 — Receiving recorded races from the watch
Needs: Race (lot-04, phone-side save), RaceRecordingRepository (lot-06, watch-side recorded history and erase-after-confirm), RaceRepository (lot-04), ConnectivityPermissionManager (lot-45)
Produces: RecordedRaceSyncService (pushes recorded races to the phone, with a manual trigger and an observable state — in progress / failure / last-success date)
Modifies: RaceRecordingRepository (lot-06, adds observeRecorded() and eraseRecorded(raceId)); RaceRepository — ajout de saveRecordedRace(name, date, segments, completion)

§7 Background work — no lot: the section is empty.

## lot-23

Anchor: §8.1, §8.3 — Return to main page after marking or inactivity; watch navigation map
Needs: SegmentMarkingController (lot-15, marking and inactivity triggers)
Produces: WatchRaceNavigator (forward-only swipe chain, auto-return timer, disabled back gesture during the race, undo/stop/30th-marking routing)
Modifies: —

## lot-24

Anchor: §8.2 — Phone navigation map
Needs: —
Produces: PhoneNavigator (card-to-detail routing, paste/preview/error routing, back-stack rule after a successful import)
Modifies: —

## lot-25

Anchor: §9.1 — Race list screen (phone)
Needs: Race (lot-04), DurationTruncationService (lot-12), DesignTokens (lot-02), PhoneStringResources (lot-43), PhoneNavigator (lot-24)
Produces: RaceListScreen
Modifies: RaceRepository (lot-04, adds observeAll(), findById(), observeReference())

## lot-26

Anchor: §9.2 — Race detail screen (phone)
Needs: Race (lot-04), Segment (lot-01), LapDeltaCalculator (lot-09), DurationTruncationService (lot-12), DesignTokens (lot-02), PhoneStringResources (lot-43), PhoneNavigator (lot-24)
Produces: RaceDetailScreen
Modifies: PhoneStringResources (lot-43, adds segmentName(index) resolving a segment's display name)

## lot-27

Anchor: §9.3 — Paste-a-result screen (phone)
Needs: HyresultResultParser (lot-18), DesignTokens (lot-02), PhoneStringResources (lot-43), PhoneNavigator (lot-24)
Produces: PasteResultScreen
Modifies: —

## lot-28

Anchor: §9.4 — Import preview screen (phone)
Needs: HyresultResultParser (lot-18), Race (lot-04, save), DesignTokens (lot-02), PhoneStringResources (lot-43), PhoneNavigator (lot-24)
Produces: ImportPreviewScreen
Modifies: PasteResultScreen / PasteResultViewModel — ajout du champ date

## lot-29

Anchor: §9.5 — Paste error screen (phone)
Needs: HyresultResultParser (lot-18, failure cause and row), DesignTokens (lot-02), PhoneStringResources (lot-43), PhoneNavigator (lot-24)
Produces: PasteErrorScreen
Modifies: —

## lot-30

Anchor: §9.6, §9.18 — Profile screen (phone); connectivity-permission-denied state
Needs: Profile (lot-05), HeartRateZoneCalculator (lot-07, zone ranges), HrMaxDerivationService (lot-19), ProfileRepository (lot-21, observe), ConnectivityPermissionManager (lot-45), DesignTokens (lot-02), PhoneStringResources (lot-43), PhoneNavigator (lot-24)
Produces: ProfileScreen
Modifies: HeartRateZoneCalculator (lot-07, adds ranges(profile) returning the five zone bounds in % and bpm, independent of a reading); PhoneStringResources — ajout de Profile.lastSyncToday(time) et Profile.lastSyncYesterday(time)

## lot-31

Anchor: §9.7 — Sensor permission screen (watch)
Needs: SensorPermissionManager (lot-13), DesignTokens (lot-02), WatchStringResources (lot-44)
Produces: SensorPermissionScreen
Modifies: —

## lot-32

Anchor: §9.8 — Waiting-for-phone screen (watch)
Needs: ProfileRepository (lot-21, observe — null = never received), DesignTokens (lot-02), WatchStringResources (lot-44)
Produces: WaitingForPhoneScreen
Modifies: —

## lot-33

Anchor: §9.9, §9.18 — Home screen (watch); connectivity-permission-denied state
Needs: RaceRepository (lot-25, observeReference), ProfileRepository (lot-21, observe — lastSyncSuccessAt for the sync-result line), RecordedRaceSyncService (lot-22, sync trigger), ConnectivityPermissionManager (lot-45), DesignTokens (lot-02), WatchStringResources (lot-44), WatchRaceNavigator (lot-23)
Produces: HomeScreen (watch)
Modifies: —

## lot-34

Anchor: §9.10 — Watch history screen
Needs: WatchHistoryStore (lot-21), DesignTokens (lot-02), WatchStringResources (lot-44)
Produces: WatchHistoryScreen
Modifies: —

## lot-35

Anchor: §9.11 — Preparation and sensor-conflict screens (watch)
Needs: RaceLaunchController (lot-14), RaceRepository (lot-25, observeReference), DesignTokens (lot-02), WatchStringResources (lot-44), WatchRaceNavigator (lot-23)
Produces: PreparationScreen
Modifies: —

## lot-36

Anchor: §9.12 — Main race page (watch)
Needs: HeartRateZoneCalculator (lot-07), PaceCalculator (lot-08), LapDeltaCalculator (lot-09), TrendArrowCalculator (lot-11), SegmentMarkingController (lot-15), SensorFreshnessWindow (lot-03), SensorPermissionManager (lot-13), Race (lot-04, reference time), DurationTruncationService (lot-12), DesignTokens (lot-02), WatchRaceNavigator (lot-23)
Produces: MainRacePageScreen
Modifies: WatchStringResources (lot-44, adds segmentName(index)); ProfileRepository — ajout de observe()

## lot-37

Anchor: §9.13 — Projection page (watch)
Needs: CumulativeDeltaEstimator (lot-10), SegmentMarkingController (lot-15), DurationTruncationService (lot-12), DesignTokens (lot-02), WatchStringResources (lot-44), WatchRaceNavigator (lot-23), ProfileRepository (lot-36, observe)
Produces: ProjectionScreen
Modifies: —

## lot-38

Anchor: §9.14 — Control page (watch)
Needs: UndoMarkingController (lot-16), StopRaceController (lot-17), DesignTokens (lot-02), WatchStringResources (lot-44), WatchRaceNavigator (lot-23)
Produces: ControlScreen
Modifies: —

## lot-39

Anchor: §9.15 — End-of-race screen (watch)
Needs: RaceRecordingRepository (lot-06, save, generated name), CumulativeDeltaEstimator (lot-10, final delta), StopRaceController (lot-17, early-stop path), ExerciseSessionManager (lot-20, close session), DurationTruncationService (lot-12), DesignTokens (lot-02), WatchStringResources (lot-44), WatchRaceNavigator (lot-23)
Produces: EndOfRaceScreen
Modifies: CumulativeDeltaEstimator (lot-10, adds finalDelta(raceSegments, referenceSegments) — the cumulative delta at the last closed segment, signed, no current index or clamp)

## lot-40

Anchor: §9.16 — Always-on / power-save display (watch)
Needs: DesignTokens (lot-02, idle variants), SensorFreshnessWindow (lot-03, refresh cadence)
Produces: AlwaysOnDisplayController
Modifies: —

## lot-41

Anchor: §9.17 — Watch-face complication
Needs: WatchRaceNavigator (lot-23, current race page)
Produces: WatchComplicationEntry
Modifies: —

## lot-42

Anchor: §10.1 — Display formats
Needs: DurationTruncationService (lot-12)
Produces: DisplayFormatter (duration, delta, pace, hr, position, zone, percentage, range, distance, press-duration, date formats)
Modifies: —

## lot-43

Anchor: §10.2, §10.3, §10.4 — Resource file conventions, dynamic text templates and fixed text catalogue (phone)
Needs: —
Produces: PhoneStringResources (phone.* dynamic templates and fixed catalogue, including the failure catalogue)
Modifies: —

## lot-44

Anchor: §10.2, §10.3, §10.4 — Resource file conventions, dynamic text templates and fixed text catalogue (watch)
Needs: —
Produces: WatchStringResources (watch.* dynamic templates and fixed catalogue)
Modifies: —

§11.1 Heart-rate data consent — no lot: it relies solely on the sensor permission (§4.1) and health-history permission (§5.2) already built there; no consent step of the app's own.

## lot-45

Anchor: §11.2 — Connectivity permission denial
Needs: —
Produces: ConnectivityPermissionManager (pairing-permission request, per-launch recheck, revocation fallback, re-request/settings redirect)
Modifies: —

§12 Lifecycle — no lot: the section is empty.
