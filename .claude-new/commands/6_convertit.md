---
description: Produce the technical document for the Cadreur, one nature at a time
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `convertisseur` — invocation 1 once per nature
that has to be written, all at once; then invocation 2, once.**

📌 **It runs as many times as needed.** 🔴 **Each run writes again only
the sections whose blocks changed, or that still carry an `<<ASSUMED`
mark**, and keeps the others as they stand.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Greps, byte comparisons and copies, and nothing else.** 📌 **You
never read a block, an entry or a question for what it says.**

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Before anything else

**1.** 🔴 **`code/decoupage.md` exists → stop.** ⚠️ **The split is cut,
and a lot cites entries by number** — 📌 **writing a section again would
renumber it under the lot.** Say that a change to the product now
belongs to a new cycle.

**2.** 🔴 **`par-genre/` absent → stop.** 📌 **Say `/5_reclasse` has to
run**: its six files are what the invocations read beside their blocks.

**2b.** 🔴 **`desc-par-nature.md` absent → stop.** Say `/5_reclasse` has
to run first.

**3. The blocking files** — every unnumbered
`convertisseur/blocked_<nature>.md` and `convertisseur/blocked_transversal.md`,
📌 **read file by file** — ⚠️ **several can stand at once**, one per
nature that blocked in the same run:

| | What you do |
|---|---|
| None | 📌 Carry on |
| Any whose `## Decision` is empty | 🔴 **Stop** — say which ones still stand, ⚠️ **all of them**, never the first found |
| Every one whose `## Decision` is filled | 📌 **Name each in its own nature's prompt** — `blocked_transversal.md` in invocation 2's |

⚠️ **Read that one heading in each, nothing else** — 📌 the agent reads
the file.

---

## Git, before invoking

🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not
`architecte` before touching it** — 📌 **a file holding questions is
not yours to file**: ⚠️ **it waits on an answer, or its answers were
never integrated.** 🔴 **Stop and say which.** 📌 **The architecte's is
the one exception** — ⚠️ **it is `/conventions`'s, not this chain's**,
and a `### Q` in it says nothing about the run; 🔴 **read the root as
if it were not there** — and leave it there, see below.

📌 **Filed, it is read by no command again** — ⚠️ **and its answers are
lost for good** — 🔴 **except under `questions/convertisseur/`**, whose
highest file this command names to a nature in its prompt, see *Which
natures run*: ⚠️ **the agent reads it, never you.**

🔴 **Then move every root `questions-*.md`:**

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

📌 **This command reads none of them.** 🔴 **A questions file stays at
the root only while it waits to be answered or integrated** — ⚠️ **the
next one written has to be the only one there.**

⚠️ **`git mv`, never a read-and-rewrite** — the agent must not open
those files, and neither should you.

🔴 **And every `convertisseur/questions-*.md` the last run wrote**, into
`convertisseur/closed/`, each under the next free number:

    git mv docs/features/<name>/convertisseur/questions-presentation.md \
           docs/features/<name>/convertisseur/closed/questions-presentation-NN.md

⚠️ **They were merged already** — 📌 **left in place, a nature that does
not run this time would see its old questions merged again.**

🔴 **Never a `technique-*.md`, answered or not** — 📌 **an answered one
is what its invocation runs on, and its prompt names it at this path**:
⚠️ **it is filed in *Once it has run*, after the nature has run on it.**

📌 **Create `questions/<agent>/` and `convertisseur/closed/` if they do
not exist.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: answers"

⚠️ **The Product Owner fills `Answer:` fields by hand, outside this
session.** A worktree branches from the last commit — uncommitted
answers are invisible inside it.

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local.

📌 **Enter the worktree before anything below**, not after a write
fails — the harness blocks a subagent's writes until the session is
isolated.

🔴 **Inside it, create `convertisseur/closed/`** if it is not there —
⚠️ an agent whose target folder is missing searches instead of
stopping.

---

## Which natures run

**For each of the eight natures**, take its part of `desc-par-nature.md` —
the lines under its `## <nature>` heading, up to the next `## `. 📌
**`<nature>` in a file name takes a hyphen for a space** —
`convertisseur/external-exchange.md`.

| What you find | The nature |
|---|---|
| Its part holds no block | 🔴 **Runs nowhere** — delete its `<nature>.md`, `<nature>-input.md` and `<nature>-notes.md` if they are there; its section is written empty |
| Its part differs from `convertisseur/<nature>-input.md`, or that file is absent | 🔴 **Runs** |
| `convertisseur/<nature>.md` is absent, **and its part changed** | 🔴 **Runs** — its last run wrote no section |
| `convertisseur/<nature>.md` holds `<<ASSUMED`, **and its part changed** | 🔴 **Runs** — ⚠️ **a mark is lifted only by writing its section again** |
| 🔴 **Its `convertisseur/technique-<nature>.md` is answered** — it holds a `### Q` and no `^Answer:$` line, by grep | 🔴 **Runs** — 📌 **whatever its blocks did**: ⚠️ **a technical answer changes no block**, and without this row it would wait for ever. 📌 **Name the file in its prompt**. |
| Either of the two, **its part byte-identical, and its `technique-<nature>.md` holds an `^Answer:$` line** | 📌 **Waits** — 🔴 **it does not run.** ⚠️ **It would read the same blocks, meet the same gap and ask the same question**: one opus invocation for a known result |
| Either of the two, **its part byte-identical, and no `technique-<nature>.md` holding an `^Answer:$` line** | 🔴 **Runs** — 📌 **the product question it waits on is answered, and the answer changed no block**: ⚠️ **the rerun is what lifts the mark, its part unchanged** — one opus invocation. 🔴 **Name in its prompt the highest `questions-convertisseur-NN.md` under `questions/convertisseur/`** — ⚠️ **the block does not carry the answer, that file does**: 📌 **without it the agent meets the same gap and marks again**, run after run |
| `convertisseur/blocked_<nature>.md` carries a filled `## Decision` | 🔴 **Runs** — ⚠️ **a decision is applied only by the invocation it is named to** |
| None of the above | 📌 **Kept as it stands** |

📌 **A nature that waits is a third state, beside *ran* and *kept*** —
🔴 **and the document does not stand while one waits.**

🔴 **Compare bytes, never by reading** — `cmp`, or `diff -q`.

📌 **Why the part and not the markers** — ⚠️ **the Rédacteur strips the
markers only when a grid or a conversion turn consumed them**, and the
grid has closed by the time this command runs: a block changed two
turns of the grid ago carries none by now. **The part the last run
translated is what this one compares against.**

🔴 **Then, for every nature that runs, copy its part to
`convertisseur/<nature>-input.md`** — 📌 **it is the agent's input, and
what the next run compares against.**

**No nature runs:**

| | What you do |
|---|---|
| `spec-technique.md` exists, opens on `# Preamble`, holds no `<<ASSUMED` and no `[B`, `tracabilite.md` is there, no nature's files were just deleted, no nature is waiting, `convertisseur/technique-transversal.md` is absent or holds an `^Answer:$` line, and `blocked_transversal.md` carries no filled `## Decision` | 🔴 **Nothing to write** — say the document stands, and go to *Once it has run* |
| Otherwise | 📌 **Skip to the assembly** — the document has to be built again around what stands. ⚠️ **An answered `technique-transversal.md` takes a nature's route**: 🔴 **it forces the assembly and invocation 2, which its prompt names** |

---

## The nature invocations

🔴 **All in one message** — ⚠️ **several messages run them in series**,
and they share nothing.

```
Agent(
  subagent_type="convertisseur",
  model="opus",
  description="Convert <name>, <nature>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 1 — Nature: <nature>.
          <Plus: convertisseur/technique-<nature>.md, its question is answered.>
          <Plus: questions/convertisseur/questions-convertisseur-NN.md, its
           answers changed no block — the mark's answer is there.>
          <Plus: convertisseur/blocked_<nature>.md, its decision is filled.>"
)
```

📌 **The `questions-convertisseur-NN.md` line goes only to a nature the
*part byte-identical, no answered technical file* row sent running** —
⚠️ **a nature whose part changed reads the answer in its blocks**, and
the file would tell it nothing the product file does not. 🔴 **You name
the file; you open none of it** — the agent reads it.

🔴 **Wait for all of them.**

🔴 **First, grep for a new unnumbered `convertisseur/blocked_*.md`.**
📌 **One is enough**: that nature is **blocked**, not missing, and not a
nature that could write no rule. ⚠️ **Report every one found as
blocked**, and go to *Once it has run* — 🔴 **never *go no further***.

🔴 **Every stop from here on merges first.** ⚠️ **Seven natures have
written their sections in the worktree** — 📌 **stopping before the
merge loses them all**, the blocking file included, and the Product
Owner sees nothing. 🔴 **The five steps of *Git, once it has
reported* — commit, leave, merge, push, remove — then report.**

🔴 **Then check each wrote `convertisseur/questions-<nature>.md`**, and
— 🔴 **when it wrote its section** — `convertisseur/<nature>-notes.md`:
📌 **the references and the traceability are built from it.**

📌 **`convertisseur/technique-<nature>.md` is written only when the
nature had a technical question** — ⚠️ **its absence is not a defect.** ⚠️ **A
missing one stops the command**
— say which nature and which file. 📌 **Merge first**, as above.

---

## The assembly

| Every nature whose part holds blocks has its `convertisseur/<nature>.md` | What you do |
|---|---|
| Yes | 📌 **Assemble** |
| No | 🔴 **Assemble nothing** — delete `spec-technique.md` if it is there, skip invocation 2, go to *The questions*, and say which nature wrote no section. ⚠️ **It asked something it cannot write a rule without**, and a document missing that rule would be cut as if it were whole |

**`spec-technique.md`, at the feature folder's root, replaced whole** —
the nine sections in order:

| § | Title | § | Title |
|---|---|---|---|
| §1 | Model | §6 | Synchronisation |
| §2 | Persistence | §7 | Presentation |
| §3 | Calculation | §8 | Access |
| §4 | Transition | §9 | Text |
| §5 | External exchange | | |

🔴 **Each of §1 to §8 is its nature's `convertisseur/<nature>.md`,
copied as it stands, by script — never retyped.** 📌 **A nature with no
block gets its heading, then `*(empty)*` — and §9 Text always does**:
no nature writes it, invocation 2 fills it.

    ## §9 Text

    *(empty)*

🔴 **Never omit a section** — ⚠️ **an empty one tells the Cadreur there
is nothing of that nature; an absent one tells him nothing.**

📌 **No preamble** — invocation 2 writes it.

---

## The references with one target

🔴 **Before invocation 2, resolve by script every `[B<n>: …]` whose block
gave a single entry** — in `spec-technique.md`, never in the nature
files.

📌 **The block's line is under `## Trace`**, in whichever
`convertisseur/*-notes.md` holds it. 🔴 **One entry on it → write that
number in place of the brackets. Several, a dash, or no line → leave
them** — invocation 2 settles those.

⚠️ **Replace, never read** — 📌 **one entry leaves nothing to judge**, and
that is the only case you touch.

🔴 **A `[B<n>:` whose `]` is not on the same line is a fault of the
run** — 📌 **the script reports it, never skips it**: ⚠️ **a
line-oriented replacement leaves it unresolved or half-replaced**, in a
document the Cadreur cuts. 🔴 **Say which section holds it, and stop,
merging first** — never hand it to invocation 2.

---

## Invocation 2

🔴 **Every time a document was assembled** — ⚠️ **a section written
again may have renumbered its entries**, and every reference into it
has to be resolved afresh.

```
Agent(
  subagent_type="convertisseur",
  model="opus",
  description="Convert <name>, transversal",
  prompt="Feature folder: docs/features/<name>/.
          Invocation 2 — Transversal.
          <Plus: convertisseur/technique-transversal.md, its question is answered.>
          <Plus: convertisseur/blocked_transversal.md, its decision is filled.>"
)
```

🔴 **Then check `convertisseur/questions-transversal.md` exists.** ⚠️
**Missing, it stops the command** — the invocation did not run.

🔴 **Then `tracabilite.md`, read against that questions file:**

| `tracabilite.md` | `questions-transversal.md` | What it is |
|---|---|---|
| There | — | 📌 The document is complete — carry on |
| Missing | Holds a `### Q` — or `technique-transversal.md` does | 📌 **Invocation 2's *No*** — ⚠️ **it asked something it cannot write the preamble without**, and wrote neither. 🔴 **Not a fault**: go to *The questions*, and say the document does not stand |
| Missing | Empty, and no `technique-transversal.md` holding one | 🔴 **A fault of the run** — say so, and stop, merging first |

📌 **An `<<ASSUMED` mark left beside an answered technical file is a
nature that did not apply its answer** — ⚠️ **say which, and run it
again, from *The nature invocations* on.** 🔴 **Once, never twice** — 📌
**a mark still there after that rerun is a fault of the run**, reported
like a missing file. 📌 **A mark beside an unanswered file is normal**:
the question is waiting.

🔴 **Grep `[B` in `spec-technique.md`.** 📌 **What remains beside a
questions file that holds questions is one of them.** ⚠️ **What remains
beside an empty questions file is a reference the run missed** — 🔴 **a
fault, never a *document stands***: say so, and run invocation 2 once
more. 📌 **Once, never twice.**

🔴 **And compare the block identifiers of `desc-produit.md`'s headings
with the first column of `tracabilite.md`.** ⚠️ **One missing, one
extra** — 📌 **a fault of the run, reported like a missing file.** 🔴
**It is the one file that says which block produced nothing**, and a
line dropped there is invisible everywhere else.

---

## The questions

🔴 **Merge into the next `questions-convertisseur-NN.md`, at the
root** — the highest number in `questions/convertisseur/`, plus one;
⚠️ the root holds none by now.

⚠️ **A `technique-<nature>.md` never goes into the merged file, nor
`technique-transversal.md`** — 🔴 **it is technical, and the Product
Owner answers it in place**: 📌 **the merged file carries the product
questions alone.**

📌 **What goes in: the files this run wrote** — the natures in section
order, then `questions-transversal.md`.

🔴 **Every entry copied as written, renumbered from `Q1`.** ⚠️ **You
rephrase nothing.**

📌 **No question at all** → 🔴 **write the file empty.** ⚠️ **That is
what ends the loop.**

---

## Once it has run

🔴 **Every blocking file you named is filed**, each on its own —
`blocked_transversal.md` the same way:

    git mv docs/features/<name>/convertisseur/blocked_<nature>.md \
           docs/features/<name>/convertisseur/blocked_<nature>-NN.md

📌 **`NN`: the highest `blocked_<nature>-NN.md` in `convertisseur/`
plus one — `01` when there is none.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **And every answered technical file you named in a prompt, whose
invocation wrote what it is for** — the nature its section, invocation
2 `tracabilite.md`; `technique-transversal.md` the same way — into
`convertisseur/closed/`, under the next free number:

    git mv docs/features/<name>/convertisseur/technique-<nature>.md \
           docs/features/<name>/convertisseur/closed/technique-<nature>-NN.md

📌 **The invocation has run on it, and the answer is applied** — ⚠️
**left in place, the *Runs* row would fire on it again next run**, one
opus invocation for a known result.

⚠️ **An invocation that wrote no section — a `No`, a blocking file —
applied nothing**: 🔴 **its answered file stays at its name**, and the
*Runs* row fires on it again, as it must.

🔴 **Grep `^Answer:$` in it first.** 📌 **One hit is a new question the
invocation wrote over the answered one** — ⚠️ **leave it at its name**:
it waits, and the answered file it replaced was consumed by that same
run.

---

## Git, once it has reported

**Then, once it has reported — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agent has no Bash and commits nothing**, and the filings of *Once it
   has run* are staged, not committed; 📌 **`git merge` takes the
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

---

## What you relay

📌 **Which natures ran — and which of them ran on an unchanged part,
to lift a mark whose product answer changed no block — which were
kept, which are waiting on an unanswered technical file, how many
questions, and how many `<<ASSUMED` marks the document holds** — a
grep.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

🔴 **The first row that matches is the one you relay** — ⚠️ **a run can
match two**: 📌 **a waiting nature makes the assembly write nothing and
*The questions* write an empty file**, and the run then matches the
waiting row and the last one. **The waiting row sits above; it wins.**
⚠️ **The *Invocation 2's No* row is the one exception** — it adds to the
row that matched above it, and never fires alone.

| The run | Next |
|---|---|
| An invocation wrote a blocking file, **and nothing else asked** | 📌 Fill its `## Decision`, then `/6_convertit` again |
| **A blocking file and technical questions only** | 🔴 **Answer them, fill the decision, then `/6_convertit`** — 📌 the short loop, the decision applied on the same rerun |
| **A blocking file and product questions**, with or without technical ones | 🔴 **Fill the decision first, answer the questions, then `/1_lexique`** — 📌 **the long loop, whatever else waits**: ⚠️ **a product answer goes through the Rédacteur and the grid, and `/6_convertit` applies the decision when its turn comes round** |
| **Technical questions only** | 🔴 **Answer them, then `/6_convertit`** — 📌 **the short loop**: a technical answer changes no block, so nothing upstream has to run again |
| **Product questions, alone or with technical ones** | 📌 **Answer them, then `/1_lexique`** — 🔴 **the long loop.** ⚠️ **Answer the technical ones too**: the agent integrates both when its turn comes round |
| **A nature is waiting** on an unanswered technical question | 🔴 **Answer it, then `/6_convertit`** — 📌 **the document does not stand while one waits** |
| **Invocation 2's *No*** — `tracabilite.md` missing beside a question | 🔴 **The row its question's kind takes, above, already fired** — 📌 **add that the document does not stand without its preamble**: ⚠️ **never the row below** |
| Wrote an empty questions file, or found the document standing — ⚠️ **never a document without `# Preamble` or without `tracabilite.md`** | 📌 `/conventions`, then `/7_lots` — 🔴 the Cadreur reads the conventions in full. 📌 The merge, `/fusion_compare`, branches off here whenever you choose |

⚠️ **The short loop is an exception to the standing rule that every
answer goes back through `/1_lexique`** — 📌 **a technical answer brings
no product vocabulary**, and touches no block.

🔴 **Nothing else is yours**: no phase chain.

**If an agent returns a blocking file**: relay it and stop.
