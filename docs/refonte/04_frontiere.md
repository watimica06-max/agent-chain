# Phase 4 — Examine a boundary

**Read this file whole before writing anything.**

🔴 **This is one pass among several.** The orchestrator runs this file
once per group, and **tells you which agents are in yours, and which
artefact they share.**

**Write in English.**

---

## What this pass is for

**Every agent of your group has already been examined on its own.**
🔴 **This pass looks at what none of those passes could see: what
happens between them.**

📌 **Our chain runs on separate contexts.** ⚠️ **An agent never sees
another's file** — it writes something, and something else reads it,
and neither has ever seen the other. 🔴 **That is where this chain
fails**, and a defect there survives precisely because it is invisible
from either side.

🔴 **You produce comments, not a rewritten agent.** 📌 **We apply the
corrections ourselves, one by one.**

**What is not yours:**

- 🔴 **A defect inside one agent** — 📌 **its own pass judged it.**
  ⚠️ **Even one you would have written differently: do not reopen it.**
- 🔴 **An agent outside your group** — 📌 **name what you would need and
  leave it.**

---

## What you read

🔴 **Four things, in this order. The fourth comes last, and that
matters.**

**1. Every agent of your group**, at `.claude/agents/<name>.md` —
🔴 **in full.** ⚠️ **A boundary is only visible from both sides at
once**: this is what this pass costs, and why it is a separate pass.

**2. Every command that invokes one of them**, in `.claude/commands/`.
📌 **Find them by grepping each agent's name.** 🔴 **In full.**

📌 **A command carries half the boundary**: what it puts in the prompt,
what it checks between two agents, what it files, renames or deletes
between them. ⚠️ **An artefact can be perfectly written and perfectly
read, and the command between them moves it somewhere neither
expects.**

**3. The comment file of every agent of your group**, in
`docs/refonte/agents/` — 🔴 **the `## What another agent would settle`
sections only.** 📌 **Those are the questions the individual passes
could not answer.** ⚠️ **Some are yours to settle now.**

**4. `docs/refonte/verdict.md`, sections 4 to 7** — 🔴 **only once you
have written everything the sweep below turns up.**

⚠️ **Read it first and it becomes your list.** 🔴 **Read it last and it
is a check.**

**Nothing else.** 🔴 **Not the grids, not the process files, not the
brief, not an agent outside your group.**

---

## What you are looking for

🔴 **The shared artefact is the subject.** 📌 **The orchestrator names
it** — a file one agent writes and another reads.

⚠️ **Sweep it, do not search it.** 🔴 **Every part of that artefact —
every section, field, marker, line, naming rule — gets its turn**,
including the ones you find nothing wrong with. 📌 **A defect lives in
what nobody thought to look at.**

### 1. Written and read

**For every part of the artefact:**

| | |
|---|---|
| **Who writes it** | The agent, and the move |
| **Who reads it** | The agent, and the move |
| **Same thing on both sides?** | 🔴 **The writer's meaning and the reader's, word for word** |

📌 **Three defects come out of this table:**

- **Written and never read** — ⚠️ **paid at every write, and at every
  read of the whole**
- **Read and never written** — 🔴 **the reader will guess**
- **Read as something else** — 📌 **the same field, two meanings.**
  ⚠️ **Neither agent is wrong on its own.**

### 2. What the reader takes for granted

🔴 **List what the reading agent assumes, rather than checks**: a state
of the artefact, a shape, an ordering, a completeness, something an
earlier agent is supposed to have guaranteed.

**For each: who establishes it, and where?** 📌 **Quote the move.**

⚠️ **Nobody establishes it** — 🔴 **that is the most expensive defect
this chain produces**, and the one that reaches the code.

### 3. Guaranteed twice

🔴 **Something one agent establishes and another re-establishes.** 📌
**One of the two is paid for nothing.**

⚠️ **Say which one should keep it** — 📌 **the one that can still act on
it, usually the earlier.** 🔴 **Not both, and never a third to watch the
second.**

### 4. What the commands do between them

📌 **Between the two agents, a command runs.** 🔴 **What it moves,
renames, deletes, checks or passes on:**

- **Does what it checks match what the next agent needs?**
- **Does what it files or deletes leave the reader what it expects to
  find?**
- **Does the prompt it writes name every file the reading agent's moves
  require?**

### 5. The questions the individual passes left

🔴 **Every entry of the `## What another agent would settle` sections
you read.** 📌 **One of three outcomes, and say which:**

- **Settled here** — with what you found
- **Still open** — it needs an agent outside your group; 📌 **name
  which**
- **Not a real question** — the agent's file already answers it;
  📌 **quote it**

---

## What judges a comment

🔴 **Three measures, in this order.**

**1. Robustness** — how many gaps between what the idea asked and what
the code does. ⚠️ **This dominates.**

**2. Round trips** — turns between agents, retries, decisions asked of
the person.

**3. Tokens** — what is read, and how many times.

🔴 **Every comment names the measure it moves, and how.** ⚠️ **A comment
that moves none of the three is a preference** — 📌 **do not write
it.**

---

## What you write

🔴 **One file**: `docs/refonte/groupes/<group>.md`, the group's name as
the orchestrator gives it.

**One entry per comment:**

    Fichier      : <the agent or command file the change lands in>
    Cible        : where exactly
    Aujourd'hui  : what is written there, or "nothing"
    Le défaut    : what breaks between the two agents, and which of the
                   five above it is
    Ce qu'il faut: what should hold instead — 🔴 the intent, not the
                   sentence to paste
    Justification: which measure moves, and how

⚠️ **A comment here often lands in one agent's file** — 🔴 **say why it
took two agents to see it.** 📌 **Otherwise it reads as something the
individual pass missed, and we would wonder why.**

### Then, the artefact as it should be

🔴 **A closing section, `## The artefact`** — 📌 **every part, with its
writer, its readers, and its meaning in one line.**

⚠️ **This is the only place where the whole of it is written down.**
📌 **Neither agent holds it: one writes half of it, the other reads
what it needs.**

### Then, what the verdict added

    ## From the verdict

    <the item, in a line>
    <already found above | not found, and here is what the files say
     about it | contradicted by the files, with the quotation>

### And what is still open

    ## What is still open

    <the question>
    <which agent, outside this group, would settle it>

🔴 **A last pass reconciles the chain and reads this section.**
