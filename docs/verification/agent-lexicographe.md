# Verification — `lexicographe.md`

**Old**: `.claude/agents/lexicographe.md` (374 lines) · **New**:
`.claude-new/agents/lexicographe.md` (520 lines) · **Pass file**:
`docs/refonte/passes/lexicographe.md` (17 comments) · **Section**:
`docs/refonte/modifications.md` lines 20–41.

The section announces **no structural modification** ("aucune
modification du fichier de travail") except the `en anglais` line,
"décidée en séance" — so there is no "Ce qui a changé" table and no
"La demande". Everything verifiable is the pass sheet: 14 passed
(C1–C14), 2 discarded (C15, C16), 1 deferred (C17). Four of the passed
comments (C9's relay row, C12, C13, C14) target `1_lexique.md`; I
checked them in `.claude-new/commands/1_lexique.md`.

Line numbers below refer to the **new** agent file unless marked *old*
or *cmd*.

---

## A. Conformity

### C1 — the lexicon's shape, and a place for the inventory — PASSÉ

- **Expected**: a named place for the inventory (every domain term with
  its count), distinct from what awaits an answer; invocation 3
  compares against both; a second sweep rebuilds the inventory from the
  current idea file and keeps `## Tranché` untouched; the shape stated
  once, in Part 2, before either invocation uses it.
- **Found**: lines 133–208, `### What lexique.md holds`, in Part 2, with
  three sections (`## Tranché` / `## Non tranché` / `## Relevé`, line
  138); `## Relevé` defined at 195–197; invocation 3 compares against
  "`## Tranché` and `## Relevé` both" (427); invocation 1 rebuilds
  `## Relevé` (281–283) and "never touch[es]" `## Tranché` (288–290).
  The old example under invocation 2 (old 252–293) is gone, replaced by
  a reference (379). The command now counts `## Non tranché` lines only
  (cmd 141–144).
- **Verdict**: **applied as asked.**

### C2 — invocation 2 reads the lexicon and updates it — PASSÉ

- **Expected**: move 1 reads the lexicon with the questions file and the
  idea file; move 3 updates the lexicon (moves answered terms out of the
  unsettled place into `## Tranché`, keeps everything else).
- **Found**: 341–342 "Read the questions file, the idea file, and
  `lexique.md`. Those three, and nothing else."; 379–384 "Update
  `lexique.md` … You update it, you never rewrite it. Every `## Tranché`
  entry an earlier turn wrote stays exactly as it is — you move each
  answered term out of `## Non tranché` and into `## Tranché`, and you
  touch nothing else."
- **Verdict**: **applied as asked.**

### C3 — one term, two meanings — PASSÉ

- **Expected** (three parts): (a) the question **quotes every occurrence
  of the term, each identifiable**, so the answer can say which ones
  carry the second meaning; (b) a fourth reading exists; (c) invocation
  2 replaces only the occurrences the answer names, and the grep expects
  the term to remain elsewhere.
- **Found**: (b) 303–308 — four readings, the fourth "this one term
  carries two meanings" ✓. (c) 362–367 — "you swap the occurrences that
  carry that meaning, and them alone. The grep then expects the term to
  remain elsewhere" ✓. (a) 310–321 — **the opposite of what was
  asked**: "the entry shows the two meanings apart — one occurrence of
  each, with its sentence … ⚠️ Not every occurrence — one per meaning is
  what the answer needs, and a term appearing thirty times would make
  the question unreadable."
- **Verdict**: **partially applied; (a) deliberately inverted.** The
  inversion undoes the purpose of (c): with one occurrence per meaning
  shown, the answer can name *which side* holds a new term but cannot
  name *which of the thirty occurrences* carry it — and 365–367 then
  says "Which occurrences carry which meaning is the answer's to say —
  where it does not say, the choice is open and goes back as a
  question", whose shape (one per meaning) again gives the Product Owner
  no way to enumerate. Either the agent decides scope (the exact defect
  the pass file wanted removed) or the question loops. **TO FIX** — see
  D.3. Question: was the readability argument meant to replace the
  pass file's "each identifiable" by some other handle (a section name,
  a sentence number) that never got written?

### C4 — applying a quote answer in the idea file — PASSÉ

- **Expected**: an answer settling a quote adds or removes the quotes at
  every occurrence in the idea file; that is the one change allowed
  beyond a term swap; the `## Tranché` entry carries the text with its
  quotes and language, the concept beside it only when the answer named
  one.
- **Found**: 357–360, word for word; Part 2 173–174 for the entry's
  shape.
- **Verdict**: **applied as asked.**

### C5 — a retired term between quotes — PASSÉ

- **Expected**: not replaced, not counted as left over; grep expects
  none *outside quotes*; same at invocation 4.
- **Found**: 348–355 (invocation 2); 497–498 (invocation 4, "the same
  rule as invocation 2"); also 410 at invocation 3, which now owns the
  lexicon-retired replacement.
- **Verdict**: **applied as asked.**

### C6 — quote sweep on the answers — PASSÉ

- **Expected**: invocation 3 also runs the quote sweep on the answers;
  invocation 4 applies a quote answer in the answered file as invocation
  2 does in the idea file.
- **Found**: 448–455 (sweep 2, "The quotes", "Same test as invocation
  1"); 493–495.
- **Verdict**: **applied as asked.**

### C7 — answer-brought domain terms enter the inventory — PASSÉ

- **Expected**: new domain terms an answer brings are added to the
  inventory by invocation 3 or 4, without a question.
- **Found**: 442–446 (invocation 3, "But you add it to `## Relevé`");
  510–512 (invocation 4, "and every domain term your answers brought,
  to `## Relevé`").
- **Verdict**: **applied as asked** (by both invocations).

### C8 — the `Question:` line as context — PASSÉ

- **Expected**: the `Question:` line is context for reading its own
  answer; the sweep runs on the answers' words only; questions never
  edited.
- **Found**: 402–406, with the three examples the pass file gave.
- **Verdict**: **applied as asked.**

### C9 — invocation 3 replaces, invocation 4 runs only when 3 asked — PASSÉ

- **Expected**: invocation 3 replaces the lexicon's retired terms
  itself then sweeps; invocation 4 applies only 3's answers and runs
  only when 3 asked something; the write list allows `Answer:` fields
  at 3 and 4; the command's relay row splits in two.
- **Found**: 408–415 ("First, replace what the lexicon retires");
  481–483 and 489–491; table rows 104–105; 221–223; write list 66–68;
  cmd 226–227 ("3 asked something" / "3 asked nothing").
- **Verdict**: **applied as asked** — but two sentences from the old
  division of labour survived and now contradict it: 386–387 and
  422–424 still say invocation 4 runs the grep. See D.1, D.2.

### C10 — a blocked run writes nothing else — PASSÉ

- **Expected**: a blocked run writes the blocking file and nothing
  else — no questions file, no lexicon.
- **Found**: 85–89.
- **Verdict**: **applied as asked.**

### C11 — the write list names the blocking file — PASSÉ

- **Expected**: the list names the blocking file and the answered file's
  `Answer:` fields at 3 and 4.
- **Found**: 66–68.
- **Verdict**: **applied as asked.**

### C12 — the prompt names what the agent applies — PASSÉ (command)

- **Expected**: at 2 and 4 the prompt names the `questions-lexicographe`
  file to apply; the template carries the blocking file when its
  decision is filled; the idea file is named at 1 and 2 only.
- **Found**: cmd 95–104 (template with the three new slots); cmd
  107–113 (the two rules spelled out).
- **Verdict**: **applied as asked.** Nothing was needed on the agent
  side; its input table already had the idea file at 1 and 2 only.

### C13 — one passage on filing — PASSÉ (command)

- **Expected**: either the command files nothing before invoking and the
  stop row is the rule, or the git rule names the stop instead of a
  filing.
- **Found**: cmd 161–175 — "Decide the invocation first … Then file
  nothing you have not identified … Anything else at the root means a
  filing failed upstream — stop, and say which files … Never move one of
  them". The `git mv` block is gone.
- **Verdict**: **applied as asked** (the first alternative).

### C14 — the ended loop at the root — PASSÉ (command)

- **Expected** (two parts): (a) a `questions-lexicographe` file with no
  `### Q` alone at the root is the ended loop — the command says so,
  says `/2_structure`, invokes nothing; (b) the `desc-produit.md` stop
  names the same next step.
- **Found**: (a) cmd 57 ✓. (b) cmd 80–84 — the `desc-produit.md` stop
  for 1 and 2 still says what it stops and why, and **nothing about
  what to run instead**.
- **Verdict**: **half applied.** (b) missing. **TO FIX** (command).
- NOTE, adjacent and pre-existing: cmd 76 "After 4, the answered file is
  clean — run `/2_structure`" contradicts cmd 228 "4 wrote a new
  questions file → answer it, then `/1_lexique` again". Not in the pass
  sheet; flagged because I read the file.

### C15 — the two counts — ÉCARTÉ

- **Expected**: not applied.
- **Found**: the modifications.md reason says "le comptage de `retenu`
  avait déjà été retiré" — but the **old** command still counted it
  (old cmd 131–132 "`retenu` for what is settled") and the **new**
  command drops it (cmd 141–144). So the `retenu` count was removed in
  this refonte, not before. What remains is the count of `## Non
  tranché` lines, and the agent now fixes "one line each" for that
  section (286) and "one entry per answered question" for `## Tranché`
  (168) — which is, in effect, the first alternative of C15's remedy.
- **Verdict**: **not applied as a comment; largely obtained by C1 and
  the command edit.** The stated reason is inaccurate. NOTE.

### C16 — skip the re-sweep on an unchanged idea file — ÉCARTÉ

- **Expected**: not applied.
- **Found**: cmd 73–74 "After 2, run 1 again" and cmd 225 "2 wrote none
  → `/1_lexique` again" unchanged.
- **Verdict**: **correctly not applied.**

### C17 — a sweep too large for one context — REPORTÉ

- **Expected**: not applied.
- **Found**: no ceiling, no size-block; "When you cannot produce" (70–94)
  still blocks on "no idea file, an empty one" only.
- **Verdict**: **correctly not applied.**

---

## B. Unannounced changes

Every hunk of the diff was matched against C1–C11. Three things match
neither a numbered comment nor an announced modification.

### B.1 — the numbering rule of the questions file — NOTE

- Old 103–104: "your number: the highest at the root, or in
  `questions/lexicographe/` if the root holds none, plus one."
- New 110–113: "Your number: the highest `questions-lexicographe-NN.md`
  found in the root and in `questions/lexicographe/` together, plus
  one — ⚠️ your own prefix only. 📌 The root may hold another agent's
  file; its number is not yours."
- **What it changes**: the old rule took the root's highest number
  whatever the prefix (at invocation 4 the root holds another agent's
  file) and fell back to the folder only when the root held nothing —
  two readings, one of which collides at filing. The new rule is the
  max over both places, own prefix only. It is the remedy of
  **`passes/redacteur.md` comment 9**, propagated to four agents
  (`classeur`, `qualifieur`, `redacteur`, `lexicographe`), but the
  lexicographe's section of modifications.md does not mention it.
  Correct and beneficial; unannounced here.

### B.2 — the `en anglais` line — announced, no spec — NOTE

- Announced in the section header ("sauf la ligne `en anglais`, décidée
  en séance") but with no "La demande" to verify against.
- New 154–155 (example entry `segment fermé — retenu / en anglais :
  closed segment`), 176–189 (the line is the Rédacteur's alone; the
  lexicographe never writes or touches it; why it exists; the Rédacteur
  adds no entry), 430–432 (invocation 3 compares against it too).
- **What it changes**: the lexicon gains a line written by another
  agent. Checked against `.claude-new/agents/redacteur.md` 163–175 and
  308–310: the Rédacteur writes it "the first time he renders" a settled
  concept, takes it when present, and writes "anything in `lexique.md`
  but an `en anglais` line" is on his never-do list. **The two files
  agree.** One consequence inside this file is not handled — see D.4.

### B.3 — who reads the lexicon — NOTE

- Old 290–291: "by the Rédacteur, and by your own invocations 1 and 4."
- New 207–208: "by the Rédacteur, and by your own invocations 1, 3
  and 4."
- **What it changes**: a factual correction — invocation 3 always read
  it. The pass file noticed this in its "From the verdict" section
  (sweep row 3), not in a numbered comment. Correct.

Everything else in the diff is C1 (the moved and extended lexicon
section; invocation 1's "What you write"), C2 (invocation 2 moves 1
and 3), C3 (the fourth reading and the `### Q2` example), C4/C5
(invocation 2 move 2), C6/C7/C8/C9 (invocation 3 rewritten, invocation 4
move 2 and 3, the table, the loop paragraph), C10 (85–89), C11 (66–68).

---

## C. Gestures against tools

**Frontmatter** (line 4): `Read, Grep, Glob, Edit, Write`.

| Gesture | Where | Tool | Has it |
|---|---|---|---|
| Read the idea file, `lexique.md`, the questions file, the answered file, a named blocking file | 32–34, 100–105, 341, 487 | Read | ✓ |
| Count how many times each domain term appears | 245–247 | Grep (count) | ✓ |
| Grep each retired term in the idea file / in the answers | 353–355, 408–411 | Grep | ✓ |
| Find the highest `questions-lexicographe-NN.md` in the root and `questions/lexicographe/` | 110–113 | Glob | ✓ |
| Swap a term, add or remove quotes, in the idea file and in `Answer:` fields | 348–367, 408–415, 489–498 | Edit | ✓ |
| Create `lexique.md` (first sweep), the questions file, the blocking file | 72–73, 279–290, 330–331 | Write | ✓ |
| Move a term between sections of `lexique.md`, append to `## Relevé`, add `## Tranché` entries | 379–384, 442–446, 510–512 | Edit | ✓ |

- **Gesture with no tool**: none.
- **Tool no gesture uses**: none — Glob has exactly one use (the
  numbering rule); the other four are used throughout.
- No Bash, no Agent, and the file asks for neither.

---

## D. Internal coherence (new file alone)

### D.1 — line 386–387 — TO FIX

> 📌 **Invocation 4 greps the retired terms in every answered file** —
> ⚠️ **which is why they are written down, not dropped.**

Contradicts 408–411 ("First, replace what the lexicon retires. Each
term `lexique.md` lists under a retained one, grepped in the answers and
swapped" — invocation 3) and 489–491 ("Invocation 3 already replaced
what the lexicon retired — you apply your answers, and them alone" —
invocation 4). Old-division leftover; should read "Invocation 3".

### D.2 — line 422–424 — TO FIX

> 📌 **A retired term is caught by a grep, and invocation 4 runs it; a
> new synonym is caught by nobody**

Same contradiction, inside invocation 3 itself, twelve lines after the
paragraph that makes invocation 3 run that grep. Should read "and you
have just run it".

### D.3 — line 365–367 — TO FIX (procedure branch that leads nowhere)

> ⚠️ **Which occurrences carry which meaning is the answer's to say** —
> 🔴 **where it does not say, the choice is open and goes back as a
> question.**

The question shape this refers to (314–321) shows "one occurrence of
each [meaning]" and says "Not every occurrence". An answer to that shape
cannot enumerate occurrences it was never shown; sending it back "as a
question" produces the same shape and the same impossibility. The
branch either loops or the agent decides the scope itself — the case C3
was written to remove. Either the question lists every occurrence
(as the pass file asked) or the file says what handle the answer uses
to designate occurrences (a section, a sentence) — which one is a
decision, not mine.

### D.4 — line 409–410 vs 176 and 430 — TO FIX

> 🔴 **Each term `lexique.md` lists under a retained one, grepped in the
> answers and swapped**

After B.2, the lines "under a retained one" include `en anglais : closed
segment` (154–155) and, as before, `Roxzone : … retenu aussi` (146) and
`F. Carry : son abréviation …` (149). Read literally, invocation 3 greps
"closed segment" in the answers and swaps it for "segment fermé" — the
inverse of what 430–432 asks ("compare against it too: an answer naming
the same thing in English is the same pair"). Nothing in the shape
marks which indented line is a retired term (`remplace :`) and which is
a kept one. The old file had the same looseness for `Roxzone` and
`F. Carry`; the `en anglais` line makes it bite, because that word is
one the Product Owner will legitimately write in an answer. Question:
is `remplace :` meant to be the marker, and should 409 say "each term on
a `remplace :` line"? (This is the half of C15 that was discarded as
"sans objet".)

### D.5 — line 104 vs 474–475 — TO FIX (minor)

> | 3 | Watching | The answered file · `lexique.md` | The answered file,
> its retired terms replaced · a new questions file, always |

The table omits `lexique.md` as an output of invocation 3, while
442–446 has it write `## Relevé` and 474–475 lists "`lexique.md`, its
`## Relevé` updated" among the outputs. The table is what the reader
consults first.

### D.6 — lines 191–193, 285–286, 457–475, 510 — TO FIX (or question)

> 🔴 **`## Non tranché`** — what waits on an answer: a pair, a doubtful
> quote. 📌 **A term leaves it when an answer settles it**

Invocation 1 writes its pairs and doubtful quotes there (285–286).
Invocation 3 raises the same kinds of doubt (419–455) but its "What you
write" (457–475) names the questions file, the answered file and
`## Relevé` — **never `## Non tranché`**. Then invocation 4 says "Add
each settled term to `lexique.md`, in the shape invocation 2 uses"
(510), and invocation 2's shape is "move each answered term out of
`## Non tranché` and into `## Tranché`" (382–384) — there is nothing to
move. Two consequences: the command's "what still waits on an answer"
count (cmd 141–144) never sees an invocation-3 question; and "in the
shape invocation 2 uses" is a move for one invocation and an insertion
for the other. Question: should invocation 3 write its doubts under
`## Non tranché` like invocation 1, or is `## Non tranché` meant to be
the pre-product-file section only? The file says neither.

### D.7 — line 510 — NOTE

> **3. Add each settled term to `lexique.md`**, in the shape invocation 2
> uses

Invocation 2 no longer states a shape; it says "see *What `lexique.md`
holds*, Part 2" (379). The reference resolves transitively but points at
a place that has nothing.

### D.8 — lines 199–200 and 281–283 — NOTE (dead rule)

> ⚠️ **A sweep rebuilds what it found from the idea file** — 📌 **it never
> removes a term an answer brought**, which is in no sweep's reach.

Answer-brought terms enter `## Relevé` at invocations 3 and 4 only
(442, 511), which run after the product file exists (36–37); invocation
1 runs only before it. So no sweep ever meets a `## Relevé` term an
answer brought, and the rule guards a case the file's own sequencing
excludes. Harmless. If it were ever to matter, nothing in the
`## Relevé` line shape (163–166: `term — count`) tells an idea-file term
from an answer-brought one — and 442–446 gives no shape at all for the
latter (a count of what?). One line fixing the shape would settle both.

### D.9 — line 497–498 — NOTE

> ⚠️ **A retired term inside a displayed text stays** — 🔴 **the same
> rule as invocation 2.**

Invocation 4 borrows invocation 2's quote rule but not its
one-term-two-meanings rule (362–367), although invocation 3's questions
have "the same shape as invocation 1's" (460) and can carry the fourth
reading. Either invocation 4 applies such an answer by the same partial
replacement, or that reading cannot be raised at 3 — not stated.

### D.10 — line 87–89 — NOTE (cross-file, not a contradiction in the file)

> an empty questions file left there would send the next run to
> invocation 2, on a file nobody answered, and the sweep would never run.

After C14, the command routes an empty `questions-lexicographe` alone
at the root to "invoke nothing, say `/2_structure`" (cmd 57), not to
invocation 2. The outcome the rule prevents is still bad (the sweep
never runs, and the chain starts), but the mechanism described is the
old one.

### Counts and references checked, no finding

"Three sections" (138) → three · "Three sweeps" (243) → three · "Four
readings" (303) → four · "Three moves" (339, 485) → three each · "the
two sweeps" (417) → two · *Your questions file* (107) and *What
`lexique.md` holds* (133) both exist where referenced · "Part 2"
references (279, 379) land in Part 2.

---

## Summary

| Severity | Findings |
|---|---|
| BLOCKING | none |
| TO FIX | A/C3 + D.3 (one-term-two-meanings: question shape cannot feed the application rule) · A/C14(b) (command: `desc-produit.md` stop names no next step) · D.1, D.2 (two "invocation 4 greps" leftovers contradict C9) · D.4 (`en anglais` word read as a retired term) · D.5 (table row 3 omits `lexique.md`) · D.6 (invocation 3's doubts never reach `## Non tranché`) |
| NOTE | B.1 (numbering rule, unannounced here, from the Rédacteur's pass) · B.2 (`en anglais`, announced without spec, coherent with the Rédacteur) · B.3 · A/C15 (reason inaccurate: `retenu` count removed now, not before) · A/C14 adjacent (cmd 76 vs 228) · D.7, D.8, D.9, D.10 |

Tools: complete in both directions. Discarded and deferred comments:
none applied.
