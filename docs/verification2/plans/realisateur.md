# realisateur — correction plan

Built against `.claude-new/agents/realisateur.md` (612 lines), the four
commands that name it (`8_code.md`; `cycle.md` L82, `audit_blocages.md`
L152-153 and `audit_conventions.md` L167 only carry a file name as an
example), `docs/verification2/realisateur.md` (both parts),
`docs/verification2/decisions.md`, the six thematic reports filtered on
`realisateur`, and — for the cited other side — `detailleur.md`,
`arbitre.md`, `testeur.md`, `relecteur.md`, `concepteur.md`,
`cadreur.md`, `architecte.md`, `docs/refonte/modifications.md` and
`docs/refonte/passes/realisateur.md`.

Line numbers are those of the files as they stand today.

---

## Verdicts

| Finding | Verdict | Where it lands |
|---|---|---|
| realisateur F01 | confirmed | Index — entry below |
| realisateur F02 | confirmed | Entry below |
| realisateur F03 | confirmed | Entry below, with F15 |
| realisateur F04 | confirmed | Entry below, with F22 |
| realisateur F05 | confirmed | Index — entry below |
| realisateur F06 | confirmed | Index — entry below |
| realisateur F07 | confirmed | Index — entry below |
| realisateur F08 | confirmed | Entry below |
| realisateur F09 | confirmed | Entry below, with renommages F05, renommages F06, passages-aval F13 |
| realisateur F10 | confirmed | Entry below |
| realisateur F11 | confirmed | `## To settle` |
| realisateur F12 | confirmed | Entry below |
| realisateur F13 | confirmed | Entry below, with fichiers F15, chemins-aval F07, passages-aval F09 |
| realisateur F14 | confirmed | Entry below |
| realisateur F15 | confirmed | Entry below, with F03 |
| realisateur F16 | confirmed | Entry below, with chemins-aval F25 |
| realisateur F17 | confirmed | Entry below |
| realisateur F18 | confirmed | Entry below, with renommages F03 |
| realisateur F19 | confirmed | Entry below |
| realisateur F20 | confirmed | Entry below |
| realisateur F21 | confirmed | Entry below |
| realisateur F22 | confirmed | Entry below, with F04 |
| realisateur F23 | confirmed | Entry below |
| realisateur F24 | confirmed | Entry below |
| realisateur F25 | confirmed | Entry below |
| realisateur F26 | confirmed | Entry below |
| renommages F02 · passages-aval F01 | confirmed | Entry below |
| renommages F03 | confirmed | Entry below, with F18 |
| renommages F04 | confirmed | Entry below |
| renommages F05 · F06 · passages-aval F13 | confirmed | Entry below, with F09 |
| renommages F08 | confirmed | Entry below |
| renommages F09 | confirmed | Entry below |
| renommages F16 | settled | `decisions.md` — no line of this agent changes; see *Settled elsewhere* |
| fichiers F15 | confirmed | Entry below, with F13 |
| chemins-aval F03 · passages-aval F02 | confirmed | Entry below |
| chemins-aval F07 | confirmed | Entry below, with F13 |
| chemins-aval F08 | confirmed | `## To settle` |
| chemins-aval F09 | confirmed | Entry below |
| chemins-aval F10 | confirmed | Entry below |
| chemins-aval F21 | confirmed | Entry below |
| chemins-aval F23 | confirmed | Entry below |
| chemins-aval F25 | confirmed | Entry below, with F16 |
| passages-aval F09 | confirmed | Entry below, with F13 |
| passages-aval F12 | confirmed | Entry below |

No `stale`, no `wrong`, no `overstated`: every fact was read at the
line the report names, and none is contradicted by a later line of the
file. The index findings (F01, F05, F06, F07) hold against the index as
it stands at `docs/refonte/modifications.md` L1082-1121.

---

## Entries — the agent file

### realisateur F02 — a verdict judged wrong still "stops and reports"

Verdict: confirmed
Decision: Make the third trigger a block like the two others — the agent writes `blocked_realisateur.md` and calls the Arbitre on a verdict it judges wrong, and the never-do line *"Argue with a verdict — fix, or stop"* says *block* where it says *stop*.
Where: realisateur.md L524-525 ↔ realisateur.md L229-232, L457
Cited: realisateur.md L229-232 — "**Blocking is not reporting.** … 🔴 **You block on a wrong sheet**, on a regression outside the lot, or on a verdict you judge wrong."
Cited: realisateur.md L524-525 — "You do not argue with a verdict. If you judge it wrong, stop and report rather than coding against it."
Owner: realisateur
Also in: —

### realisateur F03 · F15 — a missing convention on how the code is written has no branch

Verdict: confirmed
Decision: Add the missing-convention trigger to the block list — a rule the code needs and the conventions do not carry (which layer owns a symbol, what a kind of symbol is built on) is a mid-lot block the Arbitre settles through the Architecte — and state the boundary with the end-of-lot request by effect on the code: what changes the code you write is a block, what only the verification needed is a request.
Where: realisateur.md L229-232, L398-402 ↔ docs/refonte/passes/realisateur.md C8, arbitre.md L406-410
Cited: passes/realisateur.md C8 "Ce qu'il faut" — "a missing convention that decides how the lot is written — where a symbol lives, which layer owns it — is a block, settled mid-lot through the Arbitre; the end-of-lot request stays for what only the verification needed. The boundary between the two is stated by effect on the code, not by example."
Cited: arbitre.md L406-407 — "🔴 **Ask the Architecte for it — once.** **Write `architecte/arbitre-<lot>.md`** in the working folder"
Cited: realisateur.md L398-402 — "🔴 **A condition of running that nothing states.** An environment variable, a service that has to be up, a device that has to be attached, an order the commands have to follow"
Note: the placement half of C8 landed (L533-539 blocks on an unplaced declaration); the *how the code is written* half and the boundary did not. The block file's `## What blocks` names the rule that is missing; the Arbitre's own route to the Architecte does the rest.
Owner: realisateur
Also in: arbitre (no change needed — its route exists at L406-410)

### realisateur F04 · F22 — "a criterion no test can be made to read" routes a Testeur case to the Arbitre

Verdict: confirmed
Decision: Remove *"a criterion no test can be made to read"* from the wrong-sheet triggers — a criterion the Testeur could not reach is already in `tests.md` `## Criteria with no test` and on the manual list, and the only test-shaped block left is the one at L575-578: a test the agent would have to change to pass.
Where: realisateur.md L215-216 ↔ testeur.md L274-276, relecteur.md L340-342, modifications.md L1103
Cited: testeur.md L274-276 — "## Criteria with no test / <one line each, with why no test can reach it — or a dash>"
Cited: relecteur.md L340-342 — "🔴 **A criterion in `## Criteria with no test` of `tests.md` is not a gap** — 📌 **the testeur could not reach it, and it went to the manual list.**"
Cited: modifications.md L1103 — C9 "🔴 **Caduc avec A3** — 📌 **c'est le Testeur qui décide qu'un critère n'est pas testable**, et il le porte à la recette"
Owner: realisateur
Also in: —

### realisateur F08 — three bounded reads name no way to locate what they bound

Verdict: confirmed
Decision: Say how each bounded read is located — the `permanente` rules by a `Grep` on the marker at the end of the line, the `§n` rules the sheet names by a `Grep` on their number, and the two sections of the state document by a `Grep` on their headings followed by a `Read` with offset and limit — so that the L452 prohibition on reading the state document whole can be obeyed.
Where: realisateur.md L66-70, L97-98, L551-552, L452-453 ↔ architecte.md L140
Cited: architecte.md L140 — "🔴 **`permanente` or `spécifique`, at the end of the line.**"
Cited: realisateur.md L452-453 — "🔴 **Read `CURRENT_TECHNICAL_STATE.md` whole** — two sections, then greps by symbol"
Note: only the state document carries a prohibition; L66-70 bound what to hold, not what to open. The decision fixes the three reads together because the same `Grep`-then-`Read` gesture serves all of them.
Owner: realisateur
Also in: detailleur, concepteur, testeur (same reads of the same two files — same gesture)

### realisateur F09 · renommages F05 · renommages F06 · passages-aval F13 — the blocking file has two shapes on one page, and a third at the Arbitre

Verdict: confirmed
Decision: Keep one shape — `## Blocking N` per stop, `###` for its three headings, a single `## Decision` at the end, even when there is one stop — delete the second block *"The headings of an entry"* at L272-288, and have the Arbitre drop its single-entry `##` row so that the shape it expects is the one both writers produce.
Where: realisateur.md L258-270 ↔ realisateur.md L272-288, arbitre.md L129-130, detailleur.md L289-292
Cited: realisateur.md L258-259 — "🔴 **one `## Blocking N` per stop**, even when there is only one, and 🔴 **one `## Decision` at the end**, whatever the count."
Cited: realisateur.md L272-288 — "**The headings of an entry:** / ## What blocks / … / ## Decision / <left empty>"
Cited: arbitre.md L129-130 — "🔴 **`##` in a single-entry file, `###` under each `## Blocking N` in a multi-entry one.**"
Cited: detailleur.md L289-290 — "🔴 **one `## Blocking N` per stop**, even when there is only one, and 🔴 **one `## Decision` at the end**, whatever the count."
Owner: realisateur for its own duplicate; arbitre for L129-130
Follows: detailleur (already on the single shape — no change)
Also in: arbitre, detailleur

### realisateur F10 — "some numbers answered, others not" leads nowhere

Verdict: confirmed
Decision: Define a `## Decision` with a number absent as an empty decision for that entry — the agent applies the answered numbers, carries on with what they unlock, and when nothing is left writes the reprise and stops as on an empty decision — and make *Filled* in both tables (L315, L505) mean *every number answered*, so that the next run and the orchestration's move 4b never read a half-answered file as settled.
Where: realisateur.md L317 ↔ realisateur.md L362-364, L505; arbitre.md L165-166; 8_code.md L169-170
Cited: arbitre.md L165-166 — "⚠️ **A number with no answer is an entry still waiting** — 📌 **that is how a product question holds up one entry and not the file.**"
Cited: realisateur.md L505 — "| A `## Decision` filled | 📌 **Apply it, and say in your report that you did** — 🔴 **the orchestration renames the file** |"
Cited: 8_code.md L169 — "| **Its `## Decision` is empty** | 🔴 **Stop** — ⚠️ **invoking again re-raises the same block** |"
Owner: realisateur
Follows: 8_code (move 4b keys *empty* on any number absent, not on an empty heading alone)
Also in: detailleur (same two tables at L437-441), commandes

### realisateur F12 — the `## Decision` sentence sits under the reprise shape

Verdict: confirmed
Decision: Move the sentence *"The `## Decision` heading is written empty, and never omitted…"* to the blocking-file section, where that heading exists, and leave the reprise shape without it.
Where: realisateur.md L388-390 ↔ realisateur.md L370-380
Cited: realisateur.md L370-380 — the reprise shape carries `Fait`, `Non fait`, `Bloqué sur`, `En chantier` and no `## Decision`
Owner: realisateur
Also in: —

### realisateur F13 · fichiers F15 · chemins-aval F07 · passages-aval F09 — nobody reads the reprise

Verdict: confirmed
Decision: Add a Part 2 case for the reprise — first thing, with the blocking lookup: when `code/<lot>/reprise_realisateur.md` is there, read it, take `Fait` as done, start at `Non fait`, and treat `En chantier` as `## To settle` below decides — and list the file under *What you read*.
Where: realisateur.md L364-368 ↔ realisateur.md L61-88, L493-511; 8_code.md L134-136, L299
Cited: realisateur.md L366-368 — "⚠️ **A fresh Réalisateur will pick the lot up with your sheet, the blocking file once the Product Owner has filled it, and this file.** 📌 **It has none of your context** — this file is all it gets."
Cited: 8_code.md L134-136 — "📌 **If `code/<lot>/reprise_realisateur.md` is there**, 🔴 **name it in the Réalisateur's prompt**: a run before it got part of the lot done and wrote what it left. ⚠️ **Without it, it starts the lot again.**"
Cited: realisateur.md L495-496 — "🔴 **First thing, every run: look for `code/<lot>/blocked_realisateur.md`.**" — the only lookup Part 2 makes
Owner: realisateur
Follows: 8_code (its prompt line stays; the retirement is F23)
Also in: commandes

### realisateur F14 — the resumed run rewrites `## Symbols` from what it alone coded

Verdict: confirmed
Decision: Have the run that resumes after a reprise read the previous `code/<lot>/compte-rendu.md` and amend it, as the FAIL mineur row already says, never rewrite it from the code.
Where: realisateur.md L320-322 ↔ realisateur.md L366-368, L521
Cited: realisateur.md L320-322 — "📌 **A blocked run writes its report all the same** — 🔴 **`## Build` says the analysis and the tests did not pass**, and the rest says what you did write."
Cited: realisateur.md L521 — "**amend the report** — 📌 **read it, never rewrite it from the code.**"
Owner: realisateur
Also in: —

### realisateur F16 · chemins-aval F25 — the back-to-split branch states two false facts

Verdict: confirmed
Decision: Correct the two facts — the blocking file and `code/redecoupage.md` are new files that stay in the tree and the orchestration commits them before `/7_lots`; and the reason for writing no report is that the lot is about to be cut differently, not that the worktree is about to be removed.
Where: realisateur.md L335-338, L352-355 ↔ realisateur.md L226; 8_code.md L357-358, L365-366
Cited: realisateur.md L336-338 — "⚠️ **Nothing you wrote is a new file**: the concepteur committed the declarations, the testeur the tests, and your work is bodies inside files that are already tracked."
Cited: realisateur.md L352-355 — "🔴 **Write no report either** — 📌 **the worktree is about to be removed and every uncoded sheet deleted**"
Cited: 8_code.md L357-358 — "🔴 **Commit first, inside your worktree** — 📌 **`git add` and `git commit` on everything the lots coded this run.**"
Cited: 8_code.md L365-366 — "**Then run `/7_lots` on this working folder**, and wait for it. ⚠️ **Then carry on your loop**"
Owner: realisateur
Also in: commandes (8_code side unchanged)

### realisateur F17 — "one invocation per lot" is false in words

Verdict: confirmed
Decision: Replace the count with the rule it stands for — one lot per invocation, and a lot may take several invocations (a FAIL, an empty decision).
Where: realisateur.md L31 ↔ realisateur.md L515, L366
Cited: realisateur.md L515 — "**A FAIL brings a fresh Réalisateur**, never the one who wrote the code."
Owner: realisateur
Also in: —

### realisateur F18 · renommages F03 — the greps key on a `Modifies` the sheet does not carry

Verdict: confirmed
Decision: Have the sheet's `## Signatures` mark each symbol *created* or *modified* (the lot list's `Produces` / `Modifies` gives it, and the Détailleur already applies that distinction), key the Réalisateur's state-document grep and its `## Symbols` on that mark, and say `## Files` where L194 says `Modifies`.
Where: realisateur.md L123-125, L194, L555-557 ↔ detailleur.md L224-232, L259-262, L397-398; relecteur.md L317-318; testeur.md L227; cadreur.md L753-754
Cited: detailleur.md L224-232 — the `## Signatures` shape carries a signature and a comment, no *created*/*modified* mark
Cited: detailleur.md L397-398 — "🔴 **Decide whether a symbol is created or modified** — the lot declares it, you apply"
Cited: relecteur.md L317-318 — "the report's `## Symbols` list which says whether each was created or modified"
Cited: testeur.md L227 — "| **A signature the sheet declares modified** | 📌 **Adapt the test to the new signature**"
Cited: cadreur.md L753-754 — "🔴 **`Needs`, `Produces` and `Modifies` carry symbols, and symbols only.** 📌 **A name the code carries** — ⚠️ **never a file.**"
Owner: detailleur (the field)
Follows: realisateur (L123-125, L194, L555-557 key on the mark), testeur (L227 reads it), relecteur (compares the report's mark to the sheet's)
Also in: detailleur, testeur, relecteur

### realisateur F19 — a trap on a consumed symbol is read by nobody

Verdict: confirmed
Decision: Extend the move-3 grep to every symbol of the sheet's `## Dependencies` as well as those marked modified, and have the Arbitre's file say that the Réalisateur reads the two general sections whole and greps its lot's symbols, not that it reads the document whole.
Where: realisateur.md L79-80, L551-557 ↔ arbitre.md L396-398
Cited: arbitre.md L396-398 — "📌 **Why the state document at all**: 🔴 **the Réalisateur reads it whole, always** — *« you cannot grep a rule you do not know applies to you »*"
Cited: realisateur.md L555-556 — "🔴 **Then grep that document for every symbol the sheet lists as modified.**"
Owner: realisateur (its reading rule)
Follows: arbitre (L396-398 states the reader's behaviour)
Also in: arbitre

### realisateur F20 — `## Traps` is not a heading of the state document

Verdict: confirmed
Decision: Name the headings the Arbitre actually writes under — `## Traps — general`, or a subject's own `###`.
Where: realisateur.md L136-137 ↔ arbitre.md L401-403
Cited: arbitre.md L401-403 — "📌 **Where it goes**: 🔴 **`## Traps — general` when several subjects meet it**, 📌 **under the subject's own `###` heading when one owns it.** ⚠️ **`## Traps` alone is not a heading of that file.**"
Owner: realisateur
Also in: —

### realisateur F21 — a fresh run is never told it resumes a FAIL

Verdict: confirmed
Decision: Have the command's retry prompt name the verdict (a `Verdict: code/<lot>/verdict.md` line, on the model of the Détailleur's `Mode:` line), and have Part 2 key its FAIL case on that line, first thing, beside the blocking and reprise lookups.
Where: realisateur.md L50, L513-517, L495 ↔ 8_code.md L138, L295-300
Cited: 8_code.md L138 — "**4.** On FAIL → a **fresh `realisateur`**, with the verdict"
Cited: 8_code.md L295-300 — the only Réalisateur prompt shape: "Working folder: <the working folder>. Your lot: <lot>. <Plus: code/<lot>/reprise_realisateur.md.>"
Cited: 8_code.md L192 — "🔴 **The `Mode:` line is what tells the two apart**" — the precedent for a prompt line that selects a case
Owner: 8_code (the prompt)
Follows: realisateur (Part 2 case keyed on the line; L50 *"only when you resume a FAIL"* says how it knows)
Also in: commandes

### realisateur F23 — nobody archives the reprise

Verdict: confirmed
Decision: Have move 4b of `/8_code` rename `code/<lot>/reprise_realisateur.md` to `reprise_realisateur-NN.md` once the run it was named to has reported, the way it renames the blocking file, and have the Réalisateur say in its report that it consumed it.
Where: realisateur.md L364 ↔ 8_code.md L170-171, L134-136
Cited: 8_code.md L170 — "`git mv code/<lot>/blocked_<agent>.md code/<lot>/blocked_<agent>-NN.md`" — the only rename the command makes
Cited: realisateur.md L508-509 — "🔴 **You never rename it** — 📌 **you have no tool that removes a file.**"
Owner: 8_code
Follows: realisateur (the report line)
Also in: commandes

### realisateur F24 — the "still empty → call the Arbitre" row covers a case the command intercepts

Verdict: confirmed
Decision: Turn the row into a guard — an empty `## Decision` found at the start of a run means the orchestration should not have invoked you: stop and say so, never call the Arbitre again.
Where: realisateur.md L503 ↔ 8_code.md L169
Cited: 8_code.md L169 — "| **Its `## Decision` is empty** | 🔴 **Stop** — ⚠️ **invoking again re-raises the same block** |"
Cited: passes/realisateur.md C13 — "The agent's row then covers no reachable case and goes — or stays as a guard that stops without calling anyone."
Owner: realisateur
Also in: detailleur (same row at L437)

### realisateur F25 — the Détailleur still says the Réalisateur places the code

Verdict: confirmed
Decision: Have the Détailleur's never-do line say the Concepteur places the code, from the conventions.
Where: realisateur.md L533-535 ↔ detailleur.md L401-402
Cited: detailleur.md L401-402 — "- 🔴 **Decide where the code goes** — the Réalisateur does, from the conventions"
Cited: realisateur.md L533-535 — "📌 **You place nothing**: the concepteur did, against the conventions."
Owner: detailleur
Also in: detailleur

### realisateur F26 — move 4 takes an order the sheet does not carry

Verdict: confirmed
Decision: Drop the claim that `## Dependencies` carries the intra-lot order — that field lists what the lot consumes — and say the order is the one the signatures give, a symbol before those that call it, which is reading, not deciding.
Where: realisateur.md L567-569 ↔ detailleur.md L630-636
Cited: detailleur.md L631-636 — "📌 **one line per type the signature uses and this lot does not produce** … ⚠️ **A type this lot produces has no line** — 📌 **it is in `## Signatures`.**"
Owner: realisateur
Also in: —

### renommages F02 · passages-aval F01 — `## Files` cannot name a file the lot creates

Verdict: confirmed
Decision: Define `## Files` as the files the lot's modified symbols live in (the Détailleur's grep of every symbol gives them) plus `Touches`, and count a file the Concepteur places a created symbol in — named in `conception.md` — as declared for the two `## Outside the lot` fields that come after it, so that a created file is reported by nobody as outside the lot.
Where: realisateur.md L189-190 ↔ detailleur.md L259-262; cadreur.md L753-754; concepteur.md L186-188; testeur.md L58-59; relecteur.md L386-390
Cited: detailleur.md L259-262 — "🔴 **`## Files` carries the lot's `Modifies` and `Touches`, copied from `code/decoupage.md`** — 📌 **one path per line, no distinction between the two.**"
Cited: cadreur.md L753-754 — "🔴 **`Needs`, `Produces` and `Modifies` carry symbols, and symbols only.** 📌 **A name the code carries** — ⚠️ **never a file.**"
Cited: concepteur.md L186-188 — "📌 **The sheet's `## Files` narrows it** — 🔴 **a symbol goes in one of those files**, and the conventions say which."
Cited: testeur.md L58-59 — "🔴 **its `## Files` names every file the lot owns**: 📌 **where your tests go**"
Cited: realisateur.md L189-190 — "🔴 **`## Outside the lot` names every file you wrote in that the sheet's `## Files` does not name**"
Owner: detailleur (the field)
Follows: cadreur (L753-754 stays — the field is not copied from `Modifies` any more), concepteur (a created symbol's file is its to name), testeur and realisateur (`## Outside the lot` is checked against `## Files` plus the files `conception.md` places), relecteur (the three-field check at L386-390 takes the same union)
Also in: cadreur, detailleur, concepteur, testeur, relecteur

### renommages F04 — the `## Outside the lot` definition reads as two half-rules

Verdict: confirmed
Decision: Rewrite L189-191 as one rule — every file written in that the sheet's `## Files` does not name, and what was done to it, or a dash — dropping the spliced *"the sheet does not declare"*.
Where: realisateur.md L189-191 ↔ detailleur.md L261-262
Cited: realisateur.md L189-191 — "🔴 **`## Outside the lot` names every file you wrote in that the sheet's `## Files` does not name** — ⚠️ **the sheet does not declare**, and what you did to it — **or a dash.**"
Owner: realisateur
Also in: —

### renommages F08 — a decision the Concepteur applied reads as drift

Verdict: confirmed
Decision: Give `conception.md` a field naming the decision the Concepteur applied, and have the Relecteur accept that field beside the Réalisateur's `## What governed the code, besides the sheet` as what legitimises a divergence.
Where: concepteur.md L158-159 ↔ relecteur.md L184-185; realisateur.md L176-183
Cited: concepteur.md L158-159 — "🔴 **Say in your report that you applied it** — 📌 **the orchestration renames the file**"
Cited: relecteur.md L184-185 — "📌 **The decision is in the report's `## What governed the code, besides the sheet`** — 🔴 **that field, and nothing else, makes a divergence legitimate.**"
Owner: concepteur (the field)
Follows: relecteur (reads both fields)
Note: the Réalisateur's field keeps its meaning — what governed *its* code; no line of this file changes.
Also in: concepteur, relecteur

### renommages F09 — the report names a number the file does not yet carry

Verdict: confirmed
Decision: Have the report name the blocking file at its unnumbered name with the entry number (`blocked_realisateur.md — Blocking 2`), and have the Relecteur resolve that to the highest `blocked_realisateur-NN.md` in the lot folder, since the orchestration renames after the report is written and before the review.
Where: realisateur.md L176-178 ↔ 8_code.md L170-171; relecteur.md L184-185
Cited: realisateur.md L176-178 — "🔴 **`## What governed the code, besides the sheet` carries every decision you applied** … 📌 **the numbered blocking file, the rule by its number**"
Cited: 8_code.md L170 — "🔴 **rename it once the agent reports having applied it** … 📌 **`NN`: the highest in that folder plus one, `01` when there is none**"
Owner: realisateur (the field's form; the example at L158 changes with it)
Follows: relecteur (the grep that resolves it)
Also in: relecteur

### chemins-aval F03 · passages-aval F02 — `Cause: sheet` has no route

Verdict: confirmed
Decision: Route a `Cause: sheet` verdict to the Détailleur on that lot's sheet (a mode that rewrites one lot's sheet, since the ordinary mode skips a lot that has one), never to a fresh Réalisateur, and give the Réalisateur's FAIL table a row saying a `Cause: sheet` verdict is not its to code against — stop and say the sheet is being rewritten.
Where: relecteur.md L167-169 ↔ 8_code.md L138-139; realisateur.md L519-522; detailleur.md L465-469
Cited: relecteur.md L167-169 — "⚠️ **`sheet` says the fault is upstream**: the block goes back to the Détailleur, never to a fresh Réalisateur."
Cited: 8_code.md L138 — "**4.** On FAIL → a **fresh `realisateur`**, with the verdict, **then the `relecteur` again on the same lot**"
Cited: detailleur.md L467 — "| **A sheet, and no `PASS`** | 📌 **You skip it** …"
Cited: realisateur.md L519-522 — the FAIL table carries two rows, `FAIL mineur` and `FAIL structurel`
Owner: 8_code (the routing)
Follows: detailleur (the mode), realisateur (the row), relecteur (no change — L167-169 already says it)
Also in: commandes, detailleur, relecteur

### chemins-aval F09 — the re-cut lots keep their `conception.md` and `tests.md`

Verdict: confirmed
Decision: Have the post-redécoupage deletion cover `conception.md` and `tests.md` as well as `fiche-executable.md` for every lot with no `verdict.md` carrying PASS, so that the Concepteur and the Testeur run again on the re-cut lot.
Where: 8_code.md L379-382 ↔ 8_code.md L112-113; realisateur.md L533-535, L571-572
Cited: 8_code.md L379-382 — "🔴 **The sheets of every lot that is not coded are stale** … 📌 **Delete them**, in `code/<lot>/fiche-executable.md`"
Cited: 8_code.md L112-113 — "📌 **skipped when `code/<lot>/conception.md` is there** … 📌 **skipped when `code/<lot>/tests.md` is there**"
Note: the code those two reports describe stays committed in the tree — that residue is chemins-aval F08, in `## To settle`.
Owner: 8_code
Follows: realisateur (no line changes — it reads the two reports as they are)
Also in: commandes, concepteur, testeur

### chemins-aval F10 — a Relecteur block keeps its empty `## Decision` for ever

Verdict: confirmed
Decision: Have `/8_code` rename `blocked_relecteur.md` itself once the agent its table names has reported — a Relecteur block names a missing input that the fresh run supplies, not a decision anyone fills — so that move 4b does not stop the lot on the next pass.
Where: 8_code.md L418-422 ↔ 8_code.md L169-170; relecteur.md L232-234; realisateur.md L495-506
Cited: 8_code.md L420 — "| **The report** | 🔴 **A fresh `realisateur`** — 📌 **counted as an attempt** |"
Cited: relecteur.md L232-234 — "📌 **You never retire it** — 🔴 **you have no tool that renames or removes a file.** ⚠️ **The orchestration does it**, once the verdict is written."
Owner: 8_code
Follows: relecteur (no change), realisateur (no change — it never opens `blocked_relecteur.md`)
Also in: commandes, relecteur

### chemins-aval F21 — a verdict without `## Status`

Verdict: confirmed
Decision: Have the orchestration re-invoke a fresh Réalisateur after an attempt that committed nothing, with no verdict named, and give the FAIL table a row — no `## Status`, or no verdict named — meaning the previous attempt committed nothing: take the lot from move 1.
Where: 8_code.md L129-132, L149-151 ↔ realisateur.md L519-522
Cited: 8_code.md L129-132 — "📌 **An empty list means the realisateur committed nothing** — 🔴 **that counts as a failed attempt, and the Relecteur is not invoked.** ⚠️ **Increment `## Attempts` yourself then**"
Cited: realisateur.md L519-522 — two rows, `FAIL mineur` and `FAIL structurel`, keyed on a status
Owner: 8_code
Follows: realisateur (the row)
Also in: commandes

### chemins-aval F23 — no row for a back-to-split decision once `redecoupage.md` is gone

Verdict: confirmed
Decision: Add the row the Détailleur has — a `## Decision` sending the lot back to the split, and `code/redecoupage.md` gone, means the split was redone: carry on normally on the lot as it now stands, and say in your report that the decision was applied so the orchestration renames it.
Where: realisateur.md L505-506 ↔ detailleur.md L440-441
Cited: detailleur.md L441 — "| The same, **and `code/redecoupage.md` is gone** | 📌 **The split was redone** — 🔴 **detail the block, and say in your report that the decision was applied** |"
Cited: realisateur.md L505-506 — a *filled* row and a *filled and `redecoupage.md` still there* row, nothing for *gone*
Owner: realisateur
Also in: detailleur (already has it)

### passages-aval F12 — a test left green or a criterion gone has no field in `tests.md`

Verdict: confirmed
Decision: Give `tests.md` a field for the exceptions to `## Red` — a test left green because the declaration alone meets it, a criterion gone with an adapted test — and have the Réalisateur's read of `## Red` take those exceptions into account: a test named there is not one it has to turn green.
Where: testeur.md L221, L232-233, L268-291 ↔ realisateur.md L77-78; relecteur.md L333-334
Cited: testeur.md L221 — "📌 **Leave it green** — 🔴 **the criterion is met by the declaration**: ⚠️ **say so in your report**"
Cited: testeur.md L268-291 — the `tests.md` shape: `## Tests`, `## Criteria with no test`, `## Red`, `## Outside the lot` — no field for an exception
Cited: realisateur.md L77-78 — "**`code/<lot>/tests.md`** — 🔴 **its `## Red` line**: the tests were red when they were written"
Owner: testeur (the field)
Follows: realisateur (its `## Red` read), relecteur (its point 2 count)
Also in: testeur, relecteur

---

## Entries — the index (`docs/refonte/modifications.md`)

These four findings hold against the index, not against the agent. They
are applied on the index section at L1082-1121, alongside the correction
of the agent file, by whoever runs this plan.

### realisateur F01 — C1 records `git mv` the whitelist does not carry

Verdict: confirmed
Decision: Correct the C1 line — the whitelist gained `git restore` only, and the rename went to the orchestration.
Where: modifications.md L1114 ↔ realisateur.md L425-427, L508-509
Cited: modifications.md L1114 — "📌 **`git mv` et `git restore` ajoutés**"
Cited: realisateur.md L425-427 — "🔴 **Your `Bash` runs `git add`, `git commit`, `git status`, `git restore`, and the static analysis and test commands the conventions name.**"
Owner: modifications.md (index)
Also in: —

### realisateur F05 — five comments marked "à passer avec A3" whose command side is in place

Verdict: confirmed
Decision: Mark C3, C13, C14, C16 and C17 passed on the `/8_code` side, and name what remains on the agent side — F11 (C3) and F24 (C13) of this plan.
Where: modifications.md L1106 ↔ 8_code.md L12-14, L48-51, L142-157, L164-175, L463-466; realisateur.md L385-386, L475, L503
Cited: modifications.md L1106 — "📌 **Tous sur `/8_code`**, que **A3** réécrit — 🔴 **à passer avec elle**"
Cited: 8_code.md L463-464 — "⚠️ **A worktree with uncommitted files refuses a plain remove** — 🔴 **never force it**" (C3's command side); L169 (C13's); L48-51 (C14's); L142-157 (C16's); L12-14 (C17's)
Owner: modifications.md (index)
Also in: —

### realisateur F06 — the removal of the reprise lookup is recorded nowhere

Verdict: confirmed
Decision: Record in the index that Part 2 lost its reprise lookup and rename while the reprise is still written, and that F13 and F23 of this plan restore the lookup and move the rename to the orchestration.
Where: modifications.md L1085-1091 ↔ realisateur.md L364, L493-511
Cited: modifications.md L1085 — "✅ **FAIT** — 📌 **ses quatre modifications, et sa fiche de passe.**" — the four rows at L1087-1092 name no reprise
Cited: realisateur.md L364 — "🔴 **Write `code/<lot>/reprise_realisateur.md`**, then stop." — and Part 2 (L493-511) reads only `blocked_realisateur.md`
Owner: modifications.md (index)
Also in: —

### realisateur F07 — four changes the index does not list

Verdict: confirmed
Decision: Add to the index the multi-entry `## Blocking N` shape, the `Not settled here.` row, the move of the rename to the orchestration, and the rewritten wrong-sheet trigger list.
Where: modifications.md L1085-1092 ↔ realisateur.md L258-270, L504, L505-509, L215-216
Cited: modifications.md L1087-1092 — the four rows: *Réduit au codage*, *Les conventions*, *Avancer sur ce qui reste*, *Il piétine*
Owner: modifications.md (index)
Also in: —

---

## Settled elsewhere

**renommages F16** — `decisions.md` settles it: the Concepteur writes an
`architecte/` request like the Détailleur and the Réalisateur. No line
of this agent changes; its L468-469 (*"Invoke any agent but the
Arbitre"*) and L404-405 (its own request route) stand. The Concepteur's
plan carries the decision.

**cadreur F23 · fichiers F09** — `cycle.md` is deleted. Its L82 names
`_realisateur` in a stop table; the file goes with the decision, and
nothing in this agent refers to it.

---

## To settle

### realisateur F11 — what the reprise leaves in the tree

Verdict: confirmed
Decision:
Where: realisateur.md L385-386 ↔ realisateur.md L475; 8_code.md L463-466; docs/refonte/passes/realisateur.md C3
Cited: realisateur.md L385-386 — "📌 **Commit what compiles before you stop** — 🔴 **never commit what does not.** ⚠️ **Say in `En chantier` what you left uncommitted.**"
Cited: realisateur.md L475 — "- 🔴 **Leave a dirty working tree behind you**, whatever the reason"
Cited: 8_code.md L463-466 — "⚠️ **A worktree with uncommitted files refuses a plain remove** — 🔴 **never force it**: 📌 **say what is left there, and stop.** ⚠️ **An agent handed back leaving work uncommitted is a fault of that agent**"
Cited: passes/realisateur.md C3 — "Either the half-written piece is committed on the lot, flagged in `En chantier` as not compiling, or it is removed before the commit and `En chantier` says what was undone — I lean to the first, since the whole point of the reprise is not to redo it."
Owner: realisateur
Follows: 8_code (its removal step, either way)

The three lines cannot all hold. The next run opens a fresh worktree
from `HEAD`, so uncommitted code is unreachable to it whatever
`En chantier` says — the only choice is between the two options the
comment sheet names:

| Option | What it costs |
|---|---|
| **Commit the half-written piece, flagged in `En chantier` as not compiling** — the reviewer's lean | `HEAD` no longer compiles: the next lot's Concepteur, in its own worktree, cannot compile its declarations (8_code.md L112: *"Writes the declarations with empty bodies and compiles"*), and the Testeur's older tests cannot run. Every lot after the block is stopped until the Product Owner answers. |
| **`git restore` the non-compiling piece before stopping; `En chantier` says what was written and undone, and where** | The half-written code is lost; the next run redoes it from a description. `HEAD` compiles, the worktree is clean, L475 and the command's removal step hold as written. |

The second option is consistent with every 🔴 rule now in force
(L385 *never commit what does not compile*, L475, 8_code L463-466) and
with the Concepteur's and Testeur's commits, which always compile. The
first is the reviewer's explicit lean and buys the work back at the cost
of a `HEAD` that no lot after it can build on. The choice is the
Product Owner's; the plan stops here on it, and F13's `En chantier`
handling follows whichever is chosen.

### chemins-aval F08 — the dropped lot's declarations and tests stay committed

Verdict: confirmed
Decision:
Where: realisateur.md L335-338 ↔ testeur.md L228-232; 8_code.md L357-366
Cited: realisateur.md L335-338 — "🔴 **Drop what you wrote** — 📌 **`git restore` on the files you edited.** ⚠️ **Nothing you wrote is a new file**: the concepteur committed the declarations, the testeur the tests"
Cited: testeur.md L231 — "| **Anything else** | 🔴 **A block** — 📌 **the declarations broke something the sheet does not touch** |"
Owner: 8_code (the re-split handling)
Follows: realisateur (no change either way — its restore covers its own edits), concepteur, testeur

The Réalisateur's part is right as written: it can only restore what it
edited. What stays is the Concepteur's throwing declarations and the
Testeur's red tests of a lot that no longer exists, and the next lot's
Testeur blocks on them. Three ways out, none this plan's to pick:

| Option | What it costs |
|---|---|
| **The orchestration reverts the dropped lot's commits** (`git revert` of the Concepteur's and Testeur's commits) before `/7_lots` | The orchestrator's Bash is for git and this is git; but a revert of a mid-history commit can conflict with the lots coded after it in the same run, and the orchestrator does not resolve conflicts. |
| **The re-cut lot's Concepteur removes the declarations and tests the old lot left**, from the old `conception.md` and `tests.md` (chemins-aval F09 deletes them — they would have to survive as an input instead) | The Concepteur gains a delete gesture it does not have today, and a reading of files from a lot that is not its. |
| **The Testeur's *older test fails* row gains an exception** for tests of a lot the split dropped | Red tests and throwing bodies stay in the tree indefinitely; every later Testeur has to know the list of dropped lots. |

The first is the cheapest in rules and the riskiest in git; the choice
sits with the commandes plan and the Product Owner.
