## Symbols

DataLayerCapabilitySource — modified, now internal constructor takes `CapabilityClient` and `NodeClient` directly; the public `Context` constructor forwards to it via `Wearable.getCapabilityClient`/`getNodeClient`
DataLayerCapabilitySource.localNodeId() — modified, awaits `addLocalCapability(CAPABILITY_NAME)`'s `Task` first, then `nodeClient.localNode`'s `Task`
WearableLinkStateSource — modified, class doc comment only

## Build

analyze: clean (`./gradlew :core-sync:check` — lint, no ktlint/detekt task wired into this module's `check` at this time)
test: 7 passed (`./gradlew :core-sync:testDebugUnitTest`)

## State

Added: —
Removed: core-sync/src/test/kotlin/com/mgilli/core/sync/link/TaskAwaitExperimentTest.kt — untracked leftover from a prior investigation, held only a package declaration, unreferenced anywhere
Rewritten: WearableLinkStateSource — registration-not-guaranteed note, CapabilityClient/NodeClient constructor seam

## Requests

—
