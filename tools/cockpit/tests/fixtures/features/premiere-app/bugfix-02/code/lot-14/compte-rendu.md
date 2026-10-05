## Symbols

ControlScreen — modified, content container is ScalingLazyColumn, texts are androidx.wear.compose.material.Text
StopConfirmOverlay — modified, container is ScalingLazyColumn, texts are wear Text
EndOfRaceScreen — modified, container is ScalingLazyColumn, texts are wear Text
FinalDeltaText — modified, text is wear Text
WaitingForPhoneScreen — modified, container is ScalingLazyColumn, texts are wear Text
PreparationScreen — unchanged (dispatch only, no container of its own)
ReadyContent — modified, container is ScalingLazyColumn, texts are wear Text
ConflictDialog — modified, container is ScalingLazyColumn, texts are wear Text
WatchHistoryScreen — modified, both branches' container is ScalingLazyColumn, texts are wear Text
WatchHistoryRow — modified, texts are wear Text (own Column kept — it is an item's content, not the screen's top-level container)
HomeScreen — modified, content container is ScalingLazyColumn, texts are wear Text
MainRacePageScreen — modified, content container is ScalingLazyColumn, texts are wear Text
TopBlockText — modified, text is wear Text
CenterBlockText — modified, texts are wear Text
SensorPermissionScreen — modified, content container is ScalingLazyColumn, texts are wear Text
ProjectionScreen — modified, content container is ScalingLazyColumn, texts are wear Text
CumulativeDeltaText — modified, text is wear Text
EstimatedArrivalBlock — modified, texts are wear Text (own Column kept — not the screen's top-level container)

## Build

analyze: clean (:app-wear:check and :app-phone:check both green, lint included)
test: :app-wear:testDebugUnitTest all green — 1 new/extended Compose UI test per screen (2 for PreparationScreen's two states, 2 for WatchHistoryScreen's two states), full existing suite unaffected

## State

Added: gradle/libs.versions.toml carries wearCompose = "1.4.1" and the androidx-wear-compose-material/androidx-wear-compose-foundation aliases; app-wear/build.gradle.kts implements androidx.activity:activity-compose, androidx.wear.compose:compose-material, androidx.wear.compose:compose-foundation, and debugImplementation(libs.androidx.compose.ui.test.manifest)
Removed: HomeViewModel/HomeScreen's "no compose-testing setup yet" note (stale — every screen composable now has one); SensorPermissionViewModel/SensorPermissionScreen's "androidx.compose.material3 is now wired in" note (stale — replaced by the Wear Compose Material/Foundation trap)

## Convention

The sheet's per-composable rule ("the top-level content container is
ScalingLazyColumn, never Column or LazyColumn") is applied to composables
that own a whole-screen root container (`fillMaxSize()` + centering) —
the 9 screens plus StopConfirmOverlay/ReadyContent/ConflictDialog, and
WatchHistoryScreen's two branches. `WatchHistoryRow` and
`EstimatedArrivalBlock`, also named in the sheet's composable list, keep
their own small `androidx.compose.foundation.layout.Column` (three/two
stacked texts, not a screen root) — nesting a second scrolling
`ScalingLazyColumn` inside an item of the outer one measures with an
infinite height constraint and crashes at layout. Their text nodes still
draw from `androidx.wear.compose.material.Text`, per the sheet's other
rule. `:app-wear`'s `createComposeRule()` needs
`debugImplementation(libs.androidx.compose.ui.test.manifest)` to launch
its default activity, absent from the sheet's Dependencies list —
`:app-wear` carries no `MainActivity` yet (TECHNICAL_CONVENTIONS.md §2).
Added as a test-only dependency; documented as a trap in
CURRENT_TECHNICAL_STATE.md.
