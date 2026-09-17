---
description: Confirm reported gaps against the code — bug-fix cycle
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `diagnostiqueur` twice over** — once per gap for
the investigation, then once for the assembly.

📌 **It produces `desc-bug.md`** — the technical document of a bug-fix
cycle. **Then `/7_lots`, then `/8_code`.** ⚠️ **No grid, no
Convertisseur, no Fusionneur**: the product already says what is
expected, and a correction adds nothing to it.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **The working folder is the highest `bugfix-NN/` in it.** The
Product Owner created it and wrote `bug-list.md` inside. **No such
folder, or no `bug-list.md`** → say so and stop; you never create
either.

📌 **Every path below is relative to that folder.**

---

## What you read

**`bug-list.md`, and only to count and split it.** 🔴 **You read the
gaps to hand each one to an agent, never to judge, rewrite or merge
them.**

📌 **One gap, one identifier** — `G01`, `G02`, in the file's own order.
**Its full text goes in the prompt**, verbatim.

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## Git, before invoking

🔴 **Commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner writes `bug-list.md` by hand, outside this
session.** A worktree branches from the last commit — an uncommitted
gap file is invisible inside it.

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

**Two phases, in this order.**

🔴 **Skip a gap whose report already exists**, unless its
`investigation/blocked_<id>.md` carries a filled `## Decision`. **A
re-run costs a full investigation; an existing report is done.**

📌 **That is how a single failed investigation is re-run**: the Product
Owner fills its blocking file, you launch this command again, and only
that one goes.

**Phase 1 — one `Agent()` per remaining gap, all issued together.**
🔴 **Each call carries one gap and its identifier**, nothing about the
others.

```
Agent(
  subagent_type="diagnostiqueur",
  model="sonnet",
  description="investigate G01 <feature>",
  prompt="Bug-fix folder: docs/features/<name>/bugfix-NN/.
          Invocation 1 — Investigation.
          Gap G01: <the gap's text, verbatim>."
)
```

⚠️ **Wait for every call to report** before phase 2. 📌 **A call that
returns a blocking file does not stop the others** — relay it, let the
rest finish.

⚠️ **Phase 1 issuing nothing is normal** — every report exists and you
go straight to phase 2.

**Phase 2 — one `Agent()`, once every report exists.**

```
Agent(
  subagent_type="diagnostiqueur",
  model="sonnet",
  description="assemble <feature>",
  prompt="Bug-fix folder: docs/features/<name>/bugfix-NN/.
          Invocation 2 — Assembly."
)
```

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — phase 2 reads what phase 1 wrote.

📌 **Phase 1's calls do not collide**: each writes
`investigation/<id>.md`, its own file and no other.

---

## Git, once it has reported

**Then, once phase 2 reports:**

1. `git merge --no-ff <branch>` from the main checkout root
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — a phase whose output sits on
an unmerged branch is invisible to the next one. ⚠️ **A
`blocked_*.md` merges too**: the Product Owner has to see it.

---

## What you relay

The agent's own report, and nothing more. 🔴 **Nothing else is yours**:
no phase chain.

**If an agent returns a blocking file**: relay it. 📌 **In phase 1 it
is `investigation/blocked_<id>.md` and the other calls carry on**;
in phase 2 it is `blocked_diagnostiqueur.md` and you stop.

🔴 **Its `## Decision` filled, run `/diagnostique` again** — 📌 **name
the file in the agent's prompt**, and 🔴 **rename it once the agent
reports having applied it**:

    git mv blocked_diagnostiqueur.md blocked_diagnostiqueur-NN.md

📌 **`NN`: the highest in the folder plus one, `01` when there is
none.** ⚠️ **The agent has no tool that removes a file.**

⚠️ **A phase-1 block does not cancel phase 2** — invocation 2 counts
the reports against `bug-list.md` and blocks itself if one is missing.

🔴 **Say which identifier the missing report belongs to**, taken from
invocation 2's own block. **That is what the Product Owner needs to
re-run it.**
