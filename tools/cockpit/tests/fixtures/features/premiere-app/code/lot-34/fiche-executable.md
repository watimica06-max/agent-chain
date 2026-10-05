## Signatures

data class WatchHistoryRowUiState(
  name: String, date: String, totalTime: String
)

data class WatchHistoryUiState(
  entries: List<WatchHistoryRowUiState>
)

class WatchHistoryViewModel(watchHistoryStore: WatchHistoryStore)
  val uiState: StateFlow<WatchHistoryUiState>

WatchHistoryScreen(uiState: WatchHistoryUiState) — Composable

## Acceptance criteria

- Given a non-empty list from `WatchHistoryStore.observe()`, the screen renders one row per entry, each showing that entry's name, date and total time.
- Given an empty list from `WatchHistoryStore.observe()`, the screen renders the empty-state title and explanation (`WatchStringResources.History.emptyTitle`/`emptyAction`) instead of any row.
- Whatever the list's content, no row exposes a control to mark a favorite, rename, or delete a race.
- Tapping a row triggers no navigation to a detail screen.

## Dependencies

WatchHistoryStore — produced by lot-21
RaceHistoryEntry — produced by lot-21
DesignTokens — produced by lot-02
WatchStringResources — produced by lot-44
