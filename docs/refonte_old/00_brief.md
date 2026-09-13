# The chain, in brief

**An automatic coding agent.** A person with no technical background
writes an idea in free prose; compiled, tested, merged code comes out
the other end.

---

## Where it starts

`idees.md` — written by hand, in French, with no imposed format.

It carries either a feature of an existing application or, for a new
application, its basic characteristics.

---

## Upstream — from the idea to the technical document

**The Analyste** turns the free prose into `desc-produit.md`: a file
structured in blocks, each describing one behaviour, with nothing
technical in it.

**It loops.** A second invocation reads that file against a grid of
tests and writes the questions the product leaves open. The person
answers, the Analyste folds the answers in, the grid runs again. The
loop stops when no question comes out.

**The Convertisseur** refiles that document by technical nature —
model, persistence, calculation, screen, text, and eight others — then
produces `spec-technique.md`, where every rule is written to be coded
without deciding anything.

**It loops too**, against its own grid, with the same back and forth of
questions.

---

## The conventions — once per project

**The Architecte** writes `TECHNICAL_CONVENTIONS.md`: how this project
codes, derived from the product and the technical document, without
ever reading the existing code. A grid tells it which questions to ask
itself.

It raises its own questions when a choice does not derive.

**It also runs mid-course**: a downstream agent that meets a missing
rule writes a request, and the Architecte examines it, settles it, and
amends the file.

---

## The split

**The Cadreur** reads the technical document whole and splits it into
lots. Each lot declares what it needs, what it produces, what it
modifies, and the entry of the technical document it derives from.

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

## The correction cycle

It starts from a list of observed gaps instead of `idees.md`.

**The Diagnostiqueur** investigates each gap in the code — it is the
only upstream agent that reads it — then assembles its findings into a
technical document. The split and the coding follow unchanged.

---

## When an agent cannot produce

It writes a blocking file, with an empty `## Decision` field, and
stops.

**The Arbitre** reads it and fills that field when the answer is
already in the corpus — a convention, an entry of the technical
document, or the same problem settled elsewhere in the code. The agent
resumes.

**It hands back** when the answer turns on what the user sees. The
person settles it herself.

---

## The two moments where the person steps in

A questions file, with empty `Answer:` fields.

A blocking file the Arbitre could not settle.

---

## How it runs

Numbered commands, launched by hand. Each invokes one or several
agents, and stops on a block or at the end of its work.
