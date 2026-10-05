## Signatures

PayloadCodec (:core-sync, `object`) — modified

  suspend fun encode(payload: ProfileSyncPayload): ByteArray
  suspend fun encode(payload: RecordedRacePayload): ByteArray
    — `suspend` is the only change to the type: same parameter, same
      return. The snapshot mapping and the serialization both run on
      Dispatchers.IO from inside the function itself, never on the
      caller's thread. Never null, never empty. A failure raised while
      mapping or serializing still propagates uncaught, unchanged — the
      two transports rely on that to tell an encoding failure from a
      delivery failure. A CancellationException is rethrown, never
      converted.

  suspend fun decodeProfileSync(bytes: ByteArray): ProfileSyncPayload
  suspend fun decodeRecordedRace(bytes: ByteArray): RecordedRacePayload
    — `suspend` is the only change to the type: same parameter, same
      return type. Both stay non-null and non-Result. The
      deserialization and the snapshot-to-domain mapping both run on
      Dispatchers.IO from inside the function itself. Raises
      PayloadDecodingFailure when the deserialised object is not of the
      expected snapshot type, carrying the original failure as its
      `cause`; a ClassCastException never leaves either function. A byte
      array java.io cannot read as a serialization stream raises the same
      java.io failure it raises today — unchanged by this lot, and
      converted by each listener service's own catch as it already is. A
      CancellationException is rethrown, never converted.

Private declarations inside PayloadCodec.kt — modified

  the eight Serializable snapshot classes — SegmentSnapshot,
  RetainedFactorSnapshot, RejectedCalibrationSnapshot, RaceSnapshot,
  ProfileSnapshot, RaceHistoryEntrySnapshot, ProfileSyncPayloadSnapshot,
  RecordedRacePayloadSnapshot — each fixes its own serialVersionUID
  instead of letting the JVM derive one from its structure. The platform
  mechanism is the static field Java serialization reads: in Kotlin, a
  `companion object` holding `private const val serialVersionUID: Long`.
  All eight, including the six reachable only through another snapshot.

  SegmentSnapshot.toSegment(): Segment
    — a decoded durationMs below zero becomes `durationMs = null`, the
      same outcome buildSegments already gives a negative entry; zero
      stays zero, null stays null. Every other field maps through
      unchanged. This is the one place a decode is not a round trip.

  toObject — raises PayloadDecodingFailure on a type mismatch, as above.

Call sites this lot adapts to the signatures above, changing nothing else
about them

  PayloadCodecTest (:core-sync) — its three calls move inside a
  coroutine; same subjects, same assertions plus the new ones below.

  PayloadCodecCrossModuleTest (:app-phone),
  PayloadCodecCrossModuleTest (:app-wear) — the encode/decode pair in
  each of the two test bodies moves inside a coroutine. Their subject is
  PayloadCodec, so R86 puts them in this lot; the module is entered for
  nothing else, so R85 leaves that module's own check outside this lot.

  RecordedRaceListenerServiceTest (:app-phone) —
  `buildRecordedRaceEvent` reaches a suspend encode, and nothing else
  changes: no assertion, no fixture, no test added or removed. Its
  subject is RecordedRaceListenerService, whose owner stays lot-31.

  ProfileSyncListenerServiceTest (:app-wear) — `buildProfileSyncEvent`
  reaches a suspend encode, on the same terms; its owner stays lot-16.

Not touched by this lot

  RecordedRaceListenerService (:app-phone) and ProfileSyncListenerService
  (:app-wear) — their decode call already sits inside their own
  serviceScope.launch, so a suspend decode compiles there unchanged.

  WearableProfileSyncTransport and WearableRecordedRaceTransport
  (:core-sync) — their encode call already sits in a suspend `send`.

  PayloadDecodingFailure.kt (:core-sync) — used as delivered.

## Acceptance criteria

- A non-suspend function body calling encode, decodeProfileSync or decodeRecordedRace does not compile
- encode(ProfileSyncPayload) given a history list that records the thread its iteration runs on records a thread other than the one the call was made from
- decodeProfileSync given bytes whose deserialisation records the thread it runs on records a thread other than the one the call was made from
- decodeRecordedRace given bytes whose deserialisation records the thread it runs on records a thread other than the one the call was made from
- Reading back the class descriptors of the bytes encode produces, for a ProfileSyncPayload carrying a reference race and for a RecordedRacePayload, each of the eight snapshot classes carries the serialVersionUID value its own declaration fixes
- encode then decodeRecordedRace of a payload carrying two retainedFactors and one rejectedCalibration returns a payload whose two lists are equal to the originals, in the same order
- encode then decodeRecordedRace of a payload whose segment carries durationMs = -5000 returns that segment with durationMs = null, every other field unchanged
- encode then decodeProfileSync of a payload whose reference race carries a segment with durationMs = -5000 returns that segment with durationMs = null
- encode then decodeRecordedRace of a payload whose segment carries durationMs = 0 returns that segment with durationMs = 0
- decodeProfileSync given bytes holding a serialised object of another type raises PayloadDecodingFailure, never a ClassCastException
- decodeRecordedRace given bytes holding a serialised object of another type raises PayloadDecodingFailure, never a ClassCastException
- The PayloadDecodingFailure raised on a type mismatch carries the failure that triggered it as its `cause`
- decodeProfileSync given a byte array that is not a serialisation stream raises the same java.io failure it raises today, not a PayloadDecodingFailure
- encode given a payload whose list throws once iterated lets that exception reach its caller uncaught

## Dependencies

ProfileSyncPayload, RecordedRacePayload, Profile, Race, RaceHistoryEntry, Segment, RetainedFactor, RejectedCalibration, SegmentType, Station, RaceOrigin, RaceCompletion — pre-existing (:core-domain)
RecordedRacePayload's retainedFactors / rejectedCalibrations — lot-53; the matching snapshot fields and both mappings were delivered by lot-12 (its report), so §6.11's codec half is already carried and this lot only keeps it observed
PayloadDecodingFailure — created by lot-52, used as delivered
buildSegments — modified by lot-02 (this cycle); the negative-as-null rule toSegment mirrors
RecordedRaceListenerService — lot-31, coded; its decode call already inside serviceScope.launch
ProfileSyncListenerService — lot-16, coded; its decode call already inside serviceScope.launch
WearableProfileSyncTransport, WearableRecordedRaceTransport — lot-12, coded; their encode calls already inside a suspend send
kotlinx.coroutines, kotlinx-coroutines-test — pre-existing on :core-sync, :app-phone and :app-wear

## Conventions

R4 · a lot is deliverable only when the check exits 0
R85 · a module entered only to adapt an existing test's direct call sites does not bind the lot to the rest of that module's check
R86 · a test file's owner is the lot whose scope covers the subject it exercises
R19 · every public operation that can block is suspend
R24 · an operation reaching outside the process moves to the thread that work belongs on inside its own implementation, never on its caller's word
R31 · an error crossing a module boundary is of a type that module declares
R33 · governs the two listener services' own Result, not the codec's return — settled by this lot's applied Decision
R30 · no empty and no generic catch
R20 · missing data crosses a public boundary as a nullable; no invented default
R26 · no `!!` on a value coming from outside the function
R40 · every acquired resource released in the same scope, through `use`
R55 · one nominal and one failure test per public function, in this lot
R63 · English; every exported symbol carries one line saying what it guarantees and when it fails
R66 · no new dependency inside a lot
R2 · a technical decision the conventions do not cover is proposed as an amendment in the lot report

## Requests

architecte/detailleur-lot-11.md — its Verdict is still empty; the Arbitre's Decision settles this lot's signature, the conventions amendment stands
