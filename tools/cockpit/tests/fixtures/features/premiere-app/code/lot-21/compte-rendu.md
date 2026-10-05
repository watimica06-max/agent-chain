## Symbols

RaceHistoryEntry — created
ProfileSyncPayload — created
ProfileSyncPushOutcome — created
ProfileSyncApplyOutcome — created
ProfileSyncTransport — created (interface only, no Data-Layer-backed implementation yet)
WatchHistoryStore — created (interface only, no backing implementation yet)
ProfileSyncPushService — created
ProfileRepository — modified, adds `markSyncSuccess(at)`
ProfileRepositoryImpl — modified, backs `markSyncSuccess`
RaceRepository — modified, adds `replaceReference(race)`
RaceRepositoryImpl — modified, backs `replaceReference`

## Build

analyze: clean
test: :core-domain:check 105 passed, :core-data:check 33 passed, :app-phone:check 93 passed

## State

Added: ProfileSyncPushService and its data model (sync package), RaceRepository.replaceReference, ProfileRepository.markSyncSuccess
Removed: the "no writer sets lastSyncSuccessAt yet" note on Profile — now false

## Convention

—
