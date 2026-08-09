---
name: technical-state-format
description: How to write an entry in docs/CURRENT_TECHNICAL_STATE.md — what earns a place, what to remove, the domain/subject structure, where a trap goes. Load before writing to that file, never write to it without.
---

# Writing `CURRENT_TECHNICAL_STATE.md`

It exists so an agent does not **rebuild what already exists** or **fall
into a known trap**. An entry earns its place only if it is **not
quickly findable in the code** AND **not knowing it would cause a
mistake**.

**Write an entry when your step created or removed:**
- a service, provider or mechanism another step could otherwise rebuild
- a table, a route, an orchestrator chain, a deletion cascade
- a trap ("date queries must use a range — the `date` column is
  contaminated")
- a dead state ("`MealConfirmationLog.streakImpact` has no writer")

**Do NOT write**: a narrative of what you changed, anything a single
grep would answer, or a coding convention (that is
`TECHNICAL_CONVENTIONS.md`).

🔴 **Remove what your step made false.** A deleted service's entry
**disappears** — it does not become "removed by step_XXX". A changed
behaviour is **rewritten**, not appended to. Without this the file only
ever grows.

**Describe the state, never the change:**
- ✅ *"`ActivityReconciliationService` merges two same-type entries less
  than 3h apart."*
- ❌ *"step_111 deleted all three mechanisms and replaced them with…"*
- **No step number in the body** — except in the migration table, where
  it is part of the fact.
- **Rewrite if any of these appear**: a past-tense verb, a step number,
  "replaced by", "no longer", "used to". They are the signature of a
  narrative.

**Where the entry goes.** Agents search one way — *"what must I know
about X?"* The format serves that and nothing else:

- **Two heading levels only**: `## Domain` (Schema · Services ·
  Providers · Routes · Sync · Auth · Native · Traps — general · Dead
  state · To verify), then `### Subject`.
- 🔴 **The subject heading is the code identifier, verbatim** —
  `### CalendarMeal`, never `### The meal calendar entity`. That string
  is what an agent greps.
- 🔴 **The one-line summary after the dash carries the answer.** In the
  common case the agent greps the heading and stops there. Make that
  line self-sufficient.
- **Body: four lines maximum, wrapped at ~80 characters.** Longer means
  you are describing a change, not a state.
- **Tables only for genuinely tabular data** — a few words per cell. A
  row needing a paragraph becomes its own `###` entry: multi-line table
  content produces lines `Read` cannot open and `grep` truncates.

    ### ActivityReconciliationService — merges same-type entries under 3h apart

    `lib/domain/services/activity_reconciliation_service.dart`. Pure,
    no I/O. Window is `kActivityReconciliationWindow`, boundary
    EXCLUSIVE (exactly 180 min is OUT). `start_time_minutes` is the
    only start-time input — never `date` (day key, time-of-day
    contaminated) nor `createdAt`.

**Where a trap goes depends on whether it can be grepped:**
- **Owned by one subject** → put it under that subject, heading leading
  with the same identifier, then ⚠️:
  `### ActivityBudgetService ⚠️ guard is a single dated read`. One grep
  on the subject returns entry and trap together.
- **General, or owned by several** → `## Traps — general`. Agents read
  that section whole, because you cannot grep for a rule you don't know
  applies to you. When in doubt, put it here.
- `## Dead state` — what exists but is wired to nothing. Also read
  whole: you cannot grep for something you don't know is dead.
