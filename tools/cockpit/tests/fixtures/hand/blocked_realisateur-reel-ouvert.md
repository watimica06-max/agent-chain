## What blocks

`./gradlew :app-phone:testDebugUnitTest` (part of `:app-phone:check`, the
module this lot touches) fails on 8 pre-existing tests in
`MainActivityTest` and `PasteErrorViewModelTest` — neither file, nor the
symbols they exercise, belongs to this lot.

## Where

`app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt`
("renders ImportPreviewScreen with the raceName and parsed success
PasteResultViewModel produced") and
`app-phone/src/test/java/com/mgilli/hyroxtracker/ui/pasteerror/PasteErrorViewModelTest.kt`
(7 of its 12 cases). Both build a Hyresult paste fixture using the
label vocabulary the parser expected before lot-01 (`Run 1`,
`Roxzone 1`, `SkiErg`, …); `HyresultResultParser.parse` now expects
`Rox In`, `Rox Out`, `SkiErg Out`, … (`core-domain`'s own
`valid_result_no_header.txt` fixture carries the current vocabulary).
Every one of those stale fixtures now parses to
`Failure(UNKNOWN_LABEL, …)` on row 1 instead of `Success`, which is
what each of the 8 failing assertions actually shows. Confirmed
pre-existing: the same failures reproduce with this lot's own changes
stashed out, back to the commit this worktree started from.

This lot's own tests hit the identical stale-fixture issue in
`PasteResultViewModelTest`'s `VALID_PASTE`; since that file is this
lot's own to adapt (this lot modifies `onImportClicked`), its fixture
has been rebuilt on the parser's current vocabulary and now passes —
that fix is not extended to the two files above, outside this lot's
scope.

## To resume

Rebuild `MainActivityTest`'s and `PasteErrorViewModelTest`'s Hyresult
paste fixtures on the parser's current label vocabulary (as
`core-domain`'s `valid_result_no_header.txt` and this lot's own
corrected `PasteResultViewModelTest.VALID_PASTE` do), in whichever lot
owns those two files — or confirm one already does, so this lot can be
delivered once it lands.

## Decision

