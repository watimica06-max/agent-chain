# Vérification — `realisateur.md`

Read: `.claude/agents/realisateur.md` (old, 525 lines),
`.claude-new/agents/realisateur.md` (new, 606 lines),
`docs/refonte/passes/realisateur.md` (18 comments, `### N`),
`docs/refonte/modifications.md` § `# realisateur.md` (lines 1083-1174,
four structural modifications with "La demande"). Neighbouring new
files (`concepteur.md`, `testeur.md`, `arbitre.md`, `architecte.md`,
`8_code.md`) were grepped only, to check that the files the new text
names exist. Line numbers below are the **new** file's unless stated.

The pass sheet claims **11 passés, 1 écarté (C9), 6 reportés**, and
four structural modifications. Found: **3 passés as asked (C2, C10,
C15 — each with a residue) · 7 partiel (C1, C4, C5, C6, C7, C11, C18)
· 1 applied against the pass's request (C8) · 1 écarté confirmed ·
6 reportés confirmed not applied.** Of the four modifications, all four
are applied where announced; modification 1 leaves six passages saying
the opposite, including the frontmatter description.

Two findings block: the FAIL-mineur row now ends before the commit
(D-2), and the file's own description still says the agent writes the
tests (D-1).

---

## A. CONFORMITY

### The four structural modifications ("La demande")

| # | Expected (La demande) | Found in the new file | Verdict |
|---|---|---|---|
| **M1** | Fills the bodies until the tests pass; never modifies a test; naming symbols, writing declarations and writing tests are removed | L15 role rewritten; L20-29 tests are red, never touch a test, no declaration; L529-535 move 5 "Fill the bodies". **But** six passages still describe the old role: L3 frontmatter *"write the code and the tests … Writes one test per acceptance criterion"*; L52 *"You write the code, the tests, and compte-rendu.md"*; L131 *"The code and the tests, then compte-rendu.md"*; L204 *"A test to adapt … those go in the normal output"*; L380 never-do *"Write a test matching no criterion"*; L381 never-do *"Delete a test — adapt it"* | **APPLIED, six contradictions left** — see D-1, D-3 |
| **M2** | Reads the `permanente` rules whole plus those the sheet names, with the emphasis; the contradiction *"apply TECHNICAL_CONVENTIONS.md to everything you write"* vs *"the sheet names the rules"* disappears | L66-71 exactly as asked, emphasis included. **But** L90 still opens *"Apply `docs/TECHNICAL_CONVENTIONS.md` to everything you write"* followed by L91-93 *"The sheet's `## Conventions` names the rules bearing on this lot — open each one and hold it"* — the pair the demand says disappears is intact | **APPLIED, the sentence the demand removes is still there** — TO FIX |
| **M3** | Carries on with what does not depend on the lack; stops when nothing is left; a second lack is added to the blocking file, never replaces it | L217-231, all three points, plus "say in your report what you did write" | **APPLIED** (shape of a two-entry blocking file unspecified — D-11) |
| **M4** | Blocks when two attempts in a row fail for the same reason; observable fact, not duration; the two cases | L551-561, table and the caught case, verbatim from the demand | **APPLIED** |

### The comments

| # | Expected (pass file, *Ce qu'il faut*) | Found in the new file | Verdict |
|---|---|---|---|
| **C1** | The whitelist contains exactly the commands the procedures require — rename, removal, discard of the working tree — and an obedient agent can run every procedure | L570-571 whitelist now `git add, commit, status, git mv, git restore` + conventions' commands. **But** L387-389 never-do entry unchanged: *"Run a shell command that is not `git add`, `commit`, `status`, or one the conventions name"* — the "two passages asking for different things" the comment was written against is recreated between the two whitelists. Removal: no longer needed (C2 replaced delete by rename). Discard: `git restore` restores tracked files; it does not remove an untracked file the agent created — see C-2 | **PARTIEL** — TO FIX |
| **C2** | One fate for an applied blocking file, stated once: renamed to the next free number, kept; the "How you apply it" fragment attached or removed | L463-468 rename by `git mv`, never delete, the numbered ones are the record. L452 fragment now *"How you apply a filled decision"*. **But** (a) "stated once" is not met: rename is now said three times in the section (L430 row, L433-436, L463-468) plus L276 and L301; (b) L464 names the target **`blocked_<agent>-NN.md`** — a placeholder, where every other line says `blocked_realisateur-NN.md` | **PASSÉ in substance** — TO FIX the placeholder (D-6) |
| **C4** | (i) The report is a move, written before the commit and staged with the lot — or the file says it is not committed and why; (ii) the report shape carries a field for what governed the code besides the sheet (a decision applied, naming the numbered file; a convention invoked), so the Relecteur reads a differing signature as decided, not drift | (i) L565-568 move 8 writes the report, move 9 commits — done; whether the report is staged is not said (*"staging explicitly what belongs to the lot"*, L568). (ii) **Not done**: L134-156 still five fields, none for a decision or a convention invoked. The four passages the comment listed as writing into no field are all still there, and a fifth was added: L455-456 *"say so in your report"*, L304 *"Say in your report that the lot goes back"*, L213 *"name it in your report"*, L230 *"Say in your report what you did write"*, L482-483 *"stop and report"*. modifications.md records C4 as *"le rapport devient un geste"* only | **PARTIEL** — TO FIX (the Relecteur-drift justification is untouched) |
| **C5** | At each of the three block triggers, the instruction names the block — file to write, Arbitre to call — not "report"; "report" reserved for `compte-rendu.md` | Move 5 regression, L537-541: done, with the reason. **Not done**: L190-192 *"When the sheet is wrong … stop and report"*; L482-483 *"If you judge it wrong, stop and report rather than coding against it"*. L204 *"Blocking is not reporting"* still faces them | **PARTIEL — 1 of 3** — TO FIX |
| **C6** | (a) Move 3 reads the two sections whole *and* greps the document for every symbol the sheet lists as modified; (b) move 7 points to where the rule is; (c) one authority on what earns a place — the skill governs and the body does not restate, or the body states and the skill is not loaded | (a) L516-520 done, with the "general" reasoning. (b) L563 still *"Update the technical state — see below"* — nothing follows; the rule is at L105-125, above. (c) L109 still loads the skill **and** L112-114 still states *"What earns a place: a service, a provider, a mechanism…"* — two authorities kept. A new paragraph L119-122 adds a third grep target (*"your symbols, the files you edited"*) that does not coincide with move 3's (*"every symbol the sheet lists as modified"*) — see D-9 | **PARTIEL — (a) only** — TO FIX |
| **C7** | One reading rule: whole file with the sheet's list as pointer, **or** named rules plus the always-needed sections (location, verification commands, deliverable states) named by section; the agent never has to guess whether an unopened rule exists | Rule chosen: `permanente` whole + sheet-named (L66-67). The always-needed facts are still invoked without a reading that guarantees them: L491-493 *"the conventions say where"*, L571-572 *"the analysis and test commands the conventions name"*, L210-211 *"the conventions are what says which states a lot may be delivered in"*. Question for `architecte.md`: are placement, verification commands and deliverable states tagged `permanente`? If not, the agent guesses exactly what the comment forbids. And L90 keeps the whole-file wording (M2 above) | **PARTIEL** — question |
| **C8** | A missing convention that decides how the lot is written (where a symbol lives, which layer owns it) is a **block**, settled mid-lot through the Arbitre; the end-of-lot request stays for what only verification needed; boundary stated by effect on the code | L498-500: *"A kind of symbol the conventions do not place, and the concepteur did not either — a conventions request, and you carry on where the sheet points."* This is the **opposite** route: request (end of lot), not block (mid-lot). The boundary by effect on the code is not stated. It also contradicts L491-493 two lines above (*"the Détailleur does not decide the location"*) — where does "where the sheet points" come from? See D-7. With the concepteur placing declarations the case shrinks, but the row that remains routes the wrong way | **NOT AS ASKED** — TO FIX |
| **C9** | ÉCARTÉ — untestable criterion takes the wrong-sheet path | No such text in the new file. `tests.md`'s `## Criteria with no test` is the testeur's; the realisateur reads only `## Red` (L74-75) | **NOT APPLIED — as required** |
| **C10** | A stated small-integer bound on fix-and-rerun on one failure, then block with what was tried; the block names the failing test and the criterion | L551-561: two attempts, same error → block. **Not said**: that the block names the failing test and its criterion (L534 says it for the test-would-have-to-change case only) | **PASSÉ** — NOTE |
| **C11** | FAIL mineur ends with moves 6 to 8 and the report like any run; the previous report is an input, read and amended; on **either** FAIL kind the failed attempt's state entries are the fresh run's to correct, `## State` says so | L479: *"amend the report — read it, never rewrite it from the code … but the run ends as any other: moves 6 to 8, then the report."* Written against the **eight**-move numbering: under the nine moves, 8 *is* the report and **9, the commit, is not reached** — the very loss (*"a fix not committed is not merged"*) C11 was raised for. L480 FAIL structurel: state cleanup added. FAIL mineur: no state cleanup, contrary to "either FAIL kind". L474-475 *"Inputs: the same, plus the verdict"* — the previous `compte-rendu.md` not added to the inputs | **PARTIEL, and the renumbering broke it** — BLOCKING (D-2) |
| **C15** | The back-to-split test is the presence of `code/redecoupage.md`, on both rows named (the Arbitre table **and** the same row in Part 2) | L277 and L291-295: done, with the reason. **But** L431 Part 2 row still *"A `## Decision` sending the lot back to the split"* — the wording test the comment removes, on the row it explicitly targeted | **PASSÉ on one of two rows** — TO FIX (D-8) |
| **C18** | Drop the measurement parenthesis; drop "commands the Cadreur"; one statement of no-rationale; "static analysis" for "analyze"; a neutral word for "provider" | L545-546 parenthesis gone. "Commands the Cadreur" gone (replaced, see B-1). **Kept**: L173-174 and L177-178 both still state the no-rationale rule; L546 *"a screen and its provider"*; L3 *"run analyze and test"*, L146 *"analyze: clean"* | **PARTIEL — 2 of 5** — NOTE |

### Reportés — confirmed not applied

| # | Where it would show | Found |
|---|---|---|
| **C3** | Reprise: uncommitted non-compiling code vs "never leave a dirty tree"; `## Decision` line under the reprise shape | L333-334 and L401 unchanged; L336-338 `## Decision` line still under the reprise shape. Not applied |
| **C12** | Detection of the FAIL case / `verdict.md` | L50 and L474-475 unchanged. Not applied |
| **C13** | Part 2 row "still empty → call the Arbitre" | L429 unchanged. Not applied |
| **C14** | The PASS-lot paragraph | L458-461 unchanged. Not applied |
| **C16**, **C17** | Command only | Nothing in the agent. Not applied |

---

## B. UNANNOUNCED CHANGES

Every hunk of the diff maps to a modification or a comment, except
two contents inside C18's and C6's hunks:

**B-1 — L124-125, a readers list.** NOTE.
Old L102: *"⚠️ This document commands the Cadreur."*
New L124-125: *"📌 Its readers: the Détailleur, the next Réalisateur, the Diagnostiqueur."*
C18 asked for the sentence to go, not to be replaced. The new list
names three readers and not the Cadreur. Question: does the new
`cadreur.md` read `CURRENT_TECHNICAL_STATE.md`? If it does, the list
is wrong; if it does not, the old sentence was the wrong one and this
is a correction nobody wrote down.

**B-2 — L119-122, the ricochet exclusion.** NOTE.
New: *"Where you look for it: in what you touched — your symbols, the
files you edited. Grep each of them in the document. An entry made
false elsewhere, by ricochet, is not yours to find — you cannot grep
what you do not know your lot reached."*
No comment asks for a bound on the "made false" duty. C6 asks for a
grep by the sheet's modified symbols; this paragraph adds a second
grep (by files edited) and a rule that excuses what neither grep
reaches. It changes what "What your lot made false disappears" (L116)
requires: from every entry the lot made false to those the agent can
reach by name. See D-9 for the two targets.

Everything else in the diff is announced: the role (M1), the reading
list (M1, M2), the "before you stop" block (M3), the redecoupage rows
and paragraph (C15), the "filled decision" heading (C2), the rename
paragraph (C2), the FAIL rows (C11), the move 1 concepteur lines (M1,
C8), the move 3 grep (C6), move 5 (M1, C5), the stalling table (M4),
moves 8-9 (C4), the whitelist (C1).

---

## C. GESTURES AGAINST TOOLS

Frontmatter L4: `Read, Grep, Glob, Edit, Write, Bash, Skill, Agent`.

| Gesture | Where | Tool | Has it |
|---|---|---|---|
| Read the sheet, conventions, `conception.md`, `tests.md`, state document, code, blocking files, reprise, verdict, previous report | L64-78, L421-431, L441-450, L479 | Read | yes |
| Grep symbols in the code folders; grep the state document by symbol | L502-507, L516-517, L120, L480 | Grep | yes |
| Look for `blocked_realisateur-NN.md` files, `reprise_realisateur.md`; "use Grep and Glob" | L421-424, L441, L577 | Glob | yes |
| Fill the bodies; edit the state document; amend the report; add a second entry to the blocking file | L529, L107, L479, L226-228 | Edit | yes |
| Write `compte-rendu.md`, `blocked_realisateur.md`, `reprise_realisateur.md`, `architecte/realisateur-<lot>.md`, "create the folder" | L565, L201, L312, L352-353 | Write | yes (folder creation assumed of Write) |
| `git add`, `commit`, `status`, `git mv`, `git restore`, analysis and test commands | L570-572 | Bash | yes |
| Rename a blocking or reprise file | L276, L301, L430, L449, L463 | Bash `git mv` | yes — since C1 |
| Drop what you wrote | L288, L277 | Bash `git restore` | **partly** — `git restore` puts tracked files back; it does not remove an untracked file the agent created. The role says the agent creates no declaration, so new files should be rare — but a report or a request file written during the run before the drop is untracked, and L304 asks for a report on this very branch. NOTE |
| Delete a file | — | — | no gesture asks it any more (C2). The never-do L387-389 and the whitelist L570 agree on that |
| Load `technical-state-format` | L109 | Skill | yes |
| Invoke `arbitre` and wait | L255-266 | Agent | yes |
| Compare two test outputs to see whether the error moved | L551-553 | Bash output | yes |

**A tool no gesture uses**: none. Glob is used only implicitly ("look
for", L421; "use Grep and Glob", L577) — enough.

**A gesture with no tool**: none outright. Two seams:

- **C-1** — L387-389 never-do names a four-item whitelist; L570-572
  names six. An agent obeying the shorter one cannot run `git mv`
  (L463 "by `git mv`") nor `git restore`. TO FIX (same as C1).
- **C-2** — L288 "Drop what you wrote" + L301 "Rename the blocking
  file" + L304 "Say in your report" on the back-to-split branch, and
  L401 "never leave a dirty working tree": the rename is a staged
  change, the report an untracked file, and the branch says "commit
  nothing". The tree is dirty by construction on this branch. This is
  C3's territory (deferred), but the C15 rewrite made the branch more
  explicit without touching it. Question rather than verdict: what does
  the command do with a worktree left in this state?

---

## D. INTERNAL COHERENCE

**D-1 — L3, frontmatter description.** BLOCKING.
> *"to write the code and the tests a spec sheet calls for … Writes one test per acceptance criterion."*
Against L24 *"You never touch a test"* and L28 *"Nor do you name a
symbol or write a declaration"*. The description is the one line every
other agent, the orchestrator and the command see when they choose or
invoke this agent; it states the role modification 1 removed.

**D-2 — L479, FAIL mineur row.** BLOCKING.
> *"but the run ends as any other: moves 6 to 8, then the report."*
Under L489 *"The nine moves"*, move 8 is the report (L565) and move 9
the commit (L568). The row ends at the report and never reaches the
commit — C11's justification was that an uncommitted fix is not
merged. "then the report" after "moves 6 to 8" also names the report
twice. Should read moves 6 to 9.

**D-3 — L52-53, L131, L204, L380, L381.** TO FIX.
> L52 *"You write the code, the tests, and `code/<lot>/compte-rendu.md`."*
> L131 *"The code and the tests, then `code/<lot>/compte-rendu.md`"*
> L204 *"A test to adapt, a convention to propose: those go in the normal output."*
> L380 *"Write a test matching no criterion"* · L381 *"Delete a test — adapt it"*
Five rules that assume the agent writes or adapts tests, against L24-26
and L532-535 (*"a test you would have to change to make it pass is a
block"*). L204 and L381 tell it to adapt what L24 forbids it to touch.

**D-4 — L387-389 vs L570-572.** TO FIX.
Two whitelists of different length for one `Bash` (see C-1).

**D-5 — L563, move 7.** TO FIX.
> *"Update the technical state — see below."*
Nothing below concerns the technical state; the section is at
L105-125, above. Dangling reference C6 named and that survived.

**D-6 — L464.** TO FIX.
> *"to `blocked_<agent>-NN.md`"*
Placeholder; every other occurrence (L276, L301, L422, L430) says
`blocked_realisateur-NN.md`. A literal reading writes a file named
`blocked_<agent>-01.md`.

**D-7 — L491-493 vs L498-500.** TO FIX.
> L491-493 *"The sheet says what to write, the conventions say where — the Détailleur does not decide the location."*
> L500 *"a conventions request, and you carry on where the sheet points."*
Two lines apart, the sheet does not say where, then the agent carries
on where the sheet points. If the fallback location is neither the
conventions' nor the concepteur's nor the sheet's, the branch leads
nowhere — the agent invents a location, which is what C8 was written
against.

**D-8 — L431 vs L291-295.** TO FIX.
> L431 *"A `## Decision` sending the lot back to the split → Stop"*
> L293-295 *"A decision you read as back to the split without that file is a decision you misread."*
The Part 2 row still tests the wording; the Part 1 paragraph forbids
that reading. Same test, two definitions.

**D-9 — L119-122 vs L516-520.** NOTE / question.
> L119-120 *"in what you touched — your symbols, the files you edited. Grep each of them in the document."*
> L516-517 *"grep that document for every symbol the sheet lists as modified."*
Two grep targets for the entries the lot makes false: files edited
(at update time) and the sheet's modified symbols (at move 3). Neither
mentions the other. Are they meant as two passes, or is one stale?

**D-10 — L190-192, L482-483 vs L204.** TO FIX.
> L190-192 *"stop and report"* · L482-483 *"stop and report rather than coding against it"* · L204 *"Blocking is not reporting."*
"Report" in two senses at two of the three block triggers (C5's
residue). Since move 5 now spells the block out (L538), the two
remaining "stop and report" read as the lighter path by contrast.

**D-11 — L226-228 vs L233-249.** Question.
> L226-228 *"A second lack … is added to the blocking file — it never replaces the first. One entry each, and the Arbitre answers both."*
> L233 *"Its shape — four headings, the last one left empty"* · L237 *"the fact, in one sentence"*
The shape has one `## What blocks` holding one sentence and one
`## Decision`. What does "one entry each" look like — two `## What
blocks`, two `## Decision`, or two sentences under one heading? The
Arbitre and the Product Owner fill `## Decision` by hand; the file does
not say where the second answer goes.

**D-12 — L90 vs L66-71.** TO FIX (M2's own criterion).
> L90 *"Apply `docs/TECHNICAL_CONVENTIONS.md` to everything you write."*
> L66-67 *"the rules marked `permanente`, whole, and those the sheet's `## Conventions` names."*
"Apply the file" reads as apply the whole; the reading rule opens part
of it. The demand for modification 2 names this sentence as the
contradiction that disappears.

**D-13 — L173-174 and L177-178.** NOTE.
> *"Absent by construction: any rationale for a choice — it is in the sheet, not to repeat."*
> *"No rationale for a choice: it is in the sheet, not to repeat."*
Same rule twice, four lines apart (C18 residue).

**D-14 — L429, cross-reference.** NOTE.
> *"Call the Arbitre on it, as *When you cannot produce* says"*
The section *When you cannot produce* (L199) writes the file; the
Arbitre call is in the next section, *Then call the Arbitre, and wait*
(L253). The pointer lands one section early.

**D-15 — L190-191, stale example.** NOTE.
> *"A signature that will not compile, a type that does not exist"*
The concepteur declared the signatures and its file compiles (L28-29).
A non-compiling signature is now caught one agent upstream; the
example describes a case the new chain does not deliver to this agent.

**D-16 — L310-340, the empty-decision branch.** Question.
The branch writes the reprise, commits what compiles, and stops. It
does not say whether moves 7 (state) and 8 (report) run. L230 *"Say in
your report what you did write"* implies a report exists on a block;
L565 makes the report move 8, after move 6 passes — which on this
branch it has not. Does a blocked run write `compte-rendu.md`, and what
goes in `## Build`?

**D-17 — L489 count.** Checked: nine numbered moves, L491-568. Matches.

**D-18 — L546.** NOTE.
> *"a screen and its provider"*
Framework word C18 asked to neutralise; kept.

---

## Summary

| Severity | Count | Items |
|---|---|---|
| BLOCKING | 2 | D-1 (description says it writes the tests), D-2 (FAIL mineur stops before the commit) |
| TO FIX | 11 | C1/D-4, C4 (report field), C5/D-10, C6/D-5, C8/D-7, C15/D-8, D-3, D-6, D-12, M2 |
| NOTE | 7 | C10, C18/D-13/D-18, B-1, B-2/D-9, C-2, D-14, D-15 |
| Question | 4 | C7 (which sections are `permanente`), D-9, D-11, D-16 |

The pass sheet's "Passés (11)" holds for three comments as written;
seven are half-applied, and one (C8) was applied the other way round.
