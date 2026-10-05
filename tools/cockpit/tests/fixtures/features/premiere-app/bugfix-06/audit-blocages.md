# Audit of blocks — docs/features/premiere-app/bugfix-06

## Files read

### Pass 1
code/lot-11/blocked_detailleur-01.md
code/lot-19/blocked_detailleur-01.md
code/lot-20/blocked_detailleur-01.md
code/lot-20/blocked_realisateur-01.md
code/lot-22/blocked_realisateur-01.md
code/lot-24/blocked_realisateur-01.md
code/lot-24/blocked_realisateur-02.md
code/lot-27/blocked_detailleur-01.md
code/lot-31/blocked_detailleur-01.md
code/lot-36/blocked_detailleur-01.md
code/lot-41/blocked_detailleur-01.md
code/lot-43/blocked_detailleur-01.md
code/lot-45/blocked_realisateur-01.md
code/lot-49/blocked_detailleur-01.md
code/lot-50/blocked_detailleur-01.md
code/lot-56/blocked_realisateur-01.md

## Pass 1

### Still open
code/lot-11/blocked_detailleur.md
code/lot-20/blocked_detailleur.md
code/lot-27/blocked_detailleur.md
code/lot-31/blocked_detailleur.md
code/lot-36/blocked_detailleur.md
code/lot-41/blocked_detailleur.md
code/lot-43/blocked_detailleur.md
code/lot-49/blocked_detailleur.md
code/lot-50/blocked_detailleur.md

### Names carried by more than one block
`MainActivityTest` (`:app-phone`) | lot-11/blocked_detailleur-01, lot-20/blocked_realisateur-01, lot-22/blocked_realisateur-01, lot-24/blocked_realisateur-01, lot-56/blocked_realisateur-01 | lot-24 `## Where` : "`app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt` (`ImportPreviewScreen`/`PasteResultViewModel`, package `com.mgilli.hyroxtracker.ui.pasteresult`/`ui.importpreview`) — none of which lot-24 touches"
`PasteErrorViewModelTest` | lot-20/blocked_realisateur-01, lot-22/blocked_realisateur-01 | lot-22 `## Where` : "`app-phone/src/test/java/com/mgilli/hyroxtracker/ui/pasteerror/PasteErrorViewModelTest.kt` (7 of its 12 cases)"
`PasteResultViewModelTest` | lot-20/blocked_realisateur-01, lot-22/blocked_realisateur-01 | lot-22 `## Where` : "This lot's own tests hit the identical stale-fixture issue in `PasteResultViewModelTest`'s `VALID_PASTE`"
`ImportPreviewViewModelTest` | lot-20/blocked_realisateur-01, lot-31/blocked_detailleur-01 | lot-31 `## Where` : "fake `RaceRepository` implementations in `ProfileViewModelTest` (:112-125), `ProfileScreenTest` (:89-102), `ImportPreviewViewModelTest` (:72-88)"
`PasteResultViewModel` | lot-24/blocked_realisateur-01, lot-27/blocked_detailleur-01 | lot-27 `## Where` : "Both branches read `PasteResultViewModel.uiState.value.lastParseResult`"
`ImportPreviewScreen` | lot-24/blocked_realisateur-01, lot-27/blocked_detailleur-01 | lot-27 `## Where` : "`ImportPreviewScreen` and `PasteErrorScreen` cannot be built at all without their parse result"
`RaceListScreen.kt` | lot-24/blocked_realisateur-01, lot-24/blocked_realisateur-02 | lot-24/-02 `## Where` : "compared against `app-phone/src/main/java/com/mgilli/hyroxtracker/ui/racelist/RaceListScreen.kt`"
`RaceListScreenTest` | lot-24/blocked_realisateur-02, lot-31/blocked_detailleur-01 | lot-31 `## Where` : "lot-56 … names `RaceListViewModelTest`, `RaceListScreenTest`, `RaceDetailViewModelTest`, `RaceDetailScreenTest`"
`RaceListViewModelTest` | lot-24/blocked_realisateur-02, lot-31/blocked_detailleur-01 | lot-24/-02 `## Where` : "`RaceListViewModelTest.kt` at this worktree's starting `HEAD` (`e7b94a0`)"
`ProfileSyncListenerServiceTest` | lot-11/blocked_detailleur-01, lot-31/blocked_detailleur-01 | lot-11 `## Where` : "`app-wear/src/test/java/com/mgilli/app_wear/sync/ProfileSyncListenerServiceTest.kt:239` — its subject is `ProfileSyncListenerService`, lot-16, and lot-56 also names the file"
`PreparationViewModelTest` | lot-31/blocked_detailleur-01, lot-45/blocked_realisateur-01 | lot-45 `## Where` : "The test files constructing `ExerciseSessionManager`/`ExerciseSessionSystem` against the pre-modification shape (… `PreparationViewModelTest.kt`, `PreparationScreenTest.kt` …)"
`PreparationScreenTest` | lot-31/blocked_detailleur-01, lot-45/blocked_realisateur-01 | lot-31 `## Where` : "lot-56 … names … `PreparationViewModelTest`, `PreparationScreenTest` — the same job on the same two modules"
`StopRaceController` | lot-43/blocked_detailleur-01, lot-45/blocked_realisateur-01 | lot-43 `## Where` : "`Modifies: SegmentMarkingController, UndoMarkingController, StopRaceController, and their tests`"
`ControlViewModel` | lot-43/blocked_detailleur-01, lot-45/blocked_realisateur-01 | lot-43 `## Where` : "`app-wear/src/main/java/com/mgilli/app_wear/control/ControlViewModel.kt:42` (`undoMarkingController.undo`) and `:63` (`stopRaceController.stop`) — lot-40, block-18, after this block"
`MainRacePageViewModel` | lot-41/blocked_detailleur-01, lot-43/blocked_detailleur-01 | lot-43 `## Where` : "`app-wear/src/main/java/com/mgilli/app_wear/race/MainRacePageViewModel.kt:132` (`markingController.onPressEnd`) — lot-41, block-18, after this block"
`RaceDetailViewModel` | lot-20/blocked_detailleur-01, lot-36/blocked_detailleur-01 | lot-36 `## Where` : "§10 of `desc-bug.md` names one new key and it is `RaceDetailViewModel`'s rename-bound message on the phone"
`MainActivity` (`:app-phone`) | lot-19/blocked_detailleur-01, lot-27/blocked_detailleur-01 | lot-27 `## Where` : "`app-phone/src/main/java/com/mgilli/hyroxtracker/MainActivity.kt`, the `PhoneDestination.ImportPreview` and `PhoneDestination.PasteError` branches of the private `PhoneApp` composable (lines 117–138)"
`findInProgress` | lot-36/blocked_detailleur-01, lot-49/blocked_detailleur-01 | lot-49 `## Where` : "It is masked today only because `findInProgress()` finds nothing after a process death; lot-50 (§2.6, §2.7) makes it find the race"
`code/decoupage.md` | lot-11/blocked_detailleur-01, lot-19/blocked_detailleur-01, lot-31/blocked_detailleur-01, lot-36/blocked_detailleur-01, lot-41/blocked_detailleur-01, lot-50/blocked_detailleur-01 | lot-31 `## Where` : "`code/decoupage.md`, lot-31's `Modifies:` line, against these call sites confirmed by grep"
`desc-bug.md` | lot-20/blocked_detailleur-01, lot-36/blocked_detailleur-01, lot-41/blocked_detailleur-01, lot-49/blocked_detailleur-01, lot-50/blocked_detailleur-01 | lot-50 `## Where` : "`code/decoupage.md`, `## lot-50` (…) against `desc-bug.md` §1.4 and §2.6"

### Decisions resting on nothing
-

### Blocks asking outside their author's reach
The split — a Détailleur asks which lot owns four call sites | lot-11/blocked_detailleur-01 | `## To resume` : "Name the lot that adapts each of the four call sites — this one, under R85 and R86, or a new one"
The split — a Détailleur asks which lot declares a symbol and which adds a resource key | lot-19/blocked_detailleur-01 | `## To resume` : "Two points, both outside this agent's authority: 1. Which symbol carries the unavailability signal into `ProfileViewModel`, and which lot declares that modification … 2. Which lot adds the `PhoneStringResources` key `ProfileScreen` renders for that state"
Another lot's code — a Réalisateur asks that four test classes it does not own be fixed | lot-20/blocked_realisateur-01 | `## To resume` : "Whichever lot owns `MainActivityTest`/`ImportPreviewViewModelTest`/`PasteErrorViewModelTest`/`PasteResultViewModelTest` needs to fix them"
Another lot's code — a Réalisateur asks that two fixtures it does not own be rebuilt | lot-22/blocked_realisateur-01 | `## To resume` : "Rebuild `MainActivityTest`'s and `PasteErrorViewModelTest`'s Hyresult paste fixtures on the parser's current label vocabulary … in whichever lot owns those two files"
Another lot's code — a Réalisateur asks that a failing test be fixed in its owning lot | lot-24/blocked_realisateur-01 | `## To resume` : "then either fix it in its owning lot or clear it so `./gradlew check` can exit 0 for lot-24's own delivery"
The verdict — a Réalisateur asks that the review be re-run | lot-24/blocked_realisateur-02 | `## To resume` : "Confirm whether the review ran against a state prior to `e7b94a0` … and re-run it against the current `HEAD`"
The split — a Détailleur asks which lot adapts five fake `RaceRepository` implementations | lot-31/blocked_detailleur-01 | `## To resume` : "Which lot adapts the five `:app-phone`/`:app-wear` fake `RaceRepository` implementations listed above — lot-56, lot-31, or a new lot."
The split — a Détailleur asks for a catalogue its lot does not declare | lot-36/blocked_detailleur-01 | `## To resume` : "if a race-naming text is wanted, the catalogue key backing it, since adding one reaches `WatchStringResources` and `app-wear/res/values/strings.xml`, neither of which lot-36 declares"
The order — a Détailleur asks that the sequence be reordered | lot-43/blocked_detailleur-01 | `## To resume` : "Either move lot-40 and lot-41 before lot-43 in the sequence … or extend lot-43 to wrap those three call sites itself"
The sheet and the split — a Réalisateur asks that its own sheet be widened or the change moved to another lot | lot-45/blocked_realisateur-01 | `## To resume` : "Either fold `RaceLaunchController.kt`'s `Adopted` handling and `StopRaceController`'s (and, transitively, `ControlViewModel`'s/`ControlScreen`'s) move to `suspend` into lot-45's own sheet … or move `ExerciseSessionManager.close()`'s/`ExerciseSessionSystem`'s `suspend`/`Boolean` conversion to whichever lot already owns `StopRaceController`/`ControlViewModel`/`RaceLaunchController`"
The split — a Détailleur asks whether a symbol its lot does not declare is in its scope | lot-49/blocked_detailleur-01 | `## To resume` : "also say whether `WatchRaceNavigator` is in lot-49's scope for it: the lot declares `MainActivity`, `WatchApp`, `AlwaysOnDisplayController`, `DisplayModule`, `AndroidManifest.xml` and `MainActivityHomeAndRaceScreensTest` as modified, and `WatchRaceNavigator` is not among them"
The split — a Détailleur asks for a split correction | lot-50/blocked_detailleur-01 | `## To resume` : "A split correction giving lot-50 (or a new lot ordered before it) the symbols the persistence needs: `RaceEntity`, `HyroxDatabase`'s version, a new `RaceDatabaseMigrations` entry for the added column(s), and `RepositoryModule (:app-wear)`"
Another lot's test — a Réalisateur asks that a timeout it does not own be raised or investigated | lot-56/blocked_realisateur-01 | `## To resume` : "Either raise that `waitUntil`'s timeout, or investigate why `ImportPreviewViewModel.onSaveClicked`'s post-save sequence … — a decision on `app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt`, outside this lot's named symbols"

### Handed back
-

### Decisions asking for different shapes
`MainActivityTest` — three decisions forbid editing it and name lot-27 its owner, a fourth edits it | lot-20/blocked_realisateur-01, lot-22/blocked_realisateur-01, lot-24/blocked_realisateur-01, lot-56/blocked_realisateur-01 | lot-24 `## Decision` : "This does not extend to editing `MainActivityTest.kt` or `PhoneApp`, which are lot-27's" — lot-56 `## Decision` : "Raise that one `waitUntil`'s `timeoutMillis` at `app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt:172` from `5_000` to `20_000`"
`ControlViewModel` — one decision leaves the `viewModelScope.launch` move to lot-40, the other has lot-43 make it | lot-43/blocked_detailleur-01, lot-45/blocked_realisateur-01 | lot-45 `## Decision` : "`ControlViewModel`'s move into `viewModelScope.launch` under §7.1 stays lot-40's" — lot-43 `## Decision` : "Extend lot-43 to wrap the three same-module call sites itself — `ControlViewModel.kt:42`, `ControlViewModel.kt:63` and `MainRacePageViewModel.kt:132` — in `viewModelScope.launch`"
`ImportPreviewViewModelTest` — one decision forbids editing it, the other carries it into lot-31's sheet | lot-20/blocked_realisateur-01, lot-31/blocked_detailleur-01 | lot-20 `## Decision` : "This does not extend to editing `MainActivityTest`, `ImportPreviewViewModelTest`, `PasteErrorViewModelTest`, `PasteResultViewModelTest` or the ViewModels they exercise — those belong to lots 21, 22, 23 and 27" — lot-31 `## Decision` : "Carry six of the seven call sites in lot-31's own sheet — … `ProfileViewModelTest`, `ProfileScreenTest`, `ImportPreviewViewModelTest`, `ImportPreviewScreenTest` (`:app-phone`)"
`ProfileSyncListenerServiceTest` — one decision adds it to lot-11, the other defers it to lot-56 | lot-11/blocked_detailleur-01, lot-31/blocked_detailleur-01 | lot-11 `## Decision` : "Add the four test call sites to lot-11 — … and `app-wear/src/test/java/com/mgilli/app_wear/sync/ProfileSyncListenerServiceTest.kt`" — lot-31 `## Decision` : "defer `ProfileSyncListenerServiceTest` (`:app-wear`) to lot-56 and name it, with lot-56, in lot-31's report under R73"
`PreparationViewModelTest`, `PreparationScreenTest` — one decision leaves them to lot-56, the other has lot-45 adapt them | lot-31/blocked_detailleur-01, lot-45/blocked_realisateur-01 | lot-31 `## Decision` : "the eight `:app-phone`/`:app-wear` test files lot-56 already names stay lot-56's" — lot-45 `## Decision` : "Beyond these two files and the test files that must compile against them, change nothing outside the sheet's `Modifies` list"
`code/decoupage.md` — one decision records the divergence in the lot report only, three amend the split file itself | lot-19/blocked_detailleur-01, lot-31/blocked_detailleur-01, lot-49/blocked_detailleur-01, lot-50/blocked_detailleur-01 | lot-19 `## Decision` : "name both additions in lot-19's report as scope its `Modifies` line does not list" — lot-49 `## Decision` : "`decoupage.md`'s lot-49 `Modifies:` line takes the two added files" — lot-50 `## Decision` : "write lot-50's sheet against a split correction adding to its `Modifies:`"
