---
description: Give every product block its genre
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `qualifieur`, once.**

📌 **It runs between `/3_decoupe` and `/3b_nature`, every turn.** 🔴
**Only a `comportement` has a nature, and only it is probed** — ⚠️ **a
block without a genre would be given a nature it does not have, and
probed for what it does not do.**

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

🔴 **Does `blocked_qualifieur.md` sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands |
| Its `## Decision` is filled | 📌 **Name it in the prompt** |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

🔴 **Then, the questions file it wrote last turn.** 📌 **The highest
`questions-qualifieur-NN.md` under `questions/qualifieur/`** — ⚠️ **name it in the
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
| `grep -B1 '^Genre:$'` | 🔴 **The blocks whose genre is empty** — the line above each hit carries the block |
| `MODIFIED` | The blocks changed last turn, whose genre may have moved with them |

📌 **Neither returns anything** → 🔴 **do not invoke.** 📌 **Commit
what the filing moved, if anything, and push** — no worktree. ⚠️ **Say
there is nothing to qualify**, and go to *What you relay*.

⚠️ **A block with a filled genre and no marker was qualified on an
earlier turn**, and nothing about it has moved since.

🔴 **The empty line is what makes this greppable** — 📌 the Rédacteur
and the decoupeur write `Genre:` with nothing after it, never omit it.

---

## The invocation

```
Agent(
  subagent_type="qualifieur",
  model="sonnet",
  description="Qualify <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          Look at these blocks: <B7, B62, B63>.
          <Plus: your answered questions file:
           docs/features/<name>/questions/qualifieur/questions-qualifieur-NN.md.>
          <Plus: blocked_qualifieur.md, its decision is filled.>"
)
```

🔴 **Never paraphrase its process** — not the genres, its checks, its
output. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_qualifieur.md \
           docs/features/<name>/blocked_qualifieur-NN.md

📌 **`NN`: the highest `blocked_qualifieur-NN.md` in the folder plus one —
`01` when there is none.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Grep `-c '^Genre:$'` in `desc-produit.md`.** 📌 **Zero is what you
expect** — ⚠️ **anything else means a block was left unqualified**, and
you say which.

📌 **Relay which blocks changed genre**, if it says any did.

🔴 **Check `questions-qualifieur-NN.md` was written** — ⚠️ **a missing one is a
defect of the run**: the agent writes one every time.

🔴 **Any stop from here on merges first.** ⚠️ **The agent has written
its lines in the worktree** — 📌 **stopping before the merge loses the
whole invocation, and a worktree holding unmerged work never
self-cleans.** 🔴 **Merge, push, remove the worktree, and then report
the defect.**
🔴 **Grep `^### Q` in it** and say how many questions it holds.

🔴 **Never read a block to check its work.** 📌 **A wrong genre is
caught by what follows** — the classeur finds no nature for a block that
produces nothing, and the grid probes what it left in.

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

📌 **How many blocks were qualified**, which changed genre, and how many
questions.

🔴 **Nothing else is yours**: no risk level, no `TaskCreate`, no
reading of what a block says.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| What just happened | Next |
|---|---|
| It wrote a blocking file, **naming a genre it could not settle** | 📌 Fill its `## Decision`, then `/3a_genre` again |
| It wrote a blocking file **and** a questions file with questions | 🔴 **Fill the decision first, then answer, then `/1_lexique`** — 📌 both end in the Rédacteur's hands |
| A `## Decision` names a rewrite | 🔴 **`/1_lexique`**, then the route back — ⚠️ **this command cannot act on a rewrite** |
| A `## Decision` names a genre outside the list | 🔴 **Nothing runs** — ⚠️ **the tables have to carry it first**; say so |
| 🔴 **The `^Genre:$` count is non-zero and no blocking file explains it** | 📌 **Say which blocks, and run `/3a_genre` again** — ⚠️ **a line left empty by neither a block nor a decision is a defect of the run** |
| Its questions file holds questions | 🔴 **Answer them, then `/1_lexique`** — a genre in doubt is settled before the classeur gives a nature |
| Its questions file is empty, or there was nothing to qualify | 📌 `/3b_nature` |

**If it returns `blocked_qualifieur.md`**: relay it and stop.
