## What I need

A confirmation of whether `ProjectionViewModelTest` — a plain
`ViewModel`-level test, not a Compose UI test — must run under
`@RunWith(RobolectricTestRunner::class)` once it reaches a code path
calling `android.util.Log`.

## Why the lot cannot proceed

It proceeds — this is not a blocker. The sheet's own criteria (R79,
R80: a repository failure and a `MarkingOutcome.Failed` are each logged
at ERROR) require tests that reach `android.util.Log.e(...)` from
`ProjectionViewModel`. Outside Robolectric, `android.util.Log`'s
methods are unmocked Android SDK stubs and throw at test time.
`ImportPreviewViewModelTest`, `ProfileRepositoryImplTest` and
`PasteErrorViewModelTest` all carry `@RunWith(RobolectricTestRunner::class)`
for the same reason, `ImportPreviewViewModelTest` combining it with the
same `Dispatchers.setMain(UnconfinedTestDispatcher())` this lot's sheet
already asks for. I applied that same pairing to
`ProjectionViewModelTest`.

## Where I met it

Writing the tests for the repository-failure and
`MarkingOutcome.Failed` acceptance criteria.

## What I think it is

add — a general trap: a `ViewModel` test that is not driven through a
`ComposeTestRule` and reaches a code path calling `android.util.Log`
needs `@RunWith(RobolectricTestRunner::class)`, on top of
`Dispatchers.setMain`/`resetMain` when it also touches
`viewModelScope` — the two are independent requirements met by the
same annotation/setup pairing.

## Verdict

**A convention. Written as R81 and R82, section 10 of
`docs/TECHNICAL_CONVENTIONS.md`.** The pairing applied to
`ProjectionViewModelTest` is what R81 requires; the lot proceeds as
written.

**Confirmed, and the answer does not depend on the test's level.** The
`android.jar` a JVM unit test compiles and runs against carries no
implementation: every framework method is a stub that throws
`Method … not mocked`. `android.util.Log.e` is one of them.
`@RunWith(RobolectricTestRunner::class)` is what supplies an
implementation off-device. Nothing about a `ComposeTestRule` enters into
it — the trigger is the code path, not the harness.

**But the platform does not impose Robolectric, and this project already
settles the point two different ways.** The build files:

- `:app-phone`, `:app-wear` — `testOptions.unitTests` sets
  `isIncludeAndroidResources = true` only. A stub throws. The three
  precedents named in this request live here.
- `:core-data` — no `testOptions` at all. A stub throws.
- `:core-sync`, `:core-platform` — `isReturnDefaultValues = true`. A stub
  **does not throw**: `Log.e` returns 0 in silence, and a test reaching it
  passes with no runner at all.

🔴 **That divergence is the gap, not the annotation.** A lot meeting the
red test is told *what* broke and never *which of three remedies to
take* — annotate the test, mock `Log`, or flip the module's build flag.
The third is cheaper, precedented in two modules of this very project,
and forbidden by nothing in force: R9 asks first before touching a file
whose change reaches beyond the lot, R66 counts dependencies and not
build flags. **R82 closes it**; R81 makes the choice uniform across the
five modules so no lot has to read a build file to know how its test
runs.

**No rule in force carried either half.** R56 says what a test may not
reach, R55 says which tests exist, and the R65 table named Robolectric
against no rule at all — under R67 it served nothing. Its scope cell now
names R81.

📌 **Both are marked `off-grid`**: no C10 entry of
`GRILLE_CONVENTIONS.md` reaches how a test is set up to reach the
framework. They cite §6.10 and §9.4, the entries whose ERROR log under
R79 puts a framework call inside a failure test in the first place.

⚠️ **R81's test is a review, not mechanical.** No tool of the R65 table
performs this check: detekt's declared scope is import, call, naming,
exception, `!!` and ignored-result, and the omission is caught by
`./gradlew check` in three modules only — in the two setting
`isReturnDefaultValues` it is silent, which is precisely why the rule is
written.

