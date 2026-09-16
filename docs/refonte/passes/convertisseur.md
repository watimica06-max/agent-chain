# convertisseur — phase 3 comments

Files read: `.claude/agents/convertisseur.md` (whole),
`.claude/commands/6_convertit.md` (whole — the only command that invokes
the agent; `2_structure.md`, `5_reclasse.md`, `cycle.md` and
`diagnostique.md` only name it in a relay row or a description), then
`docs/refonte/verdict.md` §2 line, §4–§7.

**Role, from the file:** turn a closed product file into a numbered
technical document whose sections are code layers, one nature per
invocation run in parallel, then one transversal invocation that writes
the preamble, resolves cross-section references, runs the cross-section
closures and writes the traceability — settling nothing, raising
everything.

**Moves, as written:**

| Inv. | Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|---|
| 1 | 1 Read blocks | the only input | moves 2–4 | — |
| 1 | 2 Write section | the product of the agent | command assembly → Cadreur | — |
| 1 | 3 Write notes (Trace, Preamble) | records block→entry and what goes to the preamble | command's script resolution, inv 2 moves 2, 3, 5 | Trace duplicates knowledge the entries themselves do not carry — needed |
| 1 | 4 Run by-nature closures | catches what the reformulation left open | questions, `<<ASSUMED` marks | its "No" branch is decided while writing move 2 (see c.1) |
| 1 | 5 Write questions | the only channel to the Product Owner | command merge | — |
| 2 | 1 Read document + notes | input | all | — |
| 2 | 2 Write preamble | frames what produces no lot | Cadreur, Architecte | — |
| 2 | 3 Resolve brackets | a lot must cite numbers | Cadreur | the "nothing carries it" branch is the case *Resources* in move 4 writes (see c.6) |
| 2 | 4 Cross-section closures | *Resources* writes §9 and orphans; *Declared links* checks every reference | document | with move 3 |
| 2 | 5 Write traceability | one line per block | unknown reader — the agent does not say who reads `tracabilite.md` | mechanical concat of Trace lines + move 4 |
| 2 | 6 Write questions | channel to the PO | command merge | — |

**Judgement on the set:** every move feeds something the command or a
later reader uses, except that no reader of `tracabilite.md` is named
anywhere in agent or command (left to the group pass). Coverage is
complete. Two ordering faults: the "No" branch of *What a question costs*
is reached during move 2, not move 4 (c.1); move 3 of invocation 2
questions what move 4 could write (c.6). The rest of the order holds.

---

## Comments, in application order

### c.1 — the "No" branch is met while writing, not after

    Fichier      : .claude/agents/convertisseur.md
    Cible        : INVOCATION 1, moves 2 and 4, and "What a question costs"
    Aujourd'hui  : move 2 writes the whole section; move 4 runs the closures
                   "once your section is written — not while writing" and
                   only then applies "What a question costs", whose "No"
                   branch says "write no section — delete yours if one is
                   there".
    Le défaut    : Plane 1 (order) and Plane 2 Q3. A rule the agent cannot
                   write without an answer stops it in move 2, where no
                   instruction exists for it. It will either write an
                   `<<ASSUMED` entry (turning a "No" into a "Yes") or skip
                   the entry silently, then reach move 4 and possibly
                   delete a section and leave notes whose `## Trace` names
                   entries that no longer exist. Nothing says what happens
                   to the notes in the "No" case.
    Ce qu'il faut: the decision "can I write this rule at all?" is taken
                   at the entry, in move 2; a "No" ends the section there
                   (no section, no notes, the question written); move 4
                   remains the sweep over a section that was written.
                   Whether the notes file exists after a "No" must be
                   stated, so the command's "when it wrote its section,
                   notes" check has one meaning.
    Justification: robustness — a "No" misfiled as an `<<ASSUMED` is a
                   guessed rule in the document; tokens — a section and a
                   notes file written to be deleted.

### c.2 — a rule that belongs to another layer: the instruction reads two ways and the question has no answerer

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "What raises a signal", second item
    Aujourd'hui  : "A rule of your block that belongs to another section's
                   layer — a question, never an entry written elsewhere.
                   The block was classed or split wrong, and that is
                   settled upstream."
    Le défaut    : Plane 2 Q4 and Q3. (a) It does not say whether the
                   agent writes that rule in its own section anyway or
                   leaves it out — one reading yields an entry in the
                   wrong layer (exactly what the Cadreur must not get),
                   the other a document missing a rule with no `<<ASSUMED`
                   to stop the Cadreur. (b) The question goes to the
                   Product Owner in the four-line shape, but a nature is
                   not a product matter; she cannot answer it, and a
                   reply that changes nothing in the block text leaves
                   the classeur's line as it was. Also a partial net over
                   the classeur (already-known list), kept only because
                   it is free while writing.
    Ce qu'il faut: one reading — the rule is left out of the section and
                   the section is marked provisional the same way an
                   assumption is (so the document cannot be cut without
                   it), and the question is phrased as something the
                   Product Owner can answer (what the rule does), not as
                   a layer choice. Which agent re-natures the block on
                   that answer is for the group pass (see last section).
    Justification: robustness — an entry in the wrong layer or a missing
                   rule reaches the split; round trips — a question the
                   Product Owner cannot answer costs a full turn.

### c.3 — a block named by title that the headings do not hold

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "A reference to another section", the line "A block the
                   product names by title — find its identifier in the
                   headings"
    Aujourd'hui  : the happy path only. Elsewhere the agent is told an
                   unresolved reference is upstream's business and it
                   must not re-sweep it.
    Le défaut    : Plane 2 Q3. When the title is not in the headings (a
                   renamed block, a title paraphrased in the block) the
                   agent can write neither `§n` nor `[B<n>: …]`; the two
                   rules it has (write brackets / do not re-sweep) leave
                   it to invent — a bare description in the prose, which
                   the command's grep for `[B` never sees and the Cadreur
                   reads as settled.
    Ce qu'il faut: the case is foreseen: the reference is written in a
                   form the grep catches (a bracket carrying the title
                   and no identifier), and it is a question — the "Yes"
                   kind, since the entry can still be written.
    Justification: robustness — an untraceable reference reaches the
                   split; tokens — nil.

### c.4 — a bracket reference or an `<<ASSUMED` mark must not span two lines

    Fichier      : .claude/agents/convertisseur.md (and the command's script)
    Cible        : "A reference to another section" and "Mark it inline,
                   greppable"; command section "The references with one
                   target"
    Aujourd'hui  : nothing on line breaks. The agent's own `<<ASSUMED`
                   example wraps over two lines, and every file of this
                   chain is wrapped at ~72 columns. The command resolves
                   `[B<n>: …]` "by script".
    Le défaut    : Plane 2 Q1 (does the move reach as far as it claims).
                   A line-oriented script does not see a closing `]` on
                   the next line: the reference is left unresolved, or
                   half-replaced. `grep '[B'` still finds the start, so
                   invocation 2 catches the leftovers by hand — but the
                   one-target references the command promised to resolve
                   are then resolved by an opus invocation instead.
    Ce qu'il faut: the agent keeps a bracket reference and an `<<ASSUMED
                   …>>` mark each on one line, however long; the command's
                   script, or its check after resolution, treats a
                   `[B<n>:` without `]` on the same line as a fault to
                   report, not to skip.
    Justification: robustness — a half-replaced reference in a document
                   the Cadreur cuts; tokens — the script does what it was
                   meant to do instead of invocation 2.

### c.5 — the two preamble markers are named, never shown

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "The technical document / Two parts, not one", the
                   preamble table ("The blocks declared valid everywhere",
                   "The references marked *existing*"), and move 3 of
                   invocation 1 (`## Preamble`)
    Aujourd'hui  : the agent must recognise a cross-cutting block and an
                   *existing* reference in its input, and file them under
                   `## Preamble`; what either looks like on the page is
                   not given.
    Le défaut    : Plane 2 Q4 — a term used and never defined, for a
                   reader that has seen no product file. It will guess
                   from wording ("always", "every", "already exists"),
                   and a block that is cross-cutting by the Rédacteur's
                   convention but not by its phrasing becomes numbered
                   entries — or the reverse, a real rule goes to the
                   preamble and produces no lot.
    Ce qu'il faut: the file states the form it looks for (the exact
                   marker or line the product file carries for each of
                   the two), or says that the form is whatever the
                   product file's own legend declares and where that
                   legend sits. The form itself belongs to the Rédacteur
                   (see last section).
    Justification: robustness — a rule misfiled between preamble and
                   section is a lot missing or a constraint cut into a
                   lot.

### c.6 — invocation 2 questions at move 3 what move 4 writes

    Fichier      : .claude/agents/convertisseur.md
    Cible        : INVOCATION 2, order of moves 3 and 4
    Aujourd'hui  : move 3: "None of them carries it, or the line is a
                   dash — a question; leave the brackets." Move 4:
                   "*Resources* is the one that writes: an entry nothing
                   carries, whose content the product already settled,
                   goes at the end of its section, next number […] and
                   its number goes on the `Consumes:` line of every entry
                   that needs it."
    Le défaut    : Plane 1 — two moves splitting one job, in the wrong
                   order. A bracket whose target block gave no entry
                   carrying the expectation is, when the product settled
                   the content, exactly what *Resources* writes one move
                   later. Written in this order the agent asks a question
                   at move 3, then writes the entry at move 4, and either
                   leaves a question whose answer it wrote itself or
                   goes back to retract it — nothing tells it to.
    Ce qu'il faut: the brackets move 3 cannot resolve are the input of
                   move 4's *Resources*; only what *Resources* cannot
                   write (the product did not settle it) becomes a
                   question, and the bracket is then replaced by the new
                   number. The final `grep '[B'` stays last.
    Justification: round trips — a question the agent could answer costs
                   the Product Owner a turn and a full re-run; robustness
                   — a bracket left next to an entry that now exists reads
                   as unsettled and blocks the split for nothing.

### c.7 — a reference to a cross-cutting block becomes a question nobody can answer

    Fichier      : .claude/agents/convertisseur.md
    Cible        : INVOCATION 2, move 3, the branch "the line is a dash"
    Aujourd'hui  : dash → question. A nature invocation that references a
                   block outside its input (`[B20: every duration in
                   seconds]`) cannot know that block is cross-cutting;
                   its owner filed it under `## Preamble` with a dash in
                   `## Trace`. A block with no `## Trace` line at all is
                   not foreseen either (the command foresees it: "Several,
                   a dash, or no line → leave them").
    Le défaut    : Plane 2 Q3. The question that results ("B20 gives no
                   entry carrying …") is not a product question; the
                   Product Owner's answer changes nothing, and the bracket
                   comes back next run.
    Ce qu'il faut: before asking, move 3 reads the block's `## Preamble`
                   line: a cross-cutting rule or an *existing* reference
                   is resolved to the preamble (in whatever form the
                   `Consumes:` reader accepts — theirs to fix, not a
                   number), and only a block with neither a Trace entry
                   nor a Preamble line is a fault to raise. "No line at
                   all" is named, and treated as an invocation 1 omission
                   (a fault in the notes, not a product question).
    Justification: round trips — one unanswerable question per
                   cross-cutting rule referenced, every run; robustness —
                   a constraint the entry depends on is tied to it
                   instead of being dropped.

### c.8 — the preamble has no shape

    Fichier      : .claude/agents/convertisseur.md
    Cible        : INVOCATION 2, move 2, and "Two parts, not one"
    Aujourd'hui  : "Write the preamble, at the head of the document,
                   before §1" — three parts are named (intent/vocabulary/
                   out of scope; cross-cutting rules; dependencies), no
                   heading, no marker distinguishes it from a section.
                   The reader is told only that "content that produces no
                   lot is not a section".
    Le défaut    : Plane 2 Q4 — a placeholder with no rule for what fills
                   it. The Cadreur must tell preamble from sections
                   (sections are code layers, the preamble is never cut),
                   and the Architecte must find the dependencies in it. A
                   free-form head written differently at each run gives
                   both a different thing to parse every time.
    Ce qu'il faut: a fixed shape — one heading per part, in a fixed
                   order, distinguishable from `## §n` at a glance — and
                   each part written empty when nothing fills it, for the
                   same reason an empty section is written. What the
                   Cadreur expects is for the group pass to confirm.
    Justification: robustness — a preamble part read as a section is cut
                   into a lot; round trips — the Cadreur asking what a
                   free-form head means.

### c.9 — "Say which of the two you are in" has no destination

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "What a question costs", last line
    Aujourd'hui  : "Both cases write the question the same way. Say which
                   of the two you are in." — after "One entry per
                   question, four lines, no exception."
    Le défaut    : Plane 3 criterion 4. Two readings: say it in the
                   question entry (a fifth line, copied "as written" into
                   the Product Owner's file and handed to the Rédacteur,
                   who integrates four-line entries), or say it in the
                   report (which already reports section written / not,
                   and the `<<ASSUMED` count). The command tells the two
                   cases apart by file presence, so the sentence guards
                   nothing the entry needs.
    Ce qu'il faut: one destination, and it is the report; the entry
                   stays four lines.
    Justification: robustness — a five-line entry breaks the shape the
                   downstream reader depends on.

### c.10 — the grid is loaded whole, eight times, for one group of closures

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "What raises a signal" ("Load the grid; it is not in
                   this file") and PART 2, Reads column
    Aujourd'hui  : the whole grid is read by every nature invocation,
                   which is then told to use "the closures of your
                   invocation's group, and those alone".
    Le défaut    : Plane 2 Q2 — a file read whole where a section would
                   do, paid eight times per run. (The grid's layout is
                   not something this pass may check; if it is not split
                   by group, the comment is moot and the fault is the
                   grid's.)
    Ce qu'il faut: the invocation reads its group's part of the grid
                   only, located by its heading; invocation 2 reads the
                   cross-section part.
    Justification: tokens — eight parallel opus contexts each carrying
                   closures they are forbidden to run.

### c.11 — two body prohibitions have no mirror under "What you never do"

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "What you never do"
    Aujourd'hui  : the list mirrors grouping, settling, product-file
                   writes, code, `docs/process/`; it does not mirror
                   "never write a number outside your own section"
                   (invocation 1) nor "you never rewrite a rule another
                   invocation wrote" (invocation 2).
    Le défaut    : already-known list — a rule in the body with no
                   matching entry. Both are the two temptations most
                   specific to this agent: guessing a neighbour's number
                   while eight sections are written at once, and
                   "improving" a rule at the transversal pass, which
                   re-decides blind what a nature invocation decided with
                   its blocks in front of it.
    Ce qu'il faut: both appear in the list.
    Justification: robustness — a wrong number or a silently changed
                   rule reaches the Cadreur with nothing to stop on.

### c.12 — a blocked invocation: what it leaves on disk is not said

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "When you cannot produce", against INVOCATION 1 move 5
                   and INVOCATION 2 move 6 ("Write your questions file —
                   always")
    Aujourd'hui  : the blocking file's shape and when to write it; nothing
                   on whether the moves continue, whether the (empty)
                   questions file and the notes are still written.
    Le défaut    : Plane 2 Q3. The command decides what happened by file
                   presence: missing questions file → "stop, say which
                   file"; section missing → "a nature asked something it
                   cannot write a rule without". A blocked invocation
                   produces one of those two misreadings unless the two
                   files agree on what a block leaves behind.
    Ce qu'il faut: one rule — a blocking file ends the invocation, and
                   nothing else of that invocation is written (or the
                   reverse; but one of the two, stated in both files —
                   see c.14 for the command side).
    Justification: round trips — a block misread as a missing file or as
                   an unanswered question sends the Product Owner down the
                   wrong row of "What to run next".

### c.13 — the path table mixes two bases

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "Where you work", the table
    Aujourd'hui  : `convertisseur/<nature>-input.md`, `desc-produit.md`,
                   `spec-technique.md` … are relative to the feature
                   folder; `docs/process/GRILLE_FERMETURE_TECHNIQUE.md` is
                   relative to the repository root; nothing says which
                   base applies to which row. The prompt gives only
                   "Feature folder: docs/features/<name>/."
    Le défaut    : Plane 2 Q4 — a file named without a path. A wrong
                   base means a "file you were told to read that is not
                   there", i.e. a blocking file and a lost opus
                   invocation, or a search where the agent should stop.
    Ce qu'il faut: the table says its base (the feature folder) and the
                   one row that departs from it says so.
    Justification: robustness — one avoidable blocking file; tokens — one
                   avoidable re-run.

### c.14 — the command's early stops skip the merge, and misread a blocked nature

    Fichier      : .claude/commands/6_convertit.md
    Cible        : "The nature invocations" (last paragraph), "Invocation
                   2" (last paragraph), "The assembly" (row "No"), against
                   "Once it has run"
    Aujourd'hui  : "A missing one stops the command — say which nature
                   and which file, and go no further." Blocking files are
                   looked at only *before* invoking (their `## Decision`)
                   and filed *after* the run. The "No" row of the assembly
                   diagnoses a missing section as "it asked something it
                   cannot write a rule without". Merge and push are in
                   "Once it has run", after all of that.
    Le défaut    : command questions — an outcome the agent can produce
                   (a `blocked_<nature>.md` written this run) has no
                   handling between invocation and relay; "go no further"
                   leaves the worktree unmerged, so the blocking file, the
                   other natures' sections and the questions never reach
                   the main checkout — the Product Owner sees nothing, the
                   worktree "never self-cleans", and the next run's `git
                   mv … closed/` files as "merged already" questions that
                   never were.
    Ce qu'il faut: right after the invocations return, the command greps
                   for a new unnumbered `blocked_*.md` before checking
                   notes and questions; a blocked nature is reported as
                   blocked, not as missing files nor as a "No"; every stop
                   after the worktree was entered still runs "The
                   questions" and "Once it has run" (merge, push, remove),
                   and the relay row "An invocation wrote a blocking file"
                   then matches a state the Product Owner can see.
    Justification: robustness — work of seven natures kept instead of
                   redone; round trips — a blocking file the Product Owner
                   never sees is a turn lost, then a stop on the next run.

### c.15 — rerunning a nature whose input did not change, and the loop that never closes

    Fichier      : .claude/commands/6_convertit.md
    Cible        : "Which natures run", rows 3 and 4 (section absent;
                   section holds `<<ASSUMED`), and "No nature runs"
    Aujourd'hui  : both rows run the nature regardless of whether its
                   `<nature>-input.md` changed. The agent's mark "is
                   lifted by writing the section again, once the answer
                   is in the product file", and it can only see the answer
                   through its blocks.
    Le défaut    : already-known list — an invocation that produces
                   nothing, and a loop with no ceiling. If the part is
                   byte-identical to the last input, the invocation reads
                   the same blocks, meets the same gap, writes the same
                   `<<ASSUMED` (or the same "No") and asks the same
                   question: one opus invocation per nature per run, for
                   a known result. Nothing counts the rounds; an answer
                   the Rédacteur integrates without changing the block's
                   text (a confirmation) keeps this going forever. The
                   only legitimate reason to rerun on an unchanged input
                   is a filled `## Decision` (row 5) or a previous run
                   that died before writing (which the missing-file stop
                   already reported).
    Ce qu'il faut: an unchanged input with an `<<ASSUMED` mark or no
                   section is a nature *waiting for an answer*, not one
                   that runs; the command says so in the relay (a fourth
                   state next to ran / kept), and the "No nature runs →
                   document stands" test is not met while a nature waits.
                   Whether a confirmation always changes the block text is
                   for the Rédacteur's pass (last section).
    Justification: tokens — an opus invocation per waiting nature per
                   run; round trips — the loop gains a visible end
                   condition instead of re-asking.

### c.16 — the "document stands" and "go to /7_lots" rows ignore a leftover `[B`

    Fichier      : .claude/commands/6_convertit.md
    Cible        : "What you relay", third row; "Invocation 2", the
                   post-check
    Aujourd'hui  : after invocation 2 the command checks two files exist,
                   relays the `<<ASSUMED` count, and sends the Product
                   Owner to `/conventions` then `/7_lots` on an empty
                   questions file. The agent's own text says a `[B` left
                   after its grep "is either a question you wrote, or a
                   reference you missed" — the second case comes with an
                   empty questions file.
    Le défaut    : command question — a row for a case that is not what
                   it says. A missed reference (agent fault, no question)
                   goes to the split unresolved; whether the Cadreur stops
                   on `[B` as it does on `<<ASSUMED` is not something this
                   pass can check.
    Ce qu'il faut: the post-check of invocation 2 greps `[B` in
                   `spec-technique.md`; an empty questions file with a
                   `[B` left is a fault of the run, reported as such (and
                   invocation 2 may be run once more, with a ceiling of
                   one), never a "document stands".
    Justification: robustness — an unresolved reference in the document
                   the split is cut from.

### c.17 — a run that writes both a blocking file and questions: two rows apply, the first destroys the second

    Fichier      : .claude/commands/6_convertit.md
    Cible        : "What you relay", rows 1 and 2; "Git, before invoking"
    Aujourd'hui  : row 1: fill `## Decision`, run `/6_convertit` again.
                   Row 2: answer the questions, `/1_lexique`. Before
                   invoking, the command moves every root
                   `questions-*.md` into `questions/<agent>/` unread.
    Le défaut    : command question — an outcome with two rows. Seven
                   natures asked questions, one blocked; following row 1
                   reruns the command, which files the unanswered
                   questions as if integrated. The `<<ASSUMED`-backed ones
                   are asked again by the rerun (see c.15); a signal
                   question without a mark (layer, surviving
                   clarification) is lost.
    Ce qu'il faut: one row for the combined case, and it says the order:
                   answer the questions first (they go through the
                   Rédacteur), fill the decision, then rerun; or the
                   "move to `questions/<agent>/`" is conditioned on the
                   file being integrated rather than on it merely being
                   at the root — whichever the chain's standing rule for
                   root questions files allows.
    Justification: round trips — questions asked once and lost are asked
                   again a turn later, or never.

### c.18 — nothing checks that the traceability is complete

    Fichier      : .claude/commands/6_convertit.md
    Cible        : "Invocation 2", the post-check ("check `tracabilite.md`
                   and `convertisseur/questions-transversal.md` exist")
    Aujourd'hui  : existence only. The agent's move 5 is a transcription
                   (every heading identifier, in product order, its Trace
                   entries plus move-4 additions) that an opus invocation
                   performs after reading the whole document — the kind
                   of move that drops a line without noticing, and whose
                   rule "every block appears" is the one thing a grep can
                   verify.
    Le défaut    : Plane 2 Q1 on the agent's move, checked on the command
                   side — the move claims completeness and nothing
                   measures it, while the command already greps the
                   headings for other purposes.
    Ce qu'il faut: the post-check compares the block identifiers of the
                   product file's headings with the first column of
                   `tracabilite.md`; a missing or extra identifier is a
                   fault of the run, reported like a missing file.
    Justification: robustness — the one file that says which block
                   produced nothing is trusted blind; tokens — nil (a
                   grep).

### c.19 — history parentheticals in the command

    Fichier      : .claude/commands/6_convertit.md
    Cible        : "Git, before invoking" — "(Seen once: 186 lines in the
                   worktree, 195 in the main checkout.)", "(Seen once: a
                   whole invocation lost that way.)", "(Measured on three
                   phases: …)"; "Which natures run" — the paragraph "Why
                   the part and not the markers"
    Aujourd'hui  : the rules carry the incident that produced them.
    Le défaut    : Plane 3 criterion 5 — commentary on why a rule came to
                   be. The executor needs the rule; the incident belongs
                   to the Product Owner's process notes.
    Ce qu'il faut: the rules stand alone. (The "part not markers"
                   paragraph carries one fact the executor does need —
                   markers are stripped each turn, so they cannot be the
                   comparison — and that one line stays.)
    Justification: tokens — small, at every run of the command.

### c.20 — a question that is technical has the same destination as a product one

*(added after the verdict check — its item 15 asked what the agent
does; the agent's text confirms the gap, so it is a comment, not only
a verdict entry)*

    Fichier      : .claude/agents/convertisseur.md
    Cible        : "Your questions" (one file, one shape, one reader) and
                   INVOCATION 2, move 4 ("A rule you find wrong is a
                   question")
    Aujourd'hui  : every signal the agent raises goes to the Product
                   Owner in the four-line shape, and "The Rédacteur
                   integrates by block". Nothing in the file names a
                   question that is not a product question: two sections
                   naming one entity two ways, a layer choice (c.2), a
                   reference to a cross-cutting rule (c.7), a
                   cross-section reference the transversal cannot choose
                   between two entries.
    Le défaut    : Plane 2 Q3 — a situation where the move cannot
                   produce a useful question, unforeseen. The Product
                   Owner cannot arbitrate a technical name; the Rédacteur
                   has no product sentence to write for it; the block is
                   unchanged; the question comes back next run (c.15).
    Ce qu'il faut: the file distinguishes the two kinds. A product hole
                   takes the questions file. A technical divergence
                   between sections is either settled by invocation 2
                   inside what it is already allowed to touch (a name is
                   a reference, not a rule — "Everything else you touch
                   in a section is a reference"), or goes to whichever
                   agent owns technical choices, by a file that agent
                   reads — which one, and whether it accepts requests
                   from the upstream, is for the group pass.
    Justification: round trips — a full upstream turn (answer,
                   `/1_lexique`, `/2_structure`, …, `/6_convertit`) for
                   a choice no one on that route can make; robustness —
                   the alternative is the Cadreur grepping two names for
                   one thing.

---

## From the verdict

*(read after everything above; §2 line, §4–§7)*

**§2 — "the role holds"; nothing to correct.**
Already found: nothing to find. The role sentence at the top of this
file matches the verdict's four things (names, layers, `Consumes`,
executable phrasing).

**§4 sweep #26 / D8 — a `[B12: …]` reference to a block that yielded
no entry has no stated outcome.**
Contradicted by the agent and the command, then found in another form.
The command: "One entry on it → write that number in place of the
brackets. Several, a dash, or no line → leave them — invocation 2
settles those." The agent, invocation 2 move 3: "None of them carries
it, or the line is a dash — 🔴 a question; leave the brackets." Zero
*is* covered — as a question to the Product Owner. The defect is not
that the case is unstated but that its outcome is a question nobody on
that route can answer (c.7), and that the case the verdict guesses at
("a block whose rules all went into the preamble") is exactly the one
the notes' `## Preamble` line would resolve without asking.

**§4 sweep #28 / D9 — the preamble's dependencies travel by no named
artefact; "the product file's text outside blocks is the only
candidate".**
Contradicted by the agent. The preamble table: "Dependencies | The
references marked *existing*"; and: "⚠️ A reference marked *existing*
is neither — it goes to your notes, for the preamble." The artefact is
the *existing* mark on a reference **inside a block**, collected by
each nature invocation into `## Preamble` of its notes — not the text
outside blocks. Since blocks are what the grid probes, D9's "neither
classified nor questioned by the grid" does not follow from the agent's
text. What remains open is whether the Rédacteur writes such a mark and
in what form (c.5, and the last section). The verdict's "only he has
the global in front of him" is quoted correctly ("Dependencies come from
the Rédacteur, not from you").

**§4 sweep #29 — `tracabilite.md` read by the Architecte inv. 1 and
`/9_controle`.**
Not found above; the agent names no reader for it ("the traceability
file | `tracabilite.md`", nothing else), which is why the move-set table
marks its reader unknown. If the verdict's readers hold, move 5 is
paid for something; carried to the last section.

**§4 D2 / A3 / §7 item 6 — block identifiers assumed stable.**
Not found as a comment: the agent relies on it everywhere (`[B12: …]`,
`<<ASSUMED B40`, `Block: B7`, `## Trace`, `tracabilite.md`, "find its
identifier in the headings") and states nothing about it — correctly,
since it is not the agent that guarantees it. Nothing to change in
this file; the Rédacteur's pass settles it.

**§4 D10 / §5 U6 / §7 item 15 — technical questions travel the product
route; does the transversale settle a naming divergence or ask?**
Found in parts (c.2, c.7) and, on the verdict's prompt, as c.20. What
the agent says: it asks — "🔴 You never settle anything"; "A rule you
find wrong is a question"; one questions file, one shape, "The
Rédacteur integrates by block". No move of either invocation names
naming agreement across sections at all; if a closure of the grid
covers it, the agent's only treatment of a failure is *What a question
costs*, i.e. the Product Owner. The verdict's conclusion for the "asks"
branch is the one the file supports.

**§4 A1 — that every answer lands as text in the product file.**
Already found, as the mechanism behind c.15. The quotation: "🔴 A
question whose answer is recorded is never asked again. The answer is
in the product file by the time you run again." The agent cannot check
it (it never opens a questions file), so the rule is a premise, not an
instruction; the loop it opens is bounded only if the Rédacteur always
changes the block (last section).

**§4 A4 — that the grid is complete.**
Not a defect of this agent: "🔴 You are not the safety net of the
upstream chain … You translate what they closed." By design; nothing
to add.

**§5 U6 — stop: questions file empty and no `<<ASSUMED`; bound: none.**
Already found: c.15 gives the loop the detector it lacks (an unchanged
input with a mark is waiting, not running), and c.16 adds the `[B`
condition the stop test misses.

**§6 P8 — the command is the state machine, and it is an LLM session.**
Already found in instances: c.14 (a stop that skips the merge), c.15
(a rerun decided by a rule that ignores the input), c.16–c.18 (checks
that are greps and are not run). Nothing to add on the premise itself.

**§6 P13 — the whole product fits one context; "the Convertisseur alone
is split by nature".**
Not found above, and worth having: the split protects invocation 1
only. Invocation 2 reads "the technical document in full, and every
notes file", plus the product file's text outside blocks and the
grid — the whole output of eight sections in one context, with no
size guard in agent or command. What the agent says: nothing about
size; the command relays counts of questions and marks, not of lines.
The failure mode P13 names (silent truncation, not a block) applies
to the traceability (c.18 is the only check) and to the `[B` sweep
(c.16). I add no separate comment: the threshold is unknown to this
pass, and the two checks above are what turns a truncation into a
reported fault.

**§6 P2 / P3 — nature = section = layer; the document frozen once
cut.**
Already in the agent as design: "Sections that are code layers";
"The command refuses to run once `code/decoupage.md` is there". No
comment; the group pass judges the premise.

**§7 item 10 — where do the preamble's dependencies live?**
Answered above under D9: in the blocks, as *existing* marks, per the
agent. Whether the text outside blocks is probed is for the Sondeur's
file.

---

## What another agent would settle

    Which agent re-natures a block when the Convertisseur says one of
    its rules belongs to another layer (c.2)?
    classeur.md (and redacteur.md: does an answer that changes no
    sentence still mark the block?)
    If the classeur re-checks only blocks the Rédacteur changed, the
    layer question must force a block change or it is lost; if the
    classeur can be sent a block by name, the question should go
    there, not to the Product Owner.

    What do a cross-cutting block and an *existing* reference look like
    on the page (c.5, D9)?
    redacteur.md
    A fixed marker: c.5 is one line naming it. No marker: the
    convertisseur decides cross-cutting by phrasing, and the preamble
    is unreliable; the fix is then the Rédacteur's, not this file's.

    Does an answer that confirms a block as it stands change the
    block's text or mark it (c.15, A1, verdict item 7)?
    redacteur.md
    Always changes or marks it: the byte compare of `/6_convertit`
    sees it and the `<<ASSUMED` loop closes. Not always: the mark
    never lifts on an unchanged input, and c.15's "waiting" state
    must have a second exit (a decision file, or the Product Owner
    told the block must be edited).

    What shape does the Cadreur expect for the preamble, and does it
    stop on a leftover `[B` as it stops on `<<ASSUMED` (c.8, c.16)?
    cadreur.md
    Stops on `[B`: c.16 is a relay accuracy fix. Does not: an
    unresolved reference is cut into a lot, and c.16 is a robustness
    fix. A preamble shape the Cadreur names: c.8 adopts it. None: c.8
    proposes one and cadreur.md gains the matching line.

    Who reads `tracabilite.md`, and for what (move-set table, verdict
    sweep #29)?
    architecte.md, the /9_controle command (controleur.md)
    A reader that uses the block→entry map: move 5 stays and c.18's
    completeness check is worth it. No reader, or a reader that
    rebuilds it from the notes: move 5 goes, the notes suffice.

    Where does a technical question from the upstream go (c.20, D10)?
    architecte.md (its *précision* rule, per the verdict) and arbitre.md
    An agent that accepts a technical request from before the split:
    c.20 names its file. None: invocation 2 must settle naming
    divergences itself, within its "reference, not rule" allowance,
    and the agent file needs the line that says so.

    Is `vocabulary` for the preamble in `desc-produit.md`'s text
    outside blocks, or in the lexicon the Lexicographe writes
    (invocation 2, move 2)?
    lexicographe.md, redacteur.md
    In the product file: move 2 reads what it is told. In a lexicon
    file: the agent is told to read a file it does not name, and the
    preamble's vocabulary part is written from nothing.

    Is the technical closure grid sectioned by group (by nature /
    across sections) so that c.10 can be applied?
    the grid file itself (`docs/process/GRILLE_FERMETURE_TECHNIQUE.md`)
    — not an agent; noted so the group pass knows c.10 is conditional
    Sectioned: c.10 stands. Not: the fault is the grid's layout, and
    c.10 is dropped.

---

## Outside this pass, seen while grepping the commands

`cycle.md` names the convertisseur in rows 7, 12 and 14 of its routing
table and sends the Product Owner to `/3_reclasse`, `/4_convertit`,
`/7_decoupe`, `/1_structure`, `/2_grille` — names that do not exist
under `.claude/commands/` (the files are `5_reclasse`, `6_convertit`,
`7_lots`, `2_structure`, `4_grille`). Not read in full (it does not
invoke the agent); left for whoever holds that command.
