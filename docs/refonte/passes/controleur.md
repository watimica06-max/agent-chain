# Phase 3 — controleur

Files read, in this order: `.claude/agents/controleur.md` (whole),
`.claude/commands/9_controle.md` (whole, the command that invokes it),
`.claude/commands/8_code.md` (whole — it names the Contrôleur in four
places and decides what the Product Owner runs next), then
`docs/refonte/verdict.md` sections 2 (the agent's line) and 4 to 7,
last.

---

## Plane 1 — the agent as a whole

**Role, from the file:** confront every intention the product file
describes with the spec sheets, and report — per intention — whether a
signature or an acceptance criterion observes it; per group of blocks
first, then one assembly over the whole feature. Reads no code, judges
no sheet's quality, settles nothing.

**Moves, in the order the file states them:**

| # | Move | Why it exists | What it feeds | What it overlaps |
|---|---|---|---|---|
| 0a | Look for `code/blocked_controleur.md` every run; stop / apply and rename by `## Decision` | Resume after a Product Owner decision | Nothing downstream reads it except the next run of this agent | 0b (both decide whether the run starts) |
| 0b | No `desc-produit.md` → stop, bug-fix cycle | Guard against a wrong invocation | Nothing — the command already stopped on the same test | "When you cannot produce" lists the same case as a blocker |
| 1 | Read the group's sheets, all before any block | Have every criterion in context once | Move 2 | — |
| 2 | Each block, intention by intention: Found / Missing / Doubtful; write `code/controle/<group>.md` | The whole point of the agent | Move 4 | — |
| 3 | Pick the report file name (`rapport-controle.md` or next `-NN`) | Keep earlier reports as a record | Move 4 | — |
| 4 | Merge every `code/controle/*.md` in block order, unchanged; stop on a block nobody answered for | One report the Product Owner reads | The Product Owner (bug-list decision) | — |

**Judgement on the set:**

- Moves 1 to 4 cover the role with no gap and no overlap. Move 2 is
  where robustness lives, and its criterion (observable in a signature
  or an acceptance criterion) is one two readers can apply the same
  way — with one boundary left open, see comment 1.
- Move 0b is a net: `9_controle` stops on the same test before
  invoking. Removing it breaks nothing on the command's path; keeping
  it as a one-line stop costs nothing. What breaks is keeping it in
  *two* shapes (a stop here, a blocking file in Part 1) — see comment 3.
- Move 0a serves no case this agent produces once comments 3 and 4 are
  applied: every situation where it cannot produce is either a report
  line (a doubt) or an orchestration fault a re-run fixes, none of
  which is a decision the Product Owner takes in a `## Decision` field.
  And as written it cannot be executed — see comment 5.
- Move 4 rests on a fact nothing gives it (the full list of blocks and
  groups) — see comment 6.
- Order: fine. Move 0a says "first thing, every run" although it is
  stated after the invocation table; a reader gets it.

---

## Comments

Ordered so that applying them top to bottom works.

---

### 1

    Fichier      : .claude/agents/controleur.md
    Cible        : Invocation 1, move 2 — the three outcomes, the rule
                   "An intention you cannot attach goes under doubtful,
                   never under missing", and the `## Doubts` example
    Aujourd'hui  : Missing = "the intention, and what it described";
                   Doubtful = "the intention, and what stops you
                   deciding"; then "You do not settle a doubt. An
                   intention you cannot attach goes under doubtful,
                   never under missing"; and the example doubt is
                   "B8 Removal of the macros band — lot-11 modifies the
                   band's provider, but no criterion observes its
                   disappearance"
    Le défaut    : Plane 3, criterion 4, and Plane 2 Q1. "Cannot attach"
                   describes every missing intention — one no criterion
                   observes is exactly one the agent cannot attach — so
                   the sentence routes every miss to Doubtful and
                   leaves Missing unreachable. The example confirms the
                   wrong reading: by the agent's own criterion (a
                   sheet that mentions without observing does not
                   carry) B8 is a clear Missing, filed as a Doubt.
    Ce qu'il faut: One boundary, stated once. Missing is a fact the
                   agent can state: no signature and no criterion of
                   the group's sheets observes the intention. Doubtful
                   is a criterion that may observe it and the agent
                   cannot tell from the sheet alone which way (a
                   criterion phrased over a class, an intention whose
                   observable is not named in the block). The "cannot
                   attach" sentence goes, and the B8 example moves to
                   the Missing field or is replaced by a real doubt.
    Justification: Robustness. A miss filed as a doubt is a gap the
                   Product Owner may not open a correction cycle on;
                   the report's whole value is the Missing field being
                   trusted.

---

### 2

    Fichier      : .claude/agents/controleur.md
    Cible        : Invocation 1, move 2 — "The unit is the sentence,
                   never the whole block", "Ask which sheet observes the
                   caller — none, and the block is missing", and "What
                   you never do — Answer for a whole block at once —
                   one line per intention"
    Aujourd'hui  : Three names for the unit: the sentence (move 2), the
                   block (the caller rule), the intention (the example
                   lines, the never-do entry, "every path in [a
                   navigation map] is an intention")
    Le défaut    : Plane 3, criterion 4 (two readings), Plane 2 Q1 (can
                   two readers cut the same way). A sentence carrying
                   two intentions — "the icon opens the profile and
                   marks it read" — gets one answer under the sentence
                   rule; a table row is not a sentence; "the block is
                   missing" contradicts one-line-per-intention.
    Ce qu'il faut: The unit is the intention. The sentence is the
                   default cut; a row, a list item, a path in a map is
                   a cut too; one sentence naming two observables gives
                   two lines. The caller rule concludes on the
                   intention, not the block.
    Justification: Robustness. A second intention hidden in a sentence
                   already answered Found is the shape of gap this agent
                   exists to catch.

---

### 3

    Fichier      : .claude/agents/controleur.md
    Cible        : Part 1 "When you cannot produce" ("no product file")
                   and Part 2 "A feature cycle only"
    Aujourd'hui  : Part 1: block — write `code/blocked_controleur.md`
                   with an empty `## Decision` — when there is "no
                   product file". Part 2: "No `desc-produit.md` in the
                   working folder means you were invoked on a bug-fix
                   cycle: stop and say so."
    Le défaut    : Two passages of one agent asking for different
                   things on one situation (Plane 2 Q3, and the known
                   list). And the situation is an orchestration fault:
                   a `## Decision` on "there is no product file" is not
                   a decision the Product Owner can take. The command
                   already stops on the same test before invoking.
    Ce qu'il faut: One behaviour: stop and say so, no file. "No product
                   file" leaves the blocker list.
    Justification: Round trips. A blocking file here asks the Product
                   Owner to answer a question that is the orchestrator's
                   to fix, and the answer would lift nothing.

---

### 4

    Fichier      : .claude/agents/controleur.md
    Cible        : "What you read" (the paragraph on a `code/<lot>/`
                   folder with no sheet, and the one on merged lots) and
                   "When you cannot produce" ("lots whose sheets do not
                   exist")
    Aujourd'hui  : "What you read": a folder holding no sheet → "report
                   it as a doubt, not as a missing intention"; a merged
                   lot "leaves no folder at all; you will not see it".
                   "When you cannot produce": block on "lots whose
                   sheets do not exist".
    Le défaut    : Two passages asking different things (doubt vs
                   blocker) on the same situation. Plane 3, criterion 3
                   for both: the command invokes only after every lot
                   of the sequence carries a PASS verdict, and the agent
                   opens only the sheets its prompt names — a named lot
                   with no sheet is a fault upstream of this agent, and
                   a merged lot's folder is something it never globs
                   for. The merged-lot paragraph explains a situation
                   the agent's own reading rules keep it from meeting.
    Ce qu'il faut: One behaviour, and the report-side one: a sheet the
                   prompt names and that is not there puts every
                   intention of the blocks it was to answer for under
                   Doubtful, naming the lot — and the run continues.
                   "Lots whose sheets do not exist" leaves the blocker
                   list; the merged-lot paragraph goes.
    Justification: Round trips (a doubt in the report reaches the
                   Product Owner in the same run; a blocking file costs
                   a full stop and a re-run on a fact she can see in the
                   report), and tokens (a paragraph read at every
                   invocation about a case that cannot arise).

---

### 5

    Fichier      : .claude/agents/controleur.md
    Cible        : "When you cannot produce" (the whole section), "When
                   you resume after a blocking file" (the whole
                   section), and the two Invocation 2 sentences that
                   say "blocker"
    Aujourd'hui  : A blocking-file mechanism: write
                   `code/blocked_controleur.md` with an empty
                   `## Decision`; at every run look for it, stop if the
                   field is empty, apply and rename to `-NN` if filled;
                   "Renaming means renaming — git mv, or the
                   equivalent"; "never delete it"; then, two paragraphs
                   later, "🔴 Delete the file once applied." Invocation
                   2 says of a bad partial report and of a block nobody
                   answered for: "is a blocker … say which, and stop" —
                   without saying whether the file is written.
    Le défaut    : Four things at once.
                   (a) After comments 3 and 4 no invocation-1 case
                   writes it, and the invocation-2 cases (a partial
                   report missing or malformed, a block no group
                   answered for) are grouping or run faults the
                   orchestrator fixes by re-running a group — not a
                   `## Decision` the Product Owner takes.
                   (b) Plane 2 Q2: the agent's tools are Read, Grep,
                   Glob, Edit, Write. It has no Bash and no rename. It
                   cannot `git mv`; with Write it can only create the
                   numbered copy and leave the original — exactly what
                   the rule forbids.
                   (c) Two passages asking different things: "never
                   delete it" and "Delete the file once applied", in
                   the same section.
                   (d) Plane 2 Q3: the command issues every group at
                   once; one shared file name means two groups blocking
                   in one run overwrite each other, and on resume every
                   group's invocation reads the same file and would try
                   to apply and rename it.
    Ce qu'il faut: Either the mechanism goes — the agent stops and says
                   what it found missing, the command relays it, and a
                   re-run of `/9_controle` after the fix is the way
                   back — or, if a `## Decision` channel is wanted for
                   this agent, it must be one the agent can operate:
                   one file per group, a closing gesture the tool set
                   allows (or Bash granted), one instruction on what
                   happens to the file, and a named list of decisions
                   the Product Owner can actually write there. If it
                   goes, `8_code`'s row "`code/blocked_<agent>.md` for
                   the Contrôleur" goes with it.
    Justification: Round trips first — a stop that waits on a hand-
                   written decision nobody can meaningfully write is a
                   run lost; robustness — a rename that cannot be done
                   leaves a file the next run reads as a standing
                   block; tokens — two sections read at every one of
                   the N+1 invocations for a path never taken.

---

### 6

    Fichier      : .claude/agents/controleur.md — and
                   .claude/commands/9_controle.md for the prompt
    Cible        : Invocation 2 — "Read every `code/controle/*.md`, and
                   nothing else" and "A block missing from every partial
                   report is a blocker — say which, and stop"; the
                   assembly prompt in the command
    Aujourd'hui  : Invocation 2 reads only the partial reports. Nothing
                   tells it how many groups ran nor which blocks exist.
    Le défaut    : Plane 2 Q2 — a move resting on a fact nothing gives
                   it. From the partials alone it can notice a gap in
                   the numbering (B7 absent between B6 and B8) and
                   nothing else: the last blocks of the feature, or an
                   entire group whose invocation wrote no file, are
                   invisible. "A block nobody answered for is worse than
                   a block reported missing" — and it is the one case
                   the move cannot see.
    Ce qu'il faut: The assembly must hold the full list of blocks and
                   know which groups were expected. The command already
                   builds `tracabilite-full.md` — one line per block, in
                   block order — and prints the `G<n>` lines: the
                   assembly prompt names the block list to check against
                   (that file, or the list inline) and the number or
                   names of groups. Each partial report opens with the
                   blocks its group was given, so a group that ran and
                   answered for none of them is told apart from a group
                   that did not run.
    Justification: Robustness. A block no group answered for passes
                   silently into a report whose empty Missing field
                   reads as "the chain held".

---

### 7

    Fichier      : .claude/commands/9_controle.md (and the agent's
                   Invocation 1 "What you write" if the fix is on that
                   side)
    Cible        : Phase 3, before issuing the groups; Invocation 2's
                   "Read every `code/controle/*.md`"
    Aujourd'hui  : Nothing clears or dates `code/controle/`. The command
                   commits the feature folder before every run, so a
                   first run's partials persist. The report is numbered
                   (`-02`, `-03`) precisely so two runs can be compared;
                   the partials are not.
    Le défaut    : Plane 2 Q1 for Invocation 2 — it reads more than it
                   claims. On a second run with a different grouping
                   (the script picks the budget; sheets changed; the
                   number of groups changes), `G1..G3` are overwritten
                   and `G4`, `G5` from the first run survive. The
                   assembly gathers both states, "changes no line", and
                   the report carries lines about sheets that no longer
                   say that.
    Ce qu'il faut: A run's assembly reads only that run's partials.
                   Either the command empties `code/controle/` before
                   issuing the groups, or the partials carry the run
                   (the report number the assembly will take, or the
                   group list the command passes — see comment 6) and
                   the assembly reads those alone.
    Justification: Robustness — stale lines in the report; and round
                   trips — a Product Owner comparing two reports
                   comparing a mixed state to a clean one.

---

### 8

    Fichier      : .claude/commands/9_controle.md
    Cible        : Phase 3, the invocation-1 prompt
    Aujourd'hui  : "Feature folder: docs/features/<name>/. Invocation 1
                   — Confront. Blocks: B15, B53, B54, B56. Sheets:
                   code/lot-29, code/lot-43, code/lot-44." The group
                   name appears only in `description` ("control G1"),
                   which the agent does not see.
    Le défaut    : Command question 2 (does the prompt carry what the
                   agent needs), and Plane 2 Q4: the agent writes
                   `code/controle/<group>.md`, "the group name the
                   prompt gave you" — a placeholder with nothing filling
                   it. The agent invents a name; two groups can invent
                   the same one and overwrite each other, which then
                   surfaces as blocks nobody answered for (comment 6).
    Ce qu'il faut: The prompt names the group — the `G<n>` the script
                   printed — and the agent's file rule points at that.
    Justification: Robustness (a lost partial), then round trips (a
                   stopped assembly for a naming collision).

---

### 9

    Fichier      : .claude/commands/9_controle.md
    Cible        : "What you read"
    Aujourd'hui  : "Only whether `desc-produit.md` is there, and whether
                   every lot of `code/sequence.md` carries a `verdict.md`
                   in PASS. ⚠️ Nothing else." Then Phase 1: grep
                   `tracabilite.md` and the `Anchor:` fields of
                   `code/decoupage.md`, cross them, write
                   `tracabilite-full.md`.
    Le défaut    : Two passages of one file asking different things.
                   An orchestrator that obeys "nothing else" cannot run
                   Phase 1; one that runs Phase 1 has broken the reading
                   rule and no longer knows which other rule holds.
    Ce qu'il faut: The reading list names what Phase 1 reads —
                   `tracabilite.md` and the `Anchor:` lines of
                   `code/decoupage.md`, by grep, nothing more of either.
    Justification: Round trips — an orchestrator stopping to ask which
                   sentence wins, or reading more than the two greps
                   because the boundary is already broken.

---

### 10

    Fichier      : .claude/commands/9_controle.md
    Cible        : Phase 1 — "Two greps and a crossing, no agent"
    Aujourd'hui  : The orchestrator builds `tracabilite-full.md` by
                   hand: one line per block, the lots that build its
                   entries, deduplicated; "Every block appears". The
                   script then parses that file. No check is stated
                   that the crossing is complete.
    Le défaut    : Plane 2 Q1 and Q3 on the command's own move. The
                   crossing is a mechanical join done by a reader that
                   does not code, over as many lines as the feature has
                   blocks, and its failure mode — a block dropped, a
                   lot missed on a line — is silent: the dropped block
                   reaches no group, and the assembly (comment 6, as
                   written today) cannot see it; the missed lot makes
                   the group report an intention Missing that a sheet
                   outside the group carries. Nothing verifies the
                   output against its inputs before the script runs.
    Ce qu'il faut: The crossing is verified or not done by hand: either
                   the script (or a sibling of it) performs the join
                   from the two source files, or Phase 1 ends with a
                   check that every block identifier of `tracabilite.md`
                   is on a line of `tracabilite-full.md` and every lot
                   of `code/decoupage.md` appears at least once. I could
                   not read `grouper.py` (outside this pass) and do not
                   know what it already checks; the command says nothing
                   of a check either way.
    Justification: Robustness — a block that reaches no group is the
                   one gap the whole command exists to prevent; and
                   round trips — a false Missing sends a lot into a
                   correction cycle for nothing.

---

### 11

    Fichier      : .claude/commands/9_controle.md
    Cible        : "What you relay", and "Git, in this mode"
    Aujourd'hui  : Relay: "The agent's own report, and the name of the
                   file it wrote." Git: "Enter the worktree before
                   invoking the agent … Then, once the agent reports:
                   merge, push, remove."
    Le défaut    : Command question 1 — outcomes with no row. The agent
                   can end a run in three ways: the report; a stop with
                   a message (bug-fix invocation, sheet named and
                   absent, block nobody answered for — today "a
                   blocker"); and, as written today, a
                   `blocked_controleur.md`. Only the first has a row.
                   Nothing says what the Product Owner runs after a
                   stopped assembly (re-issue which group? re-run the
                   command?). And "once the agent reports" is one agent
                   in a run of N+1: whether the merge comes after each
                   group or after the assembly, and whether Phase 1's
                   file is written before or after the pre-control
                   commit, is left to the reader.
    Ce qu'il faut: One row per outcome: the report and its file name;
                   a stop, relayed verbatim with what is missing, and
                   what re-running the command will do about it (a
                   re-run rebuilds the groups and starts over — say so,
                   or say that the stopped group alone is reissued). One
                   worktree for the run, merged once after the assembly;
                   Phase 1's file written before the pre-control commit
                   so the run's input is in the record.
    Justification: Round trips — a Product Owner "on her own" on a
                   stop, and an orchestrator choosing a merge point;
                   tokens — a re-run from scratch where one group would
                   have done, if the row says nothing.

---

### 12

    Fichier      : .claude/commands/9_controle.md and
                   .claude/commands/8_code.md
    Cible        : 9_controle "When it runs" (first paragraph); 8_code
                   lines 12-14, 56-58, 132-138, 239-242, 249
    Aujourd'hui  : 9_controle: "`/8_code` runs the Contrôleur on its
                   own, once the last lot passes. This command is for
                   running him again." 8_code: "It never invokes the
                   Contrôleur — he needs his blocks and his sheets named
                   in the prompt, and the grouping that names them lives
                   in `/9_controle`" (12-14); "No such lot … go straight
                   to the Contrôleur, then stop" (56-58); "say that
                   `/9_controle` is what comes next — run by hand"
                   (135-136); "The Contrôleur has finished — the gap
                   report is to be read" as a stop condition (249);
                   and "the Contrôleur reports missing intentions after
                   every lot is reviewed, and a block is how they come
                   back" — a filled `## Decision` naming an agent and a
                   lot (239-242).
    Le défaut    : Command question 1 on both files. Four passages
                   disagree on who runs the Contrôleur: 9_controle says
                   8_code does; 8_code says it never does, then says go
                   straight to him, then says run 9_controle by hand,
                   then lists his finishing as one of its own stops. And
                   two routes for a missing intention: the agent and
                   9_controle send it to the report and a bug-list for a
                   correction cycle; 8_code line 239-242 sends it back as
                   a blocking file whose `## Decision` names a lot. An
                   orchestrator following 56-58 invokes an agent that
                   cannot start without a grouping it does not have.
    Ce qu'il faut: One owner. Everything in the agent points to
                   9_controle owning the grouping and the run; then
                   9_controle's first paragraph, 8_code 56-58 and 249 say
                   the same thing as 8_code 12-14 and 135-136. And one
                   route for a missing intention — the report, since
                   that is what the agent produces — so 8_code 239-242
                   either goes or names a mechanism the Contrôleur
                   actually has. I lean to the report route because the
                   agent, its command and its never-do list all state
                   it; the 8_code passage reads as an earlier design.
    Justification: Round trips — an invocation that cannot run, or a
                   Product Owner told two different next steps.

---

### 13

    Fichier      : .claude/agents/controleur.md
    Cible        : Invocation 2 as a whole
    Aujourd'hui  : An invocation of the agent reads N partial files,
                   orders their lines by block, concatenates them under
                   three headings, checks coverage, and "changes no
                   line".
    Le défaut    : Plane 1 — is there a move that could go. Every step
                   of Invocation 2 is mechanical: sort, concatenate,
                   compare against a list, pick a free file name. What
                   breaks if the agent stops doing it: nothing, provided
                   something else does. What is at risk while the agent
                   does it: "changes no line" is asked of a reader that
                   reproduces text approximately — a dropped or reworded
                   line in a 200-line copy is silent and is the kind of
                   error a script does not make.
    Ce qu'il faut: The assembly is a script beside `grouper.py`, given
                   the block list and the partials, or stays an agent
                   invocation only if something verifies the report
                   against the partials afterwards (every partial line
                   present once). I am not sure of this one: it changes
                   the shape of the command, and comments 6 and 7 fold
                   into it if it is taken. Written so that it can be
                   declined without touching the rest.
    Justification: Robustness (an exact copy), then tokens (one Sonnet
                   invocation and its whole context per run, for a
                   join).

---

### 14

    Fichier      : .claude/agents/controleur.md
    Cible        : "What you never do" — entries "Relaunch anything" and
                   "Report a lot as failed"; "When `Edit` fails"; the
                   never-do entries and sentences about files the agent
                   never reaches ("Never `idees.md` — the raw text the
                   upstream chain spent its whole loop correcting",
                   "Never the technical document, the lot list or the
                   sequence"); "The Cadreur merges lots that build one
                   thing, so a single sheet can answer for a whole
                   screen"
    Aujourd'hui  : As quoted.
    Le défaut    : Known list — a forbidden thing nothing in the body
                   asks for; Plane 2 Q2 — a read no move uses; Plane 3,
                   criteria 3 and 5. The agent has no tool to relaunch
                   anything and no field to report a lot as failed. No
                   move uses `Edit`: both invocations write fresh files,
                   and the only edit-like act (the rename of comment 5)
                   is not an edit. The agent opens only what its prompt
                   names, so forbidding named files it would never open
                   guards nothing; and the two justifications explain
                   other agents' behaviour to a reader who has not seen
                   them.
    Ce qu'il faut: The never-do list keeps the entries the body can
                   violate (read the code, open an earlier report, read
                   outside the group, re-judge, settle a doubt, answer
                   for a whole block). The `Edit` section goes with
                   `Edit` from the tool line unless a move needs it. The
                   two justifications and the two "never this file"
                   lines go; the reading rule "the blocks and sheets the
                   prompt names, and nothing else" already covers them.
    Justification: Tokens — read at every one of N+1 invocations; and,
                   for criterion 3, a shorter list is one the agent
                   actually checks itself against.

---

### 15

    Fichier      : .claude/agents/controleur.md
    Cible        : "The files, in the working folder you were given" and
                   every later "working folder"; the invocation table's
                   "Feature folder"
    Aujourd'hui  : The agent says "working folder" throughout; the
                   prompt the command sends says "Feature folder:
                   docs/features/<name>/."; the invocation table says
                   "the prompt says which one".
    Le défaut    : Plane 2 Q4 — a term used and never defined, and not
                   the word the prompt uses. A reader that has seen
                   nothing else finds "working folder" and a prompt
                   naming a "feature folder", and a `bugfix-NN/` may sit
                   inside that folder.
    Ce qu'il faut: One word, the prompt's, stated once: the folder the
                   prompt names is where `desc-produit.md` and `code/`
                   live, and never a sub-folder of it.
    Justification: Robustness — the one wrong turn (into a
                   `bugfix-NN/`) ends in "no product file" and a lost
                   run. Small, but it costs one line to close.

---

## From the verdict

Written after reading `docs/refonte/verdict.md`, section 2 (the
controleur's line) and sections 4 to 7, and after everything above.

    Section 2 — "Contrôleur — the role holds. Product → sheet, sentence
    by sentence, reading no code … It closes the chain on the product
    file, which is one step short of the idea."
    Not found as a comment, and it is not one on this agent: the agent
    says "Never `idees.md` — the raw text the upstream chain spent its
    whole loop correcting", so the verdict describes it exactly. A
    sentence lost at structuring is invisible to it by design; closing
    on the idea would be a different move, reading a different file,
    and belongs to whoever decides the chain's reading set — not to a
    correction of this file. One nuance the agent adds: "sentence by
    sentence" is the file's own phrase, and comment 2 says the unit is
    really the intention, of which the sentence is the usual cut.

    Sweep #7 / D2 — block identifiers are assumed stable; the
    Contrôleur addresses blocks by number through `/9_controle`'s map.
    Not found. The agent says nothing of stability: it takes `B15, B53`
    from its prompt, reads those blocks, and writes those numbers in its
    partials. Within the downstream the product file is frozen (the
    command: "a correction cycle has neither"; the map is built from
    `tracabilite.md` and `code/decoupage.md`, both written after
    closure), so a shift would have to happen upstream — where this
    agent cannot see it and where the verdict's item 6 sends it. On the
    agent's side there is nothing to correct; comment 6 (pass the block
    list explicitly) is what would make a shifted number visible at
    assembly rather than silent.

    Sweep #42 / D17 / section 7 item 13 — a settled blocking file is
    renamed by one agent and deleted by five; the process's
    contradiction 1.
    Already found — comment 5 (c). The precision the verdict could not
    have: this one file does both. "Renaming is what closes it — 🔴
    never delete it. 📌 The numbered ones are the record …" and, in the
    same section, two paragraphs down: "🔴 Delete the file once applied.
    A blocking file left behind would stop the next run on a question
    already settled." And neither can be executed: the agent has no
    Bash and no rename — comment 5 (b).

    Sweep #54 / D20 / section 7 item 18 — "`/8_code` invokes the
    Contrôleur without the groups it requires … As written, the
    end-of-cycle control either does not run or runs on a prompt the
    agent refuses"; "Does `/8_code` build the Contrôleur's groups, or
    call it without them?"
    Contradicted in part by the command, and the remainder already
    found — comment 12. `8_code` lines 12-14 say, verbatim: "📌 It never
    invokes the Contrôleur — 🔴 he needs his blocks and his sheets named
    in the prompt, and the grouping that names them lives in
    `/9_controle`", and lines 135-136 say to tell the Product Owner that
    `/9_controle` "is what comes next — run by hand". So neither of the
    verdict's two branches is what the command does: it neither builds
    the groups nor calls without them; it hands over. What survives of
    contradiction 3 is three leftover sentences that still say the old
    thing — `8_code` 56-58 ("go straight to the Contrôleur, then
    stop"), `8_code` 249 ("The Contrôleur has finished" as a stop of
    `/8_code`), and `9_controle`'s own first paragraph ("`/8_code` runs
    the Contrôleur on its own, once the last lot passes"). The closing
    check is a manual command, and the command says so in one place and
    denies it in three.

    Sweep #59 / D23 / section 5 U12 / section 7 item 14 — a correction
    cycle's sheets live in `bugfix-NN/code/`, where the Contrôleur never
    looks; a re-run of `/9_controle` "to compare two states" finds the
    corrected intentions still missing; U12 has no stop.
    Not found, and the verdict is right. What the agent says: "🔴 A
    feature cycle only. No `desc-produit.md` in the working folder means
    you were invoked on a bug-fix cycle: stop"; a sheet is
    "`code/<lot>/fiche-executable.md`" relative to the folder the
    prompt names. What the command says: "🔴 Always the feature folder
    itself, never a `bugfix-NN/`. The Contrôleur confronts the product
    file with the sheets built from it, and both live here — a
    correction cycle has neither"; Phase 1 crosses `tracabilite.md`
    with "the `Anchor:` fields of `code/decoupage.md`" — the feature's
    split only. So after a correction cycle built from this agent's own
    report, the second report repeats the first, by construction, and
    "that is how two states are compared" (the command, on the numbered
    reports) compares nothing. This deserves a comment of its own on
    `9_controle`, which I did not write before reading the verdict and
    add here as intent: the product file is the feature's — the agent's
    "feature cycle only" holds for that — but the sheets that carry its
    intentions can sit in the feature's `code/` and in every
    `bugfix-NN/code/` beneath it; Phase 1's map must take the `Anchor:`
    fields of every `decoupage.md` in the feature folder and its bug-fix
    sub-folders, and the group prompt must name sheets by a path that
    reaches them (`bugfix-02/code/lot-04`), which the agent's
    "`code/<lot>/fiche-executable.md`" table then has to allow.
    Measure: robustness — the second report is false; and round trips —
    the Product Owner reconciles the two reports by hand, or opens a
    correction cycle on intentions already built. Note the command's
    premise "a correction cycle has neither" is half true: it has no
    product file, and it has sheets.

    Section 5 U12 — "a second exit ('une décision remplie … même sur un
    lot qui porte déjà un PASS') whose producer — who writes a blocking
    file from a control report — is not named."
    Already found — comment 12, on `8_code` 239-242. The agent confirms
    that nobody writes it: "⚠️ Blocking is not reporting a gap. A
    missing intention, a doubt: those are the report, and they are what
    you are for" and "Relaunch anything — the Product Owner reads the
    report and decides whether it becomes a gap file for the bug-fix
    cycle". The `8_code` sentence names a route that has no producer in
    the agent it attributes it to.

    Section 6 P7 — the chain produces evidence of grid holes, "Contrôleur
    *douteux*" among them, and writes none of it where the grid would
    read it.
    Not found, and not a correction to this agent as bounded: doubts go
    to `## Doubts` of the partial and of the report, read by the
    assembly and the Product Owner, and nothing else. Whether a doubt
    that says "the block names no observable" should also reach the
    grid is a chain decision; the agent's side would be one line in the
    doubt's shape (why it is a doubt — comment 1's boundary gives the
    two reasons) so that a later reader can sort them.

    Section 6 P9 — "the Contrôleur that never reads its own previous
    report" as an instance of fresh-eyes independence.
    Confirmed by the agent: "⚠️ You never open one either. Its content
    would tell you what an earlier run concluded, and you would stop
    looking." Nothing to add; comment 7 keeps that independence and
    closes the one place it leaks (stale partials from the earlier run).

    Section 6 P13 — the Contrôleur reads all sheets against all blocks
    "in groups, by script"; a context that runs out fails by silent
    truncation, not by a block.
    Already found as an open question — "Does one group fit one
    context?" below. The agent has no rule for a group whose sheets do
    not fit, and the command says the script "sweeps every budget and
    picks one" without saying what the budget measures.

---

## What another agent would settle

    Does the group's set of sheets contain every sheet that can carry a
    block's intention?
    The cadreur's file (how the `Anchor:` fields of `code/decoupage.md`
    are written — by entry, and whether an entry's join to another
    block's screen is cited by the lot that builds the join) and the
    convertisseur's (whether an intention that joins two blocks is
    written as an entry of the block that names the trigger).
    If yes, "Missing" in a group's partial report is feature-wide and
    the design holds. If no, a Missing line can be a sheet in another
    group, and the report needs either a feature-wide second look on
    Missing lines or a wording that says "absent from the sheets its
    traceability points to" — and comment 1's boundary would need a
    fourth outcome for "carried by a sheet outside the group".

    Can a lot of the sequence carry a PASS verdict with no
    `fiche-executable.md` in its folder?
    The relecteur's file (what PASS requires) and the realisateur's
    (whether it ever removes or renames a sheet), and `8_code`'s
    redécoupage rule (it deletes the sheets of uncoded lots — but does
    the new `decoupage.md` still cite a lot whose folder is now empty?).
    If never, the "folder with no sheet → doubt" rule of comment 4 is a
    net and could go entirely. If it can, the doubt rule stays and the
    command's PASS guard is not sufficient.

    What does a block look like in `desc-produit.md`, and what bounds
    it?
    The redacteur's file (the block heading format, whether a block ends
    at the next heading, whether split blocks are renumbered or
    suffixed) and the decoupeur's.
    If blocks are `B<n>` headings ending at the next heading and
    numbering is contiguous, "read only the blocks your group names" is
    a grep away and Invocation 2's "block order" is numeric. If splits
    leave gaps or suffixes, the assembly's ordering and any
    gap-in-numbering reasoning (comment 6) need the block list passed
    explicitly, which comment 6 asks for anyway.

    Does one group fit one context?
    Not an agent file — `grouper.py`'s budget. If the budget is set
    against sheet size in tokens, the agent holds its group. If it
    counts lots, a group of long sheets degrades the confrontation in
    silence, and the agent has no rule for "my sheets do not fit".

    Is the `## Decision` route of `8_code` 239-242 a design that still
    stands?
    No agent file settles it — the arbitre's and the detailleur's would
    say whether a Decision can name "detail lot-NN again", but the
    controleur never writes such a file. If it stands, comment 5's
    second branch (a channel the agent can operate) is the one to take;
    if not, the first.
