## Symbols

HyresultParseFailureCause — modified, now EMPTY_PASTE/INSUFFICIENT_COLUMNS/INVALID_TIME_VALUE/TOO_FEW_SEGMENTS/TOO_MANY_SEGMENTS/UNKNOWN_LABEL/LABEL_OUT_OF_SEQUENCE/DIFF_SUM_MISMATCH
HyresultParseResult.Failure — modified, adds rawRow and label
HyresultResultParser.parse — modified, per the blocking file's decision
PasteErrorUiState — created
PasteErrorViewModel — created
PasteErrorScreen — created

## Build

analyze: clean (:core-domain:check, :app-phone:check, lint included)
test: 13 passed (HyresultResultParserTest), 9 passed (PasteErrorViewModelTest), 8 passed (PasteResultViewModelTest, adapted)

## State

Added: PasteErrorViewModel, PasteErrorScreen (docs/CURRENT_TECHNICAL_STATE.md, "## Race")
Removed: —

## Convention

—
