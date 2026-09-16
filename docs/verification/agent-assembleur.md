# Vérification — `assembleur.md`

Old: `.claude/agents/assembleur.md` · New: `.claude-new/agents/assembleur.md`
Pass file: `docs/refonte/passes/assembleur.md` (8 comments, `### 1` … `### 8`)
Section of `docs/refonte/modifications.md`: lines 512–538 — table + pass sheet
(Passés 8, Écartés 0, Reportés 0). **No "La demande"** for this agent.

Line numbers below refer to the **new** agent file unless a path says
otherwise. C6, C7 and C8 target `commands/4_grille.md`; they are checked
against `.claude-new/commands/4_grille.md`.

Summary: 6 of 8 defects fixed as asked; **C3 fixed in Part 3 only and
left standing in Part 1** (the file now carries both readings the comment
set out to remove); C7 leaves two loose ends. Two internal contradictions
in the new file, one of them new (lines 134 vs 143).

---

## A. Conformity

### C1 — tie rule keeps the covering question · PASSÉ

- Expected: when one question's answer closes the other and not the
  reverse, keep the covering one; only when each closes the other does
  wording decide.
- Found: lines 194–206, "**Which of the two you keep**" — "The one whose
  answer closes the other … the reverse does not hold"; "The covering
  question, never the narrower one"; "Only when each answer closes the
  other does wording decide — keep the one that states it most
  precisely. Never rewrite either." The file's own date/leading-zero
  example (lines 187–189) is reused to show the direction (lines 196–199).
- Verdict: **CONFORME**, as asked.

### C2 — multi-block question dropped only against a twin naming every block · PASSÉ

- Expected: (a) a multi-block question with a twin in one group and none
  in another stays; (b) drop only against a twin whose `Block:` line names
  every block the dropped one names; `Block:` stays uneditable.
- Found: lines 164–168 "dropped only against a twin whose `Block:` line
  names every block it names … `Block: B12, B15` is not dropped against
  `Block: B12`"; lines 170–172 "A multi-block question with a twin in one
  group and none in another stays"; line 233 "Everything else is copied
  as written" kept.
- Verdict: **CONFORME**. One stale word — see D.4 ("however precise that
  one is" refers to the old tie criterion).

### C3 — one reading of "same": the file a question came from is no part of the test · PASSÉ (listed)

- Expected (pass file, "Ce qu'il faut"): "one reading, stated once: the
  file a question came from is not part of the test … **the forbidden
  line should say 'a gap raised once', not 'a sondeur alone'**."
- Found: Part 3 fixed — lines 208–211: "A gap no other question's answer
  closes is kept, always … which file a question came from is no part of
  it: two questions of one reading that one answer closes are one
  question." But Part 1 unchanged:
  - line 3 (frontmatter description): "dropping what two of them raise
    twice" — counts sondeurs;
  - lines 20–21: "A gap one sondeur alone raised is what running several
    is for — it stays";
  - line 42, "What you never do": "**Drop a question raised by one
    sondeur only**" — the exact line the comment asked to reword.
- Verdict: **PARTIEL — TO FIX.** The defect was "one agent drops them, the
  next keeps them" because the file stated two tests. It now states both
  tests *and* a sentence saying the second is the one — line 42 still
  forbids, as a 🔴 rule, what line 211 mandates (a same-file pair is two
  questions "raised by one sondeur only"; dropping one breaks line 42).
  modifications.md's "8 sur 8" overstates this one.

### C4 — input shape stated; unplaceable question / malformed file are stops · PASSÉ

- Expected: state the shape (heading, `Block:` and its two forms,
  `Question:`, empty `Answer:`), define an empty file, make an unplaceable
  question or a malformed file a stop in `blocked_assembleur.md` naming
  file and passage, never a guess; missing-file line may stay.
- Found: new section "## The shape of a question you read", lines
  101–147: shape (105–108), `Block:` forms and `-` meaning (110–112),
  `Défaut:` line (114–125), empty file (134–135), stops (137–143), "Never
  a guess" (145–147). Missing-file line kept (line 31). The blocking file's
  `## Where` already asks for "the block, the file, the passage" (line 61).
- Verdict: **CONFORME** on the request. ⚠️ But the definition chosen for
  "empty" contradicts the stop list one paragraph later — see D.2. Checked
  against the producer: `.claude-new/agents/sondeur.md` lines 271–308
  writes exactly this shape (`### Qn` / `Block:` / `Question:` /
  optional `Défaut:` / `Answer:`, `Block: B12, B15`, `Block: -`).

### C5 — tools reduced to Read, Write · PASSÉ

- Expected: `tools: Read, Write`.
- Found: line 4 `tools: Read, Write`.
- Verdict: **CONFORME.**

### C6 — blocking-file check before the merge (command) · PASSÉ

- Expected: between "wait for all four" and the merge, any
  `cadrage-produit/blocked_*.md` at its unnumbered name → no merge, no
  root questions file.
- Found: `.claude-new/commands/4_grille.md` lines 290–296, first thing in
  "## Then the merge": "First, does any `cadrage-produit/blocked_*.md` sit
  at its unnumbered name? One is enough — no merge this turn, and no
  questions file at the root. Relay it and stop."
- Verdict: **CONFORME.** NOTE (command, not the agent): lines 294–296 say
  "A sondeur that blocked can still have left a file — whole or partial.
  The existence check below would pass it", and lines 308–309 say "A
  sondeur that blocked writes no questions file — so the existence check
  fires on it." The two sentences assert opposite facts twelve lines
  apart. Which one is true is what the pass file's "What another agent
  would settle" left to `sondeur.md` — the command now asserts both.

### C7 — the command edits no line of the questions file; the count leaves it · PASSÉ

- Expected: either the prompt names the final destination, or the count
  leaves the questions file (report or own file) and the renumber line
  goes; the relayed counts come from a named place.
- Found — option 2 taken:
  - agent lines 238–239 "Nothing else in that file"; 244–249 "The count
    goes in your report"; 254–256 the rationale; 241–242 no question →
    "write it empty".
  - command: "Renumber `Q1` upward" and "Drop its closing `## Merge`"
    gone; line 351 "The assembleur numbers from `Q1` and writes no working
    section"; line 347 the copy is `cp`, byte for byte.
- Verdict: **CONFORME on the substance.** Two loose ends the comment
  named and that remain:
  - NOTE — agent line 215 "`<out>/questions.md`, where `<out>` is the
    prompt's" (a folder) vs command line 320 "Write to
    docs/features/<name>/cadrage-produit/questions.md" (a file path). The
    pass file listed this mismatch under "Aujourd'hui"; it is unchanged on
    both sides. Harmless in practice, but the two files still describe the
    same parameter differently.
  - TO FIX (command) — line 440 "How many questions each reading raised,
    and how many the merge kept" names no source. The comment asked that
    "the counts the command relays come from a named place (the report,
    or a grep of the count lines)". The agent's report is that place; the
    command does not say so.

### C8 — a settled `blocked_assembleur.md` re-runs the merge alone (command) · PASSÉ

- Expected: no archiving, no sondeur; the relay row says so; the git
  section leaves the four files in place in that case.
- Found: command lines 62–70 "The assembleur's → the merge alone, on the
  four files still standing … Leave them in place, do not file them";
  line 449 relay row "the merge alone runs, on the four files still
  standing"; line 57 "invoke that reading alone".
- Verdict: **CONFORME.** NOTE — the exception lives in "Before anything
  else" (line 69); the "## Git, in this mode" section itself (lines
  373–379) still says unconditionally "And the previous turn's six
  `cadrage-produit/` files: `git mv …`". An orchestrator reading the git
  section as a checklist files the four files the merge is about to read.
  The comment asked for the exception in the git section.

### Écartés / Reportés

None listed; nothing to check for non-application.

---

## B. Unannounced changes

Diff old → new. Everything matching a defect above or a row of the
modifications.md table is excluded. What remains:

### B.1 — "sondeur" → "reading" in two places · NOTE

- Old line 140: "That is what running several is for"
  New line 209: "That is what running several **readings** is for"
- Old line 169: "no note on which **sondeur** found what"
  New line 252: "no note on which **reading** found what"
- What it changes: vocabulary only, in the direction of C3 (a reading, not
  a sondeur, is the unit). Consistent with Part 3; inconsistent with Part 1,
  which kept "sondeur" (lines 16, 20–21, 34, 42). Not asked by any comment.

### B.2 — `Défaut:` handling · announced in modifications.md, not in the pass file

- New lines 114–132 (input side) and 222–229 (output side): the `Défaut:`
  line, copied never written/removed/judged; "The kept question keeps its
  own `Défaut:` line, or has none … never move a `Défaut:` from the
  dropped question to the kept one."
- This is the table row "La forme d'entrée … ligne `Défaut:` comprise — et
  un défaut ne migre jamais vers la question gardée". Announced, so not an
  unannounced change — listed here because no pass comment asked for it
  and its interaction with C1 is not settled: see D.6.

### B.3 — new rationale paragraph · NOTE

- New lines 254–256: "Why not in the questions file: its only reader would
  have to strip it before the Product Owner sees it — a content edit by a
  command that may not read that file."
- What it changes: nothing operative; it is C7's justification carried
  into the agent. Fine.

### B.4 — the "no question at all" rule moved and reworded · covered by C7

- Old lines 171–173 (end of file, "the file holds the `## Merge` count
  alone") → new lines 241–242 ("write it empty"), now placed before the
  count paragraph instead of after. Consequence of C7; no other effect.

No renumbering, no moved `##` section, no rewritten table (the file has
none). Parts 1 and 2 are byte-identical to the old file except the
frontmatter `tools` line.

---

## C. Gestures against tools

Frontmatter: `tools: Read, Write`.

| Gesture (line) | Tool | Status |
|---|---|---|
| Read the named files whole (91) | Read | OK |
| Read the blocking file the prompt names (91–92) | Read | OK |
| Detect a missing file and stop (31) | Read fails → stop | OK |
| Write `<out>/questions.md` (215) | Write | OK |
| Write `blocked_assembleur.md` (50) | Write | OK |
| Report the count (244–249) | reply text, no tool | OK |
| Group / compare / choose (149–211) | reasoning, no tool | OK |
| "Never inferred from the folder" (94) | absence of Glob/Grep | holds by construction, as C5 intended |

- Gesture with no tool: none.
- Tool no gesture uses: none. Both tools are load-bearing.
- NOTE — on a resume (blocking file with a filled decision) the agent
  overwrites a `questions.md` only if one exists; it blocks *instead of*
  writing, so normally none does. If the harness's Write refuses to
  overwrite an unread file, the agent has Read. No gap.

---

## D. Internal coherence (new file alone)

### D.1 — Part 1 vs Part 3 on what is never dropped · TO FIX

- Line 42: "🔴 **Drop a question raised by one sondeur only**" (forbidden)
- Line 20–21: "A gap one sondeur alone raised is what running several is
  for — 🔴 it stays."
- Line 210–211: "which file a question came from is no part of it: two
  questions of one reading that one answer closes are one question."
- A same-file pair: each question was raised by one sondeur only; line 211
  drops one, line 42 forbids it. Same as C3, restated here because it is
  now a contradiction inside one file, not a vagueness.

### D.2 — what an empty file is vs what stops you · TO FIX

- Line 134–135: "An empty file is a file with no `### Q` — 🔴 whatever
  else it holds."
- Line 142–143: "A file that is neither empty nor a list of questions in
  that shape — 📌 a sondeur's prose, a heading with no entry under it."
- A file holding only prose ("nothing found") has no `### Q` → empty by
  line 134 → counts, brings no question. Line 143 names that same file as
  a stop. The pass file (C4) listed "a sondeur's prose 'nothing found'"
  as a case to stop on; line 134 decides it the other way and line 143
  keeps the old example. One of the two has to go. ("A heading with no
  entry under it" is coherent on its own: a `### Q1` with nothing under it
  has a `### Q`, is not empty, is not in shape → stop.)

### D.3 — "the count at the end" · NOTE

- Line 146–147: "and the count at the end would read as complete."
- The count is no longer at the end of anything the Product Owner sees
  (lines 244–249: it is in the report). Reads as a leftover of the old
  `## Merge` section. Harmless, but the phrase points at a place that no
  longer exists.

### D.4 — "however precise that one is" · NOTE

- Line 165–166: "`Block: B12, B15` is not dropped against `Block: B12`,
  however precise that one is"
- Under C1 precision decides only a mutual tie (line 204); the criterion
  that would otherwise drop the multi-block question is now *coverage*
  (line 196). The clause argues against a rule the file no longer has.
  Should read "however much its answer covers" or similar.

### D.5 — C1 and C2 can both forbid a drop with no rule saying the outcome · QUESTION

- Q1 `Block: B12, B15` narrow; Q2 `Block: B12` covering (Q2's answer
  closes Q1, not the reverse). Line 196: keep Q2, drop Q1. Line 164: Q1
  is not dropped against Q2 (Q2 does not name B15). Line 201: Q2 is not
  dropped for its narrower twin. Result: both kept — consistent with "in
  doubt, keep both" (191) but nowhere stated, and `Block:` is uneditable
  (233) so the covering question cannot absorb B15. Is "both stay" the
  intended outcome? If so, one line saying it would spare a reader working
  it out from three rules.

### D.6 — a `Défaut:` on the dropped question · QUESTION

- Lines 129–132: the kept question keeps its own `Défaut:` or has none.
- Case: Q_a covering without `Défaut:`, Q_b narrower with one. C1 keeps
  Q_a; the proposal the corpus already held is lost and the Product Owner
  answers by hand what the sondeur had already founded. The file is silent
  on whether a `Défaut:` weighs in the choice. Intended (the answer
  founded on Q_b "may not found" Q_a — line 131–132), or an unpriced loss?
  Not a verdict; a question for the author.

### D.7 — "in block order" for a multi-block question · NOTE (pre-existing)

- Line 231: "Numbering restarts at `Q1`, in block order."
- A kept `Block: B12, B15` question sits in two groups; the file says it
  is "kept once" (161) but not in which group's position it is written.
  And "block order" for an agent that never opens the product file can
  only mean identifier order; not said. Same in the old file.

### D.8 — description vs Part 2 · NOTE (pre-existing)

- Line 3: "Reads question files only" — line 91–92 adds "plus a blocking
  file, when it names one". Old file identical; unchanged.

### Counts and references

- Line 53 "four headings": four listed. OK.
- No `##`/`###` reference to a section that does not exist. The bold
  pseudo-headings (**Which of the two you keep**, **What stops you**,
  **The count goes in your report**) are never referred to by name.
- Every "What stops you" branch (139–143) leads to the Part 1 blocking
  file (50). Every "no question" branch (241) leads to a write. No branch
  leads nowhere.
