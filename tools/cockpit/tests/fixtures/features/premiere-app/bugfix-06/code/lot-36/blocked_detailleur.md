## What blocks

lot-36 is declared as making the home page say which race the sync
stopped on, but no text catalogue key names such a message and lot-36
touches no catalogue — so I cannot say whether `HomeSyncUiState.Failure`
carries the raceId at all, nor what the screen renders when it does.

## Where

lot-36 — `HomeViewModel.toHomeSyncUiState`, `HomeSyncUiState.Failure`
and `HomeScreen`'s `HomeSyncUiState.Failure` branch
(`app-wear/src/main/java/com/mgilli/app_wear/home/`), against
`desc-bug.md` §6.4 and `code/decoupage.md`'s `## Symbols` line
"toHomeSyncUiState reads a Failure that now carries a raceId, and the
screen shows the race the sync stopped on".

The two readings exclude each other, and both are defensible:

- **the screen shows the race** — `HomeSyncUiState.Failure` becomes a
  data class carrying the raceId and `HomeScreen` renders it. Blocked
  on the text: `WatchStringResources.Sync.failure` is a fixed
  `LabelRef` over `sync_failure` ("Synchronisation impossible —
  approche le téléphone de la montre."), with no placeholder and no
  argument. §10 of `desc-bug.md` names one new key and it is
  `RaceDetailViewModel`'s rename-bound message on the phone. R64
  forbids the literal and R80 forbids reporting through a key written
  for another case, and lot-36 modifies neither `WatchStringResources`
  nor `app-wear/res/values/strings.xml`.
- **the screen shows nothing new** — `HomeScreen` keeps today's fixed
  `sync_failure` line, the way lot-27's settled decision resolved the
  same "no key names this case" question on the phone. Then
  `HomeSyncUiState.Failure` must stay a bare object, because a raceId
  nothing reads is exactly the dead field §9.1 has this cycle removing
  six of — and §6.4 leaves lot-36 nothing to build, its state-side
  requirement having already shipped in lot-15
  (`RecordedRaceSyncState.Failure(val raceId: Long)`, confirmed in
  `:core-domain`).

## To resume

A decision saying, for a sync that stops on a race:

- whether `HomeSyncUiState.Failure` carries that race's identity;
- what the home page shows when it does — the raw id, the race name
  (which `HomeViewModel` cannot reach today: it holds `RaceRepository`
  and reads only `observeReference()`), or the present fixed line;
- if a race-naming text is wanted, the catalogue key backing it, since
  adding one reaches `WatchStringResources` and
  `app-wear/res/values/strings.xml`, neither of which lot-36 declares.

Nothing else in lot-36 is blocked. §6.9 (both `sync` calls derive
`raceInProgress` as `raceRecordingRepository.findInProgress()
.getOrNull() != null`, the way `ProfileSyncPushService.applyIncoming`
already does, with `RaceRecordingRepository` injected), §7.1 (the
`sensorPermissionManager.isGranted()` property initialiser at
`HomeViewModel:45` replaced by a launched read, the way the
connectivity reminder's own field already defaults to false and is
filled by `connectivityPermissionManager.onLaunch()` in `init`) and
§9.8 (`HomeScreen`'s `referenceLineText` `Text` bounded with `maxLines`
and `TextOverflow.Ellipsis`) each have their rule and their symbols
confirmed: `RaceRecordingRepository.findInProgress(): Result<Race?>`,
`RecordedRaceSyncService.sync(raceInProgress: Boolean, at: Instant)`,
`WatchStringResources.Home.referenceLine(name: String?)`. The sheet
follows within one run of the decision below.

## Decision

Take the second reading: `HomeSyncUiState.Failure` stays a bare object,
`toHomeSyncUiState` maps `RecordedRaceSyncState.Failure` to it without
reading `raceId`, and `HomeScreen`'s `HomeSyncUiState.Failure` branch
keeps today's fixed `WatchStringResources.Sync.failure` line unchanged.
Write the sheet for §6.9, §7.1 and §9.8 only.

R80 settles it: "whether the user is told is a product decision, and
until §10 names a key the log of R79 is the whole of the report" — §10
holds one entry, §10.1, and it is `RaceDetailViewModel`'s rename-bound
message on the phone, so no key names a watch sync failure and R64
forbids the literal. §6.4's bearer is `RecordedRaceSyncService`, and its
state-side requirement is already met:
`RecordedRaceSyncState.Failure(val raceId: Long)` in
`core-domain/src/main/kotlin/com/mgilli/core/domain/sync/RecordedRaceSyncState.kt`.
A `raceId` on `HomeSyncUiState.Failure` that no screen reads is the dead
UI-state field §9.1 has this cycle removing six of. This is the same
problem already settled in this cycle: `code/lot-27/blocked_detailleur-01.md`
resolves the identical "no §10 key names this case" question with no
message shown and no string resource added.

This does not extend to `RecordedRaceSyncState.Failure`, which keeps its
`raceId` — lot-15 is untouched, and `HomeViewModel` simply ignores it.
`WatchStringResources`, `app-wear/src/main/res/values/strings.xml` and
`HomeUiState.syncState`'s type stay as they are, and the
`code/decoupage.md` `## Symbols` line "the screen shows the race the sync
stopped on" is not built in lot-36. `HomeViewModel`'s only new dependency
is the `RaceRecordingRepository` §6.9 requires.
