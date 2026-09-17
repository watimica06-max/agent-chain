---
description: Derive the project's technical conventions from the two documents
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `architecte`.**

📌 **It can run more than once.** If a hole could not be filled, the
agent writes `questions-architecte-NN.md`; answering and re-running
turns each answer into a rule.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/<first argument>/` — 🔴 **the first
argument only**; ⚠️ **`$ARGUMENTS` holds both when a second names a
`bugfix-NN`.**

🔴 **Invocations 1 and 2 run on the feature folder, never on a
`bugfix-NN/`.** Conventions are derived from a feature's own two
documents, and a correction cycle has neither.

📌 **Invocation 3 runs where the request was written** — the feature
folder, or a `bugfix-NN/` inside it. **A second argument names it.**

---

## What you read

**Whether the files are there** — `spec-technique.md`,
`couverture.md`, `docs/TECHNICAL_CONVENTIONS.md`, and
`questions-architecte-*.md` at the root — 🔴 **plus two greps on that
last one**: `Answer:` lines with nothing after them, and `^### Q`.

⚠️ **Counts, never content** — 📌 **you never open a questions file.**

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## When it runs

📌 **After `/6_convertit`, before `/7_lots`.** The Cadreur reads the
conventions in full; they have to exist when it does.

⚠️ **Run by hand** — 🔴 **no command chains it**: 📌 **it sits between
`/6_convertit` and `/7_lots`**, and the Product Owner runs it there.

🔴 **Stop if `spec-technique.md` is absent** — say so. The agent derives
from it, and the upstream loop has not reached it yet. ⚠️ **Invocation 3
does not need it**: it judges a request against the conventions and the
grid.

🔴 **Stop if a root `questions-architecte-*.md` carries an empty
`Answer:`** — relay it. The agent asked something and it is unanswered.

---

## Which invocation

🔴 **Walk this table from the top and stop at the first row that
matches.**

| The folder holds | What you invoke |
|---|---|
| A `blocked_architecte.md` with an empty `## Decision` | 🔴 **Nothing** — relay it and stop |
| 🔴 **A `blocked_architecte.md` with a filled `## Decision`** | 📌 **The invocation its `## Invocation` line names** — 🔴 **name the file in the prompt** |
| A request in `architecte/` with an empty `## Verdict` | **Invocation 3 — Requests** |
| A `questions-architecte-NN.md` at the root with an empty `Answer:` | 🔴 **Nothing** — say which questions wait |
| A `questions-architecte-NN.md` at the root, **answered** | **Invocation 2 — Integrating** |
| A `questions-architecte-NN.md` at the root with **no `### Q`** | 🔴 **Nothing** — the derivation asked nothing. 📌 **Say `/7_lots`** |
| 🔴 **No `docs/TECHNICAL_CONVENTIONS.md`** | **Invocation 1 — Deriving** — 📌 **the first derivation this repository ever had** |
| **It exists, and no `couverture.md` at the working folder's root** | 🔴 **Invocation 4 — Completing** — ⚠️ **on a feature folder only**: 📌 **a `bugfix-NN` carries no technical document of its own to walk** |
| **It exists, and a `couverture.md` is there** | 📌 **Nothing to do** — say `/7_lots` |
| Nothing of the sort | 📌 **Nothing to do** — say `/7_lots` |

🔴 **The last rows are what stops a silent rewrite.** ⚠️ **Invocation 1
opens no existing conventions file and writes it afresh** — 📌 **every
rule invocation 3 added since would be lost.**

🔴 **The test is the conventions file, never `couverture.md`.** ⚠️
**`couverture.md` is written per feature**, so a second feature has
none — 📌 **and a test on it would send every feature but the first
through invocation 1.**

📌 **`couverture.md` tells something else**: whether this feature has
already been walked. 🔴 **That is the third row**, and it is what makes
the command idempotent.

📌 **An integrated questions file leaves the root** — 🔴 **filed after
invocation 2**, ⚠️ **otherwise every later run matches its row again and
integrates the same answers twice.**

🔴 **Give the agent its questions file number in the prompt** — 📌 **the
highest `questions-architecte-NN.md` in the root and in
`questions/architecte/` together, plus one**; ⚠️ **`01` when there is
none.** 📌 **It never lists a folder to find it.**

📌 **Invocation 3 runs on a working folder** — a feature, or a
`bugfix-NN` inside it. ⚠️ **Each cycle holds its own `architecte/`**,
and a request is treated in the cycle that raised it.

---

## Git, before invoking

🔴 **File away every root `questions-*.md` whose prefix is not
`architecte`:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every integrated `questions-architecte-*.md`** — 📌 **nothing
stays at the root to carry the numbering**: ⚠️ **you give the agent its
number in the prompt**, counting the root and `questions/architecte/`
together.

📌 **Create `questions/<agent>/` if it does not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and the agent works on a stale file.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local.

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

🔴 **The agent reports having applied a decision → rename its blocking
file:**

    git mv <folder>/blocked_architecte.md <folder>/blocked_architecte-NN.md

📌 **`NN`: the highest in that folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file** — 🔴 **left at
the unnumbered name, the next run stops on it.**

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
  subagent_type="architecte",
  model="opus",
  description="conventions <feature>",
  prompt="Feature folder: docs/features/<name>/. Invocation 1 — Deriving.
          Your questions file number: NN."
)
```

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`.**

---

## Git, once it has reported

**Then, once the agent reports:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**; 📌 **`git merge` takes the
   branch's commits, not the worktree's files**, and
   `git worktree remove` refuses a dirty tree
2. `git merge --no-ff -m "Merge <branch>" <branch>` from the main
   checkout root
3. `git push`
4. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.**

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — an unmerged branch is
invisible to whoever reads next.

---

## What you relay

**The agent's own report, and which invocation ran.** 🔴 **Nothing else
is yours**: no reading of the conventions file, no summary of its
rules.

📌 **And the blocking file, when the run left one** — ⚠️ **the Product
Owner would otherwise learn of it from a file listing, at best.**

**What to run next** — 📌 **indications for the Product Owner.**

| The run | Next |
|---|---|
| It raised questions | 📌 **Answer them, then `/conventions`** |
| It raised a **product question** | 🔴 **The framing grid did not close the product** — ⚠️ **the Product Owner decides**: back into the loop, or corrected by hand |
| It raised an **`inconsistency`** | 🔴 **The technical document is wrong** — 📌 **say which entry**: the fix is upstream, in `/6_convertit`, not here |
| It wrote a blocking file | 📌 **Fill its `## Decision`, then `/conventions`** |
| It asked nothing, or everything is integrated | 📌 `/7_lots` |

🔴 **Then list every file the run left in the feature folder**, one line
each, path and size:

    git status --porcelain docs/features/<name>/

📌 **Three of them want the Product Owner's eyes** — the conventions
file, `couverture.md`, and the questions file. ⚠️ **Say which, and say
plainly when the questions file holds questions**: `wc -l` on it tells
you without opening it.

🔴 **A run that wrote a question and did not say so is a run whose
question is lost.** **The Product Owner does not go looking.**
