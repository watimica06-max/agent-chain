# Scan rules — where a feature stands

Cockpit 1.3. The scan (`scan.py`) reads the files only — no Claude call, no
git command, no write — and gives every step of the chain one state:

| State | Meaning |
|---|---|
| **faite** | its output exists and nothing upstream changed it since |
| **t'attend** | an open question or blocking entry belongs to this step |
| **en cours** | a run of this command is going |
| **bloquée** | an alert stands on it (a worktree left, a file unreadable, a stop its own command names) |
| **à faire** | none of the above |
| **inconnu** | no rule of a command places it — listed below, never guessed |

Every rule below is a test the command itself makes; the page's
« Pourquoi ? » shows the rule's id, its files and these lines.
`test_scan.py` checks that each cited line still says what the rule reads
in it: a command edited without this file is a failing test, not a scan
that drifts. Paths are relative to `.claude/commands/` unless they start
with `agents/`.

---

## 1. The chains, as the commands' `Next: run` lines draw them

**Main chain** — `/1_lexique` → `/2_structure` → `/3_decoupe` →
`/3a_genre` → `/3b_nature` → `/4_grille` → `/5_reclasse` → `/6_convertit`
→ `/conventions` → `/7_lots` → `/8_code` → `/9_controle` → test on the
emulator (`/deploie`) → `/fusion`.

| Link | Where the command says it |
|---|---|
| 1_lexique → 2_structure | 1_lexique.md:272, :276, :278 |
| 2_structure → 3_decoupe | 2_structure.md:405 |
| 3_decoupe → 3a_genre | 3_decoupe.md:261 |
| 3a_genre → 3b_nature | 3a_genre.md:295 |
| 3b_nature → 4_grille | 3b_nature.md:307 |
| 4_grille → 4_grille (second time) → 5_reclasse | 4_grille.md:639, :641 |
| 5_reclasse → 6_convertit | 5_reclasse.md:227 |
| 6_convertit → conventions | 6_convertit.md:472 |
| conventions → 7_lots | conventions.md:307 |
| 7_lots → 8_code | 7_lots.md:208, :250 |
| 8_code → 8_code (lots left) → 9_controle | 8_code.md:551, :519 |
| 9_controle → *manual* | 9_controle.md:509-510 — `Next: manual lire le rapport de contrôle et la recette, décider d'une bug-list` |
| /deploie → *done* | deploie.md:68-70 |

**Where it differs from the order in the request:**
- **No command prints `Next: run /fusion` after `/9_controle` or
  `/deploie`.** /9_controle ends on a `manual` line — read, test, decide on
  a bug-list (9_controle.md:509-513); /deploie ends on `done`
  (deploie.md:68-70). /fusion is named by `Next: run` in two places only:
  `/7_lots` when the technical document holds no `### §` (7_lots.md:72-78)
  and `/2_structure` on a Rédacteur block of invocation 3
  (2_structure.md:80). 6_convertit.md:472 says `/fusion_compare`
  « branches off here whenever you choose ». **The test and /fusion are
  the Product Owner's to start**: the scan proposes the test step once a
  control is written, and /fusion is one click with a confirmation.
- **Every answer loops back to `/1_lexique`**, not to the step that asked
  (2_structure.md:404, 3a_genre.md:294, 3b_nature.md:306, 4_grille.md:638,
  :640, 6_convertit.md:469) — except technical answers (6_convertit.md:468)
  and the architecte's (conventions.md:300).
- **`/4_grille` runs twice**: a first time, then a second time against the
  global (4_grille.md:639 then :641).
- **`/conventions` is run by hand** — « no command chains it »
  (conventions.md:60-61) — though `/6_convertit` names it (6_convertit.md:472).

**Correction chain**, in a `bugfix-NN/` — `/diagnostique` → `/7_lots` →
`/8_code` → `/9_controle` (diagnostique.md:13, :228). Every command
takes the feature's name and acts on **the highest** `bugfix-NN/`
(7_lots.md:18-19, 8_code.md:25-26, 9_controle.md:20-21,
diagnostique.md:22): the cockpit launches the highest one only; an
older correction is shown read-only. No command of this chain takes
`bugfix-NN` as an argument; `/conventions` alone does
(conventions.md:26-27), and it is not a step of the chain — the flow uses
a `Next:` line's own arguments when it gives them.

---

## 2. Each command checks before it acts (§1.2)

« Before » means: before the first git action that changes the repository
(`git mv`, commit, worktree) and before any agent. ⚠️ marks a command where
a test comes **after** such an action: **the flow asks for confirmation
even when it is the step proposed** (`scan.CONFIRM`).

| Command | | Tests, then first action |
|---|---|---|
| `/1_lexique` | ✓ | Tests :36-41 (blocking), :49-63 and :77-78 (root, answers), :93-104 (product file), :121-122 (filing) — then commit :130, worktree :140. |
| `/2_structure` | ✓ | Tests :63-72 (the lexicographe's file holds `### Q`) and :74-87 (`blocked_redacteur.md`) — then `git mv` of the lexicographe's file :89-93 — **then** the root table :110-120, the vocabulary :135-139 and the answers :167-169. These three read the root *after* that filing (« the choice of invocation below reads the root after it », :89-90): they stay after it, and no line undoes the `git mv` when they stop. Commit :185 and worktree :197 come after every test. Not flagged since 1.4.3: those three stops leave only the lexicographe's empty file filed, a state the next command reads correctly. |
| `/3_decoupe` | ✓ | Tests :34-40, :47-49 (`desc-produit.md`), :51-55, :57-64 — then `git mv` :66-69, commit :123, worktree :133. « Nothing to split » :113-115 is not a stop: it commits the filing and names `/3a_genre`. |
| `/3a_genre` | ✓ | Tests :34-39, :49-53, :55-58 — then `git mv` :72-75, commit :144, worktree :150. |
| `/3b_nature` | ✓ | Tests :33-38, :48-51, :54-57 — then `git mv` :71-75, commit :146, worktree :152. |
| `/4_grille` | ✓ | Tests :40-61, :81-85, :94-98, :104-108; the `### Q` guard :253-257 — then `git mv` :266-269, commit :303, worktree :322. Note: :238 writes an empty `questions-sondeur-NN.md` at the root (no git, no agent) before the guard. |
| `/5_reclasse` | ✓ | Tests :50-90 — then `git mv` :100. No agent, no worktree; its count stops :149-152, :199-202 come after writing the views but before the commit :210. |
| `/6_convertit` | ✓ | Tests :35-60, the `### Q` guard :62-66, which natures run :85-95 and « nothing to write » :114-118 — then `git mv` :128, commit :160, worktree :170; the walk's deletions and copies :183-188 are made inside the worktree. |
| `/conventions` | ✓ | Table :76-88 walked first (its last rows invoke nothing; :86 files and commits as its outcome), guard :123-126 — then `git mv` :133, commit :158, worktree :168. |
| `/7_lots` | ✓ | Tests :58-66 (the technical document exists) and :72-78 (`^### §`) — then `git mv` :91, commit :103, worktree :109. What the Cadreur and the Vérificateur leave is read once the Cadreur hands back (:205-214), not before acting; « the command is the trigger, never the state of the folder » (:131-132). |
| `/8_code` | ✓ | Tests :74-100, `blocked_architecte.md` :102-107 and the two stop rows of 4b on the lot found :109-114 — then commit :122, worktree :128. 4b runs again on every later lot (:327-334): what it reads there, an agent of this run wrote; a stop there ends the run through « When the run ends » (:795). |
| `/9_controle` | ⚠️ | Tests :75-77, :79-81 (`tracabilite.md`), :83-87 — then commit :104, worktree :110 — **then** the map's crossing :225-228, which stays: it reads `tracabilite-full.md`, which phase 1 writes in the worktree (:192-193). Its git section runs at every end once the worktree exists, that stop included (:449-451): the run commits, merges and pushes `tracabilite-full.md`, and closes its worktree. |
| `/deploie` | ✓ | The device test :27 comes before the installs :42-46. No git, no agent. |
| `/fusion` | ✓ | Rows 1-5 :56-60 and other blocking files :68-73 first, then — a row that invokes — the `### Q` guard :112-122 — then row 6 copies `desc-produit-fusion.md` :128-129, `git mv` :157, commit :183, worktree :193. |
| `/diagnostique` | ⚠️ | Tests :21-25, :42-44, the sort of the gaps :60-73 and `desc-bug.md` :75-78 — then commit :86, worktree :96 — **then** phase 2 withheld :142-147, which stays: it reads phase 1's results. When phase 1 issues nothing (:139-140), that stop rests on the sort alone, after the commit and the worktree. Its git section runs at every end once the worktree exists, that stop included (:184-186): the worktree is closed, and the run leaves the commit of what was waiting in the folder. |

`/fusion_compare` and `/fusion_applique` belong to the `/fusion` step;
their tables (fusion_compare.md:24-29, fusion_applique.md:24-28) stop
before anything else.

---

## 3. À qui est une réponse — the step an open entry belongs to

An entry is open by the command's own test (TECHNICAL_V1 §8). It belongs
to the command named after it in « `answer …, then run X` »: that step is
« t'attend » (rule `G-ATT`).

| Rule | Entry | Step | Lines |
|---|---|---|---|
| `OWN-Q` | a root `questions-<agent>-NN.md`, any agent but architecte and fusionneur | 1_lexique | 1_lexique.md:77-78 |
| `OWN-LEX` | `blocked_lexicographe.md` | 1_lexique | 1_lexique.md:41 |
| `OWN-RED1` | `blocked_redacteur.md`, `## Invocation` 1 or 2 | 2_structure | 2_structure.md:81 |
| `OWN-RE3` | `blocked_redacteur.md`, `## Invocation` 3 | fusion | fusion.md:57 |
| `OWN-DEC` | `blocked_decoupeur.md` | 2_structure | 3_decoupe.md:39 |
| `OWN-GEN` | `blocked_qualifieur.md` | 3a_genre | 3a_genre.md:39 |
| `OWN-NAT` | `blocked_classeur.md` | 3b_nature | 3b_nature.md:38 |
| `OWN-GRI` | `cadrage-produit/blocked_*.md`, `blocked_existant.md`, `blocked_assembleur.md` | 4_grille | 4_grille.md:47-61 |
| `OWN-TEC` | `convertisseur/technique-*.md` | 6_convertit | 6_convertit.md:468 · 6_convertit.md:470 |
| `OWN-CNV` | `convertisseur/blocked_*.md` | 6_convertit | 6_convertit.md:56 |
| `OWN-ARC` | a root `questions-architecte-NN.md` | conventions | conventions.md:82 |
| `OWN-ARB` | `blocked_architecte.md`, invocation other than 3 | conventions | conventions.md:78 |
| `OWN-AR3` | `blocked_architecte.md`, invocation 3 | 8_code | 8_code.md:348-354 |
| `OWN-CAD` | `code/blocked_cadreur.md` | 7_lots | 7_lots.md:212 |
| `OWN-RED` | `code/redecoupage.md`, third return | 7_lots | 7_lots.md:379-380 |
| `OWN-COD` | `code/blocked_detailleur.md`, `code/<lot>/blocked_*.md` | 8_code | 8_code.md:354-355 · 8_code.md:773 |
| `OWN-FUS` | a root `questions-fusionneur-NN.md` | fusion | fusion.md:60 |
| `OWN-FUB` | `blocked_fusionneur.md` | fusion | fusion.md:57 |
| `OWN-DIA` | `investigation/blocked_*.md`, `blocked_diagnostiqueur.md` | diagnostique | diagnostique.md:233 · diagnostique.md:243 |
| `OWN-?` | any other | none — listed under « unknown owner » | aucune commande ne nomme ce fichier |

The form reads the feature folder and its highest `bugfix-NN/`.

---

## 4. The rules, step by step

« Turn » rules: during an upstream turn, /3_decoupe, /3a_genre and
/3b_nature say *what* they would look at, not whether they already ran —
markers stay until the grid strips them. Each of them files every root
questions file before its agent writes (3_decoupe.md:66-69,
3a_genre.md:72-75, 3b_nature.md:71-75, 4_grille.md:266-269), and the
Rédacteur, the qualifieur and the classeur write one on every run, empty
or not (agents/redacteur.md:275, agents/qualifieur.md:3,
agents/classeur.md:3). **The one file left at the root therefore says
where the turn stands**: a file of the step's own agent or of a later one
— it ran; an earlier one — it has not; none — /3_decoupe filed the
Rédacteur's.

| Rule | Step | State | Test | Lines |
|---|---|---|---|---|
| `G-ATT` | any | t'attend | an open entry belongs to the step (§3) | « À qui est une réponse » : la commande nommée après « answer …, then run » |
| `G-AMONT` | 1_lexique → 6_convertit | faite | `code/decoupage.md` exists: a change to the product belongs to a new cycle | 6_convertit.md:35-38 · 2_structure.md:248-255 |
| `G-AVAL` | any | à faire | its output exists, but a step before it is not done — not applied past the split to steps `G-AMONT` closed | §1.3 de la demande : « nothing upstream changed it since » |
| `G-BUGFIX` | main 7_lots, 8_code, 9_controle | faite | a `bugfix-NN/` exists: these commands now act on it, and a bug-list follows a control | 7_lots.md:18-19 · 8_code.md:25-26 · 9_controle.md:20-21 · 9_controle.md:512-513 |
| `G-WT` | first step not done | bloquée | `.claude/worktrees/<feature>/` exists and no run goes: the command would fail to create it | 1_lexique.md:138-140 — git worktree add .claude/worktrees/<name>, dans chaque commande à agent |
| `G-ERR` | the file's step | bloquée | a file the form cannot read | TECHNICAL_V1 §8.1 : un fichier illisible est une erreur, jamais un fichier sans question |
| `G-RUN` | the run's step | en cours | the cockpit's run of this command goes | le run en cours du cockpit |
| `G-HEAD` | — | (§2) | `HEAD` moved since the relay, not by a cockpit run | §2 : HEAD a bougé depuis le relais, hors run du cockpit |
| `X-FAITE` | — | (§2) | the stored `Next: run X`, and X is faite | §2 : la sortie de X existe |
| `X-BLOQUEE` | — | (§2) | the stored `Next: run X`, and X is bloquée | §2 : X est bloquée |
| `X-AMONT` | — | (§2) | the stored `Next: run X`, and a step before X t'attend | §2 : une étape avant X t'attend |
| `OWN-Q` | 1_lexique | t'attend | see §3 | 1_lexique.md:77-78 |
| `OWN-LEX` | 1_lexique | t'attend | see §3 | 1_lexique.md:41 |
| `OWN-RED1` | 2_structure | t'attend | see §3 | 2_structure.md:81 |
| `OWN-RE3` | fusion | t'attend | see §3 | fusion.md:57 |
| `OWN-DEC` | 2_structure | t'attend | see §3 | 3_decoupe.md:39 |
| `OWN-GEN` | 3a_genre | t'attend | see §3 | 3a_genre.md:39 |
| `OWN-NAT` | 3b_nature | t'attend | see §3 | 3b_nature.md:38 |
| `OWN-GRI` | 4_grille | t'attend | see §3 | 4_grille.md:47-61 |
| `OWN-TEC` | 6_convertit | t'attend | see §3 | 6_convertit.md:468 · 6_convertit.md:470 |
| `OWN-CNV` | 6_convertit | t'attend | see §3 | 6_convertit.md:56 |
| `OWN-ARC` | conventions | t'attend | see §3 | conventions.md:82 |
| `OWN-ARB` | conventions | t'attend | see §3 | conventions.md:78 |
| `OWN-AR3` | 8_code | t'attend | see §3 | 8_code.md:348-354 |
| `OWN-CAD` | 7_lots | t'attend | see §3 | 7_lots.md:212 |
| `OWN-RED` | 7_lots | t'attend | see §3 | 7_lots.md:379-380 |
| `OWN-COD` | 8_code | t'attend | see §3 | 8_code.md:354-355 · 8_code.md:773 |
| `OWN-FUS` | fusion | t'attend | see §3 | fusion.md:60 |
| `OWN-FUB` | fusion | t'attend | see §3 | fusion.md:57 |
| `OWN-DIA` | diagnostique | t'attend | see §3 | diagnostique.md:233 · diagnostique.md:243 |
| `OWN-?` | — | — | an open entry no command names | aucune commande ne nomme ce fichier |
| `LEX-1` | 1_lexique | faite | `desc-produit.md` exists and no other agent's file waits at the root: invocations 1 and 2 stop | 1_lexique.md:93-104 |
| `LEX-2` | 1_lexique | à faire | no questions file at the root, no product file: invocation 1 | 1_lexique.md:56 |
| `LEX-3` | 1_lexique | faite | the lexicographe's file alone, no `### Q`: the loop ended | 1_lexique.md:57 |
| `LEX-4` | 1_lexique | à faire | the lexicographe's file alone, answered: invocation 2 | 1_lexique.md:58 |
| `LEX-5` | 1_lexique | à faire | another agent's answered file alone: invocation 3 | 1_lexique.md:60 |
| `LEX-6` | 1_lexique | bloquée | two files of other agents at the root: a filing failed | 1_lexique.md:63 · 1_lexique.md:121-122 |
| `LEX-7` | 1_lexique | faite | another agent's file alone, no `### Q` | 1_lexique.md:59 |
| `LEX-8` | 1_lexique | faite | another agent's, and the lexicographe's with no `### Q` | 1_lexique.md:61 |
| `LEX-9` | 1_lexique | à faire | another agent's, and the lexicographe's with questions: invocation 4 | 1_lexique.md:62 |
| `STR-1` | 2_structure | à faire | the lexicographe's root file holds `### Q`: it stops, /1_lexique first | 2_structure.md:63-72 |
| `STR-2` | 2_structure | à faire | `blocked_redacteur.md` (1 or 2), decision filled | 2_structure.md:82 |
| `STR-3` | 2_structure | bloquée | more than one questions file: a filing failed | 2_structure.md:115 |
| `STR-4` | 2_structure | à faire | one questions file holding `### Q`: invocation 2 | 2_structure.md:114 |
| `STR-5` | 2_structure | à faire | a découpeur, qualifieur or classeur blocking file, every decision filled | 2_structure.md:116 |
| `STR-6` | 2_structure | faite | one questions file, no `### Q`: nothing to integrate | 2_structure.md:118 |
| `STR-7` | 2_structure | à faire | no questions file, no product file: invocation 1 | 2_structure.md:119 |
| `STR-8` | 2_structure | bloquée | no questions file, the product file flags `Clarification needed` | 2_structure.md:120 |
| `STR-9` | 2_structure | faite | no questions file, the product file there, no flag | 2_structure.md:120 |
| `DEC-0` | 3_decoupe | à faire | `blocked_decoupeur.md` stands: /2_structure first | 3_decoupe.md:39-40 |
| `DEC-1` | 3_decoupe | à faire | `Clarification needed`: /2_structure first | 3_decoupe.md:51-55 |
| `DEC-2` | 3_decoupe | à faire | a root file (not architecte) holds `### Q`: it would stop | 3_decoupe.md:57-61 |
| `DEC-3` | 3_decoupe | à faire | no `desc-produit.md` | 3_decoupe.md:47-49 |
| `DEC-4` | 3_decoupe | faite | the grid ran once and no heading carries `NEW` or `MODIFIED`: invoke nothing | 3_decoupe.md:87-90 · 3_decoupe.md:113-115 |
| `DEC-5` | 3_decoupe | faite | turn: a later agent's file is at the root | 3_decoupe.md:66-69 · 3a_genre.md:72-75 · 3b_nature.md:71-75 · 4_grille.md:266-269 |
| `DEC-6` | 3_decoupe | à faire | turn: the lexicographe's or the Rédacteur's file is at the root, still to file | 3_decoupe.md:66-69 |
| `DEC-7` | 3_decoupe | faite | turn: the root is empty — it filed the Rédacteur's | 3_decoupe.md:66-69 · agents/redacteur.md:275 |
| `DEC-9` | 3_decoupe | inconnu | turn: the root holds an agent's file out of the turn | aucune règle : le fichier d'un agent hors du tour |
| `GEN-1` | 3a_genre | à faire | `Clarification needed` | 3a_genre.md:49-53 |
| `GEN-2` | 3a_genre | à faire | a root file holds `### Q` | 3a_genre.md:55-58 |
| `GEN-3` | 3a_genre | à faire | no `desc-produit.md` | 3a_genre.md:109-115 · 2_structure.md:119 |
| `GEN-4` | 3a_genre | faite | no empty `Genre:`, no `MODIFIED`, no answered file filed, no blocking file: do not invoke | 3a_genre.md:127-130 |
| `GEN-5` | 3a_genre | faite | turn: its own file, or a later one, at the root | 3b_nature.md:71-75 · 4_grille.md:266-269 · agents/qualifieur.md:3 |
| `GEN-6` | 3a_genre | à faire | turn: an earlier file at the root | 3_decoupe.md:66-69 |
| `GEN-7` | 3a_genre | à faire | turn: the root is empty — /3_decoupe ran, not it | 3_decoupe.md:66-69 |
| `GEN-8` | 3a_genre | à faire | a block with an empty `Genre:` | 3a_genre.md:114 |
| `GEN-9` | 3a_genre | inconnu | turn: an agent's file out of the turn | aucune règle : le fichier d'un agent hors du tour |
| `GEN-10` | 3a_genre | à faire | the answered file filed under `questions/qualifieur/`, or a filled blocking file, waits for it | 3a_genre.md:117-120 · 3a_genre.md:40 |
| `NAT-1` | 3b_nature | à faire | `Clarification needed` | 3b_nature.md:48-51 |
| `NAT-2` | 3b_nature | à faire | a root file holds `### Q` | 3b_nature.md:54-57 |
| `NAT-3` | 3b_nature | à faire | no `desc-produit.md` | 3b_nature.md:113 · 2_structure.md:119 |
| `NAT-4` | 3b_nature | faite | every behaviour has its nature, none stale, no `MODIFIED`, nothing to apply: do not invoke | 3b_nature.md:129-130 |
| `NAT-5` | 3b_nature | faite | turn: its own file, or a later one, at the root | 4_grille.md:266-269 · agents/classeur.md:3 |
| `NAT-6` | 3b_nature | à faire | turn: an earlier file (lexicographe, Rédacteur, qualifieur) at the root | 3a_genre.md:72-75 |
| `NAT-7` | 3b_nature | à faire | turn: the root is empty | 3_decoupe.md:66-69 |
| `NAT-8` | 3b_nature | à faire | a behaviour without a nature, or a stale nature | 3b_nature.md:113-115 |
| `NAT-9` | 3b_nature | inconnu | turn: an agent's file out of the turn | aucune règle : le fichier d'un agent hors du tour |
| `NAT-10` | 3b_nature | à faire | the answered file filed under `questions/classeur/`, or a filled blocking file | 3b_nature.md:118 · 3b_nature.md:38-40 |
| `GRI-0` | 4_grille | à faire | no `desc-produit.md`: no block to probe yet | 4_grille.md:126-132 · 2_structure.md:119 |
| `GRI-1` | 4_grille | à faire | `Clarification needed` | 4_grille.md:81-85 |
| `GRI-2` | 4_grille | à faire | a behaviour without a nature: /3b_nature first | 4_grille.md:94-98 |
| `GRI-4` | 4_grille | faite | the grid closed: highest sondeur and existant files present, no `### Q`, no marker | 5_reclasse.md:50-68 · 4_grille.md:356-357 |
| `GRI-5` | 4_grille | bloquée | no behaviour block, and the grid never ran: `stop no behaviour block` | 4_grille.md:134-140 |
| `GRI-6` | 4_grille | à faire | the grid is not closed | 4_grille.md:193-201 |
| `REC-1` | 5_reclasse | à faire | the grid is not closed | 5_reclasse.md:50-68 |
| `REC-2` | 5_reclasse | à faire | an empty `Genre:` | 5_reclasse.md:74-76 |
| `REC-3` | 5_reclasse | à faire | a behaviour without a nature | 5_reclasse.md:78-81 |
| `REC-4` | 5_reclasse | à faire | a root file holds `### Q` | 5_reclasse.md:86-90 |
| `REC-5` | 5_reclasse | à faire | the six `par-genre/` files or `desc-par-nature.md` missing | 6_convertit.md:41-46 |
| `REC-6` | 5_reclasse | à faire | the views no longer copy every block of `desc-produit.md` as it stands | 5_reclasse.md:136-139 · 5_reclasse.md:149-152 |
| `REC-7` | 5_reclasse | faite | the six views copy every block, and `desc-par-nature.md` is there | 5_reclasse.md:119-139 · 5_reclasse.md:158 |
| `CNV-2` | 6_convertit | à faire | `par-genre/` or `desc-par-nature.md` missing | 6_convertit.md:41-46 |
| `CNV-3` | 6_convertit | à faire | a root file holds `### Q` | 6_convertit.md:62-66 |
| `CNV-4` | 6_convertit | à faire | a nature runs: its part differs from `<nature>-input.md`, its technical file is answered, its section is missing or `<<ASSUMED` with nothing waiting, its blocking file is filled, or its files stand with no block | 6_convertit.md:85-95 |
| `CNV-5` | 6_convertit | faite | no nature runs, and the document stands: `# Preamble`, no `<<ASSUMED`, no `[B`, `tracabilite.md`, nothing waiting | 6_convertit.md:114-118 |
| `CNV-6` | 6_convertit | à faire | no nature runs, the document does not stand: the assembly again | 6_convertit.md:119 |
| `CON-1` | conventions | à faire | no `spec-technique.md` | conventions.md:63-64 |
| `CON-2` | conventions | à faire | `blocked_architecte.md`, decision filled | conventions.md:79 |
| `CON-3` | conventions | à faire | a request in `architecte/` with no verdict: invocation 3 | conventions.md:80 |
| `CON-4` | conventions | à faire | an answered `questions-architecte-NN.md`: invocation 2 | conventions.md:83 |
| `CON-5` | conventions | à faire | no `docs/TECHNICAL_CONVENTIONS.md`: invocation 1 | conventions.md:84 |
| `CON-6` | conventions | à faire | no `couverture.md`: invocation 4 | conventions.md:85 |
| `CON-7` | conventions | faite | conventions and `couverture.md` there: nothing to do | conventions.md:86-88 |
| `LOT-1` | 7_lots | à faire | no technical document (`spec-technique.md`, or `desc-bug.md` in a correction): it stops | 7_lots.md:22-23 · 7_lots.md:58-66 |
| `LOT-2` | 7_lots | faite | no `^### §`: nothing to build, /fusion next | 7_lots.md:72-78 |
| `LOT-3` | 7_lots | bloquée | `code/blocked_verificateur.md`: the step before has to run again | 7_lots.md:207 |
| `LOT-4` | 7_lots | à faire | `code/redecoupage.md`: coding sent the split back | 7_lots.md:143 |
| `LOT-5` | 7_lots | à faire | `code/blocked_cadreur.md`, last decision filled | 7_lots.md:140 |
| `LOT-6` | 7_lots | à faire | the split holds, a request waits on its verdict | 7_lots.md:241-250 |
| `LOT-7` | 7_lots | faite | `code/sequence.md`, `## Defects` carries no line | 7_lots.md:208 |
| `LOT-8` | 7_lots | à faire | `## Defects` carries lines | 8_code.md:92-93 · 7_lots.md:142 |
| `LOT-9` | 7_lots | à faire | no split yet | 7_lots.md:141 |
| `COD-1` | 8_code | à faire | no `code/sequence.md` | 8_code.md:80-83 |
| `COD-2` | 8_code | à faire | defects, or `blocked_verificateur.md`: /7_lots first | 8_code.md:92-100 |
| `COD-3` | 8_code | bloquée | a lot not PASS with `## Attempts` at 3 | 8_code.md:318-320 |
| `COD-5` | 8_code | faite | every lot of `## Order` has a verdict opening on `PASS` | 8_code.md:85-87 |
| `COD-6` | 8_code | à faire | « n / N lots en PASS », N > n | 8_code.md:80-83 |
| `CTL-1` | 9_controle | à faire | no `desc-produit.md` | 9_controle.md:75-77 |
| `CTL-3` | 9_controle | faite | the four files of a run: `code/rapport-controle*.md` (feature), `code/recette-ordonnee.md` and `code/decisions-produit.md` (working folder), `registre-questions.md` (feature) | 9_controle.md:488-495 · 9_controle.md:509-510 |
| `CTL-4` | 9_controle | à faire | the four files are not all there | 9_controle.md:488-495 |
| `TST-1` | test | faite | `rapport-fusion.md` exists | fusion.md:59 |
| `TST-2` | test | à faire | the highest correction is controlled: test, then decide | 9_controle.md:509-513 |
| `TST-3` | test | faite | a correction is open: the bug-list is what follows the test | 9_controle.md:512-513 |
| `TST-4` | test | à faire | after the control: test, then decide | 9_controle.md:509-513 |
| `FUS-1` | fusion | à faire | no `desc-produit.md` | fusion.md:56 |
| `FUS-2` | fusion | faite | `rapport-fusion.md` exists: the merge is done | fusion.md:59 |
| `FUS-3` | fusion | à faire | no `rapport-fusion.md` | fusion.md:61-66 |
| `DIA-1` | diagnostique | à faire | `bug-list.md` absent or empty: hers to write first | diagnostique.md:21-25 |
| `DIA-2` | diagnostique | faite | `desc-bug.md` exists | diagnostique.md:75-77 · diagnostique.md:228 |
| `DIA-3` | diagnostique | à faire | `bug-list.md` written, no `desc-bug.md` | diagnostique.md:60-67 |

---

## 5. The proposed step (§1.4)

The first step of the chain, in order, that is not « faite ». It is
proposed — one click, « déduite du dossier » — when it is « t'attend » or
« à faire »; **a « bloquée » or « inconnu » step is shown and never stepped
over**. While the highest `bugfix-NN/` has a step not done, the dashboard
proposes the correction chain: the commands act on it.

---

## 6. What the scan cannot derive from a command's own test

- **`inconnu`: /3_decoupe, /3a_genre, /3b_nature** (`DEC-9`, `GEN-9`,
  `NAT-9`) when the root holds a file of an agent outside the upstream
  turn (`convertisseur`, `architecte`…) beside markers or before the grid:
  nothing says whether the step ran.
- **The test on the emulator** has no file of its own. It is read from
  what follows it — a `bugfix-NN/` (`TST-3`), `rapport-fusion.md`
  (`TST-1`) — and is otherwise « à faire » once a control is written,
  the way /9_controle's `manual` line says it.
- **/3_decoupe, /3a_genre, /3b_nature's « already ran this turn »**: their
  tests say what they would look at, not whether they ran. Read from the
  root file (« turn » rules), not from a test of their own.
- **/9_controle's « done »**: the command has no such test — « an existing
  `rapport-controle.md` is not a reason to stop » (9_controle.md:92). Read
  as « its four files are there » (9_controle.md:488-495).
- **/5_reclasse's « nothing changed since »**: no test in the command;
  read by comparing each block of the views with `desc-produit.md`, the
  copy the command says it makes (5_reclasse.md:136-139).
- **/6_convertit's byte comparison** (6_convertit.md:106): compared with
  line ends and trailing spaces ignored — how the part was copied is not
  written.
- **A filled `blocked_qualifieur.md` / `blocked_classeur.md`**: /2_structure
  takes any of them (2_structure.md:116) and /3a_genre, /3b_nature name
  them too (3a_genre.md:40, 3b_nature.md:39-40); which one applies depends
  on what the decision says (3a_genre.md:289-291). The scan follows the
  chain order and proposes /2_structure; a stored `Next:` naming the other
  is not contradicted by it.
