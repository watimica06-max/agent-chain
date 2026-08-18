---
description: Cut a technical document into lots and derive the execution sequence
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **downstream splitting mode**.

**This command runs `cadreur`, then `verificateur`, until the split
holds.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

**`code/sequence.md`, and only its `## Defects` section** — to know
whether the split holds. Each agent declares its own inputs; you pass
the feature folder and nothing else.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## How it runs

**1. `cadreur`** — produces `code/decoupage.md`.

**2. `verificateur`** — produces `code/sequence.md`.

**3. Read its `## Defects` section.**

| It holds | What you do |
|---|---|
| Nothing | 🔴 **Stop.** The split holds; report where things stand |
| Defects | Back to `cadreur`, then `verificateur` again |

🔴 **Three rounds maximum.** On the third round still carrying defects,
stop and hand back — the split is not converging, and that is the
Product Owner's call.

🔴 **Never paraphrase an agent's process in your invocation** — not its
inputs, its checks, its output format. It reads its own instructions.

### Invocation parameters

```
Agent(
  subagent_type="cadreur",
  model="sonnet",
  description="Split <feature>",
  prompt="Feature folder: docs/features/<name>/."
)
```

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the two phases are sequential and the
second reads what the first wrote.

📌 **On a take-back, say so in the prompt**: `"Feature folder: … . The
Vérificateur reported defects in code/sequence.md."`

---

## Git, in this mode

🔴 **Commit the feature folder first**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-split"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

**Then, once the split holds:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git worktree remove <path>`

🔴 **Merge before handing back, always** — including a
`blocked_*.md`: the Product Owner has to see it.

---

## What you relay

**Where the split stands**: how many lots, how many blocks, and any
defect left. 🔴 **Nothing else is yours** — no risk level, no
`TaskCreate`, no judgement on the split itself.

**If an agent returns a `blocked_*.md`**: relay it and stop.
