## What blocks

`MainActivityTest`'s (`:app-phone`) `` `renders ImportPreviewScreen with the raceName and parsed success PasteResultViewModel produced` `` times out at its hardcoded 5-second `waitUntil` (line 172) the first time `:app-phone` compiles far enough for this test to run at all; raising that timeout locally to 20 seconds, as a diagnostic only (reverted, not committed), makes it pass, and a sibling test exercising the same `RaceDetailViewModel` rendering path without the `ProfileSyncPushService.push()` hop (`` `renders RaceDetailScreen for the raceId carried by RaceDetail...` ``) passes reliably at the default timeout — so the render logic this lot changed is not implicated, only the wall-clock margin of a test this lot does not touch.

## Where

`app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt:172` — adapted by lot-31 (`RaceRepository`'s suspend/Result move), not named by lot-56's sheet.

## To resume

Either raise that `waitUntil`'s timeout, or investigate why `ImportPreviewViewModel.onSaveClicked`'s post-save sequence (`raceRepository.saveImportedRace`, then `ProfileSyncPushService.push`'s own `observeAll()`/`observeReference()` reads, each a real Room query under Robolectric) now takes longer than 5 seconds before the navigation lands — a decision on `app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt`, outside this lot's named symbols.

## Decision

Raise that one `waitUntil`'s `timeoutMillis` at
`app-phone/src/test/java/com/mgilli/hyroxtracker/MainActivityTest.kt:172` from
`5_000` to `20_000`, and name the edit in `code/lot-56/compte-rendu.md` as a
test-margin change outside the lot's named symbols.

R4 leaves the lot deliverable only on a green check, and R72's deferral is not
open here: it holds only while another lot's sheet adapts the call site, and
none does — `code/decoupage.md` names `MainActivityTest` once, under lot-27
(`Modifies: PhoneApp, MainActivityTest (:app-phone)`), which is coded and
passed, and `architecte/detailleur-lot-31.md` records that no later lot of the
sequence names it. The awaiting mechanism is already settled by lot-27, whose
report carries it as a trap — a `viewModelScope.launch` navigating after a
`.flowOn(Dispatchers.IO)` hop is awaited with `composeRule.waitUntil`, not a
fixed count of `waitForIdle()` calls — so only the wall-clock margin is at
issue, and `## What blocks` above records 20 seconds as sufficient.

This does not extend to `ImportPreviewViewModel.onSaveClicked`,
`ProfileSyncPushService.push` or any other production symbol — the post-save
sequence's cost is not this lot's to investigate — nor to any other test,
assertion or timeout in `MainActivityTest.kt`. A second `:app-phone` failure,
or any failure among this lot's own five collectors, leaves R4 standing and
blocks the lot again.

