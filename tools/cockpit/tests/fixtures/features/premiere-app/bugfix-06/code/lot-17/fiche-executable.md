## Signatures

PhoneStringResources.DeleteConfirm.rejected: LabelRef
  — fixed key, no args; shown in the delete confirmation when
    RaceDetailViewModel.onDeleteConfirmed's Result is a failure

PhoneStringResources.Rename.rejected: LabelRef
  — fixed key, no args; its resource text names the one-to-forty
    trimmed-character bound (§10.1); shown in the rename dialog when
    RaceDetailViewModel.onRenameConfirmed's Result is a failure

PhoneStringResources.Preview.rejected: LabelRef
  — fixed key, no args; shown on the import preview screen when
    ImportPreviewViewModel.onSaveClicked's Result is a failure

PhoneStringResources.Profile.lastSyncFuture(time: String): LabelRef
  — fixed key, one arg (the zero-padded time of day DateDisplay.Future
    carries, §9.9); same shape as lastSyncToday/lastSyncYesterday;
    shown by ProfileViewModel.syncStatusText's DateDisplay.Future branch
    below

ProfileViewModel.syncStatusText(denied: Boolean, lastSyncSuccessAt: Instant?): LabelRef
  — unchanged signature; its when over DisplayFormatter.formatDateRelative's
    result gains `is DateDisplay.Future -> PhoneStringResources.Profile.lastSyncFuture(display.time)`,
    closing the branch DateDisplay.Future (lot-07) left unhandled and
    the exhaustive when now compiles; the denied, never, Today,
    Yesterday and Earlier branches are unchanged

## Acceptance criteria

- DeleteConfirm.rejected resolves to a LabelRef carrying its own resource id and no args, distinct from every other DeleteConfirm key
- Rename.rejected resolves to a LabelRef carrying its own resource id and no args, distinct from every other Rename key
- Preview.rejected resolves to a LabelRef carrying its own resource id and no args, distinct from every other Preview key
- None of the three keys' resolution is affected by the default Locale, matching the object's existing locale-independence test
- lastSyncFuture("09:02") resolves to a LabelRef carrying its own resource id and "09:02" as its single arg, distinct from lastSyncToday, lastSyncYesterday, lastSyncEarlier and lastSyncNever; its resolution is not affected by the default Locale, matching the object's existing locale-independence test
- syncStatusText, given a lastSyncSuccessAt whose local calendar date is after clock.now()'s (formatDateRelative returns DateDisplay.Future), returns PhoneStringResources.Profile.lastSyncFuture(display.time) — never lastSyncEarlier

## Dependencies

LabelRef — pre-existing
DateDisplay (DateDisplay.Future carrying time: String), DisplayFormatter.formatDateRelative — lot-07
ProfileViewModel — pre-existing; its syncStatusText is modified here, closing the compile break lot-07's verdict (code/lot-07/verdict.md) and architecte/realisateur-lot-07.md report against app-phone:compileDebugKotlin; decoupage.md's own lot-17 entry lists PhoneStringResources/PhoneStringResourcesTest only — this addition is the block's resolution of that divergence, ProfileViewModel's remaining §9.9-scoped rework stays lot-19's

## Conventions

R15 · a resource key present on both apps is duplicated per module, never shared
R62 · no synonym outside the established vocabulary
R63 · identifiers in English; the French text itself lives only in the resource file
R64 · no literal user-facing string in code — a key and a resource table

## Requests

—
