# Verdict — the chain that beats both

This document compares the chain designed in `proposition.md` with the
chain running in production — eleven agents, three grids — and ends
with a single chain. It was written against the three measures of
`02_comparaison.md`: robustness first, round trips second, tokens
third, the first prevailing.

One asymmetry governs every verdict below. **Our chain has run**: it
has cut real splits, coded real lots, and several of its rules carry
the mark of something seen — *"seen three times"*, *"measured over ten
steps"*, *"each has been seen"*. **The proposal has not run**: it is
an argument. Where the two disagree and ours holds a rule that was
learned from a failure, the rule wins over the argument unless the
argument names a gap the rule cannot close. Where a measure cannot be
observed on the proposal, it is estimated, and the estimate is marked
as one. Section 9 lists every place that happened.

The outcome is not a third design. **It is our chain, with six devices
borrowed from the proposal, one weakness the proposal's own reasoning
exposed in ours, and everything else kept for a reason stated.**

---

## 0. The spine of the final chain, in five sentences

1. **The person answers product questions, and only product questions,
   in files, with a proposed answer under each** — she writes the
   answer, even when it is *ok*; her silence closes nothing. Every
   answer, whichever agent asked, enters through one door: the product
   file.
2. **Every document downstream of the product file is closed by a
   context that did not write it.** The product file by the Analyste's
   grid invocation and the Convertisseur; the technical document by a
   fresh Convertisseur invocation; the split by the Vérificateur; the
   code by the Relecteur; the whole by the Contrôleur.
3. **Signatures are written per block, against the code as it is after
   the previous block** — never for a whole feature before any code
   exists. The block is the unit that makes this affordable.
4. **A lot is cut with the code in view** — its callers, what fulfils
   its contracts, the pieces that reach outside the program, what
   listens for its triggers — because a lot cut from the document alone
   compiles into dead code, and that was seen.
5. **Whatever a script can check, a script checks, at zero tokens,
   before an agent reads** — the id chain before the split, the diff's
   scope after each lot. The scripts filter; they replace no reader.

---

## 1. Why this split into roles

### 1.1 What both designs derive from — and the fourth fact

Both chains start from the same three facts of the brief: an agent's
context is finite; the person arbitrates product and nothing else; an
error found late costs everything since. The proposal derives nine
roles and a conductor from them. Ours derives eleven.

Ours also carries a fourth fact the proposal could not have: **what a
check has to catch is known only after it missed something.** The
Vérificateur's seven kinds of defect, the Cadreur's grep of callers and
fulfilments, the Relecteur's fifth point (*what the lot writes and
never reads*), the Détailleur's *"a type nobody declares is a
blocker"*, the Réalisateur's *"per coherent unit, never per edit"* —
each of these is a rule that exists because its absence produced a
gap. The proposal's section 1.4 drops the reviewer on the argument
that it *names nothing distinct*; the Relecteur's checklist is the
list of what turned out to be distinct.

So the roles of the final chain are ours. What changes is not a role
but a device, in six places, and one invocation added where the
proposal's own argument found a hole in ours.

### 1.2 The roles, and the test that created each

| Region | Role | Created by | What it holds at once |
|---|---|---|---|
| A — closing the product | **Analyste** | nature: reads prose, writes blocks; a second invocation reads the blocks without the prose | the idea or the answers; the product file's moved blocks + the grid |
| B — deciding the technique | **Convertisseur** | nature: reads product, writes technical; a third invocation reads its own output as a stranger | the product file whole, then the technical document whole |
| B | **Architecte** | runs once per *project*; the only reader of both documents whole against a 70-entry grid | product file + technical document + conventions grid |
| split | **Cadreur** | reads the technical document whole *and* the code by grep — the one place where the document meets the code before any signature exists | the document, the conventions, the symbol inventory |
| split | **Vérificateur** | fresh reader of the split; must be able to fail it without being able to fix it | the lot list + the cited entries |
| C — producing the code | **Détailleur** | repeats per block; reads the real code after the previous block | one block's entries + the state document's traps + greps |
| C | **Réalisateur** | repeats per lot | one sheet + the files it touches |
| C | **Relecteur** | fresh reader of the lot; judges interpretation, never execution | one sheet + one report + one diff |
| closure | **Contrôleur** | reads no code, no technical document — product against sheets, sentence by sentence | one group of blocks + their sheets |
| cross-cutting | **Arbitre** | handles what every other agent stops on | the blocking files of one round + the corpus by grep |
| correction | **Diagnostiqueur** | the only upstream agent that reads code; one gap per context | one gap + the code by grep |

And what is not an agent: **the orchestrator**, driving numbered
commands, reading one status line per artefact, and running the
scripts.

Two agents outside the comparison — the Fusionneur, which merges a
finished feature into the global product document, and the Extracteur,
which builds that global from a taken-over codebase — are not among
the eleven this phase names and were not examined. The final chain
keeps them where they are; the flow in section 6 shows where they
connect.

### 1.3 What was taken from the proposal, and what was not

**Taken** — each is justified in section 8:

- A `Default:` line under every question (D1) — without
  silence-as-consent.
- One door for every product answer: the product file, whoever asked
  (D2).
- A mechanical id check before the split, and a mechanical scope check
  on each lot's diff (D6, D7).
- A stopping rule inside the Réalisateur's own analyse-and-test loop
  (D9).
- A decision that names the sheets it makes stale, and a ceiling of one
  settlement per lot (D10).
- The build files as an input of the Architecte on a taken-over
  codebase, and a preservation lot in the first split on such a
  codebase (D11, D12).

**Not taken**, each with the divergence that says why:

- Signatures fixed for the whole feature before any code (D3).
- A Splitter that reads the technical document alone (D4).
- Test-first by a separate agent instead of a reviewer (D5).
- A code map regenerated from grep at every run in place of the global
  product document and the state document (D12).
- A settler that amends the artefacts itself (D10).
- Statement-level identifiers as the unit of coverage (D7).

### 1.4 The four boundaries ours has and the proposal lacks

**Convertisseur | Architecte.** Translation vs. conventions. The
proposal's Designer does both, plus signatures, in one context. Merged,
the technical choices — which store, which threading model, which
module may import which — are re-decided per feature and drift; the
Architecte runs once per project precisely so two features get one
layout. The conventions grid's V2 reading (the `Consumes:` graph
turned into an import rule) is possible only because the technical
document exists before the conventions are written, which the
Designer's single pass forbids.

**Cadreur | Vérificateur.** Cut vs. check. The proposal checks its split
by a script on ids. The Vérificateur's *unbuilt surface* — a symbol
produced by one lot and needed by another, where one writes and the
other reads — is invisible to a name comparison; so is *a caller no
lot declares*, which *"shows when the module stops compiling, in a lot
that touches neither end"*. That sentence is an observation, not a
design.

**Détailleur | Réalisateur.** Signatures vs. code, per block. The
proposal puts the signatures in `tech.md` and admits (9.5) that drift
is the price. Ours pays one Détailleur per block and gets signatures
that were grepped against the code the previous block left.

**Réalisateur | Relecteur.** Production vs. judgement. The proposal
replaces this with Test-writer | Implementer. Section 8, D5, says why
the reviewer names four things the tests cannot.

---

## 2. What invokes — the orchestrator and the scripts

The orchestrator is ours: a top-level session following numbered
command files, each command holding its own rules. It dispatches, it
merges, it never opens a document beyond the line that tells it where
the run stands — a verdict's `## Status`, a sequence's `## Defects`,
a blocking file's `## Decision`, the presence of a questions file. The
proposal's one-page ledger is the same idea in one file; ours keeps the
state where the artefacts are, and finds it by glob and grep. No
measure moves between the two shapes; one does move on what the agents
hand back (D14): **every agent returns one line to the orchestrator**
— what it wrote, by path, and its status word. Over fifty lots, the
orchestrator's context is what those returns add up to.

**Two scripts**, both new, both from the proposal's principle that a
set comparison costs no tokens:

| Script | When | What it checks |
|---|---|---|
| **id coverage** | after the Convertisseur, before the Cadreur; again after the Cadreur | every block of the product file has a line in `tracabilite.md`; every entry of the technical document is cited by a lot's `Anchor` or declared under `## Entries with no lot` |
| **scope** | after each lot is committed, before the Relecteur reads | the lot's diff touches only the files its report declares, plus the state document; anything else is a FAIL the Relecteur does not have to read for |

Neither script judges content. A dash in `tracabilite.md` is a
Convertisseur decision the fresh closing invocation reads; a file
declared and wrongly touched is the Relecteur's. The scripts remove the
gross case from what a model reads, nothing more.

---

## 3. The files

All in the feature folder unless noted. Named once; the cards refer to
them.

| File | Written by | Read by | Nature |
|---|---|---|---|
| `idees.md` | the person | Analyste (first invocation only) | free prose, French |
| `desc-produit.md` | Analyste | Analyste, Convertisseur, Architecte, Contrôleur | blocks `Bn`, each one trigger and one output, a nature among twelve, `NEW` while unclosed |
| `docs/PRODUIT_GLOBAL.md` | Fusionneur, Extracteur | Analyste (by index) | what the application does today, in product words |
| `questions-<agent>-NN.md` | Analyste, Convertisseur, Architecte | the person, then the Analyste | one entry per question: block, question, **`Default:`**, `Answer:` |
| `spec-technique.md` | Convertisseur | Convertisseur (closing), Architecte, Cadreur (whole), Vérificateur and Détailleur (entries) | twelve sections, entries `§n.m`, `<<ASSUMED` marks |
| `tracabilite.md` | Convertisseur | the id script, Architecte, Convertisseur (closing) | one line per block: the entries carrying its rules |
| `docs/TECHNICAL_CONVENTIONS.md` | Architecte | Cadreur, Détailleur, Réalisateur, Relecteur, Arbitre | how to code here; twelve numbered sections |
| `couverture.md` | Architecte | the person, once | entry → rule, rule → test kind |
| `architecte/*.md` | Cadreur, Détailleur, Réalisateur | Architecte (requests) | a missing rule, with an empty `## Verdict` |
| `code/decoupage.md` | Cadreur | Vérificateur, Détailleur, Arbitre | the symbol inventory, then the lots: `Anchor`, `Needs`, `Produces`, `Modifies` |
| `code/sequence.md` | Vérificateur | the orchestrator, Cadreur (defects), Détailleur | `## Order`, `## Blocks`, `## Defects` |
| `code/<lot>/fiche-executable.md` | Détailleur | Réalisateur, Relecteur, Contrôleur | signatures, acceptance criteria, dependencies, conventions named, requests |
| `code/<lot>/compte-rendu.md` | Réalisateur | Relecteur, the scope script, Détailleur (by grep) | symbols created or modified, build, state, requests, **files touched** |
| `code/<lot>/verdict.md` | Relecteur | the orchestrator, Réalisateur (on FAIL), Détailleur (affected lots) | status word, cause, symbol divergences with the lots they affect |
| `code/controle/*.md`, `code/rapport-controle.md` | Contrôleur | the person | intentions found, missing, doubtful |
| `docs/CURRENT_TECHNICAL_STATE.md` | Réalisateur | Détailleur, Réalisateur (two sections), Cadreur | what exists, traps, dead state |
| `blocked_<agent>.md` | any agent that stops | Arbitre, the person, the agent that resumes | four headings; `## Decision` empty until settled; **plus the sheets the decision makes stale** |
| `bugfix-NN/bug-list.md`, `investigation/*.md`, `desc-bug.md` | the person, Diagnostiqueur | Diagnostiqueur, Cadreur, Analyste (bug-fix pass) | the correction cycle's inputs and technical document |
| the code and tests | Réalisateur | everyone downstream, by grep | the truth |

Three things are new against production: the `Default:` line, the
files-touched field of the report, and the stale-sheets list in a
settled blocking file.

---

## 4. One card per agent

Cards stay at the proposal's level: what the agent reads, its moves in
order at the macro level, what it produces, how often it runs. Where a
card changes against the agent file in production, the change is
marked **(changed)** and points at its divergence.

### 4.1 Analyste

    Analyste
    Reads:    idees.md                          (first invocation only)
              the latest questions file, whoever wrote it
              the global, by its index
              desc-produit.md, by block, never whole
              the product grid                  (grid invocation only)
              every bugfix-*/bug-list.md        (bug-fix pass only)
    Does:     1. Structure: cut what the person wrote — the idea, or
                 her answers — into blocks of one trigger and one
                 output, filed under a title the global already has or
                 a new one, each block with its nature and NEW.
              2. Close, in a fresh invocation that has not seen the
                 prose or the questions: run the product grid on every
                 block that moved, write the next questions file. Each
                 entry carries the block, the question, a Default line
                 phrased as the statement the chain would take, and an
                 empty Answer line.                          (changed, D1)
              3. Integrate every answer that comes back — the person's
                 answers to any agent's questions, the Convertisseur's
                 and the Architecte's included — by the same moves as
                 an answer to its own.                        (changed, D2)
              4. After a feature's correction cycles: read their bug
                 lists and carry every product decision they settled
                 back into the product file.
    Produces: desc-produit.md, questions-analyste-NN.md
    Runs:     1 and 2 once per round, in a loop with the person, until
              a questions file comes out empty; 1 again for every
              downstream questions file answered; 4 once per feature

*Why the second invocation is the Closer.* The proposal's Closer reads
`product.md` without the prose so that it sees what every later agent
will see. The Analyste's grid invocation does exactly that: it never
opens `idees.md`, and it may only grep the questions file *because a
question it has read it cannot unsee*. Same check, one agent, two
contexts.

### 4.2 Convertisseur

    Convertisseur
    Reads:    desc-produit.md, whole
              the technical closure grid, part 1 then part 2
              spec-technique.md                 (targeted update; closing)
              tracabilite.md                    (closing)
    Does:     1. Close the product file: nature sentence by sentence,
                 consistency block against block. Questions, no entry
                 written. Delete any technical document that predates
                 this closure.
              2. Produce the technical document: twelve sections,
                 numbered entries, one rule or one table each, each
                 traceable to a product sentence; mark what had to be
                 assumed with the question that will settle it; write
                 the traceability file.
              3. Close the technical document, in a fresh invocation
                 that did not write it: the eight part-2 closures —
                 nothing dropped, agreement between entries, declared
                 links, completeness, what a nature owes and the rest —
                 read against the product file. Questions, or closed.
                                                              (changed, D8)
    Produces: questions-convertisseur-NN.md, spec-technique.md,
              tracabilite.md
    Runs:     1 once per round until empty; 2 once, then targeted per
              round of answers; 3 once per full production

*Why a third invocation and not a third agent.* The check is the
author/reader split the proposal argues for its Closer and applies
nowhere on its technical document. The closures already exist and are
already the Convertisseur's; what moves is the context they run in.

### 4.3 Architecte

    Architecte
    Reads:    desc-produit.md and spec-technique.md, whole
              tracabilite.md
              the conventions grid, whole
              on a taken-over codebase: the build files, and them
              alone — the manifest, the dependency file, the test
              configuration                                  (changed, D11)
              the conventions in force              (invocations 2, 3)
              architecte/*.md                       (invocation 3)
              the web and the build files           (invocation 3)
    Does:     1. Derive: establish the grid's readings over both
                 documents, walk its entries, write the rule each one
                 fires, write the off-grid rules the corpus states,
                 write the coverage file. Raise every coverage and
                 conjunction gap as a question; settle every precision
                 gap yourself.
              2. Integrate: once the answers have entered the product
                 file and the technical document, re-read the two
                 documents where they changed and write the rules they
                 now derive.                                 (changed, D2)
              3. Settle requests: for each missing rule a downstream
                 agent wrote, look it up, decide whether it is a
                 convention at all, write it or say where it belongs.
    Produces: docs/TECHNICAL_CONVENTIONS.md, couverture.md,
              questions-architecte-NN.md, each request's verdict
    Runs:     1 once per project; 2 once if 1 asked; 3 once per round
              of requests, at any point of a cycle

*Why once per project.* Both chains agree, for the same reason:
conventions that change per feature are not conventions. The request
path is what ours has and the proposal lacks — a way for a convention
to be corrected mid-run, by the agent that owns the file, without a
person.

### 4.4 Diagnostiqueur

    Diagnostiqueur
    Reads:    one gap, in the prompt                    (investigation)
              the conventions, the state document, the code by grep
              every investigation report, bug-list.md    (assembly)
              the technical closure grid, three closures  (assembly)
    Does:     1. Investigate one gap: turn it into search terms, grep,
                 widen at most three times; give a verdict — missing,
                 wrong, set aside; name the bearer and the trigger;
                 confirm what the fix needs and read each caller
                 against the new mechanism; write the report.
              2. Assemble: one report per listed gap or block; give
                 each confirmed gap a nature and an entry in the
                 technical document's shape, bearer first; run the
                 three closures that apply to a bug file.
    Produces: investigation/<id>.md, desc-bug.md
    Runs:     1 once per gap, in parallel; 2 once per correction cycle

*Why it exists at all.* The proposal has no correction cycle. Its
section 9 measures itself by *"corrections the person asks for after
testing"* and designs no path for them. Ours turns an observed gap into
a technical document the same split and code chain consumes, and the
Analyste's fourth move carries what the correction settled back into
the product file, so the global stays true.

### 4.5 Cadreur

    Cadreur
    Reads:    spec-technique.md or desc-bug.md, whole, preamble first
              docs/TECHNICAL_CONVENTIONS.md, whole
              the code, by grep, in the folders the conventions name
              code/sequence.md ## Defects                 (take-back)
    Does:     1. Stop on any assumption mark. Read the document whole.
              2. Inventory every symbol the entries name, with
                 everything asked of it, grepped against what it
                 carries today — the gap is what has to be built.
              3. Group entries into lots, one per thing the code will
                 build, never across two sections; on a bug-fix cycle,
                 by bearer.
              4. For each lot declare what it needs, produces,
                 modifies; grep the callers and fulfilments of every
                 modified contract; cut a lot for every piece a rule
                 needs to reach outside the program; name what must be
                 declared outside the code; find the symbol that
                 listens for every trigger.
              5. On a taken-over codebase, in the first split: declare
                 a preservation lot — one criterion per behaviour the
                 global describes for every symbol the split modifies,
                 its tests to pass on the untouched code before any
                 other lot is coded.                         (changed, D12)
              6. Anchor each lot on the entries it builds from;
                 declare every entry no lot cites, with its reason.
              7. On a take-back, fix only the lots the defects name.
    Produces: code/decoupage.md, architecte/cadreur.md when a
              convention is missing
    Runs:     once per cycle, plus once per round of defects, three
              rounds at most

*Why it greps.* The proposal's Splitter reads `tech.md` alone, for
reproducibility. Section 8, D4, says what that costs: every caller, every
fulfilment, every listener the Splitter cannot see becomes a scope
fault at implementation, a block, a settlement round.

### 4.6 Vérificateur

    Vérificateur
    Reads:    code/decoupage.md, whole — the inventory first
              the technical document's preamble, and the entries the
              lots cite, one by one; its entry titles by grep
    Does:     1. Cross the inventory against the lots for seven kinds
                 of defect: an unbuilt surface, a hole, an overlap, an
                 orphan entry, a production nobody calls, a caller no
                 lot declares, a contract changed without its cascade.
              2. Record what orders lots without declaring it — a
                 modification consumed, two ends of one call.
              3. Confront each lot with the entries it cites: one
                 section, describing what the lot announces, and
                 nothing the lot needs beyond them.
              4. Derive the order mechanically; a cycle is a defect
                 and leaves the order empty.
              5. Group into blocks by layer and ceiling, counting
                 entries cited, not lots.
    Produces: code/sequence.md
    Runs:     once per cycle, again after each take-back

*Why it is not a script.* The id script (section 2) runs before it and
takes the orphan-entry case off its hands. The six others are readings
of what a symbol carries against what is asked of it, and no set
comparison makes them.

### 4.7 Détailleur

    Détailleur
    Reads:    code/sequence.md — its block, and ## Defects first
              code/decoupage.md, restricted to its lots, plus the
              inventory
              the technical document's preamble, and the entries its
              lots cite — those, and any one they point at for what a
              trigger reaches
              docs/CURRENT_TECHNICAL_STATE.md — two sections whole,
              the rest by symbol
              docs/TECHNICAL_CONVENTIONS.md, whole
              the code and the cycle's reports, by grep
    Does:     1. Per lot of the block: open the cited entries; derive
                 a signature from each rule — what goes in, what comes
                 out under a type that carries every outcome and what
                 it is worth at the edges, under the product's name.
              2. Grep every symbol before writing it; a symbol nothing
                 declares, nothing produced earlier and nothing the
                 framework owns is a blocker, never an interface
                 invented to fit.
              3. Write the acceptance criteria — observable, decidable,
                 attributable; one per behaviour, one on what each
                 trigger reaches, one per limit.
              4. Name the conventions the lot has to hold.
              5. After a divergence: rewrite only the sheets of the
                 block's uncoded lots, against the signature the code
                 actually carries.
    Produces: code/<lot>/fiche-executable.md per lot of the block;
              architecte/detailleur-<lot>.md when a convention is
              missing
    Runs:     once per block; again on the block's uncoded lots after
              a divergence

*Why per block and not per feature.* Section 8, D3.

### 4.8 Réalisateur

    Réalisateur
    Reads:    code/<lot>/fiche-executable.md
              docs/TECHNICAL_CONVENTIONS.md
              docs/CURRENT_TECHNICAL_STATE.md — two sections
              the code it is about to touch, and nothing more
              code/<lot>/verdict.md                 (on a FAIL)
    Does:     1. Work out where the code goes, from the conventions.
              2. Implement in the sheet's dependency order; write one
                 test per acceptance criterion; adapt the existing
                 tests a modification made false, never delete one.
              3. Run analysis and tests per coherent unit of work,
                 never per edit. Stop iterating when the same test
                 fails twice with the same message after a change
                 meant to fix it — the cause is not in this context;
                 report FAIL with that test.                 (changed, D9)
              4. Update the technical state; commit what belongs to the
                 lot; write the report, including the files touched.
                                                             (changed, D6)
              5. Return one line: the status word and the report's
                 path.                                       (changed, D14)
    Produces: the code, the tests, one commit,
              code/<lot>/compte-rendu.md; architecte/realisateur-<lot>.md
              when a running condition is undocumented
    Runs:     once per lot; a fresh one on each FAIL, three at most

*Why it writes its own tests.* Because the criteria it writes them from
were written by another hand, and a third hand checks that each test
asserts its criterion. Section 8, D5.

### 4.9 Relecteur

    Relecteur
    Reads:    code/<lot>/fiche-executable.md, code/<lot>/compte-rendu.md
              the code the lot touched, and its tests
              docs/TECHNICAL_CONVENTIONS.md — the rules the sheet names
              the scope script's result
    Does:     1. Symbols against the sheet: every signature promised,
                 created or modified as declared; every divergence
                 reported even when the code works, with the uncoded
                 lots of the block it makes false.
              2. One test per criterion, matched on what the test
                 asserts, never on its name.
              3. The conventions the sheet names hold on what the lot
                 touched.
              4. The report's fields hold.
              5. Nothing the lot writes for itself goes unread by it.
    Produces: code/<lot>/verdict.md — PASS, PASS with reservation,
              FAIL mineur, FAIL structurel; the cause; the affected
              lots
    Runs:     once per lot, at its realisation — never at the end of a
              block

*Why it stays.* Section 8, D5: four of its five points are things no
test written from the criteria can establish.

### 4.10 Contrôleur

    Contrôleur
    Reads:    desc-produit.md — the blocks its group names
              the sheets its group names                (confront)
              every partial report                      (assembly)
    Does:     1. Confront: read the group's sheets once; take each
                 block sentence by sentence and ask whether a signature
                 or a criterion observes that intention — a join needs
                 a criterion on the join, a trigger a criterion on what
                 it reaches. Found, missing, or doubtful.
              2. Assemble: merge the partial reports in block order
                 into a new numbered report, changing no line.
    Produces: code/controle/<group>.md, code/rapport-controle.md
    Runs:     once per group of blocks, then once to assemble, when
              every lot has passed

*Why a reader and not the coverage-by-tests script.* Section 8, D7: an
identifier says that something cites a block; it cannot say that the
citation carries the block's fifth sentence, or that the thing the
block triggers is reached by anything. The id script takes the gross
case; the Contrôleur reads what is left.

### 4.11 Arbitre

    Arbitre
    Reads:    the blocking files of one round, all before settling one;
              the settled ones beside them
              the split, the order, the technical document; the lot's
              sheet and report when the block bears on a lot
              docs/TECHNICAL_CONVENTIONS.md, whole
              the code, by grep, to confirm a fact
    Does:     1. Read every block of the round; two naming one symbol,
                 one contract or one module are one problem.
              2. Apply the one test: does the answer change a behaviour
                 the corpus describes? Yes — hand back to the person,
                 saying which behaviour. No — find the rule, the entry
                 or the place in the code that already answers it.
              3. Write the Decision: one instruction, what it rests on,
                 where it stops — and the sheets and lots it makes
                 stale, so the orchestration resets them.  (changed, D10)
              4. A lot blocked a second time after a settlement is
                 handed back whatever its content.         (changed, D10)
    Produces: the ## Decision field of each blocking file, and nothing
              else in them
    Runs:     once per round of blocks

*Why it writes one field and not the artefact.* Section 8, D10: the
agent that owns a document is the one that knows its shape; a settler
that amends three kinds of artefact is a fourth writer every reader
must reconcile.

---

## 5. Every loop

### 5.1 The questions loop

    Between:            Analyste ⇄ the person, with the grid invocation
                        as gate
    What sends you in:  a questions file with at least one entry whose
                        Answer line is empty
    What gets you out:  the grid invocation writes an empty questions
                        file
    What bounds it:     nothing in rounds — a person is in it. What
                        makes it converge is the Default line: a
                        question she agrees with costs her one word,
                        and the grid re-runs only on the blocks that
                        moved. An entry she leaves empty stays a
                        question; the loop does not close on silence.
    Who steps in:       the person, every round

### 5.2 The technical closing loop

    Between:            Convertisseur → the person → Analyste →
                        Convertisseur
    What sends you in:  a closing invocation — on the product file or
                        on the produced document — wrote a question
    What gets you out:  the questions file comes back empty, every
                        assumption mark is replaced, the fresh closing
                        invocation writes closed
    What bounds it:     nothing in rounds — a person is in it. An
                        answer that created a block re-runs the product
                        grid before the technical document is touched;
                        one that only sharpened a sentence goes
                        straight to a targeted update.
    Who steps in:       the person, every round

### 5.3 The conventions loop

    Between:            Architecte → the person → Analyste →
                        Convertisseur → Architecte
    What sends you in:  the deriving invocation raised a coverage or a
                        conjunction gap
    What gets you out:  the answers have entered the product file and
                        the technical document, and the integrating
                        invocation wrote the rules they derive
    What bounds it:     one round: the integrating invocation raises
                        nothing new, or what it raises is a question
                        of the same kind and the loop runs once more.
                        Once per project.
    Who steps in:       the person, once

### 5.4 The split loop

    Between:            id script → Cadreur → id script → Vérificateur
    What sends you in:  a technical document with no assumption mark
    What gets you out:  the Vérificateur writes an empty ## Defects
                        with an order and blocks
    What bounds it:     three rounds. A third round with defects
                        remaining goes to the person with the defect
                        list — the split is not describable from the
                        document as it stands.
    Who steps in:       nobody, then the person on exhaustion

### 5.5 The lot loop

    Between:            Réalisateur → scope script → Relecteur, per lot
    What sends you in:  a lot with a sheet and no PASS
    What gets you out:  a PASS or a PASS with reservation; the
                        orchestrator merges
    What bounds it:     three Réalisateurs per lot, each fresh, each
                        with the verdict; and, inside each, the
                        stopping rule of 4.8 move 3. The third FAIL
                        goes to the Arbitre with the verdict, then to
                        the person if the Arbitre finds nothing.
    Who steps in:       nobody, then the person on exhaustion

### 5.6 The block loop

    Between:            Relecteur → Détailleur → the lot loop
    What sends you in:  a verdict names a symbol divergence and the
                        uncoded lots of the block it affects
    What gets you out:  those sheets are rewritten against the code as
                        it is, and the lot loop resumes on the next lot
    What bounds it:     one rewrite per divergence; a divergence on a
                        rewritten sheet is a blocker, not a second
                        rewrite
    Who steps in:       nobody

### 5.7 The requests loop

    Between:            Cadreur, Détailleur or Réalisateur → Architecte
                        → the agent, on its next lot
    What sends you in:  a request in architecte/ with an empty
                        ## Verdict
    What gets you out:  every request of the folder carries a verdict;
                        the conventions file carries the rules that
                        were conventions
    What bounds it:     the agent that wrote the request goes on
                        against the conventions as they stand unless it
                        cannot; the Architecte runs at the end of the
                        block, once per round
    Who steps in:       nobody; the person if the Architecte blocks on
                        a product decision

### 5.8 The blocking loop

    Between:            any agent → Arbitre → the agent that resumes,
                        with the stale sheets reset
    What sends you in:  a blocking file with an empty ## Decision
    What gets you out:  the Decision is filled and the agent resumed;
                        or the Decision says not settled here, and the
                        person fills it
    What bounds it:     one settlement per lot. A second block on the
                        same lot after a settlement is handed back
                        whatever its content — two blocks in one place
                        means the lot is not describable, and a third
                        guess is not a design.
    Who steps in:       nobody, then the person

### 5.9 The correction cycle — not a loop, a second cycle

    Between:            Contrôleur → the person → Diagnostiqueur →
                        the split loop → the lot loop → Analyste
    What sends you in:  the person lists observed gaps — from the
                        Contrôleur's report, from her own testing
    What gets you out:  every lot of the correction split passed, and
                        the Analyste carried its product decisions back
                        into the product file
    What bounds it:     none — a person opens it
    Who steps in:       the person, at its opening

This path costs a split and a code chain. It is the cost of every gap
that reached the code, and its frequency per feature is the number
this whole verdict is trying to lower.

---

## 6. The flow, in one view

```
                    ┌────────────────────────────────────────────────────────┐
                    │  A. CLOSING THE PRODUCT            (with the person)   │
                    │                                                        │
   idees.md ──────▶ │  Analyste  ──▶ desc-produit.md + questions (Default:)  │
                    │     ▲  │                                  │            │
   PRODUIT_GLOBAL ─▶│     │  └── grid invocation ──▶ questions ─┤  5.1       │
   (by index)       │     │                                     ▼            │
                    │     └────────────── answers ──────── the person        │
                    │     ▲                                                  │
                    │     │  every downstream answer enters here   (5.2, 5.3)│
                    └─────┼──────────────────────────────────────────────────┘
                          │                    ‖  product closed
                    ┌─────┼──────────────────────────────────────────────────┐
                    │  B. DECIDING THE TECHNIQUE          (once per feature) │
                    │     │                                                  │
                    │  Convertisseur: close ──▶ produce ──▶ close (fresh)     │
                    │                              │            │  5.2       │
                    │                       spec-technique.md   questions ──┘
                    │                       tracabilite.md                   │
                    │                              │                         │
                    │  Architecte ──▶ TECHNICAL_CONVENTIONS.md  (once/project)│
                    │       ▲                      │              5.3        │
                    │       └── requests (5.7) ────┼───────────────────────┐ │
                    └──────────────────────────────┼───────────────────────┼─┘
                                                   ‖  technical closed     │
                    ┌──────────────────────────────┼───────────────────────┼─┐
                    │  SPLIT                       ▼                       │ │
                    │  [id script] ──▶ Cadreur ──▶ [id script] ──▶ Vérificateur
                    │                    ▲                            │  5.4 │
                    │                    └──────── ## Defects ────────┘      │
                    │                                   sequence.md          │
                    └──────────────────────────────────────┼─────────────────┘
                    ┌──────────────────────────────────────┼─────────────────┐
                    │  C. PRODUCING THE CODE     (per block, per lot, in order)
                    │                                      ▼                 │
                    │  Détailleur ──▶ sheets of the block                    │
                    │      ▲               │                                 │
                    │      │ 5.6           ▼                                 │
                    │      │        Réalisateur ──▶ code, tests, commit      │
                    │      │            ▲  │                                 │
                    │      │            │  ▼                                 │
                    │      │            │ [scope script]                     │
                    │      │            │  │                                 │
                    │      │            │  ▼                                 │
                    │      └──────── Relecteur ──▶ verdict ── 5.5 (×3)       │
                    │                        │                               │
                    │                        ▼ PASS: merge, next lot         │
                    │                                                        │
                    │  any agent ──▶ blocked ──▶ Arbitre ──▶ decision + stale │
                    │                               │       5.8 (×1 per lot) │
                    │                               ▼ not settled here       │
                    │                    ═══ the person ═══                   │
                    └────────────────────────────────────────────────────────┘
                                          │  every lot passed
                                          ▼
                    Contrôleur ──▶ rapport-controle.md ──▶ the person
                                                              │
                              ┌───────────────────────────────┘
                              ▼  bug-list.md                        5.9
                    Diagnostiqueur ──▶ desc-bug.md ──▶ SPLIT ──▶ C ──▶ Analyste
                                                                     (carry back)
                              │  feature finished
                              ▼
                    Fusionneur ──▶ PRODUIT_GLOBAL.md   (outside this comparison)
```

The orchestrator is every arrow, and runs the two bracketed scripts.

---

## 7. What it makes of each of our eleven agents

    analyste          changed
    A Default line under every question; the product file becomes the
    one door for every product answer, whichever agent asked. Round
    trips down per question, robustness held: she still writes the
    answer, and a decision recorded in the wrong document no longer
    happens.

    diagnostiqueur    kept as is
    The proposal has no correction cycle; without one, a gap observed
    after testing has no path back to the code except a new idea file
    through the whole upstream loop. Robustness across features, and
    round trips: one gap costs one investigation, not a cycle.

    convertisseur     changed
    Its part-2 closures move into a third invocation that did not
    write the document. Robustness: the author/reader split the
    proposal argues for its Closer, and ours applies on the product
    file, was missing on the technical document from the second
    feature onward, when the Architecte no longer reads it.

    architecte        changed
    On a taken-over codebase, the deriving invocation reads the build
    files; its coverage and conjunction answers reach it through the
    product file and the technical document, not as raw answers turned
    into rules. Round trips on a takeover; robustness on where a
    behaviour is recorded.

    cadreur           kept as is, plus a preservation lot on a takeover
    Its greps of callers, fulfilments, pieces and listeners are what
    turn a document into lots that compile and are called. The
    proposal's Splitter cannot see any of them and pays each one as a
    block at implementation. Robustness and round trips. The
    preservation lot is the proposal's L-00, taken for the one case
    where the existing suite cannot be trusted.

    verificateur      kept as is
    No equivalent in the proposal; its seven defect kinds are readings
    of what a symbol carries against what is asked of it, which a set
    comparison on ids cannot make. Robustness: a defect it catches
    would otherwise surface as a module that stops compiling in a lot
    that touches neither end. The id script only takes the orphan
    entry off its hands.

    detailleur        kept as is
    Per block, against the real code, it gives signatures that were
    grepped after the previous block was coded. The proposal's
    signatures written for a whole feature before any code exists
    drift on every lot, and one context could not hold them for fifty
    lots. Robustness first, tokens second.

    realisateur       changed
    Its own analyse-and-test loop gets a stopping rule, its report
    names the files it touched, and it returns one line. Tokens on a
    stuck loop and on the orchestrator's context; robustness: a
    context that iterates against a failure it does not understand
    converges on the test.

    relecteur         kept as is
    The proposal drops the reviewer for a Test-writer. Four of the
    Relecteur's five points are things no test written from the
    criteria establishes: a convention whose test is a review, a test
    asserting less than its criterion, a symbol divergence and the
    sheets it makes false, a value written and never read.
    Robustness.

    controleur        kept as is
    The proposal's coverage-by-tests script checks that a block is
    cited; the Contrôleur checks that each of its sentences is
    observed, and that what a trigger reaches is reached. Robustness:
    the missing intentions it reports are what a correction cycle
    would otherwise be opened for. The id script runs before it, not
    instead of it.

    arbitre           changed
    Its decision names the sheets and lots it makes stale, and a second
    block on one lot after a settlement goes to the person whatever
    its content. Robustness: a sheet written against a signature a
    decision changed is coded from otherwise; round trips: an
    unbounded settlement loop on one lot buys nothing after the
    first.

---

## 8. The divergences that mattered

Each entry: what differs, which measure moves and how, which chain is
right and why. Divergences that moved no measure — lots vs. vertical
slices, `Bn` vs. `P-n`, one grid vs. three, French answers, a ledger
vs. status lines — are not listed.

### D1 — A proposed answer under every question, and silence as consent

    What differs
    The proposal writes a Default line under every question and closes
    every question the person leaves empty on that default, counting
    them in a header. Ours writes an empty Answer line and loops until
    a questions file comes out empty — every question is answered by
    her hand, and no agent proposes an answer.

    Which measure moves
    Round trips: down for the proposal, on both counts — a question
    with a proposed answer is read in seconds, and a round where she
    changes nothing ends the loop. Estimated: ours has run, and its
    rounds are the person's cost, not observed here. Robustness: down
    for the proposal on the second count only — a default she never
    read is a decision she did not take, and it sits in region A,
    where a gap costs the whole chain (the proposal's own 9.1 says so).

    Which chain is right
    Each on one half. The Default line is right: it changes what she
    reads, not who decides, and it costs the agent one line it was
    going to reason about anyway. Silence-as-consent is wrong on the
    measure that prevails: the cadrage grid already says a consent is
    never ticked by default, and the same holds for any product
    statement. The final chain writes the Default and requires the
    answer, even when the answer is one word.

### D2 — Where a late product answer is recorded

    What differs
    In the proposal every product question, from whichever region,
    returns through the Structurer into product.md, and flows down
    from there. In ours the Convertisseur's questions do the same —
    an answer comes back through the Analyste first, always — but the
    Architecte's coverage and conjunction questions, which are
    behaviour questions by its own definition, are answered into the
    conventions file as rules, and the product file never sees them.

    Which measure moves
    Robustness: a behaviour settled in TECHNICAL_CONVENTIONS.md is
    invisible to the Contrôleur, which reads product against sheets,
    and to the Fusionneur, which merges the product file into the
    global. The next feature's Analyste reads a global that does not
    carry it and asks again, or worse, contradicts it. Observed on the
    agent file, not on a run.

    Which chain is right
    The proposal. One door for product answers is what makes the
    product file the single source, and ours already holds that rule
    for one of its two downstream askers. The final chain routes the
    Architecte's answers through the Analyste and the Convertisseur,
    and its integrating invocation derives rules from the updated
    documents rather than from the answers.

### D3 — Signatures fixed up front for the feature, or per block against the code

    What differs
    The proposal's Designer writes every signature into tech.md before
    any code exists; the Splitter copies them into lots; the
    Test-writer greps each one at its lot and blocks on drift; a
    Settler amends. The proposal considered just-in-time detailing and
    rejected it as one invocation per lot and a loss of reproducibility.
    Ours writes no signature before the split; the Détailleur writes
    them per block, after the previous block was coded, grepping every
    symbol.

    Which measure moves
    Robustness: for ours. Drift is the proposal's admitted price (9.5:
    one block per run is acceptable, one per lot means reconsidering),
    and it grows with the number of lots between the signature and
    its use; a feature of fifty lots has forty-nine such gaps to
    drift across. Ours has a divergence path (Relecteur naming
    affected lots, Détailleur rewriting) because divergence happened
    even inside a block — on the observed chain, the shorter horizon
    was still not zero. Tokens: for ours. The proposal's objection
    was per-lot cost; the block answers it — one Détailleur for a
    layer's worth of lots. And its own size rule concedes that one
    Designer context cannot hold a whole application's signatures.

    Which chain is right
    Ours. The block is the device that makes just-in-time both
    affordable and short-horizon. Reproducibility, which the proposal
    trades for, is not one of the three measures.

### D4 — A split cut from the document alone, or with the code in view

    What differs
    The proposal's Splitter reads tech.md and the conventions, groups
    by (layer, entity) cell, and never greps; its lot names the files
    an Implementer may touch, and a file needed and not named is a
    scope fault the Implementer blocks on. Ours' Cadreur greps every
    symbol, the callers of every modified contract, what fulfils it,
    the tests that call it; cuts a lot for every piece that reaches
    outside the program; names what has to be declared outside the
    code; finds what listens for each trigger. The Vérificateur then
    fails the split on seven kinds of defect.

    Which measure moves
    Robustness and round trips: for ours. Every caller the Splitter
    cannot see is a lot that does not compile, or a contract that
    compiles, passes its tests and does nothing — the Cadreur's file
    says this was seen. In the proposal each such case is caught at
    implementation, costs a block, a Settler, a reset of the lots
    after it; in ours it is caught before any sheet exists. Tokens:
    for the proposal — the Cadreur and the Vérificateur are two Opus
    readings the Splitter does not pay. The first measure prevails.

    Which chain is right
    Ours. What the proposal gets right within this — the file-scope
    check on the diff — is taken separately (D6).

### D5 — A Test-writer before the code, or a reviewer after it

    What differs
    The proposal has no reviewer: a Test-writer writes the tests from
    the lot's criteria before the code, the Implementer may not edit
    them, and a scope script checks the diff. Ours has the Réalisateur
    write code and tests from a sheet another hand wrote, then a
    Relecteur checks five points and writes the verdict.

    Which measure moves
    Robustness: for ours. The tests can establish that the code does
    what the criteria say. They cannot establish (a) that a test
    asserts its whole criterion — in the proposal nobody reads the
    Test-writer's tests, and 9.2 admits it; (b) that a convention
    whose test the grid marks as review holds — and the conventions
    grid marks most of its entries that way; (c) that a symbol carries
    the promised signature and which uncoded sheets a divergence makes
    false — the proposal catches this one lot later, by grep, as a
    block; (d) that a value the lot writes for itself is ever read —
    a parameter ignored, a handle never awaited, the three ways a
    signature lies that G5.9 says were each seen. Tokens: equal — one
    invocation per lot either way. Round trips: for ours — an
    Implementer that may not touch a test blocks on every existing
    test a modification made false; the Réalisateur adapts it and the
    Relecteur sees the diff.

    Which chain is right
    Ours. The separation the proposal wants is already there, one
    level up: the criteria are the Détailleur's, the tests are checked
    against them by the Relecteur on what they assert. What ours takes
    from the proposal is the stopping rule (D9) and the scope script
    (D6), not the shape.

### D6 — A mechanical check on what a lot touched

    What differs
    The proposal's lot names the files it may create and modify, and a
    script rejects any diff outside them, test files included. Ours
    bounds a lot by symbols, not files; the Relecteur checks that
    promised symbols exist and that nothing declared is unused, but
    nothing checks that the diff stayed inside what the lot was for.

    Which measure moves
    Round trips: for the proposal. A file touched outside the lot —
    another lot's symbol edited in passing, a test elsewhere adapted
    to make a suite pass — surfaces in ours at the next Détailleur
    (a production that already exists) or at the next Relecteur, one
    or more lots later, as a divergence with a block. Tokens: zero for
    the script. Estimated: no run of ours is in front of me to count
    the cases.

    Which chain is right
    The proposal, on the check; ours, on who declares the scope. The
    Cadreur bounds by symbol on purpose — the same file may be touched
    by two lots. So the final chain has the report declare the files
    the lot touched, the script compare it to the diff, and the
    Relecteur compare the declared files to the sheet's symbols. A
    diff outside the declaration fails before the Relecteur reads.

### D7 — Coverage by identifiers, mechanically

    What differs
    The proposal assigns an id to every product statement and carries
    it to the technical item, the lot, and the test name, so that
    "nothing lost" is a set difference computed by a script, before the
    split and again after the last lot. Ours carries ids at every
    level too — Bn, §n.m, lot-NN, criteria — and a traceability file
    from block to entry; but no script reads them, and from the second
    feature onward no agent reads the traceability file at all (the
    Architecte, its only reader, runs once per project). What ours has
    instead is readers: the Convertisseur's nothing-dropped closure,
    the Vérificateur's orphan-entry check, the Contrôleur's sentence-
    by-sentence confrontation.

    Which measure moves
    Robustness: for ours on content, for the proposal on presence. An
    id says a block is cited; it does not say the citation carries the
    block's fifth sentence — the proposal concedes it ("a statement
    with two facts hides one from the coverage script"), and its answer
    is a granularity rule that is itself a reading. The Contrôleur's
    "a join needs a criterion on the join" is a check ids cannot make.
    But a block absent from the traceability file, or an entry no lot
    cites and none declares, is a presence gap a script finds at zero
    tokens before the split — and in ours, after feature one, nothing
    finds the first of those until the Contrôleur, after all the code
    is written. Tokens: for the proposal, on the gross case.

    Which chain is right
    Both, at different grains. The final chain runs the id script
    before and after the Cadreur — presence, zero tokens — and keeps
    every reader for content. Statement-level ids are not adopted: the
    Contrôleur already works at the sentence, and a P-n numbering
    would add a rule about what one fact is without removing the
    reading that decides it.

### D8 — A fresh reader of the technical document

    What differs
    Neither chain has one. The proposal argues that a reader of
    tech.md who had not read product.md could not judge it, and one
    who had would redo the Designer; it settles for the id script.
    Ours runs eight closures on the technical document — in the
    context that wrote it. The Architecte reads both documents whole
    as a stranger, but once per project; the Cadreur reads the
    document whole but, as the grid states in so many words, does not
    judge its content; every agent after him opens a few entries.

    Which measure moves
    Robustness: a "nothing dropped" miss — a set named where the
    product gave its members one by one — or two entries agreeing
    badly on one value, reaches the code and costs a correction
    cycle. The proposal's own Closer argument names the mechanism:
    the author holds the intent the text failed to carry. Ours applied
    that argument to the product file and not to the next document.
    Tokens: one more reading of two documents per feature, by the
    Convertisseur's model. Estimated: no run is in front of me to
    count what the author's own closures missed.

    Which chain is right
    Neither as written. The final chain moves the part-2 closures into
    a third Convertisseur invocation that did not produce the document
    — the same device the Analyste uses between structuring and the
    grid.

### D9 — A stopping rule inside the implementer

    What differs
    The proposal's Implementer stops iterating when the same test
    fails twice with the same message after a change meant to fix it,
    and reports FAIL — a fresh context with the log takes over. Ours'
    Réalisateur runs analysis and tests "until both pass", with no
    internal bound; the bound is on Réalisateurs, three per lot.

    Which measure moves
    Tokens: a stuck context iterates until it exhausts itself, and the
    three-Réalisateur bound only starts counting once it has. Robustness:
    an agent iterating against a failure it does not understand
    converges on the test rather than on the sheet — and the
    Réalisateur may adapt existing tests, which is the one place that
    convergence has somewhere to go. Estimated on the second point;
    the first follows from the rule's absence.

    Which chain is right
    The proposal. The final chain gives the Réalisateur the stopping
    rule, and the FAIL it reports carries the test and the message so
    the fresh Réalisateur starts where the stuck one stopped.

### D10 — What a settler writes, and how often it may settle one lot

    What differs
    The proposal's Settler amends the artefact the block lives in —
    a signature in tech.md, a criterion in a lot, a file added —
    writing beside the old text; lists the lots its amendment makes
    stale so the conductor resets them; and, on a second block of the
    same lot after a settlement, hands back to the person whatever the
    content. Ours' Arbitre writes one field, the Decision, and the
    agent that blocked applies it to its own artefact; nothing names
    the sheets a decision makes stale; nothing bounds how many times
    one lot may be settled.

    Which measure moves
    Robustness: for ours on who writes — a settler amending three
    kinds of artefact is a fourth writer each reader has to reconcile,
    and the agent that owns a sheet is the one that knows how a
    changed signature propagates through it. Robustness: for the
    proposal on the stale list — a sheet in the same block written
    against a signature the decision changed is coded from, in ours,
    unless the Détailleur happens to be the one who blocked. Round
    trips and tokens: for the proposal on the ceiling — a lot blocked
    twice is a lot the document does not describe, and a third
    settlement is a guess with a cost.

    Which chain is right
    Ours on the field, the proposal on the list and the ceiling. The
    final chain keeps the Arbitre writing the Decision alone, adds the
    stale sheets and lots to that Decision, and hands a second block on
    one lot back to the person.

### D11 — The build files as an input of the conventions

    What differs
    The proposal's Architect, on an existing application, reads the
    manifest, the dependency file, the test configuration and the CI
    file, and writes down the build command, the test command, the
    layout as it is. Ours' Architecte, at its deriving invocation,
    reads no code and no build file — the verify command and the
    dependency table are filled from platform knowledge — and may
    open the build files only at its request invocation.

    Which measure moves
    Round trips, on a taken-over codebase only: a verify command or a
    module list written from platform knowledge and wrong for this
    project is discovered by the first Réalisateur, becomes a request,
    and costs an Architecte round before any lot passes. On a codebase
    the chain built, nothing moves: the conventions came first and the
    code follows them, and reading the code back would be deriving
    from one's own output — the reason ours forbids it. Estimated: the
    observed chain ran on a codebase it built.

    Which chain is right
    Each on its case. The final chain lets the deriving invocation read
    the build files, and them alone, on a taken-over codebase — the
    same exception the request invocation already carries, for the
    same reason.

### D12 — A code map per run, or a maintained global and state document

    What differs
    The proposal surveys the code by grep at every run into a
    code_map.md — signatures copied verbatim, "today: X" lines — read
    by the Structurer for defaults, the Designer for reuse, the
    Test-writer for a preservation lot L-00 whose tests must pass on
    the untouched code before any change. It rejects every existing
    document on the ground that documents lie. Ours reads no code
    upstream: the Analyste reads the global product document, in
    product words, maintained by the Fusionneur after each feature and
    by the Analyste's bug-fix pass; downstream, the Cadreur and the
    Détailleur grep the code for every symbol and read a state
    document that carries what grep cannot give — traps, dead state.

    Which measure moves
    Robustness: for ours in general. The Structurer writing "as today"
    statements from signatures writes them in the code's vocabulary
    — the proposal's own boundary argument in 7 says what that costs
    the person — while the global is in hers. "Documents lie" is
    answered in ours not by trusting the state document but by
    grepping every symbol before it is written, and keeping the
    document for the traps the code cannot show; the proposal has no
    place for a learned trap and rediscovers it each run. Tokens: for
    ours — a map regenerated per feature is paid per feature; an index
    grepped is not. Robustness on a taken-over codebase: for the
    proposal's preservation lot — there the existing suite cannot be
    trusted to hold the behaviours a lot modifies, and a test validated
    on untouched code is the only check that can exist before the
    first change. On a codebase the chain built, every criterion
    already has a test and the existing suite is the preservation
    suite; the lot would pay for tests that exist.

    Which chain is right
    Ours, with the preservation lot taken for the takeover case only —
    and there, its criteria come from the global's own blocks for the
    modified symbols, so that its green run also validates the
    Extracteur's description against the code. Estimated.

### D13 — A correction cycle

    What differs
    Ours has one: an observed gap becomes a bug list, one Diagnostiqueur
    per gap confirms it against the code and names its bearer, an
    assembly writes a technical document in the same shape the Cadreur
    cuts, and the Analyste carries the product decisions back. The
    proposal has none; a gap found in use has no path but a new idea
    file through the whole upstream loop.

    Which measure moves
    Robustness across features: without the carry-back, the product
    file and the global describe an application that no longer behaves
    that way, and the next feature is closed against a false document.
    Round trips: one gap costs one investigation and one split of a
    few lots, not a product loop with the person.

    Which chain is right
    Ours. The proposal measures itself by corrections after testing
    and never says how one is made.

### D14 — What an agent hands back to the orchestrator

    What differs
    The proposal's agents report one line — OK and a sha, FAIL and a
    test, BLOCKED — and its conductor reads nothing else. In ours some
    agents bound their return (the Architecte, three lines) and most do
    not; the orchestrator's context over a cycle is the sum of what
    fifty lots' worth of Réalisateurs, Relecteurs and Détailleurs said
    back.

    Which measure moves
    Tokens: the orchestrator's context grows with every return, and
    the CLAUDE.md warns that this is what makes an orchestrator both
    expensive and opinionated. Estimated: the size of the returns on
    the observed chain is not in front of me.

    Which chain is right
    The proposal. The final chain has every agent return one line —
    status word and path — since every artefact already carries the
    content.

---

## 9. Where this verdict estimated rather than observed

Every measure on the proposal is an estimate: it has not run. Beyond
that, the following claims about ours rest on reading the agent files
and the grids, not on a run's artefacts, and a run could overturn
them:

- **D1** — that a Default line lowers the person's cost per question
  without anchoring her on the agent's answer. The proposal's 9.1
  measurement — tracing each later correction to whether its statement
  was answered or defaulted — is the right one and applies unchanged.
- **D6** — how often a Réalisateur touched a file outside its lot on the
  observed chain. If never, the scope script costs nothing and catches
  nothing.
- **D8** — how many part-2 closure misses the author's own context let
  through. If the Convertisseur's self-closure was clean over the
  observed features, the third invocation is a reading paid for
  nothing, and 9.4's argument on the Closer applies to it too.
- **D9** — whether a stuck Réalisateur ever adapted a test wrongly. The
  token claim stands without it.
- **D10** — whether a decision ever changed a signature a not-yet-coded
  sheet of the same block depended on, in a block whose Détailleur was
  not the one that blocked.
- **D11, D12** — everything about a taken-over codebase: the observed
  chain ran on code it built.
- **D14** — the actual size of the agents' returns on a fifty-lot cycle.

One observation outside the named files bears on the whole: the
session's git log shows a first feature followed by six correction
cycles. That is evidence that gaps reached the code on the working
chain; it says nothing about which region let each through, and this
verdict has not read those cycles. The measurement that would rank
the divergences above by weight is the one the proposal's 5.6 names:
for every gap of those six cycles, which document first failed to
carry it.

---

*End of the verdict. The chain above is ours; what changed is listed
in 1.3, justified in 8, and carried into the next phase agent by
agent.*
