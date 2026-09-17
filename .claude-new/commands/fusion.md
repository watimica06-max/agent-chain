---
description: Merge a finished feature into the global — bug-fix decisions first
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command chains four phases** — the Rédacteur folding the coding
decisions in, the Fusionneur over the bug-fix lists, then its two merge
invocations.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **One run per feature, once every bug-fix cycle has been coded.**
The global is not revised while a downstream cycle is running on the
same scope.

---

## What you read

**Only what the routing table tests** — the presence of files, and
whether a `## Decision` or an `Answer:` field is empty. 🔴 **Never
their content beyond that.**

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## Where to resume

🔴 **Walk this table from the top and stop at the first row that
matches.**

| # | Test | What you do |
|---|---|---|
| 1 | `desc-produit.md` absent | 🔴 **Error** — say so and stop |
| 2 | A `blocked_*.md` with an empty `## Decision` | 🔴 **STOP** — relay it |
| 3 | A `blocked_*.md` with a filled `## Decision` | 📌 **The agent its name carries**, at the invocation its `## Invocation` line names |
| 4 | `rapport-fusion.md` exists | 🔴 **STOP** — the merge is done |
| 5 | A root questions file with an empty `Answer:` | 🔴 **STOP** — relay it |
| 6 | 🔴 **`desc-produit-fusion.md` absent** | **Rédacteur, invocation 3 — Merging** |
| 7 | 🔴 **`questions-fusionneur-NN.md` holding `### Q`, answered**, and no `plan-fusion.md` | **Fusionneur, invocation 3** |
| 8 | A `bugfix-*/` folder, and no `questions-fusionneur-*` anywhere | **Fusionneur, invocation 3** |
| 9 | `questions-fusionneur-NN.md`, answered — 📌 **empty, or its questions resolved** | **Fusionneur, invocation 2** |
| 10 | `plan-fusion.md` exists | **Fusionneur, invocation 2** |
| 11 | Otherwise | **Fusionneur, invocation 1** |

🔴 **The order of these rows is the routing.** ⚠️ **The Rédacteur comes
before every Fusionneur row**: it writes the source the Fusionneur
reads, and a Fusionneur invocation above it would run on a file that
does not exist.

⚠️ **And a `bugfix-*/` folder comes before the row without it** — 📌
**the two conditions differ by that folder alone**, and the general one
placed first would shadow the specific: a correction cycle would go to
invocation 2, which needs a plan no invocation wrote.

📌 **Row 8 fires once.** The Fusionneur writes a questions file even when
empty, and its presence is what says the pass has run — the
`bugfix-*/` folders never go away.

🔴 **An empty one sends the next run to row 9, not back to row 7** — 📌
**row 7 tests `### Q`**, so a pass that asked nothing does not repeat
itself. ⚠️ **Without that test, row 7 would fire on its own output**,
for ever.

⚠️ **Row 8 covers every `bugfix-NN` at once**, not the last one. **A
feature with no bug-fix cycle never matches rows 7 or 8.**

🔴 **Row 6 fired: copy the product file, then invoke.** 📌 **In that
order** — ⚠️ **the row tests the copy's absence**, so copying first
would make it never fire:

    cp docs/features/<name>/desc-produit.md \
       docs/features/<name>/desc-produit-fusion.md

📌 **The agent has no tool that copies** — ⚠️ **and a whole read
followed by a whole write truncates in silence.** 🔴 **It amends the
copy; you make it.**

🔴 **Row 6 runs once, before the merge ever starts.** 📌 **The
Rédacteur folds into `desc-produit-fusion.md` the product decisions
settled while the code was written** — ⚠️ **they went into sheets, and
would otherwise reach neither the product file nor the global.**

📌 **Name it every `code/decisions-produit.md` that `/9_controle`
produced, in cycle order** — 🔴 **the feature's own first, then `bugfix-01`, then
`bugfix-02`.** ⚠️ **A later cycle that revised an earlier decision wins,
and that is what the order is for.**

📌 **No decisions file at all → it writes a faithful copy** — 🔴 **the
Fusionneur must never have to choose its source.**

---

## Git, before invoking

🔴 **Before invoking, move every root `questions-*.md` whose prefix is
not the one the phase you are about to run writes:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every file of that prefix but the highest** — the last one
stays at the root, it carries the numbering.

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
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded.

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

---

## How it runs

**One phase per run.** 🔴 **Never chain two agents** — each stop hands
back to the Product Owner, and the next run picks the table up again.

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
  description="<phase> <feature>",
  prompt="Feature folder: docs/features/<name>/. <Which invocation>."
)
```

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are sequential and each
reads what the previous one wrote.

---

## Git, once it has reported

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
an unmerged branch is invisible to the next one. ⚠️ **A `blocked_*.md`
merges too**: the Product Owner has to see it.

---

🔴 **The agent reports having applied a decision → rename its blocking
file:**

    git mv <folder>/blocked_<agent>.md <folder>/blocked_<agent>-NN.md

📌 **`NN`: the highest in that folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file** — 🔴 **left at
the unnumbered name, the next run stops on it.**

## What you relay

The agent's own report, and **which row of the table fired**. 🔴
**Nothing else is yours**: no phase chain.
