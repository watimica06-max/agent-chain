# Plan — `testeur.md`

Built against `.claude-new/agents/testeur.md` (292 lines), the two
commands that name it (`8_code.md`, `9_controle.md`), its report
`docs/verification2/testeur.md`, `decisions.md`, and the six thematic
reports filtered on `testeur`. Every two-file `Where` was opened on both
sides; the quoted line is given under `Cited`.

None of the fourteen settled questions in `decisions.md` bears on this
agent.

Twenty-one findings judged: the fourteen of `testeur.md`, plus
`renommages.md` F02, `chemins-aval.md` F06, F08, F09, and
`passages-aval.md` F01, F06, F12. All twenty-one are `confirmed` — no
line in the current files shows any of them already fixed or false.
Several are one defect seen from several files; the entries say which
ones merge.

---

## `testeur.md` — the agent's own report

### testeur.md F01 — the index says an older failing test is always a block

Verdict: confirmed
Decision: Bring the index row in line with the file — an older test that fails on a signature the sheet declares modified is adapted, and blocks only otherwise.
Where: modifications.md L898 ↔ testeur.md L223-228
Cited: modifications.md L898 — "**Quand un ancien échoue** | 🔴 **C'est un blocage** — le Concepteur a cassé quelque chose"
Owner: the index, `docs/refonte/modifications.md` — no agent file changes; the file's rule (D.3, fixed) is the one to keep
Also in: —

### testeur.md F02 — the index says a passing new test is always rewritten

Verdict: confirmed
Decision: Bring the index row in line with the file — a new test that passes is rewritten when it calls a body, and left green when it asserts a declaration alone.
Where: modifications.md L897 ↔ testeur.md L216-221
Cited: modifications.md L897 — "**Quand l'un des siens passe** | 🔴 **Il le réécrit** — ⚠️ **il n'affirme rien, ou affirme ce qu'un corps vide satisfait déjà**"
Owner: the index, `docs/refonte/modifications.md` — no agent file changes
Also in: —

### testeur.md F03 — no test command when the conventions name none

Verdict: confirmed — L92-93 admits "the test command the conventions name" and nothing else; L206-207 says "The conventions name none → say so in your report and use what they give", and when none is named there is nothing they give. The concepteur (L218-219) and the realisateur (L426-427) carry the same hole.
Decision: Name what move 4 runs when the conventions name no test command — one fallback, the same one the concepteur and the realisateur take — and admit it in the `Bash` bound, so that the red check can run on a project whose conventions are not yet derived.
Where: testeur.md L205-207 ↔ testeur.md L92-96
Owner: testeur
Follows: concepteur (L212-221), realisateur (L423-427, L586) — the same fallback, or the three run three commands
Also in: concepteur.md, realisateur.md

### testeur.md F04 — move 2 has no branch ending in a block

Verdict: confirmed — L182-185 gives move 2 two outcomes, test or manual list; L187-189 defines *no* as "cannot be observed from outside the running code"; L138-140 makes the internal criterion ("the value is cached") a block; L145-147 says the manual list is for what the Product Owner can see. The same criterion is routed to two places, and the block has no branch.
Decision: Give move 2 a third branch — a criterion nobody can observe, neither a test nor the Product Owner on the device, is a block — and define *no* so that it sends to the manual list only what the Product Owner can see.
Where: testeur.md L182-189 ↔ testeur.md L136-147
Owner: testeur
Also in: —

### testeur.md F05 — "two things block you" counts three

Verdict: confirmed — L136 says two, L138 and L142 give two, L104-105 already made "a signature you cannot test against" a block, and the `## Where` template at L159-162 fits a criterion or a failing test, not a declaration.
Decision: Count every block the file names — the untestable signature of L105 included, and the removed behaviour that F14 turns into one — and give the blocking file's `## Where` a wording for each.
Where: testeur.md L136-143 ↔ testeur.md L104-105, L159-162
Owner: testeur
Also in: —

### testeur.md F06 — the absolute rule stands beside its exception

Verdict: confirmed — L23 "Every new test has to fail", L280 "that every new test failed, and every older one passed", against L221 "Leave it green — the criterion is met by the declaration".
Decision: State the declaration-only exception where the absolute is stated, and make `## Red` carry it — the tests that failed, and the ones left green because the declaration alone meets the criterion, named one by one.
Where: testeur.md L23-26, L278-280 ↔ testeur.md L216-221
Owner: testeur — decides the form of `## Red`
Follows: realisateur (L20-22, L77-78), relecteur (L333-334), `8_code.md` (L113) — each takes `## Red` as given and states the absolute; see F11
Also in: realisateur.md, relecteur.md — one decision with F07, F11 and passages-aval F12

### testeur.md F07 — three report outcomes and no heading to receive them

Verdict: confirmed — "say so in your report" at L207, L221 and L232-233; the template at L270-284 has `## Tests`, `## Criteria with no test`, `## Red`, `## Outside the lot` and nothing that fits any of the three.
Decision: Give each outcome a named place in `tests.md` — the command move 4 ran when the conventions name none, and the tests left green, both under `## Red`; the criterion gone with its behaviour goes where F14 sends it, a blocking file, and no longer into the report.
Where: testeur.md L205-207, L216-221, L230-233 ↔ testeur.md L270-284
Owner: testeur
Follows: realisateur (L77-78), relecteur (L58-59, L333-341) — the readers of `tests.md` have new lines to read
Also in: realisateur.md, relecteur.md — one decision with F06, F11 and passages-aval F12

### testeur.md F08 — a blocked run writes no `tests.md`, and the resume reads one

Verdict: confirmed — L119-123 writes the blocking file and commits "the tests you did write, the blocking file with them"; L132-134 reads "a `code/<lot>/tests.md` already there" as the trace of a blocked run and resumes from its `## Tests`. Nothing between the two writes the report. The concepteur carries the same pair (L125-128 ↔ L162-165).
Decision: Have the blocking procedure write `tests.md` — `## Tests` for the criteria covered, `## Red` for what was run — before the commit, so that the resume rule has something to read; with F10, so that the run resumes at all.
Where: testeur.md L119-123 ↔ testeur.md L132-134
Owner: testeur
Also in: concepteur.md — same defect, same shape

### testeur.md F09 — adapting an older test means reading it

Verdict: confirmed — L84-86 forbids taking another lot's tests as input and excepts "opening the file to add yours"; L227 and L230-233 adapt an older test so that "it keeps its assertion", which cannot be done without reading what it asserts.
Decision: Extend the L86 exception to move 4 — an older test the lot's sheet made false is read to be adapted; what it asserts stays its own criterion, never the testeur's.
Where: testeur.md L84-86 ↔ testeur.md L227, L230-233
Owner: testeur
Also in: —

### testeur.md F10 — the command skips the testeur before the decision is applied

Verdict: confirmed — 8_code.md L113 skips the testeur "when `code/<lot>/tests.md` is there", unconditionally; 4b at L164-170 names a filled `blocked_testeur.md` in the prompt; L436-439 says a filled decision means invoking the agent it names "even on a lot already carrying a PASS". The skip row contradicts the two others and is the one a reader meets first; the resume rule at testeur L132 can only fire against it.
Decision: Make the L113 skip yield to a filled `blocked_testeur.md` — present, the testeur runs and resumes from `tests.md`; the skip row says it, not only the general rule at L436.
Where: testeur.md L132-134 ↔ 8_code.md L113, L164-170, L436-439
Cited: 8_code.md L113 — "📌 **skipped when `code/<lot>/tests.md` is there**"; 8_code.md L436-437 — "📌 **A filled `## Decision` is not a stop** — invoke the agent it names on the lot it names, and let it apply the decision."
Owner: `8_code.md` — the command writes the skip
Follows: testeur (L132-134 — say that a filled decision is what brings it back onto a lot that has a `tests.md`)
Also in: concepteur.md — chemins-aval F06 and passages-aval F06 carry the same pair for `conception.md` (8_code L112 ↔ concepteur L162-165)

### testeur.md F11 — downstream readers take a guarantee the testeur does not give

Verdict: confirmed
Decision: Have every reader of `## Red` state the exception the testeur carries — a declaration-only test may be green, and `## Red` names it — in place of the absolute it states now.
Where: testeur.md L216-221 ↔ realisateur.md L20-22, L77-78; relecteur.md L333-334; 8_code.md L113
Cited: realisateur.md L20-22 — "The testeur wrote one per acceptance criterion, ran them, and every one of them failed"; relecteur.md L333-334 — "the testeur wrote one per criterion and checked each one failed red"; 8_code.md L113 — "Writes one test per criterion, and checks each fails red"
Owner: testeur — the form of `## Red` (F06) is what the readers key on
Follows: realisateur, relecteur, `8_code.md`
Also in: realisateur.md, relecteur.md — one decision with F06, F07 and passages-aval F12

### testeur.md F12 — `## Files` is a dash on a lot that creates everything

Verdict: confirmed
Decision: `## Files` names the test file the lot's tests go in, whether the lot creates it or opens it — never a dash where the testeur has tests to place; L58 then stays as it is, and L282-284 stops catching the lot's own test file.
Where: testeur.md L58-59, L282-284 ↔ detailleur.md L259-265
Cited: detailleur.md L265 — "📌 **A dash when the lot creates everything it touches.**"
Owner: detailleur — writes the field; with the cadreur for its source (`Touches`, cadreur L753-758)
Follows: testeur, concepteur (L186-187), realisateur (L189-191), relecteur (L386-392) — every `## Outside the lot` keys on the field
Also in: detailleur.md, cadreur.md, concepteur.md, realisateur.md, relecteur.md — one decision with renommages F02 and passages-aval F01

### testeur.md F13 — a false reason for committing

Verdict: confirmed — testeur L258-259 says the tests are destroyed because "the realisateur runs `git restore`"; the realisateur restores "the files you edited" (L335-336), never writes a test (L455) and never touches one (L574). An uncommitted test file is not among them.
Decision: Replace the reason with the true one — uncommitted, the tests are never merged and the worktree is removed at the end of the run — and drop the `git restore` cause.
Where: testeur.md L258-260 ↔ realisateur.md L335-338
Cited: realisateur.md L335-336 — "🔴 **Drop what you wrote** — 📌 **`git restore` on the files you edited.**"
Owner: testeur
Also in: —

### testeur.md F14 — a removed behaviour reaches nobody

Verdict: confirmed — testeur L232-233 "say so in your report: only the Product Owner removes a behaviour"; 8_code.md relays "which lots passed, and where the run stopped. Nothing else" (L481-482), and the one agent line it relays is the concepteur's `## Placements` (L112). `/9_controle` phase 5 gathers blocking files and the control report, never a report line.
Decision: Make it a block — a criterion whose behaviour the lot's sheet removes is a decision only the Product Owner takes, and a blocking file is the one route that stops the lot, reaches her through `8_code`'s relay, and lands in the register at `/9_controle` phase 5; the report line at L233 goes.
Where: testeur.md L230-233 ↔ 8_code.md L112-113, L479-488
Cited: 8_code.md L481-482 — "**Which lots passed, and where the run stopped.** 🔴 **Nothing else is yours**"; 8_code.md L488 — "**If an agent returns a `blocked_*.md`**: relay it and stop."
Owner: testeur — the block joins the count at F05
Follows: `8_code.md` — nothing to add, a block is already relayed (L488)
Note: the alternative, a relay row in `8_code` like the concepteur's `## Placements`, keeps the lot running but leaves the removal outside the register; it costs less per run and loses the trace, and the corpus's own rule (CLAUDE.md, "the agent that hit the ambiguity documents it in `blocked.md` and stops") settles it for the block.
Also in: —

---

## The thematic reports

### renommages.md F02 — `## Files` reads as a dash on a lot of new files

Verdict: confirmed
Decision: Same as testeur.md F12 — `## Files` names every file the lot creates as well as those it opens, the test file included, so that neither the concepteur nor the testeur nor the realisateur reports the lot's own files under `## Outside the lot`.
Where: detailleur.md L259-265 ↔ concepteur.md L186-187; testeur.md L58-59
Cited: concepteur.md L186-187 — "📌 **The sheet's `## Files` narrows it** — 🔴 **a symbol goes in one of those files**"; detailleur.md L265 — "📌 **A dash when the lot creates everything it touches.**"
Owner: detailleur
Follows: concepteur, testeur, realisateur, relecteur
Also in: detailleur.md, cadreur.md, concepteur.md, realisateur.md, relecteur.md

### chemins-aval.md F06 — the skip fires before the decision is applied

Verdict: confirmed — the finding names the concepteur pair and says "the same pair holds for the Testeur (L113 ↔ testeur.md L132)"; both hold as read.
Decision: Same as testeur.md F10 — the skip at 8_code L112 and L113 yields to a filled `blocked_<agent>.md`.
Where: 8_code.md L112-113, L164-170 ↔ concepteur.md L162-165; testeur.md L132-134
Cited: concepteur.md L162-163 — "🔴 **A `code/<lot>/conception.md` already there is a run of yours that blocked**"; testeur.md L132-133 — "🔴 **A `code/<lot>/tests.md` already there is a run of yours that blocked**"
Owner: `8_code.md`
Follows: concepteur, testeur
Also in: concepteur.md

### chemins-aval.md F08 — the dropped lot's declarations and red tests stay in the tree

Verdict: confirmed — realisateur L335-338 restores "the files you edited" and states that the declarations and the tests are committed; 8_code L357-365 commits and runs `/7_lots` with nothing removed; the next testeur runs the suite on the module (L205-206) and blocks at L228 on any older test that fails for a reason the sheet does not sanction. "Every lot after" holds for every lot in the module the dropped tests sit in — the re-cut lots of the same block — and the realisateur's move 6 (L586) fails on the same red tests.
Decision: Have the orchestration remove the dropped lot's commits from the tree — declarations, tests, `conception.md`, `tests.md` — before `/7_lots` runs, since no agent of the loop has a tool that removes a file or a commit; the realisateur's paragraph then says the rest is the orchestration's, and the testeur's L228 keeps its rule.
Where: testeur.md L119-123, L223-228 ↔ realisateur.md L335-338; 8_code.md L357-365
Cited: realisateur.md L336-338 — "⚠️ **Nothing you wrote is a new file**: the concepteur committed the declarations, the testeur the tests, and your work is bodies inside files that are already tracked."
Owner: `8_code.md` — *When the split comes back*
Follows: realisateur (L335-338), concepteur (L125-128), testeur (L119-123, L255-260 — the reason for committing does not change; what happens to the commits on a return to the split does)
Also in: realisateur.md, concepteur.md

### chemins-aval.md F09 — `conception.md` and `tests.md` survive a redécoupage

Verdict: confirmed — 8_code L379-382 deletes `code/<lot>/fiche-executable.md` for every lot with no PASS and nothing else; L112-113 skip the two agents on the presence of those files.
Decision: Delete `conception.md` and `tests.md` with the sheet, for every lot with no PASS — for the dropped lot this is what F08's removal of its commits already does; the rule at L379-382 names the three files.
Where: 8_code.md L379-382 ↔ 8_code.md L112-113
Cited: 8_code.md L379-381 — "🔴 **The sheets of every lot that is not coded are stale** … 📌 **Delete them**, in `code/<lot>/fiche-executable.md`"
Owner: `8_code.md`
Follows: concepteur, testeur — nothing to rewrite; their resume rules (L162, L132) read a file that is now gone after a redécoupage, which is the intended state
Also in: concepteur.md

### passages-aval.md F01 — `## Files` is built from a field that carries no file

Verdict: confirmed — cadreur L753-754 makes `Modifies` carry "symbols, and symbols only … never a file"; detailleur L259-262 builds `## Files` from "the lot's `Modifies` and `Touches`"; on a lot that produces and touches nothing it is a dash (L265), and the three `## Outside the lot` fields (concepteur L259, testeur L282-284, realisateur L189-191) then catch every file the lot creates.
Decision: Build `## Files` from the files the lot's symbols live in and the files it touches or creates — never from `Modifies` as a list of files — so that it names the test file; on the testeur's side nothing beyond F12.
Where: detailleur.md L259-265 ↔ cadreur.md L753-754; testeur.md L58-59, L282-284
Cited: cadreur.md L753-754 — "🔴 **`Needs`, `Produces` and `Modifies` carry symbols, and symbols only.** 📌 **A name the code carries** — ⚠️ **never a file.**"; detailleur.md L259-260 — "🔴 **`## Files` carries the lot's `Modifies` and `Touches`, copied from `code/decoupage.md`**"
Owner: detailleur — with the cadreur for the source field
Follows: concepteur, testeur, realisateur, relecteur
Also in: detailleur.md, cadreur.md, concepteur.md, realisateur.md, relecteur.md — one decision with testeur.md F12 and renommages F02

### passages-aval.md F06 — the loop skips a blocked agent's resume

Verdict: confirmed — same pair as testeur.md F10 and chemins-aval F06.
Decision: Same as testeur.md F10.
Where: 8_code.md L112-113 ↔ concepteur.md L162-165; testeur.md L132-134
Cited: see chemins-aval F06 above — the same lines
Owner: `8_code.md`
Follows: concepteur, testeur
Also in: concepteur.md

### passages-aval.md F12 — the exception to `## Red` has no field and no reader

Verdict: confirmed
Decision: Same as testeur.md F06, F07 and F11 — `## Red` names the tests left green because the declaration alone meets the criterion, and its two readers state that exception; the criterion gone with its behaviour becomes a block (F14) and leaves the report.
Where: testeur.md L221, L232-233 ↔ testeur.md L278-280; realisateur.md L76-78; relecteur.md L333-334
Cited: realisateur.md L77-78 — "**`code/<lot>/tests.md`** — 🔴 **its `## Red` line**: the tests were red when they were written"; relecteur.md L333-334 — "the testeur wrote one per criterion and checked each one failed red"
Owner: testeur
Follows: realisateur, relecteur
Also in: realisateur.md, relecteur.md

---

## What merges

Four decisions cover the twenty-one findings on the testeur's side:

| Decision | Findings |
|---|---|
| The shape of `## Red` and the places in `tests.md` | testeur F06, F07, F11; passages-aval F12 |
| A blocked run writes `tests.md`, and the command's skip yields to a filled block | testeur F08, F10; chemins-aval F06; passages-aval F06 |
| `## Files` names the lot's files, the test file included | testeur F12; renommages F02; passages-aval F01 |
| A return to the split removes the dropped lot's commits and reports | chemins-aval F08, F09 |

The rest — F01, F02 (the index), F03 (the test command), F04 and F05
(the blocks), F09 (reading an older test), F13 (the commit reason),
F14 (the removed behaviour) — stand alone.

---

## To settle

Nothing. No finding on this agent turns on intent, scope or
user-facing behaviour. F14 is the one that came close — the route a
removed behaviour takes to the Product Owner — and its entry says why
the corpus's own rule settles it for the block, and what the relay
would have cost instead.
