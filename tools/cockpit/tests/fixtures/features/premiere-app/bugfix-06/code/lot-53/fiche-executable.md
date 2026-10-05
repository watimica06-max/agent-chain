## Signatures

RecordedRacePayload(
  raceId: Long, name: String, date: Instant, segments: List<Segment>,
  completion: RaceCompletion, retainedFactors: List<RetainedFactor>,
  rejectedCalibrations: List<RejectedCalibration>
)
  — two fields added, same name and shape as Race's own retainedFactors/
    rejectedCalibrations; no default value — every construction site
    supplies them explicitly

## Acceptance criteria

- Constructing a RecordedRacePayload with a given retainedFactors and rejectedCalibrations exposes those exact lists unchanged through the corresponding properties
- A RecordedRacePayload built with empty retainedFactors and rejectedCalibrations lists exposes them as empty, not null

## Dependencies

RetainedFactor, RejectedCalibration, Segment, RaceCompletion — pre-existing

RecordedRacePayload's constructor is also called by two sites this lot
does not touch, both broken by the two new required fields until their
own lot runs:
- PayloadCodec.kt's RecordedRacePayloadSnapshot.toPayload (:core-sync) — adapted by lot-11
- RecordedRaceSyncService.sync (core-domain/src/main/kotlin/com/mgilli/core/domain/sync/RecordedRaceSyncService.kt:39, same module as RecordedRacePayload) — adapted by lot-15

The PayloadCodec case is a different module and fits R72/R73 as
precedent (detailleur-lot-03.md) already establishes. The
RecordedRaceSyncService case sits in the same :core-domain module as
RecordedRacePayload itself, so `./gradlew :core-domain:check` cannot
compile at all until lot-15 runs — see architecte/detailleur-lot-53.md.

## Conventions

R18 · data crossing a public boundary is immutable
R72 · a lot passing its own module's check is deliverable while a call site another lot's sheet adapts still fails, project-wide
R73 · that lot's report names the failing call site and the lot that adapts it

## Requests

architecte/detailleur-lot-53.md
