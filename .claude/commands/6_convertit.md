---
description: Produce the technical document for the Cadreur
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `convertisseur`, invocation 2 — Producing.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

Nothing. Each agent declares its own inputs; you pass the feature
folder and nothing else. `CLAUDE.md`'s standing reading rules apply:
never open `CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## How it runs

**What you do**: invoke the agent via `Agent()` with the feature folder
and which invocation it is — and nothing else.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

### Invocation parameters

```
Agent(
  subagent_type="<agent>",
  model="sonnet",
  run_in_background=false,
  description="<phase> <feature>",
  prompt="Feature folder: docs/features/<name>/. <Which invocation>."
)
```

❌ No `effort` parameter exists — it is static frontmatter in the
agent file. ❌ **Never pass `isolation`** — the phases are sequential
and each reads what the previous one wrote.

---

## Git, in this mode

🔴 **Commit the feature folder first**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and the agent works on a stale
`questions.md`. *(Seen once: 186 lines in the worktree, 195 in the main
checkout.)*

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then enter a worktree, before invoking the agent** — not after it
fails. The harness blocks a subagent's writes until the session is
isolated, whatever `run_in_background` says. *(Measured on three
phases: the agent does the full job, cannot write, and the whole
invocation is redone.)*

**Then, once the agent reports:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git worktree remove <path>`

🔴 **Merge before handing back, always** — a phase whose output sits on
an unmerged branch is invisible to the next one. ⚠️ **A
`blocked_*.md` merges too**: the Product Owner has to see it.

---

## What you relay

The agent's own report, and nothing more. 🔴 **Nothing else is yours**:
no phase chain, no risk level, no `TaskCreate`.

**If it returns a `blocked_*.md`**: relay it and stop.
