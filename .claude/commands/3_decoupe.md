---
description: Split product blocks carrying more than one trigger
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `decoupeur`, once.**

📌 **It runs between `/2_structure` and `/4_grille`, every turn.** 🔴 **A
block the Rédacteur just wrote or changed may carry two triggers**, and
the sondeurs would probe it as one.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, and nothing else.** 📌 **You never open a block.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## Before anything else

🔴 **Does `blocked_decoupeur.md` sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands |
| Its `## Decision` is filled | 📌 **Name it in the prompt** |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

---

## Which blocks it looks at

**First turn — no `questions-*.md` anywhere:** 🔴 **every block.** 📌
**Name none in the prompt.**

**Later turns — two greps in `desc-produit.md`:**

| Grep | What it names |
|---|---|
| `NEW` | The blocks created last turn |
| `MODIFIED` | The blocks changed last turn |

📌 **A block neither grep names was already looked at**, and has not
moved since.

⚠️ **Do not grep the questions file** — 🔴 **a block an answer touched
carries `MODIFIED`**, and the second grep finds it.

---

## The invocation

```
Agent(
  subagent_type="decoupeur",
  model="opus",
  description="Split <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          Look at these blocks: <B7, B28 — or: every block>."
)
```

🔴 **Never paraphrase its process** — not its rule, its checks, its
output. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_decoupeur.md \\
           docs/features/<name>/blocked_decoupeur-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Grep `^### B` in `desc-produit.md`** and count. 📌 **Say how many
blocks the file held before, and how many it holds now.**

⚠️ **Same count means it split nothing** — 📌 **that is a normal
outcome**, and the cycle carries on to `/4_grille`.

🔴 **Never read a block to check its work.** 📌 **The sondeurs probe
what it produced; that is what catches a bad split.**

---

## Git, in this mode

🔴 **Commit the feature folder before creating the worktree:**

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. The agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.
*(Measured on three phases: the agent does the full job, cannot write,
and the whole invocation is redone.)*

**Then, once it has reported:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always.** ⚠️ **A `blocked_*.md` merges
too**: the Product Owner has to see it.

---

## What you relay

📌 **How many blocks before, how many after.**

**What to run next** — 📌 `/4_grille`, whether it split anything or
not.

🔴 **Nothing else is yours**: no risk level, no
`TaskCreate`, no reading of what a block says.

**If it returns `blocked_decoupeur.md`**: relay it and stop.
