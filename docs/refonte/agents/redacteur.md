# Rédacteur — examination

Read: `.claude/agents/redacteur.md` (whole), `.claude/commands/2_structure.md`
(whole, the command that invokes it), `.claude/commands/cycle.md` (whole, it
routes to and from this agent). Then `docs/refonte/verdict.md`, last.

---

## Plane 1 — the agent as a whole

**Role, from the file:** the Rédacteur turns the Product Owner's free-form
idea file into the structured product file (invocation 1), and integrates
the answers of one questions file into that product file (invocation 2);
at every invocation it writes a questions file of its own, and it decides
no product matter.

**Moves, in order.**

Invocation 1 — Structuring

| # | Move | Why it exists | What it feeds | What it overlaps |
|---|---|---|---|---|
| 1.1 | Decompose each passage into subjects — one trigger, one output | Without it a block carries several triggers and the decoupeur, the classeur and the convertisseur all work on a compound | The block list, read by every downstream agent | 1.3's "a different output separates too, on a shared trigger" restates its criterion at filing time |
| 1.2 | Grep the global's index for a title covering the subject; load a near section and put the same test to it; reuse verbatim or create | Without it a subject the global already carries gets a second title and the merge cannot match them | Section and block titles — the fusionneur, and everything that greps `^###` | "Creating a section or a domain — grep before creating" is the same check one level up |
| 1.3 | File one block per subject, empty `Nature:`, numbered in writing order, `NEW` | It is the product file | The classeur (the empty line), the decoupeur and the sondeurs (the markers), every questions file (the numbers) | — |
| 1.4 | Flag what cannot be transcribed in one reading — in the block, and as a question | Without it a block carries an unconfirmed reading the grid would close | The questions file, answered by the Product Owner, integrated at invocation 2 | The contradiction rule ("the latest version applies") handles a neighbouring case by another route — see comment 3 |
| 1.5 | Stop on two unrelated subjects — blocking file | Two features in one file, nothing downstream separates them | `blocked_redacteur.md` — the Product Owner, the command | — |
| 1.6 | Write the questions file, even empty | The command's next-step table reads it | `2_structure.md`, `/1_lexique` | — |

Invocation 2 — Integrating

| # | Move | Why it exists | What it feeds | What it overlaps |
|---|---|---|---|---|
| 2.0 | Load: strip the markers, grep the titles, ranged read of the blocks named | Keeps the read to a handful of blocks; resets the markers so only this turn's stand | The product file's markers — the sondeurs and the decoupeur | — (but see comment 1) |
| 2.a | Route each answer: merge, replace, own block, split | It is the integration | The product file | 2.d asks the same two questions of every answer a second time, against the title list |
| 2.b | Split when the answer says so; renumber; update citations; strip the flag | A block that holds several stays split by the one who read the answer | The product file, the citing blocks | 2.c re-tests 2.b's halves |
| 2.c | Check each half carries one trigger; loop to 2.a | A split that leaves a compound half undoes 2.b | The product file | The decoupeur, after this agent, on the same rule — the file says so itself |
| 2.d | Answers bringing a subject no title covers — a new block, by invocation 1's four moves | The `Block: -` answers point nowhere; without it a new subject is lost | The product file | 2.a |
| 2.e | Mark every entry `[integrated: …]` | The cycle routes on it | `cycle.md`, `2_structure.md` | — |
| 2.f | Write own questions file, even empty | Same as 1.6 | Same | — |

**The set.** Every move feeds something carried forward. 2.e is last and
says so; 2.c follows 2.b; nothing needs what a later move produces.
The one move that could go without something breaking here is 2.c — if
the decoupeur, which runs on the same rule right after, sweeps every
marked block; that is the decoupeur's file (last section). 2.a and 2.d
put the same trigger/output test to every answer twice; the file makes
the second sweep deliberate ("ask it of every answer"), and the cost is
one re-reading of a handful of answers — not a comment.

---

## Comments, in the order to apply them

### 1

    Fichier      : .claude/agents/redacteur.md
    Cible        : Part 1, "The two markers" — "You strip every marker
                   before writing, so only this turn's are marked";
                   and Invocation 2, "How you load the product file",
                   step 1.
    Aujourd'hui  : At invocation 2 the agent greps NEW and MODIFIED and
                   strips both from every title line, unconditionally,
                   before integrating anything. The same file defines
                   NEW as "a new block was never closed" and MODIFIED
                   as changed "against text that no longer stands",
                   and says the sondeurs and the decoupeur grep both
                   to know what to look at again.
    Le défaut    : Plane 2, question 1 — "only this turn's are marked"
                   assumes every earlier marker was consumed, and the
                   move does not check that. Known case: two passages
                   of one agent asking for different things. The
                   command sends the Rédacteur's own questions file
                   back to it before anything downstream runs ("Answer
                   them, then /1_lexique"; the agent: "Nothing
                   downstream runs while a flag stands"). So:
                   invocation 1 → flags answered → invocation 2 strips
                   every NEW no grid turn has seen; the blocks the
                   answers did not touch end up unmarked, and never
                   probed. Same after an invocation 2 on a grid file
                   that raises a flag of its own: the next invocation
                   2, on the Rédacteur's file, strips the MODIFIED the
                   grid has not yet seen.
    Ce qu'il faut: A marker is stripped only once the grid has consumed
                   it. Within this agent that is knowable from the
                   prefix of the file it integrates: a file from the
                   grid (sondeur-*) means a turn ran on the current
                   markers — strip, then re-mark; the Rédacteur's own
                   file means no turn ran — add this turn's markers,
                   strip none. Which marker the grid itself consumes
                   is the sondeur's business (last section).
    Justification: Robustness — a block created at invocation 1 and
                   untouched by the flag answers is never probed by the
                   grid; its gaps surface at the controleur, or in the
                   code, and cost the chain again.

### 2

    Fichier      : .claude/agents/redacteur.md
    Cible        : Part 1, "What the product file looks like" — "A
                   block already carrying a nature keeps it — you never
                   empty a line the classeur filled, unless the block's
                   marker sends it back."
    Aujourd'hui  : No marker is defined anywhere as "sending a nature
                   back". Two readings: MODIFIED empties the line
                   (every changed block loses its nature), or only the
                   cases invocation 2 names (a block of its own, each
                   half of a split) get an empty line. Two lines above,
                   "You write Nature: empty, always".
    Le défaut    : Plane 3, criterion 4 — two readings. Plane 2,
                   question 4 — a term nothing defines.
    Ce qu'il faut: One statement of which blocks get an empty Nature:
                   the ones this agent creates — from the idea file,
                   from an answer, from a split, the original of a
                   split included — and that every other block keeps
                   the line it carries, MODIFIED or not. "Always" then
                   reads as "on every block you create".
    Justification: Robustness — under the first reading the classeur
                   refills the nature of every changed block and a
                   block changed in wording only can come back with a
                   different nature; under the second nothing moves.
                   Two readers of this file produce two different
                   product files today.

### 3

    Fichier      : .claude/agents/redacteur.md
    Cible        : Invocation 1, after move 4 — "When the Product Owner
                   contradicts himself: the latest version applies.
                   Name the replaced sentence in your reply — not in
                   the product file".
    Aujourd'hui  : The agent picks one of two incompatible sentences by
                   position and records the choice only in its report.
                   The report is not a file: the command relays it,
                   nothing stores it, and the command's next-step
                   table has no row for it. The product file carries
                   no trace that a choice was made.
    Le défaut    : Plane 2, question 3 — a product decision the agent
                   takes alone, against its own "You never decide a
                   product matter … you produce a question". Known
                   case: two passages asking for different things —
                   move 4 says "transcribe one reading rather than
                   stopping" and flag it; this rule transcribes one
                   reading and flags nothing. For the command: an
                   outcome with no row.
    Ce qu'il faut: A contradiction is a case of move 4: transcribe the
                   later sentence, flag the block (the sentence set
                   aside is what the Clarification needed line names)
                   and raise the question. The reply need not carry
                   it; the questions file does, and the answer comes
                   back through invocation 2 like any other.
    Justification: Robustness — a contradiction settled by position is
                   silent in the file; a wrong pick reaches the code
                   and costs a correction cycle. Round trips — none
                   added: the question rides the questions file the
                   flags already create.

### 4

    Fichier      : .claude/agents/redacteur.md
    Cible        : Invocation 2, pass b, last paragraph — "If the block
                   carries a Clarification needed line on that subject,
                   remove it"; and invocation 1, move 4 — "you strip it
                   when you integrate that answer".
    Aujourd'hui  : In invocation 2 the strip of a flag is written under
                   pass b (split) only. An answer that merges into, or
                   replaces a sentence of, a flagged block — the first
                   two rows of pass a's table — has no strip
                   instruction where the reader is executing.
    Le défaut    : Plane 2, question 1 — the move reaches less than it
                   claims: the strip covers one row of four. A reader
                   running pass a on a merge leaves the flag standing.
    Ce qu'il faut: The strip belongs to pass a: every answer landing in
                   a block removes the Clarification needed line whose
                   wording matches its question, whatever the row.
                   Pass b then needs no separate mention.
    Justification: Robustness or round trips, by what downstream does
                   with a standing flag — neither this command nor
                   cycle.md reads the blocks. If nothing downstream
                   stops on it, the line is product text to the
                   convertisseur (robustness). If the next commands
                   stop on it — the verdict's sweep says they do — the
                   chain halts on a flag whose answer was already
                   integrated, and the fix is by hand (round trips).

### 5

    Fichier      : .claude/agents/redacteur.md
    Cible        : Invocation 2, pass e — "Mark every entry you
                   integrated — append [integrated: B7] to it in the
                   questions file, naming every block you wrote into."
    Aujourd'hui  : Only entries that wrote into a block are marked. An
                   answer that changes nothing — confirms the
                   transcribed reading, "as written" — writes into no
                   block and gets no mark. And the mark's position is
                   "append to it" — to the entry — while the questions
                   file rule says "four lines, no exception".
    Le défaut    : Plane 2, question 3 — the no-change answer is not
                   foreseen. Known case: a loop with no ceiling —
                   cycle.md reads a questions file as integrated when
                   "at least one entry carries [integrated:"; a file
                   whose every answer confirmed the text carries none,
                   reads as "answered, not integrated" (row 8), and is
                   sent back to this agent, which changes nothing
                   again.
    Ce qu'il faut: Every entry gets a mark once processed, including
                   one that changed nothing — a mark whose block list
                   is empty or "-" — so that "integrated" means
                   "consumed", not "wrote somewhere". And one stated
                   place for the mark (the end of the Answer: line, or
                   a fifth line — and the four-lines rule then says so).
    Justification: Robustness and round trips — removes an unbounded
                   loop in the cycle on a fully confirmed file; a fixed
                   position is what the cycle greps.

### 6

    Fichier      : .claude/agents/redacteur.md
    Cible        : Invocation 2, pass d, last sentence — "If pass d
                   finds something, the four moves of *When you read
                   the idea file* apply to it."
    Aujourd'hui  : No section of the file bears that title. The four
                   moves are under "INVOCATION 1 — Structuring".
    Le défaut    : Plane 2, question 4 — a reference to something the
                   reader has not seen.
    Ce qu'il faut: The reference names the section as it is titled, or
                   the four moves carry a title the reference resolves
                   to. Nothing else changes.
    Justification: Robustness — a reader who cannot resolve it falls
                   back on pass a's table, which skips move 2 (the
                   global's index): a subject the global already
                   carries gets a fresh title and the merge cannot
                   match it. Small, but it is the very case pass d
                   opens the index for.

### 7

    Fichier      : .claude/agents/redacteur.md
    Cible        : Part 2, last line — "Between two sessions, re-read
                   the product file — it is your state."
    Aujourd'hui  : An agent has no sessions: each invocation is a fresh
                   reader. "Re-read" reads as whole, against "You never
                   read it whole" (invocation 2) and "Read the product
                   file whole" under what you never do.
    Le défaut    : Plane 2, question 4 — a reference to something the
                   reader has not seen (a previous session). Known
                   case: two passages asking for different things.
    Ce qu'il faut: The line goes; invocation 2's loading procedure is
                   the only way the product file is read.
    Justification: Tokens — a reader who takes it literally loads the
                   whole product file ("hundreds of lines") at every
                   invocation 2, the cost the file itself calls "the
                   single most wasteful thing you can do here".

### 8

    Fichier      : .claude/agents/redacteur.md
    Cible        : Part 1, "Outgoing references are marked" — "marked
                   as existing when it is already in the global".
    Aujourd'hui  : The mark is required; the test for "already in the
                   global" is not stated. The agent holds only the
                   global's ^# index; a screen, a piece of data or a
                   state can exist in the global inside a block whose
                   title does not name it.
    Le défaut    : Plane 2, question 2 — a move resting on a fact
                   nothing gives it; question 1 — two readers do not
                   check it the same way (one greps the index, one
                   loads sections).
    Ce qu'il faut: One test: a destination is "existing" when a title
                   of the global's index names it, and only then; a
                   destination not found there is written without the
                   mark, and that is not a question to raise. (If the
                   index is judged too coarse, the rule says which
                   sections are loaded — a cost to state, not to
                   leave to the reader.)
    Justification: Robustness — "existing" tells the convertisseur and
                   the cadreur what is reused and what is built; a mark
                   set on a guess sends a lot to build on something
                   absent, or to build what exists. Tokens — without
                   the test, a careful reader loads global sections to
                   be sure, at every reference.

### 9

    Fichier      : .claude/agents/redacteur.md
    Cible        : "The shape of a questions file" — "your number: the
                   highest at the root, or in questions/redacteur/ if
                   the root holds none, plus one."
    Aujourd'hui  : "The highest at the root" does not say of which
                   prefix. At invocation 2 the root holds the file
                   being integrated, of another prefix. Reading A (any
                   prefix): questions-sondeur-03.md at the root and
                   01..04 already in questions/redacteur/ — the agent
                   writes questions-redacteur-04.md, which collides
                   when the command files it. Reading B (own prefix):
                   the root holds none, the folder gives 05 — no
                   collision.
    Le défaut    : Plane 3, criterion 4 — two readings, one of which
                   collides.
    Ce qu'il faut: The number is the highest redacteur number found in
                   the root and in questions/redacteur/ together, plus
                   one — unique for this prefix wherever the file ends
                   up.
    Justification: Round trips — a collision at filing leaves two
                   files at the root, and the next command stops on
                   "more than one — a filing failed".

### 10

    Fichier      : .claude/commands/2_structure.md
    Cible        : "What you read" — "One ls of the feature folder's
                   root, and nothing else"; "Never open a questions
                   file's content — its name is all you need". Against
                   "How it runs" — "Read that one heading" (the
                   blocking file's ## Decision), "If it carries an
                   empty Answer: — stop"; and "Once it has run" —
                   "Check questions-redacteur-NN.md was written".
    Aujourd'hui  : The reading list forbids what three later steps
                   require: one heading of the blocking file, the
                   Answer: lines of the file to integrate, a second
                   look at the root after the run.
    Le défaut    : Known case: two passages asking for different
                   things. For the command: its checks rest on reads
                   it says not to do.
    Ce qu'il faut: The reading list names exactly the reads the command
                   does — the ls, before and after the run; the ##
                   Decision heading of blocked_redacteur.md; a grep for
                   an empty Answer: in the file to integrate — and
                   "nothing else" then holds.
    Justification: Robustness — an orchestrator that honours "never
                   open a questions file's content" skips the
                   empty-Answer check and hands an unanswered file to
                   the agent, which has no rule for an entry without
                   an answer (it is told the Product Owner filled
                   them) and guesses or blocks.

### 11

    Fichier      : .claude/commands/2_structure.md
    Cible        : "Then, which invocation and which file" — the row
                   "One, any prefix → 2 — Integrating".
    Aujourd'hui  : A questions file with no ### Q entry — the agent
                   writes one at every invocation, "even empty" — sits
                   at the root after every invocation 2 with nothing
                   to ask. It has no Answer: line, so the empty-Answer
                   stop does not fire, and the command runs invocation
                   2 on a file with nothing to integrate.
    Le défaut    : Known case: an invocation that produces nothing, in
                   a case where the agent has nothing to do. For the
                   command: a row for a case the agent has no work for.
    Ce qu'il faut: A row for the empty file: nothing to integrate, the
                   agent is not invoked, and the next step is the one
                   the last table already gives for that state
                   (/3_decoupe).
    Justification: Round trips and tokens — a worktree, a commit, a
                   full invocation and a merge for an empty result, on
                   a state one grep reads.

### 12

    Fichier      : .claude/commands/2_structure.md
    Cible        : Same table — the row "No questions file → 1 —
                   Structuring".
    Aujourd'hui  : The choice reads the questions files only. With no
                   questions file at the root and desc-produit.md
                   already there (once a later command has filed the
                   Rédacteur's empty file, or after any filing by
                   hand), the command runs invocation 1 on idees.md
                   over an existing product file. The agent has no
                   rule for that state: invocation 1 creates blocks and
                   numbers them "as you write", and Part 1 says "always
                   a targeted edit, never the whole file" — it rewrites
                   the file (renumbering every block the filed
                   questions cite) or duplicates every block.
    Le défaut    : Plane 2, question 3, on the agent — unforeseen, the
                   agent invents. For the command: a row for a case
                   the agent cannot do.
    Ce qu'il faut: Invocation 1 is chosen only when no product file
                   exists. No questions file and a product file → stop
                   and say so; the idea file is transcribed once.
    Justification: Robustness — a second transcription renumbers or
                   duplicates blocks and every filed question points at
                   the wrong one. Round trips — the product file would
                   then be repaired by hand.

### 13

    Fichier      : .claude/commands/2_structure.md
    Cible        : The Agent(...) block under "How it runs" and the
                   second one under "Invocation parameters".
    Aujourd'hui  : Two invocation templates. The first carries the
                   invocation number, the file to read and the optional
                   blocking file. The second is generic —
                   subagent_type="<agent>", description="<phase>
                   <feature>", a prompt with no Read: line — while the
                   command says "Name the file, always — the agent
                   opens that one and no other".
    Le défaut    : Known case: two passages asking for different
                   things. For the command: a prompt that does not
                   carry what the agent needs.
    Ce qu'il faut: One template, the complete one; the parameter notes
                   (no effort, no run_in_background, no isolation) sit
                   under it.
    Justification: Robustness and round trips — an orchestrator
                   following the second template names no file; the
                   agent is told not to look for itself, so the
                   invocation blocks or guesses, and is redone.

### 14

    Fichier      : .claude/commands/2_structure.md
    Cible        : "How it runs", first step — "First, file the
                   lexicographe's questions file".
    Aujourd'hui  : The git mv is unconditional. A
                   questions-lexicographe-NN.md at the root is filed
                   whatever it holds — answered and settled by
                   /1_lexique, answered and not yet settled, or
                   unanswered. Only the file that remains is checked
                   for an empty Answer:.
    Le défaut    : For the command: a row (file it) covering a case
                   where it is wrong (its questions are still waiting).
                   Plane 2, question 3 — unforeseen: the vocabulary
                   those answers carry never reaches the lexicon, and
                   the Rédacteur integrates the other file against a
                   lexicon missing it.
    Ce qu'il faut: The lexicographe's file is filed only when nothing
                   in it waits: an empty Answer: in it stops the
                   command the same way it does for the file to
                   integrate. Whether "answered" suffices or the
                   lexicographe leaves a mark of its own to test — last
                   section.
    Justification: Robustness — cycle.md guards this by its routing (an
                   empty Answer: in the latest file stops it); the
                   hand-run command does not, and a filed-away
                   unanswered file is invisible to every later routing.

### 15

    Fichier      : .claude/commands/2_structure.md
    Cible        : "Once it has run" — nothing.
    Aujourd'hui  : cycle.md, "After /1_structure": "The invalidation is
                   the command's own — it deletes desc-par-nature.md
                   and spec-technique.md when a NEW appeared, and
                   nothing otherwise. You do not repeat it. You read
                   its report — which files it deleted, or that none
                   needed it." 2_structure.md has no such step, and
                   nothing in it says the report carries it.
    Le défaut    : For the command: an outcome (a NEW block after the
                   file was reclassed or converted) with no row. Known
                   case: two passages asking for different things —
                   across the two commands that name this agent.
    Ce qu'il faut: One of the two holds. Either this command deletes
                   the derived files when the run created a NEW block
                   and its report says which, or cycle.md stops
                   claiming it and does it itself. The first is where
                   the knowledge is: this command is the one that sees
                   the NEW appear.
    Justification: Robustness — a NEW block after conversion leaves a
                   spec-technique.md that does not carry it; cycle.md's
                   row 13 then splits and codes a technical document
                   missing a block, and the gap surfaces at the
                   controleur.

### 16

    Fichier      : .claude/commands/2_structure.md
    Cible        : "Once it has run" — git mv blocked_redacteur.md →
                   blocked_redacteur-NN.md.
    Aujourd'hui  : NN has no rule.
    Le défaut    : Plane 2, question 4 — a placeholder with no rule for
                   what fills it.
    Ce qu'il faut: The same rule as the questions files: the highest
                   blocked_redacteur-NN.md in the folder, plus one; 01
                   when none.
    Justification: Round trips — a guessed number that collides fails
                   the git mv and leaves the block standing for the
                   next run. Small.

### 17

    Fichier      : .claude/commands/cycle.md
    Cible        : The rows that route to or from this agent — 6b, 7
                   ("redacteur → /1_structure"), 8, 16 — and the header
                   list /1_structure, /2_grille, /3_reclasse,
                   /4_convertit, /7_decoupe.
    Aujourd'hui  : The command that invokes the Rédacteur is
                   2_structure.md; /1_structure exists nowhere under
                   .claude/commands/. The other names in the same rows
                   match no file either, and 2_structure.md's own
                   next-step table names /1_lexique and /3_decoupe.
                   (Only the Rédacteur's rows are this pass's; the
                   pattern is the whole table's.)
    Le défaut    : For the command: every row for this agent names a
                   next step that cannot run.
    Ce qu'il faut: The rows name the commands as they exist. And
                   /1_lexique has a place in the routing that row 8
                   skips: 2_structure.md sends an answered Rédacteur
                   file through it before integration; cycle.md's row 8
                   sends the answered file straight to integration.
    Justification: Robustness — the chain stops at its first routing,
                   or the orchestrator maps the names by guess.

### 18

    Fichier      : .claude/commands/cycle.md
    Cible        : The routing table, rows 6a–6c and 12; the state
                   table, "Integrated — at least one entry carries
                   [integrated:".
    Aujourd'hui  : Rows 6a–6c route on "the latest questions file is
                   integrated". 2_structure.md files the integrated
                   file into questions/<agent>/ inside the worktree,
                   before the merge, and leaves at the root the
                   Rédacteur's fresh file — never integrated. After
                   /2_structure, rows 6a–6c cannot match. The fresh
                   file is either waiting (row 5 stops — right) or
                   empty; row 12 has branches for sondeur and
                   convertisseur and none for redacteur; rows 13–16
                   require "no questions file"; the chain lands on row
                   17, error, after every clean integration.
    Le défaut    : For the command: rows reading a state the invoking
                   command never leaves; a case (an empty Rédacteur
                   file) with no row.
    Ce qu'il faut: The routing reads the state 2_structure.md leaves —
                   the integrated file filed, the latest at the root
                   the Rédacteur's own. An empty redacteur file routes
                   where 2_structure.md's own table sends it
                   (/3_decoupe, then on to the grid); rows 6a–6c
                   either go or test the filed folder.
    Justification: Robustness — the cycle errors out after every
                   successful /2_structure, on the normal path.

---

## Swept and found sound

Recorded so the sweep is not read as a sample: 1.1 (test stated —
trigger and output — checkable by two readers); 1.3's numbering and
its "never passes into the global"; 1.5 (two features — the blocking
file's four headings, empty Decision, resume path via the prompt);
1.6/2.f (empty file is a result, missing file is a failure — both
readable by the command); the Block: line rules; the blocking-file
rules (block only when producing is impossible; doubt is flagged); the
Edit-failure rules; 2.0's four steps; 2.a's table (four rows, each
with a test); 2.b's citation update; 2.d's "do not open the index when
nothing is found"; Part 2's "the prompt says which one"; the command's
git sequence (commit first, worktree from HEAD, enter before invoking,
merge before handing back); the command's next-step table, apart from
the outcomes comments 3, 11, 12 and 15 add.

Left as preference, not written: 1.3's restatement of 1.1's criterion;
the product-specific examples ("retention, export, consent, minimum
age"; "past 250 KB") under rules that already state the class; three
bullets under "What you never do" that the first bullet already covers;
the block example split in two by three paragraphs of rules.

---

## From the verdict

Read last: section 2's Rédacteur line, sections 4 to 7. One entry per
item that names this agent.

**Section 2 — "the role holds … its weakness is not the role but its
unchecked output".**
Not found above, and not a comment on this agent: the agent says of
invocation 2 "Never idees.md — it is transcribed; the answers revise
what came of it", so nothing in it or its command reads the product
file back against the idea file. A check would be a new invocation
(the verdict's P6 "Coverage"), not a rule here.

**D1 / P6 — the idea file has no reader after structuring.**
Same as above. Not found; confirmed by the agent's own "Never
idees.md".

**D2 / A3 / item 6 — are block identifiers stable across integration?**
Contradicted by the agent — it states it: "Numbering: assigned as you
write, never reassigned — the questions file addresses blocks by
number"; at a split "The original keeps its number … The new blocks
take the next free numbers"; a contradicting answer "replaces that
sentence, never sits beside it" — the block, and its number, stay. And
"The number is local to the feature file and never passes into the
global". Item 6 closes on this file. (Comment 12 is the one route by
which numbers would shift — a second invocation 1 over an existing
file — and it is the command's, not the agent's.)

**D3 / A2 / P5 / item 23 — a forgotten MODIFIED has no detector; does
the Rédacteur diff the product file?**
Not found as such. The agent states the rule ("MODIFIED on every block
you change — whether or not a question named it") and neither it nor
its command verifies it; no diff anywhere in the three files. What this
pass adds (comment 1): markers are also lost *by rule*, not only by
omission — the agent strips every marker at invocation 2 before any
grid turn has consumed them. A byte diff between turns, where the
verdict puts it, would catch both.

**D5 / item 12 — `[integrated: B7]` has a producer and no reader.**
Contradicted by the command: cycle.md reads it for routing — "Integrated
— at least one entry carries `[integrated:`", rows 6a–6c and 8. It is
a routing signal, not the check the verdict hoped for; and as written
it fails on a fully confirmed file (comment 5) and on the state
2_structure.md leaves (comment 18). Nothing checks that *every*
answered entry carries it.

**D9 / item 10 — the preamble's dependencies "come from the Rédacteur"
by no named artefact; is text outside blocks written or probed?**
Not found above. The agent's structure allows text under `#
Application`, and no move writes anything outside a block: all four
moves of invocation 1 and all five passes of invocation 2 produce
blocks. The only dependency this agent writes is the "— existing" mark
inside a block (comment 8). If the convertisseur expects a preamble
from the Rédacteur, the move that writes it does not exist here — that
is for the group pass, with `convertisseur.md`.

**D10 — technical questions travel the product route to the
Rédacteur.**
Not found as a distinct comment. The agent says "Invocation 2 serves
every filled questions file — whichever agent wrote it … Same work
whoever asked", and pass d admits an answer that lands "in none" — with
no rule for what then. A technical answer therefore ends as a mark
with no block (comment 5's case), and the product file carries nothing
of it. The route is the verdict's concern; the agent's part is that
"none" has no outcome.

**D13 / A5 — the global's index is the Rédacteur's only instrument;
the global is assumed true.**
Not found, and not this agent's: move 2 does what the verdict describes
("A near title is a doubt, and a doubt is settled by reading. Load that
section"), and it trusts the index — comment 8 is where that trust
should at least be stated as the test.

**A1 / item 7 — what is written when an answer confirms a block as it
stands?**
Found in part. The agent's pass-a table settles more of it than the
verdict allows: an answer that names a case the text is silent on
"merges into the block, as a sentence" (same trigger, same output), and
one that resolves an ambiguity "replaces that sentence" — both leave a
trace in the block. The residue is the answer that changes no sentence;
for it the agent writes nothing, and comment 5 puts the trace in the
questions file (the mark), not in the block. A block-level trace was
considered and left: it would be a new artefact another agent (the
sondeur) has to read, which is the group pass's call.

**U3 — the Rédacteur's own signal, bound none stated.**
Consistent with the agent and the command. Comments 11 and 18 are
about what the commands do with the empty file that ends it.

**P13 — the whole product file is written in one invocation; the
failure mode is silent truncation.**
Not found above — the known case "more context than one agent holds —
it degrades instead of stopping". What the agent says: nothing.
Invocation 1 reads `idees.md` whole ("free-form and in French, that is
the point") and writes every block in one invocation; no rule tests the
idea file's size, splits invocation 1, or tells the agent to stop and
write `blocked_redacteur.md` when it cannot hold the file. The command
runs it once. The verdict is right that this breaks by scale, not by
logic; this pass has no measurement of where the ceiling sits, which is
why it is recorded here and not as a numbered comment.

**Correction after reading the verdict.** Comment 4's justification
first said a standing flag is "checked by nothing downstream". The
verdict's sweep (row 9) says `/3_decoupe`, the Découpeur and the
Sondeur stop on it — files this pass did not read. The justification
now names both outcomes; the measure moves in either.

---

## What another agent would settle

    Does the angle Sondeurs' pass A select blocks by NEW/MODIFIED
    alone, and does the global invocation's record cover unmarked
    blocks?
    sondeur.md
    Marker-only: comment 1 is the largest gap of this pass — blocks
    created at invocation 1 and untouched by the flag answers are
    never probed. Record covers all: the loss is a token cost (the
    global re-reads them), and comment 1 stands as a contradiction in
    the marker's stated meaning.

    Does the Découpeur sweep every marked block on the one-trigger
    rule, or only what invocation 2 could not see?
    decoupeur.md
    Sweeps all: move 2.c can go (one fewer pass, no round trip lost).
    Only the unseen: both stay, and the agent's "you split what an
    answer tells you to; it splits what a block turned out to hold" is
    the boundary.

    Does the Classeur check the nature a MODIFIED block carries, or
    only fill empty lines?
    classeur.md
    Checks: comment 2's reading holds — a changed block keeps its
    nature. Fills only: comment 2 must instead empty the line on a
    block whose trigger or output changed, or a stale nature reaches
    /5_reclasse.

    Does the Lexicographe leave a mark on an answered file once its
    answers are settled in the lexicon?
    lexicographe.md
    Yes: comment 14's filing test is that mark. No: the empty-Answer
    grep is the only test the command has, and an answered-but-not-
    settled lexicographe file is filed as if settled.

    Does the Fusionneur match blocks on titles or on content?
    fusionneur.md
    Titles: move 1.2's verbatim reuse is load-bearing and comment 6 is
    larger than "small". Content: 1.2 still guards duplicates inside
    the feature file, and its verbatim rule could relax.

    Does /3_decoupe, or any later command, file the Rédacteur's empty
    questions file away from the root?
    the 3_decoupe command (and 3b_nature, 4_grille)
    Yes: comment 12's state — product file, no questions file — is the
    normal state after every turn, and the guard is needed. No:
    comment 11's empty-file row is hit on every re-run of /2_structure.

    Do the Découpeur and the Sondeurs stop on a Clarification needed
    line, as the verdict's sweep says?
    decoupeur.md, sondeur.md
    Yes: a flag left by comment 4's gap stops the chain — round trips.
    No: it is product text to the convertisseur — robustness.

    Does the convertisseur read text outside blocks, and does it expect
    a preamble from the Rédacteur?
    convertisseur.md
    Expects one: a move is missing in this agent (no move writes
    outside a block). Reads none: D9 is the convertisseur's own
    sentence to correct.

    Does anything downstream act on the "— existing" mark?
    convertisseur.md, cadreur.md
    Yes (production vs modification is declared from it): comment 8's
    test is load-bearing. No: the mark and its test can both go —
    tokens.

    Does the global exist before a project's first feature?
    the socle and extrait commands
    Yes: nothing. No: invocation 1's "grep the global's index" is a
    missing input on every new project, and the agent blocks on the
    first feature by its own rule ("a file you were told to read that
    is not there").

