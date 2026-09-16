# sondeur — phase 3 comments

Read: `.claude/agents/sondeur.md` (whole); `.claude/commands/4_grille.md`
(whole, the only command that invokes it); `.claude/commands/cycle.md`
(whole, routes its outcomes). `3_decoupe.md` and `3b_nature.md` name the
sondeurs but invoke nothing — not read beyond the grep.

---

## Plane 1 — the agent as a whole

**Role, from the file:** take every question of the framing grid to the
product file and write down, as questions for the Product Owner, what
the document leaves open — three invocations run pass A over the blocks
that moved, each in its own reading order; a fourth records every block,
crosses the record (pass B) and probes the feature (pass C).

**Moves, in order:**

| # | Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|---|
| 1 | Read the product file whole, the grid whole, a blocking file if named | Everything below rests on them | Moves 4–8 | — |
| 2 | Stop on `**Clarification needed:**`; stop on an empty or short read | Not to close a text about to change; not to probe a truncated read | The blocking file (move 3) | Its first half re-does the command's own grep |
| 3 | Write `<out>/blocked_<name>.md` when producing is impossible | The only channel a stop survives | The command's "Before anything else" | — |
| 4 | Take invocation, blocks and reading order from the prompt | Decides which pass runs on which blocks | Moves 5–8 | — |
| 5 | Angle: pass A on the named blocks, in the given order | Finds the gaps inside one block | Questions file → assembleur | The global's record extracts A1.x/A4 answers from the same blocks |
| 6 | Global: the record, every block | Makes crossing tractable and checkable | Pass B (same invocation); `releve.md`, filed, read by nothing after | See 5 |
| 7 | Global: pass B from the record alone | Finds the gaps between blocks | Questions file | — |
| 8 | Global: pass C on the feature | Finds the gaps at feature level | Questions file | — |
| 9 | The three-outcome test per question (settled / open / does not apply) | Turns a grid question into a gap, or not | Moves 5, 7, 8 | — |
| 10 | Write the questions file: format, `Block:` line, one gap one question, written even when empty | What the assembleur merges and the PO answers | assembleur → `questions-sondeur-NN.md` | — |

**Judgement of the set:**

- Every move feeds the questions file or the blocking file, except the
  first half of move 2, which the command already guarantees (comment 3).
  `releve.md` is read by nothing once pass B has used it; kept as a filed
  trace, it costs nothing after it is written.
- No job falls between moves. Moves 5 and 6 both extract A1.x/A4 answers
  from the same blocks in the same turn; they run in parallel, so neither
  can feed the other. A design choice; it cannot be priced without the
  grid, which this pass does not open.
- Order inside the agent is right (record before pass B). The command's
  order is not — comment 10.
- Three angles differing only by reading order are three opus reads of
  the same two files per turn; on a later turn with two blocks in scope
  the three readings are close to identical. Whether the second and
  third angle earn their cost is a measurement — the yield of each
  angle over a real cycle — not something this pass can settle from the
  files. Noted, no comment.

---

## Comments

### 1

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Where you work", the sentence introducing the reading table
    Aujourd'hui  : "Two things to read, and nothing else:" followed by a
                   three-row table — product file, grid, blocking file.
    Le défaut    : Plane 2, Q4 — a count that no longer matches what follows
                   it. The blocking file is either inside "nothing else" or
                   not; the sentence reads both ways.
    Ce qu'il faut: The count matches the table: two files always, a third
                   only when the prompt names it — so that a named blocking
                   file is unambiguously among what may be read.
    Justification: Round trips, marginal — an agent that reads "nothing else"
                   strictly skips the decision that lifts its block and
                   blocks again on the same cause.

### 2

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Where you work", the grid row — "Whole"
    Aujourd'hui  : Every invocation reads the grid whole. The angles run
                   pass A only; the global runs the record, pass B, pass C.
    Le défaut    : Plane 2, Q2 — a file read whole where a section would do,
                   paid at every invocation, four times a turn.
    Ce qu'il faut: Each invocation reads the part of the grid its passes
                   use — pass A for the angles; for the global, the
                   questions the record extracts, pass B and pass C — plus
                   whatever the grid marks as common to every pass. If the
                   grid is not sectioned by pass, this comment falls; the
                   pass forbids opening it, so the condition is for the
                   group pass to check.
    Justification: Tokens — three invocations per turn carry two passes they
                   never run, on every turn.

### 3

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Where you work", the first of the two stops —
                   `**Clarification needed:**`
    Aujourd'hui  : The agent stops on that line and blocks, naming the block.
    Le défaut    : Known list — a net. The command greps `Clarification
                   needed` in the product file and stops before invoking;
                   the agent's test (`**Clarification needed:**`) is
                   narrower than the command's, so it can only fire where
                   the command's fires, and the command's fires first. If
                   it ever did fire, four sondeurs would write four blocking
                   files for one cause, and the command's table handles
                   "one".
    Ce qu'il faut: The agent does not re-check what its command guaranteed;
                   the stop goes. The command's grep is the net.
    Justification: Tokens, small — lines read four times a turn. Round trips
                   in the theoretical case: four blocking files for one
                   cause, a table that expects one.

### 4

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Where you work", the second stop — "A file that comes
                   back empty or short"
    Aujourd'hui  : "short" has no test. The product file of a small feature
                   is short by nature.
    Le défaut    : Plane 2, Q1 — two readers cannot check it the same way.
                   Plane 3, criterion 4.
    Ce qu'il faut: The stop names an observable: the read returned less than
                   the file holds — a truncation the tool signals, a text
                   that ends mid-block, a heading with no body after it —
                   or nothing at all. A small file that reads whole is not
                   a stop.
    Justification: Robustness — a truncated read probed as complete closes
                   half a document with no signal. Round trips — a small
                   file blocked as "short" stops four invocations for
                   nothing.

### 5

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Invocation 1 — Which blocks"
    Aujourd'hui  : "On a first turn it names none, and every block is probed.
                   On a later turn it names a few — those marked NEW or
                   MODIFIED; a block an answer touched carries MODIFIED."
    Le défaut    : Plane 3, criterion 5 — commentary on how the list came to
                   be, given to an agent that does not select blocks. Plane
                   2, Q4 — it reads two ways: an agent that sees a MODIFIED
                   block outside its list, or a listed block with no
                   marker, has two authorities. And the prompt does not
                   "name none" on a first turn — the command writes "Pass A
                   on these blocks: every block". Plane 2, Q3 — a listed
                   identifier the product file does not hold has no
                   foreseen outcome.
    Ce qu'il faut: The prompt's list is the only authority — "every block",
                   or identifiers — and the marker explanation goes. A
                   listed identifier absent from the product file is a
                   stop, naming it.
    Justification: Robustness — one authority for the scope, so the three
                   angles probe the same blocks and the merge compares like
                   with like; an absent identifier stops instead of being
                   guessed at. Tokens, marginal.

### 6

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Invocation 2 — 1. The record", the list of identifiers
    Aujourd'hui  : The agent names which grid identifiers the record holds:
                   A1.1, A1.2, A1.3, A1.4, A1.9, A4.
    Le défaut    : Plane 2, Q2 — a fact with two possible owners. If the grid
                   says which answers pass B crosses, the agent duplicates
                   it and goes stale on the grid's next edit; if the grid
                   does not, the coupling lives only here and nothing in
                   the grid signals a new crossing column. Plane 3,
                   criterion 1.
    Ce qu'il faut: One owner. Either the grid names the record's columns and
                   the agent says "the identifiers pass B crosses, as the
                   grid lists them", or the agent owns the list and the
                   grid is known to say nothing. Which is true I could not
                   check — the grid is outside this pass's reading.
    Justification: Robustness — a crossing column added to the grid and not
                   to the record is a class of gaps pass B never sees, with
                   no signal.

### 7

    Fichier      : .claude/agents/sondeur.md
    Cible        : "What you are looking for", the third outcome — "The
                   question does not apply here — move on"
    Aujourd'hui  : The settled outcome has a test ("the answer is there, in
                   the terms the question asks for"); the open outcome has
                   one; "does not apply" has none. "In doubt, ask" is the
                   tie-break, but doubt is not defined either.
    Le défaut    : Plane 2, Q1 — what is not in the list passes: the one
                   outcome that dismisses a question with nothing written
                   is the one with no test.
    Ce qu'il faut: A test for inapplicability two readers check the same
                   way — the question presupposes something the block does
                   not have (an input, a stored value, a screen), or the
                   grid itself scopes the question to a nature the block
                   does not carry. Anything else is open.
    Justification: Robustness — this is the only exit through which a real
                   gap leaves the pass with nothing written.

### 8

    Fichier      : .claude/agents/sondeur.md
    Cible        : "The Block: line" — "a pass A gap that only shows against
                   another names both"
    Aujourd'hui  : Elsewhere: "a pass A question stands on its block alone",
                   "Close a pass A gap because another block settles it —
                   that is pass B's". Here: a pass A gap may carry two
                   identifiers.
    Le défaut    : Known list — two passages asking different things. A gap
                   that shows only against another block is a crossing,
                   which the agent assigns to pass B; a pass A gap sits in
                   one block and would be found on that block alone. Two
                   angles will write one gap as `Block: B9` and
                   `Block: B7, B9`, and a merge by identifier keeps both.
    Ce qu'il faut: A pass A gap names the one block that lacks the thing. A
                   gap that exists only between two blocks is pass B's, and
                   pass B names both.
    Justification: Round trips — one gap, two questions to the PO.
                   Robustness — the Rédacteur integrates the answer into
                   one of two blocks.

### 9

    Fichier      : .claude/agents/sondeur.md
    Cible        : "What you write" — "never the grid identifier that raised
                   it. The identifier belongs to the record"
    Aujourd'hui  : The question text carries no grid identifier, and no field
                   carries it either. The record section says of the same
                   identifier that it "is what makes one block's answers
                   comparable to another's".
    Le défaut    : Two passages of one agent valuing one datum differently.
                   The questions file is read first by a merge across four
                   readings, and only then by the PO; the merge compares
                   two angles' questions on the same block by wording
                   alone. The reason given — a question put to the PO —
                   argues against the identifier in the question text, not
                   against a field of its own.
    Ce qu'il faut: What identifies a gap — block plus grid question — travels
                   with the question, in a field the merge can compare and
                   the PO can ignore; the question text stays direct.
                   Whether the assembleur uses it is for its file to say
                   (closing section); the agent should not destroy it on
                   the assumption.
    Justification: Round trips — one gap, worded differently by two angles,
                   reaches the PO twice; two distinct gaps worded alike
                   collapse into one answer. Tokens in the merge.

### 10

    Fichier      : .claude/commands/4_grille.md
    Cible        : Order of sections — "Git, in this mode" after "The four
                   invocations", "Then the merge", "Once it has reported"
    Aujourd'hui  : The steps that must precede any invocation — file the root
                   questions files, file the previous turn's
                   cadrage-produit files, commit, create the worktree from
                   HEAD, enter it, mkdir — are stated three sections after
                   the invocations they precede.
    Le défaut    : Plane 1 — a constraint stated after what it constrains.
                   The command itself records the cost of invoking before
                   the session is isolated.
    Ce qu'il faut: The command reads in execution order: pre-checks, filing,
                   commit, worktree, mkdir, block selection, invocations,
                   merge, filing of outputs, merge-push-remove, relay.
    Justification: Round trips — four opus invocations redone when the
                   worktree comes late, which the file says has happened.

### 11

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Git, in this mode" — "Before invoking, file every root
                   questions-*.md"
    Aujourd'hui  : Every root questions file is filed with no check on its
                   state. The command's own rule says a file stays at the
                   root while it waits to be answered or integrated;
                   `/cycle` tests this (its row 5), the hand-run command
                   does not.
    Le défaut    : Command question 1 — a case with no row. `/4_grille` run
                   on a root file with an empty `Answer:` (or answered, not
                   integrated) files it away, greps the same markers as
                   last turn, and re-raises the same gaps through five
                   invocations; the PO then holds two copies of one
                   question set.
    Ce qu'il faut: Before filing, a grep on the latest root questions file —
                   an empty `Answer:`, or no integration mark — and the
                   command stops, saying what to run. Greps only, in line
                   with "What you read".
    Justification: Tokens — four opus and one sonnet invocation for a turn
                   that produces nothing new. Round trips — the PO answers
                   the same questions twice.

### 12

    Fichier      : .claude/commands/4_grille.md
    Cible        : The four sondeur prompts, the line
                   `<Plus: cadrage-produit/blocked_par-bloc.md, its decision is filled.>`
    Aujourd'hui  : Every other path in the prompt is `docs/features/<name>/…`;
                   the blocking file is named relative to the feature
                   folder.
    Le défaut    : Plane 2, Q4 — a file named without its path, to an agent
                   whose rule is "every path relative to the repository
                   root". The command says itself what an agent does with a
                   missing target: it searches.
    Ce qu'il faut: The blocking file named with the same root-relative path
                   as the rest of the prompt.
    Justification: Round trips — an agent that cannot find the decision
                   blocks again on a lifted block, or searches (tokens)
                   before finding it.

### 13

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Which blocks the angles probe" — the two greps
    Aujourd'hui  : `NEW` and `MODIFIED` grepped as bare words in the product
                   file; the identifiers of the matching blocks go into
                   three prompts. Nothing says the marker's exact shape, nor
                   how a hit yields a block identifier.
    Le défaut    : Plane 2, Q1 — a bare word matches prose (a title carrying
                   "NEW", a block about a new record). Plane 2, Q4 — the
                   `<list>` placeholder has no rule for what fills it: a
                   hit's line may or may not carry the identifier. The
                   marker's shape and placement are the Rédacteur's —
                   closing section.
    Ce qu'il faut: The grep matches the marker's exact form as the Rédacteur
                   writes it, and the command says how a hit becomes an
                   identifier — the heading it sits on, or a grep that
                   returns the heading.
    Justification: Robustness — a block missing from the list is a block
                   three angles do not probe this turn, with nothing
                   signalling it. Tokens — a false match probes a block
                   that did not move.

### 14

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Before anything else" — nothing on the Nature line
    Aujourd'hui  : The third angle reads by nature; nothing checks that every
                   block carries a filled Nature line before the four are
                   invoked. In the cycle `/3b_nature` runs before; by hand,
                   nothing forces it.
    Le défaut    : Plane 2, Q3 — a move resting on a fact nothing guarantees
                   at this point. The agent forbids departing from its
                   order but does not say what to do when the order cannot
                   be built; faced with a block without nature it groups by
                   judgement.
    Ce qu'il faut: A grep before invoking — every block has a filled Nature
                   line — and a stop naming the blocks and `/3b_nature`
                   otherwise. The line's shape is the classeur's — closing
                   section.
    Justification: Robustness — a block probed in an invented grouping, or
                   left out of the by-nature reading, with no signal. Round
                   trips — caught by a grep, not by one of four invocations.

### 15

    Fichier      : .claude/commands/4_grille.md
    Cible        : The third angle's prompt — "Gather the blocks of one
                   nature, probe them together, then move to the next
                   nature"
    Aujourd'hui  : "probe them together" reads two ways: read them side by
                   side and probe each; or answer a grid question once for
                   the group.
    Le défaut    : Plane 2, Q4 — an instruction that reads two ways, against
                   the agent's rule that a pass A question stands on its
                   block alone (comment 8).
    Ce qu'il faut: The order says what it means: the grouping orders the
                   reading; every block is still taken through every
                   question on its own.
    Justification: Robustness — a question answered once for a group is a
                   gap in the blocks of the group that did not settle it.

### 16

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Then the merge" (the existence check), the file's last
                   line ("If an agent returns a blocked_*.md"), and the
                   "What you relay" table
    Aujourd'hui  : A missing questions file "stops the command — say which".
                   The blocking-file case is one line at the very end. A
                   sondeur that blocked has, by the agent's own rule,
                   written no questions file — so the existence check fires
                   on it and reports "missing". The relay table has no row
                   for a reading missing without a blocking file, nor for
                   the Clarification stop (stated inline higher up).
    Le défaut    : Command question 1 — an outcome with no row; two rules for
                   one event with no order between them.
    Ce qu'il faut: One check, in order, for each expected file: present;
                   else its blocking file present → relay it (row 1); else
                   missing → a row saying what to run (`/4_grille` again).
                   The Clarification stop gets its row.
    Justification: Round trips — a PO told "par-bloc.md is missing" has to
                   work out that a decision awaits her in
                   blocked_par-bloc.md.

### 17

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Before anything else" — the case "One, its Decision
                   filled" — together with the filing of the previous
                   turn's six cadrage-produit files
    Aujourd'hui  : On a re-run after one sondeur blocked, the three readings
                   that completed are filed to `closed/` as if the turn had
                   closed, and all four are invoked again; only the blocked
                   one receives the decision.
    Le défaut    : Known list — work done twice: three readings recomputed on
                   a product file that has not changed, because the command
                   does not keep their output.
    Ce qu'il faut: A re-run on a filled sondeur decision invokes the blocked
                   reading alone, leaves the other three files in place,
                   then merges — nothing ran on the product file between
                   the two runs. If the markers changed in between, it is a
                   new turn and all four run.
    Justification: Tokens — three opus invocations per occurrence. Blocks are
                   rare for this agent (after comments 3 and 4, few causes
                   remain), so the saving is per block, not per turn.

### 18

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Once it has reported" — `blocked_par-bloc-NN.md`;
                   "Git, in this mode" — `closed/par-bloc-NN.md`
    Aujourd'hui  : `NN` is defined once, for `questions-sondeur-NN.md`
                   (highest in `questions/sondeur/`, plus one). For the six
                   closed files and the filed blocking file it is a
                   placeholder with no rule — and the closed files are
                   filed before the new NN is computed.
    Le défaut    : Plane 2, Q4 — a placeholder with no rule for what fills it.
    Ce qu'il faut: One rule: the closed files and the filed blocking file
                   take the number of the turn that produced them — the
                   `questions-sondeur-NN.md` they fed; a blocked turn that
                   produced none takes the number it would have taken.
    Justification: Round trips — a collision on `git mv` stops the command;
                   a wrong number breaks the audit of a turn afterwards.

### 19

    Fichier      : .claude/commands/4_grille.md
    Cible        : "Once it has reported" — copy `questions.md` to
                   `questions-sondeur-NN.md`, renumber `Q1` upward, drop
                   `## Merge`
    Aujourd'hui  : "What you read: greps, and nothing else — never a
                   questions file's content"; "git mv, never a
                   read-and-rewrite"; and here a copy that renumbers entries
                   and drops a section — a read-and-rewrite, by the
                   orchestrator, of the file the PO will answer, under "you
                   rephrase nothing".
    Le défaut    : Two passages asking different things. A model rewriting a
                   file of fifty entries by hand is exactly where an entry
                   is dropped or altered.
    Ce qu'il faut: The file the assembleur writes is the file the PO answers,
                   byte for byte — numbered from Q1, no working section — so
                   that the command's step is a copy. If the `## Merge`
                   section is wanted, it goes to a file of its own. What
                   the assembleur writes today is for its file — closing
                   section.
    Justification: Robustness — a question lost or reworded between the merge
                   and the PO. Tokens — the orchestrator's context holds the
                   whole questions file every turn.

### 20

    Fichier      : .claude/commands/4_grille.md
    Cible        : "What you read" (`CALIBRATION_RISK_LEVEL.md`); "What you
                   relay" ("no risk level, no TaskCreate")
    Aujourd'hui  : A file and two concepts nothing in this chain defines;
                   CLAUDE.md names `CURRENT_TECHNICAL_STATE.md` only.
    Le défaut    : Plane 3, criteria 1 and 3 — rules against a case from
                   another project; they read well and guard nothing here.
    Ce qu'il faut: Only the reading rules this project's CLAUDE.md states.
    Justification: Tokens, small; and a reader who has seen nothing else
                   does not go looking for a file that does not exist.

### 21

    Fichier      : .claude/commands/cycle.md
    Cible        : The chain list; rows 6a, 6b, 7 (`/2_grille`); row 12
                   (`/3_reclasse`); row 7 (`a sondeur-*`); row 4
    Aujourd'hui  : The grid phase is named `/2_grille` and the next
                   `/3_reclasse`; the commands are `/4_grille` and
                   `/5_reclasse`. Row 7 routes on a blocking file named
                   `sondeur-*`; the sondeur writes
                   `cadrage-produit/blocked_par-bloc.md`, `_par-question.md`,
                   `_par-nature.md`, `_global.md`. Row 4 does not say it has
                   to look inside `cadrage-produit/`.
    Le défaut    : Command question 1 — rows naming what cannot occur,
                   outcomes with no row. As written, the cycle cannot reach
                   the sondeur's command and does not name its blocking
                   files.
    Ce qu'il faut: Rows carry the commands as they are named, and the
                   sondeur's four blocking-file names and their folder — so
                   that a lifted sondeur block routes to `/4_grille` and an
                   empty one stops the chain. The rest of the cycle's
                   staleness (other commands' names; `/3_decoupe` and
                   `/3b_nature` absent from the chain, which is what
                   guarantees the Nature line comment 14 relies on) is
                   outside this pass — left for the group pass.
    Justification: Round trips — a `/cycle` run errors on an unknown command
                   or misroutes. Robustness — a sondeur blocking file with
                   an empty decision that row 4 does not look for lets the
                   chain carry on past an unanswered stop.

### 22

    Fichier      : .claude/agents/sondeur.md
    Cible        : "Where you work", the product-file row — "Whole, to its
                   last line"; and "Invocation 1 — Which blocks"
    Aujourd'hui  : Every invocation reads the product file whole. On a later
                   turn an angle probes only the blocks the prompt names,
                   and its own rule says a pass A question "stands on its
                   block alone" — the other blocks are read and, by rule,
                   not used.
    Le défaut    : Plane 2, Q2 — a file read whole where a section would do,
                   three times a turn. (Found while checking the verdict's
                   D6 estimate against the agent, after the sweep above;
                   it is the same defect as comment 2, on the other file.)
    Ce qu'il faut: The global invocation and a first-turn angle read the file
                   whole; a later-turn angle reads the blocks the prompt
                   names, located by their heading, and nothing else. The
                   "empty or short" stop (comment 4) applies to what was
                   read.
    Justification: Tokens — on a later turn, three opus invocations each read
                   N blocks to probe k of them; the saving grows with the
                   file and with the turn count. Robustness unchanged: the
                   agent already forbids using the other blocks.

---

## From the verdict

    Section 2 — the role holds; the three angles are an unproven cost.
    Already found above (Plane 1, last point), with the same conclusion:
    a measurement, not a file defect. The agent states the bet as design:
    "Four of you run at once … The union of what you raise is what the
    chain uses — not what you agree on." Nothing in the file records or
    counts what each angle finds, so the measurement has no instrument
    yet; the per-reading counts the command relays ("How many questions
    each reading raised, and how many the merge kept") are the closest
    thing, and they count questions, not unique finds.

    D2 / sweep row 7 — block identifiers assumed stable, nobody guarantees it.
    Already found above (closing section, third item), as the condition
    on an incremental record. The agent says nothing about stability; it
    writes `Block: B7` and the record's `## B12` as if a number were a
    name. Settled by redacteur.md and decoupeur.md, as the verdict says.

    D3, A2, P5, item 23 — a forgotten MODIFIED has no detector; a byte diff
    would catch it at no agent cost.
    Not found. My comment 13 is the mirror defect (a bare-word grep that
    matches too much), not this one (a marker that is missing). What the
    command says: "Later turns — two greps in desc-produit.md, and the
    union of what they return … a block an answer touched carries
    MODIFIED, and the second grep finds it" — the marker is the only
    selector, and its presence is trusted. What the agent says: "On a
    later turn it names a few — those marked NEW or MODIFIED" — it
    trusts the list. The verdict's fix lands in the command's "Which
    blocks" step: the command commits the feature folder before creating
    the worktree, so the previous turn's product file is a commit, and
    `git diff` on `desc-produit.md` between the two gives the changed
    blocks without a marker. I would take it: the union of the diff and
    the greps as the angles' list, robustness for one git command.

    D4, item 1 — the Découpeur's new blocks may carry no marker.
    Not found; it needs decoupeur.md, outside this pass. What the command
    says of `NEW`: "The blocks created last turn" — it assumes every
    created block carries it, whoever created it. The diff above would
    cover this case too, whatever decoupeur.md says.

    D6, item 19 — the global runs its own pass A on every block to build the
    record, never reconciled with the angles' pass A.
    Contradicted in part by the agent. The global does not run pass A:
    "1. The record — for every block, in the product file's order, the
    answers pass B crosses: A1.1, A1.2, A1.3, A1.4, A1.9, and A4's list
    of names" and "You record, you do not question — pass A's gaps are
    the angles' work." Six identifiers per block, extracted, not the
    grid's pass A asked. The overlap is therefore narrower than the
    verdict prices — I noted it at Plane 1 (moves 5 and 6). Item 19's
    answer: it re-extracts from the blocks and does not reuse the angles'
    output — "Not … another sondeur's output"; the contradiction the
    verdict feared is not in the file. The token estimate ("the largest
    single reading of the upstream") is also off: every angle reads the
    product file whole as well (comment 22); the global's extra cost is
    the record's output, not its reading.

    D7, item 11 — cadrage-produit/closed/ created, nothing fills or reads it.
    Contradicted by the command. `4_grille.md`, "Git, in this mode": "And
    the previous turn's six cadrage-produit/ files: git mv
    docs/features/<name>/cadrage-produit/par-bloc.md
    docs/features/<name>/cadrage-produit/closed/par-bloc-NN.md — The same
    for par-question.md, par-nature.md, global.md, releve.md and
    questions.md." It is an archive the command fills every turn, read
    by nothing — the same status as `questions/<agent>/` (sweep row 41).
    The agent never names it, correctly. What is wrong there is comment
    18: the `NN` of those six files has no rule.

    Sweep row 9 — the `Clarification needed` stop is wired.
    Already found above, comment 3, with a nuance the sweep does not
    carry: it is wired twice, and the agent's copy can never fire.

    Sweep row 15 — grid identifiers never on a question to the person, by design.
    Already found above, comment 9, which disputes the design on one
    point: the identifier is absent from the question text and from any
    field, while the merge across four readings is where comparability
    is needed. The agent's own words for the record — "it is what makes
    one block's answers comparable to another's" — are the argument.

    Sweep rows 17 and 22 — releve.md read by the global alone; `Block: -`
    for a feature-level question, by design.
    Already found above (Plane 1) for the record; nothing to add on
    `Block: -` — the agent says exactly that: "Block: - for a pass C
    question: it was asked of the feature, and nothing in it says where
    its answer lands."

    A1, item 7 — a confirm-as-is answer leaves no text; the no-memory
    Sondeur asks again when a neighbour marks the block.
    Not found; it rests on redacteur.md. What the agent says supports the
    mechanism exactly: "Not … a previous turn's questions" and "Settled
    means the answer is there, in the terms the question asks for … If
    you have to interpret to find it, it is not there." A block re-marked
    MODIFIED whose earlier gap left no sentence is probed as a fresh gap.
    I would not change the agent for it — its no-memory rule is what
    keeps four readings independent (P9); the trace belongs in the block,
    by the Rédacteur.

    U5 — the grid turn's stop is "nothing changed", not "nothing is open";
    passes B and C do not run when no block moved; no bound; B and C
    re-run over every block each turn.
    Not found for the stop test. What the command says: "Neither grep
    returns anything, on a later turn → invoke nothing. Nothing moved
    since a turn whose questions are answered — write
    questions-sondeur-NN.md empty." The sentence asserts what it does
    not test; with item 7 unsettled, the assertion can be false. Settled
    by redacteur.md; if a confirm-as-is answer leaves no text, the cheap
    fix is on the command — run the global invocation even when no block
    moved, or never declare closure without one global run on the final
    text. The bound: seen and left (the person steps in every turn; a
    turn counter in the relay would be the only addition). The re-run of
    B and C over every block: already found above (closing section,
    third item — the incremental record).

    U9 — a Sondeur block is bounded at one round.
    Already found; comment 17 adds what the round costs today — three
    readings redone for one block.

    P9 — the Sondeurs never read each other; keep it.
    Agreed; the agent: "Not … another sondeur's output" and, under what
    it never does, "Read another sondeur's output". No comment.

    P13 — the global records every block every turn; the failure mode of a
    context that runs out is silent truncation, not a block.
    Not found. What the agent says: "Every block, whatever changed" — no
    size test, no stop; the only size-related rule ("A file that comes
    back empty or short", comment 4) is about the read, not about the
    agent's own capacity to write N×6 rows and then cross them. The
    known list names it: "More context than one agent holds — it
    degrades instead of stopping." I would conclude: the command knows
    the block count by grep before invoking; above a ceiling the group
    pass sets from the sizes seen, the record is written per group of
    blocks by separate invocations and pass B runs on the records alone
    — the agent already says pass B reads "from the record alone —
    never the blocks again", so the split costs no new rule in the
    agent, only a prompt that names a group and a record file.

    Item 10 — is text outside blocks probed by any Sondeur?
    Not found. The agent names no text outside blocks. Pass A is "to a
    block", pass B "a column of the record", pass C "once, on the
    feature"; the product file is read "Whole, to its last line", so
    pass C has the preamble in front of it, but nothing tells it to
    take the grid's pass C questions to that text rather than to the
    blocks' sum. If the Rédacteur writes outside blocks (redacteur.md),
    pass C is the only candidate and should be told so; if it does not,
    nothing is missing here.

---

## What another agent would settle

    Does the assembleur merge by identifier or by wording? (comments 9, 19)
    assembleur.md
    By (block, grid question): the sondeur must carry the identifier in a
    field, comment 9 is a requirement. By wording: comment 9 is a proposal
    that changes both agents, for the group pass to weigh. And for 19: if
    the assembleur already numbers from Q1 and something needs its
    `## Merge` section, the fix moves to the assembleur, not the command.

    What is the marker's exact shape, and does it sit on the block heading?
    (comment 13)
    redacteur.md
    On the heading, in a fixed form: the command's grep is one line and
    the identifier comes with the hit. Elsewhere: the Rédacteur's file is
    where the fix belongs, and the command derives the identifier by a
    second step.

    Are block identifiers stable across turns — does a split renumber?
    decoupeur.md, redacteur.md
    Bears on the global's record, which today recomputes six rows for
    every block every turn while only the changed blocks' rows can
    differ (known list — work done twice). Stable identifiers and every
    changed block marked MODIFIED: the global could read the previous
    `releve.md`, recompute the marked blocks' rows, and cross — output
    tokens saved on every later turn, at the cost of one read of a file
    shorter than the product file. Renumbering on split: the record has
    to be rebuilt and today's rule stands.

    What does a filled Nature line look like? (comment 14)
    classeur.md
    Settles the grep; the comment stands either way.

    Is `[integrated:` what the Rédacteur writes into an answered file?
    (comment 11)
    redacteur.md
    The cycle command uses it as a state test, so I took it as given; if
    the Rédacteur marks differently, comment 11's grep follows the mark,
    the comment stands.

    What does the Rédacteur write when an answer confirms a block as it
    stands, and does it write product text outside blocks? (verdict A1,
    U5, item 10)
    redacteur.md
    A trace in the block: the agent's no-memory rule is safe and the
    command's "nothing moved → closed" holds. No trace: the fix is on the
    command (one global run before closure), not on the agent. Text
    outside blocks: pass C must be told to cover it; none: nothing to do.

    Not an agent file — the grid, which this pass forbids opening:
    is it sectioned by pass (comment 2 stands or falls on it); does it
    name the record's columns (comment 6 says which owner); does it scope
    questions by nature (comment 7's second test exists or not).
