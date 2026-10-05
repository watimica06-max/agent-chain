## Signatures

MainRacePageViewModel — modification, constructor gains four parameters

    MainRacePageViewModel(
      @Assisted("initialRace") initialRace: Race,
      @Assisted("referenceRace") referenceRace: Race?,
      @Assisted profile: Profile,
      @Assisted sensorPermissionGranted: Boolean,
      markingController: SegmentMarkingController,
      navigator: WatchRaceNavigator,
      sensorReadingsSource: SensorReadingsSource,
      raceTicker: RaceTicker,
      raceRecordingRepository: RaceRecordingRepository,
      savedStateHandle: SavedStateHandle
    ) : ViewModel()
      — `@AssistedFactory Factory.create` keeps its four parameters
        unchanged; the four new ones are Hilt-provided (SensorModule
        already provides SensorReadingsSource and RaceTicker as
        singletons, so no DI module changes)
      — `init` collects, each on its own `viewModelScope.launch`:
        `sensorReadingsSource.heartRate()` → `onHeartRateReading`,
        `.distance()` → `onDistanceSample`, `.speed()` → `onSpeedSample`,
        `raceTicker.ticks` → `onTick`. It never calls `RaceTicker.start()`
        or `.stop()` — lot-45 owns those
      — `init` also re-reads the retained race:
        `raceRecordingRepository.findInProgress()` inside
        `viewModelScope.launch`; on success with a non-null race whose
        `id` equals the retained race id, that race replaces the held one
        and the state recomputes; on any other success the held race stays
        `initialRace`; on failure the held race stays `initialRace` and the
        failure is logged at ERROR naming the operation, carrying no
        reading, no zone and no duration

MainRacePageViewModel.onDisplayModeChanged — new

    onDisplayModeChanged(displayMode: DisplayMode) → Unit
      — records the current display mode and recomputes the state; the
        mode is not persisted, the screen re-supplies it on every entry.
        NORMAL is the mode in force until the first call

MainRacePageViewModel.onDistanceSample — modification, `speedMetersPerSecond` removed

    onDistanceSample(cumulativeDistanceM: Double, atElapsedRealtime: Long) → Unit
      — the sink for `SensorReadingsSource.distance()`, which carries no
        speed; records the cumulative distance and its instant, as today

MainRacePageViewModel.onSpeedSample — new

    onSpeedSample(speedMetersPerSecond: Double, atElapsedRealtime: Long) → Unit
      — the sink for `SensorReadingsSource.speed()`; appends one
        `SpeedSample` to the smoothing window `PaceCalculator.smoothedPace`
        reads

MainRacePageViewModel.onHeartRateReading, .onTick, .onPressEnd, .uiState —
unchanged signatures; `onTick(nowElapsedRealtime: Long)` is called from the
`raceTicker.ticks` collection with the monotonic instant read at that tick.

SensorValueDisplay — added to `MainRacePageUiState.kt` (§9.11's second gap)

    sealed interface SensorValueDisplay
      Fresh(text: String)    — inside its freshness window
      Stale(text: String)    — received, past its window, still shown
      Fallback               — nothing to show; renders exactly what
                               today's null renders, in both modes
      — `Stale` is reachable in POWER_SAVE only; in NORMAL a value past its
        window is `Fallback`, as today. It never expires: a value stays
        `Stale` for as long as it stays past its window, whatever the age
      — `sensorPermissionGranted == false` gives `Fallback` for the heart
        rate in both modes, never `Stale`

MainRacePageUiState — modification

    MainRacePageUiState(
      stationLabel: LabelRef?,
      top: RaceTopBlock,
      center: RaceCenterBlock,
      heartRate: SensorValueDisplay,
      zone: HeartRateZone?
    )
      — `heartRateText: String?` becomes `heartRate: SensorValueDisplay`
      — `zone` is the zone of the reading `heartRate` carries, `Fresh` or
        `Stale` alike; null when `heartRate` is `Fallback`

RaceCenterBlock.Pace — modification

    Pace(pace: SensorValueDisplay, trend: TrendArrow)
      — `paceText: String?` becomes `pace: SensorValueDisplay`, evaluated
        on the distance reading's own freshness; `trend` is unchanged and
        is `TrendArrow.None` whenever either pace is a fallback

MainRacePageScreen — modification, two parameters added

    @Composable
    MainRacePageScreen(
      viewModel: MainRacePageViewModel,
      displayMode: DisplayMode = DisplayMode.NORMAL,
      refreshIntervalMs: Long? = null
    )
      — forwards `displayMode`, and only it, to
        `viewModel.onDisplayModeChanged`, from an effect keyed on the
        value, never from the composition body
      — reads `refreshIntervalMs` as the cadence at which it refreshes its
        power-save layout while `displayMode == POWER_SAVE`, never as a
        freshness bound: a state emitted after the last refresh becomes
        visible when that many milliseconds have elapsed
      — `refreshIntervalMs == null`, or `displayMode == NORMAL`: every
        emission is rendered as it arrives, no cadence applies
      — renders the power-save layout — the already-declared
        `DesignTokens.Idle` opacities — while in POWER_SAVE, and the
        normal layout otherwise. A `SensorValueDisplay.Stale` value is
        rendered at a lower opacity than the same value as `Fresh`
      — both defaults exist so `WatchApp`'s existing call site, in this
        same module, keeps compiling; lot-49 passes both explicitly

## Acceptance criteria

- A heart-rate reading emitted on `SensorReadingsSource.heartRate()`, with
  no direct call on the ViewModel, shows that value on the page
- A distance reading emitted on `SensorReadingsSource.distance()`, with no
  direct call, shows the pace that distance and the segment's elapsed time
  imply
- With the same distance readings, speed samples emitted on
  `SensorReadingsSource.speed()` more than 2% faster than the segment pace
  render the up trend arrow, and slower ones the down arrow
- A tick emitted on `RaceTicker.ticks`, with no sensor emission, advances
  the rendered segment elapsed time
- Constructing the ViewModel returns before the repository read completes;
  the page shows the assisted race until that read comes back
- A `findInProgress()` success carrying the retained race id replaces the
  rendered race with the one read back
- A `findInProgress()` failure leaves the page on the assisted race and
  writes one ERROR log naming the operation, containing no reading, no
  zone, no duration and no race name
- After a saved-state rebuild, the page renders the same heart-rate value,
  pace, trend and segment elapsed time as before the rebuild
- In POWER_SAVE, a heart-rate value received and then past its freshness
  window is still shown, at a lower opacity than the same value while fresh
- In POWER_SAVE, that value is still shown a full minute after its window
  lapsed, dimmed, with no further reading
- In POWER_SAVE, a heart-rate value never received shows nothing — what an
  absent value shows today — and is not dimmed
- In POWER_SAVE, the pace value behaves the same three ways as the
  heart-rate value: shown, shown dimmed, absent
- In NORMAL, a value past its freshness window shows exactly what it shows
  today, dimmed nowhere
- With `sensorPermissionGranted == false`, the heart rate shows nothing in
  POWER_SAVE as in NORMAL, whatever has been received
- The screen renders the power-save layout when handed
  `displayMode = POWER_SAVE`, and the normal layout when handed NORMAL
- Handing the screen `POWER_SAVE` alone, with no other call, makes a
  stale-but-received value stay on screen — the mode reaches the ViewModel
- In POWER_SAVE with `refreshIntervalMs = N`, a state emitted just after a
  refresh is not visible before N milliseconds have elapsed, and is visible
  once they have
- In POWER_SAVE with `refreshIntervalMs = null`, and in NORMAL, every
  emitted state is visible without waiting

## Dependencies

MainRacePageViewModel, MainRacePageUiState, RaceCenterBlock,
MainRacePageScreen — pre-existing, modified by this lot
SensorReadingsSource, HeartRateReading, DistanceReading — produced by lot-46
RaceTicker — produced by lot-47
SegmentMarkingController, MarkingOutcome — modified by lot-43
PaceCalculator, PaceResult — modified by lot-04
SensorFreshnessWindow, Freshness — modified by lot-05
HeartRateZoneCalculator, HeartRateZone — modified by lot-06
WatchStringResources — modified by lot-18
RaceRecordingRepository — pre-existing; `findInProgress(): Result<Race?>`,
  not suspend at this point in the sequence, made suspend by lot-50, which
  names this ViewModel among its call sites. Not in lot-41's `Needs`:
  §12.2's second gap makes the retained race a re-read from the repository
DisplayMode, DesignTokens (`Idle`), WatchRaceNavigator, Race, Profile,
RaceCompletion, SegmentBlueprint, SegmentType, LabelRef, DisplayFormatter,
DurationTruncationService, LapDeltaCalculator, LapDeltaResult,
TrendArrowCalculator, TrendArrow, SpeedSample — pre-existing
SavedStateHandle, ViewModel, viewModelScope — androidx.lifecycle

## Conventions

§5 · R18 — data crossing a public boundary is immutable
§5 · R20 — missing data crosses as a nullable or a declared absence type
§5 · R22 — anything that computes states what it returns for every input it
  cannot compute on
§5 · R25 — what a signature promises, the body delivers
§6 · R34 — a caller that receives a failure acts on it
§6 · R79 — a failure carried nowhere is logged at ERROR
§7 · R41 — a §3 entry stays pure; what it reads from outside is passed in
§7 · R44 — one state holder per journey
§7 · R45 — a screen keeps what the user has in progress across a rebuild
§7 · R47 — a screen reads a source once per entry, never once per frame
§7 · R48 — what a module opens, that module's own scope releases
§7 · R49 — two clocks exist and they are two types
§9 · R53 — no direct write to standard output outside the entry point
§9 · R54 — no data attached to a person in a log message
§10 · R55 — one nominal and one failure test per public function
§10 · R56 — no test reaches the system clock; time and readings are injected
§10 · R81 — a test whose subject reaches an `android.*` method runs under
  Robolectric
§11 · R62 — the code's vocabulary, no synonym outside it
§11 · R63 — English; every exported symbol carries its one line
§11 · R64 — no user-facing string literal in the code
§2 · R74 — a call site in the same module is this lot's own scope
§2 · R4 — deliverable only when `./gradlew check` exits 0

## Requests

architecte/detailleur-lot-41.md
