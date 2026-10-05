## Signatures

HyroxTypeConverters.toRaceOrigin(value: String): RaceOrigin
  — unchanged signature; never throws; returns RaceOrigin.valueOf(value)
    when value decodes, and the same fixed RaceOrigin member on every
    call where it does not

HyroxTypeConverters.toRaceCompletion(value: String): RaceCompletion
  — unchanged signature; never throws; returns RaceCompletion.valueOf(value)
    when value decodes, and the same fixed RaceCompletion member on every
    call where it does not

HyroxTypeConverters.toZoneThresholds(value: String): List<Int>
  — unchanged signature; never throws; returns emptyList() both when
    value is empty (existing behaviour) and when any comma-separated
    segment fails to parse as Int (new behaviour)

RaceDatabaseMigrations.MIGRATION_2_3: Migration
  — Migration(2, 3); adds a unique index on races.sourceRaceId
    (CREATE UNIQUE INDEX); the already-committed MIGRATION_1_2 stays
    untouched

RaceEntity
  — gains a unique index on sourceRaceId (@Entity's indices =
    [Index(value = ["sourceRaceId"], unique = true)]); every other
    field unchanged

HyroxDatabase
  — version bumped from 2 to 3; same entities and type converters

RepositoryModule.provideHyroxDatabase(context: Context): HyroxDatabase (:app-phone, :app-wear)
  — unchanged signature; the builder adds MIGRATION_2_3 alongside the
    existing MIGRATION_1_2 and declares fallbackToDestructiveMigration(),
    so a schema whose stored version matches no declared migration path
    opens fresh instead of raising unrecovered at the first query

## Acceptance criteria

- toRaceOrigin("RECORDED") returns RaceOrigin.RECORDED; toRaceOrigin("not-a-value") does not throw and returns a RaceOrigin
- toRaceCompletion("COMPLETE") returns RaceCompletion.COMPLETE; toRaceCompletion("not-a-value") does not throw and returns a RaceCompletion
- toZoneThresholds("80,150,175,190") returns [80, 150, 175, 190]; toZoneThresholds("") returns emptyList(); toZoneThresholds("80,x,175") does not throw and returns emptyList()
- Two RaceEntity rows sharing the same non-null sourceRaceId cannot both be inserted once MIGRATION_2_3 has run — the second insert fails on the unique index
- A RaceEntity row with sourceRaceId = null inserts without conflict alongside another row also carrying sourceRaceId = null
- provideHyroxDatabase, opened against a database file whose stored version has no migration path declared from it, does not raise — the app reaches a queryable database instead of crashing at the first query

## Dependencies

RaceOrigin, RaceCompletion, Room, RaceEntity, HyroxDatabase, RaceDatabaseMigrations.MIGRATION_1_2 — pre-existing

## Conventions

R8 · no committed migration is modified; a structural schema change adds a new one
R9 · the exported schema JSON is a tool's own output, never hand-written by the lot
R16 · a field the code treats as identifying (sourceRaceId) carries a uniqueness constraint

## Requests

—
