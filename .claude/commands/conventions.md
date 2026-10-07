---
description: Derive the project's technical conventions from the two documents
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `architecte`.**

📌 **It can run more than once.** If a hole could not be filled, the
agent writes `questions-architecte-NN.md`; answering and re-running
turns each answer into a rule.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/<first argument>/` — 🔴 **the first
argument only**; ⚠️ **`$ARGUMENTS` holds both when a second names a
`bugfix-NN`.**

🔴 **Invocations 1, 2 and 4 run on the feature folder, never on a
`bugfix-NN/`.** Conventions are derived from a feature's own two
documents, and a correction cycle has neither.

📌 **Invocation 3 runs where the request was written** — the feature
folder, or a `bugfix-NN/` inside it. **A second argument names it.**

---

## What you read

**Whether the files are there** — `spec-technique.md`,
`couverture.md`, `docs/TECHNICAL_CONVENTIONS.md`, and
`questions-architecte-*.md` at the root — 🔴 **plus two greps on that
last one**: `Answer:` lines with nothing after them, and `^### Q`.

**Three greps on `docs/TECHNICAL_CONVENTIONS.md`**, when it is there —
🔴 **one per table that declares the project's structure**:
`^\| *Name *\| *Command *\|` for G2.1's, `^\| *Module *\| *Builds as *\|`
for G4.4's, `^\| *Fact *\| *Value *\|` for G12.6's.

**Two things of `blocked_architecte.md`, when the working folder holds
one, and nothing more of it** — 🔴 **whether its `## Decision` is
filled, and its `## Invocation` line.** 📌 **The walk below keys on
both.**

**Whether each request in `architecte/` carries a filled
`## Verdict`** — 🔴 **a request with no `## Verdict` heading at all
reads as one with an empty one.**

⚠️ **Counts, never content** — 📌 **you never open a questions file,
and you read no more of a blocking file or a request than the lines
named above.**

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## When it runs

📌 **After `/6_convertit`, before `/batir`.** The Bâtisseur builds what
they declare, and the Cadreur reads them in full; they have to exist
when either does.

⚠️ **Run by hand** — 🔴 **no command chains it**: 📌 **it sits between
`/6_convertit` and `/batir`**, and the Product Owner runs it there.
⚠️ **`/batir` sends here** when the conventions lack the project's
structure.

🔴 **Stop if `spec-technique.md` is absent** — say so: `Next: stop
spec-technique.md missing`. The agent derives
from it, and the upstream loop has not reached it yet. ⚠️ **Invocation 3
does not need it**: it judges a request against the conventions and the
grid.

---

## Which invocation

🔴 **Walk this table from the top and stop at the first row that
matches.**

| The folder holds | What you invoke |
|---|---|
| A `blocked_architecte.md` with an empty `## Decision` | 🔴 **Nothing** — relay it and stop — `Next: answer blocking, then run /conventions <name>` |
| 🔴 **A `blocked_architecte.md` with a filled `## Decision`** | 📌 **The invocation its `## Invocation` line names** — 🔴 **name the file in the prompt** |
| A request in `architecte/` with an empty `## Verdict` — 🔴 **or with no `## Verdict` heading at all** | **Invocation 3 — Requests** |
| 🔴 **A second argument names a `bugfix-NN`, and no row above matched** | 📌 **Nothing to invoke** — say so: ⚠️ **`/8_code` carries on**. 🔴 **The rows below are the feature folder's**: a `bugfix-NN` carries no technical document of its own to walk — `Next: run /8_code <name>` |
| A `questions-architecte-NN.md` at the root with an empty `Answer:` | 🔴 **Nothing** — say which questions wait — `Next: answer questions, then run /conventions <name>` |
| A `questions-architecte-NN.md` at the root, **answered** | **Invocation 2 — Integrating** — 🔴 **name the file in the prompt** |
| 🔴 **No `docs/TECHNICAL_CONVENTIONS.md`** | **Invocation 1 — Deriving** — 📌 **the first derivation this repository ever had** |
| **It exists, and no `couverture.md` at the feature folder's root** | 🔴 **Invocation 4 — Completing** |
| 🔴 **It exists, a `couverture.md` is there, and one of the three greps on it finds nothing** | 🔴 **Invocation 4 — Completing** — ⚠️ **conventions written before the grid declared the project's structure**: 📌 **the walk writes what the file lacks**, and `/batir` waits on it |
| A `questions-architecte-NN.md` at the root with **no `### Q`** | 🔴 **Nothing** — the derivation asked nothing. 📌 **File it and commit — the filing steps of *Git, before invoking*, no worktree — then say `/batir`** — `Next: run /batir <name>` |
| **It exists, and a `couverture.md` is there** | 📌 **Nothing to do** — say `/batir` — `Next: run /batir <name>` |
| Nothing of the sort | 📌 **Nothing to do** — say `/batir` — `Next: run /batir <name>` |

🔴 **The last rows are what stops a silent rewrite.** ⚠️ **Invocation 1
opens no existing conventions file and writes it afresh** — 📌 **every
rule invocation 3 added since would be lost.**

🔴 **The test is the conventions file, never `couverture.md`.** ⚠️
**`couverture.md` is written per feature**, so a second feature has
none — 📌 **and a test on it would send every feature but the first
through invocation 1.**

📌 **`couverture.md` tells something else**: whether this feature has
already been walked. 🔴 **That is the invocation-4 row**, and it is what
makes the command idempotent.

📌 **An integrated questions file leaves the root** — 🔴 **filed right
after invocation 2, inside the worktree before the merge** — see *Git,
once it has reported*. ⚠️ **Left at the root, the next run matches its
row again and integrates the same answers twice**: 📌 **your two greps
cannot tell an integrated file from an answered one waiting**, so no
later run can file it in your place.

🔴 **Give the agent its questions file number in the prompt** — 📌 **the
highest `questions-architecte-NN.md` in the root and in
`questions/architecte/` together, plus one**; ⚠️ **`01` when there is
none.** 📌 **It never lists a folder to find it.**

📌 **Invocation 3 runs on a working folder** — a feature, or a
`bugfix-NN` inside it. ⚠️ **Each cycle holds its own `architecte/`**,
and a request is treated in the cycle that raised it.

---

## Git, before invoking

🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not
`architecte` before touching it** — 📌 **a file holding questions is
not yours to file**: ⚠️ **it waits on an answer, or its answers were
never integrated.** 🔴 **Stop and say which** — `Next: stop <file> waits
on an answer or an integration`. 📌 **The architecte's
own file is the walk's above, not this guard's.**

🔴 **Then file away every root `questions-*.md` whose prefix is not
`architecte`:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every `questions-architecte-*.md` at the root that holds no
`### Q`** — same `git mv`, into `questions/architecte/`. 📌 **Invocations
1 and 4 write their questions file whether they asked or not** — ⚠️
**left at the root, the empty one matches its row at every later run**;
filed here, that row matches on the run right after the derivation and
never again. 📌 **Nothing stays at the root to carry the numbering**: ⚠️
**you give the agent its number in the prompt**, counting the root and
`questions/architecte/` together.

⚠️ **An integrated file is not filed here** — 🔴 **it left the root
inside the worktree, right after invocation 2**: see *Git, once it has
reported*. 📌 **Your greps cannot tell it from an answered file
waiting**, and the walk above would have taken it for invocation 2
before this step ran.

📌 **Create `questions/<agent>/` if it does not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it, and the agent works on a stale file.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local.

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

---

## How it runs

**What you do**: invoke the agent via `Agent()` with the working folder
and which invocation it is — and nothing else beyond what its form
below carries.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

### Invocation parameters

```
Agent(
  subagent_type="architecte",
  model="opus",
  description="conventions <feature>",
  prompt="Working folder: docs/features/<name>/. Invocation 1 — Deriving.
          Your questions file number: NN."
)
```

🔴 **The prompt takes one of four forms** — 📌 **the walk above says
which**:

| Invocation | The prompt |
|---|---|
| 1 — Deriving | `Working folder: docs/features/<name>/. Invocation 1 — Deriving. Your questions file number: NN.` |
| 2 — Integrating | `Working folder: docs/features/<name>/. Invocation 2 — Integrating. Answered file: questions-architecte-NN.md. Your questions file number: NN.` |
| 3 — Requests | `Working folder: <the working folder>. Invocation 3 — Requests. Called by the orchestration.` |
| 4 — Completing | `Working folder: docs/features/<name>/. Invocation 4 — Completing. Your questions file number: NN.` |

📌 **At invocation 2 the prompt names the answered file** — 🔴 **the
agent reads that file and no other**: it never lists a folder to find
it.

📌 **At invocation 3 the working folder is the feature folder, or the
`bugfix-NN/` inside it the second argument names.** 🔴 **The prompt
says who called — `Called by the orchestration.`, never inferred**: the
Architecte behaves differently when the Arbitre calls it.

📌 **A filled `blocked_architecte.md` adds its file name to the form
its `## Invocation` line names.**

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`.**

---

## Git, once it has reported

🔴 **The agent reports having applied a decision → rename its blocking
file, inside the worktree, before the steps below:**

    git mv <folder>/blocked_architecte.md <folder>/blocked_architecte-NN.md

📌 **`NN`: the highest in that folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file** — 🔴 **left at
the unnumbered name, the next run stops on it.** 📌 **Step 1 carries the
rename into the commit** — ⚠️ **done after it, the rename stays out of
the merge and leaves the tree dirty for step 5.**

🔴 **After invocation 2, file the questions file it integrated — the one
the prompt named — into `questions/architecte/`, inside the worktree
before the merge:**

    git mv docs/features/<name>/questions-architecte-NN.md \
           docs/features/<name>/questions/architecte/

📌 **Create `questions/architecte/` if it does not exist.** ⚠️ **Left at
the root, it would read as answered again, and the next run would take
it for invocation 2** — 🔴 **your greps cannot tell an integrated file
from one waiting**, so this run is the only one that knows which it is.
📌 **A new `questions-architecte-NN.md` it wrote stays at the root** — an
answer left a hole open, and it waits on the Product Owner.

**Then — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the rename and the
   filing above are staged, not committed; 📌 **`git merge` takes the
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
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — an unmerged commit is
invisible to whoever reads next.

---

## What you relay

**The agent's own report, and which invocation ran.** 🔴 **Nothing else
is yours**: no reading of the conventions file, no summary of its
rules.

📌 **And the blocking file, when the run left one** — ⚠️ **the Product
Owner would otherwise learn of it from a file listing, at best.**

**What to run next** — 📌 **indications for the Product Owner.**

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.

| The run | Next | `Next:` |
|---|---|---|
| It raised questions | 📌 **Answer them, then `/conventions`** | `Next: answer questions, then run /conventions <name>` |
| It raised a **`conjunction`** question | 📌 **The ordinary case** — 🔴 **the question arose between two entries, each complete on its own, and no grid could have seen the pair**: ⚠️ **answer it, then `/conventions`** — 📌 **the answer becomes a rule, and `couverture.md` carries its line** | `Next: answer questions, then run /conventions <name>` |
| It raised a **product question** | 🔴 **The framing grid did not close the product** — ⚠️ **the Product Owner corrects the product file by hand**: 📌 **the behaviour is built in the next cycle, as a new behaviour** — 🔴 **no upstream turn re-runs** | `Next: manual corriger le fichier produit à la main — le comportement sera construit au cycle suivant` |
| 🔴 **Its product question names `G4.4`** — 📌 **what the application runs on**, its report says so | ⚠️ **The one product answer the Architecte turns into rules** — 🔴 **answer it, then `/conventions`**: 📌 **invocation 2 writes the project's structure from it**, and the Product Owner puts it in the product file too | `Next: answer questions, then run /conventions <name>` |
| It raised an **`inconsistency`** | 🔴 **The technical document is wrong** — 📌 **say which entry**: the fix is upstream, in `/6_convertit`, not here | `Next: run /6_convertit <name>` |
| It raised a **`forme`** question | 🔴 **The framing grid lacks a form, or one keeps producing a useless rule** — ⚠️ **the Product Owner amends the grid herself**, the grid's `R4`: 📌 **no rule is written for it**, `couverture.md` says what became of it | `Next: manual amender la grille (R4)` |
| It raised a **`replacement`** question | 🔴 **A rule in force says the opposite of what this feature needs, and lots already coded follow it** — 📌 **replacing a rule in force is the Product Owner's**: ⚠️ **answer it — change the rule, or conform to it — then `/conventions`**. 🔴 **The lots the question names as coded under the old rule are hers to re-enter through `/diagnostique`**, a `bug-list.md` in a `bugfix-NN/` — ⚠️ **the chain has no other way back into coded lots** | `Next: answer questions, then run /conventions <name>` |
| It wrote a blocking file | 📌 **Fill its `## Decision`, then `/conventions`** | `Next: answer blocking, then run /conventions <name>` |
| It asked nothing, or everything is integrated | 📌 `/batir` — 🔴 **the Bâtisseur builds what the conventions declare before any split** | `Next: run /batir <name>` |

📌 **A run raising product questions, one of them on `G4.4`, takes the
`G4.4` row's `Next:`** — ⚠️ **the structure waits on that answer**, and
the others ride the same file.

🔴 **Then list every file the run left in the feature folder**, one line
each, path and size:

    git status --porcelain docs/features/<name>/

📌 **Three of them want the Product Owner's eyes** — the conventions
file, `couverture.md`, and the questions file. ⚠️ **Say which, and say
plainly when the questions file holds questions**: `wc -l` on it tells
you without opening it.

🔴 **A run that wrote a question and did not say so is a run whose
question is lost.** **The Product Owner does not go looking.**

🔴 **The `Next:` line of the table comes after that listing** — ⚠️ **it
is the relay's last line, nothing after it.**
