# realisateur — examination

**Agent**: `.claude/agents/realisateur.md`
**Commands read**: `.claude/commands/8_code.md` — the only one that
invokes it. `cycle.md`, `audit_blocages.md` and `audit_conventions.md`
name the agent's files (`blocked_realisateur*`,
`architecte/realisateur-*`) but invoke nothing; `cycle.md` was read
whole to confirm it, the two audits were grepped only.

**Role, as the file states it**: code one lot from its spec sheet —
the code, one test per acceptance criterion, analysis and tests until
green, the technical-state update, the commit and a report — blocking
through the Arbitre on a wrong sheet, a regression outside the lot or
a verdict it judges wrong.

**The moves, as listed in Part 3**: (1) locate where the code goes,
(2) read those files and the ones holding the modified symbols, (3)
read the two open sections of the state document, (4) implement in
dependency order, (5) one test per criterion, (6) analysis and tests
until both pass, (7) update the technical state, (8) commit. Part 1
adds two more that the numbered list does not carry: write
`compte-rendu.md`, and — before move 1, per Part 2 — look for a
blocking file, a reprise file, and a verdict.

Every move feeds something that reads it: 1–2 feed 4; 3 feeds 4 (how
to write); 4–5 feed 6 and the Relecteur; 7 feeds the Cadreur; 8 feeds
the orchestration's merge; the report feeds the Relecteur. No move is
paid for nothing, and no two moves split one job. The gaps are in the
seams: what the numbered list forgets, what the shell whitelist
forbids that the procedures require, and what the report has no field
for. They follow.

---

## Comments, in the order to apply them

### 1

    Fichier      : .claude/agents/realisateur.md
    Cible        : move 8's shell whitelist ("git add, commit, status,
                   and the analysis and test commands the conventions
                   name"), the matching "What you never do" entry, and
                   the three procedures that need more: Part 2
                   "Renaming means renaming — git mv, or the
                   equivalent"; "When the decision sends the lot back
                   to the split — Drop what you wrote"; Part 2 "Delete
                   the file once applied"
    Aujourd'hui  : the whitelist names four things. Renaming a file,
                   deleting a file, and discarding uncommitted work are
                   each demanded elsewhere in the file, and none of the
                   agent's tools does them: Write cannot remove a file,
                   Edit cannot rename one, and `git mv`, `git rm`,
                   `git restore`/`git checkout --` are not on the list.
    Le défaut    : Plane 2, question 2 (a move resting on a means
                   nothing gives it) and the known pattern "two
                   passages of one agent asking for different things".
                   Also Plane 3 criterion 4: "or the equivalent" has no
                   equivalent among the tools.
    Ce qu'il faut: the whitelist must contain exactly the commands the
                   agent's own procedures require — a rename, a
                   removal, a discard of the working tree — and nothing
                   the file does not ask for. Whichever way it is
                   settled, an agent that obeys the whitelist must be
                   able to execute every procedure in the file.
    Justification: robustness and round trips. An obedient agent
                   cannot rename the settled blocking file; the file
                   says itself that anything left at the unnumbered
                   name "reads as a block still standing", so the next
                   run re-calls the Arbitre on a settled question. A
                   disobedient agent picks its own shell commands, and
                   the whitelist guards nothing.

### 2

    Fichier      : .claude/agents/realisateur.md
    Cible        : Part 2, "When you resume after a blocking file" —
                   the table row "A ## Decision filled → Apply it, then
                   rename it blocked_realisateur-NN.md", the paragraph
                   "Renaming means renaming", and the section's last
                   line "🔴 Delete the file once applied"
    Aujourd'hui  : the same section says rename (twice, with emphasis
                   on leaving nothing at the old name) and then delete.
                   The section also opens by telling the agent to read
                   the numbered files, "they say what was already
                   decided on this lot" — so the numbered file is an
                   input of a later run, and deleting destroys it.
                   Between the two sits a fragment, "How you apply it —
                   📌 then code the lot from move 1, unless…", whose
                   "it" and "then" attach to nothing.
    Le défaut    : known pattern "two passages asking for different
                   things"; Plane 2, question 4 (an instruction that
                   reads two ways; a fragment a fresh reader cannot
                   place).
    Ce qu'il faut: one fate for an applied blocking file, stated once:
                   it is renamed to the next free number and kept,
                   since later runs read it. The tail of the section
                   from "How you apply it" is either attached to a
                   subject or removed.
    Justification: robustness. Half the readers delete the file, and
                   the next run on the same lot — a FAIL retry, a block
                   on a PASS lot — no longer sees what was decided and
                   can re-raise it or code against it.

### 3

    Fichier      : .claude/agents/realisateur.md, and
                   .claude/commands/8_code.md ("Git, in this mode",
                   "When the run ends")
    Cible        : agent — "When the decision comes back empty":
                   "Commit what compiles before you stop — never commit
                   what does not. Say in En chantier what you left
                   uncommitted"; the never-do entry "Leave a dirty
                   working tree behind you, whatever the reason"; and
                   the line "The ## Decision heading is written empty,
                   and never omitted", which sits under the reprise
                   shape. Command — step 3 `git worktree remove
                   <path>`.
    Aujourd'hui  : the reprise path foresees leaving uncommitted,
                   non-compiling code and describing it in `En
                   chantier`, while the never-do forbids a dirty tree
                   whatever the reason. The command merges the branch
                   and removes the worktree; the next Réalisateur runs
                   in a fresh worktree from HEAD. Nothing uncommitted
                   survives that, and a dirty worktree refuses a plain
                   remove. The `## Decision` line, placed under the
                   reprise shape that has no such heading, reads as a
                   requirement on the reprise file.
    Le défaut    : Plane 2, question 3 (the "cannot produce" path
                   describes a state the next run can never observe);
                   known pattern "two passages asking for different
                   things"; Plane 2, question 4 for the misplaced
                   `## Decision` line.
    Ce qu'il faut: what must be true is that everything the reprise
                   names is findable by the next run, and that the
                   worktree is clean when the agent hands back. Either
                   the half-written piece is committed on the lot,
                   flagged in `En chantier` as not compiling, or it is
                   removed before the commit and `En chantier` says
                   what was undone — I lean to the first, since the
                   whole point of the reprise is not to redo it. The
                   `## Decision` line belongs with the blocking file's
                   shape, where the heading exists. The command's
                   removal step assumes a clean worktree; it should say
                   what it does when it is not, or the agent's rule
                   should make that impossible.
    Justification: robustness. Work the file calls "the field that
                   matters" is lost at every empty decision, and the
                   next Réalisateur rebuilds it from a description of
                   code it cannot see; or the run ends on a failed
                   `worktree remove` that the command has no row for.

### 4

    Fichier      : .claude/agents/realisateur.md
    Cible        : Part 3, "The eight moves"; Part 1, "What you write"
                   (the five fields)
    Aujourd'hui  : the report `code/<lot>/compte-rendu.md` is not one
                   of the eight moves; move 8 "commit, staging
                   explicitly what belongs to the lot" comes last. The
                   report has five fields, "one field, one answer —
                   what does not answer the field is not in it", and
                   four passages require statements none of the five
                   fields answers: "code against the decision and say
                   so in your report" (Part 2); "Say in your report
                   that the lot goes back to the split" (Part 1);
                   "Found one [a convention permitting the state] —
                   name it in your report and carry on" (Part 1); the
                   verdict-wrong case that ends in "stop and report".
    Le défaut    : Plane 1 — a job falling between moves (the report
                   is written by no numbered move, and whether it is
                   committed is undefined); Plane 2, question 1 (the
                   report's shape does not reach what the body asks it
                   to carry); Plane 2, question 4 ("report" — see 5).
    Ce qu'il faut: the report is a move, placed so that it is written
                   before the commit and staged with the lot — or the
                   file says explicitly that it is not committed and
                   why. The report shape carries a field for what
                   governed the code besides the sheet: a decision
                   applied (naming the numbered blocking file), a
                   convention invoked to deliver a permitted state —
                   so that a signature that differs from the sheet is
                   read by the Relecteur as decided, not as drift.
    Justification: robustness. The Relecteur "compares the symbols you
                   declare to those the sheet promised"; a decision
                   that changed a signature, unrecorded in a field it
                   reads, is a FAIL on a lot that did what it was told,
                   and a retry that cannot succeed.

### 5

    Fichier      : .claude/agents/realisateur.md
    Cible        : every "stop and report": "When the sheet is wrong"
                   (…"stop and report"), move 5 ("A test failing on
                   something outside the lot signals a regression:
                   stop and report"), "When you resume a lot in FAIL"
                   ("stop and report rather than coding against it")
    Aujourd'hui  : "the report" is defined in Part 1 as
                   `compte-rendu.md`. The three cases above are the
                   three named triggers of a block ("You block on a
                   wrong sheet, on a regression outside the lot, or on
                   a verdict you judge wrong"), and the block section
                   itself says "Blocking is not reporting". The word
                   points the other way at each trigger.
    Le défaut    : Plane 2, question 4 — an instruction that reads two
                   ways, on the three passages where the difference
                   matters most.
    Ce qu'il faut: at each of the three triggers, the instruction
                   names the block — the file to write and the Arbitre
                   to call — not "report". "Report" is then reserved
                   for `compte-rendu.md` throughout.
    Justification: robustness. A regression noted in the report and
                   not blocked stops nothing: the orchestration stops
                   only on a `blocked_*.md`, and the regression is
                   merged with the lot.

### 6

    Fichier      : .claude/agents/realisateur.md
    Cible        : move 3 ("Read the two open sections … Those two
                   only — the rest is an inventory"); the never-do
                   entry "Read CURRENT_TECHNICAL_STATE.md whole — two
                   sections, then greps by symbol"; move 7 ("Update the
                   technical state — see below"); Part 1 "Updating the
                   technical state" ("What earns a place …", "What your
                   lot made false disappears")
    Aujourd'hui  : three things. (a) The never-do says two sections
                   *then greps by symbol*; move 3 says two sections and
                   nothing else. The section the agent reads is named
                   `## Traps — general`, which by its own name implies
                   traps that are not general, living elsewhere in the
                   document, on specific subjects — the ones a lot
                   modifying that subject most needs. (b) "What your
                   lot made false disappears" requires finding the
                   existing entries on the symbols the lot modifies,
                   which is the grep the body dropped. (c) Move 7 says
                   "see below"; nothing follows. The rule it points to
                   is in Part 1, and the body there states in its own
                   words what earns a place, while also requiring the
                   `technical-state-format` skill to be loaded before
                   any write — two authorities for one rule set.
    Le défaut    : known pattern "two passages asking for different
                   things"; Plane 2, question 2 (move 7 rests on
                   entries it has no instruction to find); Plane 2,
                   question 4 (dangling reference); Plane 1 overlap
                   (body vs skill on the same rule).
    Ce qu'il faut: move 3 reads the two open sections whole *and*
                   greps the document for every symbol the sheet lists
                   as modified, so that a subject-specific trap and the
                   entries the lot will make false are both found. Move
                   7 points to where the rule is. The body keeps one
                   authority on what earns a place: it says the skill
                   governs, and does not restate the criteria — or it
                   states them and the skill is not loaded; not both.
    Justification: robustness (a trap filed under a subject is missed
                   by a lot on that subject; a stale entry stays and
                   "commands the Cadreur"), tokens (one rule set loaded
                   twice, and two texts that will drift).

### 7

    Fichier      : .claude/agents/realisateur.md
    Cible        : "What you read" (`docs/TECHNICAL_CONVENTIONS.md`,
                   unqualified) and "Conventions and language" ("The
                   sheet's ## Conventions names the rules bearing on
                   this lot — open each one and hold it")
    Aujourd'hui  : one passage lists the conventions file whole among
                   the reads; the other says the sheet names which
                   rules bear on the lot, to be opened one by one. Move
                   1 needs the rules on where code goes; move 6 and
                   the shell whitelist need the analysis and test
                   commands "the conventions name"; the block section
                   needs the rules on "which states a lot may be
                   delivered in" — none of which the sheet is said to
                   name.
    Le défaut    : Plane 2, question 2 (the same thing read twice, or
                   a fact — the commands, the locations — that the
                   named-rules reading does not give); Plane 3
                   criterion 4.
    Ce qu'il faut: one reading rule: either the file whole, and the
                   sheet's `## Conventions` is a pointer to the rules
                   to hold in mind while coding; or the named rules
                   plus the sections the agent always needs (location,
                   verification commands, deliverable states), named
                   by section. Whichever it is, the agent must not have
                   to guess whether a rule it did not open exists.
    Justification: tokens if the answer is "named rules" (the file is
                   otherwise read whole at every lot); robustness if
                   the answer is "whole" (an agent reading only the
                   named rules runs no analysis command it was not
                   told, or blocks on a state a rule it did not open
                   permits — the file names that very cost).

### 8

    Fichier      : .claude/agents/realisateur.md
    Cible        : move 1 ("The sheet says what to write, the
                   conventions say where") and "When the conventions
                   fall short" ("A condition of running that nothing
                   states … You never block on this")
    Aujourd'hui  : move 1 has no path for the case where the
                   conventions do not say where a kind of symbol goes.
                   The request section is scoped to conditions of
                   running (environment, services, devices, command
                   order) and forbids blocking; the command settles
                   requests only at the end of the lot ("At the end of
                   the lot, not of the block"). A missing placement
                   rule is neither a wrong sheet nor a condition of
                   running.
    Le défaut    : Plane 2, question 3 — a situation where the move
                   cannot produce, unforeseen, so the agent invents a
                   location; the command itself shows the foreseen
                   channel ("A request the Arbitre raised mid-lot is
                   already settled"), which this agent's text never
                   routes to.
    Ce qu'il faut: a missing convention that decides how the lot is
                   written — where a symbol lives, which layer owns it
                   — is a block, settled mid-lot through the Arbitre;
                   the end-of-lot request stays for what only the
                   verification needed. The boundary between the two
                   is stated by effect on the code, not by example.
    Justification: robustness. A location guessed at lot N is either
                   the convention every later lot inherits unwritten,
                   or the thing the Architecte rules against at the end
                   of the lot, after the code is committed and merged.

### 9

    Fichier      : .claude/agents/realisateur.md
    Cible        : move 5 ("Write one test per acceptance criterion. A
                   criterion with no test is a criterion left
                   uncovered")
    Aujourd'hui  : nothing foresees a criterion that no automated test
                   in this project can check. The Relecteur checks one
                   test per criterion; a missing one is a FAIL; a fresh
                   Réalisateur meets the same criterion; three FAILs
                   stop the run.
    Le défaut    : Plane 2, question 3 — the move cannot produce and
                   nothing says what then.
    Ce qu'il faut: a criterion the agent cannot cover with a test is a
                   defect of the sheet — the Détailleur wrote it — and
                   takes the wrong-sheet path, naming the criterion.
                   It is never silently skipped, and never covered by a
                   test that asserts nothing.
    Justification: round trips. Without it, one untestable criterion
                   costs up to three Réalisateur and three Relecteur
                   invocations before a stop that says nothing about
                   the cause.

### 10

    Fichier      : .claude/agents/realisateur.md
    Cible        : move 6 ("Run the static analysis and the tests —
                   until both pass")
    Aujourd'hui  : the only exits from the loop are a regression
                   outside the lot (block) and, implicitly, a wrong
                   sheet (block). A failure inside the lot that the
                   agent cannot make pass has no exit.
    Le défaut    : known pattern "a loop with no ceiling"; Plane 2,
                   question 3.
    Ce qu'il faut: a bound on the fix-and-rerun cycles on one failure,
                   after which the agent blocks on it with what it
                   tried — a small integer, stated. The block names the
                   failing test and the criterion it covers.
    Justification: round trips and tokens. An agent past its context
                   degrades instead of stopping (the known list names
                   it); a bound converts an endless run into one block
                   the Arbitre can read.

### 11

    Fichier      : .claude/agents/realisateur.md
    Cible        : Part 2, "When you resume a lot in FAIL" — the row
                   "FAIL mineur: Fix the point reported, re-run
                   analysis and tests, rewrite the report. Do not
                   revisit the rest of the lot"; and "Inputs: the same,
                   plus the verdict"
    Aujourd'hui  : the row ends at the report. It does not say the fix
                   is committed (move 8) nor that the state document is
                   updated if the fix touched an entry (move 7). The
                   fresh Réalisateur must "rewrite the report" — whose
                   `## Symbols` covers the whole lot — while told not to
                   revisit the rest of the lot and not given the
                   previous `compte-rendu.md` among its reads.
    Le défaut    : Plane 2, question 1 (the row reaches less than the
                   run it replaces) and question 2 (a fact — the
                   previous report — nothing gives it).
    Ce qu'il faut: a FAIL mineur narrows what is coded, not where the
                   run ends: it finishes with moves 6 to 8 and the
                   report, like any run. The previous report is an
                   input on a FAIL, read and amended rather than
                   rewritten from the code. On either FAIL kind, the
                   entries the failed attempt wrote to the state
                   document are the fresh run's to correct or remove —
                   its `## State` field says what it did to them.
                   (This last point was added after reading the
                   verdict — its item 16; the planes did not turn it
                   up.)
    Justification: robustness. A fix that is not committed in the
                   worktree is not merged — the Relecteur passes a lot
                   whose fix does not exist on master. Tokens: without
                   the previous report the agent re-derives the whole
                   symbol list from the code, against the instruction
                   not to revisit it.

### 12

    Fichier      : .claude/agents/realisateur.md, and
                   .claude/commands/8_code.md (loop step 2 and 3,
                   "Invocation parameters")
    Cible        : agent — Part 2 opening ("First thing, every run:
                   look for blocked_realisateur.md … And look for
                   reprise_realisateur.md"), the verdict row in Part
                   1's table ("only when you resume a FAIL"). Command —
                   "If reprise_realisateur.md is there, name it in the
                   Réalisateur's prompt … Without it, it starts the lot
                   again"; "On FAIL → a fresh realisateur, with the
                   verdict"; the single prompt shape shown.
    Aujourd'hui  : the agent finds the blocking file and the reprise
                   file itself; the command believes the reprise must
                   be named or the agent restarts the lot. For the FAIL
                   case, neither side says how the agent knows: the
                   command says "with the verdict" without saying
                   whether that is a file named in the prompt or its
                   content pasted, and the agent never looks for
                   `verdict.md` on its own — while stating that a
                   `verdict.md` may exist on a lot it resumes for
                   another reason (a block on a PASS lot).
    Le défaut    : Plane 2, question 2 (which call this is, on FAIL,
                   rests on a fact nothing gives); command question 2
                   (the prompt does not carry what the FAIL path
                   needs; it names a thing — the reprise — the agent
                   finds by itself).
    Ce qu'il faut: one mechanism for all three resume cases, on one
                   side. Either the agent detects them all from the
                   folder — blocking file, reprise, and a `verdict.md`
                   whose status is a FAIL — and the prompt carries only
                   the working folder and the lot; or the prompt states
                   the case and the file to read, and the agent's own
                   look-ups go. Not a mix that each side believes the
                   other performs.
    Justification: robustness. An agent not told it resumes a FAIL
                   codes the lot from move 1 over a PASS-or-FAIL tree
                   it did not read the verdict of; the retry ceiling is
                   spent on runs that never saw the point reported.

### 13

    Fichier      : .claude/commands/8_code.md ("Where to resume") and
                   .claude/agents/realisateur.md (Part 2 table row "A
                   ## Decision still empty → Call the Arbitre on it")
    Cible        : as named
    Aujourd'hui  : the command resumes on "the first lot in the
                   sequence with no verdict.md carrying PASS" and
                   invokes the Réalisateur; it reads nothing else
                   first. A lot stopped on an empty `## Decision` that
                   the Product Owner has not yet filled is exactly that
                   lot, so a re-run of `/8_code` launches a Réalisateur
                   on it. The agent's row then calls the Arbitre again
                   — while the command holds that "a block that reaches
                   you has already been through it — sending it again
                   would ask twice".
    Le défaut    : command question 1 (a case — re-run before the
                   decision is written — with no row before the
                   invocation); Plane 1 on the agent (a row whose only
                   reachable case the command says must not happen).
    Ce qu'il faut: before invoking on the resume lot, the command
                   checks for a `blocked_realisateur.md` (and the other
                   agents' equivalents) with an empty `## Decision` and
                   stops there, relaying that the decision is still to
                   write. The agent's row then covers no reachable case
                   and goes — or stays as a guard that stops without
                   calling anyone.
    Justification: round trips. Each premature re-run costs a
                   Réalisateur invocation, an Arbitre invocation and
                   its polling of the Product Owner, to end where the
                   last run ended.

### 14

    Fichier      : .claude/commands/8_code.md ("What you read", "Where
                   you stop and hand back" — "A filled ## Decision is
                   not a stop … Even on a lot already carrying a PASS")
    Cible        : as named
    Aujourd'hui  : the command reads `sequence.md` and each
                   `verdict.md`'s status, "nothing else". It never globs
                   `code/*/blocked_*.md`, yet routes on a filled
                   decision found on a lot that carries a PASS — a lot
                   the resume rule skips. After the Réalisateur applies
                   it, the command does not say the Relecteur runs; the
                   agent assumes it does ("the verdict gets rewritten
                   when the Relecteur runs again").
    Le défaut    : command question 1 (a row for an outcome the
                   command has no read to detect, and an outcome —
                   re-review of the PASS lot — with no row).
    Ce qu'il faut: the command's reading list includes the blocking
                   files, so the routing it describes is reachable; and
                   a decision applied on a PASS lot is followed by the
                   Relecteur, its verdict replaced, the lot counted or
                   not as the command decides.
    Justification: robustness. A decision written by the Product
                   Owner on a PASS lot is never picked up, or is applied
                   and never re-reviewed — the intention the Contrôleur
                   reported missing is coded and nobody checks it.

### 15

    Fichier      : .claude/agents/realisateur.md
    Cible        : "Then call the Arbitre, and wait" — table row
                   "Filled, and it sends the lot back to the split"; the
                   same row in Part 2
    Aujourd'hui  : the agent must recognise a decision that sends the
                   lot back to the split, from the prose of
                   `## Decision`. No marker is named. The command names
                   one: "The Arbitre wrote code/redecoupage.md".
    Le défaut    : Plane 2, question 1 — two readers cannot check the
                   test the same way; the agent's most destructive
                   branch ("Drop everything you wrote") hangs on a
                   reading of free text.
    Ce qu'il faut: the test is a checkable one, the same on both
                   sides: the agent drops its work when the trace the
                   command already relies on is present, and not on a
                   reading of the decision's wording. What that trace
                   is, and whether the Arbitre writes it, is the
                   Arbitre's file — see the last section.
    Justification: robustness. A decision read as "back to the split"
                   when it is not discards a lot's code; read the other
                   way, the agent commits code against a lot that is
                   about to be recut.

### 16

    Fichier      : .claude/commands/8_code.md (loop step 3 "Three
                   retries maximum per lot, all FAIL types counted
                   together"; "A lot fails three times → stop")
    Cible        : as named
    Aujourd'hui  : the count lives in the running command's memory.
                   `verdict.md` is rewritten at each review; nothing on
                   disk says how many times the lot failed. A run that
                   stops for any other reason and is restarted counts
                   from zero.
    Le défaut    : known pattern "a loop with no ceiling" — the
                   ceiling exists per run, not per lot; command
                   question 1 (the row "fails three times" cannot be
                   reached across runs).
    Ce qu'il faut: the retry count is on disk, in the lot's folder or
                   in the verdict, and the ceiling is read from there.
                   Whose file carries it — the command's own marker or
                   the Relecteur's verdict — is left open.
    Justification: round trips and tokens. A lot that cannot pass is
                   retried three times per run, for as many runs as the
                   Product Owner launches, with no signal that it is
                   the same failure.

### 17

    Fichier      : .claude/commands/8_code.md
    Cible        : "Where to resume" ("No such lot — every one carries
                   a PASS — go straight to the Contrôleur, then stop");
                   "Where you stop" ("The Contrôleur has finished — the
                   gap report is to be read"); against the header ("It
                   never invokes the Contrôleur") and the end of the
                   loop ("say that /9_controle is what comes next — run
                   by hand")
    Aujourd'hui  : two passages invoke the Contrôleur and stop on its
                   report; two others say the command never does, and
                   tells the Product Owner to run `/9_controle` by
                   hand.
    Le défaut    : command question 1 — the row the Product Owner is
                   given after the last lot passes points two ways.
                   Outside this agent's own outcomes, but it is the row
                   that follows them.
    Ce qu'il faut: one behaviour at "every lot carries a PASS". Given
                   the header's reason (the Contrôleur needs a grouping
                   this command does not hold), the two invoking
                   passages are the stale ones.
    Justification: round trips. An orchestrator following the first
                   passage invokes an agent without the inputs it needs
                   and hands the Product Owner a report to read that
                   does not exist.

### 18

    Fichier      : .claude/agents/realisateur.md
    Cible        : move 6's parenthesis "(41 of 149 runs found nothing,
                   measured over ten steps.)"; "This document commands
                   the Cadreur" (Updating the technical state); the
                   duplicated "no rationale for a choice — it is in the
                   sheet, not to repeat" (twice in "What you write");
                   the words "provider" (move 6, state section) and
                   "analyze" (frontmatter, `## Build` example)
    Aujourd'hui  : a measurement explaining why a rule came to be; a
                   sentence about another agent that changes nothing
                   the Réalisateur does; the same rule stated twice
                   eight lines apart; two words from one framework's
                   vocabulary in rules meant to run on several
                   projects.
    Le défaut    : Plane 3, criterion 5 (commentary on why it came to
                   be, useless justification, duplication) and
                   criterion 6 (framework vocabulary).
    Ce qu'il faut: the rule without its history; one statement of the
                   no-rationale rule; "static analysis" and a neutral
                   word for the unit of work ("a screen and its state
                   holder", or drop the example) where the framework
                   words are.
    Justification: tokens, at every invocation. Small, and the only
                   measure these move — listed because criteria 5 and 6
                   are the ones the pass says the rules are written
                   against.

---

## From the verdict

Read after the comments above. Items are those of sections 2, 4–7
that name the Réalisateur.

**Section 2 — "writes the tests for its own criteria … in the context
that just chose an interpretation; the tests seam is the one to
move" (estimate).**
Not found — it is a design question, not a defect of the file, and it
moves no measure this pass can name from one agent. What the agent
says: move 4 implements, move 5 writes the tests; the tests come after
the bodies, from the criteria, in the same context. See item 22 below.

**D12 / item 2 — does the Réalisateur read the conventions whole, or
only what the sheet names?**
Already found — comment 7. To be exact: the agent holds both readings
at once. "What you read" lists `docs/TECHNICAL_CONVENTIONS.md`
unqualified, and "Conventions and language" says "The sheet's
`## Conventions` names the rules bearing on this lot — open each one
and hold it. Naming them is the Détailleur's job, holding them is
yours." Neither passage excludes the other; the verdict's "one of the
two is what the agent does" is not decided by the file.

**D16 — the lot that asks for a convention is coded under the old
rule, and nothing records it.**
Contradicted in part. The agent's report carries a `## Requests`
field: "names the conventions requests this lot wrote, or a dash — the
file itself carries what they say." The asking lot is therefore
traceable from its own report, which the verdict's sweep says the next
block's Détailleur greps. What the verdict says is absent — a mark in
the verdict or the technical state — is indeed absent from this file.
Comment 8 bears on the same seam from the other side: for a convention
that decides how the code is written, "carry on under the old rule" is
the wrong path altogether.

**D17 / item 13 — rename or delete a settled blocking file?**
Already found — comment 2. The exact state: this one agent does both.
Rename, three times ("rename the file `blocked_realisateur-NN.md`";
the Part 2 table; "Renaming means renaming — never write the numbered
one and leave something at the old name"), then "🔴 Delete the file
once applied" as the section's last line. The verdict counted it among
the renamers; it is also one of the deleters.

**D19 — the build claim has one producer and no independent
execution.**
Not found — the second execution would sit in the command or the
Relecteur, not in this agent. What the agent says: "Run the static
analysis and the tests — until both pass", one command at a time in
the foreground, and the report's `## Build` carries the result as two
lines of prose ("analyze: clean / test: 47 passed"). Nothing in the
file makes that claim checkable by a reader other than by re-running.

**D21 — the technical state's reader list omits the Cadreur, whom the
prose says it commands.**
Not found as a defect of this agent. The agent repeats the sentence
("⚠️ This document commands the Cadreur") and does nothing with it;
comment 18 lists it as commentary. Whether the Cadreur reads the
document is `cadreur.md`'s to say.

**D22 / P11 — "what a lot made false disappears" requires a reading
the Réalisateur does not do.**
Already found — comment 6, with a precision the verdict lacked. The
verdict describes the agent as reading "two sections whole, greps the
rest". The body of the agent reads two sections and nothing else
("Those two only — the rest is an inventory"); only the never-do entry
says "two sections, then greps by symbol". So the reading the verdict
assumes exists in the agent's prohibitions list and not in its moves.

**Item 16 — does a fresh Réalisateur after a FAIL remove what the
failed attempt wrote to the state document?**
Not found by the planes; added to comment 11 after reading. What the
agent says: nothing. The FAIL mineur row ends at "rewrite the report"
and names the state document nowhere; FAIL structurel says "from move
1", which reaches move 7, but "What your lot made false disappears"
speaks of what the lot changed in the code, not of what a previous
attempt wrote in the document. As written, an entry describing
discarded code stays.

**Item 22 — tests before or after the bodies?**
Not found — a design question. What the agent says: after. Move 4
"Implement in the sheet's dependency order", move 5 "Write one test
per acceptance criterion". The verdict's consequence follows: the
Relecteur's assertion check (its item 8) is the only guard.

**A6 / P10 — the sheet is self-sufficient; the Réalisateur blocks when
it is not.**
Confirmed by the agent: "The sheet is self-sufficient — if it is not,
it is wrong, and that is a blocker", and "Never the technical
document, the lot list, or the sequence." Holds as described; comment
5 is about the word used at the trigger, not the rule.

**U10 — Arbitre waiting on the person; the Réalisateur stops with
`reprise_realisateur.md`, compiling code committed.**
Already found, and sharpened — comment 3. The agent matches the
description ("Commit what compiles before you stop — never commit what
does not"), and the description's consequence is the defect: what does
not compile is described in `En chantier` and left uncommitted in a
worktree the command removes. The verdict's sweep row 52 marks the
reprise "wired"; its most important field points at code the next
reader cannot see. On the wait itself the agent agrees with the
verdict: the poll is the Arbitre's, the Réalisateur's wait is unbounded
and unpolled.

**A-2 — Réalisateur ⇄ analysis and tests, no bound.**
Already found — comment 10.

**A-3 — Réalisateur ⇄ Relecteur, three retakes, "sound".**
Partly contradicted — comment 16. The bound is sound within one run of
`/8_code` and does not exist across runs: nothing on disk counts the
FAILs, so a restarted command counts from zero on the same lot.

**A-6 — the redecoupage loop; "the agent drops its work".**
Already found from the agent's side — comment 15. The drop is the
agent's most destructive branch and hangs on a reading of the
`## Decision` prose; the command relies on `code/redecoupage.md` and
the agent never names it. Comment 1 adds that the whitelist gives the
agent no shell command to drop with.

**Sweep row 34 / P14 — `architecte/<demande>.md`, produced by the
Réalisateur among others.**
Consistent with the agent ("Write `architecte/realisateur-<lot>.md` in
the working folder … `## Verdict` left empty"). One thing the sweep
does not show: the agent names two triggers for a request — "A
convention you find wrong" (Conventions and language) and "A condition
of running that nothing states" (When the conventions fall short) —
and the second section's scope and "You never block on this" are
written for the second trigger only. Comment 8.

---

## What another agent would settle

**How a decision that sends the lot back to the split is recognised —
by the wording of `## Decision`, by the presence of
`code/redecoupage.md`, or both.**
`arbitre.md`. If the Arbitre always writes `code/redecoupage.md` in
that case: comment 15 reduces to naming that file as the agent's test.
If it only writes it sometimes, or the decision's wording is the only
trace: the agent needs a fixed marker in the decision, and the Arbitre
is where it would be written.

**Whether the Arbitre reads the numbered `blocked_realisateur-NN.md`
files before settling.**
`arbitre.md`. Yes (the verdict says so): comment 2's rename has a
second reader beyond this agent's own later runs, and deletion costs
the Arbitre its widening rule. No: comment 2 stands on this agent's
own reading alone ("read them, they say what was already decided"),
and the audit commands' examples name the numbered files as well.

**Whether the Arbitre's prompt needs more than the working folder and
the blocking file path — the lot name is in the path, the sheet is
beside it.**
`arbitre.md`. Needs more: the invocation block in this agent is short
of an input and every mid-lot block starts with the Arbitre lacking
it. Enough: nothing to change.

**What `verdict.md` carries: a status line the agent could detect a
FAIL from; for a FAIL mineur, the file and test the point sits in; an
attempt count.**
`relecteur.md`. Status line present: comment 12's "the agent detects
the case itself" branch is available. Absent: only the prompt can say
which call this is. Attempt count present: comment 16 closes on the
command reading it. Absent: the command needs its own marker.

**Whether the Relecteur reads the numbered blocking files, or only the
report and the sheet, when comparing symbols.**
`relecteur.md`. Reads them: comment 4's new report field is a
convenience, and a decided divergence is already visible to it. Does
not: the report field is the only channel by which a decided signature
is told apart from drift, and comment 4 is load-bearing.

**Whether the conventions file carries, in named sections, the code
folders to grep, the analysis and test commands, and the states a lot
may be delivered in.**
`architecte.md` and the `/conventions` command. Yes, in stable
sections: comments 1 and 7 can name those sections as always-read, and
"one the conventions name" in the whitelist is checkable. No: the
Réalisateur guesses its own commands and folders on a project where the
file is silent, and comment 8's block path is reached on the first lot.

**Whether the sheet's `## Conventions` names every rule that bears on
the lot, including where the code goes, or only the coding rules.**
`detailleur.md`. Everything: comment 7 resolves to "the sheet's rules
plus nothing", and the whole-file read is the redundant one. Coding
rules only: the whole-file read is required and the sheet's list is a
reminder.

**Whether the sheet's fields are literally `## Dependencies`,
`## Conventions` and `Modifies`, and whether the sheet lists the
existing tests a modification makes false.**
`detailleur.md`. Names match: the agent's references hold. They do
not: the agent points at fields the Détailleur does not write, and
move 4's order and comment 4's `## Outside the lot` rest on nothing.
Tests listed: move 5's "adapt them" has an input. Not listed: the
agent finds them by grep in folders the conventions must name.

**Whether the technical-state format files traps under subjects, so
that `## Traps — general` has non-general siblings the agent never
reads.**
The `technical-state-format` skill, and `detailleur.md`, which reads
the same document. Yes: comment 6's grep-by-symbol is the only way a
lot meets the trap on its own subject, and its absence is a robustness
gap on every modifying lot. No: the two sections are the whole of the
traps, and comment 6 reduces to the stale-entry grep and the dangling
"see below".

**Whether the Relecteur compares each test's assertion to its
criterion's outcome, or counts tests per criterion.**
`relecteur.md` — the verdict's item 8, restated from this side because
the agent writes the tests after the bodies (verdict item 22). Assertion
compared: the tests-after order costs nothing this pass can measure.
Counted only: a test that asserts the code rather than the criterion
passes, and the order of moves 4 and 5 becomes a robustness question
for the group pass.

**Whether the Contrôleur's blocking file on a PASS lot names the
Réalisateur, and who writes it.**
`controleur.md` and `/9_controle`. If a `blocked_realisateur.md` can
appear on a PASS lot from that route: comment 14's detection and
re-review are needed in the command. If the route produces a different
artefact: the agent's paragraph "A blocking file can target a lot
already carrying a PASS" describes a case that does not occur as
written.

