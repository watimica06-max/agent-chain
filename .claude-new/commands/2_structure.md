---
description: Structure the idea file into a product file
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `redacteur`, invocation 1 or 2.**

📌 **It runs as many times as needed.** With no questions file it reads
`idees.md`; with one, it integrates the answers instead.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps and headings, and nothing else:**

- **An `ls` of the feature folder's root** — before the run, and again
  after
- **A grep of `^### Q` in a `questions-lexicographe-NN.md` at the
  root**, when there is one — 📌 **the file the guard of *How it runs*
  bears on, and the one it files**
- **A grep of `^### Q` in the highest-numbered
  `questions-lexicographe-NN.md`, at the root or under
  `questions/lexicographe/`** — 📌 **invocation 1's settled-vocabulary
  test, and nothing else reads it**
- **Two headings of `blocked_redacteur.md`**, when there is one —
  `## Invocation` and `## Decision`, 📌 **those alone**
- **Every `## Decision` heading of a `blocked_decoupeur.md`,
  `blocked_qualifieur.md` or `blocked_classeur.md`**, when there is
  one — 📌 **the headings alone**
- **A grep for an empty `Answer:` with no `Défaut:` line** in the file
  to integrate — 📌 **an entry carrying a `Défaut:` is answered by
  silence**
- **A grep of `^### Q`** in the questions file the agent wrote
- **A grep of `^### .*NEW` and of `^### .*MODIFIED`** in
  `desc-produit.md`, before the run and again after — 📌 **the titles
  the second grep adds are the run's**
- **Whether `code/decoupage.md` exists** in the feature folder — 📌 **a
  test, not a read**

📌 **You pass the agent the file it reads; it does not look for
itself.** 🔴 **You never read a questions file's entries** — the greps
above are counts, not reading.

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Git, before invoking

📌 **The lexicographe's questions file was filed first, or the command
stopped on it** — see *How it runs*.

🔴 **Commit the feature folder**, before creating the worktree:

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
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated. *(Measured on three
phases: the agent does the full job, cannot write, and the whole
invocation is redone.)*

---

## How it runs

**First, a lexicographe's questions file at the root.** 🔴 **Grep it
for `^### Q` before touching it** — ⚠️ **one hit and you stop, answered
or not**: 📌 **its entries were never applied.** `/1_lexique` files the
file it applied, so one still at the root holding entries has not been
through it. Say `/1_lexique` comes next. ⚠️ **The root alone** — 📌 **a
file already under `questions/lexicographe/` holds the entries
`/1_lexique` applied**, and a guard reading it there would stop on a
settled vocabulary after its invocation 4 wrote none. 📌 **None at the
root → nothing to guard**, carry on.

📌 **No `### Q` → file it**, 🔴 **the choice of invocation below reads
the root after it:**

    git mv docs/features/<name>/questions-lexicographe-NN.md \
           docs/features/<name>/questions/lexicographe/

⚠️ **A file put away in `questions/lexicographe/` is opened by no
command again** — 📌 **this one greps the highest for `### Q`, and
nothing more** — ⚠️ **unlike `questions/qualifieur/` and
`questions/classeur/`**, which `/3a_genre` and `/3b_nature` reopen to
give their agent its own last file. ⚠️ **Here again** — 📌 **filing one
still holding entries loses its answers for good.**

⚠️ **`/1_lexique` reads the root to know which invocation it is** — 📌
**a lexicographe file left there and an answered file beside it read as
its fourth**, when its work is done.

📌 **Create `questions/lexicographe/` if it does not exist.** ⚠️
**Nothing to file is a normal outcome.** 📌 **What remains at the root
is the file to integrate — one at most.**

**Then, the Rédacteur's blocking file.** 🔴 **Does `blocked_redacteur.md`
sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Invocation` says **3** | 🔴 **Stop** — 📌 **it is `/fusion`'s**: the merge blocked, not the structuring; say so |
| It says 1 or 2, and its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands |
| It says 1 or 2, and its `## Decision` is filled | 📌 **Name it in the prompt**, beside the file to read |

⚠️ **Read those two headings, nothing else** — 📌 the agent reads the
file. 🔴 **The `## Invocation` line is what routes the file**: ⚠️ **the
Rédacteur has three invocations and one blocking-file name**, and
`/fusion` looks for the same file.

**Then, which invocation and which file:**

| At the root | Invocation | What you name |
|---|---|---|
| **One questions file, holding `### Q`** — any prefix | **2 — Integrating** | 🔴 **That one** |
| **More than one questions file** | 🔴 **Stop** — a filing failed; say which files | — |
| 🔴 **A `blocked_decoupeur.md`, `blocked_qualifieur.md` or `blocked_classeur.md`, every `## Decision` filled** | **2 — Integrating** | 🔴 **That file** — 📌 **all three block on something only a rewrite of the block settles**, and rewriting is yours |
| One of the three with **any** `## Decision` empty | 🔴 **Stop** — say the decision is still to write, and which `## Blocking N` waits | — |
| **One questions file, with no `### Q`** | 🔴 **Invoke nothing** — 📌 **nothing to integrate**; say `/3_decoupe` | — |
| No questions file, **and no `desc-produit.md`** | **1 — Structuring** | `idees.md` |
| No questions file, **and a `desc-produit.md`** | 🔴 **Stop** — 📌 **the idea file is transcribed once**; say `/3_decoupe` comes next | — |

🔴 **First match wins, and the questions file comes before the blocking
files** — 📌 **an answered file and a blocking file at the root
together: the answers go in and the file is filed; the blocking file
waits for the next run**, which finds it alone. ⚠️ **The other way round
dead-ends**: the Rédacteur applying the decision writes its own
questions file beside the answered one, and the next run stops on two.
📌 **A blocking file with an empty `## Decision` waits the same way** —
the stop on the decision comes at the next run. ⚠️ **The empty
questions file sits below the blocking-file rows** — 🔴 **a filled
decision beside a file that asked nothing is taken, not left behind on
"nothing to integrate".**

🔴 **Invocation 1 runs on a settled vocabulary, never before** — 📌
**the highest-numbered `questions-lexicographe-NN.md`, at the root or
under `questions/lexicographe/`, holds no `### Q`.** ⚠️ **None
anywhere, or entries in it → stop**, and say `/1_lexique` comes next.
🔴 **The loop closes on one evidence only** — a run that asked nothing
wrote an empty file, and it is the highest one. 📌 **A term changed
once sixty blocks carry it is sixty edits.**

⚠️ **A second invocation 1 over an existing product file renumbers or
duplicates every block** — 📌 **and every filed question then points at
the wrong one.**

⚠️ **One file, several entries** — 📌 **the qualifieur's and the
classeur's files carry a `## Blocking N` per blocked block, four
headings under each, one `## Decision` each**: 🔴 **they are not
settled together, so you test every one.** 📌 **Grep `-A2
'^## Decision$'`** — a heading followed by nothing but a blank line and
the next heading, or the end of the file, is empty. ⚠️ **Nothing else
is read** — the agent reads the file.

📌 **The file reaches you at that name because `/3a_genre` or
`/3b_nature` left it there** — 🔴 **a decision that names a rewrite
waits on the Rédacteur**, and only this command lifts it; ⚠️ **the
Découpeur's file waits the same way**, and `/3_decoupe` stops on it.

⚠️ **Any prefix** — 📌 the agent integrates the answers whichever agent
asked. 🔴 **Never `questions-architecte-*.md`** — ⚠️ **it is never the
file to integrate, and it counts in no row of the table**: 📌 **it
waits at the root for `/conventions`, which is the only command that
reads it.**

🔴 **If it carries an empty `Answer:` with no `Défaut:` line** — 📌
**stop**, and say which questions are waiting.

⚠️ **An entry whose `Answer:` is empty **and** that carries a `Défaut:`
line is answered** — 📌 **silence accepts the proposal**, and that is
what the line exists for. 🔴 **Test both**: `^Answer:\s*$` with no
`Défaut:` above it in the same entry.

```
Agent(
  subagent_type="redacteur",
  model="sonnet",
  description="Structure <name>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation <1 — Structuring, or 2 — Integrating>.
          Read: <idees.md, or questions-<agent>-NN.md, or
                blocked_<decoupeur|qualifieur|classeur>.md>.
          <Plus: blocked_redacteur.md, its decision is filled.>"
)
```

🔴 **Name the file, always** — ⚠️ **the agent opens that one and no
other.**

### Once it has run

🔴 **Any stop from here on merges first** — ⚠️ **one exception, the
refusal below, which merges nothing by design.** ⚠️ **The agent has
written in the worktree** — 📌 **stopping before the merge loses the
whole invocation**, and a worktree holding unmerged work never
self-cleans. 🔴 **The five steps of *Git, once it has reported*, and
then report.**

🔴 **Did the run create a `NEW` block, or change one?** 📌 **Grep
`'^### .*NEW'` and `'^### .*MODIFIED'` in `desc-produit.md`, and
compare with the same greps before the run** — ⚠️ **anchored on the
title line: a bare `NEW` matches prose inside a block**, and would name
one carrying no marker at all; ⚠️ **compared, because a marker can stand
since an earlier run**: the Rédacteur strips them only when the file it
integrates comes from the grid or the conversion. 📌 **The titles the
second grep adds are the run's.**

🔴 **Then, does `code/decoupage.md` exist?** ⚠️ **The split is cut, and
a lot cites entries by number** — 📌 **the technical document is not
rebuilt behind it**, and `/6_convertit` stops on it.

| `code/decoupage.md` | The run | What you do |
|---|---|---|
| **Exists** | **created a `NEW` block** | 🔴 **Refuse the integration** — below |
| **Exists** | **changed blocks, created none** | 📌 **Delete nothing.** 🔴 **Say that a change to the product now belongs to a new cycle** — the sentence `/6_convertit` says when it stops |
| Absent | **created a `NEW` block** | 🔴 **Delete all four** — below |
| Absent | **changed blocks, created none** | 🔴 **Delete `couverture.md` alone** — below |
| Either | neither | 📌 **Nothing to delete**, a normal outcome |

🔴 **The refusal**: 📌 **a `NEW` block after the split reaches no lot** —
the lots cite entries by number, and the document is not rewritten
under them. ⚠️ **Commit nothing, merge nothing** — leave the worktree,
then:

    git worktree remove --force .claude/worktrees/<name>

📌 **The feature folder is as the run found it** — the answered file, or
the blocking file, at the root, unfiled; `desc-produit.md` without the
block. 🔴 **Say which block the answer created, and that the file is the
Product Owner's to place** — ⚠️ **a change to the product now belongs to
a new cycle, and where the answer goes is hers to decide**; 📌 **left
where it is, the next run takes it again and refuses again.** 🔴 **Stop
there** — nothing below runs.

🔴 **The deletions**, when `code/decoupage.md` is absent:

    rm -rf docs/features/<name>/par-genre/ \
           docs/features/<name>/desc-par-nature.md \
           docs/features/<name>/spec-technique.md \
           docs/features/<name>/couverture.md

📌 **On `MODIFIED` alone, the last line only.** 📌 **Nothing there →
nothing to delete**, a normal outcome.

⚠️ **Why**: all four are derived from the product file — 📌 **the
fourth through the technical document it walks.** 🔴 **A block created
after the conversion leaves a `spec-technique.md` that does not carry
it** — the split and the coding then run on a technical document
missing a block, and the gap surfaces at the controleur. 🔴 **And a
`couverture.md` left behind says the feature was walked** — ⚠️
`/conventions` then finds nothing to do, instead of walking the rebuilt
document at its invocation 4. 📌 **A block changed is a section
re-converted, and a re-converted section is a rebuilt document** — 🔴
**the `couverture.md` reason holds for it**; the three others stay on
`NEW` alone, `/5_reclasse` replacing its files whole and `/6_convertit`
re-converting a changed nature.

🔴 **Say which files you deleted**, or that none needed it.

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_redacteur.md \
           docs/features/<name>/blocked_redacteur-NN.md

📌 **`NN`: the highest `blocked_redacteur-NN.md` in the folder plus
one — `01` when there is none.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **A `blocked_decoupeur.md`, `blocked_qualifieur.md` or
`blocked_classeur.md` it applied is renamed** — `blocked_<agent>-NN.md`,
the highest of that name in the folder plus one. 📌 **Whichever of the
three you named** — ⚠️ **never the Découpeur's alone**: `/3a_genre` and
`/3b_nature` left theirs at the unnumbered name for this command, and
rename nothing after a rewrite. ⚠️ **Left at the unnumbered name it
reads as a block still standing**, and `/3_decoupe`, `/3a_genre` or
`/3b_nature` stops on it.

🔴 **It wrote a blocking file: file nothing** — 📌 **it integrated
nothing.** ⚠️ **Filed, the questions would be out of reach when the
decision comes back.**

🔴 **At invocation 2, file the questions file it integrated**, into
`questions/<agent>/`, inside the worktree before the merge — 📌
**integrated, it waits for nothing**; ⚠️ **left
at the root beside the Rédacteur's own, the next command could not tell
which one waits.** 📌 **A `questions-architecte-*.md` at the root
stays there** — 🔴 **you named it to nothing**, and `/conventions` is
waiting for it.

🔴 **Check `questions-redacteur-NN.md` was written** — ⚠️ **a missing one
stops the command**: the agent says it writes one every time.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are sequential
and each reads what the previous one wrote.

---

## Git, once it has reported

**Then, once the agent reports — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the filings of *Once it
   has run* are staged, not committed; 📌 **`git merge` takes the
   branch's commits, not the worktree's files**, and
   `git worktree remove` refuses a dirty tree
2. 🔴 **Leave the worktree** — ⚠️ **a session isolated in a worktree
   cannot issue a git command against the main checkout**: the merge
   below, issued from inside it, is refused
3. `git merge --no-ff <branch>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — a phase whose output sits on
an unmerged branch is invisible to the next one. ⚠️ **A
`blocked_*.md` merges too**: the Product Owner has to see it. 📌 **The
one run that merges nothing is the refusal of *Once it has run*** — it
has nothing to hand on, and its worktree is already gone.

---

## What you relay

The agent's own report.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

🔴 **First match wins:**

| What just happened | Next |
|---|---|
| The integration was refused — a `NEW` block after the split | 🔴 **Nothing runs** — 📌 **the file at the root is the Product Owner's to place**; say which block the answer created |
| It wrote a blocking file | 📌 Fill its `## Decision`, then `/2_structure` again |
| Its questions file holds questions | 🔴 **Answer them, then `/1_lexique`** — a flag stands until answered, and nothing downstream runs meanwhile |
| Its questions file is empty | 📌 `/3_decoupe` — 🔴 a new block is split, classed and framed before the Convertisseur reads it |

📌 **A blocking file waited at the root while the answers went in** —
🔴 **say so, whichever row matched**: `/2_structure` takes it once the
root holds no answered file.

🔴 **Nothing else is yours**: no phase chain.

**If it returns a `blocked_*.md`**: relay it and stop.
