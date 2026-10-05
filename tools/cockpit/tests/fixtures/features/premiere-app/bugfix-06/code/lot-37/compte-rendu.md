## Symbols

WatchHistoryRow — modified, its `name` Text now carries `maxLines = 1`
  and `overflow = TextOverflow.Ellipsis`
WatchHistoryScreenTest — modified, carries the new tests (same-height,
  full-text-findable, date-and-total-time, 3-character-name-unchanged,
  empty-state-only criteria)

## Build

analyze: clean
test: 16 passed (`:app-wear:test` — WatchHistoryScreenTest 12,
  WatchHistoryViewModelTest 4)

## State

Added: —
Removed: —

## Requests

—
