---
description: Probe the product file against the framing grid, three readings at once
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `sondeur` three times in parallel, then
`assembleur` once.**

📌 **Three sondeurs read the same document under the same grid, in
three different orders.** 🔴 **The union of what they raise is the
turn's output** — ⚠️ **not what they agree on.**

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

🔴 **Does a `blocked_sondeur.md` or a `blocked_assembleur.md` sit in
the feature folder?**

| | What you do |
|---|---|
| Neither | 📌 Carry on |
| One, its `## Decision` empty | 🔴 **Stop** — say which one still stands |
| One, its `## Decision` filled | 📌 **Name it in that agent's prompt** |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first.

🔴 **A flagged block was transcribed on a reading nobody confirmed** —
📌 **probing it would close a text that is about to change.**

---

## Which blocks pass A probes

**First turn — no `questions-sondeur-*.md` anywhere:** 🔴 **every
block.** 📌 **Name none in the prompts.**

**Later turns — three greps, and the union of what they return:**

| Grep | In | What it names |
|---|---|---|
| `^Block:` | The highest `questions-sondeur-NN.md` | The blocks an answer touched |
| `NEW` | `desc-produit.md` | The blocks created last turn |
| `MODIFIED` | `desc-produit.md` | The blocks changed last turn |

🔴 **A question naming two blocks sends both.** ⚠️ **A `Block: -` names
none** — 📌 what its answer changed carries `MODIFIED`.

⚠️ **This narrows pass A alone.** 🔴 **Passes B and C run whole every
turn.**

📌 **The three sondeurs get the same list.**

---

## The three invocations

🔴 **The three `Agent(...)` calls go in one message.** ⚠️ **Three
messages run them in series** — 📌 they share nothing, and issued
together the wall-clock cost is one sondeur's.

🔴 **Then wait for all three** before anything else.

**They differ by one line, and one line only — their reading order.**

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by block",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Pass A on these blocks: <list — or: every block>.
          Your reading order: block by block, in the document's order.
          Take every grid question to a block before moving to the next.
          Write to docs/features/<name>/cadrage-produit/par-bloc.md."
)
```

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by question",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Pass A on these blocks: <list — or: every block>.
          Your reading order: question by question. Take one grid
          question to every block in scope, then move to the next
          question.
          Write to docs/features/<name>/cadrage-produit/par-question.md."
)
```

```
Agent(
  subagent_type="sondeur", model="opus",
  description="Probe <name>, by nature",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Pass A on these blocks: <list — or: every block>.
          Your reading order: by nature. Gather the blocks of one
          nature, probe them together, then move to the next nature.
          Write to docs/features/<name>/cadrage-produit/par-nature.md."
)
```

🔴 **Never paraphrase a sondeur's process** — not its inputs, its
checks, its output format. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notifications.

❌ **Never pass `isolation`** — 📌 **the three read the same files and
write three different ones**, and none reads what another wrote.

---

## Then the merge

🔴 **Check the three files exist.** 📌 **A missing one stops the
command** — say which, and go no further. ⚠️ **A merge missing one
reading is a merge nobody can trust.**

```
Agent(
  subagent_type="assembleur", model="sonnet",
  description="Merge the three readings of <name>",
  prompt="Merge, in docs/features/<name>/cadrage-produit/:
            par-bloc.md
            par-question.md
            par-nature.md
          Write to docs/features/<name>/cadrage-produit/questions.md."
)
```

---

## Once it has reported

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_<agent>.md \
           docs/features/<name>/blocked_<agent>-NN.md

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **Copy `cadrage-produit/questions.md` to
`questions-sondeur-NN.md`** at the feature folder's root.

📌 **Renumber `Q1` upward.** ⚠️ **Drop its closing `## Merge`
section** — 🔴 it is a working note, not a question.

📌 **Everything else is copied as written** — 🔴 **you rephrase
nothing.**

📌 **No question at all** → 🔴 **write the file empty.** ⚠️ **That is
what ends the loop.**

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

🔴 **And the previous turn's four `cadrage-produit/` files:**

    git mv docs/features/<name>/cadrage-produit/par-bloc.md \
           docs/features/<name>/cadrage-produit/closed/par-bloc-NN.md

📌 **The same for `par-question.md`, `par-nature.md` and
`questions.md`.**

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

**What to run next**

| The questions file | Next |
|---|---|
| Holds questions | 📌 **Answer them, then `/1_lexique`** — 🔴 it settles the vocabulary your answers brought, before the Rédacteur reads them |
| Is empty | 📌 `/5_reclasse` — 🔴 the product file is closed |

🔴 **Nothing else is yours**: no risk level, no
`TaskCreate`, no reading of what the questions say.

**If an agent returns a `blocked_*.md`**: relay it and stop.
