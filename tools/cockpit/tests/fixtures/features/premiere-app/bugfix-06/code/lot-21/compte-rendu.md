## Symbols

ImportPreviewViewModel — modified, `:app-phone`
ImportPreviewViewModel.onSaveClicked — modified, `:app-phone`
ImportPreviewViewModel.onCorrectClicked — unchanged, `:app-phone`
ImportPreviewUiState — modified, `:app-phone`
ImportPreviewScreen — modified, `:app-phone`
ImportPreviewViewModelTest — modified, `:app-phone`
ImportPreviewScreenTest — created, `:app-phone`

## Build

analyze: `:app-phone:lint` clean
test: `:app-phone:testDebugUnitTest` — 289 total, 279 passed, 10 failed

The 10 failures are all pre-existing, outside this lot's Modifies list,
and unrelated to `ImportPreviewViewModel`/`ImportPreviewUiState`/
`ImportPreviewScreen`: `PasteResultViewModelTest` (2), `PasteErrorViewModelTest`
(7) and `MainActivityTest` (1) all fail on fixtures written against
`HyresultResultParser`'s pre-lot-01 output shape — a well-formed pasted
result that used to parse to `Success` now parses to `Failure` under
lot-01's rewrite. Per the decoupage, `PasteResultViewModelTest` is
adapted by lot-22, `PasteErrorViewModelTest` by lot-23, `MainActivityTest`
by lot-27 — all three declare `HyresultResultParser (lot-01)`/
`HyresultParseResult` as a dependency, none has run yet. Every test this
lot's own files touch passes; this lot's own fixture is built directly
through `HyresultParseResult.Success`'s public constructor rather than
through the real parser, so it carries no dependency on lot-01's output
shape.

## State

Added: —
Removed: —

## Requests

—
