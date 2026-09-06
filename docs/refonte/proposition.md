# A chain from an idea to merged code — a design

This document designs a chain of agents that turns `idees.md`, written
in free prose by a person with no technical background, into compiled,
tested, merged code. It was written against the constraints of
`01_conception.md` and against nothing else. It carries reasons, not
only choices; the last section says what was settled without proof and
what would prove it.

The document is long on purpose. A later context reads it without the
author, and the parts that matter most — the *Does* fields, the loop
stopping tests, the rejected designs — are the parts that cannot be
compressed without losing what they are for.

---

## 0. The spine of the design, in five sentences

1. **Every product statement gets an identifier at the moment it is
   written down, and that identifier travels unchanged to the test that
   proves it.** `P-12` in the product file becomes a citation in
   technical item `T-31`, which lands in lot `L-04`, whose test is named
   `P12_...`. Coverage — nothing lost, nothing invented — is then a
   *mechanical* comparison of identifier sets, not a reading by an agent.
2. **All product decisions are closed against a fixed grid, with a
   proposed default on every question**, so the person answers by
   exception. The grid makes closure systematic; the defaults make it
   cheap.
3. **Tests are written before the code, by a different agent, from the
   acceptance criteria** — so the test is a check on the implementer
   that costs nothing extra, because the tests had to exist anyway. There
   is no reviewer agent.
4. **On an existing application, the code is surveyed fresh at every
   run, and what it does today is turned into tests before anything is
   modified.** Those tests are validated against the untouched code — the
   only truth — before the first change.
5. **What invokes the agents is a conductor that reads a one-page
   ledger and never opens an artefact.** Agents do not call agents; the
   conductor decides by a table.

Everything below is the unfolding of these five.

---

## 1. Why this split into roles

### 1.1 What the split is derived from

The brief gives three facts that decide the shape before any role is
named:

- **An agent has a finite context.** So the work must be cut into pieces
  each of which fits in one reading, and the cuts must fall where the
  hand-over can be a *file*, not a conversation.
- **The person can arbitrate product, and only product.** So there must
  be a place where every product decision is taken — with her — and
  after that place, nothing may reach her. Every technical decision must
  be taken by something that is not her, and must never be phrased to
  her as a question.
- **An error found late costs everything since.** So the artefacts must
  be ordered from the cheapest-to-correct to the most expensive, and the
  checks worth paying for are the ones placed *before* the expensive
  part begins, not after it ends.

From these, the chain has three regions, separated by two hard
boundaries:

```
  [ A. closing the product ]  ‖  [ B. deciding the technique ]  ‖  [ C. producing the code ]
        with the person             without the person, once           without the person, per lot
```

The first boundary (‖ between A and B) is **the product freeze**: after
it, `product.md` is immutable for the run, and a product question
arriving later is recorded as a defect of region A, not answered in
place. The second (‖ between B and C) is **the technical freeze**: after
it, `tech.md` and the split are the contract, and an implementer that
finds them wrong stops rather than repairs them.

### 1.2 Where the roles come from

Inside each region, a role exists when one of three things is true:

- **the input it reads is of a different nature from what the neighbour
  reads** (prose vs. code; a product file vs. a technical one) — mixing
  them in one context makes the agent carry two vocabularies and answer
  in the wrong one;
- **its output must be judged by a fresh reader** — the author of a text
  cannot see what is ambiguous in it, because the author holds the
  intent that the text failed to carry;
- **it repeats** on a different unit (per lot) while its neighbour runs
  once (per feature) — folding a per-lot step into a per-feature agent
  means reloading the feature-sized context every lot.

Applying those three tests gives the roles below. Each one is named
with the test that created it.

**Region A — closing the product**

| Role | Created by | What it holds at once |
|---|---|---|
| **Structurer** | nature: reads prose, writes numbered statements | `idees.md` + the grid + (on an existing app) the code map |
| **Surveyor** | nature: reads code, writes a digest | the modules the idea touches |
| **Closer** | fresh reader: judges `product.md` without having seen the prose | `product.md` + the grid |

**Region B — deciding the technique**

| Role | Created by | What it holds at once |
|---|---|---|
| **Architect** | runs once per *project*, not per feature | the stack, the layout, the tools |
| **Designer** | nature: reads product, writes technical | `product.md` + `code_map.md` + `conventions.md` |
| **Splitter** | reads only the technical file; must be rule-bound for reproducibility | `tech.md` |

**Region C — producing the code**

| Role | Created by | What it holds at once |
|---|---|---|
| **Test-writer** | fresh reader of the lot: writes the proof before the code exists | one lot + the signatures it names |
| **Implementer** | repeats per lot | one lot + its tests + the files it names |
| **Settler** | handles what the others stop on | `blocked.md` + the one artefact it must amend |

And one thing that is not an agent:

| | |
|---|---|
| **Conductor** | reads `state.md`, decides the next invocation by a table, runs git and the mechanical checks, and is the only thing that ever addresses the person |

Nine agents and a conductor. There is no reviewer, no auditor, no
"quality" role: section 1.4 says why.

### 1.3 What the boundaries carry: files with identifiers

Because agents do not share context, every boundary is a file, and the
file has to be readable *without the previous agent's reasons*. The
device that makes this hold is the identifier chain:

```
sentence in idees.md
   └─▶ P-n   product statement          product.md       (Structurer)
         └─▶ T-n   technical item        tech.md          (Designer)   cites P-ids
               └─▶ L-nn  lot             lots/L-nn.md     (Splitter)   lists T-ids
                     └─▶ test P<n>_...   test files       (Test-writer) named by P-id
```

Three consequences:

- **"Nothing lost"** is the set difference `{P} − {P cited by some T}`
  and later `{P} − {P named by some passing test}`. Both are computed by
  a script, at zero tokens.
- **"Nothing more"** is the set of `T` items citing no `P`, plus the set
  of files touched by a lot outside those it declared. Both mechanical.
- **Reproducibility** is anchored: the ids are assigned in document
  order, and the Splitter's rules are functions of the ids and the
  declared dependencies, nothing else.

### 1.4 Why there is no reviewer

The brief says every check must name what no other one already does.
Going through the candidates:

- *A reviewer reading the code against the lot.* What it would catch:
  the implementer misread the spec; the implementer wrote more than the
  spec. The first is caught by the tests, provided they were **not
  written by the implementer** — hence the Test-writer. The second is
  caught by the file-scope check, mechanically. What remains for a
  reviewer is "the code passes the tests but is wrong anyway", which
  means the tests were wrong — and a reviewer reading the same lot
  would have the same blind spot as the Test-writer, since both read the
  same text. The check is not distinct; it is dropped.
- *A final audit of all code against the product.* No context holds it;
  and the id chain gives its mechanical equivalent.
- *A check on the Designer.* Its output is judged by the Splitter (which
  fails on a citation gap) and by the coverage script. A reader of
  `tech.md` who had not read `product.md` could not judge it; one who
  had would be re-doing the Designer.

Two checks *are* kept, and each names what it alone catches:

- **The Closer** (region A). It reads `product.md` without the prose. It
  catches the one thing the Structurer cannot: a statement that is clear
  to its author and ambiguous on its own — which is exactly how every
  later agent will read it. It sits at the cheapest point of the chain,
  before every expensive step, and it is the explicit guarantee the
  product requirement demands.
- **The preservation tests** (lot L-00 on an existing app). They catch
  the one thing no test written *after* a change can: that the change
  broke what was there. They are validated against untouched code before
  the first modification, which is the only moment that validation is
  possible.

---

## 2. The conductor — what invokes, and what follows

The brief asks who decides to invoke an agent and what follows. Here it
is a **conductor**: the top-level Claude Code session, following a fixed
command file. It is not an agent in the sense of the brief — it does
not produce; it dispatches.

**What it reads.** One file, `docs/runs/<feature>/state.md`, a ledger
of under a page:

```
feature:      export-csv
region:       C
lot:          L-04
attempt:      2            # fresh implementer invocations on this lot
status:       FAIL         # OK | FAIL | BLOCKED
blocked_kind: -            # product | technical | -
questions:    0            # open items in questions.md
history:
  A structurer   OK   12 questions
  A surveyor     OK
  A structurer   OK   3 questions
  A closer       OK   1 question
  A structurer   OK   0 questions
  A closer       OK   closed
  B designer     OK   T-1..T-38
  B splitter     OK   L-00..L-07
  C L-00 tests   OK
  C L-01 tests   OK
  C L-01 impl    OK   merged 3f1a2c
  ...
```

Plus the **first line** of `blocked.md` when status is `BLOCKED`, which
carries the kind. It reads nothing else — not `product.md`, not
`tech.md`, not a lot, not a diff. This rule exists because a conductor
that reads artefacts accumulates a run's worth of context over thirty
lots and becomes both expensive and opinionated. It must stay dumb.

**How it decides.** By this table, and only this table:

| State | Next invocation |
|---|---|
| no `product.md` | Surveyor (existing app) then Structurer; or Structurer alone (new app) |
| `questions.md` has open items | hand to the person; wait; then Structurer (integration) |
| `questions.md` empty, Closer not yet run on this version | Closer |
| Closer returned questions | hand to the person; wait; then Structurer (integration) |
| Closer returned `closed` | product freeze → Architect if no `conventions.md`, else Designer |
| `tech.md` exists, coverage script clean | Splitter |
| coverage script reports gaps | Designer, with the gap list |
| `lots.md` exists, lot L-nn pending | Test-writer on L-nn |
| L-nn tests written | Implementer on L-nn (L-00 skips the implementer) |
| L-nn `OK` | mechanical: scope check, full suite, merge; then next lot |
| L-nn `FAIL`, attempt < 3 | Implementer on L-nn, fresh, with the failure log |
| L-nn `FAIL`, attempt = 3 | write `blocked.md` (technical); Settler |
| `BLOCKED technical` | Settler; then resume at the lot it names, with stale lots reset |
| `BLOCKED product` | halt; question to the person via `questions.md`; Structurer (integration); Designer on the affected P-ids; Splitter on the affected T-ids; resume |
| last lot merged | coverage-by-tests script; final full suite; report to the person |

**What it does itself, with no agent.** Git (`worktree`, `merge`,
`log`), the scripts (id coverage, file scope, the project's build and
test commands run once for the full suite after each merge), and
writing `state.md`. Everything that can be a script is a script;
the conductor is a model only because the command file has to react to
a `blocked.md` whose kind is a word.

**Why not a shell script entirely.** It nearly could be. What stops it
is the `BLOCKED product` row: deciding which P-ids a late question
affects is a reading, and the affected-ids list is written by the
Settler, not the conductor — so in fact the conductor stays mechanical
even there. This is stated as a goal: the conductor should be
replaceable by a script without loss, and any pressure to make it
"understand" something is a sign that a role is missing.

---

## 3. The files

All in `docs/runs/<feature>/` unless noted. Named here once; the cards
refer to them.

| File | Written by | Read by | Nature |
|---|---|---|---|
| `idees.md` | the person | Structurer, Surveyor | free prose |
| `code_map.md` | Surveyor | Structurer, Designer, Test-writer (L-00) | verbatim signatures and behaviours of the touched modules; regenerated every run |
| `product.md` | Structurer | Closer, Designer, Settler | numbered statements `P-n`, each tagged with its source sentence, each grid cell filled |
| `questions.md` | Structurer, Closer, Settler | the person, Structurer | one block per question, with `Default:` and `Answer:` lines |
| `docs/product_defaults.md` | Structurer (proposals), the person | Structurer | project-level product conventions accepted once |
| `docs/grid.md` | written once per project by hand; the Structurer and Closer read it | | the product closure grid |
| `docs/conventions.md` | Architect | Designer, Splitter, Test-writer, Implementer | how to code here: stack, layout, test framework, commands, naming, commit format |
| `tech.md` | Designer, Settler | Splitter, Test-writer, Settler | numbered items `T-n`, each citing P-ids, with signatures and files |
| `lots.md` | Splitter | conductor (order only), Settler | ordered index of lots with dependencies |
| `lots/L-nn.md` | Splitter | Test-writer, Implementer | one lot: T-ids, files allowed, acceptance criteria per P-id, signatures |
| `blocked.md` | any agent that stops | conductor (first line), Settler | `KIND: product|technical` then the question |
| `state.md` | conductor | conductor | the ledger |
| the code and tests | Test-writer, Implementer | Implementer | the truth |

---

## 4. One card per agent

Cards follow the format the brief asks for. The *Does* field lists
moves in order. Where an agent reads more than "one thing", the card
says why that holds.

### 4.1 Surveyor

    Surveyor
    Reads:    idees.md
              the project's code, by grep and by opening the files the
              grep names — bounded, see below
    Does:     1. Extract from idees.md every noun that could name a
                 thing in the code: screen names, entity names, actions,
                 field names — in the person's words.
              2. Grep the code for each, and for the obvious technical
                 synonyms (the person's "list of runs" → RunList,
                 runs, Run). Record which files hit.
              3. From the files that hit, walk one hop outward: the
                 files they import from and the files that import
                 them. Stop there. This is the touched area.
              4. For every file in the touched area, copy — verbatim,
                 by grep, never paraphrased — the public signatures:
                 classes, functions, their parameters and return types,
                 the data fields with their types and nullability.
              5. For every public function, write one line of what it
                 does today, as observed from its body — not from its
                 name, not from a comment.
              6. List the existing tests that cover the touched area,
                 by test name, and which symbol each exercises.
              7. Note every existing behaviour the idea would change,
                 as "today: X" — this is the raw material of the
                 preservation lot and of the Structurer's defaults.
              8. Write code_map.md. If the touched area exceeds what
                 one reading holds (rule: more than ~40 files or the
                 signatures alone over ~1500 lines), write the map
                 for the files that hit directly, list the one-hop
                 files by name only, and mark the map PARTIAL so the
                 Structurer knows what is missing.
    Produces: code_map.md
    Runs:     once per feature, on an existing application only —
              plus at most one extension run, on the Structurer's
              request, for an area the map lacks

*Why it reads code and prose at once.* It has to: the map's boundary is
defined by the prose vocabulary. What it holds is small — nouns from
the idea, file names, signatures — and the signatures are copied, not
understood. It never reads a whole project; the one-hop rule is what
keeps it bounded, and the PARTIAL marker is what happens when the rule
is not enough.

*Why every run, not once.* Documents lie; the last run's map describes
the code before the last feature was merged. The map is cheap relative
to a gap it prevents, and it is the only document in the chain that is
allowed to be trusted, precisely because it is regenerated from the
truth each time and copies rather than describes.

### 4.2 Structurer

    Structurer
    Reads:    idees.md
              docs/grid.md
              docs/product_defaults.md
              code_map.md                     (existing app)
              product.md + questions.md       (integration mode only)
    Does:     — first pass —
              1. Read idees.md whole. Cut it into sentences. Number
                 them S-1..S-n in order; this numbering is never
                 changed afterwards.
              2. Sort each sentence into one of: a thing shown (screen,
                 view, element), a thing done (action), a thing kept
                 (entity, field), a rule (ordering, limit, condition),
                 or noise (motivation, pleasantries) — noise is kept
                 in a "context" section, never turned into a
                 statement.
              3. Rewrite each non-noise sentence as one or more
                 product statements P-n, one fact per statement, in
                 the person's vocabulary, each tagged with its S-id.
                 A statement says what is seen or what happens; it
                 never says how.
              4. Open the grid. For every screen, run the screen
                 rows (what shows when empty; while loading; on
                 error; what each element does; what leaves the
                 screen). For every action: precondition, effect,
                 what the person sees after, what happens on failure,
                 whether it can be undone. For every entity: fields,
                 which are required, what makes two equal, what
                 orders them, what breaks a tie, limits, what deleting
                 one does to what depends on it, what happens to data
                 created before this feature. For every list: order,
                 ties, filter, empty. For every write: what happens if
                 it stops half-way.
              5. For every grid cell no statement fills: first look
                 in product_defaults.md — if a project default covers
                 it, write the statement, tagged (project default),
                 and do not ask. Then look in code_map.md — if the
                 code does something today, write the statement
                 tagged (as today) and do not ask. Otherwise write a
                 question.
              6. Every question carries: the P-id or grid cell it
                 attaches to; the question in one sentence, in the
                 person's words; a Default: line with the answer the
                 Structurer would take, phrased as a statement; an
                 empty Answer: line. Questions are grouped by screen,
                 in the order the screens appear in idees.md, so the
                 person reads in the order she wrote.
              7. If a question could not be asked because the code
                 map lacks the area (a screen the idea names that
                 no file hit), write it under "survey gap" instead.
              8. Write product.md (statements) and questions.md.
              — integration mode —
              9. Read questions.md. For every question with a
                 non-empty Answer: write the statement from the
                 answer, tagged (answered). For every empty Answer:
                 write the Default as the statement, tagged (default).
                 Remove the question.
              10. Re-run step 4 on the new statements only — an
                  answer can open a cell (she said "sort by date";
                  now: which date, and ties?). Write any new
                  questions, with defaults.
              11. For every (default) statement that is not specific
                  to this feature — "lists are newest first", "a
                  delete asks for confirmation" — append it to
                  product_defaults.md under "proposed", with the
                  feature name. The person strikes what she rejects;
                  what stays becomes a project default for the next
                  feature.
              12. Rewrite product.md whole, with a header line:
                  N statements, K answered, D by default, C from code.
    Produces: product.md, questions.md
              (and appends to docs/product_defaults.md)
    Runs:     once per feature in first pass, then once per round of
              answers, in a loop with the person and the Closer

*Why the defaults.* The product requirement says all questions are
asked up front, and warns that this costs. The cost is not the number
of questions written; it is the number the person has to *think about*.
A question with a default is read in three seconds and skipped; a
question without one stops her. So the Structurer always proposes, and
the header line tells her how many decisions were made for her, so
that "I did not read them" is a choice she makes knowingly.

*Why the grid, not the Structurer's judgement.* Two runs on one idea
must give the same product file. A grid walked row by row does; an
agent asked "what is missing?" does not. The grid also fixes the
*kind* of question — the ones the brief names: what shows when there is
nothing, what becomes of data written half-way, what separates two
equal things — so completeness is a property of the grid, checkable and
improvable by hand, not of the run.

*Why one statement per fact.* So that a P-id can be cited, tested, and
found missing. A statement with two facts hides one from the coverage
script.

### 4.3 Closer

    Closer
    Reads:    product.md
              docs/grid.md
    Does:     1. Read product.md without idees.md. This is the point:
                 it sees exactly what every later agent will see.
              2. For every statement, ask one thing: can two
                 reasonable readers implement this differently and
                 both claim they followed it? If yes, write a
                 question, with a Default, attached to the P-id.
              3. Walk the grid once more, row by row, per screen,
                 action, entity, list, write — and for every cell,
                 name the P-id that fills it. A cell with no P-id is
                 a question.
              4. Look for statements that contradict each other (two
                 orderings for one list; a required field the create
                 screen does not show). Each contradiction is a
                 question.
              5. If there is no question: append CLOSED and the count
                 of statements to the header of product.md. Otherwise
                 write questions.md.
    Produces: questions.md, or the CLOSED mark in product.md
    Runs:     once per feature after the questions loop empties; again
              after each round its own questions trigger

*Why a separate agent and not a second pass of the Structurer.* The
Structurer wrote the statements with the prose in view; where the prose
was ambiguous, it resolved the ambiguity in its head and may have
written a statement that carries the resolution only for someone who
also read the prose. The Closer has not. That is the whole value, and
it is lost the moment the Closer reads `idees.md`.

*What it is not.* It is not a second Structurer: it never rewrites a
statement, never restructures. It asks, or it closes.

### 4.4 Architect

    Architect
    Reads:    new app:       product.md
              existing app:  code_map.md, and by grep the build files
                             (the manifest, the dependency file, the
                             test configuration, the CI file)
    Does:     1. New app: choose the stack from what product.md implies
                 (a mobile app; a web service; a CLI) — one language,
                 one framework, one test framework, one build tool.
                 Choose the ones with the largest ecosystem for that
                 kind of application; write the choice and the reason
                 in one line each. This is a technical decision: it is
                 never asked.
              2. Existing app: read the build files and write down
                 what is there: language and version, framework, test
                 framework, how to build, how to run the tests, how
                 to run one test file, the directory layout as it is,
                 the naming as it is (from three examples in
                 code_map.md).
              3. Both: write the layer order the Designer and Splitter
                 will use — data model, persistence, domain logic,
                 application state, UI — with the directory each layer
                 lives in.
              4. Both: write the test conventions — one test file per
                 source file; test names begin with the P-id they
                 prove (P12_empty_list_shows_placeholder); what is
                 mocked and what is not.
              5. Both: write the commit format, the exact build
                 command, the exact test command, the exact
                 single-file test command, and what "green" means
                 (zero failures; zero analyzer warnings, or the
                 existing baseline count on an existing app).
              6. New app only: write the scaffold lot — the list of
                 files that make an empty project build and run one
                 trivial test. This becomes L-00.
    Produces: docs/conventions.md
    Runs:     once per project — re-run only when the conductor finds
              the build or test command in conventions.md failing on
              the untouched code at the start of a run

*Why once per project.* Conventions that change per feature are not
conventions, and an implementer reading them must be able to trust
them across lots. On an existing app they mirror the code, which is
why the Architect reads the build files itself rather than trusting a
README.

### 4.5 Designer

    Designer
    Reads:    product.md (CLOSED)
              code_map.md                     (existing app)
              docs/conventions.md
    Does:     1. Read product.md whole. List the entities (things kept)
                 with their fields, the screens, the actions.
              2. Data model first: for every entity, decide the stored
                 shape — type of each field, nullability, keys,
                 relations — and, on an existing app, whether it
                 already exists in code_map.md (then: reuse, extend, or
                 leave). Write one T item per entity, citing the P-ids
                 for its fields and rules.
              3. Persistence: for every write the product names,
                 decide where it goes and what "half-way" means for it
                 (the product said what the person sees; the Designer
                 says transaction or not). One T per store or per
                 operation group, citing P-ids.
              4. Domain logic: every rule (ordering, tie-break, limit,
                 validation, computation) becomes one T with a
                 function signature: name, parameters, return type,
                 the file it lives in. Cite the P-ids.
              5. Application state: for every screen, what state it
                 reads and what it mutates; one T per screen state,
                 with the signatures.
              6. UI: for every screen and element, one T naming the
                 widget/component, its file, the state it binds to,
                 and the P-ids it shows.
              7. Number the T items in the order written — by layer,
                 then by first-cited P-id. Numbering is by this rule,
                 not by hand, so a re-run numbers the same.
              8. For every T that touches a symbol present in
                 code_map.md, write "modifies <symbol>" or "reuses
                 <symbol>", with the verbatim current signature copied
                 from the map beside the new one.
              9. Declare dependencies: a T that uses a symbol another
                 T creates writes "depends: T-k". Nothing else counts
                 as a dependency.
              10. Under "decisions taken", list every technical choice
                  that was open — cache or not, one table or two,
                  which widget — with one line of reason. These are
                  recorded so nobody later mistakes them for product
                  asks.
              11. Before writing, apply the product test to each
                  decision: would the person see the difference on
                  screen or in her data? If yes, it is not the
                  Designer's to take — write blocked.md, KIND: product,
                  citing the P-id whose closure failed, and stop.
                  (This is the failure path of the guarantee. It is
                  meant to be rare; section 7 says what its frequency
                  measures.)
              12. Write tech.md, with the coverage table at the end:
                  every P-id and the T-ids citing it.
    Produces: tech.md
    Runs:     once per feature; again, restricted to named P-ids or
              T-ids, when the coverage script or the Settler hands
              back a list

*Why the whole product file at once.* The data model is shared by every
screen; a Designer that saw one screen at a time would design two
tables for one thing. What it holds is `product.md` — one feature,
closed, statements only — and the map's signatures. For a feature that
is a whole application, see the size rule below.

*Size rule for a whole application.* If `product.md` exceeds ~200
statements, the Designer runs in two shapes: a first invocation that
reads everything and writes only steps 1–2 (entities and data model,
the shared skeleton) plus the domain boundaries; then one invocation per
domain that reads the skeleton and that domain's statements and writes
steps 3–6 for it. The skeleton is small — entities are a fraction of any
product file — and it is the only cross-domain knowledge the per-domain
passes need. The Splitter then runs once over the merged `tech.md`.
Whether 200 is the right threshold is in section 7.

*Why signatures are fixed here and not later.* Because the Test-writer
needs them to write a test against code that does not exist yet, and
because two implementers in two lots have to agree on a name without
meeting. Fixing them early has a cost — drift, when lot L-03 actually
produces something a little different from what T-17 promised — and
section 6 says how drift is handled and section 7 how it is measured.

### 4.6 Splitter

    Splitter
    Reads:    tech.md
              docs/conventions.md (the layer order, the scaffold lot)
    Does:     1. Run the coverage rule before anything: every P-id in
                 the coverage table has at least one T; every T cites
                 at least one P. A gap here is not the Splitter's to
                 fix — it writes the gap list and stops, and the
                 conductor sends the Designer back with it. (This is
                 also a script; the Splitter re-checks only because it
                 is about to build on the table.)
              2. Lot L-00: on an existing app, the preservation lot —
                 every symbol tech.md marks "modifies", listed by
                 name; no T-ids; its tests come from code_map.md. On a
                 new app, the scaffold lot from conventions.md.
              3. Group T items into lots by the rule: one lot per
                 (layer, entity-or-screen) cell, in layer order,
                 cells within a layer in T-id order. This is a
                 function of tech.md alone.
              4. Size: a lot may name at most the files whose current
                 size plus the T items' estimated size fit one
                 reading — rule: at most 8 files and at most 1500
                 lines of named existing code. A cell that exceeds it
                 is cut at T-id boundaries, in T order, into L-nn-a,
                 L-nn-b.
              5. Order: topological on the "depends:" lines, ties by
                 layer order, then by lowest T-id. Write the order in
                 lots.md with each lot's dependencies.
              6. For every lot write lots/L-nn.md: the T items copied
                 in full (signatures included — the Test-writer and
                 Implementer must not need tech.md); the files it may
                 create and the files it may modify, named; and the
                 acceptance criteria — one per P-id cited by its T
                 items, phrased as an observable: "given …, when …,
                 then …", in the product's words, with the P-id.
              7. For every lot, list the symbols it uses that an
                 earlier lot creates, with the lot number — so the
                 Test-writer knows what to expect to exist.
    Produces: lots.md, lots/L-nn.md
    Runs:     once per feature; again on the Settler's request, for
              the lots after a named one

*Why it reads only `tech.md`.* Reproducibility. The split is the
artefact the brief names ("the same split, the same order"), and an
agent whose output is a function of one file and a fixed rule is the
closest a model comes to a function. Reading `product.md` too would
let it "improve" the design, which is another agent's job and a source
of variance.

*Why acceptance criteria are written here and not by the Designer.*
The criteria are per lot and per P-id, phrased for a reader who has
only the lot. The Designer, holding everything, writes them too
abstractly; the Splitter, copying T items into a lot, is at the exact
altitude the Test-writer will read from.

### 4.7 Test-writer

    Test-writer
    Reads:    lots/L-nn.md
              docs/conventions.md
              code_map.md                     (L-00 only)
              by grep: the current signature of every symbol the lot
              says an earlier lot created
    Does:     — ordinary lot —
              1. For every symbol the lot says exists already, grep it
                 in the code. If the actual signature differs from the
                 one in the lot: write blocked.md, KIND: technical,
                 "L-03 produced X, L-05 expects Y", and stop. Do not
                 adapt silently: the Implementer of this lot would
                 then read a lot that lies.
              2. For every acceptance criterion, write one test,
                 named <P-id>_<what it proves>, in the test file the
                 conventions assign to the source file the T item
                 names. The test calls the signature the lot gives,
                 with the given/when/then of the criterion. Nothing
                 else is tested: no test without a P-id.
              3. Run the test compiler (or the analyzer). The only
                 acceptable errors are unresolved references to the
                 symbols this lot creates. Any other error — a typo,
                 a wrong import, a misuse of the test framework — is
                 the Test-writer's and is fixed now.
              4. Write the list of test names into the lot file under
                 "tests", so the Implementer and the scripts have it.
              — L-00, existing app —
              5. For every "modifies" symbol, read its "today: X"
                 lines in code_map.md and write one test per line,
                 named KEEP_<symbol>_<what>. Run them against the
                 untouched code. Every one must pass. One that fails
                 means the map lied: fix the test to the code — the
                 code is the truth — and add a "map was wrong" note to
                 the lot. Commit the tests.
              — new app L-00 —
              6. Not invoked; the scaffold lot has one trivial test
                 the Implementer writes.
    Produces: test files (failing, except L-00 which passes);
              the "tests" section of lots/L-nn.md
    Runs:     once per lot

*Why before the code, and by a different agent.* Written after, by the
same agent, a test proves that the code does what the code does. Written
before, by a reader who has only the lot, it proves that the code does
what the lot says — and the Implementer inherits an unambiguous target:
make these pass, touch nothing else. It costs one invocation per lot;
it replaces a reviewer that would cost the same and catch less (section
1.4).

*Why it may not see the code beyond signatures.* If it read the
existing implementation, it would test what is there rather than what
is asked; on L-00 that is exactly right, and only there.

### 4.8 Implementer

    Implementer
    Reads:    lots/L-nn.md (with its "tests" section)
              docs/conventions.md
              the test files the lot lists
              the files the lot names as "may modify" — whole
              on retry: the failure log the conductor attaches
    Does:     1. Read the lot and the tests. Read the files it may
                 modify. Do not open anything else; if a file it did
                 not name turns out to be needed, that is a scope
                 fault of the lot — write blocked.md, KIND: technical,
                 naming the file and why, and stop.
              2. Write the code: create the "may create" files, edit
                 the "may modify" files, following the signatures in
                 the lot to the letter. Where the lot leaves a purely
                 internal choice open (a local variable, a private
                 helper), decide it; where it leaves a visible one
                 open (a return value in an unlisted case, an error
                 message), that is a hole in the lot — blocked.md,
                 KIND: technical. Never a product question here: if
                 it looks like one, it still goes out as technical,
                 and the Settler reclassifies (section 6).
              3. Run the analyzer and the lot's tests. Fix. Repeat
                 until green, or until the same test fails twice in a
                 row with the same message after a change meant to
                 fix it — then stop iterating: the cause is not in
                 this context.
              4. Run the full suite once. A failure outside the lot's
                 tests is a regression: fix it if it is in a "may
                 modify" file; otherwise it is a scope fault — stop
                 and report.
              5. Never edit a test file. A test that cannot pass as
                 written — it contradicts the lot, or its expectation
                 is wrong — is reported in blocked.md, KIND: technical,
                 with the test name and the contradiction. The scope
                 script rejects any diff on test files.
              6. On green: commit, message from the conventions, body
                 listing the T-ids and the test names. Report one
                 line: OK <sha>. On stop: report FAIL with the last
                 failing test and its message, or BLOCKED.
    Produces: code, one commit; or blocked.md
    Runs:     once per lot; up to three times in a loop with the
              conductor on failure

*Why it may not edit tests.* Because the tests are the check. The
moment the Implementer can adjust a test, the check measures the
Implementer's opinion. The price is that a genuinely wrong test costs a
Settler round; section 7 says how to know whether that price is too
high.

*Why "the same test fails twice" stops it.* An agent that iterates
against a failure it does not understand converges on the test rather
than on the spec. Two identical failures after two different fixes is
the signal that the misunderstanding is upstream, and a fresh context
with the log is more likely to see it than this one is.

### 4.9 Settler

    Settler
    Reads:    blocked.md
              the one artefact the block names: lots/L-nn.md, or
              tech.md, or product.md — and by grep the code the block
              cites
    Does:     1. Read the block. Classify it, with the product test:
                 would the person see the difference? If yes, rewrite
                 blocked.md with KIND: product, add the question to
                 questions.md with a Default, and stop — the conductor
                 halts and asks her. (A technical block was misfiled;
                 the guarantee failed; this is recorded in state.md
                 as an A-region defect.)
              2. If technical: decide it. Sources, in order: what the
                 code does today (grep); what tech.md already says for
                 a sibling case; the conventions. Write the decision
                 in one line, with its source.
              3. Amend the artefact it lives in: a signature in
                 tech.md, a criterion in the lot, a "may modify" file
                 added. Every amendment is written beside the old
                 text, never over it, with "settled: <date>", so that
                 a re-read shows what changed.
              4. Mark stale: every lot after the amended one whose
                 T items cite the amended T — list them in blocked.md
                 under "reset". The conductor resets their state to
                 pending; their tests, if written, are deleted and
                 rewritten (the Test-writer runs again on them).
              5. If the same lot is blocked a second time after a
                 settlement: do not settle; write KIND: product
                 whatever the content, so a person looks. Two blocks
                 in one place means the lot is not describable, and
                 a third guess is not a design.
    Produces: the Decision line in blocked.md; the amended artefact;
              the reset list; or a question in questions.md
    Runs:     once per block

*Why one agent for all blocks.* A block is a hole in a contract, and
the repair is the same move whatever the contract: decide, write beside,
mark stale. Giving each region its own settler would multiply agents
for one skill.

*Why it reclassifies.* The Implementer is told never to ask a product
question, because in region C nobody can answer one. So it files
everything as technical, and the Settler — the only agent in region C
that reads `product.md` — is where the product test is applied. This is
where the guarantee's failures are *counted*.

---

## 5. Every loop

### 5.1 The questions loop

    Between:            Structurer ⇄ the person, with the Closer as gate
    What sends you in:  questions.md has at least one question whose
                        Answer: line the person has not seen
    What gets you out:  questions.md is empty AND the Closer, run on
                        the current product.md, wrote CLOSED
    What bounds it:     no ceiling in time — it waits for a person.
                        In rounds, the expectation is 2 to 3; the
                        device that makes it converge is the default:
                        a round where she changes nothing closes
                        every open question at once. There is no hard
                        ceiling because a hard ceiling here means
                        starting the expensive part with a hole, which
                        is the one thing the chain is built to prevent.
    Who steps in:       the person, every round

### 5.2 The survey extension

    Between:            Structurer → Surveyor → Structurer
    What sends you in:  the Structurer wrote a "survey gap": a screen or
                        entity the idea names that code_map.md has no
                        file for
    What gets you out:  code_map.md covers the named area, or the
                        Surveyor reports "nothing in the code matches",
                        in which case the Structurer treats the area as
                        new and asks the person as for a new screen
    What bounds it:     one extension run. A second gap after an
                        extension means the idea's vocabulary and the
                        code's do not meet, and grepping again will not
                        make them; the Structurer asks the person
                        ("where in the app is this today?") — a product
                        question she can answer.
    Who steps in:       nobody, for the one run

### 5.3 The coverage loop

    Between:            Designer → coverage script → Designer
    What sends you in:  the script finds a P-id no T cites, or a T
                        citing no P-id
    What gets you out:  both sets empty
    What bounds it:     two runs. The Designer is handed the exact ids;
                        a second miss on the same ids means the
                        statement is not designable as written — that is
                        a Closer failure, and it goes to the person as a
                        product block, not around again.
    Who steps in:       nobody, then the person

### 5.4 The lot loop

    Between:            Test-writer → Implementer → scripts, per lot
    What sends you in:  a lot is pending in lots.md
    What gets you out:  the Implementer reported OK; the scope script
                        finds the diff inside the "may create / may
                        modify" files and no test file touched; the
                        full suite is green; the conductor merged
    What bounds it:     three Implementer invocations per lot (the
                        first, then two fresh ones with the log). Why
                        three and not one: a fresh context does solve a
                        share of failures a stuck one cannot — the
                        log tells it where the first went wrong. Why
                        not more: the third failure is, in this
                        design's view, evidence about the lot, not about
                        the Implementer; a fourth attempt buys tokens
                        for no new information. On the third, the
                        conductor writes blocked.md itself and the
                        Settler reads the log.
    Who steps in:       nobody

### 5.5 The settlement loop

    Between:            any blocked agent → Settler → the agent that
                        resumes (Test-writer or Implementer of the reset
                        lots; Designer and Splitter if tech.md was
                        amended)
    What sends you in:  blocked.md exists with KIND: technical
    What gets you out:  the Settler wrote a Decision and a reset list,
                        and the conductor reset those lots to pending
    What bounds it:     one settlement per lot. The same lot blocking
                        again after settlement goes out as a product
                        block whatever its content (Settler, move 5).
                        This is the ceiling that keeps region C from
                        running alone for days: every autonomous loop
                        in this design has a small integer on it, and
                        the exit on exhaustion is always "a person
                        looks", never "try again".
    Who steps in:       nobody, then the person on the second block

### 5.6 The product-block path (not a loop — a failure)

    Between:            Settler → the person → Structurer → Designer →
                        Splitter → the lots it reset
    What sends you in:  blocked.md with KIND: product
    What gets you out:  the person answered; the Structurer wrote the
                        statement; the Designer re-ran for the affected
                        P-ids; the Splitter re-ran for the affected
                        T-ids; the lots citing them are reset
    What bounds it:     none — a person is in it
    Who steps in:       the person

This path is expensive by construction: it redoes region B for the
affected ids and region C for every lot after the first affected one.
It is not optimised, on purpose. Its cost is the pressure that keeps
region A honest, and its frequency is the single most important
measurement in section 7.

---

## 6. The flow, in one view

```
                       ┌──────────────────────────────────────────────────┐
                       │  A. CLOSING THE PRODUCT      (with the person)   │
                       │                                                  │
   idees.md ──┬──────▶ │  Surveyor ──▶ code_map.md                        │
              │        │      ▲            │                              │
              │        │      │ 5.2 (×1)   ▼                              │
              └──────▶ │  Structurer ─────────▶ product.md + questions.md │
                       │      ▲                       │                   │
                       │      │   answers             ▼                   │
                       │      └──────────── the person  ◀──┐  5.1         │
                       │                                   │              │
                       │  Closer ──▶ questions.md ─────────┘              │
                       │    └──▶ CLOSED                                   │
                       └──────────────────╫───────────────────────────────┘
                                          ‖  product freeze
                       ┌──────────────────╫───────────────────────────────┐
                       │  B. DECIDING THE TECHNIQUE   (once per feature)  │
                       │                                                  │
                       │  Architect ──▶ conventions.md   (once / project) │
                       │                                                  │
                       │  Designer ──▶ tech.md ──▶ [coverage script]      │
                       │      ▲                        │ 5.3 (×2)         │
                       │      └────────────────────────┘                  │
                       │                                                  │
                       │  Splitter ──▶ lots.md, lots/L-nn.md              │
                       └──────────────────╫───────────────────────────────┘
                                          ‖  technical freeze
                       ┌──────────────────╫───────────────────────────────┐
                       │  C. PRODUCING THE CODE        (per lot, in order)│
                       │                                                  │
                       │  L-00  Test-writer ──▶ preservation tests, green │
                       │                        on untouched code         │
                       │                                                  │
                       │  L-nn  Test-writer ──▶ failing tests             │
                       │           │                                      │
                       │           ▼                                      │
                       │        Implementer ──▶ code, green ──▶ [scope]   │
                       │           │  ▲            5.4 (×3)     [suite]   │
                       │           │  └─────── FAIL + log       [merge]   │
                       │           │                                      │
                       │           ▼ BLOCKED                              │
                       │        Settler ──▶ decision, reset ── 5.5 (×1)   │
                       │           │                                      │
                       │           ▼ KIND: product                        │
                       │        ═══ halt: the person ═══  5.6             │
                       └──────────────────────────────────────────────────┘
                                          │
                                          ▼
                        [coverage-by-tests script]  {P} − {P in a passing test}
                        [full suite]                one last time on the merged branch
                        report to the person:       N statements, N proven, 0 missing
```

The conductor is not drawn: it is every arrow.

---

## 7. Why each boundary is where it is — and what breaks if it moves

**Surveyor | Structurer.** The Surveyor copies; the Structurer
interprets. Merged, one agent would read prose and code at once and
write a product statement in technical words ("the RunRepository
returns…") — and the person could no longer read her own product file.
Moved later (survey after the person has answered), the person is asked
what the code already settles: that is the round-trip cost the brief
puts second.

**Structurer | Closer.** Covered in 4.3: it is the author/reader
boundary. Merged, the check is the author re-reading its own text.
Removed, the guarantee has no explicit holder, and the frequency of 5.6
is what will show it.

**Closer | Designer — the product freeze.** The one boundary the brief
fixes itself. Moved earlier (freeze before the Closer), a hole reaches
region B. Moved later (let the Designer ask), the person is drawn into
technical conversation, which she cannot arbitrate, and every later
agent learns that product questions have an outlet.

**Architect | Designer.** Per-project vs per-feature. Merged, the
conventions are re-decided per feature and drift; two features get two
directory layouts.

**Designer | Splitter.** Decide vs. order. Merged, the split becomes a
side effect of design choices made while thinking about the data
model, and two runs give two splits. The Splitter reading only
`tech.md` is what makes "the same split" a property one can test by
re-running it.

**Splitter | Test-writer — the technical freeze.** After it, nobody
repairs `tech.md` in place. Moved earlier (fix signatures per lot,
just-in-time), the Test-writer has nothing to write against, and each
lot re-opens design. Moved later (let the Implementer adjust the
contract), the id chain stops meaning anything, because a T item no
longer says what the code does.

**Test-writer | Implementer.** Proof vs. production, by different
hands. Merged, the tests measure the code's opinion of itself, and the
only check left in region C is the compiler. This boundary is the one
this design would defend hardest, and section 9 names the measure that
would show if it is wrong.

**Implementer | Settler.** Stop vs. decide. Merged, the Implementer
decides what it cannot produce — which is the definition of invention
the brief forbids.

**Agents | Conductor.** Produce vs. dispatch. Merged into the agents
(each calling the next), context inherits, the tail of the run carries
the head, and the run stops being restartable at a lot. Merged into an
intelligent conductor that reads artefacts, the conductor becomes an
eleventh agent with a growing context and opinions about the code.

---

## 8. What was ruled out

**Chaining agents into one another, each inheriting context.** The
brief names it as the design one falls into. Rejected because: context
grows monotonically over a run, so late agents pay for early reading
they do not need; a lot cannot be restarted without replaying the
conversation; and reproducibility depends on the transcript, which is
never the same twice. The file-and-conductor design costs some
re-reading (`conventions.md` is read by four agents), and buys
restartability and fixed inputs.

**One agent for the whole of region A, asking product and technical
questions together.** Rejected because the person cannot tell which
question is hers to answer; she answers technical ones with product
words, and the chain learns nothing usable. The Designer's "decisions
taken" section exists precisely so the technical questions have an
answer that is not hers.

**Asking questions one at a time, in conversation.** Rejected on round
trips: a conversation is n round trips for n questions; a file with
defaults is one round trip for n questions and often zero further.

**Asking no questions: let the chain take every default.** Considered,
because it is the cheapest in round trips. Rejected because the brief
gives the person alone the product arbitration, and a default she never
saw is a decision she did not take. The compromise kept — defaults she
can accept by silence, counted in the header — is as close to zero
round trips as the requirement allows.

**A reviewer agent after each lot.** Rejected in 1.4: it names nothing
the Test-writer plus the scope script do not already catch, and costs
an invocation per lot.

**A final semantic audit of code against product.** Rejected: no
context holds a project, and the id chain gives its mechanical
equivalent at zero tokens.

**Reusing existing documentation of the code (a README, an
architecture file, a previous run's map).** Rejected: documents lie;
the map is regenerated per run from grep, and copies rather than
describes.

**Just-in-time detailing: an agent per lot that writes the lot's
signatures from the actual code state.** Seriously considered — it is
more truthful, because it reads the code as it is after the previous
lots. Rejected because it costs an invocation per lot, reintroduces
design decisions in region C where an error costs everything since,
and makes lot n's signatures a function of lot n−1's code rather than
of `tech.md` — so two runs give two sets. Drift is handled instead by
the Test-writer's signature check (move 1) and one Settler pass, and
its rate is measured (section 9). If the rate is high, this decision
is the one to revisit.

**Letting the Implementer edit tests to fix compile errors.** Rejected
for the reason in 4.8; the compile self-check in the Test-writer (move
3) is meant to make the case rare.

**Unbounded autonomous retry on a lot.** Rejected: after three
attempts, the information is in the lot, not in the Implementer, and
tokens spent past that point buy nothing. Every autonomous loop here
has a small integer on it.

**A lot size fixed in T items.** Rejected in favour of a size in files
and lines of existing code named: what fills an Implementer's context
is what it reads, not how many items it builds.

**One agent per region.** The simplest design: three agents. Rejected
because region A needs the author/reader split and the prose/code
split; region C needs the proof/production split. Each of those is a
distinct check that stacking would lose.

**Running the Surveyor on the whole project.** Rejected: it does not
fit, and the touched area plus one hop is what the feature needs. The
PARTIAL marker and the extension run are what happen when the rule
under-reaches.

---

## 9. What is not settled, and what would settle it

These are decisions taken without being able to say what would prove
them right. Each names the measure. The next context should treat these
as open and the rest as settled.

**9.1 Silence-as-consent on defaults.** The whole round-trip economy
rests on the person accepting defaults by not answering. The risk is
that accepted-by-default statements are where the gaps hide. *What
settles it:* over ten features, for every correction the person asks
for after testing, trace it to its P-id and note whether that statement
was `(answered)`, `(default)`, `(as today)` or `(project default)`. If
defaults dominate the corrections out of proportion to their share of
statements, the defaults must become questions without defaults — and
the round-trip cost goes up.

**9.2 Test-first instead of a reviewer.** Settled on the argument of
1.4, not on evidence. *What settles it:* the count of gaps found by the
person's testing whose cause was "the tests passed but tested the wrong
thing". If that count is non-trivial, a reviewer reading *code against
the lot* — not against the tests — names something distinct after all,
and should be added at the lot boundary.

**9.3 Reproducibility of the split.** The Splitter's rules are meant to
be a function of `tech.md`. *What settles it:* run the Splitter twice
on one `tech.md` and diff `lots.md`. Then run the Designer twice on one
`product.md` and diff `tech.md`. The second diff is expected to be
non-empty in wording and empty in ids, files and signatures; if ids
move, the numbering rule (Designer move 7) is not deterministic enough
and must be tightened. The brief asks for "the same code"; this design
claims same split, same order, same signatures and same test names, and
does not claim byte-identical bodies. Whether that satisfies "the same
code" is for the reader to decide; it is stated so that it is not
mistaken for a claim of full determinism.

**9.4 Whether the Closer earns its invocation.** *What settles it:*
over ten features, count the questions the Closer raised that the
Structurer had not, and how many of those would have surfaced as a
product block in region C. If both counts are near zero, the Closer is
the Structurer's blind spot in theory only, and it can be dropped.

**9.5 Signature drift.** Fixing signatures in `tech.md` before any code
exists assumes lots will honour them. *What settles it:* the number of
Test-writer blocks of the "L-03 produced X, L-05 expects Y" kind per
run. One per run is the price of the design; one per lot means the
just-in-time alternative in section 8 should be reconsidered.

**9.6 Lot size.** 8 files, 1500 lines of named existing code. Numbers
chosen, not measured. *What settles it:* the correlation between a
lot's named-line count and its Implementer attempt count. If attempts
rise with size, lower the ceiling; if they do not, raise it and save
invocations.

**9.7 The preservation lot's cost.** It writes tests for existing
behaviour that a well-tested codebase already has. *What settles it:*
how many `KEEP_` tests fail during the run (regressions caught) versus
how many were written. Zero failures over ten features means the
existing suite was already enough, and L-00 could be restricted to
symbols with no existing test.

**9.8 The whole-application threshold.** 200 statements for splitting
the Designer into skeleton plus per-domain passes. *What settles it:*
the first whole-application run; whether the Designer's single pass
exhausts its context, and whether the skeleton pass leaves the
per-domain passes with a cross-domain question (a sign the skeleton was
too thin).

**9.9 The Implementer's stopping rule.** "The same test fails twice with
the same message" is meant to detect a stuck context. *What settles it:*
among lots that went to a second attempt, the share the fresh attempt
solved. High, the rule is right; low, the failures are upstream and the
second attempt should be skipped in favour of the Settler directly.

**9.10 The conductor as a model.** The design says the conductor should
be replaceable by a script. *What settles it:* try. If every row of the
table in section 2 can be executed by a script reading `state.md` and
the first line of `blocked.md`, the conductor's cost is zero tokens and
the claim holds. Any row that needs a reading is a missing role.

---

*End of the design. Nothing here is an agent; it is what the agents
should be, and why.*
