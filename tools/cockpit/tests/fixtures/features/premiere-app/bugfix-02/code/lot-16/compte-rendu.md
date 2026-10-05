## Symbols

LabelRef — created, `:core-domain`, `com.mgilli.core.domain.display`
PhoneStringResources — modified, every member returns LabelRef instead of String
Profile.lastSync — removed
Profile.lastSyncNever — created, returns LabelRef, no args
Profile.lastSyncToday — modified, returns LabelRef, the full sentence
Profile.lastSyncYesterday — modified, returns LabelRef, the full sentence
Profile.lastSyncEarlier — created, returns LabelRef, the full sentence
ProfileViewModel.syncStatusText — modified, returns LabelRef
ProfileViewModel.toZoneRows — modified, label built as LabelRef
RaceDetailViewModel.buildCycles — modified, header built as LabelRef
RaceDetailViewModel.buildRow — modified, name built as LabelRef
PasteErrorViewModel.buildUiState — modified, title/body/expectedRow built as LabelRef
SegmentRowUiState — modified, name: LabelRef
CycleGroupUiState — modified, header: LabelRef
ZoneRowUiState — modified, label: LabelRef
ProfileUiState — modified, syncStatusText: LabelRef
PasteErrorUiState — modified, title/body: LabelRef, expectedRow: LabelRef?

## Build

analyze: clean (`:core-domain:check`, `:app-phone:check`, lint included)
test: 144 passed (`:app-phone`), previously-passing suite plus criterion-mapped additions

## State

Added: LabelRef
Removed: —

## Convention

—
