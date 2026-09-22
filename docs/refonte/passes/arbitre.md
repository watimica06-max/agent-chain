# Arbitre — phase 3 comments

Read: `.claude/agents/arbitre.md` in full; `.claude/commands/8_code.md` in
full (the command that runs the phase in which the arbitre is called and
that consumes what it writes); the passages of `7_lots.md` and
`audit_blocages.md` that name the arbitre. No command invokes the arbitre
directly — the Détailleur and the Réalisateur do, and their files were not
opened.

---

## The agent as a whole (plane 1)

**Role, from the file.** Fills the `## Decision` field of one blocking
file written by the Détailleur or the Réalisateur, from what the corpus
already says — conventions, technical document, code — calling the
Architecte once when a rule is missing, sending the lot back to the split
when the split is what blocks, and otherwise leaving the field empty for
the Product Owner.

**Moves, in order.**

| # | Move | Why it exists | What it feeds | What it overlaps |
|---|---|---|---|---|
| 0 | Which blocks are yours (Part 2) | Keeps a block no rule could settle out of the search | `## Decision` — "Not settled here" | Role ("What the user sees is not yours"), "What you write" ("When a block is not yours"), "What you never do" (Relecteur row): one rule, three places |
| 1 | Read the block and the settled ones beside it; look for the rule — conventions, own entry, neighbouring entry | The corpus answers most blocks | Decision, second part (what it rests on) | The "settled ones beside it" instruction is also in Role and in "What you read" |
| 2 | Same problem solved elsewhere, by grep | Consistency of the code where no rule names the case | Decision, second part | none |
| 3 | Settle or hand back — six rows | The outcome | `## Decision`, or one of the three files below | Row "A product question" restates "The one test" |
| 3c | Call the Architecte, once | A missing convention is written where conventions live | `architecte/arbitre-<lot>.md`, then Decision | none |
| 3d | Send the lot back to the split | The Cadreur re-cuts | `code/redecoupage.md`, read by `/7_lots` | none |
| 3e | Wait for the Product Owner | The person answers in the file | An empty field, read by the caller, then by `/8_code` | none |

**The set.** Every move feeds the Decision. None could go: without move
2 every unnamed case goes to the Architecte or the Product Owner; without
3c every rule-shaped block goes to the Product Owner. The order 1 → 2 → 3
is right. Two things fall between moves: where "the one test" is applied
(comment 2), and what happens when the Architecte returns neither a rule
nor a refusal (comment 11). One thing is done nowhere: telling anyone
what the search ruled out when the block is handed back (comment 14).

---

## Comments, in the order they are to be applied

### 1

    Fichier      : .claude/agents/arbitre.md
    Cible        : Role, second paragraph — the list of where an answer
                   already sits
    Aujourd'hui  : "a convention, a closure, an entry of the technical
                   document, or the same problem solved elsewhere in the
                   same code". "A closure" is defined nowhere in the file,
                   and move 1 says the grids "are not yours to open — what
                   they close reaches you through the rules the conventions
                   carry, and through the entries the technical document
                   holds".
    Le défaut    : Plane 2, question 4 — a term used and never defined,
                   naming a place the reading list does not give. Plane 3,
                   criterion 4.
    Ce qu'il faut: The Role names only the places the agent reads —
                   conventions, technical document, code. What a grid
                   closed is already inside those, and move 1 says so.
    Justification: Robustness — a reader looking for "closures" opens what
                   it is told not to (grid files, the product file) or
                   invents one. Tokens — the read that follows.

### 2

    Fichier      : .claude/agents/arbitre.md
    Cible        : Role, "What the user sees is not yours"; "The one test";
                   move 3, row "A product question"
    Aujourd'hui  : Role: "A block that turns on a behaviour — what a screen
                   shows, what a refusal returns, what a name means — goes
                   back to the Product Owner untouched" — a test on the
                   block's wording. "The one test": "Does your answer
                   change a behaviour the corpus describes?" — a test on
                   the answer, once found. Part 3 never says at which move
                   the test is applied; only row 5 of move 3 alludes to it.
    Le défaut    : Plane 1 — two passages of one agent asking for different
                   things; a constraint whose place in the order is not
                   stated. Plane 2, question 4 — read as a pre-filter, a
                   block the technical document answers in an entry (what
                   a refusal returns, say) is handed back unread; read at
                   move 3, it is settled from that entry.
    Ce qu'il faut: One test, applied at move 3 to the answer found. A
                   product-shaped block whose answer sits in an entry or a
                   convention is a rule found (row 1) — the answer changes
                   nothing the corpus describes. Only when moves 1 and 2
                   leave the block open does "turns on a behaviour" send it
                   to the Product Owner. The Role sentence must not read as
                   a filter applied before the search.
    Justification: Robustness and round trips — a block the corpus already
                   answers, handed back, costs a stop, a merge, a Product
                   Owner decision and a re-run of /8_code from the lot; the
                   reverse misreading — settling a behaviour — costs a
                   correction cycle.

### 3

    Fichier      : .claude/agents/arbitre.md
    Cible        : "Where you work" and "What you read", first two
                   paragraphs ("Each one's folder tells you what that block
                   bears on. In the split's own folder — the block bears on
                   the split as a whole, and no lot exists yet. In a lot's
                   folder — it bears on that lot."; "numbered"; "The order
                   — it may not be written yet when the block bears on the
                   split"; "The lot's sheet and report — only when the
                   block bears on a lot"); Part 2, table header "Written by"
    Aujourd'hui  : The file rests on three facts it never states — how a
                   blocking file is named, how its author is known, what
                   "the split's own folder" is. The commands hold them: a
                   standing block is `code/<lot>/blocked_<agent>.md`, a
                   settled one `blocked_<agent>-NN.md` (audit_blocages,
                   lines 26-28 and 146-150); 8_code (lines 215-217) places
                   the Détailleur's, the Réalisateur's and the Relecteur's
                   blocks in `code/<lot>/`, and only the Contrôleur's at
                   `code/`. For the two authors that are the arbitre's, the
                   split-level branch does not occur; nor does "the order
                   may not be written yet" — 8_code reads `code/sequence.md`
                   before invoking anything.
    Le défaut    : Plane 2, question 4 — a reader who has seen nothing else
                   cannot tell who wrote the block, nor which files are
                   "the settled ones". Plane 2, question 1 — a branch for a
                   case the command does not produce. Known list — a row
                   for a case that cannot occur.
    Ce qu'il faut: State the naming once — the author is the `<agent>` of
                   `blocked_<agent>.md`, the settled ones are the `-NN`
                   files in the same folder — and drop the split-level
                   branch with its two caveats (order unwritten, sheet only
                   for a lot), unless the Détailleur's file shows it writes
                   a block at `code/` level — see "What another agent would
                   settle".
    Justification: Robustness — a lot-folder block read as split-level
                   skips the sheet and the order the decision needs. Tokens
                   — a conditional branch loaded at every invocation for a
                   case that does not arrive.

### 4

    Fichier      : .claude/agents/arbitre.md
    Cible        : "What you read", first sentence and the "Blocking files
                   already settled" paragraph; the same instruction in Role
                   (lines 32-34) and in move 1
    Aujourd'hui  : "The blocking file the prompt names, and no other." Three
                   lines later: "Blocking files already settled sit beside
                   it, numbered. Read them". The settled-neighbours rule is
                   stated three times — Role, "What you read", move 1.
    Le défaut    : Known list — two passages of one agent asking for
                   different things. Plane 3, criteria 4 and 5.
    Ce qu'il faut: "No other" is about what the agent writes, and "What you
                   write" and "What you never do" already say it. The
                   reading list names the standing block and the settled
                   ones beside it, once; move 1 refers to it instead of
                   restating it.
    Justification: Robustness — the stricter reading skips the settled
                   neighbours and repeats a narrow decision. Tokens — three
                   statements of one rule.

### 5

    Fichier      : .claude/agents/arbitre.md
    Cible        : "What you read", "The technical document"
    Aujourd'hui  : Listed with no scope. Move 1 names what it uses: "the
                   technical document's own entry · a neighbouring entry of
                   the same nature" — and the split says which entries the
                   lot cites.
    Le défaut    : Plane 2, question 2 — a file read whole where a section
                   would do.
    Ce qu'il faut: The reading list names the entries the lot cites and the
                   section they sit in, not the document; the whole only
                   when the block bears on how entries relate across
                   sections (a dependency between lots).
    Justification: Tokens — the technical document is the largest file of
                   the working folder, loaded at every block on an
                   opus/high agent; known list — "more context than one
                   agent holds: it degrades instead of stopping".

### 6

    Fichier      : .claude/agents/arbitre.md
    Cible        : "What you read", "The lot's sheet and report"
    Aujourd'hui  : "report" — no file name, no path. `code/<lot>/` holds
                   `fiche-executable.md` (8_code line 201), `verdict.md`,
                   `reprise_realisateur.md` (8_code line 72); none is called
                   a report in the command.
    Le défaut    : Plane 2, question 4 — a file named without a path.
    Ce qu'il faut: Name the file. If it is `reprise_realisateur.md`, say it
                   exists only on a resumed lot and what the decision takes
                   from it — what is already written under the block's
                   symbols.
    Justification: Robustness — the agent guesses which file (an old
                   verdict, nothing) and may settle against code it does
                   not know is there.

### 7

    Fichier      : .claude/agents/arbitre.md
    Cible        : Move 1, paragraph "An earlier block naming the same
                   symbol, the same contract or the same module is the same
                   problem. Its decision was too narrow — settle wider this
                   time, and say what the earlier one missed."
    Aujourd'hui  : Stated as certain: a shared name makes it the same
                   problem, and the earlier decision was too narrow. Role
                   and "What you read" say "often means". "Say what the
                   earlier one missed" names no place to say it.
    Le défaut    : Plane 3, criterion 4 — two readings across two passages;
                   criterion 3 — as written the rule catches a second,
                   different question on the same symbol and orders it
                   widened. Plane 1 — conflicts with the decision's third
                   part, which exists to bound it.
    Ce qu'il faut: A shared name is a reason to read the earlier decision,
                   not an order to widen. Widen when the new block is the
                   question the earlier decision failed to cover, and say
                   so in the new decision's second part; a different
                   question on the same symbol gets its own bounded
                   decision. Where the code already applied the narrow
                   decision, the new one says whether that stands.
    Justification: Robustness — a decision widened by rule spreads to call
                   sites the block did not name, which is what the third
                   part is there to prevent.

### 8

    Fichier      : .claude/agents/arbitre.md
    Cible        : "When the split itself is wrong" — `## Ce qui ne l'est
                   pas` ("the lot in hand, whose code is dropped") and the
                   closing sentence ("The Réalisateur reads it, drops what
                   it wrote, and stops")
    Aujourd'hui  : Written for the Réalisateur only. The Détailleur is the
                   other caller (8_code lines 181-184: "the Détailleur
                   without writing a sheet"); it blocks before any lot of
                   the block is coded, and several lots may be left with
                   neither code nor sheet.
    Le défaut    : Plane 2, question 1 — one case of a class that holds two.
    Ce qu'il faut: The section names both callers. For a Détailleur block
                   nothing is dropped, `## Ce qui ne l'est pas` lists the
                   block's lots, none sheeted, and the Decision tells the
                   Détailleur to stop without a sheet.
    Justification: Robustness — the Cadreur reads "whose code is dropped"
                   for a lot never coded; small, but it is the one file the
                   re-split works from.

### 9

    Fichier      : .claude/agents/arbitre.md
    Cible        : "When a rule would settle it", `architecte/arbitre-<lot>.md`
    Aujourd'hui  : One name per lot. A lot can block more than once (the
                   settled ones are numbered), and each block may need a
                   rule; the second Write overwrites the first request and
                   its filled `## Verdict`.
    Le défaut    : Plane 2, questions 1 and 3 — a case the move does not
                   foresee. Known list — a record lost.
    Ce qu'il faut: The request name carries what the block carries — the
                   block file's own name, or author and number — so two
                   requests from one lot coexist; "ask once" is per block,
                   and the name then shows it.
    Justification: Robustness — the record that 8_code's move 6 and the
                   audits read is destroyed. Round trips — a later arbitre
                   on the same lot may re-read an overwritten Verdict as
                   its own.

### 10

    Fichier      : .claude/agents/arbitre.md
    Cible        : "When a rule would settle it", the `## Verdict` table,
                   row "Refused"
    Aujourd'hui  : Any refusal → wait for the Product Owner.
    Le défaut    : Plane 2, question 1 — two rows where the class holds at
                   least three: a rule written; a refusal because a rule or
                   an entry already covers it (the arbitre missed it); a
                   refusal because it turns on a behaviour. The first kind
                   of refusal is a rule found.
    Ce qu'il faut: A refusal that names an existing rule or entry is row 1
                   of move 3 — the arbitre settles from it. Only a refusal
                   saying the corpus cannot hold it goes to the Product
                   Owner. What a refusal can say is the Architecte's file's
                   business — see "What another agent would settle".
    Justification: Round trips — a block the conventions already answer is
                   otherwise stopped on, relayed, decided by the Product
                   Owner and re-run.

### 11

    Fichier      : .claude/agents/arbitre.md
    Cible        : Same table
    Aujourd'hui  : Two rows — written or changed, refused. 7_lots (line 112)
                   says the Architecte at invocation 3 can block in turn
                   (`blocked_architecte.md`); `## Verdict` is then still
                   empty when the arbitre re-reads its request.
    Le défaut    : Plane 2, question 3 — a situation where the move cannot
                   produce, unforeseen. The arbitre would read the empty
                   Verdict as a refusal (a Product Owner wait on its own
                   block, while the actual question sits in
                   `blocked_architecte.md`) or ask again, which is
                   forbidden.
    Ce qu'il faut: A third row — Verdict still empty: leave `## Decision`
                   empty, go out, and report that the Architecte blocked
                   and where. The orchestrator's stop condition must then
                   cover that file — see comment 17.
    Justification: Robustness — the Product Owner otherwise receives a
                   block whose question is in a file nobody relays.

### 12

    Fichier      : .claude/agents/arbitre.md
    Cible        : "When you wait for the Product Owner" — "poll the
                   blocking file" and the interval table
    Aujourd'hui  : Poll every 2 minutes, then every 5, up to 20 minutes. The
                   agent's tools are Read, Grep, Glob, Edit, Write, Agent:
                   none blocks for an interval, none gives the time. A poll
                   is a Read that returns at once; twenty minutes of them is
                   an unbounded loop of reads, or a wait the model reports
                   without having done it. And during the window nothing
                   tells the Product Owner a block is waiting — the report
                   that names it goes to the caller, after the wait.
    Le défaut    : Plane 2, question 2 — a move resting on a means nothing
                   gives it. Plane 2, question 1 — "every 2 minutes" is not
                   a test two readers can run without a clock.
    Ce qu'il faut: Either the agent is given a means to wait — a tool that
                   blocks for a set interval, and one that reads the clock
                   — and something names the file to the person before the
                   poll starts; or the wait goes, and the arbitre leaves the
                   field empty and goes out at once — the caller stops,
                   /8_code relays, the Product Owner answers in the file:
                   the end state of a wait that ran out. CLAUDE.md names
                   the arbitre as the one agent that polls the Product
                   Owner, so which is the Product Owner's decision; the
                   rule as written runs neither way.
    Justification: Tokens — a Read loop with no delay, on three stacked
                   agents. Round trips — unchanged either way today, since
                   nothing reaches the person during the window.

### 13

    Fichier      : .claude/agents/arbitre.md
    Cible        : Same section, and "What you never do" — "Leave
                   `## Decision` empty, except after waiting out the
                   Product Owner"
    Aujourd'hui  : The only exit written is "Nothing at 20 minutes: stop". A
                   poll that finds the field filled by the Product Owner
                   has no line — go out, complete it into the three-part
                   shape, add a third part? The "What you never do" entry
                   reads as if the arbitre must then write.
    Le défaut    : Plane 2, question 3 — an outcome unforeseen.
    Ce qu'il faut: A field filled by someone else is final — the arbitre
                   goes out without touching it and reports what it found
                   written. Moot if comment 12 removes the wait.
    Justification: Robustness — an arbitre that "completes" the Product
                   Owner's answer changes what she decided.

### 14

    Fichier      : .claude/agents/arbitre.md
    Cible        : "What you write" — "the `## Decision` field of the
                   blocking file you were given, and nothing else in it";
                   "Say it in your report instead"; "When you wait for the
                   Product Owner"
    Aujourd'hui  : On a Product Owner hand-back the field stays empty and
                   what the search ruled out — which conventions were read,
                   which entries are silent, what the code does not settle,
                   which behaviour the block turns on — goes into the
                   agent's report, read by the caller, not by the person.
                   8_code needs the field empty to stop (lines 215-222) and
                   relays the file. audit_blocages, finding 4 (lines
                   104-108), expects to quote "which behaviour it turned
                   on, or what the corpus does not say" from a handed-back
                   Decision — which the arbitre never writes for the case
                   that matters, and cannot, since a filled field is not a
                   stop for 8_code (line 239). The Product Owner decides
                   without knowing what was ruled out.
    Le défaut    : Plane 2, question 3 — the hand-back has no channel to the
                   person. Command — audit_blocages and the agent
                   contradict each other on what a hand-back carries.
    Ce qu'il faut: The reason for a hand-back lives in the blocking file, in
                   a section that is not `## Decision` — so 8_code's
                   empty-field test holds, the Product Owner reads what was
                   ruled out and which behaviour the block turns on, and
                   audit_blocages reads it there. "Nothing else in it" then
                   excepts that one section; `## What blocks`, `## Where`,
                   `## To resume` stay untouched. Whether the caller relays
                   the report is another agent's file — see below.
    Justification: Round trips — a Product Owner who does not see that rule
                   R and entry N were ruled out may answer "apply R"; and
                   audit_blocages' finding 4 is empty for every Product
                   Owner hand-back as things stand.

### 15

    Fichier      : .claude/agents/arbitre.md
    Cible        : Part 2, "Which blocks are yours" — the five paragraphs
                   after the table
    Aujourd'hui  : The table says who calls, and that anything else gets
                   "Not settled here". Then some 25 lines explain why each
                   other agent's block is not the arbitre's — Cadreur,
                   Vérificateur, Relecteur, Contrôleur, Architecte,
                   Cadreur-with-request — for blocks that 8_code (line 219)
                   and 7_lots (line 115) say never reach it. The Relecteur
                   case is also in "What you write" and "What you never do".
    Le défaut    : Plane 3, criterion 5 — commentary on why. Plane 2,
                   question 1 — enumeration where the table already states
                   the class.
    Ce qu'il faut: The table and the form of the answer, once; the author is
                   read from the file name (comment 3). What another agent's
                   block means is that agent's command's business.
    Justification: Tokens — loaded at every invocation for a route nothing
                   takes.

### 16

    Fichier      : .claude/commands/8_code.md
    Cible        : "When the split comes back", first paragraph; "Where you
                   stop and hand back", "Unless a Détailleur's or a
                   Réalisateur's `## Decision` sends the lot back to the
                   split"
    Aujourd'hui  : The orchestrator must recognise, from a filled
                   `## Decision`, that the lot goes back. Neither file fixes
                   what that decision contains: the arbitre says "write in
                   `## Decision` that the lot goes back to the split, and
                   name `code/redecoupage.md`" — free prose. 8_code's
                   reading list forbids the blocking file ("Nothing else"),
                   so it learns of the case from the caller's return.
    Le défaut    : Command — the row exists, the test that selects it does
                   not. Plane 2, question 1 — two readers cannot check it
                   the same way.
    Ce qu'il faut: One observable both files name — `code/redecoupage.md`
                   present with a section newer than the last `/7_lots`
                   run, or a fixed opening line of the Decision — and
                   8_code says where it reads it, given that its reading
                   list excludes the blocking file.
    Justification: Robustness — misread, the orchestrator stops and hands
                   the Product Owner a block that asks her nothing, or runs
                   /7_lots on a lot that was not sent back. Round trips —
                   one wasted /8_code or /7_lots either way.

### 17

    Fichier      : .claude/commands/8_code.md
    Cible        : "Where you stop and hand back"
    Aujourd'hui  : Stop rows: an empty-Decision `blocked_*.md` in one of
                   "two places" — `code/` for the Contrôleur,
                   `code/<lot>/` for the other three; three FAILs; N lots;
                   the Contrôleur finished. Move 6 invokes the Architecte
                   only between lots, but the arbitre invokes it mid-lot and
                   line 110 acknowledges that. 7_lots (line 112) has a row
                   for `blocked_architecte.md`; 8_code has none, and its two
                   places do not include where the Architecte writes.
    Le défaut    : Command — a case with no row.
    Ce qu'il faut: A row for an Architecte block, whether raised at move 6
                   or mid-lot through the arbitre, naming where the file
                   sits, that it is relayed with the caller's block, and
                   that the Product Owner fills it. Consistent with comment
                   11 on the agent side.
    Justification: Robustness — the orchestrator otherwise stops on the
                   caller's empty Decision and relays a block whose
                   question is in another file.

---

## What another agent would settle

    Do the Détailleur and the Réalisateur pass exactly what "Where you
    work" expects — the working folder and the blocking file's path — and
    in what form?
    detailleur.md, realisateur.md
    If yes, nothing to change. If either passes the feature folder, or a
    lot name instead of a path, the arbitre's first move fails silently
    on a bug-fix cycle.

    Does the Détailleur ever write a block at `code/` level — on the
    split as a whole, before any lot is designated?
    detailleur.md
    If never, comment 3 stands whole: the split-level branch, the
    "order may not be written" caveat and the "only when the block bears
    on a lot" condition all go. If it does, the branch stays and 8_code's
    "two places" (line 216) is the one that is wrong.

    Who renames `blocked_<agent>.md` to `blocked_<agent>-NN.md` once the
    field is filled?
    detailleur.md, realisateur.md
    If the caller does it, "numbered" in the arbitre holds and comment 3
    only needs to say so. If nobody does, the arbitre's "settled ones
    beside it" is a set that never forms.

    Does the caller relay the arbitre's report — what it looked for, how
    long it waited — to the orchestrator, and does the orchestrator relay
    it to the Product Owner?
    detailleur.md, realisateur.md (and 8_code's "What you relay", which
    names only the block)
    If relayed end to end, comment 14 loses its round-trips argument and
    keeps the audit's. If not, comment 14 stands whole.

    Do the callers read the decision's third part ("what it does not
    extend to") as a limit on what they may touch?
    detailleur.md, realisateur.md
    If yes, the third part is load-bearing and comment 7's bound matters.
    If they read only the first part, the third is paid for nothing and
    the bound must be inside the instruction itself.

    Does the Cadreur read `code/redecoupage.md` by the five French
    headings the arbitre writes, and does it read `## Ce qui est déjà
    codé` or the verdicts themselves?
    cadreur.md
    If it reads the headings, the arbitre's "English, like every file the
    agents read" is contradicted by its own template and one of the two
    has to give — the Cadreur's side decides which. If it reads the
    verdicts itself, the arbitre's `## Ce qui est déjà codé` and its
    conditional read of `code/<lot>/verdict.md` are work done twice.

    Does the Architecte at invocation 3 read `architecte/*.md` by glob or
    by a fixed name, and does it read the five headings the arbitre
    writes (`## What I need` … `## Verdict`)?
    architecte.md
    If by glob and by those headings, comment 9's rename is free. If by a
    fixed name or other headings, the request is never read and every
    arbitre call to the Architecte returns an empty Verdict — comment 11's
    case, every time.

    What shapes can the Architecte's `## Verdict` take on a refusal — and
    can it block in invocation 3, and where does its block sit?
    architecte.md
    If a refusal can point at an existing rule, comment 10 stands. If the
    Architecte can block at invocation 3 (7_lots says it can), comments
    11 and 17 stand and the file's location fixes 8_code's row.

    Does the Architecte, invoked mid-lot by the arbitre, also settle the
    requests the running Réalisateur left pending for move 6 — and does
    the Réalisateur then re-read the conventions before its lot ends?
    architecte.md, realisateur.md
    If yes to the first and no to the second, a rule written mid-lot is
    applied by nobody until the next lot, and 8_code's "one invocation,
    whatever the number of requests" is bypassed by the arbitre's call.
    If the Architecte reads only the request named to it, nothing to
    change.

    Do the Détailleur and the Réalisateur read `docs/TECHNICAL_CONVENTIONS.md`?
    detailleur.md, realisateur.md
    The arbitre justifies copying a new rule's text into the Decision
    with "the agent that blocked does not read the conventions". The
    instruction stands either way — the caller loaded the file before
    the rule existed — but the justification is either false or names
    a gap in the caller; the group pass decides which.
