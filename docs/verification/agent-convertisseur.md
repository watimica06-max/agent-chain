# agent-convertisseur — verification

**Read**: `.claude/agents/convertisseur.md` (old, 542 lines) ·
`.claude-new/agents/convertisseur.md` (new, 693 lines) ·
`docs/refonte/passes/convertisseur.md` (20 comments, `### c.1` … `### c.20`) ·
`docs/refonte/modifications.md` § `` # `convertisseur.md` `` (lines 539–628).
Also opened, because the section's demands and six of its passed comments land
there: `.claude/commands/6_convertit.md` and `.claude-new/commands/6_convertit.md`
(diffed), `.claude-new/commands/5_reclasse.md` lines 25–160 (what `par-genre/`
holds and who reads each file), and a grep of the new tree for `technique-`,
`par-genre`, `tracabilite.md`.

**What the section says**: three structural demands — (1) receive the three
`par-genre/` files (transverses to every nature invocation; references to the
transversal, for §9 Text; hors-périmètre to the transversal, for the preamble);
(2) a transverse rule splits in two, a numbered entry for the shared code and a
preamble constraint; (3) a second questions file, technical, named outside the
`questions-*.md` pattern, with the reversibility test as its frontier. Pass
sheet: **Passés (19)** c.1–c.9, c.11–c.20 — **Écartés (1)** c.10 —
**Partiellement passés (0)**.

c.14 to c.19 target `.claude/commands/6_convertit.md`, not the agent. They are
verified against `.claude-new/commands/6_convertit.md` since the pass sheet
lists them as passed. Line numbers below are those of the **new agent file**
unless marked *old* or *cmd*.

---

## A. Conformity

### Structural demands (modifications.md, "La demande")

| # | Expected | Found | Verdict |
|---|---|---|---|
| 1 — transverses to every nature invocation | Each nature invocation reads `par-genre/transverses.md` and draws entries and preamble lines from it | Line 51 adds the row *"the transverse rules — `par-genre/transverses.md`"* to the path table. **Nothing else names the file**: PART 2 line 539 still reads *"Your blocks · the headings · the grid"*, and line 545 says *"Read only what your invocation lists"*. Invocation 1 moves 1–3 (562–603) are unchanged — move 1 reads *"your blocks"*, move 2 writes entries *"in the order of your blocks"*, move 3's `## Preamble` still says *"what your blocks give the preamble — a cross-cutting rule"* (601–602), which after the genre split a behaviour block no longer carries. | **BLOCKING — declared in the table, not wired into any read or move.** An agent obeying line 545 never opens the file. See D-1, D-2. |
| 1 — references to the transversal, §9 Text | `par-genre/references.md` is the source of §9 Text (modifications.md: *"Le fichier des références lui donne sa source"*) | Line 52: row *"the references — catalogues and tables of formats · invocation 2 only"*. Line 90–92 unchanged: §9 Text is *"written at invocation 2, by the grid's Resources"* from wordings quoted in blocks. PART 2 line 540 does not list it; no move of invocation 2 (618–692) mentions it. | **BLOCKING — not applied beyond the path row.** The Text section keeps its old source; the catalogue is named and never read. |
| 1 — hors-périmètre to the transversal, preamble | The preamble's *Out of scope* comes from `par-genre/hors-perimetre.md` | Line 53 (path row, *"invocation 2 only"*) and line 112 (preamble table: *"`par-genre/hors-perimetre.md`, whole"*). But invocation 2 move 2, line 620–622: *"from the product file's text outside the blocks and the notes' `## Preamble` lines, nothing deduced"* — unchanged, does not name the file. PART 2 line 540 does not list it. | **TO FIX — applied in the table, not in the move that writes the preamble.** Two sources for the same part; the move's wording wins at execution. |
| 2 — a transverse rule splits in two | Shared code → numbered entry; constraint → preamble; test *"if nobody writes it, does the code lack something?"* | Lines 133–156, new section *A transverse rule splits in two*: the two-row table (140–143), the dash-formatter example (145–148), the two "without" sentences (150–152), the test (138). | **Conforming on the text asked** — but the entry's placement *"in the section of its layer"* (142) has no author: see **D-1**. |
| 3 — a technical questions file | A second file, name outside `questions-*.md`; reversibility frontier; *tranche* / *pose* table; answer applied at the section's rewrite, written nowhere | Lines 286–329, new section *Two kinds of question*: `convertisseur/technique-<nature>.md` (59, 294 — outside the pattern), the reversibility rule (302–306), the settle/ask table (308–311), *"The answer is not written anywhere afterwards — it is applied when the section is written again"* (328–329). Path row 59. | **Applied to the letter — but the route it opens leads nowhere**: see **D-3, D-4, D-5**, and the cross-file note under c.20. |

### Comments listed PASSÉ

| # | Expected (pass file, *Ce qu'il faut*) | Found | Verdict |
|---|---|---|---|
| c.1 | The "can I write this rule at all?" decision is taken at the entry, in move 2; a "No" ends the section there — no section, no notes, the question written; move 4 stays the sweep over a written section; whether notes exist after a "No" is stated | Lines 372–373: *"You meet that question while you write the entry, not after"*. Line 377 (the "No" row): *"Stop there: no section, no notes, the question written. You never write a section you will delete, and never leave notes naming entries that do not exist."* The old *"delete yours if one is there"* is gone. Move 4 (605–607) unchanged. Command: cmd 183–184 still checks notes *"when it wrote its section"* — one meaning now. | **Conforming.** Note: the moves themselves (565–578) were not touched; the rule lives only in *What a question costs*, which move 4 cites and move 2 does not. NOTE. |
| c.2 | One reading: the rule is left out of the section, the section is marked provisional the way an assumption is; the question asks what the rule does, not which layer | Lines 411–424: *"never an entry, neither here nor elsewhere"*; *"You leave it out of your section, and you mark the section the way an assumption is marked"* with the `<<ASSUMED B40: …>>` example (418–419); *"Ask what the rule does, not which layer it belongs to"* (421). | **Conforming** — but contradicted by line 310 (*"You settle … putting a rule in one section rather than another"*): see **D-6, BLOCKING**. And the example wraps over two lines against line 380: see **D-8**. |
| c.3 | A title not in the headings is written in a form the `[B` grep catches (title, no identifier), and it is a "Yes"-kind question | Lines 261–269: *"write the reference so the grep still catches it, with the title and no identifier: `[B?: the weigh-in screen]`"*; *"Never a bare description in the prose"*; *"And it is a question, the kind that still lets you write the entry."* | **Conforming** — but invocation 2 then misreads it: see **D-9**. |
| c.4 | A bracket reference and an `<<ASSUMED …>>` mark each sit on one line, however long | Lines 380–383: *"A bracket reference and an `<<ASSUMED …>>` mark each sit on one line, however long. The command resolves them by script, and a closing `]` or `>>` on the next line is a reference half-replaced, or not replaced at all."* | **Rule conforming; both examples in the file still wrap** — lines 388–389 (the very example the comment cited) and the new one at 418–419. **TO FIX**, see **D-8**. |
| c.5 | The file states the form it looks for, for the cross-cutting block and for the *existing* reference — or says where the product file's legend sits | Cross-cutting: solved by the genre split — line 113 *"The constraint half of each block of `par-genre/transverses.md`"*, line 116–117 *"You recognise none of those by their wording — the split already sorted them, and each has its own file."* *Existing*: line 114 *"The references marked existing"*, line 271–272 *"A reference marked existing is neither — it goes to your notes"*, line 601–602 — **the form of the mark is still nowhere**, and line 116's *"each has its own file"* is false for it. | **Half applied — TO FIX.** The pass sheet lists it as passed; the *existing* half of the comment is untouched, and the sentence written for the other half now misstates it. See **D-10**. |
| c.6 | Brackets move 3 cannot resolve are the input of move 4's *Resources*; only what *Resources* cannot write is a question; the bracket is then replaced by the new number; the final grep stays last | Lines 632–645: *"When none of them carries it, in this order: 1. … 2. Hold it for move 4. Resources writes the entry when the product settled its content — and then you replace the brackets with the number it gave. 3. Only what move 4 could not write is a question — leave the brackets."* Line 651: *"Then, after move 4, grep `[B`"*. | **Conforming.** |
| c.7 | Before asking, move 3 reads the block's `## Preamble` line; a cross-cutting rule or *existing* reference resolves to the preamble in whatever form the `Consumes:` reader accepts; "no line at all" is named and treated as an invocation-1 fault | Lines 634–636: *"1. Read the block's `## Preamble` line. A cross-cutting rule or a reference marked existing resolved to the preamble — it has no number: the reference names the preamble part that holds it."* Lines 647–649: *"A block with neither a `## Trace` entry nor a `## Preamble` line — that is a fault of invocation 1, not a product question: say so in your report, and leave the brackets."* | **Conforming** — with one open point: what a `Consumes:` line that "names the preamble part" looks like (`Consumes: Cross-cutting rules`?) is not shown, and the Architecte reads that line as a graph (line 34). Question, see **D-11**. |
| c.8 | A fixed preamble shape: one heading per part, fixed order, distinguishable from `## §n` at a glance, each part written empty when nothing fills it | Lines 119–131: `# Preamble` then `## Intent and vocabulary` / `## Out of scope` / `## Cross-cutting rules` / `## Dependencies`, *"A part with nothing in it is written empty, never omitted"*, *"`# Preamble` is one `#`, the sections are `## §n`"*. Four parts announced, four listed, four rows in the table (109–114). | **Conforming.** |
| c.9 | "Say which of the two you are in" has one destination: the report; the entry stays four lines | Lines 395–398: *"Say which of the two you are in — in your report, never in the entry. An entry is four lines, and a fifth breaks the shape every reader after you depends on."* | **Conforming** — but *What you report* (436–444) was not amended to carry it: see **D-12**. |
| c.11 | Both body prohibitions mirrored in *What you never do*: never write a number outside your own section; never rewrite a rule another invocation wrote | Lines 503–507: both bullets, each with its reason. | **Conforming.** Cosmetic: the blank line at 508 splits the list in two. NOTE. |
| c.12 | One rule, stated in agent and command: a blocking file ends the invocation and nothing else is written (or the reverse) | Lines 454–460: *"A blocking file ends your invocation. Nothing else of it is written — no section, no notes, no questions file, not even an empty one."* Command side: cmd 171–174 greps for a new `blocked_*.md` first and reports it *"blocked, not missing"*. | **Conforming**, both sides. |
| c.13 | The path table says its base (the feature folder) and the one row that departs says so | Lines 44–46: *"Every path below is relative to the feature folder the prompt names, except the grid, which is relative to the repository root — its row says so."* Line 62: the grid row carries *"from the repository root, not the feature folder"*. | **Conforming.** |
| c.14 (cmd) | Right after the invocations return, grep for a new unnumbered `blocked_*.md`; a blocked nature reported as blocked; every stop after entering the worktree still merges, pushes, removes | cmd 171–174 (the grep, *"never go no further"*), cmd 176–180 (*"Every stop from here on merges first … Merge, push, remove the worktree, then report"*). **But cmd 182–186, the very next paragraph, still ends *"A missing one stops the command — say which nature and which file, and go no further."*** | **Applied, with a residual contradiction two lines below it — TO FIX (cmd).** Whether "every stop from here on merges first" overrides the older sentence is left to the reader. |
| c.15 (cmd) | An unchanged input with an `<<ASSUMED` mark or no section *waits*; a fourth relay state; "document stands" not met while a nature waits | cmd 124–126: the two rows gain *"and its part changed"*, plus the row *"Either of the two, and its part is byte-identical — Waits — it does not run"*; cmd 130–131: *"A nature that waits is a third state, beside ran and kept — and the document does not stand while one waits."* | **Conforming** — except that the *No nature runs* row (cmd 148) that actually says "the document stands" was not given the "no nature waits" condition, and *What you relay* (cmd 324–325) still relays *"which natures ran, which were kept"* only. TO FIX (cmd), minor. |
| c.16 (cmd) | Post-check of invocation 2 greps `[B`; empty questions file + leftover `[B` is a fault, invocation 2 rerun once | cmd 261–265, word for word. | **Conforming.** |
| c.17 (cmd) | One row for blocking file + questions, saying the order | cmd 333: *"Answer the questions first, then fill the decision, then `/6_convertit`"*. | **Conforming.** Cosmetic but real: the paragraph inserted at cmd 337–339 sits *inside* the table and detaches its last row (cmd 340) — that row no longer renders as part of the table. TO FIX (cmd). |
| c.18 (cmd) | Post-check compares the headings' block identifiers with the first column of `tracabilite.md` | cmd 267–271. | **Conforming** — see D-2 for what it will now flag on every transverse block. |
| c.19 (cmd) | The three *(Seen once …)* / *(Measured …)* parentheticals go; the one fact of "part not markers" stays | cmd 90–92, 100–101, 103–105: parentheticals gone. cmd 135–138: the markers paragraph kept, now two sentences. | **Conforming.** |
| c.20 | The file distinguishes product from technical questions; a naming divergence between sections is settled by invocation 2 within its "reference, not rule" allowance, or goes to an agent that accepts a technical request, by a file that agent reads | Lines 286–329. Line 310: *"two sections naming one entity two ways — a name is a reference, not a rule"* under *You settle*. Line 294: the technical file. Line 297–298: *"A technical one comes back to you, and to nobody else."* | **Applied — but the second half of the ask ("by a file that agent reads") resolves to the Convertisseur itself, and the Convertisseur is forbidden to open any questions file (516–517).** BLOCKING, see **D-3**. Cross-file: `technique-` appears in **no other file** of the new tree — the command neither moves, merges, counts, nor names `technique-*.md` (its relay rows cmd 334–335 speak of technical questions, its *The questions* section cmd 277–288 merges `questions-*` only), and a technical answer changes no block, so the part stays byte-identical and cmd 124–128 never reruns the nature that must "apply it when the section is written again". The short loop the command announces (cmd 334) cannot close. |

### Comment listed ÉCARTÉ

| # | Expected | Found | Verdict |
|---|---|---|---|
| c.10 | NOT applied: the grid is still loaded whole | Line 405–406 unchanged: *"Load the grid; it is not in this file."* PART 2 lines 539–540: *"the grid"* whole. No heading-located read. | **Correctly not applied.** |

---

## B. Unannounced changes

Every hunk of the diff was matched against the pass file and the demands.
What remains:

| # | Line(s) | Old | New | What it changes |
|---|---|---|---|---|
| B-1 | 50 | *"the blocks of your nature"* | *"the **behaviour** blocks of your nature"* | Follows from demand 1 (only behaviours have a nature). Consistent with cmd/5_reclasse. NOTE. |
| B-2 | 106–107 | *"Entirely taken from the product file, nothing deduced"* | *"Entirely taken from **what the command gives you**, nothing deduced"* | Consequence of demand 1. Slightly inaccurate: the command's prompt gives the feature folder and nothing else (cmd 163–165); the files are found by the agent through the path table. NOTE. |
| B-3 | old 107–109, removed | *"A cross-cutting rule constrains without producing anything. A set of values the code has to write somewhere produces, even when the whole document references it."* | (gone; replaced by *A transverse rule splits in two*) | The removed sentence would have contradicted demand 2 ("gives two things"); removing it is coherent. Not listed in the table of changes. NOTE. |
| B-4 | 154–156 | — | *"A transverse rule that gives no code at all gives only the constraint — and that is the common case for a rule about naming, or about what the product refuses."* | New rule, not in demand 2 (which lists two outputs with no "none" case). Sensible, but it contradicts 135–136 as written: see **D-7**. |
| B-5 | 158–160 | *"The test: if nobody writes it, is something missing from the code? Yes → it is a numbered entry …"* (kept) | same, now immediately after line 138 *"Ask of it: if nobody writes it, does the code lack something?"* | The same test stated twice, eight lines apart, in two wordings. NOTE. |
| B-6 | 313–314 | — | *"Say the decision you settled, in your report — never in the document."* | New reporting obligation; c.20 asked that invocation 2 settle, not that it report. *What you report* (438) was not amended. See **D-12**. |
| B-7 | 632–645 | one paragraph | *"When none of them carries it, in this order:"* + sub-steps **1. 2. 3.** inside move 3 | c.6/c.7 asked for the order, not the form. The sub-steps reuse the moves' own numerals (*"2. Hold it for move 4"* sits under *"3. Resolve …"*). Readable, but a second numbering inside the first. NOTE. |
| B-8 | 508 | — | blank line | Splits *What you never do* into two bullet lists. Cosmetic. NOTE. |
| B-9 | 330 | `---` before `## Your questions` | none — *Two kinds of question* runs straight into *Your questions* | Every other `##` of PART 1 is preceded by a rule; this one is not. Cosmetic. NOTE. |

No renumbering, no moved section, no rewritten table beyond those tied to the
demands and comments above. PART 2 and every move of PART 3 that the demands
should have touched are byte-identical to the old file except invocation 2
move 3 (c.6/c.7).

---

## C. Gestures against tools

**Frontmatter** (line 4): `Read, Grep, Glob, Edit, Write`. Unchanged from old.

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Read blocks, notes, the technical document, the grid, the product file's text outside blocks, the three `par-genre/` files | 562, 618, 405, 620, 51–53 | Read | has it |
| Grep the headings (`#` lines) for an identifier by title | 55, 258–259 | Grep | has it |
| Grep `[B` in the document after move 4 | 651 | Grep | has it |
| Enumerate `convertisseur/*-notes.md` at invocation 2 | 540, 618 | Glob (or Grep) | has it |
| Write section, notes, product questions, technical questions, blocking file, `tracabilite.md`, whole each time | 565, 577, 580, 609, 294, 450, 672 | Write | has it |
| Insert the preamble before `## §1` in `spec-technique.md` | 620 | Edit | has it |
| Replace brackets by a number in place; append a *Resources* entry at a section's end, in place of `*(empty)*`; add a number on other entries' `Consumes:` lines | 628–630, 638–640, 658–662 | Edit | has it |
| Recovery when `Edit` fails | 525–531 | Read + Edit | has it |
| Delete a section or notes | — | (none) | **No longer needed**: the old *"delete yours if one is there"* is gone (c.1) and a blocking file writes nothing (454–456). Good — the agent never had a delete tool. |
| Mark a section provisional for an other-layer rule | 414–419 | Write (inline) | has it — where in the section the mark sits is not said, see D-13 |

**Tools no gesture uses**: none. `Glob` has one use (the notes files); `Grep` two;
the rest carry the work.

**Gestures whose tool is fine but whose trigger is missing**: reading the three
`par-genre/` files (A, demand 1) — the tool exists, the instruction to use it on
those files does not.

---

## D. Internal coherence (new file alone)

| # | Line(s) | Quote | Finding | Severity |
|---|---|---|---|---|
| D-1 | 51, 142 vs 74–76, 539, 545 | *"the transverse rules — `par-genre/transverses.md`"* · *"A numbered entry, in the section of its layer"* vs *"A block's nature is on its `Nature:` line — the classeur wrote it; read it, never derive it again"* · PART 2 inv. 1 reads *"Your blocks · the headings · the grid"* · *"Read only what your invocation lists"* | The transverse rules are in the path table and nowhere else. If the eight nature invocations each read the file (as `/5_reclasse` says they do), each must decide *by itself* whether the shared-code half belongs to its layer — a transverse block carries an empty `Nature:` (cmd/5_reclasse: *"only a behaviour has one"*), so the agent would derive a nature, which line 75–76 forbids. Nothing says which invocation writes the entry, so a formatter can be written by zero natures or by two. If instead PART 2 is obeyed, nobody opens the file and demand 1 and 2 are dead letters. | **BLOCKING** |
| D-2 | 592–593, 679–684 vs 51 | *"`## Trace`: one line per block of yours"* · *"One line per block, in the product file's order — the headings give it … Every block appears"* | A transverse block is not "of yours" (the input file holds behaviour blocks only, line 50), so no `## Trace` line names the entry it gave. `tracabilite.md` must list every heading of `desc-produit.md`, transverse blocks included; the agent has no line to copy for them, and the command's new post-check (cmd 267–271) will report each one as *"a fault of the run"*. Likewise a `[B20: the dash formatter]` reference to a transverse block finds no Trace line and, by 634–636, resolves to the preamble instead of to the entry. | **BLOCKING** |
| D-3 | 297–298 vs 516–517, 365–366 | *"A technical one comes back to you, and to nobody else."* vs *"Open `idees.md`, or any questions file — an answer reaches you through the product file"* · *"The answer is in the product file by the time you run again."* | The technical answer sits in `technique-<nature>.md` — a questions file the agent may never open — and by definition changes no block, so it never reaches the product file either. No route in the file brings it back. | **BLOCKING** |
| D-4 | 294 vs 311, 319–323, 510 | *"a choice the Product Owner cannot make"* vs *"You ask: Deciding that two concepts the Product Owner told apart are one — or the reverse"* and the `Answer:` line (323) *"where the Product Owner writes, by hand"* (353) · *"Settle a product matter, however trivial"* (never do) | The definition says the PO cannot make the choice; the one example of a choice to ask is a product distinction the PO made herself, and the shape leaves her an `Answer:` line. Who answers a technical question is not settled by the file. And merging two PO concepts is a product matter that the never-do list forbids the agent to settle, yet its answer *"comes back to you, and to nobody else"* — the Rédacteur never learns that the product file's two concepts became one in the technical document. | **TO FIX** — is the technical file answered by the PO, by the Architecte, or by nobody? |
| D-5 | 328–329 vs 385–393 | *"The answer is not written anywhere afterwards — it is applied when the section is written again."* | What causes the section to be written again is not said. Is an entry that waits on a technical question marked `<<ASSUMED`, like a product assumption (385–393), so that the command reruns the section? If not, nothing triggers the rewrite and the answer is never applied. | **TO FIX** |
| D-6 | 310 vs 411–424 | *"You settle: … putting a rule in one section rather than another"* vs *"A rule of your block that belongs to another section's layer — never an entry, neither here nor elsewhere. You leave it out of your section, and you mark the section … Ask what the rule does"* | The same situation — a rule that could sit in another layer — is sent to two opposite outcomes: settle it yourself (no question) or leave it out, mark, and ask the PO. | **BLOCKING** |
| D-7 | 135–136 vs 154–155 | *"Each block of `par-genre/transverses.md` gives two things, and you write both."* vs *"A transverse rule that gives no code at all gives only the constraint"* | "Each … two things … both" then "only the constraint … the common case". The first sentence should read "up to two". | **TO FIX** |
| D-8 | 380–381 vs 388–389, 418–419 | *"A bracket reference and an `<<ASSUMED …>>` mark each sit on one line, however long."* vs `<<ASSUMED B40: rail order taken from the display order of the` ⏎ `list screen>>` and `<<ASSUMED B40: this block holds a rule about storing the value,` ⏎ `which no entry of this section carries>>` | Both examples in the file break the rule stated eight lines above the first of them — the exact fault c.4 named. An agent copying the shape copies the wrap. | **TO FIX** |
| D-9 | 261–269 vs 647–649 | `[B?: the weigh-in screen]` *"And it is a question"* vs *"A block with neither a `## Trace` entry nor a `## Preamble` line — that is a fault of invocation 1, not a product question: say so in your report"* | `B?` has no Trace line and no Preamble line by construction, and it *is* a product question already written at invocation 1. Invocation 2 will report it as an invocation-1 fault. The `B?` case needs its own line in move 3. Also: what `Block:` names in the question for a `[B?` reference (the referencing block? nothing?) is not said. | **TO FIX** |
| D-10 | 116–117 vs 111, 114 | *"You recognise none of those by their wording — the split already sorted them, and each has its own file."* vs *"Intent, vocabulary — The product file's text outside the blocks"* · *"Dependencies — The references marked existing"* | Two of the four preamble parts have no file: intent/vocabulary is prose outside blocks, dependencies are marks inside blocks. And the *existing* mark is recognised by nothing but its wording, since its form is still not shown (c.5). | **TO FIX** |
| D-11 | 634–636 vs 34, 225–233 | *"it has no number: the reference names the preamble part that holds it"* vs *"The `Consumes:` lines — it reads them as a graph"* · the `Consumes:` shapes shown are `§3.2`, `[B12: …]`, `—` | A fourth shape of `Consumes:` operand (a preamble heading name?) is introduced and never shown. What does an entry that consumes a cross-cutting rule end with? | Question — **TO FIX** once answered |
| D-12 | 436–438 vs 313–314, 395–396, 648–649 | *"What you report: What you wrote, how many questions, how many `<<ASSUMED` marks."* | Three new obligations send things to the report — the decisions settled (313), which of the two cases each question is in (395), an invocation-1 fault found at move 3 (648) — and the technical questions count is a fourth. The report section lists none of them. | **TO FIX** |
| D-13 | 414–416 | *"you mark the section the way an assumption is marked"* | An assumption is marked *"where it sits"* (378) — inline in the entry. The left-out rule sits in no entry. Where in the section the mark goes (top? end? its own line?) is not said. | NOTE |
| D-14 | 395–396 vs 411–424 | *"Say which of the two you are in"* | The other-layer case (mark + question, entry not written) is neither "No" nor "Yes, by assuming" — a third case with the second's mark and the first's outcome. The report sentence has no word for it. | NOTE |
| D-15 | 377 vs 654–656 | *"No — Stop there: no section, no notes, the question written"* vs move 4 of invocation 2: *"treat what they return by What a question costs"* | At invocation 2 there is no section of yours and no notes; what a "No" means there (write no preamble? no traceability? stop?) is undefined. The old file had the same hole; c.1 closed it for invocation 1 only. | NOTE |
| D-16 | 601–603 | *"`## Preamble`: what your blocks give the preamble — a cross-cutting rule, a reference marked existing"* vs 113 | After the genre split, cross-cutting rules come from `transverses.md`, not from *your blocks*. If the constraint half is meant to travel through the notes' `## Preamble` to invocation 2 move 2 (621–622), every nature that read the file writes the same constraint lines and the preamble receives them up to eight times; nothing says who deduplicates. If it is not meant to travel that way, move 2 has no source for `## Cross-cutting rules`. | **TO FIX** |
| D-17 | 503–504 | *"eight sections are written at once"* | Up to eight — a nature with no block runs nowhere (cmd 122), and a nature that waits or is kept does not run either. Harmless. | NOTE |
| D-18 | 59, 294 vs 539–540, 520 | *"your technical questions — `convertisseur/technique-<nature>.md`"* vs PART 2 *Writes*: *"Your section · your notes · your questions"* · never do: *"Write outside the files your invocation lists"* | The technical file is not in the invocation's *Writes* column. By the letter of line 520, writing it is forbidden. Moves 5 and 6 (*"Write your questions file — always"*) name one file; whether the technical one is written empty when there is nothing, or not at all, is not said — and the command checks file presence to tell what happened (458). | **TO FIX** |

---

## Summary

- **Demands 1 and 2 are declared, not implemented**: the three `par-genre/`
  files enter the path table and the preamble table, and nothing else — not
  PART 2's *Reads*, not a single move. Two of them (D-1, D-2) cannot be
  implemented as written without deciding which invocation owns a transverse
  block's entry and its traceability line.
- **Demand 3 opens a route that dead-ends** inside the file (D-3, D-4, D-5,
  D-18) and outside it (no command touches `technique-*.md`; a technical answer
  never triggers a rerun).
- **One flat contradiction** between a new rule and a passed comment (D-6:
  "you settle the section" vs c.2 "never an entry, mark and ask").
- Of the 19 passed comments, 15 are conforming; c.4 has its rule but not its
  examples, c.5 is half done, c.14 leaves the sentence it was meant to remove,
  c.20 is applied to a file nobody reads.
- c.10 is correctly not applied.
