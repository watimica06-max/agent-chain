---
description: Build the project skeleton the conventions declare, and prove it builds
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **building mode**.

**This command runs `batisseur`** — 🔴 **and `architecte`, invocation
3, each time the Bâtisseur asks**, then the Bâtisseur again.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **The working folder is the feature folder, always** — ⚠️ **never a
`bugfix-NN/`**: 📌 **the project's structure is the repository's**, and
a correction cycle builds nothing a feature did not declare.

📌 **The argument names the worktree and the commit subject** — ⚠️
**the skeleton and its report are the application's**: one
`docs/BUILD_REPORT.md`, whichever feature built it last.

📌 **Every path below is relative to the working folder**, except one
starting with `docs/` or `.claude/`, relative to the repository's root.

---

## When it runs

📌 **After `/conventions`, before `/7_lots`** — 🔴 **`/conventions`'
successful endings name it**, and ⚠️ **`/7_lots` sends here** when the
project was not built from the conventions in force.

📌 **It can run more than once** — 🔴 **on a project already built it
creates nothing**, and its report says so.

---

## What you read

**`docs/TECHNICAL_CONVENTIONS.md`** — 🔴 **three greps alone**, one per
table's header line — see *Before anything else*. ⚠️ **Never a rule's
content.**

**`blocked_batisseur.md`**, when the working folder holds one — 🔴
**whether its `## Decision` is filled, and its `## To resume`, which you
relay whole** — nothing more of it.

**`architecte/batisseur.md`**, when it is there — 🔴 **whether each
`# Request N` block carries a filled `## Verdict`** — ⚠️ **a block with
no `## Verdict` heading at all reads as one with an empty one.** 📌
**Once the Architecte has answered, each block's `## What I need` and
`## Verdict`**, which you relay.

**`docs/BUILD_REPORT.md`**, the Bâtisseur's report — 🔴 **its
`## Status:` line and its `## Decision applied` section**, once the
Bâtisseur has handed back.

**`blocked_architecte.md`**, when the Architecte leaves one — 🔴 **its
existence alone.**

⚠️ **Nothing else** — `CLAUDE.md`'s standing reading rules apply.

---

## Before anything else

🔴 **Four tests, in this order, before any gesture on the repository:**

| The test fails | `Next:` |
|---|---|
| 🔴 **No `docs/TECHNICAL_CONVENTIONS.md`** | 📌 **The Architecte derives it first** — `Next: run /conventions <name>` |
| 🔴 **It lacks G2.1's, G4.4's or G12.6's table** — 📌 **no match for one of `^\| *Name *\| *Command *\|`, `^\| *Module *\| *Builds as *\|`, `^\| *Fact *\| *Value *\|`** | ⚠️ **The structure was never declared** — 📌 **conventions written before the grid declared it included**: the derivation writes it — `Next: run /conventions <name>` |
| 🔴 **`blocked_batisseur.md` whose `## Decision` is empty** | 📌 **Relay its `## To resume` whole** — ⚠️ **on a build tool it is the Product Owner's tutorial** — `Next: answer blocking, then run /batir <name>` |
| 🔴 **`.claude/worktrees/<name>` already exists** | ⚠️ **A run left it** — 📌 **say what it holds** with `git -C .claude/worktrees/<name> status --porcelain`, and stop — `Next: stop worktree already there: .claude/worktrees/<name>` |

📌 **A `blocked_batisseur.md` whose `## Decision` is filled** — 🔴
**name it in the prompt**: the Bâtisseur applies it.

📌 **A `# Request N` of `architecte/batisseur.md` with an empty
`## Verdict`** — ⚠️ **a run stopped before the Architecte answered** —
🔴 **opens the run on the Architecte**, see *How it runs*.

---

## Git, before invoking

🔴 **Commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-build"

⚠️ **The Product Owner fills `## Decision` by hand, outside this
session** — 📌 **a worktree branches from the last commit**, and an
uncommitted decision is invisible inside it.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local.

📌 **Enter the worktree before invoking an agent**, not after it fails
— the harness blocks a subagent's writes until the session is isolated.

---

## How it runs

🔴 **Before each Bâtisseur invocation, read the conventions commit
inside the worktree:**

    git log -1 --format=%H -- docs/TECHNICAL_CONVENTIONS.md

📌 **It goes in the prompt** — ⚠️ **the Architecte may have changed the
file since the last one**, and the report records the commit the
skeleton was built from.

🔴 **The run opens on the Bâtisseur** — ⚠️ **unless a `# Request N` of
`architecte/batisseur.md` waits on its `## Verdict`**: 📌 **a run
stopped before the Architecte answered**, and the Architecte's step
below comes first.

🔴 **Each time the Bâtisseur hands back, walk this table — first row
that matches:**

| On disk | What you do |
|---|---|
| 🔴 **`blocked_batisseur.md` whose `## Decision` is empty** | 🔴 **Stop** — relay its `## To resume` whole — `Next: answer blocking, then run /batir <name>` |
| 🔴 **A `# Request N` of `architecte/batisseur.md` whose `## Verdict` is empty** | 📌 **The Architecte's step**, below |
| 🔴 **`docs/BUILD_REPORT.md` saying `## Status: built`** | 📌 **The skeleton holds** — `Next: run /7_lots <name>` |
| ⚠️ **`docs/BUILD_REPORT.md` saying `## Status: blocked`, and nothing above** | 🔴 **Stop** — ⚠️ **a blocked run leaves a request or a blocking file**, and this one left neither: say so — `Next: stop the Bâtisseur ended blocked with nothing waiting` |

📌 **The report read is the one this run's Bâtisseur wrote** — ⚠️ **a
`built` left by an earlier run says nothing of the conventions in
force**, and that is why the run opens on the Bâtisseur.

**The Architecte's step** — 📌 **four gestures, in this order:**

1. 🔴 **Commit the request file** — `git add
   docs/features/<name>/architecte/ && git commit -m "chore: requête du
   Bâtisseur"` — ⚠️ **the Bâtisseur never commits it**
2. 🔴 **Invoke `architecte`, invocation 3**
3. 🔴 **`blocked_architecte.md` at the working folder's root → stop** —
   📌 **it blocks on a missing input, the conventions file first of
   all**, and the derivation runs again — `Next: run /conventions
   <name>`
4. 📌 **Otherwise, commit what it wrote** — `git add
   docs/TECHNICAL_CONVENTIONS.md docs/features/<name>/couverture.md
   docs/features/<name>/architecte/ && git commit -m "chore: verdict de
   l'Architecte"` — 🔴 **read the conventions commit again, and invoke
   `batisseur`**

🔴 **Three Architecte invocations per run, at most.** ⚠️ **A fourth
request means the tables do not converge** — 📌 **stop, and relay every
request and its verdict**: `Next: stop requests did not converge:
architecte/batisseur.md`.

📌 **The Bâtisseur bounds the loop itself** — 🔴 **a need an answered
request already carries is never raised again**: ⚠️ **a verdict that
leaves the tables short is its blocking file**, not a new request.

🔴 **The Bâtisseur's report names a blocking file under `## Decision
applied` → rename it, inside the worktree, before the steps below:**

    git mv docs/features/<name>/blocked_batisseur.md \
           docs/features/<name>/blocked_batisseur-NN.md

📌 **`NN`: the highest in the folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file** — 🔴 **left at
the unnumbered name, the next run stops on it.**

🔴 **Never paraphrase an agent's process in your invocation** — not its
inputs, its checks, its output format. It reads its own instructions.

### Invocation parameters

```
Agent(
  subagent_type="batisseur",
  model="sonnet",
  description="Build <feature>",
  prompt="Working folder: docs/features/<name>/. Conventions: <commit>."
)
```

📌 **A `blocked_batisseur.md` whose `## Decision` is filled adds a
sentence**: `Blocking file: blocked_batisseur.md.`

```
Agent(
  subagent_type="architecte",
  model="opus",
  description="Requests <feature>",
  prompt="Working folder: docs/features/<name>/. Invocation 3 — Requests. Called by the orchestration."
)
```

📌 **The prompt says who called** — 🔴 **`Called by the orchestration.`,
never inferred**: the Architecte behaves differently when the Arbitre
calls it.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — 📌 **the Bâtisseur builds on what the
Architecte just wrote**, and branching would cut it from it.

---

## Git, once it has reported

**Then — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   rename above is staged, not committed**, and so is anything the
   Architecte wrote after the last commit; 📌 **the Bâtisseur commits its
   own files**, and `git status` says what is left. 📌 **`git merge`
   takes the worktree's commit, not its files**, and `git worktree
   remove` refuses a dirty tree
2. 🔴 **Read the worktree's commit id, then leave it** —
   `git -C <path> rev-parse HEAD`; ⚠️ **a session isolated in a
   worktree cannot issue a git command against the main checkout**:
   the merge below, issued from inside it, is refused
3. `git merge --no-ff -m "Merge /batir <name>" <commit id>` from the
   main checkout root
4. `git push`
5. `git worktree remove <path>`

⚠️ **A worktree still dirty after step 1 refuses a plain remove** — 🔴
**never force it**: 📌 **say what is left there, and stop** —
`Next: stop worktree dirty: <files>`. ⚠️ **What the build wrote and the
ignore file does not hold is the usual cause** — 📌 **name it**: the
Bâtisseur's next run adds it there.

🔴 **The push is part of the merge, not an afterthought.**

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — including a blocking file:
the Product Owner has to see it.

---

## What you relay

**From the report** — 📌 **its sections, as the Bâtisseur wrote them**:
what it created, or that it created nothing; each G2.1 command with its
result and its duration; the packages; what it installed; the targets
the deploy profile gained. 🔴 **Nothing else is yours** — no judgement
on the skeleton.

📌 **Every request and its verdict**, when the Architecte ran — ⚠️
**the conventions changed in this run**, and the Product Owner learns it
here.

🔴 **A blocking file: its `## To resume`, whole** — ⚠️ **on a build tool
it is a tutorial for her**, and she should not have to open the file to
follow it.

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included:

| The run | `Next:` |
|---|---|
| `## Status: built` | `Next: run /7_lots <name>` |
| A blocking file waits | `Next: answer blocking, then run /batir <name>` |
| The conventions are missing, lack a table, or the Architecte blocked | `Next: run /conventions <name>` |
| The requests did not converge | `Next: stop requests did not converge: architecte/batisseur.md` |
| Blocked with nothing waiting | `Next: stop the Bâtisseur ended blocked with nothing waiting` |
| The worktree was there, or stayed dirty | `Next: stop worktree already there: <path>` · `Next: stop worktree dirty: <files>` |
