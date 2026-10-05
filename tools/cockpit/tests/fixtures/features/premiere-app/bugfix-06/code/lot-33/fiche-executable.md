## Signatures

WaitingForPhoneViewModel(
  profileRepository: ProfileRepository,
  navigator: WatchRaceNavigator
) : ViewModel
  — `@HiltViewModel`, `@Inject constructor`; the platform builds it, so
    it stays a `ViewModel` Hilt can construct. What changes: the
    constructor gains `navigator`, injected the same way
    SensorPermissionViewModel already takes it. `init` keeps collecting
    `profileRepository.observe()` on `viewModelScope` and, on every
    emitted Profile whose `lastSyncSuccessAt` is non-null, calls
    `navigator.onProfileSynced()` instead of writing a UI-state field.
    Nothing else calls it; a Profile whose `lastSyncSuccessAt` is null
    calls nothing.

WaitingForPhoneViewModel.uiState: StateFlow<WaitingForPhoneUiState>
  — one value, fixed at construction: the three label references. It
    never changes afterwards, whatever the profile carries.

WaitingForPhoneUiState(
  title: LabelRef, explanation: LabelRef, retryLabel: LabelRef
)
  — what changes: `hasReceivedProfile: Boolean` is dropped, and with it
    the `copy(hasReceivedProfile = true)` write in the ViewModel. The
    three remaining fields keep their current values, none null.

WaitingForPhoneScreen(
  viewModel: WaitingForPhoneViewModel, onRetryClicked: () -> Unit
)
  — public composable, signature and rendering unchanged: it reads
    `title`, `explanation` and `retryLabel` and never read the dropped
    field even before this lot. Its `MainActivity` (`:app-wear`) call site is unchanged, Hilt
    supplying the new constructor argument.

WaitingForPhoneScreenTest (`:app-wear`) — same-module call site of the
  changed constructor, this lot's own scope under R74: it constructs
  `WaitingForPhoneViewModel(FakeWaitingProfileRepository())` twice and
  must pass a navigator too. It is not named in the lot's Modifies list;
  R74 assigns it here.

## Acceptance criteria

- With WatchRaceNavigator.current at WAITING_FOR_PHONE, a Profile
  carrying a non-null lastSyncSuccessAt moves current to HOME
- With WatchRaceNavigator.current at WAITING_FOR_PHONE, a Profile whose
  lastSyncSuccessAt is null leaves current at WAITING_FOR_PHONE
- Once current has reached HOME this way, a later Profile whose
  lastSyncSuccessAt is null leaves current at HOME
- With WatchRaceNavigator.current at SENSOR_PERMISSION, a Profile
  carrying a non-null lastSyncSuccessAt leaves current at
  SENSOR_PERMISSION
- The value WaitingForPhoneUiState carries is equal before and after a
  Profile with a non-null lastSyncSuccessAt is emitted
- WaitingForPhoneScreen renders the waiting title, the explanation and
  the retry label whatever the profile carries

## Dependencies

ProfileRepository — pre-existing; `observe(): Flow<Profile>`, non-suspend,
  emitting a non-null Profile whose `lastSyncSuccessAt: Instant?` is null
  until a sync has ever succeeded
WatchRaceNavigator — created this cycle by lot-34;
  `onProfileSynced()` moves `current` from WAITING_FOR_PHONE to HOME and
  is a no-op on every other destination. Reused, never redeclared
WatchDestination, LabelRef, WatchStringResources.Waiting — pre-existing
SavedStateHandle — not used here; §12.2 does not name this ViewModel

## Conventions

R4 · `./gradlew check` exits 0
R12 · a §4/§9 watch screen is realised in `:app-wear`
R39 · no mutable global state; a dependency is passed as an argument
R42 · cooperative async on coroutines, no shared mutable state
R47 · a screen reads a source once per entry, never in a composition body
R55 · one nominal and one failure test per public function, same lot
R56 · no test reaching the clock, the data layer or real I/O
R62 · the lexicon — Profile, Sync, LastSyncSuccess
R63 · English identifiers and comments; one guarantee line per exported symbol
R64 · no user-facing string literal in the code
R74 · a same-module call site of a changed signature is this lot's own scope

## Requests

—
