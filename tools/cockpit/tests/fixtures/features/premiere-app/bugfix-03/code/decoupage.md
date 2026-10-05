## Symbols

Race
  no field distinguishing a sent-but-unacknowledged race from one never sent — gap: gains sentAt: Instant?   §1.1

RaceRecordingRepository
  no way to record that a race was sent — gap: a way RecordedRaceSyncService can call right after transport.send succeeds, with observeRecorded still returning the race until eraseRecorded runs   §1.1

RaceRecordingRepositoryImpl (app-wear)
  implements RaceRecordingRepository — gap: the new sent-marking capability   §1.1

RecordedRaceSyncService
  erases a recorded race as soon as transport.send returns true, and calls RaceRepository.saveRecordedRace directly on the watch's own repository — gap: mark the race sent instead of saving/erasing right after send, keep the race until an acknowledgement arrives, gain a way for that acknowledgement to trigger the erase   §1.1, §6.4

RecordedRacePayload
  carries name, date, segments, completion — gap: a race identifier so the phone can echo it back   §6.4

RaceRepository
  saveRecordedRace(name, date, segments, completion) — gap: an identifier-based idempotency check so a resent acknowledgement does not save a race twice   §6.4

RaceRepositoryImpl (core-data)
  implements RaceRepository — gap: the idempotency check   §6.4

PayloadCodec
  encodes ProfileSyncPayload and RecordedRacePayload, `internal` to :core-sync — gap: a decode function for each payload type, and visibility reaching :app-phone and :app-wear   §6.2, §6.3

RecordedRaceListenerService — does not exist
  gap: a WearableListenerService in :app-phone registering on /recorded-race, decoding the payload via PayloadCodec, calling RaceRepository.saveRecordedRace, and sending /recorded-race-ack once that save succeeds   §6.1, §6.4

ProfileSyncListenerService — does not exist
  gap: a WearableListenerService in :app-wear registering on /profile-sync, decoding the payload via PayloadCodec, calling ProfileSyncPushService.applyIncoming with the current raceInProgress state and instant   §6.2

RecordedRaceAckTransport — piece
  does not exist — sends the saved race's identifier to the watch on /recorded-race-ack, once RaceRepository.saveRecordedRace succeeds   §6.4

RecordedRaceAckListenerService — piece
  does not exist — observes /recorded-race-ack on the watch, feeding RecordedRaceSyncService's acknowledgement handling   §6.4

## §2 Persistence

No entries — no lot.

## §3 Calculation

No entries — no lot.

## §4 Transition

No entries — no lot.

## §5 External source

No entries — no lot.

## §7 Background work

No entries — no lot.

## §8 Journey

No entries — no lot.

## §9 Screen

No entries — no lot.

## §10 Text

No entries — no lot.

## §11 Access

No entries — no lot.

## §12 Lifecycle

No entries — no lot.

## lot-01

Anchor: §1.1 — Race carries no sent state
Needs: —
Produces: —
Modifies: Race (core-domain); RaceRecordingRepository (core-domain interface); RaceRecordingRepositoryImpl (app-wear); and every existing implementer of RaceRecordingRepository, whose declaration must gain the same new member: FakeRecordingRepository (core-domain, RecordedRaceSyncServiceTest.kt), FakeUndoMarkingRepository (app-wear, UndoMarkingControllerTest.kt), StoppingFakeRaceRecordingRepository (app-wear, StopRaceControllerTest.kt), FakeSegmentMarkingRepository (app-wear, SegmentMarkingControllerTest.kt), FakeRaceRecordingRepository (app-wear, RaceLaunchControllerTest.kt), FakeMainPageRecordingRepository (app-wear, MainRacePageViewModelTest.kt), FakeMainRacePageScreenRecordingRepository (app-wear, MainRacePageScreenTest.kt), FakeProjectionRecordingRepository (app-wear, ProjectionViewModelTest.kt), FakeProjectionScreenRecordingRepository (app-wear, ProjectionScreenTest.kt), FakeRaceRecordingRepository (app-wear, PreparationViewModelTest.kt), FakePreparationScreenRecordingRepository (app-wear, PreparationScreenTest.kt), FakeHomeRecordingRepository (app-wear, HomeViewModelTest.kt), FakeHomeScreenRecordingRepository (app-wear, HomeScreenTest.kt), FakeControlRecordingRepository (app-wear, ControlViewModelTest.kt), FakeControlScreenRecordingRepository (app-wear, ControlScreenTest.kt)

## lot-02

Anchor: §6.2 — Nothing receives a profile sync on the watch; §6.3 — PayloadCodec never decodes
Needs: ProfileSyncPayload (pre-existing); RecordedRacePayload carrying a race identifier (lot-05)
Produces: —
Modifies: PayloadCodec (core-sync) — gains decode(bytes) for ProfileSyncPayload and for RecordedRacePayload, and loses its `internal` visibility so :app-phone and :app-wear can call it

## lot-03

Anchor: §6.1 — Nothing receives a recorded race on the phone; §6.4 — A race is erased before the phone confirms receipt
Needs: PayloadCodec.decode for RecordedRacePayload (lot-02); RaceRepository.saveRecordedRace with its identifier-based idempotency check (lot-04); RecordedRaceAckTransport (lot-06)
Produces: RecordedRaceListenerService (mounted by the system, registered on /recorded-race in :app-phone's manifest)
Modifies: —

## lot-04

Anchor: §6.4 — A race is erased before the phone confirms receipt
Needs: —
Produces: —
Modifies: RaceRepository (core-domain interface); RaceRepositoryImpl (core-data) and RaceRepositoryImplTest (core-data); and every existing implementer of RaceRepository whose saveRecordedRace override must match the new signature: the fake in RaceListViewModelTest.kt (app-phone), the fake in RaceDetailViewModelTest.kt (app-phone), the fake in ProfileViewModelTest.kt (app-phone), the fake in ProfileScreenTest.kt (app-phone), the fake in ImportPreviewViewModelTest.kt (app-phone), the fake in ProfileSyncPushServiceTest.kt (core-domain), the fake in PreparationViewModelTest.kt (app-wear), the fake in PreparationScreenTest.kt (app-wear)

## lot-05

Anchor: §1.1 — Race carries no sent state; §6.4 — A race is erased before the phone confirms receipt
Needs: RaceRecordingRepository's sent-marking capability (lot-01)
Produces: RecordedRaceSyncService's acknowledgement handling (called by lot-07, RecordedRaceAckListenerService)
Modifies: RecordedRaceSyncService (core-domain) — sends, marks the race sent through RaceRecordingRepository, no longer calls RaceRepository.saveRecordedRace, and erases only once acknowledged; RecordedRaceSyncServiceTest (core-domain), including removing its now-unneeded RaceRepository fake; RecordedRacePayload (core-domain) — gains a race identifier; app-wear/di/SyncModule.kt's provideRecordedRaceSyncService (drops the RaceRepository parameter); app-wear/di/FakeSyncModule.kt (test, same); HomeViewModelTest.kt (app-wear), dropping the RaceRepository fake argument from every RecordedRaceSyncService construction; HomeScreenTest.kt (app-wear), same

## lot-06

Anchor: §6.4 — A race is erased before the phone confirms receipt
Needs: —
Produces: RecordedRaceAckTransport (called by lot-03, RecordedRaceListenerService)
Modifies: —

## lot-07

Anchor: §6.4 — A race is erased before the phone confirms receipt
Needs: RecordedRaceSyncService's acknowledgement handling (lot-05)
Produces: RecordedRaceAckListenerService (mounted by the system, registered on /recorded-race-ack in :app-wear's manifest)
Modifies: —

## lot-08

Anchor: §6.2 — Nothing receives a profile sync on the watch
Needs: PayloadCodec.decode for ProfileSyncPayload (lot-02); ProfileSyncPushService.applyIncoming (pre-existing); RaceRecordingRepository.findInProgress (pre-existing); Clock (pre-existing, core-domain)
Produces: ProfileSyncListenerService (mounted by the system, registered on /profile-sync in :app-wear's manifest)
Modifies: —
