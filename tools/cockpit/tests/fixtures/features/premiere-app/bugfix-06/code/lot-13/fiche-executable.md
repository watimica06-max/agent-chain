## Signatures

DataLayerCapabilitySource (internal class, :core-sync, com.mgilli.core.sync.link)
  — `init` no longer calls `capabilityClient.addLocalCapability(CAPABILITY_NAME)`;
    that call moves inside `localNodeId()`, awaited before the existing
    `nodeClient.localNode` await

DataLayerCapabilitySource.localNodeId(): String — suspend, signature unchanged
  — awaits `capabilityClient.addLocalCapability(CAPABILITY_NAME)`'s `Task`
    first, then `nodeClient.localNode`'s `Task`, returning its `id`; a
    failure of either `Task` propagates as a thrown exception, the same
    way `reachableNodeIds()` already lets its own `Task` failure propagate

WearableLinkStateSource.observeNodeConnected(): Flow<Boolean> — code unchanged
  — its class doc comment is updated: capability registration is no
    longer guaranteed by the time the constructor returns; a registration
    failure now surfaces as a failure of the `Flow` this function returns,
    raised the first time it is collected, instead of throwing at
    `DataLayerCapabilitySource` construction

## Acceptance criteria

- Constructing `DataLayerCapabilitySource` with a `CapabilityClient` whose
  `addLocalCapability` call would fail does not throw at construction time
- Calling `localNodeId()` when `addLocalCapability`'s `Task` fails throws
  that failure, surfacing through `observeNodeConnected()`'s `Flow` when
  it is collected, rather than being silently unread
- Calling `localNodeId()` awaits `addLocalCapability`'s `Task` to
  completion before reading `nodeClient.localNode` — observable as call
  order against mocked `CapabilityClient`/`NodeClient` instances

## Dependencies

CapabilitySource — pre-existing, interface unchanged
com.google.android.gms.tasks.Task — pre-existing (Play Services Wearable)
WearableLinkStateSource — pre-existing, doc comment only touched by this lot

## Conventions

R19 · every public operation that can block is suspend, and cancellable by its caller's coroutine
R24 · an operation reaching outside the process says so by being suspend; it moves to the right thread inside its own implementation, never on the caller's word
R63 · every exported symbol's doc line says what it guarantees and when it fails

## Requests

—
