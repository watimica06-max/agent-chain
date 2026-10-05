## Symbols

RaceListViewModel.onProfileClicked — created, calls PhoneNavigator.toProfile()
RaceListHeader — modified, now takes onProfileClicked: () -> Unit and renders a profile icon next to the "+" action; visibility changed to internal for direct testing
RaceListScreen — modified, wires RaceListHeader's onProfileClicked to RaceListViewModel.onProfileClicked and switches its empty-state check to isRaceListEmpty(uiState)
isRaceListEmpty — created, uiState.races.isEmpty()
PhoneStringResources.RaceList.profileIcon — created, LabelRef(R.string.race_list_profile_icon)

## Build

analyze: clean
test: :app-phone:check passed (RaceListScreenTest: 5 passed, RaceListViewModelTest: 9 passed)

## State

Added: —
Removed: —

## Convention

—
