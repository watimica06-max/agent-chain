# agent-sondeur — verification

**Read**: `.claude/agents/sondeur.md` (old, 252 lines, 9.4 KB) · `.claude-new/agents/sondeur.md`
(new, 387 lines, 15.4 KB) · `docs/refonte/passes/sondeur.md` (22 comments, `### 1` … `### 22`) ·
`docs/refonte/modifications.md` § `` # `sondeur.md` `` (lines 339–469).

**What the section says**: five structural modifications ("La demande" §1–§5: probe
behaviours only · load the transverse rules · the *défaut* with its citation · two
diverging rules · read the global at time 2, in a dedicated invocation 3) plus the pass
sheet — **Passés (18)** C1 · C3 · C4 · C5 · C6 · C7 · C8 · C11 · C12 · C13 · C14 · C15 ·
C16 · C17 · C18 · C19 · C20 · C22 — **Écartés (3)** C2 · C9 · C21 — **Reportés (1)** C10.

Of the 22 comments, **nine target the agent file** (C1–C9, C22) and **thirteen target
commands** (C10–C20 → `4_grille.md`, C21 → `cycle.md`). The agent-side ones are verified
in full. The command-side ones are outside this report's scope; where a grep on
`.claude-new/commands/4_grille.md` settled one at no cost, the verdict is given and marked
*incidental*. Line numbers are those of the **new** agent file unless marked *old* or *cmd*.

Existence checks done without opening the grids: `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md`
holds a heading `## What pass A left you` (line 243); `GRILLE_EXISTANT.md` exists only at
`docs-new/process/GRILLE_EXISTANT.md`, not at `docs/process/`; `docs/PRODUIT_GLOBAL.md`
is 15 bytes in this repository.

---

## A. Conformity

### Structural modifications ("La demande")

| § | Expected | Found | Verdict |
|---|---|---|---|
| §1 Probe behaviours only | Blocks whose `Genre:` is not `comportement` are not probed; the agent does not filter, `/4_grille` names the blocks; it reads `desc-produit.md`, never a partage file | Lines 43–52: two-list table — *"The blocks to probe — Every one carries `Genre: comportement`"*; *"A block of any other genre is neither — the command does not name it, and it is not yours."* Line 135: global row now *"Every behaviour block, every time"*. Command side: cmd 105–106 `grep -B1 '^Genre: comportement$'`. No mention of a partage file anywhere — the agent names nothing beyond the product file. | **Conforming** |
| §2 Transverse rules in context | Loads the `Genre: transverse` blocks the command names; never probes them; the match happens at the moment of the question — no mapping table, no per-block marking; a transverse rule carries its reach in its wording | Line 49: *"You never probe them — you hold them beside you"*. Lines 245–253: *"Before a gap becomes an obligatory question, ask whether one of the transverse blocks already answers it … A transverse rule carries its own reach in its wording … There is no table mapping a transverse rule to the blocks it reaches, and none is needed."* Cmd 218/234/251/269 pass the list in all four prompts. | **Conforming** |
| §3 Défaut with its citation | Three cases: corpus answers → nothing; nothing answers → obligatory; a transverse rule or a pattern already followed answers → *défaut* with the pre-filled answer and the reference of the founding paragraph; silence accepts; volume spreads, a settled question is still not asked | Lines 210–218: the two-row table (obligatory / *défaut*), *"silence accepts it"*, *"The volume does not rise, it spreads — a question the block itself settles is still not asked."* Lines 279–299: the five-line shape with `Défaut: <the answer you propose> — <the block and the words that found it>`. | **Conforming in substance.** Two deviations from the letter: (a) the demand says the answer is *pré-remplie* — the new file puts the proposal on a `Défaut:` line and keeps `Answer:` empty (line 294), which is a defensible reading but line 281 says the opposite — see **D-4**; (b) the demand says *"la référence du paragraphe"*, the file asks for *"the block and the words that found it"* — a quotation instead of a reference. NOTE. |
| §4 Two diverging rules | Transverse vs transverse on one block → obligatory question, never a défaut; transverse vs a rule of the block → the block wins, no défaut | Lines 258–264: both rows, in those terms — *"naming one of the two would settle it yourself"*; *"the block wins, it is the more precise. Nothing to raise: it is not a divergence, it is an exception."* | **Conforming** |
| §5 Read the global at time 2 only, in a dedicated invocation | A third invocation *Existant*, after time 1 returns an empty file; reads the blocks carrying `Global:` and only the global sections they name, never the whole file; writes its own questions file, no merge | Line 136: table row 3 — *"Existant — one, after 1 and 2 have closed — Those carrying a `Global:` line — The existing-product grid — Your questions"*. Lines 340–387: the section — *"after the framing grid has returned an empty questions file"*; *"only the sections your blocks' `Global:` lines name … Never the file whole"*; *"Your questions file, the same four lines"*; no *défaut* (line 379). Cmd 155–195: trigger, one invocation, *"No merge"*. | **Conforming** — with the placement and count issues of **B-3**, **D-1**, **D-2** |

### Comments listed PASSÉ — agent file

| # | Expected (pass file, *Ce qu'il faut*) | Found (new file) | Verdict |
|---|---|---|---|
| C1 | The count matches the table: two files always, a third only when the prompt names it | Line 35: *"Two files always, and a third only when the prompt names it:"* — word for word. | **Conforming** — but invocation 3 adds a fourth file (line 352) the sentence does not count: see **D-3** |
| C3 | The `**Clarification needed:**` stop goes; the command's grep is the net | Old lines 46–50 gone. Line 61: *"One thing stops you before you write anything"*. Cmd 38–84 (*Before anything else*) is the net. | **Conforming** |
| C4 | The stop names an observable: the read returned less than the file holds — a truncation the tool signals, a text ending mid-block, a heading with no body — or nothing at all; a small file read whole is not a stop | Lines 63–68: *"A read that returned less than the file holds — a truncation the tool signals, a text ending mid-block, a heading with no body after it — or nothing at all. Say what you asked for and what you got. A small file that reads whole is not a stop."* | **Conforming** (to the letter) |
| C5 | The prompt's list is the only authority — "every block" or identifiers; the marker explanation goes; a listed identifier absent from the product file is a stop, naming it | Lines 146–151: *"the prompt names them, and it is the only authority. Either identifiers, or every block. A marker you see on a block outside your list changes nothing — you probe your list. A listed identifier the product file does not hold is a stop — name it."* Old NEW/MODIFIED explanation gone. | **Conforming** — the word *marker* survives without a referent (**D-6**), and the new stop is not counted at line 61 (**D-2**) |
| C6 | One owner for the record's columns: the grid names them and the agent says "the identifiers pass B crosses, as the grid lists them" | Lines 162–168: *"The grid names them, under What pass A left you — you take the list from there, never from memory: a crossing added to the grid is a column the record has to carry. One line per identifier the grid lists, in its order."* The grid holds that heading (line 243 of `GRILLE_CADRAGE_PRODUIT_V2.md`). The old explicit list `A1.1, A1.2, A1.3, A1.4, A1.9, A4` is removed from the rule — but survives in the example at 170–176. | **Conforming.** NOTE: the example still enumerates six identifiers; when the grid's list changes, the example goes stale while the rule does not — the very defect C6 was about, one notch down. |
| C7 | A test for inapplicability: the question presupposes something the block does not have (an input, a stored value, a screen), or the grid scopes it to a nature the block does not carry; anything else is open | Lines 221–228: *"the narrowest of the three: the question presupposes something the block does not have — an input, a stored value, a screen — or the grid scopes it to a nature the block does not carry. Anything else is open. It is the only outcome that dismisses a question with nothing written, and a gap that leaves through it never comes back."* | **Conforming** (to the letter) |
| C8 | A pass A gap names the one block that lacks the thing; a gap that exists only between two blocks is pass B's, and pass B names both | Lines 313–320: *"One identifier for a pass A gap — always one: it is the block that lacks the thing. Several for a pass B crossing — it names every block it crosses. A gap that only shows against another block is not pass A's — it is a crossing, and pass B raises it."* Old *"a pass A gap that only shows against another names both"* gone. | **Conforming** |
| C22 | The global and a first-turn angle read the file whole; a later-turn angle reads the named blocks, by their heading, nothing else; the "short" stop applies to what was read | Line 39: *"The blocks the prompt names, by their heading — whole only when it names every block"*. Lines 57–59: *"A block you were not named is not yours to read — and a pass A question stands on its block alone, so reading the others buys nothing."* | **Conforming in substance** — one rule instead of the asked two branches. NOTE: the "whole" branch is dead in practice — the new command sends identifier lists on every turn (cmd 106: *"whatever the turn"*) and never the words *every block* alone; see **D-7**. |

### Comments listed PASSÉ — command file (incidental, by grep only)

| # | Expected | Found in `.claude-new/commands/4_grille.md` | Verdict |
|---|---|---|---|
| C11 | A grep on the latest root questions file for an empty `Answer:` or no integration mark, and a stop | cmd 96–97: *"The latest questions file at the root is answered and integrated. A `grep '^Answer:$'` on it — one hit and you stop"* | **Applied** (the integration-mark half not checked) |
| C12 | The blocking file named root-relative in the prompts | cmd 222, 239, 256, 272: `docs/features/<name>/cadrage-produit/blocked_*.md` | **Applied** |
| C13 | Grep matches the marker's exact form on the heading | cmd 118–119: `grep '^### .*NEW'`, `grep '^### .*MODIFIED'` | **Applied** |
| C14 | A Nature grep before invoking, stop naming the blocks and `/3b_nature` | cmd 87–89: *"Every block carrying `Genre: comportement` has a filled Nature line … One hit and you stop"* | **Applied** |
| C15 | Grouping orders the reading; every block still goes through every question on its own | cmd 254: *"question on its own, then move to the next nature"* | **Applied** |
| C16 | One ordered check per expected file: present / blocking file present → relay / missing → a row | cmd 290–298: blocking files checked first, then existence of the four files and the record. Relay table (cmd 445–453) has the sondeur-blocked row; **no row for a reading missing without a blocking file.** | **Partially applied** — question: where does "one of the four files is missing and no blocking file" route? Not in the relay table as grepped. |
| C17 | A re-run on a filled sondeur decision invokes the blocked reading alone | cmd 57: *"invoke that reading alone"*; cmd 63; cmd 447: *"only that reading runs"* | **Applied** |
| C18 | One `NN` rule: the turn's number | cmd 334–335: *"`NN` is the turn's number — the one the `questions-sondeur-NN.md` of this turn takes."* | **Applied** |
| C19 | The questions file is copied byte for byte, never renumbered | cmd 342–347: *"A copy, byte for byte — `cp`, never a read-and-rewrite."* | **Applied** |
| C20 | Only the reading rules this project's CLAUDE.md states; `CALIBRATION_RISK_LEVEL.md`, "risk level", `TaskCreate` go | `CALIBRATION` no longer appears. **cmd 455–456 still reads: *"Nothing else is yours: no risk level, no `TaskCreate`, no reading of what the questions say."*** | **Half applied — TO FIX (command side).** The file reference went; the two concepts the comment named as foreign to this project are still in the relay section. |

### Comments listed ÉCARTÉ / REPORTÉ — verified NOT applied

| # | Must NOT be applied | Found | Verdict |
|---|---|---|---|
| C2 | Grid read by section | Line 40: grid *"Whole"*, both grids. | **Correctly not applied** |
| C9 | A field carrying the grid identifier | Lines 327–330 unchanged: *"never the grid identifier that raised it. The identifier belongs to the record"*. No new field in the four-line shape (271–274) nor in the five-line *défaut* shape (283–287). | **Correctly not applied** |
| C10 | Command sections in execution order | cmd headings: *Git, in this mode* (cmd 359) still sits after *The four invocations* (cmd 199), *Then the merge*, *Once it has reported*. | **Correctly not applied** (deferred to `todo.md`) |
| C21 | `cycle.md` routing | Not checked — marked *caduc*; outside the agent file. | — |

---

## B. Unannounced changes

Everything in the diff was traced to a defect or to a "La demande" paragraph except the
following.

### B-1 — Grid path dropped from the reading table

- **Line 40** (old line 40)
- Old: `| **The grid**, `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md` | 🔴 **Whole** |`
- New: `| **The grid** — 📌 `GRILLE_CADRAGE_PRODUIT_V2.md` at invocations 1 and 2, `GRILLE_EXISTANT.md` at invocation 3 | 🔴 **Whole** |`
- What it changes: the agent file no longer says where the grids live. The command prompts carry the full path (cmd 180, 216), so nothing breaks — but the agent's only path rule (line 31, *"Every path you read or write is relative"*) now has no example of a grid path to apply it to, and an agent invoked with a bare name would have to search, which the file forbids for blocking files (line 121–123) and says nothing about for grids.
- **NOTE**

### B-2 — The record's rows now carry a fixed order

- **Line 168**
- Old (old 144–146): *"for every block, in the product file's order, the answers pass B crosses: `A1.1`, `A1.2`, `A1.3`, `A1.4`, `A1.9`, and `A4`'s list of names"* — an enumeration, no ordering rule for the rows.
- New: *"**One line per identifier the grid lists, in its order:**"*
- What it changes: a new constraint — rows in the grid's order — that C6 did not ask for. Harmless; it makes two blocks' records comparable line by line. Announced nowhere.
- **NOTE**

### B-3 — Invocation 3 placed in PART 3, after "What you write", not in PART 2 with invocations 1 and 2

- **Lines 338–340**: `---` then `## Invocation 3 — Existant: the feature against what is already built`, sitting at the end of `# PART 3 — What you do`.
- Old: PART 2 (*Which call is this*) holds `## Invocation 1` and `## Invocation 2`; PART 3 holds *What you are looking for* and *What you write*.
- What it changes: a reader following PART 2's table (line 132–136) to the invocation sections finds 1 and 2 there and 3 a hundred and eighty lines later, after the writing rules — which invocation 3 then partly overrides (*"no défaut at this invocation"*, line 379; *"never a gap"*, line 377). "La demande" §5 announces the invocation, not where it goes. See also **D-1**, **D-5**.
- **TO FIX** (move under PART 2, or say in PART 2 where it is)

### B-4 — Frontmatter `description` unchanged while the agent gained an invocation

- **Line 3**: *"MUST BE USED four times per grid turn, in parallel — three angles … one global invocation …"* — identical to old line 3.
- What it changes: not a change but an omission the diff makes visible: the description the orchestrator and the registry read still describes two invocations. Not a defect the pass listed; modifications.md's table announces *"🆕 invocation 3 — Existant"* for `agents/sondeur.md` without saying whether the description follows. See **D-1**.
- **TO FIX**

No renumbering, no reworded rule, no rewritten table beyond those mapped to C1, C3, C4,
C5, C6, C7, C8, C22 and §1–§5. The *What you never do* list (lines 70–82), the blocking-file
section (86–123), the *Block:* line rules other than C8, and the closing rules (325–336)
are byte-identical to the old file.

---

## C. Gestures against tools

**Frontmatter** (line 4): `tools: Read, Grep, Glob, Write` — unchanged from old.

### Gestures the file asks for, and the tool each needs

| Gesture | Lines | Tool | Has it |
|---|---|---|---|
| Read the named blocks of the product file *"by their heading"* | 39, 57 | Locate the heading (Grep) then Read from that offset | **Yes** — Grep + Read. The file never says the word *grep*; the gesture is implied by *"by their heading"* |
| Read the product file whole | 39 | Read | Yes |
| Read the grid whole (either grid) | 40 | Read | Yes |
| Read a blocking file the prompt names | 41, 120 | Read | Yes |
| Read the transverse blocks the prompt names | 49 | Grep + Read, as above | Yes |
| Detect a read that *"returned less than the file holds — a truncation the tool signals"* | 63–64 | Read's own truncation notice | Yes |
| Stop on *"a listed identifier the product file does not hold"* | 150–151 | Grep for the heading | Yes |
| Read *"only the sections your blocks' `Global:` lines name"* of `docs/PRODUIT_GLOBAL.md`, *"never the file whole"* | 352–356 | Grep for the section heading, Read with offset and limit — the only way to obey *never whole* on a file said to exceed 250 KB | Yes — Grep + Read |
| Write `<out>/blocked_<your name>.md` | 88 | Write | Yes |
| Write the questions file, the record | 268–269, 191 | Write | Yes |
| Never write in the product file | 72 | (no Edit) | Consistent — Edit is absent |

### Tools with no gesture

| Tool | Finding |
|---|---|
| **Glob** | No gesture in the file searches for a file by pattern. Every input is named by the prompt (product file, grid, blocking file, global sections, block identifiers); the file forbids looking for a blocking file itself (121–123) and forbids reading anything not named (54–59). **Glob is unused.** NOTE — harmless, but a tool the file gives no use is a tool an agent may use to do what the file forbids (find *"a previous turn's questions"*). |
| **Grep** | No gesture names it. It is needed (see above) for *"by their heading"* and for the `Global:` sections — but the file never tells the agent that the way to read a block by its heading is a grep on `^### B7 ` (the classeur's file says exactly this at its line 53–55). NOTE — an agent that Reads the whole file to find its headings has obeyed the tool and broken line 57 (*"not yours to read"*) and C22's saving. |

**No gesture without a tool.** One gesture is under-specified rather than unequipped:
how to locate a heading (Grep) is left to the agent.

---

## D. Internal coherence (new file alone)

### D-1 — "which of two invocations" followed by a three-row table — **TO FIX**

- **Line 129**: *"🔴 **The prompt says which of two invocations you are.** It is never inferred."*
- **Lines 132–136**: the table has three rows, `1 | Angle`, `2 | Global`, `3 | Existant`.
- **Line 3** (description): *"four times per grid turn"* — counts angles and global only.
- **Lines 24–26** (Role): *"Four of you run at once. Three angles … a fourth, the global invocation"* — true of time 1, silent on invocation 3, which runs alone and later.
- An announced count that does not match what follows — the very shape of C1's defect, reintroduced one section down.

### D-2 — "One thing stops you" while the file now holds two stops — **TO FIX**

- **Line 61**: *"**One thing stops you before you write anything:**"* — the read-shortfall stop (63–66).
- **Lines 150–151**: *"🔴 **A listed identifier the product file does not hold is a stop** — name it."* — a second stop, added by C5 in the same edit that reduced the count from two to one (C3).
- Same defect shape as D-1. The blocking-file section (86–118) says what a stop does; it does not say which stops exist, so line 61's count is the only inventory and it is wrong.

### D-3 — "Two files always, and a third only when the prompt names it" is false at invocation 3 — **TO FIX**

- **Line 35**: *"**Two files always, and a third only when the prompt names it:**"* — the table under it lists product file, grid, blocking file.
- **Line 350–352**: *"**What you read, beyond the usual two** — The global product file, `docs/PRODUIT_GLOBAL.md`"* — a fourth file, read whenever invocation 3 runs, whether or not a blocking file is named.
- C1 fixed the count for time 1; §5 added a reader the count does not include. Either the table gets a fourth row scoped to invocation 3 (as line 40 already scopes the grid by invocation), or line 35 says "at invocations 1 and 2".

### D-4 — `Answer:` carries the proposal / `Answer:` stays empty — **TO FIX**

- **Line 281**: *"🔴 **One more line, and `Answer:` carries the proposal:**"*
- **Lines 283–287** (the shape): the proposal is on `Défaut:`; `Answer:` is shown empty.
- **Line 294**: *"🔴 **`Answer:` stays empty, as always.** 📌 **Empty means the Product Owner accepts the proposal** — ⚠️ **written, it replaces it.**"*
- Two 🔴 rules thirteen lines apart say opposite things about the same field. The shape and line 294 agree with each other; line 281 reads like a first draft in which the proposal sat in `Answer:` (which is also how "La demande" §3 phrases it: *"sa réponse pré-remplie"*). One of the two must go. Question for the author: was the intent *pré-remplie* in `Answer:` (silence = the pre-filled text stands, and the Rédacteur integrates it as any answer) or a separate `Défaut:` line (silence = an empty `Answer:`, and the Rédacteur has to know that empty + `Défaut:` means accepted)? The second requires the Rédacteur to read `Défaut:`, which this file cannot guarantee.

### D-5 — A *défaut* founded on "the blocks that already follow the pattern" contradicts three rules of the same file — **TO FIX**

- **Line 216**: *"A transverse rule, **or a pattern the file already follows**, answers it → A *défaut*"*
- **Lines 290–291**: *"`Défaut:` names where the answer comes from — the transverse block, quoted in its own words, **or the blocks that already follow the pattern**."*
- Against **line 76–77**: *"🔴 Close a pass A gap because another block settles it — that is pass B's"*; **line 242–243**: *"Whether another block settles it is pass B's business, and only pass B's — a pass A question stands on its block alone"*; **lines 57–59**: *"A block you were not named is not yours to read — and a pass A question stands on its block alone, so reading the others buys nothing."*
- A *défaut* founded on other blocks *is* a pass A gap softened because other blocks settle it — which the file assigns to pass B. And on a later turn an angle holds only its named blocks plus the transverse ones (line 39, 57), so *"a pattern the file already follows"* is not in front of it: the only agent that sees every behaviour block is the global, which *"records, does not question"* (183). The pattern branch is therefore either forbidden (angles) or out of reach (global). "La demande" §3 does say *"un motif déjà suivi"*, so the demand and the file's older rules pull apart; the file has to say which wins, and for whom.

### D-6 — "A marker you see on a block" — a term with no referent — NOTE

- **Line 149**: *"⚠️ **A marker you see on a block outside your list changes nothing**"*
- C5 removed the sentence that defined *marker* (old 131–133: `NEW`, `MODIFIED`). No other line of the new file says what a marker is or looks like. The rule is still readable ("whatever you see, probe your list") but names a thing the file no longer introduces.

### D-7 — The "whole" branch and the "every block" branch — question

- **Line 39**: *"whole only when it names every block"*; **line 147**: *"Either identifiers, or *every block*."*
- **Line 135**: the global's blocks are *"Every behaviour block, every time"* — and the command's global prompt (cmd 267) reads *"every behaviour block: <list>"*: the words *every … block* and a list of identifiers on the same line.
- Question: when the prompt says *every behaviour block* followed by identifiers, does the agent read the file whole (line 39's second branch) or the named blocks (first branch)? The two branches give different readings of the same prompt, and the difference is the token saving C22 was about. If the command never sends *every block* alone, the branch leads nowhere and could go.

### D-8 — Is a *défaut* a gap? — the term used in two senses — NOTE

- **Line 49**: *"a question a transverse rule already answers is a *défaut*, **not a gap**"*
- **Lines 210–216**: *"It leaves it open — that is a gap. And a gap becomes one of two questions: … An obligatory question … A *défaut*"* — a *défaut* is one of the two forms a gap takes.
- **Line 297–298**: *"A *défaut* is not a lighter question — it is a question whose answer the corpus already carries somewhere else"*.
- Line 49 says a *défaut* is not a gap; line 210–216 says it is a gap that became a question. The three-outcome test at 203–228 only works under the second sense (open → gap → obligatory or défaut). Line 49's *"not a gap"* should read *"not an obligatory question"*.

### D-9 — The three-outcome test is written for invocations 1 and 2 and does not fit 3 — NOTE

- **Lines 203–205**: *"Take each question of your invocation to what it puts in front of you — **a block, or a column of the record** — and ask it. Then one of three things is true"*.
- **Lines 367–369** (invocation 3): *"You take each of them to **a block and the section it names, together** — neither is answerable from one alone."* **Line 377**: *"Every question here is an arbitration, never a gap"*.
- The general procedure (PART 3, *What you are looking for*) enumerates two objects and three outcomes; invocation 3 adds a third object and replaces the outcomes (no gap, no *défaut*, arbitration only). Nothing in PART 3 says it does not apply to invocation 3; the reader learns it from the exception at line 377. Placement (B-3) makes it worse.

### D-10 — Blocking-file name at invocation 3 — question (cross-file, stated because the rule is in this file)

- **Line 88**: *"Write `<out>/blocked_<your name>.md` — the folder and the name the prompt gives your questions file"*.
- At invocation 3 the prompt gives `docs/features/<name>/questions-existant-NN.md` (cmd 186), so the rule yields `docs/features/<name>/blocked_questions-existant-NN.md`. The command expects `docs/features/<name>/blocked_existant.md` (cmd 187) and greps `cadrage-produit/blocked_*.md` for the first time (cmd 290). Question: which name does the second time's blocking file take, and does anything check for it? Not settled by the agent file.

### D-11 — "it runs past 250 KB" — NOTE

- **Line 355**: *"🔴 **it runs past 250 KB**"* of `docs/PRODUIT_GLOBAL.md`.
- In this repository the file is 15 bytes. The number is a fact about another project's global, stated as a 🔴 rule in a file that runs on several projects (CLAUDE.md: *"the chain runs on several projects"*). The rule that matters — *never the file whole* — does not need the number.

### D-12 — Grid file locations — question

- **Line 40**: `GRILLE_EXISTANT.md` at invocation 3; the command passes `docs/process/GRILLE_EXISTANT.md` (cmd 180).
- The file exists at `docs-new/process/GRILLE_EXISTANT.md` only; `docs/process/` holds `GRILLE_CADRAGE_PRODUIT_V2.md` but no `GRILLE_EXISTANT.md`. If `docs-new/` is the staging area that replaces `docs/` with `.claude-new/`, nothing is wrong; if not, invocation 3's grid is missing at the path the command sends. Not a defect of the agent file — noted because the agent's stop rule (63–66: *"or nothing at all"*) is what would fire.

### Checked and found coherent

- Every `##`/`###` reference resolves: *"See What you write"* (256) → line 266; *"under What pass A left you"* (163) → exists in the grid; *"the same four lines"* (373) → 271–274; *"the usual two"* (350) → the table at 37–41.
- *"Four lines per question"* (276) and *"One more line"* (281) → the five-line shape at 283–287: counts match.
- The `Block:` rules (313–323) no longer contradict *"stands on its block alone"* (243): C8 closed it.
- Invocation 2's *"Every block"* (158, 162) reads as *every behaviour block* per line 135 — consistent, since the command names them all.
- The transverse-vs-block rule (262–264) and the never-do *"Answer a question the document does not answer"* (74–75) do not collide: the block's own rule is the document's answer.

---

## Summary

| Severity | Count | Items |
|---|---|---|
| BLOCKING | 0 | — |
| TO FIX | 7 | B-3, B-4, D-1, D-2, D-3, D-4, D-5 · plus C20 on the command side |
| NOTE | 8 | B-1, B-2, C (Glob unused, Grep unnamed), D-6, D-8, D-9, D-11, A-C6 example |
| Questions | 4 | D-7, D-10, D-12, A-C16 |

**Conformity**: all nine agent-side comments listed PASSÉ are applied, seven to the letter
(C1, C3, C4, C5, C7, C8, C22 in substance), C6 with its stale example; the three ÉCARTÉ
and the one REPORTÉ are correctly absent. The five structural modifications are present.
**What the edit broke** is the file's own bookkeeping: three counts (two invocations,
one stop, two files) went stale when §5 and C5 added what they count, one 🔴 rule (281)
contradicts the shape under it, and the *défaut*'s "pattern" branch (§3) collides with
three older rules that the edit left standing.
