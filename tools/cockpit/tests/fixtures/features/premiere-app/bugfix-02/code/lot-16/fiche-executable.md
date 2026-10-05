## Signatures

data class LabelRef(val id: Int, val args: List<Any> = emptyList())

— new, in `:core-domain`, package `com.mgilli.core.domain.display` (alongside `DisplayFormatter`/`DateDisplay`). `id` is a `@StringRes` resource id, held as a plain `Int` — no Android import needed to declare it. `args` are passed positionally to Android's `%1$s`/`%1$d`-style placeholders, in call order.

object PhoneStringResources

— every member that returns `String` today returns `LabelRef` instead, `id` pointing at a new entry in `app-phone/res/values/strings.xml`, `args` empty for a fixed key or holding the parameters in the order the current function takes them. A member that is a fixed `const val` becomes a `val` (a `LabelRef` instance is not a compile-time constant). This applies uniformly to every nested object (`RaceList`, `RaceDetail`, `DeleteConfirm`, `Rename`, `Paste`, `Preview`, `PasteError`, `Profile`, `Sync`) and to the two top-level functions `segmentName(index: Int): LabelRef` and `cycleHeader(cycleNumber: Int): LabelRef`. `PasteError.unknownLabelBody(label: String): LabelRef` and `PasteError.outOfSequenceBody(label: String): LabelRef` keep truncating `label` to 20 characters internally (no ellipsis, unchanged rule) before placing the truncated value in `args` — truncation is plain string logic, needs no `Context`.

Exception, `Profile`'s sync-status family — `lastSync(date: String?): String` and its two helpers composed a two-level string (`lastSync` embedding `lastSyncToday`/`lastSyncYesterday`'s own resolved text), which a `LabelRef`'s flat `args` cannot carry without resolving the inner one first — unavailable with no `Context`. Replaced by four flat members, each producing the full sentence directly:

- `Profile.lastSyncNever(): LabelRef` — no args; replaces `lastSync(null)`
- `Profile.lastSyncToday(time: String): LabelRef` — args = [time]; now the full sentence ("Dernière synchronisation réussie : aujourd'hui à %1$s"), not the fragment it used to return
- `Profile.lastSyncYesterday(time: String): LabelRef` — args = [time]; same, full sentence with "hier à %1$s"
- `Profile.lastSyncEarlier(dateTime: String): LabelRef` — args = [dateTime]; new, replaces `lastSync(date)`'s non-null branch when `date` came from `DateDisplay.Earlier.dateTime` directly

`Profile.lastSync(date: String?)` is removed — no call site keeps calling it.

ProfileViewModel.syncStatusText(denied: Boolean, lastSyncSuccessAt: Instant?): LabelRef

— unchanged parameters, return type `String` → `LabelRef`. Body: `denied` → `PhoneStringResources.Profile.syncUnavailable`; `lastSyncSuccessAt == null` → `PhoneStringResources.Profile.lastSyncNever`; otherwise dispatches `DisplayFormatter.formatDateRelative(lastSyncSuccessAt, now())`'s `DateDisplay.Today`/`Yesterday`/`Earlier` to `lastSyncToday`/`lastSyncYesterday`/`lastSyncEarlier` respectively, each fed that branch's own `time`/`dateTime` field, no nested `PhoneStringResources` call.

ProfileViewModel.toZoneRows(ranges: List<HeartRateZoneRange>): List<ZoneRowUiState>

— unchanged signature; `label` is built with `PhoneStringResources.Profile.zoneRow(range.zone.ordinal + 1)`, now a `LabelRef`.

RaceDetailViewModel.buildCycles / buildRow

— unchanged signatures; `CycleGroupUiState.header` built from `PhoneStringResources.cycleHeader(cycleNumber)`, `SegmentRowUiState.name` from `PhoneStringResources.segmentName(index)`, both now `LabelRef`.

PasteErrorViewModel.buildUiState(failure: HyresultParseResult.Failure): PasteErrorUiState

— unchanged signature; `title`/`body` built from the `PhoneStringResources.PasteError.*` calls already in place, now `LabelRef`. `expectedRow` built from `PhoneStringResources.PasteError.expectedRowExample`, now `LabelRef?`. `rawRow` is untouched — the pasted row's own text, never a resource.

data class SegmentRowUiState(..., val name: LabelRef, ...)
data class CycleGroupUiState(..., val header: LabelRef, ...)
data class ZoneRowUiState(..., val label: LabelRef, ...)
data class ProfileUiState(..., val syncStatusText: LabelRef, ...)
data class PasteErrorUiState(val title: LabelRef, val body: LabelRef, val rawRow: String?, val expectedRow: LabelRef?)

— every other field of these five classes is untouched (in particular `RaceDetailUiState.name`, `RaceListItemUiState.name`/`date`/`totalTime`, `rawRow`: all carry data, not catalogue text, and stay `String`/`String?`).

Every Composable call site reading a `PhoneStringResources` member directly, or a `UiState` field listed above, resolves it with the framework's `androidx.compose.ui.res.stringResource(id: Int, vararg formatArgs: Any): String` — `stringResource(ref.id, *ref.args.toTypedArray())` — in place of using the `LabelRef`/`String` as `Text`'s `text` directly. Affected: `RaceListScreen.kt` (`RaceList.*`), `RaceDetailScreen.kt` (`RaceDetail.*`, `DeleteConfirm.*`, `Rename.*`, `row.name`, `cycle.header`), `ProfileScreen.kt` (`Profile.*`, `Sync.*`, `row.label`, `uiState.syncStatusText`), `PasteResultScreen.kt` (`Paste.*`), `PasteErrorScreen.kt` (`PasteError.back`, `uiState.title`, `uiState.body`), `ImportPreviewScreen.kt` (`Preview.*`).

`app-phone/src/main/res/values/strings.xml` gains one entry per `PhoneStringResources` member (fixed or parameterised), French text, `%1$s`/`%1$d`-style placeholders for a parameterised key, in addition to the existing `app_name`.

## Acceptance criteria

- A fixed key (e.g. `RaceList.title`) resolves to a `LabelRef` with an empty `args` list, whose `id` resolves via `strings.xml` to the exact French text it held before
- A key parameterised by a `String` (e.g. `DeleteConfirm.title`) resolves to a `LabelRef` whose single `args` entry is the given string, and whose `id`'s format string reproduces the original interpolated sentence
- A key parameterised by an `Int` (e.g. `Profile.zoneRow`) resolves to a `LabelRef` whose single `args` entry is the given number, reproducing the original interpolated sentence
- `PasteError.unknownLabelBody`/`outOfSequenceBody` still truncate a label longer than 20 characters to exactly 20, with no ellipsis, before placing it in `args`; a label of 20 characters or fewer is carried unchanged
- `ProfileViewModel.syncStatusText` returns `Profile.syncUnavailable` when `isConnectivityDenied` is true, regardless of `lastSyncSuccessAt`
- `ProfileViewModel.syncStatusText` returns `Profile.lastSyncNever` when not denied and `lastSyncSuccessAt` is null
- `ProfileViewModel.syncStatusText` returns `Profile.lastSyncToday(time)` when `lastSyncSuccessAt` falls today, `time` matching `DisplayFormatter.formatDateRelative`'s `Today.time`
- `ProfileViewModel.syncStatusText` returns `Profile.lastSyncYesterday(time)` when `lastSyncSuccessAt` falls yesterday, `time` matching `Yesterday.time`
- `ProfileViewModel.syncStatusText` returns `Profile.lastSyncEarlier(dateTime)` when `lastSyncSuccessAt` is earlier than yesterday, `dateTime` matching `Earlier.dateTime`
- Every `SegmentRowUiState.name` in `RaceDetailViewModel.uiState` equals `PhoneStringResources.segmentName` for that row's index
- Every `CycleGroupUiState.header` in `RaceDetailViewModel.uiState` equals `PhoneStringResources.cycleHeader` for that cycle's number
- `PasteErrorViewModel.uiState.title`/`body` equal the `PhoneStringResources.PasteError` pair matching the failure's `HyresultParseFailureCause`, for each of the eight causes
- `PasteErrorViewModel.uiState.expectedRow` equals `PhoneStringResources.PasteError.expectedRowExample` exactly when `rawRow` is non-null, and is null exactly when `rawRow` is null
- `PasteErrorViewModel.uiState.rawRow` still carries the pasted row's own text unchanged, never resolved through `PhoneStringResources`

## Dependencies

LabelRef — produced by this lot, `:core-domain`, `com.mgilli.core.domain.display`
SegmentBlueprint, SegmentType, Station — pre-existing (`:core-domain`, unchanged, used by `segmentName`)
DisplayFormatter, DateDisplay — pre-existing (`:core-domain`, unchanged)
androidx.compose.ui.res.stringResource — framework (Compose, already a dependency of `:app-phone`)
RaceRepository, ProfileRepository, PhoneNavigator, PasteResultViewModel — pre-existing, unaffected by this lot

## Conventions

§3 · `:core-domain` never imports Android — `LabelRef.id` is a plain `Int`, no Android type in its declaration
§9 · files named for the class they hold — `LabelRef.kt`
§10 · no hardcoded user-facing string; every key moves into `app-phone/res/values/strings.xml`, French only
§10 · interpolated values are passed as resource parameters, never concatenated — `LabelRef.args`, never string-templated into the id's text
§10 · the two apps keep separate resource files — this lot touches only `app-phone/res/values/strings.xml`
§14 · `:core-domain` unit tests run on the JVM alone — `LabelRef` needs none of its own beyond equality (a plain `data class`); `PhoneStringResourcesTest` moves to asserting on `id`/`args`, not text
