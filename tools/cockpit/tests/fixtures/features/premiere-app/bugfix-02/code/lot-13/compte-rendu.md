## Symbols

HomeViewModel — modified, now `@HiltViewModel`/`@Inject constructor(...)`, extends `ViewModel`, runs on `viewModelScope`; `clock: Clock` replaces `now: () -> Instant`
ControlViewModel — modified, now `@HiltViewModel(assistedFactory = Factory::class)`/`@AssistedInject constructor(...)`, extends `ViewModel`
ControlViewModel.Factory — created, `@AssistedFactory`, `create(initialRace: Race): ControlViewModel`
EndOfRaceViewModel — modified, now `@HiltViewModel(assistedFactory = Factory::class)`/`@AssistedInject constructor(...)`, extends `ViewModel`
EndOfRaceViewModel.Factory — created, `@AssistedFactory`, `create(finalRace: Race, referenceRace: Race?): EndOfRaceViewModel`
PreparationViewModel — modified, now `@HiltViewModel`/`@Inject constructor(...)`, extends `ViewModel`, runs on `viewModelScope`
WatchHistoryViewModel — modified, now `@HiltViewModel`/`@Inject constructor(...)`, extends `ViewModel`, runs on `viewModelScope`
ProjectionViewModel — modified, now `@HiltViewModel(assistedFactory = Factory::class)`/`@AssistedInject constructor(...)`, extends `ViewModel`
ProjectionViewModel.Factory — created, `@AssistedFactory`, `create(initialRace: Race, referenceRace: Race?, profile: Profile): ProjectionViewModel`
WaitingForPhoneViewModel — modified, now `@HiltViewModel`/`@Inject constructor(...)`, extends `ViewModel`, runs on `viewModelScope`
MainRacePageViewModel — modified, now `@HiltViewModel(assistedFactory = Factory::class)`/`@AssistedInject constructor(...)`, extends `ViewModel`
MainRacePageViewModel.Factory — created, `@AssistedFactory`, `create(initialRace: Race, referenceRace: Race?, profile: Profile, sensorPermissionGranted: Boolean): MainRacePageViewModel`
SensorPermissionViewModel — modified, now `@HiltViewModel`/`@Inject constructor(...)`, extends `ViewModel`, runs on `viewModelScope`

## Build

analyze: clean (`./gradlew :app-wear:check`, includes lint)
test: 266 passed

## State

Added: the general trap on `@AssistedInject` constructors with two same-base-type `@Assisted` params (KSP "duplicate @Assisted type"); the dead-state note on `:app-wear`'s Hilt graph having no entry point yet
Removed: — (the `viewModelScope`-needs-a-stubbed-Main-dispatcher trap's class list is extended, not replaced)

## Convention

—
