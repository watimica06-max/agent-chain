## Symbols

ControlViewModel — modified, `savedStateHandle: SavedStateHandle` appended to the constructor
ControlUiState — modified, `undoRejectionMessage: LabelRef?` and `stopRejectionMessage: LabelRef?` added
ControlScreen — modified, renders `undoRejectionMessage` below the undo pill and `stopRejectionMessage` inside `StopConfirmOverlay`
ControlViewModelTest — modified, carries `@RunWith(RobolectricTestRunner::class)`, both direct constructions pass `savedStateHandle`, new tests cover the two `Result` folds, the coroutine-boundary criteria and the `SavedStateHandle` rebuild criteria
ControlScreenTest — modified, both direct constructions pass `savedStateHandle`, new tests cover the two rendered rejections

## Build

analyze: clean (`./gradlew check`)
test: all passed

## State

Added: —
Removed: —
(ControlViewModel/ControlScreen entry in docs/CURRENT_TECHNICAL_STATE.md rewritten to describe the two `Result` folds and the `SavedStateHandle` persistence, replacing the prior, now-false description)

`androidx.lifecycle.SavedStateHandle` reaches `:app-wear` the same way
it already reaches `ProjectionViewModel` (lot-39) — transitively,
through `androidx.hilt.navigation.compose` — with no direct
`gradle/libs.versions.toml` entry (R77, R78).

## Requests

—
