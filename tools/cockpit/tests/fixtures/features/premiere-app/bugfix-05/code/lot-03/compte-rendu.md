## Symbols

PasteResultScreen — modified, the pastedText TextField now carries a
fixed height and a locally remembered `ScrollState`
PastedTextFieldTag — created, internal test-only testTag identifying
the pastedText field (it carries no visible text once filled)

## Build

analyze: clean (`:app-phone:check` — compile, lint, tests)
test: 190 passed

## State

Added: the pastedText field's `.verticalScroll(state).height(fixed)`
ordering trap, under "Traps — general"
Removed: —

## Convention

—
