---
description: Run the coding workflow for pending task files in docs/tasks/
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "[N] | task NNN | task NNN-MMM"
---

Act as the orchestrator. Apply **MODE 1 — DEVELOPMENT** from
`.claude/CLAUDE.md`, which is the only source for the workflow, the
model assignment and the invocation parameters. Do not restate it here.

## What the argument means

| Invocation | What to run |
|---|---|
| `/start_coding` | the next pending step, **one only** |
| `/start_coding 3` | up to **3** pending steps, starting from the next one |
| `/start_coding task 109` | **step_109 only**, whatever came before it |
| `/start_coding task 109-113` | steps 109 to 113, in order |

**Pending** means: `docs/tasks/step_XXX/task.md` exists and its
`review.md` has no PASS. Determine it with Phase 0's grep.

🔴 **An already-passed step is skipped, never a blocker.** In a range
or a count, move on to the next pending one. Only stop if a single
explicit `task NNN` is already passed — then say so and stop.

Stop when the count is reached, the range is exhausted, or no pending
step remains.
