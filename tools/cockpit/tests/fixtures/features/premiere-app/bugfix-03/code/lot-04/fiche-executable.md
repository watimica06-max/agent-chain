## Signatures

    RaceRepository.saveRecordedRace(
      raceId: Long, name: String, date: Instant, segments: List<Segment>, completion: RaceCompletion
    ) → Result<Race>

`raceId` is the identifier the source (watch) race carries —
`RecordedRacePayload`'s own `raceId` (lot-05) — used only to detect a
resend of a race already saved under that identifier. It is never the
returned `Race`'s own stored id, which `RaceRepositoryImpl` still assigns
itself on first save.

On a `raceId` never saved before, `saveRecordedRace` behaves as today:
creates a new race and returns it. On a `raceId` already saved, it
returns the previously saved race unchanged, without creating a second
row.

## Acceptance criteria

- Saving a recorded race under a `raceId` never saved before creates a new race, visible afterwards through `observeAll()`
- Saving a recorded race under a `raceId` already saved returns the previously saved race, unchanged, without adding a second entry to `observeAll()`
- The race returned on a resend carries the same stored id as the one returned on the original save

## Dependencies

RaceRepository — pre-existing interface, `saveRecordedRace` gains `raceId`
RaceRepositoryImpl — pre-existing implementer, gains the idempotency check

## Conventions

§8 · Room schemas are exported and versioned; every schema change ships with a migration, destructive fallback prohibited
§13 · a repository returns a result type, never null on failure
§3 · a platform adapter (Room) lives in the module carrying its technology — the idempotency check's storage stays in `:core-data`
