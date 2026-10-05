## Symbols

RaceRepository — modified, adds `observeAll`, `findById`, `observeReference`
RaceRepositoryImpl — modified, backs `observeAll`/`observeReference` with a `MutableStateFlow<List<Race>>`, `findById` now public
RaceListItemUiState — created
RaceListUiState — created
RaceListViewModel — created
RaceListScreen — created
PhoneStringResources.RaceList.addResult — created

## Build

analyze: clean
test: :core-domain:check 74 passed, :core-data:check 31 passed, :app-phone:check 37 passed

## State

Added: RaceRepository observeAll/findById/observeReference and their ordering trap, RaceListViewModel, RaceListScreen
Removed: —

## Convention

—
