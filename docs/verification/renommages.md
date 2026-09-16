# Vérification — renames (V2.1)

Read: every file of `.claude-new/` (20 agents, 21 commands, `CLAUDE.md`,
`scripts/grouper.py`) and `docs-new/process/` (7 files), by grep on each
name below. Old names were established from `.claude/` and
`docs/process/` where the investigation did not state them. Line numbers
are the **new** file's.

Summary: **16 names checked, 5 removed names checked.** Found —
**3 BLOCKING** (a `Défaut:` accepted by silence never passes the
empty-`Answer:` gates · `technique-<nature>.md` is written and read by
nobody, with no rerun trigger · `desc-produit-fusion.md` is the
Fusionneur's only product file and `/fusion_compare` never has it
written) · **8 TO FIX** · **7 NOTE** · **2 removed names survive**
(`[integrated:` and a `blocked_verificateur` with a `## Decision`, both
in `cycle.md`).

---

## A. NEW OR CHANGED NAMES

### 1. `Touches` field of a lot

| | |
|---|---|
| **Writes** | Cadreur — `cadreur.md` L713 (template), L718-725 (rule: files declaring no symbol; same file in two lots allowed) |
| **Reads** | Vérificateur — `verificateur.md` L284 (excluded from the overlap count). Concepteur — `concepteur.md` L141, *"where the sheet's `Modifies` or `Touches` points"* |
| **Old name** | None — files used to go into `Modifies` (old `cadreur.md` L428) |

**A-1 — `concepteur.md` L137-141.** TO FIX. *"The sheet says which
files the lot touches … put it where the sheet's `Modifies` or
`Touches` points."* The sheet has neither field: `detailleur.md`
L229-260 writes five fields (`## Signatures`, `## Acceptance criteria`,
`## Dependencies`, `## Conventions`, `## Requests`) and `detailleur.md`
never mentions `Touches` or `Modifies`. The Concepteur is sent to a
field that does not exist in the file it reads. Either the Détailleur
carries the lot's `Modifies`/`Touches` into the sheet, or the Concepteur
reads `code/decoupage.md` (which its reading list does not name).

**A-2 — `realisateur.md` L162-166.** NOTE. *"`## Outside the lot` names
every file you touched that the sheet does not declare … it is not in
your `Modifies`"* — same gap as A-1: the sheet declares no files, and
`Modifies` no longer carries files. The rule still reads in the old
sense (`Modifies` = files).

**A-3 — `cadreur.md` L491-499, L615.** NOTE. Move 6 sends every grep hit
into `Modifies` *"by name"* and move 8 says *"the lot carries the
declaration"* — no move ever writes into `Touches` (already reported as
C11 PARTIEL in `agent-cadreur.md`; listed here for completeness, not
re-counted).

### 2. `## Findings`, `## Attempts` of a verdict

| | |
|---|---|
| **Writes** | Relecteur — `relecteur.md` L121, L129 (template), L144-152 (rules) |
| **Reads `## Attempts`** | `/8_code` — `8_code.md` L41-43, L111-116 (retry count on disk) |
| **Reads `## Findings`** | Nobody by name. The fresh Réalisateur on a FAIL reads *"the verdict"* (`realisateur.md` L50, L475) and fixes *"the point reported"* (L479) — the heading is never named |
| **Old name** | None. Old `## Cause` carried *"category — gap"* (old `relecteur.md` L112-113); the gap is now in `## Findings`, and `## Cause` is *"the category alone"* (L154). No `understanding — <gap>` pattern survives (grep clean). Old retry count lived in the run's memory; L111 explicitly rejects that |

**A-4 — `8_code.md` L41-43 vs L134-135.** TO FIX. L41: *"three lines:
`## Status` … `## Attempts` … `## Cause`"* (plus `## Symbol
divergences` on the final verdict, L45). L134: *"You read two fields of
a verdict — `## Status` and `## Symbol divergences`, and nothing
else."* The second sentence contradicts the first and would forbid
reading `## Attempts`, which L113 says is where the count lives.

### 3. `## Declared` of a conception report

| | |
|---|---|
| **Writes** | Concepteur — `concepteur.md` L178 (template of `code/<lot>/conception.md`) |
| **Reads** | Réalisateur — `realisateur.md` L72, L496 (*"which symbol landed in which file"*). Testeur — `testeur.md` L50, L61, L154. Relecteur — `relecteur.md` L57-58. All three name the file, none names the heading |
| **Old name** | None — the Concepteur is a new agent |

**A-5 — `GRILLE_FERMETURE_TECHNIQUE.md` L134 `## Declared links`.**
NOTE. A homonym in the technical grid (a section of the technical
document), unrelated to the conception report. No confusion in the
agents, but a grep for `## Declared` returns both.

### 4. `Genre:` and `Global:` lines of a block

| | |
|---|---|
| **Writes `Genre:`** | Rédacteur, empty — `redacteur.md` L60-64, L442. Decoupeur, empty on each half — `decoupeur.md` L179-185, L205. Qualifieur, filled — `qualifieur.md` L125, L178, L261 (*"the `Genre:` line, and nothing else"*) |
| **Reads `Genre:`** | `/3a_genre` L78, L89, L130, L205 (`^Genre:$`) · `/3b_nature` L78 (keeps `comportement` only) · Classeur L34, L50 · `/4_grille` L87-106, L139 (`comportement` probed, `transverse` passed to every sondeur) · Sondeur L48 · `/5_reclasse` L50-55, L90, L100 (one grep per genre) |
| **Writes `Global:`** | Rédacteur — `redacteur.md` L62, L75-83 (absent, never empty). Decoupeur copies it on every half — `decoupeur.md` L185, L211 |
| **Reads `Global:`** | `/4_grille` L164 (`grep -B1 '^Global: '`) · Sondeur invocation 3 — `sondeur.md` L136, L347, L353 · `GRILLE_EXISTANT.md` L11, L101 |
| **Old name** | None — old blocks carried `Nature:` alone (old `redacteur.md` L59-60). No block template without `Genre:` survives in the Rédacteur or the decoupeur |

**A-6 — `5_reclasse.md` L117-120.** NOTE. The `desc-par-nature.md`
template shows a block as `### B3 … / Nature: model` with no `Genre:`
and no `Global:` line, while L133-135 says the block is *"copied as it
stands, by script"* except its marker. The copy will carry
`Genre: comportement` and, when present, `Global:`; the template does
not. Cosmetic, but the Convertisseur's input then holds two lines its
file never describes.

**A-7 — `qualifieur.md` L51-56 vs `5_reclasse.md` L83-90.** TO FIX. The
six genre values are written with accents and spaces — `référence`,
`hors périmètre` — and `/5_reclasse` greps `^Genre: <genre>$` to fill
`par-genre/references.md` and `par-genre/hors-perimetre.md`. Nothing
states the value → file-name mapping (the way `6_convertit.md` L116-118
does for natures: *"a hyphen for a space"*). An orchestrator grepping
`^Genre: references$` gets nothing and writes an empty file, which L94
says is a valid outcome.

**A-8 — `Genre:` is not read by `/9_controle`.** QUESTION. Phase 1
(`9_controle.md` L69-92) puts *"every block"* of `tracabilite.md` into
the block-to-lot map, and a block with no lot gets a dash and *"still
needs an answer"*. Blocks of genre `directive`, `recette`, `hors
périmètre` and `référence` produce no lot by construction. Are they
meant to be confronted with the sheets, or should the map be built from
`Genre: comportement` alone?

**A-9 — `Global:` and the Fusionneur.** NOTE. The Fusionneur, whose
work is to place each block into a section of the global, never reads
the `Global:` line (grep clean in `fusionneur.md`); it works from the
global's index (L162). The line is consumed by the existing-product
reading only. Not a defect, but the one agent that most obviously could
use it does not.

### 5. `Défaut:` line of a question

| | |
|---|---|
| **Writes** | Sondeur — `sondeur.md` L280-295 (proposal founded on a transverse block or on blocks already following the pattern; `Answer:` stays empty) |
| **Copies** | Assembleur — `assembleur.md` L114-131, L225-229 (copied word for word, never moved from a dropped question to the kept one) |
| **Reads** | Rédacteur — `redacteur.md` L539-543 (*"No `Answer:` written means the Product Owner accepted it"*). `/4_grille` L144 names the mechanism |
| **Old name** | None (grep of old tree clean) |

**A-10 — `1_lexique.md` L70, `2_structure.md` L29, L94, `cycle.md` L53,
L62, L84.** BLOCKING. Every gate between the sondeurs and the Rédacteur
stops on *"a file with an empty `Answer:`"*. A *défaut* the Product
Owner accepts by silence — the very case `sondeur.md` L293-295 and
`redacteur.md` L541 describe — is an entry with an empty `Answer:`. The
file never reaches the Rédacteur: `/1_lexique` stops, `/2_structure`
stops. Either the gates test *"empty `Answer:` **and** no `Défaut:`"*,
or the Product Owner has to write the default back by hand, which is
what `4_grille.md` L144 says the line exists to avoid.

**A-11 — `sondeur.md` L280.** TO FIX. *"One more line, and `Answer:`
carries the proposal"* — contradicted by the template two lines below
(`Défaut:` carries it, `Answer:` empty) and by L293 *"`Answer:` stays
empty, as always"*. Reads as the trace of an earlier form where the
proposal went into `Answer:`.

**A-12 — Lexicographe invocation 3.** NOTE. `lexicographe.md` never
mentions `Défaut:` (grep clean). Invocation 3 sweeps *"the words those
answers bring"*; an accepted default's words are in the `Défaut:` line,
not in `Answer:`. Whether the sweep covers them is not stated.

### 6. `en anglais :` line of a lexicon entry

| | |
|---|---|
| **Writes** | Rédacteur — `redacteur.md` L163-172 (first rendering of a settled concept), L308-310 (the only thing it may write in `lexique.md`), L371-372 (invocation table) |
| **Reads** | Rédacteur — L172-173 (*"When the entry already carries one, you take it"*). Lexicographe — `lexicographe.md` L176-179 (never writes or touches it), L430-432 (invocation 3 compares against it) |
| **Old name** | None. Old `redacteur.md` L288-289 wrote nothing in `lexique.md`; no surviving rule says the Rédacteur does not write there |

Only three files name `lexique.md` (`lexicographe.md`, `redacteur.md`,
`1_lexique.md`). Consistent.

**A-13 — `lexicographe.md` L155 vs `redacteur.md` L170.** NOTE. The
lexicon template shows `en anglais : closed segment` under an entry with
no `remplace :` line, the Rédacteur's shows it after `remplace :`.
Position within the entry is not fixed anywhere; harmless as long as
nobody greps the line by position.

### 7. `par-genre/` and its six files

| File | Writes | Reads |
|---|---|---|
| `par-genre/comportements.md` | `/5_reclasse` L83 | `/5_reclasse` move 2 (L111-112, L150) — **not** the Convertisseur, despite L83 |
| `par-genre/transverses.md` | `/5_reclasse` L84 | Convertisseur — `convertisseur.md` L51, L113, L135 |
| `par-genre/directives.md` | `/5_reclasse` L85 | Architecte — `architecte.md` L274, L277, L469-475 |
| `par-genre/references.md` | `/5_reclasse` L86 | Convertisseur — `convertisseur.md` L52 (reading table, *"invocation 2 only"*) and **nowhere else in the agent** |
| `par-genre/hors-perimetre.md` | `/5_reclasse` L87 | Convertisseur — `convertisseur.md` L53, L112 (preamble *Out of scope*) |
| `par-genre/recette.md` | `/5_reclasse` L88 | `/9_controle` L171 (phase 4, merged into `code/recette-ordonnee.md`) |

Also: `/6_convertit` L40 stops when `par-genre/` is absent;
`/2_structure` L117 removes the folder when a `NEW` block appears.
**Old name**: none — the old `/5_reclasse` wrote `desc-par-nature.md`
alone (old L9, L59). The old Convertisseur took *"out of scope"* from
*"the product file's text outside the blocks"* (old L103).

**A-14 — `convertisseur.md` L52 vs the body.** TO FIX.
`par-genre/references.md` is declared as read at invocation 2 and no
move uses it: the preamble table L109-114 does not name it, §9 Text
(L74, L88-90) does not name it, invocation 2's row L540 does not name
it. `5_reclasse.md` L86 says *"The Convertisseur — its Text section"*;
the Convertisseur's Text section says nothing of the kind. A file that
is written and declared read, but consumed by no move.

**A-15 — `convertisseur.md` L539-540, invocation table.** TO FIX.
Invocation 1 reads *"Your blocks · the headings · the grid"* — not
`par-genre/transverses.md`, which L51 and `5_reclasse.md` L84 say
*"every nature invocation"* reads. Invocation 2 reads *"the product
file, its text outside the blocks"* — the old source of *Out of scope*
— and neither `hors-perimetre.md` nor `references.md`. The table is the
old reading list; the per-file table at L48-62 is the new one.

**A-16 — `5_reclasse.md` L80 *"Six files, at the feature folder's
root"*.** NOTE. They are in `par-genre/`, a folder below the root.

**A-17 — `2_structure.md` L117-122.** NOTE. Three paths are removed
(`par-genre/`, `desc-par-nature.md`, `spec-technique.md`); the
explanation says *"those two are derived from the product file"*. Old
count.

### 8. `GRILLE_EXISTANT.md`, `GRILLE_CONVENTIONS_RETIREES.md`

| | |
|---|---|
| **`GRILLE_EXISTANT.md`** | Written by nobody in the chain (a process document). Read by the Sondeur at invocation 3 — `sondeur.md` L40, L367; passed by `/4_grille` L180. Named by `PROCESS_AMONT.md` L959 as the destination of old `C1.3` |
| **`GRILLE_CONVENTIONS_RETIREES.md`** | Read by nobody. Named once, by `GRILLE_CONVENTIONS.md` L580 (*"holds them, with their text and the reason"*). Not in the Architecte's reading list, not in `/conventions`, not in `/audit_conventions` — consistent with its own header (*"to be able to put them back — not to remember them"*) |
| **Old name** | None for either. `CLAUDE.md` L177 forbids opening `docs/process/` for the orchestrator; the commands only pass grid paths |

**A-18 — `4_grille.md` L47-51 and L290.** NOTE. The on-disk table of
blocking files lists the four sondeur files and the assembleur's, not
`blocked_existant.md` which the invocation at L187 names at the feature
root; L290 checks `cadrage-produit/blocked_*.md` only. A block written
by the existing-product reading is detected by no check before the
rerun.

### 9. `desc-produit-fusion.md`

| | |
|---|---|
| **Writes** | Rédacteur, invocation 3 — Merging — `redacteur.md` L373, L638-670 (copy of `desc-produit.md` with every `code/decisions-produit.md` folded in, markers stripped; written even as a faithful copy). Triggered by `/fusion` row 10 (`fusion.md` L49, L58-68) |
| **Reads** | Fusionneur — `fusionneur.md` L45 (*"never `desc-produit.md`"*), every invocation |
| **Old name** | The Fusionneur read `desc-produit.md`. No surviving reference: `fusionneur.md` names `desc-produit.md` only to forbid it; `fusion.md` L40 tests it for existence only |

**A-19 — `fusion_compare.md` and `fusion_applique.md`.** BLOCKING. Both
invoke the Fusionneur directly (`fusion_compare.md` L9, L42) with the
generic prompt and no row-10 equivalent; `6_convertit.md` L340 offers
`/fusion_compare` right after the conversion, before any
`code/decisions-produit.md` exists. The Fusionneur then looks for
`desc-produit-fusion.md`, which only the Rédaction's invocation 3 writes
and only `/fusion` triggers. Either the two commands run row 10 first,
or the Fusionneur falls back to `desc-produit.md` — which L45 forbids.

**A-20 — `fusion.md` L93.** NOTE. The invocation template carries
*"Feature folder … <Which invocation>"* only, while L64-66 requires the
Rédacteur to be *named every `code/decisions-produit.md`, in cycle
order*. The parameter is described in prose and absent from the
template.

**A-21 — `redacteur.md` L3.** NOTE. The description says *"Two
invocations"*; the file has three (L373, L638). Same on
`fusionneur.md` L3 (*"Two invocations"*, three in the file — L460).

### 10. `code/recette.md`, `code/recette-ordonnee.md`

| | |
|---|---|
| **`code/recette.md`** | Writes: Testeur — `testeur.md` L52, L170 (*"at the split's root"*), L193. Reads: `/9_controle` L170 (phase 4) |
| **`code/recette-ordonnee.md`** | Writes: `/9_controle` L196. Reads: the Product Owner — L279 (*"What the Product Owner checks by hand"*); no agent, no command (`deploie.md` grep clean) |
| **Old name** | None (old `9_controle.md` grep clean for `recette`). `9_controle.md` L191-194 recalls *"a manual test file has existed and was abandoned"* — history, not a surviving name |

### 11. `code/registre-questions.md`, `code/decisions-produit.md`

| | |
|---|---|
| **`code/registre-questions.md`** | Writes: `/9_controle` L209 (phase 5). Reads: **nobody** — L280 says `—`; `audit_blocages.md` reads `blocked_*` files directly, not the register |
| **`code/decisions-produit.md`** | Writes: `/9_controle` L227-233 (phase 6, written even empty). Reads: Rédacteur at `/fusion` — `9_controle.md` L233, L281; `fusion.md` L64-66; `redacteur.md` L634-636 (*"every decisions file the prompt names"* — the file name itself never appears in the agent) |
| **Old name** | None |

**A-22 — `code/registre-questions.md`.** NOTE. Written every run,
consumed by no agent, no command and no audit (`audit_blocages.md` reads
the blocking files themselves). Its stated purpose — *"ten together let
a shape show"* (L206-207) — implies a reader across cycles that nothing
names.

### 12. `technique-<nature>.md` of the Convertisseur

| | |
|---|---|
| **Writes** | Convertisseur — `convertisseur.md` L59, L294 (`convertisseur/technique-<nature>.md`, `technique-transversal.md` at invocation 2), L316-330 (shape: `Entries:`, `Question:`, `Answer:`) |
| **Reads** | **Nobody.** No command names it (grep of `.claude-new/commands` for `technique-` is empty). The agent's own reading table L48-62 lists it as an output only, and L328-330 says *"the answer is not written anywhere afterwards — it is applied when the section is written again"* without saying who reads it back |
| **Old name** | None. The old Convertisseur had one questions file per nature |

**A-23 — `6_convertit.md`, the whole command.** BLOCKING. The command:
does not check the file was written (L182-186 checks `questions-<nature>.md`
and `<nature>-notes.md` only); does not merge it into the root
`questions-convertisseur-NN.md` (L276-284 — natures' `questions-*` and
`questions-transversal.md` only); does not file it into `closed/` (L74-78
— `questions-*.md` only); does not pass it back to the agent on rerun
(L160-165); and its *Which natures run* table L120-127 has no row for
*"`technique-<nature>.md` carries answers"* — a nature whose input is
byte-identical **waits** (L126). So the *short loop* the command relays
at L334 (*"Answer them, then `/6_convertit`"*) reruns nothing: the
answered file is never read, and the nature never runs. The
`/1_lexique` route (L335) passes the same file to the Lexicographe,
which does not know the `Entries:` shape either.

### 13. `questions-existant-NN.md`

| | |
|---|---|
| **Writes** | Sondeur, invocation 3, at the path `/4_grille` gives — `4_grille.md` L186; `/4_grille` itself writes it empty when no block carries `Global:` — L169 |
| **Reads** | `/4_grille` L160-162 (presence = the second time has run; `questions/existant/` once filed), L191-192 (numbering), L452. Then the generic route: `/1_lexique` (Lexicographe invocation 3, *"any prefix"*) → `/2_structure` (Rédacteur invocation 2, `2_structure.md` L91 *"any prefix"*). Filed by `/5_reclasse` L62-65 into `questions/<agent>/` |
| **Old name** | None |

Consistent with the generic `questions-<agent>-NN.md` handling; nothing
surviving.

### 14. Grid question `C1.3` → `E3.1`; `C1.4`–`C1.7` → `C1.3`–`C1.6`

| | |
|---|---|
| **New grid** | `GRILLE_CADRAGE_PRODUIT_V2.md` L361-386: `C1.1`–`C1.6`, six questions; L25 example `C1.5`; L386 *"These three are the only C1 questions with several instances"* (`C1.4`, `C1.5`, `C1.6`) — count holds |
| **Moved question** | `GRILLE_EXISTANT.md` L81 `E3.1` *"A behaviour the section describes and the block replaces"* — the old `C1.3` (*"For each existing rule the feature touches: kept, changed, retired?"*), reworded |
| **Old numbering survives** | Only in `PROCESS_AMONT.md` L956-960, L969, L981 — deliberately, as the record of the move (*"`C1.3` en est sortie … `C1.4` à `C1.7` se renumérotent"*). No agent or command cites a `C1.n` identifier (grep of `.claude-new` for `C1\.` is empty); the Sondeur's examples use `A1.n` only (`sondeur.md` L171-175) |
| **Old wording survives** | Nowhere but the same `PROCESS_AMONT.md` L957 quotation |

Clean.

---

## B. REMOVED NAMES

### `[integrated:]`

**B-1 — `cycle.md` L54, L63, L89.** SURVIVES. The marker table
(*"`[integrated:` — `/1_structure` has run since `/2_grille`"*), the
file-state table (*"Integrated — at least one entry carries
`[integrated:`"*) and routing row 8 (*"answered, not integrated"*) all
rest on it. No agent writes it any more (`redacteur.md` grep clean; the
old *"that questions file, its entries marked"* at old L289 is gone):
`/cycle` can never observe the *Integrated* state, and integration is
now shown by the file being filed into `questions/<agent>/`
(`2_structure.md` L141). `PROCESS_AMONT.md` L278 records the removal.
`cycle.md` routing was ÉCARTÉ in the cadreur pass (C26); listed here as
the surviving occurrence it is.

### The second table of `couverture.md`

**Clean.** `architecte.md` L165-168: *"One table, and one only. A rule's
test kind — mechanical or a review — is written in the conventions file
itself … A second table would say it twice."* The old per-rule lines
(`R12 G5.1 mechanical`, old L136-144) and the *"G2.3 checkable"*
sentence are gone; `GRILLE_CONVENTIONS.md` no longer names `G2.3`
(`GRILLE_CONVENTIONS_RETIREES.md` L52 holds it as withdrawn).
`audit_conventions.md` L38, L116 reads `couverture.md` as *"which entry
each rule came from"* only. `conventions.md` L74-81 uses its presence as
the invocation test.

### Agent `extracteur`

**Clean.** No `agents/extracteur.md`, no `commands/extrait.md`, no
occurrence of `extracteur` or `/extrait` in `.claude-new/` or
`docs-new/` (case-insensitive). The `CLAUDE.md` command table L51 does
not list it. *(The orchestrator's `CLAUDE.md` of the **old** tree still
does — outside this investigation's scope.)*

### `blocked_controleur`

**Clean.** No occurrence. `controleur.md` L70 *"You never write a
blocking file"*, L83. `9_controle.md` names `blocked_<agent>-NN.md`
only as the Arbitre's files it reads at phases 5-6 (L202, L219).

### `blocked_verificateur` carrying a `## Decision`

**B-2 — `cycle.md` L88, row 7.** SURVIVES. *"A cycle agent's
`blocked_*` with `## Decision` filled → … `cadreur` or `verificateur` →
`/7_decoupe`."* The Vérificateur's file has no `## Decision`
(`verificateur.md` L185-199 *"three headings, no more … No
`## Decision`"*, L255; `7_lots.md` L97 *"it carries no `## Decision`"*;
`cadreur.md` L775). The row cannot fire, and a Product Owner reading it
would add a `## Decision` nobody reads.

**B-3 — `audit_blocages.md` L28-30.** NOTE / QUESTION. *"`code/**/blocked_*.md`
without a number — one still standing … a block waiting for a
decision."* `code/blocked_verificateur.md` is unnumbered, carries no
decision, and no command or agent renames or removes it once the
missing step has rerun (`7_lots.md` L97 stops; the Vérificateur has no
Bash; `cadreur.md` L775 only reacts to it when `code/sequence.md` is
absent). Once the split is redone the file stays on disk and every
audit lists it under *Still open*. Who removes it?

---

## C. Cross-cutting

**C-1 — `cycle.md` names none of the new files.** NOTE. Beyond B-1 and
B-2, `cycle.md` routes on the old command names (`/1_structure`,
`/2_grille`, `/3_reclasse`, `/4_convertit`, `/7_decoupe`, L82-95) and
mentions none of `par-genre/`, `questions-existant-NN.md`,
`technique-<nature>.md`, `Genre:`, `Défaut:`. Every rename in this
report is invisible to `/cycle`. Already ÉCARTÉ as C26 in the cadreur
pass; recorded so the decision is taken knowing its reach.
