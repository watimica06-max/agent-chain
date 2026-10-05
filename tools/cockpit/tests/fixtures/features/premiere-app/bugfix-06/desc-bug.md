## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

### §1.1 The paste parser misreads the real Hyresult export

Bearer: HyresultResultParser

`parse` skips at most one leading row, only when a fixed-column check fails, reads every data row from a fixed four-column layout with no column for "Time of Day", and treats any row past the fixed 30-segment cycle — including a closing "Total time" row — as a new segment. `parse` recognises and skips the export's header row and its closing "Total time" row without shifting a data row's position in the cycle, reads each row's diff and cumulative values from wherever the real export carries them, and reads a duration the same way whether it carries hours or not.

### §1.2 The correction factor is written unvalidated

Bearer: ProfileRepository

`updateCorrectionFactor` writes its value unconditionally and always returns success, unlike the four other updaters which validate against a fixed range and refuse an out-of-range value. `updateCorrectionFactor` validates its value against a fixed range the same way, refusing it and leaving the stored value unchanged when it falls outside — closing the path by which a blended factor computed from an unvalidated previous value could corrupt itself across races.

### §1.3 A negative segment duration is stored and displayed as-is

Bearer: SegmentBuilder (buildSegments)

`buildSegments` turns any duration into a `Segment` unchanged, a negative one included, so a negative diff from the parser, a negative computed duration from marking a segment, or a corrupted stored value all reach the display as a nonsensical negative time; `undoLastMark` then compounds an already-negative duration by subtracting it. `buildSegments` rejects a negative entry the same way it already rejects a missing one, carrying `durationMs = null` instead, so every caller renders the missing-value glyph and `undoLastMark` leaves such a segment alone. `PayloadCodec`'s `SegmentSnapshot.toSegment` builds a `Segment` directly from a decoded `durationMs`, bypassing `buildSegments` entirely; it needs the same rejection, or must route through `buildSegments`.

### §1.4 `stopRace` ignores the instant it is given

Bearer: RaceRecordingRepository (stopRace)

`stopRace` never reads the `atInstant` parameter its contract already documents as "never truncated," and `Race` carries no end-time field, so a race's total is always the sum of its segments. Either `stopRace` stores `atInstant` on a new `Race` field, or the parameter is dropped from the signature and the interface states explicitly that no end time is recorded.

### §1.5 A race name is validated on rename alone

Bearer: RaceRepository (saveImportedRace, saveRecordedRace)

`saveImportedRace` and `saveRecordedRace` store whatever name they are given, with no trim and no length check, while `rename` refuses an empty trimmed name or one past forty characters; `PasteResultViewModel.isImportEnabled` also enables the import action on a name of spaces, since it tests for emptiness rather than blankness. `saveImportedRace` and `saveRecordedRace` apply the same trim-and-refuse rule `rename` already applies, and `isImportEnabled` tests for blankness instead of emptiness. Second gap: `ImportPreviewViewModel.onSaveClicked`, which reacts only to `saveImportedRace`'s success today, must also react to its new failure case, since nothing today reports a rejected save back to the user.

## §2 Persistence

### §2.1 Four repositories reach the database synchronously

Bearer: ProfileRepository

None of `ProfileRepository`'s methods are `suspend`; `ProfileRepositoryImpl.currentOrDefault` hides a `runBlocking` behind a Room-backed flow, and every updater calls it and `profileDao.upsert` synchronously on whatever thread the caller is on — reached directly from `ProfileViewModel`'s four setting handlers, outside `viewModelScope.launch`. `ProfileRepository`'s methods become `suspend`, `ProfileRepositoryImpl` dispatches its DAO calls on `Dispatchers.IO` and applies `flowOn` to `observe()`, `ProfileDao.upsert` becomes `suspend`, and `ProfileViewModel`'s four handlers move their call inside `viewModelScope.launch`. The same change is a second gap on three more symbols: `RaceRepository`/`RaceRepositoryImpl` (every method becomes `suspend`, `RaceDao` calls dispatch on `Dispatchers.IO`, `observeAll`/`observeReference` carry `flowOn`; `RaceDetailViewModel`'s `setAsReference`/`rename`/`delete` and `ImportPreviewViewModel.saveImportedRace` move inside `viewModelScope.launch`); `WatchHistoryStore`/`WatchHistoryStoreImpl` (`replaceAll` becomes `suspend` and dispatches, `observe()` carries `flowOn`); `RaceRecordingRepository`/`RaceRecordingRepositoryImpl` (`markSegment` and its siblings become `suspend`, replacing the `runBlocking` profile read with a plain suspend call, with `SegmentMarkingController.onPressEnd` and its callers following suit).

### §2.2 Marking a segment blocks and holds a lock across a suspension

Bearer: RaceRecordingRepositoryImpl

`markSegment` reads the profile with `runBlocking { profileRepository.observe().first() }` inside a `synchronized(lock)` block that seven other public methods also enter, so a call reaching any of them — including `findInProgress()` from the composable body, the complication service and the sync listener — blocks until that read returns; the same `runBlocking` also lets an exception escape past `markSegment`'s declared `Result<Race>` return. `markSegment` reads the profile as a plain suspend call, without `runBlocking`, and every method that touches shared state protects it without blocking a thread across a suspension point, so `findInProgress` never waits on `markSegment`'s database read; an exception raised while reading the profile or computing the correction factor is caught and returned as `Result.failure`. Second gap: making `markSegment` and `findInProgress` `suspend` changes every caller — `SegmentMarkingController.onPressEnd` becomes `suspend`; `WatchApp`'s composable body needs `produceState`/`LaunchedEffect` to collect the suspend call; `WatchRaceComplicationDataSourceService.onComplicationRequest` needs its own coroutine scope; `ProfileSyncListenerService.onMessageReceived`'s call moves inside its existing `serviceScope.launch`.

### §2.3 Room reads raise on data they wrote themselves

Bearer: HyroxTypeConverters

`toRaceOrigin`, `toRaceCompletion` and `toZoneThresholds` call `valueOf`/`toInt` on a stored value with no guard, so a value that no longer decodes raises inside Room's own cursor mapping on every read of the row that carries it. `toRaceOrigin`, `toRaceCompletion` and `toZoneThresholds` recognise a stored value that does not decode and return a well-defined fallback instead of raising. Second gap: neither application's `RepositoryModule.provideHyroxDatabase` declares a destructive fallback or guards a migration failure; both need one, so a schema off the declared migration path does not raise unrecovered at the first query.

### §2.4 `markSegment` lets an exception escape its own `Result` contract

Bearer: RaceRecordingRepositoryImpl (markSegment)

`markSegment` declares `Result<Race>` and returns `Result.failure` for its own checked cases, but nothing guards its `runBlocking` profile read or its call into `CorrectionFactorCalculator.compute`, so a failure there propagates past the declared return. `markSegment` catches any exception raised anywhere in its body and returns it as `Result.failure` instead of letting it escape.

### §2.5 Two force-unwraps rest on invariants nothing enforces

Bearer: RaceRepositoryImpl (persist)

`persist` re-reads the row it just wrote with `raceDao.findById(raceId)!!`; a rolled-back transaction or a concurrent delete between the write and the re-read throws a `NullPointerException` instead of a `Result.failure`. `persist` reads back what it wrote inside the same transaction, or states what it does when the row is gone, and the callers that rely on it — `saveImportedRace`, `saveRecordedRace`, `replaceReference` — surface that failure the way `setAsReference`, `rename` and `delete` already do. Second gap, independent bearer: `HyresultResultParser.buildExpectedLabels` calls `SegmentBlueprint.stationAt(index)!!` on a contract enforced by nothing but a doc comment; either the function states what happens when a `STATION` index carries no station, or a test asserts the pairing so the two files cannot drift silently.

### §2.6 A race in progress is not written down

Bearer: RaceRecordingRepository (RaceRecordingRepositoryImpl)

`RaceRecordingRepositoryImpl` holds every race it opens in an in-memory `LinkedHashMap`, with no DAO call in `startClock`, `markSegment`, `undoLastMark`, `stopRace` or `markSent`, so the whole set is rebuilt empty when the process dies and `findInProgress()` returns nothing. `startClock`, `markSegment`, `undoLastMark`, `stopRace` and `markSent` each write the race — its segments and any new calibration entry — to the database before returning, and `findInProgress()` reads the database instead of the in-memory map, so a race left in progress at process death is found again at start-up.

### §2.7 Resuming a preparation depends on state that never survives a process death

Bearer: RaceRecordingRepositoryImpl

`RaceRecordingRepositoryImpl` keeps every race in a plain in-memory map with no Room write, so after a process death `findInProgress()` always returns nothing and `openPreparation` falls through to opening a fresh preparation instead of resuming. `RaceRecordingRepositoryImpl` persists the race it is recording, and its current-segment state, to the database as it opens the clock and marks each segment, so `findInProgress()` reads it back after a process death and `openPreparation` returns `Resuming` as designed. Second gap: `RaceDao` carries no query to find a race with an open segment; one is needed for `findInProgress` to read from.

### §2.8 A race imported on the same day as another can reorder silently

Bearer: RaceRecordingRepositoryImpl (publishRecorded)

`publishRecorded` orders in-memory races with `reversed().sortedByDescending { it.date }`, relying entirely on `sortedByDescending` staying a stable sort to preserve the tie-break the phone's query enforces with an explicit second key. `publishRecorded` orders races by an explicit second key, `id` descending, the same two keys the phone's query already uses, so the ordering no longer depends on sort stability.

### §2.9 A race recorded after a process restart can be lost as a false duplicate

Bearer: RaceRecordingRepositoryImpl (startClock)

`RaceRecordingRepositoryImpl` assigns each race's id from an in-memory `AtomicLong` that resets to 1 on every process start, and `RaceRepositoryImpl.saveRecordedRace` deduplicates on that id alone with no window and no other uniqueness check, so a race recorded after a restart can collide with one already stored and be silently dropped. The identifier `startClock` assigns, which flows unchanged into `RecordedRacePayload.raceId` and into `saveRecordedRace`'s lookup, survives the process that made it instead of resetting on every start.

### §2.10 The recorded-race dedup check and write are not atomic

Bearer: RaceDao

`saveRecordedRace` looks up `sourceRaceId` and writes in two separate, untransacted Room calls, and `RaceEntity.sourceRaceId` carries no index or uniqueness constraint, so two concurrent calls can both pass the lookup before either writes and nothing at the schema level stops two rows from sharing one source id. The lookup and the write happen inside one `@Transaction` method that `saveRecordedRace` calls once. Second gap: `RaceEntity.sourceRaceId` gets a unique index, added through a new schema migration alongside the version bump.

### §2.11 Replacing the reference race exposes a moment with no reference at all

Bearer: RaceDao

`replaceReference` clears the reference flag and writes the new reference race in two separately-transacted Room calls, so a reader can observe a state with no reference between them. Clearing the flag and writing the new reference race happen in one Room transaction, through a single `@Transaction` method `replaceReference` calls instead of the two separate DAO calls it makes today.

### §2.12 `persist` force-unwraps a row it has just written

Bearer: RaceDao

`RaceDao.upsert` transacts only the write; `RaceRepositoryImpl.persist` then re-reads the row with a separate, unguarded `findById(raceId)!!`, so a delete landing between the two calls crashes the process instead of failing gracefully. The write and the read-back happen inside one transactional method that returns the resulting row or its absence, and `persist` surfaces that absence as a failure instead of force-unwrapping it. Second gap: `replaceReference`, which currently discards `persist`'s outcome and always returns success, must observe and propagate that outcome once it can carry absence.

### §2.13 Applying an incoming profile can silently lose a local edit

Bearer: ProfileRepository

`ProfileSyncPushService.applyProfile` writes an incoming profile's five fields through five independent read-modify-write calls, with no transaction and no lock spanning them, so a local edit landing between two of the five calls loses one of the two, whole-row, last writer winning. `ProfileRepository` exposes one operation that writes all five fields as a single atomic unit, wrapped in a Room transaction, and `applyProfile` calls it instead of the five independent updater calls.

## §3 Calculation

### §3.1 Two segment lookups assume an index that may not exist

Bearer: CumulativeDeltaEstimator

`CumulativeDeltaEstimator.estimate` finds the current segment with `first { it.index == currentSegmentIndex }`, safe today only because its caller always hands it a complete 30-entry list, and throws uncaught when that assumption breaks. `estimate` finds the current segment with a lookup that does not throw when the index is absent, and states what it returns in that case, consistent with its existing fallback outcome. Second gap, independent bearer: `RaceRecordingRepositoryImpl.undoLastMark` makes the identical assumption on its own lookup of the segment it just closed, and needs the same non-throwing lookup and a stated outcome for a missing segment.

### §3.2 A correction factor or a speed of zero makes pace, delta and trend meaningless

Bearer: PaceCalculator

`segmentPace` and `smoothedPace` multiply speed by the correction factor with no check on sign or zero, and always return a `Value`; `MainRacePageViewModel` then divides by that speed, `LapDeltaCalculator` divides the expected distance by it, and `TrendArrowCalculator` divides by a segment speed that can be zero — reaching `Long.MAX_VALUE`, `Infinity` or `NaN` instead of a stated fallback. `segmentPace` and `smoothedPace` return their existing `Fallback` outcome when the correction factor or the resulting speed is zero or negative, instead of wrapping it in a `Value`. Second gap: `LapDeltaCalculator.compute` does not rely solely on that upstream guarantee — it returns its own `Fallback` when the pace's speed is zero or negative, instead of computing a projection and flooring it through `maxOf`, which today masks a negative speed as a normal slow projection.

### §3.3 Two freshness windows treat a future reading as fresh

Bearer: SensorFreshnessWindow (evaluate)

`SensorFreshnessWindow.evaluate` and `PaceCalculator.smoothedPace`'s own window filter both compare an age against a window with `<=`, so a sample timestamped after now — a negative age — passes as fresh. `evaluate` rejects a negative age as stale, in addition to an age past the window. Second gap, independent bearer: `PaceCalculator.smoothedPace`'s own filter needs the identical guard, since it does not delegate to `evaluate`.

### §3.4 A missing or duplicate segment index corrupts a cumulative total

Bearer: SegmentBuilder (cumulativeDurationMs)

`cumulativeDurationMs` silently skips any index absent from the list it receives instead of returning null the way it already does for a present-but-null duration, and its caller falls that null back to `0`; separately, nothing on the read path deduplicates a segment index that `RaceDao.insertSegments` can silently replace rather than refuse on write. `cumulativeDurationMs` returns null as soon as any index in its range has no corresponding entry, treated the same as a null duration, and `RaceDetailViewModel.buildRow` shows the missing-value glyph instead of falling back to `0`. `CumulativeDeltaEstimator.estimate`, `.finalDelta` and `EndOfRaceViewModel.computeState` each reject a duplicate index instead of summing it twice, and `RaceDao.insertSegments` refuses a segment carrying an index already stored for that race instead of replacing it.

### §3.5 `HeartRateZoneCalculator` trusts a profile it never checks

Bearer: HeartRateZoneCalculator

`determine` and `ranges` guard only a null `hrMaxBpm`, so a zero maximum lands nearly every reading in zone five, a disordered threshold list classifies a high reading into a low zone, and a threshold list not of length four throws out of bounds — a shape already exercised in an existing test. `determine` and `ranges` treat a zero or negative `hrMaxBpm`, a non-increasing `zoneThresholds`, or a `zoneThresholds` of the wrong size the same way they already treat a null `hrMaxBpm`: an explicit `null` result, never a throw and never a zone computed from invalid values.

## §4 Transition

### §4.1 The waiting-for-phone screen never gives way

Bearer: WaitingForPhoneViewModel

`WaitingForPhoneViewModel.init` sets `hasReceivedProfile` once a profile carries a sync date, but nothing reads that field and no method of `WatchRaceNavigator` leaves `WAITING_FOR_PHONE`, so only restarting the application reaches the home screen. `WaitingForPhoneViewModel` calls a navigator method once the profile carries a sync date, the same way `SensorPermissionViewModel` calls `onSensorPermissionResolved` on its own resolution. Second gap: `WatchRaceNavigator` needs a method, analogous to `onSensorPermissionResolved`, that leaves `WAITING_FOR_PHONE` for `HOME` and is a no-op otherwise.

### §4.2 Every cold start blocks on the database before the first frame

Bearer: NavigationModule (provideWatchRaceNavigator)

`provideWatchRaceNavigator` calls `runBlocking { profileRepository.observe().first() }` while Hilt injects `MainActivity`'s fields, on the main thread inside `onCreate`, and `WatchRaceNavigator` bakes that value into its destination the first time it is read, with no path for a later value. The navigator learns whether a profile has synced from a suspension it performs itself, or from a value supplied once an asynchronous read elsewhere has completed, never by blocking the thread that constructs it — which requires `WatchRaceNavigator` to accept that condition as something re-evaluated after construction rather than a fixed constructor value.

### §4.3 Nothing routes back to a race in progress at start-up

Bearer: WatchRaceNavigator

`WatchRaceNavigator`'s first destination is chosen from the synced profile and the sensor permission alone, and nothing ever calls `RaceRecordingRepository.findInProgress()`, so a race that survives process death still opens on the home screen. `WatchRaceNavigator`'s first-read destination also accounts for a race in progress, chosen ahead of the profile-sync/sensor-permission checks, with `NavigationModule.provideWatchRaceNavigator` supplying the check lazily, read at `current`'s first access.

### §4.4 Tapping the complication does nothing after a process death

Bearer: MainActivity

`MainActivity.onNewIntent` reads the complication's destination extra, but `onCreate` never reads it and the manifest declares no `singleTop`, so a tap after the process died starts a fresh instance whose entry point ignores the extra. `MainActivity`'s manifest entry carries `android:launchMode="singleTop"` so a tap while already on top redelivers through `onNewIntent`, and `onCreate` reads the same extra off its own launch intent, navigating to the carried destination on both paths.

### §4.5 The inactivity timeout expires at the exact boundary every freshness window treats as valid

Bearer: WatchRaceNavigator (checkInactivity)

`checkInactivity` returns to `MAIN` once elapsed time is greater than or equal to the timeout, while every sensor freshness window in the project treats the same boundary instant as still within its window. `checkInactivity` treats the instant exactly at the timeout as still within it, matching the freshness windows' boundary rule.

## §5 External source

### §5.1 Four system calls are made and their outcome never read

Bearer: ExerciseSessionSystemImpl

`endExerciseSession` and `setDataDeliveryMode` call their platform methods and discard the returned `Task`, unlike `startExerciseSession` which already awaits its own; `DataLayerCapabilitySource`'s `init` block does the same with `addLocalCapability`. `endExerciseSession` and `setDataDeliveryMode` become `suspend` and await their `Task` the way `startExerciseSession` already does, reporting a failure instead of letting it pass unread; `DataLayerCapabilitySource` awaits `addLocalCapability`'s `Task` the same way its own `localNodeId`/`reachableNodeIds` already do. Second gap: neither caller runs in a coroutine today — `StopRaceController.stop` and `EndOfRaceViewModel.init` need to launch one before they can await the new `close()`, and `addLocalCapability`'s call needs to move out of `init` into a suspend step reached from `observeNodeConnected()`, since `init` cannot await anything.

### §5.2 The phone crashes at launch on a device without Health Connect

Bearer: PlatformModule (provideHealthConnectClient)

`provideHealthConnectClient` calls `HealthConnectClient.getOrCreate(context)` unconditionally, and `MainActivity` injects the result as a non-null field before `onCreate` runs, so a device without Health Connect crashes before any screen renders. `provideHealthConnectClient` checks `HealthConnectClient.getSdkStatus(context)` first and only builds the client when the SDK is available. Second gap: `MainActivity`'s injected client becomes optional and skips binding the permission host when absent; `HrHistoryReaderImpl`'s binding accommodates an absent client; `ProfileViewModel`/`ProfileUiState` gain a state distinct from "permission not yet granted" for "heart-rate history unavailable," and `ProfileScreen` renders it as text.

### §5.3 The watch never receives a single sensor reading

Bearer: ExerciseSessionManager

`MainRacePageViewModel.onHeartRateReading`/`onDistanceSample`/`onTick` and `PreparationViewModel.onHeartRateReading` have no caller anywhere in production, since no `MeasureClient` or `MeasureCallback` is registered anywhere in the module. Once the exercise session is open, something registers for the available sensor data types and forwards heart-rate readings to whichever screen's ViewModel is active, distance/speed samples to `MainRacePageViewModel.onDistanceSample`, and a periodic clock tick — independent of sensor delivery — to `MainRacePageViewModel.onTick`. Second gap: nothing today exposes a readings stream from a place reachable by the per-screen ViewModels built through `hiltViewModel`, and nothing provides a periodic tick mechanism anywhere in the module; both must be added for the fix to reach the screens.

### §5.4 A session this application already owns is opened a second time after process death

Bearer: RaceLaunchController (openPreparation)

`openPreparation` checks only `findInProgress()` to decide between resuming and opening fresh, never reconciling the manager's in-memory `sessionOpen` flag with a session already owned at the OS level, and `startExerciseSession` branches only on `OTHER_APP_IN_PROGRESS`, never on `OWNED_EXERCISE_IN_PROGRESS`, so a session lost to process death is neither detected nor closed and a second one opens on top of it. At preparation opening, the application checks whether it already owns an exercise session at the OS level: if it does and a race is in progress, the in-memory state is reconciled with the owned session; if it owns a session with no race in progress, that orphaned session is closed before a fresh one opens. Second gap: `ExerciseSessionSystem` needs a way to distinguish `OWNED_EXERCISE_IN_PROGRESS` from `NO_EXERCISE_IN_PROGRESS` with a new outcome variant, and `ExerciseSessionManager` needs an operation to adopt an already-running session and one to close an orphaned one — neither exists today.

### §5.5 The watch never switches its data-delivery mode

Bearer: MainActivity

`onEnterAmbient` and `onExitAmbient` only call `alwaysOnDisplayController`; neither touches `ExerciseSessionManager.onInteractivityChanged`, which reconfigures batching but is called only from a test. Entering ambient mode calls `exerciseSessionManager.onInteractivityChanged(false)`, and exiting calls `onInteractivityChanged(true)`, alongside the existing calls.

## §6 Synchronisation

### §6.1 The recorded-race listeners write to the database on the binder thread

Bearer: RecordedRaceListenerService

`onMessageReceived` calls `raceRepository.saveRecordedRace` directly, before any `launch`, so it runs on whatever thread Play Services handed the callback rather than on the service's own IO scope; `RecordedRaceAckListenerService` on the watch has no `CoroutineScope` at all and calls its own synchronous method the same way. `onMessageReceived` dispatches its database write onto the IO scope, sending the acknowledgement only once that write succeeds, preserving today's ordering. Second gap: `RecordedRaceAckListenerService` needs its own `CoroutineScope`, built on the same terms as the phone's, to dispatch onto.

### §6.2 `PayloadCodec` runs serialization on whatever thread calls it

Bearer: PayloadCodec

`encode` and `decodeProfileSync`/`decodeRecordedRace` build and read Java serialization streams synchronously, with the two listener services calling the decode functions outside any coroutine, before their own `serviceScope.launch`. `encode` and the two decode functions run their work on the IO dispatcher, the way the module's other sync boundaries already do. Second gap: turning them into suspend functions means each listener service's decode call moves inside its own `serviceScope.launch`, since it cannot be called from outside a coroutine as it stands.

### §6.3 A malformed message from the paired device crashes the other one

Bearer: ProfileSyncListenerService, RecordedRaceListenerService, RecordedRaceAckListenerService

All three services read incoming bytes with nothing guarding the call, on the binder thread Play Services delivers on, so a malformed or truncated payload crashes the receiving process. Each of the three `onMessageReceived` overrides catches the failure of its own read, drops the payload without acting on it, and reports the failure without letting the exception escape to the binder thread.

### §6.4 A failed acknowledgement is never checked

Bearer: RecordedRaceSyncService (sync)

`sync` discards the `Result` of `markSent`, whose contract already says it fails when no stored race matches, so the loop carries on and reports success regardless. `sync` checks that `Result`; on failure it stops the loop immediately and reports a failure state that carries the id of the race it stopped on. Second gap: `RecordedRaceSyncState.Failure` is a bare object today and must carry that raceId for the state to say which race the sync stopped on.

### §6.5 Cancellation is swallowed as a send failure

Bearer: DataLayerMessageChannel, WearableProfileSyncTransport, WearableRecordedRaceTransport, WearableRecordedRaceAckTransport

All four transports catch `Exception` and return `false`, and `CancellationException` is a subtype of `Exception`, so a scope torn down mid-send reports a delivery failure instead of unwinding. Each of the four catches `CancellationException` first and rethrows it, before its existing catch, the way `HrHistoryReaderImpl` already does — the fix repeats at all four sites, since none is reached through another, and `MessageChannel.send`'s own documentation is updated to match.

### §6.6 Five catch sites swallow their exception without a trace

Bearer: DataLayerMessageChannel, WearableProfileSyncTransport, WearableRecordedRaceTransport, WearableRecordedRaceAckTransport, HrHistoryReaderImpl

All five catch sites discard what they caught and return a plain failure value, with no logging utility of any kind existing anywhere in the project, so an unreachable node, a serialisation bug, a revoked permission and a corrupt record are indistinguishable from outside. Each of the five logs what it caught before returning its existing failure value, at a level matching how much it matters. Second gap: in the two payload transports, the call to `PayloadCodec.encode` moves out of the `try` that guards `channel.send`, so an encoding failure is distinguished from a delivery failure.

### §6.7 The eight serialized snapshot classes declare no version id

Bearer: PayloadCodec

Kotlin derives each class's `serialVersionUID` from its structure, and the two applications ship independently, so a field added, reordered or retyped on one side silently changes the identifier and breaks decoding on the other. Each of the eight classes declares its own fixed `serialVersionUID`.

### §6.8 A push refused because a race is running can still let one through

Bearer: ProfileSyncPushService (applyIncoming)

`onMessageReceived` computes whether a race is running at the instant the message arrives and hands that boolean to a coroutine that runs later, so a race started in between is invisible to `applyIncoming`, which trusts the stale value. `applyIncoming` determines whether a race is in progress itself, immediately before deciding to apply or refuse the payload, instead of trusting a value computed earlier by its caller. Second gap: `ProfileSyncPushService` needs a way to reach `RaceRecordingRepository.findInProgress()` at the moment it acts, but that repository's sole implementation lives in `:app-wear`, and `:app-phone`'s DI graph provides no binding for it today.

### §6.9 `RecordedRaceSyncService.sync` is called with a hardcoded race-in-progress state

Bearer: HomeViewModel

Both of `HomeViewModel`'s calls to `sync` hardcode `raceInProgress = false`, while `ProfileSyncListenerService` derives the same condition from `findInProgress()` on every message it receives. Both of `HomeViewModel`'s calls derive `raceInProgress` the same way `ProfileSyncListenerService` does. Second gap: `HomeViewModel` does not receive `RaceRecordingRepository` today, and needs it injected before it can compute the condition.

### §6.10 Nothing on the phone pushes when something changes

Bearer: RaceDetailViewModel, ImportPreviewViewModel

Renaming, deleting, importing or setting a race as reference calls no push; the only call to `ProfileSyncPushService.push` sits behind the profile screen's sync button and a link-established collector, both scoped to `ProfileViewModel`. Each of `RaceDetailViewModel`'s three action handlers and `ImportPreviewViewModel.onSaveClicked` pushes after its write succeeds, calling `ProfileSyncPushService.push` the same way `ProfileViewModel.pushProfile` already does. Second gap: neither ViewModel declares `ProfileSyncPushService` or `Clock` as a constructor dependency today, though both are already provided app-wide through Hilt.

### §6.11 A watch-computed correction factor is undone by the next sync

Bearer: RecordedRaceListenerService

`EndOfRaceViewModel.init` writes the watch's own correction factor at the end of a recorded race, but `RecordedRacePayload` carries no `retainedFactors`, so the phone's stored race and its `correctionFactor` never reflect it, and the next `ProfileSyncPushService.push` sends the phone's unchanged value back down, undoing the watch's computation. Receiving a recorded race on the phone derives the phone's `correctionFactor` from that race's `retainedFactors`, the same rule `EndOfRaceViewModel` applies on the watch, and writes it before the next push carries it back. Second gap: `RecordedRacePayload`, its snapshot type, `PayloadCodec`'s encode/decode, and `RaceRepository.saveRecordedRace`'s signature all need to carry `retainedFactors` (and `rejectedCalibrations`), since none of them do today.

## §7 Background work

### §7.1 Sixteen call sites reach a repository or service outside a coroutine

Bearer: ProfileViewModel, RaceDetailViewModel, ImportPreviewViewModel, PasteResultViewModel, ControlViewModel, EndOfRaceViewModel, HomeViewModel, PreparationViewModel, ProjectionViewModel, MainRacePageViewModel, SensorPermissionViewModel

Each of these ViewModels reaches a repository, controller or manager method directly from a button handler or a property initialiser, outside `viewModelScope.launch`, while the same class runs its other work inside that scope — and the repositories reached this way call Room synchronously with no dispatcher indirection, so the call runs on the caller's own thread. Every one of the sixteen call sites runs inside `viewModelScope.launch` (or, for a constructor-time read, whatever mechanism replaces it), consistently with how each class already handles its other calls.

### §7.2 Nothing in the project turns a boundary failure into a value

Bearer: RecordedRaceListenerService, ProfileSyncListenerService, RaceRepositoryImpl, ProfileRepositoryImpl, RaceRecordingRepositoryImpl

No `catch` exists in `:core-domain` or `:core-data`, no flow collection is guarded, and no scope installs a `CoroutineExceptionHandler`, so a Room failure, a decode failure or a raised flow takes its caller — and, for an unguarded scope, the whole process — down with it. Each boundary catches what it can raise and returns it as a failure the way `ExerciseSessionSystemImpl.startExerciseSession` already does, each flow collection attaches a `.catch` defining what it does when its source fails, and every scope that launches work not bounded by a caller installs a `CoroutineExceptionHandler`.

## §8 Journey

## §9 Screen

### §9.1 Six UI-state fields are written and read nowhere

Bearer: SensorPermissionUiState, WaitingForPhoneUiState, ProfileUiState, RaceDetailUiState, SegmentRowUiState

`SensorPermissionUiState.resolvedState`, `WaitingForPhoneUiState.hasReceivedProfile`, `ProfileUiState.distanceLabel`/`pressDurationLabel`, `RaceDetailUiState.raceId` and `SegmentRowUiState.index` are each written by their ViewModel and never read by any screen — the behaviour they were meant to signal already happens elsewhere in the same call site. Each of the six fields is dropped from its `UiState` data class, and the write that populated it is removed from its ViewModel, independently of the navigator fix that touches `hasReceivedProfile`'s own call site elsewhere.

### §9.2 `WatchApp` reads a repository and a permission on every recomposition

Bearer: WatchApp

The `MAIN`, `PROJECTION` and `CONTROL` branches call `findInProgress()`, and `MAIN` also calls `isGranted()`, directly in the composable body with nothing remembering the result, so each call re-runs on every recomposition rather than once per navigation. Each of these calls is read once per entry into its branch and held in a `remember`, not re-invoked on every recomposition.

### §9.3 Opening a race detail crashes on any incomplete race

Bearer: RaceDetailViewModel (buildRow)

`buildRow` looks each of the 30 indices up with `first { }`, and a race stopped early stores fewer than thirty segments — a segment never reached is absent from the list, not merely empty — so the lookup throws and the screen crashes. `buildRow` looks up the segment for an index without assuming it is present, and renders the same missing-value row it already renders for a null duration when none is found.

### §9.4 Seven call sites drop a `Result` their caller should act on

Bearer: PreparationViewModel, ControlViewModel, ImportPreviewViewModel, RaceDetailViewModel, ProfileSyncPushService

`onLaunchClicked`, `onUndoClicked`/`onStopConfirmed`, `onSaveClicked`, `onDeleteConfirmed`/`onRenameConfirmed` and `ProfileSyncPushService`'s two `markSyncSuccess` calls each act only on success, so a failure at any of them is silent — including a refused rename, which closes the dialog as if it had saved. Each of the seven call sites reads the `Result` it already receives and acts on a failure the way `ProfileViewModel` already does on its own four setting handlers, surfacing a rejection distinctly from doing nothing. Second gap: none of the five affected screens carries a rejection or failure text resource for launch, undo, stop, import-save, delete or rename today; each needs one.

### §9.5 Five unchecked casts can fail on their own paths

Bearer: PhoneApp, PayloadCodec, HapticFeedbackImpl

`PhoneApp` casts the composition context and two parse-result branches unchecked; `PayloadCodec.toObject` casts a deserialised object to its expected type unchecked; `HapticFeedbackImpl` casts a possibly-absent system service unchecked. Each of the five handles the shape it does not expect instead of throwing: `PhoneApp` guards its three casts, `PayloadCodec.toObject` turns a mismatch into the codec's own typed decoding failure, and `HapticFeedbackImpl` tolerates an absent service the same way it already tolerates no vibrator.

### §9.6 Ambient mode is computed and thrown away

Bearer: MainActivity

`WatchApp` never reads the `displayMode`/`refreshIntervalMs` `MainActivity` passes it, `MainRacePageScreen` has no power-save branch, and `AlwaysOnDisplayController` is a plain field that resets to normal on every recreation instead of a singleton. `WatchApp`'s `MAIN` branch passes `displayMode` and `refreshIntervalMs` on to `MainRacePageScreen`, which renders its already-declared power-save layout while in power-save and its normal layout otherwise, and `AlwaysOnDisplayController` becomes a Hilt singleton so its state survives a recreation.

### §9.7 `DisplayFormatter` garbles every negative duration

Bearer: DisplayFormatter

`formatMinutesSeconds` and `formatDurationTotal` divide and take the remainder of a negative total directly, rendering minus ninety seconds as "-1:-30," while `formatDelta` in the same file already extracts the sign and formats the absolute value correctly. Both functions extract the sign first, compute from the absolute value, and prefix a minus sign only when the input was negative, the same pattern `formatDelta` already applies.

### §9.8 No text is bounded on screen

Bearer: RaceListScreen (RaceListCard)

No `Text` composable in either module sets `maxLines` or overflow handling, so a long race name wraps without limit on the race list, the detail title, the delete confirmation, the watch's history, and both reference-race labels — and the race list row's name can push the total time out of place, having no weight in its row. Every `Text` rendering a race name or a label built from one sets a `maxLines` and `TextOverflow.Ellipsis` sized to its context, and the race list row's name also gets a weight so it cannot push the total time out of place.

### §9.9 A sync timestamp in the future reads as older than it is

Bearer: DisplayFormatter (formatDateRelative)

`formatDateRelative` only tests for today and yesterday, so an instant whose date is after now — a clock stepped back, or drift between devices — falls through to the same `Earlier` branch used for a genuinely old sync. `formatDateRelative` checks whether the given instant's date is after now's and returns a value distinct from `Earlier` for that case, which requires either a new `DateDisplay` subtype or reusing `Today`, and the caller's exhaustive `when` follows whichever is chosen.

### §9.10 The lap-delta column shows a value no calculation covers

Bearer: RaceDetailViewModel (buildRow)

`buildRow` computes a plain truncated subtraction for the delta column on all thirty rows of a stored, finished race, gated only on the reference segment's duration being present, while the calculation the technical document names for a lap delta is a live, continuously-recomputed projection meant for a race in progress and is never called from this file. Every row of that column names the calculation behind it for a finished race — which calculation, if any, backs a RUN row's delta and what backs the twenty-two non-run rows — and a row no calculation covers shows nothing rather than a number.

### §9.11 Every sensor value hits its freshness boundary on every power-save refresh

Bearer: MainRacePageViewModel

`computeState` evaluates freshness identically regardless of display mode, and the power-save refresh cadence matches the freshness window exactly, so every power-save refresh lands a reading exactly at the edge with no distinct outcome for that mode. `MainRacePageViewModel` receives the current display mode and, in power-save, keeps a value whose freshness has just lapsed shown and dimmed instead of falling back to a dash, while normal mode keeps its existing fallback. Second gap: nothing in the module today represents "shown but dimmed" distinct from a fresh or an absent value; the UI state needs it added.

## §10 Text

### §10.1 A bound violation shows a constraint message that does not exist

Bearer: RaceDetailViewModel

`onRenameConfirmed` discards `rename`'s `Result` and always closes the dialog, so a rejected rename — outside the one-to-forty trimmed-character bound — looks identical to a successful one, and no text resource exists to name that bound. `onRenameConfirmed` reads the `Result`; on failure it keeps the dialog open and shows a constraint message naming the bound, backed by a new key added to the screen's text catalogue.

## §11 Access

### §11.1 The connectivity permission implementation is duplicated per module

Bearer: ConnectivityPermissionSystemImpl

`ConnectivityPermissionSystemImpl` exists once per application module with identical bodies, each instantiated by its own module's `ActivityBoundPermissionHost`, so a correction made to one leaves the other untouched. One `ConnectivityPermissionSystemImpl` is compiled once and used by both modules' `ActivityBoundPermissionHost`. Second gap: no existing module can hold a single shared implementation without contradicting the current placement rule for OS-permission code, since it cannot move into `:core-domain` (no Android dependency), into either application module (they never import each other), or cleanly into `:core-sync` under today's rule — placing it requires either an Android-capable shared module or a change to that rule.

## §12 Lifecycle

### §12.1 A listener service's coroutine scope outlives the service

Bearer: ProfileSyncListenerService

`ProfileSyncListenerService` builds a `serviceScope` and never overrides `onDestroy`, so the scope and any coroutine launched into it outlive the service and stop only when the system kills the process. `ProfileSyncListenerService` overrides `onDestroy`, cancels `serviceScope` there, then calls `super.onDestroy()`. Second gap, independent bearer: `RecordedRaceListenerService` needs the identical fix on its own `serviceScope`, since neither symbol follows from the other.

### §12.2 Fourteen ViewModel fields are lost on rotation

Bearer: RaceDetailViewModel, ProfileViewModel, ImportPreviewViewModel, PasteErrorViewModel, PasteResultViewModel, MainRacePageViewModel, ProjectionViewModel, ControlViewModel, PreparationViewModel

None of these nine ViewModels takes a `SavedStateHandle`, so a configuration change loses each one's in-progress dialog state, cached values, rejection messages or sensor-derived fields. Each of the nine takes a `SavedStateHandle` in its constructor and writes to it the fields among its own that must outlive a configuration change. Second gap: `ImportPreviewViewModel` and `PasteErrorViewModel` are built from an `@Assisted` value that is not `Parcelable` and cannot become one, so the fix saves the primitives it is built from rather than the value itself; `MainRacePageViewModel`, `ProjectionViewModel` and `ControlViewModel` are built from `@Assisted` domain values the same way, and what they retain is the identifying value re-read from the repository, not the object itself.

### §12.3 The phone's navigation stack does not survive a process death

Bearer: PhoneNavigator

`PhoneNavigator`'s back stack is a plain in-memory list, reseeded to the race list alone whenever Hilt builds a fresh instance after process death, with nothing reading or writing `savedInstanceState`. The back stack is written to a persisted saved state whenever it changes, and restored from it when the navigator is constructed, so the app reopens on the last-seen destination instead of always on the race list. Second gap: restoring a `RaceDetail` destination requires its race id to be serialisable in that saved state; the `ImportPreview`/`PasteError` destinations are one-time snapshots of unsaved state and need that snapshot to survive too, or exclusion from what is restored.

### §12.4 A field being edited is lost on rotation before the user saves

Bearer: ProfileScreen

`hrMaxEditValue` and the screen's other in-progress field values are held in a plain `remember`, so a rotation discards whatever the user has typed and closes the edit dialog. `hrMaxEditValue` and the screen's other in-progress field values are held in `rememberSaveable`, the same as every other in-progress input.

## Gaps set aside

- Opening the profile screen crashes the application: the manifest already declares the permission, `ProfileViewModel.init` already requests it before reading, and `HrHistoryReaderImpl` already returns an empty list on any failure — confirmed already correct, per `investigation/G04.md`.
- The connectivity permission still redirects to settings when granted: `requestAgain` already checks `isGranted()` first and never reaches the redirect path when the permission is granted, with a passing test for exactly this case — confirmed already correct, per `investigation/G28.md`.
- A segment name is both a domain value and a displayed string: every displayed name already resolves through the text catalogue (`PhoneStringResources.segmentName`/`WatchStringResources.segmentName`), never a literal in code — confirmed already correct, per `investigation/G64.md`.
