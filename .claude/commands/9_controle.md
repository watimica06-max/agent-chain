---
description: Confront the product file against every spec sheet
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **downstream mode**.

**This command invokes `controleur` once per group of blocks, then
once more to assemble.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **Always the feature folder itself, never a `bugfix-NN/`.** The
Contrôleur confronts the product file with the sheets built from it,
and both live here — a correction cycle has neither.

📌 **Every path below is relative to it.**

---

## What you read

**Only whether `desc-produit.md` is there**, and whether every lot of
`code/sequence.md` carries a `verdict.md` in PASS.

⚠️ **Nothing else.** `CLAUDE.md`'s standing reading rules apply.

---

## When it runs

📌 **`/8_code` runs the Contrôleur on its own, once the last lot
passes.** This command is for running him again — after the sheets
changed, after his own rules changed, or to compare two states.

🔴 **Stop if `desc-produit.md` is absent** — say so. Without it there
is nothing to confront the sheets with.

🔴 **Stop if a lot of the sequence has no `verdict.md` in PASS** — name
it. He would read an incomplete set of sheets and report an intention
as missing when it is merely unwritten.

📌 **An existing `rapport-controle.md` is not a reason to stop.** He
writes the next free number beside it; that is how two states are
compared.

---

## How it runs

**Three phases.**

### Phase 1 — build the block-to-lot map

🔴 **Two greps and a crossing**, no agent.

**a.** `tracabilite.md` gives block → entries.

**b.** The `Anchor:` fields of `code/decoupage.md` give entry → lots.

**c.** Cross them into `tracabilite-full.md`, at the feature folder's
root.

🔴 **One line per block, in block order** — its identifier, then the
lots that build its entries, deduplicated:

    B1   lot-01
    B43  lot-21, lot-30, lot-33
    B59  —

📌 **Two spaces at least after the identifier**; nothing else on the
line, no title, no prose, no header. **That is the format the script
parses.**

🔴 **Every block appears.** A block whose entries no lot cites gets a
dash — it still needs an answer, and the group carrying it reads no
sheet for it.

### Phase 2 — group the blocks

    python3 .claude/scripts/grouper.py docs/features/<name>/tracabilite-full.md --auto

📌 **The script sweeps every budget and picks one**, weighing the
context of a pass against the number of passes. **It prints the groups
under `=== budget …`, one `G<n>` line each.**

🔴 **Take the grouping it prints, unchanged.** ⚠️ **Never regroup by
hand, never override the budget** — the split has to be reproducible
from the same input.

📌 **A `|` inside a `G<n>` line separates atoms**, not groups.
**Everything on one such line is one group.**

### Phase 3 — one Contrôleur per group, then one to assemble

**What you do**: invoke the agent via `Agent()` with the feature folder
and the group it takes — and nothing else.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

### Invocation parameters

```
Agent(
  subagent_type="controleur",
  model="sonnet",
  description="control G1 <feature>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 1 — Confront.
          Blocks: B15, B53, B54, B56.
          Sheets: code/lot-29, code/lot-43, code/lot-44."
)
```

⚠️ **Issue every group together**, then wait for all of them.

**Then, once every group has reported:**

```
Agent(
  subagent_type="controleur",
  model="sonnet",
  description="assemble <feature>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 2 — Assembly."
)
```

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`.**

---

## Git, in this mode

🔴 **Commit the feature folder first**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-control"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded.

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

**Then, once the agent reports:**

1. `git merge --no-ff -m "Merge <branch>" <branch>` from the main
   checkout root
2. `git push`
3. `git worktree remove <path>`

🔴 **The push is part of the merge, not an afterthought.** A report
that sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

---

## What you relay

**The agent's own report, and the name of the file it wrote.** 🔴
**Nothing else is yours**: no reading of that file, no summary of what
it found, no decision on what to do next.

📌 **The Product Owner reads the report and decides** whether it
becomes a `bug-list.md` for a correction cycle.
