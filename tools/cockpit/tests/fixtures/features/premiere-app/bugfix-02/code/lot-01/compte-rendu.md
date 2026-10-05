## Symbols

RaceEntity — created
SegmentEntity — created
RetainedFactorEntity — created
RejectedCalibrationEntity — created
ProfileEntity — created
RaceDao — created
ProfileDao — created
HyroxDatabase — created
RaceRepositoryImpl — modified, now Room-backed through RaceDao instead of an in-memory LinkedHashMap
ProfileRepositoryImpl — modified, now Room-backed through ProfileDao instead of an in-memory MutableStateFlow

## Build

analyze: clean (`:core-data:check`, `:core-domain:check`, `:app-phone:check`, `:app-wear:check`, `:core-sync:check`)
test: 41 passed (`:core-data:testDebugUnitTest`)

## State

Added: RaceEntity, SegmentEntity, RetainedFactorEntity, RejectedCalibrationEntity, ProfileEntity, RaceDao, ProfileDao, HyroxDatabase, RaceRepositoryImpl (Room-backed), ProfileRepositoryImpl (Room-backed)
Removed: RaceRepositoryImpl (in-memory LinkedHashMap backing), ProfileRepositoryImpl (in-memory MutableStateFlow backing)

## Convention

—
