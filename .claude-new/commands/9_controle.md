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

🔴 **This command hands the Product Owner three things, and nothing
else:**

| | |
|---|---|
| **The manual list**, assembled and ordered | 📌 **What no automated test could exercise** |
| **The register of escaped product questions** | 📌 **Gathered, never concluded** |
| **The product decisions taken while coding** | 📌 **One file per cycle**, for the Rédacteur |

🔴 **It runs on the main cycle and on every correction cycle.** ⚠️ **The
Contrôleur runs on the main cycle alone** — 📌 **a correction cycle has
no product file**, and there is nothing to confront.

🔴 **`desc-produit.md` absent, on the main cycle** — 📌 **say so and
stop**: there is nothing to confront the sheets with.

📌 **On a correction cycle** — 🔴 **phases 1 to 3 do not run.** ⚠️ **The
other two deliverables do.**

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

🔴 **Empty `code/controle/` before issuing the groups** — 📌 **the
partials of an earlier run would otherwise still be there.**

⚠️ **Issue every group together**, then wait for all of them.

**Then, once every group has reported:**

```
Agent(
  subagent_type="controleur",
  model="sonnet",
  description="assemble <feature>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 2 — Assembly.
          Groups issued this run: G1, G2, G3.
          Blocks to account for: B1, B2, B3, ... (or: the G<n> lines
          of tracabilite-full.md)."
)
```

🔴 **Name the groups this run issued, and the full block list.** ⚠️
**Without the groups, a partial left by an earlier run is merged with
this run's** — 📌 **and its lines speak of sheets that have changed
since.** ⚠️ **Without the block list, a group that wrote nothing is
invisible**: the numbering alone shows a hole between `B6` and `B8`,
never the last blocks of the feature.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`.**

---

### Phase 4 — the manual list

🔴 **Two sources**: 📌 **`code/recette.md`**, the lines the testeur wrote
lot by lot, **and `par-genre/recette.md`**, what the Product Owner said
he wanted to check himself.

🔴 **Order it by state, never by intention.**

| | |
|---|---|
| **Everything checkable on an empty application** | first |
| **Then with one record** | 📌 **announce the state change** |
| **Then with several** | — |

⚠️ **Every reset costs the Product Owner dearly** — 🔴 **as few as
possible, and each one announced on its own line.**

📌 **One line, one thing to look at** — 🔴 **in the Product Owner's
words, with what is expected.** ⚠️ **A line that does not say its state
cannot be placed**: leave it at the end, under *state not stated*.

🔴 **You add nothing and you reword nothing** — 📌 **you order.**

⚠️ **Why it matters**: 📌 **a manual test file has existed and was
abandoned** — 🔴 **not because it was useless, but because it was
unusable**: thousands of unordered tests, with deletions and data
resets in the middle.

**Write `code/recette-ordonnee.md`.**

### Phase 5 — the register of escaped product questions

🔴 **Two sources**: 📌 **the `Doubtful` and `Missing` fields of
`code/rapport-controle*.md`** — the latest one — **and the product
questions the Arbitre handed back**, in the `blocked_<agent>-NN.md`
files of the working folder.

🔴 **One case per line, and you conclude nothing.** ⚠️ **No class
proposed, no grid change suggested** — 📌 **an isolated case says
nothing; ten together let a shape show.**

**Write `code/registre-questions.md`.**

📌 **On a correction cycle** — 🔴 **the Arbitre's files alone**: there
is no control report.

### Phase 6 — the product decisions taken while coding

🔴 **A product question settled during the coding went into a sheet** —
📌 **never into the product file, never into the global.**

🔴 **Gather them from the `blocked_<agent>-NN.md` files**: 📌 **every
`## Decision` that settles what the application does**, as opposed to
how it is built.

⚠️ **The test is the one the Arbitre uses** — 📌 **a decision on a
behaviour, a wording, what the user sees.** 🔴 **A technical decision
is not one.**

**Write `code/decisions-produit.md`** — 📌 **one decision per line, with
the block it bears on when the file names one.**

🔴 **The Rédacteur reads it at `/fusion`**, invocation 3. ⚠️ **Write it
even empty** — 📌 **its absence would read as *the phase did not run*.**

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

**The agent's own report, and the four files this run wrote**, by name:

| | |
|---|---|
| `code/rapport-controle-NN.md` | 📌 **Main cycle only** |
| `code/recette-ordonnee.md` | 🔴 **What the Product Owner checks by hand** |
| `code/registre-questions.md` | — |
| `code/decisions-produit.md` | 📌 **Read by the Rédacteur at `/fusion`** |

🔴 **Nothing else is yours**: no reading of those files, no summary of
what they hold, no decision on what to do next.

📌 **The Product Owner reads them and decides** whether the control
report becomes a `bug-list.md` for a correction cycle.

⚠️ **The manual list is the one to run before deciding** — 📌 **a gap
the Contrôleur cannot see shows there.**
