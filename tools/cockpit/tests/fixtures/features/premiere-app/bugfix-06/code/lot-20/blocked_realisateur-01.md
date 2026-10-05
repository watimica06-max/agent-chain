## What blocks

`./gradlew :app-phone:check` fails on 16 pre-existing test failures in `MainActivityTest`,
`ImportPreviewViewModelTest`, `PasteErrorViewModelTest` and `PasteResultViewModelTest` —
none of which lot-20 touches — so R4's one definition of done cannot be met even though
lot-20's own code and its 68 tests (`RaceDetailViewModelTest`, `RaceDetailScreenTest`) are
complete and all pass.

## Where

`app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt`,
`app-phone/src/test/java/com/mgilli/hyroxtracker/ui/importpreview/ImportPreviewViewModelTest.kt`,
`app-phone/src/test/java/com/mgilli/hyroxtracker/ui/pasteerror/PasteErrorViewModelTest.kt`,
`app-phone/src/test/java/com/mgilli/hyroxtracker/ui/pasteresult/PasteResultViewModelTest.kt`.

Confirmed pre-existing: `git stash` (reverting every lot-20 file back to this worktree's
`HEAD`) and re-running those four classes reproduces the identical 16 failures — the same
assertion errors, `ClassCastException`s and `NoClassDefFoundError`s, at the same lines —
with none of lot-20's code present.

## To resume

Whichever lot owns `MainActivityTest`/`ImportPreviewViewModelTest`/`PasteErrorViewModelTest`/
`PasteResultViewModelTest` needs to fix them (or the Product Owner confirms the module-wide
`check` is not lot-20's to satisfy while that regression stands), before this lot can show a
clean `./gradlew :app-phone:check`.

## Decision

Deliver lot-20 on its own code and its 68 passing tests, and name in
`code/lot-20/compte-rendu.md` the four failing classes together with the lot
`code/decoupage.md` gives each one: `ImportPreviewViewModelTest` to lot-21,
`PasteResultViewModelTest` to lot-22, `PasteErrorViewModelTest` to lot-23,
`MainActivityTest` to lot-27 (`Modifies: PhoneApp, MainActivityTest
(:app-phone)`), stating that the 16 failures reproduce on this worktree's
`HEAD` with none of lot-20's code present.

R73 makes a red build deliverable only where the report names the failure and
the lot that owns it, and the same problem is solved that way in this cycle:
`code/lot-19/compte-rendu.md` reports these identical 16 failures in these
same four classes on `:app-phone` and `code/lot-19/verdict.md` is a PASS, and
`code/lot-30/verdict.md` accepts a pre-existing break owned by another lot on
the same terms. R74 does not bite here: it governs a call site broken by a
signature this lot changed, and the `git stash` re-run establishes these
failures are not fallout of lot-20's diff.

This does not extend to editing `MainActivityTest`,
`ImportPreviewViewModelTest`, `PasteErrorViewModelTest`,
`PasteResultViewModelTest` or the ViewModels they exercise — those belong to
lots 21, 22, 23 and 27 — nor to any failure beyond those 16: a failure in
`RaceDetailViewModelTest`, `RaceDetailScreenTest` or any other class leaves R4
standing and blocks the lot again.
