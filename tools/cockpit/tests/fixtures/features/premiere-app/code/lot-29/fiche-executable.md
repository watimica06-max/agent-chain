## Signatures

    enum class HyresultParseFailureCause {
        EMPTY_PASTE, INSUFFICIENT_COLUMNS, INVALID_TIME_VALUE,
        TOO_FEW_SEGMENTS, TOO_MANY_SEGMENTS,
        UNKNOWN_LABEL, LABEL_OUT_OF_SEQUENCE, DIFF_SUM_MISMATCH
    }

    sealed interface HyresultParseResult {
        data class Success(
            val totalTimeMs: Long,
            val segmentDurationsMs: List<Long>
        ) : HyresultParseResult

        /**
         * [rawRow] is the failing row's text as pasted, non-null only for
         * the five row-level causes (INSUFFICIENT_COLUMNS,
         * INVALID_TIME_VALUE, UNKNOWN_LABEL, LABEL_OUT_OF_SEQUENCE,
         * DIFF_SUM_MISMATCH) — null for EMPTY_PASTE, TOO_FEW_SEGMENTS and
         * TOO_MANY_SEGMENTS, which name no single row.
         *
         * [label] is the row's own label column as read, non-null only for
         * UNKNOWN_LABEL and LABEL_OUT_OF_SEQUENCE.
         *
         * For TOO_FEW_SEGMENTS/TOO_MANY_SEGMENTS, [rowNumber] carries the
         * count of segments actually read, not a line number.
         */
        data class Failure(
            val rowNumber: Int,
            val cause: HyresultParseFailureCause,
            val rawRow: String?,
            val label: String? = null
        ) : HyresultParseResult
    }

    object HyresultResultParser {
        fun parse(pastedText: String): HyresultParseResult
    }

    data class PasteErrorUiState(
        val title: String,
        val body: String,
        val rawRow: String?
    )

    class PasteErrorViewModel(
        private val pasteResultViewModel: PasteResultViewModel,
        private val navigator: PhoneNavigator
    ) {

        val uiState: StateFlow<PasteErrorUiState>

        /**
         * "Revenir au collage" tapped (§9.5): returns to the paste screen
         * (`PhoneNavigator.backToPasteResult`), keeping the pasted text
         * held by the shared `PasteResultViewModel`.
         */
        fun onBackToPasteClicked()
    }

    @Composable
    fun PasteErrorScreen(viewModel: PasteErrorViewModel)

## Acceptance criteria

- Parsing a blank or whitespace-only pasted text returns `Failure` with cause `EMPTY_PASTE`
- A data row with fewer than 4 columns returns `Failure` with cause `INSUFFICIENT_COLUMNS`, `rowNumber` set to that row's number, and `rawRow` equal to that row's text as pasted
- A data row whose diff or cumulative column does not parse as a time value returns `Failure` with cause `INVALID_TIME_VALUE`, `rowNumber` set to that row's number, and `rawRow` equal to that row's text as pasted
- A pasted text ending with fewer than 30 valid data rows returns `Failure` with cause `TOO_FEW_SEGMENTS` and `rowNumber` set to the number of segments actually read
- A pasted text yielding more than 30 valid data rows returns `Failure` with cause `TOO_MANY_SEGMENTS` and `rowNumber` set to the number of segments actually read
- A data row whose label is not among the labels the 30-position cycle can produce returns `Failure` with cause `UNKNOWN_LABEL`, `rowNumber` set to that row's number, `label` set to the value read, and `rawRow` equal to that row's text as pasted
- A data row whose label is one the cycle expects, but not at this row's position, returns `Failure` with cause `LABEL_OUT_OF_SEQUENCE`, `rowNumber` set to that row's number, `label` set to the value read, and `rawRow` equal to that row's text as pasted
- A data row whose running diff sum disagrees with its cumulative column returns `Failure` with cause `DIFF_SUM_MISMATCH`, `rowNumber` set to that row's number, and `rawRow` equal to that row's text as pasted
- A pasted text satisfying every check for all 30 rows returns `Success`, carrying the recognized total time and the 30 segment durations
- Given the shared parse result is `Failure(EMPTY_PASTE)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.emptyTitle`/`emptyBody`, and `uiState.rawRow` is null
- Given `Failure(INSUFFICIENT_COLUMNS, row)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.missingColumnsTitle(row)`/`missingColumnsBody`, and `uiState.rawRow` equals the failing row's text
- Given `Failure(INVALID_TIME_VALUE, row)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.invalidTimeTitle(row)`/`invalidTimeBody`, and `uiState.rawRow` equals the failing row's text
- Given `Failure(TOO_FEW_SEGMENTS, count)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.tooFewTitle(count)`/`tooFewBody`, and `uiState.rawRow` is null
- Given `Failure(TOO_MANY_SEGMENTS, count)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.tooManyTitle(count)`/`tooManyBody`, and `uiState.rawRow` is null
- Given `Failure(UNKNOWN_LABEL, row, label)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.unknownLabelTitle(row)`/`unknownLabelBody(label)`, and `uiState.rawRow` equals the failing row's text
- Given `Failure(LABEL_OUT_OF_SEQUENCE, row, label)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.outOfSequenceTitle(row)`/`outOfSequenceBody(label)`, and `uiState.rawRow` equals the failing row's text
- Given `Failure(DIFF_SUM_MISMATCH, row)`, `uiState.title`/`uiState.body` equal `PhoneStringResources.PasteError.inconsistentTimeTitle(row)`/`inconsistentTimeBody`, and `uiState.rawRow` equals the failing row's text
- Tapping "Revenir au collage" (`onBackToPasteClicked`) moves `PhoneNavigator.current` to `PasteResult`, and the shared `PasteResultViewModel.uiState.pastedText` is unchanged

## Dependencies

HyresultParseResult — pre-existing, modified by lot-29 (lot-18)
HyresultParseFailureCause — pre-existing, modified by lot-29 (lot-18)
HyresultResultParser — pre-existing, modified by lot-29 (lot-18)
PasteResultViewModel — pre-existing (lot-27)
PhoneNavigator — pre-existing (lot-24)
PhoneStringResources — pre-existing (lot-43)
DesignTokens — pre-existing (lot-02)
