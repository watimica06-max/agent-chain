## Signatures

### WatchHistoryScreen — modification (`:app-wear`)

After the change:

    @Composable fun WatchHistoryScreen(uiState: WatchHistoryUiState)
      — signature unchanged.

    @Composable private fun WatchHistoryRow(row: WatchHistoryRowUiState)
      — signature unchanged.

What changes:

- The `Text` rendering `row.name` — the only `Text` of this file carrying
  a race name — takes `maxLines = 1` and `overflow =
  TextOverflow.Ellipsis` (§9.8). The name occupies its own row of the
  column, above the date and the total time, on a watch screen: one line,
  the overflow elided at its end.
- The `Text` rendering `row.date` and the `Text` rendering `row.totalTime`
  are untouched: neither carries a race name nor a label built from one.
  Both are formatter output of fixed width.
- The empty-state branch is untouched: `WatchStringResources.History
  .emptyTitle` and `.emptyAction` carry no race name.
- `isHistoryEmpty(uiState: WatchHistoryUiState): Boolean` is unchanged —
  true exactly when `uiState.entries` is empty.

### WatchHistoryViewModel — no change (`:app-wear`)

    @HiltViewModel
    class WatchHistoryViewModel @Inject constructor(
      watchHistoryStore: WatchHistoryStore
    ) : ViewModel()

    val uiState: StateFlow<WatchHistoryUiState>

- The constructor, `uiState` and the `RaceHistoryEntry` → row mapping are
  unchanged. `WatchHistoryRowUiState.name` stays the store's own name,
  neither truncated nor elided in the ViewModel: §9.8 bounds the rendering,
  never the value. `decoupage.md` lists this file under `Modifies`; §9.8
  carries no rule for it, and the lot leaves it as it stands.
- `init` already collects `WatchHistoryStore.observe()` inside
  `viewModelScope.launch`; nothing about that changes here.

### WatchHistoryUiState — no change (`:app-wear`)

    data class WatchHistoryRowUiState(name: String, date: String, totalTime: String)
    data class WatchHistoryUiState(entries: List<WatchHistoryRowUiState>)

- No field added, none dropped, none retyped.

### WatchHistoryScreenTest — modification (`:app-wear`)

- Built on the module's existing `createComposeRule()` shape, as it
  already is.

## Acceptance criteria

- `WatchHistoryScreen` composed on one entry whose name is 40 characters
  long renders that name at the same height as the same screen composed on
  one entry whose name is 3 characters long, every other field of the two
  entries being equal.
- On that same 40-character entry, the full name is still findable in the
  semantics tree by its exact text — the value is elided at render, never
  shortened in the state.
- On that same 40-character entry, the row's date text and its total-time
  text are both rendered, each with its own exact text.
- `WatchHistoryScreen` composed on an entry whose name is 3 characters
  long renders that name, that date and that total time, unchanged from
  today.
- `WatchHistoryScreen` composed on an empty `WatchHistoryUiState` renders
  the texts of `history_empty_title` and `history_empty_action`, and no
  row.
- `WatchHistoryViewModel` built on a `WatchHistoryStore` emitting one
  `RaceHistoryEntry` whose name is 40 characters long exposes that name in
  full in `uiState.value.entries[0].name` — 40 characters, no ellipsis
  character, no truncation.

## Dependencies

WatchHistoryStore.observe(): Flow<List<RaceHistoryEntry>> — pre-existing
  (`:core-domain`), bound in `:app-wear`; not `suspend`, re-emitting on
  every `replaceAll`. `replaceAll` is already `suspend` at this lot's turn
  (lot-48 of this cycle). This lot touches neither.
RaceHistoryEntry (`name`, `date`, `totalTimeMs`) — pre-existing
  (`:core-domain`), unchanged
DisplayFormatter.formatDate(Instant): String — pre-existing (`:core-domain`),
  unchanged by this lot
DurationTruncationService.truncateToSeconds(ms: Long): Long — pre-existing
  (`:core-domain`), unchanged
DisplayFormatter.formatDurationTotal(totalSeconds: Long): String — pre-existing,
  corrected by lot-07 of this cycle (negative totals); reused, never
  redeclared, and not called from this lot's own diff
WatchStringResources.History.emptyTitle / .emptyAction — pre-existing
  (`:app-wear`), unchanged
DesignTokens.Typography / .Color / .Spacing — pre-existing (`:app-wear`)
TextOverflow, maxLines, Text (Wear Compose), ScalingLazyColumn,
  viewModelScope, StateFlow — Jetpack Compose / Compose for Wear OS /
  AndroidX; not project symbols, already on `:app-wear`'s classpath. No
  `Text` in this repository sets `maxLines` or `overflow` at HEAD.

Traps carried by these symbols:
- `:app-wear`'s plain `createComposeRule()` relies on
  `debugImplementation(ui-test-manifest)`, already on the module;
  `WatchHistoryScreenTest` is built this way and stays so.
- a `performClick()` on a `ScalingLazyColumn` item past the viewport
  silently no-ops. This screen's rows carry no click handler, so no
  criterion above needs `performScrollTo()`; a criterion asserting on a
  row past the visible height still needs the node to be composed.
- `stringResource(id, *args)` always runs `String.format`: the two
  empty-state labels resolve through the vararg overload today and keep
  doing so.
- `WatchHistoryViewModel` touches `viewModelScope` in its own `init` — a
  plain JVM test constructing it needs `Dispatchers.setMain(...)` in
  `@Before` and `Dispatchers.resetMain()` in `@After`.

## Conventions

§2 · R4 — `./gradlew check` exits 0, the one definition of done
§2 · R74 — a call site of anything this lot changes that sits in
  `:app-wear` is this lot's own scope, never deferred
§4 · R12 — §9.8's watch half is realised in `:app-wear`
§5 · R18 — data crossing a public boundary is immutable; the row state
  stays a `data class` of read-only fields
§7 · R47 — a screen reads a source once per entry, never in a composition
  body; nothing is read from the composition here
§10 · R55 — one nominal and one failure test per public function,
  delivered in this lot
§10 · R56 — no test reaches I/O or the system clock
§11 · R62 — the lexicon: Race, Total, Duration; no synonym
§11 · R63 — English identifiers and comments; every exported symbol
  carries one line saying what it guarantees and when it fails
§11 · R64 — no user-facing string is a literal in the code; the two
  empty-state lines stay `LabelRef`s into the watch catalogue, and no key
  is added
§12 · R66 — no new dependency inside this lot; `TextOverflow` is already
  on the module's classpath

## Requests

—
