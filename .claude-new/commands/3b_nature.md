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
`CURRENT_TECHNICAL_STATE.md`.

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

🔴 **Give the agent its questions file number in the prompt** — 📌 **the
highest `questions-classeur-NN.md` in the root and in `questions/classeur/`
together, plus one**; ⚠️ **`01` when there is none.** 🔴 **It never lists
a folder to find it** — it has no `Glob`.

🔴 **Then, the questions file it wrote last turn.** 📌 **The highest
`questions-classeur-NN.md`, at the root or under `questions/classeur/`** —
⚠️ **the root first**: a file answered and not yet filed sits there,
and looking only in the folder would file it unseen — ⚠️ **name it in the
prompt when it holds at least one `### Q`.**

📌 **It applies those answers before it derives** — 🔴 **an answer that
changed no block lands nowhere else.**

🔴 **File it once the agent reports having applied it** — 📌
`questions/classeur/`. ⚠️ **Left at the root it is named again next turn**,
and the same answers are applied twice.

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

🔴 **Grep `^### Q` in each before touching it** — 📌 **a file holding
questions is not yours to file**: ⚠️ **it waits on an answer, or its
answers were never integrated.** 🔴 **Stop and say which.**

📌 **Filed, it is read by no command again** — ⚠️ **and its answers are
lost for good.**

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
| `grep -B2 '^Nature:$'` | 🔴 **The blocks whose nature is empty** — 📌 **two lines above each hit is the heading**: `Genre:` sits between |
| 🔴 **Then keep only `Genre: comportement`** | ⚠️ **Only a behaviour has a nature** — a block of any other genre is dropped from the list |
| 🔴 **Plus `grep -B1 '^Nature: '` kept to the blocks whose `Genre:` is **not** `comportement`** | 📌 **Name those too** — ⚠️ **they changed genre since the classeur last ran**, and their nature has to be emptied: `/5_reclasse` stops on a filled one |
| `grep '^### .*MODIFIED'` | The blocks changed last turn, whose nature may have moved with them |

📌 **Neither returns anything** → 🔴 **do not invoke.** 📌 **Commit
what the filing moved, if anything, and push** — no worktree. ⚠️ **Say
there is nothing to class**, and go to *What you relay*.

⚠️ **A block with a filled nature and no marker was classed on an
earlier turn**, and nothing about it has moved since.

🔴 **The empty line is what makes this greppable** — 📌 the Rédacteur
and the decoupeur write `Nature:` with nothing after it, never omit it.

---

## Git, before invoking

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

---

## The invocation

```
Agent(
  subagent_type="classeur",
  model="sonnet",
  description="Class <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          Look at these blocks: <B7, B62, B63>.
          Your questions file number: NN.
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

🔴 **Every stop below merges first.** ⚠️ **The agent has written its
lines in the worktree** — 📌 **stopping before the merge loses the whole
invocation, and a worktree holding unmerged work never self-cleans.**
🔴 **Merge, push, remove the worktree, and then report the defect.**

🔴 **Grep `-B2 '^Nature:$'` in `desc-produit.md`, and keep the hits
whose `Genre:` is `comportement`.** 📌 **Zero is what you expect** — ⚠️
**one of those means a behaviour was left unclassed**, and you say
which.

⚠️ **A block of any other genre keeps an empty `Nature:` for good** —
🔴 **a bare `-c '^Nature:$'` would count those and report a defect on
every run.**

📌 **Relay which blocks changed nature**, if it says any did.

🔴 **Check `questions-classeur-NN.md` was written** — ⚠️ **a missing one is a
defect of the run**: the agent writes one every time.

🔴 **Grep `^### Q` in it** and say how many questions it holds.

🔴 **Never read a block to check its work.** ⚠️ **But nothing
downstream catches a wrong nature either** — 📌 **the sondeurs take it
as given and pick the grid's questions from it.**

🔴 **Relay the per-block list it reports** — one line per block, the
nature it gave. 📌 **That is the only place the Product Owner can see a
wrong one before the grid closes on it.**

---

## Git, once it has reported

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

🔴 **Nothing else is yours**: no
reading of what a block says.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| What just happened | Next |
|---|---|
| It wrote a blocking file, **naming a nature it could not settle** | 📌 Fill its `## Decision`, then `/3b_nature` again |
| It wrote a blocking file **and** a questions file with questions | 🔴 **Fill the decision first, then answer, then `/1_lexique`** — 📌 both end in the Rédacteur's hands |
| A `## Decision` names a rewrite | 🔴 **`/2_structure`** — 📌 **it names the blocking file to the Rédacteur, which rewrites the block.** ⚠️ **Then `/1_lexique` if the rewrite brought vocabulary, and the route back** |
| A `## Decision` names a nature outside the list | 🔴 **Nothing runs** — ⚠️ **the tables have to carry it first**; say so |
| 🔴 **A block carrying `Genre: comportement` still has an empty `Nature:`, and no blocking file explains it** | 📌 **Say which, and run `/3b_nature` again** — ⚠️ **a line left empty by neither a block nor a decision is a defect of the run.** 🔴 **Count only those**: a block of any other genre has an empty `Nature:` and must keep it |
| Its questions file holds questions | 🔴 **Answer them, then `/1_lexique`** — a block producing two things is split before the grid probes it |
| Its questions file is empty, or there was nothing to class | 📌 `/4_grille` |

**If it returns `blocked_classeur.md`**: relay it and stop.
