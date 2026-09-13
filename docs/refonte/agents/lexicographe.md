# lexicographe — examination

**Role, from the file:** before the product file exists, sweep the idea
file's domain terms, raise every pair that could name one same thing
and every doubtful quote as questions, apply the Product Owner's
answers in the idea file and record them in `lexique.md`; afterwards,
on every answered questions file of the grid or of the conversion,
catch a word standing where a settled one would do and replace the
retired terms in the answers.

**Moves, in order** (agent file):

| # | Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|---|
| A | Where you work / what you read | Bounds the reads to the prompt's files | Every invocation | — |
| B | The two kinds of word | Displayed text vs concept — the one distinction the sweeps rest on | Sweep 3 (inv 1), the lexicon's entries | — |
| C | What you never do | Keeps term choice with the Product Owner; bounds writes | — | Restates "never open the product file" (also in A and Part 2) |
| D | When you cannot produce | The stop and its resume | The command's "Before anything else" | — |
| E | Invocation table, questions-file numbering, single lexicon, loops | Says which call this is and where its outputs go | Every invocation, the command's "Which invocation" | — |
| 1.0 | Read `## Tranché` from the second sweep on | Stops re-asking the settled | Sweep 2 | — |
| 1.1 | Domain-term inventory with counts | The base every pair is drawn from; what inv 3 compares against | Sweep 2, `lexique.md`, inv 3 | — |
| 1.2 | Pairs (two languages, two terms, one term two meanings) | The synonyms the Rédacteur would otherwise carry into every block | Questions file, `## Non tranché` | — |
| 1.3 | Quotes (displayed text without quotes, or the reverse) | A label the chain would otherwise translate | Questions file, `## Non tranché` | — |
| 1.w | Write `lexique.md` swept section and the questions file (always) | The record and the loop's driver | Inv 2, the command's counts | — |
| 2.1 | Read the questions file | — | 2.2 | — |
| 2.2 | Check answers against each other and `## Tranché`; replace retired terms everywhere; grep to confirm; send open answers back | The one write that settles the vocabulary in place | The idea file (Rédacteur), a new questions file | — |
| 2.3 | Write `lexique.md` (`## Tranché`, `## Non tranché`) | The memory the next sweep and inv 3/4 grep | Inv 1.0, inv 3, inv 4, the Rédacteur | — |
| 3.1 | Read `Answer:` fields and the lexicon; one sweep for a word standing where a settled one would do | The only guard once the product file exists | Questions file (always) | — |
| 4.1 | Read own questions file and the answered file | — | 4.2 | — |
| 4.2 | Replace retired terms (lexicon's and newly settled) in the answers; never touch `Question:`; send open answers back | Keeps the answers the Rédacteur integrates on the settled vocabulary | The answered file (Rédacteur) | Overlaps 3.1 in what it reads — see comment 9 |
| 4.3 | Add settled terms to `lexique.md` | Same as 2.3 | Next turn's 3 and 4 | — |

**Judgement of the set.** Every move feeds something. Two things are
wrong at the set level: the lexicon's shape is stated in invocation 2
but first written by invocation 1 (order, comment 1); and invocation 4,
when invocation 3 asked nothing, is a second load of the same two
files for a grep-replace that 3 already had everything for (comment
9). One job falls between moves: the answer to a quote question has no
application move (comment 4); one enumerated class is not covered by
the readings offered (comment 3).

---

## Comments

### 1

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 1, "What you write"; Invocation 2, move 3
                   "What lexique.md holds"; Invocation 3, the paragraph
                   "lexique.md holds every term the sweeps found"
    Aujourd'hui  : Invocation 1 writes "lexique.md, its swept section:
                   the three lists" and "a swept term sits under
                   ## Non tranché". The only shape of the file is the
                   example under invocation 2, whose ## Non tranché shows
                   a pair with counts and a doubtful quote — not the
                   sweep-1 inventory. "Nothing else empties that
                   section" but an answer. Invocation 3 relies on the
                   file holding "every term the sweeps found". From the
                   second sweep on, nothing says whether ## Non tranché
                   is rebuilt from the current idea file or appended to.
    Le défaut    : Plane 1, order — the shape is stated in the move that
                   runs second. Plane 2, question 4 — "the three lists"
                   and the example read two ways: a reader matching the
                   example writes only pairs and quotes, and invocation 3
                   then compares an answer's word against pairs alone,
                   never against a term that had no rival; a reader
                   writing the inventory under ## Non tranché leaves a
                   section that no answer ever empties, and the count
                   the command relays as "what is not settled" is the
                   size of the inventory.
    Ce qu'il faut: The lexicon has a named place for the inventory —
                   every domain term with its count — distinct from the
                   place for what awaits an answer; invocation 3 compares
                   against both; a second sweep rebuilds the inventory
                   from the current idea file and keeps ## Tranché
                   untouched; the file's shape is stated once, where it
                   is first written or in Part 2, before either
                   invocation uses it.
    Justification: Robustness — invocation 3's catch exists only if the
                   inventory is in the file it greps. Round trips — the
                   "not settled" count is what the Product Owner reads to
                   know whether the vocabulary is closed.

### 2

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 2, moves 1 and 3
    Aujourd'hui  : Move 1: "Read the questions file, and it alone beside
                   the idea file." Move 2 checks the answers "against
                   ## Tranché". Move 3: "Write lexique.md". The inputs
                   table names three files, including lexique.md.
    Le défaut    : Plane 2, question 2, and "two passages asking for
                   different things" — a reader obeying move 1 never
                   opens the lexicon, cannot check against ## Tranché,
                   and at move 3 writes lexique.md from the answers
                   alone: earlier ## Tranché entries and the inventory
                   are gone. The next sweep asks them again; invocation
                   4 no longer greps their retired terms.
    Ce qu'il faut: Move 1 reads the lexicon with the questions file and
                   the idea file. Move 3 updates the lexicon — moves the
                   answered terms out of the unsettled place into
                   ## Tranché and keeps everything else — rather than
                   writing it.
    Justification: Robustness — a rewritten lexicon loses the settled
                   terms, and the agent's own rule says what is absent
                   from it is invisible to every later turn.

### 3

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 1, sweep 2 and "You propose a reading";
                   Invocation 2, move 2
    Aujourd'hui  : Sweep 2 enumerates three kinds of pair, the third
                   being "one term carrying two meanings". The readings
                   offered are three, all for two terms: same thing, two
                   distinct things, one the other's abbreviation. Move 2
                   of invocation 2 replaces "the terms the answer
                   retires, everywhere they appear" and greps for zero
                   left.
    Le défaut    : Plane 2, question 1 — the enumerated class is not
                   covered by the readings, so the question for it has
                   no stated shape. Question 3 — when the answer gives a
                   second name to one of the two meanings, the agent has
                   to decide which occurrences carry it: it either
                   guesses the scope of a term, which is the choice the
                   Product Owner owns, or replaces everywhere and merges
                   the two meanings again.
    Ce qu'il faut: For that kind, the question quotes every occurrence
                   of the term, each identifiable, so that the answer can
                   say which ones carry the second meaning; a fourth
                   reading exists for it; invocation 2 replaces only the
                   occurrences the answer names, and the grep check
                   expects the term to remain elsewhere.
    Justification: Robustness — the agent otherwise settles the scope of
                   a term by itself, silently, in the one place the chain
                   inherits from.

### 4

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 1, sweep 3; Invocation 2, move 2
    Aujourd'hui  : Sweep 3 raises "a term that reads like a displayed
                   text and carries no quotes — or the reverse". The
                   questions file carries it. Invocation 2 describes one
                   application: replace retired terms; "nothing else
                   changes"; "you swap a word, you do not rewrite". The
                   lexicon example records the case ("Réf." without
                   quotes in two sentences; "Démarrer" — displayed text,
                   with the concept beside it).
    Le défaut    : Plane 2, questions 1 and 3 — the answer to a quote
                   question has no application move. Adding or removing
                   quotes is not a word swap, and "nothing else changes"
                   forbids it. One reader adds the quotes in the idea
                   file, another records the answer in the lexicon and
                   leaves the idea file as it was.
    Ce qu'il faut: Invocation 2 states that an answer settling a quote
                   adds or removes the quotes at every occurrence in the
                   idea file, that this is the one change allowed beyond
                   a term swap, and that the ## Tranché entry carries
                   the text with its quotes and language — with the
                   concept beside it only when the answer named one.
    Justification: Robustness — a label left unquoted is a concept for
                   everything downstream, gets written in English, and
                   the text the Product Owner wanted on the screen never
                   reaches it.

### 5

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 2, move 2 (replace everywhere, grep for
                   none left); Invocation 4, move 2 (same)
    Aujourd'hui  : "Replace the terms the answer retires, everywhere they
                   appear. Then grep each retired term: none expected,
                   save where the answer keeps it. One left is an answer
                   half applied — replace it before you go on." Part 1:
                   a displayed text "stays as written, everywhere"; never
                   "translate a displayed text".
    Le défaut    : Plane 2, question 1, and "two passages asking for
                   different things" — a retired concept word that also
                   sits inside a quoted label is found by the grep, read
                   as half applied, and replaced inside the label.
    Ce qu'il faut: A retired term between quotes is not replaced and
                   does not count as left over; the grep check expects
                   none outside quotes. Same rule at invocation 4 on the
                   answers.
    Justification: Robustness — a displayed text corrupted by the one
                   agent whose rule is to never touch it.

### 6

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 3, the one sweep; Invocation 4, move 2
    Aujourd'hui  : Invocation 3 runs "one sweep, on those answers: a term
                   naming what the vocabulary already names". Sweep 3 of
                   invocation 1 (a displayed text without quotes, or the
                   reverse) is not run on answers. The agent itself says
                   "the grid asks every block for its exact wording".
    Le défaut    : Plane 2, question 1 — the move reaches less than
                   invocation 1 exactly where displayed texts arrive: the
                   answers to the grid are where the Product Owner writes
                   a label, and she writes it quoted or not. Unquoted, it
                   reaches the Rédacteur as a concept.
    Ce qu'il faut: Invocation 3 also runs the quote sweep on the answers'
                   words; invocation 4 applies a quote answer in the
                   answered file the way comment 4 has invocation 2 apply
                   it in the idea file.
    Justification: Robustness — the same gap as comment 4, on the turns
                   that produce most of the displayed texts.

### 7

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 3, "A term naming something new is not a
                   question"; Invocation 4, move 3
    Aujourd'hui  : The lexicon holds "every term the sweeps found and
                   every one an answer settled". Invocation 4 adds
                   settled terms only. Invocation 1 no longer runs once
                   the product file exists.
    Le défaut    : Plane 2, question 2 — the base invocation 3 compares
                   against freezes at the idea file's terms. A term an
                   answer introduces on one turn is in no list; a
                   synonym of it in a later turn's answer is compared
                   against nothing and passes — the case the agent calls
                   "the one that costs".
    Ce qu'il faut: The new domain terms an answer brings — data, event,
                   state, entity, view — are added to the lexicon's
                   inventory by invocation 3 or 4, still without a
                   question, so that every later turn compares against
                   them.
    Justification: Robustness — a second name for one thing entering the
                   product file from the second grid turn on, with no
                   move that can see it.

### 8

    Fichier      : .claude/agents/lexicographe.md
    Cible        : Invocation 3, "You read the Answer: fields, and them
                   alone — not the questions"
    Aujourd'hui  : As quoted. The answered file is opened whole to reach
                   its Answer: fields.
    Le défaut    : Plane 2, question 2 — an answer is a reply. "Oui,
                   celui-là", "le premier", "comme avant" designate
                   through the question they answer; read alone, the
                   agent cannot tell what a word in them names, and the
                   sweep's test — does this word mean something the
                   lexicon names — cannot be run.
    Ce qu'il faut: The Question: line is context for reading its own
                   answer; the sweep still runs on the answers' words
                   only, and the questions are still never edited.
    Justification: Robustness — the sweep can be run on every answer.
                   Tokens unchanged: the file is read whole either way.

### 9

    Fichier      : .claude/agents/lexicographe.md, and
                   .claude/commands/1_lexique.md ("What you relay", row
                   "3 ran")
    Cible        : The split between invocations 3 and 4; "What you
                   never do", last entry; the command's relay row
    Aujourd'hui  : Invocation 3 reads the answered file and the lexicon
                   and writes only a questions file. Invocation 4 always
                   runs — "when invocation 3 asked nothing, your
                   questions file is empty, and you still run" — and in
                   that case does one thing: grep the lexicon's retired
                   terms in the answers and replace them, "a retired term
                   found is not a question — the decision is made". The
                   command: "3 ran → answer its questions if it asked
                   any, then /1_lexique again — 4 replaces the retired
                   terms the answers carry, questions or not".
    Le défaut    : "A split too fine" — when 3 asks nothing, the common
                   case once the vocabulary is settled, a second opus
                   invocation reloads the same two files for a
                   replacement that needs no answer, and the command runs
                   a full commit / worktree / merge / push cycle around
                   it. Plane 1 — a move that could go: nothing breaks if
                   3 does the replacement, since it is a grep of listed
                   terms and needs nothing 3 does not hold.
    Ce qu'il faut: Invocation 3 replaces the lexicon's retired terms in
                   the answers itself, then sweeps for new synonyms;
                   invocation 4 applies only the answers to 3's
                   questions, and runs only when 3 asked something. The
                   never-do write list allows the answered file's
                   Answer: fields at 3 and 4. The command's relay row
                   splits: "3 asked something → answer, then /1_lexique
                   again"; "3 asked nothing → /2_structure".
    Justification: Round trips — one command run fewer per grid or
                   conversion turn in the common case. Tokens — one opus
                   invocation fewer, on the same files. Robustness
                   unchanged: the same replacement, one turn earlier.

### 10

    Fichier      : .claude/agents/lexicographe.md
    Cible        : "When you cannot produce"; Invocations 1 and 3,
                   "Write the questions file even when empty"
    Aujourd'hui  : A blocked run writes blocked_lexicographe.md. Nothing
                   says whether it also writes the empty questions file
                   invocations 1 and 3 must write "even when empty", or
                   the lexicon. The command decides the invocation from
                   what the root holds.
    Le défaut    : Plane 2, question 3 — the resume path. A blocked
                   invocation 1 that also writes its empty questions file
                   leaves `questions-lexicographe` alone at the root;
                   once the decision is filled, the command runs
                   invocation 2 on an empty file, and the sweep never
                   runs. Two readers of "even when empty" would not do
                   the same thing.
    Ce qu'il faut: A blocked run writes the blocking file and nothing
                   else — no questions file, no lexicon — so that the
                   resume is the same invocation, on the same root.
    Justification: Robustness — the vocabulary reaching the Rédacteur
                   unswept, with no signal. Round trips — a resume that
                   lands on the wrong invocation.

### 11

    Fichier      : .claude/agents/lexicographe.md
    Cible        : "What you never do", last entry
    Aujourd'hui  : "Write anywhere but the idea file, the lexicon, your
                   questions file and — at invocation 4 — the answered
                   file's Answer: fields." The next section: "Write a
                   blocking file — do not merely say it."
    Le défaut    : "A rule in the body with no matching entry" — the
                   blocking file is a write the list forbids. Plane 3,
                   criterion 4. An agent holding to the list says the
                   block instead of writing it, and the command's
                   "Before anything else" check never sees it.
    Ce qu'il faut: The write list names the blocking file, and — after
                   comment 9 — the answered file's Answer: fields at 3
                   and 4.
    Justification: Robustness — a block that is said and not filed is a
                   run that stops with nothing for the next run to find.

### 12

    Fichier      : .claude/commands/1_lexique.md
    Cible        : "The invocation", the prompt template; "Before
                   anything else", row "Its ## Decision is filled"
    Aujourd'hui  : The prompt names the idea file always, the lexicon
                   when it exists, the invocation number, the answered
                   file at 3 and 4, and the folder. It never names the
                   lexicographe's own answered questions file, which
                   invocations 2 and 4 apply. "Name it in the prompt" is
                   required for a filled blocking file, and the template
                   has no slot for it. The agent reads "the files the
                   prompt names, and nothing else" and "The prompt says
                   which one. It is never inferred."
    Le défaut    : Command question 2 — a file the agent must have and
                   the prompt does not name (its own questions file at 2
                   and 4; the blocking file): the agent goes looking, at
                   the root or under questions/lexicographe/, where older
                   answered files of the same name pattern sit. A thing
                   the prompt names and no move uses: the idea file at 3
                   and 4, which the agent's own rule makes it read whole.
    Ce qu'il faut: At 2 and 4 the prompt names the questions-lexicographe
                   file to apply; the template carries the blocking file
                   when its decision is filled; the idea file is named at
                   1 and 2 only.
    Justification: Robustness — the agent applies the file it was meant
                   to, not one it found. Tokens — the whole idea file
                   read at every 3 and 4 for no move.

### 13

    Fichier      : .claude/commands/1_lexique.md
    Cible        : "Git, in this mode", first rule; "Which invocation",
                   row "Two files of other agents"
    Aujourd'hui  : "Before invoking, file every root questions-*.md this
                   invocation does not read." The invocation is decided
                   from what the root holds, and every row reads all of
                   it, except "two files of other agents → stop, a
                   filing failed; say which files".
    Le défaut    : "Two passages asking for different things" — read in
                   the git section's order, an orchestrator files one of
                   the two answered files under questions/<agent>/ and
                   runs invocation 3 on the other. The filed one holds
                   the Product Owner's answers, and no command integrates
                   a file from that folder: they are lost from the
                   product file.
    Ce qu'il faut: One passage. Either the command files nothing before
                   invoking and the stop row is the rule for that case,
                   or the git rule names the stop instead of a filing.
    Justification: Robustness — answered questions that never reach the
                   Rédacteur.

### 14

    Fichier      : .claude/commands/1_lexique.md
    Cible        : "Which invocation", row "questions-lexicographe alone
                   → 2"; the stop on desc-produit.md
    Aujourd'hui  : A questions-lexicographe file alone at the root is
                   invocation 2. Invocations 2 and 4 never write an empty
                   one; an empty one alone at the root can only be the
                   file invocation 1 wrote to end its loop. The relay
                   after an empty 1 is /2_structure, but a Product Owner
                   who runs /1_lexique again gets invocation 2 on an
                   empty file. The stop on desc-produit.md says nothing
                   about what to run instead.
    Le défaut    : "An invocation that produces nothing, in a case where
                   the agent has nothing to do." Plane 2, question 3 for
                   the command — the misrun is not foreseen.
    Ce qu'il faut: A questions-lexicographe file with no `### Q` alone at
                   the root is the ended loop: the command says so, says
                   /2_structure, and invokes nothing. The desc-produit.md
                   stop names the same next step.
    Justification: Tokens — one opus invocation, and the commit /
                   worktree / merge / push cycle around it. Round trips
                   — the Product Owner told where she is instead of run
                   in a circle.

### 15

    Fichier      : .claude/commands/1_lexique.md
    Cible        : "Once it has reported", "After every invocation —
                   check lexique.md exists, and grep its two counts"
    Aujourd'hui  : Count `retenu` for what is settled, the lines under
                   ## Non tranché for what is not. The lexicon's shape is
                   an example in the agent, not a rule; its displayed-text
                   entries carry no "retenu"; after comment 1 the
                   unsettled place holds the inventory too.
    Le défaut    : Plane 2, question 1 — a test two readers cannot run
                   the same way, on a shape nothing fixes; the count
                   undercounts the settled and overcounts the unsettled.
    Ce qu'il faut: Either the agent's lexicon shape is a rule — one fixed
                   marker per ## Tranché entry, one line per unsettled
                   pair — and the command counts that marker and those
                   lines; or the command checks that the file exists and
                   relays nothing about its counts.
    Justification: Robustness — the check is meant to catch a settled
                   term not written down, which the agent says is
                   invisible afterwards; a count nobody can trust catches
                   nothing.

### 16

    Fichier      : .claude/commands/1_lexique.md
    Cible        : "Which invocation", "After 2, run 1 again"; "What you
                   relay", row "2 wrote none"
    Aujourd'hui  : After invocation 2 the next is always invocation 1
                   again — "a settled term can uncover a pair the first
                   sweep could not see" — and the loop ends only when a
                   sweep writes an empty file.
    Le défaut    : Plane 2, question 1 — the reason given presupposes the
                   idea file changed. When every answer kept its terms
                   (two distinct things, two kept side by side), the
                   idea file is byte-identical; the agent's own rule
                   makes the sweep complete ("every term of sweep 1 is
                   compared"), so a re-sweep on the same text with a
                   larger ## Tranché can find nothing — it is run to
                   produce the empty file that ends the loop.
    Ce qu'il faut: After 2 wrote no new questions file, the next is
                   /2_structure when the merge shows the idea file
                   unchanged, and /1_lexique when it changed.
    Justification: Tokens — one opus sweep of the whole idea file.
                   Round trips — one command run. Unsure: a second sweep
                   also catches what the first missed; I decided the
                   agent's own "every term compared" rule makes that a
                   net, and left the re-sweep where the text changed.

### 17

    Fichier      : .claude/agents/lexicographe.md
    Cible        : "When you cannot produce"; Invocation 1, sweeps 1
                   and 2
    Aujourd'hui  : "Block only when you cannot produce — no idea file, an
                   empty one." Sweep 1 counts every term, "down to the
                   terms that appear once"; sweep 2 compares "every term
                   of sweep 1, the rare ones included". Nothing bounds
                   the idea file's size, and nothing says what the agent
                   does when one sweep cannot hold it.
    Le défaut    : Known list — "more context than one agent holds:
                   it degrades instead of stopping". Plane 2, question 3.
                   A count or a comparison the agent can no longer run
                   whole becomes a sample with no signal, and the rare
                   terms — where the agent says a synonym hides — are
                   the first to go.
    Ce qu'il faut: A stated ceiling on what one sweep covers, and above
                   it a block that names the size — or a sweep by
                   section with the cross-section comparison written
                   down; either way the agent says when its sweep is no
                   longer a sweep, rather than delivering a sample.
    Justification: Robustness — a partial sweep is the exact defect the
                   agent exists to remove, with no reader able to see
                   it. Unsure how often an idea file reaches that size;
                   the failure is silent, which is why it is worth a
                   rule.

---

## From the verdict

**Section 2 — "the role holds … costs round trips: its own loop before
the product file, plus two invocations on every answer file
thereafter."**
Already found above — comment 9 removes the second invocation in the
common case (3 asked nothing), comment 16 removes one turn of the loop
before the product file when the idea file did not change.

**Section 4, sweep row 1 — `idees.md`: producer Product Owner and
Lexicographe (settled terms); reader Lexicographe and Rédacteur inv. 1;
"never re-read after inv. 1 — D1".**
Not about a defect of this agent; the agent agrees with the row — it is
"the only agent that writes in the idea file", and nothing in it
re-reads the idea file after the product file exists ("3 and 4 run
after it, on answers alone"). D1 is the Rédacteur's boundary.

**Section 4, sweep row 2 — `questions-lexicographe-NN.md`, "new file
each time", wired.**
Confirmed by the agent ("Always a new file — never one that already
exists"). Comment 10 adds the one case where writing it breaks the
resume: a blocked run.

**Section 4, sweep row 3 — `lexique.md`, `## Tranché` / `## Non
tranché`, retired terms under the kept one; reader Lexicographe (grep
at inv. 4) and Rédacteur; "wired".**
Partly found above. The agent contradicts the reader list on one point
and the verdict is short on another: the lexicographe reads it at
invocation 1 too ("From the second sweep on, read `lexique.md`'s
`## Tranché` first") and at invocation 3 ("read it, and ask whether the
answer's word means one of them"), not at 4 only. And "wired" judges a
description: read in the agent, the file's shape is an example, the
inventory's place in it is unstated (comment 1), and invocation 2's
move 1 tells the agent not to open it (comment 2). Whether the Rédacteur
reads it is left to the section below.

**Section 4, sweep row 4 — two natures of word (quoted display text /
unquoted concept in English), Lexicographe → Rédacteur, wired.**
Consistent with the agent's Part 1. What the verdict could not see:
the agent raises the quote doubt (sweep 3) and has no move to apply the
answer (comments 4 and 6), and its replacement rule runs into quoted
text (comment 5).

**Section 4, sweep rows 21 and 30, D10 — the Lexicographe reads
`questions-sondeur-NN.md` and `questions-convertisseur-NN.md` at 3/4;
technical questions from the Convertisseur travel the product route
through the Lexicographe.**
Not found above, and here is what the agent says: nothing. The
answered file is "another agent's questions file, whichever wrote it";
invocations 3 and 4 treat every answer alike — swept against the
product vocabulary, retired product terms replaced in it. A technical
naming answer would be compared against product terms and could be
edited by invocation 4 as if it were one. The agent neither routes nor
recognises a technical question; whether one ever arrives is the
Convertisseur's file to settle (section below).

**Section 5, U1 — the loop before the product file: stop checkable
(the empty file), bound none, "un terme tranché peut révéler une
paire"; eight turns on one feature, half on graphics and label
variants, scope narrowed in answer.**
Partly found above. The narrowing the verdict reports is in the agent
("Not how a view looks … Not the variants of one displayed text"). On
the bound, the agent gives what the verdict does not: "What it settles
is never asked again" — each turn either settles at least one pair or
ends, so the loop is bounded by the number of pairs the file holds,
not by the person's patience. Comment 16 removes the one turn that is
run on an unchanged file only to produce the empty file that ends it.

**Section 5, U2 — the loop on an answer file: stop "inv. 4 has run";
bound one pass per answer file plus one person turn if 3 asks.**
Already found above — comment 9. The verdict's "one pass" is two opus
invocations and two command runs (each with its commit, worktree,
merge, push) on every answer file, whether or not 3 asks; the agent
says so itself ("when invocation 3 asked nothing, your questions file
is empty, and you still run").

**Section 5, U3, U4, U5 — the Lexicographe 3/4 sits on the route
between the person and the Rédacteur's integration, on every
questions file (Rédacteur's, Classeur's, Sondeurs').**
Consistent with the agent: invocations 3 and 4 accept any answered
file. Nothing to add beyond comment 9 (one command run per file
instead of two).

**Sections 6 and 7** name no item for this agent. P13 (a whole
document fits one context) names the Rédacteur, the Sondeur and
others, not the Lexicographe; it is what led me to comment 17, which my
own pass had missed.

---

## What another agent would settle

**Does the Rédacteur read `lexique.md`, and does it write into it the
English word it chooses for each concept?**
`redacteur.md`. The agent says "The lexicon is read after you — by the
Rédacteur"; the `/2_structure` prompt names only `idees.md` or the
questions file to integrate, never the lexicon. If the Rédacteur reads
it and records its English renderings: the lexicon is the chain's
vocabulary, and invocation 3 can compare an answer's word against the
term the product file actually uses. If it reads it and records
nothing: two integrations may translate one retained French concept
into two English words — a second name for one thing, created by the
chain after the vocabulary was settled, and invisible to invocation 3,
which never opens the product file. If it does not read it at all: the
"kept side by side" answers and the displayed-text / concept pairs the
lexicon records reach nobody, and the lexicon feeds only the
lexicographe.

**Do every other agent's questions files carry one `Question:` line and
one `Answer:` field per entry?**
`redacteur.md`, `classeur.md`, `sondeur.md`, `convertisseur.md` (and
the `/4_grille` and `/6_convertit` renumbering). Invocations 3 and 4
rest on those two labels — read the `Answer:` fields, replace in them,
never touch a `Question:` line. Same shape everywhere: the moves have
their anchor. Any file with another shape (a multi-line answer without
the label, an answer in a table): invocation 4's "replace in the
answers" and its "never touch a question" have nothing to grep, and
the agent decides where an answer ends.

**Does the Convertisseur's questions file carry technical naming
questions?** (verdict D10, item 15)
`convertisseur.md`. Yes: the lexicographe's invocation 3 sweeps a
technical answer against the product vocabulary and may raise a
question the Product Owner cannot answer, and invocation 4 may replace
a technical name with a product term as a "retired term". No: nothing
to change in this agent.

**Should `/2_structure`'s first step — file any `questions-lexicographe`
at the root, unconditionally — stop on one whose `Answer:` fields are
empty?**
The Rédacteur's pass (`/2_structure` is its command). Invocations 2 and
4 write a new questions file only when an answer left the choice open,
and it waits at the root on the Product Owner; the relay says to answer
it and run `/1_lexique` again. A Product Owner who runs `/2_structure`
instead sees that file archived unanswered. Stops on an empty
`Answer:`: the open choices are kept. Files it regardless: they are
lost with no signal, and the Rédacteur integrates on a vocabulary that
still holds the open pair.
