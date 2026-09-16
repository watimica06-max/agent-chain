# classeur — examination

**Read**: `.claude/agents/classeur.md` in full; `.claude/commands/3b_nature.md`
in full (the only command that invokes the agent). `.claude/commands/5_reclasse.md`
names the classeur but invokes nothing — it was read only as the consumer of the
`Nature:` line, and is cited where the exact form of that line matters.

**Role, from the file**: fills the empty `Nature:` line of every block the prompt
names, re-derives the nature of every `MODIFIED` block the prompt names, and writes
a questions file whenever a block's nature is in doubt.

**Moves, in order** (Part 3 and the sections it points to):

| # | Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|---|
| 1 | Read the named block, ask what it produces | Without it the nature is a guess from the trigger | Move 2 | — |
| 2 | Take the nature that produces it, from the table of eight and the frontier table | The only mapping from output to nature | Move 3 | — |
| 3 | Write it on the block's `Nature:` line | The line the grid, `/5_reclasse` and the Convertisseur read | product file | — |
| 4 | On doubt, an entry in the questions file; move 3 stands | Doubt otherwise settled in silence | `questions-classeur-NN.md` → Product Owner → `/1_lexique` | Restates *Your questions* (same three doubts, consistent) |
| 5 | `MODIFIED` block with a filled line: re-derive, compare, overwrite if different | A changed block may have changed nature; the grid would probe it on stale questions | product file; report | Moves 1–3 on a filled line |
| 6 | Write the questions file, even empty | The command reads its presence as "the agent ran" | command's after-check | — |
| 7 | Block (`blocked_classeur.md`) when no nature fits; resume from a filled `## Decision` | The only exit when the eight do not cover a block | Product Owner; next run | — |
| 8 | Report: counts, per-block nature, blocks asked about and why | The orchestrator relays | command's *What you relay* | Per-block list and "asked about" lines repeat the file and the questions file |

**The set**: the moves cover the role and the order holds (knowledge before process,
write before doubt so a doubt never leaves the line empty). Move 5 cannot go — without
it a changed block keeps a stale nature and the grid closes it clean on the wrong
questions. Two parts of move 8 are paid for nothing as the command stands (comments
10 and 11). What move 4 produces for two of its three doubts has no path back into
the `Nature:` line (comment 6). Move 7 does not say whether the run continues on the
other blocks (comment 7).

---

## Comments, in the order they apply

### 1

    Fichier      : .claude/agents/classeur.md
    Cible        : Part 3, step 1 — the enumeration "a value, a record, a display,
                   a state change, a reconciliation, a permission"
    Aujourd'hui  : six kinds of output, for eight natures. "record" has to stand for
                   both `model` and `persistence`; "permission" for both `access` and
                   the OS-permission case of `external exchange`; nothing stands for
                   data crossing to another system.
    Le défaut    : Plane 2, question 4 — a count that no longer matches what follows
                   it. Plane 2, question 1 — the step's own test (the six) is narrower
                   than the table it points to.
    Ce qu'il faut: step 1 must either name one output per nature, in the words of the
                   table's "It produces" column, or name none and send the reader to
                   the table. Two lists that do not map one-to-one make the agent pick
                   the nearest of six before it looks at the eight.
    Justification: robustness — a block whose output is "data sent to a server" is
                   nearest to none of the six, and lands on `persistence` or
                   `presentation` by proximity; the grid then closes it on the wrong
                   questions, which the agent's own Role section says is not caught.

### 2

    Fichier      : .claude/agents/classeur.md
    Cible        : The eight natures — the `presentation` row, "and what each of their
                   actions does"; and the frontier table, which has no
                   `presentation · transition` row
    Aujourd'hui  : `presentation` is "what the user is shown or told, by any channel,
                   and what each of their actions does". The lead rule says a nature
                   is "what it produces, never what fires it".
    Le défaut    : Plane 3, criterion 4 — two readings. "The user taps Save and the
                   session is recorded" is `presentation` under "what each of their
                   actions does" and `transition`/`persistence` under "what it
                   produces, never what fires it". The frontier table settles
                   `calculation · transition` and says a view's state is
                   `presentation`, but never the pair a user action sits on.
    Ce qu'il faut: the `presentation` row must be bounded to what the user perceives —
                   what is shown, told, and the visible response to an action — and
                   the frontier table must carry the pair `presentation · transition`
                   (or `presentation · <any>`): a user action is a trigger; the block
                   takes the nature of what the action produces, and only the part
                   the user sees is `presentation`.
    Justification: robustness — most blocks of an app are fired by a user action;
                   this frontier is the one the agent meets most often and the one
                   the tables leave to its own reading. Round trips — a doubt raised
                   on every such block (the agent is told to ask "at the least
                   doubt") is a question the Product Owner answers block by block.

### 3

    Fichier      : .claude/agents/classeur.md
    Cible        : The eight natures — the `external exchange` row, "a permission the
                   system grants"
    Aujourd'hui  : the nature row says "the system"; the `access · external exchange`
                   frontier row says "the operating system".
    Le défaut    : Plane 3, criterion 4 — "the system" reads as the application as
                   readily as the OS; read that way, the row swallows `access`.
    Ce qu'il faut: the two rows must use the same words for the same thing — the
                   permission that is `external exchange` is the one granted by the
                   platform the application runs on, not by the application.
    Justification: robustness — an `access` block classed `external exchange` goes to
                   the wrong section of the technical document and the wrong layer of
                   the code.

### 4

    Fichier      : .claude/agents/classeur.md
    Cible        : Part 3, step 3, and *Where you work* ("load those, and no others")
    Aujourd'hui  : the agent is told to load the named blocks and to write "on the
                   block's `Nature:` line". Nothing says where a block starts and
                   ends, where its `Nature:` line sits, where a marker sits, or what
                   the written line looks like once filled.
    Le défaut    : Plane 2, question 4 — a placeholder with no rule for what fills it.
                   The agent invents the form: `Nature: Model`, `Nature: external-
                   exchange`, `Nature: presentation (view state)` are all reasonable
                   guesses. `/5_reclasse` stops on any value that is not exactly one
                   of the eight, and `/3b_nature` greps `^Nature:$` to find the empty
                   ones — so the form is load-bearing on both sides. "Load those, and
                   no others" is not executable without the block's extent: a grep on
                   `B7` also hits `B70`.
    Ce qu'il faut: the agent must be told (a) how a block is delimited — its `### B`
                   heading to the next heading of any level, marker trailing on the
                   heading line, `Nature:` line directly under it; (b) the exact form
                   of the filled line — `Nature: ` followed by the nature's name
                   spelled as in the table, lower case, nothing else on the line;
                   (c) how to find a block by identifier without hitting a longer one.
    Justification: round trips — a value spelled differently from the table stops
                   `/5_reclasse` two commands later, and the fix is a rerun of
                   `/3b_nature` on a block the agent had already classed correctly.
                   Tokens — a wrong delimitation loads neighbouring blocks the prompt
                   did not name.

### 5

    Fichier      : .claude/agents/classeur.md
    Cible        : *Your questions* — "Your number: the highest at the root, or in
                   `questions/classeur/` if the root holds none, plus one"
    Aujourd'hui  : two gaps. "The highest at the root" does not say the highest
                   *classeur* number — the root may hold another agent's file with a
                   higher number. And when neither the root nor the folder holds one,
                   there is nothing to add one to.
    Le défaut    : Plane 2, question 3 — the first run is a situation the move does
                   not foresee. Plane 3, criterion 4 — "the highest at the root"
                   reads two ways.
    Ce qu'il faut: the number is the highest `questions-classeur-NN` wherever it is
                   found, plus one; none anywhere means `01`. (The command files every
                   root questions file before invoking, so the root case is moot in
                   practice — the rule should still hold on its own.)
    Justification: round trips — a number that collides with one already in
                   `questions/classeur/` makes the next command's `git mv` fail or
                   overwrite a filed, answered file. Robustness — an overwritten
                   answered file is a Product Owner decision lost.

### 6

    Fichier      : .claude/agents/classeur.md
    Cible        : *Your questions* — doubts 2 and 3 ("Which nature it takes", "Which
                   side it falls on"), against *Where you work* ("the product file the
                   prompt names, and nothing else") and *What you never do* ("Fill a
                   `Nature:` line that already carries one, unless the block is marked
                   `MODIFIED`")
    Aujourd'hui  : the agent writes the nature it would give, asks, and the Product
                   Owner answers "persistence". The agent never reads an answered
                   questions file. The line is filled, so the agent may not touch it
                   again unless the block is `MODIFIED`. If the Rédacteur integrates
                   the answer by rewriting the text so that it no longer reads two
                   ways, the block comes back `MODIFIED` and move 5 re-derives —
                   fine. If the Rédacteur leaves the text as it was (an answer that
                   only names a nature gives it nothing to rewrite), the answer has
                   no path into the line: the block keeps the nature the agent
                   guessed, and no one is told.
    Le défaut    : Plane 2, question 3 — the answer to two of the three doubts has no
                   foreseen way of landing. Known list — a loop with no ceiling: if
                   the block does come back `MODIFIED` with the same text, the agent
                   meets the same doubt and asks the same question again.
    Ce qu'il faut: one of two things must hold. Either the answer to a nature
                   question is handed to the classeur — the prompt names the answered
                   file, and the agent applies the answer to the block it names,
                   before re-deriving — or the rule is that every answer to a
                   classeur question ends in a text change the agent can read from
                   the block alone, and the questions file's shape asks the Product
                   Owner for that. The agent must also know that a block it already
                   asked about, still reading two ways, is not asked about again —
                   it takes the nature the earlier answer gave, or blocks.
                   Which half the Rédacteur already covers is for the group pass —
                   see the last section.
    Justification: robustness — a nature the Product Owner settled and the file
                   never took is exactly the wrong-nature-closed-clean case the Role
                   section warns about. Round trips — the same question asked on
                   two turns is a decision asked twice of the person.

### 7

    Fichier      : .claude/agents/classeur.md
    Cible        : *When you cannot produce* — what the run does with the blocks that
                   did not block
    Aujourd'hui  : the blocking file's shape holds one block (`## Where — <the
                   block>`). Nothing says whether the agent stops at the first block
                   it cannot class or finishes the others; whether it writes its
                   questions file in that case; or what it writes when two blocks
                   block. The command relies on all three: it greps `^Nature:$`
                   expecting zero, stops if the questions file is missing, and has
                   one row for "it wrote a blocking file".
    Le défaut    : Plane 2, question 3 — the situation is foreseen (a blocking file)
                   but not the state the rest of the run is left in.
    Ce qu'il faut: the agent must finish every other named block, write its
                   questions file, and leave only the blocked block's line empty;
                   several blocked blocks go in one blocking file, one `## Where`
                   entry each, or the shape must say why one at a time. The report
                   names the blocked block(s) alongside the counts.
    Justification: round trips — stopping at the first block turns three unclassable
                   blocks into three Product Owner turns and three invocations.
                   Robustness — an agent that stops half-way and does not say so
                   leaves lines empty that the command reads as "left unclassed",
                   with no way to tell them from a blocked one.

### 8

    Fichier      : .claude/agents/classeur.md
    Cible        : *When you cannot produce* — "A blocking file the prompt names
                   carries a filled `## Decision` — it says what was settled, and you
                   resume with it"
    Aujourd'hui  : "resume with it" is the whole rule. The agent blocks for two
                   reasons — the block produces nothing, or the eight miss a nature.
                   The first reason's decision is a rewrite the Rédacteur must do; the
                   second's is a ninth nature, which exists in no table the agent
                   holds and which `/5_reclasse` refuses. In both cases the agent
                   cannot apply the decision and has no rule for that.
    Le défaut    : Plane 2, question 3 — a decision the agent cannot act on is not
                   foreseen; it will either write the ninth value, or leave the line
                   empty with nothing to say why.
    Ce qu'il faut: the agent must know the three shapes a decision can take and what
                   each means for the line: a nature among the eight — write it; a
                   block to be rewritten or removed — leave the line empty, say in the
                   report that the block awaits the Rédacteur; a nature outside the
                   eight — it cannot be written until the tables carry it, say so and
                   leave the line empty. The command's outcome table then has to
                   carry the second and third (comment 13).
    Justification: robustness — a ninth value written into the file passes
                   `/3b_nature`'s zero-check and stops `/5_reclasse` two commands
                   later, or, if the Convertisseur is reached, lands in no section.
                   Round trips — the Product Owner is sent back to `/3b_nature` on a
                   decision that command cannot apply.

### 9

    Fichier      : .claude/agents/classeur.md
    Cible        : *What you never do* — last entry, "Write anywhere but the product
                   file and your questions file"
    Aujourd'hui  : the entry forbids a third file; *When you cannot produce* orders a
                   third file, `blocked_classeur.md`, and warns that "a message in a
                   reply gets lost; a file does not".
    Le défaut    : Known list — a forbidden thing that the body asks for. Two
                   passages of one agent asking for different things.
    Ce qu'il faut: the entry must except the blocking file, or name the three files
                   the agent may write.
    Justification: robustness — an agent that obeys the forbidden list does exactly
                   what the blocking section warns against: it says it in the reply,
                   and the command's "does `blocked_classeur.md` sit in the feature
                   folder" finds nothing next run.

### 10

    Fichier      : .claude/agents/classeur.md
    Cible        : Part 3, *What you write* — "Say which blocks you asked about, and
                   why, in one line each"
    Aujourd'hui  : the report restates every entry of the questions file. The command
                   relays "how many questions" and nothing of their content; the
                   Product Owner reads the questions file to answer it.
    Le défaut    : Plane 1 — a move whose result nothing carries forward.
    Ce qu'il faut: the report carries the count and the file's name; the file carries
                   the questions.
    Justification: tokens — every question is written twice and read once.

### 11

    Fichier      : .claude/commands/3b_nature.md
    Cible        : *What you relay* ("how many blocks were classed, which changed
                   nature, and how many questions") and *Once it has reported*
                   ("Never read a block to check its work. The sondeurs probe what it
                   classed; that is what catches a wrong nature")
    Aujourd'hui  : the agent reports "per block, the nature you gave it — one line
                   each, so the Product Owner can read the classification without
                   opening the file". The command relays counts only; the per-block
                   list stops at the orchestrator. The command justifies this with
                   "the sondeurs catch a wrong nature"; the agent's Role section says
                   the opposite — "A wrong nature is not caught later. The grid closes
                   the block on the wrong questions, and the closure reads as clean."
    Le défaut    : Known list — two passages asking for different things, here across
                   the agent and its command. Plane 1 — the agent's per-block report
                   is produced and dropped. Command question 2 — a thing the agent
                   produces that the command's relay does not use.
    Ce qu'il faut: the two must agree on who catches a wrong nature. By the agent's
                   own account no one downstream does — so the per-block list must
                   reach the Product Owner: the command relays it (one line per block,
                   as the agent already produces it), and the "sondeurs catch it"
                   sentence goes unless the sondeur's file backs it. If the sondeur
                   does catch it, the agent's report line goes instead and the Role
                   section's warning is softened. Which is true is for the group pass
                   — see the last section.
    Justification: robustness — the classification is the only place the Product
                   Owner can see a wrong nature before the grid closes on it; a list
                   produced and not relayed gives that chance to no one. Tokens, if
                   the other way — a per-block report no one reads.

### 12

    Fichier      : .claude/commands/3b_nature.md
    Cible        : *Once it has reported* — "Check `questions-classeur-NN.md` was
                   written — a missing one stops the command", against *Git, in this
                   mode* — "Merge before handing back, always"
    Aujourd'hui  : the questions-file check sits in the section that runs before the
                   merge. A stop there leaves the worktree unmerged with every
                   `Nature:` line the agent wrote — and, per CLAUDE.md, a worktree
                   holding unmerged work never self-cleans.
    Le défaut    : Plane 2, question 3 on the command — the stop is foreseen, the
                   state it leaves is not. Plane 1, order — a stop before the rule
                   that says never to stop before merging.
    Ce qu'il faut: any stop after the agent has reported must first say what happens
                   to the worktree: merge what was written and report the missing
                   file as a defect, or discard the worktree explicitly. The section
                   on git should hold, in one place, that a post-report stop merges
                   first — as it already says for `blocked_*.md`.
    Justification: tokens — an invocation's whole output lost, and paid again on the
                   rerun. Round trips — a rerun for a file that was the only thing
                   missing.

### 13

    Fichier      : .claude/commands/3b_nature.md
    Cible        : *What to run next* — the three-row table
    Aujourd'hui  : rows for: a blocking file; a questions file with questions; an
                   empty one or nothing to class. No row for: (a) the `^Nature:$`
                   count is non-zero and no blocking file explains it — the check
                   above says "you say which" and nothing more; (b) a blocking file
                   and a questions file with questions on the same run — the agent
                   can produce both (comment 7), and the two rows send the Product
                   Owner to two different commands; (c) a blocking file whose
                   decision the classeur cannot apply (comment 8) — the row says
                   "then `/3b_nature` again", which is the one command that cannot
                   act on a rewrite or a ninth nature.
    Le défaut    : Command question 1 — cases with no row.
    Ce qu'il faut: a row per outcome the agent can produce after comments 7 and 8:
                   (a) an unexplained empty line is a defect of the run — the row
                   says to rerun `/3b_nature`, which will grep it up again; (b) a
                   blocking file and questions together — the decision comes first,
                   then the answers, then `/1_lexique`, since both end in the
                   Rédacteur's hands; (c) a decision that names a rewrite goes to
                   `/1_lexique`, not back to `/3b_nature`; a decision that names a
                   nature outside the eight goes nowhere until the tables are
                   changed, and the row says so.
    Justification: round trips — every case without a row is a turn the Product
                   Owner spends asking what to run, or a `/3b_nature` run that stops
                   on the same blocking file again.

### 14

    Fichier      : .claude/commands/3b_nature.md
    Cible        : *Once it has reported* — `git mv … blocked_classeur.md
                   blocked_classeur-NN.md`
    Aujourd'hui  : `NN` with no rule for what fills it; the questions file has one
                   (highest plus one), the blocking file has none.
    Le défaut    : Plane 2, question 4 — a placeholder with no rule.
    Ce qu'il faut: the same rule as the questions file — the highest
                   `blocked_classeur-NN` in the folder plus one, `01` if none.
    Justification: robustness — a guessed `NN` that collides overwrites an earlier
                   decision; the Product Owner's history of what was settled is lost.
                   Round trips, minor — the orchestrator is left to decide.

---

## What another agent would settle

    Does the Rédacteur, when it integrates an answered classeur questions file,
    change the block's text so that the nature is readable from the block alone,
    and does it mark the block MODIFIED even when only the nature was answered?
    .claude/agents/redacteur.md (and the /1_lexique, /2_structure commands that
    carry the answered file to it)
    If yes: comment 6 reduces to the "do not ask twice" rule — the answer reaches
    the classeur through move 5. If no: the answers to doubts 2 and 3 land nowhere,
    and the prompt of /3b_nature must name the answered file for the classeur to
    apply it.

    Does the sondeur, probing a block, check or question its nature — or does it
    take the nature as given and pick the grid's questions from it?
    .claude/agents/sondeur.md (and the grid it applies, which this pass does not
    read)
    If the sondeur can question a nature: the command's "the sondeurs catch a wrong
    nature" is right, the agent's Role section overstates, and the per-block report
    line can go (comment 11, second branch). If it takes the nature as given: the
    agent is right, the command's sentence is false, and the per-block list must be
    relayed (comment 11, first branch).

    Do the decoupeur and the Rédacteur write the `Nature:` line as a bare `Nature:`
    directly under the `### B` heading, with the marker trailing on the heading line?
    .claude/agents/decoupeur.md, .claude/agents/redacteur.md
    If yes: comment 4 only needs the agent told what they do, and the command's
    `grep -B1 '^Nature:$'` holds. If either writes it elsewhere or with a trailing
    space: the command's two greps miss blocks, and the classeur is never named on
    them — nothing signals it.

    Does the Convertisseur (or any reader of the technical document) act on
    "which blocks changed nature" beyond what the MODIFIED marker already carries?
    .claude/agents/convertisseur.md, .claude/commands/6_convertit.md
    If nothing does: the agent's "say in your report which blocks changed nature"
    and the command's relay of it are informational only, and stay for the Product
    Owner. If something does: that consumer needs it in a file, not in a report
    line that the relay may drop.

    Is a block's nature ever needed by the sondeurs at a finer grain than one per
    block — do they probe sentences?
    .claude/agents/sondeur.md
    If they probe sentences: "one nature per block" sends a two-output block to a
    split it may not need. If they probe blocks: the rule stands as written.

---

## From the verdict

Read after everything above: section 2's Classeur line, sections 4 to 7.

    §2 — "the role holds … the Découpeur must stop on a `Clarification
    needed` and the Classeur must not; keeping them apart is justified."
    Contradicted by the command. The agent file never mentions
    `Clarification needed`; `/3b_nature` does, and stops on it before
    invoking: "🔴 Grep `Clarification needed` in `desc-produit.md`. ⚠️ One
    hit and the command stops. 📌 Say which blocks carry one, and that
    `/2_structure` has to run first." So the Classeur does not run on a
    file carrying one any more than the Découpeur does. The argument the
    verdict gives for keeping the two roles apart is not the one the files
    support; whether another argument holds (the Découpeur's file, and
    what it would cost to carry the nature tables) is for the group pass.
    Not a comment here — the behaviour is sound either way.

    §4 sweep, row 5 / row 13 / row 14 — `desc-produit.md`, the Classeur's
    questions file, the eight natures: "wired".
    Partly already found above. The questions file is wired (the command
    checks its presence). The `Nature:` line is wired empty and not wired
    filled — comment 4: nothing on the agent's side fixes the form of the
    value `/5_reclasse` requires. The eight natures are "produced by the
    process": the agent's own text says a blocking file on a missing
    nature "is how the list learns", and no file or agent is named as the
    list's holder — comment 8.

    §4 sweep, row 7 and D2 — block identifiers assumed stable; the
    Classeur is among the six readers.
    Not found above, and the agent is not exposed: it receives identifiers
    in the prompt, grepped by the command minutes earlier, and uses them
    within that one run. Stability across turns is the Rédacteur's to
    settle; nothing the Classeur writes carries an identifier forward
    except `Block:` in its questions file, which the Rédacteur integrates
    next turn — the same exposure every questions file has.

    §4 sweep, row 8 — "`Nature:` line, written empty … wired".
    Already found above in part (comment 4). The verdict judged the empty
    line; the filled line's form is what no file states.

    §4 sweep, row 10, D3 and D4 — markers "trusted on one side"; the
    Découpeur's halves possibly unmarked.
    Not found above, and the agent confirms its dependence: Part 2 —
    "Never inferred from the folder — the orchestrator grepped, you do not
    grep again." The Classeur has no way to notice a changed block the
    command did not name; the command greps `MODIFIED`, and §7 item 23's
    list of commands that would gain from a byte diff (`/3_decoupe`,
    `/4_grille`) should include `/3b_nature`. On D4: the agent's path to a
    split block is the empty `Nature:` line, not the marker — so the
    halves are classed whether or not they carry one, as the verdict says.
    Chain-level; left to the group pass.

    §5 U4 — "The Classeur's question. In: a block whose two sentences
    produce two things. … Bound: none; each round is one block's split."
    Contradicted in scope by the agent. The verdict describes one of three
    doubts; the agent's *Your questions* table has three — "Two of its
    sentences produce two different things", "One output you could give
    either of two natures", "A frontier above that does not settle it" —
    and the route U4 draws (Rédacteur splits → Découpeur → Classeur)
    answers only the first. For the other two the answer names a nature,
    and nothing carries it into the line — comment 6. The stop the verdict
    gives ("questions file empty and `grep -c '^Nature:$'` zero") is right
    and is the command's.

    §5 U5 — the Classeur as a step of the grid turn.
    A listing, not a claim. Consistent with `/3b_nature`: "It runs between
    `/3_decoupe` and `/4_grille`, every turn."

    §6 P2 — eight natures partition everything; "a block whose two
    sentences produce two things must be split to fit the list".
    Already found as the agent's design, not as a defect: "One nature per
    block, always. A block two of whose sentences produce two different
    things was badly split — that is a question." Whether the sondeurs
    need one nature per block or could take one per sentence is in the
    last section.

    §7 — no item names the Classeur.
    Item 1 (does the Découpeur mark its halves) and item 23 (does any
    command diff the product file) touch its inputs, as above.
