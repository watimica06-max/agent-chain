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
it, ask for it and stop. `Next: stop argument missing`

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
heading — ⚠️ **or, on a file with no such heading, whether
`## Decision` holds anything** — **and the `## Invocation` line of the
Architecte's**, nothing more of it. 📌 **The two shapes are told apart
under 4b.**

**`code/<lot>/conception.md` and `code/<lot>/tests.md`** — 🔴 **their
`## Decision applied` field alone**: it is where the Concepteur and the
Testeur say they applied a decision. 📌 **The Réalisateur says it under
`## What governed the code, besides the sheet` of
`code/<lot>/compte-rendu.md`** — that field alone of it.

📌 **Nothing else.** Each agent declares its own inputs.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Where to resume

🔴 **First, a look**: 📌 **an unnumbered `code/<lot>/blocked_*.md`
whose `## Decision` is filled, on a lot already carrying a PASS** — ⚠️
**that lot runs first**: its agent invoked with the file named, then
its review again, as *Where you stop and hand back* says of a filled
decision. 🔴 **Then the read.**

🔴 **The next lot is the first in the sequence with no `verdict.md`
whose `## Status` starts with `PASS`.** 📌 **The `PASS` prefix, as
every reader matches it** — `PASS with reservation` is a PASS. A read,
not a scan — the sequence holds the order.

📌 **No such lot** — every one carries a PASS — 🔴 **there is nothing
left to run: stop, and say `/9_controle` comes next** —
`Next: run /9_controle <name>`. ⚠️ **That is the
normal shape of a run restarted after a stop on the last lot.**
🔴 **You never invoke the Contrôleur yourself** — see the head of this
file.

⚠️ **If `## Defects` is not empty**, stop: the split was never
corrected. Run `/7_lots` first — `Next: run /7_lots <name>`.

⚠️ **If `code/blocked_verificateur.md` is there**, stop the same way:
📌 **the Vérificateur writes it when an input it needs is missing**,
and the split it could not check is not one to code against. 🔴 **It
carries no `## Decision`** — nothing in it is the Product Owner's to
fill; `/7_lots` retires it and runs the step before it again. Run
`/7_lots` first — `Next: run /7_lots <name>`.

🔴 **`blocked_architecte.md` is the Architecte's, and only invocation 3
runs here** — 📌 **its `## Invocation` line naming 3, name the file in
the move-7 prompt**, and rename it at the root once the Architecte
reports having applied it. ⚠️ **Naming another invocation, it is
`/conventions`'s**: stop, and say to run it — `Next: run /conventions
<name>`.

🔴 **Then the two stop rows of 4b, before the commit** — 📌 **on the
lot found above, or the one *First, a look* runs, on
`code/blocked_detailleur.md` and on `blocked_architecte.md`**: ⚠️ **a
block an earlier run left standing stops here**, before anything
changes. 📌 **The loop runs 4b again on every later lot** — what an
agent of this run writes is read there.

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
not commit for them. 🔴 **Everything else the run leaves in the
worktree is yours to commit** — 📌 **the sheets, the verdicts, every
blocking file, the renames of 4b, the requests under `architecte/` and
what the Architecte and the Arbitre write outside the feature
folder**: the Détailleur, the Relecteur, the Architecte and the Arbitre
have no Bash, and the three that commit stage their own work only. 🔴
**A request is never a lot's** — it rides no `<lot>:` commit, so no
revert of the lot removes it. ⚠️ **You do it when the run ends** — see
*Git, once it has reported*, whose step 1 enumerates the files —
**and before `/7_lots` at a split-back**, see *When the split comes
back*; never lot by lot.

---

## The loop, per lot

**1.** 🔴 **No `code/<lot>/fiche-executable.md`** → **`detailleur`** on
that lot's block. 📌 **The test is on the lot, never on the block** — ⚠️
**a block half-detailed would pass a test on the block**, and the
Réalisateur would run on a lot with no sheet.

🔴 **No sheet, and a `verdict.md` whose `## Cause` reads `sheet`** — 📌
**read the verdict before invoking: a run before this one reverted the
lot** — ⚠️ **the prompt is then the one of move 4's step 3, its form
under move 5** — `Your lot:` and `Findings:` copied — **never the plain
one.** 📌 **The verdict stays through the sheet path by design**, so
the state reads cold.

**2. Three agents, in this order, on every lot:**

| | |
|---|---|
| **`concepteur`** | 🔴 **Writes the declarations, each body throwing *not implemented*, and compiles** — 📌 **skipped when `code/<lot>/conception.md` is there and no unnumbered `code/<lot>/blocked_concepteur.md` sits beside it** |
| **`testeur`** | 🔴 **Writes one test per criterion, and checks each fails red** — ⚠️ **except a test the declaration alone meets, left green and named under `## Red` of `tests.md`** — 📌 **skipped when `code/<lot>/tests.md` is there and no unnumbered `code/<lot>/blocked_testeur.md` sits beside it** |
| **`realisateur`** | 🔴 **Fills the bodies until the tests pass** — 📌 **skipped when `code/<lot>/compte-rendu.md` is there and no unnumbered `code/<lot>/blocked_realisateur.md` sits beside it**: ⚠️ **a lot coded and not reviewed**, which goes to move 3 |

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

    git log -1 --format=%H --grep='^Revert "<lot>: '
    git log --reverse --format=%H --grep="^<lot>: " <that sha>..HEAD

🔴 **The first command finds the lot's most recent revert** — 📌 **a
`sheet` cause or a redécoupage reverted an earlier coding of the lot**,
and those reverted commits still match the second grep. ⚠️ **The list
is the lot's commits after that revert, none of the reverted ones** —
📌 **no revert found → the whole history**, `<that sha>..HEAD` left
out.

⚠️ **The first line is the lot's first commit** — a blocked run's when
one came before, the concepteur's otherwise. 📌 **The same list is what
the revert of *When the split comes back* and of move 4 works on** —
⚠️ **cut the same way**: a revert reverts one coding, never the
commits an earlier revert already undid. 🔴 **Several lots to revert →
one list**: 📌 **each lot's, cut after its own last revert, merged and
ordered newest first across lots**, reverted in that order — ⚠️ **never
lot by lot**: a later lot's commit sits on an earlier lot's, and
reverting the earlier one first conflicts on the shared lines.

🔴 **The list is never empty on a lot that reached this move** — 📌
**the concepteur's and the testeur's commits fill it** — ⚠️ **so it
cannot tell you whether the Réalisateur committed.** 🔴 **`git
rev-parse HEAD` before invoking the Réalisateur, and again once it has
reported**: 📌 **the same sha is the empty attempt** — the Réalisateur
committed nothing. 🔴 **That counts as a failed attempt, and the
Relecteur is not invoked.** ⚠️ **Increment `## Attempts` yourself
then, on a verdict that already exists** — from an earlier attempt of
this lot: 📌 **nobody else writes on that verdict**, and the count
would stall. 🔴 **No verdict yet → write none**: ⚠️ **a verdict is the
Relecteur's file**, and inventing `## Verified`, `## Findings` and
`## Cause` for a review that never ran is worse than a count held in
this run. 📌 **Count the empty attempt in this run**, and invoke the
fresh `realisateur` with no `Verdict:` line — 🔴 **it takes the lot
from move 1, as a first run.**

📌 **If `code/<lot>/reprise_realisateur.md` is there**, 🔴 **name it in
the Réalisateur's prompt**: a run before it got part of the lot done
and wrote what it left. ⚠️ **Without it, it starts the lot again.**

**4.** On FAIL → a **fresh `realisateur`**, with the verdict, **then the
`relecteur` again on the same lot** — 📌 **one retry is one fix and one
review.** ⚠️ **The new verdict replaces the old**, at the same path.

📌 **`FAIL mineur` and `FAIL structurel` are one FAIL here** — 🔴 **the
form is the Réalisateur's, which reads it to fix the findings or to
take the lot back from its move 1**; ⚠️ **you match the `PASS` prefix,
as every reader does, and branch on `## Cause` alone** — `sheet` below,
`reasoning` for the model.

🔴 **The retry prompt names the verdict** — 📌 **a `Verdict:
code/<lot>/verdict.md` line**, see the form under *The three agents of
a lot*. ⚠️ **Without that line the agent takes the lot as a first
run**: the FAIL case of its Part 2 keys on it.

🔴 **A verdict whose `## Cause` reads `sheet` never reaches a
Réalisateur** — 📌 **the fault is upstream, in the sheet.** What you do,
in this order:

1. 🔴 **Revert the lot's commits** — 📌 **the `git log` list of move 3,
   cut after the lot's last revert, newest first**, `git revert
   --no-edit <sha>` on each. ⚠️ **A conflict takes the later lots
   down** — see the non-last-lot case below
2. 🔴 **Delete `code/<lot>/fiche-executable.md`, `conception.md`,
   `tests.md` and `compte-rendu.md`** — ⚠️ **the verdict stays**: its
   `## Attempts` is the count
3. 🔴 **`detailleur` on the block, in its ordinary mode** — 📌 **the lot
   has no sheet now, so it writes it again** — ⚠️ **with the verdict's
   `## Findings` in the prompt**, a `Findings:` line carrying them
   copied, **and the lot named**. 📌 **A parameter, not a mode**: no
   `Mode:` line with it
4. **Then move 2 on the lot**, as on a lot never coded

📌 **It counts as an attempt** — 🔴 **the Relecteur already
incremented `## Attempts` on that verdict**, and the cap below applies.

⚠️ **A `sheet` cause on a lot that is not the last coded** — 📌 **a lot
already carrying a PASS, re-run on a filled `## Decision`, see *Where
you stop and hand back*** — 🔴 **takes every lot after it in the
sequence down with it**: ⚠️ **their code was built on the signature the
sheet got wrong.** 📌 **Revert their commits and delete their files
too, PASS or not, as *When the split comes back* does for the lots
with no PASS** — 🔴 **one list for every lot concerned, merged as move
3 says**, and `fiche-executable.md`, `conception.md`, `tests.md`,
`compte-rendu.md` and `verdict.md` each. 🔴 **No `/7_lots`**: the split
stands. Step 3 writes the lot's sheet again; move 1 writes the later
lots' when their turn comes, and the loop resumes at the first lot with
no PASS — this one.

⚠️ **A conflict on a lot's revert, here or at *When the split comes
back*, takes the later lots down the same way** — 📌 **a later lot
edited the same lines, so its code rests on the reverted one**: `git
revert --abort`, every lot after it in the sequence joins the list,
PASS or not, and its files go too. 🔴 **You resolve nothing by hand**,
and no git surgery is asked of the Product Owner.

🔴 **`## Attempts` reaching 3 stops the lot** — 📌 **three codings, the
first included.** ⚠️ **Relay the last verdict and stop**: the lot is
the Product Owner's — `Next: stop <lot> failed three times`.

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

📌 **A `## Cause` of `understanding` is the plain retry at the head of
this move, on `sonnet`** — 🔴 **a sheet misread is a coding fault, not
a sheet fault, and only `reasoning` counts toward `opus`**: ⚠️ **neither
the revert above nor the model change.**

**4b.** 🔴 **Before invoking anything on a lot, look for a
`blocked_*.md` in `code/<lot>/`, `code/blocked_detailleur.md`, and
`blocked_architecte.md` at the working folder's root:**

| | |
|---|---|
| **Its `## Decision` is empty** | 🔴 **Stop** — ⚠️ **invoking again re-raises the same block** — `Next: answer blocking, then run /8_code <name>` |
| **Some numbers answered, others not** — 📌 **fewer numbered answers under `## Decision` than `## Blocking N` headings**, on the numbered shape alone | 🔴 **Stop, and do not rename** — ⚠️ **the agent applied the answered ones before it stopped**, and the rest wait on the Product Owner as on an empty `## Decision`. 📌 **A rename would bury the numbers still open** — `Next: answer blocking, then run /8_code <name>` |
| **Filled** — 📌 **by the test of its shape, below** | 📌 **Name it in the agent's prompt**, and 🔴 **rename it once the agent reports having applied it and the file still reads filled** — ⚠️ **the test of its shape run a second time, after the report**, see below:<br>📌 **At the path it sits at** — `code/<lot>/` for the three agents of move 2 and for the Relecteur's, when *Where you stop and hand back* sends you here; `code/` for the detailleur, the working folder's root for the architecte.<br>`git mv code/<lot>/blocked_<agent>.md code/<lot>/blocked_<agent>-NN.md`<br>📌 **`NN`: the highest in that folder plus one, `01` when there is none** |

🔴 **`code/<lot>/blocked_relecteur.md` is not in this table** — 📌 **the
table under *Where you stop and hand back* handles it, row by row**:
the act retires it on three rows, and the Product Owner fills
`## Decision` on the fourth alone. ⚠️ **The first row here would stop
on a file an act retires.**

🔴 **Filled is read by shape, and two shapes reach you:**

- 📌 **A file with `## Blocking N` headings** — the Détailleur's and the
  Réalisateur's, the two the Arbitre settles — 🔴 **is filled when
  every heading has its number**: ⚠️ **a grep of `^## Blocking ` and
  of the numbered lines under `## Decision`**, never the field merely
  holding text. 📌 **An entry still waiting has no number written at
  all** — that is the Arbitre's signal, and the second row reads it
- 📌 **A file with no `## Blocking N` heading** — the Concepteur's, the
  Testeur's and the Relecteur's four `##` headings, the Architecte's
  with its `## Invocation` line — 🔴 **is filled when `## Decision`
  holds anything**: ⚠️ **one block, one answer, nothing to count.** 📌
  **Grep `-A2 '^## Decision$'`** — nothing under the heading is empty

🔴 **The same test runs again once the agent has reported, before the
rename** — 📌 **a `## Blocking N` with no number, or an empty
`## Decision`, is a block the agent raised in the run that applied the
earlier one**, appended below it: ⚠️ **no rename**, the file stays at
its unnumbered name, and you relay it as a block standing.

🔴 **The rename is yours, never the agent's** — 📌 **none of the six has
a tool that removes a file.** ⚠️ **Left at the
unnumbered name, the decision is applied again on every later run**, and
`/9_controle` cannot tell a settled block from a standing one.

📌 **Where the agent says it applied the decision**: 🔴 **the concepteur
in the `## Decision applied` field of `code/<lot>/conception.md`, the
testeur in the same field of `code/<lot>/tests.md`, the realisateur
under `## What governed the code, besides the sheet` of
`code/<lot>/compte-rendu.md`** — a dash there is no application; **the
others in their report.** ⚠️ **The
Détailleur in divergence mode applies only a decision bearing on a lot
the prompt names, and says which numbers it did not apply** — 🔴 **no
rename on that report**: the next ordinary run applies the rest.

📌 **`code/<lot>/reprise_realisateur.md` is renamed the same way**,
🔴 **once the run it was named to has reported** — ⚠️ **the Réalisateur
says it consumed it**:
`git mv code/<lot>/reprise_realisateur.md code/<lot>/reprise_realisateur-NN.md`.
📌 **Left at its name, the next Réalisateur would resume a lot already
resumed.**

🔴 **`code/<lot>/blocked_relecteur.md` is retired as the table under
*Where you stop and hand back* says** — 📌 **by the act on three rows,
by the Relecteur applying a filled `## Decision` on the fourth**:
rename it the same way, at the moment that table names.

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
carries the verdict's findings, the lot they bear on, and no `Mode:`
line:

```
Agent(
  subagent_type="detailleur", model="opus",
  description="Detail <block>, <feature>",
  prompt="Working folder: <the working folder>. Your block: <block>.
          Your lot: <lot>.
          Findings: <the ## Findings of code/<lot>/verdict.md, copied>.
          <Plus: code/blocked_detailleur.md, its decision is filled.>"
)
```

🔴 **The `Your lot:` line names the lot whose sheet you deleted** — 📌
**the Détailleur takes it from the prompt, never as the one it finds
without a sheet**: ⚠️ **a block half-detailed holds other lots with no
sheet**, and the findings would land on the wrong one.

📌 **That rewrite carries its own propagation** — 🔴 **the Détailleur
greps the block's later sheets for every symbol whose signature
changed, and rewrites them as its divergence mode does.** ⚠️ **You run
no divergence call after it**: move 5 is for a final verdict's
`## Symbol divergences`, and a `sheet` FAIL has none.

📌 **You read five fields of a verdict** — 🔴 **`## Status`,
`## Attempts`, `## Cause`, `## Causes so far` and
`## Symbol divergences`.** ⚠️ **Never `## Findings`, except to copy it
into the Détailleur's prompt on a `sheet` cause**: 📌 **what it says is
the fresh Réalisateur's or the Détailleur's to judge, not yours.**

**6. Look for `stop.md` at the feature folder's root** — 🔴 **in the
main checkout, never in the worktree**: 📌 **the Product Owner creates
it there, after the worktree was cut**, and a file created in the main
checkout never reaches a worktree cut before it.

⚠️ **The opposite holds for a `## Decision` she fills while a run is
live** — 📌 **she opens the worktree and answers there**, where the
Arbitre's poll reads the blocking file; 🔴 **a decision written in the
main checkout reaches no agent running in the worktree.** 📌 **Two
files, two places**: `stop.md` in the main checkout, a blocking file
where the agent that wrote it runs.

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
derives the working folder from it as this command does —
`Next: run /9_controle <name>`.

⚠️ **On a bug-fix cycle `/9_controle` reads two folders** — 📌 **phases
1 to 3 run on the feature folder**, whose product file the Contrôleur
confronts with the feature's sheets, the corrected blocks marked
`carried`; 🔴 **phases 4 to 6 run on the working folder**: the manual
list, the register, and the product decisions the Rédacteur needs at
`/fusion`.

⚠️ **Every lot of the sequence, not every lot of this run.** 📌 **`N`
lots coded with two still pending is not a finished sequence** — say
how many remain, and `Next: run /8_code <name>`.

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
          Files the lot's commits changed: <the git diff list>.
          <Plus: code/<lot>/blocked_relecteur.md, its decision is filled.>"
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
problem the split can solve**, and the Product Owner decides. 🔴 **Tell
her where her decision goes** — 📌 **into `code/redecoupage.md` under
`## Décision du Product Owner`, then `/7_lots` by hand**, see *What
resets the count* below: that heading is what the next count keys on.

📌 **Across runs, not within one** — 🔴 **the archived files are the
count**, and a run stopped and resumed does not start it over.

🔴 **Stopping there, you still do everything below but `/7_lots` and
the fresh worktree** — 📌 **the reverts, the deletions, and the five
git steps that close the worktree**: ⚠️ **`code/redecoupage.md` and the
blocking file reach `HEAD` tracked**, where she reads them, and the
tree she runs `/7_lots` on is the one it expects. 🔴 **A stop that
leaves them in an unmerged worktree hands her nothing.**

📌 **What resets the count is hers** — 🔴 **she writes her decision
into `code/redecoupage.md` under a `## Décision du Product Owner`
heading, then runs `/7_lots` by hand**, which archives the file with
that heading inside. ⚠️ **Count only the archived files numbered above
the highest one carrying that heading** — 📌 **a grep of
`^## Décision du Product Owner` across `code/redecoupage-*.md`** — plus
the one now at `code/redecoupage.md`. 🔴 **None carries it → every
archived file counts.**

📌 **What came back and what was done with it is `/7_lots`'s to
relay** — 🔴 **it reads `code/redecoupage.md` before renaming it**; you
relay nothing of it.

🔴 **Revert the commits of every lot with no PASS** — 📌 **the lot
sent back, and every other lot of the sequence whose `verdict.md` is
absent or whose `## Status` does not start with `PASS`**: their code
was written against the old split. ⚠️ **The `git log` lists of move 3,
one per lot, cut after that lot's last revert and merged newest first
across lots as move 3 says**, `git revert --no-edit <sha>` on each — 📌
**a lot already reverted by an earlier run gives an empty list, and
nothing is reverted twice.** 🔴 **A conflict takes every lot after that
one down, PASS or not** — see the conflict rule under move 4, with the
non-last-lot case.

📌 **The Réalisateur restored its own edits before stopping** — 🔴
**`code/redecoupage.md` and the blocking file are not its to drop**:
they stay in the tree, and the commit below carries them.

🔴 **Delete what those lots hold, for every lot with no PASS** — 📌
**`code/<lot>/fiche-executable.md`, `conception.md`, `tests.md`,
`compte-rendu.md` and `verdict.md`.** ⚠️ **The sheets were written
against the old split, the reports describe reverted code, and a
verdict left there would hand its `## Attempts` to a lot cut
differently.** 🔴 **The lot keeps its number** — nothing is renumbered.

⚠️ **Move 1 writes the sheets again** — 🔴 **a Détailleur that finds a
sheet does not rewrite it**, and would detail against a lot that
changed shape. 📌 **Move 2 runs the concepteur and the testeur again the
same way**: their reports gone, they are not skipped.

🔴 **Then close your worktree, before running `/7_lots`** — 📌 **the
five steps of *Git, once it has reported*, in this order:**

1. `git add` and `git commit`, inside the worktree — 🔴 **everything
   the lots coded this run, the reverts, the deletions,
   `code/redecoupage.md` and the blocking file** — 📌 **and the
   requests under `architecte/`, `docs/TECHNICAL_CONVENTIONS.md`, the
   feature folder's `couverture.md` and
   `docs/CURRENT_TECHNICAL_STATE.md`**, as step 1 of *Git, once it has
   reported* says
2. **Read the worktree's commit id, then leave it** —
   `git -C <path> rev-parse HEAD`; the merge is refused from inside it
3. `git merge --no-ff -m "<message>" <commit id>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

⚠️ **`/7_lots` creates its worktree from `HEAD`** — 📌 **and yours sat
outside it**: unmerged, none of this run's lots are in the
`HEAD` it starts from. 🔴 **The Vérificateur would then see no
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
relay what it said, its `Next:` line included — it is this run's last
line. **There is no split to code against.**

---

## Where you stop and hand back

📌 **A Détailleur reporting that its block waits on the split, or a
Réalisateur that its lot does** — 🔴 **`code/redecoupage.md` still
there → *When the split comes back*, from its count**: ⚠️ **a run
stopped before `/7_lots` ran resumes there, never at `/7_lots`
straight** — the count is what a third return stops on, and the
reverts already made give an empty list. ⚠️ **Gone → the blocking file
was never closed**: say which file, and stop — `Next: stop <file> never
closed`.

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
| **`conception.md` or `tests.md`** | 📌 **Relay it and stop** — ⚠️ **move 2 runs the concepteur or the testeur when the file is absent**, so a review reached without it is a fault of the run, not a block to act on. 🔴 **The next run's move 2 writes the file** — that is the act: rename the blocking file once it is there, before invoking the Relecteur — `Next: run /8_code <name>` |
| **Anything else** | 📌 **Relay it and stop** — 🔴 **the Product Owner fills `## Decision`**. ⚠️ **The next run names the filled file in the Relecteur's prompt**, its `Plus:` line, and renames it once the Relecteur reports having applied it — `Next: answer blocking, then run /8_code <name>` |

🔴 **On every row, retiring the blocking file is yours** — 📌 **on the
two act rows once that agent has reported, the act is the answer and
no decision is filled**; on the third once move 2 has produced the
file; on the fourth once the Relecteur reports the decision applied.
The rename is the one of 4b.

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
answered whenever the Product Owner fills it. 🔴 **Its review then
runs again, and a `## Cause` of `sheet` on it takes the later lots
down** — see move 4.

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

**When the run ends — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   Détailleur, the Relecteur, the Architecte and the Arbitre have no
   Bash and commit nothing, and the three that commit stage their own
   work only**: the sheets, the verdicts, every blocking file, the
   renames of 4b and the requests under `architecte/` are still
   uncommitted. 🔴 **So is what sits outside the feature folder** — 📌
   **`docs/TECHNICAL_CONVENTIONS.md` and the feature folder's
   `couverture.md`, the Architecte's invocation 3;
   `docs/CURRENT_TECHNICAL_STATE.md`, the Arbitre's traps** — ⚠️ **a
   `git add` that reaches them all**, never the feature folder alone.
   📌 **`git merge` takes the worktree's commit, not its
   files**, and `git worktree remove` refuses a dirty tree
2. 🔴 **Read the worktree's commit id, then leave it** —
   `git -C <path> rev-parse HEAD`; ⚠️ **a session isolated in a
   worktree cannot issue a git command against the main checkout**:
   the merge below, issued from inside it, is refused
3. `git merge --no-ff -m "<message>" <commit id>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

⚠️ **A worktree still dirty after step 1 refuses a plain remove** — 🔴
**never force it**: 📌 **say what is left there, and stop** —
`Next: stop worktree dirty: <files>`. 📌 **What
is left is something step 1 did not stage** — a fault of this run,
never of an agent: none of them was to commit it. Forcing the removal
destroys it.

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

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.

**If you stopped on `stop.md`**: say so, and how many lots of the block
remain. 🔴 **Re-running `/8_code` picks up where you left off** — the
lots already carrying a PASS are not redone. `Next: run /8_code <name>`

**If an agent returns a `blocked_*.md`**: relay it and stop —
`Next: answer blocking, then run /8_code <name>`.

**If you stopped on a third return**: say so, and where her decision
goes — 🔴 **`code/redecoupage.md`, under a `## Décision du Product
Owner` heading, then `/7_lots` by hand**, see *When the split comes
back*. `Next: manual écrire sa décision sous ## Décision du Product
Owner dans code/redecoupage.md, then run /7_lots <name>`
