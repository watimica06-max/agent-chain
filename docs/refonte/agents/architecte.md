# architecte — examination

Files read: `.claude/agents/architecte.md`; `.claude/commands/conventions.md`,
`.claude/commands/7_lots.md`, `.claude/commands/8_code.md` (the three that
invoke it — `audit_conventions.md` only reads the `architecte/` folder and
was left unopened). Then `docs/refonte/verdict.md`, last.

---

## The sweep (plane 1)

**Role, from the file**: the agent writes and amends
`docs/TECHNICAL_CONVENTIONS.md` — deriving it from the product file and the
technical document through a grid (invocation 1), turning the Product
Owner's answers into rules (invocation 2), and judging the conventions
requests coding agents raise (invocation 3).

**Moves, in order.**

| Move | Why it exists | What it feeds | Overlaps |
|---|---|---|---|
| I1.1 Load the grid | Rule forms and readings come from it | Every later move | Repeats *What you read* — a read, not a move |
| I1.2 Match the two documents via `tracabilite.md` | Reading V6; the block↔entry correspondence | I1.3, questions | — |
| I1.3 Establish readings V1–V10 | Material the triggers weigh | I1.4, I1.5 | — |
| I1.4 Raise the readings' anomalies | Inconsistencies of the corpus surface | The questions file | Produces questions of a kind the file's two kinds do not name (C3) |
| I1.5 Walk part B, C1–C12, fill holes | The rules themselves | I1.7, I1.8, questions | — |
| I1.6 Off-grid rules | What the corpus states and the grid misses | I1.7, I1.8 | — |
| I1.7 Write the conventions file | The deliverable | Every coding agent | — |
| I1.8 Write `couverture.md` | Proof the sweep reached every entry; the mechanical/review split | The Product Owner; I2; (I3 by declaration only — C14) | — |
| I1.9 Check coverage | Catches an entry the sweep missed | Back to I1.5 | Checks I1.8's own output (C8) |
| I1.10 Write the questions file, report | The Product Owner's channel | Invocation 2 | — |
| I2.1 Read the answered file | — | I2.2 | — |
| I2.2 Turn each answer into a rule, add its coverage line | Closes the holes | The conventions file | No path for an answer that is not a rule (C3) |
| I3.1 Read every empty-verdict request | One rule for two requests | I3.2–5 | — |
| I3.2 Look it up (platform / tool / project declares) | Facts a claim rests on | I3.3 | Q3 and I3.4 both look for "already there" — different places, both unbounded today (C12) |
| I3.3 Three filters | Says whether it is a convention at all | I3.5 | Contradicts I1's mechanical rules (C13) |
| I3.4 A rule that already carries it | Avoids a duplicate rule | I3.5 | — |
| I3.5 Settle and write | The verdict, the rule, the cross-reference of a narrowing rule | The requester; the conventions file | — |

**The set.** Every move's output is carried forward except two things: the
numbered `blocked_architecte-NN.md` files, declared read by "the next run"
and used by no move (C18), and `couverture.md` at invocation 3, declared an
input and touched by no move (C14). No move could go without something
breaking; I1.9 could fold into I1.8 but costs nothing where it is. The
order holds; the two sections that constrain invocation 1 (*What you
settle, and what you ask*; the questions-file shape) sit after the ten
moves that use them, but the file is read whole, and that moves no measure.

Found clean and left alone: the invocation table's exclusivity rule
("you load nothing another one lists"); the narrowing-rule cross-reference;
the verdict carrying the rule's text; the empty-section rule; the
`no rule` written out; the renaming protocol; the "never block out of
caution" line; `Answer:` written empty and never omitted.

---

## Comments, in the order to apply them

### C1

    Fichier      : .claude/agents/architecte.md
    Cible        : the whole file — the prefix "R"
    Aujourd'hui  : "R2", "R3", "R4" name entries of the grid ("Write a rule
                   whose hole you could not fill — R2", "Amend the grid you
                   apply — R4", "except under R3"); "R12", "R30", "R74",
                   "R93" name rules of the conventions file.
    Le défaut    : Plane 2, question 4 — one term, two referents. A reader
                   who has seen nothing else cannot tell whether "under R3"
                   points into the grid or into the file it is writing.
    Ce qu'il faut: grid rules and conventions rules are told apart by their
                   prefix, and every reference to a grid rule says it is the
                   grid's. (Whether the grid itself uses "R" is a fault to
                   note on the grid, not to fix here.)
    Justification: Robustness — three entries of *What you never do* hang
                   on these references; a guard resolved to the wrong file
                   guards nothing.

### C2

    Fichier      : .claude/agents/architecte.md
    Cible        : "The coverage file" — the second column of the first
                   table (N1…N7) and the second column of the second table
                   (G5.1, G6.6, G7.3, G2.3)
    Aujourd'hui  : the examples show "§1.1 N1 → R12" and "R12 G5.1
                   mechanical". Nothing says what N is nor where it is read
                   from; the grid's entries are called C1–C12 in move 5 and
                   G-numbers here, and nothing says they are the same thing.
    Le défaut    : Plane 2, question 4 — a placeholder with no rule for what
                   fills it; one object under two names.
    Ce qu'il faut: the file says what the N column carries and which
                   document it is read from (if it is the entry's nature as
                   the technical document carries it, say so); grid entries
                   have one name throughout the agent.
    Justification: Round trips — the coverage file is what the Product
                   Owner reads to trust the sweep; a column filled by guess
                   sends her back to the run. Tokens — a search for the
                   meaning, at every invocation 1.

### C3

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, moves 2 and 4; "What you settle, and what
                   you ask" (the three kinds of gap); invocation 2, move 2
    Aujourd'hui  : every question must say which kind it is — coverage or
                   conjunction. Move 2 raises "a block whose line carries a
                   dash, or an entry that line names nowhere"; move 4 raises
                   "a cycle in V2, numbers that disagree in V5". Invocation 2
                   "turns each answer into a rule" and has one other exit:
                   an answer that leaves the choice open goes back as a
                   question.
    Le défaut    : Plane 1 — moves 2 and 4 produce questions that are
                   neither coverage nor conjunction: they are inconsistencies
                   of the corpus (a product block with no entry, two numbers
                   that disagree). Plane 2, question 3 on invocation 2 — the
                   answer to such a question is a correction of the technical
                   document, not a rule, and invocation 2 has no path for it:
                   it will write a "rule" that says what the technical
                   document should have said. Also: "an entry that line names
                   nowhere" reads two ways (an entry no line names / an entry
                   the line names but which does not exist).
    Ce qu'il faut: a third kind exists — an inconsistency of the corpus —
                   whose answer lands upstream, not in the conventions file;
                   invocation 2 knows what to do with an answer of that kind
                   (nothing in the conventions file; the coverage line
                   records that the entry was corrected, or that the
                   question stands); the command relays that kind as
                   something to fix in the technical document. And move 2's
                   two cases are stated so that one reading remains.
    Justification: Robustness — dominant: a technical fact written as a
                   convention is read by every lot as a constraint, and the
                   technical document stays wrong. Round trips — one, saved
                   when the answer goes where it belongs the first time.

### C4

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, move 4
    Aujourd'hui  : "a cycle in V2, numbers that disagree in V5, diverging
                   pairs in V7" — three readings out of ten.
    Le défaut    : Plane 2, question 1 — it enumerates where it may mean a
                   class. If part A of the grid defines what an anomaly is
                   for V1, V3, V4, V8–V10, those pass; if it does not, the
                   three are the whole list and the move should say so.
    Ce qu'il faut: the move states the class — every anomaly part A names
                   for its reading — with the three as instances; or it
                   states that these three are exhaustive.
    Justification: Robustness — an anomaly a reading exposes and nobody
                   raises is a hole two lots fill differently.

### C5

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, move 5 ("the platform's own practice") and
                   "What you settle" ("You know those practices — no file
                   lists them"); against invocation 3, move 2 ("Look, do not
                   recall") and the web being forbidden outside invocation 3
    Aujourd'hui  : at invocation 1 a hole is filled from recalled platform
                   practice and the web is forbidden; at invocation 3 recall
                   is forbidden for the same kind of fact, because "judging a
                   claim about a platform … needs looking up rather than
                   knowing".
    Le défaut    : two passages of one agent asking for different things.
                   Plane 2, question 2 — a move resting on a fact nothing
                   gives it: at invocation 1 the agent will guess, by the
                   file's own reasoning at invocation 3.
    Ce qu'il faut: one standard for a fact about the platform, whichever
                   invocation. If looking it up is what makes such a claim
                   reliable, invocation 1 may look up the holes it fills
                   from platform practice, and that alone; if recall is
                   accepted at invocation 1, the asymmetry is stated and
                   the reason given at invocation 3 goes.
    Justification: Robustness — a rule written from a wrong recollection at
                   invocation 1 is read by every lot of the feature; a rule
                   at invocation 3 governs one request.

### C6

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, move 6 ("Each cites the entries that state
                   it, and carries off-grid"); "What you never do" ("unless
                   it carries off-grid and cites the entries"); against
                   move 7 ("No provenance in it") and "The coverage file"
                   ("A rule written under R3 carries off-grid at the end of
                   its line")
    Aujourd'hui  : two passages put the mark and the citing entries on the
                   rule; one puts them on the coverage line; move 7 forbids
                   provenance in the conventions file.
    Le défaut    : Plane 2, question 4 — the instruction reads two ways, and
                   one of the readings breaks move 7.
    Ce qu'il faut: the mark and the citations live in one place, the
                   coverage line; the rule in the conventions file carries
                   nothing that says where it came from.
    Justification: Tokens — provenance in the conventions file is read by
                   every coding agent of every lot, which is exactly what
                   move 7 refuses to pay.

### C7

    Fichier      : .claude/agents/architecte.md
    Cible        : "What you write" — "Numbered, never merely titled … the
                   coding agents cite them"
    Aujourd'hui  : rules carry numbers (R12 … R93); nothing says whether the
                   sequence is global or per section, whether a number is
                   ever reused, or what happens to numbers when invocation 2
                   or 3 inserts a rule "in the section the grid gives it",
                   changes one ("R30 changed") or withdraws one.
    Le défaut    : Plane 2, question 4 — a placeholder with no rule; Plane 2,
                   question 3 — the insertion case is unforeseen.
    Ce qu'il faut: a number is allocated once, from one sequence for the
                   whole file, never reused and never shifted; a rule added
                   later takes the next number whatever section it enters;
                   a rule withdrawn keeps its number and says it is
                   withdrawn.
    Justification: Robustness — a spec sheet cites R30; a renumbering at
                   invocation 3 silently points every citation at another
                   rule, and nothing downstream can detect it.

### C8

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, move 9 — "back to move 5"
    Aujourd'hui  : one identifier missing from the first column sends the
                   agent back to move 5; nothing says whether the walk
                   repeats for that entry alone, and whether moves 6, 7 and 8
                   are redone.
    Le défaut    : Plane 2, question 4 — reads two ways; a loop whose
                   ceiling is implicit.
    Ce qu'il faut: the walk repeats for the missing entries alone; the files
                   already written are amended, not rewritten.
    Justification: Tokens — a second walk of C1–C12 over the whole document,
                   and a second write of the conventions file, for one
                   entry.

### C9

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, "Your number: the highest
                   questions-architecte-NN.md at the root, or in
                   questions/architecte/ if the root holds none"; invocation
                   2, move 1 ("the questions file you wrote"); against "Never
                   list a folder" ("What you read"; "What you never do")
    Aujourd'hui  : the number and the file to integrate can only be found by
                   listing, and listing is forbidden everywhere but
                   `architecte/` at invocation 3.
    Le défaut    : two passages asking for different things; Plane 2,
                   question 2 — a fact nothing gives the agent, under a rule
                   that forbids finding it.
    Ce qu'il faut: the prompt names the number (or the file) — the command
                   already checks for `questions-architecte-*.md` at the
                   root — or the never-list rule carves out that one glob by
                   pattern. The first is cheaper: the command has the fact.
    Justification: Robustness — an agent that obeys the rule writes `-01`
                   over the answered file at the root and destroys the
                   answers. Tokens — trivial either way.

### C10

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 2, move 1 — "and it alone"
    Aujourd'hui  : the invocation table lists four inputs for invocation 2;
                   move 1 says the questions file alone.
    Le défaut    : Plane 2, question 4 — read literally, invocation 2 amends
                   a conventions file it has not opened, against the file's
                   own line "you cannot amend what you have not read".
    Ce qu'il faut: "alone" is among questions files — not the other agents'
                   — and the table's three other inputs stand.
    Justification: Robustness — a rule written into a file the agent has
                   not read lands in a section it located by guess, or the
                   edit fails and the run ends with nothing integrated.

### C11

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 2 — "An answer that leaves the choice open goes
                   back as a new entry, with an empty Answer: field"; the
                   invocation table's Output column for invocation 2
    Aujourd'hui  : which file receives the new entry is unsaid; invocation
                   2's outputs list no questions file; the report-back would
                   then count that question nowhere.
    Le défaut    : Plane 2, questions 1 and 4.
    Ce qu'il faut: a new questions file, numbered like invocation 1's,
                   listed among invocation 2's outputs and counted in the
                   report; the command's table then has a row for it (see
                   CMD1).
    Justification: Round trips — an open answer appended to a file already
                   answered is a question the Product Owner does not reopen;
                   the hole stays until a lot hits it, and then it is a
                   Robustness cost.

### C12

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 3 — "the build files" (table, preamble, "What
                   you never do"); move 2, third question ("does the project
                   already declare it somewhere?")
    Aujourd'hui  : "build files" is never defined; "a manifest" is forbidden
                   in the same sentence that allows build files, and a
                   manifest is where a project declares its dependencies and
                   its analysers' configuration; "somewhere" is unbounded.
    Le défaut    : Plane 2, question 4 — a term undefined, an instruction
                   that reads two ways; Plane 3, criterion 2 — "somewhere"
                   could run forever.
    Ce qu'il faut: the class is named in universal terms — the files the
                   build tool and the analysers read to configure
                   themselves, the dependency manifest among them — and
                   "somewhere" is bounded to that class plus the conventions
                   file in force.
    Justification: Robustness — a rule a linter configuration already
                   enforces gets written again, or a request is refused as
                   "declared" when nothing declares it. Tokens — an agent
                   unsure of what it may open opens more.

### C13

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 3, move 3 — "A tool checks it, or could";
                   against move 2 ("a tool the project could name already
                   check it") and "The coverage file" (rules whose test is
                   "mechanical … must be wired into the verification
                   command")
    Aujourd'hui  : invocation 1 writes rules whose test is mechanical — that
                   is, tool-checkable — and records them so they get wired;
                   invocation 3 refuses as "not a convention" anything a
                   tool "checks, or could".
    Le défaut    : two passages of one agent asking for different things;
                   Plane 3, criterion 4 — "or could" admits any rule, since
                   any naming or layout rule could be a custom check.
    Ce qu'il faut: one line, true at both invocations — a rule the project
                   chose is a convention whether or not a tool can check it;
                   a tool's checking it sets the rule's test kind and
                   nothing else; what is refused is what leaves no choice
                   (the platform imposes it) or holds on one machine.
    Justification: Robustness — a real convention refused as "tooling", with
                   no tool in place, leaves the hole open — the defect the
                   agent says it exists to prevent.

### C14

    Fichier      : .claude/agents/architecte.md
    Cible        : the invocation table, row 3 (`couverture.md` as an input);
                   invocation 3, move 5; "The coverage file" — "One reader:
                   the Product Owner, once"
    Aujourd'hui  : `couverture.md` is listed among invocation 3's inputs; no
                   move of invocation 3 reads or writes it; a rule written at
                   invocation 3 never enters the second table, whose stated
                   purpose is that every mechanical rule gets wired; and the
                   file declares one reader, once, while invocations 2 and 3
                   read it.
    Le défaut    : Plane 2, question 2 — a read no move uses, paid after
                   every lot; Plane 1 — a rule written at invocation 3
                   escapes the mechanism invocation 1 set up.
    Ce qu'il faut: move 5 adds the new rule's line to the second table (test
                   kind) and, for the first table, a line naming the request
                   as what motivates it — or `couverture.md` leaves
                   invocation 3's inputs. And "one reader, once" is corrected
                   to what the table says.
    Justification: Tokens — one file read for nothing at the end of every
                   lot, today. Robustness — if the second table is how
                   mechanical rules get wired, none written at invocation 3
                   ever is.

### C15

    Fichier      : .claude/agents/architecte.md
    Cible        : "When you cannot produce" — the list of what blocks; the
                   term "a mandatory-sections file"
    Aujourd'hui  : "no technical document, a document with no entry filled,
                   a mandatory-sections file that is not there". Nothing for
                   the conventions file being absent at invocation 2 or 3 —
                   and invocation 3 is launched by `/7_lots` and `/8_code`,
                   neither of which checks that `/conventions` ever ran
                   ("run by hand — /cycle does not call it").
                   "Mandatory-sections file" is a term the file does not
                   define.
    Le défaut    : Plane 2, question 3 — unforeseen, the agent invents: a
                   fresh file with one rule and no sections, or an unasked
                   invocation 1 without its two documents. Plane 2, question
                   4 — a term with no referent.
    Ce qu'il faut: the conventions file absent at invocation 2 or 3 is a
                   block whose *To resume* is "run /conventions, invocation
                   1"; at invocation 3 when the Arbitre called, where a
                   block is forbidden, the refusal in the verdict says the
                   same. "Mandatory-sections file" is replaced by the path of
                   what is meant.
    Justification: Robustness — dominant: a one-rule file without its twelve
                   sections is what every lot then reads, and the split was
                   cut against nothing. Round trips — one, instead of a
                   downstream cycle on an improvised file.

### C16

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 3, move 1 — "requests whose ## Verdict is
                   empty, and those alone. A filled one is done."
    Aujourd'hui  : a request with no `## Verdict` heading at all is neither.
    Le défaut    : Plane 2, question 3 — unforeseen.
    Ce qu'il faut: an absent heading counts as empty; the agent adds the
                   heading and writes under it. The same wording holds for
                   the commands' glob ("Any request with an empty
                   ## Verdict").
    Justification: Robustness — by the file's own line, "a request with no
                   verdict reads as one nobody looked at"; the requester's
                   hole stays.

### C17

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 3, near the end — "You settle, you refuse, or
                   you block — and you go out"; against move 5's last row
                   ("never a blocking file here") and "When you cannot
                   produce"
    Aujourd'hui  : the same invocation says both that it never writes a
                   blocking file and that blocking is one of its three
                   exits.
    Le défaut    : two passages of one agent asking for different things.
    Ce qu'il faut: within invocation 3 a request has two exits — settled or
                   refused; a block exists for a missing input only (C15),
                   and the sentence says so.
    Justification: Robustness — an agent that reads "or you block" writes a
                   blocking file while the Arbitre waits: the two-agents-on-
                   one-answer case the file itself names.

### C18

    Fichier      : .claude/agents/architecte.md
    Cible        : "When you resume after a blocking file" — "the numbered
                   ones are the record … and the next run reads them"; the
                   row "Filled → Apply it"
    Aujourd'hui  : the numbered files are declared read and no move uses
                   them. Every block this agent can raise is a missing input
                   (C15), which a `## Decision` cannot supply — so "apply it"
                   has nothing to apply.
    Le défaut    : Plane 2, question 2 — a read no move uses; Plane 1 — a
                   result nothing carries forward.
    Ce qu'il faut: either a move names what it does with the record, or the
                   numbered files are history and declared unread; and the
                   row says what applying a decision to a missing-input
                   block means — check the input is there now, carry on.
    Justification: Tokens — N files read at every resume. Round trips — a
                   Product Owner told to fill a `## Decision` that nothing
                   can act on.

### C19

    Fichier      : .claude/agents/architecte.md
    Cible        : invocation 1, move 7 ("costs four hundred tokens read at
                   every lot"); "What you settle" — the paragraph "A
                   conjunction is invisible upstream, and not through any
                   carelessness…" and "*What identifies a segment* once the
                   product has said what the user sees"; invocation 3
                   preamble ("and for good reason — here you are not
                   deriving a file…")
    Aujourd'hui  : rules carrying their justification; one example drawn
                   from one product ("a segment").
    Le défaut    : Plane 3, criterion 5 (justification and commentary on why
                   the rule came to be); criterion 1 for the example.
    Ce qu'il faut: each rule stands without its reason; the example is
                   dropped or made general.
    Justification: Tokens — read at every invocation of an opus agent.
                   Nothing else moves; this is the only measure claimed.

### C20

    Fichier      : .claude/agents/architecte.md
    Cible        : "What you read" — "GRILLE_CONVENTIONS.md, in full, at
                   every invocation"
    Aujourd'hui  : the grid is read whole at all three invocations. Part A
                   (the readings) serves invocation 1 alone; invocations 2
                   and 3 need the shape of the file and part B's sections
                   and rule forms.
    Le défaut    : Plane 2, question 2 — a file read whole where a part
                   would do, paid at the end of every lot.
    Ce qu'il faut: the invocation table names which part of the grid each
                   invocation loads. If the grid is not partitioned so that
                   this is possible, that is a fault to note on the grid.
    Justification: Tokens — invocation 3 runs after every lot that left a
                   request; part A is loaded each time for nothing.

### CMD1

    Fichier      : .claude/commands/conventions.md
    Cible        : "Which invocation" — the table; "When it runs" — the two
                   stop rules
    Aujourd'hui  : three rows: a request with an empty verdict → 3; "a
                   questions-architecte-NN.md, answered" → 2; "nothing of the
                   sort" → 1. The agent writes a questions file "always,
                   empty or not"; the highest one stays at the root forever
                   ("it carries the numbering").
    Le défaut    : command, question 1 — cases with no row: (a) the
                   questions file holds zero questions — not "answered", not
                   "nothing of the sort"; (b) the answered file already
                   integrated — it stays at the root, so every later run
                   matches row 2 again and integrates the same answers
                   twice; (c) nothing tells the orchestrator the job is
                   finished. Any fall-through reaches row 1, and invocation 1
                   by the agent's own rule opens no existing conventions file
                   and writes it afresh — every amendment invocation 3 made
                   since, from `/7_lots` and `/8_code`, is lost.
    Ce qu'il faut: a terminal state readable from presence alone — the
                   integrated file leaves the root (filed away by the
                   command, or by the agent at the end of invocation 2), and
                   a questions file with no `### Q` reads as "nothing asked";
                   rows for "nothing asked → nothing to do, /7_lots is next"
                   and "answered and integrated → nothing to do"; and row 1
                   fires only when this feature has not been derived yet —
                   a presence test on the feature's own `couverture.md`
                   (written by invocation 1 alone, at the working folder's
                   root), no opening. The repository-wide conventions file
                   cannot be that test: it exists from the second feature
                   on. With C11, a new questions file written by invocation
                   2 then routes to row 2 like any other.
    Justification: Robustness — dominant: a silent rewrite of the file every
                   lot reads. Round trips — a run that does nothing and says
                   so costs nothing; a re-derivation costs an opus
                   invocation and a review of a file that should not have
                   changed.

### CMD2

    Fichier      : .claude/commands/conventions.md
    Cible        : the argument line — "Feature folder:
                   docs/features/$ARGUMENTS/"; against "A second argument
                   names it" (the bugfix folder for invocation 3)
    Aujourd'hui  : with a second argument, `$ARGUMENTS` holds both words and
                   the path is built from both. `/8_code` guards this very
                   trap ("the first argument only; $ARGUMENTS holds both");
                   this command does not.
    Le défaut    : command, question 2 — the prompt carries a path the agent
                   cannot use.
    Ce qu'il faut: the feature folder is built from the first argument; the
                   working folder passed to invocation 3 is the feature
                   folder, or the `bugfix-NN/` the second argument names
                   inside it; the invocation example shows the invocation 3
                   form too.
    Justification: Round trips — an invocation lost on a wrong path, on
                   every bug-fix cycle that uses this command.

### CMD3

    Fichier      : .claude/commands/conventions.md
    Cible        : "When it runs" — "Stop if a root questions-architecte-*.md
                   carries an empty Answer:"; against "What you read — only
                   whether the files are there"
    Aujourd'hui  : the test needs the file's content; the reading rule
                   allows presence only.
    Le défaut    : two passages asking for different things; Plane 2,
                   question 4 on the command.
    Ce qu'il faut: the test is a grep for `Answer:` lines with nothing after
                   them, and the reading rule says that grep is allowed and
                   opening is not.
    Justification: Round trips — an orchestrator that keeps to "presence
                   only" skips the check and runs invocation 2 on unanswered
                   questions, which come straight back. Tokens — an
                   orchestrator that opens the file loads it for nothing.

### CMD4

    Fichier      : .claude/commands/conventions.md (and the same step in
                   7_lots.md and 8_code.md around the architecte invocation)
    Cible        : "Git, in this mode" — "once the agent reports: 1. merge,
                   2. push, 3. worktree remove"
    Aujourd'hui  : no commit between the agent's report and the merge. The
                   agent has no Bash and commits nothing; `git merge` takes
                   the branch's commits, not the worktree's uncommitted
                   files; `git worktree remove` refuses a dirty tree. In
                   `/8_code` the Réalisateur commits its lot, and the
                   architecte writes after that commit, at the end of the
                   lot; in `/7_lots` the Cadreur has no Bash either.
    Le défaut    : command, question 1 — the outcome "files written,
                   uncommitted" has no step. (If the orchestrator commits
                   by habit, the step is still unwritten, and CLAUDE.md's
                   merge rule does not carry it either.)
    Ce qu'il faut: the sequence is commit, merge, push, remove — in every
                   command that invokes an agent without Bash, and after the
                   architecte's step in `/8_code` whatever the Réalisateur
                   committed before it.
    Justification: Robustness — the conventions file, `couverture.md` and
                   the questions file written and lost; or a merge of a
                   stale branch that says the run happened when its output
                   did not land.

### CMD5

    Fichier      : .claude/commands/conventions.md
    Cible        : "Which invocation" and "What you relay" — the blocking
                   file
    Aujourd'hui  : no row for a `blocked_architecte.md` at the working
                   folder's root — empty `## Decision` (stop and relay) or
                   filled (the agent applies it on its next run); the relay
                   says nothing of it. `/7_lots` names it; this command,
                   which is the one that runs invocation 1 where the agent
                   blocks most, does not.
    Le défaut    : command, question 1 — an outcome with no row.
    Ce qu'il faut: a first row in the table — a block with an empty decision
                   → relay it and stop; a filled one → carry on down the
                   table; and the relay names the file when the run left
                   one.
    Justification: Round trips — the Product Owner learns of the block from
                   the `git status` file list at best, and re-runs blind.

### CMD6

    Fichier      : .claude/commands/conventions.md
    Cible        : "What you relay" — "no decision on what comes next"
    Aujourd'hui  : the command relays the report and the file list and
                   refuses to say what follows. It knows: it sits "after
                   /6_convertit, before /7_lots", and it says a re-run turns
                   answers into rules.
    Le défaut    : command, question 1 — what to run next is absent by
                   design, and every outcome leaves the Product Owner to
                   work it out.
    Ce qu'il faut: one line per outcome — questions raised → answer them,
                   re-run; none, or all integrated → `/7_lots`; blocked →
                   fill `## Decision`, re-run.
    Justification: Round trips — the one question the Product Owner asks
                   after every run, answered by the run.

### CMD7

    Fichier      : .claude/commands/8_code.md
    Cible        : "Where you stop and hand back" — "two places:
                   code/blocked_<agent>.md … code/<lot>/blocked_<agent>.md";
                   move 6 of the loop
    Aujourd'hui  : the architecte's blocking file sits at the working
                   folder's root, a third place the command does not look at;
                   move 6 lists no outcome for its invocation (`/7_lots`
                   does).
    Le défaut    : command, question 1 — an outcome with no row.
    Ce qu'il faut: the root is the third place; move 6's outcomes are
                   written — verdicts written → next lot; a block → stop and
                   relay, as for any other.
    Justification: Robustness — the next lot's Détailleur runs against
                   conventions that were not amended, and the block sits
                   unread. Round trips — the block surfaces one run later,
                   if at all.

### CMD8

    Fichier      : .claude/commands/7_lots.md
    Cible        : "The pending requests" — "If architecte blocks in turn —
                   blocked_architecte.md — stop. It asks for a rule nobody
                   has written."
    Aujourd'hui  : the agent never blocks on a request — a doubt or a
                   product decision goes in the verdict; its only blocks are
                   missing inputs (C15). The case that does occur on the
                   `blocked_cadreur.md` + `architecte/cadreur.md` row — a
                   refusal written in the verdict — is folded into "invoke
                   cadreur again" with nothing said of what a refusal means
                   for the split.
    Le défaut    : command, question 1 — a row whose diagnosis names a case
                   that cannot occur, and the case that does occur has no
                   row.
    Ce qu'il faut: the row says what a block from this agent means — an
                   input is missing, the conventions file first of all, and
                   what to run; the refusal outcome is named, and either
                   handled here or explicitly left to the Cadreur's own
                   rules on its next run.
    Justification: Round trips — an orchestrator that relays "it asks for a
                   rule nobody has written" sends the Product Owner after a
                   decision when the fix was to run `/conventions`.

---

## From the verdict

Read after everything above: `verdict.md` sections 4 to 7 and the
Architecte's line in section 2. One entry per item that names this agent.

**Section 2 — "the role holds; invocation 1 as described has the
per-feature re-derivation defect, but that is a wire, not the role."**
Agreed on the role. The wire is D11, below.

**D11 / section 7, item 4 — invocation 1 re-derives the shared file per
feature, reading none of what exists; once per project or once per
feature, and does it overwrite?**
Not found above in its cross-feature form — CMD1 found the same row and
the same overwrite for a re-run inside one feature. The agent confirms the
verdict's reading, in its own words: *"at invocation 1, no conventions
file, whatever its name … not one your own earlier run left behind"*;
*"`docs/TECHNICAL_CONVENTIONS.md` is shared by the whole repository — one
file, whatever the cycle"*; *"Invocations 1 and 2 run on a feature folder
only"*. The command settles item 4: `/conventions` takes a feature name,
sits "after `/6_convertit`, before `/7_lots`", and its table falls through
to invocation 1 whenever the folder holds no answered questions file and no
request — so on feature N+1 it runs invocation 1, and invocation 1 writes
the shared file blind. Every rule invocation 3 added during feature N is
lost. What has to hold, beyond CMD1's presence test: a derivation on a
repository that already has the file is an amendment — invocation 1 reads
the file in force, derives for the new feature's entries, and adds; the
reason given for not reading it (*"deriving from your own output"*) holds
for the first derivation only — the amendments are settled requests, not
this agent's derivation. CMD1 keeps the command from re-deriving a feature
already derived; this is the agent-side half: row 1 runs once per feature
by design, and the agent's never-open rule holds for the first derivation
in the repository alone — from the second on, invocation 1 reads and
amends. Robustness, at feature scale — the verdict's own measure.

**D14 / section 7, item 20 — `couverture.md`'s second table promises a
wiring nobody does; is it read by any command that wires a check?**
Already found above (C14, and the unsettled section). From the two files
this pass reads, the answer to item 20 is *no*: the agent names the
Product Owner as the one reader, once, and `/conventions` reads nothing
of the run's output but the questions file's line count (*"no reading of
the conventions file, no summary of its rules"*). Whether a downstream
agent reads it is left to the group pass.

**D15 — a coverage gap reaches the person after closure, and its answer
becomes a convention that never re-enters the product route.**
Not found above in this form — C3 is adjacent (answers that are not
rules) but names inconsistencies, not coverage gaps. The agent confirms
it: *"Coverage — a behaviour question the corpus answers nowhere — Raise
it. The framing grid has a hole"*, and invocation 2 *"turns each answer
into a rule"*. It also contradicts itself on it: *"Settle a product
decision — what the user sees belongs to the framing grid"* stands under
*What you never do*, and invocation 2 writes the Product Owner's product
answer into the conventions file, where by the agent's own Role line
*"what to build"* never goes. What has to hold: C3's third kind takes in
the coverage answer — invocation 2 writes nothing in the conventions file
for it and the answer is routed to the product file by whatever route the
upstream uses (which agent carries it there is the group pass's question);
the conjunction and precision kinds stay here. Robustness on the record
(the behaviour lives where the Fusionneur never reads) — the verdict's
measure, and this pass agrees.

**D16 / section 7, item 24 — the asking lot is coded under the old rule;
does invocation 3 record the lot that predates the rule?**
Not found above. The agent says nothing of it: the verdict's shape is
*"Convention — R93 written. <the rule's text>"*, and no line of move 5
names the lot. The information is at hand — the request file is named for
its author and lot (`architecte/arbitre-<lot>.md`, and `/8_code` runs the
invocation at the end of a named lot). What has to hold: the verdict, or
the rule's coverage line, names the lot coded before the rule. One line;
Robustness at the next lot touching the same file, as the verdict says.

**D17 / section 7, item 13 — rename or delete a settled blocking file?**
For this agent, settled by the agent: it renames — *"Renaming is what
closes it — never delete it"*, *"`git mv`, or the equivalent"*. No
contradiction here; C18 notes that the numbered files it keeps are read by
no move of its own.

**D10 — the Convertisseur's technical questions should route to the
Architecte's precision rule, and nothing routes there.**
Not found above — a route between two agents is the group pass's. What
the agent says: the precision rule exists (*"Precision — Settle it
yourself and write it down"*), but the only intake for a question from
outside is invocation 3, which reads `architecte/` in the working folder
and *"opens neither"* document — and *"a rule that needs a feature's
documentation to be written is a rule invocation 1 owed"*. A convertisseur
request would have to take the request form and arrive before invocation
1 has run, which the invocation table does not foresee. Left in the
unsettled section.

**U7 — the derivation loop: "whether invocation 2 may raise again is
unstated — one round assumed".**
Contradicted by the agent, which states it: *"An answer that leaves the
choice open goes back as a new entry, with an empty `Answer:` field."*
Invocation 2 may raise again; the loop has no bound, and C11 found that
where the new entry goes is unsaid. CMD1 gives the command the row it
needs for that second file.

**U11 / section 7, item 17 — the Cadreur re-blocking after an Architecte
refusal; is there a bound in `/7_lots`?**
Half found above (CMD8 — the refusal outcome has no row). The bound: none
in `/7_lots` — the row reads *"invoke `architecte`, invocation 3, then
invoke `cadreur` again"*, with no count, in a command that counts the
Vérificateur's rounds to three. What has to hold on the command's side: one
pass through that row; a second `blocked_cadreur.md` carrying the same
request stops and relays. Whether the Cadreur re-blocks identically is its
file's question. Round trips.

**A-5 — Arbitre → Architecte: the Architecte writes no blocking file
there, "a boundary correctly drawn".**
Agreed, and already found (C17): the boundary is drawn as the verdict
says — *"a blocking file would leave two agents waiting on the same
answer"* — and one sentence in the same invocation undoes it (*"you
settle, you refuse, or you block — and you go out"*). C15 adds the one
case the boundary does not cover: the conventions file absent when the
Arbitre calls.

**A4 / P7 — the coverage and conjunction gaps are evidence of a framing
grid hole, and nothing writes them back where the grid would read them.**
Not found above; not a defect in the agent as written, and this pass may
not correct a grid. What the agent says: every question *"says which kind
of gap it is — coverage or conjunction"* — the evidence is tagged in the
questions file, so a harvest needs no change to this agent, only a reader.
Noted for the group pass.

**A7 / P4 — the Architecte never reads the code; conventions derived
without a line of what they govern.**
Confirmed by the agent: *"And the code, at no invocation — not a source
file, not a generated schema, not a manifest."* Not found above as such;
one consequence is: at invocation 1 the build files are forbidden too, so
on an existing codebase (the chain has a take-over path) the conventions
are derived blind to what the project's analysers already enforce — the
very thing invocation 3's own filter treats as decisive (*"a tool checks
it"*). What has to hold: on a repository that already carries an analyser
configuration, invocation 1 reads it as a declaration the project made,
under the same bound C12 gives invocation 3. Robustness — a rule that
contradicts the linter is a rule every lot breaks or a linter every lot
fights.

**P14 — the conventions file is where the project enters, and it carries
the most boundary defects.**
Agreed; this pass adds C13 (tool-checkable rules refused at invocation 3
and recorded as mechanical at invocation 1) and C15 (no rule for the file
being absent) to that list.

---

## What another agent would settle

**Do every requester (Cadreur, Détailleur, Réalisateur, Arbitre) write a
`## Verdict` heading, empty, in the request?**
`cadreur.md`, `detailleur.md`, `realisateur.md`, `arbitre.md`.
Yes: C16 is a guard for a malformed file only. No: requests without the
heading are invisible to the agent's move 1 and to the three commands'
glob alike, and nobody looks at them.

**Does any downstream agent read `couverture.md`'s second table and wire
a mechanical rule into a verification command?**
`cadreur.md`, `realisateur.md`, `relecteur.md`.
Yes: C14 is stronger — invocation 3's rules escape a wiring that exists.
No: the second table has no reader but the Product Owner, its purpose
line is a promise, and the mechanical/review column is paid for nothing.

**Does the Convertisseur always write `tracabilite.md`?**
`convertisseur.md`. (The verdict's sweep says it does, at invocation 2.)
Always: move 2's fallback "match on titles" is a net over a guarantee —
drop it, and block on absence. Sometimes: the fallback is the move for
those runs, and "say in the questions file that you did" should say what
that costs the coverage.

**Does the technical document carry a nature per entry and `§` numbered
identifiers?**
`convertisseur.md`. Yes: C2's N column has a source, to be named. No: the
column has nothing to carry and goes.

**What prompt does the Arbitre pass when it calls this agent?**
`arbitre.md`. "Working folder … Invocation 3 — Requests": the call works
as the agent's *"The prompt says which one. It is never inferred"*
demands. Less than that: the call fails on the agent's own rule.

**Does the Cadreur, re-run after a refusal in `architecte/cadreur.md`,
treat its own `blocked_cadreur.md` with an empty `## Decision` as a block
still standing, and does it re-block with the same request?**
`cadreur.md`. Standing: the `/7_lots` row loops — block, architecte,
block again — with no count (CMD8, U11). Cleared by the verdict: the row
works and needs only the bound.

**Does the Réalisateur read `TECHNICAL_CONVENTIONS.md` in full?**
`realisateur.md`, `detailleur.md`. Yes: the agent's Role line and move 7's
token argument hold. No: move 7's reason is stale, and the Détailleur is
the one reader of a provenance line — C6 and C19 change nothing either
way.

**Does the Réalisateur's commit take the whole worktree, or only its lot's
files?**
`realisateur.md`. Whole: CMD4 bites in `/8_code` only when the architecte
is the last writer of the run. Its files only: every architecte write in
`/8_code` is uncommitted until the run's end, and CMD4 is the whole
story.

**Is there a route from the Convertisseur's technical questions to this
agent's precision rule?**
`convertisseur.md`, `/6_convertit`. Yes: D10 is narrower than the verdict
says. No: the invocation table needs an intake before invocation 1 has run
— a fourth case, not a request.

**Do `desc-produit.md` and `spec-technique.md` together, plus the grid,
fit the context invocation 1 holds?**
`convertisseur.md` (the size of what it assembles), `redacteur.md`. Yes:
nothing to do. No: invocation 1 has no stop on size and degrades silently;
whether a split by grid part (readings, then entries) is possible would
be the next question.
