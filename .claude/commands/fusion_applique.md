---
description: Apply the merge plan and write the report
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `fusionneur`, invocation 2 — Apply.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/$ARGUMENTS/`

---

## Before anything else

🔴 **Five tests, in this order** — 📌 **stop at the first that fires:**

| | |
|---|---|
| `rapport-fusion.md` exists | 🔴 **Stop** — 📌 **the merge is done** — `Next: done` |
| `plan-fusion.md` absent | 🔴 **Stop** — 📌 **invocation 1 has not run**: say to use `/fusion_compare` — `Next: run /fusion_compare <name>` |
| `blocked_fusionneur.md` with an empty `## Decision` | 🔴 **Stop** — 📌 **relay it** — `Next: answer blocking, then run /fusion_applique <name>` |
| `blocked_fusionneur.md` with a filled `## Decision`, and its `## Invocation` line names 1 or 3 | 🔴 **Stop** — 📌 **it is not this command's**: say `/fusion_compare` for 1, `/fusion` for 3 — `Next: run /fusion_compare <name>` for 1, `Next: run /fusion <name>` for 3 |
| A root `questions-fusionneur-*.md` with an empty `Answer:` | 🔴 **Stop** — 📌 **relay which questions wait** — `Next: answer questions, then run /fusion_applique <name>` |

🔴 **A `blocked_fusionneur.md` with a filled `## Decision` whose
`## Invocation` line names 2 → name it in the prompt.** 📌 **The agent
applies it and says so in its report** — see *Git, once it has
reported*. ⚠️ **Read those two headings, nothing else** — the agent
reads the file.

---

## What you read

**Only what the tests above need** — whether a file is there, whether
a `## Decision` is empty, what the `## Invocation` line says, one grep
for an empty `Answer:` — and the greps *Git, before invoking* and *On
`INIT` — the copy* name. 📌 **Counts, never content** — each agent
declares its own inputs; you pass the feature folder, the invocation,
the number and — when there is one — the filled blocking file, nothing
else. `CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Git, before invoking

🔴 **Compute the agent's questions file number** — 📌 **the highest
`questions-fusionneur-NN.md` at the root and under
`questions/fusionneur/` together, plus one**; ⚠️ **`01` when there is
none.** 🔴 **It goes in the prompt** — the agent never lists a folder
to find it. 📌 **Invocation 2 needs it too**: on an ambiguous answer it
writes the next questions file, and nothing else.

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

## On `INIT` — the copy

🔴 **`plan-fusion.md` holds `INIT` alone → copy the product file over
the global, in the worktree, before invoking:**

    cp docs/features/<name>/desc-produit-fusion.md docs/PRODUIT_GLOBAL.md

📌 **One grep tells** — the plan's only non-empty line is the word
`INIT`. ⚠️ **Any other plan: no copy** — the agent applies it by
targeted edits.

📌 **The agent has no tool that copies** — ⚠️ **and a whole read
followed by a whole write truncates in silence.** 🔴 **It strips from
the copy what belongs to the feature file alone; you make the copy.**

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
  description="Apply <feature>",
  prompt="Feature folder: docs/features/<name>/. Invocation 2 — Apply.
          Questions file number: <NN>.
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

🔴 **The agent reports having applied a decision → rename its blocking
file**, inside the worktree, before the steps below:

    git mv docs/features/<name>/blocked_fusionneur.md \
           docs/features/<name>/blocked_fusionneur-NN.md

📌 **`NN`: the highest in that folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file** — 🔴 **left at
the unnumbered name, the next run stops on it.** 📌 **Step 1 carries the
rename into the commit** — ⚠️ **done after it, the rename stays out of
the merge and leaves the tree dirty for step 5.**

**Then, once it has reported — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the copy *On `INIT`*
   makes and the rename above are committed by nobody else; 📌 **`git
   merge` takes the branch's commits, not the worktree's files**, and
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

---

## Filing away, once the merge holds

🔴 **The merge branch ends here — once `rapport-fusion.md` is
written**: move every root `questions-*.md` to `questions/<its agent>/`:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

⚠️ **`git mv`, never a read-and-rewrite.** 📌 **Create the folder if it
does not exist**, and commit the moves.

⚠️ **No report, nothing filed.** 📌 **A run that wrote a questions file
holding a question, or a `blocked_fusionneur.md`, applied nothing** —
the file stays at the root, where the Product Owner answers it and the
next run's tests find it.

---

## What you relay

The agent's own report, and nothing more. 🔴 **Nothing else is yours**:
no phase chain.

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.
📌 **`rapport-fusion.md` written** — `Next: done`.

**If it returns a `blocked_*.md`**: relay it and stop —
`Next: answer blocking, then run /fusion_applique <name>`.

**If its questions file holds a `### Q`**: relay it and stop — 📌
**answered, `/fusion_applique` again** — `Next: answer questions, then
run /fusion_applique <name>`.
