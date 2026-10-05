## Symbols

HealthHistoryAvailability — created
PhoneStringResources.Profile.hrHistoryUnavailable — created
ProfileUiState — modified, drops distanceLabel and pressDurationLabel, adds isHealthHistoryUnavailable
ProfileViewModel — modified, appends healthHistoryAvailability and savedStateHandle to the constructor, moves the four setting handlers into viewModelScope.launch, gates the hrMax-derivation launch on HealthHistoryAvailability.isAvailable(), persists the four rejection flags through savedStateHandle
ProfileScreen — modified, moves hrMaxEditValue/fieldValue/distanceFieldValue/longPressFieldValue from remember to rememberSaveable, renders hrHistoryUnavailable in the heart-rate section
ProfileViewModelTest — modified, adapted to ProfileRepository/WatchHistoryStore's current suspend interface and ProfileSyncPushService's current RaceRecordingRepository parameter, one test per acceptance criterion
ProfileScreenTest — modified, same adaptation, plus the rotation and heart-rate-history-unavailable tests
HealthHistoryAvailabilityTest — created
PhoneStringResourcesTest — modified, asserts the new hrHistoryUnavailable key

## Build

analyze: clean
test: 225 passed, 16 failed. Every failure is pre-existing and outside this lot — ImportPreviewViewModelTest, PasteErrorViewModelTest, PasteResultViewModelTest, MainActivityTest, none of which this lot's diff touches. Every ProfileViewModelTest, ProfileScreenTest, PhoneStringResourcesTest and HealthHistoryAvailabilityTest test passes.

## State

Added: HealthHistoryAvailability
Removed: —

## Requests

—
