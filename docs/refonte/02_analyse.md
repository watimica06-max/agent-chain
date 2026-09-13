# Phase 2 — Judge the chain, whole

**Read this file whole before writing anything.**

⚠️ **Read `docs/refonte/proposition.md` first, in full** — it is your
own design from the previous phase. 🔴 **Then read the two process
files named below.**

**Write in English.** 📌 **The process files are in French** — read
them as they are, and write your verdict in English all the same.

---

## What this phase is for

**You designed a chain in phase 1, without seeing ours. Now you see
ours, at the level its shape is decided.**

🔴 **You judge our chain. You do not build another one.** 📌 **Your own
design is a source of ideas here, not a competitor** — a role you
foresaw and we do not have is worth reporting; which of the two chains
would "win" is not a question this phase answers.

⚠️ **A later phase corrects our agents one by one.** 🔴 **What you write
here is what it starts from** — a judgement without a reason produces
no correction anyone can act on.

---

## What you have in front of you

**Your own proposal** — a chain you designed, without seeing ours.
📌 **It has never run. Ours has, and has produced real code.** ⚠️ **A
working system and an untested design are not weighed as equals.**

**Our two process files, to read in full:**

    docs/process/PROCESS_AMONT.md
    docs/process/PROCESS_AVAL.md

📌 **They describe the chain at the level this phase works on**: what
each agent is for, what it reads and produces, where the boundaries
fall, and — this is why you read them rather than the agents — **the
reason behind each choice.** ⚠️ **Several carry the case that produced
them**: a defect observed, and the rule it led to.

🔴 **A reason stated is not a reason proved.** 📌 **Where a
justification does not hold, say so** — that is worth more than
agreeing with it.

### What you are not shown, and what follows from it

🔴 **You do not read the agents themselves, nor the grids.** 📌 **The
process files say which families of closure each grid runs and why**;
that is the level you judge at.

⚠️ **So you judge the chain as it is described.** 🔴 **An agent may
depart from what the process says of it, and you cannot see that** —
📌 **which is what the next phase reads the agents for.**

⚠️ **Where a judgement of yours turns on something only an agent's
file could settle, do not guess** — 🔴 **name it under *What only the
agents can settle*.**

---

## What judges the chain

🔴 **Three measures, in this order.** 📌 **The same ones
`proposition.md` was designed against.**

**1. Robustness** — how many gaps between what the idea asked and what
the code does. ⚠️ **This dominates**: a correction cycle pays for the
whole chain again, on every gap.

**2. Round trips** — decisions asked of the person, turns between
agents, retries after a failure.

**3. Tokens** — what is read, and how many times.

🔴 **The first prevails.** A costlier chain producing no gap beats a
cheap one producing ten.

🔴 **Every judgement names the measure it moves, and in which
direction.** ⚠️ **A judgement that moves none of the three is a
preference** — 📌 **do not write it.**

⚠️ **Some of these cannot be observed from a description.** 🔴
**Estimate, and say that you are estimating.**

---

## What you write

🔴 **Write it to `docs/refonte/verdict.md`**, in seven sections, in this
order.

⚠️ **Sections 2, 4 and 5 are swept, not searched.** 🔴 **The process
files name a closed set of agents, of artefacts and of loops: every one
of them gets its line, including the ones you find nothing wrong
with.** 📌 **A defect lives in what nobody thought to look at** — a
sweep that stops where the interesting cases are found is a sample, and
it misses exactly what a fresh reading was for.

### 1. The chain, as a whole

**Does its shape hold, and where does it break?** 📌 **A few
paragraphs.** 🔴 **Not a chain of your own** — what is sound in this
one, what is not, and what the not costs.

### 2. The roles

**One line per agent, and a reason under it:**

    <agent> — the role holds | overlaps <X> | should not exist | should split
    <why, in one or two sentences, and which measure moves>

🔴 **Every agent of both process files gets a line.** 📌 **"The role
holds" needs its reason as much as the others** — silence reads as *not
examined*.

📌 **A role holds when it does one thing, that thing is needed, and no
other agent does it.** ⚠️ **An agent may be well built and still hold a
role that should not exist.**

### 3. The roles that are missing

**What your own design foresaw and this chain has no agent for.**

🔴 **For each: a real hole, or a choice the process files justify?**
⚠️ **Say which** — 📌 **a hole names what goes wrong without it; a
justified choice names the justification, and whether it convinces
you.**

### 4. The boundaries

🔴 **This is the section that matters most.** 📌 **What one agent
produces, another reads** — and that is where a chain of separate
contexts fails.

**One entry per defect:**

    <what is defective>
    <the agents on either side of it>
    <which measure moves, and how>

🔴 **What to look for, in one sentence: wherever one agent takes
something for granted that nothing in the chain guarantees, or pays for
something nothing needs.** ⚠️ **A boundary defect is rarely visible
from either side alone** — 📌 **that is why it survives, and why no
list of known shapes will find the next one.**

🔴 **Sweep it: every artefact the process files name** — a file, a
field, a marker, a line, a naming rule — **gets a producer and at least
one reader, or it is an entry here.** 📌 **Take them one at a time, in
the order the process files introduce them.**

⚠️ **Then the same for what an agent assumes rather than reads**: a
state of a file, a convention, a guarantee an earlier agent is supposed
to have made. 🔴 **Who established it, and where?**

### 5. The loops

**One entry per loop the process files describe:**

    <between which agents>
    <what sends you in>
    <the stopping test — and whether it can be checked>
    <what bounds it>
    <who steps in>

🔴 **The stopping test is the field that matters.** 📌 **A test that
cannot be checked is a loop that ends when someone gets tired** — say
so where you find one.

⚠️ **Separate the two natures**: 📌 **a loop that waits for a person
can run for days; one that runs alone cannot.**

### 6. What this chain takes for granted

🔴 **Every design rests on premises its designers stopped seeing.**
📌 **Find this chain's, and say what each costs.**

⚠️ **A premise is not a rule you disagree with** — 📌 **it is something
the chain never puts in question**, because the shape it took makes the
question unaskable.

**For each one:**

    <the premise, stated plainly>
    <what it buys>
    <what it costs, and which measure pays>
    <what the chain would look like without it>

🔴 **A premise you find sound still goes here** — ⚠️ **naming it is the
work; agreeing with it afterwards is fine.**

📌 **Nothing in this file tells you which they are** — 🔴 **if it did,
they would not be premises.**

### 7. What only the agents can settle

**The judgements you could not reach from a description.**

    <the question>
    <which agent's file would settle it>
    <what you would conclude either way>

🔴 **This list is what the next phase carries into each agent.** ⚠️
**Without it, it reads every agent with no idea what to look for.**

---

## What you do not do

- 🔴 **Design a chain of your own** — you judge this one
- 🔴 **Rewrite `proposition.md`** — it stands as it was written
- 🔴 **Write an agent, or an instruction for one** — the next phase does
  that
- 🔴 **Report a judgement that moves no measure**
- 🔴 **Read anything outside what this file names** — not the agents,
  not the grids, not the commands
- Ask questions — decide, and say where you estimated rather than
  observed
