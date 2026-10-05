- Nothing in the application respects the thread the database demands,
  and it shows in two ways: a crash where Room checks, a freeze where
  something blocks. Fourteen interfaces reach outside the process
  without saying so — `ProfileRepository`, `RaceRepository`,
  `RaceRecordingRepository` and `WatchHistoryStore` touch the database;
  the four permission contracts touch the OS and the preferences file;
  `ExerciseSessionSystem`, `ExerciseSessionManager`, `HapticFeedback`,
  `AmbientBinder`, `CapabilitySource` and `Clock` touch a system
  service — and not one of their methods is `suspend`, so no caller can
  do anything about the thread it is on.
  `ProfileRepositoryImpl.currentOrDefault` hides a `runBlocking` behind
  that silence; `RaceRepositoryImpl` and
  `WatchHistoryStoreImpl` call their DAO synchronously outright. No
  implementation switches thread, and no `Flow` out of Room carries a
  `flowOn`.

  📌 **Six interfaces already do it right** — `HrHistoryReader`,
  `HrPermissionSystem`, the three transports and `MessageChannel` are
  `suspend` where they reach out. The other fourteen follow: `suspend`
  on the interface, the dispatcher switched inside the implementation,
  `flowOn` on the flows, and nothing trusting the thread of whoever
  calls it. Every caller follows from that — a ViewModel launches in
  `viewModelScope`, a domain service awaits, and nothing blocks a
  thread waiting for another.

- Sixteen call sites reach a repository, a domain service or a platform
  piece from outside a coroutine, on nine of the fifteen ViewModels.
  `ProfileViewModel` does it on its four setting handlers;
  `RaceDetailViewModel` on a property initialiser reading the race and
  on its reference, rename and delete handlers; `ImportPreviewViewModel`
  when saving; `PasteResultViewModel` on a property initialiser reading
  the clock; `ControlViewModel` when undoing and when stopping;
  `EndOfRaceViewModel` in its `init`, closing the exercise session and
  writing the correction factor; `HomeViewModel` on a property
  initialiser reading the permission; `PreparationViewModel` when
  launching a race; `ProjectionViewModel` and `MainRacePageViewModel`
  when marking a segment; `SensorPermissionViewModel` when resuming.
  Each of them runs its work in `viewModelScope`.

- Marking a segment holds a lock while it waits on the database, and
  everything reaching that lock freezes with it.
  `RaceRecordingRepositoryImpl` wraps eight of its nine public methods
  in `synchronized(lock)`, and `markSegment` — inside that block —
  reads the profile through a `runBlocking` on a Room-backed flow.
  Three independent paths reach the same lock while it is held: both
  race screens, the `WatchApp` composable which calls `findInProgress()`
  on every recomposition, and the watch-face complication's
  `onComplicationRequest`. A repository never blocks a thread waiting
  for a flow, and never holds a lock across a suspension: the value it
  needs is read as a suspension, in the coroutine its caller already
  runs in. That `runBlocking` also escapes the
  method's own contract: `markSegment` returns `Result<Race>`, and an
  exception raised inside the block passes straight through the return
  — a database failure there is never the `Result.failure` the
  signature promises.

- Opening the profile screen crashes the application. `HrHistoryReaderImpl`
  reads heart-rate history from Health Connect, which requires
  `android.permission.health.READ_HEART_RATE`; `app-phone` does not
  declare it, and the `SecurityException` reaches the main thread
  unhandled. The phone declares that permission, the profile screen
  requests it before reading, and a refused permission leaves the
  stored maximum untouched rather than raising. A read that fails
  returns no values.

- The paste parser rejects a real Hyresult result. A pasted result
  opens on a header row — `Split`, `Time of Day`, `Time`, `Diff` — and
  the parser reads it as a split, which shifts every column by one. It
  closes on a `Total time` row that names no split. Durations past the
  hour read `1:01:40`, three parts, where the parser expects two. The
  header row and the closing total are skipped, and a duration is read
  whether it carries hours or not.

- The waiting-for-phone screen never gives way. It is shown until a
  profile has been received, and nothing acts on that condition once
  it is met: `WaitingForPhoneViewModel` collects the profile and sets
  `hasReceivedProfile` when one carries a sync date, no code reads that
  field, and no method of `WatchRaceNavigator` leaves
  `WAITING_FOR_PHONE`. Only restarting the application gets past it.
  The screen gives way to the home screen as soon as a profile has been
  received, while the application is running.

- Six UI-state fields are written and read nowhere.
  `SensorPermissionUiState.resolvedState` is set four times by its
  ViewModel and no composable reads it;
  `WaitingForPhoneUiState.hasReceivedProfile` likewise;
  `ProfileUiState.distanceLabel` and `ProfileUiState.pressDurationLabel`
  are shadowed on screen by local values of the same name built from
  the text catalogue; `RaceDetailUiState.raceId` and
  `SegmentRowUiState.index` are carried and never displayed. A field a
  screen never reads leaves the ViewModel, unless a screen starts
  reading it — say which, per field.

- Every cold start blocks on the database before the first frame.
  `NavigationModule.provideWatchRaceNavigator` reads
  `runBlocking { profileRepository.observe().first() }` to know whether
  a profile has been synced, and Hilt resolves that `@Provides` while
  injecting `MainActivity`'s fields — inside `onCreate`, on the main
  thread. The navigator learns that from a suspension, or from a value
  it is given once the read has happened, never by blocking the thread
  that builds it.

- The phone's recorded-race listener writes to the database on whatever
  thread Play Services hands it. `RecordedRaceListenerService` holds a
  `CoroutineScope` on `Dispatchers.IO` and uses it for the
  acknowledgement alone: `raceRepository.saveRecordedRace(...)` runs
  before any `launch`, straight inside `onMessageReceived`. The write
  goes on that scope, like the acknowledgement it precedes.
  `RecordedRaceAckListenerService` on the watch has no scope at all and
  gets one on the same terms.

- Neither listener service ever cancels its `CoroutineScope`. The two
  `serviceScope` values are the only ones built in production code, and
  neither class overrides `onDestroy`: a coroutine launched there
  outlives the service and stops only when the system kills the
  process. Each service cancels its scope when it is destroyed.

- Four system calls are made and their outcome never read.
  `ExerciseSessionSystemImpl` calls `endExerciseAsync()` and
  `overrideBatchingModesForActiveExerciseAsync(...)` and drops the
  `Task` each returns; `DataLayerCapabilitySource` calls
  `addLocalCapability(...)` in its `init` and drops it too. A failure
  in any of them is silent today — the session may stay open, the
  capability may never be advertised. Each of them is awaited, and a
  failure is reported the way the other platform calls report theirs.

- `WatchApp` reads a repository and a permission on every
  recomposition. Its `MAIN`, `PROJECTION` and `CONTROL` branches call
  `raceRecordingRepository.findInProgress()`, and the `MAIN` branch
  also calls `sensorPermissionManager.isGranted()` — directly in the
  composable body, with nothing remembering the result. Both are read
  once per navigation rather than once per frame.

- `PayloadCodec` runs Java serialization on whatever thread calls it.
  Its `encode` and `decode` build and read `ObjectOutputStream` /
  `ObjectInputStream` synchronously, with no suspension point, inside
  each transport's `suspend fun send`. The buffers are in memory, so
  nothing waits on a device — but a summarised history of twenty races
  is real work on a caller's thread, and the codec is a boundary like
  any other. It does that work on the IO dispatcher, the way every
  other boundary does.

- Nothing in the project turns a failure into a value, at any of the
  three places it could. Seven `catch` blocks exist across three
  hundred files, none in `:core-domain` or `:core-data`, and no
  `runCatching` anywhere: the domain models failure with `Result`, and
  the boundaries that actually fail — Room, Health Connect, Health
  Services, the Data Layer, deserialisation — raise straight through
  it. No flow collection is guarded either: seven `collect` sites in
  `:app-wear` and the two collectors of the link-state flow carry no
  `catch`, so a flow that raises takes its ViewModel with it. And no
  scope installs a `CoroutineExceptionHandler` — neither a
  `viewModelScope`, nor either `serviceScope`, nor anything Hilt
  provides — so what escapes reaches the default handler and takes the
  process.

  📌 **Each boundary catches what it can raise and returns it as a
  failure**, the way `ExerciseSessionSystemImpl` already does; each
  collection says what it does when its source fails; each scope
  handles what its work can raise.

- Opening a race detail crashes on any incomplete race.
  `RaceDetailViewModel` line 174 looks each index from 1 to 30 up in
  `race.segments` with a `first { }`, and `saveRecordedRace` stores an
  incomplete race with fewer than thirty segments — a segment never
  reached is absent from the list, not merely empty. That is exactly
  the shape the watch sends when a race is stopped early, and no test
  covers it: the generator always builds thirty. It renders the race
  the way the screen describes for an incomplete one.

- Two more lookups make the same assumption on the same data.
  `CumulativeDeltaEstimator` finds the current segment by index with
  nothing checking it exists, and `RaceRecordingRepositoryImpl` finds
  the segment it just closed the same way — safe today only by an
  invariant held in another file, which neither call site can see.
  Each says what it does when the segment is not there.

- A malformed message from the paired device crashes the other one.
  All three listener services read incoming bytes with nothing guarding
  the call, on the binder thread Play Services delivers on:
  `ProfileSyncListenerService` and `RecordedRaceListenerService` decode
  a payload, and `RecordedRaceAckListenerService` reads a long out of a
  buffer that raises on anything shorter than eight bytes. A payload
  that fails to read is dropped and reported, never raised.

- The phone crashes at launch on a device without Health Connect.
  `PlatformModule` calls `HealthConnectClient.getOrCreate(context)`,
  which raises when Health Connect is not installed, and
  `MainActivity` injects that singleton at field injection. The client
  is obtained only after `getSdkStatus()` says it can be, and the
  profile screen states that the heart-rate history is unavailable
  rather than the application failing to start.

- A recorded race can be reported as synced when it was not.
  `RecordedRaceSyncService` line 52 drops the `Result` of
  `markSent`, whose contract says it fails when no stored race matches;
  the loop carries on and `sync()` reports success regardless. A
  failure there stops the loop reporting success, and says which race
  it stopped on.

- Seven more calls drop a `Result` their caller should act on.
  `PreparationViewModel` launches a race and navigates to the race
  screen without looking at whether the clock started;
  `ControlViewModel` undoes and stops without a failure branch;
  `ImportPreviewViewModel` saves without one, so a failed import is a
  silent no-op; `RaceDetailViewModel` deletes without one, and renames
  without one — `rename` validates and refuses an empty name or one
  past forty characters, so the dialog closes, the old name stays, and
  nothing is said; `ProfileSyncPushService` drops two. Each acts on the
  failure the way `ProfileViewModel` already does on its own.

- Room reads raise on data it wrote itself. `HyroxTypeConverters` calls
  `valueOf` on a stored enum name and `toInt()` on a stored threshold
  string, on every read of a race or a profile: a value that no longer
  matches raises where it is read, with no way for a caller to
  recover. Both apps also build their database without a destructive
  fallback and without guarding the migration, so a schema off the
  declared path raises at the first query.

- Cancelling a coroutine is swallowed as a send failure. The four
  transports of `:core-sync` — `MessageChannel`,
  `WearableProfileSyncTransport`, `WearableRecordedRaceTransport`,
  `WearableRecordedRaceAckTransport` — catch `Exception` and return
  `false`, and `CancellationException` is an `Exception`: a scope torn
  down mid-send reports a failure instead of unwinding. Cancellation is
  rethrown before anything else is caught, the way
  `HrHistoryReaderImpl` already does.

- Five catch sites swallow without a trace. The four transports return
  `false` and `HrHistoryReaderImpl` returns an empty list, and none of
  them logs what it caught: an unreachable node, a serialisation bug, a
  revoked permission and a corrupt record are indistinguishable from
  outside. Each logs what it swallowed, at a level matching how much it
  matters. `MessageChannel` also catches around
  `PayloadCodec.encode`, so a data-model bug reads as a network drop —
  the catch covers the send alone.

- The eight `Serializable` classes of `PayloadCodec` declare no
  `serialVersionUID`. Kotlin derives one from the structure, and the
  two applications ship independently: a field added, reordered or
  retyped on one side changes that identifier silently, and every
  decode on the other side fails. Each class declares its own, fixed.

- `markSegment` escapes its own contract. It returns `Result<Race>`,
  and the `runBlocking` inside it raises straight past that return: a
  database failure there is an exception, not the `Result.failure` the
  signature promises. Everything that can fail inside it comes back as
  a failure.

- Five unchecked casts can fail on their own paths. `MainActivity` on
  the phone casts a parse result to `Success` and to `Failure` on two
  branches, safe only by the discipline of three separate classes with
  no typing behind it, and casts the local context to
  `ComponentActivity`; `PayloadCodec` casts a deserialised object to
  its expected type, so bytes of one kind read as another raise;
  `HapticFeedbackImpl` casts a system service the platform documents as
  possibly absent. Each of them handles the shape it does not expect.

- Two `!!` rest on invariants nothing enforces.
  `HyresultResultParser` asserts a station exists for every index while
  building its expected labels, which ties two files together with
  neither typing nor a test — a change to either makes the whole parser
  fail as its class loads. `RaceRepositoryImpl` asserts a row exists
  right after writing it, which a rolled-back transaction or a
  concurrent delete disproves. Both state what they do when the value
  is absent.

- The connectivity permission still redirects to the settings when it
  is already granted. `ConnectivityPermissionSystemImpl.canShowSystemPrompt`
  reads its first-request flag and then the platform's rationale
  helper, and never asks whether the permission is granted — that
  helper
  returns false both for a granted permission and for a permanently
  refused one. That is the
  fault already corrected on the sensor side, in
  `SensorPermissionManager.requestAgain`, and never carried across.

- `ConnectivityPermissionSystemImpl` exists twice, once per application
  module, with identical bodies. A correction to one leaves the other
  as it was, and the two have already drifted apart from the sensor
  equivalent that way. One implementation serves both modules.

- A race in progress survives nothing. `RaceRecordingRepositoryImpl` is
  the only recorder in the project and holds every race in a
  `LinkedHashMap` in memory — segment index, durations, marks,
  `currentSegmentOpenedAt`, calibration factors, and the id counter
  itself — with no DAO call in `startClock`, `markSegment`,
  `undoLastMark`, `stopRace` or `markSent`. The repository, the four
  race controllers and `ExerciseSessionManager` are all singletons, so
  the whole set is rebuilt empty when the process dies: the race is
  gone, and `findInProgress()` returns nothing to the five places that
  ask it. A race in progress is written down as it happens and read
  back at start-up, so that the watch can be killed mid-race and pick
  the race up where it left off.

- Nothing routes back to a race in progress at start-up.
  `WatchRaceNavigator` decides its first destination from the synced
  profile and the sensor permission alone, and never asks
  `findInProgress()`. Even once a race survives the process, the user
  lands on the home screen with no trace of it. The first destination
  accounts for a race in progress.

- The watch never receives a single sensor reading. On
  `MainRacePageViewModel`, `onHeartRateReading`, `onDistanceSample` and
  `onTick`, and `onHeartRateReading` on `PreparationViewModel`, have no
  caller anywhere in production — no `MeasureClient` and no
  `MeasureCallback` is registered in the module. The preparation screen
  shows its heart-rate label with nothing beside it, the race pages
  never show a zone, and the correction factor has no measured distance
  to work from. Something registers for the data types the session
  offers and feeds those handlers while a race runs.

- The exercise session outlives the application that opened it.
  `ExerciseSessionManager.close()` is called from two places only —
  `StopRaceController.stop()` on success and `EndOfRaceViewModel.init` —
  and from nothing bound to a lifecycle. `startExerciseSession` checks
  `exerciseTrackedStatus` but branches on `OTHER_APP_IN_PROGRESS` alone,
  never on `OWNED_EXERCISE_IN_PROGRESS`: a session this application
  opened and lost to a process death is neither detected nor closed,
  and the next launch opens a second one on top of it. The application
  finds its own session again at start-up and either resumes it or
  closes it before opening another.

- Ambient mode is computed and thrown away. `MainActivity` binds the
  ambient observer, calls `enterPowerSave`/`exitPowerSave` and passes
  the resulting `displayMode` and `refreshIntervalMs` to `WatchApp` —
  whose body references neither, anywhere in the module. And
  `AlwaysOnDisplayController` is a plain field on the activity rather
  than a singleton, so its mode resets to NORMAL on every recreation,
  a rotation included. The race pages render their power-save layout
  and refresh on the ambient beat, from a controller whose state
  survives the activity.

- The watch never switches its data-delivery mode.
  `ExerciseSessionManager.onInteractivityChanged`, which exists to move
  Health Services between continuous and batched delivery when the
  screen stops being interactive, has no caller outside its own test.
  It is called on the ambient transitions the activity already
  observes.

- Tapping the complication does nothing in the case it exists for.
  `WatchRaceComplicationDataSourceService` builds a `PendingIntent`
  carrying the destination to open, and `MainActivity` reads that extra
  in `onNewIntent` alone — which fires only when an activity is already
  alive. The manifest declares no `singleTop`, so a tap after the
  process died runs a fresh `onCreate` that never looks at the intent's
  extras, and the destination is lost exactly when the complication is
  most useful. The activity reads that extra on both paths.

- Fourteen ViewModel fields are lost on rotation. On the phone,
  `RaceDetailViewModel` holds its dialog state and a cached race;
  `ProfileViewModel` holds the profile, the connectivity flag, the sync
  state and four rejection messages; `ImportPreviewViewModel`,
  `PasteErrorViewModel` and `PasteResultViewModel` hold state built
  from an assisted value and never written down before the user saves.
  On the watch, `MainRacePageViewModel` holds the race, the clock, the
  last heart rate and zone, and four distance and speed values;
  `ProjectionViewModel` and `ControlViewModel` hold the race;
  `PreparationViewModel` holds the reference race and an `opened` flag.
  No ViewModel in either module receives a `SavedStateHandle`. Each
  says which of its fields must outlive a configuration change, and
  keeps those where they will.

- The phone's navigation stack is a plain list in memory, held by a
  singleton, with nothing tied to a saved state: whatever screen the
  user was on, the application reopens on the race list. The stack is
  restored with the application.

- `ProfileScreen` keeps the heart-rate edit value in a plain `remember`,
  so what the user has typed is lost on a rotation, before any process
  death. It is remembered across configuration changes, like every
  other in-progress input.

- `PreparationViewModel` silently starts a new preparation instead of
  resuming. Its `opened` flag guards `openPreparation` against a double
  call within one instance and comes back false on a new one, so after
  a process death it calls `openPreparation` again — which, finding no
  race in progress, opens a fresh preparation rather than surfacing
  `PreparationState.Resuming`, the state that exists for exactly this
  case.

- `correctionFactor` is the only profile value with no validation
  anywhere. The four others are bounded on write and re-checked when a
  sync payload applies them; this one is written unchecked from
  `EndOfRaceViewModel`, applied unchecked from a sync payload, and
  never re-read with a guard. The measured factor is bounded to a
  trusted range, but the blend of measured and previous is not, and the
  previous value is never validated on the way in — so a corrupt value
  survives every race and feeds itself. It is bounded where it is
  written, and a value outside those bounds is refused the way the
  other four are.

- A correction factor or a speed of zero makes pace, delta and trend
  meaningless without raising. `PaceCalculator` multiplies speed by the
  factor with no check on sign or zero; `MainRacePageViewModel` then
  divides a thousand by that speed, `LapDeltaCalculator` divides the
  expected distance by it, and `TrendArrowCalculator` divides by a
  segment speed that can be zero — the first two reach `Long.MAX_VALUE`
  through `Infinity`, and the third returns `NaN`, which fails every
  comparison and falls through to a downward arrow. Each says what it
  returns when there is nothing to divide by, and `LapDeltaCalculator`
  stops masking a zero or negative speed behind its `maxOf` floor.

- `DisplayFormatter` garbles every negative duration. Kotlin's integer
  division truncates toward zero, so `formatMinutesSeconds` renders
  minus ninety seconds as `-1:-30` and `formatDurationTotal` does the
  same in hours — while `formatDelta`, in the same file, extracts the
  sign and formats the absolute value correctly. The two follow it.

- A negative duration reaches the display from three directions and
  nothing stops it: the parser accepts a signed time value, the watch
  stores whatever `markSegment` computes without checking, and neither
  Room nor the payload codec bounds what it reads back. `undoLastMark`
  compounds an already-negative duration by subtracting it. A duration
  is checked where it enters, and a segment that cannot carry a
  sensible one says so.

- Two freshness windows treat a reading from the future as fresh.
  `SensorFreshnessWindow.evaluate` and `PaceCalculator.smoothedPace`
  both compare an age against a window with `<=`, and a negative age —
  a sample timestamped after now — passes. Both reject an age that
  cannot be.

- `SegmentBuilder.cumulativeDurationMs` returns a total lower than the
  truth when a segment index is missing. It walks the segments it has
  and adds them, so a gap is silently skipped rather than making the
  result unavailable — which is what its own documentation suggests it
  does. And a duplicate index is added twice, by that function and by
  `CumulativeDeltaEstimator` and `EndOfRaceViewModel` alike, while
  `insertSegments` on the way in replaces one with the other without a
  word. Both shapes are stated: a missing index makes the total
  unavailable, a duplicate is refused where it is written.

- `HeartRateZoneCalculator` trusts a profile it never checks. It
  filters a null maximum heart rate but not a zero, which puts every
  boundary at zero and lands almost every reading in zone five; it maps
  the thresholds without checking they increase, so a disordered
  profile classifies a high reading into a low zone; and it indexes
  those thresholds assuming exactly four, which nothing in the type,
  the database or the payload enforces — one of its own tests already
  passes an empty list. It states what it does with a profile that
  cannot yield zones, rather than raising or answering wrongly.

- `stopRace` ignores the instant it is given. Its contract says that
  instant is never truncated; the implementation never reads it at all,
  and a race carries no end time — the total is always the sum of its
  segments. Either the parameter is used, or it goes and the contract
  says so.

- Two races imported on the same day carry the same instant.
  `ImportPreviewViewModel` dates an imported race at the start of its
  calendar day, so a second import that day ties with the first. The
  phone's query breaks that tie by id and is tested for it; the watch's
  own ordering relies on the stability of a sort rather than a second
  comparison, and would break silently if the reversal around it ever
  went. The watch orders on the same two keys the phone does.

- A race name is validated on one path and not the others. `rename`
  refuses an empty name and one past forty characters;
  `saveImportedRace` and `saveRecordedRace` store whatever they are
  given, so an imported race can carry a name that renaming it would
  refuse. And the paste screen enables its import button on a name of
  spaces, because it tests for emptiness rather than blankness. The
  same rule applies wherever a name is written.

- No text in either application is bounded on screen. There is no
  `maxLines` and no overflow handling anywhere in the two modules: a
  long race name wraps without limit on the race list — whose row has
  no weight on the name, so it can push the total time out of place —
  on the detail title, in the delete confirmation, on the watch's
  history, and on both reference-race labels. Each states how it
  behaves when the text does not fit.

- `WatchRaceNavigator` treats its inactivity timeout as expired at the
  exact boundary, where every sensor freshness window in the project
  treats the same boundary as still valid. One convention, stated once.

- A sync timestamp in the future reads as older than it is.
  `formatDateRelative` compares two local dates and falls through to
  its `Earlier` branch when the stored instant is ahead of now — a
  clock that stepped back, or drift between the two devices. It says
  what it shows when the date it is given is not in the past.

- A genuinely new race can be swallowed as a duplicate and lost for
  good. The watch numbers its races from an in-memory counter that
  restarts at one with every process, and the phone deduplicates on
  that number alone, with no window and no uniqueness behind it: a race
  recorded after the watch restarts can carry the number of a race
  synced in an earlier session, and `saveRecordedRace` returns the old
  one without storing the new. A race identifies itself in a way that
  survives the process that made it.

- The phone's deduplication is not atomic. `saveRecordedRace` looks the
  source id up and then writes, in two separate Room calls with no
  transaction around them and no lock on the method, and the column it
  looks up carries neither an index nor a uniqueness constraint — so
  the lookup is a full scan, and nothing structurally prevents two rows
  from sharing one source id. The check and the write happen together,
  and the column enforces what the code assumes.

- Replacing the reference race leaves a moment with no reference at
  all. `replaceReference` clears the flag on every row and then writes
  the new one, in two separate Room transactions, and anything
  observing the reference flow can read between them. The two happen as
  one.

- `persist` force-unwraps a row it has just written, and a concurrent
  delete between the write and the read makes that unwrap fail. It
  reads back what it wrote in the same transaction, or says what it
  does when the row is gone.

- Applying an incoming profile can silently lose a local edit.
  `applyProfile` writes the five fields through five independent calls,
  each reading the whole profile and writing the whole row back — a
  read-modify-write with no transaction and no lock over the set. A
  user editing the profile while a push arrives loses one of the two,
  whole-row, last writer winning. The five fields are applied as one.

- An incoming push can be accepted while a race is running.
  `ProfileSyncListenerService` computes whether a race is in progress
  when the message arrives, then hands that boolean to a coroutine that
  runs later; `applyIncoming` trusts it rather than checking at the
  moment it acts. A race started in between lets through a push that
  should have been refused — and a refused push replaces the watch's
  whole state. The check happens where the decision is made.

- `RecordedRaceSyncService.sync` is called with a hardcoded false for
  whether a race is running, from both of the watch's call sites, where
  the profile listener recomputes the same condition on every message.
  It derives that state the same way.

- Nothing on the phone pushes when something changes. A race renamed,
  deleted, imported or made the reference triggers no push — the only
  call sits behind the profile screen's sync button. The watch's
  reference and history are never fresher than the last successful
  push, for as long as the user never presses it and the link never
  comes back. A change to what the watch mirrors reaches it the way the
  spec describes for the push it already has.

- The correction factor a watch race retains never reaches the phone.
  It is computed on the watch at the end of a recorded race and
  overwrites the watch's own `Profile.correctionFactor`, and no sync
  path carries it back: `ProfileSyncPushService` pushes the phone's own
  unchanged value down on the next established link, undoing it, so the
  next race starts from a factor that ignores every race the watch ever
  recorded. The phone's `correctionFactor` is derived from the
  `retainedFactors` a race already carries when the pull delivers it,
  and the push that follows sends that value.

- The lap-delta column shows a value no calculation covers. §3.4 states
  the lap delta exists only on RUN segments, and defines it as a
  projection from a live segment pace, recomputed continuously; the
  race detail screen renders a delta on all thirty rows of a stored
  race, each compared against the reference race's duration for that
  segment index. Nothing states what backs the twenty-two rows that are
  not runs, nor what a projected delta means once a race is over. Every
  row of that column names the calculation behind it, and a row no
  calculation covers shows nothing rather than a number.

- A segment name is both a domain value and a displayed string, and
  nothing says which. §5.1 maps each segment index to a name — SkiErg,
  Rameur, Farmers Carry, Wall Balls — which the race detail screen
  renders in every row and the main page renders as the station and as
  the Roxzone destination. §10.2 forbids any user-facing string from
  being written in code, and §10.4's catalogue holds no key for a
  single segment name. Each name is one or the other: a value the
  domain produces, or a key the resources carry, and the code says
  which.

- Every sensor value reaches its freshness boundary on every power-save
  refresh. §1.3 gives sensor-derived values a ten-second freshness
  window, in both display modes, past which they fall back and render
  as a dash; §9.16 sets the power-save refresh cadence to exactly ten
  seconds, and states that in power-save values stay shown and dimmed
  rather than replaced with a dash. A value refreshed on that beat is
  at the boundary each time, and what it renders there follows from one
  entry or the other, not from which one the code happens to consult.

- Two entries point at text that does not exist. §2.2 states that a
  bound violation shows §10.1's constraint message, and §10.1 defines
  display formats only — no message, and no key for one in §10.4's
  catalogue. §4.1 states that §9.9's home-screen reminder re-requests
  the permission, and §9.9 describes no reminder, only a badge. Each
  string a screen shows has a key that exists, and a reference to text
  points at text.
