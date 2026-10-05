## Symbols

PasteErrorViewModel — modified, `SavedStateHandle` added to the constructor
PasteErrorViewModel.uiState — modified, built from the handle's four primitives when it carries them, from the `@Assisted` failure otherwise
PasteErrorViewModel.onBackToPasteClicked — unchanged

## Build

analyze: clean
test: `./gradlew :app-phone:check` — 306 tests completed, 1 failed

The 1 failure is pre-existing and outside this lot's scope:

- `MainActivityTest` (1) — "renders ImportPreviewScreen with the raceName
  and parsed success PasteResultViewModel produced" — owned by lot-27
  (`code/decoupage.md`: `Modifies: PhoneApp, MainActivityTest
  (:app-phone)`), the same failure `code/lot-22/blocked_realisateur-01.md`
  and `code/lot-22/compte-rendu.md` already name, reproducing on the
  commit this worktree started from with none of this lot's code present.

`PasteErrorViewModelTest`'s own 7 previously-failing cases (owned by this
lot per `code/lot-22/blocked_realisateur-01.md`'s decision) are fixed:
its `VALID_ROWS` fixture is rebuilt on the parser's current label
vocabulary (`Rox In`, `SkiErg Out`, …, matching `core-domain`'s own
`valid_result_no_header.txt` and `PasteResultViewModelTest`'s own
rebuilt `VALID_PASTE`) — the stale vocabulary parsed every mutated row
to `Failure(UNKNOWN_LABEL, 1, …)` before the intended row-level cause
was ever reached.

## State

Added: —
Removed: —

## Requests

—
