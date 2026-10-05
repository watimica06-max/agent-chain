## Symbols

ProfileRepository.observe() — created
ProfileRepositoryImpl — modified, backed by a MutableStateFlow<Profile>, implements observe()
WatchStringResources.segmentName(index) — created
DeltaTone — created
RaceTopBlock — created
RaceCenterBlock — created
MainRacePageUiState — created
MainRacePageViewModel — created
MainRacePageScreen — created

## Build

analyze: clean (core-domain:check, core-data:check, app-wear:check, app-phone:check)
test: all passed

## State

Added: MainRacePageViewModel / MainRacePageScreen (app-wear/.../race/), MainRacePageUiState (DeltaTone, RaceTopBlock, RaceCenterBlock)
Removed: ProfileRepository ⚠️ no read method — only the five updaters (observe() now fills that gap)

## Convention

—
