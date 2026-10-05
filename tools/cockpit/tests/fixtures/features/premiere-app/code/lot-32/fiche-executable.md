## Signatures

    data class WaitingForPhoneUiState(
        val title: String,
        val explanation: String,
        val retryLabel: String,
        val hasReceivedProfile: Boolean
    )

    class WaitingForPhoneViewModel(
        profileRepository: ProfileRepository
    ) {

        val uiState: StateFlow<WaitingForPhoneUiState>
    }

    @Composable
    fun WaitingForPhoneScreen(
        viewModel: WaitingForPhoneViewModel,
        onRetryClicked: () -> Unit
    )

## Acceptance criteria

- `uiState.title` equals `WatchStringResources.Waiting.title`
- `uiState.explanation` equals `WatchStringResources.Waiting.explanation`
- `uiState.retryLabel` equals `WatchStringResources.Waiting.retry`
- `uiState.hasReceivedProfile` is false while `ProfileRepository.observe()`'s emitted `Profile.lastSyncSuccessAt` is null
- `uiState.hasReceivedProfile` becomes true once `ProfileRepository.observe()` emits a `Profile` whose `lastSyncSuccessAt` is non-null
- `uiState.hasReceivedProfile` stays true on every later emission — `lastSyncSuccessAt`, once set, is never cleared

## Dependencies

Profile — pre-existing (lot-05)
ProfileRepository — pre-existing, extended by lot-21 (`markSyncSuccess`) and lot-36 (`observe`)
DesignTokens — pre-existing (lot-02)
WatchStringResources — pre-existing (lot-44), `Waiting.title`/`explanation`/`retry` already defined
