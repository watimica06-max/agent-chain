# Verification — `redacteur.md`

Read: `.claude/agents/redacteur.md` (old), `.claude-new/agents/redacteur.md`
(new), `docs/refonte/passes/redacteur.md` (18 comments), the
`# redacteur.md` section of `docs/refonte/modifications.md` (lines
143–293), plus — to settle C10–C16 and C17–C18, which target command
files — `.claude-new/commands/2_structure.md` and a `diff -q` of
`cycle.md` old against new. Cross-checked by grep only:
`.claude-new/agents/sondeur.md` (the *défaut* entry form),
`qualifieur.md` (the `transverse` genre), `lexicographe.md` (the
`en anglais` line), `.claude-new/commands/fusion.md` (row 10).

Line numbers below are the **new** file's unless marked *old*.

📌 **A note on modifications.md's layout.** The `# redacteur.md`
section has no "Ce qui a changé" table — it opens directly on "La
demande" (five numbered modifications) and closes on the pass sheet.
The `Genre:` line the Rédacteur now writes is announced not there but
in the `# 🆕 qualifieur.md` table (line 53: *"Écrit `Genre:` vide à
côté de `Nature:`, aux deux endroits qui décrivent la forme d'un
bloc"*). Both are treated as announced structural modifications below.

---

## A. CONFORMITY

### A.1 — The pass sheet (C1–C18)

| Id | Status | Expected (pass file, *Ce qu'il faut*) | Found in the new file | Verdict |
|---|---|---|---|---|
| C1 | PASSÉ | Strip markers only once the grid has consumed them: a file from the grid → strip then re-mark; the Rédacteur's own file → add this turn's markers, strip none | Lines 118–131: *"You strip the markers only when the file you integrate comes from an agent that read them … from the grid or from the conversion … strip them all, then mark what this turn touches. Any other answered file — your own, the qualifieur's, the classeur's, the lexicographe's — means no turn ran. You add this turn's markers and you strip none."* Mirrored in invocation 2 step 1, lines 520–522. | ✅ Fixed as asked. Goes further than the pass file (adds *the conversion* to the strip case, and three agents to the no-strip case) — see B.4, B.5 and D.9 |
| C2 | PASSÉ | One statement: an empty `Nature:` on every block this agent creates (idea file, answer, split, original of a split included); every other block keeps its line, MODIFIED or not | Lines 64–73, exactly that, extended to `Genre:` | ✅ Fixed as asked in Part 1 — ⚠️ **but the two places in invocation 2 that create blocks still say `Nature:` only** (pass a row 3, line 563; pass b step 3, line 574). See D.6 |
| C3 | PASSÉ | A contradiction is a case of move 4: transcribe the later sentence, flag the block, the flag names the sentence set aside, raise the question; the answer comes back via invocation 2 | Lines 481–490, all four elements present | ✅ Fixed as asked |
| C4 | PASSÉ | The strip of the `Clarification needed` line belongs to pass a, whatever the row; pass b needs no separate mention | Lines 545–548 (pass a, *"Whatever row it lands in"*); pass b line 581 keeps a pointer *"The flag is stripped at pass a — see there"* | ✅ Fixed as asked. The pointer in pass b is harmless |
| C5 | ÉCARTÉ | Not applied (mark on every entry, fixed position) | Pass e is deleted outright (old 516–519), *"Five passes"* → *"Four passes"* (line 535), Part 2 row 2 no longer lists *"that questions file, its entries marked"* (line 372). No `[integrated:` anywhere in `.claude-new/agents/` or `2_structure.md` | ✅ Not applied. The removal itself is announced only by the écarté reason (*"la marque a été retirée de la chaîne (D5)"*), not by a structural modification — recorded in B.14 |
| C6 | PASSÉ | The reference names the section as titled | Line 612–613: *"the four moves of INVOCATION 1 — Structuring"*; same wording reused at 660–661 | ✅ Fixed as asked |
| C7 | PASSÉ | The *"Between two sessions, re-read the product file"* line goes | Old 306–307 absent from the new file | ✅ Fixed as asked |
| C8 | PASSÉ | One test: "existing" when a title of the global's index names it, and only then; not found → no mark, not a question | Lines 206–214: *"marked as existing when a title of the global's index names it … That is the whole test … written without the mark — and that is not a question to raise. You never load a section to find out"* | ✅ Fixed as asked. Lines 216–218 add the pass file's justification as a rule rationale |
| C9 | PASSÉ | Number = highest redacteur number in the root and `questions/redacteur/` together, plus one | Lines 248–251, exactly that, *"your own prefix only"* | ✅ Fixed as asked. Formatting slip — see D.13 |
| C10 | PASSÉ (`2_structure.md`) | The reading list names exactly the reads the command does | New `2_structure.md` lines 23–31: ls before/after, the `## Decision` heading, grep for empty `Answer:`, grep `^### Q` | ✅ Fixed as asked |
| C11 | PASSÉ (`2_structure.md`) | A row for the empty questions file: invoke nothing, next is `/3_decoupe` | Line 83: *"One, with no `### Q` → Invoke nothing — nothing to integrate; say `/3_decoupe`"* | ✅ Fixed as asked |
| C12 | PASSÉ (`2_structure.md`) | Invocation 1 only when no product file exists; product file and no questions file → stop | Lines 81–82, 87–89 | ✅ Fixed as asked |
| C13 | PASSÉ (`2_structure.md`) | One complete template, parameter notes under it | One `Agent(...)` block (97–107) with the `Read:` line; notes at 149–158 | ✅ Fixed as asked |
| C14 | PASSÉ (`2_structure.md`) | The lexicographe's file is filed only when nothing in it waits | Lines 44–46: grep for an empty `Answer:` first, one hit stops | ✅ Fixed as asked |
| C15 | PASSÉ (`2_structure.md`) | The command deletes the derived files when a `NEW` block appeared, and its report says which | Lines 114–128 | ✅ Fixed as asked. NOTE: line 123 says *"those two are derived"* while the `rm` at 117–119 removes three paths (`par-genre/`, `desc-par-nature.md`, `spec-technique.md`) — count mismatch in the command, not in the agent |
| C16 | PASSÉ (`2_structure.md`) | `NN` = highest `blocked_redacteur-NN.md` in the folder plus one, `01` when none | Lines 135–136 | ✅ Fixed as asked |
| C17 | ÉCARTÉ (`cycle.md`) | Not applied | `diff -q` old/new `cycle.md`: identical | ✅ Not applied |
| C18 | ÉCARTÉ (`cycle.md`) | Not applied | Same | ✅ Not applied. NOTE: the untouched `cycle.md` still routes on `[integrated:` (its lines 54, 63), a mark the chain no longer produces — consistent with *"cycle.md est périmée"* |

### A.2 — The structural modifications ("La demande")

| # | Modification | Expected | Found | Verdict |
|---|---|---|---|---|
| 1 | `Global:` line | A `Global:` line beside `Genre:`/`Nature:`, naming the **section** of the global, never the block; absent (never empty) when nothing is attached; a new section carrying a global section's title is an attachment; the *why* (the grid closes with that section in front of it) | Example line 62 (`Global: ## Activity screen`), rules at 75–89: section not block ✓, absent never empty ✓, same-title section ✓, why ✓ | ✅ Present in Part 1 as specified. ⚠️ **Never carried into the procedure**: move 3 (lines 441–442) still says *"with an empty `Genre:` line and an empty `Nature:` line"* and no `Global:`; neither pass a row 3, pass b, pass d nor invocation 3 mention it. The demand says *"c'est un ajout à ce qu'il écrit"* — the place where it writes does not say so. See D.7 |
| 2 | A *défaut* with no written answer is accepted | At integration, no `Answer:` written → integrate the proposal | Lines 539–543: *"An entry marked défaut carries its own answer, with the paragraph that founds it. No `Answer:` written means the Product Owner accepted it … An `Answer:` written overrides it"* | ✅ As specified. Matches the sondeur's form (`Défaut:` line, `Answer:` empty). NOTE: the line is called *"marked défaut"*, never `Défaut:` by name — see D.10 |
| 3 | A changed transverse rule marks every block | When an answer modifies a transverse rule, all blocks are marked; brutal, meant to be | Lines 103–110 | ✅ As specified. ⚠️ Which marker is not said — see D.8 |
| 4 | The English word goes into the lexicon | First rendering → `en anglais :` line on the `## Tranché` entry; already carried → take it; absent from the lexicon → render and write nothing; never an entry; that line and only that line | Lines 162–187 (all three cases and the *never an entry* rule), never-do bullet 308–310, Part 2 outputs rows 1–2 (371–372) | ✅ As specified. The lexicographe's new file carries the line (`lexicographe.md` 155, 176) — the receiving side exists |
| 5 | Invocation 3 — `desc-produit-fusion.md` | Once at the end, launched by `/fusion`; reads `desc-produit.md` + every decisions file in cycle order; writes `desc-produit-fusion.md` with no marker; one invocation so it arbitrates between cycles; no decisions → faithful copy; placement as invocation 2; `desc-produit.md` never modified | Lines 623–670 and Part 2 row 3 (373); `fusion.md` row 10 invokes it | ✅ As specified. ⚠️ Its wiring into the rest of the file is incomplete: frontmatter, Part 2's two-way wording, the inputs it needs for "the four moves", the questions-file rule, the whole-read ban — see D.1–D.5 |
| Q | `Genre:` written empty (qualifieur section, *"aux deux endroits"*) | Empty `Genre:` beside `Nature:` at the two places describing a block's form | Line 60 and line 442 ✓ | ✅ At the two places named. ⚠️ The file has **four** places that describe a block this agent creates; the two in invocation 2 (563, 574) were not updated — see D.6 |

---

## B. UNANNOUNCED CHANGES

Every hunk of `diff old new` was matched against C1–C9, the five
modifications and the qualifieur row. What follows is what does not
match, or matches only in part.

**B.1 — line 62 · `Global: ## Activity screen` in the example** —
announced (mod 1). No finding.

**B.2 — lines 70–73 · a rationale that makes a claim about two other
agents.** NOTE.
> new: *"A marker is not what sends a nature back: the qualifieur and
> the classeur are given the marked blocks too, and each decides for
> itself whether its line still holds."*

Not in the pass file's *Ce qu'il faut* (C2 asked for one statement of
which blocks get an empty line, nothing about who re-checks). Checked:
`classeur.md` 265 and `qualifieur.md` 250 both carry *"On a block
marked `MODIFIED` whose line already carries a …"* — the claim holds.

**B.3 — lines 103–110 · transverse rule** — announced (mod 3). No
finding beyond D.8.

**B.4 — lines 118–121 · "from the conversion".** NOTE / question.
> old: *"You strip every marker before writing, so only this turn's are marked."*
> new: *"A questions file from the grid or from the conversion means a turn ran on the current markers — strip them all"*

C1 named one strip case: a file from the grid (`sondeur-*`). The
convertisseur's file is added. The outcome is right by ordering (the
grid ran and raised nothing before the conversion, so the standing
markers were consumed), but the sentence that introduces the rule,
line 118 *"comes from an agent that read them"*, is not literally true
of the convertisseur, which reads the whole closed file, not its
markers. See D.9.

**B.5 — lines 123–125 · the no-strip list.** NOTE.
> new: *"Any other answered file — your own, the qualifieur's, the classeur's, the lexicographe's — means no turn ran."*

C1 named only *"the Rédacteur's own file"*. The qualifieur's and the
classeur's files do reach invocation 2 (both agents write a questions
file). The lexicographe's never does: `2_structure.md` files it away
first (lines 44–63, *"What remains at the root is the file to
integrate"*). Listing it describes a case that does not occur —
harmless, but a reader may wonder which command would hand it over.

**B.6 — lines 127–131 · "Why" paragraph on the angles and the global
invocation.** NOTE. New rationale, taken from the pass file's *Le
défaut*; it asserts what the sondeur does (*"the global invocation
still crosses it against the others"*). Not verified here — it is the
sondeur's file's business.

**B.7 — lines 162–187 · "The English word is recorded, once"** —
announced (mod 4). No finding.

**B.8 — lines 216–218 · what the "existing" mark is for.** NOTE.
> new: *"The mark tells the convertisseur and the cadreur what is reused and what is built — guessed, it sends a lot to build on something absent, or to build what exists."*

C8's justification lifted into the rule text. The pass file itself
left open whether anything downstream reads the mark (*"What another
agent would settle"*, second-to-last entry). The claim is now stated
as fact.

**B.9 — lines 248–251 · questions-file number** — C9. No finding
beyond D.13.

**B.10 — lines 308–310 · never-do bullet on `lexique.md`** — mod 4.
No finding.

**B.11 — Part 2 table, lines 371–373** — mod 4 (outputs), mod 5 (row
3), C5 (mark removed from row 2's output). No finding beyond D.1–D.2.

**B.12 — lines 441–446 · move 3 names the qualifieur** — qualifieur
row. No finding beyond D.7.

**B.13 — lines 481–490 · contradiction** — C3. No finding.

**B.14 — line 535 · "Five passes" → "Four passes"** and the deletion
of pass e (old 516–519). Consequence of C5 being écarté with the reason
*"la marque a été retirée de la chaîne"*. Announced by that reason, not
by a listed modification; the removal is complete in this file (Part 2
row 2 output updated). No finding.

**B.15 — lines 539–548 · pass a gains two paragraphs** — mod 2 and C4.
No finding beyond D.10.

**B.16 — lines 623–670 · INVOCATION 3** — mod 5. Two sentences go
beyond the demand:
> line 654–656: *"Two decisions of different cycles that cannot both hold is not a question — the later one applies, and you say so in your report."*

The demand says *"une seule invocation, pour qu'il arbitre les
contradictions entre cycles"* — this is the arbitration rule, in scope.
> line 659: *"read it against the title list, as pass a does"*

See D.11 — pass a does not read against the title list.

**Not changed, and worth recording:** the frontmatter (lines 1–7) is
byte-identical to the old file, description included — see D.1.

---

## C. GESTURES AGAINST TOOLS

Frontmatter tools (line 4): `Read, Grep, Glob, Edit, Write`.

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Grep the global's `^#` index; grep `NEW`/`MODIFIED`; grep `^###`; grep a block number across the product file | 135, 402, 429, 520, 525, 577 | `Grep` | ✓ |
| Read `idees.md`, `lexique.md`, the questions file, the blocking file; ranged reads of blocks and of global sections | 396–400, 433, 500–503, 526–527 | `Read` | ✓ |
| Create the product file, the questions file, `blocked_redacteur.md`, `desc-produit-fusion.md` | 371, 253, 323, 647 | `Write` | ✓ |
| Targeted edits of blocks, marker lines, `Clarification needed` lines, the `en anglais :` line in `lexique.md` | 229–230, 520–528, 545–548, 164–166 | `Edit` | ✓ |
| Find *"the highest `questions-redacteur-NN.md` found in the root and in `questions/redacteur/`"* | 248–249 | `Glob` | ✓ — the only gesture that needs `Glob` |
| **Copy `desc-produit.md` to `desc-produit-fusion.md`** | 647 | none — no `Bash`, so no `cp` | ⚠️ **TO FIX.** The only way with these tools is a whole `Read` followed by a `Write`. The file forbids the whole read (303 *"Read the product file whole"* under *What you never do*; 516 *"You never read it whole"*), and the pass file's P13 entry names the failure mode of writing hundreds of lines in one go: silent truncation. Either the copy is the command's gesture (a `cp` in `fusion.md` before the agent runs), or invocation 3 says explicitly that this is the one time the file is read whole, and how truncation is checked (line count before and after) |
| "Say so in your report" | 656 | none needed | ✓ — the final message |

**Tools no gesture uses:** none. Every tool listed is used at least
once.

**Gestures no tool serves:** the copy at invocation 3 (above).

---

## D. INTERNAL COHERENCE — the new file alone

**D.1 — line 3 · frontmatter still says two invocations.** TO FIX.
> *"Two invocations: structuring the idea file, and integrating an answered questions file."*

Part 2 (369–373) and Part 3 (623) define three. The description is
what the orchestrator sees in the agent registry; `fusion.md` row 10
calls *"Rédacteur, invocation 3 — Merging"*, which the description
says does not exist. (Pre-existing and unrelated: *"The only agent that
writes the product file"* was already untrue of the old file — the
decoupeur, the classeur and now the qualifieur write in it too. NOTE.)

**D.2 — lines 375–380 · two-way wording over a three-row table.** TO
FIX (small).
> line 375: *"Neither is ever inferred from the folder"*
> line 379–380: *"an input listed against the other stays unopened"*

Written for two invocations; with three, *"neither"* and *"the other"*
have no referent. Same class as C6 and C7 (a reference the reader
cannot resolve).

**D.3 — invocation 3 needs inputs it is not given.** TO FIX.
> line 373 (inputs): *"`desc-produit.md` · every decisions file the prompt names"*
> line 660–661: *"A subject no title covers becomes a block, by the four moves of INVOCATION 1 — Structuring"*
> line 296: *"Read anything your invocation does not list under Inputs"* (forbidden)

Move 2 of invocation 1 (429–439) greps the global's index and loads a
near section; move 3 files under a global title; `Global:` (75–77) is
derived from that grep. None of that is possible without the global,
which row 3 does not list — nor `lexique.md`, which the *en anglais*
rule (162–166) needs for any concept rendered in English for the first
time. Either row 3 lists them, or invocation 3 says a new block is
created without move 2 and without `Global:` — and then says what the
Fusionneur gets instead.

**D.4 — the questions-file rule against invocation 3.** TO FIX, or a
question.
> line 253–255: *"Write it at every invocation, even empty — … a missing one says you did not run."*
> line 373, 670: invocation 3's only output is `desc-produit-fusion.md`.

Either invocation 3 writes `questions-redacteur-NN.md` too (and
`fusion.md` then has a root questions file to route on — its row 5
stops on an empty `Answer:`), or the rule says *"at invocations 1 and
2"*. Related: *"the four moves"* include move 4 (flag the block, write
the question, *"Nothing downstream runs while a flag stands"*, 477). A
decision at invocation 3 that cannot be transcribed in one reading has
no route: no questions file is written, no `## Decision` comes back,
and a `Clarification needed` line would sit in a file whose only
reader is the Fusionneur. **Which branch does a decision the agent
cannot place take?** The file gives none — a procedure branch that
leads nowhere.

**D.5 — the whole-read ban against the copy.** TO FIX. See C above.
> line 303: *"Read the product file whole — grep its titles, load the blocks you need"* (never)
> line 647: *"Copy `desc-produit.md` to `desc-produit-fusion.md`"*

A rule contradicted elsewhere in the file. The ban's own reason
(516–518, *"the single most wasteful thing you can do here"*) is written
for invocation 2; invocation 3 has to read the whole thing at least
once.

**D.6 — `Genre:` present at two of four creation sites.** TO FIX.
> line 64–66: *"You write `Genre:` and `Nature:` empty on every block you create — from the idea file, from an answer, from a split, the original of a split included."*
> line 563 (pass a row 3): *"It becomes a block of its own, with an empty `Nature:`"*
> line 574–576 (pass b step 3): *"Each block gets an empty `Nature:`, the original included — a split rarely leaves two halves of one nature, and the classeur fills them after you"*

Part 1 and move 3 (442) say both lines; the two invocation-2 sites say
`Nature:` alone, and pass b's rationale still names only the classeur.
A reader executing pass b leaves the original's `Genre:` filled; line
67–68 says the qualifieur *"greps for the empty ones"*, so that block
keeps a genre that a split *"rarely"* preserves (446–447). The
qualifieur row in modifications.md said *"aux deux endroits"* — there
were four.

**D.7 — `Global:` is described, never written.** TO FIX.
> line 75–77: *"`Global:` names the section of the global this block attaches to … and you already know it: move 2 greps the index to file the block."*
> line 441–442 (move 3): *"File. One block per subject, under the title found or created, with an empty `Genre:` line and an empty `Nature:` line."*

Move 3 is the only place the file says what a block is written with,
and `Global:` is not in it. Nor at pass a row 3 (563), pass b (572–579
— do the halves inherit the original's `Global:`?), pass d (605–607),
or invocation 3 (658–661). Part 1's *"you already know it"* is true of
move 2's result but no move says to write it down. Given the demand's
own *why* (*"sans ce marquage, la grille ne sait pas lesquels le
nécessitent"*), a block filed without the line is exactly the failure
mod 1 exists to prevent.

**D.8 — line 103 · "marks every block" — with which marker?** TO FIX
(small).
> *"A block carrying `Genre: transverse` that you change marks every block of the file."*

The two markers are defined at 96–101: `NEW` for created, `MODIFIED`
for changed. A block untouched in wording is neither. Presumably
`MODIFIED`; a block already `NEW` presumably keeps `NEW`. Neither is
said, and line 112–113 insists *"They are not the same thing"*.

**D.9 — line 118–119 · "an agent that read them" against line 119–120
"or from the conversion".** Question.
> *"You strip the markers only when the file you integrate comes from an agent that read them. A questions file from the grid or from the conversion means a turn ran on the current markers"*

Does the convertisseur read the markers? If not, the first sentence
states a criterion the second sentence does not follow. The rule
holds by ordering (a grid turn ran and raised nothing before
`/6_convertit`); the file should say that, or drop *"an agent that read
them"*. Also, the never-do bullet at 311–312 still says *"the sondeurs
would never probe it again"* and 115–116 *"The sondeurs and the
decoupeur grep both"* — the qualifieur and the classeur, which line 72
says also read the markers, are in neither list. NOTE.

**D.10 — lines 539–543 · "An entry marked *défaut*".** NOTE.
The sondeur's form (`sondeur.md` 281–286) is a fifth line, `Défaut:`,
between `Question:` and `Answer:`. The Rédacteur's text never names the
line; *"marked défaut"* could be read as a word in the `Question:`
line. Naming the line (`Défaut:`) closes it. Also, 257 *"One entry per
question, four lines, no exception"* is the Rédacteur's own file's rule
and stays true; but a reader integrating a five-line entry has nothing
that tells him the fifth line is expected.

**D.11 — line 659 · "as pass a does".** NOTE.
> *"Where a decision lands — almost always in an existing block: read it against the title list, as pass a does."*

Pass a (537–568) asks trigger and output of the block; it is **pass d**
(593–594) that answers *"on the title list from step 2"*. Wrong
cross-reference — same class as C6.

**D.12 — lines 628–631 · three names for one artefact.** NOTE.
> *"a product question settled while the code was being written went into a **sheet**, never into the product file … was decided in a **blocking file**"*; inputs: *"every **decisions file**"*.

The input is `code/decisions-produit.md` (per `fusion.md` 61–63).
*Sheet* and *blocking file* are the artefacts upstream of it; the
Rédacteur never opens either. A term used in two senses, or three
terms for one route.

**D.13 — line 248 · formatting.** NOTE.
> *"🔴 **Yours is `questions-redacteur-NN.md`, at the root** — 🔴 **Your number: the highest …"*

Two red markers in one sentence, a capital mid-sentence, and a
130-character line in a file wrapped at ~72. Reads like a paste over
the old sentence.

**D.14 — line 617 · "on either branch".** NOTE (pre-existing).
> *"Output of this invocation, on either branch: the product file."*

Invocation 2 names no two branches. Probably *pass d finds nothing /
finds something* (609–613). Unresolvable as written.

**D.15 — line 83–85 against line 237–238.** Question.
> 83–85: *"A section you create in this file that carries the same title as one of the global's is an attachment — the line says so, whether or not you reused the title."*
> 237–238: *"Grep before creating — a title close to an existing one creates a duplicate nothing will catch."*

Move 2 (437) creates a title only on *"No"* — different trigger or
output from the global's section. Can a created section then carry
the *same* title as a global section, or is that the duplicate 237
forbids? If *"existing"* at 237 means the feature file's own sections,
say so; if it means the global's, 83–85 contradicts it.

**D.16 — invocation 3 and the `NEW` rule.** NOTE.
> 96: *"`NEW` on every block you create"*; 313: *"Create a block without `NEW` — same reason"* (never)
> 663–664: *"Strip every marker — no `NEW`, no `MODIFIED` in the file you write."*

Resolved by ordering (mark at move 2, strip at move 3) but a reader of
*What you never do* has no hint that one invocation ends with none.
Also: a block created at invocation 3 carries empty `Genre:` and
`Nature:` (64–66) and nobody fills them — the qualifieur and the
classeur do not run after `/fusion`. **Does the Fusionneur need those
lines filled?** Not this file's to answer, but this file creates the
case.

**D.17 — `fusion.md` hands the agent less than it needs.** Question,
outside this file.
> `redacteur.md` 634–636: *"every decisions file the prompt names — in the order it names them"*
> `fusion.md` 87–92 (its only template): `prompt="Feature folder: docs/features/<name>/. <Which invocation>."`

Row 10's prose says to name every `code/decisions-produit.md` in cycle
order; the template has no line for it. The same defect C13 fixed in
`2_structure.md`. An orchestrator following the template names no
file, and the agent — *"you never look for one yourself"* (383–385)
— has nothing to fold.

---

## Summary

- **A.** All 15 PASSÉ comments are fixed as the pass file asked (C1–C9
  in the agent, C10–C16 in `2_structure.md`); the 3 ÉCARTÉ were not
  applied (C5's mark is removed altogether, `cycle.md` is untouched).
  All five structural modifications and the `Genre:` line are present.
- **B.** No silent change of substance. Three extensions beyond the
  pass file (B.2, B.4/B.5, B.8), all rationale; one count change
  (*"Four passes"*) that follows from C5's écarté reason.
- **C.** Tools fit every gesture but one: the copy at invocation 3 has
  no `cp` and collides with the whole-read ban.
- **D.** The invocation 3 graft is under-wired — frontmatter (D.1),
  two-way wording (D.2), missing inputs (D.3), the questions-file
  rule and the no-route flag (D.4), the whole read (D.5). Two
  procedural gaps in the new lines predate it: `Genre:` at two of four
  creation sites (D.6), `Global:` written nowhere (D.7).

**BLOCKING**: none.
**TO FIX**: D.1, D.2, D.3, D.4, D.5 (= C's gesture finding), D.6, D.7,
D.8.
**NOTE / question**: the rest.
