# Conventions extraction grid

> A derivation test, not a catalogue to copy out. Every rule it holds
> has a trigger, and a trigger the corpus does not satisfy writes
> nothing.

🔴 **Neither document holds a convention.** They describe behaviour,
and a convention is an implementation decision. **What the Architecte
looks for is where two entries could be built differently.**

📌 **Two properties of the technical document do the work**: the
natures — a closed vocabulary of twelve, so a sweep can be exhaustive —
and `Consumes:` — a declared graph, so it can be read mechanically.

**Notation.** `N1`–`N12` are the natures of the technical document, in
order: model, persistence, calculation, transition, external source,
synchronisation, background work, journey, screen, text, access,
lifecycle. `C1`–`C12` are the sections of the conventions file.

🔴 **Never write `§2.5` alone.** It is ambiguous between the two.

---

## How this grid is applied

**R1 — A trigger the corpus does not satisfy writes nothing.** Not even
a rule that reads as common sense. 📌 **This is what stops the grid
from pouring out forty-five rules whatever the project.**

**R2 — A hole the two documents cannot fill writes nothing.** No
default value, no approximation. 🔴 **The entry raises a question
instead.**

**R3 — A rule this grid does not hold is allowed, and marked.** The
most valuable rule of a conventions file is the counter-intuitive one,
and a counter-intuitive rule is by construction absent from a grid
written in advance. 📌 **It cites the entries that motivate it and
carries `off-grid`.** ⚠️ **The mark is not distrust** — it is how the
grid learns which forms it lacks.

**R5 — A list never permits what it leaves out.** A hole asking for an
enumeration carries the rule over *every* case of its class; the list
names those the corpus states, it does not bound the rule. ⚠️ **Writing
*only X and Y* where the corpus happened to name X and Y turns an
incomplete reading into a permission.**

**R4 — The Architecte never amends the grid he applies.** A missing
form, or a form that keeps producing a useless rule, goes back through
a coding agent's lot report.

---

# Part A — Readings

*Facts established once, over the whole corpus. They produce no rule:
they feed the triggers and the holes of part B.*

| ID | Reading | How |
|---|---|---|
| **V1** | Which natures are non-empty, and how many entries each holds | count on the technical document |
| **V2** | The `Consumes:` graph aggregated by nature; whether it is acyclic | read the `Consumes:` lines |
| **V3** | Root entries — those consuming nothing — and entries consumed by more than five others | same |
| **V4** | The lexicon: concept names appearing in more than one entry, and competing forms of one concept | read the product file |
| **V5** | Whether the numbers stated across entries agree with each other | read the product file |
| **V6** | Cross-coverage: one product block ↔ one technical entry, both ways | match the identifiers |
| **V7** | Pairs of entries consuming the same entry with diverging expectations | cross V2 |
| **V8** | Quantities carrying a unit, a scale or an identity, and facts stated as always true | sweep N1 |
| **V9** | Ambient sources each entry reads: clock, randomness, locale, environment | sweep N2, N3, N5, N7 |
| **V10** | Writes declared to happen before a call returns | sweep N2 |

🔴 **V2 is the most valuable reading of this grid.** It turns the
costliest architectural decision — the direction of dependencies — into
a mechanical read of a graph the upstream chain already wrote.

🔴 **V6 runs before everything else.** A defect there is a question,
never work to make up for.

🔴 **A rule is mechanical only where a tool carries it**, and the tool
is one you name in C12. **A formatter is not a rule linter**: a project
can hold one without the other, and calling a rule mechanical on a tool
you did not name makes the `Test` field a wish.

⚠️ **Either the tool is in C12 and the rule is mechanical, or the rule
is a review.** 🔴 **Never mechanical on nothing.**

---

# The shape of the file

*Twelve sections, in this order. The line under each title is what it
settles — it goes in the file. The count in brackets is what to expect,
not a target.*

    # Technical conventions — <project>
    Version <n>, settled <date>.

    ## 1. Governance
    How this file carries authority, and what to do where it is silent.
    [1 to 3]

    ## 2. Verification
    The one command attesting a lot is deliverable, and what is left to
    the formatter.
    [3]

    ## 3. Boundaries
    The files a lot does not touch, and those that need asking first.
    [3 to 4]

    ## 4. Structure and dependency direction
    Where a new file goes, and who may import whom.
    [5 to 8]

    ## 5. Interface contracts
    The shape of what crosses a public boundary — what ties the agent
    writing signatures to the one writing code.
    [6 to 8]

    ## 6. Errors and failure
    How an error is represented, propagated, and what may stop the
    program.
    [6 to 8]

    ## 7. State, resources and effects
    Where mutable state lives, who owns a resource, what survives what,
    on which execution model the code is written.
    [5 to 8]

    ## 8. Configuration and secrets
    Where settings come from, and when they are validated.
    [3]

    ## 9. Diagnostics
    Through which channel the program says what it does, and what never
    appears there.
    [1 to 2]

    ## 10. Tests
    What has to be tested, at which level, and what a test may not do.
    [5 to 7]

    ## 11. Naming, language and comments
    Where names come from, and what a comment may say.
    [2 to 3]

    ## 12. Dependencies and versions
    The non-negotiable versions, the tools the rules need, and the
    right to add one.
    [a table, plus 1 to 2]

🔴 **What never appears in it**: where a rule came from · the reasoning
behind a rule that is not counter-intuitive · any rule a formatter or a
linter already enforces · any product policy.

---

# Part B — Rule entries

*Each entry carries four fields: **question**, **trigger**, **form**
with its holes in `< >`, and **test**.*

---

## C1 — Governance

**G1.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Every rule in this file is MUST unless prefixed SHOULD.
  Where this file and the existing code conflict, this file wins."
- **Test**: none. 🔴 **The only rule of the file with no test**, and
  deliberately: it settles how the file is read, not what the code
  does. **Every other rule is checkable against a file.**

**G1.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "A technical decision this file does not cover is proposed
  as a convention amendment in the lot report, never settled in
  silence."
- **Test**: the lot report carries that field; check it is there.

**G1.3** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "This file carries its version and the date it was
  settled, in its header."
- **Test**: mechanical — header presence, wired into `<cmd verify>`.

---

## C2 — Verification

**G2.1** · *Question*: which single command attests a lot is
deliverable? · *Trigger*: always — the hole is filled from platform
knowledge, not from the documents
- **Form**: "A lot is deliverable only when `<cmd verify>` exits 0. No
  other definition of done."
- **Test**: the command exists and runs on a clean checkout.

**G2.2** · *Question*: does a formatter exist for `<language>`? ·
*Trigger*: one exists
- **Form**: "`<cmd fmt>` is authoritative on layout: where it rewrites
  a file, the rewritten version is the right one. No layout rule is
  argued in this file."
- **Test**: mechanical — `<cmd fmt --check>` failing fails
  `<cmd verify>`.

**G2.3** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Every rule of this file whose test is mechanical is wired
  into `<cmd verify>`. A mechanisable rule left unwired is a defect of
  this file."
- **Test**: review.

---

## C3 — Boundaries

**G3.1** · *Question*: does the project hold generated code? ·
*Trigger*: an entry describes an artefact derived from a source
- **Form**: "Never edit a file carrying the `@generated` header: change
  `<source>`, then run `<cmd gen>`."
- **Test**: mechanical — a diff touching a generated file with no diff
  on its source fails.

**G3.2** · *Question*: does the platform carry a dependency lock file?
· *Trigger*: it does
- **Form**: "Never edit `<lock file>` by hand; go through `<cmd deps>`."
- **Test**: mechanical — a lock diff with no manifest diff fails.

**G3.3** · *Question*: is there durable storage whose structure
evolves? · *Trigger*: an N2 entry describes structured persistence
- **Form**: "No file under `<migrations>/` already dated is modified;
  add one."
- **Test**: mechanical — a diff on a migration older than the lot
  fails.

**G3.4** · *Question*: which paths does a lot never write, and which
does it write only after asking? · *Trigger*: always
- **Form**: "Never: `<what a tool produces — build output, generated
  sources, lock files, dated migrations>`. Ask first: `<the paths a
  change to which reaches beyond the lot>`."
- **Test**: mechanical on the "never" line — a diff touching one of
  those paths fails.

📌 **The "never" line follows from the tools you named in C12**: what a
tool produces, a lot does not write by hand. ⚠️ **The "ask first" line
is your own call**, and it is short or it is noise.

---

## C4 — Structure and dependency direction

**G4.1** · *Question*: which nature consumes which (V2)? · *Trigger*:
V2 is acyclic
- **Form**: "The import graph between top-level modules is a subset of
  the `Consumes:` adjacency aggregated by nature. An import outside
  that graph is an amendment proposed before writing."
- **Test**: mechanical — import check wired into `<cmd verify>`.

**G4.2** · *Question*: which entries consume nothing (V3)? · *Trigger*:
V3 finds at least one root
- **Form**: "`<modules realising the root entries>` import no module of
  this project."
- **Test**: mechanical — import check.

**G4.3** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No module named `utils`, `common`, `helpers`, `misc` or
  `shared`. A module is named for the concept it holds, taken from the
  lexicon."
- **Test**: mechanical — name check.

**G4.4** · *Question*: what is a module's grain? · *Trigger*: always —
the hole is the Architecte's own call, informed by V1 and V3
- **Form**: "One top-level module per `<nature | group of entries>`,
  named: `<the list, in full>`. Every entry of the technical document
  is realised in one of them."
- **Test**: mechanical — every top-level module appears in the list,
  and the reverse.

🔴 **The list is written out in the rule.** A convention that points at
a file the four agents do not read is a convention they cannot follow.

**G4.5** · *Question*: where does data from outside come in? ·
*Trigger*: N5 non-empty
- **Form**: "Every access to an external source is confined to
  `<boundary module>`; no other module imports `<client library>`."
- **Test**: mechanical — import check.

**G4.6** · *Question*: who may import a screen? · *Trigger*: N9
non-empty
- **Form**: "No screen module is imported by a module of another
  nature."
- **Test**: mechanical — import check.

**G4.8** · *Question*: which adapters do two application modules both
need? · *Trigger*: more than one application module, and V1 shows a
nature both of them reach
- **Form**: "An adapter both applications need lives in
  `<the shared module>`, which they depend on and which depends on
  neither. **Identical, not merely similar**: one whose behaviour
  differs between them stays where it is used."
- **Test**: mechanical — no two source files of the same name under two
  application modules.

📌 **Two copies of one adapter is what this prevents** — a correction to
one leaves the other as it was, and nothing says so.

**G4.9** · *Question*: which stored data is searched on, and which
identifies (V8, N2)? · *Trigger*: N2 non-empty
- **Form**: "A field the code searches on carries an index; a field the
  code treats as identifying carries a uniqueness constraint. 🔴 **Every
  such field, whether or not an entry names it** — a lookup a lot
  writes counts as much as one the corpus states."
- **Test**: mechanical — schema check.

⚠️ **A field the code treats as identifying without the store saying so
is an assumption two lots can break.**

**G4.7** · *Question*: does the `Consumes:` graph hold a cycle (V2)? ·
*Trigger*: V2 finds one
- **Form**: none. 🔴 **The entry raises a question naming the entries in
  the cycle, and G4.1 is not written.**
- **Test**: not applicable.

---

## C5 — Interface contracts

**G5.1** · *Question*: which quantities carry a unit, a scale or an
identity (V8)? · *Trigger*: V8 non-empty
- **Form**: "No `<quantity read>` appears as a bare primitive in a
  public signature."
- **Test**: review; mechanical where `<language>` carries nominal
  types.

**G5.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Data crossing a public boundary is immutable; no public
  function mutates its argument."
- **Test**: review.

**G5.3** · *Question*: which operations can block or run long? ·
*Trigger*: N5 or N7 non-empty
- **Form**: "Every public operation that can block accepts
  `<the platform's cancellation mechanism>` in its signature. No
  unbounded wait is reachable from a public boundary."
- **Test**: signature review; mechanisable on the modules concerned.

**G5.4** · *Question*: which data can be missing at display time? ·
*Trigger*: N9 non-empty
- **Form**: "Missing data is carried by `<absence type>`; no module
  invents a default for data that is not there."
- **Test**: review.

**G5.5** · *Question*: what identifies one thing seen from two origins?
· *Trigger*: N6 non-empty
- **Form**: "Every synchronisable entity carries its identity and its
  origin in its type."
- **Test**: review.

---

**G5.8** · *Question*: which operations reach a store, a device or the
network, and what does their signature say about it? · *Trigger*: N2,
N5, N6 or N7 non-empty
- **Form**: "An operation reaching outside the process says so in its
  signature, in whatever way `<the platform>` expresses waiting. 🔴 **It
  moves to the thread that work belongs on, inside its own
  implementation, and never on its caller's word.**"
- **Test**: signature check on the modules concerned.

⚠️ **G7.4 states the model the project presumes.** 🔴 **This one binds
each signature to it** — without it, every lot decides on its own which
call may block.

**G5.9** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "What a signature promises, the body delivers. 🔴 **An
  argument it takes is read**, a handle it is handed is awaited, and a
  value that must outlive the process is written where it does."
- **Test**: review, signature by signature.

📌 **Three ways one signature lies**, and each has been seen: a
parameter ignored, a fire-and-forget call never read, an identity held
only in memory.

⚠️ **A declared failure type that does not carry every failure is a
fourth** — 🔴 **G6.8 holds it**, where the failure comes from leaving
the process.

**G5.6** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No non-null assertion on a value coming from outside the
  function: what can be missing is declared as such, and handled."
- **Test**: mechanical where `<language>` marks such an assertion.

⚠️ **An invariant held in another file is not an invariant** — the call
site cannot see it, and a change to either breaks the assertion.

**G5.7** · *Question*: which quantities are compared against a bound
(V8)? · *Trigger*: V8 holds at least one bounded quantity
- **Form**: "A bound is `<inclusive | exclusive>`, the same way for
  every quantity of one kind. 🔴 **A duration against a window, a
  timeout, a threshold — one convention, all of them**, whether or not
  an entry names each."
- **Test**: review, kind by kind.

📌 **Two rules comparing one quantity two ways is invisible in each of
them, and wrong between them.**

---

## C6 — Errors and failure

**G6.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No empty and no generic catch. An error is handled where
  it is caught or propagated with the calling context — never
  absorbed."
- **Test**: mechanical — most linters carry it.

**G6.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "An error crossing a module boundary is of a type that
  module declares; a dependency's own error never crosses."
- **Test**: review.

**G6.3** · *Question*: which types does an external source hand over,
and where do they stop? · *Trigger*: N5 non-empty
- **Form**: "Data entering through `<boundary module>` is validated
  there and converted to a domain type; no type of the source crosses."
- **Test**: mechanical — import check, plus review.

**G6.8** · *Question*: what reaches outside the process, and what does
it hand back when it fails? · *Trigger*: N2, N5, N6 or N7 non-empty
- **Form**: "Every call leaving the process — a store, a device, the
  network, a deserialisation — returns its failure as a value. 🔴 **What
  it needs before it can run at all** — a permission, a service, a
  client — **is checked before, not caught after.**"
- **Test**: a failure-injection test per boundary.

📌 **G6.3 covers what an external source hands in.** 🔴 **This one
covers everything else that leaves the process** — a store raises, a
deserialisation raises, a platform service may not be there at all.

**G6.4** · *Question*: which transitions are forbidden? · *Trigger*: an
N4 entry names at least one
- **Form**: "A transition N4 does not name is a declared error, never a
  no-op."
- **Test**: review; paired with G10.4.

**G6.5** · *Question*: what does a refusal return? · *Trigger*: N11
non-empty
- **Form**: "An access refusal is a declared error type, never empty
  data, a truncated list or silence."
- **Test**: review.

**G6.6** · *Question*: which writes happen before a call returns (V10)?
· *Trigger*: V10 non-empty
- **Form**: "`<the writes read>` are synchronous; their failure
  propagates. None is deferred."
- **Test**: a failure-injection test per write read.

**G6.7** · *Question*: what happens when two origins diverge? ·
*Trigger*: N6 non-empty **and** an N6 entry states a resolution policy
- **Form**: "A synchronisation conflict is a declared error type, never
  a silent resolution. The policy is `<the one N6 states>`."
- **Test**: review.
- 🔴 **R2 applies**: N6 non-empty with no policy anywhere writes
  nothing and raises a question.

---

## C7 — State, resources and effects

**G7.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No mutable global state outside the entry point.
  Dependencies are passed as arguments, never read from a module
  variable."
- **Test**: mechanical where `<language>` allows; review otherwise.

**G7.2** · *Question*: which resources are acquired and given back? ·
*Trigger*: N2 or N5 non-empty
- **Form**: "Every acquired resource is released in the same scope,
  through `<the platform's mechanism>`."
- **Test**: mechanical where a linter carries it.

**G7.3** · *Question*: which ambient sources do calculations read (V9)?
· *Trigger*: N3 non-empty
- **Form**: "Every N3 entry is realised by a pure function.
  `<the ambient sources read in V9>` are passed as arguments. None of
  them is read inside `<the root modules>`."
- **Test**: mechanical — import and call check.

**G7.4** · *Question*: what execution model does this project presume?
· *Trigger*: always — the hole is the Architecte's call, informed by V1
- **Form**: "Presumed execution model: `<single-threaded | pool of N |
  cooperative async>`. Code departing from it is an amendment proposed
  before writing, carrying its own locking discipline."
- **Test**: review.

**G7.5** · *Question*: who holds the state of a journey? · *Trigger*:
N8 non-empty
- **Form**: "The state of a journey is held by one module:
  `<the pairs, journey by journey>`."
- **Test**: review.

---

**G7.6** · *Question*: what does each screen hold that the system can
take away? · *Trigger*: N9 non-empty
- **Form**: "Every screen's own state says what becomes of it when the
  system rebuilds that screen. 🔴 **What the user has in progress is
  kept, on every screen** — a field being typed, a dialog's contents, a
  selection not confirmed, the path they navigated to get here.
  **Anything else is built again from its source.**"
- **Test**: one test per screen holding state.

⚠️ **A screen is rebuilt far more often than a process dies** — a
rotation, a resize, a theme change.

**G7.7** · *Question*: none, fixed entry · *Trigger*: N9 non-empty
- **Form**: "A screen reads a source once per entry, never once per
  frame. A read that is not remembered is a read on every redraw."
- **Test**: review; mechanical where the platform's own tooling
  carries it.

**G7.8** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Everything opened is closed, and this file says where:
  `<the pairs, opened by / closed by>`. A handle, a session, a scope, a
  registration — each has one place that ends it."
- **Test**: review, pair by pair.

📌 **G7.2 covers what a single scope opens and closes.** ⚠️ **This
covers what outlives a scope** — what one moment opens and another has
to end.

---

## C8 — Configuration and secrets

**G8.1** · *Question*: what must be ready before anything answers? ·
*Trigger*: N12 non-empty
- **Form**: "`<the prerequisites N12 states>` are validated at
  start-up; failure stops immediately, naming the one at fault."
- **Test**: a start-up test per prerequisite.

**G8.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Configuration is read in one module. No environment,
  command-line or configuration-file read anywhere else."
- **Test**: mechanical — call check.

**G8.3** · *Question*: none, fixed entry · *Trigger*: N5 or N11
non-empty
- **Form**: "No secret in clear in the code, the tests or a default
  value; a secret is referred to by name."
- **Test**: mechanical — most scanners carry it.

---

## C9 — Diagnostics

**G9.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No direct write to standard output outside the entry
  point: go through `<the log>`. ERROR is for what needs a human."
- **Test**: mechanical — call check.

**G9.2** · *Question*: which data is attached to a person? · *Trigger*:
an N1 or N11 entry names such data
- **Form**: "No `<field read>` appears in a log message, not even
  truncated."
- **Test**: mechanical — pattern check on log calls.

---

## C10 — Tests

**G10.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Every public function has at least one nominal test and
  one failure test, delivered in the same lot as the code."
- **Test**: review.

**G10.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No test reaches the network, the file system outside a
  temporary directory, or the system clock: time and I/O are
  injected."
- **Test**: mechanical — call check in test sources.

**G10.3** · *Question*: which facts are stated as always true (V8)? ·
*Trigger*: V8 holds at least one
- **Form**: "Each fact read in V8 has a test that attempts to build a
  value violating it and expects a failure."
- **Test**: one test per fact read.

🔴 **A fact is one the corpus states in so many words.** ⚠️ **Not one
you infer from two values sitting near each other** — two numbers in
one entry, in two different units, state nothing about their sum. **R2
applies: what the corpus does not state writes no rule.**

**G10.4** · *Question*: G6.4 named the forbidden transitions — which
of them has a test? · *Trigger*: an N4 entry names at least one
- **Form**: "Each forbidden transition N4 names has its own test."
- **Test**: one test per transition.

**G10.5** · *Question*: what bounds do the calculations state? ·
*Trigger*: N3 non-empty
- **Form**: "Each N3 entry has a test on the bounds its product block
  states."
- **Test**: one test per entry.

**G10.6** · *Question*: at what grain do two origins compare? ·
*Trigger*: N6 non-empty
- **Form**: "The comparison grain N6 states has a test confronting two
  origins on `<the grain>`."
- **Test**: one test.

**G10.7** · *Question*: G6.6 named the writes that precede a return —
which of them has an interruption test? · *Trigger*: V10 non-empty
- **Form**: "Each write read in V10 has a test interrupting between the
  write and the return."
- **Test**: one test per write.

---

## C11 — Naming, language and comments

**G11.1** · *Question*: what is the lexicon (V4)? · *Trigger*: always
- **Form**: "The code's vocabulary is `<the lexicon>`. No synonym, no
  abbreviation outside it. A concept the lexicon does not hold is an
  amendment proposed before writing."
- **Test**: review.

**G11.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Identifiers, comments, error messages and documentation in
  English. Every exported symbol carries one line saying what it
  guarantees and when it fails. No comment paraphrases the line below
  it."
- **Test**: review; partly mechanical.

**G11.3** · *Question*: are user-facing strings keys or literals? ·
*Trigger*: N10 non-empty
- **Form**: "No user-facing string is a literal in the code: a key and
  a table, the key being the one its N10 entry names."
- **Test**: mechanical — literal check outside the resource files.

---

## C12 — Dependencies and versions

**G12.1** · *Question*: which language and which core dependencies, at
which versions? · *Trigger*: always — filled from platform knowledge
- **Form**: a table: `<language X.Y>`, `<framework A.B>`, one line
  each. **Non-negotiable within a lot.**
- **Test**: mechanical — version check wired into `<cmd verify>`.

**G12.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No new dependency inside a lot. An addition is an
  amendment proposed before writing, and delivered on its own."
- **Test**: mechanical — a manifest diff inside a lot fails.

**G12.3** · *Question*: which tools do the rules of this file need? ·
*Trigger*: a rule written here calls for one
- **Form**: the table of G12.1 carries them, each with the rules it
  serves.
- **Test**: mechanical — every tool named in a `Test` field appears in
  the table.

🔴 **A rule that demands tests, on a project naming no test framework,
is a rule the first lot cannot follow.** ⚠️ **And G12.2 forbids adding
one inside a lot** — the tool is named here, or the rule is not
written.

🔴 **A tool named here carries the rules it is named for, and no
others.** ⚠️ **A rule whose exact check no named tool performs is a
review**, however close a named tool sounds: a formatter is not a rule
linter, and a rule linter does not read a database schema.

**G12.4** · *Question*: does the corpus presume network access? ·
*Trigger*: N5 **empty**
- **Form**: "No network dependency and no network call."
- **Test**: mechanical — import check.

📌 **The only entry a trigger fires on an *empty* nature.** An absence
is a fact, and a fact worth writing down.

---

## What the volume should be

**Sixty-three entries, of which eight to twelve do not fire on a given
project.** 📌 **Fifty to fifty-five rules written.**

⚠️ **Two places where the budget strains:**

📌 **C11 reaches three dense rules** when N10 is non-empty. **If G11.2
is fully carried by the linter, it moves to C2.**

📌 **C6 and C10 are paired** — G6.4 with G10.4, G6.6 with G10.7. 🔴
**Each pair reads one fact of the corpus and writes two different
rules**: what the code does with it, and what proves the code does it.
**They are answered once and written twice.**

⚠️ **If the budget presses, keep the test rule and drop the error
rule**: the test is verifiable, the error rule only reviewable.
