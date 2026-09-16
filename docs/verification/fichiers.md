# Vérification — les fichiers de la chaîne

Census of every file `.claude-new/` produces and consumes. Built by grep
only — the two passes the brief names (168 backticked names, 202 raw
names, union deduplicated to the canonical paths below), then `grep -rn`
on each name and a read of the hit lines. `docs-new/process/` was used
for name discovery only: every name it carries is a spelling variant of
one found in `.claude-new/`, except `GRILLE_CONVENTIONS_RETIREES.md` and
`.claude/CLAUDE.md`.

Line numbers are those of `.claude-new/…`. "PO" is the Product Owner.
"inv N" is an agent's invocation number as its own file counts them.
"`/x` (cmd)" means the command itself, by script or `git mv`, no agent.

---

## A. The census — one line per file

### A1. Repository root (`docs/`, `docs/process/`)

| File | Written by | Read by | When |
|---|---|---|---|
| `docs/PRODUIT_GLOBAL.md` | `/socle` creates it (`# Application`); Fusionneur inv 2 and inv 3 | Rédacteur inv 1–2 (its `^#` index, by grep); Sondeur inv 3 (Existant); Fusionneur inv 1–3 | `/socle`; `/4_grille` second turn; `/fusion` |
| `docs/TECHNICAL_CONVENTIONS.md` | Architecte inv 1, 2, 3, 4 (architecte.md:274-277) — `/socle` says "written by hand" (socle.md:28-30, 40), see C3 | Cadreur (whole); Détailleur (whole); Concepteur, Testeur, Réalisateur, Relecteur (`permanente` rules + those the sheet names); Arbitre (whole); Diagnostiqueur inv 1; Architecte; `/audit_conventions` (whole) | `/conventions` → `/7_lots` → `/8_code`; `/diagnostique` |
| `docs/CURRENT_TECHNICAL_STATE.md` | `/socle` creates it; Réalisateur move 7, every lot; Arbitre, `## Traps` (arbitre.md:364) | Détailleur (two sections + grep); Réalisateur (two sections); Diagnostiqueur inv 1 | `/8_code`; `/diagnostique` |
| `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md` | PO, off-chain | Sondeur inv 1 and 2 (whole) | `/4_grille` |
| `docs/process/GRILLE_EXISTANT.md` | PO | Sondeur inv 3 | `/4_grille`, second turn |
| `docs/process/GRILLE_FERMETURE_TECHNIQUE.md` | PO | Convertisseur inv 1–2; Diagnostiqueur inv 2 | `/6_convertit`; `/diagnostique` |
| `docs/process/GRILLE_CONVENTIONS.md` | PO | Architecte, every invocation (architecte.md:54) | `/conventions`, requests |
| `docs/process/GRILLE_CONVENTIONS_RETIREES.md` | PO | nobody in the chain (named once, by GRILLE_CONVENTIONS.md:580) | — |
| `docs/process/PROCESS_AMONT.md`, `PROCESS_AVAL.md`, `MODELE_CIBLE_V3.md` | PO | nobody — CLAUDE.md:177 forbids it | — |
| `CALIBRATION_RISK_LEVEL.md` | nobody | nobody — eight commands say "never open it" (2_structure:38, 3a:28, 3b:27, 3_decoupe:27, 5:44, 6:29, 7:41, 8:54); absent from `docs-new/` | stale, see B3 |
| `.claude/CLAUDE.md` | PO | the orchestrator, automatically | every session |

### A2. Feature root — `docs/features/<name>/`

| File | Written by | Read by | When |
|---|---|---|---|
| `idees.md` | PO by hand; Lexicographe inv 2 (settled terms, in place) | Lexicographe inv 1, 2; Rédacteur inv 1 | `/1_lexique`; `/2_structure` |
| `lexique.md` | Lexicographe inv 1, 2, 4; Rédacteur, its `en anglais` lines only (redacteur.md:308) | Lexicographe, every invocation; Rédacteur inv 1–2; `/1_lexique` (cmd, greps `## Non tranché`) | `/1_lexique`; `/2_structure` |
| `desc-produit.md` | Rédacteur inv 1 (creates), inv 2 (integrates); Découpeur (splits in place); Qualifieur (`Genre:` line); Classeur (`Nature:` line) — each command in sequence | Sondeur inv 1–3; Convertisseur inv 2 (text outside the blocks); Architecte inv 1, 4; Contrôleur inv 1 (its group's blocks); Rédacteur inv 3; `/5_reclasse` (cmd, copies blocks); commands `/3`→`/9` by grep (`Clarification needed`, `NEW`, `^Genre:$`, `^### B`) | `/2_structure` → `/9_controle` |
| `desc-par-nature.md` | `/5_reclasse` (cmd, move 2, replaced whole); deleted by `/2_structure` on a `NEW` block (2_structure:117) | `/6_convertit` (cmd, cut into `<nature>-input.md`); `/cycle` (existence) | `/5_reclasse`; `/6_convertit` |
| `par-genre/comportements.md` | `/5_reclasse` (cmd, move 1) | `/5_reclasse` (cmd, move 2) | `/5_reclasse` |
| `par-genre/transverses.md` | `/5_reclasse` | Convertisseur inv 1 (constraint half), inv 2 | `/6_convertit` |
| `par-genre/references.md` | `/5_reclasse` | Convertisseur inv 2 | `/6_convertit` |
| `par-genre/hors-perimetre.md` | `/5_reclasse` | Convertisseur inv 2 (preamble) | `/6_convertit` |
| `par-genre/directives.md` | `/5_reclasse` | Architecte inv 1, 4 | `/conventions` |
| `par-genre/recette.md` | `/5_reclasse` | `/9_controle` (cmd, phase 4) | `/9_controle` |
| `spec-technique.md` | `/6_convertit` (cmd) assembles §1–§8 from `convertisseur/<nature>.md` and resolves single-target refs (6_convertit:197, 227); then Convertisseur inv 2 completes it; deleted by `/2_structure` on a `NEW` | Cadreur (whole); Vérificateur (preamble, cited entries, `^### §` grep); Détailleur (preamble, cited entries); Arbitre; Architecte inv 1, 4; Convertisseur inv 2; `/audit_conventions`; `/conventions` (existence); `/cycle` (`<<ASSUMED`) | `/6_convertit` → `/8_code` |
| `tracabilite.md` | Convertisseur inv 2 (convertisseur.md:672) | Architecte inv 1 (move 2), 4; `/9_controle` (phase 1); `/6_convertit` (cmd, checks against block headings) | `/conventions`; `/9_controle` |
| `tracabilite-full.md` | `/9_controle` (cmd, phase 1) | `.claude/scripts/grouper.py`; Contrôleur inv 2 (named in the prompt, 9_controle:149) | `/9_controle` |
| `desc-bug.md` (in `bugfix-NN/`) | Diagnostiqueur inv 2 | Cadreur, Vérificateur, Détailleur, Arbitre, Architecte, `/audit_conventions` — as the working folder's technical document | `/diagnostique` → `/7_lots`, `/8_code` |
| `desc-produit-fusion.md` | Rédacteur inv 3 | Fusionneur inv 1, 2 (fusionneur.md:45) | `/fusion` |
| `plan-fusion.md` | Fusionneur inv 1 | Fusionneur inv 2; `/fusion`, `/cycle` (existence) | `/fusion` |
| `rapport-fusion.md` | Fusionneur inv 2 | PO; `/fusion`, `/cycle` (existence = merge done) | `/fusion` |
| `bugfix-NN/bug-list.md` | PO by hand (diagnostique.md:111) | `/diagnostique` (cmd, count and split); Diagnostiqueur inv 2 (order); Fusionneur inv 3 | `/diagnostique`; `/fusion` |
| `bugfix-NN/investigation/<id>.md` | Diagnostiqueur inv 1 | Diagnostiqueur inv 2 | `/diagnostique` |
| `stop1.md` / `stop.md` | `/cycle` creates `stop1.md`; PO renames it `stop.md` | `/cycle` (halt); `/8_code`:148 | `/cycle` |
| `audit-blocages.md` | `/audit_blocages` (cmd, append) | `/audit_blocages` next pass; PO | by hand |
| `audit-conventions.md` | `/audit_conventions` (cmd, append) | `/audit_conventions` next pass; PO | by hand |
| `couverture.md` (working folder) | Architecte inv 1 (creates), 2, 3, 4 (updates) | Architecte inv 2–4; `/conventions` (existence is the dispatch test, conventions.md:74-81); `/audit_conventions` (38, 116, 139); PO | `/conventions` on |

### A3. Questions files — feature root, then `questions/<agent>/` once filed

| File | Written by | Read by | When |
|---|---|---|---|
| `questions-lexicographe-NN.md` | Lexicographe inv 1, 3 (always), 2, 4 (only when an answer leaves the choice open) | PO; Lexicographe inv 2, 4; `/1_lexique` (count `### Q`); `/2_structure` (stops on an empty `Answer:`) | `/1_lexique` |
| `questions-redacteur-NN.md` | Rédacteur inv 1, 2 (always) | PO; Lexicographe inv 3 → 4; Rédacteur inv 2 | `/2_structure` → `/1_lexique` → `/2_structure` |
| `questions-qualifieur-NN.md` | Qualifieur (always) | PO; Lexicographe inv 3; Rédacteur inv 2; Qualifieur next turn, from `questions/qualifieur/` (3a_genre:45) | `/3a_genre` |
| `questions-classeur-NN.md` | Classeur (always) | PO; Lexicographe inv 3; Rédacteur inv 2; Classeur next turn (3b_nature:43) | `/3b_nature` |
| `questions-sondeur-NN.md` | `/4_grille` (cmd, byte copy of `cadrage-produit/questions.md`, 4_grille:342) | PO; Lexicographe inv 3; Rédacteur inv 2; `/3_decoupe` (existence = the grid has run) | `/4_grille` |
| `questions-existant-NN.md` | Sondeur inv 3 | PO; Lexicographe inv 3; Rédacteur inv 2; `/4_grille` (existence = second turn) | `/4_grille` second turn |
| `questions-convertisseur-NN.md` | `/6_convertit` (cmd, merge of `convertisseur/questions-*.md`, 6_convertit:277) | PO; Lexicographe inv 3; Rédacteur inv 2 | `/6_convertit` |
| `questions-architecte-NN.md` | Architecte inv 1, 4 (and 2 when open) | PO; Architecte inv 2; `/conventions` (dispatch) — never through `/1_lexique` | `/conventions` |
| `questions-fusionneur-NN.md` | Fusionneur inv 1, 3 (even empty) | PO; Fusionneur inv 2; `/fusion`, `/fusion_compare` (dispatch) | `/fusion` |
| `questions/<agent>/questions-*-NN.md` | every command, by `git mv` | Qualifieur, Classeur, Lexicographe (their own last file, named in the prompt); commands, for the next `NN` | archive |

### A4. Blocking files — feature root and working folder

| File | Written by | Read by | Retired by |
|---|---|---|---|
| `blocked_lexicographe.md` | Lexicographe; `## Decision` by PO | Lexicographe (when the prompt names it) | `/1_lexique` (`git mv` → `-NN`, 1_lexique:128) |
| `blocked_redacteur.md` | Rédacteur; PO | Rédacteur | `/2_structure`:132 |
| `blocked_decoupeur.md` | Découpeur; PO | Découpeur | `/3_decoupe`:120 |
| `blocked_qualifieur.md` | Qualifieur; PO | Qualifieur | `/3a_genre`:121 |
| `blocked_classeur.md` | Classeur; PO | Classeur | `/3b_nature`:121 |
| `blocked_existant.md` | Sondeur inv 3; PO | Sondeur inv 3 | `/4_grille` (generic rule, 4_grille:328) |
| `blocked_assembleur.md` | Assembleur; PO | Assembleur | `/4_grille` (generic rule) |
| `blocked_fusionneur.md` | Fusionneur; PO | Fusionneur | Fusionneur itself (fusionneur.md:275) |
| `blocked_architecte.md` (working folder) | Architecte; PO | Architecte; `/conventions`:69, `/7_lots`:121, `/8_code`:318 (stop) | Architecte itself (architecte.md:309) |
| `bugfix-NN/blocked_diagnostiqueur.md` | Diagnostiqueur inv 2; PO | Diagnostiqueur; `/diagnostique` | Diagnostiqueur itself (diagnostiqueur.md:160) |
| `bugfix-NN/investigation/blocked_<id>.md` | Diagnostiqueur inv 1; PO | `/diagnostique` (skip rule, :48); Diagnostiqueur inv 1 | Diagnostiqueur itself |
| `blocked_*-NN.md` (settled, anywhere) | the retirers above | Arbitre ("beside it, numbered", arbitre.md:98); `/9_controle` phases 5–6; `/audit_blocages` | — |

### A5. `cadrage-produit/`

| File | Written by | Read by | When |
|---|---|---|---|
| `par-bloc.md`, `par-question.md`, `par-nature.md` | Sondeur inv 1, one each | Assembleur | `/4_grille` |
| `global.md` | Sondeur inv 2 | Assembleur | `/4_grille` |
| `releve.md` | Sondeur inv 2 (the record) | Sondeur inv 2 itself, pass B (sondeur.md:186); `/4_grille` (existence, :299) — no agent afterwards, see anomaly A2 | `/4_grille` |
| `questions.md` | Assembleur | `/4_grille` (cmd, copied to the root) | `/4_grille` |
| `blocked_par-bloc.md`, `blocked_par-question.md`, `blocked_par-nature.md`, `blocked_global.md` | the matching Sondeur; PO | that Sondeur (when named); `/4_grille` (stop at :290, rename at :331) | `/4_grille` |
| `closed/{par-bloc,par-question,par-nature,global,releve,questions}-NN.md` | `/4_grille` (`git mv`, :375) | nobody — archive | — |

### A6. `convertisseur/`

| File | Written by | Read by | When |
|---|---|---|---|
| `<nature>-input.md` | `/6_convertit` (cmd, cut from `desc-par-nature.md`, :141) | Convertisseur inv 1; `/6_convertit` (diff decides which natures run, :123) | `/6_convertit` |
| `<nature>.md` | Convertisseur inv 1 | `/6_convertit` (assembly, `<<ASSUMED` grep) | `/6_convertit` |
| `<nature>-notes.md` | Convertisseur inv 1 | Convertisseur inv 2; `/6_convertit` (`## Trace`, single-target refs, :229) | `/6_convertit` |
| `questions-<nature>.md` | Convertisseur inv 1 | `/6_convertit` (merged into `questions-convertisseur-NN.md`, then filed to `closed/`) | `/6_convertit` |
| `questions-transversal.md` | Convertisseur inv 2 | `/6_convertit` (same) | `/6_convertit` |
| `technique-<nature>.md`, `technique-transversal.md` | Convertisseur inv 1 / inv 2 (convertisseur.md:59, 294) | **nobody** — see A1 of the anomalies | — |
| `blocked_<nature>.md`, `blocked_transversal.md` | Convertisseur; PO | Convertisseur (when named); `/6_convertit` (stop :46, rerun :127, rename :297) | `/6_convertit` |
| `closed/questions-<nature>-NN.md` | `/6_convertit` (`git mv`, :77) | nobody — archive | — |

### A7. `architecte/` (working folder)

| File | Written by | Read by | When |
|---|---|---|---|
| `architecte/cadreur.md` | Cadreur (request, cadreur.md:183); Architecte inv 3 (`## Verdict`) | Cadreur next run (cadreur.md:202); `/7_lots` (dispatch, :93-94); `/audit_conventions` | `/7_lots` |
| `architecte/detailleur-<lot>[-2].md` | Détailleur (:350); Architecte inv 3 (`## Verdict`) | Architecte inv 3; `/7_lots`:105, `/8_code`:153 (glob for an empty `## Verdict`); `/audit_conventions` — the Détailleur never re-reads it, the rule reaches it through the conventions file | `/8_code` |
| `architecte/realisateur-<lot>.md` | Réalisateur (:352); Architecte inv 3 | same as above | `/8_code` |
| `architecte/arbitre-<lot>.md` | Arbitre (:382); Architecte inv 3, called by the Arbitre | Arbitre (re-reads the verdict, copies it into `## Decision`, arbitre.md:407); `/audit_conventions` | `/8_code`, mid-lot |

### A8. `code/` — the split

| File | Written by | Read by | When |
|---|---|---|---|
| `code/decoupage.md` | Cadreur (inventory then lots; corrected on defects; extended on a redécoupage) | Vérificateur (whole); Détailleur (its block's lots); Arbitre; `/7_lots` (`## lot-` count); `/9_controle` and `/audit_conventions` (`Anchor:` lines); `/6_convertit` (existence → stop) | `/7_lots` → `/9_controle` |
| `code/sequence.md` | Vérificateur, every round (even with no defect) | Cadreur (`## Defects`); Détailleur (its block); Relecteur (its block line, on a divergence only); Arbitre; `/7_lots`, `/8_code`, `/9_controle`, `/cycle` | `/7_lots` → `/9_controle` |
| `code/blocked_cadreur.md` | Cadreur; `## Decision` by PO, or the verdict of `architecte/cadreur.md` | Cadreur next run; `/7_lots` (:55-56, :93-96) | `/7_lots` (`git mv`, :96) |
| `code/blocked_verificateur.md` | Vérificateur (:167), no `## Decision` | Cadreur (:775, goes out); `/7_lots` (:97, stop) | **nobody** — see the specific checks |
| `code/redecoupage.md` | Arbitre (creates, :320); Cadreur (appends `## Ce qui revient`, `## Ce que j'en fais`, :860) | Cadreur (:823); Vérificateur (`## Ce qui est déjà codé`); Détailleur (:422-423) and Réalisateur (:277) (existence); `/7_lots`:59-67; `/8_code`:268-312 | `/8_code` → `/7_lots` |
| `code/redecoupage-NN.md` | **nobody** — see B1 | Cadreur (:827, every one); `/8_code` (:272, count → stop at the third) | — |
| `code/recette.md` | Testeur (a line per criterion no test carries, :170) | `/9_controle` (phase 4) | `/9_controle` |
| `code/recette-ordonnee.md` | `/9_controle` (cmd, :196) | PO | after `/9_controle` |
| `code/rapport-controle.md`, `-NN` | Contrôleur inv 2 (:253) | PO; `/9_controle` (phase 5, latest one) | `/9_controle` |
| `code/controle/<group>.md` | Contrôleur inv 1 | Contrôleur inv 2 | `/9_controle` |
| `code/registre-questions.md` | `/9_controle` (cmd, :209) | nobody named — the relay table says `—` (:280) | — |
| `code/decisions-produit.md` | `/9_controle` (cmd, :227, even empty) | Rédacteur inv 3, named by `/fusion` (:64) | `/fusion` |

### A9. `code/<lot>/` — one lot

| File | Written by | Read by | When |
|---|---|---|---|
| `fiche-executable.md` | Détailleur (whole block at once; rewritten on a divergence) | Concepteur, Testeur, Réalisateur, Relecteur, Contrôleur inv 1, Arbitre | `/8_code`, `/9_controle` |
| `conception.md` | Concepteur | Testeur, Réalisateur, Relecteur | `/8_code` |
| `tests.md` | Testeur | Réalisateur (`## Red`), Relecteur | `/8_code` |
| `compte-rendu.md` | Réalisateur | Relecteur; Arbitre; Détailleur (grep only, detailleur.md:607) | `/8_code` |
| `verdict.md` | Relecteur | `/8_code` (`## Status`, `## Attempts`, `## Cause`, `## Symbol divergences`); Vérificateur and Arbitre (`## Status`); Relecteur (other lots' PASS, on a divergence); `/9_controle`, `/cycle` | `/8_code` on |
| `reprise_realisateur.md` | Réalisateur, stopped mid-lot (:312) | Réalisateur next run (:441, renames `-NN`); `/8_code` (names it, :105) | `/8_code` |
| `blocked_detailleur.md` | Détailleur; `## Decision` by Arbitre (or PO, through the Arbitre's wait) | Arbitre; Détailleur (applies, renames `-NN`, :107) | `/8_code` |
| `blocked_realisateur.md` | Réalisateur; Arbitre | Arbitre; Réalisateur (applies, renames `-NN`, :148, :173) | `/8_code` |
| `blocked_concepteur.md` | Concepteur (:90); `## Decision` by PO | Concepteur when named (:118); `/8_code` (stop) | **nobody** — see C1 |
| `blocked_testeur.md` | Testeur (:95); PO | Testeur; `/8_code` (stop) | **nobody** — see C1 |
| `blocked_relecteur.md` | Relecteur (:201); PO | Relecteur (:267-276); `/8_code` (stop) | **contradictory** — see C1 |

---

## B. Anomalies

### B-A. Written, and nobody reads it

**A1. `convertisseur/technique-<nature>.md` and `technique-transversal.md`.**
The Convertisseur writes its technical questions there (convertisseur.md:59,
:294, :316-330) and says the answer "comes back to you, and to nobody
else" (:297) and "is applied when the section is written again" (:328).
Nothing carries it back:

- the Convertisseur's own reading table (:539-540) lists neither file;
- `/6_convertit` never names them — not in the rerun conditions
  (:122-127, every "Runs" row requires "its part changed", and a
  technical answer changes no block), not in the invocation prompt
  (:156-166), not in the merge into `questions-convertisseur-NN.md`
  (:277-282, natures then `questions-transversal.md` only), not in the
  filing to `closed/` (:74-78, `questions-*.md` only);
- its relay row "Technical questions only → answer them, then
  `/6_convertit`" (:334) has no source that tells the command a
  technical question was asked.

An answered technical question therefore reruns nothing, and the mark it
left, if any, stays.

**A2. `cadrage-produit/releve.md`.** Written by the global Sondeur and
read by that same invocation for pass B (sondeur.md:186), then checked
for existence by `/4_grille`:299 and archived to `closed/`. No later
agent or command opens it. It is a working document, not a defect — but
nothing downstream uses the record.

**A3. `code/registre-questions.md`.** `/9_controle` writes it (:209); its
own relay table gives its reader as `—` (:280). No agent or command reads
it. If it is for the PO, the table should say so, as it does for the two
neighbours.

**A4. `docs/process/GRILLE_CONVENTIONS_RETIREES.md`.** Named only by
`GRILLE_CONVENTIONS.md:580`; no agent reads it. PO's own document —
noted for completeness.

### B-B. Read, and nobody writes it

**B1. `code/redecoupage-NN.md`.** Read by the Cadreur ("read every
`code/redecoupage-NN.md`", cadreur.md:827) and counted by `/8_code`
(:272, "the highest number — at the third, you stop"); `/8_code`:312 and
detailleur.md:422-423 test that `code/redecoupage.md` is "gone". Nobody
renames it:

- verificateur.md:441-445 — "say in your report that it can be archived
  … you have no tool that renames a file — the command does it";
- 7_lots.md:76-78 — "the Vérificateur keeps them where they ran and
  archives the file when the sequence is written";
- 7_lots.md carries `git mv` for `blocked_cadreur.md` (:96) and the
  questions files (:175) — none for `redecoupage.md`.

Consequence: `code/redecoupage.md` never disappears. The Détailleur
stops on every run ("the split has not been redone", :422), `/8_code`
sends back to `/7_lots` for ever (:312), the third-redécoupage ceiling
(:272) never fires, and the Cadreur's "read every `-NN`" (:827) reads
nothing.

**B2. The Contrôleur's blocking file.** Never written — controleur.md:70
"You never write a blocking file", and `/9_controle` has no branch for
one. Still expected in two places of arbitre.md: :164 "When a block is
not yours — a Relecteur's, a Contrôleur's, an Architecte's" and :247 "A
Relecteur or Contrôleur block says something is missing". Harmless, but
stale.

**B3. `CALIBRATION_RISK_LEVEL.md`.** Eight commands forbid opening it
(list in A1). Nothing writes it, nothing reads it, `docs-new/` does not
hold it. A dead reference.

### B-C. Written by two hands, with no stated order

**C1. The five lot-level blocking files — who retires them.**

- `blocked_relecteur.md`: relecteur.md:203-205 "You never retire it —
  you have no tool that renames or removes a file. The orchestration
  does it, once the verdict is written" **and** relecteur.md:276 "Apply
  it, then rename it `blocked_relecteur-NN.md`, next free number" (with
  `git mv` explained at :278). The two statements sit in the same file.
  `/8_code` has no rename at all (grep `git mv|rename|numbered`: no
  hit).
- `blocked_concepteur.md`, `blocked_testeur.md`: the agent applies a
  filled `## Decision` and "carries on" (concepteur.md:118); neither
  agent nor `/8_code` renames the file. It stays at its unnumbered name
  with a filled decision. `/8_code`:48 tolerates it, but `/9_controle`
  phases 5-6 gather `blocked_<agent>-NN.md` only (:202, :219) and
  `/audit_blocages`:28 counts an unnumbered file as "still standing".
- `blocked_detailleur.md`, `blocked_realisateur.md`: retired by their
  own agent — stated, consistent (detailleur.md:107, realisateur.md:148).

**C2. `code/redecoupage.md` → `-NN`.** Two agents each say the other does
it — see B1.

**C3. `docs/TECHNICAL_CONVENTIONS.md`.** socle.md:28-30 and :40 say it is
"written by hand before `/7_lots` runs"; the Architecte writes it at
every invocation (architecte.md:274-277) and `/conventions` runs it. The
same paragraph (socle.md:26) says "the Cadreur blocks without
`CURRENT_TECHNICAL_STATE.md`" — cadreur.md never names that file; its
reading list ends "Nothing else" (:345-366). `/socle` is behind the
agents.

**C4. `docs/CURRENT_TECHNICAL_STATE.md`.** Réalisateur (move 7) and
Arbitre (`## Traps`, arbitre.md:364). No order is stated; it is safe by
construction, since the Arbitre writes while the Réalisateur or the
Détailleur waits on it and lots run one at a time. Worth one sentence in
the Réalisateur, which greps "its lot's symbols" there on a FAIL
structurel (:480) and would not know a trap line is the Arbitre's.

Files with several writers **and** a stated order, not anomalies:
`desc-produit.md` (four agents, each its own line or scope, in command
order); `lexique.md` (redacteur.md:308 restricts the Rédacteur to the
`en anglais` line); `spec-technique.md` (assembly by the command, then
Convertisseur inv 2, 6_convertit:197 then :244); `architecte/*.md`
(requester writes the request, Architecte the `## Verdict`).

---

## C. The three specific checks

**The Contrôleur's blocking file.** Nobody writes it (controleur.md:70-84
says what replaced it: a doubt in the report). Nobody in the commands
expects it. Two residual mentions in arbitre.md:164 and :247 — see B2.

**The Vérificateur's blocking file.** Still written and still expected:

- written — verificateur.md:167 "Write `code/blocked_verificateur.md`",
  with the rule that it carries no `## Decision` and is never renamed
  (:250-256);
- expected — cadreur.md:775 ("No `code/sequence.md`, and a
  `code/blocked_verificateur.md` → go out without correcting"),
  7_lots.md:97 (stop and relay), 7_lots.md:130 and arbitre.md:242
  ("what the Cadreur and the Vérificateur block on is mechanical");
- retired by nobody — the Vérificateur "never renames it" (:256), the
  Cadreur goes out, `/7_lots` stops. Once written it stays, and
  7_lots.md:97 sits in the after-run table: the next run that succeeds
  still finds it and stops.
- `docs-new/process/` never names it (0 hits for `blocked_verificateur`
  in `docs-new/`): the process documents dropped it, the agents did not.

**The second table of `couverture.md`.** No agent or command expects it.
architecte.md:146-168 defines one table, one line per entry, and forbids
a second ("One table, and one only … a second table would say it twice
and go stale"). `/audit_conventions` reads it only for "which entry each
rule came from" (:38, :116, :139) and `/conventions` only for its
existence (:74-81). The only text still describing the second table is
`docs-new/process/PROCESS_AMONT.md:767` ("Puis une seconde table, une
ligne par règle : son entrée de grille, et si son test est mécanique ou
une relecture") — the PO's document, behind the agent.

---

## D. Side notes met on the way — names, not files

- `cycle.md`:84-97 routes to `/1_structure`, `/2_grille`, `/3_reclasse`,
  `/4_convertit`, `/7_decoupe`; none exists in `.claude-new/commands/`,
  and `/1_lexique`, `/3a_genre`, `/3b_nature`, `/5_reclasse` appear
  nowhere in its table.
- CLAUDE.md's `subagent_type` row lists `verificateur`, `detailleur`,
  `realisateur`, `relecteur`, `controleur`, `arbitre` twice.
- 2_structure.md:54 "A file put away in `questions/lexicographe/` is
  read by no command" — true for that prefix; `/3a_genre`:45 and
  `/3b_nature`:43 do read `questions/qualifieur/` and
  `questions/classeur/` (the agent's own last file). Not a contradiction,
  but the sentence generalises badly.
