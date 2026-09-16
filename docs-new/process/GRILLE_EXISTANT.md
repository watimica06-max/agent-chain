# Existing-product grid

> A closure test for what a feature **hits**, not for what it leaves
> open. The framing grid closes a feature on itself; this one closes it
> against the product already built.

🔴 **It runs once, after the framing grid has returned an empty
questions file.** 📌 **Nothing is open inside the feature any more** —
⚠️ **what remains is what it collides with outside itself.**

🔴 **Only the blocks carrying a `Global:` line.** 📌 **That line names
the section of the global product file the block attaches to** — ⚠️ **a
block attached to nothing hits nothing**: it describes something that
did not exist.

🔴 **Every question here needs two things**: a block of the feature, and
the section of the global it names. 📌 **None is answerable from the
feature alone** — that is what the framing grid was for.

⚠️ **A question this grid raises is an arbitration**, never a gap. 📌
**Two things are true at once and cannot both stay** — the Product
Owner says what becomes of each.

🔴 **Every question carries an identifier** — `E1.2`, `E3.1`. ⚠️
**Whoever answers writes it, exactly.**

---

# E1 — What the block takes, and something else already holds

🔴 **The feature claims a place, a name, a resource.** 📌 **Ask of each
whether the global section already gives it to something.**

**`E1.1` A place on a screen.**
📌 **A corner, a row, a slot, a position named in words** — ⚠️ *bottom
right*, *at the top of the list*, *beside the title*. 🔴 **The section
already puts something there → what becomes of the two?**

**`E1.2` A gesture, a shortcut, a key.**
📌 **A tap, a long press, a swipe, a system gesture.** ⚠️ **Two things
answering one gesture on one screen is an arbitration.**

**`E1.3` A name the user sees.**
🔴 **A screen title, a button label, a menu entry.** ⚠️ **The same words
for two different things is a collision even when the two never meet**
— 📌 **the user reads one vocabulary.**

**`E1.4` A piece of data something else already writes.**
📌 **The block produces a value the section already says is produced
elsewhere** — 🔴 **which one wins, and when?**

**`E1.5` A resource only one thing can hold at a time.**
📌 **A sensor, a camera, a lock, a foreground slot, a notification
channel** — ⚠️ **the section already claims it.**

---

# E2 — What the block says, and the section says otherwise

**`E2.1` A rule of the section that the block contradicts.**
🔴 **Not a rule it refines — one it makes false.** 📌 **Quote both.**

⚠️ **A block that narrows a rule is not a contradiction** — 📌 **it is a
case the rule did not cover**, and it belongs to the feature.

**`E2.2` A value, a unit, a format the section fixes differently.**
📌 **The same quantity written two ways**, in two places the user can
see at once.

**`E2.3` A state the section says is impossible.**
🔴 **The block puts the product in a state the section rules out** —
⚠️ **one of the two is wrong, and it is not for you to say which.**

---

# E3 — What the feature takes away without saying so

🔴 **The framing grid never asks this**: it reads the feature, and what
the feature does not mention is invisible to it.

**`E3.1` A behaviour the section describes and the block replaces.**
📌 **The block does what the section already did, differently** — 🔴
**does the old one remain, beside it, or is it gone?**

⚠️ **Silence is not removal.** 📌 **A behaviour nobody described again
is still in the code.**

**`E3.2` A way in that no longer leads anywhere.**
📌 **The section names a button, a link, a notification that opens
something the feature changes or removes** — 🔴 **what does it open
now?**

**`E3.3` Something the section says is always true, and the feature
makes occasional.**
⚠️ **The section promises it without condition; the block adds one.**

---

# E4 — Closing test

🔴 **For every block carrying a `Global:` line, one pass of E1 to E3
against its own section.** 📌 **A block whose section answers nothing
raises nothing** — that is the common case.

⚠️ **You never read a section no block names** — 🔴 **the global runs
past 250 KB**, and what no block attaches to cannot be hit.

📌 **An arbitration answered becomes a block of the feature file** —
🔴 **including the one that says what the existing thing becomes.**
⚠️ **It does not belong to the feature, and that is expected**: the
Fusionneur will carry it back to the global.
