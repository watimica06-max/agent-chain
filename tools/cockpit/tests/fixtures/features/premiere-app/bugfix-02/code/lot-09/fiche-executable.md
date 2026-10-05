## Signatures

    // :core-sync
    class WearableProfileSyncTransport(context: Context) : ProfileSyncTransport {
      override suspend fun send(payload: ProfileSyncPayload): Boolean
      // Delivers payload to the paired device over the Wearable Data Layer.
      // True once delivery succeeds; false on any delivery failure — never
      // throws.
    }

    class WearableRecordedRaceTransport(context: Context) : RecordedRaceTransport {
      override suspend fun send(payload: RecordedRacePayload): Boolean
      // Delivers payload to the phone over the Wearable Data Layer.
      // True once delivery succeeds; false on any delivery failure — never
      // throws.
    }

    class WearableLinkStateSource(context: Context) {
      fun observeNodeConnected(): Flow<Boolean>
      // The paired node's connection state, built on the Wearable Data
      // Layer's node-connection signal: the current state on subscription,
      // then again on every change. Wired into LinkStateMonitor's
      // rawLinkEstablished parameter.
    }

## Acceptance criteria

- `WearableProfileSyncTransport.send` returns true once the payload is delivered to the paired device
- `WearableProfileSyncTransport.send` returns false, without throwing, when delivery fails
- `WearableRecordedRaceTransport.send` returns true once the payload is delivered to the phone
- `WearableRecordedRaceTransport.send` returns false, without throwing, when delivery fails
- `WearableLinkStateSource.observeNodeConnected()` emits false on subscription when no node is connected
- `WearableLinkStateSource.observeNodeConnected()` emits true on subscription when the paired node is already connected
- `WearableLinkStateSource.observeNodeConnected()` emits true when the paired node connects after subscription
- `WearableLinkStateSource.observeNodeConnected()` emits false when the paired node disconnects after subscription

## Dependencies

ProfileSyncTransport — pre-existing, interface unchanged
RecordedRaceTransport — pre-existing, interface unchanged
LinkStateMonitor — pre-existing, constructor unchanged (`rawLinkEstablished: Flow<Boolean>`)
ProfileSyncPayload — pre-existing, unchanged
RecordedRacePayload — pre-existing, unchanged
play-services-wearable (`com.google.android.gms:play-services-wearable`) — added by this lot to `core-sync/build.gradle.kts`; already declared in the version catalogue and in `app-wear/build.gradle.kts`

## Conventions

§3 · a platform adapter for the Data Layer lives in `:core-sync`
§9 · a flow is named for what it carries, no `Flow` suffix
§13 · never swallow an exception silently — a delivery failure surfaces as `false`, not a swallowed `catch`
§14 · sync code is tested against fakes, never against real hardware in CI
