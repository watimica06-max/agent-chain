---
description: Probe the product file against the framing grid — three angles and one global invocation at once
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `sondeur` four times in parallel, then
`assembleur` once.**

📌 **Three angles run pass A, each in its own reading order, on the
blocks that moved; one global invocation records every block and runs
passes B and C.** 🔴 **The union of what they raise is the turn's
output** — ⚠️ **not what they agree on.**

📌 **It runs as many times as needed.** Each run writes the next
`questions-sondeur-NN.md`. **An empty one ends the loop**; then run
`/5_reclasse`.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, and nothing else.** 📌 **You never open a block, the grid,
or a questions file's content.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## Before anything else

🔴 **Does a blocking file sit in the feature folder, unnumbered?** 📌
**Five names, one per invocation this command runs** — ⚠️ **the four
sondeurs run at once, and a shared name would let one overwrite
another:**

| File | Whose |
|---|---|
| `cadrage-produit/blocked_par-bloc.md` | The sondeur reading block by block |
| `cadrage-produit/blocked_par-question.md` | The sondeur reading question by question |
| `cadrage-produit/blocked_par-nature.md` | The sondeur reading by nature |
| `cadrage-produit/blocked_global.md` | The global invocation |
| `blocked_assembleur.md`, at the feature folder's root | The assembleur |

| | What you do |
|---|---|
| None | 📌 Carry on |
| One, its `## Decision` empty | 🔴 **Stop** — say which one still stands |
| One, its `## Decision` filled | 📌 **Name it in that agent's prompt, and in no other** |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

🔴 **A flagged block was transcribed on a reading nobody confirmed** —
📌 **probing it would close a text that is about to change.**

---

## Which blocks the angles probe

**First turn — no `questions-sondeur-*.md` anywhere:** 🔴 **every
block.** 📌 **Name none in the prompts.**

**Later turns — two greps in `desc-produit.md`, and the union of what
they return:**

| Grep | What it names |
|---|---|
| `NEW` | The blocks created last turn |
| `MODIFIED` | The blocks changed last turn |

⚠️ **Never the questions file** — 🔴 **a block an answer touched carries
`MODIFIED`**, and the second grep finds it.

⚠️ **This narrows the angles alone.** 🔴 **The global invocation reads
every block, every turn** — a changed block changes its crossings with
the others.

📌 **The three angles get the same list.**

📌 **Neither grep returns anything, on a later turn** → 🔴 **invoke
nothing.** 📌 **Nothing moved since a turn whose questions are
answered** — write `questions-sondeur-NN.md` empty, commit and push
without a worktree, and go to *What you relay*.

---

## The four invocations

🔴 **The four `Agent(...)` calls go in one message.** ⚠️ **Several
messages run them in series** — 📌 they share nothing, and issued
together the wall-clock cost is one sondeur's.

🔴 **Then wait for all four** before anything else.

**The three angles differ by one line, and one line only — their
reading order.**

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by block",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 1 — Angle.
          Pass A on these blocks: <list — or: every block>.
          Your reading order: block by block, in the document's order.
          Take every grid question to a block before moving to the next.
          Write to docs/features/<name>/cadrage-produit/par-bloc.md.
          <Plus: cadrage-produit/blocked_par-bloc.md, its decision is filled.>"
)
```

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by question",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 1 — Angle.
          Pass A on these blocks: <list — or: every block>.
          Your reading order: question by question. Take one grid
          question to every block in scope, then move to the next
          question.
          Write to docs/features/<name>/cadrage-produit/par-question.md.
          <Plus: cadrage-produit/blocked_par-question.md, its decision is filled.>"
)
```

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by nature",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 1 — Angle.
          Pass A on these blocks: <list — or: every block>.
          Your reading order: by nature. Gather the blocks of one
          nature, probe them together, then move to the next nature.
          Write to docs/features/<name>/cadrage-produit/par-nature.md.
          <Plus: cadrage-produit/blocked_par-nature.md, its decision is filled.>"
)
```

**The global invocation:**

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Record and cross <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 2 — Global: every block.
          Write the record to docs/features/<name>/cadrage-produit/releve.md.
          Write to docs/features/<name>/cadrage-produit/global.md.
          <Plus: cadrage-produit/blocked_global.md, its decision is filled.>"
)
```

🔴 **Never paraphrase a sondeur's process** — not its inputs, its
checks, its output format. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notifications.

❌ **Never pass `isolation`** — 📌 **the four read the same files and
write different ones**, and none reads what another wrote.

---

## Then the merge

🔴 **Check the four questions files exist, and the record.** 📌 **A
missing one stops the command** — say which, and go no further. ⚠️ **A
merge missing one reading is a merge nobody can trust.**

```
Agent(
  subagent_type="assembleur", model="sonnet",
  description="Merge the four readings of <name>",
  prompt="Merge, in docs/features/<name>/cadrage-produit/:
            par-bloc.md
            par-question.md
            par-nature.md
            global.md
          Write to docs/features/<name>/cadrage-produit/questions.md.
          <Plus: blocked_assembleur.md, its decision is filled.>"
)
```

---

## Once it has reported

🔴 **A blocking file you named is filed**, in the folder it sits in:

    git mv docs/features/<name>/cadrage-produit/blocked_par-bloc.md \
           docs/features/<name>/cadrage-produit/blocked_par-bloc-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Copy `cadrage-produit/questions.md` to
`questions-sondeur-NN.md`** at the feature folder's root — 📌 **`NN`:
the highest `questions-sondeur-NN.md` in `questions/sondeur/`, plus
one**; ⚠️ the root holds none by now.

📌 **Renumber `Q1` upward.** ⚠️ **Drop its closing `## Merge`
section** — 🔴 it is a working note, not a question.

📌 **Everything else is copied as written** — 🔴 **you rephrase
nothing.**

📌 **No question at all** → 🔴 **write the file empty.** ⚠️ **That is
what ends the loop.**

---

## Git, in this mode

🔴 **Before invoking, file every root `questions-*.md`:**

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there.**

⚠️ **`git mv`, never a read-and-rewrite** — the agents must not open
those files, and neither should you.

🔴 **And the previous turn's six `cadrage-produit/` files:**

    git mv docs/features/<name>/cadrage-produit/par-bloc.md \
           docs/features/<name>/cadrage-produit/closed/par-bloc-NN.md

📌 **The same for `par-question.md`, `par-nature.md`, `global.md`,
`releve.md` and `questions.md`.**

📌 **Create `questions/<agent>/` and `cadrage-produit/closed/` if they
do not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and an agent works on a stale
`questions.md`. *(Seen once: 186 lines in the worktree, 195 in the main
checkout.)*

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.
*(Measured on three phases: the agent does the full job, cannot write,
and the whole invocation is redone.)*

🔴 **Then, inside the worktree, create the folder the agents write
into:**

    mkdir -p docs/features/<name>/cadrage-produit/closed

⚠️ **An agent whose target folder is missing does not stop** — 📌 **it
searches**: it lists the folder, tries an absolute path. 🔴 **Create the
folder and none of that happens.**

**Then, once every agent has reported:**

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

## What you relay

📌 **How many questions each reading raised**, and how many the merge
kept.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| The run | Next |
|---|---|
| Wrote a blocking file | 📌 Fill its `## Decision`, then `/4_grille` again |
| Its questions file holds questions | 📌 **Answer them, then `/1_lexique`** — 🔴 it settles the vocabulary your answers brought, before the Rédacteur reads them |
| Its questions file is empty | 📌 `/5_reclasse` — 🔴 the product file is closed |

🔴 **Nothing else is yours**: no risk level, no
`TaskCreate`, no reading of what the questions say.

**If an agent returns a `blocked_*.md`**: relay it and stop.
