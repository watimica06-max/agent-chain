## Symbols

PayloadCodec.encode(ProfileSyncPayload): ByteArray — modified, now suspend
PayloadCodec.encode(RecordedRacePayload): ByteArray — modified, now suspend
PayloadCodec.decodeProfileSync(bytes): ProfileSyncPayload — modified, now suspend, raises PayloadDecodingFailure on a type mismatch
PayloadCodec.decodeRecordedRace(bytes): RecordedRacePayload — modified, now suspend, raises PayloadDecodingFailure on a type mismatch
SegmentSnapshot, RetainedFactorSnapshot, RejectedCalibrationSnapshot, RaceSnapshot, ProfileSnapshot, RaceHistoryEntrySnapshot, ProfileSyncPayloadSnapshot, RecordedRacePayloadSnapshot (private, PayloadCodec.kt) — modified, each fixes its own serialVersionUID
SegmentSnapshot.toSegment() (private extension, PayloadCodec.kt) — modified, a decoded negative durationMs becomes null
toObject (private extension, PayloadCodec.kt) — modified, catches the type-mismatch ClassCastException and raises PayloadDecodingFailure with it as cause
PayloadCodecTest (:core-sync) — modified, its three existing calls move inside runTest; new tests added for every other criterion, including a failure test for encode(ProfileSyncPayload) and a reflection-based test observing that encode/decodeProfileSync/decodeRecordedRace compile only as suspend functions
PayloadCodecCrossModuleTest (:app-phone) — modified, its two calls move inside runTest
PayloadCodecCrossModuleTest (:app-wear) — modified, its two calls move inside runTest
RecordedRaceListenerServiceTest (:app-phone) — modified, buildRecordedRaceEvent reaches encode through runBlocking; no assertion, fixture or test changed
ProfileSyncListenerServiceTest (:app-wear) — modified, buildProfileSyncEvent reaches encode through runBlocking; no assertion, fixture or test changed

## Build

analyze+test (`:core-sync:check`): clean — 48 tests passed
analyze+test (`:app-phone:check`): clean
analyze+test (`:app-wear:check`): clean

## State

Added: PayloadCodec's entry now states its four functions are suspend and dispatch to Dispatchers.IO internally, that each snapshot class fixes its own serialVersionUID, and its exact decode-failure contract (PayloadDecodingFailure on a type mismatch only, cause set; any other deserialisation failure unchanged; negative durationMs decodes to null)
Added: a trap on a custom exception thrown across a withContext dispatcher switch arriving at a JVM test as a stack-trace-recovery-wrapped copy
Removed: PayloadCodec's prior undifferentiated "a decode failure propagates" description, superseded by the entry above

## Requests

—
