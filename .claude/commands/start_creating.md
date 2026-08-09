---
description: Create task files from one or more spec documents
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<path/to/spec.md> [more specs...]"
---

Act as the orchestrator, in **task-file authoring mode**.

**The argument is mandatory**: one or more paths to the source spec
documents. Without it, ask for them and stop — never guess which specs
are meant.

## What you read

- `docs/tasks/_planning/<short-name>-plan.md` — **the only file you
  open in this mode**, and only to determine which phase you are
  invoking (see below).

You do not read the source specs, the task files being produced, or the
code. `CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## How it runs

**What you do**: invoke **task-writer**
(`.claude/agents/task-writer.md`) via `Agent()` with the **source file
path(s)** as the `prompt`, plus `model` — and nothing else.

🔴 **Never paraphrase task-writer's process in your invocation** — not
its phases, numbering, checks or pause schedule. It reads its own
instructions. Two runs drifted precisely because the orchestrator
composed its own restatement (one front-loaded a numbering check
before Phase 1; one told it to "start from CHECK 0", skipping Phase 1's
plan and pause entirely). **The fix is no paraphrase, not a better
one.** If the process must change, change `task-writer.md` — never
re-describe it here. Do not attempt the scoping inline yourself either.

📌 `model` is **your** parameter, not a restatement of its process.
Passing it is required; describing what it should do with it is what to
avoid.

### Which phase am I invoking? — read it, don't assume

Task-writer's model depends on the **phase**, so determine it
before every invocation. Read
`docs/tasks/_planning/<short-name>-plan.md`:

| Plan file state | Phase being invoked | Pass |
|---|---|---|
| No plan file yet | Phase 1 — macro plan | **opus** |
| `status: writing`, files still `complete: no` | Phase 2 — writing | **opus** |
| A phase's files all `complete: yes`, no verification recorded for it | End-of-phase verification | **sonnet** |
| `status: audit` | Phase 3 — cross-phase pass | **sonnet** |
| Phase 3 reported done | Phase 4 — close-out | **sonnet** |

⚠️ **A handoff mid-Phase-2 is still Phase 2** — context hygiene and
product decisions do not change the phase, so the model stays
`opus`. Only the verification passes and close-out drop to
Sonnet.

**Resume**: task-writer resumes from its own plan file — you do not
reconstruct progress. You read that file only to pick the right
model above.

### At every pause

🔴 **Never pass `isolation` in this mode.** It is concurrency
isolation, and task-writer's agents are sequential: each hand-off reads
the plan file the previous one wrote. An isolated agent branches fresh
and cannot see it. *(In the coding cycle the same mistake cost 135k
tokens on the first run.)*

🔴 **Before starting a new phase: check the plan file yourself.** If
the previous phase is complete with no verification recorded, run that
verification first. *(Missed once: Phase G finished, the run entered
Phase H unverified.)*

**Mechanical steps, yours to do without waiting for anyone**: verify
the diff is clean.

**Never idle** — context freshness and product decisions are both
handled by spawning a fresh subagent, which starts context-free:

- **After every task file**: task-writer hands back — **one agent, one
  task file**, never chained. Invoke a new one immediately, **still
  `opus`** (a handoff does not change the phase). No message to
  the Product Owner, no waiting. *(Chaining was measured and is never
  cheaper — see `docs/process/ANALYSE_CONTEXTE_SUBAGENTS.md`.)*
- **A product decision**: relay the question to her **and keep going in
  parallel** — invoke a fresh task-writer, **`opus`**, on the
  files of this phase the decision does not affect (task-writer names
  them). 🔴 **Never cross into the next phase while it is unanswered.**
- **A phase's last file is written**: spawn a **third, context-free
  task-writer** whose only job is that phase's verification —
  **`sonnet, high`, not opus**. Never the agent that wrote the files —
  it would audit its own output, with a loaded context. *(Shape: agent
  1 writes G1-G3 · agent 2 writes G4-G5 and reports complete · agent 3,
  fresh, verifies G1-G5.)* Relay where things stand; **silence means
  continue**.

- **No pause after individual HIGH-risk task files.**

🔴 **Never fabricate her approval.** No "accepted, no objections", no
summary judgment, no paraphrase of something she said earlier as if it
covered new content. If she hasn't sent a new message, you have nothing
to relay. *(Happened twice in a row: `step_108` and `step_109` were
re-invoked on generated acceptance text she never wrote.)* Continuing
on independent files while a question is open is **not** the same as
answering it for her.

**task-writer updates on its own**: its plan file, the run's annexe,
and `PLAN_TASK_FILES_V2.md` (at close-out). You do not update these
for task files it produced.

📌 **`CALIBRATION_RISK_LEVEL.md` is not written during authoring** —
the reviewer writes its entries at PASS time, when the real outcome is
known.

---


---

## Invocation parameters

```
Agent(
  subagent_type="task-writer",
  model="opus",
  run_in_background=false,
  description="Author task files from <source>",
  prompt="<the source spec paths, and nothing else>"
)
```

`model` per the phase table above. ❌ No `effort` parameter exists —
it is static frontmatter in `task-writer.md`.

---

## Before every invocation

🔴 **Confirm task-writer's planned step number is still free.** Numbers
are assigned once, in its Phase 1 plan — but a concurrent session or an
unmerged branch can claim one in the meantime (it has happened). Check
the `docs/tasks/` listing. **task-writer cannot run this itself.** If the planned number
is taken, **say so in the invocation**: it will take the next free one
and correct its plan.

---

## Git, in this mode

**task-writer commits each task file itself as it goes** — you do not
commit for it, and with no worktree there is nothing to merge back.

🔴 Its `Bash` is `git add`/`commit`/`status` only: it never merges,
never branches, never runs `git worktree list`. Anything else is
yours.
