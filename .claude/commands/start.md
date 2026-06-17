---
description: Run the autonomous agent workflow for the next pending task in docs/tasks/
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
---

Act as the orchestrator and execute the autonomous workflow defined in `.claude/CLAUDE.md`.

Do not re-derive the workflow here — CLAUDE.md is authoritative for the phases, the
risk-level routing (LOW / MEDIUM / HIGH), the per-agent model rules, and the
reviewer failure loop. Apply it as written.

Concretely: identify the next pending step in `docs/tasks/` (the first `step_XX_*/task.md`
with no PASS `review.md`), read its risk level, and run the matching workflow from CLAUDE.md
through to the reviewer's verdict. Then stop and present the manual-test list to the user.

If no pending task exists, say so and stop.
