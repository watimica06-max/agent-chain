## What I need

A confirmation that `./gradlew check` on the whole project is expected
to still fail on `:app-phone`, unrelated to this lot's scope.

## Why the lot cannot proceed

It proceeds — this is not a blocker. `./gradlew :app-wear:check` exits
0 with this lot's changes, restoring `:app-wear`'s compilation as this
lot's own dependencies section states. Running the project-wide
`./gradlew check` still fails, but at `:app-phone:compileDebugKotlin`,
on `ProfileViewModel.kt` calling `ProfileRepository.updateHrMaxBpm`,
`updateExpectedDistanceM`, `updateLongPressMs` and
`updateZoneThreshold` outside a coroutine — none of them are named in
this lot's sheet, dependencies or conventions, and no file under
`app-phone` was touched to reach a passing `:app-wear:check`.

## Where I met it

Running `./gradlew check` (whole project) after this lot's changes were
complete and `:app-wear:check` had already passed on its own.

## What I think it is

add — a note that R4 (`./gradlew check` exits 0) for a lot scoped to
one module, as this one is to `:app-wear`, is verified module-scoped
rather than project-wide when another module carries an unrelated,
pre-existing compilation failure.

## Verdict

**A convention, and the same one `detailleur-lot-03.md` carries. Written
as R72 and R73, section 2 of `docs/TECHNICAL_CONVENTIONS.md`.**

R72 makes this lot deliverable on `./gradlew :app-wear:check` exiting 0
while the only remaining project-wide failure is a call site another
lot's sheet adapts. R73 requires the report to name that call site and
the lot that adapts it.

🔴 **R72 does not confirm what this request asks.** It does not settle
that the `:app-phone` `ProfileViewModel` failure is expected — it makes
this lot deliverable only once a lot's sheet is named as adapting those
four call sites. Whether one does is a fact of the split, which this
agent does not read. **If no sheet names them, the split has a hole and
that goes back through the lot report — not into this file.**
