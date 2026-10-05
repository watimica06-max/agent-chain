## Status

PASS with reservation

## Cause

—

## Symbol divergences

ProjectionViewModel.onPressEnd — modified to forward `segmentDistanceM = null`, per the report's note of a resolved blocking decision; the sheet's Signatures section never names this call site of `SegmentMarkingController.onPressEnd`, only `MainRacePageViewModel`'s. The change itself is correct and consistent with the sheet's intent (this screen holds no distance-tracking state), and was resolved through the proper blocking channel rather than decided unilaterally — reported here because the sheet under-specified a call site of a signature it changed.
