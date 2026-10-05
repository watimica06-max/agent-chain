## Signatures

settings.gradle.kts
  gains `include(":core-platform")`, alongside the existing
  `include(":core-sync")`

core-platform/build.gradle.kts — new file
  `com.android.library` plugin, same shape as `:core-sync`'s own
  (`core-sync/build.gradle.kts`): `namespace = "com.mgilli.core.platform"`,
  `compileSdk` release(37), `defaultConfig.minSdk = 31`,
  `kotlin { jvmToolchain(libs.versions.jdk.get().toInt()) }`
  dependencies:
    `implementation(project(":core-domain"))` — carries
      `ConnectivityPermissionSystem`, the interface lot-14's relocated
      `ConnectivityPermissionSystemImpl` implements; the same edge
      `:core-sync` already carries
    `androidx.activity` and `androidx.core` (the plain artifacts, not
      the `-compose`/`-ktx` extensions already in the catalog) as
      `implementation` — the two lot-14's `ConnectivityPermissionSystemImpl`
      needs for `ActivityResultLauncher`, `ContextCompat`, `ActivityCompat`;
      new entries in `gradle/libs.versions.toml` since neither is
      catalogued today
    `testImplementation(libs.junit)`, `testImplementation(libs.kotlinx.coroutines.test)`,
      `testImplementation(libs.robolectric)` — the relocated
      `ConnectivityPermissionSystemImplTest` (lot-14) is Robolectric-based
      and exercises a suspended `requestPermission`

app-phone/build.gradle.kts
  gains `implementation(project(":core-platform"))`, the same way it
  already carries `implementation(project(":core-sync"))`

app-wear/build.gradle.kts
  gains `implementation(project(":core-platform"))`, the same way it
  already carries `implementation(project(":core-sync"))`

## Acceptance criteria

- `:core-platform` is declared in `settings.gradle.kts` and
  `./gradlew :core-platform:check` exits 0 with no source in it yet
- `core-platform/build.gradle.kts` declares `androidx.activity` and
  `androidx.core` as compile dependencies — the two the Product Owner's
  decision names, absent from every other module's own dependency list
- `:app-phone`'s and `:app-wear`'s own `build.gradle.kts` each declare
  `implementation(project(":core-platform"))`, and
  `./gradlew :app-phone:check` / `./gradlew :app-wear:check` still exit 0

## Dependencies

androidx.activity, androidx.core — new version-catalog entries this lot
  adds; R66 authorizes it since this lot is the dependency's own,
  delivered on its own
core-domain — pre-existing, depended on the same way :core-sync already
  depends on it

## Conventions

R15 · any adapter both applications need lives in a module they both
  depend on and that depends on neither
R12 · :core-platform realizes §11.1 in the module table
R11 · no module named utils/common/helpers/misc/shared — named for what
  it holds
R14 · no module of another nature imports :app-phone or :app-wear
R66 · no new dependency inside a lot except one delivered on its own —
  this is that lot, for androidx.activity and androidx.core

## Requests

—
