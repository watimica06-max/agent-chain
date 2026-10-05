## Signatures

    Race.sentAt: Instant?

    RaceRecordingRepository.markSent(raceId: Long, at: Instant) → Result<Race>

`markSent` sets `sentAt = at` on the race held under `raceId`, leaving every
other field of that race unchanged, and never removes it from
`observeRecorded()`. Fails, leaving the stored race unchanged, when
`raceId` carries no stored race — same not-found contract as
`markSegment`/`undoLastMark`/`stopRace`.

`RaceRecordingRepositoryImpl` implements `markSent` the same way it
implements its other mutating members: under its existing lock, replacing
the stored race, then republishing `observeRecorded()` — whose filter
already only excludes a race carrying a non-null `currentSegmentIndex`,
so a race marked sent keeps being emitted.

## Acceptance criteria

- Marking sent a race the repository holds sets its `sentAt` to the given instant and leaves every other field of that race unchanged
- A race marked sent is still returned by `observeRecorded()`, in the same order as before, until `eraseRecorded` removes it
- Marking sent an id the repository does not hold returns a failure, leaving `observeRecorded()`'s content unchanged
- A race that has never been marked sent carries a null `sentAt`

## Dependencies

Race — pre-existing, gains `sentAt`
RaceRecordingRepository — pre-existing interface, gains `markSent`
RaceRecordingRepositoryImpl — pre-existing implementer, implements `markSent`

## Conventions

§3 · `:core-domain` never imports Android — `Race`/`RaceRecordingRepository` stay JVM-pure
§13 · a repository returns a result type, never null on failure
§7 · `sentAt` is a wall-clock instant recorded for bookkeeping, not a monotonic value feeding any duration computation
