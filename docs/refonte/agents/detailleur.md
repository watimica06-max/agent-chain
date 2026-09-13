# detailleur — phase 3 examination

Files read: `.claude/agents/detailleur.md` (whole), `.claude/commands/8_code.md`
(whole — the only command that invokes it; `cycle.md`, `audit_blocages.md` and
`socle.md` name the detailleur without invoking it).

## Plane 1 — the agent as a whole

**Role, from the file**: for every lot of one block, turn the rules of the
entries the lot cites into a spec sheet — signatures, acceptance criteria,
dependencies, conventions to hold, requests raised — that the Réalisateur
codes from without deciding anything; walk the whole block before writing
any sheet; block through the Arbitre; and rewrite the sheets a divergence
made false.

**Moves, in the order the file runs them:**

| # | Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|---|
| R | PART 2 — look for `blocked_detailleur.md` on every lot, act on its `## Decision` | Resumes a block left on a decision; without it a settled block is re-asked | The walk (a decision replaces an entry's rule) | Row 2 of its table re-enters "When you cannot produce" |
| W | Walk — open every cited entry of every lot, look for anything that stops | Avoids detailing lots whose sheets a redécoupage deletes | Moves 1–3 (the reading is done) | Move 1 is declared identical to it |
| 1 | Open every entry the lot cites, whole | The rules come from there | Moves 3, 7 | Fully covered by W (the file says so) |
| 2 | Read `## Traps — general` and `## Dead state` of the state document, whole | A trap changes a signature | Move 3 | Block-invariant, yet placed per lot |
| 3 | Derive a signature per rule | The sheet's first field | Move 6 | — |
| 4 | Grep every symbol on the code folders | A false symbol contaminates the block | Move 6, `## Dependencies` | Grep of the state document per symbol is implied here but written in move 2 |
| 5 | Grep the cycle's reports for every symbol found | Distinguish "produced this cycle" from "pre-existing" | `## Dependencies` only | Partly the `## Symbols` inventory already read |
| 6 | Write the signature | Sheet | Réalisateur, Relecteur | — |
| 7 | Write the acceptance criteria | Sheet | Réalisateur (one test each), Relecteur | — |
| 8 | Name the conventions the lot must hold | Sheet | Réalisateur, Relecteur | — |
| B | Block: write `blocked_detailleur.md`, call the Arbitre, wait, act | The only exit that does not guess | Orchestrator, Arbitre, PART 2 of the next run | — |
| C | Conventions request: write `architecte/detailleur-<lot>.md`, carry on | A missing convention reaches the Architecte | `## Requests`, command move 6 | — |
| D | Divergence mode: rewrite the sheets of the named uncoded lots | Sheets written against a signature the code does not carry | Réalisateur of the next lots | Unspecified which of R, W, 1–8 it runs |

**Judging the set.** Every move but 5 feeds a field something downstream
reads. Move 5 feeds one label in `## Dependencies` whose reader I cannot
name from this file (see the last section). The role is covered, with
three seams: the walk promises to catch every stop but only performs the
reading half of what stops the agent (moves 4 and 5 stop too); nothing
says what to do with a lot that already carries a sheet; and mode D says
what to rewrite but not which moves it runs. The order is right except
move 2, which is block-invariant and sits inside the per-lot loop, and
the pointers "see below" for signatures and criteria, which point at
sections that sit above. No move can go without breaking something,
except possibly move 5 (tokens), pending the question left to the group
pass.

## Comments — to apply top to bottom

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 2, the two rules at "Renaming is what closes it —
                   never delete it" and "Delete the file once applied"
    Aujourd'hui  : line 433: "Renaming is what closes it — 🔴 never delete
                   it. The numbered ones are the record". Line 444, same
                   section: "🔴 Delete the file once applied. A blocking
                   file left behind would stop the next run".
    Le défaut    : Plane 1, order/consistency — two passages of one agent
                   asking for opposite things; Plane 2 Q4, an instruction
                   that reads two ways.
    Ce qu'il faut: one rule: a settled file is renamed to its numbered
                   form and never deleted. The second passage's concern
                   (a file left behind stops the next run) is already met
                   by the renaming rule two paragraphs above it.
    Justification: robustness — one reading deletes the record the next
                   run and audit_blocages read; the other leaves a file
                   the agent itself says re-blocks the next run. Either
                   way the agent picks.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 2, table row "A ## Decision sending the lot back
                   to the split → Stop. The split has not been redone"
    Aujourd'hui  : the row asserts the split has not been redone, with no
                   test. The command runs /7_lots immediately on a
                   redécoupage, so on the next invocation the split
                   usually has been redone — and the unnumbered file,
                   if nobody closed it, is still there.
    Le défaut    : Plane 2 Q1 — no test two readers apply the same way;
                   Q3 — the case "split redone, file still standing" is
                   unforeseen, and the agent stops on a settled block.
    Ce qu'il faut: the row needs an observable test for "the split has
                   been redone since" (the file the Arbitre wrote,
                   `code/redecoupage.md`, gone or consumed; or the lot
                   list's date/version past the decision), and a rule for
                   the redone case: rename the file to its numbered form
                   and detail the block. Who closes that file is named in
                   the last section.
    Justification: round trips — without the test, every run on a block
                   that once went back to the split stops and asks; the
                   command then has no row for that message (see command
                   comments).

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, "First, walk the whole block" and "Write a sheet
                   for every lot of the block"
    Aujourd'hui  : nothing on a lot of the block that already carries a
                   `code/<lot>/fiche-executable.md`. The command asserts
                   "a Détailleur that finds a sheet does not rewrite it"
                   (8_code line 205) — the agent never says so.
    Le défaut    : Plane 2 Q3 — a situation the move meets (partial block:
                   a run that ended mid-block, a divergence rewrite, a
                   redécoupage where the command deleted only the sheets
                   of uncoded lots) and does not foresee. The agent will
                   either overwrite or skip, by chance.
    Ce qu'il faut: an explicit rule in the walk: a lot that already has a
                   sheet and no PASS verdict is either skipped (the
                   command's assumption) or rewritten — one of the two,
                   stated; a lot with a PASS verdict is never touched
                   (already a never-do). The command's move 1 must then
                   match it (see command comments).
    Justification: robustness — a rewritten sheet on a half-coded block
                   changes the signature the next lots were about to
                   consume; a skipped stale sheet codes the old split.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, "First, walk the whole block" — what the walk
                   looks for — and "Then call the Arbitre", the line
                   "You have written no sheet at this point"
    Aujourd'hui  : the walk is "the same reading move 1 does" and "what
                   stops you shows in the entries". But two of the three
                   declared block causes — a grep contradicting the lot's
                   declaration (Production or modification), a type nobody
                   declares (move 4, last row) — show only in greps, which
                   run in move 4, after the sheets of the earlier lots are
                   written. "You have written no sheet at this point" is
                   then false, and nothing says what becomes of the sheets
                   already written when the Arbitre sends the lot back.
    Le défaut    : Plane 1 — two passages asking for different things
                   (walk catches everything / move 4 stops); Plane 2 Q1 —
                   the walk reaches less than it claims; Q3 — a block
                   arriving mid-block is unforeseen.
    Ce qu'il faut: the walk must include the cheap grep half: for every
                   lot, one grep of the symbol the lot declares as
                   produced or modified, on the code folders — enough to
                   catch both grep-based causes before any sheet exists.
                   And a sentence for the residual case (a stop found at
                   move 4 on a later lot): the sheets already written
                   stand; the command deletes them if the split changes.
    Justification: round trips — the file's own arithmetic: "eight lots
                   detailed twice"; robustness — an unforeseen mid-block
                   stop makes the agent decide what to do with its own
                   sheets.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : "When you cannot produce" and "Then call the Arbitre"
    Aujourd'hui  : "Write code/<lot>/blocked_detailleur.md" — one file,
                   one lot; "Invoke arbitre on the file you just wrote" —
                   one call. The walk covers every lot and can find a
                   stop on several.
    Le défaut    : Plane 2 Q3 — several stops in one walk is the case the
                   walk was built to find, and it is not foreseen: one
                   file for all? one per lot, called in sequence? all
                   written, then called? Applying the first decision
                   before the second is raised changes what the second
                   asks.
    Ce qu'il faut: state it: every stop the walk finds is filed, one
                   blocking file per lot; the Arbitre is called once per
                   file, sequentially; no decision is applied and no
                   sheet written until every file has come back; one
                   "back to the split" among them ends the invocation
                   without sheets.
    Justification: round trips — otherwise the second stop surfaces on
                   the next run, one whole invocation later; robustness —
                   the agent inventing the shape of a multi-lot block.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : "What you read", the `code/sequence.md` bullet, its
                   `## Defects` clause
    Aujourd'hui  : "a defect naming a lot of your block means the split
                   was not corrected — stop and report rather than
                   detailing against it". The command already stops on a
                   non-empty `## Defects` before invoking anything
                   (8_code, "Where to resume"), and stops again if
                   /7_lots returns a defect. "Stop and report" has no
                   form — not the blocking file, not anything named.
    Le défaut    : known failure "a net: a move re-checking what an
                   earlier agent already guaranteed"; Plane 2 Q3 — a stop
                   with no shape, so the agent invents one.
    Ce qu'il faut: either drop the clause (what breaks: nothing — the
                   command guards it at both entries), or keep it and
                   give it the blocking-file form so that the command's
                   stop rows recognise it. Dropping is the cleaner.
    Justification: robustness — an unshaped report is a message the
                   orchestrator has no row for; tokens — negligible.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 2 — its place in "The eight moves, per lot
                   of the block"
    Aujourd'hui  : move 2 reads the two open sections of the state
                   document, whole, inside the per-lot loop. The sections
                   do not change between lots; the walk, which reads
                   everything else move 1 opens, does not read them.
    Le défaut    : Plane 2 Q2 — the same thing read once per lot, paid at
                   every invocation; Plane 1 order — a block-invariant
                   read placed in a per-lot loop.
    Ce qu'il faut: move 2 runs once, in the walk (or just before the
                   per-lot loop), and the per-lot list starts at move 3.
    Justification: tokens — two sections times the number of lots of the
                   block, on opus, per invocation.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 4 — "Every code search targets the code
                   folders the conventions name … never a bare pattern",
                   and "A trap owned by a symbol comes back with it — the
                   state document files it under that symbol"
    Aujourd'hui  : the per-symbol grep of `docs/CURRENT_TECHNICAL_STATE.md`
                   is announced in move 2 ("the rest of that file you grep,
                   symbol by symbol") — before any symbol is known — and
                   move 4, where the symbols are known, restricts every
                   search to the code folders. Read literally, the trap
                   "comes back" from a grep no move runs.
    Le défaut    : Plane 2 Q1 — the move reaches less than it claims (one
                   source where two carry the thing); Plane 1 order — a
                   constraint stated in a move that cannot yet apply it.
    Ce qu'il faut: move 4 names two greps per symbol: the code folders
                   the conventions name, and the state document; move 2
                   loses its forward reference.
    Justification: robustness — a symbol-owned trap not seen is a
                   signature the state document says is wrong, caught at
                   review or later.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 4 — "the code folders the conventions
                   name"
    Aujourd'hui  : the rule rests on the conventions naming the code
                   folders. `TECHNICAL_CONVENTIONS.md` is written by hand
                   on a new project (socle says so) and nothing here
                   foresees the folders being absent from it.
    Le défaut    : Plane 2 Q2 — a move resting on a fact nothing
                   guarantees; Q3 — the case is unforeseen, and the
                   alternative the file itself names (a bare grep) returns
                   docs and build output as code.
    Ce qu'il faut: a foreseen fallback, one of: a conventions request
                   (this is exactly "a property no rule imposes"), or a
                   stop. Not a bare grep.
    Justification: robustness — a bare grep finds a symbol in an old plan
                   and the sheet reuses a type that does not exist.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 4, the grep table, row "Not found, and an
                   earlier lot of the sequence produces it — Legitimate"
    Aujourd'hui  : the row treats a symbol promised by an earlier lot and
                   absent from the code as legitimate. The command details
                   a block only when every lot before it carries a PASS
                   (next lot = first without PASS; block detailed when
                   reached). So at detailing time, an earlier lot of a
                   previous block has been coded and reviewed: its symbol
                   is in the code or was never built — or built under
                   another name. The row above it already covers earlier
                   lots of this block.
    Le défaut    : Plane 3 criterion 3 — the row reads well and guards
                   the wrong thing: it passes exactly the case where the
                   sheet is about to be written against a phantom.
    Ce qu'il faut: for a producer in an earlier block, "not found" is
                   the last row (stop, or at least a blocking file naming
                   the lot that promised it). The row stays only for an
                   earlier lot of the same block — which the row above
                   already says. Holds if blocks are contiguous in the
                   sequence — see the last section.
    Justification: robustness — a signature consuming a symbol the code
                   does not carry fails at the Réalisateur's first
                   compile, one lot later, with a blocking file that
                   points at the wrong lot.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 5 — `Grep(pattern: "<symbol>", glob:
                   "**/compte-rendu.md")`
    Aujourd'hui  : a bare glob, no path: it sweeps every feature folder
                   of the repository and every earlier cycle, including
                   the parent feature's reports on a bug-fix cycle. A hit
                   from another feature reads as "an earlier lot of this
                   cycle created it". The fallback ("grep code/") is
                   scoped; the primary is not.
    Le défaut    : Plane 2 Q1 — the move reaches more than it says ("this
                   cycle's reports"), and the table's two verdicts depend
                   on that scope.
    Ce qu'il faut: the primary grep is scoped to the working folder's
                   `code/`, like the fallback.
    Justification: robustness — a symbol classified "produced this
                   cycle" that is in fact pre-existing enters
                   `## Dependencies` with the wrong provenance; tokens —
                   a repository-wide glob on every found symbol.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 5 as a whole
    Aujourd'hui  : one grep per symbol found in the code, on every lot.
                   Both outcomes lead to the same act (reuse, never
                   redeclare); the only thing the result changes is the
                   label in `## Dependencies`. The `## Symbols` inventory
                   of the lot list, already read, says which lot produces
                   a declared symbol; move 5's own justification says it
                   is for the undeclared ones only ("what no split
                   declared").
    Le défaut    : Plane 1 — a move whose result nothing in this file
                   carries forward but a label; known failure "work done
                   twice" for every symbol `## Symbols` already places.
    Ce qu'il faut: at minimum, move 5 runs only on a found symbol that
                   `## Symbols` does not place. Whether it can go entirely
                   depends on who reads the "pre-existing / produced by
                   lot-NN" label — left to the group pass.
    Justification: tokens — one grep per found symbol per lot, most of
                   them answering what the inventory already says.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 6, and the `## Dependencies` field of the
                   sheet
    Aujourd'hui  : the sheet has five fields; moves 6, 7, 8 and section
                   "When the conventions fall short" fill four. No move
                   says to write `## Dependencies`, nor from what — its
                   content is inferable from the move 4 and 5 tables, and
                   only from there.
    Le défaut    : Plane 1 — a job falling between two moves; Plane 2
                   Q4 — a reader who has seen nothing else has no rule
                   for what fills it.
    Ce qu'il faut: move 6 (or a move of its own) writes `## Dependencies`
                   from the classification moves 4 and 5 produced: one
                   line per type the signature uses that this lot does
                   not produce, with its provenance.
    Justification: robustness — a field filled by inference varies
                   between runs, and the Relecteur checks the sheet.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : "When a verdict sends the block back" (end of PART 3)
    Aujourd'hui  : "Inputs: the same, plus the verdict naming the affected
                   lots. Rewrite only those sheets, against the signature
                   the code actually carries — grep it." Nothing says
                   whether PART 2 runs, whether the walk runs (the
                   never-do "write a sheet before walking the whole block"
                   applies literally and would re-walk lots it will not
                   touch), which of moves 3–8 run, or what "the verdict"
                   is on disk (no path anywhere; the command already names
                   the lots in the prompt).
    Le défaut    : Plane 2 Q4 — a mode a reader cannot run from the file;
                   Q2 — an input named without a path and duplicated by
                   the prompt.
    Ce qu'il faut: this mode is defined as a list against the normal run:
                   PART 2 check yes; no re-walk of the entries (the coded
                   lot's code is the ground); moves 3–8 on the named lots
                   only, with the diverged symbol taken from the code by
                   grep; plus one read the normal run never needs — the
                   block's other uncoded sheets, so a symbol two sheets
                   share is rewritten the same way in both (refined after
                   the verdict, item 21); the affected lots come from the
                   prompt, and the verdict file is not an input — or it
                   is, with its path in the on-disk table.
    Justification: robustness — an under-specified mode on the one
                   occasion the chain has just proved a sheet false;
                   tokens — a full re-walk of a block to rewrite two
                   sheets.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 1, the "Referred to as / On disk" table
    Aujourd'hui  : four rows: lot list, sequence, technical document,
                   spec sheet. The file also names "the reports of this
                   cycle's coded lots" (on disk only inside move 5's grep
                   pattern, `compte-rendu.md`, never with its folder), and
                   "the verdict" (never on disk).
    Le défaut    : Plane 2 Q4 — a file named without a path.
    Ce qu'il faut: every file the agent touches, even by grep, has a row;
                   the report at least, the verdict if the previous
                   comment keeps it as an input.
    Justification: robustness — a path guessed is a glob widened, and
                   move 5's scope error above is the visible consequence.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 3, move 3 ("work out a signature — see below") and
                   move 7 ("Write the acceptance criteria — see below")
    Aujourd'hui  : both sections referred to sit in PART 1, above; what
                   sits below is the divergence mode.
    Le défaut    : Plane 2 Q4 — a reference that no longer matches the
                   layout.
    Ce qu'il faut: name the section ("Deriving a signature from a rule",
                   "Writing an acceptance criterion") rather than a
                   direction.
    Justification: robustness, small — a reader who follows "below"
                   lands on the wrong section; no other measure.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : PART 1, "Deriving a signature" — the Written / Not
                   enough table; "What you write" — the `## Conventions`
                   example line "a rule needing a Context is in the wrong
                   module"
    Aujourd'hui  : the examples are written in one platform's vocabulary:
                   `Flow<Profile?>`, `Flow<List<Race>>`, `Long`,
                   `Context`. The file says the chain runs on several
                   projects (paths never hardcoded, "on a new application
                   almost every type" is a framework's).
    Le défaut    : Plane 3 criterion 6 — the words of one language and
                   one framework; the rule the table illustrates (edges:
                   absence, emptiness, bound, unit, order) is itself
                   general.
    Ce qu'il faut: the same three rows with neutral shapes — a nullable
                   stream, a list, a signed duration — or the rule alone,
                   which is already complete at "absence, emptiness, a
                   bound, a unit, an order".
    Justification: round trips, small — a type name copied from the
                   example on a project that has no such type is caught
                   by move 4 as "not found" and becomes a false stop.

---

    Fichier      : .claude/agents/detailleur.md
    Cible        : the justification passages: "Writing an acceptance
                   criterion" lines "The second kind is the one that goes
                   missing … no calculation fails without it"; "First,
                   walk the whole block" paragraph "Why nothing first,
                   rather than what you can" and the one after; "What you
                   read" line "The Vérificateur read these same sections —
                   not a duplicate"; "Deriving a signature" the paragraph
                   "The sheet says it, it does not decide it"
    Aujourd'hui  : each explains why the rule beside it came to be; none
                   adds a case or a test the rule does not already carry.
    Le défaut    : Plane 3 criterion 5.
    Ce qu'il faut: the rules stand alone. (One exception worth keeping
                   is the arithmetic "eight lots detailed twice" if the
                   walk comment above is applied, since it becomes the
                   rule's own test.)
    Justification: tokens — read on opus at every invocation; nothing
                   else moves.

---

    Fichier      : .claude/commands/8_code.md
    Cible        : "The loop, per lot", move 1
    Aujourd'hui  : "If the lot's block has no sheets → detailleur on that
                   block." A block with some sheets and a current lot
                   without one (a run that ended mid-block; a redécoupage
                   that deleted only the uncoded lots' sheets while the
                   block kept coded ones) fails the test, and move 2 runs
                   the Réalisateur on a lot with no sheet.
    Le défaut    : command question 1 — an outcome (partial block) with
                   no row; Plane 2 Q1 — a test on the block where the
                   thing at stake is the lot.
    Ce qu'il faut: the test is on the current lot: no
                   `code/<lot>/fiche-executable.md` → detailleur on its
                   block; and the agent's rule for lots that already carry
                   a sheet (agent comment above) is what makes that safe.
    Justification: robustness — the Réalisateur invents a sheet's worth
                   of decisions, which is the one thing the chain is built
                   to prevent.

---

    Fichier      : .claude/commands/8_code.md
    Cible        : "Where you stop and hand back" and "When the split
                   comes back"
    Aujourd'hui  : the rows cover: a `blocked_*.md` with empty Decision;
                   a filled Decision sending the lot back to the split
                   (→ /7_lots, then carry on); a filled Decision otherwise
                   (→ invoke the agent it names). The Détailleur has one
                   more exit: PART 2 finds a back-to-split decision and
                   stops with a message — "the block is waiting on the
                   split" — no file written. With /7_lots already run,
                   "a filled Decision is not a stop — invoke the agent it
                   names" sends the Détailleur back onto the same file,
                   which stops again.
    Le défaut    : command question 1 — an outcome the agent produces
                   with no row, and the nearest row loops with no ceiling.
    Ce qu'il faut: a row for it: a Détailleur that reports a block
                   waiting on the split is a redécoupage not applied —
                   run /7_lots if `code/redecoupage.md` is still there,
                   otherwise the blocking file was never closed: say which
                   file and stop. Ties to the agent's PART 2 comment and
                   to the question left to the group pass (who closes that
                   file).
    Justification: round trips — an invocation per loop turn, and the
                   Product Owner on her own when it stops.

---

    Fichier      : .claude/commands/8_code.md
    Cible        : the opening ("It never invokes the Contrôleur") against
                   "Where to resume" ("go straight to the Contrôleur, then
                   stop") and "Where you stop and hand back" ("The
                   Contrôleur has finished — the gap report is to be read")
    Aujourd'hui  : the command says both that it never invokes the
                   Contrôleur (its grouping lives in /9_controle, "run by
                   hand") and that it goes to him when every lot carries
                   a PASS, and stops when he has finished.
    Le défaut    : Plane 1 on the command — two passages asking for
                   different things; command question 1 — a "next" row
                   that names something the command says it cannot run.
    Ce qu'il faut: one of the two. The closing paragraph ("say that
                   /9_controle is what comes next — run by hand") is the
                   later and more specific; the other two lines follow it.
    Justification: robustness — an orchestrator reading the first rule
                   invokes an agent without the block grouping it needs
                   (the command's own reason for not doing it).

## From the verdict

Read after everything above: sections 4 to 7, and the Détailleur's
entry in section 2.

    Section 2 — "the role holds"; the walk avoids eight sheets twice;
    the two tests for disappearing assertions are the sharpest rule.
    Confirmed on the file, with one exactness: the walk avoids that
    cost only for stops the entries show. The grep-based stops (a
    declaration the code contradicts, a type nobody declares) are
    found at move 4, after earlier lots' sheets exist — comment 4
    above.

    Sweep rows 28, 31, 34, 44, 47, 48, 49, 50, 55 — the Détailleur as
    reader of cited entries, conventions (whole), `desc-bug.md`,
    `decoupage.md`, `sequence.md`, reports (by grep), the state
    document (two sections whole, rest grepped); producer of the sheet
    and of `architecte/` requests.
    All confirmed by the file. Row 50's "by grep" is confirmed and is
    where comment 11 applies (the grep's scope is the whole
    repository, not "this cycle").

    D12 — who reads the conventions for the Réalisateur is said two
    ways.
    Not found above as a comment (it needs `realisateur.md`). What the
    agent says, exactly: "You read the conventions whole; the
    Réalisateur codes against the sheet. A rule you do not name is a
    rule he will not apply, and the Relecteur will not know to look
    for." And one thing the verdict did not see, which makes D12
    heavier if the sheet is the carrier: move 8 names "Every 🔴 rule of
    TECHNICAL_CONVENTIONS.md bearing on what the lot touches" — the
    🔴 ones only. A convention without that mark is never carried into
    a sheet. If the Réalisateur codes from the sheet alone, every
    unmarked convention is dead for every lot. That is a comment in its
    own right, conditional on the answer to item 2 below:

        Fichier      : .claude/agents/detailleur.md
        Cible        : PART 3, move 8
        Aujourd'hui  : "Every 🔴 rule … bearing on what the lot touches"
        Le défaut    : Plane 2 Q1 — one case of a class that holds
                       several: the filter drops every rule not marked
                       🔴, and the file's own sentence says an unnamed
                       rule is unapplied.
        Ce qu'il faut: every rule bearing on what the lot touches, or
                       the mark is explicitly the carrier's threshold
                       and the conventions file is written knowing it.
        Justification: robustness, if the Réalisateur codes from the
                       sheet alone; nothing, if he reads the file whole.

    D16 — the asking lot is coded under the old rule, and the
    divergence is unrecorded.
    Confirmed on the behaviour: "You never block on this. Write the
    signature against the conventions as they stand, and carry on."
    Partially contradicted on the record: the sheet carries a
    `## Requests` field — "names the conventions requests this lot
    raised, or a dash — without it nobody knows one was written". So
    the sheet does say which lot raised which request; what the verdict
    names (the review verdict, the technical state) is not the
    Détailleur's to write.

    D17 / item 13 — rename or delete a settled blocking file: "renamed
    by one agent and deleted by five".
    Already found above (comment 1), with a precision the verdict could
    not have: this agent does both — "Renaming is what closes it —
    never delete it" and, eleven lines later, "Delete the file once
    applied". It is not on one side of the contradiction; it holds the
    contradiction.

    D22 — a stale entry in the technical state is a signature the next
    Détailleur writes against something that no longer exists.
    Partially contradicted. The agent does not sign from the state
    document: "every symbol is confirmed by grep before being written",
    on the code folders (move 4), and "not found, and none of the
    above → Stop". A symbol that vanished is caught. What the code grep
    does not catch is a symbol that still exists with a changed shape
    the stale entry misdescribes — the residue of D22 is that case, not
    the whole of it.

    D23 — a correction cycle's sheets live in `bugfix-NN/code/`.
    Confirmed: every path is relative to the working folder the command
    passes, and the command makes that folder `bugfix-NN/` when one
    exists. Nothing to correct in this agent; `controleur.md` settles
    it.

    D20 / item 18 — `/8_code` and the Contrôleur.
    Already found above (command comment 3): the command says it never
    invokes him and, twice, that it goes to him.

    A4 — "not the safety net of the upstream chain", said of the
    Détailleur.
    Confirmed, verbatim, twice (Role, and the never-do list).

    A6 / P10 — the sheet is self-sufficient, established by the walk and
    the rule to name every applicable convention; "every edge of every
    return".
    Confirmed for the edges: "A signature says what the return is
    worth at the edges — absence, emptiness, a bound, a unit, an order."
    For the conventions, see D12 above: "every applicable" is, in the
    file, "every 🔴".

    U10 — Arbitre waiting on the person; "Détailleur: block as is".
    Confirmed: "Still empty → stop, leaving the block as it stands." The
    twenty-minute poll is the Arbitre's; the Détailleur's own wait is
    "unbounded — do not poll, do not time out", consistent with it.

    A-4 — divergence → Détailleur, "sound".
    Found above with a different verdict (comment 14): the loop is
    bounded, but the mode is not runnable from the file — which moves
    run, whether PART 2 and the walk run, and where "the verdict" is on
    disk are all unstated.

    A-6 — redecoupage: sheets of uncoded lots deleted, Détailleur on the
    new block.
    Confirmed on the command side. What neither file says, and comment
    2 and command comment 2 turn on: who closes the
    `blocked_detailleur.md` whose decision sent the lot back, once
    `/7_lots` has run. Left to the group pass below.

    P4 — "Détailleur by grep".
    Confirmed: "The code, by grep only" — with the addition that the
    grep is scoped to folders the conventions name, and comment 9 on
    what happens when they name none.

    Item 2 — does the Réalisateur read the conventions whole or the
    sheet only? (`realisateur.md`, `detailleur.md`)
    The Détailleur's side is quoted under D12. The other side is not
    mine to read.

    Item 21 — does the Détailleur re-walk the block before rewriting
    sheets after a divergence?
    Not found as a yes or a no: the file does not say (comment 14). The
    verdict's concern on "no" — a rewritten sheet contradicting a
    sibling the divergence did not name — is real, and is met by reading
    the block's other uncoded sheets, not by re-walking the entries;
    comment 14 was refined to say so.

## What another agent would settle

    Who closes `code/<lot>/blocked_detailleur.md` when its decision sent
    the lot back to the split and `/7_lots` has since run?
    `cadreur.md`, `/7_lots`, `arbitre.md`.
    If the Cadreur or `/7_lots` renames or removes it with the old
    split: PART 2 row 4 fires only when the split is genuinely pending,
    and comment 2 reduces to naming that test. If nobody: the row fires
    on every run of that block forever, and the command's "invoke the
    agent it names" loops with no ceiling (command comment 2).

    Does the Réalisateur read `TECHNICAL_CONVENTIONS.md` whole, or only
    the `## Conventions` field of the sheet?
    `realisateur.md` (and `relecteur.md` for what it checks against).
    Sheet only: move 8's "🔴 rules only" filter drops every unmarked
    convention from every lot — robustness, and the D12 comment above
    applies in full. Whole file: move 8 is a redundancy paid in tokens,
    and the D12 comment does not apply.

    Does anything read the provenance label in `## Dependencies` —
    "pre-existing" versus "produced by lot-NN"?
    `realisateur.md`, `relecteur.md`.
    Nothing: move 5 can go entirely, and comment 12 becomes "remove";
    the code grep of move 4 already forbids redeclaring what exists.
    Something (the Relecteur checking that a lot did not redeclare a
    cycle symbol, say): move 5 stays, scoped as comment 11 says and
    restricted as comment 12 says.

    Are the lots of one block contiguous in the sequence?
    `verificateur.md`.
    Contiguous: comment 10 holds as written — at detailing time every
    lot before the block carries a PASS, and "an earlier lot of the
    sequence produces it, not found" is a defect. Interleaved: the row
    is right for the interleaved case and comment 10 narrows to blocks
    already fully PASSed.

    Is there a ceiling on a block's size — lots, or cited entries?
    `verificateur.md`, `cadreur.md`.
    Yes: the Détailleur's whole-block walk has a known upper bound. No:
    the walk plus the eight moves per lot plus the conventions whole is
    unbounded in one context, and the failure mode is degradation, not
    a stop — the known failure "more context than one agent holds"
    lands here, and the agent has no rule for it.

    Does a verdict that names a divergence carry PASS or FAIL, and does
    the coded lot's sheet stay as written after its code diverged?
    `relecteur.md`, `controleur.md`.
    PASS with the coded sheet untouched: "Leave the coded lots alone:
    their sheets describe what was built" is false for exactly that lot
    — its sheet describes what was specified, its code carries something
    else — and the Contrôleur, who reads sheets not code, is misled on
    it. FAIL: the divergence is corrected in the code, the sheets are
    true again, and the rewrite mode of comment 14 is rarely needed.

    Do the conventions' rules carry an identifier (`§NN`)?
    `architecte.md`, `/conventions`.
    Yes: move 8's "name the rule, never restate it" has something to
    name. No (a hand-written file, as `/socle` allows): the rule cannot
    be followed, and the sheet either restates or points at nothing.

    Does the Arbitre take several blocking files from one walk, and does
    one "back to the split" decision cover the sibling blocks of the
    same walk?
    `arbitre.md`.
    One file per invocation and independent decisions: comment 5's
    sequencing (file all, call each, apply none until all are back)
    holds. A redecoupage that supersedes the siblings: the agent may
    stop at the first "back to the split" and leave the other files
    unnumbered, which PART 2 would then treat as still standing.

    Does `## Symbols` in `code/decoupage.md` place every symbol a lot
    produces, or only the ones another lot consumes?
    `cadreur.md`.
    Every produced symbol: comment 12's restriction of move 5 to
    "symbols `## Symbols` does not place" leaves move 5 almost nothing
    to do. Consumed only: move 5 keeps a real residue (symbols produced
    and consumed inside one lot, or created unplanned).
