## What blocks

§1.4 leaves `stopRace`'s end time as an unsettled either/or, and the
database-backed rewrite §2.6 asks for cannot store `Race.sentAt` — nor a
new end-time field — because `RaceEntity`, `HyroxDatabase` and
`RaceDatabaseMigrations` carry no column for either and lot-50 declares
none of them as modified.

## Where

`code/decoupage.md`, `## lot-50` (`Modifies: RaceRecordingRepository,
RaceRecordingRepositoryImpl, Race, RaceRecordingRepositoryImplTest,
PhoneRaceRecordingRepository`) against `desc-bug.md` §1.4 and §2.6.

Four separate facts, each confirmed by grep:

1. §1.4 states two mutually exclusive outcomes — "Either `stopRace`
   stores `atInstant` on a new `Race` field, or the parameter is dropped
   from the signature and the interface states explicitly that no end
   time is recorded." `decoupage.md`'s `## Symbols` repeats the same
   either/or verbatim ("stopRace reads atInstant, or the parameter is
   dropped §1.4"), so nothing upstream settles it. The two branches give
   two different signatures — `stopRace(raceId, atInstant)` versus
   `stopRace(raceId)` — and two different acceptance criteria.

2. `core-domain/.../race/Race.kt` carries `sentAt: Instant?`;
   `core-data/.../db/RaceEntity.kt` carries no matching column, and a
   grep for `sentAt` across `src/main` finds it read nowhere but the
   in-memory `RaceRecordingRepositoryImpl.markSent`. §2.6 names
   `markSent` among the five methods that "each write the race ... to
   the database before returning", but with no column its write is a
   no-op against the stored row, so §2.6's rule has no observable
   criterion on `markSent`.

3. Adding an end-time column (§1.4, first branch) or a `sentAt` column
   (§2.6) means editing `RaceEntity`, bumping `HyroxDatabase`'s
   `version = 3` and adding a `MIGRATION_3_4` beside `MIGRATION_1_2` and
   `MIGRATION_2_3`. Those three symbols belong to lot-08 and lot-09,
   both already coded and closed — their reports are the only hits for
   `RaceEntity` across `code/**/compte-rendu.md` — and R8 forbids
   modifying a committed migration. Lot-50 declares none of them.

4. `app-wear/.../di/RepositoryModule.kt:81` constructs
   `RaceRecordingRepositoryImpl(profileRepository)`. Reading and writing
   through `RaceDao` needs that dependency injected, which changes
   `RepositoryModule (:app-wear)` — also absent from lot-50's
   `Modifies`.

## To resume

- A decision on §1.4: `stopRace` keeps `atInstant` and `Race` carries a
  persisted end-time field, or `atInstant` is dropped from the signature
  and `RaceRecordingRepository`'s documentation states that no end time
  is recorded.
- A split correction giving lot-50 (or a new lot ordered before it) the
  symbols the persistence needs: `RaceEntity`, `HyroxDatabase`'s version,
  a new `RaceDatabaseMigrations` entry for the added column(s), and
  `RepositoryModule (:app-wear)`.
- Or, if `Race.sentAt` is deliberately not persisted, a statement to that
  effect so §2.6's "write the race before returning" is read as excluding
  `markSent`, and `markSent` keeps a criterion this lot can be held to.

## Decision

Take §1.4's first branch: `stopRace` keeps `atInstant` and stores it on a
new `Race.stoppedAt: Instant? = null`; persist `stoppedAt` and the
existing `Race.sentAt` as two nullable columns, `stoppedAtEpochMs` and
`sentAtEpochMs`, on `RaceEntity`; and write lot-50's sheet against a
split correction adding to its `Modifies:` — `RaceEntity`,
`HyroxDatabase` (version 3 → 4), `RaceDatabaseMigrations` (a new
`MIGRATION_3_4` adding both columns), `RaceDatabaseMigrationsTest`,
`RepositoryModule (:app-wear)` (registers `MIGRATION_3_4` and injects
`RaceDao` into `RaceRecordingRepositoryImpl`) and
`RepositoryModule (:app-phone)` (registers `MIGRATION_3_4`).

R25 settles the either/or: an argument a signature takes is read, and a
value that must outlive the process is written where it does. The chain
feeding `atInstant` already exists — `ControlScreen.kt:98`'s
`Instant.now()` → `ControlViewModel.onStopConfirmed` (:104) →
`StopRaceController.stop` (StopRaceController.kt:28) — and lot-50 is the
last lot of `code/sequence.md` (block-20, alone), so R73 leaves no later
lot to own the call sites dropping the parameter would break. §2.6 names
`markSent` among the five methods that "each write the race … to the
database before returning", which is the corpus's own answer on
`sentAt`. R8 requires a structural change to add a new migration beside
the committed ones, and lot-08 solved the identical problem the same
way (`code/lot-08/compte-rendu.md`: `MIGRATION_2_3` created,
`HyroxDatabase` bumped 2 → 3, both `RepositoryModule.provideHyroxDatabase`
updated). `stoppedAt` takes `Stop` from R62's lexicon;
`stoppedAtEpochMs`/`sentAtEpochMs` follow `RaceEntity.dateEpochMs`.

Nothing reads `Race.stoppedAt`: the race total stays the sum of its
segments, `stopRace` keeps leaving the segment in progress abandoned with
no duration and never truncated to `atInstant`, no screen and no §10 key
carries it, and `RecordedRacePayload` gains neither field — it stays
lot-53's. `MIGRATION_1_2` and `MIGRATION_2_3` are untouched under R8;
`RaceDao` needs no new query, `upsert`/`upsertAndFind` already carrying
the whole row; and the extension to `RepositoryModule (:app-phone)` is
the one `addMigrations` line, nothing else in `:app-phone`.

## Applied

2026-09-06, block-20 — `code/lot-50/fiche-executable.md` written against
this decision.
