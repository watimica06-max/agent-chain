# Phase 3 — Examine one agent

**Read this file whole before writing anything.**

🔴 **This is one pass among several.** The orchestrator runs this file
once per agent, and **tells you which one you are working on.**

📌 **`<name>` below is that agent's name** — its file is
`.claude/agents/<name>.md`.

**Write in English.**

---

## What this pass is for

**We want to know whether this agent is well built, and what exactly is
wrong with it.**

🔴 **You produce comments, not a rewritten agent.** A rewritten file
hides the reasoning: to know what moved, we would have to diff four
hundred lines and guess which change carries an intention and which is
your way of saying the same thing. 📌 **We apply the corrections
ourselves, one by one.**

🔴 **One agent, and its command. Nothing else.** ⚠️ **You do not read
the neighbouring agents, and you do not judge this one against them** —
📌 **a later pass does that, over a group of agents at once.** **What
you would need another agent's file to settle, you name and leave.**

📌 **An agent with nothing wrong in it gives an empty list.** 🔴 **That
is a result, not a failure** — do not invent a comment to fill the
file.

---

## What you read

🔴 **Three things, in this order. The third comes last, and that
matters.**

**1. Our agent, at `.claude/agents/<name>.md`** — 🔴 **in full.**

**2. Its command**, in `.claude/commands/` — the one that invokes it.
📌 **Find it by grepping the agent's name there.** ⚠️ **Several
commands may invoke one agent, and one command may invoke several** —
🔴 **read every command that invokes yours, in full.**

📌 **A command is not a wrapper**: it decides which invocation runs,
what goes into the prompt, what it checks before and after, what it
files, and what it tells the Product Owner to run next. ⚠️ **A defect
lives there as readily as in the agent.**

**3. `docs/refonte/verdict.md`, sections 4 to 7, and your agent's line
in section 2** — 🔴 **only once you have written everything the three
planes below turn up.**

⚠️ **Read it first and it becomes your list** — 📌 **you would look for
what it names and stop there.** 🔴 **Read it last and it is a check**:
what it saw and you did not is worth having; what it claims and the
agent contradicts is worth more.

**Nothing else.** 🔴 **Not the other agents, not the grids, not the
process files, not the brief.**

⚠️ **If your agent applies a grid, you still do not read it** — 📌 **you
judge how the agent uses it, not what it contains.**

---

## What you are looking for

🔴 **Three planes, in this order, over the agent and its command.** 📌
**Each is a sweep, not a search** — every move gets its turn, including
the ones you find nothing wrong with. ⚠️ **A sweep that stops where the
interesting cases are found is a sample**, and it misses exactly what a
fresh reading was for.

### Plane 1 — the agent as a whole

**State its role in one sentence, from what the file actually says.**
🔴 **Then list its moves, in order**, and for each:

| | |
|---|---|
| **Why it exists** | What the chain would lose without it |
| **What it feeds** | The output it contributes to, and what reads that |
| **What it overlaps** | Another move of this same agent doing part of the same thing |

🔴 **Then judge the set, not the moves:**

- **Does every move serve what this agent produces?** 📌 **A move whose
  result nothing carries forward is paid for nothing.**
- **Do the moves cover the role, with no overlap?** ⚠️ **Two moves
  splitting one job, or one job falling between two moves.**
- **Is there a move that could go?** 🔴 **Say what would break.**
- **Is the order right?** 📌 **A move needing what a later one
  produces; a constraint stated after what it constrains.**

### Plane 2 — each move

🔴 **Four questions, on every move:**

**1. Does the move do what it says?** 📌 **Does it reach as far as it
claims** — one folder where two carry the thing, one case of a class
that holds three? 📌 **Does it enumerate cases where it means a class?**
⚠️ **What is not in the list passes.** 📌 **Can two readers check its
test the same way?** 🔴 *Until it is coherent* is not a test.

**2. Can the agent do it with what it reads?** 📌 **A move resting on a
fact nothing gives it** — 🔴 **it will guess.** 📌 **A read no move
uses, a file read whole where a section would do, the same thing read
twice** — ⚠️ **paid at every invocation.**

**3. What happens when it cannot?** 📌 **Every situation where this
move cannot produce** — is it foreseen, with a stop and a way to
resume? ⚠️ **Unforeseen, the agent invents.**

**4. Can a reader who has seen nothing else run it?** 🔴 **This agent is
read by something that has seen no other file, no other phase, no
conversation.** 📌 **A term used and never defined; a reference to
something the reader has not seen — *as the previous agent produced*,
*the usual shape*; a count that no longer matches what follows it; a
placeholder with no rule for what fills it; a file named without a
path; an instruction that reads two ways.**

### Plane 3 — each rule, as written

🔴 **Six criteria, on every rule the agent states.** 📌 **These are the
ones we write our own rules against.**

| | The criterion |
|---|---|
| **1** | **A general rule** — not built to catch one case particular to one product or one codebase |
| **2** | **A bounded case** — not a list that could run forever |
| **3** | **It catches something real** — a defect that happens, not one imagined |
| **4** | **No ambiguity** — one reading, not two |
| **5** | **No useless example or justification**, no commentary on why it came to be |
| **6** | **Universal programming vocabulary** — not the words of one language or one framework |

⚠️ **A rule failing criterion 3 is the hardest to see** — 📌 **it reads
well and guards nothing.**

### And for the command

🔴 **Two more questions, on the command alone:**

**Does what it says to run next match what can happen?** 📌 **Every
outcome the agent can produce has a row; every row names an outcome the
agent can produce.** ⚠️ **A row for a case that cannot occur, or a case
with no row, and the Product Owner is on their own.**

**Does the prompt carry what the agent needs, and only that?** 📌 **A
file the agent must have and the prompt does not name; a thing the
prompt names and no move uses.**

---

## What we already know goes wrong

⚠️ **This list is not what you are asked to find.** 🔴 **It is what we
have already found, in other agents, so that you do not spend the pass
rediscovering it** — 📌 **the three planes above are the search.**

- A move that reaches less than it should, and nothing signals it
- A net: a move re-checking what an earlier agent already guaranteed
- Work done twice: the agent recomputes what an earlier one wrote,
  because it does not read its output
- An invocation that produces nothing, in a case where the agent has
  nothing to do
- More context than one agent holds — ⚠️ **it degrades instead of
  stopping**
- A split too fine: two invocations where one would do, each reloading
  the same context
- A loop with no ceiling
- A forbidden thing under *what you never do* that nothing in the body
  asks for, or a rule in the body with no matching entry
- Two passages of one agent asking for different things

---

## What judges a comment

🔴 **Three measures, in this order.**

**1. Robustness** — how many gaps between what the idea asked and what
the code does. ⚠️ **This dominates**: a correction cycle pays for the
whole chain again, on every gap.

**2. Round trips** — turns between agents, retries, decisions asked of
the person.

**3. Tokens** — what is read, and how many times.

🔴 **Every comment names the measure it moves, and how.**

⚠️ **A comment that moves none of the three is a preference** — 📌 **do
not write it.** **Rephrasing a sentence that already works is not a
correction.**

---

## What you write

🔴 **One file**: `docs/refonte/agents/<name>.md`.

**One entry per comment, in the order they are to be applied:**

    Fichier      : <the agent or command file>
    Cible        : where exactly — move 6, the "What you read"
                   section, the order of moves 4 to 7
    Aujourd'hui  : what is written there, or "nothing"
    Le défaut    : which plane and which question turns it up
    Ce qu'il faut: what should hold instead — 🔴 the intent, not the
                   sentence to paste
    Justification: which measure moves, and how

📌 **We write the final wording ourselves** — 🔴 **say what has to be
true, not the words to copy in.**

🔴 **Each comment reads against the state the ones before it assume.**
📌 **Write them so that applying them top to bottom works.**

### Then, what the verdict added

🔴 **A closing section, `## From the verdict`** — written after you have
read it, and after everything above.

**One entry per item of the verdict that names your agent:**

    <the item, in a line>
    <already found above | not found, and here is what the agent says
     about it | contradicted by the agent, with the quotation>

📌 **The third case is the one to be exact about** — ⚠️ **the verdict
judged a description; you are the first to read the agent itself.**

### And what you could not settle

    ## What another agent would settle

    <the question>
    <which agent's file would settle it>
    <what you would conclude either way>

🔴 **A group pass runs after yours and reads this section.** ⚠️ **Write
it even where you think that pass will see it anyway** — 📌 **it is the
only channel between passes.**

---

## What you do not do

- 🔴 **Rewrite the agent, or any part of it** — comments, not a file
- 🔴 **Write a comment whose justification names no measure**
- 🔴 **Write comments for an agent other than yours**
- 🔴 **Read beyond the three things named above**
- 🔴 **Judge your agent against another** — name what you would need,
  and leave it
- 🔴 **Correct a grid** — note the fault, leave the grid alone
- 🔴 **Invent a comment to avoid an empty file**
- 🔴 **Edit anything under `.claude/`** — our chain stays as it is
- Ask questions — decide, and note where you were unsure
