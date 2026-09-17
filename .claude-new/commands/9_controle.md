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

**The argument is the working folder** —
`docs/features/<name>/`, or `docs/features/<name>/bugfix-NN/`.

📌 **Every path below is relative to it.**

🔴 **Which cycle you are on is read from the folder name** — 📌 **a
`bugfix-NN` segment means a correction cycle.**

| | What runs |
|---|---|
| **A feature folder** | 🔴 **All six phases** |
| **A `bugfix-NN/`** | 📌 **Phases 4 to 6 only** — ⚠️ **the Contrôleur confronts a product file with the sheets built from it, and a correction cycle has neither** |

---

## What you read

📌 **At phase 1**: `tracabilite.md`, and the `Anchor:` lines of
`code/decoupage.md` **by grep** — 🔴 **never either file whole.**

**Then only whether `desc-produit.md` is there**, and whether every lot of
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

🔴 **`desc-produit.md` absent, on a feature folder** — 📌 **say so and
stop**: there is nothing to confront the sheets with.

🔴 **Stop if a lot of the sequence has no `verdict.md` in PASS** — name
it. 📌 **On a correction cycle, the sequence and the lots are the
bugfix folder's own** — ⚠️ **phases 4 to 6 read `code/` under the
working folder, whichever it is.**

⚠️ **He would otherwise read an incomplete set of sheets** — 📌 **and
report an intention as missing when it is merely unwritten.**

📌 **An existing `rapport-controle.md` is not a reason to stop.** He
writes the next free number beside it; that is how two states are
compared.

---

## Git, before invoking

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

---

## How it runs

**Six phases.**

🔴 **`tracabilite.md` absent, on a feature folder** — 📌 **phase 1 reads
it**: say so and stop, the conversion did not finish.

📌 **`code/recette.md` absent** — ⚠️ **normal, not a stop**: no lot had
a criterion beyond a test. 🔴 **Phase 4 then builds from
`par-genre/recette.md` alone**, and says the other source was empty.

### Phase 1 — build the block-to-lot map

🔴 **Two greps and a crossing**, no agent.

🔴 **Keep the blocks carrying `Genre: comportement` alone** — 📌 **the
other four genres produce no lot by construction**, and each is taken
up elsewhere:

| Genre | Where it is taken up |
|---|---|
| `recette` | 📌 **Phase 4** — `par-genre/recette.md` feeds `code/recette-ordonnee.md` |
| `directive` | 📌 **The Architecte** turned it into a conventions rule |
| `référence` | 📌 **The Convertisseur**, §9 Text of the technical document |
| `hors périmètre` | ⚠️ **Set aside by the Product Owner, explicitly** |

⚠️ **Say how many blocks you kept and how many each genre set aside** —
🔴 **so none of them reads as dropped.**

**a.** `tracabilite.md` gives block → entries.

**b.** The `Anchor:` fields of `code/decoupage.md` give entry → lots.

🔴 **Plus its `## Entries with no lot` section** — 📌 **an entry the code
already carries**: ⚠️ **mark those entries `carried`**, never as a block
with no lot. 🔴 **Without it the Contrôleur reports their intentions
missing**, and they were built before this feature ran.

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

**d.** 🔴 **Check the crossing before going on** — 📌 **count the blocks
of `tracabilite.md` and the lines of `tracabilite-full.md`**: ⚠️ **they
match, or a block was lost in the join.**

🔴 **And grep every lot of `code/decoupage.md` in it** — 📌 **a lot
appearing in no line built no entry any block names**, which is either
a split defect or a crossing defect. ⚠️ **Say which lots, and stop.**

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
          Group: G1.
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
          Blocks per group, one line each:
            G1: B1, B2, B3
            G2: B4, B5
            ..."
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
she wanted to check herself.

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

🔴 **Two sources**: 📌 **the `## Doubts` and `## Intentions missing`
sections of `code/rapport-controle*.md`** — the latest one — **and the product
questions the Arbitre handed back**, in the numbered blocking files.

🔴 **They sit at two depths** — 📌 **`code/blocked_*-NN.md`** for the
Cadreur and the Détailleur, **`code/<lot>/blocked_*-NN.md`** for the
four agents of the loop. ⚠️ **Glob both** — 🔴 **the unnumbered ones are
still open**, and not yours to read.

🔴 **One case per line, and you conclude nothing.** ⚠️ **No class
proposed, no grid change suggested** — 📌 **an isolated case says
nothing; ten together let a shape show.**

📌 **Its reader is the Product Owner, across cycles** — 🔴 **she decides
whether a recurring kind of escaped question becomes an entry of
`GRILLE_CADRAGE_PRODUIT_V2.md`.** ⚠️ **Append, never overwrite**: the
file is the record of every cycle, not of this one.

**Write `code/registre-questions.md`.**

📌 **On a correction cycle** — 🔴 **the Arbitre's files alone**: there
is no control report.

### Phase 6 — the product decisions taken while coding

🔴 **A product question settled during the coding went into a sheet** —
📌 **never into the product file, never into the global.**

🔴 **Gather them from the same two depths as phase 5**: 📌 **every
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

## Git, once it has reported

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
| `code/registre-questions.md` | 🔴 **Read by the Product Owner, across cycles** — 📌 **a kind of product question that keeps escaping upstream is a question the framing grid is missing** |
| `code/decisions-produit.md` | 📌 **Read by the Rédacteur at `/fusion`** |

🔴 **Nothing else is yours**: no reading of those files, no summary of
what they hold, no decision on what to do next.

📌 **The Product Owner reads them and decides** whether the control
report becomes a `bug-list.md` for a correction cycle.

⚠️ **The manual list is the one to run before deciding** — 📌 **a gap
the Contrôleur cannot see shows there.**
