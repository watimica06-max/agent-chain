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

**`code/sequence.md`, and only its `## Defects` section** — to know
whether the split holds. Each agent declares its own inputs; you pass
the feature folder and nothing else.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## How it runs

🔴 **This command always produces a split.** An existing
`code/decoupage.md` or `code/sequence.md` is overwritten — **the
command is the trigger, never the state of the folder.**

⚠️ **Never restore a deleted file from git history.** A missing split
means the Product Owner wants a new one; diagnosing why it went
missing is not your call.

🔴 **Unless `code/redecoupage.md` is there.** 📌 **Then coding sent the
split back**, and lots are already coded and merged — ⚠️ **overwriting
their entries would describe something that is not in the tree.**

**Say so in the prompt of both agents**, and name the file:

    A code/redecoupage.md is present: coding sent the split back.
    Read it before anything else.

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
| `code/sequence.md`, no `## Defects` | 🔴 **The split holds.** See *the pending requests*, then stop and report |
| `code/blocked_cadreur.md` **and** `architecte/cadreur.md` | 📌 **The conventions fall short**: invoke `architecte`, invocation 3, then invoke `cadreur` again |
| `code/blocked_cadreur.md` alone | 🔴 **Stop.** Relay it — the Product Owner fills `## Decision`, and the Cadreur reads it on its next run |
| `code/blocked_verificateur.md` | 🔴 **Stop.** There was nothing to check |

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

📌 **If `architecte` blocks in turn** — `blocked_architecte.md` —
**stop.** 🔴 **It asks for a rule nobody has written.**

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
