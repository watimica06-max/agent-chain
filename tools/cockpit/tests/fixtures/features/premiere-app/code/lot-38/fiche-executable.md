## Signatures

    data class ControlUiState(
        val undoLabel: String?,
        val undoEnabled: Boolean,
        val stopConfirmVisible: Boolean
    )

    class ControlViewModel(
        initialRace: Race,
        private val undoMarkingController: UndoMarkingController,
        private val stopRaceController: StopRaceController,
        private val navigator: WatchRaceNavigator
    ) {

        val uiState: StateFlow<ControlUiState>

        /** The undo pill tapped (§4.4/§9.14): reopens the segment it names. */
        fun onUndoClicked()

        /** The stop control tapped (§4.5/§9.14): opens the confirmation. */
        fun onStopClicked()

        /** "Annuler" tapped in the stop confirmation (§9.14): closes it, no repository call. */
        fun onStopCancelled()

        /** "Arrêter" tapped in the stop confirmation (§4.5/§9.14). */
        fun onStopConfirmed(atInstant: Instant)
    }

    @Composable
    fun ControlScreen(viewModel: ControlViewModel)

## Acceptance criteria

- `undoEnabled` is false while `currentSegmentIndex` is null or 1, matching `UndoMarkingController.canUndo`
- `undoEnabled` is true once `currentSegmentIndex` is greater than 1
- With `currentSegmentIndex = N` (`N` > 1), `undoLabel` equals `WatchStringResources.Control.undoLabel(WatchStringResources.segmentName(N - 1))` — the segment the last marking closed
- Tapping the undo control while enabled calls `UndoMarkingController.undo`, updates `uiState` from the race it returns, and moves `WatchRaceNavigator.current` to `MAIN`
- Tapping the stop control sets `stopConfirmVisible` to true
- "Annuler" in the stop confirmation sets `stopConfirmVisible` back to false without calling `StopRaceController.stop`
- "Arrêter" in the stop confirmation calls `StopRaceController.stop(raceId, atInstant)` and, on success, moves `WatchRaceNavigator.current` to `END`
- A failing `StopRaceController.stop` leaves `WatchRaceNavigator.current` on `CONTROL` and `stopConfirmVisible` true

## Dependencies

Race — pre-existing (lot-04)
UndoMarkingController — pre-existing (lot-16)
StopRaceController — pre-existing (lot-17)
WatchRaceNavigator — pre-existing (lot-23)
WatchDestination — pre-existing (lot-23)
DesignTokens — pre-existing (lot-02)
WatchStringResources — pre-existing (lot-44); `segmentName(index)` — produced by lot-36 (this block, currently blocked — see `code/lot-36/blocked_detailleur.md`)
