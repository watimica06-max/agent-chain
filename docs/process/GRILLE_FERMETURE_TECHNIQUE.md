# Technical closure grid

> A closure test, not a checklist. It generates its signals from the
> file under it.

🔴 **A translation is complete when nothing the product settled has
been lost, and nothing it did not settle has been added.** Every rule
sits in one place, names what it consumes, and leaves no case open.

**Part 1 closes the product file, part 2 the technical document.**
📌 **"Block"** means a block of the product file; **"entry"** a
numbered entry of the technical document.

---

# Part 1 — On the product file

## Nature

**Does each sentence of this block produce what the block produces?**

🔴 **The output gives the nature, the trigger only bounds it.** Almost
every block has a trigger — *once consumption exceeds the target*,
*whenever the screen becomes visible* — so a trigger alone tells you
nothing.

| It produces | Its nature |
|---|---|
| Something displayed | `screen`, even when an event fires it |
| Anything else | The nature of what it produces |

🔴 **Sentence by sentence, not block by block.** A block reads coherent
as a whole and still carries one sentence producing something else —
an exception, a special case, a *"except when…"* clause tacked onto a
rule.

**That sentence becomes its own block**, under the nature it produces.

⚠️ **Read past what merely describes what the user sees meanwhile.** A
block whose output is a data reload is not a `screen` block because it
also says what stays on screen during it.

🔴 **A marker is a claim, not proof.** File by what you read.

## Consistency

**Does this block agree with the others?**

🔴 **Two blocks disagreeing on the same subject is a signal**, whatever
the wording each uses. A block claiming *"only X varies"* while another
describes Y varying is a contradiction, even when both read as
reasonable on their own.

📌 **You are the only one who reads the file whole.** The upstream
chain loads a few blocks at a time; the gap between two of them is
yours to see.

---

# Part 2 — On the technical document

## Traceability

**Can you point at the sentence in the product file yours follows
from?**

**Yes** → you made it explicit. **No** → you added.

🔴 **Anything you would have to add is a question**, however small it
looks and however obvious the addition seems.

⚠️ **The additions that slip through are the small ones**: where a
value is stored, which of several items goes first, what a unit is.
**They feel like translation and they are decisions.**

## Singularity

**Does this rule live in one place?**

🔴 **Never duplicate between sections — reference instead.**

**The owning section answers "where does this behaviour come from",
not "where is it seen".** A calculation rule belongs to calculations
even if it produces a display; a field bound to the model even if it
shows at input time.

⚠️ **A cross-domain interaction matrix belongs to the domain that
applies it**, never to the ones it concerns.

## Agreement between entries

**Do two entries say the same thing about the same subject?**

🔴 **You wrote them both**, from two product blocks that spoke of the
same rule. **Neither is a duplicate you chose to write** — you
reformulated twice, and two reformulations of one thing rarely
coincide.

| Where it shows | What to look for |
|---|---|
| A rule restated | One entry lists a case another excludes |
| A value repeated | Two entries give it with different precision or units |
| A label quoted twice | The two wordings differ |
| An order of precedence | Two entries state it in opposite directions |

⚠️ **This is not *Singularity*.** That one bars duplication you chose;
this one catches the duplication you did not notice.

📌 **Nobody else can see it.** The Cadreur reads the whole document but
does not judge its content; every agent after him opens a few entries.

## Declared links

**Is what a section consumes declared?**

🔴 **Every dependency is declared, even without duplication.** A
section that needs another to work references it: the data it reads,
the calculation whose result it displays, the text key it uses, the
entity it persists.

⚠️ **That is what gives the execution order.** A screen displaying a
computed value never copies the rule — without the declaration,
nothing would tie them.

## Resources

**Does this content require something to exist for it to be
available?**

| The answer | What you do |
|---|---|
| No | Move on |
| Yes, and an entry already carries it | Reference it |
| Yes, and no entry carries it | 🔴 **Write that entry yourself** |

⚠️ **A section describing a content does not carry the resource that
makes it available.** A label quoted in a screen section needs its key
in the text section — the product says the wording, the technical
document says the key. **The same holds for a colour and its role, a
screen and its route, a value and the entity that stores it.**

📌 **Writing it is not deciding.** The product settled the wording;
naming the resource that carries it is the translation you are here
for. ⚠️ **Unless the product never settled it** — then it is a
question.

## Completeness

**Does this rule leave a case undetermined?**

🔴 **A rule that does not is not written.** *"Beyond a threshold"*
without the threshold, *"recent entries"* without the window: the case
is open and the code would have to guess.

⚠️ **On an interval, a bound belongs to one case or the other.** Say
which.

📌 **The cases a rule distinguishes must cover every possible value,
each of them once.**

---

# Running it

**Part 1, on each block of the product file.** A block that fails
either test is signalled; nothing is written from it.

**Part 2, on the technical document, once every section is filled.**
🔴 **Not while writing** — entries accumulate, and what they consume or
contradict only shows once the document stands.

⚠️ **A failure is a question, never a fix.** The one exception is
*Resources*, where the missing entry is written when the product
already settled its content.
