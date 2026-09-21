# Vérification 3 — plan

Source: `docs/verification3/consolide.md`, 63 entries. Every file a `Where` names was opened at the lines named, on both sides, before any decision below — except entry 44, whose two files sit in `docs/process/` and are not opened by this session (the Product Owner's documents). Line numbers are the ones read under `.claude-new/`; where they differ from the consolidated report, the ones read are given.

Two rules of this plan:

- A `Decision` says what changes and in which file, never the wording. The agent that applies it writes the prose.
- Entries whose fix turns on intent, scope or what the Product Owner sees carry `Decision: —` and sit in `## To settle` at the end, with what each option costs. Three entries (11, 26, 29) carry a decision on their mechanical part and a residual question in `## To settle`.

Entries sharing an owner were read together — see *Shared owners* before the summary table. Entries marked `Same as` in the consolidated report got one decision each (1, 2, 4, 9, 11, 26, 29, 32, 36, 38); entry 58 is the same defect as 26 and takes its decision.

Every entry below whose `Where` names two files appeared in one report only, unless its `Same as` says otherwise — both sides were opened here, which is said once and holds for all of them; entry 44 is the one whose second side stays unopened.

---

## BLOCKING

### 1 · fichiers F02 — Phase 1's genre filter has no source, and forgets `transverse`

Severity: BLOCKING
Decision: In `9_controle.md`, phase 1 takes each block's genre from a grep of `^Genre: comportement` in `desc-produit.md` (the heading one line above each hit, as `/3a_genre` L107 greps it), keeps those blocks plus every other block whose `tracabilite.md` line carries at least one entry, adds a `transverse` row to the set-aside table at L136-141 (constraint half taken up by the preamble's `## Cross-cutting rules`, code half kept through its entry's lot), and L195 says every *kept* block appears.
Where: 9_controle.md L39-42, L132-134, L187-197 ↔ convertisseur.md L172-173, L184-186, L194-200, L862-864 ↔ qualifieur.md L74-86
Cited: convertisseur.md L862-864 — "**Every block appears**, those no entry carries included — a transverse block that gave only a constraint, a block out of scope, a directive — a dash says someone looked and found none." · convertisseur.md L172 — "**The shared piece of code** — a formatter, a comparison, a rule the code has to hold somewhere | 🔴 **A numbered entry, in the section of its layer**" · qualifieur.md L83 — "| `transverse` | A rule whose **subject is a category, not an object of the product** |"
Owner: 9_controle.md
Follows: — (the Convertisseur and the Qualifieur change nothing; the filter stays, it gains a source)
Note: the grep of `desc-produit.md` is the same reading mode L39-42 already allows for the `Anchor:` lines — by grep, never the file whole. Read with entries 10, 32, 33 (same owner) — no collision.

### 2 · fichiers F01 — Every agent without Bash leaves its output uncommitted

Severity: BLOCKING
Decision: In `8_code.md`, *Git, once it has reported* (L614-625) opens on a `git add` and `git commit` inside the worktree, as `/conventions` L232-235 and this command's own split-back path L513-515 already do, and L622-625 stop reading uncommitted agent files as the agent's fault.
Where: 8_code.md L105-108, L614-625 ↔ relecteur.md L4, L46 (same section in 7_lots.md L269-273, 9_controle.md L389-394, diagnostique.md L172-177)
Cited: relecteur.md L4 — "tools: Read, Grep, Glob, Write" · relecteur.md L46 — "**You write** `code/<lot>/verdict.md`."
Owner: 8_code.md
Follows: 7_lots.md L269-273, 9_controle.md L389-394, diagnostique.md L172-177
Note: one rewrite of the section serves entries 2, 22 and 62 — five steps: commit inside the worktree, leave it, merge from the main checkout root, push, remove. Write it once and copy it.

### 3 · renommages F01 — An entry still waiting on the Product Owner reads as answered

Severity: BLOCKING
Decision: In `arbitre.md`, one shape for a waiting entry — its number is not written at all, as L195-196 and L493-499 say — and L181-183, L470 and L486 say the same thing instead of "an empty number" and "leave those numbers unanswered".
Where: arbitre.md L181-183, L194-198, L468-471, L486, L493-499 ↔ 8_code.md L233-240
Cited: 8_code.md L237-240 — "**Count the numbered answers against the `## Blocking N` headings** — 📌 **a grep of `^## Blocking ` and of the numbered lines under `## Decision`**: ⚠️ **a file is filled when every heading has its number**, never when the field merely holds text."
Owner: arbitre.md
Follows: — (8_code.md's count reads the single shape right once the Arbitre writes it; see entry 25 for what 8_code.md changes on its own account)
Note: read with entry 7 (same owner, same template) — the two agree: an answered entry carries its number, a waiting one carries none.

### 4 · chemins-amont F01 — The second time never re-runs once it asked, and `/5_reclasse` waits for it

Severity: BLOCKING
Decision: In `4_grille.md`, the second time's "has it already run" test (L296-298) distinguishes the highest `questions-existant-NN.md`: empty → over, write nothing; holding a `### Q` and filed under `questions/existant/` (its answers went through `/1_lexique` and `/2_structure`) → write the next `questions-existant-NN.md` empty, without an agent, as L305-307 already does when no block attaches. A highest one at the root is the `### Q` guard's (L210-215).
Where: 4_grille.md L293-298, L305-307, L546-548 ↔ 5_reclasse.md L50-62
Cited: 5_reclasse.md L50-52 — "**The highest-numbered `questions-sondeur-NN.md` and the highest-numbered `questions-existant-NN.md`, each present and holding no `### Q`**" · L61-62 — "**Either missing, or the highest holding a `### Q`** → 🔴 **stop**: say to run `/4_grille`."
Owner: 4_grille.md
Follows: — (`/5_reclasse`'s test stays the single closure evidence)
Note: "runs once" (L293) holds — no agent runs; the file is the evidence the rest of the chain keys on. Read with entries 16 and 49 (same owner, same section) — no collision.

### 5 + 6 · chemins-amont F02 / F03 — Both orders of "decision, then answer" dead-end in `/2_structure`

Severity: BLOCKING
Decision: In `2_structure.md`, the invocation table (L130-138) reads the questions file before the blocking files: the rows run — a questions file holding `### Q` (integrate it, L137) · more than one (stop, L138) · a `blocked_decoupeur|qualifieur|classeur.md` with every `## Decision` filled (L133) · one with any `## Decision` empty (L134) · an empty questions file (L136) · the two no-questions-file rows (L132, L135). A run with both an answered file and a blocking file at the root integrates the answered file and files it; the next run takes the blocking file. `3a_genre.md` L255 adopts `3b_nature.md` L265's order — answer first, decision once integrated — and L265 drops its "never at the root together" clause.
Where: 2_structure.md L130-138, L186-187, L249-255 ↔ 3a_genre.md L255 ↔ 3b_nature.md L265
Cited: 3a_genre.md L255 — "| It wrote a blocking file **and** a questions file with questions | 🔴 **Fill every decision first, then answer, then `/1_lexique`** — 📌 both end in the Rédacteur's hands |" · 3b_nature.md L265 — "🔴 **Answer the questions first, then `/1_lexique`** — 📌 **fill the decision second, once the answers are integrated.** ⚠️ **Both end in the Rédacteur's hands, but never at the root together**: `/2_structure` would take the blocking file and leave the answered file beside the Rédacteur's own, and the next command stops on two"
Owner: 2_structure.md
Follows: 3a_genre.md L255, 3b_nature.md L265
Note: one defect, two entries in the consolidated report, one decision. Row L136 ("one, with no `### Q` → invoke nothing") has to sit *below* the blocking-file rows, or a filled blocking file beside an empty questions file would loop on "nothing to integrate" — the order above places it there.

---

## TO FIX

### 7 · renommages F02 — A single-entry decision in the three-part shape is never counted filled

Severity: TO FIX
Decision: In `arbitre.md`, the decision template (L147-157) carries the entry's number — the three parts sit under `N.` for every entry, a single one included — so "one number per `## Blocking N`" is no longer stated only under *A file with several blockings* (L177-179).
Where: arbitre.md L137-140, L147-157, L177-179 ↔ 8_code.md L234, L237-240
Cited: 8_code.md L239-240 — "⚠️ **a file is filled when every heading has its number**, never when the field merely holds text."
Owner: arbitre.md
Follows: — (detailleur.md L326-330 and realisateur.md L299-301 already write `## Blocking 1` for a single stop; 8_code.md's count stays)

### 8 · renommages F03 — `## Where` cannot point at a request that has no name

Severity: TO FIX
Decision: In `cadreur.md`, each request block of `architecte/cadreur.md` (L227-231, L240-243) opens on an identifier of its own, and `code/blocked_cadreur.md`'s `## Where` (L196-198, L314) carries that identifier when the block is on a conventions request.
Where: cadreur.md L196-198, L227-231, L240-243, L314 ↔ 7_lots.md L167-168, L182-186
Cited: 7_lots.md L185-186 — "⚠️ **the block the blocking file's `## Where` names is the one that counts.**"
Owner: cadreur.md
Follows: 7_lots.md L167-168, L182-186 (read the identifier); architecte.md invocation 3 (writes its `## Verdict` under the block the identifier names — see entry 30)

### 9 · renommages F04 — A `forme` answer is written as a convention

Severity: TO FIX
Decision: In `architecte.md`, invocation 2 (L634-652) exempts a `forme` answer as it exempts `inconsistency` and `coverage`: no rule, a `couverture.md` line saying what became of it, and the report naming it as a grid amendment the Product Owner makes herself (L556-558).
Where: architecte.md L544-546, L556-560, L634-652 ↔ conventions.md L263-269
Cited: conventions.md L267 — "| It raised an **`inconsistency`** | 🔴 **The technical document is wrong** — 📌 **say which entry**: the fix is upstream, in `/6_convertit`, not here |" (the table has rows for `coverage` and `inconsistency`, none for `forme`)
Owner: architecte.md
Follows: conventions.md L263-269 — a row for a `forme` answer

### 10 · fichiers F03 — Step d's count can never match

Severity: TO FIX
Decision: In `9_controle.md`, step d (L187-189) counts the blocks phase 1 kept against the lines of `tracabilite-full.md`, not every block of `tracabilite.md`.
Where: 9_controle.md L132, L187-189 ↔ convertisseur.md L857-864
Cited: convertisseur.md L862 — "🔴 **Every block appears**, those no entry carries included"
Owner: 9_controle.md
Follows: —
Note: consequence of entry 1's filter; read with it — the kept set entry 1 defines is what step d counts.

### 11 · fichiers F04 — A `NEW` block after the split deletes the technical document nobody can rebuild

Severity: TO FIX
Decision: In `2_structure.md`, the deletion at L202-210 does not run when `code/decoupage.md` exists: nothing is deleted, and the command says the `NEW` block belongs to a new cycle — the sentence `/6_convertit` L37-38 already says.
Where: 2_structure.md L202-210 ↔ 6_convertit.md L35-38 (cadreur.md L61 reads the document)
Cited: 6_convertit.md L35-38 — "🔴 **`code/decoupage.md` exists → stop.** ⚠️ **The split is cut, and a lot cites entries by number** — 📌 **writing a section again would renumber it under the lot.** Say that a change to the product now belongs to a new cycle."
Owner: 2_structure.md
Follows: —
Note: the guard is the mechanical part. How a `NEW` block created after the split reaches the code is a question of intent → `## To settle`, item A.

### 12 · fichiers F05 — The audit never sees the Convertisseur's blocks

Severity: TO FIX
Decision: In `audit_blocages.md`, `convertisseur/` is the fifth place (L26-30, L32-33, L35-36), for `blocked_<nature>-NN.md` and `blocked_transversal-NN.md`.
Where: audit_blocages.md L26-36 ↔ 6_convertit.md L343-350
Cited: 6_convertit.md L346-347 — "git mv docs/features/<name>/convertisseur/blocked_<nature>.md \ docs/features/<name>/convertisseur/blocked_<nature>-NN.md"
Owner: audit_blocages.md
Follows: —

### 13 · chemins-amont F04 — An answer naming a genre alone is never applied

Severity: TO FIX
Decision: In `3a_genre.md`, the "neither returns anything → do not invoke" rule (L110-112) gains a third trigger: the highest `questions-qualifieur-NN.md` under `questions/qualifieur/` holds a `### Q` → invoke, with that file named (L154-155) and no block listed. The agent's next file, empty, is what makes the trigger fall silent.
Where: 3a_genre.md L88-97, L103-112, L154-155 ↔ qualifieur.md L173, L185-186, L220, L323-324
Cited: qualifieur.md L220 — "| **The answer still fits the block** | 📌 **Apply it** — ⚠️ **even when nothing in the block changed**: an answer naming a genre alone leaves the text as it was, and it is here that it lands |"
Owner: 3a_genre.md
Follows: — (qualifieur.md L323-324 already claims the blocks an answer names)

### 14 · chemins-amont F05 — Same hole for the classeur

Severity: TO FIX
Decision: In `3b_nature.md`, the same third trigger at L111-113: the highest `questions-classeur-NN.md` under `questions/classeur/` holds a `### Q` → invoke, with that file named.
Where: 3b_nature.md L87-96, L102-113 ↔ classeur.md L169-175
Cited: classeur.md L169-171 — "📌 **A block an answer names is yours to open**, whether or not the prompt lists it — ⚠️ **its line is filled and nothing marked it**, so neither grep finds it."
Owner: 3b_nature.md
Follows: —

### 15 · chemins-amont F06 — A product answer that changed no block re-asks the same question every run

Severity: TO FIX
Decision: —
Where: 6_convertit.md L143-144 ↔ convertisseur.md L487-489, L632-634
Cited: convertisseur.md L632-634 — "🔴 **Open `idees.md`**, or any questions file 📌 **but the answered technical file the prompt names** — a product answer reaches you through the product file, a technical one through that file alone"
Owner: — (see `## To settle`, item B)
Follows: —
Note: both sides verified; the fix turns on where a product answer lands — a principle the Convertisseur states at L633-634 — and two designs respect different halves of the text. `## To settle`, item B.

### 16 · chemins-amont F07 — A turn whose answers changed no block cannot close the grid

Severity: TO FIX
Decision: In `4_grille.md`, row L204 changes: neither marker returned, the highest `questions-sondeur-NN.md` holding a `### Q` and filed under `questions/sondeur/`, no `questions-existant-NN.md` anywhere → the first time is closed (the answers were integrated and changed no block): write the next `questions-sondeur-NN.md` empty without an agent, as L305-307 does, and go on to the second time. The stop stays for a highest file at the root — the guard's case (L210-215).
Where: 4_grille.md L176-183, L197-204 ↔ 2_structure.md L98-103, L249-250 ↔ redacteur.md L103
Cited: 2_structure.md L249-250 — "🔴 **At invocation 2, file the questions file it integrated**, into `questions/<agent>/`, inside the worktree before the merge" · redacteur.md L103 — "🔴 **`MODIFIED` on every block you change**"
Owner: 4_grille.md
Follows: —
Note: the empty file it writes is the evidence `/5_reclasse` L50-52 tests, so nothing changes there. Same pattern as entry 4.

### 17 · chemins-amont F08 — The `### Q` guard stops on the architecte's waiting file

Severity: TO FIX
Decision: In `3a_genre.md`, the `### Q` guard (L54-59) excludes `questions-architecte-*.md`, as `/conventions` L122-126 and `/1_lexique` L68-71 do; the filing exception at L71-73 stays.
Where: 3a_genre.md L54-59, L71-73 ↔ conventions.md L122-126 (same guard in 3b_nature.md L53-58, 3_decoupe.md L51-54, 4_grille.md L210-215, 5_reclasse.md L80-82, 6_convertit.md L62-65, fusion_compare.md L50-53)
Cited: conventions.md L122-126 — "🔴 **Grep `^### Q` in each root `questions-*.md` whose prefix is not `architecte` before touching it** … 📌 **The architecte's own file is the walk's above, not this guard's.**"
Owner: 3a_genre.md
Follows: 3b_nature.md L53-58, 3_decoupe.md L51-54, 4_grille.md L210-215, 5_reclasse.md L80-82, 6_convertit.md L62-65, fusion_compare.md L50-53

### 18 · chemins-amont F09 — Two commands file the architecte's answered file where nobody reads it

Severity: NOTE (overstated from TO FIX, as consolidated)
Decision: In `fusion.md`, the filing at L113-117 leaves `questions-architecte-*.md` at the root, as every other command does; `fusion_applique.md` L175-179 the same.
Where: fusion.md L47, L113-117 ↔ conventions.md L85, L109-112 (fusion_applique.md L175-179)
Cited: conventions.md L85 — "| A `questions-architecte-NN.md` at the root, **answered** | **Invocation 2 — Integrating** — 🔴 **name the file in the prompt** |"
Owner: fusion.md
Follows: fusion_applique.md L175-179
Note: `/3_decoupe`, `/5_reclasse` and `/fusion_compare` exhibit entry 17, not this — verified: their guard (3_decoupe L51-54, 5_reclasse L80-82, fusion_compare L50-53) stops before their filing line.

### 19 · chemins-amont F10 — `/2_structure` stops on a settled vocabulary after "4 wrote none"

Severity: TO FIX
Decision: In `2_structure.md`, the guard at L86-90 bears on a `questions-lexicographe-NN.md` at the root alone (the one L92-96 files), and *What you read* L27-29 separates the two reads — the root file for the guard, the highest anywhere for invocation 1's settled-vocabulary test at L140-143, which stays as it is.
Where: 2_structure.md L27-29, L86-90, L140-143 ↔ 1_lexique.md L205-210, L217-221, L263
Cited: 1_lexique.md L205-206 — "🔴 **After 2 or 4, file the lexicographe's questions file it applied**, into `questions/lexicographe/`" · L263 — "| 4 wrote none | 📌 `/2_structure` — 🔴 the answers are settled |"
Owner: 2_structure.md
Follows: — (a filed lexicographe file is by construction applied — `/1_lexique` L205 — so the root-only guard loses nothing)

### 20 · chemins-amont F12 — The second decoupeur runs outside any worktree

Severity: TO FIX
Decision: In `3_decoupe.md`, the short-list re-invocation (L204-207) moves under *Once it has reported* (L157-171), inside the worktree, before *Git, once it has reported* merges and removes it (L179-181); *What you relay* keeps the report of a list still short after the second run.
Where: 3_decoupe.md L204-207 ↔ 3_decoupe.md L175-181, L129-132
Cited: 3_decoupe.md L179-181 — "1. `git merge --no-ff <branch>` from the main checkout root 2. `git push` 3. `git worktree remove <path>`"
Owner: 3_decoupe.md
Follows: —

### 21 · chemins-amont F13 — An empty architecte file sticks at the root and answers "/7_lots" for ever

Severity: TO FIX
Decision: In `conventions.md`, *Git, before invoking* L137-140 files away an empty `questions-architecte-NN.md` as it files an integrated one, so row L86 matches on the run right after the derivation and never again.
Where: conventions.md L75-76, L86-90, L137-140 ↔ architecte.md L334, L337
Cited: architecte.md L334 (invocation 1's output column) — "`TECHNICAL_CONVENTIONS.md` · `couverture.md` · a questions file" · L337 (invocation 4) — "The conventions file, **added to** · `couverture.md`, **for this feature** · a questions file"
Owner: conventions.md
Follows: —
Note: the side the consolidated report said no report named — the Architecte writing a questions file at 1 and 4 whatever it asked — is opened here: L334 and L337 list it unconditionally.

### 22 · chemins-amont F14 — No upstream command commits inside the worktree before merging

Severity: TO FIX
Decision: In `1_lexique.md`, *Git, once it has reported* (L230-236) opens on the commit step `/conventions` L232-235 has, with the same reason.
Where: 1_lexique.md L205-206, L230-236 ↔ conventions.md L232-235 (same section in 2_structure.md L273-279, 3_decoupe.md L175-181, 3a_genre.md L223-229, 3b_nature.md L228-234, 4_grille.md L511-517, 6_convertit.md L378-384, fusion.md L220-226, fusion_compare.md L140-146, fusion_applique.md L142-148)
Cited: conventions.md L232-235 — "1. 🔴 **`git add` and `git commit` inside the worktree** — ⚠️ **the agent has no Bash and commits nothing**; 📌 **`git merge` takes the branch's commits, not the worktree's files**, and `git worktree remove` refuses a dirty tree"
Owner: 1_lexique.md
Follows: 2_structure.md, 3_decoupe.md, 3a_genre.md, 3b_nature.md, 4_grille.md, 6_convertit.md, fusion.md, fusion_compare.md, fusion_applique.md
Note: same rewrite as entries 2 and 62 — one text, copied.

### 23 · chemins-aval F03 — An empty attempt is never detected

Severity: TO FIX
Decision: In `8_code.md`, the empty-attempt test of move 3 (L157-158, L164-167) compares `HEAD` before and after the Réalisateur's invocation — no new commit is the empty attempt — instead of testing the lot's whole `git log` list, which the Concepteur's and Testeur's commits always fill.
Where: 8_code.md L105-108, L147-158, L164-167 ↔ concepteur.md L286, testeur.md L303, realisateur.md L695
Cited: concepteur.md L286 — "🔴 **The message reads `<lot>: <what the commit carries>`**" · testeur.md L303 — "🔴 **The message reads `<lot>: <what the commit" · realisateur.md L695 — "message reads `<lot>: <what the commit carries>`**"
Owner: 8_code.md
Follows: —
Note: the side the consolidated report said no report named — the three agents' commit-message rule — is opened here: all three use the `<lot>: ` prefix.

### 24 · chemins-aval F04 — 4b stops on `blocked_relecteur.md`'s empty decision before the act that retires it

Severity: TO FIX
Decision: In `8_code.md`, 4b's table (L227-235) excludes `code/<lot>/blocked_relecteur.md`, which the table under *Where you stop and hand back* (L572-581) handles — its `## Decision` is empty by shape.
Where: 8_code.md L227-233 ↔ 8_code.md L267-270, L572-581 ↔ relecteur.md L277-289
Cited: relecteur.md L277 — "**Its shape** — four headings, the last one left empty:" · 8_code.md L267-270 — "🔴 **`code/<lot>/blocked_relecteur.md` is retired by the act** … ⚠️ **no decision is filled**"
Owner: 8_code.md
Follows: —
Note: the relecteur side the consolidated report said no report named (L277-289) is opened here.

### 25 · chemins-aval F05 — The "every heading has its number" test is applied to files that carry no `## Blocking N`

Severity: TO FIX
Decision: In `8_code.md`, 4b (L233-235) and L237-240 give two tests by shape: a file with `## Blocking N` headings is filled when every heading has its number; a file with none — the Concepteur's, Testeur's, Relecteur's and Architecte's four `##` headings — is filled when `## Decision` holds anything.
Where: 8_code.md L49-55, L233-235, L237-240 ↔ concepteur.md L143-149, testeur.md L182-188, relecteur.md L277-285, architecte.md L248-254, arbitre.md L142-144
Cited: arbitre.md L142-144 — "📌 **The Concepteur, the Testeur and the Relecteur write four `##` headings and no `## Blocking N`** — that shape stays theirs" · architecte.md L254 — "| `## Decision` | 🔴 **Left empty** — the Product Owner fills it |"
Owner: 8_code.md
Follows: —
Note: read with entries 3 and 7 — the numbered shape is the Arbitre's two files; this entry adds the other shape's test, nothing else.

### 26 · chemins-aval F06 — The revert list is the whole history

Severity: TO FIX
Decision: In `8_code.md`, the `git log` list of move 3 (L151), wherever it drives a revert (move 4 step 1 L186-189, *When the split comes back* L486-492) or the Relecteur's diff (L141-145), is cut to the lot's commits after its most recent `Revert "<lot>: …"` commit.
Where: 8_code.md L142-155, L186-189, L486-492 ↔ 8_code.md L595-598
Cited: 8_code.md L595-598 — "📌 **A filled `## Decision` is not a stop** — invoke the agent it names on the lot it names, and let it apply the decision. ⚠️ **Even on a lot already carrying a PASS**"
Owner: 8_code.md
Follows: —
Note: F06's sentence is decided. F16's sentence — a `sheet` cause on a lot that is not the last coded, reverting commits later lots built on — has no rule and is a scope question → `## To settle`, item C. Entry 58 is the same defect and takes this decision.

### 27 · chemins-aval F07 — A signature rewritten after a `sheet` cause reaches no later sheet

Severity: TO FIX
Decision: In `detailleur.md`, on a `Findings:` prompt (L515-519), after writing the sheet again the Détailleur greps the block's later sheets for every symbol whose signature changed and rewrites those sheets as its divergence mode does; `8_code.md` L294-305 says the Findings rewrite carries that propagation, so move 5 is not needed for it.
Where: detailleur.md L507-519 ↔ relecteur.md L207-211 ↔ 8_code.md L186-197, L272-289, L294-305, L505-508
Cited: relecteur.md L209-211 — "🔴 **`## Symbol divergences` is for propagation, never for a failure** — 📌 **a signature changed by a decision the Concepteur or the Réalisateur applied, that later lots have to follow.**"
Owner: detailleur.md
Follows: 8_code.md L294-305
Note: the block's sheets are all written at block start (detailleur L523-524, one walk), so the later sheets do exist when a `sheet` cause hits an earlier lot. Read with entry 60 (same lines) — compatible.

### 28 · chemins-aval F09 — The Arbitre's twenty-minute poll (settled: not a defect)

Severity: TO FIX (as consolidated) — the poll itself is settled, not a defect
Decision: In `8_code.md`, L313-315 says two things apart: `stop.md` is looked for in the main checkout because the Product Owner creates it there after the worktree was cut; a blocking file she fills during a live run is filled in the worktree, where the Arbitre's poll reads it. `arbitre.md` L466-499 stays exactly as it is.
Where: 8_code.md L313-315 ↔ arbitre.md L466-499 (8_code.md L564-567)
Cited: arbitre.md L486 — "🔴 **Her answer appears under a number: apply it and carry on with your turn.**"
Owner: 8_code.md
Follows: —

### 29 · chemins-aval F10 — The redécoupage count is bypassed on a re-run, and the third stop is incomplete

Severity: TO FIX
Decision: In `8_code.md`, L548-549 routes a "block waits on the split" report through *When the split comes back* (L466-525) — the count at L473-480 included — instead of straight to `/7_lots`; and the third-return stop at L475-477 still closes the worktree by the four steps of L510-518 (commit, merge, push, remove), so `code/redecoupage.md` and the blocking file reach `HEAD` tracked.
Where: 8_code.md L548-549 ↔ 8_code.md L473-480, L510-518 ↔ detailleur.md L484-485
Cited: detailleur.md L484 — "| A `## Decision` sending the lot back to the split, **and `code/redecoupage.md` is still there** | 🔴 **Stop.** The split has not been redone — say the block is waiting on it |"
Owner: 8_code.md
Follows: —
Note: the Détailleur's wording L548 keys on — the side the consolidated report said no report named — is opened here (detailleur L484-485). What runs after the Product Owner's decision on a third return is nowhere written and is hers → `## To settle`, item D.

### 30 · passages F02 — The second request of a settled file is never answered

Severity: TO FIX
Decision: In `architecte.md`, invocation 3 (L686-690) opens every file of `architecte/` and settles each request block whose `## Verdict` is empty, skipping blocks — not files — whose verdict is filled.
Where: cadreur.md L240-243 ↔ architecte.md L686-690 (7_lots.md L182-186, L194-199 and 8_code.md L329-332 read per request)
Cited: cadreur.md L240-243 — "🔴 **Two needs in one run go in one file**, one block of headings each. 📌 **A file already there whose `## Verdict` is filled is answered** — ⚠️ **you never reopen it**: write the new need under a fresh heading block, below."
Owner: architecte.md
Follows: — (the stacked shape stays; entry 8 gives each block an identifier the verdict sits under)

### 31 · passages F03 — The Architecte questions every dash line the Convertisseur writes on purpose

Severity: TO FIX
Decision: In `architecte.md`, L417 raises `inconsistency` on a dash line only for a block whose `Genre:` is `comportement` or `référence` (read in `desc-produit.md`, which invocations 1 and 4 open whole — L334, L337); a dash on a `directive`, `hors périmètre`, `recette` or `transverse` block is the Convertisseur's design and raises nothing.
Where: convertisseur.md L862-864 ↔ architecte.md L413-422
Cited: convertisseur.md L862-864 — "🔴 **Every block appears**, those no entry carries included — a transverse block that gave only a constraint, a block out of scope, a directive — a dash says someone looked and found none."
Owner: architecte.md
Follows: —

### 32 · passages F05 — `decisions-produit.md` never gets a block identifier

Severity: TO FIX
Decision: In `9_controle.md`, phase 6 (L366-374) derives the block from the lot the blocking file names — the `## Blocking N — lot-NN` heading of the Détailleur's, the `code/<lot>/` folder of the others — through `tracabilite-full.md` of phase 1: one block on that lot → its identifier; several or none → the dash.
Where: 9_controle.md L366-374 ↔ detailleur.md L326-348 ↔ realisateur.md L299-311
Cited: detailleur.md L326-329 — "🔴 **one `## Blocking N — lot-NN` per stop**, even when there is only one, 📌 **the lot named in the heading, always**" · realisateur.md L303-307 — "## Blocking 1 / ### What blocks / ### Where / ### To resume"
Owner: 9_controle.md
Follows: — (no blocking-file shape changes; redacteur.md L740-741 reads the line as written, which it still can)

### 33 · passages F07 — Every entry with no lot reads as already built

Severity: TO FIX
Decision: In `9_controle.md`, phase 1 b (L149-154) marks `carried` only an entry whose `## Entries with no lot` line gives the "already carried by the code" reason, maps an entry "carried by §a and §b" to the lots of §a and §b, and gives an attribution or boundary entry no lot and no mark; `cadreur.md` L494 and L767-770 fix one greppable form per reason.
Where: cadreur.md L494, L762-774 ↔ 9_controle.md L149-154, L245-248
Cited: cadreur.md L767 — "§8.1 — carried by §4.1 and §5.2, nothing of its own to build" · L769-770 — "📌 **An entry attributing a rule to another, or setting a boundary, builds nothing.**"
Owner: 9_controle.md
Follows: cadreur.md L494, L767-770

---

## QUESTION

### 34 · fichiers F08 — Row 8 runs invocation 3 before invocation 1, and `INIT` never fires

Severity: QUESTION
Decision: —
Where: fusion.md L50, L65-69 ↔ fusionneur.md L355-357, L524-604
Cited: fusionneur.md L355-357 — "🔴 **A global holding nothing but `# Application` is a first feature.** There is nothing to compare: **the plan is one line, `INIT`**, and no question comes out of it." · L585 — "**3. Merge what you kept**, by the same three levels as invocation 1"
Owner: — (see `## To settle`, item E)
Follows: —
Note: both sides opened here; the finding holds — invocation 3 writes into the global (L585-593), so a first feature with a bug-fix cycle reaches invocation 1 with a global that is no longer `# Application` alone. The fix is a design choice → `## To settle`, item E.

### 35 · chemins-amont F25 — A `bugfix-NN` coded after the merge never carries its decisions into the global

Severity: QUESTION
Decision: —
Where: fusion.md L46 ↔ fusion.md L18-20
Cited: fusion.md L18-20 — "🔴 **One run per feature, once every bug-fix cycle has been coded.** The global is not revised while a downstream cycle is running on the same scope."
Owner: — (see `## To settle`, item F)
Follows: —
Note: L18 states the intent the finding questions; whether a correction cycle after the merge is supported is the Product Owner's → `## To settle`, item F.

### 36 · passages F08 — Row 3 cannot route an upstream blocking file, and re-invokes the Rédacteur with the blocking file alone

Severity: QUESTION
Decision: In `fusion.md`, rows 2-3 (L44-45) bear on the two files this command can route — `blocked_redacteur.md` whose `## Invocation` says 3, and `blocked_fusionneur.md`; any other blocking file stops the walk, the command it belongs to named (the symmetric test `/2_structure` L119 makes). Row 3's Rédacteur prompt names the decisions files as row 6's does (L101-104). `redacteur.md` invocation 3 carries on folding after writing `blocked_redacteur.md`, filing every decision it could not place, and on the re-invocation folds those alone.
Where: fusion.md L44-45, L101, L201 ↔ redacteur.md L750-753
Cited: redacteur.md L750-751 — "🔴 **A decision you cannot place, or cannot read, goes into `blocked_redacteur.md`**, its `## Invocation` line saying 3."
Owner: fusion.md
Follows: redacteur.md L750-753
Note: both sides opened; the routing part is mechanical, the "carries on" part follows the Détailleur's pattern (arbitre.md L175 — "files everything one walk found, at once").

### 37 · chemins-aval F19 — Neither side says how `B<n>` is written inside a gap of `bug-list.md`

Severity: QUESTION
Decision: —
Where: 9_controle.md L427-431 ↔ diagnostiqueur.md L616-620
Cited: diagnostiqueur.md L616-618 — "🔴 **A gap `bug-list.md` marks with a `B<n>` — the block a control report found unbuilt — hands it to every entry it gives**: 📌 **the identifier closes the entry's title, in parentheses**"
Owner: — (see `## To settle`, item G)
Follows: —
Note: `bug-list.md` is the Product Owner's hand-written file; the shape she writes `B<n>` in is hers to fix → `## To settle`, item G. Once she has, both files state it: `9_controle.md` L427-431 (writer's side) and `diagnostiqueur.md` L616 (reader's grep).

---

## NOTE

### 38 · renommages F05 — Readers are sent to a `Vocabulary` heading the preamble does not carry

Severity: NOTE
Decision: In `verificateur.md`, L62 and L415 name the preamble part by its heading, `## Intent and vocabulary`; `detailleur.md` L68 and L607 the same.
Where: verificateur.md L62, L415 ↔ convertisseur.md L133-141 ↔ detailleur.md L68, L607
Cited: convertisseur.md L136-141 — "# Preamble / ## Intent and vocabulary / ## Out of scope / ## Cross-cutting rules / ## Dependencies"
Owner: verificateur.md
Follows: detailleur.md L68, L607

### 39 · renommages F06 — `desc-bug.md` opens on `## Preamble`, `spec-technique.md` on `# Preamble`

Severity: NOTE
Decision: In `diagnostiqueur.md`, L563 writes `# Preamble`, one `#`, as the technical document does.
Where: diagnostiqueur.md L563 ↔ convertisseur.md L144-146
Cited: convertisseur.md L144-146 — "🔴 **`# Preamble` is one `#`, the sections are `## §n`** — the Cadreur tells them apart at a glance, and never cuts the preamble."
Owner: diagnostiqueur.md
Follows: — (no command or agent greps `Preamble` on `desc-bug.md` — verified by grep across `.claude-new/`)

### 40 · renommages F07 — A requirement filed under `## Trigger` never reaches `desc-bug.md`

Severity: NOTE
Decision: In `diagnostiqueur.md`, move 7 (L514-519) carries a second requirement filed under `## Trigger` as it carries one under `## Expected`.
Where: diagnostiqueur.md L411-415 ↔ diagnostiqueur.md L514-519
Cited: diagnostiqueur.md L514-515 — "**7. Write one entry per `## Bearer` block of the report**, from its `## Today` and `## Expected`."
Owner: diagnostiqueur.md
Follows: —

### 41 · renommages F08 — `## Placements not settled by the conventions` is written every time and read by nobody

Severity: NOTE
Decision: In `concepteur.md`, drop the field `## Placements not settled by the conventions` (L231-232, L314-317, L338-340) — the `architecte/` request already carries the placement under `## Where I met it` (L229).
Where: concepteur.md L231-233, L314-317, L338-340 ↔ 8_code.md L57-58
Cited: 8_code.md L57-58 — "**`code/<lot>/conception.md`** — 🔴 **its `## Decision applied` field alone**: it is where the Concepteur says it applied a decision."
Owner: concepteur.md
Follows: — (relecteur reads `## Declared` and `## Outside the lot` — L453-459 — not this field; verified by grep across `.claude-new/`)

### 42 · renommages F09 — The Testeur's own test file lands under `## Outside the lot`

Severity: NOTE
Decision: In `testeur.md`, a test file the Testeur creates for the lot (L86-87) is declared in `tests.md` under a field of its own and excluded from `## Outside the lot` (L332-335); `relecteur.md` L453-459 counts that field as declared, beside `## Files` and `## Declared`.
Where: testeur.md L86-87, L332-335 ↔ concepteur.md L114-118 ↔ relecteur.md L453-459
Cited: concepteur.md L114-116 — "🔴 **Touch a file that neither the sheet's `## Files` nor your `## Declared` names** — 📌 **a file you create to hold a declaration is `## Declared`'s**" · relecteur.md L453-456 — "🔴 **`## Outside the lot` names every file the lot touched that neither its sheet's `## Files` nor `conception.md`'s `## Declared` names, or a dash** — 📌 **`## Files` carries the existing files the lot opens, `## Declared` the files the Concepteur created**"
Owner: testeur.md
Follows: relecteur.md L453-459

### 43 · renommages F10 — `## Conventions requests` is a list nobody consumes

Severity: NOTE
Decision: In `cadreur.md`, drop the `## Conventions requests` section of `code/decoupage.md` (L245-248, L811, L848-851) — `/7_lots` L194 and `/8_code` L329 find requests by globbing `architecte/`.
Where: cadreur.md L245-248, L811, L848-851 ↔ 7_lots.md L194-195
Cited: 7_lots.md L194-195 — "📌 **Once the split holds**, glob `architecte/`. **Any request with an empty `## Verdict`** → `architecte`, invocation 3."
Owner: cadreur.md
Follows: —
Note: read with entry 8 (same owner) — no collision: entry 8 changes the request blocks in `architecte/cadreur.md`, this one removes a section of `code/decoupage.md`.

### 44 · renommages F11 — Both process documents still name `/cycle`

Severity: NOTE
Decision: —
Where: PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010
Cited: — (not opened)
Owner: —
Follows: —
Note: could not verify — `docs/process/` is the Product Owner's, and this session does not open it (CLAUDE.md, *What you never do*). Neither side was opened by this plan nor, per the consolidated report, by the consolidation. The two lines are hers to change if she wishes; no agent touches them.

### 45 · fichiers F06 — The Arbitre names `/8_code` as the reader of `code/redecoupage.md`'s headings

Severity: NOTE
Decision: In `arbitre.md`, L210-211 names `/7_lots` as the command that relays those headings.
Where: arbitre.md L210-211 ↔ 8_code.md L482-484 ↔ 7_lots.md L297-300
Cited: 8_code.md L482-484 — "📌 **What came back and what was done with it is `/7_lots`'s to relay** — 🔴 **it reads `code/redecoupage.md` before renaming it**; you relay nothing of it."
Owner: arbitre.md
Follows: —

### 46 · fichiers F07 — `/8_code` never looks for `code/blocked_verificateur.md`

Severity: NOTE
Decision: In `8_code.md`, *Where to resume* (L69-81) stops when `code/blocked_verificateur.md` exists, as it stops on a non-empty `## Defects` — run `/7_lots` first.
Where: 8_code.md L69-81 ↔ verificateur.md L176-177 ↔ 7_lots.md L89-94, L172
Cited: verificateur.md L176-177 — "🔴 **Write `code/blocked_verificateur.md`** — do not merely say it." · 7_lots.md L172 — "| `code/blocked_verificateur.md` | 🔴 **Stop.** 📌 **Relay which file was missing** … the step before it has to run again |"
Owner: 8_code.md
Follows: —

### 47 · fichiers F09 — `par-genre/comportements.md` is said to be read by the Convertisseur

Severity: NOTE
Decision: In `5_reclasse.md`, L109 names this command's second move as the file's only reader.
Where: 5_reclasse.md L109 ↔ convertisseur.md L53
Cited: convertisseur.md L53 — "| your blocks | `convertisseur/<nature>-input.md` — the behaviour blocks of your nature, copied there by the command |"
Owner: 5_reclasse.md
Follows: —
Note: entry 1 does not use this file as its genre source (it greps `desc-produit.md`), so nothing else names it.

### 48 · chemins-amont F15 — The blocking-file rename sits under *Git, before invoking*

Severity: NOTE
Decision: In `conventions.md`, the rename at L165-172 moves under *Git, once it has reported* (L228-239), after the commit step.
Where: conventions.md L165-172 ↔ conventions.md L228-239
Cited: conventions.md L165-166 — "🔴 **The agent reports having applied a decision → rename its blocking file:**"
Owner: conventions.md
Follows: —
Note: read with entry 21 (same owner) — different paragraphs, no collision.

### 49 · chemins-amont F16 — "Invoke nothing, without a worktree" is decided after the worktree was created

Severity: NOTE
Decision: In `4_grille.md`, the second time's `Global:` grep (L300-307) runs before the worktree is created (L266-268); a run that attaches to nothing creates none.
Where: 4_grille.md L305-307 ↔ 4_grille.md L266-268
Cited: 4_grille.md L305-307 — "📌 **Nothing returned** → 🔴 **invoke nothing.** ⚠️ **The feature touches nothing that exists** — write `questions-existant-NN.md` empty, commit and push without a worktree, and relay."
Owner: 4_grille.md
Follows: —
Note: read with entries 4 and 16 — the empty files they write are written the same way, without a worktree; no collision.

### 50 · chemins-amont F17 — A re-converted `MODIFIED` block leaves `couverture.md` standing

Severity: NOTE
Decision: In `2_structure.md`, the `couverture.md` deletion at L210 fires on a `MODIFIED` block too (grep `^### .*MODIFIED`), the three other deletions staying on `NEW` alone — a re-converted section is a rebuilt document, and L218-221's reason holds for it.
Where: 2_structure.md L202-221 ↔ conventions.md L88-89
Cited: conventions.md L89 — "| **It exists, and a `couverture.md` is there** | 📌 **Nothing to do** — say `/7_lots` |"
Owner: 2_structure.md
Follows: —
Note: read with entry 11 (same paragraph) — entry 11's `code/decoupage.md` guard covers this deletion too; one edit of the paragraph.

### 51 · chemins-amont F18 — The blocking table names "one" file while several can stand

Severity: NOTE
Decision: In `6_convertit.md`, the table at L49-53 reads per file: any unnumbered `convertisseur/blocked_*.md` with an empty `## Decision` stops the command, all of them named; each filled one is named in its own nature's prompt.
Where: 6_convertit.md L49-53 ↔ 6_convertit.md L191-194
Cited: 6_convertit.md L191-192 — "🔴 **First, grep for a new unnumbered `convertisseur/blocked_*.md`.** 📌 **One is enough**"
Owner: 6_convertit.md
Follows: —

### 52 · chemins-amont F19 — A waiting nature forces the assembly every run, and two relay rows match

Severity: NOTE
Decision: In `6_convertit.md`, the relay table at L410-419 gets a first-match rule, the waiting row (L417) placed above the last row (L419); the assembly forced by a waiting nature stays — it is the "Assemble nothing" branch of L218, which costs no invocation.
Where: 6_convertit.md L410-419 ↔ 6_convertit.md L167-168
Cited: 6_convertit.md L168 — "| Otherwise | 📌 **Skip to the assembly** — the document has to be built again around what stands."
Owner: 6_convertit.md
Follows: —

### 53 · chemins-amont F20 — `/1_lexique` and `/2_structure` bounce on the same state

Severity: NOTE
Decision: In `1_lexique.md`, L99-101 names `/3_decoupe` — the step `/2_structure` L135 names for the same state (`desc-produit.md` there, nothing at the root).
Where: 1_lexique.md L93-101 ↔ 2_structure.md L135
Cited: 2_structure.md L135 — "| No questions file, **and a `desc-produit.md`** | 🔴 **Stop** — 📌 **the idea file is transcribed once**; say `/3_decoupe` comes next | — |"
Owner: 1_lexique.md
Follows: —

### 54 · chemins-amont F21 — A `/1_lexique` run by mistake after "4 wrote none" re-watches a corrected file

Severity: NOTE
Decision: —
Where: 1_lexique.md L60 ↔ 1_lexique.md L263
Cited: 1_lexique.md L60 — "| Another agent's questions file alone | **3 — Watching** |"
Owner: — (see `## To settle`, item H)
Follows: —

### 55 · chemins-amont F22 — "Once, not until it clears" has no record across runs

Severity: NOTE
Decision: —
Where: 3a_genre.md L258 ↔ 3b_nature.md L268
Cited: 3b_nature.md L268 — "📌 **Say which, and run `/3b_nature` once more** — ⚠️ **once, not until it clears**: 🔴 **a second run that leaves one empty stops there, the blocks named**"
Owner: — (see `## To settle`, item I)
Follows: —

### 56 · chemins-amont F23 — The two-genre route can repeat on the same block

Severity: NOTE
Decision: —
Where: 3a_genre.md L256 ↔ qualifieur.md L95-102
Cited: qualifieur.md L100-102 — "🔴 **The route back is not yours**: `/2_structure` names the file to the Rédacteur, which rewrites the block with `MODIFIED`, and `/3_decoupe` splits it."
Owner: — (see `## To settle`, item J)
Follows: —

### 57 · chemins-amont F26 — `.claude/commands/cycle.md` is still tracked and named

Severity: NOTE
Decision: — (verdict `moot`, settled: out of scope — `.claude/` is the chain before the refonte, which this campaign does not touch; change nothing)
Where: .claude/commands/cycle.md L1 ↔ .claude/CLAUDE.md L51
Cited: —
Owner: —
Follows: —

### 58 · chemins-aval F11 — A re-cut lot's Relecteur diff carries every lot coded since

Severity: NOTE
Decision: Covered by entry 26 — the list cut to the commits after the lot's last revert gives the Relecteur's diff its first commit.
Where: 8_code.md L98 (read L141-155) ↔ 8_code.md L502-503
Cited: 8_code.md L502-503 — "🔴 **The lot keeps its number** — nothing is renumbered."
Owner: 8_code.md (through entry 26)
Follows: —

### 59 · chemins-aval F13 — `carried` is marked per entry, carried per block

Severity: NOTE
Decision: In `controleur.md`, L215-220 reads a line that carries both lots and the mark as: the lots' sheets are read, and an intention no sheet carries is found with the mark as its reason; a line with the mark and no lot stays one found line. `9_controle.md` L171-173 says that is what a mixed line means.
Where: 9_controle.md L151-152, L171-179 ↔ controleur.md L111-115, L215-220
Cited: controleur.md L217-220 — "⚠️ **A block that reaches you marked `carried` was built by a correction cycle** — its intentions are not missing, they were built elsewhere. 🔴 **One line under `## Intentions found`, with the mark as its reason** — never a `Missing` one, and you read no sheet for it."
Owner: controleur.md
Follows: 9_controle.md L171-173
Note: the controleur side was opened here; the consolidated report had not. Read with entry 33 (both about the mark) — compatible: 33 says which entries get it, 59 how a mixed line is read.

### 60 · chemins-aval F14 — The `Findings:` prompt names no lot

Severity: NOTE
Decision: In `8_code.md`, the Findings prompt (L297-305) names the lot; `detailleur.md` L515-519 takes the lot from the prompt rather than as the one with no sheet.
Where: 8_code.md L297-305 ↔ detailleur.md L515-519
Cited: detailleur.md L515-517 — "📌 **A prompt carrying a verdict's `## Findings`** names a lot whose sheet the review found false — ⚠️ **the orchestration has deleted that sheet**, so the lot falls under *No sheet*"
Owner: 8_code.md
Follows: detailleur.md L515-519
Note: read with entry 27 (same lines of detailleur.md) — compatible.

### 61 · chemins-aval F17 — The scope test reads files in `Modifies`, which carries symbols

Severity: NOTE
Decision: In `audit_conventions.md`, L106-107's scope test reads files from `Touches` and symbols from `Modifies`.
Where: audit_conventions.md L106-107 ↔ cadreur.md L822-826
Cited: cadreur.md L822-823 — "🔴 **`Needs`, `Produces` and `Modifies` carry symbols, and symbols only.** 📌 **A name the code carries** — ⚠️ **never a file.**"
Owner: audit_conventions.md
Follows: —

### 62 · chemins-aval F18 — The merge "from the main checkout root" is issued from inside the worktree

Severity: NOTE
Decision: In `8_code.md`, *Git, once it has reported* (L614-620) names, between the commit step entry 2 adds and the merge, the exit from the worktree — the session leaves the isolated worktree before `git merge` is issued from the main checkout root.
Where: 8_code.md L618 ↔ 8_code.md L102-103
Cited: 8_code.md L102-103 — "📌 **One worktree for the whole run**, not one per lot. Enter it before invoking anything."
Owner: 8_code.md
Follows: every command carrying the section — 1_lexique.md, 2_structure.md, 3_decoupe.md, 3a_genre.md, 3b_nature.md, 4_grille.md, 6_convertit.md, fusion.md, fusion_compare.md, fusion_applique.md, 7_lots.md, 9_controle.md, diagnostique.md, conventions.md
Note: the harness behaviour the finding rests on was not measured by the consolidation; this session, worktree-isolated, had a compound git-free command refused with "a worktree-isolated session's git operations must target its own worktree", which is the same guard. Same rewrite as entries 2 and 22 — one text.

### 63 · passages F09 — The Découpeur's blocking file has no `## Decision` to grep

Severity: NOTE
Decision: In `decoupeur.md`, L134-139 gives `blocked_decoupeur.md` the four `##` headings the single-stop shape uses elsewhere (cadreur.md L192-206), `## Decision` written empty.
Where: decoupeur.md L134-139 ↔ 3_decoupe.md L38 ↔ 2_structure.md L155-157
Cited: 3_decoupe.md L38 — "| Its `## Decision` is empty | 🔴 **Stop** — say the blocking file still stands, and that its `## Decision` is to fill |" · 2_structure.md L155-156 — "📌 **Grep `-A2 '^## Decision$'`**"
Owner: decoupeur.md
Follows: —

---

## Shared owners — read together

| Owner | Entries | Collision check |
|---|---|---|
| 8_code.md | 2, 62 (Git section) · 23, 26 (move 3's list) · 24, 25 (4b) · 28 (move 6) · 29 (split-back) · 46 (resume) · 60 (Findings prompt) | 2 + 62: one rewrite, five steps. 23 + 26: 23 changes the *test* (HEAD before/after), 26 cuts the *list* (after the last revert) — compatible. 24 + 25: 24 removes one file from 4b's table, 25 adds a shape test — compatible. |
| 9_controle.md | 1, 10 (phase 1 filter and count) · 33 (phase 1 b) · 32 (phase 6) | 1 defines the kept set, 10 counts it, 33 says which entries are marked — three paragraphs, no overlap. |
| 2_structure.md | 5+6 (invocation table) · 19 (guard) · 11, 50 (deletion paragraph) | 11 and 50 edit the same paragraph — one edit: the `code/decoupage.md` guard on the whole, `couverture.md` on `MODIFIED` too. |
| 4_grille.md | 4, 16, 49 (second time; row L204) | All three write or test outside a worktree the same way. |
| arbitre.md | 3, 7 (decision shape) · 45 (pointer) | 3 + 7 agree: answered → numbered; waiting → no number. |
| architecte.md | 9 (invocation 2) · 30, 31 (invocation 3 / move 2) | Different sections. |
| cadreur.md | 8, 43 · follows 33 | 8 edits `architecte/cadreur.md`'s request blocks; 43 removes a `code/decoupage.md` section; 33 fixes the reason forms of `## Entries with no lot`. |
| conventions.md | 21, 48 · follows 9 | Different paragraphs. |
| 6_convertit.md | 51, 52 | Different tables. |
| 1_lexique.md | 22, 53 | Different sections. |
| 3a_genre.md | 13, 17 · follows 5+6 | Different paragraphs (L110, L54, L255). |
| fusion.md | 18, 36 | Different sections. |
| diagnostiqueur.md | 39, 40 | Different lines. |
| detailleur.md | 27 · follows 38, 60 | 27 and 60 touch L515-519: one adds propagation, the other reads the lot from the prompt — compatible. |

---

## Summary table

| # | Severity | Decision | Where | Owner | Follows |
|---|---|---|---|---|---|
| 1 | BLOCKING | Phase 1's genre from a grep of `desc-produit.md`; keep behaviours plus every block whose line carries an entry; add `transverse` to the table; L195 says every kept block | 9_controle.md L39-42, L132-134, L187-197 ↔ convertisseur.md L172, L862-864 ↔ qualifieur.md L74-86 | 9_controle.md | — |
| 2 | BLOCKING | Commit inside the worktree before the merge; L622-625 stop blaming the agent | 8_code.md L614-625 ↔ relecteur.md L4, L46 | 8_code.md | 7_lots.md, 9_controle.md, diagnostique.md |
| 3 | BLOCKING | One shape for a waiting entry: no number written | arbitre.md L181-183, L194-198, L468-499 ↔ 8_code.md L233-240 | arbitre.md | — |
| 4 | BLOCKING | Highest `questions-existant` filed with `### Q` → write the next one empty, no agent | 4_grille.md L293-298 ↔ 5_reclasse.md L50-62 | 4_grille.md | — |
| 5+6 | BLOCKING | Questions-file rows above blocking-file rows; 3a L255 adopts 3b L265's order; L265 drops its clause | 2_structure.md L130-138 ↔ 3a_genre.md L255 ↔ 3b_nature.md L265 | 2_structure.md | 3a_genre.md, 3b_nature.md |
| 7 | TO FIX | The decision template carries the number for every entry | arbitre.md L147-157, L177-179 ↔ 8_code.md L237-240 | arbitre.md | — |
| 8 | TO FIX | Request blocks get an identifier; `## Where` carries it | cadreur.md L196-198, L227-243, L314 ↔ 7_lots.md L167-168, L182-186 | cadreur.md | 7_lots.md, architecte.md |
| 9 | TO FIX | Invocation 2 exempts `forme` like `inconsistency` and `coverage` | architecte.md L544-560, L634-652 ↔ conventions.md L263-269 | architecte.md | conventions.md |
| 10 | TO FIX | Step d counts the kept blocks | 9_controle.md L132, L187-189 ↔ convertisseur.md L857-864 | 9_controle.md | — |
| 11 | TO FIX | No deletion when `code/decoupage.md` exists; say "new cycle" as 6_convertit does — rest To settle A | 2_structure.md L202-210 ↔ 6_convertit.md L35-38 | 2_structure.md | — |
| 12 | TO FIX | `convertisseur/` is the fifth place | audit_blocages.md L26-36 ↔ 6_convertit.md L343-350 | audit_blocages.md | — |
| 13 | TO FIX | Third trigger: filed qualifieur file with `### Q` → invoke with it | 3a_genre.md L103-112, L154-155 ↔ qualifieur.md L220, L323-324 | 3a_genre.md | — |
| 14 | TO FIX | Same for the classeur | 3b_nature.md L102-113 ↔ classeur.md L169-175 | 3b_nature.md | — |
| 15 | TO FIX | — (To settle B) | 6_convertit.md L143-144 ↔ convertisseur.md L487-489, L632-634 | — | — |
| 16 | TO FIX | Filed sondeur file with `### Q`, no marker, no existant → write the next sondeur file empty, first time closed | 4_grille.md L176-183, L197-204 ↔ 2_structure.md L249-250 | 4_grille.md | — |
| 17 | TO FIX | The `### Q` guard excludes `questions-architecte-*.md` | 3a_genre.md L54-59 ↔ conventions.md L122-126 | 3a_genre.md | 3b_nature, 3_decoupe, 4_grille, 5_reclasse, 6_convertit, fusion_compare |
| 18 | NOTE | Leave `questions-architecte-*.md` at the root | fusion.md L113-117 ↔ conventions.md L85 | fusion.md | fusion_applique.md |
| 19 | TO FIX | The L86 guard bears on a root lexicographe file alone; L27-29 split the two reads | 2_structure.md L27-29, L86-90, L140-143 ↔ 1_lexique.md L205-206, L263 | 2_structure.md | — |
| 20 | TO FIX | Re-invocation moves before the merge, inside the worktree | 3_decoupe.md L204-207 ↔ L175-181 | 3_decoupe.md | — |
| 21 | TO FIX | File the empty architecte file too at *Git, before invoking* | conventions.md L86, L137-140 ↔ architecte.md L334, L337 | conventions.md | — |
| 22 | TO FIX | Commit inside the worktree, as conventions L232-235 | 1_lexique.md L230-236 ↔ conventions.md L232-235 | 1_lexique.md | nine upstream commands |
| 23 | TO FIX | Empty attempt = no new commit between before and after the Réalisateur | 8_code.md L147-158, L164-167 ↔ concepteur L286, testeur L303, realisateur L695 | 8_code.md | — |
| 24 | TO FIX | 4b's table excludes `blocked_relecteur.md` | 8_code.md L227-235 ↔ L267-270, L572-581 | 8_code.md | — |
| 25 | TO FIX | Two filled-tests by shape: numbered headings vs four-heading files | 8_code.md L233-240 ↔ arbitre.md L142-144 | 8_code.md | — |
| 26 | TO FIX | The revert/diff list is cut after the lot's last `Revert "<lot>: …"` — F16 To settle C | 8_code.md L142-155, L186-189, L486-492 ↔ L595-598 | 8_code.md | — |
| 27 | TO FIX | Findings rewrite propagates changed signatures to the block's later sheets | detailleur.md L507-519 ↔ relecteur.md L209-211 ↔ 8_code.md L294-305 | detailleur.md | 8_code.md |
| 28 | settled | L313-315 separates `stop.md` (main checkout) from a blocking file filled in the worktree; arbitre unchanged | 8_code.md L313-315 ↔ arbitre.md L466-499 | 8_code.md | — |
| 29 | TO FIX | L548 routes through *When the split comes back*; the third-return stop still closes the worktree — "what next" To settle D | 8_code.md L548-549 ↔ L473-480, L510-518 ↔ detailleur.md L484 | 8_code.md | — |
| 30 | TO FIX | Invocation 3 skips blocks, not files | cadreur.md L240-243 ↔ architecte.md L686-690 | architecte.md | — |
| 31 | TO FIX | A dash raises `inconsistency` only on `comportement` and `référence` blocks | convertisseur.md L862-864 ↔ architecte.md L413-422 | architecte.md | — |
| 32 | TO FIX | Phase 6 derives the block from the lot through `tracabilite-full.md` | 9_controle.md L366-374 ↔ detailleur.md L326-330, realisateur.md L303-307 | 9_controle.md | — |
| 33 | TO FIX | `carried` only for "already carried by the code"; three greppable reason forms | cadreur.md L494, L762-774 ↔ 9_controle.md L149-154 | 9_controle.md | cadreur.md |
| 34 | QUESTION | — (To settle E) | fusion.md L50 ↔ fusionneur.md L355-357, L585 | — | — |
| 35 | QUESTION | — (To settle F) | fusion.md L46 ↔ L18-20 | — | — |
| 36 | QUESTION | Rows 2-3 bear on the two files this command routes; row 3 names the decisions files; the Rédacteur carries on after a block | fusion.md L44-45, L101, L201 ↔ redacteur.md L750-753 | fusion.md | redacteur.md |
| 37 | QUESTION | — (To settle G) | 9_controle.md L427-431 ↔ diagnostiqueur.md L616-620 | — | — |
| 38 | NOTE | Name the part `## Intent and vocabulary` | verificateur.md L62, L415 ↔ convertisseur.md L138 ↔ detailleur.md L68, L607 | verificateur.md | detailleur.md |
| 39 | NOTE | `# Preamble` in `desc-bug.md` | diagnostiqueur.md L563 ↔ convertisseur.md L144-146 | diagnostiqueur.md | — |
| 40 | NOTE | Move 7 reads `## Trigger` for a second requirement | diagnostiqueur.md L411-415 ↔ L514-519 | diagnostiqueur.md | — |
| 41 | NOTE | Drop the placements field | concepteur.md L231-233, L314-317, L338-340 ↔ 8_code.md L57-58 | concepteur.md | — |
| 42 | NOTE | The Testeur's test file is declared, not outside the lot | testeur.md L86-87, L332-335 ↔ concepteur.md L114-118 ↔ relecteur.md L453-459 | testeur.md | relecteur.md |
| 43 | NOTE | Drop `## Conventions requests` | cadreur.md L245-248, L848-851 ↔ 7_lots.md L194-195 | cadreur.md | — |
| 44 | NOTE | — (not verified: `docs/process/` not opened) | PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010 | — | — |
| 45 | NOTE | Name `/7_lots` | arbitre.md L210-211 ↔ 8_code.md L482-484 | arbitre.md | — |
| 46 | NOTE | Resume stops on `code/blocked_verificateur.md` | 8_code.md L69-81 ↔ verificateur.md L176 ↔ 7_lots.md L172 | 8_code.md | — |
| 47 | NOTE | Second move is the only reader | 5_reclasse.md L109 ↔ convertisseur.md L53 | 5_reclasse.md | — |
| 48 | NOTE | Rename moves under *Git, once it has reported* | conventions.md L165-172 ↔ L228-239 | conventions.md | — |
| 49 | NOTE | `Global:` grep before the worktree | 4_grille.md L300-307 ↔ L266-268 | 4_grille.md | — |
| 50 | NOTE | `couverture.md` wiped on `MODIFIED` too | 2_structure.md L202-221 ↔ conventions.md L89 | 2_structure.md | — |
| 51 | NOTE | Blocking table reads per file | 6_convertit.md L49-53 ↔ L191-194 | 6_convertit.md | — |
| 52 | NOTE | First-match rule on the relay table | 6_convertit.md L410-419 ↔ L167-168 | 6_convertit.md | — |
| 53 | NOTE | L99 names `/3_decoupe` | 1_lexique.md L93-101 ↔ 2_structure.md L135 | 1_lexique.md | — |
| 54 | NOTE | — (To settle H) | 1_lexique.md L60 ↔ L263 | — | — |
| 55 | NOTE | — (To settle I) | 3a_genre.md L258 ↔ 3b_nature.md L268 | — | — |
| 56 | NOTE | — (To settle J) | 3a_genre.md L256 ↔ qualifieur.md L95-102 | — | — |
| 57 | NOTE | — (moot, settled: change nothing) | .claude/commands/cycle.md ↔ .claude/CLAUDE.md L51 | — | — |
| 58 | NOTE | Covered by 26 | 8_code.md L141-155 ↔ L502-503 | 8_code.md | — |
| 59 | NOTE | A mixed line: sheets read, unmatched intentions found with the mark as reason | 9_controle.md L151-152, L171-179 ↔ controleur.md L215-220 | controleur.md | 9_controle.md |
| 60 | NOTE | The Findings prompt names the lot | 8_code.md L297-305 ↔ detailleur.md L515-519 | 8_code.md | detailleur.md |
| 61 | NOTE | Files from `Touches`, symbols from `Modifies` | audit_conventions.md L106-107 ↔ cadreur.md L822-826 | audit_conventions.md | — |
| 62 | NOTE | Name the exit from the worktree before the merge | 8_code.md L614-620 ↔ L102-103 | 8_code.md | fourteen commands with the section |
| 63 | NOTE | Four `##` headings for the Découpeur's blocking file | decoupeur.md L134-139 ↔ 3_decoupe.md L38 ↔ 2_structure.md L155-157 | decoupeur.md | — |

---

## Counts

- **63 entries**, 62 distinct defects (5 and 6 are one).
- **Decided: 54** — entries 1, 2, 3, 4, 5+6, 7, 8, 9, 10, 11 (guard), 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26 (F06), 27, 28, 29 (F10 and the git part of F12), 30, 31, 32, 33, 36, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 58 (through 26), 59, 60, 61, 62, 63.
- **`## To settle`, Decision empty: 7** — entries 15, 34, 35, 37, 54, 55, 56. The section holds 10 items (A-J): items A, C, D are residual questions on entries 11, 26, 29, which carry a decision on their mechanical part.
- **Could not verify: 1** — entry 44 (`docs/process/`, not opened by this session).
- **Moot, change nothing: 1** — entry 57 (settled by the Product Owner).

54 + 7 + 1 + 1 = 63.

---

## To settle

Each item: what is open, the options, what each costs. The `Decision` of the entry it belongs to stays empty (A, C, D excepted — their entry carries the mechanical part).

### A — Entry 11: how a `NEW` block created after the split reaches the code

Once `code/decoupage.md` exists, `/2_structure` will delete nothing and say the block belongs to a new cycle (the decision of entry 11). What that new cycle is, nothing says.

- **Option 1 — a `bugfix-NN/` cycle**: the Product Owner writes the new behaviour into a `bug-list.md` as a gap ("the application does not do X"), and `/diagnostique` opens a correction cycle. Cost: nothing to write; the block sits in `desc-produit.md` with `NEW` and is probed by the grid, but its entries never reach `spec-technique.md` — the Contrôleur will report it missing at every later control until the correction cycle's `B<n>` marks it `carried`. A wording in `2_structure.md` L202-210 naming this route is a one-line follow-up.
- **Option 2 — `/6_convertit` learns to append**: a re-conversion after the split that only *adds* entries (new numbers at the end of each section, no renumbering) would keep the coded lots' citations valid. Cost: a new mode of the Convertisseur and of `/6_convertit`, the Cadreur's block C extended to "new entries no lot cites" — a campaign of its own.
- **Option 3 — forbid it**: `/2_structure` refuses to integrate an answer that creates a `NEW` block once the split is cut. Cost: the answer is lost or hand-carried; the Product Owner decides where it goes.

### B — Entry 15: where a product answer that changed no block lands for the Convertisseur

The Convertisseur marks `<<ASSUMED B40: …>>`, asks; the Product Owner confirms the assumption; the Rédacteur changes nothing (the block already implied it); `/6_convertit` L144 reruns the nature on a byte-identical part; the agent meets the same gap and marks again. Two fixes, each respecting a different sentence of the text.

- **Option 1 — the Convertisseur reads its answered file**: `/6_convertit`'s row L144 names, in that nature's prompt, the highest `questions-convertisseur-NN.md` under `questions/convertisseur/`, and `convertisseur.md` L632-634 admits that file beside the technical one (the answer to a mark's question lifts the mark). Cost: two files, one exception to "a product answer reaches you through the product file" (L633-634) — the same exception `/3a_genre` L88-97 already makes for the Qualifieur, so there is precedent. Owner would be `6_convertit.md`, Follows `convertisseur.md`.
- **Option 2 — the Rédacteur writes the confirmation into the block**: `redacteur.md` invocation 2 gains a rule — an answer that restates what a block already implies is still written into the block, making the implicit explicit, with `MODIFIED`; the part then differs, row L139 fires, the agent reads a block that says it. Cost: one rule in `redacteur.md` with a soft test ("already implied"), one opus invocation per such answer either way; row L144 of `/6_convertit` becomes moot and can go. Respects L633-634 to the letter.

A minute of the Product Owner's decides which principle holds: "every product answer goes through the product file" (option 2) or "an agent may read its own answered file" (option 1, already true of three other agents).

### C — Entry 26, F16's sentence: a `sheet` cause on a lot that is not the last coded

`8_code.md` L595-598: a filled decision on a lot already carrying a PASS re-runs its agent and its review. If that review's `## Cause` reads `sheet`, move 4 reverts the lot's commits — commits later lots were built on — and nothing says what happens to those later lots.

- **Option 1 — treat it as a redécoupage**: a `sheet` cause on a lot that is not the last coded goes through *When the split comes back*: every lot after it with a PASS is reverted too and re-coded. Cost: many lots redone for one sheet; safe.
- **Option 2 — forbid the re-review path from producing `sheet`**: on a re-run of a PASSed lot, the Relecteur can FAIL on the code but not on the sheet (the sheet was reviewed PASS once); a wrong sheet found then is a `bug-list.md` gap for a correction cycle. Cost: one rule in `relecteur.md`, one in `8_code.md` L595-598; the defect is fixed later, not now.
- **Option 3 — accept the hole**: say at L595-598 that a `sheet` cause there stops the command, and the Product Owner decides. Cost: one sentence; she is asked each time it happens.

### D — Entry 29, F12's sentence: what runs after the Product Owner's decision on a third return

At the third redécoupage the command stops (L475-477) and `code/redecoupage.md` reaches `HEAD` (decision of entry 29). What she does next is written nowhere: `/7_lots` would dispatch to block C again (a fourth split), `/8_code` would count three and stop again.

- **Option 1 — she runs `/7_lots` by hand after amending**: she edits `code/redecoupage.md` (or the product file), and `/7_lots` re-splits; `/8_code`'s count would then need to reset — say, on a `code/redecoupage.md` she has annotated, or by her renaming the archived files. Cost: a rule in `/8_code` L473-480 saying what resets the count.
- **Option 2 — the third return closes the cycle**: the feature stops there; the remaining lots go to a `bug-list.md` and a correction cycle with a new split. Cost: one paragraph in `/8_code` and `/7_lots`; the unfinished lots are not lost, they change cycle.

### E — Entry 34: bug-fix decisions on a first feature, before `INIT`

Row 8 (`fusion.md` L50) runs the Fusionneur's invocation 3, which writes into the global (fusionneur L585-593), before invocation 1 tests the global for `# Application` alone (L355-357). On a first feature that went through a bug-fix cycle, `INIT` never fires and the feature is merged sentence by sentence into a near-empty global.

- **Option 1 — invocation 3 writes into the copy on a first feature**: `fusionneur.md` invocation 3 tests the global first; `# Application` alone → its merges go into `desc-produit-fusion.md` (which `INIT` then copies over the global) instead of the global. Cost: one branch in the fusionneur; the Rédacteur's copy is then edited by two agents in turn, which L716-717 and L725-729 do not anticipate.
- **Option 2 — row 8 is skipped on a first feature**: `fusion.md` row 8 adds "and the global holds more than `# Application`"; on a first feature the bug-fix decisions are lost unless carried by hand. Cost: one condition; a loss she has to know about.
- **Option 3 — reorder**: invocation 3 runs after invocation 2 (after `INIT` or the compare has landed). Cost: the routing table's whole logic (rows 4, 7, 8, 9 and "row 8 fires once" L71-73) has to be redone — a campaign of its own.

### F — Entry 35: a correction cycle coded after the merge

`fusion.md` L18 says one run per feature, once every bug-fix cycle has been coded; row 4 stops for good on `rapport-fusion.md`. A `bugfix-NN` cut afterwards never carries its decisions into the global.

- **Option 1 — accept it as the stated intent**: L18 already says so; add that a correction after the merge is a new feature's, or is hand-carried. Cost: one sentence.
- **Option 2 — allow a re-run**: row 4 stops only when no `bugfix-NN/` is newer than `rapport-fusion.md`; a newer one sends the run to row 8 for its decisions alone (invocation 3, then the compare on the delta). Cost: a date or number comparison in the table, and invocation 1's compare has to cope with a global that already carries the feature — which it does not today (L359-360).

### G — Entry 37: the shape of `B<n>` inside a gap of `bug-list.md`

`bug-list.md` is hers, hand-written. `9_controle.md` L427-431 says a gap she takes from the report "keeps its `B<n>`", `diagnostiqueur.md` L616 reads it — neither says in what form. She picks one greppable form (for instance the identifier in parentheses at the end of the gap's first line, as the Diagnostiqueur writes it into `desc-bug.md` at L620); then `9_controle.md` L427-431 states it (owner) and `diagnostiqueur.md` L616 reads by it (follows). Cost: her choice, two sentences.

### H — Entry 54: a `/1_lexique` run by mistake after "4 wrote none"

The answered file sits alone at the root and reads as invocation 3 again (L60) — one opus invocation, no damage.

- **Option 1 — accept**: the relay at L263 already says `/2_structure`; a run by mistake costs one invocation. Cost: nothing.
- **Option 2 — a record**: invocation 4 leaves a mark the table can test (a line in `lexique.md`, or the answered file renamed on filing). Cost: a new state to maintain in `lexicographe.md` and `1_lexique.md`, for a mistaken run.

### I — Entry 55: "once, not until it clears" has no record across runs

`3a_genre.md` L258 and `3b_nature.md` L268 rely on the Product Owner counting the second run.

- **Option 1 — accept**: she runs it once more and stops; the rule is a rule for her. Cost: nothing.
- **Option 2 — a record**: the empty `Genre:`/`Nature:` count of the previous run is written somewhere the next run reads (the questions file's header, a marker file). Cost: a state file for a defect-of-the-run case that should not recur.

### J — Entry 56: the two-genre route can repeat as long as the rewrite holds two genres

Block → `/2_structure` → `/3_decoupe` → `/3a_genre` → block again, bounded only by her decision each time (qualifieur L95-102).

- **Option 1 — accept**: each turn she writes the decision, so she sees the repetition and can settle it by splitting the block herself in the decision. Cost: nothing; a sentence at L256 saying so.
- **Option 2 — cap it**: on the second identical block, `/3a_genre` stops and says the rewrite did not settle it. Cost: a count across runs — the same record item I lacks.

---

*54 entries decided · 7 with an empty `Decision` (15, 34, 35, 37, 54, 55, 56) · 1 not verified (44) · 1 moot (57) — 63 in all. Ten `## To settle` items, A-J; three of them (A, C, D) are residual questions on entries that carry a decision.*
