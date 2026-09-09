---
description: Probe the product file against the framing grid
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `sondeur`, once.**

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

## Which blocks pass A probes

**First turn — no `questions-sondeur-*.md` anywhere:** 🔴 **every
block.** 📌 **Name none in the prompt.**

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

⚠️ **This narrows pass A alone.** 🔴 **Passes B and C run whole every
turn** — 📌 the document changed, and what crosses changed with it.

---

## The invocation

```
Agent(
  subagent_type="sondeur",
  model="opus",
  description="Probe <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          The grid: docs/process/GRILLE_CADRAGE_PRODUIT_V2.md.
          Pass A on these blocks: <B3, B7, B12 — or: every block>.
          Write to docs/features/<name>/cadrage-produit/sondage.md."
)
```

🔴 **Never paraphrase its process in your prompt** — not its inputs,
its checks, its output format. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **Check `cadrage-produit/sondage.md` exists and carries its two
sections** — `## Answers`, `## Questions`.

📌 **A missing file or section stops the command** — say which.

🔴 **Copy its `## Questions` section into `questions-sondeur-NN.md`**
at the feature folder's root.

📌 **Renumber `Q1` upward.** ⚠️ **Everything else is copied as
written** — 🔴 **you rephrase nothing.**

📌 **No question at all** → 🔴 **write the file empty.** ⚠️ **That is
what ends the loop.**

---

## Git, in this mode

🔴 **Before invoking, file every root `questions-*.md` whose prefix is
not `sondeur`:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every `questions-sondeur-NN.md` but the highest** — the last
one stays at the root, it carries the numbering.

🔴 **And the previous turn's `sondage.md`:**

    git mv docs/features/<name>/cadrage-produit/sondage.md \
           docs/features/<name>/cadrage-produit/closed/sondage-NN.md

📌 **Create `questions/<agent>/` and `cadrage-produit/closed/` if they
do not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

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
`origin/master`, which can sit several commits behind local. The agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.
*(Measured on three phases: the agent does the full job, cannot write,
and the whole invocation is redone.)*

🔴 **Then, inside the worktree, create the folder the agent writes
into:**

    mkdir -p docs/features/<name>/cadrage-produit/closed

⚠️ **An agent whose target folder is missing does not stop** — 📌 **it
searches**: it lists the folder, tries an absolute path. 🔴 **Create the
folder and none of that happens.**

**Then, once it has reported:**

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

📌 **How many blocks pass A covered**, and how many questions the file
holds.

🔴 **Nothing else is yours**: no phase chain, no risk level, no
`TaskCreate`, no reading of what the questions say.

**If the agent returns a `blocked_*.md`**: relay it and stop.
