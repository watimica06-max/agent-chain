## Signatures

RaceListScreen(viewModel: RaceListViewModel)
  — public composable, signature unchanged. Renders one card per
    RaceListItemUiState of viewModel.uiState, most recent first, and
    the empty state when the list is empty; unchanged by this lot.

RaceListCard(race: RaceListItemUiState, onClick: () -> Unit)
  — private composable in RaceListScreen.kt, signature unchanged.
    What changes: the Text rendering `race.name` is bounded — it takes
    a maxLines and TextOverflow.Ellipsis sized to a list row, and a
    weight inside its Row, so a name of any length within the 1–40
    character bound never grows the card's height and never reduces the
    width the `race.totalTime` Text gets. The `race.totalTime`,
    `race.date` and badge Texts are unchanged: none renders a race name
    or a label built from one.

RaceListViewModel — unchanged by this lot.
  — `uiState: StateFlow<RaceListUiState>`, and `toItem` keeps carrying
    `race.name` whole into `RaceListItemUiState.name`: the bound is a
    rendering bound, never a truncation of the value. No name is cut,
    padded or ellipsized before it reaches the screen.

## Acceptance criteria

- A race named with 40 characters renders its card's name at the same
  height as a race named with 3 characters
- A race named with 40 characters renders its card's total time at the
  same width as a race named with 3 characters, and it stays displayed
- A race named with 3 characters renders its name and its total time
  side by side, both displayed, unchanged from today
- The name RaceListItemUiState carries for a 40-character race name is
  those 40 characters, whole

## Dependencies

RaceRepository — pre-existing; `observeAll(): Flow<List<Race>>` feeds
  RaceListViewModel.uiState, untouched here
RaceListItemUiState, RaceListUiState — pre-existing (RaceListUiState.kt)
DesignTokens, PhoneStringResources — pre-existing; no token and no key
  is added
androidx.compose.ui.text.style.TextOverflow — Jetpack Compose, R65

## Conventions

R4 · `./gradlew check` exits 0
R12 · a §9 phone screen is realised in `:app-phone`
R47 · a screen reads a source once per entry, never in a composition body
R55 · one nominal and one failure test per public function, same lot
R62 · the lexicon — Race, Total
R63 · English identifiers and comments; one guarantee line per exported symbol
R64 · no user-facing string literal in the code
R71 · Compose only, no XML layout

## Requests

—
