## Symbols

RaceRecordingRepository.markSegment — modified, gains `segmentDistanceM: Double?`
RaceRecordingRepositoryImpl — modified, gains a `ProfileRepository` constructor dependency
CorrectionFactorCalculator.compute — modified, `station: Station` replaced by `kilometre: Int`
RetainedFactor — modified, `station: Station` replaced by `kilometre: Int`
RejectedCalibration — modified, `station: Station` replaced by `kilometre: Int`
SegmentMarkingController.onPressEnd — modified, gains `segmentDistanceM: Double?`
MainRacePageViewModel.onPressEnd — modified, computes and forwards `segmentDistanceM`
ProjectionViewModel.onPressEnd — modified, always forwards `segmentDistanceM = null` (per resolved blocking decision)

## Build

analyze: clean (`:core-domain:check`, `:app-wear:check`, including lint)
test: `:core-domain:test` all passed; `:app-wear:testDebugUnitTest` all passed

## State

Added: —
Removed: —

## Convention

—
