# Relecteur — examination

**Agent**: `.claude/agents/relecteur.md`
**Command that invokes it**: `.claude/commands/8_code.md` — the only one. `cycle.md`, `audit_blocages.md` and `socle.md` name the relecteur but never invoke it (a routing row, a list of who owns what, a note on who reads the conventions).

## Plane 1 — the agent as a whole

**Role, from the file**: it judges one coded lot against its spec sheet and the realisation report — symbols, one test per criterion, the conventions the sheet names, the report's fields, self-use of what the lot writes — and writes a verdict whose `## Status` line drives the coding loop.

**Its moves, in order of execution**

| # | Move | Why it exists | What it feeds | What it overlaps |
|---|---|---|---|---|
| R | Look for `blocked_relecteur.md`, apply a filled decision, retire the file | A settled block must not stop the next run | The five checks | — |
| 1 | Symbols match the sheet's signatures (created / modified) | The later lots of the block are detailed on these signatures | `## Symbol divergences`, `## Status`; read by `8_code` move 4 and by the Détailleur | Point 4 says "Point 1 already covered `## Symbols`" — no overlap left |
| 2 | One test per acceptance criterion, matched on assertions | A criterion with no test is the gap the Contrôleur will find later, at the price of a whole cycle | `## Status`, `## Cause` | — |
| 3 | The conventions the sheet names hold on the lot | The Architecte's rules bind only if something reads them against the code | `## Status` | — |
| 4 | The report's fields hold: `## Build`, `## State`, `## Requests`, `## Outside the lot`; the sheet's `## Requests` | The report is the only trace of the lot; a red module must not pass | `## Verified`, `## Status` | — |
| 5 | Nothing the lot writes goes unused by the lot itself | A symbol can carry the right signature and do nothing with it | `## Status` | Reads the bodies point 1 only greps — stated as distinct |
| V | Write `verdict.md`: Status, Verified, Cause, Symbol divergences | The loop stalls without it | `8_code` (Status; divergences at move 4); the fresh Réalisateur on a FAIL | — |
| B | Write `blocked_relecteur.md` when there is nothing to judge | The run must stop rather than grade an absent lot | `8_code` — relay and stop | — |

**The set**

- **Move whose result nothing carries forward**: `## Cause` — `8_code` reads `## Status` only, retries with a fresh `sonnet` Réalisateur whatever the cause, and the "threshold set on the accumulated causes" that would justify Opus exists in no file the chain runs. Also the **PASS with reservation** status: the reservation has no field in the verdict and no reader. Both below.
- **One job falling between two moves**: naming the lots a divergence affects — asked of move 1 and of the never-do list, but no move and no read gives the agent the block's composition or which lots are still uncoded. Below.
- **Order**: point 4's build check decides `FAIL structurel` on its own and makes points 1, 2, 3 and 5 moot ("its code was never executed"); it runs fourth. Below, last.
- **Nothing to remove**: each of the five points catches a different observable and each has a reader.

---

## Comments — in the order to apply them

### 1

    Fichier      : .claude/agents/relecteur.md
    Cible        : PART 2 "When you resume after a blocking file" — the
                   table row "A ## Decision filled", the "Renaming means
                   renaming" paragraph, and "Delete the file once applied";
                   the frontmatter tools line
    Aujourd'hui  : The row says: apply it, then rename it
                   blocked_relecteur-NN.md ("git mv, or the equivalent
                   ... never leave something at the old name"). Two
                   paragraphs later: "Delete the file once applied." The
                   agent's tools are Read, Grep, Glob, Edit, Write — none
                   renames, none deletes, and no move uses Edit.
    Le défaut    : Plane 3 criterion 4 (two rules, one target: rename vs
                   delete) and Plane 2 question 2 (the move rests on an
                   action no tool performs). With Write alone the agent
                   can create the numbered copy but must leave the
                   unnumbered file in place — the exact thing the
                   paragraph forbids — or overwrite it with something,
                   which the next run reads as a block still standing.
    Ce qu'il faut: One retirement rule, executable with the tools the
                   agent has. Either the agent gets a tool that renames
                   (and the "delete" sentence goes), or retirement is not
                   its job: the agent re-reads a filled decision, runs
                   the five checks, and the orchestration — which has
                   git — renames the file after the verdict. The
                   unmatched Edit tool and the "When Edit fails" section
                   go with whichever is chosen if nothing edits.
    Justification: Robustness — as written, every settled relecteur
                   block leaves a file the next run treats as a standing
                   block, so a lot once blocked cannot be reviewed again
                   without a hand intervention. Round trips — one stop on
                   the Product Owner per settled block, for nothing.
                   Tokens — a section and a tool no move uses, loaded on
                   every invocation.

### 2

    Fichier      : .claude/agents/relecteur.md
    Cible        : "What you read" (third bullet, "The code the lot
                   touched, and the tests"); point 4, the "## Outside the
                   lot ... Check it against the diff" paragraph; "When you
                   cannot produce" ("no code committed")
    Aujourd'hui  : The agent must check ## Outside the lot "against the
                   diff", and block when "no code [is] committed". Nothing
                   it reads and no tool it has yields a diff or a commit:
                   the only list of files the lot touched is the one the
                   report itself declares, plus the sheet's declared
                   files.
    Le défaut    : Plane 2 question 2 — a move resting on a fact nothing
                   gives it. The Outside-the-lot check can only confirm
                   the report against the report; a file changed and
                   declared nowhere is invisible to it, which is the one
                   case the paragraph exists for. Same for "no code
                   committed": the agent can grep a symbol's presence,
                   not its commit.
    Ce qu'il faut: The agent must hold an independent list of the files
                   the lot's commit(s) changed. The cheapest source is the
                   invocation: the orchestration has git and the
                   worktree, and names the changed files in the prompt
                   (see comment 3); the agent then reads those files as
                   "the code the lot touched" and checks the report's
                   ## Outside the lot against that list. "No code
                   committed" stops being a block of the agent's: with an
                   empty file list the orchestration does not invoke it.
    Justification: Robustness — an undeclared file change is the case
                   that later makes a sheet false with no trace; today it
                   passes by construction. Round trips — an invocation
                   that opens on nothing to review, then a block, then a
                   Product Owner stop, replaced by no invocation at all.

### 3

    Fichier      : .claude/commands/8_code.md
    Cible        : "Invocation parameters" — the prompt of the relecteur
                   (only the realisateur's is shown; the relecteur's is
                   inferred from "Name the lot ... in the prompt")
    Aujourd'hui  : Working folder and lot, nothing else.
    Le défaut    : "And for the command", question 2 — a thing the agent
                   must have and the prompt does not name. With comment 2
                   applied, the agent needs the list of files the lot
                   committed; the orchestration is the only party that
                   can compute it before invoking.
    Ce qu'il faut: The relecteur's invocation is written out like the
                   realisateur's, and its prompt carries the files the
                   lot's commit(s) changed. An empty list means the
                   realisateur committed nothing: the command treats that
                   as a failed attempt of the realisateur (it counts in
                   the three) and does not invoke the relecteur.
    Justification: Robustness and round trips, as comment 2 — plus the
                   relecteur's block on "no code" becomes unreachable,
                   which removes one of the three stops on the Product
                   Owner this agent can cause for something no product
                   decision can settle.

### 4

    Fichier      : .claude/agents/relecteur.md
    Cible        : "What you do not check", last two paragraphs ("A
                   divergence only threatens the uncoded lots of the same
                   block ... Name those lots in the verdict"); "What you
                   read" ("Nothing else. Not ... the lot list, not the
                   sequence"); never-do "Report a divergence without
                   naming the lots it affects"; the example
                   "affects lot-04, which consumes it"
    Aujourd'hui  : The agent must name, for each divergent symbol, the
                   uncoded lots of the same block that it affects — and
                   is forbidden to read the sequence (which holds the
                   blocks) or anything that says which lots are coded or
                   which sheets cite the symbol.
    Le défaut    : Plane 2 question 2 — the fact is given by nothing the
                   agent reads; it will guess, and the never-do rule
                   forces it to write a guess rather than leave the field
                   honest. Also Plane 1: a job (finding the affected lots)
                   falling between the agent, which is told to name them,
                   and the command, which only forwards what is named.
                   The rule "the later blocks are detailed on the real
                   code" also lives under a heading called "What you do
                   not check" while it is a thing to write.
    Ce qu'il faut: The agent must have a bounded source for "which
                   uncoded lots of my block cite this symbol": the block
                   line of its lot in code/sequence.md (one line, not the
                   file), the presence of a PASS verdict per lot of that
                   block, and one grep of the divergent symbol across
                   those lots' sheets. The "Nothing else" list is amended
                   accordingly. The affected lots are the ones whose
                   sheet names the symbol — a rule two readers apply the
                   same way — and a divergence no uncoded sheet cites is
                   reported with "affects none". The paragraph moves out
                   of "What you do not check" to where the divergence is
                   reported.
    Justification: Robustness — this field is what sends the block back
                   to the Détailleur; a lot missed here is coded against
                   a false sheet and fails at review or, worse, passes
                   with the wrong contract. Tokens — one line of the
                   sequence and one grep, against the alternative of
                   opening the block's sheets.

### 5

    Fichier      : .claude/agents/relecteur.md
    Cible        : Point 1 ("Every divergence is reported, even when the
                   code works"); never-do "Let a symbol divergence pass
                   because the code works"; the verdict table; the
                   example verdict under "What you write"
    Aujourd'hui  : A divergence is a failure of point 1 (never let it
                   pass) and at the same time a fact to propagate ("their
                   sheets ... are now false; the orchestration sends the
                   block back to the Détailleur"). The example shows
                   `FAIL mineur` with a missing test as cause AND a
                   divergence listed — two points failing, which the
                   table grades `structurel` ("several points fail
                   together"), and a divergence treated as information,
                   not as the failure.
    Le défaut    : Plane 3 criterion 4 and "two passages asking different
                   things". If a divergence is a FAIL, the fresh
                   Réalisateur conforms the code to the sheet and the
                   later sheets are not false — nothing to propagate. If
                   it is a fact to propagate, it is not a FAIL. The agent
                   says both, and the example contradicts its own table.
    Ce qu'il faut: One policy, stated once. The distinction that makes
                   both readings true is whether the divergence was
                   settled mid-lot: a signature changed by a filled
                   decision the Réalisateur applied is reported in
                   ## Symbol divergences with its affected lots and is
                   not a failure; a signature that diverges with no such
                   decision is a failure of point 1 and is listed as a
                   finding, not in the propagation field. The agent needs
                   to see which is which — the settled
                   blocked_realisateur-NN.md files of the lot, or a
                   report field naming the decisions applied (which one
                   exists is for another agent's file to settle; see the
                   last section). The example is rewritten to agree with
                   the table.
    Justification: Robustness — this is the switch between "fix the
                   code" and "rewrite four sheets"; read the wrong way,
                   either the block is detailed on a signature about to
                   be reverted, or a lot that silently changed a
                   contract passes. Round trips — a Détailleur invocation
                   (opus) spent rewriting sheets against a divergence the
                   next retry removes.

### 6

    Fichier      : .claude/commands/8_code.md
    Cible        : "What you read" ("code/<lot>/verdict.md — its
                   ## Status line only"); "The loop, per lot", moves 3
                   and 4
    Aujourd'hui  : The command reads Status only, yet move 4 fires "if
                   the verdict names lots affected by a divergence" —
                   which is in ## Symbol divergences. Moves 3 and 4 are
                   listed one after the other with no condition tying
                   them: a FAIL verdict that also names affected lots
                   triggers both a fresh Réalisateur and a Détailleur
                   rewrite, on the same verdict.
    Le défaut    : "And for the command", question 1 — two passages
                   asking different things (Status only / read the
                   divergences), and a row that fires on a state that
                   the next move may erase (the fix can restore the
                   promised signature; the re-review then lists no
                   divergence).
    Ce qu'il faut: The command reads two fields of the verdict — Status
                   and Symbol divergences — and says so. Move 4 runs on
                   the lot's final verdict only, after the retries are
                   over, never on a FAIL that is about to be retried.
                   With comment 5, what it forwards to the Détailleur is
                   the propagation field alone.
    Justification: Robustness — an orchestrator obeying "Status only"
                   never rewrites a sheet; one obeying move 4 literally
                   rewrites sheets against a signature the next retry
                   reverts. Round trips — one opus invocation per FAIL
                   carrying a divergence, wasted.

### 7

    Fichier      : .claude/agents/relecteur.md
    Cible        : "What you write" — the four fields; point 4 ("A
                   missing field is a divergence", "Missing there is a
                   divergence as well"); "Prose: One field, one answer"
    Aujourd'hui  : The verdict holds Status, Verified, Cause, Symbol
                   divergences. Nothing names which points failed and on
                   what — the example smuggles the finding into Cause
                   ("understanding — criterion 3 has no test"), one line
                   for one failure. A missing report field, a broken
                   convention, an unused parameter (points 3, 4, 5) have
                   no field at all, and the word "divergence" covers a
                   symbol mismatch (with affected lots), a missing report
                   field and a missing sheet field alike.
    Le défaut    : Plane 2 question 1 (the verdict does not reach as far
                   as the checklist: five points observed, one line to
                   report them) and Plane 3 criterion 4 (one word, three
                   meanings — and the never-do "report a divergence
                   without naming the lots it affects" applies to only
                   one of them).
    Ce qu'il faut: A field listing every failed point, one line each,
                   naming the object — the symbol, the criterion number,
                   the rule, the report field. Cause carries the category
                   alone. "Divergence" is reserved for the symbol case;
                   the other gaps are findings. Verified keeps its role
                   but its name must not read as something the agent
                   established — it copies a claim, and the agent says
                   so.
    Justification: Round trips — the fresh Réalisateur is invoked "with
                   the verdict"; a verdict that names one finding out of
                   three buys a second FAIL on the two it did not name.
                   Robustness — a structurel verdict with no list of what
                   failed cannot be checked by the next reviewer or by
                   the audit.

### 8

    Fichier      : .claude/commands/8_code.md
    Cible        : "The loop, per lot", move 3 ("On FAIL → a fresh
                   realisateur, with the verdict. Three retries
                   maximum")
    Aujourd'hui  : Nothing reads ## Cause. Every retry is a fresh
                   Réalisateur on sonnet, whatever the cause. The agent
                   writes "only the second [limit of reasoning] would
                   justify Opus, and the threshold is set on the
                   accumulated causes" — a threshold no file states.
    Le défaut    : Plane 1 — a move whose result nothing carries forward.
                   Plane 2 question 4 — a reference to a rule the reader
                   has not seen.
    Ce qu'il faut: The command holds the rule the agent alludes to: on a
                   retry, it reads Cause, and states the count of
                   "limit of reasoning" causes on one lot from which the
                   fresh Réalisateur is passed opus (or the field is
                   removed from the agent — but then the distinction the
                   agent already makes is thrown away; I decide for the
                   consumer). The three-retry ceiling is unchanged.
    Justification: Round trips — a reasoning failure retried twice more
                   on the same model is the retry that fails three times
                   and stops on the Product Owner; the escalation is what
                   the field was designed for. Tokens — otherwise every
                   verdict pays a field nobody reads.

### 9

    Fichier      : .claude/agents/relecteur.md
    Cible        : "The verdict" — the "On a FAIL, name the cause"
                   paragraph
    Aujourd'hui  : "Only the second would justify Opus, and the
                   threshold is set on the accumulated causes."
    Le défaut    : Plane 3 criterion 5 — a justification, and a
                   reference to a rule that lives elsewhere (in the
                   command, once comment 8 is applied).
    Ce qu'il faut: The agent names the two categories and the test that
                   separates them (what the Réalisateur misread in the
                   sheet, versus what it read right and worked out
                   wrong); who escalates and when is the command's.
    Justification: Tokens — commentary loaded on every run. Robustness —
                   the reader stops looking for a threshold it is not
                   asked to apply.

### 10

    Fichier      : .claude/agents/relecteur.md
    Cible        : "The verdict" — the row "PASS with reservation"; the
                   "Status" rule ("one of the four words")
    Aujourd'hui  : "A point passes, but is worth noting for what
                   follows." The verdict's fields hold no place for the
                   note; the command reads Status and (comment 6)
                   divergences; the Contrôleur reads sheets, not
                   verdicts; the resume rule counts a lot as done when
                   its verdict "carries PASS", which a line reading
                   "PASS with reservation" does or does not, depending
                   on the reader.
    Le défaut    : Plane 1 — an output nothing carries forward. Plane 2
                   question 4 — a placeholder with no rule for what
                   fills it. "And for the command", question 1 — an
                   outcome with no row.
    Ce qu'il faut: The status goes, and Status carries three values. If
                   a passing point leaves something a later lot must
                   know, the propagation field of comment 5 is where a
                   symbol fact goes, and the state document (the
                   Réalisateur's) is where a code fact goes — neither
                   needs a fourth status. I was unsure only about
                   whether some reader of verdicts I cannot see exists;
                   see the last section.
    Justification: Robustness — the resume rule of `8_code` must be
                   unambiguous on every status the agent can write, and
                   is not on this one. Round trips — a note that reaches
                   nobody is written, and re-read, for nothing.

### 11

    Fichier      : .claude/commands/8_code.md
    Cible        : "Where to resume" ("no verdict.md carrying PASS");
                   "The loop, per lot", move 3
    Aujourd'hui  : "Carrying PASS" is the whole test. Move 3 sends a
                   fresh Réalisateur with the verdict and says nothing
                   about what runs after the fix — the pair
                   "realisateur → relecteur" is move 2, and move 3 does
                   not say it returns to it. The retry unit ("three
                   retries") is therefore either a fix or a fix plus a
                   review.
    Le défaut    : "And for the command", question 1 — the row for a
                   FAIL stops short of what produces the next PASS.
                   Plane 2 question 4 — an instruction that reads two
                   ways.
    Ce qu'il faut: The test on the status is exact (the line is `PASS`,
                   with comment 10 applied). Move 3 states that a fix is
                   followed by a relecteur on the same lot, that the
                   relecteur overwrites the verdict, and that one retry
                   is one fix-and-review.
    Justification: Robustness — an orchestrator that fixes and moves on
                   leaves a FAIL verdict in place, and the next run
                   re-codes a lot already fixed. Round trips — the
                   ceiling means the same thing to every run.

### 12

    Fichier      : .claude/agents/relecteur.md
    Cible        : "The verdict" table — rows FAIL mineur and FAIL
                   structurel; "Never fall to structurel by default"
    Aujourd'hui  : mineur is "one point fails, on its own — targeted
                   fix, no full re-review"; structurel is "the lot does
                   not do what the sheet asks, or several points fail
                   together". Two independent gaps on two points read
                   as structurel by the table and as isolated by the
                   warning. "No full re-review" is contradicted by the
                   agent itself, which has one mode and runs the five
                   checks every time.
    Le défaut    : Plane 3 criterion 4 (two readers grade the same lot
                   differently) and "two passages asking different
                   things". Plane 2 question 1 — "several ... together"
                   is not a test two readers apply the same way.
    Ce qu'il faut: structurel is defined by what fails, not by how
                   many: the lot's own module red or not run (point 4),
                   or a symbol the sheet promised that is absent or
                   unauthorised-divergent (point 1) — the lot has not
                   demonstrated the contract. Everything else is mineur,
                   however many findings. The words "no full
                   re-review" go: the re-review is full, and that is
                   right, because a fix can break another point.
                   Whether anything downstream acts on mineur versus
                   structurel is for another file to settle (last
                   section); the command today does not.
    Justification: Robustness — the status is the one line the loop
                   reads; two gradings of one lot is two loops.

### 13

    Fichier      : .claude/agents/relecteur.md
    Cible        : Point 3, first two paragraphs; "What you read", the
                   `docs/TECHNICAL_CONVENTIONS.md` bullet
    Aujourd'hui  : First paragraph: "Only those a grep settles — a
                   hardcoded user-facing string, an identifier not in
                   English, a convention the sheet named explicitly."
                   Second: "The sheet's ## Conventions says which ones.
                   Open each rule it names." Third: "Not a full audit
                   ... the rules the sheet names." The conventions file
                   is in the reading list whole.
    Le défaut    : Plane 3 criterion 4 — the scope is either "the rules
                   the sheet names" or "those plus two universal ones";
                   the first paragraph lists the two as peers of the
                   third. Plane 2 question 2 — a file read whole where
                   the sections the sheet names would do.
    Ce qu'il faut: One scope. If the two universal checks are wanted on
                   every lot, they are stated as such, apart from the
                   sheet's list, with the test each applies (a literal
                   shown to the user outside the localisation mechanism;
                   an identifier whose words are not English). The
                   conventions file is read by section: the rules the
                   sheet's ## Conventions names, nothing more.
    Justification: Robustness — a rule two readers scope differently is
                   applied by one and not the other. Tokens — the
                   conventions file grows with every Architecte
                   invocation and is loaded whole on every lot.

### 14

    Fichier      : .claude/agents/relecteur.md
    Cible        : PART 3, points 1 and 2; "When you cannot produce"
    Aujourd'hui  : The block cases are "no sheet, no report, or no code
                   committed". Point 1 foresees created and modified.
                   Point 2 takes "the criteria one by one". Nothing says
                   what a sheet with no signatures, no criteria or no
                   ## Conventions section does to the check, nor a
                   symbol the sheet asks removed, nor a test that exists
                   but is disabled.
    Le défaut    : Plane 2 question 3 — a situation where the move cannot
                   produce, unforeseen. Point 2 on an empty criteria
                   list passes vacuously ("what is not in the list
                   passes"); point 1 on a removal has no row.
    Ce qu'il faut: The agent states the outcome of each: a sheet lacking
                   a section the checklist depends on is a finding
                   against the sheet (the Détailleur's, not the lot's)
                   and the status it yields; a removal is a third row of
                   point 1 (the symbol no longer resolves); a test that
                   does not run does not count as the criterion's test.
    Justification: Robustness — the vacuous pass is exactly the gap a
                   correction cycle later pays for; a sheet with no
                   criteria today yields PASS on point 2 by
                   construction.

### 15

    Fichier      : .claude/commands/8_code.md
    Cible        : "Where you stop and hand back" — "The Relecteur and
                   the Contrôleur do not call [the Arbitre] ... their
                   blocks say something is missing" and "Any other block
                   → relay it and stop. The Product Owner fills
                   ## Decision"
    Aujourd'hui  : A relecteur block — no sheet, no report — goes to the
                   Product Owner.
    Le défaut    : "And for the command", question 1 — a row that sends
                   to the person a case an agent settles. The Product
                   Owner does not code; a missing report is a
                   Réalisateur that stopped short, and the command
                   already has the machinery for that: a fresh
                   Réalisateur, the `reprise_realisateur.md` rule, the
                   three-attempt ceiling.
    Ce qu'il faut: A relecteur block naming a missing report is routed
                   to a fresh Réalisateur on the lot, counted as an
                   attempt; a missing sheet to the Détailleur on the
                   block. Only when the ceiling is reached does the
                   command stop on the Product Owner. (With comment 3,
                   "no code" never reaches the relecteur.) The
                   `blocked_relecteur.md` file is then written for the
                   trace and retired by the orchestration — comment 1.
    Justification: Round trips — every relecteur block today is a stop
                   on the person for something no product decision
                   answers; she can only write "run it again".

### 16

    Fichier      : .claude/agents/relecteur.md
    Cible        : PART 3 — "The checklist — five points, in this order"
    Aujourd'hui  : Symbols, tests, conventions, report fields, self-use.
                   Point 4 alone can yield `FAIL structurel` ("the lot's
                   own module not compiling, or its tests not running
                   ... whatever reason the report gives ... a targeted
                   fix would demonstrate nothing").
    Le défaut    : Plane 1, order — the decision that voids the other
                   four points is taken after them.
    Ce qu'il faut: The build claim of the report is read first; when it
                   yields structurel, the verdict is written from that
                   alone and the other points are not run — the fresh
                   Réalisateur redoes the lot whole. The other points
                   keep their order.
    Justification: Tokens — a review that greps every symbol, reads
                   every body and hunts every test on a lot whose
                   module never compiled. No robustness cost: the
                   verdict is the same.

### 17 — added after the verdict, checked against the agent

    Fichier      : .claude/agents/relecteur.md
    Cible        : PART 3 — between point 1 (symbols promised) and
                   point 5 (self-use); point 4's "## Outside the lot"
    Aujourd'hui  : Point 1 checks that every symbol the sheet promises
                   exists with its signature. Point 4 checks that every
                   file outside the sheet is named. Point 5 reads the
                   bodies for what the lot writes and ignores. Nothing
                   looks the other way: a symbol, a public member or a
                   behaviour added inside a declared file that no sheet
                   entry and no criterion asks for passes every point.
    Le défaut    : Plane 2 question 1, prompted by verdict section 7
                   item 9 — the review reaches from the sheet to the
                   code and never from the code back to the sheet, so
                   an invention inside a declared file has no reader:
                   the Contrôleur compares product to sheets, this
                   agent compares sheets to code, and what is in the
                   code and in no sheet is in neither comparison.
    Ce qu'il faut: One bounded check, on the changed files the prompt
                   names (comment 3): every symbol declared there that
                   neither the sheet nor the report's ## Symbols names
                   is a finding. Symbols, not branches — a branch is
                   not greppable and the point must stay a grep. The
                   status it yields is mineur (comment 12).
    Justification: Robustness — an unasked behaviour is the gap the
                   idea never contained and no later phase can see; it
                   reaches the emulator. Tokens — one grep per changed
                   file, against the symbol list already in hand from
                   point 1.

---

## From the verdict

    Section 2 — "Relecteur — the role holds. Judges interpretation
    against the sheet, never mechanics, never source fidelity — each
    exclusion names who already covers it. 'Un lot, un verdict' and
    the divergence naming are what drive the loop."
    Already found, in part; contradicted in part. The role and the
    exclusions hold as described. "The divergence naming drives the
    loop" is what the agent intends and cannot do: it is forbidden to
    read what would tell it which lots are affected (comment 4), and
    the command it drives reads "## Status only" (comment 6).

    Section 4, sweep row 31 — TECHNICAL_CONVENTIONS.md read whole by
    the Relecteur.
    Already found — comment 13: the agent lists the file whole in
    "What you read" and then says "Open each rule [the sheet] names";
    the whole-file read is unused by any move.

    Section 4, sweep row 51 — verdict.md "(PASS / FAIL minor / FAIL
    structural; divergence names lots; build line copied)"; readers
    "command; Réalisateur on FAIL; Arbitre (status)".
    Contradicted by the agent on the statuses: it writes four, not
    three — "PASS with reservation" is the fourth ("A point passes,
    but is worth noting for what follows") — and that one has no
    field and no reader (comment 10). "Arbitre (status)" is a reader
    the agent never mentions; I cannot confirm it — added to the last
    section.

    Section 4, D14 — "A rule declared mechanical and never wired is a
    rule the Relecteur searches for by reading."
    Contradicted by the agent, narrowly: point 3 reads "Only those a
    grep settles — a hardcoded user-facing string, an identifier not
    in English, a convention the sheet named explicitly." The agent
    does not search by reading; it greps, and only the rules the sheet
    names. A mechanical rule not wired and not named by the sheet is
    checked by nobody — worse than the verdict's reading, not better.

    Section 4, D16 — the asking lot is coded and reviewed under the old
    rule; "neither the verdict nor the technical state says 'lot-03
    predates rule R12'".
    Not found above; the agent confirms it. Point 3 checks "the rules
    the sheet names", the verdict's four fields have no place for a
    rule the lot predates, and the report's ## Requests (which the
    agent checks for presence only) is the only trace. What should
    hold is on the command or the Architecte more than here; the one
    thing this agent could do is copy the lot's ## Requests line into
    the verdict, so the divergence is on the lot's record. Robustness
    at the next lot on the same file, as the verdict says.

    Section 4, D19 — the build claim is copied, never re-run;
    "recopie ce que le compte rendu affirme du build — jamais vide".
    Not found as a comment; the agent says exactly that: "## Verified
    copies what ## Build claims, in one line", and under "What you do
    not check": "The mechanics — static analysis, tests run, files
    present: the Réalisateur's loop covers them." Two things the
    verdict could not see: the agent has no tool that could run
    anything (Read, Grep, Glob, Edit, Write), so an execution here
    would need a tool grant, not a sentence; and point 4 already does
    more than copy — it reads the convention the report invokes for a
    red module elsewhere and refuses a red own-module "whatever reason
    the report gives". Whether a re-run belongs here or in the command
    after the last lot, I leave to the group pass; the verdict's own
    estimate (one full run by the command) costs this agent nothing.

    Section 4, D22 — "the exact divergence the Relecteur then reports,
    one block later".
    Already found in what it relies on: the agent does report it
    (point 1, "every divergence is reported") — and cannot name the
    lots it affects (comment 4).

    Section 5, A-3 — "In: a FAIL (minor: fix the point; structural:
    redo the lot ...). Stop: PASS. Bound: three retakes per lot, all
    FAIL kinds together, fresh Réalisateur each time. Sound."
    Contradicted on the FAIL kinds: the command does one thing on any
    FAIL ("a fresh realisateur, with the verdict"), so "fix the point"
    versus "redo the lot" is nowhere enforced by the loop; and the
    agent's own "FAIL mineur ... no full re-review" is false of its
    own process, which has one mode and runs the five checks every
    time (comment 12). "Stop: PASS" is also loose: a "PASS with
    reservation" line may or may not be read as PASS by the resume
    rule (comments 10, 11).

    Section 5, A-4 — "Divergence → Détailleur ... Checkable by the
    command (the verdict names them). Bound: one rewrite per verdict
    ... Sound."
    Contradicted: the command's reading rule is "## Status line only",
    so the trigger is checkable only by breaking that rule (comment
    6); the verdict names lots the agent has no source for (comment
    4); and the same verdict that names them is a FAIL that sends a
    fresh Réalisateur who may remove the divergence — the two loops
    A-3 and A-4 fire on one verdict with no order between them
    (comments 5, 6).

    Section 7, item 8 — "Does the Relecteur compare a test's assertion
    to the criterion's outcome — or only count one test per
    criterion?"
    Settled by the agent, on the side of the assertion: point 2 says
    "find the test that observes each. Match on what the test asserts,
    not on its name — a name can be misleading, an assertion cannot."
    A test asserting "no crash" does not observe "shows a dash" under
    that rule. The verdict's "Tester" hole is therefore narrowed to
    what the agent cannot see: a criterion the sheet never wrote
    (comment 14 on a sheet with no criteria).

    Section 7, item 9 — "Does the Relecteur flag a symbol or a branch
    no criterion asks for?"
    Not found above, and the agent answers no: point 1 goes from the
    sheet's signatures to the code, point 5 reads the promised bodies,
    ## Outside the lot covers files, not symbols within a declared
    file. Written as comment 17, bounded to symbols.

    Section 7, item 13 / D17 / sweep row 42 — "Rename or delete a
    settled blocking file?"
    Already found — comment 1 — and more exact than the verdict: this
    agent does not choose one of the two, it says both, seven lines
    apart ("rename it blocked_relecteur-NN.md ... git mv" then "Delete
    the file once applied"), and has no tool for either.

    Section 6, P10 — a sheet that omits a convention "is a lot coded
    without it and reviewed without it".
    Already found in its consequence for this agent: point 3 is
    scoped to the sheet's list (comment 13 asks for the scope to be
    stated once). Whether the two universal checks the agent lists
    are meant as a floor under the sheet is the ambiguity that
    comment names.

---

## What another agent would settle

    Does the Arbitre read verdict.md's status, as verdict.md's sweep
    row 51 says?
    .claude/agents/arbitre.md
    If yes: comment 10 must keep a status the Arbitre distinguishes,
    and comment 12's definition of structurel must match what the
    Arbitre does with it. If no: the verdict's reader list is wrong
    and comments 10 and 12 stand as written.

    Does the Réalisateur, on a retry "with the verdict", read Status,
    Cause and the findings to scope its fix — or does it re-read the
    sheet and start over?
    .claude/agents/realisateur.md
    If it reads them: comment 7 (a findings field) is the difference
    between one retry and two, and comment 12's mineur/structurel
    distinction has a consumer. If it does not: the distinction has no
    reader anywhere and the verdict could carry FAIL alone.

    Does the report record the decisions the Réalisateur applied mid-lot
    (a field naming the settled blocked_realisateur-NN.md and what each
    changed)?
    .claude/agents/realisateur.md, and .claude/agents/arbitre.md for
    the shape of a settled decision
    If yes: comment 5's authorised/unauthorised divergence is read from
    the report, and the relecteur's reading list does not grow. If no:
    the relecteur must open the lot's settled blocking files, or the
    report gains the field.

    When move 4 sends the Détailleur to rewrite the sheets a divergence
    made false, does it rewrite against the code, or against what the
    verdict states as the new signature?
    .claude/agents/detailleur.md
    Against the code: ## Symbol divergences need only name symbol and
    lots. Against the verdict: the field must carry the actual
    signature, verbatim, and comment 7's format says so.

    Does the sheet declare the files the lot may touch and where its
    tests live?
    .claude/agents/detailleur.md (the sheet's shape)
    If yes: point 2's search for tests is bounded and ## Outside the lot
    has a baseline besides the diff. If no: comment 2's file list from
    the prompt is the only baseline, and point 2 greps the whole test
    tree per criterion.

    Does the Réalisateur's loop actually run analysis and tests before
    it writes ## Build, and stop when red?
    .claude/agents/realisateur.md
    If yes: "Verified copies the claim" is a fair trace and point 4 is
    not a net. If no: the relecteur is the only check on the build and
    copying a claim guards nothing — it would need a tool to run the
    module's check itself.

    Does anything read verdict.md besides 8_code — the Contrôleur, the
    audit commands, the fusion?
    .claude/agents/controleur.md, .claude/commands/9_controle.md,
    .claude/commands/audit_blocages.md beyond the line I saw
    If something reads reservations or verdict prose: comment 10 keeps
    the status and gives it a field instead. If nothing: comment 10
    stands as written.
