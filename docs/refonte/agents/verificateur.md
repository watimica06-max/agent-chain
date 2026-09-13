# Pass on `verificateur`

Files read: `.claude/agents/verificateur.md` (whole); `.claude/commands/7_lots.md`
(whole — the only command on the path to this agent, through the Cadreur);
`.claude/commands/cycle.md` and `.claude/commands/audit_blocages.md` (whole —
both name the agent, neither invokes it); `docs/refonte/verdict.md` §4–7 and
the agent's line in §2, read last.

Role, from the file: the Vérificateur checks that the lot list the Cadreur
just wrote holds against the technical document — crossing the symbol
inventory against the lots, confronting each lot with the entries it cites,
deriving the execution order mechanically and grouping the lots into blocks —
and writes `code/sequence.md`, which drives the coding loop; it reports
defects and never corrects; it is invoked by the Cadreur, up to three times
on one split, on a fresh context each time.

Moves, in the order the file runs them:

| # | Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|---|
| 0 | Look for `code/blocked_verificateur.md`, apply a filled decision | Resume after a block | Itself (re-runs the six moves) | — but see comment 8: nothing it applies exists |
| 1 | Cross the `## Symbols` inventory against the lots (seven defect kinds) | Catches what names alone miss: surfaces, holes, overlaps, orphans, dead productions, undeclared callers, uncascaded contracts | `## Defects` → Cadreur | Kinds 6 and 7 are one check at two granularities (comment 10) |
| 2 | Record what orders lots without a `Needs` line | Order is incomplete without modifications and both-ends changes | Move 4 | Its "coded lot first" clause is an order rule, not a dependency (comment 12) |
| 3 | Open each cited entry and confront section, announcement, coverage | Protects the Détailleur from a false anchor | `## Defects` → Cadreur | — |
| 4 | Derive the order topologically, mechanical tie-break | The sequence itself | `## Order` → Cadreur, `/8_code` | — |
| 5 | Group into blocks under per-layer ceilings | Shared reading per block | `## Blocks` → `/8_code` | — |
| 6 | On a redécoupage, archive `code/redecoupage.md` | The next redécoupage must see what already came back | The next redécoupage | — |
| — | Write `code/sequence.md`; write `code/blocked_verificateur.md` when the lot list is missing | Output; stop | Cadreur, command | — |

Judgement on the set: the six moves cover the role and are in a workable
order (inventory → undeclared orderings → entries → order → blocks → archive).
Two things do not hold at the set level. The redécoupage handling is spread
over "What you read", moves 2, 5 and 6, and moves 1 and 3 say nothing about
coded lots although the file says they are treated differently (comment 5).
The blocking machinery of Part 2 (decision, rename, numbered files, "run the
six moves again") serves a block whose only named cause admits no decision
(comment 8). One read — the `## Status` line of coded lots' verdicts — feeds
no move (comment 4). Move 6 runs at the wrong moment of the loop
(comment 19).

---

## Comments, in order of application

### 1

    Fichier      : .claude/agents/verificateur.md
    Cible        : frontmatter `tools`; Part 2 "When you resume after a
                   blocking file" (rename with `git mv`, "Delete the file
                   once applied"); move 6 (rename `code/redecoupage.md`);
                   section "When `Edit` fails"
    Aujourd'hui  : `tools: Read, Grep, Glob, Edit, Write`. The body asks for
                   three file renames or deletions ("Renaming means renaming
                   — git mv, or the equivalent: one file, under a new name.
                   Never write the numbered one and leave something at the
                   old name — not a copy, not a note, not an empty file"),
                   and carries a section on `Edit` failures although no move
                   edits a file — every output is written whole.
    Le défaut    : Plane 2, question 2 (can it do it with what it has) and
                   question 3 (what happens when it cannot). With Read, Grep,
                   Glob, Edit and Write an agent can create and overwrite
                   files; it cannot move or delete one. Every rename the file
                   demands ends with something left at the old name — the
                   exact outcome the file forbids — or with the agent
                   inventing a workaround. `Edit` is granted and never used,
                   and its failure section is read at every invocation for
                   nothing.
    Ce qu'il faut: The renames the body asks for and the tools the
                   frontmatter grants must agree. Either the agent gets a tool
                   that moves and deletes files, or the archiving and
                   renumbering are done by the party that has one (the
                   Cadreur, or the command after the Cadreur hands back), and
                   the agent's body stops asking for what it cannot do. If
                   `Edit` stays unused, the tool and its failure section go.
    Justification: Robustness — a `redecoupage.md` or an unnumbered
                   `blocked_verificateur.md` left behind is read by the next
                   run as a live redécoupage or a standing block, and the
                   run takes the wrong branch. Tokens — a tool section read
                   at every invocation for a tool never used.

### 2

    Fichier      : .claude/agents/verificateur.md
    Cible        : Role section, the paragraph "A path starting with `docs/`
                   is relative to the repository root, not to the working
                   folder — the conventions and the state document are
                   shared by the whole repository"
    Aujourd'hui  : That paragraph, right after "Every path below is relative
                   to [the working folder]" and "Relative, always —
                   `docs/features/…`".
    Le défaut    : Plane 3, criteria 3 and 5. The agent opens no file under
                   `docs/` that is not under the working folder — "Nothing
                   else. Not the code, not the state document" — so the rule
                   guards nothing, and its justification names two documents
                   the agent never reads. It also leaves two path rules
                   standing side by side for a reader to reconcile.
    Ce qu'il faut: One path rule: every path in the file is relative to the
                   working folder. Nothing about the repository root.
    Justification: Tokens — a rule paid at every invocation that no move
                   uses. Round trips, marginally — a reader reconciling two
                   path rules before starting.

### 3

    Fichier      : .claude/agents/verificateur.md
    Cible        : "What you read", the line "The `## Symbols` inventory
                   comes first — it is what the lots are checked against"
    Aujourd'hui  : The inventory is named by heading only; no file is named.
                   Move 1 rests entirely on it ("an operation the inventory
                   lists", "the inventory marks it as such").
    Le défaut    : Plane 2, question 4 — a file named without a path; a
                   reader who has seen nothing else does not know whether
                   `## Symbols` sits in `code/decoupage.md`, in the technical
                   document's preamble, or in a file of its own.
    Ce qu'il faut: The inventory is named with the file that carries it, in
                   the path table of the Role section alongside the lot list
                   and the sequence.
    Justification: Robustness — move 1 is the check "names alone cannot
                   make"; an agent hunting for its input in the wrong file
                   runs move 1 on nothing or on the wrong list.

### 4

    Fichier      : .claude/agents/verificateur.md
    Cible        : "What you read", the bullet "`code/<lot>/verdict.md`, its
                   `## Status` line only, for the lots that section names —
                   to confirm each still carries PASS"
    Aujourd'hui  : The read is prescribed; no move consumes it. Nothing says
                   what the agent does when a lot listed under `## Ce qui est
                   déjà codé` does not carry PASS — a defect (of which type),
                   a block, or nothing.
    Le défaut    : Plane 2, question 2 (a read no move uses) and question 3
                   (the failing case is unforeseen — the agent invents).
    Ce qu'il faut: Either a move names the case and its outcome — a coded
                   lot whose verdict is not PASS is one more defect kind, or
                   is excluded from the coded set and ordered with the rest —
                   or the read goes. The chosen outcome sits in the move that
                   handles coded lots, not in the reading list.
    Justification: Robustness if kept with an outcome — a lot whose code
                   failed review would otherwise be frozen as "coded and
                   merged" and everything after it ordered against code that
                   is not there. Tokens if dropped — one file per coded lot
                   opened for nothing.

### 5

    Fichier      : .claude/agents/verificateur.md
    Cible        : "What you read" (redécoupage bullet: "what you do with
                   them is not what you do with the rest"), move 1 (all seven
                   kinds), move 3
    Aujourd'hui  : Only moves 2, 5 and 6 say what changes for a coded lot.
                   Move 1's overlap is "two lots naming the same symbol,
                   whether they produce or modify it"; move 2 expects "a lot
                   that modifies what a coded one built". Move 1's "production
                   nobody calls" and "unbuilt surface" apply to coded lots as
                   written. Move 3 confronts every cited entry, coded lot or
                   not.
    Le défaut    : Plane 1 — one job (treating coded lots differently)
                   falling between moves; and the known case "two passages of
                   one agent asking for different things": on every
                   redécoupage, a correcting lot that modifies a coded lot's
                   symbol is an overlap by move 1 and the expected shape by
                   move 2.
    Ce qu'il faut: Each move states what a coded lot is to it. At move 1, a
                   coded lot's productions are in the tree — they count as
                   pre-existing for holes, and a later lot modifying them is
                   not an overlap; a coded lot itself is not re-examined for
                   dead productions or surfaces. At move 3, its entries are
                   not re-confronted (they were coded and merged). The rule
                   lives where the check is, not in the reading list.
    Justification: Round trips — without it, every redécoupage round raises
                   a false overlap on every correction, and the Cadreur
                   answers it three times. Robustness — re-confronting coded
                   entries can send a merged lot back to the split.

### 6

    Fichier      : .claude/agents/verificateur.md
    Cible        : "What you write", the `## Defects` line format ("which
                   lot, which type, what correction is expected")
    Aujourd'hui  : The type field has no vocabulary. The examples use `hole`
                   and `anchor`; move 1 names "unbuilt surface", "hole",
                   "overlap", "orphan entry", "production nobody calls",
                   "caller no lot declares", "contract changed without its
                   cascade"; move 2 ends in "they are one lot — say so as a
                   defect"; move 3 in "badly cut", "missing an anchor", "two
                   lots naming one bearer"; move 4 in a cycle. The first field
                   is "which lot", but an orphan entry belongs to no lot and
                   a cycle belongs to several.
    Le défaut    : Plane 2, question 1 (can two readers check it the same
                   way — two runs will name one defect two ways) and
                   question 4 (a placeholder with no rule for what fills it).
    Ce qu'il faut: One closed list of type names, one per kind the moves
                   raise, stated once where the format is given and used by
                   every move that raises a defect. A rule for the first
                   field when the defect attaches to an entry (the entry
                   number) or to a set of lots (one line per lot, or the set
                   on one line — one rule).
    Justification: Round trips — the Cadreur corrects "only the lots those
                   defects name"; a defect it cannot locate or classify costs
                   a round. Robustness — a defect the agent could not fit the
                   format is one it may leave out.

### 7

    Fichier      : .claude/agents/verificateur.md
    Cible        : "What you write", the rule "The third field quotes the
                   line it contests, as the two examples above do"
    Aujourd'hui  : The two examples ("needs ActivityBudget, produced by no
                   lot — add a lot for it, or declare it pre-existing") carry
                   no visible quotation: nothing marks what is copied from the
                   lot list and what is the expected correction.
    Le défaut    : Plane 3, criterion 4 — two readings: "quote" as verbatim
                   copy, or as mention. The rule's stated purpose ("a quote
                   you cannot find there is a defect that no longer holds")
                   only works under the first.
    Ce qu'il faut: The third field carries a verbatim copy of the contested
                   line, set apart from the correction by a fixed separator
                   or marker, and the examples show it that way.
    Justification: Round trips — the Cadreur's test for a stale defect is a
                   text search; a paraphrase never matches and every defect
                   looks current.

### 8

    Fichier      : .claude/agents/verificateur.md
    Cible        : "When you cannot produce" and Part 2 "When you resume
                   after a blocking file" (the table, "Renaming means
                   renaming", "How you apply it — run all six moves again",
                   "Delete the file once applied")
    Aujourd'hui  : The only named block cause is "the lot list is missing or
                   unreadable — there is nothing to check". The resume
                   protocol then applies a `## Decision` to it, renames the
                   file to `-NN`, re-runs the six moves, and — three lines
                   later — "Delete the file once applied".
    Le défaut    : Plane 1 — a move whose result nothing carries forward: no
                   decision a Product Owner writes makes a missing lot list
                   appear; the lot list is the Cadreur's to produce, and on
                   the next run either it is there (nothing to apply) or it
                   is not (block again). Known case "two passages asking for
                   different things": rename versus delete. Plane 2,
                   question 3: the block reports a malfunction of the step
                   before, not a question.
    Ce qu'il faut: The blocking file says what is missing and where, and
                   stops; it carries no `## Decision` to fill and no resume
                   protocol, because nothing in it is the Product Owner's to
                   settle. Part 2's resume table, the numbering, the
                   rename-or-delete and the "run the six moves again" go with
                   it. If a decision-bearing block case does exist for this
                   agent, it is named, and only then does a resume protocol
                   stay — with one instruction, rename or delete, not both.
    Justification: Round trips — the Product Owner is asked to write a
                   decision she cannot write, and the chain waits on her for
                   a mechanical failure. Tokens — a whole Part 2 section read
                   at every invocation for a path that cannot be taken.

### 9

    Fichier      : .claude/agents/verificateur.md
    Cible        : "When you cannot produce"
    Aujourd'hui  : One case foreseen (lot list missing or unreadable). Not
                   foreseen: the technical document absent, or both
                   `spec-technique.md` and `desc-bug.md` present ("never
                   both"); a cited entry whose number the `^### §` grep does
                   not return; the `## Symbols` inventory absent or empty; a
                   lot with no cited entry at all.
    Le défaut    : Plane 2, question 3 — every situation where the move
                   cannot produce, foreseen with an outcome. Each unnamed one
                   is a place where the agent chooses between block, defect
                   and silence.
    Ce qu'il faut: Each of these has a named outcome: defect (with its type
                   from comment 6) where the Cadreur can correct it — an
                   entry cited that does not exist, a lot citing nothing —
                   and block where nothing can be checked — no technical
                   document, two technical documents, no inventory.
    Justification: Robustness — a lot anchored on a non-existent entry that
                   passes silently reaches the Détailleur, which has to
                   invent the entry's content.

### 10

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 1, kinds "A caller no lot declares" and "A contract
                   changed without its cascade"
    Aujourd'hui  : Kind 6: "a lot changes a signature, and something calling
                   it is named in no `Modifies` field … It shows when the
                   module stops compiling." Kind 7: "a lot modifies a
                   contract and declares nothing that fulfils it, nor
                   anything that calls it … You judge the shape, not the
                   count. Whether four callers is the right number is the
                   Cadreur's to know."
    Le défaut    : Plane 2, question 2 — kind 6 rests on knowing what calls
                   the changed signature, and the agent reads no code and
                   nothing in its reading list names callers; it will guess,
                   or never raise it. Plane 1 overlap — kind 7 is the same
                   defect at the granularity the agent can see (none
                   declared versus some), and says so itself ("that a
                   changed contract declares none of either is a defect you
                   can see"). Plane 3, criterion 6 — "the module stops
                   compiling" is commentary in one toolchain's words.
    Ce qu'il faut: One kind: a changed signature or contract whose lot
                   declares no caller and no fulfiller. If the inventory does
                   carry callers per symbol (a fact the Cadreur's file
                   settles — see the closing section), kind 6 stays and names
                   the inventory as its source; otherwise it goes, and the
                   list says six kinds.
    Justification: Round trips — a kind the agent cannot ground produces
                   guessed defects the Cadreur has to refute. Tokens — two
                   paragraphs for one check.

### 11

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 1, the paragraph "A piece is the exception"
    Aujourd'hui  : It sits after the cascade kind and its "shape, not the
                   count" note, and reads as an exception to the cascade
                   rule. Its content ("no entry names it, and what calls it
                   is the contract it fulfils") excepts a piece from
                   "production nobody calls" (no caller named in `Produces`)
                   and from "orphan entry" (no entry to cite).
    Le défaut    : Plane 2, question 4 — an instruction that reads two ways
                   by its placement; Plane 3, criterion 4.
    Ce qu'il faut: The exception is stated under each kind it excepts, or
                   names those kinds explicitly, so a reader applying kind 5
                   sees it there.
    Justification: Robustness — a piece raised as dead production on every
                   split, or a real uncascaded contract waved through as "a
                   piece".

### 12

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 2, the paragraph "A lot that modifies what a coded
                   one built comes first among what is left"
    Aujourd'hui  : Stated as a position ("comes first"), under a move that
                   records orderings for move 4 to consume as dependencies.
                   Move 4 derives "from the declared dependencies and from
                   what move 2 recorded" through eligibility (needs
                   satisfied) and a layer tie-break. A correcting lot may
                   itself need a symbol an uncoded lot produces; "first" and
                   "eligible" then disagree, and nothing says which wins.
    Le défaut    : Plane 3, criterion 4 — two readings; Plane 2, question 4
                   — move 4's algorithm has no slot for a priority. The file
                   promises "two runs give the same sequence"; here they need
                   not.
    Ce qu'il faut: The rule is expressed in move 4's own terms: either as a
                   dependency (every uncoded lot consuming the corrected
                   symbol needs the correcting lot — which is what the
                   paragraph's second sentence already says) or as the first
                   tie-break among eligible lots. Whichever, a correcting lot
                   that is not eligible is not placed first, and the file
                   says so.
    Justification: Robustness — the order the coding loop runs on must be
                   the same on every run; a rule outside the algorithm makes
                   it depend on the reading.

### 13

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 1 "An overlap" against move 2 "Two lots changing
                   both ends of one call" and move 1 "A contract changed
                   without its cascade"
    Aujourd'hui  : Kind 7 requires a lot changing a contract to declare
                   "anything that calls it". Kind 3 makes "two lots naming
                   the same symbol, whether they produce or modify it" a
                   defect. Move 2 treats the case where one lot changes a
                   signature and another changes the call as legitimate and
                   orders it. If the first lot declares the caller (kind 7
                   satisfied) and the second lot modifies that same caller,
                   both name it and kind 3 fires.
    Le défaut    : Known case "two passages asking for different things";
                   Plane 2, question 1 — the overlap test reaches a case
                   move 2 protects. Whether this actually bites depends on
                   where the Cadreur's format declares a cascade caller — in
                   `Modifies` or as an annotation on the changed symbol — a
                   fact the Cadreur's file settles (closing section).
    Ce qu'il faut: The overlap kind states that a caller declared as the
                   cascade of a changed contract does not count as "naming
                   the symbol" for overlap when another lot modifies that
                   caller — or the format keeps cascade callers out of
                   `Modifies` and the file says where they are read from.
    Justification: Round trips — a false overlap on every signature change
                   whose call site is cut into its own lot, which move 2
                   says is the normal shape.

### 14

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 3 — "§3.1, never §3"; "a lot groups by bearer …
                   two lots naming one bearer"; "Two lots may cite one
                   entry — a contract and the piece that realises it"
    Aujourd'hui  : "Bearer" is used three times and never defined, nor
                   pointed at the document that defines it. A lot citing a
                   section (`§3`) instead of an entry is said to be wrong and
                   is no named defect. Two lots citing one entry is allowed
                   for one case; whether any other double citation is a
                   defect, and of which kind, is not said.
    Le défaut    : Plane 2, question 4 (a term never defined); question 1 —
                   "what is not in the list passes": a section-level
                   citation and a non-contract/piece double citation are
                   wrong by implication and raised by nothing.
    Ce qu'il faut: "Bearer" is defined in the file or the file names where
                   the technical document defines it (the preamble, if that
                   is where). A section-level citation is a named defect
                   kind. Two lots citing one entry outside the contract/piece
                   case is either a named defect or explicitly not one.
    Justification: Robustness — a lot anchored on a whole section gives the
                   Détailleur a sheet with no bounded entry; an unnoticed
                   double citation gives two lots building one thing.

### 15

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 4, step c "A lot that never becomes eligible sits in
                   a cycle — a defect, not a blocker" and "On a cycle … leave
                   `## Order` and `## Blocks` empty"
    Aujourd'hui  : A lot whose need no lot produces and that is not marked
                   pre-existing — a hole, already raised at move 1 — never
                   becomes eligible either. By step c it is "in a cycle", the
                   order is left empty, and the Cadreur reads a cycle where
                   there is none.
    Le défaut    : Plane 3, criterion 4 — the test "never eligible" has two
                   causes and one verdict. Plane 2, question 3 — what the
                   order does with a lot behind a hole is unforeseen.
    Ce qu'il faut: Move 4 distinguishes a lot blocked by a hole (its
                   unsatisfied need is produced by no lot at all) from a lot
                   in a cycle (its need is produced by a lot that is itself
                   ineligible, transitively back to it). One rule says what
                   the order does with a hole — for instance treat the
                   missing need as pre-existing for ordering so the rest of
                   the sequence still comes out — and only a true cycle
                   empties `## Order`.
    Justification: Round trips — a hole reported as a cycle sends the
                   Cadreur looking for a loop that is not there. Robustness
                   — an order emptied for a single missing mark loses the
                   whole sequence for a round.

### 16

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 4, the tie-break "take the one whose layer matches
                   the lot you just placed"
    Aujourd'hui  : A lot's layer is the section its entries come from (move
                   3: "Entries from two sections are a defect: the lot
                   belongs to no layer"). On a bug-fix cycle a lot "can carry
                   entries from any section" — it has no layer, and the
                   tie-break has no input.
    Le défaut    : Plane 2, question 3 — the bug-fix case of this step is
                   unforeseen; the file promises a mechanical tie-break and
                   has none there.
    Ce qu'il faut: On a bug-fix cycle, the tie-break is the lot list's own
                   order, stated at move 4 next to the layer rule.
    Justification: Robustness — two runs on one bug-fix split must give one
                   sequence.

### 17

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 5 and "The ceilings, by the layer the lots belong
                   to" (the table and the five paragraphs after it)
    Aujourd'hui  : The table's column is "Lots per block"; four paragraphs
                   later, "The ceilings count entries cited, not lots". Each
                   ceiling is a range ("8-10", "3-4") and "indicative,
                   estimates rather than measurements". The layers are
                   Models/migrations, Services, Repositories, Providers,
                   Screens; nothing maps a section of the technical document
                   to one of these names, and a section matching none has no
                   ceiling.
    Le défaut    : Known case "two passages asking for different things"
                   (lots versus entries). Plane 2, question 1 — a range that
                   is "not a target" is not a test two readers apply the same
                   way: one closes at 8, one at 10. Plane 2, question 2 —
                   the section-to-layer mapping is a fact nothing gives;
                   question 3 — an unlisted layer is unforeseen. Plane 3,
                   criterion 6 — "Providers", "Screens" are one framework's
                   vocabulary; criterion 1 — the table fits one project.
    Ce qu'il faut: One number per layer, counting entries cited, and the
                   table's header says so. The mapping from the technical
                   document's sections to the layers is stated — or the
                   ceilings are keyed on the sections as the technical
                   document names them, which removes the mapping and the
                   framework words. A default ceiling for a section the
                   table does not list. The "indicative, not targets"
                   sentence goes: a ceiling the agent may exceed at will is
                   not a rule.
    Justification: Robustness — `## Blocks` drives how many lots the
                   Détailleur holds at once; blocks that differ from run to
                   run or overflow a reader's context degrade every sheet in
                   the block. Round trips — a block closed early costs a
                   Détailleur invocation.

### 18

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 5, "On a redécoupage … The coded ones keep the
                   blocks they ran in — write them back unchanged"
    Aujourd'hui  : Nothing in "What you read" gives the block a coded lot
                   ran in: the previous `code/sequence.md` is not listed (and
                   is the file about to be overwritten), and whether
                   `redecoupage.md`'s `## Ce qui est déjà codé` carries it is
                   not said. How the new blocks are numbered after the kept
                   ones is not said.
    Le défaut    : Plane 2, question 2 — a move resting on a fact nothing
                   gives it; question 4 — a placeholder (the kept block) with
                   no rule for what fills it.
    Ce qu'il faut: The file names where the block of a coded lot is read
                   from (the previous `code/sequence.md`, read before it is
                   rewritten, or the redécoupage file if it carries it) and
                   states that new blocks continue the numbering after the
                   highest kept one.
    Justification: Robustness — a coded lot written into a different block
                   than it ran in breaks whatever `/8_code` keys on block
                   identity; the agent otherwise guesses it.

### 19

    Fichier      : .claude/agents/verificateur.md
    Cible        : Move 6, "archive it … once the sequence is written"
    Aujourd'hui  : The archive happens at the end of every run. The agent
                   runs up to three times on one split; after round 1 the
                   file is `redecoupage-NN.md`, the Cadreur's correction
                   round and the agent's round 2 no longer find
                   `code/redecoupage.md`, and — by the file's own reading
                   list — no longer know which lots are coded: move 2's
                   "coded lot is behind", move 5's "write them back
                   unchanged", and comment 5's exemptions all switch off.
    Le défaut    : Plane 1 — order: a move that destroys what a later
                   round of the same loop needs. Plane 2, question 1 — the
                   move reaches further than it should (every round instead
                   of the last).
    Ce qu'il faut: The archive happens only on the run whose `## Defects`
                   is empty — the one that ends the loop. A run that reports
                   defects leaves `code/redecoupage.md` where it is. (With
                   comment 1, whoever performs the rename applies the same
                   condition.)
    Justification: Robustness — on rounds 2 and 3 of a redécoupage, coded
                   and merged lots get re-ordered and re-blocked as if
                   uncoded, and the sequence contradicts the tree.

### 20

    Fichier      : .claude/agents/verificateur.md
    Cible        : Role ("One invocation per round — up to three on one
                   split"), "What you never do" (last item), Part 2 "Who
                   invokes you" (whole); and the commentary sentences "Rarer
                   since he greps the code", "on a new application most needs
                   look like that", "These two checks protect the
                   Détailleur", "It shows when the module stops compiling,
                   in a lot that touches neither end"
    Aujourd'hui  : The fresh-context rule — do not look for what an earlier
                   round reported, check the split in front of you — is
                   stated three times. The listed sentences explain why a
                   rule exists or how a defect manifests downstream; none
                   changes what the agent does.
    Le défaut    : Plane 3, criterion 5 — justification and commentary on
                   why a rule came to be; a rule stated three times is read
                   three times.
    Ce qu'il faut: The fresh-context rule stated once, where the rounds are
                   introduced, with one line in "What you never do". The
                   commentary sentences go; what remains of each paragraph
                   is the test.
    Justification: Tokens — paid at every invocation, three per split.

### 21

    Fichier      : .claude/commands/7_lots.md
    Cible        : "How it runs", the table "On disk / What it does" (row
                   "`code/sequence.md` carrying `## Defects`") and the table
                   "When it hands back" (row "`code/sequence.md`, no
                   `## Defects`")
    Aujourd'hui  : Both tests are on the presence of the heading. The agent
                   writes the heading always: "Write the file even with no
                   defect — an empty `## Defects` section says the split
                   holds".
    Le défaut    : Command question 1 — a row names an outcome that cannot
                   occur (a `sequence.md` without the heading), and the
                   outcome that does occur (heading present, nothing under
                   it) matches the wrong row.
    Ce qu'il faut: The tests read the content under `## Defects` — no line
                   under it, the split holds; one or more lines, it does not.
    Justification: Round trips — a holding split is relayed as a failing
                   one, the orchestrator reports defects that do not exist
                   and `/cycle` stops on "the split is not converging".

### 22

    Fichier      : .claude/commands/7_lots.md
    Cible        : "How it runs", the paragraph "Say so in the prompt of
                   both agents, and name the file" with the two-line prompt
                   excerpt
    Aujourd'hui  : Three statements in one section: the orchestrator puts a
                   redécoupage notice "in the prompt of both agents"; "You do
                   not run `verificateur`" — its prompt is the Cadreur's;
                   and under Invocation parameters, "The Cadreur finds by
                   itself what brought it back — a `## Defects` section, or a
                   `code/redecoupage.md`. Say nothing about it in the
                   prompt". The agent's own reading list already opens
                   `code/redecoupage.md` "when it is there".
    Le défaut    : Known case "two passages asking for different things";
                   Command question 2 — a thing the prompt names that no
                   move needs. The orchestrator cannot write the
                   Vérificateur's prompt at all.
    Ce qu'il faut: One rule, and it is the one the file already states
                   twice: the prompt carries the working folder and nothing
                   else; both agents find the redécoupage file themselves.
                   The "say so in the prompt of both agents" passage goes.
    Justification: Round trips — the orchestrator stalls on an instruction
                   it cannot carry out, or paraphrases an agent's process in
                   the prompt, which the same command forbids.

### 23

    Fichier      : .claude/commands/7_lots.md
    Cible        : "When it hands back" table — row "`code/blocked_
                   verificateur.md` → Stop. There was nothing to check"; "What
                   you relay" — "The Product Owner fills `## Decision`, and
                   the Cadreur reads it on its next run"; and the absence of
                   a row for `code/sequence.md` carrying defects with no
                   blocking file
    Aujourd'hui  : The only cause of a Vérificateur block is a lot list
                   missing or unreadable — after the Cadreur has just written
                   it. The command stops and hands a `## Decision` to the
                   Product Owner, which the Cadreur "reads on its next run"
                   although the file is the Vérificateur's. A third-round
                   non-convergence is said to arrive as `blocked_cadreur.md`;
                   a `sequence.md` still carrying defects without one has no
                   row.
    Le défaut    : Command question 1 — a row whose follow-up cannot happen
                   (no decision settles a missing file; the wrong agent is
                   said to read it), and a possible outcome with no row —
                   whether it is possible depends on the Cadreur always
                   blocking at round 3 (closing section).
    Ce qu'il faut: The Vérificateur row treats the block as a malfunction
                   of the step before: relay which file was missing, with no
                   decision asked of anyone (consistent with comment 8). A
                   row for `sequence.md` with defects and no blocking file —
                   stop and relay the defects — unless the Cadreur's file
                   guarantees it cannot occur, in which case the command
                   says so.
    Justification: Round trips — a Product Owner asked to fill a decision
                   that no agent will read; an outcome with no row leaves the
                   orchestrator deciding on its own.

### 24

    Fichier      : .claude/commands/7_lots.md
    Cible        : Section order — "Git, in this mode" (file away
                   questions, commit, create and enter the worktree) after
                   "How it runs" and "Invocation parameters"
    Aujourd'hui  : The worktree creation and "Enter the worktree before
                   invoking the agent, not after it fails" come two sections
                   after the invocation they constrain.
    Le défaut    : Plane 1 — a constraint stated after what it constrains.
    Ce qu'il faut: The steps appear in running order: file away, commit,
                   worktree, enter, invoke, read what came back, merge, push,
                   remove.
    Justification: Round trips — the command itself records a whole
                   invocation lost to this ordering ("Seen once").

### 25

    Fichier      : .claude/commands/cycle.md
    Cible        : Every command name in the file — the opening list
                   (`/1_structure`, `/2_grille`, `/3_reclasse`,
                   `/4_convertit`, `/7_decoupe`, `/5_compare`,
                   `/6_fusionne`), the routing table (rows 6, 7, 8, 9, 11,
                   12–16), "After `/1_structure`", the warnings
    Aujourd'hui  : The files in `.claude/commands/` are `1_lexique`,
                   `2_structure`, `3_decoupe`, `3b_nature`, `4_grille`,
                   `5_reclasse`, `6_convertit`, `7_lots`, `8_code`,
                   `fusion_compare`, `fusion_applique`. Row 7 routes a filled
                   `blocked_verificateur` decision to `/7_decoupe`, which
                   does not exist; the route to the split is `/7_lots`.
    Le défaut    : Plane 2, question 4 — a reference to something that does
                   not exist, on every row. Command question 1 — the row for
                   this agent's block names a next step that cannot run
                   (and, per comment 8, a decision that cannot be written).
    Ce qu'il faut: The names match the files on disk, including
                   `/1_lexique` and `/3_decoupe`/`/3b_nature`, which the
                   chain currently skips. Row 7's `verificateur` entry
                   follows whatever comment 8 decides about that block.
    Justification: Round trips — the chaining command stops on an unknown
                   command at every phase boundary, or runs the wrong one.

---

## From the verdict

Read after everything above: section 2 (the agent's line), sections 4 to 7.

Section 2 — "Vérificateur — the role holds. Judges a split it did not
cut, on a fresh context each time, and derives the sequence mechanically.
The three defects it catches that names alone cannot (unbuilt surface,
undeclared caller, contract without cascade) are its reason. Tokens: up to
three full readings of the split per cycle."
→ Not found above as a defect, and it is not one: the role, the fresh
context and the mechanical order are in the file as described. One
contradiction by the agent, on the three defects: the file states seven
kinds at move 1, and the one the verdict calls "undeclared caller" the
agent itself says it cannot count — "You judge the shape, not the count.
Whether four callers is the right number is the Cadreur's to know; that a
changed contract declares none of either is a defect you can see." That
is comment 10: of the three named as the agent's reason, one is grounded in
nothing the agent reads.

Section 4, sweep entries 28 and 44 — `spec-technique.md` and `desc-bug.md`
read by the Vérificateur "(cited entries)".
→ Consistent with the file, which adds two reads the verdict does not list:
the preamble, always, and the `^### §` grep of titles. Nothing to add.

Section 4, sweep entry 42 and D17 — "A settled blocking file is renamed by
one agent and deleted by five"; section 7, question 13 — "Rename or delete
a settled blocking file?"
→ Already found above, and sharper than the verdict has it: this agent
does both in one section — "rename it `code/blocked_verificateur-NN.md`,
next free number" and, ten lines later, "Delete the file once applied"
(comment 8). And with its tools it can do neither (comment 1). Question 13
cannot be answered from this file: it says both.

Section 4, sweep entry 46, D18, and section 7, question 5 — "The Cadreur's
symbol inventory is an input to the Vérificateur and is not a named file …
If the inventory lives only in the Cadreur's context, the Vérificateur
cannot read it and its first defect class is checked against the lots' own
declarations — ratification."
→ Partly found above (comment 3). Contradicted in part by the agent: it
does not take the inventory from the Cadreur's context or from its prompt;
it lists it under "What you read" — "The `## Symbols` inventory comes
first — it is what the lots are checked against" — so the file expects a
heading on disk. What it does not say is in which file. Whether
`code/decoupage.md` carries a `## Symbols` section is the Cadreur's file
to settle (closing section); if it does, D18 is a missing path in this
agent, not a missing artefact. One thing the verdict does not ask, and
that the same check depends on: whether the lots' `Produces` and
`Modifies` name operations or only symbols — without operations, "an
operation the inventory lists that no lot produces or modifies" cannot be
made whatever file the inventory is in (closing section).

Section 4, sweep entry 47 — `code/decoupage.md` read by the Vérificateur.
→ Consistent. Nothing to add.

Section 4, sweep entry 48 — `code/sequence.md` (order, blocks, defects),
readers "command; Détailleur; Cadreur (defects)": wired.
→ Wired, but the wire is misread: the command tests for the presence of
the `## Defects` heading, and the agent writes the heading on every run
(comment 21). The verdict judged the artefact, not the test.

Section 4, sweep entry 53, and section 5, A-6 — `code/redecoupage.md`,
"Vérificateur (archives)"; the redécoupage loop "Cadreur, fresh cut of the
uncoded lots; Vérificateur ×≤3 … Bound: none".
→ The archive step is found above with a defect the verdict does not
name: it fires on every one of the "×≤3" runs, not once per loop, so the
Cadreur's correction rounds lose the file (comment 19). On the missing
ceiling: not found above, and not this agent's to hold — but the agent is
the one that numbers `redecoupage-NN.md`, which is the count a ceiling
would read, and nothing in the file reads it. Where the ceiling should
sit is for the group pass.

Section 5, A-1 — "Cadreur ⇄ Vérificateur. Stop: an empty defect list.
Checkable — a section of `sequence.md`. Bound: three rounds, counted by
the Cadreur, then a blocking file naming what did not converge. Sound."
→ Consistent with the agent's Part 2. Two things the verdict does not see,
both above: the command's test on that section is on the heading, not on
its emptiness (comment 21); and the third-round `blocked_cadreur.md` is
assumed, so `7_lots.md` has no row for a `sequence.md` still carrying
defects without one (comment 23). Whether the Cadreur always blocks at
round 3 is its file's to settle.

Section 6, P3 — "the Vérificateur's three defect classes"; P9 — the
fresh context "buys: the Vérificateur … I would keep every instance".
→ Seven kinds, not three — the description the verdict judged is behind
the file. P9 is consistent with the agent; the only cost above is that
the rule is stated three times in one file (comment 20).

Section 7, question 17 — a bound on the Cadreur re-blocking after an
Architecte refusal, "`cadreur.md`, `/7_lots`".
→ Names the command, not this agent; nothing in `7_lots.md` bounds it
either, but the loop does not pass through the Vérificateur. Left for the
Cadreur's pass.

Nothing else in sections 4 to 7 names this agent.

---

## What another agent would settle

The shape of `code/decoupage.md`: does `Produces` / `Modifies` list
operations per symbol or symbols only; where the pre-existing mark lives
(on the need, or in the inventory); where a piece is marked; where the
caller of a production is named; where a cascade caller of a changed
contract is declared (`Modifies`, or an annotation).
→ `cadreur.md`.
→ If operations and callers are declared: move 1's kinds 1, 5, 6 and 7
are runnable as written and comment 10 reduces to merging two paragraphs.
If not: kinds 1, 5 and 6 cannot be checked from what the agent reads and
collapse to name crossing; the agent must say so or stop claiming them.
Comment 13 bites only if cascade callers live in `Modifies`.

Does `code/decoupage.md` carry a `## Symbols` heading, and does the Cadreur
keep the inventory there across rounds?
→ `cadreur.md`.
→ Yes: comment 3 is a missing path and D18 is closed. No: the agent's move
1 has no input and D18 stands as the verdict wrote it.

What the Cadreur's prompt to the Vérificateur carries (the working folder
only? a round number? a redécoupage notice?), and whether the Cadreur
always writes `blocked_cadreur.md` when the third round still shows
defects.
→ `cadreur.md`.
→ If the prompt carries only the working folder, the agent's reading list
is sufficient and nothing is missing. If it carries a round number, the
agent's "fresh context, do not look for what you said" is partly undone
and the file should say what it does with it. If the Cadreur does not
always block at round 3, comment 23's missing row is a real outcome.

Does the Cadreur read `## Defects` by type name, by quoted line, or by lot
identifier only; and does it mark coded lots in the lot list distinctly?
→ `cadreur.md`.
→ By type or by quote: comments 6 and 7 are load-bearing. By lot only:
they are still worth applying for two runs of this agent, but do not cost a
round. If coded lots are marked in the lot list, comment 5's rules can key
on the mark instead of on `redecoupage.md`, and comment 19 loses half its
weight.

How the technical document's sections are named, and whether they map one
to one onto Models/Services/Repositories/Providers/Screens; whether the
preamble defines "bearer" for a `desc-bug.md`.
→ `convertisseur.md` (spec-technique.md), `diagnostiqueur.md`
(desc-bug.md).
→ If the sections carry those names, comment 17's mapping is a one-line
statement and comment 14's "bearer" is a pointer to the preamble. If not,
the ceilings table has no key and "bearer" is undefined for this agent.

What `code/redecoupage.md`'s `## Ce qui est déjà codé` carries — lot
identifiers only, or also the block each ran in and its verdict status —
and who writes it.
→ The agent that writes it (named by `8_code.md`; the verdict says the
Arbitre).
→ If it carries the block, comment 18 is a pointer. If not, the agent must
read the previous `code/sequence.md` before rewriting it, and the reading
list gains a file. If it carries verdict status, comment 4's read is
duplicated.

What values `## Status` in `code/<lot>/verdict.md` takes, and whether a
non-PASS lot can appear under `## Ce qui est déjà codé` at all.
→ `relecteur.md`; the command `8_code.md`.
→ If a non-PASS lot can never be listed there, comment 4's read is dead
and goes. If it can, comment 4's outcome rule is needed.

Whether anything downstream keys on block identity (block numbers,
`block-N` names) across a redécoupage.
→ `detailleur.md`; the command `8_code.md`.
→ If yes, comment 18's numbering rule is load-bearing. If nothing reads
block identity, "write them back unchanged" can become "coded lots are not
re-blocked" and the numbering question disappears.

Whether the Cadreur, on a redécoupage, also needs `code/redecoupage.md` on
its correction rounds (rounds 2 and 3).
→ `cadreur.md`.
→ If yes, comment 19 is confirmed on both sides of the loop. If the
Cadreur snapshots what it needs at round 1, comment 19 still holds for the
Vérificateur's own rounds.
