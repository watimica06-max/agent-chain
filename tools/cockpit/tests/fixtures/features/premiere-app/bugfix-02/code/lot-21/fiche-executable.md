## Signatures

No symbol is produced or modified — this lot only adds dependencies that
compile and resolve, unused until lot-10/lot-11/lot-12/lot-13 consume
them. lot-10's and lot-12's blocked_detailleur.md decisions (PhoneNavigator
and WatchRaceNavigator each exposing `current` as a `StateFlow`, collected
by the root composable through `collectAsStateWithLifecycle`) are what the
newly-added dependency below serves — neither navigator's own modification
is part of this lot.

    // gradle/libs.versions.toml — [versions] entries
    hilt = "<a Hilt/Dagger release compatible with Kotlin 2.2.10 / AGP 9.3.1>"
    hiltNavigationCompose = "<an androidx.hilt:hilt-navigation-compose release compatible with hilt 2.60.1 / composeBom 2026.02.01>"

    // gradle/libs.versions.toml — [libraries] entries
    hilt-android          = { group = "com.google.dagger", name = "hilt-android",          version.ref = "hilt" }
    hilt-android-compiler  = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
    androidx-lifecycle-viewmodel-ktx     = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-ktx",     version.ref = "lifecycleRuntimeKtx" }
    androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
    androidx-hilt-navigation-compose     = { group = "androidx.hilt",      name = "hilt-navigation-compose",     version.ref = "hiltNavigationCompose" }
    // lifecycle-viewmodel-ktx/-compose share lifecycleRuntimeKtx's
    // version — androidx.lifecycle's artifacts release in lockstep, and
    // androidx-lifecycle-runtime-ktx is already pinned to that key.
    // hilt-navigation-compose is androidx.hilt, not com.google.dagger —
    // it versions independently of the hilt key and gets its own.
    // lot-11's and lot-13's blocked_detailleur.md decisions need its
    // creationCallback for their @AssistedFactory-backed ViewModels.

    // gradle/libs.versions.toml — new [libraries] entry
    androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }
    // lifecycle-runtime-compose is the artifact carrying
    // collectAsStateWithLifecycle — it shares lifecycleRuntimeKtx's
    // version key for the same lockstep reason as the two lines above.
    // lot-10's and lot-12's blocked_detailleur.md decisions need it to
    // collect PhoneNavigator's/WatchRaceNavigator's StateFlow<current
    // destination> from the root composable.

    // gradle/libs.versions.toml — new [plugins] entry
    hilt-android = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }

    // app-phone/build.gradle.kts and app-wear/build.gradle.kts — each
    // gets, in its own plugins { } block:
    alias(libs.plugins.hilt.android)
    alias(libs.plugins.ksp)
    // Neither module applies the ksp plugin today — only :core-data
    // does, for Room (lot-01). Hilt's annotation processor needs its
    // own ksp application in each module that uses it.

    // and, in its own dependencies { } block:
    implementation(libs.hilt.android)
    ksp(libs.hilt.android.compiler)
    implementation(libs.androidx.lifecycle.viewmodel.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.hilt.navigation.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    // ksp, not kapt, for hilt-android-compiler — the project already
    // runs Room's annotation processing through ksp (:core-data, lot-01)
    // and gradle.properties' existing
    // android.disallowKotlinSourceSets=false already covers a ksp
    // processor's generated-sources path under AGP's built-in Kotlin
    // compilation (CURRENT_TECHNICAL_STATE.md, Traps — general) —
    // introducing kapt as a second, separate annotation-processing
    // mechanism is not needed and not covered by that same trap.

## Acceptance criteria

- `gradle/libs.versions.toml` declares the `hilt` version, the `hilt-android`/`hilt-android-compiler` libraries, the `hilt-android` plugin, and the `androidx-lifecycle-viewmodel-ktx`/`androidx-lifecycle-viewmodel-compose` libraries
- `gradle/libs.versions.toml` declares the `hiltNavigationCompose` version and the `androidx-hilt-navigation-compose` library
- `gradle/libs.versions.toml` declares the `androidx-lifecycle-runtime-compose` library, sharing `lifecycleRuntimeKtx`'s version
- `app-phone/build.gradle.kts` applies the `hilt-android` and `ksp` plugins and declares `hilt-android`, `hilt-android-compiler` (as a `ksp` processor), `androidx-lifecycle-viewmodel-ktx`, `androidx-lifecycle-viewmodel-compose`, `androidx-hilt-navigation-compose` and `androidx-lifecycle-runtime-compose` as dependencies
- `app-wear/build.gradle.kts` applies the `hilt-android` and `ksp` plugins and declares the same six dependencies
- `./gradlew :app-phone:check` and `./gradlew :app-wear:check` both succeed with these dependencies present and no production code yet calling `collectAsStateWithLifecycle` or `hiltViewModel(creationCallback = ...)`

## Dependencies

— (this lot needs nothing pre-existing beyond the version catalogue and build files it edits)

## Conventions

§1 · the mandatory stack names Hilt for DI and ViewModel + StateFlow for state — no other DI framework
§14 · `JAVA_HOME` set before any Gradle command; one verification command per module (`./gradlew :<module>:check`)
