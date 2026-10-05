# Audit of conventions — bugfix-06

## Requests read

### Pass 1
architecte/cadreur.md
architecte/detailleur-lot-03.md
architecte/detailleur-lot-09.md
architecte/detailleur-lot-10.md
architecte/detailleur-lot-11.md
architecte/detailleur-lot-19.md
architecte/detailleur-lot-20.md
architecte/detailleur-lot-31.md
architecte/detailleur-lot-41.md
architecte/detailleur-lot-47.md
architecte/detailleur-lot-50.md
architecte/detailleur-lot-53.md
architecte/detailleur-lot-56.md
architecte/realisateur-lot-01.md
architecte/realisateur-lot-04.md
architecte/realisateur-lot-07.md
architecte/realisateur-lot-28.md
architecte/realisateur-lot-39.md
architecte/realisateur-lot-41.md
architecte/realisateur-lot-42.md
architecte/realisateur-lot-43.md

## Pass 1

### Requests still untreated

-

### Rules the cycle added

*no coverage file* — `couverture.md` is absent from bugfix-06, so no rule can be traced to an entry, and none can be shown to trace to none.

### Rules no lot can follow in its own scope

R3 | Binds this file, not a lot: no lot's `Modifies` holds `docs/TECHNICAL_CONVENTIONS.md`, and its header still reads "Version 1, settled 2026-09-03" while R72–R92 were written into it during this cycle | R3's own text, against the 21 rules the requests of this folder record as added
R6 | Requires every mechanisable rule to be wired into `./gradlew check`; the wiring lives in build and tool configuration no lot produces, and R67 states which rules each tool serves without any lot being able to add one | R6's own text, R67
R12 | Names `:core-platform` as the module realising §11.1, a module that does not exist; creating it means a `settings.gradle.kts` entry plus the `androidx.activity` and `androidx.core` declarations, which R77 counts as R66's forbidden addition inside a lot | architecte/cadreur.md
R16 | Requires an index on "any lookup a lot adds", but the entity, database and migration files carrying an index sit outside the adding lot's declared scope, and R8 bars modifying a committed migration | architecte/detailleur-lot-09.md
R65 | Names versions the build does not carry — AGP 8.9 against 9.3.2, Kotlin 2.1 against 2.2.10, `compileSdk` 36 against 37, `minSdk` 30/34 against 31/31, Compose BOM 2025.04 against 2026.02.01, Health Services 1.1 against 1.0.0, Play Services Wearable 19.0 against 18.0.0 — and under R1 the file wins; no lot can bring the build to them, since R66/R77 bar the build-file edit inside a lot | architecte/detailleur-lot-19.md
R69 | Requires both applications to be signed with the same key; a signing key is neither a symbol a lot produces nor a file a lot's `Modifies` names | R69's own text
R73 | Makes a lot's deliverability depend on another lot's sheet naming the owner of a broken call site; the lot cannot supply that name, and lot-07 was left undeliverable on exactly that | architecte/realisateur-lot-07.md

### Contradictions

R4 / R72 | Section 2. R4: deliverable "only when `./gradlew check` exits 0. No other definition of done." R72: deliverable on `./gradlew :<module>:check` alone while a project-wide failure stands. R72's "every other red build leaves R4 standing" places R4 elsewhere without lifting its "no other definition of done" | R4 and R72, section 2
R74 / R86 | Section 2. R74: a call site in the *same* module as the changed signature "never qualifies" for R72's deferral and "is this lot's own scope by construction." R86: "A production call site left broken in the same module by that same signature change is deferred under R72/R74." One tells the lot to carry it, the other to defer it | R74 and R86, section 2
R12 / R15 | Section 4. R12: "every entry of the technical document is realised in exactly one of them", while its own table lists §10.2 and §10.3 unqualified in both the `:app-phone` and `:app-wear` rows. R15: a §10.2 key present on both sides "is duplicated in `:app-phone` and in `:app-wear`, never shared" | R12 and R15, section 4

### Rules binding what their entry does not mention

*no coverage file* — `couverture.md` is absent from bugfix-06, so no rule can be opened against the entry it traces to.

### Refused, and where they belong

architecte/realisateur-lot-01.md | "Not a convention. It belongs to the machine." | "the environment the agents run in — `ANDROID_HOME` set once for the session, or a `local.properties` generated before the first `./gradlew` call. That is a decision for the Product Owner's machine setup and for the run harness, not for this file"
architecte/realisateur-lot-41.md | "Not a convention. It belongs to `CURRENT_TECHNICAL_STATE.md`, which this agent does not write." | "a trap entry on `CURRENT_TECHNICAL_STATE.md`, which the Détailleur and the Réalisateur read and write — not this file, and not this agent"
architecte/realisateur-lot-43.md | "Not a convention. It belongs to `CURRENT_TECHNICAL_STATE.md`, which this agent does not write." | "`CURRENT_TECHNICAL_STATE.md`'s existing `RaceTicker`/`Dispatchers.Main` trap entry, which the Détailleur and the Réalisateur read and write"
architecte/detailleur-lot-09.md | "Not a convention. R16 already answers the technical half without exception" | "the open point is carried in lot-09's own report"; "Note the missing index on `currentSegmentIndex` in lot-09's report, for whichever later lot's scope covers the schema files"
architecte/detailleur-lot-47.md | "Already carried, by R49 and R25 together. No rule written." | "Carry the stale `Needs:` entry back through lot-47's report, as a correction to the split, not as a convention amendment"
architecte/realisateur-lot-07.md | "Already carried — R73 … Naming which lot's sheet adapts `ProfileViewModel.kt` is a split decision, not a convention" | "Escalate the coverage gap to the split; no rule is written here"
architecte/detailleur-lot-19.md | R65's staleness refused within the request | "Raise it to the Product Owner as its own amendment"
architecte/detailleur-lot-20.md | Whether the user is told a push failed, refused within the request | "a product decision, and is not settled here. It needs an §10 key, and this agent invents none. Carry it back as a product question if the behaviour is wanted"
architecte/detailleur-lot-31.md | `MainActivityTest`'s orphaned break, refused within the request | "Not architecte's to settle: raise it back through the split, the same way lot-53's R74 finding was raised, so a lot is named to adapt it"
architecte/detailleur-lot-53.md | The lot-15 / lot-53 same-module assignment, refused within the request | "The split assigning `RecordedRaceSyncService.sync` to lot-15 while it shares `:core-domain` with lot-53's change needs correcting — that correction is not architecte's to make … raise it there"

### Standing since an earlier pass

-

### Rules the split never meets

*no coverage file* — `couverture.md` is absent from bugfix-06, so no rule can be traced to an entry and confronted with `code/decoupage.md`'s `Anchor` lines.
