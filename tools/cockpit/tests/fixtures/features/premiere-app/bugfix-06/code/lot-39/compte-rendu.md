## Symbols

ProjectionViewModel — modified, two constructor parameters appended
  (`RaceRecordingRepository`, `SavedStateHandle`); `onPressEnd` and the
  constructor-time retained-race read now run on `viewModelScope`
ProjectionViewModelTest — modified, every construction converted to the
  new constructor shape; new tests for the coroutine-timing, the
  retained-race read and the rebuild-across-instances criteria
ProjectionScreenTest — modified, its own direct `ProjectionViewModel`
  construction converted to the new constructor shape (R74) — not named
  under the sheet's own `## Signatures`, but a call site inside
  `:app-wear`

## Build

analyze: clean (`./gradlew :app-wear:check` — lint)
test: 430 passed, 0 failed (`:app-wear`)

## State

Added: `ProjectionViewModel`'s constructor-time `RaceRecordingRepository
  .findInProgress()` read and its `SavedStateHandle` persistence
  (held race id, `lastKnownNow`, current lap delta primitives)
Removed: `ProjectionViewModel` from the state document's list of
  ViewModels needing no stubbed Main dispatcher in their tests — it now
  touches `viewModelScope`

`androidx.lifecycle.SavedStateHandle` reaches `:app-wear` the same way
it already reaches `:app-phone` — transitively, through
`androidx.hilt.navigation.compose` — with no direct
`gradle/libs.versions.toml` entry (R77, R78).

## Requests

architecte/realisateur-lot-39.md
