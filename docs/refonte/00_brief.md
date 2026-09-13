# The chain, in brief

**An automatic coding agent.** A person with no technical background
writes an idea in free prose; compiled, tested, merged code comes out
the other end.

**Eighteen agents, twenty-one commands.** A command is launched by
hand, invokes one or several agents, and stops on a block or at the end
of its work. 🔴 **No command launches another** — each ends by telling
the person what to run next.

---

## Where it starts

`idees.md` — written by hand, in French, with no imposed format.

It carries either a feature of an existing application or, for a new
application, its basic characteristics.

---

## Upstream — from the idea to the technical document

**The Lexicographe settles the vocabulary, before anything is
written.** It sweeps the idea file for the terms that name what the
code will build — a piece of data, an event, a state, an entity, a view
— and raises the ones that could name one same thing. Answered, it
replaces the retired terms in place and writes `lexique.md`, which the
chain reads afterwards.

**The Rédacteur turns the free prose into `desc-produit.md`**: domains,
sections, and blocks — one block, one trigger, one thing produced —
with nothing technical in it. It writes in English, and keeps the
displayed texts in French, as written. A second invocation folds the
person's answers back into that file, marking what it creates `NEW` and
what it changes `MODIFIED`.

**The Découpeur splits** any block carrying more than one trigger. It
splits, and never rewrites a sentence.

**The Classeur fills each block's `Nature:` line** — what the block
produces, among eight: model, persistence, calculation, transition,
external exchange, synchronisation, presentation, access. At the least
doubt, it asks rather than choosing.

**The Sondeurs probe the product file against a grid of tests**, four
invocations at once: three angles run the grid's per-block pass, each
in its own reading order — block by block, question by question, nature
by nature; one global invocation records every block and runs the two
passes that cross the blocks against each other and against the feature
as a whole. **The Assembleur merges their four files into one**,
dropping what two of them raise twice.

**It loops.** The questions file goes to the person, who answers in
French. 🔴 **Every answer re-enters through the Lexicographe, then the
whole chain** — a block an answer changed is split again, classed
again, probed again. The loop stops when the questions file comes out
empty.

**A command then refiles the product file by nature**, by script: the
blocks copied under the eight headings, the sort being a grep on the
`Nature:` line.

**The Convertisseur produces `spec-technique.md`**, where every rule is
written to be coded without deciding anything. One invocation per
nature, all at once, each writing its own section — §1 to §8 — from the
blocks of its nature alone. Then one crosswise invocation, over the
assembled document: the preamble, the references between sections, the
`Consumes:` line closing every entry, the text keys, and the closures
that no single nature can run.

**It loops too**, on the same route: a question reaches the person, and
the answer comes back through the Lexicographe and the whole chain.
When it must assume something to write a rule at all, it writes it and
marks the spot; the split refuses to run while a mark stands.

---

## The conventions — once per project

**The Architecte writes `TECHNICAL_CONVENTIONS.md`**: how this project
codes, derived from the product and the technical document, without
ever reading the existing code. A grid tells it which questions to ask
itself, and the `Consumes:` graph tells it which way modules may depend
on each other.

It raises its own questions when a choice does not derive.

**It also runs mid-course**: a downstream agent that meets a missing
rule writes a request, and the Architecte examines it, settles it, and
amends the file.

---

## The split

**The Cadreur reads the technical document whole** and splits it into
lots. Each lot cites entries of one section only, declares what it
needs, what it produces, what it modifies, and the entry it derives
from. On an existing application, it greps the code for every symbol it
names.

**The Vérificateur** crosses those declarations, notes the defects —
holes, cycles, overlaps — derives the execution order, and groups the
lots into blocks.

**They loop.** A defect sends it back to the Cadreur, three rounds at
most.

---

## The coding — block by block

**The Détailleur** writes the sheets of a whole block in one go:
signatures and acceptance criteria, per lot. It reads the real code to
confirm what exists.

**The Réalisateur** codes one lot, writes its tests, runs the analysis
and the verification.

**The Relecteur** returns a verdict on that lot.

**They loop.** A failure sends it to a fresh Réalisateur, three retries
at most.

**Then the next block**: its sheets are written after the previous one
has been coded, against code that exists.

**The Contrôleur** runs once, when every lot has passed. It confronts
the product file with the sheets and says what was described and is
found nowhere.

---

## The other ways in

**The correction cycle** starts from a list of observed gaps instead of
`idees.md`. **The Diagnostiqueur** investigates each gap in the code —
it is the only upstream agent that reads it — then assembles its
findings into a technical document. The split and the coding follow
unchanged.

**Taking over undocumented code**: the Extracteur builds the global
product document from the code itself, one domain per invocation.

**After a feature is coded**, the Fusionneur merges its product file
into the global product document, sentence by sentence, and writes the
merge report the person reviews.

---

## When an agent cannot produce

It writes a blocking file, with an empty `## Decision` field, and
stops. The person fills that field, and the command hands it back to
the agent, which applies it and resumes.

**Downstream, the Arbitre answers first.** It reads the blocking file
and fills the field when the answer is already in the corpus — a
convention, an entry of the technical document, or the same problem
settled elsewhere in the code. **It hands back to the person** when the
answer turns on what the user sees.

---

## The three moments where the person steps in

A questions file, with empty `Answer:` fields — she answers in French.

A blocking file with an empty `## Decision`.

The manual test on the device, after the code.

---

## What holds it together

🔴 **Each agent reads what its invocation names, and nothing else.** No
agent reads another's file, the process documentation, or another
feature's folder.

🔴 **Every check names what no other one does.** An agent relies on the
work of the one before it; a move that re-checks what an earlier agent
guaranteed is removed rather than doubled.

🔴 **A questions file is written every turn, even empty** — empty means
the chain moves on, filled means it goes back to the Lexicographe.
