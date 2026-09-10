# Technical closure grid

> A closure test, not a checklist. It generates its signals from the
> file under it.

🔴 **A translation is complete when nothing the product settled has
been lost, and nothing it did not settle has been added.** Every rule
sits in one place, names what it consumes, and leaves no case open.

**Two groups, both on the technical document.** 🔴 **By nature** — on
one section, against the blocks it was written from. 🔴 **Across
sections** — once, on the whole document, when every section is
written.

📌 **"Block"** means a block of the product file; **"entry"** a
numbered entry of the technical document.

---

# By nature

## Traceability

**Can you point at the sentence in the product file yours follows
from?**

**Yes** → you made it explicit. **No** → you added.

🔴 **Anything you would have to add is a question**, however small it
looks and however obvious the addition seems.

⚠️ **The additions that slip through are the small ones**: where a
value is stored, which of several items goes first, what a unit is.
**They feel like translation and they are decisions.**

## Nothing dropped

**Read your blocks again, block by block, sentence by sentence: is
everything each sentence states somewhere in an entry?**

🔴 **The unit is the sentence, not the list.** ⚠️ **A sentence
enumerating nothing is dropped as easily as a member of a set** — and
nothing counts it missing.

🔴 **Naming a set erases its members.** *"A relative-date template"*
stands in for three labels; *"a three-case type"* stands in for three
cases to handle. **The product gave them one by one, and each has to
exist in the code.**

| The product gives | The entry must carry |
|---|---|
| Wordings, one by one | Each one, in full |
| A rule's cases | Each case, and what it produces |
| A set of values | Every value, not the set's name |
| A single statement holding no list | 🔴 **That statement** — a position, a relation, a constancy, an absence, a form |

⚠️ **The last row is the one that catches nothing by counting.** 📌 **A
sentence placing one thing against another, or stating that something
never changes, holds no member to count** — 🔴 **and reads as
commentary when it is a requirement.**

📌 **A quoted wording is what is displayed, never an example of a
format.** ⚠️ **Its every character belongs to the entry**, prefix and
punctuation included.

⚠️ **This runs the other way round from *Traceability*.** That one
starts from your sentence and looks for its source; this one starts
from the product's and checks it arrived whole.

📌 **It is a sweep, not a test on one entry** — run it once, on the
finished section.

## Completeness

**Does this rule leave a case undetermined?**

🔴 **A rule that does not is not written.** *"Beyond a threshold"*
without the threshold, *"recent entries"* without the window: the case
is open and the code would have to guess.

⚠️ **On an interval, a bound belongs to one case or the other.** Say
which.

📌 **The cases a rule distinguishes must cover every possible value,
each of them once.**

🔴 **An entry naming where it applies says whether that list is
closed.** ⚠️ **A list read as exhaustive by one reader and as an
example by another leaves the question open** — 📌 **and the entries it
does not name carry nothing either way.**

🔴 **Say it, both ways**: what the list covers, and that nothing
outside it is concerned — or that the entries outside it settle the
question themselves.

**Can any input of the rule take a value the rule cannot compute on?**

🔴 **The corpus bounds it, or the rule says what it returns there.** ⚠️
**Neither leaves the code to invent one**, and what it invents reads as
an answer.

📌 **Distinct from the question above**: that one asks whether the
cases cover the values; this one asks whether the values are ones the
rule can take at all.

## What a nature owes

**Does every field carry what its nature owes it?**

🔴 **A field named without its constraints, a lookup named without its
index, a schema named without its migration** — ⚠️ **the nature says
what it carries, and a field that gets only part of it leaves the rest
to the code.**

📌 **Carried, or declared as having none** — never silent.

⚠️ **This one bears on an entry's contents, not on a rule.**
*Completeness* asks whether a rule leaves a case open; this asks
whether an entry left a field bare.

🔴 **A presentation entry owes the source of everything it shows.** ⚠️ **The
product says what the user finds again on coming back; the technical
document says where the rest comes from** — 📌 **read from a store,
recomputed, or requested afresh.**

📌 **Asked of every presentation entry**, whatever the product decided is
kept: 🔴 **what is not kept is rebuilt from somewhere**, and a view
whose entry does not name that somewhere leaves it to the code.

---

# Across sections

## Declared links

**Is what a section consumes declared?**

🔴 **Every dependency is declared, even without duplication.** A
section that needs another to work references it: the data it reads,
the calculation whose result it displays, the text key it uses, the
entity it persists.

⚠️ **That is what gives the direction of dependencies.** A screen
displaying a computed value never copies the rule — without the
declaration, nothing would tie them.

🔴 **Declared on the entry's last line** — `Consumes:`, then the
entries it needs, or `—` when it needs none:

    Consumes: §1.1, §3.7, §9.4.
    Consumes: —

⚠️ **A dependency stated only in the prose is not declared** — whoever
reads these lines as a graph never sees it.

**Does the destination carry what the reference attributes to it?**

🔴 **A reference names what it expects of its target.** ⚠️ **The entry
cited carries it, or the reference is false** — and a false reference
is worse than none: it reads as settled.

📌 **Declaring a link and checking it are two closures.** The first
asks whether the dependency is named; this one asks whether the thing
named answers for it.

## Singularity

**Does this rule live in one place?**

🔴 **Never duplicate between sections — reference instead.**

**And is that place the one the behaviour comes from?**

🔴 **Ask it of every rule, not only the ones written twice.** ⚠️ **A
rule living in the section where it is seen holds only there** — a
second path reaching the same thing never meets it.

📌 **The owning section answers "where does this behaviour come from",
not "where is it seen".** A calculation rule belongs to calculations
even if it produces a display; a field bound to the model even if it
shows at input time.

⚠️ **A cross-domain interaction matrix belongs to the domain that
applies it**, never to the ones it concerns.

## Agreement between entries

**Do two entries say the same thing about the same subject?**

🔴 **They come from two product blocks that spoke of the same rule.**
**Neither is a duplicate anyone chose to write** — one thing
reformulated twice rarely comes out the same twice.

| Where it shows | What to look for |
|---|---|
| A rule restated | One entry lists a case another excludes |
| A value repeated | Two entries give it with different precision or units |
| A label quoted twice | The two wordings differ |
| An order of precedence | Two entries state it in opposite directions |

⚠️ **This is not *Singularity*.** That one bars duplication you chose;
this one catches the duplication you did not notice.

**Do two entries treat the same kind of thing in two ways?**

🔴 **Two durations against a threshold, two identifiers, two orders,
two units** — ⚠️ **the kind is the same, the answer has to be.**

📌 **The reverse of the closure above**: that one looks for two
wordings of one rule, this one for two rules of one kind. **Neither is
wrong on its own; together they are.**

**Does one entry give two answers to one question?**

🔴 **A rule holding two cases gives each its own answer** — ⚠️ **and
the entry says which case is which.** 📌 **Written as one name covering
both, it reads as one answer**, and whoever codes it keeps whichever
half they read.

🔴 **Two calculations, two values, two forms under a single name are
two rules.** ⚠️ **Name the condition that separates them**, or write
one of them out of the entry.

📌 **Nobody else can see it.** The Cadreur reads the whole document but
does not judge its content; every agent after him opens a few entries.

## Resources

**Does this content require something to exist for it to be
available?**

| The answer | What you do |
|---|---|
| No | Move on |
| Yes, and an entry already carries it | Reference it |
| Yes, and no entry carries it | 🔴 **Write that entry yourself** |

⚠️ **A section describing a content does not carry the resource that
makes it available.** A label quoted in the presentation section needs
its key in the text section — the product says the wording, the technical
document says the key. **The same holds for a colour and its role, a
view and its route, a value and the entity that stores it.**

📌 **Writing it is not deciding.** The product settled the wording;
naming the resource that carries it is the translation you are here
for. ⚠️ **Unless the product never settled it** — then it is a
question.

🔴 **A content described without being quoted needs its resource just
the same.** ⚠️ **An entry saying that something is stated, indicated
or announced, without giving the words, still puts a wording on
screen** — 📌 **and nothing quoted is nothing to trace.**

🔴 **Ask what will be read there**, and either reference the entry
carrying it or raise the question. ⚠️ **Leaving it undecided sends
whoever codes it to invent a wording**, and nothing downstream will
say it was invented.

---

# Running it

**By nature — on each section, once it is written.** 🔴 **Not while
writing** — what a section dropped or left open only shows once it
stands. 📌 ***Nothing dropped* sweeps rather than tests an entry**: it
reads the blocks again.

**Across sections — once, on the whole document, when every section
is written.** 📌 ***Agreement between entries* sweeps rather than tests
an entry**: it reads the document as a whole.

⚠️ **A failure is a question, never a fix.** The one exception is
*Resources*, where the missing entry is written when the product
already settled its content.
