---
description: Run the cycle's phases in sequence, stopping whenever a decision is needed
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **cycle mode**.

**This command chains the cycle's own commands** — `/1_structure`,
`/2_grille`, `/3_reclasse`, `/4_convertit`, `/7_decoupe` — and stops
the moment something needs a decision.

⚠️ **`/5_compare` and `/6_fusionne` are not in the chain.** They update
the global product document, and nothing downstream reads it — run them
when you choose.

🔴 **It stops before `/8_code`.** The split is the last point where
turning back costs no commits.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## Before anything

**Create `stop1.md`, empty, if it does not exist** in the feature
folder.

📌 **It is the disarmed form of the stop signal.** Renaming it to
`stop.md` halts the chain before the next phase; renaming it back
resumes.

⚠️ **Prerequisite, not your job**: `docs/features/*/stop*.md` must be
in the project's `.gitignore`. **If it is not, say so and carry on** —
neither file is ever committed.

---

## What the markers mean

🔴 **Three markers drive every routing decision.** Read them exactly.

| Marker | Where | What it means |
|---|---|---|
| An empty `Answer:` | A questions file | A decision is waiting for the Product Owner |
| `[integrated:` | A questions file | `/1_structure` has run since `/2_grille` |
| `NEW` | `desc-produit.md` | A block has never been closed by the grid |

**And three states of a questions file:**

| State | Test |
|---|---|
| **Empty** | No `### Q` line at all — 📌 the closing `## Questions set aside` section does not count |
| **Answered** | Every `Answer:` carries text |
| **Integrated** | At least one entry carries `[integrated:` |

📌 **"The latest questions file" is the highest-numbered one at the
root**, whatever its prefix.

---

## The routing table

🔴 **Replayed after every phase. First match wins, always.**

| # | Test | What you do |
|---|---|---|
| 1 | `stop.md` at the root | 🔴 **STOP** — the Product Owner halted the chain |
| 2 | Two or more questions files at the root | 🔴 **STOP** — a filing step failed; say which files |
| 3 | A `blocked_detailleur`, `_realisateur` or `_relecteur` | **STOP** — that block belongs to `/8_code` |
| 4 | A cycle agent's `blocked_*` with `## Decision` empty | **STOP** — the decision is still to write |
| 5 | The latest questions file has an empty `Answer:` | **STOP** — questions are waiting |
| 6a | Latest is integrated **and** `NEW` is present | `/2_grille` |
| 6b | Latest is integrated, prefix `analyste` | `/2_grille` |
| 6c | Latest is integrated, other prefix, no `NEW` | `/3_reclasse` if no `spec-technique.md`, else `/4_convertit` |
| 7 | A cycle agent's `blocked_*` with `## Decision` filled | `analyste` → `/1_structure` · `convertisseur` → `/3` or `/4` on `spec-technique.md` · `cadreur` or `verificateur` → `/7_decoupe` |
| 8 | Latest is answered, not integrated | `/1_structure` |
| 9 | `<<ASSUMED` in `spec-technique.md` | `/4_convertit` |
| 10 | `code/sequence.md` carries defects | 🔴 **STOP** — the split is not converging |
| 11 | `code/sequence.md` is clean | 🔴 **STOP** — run `/8_code` |
| 12 | Latest is empty | `analyste` → `/3_reclasse` · `convertisseur` → `/4_convertit` if no `spec-technique.md`, else `/7_decoupe` |
| 13 | `spec-technique.md`, no questions file | `/7_decoupe` |
| 14 | `desc-par-nature.md`, no questions file | `/4_convertit` |
| 15 | `desc-produit.md`, no questions file | `/2_grille` |
| 16 | `idees.md` alone | `/1_structure` |
| 17 | None of the above | **Error** — say what the folder holds |

⚠️ **The order is the logic.** A `NEW` outranks a resolved block:
closing what was never closed comes before resuming where you stopped.

---

## After `/1_structure`

📌 **The invalidation is the command's own** — it deletes
`desc-par-nature.md` and `spec-technique.md` when a `NEW` appeared, and
nothing otherwise. **You do not repeat it.**

🔴 **You read its report** — which files it deleted, or that none
needed it — **and you replay the table.**

---

## Warnings

**Raised when a `NEW` appears, never routed** — this command drives
neither the merge nor the code:

⚠️ **`plan-fusion.md` exists** → *the merge plan is stale, re-run
`/5_compare`.*

🔴 **`rapport-fusion.md` exists** → *the global carries an earlier
version of this feature.*

⚠️ **Any `code/*/verdict.md` exists** → *lots were coded against a
split that is about to change.*

📌 **Carry on after saying it.** They are the Product Owner's calls.

---

## Between two phases

🔴 **Look for `stop.md` from the main checkout, never from a
worktree** — a worktree holds a copy frozen at its creation, and would
never see a file created after it.

📌 **Which is why each phase gets its own worktree**: created from
local `HEAD`, merged, removed, before the next one starts. **Each
phase's output is acquired even if you stop right after.**

---

## What you relay when you stop

**The cause · the phase reached · what to do to resume.**

⚠️ **Plus every warning raised along the way.**

🔴 **Never paraphrase an agent's process**, and never run an agent
directly — you chain commands, and each carries its own mode.
