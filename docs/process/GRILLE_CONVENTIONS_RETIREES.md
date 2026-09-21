# Withdrawn grid entries — open doors

> 🔴 **Thirty-four of the seventy Part B entries, withdrawn.** 📌 **Kept
> here with their full text, to be able to put them back — not to
> remember them.**

## Why they were withdrawn

📌 **Each of the seventy entries was measured**: its *Question* was read
alone, an answer written cold, and only then the *Form* compared to it.

| Class | Count | What it means |
|---|---|---|
| **Open door** | **34** | 🔴 **The cold answer met the Form** — one reasonable choice exists, and the entry prescribes what would have been done anyway |
| **Correction** | 24 | 📌 **The cold answer differed, and the Form was right** — the entry catches a real mistake |
| **Arbitration** | 12 | 📌 **Two defensible choices** — without the entry, two lots would decide differently |

⚠️ **The thirty-four probably come from three historical causes, all
corrected since** — 🔴 **a technical document disconnected from the
product, a Détailleur that missed things, and Sonnet where Opus was
needed.** 📌 **That can only be proved by withdrawing them and
watching.**

## When to put one back

🔴 **A lot decides something this entry would have settled, and decides
it wrong.** 📌 **That is the signal** — ⚠️ **not a reading that finds the
entry sensible**: every one of them is sensible, that is what made it
an open door.

📌 **Put back the entry's text as it stands below**, in its section.

---

**G1.3** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "This file carries its version and the date it was
  settled, in its header."
- **Test**: mechanical — header presence, wired into `<cmd verify>`.

---

## C2 — Verification

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

**G4.2** · *Question*: which entries consume nothing (V3)? · *Trigger*:
V3 finds at least one root
- **Form**: "A module realising an entry that consumes nothing depends
  on no module of this project. 🔴 **Every such module**, whatever it is
  named."
- **Test**: mechanical — `<the dependency check>`.

⚠️ **A module realising both a root entry and a consuming one breaks
this rule by construction** — say so as a question rather than naming
only the modules that happen to obey.

**G4.3** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No module named `utils`, `common`, `helpers`, `misc` or
  `shared`. A module is named for the concept it holds, taken from the
  lexicon."
- **Test**: mechanical — name check.

**G4.5** · *Question*: where does the program meet other systems? ·
*Trigger*: N5 non-empty
- **Form**: "Every exchange with another system is confined to
  `<boundary module>`; no other module depends on `<client library>`."
- **Test**: mechanical — `<the dependency check>`.

**G4.6** · *Question*: who may depend on a presentation module? ·
*Trigger*: N7 non-empty
- **Form**: "No presentation module is depended on by a module of
  another nature."
- **Test**: mechanical — `<the dependency check>`.

**G4.7** · *Question*: which adapters do two application modules both
need? · *Trigger*: more than one application module, and V1 shows a
nature both of them reach
- **Form**: "**Any** adapter both applications need lives in a shared
  module they both depend on and that depends on neither — **whatever
  it adapts**. 🔴 **If no shared module suits what it adapts, one is
  added for it**, named for what it holds."

  🔴 **"Identical, not merely similar: one whose behaviour differs
  between them stays where it is used."**
- **Test**: mechanical — no two source files of the same name under two
  application modules.

📌 **Two copies of one adapter is what this prevents** — a correction to
one leaves the other as it was, and nothing says so.

**G4.8** · *Question*: which stored data is searched on, and which
identifies (V8, N2)? · *Trigger*: N2 non-empty
- **Form**: "A field the code searches on carries an index; a field the
  code treats as identifying carries a uniqueness constraint. 🔴 **Every
  such field, whether or not an entry names it** — a lookup a lot
  writes counts as much as one the corpus states."
- **Test**: mechanical — schema check.

⚠️ **A field the code treats as identifying without the store saying so
is an assumption two lots can break.**

**G4.9** · *Question*: does the `Consumes:` graph hold a cycle (V2)? ·
*Trigger*: V2 finds one
- **Form**: none. 🔴 **The entry raises a question naming the entries in
  the cycle, and G4.1 is not written.**
- **Test**: not applicable.

---

## C5 — Interface contracts

**G5.2** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "Data crossing a public boundary is immutable; no public
  function mutates its argument."
- **Test**: review.

**G5.3** · *Question*: which operations can block or run long? ·
*Trigger*: N5 non-empty, or an entry runs with nobody waiting on it
- **Form**: "Every public operation that can block accepts
  `<the platform's cancellation mechanism>` in its signature. No
  unbounded wait is reachable from a public boundary."
- **Test**: signature review; mechanisable on the modules concerned.

**G5.4** · *Question*: which data can be missing at display time? ·
*Trigger*: N7 non-empty
- **Form**: "Missing data is carried by `<absence type>`; no module
  invents a default for data that is not there."
- **Test**: review.

**G5.9** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "What a signature promises, the body delivers. 🔴 **An
  argument it takes is read**, a handle it is handed or hands back is
  awaited, and a value that must outlive the process is written where
  it does."
- **Test**: review, signature by signature.

📌 **Three ways one signature lies**, and each has been seen: a
parameter ignored, a fire-and-forget call never read, an identity held
only in memory.

⚠️ **A declared failure type that does not carry every failure is a
fourth** — 🔴 **G6.4 holds it**, where the failure comes from leaving
the process.

**G5.10** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No non-null assertion on a value coming from outside the
  function: what can be missing is declared as such, and handled."
- **Test**: mechanical where `<language>` marks such an assertion.

⚠️ **An invariant held in another file is not an invariant** — the call
site cannot see it, and a change to either breaks the assertion.

**G6.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No handler that swallows a failure, and none that catches
  every kind at once. A failure is handled where it is caught or
  propagated with the calling context — never absorbed."
- **Test**: mechanical — most linters carry it.

**G6.3** · *Question*: what types enter from outside the process, and
where do they stop? · *Trigger*: N5 or N6 non-empty
- **Form**: "🔴 **Data entering from anywhere outside the process** — a
  source, a payload from another device, a store — is validated at the
  module that receives it and converted to a domain type; no type of
  the outside crosses."
- **Test**: mechanical — `<the dependency check>`, plus review.

⚠️ **A payload from the paired device is data from outside**, as much
as a file or a service is.

**G6.5** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "A caller that receives a failure acts on it. 🔴 **It is
  handled, propagated, or reported — never dropped**, and never left to
  a value that reads as success."
- **Test**: mechanical where `<language>` marks an unused result;
  review otherwise.

⚠️ **G6.4 says what a boundary hands back.** 🔴 **This says what the
one who receives it does** — the two are answered separately, and the
second is the one nothing else covers.

**G7.1** · *Question*: none, fixed entry · *Trigger*: always
- **Form**: "No mutable global state outside the entry point.
  Dependencies are passed as arguments, never read from a module
  variable."
- **Test**: mechanical where `<language>` allows; review otherwise.

**G7.2** · *Question*: which objects does the platform construct
rather than the code? · *Trigger*: N7 or N8 non-empty, or an entry
runs with nobody waiting on it
- **Form**: "🔴 **What the platform constructs receives its dependencies
  through `<the mechanism>`** — never by reading them from a module
  variable, never by building them itself."

  🔴 **"A dependency the mechanism cannot supply is a build failure,
  never a run-time one."**
- **Test**: review, one such object at a time.

📌 **G7.1 forbids the wrong way; this names the right one.** ⚠️ **A
screen, a service, an activity is instantiated by the system** — no
caller passes it anything, and without a mechanism named here every lot
invents its own.

🔴 **Name it for what it is** — a library and its version, not a
principle — **and put it in the table of G12.1.** ⚠️ **G12.2 forbids a
lot from adding a dependency**, so a mechanism not named here leaves
the first lot unable to build anything the platform constructs.

**G7.3** · *Question*: which resources are acquired and given back? ·
*Trigger*: N2 or N5 non-empty
- **Form**: "Every acquired resource is released in the same scope,
  through `<the platform's mechanism>`."
- **Test**: mechanical where a linter carries it.

**G7.7** · *Question*: who holds the state of a path across several
views? · *Trigger*: an N7 entry says what moves the user from one view
to the next
- **Form**: "The state of a path across several views is held by one
  module, and this file says which. 🔴 **Every such path**, whether or
  not an entry names it as one."
- **Test**: review, path by path.

---

**G7.8** · *Question*: what does each screen hold that the system can
take away? · *Trigger*: N7 non-empty
- **Form**: "Every screen keeps what the user has in progress across a
  system rebuild. 🔴 **Anything they have entered, opened or selected
  and not yet confirmed.**"
- **Test**: one test per screen holding state.

⚠️ **A screen is rebuilt far more often than a process dies** — a
rotation, a resize, a theme change.

**G8.3** · *Question*: none, fixed entry · *Trigger*: N5 or N8
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

**G10.4** · *Question*: G6.6 named the forbidden transitions — which
of them has a test? · *Trigger*: an N4 entry names at least one
- **Form**: "Each forbidden transition N4 names has its own test."
- **Test**: one test per transition.

**G10.5** · *Question*: what bounds do the calculations state? ·
*Trigger*: N3 non-empty
- **Form**: "Each N3 entry has a test on the bounds its product block
  states."
- **Test**: one test per entry.

**G11.3** · *Question*: are user-facing strings keys or literals? ·
*Trigger*: N9 non-empty
- **Form**: "No user-facing string is a literal in the code: a key and
  a table."

  🔴 **"The key is the one its own N9 entry names — every N9 entry,
  not one of them."**
- **Test**: mechanical — literal check outside the resource files.

---

## C12 — Dependencies and versions

**G12.1** · *Question*: which language and which core dependencies, at
which versions? · *Trigger*: always — filled from platform knowledge
- **Form**: a table: `<language X.Y>`, `<framework A.B>`, one line
  each. **Non-negotiable within a lot.**
- **Test**: mechanical — version check wired into `<cmd verify>`.
