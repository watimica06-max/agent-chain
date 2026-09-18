# Vérification 3 — consolidé

Five reports read: `renommages.md` (11) · `fichiers.md` (9) · `chemins-amont.md` (27) · `chemins-aval.md` (19) · `passages.md` (10) — 76 findings. Every file a BLOCKING or TO FIX `Where` names was opened at those lines under `.claude-new/`. Line numbers below are the ones read, which sometimes widen or correct the ones reported.

Merged on `Where` (same file, same line). Two exceptions are stated where they occur: entry 9 merges two findings on the same passage whose cited lines differ by ten; entries 10 and 31 share `convertisseur.md L862` and are **not** merged — that line is the sound side of two different readers' defects, and one owner could not settle both.

Severity order: BLOCKING · TO FIX · QUESTION · NOTE. Verdicts were given to BLOCKING and TO FIX only; the rest carry `—`.

| # | Severity | Verdict | Finding | Where | Owner | Same as |
|---|---|---|---|---|---|---|
| 1 | BLOCKING | confirmed | Phase 1's genre filter has no source in its reading list, and omits `transverse`, so step d stops on every feature whose transverse rules gave code | 9_controle.md L39-42, L132-134, L187-195 ↔ convertisseur.md L172, L194-200, L749-754, L853-864 ↔ qualifieur.md L74-86 | 9_controle.md | chemins-aval F01, chemins-aval F02, passages F01, passages F06 |
| 2 | BLOCKING | confirmed | Every agent without Bash leaves its files uncommitted; the merge brings nothing, the remove refuses, and the verdict never reaches `HEAD` | 8_code.md L105-108, L614-625 ↔ relecteur.md L4, L46 (also 7_lots.md L269-273, 9_controle.md L389-394, diagnostique.md L172-177) | 8_code.md | chemins-aval F08 |
| 3 | BLOCKING | confirmed | The Arbitre marks a waiting entry two ways; under one of them `/8_code` counts it answered and archives the file | arbitre.md L181-183, L194-198 ↔ 8_code.md L233-240 | arbitre.md | — |
| 4 | BLOCKING | confirmed | The second time never re-runs once it asked, and `/5_reclasse` waits for the empty file it will never write | 5_reclasse.md L50-62 ↔ 4_grille.md L293-298, L546-548 | 4_grille.md | chemins-amont F27 |
| 5 | BLOCKING | confirmed | "Decision first, then answer" leaves the answered qualifieur file beside the Rédacteur's own; every command stops on two | 3a_genre.md L255 ↔ 2_structure.md L133, L186-187, L249 (3b_nature.md L265 says so) | 2_structure.md | — |
| 6 | BLOCKING | confirmed | "Answer first, decision once integrated" reaches `/2_structure` with an empty decision, whose row stops before integrating | 3b_nature.md L265 ↔ 2_structure.md L134, L137 | 2_structure.md | — |
| 7 | TO FIX | confirmed | A single-entry decision in the Arbitre's three-part shape has no number, so `/8_code` never counts it filled | arbitre.md L147-157, L177-179 ↔ 8_code.md L234, L237-240 | arbitre.md | — |
| 8 | TO FIX | confirmed | `## Where` names a lot, section or file, and the request blocks carry no identifier, so the dispatch cannot find "the request its `## Where` names" | cadreur.md L196-198, L227-231, L240-243, L314 ↔ 7_lots.md L167-168, L182-186 | cadreur.md | — |
| 9 | TO FIX | confirmed | A `forme` answer, which amends the grid, is turned into a convention | architecte.md L544-546, L556-560, L634-652 ↔ conventions.md L263-269 | architecte.md | passages F04 |
| 10 | TO FIX | confirmed | Step d counts every block of `tracabilite.md` against behaviours alone | 9_controle.md L132, L187-189 ↔ convertisseur.md L857-864 | 9_controle.md | — |
| 11 | TO FIX | confirmed | A `NEW` block after `/7_lots` deletes `spec-technique.md`, and `/6_convertit` refuses to rebuild it | 2_structure.md L202-210 ↔ 6_convertit.md L35-38 | 2_structure.md | chemins-amont F11 |
| 12 | TO FIX | confirmed | The audit's four places leave out `convertisseur/` | audit_blocages.md L26-30 ↔ 6_convertit.md L343-350 | audit_blocages.md | — |
| 13 | TO FIX | confirmed | An answer naming a genre alone leaves nothing for the two greps, so the invocation that would apply it is skipped | 3a_genre.md L103-112, L154-155 ↔ qualifieur.md L173, L185-186, L220, L323-324 | 3a_genre.md | — |
| 14 | TO FIX | confirmed | Same hole for the classeur | 3b_nature.md L102-113 ↔ classeur.md L169-175 | 3b_nature.md | — |
| 15 | TO FIX | confirmed | A rerun on a byte-identical part with no product answer in the block meets the same gap and re-asks | 6_convertit.md L143-144 ↔ convertisseur.md L487-489, L632-634 | 6_convertit.md | — |
| 16 | TO FIX | confirmed | A turn whose answers changed no block leaves neither a marker nor an empty file, and the grid cannot close | 4_grille.md L176-183, L197-204 ↔ 2_structure.md L98-103, L249-250 | 4_grille.md | — |
| 17 | TO FIX | confirmed | The `### Q` guard runs over the architecte's waiting file before the exception is stated, in seven commands | 3a_genre.md L54-59, L71-73 ↔ conventions.md L122-126 | 3a_genre.md | — |
| 18 | TO FIX | overstated → NOTE | Only `/fusion` and `/fusion_applique` file the architecte's answered file; the three others stop on its `### Q` first | 3_decoupe.md L51-59 ↔ conventions.md L85, L109-112 (fusion.md L47, L113-117; fusion_applique.md L175-179) | fusion.md | — |
| 19 | TO FIX | confirmed | After "4 wrote none" the highest lexicographe file holds entries, and `/2_structure` stops on a settled vocabulary | 2_structure.md L27-29, L86-90, L140-143 ↔ 1_lexique.md L205-210, L217-221, L263 | 2_structure.md | — |
| 20 | TO FIX | confirmed | The re-invocation on a short list is written after the worktree was removed | 3_decoupe.md L204-207 ↔ 3_decoupe.md L175-181 | 3_decoupe.md | — |
| 21 | TO FIX | confirmed | An empty `questions-architecte-NN.md` is filed by nobody and its row precedes invocation 4's | conventions.md L86 ↔ conventions.md L137-140 | conventions.md | — |
| 22 | TO FIX | confirmed | Only `/conventions` commits inside the worktree; every other upstream command merges a branch with no commit | 1_lexique.md L205-206, L230-236 ↔ conventions.md L232-235 (nine sibling commands) | 1_lexique.md | — |
| 23 | TO FIX | confirmed | The empty-attempt list always holds the concepteur's and testeur's commits | 8_code.md L105-108, L147-158 (reported L113 ↔ L110) | 8_code.md | — |
| 24 | TO FIX | confirmed | 4b stops on `blocked_relecteur.md`'s empty decision before the act meant to retire it | 8_code.md L227-233 ↔ 8_code.md L267-270, L572-581 | 8_code.md | — |
| 25 | TO FIX | confirmed | The "every heading has its number" test is applied to files that carry no `## Blocking N` | 8_code.md L49-55, L237-240 (reported L195) ↔ concepteur.md L143-149, testeur.md L182-188, relecteur.md L277-285, architecte.md L251 | 8_code.md | — |
| 26 | TO FIX | confirmed (F06) | The revert list is the whole history, so a second revert re-reverts; and a `sheet` cause on a lot that is not the last has no rule | 8_code.md L142-155, L186-189, L486-492 ↔ 8_code.md L595-598 | 8_code.md | chemins-aval F16 |
| 27 | TO FIX | confirmed | A signature rewritten after a `sheet` cause reaches no later sheet: the ordinary mode skips them and divergences are decided ones only | detailleur.md L507-519 ↔ relecteur.md L207-211, 8_code.md L272-289, L505-508 | detailleur.md | — |
| 28 | TO FIX | confirmed | The Arbitre polls for twenty minutes inside a worktree where the Product Owner's answer never appears | arbitre.md L466-478 ↔ 8_code.md L313-315, L564-567 | arbitre.md | — |
| 29 | TO FIX | confirmed (F10) | On a re-run the redécoupage count is bypassed; at the third the stop leaves the file untracked and nothing says what runs next | 8_code.md L548-549 ↔ 8_code.md L473-480, L510-518 | 8_code.md | chemins-aval F12 |
| 30 | TO FIX | confirmed | The Cadreur stacks two requests in one file; invocation 3 skips any file holding a filled verdict | cadreur.md L240-243 ↔ architecte.md L686-690 | architecte.md | — |
| 31 | TO FIX | confirmed | The Architecte raises `inconsistency` on every dash line the Convertisseur writes by design | convertisseur.md L862-864 ↔ architecte.md L413-422 | architecte.md | — |
| 32 | TO FIX | confirmed | No blocking-file shape names a block, so every `decisions-produit.md` line opens on a dash | 9_controle.md L366-374 ↔ detailleur.md L326-346, realisateur.md L299-311 | 9_controle.md | chemins-aval F15 |
| 33 | TO FIX | confirmed | `## Entries with no lot` holds three reasons; phase 1 marks all of them `carried` | cadreur.md L494, L762-774 ↔ 9_controle.md L149-154, L245-248 | 9_controle.md | — |
| 34 | QUESTION | — | Row 8 runs invocation 3 before invocation 1, so `INIT` never fires on a first feature that went through a bug-fix cycle | fusion.md L50 ↔ fusionneur.md L355-357 | fusion.md | — |
| 35 | QUESTION | — | Row 4 stops for good once `rapport-fusion.md` exists; a later `bugfix-NN` never carries its decisions into the global | fusion.md L46 ↔ fusion.md L18 | fusion.md | — |
| 36 | QUESTION | — | Row 3 cannot route an upstream blocking file, and re-invokes the Rédacteur with the blocking file alone | fusion.md L45 ↔ fusion.md L44, redacteur.md L750, fusion.md L101, L201 | fusion.md | chemins-amont F24 |
| 37 | QUESTION | — | Neither side says how `B<n>` is written inside a gap of `bug-list.md` | 9_controle.md L428 ↔ diagnostiqueur.md L616 | 9_controle.md | — |
| 38 | NOTE | — | Readers are sent to a `Vocabulary` heading the preamble does not carry | verificateur.md L62, L415 ↔ convertisseur.md L133-138, detailleur.md L68, L607 | verificateur.md | passages F10 |
| 39 | NOTE | — | `desc-bug.md` opens on `## Preamble`, `spec-technique.md` on `# Preamble` | diagnostiqueur.md L563 ↔ convertisseur.md L144 | diagnostiqueur.md | — |
| 40 | NOTE | — | A requirement filed under `## Trigger` never reaches `desc-bug.md` | diagnostiqueur.md L411 ↔ diagnostiqueur.md L515 | diagnostiqueur.md | — |
| 41 | NOTE | — | `## Placements not settled by the conventions` is written every time and read by nobody | concepteur.md L314 ↔ 8_code.md L57 | concepteur.md | — |
| 42 | NOTE | — | The Testeur's own test file lands under `## Outside the lot` | testeur.md L332 ↔ concepteur.md L118 | testeur.md | — |
| 43 | NOTE | — | `## Conventions requests` is a list nobody consumes | cadreur.md L848 ↔ 7_lots.md L194 | cadreur.md | — |
| 44 | NOTE | — | Both process documents still name `/cycle` | PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010 | PROCESS_AMONT.md | — |
| 45 | NOTE | — | The Arbitre says `/8_code` relays `code/redecoupage.md`'s headings; `/7_lots` is the reader | arbitre.md L210-211 ↔ 8_code.md L482-484 | arbitre.md | — |
| 46 | NOTE | — | `/8_code` resumes on `## Defects` alone and never looks for `code/blocked_verificateur.md` | 8_code.md L69-81 ↔ verificateur.md L176 | 8_code.md | — |
| 47 | NOTE | — | `par-genre/comportements.md` is said to be read by the Convertisseur, which never opens it | 5_reclasse.md L109 ↔ convertisseur.md L53 | 5_reclasse.md | — |
| 48 | NOTE | — | The blocking-file rename sits under *Git, before invoking* | conventions.md L165 ↔ conventions.md L228 | conventions.md | — |
| 49 | NOTE | — | "Invoke nothing, without a worktree" is decided after the worktree was created | 4_grille.md L305 ↔ 4_grille.md L266 | 4_grille.md | — |
| 50 | NOTE | — | Only a `NEW` block wipes `couverture.md`; a re-converted `MODIFIED` block leaves it standing | 2_structure.md L214 ↔ conventions.md L89 | 2_structure.md | — |
| 51 | NOTE | — | The blocking table names "one" file while the parallel invocations can leave several | 6_convertit.md L52 ↔ 6_convertit.md L191 | 6_convertit.md | — |
| 52 | NOTE | — | A waiting nature forces the assembly every run, and two relay rows match with no first-match rule | 6_convertit.md L417 ↔ 6_convertit.md L168 | 6_convertit.md | — |
| 53 | NOTE | — | `/1_lexique` and `/2_structure` bounce on the same state | 1_lexique.md L99 ↔ 2_structure.md L135 | 1_lexique.md | — |
| 54 | NOTE | — | After "4 wrote none" a `/1_lexique` run by mistake re-watches a corrected file | 1_lexique.md L60 ↔ 1_lexique.md L263 | 1_lexique.md | — |
| 55 | NOTE | — | "Once, not until it clears" has no record across runs | 3a_genre.md L258 ↔ 3b_nature.md L268 | 3a_genre.md | — |
| 56 | NOTE | — | The two-genre route can repeat as often as the rewrite still holds two genres | 3a_genre.md L256 ↔ qualifieur.md L100 | 3a_genre.md | — |
| 57 | NOTE | — | `.claude/commands/cycle.md` is still tracked and three `.claude/` files still name it | .claude/commands/cycle.md L1 ↔ .claude/CLAUDE.md L51 | .claude/CLAUDE.md | — |
| 58 | NOTE | — | A re-cut lot's reverted first commit still matches the grep; the Relecteur's diff carries every lot since | 8_code.md L98 ↔ 8_code.md L502 | 8_code.md | — |
| 59 | NOTE | — | `carried` is marked per entry, carried per block | 9_controle.md L152 ↔ 9_controle.md L173 | 9_controle.md | — |
| 60 | NOTE | — | The `Findings:` prompt names no lot; two lots without a sheet and the findings land on the wrong one | 8_code.md L302 ↔ detailleur.md L515 | 8_code.md | — |
| 61 | NOTE | — | The scope test reads files in `Modifies`, which carries symbols | audit_conventions.md L107 ↔ cadreur.md L822 | audit_conventions.md | — |
| 62 | NOTE | — | `git merge` "from the main checkout root" is issued by a session inside the worktree, and no command names the exit | 8_code.md L618 ↔ 8_code.md L102 | 8_code.md | — |
| 63 | NOTE | — | The Découpeur's blocking file is a field table with no `## Decision` to grep | decoupeur.md L136 ↔ 3_decoupe.md L38 | decoupeur.md | — |

---

## BLOCKING

### fichiers F02 — Phase 1's genre filter has no source, and forgets `transverse`

Severity: BLOCKING
Same as: chemins-aval F01 (BLOCKING) · chemins-aval F02 (BLOCKING — cites L133, the continuation of the L132 sentence) · passages F01 (BLOCKING) · passages F06 (TO FIX)
Where: 9_controle.md L39-42, L132-134, L187-193, L195 · convertisseur.md L172-173, L194-200, L749-754, L853-864 · qualifieur.md L74-86
Finding: Two sentences, both held. *(a)* Phase 1 keeps the blocks carrying `Genre: comportement` alone (L132), but its reading list (L39-42, "nothing else") holds `tracabilite.md` — identifier, title, entries (convertisseur L853-855) — and the `Anchor:` lines, none of which carries a genre, so the filter has no source and an orchestrator obeying *What you read* either opens the product file it forbids itself or keeps every block. *(b)* L133 says "the other four genres" and lists four, omitting `transverse` (qualifieur L74-86 counts six); a transverse block's code half is a numbered entry (convertisseur L172-173, L749-754) with an ordinary traceability line naming it (L194-200) that the Cadreur cuts a lot for, so that lot appears in no kept line of `tracabilite-full.md` and step d (L191-193) stops the command on every feature whose transverse rules gave code — and the transverse intentions are never confronted. L195 ("Every block appears") contradicts L132 inside the same phase.
Verdict: confirmed — 9_controle.md L39-42 name no file carrying a genre; L133 lists four genres against qualifieur.md L74's six.
Owner: 9_controle.md
Follows: —

### fichiers F01 — Every agent without Bash leaves its output uncommitted, and the verdict never reaches `HEAD`

Severity: BLOCKING
Same as: chemins-aval F08 (TO FIX)
Where: 8_code.md L105-108, L614-625 (reported L622-625) · relecteur.md L4, L46 · same three-step section in 7_lots.md L269-273, 9_controle.md L389-394, diagnostique.md L172-177
Finding: The Relecteur has no Bash (L4) and writes `code/<lot>/verdict.md` (L46) in the worktree — as do the Détailleur, Cadreur, Vérificateur, Contrôleur, Architecte and Diagnostiqueur, none of whose `tools:` line carries Bash; only the Concepteur, Testeur and Réalisateur commit (L105-108: "you do not commit for them"), and *Git, once it has reported* goes straight to merge, push, remove (L618-620), so the verdict sits uncommitted, `git merge` brings nothing of it, `git worktree remove` refuses, and L622-625 tells the orchestrator to blame the agent and stop rather than commit as `CLAUDE.md L7-8` expects — the file *Where to resume* keys on (L69-70) is never in the `HEAD` the next run resumes from. Only `/conventions` (L232-235) and `/8_code`'s split-back path (L513-515) carry the commit.
Verdict: confirmed — 8_code.md L614-625 hold no `git add`/`git commit`; relecteur.md L4 lists `Read, Grep, Glob, Write`.
Owner: 8_code.md
Follows: 7_lots.md, 9_controle.md, diagnostique.md — same section, same agents without Bash. Same mechanism upstream: entry 22.

### renommages F01 — An entry still waiting on the Product Owner reads as answered

Severity: BLOCKING
Same as: —
Where: arbitre.md L181-183, L194-198 · 8_code.md L233-240
Finding: The Arbitre says an entry waiting on the Product Owner is marked by "an empty number" under which no placeholder is written (L181-183) and, twelve lines later, that "its number is simply absent" (L194-195); `/8_code` counts a file filled by "the numbered lines under `## Decision`" against the `## Blocking N` headings (L237-240), so under the first wording the empty number is counted, the file reads as filled, is renamed (L235) and the entry waiting on her is archived unanswered. The chemins-aval *Sound* list read L183 as "leaves the number empty" and 4b as stopping — both readings stand in the text.
Verdict: confirmed — arbitre.md L183 and L195 describe two shapes; 8_code.md L238-239 counts numbered lines.
Owner: arbitre.md
Follows: 8_code.md — 4b's count keys on the shape the Arbitre writes

### chemins-amont F01 — The second time never re-runs once it asked, and `/5_reclasse` waits for it

Severity: BLOCKING
Same as: chemins-amont F27 (NOTE — scenario summary on the same two lines)
Where: 5_reclasse.md L50-62 · 4_grille.md L293-298, L546-548
Finding: Once the second time asked anything, its `questions-existant-NN.md` holds `### Q` for good — answered, integrated, filed under `questions/existant/`, never rewritten, since L296-298 says one such file anywhere ends the second time and writes nothing — while `/5_reclasse` L50-62 requires the highest `questions-existant-NN.md` to hold no `### Q` and otherwise says "run `/4_grille`", which (L548) says "`/5_reclasse`"; on any project that already has a global, the feature never leaves the grid.
Verdict: confirmed — 4_grille.md L296-298 write nothing once a file exists anywhere; 5_reclasse.md L61-62 stop on a `### Q` in the highest.
Owner: 4_grille.md
Follows: 5_reclasse.md — its closure test keys on what the second time writes

### chemins-amont F02 — "Decision first, then answer" leaves two questions files at the root

Severity: BLOCKING
Same as: —
Where: 3a_genre.md L255 · 2_structure.md L130-138 (row L133), L186-187, L249-255 · 3b_nature.md L265 (states the same dead end)
Finding: The route L255 prescribes ends at `/2_structure` with `blocked_qualifieur.md` filled and the answered `questions-qualifieur-NN.md` at the root together; row L133 matches first and names the blocking file alone (the prompt names one file — L186-187), L249 files only what was integrated, so the answered file stays beside the Rédacteur's own and every next command stops on two (2_structure L138, 1_lexique L63, 3a_genre L54) with no command that empties it — 3b_nature.md L265 says so in as many words for the classeur's case.
Verdict: confirmed — 3b_nature.md L265 describes exactly this outcome.
Owner: 2_structure.md — its table L133-134 dead-ends both orders (see the next entry), so neither relay row alone can settle it
Follows: 3a_genre.md L255

### chemins-amont F03 — "Answer first, decision once integrated" stops on the empty decision

Severity: BLOCKING
Same as: —
Where: 3b_nature.md L265 · 2_structure.md L134, L137
Finding: The route L265 prescribes reaches `/2_structure` with `blocked_classeur.md` still empty and the answered `questions-classeur-NN.md` at the root; row L134 ("one of the three with any `## Decision` empty → stop") precedes the row that would integrate the questions file (L137), so the command stops before integrating — the two are required at once, and each order (this entry, the previous) dead-ends.
Verdict: confirmed — 2_structure.md L134 sits above L137 in an ordered table.
Owner: 2_structure.md
Follows: 3b_nature.md L265

---

## TO FIX

### renommages F02 — A single-entry decision in the three-part shape is never counted filled

Severity: TO FIX
Same as: —
Where: arbitre.md L147-157 (reported L148), L177-179 · 8_code.md L234, L237-240 · detailleur.md L326-330, L346-351 and realisateur.md L299-311 (both expect "one numbered answer per blocking")
Finding: The Arbitre's decision template (L147-157) carries no number and "one number per `## Blocking N`" is stated only under *A file with several blockings* (L177-179), while the Détailleur and Réalisateur always write `## Blocking 1` even for one stop and `/8_code` reads a file as filled only when every heading has its number, "never when the field merely holds text" (L237-240) — a single-entry file settled in the three-part shape has one heading and no numbered line, matches row L234, is never renamed, and the lot stops on every later run.
Verdict: confirmed.
Owner: arbitre.md
Follows: 8_code.md

### renommages F03 — `## Where` cannot point at a request that has no name

Severity: TO FIX
Same as: —
Where: cadreur.md L196-198, L227-231, L240-243, L314 · 7_lots.md L167-168, L182-186
Finding: The dispatch keys on "the request its `## Where` names" inside `architecte/cadreur.md` (cadreur L314; 7_lots L167-168, L182-186 "the block the blocking file's `## Where` names is the one that counts"), but `## Where` is defined as "the lot, section or file" (L196-198) and the request blocks carry five headings and no identifier (L227-231, L240-243), so on a conventions block neither the Cadreur nor `/7_lots` can tell which verdict lifts it once the file holds more than one request.
Verdict: confirmed.
Owner: cadreur.md
Follows: 7_lots.md

### renommages F04 — A `forme` answer is written as a convention

Severity: TO FIX
Same as: passages F04 (TO FIX) — merged on the same `Kind:` passage (architecte.md L544-560); the cited lines differ (L546 / L556)
Where: architecte.md L544-546, L556-560, L634-652 · conventions.md L263-269
Finding: `forme` is the fifth `Kind:` (L545-546) whose answer "amends the grid, and the Product Owner does that herself" (L556-558), but invocation 2 turns "each answer into a rule" (L634) and exempts only `inconsistency` (L640-642) and `coverage` (L651-652), and `/conventions`'s relay table (L263-269) has no row for it, so a grid amendment lands in the conventions file as a rule.
Verdict: confirmed — architecte.md L634-652 name two exemptions, neither `forme`.
Owner: architecte.md
Follows: conventions.md — its relay table

### fichiers F03 — Step d's count can never match

Severity: TO FIX
Same as: —
Where: 9_controle.md L132, L187-189 · convertisseur.md L857-864
Finding: Step d requires the block count of `tracabilite.md` to equal the line count of `tracabilite-full.md` (L187-189), but the first lists every block, dash lines included (convertisseur L857-864), and phase 1 keeps behaviours alone (L132), so the check fails on every feature holding a directive, a reference, an out-of-scope or a constraint-only transverse block. A consequence of entry 1's filter. Shares convertisseur.md L862 with entry 31 — not merged: that line is the sound side of two different readers' defects.
Verdict: confirmed.
Owner: 9_controle.md
Follows: —

### fichiers F04 — A `NEW` block after the split deletes the technical document nobody can rebuild

Severity: TO FIX
Same as: chemins-amont F11 (TO FIX)
Where: 2_structure.md L202-210 · 6_convertit.md L35-38 · cadreur.md L61 (reads it)
Finding: `/2_structure` deletes `spec-technique.md` on any `NEW` block (L202-210) without testing `code/decoupage.md`, while `/6_convertit` refuses to run once the split is cut (L35-38), so an answer integrated after `/7_lots` leaves the Cadreur, the Vérificateur and the Détailleur with no technical document, the coded lots citing one that no longer exists, and no command that regenerates it.
Verdict: confirmed — 2_structure.md L202-210 carry no `code/decoupage.md` guard; 6_convertit.md L35 stops on it.
Owner: 2_structure.md
Follows: —

### fichiers F05 — The audit never sees the Convertisseur's blocks

Severity: TO FIX
Same as: —
Where: audit_blocages.md L26-36 · 6_convertit.md L343-350
Finding: The audit's four places (L26-30: `code/**/`, `cadrage-produit/`, the root, `investigation/`) leave out `convertisseur/`, where `/6_convertit` files `blocked_<nature>-NN.md` and `blocked_transversal-NN.md` (L343-350), so every block the Convertisseur ever raised is invisible to `/audit_blocages`.
Verdict: confirmed.
Owner: audit_blocages.md
Follows: —

### chemins-amont F04 — An answer naming a genre alone is never applied

Severity: TO FIX
Same as: —
Where: 3a_genre.md L88-97, L103-112, L154-155 · qualifieur.md L173, L185-186, L220, L323-324 · redacteur.md L103 (marks only a block it changes)
Finding: The answered qualifieur file is named only inside the invocation (L154-155), and the invocation is skipped when neither grep returns anything (L110); an asked block keeps `comportement` on its line meanwhile (qualifieur L173, L185-186) and "an answer naming a genre alone leaves the text as it was, and it is here that it lands" (L220), so the Rédacteur marks nothing, both greps return nothing, and the answer never lands — the block stays probed as a behaviour.
Verdict: confirmed.
Owner: 3a_genre.md
Follows: qualifieur.md — L220 places the landing in the invocation

### chemins-amont F05 — Same hole for the classeur

Severity: TO FIX
Same as: —
Where: 3b_nature.md L87-96, L102-113 · classeur.md L169-175
Finding: classeur L169-171 says a block an answer names has "its line filled and nothing marked it, so neither grep finds it", and `/3b_nature` L111 invokes nothing when neither grep finds anything, so an answer naming a nature alone is never applied when no other block needs the agent that turn.
Verdict: confirmed.
Owner: 3b_nature.md
Follows: classeur.md

### chemins-amont F06 — A product answer that changed no block re-asks the same question every run

Severity: TO FIX
Same as: —
Where: 6_convertit.md L143-144 · convertisseur.md L487-489, L632-634
Finding: Row L144 reruns a nature on a byte-identical part because "the answer changed no block" and "the rerun is what lifts the mark", but the agent opens no questions file except the answered technical one the prompt names (L632-634) and a mark is lifted "once the answer is in the product file" (L487-489), so it meets the same gap, marks `<<ASSUMED` again and re-asks — one opus invocation per run, the mark never lifted.
Verdict: confirmed.
Owner: 6_convertit.md
Follows: convertisseur.md

### chemins-amont F07 — A turn whose answers changed no block cannot close the grid

Severity: TO FIX
Same as: —
Where: 4_grille.md L176-183, L197-204 · 2_structure.md L98-103, L249-250 · redacteur.md L103
Finding: A turn whose answers changed no block leaves no marker (the Rédacteur marks only what it changes, redacteur L103) and no empty file (the answered one is filed under `questions/sondeur/`, 2_structure L249-250, still holding its `### Q`), and row L204 says "stop, `/4_grille` again once a marker or an empty file is there" — nothing downstream produces either, so the grid cannot close on that feature.
Verdict: confirmed.
Owner: 4_grille.md
Follows: 2_structure.md

### chemins-amont F08 — The `### Q` guard stops on the architecte's waiting file

Severity: TO FIX
Same as: —
Where: 3a_genre.md L54-59, L71-73 · conventions.md L122-126 · same guard in 3b_nature.md L53-58, 3_decoupe.md L51-54, 4_grille.md L102-104 and L210-215, 5_reclasse.md L80-82, 6_convertit.md L62-65, fusion_compare.md L50-53
Finding: The guard runs over every root `questions-*.md` (L54) and the architecte exception is stated only for the filing that follows it (L71-73) — where `/conventions` L122-126 states it for the guard itself — so a `questions-architecte-NN.md` waiting on the Product Owner stops seven commands instead of being read as absent; only `/1_lexique` (L68-71) and `/2_structure` (L166-169) say to read the root as if it were not there.
Verdict: confirmed.
Owner: 3a_genre.md
Follows: 3b_nature.md, 3_decoupe.md, 4_grille.md, 5_reclasse.md, 6_convertit.md, fusion_compare.md

### chemins-amont F09 — Two commands file the architecte's answered file where nobody reads it

Severity: TO FIX (as reported)
Same as: —
Where: 3_decoupe.md L51-59 · 5_reclasse.md L80-90 · fusion_compare.md L50-59 · fusion.md L47, L113-117 · fusion_applique.md L175-179 · conventions.md L85, L109-112
Finding: As reported, `/3_decoupe`, `/5_reclasse`, `/fusion`, `/fusion_compare` and `/fusion_applique` file every root `questions-*.md` with no architecte exception, and invocation 2 needs the file at the root (conventions L85), so an answered architecte file filed away loses its answers.
Verdict: overstated — TO FIX → NOTE. In `/3_decoupe` (L51-54), `/5_reclasse` (L80-82) and `/fusion_compare` (L50-53) the `### Q` guard stops the command on the `### Q` an answered file necessarily holds, before L56, L87 and L55 file anything — those three exhibit entry 17, not this. Only `/fusion` (row 5 L47 passes an answered file; L113-117 file it) and `/fusion_applique` (L175-179) file it, and only at fusion time, on a file the Product Owner answered without running `/conventions` since.
Owner: fusion.md
Follows: fusion_applique.md

### chemins-amont F10 — `/2_structure` stops on a settled vocabulary after "4 wrote none"

Severity: TO FIX
Same as: —
Where: 2_structure.md L27-29, L86-90, L140-143 · 1_lexique.md L205-210, L217-221, L263
Finding: "Grep it for `### Q`, one hit and you stop, answered or not" (L86-87) with "it" defined at L27-29 as the highest lexicographe file *at the root or filed*; invocation 4 files the file it applied (1_lexique L205-206) and writes a new one only when it asked (L208-210, L220-221), so after "4 wrote none" (L263 → `/2_structure`) the applied file under `questions/lexicographe/` is the highest, holds entries, and `/2_structure` stops on a settled vocabulary. Invocations 1-2 end on an empty file (1_lexique L217-218); 3-4 do not.
Verdict: confirmed.
Owner: 2_structure.md
Follows: 1_lexique.md

### chemins-amont F12 — The second decoupeur runs outside any worktree

Severity: TO FIX
Same as: —
Where: 3_decoupe.md L204-207 · 3_decoupe.md L175-181, L129-132
Finding: The re-invocation on a short list (L204-207) is written under *What you relay*, after *Git, once it has reported* has merged and removed the worktree (L179-181), so the second decoupeur runs in no isolated session and its writes are blocked (L129-132 say why the worktree is entered first).
Verdict: confirmed.
Owner: 3_decoupe.md
Follows: —

### chemins-amont F13 — An empty architecte file sticks at the root and answers "/7_lots" for ever

Severity: TO FIX
Same as: —
Where: conventions.md L75-76, L86-90, L137-140
Finding: An empty `questions-architecte-NN.md` is never integrated, so L137-140 ("every integrated `questions-architecte-*.md`") never files it, and row L86 precedes rows L87-90 in a first-match walk (L75-76), so once a derivation asked nothing every later run of that folder answers "`/7_lots`" — including after `/2_structure` wiped `couverture.md` for a `NEW` block (L214-221), when invocation 4 (row L88) should walk it.
Verdict: confirmed.
Owner: conventions.md
Follows: —
Side missing: the Architecte's side — the empty file it writes at invocation 1 or 4 — is named by no report.

### chemins-amont F14 — No upstream command commits inside the worktree before merging

Severity: TO FIX
Same as: —
Where: 1_lexique.md L205-206, L230-236 · conventions.md L232-235 · same section in 2_structure.md L273-279 (its `git mv` L249-250), 3_decoupe.md L175-181, 3a_genre.md L223-229, 3b_nature.md L228-234, 4_grille.md L511-517, 6_convertit.md L378-384, fusion.md L220-226, fusion_compare.md L140-146, fusion_applique.md L142-148
Finding: Only `/conventions` commits inside the worktree before merging (L232-235, which says why: the agent has no Bash, `git merge` takes the branch's commits not the worktree's files, `git worktree remove` refuses a dirty tree); every other upstream command goes straight to `git merge --no-ff`, and none of its agents has Bash (every `tools:` line under `.claude-new/agents/`), so the merge brings nothing, the remove refuses, and the agent's writes plus the in-worktree `git mv` (1_lexique L205-206, 2_structure L249-250) stay on the branch. Same mechanism as entry 2; here it reaches every write of every upstream agent, not one file.
Verdict: confirmed.
Owner: 1_lexique.md
Follows: 2_structure.md, 3_decoupe.md, 3a_genre.md, 3b_nature.md, 4_grille.md, 6_convertit.md, fusion.md, fusion_compare.md, fusion_applique.md

### chemins-aval F03 — An empty attempt is never detected

Severity: TO FIX
Same as: —
Where: 8_code.md L105-108, L147-158, L164-167 (reported L113 ↔ L110)
Finding: The empty-attempt test is "an empty list" from `git log --grep="^<lot>: "` (L151, L157), but the Concepteur and Testeur commit under the same `<lot>: ` prefix before the Réalisateur runs (L105-108), so the list is never empty once they ran; a Réalisateur that commits nothing is not detected, the Relecteur is invoked on declarations and red tests, and the in-run count (L164-167) never fires.
Verdict: confirmed.
Owner: 8_code.md
Follows: —
Side missing: the commit-message rule of concepteur.md, testeur.md and realisateur.md is the other side of that list and is named by no report.

### chemins-aval F04 — 4b stops on `blocked_relecteur.md`'s empty decision before the act that retires it

Severity: TO FIX
Same as: —
Where: 8_code.md L227-233 · 8_code.md L267-270, L572-581 · relecteur.md L277-285 (its `## Decision` left empty by shape)
Finding: 4b looks for any `blocked_*.md` in `code/<lot>/` before invoking anything and stops on an empty `## Decision` (L227-233), while `blocked_relecteur.md` keeps its `## Decision` empty by design until the fresh Réalisateur or the Détailleur has reported (L267-270, L579-581), so the act meant to retire it is never reached under the first rule, and every Relecteur block stops on the Product Owner — the two rules stand in the same file and say opposite things about that file.
Verdict: confirmed — 8_code.md L233 and L267-270 both stand.
Owner: 8_code.md
Follows: —
Side missing: relecteur.md L277-285 (the shape whose `## Decision` is empty) is named by no report.

### chemins-aval F05 — The "every heading has its number" test is applied to files that carry no `## Blocking N`

Severity: TO FIX
Same as: —
Where: 8_code.md L49-55, L235, L237-240 (reported L195) · concepteur.md L143-149 · testeur.md L182-188 · relecteur.md L277-285 · architecte.md L251 · arbitre.md L142-143 (states the four-heading shape)
Finding: The filled test — "a file is filled when every heading has its number, never when the field merely holds text" (L237-240), read for every `blocked_*.md` (L49-55) — is applied to the Concepteur's, Testeur's, Relecteur's and Architecte's files, which carry four `##` headings and no `## Blocking N` (arbitre L142-143 says so), so an answer the Product Owner writes as text under their `## Decision` reads as not filled and those blocks never lift; a reading by count (zero headings, zero numbers) says the opposite, and the text gives both.
Verdict: confirmed.
Owner: 8_code.md
Follows: —

### chemins-aval F06 — The revert list is the whole history; and a `sheet` cause on a lot that is not the last has no rule

Severity: TO FIX
Same as: chemins-aval F16 (NOTE) — same line, a different sentence; both reported
Where: 8_code.md L142-155, L186-189, L486-492 · 8_code.md L595-598
Finding: *(F06)* The revert list is the whole-history `git log --grep="^<lot>: "` (L151, reused at L186 and L489), which after one revert still lists the commits already reverted, so a second `sheet` cause or a redécoupage on the same lot reverts them again, conflicts, and stops the command on the Product Owner (L187-189). *(F16)* A filled decision on a lot already carrying a PASS re-runs its agent and its review (L595-598), and a `sheet` cause there reverts commits later lots built on, with no rule for a lot that is not the last coded.
Verdict: confirmed for F06's sentence; F16 (NOTE) not verified beyond the shared line.
Owner: 8_code.md
Follows: —

### chemins-aval F07 — A signature rewritten after a `sheet` cause reaches no later sheet

Severity: TO FIX
Same as: —
Where: detailleur.md L507-519 · relecteur.md L207-211 · 8_code.md L193-197, L272-289, L505-508
Finding: A sheet rewritten after a `sheet` cause (8_code L193-197; detailleur L515-519) can change a signature the block's later sheets consume, the ordinary mode skips every sheet already there (detailleur L511-512; 8_code L505-506), and `## Symbol divergences` covers decided divergences only (relecteur L209-211), the one trigger of move 5 (8_code L272-289), so the later lots are conceived and tested against a signature that no longer exists and nothing rewrites their sheets.
Verdict: confirmed.
Owner: detailleur.md
Follows: 8_code.md — move 5 keys on `## Symbol divergences` alone

### chemins-aval F09 — The Arbitre's twenty-minute poll cannot see the Product Owner's answer

Severity: TO FIX
Same as: —
Where: arbitre.md L466-478 · 8_code.md L102-103, L313-315, L564-567
Finding: The Arbitre polls the blocking file with `sleep` for up to twenty minutes (L466-478) from inside the worktree the run entered (8_code L102-103), where — by the command's own account of `stop.md` (L313-315) — a file the Product Owner writes in the main checkout never appears; and the blocking file is itself unmerged, so the only copy she could fill is the worktree's. Every product question costs twenty minutes and ends empty.
Verdict: confirmed — the premise that she writes in the main checkout is the command's own (L313-315), not measured.
Owner: arbitre.md
Follows: 8_code.md — L564-567 rests on the wait having been made

### chemins-aval F10 — The redécoupage count is bypassed on a re-run, and the third stop is incomplete

Severity: TO FIX
Same as: chemins-aval F12 (NOTE) — same line, a different sentence; both reported
Where: 8_code.md L548-549 · 8_code.md L473-480, L510-518
Finding: *(F10)* On a re-run, a Détailleur reporting that `code/redecoupage.md` is still there sends the command straight to `/7_lots` (L548-549), bypassing the count of archived redécoupages (L473-480), so the third-return stop holds only inside the run that hit it and a fourth split is cut anyway. *(F12)* At the third redécoupage the command stops before the revert, the deletions and the commit that carry `code/redecoupage.md` (L510-518), so the file the Product Owner is to decide on sits untracked in a worktree that cannot be removed, and no row of any command says what runs after her decision.
Verdict: confirmed for F10's sentence; F12 (NOTE) not verified beyond the shared line.
Owner: 8_code.md
Follows: 7_lots.md — F12's "what runs after her decision"
Side missing: the Détailleur's report wording that L548 keys on ("waits on the split") is named by no report.

### passages F02 — The second request of a settled file is never answered

Severity: TO FIX
Same as: —
Where: cadreur.md L240-243 · architecte.md L686-690 · 7_lots.md L182-186, L194-199 and 8_code.md L329-332 (read per request)
Finding: The Cadreur stacks two requests in one `architecte/cadreur.md`, "a fresh heading block, below" a filled `## Verdict` (L240-243), while invocation 3 greps the folder for a filled verdict and "skip[s] those files" (L686-687), so the second request of a file whose first is settled is never opened and the Cadreur's block stands for good — `/7_lots` and `/8_code` glob per request, the Architecte per file.
Verdict: confirmed.
Owner: architecte.md
Follows: cadreur.md — the writer of the stacked shape, should the shape be what moves

### passages F03 — The Architecte questions every dash line the Convertisseur writes on purpose

Severity: TO FIX
Same as: —
Where: convertisseur.md L862-864 · architecte.md L413-422
Finding: `tracabilite.md` carries a dash for every directive, out-of-scope, recette and constraint-only transverse block by design (L862-864: "a dash says someone looked and found none"), while the Architecte raises an `inconsistency` question on every dash line (L417, L420), so each derivation asks the Product Owner about blocks that produced no entry on purpose. Shares L862 with entry 10 — not merged, see there.
Verdict: confirmed. Origin pre-existing.
Owner: architecte.md
Follows: —

### passages F05 — `decisions-produit.md` never gets a block identifier

Severity: TO FIX
Same as: chemins-aval F15 (NOTE)
Where: 9_controle.md L366-374 · detailleur.md L326-346 · realisateur.md L299-311
Finding: Phase 6 opens each line on the `B<n>` "when the blocking file names the block" (L369-374), but no blocking-file shape carries one — the Détailleur's heading names a lot and its `### Where` "the lot, section or file" (L326-340), the Réalisateur's nothing (L303-307) — so every line opens on a dash and the Rédacteur, at `/fusion` invocation 3 (L378-382), places each decision by reading alone.
Verdict: confirmed.
Owner: 9_controle.md
Follows: — (redacteur.md is the downstream reader of the line, named by no report)

### passages F07 — Every entry with no lot reads as already built

Severity: TO FIX
Same as: —
Where: cadreur.md L494, L762-774 · 9_controle.md L149-154, L245-248
Finding: `## Entries with no lot` holds three reasons — "already carried by the code" (cadreur L494), "carried by §4.1 and §5.2, nothing of its own to build" and "attributing a rule to another, or setting a boundary" (L767-770) — and phase 1 reads it as one ("an entry the code already carries", L151-152) and marks every entry there `carried`, so a block whose entries are all attributed elsewhere is reported found and no sheet is read for it (L245-248).
Verdict: confirmed.
Owner: 9_controle.md
Follows: —

---

## QUESTION

### fichiers F08 — Row 8 runs invocation 3 before invocation 1, and `INIT` never fires

Severity: QUESTION
Same as: —
Where: fusion.md L50 · fusionneur.md L355-357
Finding: Row 8 runs invocation 3 before invocation 1 and invocation 3 writes into the global, so on a first feature that went through a bug-fix cycle the global no longer holds `# Application` alone when invocation 1 tests it, `INIT` never fires, and the whole feature is merged sentence by sentence into a near-empty global.
Verdict: — (not verified: below TO FIX)
Owner: fusion.md
Follows: fusionneur.md

### chemins-amont F25 — A `bugfix-NN` coded after the merge never carries its decisions into the global

Severity: QUESTION
Same as: —
Where: fusion.md L46 · fusion.md L18
Finding: Row 4 stops for good once `rapport-fusion.md` exists, so a `bugfix-NN` coded after the merge never carries its decisions into the global.
Verdict: — (not verified)
Owner: fusion.md
Follows: —

### passages F08 — Row 3 cannot route an upstream blocking file, and re-invokes the Rédacteur with the blocking file alone

Severity: QUESTION
Same as: chemins-amont F24 (NOTE) — same line, a different sentence; both reported
Where: fusion.md L45 · fusion.md L44, L101, L201 · redacteur.md L750
Finding: *(passages F08)* Row 3 re-invokes the Rédacteur at invocation 3 with the blocking file alone (L201), the decisions files being named only when row 6 fires (L101); whether the agent carries on folding after writing `blocked_redacteur.md` is not said, and if it stops there the decisions after the blocked one are never folded. *(chemins-amont F24)* Rows 2-3 catch any `blocked_*.md`, and an upstream file such as `blocked_qualifieur.md` carries no `## Invocation` line, so a filled one at fusion time routes to an agent at an invocation the row cannot name.
Verdict: — (not verified)
Owner: fusion.md
Follows: redacteur.md

### chemins-aval F19 — Neither side says how `B<n>` is written inside a gap of `bug-list.md`

Severity: QUESTION
Same as: —
Where: 9_controle.md L428 · diagnostiqueur.md L616
Finding: Neither side says how the `B<n>` is written inside a gap of the hand-written `bug-list.md`, so the Diagnostiqueur has no pattern to read it by and a gap carrying it in another form loses the `carried` mark at the next control.
Verdict: — (not verified)
Owner: 9_controle.md
Follows: diagnostiqueur.md

---

## NOTE

### renommages F05 — Readers are sent to a `Vocabulary` heading the preamble does not carry

Severity: NOTE
Same as: passages F10 (NOTE)
Where: verificateur.md L62, L415 · convertisseur.md L133-138 · detailleur.md L68, L607
Finding: The Vérificateur and the Détailleur send readers to the preamble's `Vocabulary`, a heading the technical document does not carry — its part is `## Intent and vocabulary` — so a reader that greps the name it was given finds nothing.
Verdict: —
Owner: verificateur.md
Follows: detailleur.md

### renommages F06 — `desc-bug.md` opens on `## Preamble`, `spec-technique.md` on `# Preamble`

Severity: NOTE
Same as: —
Where: diagnostiqueur.md L563 · convertisseur.md L144
Finding: The Convertisseur says the single `#` is how the Cadreur tells the preamble apart at a glance and never cuts it; on a bug-fix cycle the preamble sits at the same level as the sections it must never cut.
Verdict: —
Owner: diagnostiqueur.md
Follows: —

### renommages F07 — A requirement filed under `## Trigger` never reaches `desc-bug.md`

Severity: NOTE
Same as: —
Where: diagnostiqueur.md L411 · diagnostiqueur.md L462, L515
Finding: A second requirement may be filed under `## Trigger` "when it is the trigger", but invocation 2 writes each entry from `## Today` and `## Expected` and reads `## Trigger` nowhere, so the Cadreur cuts a lot that cannot be built.
Verdict: —
Owner: diagnostiqueur.md
Follows: —

### renommages F08 — `## Placements not settled by the conventions` is written every time and read by nobody

Severity: NOTE
Same as: —
Where: concepteur.md L314 · 8_code.md L57
Finding: `/8_code` opens `conception.md` for `## Decision applied` alone and the Relecteur for `## Declared` and `## Outside the lot`, so the field costs a mandatory line and settles nothing the `architecte/` request does not already carry.
Verdict: —
Owner: concepteur.md
Follows: —

### renommages F09 — The Testeur's own test file lands under `## Outside the lot`

Severity: NOTE
Same as: —
Where: testeur.md L87, L332 · concepteur.md L118 · realisateur.md L223 · relecteur.md L453
Finding: A test file the Testeur creates is in neither `## Files` nor `## Declared`, so by its own definition it lands under `## Outside the lot`, the field reserved for a file "a decision authorised", and the lot's own test file is reported as an intrusion the Relecteur then treats as declared.
Verdict: —
Owner: testeur.md
Follows: relecteur.md

### renommages F10 — `## Conventions requests` is a list nobody consumes

Severity: NOTE
Same as: —
Where: cadreur.md L848 · 7_lots.md L194
Finding: The section is written in `code/decoupage.md` so a fast-path request is "not invisible", but `/7_lots` finds requests by globbing `architecte/` and no agent reads the section.
Verdict: —
Owner: cadreur.md
Follows: —

### renommages F11 — Both process documents still name `/cycle`

Severity: NOTE
Same as: —
Where: PROCESS_AMONT.md L1210 · PROCESS_AVAL.md L1010
Finding: Both still say "`/cycle` ne l'appelle pas", naming a command the chain removed. Not opened here — `docs/process/` is the Product Owner's.
Verdict: —
Owner: PROCESS_AMONT.md
Follows: PROCESS_AVAL.md

### fichiers F06 — The Arbitre names `/8_code` as the reader of `code/redecoupage.md`'s headings

Severity: NOTE
Same as: —
Where: arbitre.md L210-211 · 8_code.md L482-484 · 7_lots.md L297-299
Finding: `/8_code` relays nothing of the file and `/7_lots` is the reader — a wrong pointer, no functional cost.
Verdict: —
Owner: arbitre.md
Follows: —

### fichiers F07 — `/8_code` never looks for `code/blocked_verificateur.md`

Severity: NOTE
Same as: —
Where: 8_code.md L69-81 · verificateur.md L176
Finding: `/8_code` resumes on `## Defects` alone, so a run whose check blocked after the Cadreur re-cut codes against the previous round's `code/sequence.md`.
Verdict: —
Owner: 8_code.md
Follows: —

### fichiers F09 — `par-genre/comportements.md` is said to be read by the Convertisseur

Severity: NOTE
Same as: —
Where: 5_reclasse.md L109 · convertisseur.md L53
Finding: The Convertisseur opens only `convertisseur/<nature>-input.md` cut from `desc-par-nature.md`; the file's only reader is `/5_reclasse`'s own second move — a misnamed reader, no functional cost.
Verdict: —
Owner: 5_reclasse.md
Follows: —

### chemins-amont F15 — The blocking-file rename sits under *Git, before invoking*

Severity: NOTE
Same as: —
Where: conventions.md L165-172 · conventions.md L228-239
Finding: The "once it has reported" section has no rename, so an applied `blocked_architecte.md` is renamed only if the orchestrator reads out of order — left unnumbered, the next run stops on it.
Verdict: —
Owner: conventions.md
Follows: —

### chemins-amont F16 — "Invoke nothing, without a worktree" is decided after the worktree was created

Severity: NOTE
Same as: —
Where: 4_grille.md L305-307 · 4_grille.md L266-268
Finding: A feature attaching to nothing leaves an orphan worktree behind every second time.
Verdict: —
Owner: 4_grille.md
Follows: —

### chemins-amont F17 — A re-converted `MODIFIED` block leaves `couverture.md` standing

Severity: NOTE
Same as: —
Where: 2_structure.md L214 · conventions.md L89
Finding: Only a `NEW` block wipes `couverture.md`, so after a `MODIFIED` block is re-converted invocation 4 finds "nothing to do" and the rewritten entries are never walked against the conventions.
Verdict: —
Owner: 2_structure.md
Follows: —

### chemins-amont F18 — The blocking table names "one" file while several can stand

Severity: NOTE
Same as: —
Where: 6_convertit.md L52 · 6_convertit.md L191
Finding: Two blocked natures with one decision filled and one empty have no written outcome.
Verdict: —
Owner: 6_convertit.md
Follows: —

### chemins-amont F19 — A waiting nature forces the assembly every run, and two relay rows match

Severity: NOTE
Same as: —
Where: 6_convertit.md L417 · 6_convertit.md L168
Finding: When its section is absent the run ends on an empty questions file that matches both the "waiting" and the "`/conventions`" relay rows with no first-match rule.
Verdict: —
Owner: 6_convertit.md
Follows: —

### chemins-amont F20 — `/1_lexique` and `/2_structure` bounce on the same state

Severity: NOTE
Same as: —
Where: 1_lexique.md L99 · 2_structure.md L135
Finding: With `desc-produit.md` present and nothing at the root, `/1_lexique` says "`/2_structure`" and `/2_structure` stops on that state saying "`/3_decoupe`" — one wasted run per bounce.
Verdict: —
Owner: 1_lexique.md
Follows: 2_structure.md

### chemins-amont F21 — A `/1_lexique` run by mistake after "4 wrote none" re-watches a corrected file

Severity: NOTE
Same as: —
Where: 1_lexique.md L60 · 1_lexique.md L263
Finding: The answered file sits alone at the root and reads as invocation 3 again — one opus invocation.
Verdict: —
Owner: 1_lexique.md
Follows: —

### chemins-amont F22 — "Once, not until it clears" has no record across runs

Severity: NOTE
Same as: —
Where: 3a_genre.md L258 · 3b_nature.md L268
Finding: Nothing tells the second run it is the second, so the exit rests on the Product Owner counting.
Verdict: —
Owner: 3a_genre.md
Follows: 3b_nature.md

### chemins-amont F23 — The two-genre route can repeat on the same block

Severity: NOTE
Same as: —
Where: 3a_genre.md L256 · qualifieur.md L100
Finding: The route block → `/2_structure` → `/3_decoupe` → `/3a_genre` repeats as often as the rewrite still holds two genres; only the Product Owner's decision bounds it.
Verdict: —
Owner: 3a_genre.md
Follows: qualifieur.md

### chemins-amont F26 — `.claude/commands/cycle.md` is still tracked and named

Severity: NOTE
Same as: —
Where: .claude/commands/cycle.md L1 · .claude/CLAUDE.md L51 · .claude/commands/conventions.md L43 · .claude/commands/socle.md L19
Finding: No command under `.claude-new/` names `/cycle`, but the old tree still tracks and names it.
Verdict: —
Owner: .claude/CLAUDE.md
Follows: .claude/commands/conventions.md, .claude/commands/socle.md

### chemins-aval F11 — A re-cut lot's Relecteur diff carries every lot coded since

Severity: NOTE
Same as: —
Where: 8_code.md L98 · 8_code.md L502
Finding: A re-cut lot keeps its number and its reverted first commit still matches the `git log` grep, so the Relecteur's file list is the diff from before the redécoupage, which its `## Outside the lot` check reads as this lot's.
Verdict: —
Owner: 8_code.md
Follows: —

### chemins-aval F13 — `carried` is marked per entry, carried per block

Severity: NOTE
Same as: —
Where: 9_controle.md L152 · 9_controle.md L173
Finding: A block with one built entry and one entry the code already carried is either wholly `carried` or reported missing.
Verdict: —
Owner: 9_controle.md
Follows: —

### chemins-aval F14 — The `Findings:` prompt names no lot

Severity: NOTE
Same as: —
Where: 8_code.md L302 · detailleur.md L515
Finding: The Détailleur finds the lot as the one with no sheet, so after a run that stopped at move 4 of a later lot two lots have none and the findings land on the wrong one.
Verdict: —
Owner: 8_code.md
Follows: detailleur.md

### chemins-aval F17 — The scope test reads files in `Modifies`, which carries symbols

Severity: NOTE
Same as: —
Where: audit_conventions.md L107 · cadreur.md L822-826
Finding: The lot list carries files in `Touches` and symbols in `Modifies`, so finding 2 is applied on the wrong field.
Verdict: —
Owner: audit_conventions.md
Follows: —

### chemins-aval F18 — The merge "from the main checkout root" is issued from inside the worktree

Severity: NOTE
Same as: —
Where: 8_code.md L618 · 8_code.md L102-103
Finding: The harness refuses a git command aimed at the main checkout from a worktree-isolated session, so the merge needs an exit from the worktree that no command names — the same three-step section stands in every agent-invoking command.
Verdict: —
Owner: 8_code.md
Follows: every command carrying the same *Git, once it has reported* section (the nine of entry 22, plus 7_lots.md, 9_controle.md, diagnostique.md, conventions.md)

### passages F09 — The Découpeur's blocking file has no `## Decision` to grep

Severity: NOTE
Same as: —
Where: decoupeur.md L136 · 3_decoupe.md L38 · 2_structure.md L155
Finding: The file is given as a field table with no `##` form, while `/3_decoupe` and `/2_structure` grep `^## Decision$`, so a file written as the table reads stops nothing and routes nowhere.
Verdict: —
Owner: decoupeur.md
Follows: —

---

76 findings went in; 63 entries came out (13 merges).
40 findings (9 BLOCKING, 31 TO FIX) were verified against the files: 39 `confirmed`, 1 `overstated` (chemins-amont F09, TO FIX → NOTE), 0 `stale`, 0 `wrong`.
