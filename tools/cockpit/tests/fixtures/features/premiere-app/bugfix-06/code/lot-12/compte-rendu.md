## Symbols

MessageChannel.send — unchanged signature; doc line updated to state the CancellationException exception
DataLayerMessageChannel.send — modified, rethrows CancellationException first, then logs and returns false
WearableProfileSyncTransport.send — modified, PayloadCodec.encode moved outside the try; rethrows CancellationException; logs and returns false
WearableRecordedRaceTransport.send — modified, PayloadCodec.encode moved outside the try; rethrows CancellationException; logs and returns false
WearableRecordedRaceAckTransport.send — modified, rethrows CancellationException first, then logs and returns false

Out of the sheet's own scope, applying the Product Owner's filled `blocked_realisateur.md` Decision (which governs over the sheet's "PayloadCodec — pre-existing, unmodified"):

RecordedRacePayloadSnapshot (private, PayloadCodec.kt) — modified, now carries retainedFactors: List<RetainedFactorSnapshot> and rejectedCalibrations: List<RejectedCalibrationSnapshot>
RecordedRacePayload.toSnapshot() (private extension, PayloadCodec.kt) — modified, maps retainedFactors/rejectedCalibrations through
RecordedRacePayloadSnapshot.toPayload() (private extension, PayloadCodec.kt) — modified, maps retainedFactors/rejectedCalibrations back

## Build

analyze: no ktlint/detekt task wired into any module's `check` (confirmed by grep across every `*.gradle.kts`); nothing to run beyond `check` itself
test (:core-sync:check): clean — compiles and all tests pass
test (:app-wear:check): clean — compiles and all tests pass

Fixed after FAIL mineur: the four tests named "logs the exception it
catches before returning false" (DataLayerMessageChannel.send,
WearableProfileSyncTransport.send, WearableRecordedRaceTransport.send,
WearableRecordedRaceAckTransport.send — the last one renamed from
"send returns false, without throwing, when MessageChannel send
throws" to match its criterion) each now assert, via Robolectric's
ShadowLog, that a Log.WARN entry carrying the caught exception was
recorded under the class's own tag, alongside the existing return-value
assertion. `core-sync` gained `testImplementation(libs.robolectric)`
(the catalog entry already existed, used elsewhere for the same
purpose per TECHNICAL_CONVENTIONS.md's tool table). Re-run after the
fix:
test (:core-sync:check): clean — compiles and all tests pass
test (:app-wear:check): clean — compiles and all tests pass
test (:app-phone:check): blocked before reaching the test files this lot touched — `:app-phone:compileDebugKotlin` fails on `ProfileViewModel.kt` lines 121, 128, 135 and 143 ("Suspend function ... can only be called from a coroutine or another suspend function"), calling `ProfileRepository.updateHrMaxBpm`/`updateExpectedDistanceM`/`updateLongPressMs`/`updateZoneThreshold` directly from `onHrMaxUpdated`/`onExpectedDistanceChanged`/`onLongPressChanged`/`onZoneThresholdChanged`, none of which open a coroutine. This file is untouched by this lot and unrelated to `RecordedRacePayload`/`PayloadCodec`; it is the leftover call site of some other lot's signature change making those four `ProfileRepository` methods `suspend` (R19). Per R72/R73, this lot stays deliverable — this app-phone-only failure is a call site outside this lot's own touched files — but no lot is named its owner here since the split/sequence are outside what a Réalisateur reads.

## State

Added: a trap on PayloadCodec's private Snapshot classes needing to mirror their domain payload's fields by hand
Removed: the false claim that WearableProfileSyncTransport/WearableRecordedRaceTransport/WearableRecordedRaceAckTransport never throw

## Requests

—
