## Symbols

PhoneApp — modified, now internal (package-visible, not private).
  `LocalContext.current as? ComponentActivity` is a checked conversion:
  the back gesture calls `finish()` on a match when `navigator.back()`
  returns false, and does nothing on no match. The `ImportPreview` and
  `PasteError` branches render their screen only when
  `PasteResultViewModel.uiState.value.lastParseResult` is the expected
  variant; on any other value they render nothing and call
  `PhoneNavigator.backToPasteResult()` from a `LaunchedEffect(Unit)`
  entered with the branch.
MainActivity.onCreate / onDestroy — unchanged
MainActivityTest — modified. `VALID_HYRESULT_PASTE` rewritten on
  `HyresultResultParser`'s post-lot-01 label vocabulary (R72). Nine
  tests added for the guarded branches and the guarded host.

## Build

check (:app-phone): clean
test (:app-phone): 317 passed

## State

Added: `MainActivity`'s technical-state entry rewritten for `PhoneApp`'s
  guarded `ComponentActivity` cast and its `ImportPreview`/`PasteError`
  fallback to `backToPasteResult()`. New `Traps — general` entry: a
  `viewModelScope.launch` navigating after a `.flowOn(Dispatchers.IO)`
  hop needs `composeRule.waitUntil`, not a fixed count of
  `waitForIdle()` calls.
Removed: —

## Requests

—
