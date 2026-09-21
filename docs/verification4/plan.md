# Vérification 4 — plan

Source: `docs/verification4/consolide.md`, 40 entries. Every file a `Where` names was opened at the lines named, on every side, before any decision below — except entry 22, whose two files sit in `docs/process/` and are not opened by this session. Line numbers are the ones read under `.claude-new/` (and `docs-new/process/` for entry 20) before the chain moved — a `Where` naming `.claude-new/` or `docs-new/` is read as `.claude/` or `docs/`; where they differ from the consolidated report, the ones read are given.

Three rules of this plan:

- A `Decision` says what changes and in which file, never the wording. The agent that applies it writes the prose.
- Entries whose fix turned on intent, scope or what the Product Owner sees carried `Decision: —` and sat in `## To settle` at the end, with what each option costs; four entries (1, 4, 29, 34) carried a decision on their mechanical part and a residual question there. 📌 **All nine items were settled on 2026-09-21** — each entry's `Decision` now carries the settled part, and `## To settle` keeps the options for the record.
- Decisions of `docs/verification3/plan.md` stand. Where an entry touches one, the entry says how it fits; none reverses one.

Entries marked `Same as` in the consolidated report got one decision each (3, 4, 6, 11, 19, 30, 34). Every entry whose `Where` names two files appeared in one report only — the consolidation opened both sides, and this plan opened them again; that is said once here and holds for all of them. Entry 22 is the one whose sides stay unopened.

`Cited` quotes the line from the side the owner does not hold. On an entry whose `Where` names one file, it quotes the line the decision rests on.

---

## BLOCKING

### 1 · passages F01 — The Concepteur has no rule on the `created` / `modified` mark

Severity: BLOCKING
Decision: In `concepteur.md`, move 1 (L190-191) reads each symbol's mark beside its signature; a `modified` symbol is edited in place — the existing declaration, found by the grep of L76-78, takes the sheet's signature — and is neither declared beside the old one nor read as a taken name (L78) or a duplicate (L176-179); `## Declared` (L301-304) carries the mark per symbol as the Réalisateur's `## Symbols` does. The body: item A settled, Option 1 — a declaration the lot marks `modified` loses its existing body to the same *not implemented* throw as a new one, and nothing carries the old body forward; one sentence in `concepteur.md` beside L17-18 or L106-107, which say every body throws but not of a body that already exists. The earlier tests of that symbol turn red in its module and the Réalisateur runs « until both pass » (testeur.md L244-245, realisateur.md L665-669), so the earlier behaviour stays a constraint with the earlier test as its specification.
Where: detailleur.md L267-271 ↔ concepteur.md L190-191, L236-245, L76-78, L176-179 (relecteur.md L370-381, cadreur.md L422-423)
Cited: detailleur.md L267-268 — "🔴 **Every symbol of `## Signatures` opens with its mark — `created` or `modified`** — 📌 **copied from the lot's `Produces` or `Modifies`**, one mark per symbol." · relecteur.md L381 — "a symbol the sheet marks *modified* that the report declares *created* was written beside the old one, not in its place" · testeur.md L272 — "| **A signature `## Signatures` marks *modified*** | 📌 **Adapt the test to the new signature** — 🔴 **that is the lot doing its work**"
Owner: concepteur.md
Follows: — (detailleur.md L267 defines the mark, relecteur.md L376-382 and testeur.md L272 already read it; a grep of *modif* in concepteur.md returns nothing — verified)
Note: the Testeur's L272 already expects the Concepteur to change a modified declaration's signature in place — the decision writes what its neighbours assume.

### 2 · chemins-amont F01 — A filled blocking file beside an empty questions file leaves two files at the root

Severity: BLOCKING
Decision: In `2_structure.md`, invocation 2 on the blocking-file row (L146) files the empty `questions-<agent>-NN.md` that L160-162 admit beside the blocking file, into `questions/<agent>/` by the same `git mv` as L313-316, inside the worktree before the merge — so the Rédacteur's new file is the only one at the root; `questions-architecte-*.md` stays excepted (L317-319).
Where: 2_structure.md L143-162, L313-319, L384-386 ↔ redacteur.md L275-277 ↔ 1_lexique.md L63, 2_structure.md L145
Cited: redacteur.md L275-277 — "🔴 **Write it at invocations 1 and 2, even empty** — ⚠️ **an empty one says nothing waits on an answer and the chain moves on; a missing one says you did not run.**" · 1_lexique.md L63 — "| Two files of other agents | 🔴 **Stop** — a filing failed; say which files |"
Owner: 2_structure.md
Follows: — (the Rédacteur keeps writing its file; the stops of 1_lexique.md L63 and 2_structure.md L145 stay)
Note: fits verification 3's entry 5+6 — the row order it fixed stays; this adds the filing the blocking-file row lacked. Read with entry 27 (same owner) — different rows, no collision.

---

## TO FIX

### 3 · renommages F01 — `## Décision du Product Owner` is named to nobody who writes or reads it

Severity: TO FIX
Decision: In `8_code.md`, the third-return stop (L552-554) and *What you relay* (L750-759) tell the Product Owner what L566-568 keys on — her decision goes into `code/redecoupage.md` under `## Décision du Product Owner`, then `/7_lots` by hand. `7_lots.md` L318-323 says the same on a third return, and `cadreur.md` block C (L976-981) names that section as her instruction, binding on the cut it makes.
Where: 8_code.md L552-554, L566-573, L750-759 ↔ 7_lots.md L318-323 ↔ cadreur.md L976-981
Cited: 7_lots.md L322-323 — "⚠️ **A third return says the split is not the problem the split can solve**, and she decides." · cadreur.md L980-981 — "**Read it in full**, and 🔴 **read every `code/redecoupage-NN.md` beside it** — those are the times the split was already sent back."
Owner: 8_code.md
Follows: 7_lots.md L318-323, cadreur.md L976-981
Note: the heading occurs at 8_code.md L567 and L571 only, across every command and agent file (grep, verified). This is the "what resets the count" verification 3's item D asked for — the mechanism stands; the entry names it to its writer and its reader.

### 4 · fichiers F01 — The `<lot>:` commits and the `sheet`-cause revert disagree on what belongs to the lot

Severity: TO FIX
Decision: In `8_code.md`: (F01) `code/<lot>/compte-rendu.md` joins the deletion lists at L219-221, L238 and L593-594. (F02) the requests of `architecte/` are the command's to commit, never a lot's — L114-123 and both step-1 enumerations (L608-610, L720-724) name `architecte/` among what the command stages; `concepteur.md` L283-284 drops "the request when you wrote one" from what the Concepteur stages, `realisateur.md` L698 the same for its own request — a request then rides no `<lot>:` commit, and no revert removes it. (F03, the Arbitre's trap) item B settled, Option 2 — in `realisateur.md`, at the step where it calls the Arbitre: right after the Arbitre returns and before the Réalisateur resumes its own steps, it commits `CURRENT_TECHNICAL_STATE.md` alone, under a message that does not begin with `<lot>: ` — the revert list is built by the `^<lot>: ` grep of the log (8_code.md L162-174, reused L215-217 and L582-584), so no revert removes the trap. Owner of that part: realisateur.md; follows none — step 9 already puts the file in the lot's diff.
Where: 8_code.md L215-221, L236-238, L593-594, L608-610, L720-724 ↔ realisateur.md L695-700 ↔ concepteur.md L281-288 ↔ arbitre.md L401 ↔ detailleur.md L668-682 ↔ audit_conventions.md L26-27
Cited: concepteur.md L281-285 — "**5. Commit.** 🔴 **`git status` first** — 📌 **it says what the worktree holds**, and you stage explicitly what belongs to the lot: the declarations, the files the module needed, `code/<lot>/conception.md` and the request when you wrote one" · realisateur.md L698 — "**9. Commit**, staging explicitly what belongs to the lot." · detailleur.md L681 — "| A hit | An earlier lot of this cycle created it — **reuse it, never redeclare it** |" · arbitre.md L401 — "| **A platform trap nobody could guess before a red test** | 🔴 **`CURRENT_TECHNICAL_STATE.md`** — 📌 **write it there yourself**, and settle the block with it |"
Owner: 8_code.md (F01, F02) · realisateur.md (F03)
Follows: concepteur.md L283-284, realisateur.md L698 (their staging lists); 7_lots.md L277-282 (its step 1 commits the Architecte's verdicts on `architecte/` — same enumeration)
Note: `compte-rendu` occurs nowhere in 8_code.md (grep, verified). Read with entries 17 and 18 (same paragraphs): 17 orders the reverts, 18 enumerates the closing commit — one edit of L608-610 and L720-724 serves 4 and 18. The non-last-lot paragraph L232-242 is verification 3's item C, Option 1, already written — this entry adds a file to its list and changes nothing else of it.

### 5 · passages F02 — `tests.md` has no field for a decision applied

Severity: TO FIX
Decision: In `testeur.md`, `tests.md` (L318-343) gains a `## Decision applied` field with the Concepteur's meaning (concepteur.md L311-313, L329-335) — the blocking file named, or a dash — and L150-152 points to it. `8_code.md` L59-60 and L303-305 name that field for the Testeur, and the Réalisateur's `## What governed the code, besides the sheet` (realisateur.md L177-181, L197-203) as the third.
Where: testeur.md L150-152, L56, L318-343 ↔ 8_code.md L59-60, L303-305 (concepteur.md L311-313)
Cited: 8_code.md L303-305 — "📌 **Where the agent says it applied the decision**: 🔴 **the concepteur in the `## Decision applied` field of `code/<lot>/conception.md`** — a dash there is no application; **the others in their report.**"
Owner: testeur.md
Follows: 8_code.md L59-60, L303-305
Note: *applied* occurs in testeur.md at L150 alone (verified). Read with entry 15 (the rename this field triggers) — compatible.

### 6 · chemins-amont F02 — The rewrite route loses the genre decisions of a mixed file, and its `/1_lexique` leg lands on a stop

Severity: TO FIX
Decision: In `3a_genre.md`, row L284 says two things: the `/2_structure` route holds when every `## Decision` of the file names a rewrite — a file mixing genre decisions and rewrites runs `/3a_genre` first, whose Qualifieur writes the genres and leaves the file unnumbered for `/2_structure` (the rule L200-205 already carry); and the `/1_lexique` leg goes — after `/2_structure` the next step is `/3_decoupe` (2_structure.md L382), the Lexicographe having nothing to watch on a rewrite. `3b_nature.md` L295 the same, for the Classeur's file. The sentence verification 3's item J put in that row stays.
Where: 3a_genre.md L284, L34-40, L200-205 · 3b_nature.md L295 ↔ 2_structure.md L300-307, L382 ↔ redacteur.md L577-580, L275 · 1_lexique.md L59, L93-99
Cited: redacteur.md L577-580 — "⚠️ **A decision that names a genre or a nature is not yours**: the block it concerns you leave as it stands — the agent that blocked writes the line on its next run." · 2_structure.md L300-302 — "🔴 **A `blocked_decoupeur.md`, `blocked_qualifieur.md` or `blocked_classeur.md` it applied is renamed** — `blocked_<agent>-NN.md`" · 1_lexique.md L59 — "| Another agent's questions file alone, **with no `### Q`** | 🔴 **Invoke nothing** — 📌 **nothing to watch**; say `/2_structure` |"
Owner: 3a_genre.md
Follows: 3b_nature.md L295
Note: F17's mechanism as consolidated — redacteur.md L275 writes an empty file, so `/1_lexique` stops at L59, not at L93-99 — holds on reading; the cost is the same, and dropping the leg settles both readings. 2_structure.md and redacteur.md change nothing: the order "genres first, rename after the rewrite" is what L200-205 and L300-307 already describe.

### 7 · chemins-amont F03 — Once the first time is closed, a block a later answer creates or changes is never probed

Severity: TO FIX
Decision: Item C settled, Option 1 — in `4_grille.md`, the turn that closes the first time (the one whose highest `questions-sondeur-NN.md` comes back empty) strips a trailing `NEW` or `MODIFIED` from the `### B` heading lines of `desc-produit.md` — a command editing the product file without an agent, as `/5_reclasse` already does when it copies (5_reclasse.md L182-183). The closure test becomes two-part: the highest sondeur file empty *and* no marker on any heading; a marker found beside an empty sondeur file reopens the first time, on the marked blocks alone. One sentence on the case that stays open: on an integration from `idees.md` or from the existant the Rédacteur does not strip (redacteur.md L598-599, *only when*), so markers of an earlier turn can survive and reopen the first time on blocks already probed — probing twice is the accepted side. No reader of the markers follows: every reader sits before `/4_grille` in the turn, `/5_reclasse` strips them, the Contrôleur ignores them (L70-72), `/6_convertit` compares bytes (L158-161).
Where: 4_grille.md L176-183, L128-134, L191-195, L311-321 ↔ 2_structure.md L382 ↔ redacteur.md L126-134
Cited: 2_structure.md L382 — "| Its questions file is empty | 📌 `/3_decoupe` — 🔴 a new block is split, classed and framed before the Convertisseur reads it |" · redacteur.md L132 — "| `sondeur`, `existant` | 🔴 **The grid** — 📌 **strip them all**, then mark what this turn touches |"
Owner: 4_grille.md
Follows: 5_reclasse.md L50-62 (the closure it tests — aligned on the two-part test); every other file that tests closure, swept (3_decoupe.md L84 tests only that the grid ran once — no change). 2_structure.md L382's promise now holds unchanged.
Note: both sides verified; the defect stands. No reopen rule survives the trap L191-195 name — the markers of the closing turn are stripped by nobody, so "highest sondeur file empty and a marker present" is also the state a closed grid rests in — and every candidate fix either lets a command edit the product file or accepts the hole. Intent → `## To settle`, item C.

### 8 · chemins-amont F04 — The "latest questions file is answered" gate has no architecte exception

Severity: TO FIX
Decision: In `4_grille.md`, the gate at L102-106 excludes `questions-architecte-*.md`, as the `### Q` guard (L218-228) and the filing (L235-237) do — that file is `/conventions`'s row L84.
Where: 4_grille.md L102-106 ↔ L218-228, L235-237 ↔ conventions.md L84 (architecte.md L548-549)
Cited: conventions.md L84 — "| A `questions-architecte-NN.md` at the root with an empty `Answer:` | 🔴 **Nothing** — say which questions wait |" · architecte.md L548-549 — "🔴 **The `Answer:` line is written empty, and never omitted** — it is where the Product Owner writes, by hand."
Owner: 4_grille.md
Follows: —
Note: the gate exists in 4_grille.md alone (grep of *latest questions file* across commands, verified). Same exception as verification 3's entry 17, one paragraph further up.

### 9 · chemins-amont F05 — Two rows match one nature, and only one of them gets the answer file

Severity: TO FIX
Decision: In `6_convertit.md`, the nature table (L143-153) says how several matching rows combine: a nature runs once when any *Runs* row matches it, and its prompt carries the line of every row that matched — the answered technical file of L149, the `questions-convertisseur-NN.md` of L151, the decision of L152; L198-202 says so instead of "only to a nature the byte-identical row sent running".
Where: 6_convertit.md L143-153, L198-202, L313-318 ↔ convertisseur.md L503-507
Cited: convertisseur.md L503-507 — "🔴 **The prompt names the questions file you wrote last turn**, its `Answer:` lines filled, 📌 **when its answers changed no block** — ⚠️ **and only then** … 🔴 **You never look for it yourself.**"
Owner: 6_convertit.md
Follows: — (the Convertisseur reads what the prompt names, which is verification 3's item B, Option 1 — unchanged)
Note: the only first-match rule in 6_convertit.md is L433, on the relay table (verified). Read with entry 30 (same owner) — different tables.

### 10 · chemins-amont F06 — The empty-architecte-file row is walked before invocation 4's

Severity: TO FIX
Decision: In `conventions.md`, the empty-file row (L86) moves below the two `couverture.md` rows (L88-89): a missing `couverture.md` sends the run to invocation 4 first, and the leftover empty file is filed by *Git, before invoking* (L140-147) on that same run.
Where: conventions.md L75-76, L86, L88-89, L140-147 ↔ 2_structure.md L246, L279-281
Cited: 2_structure.md L278-281 — "🔴 **And a `couverture.md` left behind says the feature was walked** — ⚠️ `/conventions` then finds nothing to do, instead of walking the rebuilt document at its invocation 4."
Owner: conventions.md
Follows: —
Note: verification 3's entry 21 (the filing at L140-147) stands — after the move, that filing is what retires the leftover on the invocation-4 run, and row L86 still matches once, on the run right after a derivation. Read with entry 28 (same table) — compatible.

### 11 · chemins-amont F07 — `/fusion_compare`'s three gates miss the bug-fix pass, the plan and the report

Severity: TO FIX
Decision: In `fusion_compare.md`, the *Before anything else* table (L20-26) gains three tests, walked in this order after the three it has: `rapport-fusion.md` exists → stop, the merge is done (fusion.md row 4); `plan-fusion.md` exists → stop, say `/fusion_applique` (row 10); a `bugfix-*/` folder and no `questions-fusionneur-*` anywhere → stop, say `/fusion` (row 8's pass has not run).
Where: fusion_compare.md L20-26 ↔ fusion.md L58, L62, L64, L91-93
Cited: fusion.md L62 — "| 8 | A `bugfix-*/` folder, and no `questions-fusionneur-*` anywhere | **Fusionneur, invocation 3** |" · L91-93 — "📌 **Row 8 fires once.** The Fusionneur writes a questions file even when empty, and its presence is what says the pass has run — the `bugfix-*/` folders never go away."
Owner: fusion_compare.md
Follows: — (`/fusion`'s rows key on the same files, unchanged)
Note: read with entries 12 and 31 (same owner) — three different sections.

### 12 · chemins-amont F08 — The blocking-file rename sits after the worktree is gone

Severity: TO FIX
Decision: In `fusion_compare.md`, the rename (L173-181) moves above the five steps (L149-160), inside the worktree, with the reason `fusion_applique.md` L152-154 gives.
Where: fusion_compare.md L149-160, L173-181 ↔ fusion_applique.md L144-154
Cited: fusion_applique.md L152-154 — "📌 **Step 1 carries the rename into the commit** — ⚠️ **done after it, the rename stays out of the merge and leaves the tree dirty for step 5.**"
Owner: fusion_compare.md
Follows: —

### 13 · chemins-aval F01 — A Relecteur block nobody acts on is retired by nobody, and two files disagree on who fills it

Severity: TO FIX
Decision: In `8_code.md`, the hand-back table (L672-681) retires the Relecteur's file on every row: on the two act rows as now; on the `conception.md` / `tests.md` row, the next run renames it before invoking the Relecteur once move 2 has produced the missing file — the act is move 2's; on *anything else*, the Product Owner fills `## Decision` (L687-688, as relecteur.md L268-269 says), the Relecteur's prompt (L509-516) carries a `Plus:` line naming the filled file, and it is renamed once the Relecteur reports having applied it (relecteur.md L332). L279-282 then says the file is out of 4b's rows because this table handles it, not because nobody fills it.
Where: 8_code.md L279-282, L672-691, L509-516 ↔ relecteur.md L264-269, L295-298, L324-337
Cited: relecteur.md L268-269 — "🔴 **Anything else it relays and stops**, and the Product Owner writes under `## Decision`." · L332 — "| A `## Decision` filled | 📌 **Apply it, and say in your closing message that you did** — 🔴 **the orchestration renames the file** |"
Owner: 8_code.md
Follows: — (relecteur.md already reads both cases; 4b keeps excluding the file, verification 3's entry 24)

### 14 · chemins-aval F02 — A cold re-entry after a `sheet` revert reaches move 1 with no findings

Severity: TO FIX
Decision: In `8_code.md`, move 1 (L129-132) reads the lot's `verdict.md` when there is one: no sheet and a `## Cause` of `sheet` → the Détailleur's prompt is the one of L354-363 — `Your lot:` and `Findings:` copied — never the plain one; the verdict stays through the sheet path by design (L220-221), so the state is readable cold.
Where: 8_code.md L129-132, L67-79 ↔ L222-226, L350-368, L376-380
Cited: 8_code.md L220-221 — "⚠️ **the verdict stays**: its `## Attempts` is the count" · L378-380 — "⚠️ **Never `## Findings`, except to copy it into the Détailleur's prompt on a `sheet` cause**"
Owner: 8_code.md
Follows: —
Note: *Findings* occurs in 8_code.md at L192, L224, L360 and L378, all under move 4 (verified). Verification 3's entries 27 and 60 (the prompt's `Your lot:` line, the propagation) stand — move 1 reuses that prompt.

### 15 · chemins-aval F03 — A block raised in the run that applied a decision is archived as settled

Severity: TO FIX
Decision: In `8_code.md`, the rename of 4b's filled row (L277) follows a second test of the file after the agent reports, by the same two shapes as L284-296: a `## Blocking N` with no number, or an empty `## Decision`, is a block raised in the run that applied the earlier one — no rename, relayed as a block standing (the rule 7_lots.md L177-180 has for the Cadreur's file). `detailleur.md` L311 and `realisateur.md` L262 say a fresh block on a run that was named a filled file is appended below as the next `## Blocking N`, never a rewrite of the file; the Arbitre numbers its answer under the existing ones.
Where: 8_code.md L277, L284-296 ↔ detailleur.md L311-331, realisateur.md L262, L296-315 (7_lots.md L177-180) ↔ arbitre.md L147-160
Cited: 7_lots.md L177-180 — "⚠️ **A *decision applied* whose last `## Decision` is empty is a block raised in that same run**, appended below the one applied: 🔴 **the file stays at its unnumbered name**, and you relay it as a block standing." · realisateur.md L296-297 — "🔴 **A second lack you meet while carrying on is added to the blocking file** — ⚠️ **it never replaces the first.**"
Owner: 8_code.md
Follows: detailleur.md L311, realisateur.md L262 (append, never rewrite); arbitre.md L147-150 (numbers the new entry below)
Note: a grep of *append* / *fresh block* in detailleur.md, realisateur.md and 8_code.md returns nothing on these files (verified; arbitre.md L215 is on `code/redecoupage.md`). Read with entries 5 and 13 — the Testeur's and the Relecteur's files take the four-heading shape, whose post-report test is "`## Decision` still holds something".

### 16 · chemins-aval F04 — `## Redécoupage: archivable` survives the archive it triggered

Severity: TO FIX
Decision: In `7_lots.md`, after the `git mv` of L115-122 the command removes the `## Redécoupage: archivable` line from `code/sequence.md`, so the trigger is consumed with the archive and no later run finds a stale one; `verificateur.md` L98-100 says the command consumes the line.
Where: 7_lots.md L115-127 ↔ verificateur.md L98-100, L501-503 ↔ cadreur.md L892-917, L1036-1039
Cited: verificateur.md L501-503 — "**6. On a redécoupage, write `## Redécoupage: archivable` in `code/sequence.md`** — 🔴 **and only when your `## Defects` section is empty.**" · cadreur.md L1037-1039 — "⚠️ **the command reads that line from `code/sequence.md` itself and archives the file on it**, not on your report."
Owner: 7_lots.md
Follows: verificateur.md L98-100
Note: the Cadreur side read here — a Cadreur that goes out on block C before calling the Vérificateur (a `blocked_cadreur.md` on a request, or L915's row) leaves the previous `sequence.md` and its line; cadreur.md L925-926, which the consolidated report cites, is the third-round block, written *after* a round that rewrote `sequence.md` with defects and no line. The mechanism holds on the other exits; the decision covers all of them. Read with entry 35 (same owner) — different paragraphs.

### 17 · chemins-aval F05 — The multi-lot revert has no order across lots

Severity: TO FIX
Decision: In `8_code.md`, the reverts of several lots — *When the split comes back* (L579-587) and the non-last-lot case (L236-238) — work on one list: the commits of every lot concerned, each lot's cut after its last revert as move 3 says (L162-180), merged and ordered newest first across lots, reverted in that order.
Where: 8_code.md L579-587, L236-238, L162-180 ↔ testeur.md L283-288 (realisateur.md L693)
Cited: testeur.md L287-288 — "🔴 **One line per criterion no test can exercise** — 📌 **appended, never rewritten**: every lot of the split adds to it." · realisateur.md L693 — "**7. Update the technical state** — see *Updating the technical state*."
Owner: 8_code.md
Follows: —
Note: verification 3's entry 26 (the list cut after the last revert) stands — this orders what it cuts. Read with entry 4 (same paragraphs) — compatible.

### 18 · chemins-aval F06 — Step 1 of the closing sequence lists no file outside the feature folder

Severity: TO FIX
Decision: In `8_code.md`, step 1 of both closing sequences (L608-610 and L720-724) enumerates what agents without Bash leave outside the feature folder: `docs/TECHNICAL_CONVENTIONS.md` and the feature folder's `couverture.md` (the Architecte's invocation 3, architecte.md L337), `docs/CURRENT_TECHNICAL_STATE.md` (the Arbitre's traps, L401), and the `architecte/` requests (entry 4) — a `git add` that reaches them all. `7_lots.md` L277-282 the same for its Architecte run.
Where: 8_code.md L608-610, L720-724, L96-98 ↔ architecte.md L4, L337 · arbitre.md L401, L477-478
Cited: architecte.md L4 — "tools: Read, Grep, Glob, WebSearch, WebFetch, Edit, Write" · L337 (invocation 3's output) — "The conventions file, updated · `couverture.md`, **a line per rule it added** · each request's verdict" · arbitre.md L477-478 — "📌 **`sleep` between two reads** — ⚠️ **that is the only command your `Bash` runs**"
Owner: 8_code.md
Follows: 7_lots.md L277-282
Note: `TECHNICAL_CONVENTIONS` and `couverture` occur nowhere in 8_code.md (verified). One edit of L608-610 and L720-724 serves entries 4 and 18.

---

## QUESTION

### 19 · fichiers F04 — Nothing resets `Round:` after a third-round decision

Severity: QUESTION
Decision: Item D settled, Option 1 — in `cadreur.md` L919-926, a round beyond the third that still carries defects blocks again at once, naming the decision that bought it; each filled `blocked_cadreur.md` buys exactly one round. The Vérificateur's `Round:` line goes on counting up.
Where: cadreur.md L919-926 ↔ verificateur.md L121-126
Cited: verificateur.md L121-125 — "**The round line** — 🔴 **`Round: N`, the first line of the file.** 📌 **The previous `code/sequence.md`'s number plus one when its `## Defects` carried lines; `1` otherwise** … 🔴 **The Cadreur counts its rounds on that line, never on files**"
Owner: cadreur.md
Follows: — (verificateur.md L121-126 unchanged)
Note: both sides verified — after a filled third-round decision the next round is `4`, and L919-926 say nothing of a fourth. Whether a decision buys fresh rounds is hers → `## To settle`, item D.

---

## NOTE

### 20 · renommages F02 — Two routes for a missing form

Severity: NOTE
Decision: In `GRILLE_CONVENTIONS.md` (`docs-new/process/`), `R4` (L50-52) names the route the Architecte follows — a `Kind: forme` question in its questions file, whose answer amends the grid by the Product Owner's hand — instead of a conventions request in `architecte/`.
Where: docs-new/process/GRILLE_CONVENTIONS.md L50-52 ↔ architecte.md L300-301, L564-568
Cited: architecte.md L300-301 — "🔴 **Amend the grid you apply** — the grid's `R4`. 📌 **A form it lacks is a `forme` question** in your questions file" · L564-566 — "📌 **`forme` is the grid's `R4` route** — 🔴 **a form the grid lacks, or one that keeps producing a useless rule.** ⚠️ **Its answer amends the grid, and the Product Owner does that herself**"
Owner: GRILLE_CONVENTIONS.md
Follows: —
Note: the agent's route is the one verification 3's entry 9 settled (a `forme` answer is a grid amendment, never a rule); the grid's sentence predates it. The grid sits in the Product Owner's documents folder — the applying agent changes those three lines and nothing else there.

### 21 · renommages F03 — `Cause: sheet` spelt as a line where every reader expects a heading

Severity: NOTE
Decision: In `relecteur.md`, L363 names the cause as the template writes it — `sheet` under `## Cause` (L160-162).
Where: relecteur.md L360-366 ↔ relecteur.md L160-162, 8_code.md L211-212
Cited: 8_code.md L211-212 — "🔴 **A verdict whose `## Cause` reads `sheet` never reaches a Réalisateur**"
Owner: relecteur.md
Follows: —

### 22 · renommages F04 — "`/cycle` ne l'appelle pas" survives in the two process documents

Severity: NOTE
Decision: — (moot, settled: `PROCESS_AMONT.md` and `PROCESS_AVAL.md` are out of scope for this campaign; change nothing)
Where: PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010
Cited: — (not opened)
Owner: —
Follows: —
Note: could not verify — `docs/process/` is the Product Owner's and this session does not open it; the two lines are hers, as verification 3's entry 44 already said.

### 23 · renommages F05 — Three commands sit in no row of the orchestrator's table

Severity: NOTE
Decision: In `.claude-new/CLAUDE.md`, the command table (L49-57) gains a row for `/audit_blocages`, `/audit_conventions` and `/deploie` — outside the chain, run by hand, what each runs — so L62-63 no longer makes them ordinary requests.
Where: .claude-new/CLAUDE.md L49-57, L62-63 ↔ audit_blocages.md L2, audit_conventions.md L2, deploie.md L2
Cited: audit_blocages.md L2 — "description: Read a cycle's blocking files and report what recurs across them" · audit_conventions.md L2 — "description: Read what the conventions gained during a cycle and report what it costs" · deploie.md L2 — "description: Install both applications on the physical phone and watch"
Owner: CLAUDE.md
Follows: —

### 24 · fichiers F05 — `releve.md` is archived for nobody

Severity: NOTE
Decision: Item E settled, Option 1 — `cadrage-produit/releve.md` stays in `/4_grille`'s archive list. No file changes.
Where: sondeur.md L225-231 ↔ 4_grille.md L450, L254-260
Cited: sondeur.md L225-226, L230-231 — "**2. Pass B, from the record alone** — 🔴 **never the blocks again.** … 📌 **The prompt names where the record goes**, beside your questions file."
Owner: 4_grille.md
Follows: —
Note: verified — the record is written and read within one global invocation, and the archive names no later reader. Whether a trace of it is wanted is hers → `## To settle`, item E.

### 25 · passages F03 — One decision per line, and a decision that spans several

Severity: NOTE
Decision: In `9_controle.md`, phase 6 (L401-409) writes a `## Decision` of several lines as one line — its parts joined in order on the identifier's line, nothing dropped and nothing on a continuation line — so the shape L407-409 promise the Rédacteur holds.
Where: 9_controle.md L401-409 ↔ arbitre.md L147-160 ↔ redacteur.md L749-752
Cited: arbitre.md L147-148 — "**A decision has three parts, under the entry's number** — 🔴 **one `N.` per `## Blocking N`, a single entry included**" · redacteur.md L749-750 — "📌 **A decisions line opens on the identifier of the block it bears on**, when it bears on one — 🔴 **you read it as written, and never guess another.**"
Owner: 9_controle.md
Follows: — (redacteur.md reads a line as written, which it still can; arbitre.md's shape stays)

### 26 · chemins-amont F09 — A stop-path pointer names three steps out of five

Severity: NOTE
Decision: In `3b_nature.md`, L221 names the five steps of *Git, once it has reported* (L251-263), as `3a_genre.md` L219 does.
Where: 3b_nature.md L218-221 ↔ 3b_nature.md L251-263 (3a_genre.md L216-220)
Cited: 3b_nature.md L253 — "1. 🔴 **`git add` and `git commit` inside the worktree**" · 3a_genre.md L219-220 — "🔴 **The five steps of *Git, once it has reported*, and then report the defect.**"
Owner: 3b_nature.md
Follows: —

### 27 · chemins-amont F10 — A `Clarification needed` flag with no questions file bounces for ever

Severity: NOTE
Decision: In `2_structure.md`, the row at L150 greps `Clarification needed` in `desc-produit.md` before naming `/3_decoupe`: a hit → stop, saying the flag stands with no questions file at the root to lift it — a filing or an integration went wrong, and the file is hers to find — never `/3_decoupe`.
Where: 2_structure.md L150 ↔ 3_decoupe.md L47-50 (3a_genre.md L49-52, 3b_nature.md L48-51, 4_grille.md L81-84)
Cited: 3_decoupe.md L47-50 — "🔴 **Grep `Clarification needed` in `desc-produit.md`.** ⚠️ **One hit and the command stops.** 📌 **Say which blocks carry one**, and that `/2_structure` has to run first."
Owner: 2_structure.md
Follows: — (the four stops stay; they now point at a command that names the state)
Note: read with entry 2 (same owner) — different rows.

### 28 · chemins-amont F11 — A feature-level question blocks a `bugfix-NN` request

Severity: NOTE
Decision: In `conventions.md`, the stop at L68-69 goes; row L84 of the walk, below the invocation-3 rows (L82-83), is where an unanswered `questions-architecte-*.md` stops the run.
Where: conventions.md L68-69 ↔ conventions.md L26-27, L82-84
Cited: conventions.md L83 — "| 🔴 **A second argument names a `bugfix-NN`, and no row above matched** | 📌 **Nothing to invoke** — say so: ⚠️ **`/8_code` carries on**." · L84 — "| A `questions-architecte-NN.md` at the root with an empty `Answer:` | 🔴 **Nothing** — say which questions wait |"
Owner: conventions.md
Follows: —
Note: read with entry 10 (same table) — 10 moves row L86 below L88-89, 28 keeps row L84 where it is; no collision.

### 29 · chemins-amont F12 — Four opus sondeurs on an empty list

Severity: NOTE
Decision: In `4_grille.md`, the first turn (L125-126) invokes nothing when the `Genre: comportement` grep returns no block, and says so — as `3a_genre.md` L125-128 does on an empty list. What the run writes or says next: item F settled, neither option — the stop is at `/7_lots`, not at `/4_grille` (see entry 30, F13); `/4_grille` gets no further rule.
Where: 4_grille.md L120-126 ↔ sondeur.md L53 · 3a_genre.md L125-128, 3b_nature.md L127-130
Cited: sondeur.md L53 — "| **The blocks to probe** | 📌 **Every one** — at 1 and 2, each carries `Genre: comportement`" · 3a_genre.md L125-126 — "📌 **Neither grep returns anything, and that highest file holds no `### Q` — or there is none** → 🔴 **do not invoke.**"
Owner: 4_grille.md
Follows: —
Note: read with entries 7, 8 and 24 (same owner) — different paragraphs.

### 30 · chemins-amont F13 — The *Otherwise → assembly* row runs on nothing, and on a nature that waits

Severity: NOTE
Decision: Item F settled. *F13, a feature with no behaviour block — neither option; the stop is at `/7_lots`.* A `transverse` block gives a lot only if it has a code half, and invocation 2 of the Convertisseur is what decides that (convertisseur.md L162-168, L185-187; 9_controle.md L146 downstream) — so no command before `/6_convertit` can tell whether the feature has something to build. `/4_grille` probes only `comportement` (4_grille.md L120-123): no rule. `/5_reclasse` must run — it writes `par-genre/recette.md` (5_reclasse.md L122) and a genre with no block gets an empty file (L135-137): no rule. `/6_convertit` must run — the only place the question is answerable, it writes the `tracabilite.md` `/9_controle` requires, and it already runs on an empty nature (L145): no rule. `/conventions` and `/fusion` are manual: no rule. The one rule, in `7_lots.md`: a `spec-technique.md` carrying zero numbered entries — the command cuts no split, names no next command, and its relay says where the feature's content lives: `par-genre/recette.md` at the feature folder's root and the preamble's `## Cross-cutting rules` in the technical document — then `/fusion`. Accepted cost, said in that row: `/9_controle` does not run, so `code/recette-ordonnee.md` is never written; the recette stays readable in `par-genre/recette.md`. The test is written against the shape `6_convertit.md` actually produces — if the document carries no countable entry marker, nothing is written and the entry is refused. *F18, a nature waiting on a technical answer — Option 1*: in `6_convertit.md`, no assembly while a nature waits — the assembly table (L230-233) treats a waiting nature as its *No* row: nothing assembled, `spec-technique.md` deleted, invocation 2 skipped, the nature named; the *No nature runs* table sends a run that fails L174 on a waiting nature alone to the same outcome. L155-156 and L433-436 already say it — this brings L230-233 into line, not a new rule. The `/conventions` stop on a missing document then holds.
Where: 6_convertit.md L170-175, L145, L155-156, L230-233, L433-438 ↔ 5_reclasse.md L134-137 ↔ fusionneur.md L83-87
Cited: 5_reclasse.md L135-137 — "⚠️ **A genre with no block gets an empty file**, never no file: its absence would read as *the split did not run*." · fusionneur.md L83-85 — "🔴 **Read `Genre:` on every block, at invocations 1 and 2, `INIT` included.** 📌 **`comportement`, `transverse`, `recette` and `référence`** enter. ⚠️ **`directive` and `hors périmètre` never do**"
Owner: 6_convertit.md (F18) · 7_lots.md (F13)
Follows: — (5_reclasse.md L134-137 and fusionneur.md L83-87 unchanged)
Note: both defects verified. F18 rests on two sentences of the same file that disagree — L230-233 assemble whenever every nature with blocks has its file, L433-436 assume a waiting nature makes the assembly write nothing — and picking one changes what the Product Owner sees while a nature waits; F13 is what the chain does with a feature that has no behaviour block. Both → `## To settle`, item F.

### 31 · chemins-amont F14 — The `### Q` guard stops on the Fusionneur's own integrated file

Severity: NOTE
Decision: In `fusion_compare.md`, the `### Q` guard (L50-56) leaves `questions-fusionneur-*.md` alone, as the filing (L71-72) already keeps the highest at the root by design; whether that file waits is the test `/fusion` row 5 makes — an empty `Answer:` stops, a `### Q` does not.
Where: fusion_compare.md L50-56, L71-72 ↔ fusion.md L59, L153-154
Cited: fusion.md L153-154 — "🔴 **And every file of that prefix but the highest** — the last one stays at the root, it carries the numbering." · L59 — "| 5 | A root questions file with an empty `Answer:` — 📌 **`questions-architecte-*.md` excepted** | 🔴 **STOP** — relay it |"
Owner: fusion_compare.md
Follows: —

### 32 · chemins-amont F16 — `/fusion` files other agents' root files without the `### Q` guard

Severity: NOTE
Decision: In `fusion.md`, *Git, before invoking* (L140-144) opens on the `### Q` guard every other command carries (3_decoupe.md L52-58) — the Fusionneur's own prefix and the architecte's excepted, as L146-148 and L153-154 already except them from the filing.
Where: fusion.md L140-154 ↔ 3_decoupe.md L52-58
Cited: 3_decoupe.md L52-55 — "🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not `architecte` before touching it** — 📌 **a file holding questions is not yours to file**: ⚠️ **it waits on an answer, or its answers were never integrated.** 🔴 **Stop and say which.**"
Owner: fusion.md
Follows: —

### 33 · chemins-aval F09 — The walk stops the block on its own PASSed lots

Severity: NOTE
Decision: In `detailleur.md`, the walk's grep (L501-503) skips a lot whose sheet stands with a PASS verdict — L512's row — and L115-117 says a production found for such a lot is what the lot built, never a contradiction.
Where: detailleur.md L501-503 ↔ detailleur.md L112-119, L508-514
Cited: detailleur.md L512 — "| **A sheet, and its verdict's `## Status` starts with `PASS`** | 🔴 **Never touched** — a reservation after the word changes nothing |" · L117 — "| A production that already exists, or the reverse | The lot was declared against a stale state document |"
Owner: detailleur.md
Follows: —

### 34 · chemins-aval F10 — *Where to resume* has no row for a PASSed lot with a filled decision, nor for a revert conflict

Severity: NOTE
Decision: In `8_code.md`, *Where to resume* (L71-74) opens on a look for an unnumbered `code/<lot>/blocked_*.md` with a filled `## Decision` on a lot already carrying a PASS — that lot runs first, its agent invoked with the file named and its review run again, as L695-700 promise; then the first lot with no PASS. On a revert conflict (F12): item G settled, Option 2 — a conflict on a lot's revert takes down every lot after it in the sequence, PASS or not, as the non-last-lot rule (L232-242) already does for a `sheet` cause; L217-218 and L586-587 point at L232-242 and do not restate it. A conflict means a later lot edited the same lines, so it depends on the reverted code; no git surgery is asked of the Product Owner.
Where: 8_code.md L71-74 ↔ L695-700 · L215-218, L586-587
Cited: 8_code.md L695-698 — "📌 **A filled `## Decision` is not a stop** — invoke the agent it names on the lot it names, and let it apply the decision. ⚠️ **Even on a lot already carrying a PASS**" · L217-218 — "⚠️ **A conflict stops the command**: `git revert --abort`, say so, and resolve nothing"
Owner: 8_code.md
Follows: —
Note: verification 3's entry 46 (resume stops on `code/blocked_verificateur.md`) sits in the same section — compatible, a look before the read.

### 35 · chemins-aval F11 — The hand-back table has no first-match rule

Severity: NOTE
Decision: In `7_lots.md`, the hand-back table (L163-172) gets a first-match rule, the `code/blocked_verificateur.md` row (L172) placed first — the Vérificateur writes no `sequence.md` when it blocks, and the previous one still stands with its empty `## Defects`.
Where: 7_lots.md L165 ↔ 7_lots.md L172, L89-94
Cited: 7_lots.md L172 — "| `code/blocked_verificateur.md` | 🔴 **Stop.** 📌 **Relay which file was missing** — ⚠️ **it carries no `## Decision`**: nothing in it is the Product Owner's to settle, and the step before it has to run again |"
Owner: 7_lots.md
Follows: —
Note: L89-94 remove the previous run's file before the Cadreur runs, so one found after it is this run's. Read with entry 16 (same owner) — different paragraphs.

### 36 · chemins-aval F13 — Three empty attempts leave nothing on disk

Severity: NOTE
Decision: Item H settled, Option 1 — accept. The count stays in this run alone, as verification 3's entry 23 decided. No file changes.
Where: 8_code.md L182-196, L251-255 ↔ 8_code.md L257-262, L706-707
Cited: 8_code.md L191-194 — "🔴 **No verdict yet → write none**: ⚠️ **a verdict is the Relecteur's file**, and inventing `## Verified`, `## Findings` and `## Cause` for a review that never ran is worse than a count held in this run." · L259-261 — "⚠️ **Otherwise a run stopped for any reason restarts the count at zero**, and a lot that cannot pass is retried three times per run for ever."
Owner: 8_code.md
Follows: —
Note: verified — the two sentences are both deliberate (verification 3's entry 23 wrote the first), and the cap they leave holds per run. A count on disk means a file of the command's own, or a stop after the first empty attempt: a design choice → `## To settle`, item H.

### 37 · chemins-aval F14 — Move 2 never skips the Réalisateur on its report

Severity: NOTE
Decision: In `8_code.md`, move 2's table (L136-140) skips the Réalisateur when `code/<lot>/compte-rendu.md` is there and no unnumbered `code/<lot>/blocked_realisateur.md` sits beside it, and the lot goes to move 3 — a lot coded and not reviewed; entry 4's deletion of that report on a revert keeps a re-coded lot from being skipped.
Where: 8_code.md L136-140 ↔ 8_code.md L182-196
Cited: 8_code.md L138 — "📌 **skipped when `code/<lot>/conception.md` is there and no unnumbered `code/<lot>/blocked_concepteur.md` sits beside it**" · L186-187 — "📌 **the same sha is the empty attempt** — the Réalisateur committed nothing. 🔴 **That counts as a failed attempt, and the Relecteur is not invoked.**"
Owner: 8_code.md
Follows: —
Note: the Réalisateur writes its report at step 8, after the code (realisateur.md L695-696) — a report on disk is a finished coding, never a partial one (those leave `reprise_realisateur.md`).

### 38 · chemins-aval F15 — The ownership list omits the Concepteur and the Testeur

Severity: NOTE
Decision: In `audit_blocages.md`, the list at L107-109 names the Concepteur (its declarations) and the Testeur (its tests) between the Détailleur and the Réalisateur.
Where: audit_blocages.md L103-110 ↔ concepteur.md L12-15, testeur.md L52-56
Cited: concepteur.md L14-15 — "You turn the spec sheet's signatures into declarations the compiler accepts, **each body throwing *not implemented***."
Owner: audit_blocages.md
Follows: —

### 39 · chemins-aval F16 — Finding 7 reads `desc-bug.md` anchors against a `spec-technique.md` coverage

Severity: NOTE
Decision: In `audit_conventions.md`, finding 7 (L144-148) runs only when `couverture.md` traces to the document the split was cut from; on a correction cycle whose `couverture.md` traces to `spec-technique.md` while `code/decoupage.md` anchors on `desc-bug.md`, the finding is skipped and the report says so under its heading.
Where: audit_conventions.md L144-148 ↔ audit_conventions.md L53-57, L59-60
Cited: audit_conventions.md L55-57 — "`couverture.md` traces to the document it was written against, which may be the feature's `spec-technique.md` rather than this cycle's `desc-bug.md`."
Owner: audit_conventions.md
Follows: —

### 40 · chemins-aval F17 — Gap identifiers are positional

Severity: NOTE
Decision: Item I settled, Option 2 — each gap in `bug-list.md` opens on its own `G<n>`, written by the Product Owner, as a control-report gap already carries its `B<n>`; `diagnostique.md` (L37) reads the identifier instead of counting position, and a gap with no identifier stops the command, which says which line lacks one. Follows: whatever describes `bug-list.md`'s shape to the Product Owner — diagnostiqueur.md (L63, L490, L535, L621-623: the order and the `B<n>`), 9_controle.md L495-496 (how a gap she takes from the report enters `bug-list.md`). A description outside `.claude/` and `docs/process/` is named, not changed; `PROCESS_AVAL.md` L894, L1073 are the Product Owner's, out of scope as entry 22.
Where: diagnostique.md L33-38 ↔ diagnostiqueur.md L79-82, L191-200
Cited: diagnostiqueur.md L79-82 — "🔴 **You block when producing is impossible** — 📌 **four cases**: a prompt naming no gap · a report set that does not match `bug-list.md` · a report that does not carry what an entry needs · a closure that fails."
Owner: diagnostique.md
Follows: diagnostiqueur.md L63, L80-81, L194-198, L490, L535, L621-623; 9_controle.md L495-496
Note: verified — `G01`, `G02` are "in the file's own order" (L37) and nothing else names a gap. `bug-list.md` is hers, hand-written; whether she freezes its order or writes identifiers is hers → `## To settle`, item I.

---

## Shared owners — read together

| Owner | Entries | Collision check |
|---|---|---|
| 8_code.md | 3 (third-return stop, relay) · 4, 17, 18 (revert paragraphs, closing step 1) · 13 (hand-back table, L279-282, Relecteur prompt) · 14 (move 1) · 15 (4b post-report test) · 34 (resume) · 37 (move 2) · follows 5 (L59-60, L303-305) · 36 to settle | 4 + 18: one edit of L608-610 and L720-724 (`architecte/`, the two docs files). 4 + 17: 17 orders the reverts, 4 changes what they carry — compatible. 13 + 15: the Relecteur's file is out of 4b and in the hand-back table; 15's post-report test applies to it on the *anything else* row only — compatible. 14 + 37: move 1 and move 2, different lines. 34 + verification 3's 46: same section, a look then a read. |
| 4_grille.md | 8 (L102-106) · 29 (L125-126) · 7 (closure L176-183) · 24 (no change) | Different paragraphs. |
| 6_convertit.md | 9 (nature table, L198-202) · 30 F18 (L230-233, L170-175) | 30 bears on L170-175 and L230-233, 9 on L143-153 — no overlap. |
| 7_lots.md | 16 (L115-127) · 35 (L163-172) · 30 F13 (one row, zero entries) · follows 3 (L318-323), 18 (L277-282) | Five paragraphs, no overlap. |
| conventions.md | 10 (row L86 moves below L88-89) · 28 (L68-69 dropped, row L84 stays) | Same table; 28 relies on row L84 sitting below L82-83, which 10 does not move. |
| fusion_compare.md | 11 (L20-26) · 12 (L149-181) · 31 (L50-56) | Three sections. |
| 2_structure.md | 2 (invocation-2 filing) · 27 (row L150) | Different rows; the table order of verification 3's 5+6 stays. |
| 3a_genre.md | 6 (row L284) · verification 3's 56 (same row, its sentence stays) | One edit of the row keeps J's sentence. |
| 3b_nature.md | 26 (L221) · follows 6 (L295) | Different lines. |
| concepteur.md | 1 (move 1, `## Declared`) · follows 4 (L283-284) | Different moves. |
| realisateur.md | 4 F03 (the step that calls the Arbitre) · follows 4 (L698), 15 (L262) | Different lines. |
| detailleur.md | 33 (walk) · follows 15 (L311) | Different sections. |
| relecteur.md | 21 (L363) · follows 13 (no change) | — |
| testeur.md | 5 | — |
| verificateur.md | follows 16 (L98-100) | — |
| cadreur.md | follows 3 (block C) · 19 (L919-926) | Different sections. |
| fusion.md | 32 | — |
| 9_controle.md | 25 | — |
| audit_blocages.md 38 · audit_conventions.md 39 · CLAUDE.md 23 · GRILLE_CONVENTIONS.md 20 · diagnostique.md 40 · 5_reclasse.md follows 7 · diagnostiqueur.md and 9_controle.md follow 40 | one each | — |

---

## Summary table

| # | Severity | Decision | Where | Owner | Follows |
|---|---|---|---|---|---|
| 1 | BLOCKING | Move 1 reads the mark; a `modified` symbol is edited in place, never redeclared nor a clash; `## Declared` carries the mark — body: the throw, like a new one (A, Option 1) | detailleur.md L267-271 ↔ concepteur.md L190, L236-245, L78, L176-179 | concepteur.md | — |
| 2 | BLOCKING | Invocation 2 on a blocking file files the empty questions file beside it | 2_structure.md L146, L160-162, L313-316 ↔ redacteur.md L275 ↔ 1_lexique.md L63 | 2_structure.md | — |
| 3 | TO FIX | The stop and the relay name the heading and `/7_lots`; 7_lots relays it; block C reads it as her instruction | 8_code.md L552-554, L566-573, L750-759 ↔ 7_lots.md L318-323 ↔ cadreur.md L976-981 | 8_code.md | 7_lots.md, cadreur.md |
| 4 | TO FIX | `compte-rendu.md` in the three deletion lists; `architecte/` requests are the command's to commit, never a lot's — trap: the Réalisateur commits the state document alone, unprefixed (B, Option 2) | 8_code.md L215-221, L236-238, L593-594, L608-610, L720-724 ↔ realisateur.md L698 ↔ concepteur.md L281-285 ↔ arbitre.md L401 ↔ detailleur.md L681 | 8_code.md, realisateur.md | concepteur.md, realisateur.md, 7_lots.md |
| 5 | TO FIX | `tests.md` gains `## Decision applied`; 8_code names the three fields | testeur.md L150-152, L318-343 ↔ 8_code.md L59-60, L303-305 | testeur.md | 8_code.md |
| 6 | TO FIX | Row L284: `/2_structure` only when every decision is a rewrite, a mixed file runs `/3a_genre` first; the `/1_lexique` leg goes | 3a_genre.md L284, L200-205 · 3b_nature.md L295 ↔ 2_structure.md L300-307, L382 ↔ redacteur.md L577-580, L275 ↔ 1_lexique.md L59 | 3a_genre.md | 3b_nature.md |
| 7 | TO FIX | The closing turn strips the markers; closure = empty file and no marker; a marker reopens on the marked blocks (C, Option 1) | 4_grille.md L176-183, L191-195 ↔ 2_structure.md L382 ↔ redacteur.md L132 | 4_grille.md | 5_reclasse.md |
| 8 | TO FIX | The answered-file gate excludes `questions-architecte-*.md` | 4_grille.md L102-106 ↔ L218-228, L235-237 ↔ conventions.md L84 | 4_grille.md | — |
| 9 | TO FIX | Rows combine: one run, every matching row's prompt line | 6_convertit.md L143-153, L198-202 ↔ convertisseur.md L503-507 | 6_convertit.md | — |
| 10 | TO FIX | Row L86 moves below the `couverture.md` rows | conventions.md L86, L88-89, L140-147 ↔ 2_structure.md L279-281 | conventions.md | — |
| 11 | TO FIX | Three gates added: report, plan, bug-fix pass not run | fusion_compare.md L20-26 ↔ fusion.md L58, L62, L64, L91-93 | fusion_compare.md | — |
| 12 | TO FIX | The rename moves before the five steps, inside the worktree | fusion_compare.md L149-181 ↔ fusion_applique.md L144-154 | fusion_compare.md | — |
| 13 | TO FIX | Every hand-back row retires the file; *anything else* → PO fills, Relecteur prompt names it, renamed after | 8_code.md L279-282, L672-691, L509-516 ↔ relecteur.md L264-269, L332 | 8_code.md | — |
| 14 | TO FIX | Move 1 uses the Findings prompt on a `sheet` verdict | 8_code.md L129-132 ↔ L222-226, L354-363 | 8_code.md | — |
| 15 | TO FIX | 4b re-tests the file after the report; a fresh block is appended, never a rewrite | 8_code.md L277, L284-296 ↔ detailleur.md L311, realisateur.md L262 ↔ 7_lots.md L177-180 | 8_code.md | detailleur.md, realisateur.md, arbitre.md |
| 16 | TO FIX | The command strips the line after the archive | 7_lots.md L115-127 ↔ verificateur.md L98-100, L501-503 ↔ cadreur.md L1036-1039 | 7_lots.md | verificateur.md |
| 17 | TO FIX | One revert list across lots, newest first | 8_code.md L579-587, L236-238, L162-180 ↔ testeur.md L287-288 | 8_code.md | — |
| 18 | TO FIX | Step 1 enumerates the conventions file, `couverture.md`, the state document, `architecte/` | 8_code.md L608-610, L720-724 ↔ architecte.md L4, L337 · arbitre.md L401, L477-478 | 8_code.md | 7_lots.md |
| 19 | QUESTION | A round beyond the third with defects blocks again; one decision, one round (D, Option 1) | cadreur.md L919-926 ↔ verificateur.md L121-126 | cadreur.md | — |
| 20 | NOTE | `R4` names the `forme` question route | docs-new/process/GRILLE_CONVENTIONS.md L50-52 ↔ architecte.md L300-301, L564-568 | GRILLE_CONVENTIONS.md | — |
| 21 | NOTE | L363 spells the cause as the template does | relecteur.md L363 ↔ L160-162, 8_code.md L211 | relecteur.md | — |
| 22 | NOTE | — (moot, settled; not opened) | PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010 | — | — |
| 23 | NOTE | A row for the three commands | .claude-new/CLAUDE.md L49-57, L62-63 ↔ the three `description:` lines | CLAUDE.md | — |
| 24 | NOTE | `releve.md` stays archived — no change (E, Option 1) | sondeur.md L225-231 ↔ 4_grille.md L450, L254-260 | 4_grille.md | — |
| 25 | NOTE | A multi-line decision is written as one line, parts joined | 9_controle.md L401-409 ↔ arbitre.md L147-160 ↔ redacteur.md L749-750 | 9_controle.md | — |
| 26 | NOTE | L221 names the five steps | 3b_nature.md L221 ↔ L251-263 | 3b_nature.md | — |
| 27 | NOTE | Row L150 greps the flag first and names the state | 2_structure.md L150 ↔ 3_decoupe.md L47-50 | 2_structure.md | — |
| 28 | NOTE | L68-69 dropped; row L84 is the stop | conventions.md L68-69 ↔ L82-84 | conventions.md | — |
| 29 | NOTE | Empty behaviour list → invoke nothing, say so — the rest: the stop is `/7_lots`'s (F, see 30) | 4_grille.md L125-126 ↔ sondeur.md L53 | 4_grille.md | — |
| 30 | NOTE | F13: `/7_lots` stops on a document with zero entries, names where the content lives, then `/fusion` (F, neither option) · F18: no assembly while a nature waits (F, Option 1) | 6_convertit.md L170-175, L230-233, L433-438 ↔ 5_reclasse.md L134-137 ↔ fusionneur.md L83-87 · 7_lots.md | 6_convertit.md, 7_lots.md | — |
| 31 | NOTE | The guard leaves the Fusionneur's files to row 5's test | fusion_compare.md L50-56, L71-72 ↔ fusion.md L59, L153-154 | fusion_compare.md | — |
| 32 | NOTE | The `### Q` guard opens the filing | fusion.md L140-154 ↔ 3_decoupe.md L52-58 | fusion.md | — |
| 33 | NOTE | The walk's grep skips PASSed lots | detailleur.md L501-503 ↔ L115-117, L512 | detailleur.md | — |
| 34 | NOTE | Resume looks first for a filled decision on a PASSed lot — conflict: the later lots go down too, as L232-242 (G, Option 2) | 8_code.md L71-74 ↔ L695-700 · L217-218, L586-587 | 8_code.md | — |
| 35 | NOTE | First-match rule, the Vérificateur row first | 7_lots.md L163-172 ↔ L89-94 | 7_lots.md | — |
| 36 | NOTE | Accept — the count stays per run, no change (H, Option 1) | 8_code.md L182-196, L251-255 ↔ L257-262, L706-707 | 8_code.md | — |
| 37 | NOTE | Move 2 skips the Réalisateur on its report | 8_code.md L136-140 ↔ L182-196 | 8_code.md | — |
| 38 | NOTE | The list names the Concepteur and the Testeur | audit_blocages.md L107-109 ↔ concepteur.md L14-15 | audit_blocages.md | — |
| 39 | NOTE | Finding 7 skipped when `couverture.md` traces to another document | audit_conventions.md L144-148 ↔ L53-57 | audit_conventions.md | — |
| 40 | NOTE | Each gap opens on its `G<n>`, hers; the command reads it, stops on a gap without one (I, Option 2) | diagnostique.md L37 ↔ diagnostiqueur.md L79-82, L191-200 | diagnostique.md | diagnostiqueur.md, 9_controle.md |

---

## Counts

- **40 entries**, 40 distinct defects (the `Same as` halves were consolidated already).
- **Decided: 39** — every entry but 22. The nine `## To settle` items (A-I) were settled by the Product Owner on 2026-09-21 and written into their entries: 1 (A), 4 (B), 7 (C), 19 (D), 24 (E), 29 and 30 (F), 34 (G), 36 (H), 40 (I). Two of them change no file: 24 and 36.
- **Could not verify: 1** — entry 22 (`docs/process/`, not opened by this session; moot by the *Settled* rule, change nothing).

39 + 1 = 40. Nine `## To settle` items, A-I, all settled.

**Contradictions with verification 3's decisions: none found.** Entries 2, 3, 4, 8, 9, 10, 13, 14, 17, 34 and 37 touch lines a verification 3 decision wrote; each entry says how it fits, and none reverses one.

---

## To settle

Each item: what was open, the options, what each costs — kept as written for the record. 📌 **All nine are settled**; the decision stands in the `Decision` of the entry it belongs to, and the line under each heading here names it.

### A — Entry 1: the body of a `modified` symbol

**Settled: Option 1.**

The Concepteur edits a `modified` declaration in place (the decision). Its body is the question: concepteur.md L17-18 and L106-107 say every body throws *not implemented*, and testeur.md L265 counts on it ("the bodies throw, so anything calling one raises") — applied to a modified symbol, the working body of the previous lot is replaced by a throw until the Réalisateur writes it again.

- **Option 1 — the rule as written, a throw**: uniform, the Testeur's red tests stay red, the Réalisateur rewrites the body from the sheet's criteria as for any symbol. Cost: the old logic leaves the tree at the Concepteur's commit; on a lot that fails three times it is gone with the revert, and nothing but git history holds it.
- **Option 2 — the body stays when it still compiles**: the Concepteur changes the signature and touches the body only where the compiler forces it. Cost: a rule against L17-18 and L106-107; a test on a modified symbol may pass green at the Testeur, which then has to tell a met criterion from an untouched body; the Concepteur decides what "still compiles" means on a body it must not read as logic.

### B — Entry 4, F03: the Arbitre's trap rides the lot's commit

**Settled: Option 2.**

A trap the Arbitre writes into `CURRENT_TECHNICAL_STATE.md` mid-lot (arbitre.md L401) is committed by the Réalisateur's step 9 with the lot's own state entries, in one file, and a `sheet` revert removes both.

- **Option 1 — accept**: the re-coded lot meets the same red test, calls the Arbitre, which writes the trap again. Cost: one Arbitre invocation per such recoding, and a second settling that may differ from the first.
- **Option 2 — the Réalisateur commits the trap apart**: right after the Arbitre returns, and before its own step 7, the Réalisateur commits the state document alone under a message not prefixed `<lot>:` — outside every revert list. Cost: one rule in realisateur.md (its step 5/6, where it calls the Arbitre) and a commit the Relecteur's diff includes as a file the lot touched.

### C — Entry 7: reopening the first time after a later integration

**Settled: Option 1.**

Once the highest `questions-sondeur-NN.md` is empty, 4_grille.md L176-183 close the first time and nothing reopens it; a block a second-time or conversion answer creates or changes (marked by the Rédacteur, L132-133) reaches `/5_reclasse` unprobed, against 2_structure.md L382. Any reopen rule keyed on the markers meets L191-195: the closing turn's markers are stripped by nobody, so a closed grid and a reopened one look alike.

- **Option 1 — the command strips the markers at closure**: the run that writes or receives the empty sondeur file removes `NEW` / `MODIFIED` from the heading lines of `desc-produit.md`; the closure test becomes "highest sondeur file empty *and* no marker", and a marker found with an empty file reopens the first time on the marked blocks. Cost: a command edits the product file (as `/5_reclasse` already does, without an agent); the Rédacteur's L126-134 lose their monopoly on the markers.
- **Option 2 — accept the hole**: 2_structure.md L382's promise is narrowed — a block created or changed after the first time closed is split, classed and given a nature, and reaches the Convertisseur unprobed; the relay says so. Cost: one sentence in each file; the Product Owner probes such a block by hand or not at all.
- **Option 3 — the Rédacteur asks the grid**: an integration of a `existant` or `convertisseur` file that creates or changes a block writes the next `questions-sondeur-NN.md` itself, holding one `### Q` naming the block for probing — so the highest sondeur file is no longer empty and the first time reopens on the existing rows. Cost: the Rédacteur writes another agent's file, and `/5_reclasse`'s closure test sees an open grid until a turn runs.

### D — Entry 19: rounds after a third-round decision

**Settled: Option 1.**

cadreur.md L919-926 count three rounds on the Vérificateur's `Round:` line; after a filled third-round `blocked_cadreur.md` the next line reads `4`, and nothing says what a round beyond three does.

- **Option 1 — one round per decision**: a round beyond the third still carrying defects blocks again at once, the decision named; each of her answers buys one round. Cost: two sentences in cadreur.md; a decision that needs two corrections costs her two rounds.
- **Option 2 — a decision resets the count**: the Cadreur, applying a filled decision, tells the Vérificateur in its prompt that the round count restarts, and verificateur.md L121-126 write `1` on that prompt. Cost: a prompt parameter and a rule in both files; three fresh rounds per decision.

### E — Entry 24: `releve.md` archived for nobody

**Settled: Option 1 — no file changes.**

The global sondeur writes and reads `cadrage-produit/releve.md` inside one invocation (sondeur.md L225-231); 4_grille.md L254-260 archive it with the five other files, and no later reader is named.

- **Option 1 — keep it**: a trace of what pass B crossed, beside the questions it produced. Cost: nothing.
- **Option 2 — drop it from the archive list**: the file is overwritten each turn and never kept. Cost: one line in 4_grille.md; a pass-B question can no longer be traced to the record that produced it.

### F — Entries 29 and 30: a feature with no behaviour block, and a nature that waits

**Settled: F13 — neither option, the stop is at `/7_lots` (one row; every command before it runs, none gets a rule); F18 — Option 1.**

Two questions of one kind — what the chain does when there is nothing, or not yet something, to build.

*A feature whose blocks are all `directive`, `hors périmètre`, `recette` or `transverse` (29, 30 F13):* `/4_grille` runs four opus sondeurs on nothing (decided: it invokes nothing), `/6_convertit` builds an empty document, `/conventions` walks it, `/7_lots` cuts a split on nothing, and `/fusion` merges a global of empty sections.

- **Option 1 — stop at `/4_grille`**: no behaviour block → the run says the feature has nothing to build and names no next command; the chain ends there for it. Cost: one row in 4_grille.md; a feature meant to carry only conventions or exclusions reaches neither the technical document nor the global.
- **Option 2 — run through**: each command writes its empty evidence (the empty sondeur and existant files, an empty document, an empty split) and the chain ends at `/fusion` with the `transverse` and `recette` blocks merged. Cost: several opus invocations for nothing, and 6_convertit.md, 7_lots.md and fusionneur.md each need a sentence on an empty input.

*A nature waiting on a technical answer (30 F18):* 6_convertit.md L230-233 assemble whenever every nature with blocks has its file, L433-436 assume a waiting nature makes the assembly write nothing, L155-156 say the document does not stand while one waits.

- **Option 1 — no assembly while a nature waits**: the assembly table treats a waiting nature as its *No* row — nothing assembled, `spec-technique.md` deleted, invocation 2 skipped, the nature named — and the *No nature runs* table sends a run that fails L174 on a waiting nature alone to the same outcome. Cost: no document on disk while a question waits (the `/conventions` stop on a missing document then holds); the Product Owner reads the question in the technical file, not in a marked document.
- **Option 2 — assemble with the mark inside**: L230-233 stay, L433-436 stop assuming; the assembly and invocation 2 run on every re-run while the nature waits. Cost: one opus invocation (the transversal) per re-run for a known result; the marked document stays readable.

### G — Entry 34, F12: a revert conflict

**Settled: Option 2.**

8_code.md L217-218 and L586-587 stop the command on a conflict with nothing changed, and every re-run meets it again. Entry 17's order removes the conflicts the shared files caused; the ones left are real — a later lot edited the same lines.

- **Option 1 — the Product Owner resolves it as an ordinary request**: the stop says which commit and which files conflict, and she asks the orchestrator, outside the command, to revert by hand and commit; the next `/8_code` finds the revert done (the list of move 3 is empty after it). Cost: one sentence; a git operation done outside any command.
- **Option 2 — the command reverts the later lots too**: a conflict on a lot's revert takes every lot after it in the sequence down, PASS or not, as the non-last-lot rule (L232-242) already does for a `sheet` cause. Cost: lots redone for a conflict; safe, and no hand work.

### H — Entry 36: three empty attempts across runs

**Settled: Option 1 — no file changes.**

The empty-attempt count lives in this run alone (8_code.md L191-196, L253-255), by a choice verification 3's entry 23 made; a run stopped and restarted repeats the three.

- **Option 1 — accept**: a Réalisateur that commits nothing three times in a row is a broken run, and the Product Owner sees it in the relay. Cost: nothing; up to three empty runs per `/8_code` run.
- **Option 2 — stop after the first**: an empty attempt stops the lot at once, relayed as a fault of the run, no retry. Cost: one row in move 3; a transient failure (a build tool hiccup) costs a run.
- **Option 3 — a count file of the command's own**: `code/<lot>/attempts.md` holds the empty attempts, read at move 3 and deleted when the Relecteur writes a verdict. Cost: a new file, its rule, and its deletion in the revert lists.

### I — Entry 40: gap identifiers are positional

**Settled: Option 2.**

`G01`, `G02` follow `bug-list.md`'s order (diagnostique.md L37); a gap she inserts between two runs shifts them, and invocation 2 blocks on a report set that no longer matches. `bug-list.md` is hers, hand-written.

- **Option 1 — a rule on the file**: a gap added once a run has started goes at the end, never between two; diagnostique.md says so, and the command says so when it stops on a mismatch. Cost: one sentence; a rule she has to remember.
- **Option 2 — she writes the identifier**: each gap opens on its `G<n>`, as a control-report gap already carries its `B<n>` (verification 3's item G); the command reads it instead of counting. Cost: a shape she has to write by hand, and a rule for a gap without one.

---

*39 entries decided · 1 not verified and moot (22) — 40 in all. Nine `## To settle` items, A-I, all settled on 2026-09-21 and written into their entries; 24 and 36 change no file.*
