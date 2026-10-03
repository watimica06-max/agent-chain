---
description: Cut a technical document into lots and derive the execution sequence
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **downstream splitting mode**.

**This command runs `cadreur`, once.** 🔴 **It calls the Vérificateur
itself**, corrects what it reports, and calls it again — ⚠️ **three
rounds at most, which it counts.**

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant. `Next: stop argument missing`

Feature folder: `docs/features/$ARGUMENTS/`

🔴 **The working folder is the highest `bugfix-NN/` in it, if there is
one; the feature folder itself otherwise.** A bug-fix cycle keeps
everything it produces inside its own folder.

📌 **Same structure either way**: the technical document at the root —
`spec-technique.md` or `desc-bug.md` — and `code/` beside it.

📌 **Every path below is relative to the working folder.**

---

## What you read

**`code/sequence.md`** — 📌 **its `## Defects` section**, to know
whether the split holds, 🔴 **its `block-N:` lines under `## Blocks`**,
to count the blocks, **and its `## Redécoupage: archivable` line**, when
there is one — see *How it runs*.

**`code/redecoupage.md`**, when it is there — 🔴 **its `## Ce qui
revient` and `## Ce que j'en fais` sections alone**, to relay them. 📌
**Read before you rename it** — see *How it runs*.

**`code/decoupage.md`** — 🔴 **its `## lot-` headings alone**, to count
the lots. ⚠️ **Never a lot's content.**

**`spec-technique.md`** — 🔴 **a grep of `^### §` alone**, to count the
entries — see *Git, before invoking*. ⚠️ **Never an entry's content.**

📌 **Each agent declares its own inputs**; you pass the feature folder
and nothing else.

`CLAUDE.md`'s standing reading rules apply: never open
`CURRENT_TECHNICAL_STATE.md`.

---

## Git, before invoking

🔴 **File away every root `questions-*.md` first** — the upstream loop
is over and nothing downstream reads them:

    git mv docs/features/<name>/questions-<agent>-NN.md \
           docs/features/<name>/questions/<agent>/

⚠️ **`git mv`, never a read-and-rewrite.** 📌 **Create the folder if it
does not exist.**

⚠️ **Never `questions-architecte-*.md`** — 🔴 **leave it at the root**:
📌 **it waits for `/conventions`, which is the only command that reads
it.**

🔴 **Then commit the feature folder**, before creating the worktree:

    git add docs/features/<name>/ && git commit -m "chore: pre-split"

📌 **Nothing to commit is a normal outcome** — carry on.

🔴 **Then, when the document is `spec-technique.md`, grep `^### §` in
it.** 📌 **No hit — every section holds `*(empty)*`** → ⚠️ **the feature
has nothing to build**: 🔴 **cut no split, create no worktree, invoke
nothing, name no next command.** 📌 **Say where its content lives** —
`par-genre/recette.md` at the feature folder's root, and the preamble's
`## Cross-cutting rules` in the technical document — **then `/fusion`** —
`Next: run /fusion <name>`.
⚠️ **Accepted cost: `/9_controle` does not run, so
`code/recette-ordonnee.md` is never written** — the recette stays
readable in `par-genre/recette.md`; ordering it against zero lots means
nothing.

🔴 **Then create a worktree from local `HEAD`, and register it:**

    git worktree add .claude/worktrees/<name> HEAD

⚠️ **Never let the tooling branch it for you** — its default base is
`origin/master`, which can sit several commits behind local. An agent
would then work on stale content and its output would have to be
discarded. *(Seen once: a whole invocation lost that way.)*

📌 **Enter the worktree before invoking the agent**, not after it
fails — the harness blocks a subagent's writes until the session is
isolated.

---

## How it runs

🔴 **First, remove `code/blocked_verificateur.md` if it is there** — 📌
**`git rm`.** ⚠️ **It belongs to the previous run**: its cause is either
fixed, and the file is a lie, or still there, and the Vérificateur
writes it again. 🔴 **Nothing else retires it** — 📌 **it carries no
`## Decision`, so no rename closes it**, and every later audit would
list it as a block still waiting.

🔴 **The command is the trigger, never the state of the folder** — 📌
**it produces a split in every state but one.**

⚠️ **What the Cadreur does with an existing one depends on what sits
beside it**, and it is not yours to decide:

| On disk | What it does |
|---|---|
| `code/blocked_cadreur.md` whose **last** `## Decision` is **empty** | 🔴 **Nothing** — it stops and says the block stands — ⚠️ **unless the request its `## Where` names carries a filled `## Verdict`**: that verdict lifts it |
| `code/blocked_cadreur.md` whose **last** `## Decision` is **filled** | 📌 **Applies it**, then carries on with whatever else sits there |
| Nothing | A first split — the whole document |
| `code/sequence.md` whose `## Defects` **carries lines** | 🔴 **Corrects only the lots those defects name** — the rest stays |
| `code/redecoupage.md` | 🔴 **Re-splits what coding sent back** — see below |

📌 **A blocking file holding several blocks, one set of headings each,
is read on its last `## Decision`** — ⚠️ **the earlier ones were applied
in earlier runs**, and a block raised in the run that applied one is
appended below it, as a fresh block.

🔴 **Once the Cadreur has handed back, grep `code/sequence.md` for
`## Redécoupage: archivable`.** 📌 **The line is there** → 🔴 **rename
`code/redecoupage.md` yourself**:

    git mv code/redecoupage.md code/redecoupage-NN.md

📌 **`NN`: the highest in the folder plus one, `01` when there is
none.** 🔴 **That line, read from the file, is the trigger** — ⚠️ **the
Cadreur relays it in its report as a courtesy, and the report is not
what you key on.** 📌 **The Vérificateur writes it only on a round whose
`## Defects` is empty** — 🔴 **left at the unnumbered name, every later
run dispatches to block C**, and `/8_code` sends the split back for
ever.

🔴 **Then remove that line from `code/sequence.md`** — 📌 **the trigger
is consumed with the archive**: ⚠️ **left in place, a later run would
find a stale one** and archive a file nothing had re-split.

🔴 **Before the `git mv`, read its `## Ce qui revient` and `## Ce que
j'en fais`** — 📌 **you relay both, on every redécoupage**, see *What
you relay*. ⚠️ **Renamed first, the file carries a number you would
have to guess.**

📌 **Pass the working folder; it reads the folder itself.**

⚠️ **Never restore a deleted file from git history.** A missing split
means the Product Owner wants a new one; diagnosing why it went
missing is not your call.

🔴 **Unless `code/redecoupage.md` is there.** 📌 **Then coding sent the
split back**, and lots are already coded and merged — ⚠️ **overwriting
their entries would describe something that is not in the tree.**

🔴 **Say nothing about it in the prompt.** 📌 **The Cadreur dispatches
on what sits on disk** — ⚠️ **a paraphrase competes with its own
instructions**, and this command says so itself.

📌 **They know what to do with it** — the Cadreur leaves the coded lots
closed and adds lots for what has to change, the Vérificateur keeps
them where they ran and writes `## Redécoupage: archivable` when the
sequence is
written.

**One invocation: `cadreur`.** 🔴 **It calls the Vérificateur itself**,
reads the defects, corrects, and calls it again — 📌 **three rounds at
most, which it counts.**

⚠️ **You do not run `verificateur`** — 🔴 **and you do not loop.** 📌
**You invoke the Cadreur once and read what comes back.**

**When it hands back**, look at what is on disk — 🔴 **first row that
matches, top to bottom**: ⚠️ **the Vérificateur writes no `sequence.md`
when it blocks**, and the previous one still stands with its empty
`## Defects`.

| What you find | What you do |
|---|---|
| `code/blocked_verificateur.md` | 🔴 **Stop.** 📌 **Relay which file was missing** — ⚠️ **it carries no `## Decision`**: nothing in it is the Product Owner's to settle, and the step before it has to run again — `Next: stop input missing: <file> — the step before it has to run again` |
| `code/sequence.md` whose `## Defects` **carries no line** | 🔴 **The split holds.** See *the pending requests*, then stop and report — `Next: run /8_code <name>` |
| `code/sequence.md` whose `## Defects` **carries lines**, and no blocking file | 🔴 **Stop** — 📌 **relay the defects**: the three rounds did not clear them — `Next: stop defects remain after three rounds` |
| `code/blocked_cadreur.md` **and** the `# Request N` its `## Where` names, in `architecte/cadreur.md`, with an **empty** `## Verdict` | 📌 **The conventions fall short**: invoke `architecte`, invocation 3, then invoke `cadreur` again |
| The `# Request N` its `## Where` names with a **filled** `## Verdict`, and the Cadreur has not yet reported on it | 📌 **The Architecte has answered** — 🔴 **invoke `cadreur`**: the verdict is what lifts its block |
| The Cadreur reports **block standing** — `code/blocked_cadreur.md`, last `## Decision` empty, nothing lifting it | 🔴 **Stop.** Relay it — the Product Owner fills `## Decision`, and the Cadreur reads it on its next run — `Next: answer blocking, then run /7_lots <name>` |
| The Cadreur reports **verdict refused** | 🔴 **Stop.** 📌 **Relay the request and its verdict** — ⚠️ **never invoke `cadreur` again on it**: nothing it can cut changes, and the Product Owner decides — `Next: stop verdict refused: <request>` |
| The Cadreur reports **decision applied**, and the file's last `## Decision` is filled — or reports **verdict applied** | 🔴 **Rename the file** — 📌 **the agent has no tool that removes one:**<br>`git mv code/blocked_cadreur.md code/blocked_cadreur-NN.md`<br>📌 **`NN`: the highest in the folder plus one, `01` when there is none.** ⚠️ **Anything left at the unnumbered name reads as a block still standing** |

🔴 **The Cadreur's report states the outcome on the blocking file in
one of four terms** — *decision applied* · *verdict applied* · *verdict
refused* · *block standing* — 📌 **and that line is what the rename and
the relay key on.** ⚠️ **A *decision applied* whose last `## Decision`
is empty is a block raised in that same run**, appended below the one
applied: 🔴 **the file stays at its unnumbered name**, and you relay it
as a block standing.

🔴 **The two conventions rows key on one request, never on the whole
of `architecte/cadreur.md`** — 📌 **the file holds every request this
split raised, one `# Request N` heading each**, and a mixed file — one
verdict filled, another empty — is read block by block: ⚠️ **the
`# Request N` the blocking file's `## Where` names — as
`architecte/cadreur.md — Request N` — is the one that counts.** 🔴
**Read the number from `## Where`, then the block under that heading**
— 📌 **a `## Where` naming the file alone points at every request it
holds**, and you cannot tell which verdict lifts it: neither
conventions row matches, and the file is a block standing.

📌 **A `blocked_cadreur.md` at the third round** names what would not
converge. ⚠️ **That is not a failure of the command** — 🔴 the split
does not converge, and the Product Owner decides.

### The pending requests

📌 **Once the split holds**, glob `architecte/`. **Any request with an
empty `## Verdict`** → `architecte`, invocation 3.

🔴 **A request with no `## Verdict` heading at all reads as one with an
empty one** — 📌 **here and in the table above alike**: the Architecte
adds the heading and writes under it.

🔴 **One invocation, whatever their number.** ⚠️ **Then stop** — the
conventions changed after the split was cut, and `/8_code` runs against
both: `Next: run /8_code <name>`.

```
Agent(
  subagent_type="architecte",
  model="opus",
  description="Requests <the working folder>",
  prompt="Working folder: <the working folder>. Invocation 3 — Requests. Called by the orchestration."
)
```

📌 **The prompt says who called** — 🔴 **`Called by the orchestration.`,
never inferred**: the Architecte behaves differently when the Arbitre
calls it.

📌 **If `architecte` blocks in turn** — `blocked_architecte.md` at the
working folder's root — **stop.** 🔴 **It blocks on a missing input,
the conventions file first of all** — ⚠️ **not on the request**: a
doubt or a product matter goes in the verdict. 📌 **Say to run
`/conventions`** — `Next: run /conventions <name>`.

⚠️ **You never invoke the Arbitre here.** 📌 **What the Cadreur and the
Vérificateur block on is mechanical** — a missing document, an
unreadable list, a convention that forbids what a lot needs. 🔴 **None
of it is settled by looking at the corpus**, and the last one goes to
the Architecte.

🔴 **Never paraphrase an agent's process in your invocation** — not its
inputs, its checks, its output format. It reads its own instructions.

### Invocation parameters

```
Agent(
  subagent_type="cadreur",
  model="opus",
  description="Split <feature>",
  prompt="Working folder: <the working folder>."
)
```

🔴 **Pass the working folder, never the feature folder.** On a bug-fix
cycle they differ, and the agent would read the wrong one.

📌 **`cadreur` runs on `opus`** — it decides the whole structure, and
an error here spreads to every lot. ⚠️ **You never invoke
`verificateur`**: the Cadreur does, with the model its own frontmatter
names.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — 📌 **the Cadreur keeps its context
across the rounds**, and branching would cut it from what it just
cut.

📌 **The Cadreur finds by itself what brought it back** — a
`## Defects` section, or a `code/redecoupage.md`. 🔴 **Say nothing about
it in the prompt**: it reads its own instructions, and a paraphrase
would compete with them.

---

## Git, once it has reported

**Then, once the Cadreur — or the Architecte, when *the pending
requests* ran it — has reported — 📌 five steps, in this order:**

1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the
   agents have no Bash and commit nothing**, and the renames of *How it
   runs* — `code/redecoupage-NN.md`, `code/blocked_cadreur-NN.md`, the
   `git rm` of `code/blocked_verificateur.md`, the line removed from
   `code/sequence.md` — are staged, not committed. 🔴 **So is what the
   Architecte, invocation 3, leaves** — 📌 **each request's verdict
   under `architecte/`, `docs/TECHNICAL_CONVENTIONS.md` and the feature
   folder's `couverture.md`** — ⚠️ **a `git add` that reaches them
   all**, never the working folder alone; 📌 **`git merge` takes the
   branch's commits, not the worktree's files**, and `git worktree
   remove` refuses a dirty tree
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
never of an agent: none of them was to commit it. Forcing the removal
destroys it.

🔴 **The push is part of the merge, not an afterthought.** A phase that
sits only on the local machine is lost with it.

⚠️ **A push that fails — diverged remote, no network — is reported, not
retried and not worked around.** The merge holds locally; say so and
carry on.

🔴 **Merge before handing back, always** — including a
`blocked_*.md`: the Product Owner has to see it.

---

## What you relay

**Where the split stands**: how many lots, how many blocks, any defect
left — 🔴 **and the Vérificateur's remark when a ceiling forced a block
it would not have cut that way**: 📌 **the Cadreur carries it in its
report, you relay it with the lots, the blocks and the defects** — it
reaches the Product Owner, who moves the ceilings. 🔴 **Nothing else is
yours** — no judgement on the split itself, and no reading of git
history to explain what a run found.

🔴 **The relay ends on its `Next:` line**, in `CLAUDE.md`'s grammar —
📌 **every ending of this command names its own**, stops included.

**On every redécoupage**: 🔴 **the `## Ce qui revient` and `## Ce que
j'en fais` of `code/redecoupage.md`**, read from the file before you
rename it — 📌 **the Cadreur wrote them there at the end of its run**,
and the Product Owner sees the pattern without opening the file.
⚠️ **A third return says the split is not the problem the split can
solve**, and she decides — 📌 **her decision goes into
`code/redecoupage.md` under `## Décision du Product Owner`, then
`/7_lots` by hand**: 🔴 **the Cadreur's block C reads it as her
instruction**, and `/8_code` counts the returns from that heading —
`Next: manual écrire sa décision sous ## Décision du Product Owner dans
code/redecoupage.md, then run /7_lots <name>`.

**If an agent returns a `blocked_*.md`**: 🔴 **relay it and stop**,
naming the file. 📌 **The Product Owner fills `## Decision`**, and the
Cadreur reads it on its next run — `Next: answer blocking, then run
/7_lots <name>`.

⚠️ **Except a `blocked_cadreur.md` whose `## Where` names a request
with an empty `## Verdict`** — 📌 that one goes to the Architecte, and
the Cadreur runs again.

⚠️ **And except `code/blocked_verificateur.md`** — 🔴 **it carries no
`## Decision`**: nothing in it is the Product Owner's to fill. 📌
**Relay which file was missing**, and the step before it has to run
again.
