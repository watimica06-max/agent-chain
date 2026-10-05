## Signatures

Every one of the nine screens below keeps its existing parameters and
return type (`Unit`, `@Composable`) — nothing about how it is called
changes. What changes is what each draws from internally:

    ControlScreen(viewModel: ControlViewModel)
    EndOfRaceScreen(viewModel: EndOfRaceViewModel)
    WaitingForPhoneScreen(viewModel: WaitingForPhoneViewModel, onRetryClicked: () -> Unit)
    PreparationScreen(viewModel: PreparationViewModel)
    WatchHistoryScreen(uiState: WatchHistoryUiState)
    HomeScreen(viewModel: HomeViewModel, onHistoryClicked: () -> Unit)
    MainRacePageScreen(viewModel: MainRacePageViewModel)
    SensorPermissionScreen(viewModel: SensorPermissionViewModel)
    ProjectionScreen(viewModel: ProjectionViewModel)

For each, and for every private composable it delegates to in the same
file (`StopConfirmOverlay`, `FinalDeltaText`, `ReadyContent`,
`ConflictDialog`, `WatchHistoryRow`, `TopBlockText`, `CenterBlockText`,
`CumulativeDeltaText`, `EstimatedArrivalBlock`):

- every text node draws from `androidx.wear.compose.material.Text`,
  never `androidx.compose.material3.Text`
- the top-level content container is
  `androidx.wear.compose.foundation.lazy.ScalingLazyColumn`, never
  `androidx.compose.foundation.layout.Column` or
  `androidx.compose.foundation.lazy.LazyColumn`

`WatchHistoryScreen` keeps both its branches (empty-state message,
populated list via `items(uiState.entries)`), both now inside a
`ScalingLazyColumn`.

    // gradle/libs.versions.toml — new [libraries] entries
    androidx-wear-compose-material    = { group = "androidx.wear.compose", name = "compose-material",    version.ref = "wearCompose" }
    androidx-wear-compose-foundation  = { group = "androidx.wear.compose", name = "compose-foundation",  version.ref = "wearCompose" }

    // app-wear/build.gradle.kts — new dependencies
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.wear.compose.material)
    implementation(libs.androidx.wear.compose.foundation)

## Acceptance criteria

- `ControlScreen`'s content exposes a scroll-action node, which it did not before under `Column`
- `EndOfRaceScreen`'s content exposes a scroll-action node, which it did not before under `Column`
- `WaitingForPhoneScreen`'s content exposes a scroll-action node, which it did not before under `Column`
- `PreparationScreen`'s content exposes a scroll-action node in both its ready state and its sensor-conflict dialog state, which it did not before under `Column`
- `WatchHistoryScreen`'s content exposes a scroll-action node in both its empty state and its populated-list state
- `HomeScreen`'s content exposes a scroll-action node, which it did not before under `Column`
- `MainRacePageScreen`'s content exposes a scroll-action node, which it did not before under `Column`
- `SensorPermissionScreen`'s content exposes a scroll-action node, which it did not before under `Column`
- `ProjectionScreen`'s content exposes a scroll-action node, which it did not before under `Column`

## Dependencies

ControlScreen, EndOfRaceScreen, WaitingForPhoneScreen, PreparationScreen, WatchHistoryScreen, HomeScreen, MainRacePageScreen, SensorPermissionScreen, ProjectionScreen — pre-existing, modified by this lot
ControlViewModel, EndOfRaceViewModel, WaitingForPhoneViewModel, PreparationViewModel, WatchHistoryUiState, HomeViewModel, MainRacePageViewModel, SensorPermissionViewModel, ProjectionViewModel — pre-existing, unchanged
androidx.activity:activity-compose — alias `androidx-activity-compose`, already in the version catalogue (used today by `app-phone/build.gradle.kts`), added by this lot to `app-wear/build.gradle.kts`
androidx.wear.compose:compose-material, androidx.wear.compose:compose-foundation — new aliases, added by this lot to the version catalogue and to `app-wear/build.gradle.kts`

## Conventions

§1 · the mandatory stack names Compose for Wear OS on the watch
§3 · `:app-phone` and `:app-wear` never import each other — the swap stays inside `:app-wear`
§9 · composables are named `PascalCase`, a noun — unchanged names carried over
