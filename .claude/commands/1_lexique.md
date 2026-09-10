---
description: Settle the idea file's vocabulary before the product file is written
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `lexicographe`.**

📌 **It runs before `/2_structure`, and loops** until a questions file
comes out empty. 🔴 **Then the vocabulary is settled**, and the chain
starts.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, and nothing else.** 📌 **You never open the idea file, nor a
questions file's content.**

⚠️ **`CLAUDE.md`'s standing reading rules apply.**

---

## Before anything else

🔴 **Does `blocked_lexicographe.md` sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands |
| Its `## Decision` is filled | 📌 **Name it in the prompt** |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

---

## Which invocation

🔴 **What sits at the feature folder's root decides.** 📌 **The name,
never the number.**

| At the root | Invocation |
|---|---|
| Neither questions file | **1 — Sweeping** |
| `questions-lexicographe` alone | **2 — Settling** |
| `questions-sondeur` alone | **3 — Watching** |
| Both | **4 — Correcting** |

⚠️ **`/2_structure` files the lexicographe's**, 📌 **`/4_grille` files
whatever is not its own** — 🔴 **which is what keeps these four apart.**

**A file with an empty `Answer:`** → 🔴 **stop**, and say which
questions are waiting.

📌 **After 2, run 1 again** — 🔴 **a settled term can uncover a pair the
first sweep could not see.**

📌 **After 4, the grid's file is clean** — 🔴 **run `/2_structure`.**

⚠️ **An empty questions file ends a loop.**

🔴 **A `desc-produit.md` in the folder does not stop 3 or 4** — 📌 they
run on every turn of the grid. ⚠️ **It stops 1 and 2**: the vocabulary
is settled before the product file exists, never after — a term changed
then would leave sixty blocks carrying the old one.

---

## The invocation

```
Agent(
  subagent_type="lexicographe",
  model="opus",
  description="Sweep <name>'s vocabulary",
  prompt="The idea file: docs/features/<name>/idees.md.
          Invocation <1 — Sweeping, 2 — Settling,
                       3 — Watching, or 4 — Correcting>.
          Write to docs/features/<name>/."
)
```

🔴 **Never paraphrase its process** — not its inputs, its sweeps, its
output format. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_lexicographe.md \\
           docs/features/<name>/blocked_lexicographe-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

**After every invocation** — 🔴 **check `lexique.md` exists**, and grep
its two counts: `retenu` for what is settled, the lines under
`## Non tranché` for what is not.

**After 1 or 3** — 🔴 **grep `^### Q` in the questions file** and
count. 📌 **Say how many.**

⚠️ **A missing file stops the command** — say which.

🔴 **Never read what a question says.** 📌 **The Product Owner answers
them, not you.**

---

## Git, in this mode

🔴 **File the previous turn's questions file before invoking:**

    git mv docs/features/<name>/questions-lexicographe-NN.md \
           docs/features/<name>/questions/lexicographe/

📌 **The highest-numbered one stays at the root** — it carries the
numbering. ⚠️ **Create `questions/lexicographe/` if it does not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and the agent settles nothing.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. *(Seen
once: a whole invocation lost that way.)*

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

**What to run next**

| What just happened | Next |
|---|---|
| 1 or 3 asked something | 📌 Answer them, then `/1_lexique` again |
| 2 ran, and 1 finds nothing left | 📌 `/2_structure` |
| 4 ran | 📌 `/2_structure` — 🔴 the grid's answers are settled |

🔴 **Nothing else is yours**: no risk level, no
`TaskCreate`, no reading of what a term means.

**If it returns `blocked_lexicographe.md`**: relay it and stop.
