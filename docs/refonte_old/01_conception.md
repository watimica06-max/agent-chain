# Phase 1 — Design the chain

**Read this file whole before writing anything.**

You are asked to design a system, not to build it. 🔴 **Nothing you
write here becomes an agent** — you are thinking about what the agents
should be.

⚠️ **Write in English.** 📌 **No limit on how many agents you propose.**

---

## What this phase is for

**We run a chain that turns ideas into code. It works. We do not know
whether it is the right shape.**

🔴 **You are asked to design one without seeing ours** — and that is
deliberate. 📌 **Shown our chain first, you would refine it; you would
never find that a whole role should not exist.**

⚠️ **A later phase puts the two side by side.** 🔴 **What makes that
comparison worth anything is that you designed yours free of ours** —
so design against the constraints below, and against nothing else.

📌 **What you produce is read by another context, without you.** 🔴
**It carries your reasons, not only your choices.**

---

## What the system does

**A person with no technical background writes an idea in free prose.
Compiled, tested, merged code comes out the other end.**

### What comes in

`idees.md` — written by hand, in free prose, more or less organised.

📌 **It describes either an application, or a feature to add to an
application that already exists.**

⚠️ **It is almost always incomplete, and not because it is badly
written.** The person describes what they want to see, and leaves
decisions open without knowing it — what shows when there is nothing,
what becomes of data written half-way, what separates two equal
things.

🔴 **Code cannot leave those open.**

### What comes out

**Compiled code, tested, merged, running — ready to be pushed to
whatever carries it.**

---

## The ground you build on

**Everything happens inside Claude Code, integrated into the project's
development environment.**

📌 **On an existing application**, the code already written and every
file of the project are directly accessible.

⚠️ **On a new application, the folder is empty** — there is nothing to
read.

### What an agent is

📌 **An agent is invoked with its own context, produces a result, and
goes out.**

⚠️ **What decides to invoke it, and what follows, is something else** —
🔴 **you say what.**

📌 **This is given because otherwise you would chain agents into one
another**, each inheriting the previous one's context. 🔴 **That is a
possible design, but choose it — do not fall into it.**

---

## The product requirement

🔴 **Whatever goes back and forth with the person about the product
happens at the start, and there only.**

**Once the product is settled, the person does not step in by hand
again.**

⚠️ **This is a requirement, not an observation**: something, somewhere,
has to guarantee that no product decision is left open before the code
begins. 📌 **A product question surfacing while coding is a failure of
that guarantee.**

🔴 **And the guarantee costs.** Closing the whole product up front takes
questions, many of them. 📌 **That is a real design problem** — solve
it, do not route around it.

---

## The constraints

- **An agent has a finite context**; it does not hold a whole project
- **The person who writes the idea has no technical background** and
  cannot arbitrate an implementation choice
- 🔴 **She alone can arbitrate a product choice** — the two together say
  where she steps in, and where she must not
- **The code that exists is the only truth**; documents lie
- 🔴 **On an existing application, the chain does not break what
  works** — it reads and modifies code it did not write
- **Every invocation costs**, and an error early spreads
- 🔴 **An error found late costs everything done since**
- 🔴 **An agent that cannot produce stops, and does not invent** — ⚠️
  **what happens then is yours to design**

---

## What the system has to guarantee

- **The code does what the idea asked** — nothing lost on the way
- **Nothing more** — no invention
- **What worked still works**
- 🔴 **The result is reproducible** — two runs on one idea give the same
  split, the same order, the same code

### And what judges a design, in this order

🔴 **1. Robustness** — how many gaps between what the idea asked and
what the code does.

⚠️ **A correction cycle pays for the whole chain again**, on every
gap: 📌 **it is the cost that dominates all others**, and a robust
process would hold in a single coding session.

📌 **2. Round trips** — decisions asked of the person, turns between
agents, retries after a failure.

📌 **3. Tokens** — what is read, and how many times.

🔴 **The first prevails.** ⚠️ **A costlier chain producing no gap beats
a cheap one producing ten.**

---

## On errors, and what they cost

**A robust process minimises errors, and catches early the ones that
remain.**

⚠️ **But stacking checks is not an answer**: an agent catching another's
mistake costs an invocation and a load, and it would take a third to
catch the second. 🔴 **Every check added has to name what no other one
already does.**

🔴 **An agent relies on the work of the one before it.** ⚠️ **Without
that, each re-verifies everything, and the cost explodes.**

📌 **Where and why a check is worth it anyway is yours to decide** — 🔴
**and to justify.**

⚠️ **The final bound**: *everything is paid in tokens and in time — that
is what to minimise.*

---

## What you write

🔴 **Write it to `docs/refonte/proposition.md`.**

⚠️ **Another context will pick this file up without you** — 📌 **it
carries your reasons, not only your choices.**

### First, why this split into roles

**Before describing any agent**: why these roles and not others, where
the boundaries fall, and what justifies each one.

🔴 **This comes first on purpose** — it makes you think the split
through rather than lay one down.

### Then, one card per agent

    <name>
    Reads:    the files, named
    Does:     its moves, in order — precise enough that one sees what
              happens, not an abstract verb
    Produces: the files, named
    Runs:     once per project · per feature · per lot · in a loop
              with <agent>

📌 **The `Does` field is what keeps you from skimming.** ⚠️ **Without
it, *the Converter turns product into technical* passes**, and nobody
knows whether you saw the difficulty.

🔴 **One agent reads what fits in one reading, and produces one thing.**
⚠️ **If you have one read a whole project, or produce three artefacts of
different natures, say why you think that holds** — 📌 **name what it
holds at once, and why that stays inside one context.**

🔴 **This does not forbid it — it asks you to say what makes it
tenable.**

### Then, every loop

    Between which agents
    What sends you in       the condition, not a file name
    What gets you out       the stopping test, checkable
    What bounds it          a ceiling of turns, or none, and why
    Who steps in            a person, or nobody

📌 **The stopping test is the hard field** — 🔴 *until it is good enough*
is not one.

📌 **The last line separates two natures of loop**: ⚠️ **one that waits
for a person can run for days; one that runs alone cannot.**

### Then the flow, in one view

**The whole chain at a glance, loops included.**

### And last, because another context reads this without you

📌 **Why each boundary is where it is** — ⚠️ what breaks if it moves.

📌 **What you ruled out** — 🔴 the designs you considered and rejected,
with the reason.

📌 **What you are not sure of** — ⚠️ **a point you settled without
being able to say what would prove you right.** 🔴 **Name what would
settle it** — a measure, a case, something someone could check.

🔴 **That last one matters most**: without it, the next context takes
everything as equally settled.

---

## What you do not do

- 🔴 **Write agent files** — this is a design, not a build
- 🔴 **Ask questions** — you produce and you are done; where something
  is undecided, decide it and say you did
- 🔴 **Read anything outside what this file names**
- 🔴 **Design against a chain you imagine we have** — you have not seen
  ours, and that is deliberate
