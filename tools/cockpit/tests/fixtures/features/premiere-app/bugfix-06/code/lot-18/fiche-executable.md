## Signatures

WatchStringResources.Prep.launchRejected: LabelRef
  — fixed key, no args; shown when PreparationViewModel.onLaunchClicked's
    Result is a failure

WatchStringResources.Control.undoRejected: LabelRef
  — fixed key, no args; shown when ControlViewModel.onUndoClicked's
    Result is a failure

WatchStringResources.StopConfirm.rejected: LabelRef
  — fixed key, no args; shown when ControlViewModel.onStopConfirmed's
    Result is a failure

## Acceptance criteria

- Prep.launchRejected resolves to a LabelRef carrying its own resource id and no args, distinct from every other Prep key
- Control.undoRejected resolves to a LabelRef carrying its own resource id and no args, distinct from every other Control key
- StopConfirm.rejected resolves to a LabelRef carrying its own resource id and no args, distinct from every other StopConfirm key
- None of the three keys' resolution is affected by the default Locale, matching the object's existing locale-independence test

## Dependencies

LabelRef — pre-existing

## Conventions

R15 · a resource key present on both apps is duplicated per module, never shared
R62 · no synonym outside the established vocabulary
R63 · identifiers in English; the French text itself lives only in the resource file
R64 · no literal user-facing string in code — a key and a resource table

## Requests

—
