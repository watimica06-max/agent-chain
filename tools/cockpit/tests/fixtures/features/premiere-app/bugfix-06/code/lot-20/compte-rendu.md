## Symbols

SegmentRowUiState — modified, `index` dropped
RaceDetailUiState — modified, `raceId` dropped, `renameRejectionMessage` and `deleteRejectionMessage` added
RaceDetailViewModel — modified, three constructor parameters appended, three write handlers moved into `viewModelScope.launch`, `SavedStateHandle`-backed dialog state
RaceDetailScreen — modified, bounded title/rename/delete-confirm rendering
RaceDetailViewModelTest — modified
RaceDetailScreenTest — created

## Build

analyze: clean
test: 68 passed (`RaceDetailViewModelTest` 65, `RaceDetailScreenTest` 3)

`./gradlew :app-phone:check` fails on 16 pre-existing failures, none in a
class this lot touches: `MainActivityTest`, `ImportPreviewViewModelTest`,
`PasteErrorViewModelTest`, `PasteResultViewModelTest`. `git stash`
(reverting every lot-20 file back to this worktree's `HEAD`) reproduces
the identical 16 failures with none of lot-20's code present, so they are
not fallout of this lot's diff. `code/decoupage.md` assigns each class to
another lot: `ImportPreviewViewModelTest` to lot-21,
`PasteResultViewModelTest` to lot-22, `PasteErrorViewModelTest` to
lot-23, `MainActivityTest` to lot-27. `code/lot-19/compte-rendu.md`
reports these same 16 failures in these same four classes on
`:app-phone`, with `code/lot-19/verdict.md` a PASS on that basis (R72,
R73).

## State

Added: —
Removed: —

## Requests

architecte/detailleur-lot-20.md
