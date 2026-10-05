## Signatures

`WatchStringResources` becomes an object whose every member returns
`LabelRef` (`com.mgilli.core.domain.display.LabelRef`, produced by
lot-16) instead of `String`. Applies uniformly to `Permission`,
`Waiting`, `Home`, `History`, `Prep`, `Projection`, `StopConfirm`,
`ResumeDialog`, `End`, `Sync` — every fixed `const val` becomes a `val`
returning a `LabelRef` with empty `args`. The two existing parameterised
functions keep their parameters, returning `LabelRef` with `args` in
call order:

- `Home.referenceLine(name: String?): LabelRef` — `name` non-null: a
  `LabelRef` with `args = [name]` pointing at "Réf. — %1$s"; `name`
  null: a distinct `LabelRef` with empty `args` pointing at the fixed
  "⚠ Aucune référence" entry — two resource ids reached by the same
  branch that exists today, not one id with a conditional argument.
- `Prep.referenceLoaded(name: String): LabelRef` — `args = [name]`.

Exception — `WatchStringResources.RaceName` is removed entirely.
`RaceRecordingRepositoryImpl.startClock` builds `Race.name` directly as
`DisplayFormatter.formatDateTime(startedAt)` (same formatting as
today), with no `WatchStringResources` call and no import of it: the
generated race name is written to the database and travels to the
phone — domain data, not a displayed label — so it never becomes a
`LabelRef` and never gets a `strings.xml` entry.

Exception — `segmentName` and `Control.undoLabel` are redesigned so
neither ever places an unresolved `LabelRef` inside another `LabelRef`'s
`args` (Android's `stringResource(id, *args)` needs its `args` already
resolved — a nested `LabelRef` cannot be flattened into them without a
`Context`, unavailable here, mirroring lot-16's `Profile.lastSync`
exception):

- `segmentName(index: Int): LabelRef` — `RUN`: one resource id
  parameterised by the run number `(index - 1) / 4 + 1` (unchanged
  formula). `STATION`: one of eight fixed resource ids selected by
  `SegmentBlueprint.stationAt(index)`, one per `Station` value (mirrors
  today's private `stationName` mapping — SkiErg / Sled Push / Sled
  Pull / Burpee BJ / Rameur / Farmers Carry / Sandbag Lunges / Wall
  Balls; the mapping stays exhaustive over `Station` even though
  `stationAt` never actually returns `WALL_BALLS`). `FINAL`: its own
  fixed "Wall Balls" resource id. `ROXZONE_OUT`: one of eight fixed
  "Roxzone → <Station>" resource ids selected by
  `SegmentBlueprint.stationAt(index + 1)` — the segment right after a
  `ROXZONE_OUT` is always a `STATION`, computed directly, never through
  a nested call to `segmentName`. `ROXZONE_IN`: one resource id
  "Roxzone → Run %1$d", parameterised by `index / 4 + 1` — the segment
  right after a `ROXZONE_IN` is always the `RUN` at `index + 1`, whose
  number is computed directly with the same formula as the `RUN`
  branch, not by calling `segmentName(index + 1)`.
- `Control.undoLabel(index: Int): LabelRef` — replaces
  `undoLabel(segment: String): String`. Takes the index of the segment
  being reopened directly; the call site no longer pre-resolves its
  name through `segmentName`. Mirrors `segmentName`'s own branching
  with a distinct "Annuler : …" resource id per case: `RUN` → "Annuler
  : Run %1$d", same parameterisation; `STATION` → one of eight fixed
  "Annuler : <Station>" ids; `ROXZONE_OUT` → one of eight fixed
  "Annuler : Roxzone → <Station>" ids; `ROXZONE_IN` → "Annuler :
  Roxzone → Run %1$d", same parameterisation. `FINAL` is never reached
  in practice (`ControlViewModel` only calls this with
  `currentSegmentIndex - 1`, at most 29), but the `when` stays
  exhaustive over `SegmentType` for the compiler, reusing the
  `STATION`/`WALL_BALLS` case's "Annuler : Wall Balls" id.

`ControlViewModel.computeState()` — unchanged signature; `undoLabel`
built as `WatchStringResources.Control.undoLabel(index - 1)` in place
of `WatchStringResources.Control.undoLabel(WatchStringResources.segmentName(index - 1))`.

`HomeViewModel.computeState()` — unchanged signature;
`referenceLineText`/`startLabel`/`historyLabel`/`syncLabel` built from
the corresponding `WatchStringResources.Home` members, all now
`LabelRef`.

`PreparationViewModel.readyState(referenceLoaded: Boolean)` — unchanged
signature; `referenceLoadedText` built from
`WatchStringResources.Prep.referenceLoaded`, now `LabelRef?`.
`heartRateText` (on both `Ready` and `OpenFailed`) is untouched — it
comes from `DisplayFormatter.formatHr`, not a catalogue key, and stays
`String?`.

`SensorPermissionViewModel`'s initial `uiState` — `title`/`explanation`/
`actionLabel` built from `WatchStringResources.Permission.title`/
`explanation`/`action`, now `LabelRef`.

`WaitingForPhoneViewModel`'s initial `uiState` — `title`/`explanation`/
`retryLabel` built from `WatchStringResources.Waiting.title`/
`explanation`/`retry`, now `LabelRef`.

`MainRacePageViewModel.computeState()` — unchanged signature;
`stationLabel` (`STATION`/`FINAL` branch) and the argument to
`RaceCenterBlock.NextStep` (`ROXZONE_OUT`/`ROXZONE_IN` branch) built
from `WatchStringResources.segmentName`, now `LabelRef`.

UiState classes:

```
data class ControlUiState(val undoLabel: LabelRef?, val undoEnabled: Boolean, val stopConfirmVisible: Boolean)
data class HomeUiState(val referenceLineText: LabelRef, val referenceTotalTime: String?, val hasReference: Boolean, val startLabel: LabelRef, val historyLabel: LabelRef, val syncLabel: LabelRef, val syncState: HomeSyncUiState, val sensorPermissionReminderVisible: Boolean)
data class SensorPermissionUiState(val title: LabelRef, val explanation: LabelRef, val actionLabel: LabelRef, val resolvedState: SensorPermissionState?)
data class WaitingForPhoneUiState(val title: LabelRef, val explanation: LabelRef, val retryLabel: LabelRef, val hasReceivedProfile: Boolean)
sealed interface PreparationUiState {
    data class Ready(val heartRateText: String?, val referenceLoadedText: LabelRef?) : PreparationUiState
    data class OpenFailed(val heartRateText: String?) : PreparationUiState
    object SensorConflict : PreparationUiState
}
data class MainRacePageUiState(val stationLabel: LabelRef?, val top: RaceTopBlock, val center: RaceCenterBlock, val heartRateText: String?, val zone: HeartRateZone?)
data class RaceCenterBlock.NextStep(val destinationName: LabelRef) : RaceCenterBlock
```

— every other field of these classes, and every other `RaceTopBlock`/
`RaceCenterBlock` variant, is untouched: they carry `DisplayFormatter`
output or plain data, not catalogue text.

Every Composable call site reading a `WatchStringResources` member
directly, or a `UiState` field listed above, resolves it with
`androidx.compose.ui.res.stringResource(id: Int, vararg formatArgs: Any): String`
— `stringResource(ref.id, *ref.args.toTypedArray())` — same mechanism
as `PhoneStringResources`' call sites (lot-16). Affected: `HomeScreen.kt`
(`Home.*`, `Sync.*`, `Permission.reminder`/`action`, and `uiState`'s
four `LabelRef` fields), `ControlScreen.kt` (`Control.title`/`stop`,
`StopConfirm.*`, `ResumeDialog.*`, `uiState.undoLabel`),
`PreparationScreen.kt` (`Prep.hrLabel`/`launch`/`quit`, `ResumeDialog.*`,
`referenceLoadedText`), `SensorPermissionScreen.kt`
(`uiState.title`/`explanation`/`actionLabel`), `WaitingForPhoneScreen.kt`
(`uiState.title`/`explanation`/`retryLabel`), `ProjectionScreen.kt`
(`Projection.etaLabel`), `WatchHistoryScreen.kt`
(`History.emptyTitle`/`emptyAction`), `EndOfRaceScreen.kt`
(`End.finish`), `MainRacePageScreen.kt` (`uiState.stationLabel`,
`center.destinationName`).

`app-wear/src/main/res/values/strings.xml` gains one entry per
`WatchStringResources` member (fixed or parameterised), plus the eight
"Roxzone → <Station>" and the four families of "Annuler : …" entries
described above, French text, `%1$s`/`%1$d`-style placeholders for a
parameterised key, in addition to the existing `app_name`.

## Acceptance criteria

- Every fixed key (e.g. `Permission.title`, `Waiting.title`,
  `Home.start`, `History.emptyTitle`, `Prep.hrLabel`,
  `Projection.etaLabel`, `Control.title`, `StopConfirm.title`,
  `ResumeDialog.title`, `End.finish`, `Sync.inProgress`) resolves to a
  `LabelRef` with an empty `args` list, whose `id` resolves via
  `strings.xml` to the exact French text it held before
- `Home.referenceLine(name)` with a non-null `name` resolves to a
  `LabelRef` whose single `args` entry is `name` and whose `id`'s
  format string reproduces "Réf. — `name`"; with a null `name` it
  resolves to a distinct `LabelRef` with empty `args`, whose `id`
  resolves to "⚠ Aucune référence"
- `Prep.referenceLoaded(name)` resolves to a `LabelRef` whose single
  `args` entry is `name`, reproducing "Référence chargée · `name`"
- `segmentName` reproduces, for every one of the 30 indices, the exact
  French text `WatchStringResourcesTest` asserts today — in particular
  index 1 → "Run 1", index 29 → "Run 8" (`RUN`), index 3 → "SkiErg"
  (`STATION`), index 30 → "Wall Balls" (`FINAL`), index 2 →
  "Roxzone → SkiErg" (`ROXZONE_OUT`), index 4 → "Roxzone → Run 2"
  (`ROXZONE_IN`)
- `Control.undoLabel(index)` resolves to "Annuler : " followed by
  exactly the text `segmentName(index)` resolves to, for a `RUN`
  index, a `STATION` index, a `ROXZONE_OUT` index and a `ROXZONE_IN`
  index
- `ControlViewModel.uiState.undoLabel` equals
  `WatchStringResources.Control.undoLabel(index - 1)` exactly when
  `UndoMarkingController.canUndo` is true, and is null when it is false
- `HomeViewModel.uiState.referenceLineText` equals
  `WatchStringResources.Home.referenceLine(reference?.name)` for both a
  present and an absent reference; `startLabel`/`historyLabel`/
  `syncLabel` always equal their `WatchStringResources.Home` members
- `PreparationViewModel`'s `Ready.referenceLoadedText` equals
  `WatchStringResources.Prep.referenceLoaded(name)` when a reference
  race is loaded, and is null when none is loaded or the session
  failed to open
- `SensorPermissionViewModel.uiState.title`/`explanation`/`actionLabel`
  equal `WatchStringResources.Permission.title`/`explanation`/`action`
- `WaitingForPhoneViewModel.uiState.title`/`explanation`/`retryLabel`
  equal `WatchStringResources.Waiting.title`/`explanation`/`retry`
- `MainRacePageViewModel.uiState.stationLabel` equals
  `WatchStringResources.segmentName(index)` on a `STATION`/`FINAL`
  segment, and is null on a `RUN`/`ROXZONE` segment
- `MainRacePageViewModel.uiState.center` is
  `RaceCenterBlock.NextStep(WatchStringResources.segmentName(index + 1))`
  on a `ROXZONE_OUT`/`ROXZONE_IN` segment
- `RaceRecordingRepositoryImpl.startClock`'s resulting `Race.name`
  equals `DisplayFormatter.formatDateTime(startedAt)` exactly, with no
  dependency on `WatchStringResources`
- Each of the nine affected screens (`HomeScreen`, `ControlScreen`,
  `PreparationScreen`, `SensorPermissionScreen`,
  `WaitingForPhoneScreen`, `ProjectionScreen`, `WatchHistoryScreen`,
  `EndOfRaceScreen`, `MainRacePageScreen`) renders, through
  `stringResource`, the same displayed French text it rendered before
  this lot, for every state exercised by its existing Compose UI test

## Dependencies

LabelRef — produced by lot-16, `:core-domain`, `com.mgilli.core.domain.display`
SegmentBlueprint, SegmentType, Station — pre-existing (`:core-domain`, unchanged)
DisplayFormatter — pre-existing (`:core-domain`, unchanged)
androidx.compose.ui.res.stringResource — framework (Compose, already a dependency of `:app-wear` through Wear Compose)
RaceRepository, ProfileRepository, RaceRecordingRepository, WatchRaceNavigator, SensorPermissionManager, UndoMarkingController, StopRaceController, RaceLaunchController, SegmentMarkingController — pre-existing, unaffected by this lot beyond the call-site edits described above

## Conventions

§3 · a platform adapter/text catalogue lives in the module owning it — `WatchStringResources` and its resource ids stay in `:app-wear`, never move to `:core-domain`
§9 · files named for the class they hold — `WatchStringResources.kt` keeps its name, no new file
§10 · no hardcoded user-facing string; every key moves into `app-wear/res/values/strings.xml`, French only
§10 · interpolated values are passed as resource parameters, never concatenated — bars embedding a resolved segment name as a raw string inside another `LabelRef`'s `args`, hence the flattened per-branch ids for `segmentName`'s `ROXZONE` cases and for `Control.undoLabel`
§10 · the two apps keep separate resource files — this lot touches only `app-wear/res/values/strings.xml`
§14 · Compose UI tests stay in `src/test`, Robolectric — the nine affected screens' existing UI tests keep asserting on rendered text, now resolved through `stringResource`
