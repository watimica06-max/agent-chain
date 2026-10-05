## Symbols

PhoneNavigator — modified, `current` is now `StateFlow<PhoneDestination>`, class is `@Singleton`/`@Inject constructor()`
HyroxTrackerApplication — created
MainActivity — modified
ActivityBoundPermissionHost — created
RepositoryModule, ConnectivityModule, PlatformModule, SyncModule, TimingModule — created (`com.mgilli.hyroxtracker.di`, Hilt wiring for the seven `Needs` bindings plus the concrete classes they compose to)
FakePlatformModule, FakeRepositoryModule — created (`src/test`, `@TestInstallIn`-replace `PlatformModule`/`RepositoryModule` under Robolectric)

## Build

analyze: clean (`:app-phone:lintDebug` clean after `@SuppressLint("StateFlowValueCalledInComposition")` on the dispatch composable, matching the sheet's literal `pasteResultViewModel.uiState.value` read)
test: `:app-phone:check` clean — all tests pass, including a new `MainActivityTest` (Hilt+Robolectric+Compose) and `ActivityBoundPermissionHostTest`. `:core-domain:check`, `:core-data:check`, `:core-sync:check` re-run clean after the shared `gradle/libs.versions.toml` edit.

## State

Added: MainActivity (dispatch + Hilt entry point), the five `:app-phone` Hilt modules and the two test-only replacement modules, ActivityBoundPermissionHost, PhoneNavigator's `current` as a StateFlow
Removed: —

## Convention

—
