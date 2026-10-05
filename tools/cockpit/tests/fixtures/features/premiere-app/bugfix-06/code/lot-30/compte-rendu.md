## Symbols

PhoneRaceRecordingRepository — created
RaceRecordingModule (:app-phone) — created

## Build

analyze/test: cannot run. `./gradlew :app-phone:check` (and even
`:app-phone:compileDebugKotlin`, since `:app-phone` depends on
`:core-sync`) fails before reaching `:app-phone` at all —
`PayloadCodec.kt:187` in `:core-sync`, `No value passed for parameter
'retainedFactors'` / `'rejectedCalibrations'`. This is pre-existing,
unrelated to this lot's two new files, and already scoped in
`decoupage.md`: `PayloadCodec` is lot-11's own modification. The
signature that changed (`RecordedRacePayload`) lives in `:core-domain`,
the broken call site in `:core-sync` — a different module, so R74's
condition for an R72 deferral is met; R72/R73 apply, the same way
lot-09's report already recorded for an equivalent case one layer
closer to the signature. No ktlint or detekt task is currently
registered project-wide (confirmed via `./gradlew tasks --all`) to run
in `PayloadCodec`'s place. `PhoneRaceRecordingRepository.kt` and
`RaceRecordingModule.kt`, plus their two test files, are reviewed by
hand against `RaceRecordingRepository`'s interface contract and against
`:app-wear`'s `RaceRecordingRepositoryImpl` / `RepositoryModule` for
signature and binding-style consistency; both new files carry a nominal
and a failure test per the sheet's four acceptance criteria (8 tests:
findInProgress, observeRecorded, the six write methods, and the module
provider).

## State

Added: PhoneRaceRecordingRepository (:app-phone); RaceRecordingModule
(:app-phone) — sixth Hilt module of the `:app-phone` DI graph, binding
RaceRecordingRepository to PhoneRaceRecordingRepository
Removed: —

## Requests

—
