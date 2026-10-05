## Signatures

EndOfRaceViewModel.computeState(finalRace: Race, referenceRace: Race?) → EndOfRaceUiState
isIncomplete is true when finalRace.completion is RaceCompletion.INCOMPLETE, false when
RaceCompletion.COMPLETE. Every other field keeps its current computation, unaffected.

data class EndOfRaceUiState(
  totalTime: String,
  finalDeltaText: String?,
  finalDeltaTone: DeltaTone?,
  dateTime: String,
  isIncomplete: Boolean
)

WatchStringResources.End.incomplete: LabelRef — static, states the race is incomplete

## Acceptance criteria

- A finalRace whose completion is RaceCompletion.COMPLETE produces EndOfRaceUiState.isIncomplete = false
- A finalRace whose completion is RaceCompletion.INCOMPLETE produces EndOfRaceUiState.isIncomplete = true
- EndOfRaceScreen renders WatchStringResources.End.incomplete's message when uiState.isIncomplete is true
- EndOfRaceScreen renders no incomplete-race message when uiState.isIncomplete is false

## Dependencies

Race — pre-existing
RaceCompletion — pre-existing
EndOfRaceViewModel — pre-existing, modified by this lot
EndOfRaceUiState — pre-existing, modified by this lot
EndOfRaceScreen — pre-existing, modified by this lot
WatchStringResources.End — pre-existing, new entry added by this lot
LabelRef — pre-existing

## Conventions

§10 · no hardcoded string
§10 · French only
§11 · one StateFlow per screen, holding a single immutable UI state class
