---
description: Structure the idea file into a product file
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent
argument-hint: "<feature folder name>"
---

Act as the orchestrator, in **upstream mode**.

**This command invokes `redacteur`, invocation 1 or 2.**

📌 **It runs as many times as needed.** With no questions file it reads
`idees.md`; with one, it integrates the answers instead.

**The argument is mandatory**: the feature folder name. Without it, ask
for it and stop — never guess which feature is meant.

Feature folder: `docs/features/$ARGUMENTS/`

---

## What you read

🔴 **Four reads, and nothing else:**

- **An `ls` of the feature folder's root** — before the run, and again
  after
- **The `## Decision` heading of `blocked_redacteur.md`**, when there is
  one — 📌 **that heading alone**
- **A grep for an empty `Answer:`** in the file to integrate, and in the
  lexicographe's
- **A grep of `^### Q`** in the questions file the agent wrote

📌 **You pass the agent the file it reads; it does not look for
itself.** 🔴 **You never read a questions file's entries** — the greps
above are counts, not reading.

⚠️ **`CLAUDE.md`'s standing reading rules apply**: never open
`CURRENT_TECHNICAL_STATE.md` or `CALIBRATION_RISK_LEVEL.md`.

---

## How it runs

**First, the lexicographe's questions file.** 🔴 **Grep it for an empty
`Answer:` before touching it** — ⚠️ **one hit and you stop**, and say
which questions wait: `/1_lexique` has not finished.

📌 **Nothing waiting → file it**, 🔴 **the choice of invocation below
reads the root after it:**

    git mv docs/features/<name>/questions-lexicographe-NN.md \
           docs/features/<name>/questions/lexicographe/

⚠️ **A file put away in `questions/lexicographe/` is read by no command
again** — 📌 **filing an unanswered one loses its answers for good.**

⚠️ **`/1_lexique` reads the root to know which invocation it is** — 📌
**a lexicographe file left there and an answered file beside it read as
its fourth**, when its work is done.

📌 **Create `questions/lexicographe/` if it does not exist.** ⚠️
**Nothing to file is a normal outcome.** 📌 **What remains at the root
is the file to integrate — one at most.**

**Then, the blocking file.** 🔴 **Does `blocked_redacteur.md` sit in
the feature folder?**

| | What you do |
|---|---|
| Absent | 📌 Carry on |
| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands |
| Its `## Decision` is filled | 📌 **Name it in the prompt**, beside the file to read |

⚠️ **Read that one heading, nothing else** — 📌 the agent reads the
file.

**Then, which invocation and which file:**

| At the root | Invocation | What you name |
|---|---|---|
| No questions file, **and no `desc-produit.md`** | **1 — Structuring** | `idees.md` |
| No questions file, **and a `desc-produit.md`** | 🔴 **Stop** — 📌 **the idea file is transcribed once**; say `/3_decoupe` comes next | — |
| One, **with no `### Q`** | 🔴 **Invoke nothing** — 📌 **nothing to integrate**; say `/3_decoupe` | — |
| One, any prefix | **2 — Integrating** | 🔴 **That one** |
| More than one | 🔴 **Stop** — a filing failed; say which files | — |

⚠️ **A second invocation 1 over an existing product file renumbers or
duplicates every block** — 📌 **and every filed question then points at
the wrong one.**

⚠️ **Any prefix** — 📌 the agent integrates the answers whichever agent
asked.

🔴 **If it carries an empty `Answer:`** — 📌 **stop**, and say
which questions are waiting.

```
Agent(
  subagent_type="redacteur",
  model="sonnet",
  description="Structure <name>",
  prompt="Feature folder: docs/features/<name>/.
          Invocation <1 — Structuring, or 2 — Integrating>.
          Read: <idees.md, or questions-<agent>-NN.md>.
          <Plus: blocked_redacteur.md, its decision is filled.>"
)
```

🔴 **Name the file, always** — ⚠️ **the agent opens that one and no
other.**

### Once it has run

🔴 **Did the run create a `NEW` block?** 📌 **Grep `NEW` in
`desc-produit.md`** — ⚠️ **and only then:**

    rm -rf docs/features/<name>/par-genre/ \
           docs/features/<name>/desc-par-nature.md \
           docs/features/<name>/spec-technique.md

📌 **Nothing there → nothing to delete**, a normal outcome.

⚠️ **Why**: those two are derived from the product file. 🔴 **A block
created after the conversion leaves a `spec-technique.md` that does not
carry it** — the split and the coding then run on a technical document
missing a block, and the gap surfaces at the controleur.

🔴 **Say which files you deleted**, or that none needed it.

🔴 **A blocking file you named is filed:**

    git mv docs/features/<name>/blocked_redacteur.md \
           docs/features/<name>/blocked_redacteur-NN.md

📌 **`NN`: the highest `blocked_redacteur-NN.md` in the folder plus
one — `01` when there is none.**

⚠️ **Anything left at the unnumbered name reads as a block still
standing**, and the next run stops on it.

🔴 **At invocation 2, file the questions file it integrated**, into
`questions/<agent>/`, inside the worktree before the merge — 📌 **integrated, it waits for nothing**; ⚠️ **left
at the root beside the Rédacteur's own, the next command could not tell
which one waits.**

🔴 **Check `questions-redacteur-NN.md` was written** — ⚠️ **a missing one
stops the command**: the agent says it writes one every time.

🔴 **Never paraphrase the agent's process in your invocation** — not
its inputs, its checks, its output format. It reads its own
instructions.

❌ No `effort` parameter. ⚠️ **`run_in_background` may not exist
either** — in this environment the Agent tool always runs async and
notifies on completion. Do not pass it; wait for the notification.

❌ **Never pass `isolation`** — the phases are sequential
and each reads what the previous one wrote.

---

## Git, in this mode

📌 **The lexicographe's questions file was filed first** — see *How it
runs*.

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

**Then, once the agent reports:**

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

The agent's own report.

**What to run next** — 📌 **indications for the Product Owner.**
⚠️ **You relay them; you run nothing after this command.**

🔴 **First match wins:**

| What just happened | Next |
|---|---|
| It wrote a blocking file | 📌 Fill its `## Decision`, then `/2_structure` again |
| Its questions file holds questions | 🔴 **Answer them, then `/1_lexique`** — a flag stands until answered, and nothing downstream runs meanwhile |
| Its questions file is empty | 📌 `/3_decoupe` — 🔴 a new block is split, classed and framed before the Convertisseur reads it |

🔴 **Nothing else is yours**: no phase chain, no risk level, no
`TaskCreate`.

**If it returns a `blocked_*.md`**: relay it and stop.
