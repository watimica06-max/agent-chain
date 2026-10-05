## Preamble

Intent: correcting the gaps reported on premiere-app.
Out of scope: everything not listed below.
Dependencies: the whole feature, already built.

## §1 Model

## §2 Persistence

### §2.1 ProfileRepository.observe() emits nothing on failure

Bearer: ProfileRepository (fulfilled by ProfileRepositoryImpl)

ProfileRepositoryImpl.observe() catches a profileDao.observe() failure and lets the flow complete without emitting, so the four callers that call .first() on it receive an empty completed flow instead of a declared failure. ProfileRepository.observe() must declare a Flow whose element carries a failure case of its own type, and ProfileRepositoryImpl's catch must emit that failure instead of completing silently; every current caller — the two produceState reads in WatchApp, NavigationModule's profileAlreadySynced, and RaceRecordingRepositoryImpl's correction-factor read — must be rewritten against the new element type and handle the failure case explicitly.

### §2.2 `watch-history.db` carries no migration or fallback strategy

Bearer: RepositoryModule.provideWatchHistoryDatabase

Both RepositoryModule.provideWatchHistoryDatabase providers (app-phone and app-wear) build WatchHistoryDatabase with no addMigrations and no fallbackToDestructiveMigration, unlike provideHyroxDatabase in the same files. Raising WatchHistoryDatabase's version without an explicit schema-evolution strategy on both providers throws IllegalStateException on the first query issued by any pre-existing installation; both providers must carry an explicit migration or destructive-fallback strategy for WatchHistoryDatabase, matching the discipline already applied to HyroxDatabase.

### §2.3 A dependency's exception travels inside the declared `Result`

Bearer: RaceRepositoryImpl (also ProfileRepositoryImpl and RaceRecordingRepositoryImpl)

Every suspend surface of RaceRepositoryImpl, ProfileRepositoryImpl and RaceRecordingRepositoryImpl wraps its DAO call in runCatching and returns the caught throwable — a raw dependency exception such as SQLiteException, or a raw JDK exception for a domain refusal — unconverted inside Result.failure. Each of these suspend surfaces must convert its caught failure into a declared domain failure type before returning it, the same way RaceRepositoryImpl.observeAll() and observeReference() already convert their Flow failures into RaceQueryFailure.

### §2.4 Four local stores read and write disk on the caller's thread

Bearer: SensorPermissionLaunchStoreImpl, ConnectivityPermissionLaunchStoreImpl (wear and phone), PhoneNavigationStateStore

SensorPermissionLaunchStoreImpl, both ConnectivityPermissionLaunchStoreImpl implementations and PhoneNavigationStateStore call SharedPreferences.getBoolean, getString or edit().apply() directly from a non-suspend function, on the caller's own thread. All four must declare isFirstLaunch, recordLaunch, save and restore as suspend and move the SharedPreferences access onto Dispatchers.IO; SensorPermissionManager.isFirstLaunch() must itself become suspend to await the change, and PhoneNavigator needs either its own coroutine scope to launch save and restore on or a suspend construction and navigation API, since its backStack property reads restore() synchronously in a property initializer today.

## §3 Calculation

## §4 Transition

### §4.1 Five destinations can render nothing while resolving or on failure

Bearer: WatchApp

In WatchApp, the MAIN, PROJECTION, CONTROL and END branches each read a produceState value that starts at null and render only inside an if with no else, so the branch renders nothing while the read is still resolving or has failed; PreparationScreen's own null -> Unit branch does the same for PREPARATION. Each of the five destinations must render a loading state while its data resolves and a distinct error state if the read fails, and the three produceState blocks that call findInProgress() must read its Result directly instead of discarding a failure through getOrNull() so the new error state is reachable.

### §4.2 A stale navigation token is treated differently on two paths

Bearer: MainActivity.onNewIntent

onNewIntent converts the complication's EXTRA_TAPPED_DESTINATION extra with WatchDestination.valueOf(extra), which throws IllegalArgumentException on a name WatchDestination no longer declares, while the cold-launch path's tappedDestination performs the same lookup tolerantly and returns null. onNewIntent must perform the same tolerant conversion as tappedDestination, written once and shared by both entries, so an unknown name leaves the current destination unchanged instead of throwing.

## §5 External source

### §5.1 Sensor capabilities are read on the wrong Health Services client

Bearer: SensorReadingsSource

SensorReadingsSource registers every requested data type on measureClient using the capabilities ExerciseSessionSystemImpl.availableDataTypes() reports from ExerciseClient, never checking measureClient's own capabilities, so DataType.DISTANCE and DataType.SPEED are registered on measureClient even though that client does not deliver them as a punctual measurement. SensorReadingsSource must check measureClient.getCapabilitiesAsync() before calling registerMeasureCallback and register only the types that call reports as supported; distance and speed must instead be read from ExerciseClient's own exercise-update flow, which does not exist anywhere in app-wear today and must be added.

### §5.2 `registerOne()` can suspend without ever resuming

Bearer: SensorReadingsSource.registerOne

registerOne() wraps registerMeasureCallback in a suspendCancellableCoroutine that resumes only from onRegistered or onRegistrationFailed, so a data type the platform never acknowledges suspends the coroutine, and register()'s sequential loop with it, forever, blocking every subsequent type and the whole preparation screen; the same unbounded-wait shape exists in SensorPermissionSystemImpl.requestPermission() and ConnectivityPermissionSystemImpl.requestPermission(). registerOne()'s wait must be bounded by a timeout that is treated as a registration failure for that type only, and both requestPermission() implementations must bound their deferred.await() the same way, returning a declined permission on expiry and clearing the pending callback registration.

### §5.3 Seven failures are swallowed without a log line

Bearer: ExerciseSessionSystemImpl

Seven sites across ExerciseSessionSystemImpl, SensorReadingsSource, ExerciseSessionManager and RaceLaunchController catch or receive a failure — a session-start refusal, an end-session failure, a data-delivery-mode failure, an unregistration failure, a registration failure, a discarded registration boolean, and a mapped OpenFailed — without writing any of them to the log. Each of the seven sites must log at ERROR, naming the operation and the fault, and ExerciseSessionManager.open() must read the boolean readingsSource.register() returns and act on a false result instead of discarding it.

### §5.4 Three calls run outside the `try` that should cover them

Bearer: ExerciseSessionSystemImpl.startExerciseSession, PlatformModule.provideHealthConnectClient, HrPermissionSystemImpl.isGranted

ExerciseSessionSystemImpl.startExerciseSession() calls getCurrentExerciseInfoAsync().await() before its own try block, PlatformModule.provideHealthConnectClient() calls HealthConnectClient.getOrCreate(context) outside the try that guards getSdkStatus, and HrPermissionSystemImpl.isGranted() calls getGrantedPermissions() with no try at all, so each throws instead of resolving to the failure value its own function already returns elsewhere. Each of the three calls must move inside the try that already covers the rest of its function, resolving to the same failure-as-a-value outcome — Failed, the getSdkStatus null sentinel, and false respectively — instead of letting the exception propagate.

## §6 Synchronisation

### §6.1 A second device-link registration throws instead of completing

Bearer: DataLayerCapabilitySource

DataLayerCapabilitySource.localNodeId() calls addLocalCapability(CAPABILITY_NAME).await() and lets its Task failure propagate as a thrown exception, deliberately, per its own class comment; because the capability registration persists across launches, every launch after the first receives DUPLICATE_CAPABILITY and the exception kills the application, and addListener/removeListener each discard their own Task's failure. localNodeId() must treat DUPLICATE_CAPABILITY as a normal outcome and complete without throwing, every other ApiException must be caught and turned into a declared link-absent outcome, the class comment documenting the thrown-exception behaviour must be removed, and addListener/removeListener must stop discarding the Task they return.

### §6.2 Two listener services discard the outcome they read

Bearer: ProfileSyncListenerService

ProfileSyncListenerService.onMessageReceived calls profileSyncPushService.applyIncoming(...) and discards its returned outcome entirely, so neither a Refused nor a Failure is logged, and WatchRaceComplicationDataSourceService.onComplicationRequest separately reads raceRecordingRepository.findInProgress().getOrNull(), discarding a store failure so it renders identically to no race in progress. onMessageReceived must read the returned outcome and log Refused and Failure at ERROR, the way RecordedRaceAckListenerService already logs its own failure, and onComplicationRequest must read the Result from findInProgress() and log a store failure at ERROR distinctly from the nominal case, while still handing the complication data source an empty result on that failure.

## §7 Background work

### §7.1 The race clock is coupled to the exercise session's outcome

Bearer: RaceLaunchController

raceTicker.start() is called only from ExerciseSessionManager.registerReadingsAndStartTicker(), reached only when the exercise session opens successfully, so when startExerciseSession() fails the ticker never starts even though the race clock is started and the race is recorded regardless. RaceLaunchController.launch and retryAndLaunch must start raceTicker at the same point they call recordingRepository.startClock(...), independently of the exercise session's outcome, which requires RaceControllerModule.provideRaceLaunchController to supply RaceLaunchController with a RaceTicker; raceTicker.stop() must move out of ExerciseSessionManager.close() and pair with the race's own end instead of the session's close.

### §7.2 Twenty-four waits carry no timeout

Bearer: none single — twenty-one independent await/suspend call sites across core-sync, app-wear, app-phone and the Room repositories

None of the twenty-one await calls listed — the device-link check, the message channel, the exercise-session client calls, the sensor unregistration, the Health Connect reads, and every Room repository's suspend surface — is wrapped in a timeout, so each resolves only when the underlying platform, store or dependency responds, however long that takes; three of them, in HrPermissionSystemImpl, share the same fully unblockable shape as the two permission-dialog waits fixed separately. Each of the twenty-one calls must be wrapped in a timeout sized to what it does, with the timeout treated as an ordinary failure — logged, and turned into the same declared failure value the call already returns on any other failure — and HrPermissionSystemImpl.requestPermission()'s deferred.await() must additionally resolve to a declined permission on timeout rather than leaving the coroutine suspended.

### §7.3 The complication service can crash outside any activity

Bearer: WatchRaceComplicationDataSourceService

onComplicationRequest reads WatchRaceNavigator.current, whose lazy initialiser launches NavigationModule's asynchronous reads on a scope with no exception handler; a failure surfacing from profileRepository.observe() propagates uncaught out of that coroutine with no activity or screen able to catch it, crashing the hosting system service. Once the profile source emits its failure as a value instead of throwing, onComplicationRequest must resolve to a value it can read and call listener.onComplicationData(null) on that failure, the same way the no-race-in-progress case already does, rather than let the coroutine terminate the process.

## §8 Journey

## §9 Screen

### §9.1 `MainRacePageScreen` has no rendering floor

Bearer: MainRacePageScreen

MainRacePageScreen renders four items behind ?.let guards — the station label, the top block, the center block and the heart-rate text — and on a RUN segment with no reference race and no sensor reading yet, every guard is skipped and the ScalingLazyColumn composes with zero items over a black background; a race always starts on such a segment. MainRacePageScreen must never compose with zero rendered items: the segment name must render on every segment type, which requires MainRacePageViewModel.computeState()'s RUN branch to call WatchStringResources.segmentName(index) instead of hardcoding null; a Fallback pace must render "—:—" followed by its unit, which requires adding a unit suffix to every pace state, not only Fallback, since DisplayFormatter.formatPace never appends one today; and a Fallback heart rate must render "—" with its zone arc attenuated, which requires a zone arc component on this screen, since none exists today — the screen currently renders heart rate as plain colored text.

### §9.2 A failed session renders identically to one still loading

Bearer: PreparationUiState (and MainRacePageUiState)

PreparationUiState declares OpenFailed as a case distinct from Ready, but PreparationScreen renders both through the same ReadyContent with identical labels, and mutableUiState starts at null rendered as null -> Unit, so a failed session open looks identical to one still waiting for its first reading; MainRacePageUiState has no case at all meaning the exercise session failed, only SensorValueDisplay.Fallback, which covers both no reading yet and no session ever opened. PreparationUiState must carry a case for a failed session open rendered through a body distinct from ReadyContent and reachable on the first emission, MainRacePageUiState must carry a distinct case for the same failure, and both require ExerciseSessionOpenResult to carry its own case for a permission refusal, distinct from Failed, so ExerciseSessionSystemImpl.startExerciseSession()'s catch can distinguish it from any other failure.

## §10 Text

## §11 Access

### §11.1 `ACTIVITY_RECOGNITION` is declared nowhere

Bearer: AndroidManifest.xml (app-wear)

app-wear's AndroidManifest.xml declares VIBRATE, BLUETOOTH_CONNECT, BODY_SENSORS and health.READ_HEART_RATE but never android.permission.ACTIVITY_RECOGNITION, which Health Services requires for ExerciseClient; without it, startExerciseAsync() is refused with a SecurityException and Health Services strips every data type that depends on it before the exercise session is ever reached. The manifest must declare ACTIVITY_RECOGNITION, and the app must request it at runtime through the existing sensor permission parcours rather than a second parallel path, which requires that parcours' single-permission request mechanism — SensorPermissionSystemImpl.requestPermission, its launcher and SENSOR_PERMISSION — to accept and report on two dangerous permissions instead of one.

### §11.2 Two permission waits that nothing can unblock

Bearer: ConnectivityPermissionSystemImpl.requestPermission, SensorPermissionSystemImpl.requestPermission

Both requestPermission() implementations create a CompletableDeferred, launch the system permission dialog, and await it with no timeout; if the hosting activity is destroyed before the dialog's callback fires, the deferred is never completed and the coroutine suspends for the remainder of the process's life, reached unconditionally on first launch from HomeViewModel.init and ProfileViewModel.init. Both must bound their deferred.await() with a timeout that resolves as an unanswered dialog, never as a stated refusal, leaving KEY_HAS_REQUESTED untouched so a further prompt can still be offered; this requires a third outcome distinct from granted and denied, which neither the requestPermission signature nor SensorPermissionState/ConnectivityPermissionState — both limited to Granted and Fallback today — currently has room for.

### §11.3 Opening system settings has no guard against `ActivityNotFoundException`

Bearer: SensorPermissionSystemImpl.openAppSettings, ConnectivityPermissionSystemImpl.openAppSettings

Both openAppSettings() implementations build the application-details settings Intent and call activity.startActivity(intent) directly, with no resolvability check and no try/catch, so a device or OS version lacking that settings screen throws ActivityNotFoundException uncaught. Both must resolve the intent before launching it, or catch ActivityNotFoundException around the call, and treat an unresolvable intent as a nominal outcome: the current permission screen stays displayed and the user is left with an indication of what to do by hand.

## §12 Lifecycle

### §12.1 The sensor session is never reopened on a cold resume

Bearer: WatchRaceNavigator

WatchRaceNavigator's cold-resume check writes WatchDestination.MAIN directly as soon as raceInProgress() is true, without touching ExerciseSessionManager, so no Health Services session is opened and no sensor is registered — only the warm-resume path, through PreparationViewModel and RaceLaunchController.reconcileResumedSession(), reopens a resumed race's session today. The cold-resume check must reopen the session before or as part of writing MAIN, the same way reconcileResumedSession() does for the warm-resume path, which requires RaceLaunchController to expose that reopening for cold-resume use and WatchRaceNavigator to receive a new suspend closure wired in NavigationModule.provideWatchRaceNavigator, bounded by a timeout consistent with R19.

## Gaps set aside
