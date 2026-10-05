## Symbols

RaceListViewModel.uiState — modified
RaceDetailViewModel.uiState — modified
HomeViewModel's init observeReference collector — modified
PreparationViewModel's init observeReference collector — modified
MainActivity.WatchApp's referenceRace read — modified
collectReferenceRace — created, backs MainActivity.WatchApp's referenceRace read
ProfileSyncListenerServiceTest's fake RaceRepository — modified

MainActivityTest (:app-phone) — its `renders ImportPreviewScreen with the raceName
and parsed success PasteResultViewModel produced` test's `waitUntil` timeout,
raised from 5_000 to 20_000ms — a test-margin change outside this lot's named
symbols, applied per `code/lot-56/blocked_realisateur-01.md`'s decision.

## Build

check: `./gradlew check` — BUILD SUCCESSFUL across all six modules
(core-domain, core-data, core-sync, core-platform, app-phone, app-wear)

## State

Added: —
Removed: —
Corrected: PreparationViewModel / PreparationScreen entry in
CURRENT_TECHNICAL_STATE.md — openPreparation now runs on the first success,
not merely the first emission

## Requests

—
