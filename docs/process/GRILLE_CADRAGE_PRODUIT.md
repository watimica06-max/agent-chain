# Product framing grid

> A closure test, not a list of subjects. It generates its questions
> from the blocks present.

🔴 **A framing is complete when nothing is left dangling.** Every
element has a named trigger and a named effect; every name it cites
either points at something described, or is defined on the spot. **A
name with nothing behind it is a gap.**

**Run parts 1, 2 and 5 on every block of the product file.** One block,
one closure. 📌 **Part 3** for a block nothing sets off, **part 4** once
on the feature. 🔴 **"Block" always means a block of the product file** —
the grid's own divisions are parts.

---

# Part 1 — Close the block

## Upstream

**What sets it in motion?**
A user action, a system event, a threshold crossed, incoming data, time
passing. 🔴 **Nothing sets it off → it is a reference table**, see
part 3.

**What does it consume?**
Name each piece of data.

**Does each one already exist?**
🔴 Existing → mark it *existing*, the thread closes. Not existing → it
must be described, and becomes a block of its own.

**Who else writes the same data?**
⚠️ Two paths writing the same thing diverge. Same rule, or the
difference is named.

## Downstream

**What does it produce?**
Data, a display, a state change, another mechanism firing.

**Who consumes it?**
Name each consumer.

**When does each consumer read, relative to when this block writes?**
🔴 A consumer reading before the write gets nothing.

**Does it change the behaviour of what it reaches?**
Unchanged → thread closes, marked *existing*. Changed → walk up what
depends on it.

## Around it

**This block sits in something that already exists. What surrounds it
and does not change?**

What shares its display surface · what treats the same subject
elsewhere · what it replaces without saying so.

⚠️ **A chain walks up what consumes and down what produces. A neighbour
does neither** — no closure reaches it.

## The reverse

🔴 **Asked even when the answer is "nothing".**

**What happens when the trigger stops being true?**
The effect undoes itself, persists, or persists until something clears
it.

**What becomes of what was already produced?**
Kept, recomputed, deleted.

**Can it be set off again?**
Finding the earlier state, or clean.

---

# Part 2 — Make the block codable

🔴 **Ask the questions of the block's nature, and only those.**

| Nature | Questions |
|---|---|
| model | Type, bounds, allowed values? Mandatory or optional? 🔴 Even when trivial — the upper bound is a product decision |
| persistence | Stored or recomputed? What happens to existing records if the structure changes? |
| calculation | Inputs, output, rule for each case? And when an input is missing? 🔴 See exhaustiveness below |
| transition | What event triggers it? What states exist, reachable from which? 🔴 See exhaustiveness below |
| external source | What if it fails, is unavailable, returns invalid data? |
| synchronisation | Rule when two versions diverge? What the user sees during, and on failure? |
| background work | Frequency? What if the system interrupts it — does it resume alone? |
| journey | Conditions for moving on? What if the user goes back, or abandons? |
| screen | What is displayed, where, what each action does? What is shown with no data, loading, on failure? |
| text | Exact label? What it becomes if the value is absent? |
| access | Who sees, who changes? What does someone who cannot? |
| lifecycle | How long does the data live, what becomes of it after? |

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

# Part 3 — Blocks with no trigger

*A reference table, a scale, a convention, a catalogue.*

**What values, exactly?** 🔴 All of them, not a sample.

**Who consults them?**

**What if a value looked up is not there?**
Default, error, or impossible by construction.

**Can they change after delivery?**
⚠️ If so: is what was computed with the old values recomputed?

---

# Part 4 — What no chain reveals

*Run once on the feature. The only enumerated questions — short on
purpose.*

**Does a settings change apply retroactively, or only from now on?**
⚠️ **The most often forgotten.** A single value applies retroactively by
construction; a dated value only from its date.

**What is out of scope, though one might think it in?**

**For each existing rule the feature touches: kept, changed, removed?**
🔴 **Silence is not removal.** Rule by rule.

**What terms must be settled before writing the rules?**
The words that mean different things depending on who uses them.

**Are the displayed terms the product's or the code's?**
🔴 Internal naming never surfaces on screen.

**Does it collect personal or sensitive data?**
Health, location, biometrics, identifiers. Consent is a product
decision, never ticked by default.

**What system permissions, and what if they are denied for good?**
🔴 Asked at the moment of use, never at launch.

---

# Part 5 — Closing test

**Two questions on every name a block cites**, and they are not the
same:

🔴 **Does it point at something described?** A destination, a piece of
data, a rule — described here, or marked *existing*.

📌 **A block title answers this.** Open the target only when the
citation asserts something about its content — *"as described in B4"*,
*"the same colour as B3"*. **A bare pointer needs no more than the
title.**

🔴 **Is it defined where it stands?** A name designating an attribute
of the block itself points nowhere — 🔴 **a chain does not catch it.**

| The block cites | What must be there |
|---|---|
| A displayed text | Its exact wording |
| A dimension, a position | Its value, or what it depends on |
| A visual state | What distinguishes it from the others |
| Something existing that changes | What it becomes — never just that it changes |
| Something existing that stays | 🔴 **Say so**; silence reads as an oversight |

🔴 **Every block went through parts 1 and 2 in full.**

**A category ruled out is declared ruled out** — never skipped in
silence.

⚠️ **Every answer is codable as it stands.** If it needs explaining,
rewrite it.

---

📌 **This grid does not enumerate cases.** What it does not generate
from the blocks present, it does not ask.
