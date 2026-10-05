## Signatures

PasteResultScreen(viewModel: PasteResultViewModel): @Composable Unit —
the pastedText TextField takes a fixed height and scrolls its own
content past it, so the race name field, the date and the "Importer"
action keep a fixed, reachable position regardless of how many rows
are pasted.

No new symbol is created and no public signature changes — this is a
Composable-internal layout change (a Modifier addition, plus a locally
remembered scroll state).

## Acceptance criteria

- The pastedText TextField's rendered height is the same whether it
  holds a single pasted line or enough lines to overflow the screen
- Content beyond the field's fixed height stays reachable by scrolling
  within the field itself
- The race name field, the date and the "Importer" action keep the
  same on-screen position whether the pasted text holds one line or
  enough to overflow the field

## Dependencies

PasteResultUiState — pre-existing (pastedText, raceName, raceDate,
maxSelectableDate, isImportEnabled), unmodified
PasteResultViewModel — pre-existing (onPastedTextChanged,
onRaceNameChanged, onRaceDateChanged, onImportClicked), unmodified

## Conventions

§11 · a text being typed, a dialog open or closed, a toggle between two
views: those are the composable's own, and belong in remember, not the
state class — the field's scroll state stays local, not added to
PasteResultUiState
