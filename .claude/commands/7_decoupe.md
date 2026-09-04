---
description: Cut a technical document into lots and derive the execution sequence
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **downstream splitting mode**.

**This command runs `cadreur`, then `verificateur`, until the split
holds.**

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

**1. `cadreur`** — produces `code/decoupage.md`.

🔴 **If it wrote `blocked_cadreur.md` and `architecte/cadreur.md`
together**, the conventions fall short of what the split needs:
**invoke `architecte`, invocation 3**, then run `cadreur` again. ⚠️
**The blocking file goes; the request stays with its verdict.**

📌 **If `architecte` blocks in turn** — `blocked_architecte.md` —
**stop.** The Product Owner settles it.

📌 **A request written without a blocking file changes nothing here** —
the Cadreur cut against the conventions as they stand, and the request
waits for the end of the run.

**2. `verificateur`** — produces `code/sequence.md`.

**3. Read its `## Defects` section.**

| It holds | What you do |
|---|---|
| Nothing | 🔴 **The split holds.** If `architecte/` holds a request with an empty `## Verdict`, invoke `architecte`, invocation 3. Then stop and report |
| Defects | Back to `cadreur`, then `verificateur` again |

🔴 **Three rounds maximum.** On the third round still carrying defects,
**write `code/blocked_verificateur.md`**, then stop.

| Heading | What goes in |
|---|---|
| `## What blocks` | The defects still standing, and what each agent held to across the rounds |
| `## Where` | The lots and the entries they cite |
| `## To resume` | What the Product Owner has to settle |
| `## Decision` | 🔴 **Left empty** |

⚠️ **A report in the console is lost; a file is not.** 📌 **The
Cadreur reads it on his next run** — a filled `## Decision` is a split
instruction.

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

🔴 **Pass the working folder, never the feature folder.** On a bug-fix
cycle they differ, and the agent would read the wrong one.
```

📌 **`cadreur` and `verificateur` run on `opus`** — they decide the
whole structure, and an error here spreads to every lot.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the two phases are sequential and the
second reads what the first wrote.

📌 **On a take-back, say so in the prompt**: `"Feature folder: … . The
Vérificateur reported defects in code/sequence.md."`

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

**If an agent returns a `blocked_*.md`**: relay it and stop.
