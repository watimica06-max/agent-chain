---
description: Settle the vocabulary — the idea file's before the product file is written, then every answered questions file's
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `lexicographe`.**

📌 **It runs before `/2_structure`, and loops** until a questions file
comes out empty. 🔴 **Then the vocabulary is settled**, and the chain
starts.

📌 **It runs again on every answered questions file of the grid or of
the conversion** — 🔴 **before `/2_structure` integrates it.**

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
| No questions file | **1 — Sweeping** |
| `questions-lexicographe` alone | **2 — Settling** |
| Another agent's questions file alone | **3 — Watching** |
| Another agent's, and `questions-lexicographe` | **4 — Correcting** |
| Two files of other agents | 🔴 **Stop** — a filing failed; say which files |

📌 **Call the other agent's file *the answered file***, whichever agent
wrote it — 🔴 **3 and 4 name it in the prompt.**

⚠️ **Every command of the cycle files the questions files it does not
read** — 🔴 **which is what keeps these four apart**: the root holds at
most the file waiting on you, and yours.

**A file with an empty `Answer:`** → 🔴 **stop**, and say which
questions are waiting.

📌 **After 2, run 1 again** — 🔴 **a settled term can uncover a pair the
first sweep could not see.**

📌 **After 4, the answered file is clean** — 🔴 **run `/2_structure`.**

⚠️ **An empty questions file ends a loop.**

🔴 **A `desc-produit.md` in the folder does not stop 3 or 4** — 📌 they
run on every turn of the grid and of the conversion. ⚠️ **It stops 1
and 2**: the vocabulary is settled before the product file exists,
never after — a term changed then would leave sixty blocks carrying the
old one.

---

## The invocation

```
Agent(
  subagent_type="lexicographe",
  model="opus",
  description="Sweep <name>'s vocabulary",
  prompt="The idea file: docs/features/<name>/idees.md.
          <When it exists: The lexicon: docs/features/<name>/lexique.md.>
          Invocation <1 — Sweeping, 2 — Settling,
                       3 — Watching, or 4 — Correcting>.
          <At 3 and 4: The answered file:
           docs/features/<name>/questions-<agent>-NN.md.>
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

    git mv docs/features/<name>/blocked_lexicographe.md \
           docs/features/<name>/blocked_lexicographe-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **After 2 or 4, file the lexicographe's questions file it applied**,
into `questions/lexicographe/`, inside the worktree before the merge —
⚠️ **left at the root, it would read as waiting again**, and the next
run would take it for invocation 2. 📌 **A new
`questions-lexicographe-NN.md` it wrote stays at the root** — an answer
left the choice open, and it waits on the Product Owner.

**After every invocation** — 🔴 **check `lexique.md` exists**, and grep
its two counts: `retenu` for what is settled, the lines under
`## Non tranché` for what is not.

**After 1 or 3** — 🔴 **grep `^### Q` in the new
`questions-lexicographe-NN.md`** and count. 📌 **Say how many.**

**After 2 or 4** — 📌 **say whether it wrote a new one**, and how many
entries it holds.

⚠️ **A missing file stops the command** — say which.

🔴 **Never read what a question says.** 📌 **The Product Owner answers
them, not you.**

---

## Git, in this mode

🔴 **Before invoking, file every root `questions-*.md` this invocation
does not read** — ⚠️ **the lexicographe's is read at 2 and 4, the
answered file at 3 and 4**:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

📌 **Create `questions/<agent>/` if it does not exist**; nothing to file
is a normal outcome.

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

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| What just happened | Next |
|---|---|
| It wrote a blocking file | 📌 Fill its `## Decision`, then `/1_lexique` again |
| 1 asked something | 📌 Answer them, then `/1_lexique` again |
| 1 asked nothing | 📌 `/2_structure` — 🔴 the vocabulary is settled |
| 2 wrote a new questions file | 📌 Answer it, then `/1_lexique` again |
| 2 wrote none | 📌 `/1_lexique` again — 🔴 a settled term can uncover a pair |
| 3 ran | 📌 **Answer its questions if it asked any, then `/1_lexique` again** — 🔴 4 replaces the retired terms the answers carry, questions or not |
| 4 wrote a new questions file | 📌 Answer it, then `/1_lexique` again |
| 4 wrote none | 📌 `/2_structure` — 🔴 the answers are settled |

🔴 **Nothing else is yours**: no risk level, no
`TaskCreate`, no reading of what a term means.

**If it returns `blocked_lexicographe.md`**: relay it and stop.
