---
description: Settle the vocabulary — the idea file's before the product file is written, then every answered questions file's
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `lexicographe`.**

📌 **It runs before `/2_structure`, and loops** until a questions file
comes out empty. 🔴 **Then the vocabulary is settled**, and the chain
starts.

📌 **It runs again on every answered questions file of the grid or of
the conversion** — 🔴 **before `/2_structure` integrates it.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, and nothing else.** 📌 **You never open the idea file, nor a
questions file's content.**

⚠️ **`CLAUDE.md`'s standing reading rules apply.**

---

## Before anything else

🔴 **Does `blocked_lexicographe.md` sit in the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands — `Next: answer blocking, then run /1_lexique <name>` |
| Its `## Decision` is filled | 📌 **Name it in the prompt** |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

---

## Which invocation

🔴 **What sits at the feature folder's root decides.** 📌 **The name,
never the number.**

| At the root | Invocation |
|---|---|
| No questions file | **1 — Sweeping** |
| `questions-lexicographe` alone, **with no `### Q`** | 🔴 **Invoke nothing** — the loop ended. 📌 **Say so, and say `/2_structure`** — `Next: run /2_structure <name>` |
| `questions-lexicographe` alone | **2 — Settling** |
| Another agent's questions file alone, **with no `### Q`** | 🔴 **Invoke nothing** — 📌 **nothing to watch**; say `/2_structure` — `Next: run /2_structure <name>` |
| Another agent's questions file alone | **3 — Watching** |
| Another agent's, and `questions-lexicographe` **with no `### Q`** | 🔴 **Invoke nothing** — 📌 **3 asked nothing**, and 4 runs only when 3 asked; say `/2_structure` — `Next: run /2_structure <name>` |
| Another agent's, and `questions-lexicographe` | **4 — Correcting** |
| Two files of other agents | 🔴 **Stop** — a filing failed; say which files — `Next: stop filing failed: <files>` |

📌 **Call the other agent's file *the answered file***, whichever agent
wrote it — 🔴 **3 and 4 name it in the prompt.**

🔴 **Never `questions-architecte-*.md`** — ⚠️ **it is never the answered
file, and it counts in no row of the table**: 📌 **it waits at the root
for `/conventions`, which is the only command that reads it.** 🔴 **Read
the root as if it were not there** — and leave it there.

⚠️ **Every command of the cycle files the questions files it does not
read** — 🔴 **which is what keeps these four apart**: the root holds at
most the file waiting on you, and yours.

**A file with an empty `Answer:` and no `Défaut:` line** → 🔴 **stop**,
and say which questions are waiting. `Next: answer questions, then run /1_lexique <name>`

⚠️ **An entry whose `Answer:` is empty **and** that carries a `Défaut:`
line is answered** — 📌 **silence accepts the proposal**, and that is
what the line exists for. 🔴 **Test both**: `^Answer:\s*$` with no
`Défaut:` above it in the same entry.

📌 **After 2, run 1 again** — 🔴 **a settled term can uncover a pair the
first sweep could not see.**

📌 **After 4, the answered file is clean** — 🔴 **unless 4 asked
something itself**: see *What you relay*.

⚠️ **An empty questions file ends a loop.**

🔴 **A `desc-produit.md` in the folder does not stop 3 or 4** — 📌 they
run on every turn of the grid and of the conversion. ⚠️ **It stops 1
and 2**: the vocabulary is settled before the product file exists,
never after — a term changed then would leave sixty blocks carrying the
old one.

🔴 **On that stop, say `/3_decoupe`** — 📌 **the vocabulary is settled
and the idea file is transcribed once**: `/2_structure` stops on the
same state and names the same step. ⚠️ **A stop that names no next step
leaves the Product Owner to guess** — 🔴 **and one that names
`/2_structure` sends her to a command that stops in turn.**
`Next: run /3_decoupe <name>`

---

## Git, before invoking

🔴 **Decide the invocation first** — see *Which invocation*. ⚠️ **This
command is the only one of the cycle that reads a questions file to
decide what it is**: filing before deciding would move the very file
that says it.

🔴 **Then file nothing you have not identified.** 📌 **The root holds at
most two files, and the invocation you just chose names them both**:
the lexicographe's, and the answered one. ⚠️ **A
`questions-architecte-*.md` is neither** — it is `/conventions`'s, and
stays where it is.

⚠️ **Anything else at the root means a filing failed upstream** — 🔴
**stop, and say which files** — `Next: stop filing failed: <files>`. 📌 **Never move one of them**: an
answered questions file put away in `questions/<agent>/` is read by no
command again, and the Product Owner's answers are lost.

📌 **Nothing to file before invoking is the normal case.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and the agent settles nothing.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. *(Seen
once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking**, not after a write fails —
the harness blocks a subagent's writes until the session is isolated.

---

## The invocation

```
Agent(
  subagent_type="lexicographe",
  model="opus",
  description="Sweep <name>'s vocabulary",
  prompt="<At 1 and 2: The idea file: docs/features/<name>/idees.md.>
          <When it exists: The lexicon: docs/features/<name>/lexique.md.>
          Invocation <1 — Sweeping, 2 — Settling,
                       3 — Watching, or 4 — Correcting>.
          <At 2 and 4: The questions file to apply:
           docs/features/<name>/questions-lexicographe-NN.md.>
          <At 3 and 4: The answered file:
           docs/features/<name>/questions-<agent>-NN.md.>
          <Plus: blocked_lexicographe.md, its decision is filled.>
          Write to docs/features/<name>/."
)
```

📌 **The idea file at 1 and 2 only** — ⚠️ **no move of 3 or 4 opens
it**, and the agent reads whole what the prompt names.

🔴 **Its own questions file is named at 2 and 4** — ⚠️ **those
invocations apply it**, and without the name the agent looks for it
where older answered files of the same shape sit.

🔴 **Never paraphrase its process** — not its inputs, its sweeps, its
output format. It reads its own instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

---

## Once it has reported

🔴 **A blocking file you named is filed — once you have told it from a
new one.** ⚠️ **A resumed run can block again, and the agent writes the
same name**: 📌 **grep its `## Decision` first.**

| `## Decision` of `blocked_lexicographe.md` | What you do |
|---|---|
| Still filled | 📌 **The block you named, applied** — file it |
| Empty again | 🔴 **A new block** — 📌 **relay it and stop; file nothing** |

    git mv docs/features/<name>/blocked_lexicographe.md \
           docs/features/<name>/blocked_lexicographe-NN.md

📌 **`NN`: the highest `blocked_lexicographe-NN.md` in the folder plus
one — `01` when there is none.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it — 🔴 **which is exactly what a
new block must do.**

🔴 **After 2 or 4, file the lexicographe's questions file it applied**,
into `questions/lexicographe/`, inside the worktree before the merge —
⚠️ **left at the root, it would read as waiting again**, and the next
run would take it for invocation 2. 📌 **A new
`questions-lexicographe-NN.md` it wrote stays at the root** — an answer
left the choice open, and it waits on the Product Owner.

**After every invocation** — 🔴 **check `lexique.md` exists**, and grep
the lines under `## Non tranché`: 📌 **what still waits on an answer.**
⚠️ **That section alone** — `## Tranché`, `## Tranché sans toi` and
`## Relevé` are not counted.

📌 **Then count the lines under `## Tranché sans toi`, and say how many
there are** — 🔴 **what the Lexicographe settled without the Product
Owner, quotes and words only**: she reads them in `lexique.md` and
overrules one by saying so in a later answer.

**After 1 or 3** — 🔴 **grep `^### Q` in the new
`questions-lexicographe-NN.md`** and count. 📌 **Say how many.**

**After 2 or 4** — 📌 **say whether it wrote a new one**, and how many
entries it holds.

⚠️ **A missing file stops the command** — say which. `Next: stop <file> missing`

🔴 **Never read what a question says.** 📌 **The Product Owner answers
them, not you.**

---

## Git, once it has reported

**Then, once it has reported — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the filings of *Once it
   has reported* are staged, not committed; 📌 **`git merge` takes the
   worktree's commit, not its files**, and
   `git worktree remove` refuses a dirty tree
2. 🔴 **Read the worktree's commit id, then leave it** —
   `git -C <path> rev-parse HEAD`; ⚠️ **a session isolated in a
   worktree cannot issue a git command against the main checkout**:
   the merge below, issued from inside it, is refused
3. `git merge --no-ff -m "<message>" <commit id>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.**

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.**

🔴 **Merge before handing back, always.** ⚠️ **A `blocked_*.md` merges
too**: the Product Owner has to see it.

---

## What you relay

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.

| What just happened | Next | `Next:` |
|---|---|---|
| It wrote a blocking file | 📌 Fill its `## Decision`, then `/1_lexique` again | `Next: answer blocking, then run /1_lexique <name>` |
| 1 asked something | 📌 Answer them, then `/1_lexique` again | `Next: answer questions, then run /1_lexique <name>` |
| 1 asked nothing | 📌 `/2_structure` — 🔴 the vocabulary is settled | `Next: run /2_structure <name>` |
| 2 wrote a new questions file | 📌 Answer it, then `/1_lexique` again | `Next: answer questions, then run /1_lexique <name>` |
| 2 wrote none | 📌 `/1_lexique` again — 🔴 a settled term can uncover a pair | `Next: run /1_lexique <name>` |
| 3 asked something | 📌 **Answer it, then `/1_lexique` again** | `Next: answer questions, then run /1_lexique <name>` |
| 3 asked nothing | 📌 `/2_structure` — 🔴 **3 has already replaced what the lexicon retires**, and nothing waits | `Next: run /2_structure <name>` |
| 4 wrote a new questions file | 📌 Answer it, then `/1_lexique` again | `Next: answer questions, then run /1_lexique <name>` |
| 4 wrote none | 📌 `/2_structure` — 🔴 the answers are settled | `Next: run /2_structure <name>` |

🔴 **Nothing else is yours**: no reading of what a term means.

**If it returns `blocked_lexicographe.md`**: relay it and stop.
