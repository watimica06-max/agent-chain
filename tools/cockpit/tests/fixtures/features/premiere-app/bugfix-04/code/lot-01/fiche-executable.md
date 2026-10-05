## Signatures

WatchApp(...) — installs a root
  `BackHandler(enabled = !navigator.backGestureEnabled) { }`
  around its `when(destination)` dispatch: consumes the gesture, doing
  nothing, while `backGestureEnabled` is false (MAIN, PROJECTION,
  CONTROL, END); disabled — leaving the system's default effect in
  place — while `backGestureEnabled` is true (HOME, PREPARATION).

WatchApp's PREPARATION branch — wraps `PreparationScreen` in
  `BackHandler { navigator.quitPreparation() }`, unconditionally
  enabled for as long as that branch is composed.

## Acceptance criteria

- On MAIN, the system back gesture is consumed and has no effect: `WatchRaceNavigator.current` stays MAIN
- On PROJECTION, the system back gesture is consumed and has no effect: `current` stays PROJECTION
- On CONTROL, the system back gesture is consumed and has no effect: `current` stays CONTROL
- On END, the system back gesture is consumed and has no effect: `current` stays END
- On PREPARATION, the system back gesture calls `WatchRaceNavigator.quitPreparation()`, moving `current` to HOME — the same effect as the existing "Quitter" tap
- On HOME, `WatchApp`'s root back handling is disabled and does not intercept the gesture, leaving the pre-existing behaviour (including the nested `showingHistory` handler) untouched

## Dependencies

WatchRaceNavigator.backGestureEnabled — pre-existing
WatchRaceNavigator.quitPreparation() — pre-existing
androidx.activity.compose.BackHandler — framework, already used elsewhere in `WatchApp`

## Conventions

§9 · composables are `PascalCase`, a noun — `WatchApp` and `PreparationScreen` keep their existing names
§11 · application state never lives in a composable — the new handling reads only `WatchRaceNavigator.backGestureEnabled`, no new composable-local navigation state
