## Signatures

sealed interface HyresultParseResult {
  data class Success(
    val totalTimeMs: Long, val segmentDurationsMs: List<Long>
  ) : HyresultParseResult
  data class Failure(
    val rowNumber: Int, val cause: HyresultParseFailureCause
  ) : HyresultParseResult
}

enum class HyresultParseFailureCause {
  INSUFFICIENT_COLUMNS, INVALID_TIME_VALUE, UNEXPECTED_LABEL,
  DIFF_SUM_MISMATCH, UNEXPECTED_ROW_COUNT
}

HyresultResultParser.parse(pastedText: String) → HyresultParseResult

## Acceptance criteria

- A well-formed paste of 30 data rows, with a matching running diff sum on every row and labels in the expected cycle order, returns Success with totalTimeMs equal to the last row's cumulated time and 30 entries in segmentDurationsMs
- A row with fewer than 4 columns returns Failure with cause INSUFFICIENT_COLUMNS and that row's number
- A first row whose 4th column does not parse as a time value is skipped as a header — parsing still succeeds on an otherwise well-formed table
- A second row (immediately after a skipped header) whose 4th column also fails to parse as a time value returns Failure with cause INVALID_TIME_VALUE and that row's number, not a second skip
- A row whose diff value does not match the running sum against the time column returns Failure with cause DIFF_SUM_MISMATCH and that row's number
- A row whose label breaks the expected cycle order returns Failure with cause UNEXPECTED_LABEL and that row's number
- A paste with a number of data rows other than 30 returns Failure with cause UNEXPECTED_ROW_COUNT
- Columns separated by a tab and columns separated by a run of multiple spaces both parse identically, station names' own single internal spaces never splitting into extra columns
- A time value with 2 components reads as m:ss and one with 3 components reads as h:mm:ss, and the scale may differ between rows of the same paste
- On any failure, the result carries only the row number and the cause — never a partial totalTimeMs or segmentDurationsMs

## Dependencies

Station — pre-existing (lot-01), used by the label-to-segment mapping table
