## Signatures

    interface RaceRepository {

        // setAsReference, rename, delete, saveImportedRace unchanged.

        /**
         * Every stored race, sorted by `date` descending, ties broken by
         * insertion order descending (§9.1). Emits again whenever the
         * stored races change.
         */
        fun observeAll(): Flow<List<Race>>

        /** The stored race for [raceId], or null when none is stored under it. */
        fun findById(raceId: Long): Race?

        /**
         * The race currently flagged `isReference`, or null when none is
         * set. Emits again whenever the reference changes.
         */
        fun observeReference(): Flow<Race?>
    }

    data class RaceListItemUiState(
        val raceId: Long,
        val name: String,
        val date: String,
        val totalTime: String,
        val isReference: Boolean,
        val isIncomplete: Boolean
    )

    data class RaceListUiState(
        val races: List<RaceListItemUiState>
    )

    class RaceListViewModel(
        raceRepository: RaceRepository,
        private val navigator: PhoneNavigator
    ) {

        val uiState: StateFlow<RaceListUiState>

        /** A race card tapped (§9.1): opens its detail screen. */
        fun onRaceClicked(raceId: Long)

        /** The header "+" tapped (§9.1): opens the paste-a-result screen. */
        fun onAddResultClicked()
    }

    @Composable
    fun RaceListScreen(viewModel: RaceListViewModel)

## Acceptance criteria

- `RaceRepository.observeAll()` emits a list containing every stored race
- `RaceRepository.observeAll()` orders two races with different `date`s by `date` descending
- `RaceRepository.observeAll()` orders two races sharing the same `date` by most-recently-inserted first
- `RaceRepository.observeAll()` emits an updated list after a race is added, renamed or deleted
- `RaceRepository.findById(raceId)` returns the stored race matching `raceId`
- `RaceRepository.findById(raceId)` returns null for an id with no stored race
- `RaceRepository.observeReference()` emits the race whose `isReference` is true
- `RaceRepository.observeReference()` emits null when no race is set as reference
- `RaceRepository.observeReference()` emits again once `setAsReference` changes which race holds the flag
- `uiState.races` lists one entry per stored race, carrying its `name`, formatted `date` and formatted `totalTime`
- A race's `totalTime` equals the sum of its reached segments' `durationMs`, truncated and formatted as `duration-total` (§10.1) — never a stored cumulative field
- The reference race's entry carries `isReference = true`; every other entry carries `false`
- An `incomplete` race's entry carries `isIncomplete = true`
- `onRaceClicked(raceId)` moves `PhoneNavigator.current` to `RaceDetail(raceId)`
- `onAddResultClicked()` moves `PhoneNavigator.current` to `PasteResult`
- `uiState.races` is empty when no race is stored

## Dependencies

Race — pre-existing (lot-04)
Segment — pre-existing (lot-01)
RaceRepository — modified by this lot (adds `observeAll`, `findById`, `observeReference`)
DurationTruncationService — pre-existing (lot-12)
DisplayFormatter — pre-existing (lot-42)
DesignTokens — pre-existing (lot-02)
PhoneStringResources — pre-existing (lot-43)
PhoneNavigator — pre-existing (lot-24)
PhoneDestination — pre-existing (lot-24)
