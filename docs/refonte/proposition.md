# Proposal — a chain from a prose idea to merged code

This document was written without seeing the chain that runs today. It
is designed against the constraints in `01_conception.md` and against
the example idea file only. Everything marked **Decided:** is a point
the brief left open and that I settled; the last section says which
of those I could not justify to the end, and what would settle them.

---

## 1. Why this split into roles

### 1.1 The three things that force a boundary

Reading the brief, only three things force one agent to end and
another to begin. Every boundary below is placed by one of them, and
I have tried not to place any boundary for another reason.

**a. The reading set changes size.** Some work needs the whole idea
file at once — nothing else can find that a rule stated on line 1180
applies to a screen described on line 400, or that two words on
opposite ends of the file name one thing. Other work needs one slice
of it, plus a little global context. A twelve-hundred-line file is
readable in one context; what is not tenable is reading it *and*
producing hundreds of behaviours' worth of output in that same
context. So the rule is: **an agent that reads the whole file
produces only an index; an agent that produces content reads only
one slice.** Two whole-file readers exist (the Lexicon and the
Mapper) and each writes a table, not prose.

**b. The nature of the material changes.** Prose becomes structured
behaviours; behaviours become questions; answered behaviours become a
plan; the plan becomes interfaces, then tests, then code. At each of
these steps the *skill* asked of the agent changes, and so does what
it must be told not to do (a normaliser must not invent a rule; a
tester must not read the code it tests). Putting two natures in one
context makes the "must not" harder to hold. It also makes the output
harder to check, because the check has nothing crisp to hold it
against.

**c. A check needs independence.** A check is only worth its
invocation if the checker cannot be wrong for the same reason the
producer was. An agent re-reading its own output in the same context
inherits its own misreading. So every check in this chain is a
separate context that reads the *input* of the producer and the
*output* of the producer, and nothing the producer thought. There are
exactly three such checks, and each names what no other catches:

| Check | What it catches, that nothing else does |
|---|---|
| Coverage (prose vs spec) | A sentence of the idea that reached no behaviour — loss at the cheapest point to catch it |
| Tester (spec vs code, via tests) | Code that does less than the spec, or does it differently — enforced by a context that never saw the code |
| Reviewer (diff vs spec) | Code that does *more* than the spec — invention — which no test can catch, since a test asserts presence, not absence |

Nothing else re-verifies. The Coder relies on the Tester's tests; the
Planner relies on the Normaliser's headers; the Designer relies on
the Locator's symbol table. Where an agent finds its predecessor's
work insufficient it stops and says so — it does not redo it.

### 1.2 The product requirement, and how the split serves it

The requirement that the person steps in at the start and never
again means one phase must *prove* the product closed before code
begins. "Prove" is too strong for prose; what can be done is to make
the search for open decisions **systematic and exhaustive by
construction**: apply a fixed list of decision classes to every
behaviour, one by one, and record for each either *settled in the
text, here* or *asked, question n*. That is the Prober, and it is why
the prose is normalised into numbered behaviours *before* it is
probed — one cannot enumerate the decision classes of a paragraph,
but one can of a behaviour.

The cost of that exhaustiveness is the number of questions, and the
brief is right that it is a real design problem. The answer here is
not to ask fewer — it is to make most of them **answerable by
silence**. A question has two tiers:

- **default** — the text does not settle it *here*, but a rule
  elsewhere in the file or a pattern the file already follows gives
  an answer; the agent proposes that answer, cites the source, and
  the person accepts it by not overriding it;
- **mandatory** — nothing in the file gives a basis; the person must
  write an answer.

On the example file, the transverse rules of §13.1 (absence shows as
a dash, a fallback is not an error, the clock never falls back)
answer most *absence* and *failure* questions of every screen by
themselves. The Mapper's job of finding such transverse units is what
makes the default tier possible, and is the main reason the Mapper
exists as a whole-file reader.

### 1.3 Why the technical side has no global document

Downstream, I considered a stage that rewrites the whole product spec
into a whole technical document, and ruled it out (§6). The technical
frame here is two things only: **conventions** (how code is written in
this project — once per project, derived from the code where code
exists) and **a per-lot interface** (the signatures this lot adds or
changes — decided against the actual code at the moment it is
needed). The reason is the brief's own: documents lie, code is the
truth. A technical document written for the whole product before any
lot is coded would be stale by lot three, and every later agent would
have to choose between it and the code.

### 1.4 What the roles are, at a glance

| # | Agent | Reads | Produces | Runs |
|---|---|---|---|---|
| 1 | Lexicon | whole idea file | `lexique.md` | once per feature, then once per answer file |
| 2 | Mapper | whole idea file + lexicon | `carte.md` | once per feature |
| 3 | Normaliser | one unit of prose (or one unit of spec + its answers) | `spec/U-nn.md` | per unit; again per unit per answer round |
| 4 | Coverage | one unit of prose + its spec | `couverture/U-nn.md` | per unit, after first normalisation only |
| 5 | Locator | one spec unit + the code, by grep | `existant/U-nn.md` | per unit, existing application only |
| 6 | Prober | one spec unit + transverse units + lexicon + existant | `questions/U-nn.md` | per unit per round |
| 7 | Collator | every `questions/U-nn.md` of the round | `questions-NN.md` | once per round |
| 8 | Conventions | code tree + samples (existing app) or map + headers (new app) | `conventions.md` | once per project; extended on demand |
| 9 | Planner | map + spec headers + existant headers + conventions | `lots.md` | once per feature; re-run from a lot on a contradiction |
| 10 | Designer | one lot's spec units + conventions + existant symbols + touched files | interface files with stubs, committed | per lot |
| 11 | Tester | one lot's spec units + the interfaces | test files, committed | per lot |
| 12 | Coder | one lot's spec units + interfaces + tests + conventions + touched files | code, committed | per lot, in a loop with the compiler |
| 13 | Reviewer | one lot's diff + its spec units | `revue/L-nn.md` | per lot, in a loop with the Coder |

Plus the **Driver**, which is not an agent (§2.0).

---
## 2. One card per agent

Conventions used in every card: `<f>` is the feature folder,
`docs/<feature>/`. Unit identifiers are `U-nn`, behaviour identifiers
`U-nn.B-mm`, lot identifiers `L-nn`, question identifiers `Q-nnn`.
Every file an agent produces starts with one line, `STATUS: done` or
`STATUS: blocked`, and the Driver reads nothing else of it.

### 2.0 The Driver — what invokes, and what follows

**Decided:** agents never invoke agents. One thing invokes them all,
and it holds no judgement.

The Driver is the Claude Code session in which the person launched the
command. Its rules are a decision table over files: it reads
`<f>/etat.md` (the phase, the round, the current lot), tests for the
existence of the next expected file and the `STATUS` line of the last
one, invokes the next agent with the file paths that agent's card
names, and writes the new state. It never opens an agent's output
beyond the `STATUS` line, never summarises, never decides a product
or technical point. It logs every invocation with the hashes of the
files passed, so a run can be replayed.

Why not let agents chain into each other: an agent that invokes the
next passes its context along, and the next one inherits a reading it
did not do — that is exactly the check-independence of §1.1c lost,
and it is the path by which one early misreading spreads. It also
makes the run depend on the order in which contexts happened to
finish, which breaks reproducibility.

Why the Driver has no judgement: every branch it takes must be
replayable from the files alone. A Driver that reads outputs and
"decides what to do next" is an agent without a card.

### 2.1 Lexicon

    Reads:    idees.md, whole
              — mode 2: reponses-NN.md, whole, plus lexique.md
    Does:     1. Lists every noun phrase that names a thing of the
                 product — an entity (a run, a reference, a segment),
                 a screen, a state (incomplete, in preparation), a
                 measure (segment pace, smoothed pace) — with the line
                 of first occurrence and the count of occurrences.
              2. Groups the phrases that could name one same thing:
                 same head noun, one a qualification of the other, or
                 used in the same position of two parallel sentences
                 ("the favourite" in §5.3, "the reference" everywhere
                 else).
              3. For each group, writes what the text lets it
                 conclude: *one thing, evident* (the text uses them
                 interchangeably in one paragraph), *one thing,
                 probable* (used in parallel contexts), *two things*
                 (the text distinguishes them somewhere), or *cannot
                 tell*.
              4. Chooses one canonical term per group and records the
                 others as synonyms of it.
              5. Every *probable* or *cannot tell* becomes a question
                 line — tier `default` with the canonical term as the
                 proposed answer for *probable*, tier `mandatory` for
                 *cannot tell*.
              6. Mode 2, on an answer file: repeats 1–5 on the answer
                 text only, against the existing lexicon, and appends.
                 Answers bring words the idea never used.
    Produces: <f>/lexique.md — one table: canonical term, synonyms,
              kind (entity / screen / state / measure / action), line
              of first occurrence, verdict; plus a `questions`
              section in the question format of §2.6.
    Runs:     once per feature before anything else; then once per
              answer file, before the Normaliser integrates it.

What it holds at once: the whole idea file and a table of perhaps
fifty rows. It stays in one context because it produces the table and
nothing else — no rewriting, no probing.

### 2.2 Mapper

    Reads:    idees.md, whole; lexique.md
    Does:     1. Cuts the file into units at its own structure —
                 headings first; inside a heading, a change of subject
                 (a new screen, a new rule set). A unit is at most
                 about a hundred lines; a longer section is cut at its
                 sub-headings or, failing that, at its paragraphs,
                 and the cut is recorded by line numbers.
              2. Numbers the units U-01, U-02… in source order. Source
                 order is the only order the input offers that two
                 runs will agree on.
              3. Gives each unit one kind:
                 - `behaviour` — describes what the product does
                   somewhere (a screen, a flow, a calculation);
                 - `transverse` — a rule that applies across units
                   (the example's §13.1, §3, Annex B, Annex C.1);
                 - `directive` — a technical constraint the person
                   wrote (the example's ⚙️ boxes): obeyed, never
                   arbitrated, never turned into a question;
                 - `reference` — a table or format the behaviours
                   cite (Annex A's format, C.4's texts);
                 - `out-of-scope` — the person's own exclusions;
                 - `acceptance` — what the person wants checked by
                   hand on the device;
                 - `external` — pointers to other documents; ignored.
                 A unit that mixes kinds (a directive box inside a
                 screen) keeps the enclosing kind and the box is
                 marked as a directive inside the spec later.
              4. For each unit, lists the cross-references: explicit
                 (a section number, a named term defined elsewhere)
                 and lexical (a canonical term of the lexicon whose
                 defining unit is another one). Over-linking is
                 cheap; a missed link is a gap found late.
              5. For each unit, lists the canonical terms it defines
                 and the ones it only uses.
              6. Marks the transverse units every behaviour unit must
                 be read with.
    Produces: <f>/carte.md — one table: unit, lines, kind, title,
              defines, uses, references; plus the list of transverse
              units.
    Runs:     once per feature.

What it holds at once: the whole idea file and the lexicon, and it
writes a table of thirty to sixty rows. The one thing that needs the
whole file — the cross-reference and the transverse list — is the
only thing it does.

### 2.3 Normaliser

    Reads:    mode 1: carte.md (its own row and the transverse list),
              the lines of its unit in idees.md, the lines of every
              transverse unit, lexique.md
              mode 2: its spec/U-nn.md, the lines of reponses-NN.md
              that carry its unit's identifier, lexique.md
    Does:     Mode 1, from prose:
              1. Reads its unit and rewrites every sentence that says
                 what the product does as a behaviour: an identifier
                 U-nn.B-mm in source order, a **trigger** (the
                 person's action, an event, an elapsed time, a state
                 becoming true), an **outcome** (what is shown,
                 stored, sent, computed), and the **cases** the text
                 already distinguishes (when there is no reference;
                 when the run is incomplete).
              2. Replaces every synonym by its canonical term.
              3. Keeps every directive box attached to the behaviour
                 it constrains, marked `directive`, verbatim.
              4. Keeps render descriptions (tokens, sizes, positions)
                 as the outcome of the behaviour "the screen is
                 shown", never dropped: they are product.
              5. Where a sentence states a behaviour but the trigger
                 or the outcome is not in the text, writes the
                 behaviour with the missing part marked `open` — it
                 does not fill it. Where a sentence contradicts
                 another in the same unit, writes both and marks
                 `contradiction`.
              6. Writes the unit header: entities read, entities
                 written, screens, units referenced, directives
                 present, count of behaviours, count of `open`.
              Mode 2, from answers:
              7. For each answer addressed to a behaviour of this
                 unit, rewrites that behaviour — fills the `open`,
                 adds the case, changes the outcome — and records
                 `settled by Q-nnn` on it.
              8. For a default-tier question the person did not
                 override, applies the proposed default the same way,
                 recorded `settled by Q-nnn (default)`.
              9. Where an answer describes a behaviour no existing
                 identifier covers, appends a new behaviour at the end
                 of the unit, numbered after the last, never inserted
                 — identifiers never shift.
              10. Rewrites the header.
    Produces: <f>/spec/U-nn.md — header, then the behaviours.
    Runs:     once per unit after the Mapper; then once per unit
              touched by an answer file, per round.

Why it reads the transverse units: without them, "list empty: a
message says to paste a result" is written as a behaviour and the
absence rule of §13.1 is never connected to it. With them, the
Normaliser writes the case and cites the transverse behaviour.

Why it does not fill an `open`: it is the point where invention would
enter, unseen, and every later agent would build on it. Marking is
what makes the Prober's work enumerable.

### 2.4 Coverage

    Reads:    the lines of its unit in idees.md; spec/U-nn.md
    Does:     1. Takes the prose sentence by sentence.
              2. For each sentence that says something the product
                 does or shows or refuses, finds the behaviour
                 identifier whose trigger or outcome carries it.
              3. Lists every sentence that has none, with its line.
              4. Lists every behaviour that carries nothing the prose
                 says — the reverse direction, invention at the
                 normalisation step.
              5. Sentences that are commentary, motivation ("the
                 literature places it under 50 %"), or the person's
                 own explanation of a choice are listed under
                 `rationale`, not counted as lost — but listed, so
                 the next context can see the classification.
    Produces: <f>/couverture/U-nn.md — three lists: lost, invented,
              rationale. STATUS is `done` when the first two are
              empty.
    Runs:     once per unit, after the first normalisation only. Not
              after answer rounds: an answer is short, applied by
              identifier, and the Normaliser records which question
              settled what — the traceability is in the spec itself.

Why it is worth an invocation: it is the earliest point at which
"nothing lost" can be tested, and a loss here is invisible to every
later step — the Tester tests the spec, the Reviewer reviews against
the spec; neither ever sees the prose again. One invocation per unit
on a hundred lines is the cheapest check in the chain.

### 2.5 Locator — existing application only

    Reads:    spec/U-nn.md (header and behaviours); conventions.md;
              the code, by grep on the unit's canonical terms, its
              screen names, and every visible string the behaviours
              name — string resources first, then symbol names; then
              the functions those hits sit in, read whole.
    Does:     1. For each grep hit, records the symbol (file, name,
                 kind: screen / view-model / repository / entity /
                 test) and the behaviour identifiers it relates to.
              2. For each behaviour, reads the code around its hits
                 and writes what the code does *today* in one
                 sentence, in product terms — "today the list sorts
                 by name".
              3. Classifies each behaviour against that: `new` (no
                 code does this), `kept` (the code already does it),
                 `changed` (the code does something else here).
              4. Every `changed` whose spec does not itself say it
                 replaces existing behaviour becomes a `mandatory`
                 question: "today X; the idea says Y; replace?" —
                 the person may not know the app does X.
              5. Every `kept` behaviour records whether a test covers
                 it today.
              6. Lists the files any lot on this unit will touch.
    Produces: <f>/existant/U-nn.md — symbol table, per-behaviour
              classification, files to touch, questions section.
    Runs:     once per unit after Coverage, on an existing
              application; not at all on a new one. Not re-run after
              answer rounds unless a round adds a behaviour to the
              unit (the Driver compares behaviour counts).

Why grep and not a project read: the unit names its own terms, and a
term that hits nothing in the code is a `new` behaviour — that is the
answer, not a failure. What it holds at once is one unit's spec and
the handful of functions its terms hit.

Why here and not later: a conflict with existing behaviour is a
product question, and product questions are closed before code. Found
during coding, it is a breach.

### 2.6 Prober

    Reads:    spec/U-nn.md; the spec of every transverse unit;
              lexique.md; existant/U-nn.md when it exists; the
              decision grid, grille.md (a project-level file, see
              below)
    Does:     1. For each behaviour, walks the decision grid class by
                 class. The grid, **Decided:** as a starting list —
                 - *absence*: nothing to show, no data, the thing it
                   depends on does not exist;
                 - *failure*: the operation fails — what is shown,
                   what remains written;
                 - *interruption*: the app is killed, the device
                   sleeps, the link drops half-way — what state is
                   found on return;
                 - *order and ties*: what sorts, what separates two
                   equal things;
                 - *bounds*: minimum, maximum, length, count,
                   precision, rounding;
                 - *permission*: denied, revoked, granted later;
                 - *retroactivity*: a setting or a reference changes —
                   what happens to what already exists;
                 - *conflict*: two rules apply to one situation;
                 - *identity*: two things equal by name, by date;
                 - *text*: every visible string the behaviour shows,
                   named or not;
                 - *existing* (existing application): kept or
                   replaced.
              2. For each class, records one of: `n/a` (the class
                 cannot apply to this trigger — a pure computation has
                 no permission case), `settled: <where>` (this
                 behaviour, or a transverse behaviour, or a directive
                 says it), or a question.
              3. A question carries: identifier Q-nnn (unit, then
                 behaviour, then class, so two runs number alike),
                 the behaviour, the class, the question in the
                 person's words — no technical term — and its tier:
                 `default` with a proposed answer and the citation
                 that grounds it, or `mandatory`.
              4. Every `open` and `contradiction` mark of the
                 Normaliser becomes a `mandatory` question.
              5. Writes the record — the per-class table — and the
                 questions.
    Produces: <f>/questions/U-nn.md — the record (behaviour × class)
              and the question list. STATUS `done` always; the count
              of questions is in the header.
    Runs:     once per unit per round; after round 1, only on units
              the Normaliser rewrote in that round.

Why a grid and not "find what is open": "find what is open" is not
enumerable, and two runs would find different things. The grid makes
the record checkable — a class marked `n/a` on a behaviour that later
turns out to need it names exactly what to add to the grid.

Why one context per unit: the record for one unit of thirty
behaviours is three hundred lines; the Prober reads the transverse
units alongside because that is where the defaults come from.

`grille.md` is a project-level file, not a feature file. It grows by
one line every time a product question surfaces during coding (§3,
loop L5): the class that would have caught it. That is the mechanism
by which the guarantee improves instead of being restated.

### 2.7 Collator

    Reads:    every <f>/questions/U-nn.md of the round, the
              `questions` section of lexique.md (round 1)
    Does:     1. Concatenates the questions in unit order.
              2. Merges questions that ask one thing about one
                 behaviour reached from two units (a transverse rule
                 probed from two screens): keeps the lowest identifier,
                 lists the others as merged into it.
              3. Puts the mandatory questions first within each unit,
                 then the defaults, each default showing its proposed
                 answer and its source in one line.
              4. Writes the one sentence the person needs at the top:
                 answer the mandatory ones; a default you do not
                 override is applied as written.
    Produces: <f>/questions-NN.md — the one file the person reads in
              round NN.
    Runs:     once per round.

Why an agent and not the Driver: the merge in step 2 is a reading, not
a concatenation. It stays small — question files only, never the spec.

### 2.8 Conventions

    Reads:    existing application: the file tree; the build files;
              the test folder's layout; one file of each kind the tree
              shows (one screen, one view-model, one repository, one
              entity, one test) — the largest of each kind, whole;
              the directive units of carte.md
              new application: carte.md, every spec header, the
              directive units, the platforms and the entities they
              name
              mode 2 (extend): conventions.md and one blocked.md of
              class `convention`
    Does:     1. Existing application: reads the samples and writes,
                 for each kind of file, where it lives, how it is
                 named, what it may depend on, and how it is tested —
                 from what the code does, not from what any document
                 in the repository says. Where two samples disagree,
                 writes the majority and records the exception.
              2. New application: decides the stack, the module
                 layout, the naming, the persistence, the test
                 framework, the build and test commands — from the
                 platforms and directives the idea names, otherwise by
                 the platform's default toolchain. **Decided:** the
                 person is not asked; she cannot arbitrate this.
              3. Both: writes the two commands every Coder runs
                 (build, test), the branch naming, and the rule for
                 what a lot may not touch (generated files, existing
                 tests).
              4. Mode 2: reads the block, adds the one convention that
                 unblocks it, records the lot that asked.
    Produces: docs/conventions.md — project-level, not per feature.
    Runs:     once per project; then once per convention block.

What it holds at once: five sample files and a tree. Why it does not
read the project: the conventions are how code is written, and five
representative files show that; reading the rest would show the same
again.

### 2.9 Planner

    Reads:    carte.md; the header of every spec/U-nn.md (not the
              behaviours); the header of every existant/U-nn.md;
              conventions.md
    Does:     1. Lists the entities every unit writes and reads (from
                 the headers).
              2. Forms the **foundation lots**: one per cluster of
                 entities written together (the run and its segments;
                 the profile), containing the data model, the domain
                 constants and the transverse rules that are pure
                 computation (formats, rounding). On a new
                 application, a lot L-00 *scaffold* comes first:
                 project skeleton, build, one passing test.
              3. Forms the **feature lots**: one per `behaviour` unit,
                 merged with any `reference` unit only it uses. A unit
                 over twenty-five behaviours is split at a behaviour
                 boundary into two lots, in identifier order.
                 **Decided:** twenty-five, a size one Coder context
                 holds with its tests and touched files.
              4. Orders: a lot depends on every lot that writes an
                 entity it reads, and on every lot that owns a unit it
                 references. Topological order; ties broken by lowest
                 unit identifier. Two runs give one order.
              5. For each lot: units, behaviour range, depends-on,
                 files it will touch (from existant), and the
                 pre-existing tests that cover kept behaviours in it.
              6. Re-plan mode: from a given lot onward, with the lots
                 before it fixed.
    Produces: <f>/lots.md
    Runs:     once per feature, after the product is closed; again
              from a lot onward on a contradiction block.

Why headers only: the headers carry exactly what the plan needs —
entities and references — and reading the behaviours would be reading
the whole spec for a table. Why vertical lots and not layers: a layer
is not testable against a behaviour, and "nothing lost" is tested per
behaviour.

### 2.10 Designer

    Reads:    the lot's row in lots.md; its spec units, whole;
              conventions.md; the symbol table of its existant units;
              every file the lot touches, whole; the interfaces of
              the lots it depends on (their committed interface
              files)
    Does:     1. For each behaviour, names the symbol that will carry
                 it: an existing one (from existant), or a new one,
                 placed and named by the conventions.
              2. Writes the interface files: types, function
                 signatures, screen entry points, with bodies that
                 fail loudly (`TODO`), in the project's language —
                 enough for tests to compile against.
              3. Writes, in a comment on each symbol, the behaviour
                 identifiers it carries. This is the trace the Tester
                 and the Reviewer read.
              4. For a `changed` behaviour, changes the existing
                 signature only if the behaviour requires it, and
                 lists every caller the grep finds.
              5. Runs the build. A build that fails on the stubs is
                 its own error; it fixes it — two attempts, then
                 blocked.
              6. Commits on the lot branch.
    Produces: interface files, committed; <f>/lots/L-nn/design.md —
              the symbol ↔ behaviour table and the list of callers.
    Runs:     once per lot.

Why a separate context from the Coder: the interface is where "how
does this fit the existing code" is decided, and it must be decided
once, small, with the touched files in view — not discovered by a
Coder half-way through a body. It is also what lets the Tester write
compiling tests before any body exists.

### 2.11 Tester

    Reads:    the lot's spec units, whole; the interface files;
              design.md; conventions.md (test conventions); the
              pre-existing tests that cover kept behaviours in the
              lot. **Never** the bodies — there are none yet.
    Does:     1. For each behaviour of the lot, writes one test named
                 by the behaviour identifier, exercising its trigger
                 and asserting its outcome and every case the spec
                 lists. A behaviour with three cases gets three
                 assertions or three tests, named by case.
              2. For each behaviour it cannot exercise in a test —
                 pure rendering, a system dialog, a sensor — writes a
                 line in a manual list: the behaviour identifier and
                 what to look at, in the person's words. **Decided:**
                 the Tester decides which; the line is the trace.
              3. For each `kept` behaviour of an existing application
                 with no test today, writes one — this is the "what
                 worked still works" guarantee at the point the code
                 is touched.
              4. Runs the tests: every new one must fail (red) and
                 every pre-existing one must pass. A new test that
                 passes on stubs asserts nothing; it rewrites it.
              5. Commits on the lot branch.
              Mode 2 (confront), on a Coder block of class `test`:
              6. Rereads the one test and the one behaviour; either
                 the test is wrong — rewrites it — or it is right —
                 writes why in one paragraph. Never touches code.
    Produces: test files, committed; <f>/lots/L-nn/manuel.md
    Runs:     once per lot; mode 2 once per `test` block.

Why before the Coder, and in another context: a test written after
the code, by the context that wrote the code, asserts what the code
does. Written before, by a context that read only the spec, it
asserts what the spec says. The trace *behaviour → test name* is what
makes the end-of-chain coverage check mechanical.

### 2.12 Coder

    Reads:    the lot's spec units, whole; interface files; the
              tests; design.md; conventions.md; every touched file,
              whole; the code of the lots it depends on, by symbol —
              the interfaces first, bodies only where the signature
              does not say enough
    Does:     1. Fills the bodies, behaviour by behaviour in
                 identifier order, each to make its named tests pass.
              2. Runs the build and the whole test suite after each
                 behaviour, not at the end.
              3. On a failure: reads the failing test and the
                 behaviour it names, fixes the body. The same failure
                 signature (same test, same assertion) three times is
                 a stop: blocked, class `test` if it believes the test
                 wrong against the spec, class `convention` if it
                 lacks a way to do it in this project, class `product`
                 if the spec itself does not say, class `contradiction`
                 if two behaviours cannot both hold.
              4. Never edits a test. Never edits a file outside the
                 lot's touched list without adding it to design.md
                 with the reason.
              5. Runs any static analysis the conventions name; fixes
                 what it reports.
              6. Commits on the lot branch when the suite is green.
    Produces: code, committed; <f>/lots/L-nn/blocked.md when it
              stops, with the class, the behaviour, what it found,
              what it lacks.
    Runs:     once per lot, in a loop with the compiler; resumed after
              a block is settled, from the behaviour it stopped on.

### 2.13 Reviewer

    Reads:    the lot's diff against the integration branch; its spec
              units; design.md; the tests
    Does:     1. Walks the diff symbol by symbol. For each added or
                 changed symbol, finds the behaviour identifier that
                 asks for it (from the trace comment and the spec). A
                 symbol no behaviour asks for is an **invention**
                 finding — unless it is a private helper of one that
                 is, which it says.
              2. For each behaviour of the lot, opens its test and
                 checks that the assertion is the outcome the spec
                 states, not a weaker one (a test that checks "no
                 crash" for a behaviour that says "shows a dash").
              3. Checks the conventions on the diff: placement,
                 naming, no visible string outside resources — only
                 what a grep can confirm.
              4. Writes the verdict: `pass`, or the findings, each
                 with the file, the line, the behaviour identifier and
                 which of the three kinds it is.
    Produces: <f>/lots/L-nn/revue.md
    Runs:     once per lot after the Coder, again after each fix
              round.

Why it exists although tests exist: a test proves presence of what the
spec asks; nothing but a reading proves absence of what it does not.
Why it does not re-run the tests, re-check the interfaces or re-read
the prose: those are settled, and re-verifying them is the cost
explosion the brief names.

### 2.14 What is not an agent

Three steps are mechanical and belong to the Driver:

- **Freezing the product**: when a round yields zero questions, the
  Driver tags `spec/` in git; nothing downstream reads an untagged
  spec.
- **Merging a lot**: on a `pass` verdict, `git merge --no-ff` of the
  lot branch into the integration branch, then the next lot. Lots run
  one at a time, in `lots.md` order — see §5 for why not in parallel.
- **Closing the feature**: after the last lot, the Driver greps the
  test names for every behaviour identifier of the spec, greps the
  `manuel.md` files for the rest, and writes
  `<f>/verification-manuelle.md`: the manual lines, in unit order,
  and a list of identifiers found in neither — which must be empty.
  That list is the "nothing lost" check at the code end, and it costs
  no invocation. The manual file is what the person takes to the
  emulator, in her own time.

---

## 3. Every loop

### L1 — Question rounds

    Between which agents   Prober → Collator → the person → Lexicon
                           (mode 2) → Normaliser (mode 2) → Prober
    What sends you in      a Prober record holds at least one
                           question, of either tier
    What gets you out      a round in which every Prober invoked
                           reports zero questions in its header —
                           checkable by the Driver on the headers
                           alone
    What bounds it         no ceiling: it waits for a person, and each
                           round probes only the units the previous
                           answers rewrote, so the set shrinks unless
                           an answer opens a new behaviour. Decided:
                           at round 4 the Driver adds one line at the
                           top of the question file saying which
                           units keep reopening, so the person can
                           choose to rewrite that part of the idea by
                           hand; the loop itself continues.
    Who steps in           the person, once per round

Why "zero questions" and not "zero mandatory questions": a default
the person has not seen is a decision she has not taken. The last
round is therefore always a round of defaults she confirms by silence
— cheap for her, and the only way the guarantee holds as stated.

### L2 — Coverage retry

    Between which agents   Coverage → Normaliser (mode 1) → Coverage
    What sends you in      the Coverage file lists at least one lost
                           sentence or one invented behaviour
    What gets you out      both lists empty
    What bounds it         one retry. The Normaliser is re-invoked
                           with the Coverage file added to its
                           reading; if the second Coverage still
                           lists something, the unit is blocked
                           (class `normalisation`) and the Driver
                           stops the feature before any question is
                           asked — the person would otherwise answer
                           questions about a misread unit.
    Who steps in           nobody; a block here goes to whoever
                           maintains the chain, not to the person

### L3 — Build and test

    Between which agents   Coder ↔ the compiler and the test runner
    What sends you in      a build error or a failing test
    What gets you out      build green, every test of the lot passes,
                           every pre-existing test passes
    What bounds it         three attempts on one failure signature
                           (same test, same assertion text); then
                           blocked with a class. Distinct failures do
                           not count against each other — a lot of
                           twenty behaviours legitimately sees twenty
                           red tests turn green one by one.
    Who steps in           nobody

### L4 — Review

    Between which agents   Reviewer → Coder → Reviewer
    What sends you in      a verdict with at least one finding
    What gets you out      the verdict `pass` — zero findings
    What bounds it         two fix rounds. A third verdict with
                           findings blocks the lot (class `review`),
                           because a Coder that cannot remove an
                           invention in two tries is being asked for
                           something the spec and the code disagree
                           on, and that is a contradiction to settle,
                           not a fix to retry.
    Who steps in           nobody

### L5 — Blocks

    Between which agents   any blocked agent → the Driver → one of:
                           Conventions (mode 2), Tester (mode 2), the
                           Normaliser (mode 2) then the Planner
                           (re-plan), or the person
    What sends you in      a file whose STATUS line reads `blocked`
    What gets you out      the blocked agent, re-invoked, reports
                           `done`
    What bounds it         one settlement per (lot, class). A second
                           block of the same class on the same lot
                           stops the feature: the settlement did not
                           settle, and looping would spend invocations
                           on a cause the chain cannot see.
    Who steps in           the person, only for class `product` — and
                           that is a recorded breach of the guarantee
                           (see below). Nobody otherwise.

The routing, by class:

| Class | Routed to | What follows |
|---|---|---|
| `convention` | Conventions, mode 2 | the blocked agent resumes |
| `test` | Tester, mode 2 | the Coder resumes with the rewritten test or the Tester's paragraph |
| `contradiction` | Normaliser, mode 2, on the two units, with the block as its "answer"; then Planner re-plan from this lot | the lot restarts from the Designer; its branch is dropped |
| `product` | the person, through a one-question file `questions-NN.md`; Normaliser mode 2; then as `contradiction` | recorded in `<f>/breaches.md`: the behaviour, the class the grid missed; `grille.md` gains that class |
| `normalisation`, `review` | nobody — the feature stops | a person who maintains the chain reads the block |

A `contradiction` is the expensive case — it pays the lot again. It
is bounded to once per lot, and it should be rare exactly because
the Prober's *conflict* class exists to catch it upstream; every one
that reaches coding is also a line for `grille.md`.

### L6 — Designer's build

    Between which agents   Designer ↔ the compiler
    What sends you in      the stubs do not build
    What gets you out      build green with every new test target
                           resolvable
    What bounds it         two attempts, then blocked (class
                           `convention` — the stubs cannot be placed
                           the way the conventions say)
    Who steps in           nobody

---

## 4. The flow, in one view

    idees.md
       │
       ▼
    Lexicon ──────────────► lexique.md
       │
       ▼
    Mapper ───────────────► carte.md   (units U-nn, kinds, cross-refs,
       │                                transverse list)
       ▼   per unit, all at once
    Normaliser (mode 1) ──► spec/U-nn.md
       │
       ▼   per unit, all at once
    Coverage ─────────────► couverture/U-nn.md ──┐
       │                      lost/invented ≠ ∅ ─┘► Normaliser once more
       │                      still ≠ ∅ ──────────► STOP (normalisation)
       ▼   per unit, existing app only
    Locator ──────────────► existant/U-nn.md   (new / kept / changed,
       │                                        symbols, files, questions)
       ▼   per unit ┌────────────────────────────────────────────┐
    Prober ─────────┼─► questions/U-nn.md                        │
       │            │                                            │ L1
       ▼            │                                            │
    Collator ───────┼─► questions-NN.md ──► the person ──► reponses-NN.md
       │            │                                            │
       │            │   Lexicon (mode 2) → Normaliser (mode 2)   │
       │            │   on touched units ─────────────────────────┘
       │ zero questions in every header
       ▼
    Driver: git tag the spec  ═══ product closed; the person is done ═══
       │
       ▼   once per project (if absent)
    Conventions ──────────► docs/conventions.md
       │
       ▼
    Planner ──────────────► lots.md   (L-00 scaffold on a new app,
       │                               foundation lots, feature lots,
       │                               topological order)
       ▼   for each lot, in order, on a branch from the integration head
    ┌──────────────────────────────────────────────────────────────┐
    │ Designer ──► interfaces + stubs (build green, L6)            │
    │    │                                                         │
    │ Tester ────► tests, one per behaviour, red; manuel.md        │
    │    │                                                         │
    │ Coder ─────► bodies; build+test after each behaviour (L3)    │
    │    │             blocked? ──► L5 routing ──► resume / restart │
    │ Reviewer ──► revue.md ──┐                                    │
    │    │        findings ───┴──► Coder fix ──► Reviewer (L4, ≤2) │
    │    │ pass                                                    │
    │ Driver: merge --no-ff into integration                       │
    └──────────────────────────────────────────────────────────────┘
       │
       ▼   after the last lot
    Driver: full suite; grep behaviour ids ↔ test names ∪ manuel.md
       │
       ▼
    verification-manuelle.md ──► the person, on the emulator, her time

Counting invocations on a file the size of the example (say forty
units, of which eight transverse or reference, and twenty-five lots):
2 whole-file readers; 32 Normalisers + 32 Coverages (+ a few retries);
32 Locators on an existing app; 32 Probers then perhaps 10 and 3 on
later rounds; 3 Collators; 3 Lexicon mode 2; ~45 Normaliser mode 2;
1 Conventions; 1 Planner; 25 × (Designer + Tester + Coder + Reviewer)
= 100, plus fix rounds. Around three hundred invocations, most of them
small. The whole idea file is read twice; each unit's prose about
three times; each spec unit about six times; the code, only by grep
and by touched file. What dominates is the lots, and that is where the
robustness is bought.

---

## 5. Why each boundary is where it is — what breaks if it moves

**Lexicon before Mapper, not merged into it.** Move the lexicon into
the Mapper and the cross-reference table is drawn on raw words: "the
favourite" and "the reference" become two entities, and the lot that
owns one never learns it also owns the other. Merge the Mapper into
the Lexicon and one context produces two tables of different nature
from one reading — tenable for tokens, but the second table is drawn
while the first is still a draft, and a synonym settled late is not
propagated. Two cheap whole-file readings cost less than one missed
link.

**Normalise before probing, not after.** Probe the prose and the
questions are about paragraphs; two runs ask different ones, and the
answers cannot be applied by identifier. Probe the behaviours and the
record is a table, replayable, and every answer lands on one line.
What it costs: the Normaliser can misread before anyone has asked
anything — hence Coverage right behind it, before the first question.

**Coverage after the first normalisation only.** Move it after every
round and it reads the prose again for every answer; the answer is
not in the prose, so it would find "lost" what the answer added.
Drop it entirely and the first loss is found on the emulator.

**Locator between Coverage and Prober, not in the Planner.** The
Locator's output feeds *questions* (a silently replaced behaviour).
Put it in the Planner and the conflict surfaces after the product is
closed — a breach by construction on every existing application.

**Prober per unit, with the transverse units.** Give it only its unit
and every absence question is mandatory; give it the whole spec and it
does not fit. The transverse units are the compromise: a hundred and
fifty lines that answer most of the grid for every screen.

**Freeze the spec before Conventions and Planner.** Let the Planner
run on an open spec and a late answer adds an entity the lots do not
own; the plan is re-cut and the order changes — reproducibility lost
for the same idea.

**Conventions per project, not per feature.** A per-feature
conventions file lets two features name a repository two ways; the
second Designer must choose, and it chooses differently on two runs.

**Planner reads headers, not behaviours.** Reading the behaviours
turns the Planner into a third whole-document reader that produces a
table — it would fit, but the table would be drawn from prose that the
headers already summarise, and a header the Planner cannot plan from
is a Normaliser defect to fix there, not to paper over here.

**Designer separate from Coder.** Merge them and the signature is
decided mid-body, after the Coder has read the tests — which do not
exist yet, since the Tester needs the signatures. The order Designer →
Tester → Coder is what lets a context that never sees the code write
the tests.

**Tester before Coder, never after.** After, the tests assert the
code. The whole "nothing lost" guarantee at the code end rests on this
ordering; it is the boundary I would defend before any other
downstream.

**Reviewer after the Coder, on the diff.** Before the Coder there is
nothing to review; on the whole file instead of the diff it re-reads
what earlier lots already passed.

**Lots one at a time, on one integration branch.** In parallel, two
lots that touch one file merge in an order that depends on which
finished first; the merged code differs between runs. Sequential is
slower in wall time and identical in tokens.

**The person at the start only, and the breach file.** The brief makes
it a requirement; the design makes a breach visible and turns it into
a grid line, so the requirement is approached run after run rather
than asserted.

## 6. What I ruled out

**One agent per feature with a plan in its head.** It does not hold a
hundred behaviours and their tests; and when it stops, everything it
knew is lost with the context.

**Agents chaining into each other with inherited context.** Cheaper in
reads, since the next agent already "knows" the file. Ruled out
because inherited context is inherited misreading, because the
independent checks of §1.1c become impossible, and because a chain
whose shape depends on runtime order is not replayable.

**Conversing with the person.** An agent that asks one question,
waits, asks the next — the natural shape in a chat. Ruled out on round
trips (hundreds of them), on reproducibility (the order of questions
depends on the answers), and on the record: a conversation leaves no
per-behaviour table.

**Asking the questions on the prose, before normalising.** Discussed
in §5. Ruled out for replayability of the questions and for the
identifier-addressed answers.

**Having the person sign off the normalised spec.** It would be the
cleanest closure. Ruled out because she will not read fifteen hundred
lines of behaviours she already wrote once in prose, and a sign-off
not read is worse than none; Coverage is the substitute, mechanical
and per unit.

**A global technical document between spec and lots.** One artefact
that says, for the whole product, which modules, which types, which
flows. It would give cross-lot consistency in one place. Ruled out
because it is a second whole-product document that must be maintained
against the code as lots land, and the brief's own constraint says the
code is the truth. Consistency is bought instead by conventions
(global, small) plus the Designer reading the actual interfaces of
the lots it depends on. This is also the point I am least sure of —
see §7.

**Cutting lots by technical layer** (data, then domain, then UI). Each
layer lot is untestable against a behaviour; the first behaviour is
proven only when the last layer lands, which is the late error the
brief prices highest.

**The Coder writing its own tests.** One invocation saved per lot.
Ruled out in §5: the test would assert the code.

**A single end-of-chain verifier reading everything.** It would find
gaps — at the point where each costs the most. The chain instead puts
one small check at each point where a nature changes, and makes the
end check a grep.

**Retrying a blocked agent with a hint.** "Try again, and this time…"
in the same class is the invention path: an agent that could not
produce from the files will produce from the hint. Every block is
routed to the agent whose output was missing, or stops.

**A separate bug-fix chain.** A gap the person finds on the emulator
is a short idea file on an existing application: "the list should
sort by date; it sorts by name". The same chain runs it — the Locator
does the work, the Prober asks little, one lot. A second chain would
be a second set of boundaries to keep consistent with the first.

**Letting the Driver read outputs and decide.** It would save a
Collator, maybe a Planner. Ruled out because a Driver with judgement
is an agent whose card nobody wrote, and the one place a
non-replayable decision would hide.

## 7. What I am not sure of — and what would settle it

Each point below is one I settled without being able to say what
proves me right. The last column is the thing someone could measure
or the case someone could run.

**1. Defaults accepted by silence.** The two-tier question is the
whole answer to "closing costs many questions". If the person skims
and lets a wrong default through, the guarantee is formally held and
practically broken. *Would settle it:* over several features, count
the corrections the person asks for after the emulator whose root
cause is a `settled by Q-nnn (default)` line. If it is not near zero,
the default tier must shrink to citations of transverse rules only,
and patterns "the file already follows" stop counting.

**2. The Mapper's cross-references from one reading.** Explicit
references are safe; implicit ones (a setting in §4.4 governs the arc
in §6.3 without either naming the other) may be missed, and the
Normaliser of §6.3 then writes a behaviour without its dependency.
*Would settle it:* count the `contradiction` and `product` blocks
whose cause is a link absent from `carte.md`. A second Mapper pass
reading the spec headers instead of the prose is the fix if the count
is not zero.

**3. Tester before Coder — worth a full invocation per lot?** It
doubles the reading of each lot's spec. I placed it on the argument of
§5, not on a measure. *Would settle it:* run one feature both ways;
count Reviewer findings of kind "test weaker than spec" and gaps found
on the emulator. If both are equal, the Coder can write the tests
first in its own context and the Tester goes.

**4. The Reviewer.** Its distinct catch is invention, and I do not
know how often a Coder working from named tests invents. *Would
settle it:* findings per lot over a few features. Near zero, and the
Reviewer becomes a grep for the conventions run by the Driver.

**5. No global technical document.** Cross-lot consistency rests on
conventions plus the Designer reading its dependencies' interfaces.
Two lots may still shape one concept two ways (two ways to represent
"no reference"). *Would settle it:* count Reviewer or Designer notes
of the form "this exists differently in lot L-mm"; count the
conventions added by mode 2. If either grows with the number of lots,
a small global *types* document, produced by the Planner from the
foundation lots and read by every Designer, is the fix — not a full
technical document.

**6. The grid's starting list.** Eleven classes, from reading one
example file. *Would settle it:* every `product` block names the class
that would have caught it; a class added twice means the list was
short, a class never added means it was long enough. The grid is a
file precisely so that this is measurable.

**7. Twenty-five behaviours per lot.** A number, chosen so that a
Coder holds the spec, the tests and the touched files at once. *Would
settle it:* the size of the largest lot that completed without a
block, and of the smallest that blocked on context.

**8. Reproducibility of the code itself.** The design makes the split,
the order, the identifiers, the question numbers, the test names and
the signatures reproducible, because each is derived by a rule from
its input. The bodies are not: two runs give two bodies for one test.
I claim that is what "the same code" can mean here. *Would settle it:*
run one closed spec twice and diff `lots.md`, the test file names, the
interface files; those must be identical. If the brief means the
bodies too, only a fixed-seed model or a body-level template makes it
so, and that is outside this design.

**9. The Locator by grep.** A behaviour whose existing implementation
uses none of the unit's words — a generic list component — is
classified `new` when it is `changed`. *Would settle it:* on an
existing application, the count of Designer notes "existing symbol
found that the Locator did not list".

**10. Conventions from five samples.** On an old application with
several generations of style, the largest file of each kind may be
the oldest. *Would settle it:* the count of `convention` blocks per
feature; if it does not fall to zero after the first feature, the
sampling rule should take the most recently modified file of each
kind instead.

**11. The last round of L1 is always a round of defaults.** It costs
the person one more look. I chose it so that "no product decision
left open" is literally true. *Would settle it:* whether she ever
overrides anything in a defaults-only round. If never, across
features, a defaults-only round can be applied without her, and the
loop exits one round earlier.

**12. On independence from the existing chain.** I did not read any
agent file, command file, or process document of this repository. The
environment did, however, place in my context the list of the
project's registered agent names and their one-line descriptions,
which it does for every session. I designed from the constraints and
the example; where a name here resembles one of theirs, the next
context should treat the resemblance as unproven independence, not as
convergence. *Would settle it:* nothing after the fact; it is stated
so the side-by-side comparison can weigh it.
