# Verification V2.3 — Paths and loops, upstream

**Scope**: `.claude-new/commands/` — `1_lexique`, `2_structure`,
`3_decoupe`, `3a_genre`, `3b_nature`, `4_grille`, `5_reclasse`,
`6_convertit`, `conventions`, `fusion`, `fusion_compare`,
`fusion_applique`. Agent files opened only where a command's routing
depends on what the agent writes or renames: `redacteur`, `decoupeur`,
`classeur`, `sondeur`, `convertisseur`, `architecte`, `fusionneur`,
`lexicographe`.

Line numbers are those of the **new command file** unless marked
*(agent)*. Severity: **BLOCKING** — a state the chain cannot leave or
that loses work · **TO FIX** — a state with no routing line, or a
routing line that leads to a stop · **NOTE** — wasteful, ambiguous, or
inherited.

The summary is at the end (§4). The five specific checks are in §2,
the three scenarios in §3.

---

## 1. Per command — states and loops

### `/1_lexique`

**Blocking file** (36–42): absent → carry on · empty → stop · filled →
named. Filed afterwards (126–129). ✅ No `NN` rule stated for
`blocked_lexicographe-NN.md` (compare `2_structure` 135) — NOTE.

**Root states** (54–61, 70, 80–84):

| State at the root | Outcome | |
|---|---|---|
| No questions file, no `desc-produit.md` | Invocation 1 | ✅ |
| No questions file, `desc-produit.md` present | Line 82: "it stops 1 and 2" — a stop | ✅ written, but it is the dead end of three routes (see `3_decoupe`, `3a`, `3b` below) |
| `questions-lexicographe` alone, no `### Q` | Invoke nothing, say `/2_structure` | ✅ |
| `questions-lexicographe` alone, empty `Answer:` | Stop (70) | ✅ |
| `questions-lexicographe` alone, answered | Invocation 2 | ✅ |
| Another agent's file alone, **no `### Q`** | Invocation 3 runs on an empty file | NOTE — one opus invocation for nothing; row 57 has the guard for its own file only |
| Another agent's file alone, empty `Answer:` | Stop (70) | ✅ |
| Another agent's file alone, answered | Invocation 3 | ✅ |
| Another agent's + `questions-lexicographe`, both answered | Invocation 4 | ✅ |
| Another agent's + `questions-lexicographe`, either unanswered | Stop (70) | ✅ |
| Two files of other agents | Stop (61) | ✅ |
| Two `questions-lexicographe` files | Not in the table; caught by 170 "anything else … stop" | ✅ |

**Loop 1↔2** (73, 225): 2 always hands back to 1; 1 always writes a
file (agent 121); the loop ends when 1's file has no `### Q` (57). Exit
reachable; bound is the sweep converging. ✅

**Loop 3↔4** (agent 210–225): 3 writes a file always; empty → turn
over → `/2_structure` (227); non-empty → answered → 4; 4 writes a new
file only on an open choice (agent 122) → 4 again. Exit reachable. ✅

### `/2_structure`

**Lexicographe's file** (44–63): empty `Answer:` → stop · otherwise
filed. ✅ **An empty one** (no `### Q`) has no `Answer:` line, so it is
filed — correct.

**Blocking file** (65–75): absent / empty / filled. ✅ Filed with `NN`
(130–136). ✅

**Root states** (79–95):

| State | Outcome | |
|---|---|---|
| No questions file, no `desc-produit.md` | Invocation 1 | ✅ |
| No questions file, `desc-produit.md` | Stop, "transcribed once" (82) | ✅ written — but see TO FIX below |
| One file, no `### Q` | Invoke nothing, `/3_decoupe` | ✅ |
| One file, empty `Answer:` | Stop (94) | ✅ |
| One file, answered, any prefix | Invocation 2 | ✅ |
| Two or more | Stop (85) | ✅ |
| `blocked_redacteur.md` filled + no questions file + `desc-produit.md` | Row 82 fires: **stop** — the decision is never applied | **TO FIX** — see below |

**TO FIX — an invocation-2 block cannot be resumed.** Line 141: "At
invocation 2, file the questions file it integrated". When invocation 2
wrote `blocked_redacteur.md` mid-way, the command does not say whether
the file counts as integrated. If it is filed, the next run finds no
questions file and a `desc-produit.md` → row 82 stops, and the filled
`## Decision` has no invocation to reach. If it is not filed, the next
run is invocation 2 again, with the decision — which is the intent. The
line needs "unless it wrote a blocking file".

**TO FIX — no stop-merges-first clause.** 146–147: "a missing
[`questions-redacteur-NN.md`] stops the command" — `3a_genre` 139–143
and `3b_nature` 139–143 say that any stop after the agent ran merges
first; `2_structure` has no such line, and a stop here leaves the
worktree unmerged with the product file in it.

**Loop** (222–226): questions → answer → `/1_lexique` → `/2_structure`
(2) → new file → … ends when the Rédacteur's file is empty. The agent
writes one every time (agent 253). Exit reachable. ✅

### `/3_decoupe`

| State | Outcome | |
|---|---|---|
| `blocked_decoupeur.md` absent / empty / filled | 35–39 | ✅ |
| `Clarification needed` in the product file | Stop (44–47) | ✅ |
| Root `questions-*.md`, any state | Filed blind (49–52) | **TO FIX** — see *Unanswered files* in §2 |
| `desc-produit.md` absent | Stop (66–67) | ✅ |
| No `questions-sondeur-*` anywhere | Every block | ✅ |
| Later turn, no `NEW`/`MODIFIED` | Invoke nothing, commit, relay (88–90) | ✅ |
| Later turn, markers | Those blocks | ✅ |

**BLOCKING — the blocking route dead-ends.** Relay 201: "Fill its
`## Decision`, then `/2_structure` … `/3_decoupe` again afterwards".
The decoupeur blocks on one case only — a sentence carrying two
triggers whose "`To resume` is a rewording upstream" (agent 113–131).
`/2_structure` checks `blocked_redacteur.md` only (65), and the
Rédacteur reads "a blocking file the prompt names" (agent 383) — the
command never names `blocked_decoupeur.md`. With no questions file at
the root and a `desc-produit.md`, `/2_structure` row 82 **stops**. The
filled decision reaches nobody. Running `/3_decoupe` again names the
file to the decoupeur, which "may not reword" (agent 125). No agent
consumes a decoupeur decision.

### `/3a_genre`

| State | Outcome | |
|---|---|---|
| `blocked_qualifieur.md` absent / empty / filled | 36–40 | ✅ |
| Highest `questions/qualifieur/questions-qualifieur-NN.md` holds `### Q` | Named in the prompt (45–47) | ✅ — see NOTE |
| `Clarification needed` | Stop (52–55) | ✅ |
| Root `questions-*.md`, any state | Filed blind (57–60) | **TO FIX** (§2) |
| No `^Genre:$`, no `MODIFIED` | Invoke nothing (81–83) | ✅ |
| Otherwise | Those blocks | ✅ |
| After the run: `^Genre:$` count non-zero, no blocking file | Relay 205: `/3a_genre` again | ✅ bounded — the rerun names the same empty-genre blocks |

**TO FIX — the rewrite route.** Relay 203: "A `## Decision` names a
rewrite → `/1_lexique`, then the route back". `/1_lexique` with no
questions file and a `desc-produit.md` stops (its line 82); even if it
did not, `/2_structure` row 82 stops. Same dead end as `3_decoupe` —
no agent consumes a rewrite decision written in
`blocked_qualifieur.md`. Also relay 202 ("both end in the Rédacteur's
hands") — the questions file reaches the Rédacteur, the decision does
not.

**TO FIX — filed before it is looked for.** Line 45 reads the highest
file **under `questions/qualifieur/`**, line 57 files the root files
afterwards. On the normal route the answered file was filed by
`/2_structure` (its 141), so the order holds. But if the Product Owner
answered and ran `/3a_genre` directly, the answered file is still at
the root at line 45 (not seen), then filed at line 57 (not named) —
the answers are applied only on the following turn, if ever.

**NOTE — re-application.** When nothing is qualified (no invocation),
no new `questions-qualifieur` file is written, and the highest one
under `questions/qualifieur/` still holds `### Q` — the next turn names
it again and the agent re-applies the same answers. The agent tolerates
it (agent 157–163) but the prompt line is misleading.

**NOTE — `MODIFIED` grep unanchored** (79): `3_decoupe` 79 and
`4_grille` 121 warn that a bare marker matches prose. Same in
`3b_nature` 79.

### `/3b_nature`

Same shape as `3a_genre`; same TO FIX on the rewrite route (207), the
filing order (44 vs 56), the blind filing (56), and the same NOTES.

**TO FIX — the post-run check contradicts the scope.** 130–132:
"Grep `-c '^Nature:$'` … Zero is what you expect — anything else means
a block was left unclassed". The classeur never touches a
non-behaviour block (agent 34–37), and `5_reclasse` 59 says "a block of
any other genre carries an empty `Nature:`, and that is right". So the
count is non-zero on every feature that has a directive, a transverse
rule, a reference. Relay 209 then says "run `/3b_nature` again"; the
rerun invokes nothing (the comportement filter at 78 empties the list)
and relays row 209 again, since the count has not changed. The row
before 211 is matched forever. The check needs the same comportement
filter as line 78, `4_grille` 87–89 and `5_reclasse` 54–56.

### `/4_grille`

**Blocking files** (40–70): five names; empty → stop · filled → that
reading alone, or the merge alone. ✅ Markers changed in between → new
turn (72). ✅

| State | Outcome | |
|---|---|---|
| `Clarification needed` | Stop (75–78) | ✅ |
| A behaviour block with empty `Nature:` | Stop (87–90) | ✅ |
| Latest root file has an empty `Answer:` | Stop (96–99) | ✅ |
| Latest root file answered, **not integrated** | Passes, then filed at 361 — **answers lost** | **TO FIX** (§2) |
| First turn (no `questions-sondeur-*`) | Every behaviour block | ✅ |
| Later turn, markers | Those blocks + global | ✅ |
| Later turn, no markers, no `questions-existant-*` | Second time | ✅ written — **unreachable**, see BLOCKING |
| Later turn, no markers, `questions-existant-*` anywhere | Relay, `/5_reclasse` (160–162, 453) | ✅ |
| Second time, no `Global:` line | Empty file, no worktree (168–170) | ✅ |
| `blocked_existant.md`, empty or filled | **No routing line** | **TO FIX** |
| After the four: a `cadrage-produit/blocked_*` unnumbered | Stop, no merge (290–292) | ✅ |
| A reading missing, no blocking file | Stop, `/4_grille` again (306) | ✅ |

**BLOCKING — the first-time loop restarts on itself.** The loop is
meant to end on an empty `questions-sondeur-NN.md` (18, 354–355). The
relay for that case (451) says `/4_grille` again — "the second time
runs". The second time is reached only when "no block [is] marked"
(149–151, 157–158). Markers are stripped by one agent only: the
Rédacteur, at invocation 2, when it integrates a grid or conversion
file (agent 520–522). An **empty** questions file is never integrated —
`/2_structure` row 83 invokes nothing on it. So after the turn that
produced the empty file, every block the previous integration marked
still carries `NEW` or `MODIFIED`; the next `/4_grille` finds them at
118–119 and runs the four sondeurs on the same text, which produce the
same empty file, which relays "`/4_grille` again". Four opus
invocations and one sonnet per lap, with no exit on the relay table:
row 453 (`/5_reclasse`) requires the second time to have run or to be
over. The only way out is the Product Owner running `/5_reclasse`
against the relay, which skips the second time for good. The old
`4_grille` (324) went to `/5_reclasse` straight from the empty file;
the new "first time is closed" test was added without anything that
clears the markers when the grid asks nothing.

**TO FIX — `blocked_existant.md` is routed nowhere.** The second-time
prompt (187) names it, the sondeur writes it at `<out>/blocked_<your
name>.md` (agent 88) — the feature root — but it is not among the five
files of 45–51, no "Before anything else" row tests its `## Decision`,
no filing line numbers it, and the relay table (446–453) has no row
for a second-time block. A second-time sondeur that blocks leaves no
`questions-existant` file, so the next run's "has it already run?"
(160) says no and reruns invocation 3 with the block still standing.

**Loop bound — the second time.** Once only, guarded by
`questions-existant-NN.md` anywhere (160–162) and by the empty file
written when nothing attaches (168–170). ✅ The `NN` rule at 191 ("plus
one") implies several; harmless while 160 stands. Its answers, once
integrated, mark blocks — those go back through the first time, whose
loop then hits the BLOCKING above.

### `/5_reclasse`

| State | Outcome | |
|---|---|---|
| A `^Genre:$` | Stop, `/3a_genre` (50–52) | ✅ |
| A behaviour with empty `Nature:` | Stop, `/3b_nature` (54–57) | ✅ |
| Root `questions-*.md`, any state | Filed blind (62–65) | **TO FIX** (§2) |
| A genre outside the six · a nature outside the eight | Stop without writing (100, 146) | ✅ |
| Counts differ | Stop without committing (103–105, 149–152) | ✅ |
| Grid not closed (markers present, or a root questions file with `### Q`) | **No test** — the command runs | NOTE — it is the escape hatch from the `4_grille` loop, and it does not know it |

No loop. ✅ Wording: 79 says "at the feature folder's root", the
files are under `par-genre/` — NOTE.

### `/6_convertit`

| State | Outcome | |
|---|---|---|
| `code/decoupage.md` exists | Stop (35–38) | ✅ |
| `par-genre/` or `desc-par-nature.md` absent | Stop (40–44) | ✅ |
| `convertisseur/blocked_*` absent / empty / filled | 49–53 | ✅ |
| Root `questions-*.md`, any state | Moved blind (62–65) — line 333 admits it | **TO FIX** (§2) |
| Nature: part changed, or `-input.md` absent | Runs | ✅ |
| Nature: section absent or `<<ASSUMED`, part byte-identical | **Waits** (126) | ✅ written — but see §2, short loop |
| Nature: blocked, decision filled | Runs | ✅ |
| No nature runs, document standing | Nothing to write (148) | ✅ |
| No nature runs, otherwise | Assembly + invocation 2 (149) | ✅ written — see NOTE below |
| A nature blocked | Report, merge, stop (171–180) | ✅ |
| A nature wrote no section (product question it cannot write without) | No assembly, delete `spec-technique.md`, questions, relay (195) | ✅ |
| `[B` beside an empty questions file after invocation 2 | Invocation 2 once more, never twice (261–265) | ✅ bounded |
| `tracabilite.md` first column ≠ headings | Fault, reported (267–271) | ✅ |
| Blocking file named | Filed (294–298), no `NN` rule | NOTE |

**BLOCKING — the technical-question route has no reader and no exit.**
Detailed in §2. In one line: the agent writes technical questions to
`convertisseur/technique-<nature>.md` (agent 59, 294); the command
merges `questions-<nature>.md` and `questions-transversal.md` only
(281–282); nothing anywhere opens, files or relays `technique-*.md`
(grep of `.claude-new/` and `docs-new/`: two hits, both in the agent).

**NOTE — a document that "does not stand" is relayed as standing.**
131: "the document does not stand while one [nature] waits". A waiting
nature keeps its `<<ASSUMED` mark; 148 does not match (the document
holds `<<ASSUMED`), so 149 assembles and runs invocation 2 every time
the command is launched, on unchanged sections. Invocation 2's file is
then merged; if empty, relay 340 sends to `/conventions` and `/7_lots`
with the marks still in the document — the relay reports the count
(325) but routes on regardless. Each launch costs one opus invocation
and changes nothing.

**NOTE — relay table broken.** 337–339 are prose inserted between two
rows of the table at 330–340; the last row (340) is outside the table.

### `/conventions`

| State | Outcome | |
|---|---|---|
| `spec-technique.md` absent (inv. 1, 2, 4) | Stop (52) | ✅ |
| `blocked_architecte.md`, empty | Nothing (69) | ✅ |
| `blocked_architecte.md`, **filled** | **No row** — falls through to 70–76 | TO FIX — see below |
| Request with empty `## Verdict` | Invocation 3 | ✅ |
| Root `questions-architecte`, empty `Answer:` | Nothing (71) | ✅ |
| Root `questions-architecte`, answered | Invocation 2 | ✅ |
| Root `questions-architecte`, no `### Q` | Nothing, `/7_lots` (73) | ✅ |
| No `couverture.md` | **Invocation 1** (74) | **BLOCKING** on a second feature — §2 |
| `couverture.md` + `TECHNICAL_CONVENTIONS.md` | Invocation 4 (75) | ✅ written — unreachable when needed |
| `couverture.md`, no `TECHNICAL_CONVENTIONS.md` | Row 76, "nothing to do" | ✅ — the only state row 76 can match |

**TO FIX — filled `blocked_architecte.md`.** The agent renames it
itself when it resumes (agent 300–320), so no filing line is owed —
but the command must reach the same invocation that blocked. With the
table as written, a block at invocation 4 (before `couverture.md` was
written) is followed by row 74 → invocation 1, which "opens no
existing conventions file and writes it afresh" (78–79).

**Contradiction — where the integrated file goes.** 84–86: filed after
invocation 2, "otherwise every later run … integrates the same answers
twice". 133–134: "every `questions-architecte-*.md` but the highest —
the last one stays at the root". After invocation 2 wrote no new file,
the integrated one is the highest. One of the two lines has to yield.
If 84 wins, the root is empty on the next run and row 74/75 re-derives
or re-completes (an opus invocation for a walk already done). If 133
wins, row 72 integrates twice. NOTE — reachable only by running
`/conventions` by hand a second time.

**Loop** (invocation 2 → new file on an open choice → invocation 2):
bounded by the agent writing none (agent 502–505). ✅

### `/fusion`

| Row | State | Outcome | |
|---|---|---|---|
| 1 | `desc-produit.md` absent | Error | ✅ |
| 2 | `blocked_*` empty | Stop | ✅ |
| 3 | `blocked_*` filled | "The agent it names, at the invocation it names" | TO FIX — the blocking-file shape (agent 194–210) has no invocation field; the command must infer it from rows 4–11 and does not say so |
| 4 | `rapport-fusion.md` | Stop, done | ✅ |
| 5 | Root file with empty `Answer:` | Stop | ✅ |
| 6 | `questions-fusionneur`, answered | Invocation 2 | ✅ — **shadows row 8** |
| 7 | `plan-fusion.md` | Invocation 2 | ✅ |
| 8 | `questions-fusionneur` answered + `bugfix-*/` | Invocation 3 | **unreachable** — row 6 matches first |
| 9 | `bugfix-*/`, no `questions-fusionneur-*` anywhere | Invocation 3 | ✅ once |
| 10 | `desc-produit-fusion.md` absent | Rédacteur 3 | ✅ |
| 11 | Otherwise | Invocation 1 | ✅ |

**BLOCKING — the correction-cycle merge dead-ends after invocation 3.**
Row 9 runs invocation 3, which "writes a questions file even when
empty" (52–53, agent 502–503) under the same name as invocation 1's,
`questions-fusionneur-NN.md` (agent 89). On the next run that file is
at the root (117–118 keep the highest there). Two cases:

- **It holds questions**, answered → row 6 → invocation 2, whose
  inputs are "the merge plan · the questions file you wrote" (agent
  249) — `plan-fusion.md` does not exist, `desc-produit-fusion.md`
  does not exist (row 10 never fired). The agent blocks on a missing
  input (agent 182–186) → row 2 stops; no decision the Product Owner
  can write creates the plan. Nothing applies invocation 3's answers:
  row 8 would rerun invocation 3, which re-reads every bug list and
  merges again.
- **It is empty.** "Answered" is undefined in this command; the
  chain's own definition (`cycle.md` 62, "every `Answer:` carries
  text") is vacuously true → row 6 → the same dead end. Read strictly
  (needs a `### Q`), the file matches rows 5–9 nowhere, falls to row
  10, and the merge proceeds — one reading works, the other does not,
  and the command does not say which.

Rows 6/8 order is inherited from the old file (its 45–47); row 10 is
new and sits below both.

### `/fusion_compare` · `/fusion_applique`

No state is tested: no blocking-file check, no `Answer:` grep, no
existence check. The prompt template (38–43) names `<agent>` and
`<phase>` generically; the command's first line says which.

| State | `fusion_compare` | `fusion_applique` |
|---|---|---|
| `blocked_fusionneur.md`, empty | Not tested — the agent stops itself (agent 273) | same |
| `blocked_fusionneur.md`, filled | Not tested — the agent applies and renames (agent 275) | same |
| `desc-produit-fusion.md` absent | **Not tested** — the agent reads "the product file = `desc-produit-fusion.md`, never `desc-produit.md`" (agent 45); absent → block | — |
| `plan-fusion.md` absent | — | **Not tested** → block |
| Root `questions-fusionneur`, empty `Answer:` | — | **Not tested** — invocation 2 runs on unanswered questions |
| `rapport-fusion.md` exists | Not tested — invocation 1 reruns | Not tested — invocation 2 reruns, global merged twice |

**TO FIX — `/fusion_compare` has no route to `desc-produit-fusion.md`.**
The Rédacteur's invocation 3 that writes it is run by `/fusion` row 10
only. `6_convertit` 340 says "the merge, `/fusion_compare`, branches
off here whenever you choose" — launched from there, the file does not
exist, and the fusionneur blocks (or, worse, if it falls back on
`desc-produit.md`, merges a file still carrying markers). Either
`fusion_compare` runs the Rédacteur first, or its first line stops on
the missing file.

**TO FIX — `/fusion_applique` runs on an unanswered file** and on an
already-merged global (no `rapport-fusion.md` test). Every other
command of the cycle greps `^Answer:$` before invoking.

---

## 2. The five specific checks

### An empty questions file · an unanswered one · two at the root

| | Empty (no `### Q`) | Unanswered (an empty `Answer:`) | Two at the root |
|---|---|---|---|
| `1_lexique` | Own: loop ended (57) ✅ · other agent's: invocation 3 runs on nothing (NOTE) | Stop (70) ✅ | Two of other agents: stop (61); anything else: stop (170) ✅ |
| `2_structure` | Invoke nothing (83) ✅ | Stop (46, 94) ✅ | Stop (85) ✅ |
| `3_decoupe` · `3a_genre` · `3b_nature` · `5_reclasse` · `6_convertit` | Filed ✅ | **Filed — answers or questions lost** | Both filed |
| `4_grille` | Filed ✅ | Stop (97) ✅ | Only "the latest" is grepped (96); the other is filed blind |
| `conventions` | Row 73 ✅ | Stop (57, 71) ✅ | Other prefixes filed (124); own: all but the highest (133) ✅ |
| `fusion` | Undefined — see §1 | Stop (row 5) ✅ | Other prefixes filed (108); own: all but the highest ✅ |
| `fusion_compare` | Not tested | **Not tested** | Other prefixes filed; own: all but the highest |
| `fusion_applique` | Not tested | **Not tested** | Not tested before; all filed after (105) |

**TO FIX — five commands file an unanswered file silently.**
`3_decoupe` 49, `3a_genre` 57, `3b_nature` 56, `5_reclasse` 62,
`6_convertit` 62: "File every root `questions-*.md`". `1_lexique` 170–173
states the cost: "an answered questions file put away in
`questions/<agent>/` is read by no command again, and the Product
Owner's answers are lost" — and an unanswered one is lost the same
way. The Rédacteur's own questions are protected by the
`Clarification needed` marker (redacteur agent 465, 546); the
qualifieur's, the classeur's, the sondeurs', the Convertisseur's are
not. `4_grille` 96–99 and `conventions` 57 show the grep that is
missing. A related case: a file **answered but not integrated** (the
Product Owner skipped `/1_lexique` + `/2_structure`) passes
`4_grille`'s grep and is filed at 361 — since `/2_structure` files what
it integrates (141), any root file holding a `### Q` is by construction
not integrated, and that is the test to add.

### A blocking file: empty decision · filled · already numbered

| | Empty | Filled | Already numbered |
|---|---|---|---|
| `1_lexique` | Stop ✅ | Named; filed after, no `NN` rule | Ignored ✅ |
| `2_structure` | Stop ✅ | Named; filed with `NN` ✅ — but at invocation 2 the decision may be unreachable (§1) | Ignored ✅ |
| `3_decoupe` | Stop ✅ | Named to the decoupeur, which cannot act on its own `To resume` (rewording); relay sends to `/2_structure`, which stops — **BLOCKING** | Ignored ✅ |
| `3a_genre` · `3b_nature` | Stop ✅ | A genre/nature: applied ✅ · a rewrite: no consumer — **TO FIX** · outside the list: "nothing runs" ✅ | Ignored ✅ |
| `4_grille` | Stop ✅ (five names) · `blocked_existant.md`: **not tested** | That reading alone ✅ · `blocked_existant.md`: named in the prompt only if the orchestrator thinks of it; never filed | Ignored ✅ (`NN` = turn number, 334) |
| `5_reclasse` | No agent — n/a | | |
| `6_convertit` | Stop ✅ | That nature runs ✅; filed after, no `NN` rule | Ignored ✅ |
| `conventions` | Nothing (69) ✅ | **No row** — the agent handles it, but the command may pick the wrong invocation (§1) | Agent reads them as settled ✅ |
| `fusion` | Stop ✅ | Row 3 — the invocation cannot be read off the file | Agent ✅ |
| `fusion_compare` · `fusion_applique` | Not tested; the agent stops itself at the cost of an invocation | Agent applies and renames ✅ | ✅ |

### The second closing pass

**Does it fire when the first returns an empty file?** No. The relay
(451) sends the Product Owner to `/4_grille`; that run re-enters the
first time because the markers of the last integration are still on
the blocks — an empty file is never integrated and nobody else strips
`NEW`/`MODIFIED` (redacteur agent 520–522 is the only strip; grep of
`.claude-new/` finds no other). **BLOCKING**, detailed under
`/4_grille` in §1. The second time is reachable only when the last
integration changed no block at all.

**Does it run once only?** Yes, if reached: `questions-existant-NN.md`
anywhere ends it (160–162), and the "nothing attaches" case writes the
file empty (168–170) so the guard always exists afterwards. One gap: a
second-time sondeur that **blocks** writes no `questions-existant`
file, so the guard is absent and the invocation reruns — with a
`blocked_existant.md` no line of the command tests or files (**TO
FIX**).

### The Convertisseur's short loop against its long loop

**The long loop** (product questions, relay 335): the answer changes a
block → `/1_lexique` (3) → `/2_structure` (2) → `/3_decoupe` →
`/3a_genre` → `/3b_nature` → `/4_grille` → `/5_reclasse` rewrites
`desc-par-nature.md` → `/6_convertit` finds the nature's part differs
from `<nature>-input.md` (123) → that nature runs. Reaches its exit —
subject to the `/4_grille` BLOCKING on the way back (an empty grid file
after the integration loops there).

**The short loop** (technical questions, relay 334): "Answer them, then
`/6_convertit` — a technical answer changes no block, so nothing
upstream has to run again." Four breaks, each sufficient:

1. **The questions never reach the Product Owner.** The agent writes
   them to `convertisseur/technique-<nature>.md` (agent 59, 294). The
   command merges into the root file "the files this run wrote — the
   natures in section order, then `questions-transversal.md`" (281–282)
   — that is `questions-<nature>.md`, the product ones. `technique-*`
   is not merged, not filed to `closed/` (74–78 move `questions-*`
   only), not counted in the relay.
2. **The command cannot tell the two kinds apart.** 25–26: it never
   reads a question. The relay rows 334/335 ask it to know whether the
   questions are technical or product; the only greppable difference
   (`Block:` vs `Entries:`, agent 318–323 and 340–348) is not named.
3. **The rerun runs nothing.** The nature's part is byte-identical to
   its `-input.md` (a technical answer changes no block, by definition
   at 334); its section holds `<<ASSUMED` or is absent → row 126:
   "Waits — it does not run". The exit condition of the short loop —
   the section written again with the answer — requires "its part
   changed" (125), which the loop's own premise rules out.
4. **The agent cannot read the answer.** "Open … any questions file —
   an answer reaches you through the product file" (agent 515–516),
   and invocation 1 reads its blocks, the headings and the grid (agent
   539). A technical answer is "not written anywhere afterwards … it
   is applied when the section is written again" (agent 328) — by an
   agent that may not open the file it sits in.

Net: a technical question leaves an `<<ASSUMED` mark (or no section)
that nothing can lift, and the document either never stands (131) or
is relayed as standing with marks in it (340). **BLOCKING.**

### The Architecte's invocation 4

**How does the command choose 4 over 1?** Rows 74–75: no
`couverture.md` at the working folder's root → invocation 1; a
`couverture.md` and `docs/TECHNICAL_CONVENTIONS.md` → invocation 4.
Lines 78–82 explain: "this feature's own `couverture.md` is the test:
invocation 1 alone writes it, and it tells a feature never derived
from one already done."

**The test is inverted.** Invocation 1 writes `couverture.md` (agent
274, 380); invocation 4 writes it too, "for this feature" (agent 277,
681). On a **second feature's first** `/conventions`, its folder has no
`couverture.md` — nothing has run there yet — so row 74 fires and
invocation 1 runs, which by its own rule reads "no conventions file,
whatever its name … not one your own earlier run left behind" (agent
74–77) and writes `TECHNICAL_CONVENTIONS.md` — the "silent rewrite"
78–82 says the rows prevent, losing "every rule invocation 3 added
since". Row 75 fires only after invocation 1 has already run on this
feature, i.e. after the damage. The state that distinguishes a first
feature from a later one is the existence of
`docs/TECHNICAL_CONVENTIONS.md`, which row 74 does not look at.
**BLOCKING** for any project past its first feature.

Corollary: invocation 4 blocked before writing `couverture.md` → row 74
→ invocation 1 on resume (same loss). And a bug-fix cycle (second
argument) that has no pending request: row 75 → invocation 4 walks the
feature again — 22–24 restrict 1 and 2 to the feature folder but say
nothing of 4 (NOTE).

---

## 3. Three scenarios

### A — a first feature on an empty project

`idees.md` alone. `/1_lexique` 1 → (questions → 2 → 1)\* → empty file →
`/2_structure` 1 → `desc-produit.md`, every block `NEW`, `Genre:` and
`Nature:` empty, `questions-redacteur-01` → (questions → `/1_lexique` 3
→ `/2_structure` 2)\* → empty → `/3_decoupe` (every block) →
`/3a_genre` (every block; questions go round through `/1_lexique` and
`/2_structure` and come back under `questions/qualifieur/`) →
`/3b_nature` (post-run count non-zero if any non-behaviour block exists
— relay 209 says rerun; the rerun invokes nothing and says the same;
the Product Owner has to run `/4_grille` against the relay) →
`/4_grille` turn 1 (every behaviour block, `NEW`) → questions →
`/1_lexique` 3 → `/2_structure` 2 (strips `NEW`, marks `MODIFIED`) →
`/3_decoupe` → `/3a` → `/3b` → `/4_grille` turn 2 → … → **turn N asks
nothing → relay "`/4_grille` again" → the same blocks still carry
`MODIFIED` → turn N+1 = turn N. Stops here**, on the relay table; the
Product Owner escapes by running `/5_reclasse` by hand, and the second
time never runs (on an empty project it would have found no `Global:`
line and written an empty `questions-existant-01` — no loss, but not by
design).

Then `/5_reclasse` → `/6_convertit`: product questions take the long
loop and come back with the nature's part changed ✅; **a technical
question is never shown** (§2) and its `<<ASSUMED` mark never lifts;
each relaunch re-assembles and reruns invocation 2. With no technical
question: empty file → `/conventions` → no `couverture.md` → invocation
1 ✅ (correct on a first feature) → questions → invocation 2 → `/7_lots`.
Later `/fusion`: row 10 → Rédacteur 3 → row 11 → invocation 1 → row
6/7 → invocation 2 → `rapport-fusion.md` → row 4 stop ✅.

### B — a feature on a project that already has some

Identical up to `/4_grille`, where the difference should show: blocks
carrying `Global:` are to be crossed against `PRODUIT_GLOBAL.md` in the
second time. **Unreachable** — same loop as A. If the Product Owner
forces `/5_reclasse`, the crossing is skipped and nothing records it
(`/5_reclasse` does not test for `questions-existant-*`).

`/6_convertit` as in A. `/conventions`: **no `couverture.md` in this
feature → invocation 1 → `docs/TECHNICAL_CONVENTIONS.md` rewritten
afresh**, every rule the previous features' lots added is lost; the
relay says `/7_lots` as if nothing happened. `/fusion` as in A ✅ (one
`bugfix-*/` absent).

### C — a correction cycle (`bugfix-NN/`)

None of the twelve commands runs the chain on a `bugfix-NN/`; two of
them have a bug-fix invocation.

`/conventions <feature> bugfix-NN`: a request with an empty
`## Verdict` in `bugfix-NN/architecte/` → invocation 3 ✅. No pending
request: the table falls to rows 71–76 on the **feature** folder — an
empty `questions-architecte` left at the root → row 73, "`/7_lots`"
(misleading but harmless); otherwise row 75 → invocation 4 re-walks the
feature (NOTE).

`/fusion <feature>` after the bug-fix lots are coded: row 9 →
invocation 3 → `questions-fusionneur-01.md` (empty or not) → next run:
**row 6 → invocation 2 with no `plan-fusion.md` and no
`desc-produit-fusion.md` → the agent blocks → row 2 stop.** No decision
unblocks it: the plan is written by invocation 1, which row 11 reaches
only when no answered `questions-fusionneur` sits at the root, and
108–118 keep the highest one there. **Stops here.** (Under a strict
reading of "answered" the empty-file case falls through to row 10 and
proceeds; the non-empty case dead-ends either way.)

---

## 4. Summary of findings

### BLOCKING

| # | Where | Finding |
|---|---|---|
| B1 | `4_grille` 149–151, 451; redacteur agent 520 | The first-time loop restarts on itself: an empty `questions-sondeur` is never integrated, so no marker is ever stripped, so "no block marked" is never true, so the second time and `/5_reclasse` are unreachable from the relay. Every feature hits it. |
| B2 | `6_convertit` 126, 281–282, 334; convertisseur agent 59, 294, 328, 516 | The short loop has no path: `technique-<nature>.md` is merged nowhere, the command cannot tell technical from product, the rerun "waits" on a byte-identical part, and the agent may not open a questions file. An `<<ASSUMED` left by a technical question never lifts. |
| B3 | `conventions` 74–75, 78–82; architecte agent 74–77 | The invocation-1/4 test reads the feature's `couverture.md`, absent on every feature's first run; a second feature runs invocation 1 and rewrites `docs/TECHNICAL_CONVENTIONS.md` afresh. |
| B4 | `fusion` rows 6–10, 117–118; fusionneur agent 89, 249, 502 | After invocation 3, its `questions-fusionneur-NN.md` matches row 6 → invocation 2 without a plan → block. Row 8 is shadowed; row 10 sits below. A correction cycle cannot be merged. |
| B5 | `3_decoupe` 201; `2_structure` 65, 82; decoupeur agent 125–131 | The decoupeur's only block asks for a rewording upstream; `/2_structure` names `blocked_redacteur.md` only and stops on "no questions file + `desc-produit.md`". No agent consumes the decision. |

### TO FIX

| # | Where | Finding |
|---|---|---|
| F1 | `3_decoupe` 49 · `3a_genre` 57 · `3b_nature` 56 · `5_reclasse` 62 · `6_convertit` 62 | Every root `questions-*.md` is filed without the `^Answer:$` grep — an unanswered file (or an answered, not integrated one) is lost. `4_grille` 361 files an answered-not-integrated file the same way; a root file holding `### Q` is the test. |
| F2 | `3a_genre` 203 · `3b_nature` 207 | "A `## Decision` names a rewrite → `/1_lexique`, then the route back": `/1_lexique` stops on `desc-produit.md` (its 82), `/2_structure` stops at row 82; no consumer for the decision. |
| F3 | `3b_nature` 130–132, 209 | Post-run `grep -c '^Nature:$'` counts the non-behaviour blocks (which rightly stay empty — `5_reclasse` 59, classeur agent 34–37); relay 209 reruns forever. Needs the comportement filter. |
| F4 | `4_grille` 45–51, 187, 446–453; sondeur agent 88 | `blocked_existant.md` is named in a prompt but tested, filed and relayed nowhere; a second-time block reruns invocation 3. |
| F5 | `2_structure` 141 | "File the questions file it integrated" does not say what to do when invocation 2 blocked — filed, the decision can never be applied (row 82). |
| F6 | `2_structure` 146 | A stop on a missing `questions-redacteur` does not merge first (contrast `3a_genre` 139–143). |
| F7 | `conventions` 69–76 | No row for a filled `blocked_architecte.md`; a block at invocation 4 before `couverture.md` resumes as invocation 1. |
| F8 | `conventions` 84–86 vs 133–134 | The integrated file is "filed after invocation 2" and "the highest stays at the root" — both cannot hold. |
| F9 | `fusion` row 3 | "At the invocation it names" — the blocking file's shape carries no invocation. |
| F10 | `fusion_compare` (whole) · `6_convertit` 340 | No test for `desc-produit-fusion.md`, which only `/fusion` row 10 produces; launched from `6_convertit`'s hint, the fusionneur blocks. |
| F11 | `fusion_applique` (whole) | No `^Answer:$` grep, no `plan-fusion.md` test, no `rapport-fusion.md` test — invocation 2 runs unanswered, or twice. |
| F12 | `3a_genre` 45 vs 57 · `3b_nature` 44 vs 56 | The answered file is looked for under `questions/<agent>/` before the root is filed; answered at the root, it is filed unseen. |

### NOTE

| # | Where | Finding |
|---|---|---|
| N1 | `1_lexique` 59 | Another agent's empty file → invocation 3 on nothing (own file guarded at 57, other's not). |
| N2 | `1_lexique` 128 · `6_convertit` 297 | No `NN` rule for the blocking file (compare `2_structure` 135). |
| N3 | `3a_genre` 79 · `3b_nature` 79 | `MODIFIED` grep unanchored, against `3_decoupe` 79 and `4_grille` 121. |
| N4 | `3a_genre` 45–50 | With nothing to qualify, the same answered file is named again next turn and re-applied. |
| N5 | `5_reclasse` | No test that the grid closed (markers, root `### Q`, `questions-existant`) — it is the de-facto exit of B1 and does not know it. |
| N6 | `6_convertit` 131, 148–149, 340 | A "waiting" nature keeps the document from standing, yet every relaunch assembles, reruns invocation 2, and relays `/7_lots` with `<<ASSUMED` marks in the document. |
| N7 | `6_convertit` 330–340 | Prose at 337–339 splits the relay table; row 340 is outside it. |
| N8 | `conventions` 22–27 | Invocation 4 is not restricted to the feature folder as 1 and 2 are; a bug-fix run with no request re-walks the feature. |
| N9 | `cycle.md` (identical to the old file) | Still routes to `/1_structure`, `/2_grille`, `/3_reclasse`, `/4_convertit`, `/5_compare`, `/7_decoupe` and tests `[integrated:` — out of scope here, but it is the command that chains the twelve. |
| N10 | `5_reclasse` 79 | "Six files, at the feature folder's root" — they are under `par-genre/`. |
