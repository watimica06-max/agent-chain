## Signatures

ExampleInstrumentedTest — `app-phone/src/androidTest/java/com/mgilli/hyroxtracker/ExampleInstrumentedTest.kt` deleted, and the whole `app-phone/src/androidTest` source tree left empty.

app-phone/build.gradle.kts — the `androidTestImplementation(libs.androidx.junit)` and `androidTestImplementation(libs.androidx.espresso.core)` lines removed. `androidTestImplementation(platform(libs.androidx.compose.bom))` and `androidTestImplementation(libs.androidx.compose.ui.test.junit4)` are untouched — the entry names only `androidx.test.ext.junit` and `androidx.espresso.core`.

## Acceptance criteria

- `app-phone/src/androidTest/java/com/mgilli/hyroxtracker/ExampleInstrumentedTest.kt` no longer exists
- `app-phone/build.gradle.kts` declares neither `libs.androidx.junit` (`androidx.test.ext:junit`) nor `libs.androidx.espresso.core` (`androidx.test.espresso:espresso-core`) as a dependency

## Dependencies

—

## Conventions

§14 · `androidTest` is never used — nothing in the task graph runs it
