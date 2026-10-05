## Symbols

HyroxTypeConverters.toRaceOrigin — modified, falls back to `RaceOrigin.entries.first()` instead of throwing
HyroxTypeConverters.toRaceCompletion — modified, falls back to `RaceCompletion.entries.first()` instead of throwing
HyroxTypeConverters.toZoneThresholds — modified, returns emptyList() on an unparsable segment too
RaceDatabaseMigrations.MIGRATION_2_3 — created
RaceEntity — modified, gains a unique index on sourceRaceId
HyroxDatabase — modified, version bumped from 2 to 3
RepositoryModule.provideHyroxDatabase (:app-phone) — modified, adds MIGRATION_2_3 and fallbackToDestructiveMigration()
RepositoryModule.provideHyroxDatabase (:app-wear) — modified, adds MIGRATION_2_3 and fallbackToDestructiveMigration()

## Build

analyze: clean (`:core-data:check`, `:app-wear:check`)
test: `:core-data:check` — 64 passed, 0 failed (including 3 new HyroxTypeConvertersTest
  and 2 new RaceDatabaseMigrationsTest); `:app-wear:check` — 353 passed, 0 failed
  (including the new RepositoryModuleTest)

`:app-phone:check` does not exit 0: `ProfileViewModel.kt` fails to compile at `HEAD`,
before this lot's own change, on two pre-existing defects this lot does not touch —
a non-exhaustive `when` missing the `DateDisplay.Future` branch (owned by lot-17,
whose sheet names this exact gap) and four calls into the now-`suspend`
`ProfileRepository` from outside a coroutine scope (owned by lot-19, per lot-17's
own fiche). `git status` confirms `ProfileViewModel.kt` carries no local
modification. This lot's own file, `RepositoryModule.kt`, raises no error in that
same compile pass — the whole main source set is type-checked in one step, and
its only reported errors are ProfileViewModel.kt's five lines. `RepositoryModuleTest.kt`
(`:app-phone`) cannot be compiled or run while the main source set fails; its content
mirrors the `:app-wear` counterpart, which passes.

## State

Added: RaceDatabaseMigrations.MIGRATION_2_3, HyroxDatabase version 3 with a unique
  index on races.sourceRaceId, HyroxTypeConverters' non-throwing decode fallback
Removed: —

## Requests

—
