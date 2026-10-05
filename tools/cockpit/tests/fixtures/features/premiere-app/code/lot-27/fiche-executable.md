## Signatures

    data class PasteResultUiState(
        val pastedText: String,
        val raceName: String,
        val isImportEnabled: Boolean,
        val lastParseResult: HyresultParseResult?
    )

    class PasteResultViewModel {

        val uiState: StateFlow<PasteResultUiState>

        /** The paste area's content changes (§9.3). */
        fun onPastedTextChanged(text: String)

        /** The name field's content changes (§9.3). */
        fun onRaceNameChanged(name: String)

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

## Acceptance criteria

- `uiState.isImportEnabled` is false when the paste area is empty and the name field is filled
- `uiState.isImportEnabled` is false when the name field is empty and the paste area is filled
- `uiState.isImportEnabled` is true once both the paste area and the name field are filled
- `onImportClicked`, given a pasted text that parses successfully, moves `PhoneNavigator.current` to `ImportPreview`
- `onImportClicked`, given a pasted text that fails to parse, moves `PhoneNavigator.current` to `PasteError`
- `onImportClicked` sets `uiState.lastParseResult` to the parser's outcome, whether `Success` or `Failure`

## Dependencies

HyresultResultParser — pre-existing (lot-18)
DesignTokens — pre-existing (lot-02)
PhoneStringResources — pre-existing (lot-43)
PhoneNavigator — pre-existing (lot-24)
PhoneDestination — pre-existing (lot-24)
