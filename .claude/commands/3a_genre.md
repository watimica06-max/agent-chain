---
description: Give every product block its genre
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `qualifieur`, once.**

📌 **It runs between `/3_decoupe` and `/3b_nature`, every turn.** 🔴
**Only a `comportement` has a nature, and only it is probed** — ⚠️ **a
block without a genre would be given a nature it does not have, and
probed for what it does not do.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, and nothing else.** 📌 **You never open a block.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Before anything else

🔴 **Does `blocked_qualifieur.md` sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| **Any** `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands, and which `## Blocking N` waits — `Next: answer blocking, then run /3a_genre <name>` |
| **Every** `## Decision` is filled | 📌 **Name it in the prompt** |

⚠️ **One file, several entries** — 📌 **a `## Blocking N` per blocked
block, four headings under each, one `## Decision` each**: 🔴 **they are
not settled together, so you test every one.** 📌 **Grep `-A2
'^## Decision$'`** — a heading followed by nothing but a blank line and
the next heading, or the end of the file, is empty. ⚠️ **Nothing else
is read** — the agent reads the file.

🔴 **Grep `Clarification needed` in `desc-produit.md`.**

⚠️ **One hit and the command stops.** 📌 **Say which blocks carry
one**, and that `/2_structure` has to run first — `Next: run /2_structure
<name>`.

🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not
`architecte` before touching it** — 📌 **a file holding questions is
not yours to file**: ⚠️ **it waits on an answer, or its answers were
never integrated.** 🔴 **Stop and say which** — `Next: stop <file> waits
on an answer or an integration`. 📌 **The qualifieur's own
is no exception** — ⚠️ **answered, it goes through `/1_lexique` and
`/2_structure`**, which integrate it and put it away; 🔴 **still at the
root, it has not been through them.** 📌 **The architecte's is the one
exception** — ⚠️ **it is `/conventions`'s, not this chain's**, and a
`### Q` in it says nothing about the run; 🔴 **read the root as if it
were not there** — and leave it there, see below.

📌 **Filed, a file is read by no command again** — ⚠️ **and its answers
are lost for good** — 🔴 **except under `questions/qualifieur/` and
`questions/classeur/`**, which `/3a_genre` and `/3b_nature` reopen to
give their agent its own last file.

🔴 **File every root `questions-*.md`**, by `git mv`:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there**, or the next command
cannot tell which one waits.

📌 **Create `questions/<agent>/` if it does not exist**; nothing to file
is a normal outcome.

🔴 **Give the agent its questions file number in the prompt** — 📌 **the
highest `questions-qualifieur-NN.md` under `questions/qualifieur/`, plus
one**; ⚠️ **`01` when there is none.** 🔴 **It never lists a folder to
find it** — it has no `Glob`.

🔴 **Then, the questions file it wrote last turn.** 📌 **The highest
`questions-qualifieur-NN.md` under `questions/qualifieur/`, and nowhere
else** — ⚠️ **`/2_structure` files it there when it integrates the
answers**, and the guard above has just stopped on any still at the
root. 🔴 **Name it in the prompt when it holds at least one `### Q`.**

📌 **It applies those answers before it derives** — 🔴 **an answer that
changed no block lands nowhere else.** ⚠️ **Nothing to file after the
run**: the file is already where it belongs, and the one the agent
writes this turn is the root's, until its answers are integrated.

---

## Which blocks it looks at

**Two greps, the union of what they return — and a third trigger, which
names no block:**

| Grep | What it names |
|---|---|
| `grep -B1 '^Genre:$'` | 🔴 **The blocks whose genre is empty** — the line above each hit carries the block |
| `grep '^### .*MODIFIED'` | The blocks changed last turn, whose genre may have moved with them |

🔴 **The third trigger is the answered file** — 📌 **the highest
`questions-qualifieur-NN.md` under `questions/qualifieur/` holds a
`### Q`** → 🔴 **invoke, that file named**, even when the two greps
returned nothing — 📌 **then no block is listed.** ⚠️ **An answer
naming a genre alone changes no block** — the Rédacteur leaves the text
as it was, so no `MODIFIED` marks it and no `Genre:` line is empty; 📌
**the agent finds the blocks its answers name, and it is there that the
genre lands.** 🔴 **What silences the trigger is the agent's own next
file**, empty — filed, it is the highest, and it holds no `### Q`.

📌 **Neither grep returns anything, and that highest file holds no
`### Q` — or there is none** → 🔴 **do not invoke.** 📌 **Commit what
the filing moved, if anything, and push** — no worktree. ⚠️ **Say there
is nothing to qualify**, and go to *What you relay*.

⚠️ **A block with a filled genre and no marker was qualified on an
earlier turn**, and nothing about it has moved since.

🔴 **The empty line is what makes this greppable** — 📌 the Rédacteur
and the decoupeur write `Genre:` with nothing after it, never omit it.

---

## Git, before invoking

🔴 **Commit the feature folder before creating the worktree:**

    git add docs/features/<name>/ && git commit -m "chore: answers"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. The agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.

---

## The invocation

```
Agent(
  subagent_type="qualifieur",
  model="sonnet",
  description="Qualify <name>",
  prompt="The product file: docs/features/<name>/desc-produit.md.
          <Look at these blocks: B7, B62, B63.>
          Your questions file number: NN.
          <Plus: your answered questions file:
           docs/features/<name>/questions/qualifieur/questions-qualifieur-NN.md.>
          <Plus: blocked_qualifieur.md, every ## Decision is filled.>"
)
```

📌 **The `Look at these blocks` line carries what the two greps
returned** — 🔴 **and goes when they returned nothing**: the answered
file alone invoked, and the blocks it names are the agent's to find.

🔴 **Never paraphrase its process** — not the genres, its checks, its
output. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A blocking file you named is renamed only when the agent reports
having written the genre every decision named:**

    git mv docs/features/<name>/blocked_qualifieur.md \
           docs/features/<name>/blocked_qualifieur-NN.md

📌 **`NN`: the highest `blocked_qualifieur-NN.md` in the folder plus one —
`01` when there is none.**

🔴 **It reports, in these words, that a block *waits on the
Rédacteur*** → 📌 **leave the file at its unnumbered name.** ⚠️ **That
decision names a rewrite, and the Rédacteur has not seen it yet**:
`/2_structure` names the file to it at that name, and renames it after
the rewrite. 🔴 **Renamed here, it matches nothing `/2_structure` looks
for**, and the genre stays empty with nothing to explain it.

📌 **You key on the report line, never on the decision** — ⚠️ **your
grep told filled from empty, never what a decision says.** 🔴 **A genre
it could not write for another reason — a value outside the six —
leaves the file at its name too**: the decision has to change first.

⚠️ **A file at the unnumbered name is a block still standing** — 📌
**every command that looks for it finds it there**, and `/2_structure`
is the one that lifts a rewrite.

🔴 **Every stop below merges first.** ⚠️ **The agent has written
its lines in the worktree** — 📌 **stopping before the merge loses the
whole invocation, and a worktree holding unmerged work never
self-cleans.** 🔴 **The five steps of *Git, once it has reported*, and
then report the defect.**

🔴 **Grep `-c '^Genre:$'` in `desc-produit.md`.** 📌 **Zero is what you
expect** — ⚠️ **anything else means a block was left unqualified**, and
you say which.

📌 **Relay which blocks changed genre**, if it says any did — 🔴 **and
the per-block list it reports**, one line per block, the genre it gave.

🔴 **Check `questions-qualifieur-NN.md` was written** — ⚠️ **a missing one is a
defect of the run**: the agent writes one every time. `Next: stop
questions-qualifieur-NN.md missing`

🔴 **Grep `^### Q` in it** and say how many questions it holds.

🔴 **Never read a block to check its work.** 📌 **A wrong `comportement`
is the side downstream sees** — the classeur blocks on a block that
produces nothing, and the sondeurs probe it and find nothing to ask.
⚠️ **A behaviour filed as anything else leaves the file the grid reads,
and nobody downstream catches it** — 🔴 **the per-block list is the only
place the Product Owner can see one before the grid closes.**

---

## Git, once it has reported

**Then, once it has reported — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the rename of *Once it
   has reported* is staged, not committed; 📌 **`git merge` takes the
   branch's commits, not the worktree's files**, and
   `git worktree remove` refuses a dirty tree
2. 🔴 **Leave the worktree** — ⚠️ **a session isolated in a worktree
   cannot issue a git command against the main checkout**: the merge
   below, issued from inside it, is refused
3. `git merge --no-ff <branch>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.**

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.**

🔴 **Merge before handing back, always.** ⚠️ **A `blocked_*.md` merges
too**: the Product Owner has to see it.

---

## What you relay

📌 **How many blocks were qualified**, which changed genre, and how many
questions — 🔴 **and the per-block list, as the agent reports it.**

🔴 **Nothing else is yours**: no reading of what a block says — ⚠️
**relaying a list the agent wrote is not reading a block.**

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.

| What just happened | Next | `Next:` |
|---|---|---|
| It wrote a blocking file — **a genre it could not settle, or two it read in one block** | 📌 Fill every `## Decision`, then `/3a_genre` again — ⚠️ **or the row below that the decision fits** | `Next: answer blocking, then run /3a_genre <name>` |
| It wrote a blocking file **and** a questions file with questions | 🔴 **Answer the questions first, then `/1_lexique`** — 📌 **fill the decision second, once the answers are integrated.** ⚠️ **Both end in the Rédacteur's hands** — at the root together, `/2_structure` takes the answered file and leaves the blocking file for its next run | `Next: answer questions, then run /1_lexique <name>` |
| **Every** `## Decision` names a rewrite | 🔴 **`/2_structure`** — 📌 **it names the blocking file to the Rédacteur, which rewrites the block with `MODIFIED`.** ⚠️ **Then `/3_decoupe`, and back here** — 🔴 **not `/1_lexique`**: the Lexicographe has nothing to watch on a rewrite. ⚠️ **A file mixing genre decisions and rewrites runs `/3a_genre` first** — 📌 **the qualifieur writes the genres, and the file stays at its unnumbered name for `/2_structure`** (*Once it has reported*). 📌 **A block that called for two genres takes this route: the split is the decoupeur's, on the rewritten block.** ⚠️ **A rewrite that still holds two genres blocks again, on the same block** — 🔴 **each turn is a decision she writes, so the repetition is hers to see**: 📌 **a decision that says how to split the block settles it**, the Rédacteur splits what a decision tells it to | `Next: run /2_structure <name>` |
| A `## Decision` names a genre outside the list | 🔴 **Nothing runs** — ⚠️ **the tables have to carry it first**; say so | `Next: stop genre outside the six: <block>` |
| 🔴 **The `^Genre:$` count is non-zero and no blocking file explains it** | 📌 **Say which blocks, and run `/3a_genre` once more** — ⚠️ **once, not until it clears**: 🔴 **a second run that leaves one empty stops there, the blocks named** — a line left empty by neither a block nor a decision is a defect of the run, and a third run would repeat it | First run: `Next: run /3a_genre <name>` · second: `Next: stop <blocks> left unqualified` |
| Its questions file holds questions | 🔴 **Answer them, then `/1_lexique`** — a genre in doubt is settled before the classeur gives a nature | `Next: answer questions, then run /1_lexique <name>` |
| Its questions file is empty, or there was nothing to qualify | 📌 `/3b_nature` | `Next: run /3b_nature <name>` |

**If it returns `blocked_qualifieur.md`**: relay it and stop.
