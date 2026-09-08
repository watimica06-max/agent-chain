---
description: Probe the product file against the framing grid, block by block then across
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `sondeur-bloc` once per block, then
`sondeur-index`, then `sondeur-feature`.**

📌 **It runs as many times as needed.** Each run writes the next
`questions-sondeur-NN.md`. **An empty one ends the loop**; then run
`/3_reclasse`.

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

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/1_structure` has to run first.

🔴 **A flagged block was transcribed on a reading nobody confirmed** —
📌 **probing it would close a text that is about to change**, and every
question it raised would have to be asked again.

---

## Which blocks are probed

**First turn — no `questions-sondeur-*.md` anywhere:** 🔴 **every
block.**

**Later turns — three greps, and the union of what they return:**

| Grep | In | What it names |
|---|---|---|
| `^Block:` | The highest `questions-sondeur-NN.md` | The blocks an answer touched |
| `NEW` | `desc-produit.md` | The blocks created last turn |
| `MODIFIED` | `desc-produit.md` | The blocks changed last turn |

🔴 **A question naming two blocks sends both.** ⚠️ **A `Block: -` names
none** — 📌 what its answer changed carries `MODIFIED`, and the second
grep finds it.

📌 **A block none of the three names was closed on an earlier turn**
and has not moved since.

---

## The line ranges

🔴 **Grep `^### B` in `desc-produit.md`** — each hit opens a block, and
the block ends on the line before the next hit.

📌 **The last block ends at the file's last line.**

**In the grid, `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md`:**

🔴 **Grep `^# PASS` and `^# C1`** — 📌 the three passes are contiguous,
each is one range.

⚠️ **Never hardcode a line number** — 📌 **the grid changes**, and a
stale range sends an agent into another pass.

**Every agent gets two ranges: how the grid is read — the lines before
`# PASS A` — and its own pass.**

---

## How it runs

### 1. The block pass

🔴 **One `sondeur-bloc` per block to probe, ten at a time.**

```
Agent(
  subagent_type="sondeur-bloc",
  model="sonnet",
  description="Probe <block>",
  prompt="Your block: docs/features/<name>/desc-produit.md,
          lines <from> to <to>.
          The grid, docs/process/GRILLE_CADRAGE_PRODUIT_V2.md:
            lines <a> to <b> — how the grid is read
            lines <c> to <d> — pass A
          Write to docs/features/<name>/cadrage-produit/blocs/<block>.md."
)
```

⚠️ **Wait for each group of ten before launching the next.**

🔴 **After each group, check every file exists and carries its three
sections** — `## Answers`, `## Questions`, `## Index`.

📌 **A missing file or a missing section stops the command** — say
which, and go no further.

### 2. The index

🔴 **Concatenate the `## Index` sections into
`cadrage-produit/INDEX.md`**, one entry per block, in block order.

⚠️ **Copy, never rewrite.** 📌 **You are not judging what an entry
says.**

**On a later turn**, 🔴 **the index already exists**: replace the
entries of the blocks you just probed, add the entries of blocks that
are new, leave the rest untouched.

### 3. The crossings

```
Agent(
  subagent_type="sondeur-index",
  model="sonnet",
  description="Cross the index <name>",
  prompt="The index: docs/features/<name>/cadrage-produit/INDEX.md.
          The grid, docs/process/GRILLE_CADRAGE_PRODUIT_V2.md:
            lines <a> to <b> — how the grid is read
            lines <e> to <f> — pass B
          Write to docs/features/<name>/cadrage-produit/INDEX-questions.md."
)
```

### 4. The feature

```
Agent(
  subagent_type="sondeur-feature",
  model="sonnet",
  description="Probe the feature <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid, docs/process/GRILLE_CADRAGE_PRODUIT_V2.md:
            lines <a> to <b> — how the grid is read
            lines <g> to <h> — pass C
          Write to docs/features/<name>/cadrage-produit/FEATURE-questions.md."
)
```

📌 **Both run whatever the block pass covered** — 🔴 **the index and the
document changed, and their questions are asked afresh every turn.**

### 5. The questions file

🔴 **Assemble `questions-sondeur-NN.md`** at the feature folder's root
— the block pass's questions, then the index's, then the feature's.

📌 **Renumber `Q1` upward across the whole file.** ⚠️ **Everything else
is copied as written** — 🔴 **you rephrase nothing.**

📌 **No question anywhere** → 🔴 **write the file empty.** ⚠️ **That is
what ends the loop.**

🔴 **Never paraphrase an agent's process in your invocation** — not its
inputs, its checks, its output format. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — 📌 **the ten agents of a group each read
a different block and write a different file**, and none reads what
another wrote.

---

## Git, in this mode

🔴 **Before invoking, file every root `questions-*.md` whose prefix is
not `sondeur`:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **`git mv`, never a read-and-rewrite** — the agents must not open
those files, and neither should you.

🔴 **And every `questions-sondeur-NN.md` but the highest** — the last
one stays at the root, it carries the numbering.

🔴 **And the previous turn's block files:**

    git mv docs/features/<name>/cadrage-produit/blocs/<block>.md \
           docs/features/<name>/cadrage-produit/blocs/closed/

📌 **`INDEX.md`, `INDEX-questions.md` and `FEATURE-questions.md` stay
where they are** — the next turn overwrites them.

📌 **`INDEX.md` stays** — it lives from one turn to the next.

📌 **Create `questions/<agent>/` if it does not exist.**

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

📌 **One worktree for the whole command** — 🔴 **every agent runs inside
it**, and it is removed once they have all reported.

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.
*(Measured on three phases: the agent does the full job, cannot write,
and the whole invocation is redone.)*

🔴 **Then, inside the worktree, create the folders the agents write
into:**

    mkdir -p docs/features/<name>/cadrage-produit/blocs/closed

⚠️ **An agent whose target folder is missing does not stop** — 📌 **it
searches**: it lists the folder, reads another agent's output, tries an
absolute path. 🔴 **Create the folders and none of that happens.**

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

📌 **How many blocks were probed**, how many questions the file holds,
and where they came from — block pass, index, feature.

🔴 **Nothing else is yours**: no phase chain, no risk level, no
`TaskCreate`, no reading of what the questions say.

**If an agent returns a `blocked_*.md`**: relay it and stop.
