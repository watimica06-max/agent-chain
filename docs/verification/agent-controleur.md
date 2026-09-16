# Vérification — `controleur.md`

Old: `.claude/agents/controleur.md` · New: `.claude-new/agents/controleur.md`
Pass file: `docs/refonte/passes/controleur.md` (15 comments, `### 1` … `### 15`)
Section of `docs/refonte/modifications.md`: lines 1241–1275 — pass sheet
only (Passés 11: C1–C10, C15 · Écartés 1: C14 · Reportés 3: C11–C13) and a
"Les plus structurants" table. **No "La demande"** for this agent
("aucune modification du fichier de travail").

Line numbers below refer to the **new** agent file unless a path says
otherwise. Comments 6 to 12 have a half on `commands/9_controle.md` (and
comment 12 on `8_code.md`); the command half is checked against
`.claude-new/commands/9_controle.md` and reported apart, since the A4/A5
rewrite of the commands (named by the sheet as the home of C11–C13) may
be what settles it.

Summary: the blocking mechanism is gone as asked (C3, C5), the assembly now
holds groups and block list (C6, C7), the Missing/Doubtful boundary is
stated (C1). But **four "passé" comments are only half applied in the
agent file** — C1 (the `B8` example still files a Missing as a doubt), C2
(the old "unit is the sentence" rule and "the block is missing" survive
beside the new rule), C4 (the merged-lot paragraph asked to go is still
there), and C15 (listed passé, **not applied at all**: "working folder"
stands in three places, undefined). **The sheet's numbering drifts from
the pass file at 13/14**, so what was decided on comment 14 (the
`Edit`/never-do clean-up, which the new file half-applies) is not
readable. One unannounced structural change: the `# PART 3 — What you do`
heading vanished with the section deleted above it, and both invocations
now sit under "PART 2 — Which call is this". On the command side, C8, C9
and C10 are listed passé and are not applied; C8's absence leaves the
new agent rule "never a name you choose" with nothing to point at.

---

## A. Conformity

### Numbering of the sheet against the pass file — a question first

`modifications.md` line 1256: "**C14** | Faire l'assemblage par un script
| La fiche se dit elle-même incertaine — et ça change la forme de la
commande." That is the pass file's **`### 13`** (line 488–495: "The
assembly is a script beside `grouper.py` … I am not sure of this one: it
changes the shape of the command"). The pass file's `### 14` is the
never-do / `Edit` clean-up, which no row of the sheet describes.
Reportés "C11 · C12 · C13 — le propriétaire du groupement, le worktree,
les issues — sur `/9_controle` et `/8_code`" match pass `### 11`
(relay rows, worktree, outcomes) and `### 12` (owner) — and nothing in
`### 13`, which is on the agent file.

**Question:** is the sheet's C_n = pass `### n` throughout, with C14
mislabelled, or is it shifted by one from C12 on (C13 = pass 12, C14 =
pass 13, C15 = pass 14, and pass 15 unlisted)? The new file supports the
shift: pass 14 is half applied (`Edit` removed) and pass 15 is not applied
at all (see C14 and C15 below). Verdicts below follow **the pass file's
numbering**, and state both readings where they differ. Severity of the
question itself: **TO FIX** in `modifications.md` — the record of what
was decided on two comments cannot be read.

### C1 — the Missing / Doubtful boundary · PASSÉ

- Expected (pass, lines 82–89): one boundary, stated once — Missing = no
  signature and no criterion of the group's sheets observes it; Doubtful
  = a criterion may observe it and the sheet alone does not say which
  way; the "cannot attach" sentence goes; **the `B8` example moves to
  Missing or is replaced by a real doubt.**
- Found: lines 182–192 — "You do not settle a doubt. But the two fields
  are told apart by a fact, not by your confidence" then the two-row
  table, then "An intention nothing observes is `Missing` — not a doubt."
  The "cannot attach" sentence is gone. **The `B8` example is unchanged,
  lines 223–226**: "B8 Removal of the macros band — lot-11 modifies the
  band's provider, but no criterion observes its disappearance" — still
  under `## Doubts`, and by line 190 it is a Missing.
- Verdict: **PARTIAL — TO FIX.** The rule is right; the only worked
  example of a doubt in the file demonstrates the wrong filing, which is
  exactly the confusion the comment set out to remove.
- Note: the boundary is now stated three times — the outcome table
  (145–149), the boundary table (185–188), and the restatement at 190–192,
  whose second sentence ("A sheet that mentions a subject without
  observing it does not carry it") repeats lines 163–166 word for word in
  substance. NOTE.

### C2 — the unit is the intention · PASSÉ

- Expected (pass, lines 115–119): the unit is the intention; the sentence
  is the default cut, a row / list item / path in a map is a cut too; one
  sentence naming two observables gives two lines; **the caller rule
  concludes on the intention, not the block.**
- Found: lines 151–154, new — "The unit is the intention, never the
  block. A sentence is the usual cut — and a table row, a list item, a
  branch of a flow are cuts too. One sentence naming two observables
  gives two lines." Asked for, present.
  **But the old rule was not removed**: line 138, "🔴 **The unit is the
  sentence, never the whole block.**" — two 🔴 rules thirteen lines apart
  naming two different units. And the caller rule is unchanged, line
  172: "Ask which sheet observes the caller — **none, and the block is
  missing**."
- Verdict: **PARTIAL — TO FIX.** The comment's defect was "three names
  for the unit"; the new file has the same three, plus the right answer.
  Line 138 and line 172 must go or be reworded to "intention".

### C3 — no product file: one behaviour, no file · PASSÉ

- Expected: stop and say so, no file; "no product file" leaves the
  blocker list.
- Found: line 79, "**No product file** | Stop and say so, no file — the
  command checks the same thing before invoking you, and no decision the
  Product Owner writes would make one appear"; lines 122–124 (Part 2)
  unchanged, "stop and say so". Both passages now say the same thing;
  the blocker list is gone.
- Verdict: **CONFORME.**

### C4 — a named sheet that is not there: doubt, not blocker · PASSÉ

- Expected (pass, lines 171–176): every intention of the blocks it was to
  answer for goes under Doubtful, naming the lot, and the run continues;
  "lots whose sheets do not exist" leaves the blocker list; **the
  merged-lot paragraph goes.**
- Found: line 80, "**A sheet your prompt names and that is not there** |
  Every intention of the blocks it was to answer for goes under
  `Doubtful`, naming the lot — and the run carries on." Blocker list gone.
  **Lines 56–59 unchanged**: "A `code/<lot>/` folder holding no sheet
  means that lot was never detailed — report it as a doubt, not as a
  missing intention. A merged lot leaves no folder at all; you will not
  see it, and there is nothing to report."
- Verdict: **PARTIAL — TO FIX.** The merged-lot sentence the comment
  asked to remove is still read at every invocation. The first sentence
  now states the same case as line 80 in a looser form ("report it as a
  doubt" — one line? one per intention?) while line 80 is precise; keep
  one.

### C5 — the blocking mechanism goes · PASSÉ

- Expected (first branch, pass lines 222–227): the mechanism goes; the
  two Invocation 2 "blocker" sentences go with it; `8_code`'s row for the
  Contrôleur goes.
- Found: "When you cannot produce" replaced by "You never write a
  blocking file" (70–84); "When you resume after a blocking file"
  removed; no `blocked_controleur` anywhere in the file. Invocation 2's
  "A partial report that leaves you unable to write a line is a blocker"
  → "is said so in the report" (247–249); "A block missing from every
  partial report is a blocker — say which, and stop" → the Doubtful
  table (270–275).
- Verdict: **CONFORME** on the agent file. Two notes:
  - The pass file's branch said "the agent **stops** and says what it
    found missing"; the new file never stops on an assembly fault — it
    files under Doubtful and carries on. The sheet's own summary ("ses
    deux causes vont au rapport") endorses that reading, so this is a
    deliberate deviation from the pass wording, not an error. NOTE.
  - `8_code`'s row "`code/blocked_<agent>.md` for the Contrôleur" — not
    checked here (outside this file; C12 is reporté on `8_code`). Question
    for the commands' verification: does the new `8_code.md` still name a
    blocking file the Contrôleur no longer writes?

### C6 — the assembly holds the block list and the groups · PASSÉ

- Expected: the assembly prompt names the block list and the groups;
  each partial opens with the blocks its group was given.
- Found, agent: lines 241–245 "The prompt names two things: the groups
  this run issued, and the block list to check against"; lines 270–283
  the two-row check (block unmentioned / group with no partial) and
  "Each partial opens with the blocks its group was given — that is what
  tells the two cases apart"; line 204–205 the partial "opens with the
  blocks you were given, one line".
  Found, command (`.claude-new/commands/9_controle.md` lines 145–149,
  151–156): the assembly prompt carries "Groups issued this run: G1, G2,
  G3. Blocks to account for: B1, B2, B3, …".
- Verdict: **CONFORME.** Two loose ends, in D.5 and D.6 (no format for
  the opening line, and the prompt hint "the G<n> lines of
  tracabilite-full.md" names lines that file does not hold).

### C7 — a run's assembly reads only that run's partials · PASSÉ

- Expected: either the command empties `code/controle/`, or the partials
  carry the run and the assembly reads those alone.
- Found: both. Command line 133–134, "Empty `code/controle/` before
  issuing the groups"; agent lines 242–245, "never a file of
  `code/controle/` the prompt does not name: a partial of an earlier run
  may still be sitting there".
- Verdict: **CONFORME** (belt and braces; harmless).

### C8 — the invocation-1 prompt names the group · PASSÉ

- Expected (pass, lines 324–325): "The prompt names the group — the
  `G<n>` the script printed — and the agent's file rule points at that."
- Found, agent: lines 200–202 — "`code/controle/<group>.md` — the group
  name the prompt gave you, `G1`, `G2`, as the command printed it. Never
  a name you choose: two groups on one name overwrite each other." Asked
  for, present.
  Found, command: the invocation-1 prompt is **unchanged** (new
  `9_controle.md` lines 118–127): "Feature folder: … Invocation 1 —
  Confront. Blocks: B15, B53, B54, B56. Sheets: code/lot-29, …" — `G1`
  appears only in `description="control G1 <feature>"`, which the agent
  does not see.
- Verdict: **agent side CONFORME, command side NOT APPLIED — BLOCKING as
  a pair.** The agent now has a 🔴 rule that forbids the only thing it
  could do when the prompt carries no group name. Every group invocation
  of a run hits it. Question: is the A4/A5 rewrite of `9_controle.md`
  expected to add `Group: G1` to that prompt? The sheet's cascade note
  (line 1272–1274) mentions the assembly prompt only.

### C9 — the command's reading list names Phase 1's inputs · PASSÉ

- Expected: "What you read" names `tracabilite.md` and the `Anchor:`
  lines of `code/decoupage.md`, by grep.
- Found, new `9_controle.md` lines 25–30: unchanged — "Only whether
  `desc-produit.md` is there, and whether every lot of `code/sequence.md`
  carries a `verdict.md` in PASS. ⚠️ Nothing else." Phase 1 (lines
  52–60) still greps both files.
- Verdict: **NOT APPLIED — listed passé.** TO FIX on the command, or
  the sheet's list is wrong. Same question as C8 about A4/A5.

### C10 — the crossing is verified · PASSÉ

- Expected: the script does the join, or Phase 1 ends with a check that
  every block of `tracabilite.md` and every lot of `code/decoupage.md`
  appear in `tracabilite-full.md`.
- Found, new `9_controle.md` Phase 1: no check stated; "Every block
  appears" (line 73) remains an instruction, not a verification.
- Verdict: **NOT APPLIED — listed passé.** TO FIX on the command, or the
  sheet's list is wrong.

### C11 — relay rows per outcome, one merge point · REPORTÉ

- Expected: not applied.
- Found: "What you relay" was rewritten (four files), but no row for a
  stop outcome and no "what re-running does"; "Git, in this mode" still
  says "once the agent reports" for a run of N+1 agents.
- Verdict: **not applied, as declared.** (The rewrite that did happen
  belongs to the commands' own section.)

### C12 — one owner of the Contrôleur run · REPORTÉ

- Expected: not applied.
- Found: `9_controle.md`'s first paragraph ("`/8_code` runs the Contrôleur
  on its own") — the sentence C12 targeted on this command — **is gone**,
  replaced by "The Contrôleur runs on the main cycle alone" (lines
  44–46). `8_code.md` not checked here.
- Verdict: **half applied on `9_controle` although reporté.** NOTE — it
  goes the right way; the commands' verification should confirm `8_code`
  56–58, 239–242, 249 were handled the same way.

### C13 — the assembly as a script · REPORTÉ (or ÉCARTÉ as "C14")

- Expected: not applied.
- Found: Invocation 2 is still an agent move (lines 237–297).
- Verdict: **not applied, as declared** — under either reading of the
  numbering.

### C14 — never-do / `Edit` clean-up · ÉCARTÉ per the sheet (but see the numbering question)

- Pass `### 14` asked: keep only the never-do entries the body can
  violate; drop `Edit` and its section unless a move needs it; drop the
  two justifications and the two "never this file" lines; drop the
  Cadreur sentence.
- Found: **`Edit` removed from the tool line (line 4) and "When `Edit`
  fails" removed** — applied. Still present: never-do "Relaunch anything"
  (99–100) and "Report a lot as failed" (101–102); "Never `idees.md` — the
  raw text the upstream chain spent its whole loop correcting" (61–62);
  "Never the technical document, the lot list or the sequence" (65–66);
  "The Cadreur merges lots that build one thing" (158–159) — not applied.
- Verdict: **HALF APPLIED.** If the sheet's "écarté" really refers to
  this comment, the `Edit` removal is an unannounced change (a correct
  one — no move uses `Edit`, see C below). If it is passé under the
  shifted numbering, four of its five items are missing. TO FIX either
  the sheet or the file; the question above decides which.

### C15 — "working folder" replaced by the prompt's word · PASSÉ

- Expected (pass, lines 555–557): one word, the prompt's — the folder
  the prompt names is where `desc-produit.md` and `code/` live, and never
  a sub-folder of it.
- Found: **unchanged.** Line 26, "The files, in the working folder you
  were given."; line 33, "not to the working folder"; line 122, "No
  `desc-produit.md` in the working folder". No definition; the prompt
  (command line 122) still says "Feature folder:".
- Verdict: **NOT APPLIED — listed passé.** TO FIX (one line, as the
  pass file said). Under the shifted-numbering reading this comment is
  simply absent from the sheet, which would explain it.

---

## B. Unannounced changes

Diff old → new, hunk by hunk. Everything maps to a comment except two
items.

### B.1 — `# PART 3 — What you do` heading removed · TO FIX

- Old, lines 190–192: `# PART 3 — What you do` then `## INVOCATION 1 —
  Confront`.
- New: the heading is gone; `## INVOCATION 1 — Confront` (line 128) and
  `## INVOCATION 2 — Assembly` (237) now sit under `# PART 2 — Which
  call is this` (106).
- What it changes: the file's three-part skeleton (know / which call /
  do) becomes two parts, and Part 2's title no longer describes two
  thirds of its content. No comment asks for it; the heading and its
  preceding `---` were inside the hunk that deleted "When you resume
  after a blocking file" — a collateral deletion.

### B.2 — `Edit` dropped from the frontmatter tools · NOTE (announcement unclear)

- Old line 4: `tools: Read, Grep, Glob, Edit, Write` · New: `tools: Read,
  Grep, Glob, Write`, and the section "When `Edit` fails" (old 126–133)
  removed.
- What it changes: nothing in behaviour — no move edits a file (see C).
  It is pass comment 14's ask; whether the sheet counts 14 as passé or
  écarté is the numbering question in A. Listed here so it is not lost
  if the answer is "écarté".

### B.3 — the `---` separator before "What you never do" · NOTE

- Old: `## When you cannot produce` … `---` … `## What you never do`.
- New: line 84 ends "read in the report.**" and line 86 is `## What you
  never do` with no `---` between — the only pair of `##` sections in the
  file not separated by a rule. Cosmetic; same collateral cause as B.1.

Everything else in the diff — the blocking sections, the Missing /
Doubtful table, the unit paragraph, the group-name and opening-line
rules, Invocation 2's reading rules and check table — is C1–C8.

---

## C. Gestures against tools

Frontmatter, line 4: **Read, Grep, Glob, Write.**

| Gesture | Where | Tool | Has it |
|---|---|---|---|
| Read the named blocks of `desc-produit.md` | 49, 135 | Read (+ Grep to locate `B15` in the file) | yes |
| Read the named sheets, all before any block | 50–51, 132–133 | Read | yes |
| See that a named `code/<lot>/` has no sheet | 56, 80 | Glob | yes |
| Write `code/controle/<group>.md` | 200 | Write | yes |
| Stop and say so, no file | 79, 123 | none needed | — |
| Read the partial of each named group | 242 | Read | yes |
| `Glob("code/rapport-controle*.md")`, pick the next free name | 253–257 | Glob | yes |
| Write the report | 287 | Write | yes |
| Never write over an earlier report | 259 | Glob before Write covers it | yes |

- **Gesture with no tool: none.** The rename that had no tool (old
  "git mv") is gone with the blocking mechanism; nothing asks for Bash
  or Edit any more.
- **Tool no gesture names: `Grep`.** No line says "grep"; it is the
  natural way to find a block heading in `desc-produit.md` or a `B<n>`
  in a partial, so it is implied rather than idle. NOTE, not a defect.
- `Edit` removed: correct — both invocations create fresh files and
  the file forbids overwriting the only existing ones (reports).
- One gesture rests on a **fact** rather than a tool: line 275 asks to
  file "every block it was given" for a group whose partial is absent.
  The prompt (241–242) gives the groups and the block list, not the
  group → blocks mapping; the agent recovers it by elimination from the
  other partials' opening lines (282–283). Exact with one silent group;
  with two, the blocks can be filed under Doubtful but not attributed to
  a group. NOTE — see D.6.

---

## D. Internal coherence (new file alone)

### D.1 — two 🔴 rules on the unit · TO FIX

- Line 138: "🔴 **The unit is the sentence, never the whole block.**"
- Line 151: "🔴 **The unit is the intention, never the block.**"
- Line 156: "Name the block and the sentence when a block holds several"
  — assumes the sentence is the unit again, whereas 152–153 say a row or
  a list item is a cut too.

### D.2 — the caller rule concludes on the block · TO FIX

- Line 172: "none, and **the block is missing**" — against line 151 and
  never-do line 97 "Answer for a whole block at once — one line per
  intention".

### D.3 — the `## Doubts` example is a Missing · TO FIX

- Lines 223–226: "B8 Removal of the macros band — lot-11 modifies the
  band's provider, but **no criterion observes its disappearance**"
  under `## Doubts`.
- Line 190: "⚠️ **An intention nothing observes is `Missing`** — not a
  doubt."

### D.4 — the invocation table contradicts Invocation 2's reading rule · TO FIX

- Line 113: "| 2 | Assembly | **Every `code/controle/*.md`** | The report |"
- Lines 242–245: "Read the partial of each named group — **never a file
  of `code/controle/` the prompt does not name**".
  The table was not updated with C7.

### D.5 — "opens with the blocks you were given" has no shape · TO FIX

- Line 204–205: "🔴 It opens with the blocks you were given, one line".
- Lines 209–226, the template of the very same file, opens with
  `## Intentions found` and shows no such line.
- Line 282: the assembly relies on that line to "tell the two cases
  apart" — and has no format to recognise it by. Give the line in the
  template (`Blocks: B15, B53, B54, B56`).

### D.6 — a group whose partial is absent: "naming the group" needs a mapping the prompt does not give · NOTE / question

- Line 241–242: the prompt names "the groups this run issued, and the
  block list to check against".
- Line 275: "Every block **it was given** goes under `Doubtful`, naming
  the group".
  With one missing group the blocks are found by elimination (282–283);
  with two, the file cannot say which group each block belongs to. Is a
  per-group block list in the assembly prompt wanted, or is "naming the
  groups that did not report" enough? (The command's prompt hint "the
  G<n> lines of tracabilite-full.md" — `9_controle.md` line 148–149 —
  points at lines that file does not hold; `tracabilite-full.md` holds
  `B<n>  lot-…` lines and the `G<n>` lines are the script's stdout.
  Command side, noted for its own verification.)

### D.7 — "said so in the report": in which field? · TO FIX (minor)

- Lines 247–249: "A partial that leaves you unable to write a line is
  **said so in the report**, never a reason to go looking."
- Lines 287–288: the report is "the same three fields" (Found / Missing
  / Doubts). None is named for a malformed partial; the branch ends
  without a place to write. Presumably `## Doubts`, naming the group —
  say it.

### D.8 — "Two moves" then three · NOTE

- Line 251: "**Two moves.**" — move 1 (253), move 2 (265) — then line
  270 "🔴 **Then check the block list the prompt gave you**", an
  unnumbered third step with its own table. Invocation 1's "Two moves"
  (130) is exact.

### D.9 — the same case in two wordings · TO FIX (with C4)

- Lines 56–57: a `code/<lot>/` folder holding no sheet → "report it as a
  doubt, not as a missing intention".
- Line 80: a named sheet not there → "Every intention of the blocks it
  was to answer for goes under `Doubtful`, naming the lot".
  Same situation; the first leaves the shape of the line open. And lines
  57–59 (merged lots) describe a case the reading rule (49–51: the named
  sheets and no other) keeps the agent from meeting.

### D.10 — the same criterion twice · NOTE

- Lines 163–166: "a sheet that *mentions* a button without any criterion
  observing it does not carry the intention".
- Lines 191–192: "A sheet that mentions a subject without observing it
  does not carry it."

### D.11 — never-do entries nothing can violate · NOTE

- Lines 99–100 "Relaunch anything", 101–102 "Report a lot as failed":
  no tool relaunches, no field of the report takes a lot verdict. Pass
  comment 14's point; standing or discarded depending on the numbering
  question.

### D.12 — cosmetic · NOTE

- Lines 41–45: three consecutive `---` (pre-existing, unchanged).
- Line 85: no `---` before `## What you never do` (see B.3).
- Lines 122–124 and 79 say "no product file → stop and say so" twice;
  consistent, so not a defect — but C3 asked "one behaviour", and one
  passage would do.
