## Symbols

RaceDetailViewModel — modified, now @HiltViewModel, extends androidx.lifecycle.ViewModel, @AssistedInject constructor(@Assisted raceId, raceRepository, navigator), runs in viewModelScope
RaceDetailViewModel.Factory — created, @AssistedFactory, create(raceId) → RaceDetailViewModel
RaceListViewModel — modified, now @HiltViewModel, extends androidx.lifecycle.ViewModel, @Inject constructor(raceRepository, navigator), runs in viewModelScope
ProfileViewModel — modified, now @HiltViewModel, extends androidx.lifecycle.ViewModel, @Inject constructor(profileRepository, profileSyncPushService, connectivityPermissionManager, hrHistoryReader, linkStateMonitor, clock), runs in viewModelScope
ImportPreviewViewModel — modified, now @HiltViewModel, extends androidx.lifecycle.ViewModel, @AssistedInject constructor(@Assisted success, raceRepository, navigator), onSaveClicked now takes (raceName, raceDate)
ImportPreviewViewModel.Factory — created, @AssistedFactory, create(success) → ImportPreviewViewModel
PasteErrorViewModel — modified, now @HiltViewModel, extends androidx.lifecycle.ViewModel, @AssistedInject constructor(@Assisted failure, navigator)
PasteErrorViewModel.Factory — created, @AssistedFactory, create(failure) → PasteErrorViewModel
PasteResultViewModel — modified, now @HiltViewModel, extends androidx.lifecycle.ViewModel, @Inject constructor(navigator, clock)
Clock — created, :core-domain, com.mgilli.core.domain.timing, now(): Instant
SystemClock — created, :core-domain, com.mgilli.core.domain.timing, implements Clock, @Inject constructor()

## Build

analyze: clean (:core-domain:check, :app-phone:check — lint passes on both)
test: :core-domain:check 122 passed · :app-phone:check 159 passed

## State

Added: Clock, SystemClock (both under CURRENT_TECHNICAL_STATE.md's Timing domain)
Removed: —

## Convention

Three mechanical additions, none altering the signatures the sheet gave:

- `:core-domain` carries no `javax.inject` dependency yet the sheet asks
  for `@Inject constructor()` on `SystemClock`. Added `javax.inject:javax.inject:1`
  to the version catalogue and to `core-domain/build.gradle.kts` —
  a plain JSR-330 artifact, no Android dependency, so §3 stands.
- This project's pinned Hilt (2.60.1) rejects a bare `@HiltViewModel` on
  an `@AssistedInject` class — `kspDebugKotlin` fails with "must have a
  valid assisted factory specified". `RaceDetailViewModel`,
  `ImportPreviewViewModel` and `PasteErrorViewModel` carry
  `@HiltViewModel(assistedFactory = <Self>.Factory::class)` instead.
- `PasteResultViewModel`'s sheet text names `LocalDate.ofInstant`, which
  needs API 34 and fails lint under this project's minSdk 30 (§2). Used
  `clock.now().atZone(zone).toLocalDate()`, the exact same value.

`ImportPreviewScreen.kt` (not in this lot's Modifies list) gained two
parameters, `raceName: String, raceDate: LocalDate`, forwarded to
`onSaveClicked` — its one call site broke once that method stopped
being no-arg, and the composable itself has no caller anywhere in
`:app-phone` yet (no `NavHost` exists), so this is a mechanical,
non-behavioural fix to keep `:app-phone:check` green, not new wiring.
