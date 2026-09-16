---
description: Cut a technical document into lots and derive the execution sequence
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **downstream splitting mode**.

**This command runs `cadreur`, once.** 🔴 **It calls the Vérificateur
itself**, corrects what it reports, and calls it again — ⚠️ **three
rounds at most, which it counts.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **The working folder is the highest `bugfix-NN/` in it, if there is
one; the feature folder itself otherwise.** A bug-fix cycle keeps
everything it produces inside its own folder.

📌 **Same structure either way**: the technical document at the root —
`spec-technique.md` or `desc-bug.md` — and `code/` beside it.

📌 **Every path below is relative to the working folder.**

---

## What you read

**`code/sequence.md`** — 📌 **its `## Defects` section**, to know
whether the split holds, **and its headings**, to count the blocks.

**`code/decoupage.md`** — 🔴 **its `## lot-` headings alone**, to count
the lots. ⚠️ **Never a lot's content.**

📌 **Each agent declares its own inputs**; you pass the feature folder
and nothing else.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## How it runs

🔴 **The command is the trigger, never the state of the folder** — 📌
**it produces a split in every state but one.**

⚠️ **What the Cadreur does with an existing one depends on what sits
beside it**, and it is not yours to decide:

| On disk | What it does |
|---|---|
| `code/blocked_cadreur.md`, `## Decision` **empty** | 🔴 **Nothing** — it stops and says the block stands |
| `code/blocked_cadreur.md`, `## Decision` **filled** | 📌 **Applies it**, then carries on with whatever else sits there |
| Nothing | A first split — the whole document |
| `code/sequence.md` whose `## Defects` **carries lines** | 🔴 **Corrects only the lots those defects name** — the rest stays |
| `code/redecoupage.md` | 🔴 **Re-splits what coding sent back** — see below |

📌 **Pass the feature folder; it reads the folder itself.**

⚠️ **Never restore a deleted file from git history.** A missing split
means the Product Owner wants a new one; diagnosing why it went
missing is not your call.

🔴 **Unless `code/redecoupage.md` is there.** 📌 **Then coding sent the
split back**, and lots are already coded and merged — ⚠️ **overwriting
their entries would describe something that is not in the tree.**

🔴 **Say nothing about it in the prompt.** 📌 **The Cadreur dispatches
on what sits on disk** — ⚠️ **a paraphrase competes with its own
instructions**, and this command says so itself.

📌 **They know what to do with it** — the Cadreur leaves the coded lots
closed and adds lots for what has to change, the Vérificateur keeps
them where they ran and archives the file when the sequence is
written.

**One invocation: `cadreur`.** 🔴 **It calls the Vérificateur itself**,
reads the defects, corrects, and calls it again — 📌 **three rounds at
most, which it counts.**

⚠️ **You do not run `verificateur`** — 🔴 **and you do not loop.** 📌
**You invoke the Cadreur once and read what comes back.**

**When it hands back**, look at what is on disk:

| What you find | What you do |
|---|---|
| `code/sequence.md` whose `## Defects` **carries no line** | 🔴 **The split holds.** See *the pending requests*, then stop and report |
| `code/sequence.md` whose `## Defects` **carries lines**, and no blocking file | 🔴 **Stop** — 📌 **relay the defects**: the three rounds did not clear them |
| `code/blocked_cadreur.md` **and** `architecte/cadreur.md` with an **empty** `## Verdict` | 📌 **The conventions fall short**: invoke `architecte`, invocation 3, then invoke `cadreur` again |
| `architecte/cadreur.md` with a **filled** `## Verdict` | 📌 **The Architecte has answered** — 🔴 **invoke `cadreur`**: the verdict is what lifts its block |
| `code/blocked_cadreur.md` alone, `## Decision` empty | 🔴 **Stop.** Relay it — the Product Owner fills `## Decision`, and the Cadreur reads it on its next run |
| The Cadreur reports it **applied** a decision | 🔴 **Rename the file** — 📌 **the agent has no tool that removes one:**<br>`git mv code/blocked_cadreur.md code/blocked_cadreur-NN.md`<br>📌 **`NN`: the highest in the folder plus one, `01` when there is none.** ⚠️ **Anything left at the unnumbered name reads as a block still standing** |
| `code/blocked_verificateur.md` | 🔴 **Stop.** 📌 **Relay which file was missing** — ⚠️ **it carries no `## Decision`**: nothing in it is the Product Owner's to settle, and the step before it has to run again |

📌 **A `blocked_cadreur.md` at the third round** names what would not
converge. ⚠️ **That is not a failure of the command** — 🔴 the split
does not converge, and the Product Owner decides.

### The pending requests

📌 **Once the split holds**, glob `architecte/`. **Any request with an
empty `## Verdict`** → `architecte`, invocation 3.

🔴 **One invocation, whatever their number.** ⚠️ **Then stop** — the
conventions changed after the split was cut, and `/8_code` runs against
both.

```
Agent(
  subagent_type="architecte",
  model="opus",
  description="Requests <the working folder>",
  prompt="Working folder: <the working folder>. Invocation 3 — Requests."
)
```

📌 **If `architecte` blocks in turn** — `blocked_architecte.md` at the
working folder's root — **stop.** 🔴 **It blocks on a missing input,
the conventions file first of all** — ⚠️ **not on the request**: a
doubt or a product matter goes in the verdict. 📌 **Say to run
`/conventions`.**

⚠️ **You never invoke the Arbitre here.** 📌 **What the Cadreur and the
Vérificateur block on is mechanical** — a missing document, an
unreadable list, a convention that forbids what a lot needs. 🔴 **None
of it is settled by looking at the corpus**, and the last one goes to
the Architecte.

🔴 **Never paraphrase an agent's process in your invocation** — not its
inputs, its checks, its output format. It reads its own instructions.

### Invocation parameters

```
Agent(
  subagent_type="cadreur",
  model="opus",
  description="Split <feature>",
  prompt="Working folder: <the working folder>."
)
```

🔴 **Pass the working folder, never the feature folder.** On a bug-fix
cycle they differ, and the agent would read the wrong one.

📌 **`cadreur` runs on `opus`** — it decides the whole structure, and
an error here spreads to every lot. ⚠️ **You never invoke
`verificateur`**: the Cadreur does, with the model its own frontmatter
names.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — 📌 **the Cadreur keeps its context
across the rounds**, and branching would cut it from what it just
cut.

📌 **The Cadreur finds by itself what brought it back** — a
`## Defects` section, or a `code/redecoupage.md`. 🔴 **Say nothing about
it in the prompt**: it reads its own instructions, and a paraphrase
would compete with them.

---

## Git, in this mode

🔴 **File away every root `questions-*.md` first** — the upstream loop
is over and nothing downstream reads them:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **`git mv`, never a read-and-rewrite.** 📌 **Create the folder if it
does not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-split"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

**Then, once the split holds:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — including a
`blocked_*.md`: the Product Owner has to see it.

---

## What you relay

**Where the split stands**: how many lots, how many blocks, and any
defect left. 🔴 **Nothing else is yours** — no risk level, no
`TaskCreate`, no judgement on the split itself, and no reading of git
history to explain what a run found.

**If an agent returns a `blocked_*.md`**: 🔴 **relay it and stop**,
naming the file. 📌 **The Product Owner fills `## Decision`**, and the
Cadreur reads it on its next run.

⚠️ **Except a `blocked_cadreur.md` with an `architecte/cadreur.md`
beside it** — 📌 that one goes to the Architecte, and the Cadreur runs
again.
