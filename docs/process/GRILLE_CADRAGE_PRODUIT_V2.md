# Product framing grid

> A closure test, not a list of subjects. It generates its questions
> from the blocks present.

🔴 **A framing is complete when nothing is left dangling.** Every
element has a named trigger and a named effect; every name it cites
either points at something described, or is defined on the spot. **A
name with nothing behind it is a gap.**

🔴 **Three passes, and they read different things.**

**Pass A — one block at a time.** 📌 **Everything a block closes on its
own.** ⚠️ **Answer from that block alone** — 🔴 whether another block
holds the answer is not this pass's question.

**Pass B — the blocks against each other.** 📌 **Everything that only
shows when two are put together.** ⚠️ **Nothing here is visible from
one block**, and a chain never reaches it.

**Pass C — the feature, once.** 📌 **What no block raises, because it
belongs to none of them.**

🔴 **Every question carries an identifier** — `A1.3`, `A2.screen.2`,
`C1.6`. ⚠️ **Whoever answers writes that identifier, exactly** — 📌 it
is what makes one block's answers comparable to another's.

⚠️ **A closure belongs to one pass, never both.**

🔴 **"Block" always means a block of the product file** — the grid's own
divisions are parts.

---

# PASS A — one block at a time

# A1 — Close the block

## Upstream

**`A1.1` What sets it in motion?**
A user action, a system event, a threshold crossed, incoming data, time
passing.

🔴 **Two answers look alike and are not.** 📌 **Nothing sets it off** —
it is consulted, never fired: a reference table, and A3 applies.
⚠️ **Something sets it off and the block does not say what** — that is
a gap, and A3 does not apply.

🔴 **Say which of the two**, never *"no trigger"* alone.

**`A1.2` What does it consume?**
🔴 **Name each piece of data.**

⚠️ **Whether another block produces it is not your question** — 📌 pass
B answers that.

## Downstream

**`A1.3` What does it produce?**
Data, a display, a state change, another mechanism firing. 🔴 **Name
each one.**

**`A1.4` Where does it draw?**
🔴 **Asked of every block that displays anything.** 📌 **Name the screen
and the area it occupies.**

**`A1.5` If it produces an order — what separates two elements that
tie?**
🔴 **Asked whenever a block sorts, ranks or picks a most recent.** ⚠️
**A key that can repeat leaves the order to chance**: two records made
the same day, two values equally close.

## The reverse

🔴 **Asked even when the answer is "nothing".**

**`A1.6` What happens when the trigger stops being true?**
The effect undoes itself, persists, or persists until something clears
it.

**`A1.7` What becomes of what was already produced?**
Kept, recomputed, deleted.

**`A1.8` Can it be set off again?**
Finding the earlier state, or clean.

---

# A2 — Make the block codable

🔴 **Ask the questions of the block's nature, and only those.**

📌 **Their identifiers carry the nature** — `A2.model.1`, `A2.screen.3`.

| Nature | Questions |
|---|---|
| model | **1** Type, bounds, allowed values? · **2** Mandatory or optional? 🔴 Even when trivial — the upper bound is a product decision |
| persistence | **1** Stored or recomputed? · **2** 🔴 If something can be stored incomplete: what does it hold then — the absence, or an empty value? |
| calculation | **1** Inputs, output, rule for each case? · **2** And when an input is missing? · **3** What values can its output take, and which are acceptable? 🔴 See below |
| transition | **1** What event triggers it? · **2** What states exist, reachable from which? 🔴 See exhaustiveness below |
| external source | **1** What if it fails, is unavailable, returns invalid data? · **2** 🔴 What makes two incoming things the same one — and what happens to the second? |
| synchronisation | **1** Rule when two versions diverge? · **2** What the user sees during, and on failure? · **3** 🔴 What identifies one same thing seen from both sides? And to which changes does a mirrored copy update — the list being closed |
| background work | **1** Frequency? · **2** What if the system interrupts it — does it resume alone? |
| journey | **1** Conditions for moving on? · **2** What if the user goes back, or abandons? |
| screen | **1** What is displayed, where, what each action does? · **2** What is shown with no data, loading, on failure? · **3** 🔴 What the user has in progress on this screen is kept when they leave and come back, or lost — say which, for each thing they can have in progress |
| text | **1** Exact label? · **2** What it becomes if the value is absent? |
| access | **1** Who sees, who changes? · **2** What does someone who cannot? |
| lifecycle | **1** How long does the data live, what becomes of it after? |

**On `calculation` — the bounds of an output:**

🔴 **A value a calculation produces and a field stores carries the same
bounds as one the user would have typed.** ⚠️ **The grid bounds a field
at `model`; nothing bounds what a rule computes** unless this question
is asked.

**Exhaustiveness — on `calculation` and `transition`:**

🔴 **Do the cases the rule distinguishes cover every possible value,
once each?** Not one value falling through, not one falling in two.

⚠️ **On an interval, the boundary belongs to one case or the other** —
never to both, never to neither. *"Above 5%"* does not say where 5.0%
lands.

📌 **It is not only about numbers.** A rule branching on statuses, on
states, on programmes, has the same duty: what happens to the status it
does not name, to the state in between, to the case that has no
programme.

---

# A3 — Blocks with no trigger

*A reference table, a scale, a convention, a catalogue.*

🔴 **Asked only when `A1.1` answered that nothing sets the block off.**
📌 **Otherwise, write `A3 | not applicable` and its reason, on one
line** — ⚠️ **a section skipped in silence and a section that does not
apply read the same.**

**`A3.1` What values, exactly?** 🔴 All of them, not a sample.

**`A3.2` Who consults them?**

**`A3.3` What if a value looked up is not there?**
Default, error, or impossible by construction.

**`A3.4` Can they change after delivery?**
⚠️ If so: is what was computed with the old values recomputed?

---

# A4 — Closing test

📌 **Its last question is B2's** — see below.

🔴 **Write down every name a block uses**, with the value the block
gives it. ⚠️ **Even a name you close here** — pass B needs them all to
find one name carrying two values.

🔴 **First, list what the block names and does not settle on the
spot.** ⚠️ **Every one of them, written out** — 📌 **a judgement on a
list you did not write covers what you did not look at.**

📌 **A name is anything the block refers to and expects to exist**: a
thing it displays, a value it applies, a state it distinguishes, a rule
it invokes. 🔴 **Not only what carries a proper name** — *"the five zone
rows"*, *"the active arc at rest"* and *"the time shown"* are names.

**Then two questions on each:**

**`A4.1`** 🔴 **Is it settled where it stands?** ⚠️ **A name designating
something of the block itself points nowhere** — 🔴 **a chain does not
catch it.**

**`A4.2`** 🔴 **Does it point at something described?** A destination, a
piece of data, a rule — described here, or marked *existing*.

📌 **A block title answers this.**
⚠️ **Open the target only when the citation asserts something about its
content** — *"as described in B4"*, *"the same colour as B3"*. **A bare
pointer needs no more than the title.**

| The block names | What must be there |
|---|---|
| A displayed text | Its exact wording |
| A displayed value | Its exact form — 🔴 **`09:14` and `9:14` are two answers** |
| A dimension, a position | Its value, or what it depends on |
| A visual state | What distinguishes it from the others |
| A set it counts | Every member, one by one, never the count alone |
| Something existing that changes | What it becomes — never just that it changes |
| Something existing that stays | 🔴 **Say so**; silence reads as an oversight |

⚠️ **A row that returns nothing is answered too** — 📌 *the block
displays no value*. 🔴 **Silence on a row and a row that does not apply
read the same.**

---

**A third question, on every word the block uses to qualify
something:**

**`A4.3`** 🔴 **Does it compare, and against what?** ⚠️ **A word saying a
thing is
more, less, or placed relative to something says nothing until the
other term is given.**

📌 **The test is not the word, it is what it leaves out** — 🔴 **a
comparison with one term missing.** ⚠️ **A value stated outright
compares to nothing and needs none of this.**

📌 **The other term is in the block, or it is a question.** 🔴 **Two
uses of one qualifier resolving to two different terms is the same
mistake as one name worth two things.**

🔴 **Every block went through A1 and A2 in full.**

**A category ruled out is declared ruled out** — never skipped in
silence.

⚠️ **Every answer is codable as it stands.** If it needs explaining,
rewrite it.

---

# PASS B — the blocks against each other

# B1 — Close the block against the others

🔴 **Every question here needs two blocks**, and none is
answerable from one.

## What pass A left you

🔴 **Every crossing below reads pass A's answers**, never the blocks
again:

| What you cross | Where it is |
|---|---|
| What a block consumes | `A1.2`, per block |
| What it produces | `A1.3` |
| Where it draws | `A1.4` |
| When it fires | `A1.1` — 📌 **a block writes when its trigger fires** |
| Every name it uses, with its value | `A4`'s list |

📌 **Gather one of these across every block, then cross it** — 🔴 **never
block by block**, or you re-read sixty times what one column shows at
once.

## The crossings

**`B1.1` A piece of data consumed and produced nowhere.**
🔴 **It exists outside the feature, or it is missing.** ⚠️ **Say which**
— an unnamed origin is a gap.

**`B1.2` One piece of data produced by two blocks.**
⚠️ **Two paths writing the same thing diverge.** 🔴 **Same rule, or the
difference is named.**

**`B1.3` A production consumed by nobody.**
📌 **It is written for nothing, or a consumer was left out.**

**`B1.4` A consumer reading before the writer writes.**
🔴 **It gets nothing.** ⚠️ **Compare the two moments** — a block reading
at launch and a block writing on a user action never meet.

**`B1.5` Two blocks drawing on the same screen and area.**
🔴 **One replaces the other, they coexist, or nobody decided.** 📌 **The
one written second rarely says which.**

**`B1.6` A name one block declares and no other uses.**
🔴 **It is dead, or its consumer uses another in its place.** ⚠️ **Say
which** — 📌 **a scale that declares five steps and sees four used has
either one step too many, or one screen reaching for the wrong one.**

⚠️ **This is not `B1.3`.** 📌 **That one crosses produced data; a name
is declared, not produced**, and nothing in `Produces` carries it.

**`B1.7` One name carrying two values.**
📌 **See B2.**

## What a crossing costs

🔴 **Every crossing above asks the same thing of its answer: does the
block change?**

⚠️ **Unchanged → the thread closes**, and the block is marked
*existing*. 🔴 **Changed → it is a block of its own, and nobody else
will write it.**

📌 **That holds for a block already in the document and for one that is
not there at all** — a piece of data nothing produces needs a block
before anything can consume it.

⚠️ **This is what a chain never reaches.** 📌 **A chain walks up what
consumes and down what produces; two blocks sharing a screen, or one
name, do neither** — 🔴 **only a column gathered whole shows them.**

---

# B2 — One name, across the blocks

🔴 **Answered from the `Names` column, gathered across
every block.**

**`B2.1`** 🔴 **One name, used twice, is worth the same twice.** ⚠️ **Read
every
use of a name together, never one at a time** — 📌 each use is complete
on its own, and that is why two different values under one word go
unseen.

📌 **Two uses answering differently are two names, or one mistake** —
🔴 **ask which.**

---

# PASS C — once on the feature

# C1 — What no chain reveals

*Run once on the feature. The only enumerated questions — short on
purpose.*

**`C1.1` Does a settings change apply retroactively, or only from now
on?**
⚠️ **The most often forgotten.** A single value applies retroactively by
construction; a dated value only from its date.

**`C1.2` What is out of scope, though one might think it in?**

**`C1.3` For each existing rule the feature touches: kept, changed,
removed?**
🔴 **Silence is not removal.** Rule by rule.

**`C1.4` What terms must be settled before writing the rules?**
The words that mean different things depending on who uses them.

**`C1.5` Are the displayed terms the product's or the code's?**
🔴 Internal naming never surfaces on screen.

**`C1.6` Does it collect personal or sensitive data?**
Health, location, biometrics, identifiers. Consent is a product
decision, never ticked by default. 🔴 **One answer per kind** — health
and location are not consented to together.

**`C1.7` What system permissions, and what if they are denied for
good?**
🔴 Asked at the moment of use, never at launch. 🔴 **One answer per
permission** — a refused sensor and a refused link do not leave the
same application behind.

⚠️ **These two are the only C1 questions with several instances.**
📌 **Everything else here is asked once**; these are asked once per
thing they name.

---

📌 **This grid does not enumerate cases.** What it does not generate
from the blocks present, it does not ask.
