## Signatures

PasteErrorUiState — adds a field alongside rawRow:

  data class PasteErrorUiState(
    val title: String,
    val body: String,
    val rawRow: String?,
    val expectedRow: String?
  )

  expectedRow — the illustrated expected form of the row, non-null exactly
  when rawRow is non-null (per the Product Owner's decision recorded in
  docs/features/premiere-app/bugfix/code/lot-07/blocked_detailleur.md,
  applied and removed): present for INSUFFICIENT_COLUMNS,
  INVALID_TIME_VALUE, UNKNOWN_LABEL, LABEL_OUT_OF_SEQUENCE and
  DIFF_SUM_MISMATCH; null for EMPTY_PASTE, TOO_FEW_SEGMENTS and
  TOO_MANY_SEGMENTS.

PasteErrorViewModel.buildUiState(failure: HyresultParseResult.Failure) → PasteErrorUiState
  Populates expectedRow from failure exactly when failure.rawRow is
  non-null; leaves it null when failure.rawRow is null.

PasteErrorScreen(viewModel: PasteErrorViewModel)
  Renders uiState.expectedRow beside uiState.rawRow whenever both are
  present. Renders neither when both are null.

## Acceptance criteria

- A failure with cause INSUFFICIENT_COLUMNS produces a non-null expectedRow
- A failure with cause INVALID_TIME_VALUE produces a non-null expectedRow
- A failure with cause UNKNOWN_LABEL produces a non-null expectedRow
- A failure with cause LABEL_OUT_OF_SEQUENCE produces a non-null expectedRow
- A failure with cause DIFF_SUM_MISMATCH produces a non-null expectedRow
- A failure with cause EMPTY_PASTE produces a null expectedRow
- A failure with cause TOO_FEW_SEGMENTS produces a null expectedRow
- A failure with cause TOO_MANY_SEGMENTS produces a null expectedRow
- When uiState.expectedRow is non-null, PasteErrorScreen renders it alongside the row as pasted
- When uiState.expectedRow is null, PasteErrorScreen renders no illustrated expected form

## Dependencies

HyresultParseFailureCause — pre-existing
HyresultParseResult.Failure — pre-existing (rowNumber, cause, rawRow, label)
PasteErrorUiState — modified: adds expectedRow
PasteErrorViewModel — modified: buildUiState populates expectedRow
PasteErrorScreen — modified: renders expectedRow beside rawRow
