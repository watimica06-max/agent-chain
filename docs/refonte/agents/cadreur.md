# cadreur — examination

Files read, in this order: `.claude/agents/cadreur.md` (813 lines),
`.claude/commands/7_lots.md` (the only command that invokes it; 219
lines), `.claude/commands/cycle.md` (does not invoke it — it chains
`/7_lots` and names the cadreur in its routing table; read because that
table says what the Product Owner runs after a cadreur block), then
`docs/refonte/verdict.md` sections 2 (the cadreur line) and 4 to 7.

## Plane 1 — the agent as a whole

**Role, from the file:** the cadreur turns one technical document
(`spec-technique.md` or `desc-bug.md`) into `code/decoupage.md` — a
symbol inventory established by grep, then a list of lots each citing
entries of one section and declaring what it needs, produces and
modifies — and then calls the vérificateur on that file, corrects the
lots its defects name, and calls it again, three rounds at most.

**Its moves, in order:**

| # | Move | Why it exists | What it feeds | What it overlaps |
|---|---|---|---|---|
| 0 | Part 2 — read the disk, pick block A/B/C/D | Without it every run is a first split and destroys a corrected or coded split | Everything after | Block D restates it ("First thing, every run: look for `code/blocked_cadreur.md`") |
| 0b | Which cycle — feature or bug fix | The bug-fix document has bearers; grouping differs | Moves 3 and 4 | Contradicts move 10 and *What you never do* (see comment 7) |
| R | Read the technical document and the conventions in full | The only agent that sees the whole document; the conventions bound a lot | Moves 2 to 9 | Move 2 says "Read it in full" again |
| 1 | Grep `<<ASSUMED`, stop on a hit | A provisional rule would be cut into a lot about to change | Blocking file | *When you cannot produce* lists the same case |
| 2 | Read in full; honour `Out of scope` | No lot for what the feature does not touch | Move 4 | Reading section R |
| 3 | Inventory the symbols, grep each, write the inventory | The gap between what the code carries and what entries ask is what has to be built | `## Symbols`; moves 5 and 6 | Move 6 greps the same names again (comment 14) |
| 4 | Group entries into lots, section by section | The Convertisseur numbered, it did not group | The lot list | — |
| 5 | Declare Needs / Produces / Modifies | The vérificateur's dependency check and the Détailleur's sheets rest on these | The four fields | Move 7's second half (what an entry obliges to exist) refines the "Production" row |
| 6 | Grep the callers, fulfilments and look-alikes of every modified symbol; name what calls each production | A changed contract breaks them; undeclared, the Réalisateur meets them at the build | `Modifies`, `Produces` | Move 3's grep on the same names |
| 7 | Find the pieces; find what an entry obliges to exist | A contract with nothing behind it does nothing | New lots; `Needs` | Move 5's "Production" row |
| 8 | Name what has to be declared outside the code | No grep on a symbol finds a manifest line | `Modifies`; conventions requests | — |
| 9 | Find the listener of every trigger | A rule nobody calls is dead code | `Modifies`; possibly a new lot | Move 7's "cut a lot for it" (same open question: which lot, which anchor) |
| 10 | Cite the anchors; list the entries with no lot | The Détailleur opens only what is cited; an uncited entry is invisible downstream | `Anchor`; `## Entries with no lot` | — |
| W | Write `code/decoupage.md` in the given shape | The vérificateur parses it | The vérificateur | — |
| V | Call the vérificateur, wait, read `## Defects`, correct the named lots, up to three rounds | A fresh reader checks the split; the ceiling stops the loop | `code/sequence.md`; the command's table | Block B is the same loop entered cold |
| B | Take-back from cold | A `/7_lots` re-run by hand on a `## Defects` left on disk | Same as V | V |
| C | Redécoupage | Coding proved the split wrong; coded lots are closed | New lots; `## Ce qui revient` / `## Ce que j'en fais` in `code/redecoupage.md` | — |
| D | Apply a Product Owner decision, rename the blocking file | The only way a block lifts | The other blocks | Move 0 |

**Judging the set.**

- Every move feeds something a later reader uses, with one exception:
  move 3's row "It exists and already carries it — Nothing, and say
  so" produces a fact that no field of the output carries (comment 13).
- The moves cover the role. Two jobs fall between moves: what happens
  when the vérificateur blocks instead of writing a sequence (comment
  18), and what block C does once its lots are added — nothing says
  the vérificateur is called (comment 19).
- No move could go. Removing move 3 would leave move 5 declaring
  against symbols never grepped; removing move 9 would leave rules
  nobody calls; removing V would put the loop back on the orchestrator.
- The order holds, except that the bug-fix exception to the
  one-section rule (Part 2) is stated 300 lines before the rule it
  excepts and is absent from the rule itself (comment 7), and move 3
  points forward to "move 5" for something move 7 holds (comment 12).

## Plane 2 and Plane 3 — the comments

Applied top to bottom.

---

### 1

    Fichier      : .claude/agents/cadreur.md
    Cible        : PART 2 dispatch table (lines 226-231), block D's own
                   table (lines 790-794), "One invocation per cycle"
                   (line 24), "Which cycle is this?" (lines 249-250)
    Aujourd'hui  : The Part 2 table has four rows: blocked file with
                   `## Decision` filled → D; `code/redecoupage.md` → C;
                   `## Defects` → B; "None of these" → A. Block D then
                   adds a row Part 2 does not have — `## Decision`
                   still empty → "Stop. Nothing changed". Part 2 also
                   says "D, then the block that applies after it" and,
                   ten lines later, "On B, C or D, you do not run block
                   A's ten moves". Line 24 says "One invocation per
                   cycle".
    Le défaut    : Plane 2, question 4 (an instruction that reads two
                   ways) and the known pattern "two passages asking for
                   different things". A blocking file with an empty
                   Decision matches no Part 2 row but "None of these",
                   which is a first split over a standing block. A
                   block raised before any split existed (no
                   conventions, `<<ASSUMED`, unnumbered sections) has
                   to be followed by A's ten moves once the decision
                   is applied — Part 2 forbids exactly that. "One
                   invocation per cycle" is false the moment B, C or D
                   exists.
    Ce qu'il faut: One dispatch table, in one place, whose rows are
                   exhaustive over what can sit on disk: blocking file
                   with empty Decision → stop, say it stands; blocking
                   file with Decision filled → apply it, then dispatch
                   again on what remains (which may be A, when no
                   `code/decoupage.md` exists); the rest as today. The
                   "never A's ten moves after D" rule holds only when a
                   split already exists on disk. Drop or qualify "one
                   invocation per cycle".
    Justification: Robustness — the empty-Decision case today lets a
                   first split overwrite a blocked one when `/7_lots`
                   is run by hand (`/cycle` catches it, `/7_lots` does
                   not). Round trips — a D followed by an impossible
                   "no ten moves" leaves the agent to invent what a
                   first split after a decision looks like.

---

### 2

    Fichier      : .claude/agents/cadreur.md, and .claude/commands/7_lots.md
    Cible        : Block D, "Renaming means renaming — git mv, or the
                   equivalent" (lines 794-802); frontmatter `tools`
    Aujourd'hui  : The agent must rename `code/blocked_cadreur.md` to
                   `code/blocked_cadreur-NN.md` and leave "nothing at
                   the old name — not a copy, not a note, not an empty
                   file". Its tools are Read, Grep, Glob, Edit, Write,
                   Agent. The command has Bash and never touches the
                   blocking file.
    Le défaut    : Plane 2, question 2 — a move the agent cannot do
                   with what it has. Write creates the numbered file;
                   nothing in its tool set removes the unnumbered one.
                   The only reachable outcome is the one the rule
                   forbids: a numbered copy beside an untouched
                   original, or an emptied original.
    Ce qu'il faut: Either the rename is the command's step (it has
                   Bash, and it already reads the disk after the agent
                   hands back), with the agent only reporting that the
                   decision was applied; or the agent gets the tool the
                   move needs. Either way the agent's text must not
                   demand what its tools cannot do.
    Justification: Robustness — "anything left at the unnumbered name
                   reads as a block still standing", by the agent's own
                   rule: every applied decision today leaves a standing
                   block, and the next run stops on it. Round trips —
                   one dead run per decision.

---

### 3

    Fichier      : .claude/agents/cadreur.md, and .claude/commands/7_lots.md
    Cible        : Agent: "When you cannot produce" (lines 110-114) and
                   block D; command: the after-table row "blocked_cadreur.md
                   and architecte/cadreur.md → invoke architecte,
                   invocation 3, then invoke cadreur again" (line 86)
    Aujourd'hui  : The agent says the `## Decision` heading "is the
                   only way this block ever lifts" and that the Product
                   Owner writes it. On a conventions shortfall the
                   command sends the pair to the Architecte and brings
                   the cadreur back. The Architecte writes into
                   `architecte/cadreur.md` (its `## Verdict`); nothing
                   in either file says who fills or closes
                   `code/blocked_cadreur.md`. On its return the cadreur
                   finds a blocking file with an empty Decision and,
                   per block D, stops. The command's row tests only the
                   presence of `architecte/cadreur.md`, not the state
                   of its `## Verdict`.
    Le défaut    : Plane 2, question 3 — a resume path that does not
                   resume. Command question 1 — a row whose outcome
                   cannot occur as described. Also: a request from an
                   earlier run whose Verdict is already filled, plus a
                   new block for an unrelated reason (third round),
                   matches the row and goes to the Architecte for
                   nothing.
    Ce qu'il faut: The agent must know what lifts a conventions block:
                   on entry, a blocking file whose `## Where` names a
                   request in `architecte/` with a filled `## Verdict`
                   is lifted by that verdict (accepted → carry on with
                   the convention as amended; refused → the block
                   stands and needs the Product Owner), and the file is
                   closed the same way a decided one is. The command's
                   row must test an empty `## Verdict` in the request,
                   not the mere presence of the file.
    Justification: Round trips — today the Architecte round is
                   followed by a run that stops immediately, and the
                   Product Owner is asked to write a Decision the
                   Architecte already gave. Robustness — the stale
                   request case sends a third-round block down the
                   wrong path.

---

### 4

    Fichier      : .claude/agents/cadreur.md
    Cible        : "When you cannot produce" (lines 104-108) against
                   "When the conventions fall short" (lines 162-164)
    Aujourd'hui  : The first says a convention that forbids what a lot
                   needs is a blocking case, "you never work around
                   it — not by cutting the lot differently, not by
                   declaring less than it needs". The second offers a
                   fast path: "Can you finish without it? Yes — write
                   the request and carry on, cutting against the
                   conventions as they stand."
    Le défaut    : Plane 2, question 1 — "Can you finish without it?"
                   is not a test two readers apply the same way, and
                   the first passage reads as if the answer is always
                   no. Plane 3, criterion 4.
    Ce qu'il faut: One observable criterion separating the two paths —
                   for instance: the request changes what the lot
                   declares (which module a symbol lives in, whether a
                   symbol may exist at all) → block; the request only
                   asks the conventions to sanction something the lot's
                   declarations already state in full (a library the
                   lot names, a permission it names) → fast path. The
                   first passage then names the block as the case
                   where the declarations themselves depend on the
                   answer.
    Justification: Robustness — read one way, every shortfall blocks
                   and the Product Owner is pulled in for what the
                   Architecte settles; read the other, a lot is cut
                   against a rule that forbids it and the Détailleur
                   inherits the contradiction. Round trips either way.

---

### 5

    Fichier      : .claude/agents/cadreur.md
    Cible        : "When the conventions fall short" — the file name
                   `architecte/cadreur.md` (line 148), and "`##
                   Conventions requests` names each file you wrote in
                   `architecte/`" (lines 639-640)
    Aujourd'hui  : One fixed file name; the output section speaks of
                   "each file", one per line.
    Le défaut    : Plane 2, question 4 — a placeholder with no rule for
                   what fills it when there are two needs in one run,
                   or a need in a later run while an answered request
                   already sits at that name.
    Ce qu'il faut: A rule for the second request: either one file with
                   one block of five headings per need, or numbered
                   files, and what to do when a file with a filled
                   `## Verdict` already stands at the name. Whichever
                   holds, the `## Conventions requests` section names
                   what the rule produces.
    Justification: Robustness — the second need overwrites the first,
                   or the agent reopens an answered request; the
                   Architecte then settles half of what was asked.

---

### 6

    Fichier      : .claude/agents/cadreur.md
    Cible        : "When you cannot produce" (lines 99-102), "Which
                   cycle is this?" (line 250), move 7 (line 495), move
                   9 (line 566), the third round (lines 687-689)
    Aujourd'hui  : Line 99 says "You block only when cutting is
                   impossible — no technical document, no conventions,
                   a document whose sections are not numbered, or one
                   still carrying an `<<ASSUMED` mark", then the
                   conventions case. Three more blocking cases live
                   elsewhere: no technology for a piece (move 7), a
                   listener that cannot be told (move 9), the third
                   round. And one case blocks without a file: a folder
                   carrying both technical documents — "stop and say
                   so" (line 250), while line 95 says "do not merely
                   say it".
    Le défaut    : Plane 3, criterion 2 and 4 — a list introduced by
                   "only" that is not the list. Plane 2, question 3 —
                   the two-documents stop writes nothing, so the
                   command's after-table finds nothing on disk and has
                   no row for it.
    Ce qu'il faut: The blocking cases enumerated once, in the section
                   that owns blocking, and the moves that raise one
                   pointing back at it. The two-documents case writes
                   the blocking file like every other.
    Justification: Robustness — "what is not in the list passes": a
                   reader at move 7 or 9 who trusts the "only" list
                   invents rather than blocks. Round trips — a stop
                   with no file is invisible to the command, which
                   reports a run that produced nothing and cannot say
                   why.

---

### 7

    Fichier      : .claude/agents/cadreur.md
    Cible        : "Which cycle is this?" — "Group by bearer, even
                   across sections" (lines 273-276) against move 4
                   (line 375), move 10 (line 578), "What makes a lot"
                   (lines 62-64) and *What you never do* ("Cite a bare
                   §3, or entries from two sections")
    Aujourd'hui  : The bug-fix section says two entries sharing a
                   bearer are one lot "whatever sections they come
                   from", and that its three differences are "listed
                   here and nowhere else". Every other statement of the
                   one-section rule is absolute, the never-do entry
                   included.
    Le défaut    : Known pattern — two passages asking for different
                   things — and Plane 2, question 4: a reader who
                   scans *What you never do* on a bug-fix run refuses a
                   grouping Part 2 requires. The rule's stated reason
                   ("its nature would be undecided, and a block holds
                   one layer") is then patched by "a single bearer
                   never spans two layers", which is an assumption
                   about the code, not a check.
    Ce qu'il faut: The one-section rule carries its own exception where
                   it is stated (move 10 and the never-do entry): on a
                   `desc-bug.md`, the unit is the bearer and a lot's
                   layer is the bearer's. And a check, not an
                   assumption: a bearer whose entries would put it in
                   two layers is a blocking case, not a fact declared
                   impossible.
    Justification: Robustness — the never-do list is what an agent
                   reads last and trusts most. Round trips — whether
                   the vérificateur accepts a cross-section anchor on a
                   bug fix is not visible from here (see the last
                   section); if it does not, every bug-fix lot comes
                   back as a defect.

---

### 8

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 4's table, row "§1 Model, §2 Persistence |
                   Entity, with its table and its migration" (line
                   367) against the one-section rule
    Aujourd'hui  : The row reads as one lot per entity spanning the
                   model entry (§1) and its persistence entry (§2) —
                   which the rule forbids — or as "each of these two
                   sections yields one lot per entity", which would
                   make two lots for one entity and its table.
    Le défaut    : Plane 2, question 4 — an instruction that reads two
                   ways, on the first row the agent applies.
    Ce qu'il faut: Say which: two rows, one per section, each with its
                   own unit; or, if an entity and its table are meant
                   to be one lot, the one-section rule must say so as
                   an exception and the vérificateur must know it.
    Justification: Round trips — read the first way, the first defect
                   of every split is a §1/§2 anchor; read the second,
                   the entity lot and the table lot are ordered only
                   if the second declares a need on the first, which
                   nothing here asks for.

---

### 9

    Fichier      : .claude/agents/cadreur.md
    Cible        : "What makes a lot" — the third constraint and its
                   table (lines 70-89)
    Aujourd'hui  : A lot's size is judged by "a lot so large that four
                   of its kind would not fit in a block", and a block
                   is defined in the same table as a count of lots per
                   layer (3-4 for screens). The only per-lot measure is
                   a prose column ("what a lot adds in reading").
    Le défaut    : Plane 2, question 1 — two readers cannot check the
                   test the same way: the size of a lot is expressed in
                   blocks and the size of a block in lots. For screens
                   the test is met by construction. The known pattern
                   "more context than one agent holds — it degrades
                   instead of stopping" is exactly what this constraint
                   is meant to prevent, and it has no measurable edge.
    Ce qu'il faut: One observable bound per lot, counted from what the
                   lot declares — entries cited, symbols in the three
                   fields, files in `Modifies` — with the ceiling per
                   layer expressed in that unit. The block table stays
                   as what the vérificateur groups by, not as the
                   cadreur's ruler.
    Justification: Robustness — this is the one constraint the agent
                   says "nothing downstream can fix", and it is the
                   one with no test.

---

### 10

    Fichier      : .claude/agents/cadreur.md
    Cible        : "What you write" — "Then five fields per lot" (line
                   625) and the example that follows; move 7, "Its
                   identifier says what it is — the contract's name
                   plus what realises it" (lines 502-503)
    Aujourd'hui  : The example shows four fields: Anchor, Needs,
                   Produces, Modifies. Move 7 asks each piece lot to
                   carry an identifier, and no field holds one — lots
                   are `## lot-NN`.
    Le défaut    : Plane 2, question 4 — a count that no longer matches
                   what follows it, and a move (7) writing into a field
                   that does not exist.
    Ce qu'il faut: Four fields, or the fifth named and shown — and if
                   the fifth is a name or a layer, move 7's identifier
                   goes there and the vérificateur can read the layer
                   from it rather than infer it from the section.
    Justification: Robustness — the agent invents a fifth field, or
                   the vérificateur looks for one; either way the file
                   format is not the one the next reader parses.

---

### 11

    Fichier      : .claude/agents/cadreur.md
    Cible        : The unit of `Modifies` — move 5 (line 393: "A symbol
                   is a name the code carries… Not a file"), move 6
                   (line 428: "Every file the grep returns goes into
                   the lot's `Modifies`, by name"), move 8 (line 544:
                   "The lot carries the declaration"), and the
                   constraint "Two lots never touch the same symbol…
                   The same file is allowed" (lines 66-68)
    Aujourd'hui  : `Modifies` holds symbols by move 5, files by move 6,
                   and manifest or build-file lines by move 8 that are
                   neither. The collision rule is on symbols and
                   explicitly not on files.
    Le défaut    : Plane 2, question 4 — the field has no unit, so the
                   rule the vérificateur checks on it ("two lots never
                   touch the same symbol") cannot be applied uniformly:
                   a file named in one lot and a symbol that file holds
                   named in another is a collision nobody sees.
    Ce qu'il faut: One unit for `Modifies`, or two fields — the symbols
                   a lot changes, and the files it has to touch that
                   declare no symbol (a test file, a manifest, a build
                   file). The collision rule applies to the first; the
                   second is what the Réalisateur must own.
    Justification: Robustness — the collision check is the reason two
                   lots can be coded in sequence without one breaking
                   the other; a mixed field lets a collision through.

---

### 12

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 3, "Move 5 says how you find them" (line 342)
    Aujourd'hui  : Points to move 5 for how pieces are found. Move 7
                   holds that ("Find the pieces the rules need").
    Le défaut    : Plane 2, question 4 — a cross-reference that no
                   longer matches.
    Ce qu'il faut: The pointer names move 7.
    Justification: Round trips — a reader at move 5 finds nothing about
                   pieces and either drops the inventory line or
                   invents the test.

---

### 13

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 3's table, last row (line 352: "Nothing — and
                   say so; an entry asking for what is there is a
                   defect"); move 10's `## Entries with no lot` (lines
                   583-595); "Write the file even when a section yields
                   no lot — say so with a line" (line 656) against "No
                   prose between lots" (line 647)
    Aujourd'hui  : "Say so" names no place. `## Entries with no lot`
                   gives one example reason (carried by other entries)
                   and does not list "already carried by the code". A
                   section with no lot gets "a line", which the no-prose
                   rule forbids between lots, and which is redundant if
                   each of its entries is already in the no-lot list.
    Le défaut    : Plane 1 — a move whose result nothing carries
                   forward. Plane 2, question 4 — a place unnamed, two
                   passages at odds on the section line. And "is a
                   defect" names no one who acts on it: the agent may
                   not flag ("Blocking is not flagging").
    Ce qu'il faut: The already-carried case lands in `## Entries with
                   no lot` with that reason, so the Détailleur and the
                   Contrôleur know the entry is satisfied rather than
                   forgotten. Whether an entry asking for what exists
                   is reported upstream, and where, is decided here or
                   dropped. The "section yields no lot" line either is
                   that list or goes.
    Justification: Robustness — the Contrôleur confronts every block
                   against the sheets; an entry satisfied by existing
                   code and recorded nowhere reads as a gap. Tokens —
                   the redundant line is nothing; the missing record
                   costs a correction cycle.

---

### 14

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 3, "Grep each symbol as you note it" (line 344)
                   and move 6, "Grep the callers of every symbol
                   declared modified" (line 411)
    Aujourd'hui  : Move 3 greps every symbol's name across the code
                   folders to know whether it exists and what it
                   carries. Move 6 greps the same name again, in the
                   same folders plus tests, for its callers. A grep on
                   a name returns its callers along with its
                   declaration; the second grep returns the first's
                   hits.
    Le défaut    : Plane 2, question 2 — the same thing read twice,
                   paid at every invocation, on the agent's most
                   frequent operation.
    Ce qu'il faut: Move 3 greps once, on the code and test folders,
                   and keeps the hit list per symbol; move 6 classifies
                   those hits (declaration, caller, fulfilment,
                   look-alike, test) for the symbols the lot modifies,
                   grepping again only where a name was not in the
                   inventory (a listener, a piece).
    Justification: Tokens — the inventory is "a symbol named in eleven
                   entries" wide; halving the greps on it is the
                   largest saving this agent has. Robustness — one hit
                   list means move 6 cannot find fewer callers than
                   move 3 saw.

---

### 15

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 6's caller table, row 2 (line 467: "Another lot
                   removes the call as part of its own change —
                   Nothing; that lot already declares it, and runs
                   first"), against lines 474-476
    Aujourd'hui  : The row rests on the removing lot running first.
                   Nine lines later the agent states the principle
                   that breaks it: when two lots are tied by nothing,
                   "neither consumes the other's production, so nothing
                   orders them". The lot changing the signature
                   declares no need on the lot removing the call; the
                   vérificateur derives order from declarations.
    Le défaut    : Plane 2, question 1 — the move claims an order it
                   does not produce. Plane 3, criterion 4.
    Ce qu'il faut: The row must produce the order it relies on: the
                   signature lot declares a need on the removing lot
                   (or the removing lot is declared as what makes the
                   change buildable), so the sequence carries it.
    Justification: Robustness — sequenced the other way, the module is
                   uncompilable after the first lot and the Réalisateur
                   meets a caller no lot owns — the exact failure move
                   6 exists to prevent.

---

### 16

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 6, "A lot changing a mechanism changes what its
                   callers need… The test, on each caller: what it
                   holds today, does the new mechanism accept it?"
                   (lines 457-462), under "Grep, never a file read"
    Aujourd'hui  : The test asks what each caller holds. A grep hit is
                   a line; what a caller holds is usually not on the
                   line that names the symbol.
    Le défaut    : Plane 2, question 2 — a move resting on a fact its
                   reads do not give it: it will guess, or open the
                   file the never-do list forbids.
    Ce qu'il faut: Bound the test to what a hit shows, and name the
                   default when it does not settle: a caller the grep
                   cannot clear is declared a modification (the
                   conservative side — a declared file that needed no
                   change costs the Réalisateur a look; an undeclared
                   one costs a build).
    Justification: Robustness — the choice between guessing and a
                   forbidden read is made silently today; a stated
                   default makes both readers land in the same place.

---

### 17

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 9, "Nothing listens for it and no lot builds
                   one → a lot produces it, and the entries say what it
                   has to emit" (lines 564-566); move 7's third row on
                   what an entry obliges to exist (line 522: "cut a lot
                   for it, or report the split cannot carry this entry")
    Aujourd'hui  : "A lot produces it" — the rule's own lot, or a new
                   one? With what anchor, in which section, at what
                   layer? Move 7 answers all of that for pieces (own
                   lot, same entry, the platform module) and nothing
                   answers it for listeners. Move 7's third row offers
                   two outcomes ("cut a lot" / "report") with no test
                   choosing between them.
    Le défaut    : Plane 2, question 1 (two readers cut differently)
                   and question 3 (the "or report" branch is not a
                   blocking case named anywhere, so it has no file).
    Ce qu'il faut: A listener lot is cut like a piece: its own lot when
                   it belongs to another layer, the rule's lot
                   otherwise; it cites the entry naming the trigger and
                   needs the rule. Move 7's third row names the test
                   that separates "cut" from "report", and "report"
                   means the blocking file.
    Justification: Robustness — a listener folded into a domain lot
                   crosses the layer boundary the whole file guards;
                   an entry "reported" without a file is the same
                   unrecorded stop as comment 6.

---

### 18

    Fichier      : .claude/agents/cadreur.md
    Cible        : "Then call the Vérificateur, and wait" — the table
                   on what comes back (lines 680-685)
    Aujourd'hui  : Two rows: `## Defects` empty, or defects. The command
                   knows a third outcome — `code/blocked_verificateur.md`
                   ("There was nothing to check") — and the agent's
                   table has no row for a missing `code/sequence.md`.
    Le défaut    : Plane 2, question 3 — a situation the move cannot
                   handle and does not foresee; the agent would read a
                   file that is not there.
    Ce qu'il faut: A row for the vérificateur having blocked: the
                   cadreur goes out without correcting, since what the
                   vérificateur blocks on is not a defect in a lot.
    Justification: Round trips — an unforeseen return is an invented
                   one; the agent may re-run the vérificateur on the
                   same unreadable split and burn a round.

---

### 19

    Fichier      : .claude/agents/cadreur.md
    Cible        : Block C (lines 724-781); *What you never do*, "Run
                   the ten moves on a take-back or a redécoupage"
    Aujourd'hui  : Block C says what to read, which lots are closed,
                   how to number, and what to write at the end of
                   `code/redecoupage.md`. It does not say that the
                   vérificateur is called once the lots are added —
                   the command relies on it ("the Vérificateur keeps
                   them where they ran and archives the file when the
                   sequence is written"), and block B says "everything
                   else of block A applies" while C says nothing. And
                   a lot added on a redécoupage needs moves 5 to 10 run
                   on it (declarations, callers, pieces, anchors) — the
                   never-do entry forbids "the ten moves" without
                   distinguishing the whole document from the lot added.
    Le défaut    : Plane 2, question 4 — a reader who has seen nothing
                   else does not know C ends in a vérificateur round;
                   question 1 — "the ten moves" reaches further than it
                   should (it should forbid re-cutting, not
                   declaring).
    Ce qu'il faut: C states that it ends as A does — the vérificateur
                   is called, the rounds are counted — and that moves
                   5 to 10 apply to every lot added or changed, while
                   moves 3 and 4 are not re-run over the document. The
                   never-do entry says the same.
    Justification: Robustness — a redécoupage split never checked is
                   never sequenced; the command then finds the old
                   `code/sequence.md` without defects and reports "the
                   split holds". A lot added without move 6 carries
                   undeclared callers, which is the defect that sent
                   the split back in the first place.

---

### 20

    Fichier      : .claude/agents/cadreur.md
    Cible        : Move 5 (line 404: "`ViewModel`, a Room annotation, a
                   base widget"), move 6 (lines 447-453: "A `when` that
                   exhausts it", "the replacement annotation"), the
                   layer table (line 75-81: Models, Services,
                   Repositories, Providers, Screens)
    Aujourd'hui  : Rules stated in the words of one language and one
                   framework. CLAUDE.md says the chain runs on several
                   projects.
    Le défaut    : Plane 3, criterion 6 (and 5 for the examples). A
                   reader on a project with no `when` and no
                   "Providers" layer either skips the rule or maps it
                   by guess.
    Ce qu'il faut: The look-alike rule in universal terms — an
                   exhaustive match on the type, a test double
                   standing in for it, an implementation of its
                   interface; the framework-type rule without the
                   product names; the layer table's rows named by what
                   the conventions call the layers, or by role
                   (persistence, domain, state, presentation).
    Justification: Robustness — a rule the reader cannot map is a rule
                   not applied, and the look-alike rule is the one that
                   finds what "no caller-grep finds".

---

### 21

    Fichier      : .claude/agents/cadreur.md
    Cible        : Rules stated more than once: the caller-grep rule
                   (never-do entry; lines 418-421; lines 423-426 with
                   "measured: five test files…"); "do not argue with a
                   defect" (never-do; 691-692; 708-709); the three-round
                   ceiling (24-26; 198; 687-689; and twice in the
                   command); "no ten moves on B/C/D" (201-202; 240-243;
                   719-720); the unbounded wait (197; 677-678); "look
                   for the blocking file first" (223-233; 786); "Read
                   it in full" (295; 357)
    Aujourd'hui  : Each rule is stated two to four times, several with
                   a justification or an anecdote attached.
    Le défaut    : Plane 3, criterion 5. Every invocation — including
                   B and D, which use a fraction of the file — loads
                   813 lines on `opus`.
    Ce qu'il faut: Each rule once, where it applies; the never-do list
                   as the index of them, not a second statement. The
                   "measured" anecdotes and the "why" sentences go.
    Justification: Tokens — the duplicated passages are roughly a
                   fifth of the file, paid on every run and on every
                   verificateur round the cadreur survives.

---

### 22

    Fichier      : .claude/agents/cadreur.md
    Cible        : *What you never do* against the body: "Never the
                   product file, either grid, or any questions file"
                   (line 313) and "Every code search targets the code
                   folders the conventions name… never a bare pattern"
                   (lines 306-311)
    Aujourd'hui  : Two 🔴 rules in the body with no entry in the list;
                   the list is otherwise a faithful index.
    Le défaut    : Known pattern — a rule in the body with no matching
                   entry.
    Ce qu'il faut: Once comment 21 makes the list the index, these two
                   are in it.
    Justification: Tokens — a bare grep sweeps `docs/` and the build
                   output on every symbol; the list is where that rule
                   is looked up.

---

### 23

    Fichier      : .claude/commands/7_lots.md
    Cible        : Lines 64-67 ("Say so in the prompt of both agents,
                   and name the file") against lines 151-154 ("The
                   Cadreur finds by itself what brought it back… Say
                   nothing about it in the prompt") and lines 78-79
                   ("You do not run `verificateur`")
    Aujourd'hui  : On a redécoupage the command must add a sentence to
                   the prompt of "both agents"; the command invokes one
                   agent; and forty lines later it must say nothing
                   about a `code/redecoupage.md` in the prompt.
    Le défaut    : Two passages asking for different things, in the
                   command; and "both agents" names an invocation the
                   command does not make (the cadreur's own
                   vérificateur prompt template carries no such line).
    Ce qu'il faut: One rule. Since the agent's Part 2 already
                   dispatches on `code/redecoupage.md`, the prompt
                   carries nothing; if the vérificateur needs the
                   sentence, the cadreur's template is where it goes.
    Justification: Round trips — the orchestrator obeys one passage or
                   the other; whichever it picks, half the file says it
                   was wrong, and a paraphrase "competes with" the
                   agent's own instructions by the command's own words.

---

### 24

    Fichier      : .claude/commands/7_lots.md
    Cible        : "How it runs" — "This command always produces a
                   split" (line 42) and its "On disk" table (lines
                   48-52)
    Aujourd'hui  : Three rows: nothing, `## Defects`, `code/redecoupage.md`.
                   The agent's Part 2 has a fourth state (a blocking
                   file, with its Decision empty or filled), on which
                   the agent either stops or applies a decision — and
                   the after-table (line 87) itself says "the Cadreur
                   reads it on its next run". "Always produces a
                   split" is false on the empty-Decision run.
    Le défaut    : Command question 1 — a case with no row; and a
                   sentence that a foreseen case contradicts.
    Ce qu'il faut: The table lists the blocking-file states with what
                   the agent does on each, and "always produces a
                   split" is scoped to the states where it can.
    Justification: Round trips — the orchestrator that reads only this
                   table, on a folder with a standing block, expects a
                   split and gets a stop it has no row for.

---

### 25

    Fichier      : .claude/commands/7_lots.md
    Cible        : "What you read" (lines 31-33: `code/sequence.md`,
                   "and only its `## Defects` section") against "What
                   you relay" (line 208: "how many lots, how many
                   blocks")
    Aujourd'hui  : The blocks are in the sequence the vérificateur
                   writes, outside `## Defects`; the lot count is in
                   `code/decoupage.md`, which the command does not
                   read at all.
    Le défaut    : Two passages at odds: what is relayed is not in what
                   is read.
    Ce qu'il faut: Either the reading list names what the counts come
                   from (the sequence's headings, the lot headings), or
                   the relay drops the counts and names the files.
    Justification: Round trips — the orchestrator either breaks the
                   reading rule or reports without the numbers and the
                   Product Owner opens the files herself.

---

### 26

    Fichier      : .claude/commands/cycle.md
    Cible        : Routing table row 7 (line 88: "`cadreur` or
                   `verificateur` → `/7_decoupe`"), rows 12-13, and
                   the chain named at lines 9-10
    Aujourd'hui  : The command that runs the cadreur is `/7_lots`; the
                   table routes to `/7_decoupe`, and the chain names
                   `/1_structure`, `/2_grille`, `/3_reclasse`,
                   `/4_convertit` — none of which is in
                   `.claude/commands/`.
    Le défaut    : Command question 1 — "what it says to run next" is
                   a command that does not exist. At the edge of this
                   pass (cycle does not invoke the cadreur); noted
                   because it is the route by which a cadreur decision
                   is resumed in chained mode.
    Ce qu'il faut: The routing table names the commands as they are
                   named on disk.
    Justification: Round trips — a resumed cadreur block in `/cycle`
                   stops on an unknown command and the Product Owner
                   has to find the right one.

## From the verdict

Read after everything above: section 2's cadreur line, sections 4 to 7.
One entry per item that names the cadreur. Section 1 and section 3
mention it too and were not read.

    Section 2 — "the role holds"; keeping its context across
    vérificateur rounds is "the right exception to the fresh-eyes rule".
    Already found in substance — nothing above asks to change the role.
    One addition the verdict could not see: the exception is undercut by
    block B, which re-enters the same loop from cold, with nothing in
    context, whenever `/7_lots` is run again by hand.

    Sweep rows 28, 31, 47, 48, 53 — the cadreur reads the technical
    document whole, the conventions whole, writes `code/decoupage.md`,
    reads `## Defects` in `code/sequence.md`, reads `code/redecoupage.md`.
    Confirmed by the agent, line for line.

    Sweep row 34 — `architecte/<demande>.md` with `## Verdict`, read by
    "the author".
    Contradicted by the agent: nothing in `cadreur.md` says the cadreur
    ever reads the `## Verdict` of a request it wrote. The file is named
    once as something written (line 148) and once as something to list
    (line 639). Comment 3 above.

    Sweep row 44 — `desc-bug.md`, "carrier per entry", read by the
    cadreur.
    Confirmed: "Each entry names a `Bearer:`" (line 259).

    Sweep row 46 / D18 / section 7 item 5 — the symbol inventory "is not
    a named file"; if it lives only in the cadreur's context the
    vérificateur's first defect class is ratification.
    Contradicted by the agent: "Write it into `code/decoupage.md`,
    before the lots" (line 354), and the output shape opens with a
    `## Symbols` section (lines 603-616). D18 closes on the cadreur's
    side. Whether the vérificateur reads that section is another file's
    to settle (below).

    Sweep row 55 / D21 / P11 / section 7 item 3 — does the cadreur read
    `CURRENT_TECHNICAL_STATE.md`? "Ce document commande le Cadreur".
    Contradicted by the agent: the file is named nowhere in
    `cadreur.md`. Its reading list is the technical document, the
    conventions, and the code by grep (lines 295-302). So the verdict's
    "No" branch is the true one: production or modification is declared
    from grep alone, and the sentence the verdict quotes describes an
    agent that does not exist. P11's "a Cadreur that reads a description
    of what exists rather than the code" is false in the same way — the
    cadreur reads the code, by grep.

    D17 / section 7 item 13 — rename or delete a settled blocking file;
    the cadreur renames.
    Confirmed: block D renames to `code/blocked_cadreur-NN.md` and
    forbids deleting (lines 794-812). And found beyond it: the cadreur
    cannot rename with the tools its frontmatter gives it (comment 2).
    The verdict weighs rename against delete; the agent as written can
    do neither.

    A7 / P4 — grep is knowledge; "the closest callers declare nothing of
    its origin" is answered with "grep the name".
    Confirmed: the never-do entry and move 6 (lines 418-426). Found
    beyond it: one test in move 6 needs what a grep line does not show —
    "what a caller holds today, does the new mechanism accept it" —
    and the agent gives no default when the grep does not settle it
    (comment 16).

    U11 / section 7 item 17 — is there a bound on the cadreur re-blocking
    with the same convention request after an Architecte refusal?
    Not found. The agent says nothing about a refusal: "you never work
    around it" (line 105) and "the only way this block ever lifts" is
    the Product Owner's `## Decision` (lines 134-136). Taken literally,
    the cadreur does not re-block after a refusal — it never sees the
    refusal, because it never reads the verdict (comment 3); on its
    return it finds its own blocking file with an empty Decision and
    stops. So U11 is not an unbounded loop but a dead end that reaches
    the person on the first pass, with a wasted Architecte round in
    between. What the person would need to know — that the Architecte
    refused, and why — is in a file the command does not relay.

    A-1 — Cadreur ⇄ Vérificateur, three rounds, "sound".
    Confirmed for the count. Found beyond it: the return table has no
    row for a vérificateur that blocked instead of writing a sequence
    (comment 18), and block C never says the loop runs at all
    (comment 19).

    A-6 — redécoupage, "the loop without a ceiling"; the convergence
    mechanism is the cadreur's "ce qu'il en fait", a judgement.
    Confirmed by the agent: block C counts nothing; its closest thing to
    a bound is "say it in your report too, when something is on its
    third return" (line 779) — a report line, not a stop. Nothing above
    proposes the ceiling: it would be a rule about what the command does
    on the Nth `code/redecoupage-NN.md`, and that is the command's or the
    group pass's, not a correction to a move.

    P2 — the cadreur's "one section per lot".
    Confirmed for a feature; contradicted on a bug fix: "Group by bearer,
    even across sections… whatever sections they come from" (lines
    273-276). The premise the verdict names is not universal in the
    agent, and the exception is stated where the rule's readers do not
    look (comment 7).

    P3 / P13 — the cadreur reads the technical document whole; the
    failure of a context that runs out "is silent truncation, not a
    block".
    Confirmed: no rule in the agent foresees a document too large to
    read whole. Not made a comment above: the agent cannot measure its
    own context, and the stop would have to be a size rule on the
    document, which is the Convertisseur's or the command's to place.

    P9 — the one place the fresh-context premise is inverted is the
    cadreur, "argued".
    Confirmed: lines 664-666 give the argument. See section 2's entry
    for block B.

## What another agent would settle

    Does the vérificateur accept a lot whose anchors span two sections
    when the document is `desc-bug.md`?
    `verificateur.md`.
    Yes: comment 7 is only a matter of where the exception is stated.
    No: every bug-fix lot with two bearers' worth of entries comes back
    as a defect, and three rounds cannot converge — the bug-fix cycle
    cannot be split at all.

    Does the vérificateur read the `## Symbols` section of
    `code/decoupage.md`, and check the lots' declarations against it?
    `verificateur.md`.
    Yes: D18 closes entirely and the inventory earns its place in the
    file. No: the inventory is written for nobody but the cadreur, and
    it should either be read there or not written to disk (tokens).

    Do the vérificateur's defects name every lot a fix has to touch —
    both lots of a symbol collision, the lot that should cite an
    orphaned entry?
    `verificateur.md`.
    Yes: "fix only the lots named" is workable. No: the cadreur has to
    touch an unnamed lot to fix a named one, and its own never-do entry
    forbids it — it either breaks the rule or leaves the defect for the
    next round.

    On what does the vérificateur block, and what does it write?
    `verificateur.md`.
    Only on a missing or unreadable `code/decoupage.md`: the command's
    "There was nothing to check" holds, and the cadreur's return table
    needs one extra row (comment 18). On more than that: the row needs
    a test, and some of those cases may be defects the cadreur should
    correct rather than stops.

    Does the vérificateur derive a lot's layer from its section number,
    or from a field of the lot?
    `verificateur.md`.
    From the section: the four fields suffice and comment 10 resolves as
    "four, not five". From a field: that field is the missing fifth, and
    the cadreur has to write it.

    Does the vérificateur's collision check read `Modifies` as symbols,
    files, or both?
    `verificateur.md`.
    Symbols only: the files move 6 puts there are invisible to it and
    two lots can name the same test file with the same symbol
    (comment 11 stands). Both: the same file allowed in two lots (line
    67) is flagged as a collision, and the rule and the check disagree.

    Does the Architecte's invocation 3 touch `code/blocked_cadreur.md` —
    fill its `## Decision`, rename it, or leave it?
    `architecte.md`.
    Fills or renames it: comment 3's dead end closes on the Architecte's
    side, and the cadreur only needs to know what it will find. Leaves
    it: the cadreur's next run stops on an empty Decision after every
    Architecte round, and comment 3 is the fix.

    What does the Architecte write on a refusal, and where?
    `architecte.md`.
    A `## Verdict` saying so, in the request: the cadreur can read it
    and the command can relay it. Nothing distinguishable from an
    acceptance: the cadreur cannot tell whether to carry on or stand,
    and U11 becomes what the verdict feared.

    What does `code/redecoupage.md` carry, and does the Arbitre name the
    lot in hand and expect the two French headings the cadreur appends?
    `arbitre.md`.
    Names the lot and expects the sections: block C is complete as read.
    Neither: "the one in hand" (line 740) is a reference to something
    the cadreur has no way to find, and the appended sections are read
    by nobody but the next cadreur.

    Does the Détailleur, or the Contrôleur, read `## Entries with no
    lot`?
    `detailleur.md`, `controleur.md`.
    Yes: comment 13's "already carried by the code" reason is what
    keeps a satisfied entry from reading as a gap. No: the section is a
    record for the person only, and the reason column matters less.

    Does `desc-bug.md`, as the Diagnostiqueur writes it, carry numbered
    sections, a preamble with `Out of scope`, and possibly `<<ASSUMED`
    marks?
    `diagnostiqueur.md`.
    Yes: "everything else is identical: same moves" (line 284) holds.
    No: moves 1 and 2 have nothing to act on and the "sections not
    numbered" blocking case fires on every bug-fix document.

    Are the technical document's section titles the ones move 4's table
    lists (§7 Presentation, §9 Text), and is there a section the table
    does not name?
    `convertisseur.md`.
    Same titles, same nine: the table maps. A section missing from the
    table: its entries have no "one lot per" rule and the cadreur cuts
    them by guess.

    Does the Détailleur or the Réalisateur read `code/decoupage.md`'s
    `Modifies` as a list of files it owns?
    `detailleur.md`, `realisateur.md`.
    Yes: the unit question (comment 11) matters downstream too — a
    symbol name there is not a file the Réalisateur can open. No: the
    field's unit only matters to the vérificateur.

