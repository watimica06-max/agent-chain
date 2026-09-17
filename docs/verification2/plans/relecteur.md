# Plan — relecteur

Built against `.claude-new/agents/relecteur.md`, the two commands that name it —
`.claude-new/commands/8_code.md` and `.claude-new/commands/cycle.md` — the report
`docs/verification2/relecteur.md` (both parts), `docs/verification2/decisions.md`,
and the six thematic reports filtered to `relecteur`. Every cited line was opened
before its verdict; the other side of each two-file `Where` is quoted in the entry.

Two settled questions of `decisions.md` touch this agent:

- **`passages-aval.md` F15** — every reader matches the `PASS` prefix. The relecteur
  is a reader at L195-196 (*"those carrying no `PASS` verdict"*). Applied in the
  entry for `passages-aval.md` F15 below; the entry for `relecteur.md` F12 gives the
  reservation a place, and its reader goes to `## To settle`.
- **`cadreur.md` F23** — `cycle.md` is deleted. Its row 3 (L82, *"A `blocked_detailleur`,
  `_realisateur` or `_relecteur` → STOP"*) goes with it; after that `/8_code` is the
  only command that invokes the relecteur. `relecteur.md` itself names neither
  `/cycle` nor `cycle.md` (its one "cycle", L237, is the ordinary word).

Three findings are reported three times each — by the agent's report and by two
thematic reports. Each is decided once, in full, under the agent's report; the two
thematic entries point at it.

---

## Report `relecteur.md`

### relecteur.md F01 — the index off by one from C11

Verdict: confirmed
Decision: Renumber the relecteur section of the index to the pass sheet's own numbers — passed: 1-7, 12, 13, 14, 16, 17; deferred to `/8_code`: 8, 9, 10, 11, 15 — so that every entry names the comment it describes.
Where: modifications.md L1190-1207 ↔ passes/relecteur.md L358-543
Cited: modifications.md L1203 — "**C11** | `FAIL structurel` se définissait par un *nombre* de points en échec"; passes/relecteur.md L384-390 — "### 12 … `structurel` is 'the lot does not do what the sheet asks, or several points fail together'". modifications.md L1205 — "**C13** | Les cas vides passaient"; passes/relecteur.md L444-447 — "### 14 … Nothing says what a sheet with no signatures, no criteria or no `## Conventions` section does". modifications.md L1206 — "**C15** | Il lit la revendication de compilation en premier"; passes/relecteur.md L499-503 — "### 16 … Point 4 alone can yield `FAIL structurel`". passes/relecteur.md L358-360 — "### 11 … Fichier : .claude/commands/8_code.md" and L470-472 — "### 15 … Fichier : .claude/commands/8_code.md" are the two `/8_code` comments the index lists as passed.
Owner: the index `docs/refonte/modifications.md` — `relecteur.md` unchanged
Also in: —

The index's C14 and C17 are read as deferred; ### 14 is applied at relecteur.md L404-416 (partially — F04) and ### 17 at L417-423.

### relecteur.md F02 — `## Causes so far` has no record

Verdict: confirmed
Decision: Record in the index's relecteur section that `## Causes so far` was added by the first round's D-7 / C8 correction, with `/8_code` L159 as its reader.
Where: relecteur.md L149-150, L171-174 ↔ modifications.md L1175-1240
Cited: a grep of `Causes so far` over `docs/refonte/modifications.md` and `docs/refonte/passes/relecteur.md` returns nothing; report Part 2 L60 — "D-7 | fixed | `.claude-new/agents/relecteur.md:114–116, 146, 150` · `.claude-new/commands/8_code.md:159, 325–326`"; 8_code.md L159 — "`## Causes so far` of the last verdict holds `reasoning` twice"
Owner: the index `docs/refonte/modifications.md` — `relecteur.md` unchanged here; what the field lacks is F09 and F10
Also in: —

### relecteur.md F03 — ### 17 applied on the sheet alone

Verdict: confirmed
Decision: Keep the sheet-only test — a report that lists what nobody asked for would certify itself — and record the departure and its reason in the index.
Where: passes/relecteur.md L541-543 ↔ relecteur.md L419-422
Cited: passes/relecteur.md L540-542 — "every symbol declared there that neither the sheet nor the report's ## Symbols names is a finding"; relecteur.md L420-422 — "**The sheet, never the report**: a report that lists what nobody asked for would certify itself"
Owner: the index `docs/refonte/modifications.md` — `relecteur.md` unchanged
Also in: —

### relecteur.md F04 — ### 14 settled the missing criteria only

Verdict: confirmed
Decision: State the outcome of a sheet with no `## Signatures` and of a sheet with no `## Conventions` — the same as no criteria for a section absent (`FAIL structurel`, `Cause: sheet`, the block goes back), and point 3 on the `permanente` scope alone when `## Conventions` is present and carries a dash.
Where: passes/relecteur.md L456-461 ↔ relecteur.md L404-407
Cited: passes/relecteur.md L459-461 — "a sheet lacking a section the checklist depends on is a finding against the sheet (the Détailleur's, not the lot's) and the status it yields"; relecteur.md L404-405 — "a sheet with no criteria is a `FAIL structurel`, `Cause: sheet`" — signatures and conventions are not named
Owner: relecteur
Also in: —

Folds into F11: the `FAIL structurel` row has to list this third thing.

### relecteur.md F05 — ### 13 asked for a read by section

Verdict: confirmed
Decision: Keep the whole-file fallback — the Architecte marks three kinds `permanente` on every file it writes, so a file with no marker is one it never derived — and record the departure in the index, as the same fallback is shared with the Concepteur, the Testeur and the Réalisateur.
Where: passes/relecteur.md L433-436 ↔ relecteur.md L66-68
Cited: passes/relecteur.md L437-438 — "The conventions file is read by section: the rules the sheet's ## Conventions names, nothing more"; relecteur.md L66-68 — "No rule carries the marker — read the file whole: the Architecte has not derived it yet"; architecte.md L150-151 — "Three kinds are always `permanente`"; realisateur.md L66-69, concepteur.md L62-66, testeur.md L66-69 — the same three-line fallback
Owner: the index `docs/refonte/modifications.md` — `relecteur.md` unchanged
Also in: —

### relecteur.md F06 — bounded reads with no tool named

Verdict: confirmed
Decision: Name Grep as the tool of every read bounded to one line — the fields of the verdict being replaced, the block line of `code/sequence.md`, the `## Status` line of the block's other verdicts — since Read opens the file whole.
Where: relecteur.md L4 ↔ relecteur.md L60-61, L80-83, L194-195
Owner: relecteur
Also in: —

L4 — "tools: Read, Grep, Glob, Write"; L60-61 — "its `## Attempts` line alone"; L80-81 — "that one line, never the file"; L194-195 — "that one line, not the file". The lines to grep from the old verdict are the ones F10 settles.

### relecteur.md F07 — "one of two words" followed by three

Verdict: confirmed
Decision: Make the count match the list — three words, `understanding`, `reasoning`, `sheet`.
Where: relecteur.md L114 ↔ relecteur.md L115
Owner: relecteur
Also in: —

The "two" predates `sheet`: the first round's D-7 named "understanding of the lot, or limit of reasoning" (docs/verification/agent-relecteur.md L110), and `sheet` came with C14 / D-5.

### relecteur.md F08 — `reasoning` defined twice

Verdict: confirmed
Decision: Keep one definition of `reasoning` — the calculation badly conducted, the cascade badly anticipated — and give "the sheet read wrongly" to `understanding`, where it belongs; the second paragraph then defines both words, or goes.
Where: relecteur.md L115-116 ↔ relecteur.md L176-178
Owner: relecteur
Also in: —

L115-116 — "`reasoning` covers a calculation badly conducted, a cascade badly anticipated"; L176-178 — "`reasoning` is the word for a lot whose code does something other than the sheet asks, having read it wrongly". The escalation to opus (8_code.md L159) is meant for the model's limit — "limit of reasoning" in the first round's wording — not for a misread.

### relecteur.md F09 — the head-rule verdict drops two fields

Verdict: confirmed
Decision: Make the head-rule verdict carry all seven fields — `## Verified` with the red or not-run claim, `## Causes so far` copied from the verdict replaced plus `understanding` — so a red build neither empties the field the file says is never empty nor breaks the cause chain.
Where: relecteur.md L312-315 ↔ relecteur.md L157-160, L171-174, L207-210
Owner: relecteur
Also in: passages-aval.md F07, chemins-aval.md F05 (below)

L312-315 lists `## Status`, `## Attempts`, `## Findings`, `## Cause`, `## Symbol divergences`; L208-210 — "Never leave the field empty"; L171-174 — "carries every cause this lot has had … copied from the verdict you replace, plus yours"; 8_code.md L159 — "`## Causes so far` of the last verdict holds `reasoning` twice".

### relecteur.md F10 — `## Attempts` alone, yet `## Causes so far` copied

Verdict: confirmed
Decision: Widen the read of the verdict being replaced to two lines — `## Attempts` and `## Causes so far` — at L60-61 and wherever the bound is restated.
Where: relecteur.md L60-61 ↔ relecteur.md L171-173
Owner: relecteur
Also in: passages-aval.md F08, chemins-aval.md F04 (below)

### relecteur.md F11 — a third thing in a table of two

Verdict: confirmed
Decision: List in the `FAIL structurel` row the third thing that yields it — a sheet missing a section the checklist depends on (F04) — and let the row's count follow.
Where: relecteur.md L112 ↔ relecteur.md L404-405
Owner: relecteur
Also in: —

### relecteur.md F12 — the reservation is written nowhere

Verdict: confirmed
Decision: Give the reservation a place — `## Findings` carries it, one line per reserved point, in the same shape as a failed point — and say so in the row; who reads it is in `## To settle`.
Where: relecteur.md L110 ↔ relecteur.md L124-155
Owner: relecteur
Also in: —

`decisions.md` (`passages-aval.md` F15) keeps the value and settles that a reserved lot counts as coded; it does not name a reader for the note, and the pass sheet's ### 10 (passes/relecteur.md L328-335) already found none.

### relecteur.md F13 — the shape sent to the wrong section

Verdict: confirmed
Decision: Point the reference at *What you write*, where the seven fields are.
Where: relecteur.md L46-47 ↔ relecteur.md L105-119, L124-155
Owner: relecteur
Also in: —

### relecteur.md F14 — a manual-list criterion read as uncovered

Verdict: confirmed
Decision: Make the second way of seeing a test that does not run read "a criterion listed under neither `## Tests` nor `## Criteria with no test` of `tests.md`", so that L340 and L410-411 no longer contradict each other.
Where: relecteur.md L409-411 ↔ relecteur.md L340-342
Owner: relecteur
Also in: —

L410-411 — "a criterion `tests.md` does not list under `## Tests`"; L340-342 — "A criterion in `## Criteria with no test` of `tests.md` is not a gap".

### relecteur.md F15 — rules for points 1 and 2 placed after point 4

Verdict: confirmed
Decision: Move each rule under the point it governs — the no-criteria sheet under point 2 (with F04's siblings), the disabled or unlisted test under point 2, the symbol that no longer resolves under point 1 — and leave nothing between point 4 and point 5 but point 4.
Where: relecteur.md L404-416 ↔ relecteur.md L317-346
Owner: relecteur
Also in: —

### relecteur.md F16 — no `conception.md` or no `tests.md` has no outcome

Verdict: confirmed
Decision: Extend the block to the four inputs the checklist cannot run without — the sheet, the report, `conception.md`, `tests.md` — and give `/8_code`'s Relecteur-block table a row for each of the two new ones, whatever that row does.
Where: relecteur.md L58-59, L340 ↔ relecteur.md L236-239
Cited: 8_code.md L418-422 — "| The report | A fresh `realisateur` … | The sheet | `detailleur` on the block | Anything else | Relay it and stop |"; 8_code.md L112-113 — the Concepteur is "skipped when `code/<lot>/conception.md` is there", the Testeur "when `code/<lot>/tests.md` is there"
Owner: relecteur
Follows: 8_code (its table at L418-422)
Also in: commandes.md

### relecteur.md F17 — `## Cause` and `## Findings` on a PASS

Verdict: confirmed
Decision: State what the seven fields carry on a PASS — `## Findings` a dash, or the reservation lines of F12; `## Cause` a dash; `## Causes so far` the causes copied from the verdict replaced, or a dash when there is none.
Where: relecteur.md L114 ↔ relecteur.md L124-155
Owner: relecteur
Also in: —

### relecteur.md F18 — "your report" names the return message

Verdict: confirmed
Decision: Use a word other than *report* for the agent's return message at L295 and L298, since "the report" is `code/<lot>/compte-rendu.md` everywhere else in the file.
Where: relecteur.md L41 ↔ relecteur.md L295, L298
Owner: relecteur
Also in: —

### relecteur.md F19 — `Cause: sheet` has no route

Verdict: confirmed
Decision: —
Where: relecteur.md L167-169, L407 ↔ 8_code.md L41-43, L138-144; detailleur.md L466-467
Cited: 8_code.md L138-139 — "**4.** On FAIL → a **fresh `realisateur`**, with the verdict, **then the `relecteur` again on the same lot**"; 8_code.md L41-43 — "`## Cause`, to know whether to escalate"; 8_code.md L159 — the only branch on a cause, "`reasoning` twice → the third realisateur is passed `opus`"; detailleur.md L466-467 — "A sheet, and no `PASS` → You skip it"; detailleur.md L672-676 — the divergence mode "rewrite only those sheets, against the signature the code actually carries", which is not this case; realisateur.md L519-520 — the FAIL table has two rows, `mineur` and `structurel`, and no `sheet`
Owner: 8_code — the route is the command's; the Détailleur owns the mode it lands in
Follows: relecteur (L167-169 and L407 promise the route), detailleur, realisateur (L519-520)
Also in: commandes.md, detailleur.md, realisateur.md — and passages-aval.md F02, chemins-aval.md F03 (below)

The fact holds: the promise is at relecteur.md L168-169 — "`sheet` says the fault is upstream: the block goes back to the Détailleur, never to a fresh Réalisateur" — and no command or agent carries it. The report's own Part 2 (C14, D-5) says the same. What the route looks like turns on which agent gains a mode and on what happens to the lot's `conception.md`, `tests.md` and code once the sheet is rewritten — see `## To settle`.

### relecteur.md F20 — "fix the point reported", singular

Verdict: confirmed
Decision: Make the Réalisateur's `FAIL mineur` row fix every point `## Findings` names, not one.
Where: relecteur.md L162-165 ↔ realisateur.md L520
Cited: realisateur.md L520 — "| **FAIL mineur** | Fix the point reported, re-run the static analysis and the tests"; relecteur.md L162-165 — "`## Findings` names every point that failed … A verdict naming one gap out of three sends a fresh Réalisateur to fix one third of the lot"
Owner: realisateur
Follows: — (the relecteur's side already names every point)
Also in: realisateur.md

---

## Thematic reports

### renommages.md F08 — a Concepteur-applied decision reads as drift

Verdict: confirmed
Decision: Give `conception.md` a field naming the decision the Concepteur applied, and let the relecteur read a divergence as decided when either that field or the report's `## What governed the code, besides the sheet` accounts for it.
Where: concepteur.md L158 ↔ relecteur.md L184-190
Cited: concepteur.md L158-159 — "Say in your report that you applied it — the orchestration renames the file"; concepteur.md L51 — "the report | `code/<lot>/conception.md`"; concepteur.md L247-259 — its four fields are `## Declared`, `## Compile`, `## Placements not settled by the conventions`, `## Outside the lot`; relecteur.md L184-186 — "that field, and nothing else, makes a divergence legitimate"
Owner: concepteur
Follows: relecteur (L54-57, L184-190 — the test keys on one field and has to key on two), 8_code (4b renames on "reports having applied it", L170)
Also in: concepteur.md, commandes.md

### renommages.md F09 — the number the report cannot know

Verdict: confirmed
Decision: Have `## What governed the code, besides the sheet` name the blocking file at the name it has when the report is written — the unnumbered one — or by the decision it carries, never by a number assigned afterwards.
Where: realisateur.md L178 ↔ 8_code.md L170
Cited: realisateur.md L176-177 — "the numbered blocking file, the rule by its number"; 8_code.md L170 — "rename it once the agent reports having applied it … `NN`: the highest in that folder plus one"
Owner: realisateur
Follows: — for the relecteur: it reads the field (L54-57) and never opens a blocking file (its reading list, L51-68, names none), so it greps no number; the finding's "the number the Relecteur will grep" overstates its part
Also in: realisateur.md, commandes.md

### passages-aval.md F01 — `## Files` built from a field that carries no file

Verdict: confirmed
Decision: Define `## Files` as the files the lot owns — the ones it creates and the ones it modifies, as its three downstream readers already read it — established by the Détailleur from `Touches` and its own grep, never copied from `Modifies`.
Where: detailleur.md L259-265 ↔ cadreur.md L753-754, relecteur.md L386-388
Cited: cadreur.md L753-754 — "`Needs`, `Produces` and `Modifies` carry symbols, and symbols only. A name the code carries — never a file"; detailleur.md L259-261 — "`## Files` carries the lot's `Modifies` and `Touches`, copied from `code/decoupage.md`"; realisateur.md L60-61 and testeur.md L57-58 — "its `## Files` names every file the lot owns"; relecteur.md L386-388 — "`## Outside the lot` names every file the lot touched that its sheet's `## Files` does not name, or a dash"
Owner: detailleur
Follows: relecteur — its check at L386-392 keys on `## Files` as the declared set and holds under the new definition; the line to rewrite is the one that says what the set is, if the relecteur restates it; concepteur, testeur, realisateur likewise
Also in: detailleur.md, cadreur.md, concepteur.md, testeur.md, realisateur.md

### passages-aval.md F02 — `Cause: sheet` never reaches the Détailleur

Verdict: confirmed
Decision: — (same finding as relecteur.md F19; see `## To settle`)
Where: relecteur.md L167-169, L405-407 ↔ 8_code.md L138-139, detailleur.md L466-467
Cited: as in relecteur.md F19
Owner: 8_code
Follows: relecteur, detailleur, realisateur
Also in: relecteur.md F19, chemins-aval.md F03, commandes.md, detailleur.md, realisateur.md

### passages-aval.md F07 — the build-red verdict drops out of the count

Verdict: confirmed
Decision: Same as relecteur.md F09 — all seven fields on the head-rule verdict.
Where: relecteur.md L312-314 ↔ 8_code.md L159, L200; relecteur.md L171-174, L208-210
Cited: 8_code.md L159 — "`## Causes so far` of the last verdict holds `reasoning` twice → the third realisateur is passed `opus`"; 8_code.md L199-200 — "You read four fields of a verdict — `## Status`, `## Attempts`, `## Causes so far` and `## Symbol divergences`"
Owner: relecteur
Also in: relecteur.md F09, chemins-aval.md F05

### passages-aval.md F08 — the accumulated causes read against the rule

Verdict: confirmed
Decision: Same as relecteur.md F10 — the read of the old verdict covers both lines.
Where: relecteur.md L60-61 ↔ relecteur.md L171-174
Owner: relecteur
Also in: relecteur.md F10, chemins-aval.md F04

### passages-aval.md F10 — `§3 ·` on the sheet, `R30` at the Architecte, `R12` in the verdict

Verdict: confirmed
Decision: Cite a rule by its `Rnn` number in the sheet's `## Conventions`, as the Architecte numbers it and as the report and the verdict already do, so that "the rules the sheet names" is a list of rules and not of sections.
Where: detailleur.md L252-253, L652 ↔ architecte.md L131-132, relecteur.md L141, L349-357
Cited: detailleur.md L252-253 — "§3 · a rule needing the platform's ambient handle is in the wrong module / §9 · the name of the rule, not of the structure"; detailleur.md L652 — "Name the rule, never restate it — `§10 · no hardcoded string`"; architecte.md L120-121 — "R12 · Every identifier that leaves a module is in English · permanente · mechanical"; architecte.md L131-132 — "a spec sheet cites `R30`, and renumbering would point every citation at another rule"; relecteur.md L141 — "point 3 — R12, the identifier is not in English"; realisateur.md L177 — "R18 — the identifier is in English"
Owner: detailleur — it writes the field; the numbering is the Architecte's and already says `Rnn`
Follows: — for the relecteur: its example and its point 3 already key on rules; nothing to rewrite once the sheet cites `Rnn`
Also in: detailleur.md, architecte.md, realisateur.md

The report's `L372-373` for the relecteur does not land on a conventions line; the lines that key on the sheet's list are L349-357.

### passages-aval.md F12 — a green-by-declaration test that `## Red` hides

Verdict: confirmed
Decision: Give `tests.md` a field for the tests left green because the declaration alone meets the criterion, and for a criterion gone with an adapted test; the relecteur's point 2 then describes the Testeur's work as it is, and counts a green-by-declaration test as its criterion's test.
Where: testeur.md L221, L232-233 ↔ testeur.md L278-280, realisateur.md L76-77, relecteur.md L333-334
Cited: testeur.md L221 — "Leave it green — the criterion is met by the declaration: say so in your report"; testeur.md L232-233 — "If the criterion it asserted is gone too, say so in your report"; testeur.md L270-282 — the fields are `## Tests`, `## Criteria with no test`, `## Red`, `## Outside the lot`; testeur.md L280 — "`## Red` — that every new test failed, and every older one passed"; relecteur.md L333-334 — "the testeur wrote one per criterion and checked each one failed red"
Owner: testeur
Follows: relecteur (L333-334, and point 2's matching on the new field), realisateur (L76-77 reads `## Red` as given)
Also in: testeur.md, realisateur.md

### passages-aval.md F15 — `PASS with reservation` against readers keyed on `PASS`

Verdict: confirmed — settled by `decisions.md`
Decision: Apply the settled decision — the relecteur's own test at L195-196 matches the `PASS` prefix, and the file says so where it names the four words (L219).
Where: relecteur.md L110, L222 ↔ detailleur.md L466, verificateur.md L69-70, 8_code.md L62-63, 9_controle.md L60
Cited: decisions.md L135-140 — "Every reader matches the `PASS` prefix … The readers concerned: `relecteur`, `detailleur`, `verificateur`, `8_code`, `9_controle`"; detailleur.md L466 — "A sheet, and its verdict is `PASS` → Never touched"; verificateur.md L69-70 — "its `## Status` line only … to confirm each still carries PASS"; 8_code.md L62-63 — "the first in the sequence with no `verdict.md` carrying PASS"; 9_controle.md L60 — "Stop if a lot of the sequence has no `verdict.md` in PASS"
Owner: relecteur — for its own reader line; each of the other four for theirs
Follows: detailleur, verificateur, 8_code, 9_controle
Also in: detailleur.md, verificateur.md, commandes.md

### fichiers.md F10 — the Contrôleur credited with a block it never writes

Verdict: confirmed
Decision: Drop the Contrôleur from the sentence at 8_code.md L415 — the relecteur's half of it holds.
Where: 8_code.md L415 ↔ controleur.md L73-75
Cited: controleur.md L73-75 — "## You never write a blocking file — Everything you find goes in your report"; 8_code.md L415-416 — "The Relecteur and the Contrôleur do not call it either — their blocks say something is missing, not something to settle"; relecteur.md L4 — no `Agent` tool, and L229 — it does write `blocked_relecteur.md`
Owner: 8_code
Follows: — (nothing of the relecteur's changes)
Also in: commandes.md, controleur.md

### chemins-aval.md F03 — a wrong sheet costs three Réalisateur runs

Verdict: confirmed
Decision: — (same finding as relecteur.md F19; see `## To settle`)
Where: relecteur.md L168 ↔ 8_code.md L138, realisateur.md L519-520
Cited: as in relecteur.md F19
Owner: 8_code
Follows: relecteur, detailleur, realisateur
Also in: relecteur.md F19, passages-aval.md F02, commandes.md, realisateur.md, detailleur.md

### chemins-aval.md F04 — the field the opus escalation counts on

Verdict: confirmed
Decision: Same as relecteur.md F10.
Where: relecteur.md L61 ↔ relecteur.md L172
Owner: relecteur
Also in: relecteur.md F10, passages-aval.md F08

### chemins-aval.md F05 — one structural failure breaks the chain

Verdict: confirmed
Decision: Same as relecteur.md F09.
Where: relecteur.md L312 ↔ 8_code.md L159; relecteur.md L208
Cited: 8_code.md L159 — as in passages-aval.md F07
Owner: relecteur
Also in: relecteur.md F09, passages-aval.md F07

### chemins-aval.md F10 — `blocked_relecteur.md` is never retired

Verdict: confirmed
Decision: Have `/8_code` retire `blocked_relecteur.md` itself when it acts on the report row or the sheet row — the act is the answer to the block — and align the relecteur's line on when the orchestration retires it, which is not "once the verdict is written".
Where: 8_code.md L418-422 ↔ relecteur.md L229-234
Cited: 8_code.md L418-422 — "| The report | A fresh `realisateur` — counted as an attempt | The sheet | `detailleur` on the block |"; 8_code.md L169-170 — "Its `## Decision` is empty → Stop … Filled → rename it once the agent reports having applied it"; relecteur.md L232-234 — "You never retire it … The orchestration does it, once the verdict is written"; relecteur.md L241-257 — the block is written with `## Decision` empty
Owner: 8_code
Follows: relecteur (L232-234)
Also in: commandes.md

On the next pass, move 4b (L164-170) meets the file with its `## Decision` still empty and stops the lot, whatever the fresh Réalisateur or the Détailleur did.

### chemins-aval.md F22 — a re-cut lot inherits its `## Attempts`

Verdict: confirmed
Decision: Have `/8_code` delete `code/<lot>/verdict.md` alongside the stale sheet, for every lot with no verdict carrying PASS, when the split comes back — the count then starts at 1 on the new shape, by the relecteur's existing rule.
Where: 8_code.md L344, L379-382 ↔ relecteur.md L157-160, cadreur.md L884-885
Cited: 8_code.md L379-382 — "The sheets of every lot that is not coded are stale … Delete them, in `code/<lot>/fiche-executable.md`" — the verdict is not named; cadreur.md L884-885 — "Every other lot is yours — the one in hand included, whose code was dropped" — nothing forbids keeping the number; relecteur.md L157-158 — "`## Attempts` carries the count the verdict you replace held, plus one — `1` when there was no verdict"
Owner: 8_code
Follows: — (the relecteur's rule already yields 1 on a missing verdict)
Also in: commandes.md

---

## To settle

### The route of `Cause: sheet` — relecteur.md F19 · passages-aval.md F02 · chemins-aval.md F03

The promise is the relecteur's (L167-169: the block goes back to the Détailleur, never to a fresh Réalisateur) and the first round asked for it (C14, D-5); nothing carries it. Three shapes, none of them the relecteur's to pick — each puts a mode on a different agent and decides what a wrong sheet costs.

| Option | What it takes | What it costs |
|---|---|---|
| **A — delete and re-detail** | `/8_code` deletes the lot's `fiche-executable.md`, `conception.md` and `tests.md` on `Cause: sheet` and runs the Détailleur on the block in its ordinary mode, which writes the missing sheet (move 1) | The Détailleur reads no verdict (detailleur.md L672-673) and rewrites from the same entries — it can reproduce the defect; the declarations and tests the lot already put in the worktree stay there, and the Concepteur "declares only what is missing" (concepteur.md L163-164) against a sheet that changed |
| **B — a third Détailleur mode** | `Mode: sheet` on one lot, fed the verdict's `## Findings`, rewriting that sheet from the entries; `/8_code` then invalidates `conception.md` and `tests.md` | A new mode in the Détailleur and a new prompt in `/8_code`; the same leftover code as A; and whether `## Attempts` restarts on the rewritten sheet has to be said |
| **C — stop on the Product Owner** | `Cause: sheet` is relayed like an "anything else" block (8_code.md L422); the relecteur's L167-169 is rewritten to say the orchestration stops | Every wrong sheet costs a human round trip; no new mechanism, and no agent rewrites a sheet nobody has judged |

Whichever is chosen, realisateur.md L519-520 (two rows, no `sheet`) and relecteur.md L167-169, L407 follow it.

### Who reads a reservation — relecteur.md F12

`decisions.md` keeps `PASS with reservation` and settles that it counts as coded. The entry above gives the note a place (`## Findings`); nobody is named to read it, and `/8_code` L200-201 says it never reads `## Findings`.

| Option | What it costs |
|---|---|
| **Keep the row, no reader** | The note is written for nothing — the pass sheet's ### 10 (passes/relecteur.md L328-335) named exactly that |
| **Give it a reader** — the Détailleur of the next block, or the Contrôleur at `/9_controle` | A new input on that reader, and a rule on what a reservation changes for it |
| **Drop the row** | Reopens the premise of a settled question — the Product Owner's, not this plan's |
