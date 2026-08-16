---
description: Produce the technical document for the Cadreur
allowed-tools: Read, Grep, Glob, Agent
argument-hint: [feature folder name]
---

Act as the orchestrator. Invoke the **convertisseur** subagent,
invocation 2 — Producing.

Feature folder: `docs/features/$ARGUMENTS/`

Invocation parameters: see `.claude/CLAUDE.md`, "Agent invocation" and
the upstream rule under the command table.

🔴 **No argument → stop and ask for the feature folder.** Do not invoke
anything.

🔴 **Nothing else is yours.** No phase chain, no risk level, no
`TaskCreate`. Relay what the agent returns — including a
`blocked_*.md` — and stop.
