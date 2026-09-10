---
description: Give every product block its nature
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `classeur`, once.**

📌 **It runs between `/3_decoupe` and `/4_grille`, every turn.** 🔴 **The
grid asks a block the questions of its nature** — ⚠️ **a block without
one would be asked none.**

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

🔴 **Does `blocked_classeur.md` sit in the feature folder?**

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

**Two greps, and the union of what they return:**

| Grep | What it names |
|---|---|
| `grep -B1 '^Nature:$'` | 🔴 **The blocks whose nature is empty** — the line above each hit carries the block |
| `MODIFIED` | The blocks changed last turn, whose nature may have moved with them |

📌 **Neither returns anything** → 🔴 **do not invoke.** ⚠️ **Say so**,
and carry on to `/4_grille`.

⚠️ **A block with a filled nature and no marker was classed on an
earlier turn**, and nothing about it has moved since.

🔴 **The empty line is what makes this greppable** — 📌 the Rédacteur
and the decoupeur write `Nature:` with nothing after it, never omit it.

---

## The invocation

```
Agent(
  subagent_type="classeur",
  model="sonnet",
  description="Class <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          Look at these blocks: <B7, B62, B63>.
          <Plus: blocked_classeur.md, its decision is filled.>"
)
```

🔴 **Never paraphrase its process** — not the natures, its checks, its
output. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_classeur.md \
           docs/features/<name>/blocked_classeur-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Grep `-c '^Nature:$'` in `desc-produit.md`.** 📌 **Zero is what you
expect** — ⚠️ **anything else means a block was left unclassed**, and
you say which.

📌 **Relay which blocks changed nature**, if it says any did.

🔴 **Never read a block to check its work.** 📌 **The sondeurs probe
what it classed; that is what catches a wrong nature.**

---

## Git, in this mode

🔴 **Commit the feature folder before creating the worktree:**

    git add docs/features/<name>/ && git commit -m "chore: answers"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. The agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.

**Then, once it has reported:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.**

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.**

🔴 **Merge before handing back, always.** ⚠️ **A `blocked_*.md` merges
too**: the Product Owner has to see it.

---

## What you relay

📌 **How many blocks were classed**, and which changed nature.

🔴 **Nothing else is yours**: no risk level, no `TaskCreate`, no
reading of what a block says.

**What to run next** — 📌 `/4_grille`, whether it classed anything or
not.

**If it returns `blocked_classeur.md`**: relay it and stop.
