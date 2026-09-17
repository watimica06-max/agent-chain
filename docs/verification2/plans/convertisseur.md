# convertisseur — correction plan

Built against `.claude-new/agents/convertisseur.md`, `.claude-new/commands/6_convertit.md`,
`.claude-new/commands/cycle.md` (the two commands that name the agent),
`docs/verification2/convertisseur.md` (both parts), `docs/verification2/decisions.md`,
and the six thematic reports filtered on `convertisseur`.

Every line number below was read in the file it names, in this worktree.

---

## Part 1 — the twenty-two findings

### convertisseur.md F01 — c.4's command half is missing

Verdict: confirmed
Decision: Make the resolving script, or its check after resolution, report a `[B<n>:` whose `]` is not on the same line as a fault instead of skipping it.
Where: 6_convertit.md L236-246 ↔ passes/convertisseur.md L125-150 (c.4)
Cited: 6_convertit.md L245 — "Replace, never read — one entry leaves nothing to judge, and that is the only case you touch" — nothing about a bracket that does not close on its line; the agent half stands at convertisseur.md L459-462.
Owner: 6_convertit
Also in: commandes

### convertisseur.md F02 — the index says every nature reads `transverses.md`, the file says invocation 2 alone

Verdict: confirmed
Decision: —  *(see `## To settle` 1)*
Where: modifications.md L547 ↔ convertisseur.md L146-147
Cited: modifications.md L547 — "Les transverses | Toutes les invocations de nature — elles en tirent leurs entrées et leurs lignes de préambule"; convertisseur.md L146-147 — "Invocation 2 does this, alone — no nature invocation opens `par-genre/transverses.md`."
Owner: —
Also in: commandes (5_reclasse side), cadreur —

The report's part 2 row *« 1 — transverses to every nature invocation | other »* says the wiring is *« as the demand asked »* — it is not: the demand asked every nature invocation, the file gives it to one. The divergence is deliberate (L149-153 gives its reason) and is the question in `## To settle` 1.

### convertisseur.md F03 — the *settle* row was narrowed against the index

Verdict: confirmed
Decision: Treat with F12 — the narrowing produced an empty case; F12's decision replaces it.
Where: modifications.md L590 ↔ convertisseur.md L363
Cited: modifications.md L590 — "Il tranche | Renommer un symbole · ranger une règle dans une section plutôt qu'une autre · choisir une comparaison"
Owner: convertisseur
Also in: —

### convertisseur.md F04 — invocation 2 reads a product-file text the file calls empty

Verdict: confirmed
Decision: Remove *« the product file, its text outside the blocks »* from invocation 2's Reads; the headings, already listed, are what move 2 and move 5 use.
Where: convertisseur.md L632 ↔ convertisseur.md L717
Owner: convertisseur
Also in: —

### convertisseur.md F05 — `references.md` is given to an invocation that does not exist

Verdict: confirmed
Decision: Name invocation 2 in the `references.md` row, and give invocation 2 a move that opens the file and writes §9 Text from it, before move 3 resolves the brackets.
Where: convertisseur.md L52 ↔ convertisseur.md L632, L88, L710-808
Owner: convertisseur
Also in: —

The second half is the report's part 2 row *« 1 — references to the transversal, §9 Text | other »*: L88 names `references.md` as §9's source and L632 lists it under invocation 2's reads, but none of moves 1-6 (L710-808) opens it — move 4 writes §9 from *Resources* alone (L774-777). Confirmed by reading the seven moves. Without the move, the row and the section table promise a source nobody reads.

### convertisseur.md F06 — « never settle anything » beside a *You settle* table

Verdict: confirmed
Decision: Narrow the headline at L3 and L18 to product matters, which is what L602 already says, so the reversibility table is no longer contradicted.
Where: convertisseur.md L3, L18 ↔ convertisseur.md L355-363, L602
Owner: convertisseur
Also in: —

### convertisseur.md F07 — « the only case » has a second case

Verdict: confirmed
Decision: State both exceptions to the *never write a number outside your own section* rule — the transverse entry of move 2b and the *Resources* entry of move 4 — and drop the *only case* claim.
Where: convertisseur.md L179-180 ↔ convertisseur.md L774-778, L596-597
Owner: convertisseur
Also in: —

### convertisseur.md F08 — three lines against four for one shape

Verdict: confirmed
Decision: Count both question shapes the same way, heading included or excluded for both, and align L474-475 with the count chosen.
Where: convertisseur.md L371-376 ↔ convertisseur.md L410-416, L474-475
Owner: convertisseur
Also in: —

### convertisseur.md F09 — `Entries: §3.2, §7.1` names a number outside the writer's section

Verdict: confirmed
Decision: Make the `Entries:` line obey the reference rule of L285-291 — own numbers inside the section, a bracket reference outside it at invocation 1, any number at invocation 2 — and fix the example.
Where: convertisseur.md L374 ↔ convertisseur.md L224-225, L285-291, L596
Owner: convertisseur
Also in: —

### convertisseur.md F10 — a transverse block has no `## Trace` line anywhere

Verdict: confirmed
Decision: Have move 2b record, for every transverse block, the entry it gave or the preamble part that holds it, where move 3 reads it; make move 3 resolve a reference to a transverse block from that record; and exclude transverse blocks from the *fault of invocation 1* rule at L763-765.
Where: convertisseur.md L746-748, L763-765 ↔ convertisseur.md L146-147, L681, L722-734
Owner: convertisseur
Also in: —

Verified: only invocation 2 opens `transverses.md` (L146-147); a nature's `## Trace` covers *« one line per block of yours »* (L684); move 3 walks Trace, then `## Preamble` (L746), then *« neither → fault of invocation 1 »* (L763-765). A transverse block's reference therefore always hits the fault rule, even after move 2b wrote its entry. ⚠️ Voided if `## To settle` 1 chooses route A.

### convertisseur.md F11 — a `## Trace` line in a file that has no headings

Verdict: confirmed
Decision: Give the transverse block an ordinary `tracabilite.md` line at move 5 — identifier, title, its entry or a dash, in product-file order — built from move 2b's record, and drop the *« `## Trace` line in `tracabilite.md` »* wording at L183 and L729.
Where: convertisseur.md L183-185, L729-731 ↔ convertisseur.md L795-797, L802-803
Cited: convertisseur.md L802-803 — "nothing else on the line, no prose, no header"; 6_convertit.md L282-283 — "compare the block identifiers of `desc-produit.md`'s headings with the first column of `tracabilite.md`".
Owner: convertisseur
Also in: —

`desc-produit.md` keeps every block after the split (5_reclasse.md L127 counts `^### B` across the six files against it), so a transverse block missing from the first column is reported by the command as an extra or missing line. ⚠️ Voided if `## To settle` 1 chooses route A.

### convertisseur.md F12 — the *settle* case « one section of yours rather than another » is empty

Verdict: confirmed
Decision: Replace the empty item in the *You settle* row with a choice a nature invocation actually faces — how a rule of its own nature is cut into entries and where in its one section — and rest the *misplaced* contrast at L494-496 on that instead.
Where: convertisseur.md L363 ↔ convertisseur.md L74, L494-496, L657
Owner: convertisseur
Also in: —

### convertisseur.md F13 — `technique-transversal.md` missing from invocation 2's Writes

Verdict: confirmed
Decision: Add the technical questions file to invocation 2's Writes, *« when you have any »*, as row 1 does.
Where: convertisseur.md L340 ↔ convertisseur.md L632
Owner: convertisseur
Also in: —

### convertisseur.md F14 — a named blocking file that no Reads column lists

Verdict: confirmed
Decision: Add *« the blocking file the prompt names »* to both Reads columns of Part 2.
Where: convertisseur.md L584-587 ↔ convertisseur.md L631-632, L637
Owner: convertisseur
Also in: —

### convertisseur.md F15 — the answered technical file is filed before the row that fires on it

Verdict: confirmed
Decision: Decide which natures run on the answered `technique-<nature>.md` before it is filed, and give the invocation-1 prompt a path that exists at invocation time.
Where: 6_convertit.md L78-80 ↔ 6_convertit.md L131, L171; convertisseur.md L385-386
Cited: 6_convertit.md L78-80 — "And every `convertisseur/questions-*.md` the last run wrote, into `convertisseur/closed/` … and every answered `technique-<nature>.md` with them"; L131 — "Its `convertisseur/technique-<nature>.md` holds an answered question | Runs … Name the file in its prompt"; convertisseur.md L385 — "The prompt names your answered technical file when there is one".
Owner: 6_convertit
Follows: convertisseur — L59 and L385-386 must accept the path the prompt names when it is the filed one, or the file must still sit at L59's path when the agent runs.
Also in: commandes (chemins-amont.md F13, fichiers.md F01 — the same finding without the agent's name)

⚠️ Whichever order is chosen, one more thing has to hold: a rerun with a new technical question writes `technique-<nature>.md` whole (L631), over the answered one if it is still there — so the answered file must be archived, and the *Runs* row must not fire twice on it.

### convertisseur.md F16 — `technique-transversal.md` is answered and never applied

Verdict: confirmed
Decision: Give the transversal technical file the same route as a nature's — an answered one forces the assembly and invocation 2, is named in the invocation-2 prompt, and is filed once consumed; and make the *No nature runs* row count it.
Where: convertisseur.md L340, L385-386 ↔ 6_convertit.md L131-132, L154, L261-263
Cited: 6_convertit.md L261-263 — the invocation-2 prompt carries only "Feature folder … Invocation 2 — Transversal. <Plus: convertisseur/blocked_transversal.md …>"; L154 — the *stands* row names "no nature is waiting on an answered technical file" and nothing of a transversal one.
Owner: 6_convertit
Follows: convertisseur — L385-386 already opens the file the prompt names; nothing else to change once the prompt names it.
Also in: —

### fichiers.md F02 — same finding as convertisseur.md F16

Verdict: confirmed
Decision: As convertisseur.md F16.
Where: convertisseur.md L340 ↔ 6_convertit.md L263
Owner: 6_convertit
Also in: —

### chemins-amont.md F14 — same finding as convertisseur.md F16

Verdict: confirmed
Decision: As convertisseur.md F16.
Where: 6_convertit.md L263 ↔ convertisseur.md L340
Owner: 6_convertit
Also in: —

### convertisseur.md F17 — a legitimate *No* at invocation 2 reads as a broken run

Verdict: confirmed
Decision: Have the command tell invocation 2's *No* from a fault — a missing `tracabilite.md` beside a `questions-transversal.md` that holds a question is the *No*, beside an empty one it is the fault — and never let the *document stands* row fire on a document invocation 2 left without preamble or traceability.
Where: convertisseur.md L453-457 ↔ 6_convertit.md L267-269, L154
Cited: 6_convertit.md L267-269 — "Then check `tracabilite.md` and `convertisseur/questions-transversal.md` exist. A missing one stops the command — say which."
Owner: 6_convertit
Follows: convertisseur — L453-457 says what a *No* leaves on disk; it has to match what the command tests.
Also in: commandes

### convertisseur.md F18 — the rerun trigger stated backwards

Verdict: confirmed
Decision: Name the answered technical file as what makes the command run the nature again, and the `<<ASSUMED` mark as what that rerun lifts.
Where: convertisseur.md L395-397 ↔ 6_convertit.md L130-132
Cited: 6_convertit.md L131 — "Its `convertisseur/technique-<nature>.md` holds an answered question | Runs — whatever its blocks did"; L130 — a marked section runs only "and its part changed".
Owner: convertisseur
Also in: —

### convertisseur.md F19 — `/5_reclasse`'s reader table names eight readers `transverses.md` never reaches

Verdict: confirmed
Decision: —  *(see `## To settle` 1 — the reader table follows whichever route is chosen)*
Where: 5_reclasse.md L102 ↔ convertisseur.md L146-147
Cited: 5_reclasse.md L102 — "`par-genre/transverses.md` | Every nature invocation of the Convertisseur"
Owner: —
Also in: commandes

### passages-amont.md F07 — same finding as convertisseur.md F19

Verdict: confirmed
Decision: —  *(see `## To settle` 1)*
Where: 5_reclasse.md L102 ↔ convertisseur.md L52, L146-147
Owner: —
Also in: commandes

### convertisseur.md F20 — the Architecte does not read `Consumes:` for the purpose the file gives it

Verdict: confirmed
Decision: Make the reader table at L28-34 say what each reader does with the line — the Architecte finds conjunction pairs between entries, the Cadreur reads it inside each entry to order what a lot needs — and attribute the direction of dependencies to the reader that uses it.
Where: convertisseur.md L34 ↔ architecte.md L513-514
Cited: architecte.md L513-514 — "and the graph that names the pairs, `Consumes:`, does not exist yet when that grid runs" — the only mention of the line in the file.
Owner: convertisseur
Also in: architecte —

### passages-amont.md F06 — the Cadreur never names `Consumes:`

Verdict: confirmed
Decision: Name `Consumes:` in the Cadreur's file as the line it reads in each entry to place a screen's lot behind the lot that computes what it shows.
Where: convertisseur.md L275-278, L295 ↔ cadreur.md L753
Cited: cadreur.md L753-754 — "`Needs`, `Produces` and `Modifies` carry symbols, and symbols only" — and no line of cadreur.md names `Consumes:` (grep).
Owner: cadreur
Follows: convertisseur — L275-278 and L34 must name the reader the Cadreur's file then declares (with F20).
Also in: cadreur

### convertisseur.md F21 — `cycle.md` relays to `/3`, `/4`, `/4_convertit`

Verdict: confirmed
Decision: Apply decisions.md `cadreur.md` F23 — `cycle.md` is deleted and its rows with it; no correction of the rows.
Where: cycle.md L88, L93 ↔ 6_convertit.md L2
Cited: cycle.md L88 — "`convertisseur` → `/3` or `/4` on `spec-technique.md`"; L93 — "`convertisseur` → `/4_convertit` if no `spec-technique.md`, else `/7_decoupe`".
Owner: commandes
Also in: commandes (renommages.md F14)

### convertisseur.md F22 — a `[B<n>: …]` left as a question reaches the Cadreur unseen

Verdict: confirmed
Decision: Make the Cadreur's stop grep `[B`, not `[B?:` alone — any bracket reference left in the document is one nobody resolved.
Where: convertisseur.md L754-757 ↔ cadreur.md L138, L397
Cited: cadreur.md L397 — "1. Grep `<<ASSUMED` and `[B?:` in the technical document. One hit of either and you stop"; 6_convertit.md L276 already greps `[B` for the same meaning.
Owner: cadreur
Follows: convertisseur — L754-757 may then say the leftover stops the split instead of *« reads as settled »*.
Also in: cadreur

### passages-amont.md F05 — same finding as convertisseur.md F22

Verdict: confirmed
Decision: As convertisseur.md F22.
Where: convertisseur.md L766 ↔ cadreur.md L392-397
Owner: cadreur
Also in: cadreur

---

## Part 2 — the status table's `open` and `other` rows

### convertisseur.md (part 2) c.1 — « open »

Verdict: wrong
Cited: convertisseur.md L440-447 — "You meet that question while you write the entry, not after — the moment you cannot turn a rule into something executable. … No — the rule does not exist without it | Stop there: no section, no notes, the question written." — and 6_convertit.md L189-190 tests the notes *« when it wrote its section »*, the one meaning c.1 asked for. c.1 is applied; the row is unfounded.

### convertisseur.md (part 2) B-5 — the same test stated twice

Verdict: confirmed
Decision: State the *« if nobody writes it, does the code lack something? »* test once.
Where: convertisseur.md L158 ↔ convertisseur.md L187-189
Owner: convertisseur
Also in: —

### convertisseur.md (part 2) c.20 / D-3 — « other »: the never-do still forbids opening the technical file

Verdict: confirmed
Decision: Exempt the technical file the prompt names from the *« any questions file »* never-do, and from *« an answer reaches you through the product file »*.
Where: convertisseur.md L608-609 ↔ convertisseur.md L385-386
Owner: convertisseur
Also in: —

### convertisseur.md (part 2) D-14 — « other »: « which of the two » beside three words

Verdict: confirmed
Decision: Say three cases wherever the report sentence names two — L473-474 and L527-528 — matching L449-451.
Where: convertisseur.md L473-474, L527-528 ↔ convertisseur.md L445-451
Owner: convertisseur
Also in: —

### convertisseur.md (part 2) D-16 — « other »: move 3 of invocation 1 still notes a cross-cutting rule from its blocks

Verdict: confirmed
Decision: Remove the cross-cutting item from the notes' `## Preamble` (example and rule), leaving the *existing* references — a behaviour block carries no rule over a category once the genre split has run.
Where: convertisseur.md L681, L693-694 ↔ convertisseur.md L146-153, L719; 5_reclasse.md L101-102
Owner: convertisseur
Also in: —

⚠️ Under route A of `## To settle` 1 the item is not removed but re-sourced: the nature notes it from `transverses.md`, not from *its blocks*.

### convertisseur.md (part 2) « 1 — transverses to every nature invocation » and « 1 — references » — « other »

Covered by F02 and F05 above.

---

## To settle

### 1. Who reads `par-genre/transverses.md`

🔴 **The demand (modifications.md L547) says every nature invocation; the file (convertisseur.md L146-147) says invocation 2 alone, and `/5_reclasse` L102 still says every nature.** The correction between rounds chose the file's route on two grounds (L149-153): a transverse block carries an empty `Nature:` line, so a nature invocation would have to derive one; and eight invocations would write the same constraint eight times.

⚠️ **The first ground does not hold as stated**: invocation 2 places the code half *« in the section of its layer »* (L178-179), which is the same derivation, made by an invocation that has no blocks in front of it. The second ground is real.

| Route | What it costs |
|---|---|
| **A — every nature invocation reads it** (the demand) | Each nature writes the transverse entries of its layer with its own numbering and its own `## Trace` line — F10 and F11 dissolve, D-16 becomes a re-sourcing. ⚠️ Each nature has to judge which transverse rules are its layer's: two natures can both claim one, or none; the constraint half needs one writer (invocation 2, from the file) or it is written up to eight times. Eight opus contexts each load the file. |
| **B — invocation 2 alone** (the file as written) | One reader, one writer of the constraint half. ⚠️ Invocation 2 numbers entries in sections it did not write (F07), derives their layer blind, and needs the record F10 and F11 add so that references to a transverse block resolve and `tracabilite.md` stays complete. The index row and `/5_reclasse` L102 must be corrected to say so (F02, F19). |

📌 **Whichever route is chosen**, F02, F19 and passages-amont F07 get their decision from it; F10, F11 and D-16 stand as written under B and are voided or re-shaped under A.

### 2. Where a leftover `[B<n>: …]` is caught — decided above, flagged here

F22 decides the Cadreur greps `[B`. 📌 **The alternative** — invocation 2 turning a leftover bracket into an `<<ASSUMED` mark — keeps the Cadreur's grep as it is but loses the reference's expectation text, which is what resolves it later (L292-294). Not a product matter; the decision is taken, and the cadreur plan may take the other side — flagged so the merge sees both.
