## Symbols

PasteResultViewModel — modified, `SavedStateHandle` added to the constructor
PasteResultViewModel.uiState — modified, initial value restored from the handle
PasteResultViewModel.onPastedTextChanged — modified, writes the handle
PasteResultViewModel.onRaceNameChanged — modified, writes the handle
PasteResultViewModel.onRaceDateChanged — modified, writes the handle
PasteResultUiState.isImportEnabled — modified, blank-aware rule
PasteResultViewModel.onImportClicked — modified, body runs inside viewModelScope.launch

## Build

analyze: clean
test: `./gradlew :app-phone:check` — 302 tests completed, 8 failed

The 8 failures reproduce on the commit this worktree started from, with
none of lot-22's code present, and touch neither the files nor the
symbols this lot modifies:

- `MainActivityTest` (1) — "renders ImportPreviewScreen with the
  raceName and parsed success PasteResultViewModel produced" — owned by
  lot-27 (`code/decoupage.md`: `Modifies: PhoneApp, MainActivityTest
  (:app-phone)`)
- `PasteErrorViewModelTest` (7) — every case but `EMPTY_PASTE` — owned
  by lot-23 (`code/decoupage.md`: `Modifies: PasteErrorViewModel,
  PasteErrorUiState, PasteErrorViewModelTest`)

Both build a Hyresult paste fixture on the label vocabulary the parser
expected before lot-01; `HyresultResultParser.parse` now expects the
vocabulary `core-domain`'s own `valid_result_no_header.txt` fixture
carries, so every stale fixture now parses to `Failure(UNKNOWN_LABEL,
…)` instead of `Success`.

## State

Added: —
Removed: —

## Requests

—
