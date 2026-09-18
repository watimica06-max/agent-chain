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
`CURRENT_TECHNICAL_STATE.md`.

---

## Before anything else

🔴 **Does a blocking file sit in the feature folder, unnumbered?** 📌
**Six names, one per invocation this command runs** — ⚠️ **the four
sondeurs run at once, and a shared name would let one overwrite
another:**

| File | Whose |
|---|---|
| `cadrage-produit/blocked_par-bloc.md` | The sondeur reading block by block |
| `cadrage-produit/blocked_par-question.md` | The sondeur reading question by question |
| `cadrage-produit/blocked_par-nature.md` | The sondeur reading by nature |
| `cadrage-produit/blocked_global.md` | The global invocation |
| `blocked_existant.md`, **at the feature root** | 🔴 **The second time** — 📌 **not under `cadrage-produit/`** |
| `blocked_assembleur.md`, at the feature folder's root | The assembleur |

🔴 **Test all six names — any number can stand at once.** ⚠️ **Four
sondeurs that ran together can leave two, three or four files**, each
with its own decision.

| | What you do |
|---|---|
| None | 📌 Carry on |
| Any, its `## Decision` empty | 🔴 **Stop** — say which ones still stand, every one of them |
| Every one standing has its `## Decision` filled | 📌 **Name each in its own reading's prompt, and in no other** — 🔴 **and invoke those readings alone, together**: see below. ⚠️ **The merge waits for all of them** |

⚠️ **Read that one heading in each, nothing else** — 📌 the agent reads
the file.

🔴 **On a decision you just lifted, only what blocked runs again.** 📌
**A sondeur's decision → that reading alone** — ⚠️ **several sondeurs'
→ those readings, and no other.** 📌 **The assembleur's → the merge
alone**, on the four files still standing: ⚠️ **re-running the
sondeurs would replace the very inputs the decision was written
against.** 📌 **The files of the readings that did not block are
already in `cadrage-produit/`** — ⚠️ **nothing touched the product file
between the two runs**, and recomputing them would cost up to three
opus invocations for the same result. 🔴 **Leave them in place, do not
file them, and merge once every blocked reading has written its own.**

⚠️ **Unless the markers changed in between** — 📌 **then it is a new
turn, and all four run.**

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

🔴 **A flagged block was transcribed on a reading nobody confirmed** —
📌 **probing it would close a text that is about to change.**

---

## Before you invoke: two greps

🔴 **Every block carrying `Genre: comportement` has a filled
`Nature:`** — 📌 `grep -B1 '^Nature:$'`, then keep the ones whose
`Genre:` says `comportement`. ⚠️ **One hit and you stop** — say which
blocks, and that `/3b_nature` has to run first.

📌 **The third angle reads by nature** — 🔴 **a block without one would
be grouped by judgement, or left out of that reading with nothing
signalling it.**

🔴 **The latest questions file at the root is answered.** 📌 **An entry
whose `Answer:` is empty and that carries no `Défaut:` line** — ⚠️ **one
and you stop**, saying which questions wait: the turn that produced
them is not closed, and probing again would raise the same gaps through
five invocations.

⚠️ **An entry whose `Answer:` is empty **and** that carries a `Défaut:`
line is answered** — 📌 **silence accepts the proposal**, and that is
what the line exists for. 🔴 **Test both**: `^Answer:\s*$` with no
`Défaut:` above it in the same entry.

📌 **Whether it is integrated is the `### Q` guard's test**, under
*Git, before invoking*.

---

## Which blocks the angles probe

🔴 **Only the blocks carrying `Genre: comportement` are probed** — 📌
**`grep -B1 '^Genre: comportement$'` gives them**, whatever the turn.
⚠️ **A block of any other genre is never named to a sondeur**: it has no
trigger, no output, and the grid's questions do not apply to it.

**First turn — no `questions-sondeur-*.md` anywhere:** 🔴 **every
behaviour block.** 📌 **Name them all.**

**Later turns — two greps in `desc-produit.md`, and the union of what
they return:**

| Grep | What it names |
|---|---|
| `grep '^### .*NEW'` | The blocks created last turn |
| `grep '^### .*MODIFIED'` | The blocks changed last turn |

🔴 **Anchored on the heading line, where the marker sits.** ⚠️ **A bare
`NEW` matches prose inside a block**, and would name one carrying no
marker.

📌 **The hit is the heading** — 🔴 **the identifier is what follows
`### `, up to the first space after it.**

⚠️ **Never the questions file** — 🔴 **a block an answer touched carries
`MODIFIED`**, and the second grep finds it.

⚠️ **This narrows the angles alone.** 🔴 **The global invocation reads
every block, every turn** — a changed block changes its crossings with
the others.

📌 **The three angles get the same list.**

## The transverse blocks

🔴 **A second grep, `grep -B1 '^Genre: transverse$'`** — 📌 **and their
identifiers go in every sondeur's prompt, as a list of their own.**

⚠️ **They are not probed.** 📌 **The sondeur holds them beside the
blocks it probes**: a question a transverse rule already answers becomes
a *défaut*, not a gap the Product Owner has to close by hand.

🔴 **Every turn, whatever moved** — ⚠️ **a transverse rule reaches blocks
that did not move**, and the angles need it whether or not it changed.

## The out-of-scope blocks

🔴 **A third grep, `grep -B1 '^Genre: hors périmètre$'`** — 📌 **and
their identifiers go in the global invocation's prompt only.**

⚠️ **Not to the three angles** — 📌 **what they answer is `C1.2`, a pass
C question asked once on the feature**, and pass C is the global's.

🔴 **The Product Owner already wrote what she excludes** — ⚠️ **without
them the grid asks him a second time**, and she answers what he has
already answered.

🔴 **What closes the first time is the highest-numbered
`questions-sondeur-NN.md` holding no `### Q`** — 📌 **wherever it sits,
at the root or filed under `questions/sondeur/`**: ⚠️ **glob both
places and test the highest `NN` alone** — an earlier turn's file holds
its answered questions, and says nothing about the grid. 🔴 **Test it
before the two marker greps of *Which blocks the angles probe*.** 📌
**It is empty → the first time is closed**, and the second time runs:
see below.

⚠️ **Root or filed, because a sibling command files it** — 📌 **a
`/3_decoupe` run by hand between the closure and the second time, or
`/4_grille` itself on the run that blocked in `blocked_existant.md`,
moves the empty file under `questions/sondeur/`**: 🔴 **a test on the
root alone would then read a closed grid as a broken one.**

⚠️ **Never *no marker returned*** — 📌 **markers are stripped by the
Rédacteur when it integrates a questions file that holds questions.** 🔴
**An empty one is integrated by nobody**, so the markers stay, and a
test on them would send the grid round for ever on a feature it has
nothing left to ask about.

📌 **Neither marker grep returns anything, and the highest-numbered
`questions-sondeur-NN.md` holds a `### Q`** → 🔴 **two cases, told apart
by `questions-existant-NN.md`, root or `questions/existant/`:**

| | What it is | Next |
|---|---|---|
| One exists | 🔴 **The grid is closed** — the second time already ran, and nothing moved since | 📌 **Invoke nothing**, and say `/5_reclasse` |
| None anywhere | 🔴 **A run produced no questions file at all** — nothing moved and nothing closed the turn | 📌 **Stop and say so**, naming the highest file and where it sits — `/4_grille` again once a marker or an empty file is there |

---

## Git, before invoking

🔴 **Grep `^### Q` in each root `questions-*.md` before touching it** —
📌 **a file holding questions is not yours to file**: ⚠️ **it waits on
an answer, or its answers were never integrated.** 🔴 **Stop and say
which.** 📌 **The sondeur's own is no exception** — ⚠️ **answered, it
goes through `/1_lexique` and `/2_structure`**, which integrate it and
put it away; 🔴 **still at the root, it has not been through them.**
📌 **The empty one that closed a time holds no `### Q`**, and is filed
like any other.

🔴 **Then file every root `questions-*.md`:**

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there.**

⚠️ **`git mv`, never a read-and-rewrite** — the agents must not open
those files, and neither should you.

🔴 **Not on a turn about to re-run the merge alone** — 📌 **a turn
resuming on `blocked_assembleur.md`'s decision**: ⚠️ **every
`cadrage-produit/` file the previous turn wrote is what the merge is
about to read**, and filing any of them would take it from under it.
📌 **Nor on a turn re-running a blocked reading alone** — 🔴 **the
other readings' files stay where they are**: see *Before anything
else*.

**Otherwise, the previous turn's six `cadrage-produit/` files:**

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

---

## The second time — the feature against what is already built

🔴 **It runs once, and only when the first time has closed** — 📌 **no
block marked, nothing left to probe inside the feature.**

🔴 **Has it already run?** 📌 **A `questions-existant-NN.md` anywhere,
at the root or in `questions/existant/`** — ⚠️ **one and the second time
is over**: write nothing, and go to *What you relay*.

🔴 **Which blocks** — 📌 **`grep -B3 '^Global: '` in
`desc-produit.md`** — ⚠️ **three lines above each hit is the heading**:
`Genre:` and `Nature:` sit between. 📌 **Those alone**: a block
attached to nothing hits nothing.

📌 **Nothing returned** → 🔴 **invoke nothing.** ⚠️ **The feature
touches nothing that exists** — write `questions-existant-NN.md` empty,
commit and push without a worktree, and relay.

🔴 **One invocation, not four** — 📌 **there is one corpus to cross, and
three reading orders would read the global three times.**

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Cross <name> against the global",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_EXISTANT.md.
          The global: docs/PRODUIT_GLOBAL.md.
          Invocation 3 — Existant.
          These blocks, with the global section each names:
            <B12 → ## Activity screen>
            <B40 → ## Steps panel>
          Write to docs/features/<name>/questions-existant-NN.md.
          Your blocking file, if you cannot produce:
            docs/features/<name>/blocked_existant.md.
          <Plus: that same file, its decision is filled.>"
)
```

📌 **`NN`: the highest `questions-existant-NN.md` in
`questions/existant/`, plus one** — ⚠️ **`01` when there is none.**

🔴 **It wrote `blocked_existant.md`** — 📌 **relay it and stop.** ⚠️
**Its decision filled, `/4_grille` runs the second time again**, naming
the file in the prompt; 🔴 **rename it `blocked_existant-NN.md` once the
agent reports having applied it.**

🔴 **No merge** — 📌 **one reading, one file.** ⚠️ **The assembleur
merges the four of the first time, and them alone.**

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
          Pass A on these blocks: <list>.
          The transverse blocks, to hold beside them: <list — or: none>.
          Your reading order: block by block, in the document's order.
          Take every grid question to a block before moving to the next.
          Write to docs/features/<name>/cadrage-produit/par-bloc.md.
          <Plus: docs/features/<name>/cadrage-produit/blocked_par-bloc.md, its decision is filled.>"
)
```

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by question",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 1 — Angle.
          Pass A on these blocks: <list>.
          The transverse blocks, to hold beside them: <list — or: none>.
          Your reading order: question by question. Take one grid
          question to every block in scope, then move to the next
          question.
          Write to docs/features/<name>/cadrage-produit/par-question.md.
          <Plus: docs/features/<name>/cadrage-produit/blocked_par-question.md, its decision is filled.>"
)
```

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by nature",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 1 — Angle.
          Pass A on these blocks: <list>.
          The transverse blocks, to hold beside them: <list — or: none>.
          Your reading order: by nature. Read the blocks of one
          nature side by side, take each of them through every
          question on its own, then move to the next nature.
          Write to docs/features/<name>/cadrage-produit/par-nature.md.
          <Plus: docs/features/<name>/cadrage-produit/blocked_par-nature.md, its decision is filled.>"
)
```

**The global invocation:**

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Record and cross <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Invocation 2 — Global: every behaviour block: <list>.
          The transverse blocks, to hold beside them: <list — or: none>.
          The out-of-scope blocks: <list — or: none>.
          Write the record to docs/features/<name>/cadrage-produit/releve.md.
          Write to docs/features/<name>/cadrage-produit/global.md.
          <Plus: docs/features/<name>/cadrage-produit/blocked_global.md, its decision is filled.>"
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

🔴 **First, does any `cadrage-produit/blocked_*.md`, or
`blocked_existant.md` at the feature root, sit at its
unnumbered name?** 📌 **One is enough** — ⚠️ **no merge this turn, and
no questions file at the root.** 🔴 **Relay it and stop.**

⚠️ **A sondeur that blocked writes no questions file** — 📌 **so the
existence check below would fire on it**, and report as missing a
reading that stopped for a reason you can read.

🔴 **Then check the four questions files exist, and the record.** ⚠️ **A
merge missing one reading is a merge nobody can trust.**

📌 **For each one that is missing, in this order:**

| | What you do |
|---|---|
| Its blocking file sits beside it | 🔴 **Relay it and stop** — 📌 **a decision awaits the Product Owner**, and the reading will resume from it |
| No blocking file either | 🔴 **Stop** — 📌 **say which reading produced nothing, and to run `/4_grille` again** |

⚠️ **A sondeur that blocked writes no questions file** — 📌 **so the
existence check fires on it, and *missing* is the wrong word for it.**

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
          <Plus: docs/features/<name>/blocked_assembleur.md, its decision is filled.>"
)
```

---

## Once it has reported

🔴 **The assembleur reports a missing input** — 📌 **it wrote nothing:
no `blocked_assembleur.md`, no `questions.md`.** ⚠️ **A missing input is
not a decision the Product Owner writes** — it is this command's to
repair.

| | What you do |
|---|---|
| Its report names a missing file | 🔴 **Stop** — 📌 **say which file, and to run `/4_grille` again** — ⚠️ nothing below runs |

🔴 **A blocking file you named is filed**, in the folder it sits in:

    git mv docs/features/<name>/cadrage-produit/blocked_par-bloc.md \
           docs/features/<name>/cadrage-produit/blocked_par-bloc-NN.md

📌 **`NN` is the turn's number** — 🔴 **the one the
`questions-sondeur-NN.md` of this turn takes.** ⚠️ **A turn that
produced none takes the number it would have taken.** 📌 **The six
`closed/` files take the same one.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Copy `cadrage-produit/questions.md` to
`questions-sondeur-NN.md`** at the feature folder's root — 📌 **`NN`:
the highest `questions-sondeur-NN.md` in `questions/sondeur/`, plus
one**; ⚠️ the root holds none by now.

🔴 **A copy, byte for byte** — 📌 **`cp`, never a read-and-rewrite.**
⚠️ **You hold fifty entries in context and rewrite them by hand is
exactly where one is dropped or reworded.**

📌 **The assembleur numbers from `Q1` and writes no working section** —
🔴 **what it writes is what the Product Owner answers.**

📌 **No question at all** → 🔴 **write the file empty.** ⚠️ **That is
what ends the loop.**

---

## Git, once it has reported

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

📌 **How many questions each reading raised, and how many the merge
kept** — 🔴 **both from the assembleur's report**, never a count of
your own.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| The run | Next |
|---|---|
| A **sondeur** wrote a blocking file — or several did | 📌 Fill each `## Decision`, then `/4_grille` again — 🔴 **only those readings run** |
| The **assembleur** wrote one | 📌 Fill its `## Decision`, then `/4_grille` again — 🔴 **the merge alone runs**, on the four files still standing |
| **First time** — its questions file holds questions | 📌 **Answer them, then `/1_lexique`** — 🔴 it settles the vocabulary your answers brought, before the Rédacteur reads them |
| **First time** — its questions file is empty | 📌 **`/4_grille` again** — 🔴 **the second time runs** |
| **Second time** — `questions-existant-NN.md` holds questions | 📌 **Answer them, then `/1_lexique`** — ⚠️ **an arbitration becomes a block, like any other answer** |
| **Second time** — it is empty, or had already run | 📌 `/5_reclasse` — 🔴 the product file is closed |

🔴 **Nothing else is yours**: no reading of what the questions say.

**If an agent returns a `blocked_*.md`**: relay it and stop.
