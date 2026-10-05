## Signatures

    object PhoneStringResources {

        // ... existing objects unchanged.

        /**
         * The display name for the segment at [index] (1..30), derived from
         * `SegmentBlueprint.typeAt`/`stationAt`:
         * - RUN            → "Run {run number}" (1..8, by RUN occurrence order)
         * - STATION        → the station's French name (SkiErg, Sled Push,
         *                     Sled Pull, Burpee BJ, Rameur, Farmers Carry,
         *                     Sandbag Lunges)
         * - ROXZONE_OUT    → "Roxzone → {station}", the station reached by
         *                     the STATION segment that immediately follows
         * - ROXZONE_IN     → "Roxzone → piste"
         * - FINAL (30)     → "Wall Balls"
         */
        fun segmentName(index: Int): String

        /** "CYCLE {cycleNumber}" (§9.2's cycle group header, cycleNumber 1..8). */
        fun cycleHeader(cycleNumber: Int): String
    }

    enum class DeltaTone { AHEAD, BEHIND, ZERO }

    data class SegmentRowUiState(
        val index: Int,
        val name: String,
        val duration: String?,
        val cumulative: String?,
        val delta: String?,
        val deltaTone: DeltaTone?
    )

    data class CycleGroupUiState(
        val cycleNumber: Int,
        val header: String,
        val rows: List<SegmentRowUiState>
    )

    data class RaceDetailUiState(
        val raceId: Long,
        val name: String,
        val date: String,
        val total: String,
        val isReference: Boolean,
        val isSetReferenceVisible: Boolean,
        val isDeltaColumnVisible: Boolean,
        val cycles: List<CycleGroupUiState>,
        val renameFieldValue: String?,
        val isDeleteConfirmVisible: Boolean,
        val isDeleteReferenceNoticeVisible: Boolean
    )

    class RaceDetailViewModel(
        raceId: Long,
        raceRepository: RaceRepository,
        private val navigator: PhoneNavigator
    ) {

        val uiState: StateFlow<RaceDetailUiState>

        /** "Définir comme référence" tapped (§2.1). */
        fun onSetAsReferenceClicked()

        /** "Renommer" tapped (§2.1): opens the rename dialog pre-filled with the current name. */
        fun onRenameClicked()

        /** The rename dialog's field content changes. */
        fun onRenameTextChanged(text: String)

        /** The rename dialog's "Annuler": closes it, no write. */
        fun onRenameCancelled()

        /** The rename dialog's "Enregistrer" (§2.1's rename). */
        fun onRenameConfirmed()

        /** "Supprimer" tapped (§2.1): opens the delete confirmation. */
        fun onDeleteClicked()

        /** The delete confirmation's "Annuler": closes it, no write. */
        fun onDeleteCancelled()

        /**
         * The delete confirmation's "Supprimer" (§2.1's delete). On success,
         * moves `PhoneNavigator.current` back to the previous screen.
         */
        fun onDeleteConfirmed()
    }

    @Composable
    fun RaceDetailScreen(viewModel: RaceDetailViewModel)

## Acceptance criteria

- `uiState.cycles` lists exactly 8 cycle groups, headers "CYCLE 1".."CYCLE 8"
- Cycles 1 through 7 each list exactly 4 rows, for segment indices `4n-3`..`4n`
- Cycle 8 lists exactly 2 rows, for segment indices 29 and 30
- Every row 1..30 renders exactly once across the 8 cycles, in index order
- `SegmentRowUiState.name` equals `PhoneStringResources.segmentName(index)` for that row's index
- `segmentName(1)` returns "Run 1"; `segmentName(29)` returns "Run 8"
- `segmentName(3)` returns "SkiErg"; `segmentName(27)` returns "Sandbag Lunges"
- `segmentName(2)` returns "Roxzone → SkiErg" (the station reached by segment 3)
- `segmentName(4)` returns "Roxzone → piste"
- `segmentName(30)` returns "Wall Balls"
- A segment with no stored `durationMs` (never reached) shows a dash for both `duration` and `cumulative`, and a null `delta`
- A reached segment's `duration` equals `DurationTruncationService.segmentDisplayedSeconds(cumulativeMs, previousCumulativeMs)`, formatted `duration-segment` (§10.1); segment 1 uses 0 as `previousCumulativeMs`
- A reached segment's `cumulative` equals `DurationTruncationService.truncateToSeconds(cumulativeMs)`, formatted `duration-elapsed` (§10.1)
- `uiState.total` equals the sum of every reached segment's raw `durationMs`, truncated and formatted `duration-total` (§10.1) — never a segment's `cumulativeMs`
- `uiState.isDeltaColumnVisible` is true when a reference race exists and it is not the race being viewed
- `uiState.isDeltaColumnVisible` is false when the race being viewed is itself the reference
- `uiState.isDeltaColumnVisible` is false when no race is set as reference
- When `isDeltaColumnVisible` is true, a reached segment's `delta` equals the truncated millisecond difference (this race's `durationMs` − the reference race's `durationMs` at the same index), formatted `delta` (§10.1)
- When `isDeltaColumnVisible` is false, every row's `delta` is null
- A segment whose truncated delta is negative carries `deltaTone = AHEAD`
- A segment whose truncated delta is positive carries `deltaTone = BEHIND`
- A segment whose truncated delta is zero carries `deltaTone = ZERO`
- `uiState.isReference` is true only when the race being viewed is the current reference
- `uiState.isSetReferenceVisible` is false when the race's `completion` is `incomplete`
- `uiState.isSetReferenceVisible` is false when `isReference` is already true
- `uiState.isSetReferenceVisible` is true otherwise
- `onSetAsReferenceClicked` calls `RaceRepository.setAsReference(raceId)`
- `onRenameClicked` sets `uiState.renameFieldValue` to the race's current `name`
- `onRenameCancelled` clears `uiState.renameFieldValue` without calling `RaceRepository.rename`
- `onRenameConfirmed` calls `RaceRepository.rename(raceId, uiState.renameFieldValue)`
- `onDeleteClicked` sets `uiState.isDeleteConfirmVisible` to true
- `uiState.isDeleteReferenceNoticeVisible` is true when `isReference` is true, false otherwise
- `onDeleteCancelled` sets `uiState.isDeleteConfirmVisible` to false without calling `RaceRepository.delete`
- `onDeleteConfirmed` calls `RaceRepository.delete(raceId)`, then, on success, moves `PhoneNavigator.current` back to the previous screen

## Dependencies

Race — pre-existing (lot-04)
Segment — pre-existing (lot-01)
SegmentType, Station, SegmentBlueprint — pre-existing (lot-01)
RaceRepository — pre-existing, as extended by lot-25 (`findById`/`observeAll`/`observeReference`); no further modification by this lot
DurationTruncationService — pre-existing (lot-12)
DisplayFormatter — pre-existing (lot-42)
DesignTokens — pre-existing (lot-02)
PhoneStringResources — modified by this lot: adds `segmentName(index)` (per the Product Owner's decision resolving the earlier block) and `cycleHeader(cycleNumber)` (§9.2's literal "CYCLE n" header text, §10.2's no-hardcoded-string rule)
PhoneNavigator — pre-existing (lot-24)
PhoneDestination — pre-existing (lot-24)

Note: `LapDeltaCalculator` (lot-09) is not used — §3.4 states it is consumed by §9.12/§3.5 only (live, pace-derived projection). §9.2 compares two already-measured durations; its delta is a plain millisecond subtraction between the two races' stored segment values, per §3.7's own delta-truncation rule.
