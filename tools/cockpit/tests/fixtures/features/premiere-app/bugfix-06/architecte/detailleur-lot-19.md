## What I need

Whether making an AndroidX artifact that is currently reachable only as a
transitive dependency into an explicit entry in `gradle/libs.versions.toml`
and in a module's `build.gradle.kts` counts as R66's "new dependency inside
a lot" — and, if it does, which lot is allowed to add it.

The artifact is `androidx.lifecycle:lifecycle-viewmodel-savedstate`, the one
carrying `androidx.lifecycle.SavedStateHandle`.

## Why the lot cannot proceed

It proceeds. The sheet is written against the conventions as they stand,
taking `SavedStateHandle` as framework-provided the way `decoupage.md`
declares it. This is the property two lots would answer differently, not a
blocker.

## Where I met it

§12.2 gives nine ViewModels a `SavedStateHandle`. Five of them are phone
lots — lot-19 (`ProfileViewModel`), lot-20 (`RaceDetailViewModel`), lot-21
(`ImportPreviewViewModel`), lot-22 (`PasteResultViewModel`), lot-23
(`PasteErrorViewModel`) — and four are watch lots. Every one of the nine
needs the same import.

Confirmed by grep:

- `SavedStateHandle` appears in no `.kt` file of this repository.
- `gradle/libs.versions.toml` carries `lifecycle-runtime-ktx`,
  `lifecycle-viewmodel-ktx`, `lifecycle-viewmodel-compose` and
  `lifecycle-runtime-compose`, all on `lifecycleRuntimeKtx = "2.6.1"`, and
  no `lifecycle-viewmodel-savedstate` entry.
- `app-phone/build.gradle.kts` declares
  `androidx.hilt.navigation.compose`, whose own dependency chain is the
  only route by which `SavedStateHandle` reaches the compile classpath.
- No `*.lockfile` exists anywhere in the repository, so R7's locking is not
  in force and resolution is live.

The two answers differ in what the Réalisateur writes: relying on the
transitive means touching no build file at all; making it explicit means a
version-catalog entry and a `build.gradle.kts` line in `:app-phone` and
`:app-wear`, which reads as R66's prohibited addition unless this says
otherwise. Whichever answer holds must hold for all nine lots — five of
them in `:app-phone`, and the first is lot-19.

## What I think it is

update — R66 says nothing about an artifact already on the classpath, and
R65's table names no lifecycle artifact at all.

## Verdict

**A convention. Written as R77 and R78, section 12 of
`docs/TECHNICAL_CONVENTIONS.md`.** The nine lots proceed with no build
file touched.

**R66 was genuinely open, and that is why a rule was needed.** Its text —
"no new dependency inside a lot" — does not say whether *new* means new
to the resolved classpath or new to the manifest. Its test does:
`couverture.md` records R66 as mechanical under G12.2, whose check is *a
manifest diff inside a lot fails*. **R77 writes that into the rule** —
what R66 counts is the manifest. Nothing on the classpath is new; an
entry in `libs.versions.toml` or a line in a `build.gradle.kts` is.

**The route is real, and shorter than the request supposed.** Checked
against the published POMs, not recalled:

- `androidx.lifecycle:lifecycle-viewmodel-compose` is declared
  explicitly in **both** `app-phone/build.gradle.kts` and
  `app-wear/build.gradle.kts` — it is not reached only through
  `hilt-navigation-compose`.
- `lifecycle-viewmodel-compose-android:2.9.1` depends on
  `androidx.lifecycle:lifecycle-viewmodel-savedstate` at **compile**
  scope, on a strict version `[2.9.1]`. Gradle maps a Maven `compile`
  scope to `api`, so that edge is on the consumer's compile classpath —
  `implementation` strips transitives for *project* dependencies, never
  for external modules.
- `androidx.hilt:hilt-navigation-compose:1.3.0` requires
  `lifecycle-viewmodel-compose:2.9.1`, so the catalog's
  `lifecycleRuntimeKtx = "2.6.1"` is a floor conflict resolution raises,
  not the version in force.

**`SavedStateHandle` therefore compiles in both applications as things
stand** — all five phone lots and all four watch lots, with no build
file edited.

⚠️ **R78 is the price of that answer.** Relying on an edge the project
does not declare is defensible only while someone records it, so each
such lot names the artifact in its report.

📌 **"Which lot is allowed to add it" is not settled here, and needs no
settling.** R66 already answers it — an addition is *delivered on its
own*, so no lot in the split adds it; a promotion to an explicit entry
is its own amendment. **This agent does not settle the split** in any
case.

---

⚠️ **A separate finding, not settled by this request: R65's table is
stale against the build.** Reading the build files was allowed here, and
seven rows disagree with them — AGP 8.9 against 9.3.2, Kotlin 2.1
against 2.2.10, `compileSdk` 36 against 37, `minSdk` 30/34 against 31/31,
Compose BOM 2025.04 against 2026.02.01, Health Services 1.1 against
1.0.0, Play Services Wearable 19.0 against 18.0.0. 🔴 **Under R1 the
file wins, which would read as an instruction to downgrade the build** —
plainly not what R65 intends. 📌 **Not corrected here**: `minSdk` and
`compileSdk` decide which watches run the application, which is a product
decision, and the rest should be settled in one pass rather than
piecemeal. **Raise it to the Product Owner as its own amendment.**
