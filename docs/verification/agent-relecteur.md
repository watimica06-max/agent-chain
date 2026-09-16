# Vérification — `relecteur.md`

Files read: `.claude/agents/relecteur.md` (old, 324 lines),
`.claude-new/agents/relecteur.md` (new, 416 lines),
`docs/refonte/passes/relecteur.md` (17 comments), `docs/refonte/modifications.md`
lines 1175–1240 (`# relecteur.md`) plus lines 1416–1428 (`# 8_code.md`, for the
`## Attempts` field) and line 1596 (the per-file résumé). Cross-checks by grep
only: `.claude-new/commands/8_code.md`, `.claude-new/agents/{concepteur,testeur,
realisateur,verificateur,architecte,detailleur}.md`.

Line numbers below are those of the **new** file unless marked *old*.

Pass sheet, as modifications.md states it: **Passés (12)** C1 · C2 · C3 · C4 ·
C5 · C6 · C7 · C11 · C12 · C13 · C15 · C16 · **Reportés (5)** C8 · C9 · C10 ·
C14 · C17, "tous sur `/8_code`" · **Écartés (0)**. Structural modifications:
three rows — point 2 largely mechanical (testeur), point 3 widened to
`permanente` rules, point 4 lightened (compilation proved by the run).

⚠️ **The record's numbering does not match the pass file.** Its "plus
structurants" table describes C11 as the `FAIL structurel` redefinition
(pass file **12**), C13 as the empty cases (pass file **14**), C15 as
build-read-first (pass file **16**); its deferred row names "le plafond des
trois tentatives" (pass file **11**) and "ses blocages qui arrêtent sur le
Product Owner" (pass file **15**) while listing both 11 and 15 as PASSÉ. Below
I match on the pass file's own numbers and report what the files show; the
record's lists are wrong in five places (see the last column of A).

---

## A. Conformity

| # | Expected (pass file) | Found (new file, or `/8_code` where the comment targets it) | Verdict |
|---|---|---|---|
| **C1** (PASSÉ) | One retirement rule, executable with the agent's tools: either it gets a tool that renames and the "delete" sentence goes, or retirement is not its job and the orchestration renames after the verdict. The unmatched `Edit` tool and "When `Edit` fails" go if nothing edits | Both branches were applied at once. Lines 204–206: "You never retire it — you have no tool that renames or removes a file. The orchestration does it". Lines 276, 278–281, 288–293: "Apply it, then rename it `blocked_relecteur-NN.md`" · "Renaming means renaming — `git mv`" · "Rename the file once applied, by `git mv`, to `blocked_<agent>-NN.md`". Tools line 4 unchanged: no Bash. `Edit` still in the tools, "When `Edit` fails" still at 254–260. `/8_code` new has no rename move for a relecteur file (grep `rename\|git mv\|-NN`: only `stop1.md` and `redecoupage-NN.md`) | **BLOCKING — not fixed, made worse.** The old file said rename *and* delete; the new says rename *and* never-retire, and still has no tool for the rename. "The orchestration does it" names a gesture no command performs. `Edit` and its section stay with nothing using them |
| **C2** (PASSÉ) | The agent holds an independent list of changed files, from the prompt; reads those as "the code the lot touched"; checks `## Outside the lot` against that list. "No code committed" stops being one of its block cases | Lines 59–60, 64–66: prompt is the only source, "you cannot grep a commit". Line 374 still says "Check it against the diff" without tying "the diff" to the prompt's list. Line 210–211: block cases still "no sheet, no report, or no code committed" | **Fixed in substance, one leftover.** The "no code committed" block case was to go (and `/8_code` 102–103 makes it unreachable: empty list → not invoked); it stays. TO FIX |
| **C3** (PASSÉ, on `/8_code`) | The relecteur's invocation written out; its prompt carries the files the lot's commits changed; an empty list = failed attempt, relecteur not invoked | `/8_code` new 97–103 and 233–236: `git diff --name-only` between the lot's first commit and `HEAD`; invocation block with "Files the lot's commits changed"; empty list counts as a failed attempt | **Fixed as asked.** Side effect the pass file could not foresee: the diff now spans the concepteur's commit too (concepteur.md new 170 commits), see D-9 |
| **C4** (PASSÉ) | A bounded source for "which uncoded lots of my block cite this symbol": the block line of `code/sequence.md`, the PASS verdicts of that block's lots, one grep across those sheets; "Nothing else" amended; "affects none" when no sheet cites it; the paragraph moves **out of** "What you do not check" | Lines 71–74 (exception to "Nothing else"), 164–172 (the procedure, "affects none"). Lines 86–91: the two paragraphs are **still under "What you do not check"**, unchanged | **Fixed in substance, not in form.** The paragraph was duplicated, not moved. TO FIX (see D-2) |
| **C5** (PASSÉ) | One policy: a divergence backed by a filled decision → `## Symbol divergences`, not a failure; with no decision → finding of point 1. The agent needs a source to tell which is which (settled `blocked_realisateur-NN.md`, or a report field). Example rewritten to agree with the table | Lines 102, 155–162: the two-way policy, stated as asked. Example 129–142 agrees with the table (`FAIL mineur`, findings listed, a propagated divergence). **No source for the switch**: "What you read" (53–74) names neither `blocked_realisateur-NN.md` nor a report field, and realisateur.md new (131–166) has no field naming the decisions applied — its report is `## Symbols · Outside the lot · Build · State · Requests` | **Policy fixed; its input missing.** The one fact that decides `FAIL structurel` versus propagation is observable by nothing the agent reads. BLOCKING (see C-3) |
| **C6** (PASSÉ, on `/8_code`) | The command reads Status and Symbol divergences and says so; move 4 (now 5) runs on the final verdict only, after the retries | `/8_code` new 45–46, 127–135: "On the final verdict only — never on a FAIL about to be retried"; "You read two fields of a verdict — `## Status` and `## Symbol divergences`, and nothing else" | **Fixed as asked** — with an internal contradiction in `/8_code`: 41–43 says three lines (`## Status`, `## Attempts`, `## Cause`), 134–135 says two fields and nothing else. Outside this file; noted for the `/8_code` pass |
| **C7** (PASSÉ) | A field listing every failed point with its object; Cause carries the category alone; "divergence" reserved for the symbol case, other gaps are findings; Verified says it copies a claim | Lines 129–133, 149–152: `## Findings`, one line per point with the object. 154: Cause = category alone. 175–177: "You copy a claim, you do not establish it". **"Divergence" not reserved**: 356 "A missing field is a divergence", 382–383 "Missing there is a divergence as well", 317–318 "is a divergence too" (that one is a symbol, fine) | **Three of four applied.** The word is still used for a missing report field and a missing sheet field, the two senses C7 named. TO FIX (see D-1) |
| **C8** (REPORTÉ, on `/8_code`) | The command reads Cause and states the count of "limit of reasoning" causes from which the fresh Réalisateur is passed opus | `/8_code` new 118–120 and 253–254: "`Cause: reasoning` twice on one lot → the third realisateur is passed `opus`" | **Listed REPORTÉ, found APPLIED.** The record is wrong. And the literal the command matches — `reasoning` — is not the word the agent is told to write: 106–107 says "understanding of the lot, or limit of reasoning", the example (137) writes `understanding`. Whether the agent writes `reasoning` or `limit of reasoning` is unsettled. TO FIX in the agent (see D-7) |
| **C9** (REPORTÉ) | Remove "Only the second would justify Opus, and the threshold is set on the accumulated causes"; name the two categories and the test that separates them | Lines 108–109 unchanged | **Not applied — consistent with REPORTÉ.** But C8 was applied in `/8_code`, so the threshold this sentence alludes to now exists there (two `reasoning` on one lot): the deferral has lost its reason |
| **C10** (REPORTÉ) | `PASS with reservation` goes; Status carries three values | Line 100 row unchanged; 191 "one of the four words" | **Not applied — consistent with REPORTÉ.** `/8_code` still resumes on "no `verdict.md` carrying PASS" (60–61, 287): the ambiguity C10 and C11 describe is intact |
| **C11** (PASSÉ, on `/8_code`) | The resume test is exact (the line is `PASS`); move 3 states that a fix is followed by a relecteur on the same lot, that the relecteur overwrites the verdict, that one retry = one fix-and-review | `/8_code` new 60–61: "no `verdict.md` carrying PASS" (unchanged). 109–110: "On FAIL → a fresh `realisateur`, with the verdict. Three retries maximum per lot" — nothing says the relecteur runs again, nothing about overwriting. Only the agent's `## Attempts` rule (144) implies a verdict is replaced | **Listed PASSÉ, found NOT applied.** The record is wrong; the loop's retry unit is still undefined |
| **C12** (PASSÉ) | structurel defined by what fails (point 4 red/not run, point 1 absent/unauthorised-divergent), everything else mineur however many; "no full re-review" goes | Lines 101–102: exactly that; "the re-review is full: a fix can break another point" | **Fixed as asked.** Leftovers: 104 and 247 "Never fall to structurel by default for an isolated gap" now guard against a reading the table no longer permits — harmless, NOTE |
| **C13** (PASSÉ) | One scope for point 3. If the two universal checks stay, they are stated apart from the sheet's list with the test each applies; the conventions file is read by section | Line 61–62: read "the rules the sheet names, and every rule marked `permanente`" — by section, as asked. Lines 338–340 unchanged: "Only those a grep settles — a hardcoded user-facing string, an identifier not in English, a convention the sheet named explicitly" — the two universal checks still listed as peers, no test stated. 342–344: sheet's list + `permanente`. 349–350 unchanged: "You check the rules the sheet names" | **Reading list fixed; scope not unified.** Point 3 now states three scopes in twelve lines (the two universals + named · named + `permanente` · named only). TO FIX (see D-3) |
| **C14** (REPORTÉ) | A sheet lacking a section the checklist depends on is a finding against the sheet **and the status it yields**; a removal is a third row of point 1; a test that does not run does not count | Lines 387–391: all three cases present — "a sheet with no criteria yields no `PASS` on point 2: it is a finding against the sheet, and the Détailleur's, not the lot's" · "A test that does not run does not cover its criterion" · "a symbol … that no longer resolves is point 1's third case". The status it yields: **not stated**. Point 1's table (312–315) still has two rows; the "third case" exists only in this paragraph, 75 lines below | **Listed REPORTÉ, found APPLIED — partly.** The record is wrong. The finding "against the sheet" has no status and no route: `/8_code` sends every FAIL to a fresh Réalisateur (109), who cannot fix a sheet. TO FIX (see D-5) |
| **C15** (PASSÉ, on `/8_code`) | A relecteur block naming a missing report → fresh Réalisateur, counted; a missing sheet → Détailleur; the Product Owner only at the ceiling | `/8_code` new 327–336: "The Relecteur and the Contrôleur do not call it either — their blocks say something is missing" · "Any other block → relay it and stop. The Product Owner fills `## Decision`" — unchanged from old 224 | **Listed PASSÉ, found NOT applied.** The record is wrong; every relecteur block still stops on the Product Owner |
| **C16** (PASSÉ) | The build claim is read first; when it yields structurel, the verdict is written from that alone, other points not run | Lines 301–305: exactly that | **Fixed as asked.** Two consequences not handled: 286 "then run the five checks from the start" and 359–371 (point 4's own red-module rules) now describe a path the head rule closes — see D-6; and what `## Findings` and `## Cause` hold on a verdict "written from that alone" is unsaid — see D-8 |
| **C17** (REPORTÉ) | One bounded check on the changed files: every symbol declared there that neither the sheet nor the report's `## Symbols` names is a finding; symbols not branches; yields mineur | Lines 393–399: exactly that, as a widening of point 5 | **Listed REPORTÉ, found APPLIED.** The record is wrong. Applied as asked; two side effects in D-4 and D-10 |

**Record versus files, in one line**: PASSÉ but not applied — **C11, C15**;
REPORTÉ but applied — **C8, C14, C17**; PASSÉ and applied against its own
letter — **C1** (both branches), **C4** (duplicated, not moved), **C7** (term
not reserved), **C13** (scope not unified), **C5** (no input for the switch).

---

## B. Unannounced changes

Every hunk of the diff maps to a comment or to one of the three structural
rows — except the following.

| # | Old | New | What it changes | Severity |
|---|---|---|---|---|
| B-1 | *old* 102: "four fields" — Status, Verified, Cause, Symbol divergences | 115–123: "six fields", with **`## Attempts`** (144–147: "the count the verdict you replace held, plus one — `1` when there was no verdict") | A new output field, with a reader (`/8_code` 112–116). Announced only in the **`/8_code`** section of modifications.md (line 1425, "Le Relecteur écrit ce champ"), not in this agent's section nor in any of the 17 comments. Not a defect of the change — a gap in the record | NOTE |
| B-2 | *old* 57: "**The code the lot touched**, and the tests" | 57–58: "**`code/<lot>/conception.md`** and **`code/<lot>/tests.md`** — what the concepteur declared and what the testeur covered" | Two new inputs. `tests.md` has a reader (331–333, `## Criteria with no test`). **`conception.md` has none**: no point of the checklist names it, and point 5's symbol check (396–398) uses "the sheet" and "the report's `## Symbols`" only. Covered by the structural row "Point 2" for `tests.md`; nothing announces `conception.md` | TO FIX (see C-6) |
| B-3 | *old* 121–122: "`## Verified` copies what `## Build` claims, in one line: which command ran green, and how many tests" | 175–177: same, plus "You copy a claim, you do not establish it" — and the example 127 changed from `:core-domain:check green, 47 tests` to `<the report's build claim, copied>` | Asked by C7 (Verified must not read as established). The example lost its concrete shape — a placeholder where the old line showed what "one line" means. Cosmetic | NOTE |
| B-4 | *old* 116–119: the example divergence names a real symbol, `ActivityReconciliationService.reconcile — returns bool, sheet says ReconciliationResult` | 139–142: `<symbol> — returns <what the code has>, sheet says <what it promised>` | Neutralised. No comment asks it. Harmless; the pattern is the same | NOTE |
| B-5 | *old* 229: "Delete the file once applied" | 288–293: "Rename the file once applied, by `git mv`, to `blocked_<agent>-NN.md` — the highest number beside it, plus one" | The **direction** is C1's; the **text** is a paragraph shared verbatim with detailleur.md new 445 and realisateur.md new 464 — placeholder `<agent>` not instantiated (the file writes `blocked_relecteur-NN.md` at 269–270, 276), and a second numbering formula next to "next free number" (276). Both differ when the sequence has a gap | TO FIX |
| B-6 | *old* 254–257: point 2 in one paragraph | 323–336: the "Match on what the test asserts" sentence became its own paragraph; "The correspondence is direct — a criterion with no test is an observable gap" kept after the new `## Criteria with no test` rule | Reordering only; but the kept sentence now reads against the new rule two lines above it — see D-11 | NOTE |
| B-7 | *old* 266–268: "The sheet's `## Conventions` says which ones. Open each rule it names and check the lot against it" | 342–347: split into two paragraphs, "Open each and check the lot against it" | Rewording to fit the `permanente` widening. "Each" now has two antecedents (the named rules and the `permanente` ones) — that is the intent | NOTE |
| B-8 | *old* 307: "**5. Nothing the lot writes goes unused by the lot itself.** 🔴 **What it receives…" | 393–401: new heading "…and nothing it declares was unasked", new paragraph, then "📌 **It yields `FAIL mineur`.** 🔴 **What it receives and never reads…" on the **same line** | The C17 paragraph was inserted mid-sentence: the old self-use rule now begins in the middle of a line about the unasked-symbol case, and "It yields `FAIL mineur`" attaches to one case while the other has no stated status (mineur by the table's "everything else", but the reader has to go back 300 lines) | TO FIX |

No section was renumbered, no table rewritten beyond the verdict table (C12)
and the example (C7). Frontmatter (name, description, tools, model, effort)
unchanged — which is itself the C1 defect: `tools` was to change or `Edit`
was to go.

---

## C. Gestures against tools

Frontmatter (line 4): **Read, Grep, Glob, Edit, Write.** No Bash, no Agent.

| # | Gesture | Where | Tool | Verdict |
|---|---|---|---|---|
| C-1 | Read the sheet, the report, `conception.md`, `tests.md`, the changed files, the conventions by section, the block line of `sequence.md`, the other lots' sheets and verdicts | 55–74, 166–169 | Read, Grep, Glob | Has the means |
| C-2 | "Rename it `blocked_relecteur-NN.md`" · "`git mv`, or the equivalent" · "Rename the file once applied, by `git mv`" | 276, 278, 288 | **None.** No Bash; Write creates, Edit edits in place; neither renames or removes. The file itself says so at 204–205 | **BLOCKING** — three instructions with no tool, next to a sentence admitting it. The agent that obeys 276 with Write leaves the unnumbered file in place, which 283–284 says reads as a block still standing |
| C-3 | Tell a divergence "with a decision behind it" (propagate) from one "with no decision behind it" (`FAIL structurel`) | 102, 155–162 | **No input.** Not a tool gap: the tools could read `code/<lot>/blocked_realisateur-NN.md` or a report field, but "What you read" names neither and the report has no such field (realisateur.md new 131–166) | **BLOCKING** — the switch between "fix the code" and "rewrite the block's sheets" rests on a fact the agent is not told where to find |
| C-4 | "Check it against the diff" (`## Outside the lot`) | 374 | The prompt's file list (64–66), read by eye. No git needed | Has the means, once "the diff" is read as "the list the prompt names" — the word should say so. NOTE |
| C-5 | "A test that does not run does not cover its criterion" | 389–390 | No Bash: the agent cannot run a test. It can grep a skip/ignore marker, and read `tests.md` `## Red` (testeur.md new 204–213, "every new test failed") | **Question**: is "does not run" meant as *disabled in the source* (greppable) or *not executed by the build* (not observable here)? The sentence does not say |
| C-6 | Read `code/<lot>/conception.md` | 57–58 | Read | A tool with a read and **no gesture that consumes it**: no point names `conception.md`. Either point 5's "neither the sheet nor the report's `## Symbols`" was meant to include `## Declared`, or the bullet is dead weight loaded every run. TO FIX |
| C-7 | `Edit` | 4, 254–260 | — | **A tool no gesture uses.** The verdict (115) and the blocking file (201) are written whole; nothing edits a file in place. C1 said the tool and its section go if nothing edits. TO FIX |
| C-8 | Grep the divergent symbol across the block's uncoded sheets; know which lots carry no `PASS` | 167–169 | Grep, Glob, Read on `code/<other-lot>/verdict.md` | Has the means. The verdict files of other lots are not in "What you read" — the exception at 71–74 names "the sheets", not the verdicts that say which sheets. NOTE |
| C-9 | Grep every symbol declared in the changed files against the sheet and `## Symbols` | 396–398 | Grep, Read | Has the means — one read per changed file for the declarations, the symbol list already in hand from point 1. Cost is bounded by the prompt's list |

---

## D. Internal coherence

| # | Line | Quote | What is wrong | Severity |
|---|---|---|---|---|
| D-1 | 204–206 vs 276, 278–281, 288–293 | "You never retire it — you have no tool that renames or removes a file. The orchestration does it" · "Apply it, then rename it `blocked_relecteur-NN.md`" · "Renaming means renaming — `git mv`" · "Rename the file once applied, by `git mv`" | A rule contradicted three times in the same file, 70 lines apart. And "the orchestration does it" is a procedure branch that leads nowhere: `/8_code` new has no such move | **BLOCKING** |
| D-2 | 86–91 vs 164–172 | "A divergence only threatens the uncoded lots of the same block … Name those lots in the verdict" under **"What you do not check"** · the same rule, with its procedure, under "What you write" | The same thing said twice, once under a heading that says the opposite of what the paragraph is (a thing to write). C4 asked for a move, the file did a copy | TO FIX |
| D-3 | 338–340 vs 342–344 vs 349–350 | "Only those a grep settles — a hardcoded user-facing string, an identifier not in English, a convention the sheet named explicitly" · "The sheet's `## Conventions` says which ones — and every rule marked `permanente`" · "You check the rules the sheet names, on the lot" | Three scopes for one check. Two readers apply two of them. The `permanente` widening (structural row "Point 3") is contradicted six lines later by the unchanged "Not a full audit" paragraph | TO FIX |
| D-4 | 356, 382–383 vs 149–162 | "A missing field is a divergence" · "Missing there is a divergence as well" · `## Symbol divergences` "is for propagation, never for a failure" · never-do 250 "Report a divergence without naming the lots it affects" | "Divergence" in two senses: a symbol fact to propagate (with affected lots) and a missing field (a finding). Read literally, a missing `## State` line must name the lots it affects and belongs in the propagation field | TO FIX |
| D-5 | 387–389 | "a sheet with no criteria yields no `PASS` on point 2: it is a finding against the sheet, and the Détailleur's, not the lot's" | A branch that leads nowhere: no status is named (mineur by "everything else"? structurel? neither fits — the lot did nothing wrong), `## Findings` is defined as "every point that failed" on the lot (149), `## Cause` has no category for "the sheet", and the only reader of a FAIL sends a fresh Réalisateur (`/8_code` 109) who cannot rewrite a sheet | TO FIX |
| D-6 | 301–305 vs 286, 359–371 | "It says the module is red or the tests did not run — write the verdict from that alone and run no other point" · "then run the five checks from the start" · point 4: "The lot's own module not compiling, or its tests not running, is a `FAIL structurel` — whatever reason the report gives" | The head rule closes the path point 4 still describes at length (359–371: eleven lines on a red own-module, reachable only if the head rule was not obeyed). Not contradictory — the same verdict — but a rule stated twice, once as "first" and once as "fourth". 286 ("the five checks from the start") ignores the head rule | NOTE |
| D-7 | 106–107, 137 vs 154 | "understanding of the lot, or limit of reasoning" · example `understanding` · "`## Cause` carries the category alone" | The second category has no fixed literal — `limit of reasoning`? `reasoning`? — and `/8_code` 118 matches on `Cause: reasoning`. The first category is a single word in the example; the second is three words in the rule. Two readers write two strings; one of them the orchestration never matches | TO FIX |
| D-8 | 301–305 vs 115–162 | "write the verdict from that alone" | What the six fields hold on that verdict is unsaid: `## Findings` (which point? "point 4" before point 4 ran), `## Cause` (neither category describes a build that did not run), `## Symbol divergences` (not examined). 179–182 covers `## Verified` and `## Status` only | NOTE |
| D-9 | 373–375 vs 57–58, 64–66 | "`## Outside the lot` names every file the lot touched that its sheet does not declare … Check it against the diff" | `/8_code` computes the list "between the lot's first commit and `HEAD`" — the concepteur commits first (concepteur.md new 170), so the list holds his files too. `conception.md` and `tests.md` carry their own `## Outside the lot` (concepteur.md new 190–192, testeur.md new 208–210), which the relecteur reads but is not told to use. **Question**: is the check "the report's `## Outside the lot` alone against the whole list" — in which case a file the concepteur declared and the Réalisateur did not is a false finding — or "the three `## Outside the lot` together"? | TO FIX (as a question) |
| D-10 | 396–398 vs 317–318 | "every symbol declared there that neither the sheet nor the report's `## Symbols` names is a finding" · "A symbol in the sheet that the report does not list is a divergence too" | Asymmetric on purpose (C17's wording) — but it makes `## Symbols` self-certifying: a symbol the sheet never asked for passes point 5 as soon as the report lists it. Point 1 checks sheet → report; nothing checks report → sheet. **Question**: intended? | NOTE |
| D-11 | 331–333 vs 335–336 | "A criterion in `## Criteria with no test` of `tests.md` is not a gap" · "The correspondence is direct — a criterion with no test is an observable gap, not a judgement call" | Two adjacent sentences; the second is true only with "and not listed there", which it does not say | NOTE |
| D-12 | 99 vs 301–305 | "PASS — The five points pass" | Fine as written; but with the head rule a review can end before any point ran, and 104/247 "Never fall to structurel by default for an isolated gap" now guards a reading the table (101–102) no longer allows. Dead guard | NOTE |
| D-13 | 289 vs 269–270, 276 | "`blocked_<agent>-NN.md`" vs "`blocked_relecteur-NN.md`" | Placeholder not instantiated; shared paragraph (see B-5). Two numbering rules: "next free number" (276) vs "the highest number beside it, plus one" (289) | NOTE |
| D-14 | 144–147 | "`## Attempts` carries the count the verdict you replace held, plus one" | Coherent in the file. Across the loop: `/8_code` 102–103 counts an empty diff as a failed attempt and does **not** invoke the relecteur — so that attempt is never written to disk, and 113–116's "the count lives on disk" undercounts by one per such attempt. Outside this file; noted for `/8_code` | NOTE |
| D-15 | 47–51, 410–416 | three and four consecutive `---` | Empty separators, pre-existing in the old file (*old* 47–51, 318–324). Cosmetic | NOTE |
| D-16 | 22–23 vs 164–172 | "One invocation per lot, at its realisation — never at the end of a block" | Consistent with the divergence procedure, which reads one block line and other lots' sheets without reviewing them. No contradiction; recorded because the exception at 71–74 is the first time the agent opens anything of another lot, and 68–69 "Nothing else… not the lot list, not the sequence" now has an exception four lines below it — the "Nothing else" should carry the exception in the same sentence | NOTE |

---

## Summary

- **Two BLOCKING**: the settled-block retirement (C1 / D-1 / C-2) — the
  file now says "you never retire it" and "rename it by `git mv`" with no tool
  for either; and the decided/undecided divergence switch (C5 / C-3) that
  decides `FAIL structurel` on a fact the agent has no source for.
- **The record is wrong in five places**: C11 and C15 are listed PASSÉ and
  were not applied in `/8_code`; C8, C14 and C17 are listed REPORTÉ and were
  applied. The "plus structurants" table numbers three comments off by one.
- **TO FIX, in the file**: C2's leftover block case ("no code committed",
  211); C4's duplicated paragraph under "What you do not check" (86–91); C7's
  "divergence" still meaning a missing field (356, 382); C13's three scopes
  for point 3 (338–350); C14's finding against the sheet with no status and no
  route (387–389); the `Cause` literal `/8_code` matches (106–107 vs `Cause:
  reasoning`); `conception.md` read and never used (57); `Edit` and its section
  with nothing to edit (4, 254–260); the C17 paragraph spliced mid-sentence
  into point 5 (399); the `<agent>` placeholder and second numbering rule
  (289).
- **Questions**, not verdicts: whether `## Outside the lot` is checked from
  the Réalisateur's report alone against a diff that includes the concepteur's
  commit (D-9); whether "a test that does not run" means disabled-in-source or
  not-executed (C-5); whether a symbol the report lists and the sheet does not
  is meant to pass point 5 (D-10).
