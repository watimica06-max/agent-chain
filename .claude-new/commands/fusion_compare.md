---
description: Compare the product file against the global
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `fusionneur`, invocation 1 — Compare and question.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## Before anything else

🔴 **Three tests, in this order** — 📌 **stop at the first that fires:**

| | |
|---|---|
| `desc-produit-fusion.md` absent | 🔴 **Stop** — 📌 **say to run `/fusion` first**: ⚠️ **only its Rédacteur row writes that file**, and the Fusionneur reads it and nothing else |
| `blocked_fusionneur.md` with an empty `## Decision` | 🔴 **Stop** — 📌 **relay it** |
| `blocked_fusionneur.md` with a filled `## Decision`, and its `## Invocation` line names 2 or 3 | 🔴 **Stop** — 📌 **it is not this command's**: say `/fusion_applique` for 2, `/fusion` for 3 |

🔴 **A `blocked_fusionneur.md` with a filled `## Decision` whose
`## Invocation` line names 1 → name it in the prompt.** 📌 **The agent
applies it and says so in its report** — see *Git, once it has
reported*. ⚠️ **Read those two headings, nothing else** — the agent
reads the file.

---

## What you read

**Only what the tests above need** — whether a file is there, whether
a `## Decision` is empty, what the `## Invocation` line says — and the
greps *Git, before invoking* names. 📌 **Never content beyond that.**
Each agent declares its own inputs; you pass the feature folder, the
invocation, the number and — when there is one — the filled blocking
file, nothing else. `CLAUDE.md`'s standing reading rules apply: never
open `CURRENT_TECHNICAL_STATE.md`.

---

## Git, before invoking

🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not
`architecte` before touching it** — 📌 **a file holding questions is
not yours to file**: ⚠️ **it waits on an answer, or its answers were
never integrated.** 🔴 **Stop and say which.** 📌 **The architecte's is
the one exception** — ⚠️ **it is `/conventions`'s, not this chain's**,
and a `### Q` in it says nothing about the run; 🔴 **read the root as if
it were not there** — and leave it there, see below.

🔴 **Then move every root `questions-*.md` whose prefix is not
`fusionneur`:**

    git mv docs/features/<name>/questions-<other>-NN.md \
           docs/features/<name>/questions/<other>/

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every `questions-fusionneur-NN.md` but the highest** — the
last one stays at the root.

📌 **Create `questions/<agent>/` if it does not exist.**

🔴 **Compute the agent's questions file number** — 📌 **the highest
`questions-fusionneur-NN.md` at the root and under
`questions/fusionneur/` together, plus one**; ⚠️ **`01` when there is
none.** 🔴 **It goes in the prompt** — the agent never lists a folder
to find it.

🔴 **Then commit the feature folder**, before creating the worktree:

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

**What you do**: invoke the agent via `Agent()` with the feature folder,
which invocation it is, its questions file number — and the blocking
file, when a filled one is there — and nothing else.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

### Invocation parameters

```
Agent(
  subagent_type="fusionneur",
  model="sonnet",
  description="Compare <feature>",
  prompt="Feature folder: docs/features/<name>/. Invocation 1 — Compare
          and question. Questions file number: <NN>.
          [Blocking file: docs/features/<name>/blocked_fusionneur.md,
          its `## Decision` filled.]"
)
```

📌 **The bracketed line only when the test in *Before anything else*
found a filled one.**

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are sequential
and each reads what the previous one wrote.

---

## Git, once it has reported

**Then, once the agent reports — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**; 📌 **`git merge` takes the
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
`blocked_*.md` merges too**: the Product Owner has to see it.

🔴 **The agent reports having applied a decision → rename its blocking
file:**

    git mv docs/features/<name>/blocked_fusionneur.md \
           docs/features/<name>/blocked_fusionneur-NN.md

📌 **`NN`: the highest in that folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file** — 🔴 **left at
the unnumbered name, the next run stops on it.**

---

## What you relay

The agent's own report, and nothing more. 🔴 **Nothing else is yours**:
no phase chain.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

| What just happened | Next |
|---|---|
| It wrote `blocked_fusionneur.md` | 📌 Fill its `## Decision`, then `/fusion_compare` again |
| Its questions file holds a `### Q` | 📌 Answer them, then `/fusion_applique` |
| Its questions file is empty | 📌 `/fusion_applique` at once |

**If it returns a `blocked_*.md`**: relay it and stop.
