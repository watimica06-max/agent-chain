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

Deliver lot-22 on its own code and its own passing tests, and name in
`code/lot-22/compte-rendu.md` the 8 failing tests together with the lot
`code/decoupage.md` gives each file — `PasteErrorViewModelTest` to
lot-23 (`Modifies: PasteErrorViewModel, PasteErrorUiState,
PasteErrorViewModelTest`) and `MainActivityTest` to lot-27 (`Modifies:
PhoneApp, MainActivityTest (:app-phone)`) — stating that the 8 failures
reproduce on the commit this worktree started from with none of
lot-22's code present.

R73 makes a red build deliverable where the report names the failing
call site and the lot that owns it, and the same problem is settled
that way twice in this cycle: `code/lot-20/blocked_realisateur-01.md`
decides these same two classes on these same terms, and
`code/lot-21/compte-rendu.md`, which names `PasteErrorViewModelTest`
(7) and `MainActivityTest` (1) as lot-23's and lot-27's, carries a PASS
in `code/lot-21/verdict.md`. R74 does not bite: the changed behaviour
is `HyresultResultParser.parse`'s, which lives in `:core-domain` and
not in the module holding the stale fixtures, and those fixtures still
compile — they fail at assertion time, not in the one-pass module
compile R74 rests on.

This does not extend to editing `MainActivityTest`,
`PasteErrorViewModelTest` or `PasteErrorViewModel` — those are lot-23's
and lot-27's — nor to any failure beyond those 8: a failure in
`PasteResultViewModelTest`, `PasteResultScreenTest` or any other
`:app-phone` class leaves R4 standing and blocks the lot again. This
lot's own already-rebuilt `PasteResultViewModelTest.VALID_PASTE`
fixture stays as it is.
