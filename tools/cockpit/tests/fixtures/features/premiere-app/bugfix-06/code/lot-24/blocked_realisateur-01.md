## What blocks

`./gradlew check` fails on `MainActivityTest.renders ImportPreviewScreen with
the raceName and parsed success PasteResultViewModel produced`, a test
outside this lot's scope, deterministically (not flaky): it cannot find the
text `1:08:50` in the rendered `ImportPreviewScreen` after a well-formed
30-row Hyresult paste.

## Where

`app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt`
(`ImportPreviewScreen`/`PasteResultViewModel`, package
`com.mgilli.hyroxtracker.ui.pasteresult`/`ui.importpreview`) — none of
which lot-24 touches. Lot-24's own scope is `RaceListScreen.kt` and its
tests (`ui.racelist`), which pass in isolation
(`./gradlew :app-phone:testDebugUnitTest --tests "*RaceList*"` is clean).
Confirmed by re-running `MainActivityTest` alone: same single failure,
same reason, both in isolation and as part of the full `check`.

## To resume

Confirm whether this failure predates lot-24 (a pre-existing regression
from an earlier lot in this bugfix cycle) or is a flake to re-run, then
either fix it in its owning lot or clear it so `./gradlew check` can exit
0 for lot-24's own delivery.

## Decision

Deliver lot-24 on its own code and its own passing tests, and name in
`code/lot-24/compte-rendu.md` the single failing test
`MainActivityTest."renders ImportPreviewScreen with the raceName and
parsed success PasteResultViewModel produced"` together with its owner,
lot-27 (`code/decoupage.md`: `Modifies: PhoneApp, MainActivityTest
(:app-phone)`), stating that it is pre-existing and reproduces with none
of lot-24's code present.

The failure is neither a flake nor a regression of this cycle's earlier
lots to re-open: `code/lot-27/fiche-executable.md` already takes it as
its own scope — "the stale fixture lot-21 and lot-22 deferred here under
R72 — its 30-row `VALID_HYRESULT_PASTE` constant is written on the label
vocabulary `HyresultResultParser` expected before lot-01" — and lot-27
runs next in block-12. R73 makes a red build deliverable where the
report names the failing call site and the lot that owns it, and this
same failure is settled on these same terms three times already in this
cycle: `code/lot-20/blocked_realisateur-01.md`,
`code/lot-22/blocked_realisateur-01.md` and
`code/lot-21/compte-rendu.md`, the last two carrying PASS verdicts.
R74 does not bite: the changed behaviour is `HyresultResultParser.parse`,
which lives in `:core-domain` and not in the module holding the stale
fixture, and that fixture still compiles — it fails at assertion time,
not in the one-pass module compile R74 rests on.

This does not extend to editing `MainActivityTest.kt` or `PhoneApp`,
which are lot-27's, nor to any failure beyond that one test: a second
failing `:app-phone` test, or any failure in `ui.racelist`, leaves R4
standing and blocks the lot again.
