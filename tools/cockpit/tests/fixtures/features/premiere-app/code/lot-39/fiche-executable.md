## Signatures

    object CumulativeDeltaEstimator {

        // estimate(...) unchanged.

        /**
         * The cumulative delta at the race's last closed segment: Σ(real −
         * reference) over every entry of [raceSegments] carrying a
         * non-null `durationMs`, matched to [referenceSegments] by
         * `Segment.index`. Takes no current segment index and applies no
         * per-segment clamp, unlike `estimate`.
         */
        fun finalDelta(raceSegments: List<Segment>, referenceSegments: List<Segment>): Long
    }

    enum class DeltaTone { AHEAD, BEHIND, ZERO }

    data class EndOfRaceUiState(
        val totalTime: String,
        val finalDeltaText: String?,
        val finalDeltaTone: DeltaTone?,
        val dateTime: String
    )

    class EndOfRaceViewModel(
        finalRace: Race,
        referenceRace: Race?,
        exerciseSessionManager: ExerciseSessionManager,
        private val navigator: WatchRaceNavigator
    ) {

        val uiState: StateFlow<EndOfRaceUiState>

        /** "Terminer" tapped (§8.3): returns to the home screen (§9.9). */
        fun onFinishClicked()
    }

    @Composable
    fun EndOfRaceScreen(viewModel: EndOfRaceViewModel)

## Acceptance criteria

- `finalDelta` sums (real − reference) `durationMs` only over segments carrying a non-null `durationMs` — a segment never reached contributes nothing to the sum
- `finalDelta` keeps a negative contribution from a non-RUN segment finished faster than its reference, unlike `estimate`, which clamps that case to zero
- `totalTime` is the sum of `finalRace`'s reached segments' `durationMs`, truncated and formatted as `duration-total` (§10.1)
- `dateTime` is `finalRace.date` formatted as date+time (§10.1)
- With `referenceRace` non-null, `finalDeltaText`/`finalDeltaTone` reflect `CumulativeDeltaEstimator.finalDelta(finalRace.segments, referenceRace.segments)`, truncated and formatted as a delta, toned `AHEAD`/`BEHIND`/`ZERO` by its sign
- With `referenceRace` null, `finalDeltaText` and `finalDeltaTone` are both null — the final delta block is hidden, not shown
- Constructing the view model while the exercise session is open closes it via `ExerciseSessionManager.close()`
- `onFinishClicked()` moves `WatchRaceNavigator.current` from `END` to `HOME`

## Dependencies

Race — pre-existing (lot-04)
Segment — pre-existing (lot-01)
CumulativeDeltaEstimator — modified by this lot (adds `finalDelta`)
ExerciseSessionManager — pre-existing (lot-20)
DurationTruncationService — pre-existing (lot-12)
DisplayFormatter — pre-existing (lot-42)
DesignTokens — pre-existing (lot-02)
WatchStringResources — pre-existing (lot-44)
WatchRaceNavigator — pre-existing (lot-23)
WatchDestination — pre-existing (lot-23)
