# Phase 3 — Correct one agent

**Read this file whole before writing anything.**

🔴 **This is one pass among several.** The orchestrator runs this file
once per agent, and **tells you which one you are working on.**

📌 **`<name>` below is that agent's name**, as `verdict.md` writes it.
⚠️ **For an agent of ours the verdict kept or changed, that is our
file's name too** — `.claude/agents/<name>.md`.

**Write in English.**

---

## What this pass is for

**We want to know whether our agents are well built, and what exactly
to change in them.**

🔴 **You produce instructions, not a rewritten agent.** A rewritten file
hides the reasoning: to know what moved, we would have to diff four
hundred lines and guess which change carries an intention and which is
your way of saying the same thing.

📌 **A list of instructions carries only what moves** — we read it,
sort it, and accept it instruction by instruction.

**What the verdict said about your agent decides the shape of this
pass:**

| The verdict says | What this pass produces |
|---|---|
| **Kept as is** | 🔴 **Instructions all the same.** The verdict kept its role; that says nothing about how well it is written. ⚠️ **Go through *What to look for*, below** |
| **Changed** | Instructions — those the verdict asked for, **and everything *What to look for* turns up besides** |
| **New**, or **merged** | 🔴 **The agent written in full** — see *When the agent is new or merged* |
| **Dropped** | 🔴 **Nothing.** Write `docs/refonte/instructions/<name>.md` holding one line: *dropped by the verdict, no instruction*. ⚠️ **Write the file anyway** — its absence would read as a pass that never ran |

📌 **An agent with nothing wrong in it gives an empty list**, under the
same one-line form. 🔴 **That is a result, not a failure** — do not
invent an instruction to fill the file.

---

## What you read

🔴 **Six things at most, and nothing else** — 📌 the fifth only in one
case.

**1. The card for your agent in `docs/refonte/verdict.md`** — what the
verdict decided about it, and why. 📌 **Its card, not the whole
verdict.**

⚠️ **A card is `verdict.md`'s entry for one agent**: what it reads,
what its moves are, what it produces, how often it runs, and — for one
of ours — whether the verdict kept it, changed it, merged it or dropped
it. 🔴 **It stays macro**: turning its moves into an agent's full
instructions is this pass's work.

**2. Our agent, at `.claude/agents/<name>.md`** — 🔴 **in full.**
⚠️ **Without it no instruction is writable**: *drop move 6* means
nothing until you know what move 6 says.

**3. The grid it applies**, if it applies one — its own card says so.
⚠️ **You do not correct the grid here**: a grid serves several agents,
and a pass that sees one of them cannot judge it. 🔴 **A fault you find
in it goes under `## Consequences elsewhere`**, named as the grid.

**4. The instruction files already written**, in
`docs/refonte/instructions/` — 🔴 **their `## Consequences elsewhere`
sections only.** ⚠️ **One of them may name your agent**: a change
decided in an earlier pass that your agent has to follow.

📌 **You act on those** — 🔴 **write the instruction it calls for**, and
say which pass raised it.

**5. `.claude/agents/cadreur.md`** — 🔴 **only when you are writing an
agent in full**, and only for its conventions. ⚠️ **Not for what it
does.**

**6. Nothing else.** 🔴 **Not the other agents, not the brief, not the
other grids.**

📌 **Why not the neighbouring agents**: if a change here forces a change
there, 🔴 **you note it and do not touch it** — a later pass reconciles
the whole chain, and reading every neighbour would double the cost of
every pass for work that pass will redo.

---

## What judges an instruction

🔴 **Three measures, in this order.** 📌 **They are the same ones the
verdict was reached with** — you do not need to have seen it argued.

**1. Robustness** — how many gaps between what the idea asked and what
the code does. ⚠️ **This dominates.**

**2. Round trips** — turns between agents, retries, decisions asked of
the person.

**3. Tokens** — what is read, and how many times.

🔴 **Every instruction names the measure it moves, and how.**

⚠️ **An instruction that moves none of the three is a preference** — 📌
**do not write it.** **Rephrasing a sentence that already works is not
a correction.**

---
## What to look for

🔴 **This list is what we know goes wrong. It is not closed** — a fault
outside it is still a fault, and worth an instruction.

### In what the agent does

**A move that reaches less than it should** — 📌 it searches one folder
where two carry the thing, treats one case of a class that holds three.
⚠️ **Nothing signals it**: the move runs, and what it misses never
reports itself.

**A list where a class is meant** — 📌 the move enumerates cases instead
of naming what they share. ⚠️ **What is not in the list passes.**

**A test nobody can check** — 📌 *until it is coherent*, *precise
enough*. 🔴 **Two readers, two verdicts.**

**A move out of order** — 📌 one that needs what a later move produces,
or a constraint stated after what it constrains.

**A missing stop** — 📌 a situation where the agent cannot produce and
which it does not foresee. ⚠️ **It will invent.**

### In what it reads and writes

**A read no move uses** — 📌 paid at every invocation.

**A read that is missing** — 📌 a move rests on a fact nothing gives it.
🔴 **It will guess.**

**A read wider than needed** — 📌 a whole file where a section would do,
a file read where a grep would answer.

**The same thing read twice** — 📌 in one invocation, or by two agents
in a row for the same purpose.

**An output nobody reads** — 📌 a field the agent writes that no later
agent uses.

**An output larger than its reader needs** — ⚠️ paid again at every read
that follows.

### In how it sits in the chain

**A net** — 📌 a move that re-checks what an earlier agent already
guaranteed.

**Work done twice** — 📌 the agent recomputes what an earlier one wrote,
because it does not read its output.

**An invocation that produces nothing** — 📌 the agent is called in a
case where it has nothing to do. ⚠️ **The cost is paid anyway.**

**More context than one agent holds** — ⚠️ it degrades instead of
stopping, and nothing signals it.

**A split too fine** — 📌 two invocations where one would do, each
reloading the same context. 🔴 **The opposite fault of the one above,
and it costs too.**

**An avoidable round trip** — 📌 a question a reading would have
answered, or asked after work the answer invalidates.

**A loop with no ceiling** — 📌 nothing bounds the number of turns.

### In how it is written

**A forbidden thing matching no rule** — 📌 an entry under *what you
never do* that nothing in the body asks for, or a rule in the body with
no matching entry.

**Two passages of one agent asking for different things.**

### In whether it stands on its own

🔴 **An agent is read by something that has seen nothing else.** ⚠️
**No earlier agent's file, no other phase, no conversation** — what it
does not say, its reader does not know.

**A term used and never defined** — 📌 a name for an artefact, a field,
a state, a shape. ⚠️ **Obvious to whoever wrote the chain, not to the
agent running alone.**

**A reference to something the reader has not seen** — 📌 *as the
previous agent produced*, *in the same format as before*, *the usual
shape*. 🔴 **Name it, or describe it on the spot.**

**A count that no longer matches** — 📌 *four things and nothing else*
above a list of five, *the three checks* where there are now four.
⚠️ **A number stated once and changed nowhere else.**

**A placeholder with no rule** — 📌 `<name>`, `<lot>`, `<agent>` used
without saying what fills them and where it comes from.

**An instruction that reads two ways** — 📌 *drop move 5* after a
reorder: move 5 before, or after? 🔴 **Two readers, two different
actions.**

**A file named without a path**, or 📌 **a path that only holds in one
of the cases the agent handles.**

---

## What you write

🔴 **One file**: `docs/refonte/instructions/<name>.md`.

**One entry per instruction, in the order they are to be applied:**

    Fichier      : <the agent file>
    Opération    : add a move | drop a move | reorder | replace text |
                   move to <other agent> | add a section |
                   merge two moves | …
    Cible        : where exactly — move 6, the "What you read"
                   section, the order of moves 4 to 7
    Aujourd'hui  : what is written there, or "nothing"
    Après        : what should be written, or "dropped"
    Justification: which measure moves, and how

📌 **The `Opération` field forces the scale to be declared.** ⚠️ **An
instruction whose operation you cannot name is style, not correction.**

🔴 **Each instruction reads against the state the ones before it
produced.** ⚠️ *Reorder moves 4 to 7* then *drop move 5* is ambiguous
unless the second means move 5 **after** the reorder — 📌 **write them
so that applying them top to bottom works.**

### What you note but do not do

🔴 **A change here that forces a change elsewhere** — name the other
agent and what would have to follow, under a closing section:

    ## Consequences elsewhere

    <other agent> : <what would have to change, and why>

📌 **You do not write instructions for that agent** — it has its own
pass. 🔴 **A pass that runs after yours reads this section**, and the
reconciliation pass at the end reads what nobody picked up.

⚠️ **Write it even when you think the other pass will see it anyway** —
📌 **it is the only channel between passes.**

---

## When the agent is new or merged

🔴 **Then there is no base, and you write the agent in full**, to
`docs/refonte/agents/<name>.md`.

**Read, in addition to the six above**: every one of our agents the
verdict says it merges — 🔴 **in full**, because a move you drop
silently is a move nobody will notice is gone.

**Match our conventions.** 🔴 **Read `.claude/agents/cadreur.md` in
full for them** — ⚠️ **for style only, not for what it does.** 📌 **It
is the one to copy from**: it is long enough to show every convention
at work.

- **Frontmatter** — `name`, `description` as one sentence a router
  matches on, `tools` naming only what is used, `model`, `effort`
- **Sections** — `## Role`, `## What you read`, `## What you write`,
  `## What you never do`, in that order, plus what the agent needs
  between them
- **Prose** — present indicative, active voice; one instruction, one
  sentence
- 🔴 **A list never states more than the class it covers** — where you
  would enumerate cases, name the class. ⚠️ **An agent given a list
  copies the list**, not the class behind it

🔴 **And whatever its role, every agent needs**: a stated condition
under which it cannot produce and stops, what it writes then, and how
it resumes after being unblocked.

---

## What you do not do

- 🔴 **Rewrite an agent the verdict did not call new or merged** —
  instructions, not a file
- 🔴 **Write an instruction whose justification names no measure**
- 🔴 **Write instructions for an agent other than yours**
- 🔴 **Read beyond the six things named above**
- 🔴 **Correct a grid** — note the fault, leave the grid alone
- 🔴 **Invent an instruction to avoid an empty file** — an agent with
  nothing wrong gives an empty list
- 🔴 **Edit anything under `.claude/`** — our chain stays as it is
- Ask questions — decide, and note where you were unsure
