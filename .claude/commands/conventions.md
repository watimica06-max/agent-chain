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

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **Always the feature folder, never a `bugfix-NN/`.** Conventions are
derived from a feature's own two documents; a correction cycle has
neither.

---

## What you read

**Only whether the files are there.** `spec-technique.md` and
`questions-architecte-*.md` at the root.

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## When it runs

<!-- TEMPORARY — dry run. This command sits outside the numbered chain
     and `/cycle` does not call it. Renumber it and wire it in once the
     grid has been measured. -->

📌 **Run by hand, on a feature whose technical document exists.** 🔴
**Not part of `/cycle`.**

⚠️ **The agent writes `docs/conventions-test.md` and never opens
`docs/TECHNICAL_CONVENTIONS.md`.** **Nothing it writes reaches the
coding agents.**

🔴 **On a project that already holds code, that dry run is what tells
you whether the grid derives or copies.** ⚠️ **The agent reads neither
the code nor the build files** — if a rule it writes matches what the
project already does, the grid found it, not the repository.

<!-- END TEMPORARY -->

🔴 **Stop if `spec-technique.md` is absent** — say so. The agent derives
from it, and the upstream loop has not reached it yet.

🔴 **Stop if a root `questions-architecte-*.md` carries an empty
`Answer:`** — relay it. The agent asked something and it is unanswered.

---

## Which invocation

| The root holds | What you invoke |
|---|---|
| A `questions-architecte-NN.md`, answered | **Invocation 2 — Integrating** |
| Nothing of the sort | **Invocation 1 — Deriving** |

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
  model="sonnet",
  description="conventions <feature>",
  prompt="Feature folder: docs/features/<name>/. Invocation 1 — Deriving."
)
```

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`.**

---

## Git, in this mode

🔴 **File away every root `questions-*.md` whose prefix is not
`architecte`:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every `questions-architecte-*.md` but the highest** — the last
one stays at the root, it carries the numbering.

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

**Then, once the agent reports:**

1. `git merge --no-ff -m "Merge <branch>" <branch>` from the main
   checkout root
2. `git push`
3. `git worktree remove <path>`

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
rules, no decision on what comes next.

🔴 **Then list every file the run left in the feature folder**, one line
each, path and size:

    git status --porcelain docs/features/<name>/

📌 **Three of them want the Product Owner's eyes** — the conventions
file, `couverture.md`, and the questions file. ⚠️ **Say which, and say
plainly when the questions file holds questions**: `wc -l` on it tells
you without opening it.

🔴 **A run that wrote a question and did not say so is a run whose
question is lost.** **The Product Owner does not go looking.**
