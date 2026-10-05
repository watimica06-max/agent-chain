- Neither application module has a working entry point. `app-wear`
  declares no activity at all in its manifest, so the watch app
  installs and never appears in the launcher. `app-phone` declares one,
  but it is the Android Studio template's, showing a
  `Greeting("Android")` screen instead of the application. Each module
  needs an `Application` class for dependency injection, a
  `MainActivity` hosting the root composable, and both declared in its
  manifest.

- No root composable exists on either module. On the watch it reads
  `WatchRaceNavigator.current` and renders the matching screen —
  `WatchDestination` and the navigator already carry the whole rule,
  including the first-launch choice among the permission screen, the
  waiting-for-phone screen and the home screen. On the phone it reads
  `PhoneNavigator`, which starts on the race list and needs nothing
  else.

- `app-wear` does not declare `androidx.activity:activity-compose` in
  its build file, so no `ComponentActivity` can be written there. It is
  already in the version catalogue and already used by `app-phone`.

- Nothing the application stores survives being closed.
  `RaceRepositoryImpl` and `ProfileRepositoryImpl` hold everything in
  memory: a race in progress does not survive a restart, an imported
  race disappears, the profile's correction factor is lost. Both need a
  Room-backed implementation in `:core-data` — entities, DAOs, a
  database, and the exported schema the conventions require. Room is in
  no build file and in no version catalogue entry.

- Nothing constructs the ViewModels. Every one of them takes its
  dependencies as plain constructor parameters, and no factory, no
  container and no graph exists to build them. The conventions name
  Hilt, which is in no build file and in no version catalogue entry.

- `SensorPermissionSystem` has no implementation. It reads and requests
  the body-sensors permission from the OS; the Android SDK covers it.

- `SensorPermissionLaunchStore` and `ConnectivityPermissionLaunchStore`
  have no implementation. Each persists a one-time first-launch flag;
  SharedPreferences covers both.

- `ConnectivityPermissionSystem` has no implementation, and which OS
  permission it stands for has never been decided. It reports whether
  the app may reach the paired device, whether the system will still
  show a prompt, requests it, and opens the app's settings page. The
  choice of permission is part of this fix.

- `ExerciseSessionSystem` has no implementation. It opens one exercise
  session for a whole race, checks which data types the device offers,
  delivers heart rate and distance while the race runs, and closes at
  the end. It needs the Health Services SDK, absent from the version
  catalogue.

- `HrHistoryReader` has no implementation. It reads the heart-rate
  values recorded over the last twelve months, from which the maximum
  is derived. It needs the Health Connect client, absent from the
  version catalogue.

- `ProfileSyncTransport` and `RecordedRaceTransport` have no
  implementation, and nothing feeds `LinkStateMonitor`'s flow. They
  carry the profile and reference down to the watch, carry recorded
  races up to the phone in chunks, and report when the link between the
  two devices becomes established. All three belong in `:core-sync` and
  need the Wearable Data Layer, which is in the version catalogue and
  declared by `app-wear` but not by `app-phone`.

- `WatchHistoryStore` has no implementation. It holds the summarised
  history the watch receives on each push, replaced as a whole block,
  and it must survive process death — so it goes with the Room work.

- `app-wear` is built with mobile Compose. Its build file depends on
  `androidx.compose.material3`, no `androidx.wear.compose.*` import
  exists anywhere, and no Wear Compose entry exists in the version
  catalogue. The watch screens use phone components — scaffolds, lists
  and scrolling behave wrong on a round screen.

- No class named `*ViewModel` extends `androidx.lifecycle.ViewModel`.
  They are plain Kotlin classes carrying the name, with no lifecycle,
  no `viewModelScope`, and no survival across a configuration change.
  A race in progress would lose its state on rotation or on the watch
  waking.

- No user-facing string lives in the resource files. Both `strings.xml`
  hold only `app_name`; every text sits in `const val` inside
  `PhoneStringResources` and `WatchStringResources`, and interpolated
  values are built with Kotlin string templates rather than resource
  parameters.

- `Segment.cumulativeMs` is a stored field, computed once when segments
  are built and never recomputed. A cumulative value is derived on
  read, never stored — a stored one can disagree with the sum of its
  parts.

- `app-phone/src/androidTest/.../ExampleInstrumentedTest.kt` is the
  Android Studio template's, and nothing in the task graph runs it.
