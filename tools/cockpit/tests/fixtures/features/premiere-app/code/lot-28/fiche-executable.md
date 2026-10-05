## Signatures

    data class PasteResultUiState(
        val pastedText: String,
        val raceName: String,
        val raceDate: LocalDate,
        val maxSelectableDate: LocalDate,
        val isImportEnabled: Boolean,
        val lastParseResult: HyresultParseResult?
    )

    class PasteResultViewModel(
        private val navigator: PhoneNavigator,
        today: LocalDate = LocalDate.now()
    ) {

        val uiState: StateFlow<PasteResultUiState>
        // raceDate and maxSelectableDate both initialize to [today]

        /** The paste area's content changes (§9.3). */
        fun onPastedTextChanged(text: String)

        /** The name field's content changes (§9.3). */
        fun onRaceNameChanged(name: String)

        /**
         * The date field's value changes, through the standard date
         * picker (§9.3). [date] is never later than
         * [PasteResultUiState.maxSelectableDate] — the picker's own
         * selectable range enforces that bound, so no rejection path
         * exists here.
         */
        fun onRaceDateChanged(date: LocalDate)

        /**
         * "Importer" tapped (§9.3): parses [PasteResultUiState.pastedText]
         * via `HyresultResultParser.parse` (§5.1). On
         * `HyresultParseResult.Success`, opens the import preview screen
         * (`PhoneNavigator.toImportPreview`, §9.4). On
         * `HyresultParseResult.Failure`, opens the paste error screen
         * (`PhoneNavigator.toPasteError`, §9.5).
         */
        fun onImportClicked()
    }

    @Composable
    fun PasteResultScreen(viewModel: PasteResultViewModel)

    data class ImportPreviewUiState(
        val totalTime: String,
        val segmentsCount: Int
    )

    class ImportPreviewViewModel(
        private val pasteResultViewModel: PasteResultViewModel,
        private val raceRepository: RaceRepository,
        private val navigator: PhoneNavigator
    ) {

        // Derived from the shared PasteResultViewModel's
        // lastParseResult, which is HyresultParseResult.Success by
        // construction whenever this screen is reached (§9.4 is only
        // opened from onImportClicked's Success branch):
        //   totalTime = DisplayFormatter.formatDurationTotal(
        //     DurationTruncationService.truncateToSeconds(success.totalTimeMs)
        //   )
        //   segmentsCount = success.segmentDurationsMs.size
        val uiState: StateFlow<ImportPreviewUiState>

        /**
         * "Corriger" tapped (§9.4): returns to the paste screen
         * (`PhoneNavigator.backToPasteResult`), keeping the pasted text
         * held by the shared `PasteResultViewModel`.
         */
        fun onCorrectClicked()

        /**
         * "Enregistrer" tapped (§9.4): saves the parsed result as a new
         * race (§2.1), via
         * `raceRepository.saveImportedRace(
         *   pasteResultViewModel.uiState.value.raceName,
         *   pasteResultViewModel.uiState.value.raceDate
         *     .atStartOfDay(ZoneId.systemDefault()).toInstant(),
         *   buildSegments(success.segmentDurationsMs)
         * )`.
         * On success, opens the new race's detail screen, collapsing
         * the import flow off the back stack
         * (`PhoneNavigator.toRaceDetailAfterImport(race.id)`).
         */
        fun onSaveClicked()
    }

    @Composable
    fun ImportPreviewScreen(viewModel: ImportPreviewViewModel)

## Acceptance criteria

- `uiState.raceDate` equals today's date before any edit (the prefill)
- `uiState.maxSelectableDate` equals today's date
- `onRaceDateChanged(date)` sets `uiState.raceDate` to `date`, for any date on or before today, however far in the past (no lower bound)
- `uiState.isImportEnabled` is true once the paste area and the name field are both filled — the date field always holds a value from construction on, so it never itself withholds enablement
- Given a successful parse with a given total time and 30 segment durations, `ImportPreviewViewModel.uiState.totalTime` equals `DisplayFormatter.formatDurationTotal` of the truncated total, and `uiState.segmentsCount` equals 30
- Tapping "Corriger" (`onCorrectClicked`) moves `PhoneNavigator.current` to `PasteResult`, and the shared `PasteResultViewModel.uiState.pastedText` is unchanged
- Tapping "Enregistrer" (`onSaveClicked`) calls `RaceRepository.saveImportedRace` with the shared `PasteResultViewModel`'s `raceName`, its `raceDate` converted to an `Instant` at the start of that day in the system default zone, and the segments built from the parsed durations
- Tapping "Enregistrer" moves `PhoneNavigator.current` to `RaceDetail(savedRaceId)`, with the back stack collapsed to `RaceList` beneath it

## Dependencies

HyresultParseResult — pre-existing (lot-18)
HyresultResultParser — pre-existing (lot-18)
Race — pre-existing (lot-04)
RaceRepository — pre-existing (lot-04)
Segment — pre-existing (lot-01)
buildSegments — pre-existing (lot-01)
DisplayFormatter — pre-existing (lot-42)
DurationTruncationService — pre-existing (lot-12)
PasteResultViewModel — pre-existing, modified by lot-28 (lot-27)
PasteResultScreen — pre-existing, modified by lot-28 (lot-27)
DesignTokens — pre-existing (lot-02)
PhoneStringResources — pre-existing (lot-43)
PhoneNavigator — pre-existing (lot-24)
PhoneDestination — pre-existing (lot-24)
