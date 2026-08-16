---
description: Verify the product file and close it
allowed-tools: Read, Grep, Glob, Agent
argument-hint: [feature folder name]
---

Act as the orchestrator. Invoke the **analyste** subagent,
invocation 4 — Finalising.

Feature folder: `docs/features/$ARGUMENTS/`

Invocation parameters: see `.claude/CLAUDE.md`, "Agent invocation" and
the upstream rule under the command table.

🔴 **No argument → stop and ask for the feature folder.** Do not invoke
anything.

🔴 **Nothing else is yours.** No phase chain, no risk level, no
`TaskCreate`. Relay what the agent returns — including a
`blocked_*.md` — and stop.
