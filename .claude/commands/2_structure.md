---
description: Structure the idea file into a product file
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `redacteur`, invocation 1 or 2.**

📌 **It runs as many times as needed.** With no questions file it reads
`idees.md`; with one, it integrates the answers instead.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **One `ls` of the feature folder's root**, and nothing else.
📌 **You pass the agent the file it reads; it does not look for
itself.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

🔴 **Never open a questions file's content** — 📌 its name is all you
need.

---

## How it runs

**First, the blocking file.** 🔴 **Does `blocked_redacteur.md` sit in
the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands |
| Its `## Decision` is filled | 📌 **Name it in the prompt**, beside the file to read |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

**Then, which invocation and which file:**

| At the root | Invocation | What you name |
|---|---|---|
| No questions file | **1 — Structuring** | `idees.md` |
| One or more, any prefix | **2 — Integrating** | 🔴 **The highest-numbered one** |

⚠️ **Any prefix** — 📌 the agent integrates the answers whichever agent
asked.

🔴 **If the highest carries an empty `Answer:`** — 📌 **stop**, and say
which questions are waiting.

```
Agent(
  subagent_type="redacteur",
  model="opus",
  description="Structure <name>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation <1 — Structuring, or 2 — Integrating>.
          Read: <idees.md, or questions-<agent>-NN.md>.
          <Plus: blocked_redacteur.md, its decision is filled.>"
)
```

🔴 **Name the file, always** — ⚠️ **the agent opens that one and no
other.**

### Once it has run

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_redacteur.md \
           docs/features/<name>/blocked_redacteur-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Grep `NEW` in `desc-produit.md`.** If any is there, **delete
`desc-par-nature.md` and `spec-technique.md`.**

⚠️ **The product file gained a block**, and anything built from the
previous version is stale — a targeted update on that technical
document would patch a file that no longer matches.

📌 **`MODIFIED` alone does not trigger this.** ⚠️ **A block that changed
still exists under the same identifier**, and a targeted update reaches
it.

📌 **Neither marker, nothing to delete.** An answer that only sharpened
a sentence leaves both valid, and the cycle can return straight to
`/5_reclasse` or `/6_convertit`.

**Say which files you deleted**, or that none needed it.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

### Invocation parameters

```
Agent(
  subagent_type="<agent>",
  model="sonnet",
  description="<phase> <feature>",
  prompt="Feature folder: docs/features/<name>/. <Which invocation>."
)
```

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are sequential
and each reads what the previous one wrote.

---

## Git, in this mode

🔴 **File the lexicographe's questions file before anything else:**

    git mv docs/features/<name>/questions-lexicographe-NN.md \
           docs/features/<name>/questions/lexicographe/

⚠️ **`/1_lexique` reads the root to know which invocation it is** — 📌
**a lexicographe file left there and a grid file beside it read as its
fourth**, when its work is done.

📌 **Create `questions/lexicographe/` if it does not exist.** ⚠️
**Nothing to file is a normal outcome.**

🔴 **Commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and the agent works on a stale
`questions.md`. *(Seen once: 186 lines in the worktree, 195 in the main
checkout.)*

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated. *(Measured on three
phases: the agent does the full job, cannot write, and the whole
invocation is redone.)*

**Then, once the agent reports:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — a phase whose output sits on
an unmerged branch is invisible to the next one. ⚠️ **A
`blocked_*.md` merges too**: the Product Owner has to see it.

---

## What you relay

The agent's own report.

**What to run next**

| What just happened | Next |
|---|---|
| It flagged a clarification | 🔴 **Answer it, then `/2_structure`** — nothing downstream runs while a flag stands |
| It wrote the product file | 📌 `/3_decoupe` | 🔴 **Nothing else is yours**:
no phase chain, no risk level, no `TaskCreate`.

**If it returns a `blocked_*.md`**: relay it and stop.
