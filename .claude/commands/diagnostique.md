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
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **The working folder is the highest `bugfix-NN/` in it.** The
Product Owner created it and wrote `bug-list.md` inside. **No such
folder, or no `bug-list.md`** → say so and stop; you never create
either. `Next: stop no bugfix-NN/bug-list.md`

📌 **Every path below is relative to that folder.**

---

## What you read

**`bug-list.md`, and only to split it, gap by gap.** 🔴 **You read the
gaps to hand each one to an agent, never to judge, rewrite or merge
them.**

📌 **One gap, one identifier** — the `G<n>` each gap opens on, `G01`,
`G02`. 🔴 **Read from the line, never counted from the gap's
position** — 📌 **the Product Owner writes it**, as a control-report
gap already carries its `B<n>` in parentheses at the end of its first
line. **Its full text goes in the prompt**, verbatim, the `G<n>`
passed as its identifier. ⚠️ **A gap opening on no `G<n>`** → 🔴 **stop
before issuing anything, and say which line lacks one** —
`Next: stop gap without a G<n>: <line>`.

**`investigation/`, and only to sort the gaps** — a `Glob` on
`investigation/*.md` tells which gap has its report and which has a
blocking file. 🔴 **A blocking file is opened for its `## Decision`
alone**, to tell empty from filled — never for what it says.

**`desc-bug.md`** — 📌 **its existence, nothing more**: a `Glob` before
phase 2.

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

🔴 **Sort every gap of `bug-list.md` before issuing anything**, on
what `investigation/` holds for its identifier — the first row that
matches decides:

| For `<id>` | Phase 1 |
|---|---|
| `investigation/blocked_<id>.md` with a filled `## Decision` | **Issue it**, naming the file in the prompt — the agent applies it, then investigates |
| `investigation/blocked_<id>.md` with an empty `## Decision` | 🔴 **Skip it, and relay it as standing** — nothing changed since it was written; re-issuing it costs a full investigation that stops at the same place |
| `investigation/<id>.md` exists | **Skip it** — 🔴 **an existing report is done; a re-run costs a full investigation** |
| Nothing | **Issue it** |

📌 **That is how a single failed investigation is re-run**: the Product
Owner fills its blocking file, you launch this command again, and only
that one goes.

**Phase 1 — one `Agent()` per gap to issue, all issued together.**
🔴 **Each call carries one gap and its identifier**, nothing about the
others.

```
Agent(
  subagent_type="diagnostiqueur",
  model="sonnet",
  description="investigate G01 <feature>",
  prompt="Bug-fix folder: docs/features/<name>/bugfix-NN/.
          Invocation 1 — Investigation.
          Gap G01: <the gap's text, verbatim>.
          [Blocking file: investigation/blocked_G01.md — its
          ## Decision is filled.]"
)
```

📌 **The bracketed line goes in only on the first row of the table.**

⚠️ **Wait for every call to report** before phase 2. 📌 **A call that
returns a blocking file does not stop the others** — relay it, let the
rest finish.

⚠️ **Phase 1 issuing nothing is normal** — every gap has its report,
or what has none stands blocked.

🔴 **Phase 2 runs only once every report exists.** ⚠️ **A phase-1 block
withholds it** — a gap whose investigation blocked has no report, and
invocation 2 would only block in turn, on a file no decision can
supply a report to. 📌 **Report the blocked identifiers from your own
phase-1 results** — the calls that returned a blocking file, and the
gaps skipped as standing — and stop there; see *What you relay*.

🔴 **Before issuing phase 2, `Glob` `desc-bug.md` in the folder.** ⚠️
**It exists → do not issue phase 2**: 📌 **relay it as done** — what
it holds is settled, and the agent would only stop on it.

**Phase 2 — one `Agent()`, once every report exists and no
`desc-bug.md` does.**

```
Agent(
  subagent_type="diagnostiqueur",
  model="sonnet",
  description="assemble <feature>",
  prompt="Bug-fix folder: docs/features/<name>/bugfix-NN/.
          Invocation 2 — Assembly.
          [Blocking file: blocked_diagnostiqueur.md — its
          ## Decision is filled.]"
)
```

📌 **The bracketed line goes in only when that file is there with a
filled `## Decision`.**

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

**Then, once the last call you issued reports** — phase 2's, or
phase 1's when phase 2 is withheld or not issued — 📌 **five steps, in
this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the renames of *What
   you relay* are staged, not committed; 📌 **`git merge` takes the
   branch's commits, not the worktree's files**, and
   `git worktree remove` refuses a dirty tree
2. 🔴 **Leave the worktree** — ⚠️ **a session isolated in a worktree
   cannot issue a git command against the main checkout**: the merge
   below, issued from inside it, is refused
3. `git merge --no-ff <branch>` from the main checkout root
4. `git push`
5. `git worktree remove <path>`

⚠️ **A worktree still dirty after step 1 refuses a plain remove** — 🔴
**never force it**: 📌 **say what is left there, and stop** —
`Next: stop worktree dirty: <files>`. 📌 **What
is left is something step 1 did not stage** — a fault of this run,
never of the agent: it was not to commit it. Forcing the removal
destroys it.

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

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.
📌 **Phase 2 wrote `desc-bug.md`** — `Next: run /7_lots <name>`.

**If an agent returns a blocking file**: relay it. 📌 **In phase 1 it
is `investigation/blocked_<id>.md` and the other calls carry on**;
in phase 2 it is `blocked_diagnostiqueur.md` and you stop —
`Next: answer blocking, then run /diagnostique <name>`.

**If phase 2 is not issued**: say why. 📌 **`desc-bug.md` exists** —
relay it as done, and name the next step, `/7_lots` — `Next: run /7_lots
<name>`. 📌 **Phase 2
withheld** — 🔴 **list every identifier standing blocked**, from your
own phase-1 results: the calls that returned
`investigation/blocked_<id>.md`, and the gaps skipped as standing.
**That is what the Product Owner needs to re-run them** — ⚠️ **never
an identifier taken from an invocation-2 block**: there is none.
`Next: answer blocking, then run /diagnostique <name>`

🔴 **A blocking file's `## Decision` filled, run `/diagnostique`
again** — 📌 **name the file in the agent's prompt**, and 🔴 **rename it
once the agent reports having applied it** — the same gesture for both
files:

    git mv investigation/blocked_<id>.md investigation/blocked_<id>-NN.md
    git mv blocked_diagnostiqueur.md blocked_diagnostiqueur-NN.md

📌 **`NN`: the highest beside it plus one, `01` when there is none** —
counted per file: among `investigation/blocked_<id>-NN.md` for that
identifier, among `blocked_diagnostiqueur-NN.md` at the root. ⚠️ **The
agent has no tool that removes a file.** 🔴 **A filled decision left at
the unnumbered name re-issues the gap at the next run**, and
`/audit_blocages` lists it as still open.
