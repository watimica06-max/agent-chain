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

Feature folder: `docs/features/<first argument>/` — 🔴 **the first
argument only**; `$ARGUMENTS` holds both.

🔴 **The working folder is the highest `bugfix-NN/` in it, if there is
one; the feature folder itself otherwise.** A bug-fix cycle keeps
everything it produces inside its own folder.

📌 **Same structure either way**: the technical document at the root —
`spec-technique.md` or `desc-bug.md` — and `code/` beside it.

📌 **Every path below is relative to the working folder.**

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

📌 **No such lot** — every one carries a PASS — 🔴 **go straight to the
Contrôleur**, then stop. ⚠️ **That is the normal shape of a run
restarted after a stop on the last lot.**

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

**5. Look for `stop.md` at the feature folder's root** — 🔴 **from the
main checkout, never from a worktree**: a worktree holds a copy frozen
at its creation and would never see a file created after it.

📌 **Present → stop here**, whatever lots remain. **The lot just
finished is merged and pushed; nothing is lost.** ⚠️ **Say how many
lots remain and that the stop was asked for** — a stop is not a
failure.

📌 **Absent → next lot.**

🔴 **`stop1.md` is the disarmed form** — the Product Owner renames it
to `stop.md` to halt, and back to resume. ⚠️ **Neither being there is
not an error**: say so and carry on.

**6. At the end of the block** — 🔴 **before the next one, and never
during** — glob `architecte/`. **Any request with an empty
`## Verdict` → `architecte`, invocation 3.**

🔴 **One invocation, whatever the number of requests.** ⚠️ **Never one
per file**: he reads them all before settling any, and two invocations
would write the conventions file at once.

⚠️ **Never while a lot is running.** 📌 **The conventions file is what
every agent of the next block reads**, and two worktrees writing it at
once lose one of the two.

📌 **A stop at move 5 skips this**, like a block does — the pending
requests wait for the next run, on the block they belong to.

📌 **No request, or every verdict filled** — carry on without invoking
anything.

**When every lot of the sequence carries a PASS** → **`controleur`**,
then stop.

🔴 **Only on a feature cycle.** On a bug-fix cycle — the working folder
carries `desc-bug.md` — **skip him and stop**: he compares the product
file to the sheets, and there is no product file here.

🔴 **Every lot of the sequence, not every lot of this run.** `N` lots
coded with two still pending means no Contrôleur — he compares the
product file to *all* the sheets, and a missing one would make him
report an intention as absent.

📌 **When `N` happens to cover the last lots**, he runs before you hand
back: reaching `N` and finishing the sequence are the same moment.

🔴 **A `stop.md` on the last lot stops before him.** ⚠️ **He reads
every sheet at once**, and a run halted mid-sequence has none to
compare — re-running `/8_code` with no lot left invokes him.

⚠️ **The count is on lots reviewed PASS**, not on invocations: the
Détailleur runs when a new block starts, without entering the count.

🔴 **Never paraphrase an agent's process in your invocation.**

### Invocation parameters

```
Agent(
  subagent_type="realisateur",
  model="sonnet",
  description="Code <lot>",
  prompt="Working folder: <the working folder>. Lot: lot-03."
)
```

🔴 **Name the lot — or the block, for the Détailleur — in the prompt.**
The agent cannot guess which one is his.

🔴 **Pass the working folder, never the feature folder.** On a bug-fix
cycle they differ, and the agent would read the wrong one.

📌 **`detailleur` runs on `opus`**, `realisateur` and `relecteur` on
`sonnet` — the first writes the signatures every lot of the block is
built on, the other two work against a sheet already written.

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

**Before stopping, invoke `arbitre` on it** — 🔴 **except on a
Relecteur or Contrôleur block**, which says something is missing rather
than something to settle.

    Agent(
      subagent_type="arbitre",
      model="opus",
      description="Settle <lot>",
      prompt="Working folder: <the working folder>.
              Blocking files: <their paths in it>."
    )

📌 **Several blocks at once** — 🔴 **one invocation, naming them all.**
⚠️ **Never one per file**: blocks raised together often carry one
cause, and an Arbitre seeing only one settles it too narrowly.

📌 **`## Decision` filled** → run the agent it names again, on the lot
it names, **at the move it blocked on** — a Détailleur block returns to
move 1, a Réalisateur block to move 2. ⚠️ **The relaunch does not count
as a retry**: the lot never failed, it stopped.

📌 **Still empty** → relay it and stop.

🔴 **When you stop on a block, move 6 has not run** — the pending
requests wait for the next `/8_code`, on the block they belong to. ⚠️
**Do not invoke `architecte` on a block that did not finish**: its
lots may still change.

🔴 **One pass per block.** A block the Arbitre handed back does not go
to it twice — even when a later block on the same lot does.

📌 **A filled `## Decision` is not a stop** — invoke the agent it names
on the lot it names, and let it apply the decision. ⚠️ **Even on a lot
already carrying a PASS**: the Contrôleur reports missing intentions
after every lot is reviewed, and a block is how they come back.

🔴 **A lot fails three times.** 📌 **Look for `stop.md` then too** —
say it was asked for, alongside the failure.

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
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — including a `blocked_*.md`.

---

## What you relay

**Which lots passed, and where the run stopped.** 🔴 **Nothing else is
yours** — no judgement on the code, no re-reading of a verdict.

**If you stopped on `stop.md`**: say so, and how many lots of the block
remain. 🔴 **Re-running `/8_code` picks up where you left off** — the
lots already carrying a PASS are not redone.

**If an agent returns a `blocked_*.md`**: relay it and stop.
