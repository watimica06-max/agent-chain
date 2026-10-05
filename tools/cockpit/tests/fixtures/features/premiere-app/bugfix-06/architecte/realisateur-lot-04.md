## What I need

A confirmation that `./gradlew check` on the whole project is expected
to still fail on `:app-phone`, unrelated to this lot's scope.

## Why the lot cannot proceed

It proceeds — this is not a blocker. `./gradlew :core-domain:check`
exits 0 with this lot's changes. Running the project-wide `./gradlew
check` still fails, but at `:app-phone:compileDebugKotlin`, on
`ProfileViewModel.kt` calling `ProfileRepository.updateHrMaxBpm`,
`updateExpectedDistanceM`, `updateLongPressMs` and
`updateZoneThreshold` outside a coroutine — none of them are named in
this lot's sheet, dependencies or conventions, and no file under
`app-phone` was touched to reach a passing `:core-domain:check`. This
is the same pre-existing failure `realisateur-lot-01.md` and
`realisateur-lot-42.md` already report against different lots.

## Where I met it

Running `./gradlew check` (whole project) after this lot's changes were
complete and `:core-domain:check` had already passed on its own.

## What I think it is

add — the same note `realisateur-lot-42.md` already proposes: R4
(`./gradlew check` exits 0) for a lot scoped to one module, as this one
is to `:core-domain`, is verified module-scoped rather than
project-wide when another module carries an unrelated, pre-existing
compilation failure.

## Verdict

**A convention, and the same one `detailleur-lot-03.md` and
`realisateur-lot-42.md` carry. Written as R72 and R73, section 2 of
`docs/TECHNICAL_CONVENTIONS.md`.**

R72 makes this lot deliverable on `./gradlew :core-domain:check` exiting
0 while the only remaining project-wide failure is a call site another
lot's sheet adapts. R73 requires the report to name that call site and
the lot that adapts it.

🔴 **The same reservation as on `realisateur-lot-42.md`.** R72 does not
declare the `:app-phone` `ProfileViewModel` failure expected; it makes
this lot deliverable once a lot's sheet is named as adapting those call
sites. **If none does, that is a hole in the split, and it goes back
through the lot report.**
