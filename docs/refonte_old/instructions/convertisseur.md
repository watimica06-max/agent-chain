# Instructions — convertisseur

Verdict card 4.2: **changed** (D8). What the verdict asked for: a third
invocation, a fresh reader that did not write the technical document,
running the eight part-2 closures against the product file. What the
Analyste pass raised for this agent: the marks its questions entries
carry back (`[integrated: Bn]`, `[not product]`, `[unanswered]`), and
the `Default:` line every questions entry carries (D1, D2).

Applied top to bottom. `Cible` locates by section heading and quotes
the sentence; the line numbers in brackets are those of the file
before any instruction is applied, as a finding aid only.

---

## 1

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : frontmatter, `description` [line 3], last sentence
    Aujourd'hui  : "Two invocations, separated by a question round-trip."
    Après        : "Three invocations: one closes the product file, one
                   produces the technical document, one closes that
                   document as a reader that did not write it."
    Justification: robustness — a count that no longer matches the
                   card; the router matches on this sentence, and an
                   orchestrator reading "two" will never launch the
                   third.

## 2

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "Which invocation is this?", the table
                   [lines 40-43] and what precedes the grid line
    Aujourd'hui  : a two-row table (1 Closing · 2 Producing); nothing
                   says how the agent learns which invocation it runs.
    Après        : 🔴 **Your prompt names the invocation.** One run, one
                   invocation — invocation 3 reads what invocation 2
                   wrote, and a run that did both would read its own
                   work. A prompt that names none: block (see *When you
                   cannot produce*).

                   | # | Invocation | Inputs | Output |
                   |---|---|---|---|
                   | 1 | Closing the product file | The product file · the grid, part 1 | The next questions file · 🔴 deletes any technical document and any traceability file |
                   | 2 | Producing | Full production: the product file · the grid's *Traceability* section. Targeted update: the technical document · the questions-file entries its `<<ASSUMED` marks name · the product-file blocks those entries' `[integrated: Bn]` marks name | The technical document · `tracabilite.md` · a questions file |
                   | 3 | Closing the technical document | The product file · the technical document · `tracabilite.md` · the grid, part 2 | The technical document, corrected where the product file settles it · `tracabilite.md` · a questions file |
    Justification: robustness — the card's third invocation exists
                   nowhere in the file; and a missing stop: nothing
                   today tells the agent which invocation it is, so it
                   infers from the files it finds — invocation 3 and a
                   targeted invocation 2 see the same folder. The
                   one-run-one-invocation rule is what makes 3 a reader
                   rather than an author; without it the card's whole
                   point can be lost silently. Tokens — invocation 2
                   loads one grid section instead of the whole of part
                   2 (see 3).

## 3

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "Which invocation is this?", the grid line
                   [lines 45-47]
    Aujourd'hui  : "🔴 The grid is docs/process/GRILLE_FERMETURE_TECHNIQUE.md
                   — part 1 at invocation 1, part 2 at invocation 2.
                   It holds the closures; this file holds the moves."
    Après        : "🔴 The grid is docs/process/GRILLE_FERMETURE_TECHNIQUE.md
                   — part 1 at invocation 1, its *Traceability* section
                   alone at invocation 2, part 2 whole at invocation 3.
                   It holds the closures; this file holds the moves."
    Justification: tokens — invocation 2 keeps only the closure it
                   applies while writing (the one that produces the
                   `<<ASSUMED` marks) and stops paying for the seven
                   others at every production; robustness — the
                   loading matches the moves (see 12 and 18).

## 4

    Fichier      : .claude/agents/convertisseur.md
    Opération    : add a section
    Cible        : right after the files table and its "Nothing outside
                   that folder" line [after line 36], before "Which
                   invocation is this?"
    Aujourd'hui  : nothing — the reading rule sits inside invocation 1
                   move 1 and is restated, without its exception, in
                   invocation 2 move 2.
    Après        : ## Reading the product file

                   🔴 **Whole, once, never partially** — a calculation
                   rule can be described inside a screen section, and
                   the other way round.

                   ⚠️ **Except its closing section** — `## Questions set
                   aside` from the Analyste, `## Gaps set aside` from
                   the Diagnostiqueur. It records what was ruled out
                   and holds no product content. **Skip it, at every
                   invocation.**
    Justification: robustness — today only invocation 1 skips the
                   section that holds ruled-out questions; invocation 2
                   reads it "in full" and can translate a ruled-out
                   point or ask it again, the same fault the file
                   already guards against for `idees.md`. Tokens — one
                   rule, stated once, referenced three times (5, 14,
                   18).

## 5

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "INVOCATION 1 — Closing", move 1
                   [lines 149-155], the two paragraphs before the
                   natures table
    Aujourd'hui  : "**1. Read the product file in full, once.** 🔴 Never
                   partially — a calculation rule can be described
                   inside a screen section, and the other way round.
                   ⚠️ Except its closing section — ... Skip it."
    Après        : "**1. Read the product file** — as *Reading the
                   product file* says."
                   The natures table that follows stays as it is.
    Justification: tokens — the same thing said twice in one file,
                   once 4 exists.

## 6

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "INVOCATION 1 — Closing", move 3 [lines 185-187]
    Aujourd'hui  : "**3. Delete `spec-technique.md` if it exists.** 🔴
                   The product file has moved since it was written —
                   leaving it would send invocation 2 into a targeted
                   update on a document that no longer matches."
    Après        : "**3. Delete `spec-technique.md` and `tracabilite.md`
                   if they exist.** 🔴 The product file has moved since
                   they were written — leaving the document would send
                   invocation 2 into a targeted update on one that no
                   longer matches; leaving the traceability file would
                   let it be read as current by whoever reads it next."
    Justification: robustness — a move that reaches less than it
                   should: the traceability file is the document's
                   companion, and the card lists other readers of it
                   (the id-coverage check, the Architecte); a stale one
                   beside no document, or beside a document that a
                   later full production may never write (the "No"
                   case of *What a question costs*), reads as a result.

## 7

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "What raises a signal", first paragraph
                   [lines 127-129]
    Aujourd'hui  : "**A closure that fails**, by the closure grid —
                   docs/process/GRILLE_FERMETURE_TECHNIQUE.md, part 1
                   at invocation 1, part 2 at invocation 2. 🔴 Load it;
                   it is not in this file."
    Après        : "**A closure that fails**, by the closure grid —
                   docs/process/GRILLE_FERMETURE_TECHNIQUE.md, part 1
                   at invocation 1, *Traceability* at invocation 2,
                   part 2 at invocation 3. 🔴 Load it; it is not in
                   this file."
    Justification: robustness — two passages of one agent asking for
                   different things, once 3 is applied.

## 8

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "What raises a signal", "What does not raise
                   a signal" [lines 137-141], the words "a block
                   holding two subjects"
    Aujourd'hui  : "... a missing precision the product framing grid
                   already swept for, a block holding two subjects, and
                   never a judgement on product relevance."
    Après        : "... a missing precision the product framing grid
                   already swept for, a block holding two subjects of
                   one nature — two natures in one block is exactly
                   what the grid's *Nature* closure catches — and never
                   a judgement on product relevance."
    Justification: robustness — a test nobody can check as written: the
                   grid's *Nature* closure says a sentence producing
                   another nature's output becomes its own block, and
                   this line says two subjects in a block is not a
                   signal. One reader files the block, the other lets
                   it pass. Two readers, two verdicts.

## 9

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "Where questions files live" › "The shape of
                   every entry" [lines 102-112], the count, the example
                   and the `Answer:` rule
    Aujourd'hui  : "🔴 One entry per question, four lines, no exception.
                   Numbering restarts at Q1 in each file:
                       ### Q1
                       Block: B7 — Rejecting invalid durations
                       Question: what happens to an entry whose duration is zero?
                       Answer:
                   🔴 The `Answer:` line is written empty, and it is
                   never omitted — it is where the Product Owner
                   writes, by hand. An entry without it is unusable."
    Après        : "🔴 One entry per question, five lines, no exception.
                   Numbering restarts at Q1 in each file:
                       ### Q1
                       Block: B7 — Rejecting invalid durations
                       Question: what happens to an entry whose duration is zero?
                       Default: it is rejected, as a negative one is
                       Answer:
                   **`Default:` carries the answer the document takes
                   if none comes** — the assumption behind an
                   `<<ASSUMED` mark, the reading a closure would settle
                   on; 🔴 **`none` where no rule exists without the
                   answer.** A default proposes; it settles nothing —
                   the Product Owner consents or overrides.
                   🔴 The `Answer:` line is written empty, and it is
                   never omitted — it is where the Product Owner
                   writes, by hand. An entry without it is unusable."
    Justification: raised by the Analyste pass (`## Consequences
                   elsewhere`: whether the entries carry a `Default:`
                   line, D1, is this pass's matter). Round trips — a
                   question with a proposed answer is settled by
                   silence where the proposal holds, instead of a
                   written answer for each; robustness — the
                   assumption already sits inside the `<<ASSUMED` mark,
                   which the Product Owner never reads, and now sits
                   where she does read. Unsure: the `none` value for
                   the "No" case is my decision — an agent that has no
                   rule cannot propose one — and it has to hold on the
                   Analyste's side (silence over `none` integrates
                   nothing; see *Consequences elsewhere*).

## 10

    Fichier      : .claude/agents/convertisseur.md
    Opération    : add text
    Cible        : section "Where questions files live", at its end,
                   after "🔴 Write it even when empty ..." [after line 121]
    Aujourd'hui  : nothing — the marks the Analyste puts on the entries
                   of this agent's file are defined nowhere in it.
    Après        : ### What comes back

                   **After the Analyste's pass, every entry of your file
                   carries one mark:**

                   | Mark | Where the answer is |
                   |---|---|
                   | `[integrated: Bn]` | In block `Bn` of the product file — read it there, and only there |
                   | `[not product]` | In the entry's `Answer:` line, and nowhere else |
                   | `[unanswered]` | Nowhere — 🔴 **nobody re-asks it but you** |
    Justification: raised by the Analyste pass (D2: an integrated
                   answer is read from the product file, not from the
                   entry; an unanswered one is lost unless the asker's
                   next file carries it). Robustness — a term used and
                   never defined: the targeted update (15) acts on
                   these marks and cannot without knowing them; an
                   agent that reads only `Answer:` applies a stale or
                   empty text where the product file now carries the
                   answer.

## 11

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "Between the two — the round-trip", whole
                   [lines 195-221], title included
    Aujourd'hui  : the route table (`/1_structure`, `NEW`, `/2_grille`
                   → `/3_reclasse` → `/4_convertit`), the note on
                   `/3_reclasse` deleting the document, and three rules:
                   never re-ask a recorded answer, a fully answered file
                   is the stopping condition, a new problem joins the
                   next file.
    Après        : ## The round-trip

                   Every questions file goes to the Product Owner, who
                   fills `Answer:` by hand, then to the Analyste, who
                   carries each answer into the product file and marks
                   the entry — see *What comes back*.

                   **Invocation 1's questions come back to invocation
                   1**, which closes the product file again.
                   **Invocation 2's and 3's questions come back to
                   invocation 2**, as a targeted update.

                   🔴 **A question whose answer is recorded is never
                   asked again.** The stopping condition is a fully
                   answered questions file, not a number of rounds.

                   ⚠️ **If an answer surfaces a new problem**, it joins
                   the next questions file. That is normal, not a
                   failure.
    Justification: robustness — the route table is false once a third
                   invocation exists: "straight to the invocation that
                   asked" would send an invocation-3 question back to
                   invocation 3, which never applies an answer. Tokens
                   — command names and routes no move of this agent
                   uses, paid at every invocation; the orchestration
                   owns them.

## 12

    Fichier      : .claude/agents/convertisseur.md
    Opération    : drop a move
    Cible        : section "INVOCATION 2 — Producing": the count
                   [line 227] and move 3 [lines 272-274]
    Aujourd'hui  : "**Three moves.**" ... "**3. Run part 2 of the
                   closure grid, once every section is filled** — 🔴
                   not while writing — and treat what it returns by the
                   table below."
    Après        : "**Two moves.**"; move 3 dropped. At the end of move
                   2, after "the closure grid's *Traceability* draws
                   the line.", add: "What *Traceability* draws out — a
                   sentence of yours you cannot point at a product
                   sentence for — is treated by *What a question
                   costs*, below. 🔴 **The seven other closures of part
                   2 are not yours to run**: they run at invocation 3,
                   on the finished document, by a reader that did not
                   write it."
    Justification: robustness — the card's move 3: the author's own
                   closure misses what the author wrote; the check
                   moves to a fresh context. The count matches again,
                   and the table "What a question costs" keeps an
                   anchor now that the move that pointed at it is gone.

## 13

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "INVOCATION 2 — Producing", move 2, the
                   sentence "Two regimes, two invocations" [lines 265-267]
    Aujourd'hui  : "⚠️ Two regimes, two invocations: closing reads
                   without writing, production translates into
                   technical terms."
    Après        : "⚠️ Two regimes: closing raises, production
                   translates into technical terms — invocation 3
                   corrects, but only what the product file already
                   settled."
    Justification: robustness — a count that no longer matches, and a
                   sentence that would read invocation 3 as writing
                   nothing (see 18).

## 14

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "INVOCATION 2 — Producing", move 2, first
                   sentence [lines 255-257]
    Aujourd'hui  : "**2. On a full production, take the updated product
                   file**, which carries the answers. 🔴 Read it in
                   full, once — a calculation rule can be described
                   inside a screen section, and the other way round."
    Après        : "**2. On a full production, take the updated product
                   file**, which carries the answers. 🔴 Read it as
                   *Reading the product file* says."
    Justification: tokens — the rule stated twice; robustness — this
                   reading now skips the closing section (4).

## 15

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "INVOCATION 2 — Producing", move 1: the
                   "Exists" row [line 235], the paragraph "On a targeted
                   update, read only the questions file each mark
                   names" [lines 237-238], the paragraph "A mark whose
                   answer is still empty" [lines 245-246] and the
                   paragraph "An answer that does not settle the mark"
                   [lines 248-251]
    Aujourd'hui  : row: "Exists → 🔴 Targeted update only — grep
                   `<<ASSUMED`, replace each mark with its answer, touch
                   nothing else". Then: "read only the questions file
                   each mark names — the answer is there, at the entry
                   the mark identifies." Then: "A mark whose answer is
                   still empty stays as it is. Say which ones remain."
                   Then: "An answer that does not settle the mark —
                   ambiguous, or beside the point — leaves the mark in
                   place and becomes a new question, in a new file.
                   Rewrite the mark to carry that new identifier ..."
    Après        : row: "Exists → 🔴 **Targeted update only** — grep
                   `<<ASSUMED`; for each mark, read the entry it names
                   and act by that entry's mark; **touch no other
                   entry**".

                   Then, replacing the three paragraphs:

                   📌 **Where the answer is, the entry's mark says** —
                   see *What comes back*: `[integrated: Bn]` → block
                   `Bn` of the product file, read alone; `[not product]`
                   → the entry's `Answer:` line.

                   🔴 **Apply it at the entry the mark sits in**: replace
                   the mark's text with the answer, or rewrite the
                   sentence the mark qualifies when the mark says the
                   rule depends on the answer. No other entry moves; no
                   entry is renumbered.

                   ⚠️ **`[unanswered]`, or an answer that does not
                   settle the mark** — ambiguous, or beside the point:
                   the mark stays, the question is asked again in this
                   invocation's file, and 🔴 **the mark is rewritten to
                   carry the new identifier**, so it still points at
                   where its answer will come from. Say which ones
                   remain.
    Justification: raised by the Analyste pass (D2, and the
                   `[unanswered]` mark: "the asker's next file has to,
                   or the question is lost"). Robustness — today the
                   agent reads the answer from the questions file where
                   the product file now carries its integrated form,
                   and leaves an unanswered mark silently in place,
                   which no later invocation will ask again; and
                   invocation 3's marks (18) can qualify a whole rule,
                   which "replace the mark" cannot apply. Round trips —
                   a lost question is a round paid later, after the
                   Cadreur has cut on the assumption.

## 16

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "The traceability file", last paragraph
                   [lines 323-324]
    Aujourd'hui  : "🔴 On a targeted update, leave it as it is. A mark
                   replaced by its answer changes no rule's origin."
    Après        : "🔴 On a targeted update, one change only: a block
                   named by `[integrated: Bn]` whose line does not yet
                   cite the entry the mark sat in gains that entry. A
                   mark replaced by its answer changes no other rule's
                   origin."
    Justification: robustness — with D2, an answer may be integrated
                   into a block other than the one the entry was
                   written from; the entry then carries a rule of that
                   block, and the file that says which blocks each
                   entry carries rules from would say otherwise to the
                   id-coverage check and the Architecte, who read it.

## 17

    Fichier      : .claude/agents/convertisseur.md
    Opération    : replace text
    Cible        : section "What a question costs": its first line
                   [line 278] and the paragraph "Both cases write the
                   question the same way" [lines 294-295]
    Aujourd'hui  : "**Ask yourself: without this, can I write the rule
                   at all?**" ... "📌 Both cases write the question the
                   same way — a new entry with an empty `Answer:` field.
                   **Say which of the two you are in.**"
    Après        : "**At invocation 2, for every sentence *Traceability*
                   leaves you unable to source, ask yourself: without
                   this, can I write the rule at all?**" ... "📌 Both
                   cases write the question the same way — a new entry
                   with an empty `Answer:` line; its `Default:` carries
                   the assumption in the second case, `none` in the
                   first. **Say which of the two you are in.**"
    Justification: robustness — once 12 is applied this table is no
                   longer reached from a move; it has to say what it
                   treats and where, or a reader applies it at
                   invocation 3, where the "No" row deletes a document
                   a reader must never delete (18). The `Default:` line
                   follows 9.

## 18

    Fichier      : .claude/agents/convertisseur.md
    Opération    : add a section
    Cible        : after the section "The technical document" (after
                   "**Write in English.**" and its rule [line 441]),
                   before "When you cannot produce"
    Aujourd'hui  : nothing
    Après        : ## INVOCATION 3 — Closing the technical document

                   You are the reader invocation 2 never had. 🔴 **You
                   did not write this document.** You read it as a
                   stranger, against the product file.

                   **Four moves.**

                   **1. Read the product file** — as *Reading the
                   product file* says — **then `spec-technique.md` and
                   `tracabilite.md`, whole.** 🔴 **No `spec-technique.md`
                   → block**: invocation 2 produced nothing, and there
                   is nothing to close.

                   **2. Run part 2 of the grid, in the grid's order** —
                   the six closures that test an entry, on every entry;
                   the two sweeps, *Nothing dropped* and *Agreement
                   between entries*, once on the whole. 📌 A `—` line of
                   `tracabilite.md` is where *Nothing dropped* looks
                   first. 🔴 **A failure never stops the rest.**

                   📌 **A `<<ASSUMED` mark is an open point already
                   asked.** The entry is closed on what it says; the
                   mark's question is not asked again, and the mark is
                   not a *Traceability* failure.

                   **3. Treat each failure by one test — does the
                   corrected sentence pass *Traceability*?** Can you
                   point at the product sentence, or the grid rule, the
                   correction follows from, adding nothing the product
                   did not settle?

                   | The answer | What you do |
                   |---|---|
                   | **Yes** | **Correct the document.** A dropped member written out; a duplicate replaced by a reference to the owning entry; an undeclared link declared; a false reference pointed at the entry that carries it; a missing resource entry appended; a rule living where it is seen appended to its owning section, the old entry becoming the reference |
                   | **No** | **A question** in this invocation's file, and an `<<ASSUMED` mark at every entry concerned, carrying the question's identifier and what is open. **The entry stands as written** |

                   🔴 **An entry you append takes the next number of its
                   section, and a line in `tracabilite.md` for every
                   block it comes from.** 🔴 **No entry is renumbered,
                   none is deleted, and the document is never deleted
                   here** — a question leaves it standing, marked.

                   **4. Write the questions file** — see *Where
                   questions files live*. **Empty, it says *closed*.**
    Justification: the card's move 3 (D8). Robustness — the author's
                   closure misses what the author wrote; a reader with
                   no memory of writing it catches the dropped member,
                   the two reformulations that disagree, the false
                   reference. Round trips — a failure whose correction
                   the product file already settles is corrected, not
                   asked: a question the reading answers is an
                   avoidable round trip (the person, the Analyste, a
                   targeted update, for zero product information); and
                   the reader never deletes the document, so no
                   closure failure costs a full re-production. Tokens —
                   a marked entry and a targeted update in place of a
                   full production. Unsure: (a) the grid's "A failure
                   is a question, never a fix" was written for the
                   author; letting the reader correct what the product
                   settles extends the grid's own *Resources* exception
                   and its reasoning ("writing it is not deciding") —
                   noted for the grid below; (b) a correction made by
                   the reader is itself read fresh by nobody — it is
                   reported (19) so it can be challenged.

## 19

    Fichier      : .claude/agents/convertisseur.md
    Opération    : add text
    Cible        : section "What you report", after "A signal is
                   reported as a question already written" [after line 488]
    Aujourd'hui  : nothing on corrections
    Après        : "🔴 **At invocation 3, every correction you made**:
                   the entry, the closure that failed, the product
                   sentence or grid rule the correction follows from.
                   A correction nobody sees is a decision nobody can
                   challenge."
    Justification: robustness — 18 lets a reader change the document;
                   the report is the only place the change is visible
                   without diffing the document. Tokens — a list of
                   corrections is smaller than the diff a reader would
                   otherwise have to make.

## 20

    Fichier      : .claude/agents/convertisseur.md
    Opération    : add to a list
    Cible        : section "What you never do", after "Re-sweep what
                   the upstream chain covered" [after line 504]
    Aujourd'hui  : no entry matches the rules 2 and 18 add
    Après        : - 🔴 **Run two invocations in one run** — the reader
                     of invocation 3 is never the author of invocation 2
                   - 🔴 **Change, at invocation 3, anything the product
                     file or the grid does not settle** — that is a
                     question, with a mark
                   - 🔴 **Delete the technical document at invocation 3**
    Justification: robustness — rules in the body with no matching
                   entry in the list an agent checks itself against;
                   the three are the ones that, broken, void the third
                   invocation silently.

---

## Consequences elsewhere

The technical closure grid (`docs/process/GRILLE_FERMETURE_TECHNIQUE.md`)
: its closing line, "A failure is a question, never a fix. The one
exception is *Resources*", was written for an author closing its own
document. With a fresh reader (18) the agent corrects any failure whose
correction the product file or the grid already settles — a dropped
member, a duplicate, an undeclared or false link, a rule living in the
wrong section — on the grid's own *Resources* reasoning ("writing it is
not deciding"). The grid's sentence and the agent's move now disagree;
one of them has to move, and I left the grid alone. Also, "Part 2 —
eight closures, once every section is filled. Not while writing" now
reads as one invocation's work; the *Traceability* section is loaded
alone at invocation 2 (3), which the grid's structure allows but its
"Running it" section does not say.

The command that runs the cycle (and whatever launches the third
invocation) : (a) invocation 3 is a separate run, launched after each
full production of invocation 2 and never after a targeted update
(card: "3 once per full production"); the prompt names the invocation
(2) — an unnamed one blocks. (b) A targeted update that rewrote a rule
from an invocation-3 answer (15) is read fresh by nobody; the card's
"once per full production" leaves it so. (c) Invocations 2 and 3 each
write a questions file before any answer comes back; the Analyste pass
(its entry 5) says the Analyste blocks on two unconsumed files at the
feature root — file invocation 2's before launching 3, or the Analyste
blocks. (d) Do not launch invocation 3 when invocation 2 wrote no
document (its "No" case): the agent blocks on the missing file. (e)
The document handed on may carry `<<ASSUMED` marks — from invocation 2
or 3 — until every answer is in; whether the Cadreur is launched on a
marked document is the command's rule, not this agent's. (f) The
questions loop has no ceiling inside the agent — a fully answered file
ends it — and invocation 3 holds the product file, the technical
document and part 2 whole, with nothing signalling an overflow; both
are the command's to bound, as the Analyste pass already noted for its
own loop.

Analyste : (a) the Convertisseur now reads block `Bn` from
`[integrated: Bn]` and the `Answer:` line from `[not product]`, and
re-asks `[unanswered]` itself (10, 15) — the marks' names and meanings
are taken verbatim from the Analyste pass; if that pass's names change,
these do too. (b) The `Default:` line is `none` where no rule exists
without the answer (9); silence over `none` must integrate nothing —
unsure how D1's silence-as-consent reads that. (c) The Convertisseur
relies on each block's reference line — "the outgoing references
carried on each block", a reference "marked *existing*" (agent file,
invocation 2 move 2) — whose shape the Analyste writes and the
Convertisseur's file never describes; I could not describe it without
the product file's format. Left for the reconciliation pass: either the
Analyste's pass names the shape, or the Convertisseur's file quotes it.

Cadreur : entries appended by invocation 3 (a missing resource, a rule
moved to its owning section) sit at the end of their section with the
next number; the old entry of a moved rule becomes a reference, not a
gap — numbering holds across runs. `<<ASSUMED` marks may remain in the
document it receives (see the command, e).

Architecte : the technical document and `tracabilite.md` may gain
entries at invocation 3 — it should read them after 3, not after 2
(the verdict's loop 5.3 "Convertisseur → Architecte" does not say
which invocation).

The verdict card 4.2 : "Reads: spec-technique.md (targeted update;
closing)" — a targeted update now also reads the product-file blocks
that `[integrated: Bn]` names (D2, via the Analyste pass), and
invocation 2 reads the grid's *Traceability* section rather than part 2
whole.
