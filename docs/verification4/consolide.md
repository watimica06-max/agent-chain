# Vérification 4 — consolidé

Five reports read: `renommages.md` (5) · `fichiers.md` (5) · `chemins-amont.md` (18) · `chemins-aval.md` (17) · `passages.md` (3) — 48 findings. Every file a BLOCKING or TO FIX `Where` names was opened at those lines under `.claude-new/`. Line numbers below are the ones read, which sometimes widen or correct the ones reported.

Merged on `Where` (same file, same line): seven merges, eight findings absorbed. One placement is stated because the rule alone does not settle it: chemins-aval F12 shares `8_code.md L216-218` with entry 4 and `8_code.md L71-74` with chemins-aval F10; it sits with F10 (entry 34), because its defect is the missing resume row and the revert step is only what sends the run back there. Entry 4 and entry 34 are not merged with each other.

Severity order: BLOCKING · TO FIX · QUESTION · NOTE. Verdicts were given to BLOCKING and TO FIX, and to the one NOTE the *Settled* table covers; the rest carry `—`. Where a NOTE's lines were read on the way to a merge and contradict it, the entry says so with the line.

| # | Severity | Verdict | Finding | Where | Owner | Same as |
|---|---|---|---|---|---|---|
| 1 | BLOCKING | confirmed | The sheet marks every signature `created` or `modified`; the Concepteur has no rule on the mark, declares every symbol with a throwing body and reads a taken name as a clash — every bug-fix lot fails at its first agent | detailleur.md L267-271 ↔ concepteur.md L190, L236-245, L78, L176-179 (relecteur.md L379-381, cadreur.md L422-423) | concepteur.md | — |
| 2 | BLOCKING | confirmed | The blocking-file row of `/2_structure` runs the Rédacteur beside an empty questions file nothing files; the Rédacteur writes a second one, and two files at the root stop `/1_lexique` and `/2_structure` alike | 2_structure.md L143-162, L313-316 ↔ redacteur.md L274-276 ↔ 1_lexique.md L63, 2_structure.md L145, L384 | 2_structure.md | — |
| 3 | TO FIX | confirmed | `## Décision du Product Owner` resets the redécoupage count, and no command names it to the Product Owner nor tells the Cadreur what the section is | 8_code.md L566-572, L748-759 ↔ 7_lots.md L318-323 ↔ cadreur.md L976-981 | 8_code.md | chemins-aval F08 |
| 4 | TO FIX | confirmed | The `<lot>:` commits and the `sheet`-cause revert disagree on the lot's perimeter: `compte-rendu.md` is in neither list, the Concepteur's request and the Arbitre's trap ride the lot commit and are reverted with it | 8_code.md L215-221, L594-595, L406 ↔ realisateur.md L695-700 ↔ concepteur.md L281-288 ↔ arbitre.md L401 ↔ detailleur.md L668-681 ↔ audit_conventions.md L26-27 | 8_code.md | fichiers F02, fichiers F03 |
| 5 | TO FIX | confirmed | The Testeur is told to say in its report that it applied a decision, and `tests.md`'s five fields hold no place for it, so the rename `/8_code` keys on never fires | testeur.md L150-152, L56, L315-343 ↔ 8_code.md L303-305 (concepteur.md L311) | testeur.md | — |
| 6 | TO FIX | confirmed (F02) · F17's mechanism contradicted | The rewrite route sends a mixed blocking file to `/2_structure`, which renames it after a Rédacteur that applies rewrites alone — the genre decisions are read by nobody; the same row's `/1_lexique` leg spends a run on a stop | 3a_genre.md L284, L33-40 · 3b_nature.md L295 ↔ 2_structure.md L300-307, L384 ↔ redacteur.md L578-580, L275 · 1_lexique.md L56-59, L93-99 | 3a_genre.md | chemins-amont F17 |
| 7 | TO FIX | confirmed | The closure test runs before the marker greps, so once the first time is closed a block a later answer creates or changes reaches the Convertisseur unprobed | 4_grille.md L176-183, L128-134, L319-321 ↔ 2_structure.md L382 ↔ redacteur.md L132 | 4_grille.md | — |
| 8 | TO FIX | confirmed | The "latest questions file is answered" gate carries no `questions-architecte` exception, and stops a grid turn on a file only `/conventions` reads | 4_grille.md L102-106 ↔ L224-228, L235 ↔ conventions.md L84 (architecte.md L546-548) | 4_grille.md | — |
| 9 | TO FIX | confirmed | Rows L149 and L151 both match a nature with `<<ASSUMED`, its part unchanged and its technical file answered; no first-match rule, and the answer file goes to L151's row alone | 6_convertit.md L143-153, L198-199, L313-316 ↔ convertisseur.md L502-512 | 6_convertit.md | — |
| 10 | TO FIX | confirmed | The empty-architecte-file row precedes invocation 4's, so after `/2_structure` deleted `couverture.md` the run files the leftover and says `/7_lots` without walking the rebuilt document | conventions.md L73-74, L86, L88, L140-143 ↔ 2_structure.md L246, L279-281 | conventions.md | — |
| 11 | TO FIX | confirmed | `/fusion_compare`'s three gates test neither `bugfix-*/` folders, nor `plan-fusion.md`, nor `rapport-fusion.md`, so row 8 of `/fusion` can never fire and a re-run overwrites a plan or compares against a merged global | fusion_compare.md L20-26 ↔ fusion.md L58, L62, L64, L91-93 | fusion_compare.md | chemins-amont F15 |
| 12 | TO FIX | confirmed | The blocking-file rename sits after step 5, outside the commit and the push, where `/fusion_applique` rules it out | fusion_compare.md L150-156, L173-181 ↔ fusion_applique.md L143-154 | fusion_compare.md | — |
| 13 | TO FIX | confirmed | A Relecteur block on the two "relay and stop" rows is retired by nobody, and the two files disagree on whether the Product Owner fills its `## Decision` | 8_code.md L279-282, L676-691 ↔ relecteur.md L262-269, L325-335 | 8_code.md | — |
| 14 | TO FIX | confirmed | The verdict's `## Findings` reach the Détailleur's prompt inside move 4 only; a cold re-entry after a `sheet` revert whose Détailleur step did not finish reaches move 1 and invokes it blind | 8_code.md L129, L67-79 ↔ L222-226, L350-361, L376-379 | 8_code.md | — |
| 15 | TO FIX | confirmed | A run that applies a filled decision and blocks anew writes the same unnumbered file, and the rename on the "applied" report archives the new block as settled | 8_code.md L277 ↔ detailleur.md L311, realisateur.md L262 (7_lots.md L177-180) | 8_code.md | — |
| 16 | TO FIX | confirmed | `## Redécoupage: archivable` stays in `code/sequence.md` after the archive; a later redécoupage where the Cadreur goes out before calling the Vérificateur archives the fresh file unsplit | 7_lots.md L115-127 ↔ verificateur.md L97-100, L501-503 ↔ cadreur.md L925-926 | 7_lots.md | — |
| 17 | TO FIX | confirmed | The multi-lot revert is ordered per lot only; two lots' appends to `code/recette.md` and the state document conflict when an older lot is reverted first, and the conflict stops the command | 8_code.md L579-587, L236-241 ↔ testeur.md L283-288 (realisateur.md L693) | 8_code.md | — |
| 18 | TO FIX | confirmed | Step 1 of the closing sequence lists only feature-folder files as uncommitted and omits `TECHNICAL_CONVENTIONS.md`, `couverture.md` and the Arbitre's trap, written by agents with no Bash | 8_code.md L720-724 ↔ architecte.md L4 (reported L15) · arbitre.md L401, L478 | 8_code.md | — |
| 19 | QUESTION | — | After a third-round `blocked_cadreur.md` is answered the Vérificateur writes `Round: 4`; the Cadreur's rule speaks of the third only, and a decision buys no fresh rounds | cadreur.md L919-926 ↔ verificateur.md L121-126 | cadreur.md | chemins-aval F07 |
| 20 | NOTE | — | The grid's `R4` routes a missing form to a conventions request; the Architecte routes it to a `Kind: forme` question — two routes for one thing | GRILLE_CONVENTIONS.md L50-52 ↔ architecte.md L300-301, L564-568 | GRILLE_CONVENTIONS.md | — |
| 21 | NOTE | — | The second head rule spells `Cause: sheet` where the template and `/8_code` read a `## Cause` heading with `sheet` under it | relecteur.md L363 ↔ relecteur.md L160-162, 8_code.md L211 | relecteur.md | — |
| 22 | NOTE | stale | Both process documents still say "`/cycle` ne l'appelle pas" | PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010 | — | — |
| 23 | NOTE | — | `/audit_blocages`, `/audit_conventions` and `/deploie` sit in no row of the orchestrator's command table, whose L62 makes anything else an ordinary request | CLAUDE.md L51-57, L62 ↔ audit_blocages.md L1, audit_conventions.md L1, deploie.md L1 | CLAUDE.md | — |
| 24 | NOTE | — | `cadrage-produit/releve.md` is written and read by the global sondeur alone, then archived for nobody | sondeur.md L230-231 ↔ 4_grille.md L450, L256-260 | 4_grille.md | — |
| 25 | NOTE | — | `decisions-produit.md` is "one decision per line, identifier first", and a `## Decision` copied "as written" spans lines whose continuations open on no identifier | 9_controle.md L404 ↔ arbitre.md L152 ↔ redacteur.md L749 | 9_controle.md | — |
| 26 | NOTE | — | The stop-path pointer names three steps where the section holds five; read literally the commit inside the worktree is skipped | 3b_nature.md L221 ↔ 3b_nature.md L253-263 (3a_genre.md L219) | 3b_nature.md | — |
| 27 | NOTE | — | A `Clarification needed` flag with no questions file at the root bounces between `/3_decoupe` and `/2_structure` for ever | 3_decoupe.md L47-50 (3a_genre.md L49-52, 3b_nature.md L48-51, 4_grille.md L81-84) ↔ 2_structure.md L150 | 2_structure.md | — |
| 28 | NOTE | — | The stop on an unanswered root `questions-architecte-*.md` precedes the walk, and blocks an invocation 3 for a `bugfix-NN` that needs neither | conventions.md L68-69 ↔ conventions.md L26-27, L83 | conventions.md | — |
| 29 | NOTE | — | A feature with no `Genre: comportement` block runs four opus sondeurs on an empty list | 4_grille.md L120-126 ↔ sondeur.md L53 | 4_grille.md | — |
| 30 | NOTE | — | The *Otherwise → assembly* row sends to the assembly both an all-`directive` feature (an empty document, a walk and a split on nothing) and a waiting nature whose `<nature>.md` stands (an opus invocation for a known result on every re-run) | 6_convertit.md L174-175, L145, L230-233, L433-436 ↔ 5_reclasse.md L134-137 ↔ fusionneur.md L83-86 | 6_convertit.md | chemins-amont F18 |
| 31 | NOTE | — | The `### Q` guard of `/fusion_compare` has no exception for the Fusionneur's own file, and stops on one `/fusion` integrated | fusion_compare.md L50-56 ↔ fusion.md L153-154 | fusion_compare.md | — |
| 32 | NOTE | — | `/fusion` files other agents' root questions files without the `### Q` guard, and an answered, unintegrated file is put away with its answers | fusion.md L140-144 ↔ 3_decoupe.md L52-58 | fusion.md | — |
| 33 | NOTE | — | The walk greps every lot's produced symbol, coded lots included, and "a production that already exists" stops the block on its own PASSed lots | detailleur.md L501-503 ↔ detailleur.md L115-117 (L512) | detailleur.md | — |
| 34 | NOTE | — | *Where to resume* skips every PASSed lot, so the promised re-run on one has no trigger; and a revert conflict stops the command with nothing changed, so every re-run hits it again and no row says how the Product Owner unblocks the lot | 8_code.md L71-74 ↔ L695-698 · L216-218 | 8_code.md | chemins-aval F12 |
| 35 | NOTE | — | The hand-back table has no first-match rule; a Vérificateur block leaves the previous `sequence.md` with its empty `## Defects`, and row 1 reports "the split holds" | 7_lots.md L165 ↔ 7_lots.md L172 | 7_lots.md | — |
| 36 | NOTE | — | Three empty attempts leave no verdict and no count on disk; the cap holds in one run and the next repeats the three | 8_code.md L253-255 ↔ 8_code.md L259-261 (L706) | 8_code.md | — |
| 37 | NOTE | — | Move 2 skips the Concepteur and the Testeur on their report but never the Réalisateur on `compte-rendu.md`, so a coded, unreviewed lot re-runs it as a first run | 8_code.md L138-140 ↔ 8_code.md L184-188 | 8_code.md | — |
| 38 | NOTE | — | The ownership list of finding 3 names five agents and omits the Concepteur and the Testeur | audit_blocages.md L107-109 ↔ concepteur.md L12 | audit_blocages.md | — |
| 39 | NOTE | — | On a correction cycle finding 7 reads anchors citing `desc-bug.md` against a `couverture.md` traced to `spec-technique.md`; every rule reads "never met" | audit_conventions.md L144-145 ↔ audit_conventions.md L53-57 | audit_conventions.md | — |
| 40 | NOTE | — | Gap identifiers are positional; a gap inserted into `bug-list.md` between runs shifts them, and invocation 2 blocks on a mismatch no decision lifts | diagnostique.md L37 ↔ diagnostiqueur.md L80-81, L194-198 | diagnostique.md | — |

---

## BLOCKING

### passages F01 — The Concepteur has no rule on the `created` / `modified` mark

Severity: BLOCKING
Same as: —
Where: detailleur.md L267-271 (every `## Signatures` line opens on its mark, copied from `Produces` or `Modifies`; the Réalisateur and the Relecteur key on it) ↔ concepteur.md L190 ("Every symbol it names, with its signature"), L236-245 (each body throws *not implemented*), L78 and L176-179 (a name already taken is a clash, a duplicate-symbol error) · relecteur.md L371-381 (the "written beside the old one" finding) · cadreur.md L422-423 ("Almost everything you declare is a modification")
Verdict: confirmed — a grep of *modified* and *modifies* in `concepteur.md` returns nothing; L190, L236 and L178 read as the report says.
Finding: The Concepteur, first reader of the sheet, declares a `modified` symbol as a new one or refuses it as a clash, so every lot of a bug-fix cycle fails at its first agent and the Relecteur's finding at L381 arrives two agents too late.
Owner: concepteur.md
Follows: — (detailleur.md L267 defines the mark and relecteur.md L379-381 already reads it; both sides are present in the report)

### chemins-amont F01 — A filled blocking file beside an empty questions file leaves two files at the root

Severity: BLOCKING
Same as: —
Where: 2_structure.md L143-162 (the dispatch table: questions-file rows first, then the blocking-file row; L160-162 designs the very case, "a filled decision beside a file that asked nothing is taken"), L313-316 (invocation 2 files "the questions file it integrated" — none, on a blocking-file run) ↔ redacteur.md L274-276 ("Write it at invocations 1 and 2, even empty") ↔ 1_lexique.md L63 and 2_structure.md L145 (two files → "a filing failed", stop), 2_structure.md L384 (the route recommended)
Verdict: confirmed — L313 is the only filing line of invocation 2, and it names the integrated file; L160-162 admit the empty file beside the blocking file and no line files it; L275 makes the Rédacteur write a second one.
Finding: After the blocking-file row runs, the previous run's empty `questions-redacteur-NN.md` stays at the root beside the new one; when the new one holds a `### Q`, `/1_lexique` and `/2_structure` both stop on two files and no command files either — the route L384 recommends dead-ends until the Product Owner files by hand.
Owner: 2_structure.md
Follows: — (redacteur.md L275 writes the second file, 1_lexique.md L63 stops on it: both sides are present in the report and read as designed)

---

## TO FIX

### renommages F01 — `## Décision du Product Owner` is named to nobody who writes or reads it

Severity: TO FIX
Same as: chemins-aval F08 (8_code.md L566-568 ↔ cadreur.md L976-981)
Where: 8_code.md L566-572 (the heading, and the grep that counts archived files above the highest one carrying it) ↔ 8_code.md L748-759 (*What you relay*: lots passed and where the run stopped, "nothing else") ↔ 7_lots.md L318-323 (relays `## Ce qui revient` and "she decides", never the heading — line read here; neither report cites it) ↔ cadreur.md L976-981 (block C reads `code/redecoupage.md` "in full", never told the section is her instruction)
Verdict: confirmed — the heading occurs at 8_code.md L567 and L571 only, across every command and agent file (grep); 7_lots.md L322-323 stop at "she decides".
Finding: The count resets on a heading only the Product Owner can write and nothing names to her, so the count never resets and every return after the third stops at once (renommages); and the Cadreur, never told what the section is, may read her decision on a third return as history and make the same cut a fourth time (chemins-aval).
Owner: 8_code.md
Follows: 7_lots.md L318-323, cadreur.md L976-981

### fichiers F01 — The `<lot>:` commits and the `sheet`-cause revert disagree on what belongs to the lot

Severity: TO FIX
Same as: fichiers F02 (concepteur.md L281-285 ↔ 8_code.md L215-218, L406 ↔ audit_conventions.md L26-27), fichiers F03 (arbitre.md L401 ↔ realisateur.md L693-700 ↔ 8_code.md L215-218)
Where: 8_code.md L215-221 (step 1 reverts the lot's commits; step 2 deletes `fiche-executable.md`, `conception.md`, `tests.md`), L594-595 (four files at a split-back), L406 (move 7 globs `architecte/`) ↔ realisateur.md L695-700 (step 8 writes `compte-rendu.md`; step 9 stages "explicitly what belongs to the lot") ↔ concepteur.md L281-288 (stages "the request when you wrote one" under `<lot>:`) ↔ arbitre.md L401 (a platform trap is written into `CURRENT_TECHNICAL_STATE.md` mid-lot) ↔ detailleur.md L668-681 (grep on `**/compte-rendu.md`: a hit is "reuse it, never redeclare it") ↔ audit_conventions.md L26-27
Verdict: confirmed — `compte-rendu` occurs nowhere in 8_code.md (grep); L219-220 name three files; concepteur.md L282-284 and L287 read as reported.
Finding: Three sentences, none settled here. `code/<lot>/compte-rendu.md` is in neither the deletion list nor the staging rule, so whether it survives a revert depends on what the Réalisateur staged, and a survivor makes the Détailleur reuse a symbol the revert removed (F01). The Concepteur commits its `architecte/concepteur-<lot>.md` under the `<lot>:` message, so the revert deletes the request: a rule already in `TECHNICAL_CONVENTIONS.md` traces to nothing, and a request awaiting its verdict vanishes before move 6 globs for it (F02). A trap the Arbitre writes into the state document rides the Réalisateur's commit and is reverted with it, so the recoded lot meets the same red test and asks again (F03).
Owner: 8_code.md
Follows: realisateur.md L695-700, concepteur.md L281-288, arbitre.md L401, detailleur.md L668-681, audit_conventions.md L26-27

### passages F02 — `tests.md` has no field for a decision applied

Severity: TO FIX
Same as: —
Where: testeur.md L150-152 ("Say in your report that you applied it — the orchestration renames the file"), L56 (your report is `code/<lot>/tests.md`), L315-343 (the shape: `## Tests`, `## Criteria with no test`, `## Red`, `## Created`, `## Outside the lot`) ↔ 8_code.md L303-305 ("the concepteur in `## Decision applied` … the others in their report") · concepteur.md L311 (the field the Concepteur has)
Verdict: confirmed — the five headings at L318-343 carry no such field; *applied* occurs in testeur.md at L150 alone.
Finding: The line lands in a heading nothing reads or in the closing message, so the rename `/8_code` keys on never fires and the decision is applied again on every later run (8_code.md L299-301).
Owner: testeur.md
Follows: 8_code.md L303-305

### chemins-amont F02 — The rewrite route loses the genre decisions of a mixed file, and its `/1_lexique` leg lands on a stop

Severity: TO FIX
Same as: chemins-amont F17 (3a_genre.md L284 ↔ 1_lexique.md L56, L93-99)
Where: 3a_genre.md L284 (row: a `## Decision` names a rewrite → `/2_structure`, "then `/1_lexique` if the rewrite brought vocabulary, `/3_decoupe`, and back here"), L33-40 (the dispatch names `blocked_qualifieur.md` at its unnumbered name only) · 3b_nature.md L293-295 (same row, same leg) ↔ 2_structure.md L300-307 (renames the file to `blocked_<agent>-NN.md` after the Rédacteur), L384 ↔ redacteur.md L578-580 ("A decision that names a genre or a nature is not yours … the agent that blocked writes the line on its next run"), L275 · 1_lexique.md L56-59, L93-99
Verdict: confirmed on F02 — renamed by 2_structure.md L300-302, the file is no longer the one 3a_genre.md L38-40 names, and its genre decisions reach no Qualifieur. F17's mechanism is contradicted by redacteur.md L275: the Rédacteur writes `questions-redacteur-NN.md` at invocation 2 "even empty", so the root is not without a questions file and `/1_lexique` L57-59 stops on "invoke nothing, say `/2_structure`" — not on invocation 1 and `desc-produit.md`; the cost, a run spent on a stop that names the wrong next command, stands.
Finding: A `blocked_qualifieur.md` or `blocked_classeur.md` mixing a genre decision with a rewrite decision is routed to `/2_structure`, which renames it after a Rédacteur that applies rewrites alone, so the genre decisions are never read and the block re-blocks on the same question at the next `/3a_genre` (F02); and the same row's "`/1_lexique` if the rewrite brought vocabulary" spends a run on a stop (F17).
Owner: 3a_genre.md
Follows: 3b_nature.md L293-295, 2_structure.md L300-307, redacteur.md L578-580

### chemins-amont F03 — Once the first time is closed, a block a later answer creates or changes is never probed

Severity: TO FIX
Same as: —
Where: 4_grille.md L176-183 (the closure is the highest `questions-sondeur-NN.md` holding no `### Q`, tested "before the two marker greps"; empty → "the first time is closed, and the second time runs"), L128-134 (the `NEW` / `MODIFIED` greps belong to the first time's later turns), L319-321 (the second time runs once) ↔ 2_structure.md L382 ("a new block is split, classed and framed before the Convertisseur reads it") ↔ redacteur.md L132 (`convertisseur` answers strip the markers and mark what the turn touches)
Verdict: confirmed — L181-182 read as reported; no row reopens the first time on a marker once the highest sondeur file is empty.
Finding: A block a second-time or conversion answer creates or changes reaches `/5_reclasse` and the Convertisseur without pass A ever probing it, against the promise of 2_structure.md L382.
Owner: 4_grille.md
Follows: 2_structure.md L382, redacteur.md L132. The consumer side — `/5_reclasse`'s closure test, 4_grille.md L209-212 — is cited by neither report.

### chemins-amont F04 — The "latest questions file is answered" gate has no architecte exception

Severity: TO FIX
Same as: —
Where: 4_grille.md L102-106 (the gate: an entry with an empty `Answer:` and no `Défaut:` stops the run) ↔ 4_grille.md L224-228 and L235 (the exception, stated for the `### Q` guard and the filing only) ↔ conventions.md L84 (`/conventions` is the reader of that file) · architecte.md L546-548 (its `Answer:` line is written empty, never omitted)
Verdict: confirmed — L102-106 name no prefix, and the exception sits under *Git, before invoking* only.
Finding: A grid turn run after `/conventions` stops on the Architecte's unanswered file that only `/conventions` reads.
Owner: 4_grille.md
Follows: —

### chemins-amont F05 — Two rows match one nature, and only one of them gets the answer file

Severity: TO FIX
Same as: —
Where: 6_convertit.md L143-153 (the nature table, no first-match rule), L149 (technical file answered → runs, file named), L151 (part byte-identical, no technical file holding `^Answer:$` → runs, `questions-convertisseur-NN.md` named), L198-199 (that line goes "only to a nature the *part byte-identical, no answered technical file* row sent running"), L313-316 (a mark left after one rerun is a fault) ↔ convertisseur.md L502-512 (reads only the file the prompt names; never looks for it)
Verdict: confirmed — the only first-match rule in 6_convertit.md is L433, on the *What to run next* table; L198-199 read as reported.
Finding: A nature carrying `<<ASSUMED`, its part unchanged and its technical file answered, matches L149 and L151 at once; on a first-match reading the product answer is never handed over, the mark stays, and L313-316 declare a fault after one rerun.
Owner: 6_convertit.md
Follows: —

### chemins-amont F06 — The empty-architecte-file row is walked before invocation 4's

Severity: TO FIX
Same as: —
Where: conventions.md L73-74 ("Walk this table from the top and stop at the first row that matches"), L86 (empty `questions-architecte-NN.md` at the root → file it, say `/7_lots`), L88 (no `couverture.md` → invocation 4), L140-143 (the empty file "matches its row on the run right after the derivation and never again") ↔ 2_structure.md L246, L279-281 (`couverture.md` deleted on a rebuilt document, so that `/conventions` walks it at invocation 4)
Verdict: confirmed — L86 tests nothing about `couverture.md`, and precedes L88.
Finding: After `/2_structure` deleted `couverture.md`, the run files the leftover empty file and sends her to `/7_lots` without walking the rebuilt document — the Cadreur cuts on conventions that never saw it.
Owner: conventions.md
Follows: —

### chemins-amont F07 — `/fusion_compare`'s three gates miss the bug-fix pass, the plan and the report

Severity: TO FIX
Same as: chemins-amont F15 (fusion_compare.md L20-26 ↔ fusion.md L58, L64)
Where: fusion_compare.md L20-26 (three tests: `desc-produit-fusion.md` absent, `blocked_fusionneur.md` empty, `blocked_fusionneur.md` of invocation 2 or 3) ↔ fusion.md L62 (row 8: a `bugfix-*/` folder and no `questions-fusionneur-*` anywhere → invocation 3), L91-93 ("Row 8 fires once … its presence is what says the pass has run"), L58 and L64 (rows 4 and 10: `rapport-fusion.md`, `plan-fusion.md`)
Verdict: confirmed — L20-26 read as reported.
Finding: Run before `/fusion`'s bug-fix pass, `/fusion_compare` writes `questions-fusionneur-01.md` and row 8 can never fire again — invocation 3 never runs and the correction cycles' product decisions never reach the global (F07); with no row for `plan-fusion.md` or `rapport-fusion.md`, a re-run overwrites a plan whose answers wait at the root, or compares against a global the feature already merged into (F15).
Owner: fusion_compare.md
Follows: fusion.md L58-64, L91-93 (its rows key on files the compare writes)

### chemins-amont F08 — The blocking-file rename sits after the worktree is gone

Severity: TO FIX
Same as: —
Where: fusion_compare.md L150-156 (the five steps), L173-181 (the rename, after them) ↔ fusion_applique.md L143-154 (the rename "inside the worktree, before the steps below"; "done after it, the rename stays out of the merge and leaves the tree dirty for step 5")
Verdict: confirmed.
Finding: The rename is made in the main checkout outside the commit and the push — the placement `/fusion_applique` rules out in so many words; the split lost this half here alone.
Owner: fusion_compare.md
Follows: —

### chemins-aval F01 — A Relecteur block nobody acts on is retired by nobody, and two files disagree on who fills it

Severity: TO FIX
Same as: —
Where: 8_code.md L279-282 (4b excludes `code/<lot>/blocked_relecteur.md`: "its `## Decision` is empty by shape, nobody fills it"), L676-691 (the hand-back table: two act rows retire the file, two rows "relay it and stop"; L690-691 "the Product Owner fills `## Decision`, and the next `/8_code` picks it up") ↔ relecteur.md L262-269 ("Anything else it relays and stops, and the Product Owner writes under `## Decision`"), L325-335 (filled → "Apply it … the orchestration renames the file")
Verdict: confirmed — L280 against relecteur.md L268-269 and L331; the rename of L277 reaches the Relecteur's file only "when *Where you stop and hand back* sends you here", which the two act rows alone do (L681-683).
Finding: A Relecteur block on the two "relay and stop" rows is retired by nobody while the Relecteur's PART 2 stops on the unnumbered file at every later run, so the lot can never be reviewed again; and the two files disagree on whether the Product Owner fills its `## Decision`, a filled one being named in no prompt and renamed by no rule.
Owner: 8_code.md
Follows: relecteur.md L262-269, L331-335

### chemins-aval F02 — A cold re-entry after a `sheet` revert reaches move 1 with no findings

Severity: TO FIX
Same as: —
Where: 8_code.md L129 (no `fiche-executable.md` → `detailleur` on the block, plain), L67-79 (*Where to resume* reads no verdict's `## Cause`) ↔ 8_code.md L222-226 (step 3 of the `sheet` path: `Findings:` in the prompt), L350-361 (the prompt form, "after a `sheet` FAIL — see move 4"), L376-379 (`## Findings` read only to copy it there)
Verdict: confirmed — *Findings* occurs in 8_code.md at L192, L224, L360 and L378, all under move 4; move 1 keys on the missing sheet alone.
Finding: A re-entry after a `sheet` cause whose Détailleur step did not finish invokes the Détailleur blind — the sheet is rewritten with the same fault and the remaining attempts are burnt on it.
Owner: 8_code.md
Follows: —

### chemins-aval F03 — A block raised in the run that applied a decision is archived as settled

Severity: TO FIX
Same as: —
Where: 8_code.md L277 (rename "once the agent reports having applied it"; 4b's tests at L274-276 run before invoking only) ↔ detailleur.md L311 (writes `code/blocked_detailleur.md`) and realisateur.md L262 (writes `code/<lot>/blocked_realisateur.md`), neither with a rule on a file already holding a filled `## Decision` · 7_lots.md L177-180 (the rule, for the Cadreur's file: appended below, "the file stays at its unnumbered name")
Verdict: confirmed — a grep of *append* / *below the filled* / *fresh block* in detailleur.md, realisateur.md and 8_code.md returns nothing on these files (arbitre.md L215 is on `code/redecoupage.md`); 8_code.md re-tests nothing after the report.
Finding: The new block is written into the same unnumbered file, the command renames it on the "applied" report, and the block vanishes as settled.
Owner: 8_code.md
Follows: detailleur.md L311, realisateur.md L262, arbitre.md (the writer of the numbered `## Decision`)

### chemins-aval F04 — `## Redécoupage: archivable` survives the archive it triggered

Severity: TO FIX
Same as: —
Where: 7_lots.md L115-127 (grep the line in `code/sequence.md` → `git mv code/redecoupage.md`; "that line, read from the file, is the trigger") ↔ verificateur.md L97-100, L501-503 (writes it on a redécoupage whose `## Defects` is empty; "you write over" `sequence.md`, L126) ↔ cadreur.md L925-926 (a third-round block goes out before the Vérificateur is called — the side neither report cites by line)
Verdict: confirmed — no line in 7_lots.md, cadreur.md or verificateur.md clears the line; only a Vérificateur run overwrites the file.
Finding: A later redécoupage where the Cadreur goes out before calling the Vérificateur still finds the line and archives the fresh `code/redecoupage.md` unsplit — the second dispatch never reaches block C, the Réalisateur reads the file as gone and codes against the split that was sent back.
Owner: 7_lots.md
Follows: verificateur.md L501-503, cadreur.md L1036 (relays the line)

### chemins-aval F05 — The multi-lot revert has no order across lots

Severity: TO FIX
Same as: —
Where: 8_code.md L579-587 ("every lot with no PASS … the `git log` list of move 3 per lot, cut after that lot's last revert, newest first"; a conflict stops the command), L236-241 (a `sheet` cause on a non-last lot takes the later lots down the same way) ↔ testeur.md L283-288 (`code/recette.md` is "appended, never rewritten: every lot of the split adds to it") · realisateur.md L693 (step 7 updates `docs/CURRENT_TECHNICAL_STATE.md` — the second shared file, cited by the report without a line)
Verdict: confirmed.
Finding: Reverting an older lot's commits before a newer lot's conflicts on the two shared files and stops the command — a conflict a global newest-first order would not produce.
Owner: 8_code.md
Follows: —

### chemins-aval F06 — Step 1 of the closing sequence lists no file outside the feature folder

Severity: TO FIX
Same as: —
Where: 8_code.md L720-724 (what is still uncommitted: "the sheets, the verdicts, every blocking file and the renames of 4b") ↔ architecte.md L4 (`tools:` without Bash — the report cites L15, the role line) · arbitre.md L401 (trap into `CURRENT_TECHNICAL_STATE.md`), L478 (its Bash runs the poll and nothing else)
Verdict: confirmed — `TECHNICAL_CONVENTIONS` and `couverture` occur nowhere in 8_code.md (grep). Step 1's `git add` carries no path; the gap is in the enumeration a reader stages from.
Finding: A `git add` scoped like the pre-code commit (L97) leaves the tree dirty and step 5 refuses the remove — the run ends on "say what is left there, and stop".
Owner: 8_code.md
Follows: —

---

## QUESTION

### fichiers F04 — Nothing resets `Round:` after a third-round decision

Severity: QUESTION
Same as: chemins-aval F07 (cadreur.md L919-926 ↔ verificateur.md L121-126)
Where: cadreur.md L919-926 ("Three rounds at most … the count is the round number the Vérificateur writes … still carrying defects at the third: write `code/blocked_cadreur.md`") ↔ verificateur.md L121-126 (`Round:` is the previous number plus one when the previous `## Defects` carried lines)
Verdict: —
Finding: After a third-round `blocked_cadreur.md` and a filled decision, the next Vérificateur writes `Round: 4` and the Cadreur blocks again on the first round still carrying defects — one round instead of three after every decision (fichiers); whether round 4 with defects corrects again or blocks again is unwritten, and a decision never buys the fresh rounds it would need (chemins-aval). The two sentences agree.
Owner: cadreur.md
Follows: verificateur.md L121-126

---

## NOTE

### renommages F02 — Two routes for a missing form

Severity: NOTE
Same as: —
Where: GRILLE_CONVENTIONS.md L50-52 (`R4` → a conventions request in `architecte/`) ↔ architecte.md L300-301, L564-568 (→ a `Kind: forme` question in `questions-architecte-NN.md`)
Verdict: —
Finding: An Architecte following the grid it reads files a request its own invocation 3 would then settle as a rule.
Owner: GRILLE_CONVENTIONS.md
Follows: —

### renommages F03 — `Cause: sheet` spelt as a line where every reader expects a heading

Severity: NOTE
Same as: —
Where: relecteur.md L363 ↔ relecteur.md L160-162 (the verdict template: `## Cause`, `sheet` under it), 8_code.md L211 (reads "a verdict whose `## Cause` reads `sheet`")
Verdict: —
Finding: A Relecteur writing the line as L363 spells it produces a cause `/8_code` never matches, and the sheet route never fires.
Owner: relecteur.md
Follows: —

### renommages F04 — "`/cycle` ne l'appelle pas" survives in the two process documents

Severity: NOTE
Same as: —
Where: PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010
Verdict: stale — *Settled*, rows « `/cycle` is deleted » and « `PROCESS_AMONT.md` and `PROCESS_AVAL.md` are out of date by decision ».
Finding: The one occurrence of the removed command name under `docs-new/`, reported as the surviving occurrence the sweep asks for.
Owner: —
Follows: —

### renommages F05 — Three commands sit in no row of the orchestrator's table

Severity: NOTE
Same as: —
Where: CLAUDE.md L51-57 (the command table), L62 ("anything else is an ordinary request") ↔ audit_blocages.md L1, audit_conventions.md L1, deploie.md L1
Verdict: —
Finding: A run of `/audit_blocages`, `/audit_conventions` or `/deploie` is one the orchestrator's own rules tell it to treat as no workflow.
Owner: CLAUDE.md
Follows: —

### fichiers F05 — `releve.md` is archived for nobody

Severity: NOTE
Same as: —
Where: sondeur.md L230-231 (the global sondeur writes it and reads it for its pass B) ↔ 4_grille.md L450, L256-260 (archived into `closed/`, no later reader named)
Verdict: —
Finding: Every turn archives a file nobody opens.
Owner: 4_grille.md
Follows: sondeur.md L230-231

### passages F03 — One decision per line, and a decision that spans several

Severity: NOTE
Same as: —
Where: 9_controle.md L404 (`decisions-produit.md`: one decision per line, identifier first, "nothing before the identifier: the Rédacteur greps it") ↔ arbitre.md L152 (a `## Decision` is three parts on several lines) ↔ redacteur.md L749 (reads a line "as written", no rule for the ones that follow)
Verdict: —
Finding: A decision copied "as written" spreads over lines whose continuations open on no identifier, and the Rédacteur has no rule for them.
Owner: 9_controle.md
Follows: redacteur.md L749, arbitre.md L152

### chemins-amont F09 — A stop-path pointer names three steps out of five

Severity: NOTE
Same as: —
Where: 3b_nature.md L221 ("merge, push, remove the worktree") ↔ 3b_nature.md L253-263 (the five steps) · 3a_genre.md L219 ("the five steps")
Verdict: —
Finding: Read literally it skips the commit inside the worktree, and the merge carries nothing.
Owner: 3b_nature.md
Follows: —

### chemins-amont F10 — A `Clarification needed` flag with no questions file bounces for ever

Severity: NOTE
Same as: —
Where: 3_decoupe.md L47-50 (one hit → stop, "`/2_structure` has to run first"; the same in 3a_genre.md L49-52, 3b_nature.md L48-51, 4_grille.md L81-84) ↔ 2_structure.md L150 (no questions file and a `desc-produit.md` → stop, "`/3_decoupe` comes next")
Verdict: —
Finding: No row lifts the flag, and the two commands send the Product Owner to each other.
Owner: 2_structure.md
Follows: 3_decoupe.md L47-50, 3a_genre.md L49-52, 3b_nature.md L48-51, 4_grille.md L81-84

### chemins-amont F11 — A feature-level question blocks a `bugfix-NN` request

Severity: NOTE
Same as: —
Where: conventions.md L68-69 (stop on an unanswered root `questions-architecte-*.md`, before the walk) ↔ conventions.md L26-27, L83 (invocation 3 for a `bugfix-NN` needs neither the document nor that answer)
Verdict: —
Finding: The stop precedes the walk, so an invocation 3 that needs no answer is blocked by one.
Owner: conventions.md
Follows: —

### chemins-amont F12 — Four opus sondeurs on an empty list

Severity: NOTE
Same as: —
Where: 4_grille.md L120-126 (first turn: "every behaviour block") ↔ sondeur.md L53 · 3a_genre.md L125-128, 3b_nature.md L127-130 (invoke nothing on an empty list)
Verdict: —
Finding: A feature with no `Genre: comportement` block has no written outcome, and four opus sondeurs run on nothing.
Owner: 4_grille.md
Follows: —

### chemins-amont F13 — The *Otherwise → assembly* row runs on nothing, and on a nature that waits

Severity: NOTE
Same as: chemins-amont F18 (6_convertit.md L174 ↔ 6_convertit.md L230-233, L433-436)
Where: 6_convertit.md L174-175 (the *Otherwise* row: skip to the assembly), L145 (a part with no block: section written empty), L230-233 (the assembly runs when every nature with blocks has its file), L433-436 (assume a waiting nature makes the assembly write nothing) ↔ 5_reclasse.md L134-137 ↔ fusionneur.md L83-86
Verdict: —
Finding: A feature whose blocks are all `directive` or `hors périmètre` stops nowhere upstream — an empty technical document, a conventions walk and a split on nothing, and at `INIT` a global of empty sections the next compare no longer reads as `# Application` alone (F13); a nature waiting on a technical answer with its `assumed` section written keeps its `<nature>.md`, so the assembly and invocation 2 run on every re-run while it waits, where L433-436 assume they write nothing (F18). Two defects of one row; both reported, neither settled.
Owner: 6_convertit.md
Follows: 5_reclasse.md L134-137, fusionneur.md L83-86

### chemins-amont F14 — The `### Q` guard stops on the Fusionneur's own integrated file

Severity: NOTE
Same as: —
Where: fusion_compare.md L50-56 ↔ fusion.md L153-154 (only `/fusion` files the bug-fix pass's answered file)
Verdict: —
Finding: After a bug-fix pass, `/fusion_compare` stops on an integrated file and reports it as never integrated.
Owner: fusion_compare.md
Follows: —

### chemins-amont F16 — `/fusion` files other agents' root files without the `### Q` guard

Severity: NOTE
Same as: —
Where: fusion.md L140-144 ↔ 3_decoupe.md L52-58 (the guard every other command carries)
Verdict: —
Finding: An answered but unintegrated file at the root is put away and its answers lost for good.
Owner: fusion.md
Follows: —

### chemins-aval F09 — The walk stops the block on its own PASSed lots

Severity: NOTE
Same as: —
Where: detailleur.md L501-503 (greps every lot's produced symbol, coded lots included) ↔ detailleur.md L115-117 ("a production that already exists" stops the block), L512 (the exemption, stated for the sheet alone)
Verdict: —
Finding: Every re-entry on a partly coded block — a `sheet` re-detail, a decision applied late — blocks on its own PASSed lots unless the agent infers an exemption.
Owner: detailleur.md
Follows: —

### chemins-aval F10 — *Where to resume* has no row for a PASSed lot with a filled decision, nor for a revert conflict

Severity: NOTE
Same as: chemins-aval F12 (8_code.md L216-218 ↔ 8_code.md L71-74)
Where: 8_code.md L71-74 (the next lot is the first with no PASS) ↔ L695-698 ("even on a lot already carrying a PASS") · L216-218 (a conflict stops the command, `git revert --abort`, "resolve nothing")
Verdict: —
Finding: The promised re-run on a PASSed lot has no trigger, and a decision filled late on such a lot is never seen (F10); a revert conflict stops the command with nothing changed on disk, so every re-run re-enters the same `sheet` path and hits the same conflict, and no row says how the Product Owner unblocks the lot (F12). Placed here and not in entry 4: its defect is the missing resume row, not what the revert removes.
Owner: 8_code.md
Follows: —

### chemins-aval F11 — The hand-back table has no first-match rule

Severity: NOTE
Same as: —
Where: 7_lots.md L165 (row 1: `## Defects` carries no line → "the split holds") ↔ 7_lots.md L172 (`code/blocked_verificateur.md` → stop)
Verdict: —
Finding: A Vérificateur block leaves the previous `code/sequence.md` untouched with its empty `## Defects`, so row 1 matches too, the run reports "the split holds" and invokes the Architecte — `/8_code` L85 catches it one command later.
Owner: 7_lots.md
Follows: —

### chemins-aval F13 — Three empty attempts leave nothing on disk

Severity: NOTE
Same as: —
Where: 8_code.md L253-255 ↔ 8_code.md L259-261 (the disk count exists to prevent "retried three times per run for ever"), L706 (the stop has no last verdict to relay)
Verdict: —
Finding: The cap holds in one run only, and the next run repeats the three.
Owner: 8_code.md
Follows: —

### chemins-aval F14 — Move 2 never skips the Réalisateur on its report

Severity: NOTE
Same as: —
Where: 8_code.md L138-140 (the Concepteur and the Testeur are skipped on `conception.md` and `tests.md`) ↔ 8_code.md L184-188 (the empty-attempt rule)
Verdict: —
Finding: A lot coded but not reviewed re-runs the Réalisateur as a first run; if it commits nothing, the empty-attempt rule withholds the Relecteur and three such runs stop the lot on the Product Owner.
Owner: 8_code.md
Follows: —

### chemins-aval F15 — The ownership list omits the Concepteur and the Testeur

Severity: NOTE
Same as: —
Where: audit_blocages.md L107-109 ↔ concepteur.md L12
Verdict: —
Finding: A Réalisateur block asking for a declaration or a test cannot be classified as reaching outside its author.
Owner: audit_blocages.md
Follows: —

### chemins-aval F16 — Finding 7 reads `desc-bug.md` anchors against a `spec-technique.md` coverage

Severity: NOTE
Same as: —
Where: audit_conventions.md L144-145 ↔ audit_conventions.md L53-57
Verdict: —
Finding: On a correction cycle every rule reads as "never met" and the heading fills with noise.
Owner: audit_conventions.md
Follows: —

### chemins-aval F17 — Gap identifiers are positional

Severity: NOTE
Same as: —
Where: diagnostique.md L37 ↔ diagnostiqueur.md L80-81, L194-198
Verdict: —
Finding: A gap the Product Owner inserts into `bug-list.md` between two runs shifts them: an existing `investigation/G02.md` is skipped for a gap it does not describe, and invocation 2 blocks on a mismatch no decision can lift.
Owner: diagnostique.md
Follows: diagnostiqueur.md L80-81, L194-198

---

48 findings in, 40 entries out (7 merges absorbed 8 findings).
19 BLOCKING and TO FIX verified at their lines: 19 `confirmed`, 0 `wrong`, 0 `overstated`; one merged NOTE half (chemins-amont F17) has its mechanism contradicted by redacteur.md L275, its cost standing.
1 `stale` (renommages F04, by the *Settled* table).
