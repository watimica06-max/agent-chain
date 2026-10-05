## Symbols

WatchApp — modified, installs a root `BackHandler(enabled = !navigator.backGestureEnabled) { }` around its `when(destination)` dispatch
WatchApp's PREPARATION branch — modified, wraps `PreparationScreen` in an unconditional `BackHandler { navigator.quitPreparation() }`

## Build

analyze: clean
test: :app-wear:check — 121 tasks, BUILD SUCCESSFUL, all tests passed (6/6 new in MainActivityBackGestureTest)

## State

Added: —
Removed: —

## Convention

—
