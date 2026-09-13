# Phase 2 — Compare, and settle

**Read this file whole before writing anything.**

⚠️ **Read `docs/refonte/proposition.md` first, in full** — it is your
own design from the previous phase. 📌 **Then read the eleven agent
files and the three grids named below.** 🔴 **Then read
`docs/refonte/00_brief.md`**, which explains how our chain works.

**Write in English.**

---

## What this phase is for

**You designed a chain in phase 1, without seeing ours. Now you see
ours.**

🔴 **The point is not to grade either one.** 📌 **It is to find where
one of them gets something right that the other misses**, and to end
with a chain that beats both.

⚠️ **What comes out of this phase drives the next one**, which corrects
our agents one by one. 🔴 **A divergence you report without a verdict,
or a verdict you leave unjustified, produces no correction anyone can
act on.**

---

## What you have in front of you

**Your own proposal** — a chain you designed, without seeing ours.

**Our chain, running in production.** 🔴 **It has produced real code.**
📌 **Yours has not run — it is a hypothesis.** Keep that difference in
mind throughout: a working system and an untested design are not
compared as equals.

**Our eleven agents, to read in full**, each at the path named:

    .claude/agents/analyste.md
    .claude/agents/diagnostiqueur.md
    .claude/agents/convertisseur.md
    .claude/agents/architecte.md
    .claude/agents/cadreur.md
    .claude/agents/verificateur.md
    .claude/agents/detailleur.md
    .claude/agents/realisateur.md
    .claude/agents/relecteur.md
    .claude/agents/controleur.md
    .claude/agents/arbitre.md

**And our three grids**, each a set of tests two of those agents
apply:

    docs/process/GRILLE_CADRAGE_PRODUIT.md
    docs/process/GRILLE_FERMETURE_TECHNIQUE.md
    docs/process/GRILLE_CONVENTIONS.md

---

## What judges one chain against the other

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

---

## What counts as a real divergence

🔴 **Report only where a difference changes what happens.** ⚠️ **Two
ways of doing the same thing are not one** — do not report that ours
splits work into lots while yours splits it into vertical slices unless
that choice moves one of the three measures.

**For each divergence you report:**

📌 **Say which of the three measures moves, and in which direction** —
what one chain catches that the other does not, what one pays that the
other does not, what one makes possible that the other cannot.

🔴 **Then say which chain is right, and why.** ⚠️ **A divergence with no
verdict teaches nothing** — do not list it without one.

📌 **No measure moves → it is a preference.** Do not report it.

⚠️ **Some of these measures cannot be observed on a chain that has never
run.** 🔴 **Estimate, and say that you are estimating.**

---

## What you write

🔴 **Write it to `docs/refonte/verdict.md`.**

### First, the final chain

**The chain that beats both** — 📌 **at the format `proposition.md`
uses**: why the split into roles is what it is, then one card per
agent, then every loop, then the flow as a whole.

⚠️ **A card names** what the agent reads, its moves in order, what it
produces, and how often it runs. 🔴 **A loop names** the agents it runs
between, what sends you in, what gets you out, what bounds it, and
whether a person steps in.

⚠️ **This is still macro.** 🔴 **Do not go into an agent's moves in
detail here** — that is the next phase's work.

### Then, what it makes of each of our eleven agents

**One line each, naming the outcome and the reason:**

    <our agent's name>  kept as is | changed | merged into <X> | dropped
    <why, in one or two sentences, tied to a measure>

🔴 **Justify every line.** 📌 **"Kept as is" needs a reason as much as
"dropped" does** — silence reads as *not examined*.

### Then, the divergences that mattered

**One entry per divergence that met the test above:**

    <what differs>
    <which measure moves, and how>
    <which chain is right, and why>

---

## What you do not do

- 🔴 **Design an agent's internal moves in detail** — the final chain's
  cards stay at phase 1's level of detail
- 🔴 **Report a divergence that moves no measure**
- 🔴 **Rewrite `proposition.md`** — it stands as it was written
- 🔴 **Read anything outside what this file names**
- Ask questions — decide, and say where you estimated rather than
  observed
