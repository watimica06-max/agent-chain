## Signatures

RaceListViewModel.onProfileClicked(): Unit — calls
PhoneNavigator.toProfile()

RaceListHeader(onAddResultClicked: () -> Unit, onProfileClicked: () ->
Unit): @Composable Unit — renders a profile icon next to the existing
"+" action, backed by PhoneStringResources.RaceList's new glyph entry;
tapping it invokes onProfileClicked

RaceListScreen(viewModel: RaceListViewModel): @Composable Unit — wires
RaceListHeader's onProfileClicked to viewModel::onProfileClicked;
switches its empty-state rendering from the inline
`uiState.races.isEmpty()` check to `isRaceListEmpty(uiState)`

isRaceListEmpty(uiState: RaceListUiState): Boolean — true when
uiState.races is empty, false when it holds at least one race

PhoneStringResources.RaceList.profileIcon: LabelRef — new entry naming
the profile icon's glyph

## Acceptance criteria

- RaceListHeader renders a profile icon in addition to the existing
  title and "+" action
- Tapping the profile icon invokes the onProfileClicked callback
- RaceListScreen wires RaceListHeader's onProfileClicked to
  RaceListViewModel.onProfileClicked, whose call advances
  PhoneNavigator.current to PhoneDestination.Profile
- isRaceListEmpty(uiState) is true when RaceListUiState.races is empty
- isRaceListEmpty(uiState) is false when RaceListUiState.races holds
  at least one race

## Dependencies

PhoneNavigator — pre-existing (toProfile())
RaceListUiState — pre-existing
LabelRef — pre-existing (:core-domain)
WatchHistoryScreen.isHistoryEmpty — pre-existing, in :app-wear; mirrored
in shape, not imported

## Conventions

§9 · the name of the rule, not of the structure — isRaceListEmpty
mirrors isHistoryEmpty's naming
§10 · no hardcoded string — the profile icon's glyph is a new
PhoneStringResources.RaceList entry, not a literal
§3 · :app-phone and :app-wear never import each other — isRaceListEmpty
is rebuilt locally in :app-phone, not imported from :app-wear
