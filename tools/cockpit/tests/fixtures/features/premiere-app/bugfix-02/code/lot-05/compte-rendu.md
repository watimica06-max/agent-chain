## Symbols

cumulativeDurationMs (:core-domain) — created
Segment (:core-domain) — modified, constructor now index/type/station/durationMs only
buildSegments (:core-domain) — modified, no longer computes or stores a cumulative
RaceDetailViewModel.buildRow — modified, derives cumulative and previous-cumulative through cumulativeDurationMs
RaceRecordingRepositoryImplTest (app-wear) — modified, asserts through cumulativeDurationMs instead of Segment.cumulativeMs
RaceDetailViewModelTest (app-phone) — modified, adapted to Segment's current shape (its assertions read Segment.cumulativeMs, made false by this lot's removal of that field)

## Build

analyze: clean
test: :core-domain 121 passed, :app-phone 141 passed, :app-wear 211 passed

## State

Added: cumulativeDurationMs (:core-domain)
Removed: Segment.cumulativeMs (stored field)

## Convention

—
