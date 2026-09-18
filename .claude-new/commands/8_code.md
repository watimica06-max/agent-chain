---
description: Code the pending lots of a split, one by one, through detail, realisation and review
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name> [N]"
---

Act as the orchestrator, in **downstream coding mode**.

**This command runs `detailleur`, `concepteur`, `testeur`, `realisateur`
and `relecteur` lot by lot.**

📌 **It never invokes the Contrôleur** — 🔴 **he needs his blocks and
his sheets named in the prompt**, and the grouping that names them
lives in `/9_controle`.

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

**`code/<lot>/verdict.md`** — 🔴 **four lines**: `## Status`, to find
where to resume · `## Attempts`, the retry count · `## Cause`, to know
whether to escalate, and whether the sheet is what failed ·
`## Causes so far`, to know which model the retry runs on.

**On the final verdict of a lot**, its `## Symbol divergences` field
too.

🔴 **Every `blocked_*.md` of the lot, `code/blocked_detailleur.md` at
the split's root, and `blocked_architecte.md` at the working folder's
root** — 📌 **the Détailleur blocks on a block, not on a lot; the
Architecte on a missing input.** 📌 **Its `## Blocking N` headings and
the numbered answers under `## Decision`** — empty, some, or one per
heading — **and the `## Invocation` line of the Architecte's**, nothing
more of it.

**`code/<lot>/conception.md`** — 🔴 **its `## Decision applied` field
alone**: it is where the Concepteur says it applied a decision.

📌 **Nothing else.** Each agent declares its own inputs.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Where to resume

🔴 **The next lot is the first in the sequence with no `verdict.md`
whose `## Status` starts with `PASS`.** 📌 **The `PASS` prefix, as
every reader matches it** — `PASS with reservation` is a PASS. A read,
not a scan — the sequence holds the order.

📌 **No such lot** — every one carries a PASS — 🔴 **there is nothing
left to run: stop, and say `/9_controle` comes next.** ⚠️ **That is the
normal shape of a run restarted after a stop on the last lot.**
🔴 **You never invoke the Contrôleur yourself** — see the head of this
file.

⚠️ **If `## Defects` is not empty**, stop: the split was never
corrected. Run `/7_lots` first.

---

## Git, before invoking

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

⚠️ **The `concepteur`, the `testeur` and the `realisateur` commit
inside it, lot by lot** — 📌 **each its own work, with a message
reading `<lot>: <what the commit carries>`.** That is theirs; you do
not commit for them.

---

## The loop, per lot

**1.** 🔴 **No `code/<lot>/fiche-executable.md`** → **`detailleur`** on
that lot's block. 📌 **The test is on the lot, never on the block** — ⚠️
**a block half-detailed would pass a test on the block**, and the
Réalisateur would run on a lot with no sheet.

**2. Three agents, in this order, on every lot:**

| | |
|---|---|
| **`concepteur`** | 🔴 **Writes the declarations, each body throwing *not implemented*, and compiles** — 📌 **skipped when `code/<lot>/conception.md` is there and no unnumbered `code/<lot>/blocked_concepteur.md` sits beside it** |
| **`testeur`** | 🔴 **Writes one test per criterion, and checks each fails red** — ⚠️ **except a test the declaration alone meets, left green and named under `## Red` of `tests.md`** — 📌 **skipped when `code/<lot>/tests.md` is there and no unnumbered `code/<lot>/blocked_testeur.md` sits beside it** |
| **`realisateur`** | 🔴 **Fills the bodies until the tests pass** |

⚠️ **Each waits for the one before it.** 📌 **The testeur needs
declarations to call**; the realisateur needs red tests to turn green.

🔴 **A `conception.md` or a `tests.md` beside an unnumbered blocking
file is not a finished run** — 📌 **the agent writes its report before
its blocking file**, so the report is there on a standing block too.
⚠️ **That block goes through 4b**: empty, stop; filled, the agent runs,
named the file, and resumes from its own report.

🔴 **A blocking file from any of the three stops the lot there** — 📌
**the two after it do not run.**

**3.** **`relecteur`**, once the realisateur has reported.

🔴 **The prompt names the files the lot's commits changed** — 📌
**`git diff --name-only <first>^ HEAD`, from the parent of the lot's
first commit to `HEAD`** — ⚠️ **the parent, or the first commit's own
files are left out.** 🔴 **The Relecteur cannot grep a commit**, and
its check on `## Outside the lot` rests on that list.

🔴 **The lot's first commit is found by `git log`** — 📌 **the three
committing agents write `<lot>: <what the commit carries>` as their
message**, so:

    git log --reverse --format=%H --grep="^<lot>: "

⚠️ **The first line is the lot's first commit** — a blocked run's when
one came before, the concepteur's otherwise. 📌 **The same list is what
the revert of *When the split comes back* and of move 4 works on.**

📌 **An empty list means the realisateur committed nothing** — 🔴 **that
counts as a failed attempt, and the Relecteur is not invoked.** ⚠️
**Increment `## Attempts` yourself then, on a verdict that already
exists** — from an earlier attempt of this lot: 📌 **nobody else
writes on that verdict**, and the count would stall. 🔴 **No verdict
yet → write none**: ⚠️ **a verdict is the Relecteur's file**, and
inventing `## Verified`, `## Findings` and `## Cause` for a review
that never ran is worse than a count held in this run. 📌 **Count the
empty attempt in this run**, and invoke the fresh `realisateur` with
no `Verdict:` line — 🔴 **it takes the lot from move 1, as a first
run.**

📌 **If `code/<lot>/reprise_realisateur.md` is there**, 🔴 **name it in
the Réalisateur's prompt**: a run before it got part of the lot done
and wrote what it left. ⚠️ **Without it, it starts the lot again.**

**4.** On FAIL → a **fresh `realisateur`**, with the verdict, **then the
`relecteur` again on the same lot** — 📌 **one retry is one fix and one
review.** ⚠️ **The new verdict replaces the old**, at the same path.

🔴 **The retry prompt names the verdict** — 📌 **a `Verdict:
code/<lot>/verdict.md` line**, see the form under *The three agents of
a lot*. ⚠️ **Without that line the agent takes the lot as a first
run**: the FAIL case of its Part 2 keys on it.

🔴 **A verdict whose `## Cause` reads `sheet` never reaches a
Réalisateur** — 📌 **the fault is upstream, in the sheet.** What you do,
in this order:

1. 🔴 **Revert the lot's commits** — 📌 **the `git log` list of move 3,
   newest first**, `git revert --no-edit <sha>` on each. ⚠️ **A
   conflict stops the command**: `git revert --abort`, say so, and
   resolve nothing
2. 🔴 **Delete `code/<lot>/fiche-executable.md`, `conception.md` and
   `tests.md`** — ⚠️ **the verdict stays**: its `## Attempts` is the
   count
3. 🔴 **`detailleur` on the block, in its ordinary mode** — 📌 **the lot
   has no sheet now, so it writes it again** — ⚠️ **with the verdict's
   `## Findings` in the prompt**, a `Findings:` line carrying them
   copied. 📌 **A parameter, not a mode**: no `Mode:` line with it
4. **Then move 2 on the lot**, as on a lot never coded

📌 **It counts as an attempt** — 🔴 **the Relecteur already
incremented `## Attempts` on that verdict**, and the cap below applies.

🔴 **`## Attempts` reaching 3 stops the lot** — 📌 **three codings, the
first included.** ⚠️ **Relay the last verdict and stop**: the lot is
the Product Owner's.

📌 **No `## Attempts` line in a verdict** — 🔴 **read it as 1** and say
so: a verdict written without it is a defect of the Relecteur.

🔴 **An attempt that committed nothing counts** — 📌 **increment it
yourself in the verdict** when no Relecteur ran and a verdict is there,
⚠️ **or three empty runs would never reach the cap.** 🔴 **No verdict
there → none is written**, see move 3: the empty attempt is counted in
this run.

🔴 **The count lives on disk, not in this run's memory** — 📌 **the
`## Attempts` line of `code/<lot>/verdict.md`**, which the Relecteur
writes. ⚠️ **Otherwise a run stopped for any reason restarts the count
at zero**, and a lot that cannot pass is retried three times per run for
ever. 📌 **The one count held in this run alone is an empty first
attempt** — no verdict exists yet to carry it.

📌 **`## Causes so far` of the last verdict holds `reasoning` twice** →
🔴 **the third realisateur is passed `opus`.** ⚠️ **A reasoning failure
retried on the same model is the retry that fails three times and
stops on the Product Owner.**

**4b.** 🔴 **Before invoking anything on a lot, look for a
`blocked_*.md` in `code/<lot>/`, `code/blocked_detailleur.md`, and
`blocked_architecte.md` at the working folder's root:**

| | |
|---|---|
| **Its `## Decision` is empty** | 🔴 **Stop** — ⚠️ **invoking again re-raises the same block** |
| **Some numbers answered, others not** — 📌 **fewer numbered answers under `## Decision` than `## Blocking N` headings** | 🔴 **Stop, and do not rename** — ⚠️ **the agent applied the answered ones before it stopped**, and the rest wait on the Product Owner as on an empty `## Decision`. 📌 **A rename would bury the numbers still open** |
| **Filled** — 📌 **one answer per `## Blocking N`** | 📌 **Name it in the agent's prompt**, and 🔴 **rename it once the agent reports having applied it**:<br>📌 **At the path it sits at** — `code/<lot>/` for the four agents of the loop, `code/` for the detailleur, the working folder's root for the architecte.<br>`git mv code/<lot>/blocked_<agent>.md code/<lot>/blocked_<agent>-NN.md`<br>📌 **`NN`: the highest in that folder plus one, `01` when there is none** |

🔴 **Count the numbered answers against the `## Blocking N` headings** —
📌 **a grep of `^## Blocking ` and of the numbered lines under
`## Decision`**: ⚠️ **a file is filled when every heading has its
number**, never when the field merely holds text.

🔴 **The rename is yours, never the agent's** — 📌 **none of the six has
a tool that removes a file.** ⚠️ **Left at the
unnumbered name, the decision is applied again on every later run**, and
`/9_controle` cannot tell a settled block from a standing one.

📌 **Where the agent says it applied the decision**: 🔴 **the concepteur
in the `## Decision applied` field of `code/<lot>/conception.md`** — a
dash there is no application; **the others in their report.** ⚠️ **The
Détailleur in divergence mode applies only a decision bearing on a lot
the prompt names, and says which numbers it did not apply** — 🔴 **no
rename on that report**: the next ordinary run applies the rest.

🔴 **`blocked_architecte.md` is the Architecte's, and only invocation 3
runs here** — 📌 **its `## Invocation` line naming 3, name the file in
the move-7 prompt**, and rename it at the root once the Architecte
reports having applied it. ⚠️ **Naming another invocation, it is
`/conventions`'s**: stop, and say to run it.

📌 **`code/<lot>/reprise_realisateur.md` is renamed the same way**,
🔴 **once the run it was named to has reported** — ⚠️ **the Réalisateur
says it consumed it**:
`git mv code/<lot>/reprise_realisateur.md code/<lot>/reprise_realisateur-NN.md`.
📌 **Left at its name, the next Réalisateur would resume a lot already
resumed.**

🔴 **`code/<lot>/blocked_relecteur.md` is retired by the act** — 📌 **a
fresh `realisateur` for the report, the `detailleur` for the sheet**,
see the table under *Where you stop and hand back* — ⚠️ **no decision
is filled**: rename it the same way once that agent has reported.

**5.** ⚠️ **If the lot's final verdict carries `## Symbol divergences`
naming affected lots** → **`detailleur`** on the block, to rewrite those
sheets only:

```
Agent(
  subagent_type="detailleur", model="opus",
  description="Propagate <block>, <feature>",
  prompt="Working folder: <the working folder>. Your block: <block>.
          Mode: divergence.
          Affected lots: lot-07, lot-09.
          <Plus: code/blocked_detailleur.md, its decision is filled.>"
)
```

🔴 **The `Mode:` line is what tells the two apart** — ⚠️ **without it
the agent runs its ordinary mode and skips every lot that has a
sheet**: 📌 **the propagation silently does not happen.**

🔴 **On the final verdict only** — 📌 **never on a FAIL about to be
retried**: the retry may revert the very signature you propagated.

📌 **The ordinary-mode prompt after a `sheet` FAIL** — see move 4 —
carries the verdict's findings and no `Mode:` line:

```
Agent(
  subagent_type="detailleur", model="opus",
  description="Detail <block>, <feature>",
  prompt="Working folder: <the working folder>. Your block: <block>.
          Findings: <the ## Findings of code/<lot>/verdict.md, copied>.
          <Plus: code/blocked_detailleur.md, its decision is filled.>"
)
```

📌 **You read five fields of a verdict** — 🔴 **`## Status`,
`## Attempts`, `## Cause`, `## Causes so far` and
`## Symbol divergences`.** ⚠️ **Never `## Findings`, except to copy it
into the Détailleur's prompt on a `sheet` cause**: 📌 **what it says is
the fresh Réalisateur's or the Détailleur's to judge, not yours.**

**6. Look for `stop.md` at the feature folder's root** — 🔴 **from the
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

**7. At the end of the lot** — 🔴 **before the next one, and never
while one runs** — glob `architecte/`. **Any request with an empty
`## Verdict` → `architecte`, invocation 3.** 🔴 **A request with no
`## Verdict` heading at all reads as an empty one** — it fires the
same.

🔴 **At the end of the lot, not of the block.** ⚠️ **A rule settled a
block late is settled after every lot it should have governed** — 📌
**this way the next lot has it.**

🔴 **One invocation, whatever the number of requests.** ⚠️ **Never one
per file**: he reads them all before settling any, and two invocations
would write the conventions file at once.

📌 **A request the Arbitre raised mid-lot is already settled** — its
`## Verdict` is filled, and this move skips it.

```
Agent(
  subagent_type="architecte",
  model="opus",
  description="Requests <the working folder>",
  prompt="Working folder: <the working folder>. Invocation 3 — Requests.
          Called by the orchestration.
          <Plus: Blocking file: blocked_architecte.md, its decision is filled.>"
)
```

🔴 **`Called by the orchestration.` is never left out** — 📌 **the
Architecte behaves differently when the Arbitre calls it**, and it
infers nothing.

📌 **The `Blocking file:` line only when a filled `blocked_architecte.md`
sits at the working folder's root** — see 4b.

⚠️ **Never while a lot is running.** 📌 **The conventions file is what
every agent of the next block reads**, and two worktrees writing it at
once lose one of the two.

📌 **A stop at move 6 skips this**, like a block does — the pending
requests wait for the next run, on the block they belong to.

📌 **No request, or every verdict filled** — carry on without invoking
anything.

**When every lot of the sequence carries a PASS** → **stop, and say
so.** 🔴 **You never invoke the Contrôleur** — 📌 **it needs a grouping
this command does not hold**, and `/9_controle` builds it.

📌 **Say that `/9_controle <feature>` is what comes next** — 🔴 **run by
hand, on both cycles**, ⚠️ **with the feature name, never a path**: it
derives the working folder from it as this command does.

⚠️ **On a bug-fix cycle `/9_controle` reads two folders** — 📌 **phases
1 to 3 run on the feature folder**, whose product file the Contrôleur
confronts with the feature's sheets, the corrected blocks marked
`carried`; 🔴 **phases 4 to 6 run on the working folder**: the manual
list, the register, and the product decisions the Rédacteur needs at
`/fusion`.

⚠️ **Every lot of the sequence, not every lot of this run.** 📌 **`N`
lots coded with two still pending is not a finished sequence** — say
how many remain.

⚠️ **The count is on lots reviewed PASS**, not on invocations: the
Détailleur runs when a new block starts, without entering the count.

🔴 **Never paraphrase an agent's process in your invocation.**

**The three agents of a lot, in order:**

```
Agent(
  subagent_type="concepteur", model="sonnet",
  description="Declare <lot>",
  prompt="Working folder: <the working folder>. Your lot: <lot>.
          <Plus: code/<lot>/blocked_concepteur.md, its decision is filled.>"
)
```

```
Agent(
  subagent_type="testeur", model="sonnet",
  description="Test <lot>",
  prompt="Working folder: <the working folder>. Your lot: <lot>.
          <Plus: code/<lot>/blocked_testeur.md, its decision is filled.>"
)
```

```
Agent(
  subagent_type="realisateur", model="sonnet",
  description="Code <lot>",
  prompt="Working folder: <the working folder>. Your lot: <lot>.
          <Plus: code/<lot>/reprise_realisateur.md.>
          <Plus, on a retry: Verdict: code/<lot>/verdict.md.>
          <Plus: code/<lot>/blocked_realisateur.md, its decision is filled.>"
)
```

🔴 **The `Verdict:` line on a retry only** — 📌 **it is what tells the
agent it resumes a FAIL**; ⚠️ **on a first run, or after an attempt
that committed nothing, there is none.**

```
Agent(
  subagent_type="relecteur", model="sonnet",
  description="Review <lot>",
  prompt="Working folder: <the working folder>. Your lot: <lot>.
          Files the lot's commits changed: <the git diff list>."
)
```

### Invocation parameters

🔴 **Name the lot — or the block, for the Détailleur — in the prompt.**
The agent cannot guess which one is his.

🔴 **Pass the working folder, never the feature folder.** On a bug-fix
cycle they differ, and the agent would read the wrong one.

📌 **`detailleur` runs on `opus`** — it writes the signatures every lot
of the block is built on. 🔴 **`concepteur`, `testeur`, `realisateur`
and `relecteur` on `sonnet`** — they work against a sheet already
written.

⚠️ **One exception** — 📌 **a third `realisateur` on a lot whose verdict
holds `reasoning` twice in `## Causes so far` runs on `opus`.**

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are
sequential and each reads what the previous one wrote.

---

## When the split comes back

🔴 **A Détailleur's or a Réalisateur's `## Decision` sends the lot back
to the split.** 📌 **The Arbitre wrote `code/redecoupage.md`**, and the
agent stopped — ⚠️ **the Détailleur without writing a sheet, the
Réalisateur after dropping its code.**

🔴 **Count the redécoupages of this feature** — 📌 **the archived
`code/redecoupage-NN.md` files, plus the one now at
`code/redecoupage.md`.** ⚠️ **The count reaching three, you stop instead
of running `/7_lots`**: 📌 **a third round says the split is not the
problem the split can solve**, and the Product Owner decides.

📌 **Across runs, not within one** — 🔴 **the archived files are the
count**, and a run stopped and resumed does not start it over.

📌 **What came back and what was done with it is `/7_lots`'s to
relay** — 🔴 **it reads `code/redecoupage.md` before renaming it**; you
relay nothing of it.

🔴 **Revert the commits of every lot with no PASS** — 📌 **the lot
sent back, and every other lot of the sequence whose `verdict.md` is
absent or whose `## Status` does not start with `PASS`**: their code
was written against the old split. ⚠️ **The `git log` list of move 3
per lot, newest first**, `git revert --no-edit <sha>` on each. 🔴 **A
conflict stops the command**: `git revert --abort`, say so, and resolve
nothing — the Product Owner decides.

📌 **The Réalisateur restored its own edits before stopping** — 🔴
**`code/redecoupage.md` and the blocking file are not its to drop**:
they stay in the tree, and the commit below carries them.

🔴 **Delete what those lots hold, for every lot with no PASS** — 📌
**`code/<lot>/fiche-executable.md`, `conception.md`, `tests.md` and
`verdict.md`.** ⚠️ **The sheets were written against the old split,
the reports describe reverted code, and a verdict left there would
hand its `## Attempts` to a lot cut differently.** 🔴 **The lot keeps
its number** — nothing is renumbered.

⚠️ **Move 1 writes the sheets again** — 🔴 **a Détailleur that finds a
sheet does not rewrite it**, and would detail against a lot that
changed shape. 📌 **Move 2 runs the concepteur and the testeur again the
same way**: their reports gone, they are not skipped.

🔴 **Then close your worktree, before running `/7_lots`** — 📌 **in
this order:**

1. `git add` and `git commit`, inside the worktree — 🔴 **everything
   the lots coded this run, the reverts, the deletions,
   `code/redecoupage.md` and the blocking file**
2. `git merge --no-ff <branch>` from the main checkout root
3. `git push`
4. `git worktree remove <path>`

⚠️ **`/7_lots` creates its worktree from `HEAD`** — 📌 **and yours was
a branch of its own**: unmerged, none of this run's lots are in the
`HEAD` it branches from. 🔴 **The Vérificateur would then see no
`PASS`**, and the Cadreur could re-cut lots already coded.

**Then run `/7_lots` on this working folder**, and wait for it.

🔴 **Then open a fresh worktree from the merged `HEAD`** — 📌 **as
*Git, before invoking* says, commit first** — **and carry on your
loop** in it. ⚠️ **You do not hand back, and the Product Owner is not
waiting on anything.**

🔴 **Where you carry on from is the same rule as always**: the first
lot in the sequence with no `verdict.md` whose `## Status` starts with
`PASS`. ⚠️ **The split changed, the coded lots did not** — their
verdicts are still there, and they are still behind.

📌 **Your count of lots carries on too** — 🔴 **it does not restart.**
`N` counts lots reviewed PASS in this run, and a redécoupage reviewed
none.

⚠️ **If `/7_lots` stops on a defect or a block**, 🔴 **stop too** —
relay what it said. **There is no split to code against.**

---

## Where you stop and hand back

📌 **A Détailleur reporting that its block waits on the split** — 🔴
**`code/redecoupage.md` still there → run `/7_lots`**; ⚠️ **gone → the
blocking file was never closed**: say which file, and stop.

🔴 **A `blocked_*.md` whose `## Decision` is still empty**, wherever it
sits — 📌 **three places:**

- `code/<lot>/blocked_<agent>.md` — 📌 **the concepteur, the testeur,
  the realisateur and the relecteur**
- `code/blocked_detailleur.md` — 🔴 **at the split's root**: it blocks
  on a block, not on a lot
- `blocked_architecte.md` at the working folder's root — ⚠️ **it blocks
  on a missing input**, and the next lot's Détailleur would run against
  conventions that were not amended. 📌 **Filled, it goes through 4b
  like the others** — named in the move-7 prompt, renamed once applied

🔴 **You never invoke the Arbitre.** 📌 **The Détailleur and the
Réalisateur call it themselves**, wait for it, and only stop when the
field came back empty. ⚠️ **A block that reaches you has already been
through it** — sending it again would ask twice.

📌 **The Relecteur does not call it either** — 🔴 its blocks say
something is missing, not something to settle.

| What a Relecteur block names missing | What you do |
|---|---|
| **The report** | 🔴 **A fresh `realisateur`** — 📌 **counted as an attempt** |
| **The sheet** | 🔴 **`detailleur` on the block** |
| **`conception.md` or `tests.md`** | 📌 **Relay it and stop** — ⚠️ **move 2 runs the concepteur or the testeur when the file is absent**, so a review reached without it is a fault of the run, not a block to act on |
| **Anything else** | 📌 **Relay it and stop** |

🔴 **On the two rows you act on, retire the blocking file yourself**
once that agent has reported — 📌 **the act is the answer, no decision
is filled**; the rename is the one of 4b.

⚠️ **Unless a Détailleur's or a Réalisateur's `## Decision` sends the
lot back to the split.** 🔴 **That is not a stop** — see *When the
split comes back*.

📌 **Any other block** → relay it and stop. 🔴 **The Product Owner
fills `## Decision`**, and the next `/8_code` picks it up.

🔴 **When you stop on a block, move 6 has not run** — 📌 **a request
waiting in `architecte/` waits for the next `/8_code`.** ⚠️ **Do not
invoke `architecte` on a lot that did not finish**: what it asks for
may change with the decision.

📌 **A filled `## Decision` is not a stop** — invoke the agent it names
on the lot it names, and let it apply the decision. ⚠️ **Even on a lot
already carrying a PASS**: a block left unsettled on an earlier run is
answered whenever the Product Owner fills it.

🔴 **What the Contrôleur reports never comes back this way** — 📌 **a
missing intention goes into a `bug-list.md` and a correction cycle**,
never into a block on a closed lot.

🔴 **A lot fails three times.** 📌 **Look for `stop.md` then too** —
say it was asked for, alongside the failure.

🔴 **`N` lots have been reviewed PASS.**

⚠️ **Otherwise you never stop.** An isolated FAIL, a finished block, a
fix that passes: carry on.

---

## Git, once it has reported

**When the run ends:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git push`
3. `git worktree remove <path>`

⚠️ **A worktree with uncommitted files refuses a plain remove** — 🔴
**never force it**: 📌 **say what is left there, and stop.** ⚠️ **An
agent handed back leaving work uncommitted is a fault of that agent**,
and forcing the removal destroys it.

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
