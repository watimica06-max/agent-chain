---
description: Code the pending lots of a split, one by one, through detail, realisation and review
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name> [N]"
---

Act as the orchestrator, in **downstream coding mode**.

**This command runs `detailleur`, `realisateur` and `relecteur` lot by
lot, then `controleur` when every lot has passed.**

**The first argument is mandatory**: the feature folder name. Without
it, ask for it and stop.

**The second is optional**: how many lots to code. 🔴 **One by
default.**

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

**`code/sequence.md`** — the order, the blocks, and its `## Defects`
section.

**`code/<lot>/verdict.md`** — its `## Status` line only, to find where
to resume.

📌 **Nothing else.** Each agent declares its own inputs.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## Where to resume

🔴 **The next lot is the first in the sequence with no `verdict.md`
carrying PASS.** A read, not a scan — the sequence holds the order.

⚠️ **If `## Defects` is not empty**, stop: the split was never
corrected. Run `/7_decoupe` first.

---

## The loop, per lot

**1.** If the lot's block has no sheets → **`detailleur`** on that
block.

**2.** **`realisateur`** → **`relecteur`**.

**3.** On FAIL → a **fresh `realisateur`**, with the verdict. 🔴 **Three
retries maximum per lot**, all FAIL types counted together.

**4.** ⚠️ **If the verdict names lots affected by a divergence** →
**`detailleur`** on the block, to rewrite those sheets only. Say which
lots in the prompt.

**5.** Next lot.

**When every lot of the sequence carries a PASS** → **`controleur`**,
then stop.

🔴 **Every lot of the sequence, not every lot of this run.** `N` lots
coded with two still pending means no Contrôleur — he compares the
product file to *all* the sheets, and a missing one would make him
report an intention as absent.

📌 **When `N` happens to cover the last lots**, he runs before you hand
back: reaching `N` and finishing the sequence are the same moment.

⚠️ **The count is on lots reviewed PASS**, not on invocations: the
Détailleur runs when a new block starts, without entering the count.

🔴 **Never paraphrase an agent's process in your invocation.**

### Invocation parameters

```
Agent(
  subagent_type="realisateur",
  model="sonnet",
  description="Code <lot>",
  prompt="Feature folder: docs/features/<name>/. Lot: lot-03."
)
```

🔴 **Name the lot — or the block, for the Détailleur — in the prompt.**
The agent cannot guess which one is his.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are
sequential and each reads what the previous one wrote.

---

## Where you stop and hand back

🔴 **A `blocked_*.md` whose `## Decision` is still empty**, wherever it
sits — 📌 **two places**: `code/blocked_<agent>.md` for the Contrôleur,
`code/<lot>/blocked_<agent>.md` for the other three.

📌 **A filled `## Decision` is not a stop** — invoke the agent it names
on the lot it names, and let it apply the decision. ⚠️ **Even on a lot
already carrying a PASS**: the Contrôleur reports missing intentions
after every lot is reviewed, and a block is how they come back.

🔴 **A lot fails three times.**

🔴 **`N` lots have been reviewed PASS.**

🔴 **The Contrôleur has finished** — the gap report is to be read.

⚠️ **Otherwise you never stop.** An isolated FAIL, a finished block, a
fix that passes: carry on.

---

## Git, in this mode

🔴 **Commit the feature folder first**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-code"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded.

📌 **One worktree for the whole run**, not one per lot. Enter it before
invoking anything.

⚠️ **The `realisateur` commits inside it, lot by lot.** That is his;
you do not commit for him.

**When the run ends:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git worktree remove <path>`

🔴 **Merge before handing back, always** — including a `blocked_*.md`.

---

## What you relay

**Which lots passed, and where the run stopped.** 🔴 **Nothing else is
yours** — no judgement on the code, no re-reading of a verdict.

**If an agent returns a `blocked_*.md`**: relay it and stop.
