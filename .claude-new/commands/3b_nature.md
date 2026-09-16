---
description: Give every product block its nature
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `classeur`, once.**

📌 **It runs between `/3a_genre` and `/4_grille`, every turn.** 🔴 **The
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

🔴 **Then, the questions file it wrote last turn.** 📌 **The highest
`questions-classeur-NN.md` under `questions/classeur/`** — ⚠️ **name it in the
prompt when it holds at least one `### Q`.**

📌 **It applies those answers before it derives** — 🔴 **an answer that
changed no block lands nowhere else.**

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

🔴 **File every root `questions-*.md`**, by `git mv`:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there**, or the next command
cannot tell which one waits.

📌 **Create `questions/<agent>/` if it does not exist**; nothing to file
is a normal outcome.

---

## Which blocks it looks at

**Two greps, and the union of what they return:**

| Grep | What it names |
|---|---|
| `grep -B1 '^Nature:$'` | 🔴 **The blocks whose nature is empty** — the line above each hit carries the block |
| 🔴 **Then keep only `Genre: comportement`** | ⚠️ **Only a behaviour has a nature** — a block of any other genre is dropped from the list |
| `MODIFIED` | The blocks changed last turn, whose nature may have moved with them |

📌 **Neither returns anything** → 🔴 **do not invoke.** 📌 **Commit
what the filing moved, if anything, and push** — no worktree. ⚠️ **Say
there is nothing to class**, and go to *What you relay*.

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
          <Plus: your answered questions file:
           docs/features/<name>/questions/classeur/questions-classeur-NN.md.>
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

📌 **`NN`: the highest `blocked_classeur-NN.md` in the folder plus one —
`01` when there is none.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Grep `-c '^Nature:$'` in `desc-produit.md`.** 📌 **Zero is what you
expect** — ⚠️ **anything else means a block was left unclassed**, and
you say which.

📌 **Relay which blocks changed nature**, if it says any did.

🔴 **Check `questions-classeur-NN.md` was written** — ⚠️ **a missing one is a
defect of the run**: the agent writes one every time.

🔴 **Any stop from here on merges first.** ⚠️ **The agent has written
its lines in the worktree** — 📌 **stopping before the merge loses the
whole invocation, and a worktree holding unmerged work never
self-cleans.** 🔴 **Merge, push, remove the worktree, and then report
the defect.**
🔴 **Grep `^### Q` in it** and say how many questions it holds.

🔴 **Never read a block to check its work.** ⚠️ **But nothing
downstream catches a wrong nature either** — 📌 **the sondeurs take it
as given and pick the grid's questions from it.**

🔴 **Relay the per-block list it reports** — one line per block, the
nature it gave. 📌 **That is the only place the Product Owner can see a
wrong one before the grid closes on it.**

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

📌 **How many blocks were classed**, which changed nature, and how many
questions — 🔴 **and the per-block list, as the agent reports it.**

🔴 **Nothing else is yours**: no risk level, no `TaskCreate`, no
reading of what a block says.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| What just happened | Next |
|---|---|
| It wrote a blocking file, **naming a nature it could not settle** | 📌 Fill its `## Decision`, then `/3b_nature` again |
| It wrote a blocking file **and** a questions file with questions | 🔴 **Fill the decision first, then answer, then `/1_lexique`** — 📌 both end in the Rédacteur's hands |
| A `## Decision` names a rewrite | 🔴 **`/1_lexique`**, then the route back — ⚠️ **this command cannot act on a rewrite** |
| A `## Decision` names a nature outside the list | 🔴 **Nothing runs** — ⚠️ **the tables have to carry it first**; say so |
| 🔴 **The `^Nature:$` count is non-zero and no blocking file explains it** | 📌 **Say which blocks, and run `/3b_nature` again** — ⚠️ **a line left empty by neither a block nor a decision is a defect of the run** |
| Its questions file holds questions | 🔴 **Answer them, then `/1_lexique`** — a block producing two things is split before the grid probes it |
| Its questions file is empty, or there was nothing to class | 📌 `/4_grille` |

**If it returns `blocked_classeur.md`**: relay it and stop.
