# App v1 — analyse

What has to change in the chain for the file contracts of
`docs/app/TECHNICAL_V1.md` §8 (questions and blocking files) and §9
(`Next:`) to hold. Read-only: nothing below has been applied.

Every reference is `path:line`. `cmd/` stands for `.claude/commands/`,
`agt/` for `.claude/agents/`, `feat/` for `docs/features/`.
« Not found » means searched and absent.

---

## A — Questions files

### Writers

| Agent or command | Writes | Proposals today | Change for §8.1 |
|---|---|---|---|
| `lexicographe` | `questions-lexicographe-NN.md` (agt/lexicographe.md:110-123) — `Terms:` · `Question:` · `Answer:` (:310-314, :524-527) | **In the prose of `Question:`** — « you propose a reading, never a term » (:318-323): the four readings (*one thing* · *two things* · *abbreviation* · *two meanings*) are stated in the question | `Options:` after `Question:` in the two templates (:310-314, :524-527), the readings as options; « Say which you read… then leave `Answer:` empty » (:347) stays |
| `redacteur` (inv. 1, 2) | `questions-redacteur-NN.md` (agt/redacteur.md:269-277) — `Block:` · `Question:` · `Answer:` (:287-290) | **None** — « the question stated directly, no preamble, no rationale » (:298) | `Options:` after `Question:` in the template (:287-290); « One entry per question, four lines, no exception » (:284) to amend |
| `qualifieur` | `questions-qualifieur-NN.md` (agt/qualifieur.md:188-198) | **In the prose of `Question:`** — template « the doubt — `comportement` or `transverse`… » (:197); and « Never suggest the answer » (:202-203) | `Options:` in the template (:195-198), one option per genre in doubt; « four lines, no exception » (:192) and « Never suggest the answer » (:202-203) to reword so that listing options is allowed |
| `classeur` | `questions-classeur-NN.md` (agt/classeur.md:140-150) | **In the prose of `Question:`** — « the two natures or the frontier in doubt » (:149); « Never suggest the answer » (:154-155) | Same as the qualifieur: template :147-150, rule :144 and :154-155 |
| `sondeur` inv. 1-2 | `cadrage-produit/<reading>.md` (agt/sondeur.md:381-387), input of the assembleur | **`Défaut:` only** — `Défaut: <the answer you propose> — <the block and the words that found it>` (:394-400); otherwise « never a suggested answer » (:453-454) | `Options:` in the template (:384-387, :396-400); `Défaut:` must become the **verbatim text of one option** — today it carries ` — <source>` (:399), which would then be copied into `Answer:` (see *Défaut*, below); :453-454 to reword |
| `sondeur` inv. 3 | `questions-existant-NN.md` (cmd/4_grille.md:388; agt/sondeur.md:266-271) | **None** — « You never propose which one wins — no *défaut* at this invocation » (agt/sondeur.md:273-276) | `Options:` holding the two sides of the arbitration (« two things are true at once and cannot both stay », :273-274), never a `Défaut:` |
| `assembleur` | `cadrage-produit/questions.md` (agt/assembleur.md:253-267) | **`Défaut:` copied** — « you never write one, never remove one » (:144-146) | Accept `Options:` in the shape it reads (:124-146) — otherwise « a file that is neither empty nor a list of questions in that shape » stops it (:173-175); `Options:` travels with its question like `Défaut:` (:148-157, :269-270); add it to the output template (:258-267) |
| `/4_grille` (command) | `questions-sondeur-NN.md` — « Copy `cadrage-produit/questions.md`… A copy, byte for byte » (cmd/4_grille.md:559-566); also writes empty `questions-sondeur-NN.md` / `questions-existant-NN.md` without an agent (:232, :351, :366) | As the assembleur's | **None** — a byte copy carries `Options:` |
| `convertisseur` | Product: `convertisseur/questions-<nature>.md`, `…-transversal.md` (agt/convertisseur.md:420-435). Technical: `convertisseur/technique-<nature>.md`, `Entries:` in place of `Block:` (:383-391) | Product: **none** (:447). Technical: **in the prose** — « `<the choice, and what each side would cost>` » (:390) | `Options:` in both templates (:388-391, :432-435); « An entry is four lines… and a fifth breaks the shape every reader after you depends on » (:496-499) to amend |
| `/6_convertit` (command) | `questions-convertisseur-NN.md` — « Every entry copied as written, renumbered from `Q1` » (cmd/6_convertit.md:343-356) | As the convertisseur's product files | **None** — « copied as written » carries `Options:` |
| `architecte` (inv. 1, 2, 4) | `questions-architecte-NN.md` (agt/architecte.md:539-547) — `Block:` · `Kind:` · `Question:` · `Answer:` | **In the prose** for `replacement` — « it asks the choice, in those terms: change the rule, or conform to it » (:563-564); otherwise « You raise, you never answer » (:536-537) | `Options:` in the template (:543-547); « five lines » (:540) to amend |
| `fusionneur` (inv. 1, 2, 3) | `questions-fusionneur-NN.md` (agt/fusionneur.md:99-117) | **None** (:125) | `Options:` in the template (:114-117); « four lines, no exception » (:111) to amend |

**11 writers** — 9 agents, 2 commands. Not found: any other agent or
command writing a `questions-*` file (`cadreur`, `detailleur`,
`diagnostiqueur`, `realisateur`, `verificateur`, `decoupeur`, `arbitre`
checked; agt/cadreur.md:294 and :454 say it opens none).

### Readers of `Answer:`

| Reader | Test | Still works with option text? |
|---|---|---|
| `/1_lexique` | « `^Answer:\s*$` with no `Défaut:` above it in the same entry » (cmd/1_lexique.md:77-83) | Yes — the test only tells empty from filled |
| `/2_structure` | Same test (cmd/2_structure.md:39-41, :199-205) | Yes |
| `/4_grille` | Same test, on « the latest questions file at the root » (cmd/4_grille.md:102-111) | Yes |
| `/6_convertit` | On `technique-*.md` only: « holds a `### Q` and no `^Answer:$` line, by grep » (cmd/6_convertit.md:149-151, :180, :393) | Yes. ⚠️ `^Answer:$` has no `\s*`: a lone trailing space reads as **answered** here and as **empty** under the three tests above |
| `/conventions` | « `Answer:` lines with nothing after them » (cmd/conventions.md:35-36, :81) | Yes |
| `/fusion` | Row 5: « A root questions file with an empty `Answer:` » (cmd/fusion.md:60) — no pattern quoted | Yes |
| `/fusion_applique` | « one grep for an empty `Answer:` » (cmd/fusion_applique.md:28, :41-42) — no pattern quoted | Yes |
| `lexicographe` inv. 2, 4 | Reads its own answers and applies them term by term (agt/lexicographe.md:365-407, :551-580) | Yes — an option names a reading; `<option> — <remark>` is read whole |
| `lexicographe` inv. 3, 4 | Sweeps **another agent's** `Answer:` fields, and the `Défaut:` of an empty one; **rewrites terms inside them** (:66-69, :430-452, :553-556) | Yes, with two side effects: the answer may stop matching its option after a swap (:449-452); and an English option text meets the `en anglais` comparison (:492-494) — see *Language* |
| `redacteur` inv. 2 | Integrates each answer by meaning; `Défaut:` taken when `Answer:` is empty, « An `Answer:` written overrides it » (agt/redacteur.md:589-623) | Yes — read by meaning; the remark after ` — ` is integrated with the rest |
| `qualifieur` | « Each answer names a block… Apply it » (agt/qualifieur.md:215-228) | Yes — an option naming one of the six genres is what it applies |
| `classeur` | Same (agt/classeur.md:162-193) | Yes — same, with the eight natures |
| `convertisseur` inv. 1 | The answered `questions-convertisseur-NN.md` the prompt names (agt/convertisseur.md:503-516); the answered `technique-<nature>.md` (:398-404) | Yes |
| `architecte` inv. 2 | « Turn each answer into a rule »; « An answer that leaves the choice open gives a new questions file » (agt/architecte.md:631-690) | Yes — a chosen option closes the choice; `coverage` accepts *voir produit* (:668-670) |
| `fusionneur` inv. 2, 3 | Each `PENDING` line resolves on « The answer says »: holds → `KEEP`, changed → `REPLACE`, no longer holds → `DELETE`; title kept / new title (agt/fusionneur.md:445-468, :616-621) | Yes — but `REPLACE` and a new title need the new words: an option alone (« the rule changed ») is « ambiguous » (:461-462) unless the remark after ` — ` carries them |

**14 readers** — 7 commands, 7 agents. `/fusion_compare` names the test
and leaves it to `/fusion` (cmd/fusion_compare.md:60-63). `/3_decoupe`,
`/3a_genre`, `/3b_nature`, `/5_reclasse`, `/7_lots` test `^### Q`
only, never `Answer:`.

### What the tables cannot hold

**Real shapes, beside the instructions.**

- `lexicographe` — feat/premiere-app-2/questions/lexicographe/questions-lexicographe-01.md:1-14: a French title and paragraph **above** `### Q1`, then `Terms:`/`Question:`/`Answer:` as instructed. feat/premiere-app-3/questions-lexicographe-01.md:1-12: a `Question:` **wrapped over seven lines**. The instructions show a multi-line `Question:` too (agt/lexicographe.md:338-341). The parser must accept prose before the first `### Q` and a `Question:` running until `Answer:`.
- `classeur` — feat/premiere-app-2/questions-classeur-01.md:1-4: the shape as instructed; the candidate natures are in the prose (« which nature should the whole block carry? »).
- `redacteur` — feat/premiere-app-2/questions/redacteur/questions-redacteur-01.md:1-5: `Answer:L'autorisation…` (no space after the colon), then a line `[integrated: B163, B164, B165]`. No `integrated:` anywhere in `.claude/` today: an older rule.
- `sondeur`/`assembleur` — feat/premiere-app/questions-sondeur-01.md:1-6: older shape — a title line, `Block: B1 — Race segment structure` (the title on the `Block:` line, which agt/sondeur.md:419-421 now forbids).
- `convertisseur` — feat/premiere-app/questions/convertisseur/questions-convertisseur-02.md:1-5: older shape, `Block:` with a title.
- **Not found** in any real file: a `Défaut:` line (`^Défaut:` returns nothing under `docs/features/`), an `Options:` line, a non-empty `questions-architecte-*`, any `questions-qualifieur-*`, `questions-fusionneur-*`, `questions-existant-*` or `technique-*`. `questions/analyste/` belongs to an agent no longer in `.claude/agents/`.

**A questions file outside the `questions-*-NN.md` name.**
`convertisseur/technique-<nature>.md` and `technique-transversal.md`
carry `### Q`/`Answer:` and are answered **in place** by the Product
Owner (cmd/6_convertit.md:347-350, :452). They never go into the
merged file. A form that globs `questions-*.md` alone misses them, and
`/6_convertit`'s « technical questions only » ending (:452) would then
have no form to point at.

**`Défaut:` against §8.1.** §8.1 wants `Défaut:` to « repeat one
option's text verbatim ». The sondeur writes
`Défaut: <the answer you propose> — <the block and the words that
found it>` (agt/sondeur.md:399), and the assembleur copies it word for
word (agt/assembleur.md:141, :266). Written « explicitly » into
`Answer:` (§8.1, last bullet), the source would travel into the answer.
Where the source goes once `Défaut:` is reduced to an option's text is
a choice the analysis cannot make. One known constraint: the
`Question:` takes « no rationale » (agt/sondeur.md:453).

**Language.** Questions are written in English, answers in French
(agt/lexicographe.md:352, agt/redacteur.md:296, agt/sondeur.md:451,
agt/qualifieur.md:202, agt/classeur.md:154, agt/convertisseur.md:445,
agt/architecte.md:553, agt/fusionneur.md:123). §8.1 writes the
option's full text into `Answer:` « so every reader keeps reading plain
French ». That holds only if options are written in French. Written in
English, they meet two readers:

- the Lexicographe, which compares answer words against `en anglais`
  lines: « an answer naming the same thing in English is the same
  pair » (agt/lexicographe.md:492-494);
- the Rédacteur, which « translates » answers (agt/redacteur.md:589-590).

The language of option text has to be decided before any template
changes.

**Multi-line answers.** Yes, they are needed. 141 real entries carry
text on lines below `Answer:`, mostly feat/premiere-app-2/questions/
lexicographe/questions-lexicographe-02…14.md, plus
questions-convertisseur-02, 03, 06 (e.g.
questions-convertisseur-02.md:17-27, five paragraphs). In all 141 the
first line after `Answer:` is non-empty. The readers above test only
the `Answer:` line, so the free-text field must **start its text on the
`Answer:` line**. Text that begins on the next line reads as empty to
`^Answer:\s*$`. No reader states a one-line limit for `Answer:` (not
found).

**§8.3 — what the application must satisfy before saving.**
`^Answer:\s*$` and `^Answer:$` both stop matching, and the text starts
on the `Answer:` line. Not found: any reader that reads `Options:`;
nothing in the chain needs it after the answer is written.

---

## B — Blocking files

| Writer | Family | Where it lives (between / during runs) | Options today | Change |
|---|---|---|---|---|
| `lexicographe` — `blocked_lexicographe.md` | One block (agt/lexicographe.md:73-81) | Main checkout, feature root / its worktree, never answered there | None | `Options:` at the end of the `To resume` body (:80) |
| `redacteur` inv. 1-2 — `blocked_redacteur.md` | One block + `## Invocation` (agt/redacteur.md:363-383) | Main checkout / worktree | None | Same, in `## To resume` (:377-379) |
| `redacteur` inv. 3 — `blocked_redacteur.md` | **Numbered**, one `## Decision` per `## Blocking N` (:390-395) | Main checkout / worktree | None | Same, in each entry's `## To resume` |
| `decoupeur` — `blocked_decoupeur.md` | One block (agt/decoupeur.md:134-150) | Main checkout / worktree | None | Same (:146-148) |
| `qualifieur` — `blocked_qualifieur.md` | **Numbered**, one `## Decision` per entry (agt/qualifieur.md:258-277, :291-293) | Main checkout / worktree | None — the decision takes « a genre among the six », « rewritten or removed », or a genre outside (:302-306) | Same, in each entry's `## To resume`: the genres read, plus the rewrite |
| `classeur` — `blocked_classeur.md` | **Numbered**, one `## Decision` per entry (agt/classeur.md:220-239, :260-262) | Main checkout / worktree | None — same three decision shapes (:270-274) | Same, the natures plus the rewrite |
| `sondeur` — `cadrage-produit/blocked_<reading>.md`, `blocked_existant.md` | One block (agt/sondeur.md:113-144) | Main checkout / worktree | None | Same (:138-140) |
| `assembleur` — `blocked_assembleur.md` | One block (agt/assembleur.md:60-83) | Main checkout / worktree | None | Same (:77-79) |
| `convertisseur` — `convertisseur/blocked_<nature>.md`, `blocked_transversal.md` | One block (agt/convertisseur.md:584-617) | Main checkout / worktree | None | Same (:611-613) |
| `architecte` — `blocked_architecte.md` | One block + `## Invocation` (agt/architecte.md:247-256) | Main checkout, working-folder root / worktree | None — a directive decision takes « reworded » or « the rule in full » (:375-381) | Same, in `## To resume` |
| `fusionneur` — `blocked_fusionneur.md` | One block + `## Invocation` (agt/fusionneur.md:223-255) | Main checkout / worktree | None | Same (:249-251) |
| `diagnostiqueur` — `investigation/blocked_<id>.md`, `blocked_diagnostiqueur.md` | One block (agt/diagnostiqueur.md:76-111) | Main checkout, bug-fix folder / worktree | None | Same (:105-107) |
| `cadreur` — `code/blocked_cadreur.md` | **One block, appended**: « append the new block below, as a fresh set of the four headings »; read on its **last** `## Decision` (agt/cadreur.md:138-143; cmd/7_lots.md:124-127) | Main checkout / worktree | None | Same, in each appended block's `## To resume` (:200-202) |
| `verificateur` — `code/blocked_verificateur.md` | **No `## Decision`** — « three headings, no more » (agt/verificateur.md:198-213) | — | — | **None** — never a form (§8.2 agrees; cmd/7_lots.md:186) |
| `detailleur` — `code/blocked_detailleur.md` | **Numbered**, `## Blocking N — lot-NN`, `###` sub-headings, **one** `## Decision` at the end holding numbered answers (agt/detailleur.md:328-353, :543-559) | Main checkout, split root / **worktree during `/8_code`**, where the Arbitre polls it (cmd/8_code.md:440-446; agt/arbitre.md:506-536) | None | `Options:` at the end of each entry's `### To resume` (:344-346, :551) |
| `realisateur` — `code/<lot>/blocked_realisateur.md` | **Numbered**, one `## Decision` at the end (agt/realisateur.md:306-325) | Main checkout / **worktree during `/8_code`**, same poll | None | Same (:313-314) |
| `concepteur` — `code/<lot>/blocked_concepteur.md` | One block (agt/concepteur.md:146-162) | Main checkout / worktree, committed by the agent (:137-141) | None | Same (:156-158) |
| `testeur` — `code/<lot>/blocked_testeur.md` | One block (agt/testeur.md:185-205) | Main checkout / worktree, committed by the agent (:142-145) | None | Same |
| `relecteur` — `code/<lot>/blocked_relecteur.md` | One block (agt/relecteur.md:277-293) | Main checkout / worktree | None | Same (:287-289) — but only one of its four cases waits on the Product Owner (below) |

**18 writers**, all agents. No command writes a `blocked_*.md`. The
Arbitre writes only inside the Détailleur's and the Réalisateur's
`## Decision` (agt/arbitre.md:133-134).

### What the table cannot hold

**Five shapes, not two.** §8.2 names « one block, a single
`## Decision` » and « numbered entries, one decision per entry ». The
chain has five:

1. One block — 11 writers.
2. One block plus `## Invocation`, which routes the file between
   commands — redacteur, architecte, fusionneur (cmd/2_structure.md:134-141,
   cmd/fusion.md:57-58, cmd/conventions.md:77-78).
3. Numbered, one `## Decision` **per entry** — qualifieur, classeur,
   redacteur inv. 3.
4. Numbered, **one** `## Decision` for all entries, answered `N.` by
   number — detailleur, realisateur (agt/arbitre.md:144-157).
5. One block **appended** several times, only the last
   `## Decision` live — cadreur.

**The Arbitre's test (B.3)** — cmd/8_code.md:328-340, reused as is:

> « A file with `## Blocking N` headings — the Détailleur's and the
> Réalisateur's, the two the Arbitre settles — is filled when every
> heading has its number: a grep of `^## Blocking ` and of the numbered
> lines under `## Decision`, never the field merely holding text. An
> entry still waiting has no number written at all »

and the row « Some numbers answered, others not — fewer numbered
answers under `## Decision` than `## Blocking N` headings »
(cmd/8_code.md:319). The entries left to the Product Owner are the
`## Blocking N` whose `N.` is absent (agt/arbitre.md:197-200: « the
absent number is the signal »).

Two exceptions:

- A `## Decision` reading `Not settled here.` (agt/arbitre.md:179-184;
  agt/realisateur.md:560) **is** numbered text, so the test reads it as
  filled. Not found: any command row that shows it to the Product Owner.
- The cadreur's conventions block lifts by the Architecte's
  `## Verdict`, not by a decision: cmd/7_lots.md:189-190 and
  agt/cadreur.md:326, :1097-1108. An empty last `## Decision` whose
  request has an empty verdict waits on the Architecte, not on her.

**Relecteur.** Three of its four cases are retired by an act, not a
decision (cmd/8_code.md:734-745). Only « Anything else » (:739) waits
on her.

**Where her decision is written (B.4)** — the exact place each test
looks:

| Shape | Where | The test that reads it |
|---|---|---|
| 1, 2 | Under the single `## Decision`, on the line after the blank line | « Grep `-A2 '^## Decision$'` — nothing under the heading is empty » (cmd/8_code.md:339-340); the same `-A2` in cmd/2_structure.md:183-185 |
| 3 | Under **each** entry's `## Decision` | `grep -A2 '^## Decision$'`, « a heading followed by nothing but a blank line and the next heading, or the end of the file, is empty » (cmd/3a_genre.md:42-47; cmd/3b_nature.md:41-46) |
| 4 | Under the single `## Decision`, as `N. <text>`, `N` matching its `## Blocking N` (agt/arbitre.md:154-161, :526-528) | The count above (cmd/8_code.md:330-335) |
| 5 | Under the **last** `## Decision` of the file | « read on its last `## Decision` » (cmd/7_lots.md:118-119, :124-127) |

What that means for §8.3:

- **Shapes 1-3 (`-A2`).** Text placed after two blank lines reads as
  empty.
- **Shape 4 (counts numbered lines).** An answer holding a line that
  opens on a number and a dot (an option phrased as a list) counts as
  an extra answer.

**During a live run (B.2).** Only shape 4 is answered in a worktree
(cmd/8_code.md:440-446: « she opens the worktree and answers there,
where the Arbitre's poll reads the blocking file »), for 20 minutes at
most (agt/arbitre.md:518-536). Every other blocking file is merged to
the main checkout before the command hands back (e.g.
cmd/1_lexique.md:253-254).

**Where `Options:` sits (recommendation).** At the end of the body of
`To resume` (`## To resume`, or `### To resume` in shape 4), never as a
new heading. `To resume` already holds « the decision or fix needed ».
A new heading would change counts the agents announce (« four
headings », « three headings, no more »), which
`.claude/scripts/coherence.py:89-104` checks against the `    ## `
lines of each template.

**The Arbitre's hand-back.** What the Product Owner has to settle on a
handed-back entry is said **in the Arbitre's report only**
(agt/arbitre.md:212-219). The file stays silent: « Anything written
under a number reads as an answer — never a note » (:215-216). The
Arbitre may touch nothing but `## Decision` (:133-134, :141-142). The
form can show the entry and its `### To resume`, nothing the Arbitre
found.

**Real files.** All 26 real blocking files sit in feat/premiere-app/
(`bugfix-06/code/lot-*/` and `code/lot-23/`). Not found: any file in
shape 3, 4 or 5 (`^## Blocking` returns nothing under `docs/features/`).
They are the older one-block shape, written **under the lot**
(`code/lot-20/blocked_detailleur.md`) where the current rule writes
`code/blocked_detailleur.md` (agt/detailleur.md:312-314). Their
decisions run 20 to 42 lines (e.g.
feat/premiere-app/bugfix-06/code/lot-24/blocked_realisateur-02.md).
feat/premiere-app/bugfix-06/code/lot-20/blocked_detailleur.md:1-4 opens
on a « SETTLED AND APPLIED » banner above the headings, written by
hand.

**A fourth place the Product Owner writes.** `## Décision du Product
Owner` in `code/redecoupage.md`, after a third return
(cmd/8_code.md:606-611, cmd/7_lots.md:348-352). TECHNICAL_V1 §2.3 lists
three places; this is not one of them.

---

## C — How each command ends

The grammar is §9's. `<name>` is the command's argument. « (not
stated) » marks an ending where the command names no next step. The
line printed is then the closest grammar form, and the gap is listed
after the table.

**Shared by the 17 commands taking an argument:** « The argument is
mandatory… Without it, ask for it and stop » (e.g. cmd/1_lexique.md:18-19)
→ `Next: stop argument missing` (not stated).

| Command | Ending | Line | Next: |
|---|---|---|---|
| `/1_lexique` | `blocked_lexicographe.md`, `## Decision` empty | :41 « Stop — say the blocking file still stands » | `Next: answer blocking` |
| | Own file alone, no `### Q` | :57 « say `/2_structure` » | `Next: run /2_structure <name>` |
| | Another agent's file alone, no `### Q` | :59 | `Next: run /2_structure <name>` |
| | Both, lexicographe's with no `### Q` | :61 | `Next: run /2_structure <name>` |
| | Two files of other agents | :63 « a filing failed; say which files » | `Next: stop filing failed` (not stated) |
| | Empty `Answer:`, no `Défaut:` | :77-78 « say which questions are waiting » | `Next: answer questions` |
| | `desc-produit.md` present at inv. 1-2 | :99 « say `/3_decoupe` » | `Next: run /3_decoupe <name>` |
| | Anything else at the root | :120-121 « stop, and say which files » | `Next: stop filing failed` (not stated) |
| | A file missing after the run | :225 « say which » | `Next: stop <file> missing` (not stated) |
| | Blocking file written | :265 « Fill its `## Decision`, then `/1_lexique` again » | `Next: answer blocking` |
| | 1 asked something | :266 | `Next: answer questions` |
| | 1 asked nothing | :267 | `Next: run /2_structure <name>` |
| | 2 wrote a new file | :268 | `Next: answer questions` |
| | 2 wrote none | :269 | `Next: run /1_lexique <name>` |
| | 3 asked something | :270 | `Next: answer questions` |
| | 3 asked nothing | :271 | `Next: run /2_structure <name>` |
| | 4 wrote a new file | :272 | `Next: answer questions` |
| | 4 wrote none | :273 | `Next: run /2_structure <name>` |
| `/2_structure` | Lexicographe's file at root holding `### Q` | :98-101 « Say `/1_lexique` comes next » | `Next: run /1_lexique <name>` |
| | `blocked_redacteur.md` says 3 | :134 « it is `/fusion`'s » | `Next: run /fusion <name>` |
| | `blocked_redacteur.md` 1-2, decision empty | :135 | `Next: answer blocking` |
| | More than one questions file | :148 « a filing failed » | `Next: stop filing failed` (not stated) |
| | A découpeur/qualifieur/classeur file with a decision empty | :150 | `Next: answer blocking` |
| | One questions file, no `### Q` | :151 | `Next: run /3_decoupe <name>` |
| | No questions file, product file there, flag hit | :153 « the file is the Product Owner's to find — never `/3_decoupe` » | `Next: manual find why a Clarification needed flag stands` |
| | Same, no flag | :153 « say `/3_decoupe` comes next » | `Next: run /3_decoupe <name>` |
| | Vocabulary not settled | :171 « say `/1_lexique` comes next » | `Next: run /1_lexique <name>` |
| | Empty `Answer:`, no `Défaut:` | :199-200 | `Next: answer questions` |
| | Refusal — `NEW` block after the split | :262-266, :389 « the file at the root is the Product Owner's to place » | `Next: manual place the answer that created <block>` |
| | `questions-redacteur-NN.md` missing | :331-332 « stops the command » | `Next: stop questions file missing` (not stated) |
| | Blocking file written | :390 « then `/2_structure` again » | `Next: answer blocking` |
| | Questions | :391 « then `/1_lexique` » | `Next: answer questions` |
| | Empty questions file | :392 | `Next: run /3_decoupe <name>` |
| `/3_decoupe` | `blocked_decoupeur.md`, decision empty | :39 | `Next: answer blocking` |
| | `blocked_decoupeur.md`, decision filled | :40 « say `/2_structure` has to run first » | `Next: run /2_structure <name>` |
| | `Clarification needed` hit | :49-50 | `Next: run /2_structure <name>` |
| | Root questions file holding `### Q` | :52-55 « Stop and say which » | `Next: stop <file> waits` (not stated) |
| | `desc-produit.md` absent | :81-82 « `/2_structure` has not run » | `Next: run /2_structure <name>` |
| | Nothing to split | :110-112 → relay « Otherwise » | `Next: run /3a_genre <name>` |
| | List still short after the second invocation | :236-238 « say which blocks were never looked at — `/3a_genre` would run on it » | `Next: stop split incomplete` (not stated) |
| | Blocking file written | :250 « then `/2_structure`… `/3_decoupe` again afterwards » | `Next: answer blocking` |
| | A block whose only trigger is a sequel | :251 « the next step does not change » | `Next: run /3a_genre <name>` |
| | Otherwise | :252 | `Next: run /3a_genre <name>` |
| `/3a_genre` | Any `## Decision` empty | :39 | `Next: answer blocking` |
| | `Clarification needed` hit | :49-52 | `Next: run /2_structure <name>` |
| | Root questions file holding `### Q` | :54-57 | `Next: stop <file> waits` (not stated) |
| | Nothing to qualify | :125-128 → :288 | `Next: run /3b_nature <name>` |
| | `questions-qualifieur-NN.md` missing | :229-230 « a defect of the run » | `Next: stop questions file missing` (not stated) |
| | Blocking file written | :282 « then `/3a_genre` again » | `Next: answer blocking` |
| | Blocking file and questions | :283 « Answer the questions first, then `/1_lexique` » | `Next: answer questions` |
| | Every decision names a rewrite | :284 « `/2_structure` » | `Next: run /2_structure <name>` |
| | A genre outside the list | :285 « Nothing runs — the tables have to carry it first » | `Next: stop genre outside the list` (who acts: not stated) |
| | Empty `Genre:` unexplained, first time | :286 « run `/3a_genre` once more » | `Next: run /3a_genre <name>` |
| | Same, second time | :286 « stops there, the blocks named » | `Next: stop <blocks> left unqualified` (not stated) |
| | Questions | :287 | `Next: answer questions` |
| | Empty, or nothing to qualify | :288 | `Next: run /3b_nature <name>` |
| `/3b_nature` | Any `## Decision` empty | :38 | `Next: answer blocking` |
| | `Clarification needed` hit | :48-51 | `Next: run /2_structure <name>` |
| | Root questions file holding `### Q` | :53-56 | `Next: stop <file> waits` (not stated) |
| | Nothing to class | :127-130 → :300 | `Next: run /4_grille <name>` |
| | `questions-classeur-NN.md` missing | :235-236 | `Next: stop questions file missing` (not stated) |
| | Blocking file written | :294 « then `/3b_nature` again » | `Next: answer blocking` |
| | Blocking file and questions | :295 | `Next: answer questions` |
| | Every decision names a rewrite | :296 | `Next: run /2_structure <name>` |
| | A nature outside the list | :297 « Nothing runs — the tables have to carry it first » | `Next: stop nature outside the list` (who acts: not stated) |
| | Empty `Nature:` unexplained, first time | :298 « run `/3b_nature` once more » | `Next: run /3b_nature <name>` |
| | Same, second time | :298 « stops there, the blocks named » | `Next: stop <blocks> left unclassed` (not stated) |
| | Questions | :299 | `Next: answer questions` |
| | Empty, or nothing to class | :300 | `Next: run /4_grille <name>` |
| `/4_grille` | A blocking file with `## Decision` empty | :61 | `Next: answer blocking` |
| | `Clarification needed` hit | :81-84 | `Next: run /2_structure <name>` |
| | A behaviour without a nature | :93-96 « `/3b_nature` has to run first » | `Next: run /3b_nature <name>` |
| | Latest root file unanswered | :102-106 | `Next: answer questions` |
| | No behaviour block | :132-134 « say the feature carries no behaviour block, and go to *What you relay* » — no relay row matches | (not stated) |
| | Sondeur's file at root holding `### Q`, no marker | :233 « `/1_lexique` and `/2_structure` have to run first » | `Next: run /1_lexique <name>` |
| | Root questions file holding `### Q` | :247-250 | `Next: stop <file> waits` (not stated) |
| | Second time already over | :350 → :628 | `Next: run /5_reclasse <name>` |
| | Second time ran once, filed | :351 → :628 | `Next: run /5_reclasse <name>` |
| | Second time, no `Global:` block | :365-367 → :628 | `Next: run /5_reclasse <name>` |
| | `blocked_existant.md` written | :398 | `Next: answer blocking` |
| | Any reading blocked | :500-503 | `Next: answer blocking` |
| | A reading missing, no blocking file | :517 « to run `/4_grille` again » | `Next: run /4_grille <name>` |
| | Assembleur reports a missing input | :544 | `Next: run /4_grille <name>` |
| | Sondeur blocked | :623 | `Next: answer blocking` |
| | Assembleur blocked | :624 | `Next: answer blocking` |
| | First time, questions | :625 « then `/1_lexique` » | `Next: answer questions` |
| | First time, empty | :626 | `Next: run /4_grille <name>` |
| | Second time, questions | :627 | `Next: answer questions` |
| | Second time, empty | :628 | `Next: run /5_reclasse <name>` |
| `/5_reclasse` | Grid not closed | :66-67 « say to run `/4_grille` » | `Next: run /4_grille <name>` |
| | `^Genre:$` non-zero | :73-75 | `Next: run /3a_genre <name>` |
| | Behaviour without a nature | :77-80 | `Next: run /3b_nature <name>` |
| | Root questions file holding `### Q` | :85-88 | `Next: stop <file> waits` (not stated) |
| | `Genre:` value outside the six | :144-145 | `Next: stop <block> genre unknown` (not stated) |
| | Genre counts differ | :147-149 | `Next: stop block lost or doubled` (not stated) |
| | `Nature:` value outside the eight | :192-193 | `Next: stop <block> nature unknown` (not stated) |
| | Nature counts differ | :195-198 | `Next: stop block lost or doubled` (not stated) |
| | Normal end | :223 | `Next: run /6_convertit <name>` |
| `/6_convertit` | `code/decoupage.md` exists | :35-38 « a change to the product now belongs to a new cycle » | `Next: stop split already cut` (how to open a cycle: not stated) |
| | `par-genre/` absent | :40-41 | `Next: run /5_reclasse <name>` |
| | `desc-par-nature.md` absent | :43-44 | `Next: run /5_reclasse <name>` |
| | Blocking file, decision empty | :54 | `Next: answer blocking` |
| | Root questions file holding `### Q` | :64-67 | `Next: stop <file> waits` (not stated) |
| | A nature's questions or notes file missing | :229-231 | `Next: stop <file> missing` (not stated) |
| | `[B<n>:` split over two lines | :283-287 | `Next: stop broken reference in <section>` (not stated) |
| | `tracabilite.md` missing, questions empty | :318 « A fault of the run » | `Next: stop fault of the run` (not stated) |
| | `<<ASSUMED` still there after the rerun | :320-323 | `Next: stop fault of the run` (not stated) |
| | `[B` left after the second invocation 2 | :327-331 | `Next: stop fault of the run` (not stated) |
| | Block identifiers ≠ `tracabilite.md` | :333-335 | `Next: stop fault of the run` (not stated) |
| | Blocking file alone | :449 | `Next: answer blocking` |
| | Blocking file and technical questions | :450 « Answer them, fill the decision, then `/6_convertit` » | `Next: answer questions` — and blocking: one line cannot say both |
| | Blocking file and product questions | :451 « Fill the decision first, answer the questions, then `/1_lexique` » | `Next: answer blocking` — then questions |
| | Technical questions only | :452 | `Next: answer questions` (the `technique-*.md` files) |
| | Product questions | :453 « then `/1_lexique` » | `Next: answer questions` |
| | A nature waiting | :454 | `Next: answer questions` |
| | Invocation 2's *No* | :455 « adds to the row above » | — no line of its own |
| | Empty, or the document stands | :456 « `/conventions`, then `/7_lots` » | `Next: run /conventions <name>` |
| `/7_lots` | No `^### §` — nothing to build | :75-85 « name no next command… then `/fusion` » | `Next: run /fusion <name>` |
| | `code/blocked_verificateur.md` | :186 « the step before it has to run again » | `Next: stop input missing` (which step: not stated) |
| | Split holds | :187 « then stop and report » | (not stated — `/8_code` appears only at :229, for the requests case) |
| | Requests settled after the split | :227-229 « `/8_code` runs against both » | `Next: run /8_code <name>` |
| | Defects left after three rounds | :188 « relay the defects » | `Next: stop defects remain` (not stated) |
| | Block standing | :191 | `Next: answer blocking` |
| | Verdict refused | :192 « the Product Owner decides » | `Next: manual decide on the refused request` (where: not stated) |
| | Architecte blocks | :244-248 « Say to run `/conventions` » | `Next: run /conventions <name>` |
| | Worktree still dirty | :316-317 « say what is left there, and stop » | `Next: stop worktree dirty` (not stated) |
| | Third redécoupage | :348-352 « her decision goes into `code/redecoupage.md`… then `/7_lots` by hand » | `Next: manual write ## Décision du Product Owner in code/redecoupage.md` |
| | An agent returns a blocking file | :354-356 | `Next: answer blocking` |
| `/8_code` | Every lot PASS at start | :85-87 « say `/9_controle` comes next » | `Next: run /9_controle <name>` |
| | `## Defects` not empty | :91-92 « Run `/7_lots` first » | `Next: run /7_lots <name>` |
| | `code/blocked_verificateur.md` | :94-99 | `Next: run /7_lots <name>` |
| | `## Attempts` reaches 3 | :282-284 « the lot is the Product Owner's » | `Next: stop <lot> failed three times` (what she does: not stated) |
| | Blocking file, decision empty | :318 | `Next: answer blocking` |
| | Some numbers answered | :319 | `Next: answer blocking` |
| | `blocked_architecte.md` of another invocation | :366-367 « say to run it » | `Next: run /conventions <name>` |
| | `stop.md` | :447-451, :825-827 « Re-running `/8_code` picks up » | `Next: run /8_code <name>` |
| | Every lot of the sequence PASS | :503-509 | `Next: run /9_controle <name>` |
| | Third redécoupage | :606-611, :831-834 | `Next: manual write ## Décision du Product Owner in code/redecoupage.md` |
| | `/7_lots` stops inside the run | :699-700 « relay what it said » | the `Next:` `/7_lots` gave |
| | `redecoupage.md` gone, blocking file open | :711-712 « say which file, and stop » | `Next: stop <file> never closed` (not stated) |
| | Relecteur: `conception.md`/`tests.md` missing | :738 « The next run's move 2 writes the file » | `Next: run /8_code <name>` |
| | Relecteur: anything else | :739 | `Next: answer blocking` |
| | `N` lots reviewed PASS | :773, :518-520 « say how many remain » | (not stated) |
| | Worktree still dirty | :803-806 | `Next: stop worktree dirty` (not stated) |
| | An agent returns a blocking file | :829 | `Next: answer blocking` |
| `/9_controle` | `desc-produit.md` absent | :74-75 | `Next: stop product file missing` (not stated) |
| | A lot without PASS | :77-78 « name it » | `Next: stop <lot> not PASS` (not stated) |
| | `tracabilite.md` absent | :121-122 « the conversion did not finish » | `Next: stop conversion unfinished` (not stated) |
| | A lot in no line of the map | :222-224 « Say which lots, and stop » | `Next: stop crossing defect` (not stated) |
| | Worktree still dirty | :461-465 | `Next: stop worktree dirty` (not stated) |
| | Normal end | :497-501 « no decision on what to do next… The Product Owner reads them and decides » | `Next: manual read the report and the manual list, then decide on a bug-list` |
| `/conventions` | `spec-technique.md` absent | :63-64 « say so » | `Next: stop technical document missing` (not stated) |
| | Blocking file, decision empty | :77 | `Next: answer blocking` |
| | `bugfix-NN` argument, nothing matched | :80 « `/8_code` carries on » | `Next: run /8_code <name>` |
| | Questions waiting | :81 | `Next: answer questions` |
| | Architecte file with no `### Q` | :85 « say `/7_lots` » | `Next: run /7_lots <name>` |
| | Conventions and `couverture.md` exist | :86 | `Next: run /7_lots <name>` |
| | Nothing of the sort | :87 | `Next: run /7_lots <name>` |
| | Root questions file holding `### Q` | :122-125 | `Next: stop <file> waits` (not stated) |
| | Raised questions | :295 « then `/conventions` » | `Next: answer questions` |
| | `conjunction` | :296 | `Next: answer questions` |
| | Product question | :297 « corrects the product file by hand » | `Next: manual correct the product file` |
| | `inconsistency` | :298 « the fix is upstream, in `/6_convertit` » | `Next: run /6_convertit <name>` |
| | `forme` | :299 « amends the grid herself » | `Next: manual amend the grid` |
| | `replacement` | :300 « answer it… then `/conventions` » | `Next: answer questions` |
| | Blocking file written | :301 | `Next: answer blocking` |
| | Asked nothing | :302 | `Next: run /7_lots <name>` |
| `/diagnostique` | No `bugfix-NN/` or no `bug-list.md` | :22-25 | `Next: stop no bug-list` (not stated) |
| | A gap opening on no `G<n>` | :42-43 « say which line lacks one » | `Next: stop gap without identifier` (not stated) |
| | Phase 1 blocking standing or new; phase 2 withheld | :97, :131-136, :221-227 | `Next: answer blocking` |
| | `desc-bug.md` exists | :139-140, :221-222 « name the next step, `/7_lots` » | `Next: run /7_lots <name>` |
| | Phase 2 blocked | :217-219 | `Next: answer blocking` |
| | Worktree still dirty | :193-197 | `Next: stop worktree dirty` (not stated) |
| | Phase 2 done | :12-13 « Then `/7_lots`, then `/8_code` » (relay :214 says nothing) | `Next: run /7_lots <name>` |
| `/fusion` | `desc-produit.md` absent | :56 | `Next: stop product file missing` (not stated) |
| | Row 2, decision empty | :57 | `Next: answer blocking` |
| | Row 4, `rapport-fusion.md` exists | :59 « the merge is done » | `Next: done` |
| | Row 5, empty `Answer:` | :60 | `Next: answer questions` |
| | Another command's blocking file | :69-73 « the command it belongs to named » | `Next: run /<that command> <name>` |
| | Root questions file holding `### Q` | :141-145 | `Next: stop <file> waits` (not stated) |
| | Any phase ended | :222-223 « the next run picks the table up again » (relay :304-305 gives no next) | `Next: run /fusion <name>` — or `answer questions` / `answer blocking` when the phase wrote one |
| `/fusion_compare` | No `desc-produit-fusion.md` | :24 | `Next: run /fusion <name>` |
| | Blocking file, decision empty | :25 | `Next: answer blocking` |
| | Blocking file filled, invocation 2 or 3 | :26 | `Next: run /fusion_applique <name>` or `Next: run /fusion <name>` |
| | `rapport-fusion.md` exists | :27 | `Next: done` |
| | `plan-fusion.md` exists | :28 | `Next: run /fusion_applique <name>` |
| | `bugfix-*/` and no fusionneur file | :29 | `Next: run /fusion <name>` |
| | Root questions file holding `### Q` | :53-57 | `Next: stop <file> waits` (not stated) |
| | Blocking file written | :204 | `Next: answer blocking` |
| | Questions | :205 « then `/fusion_applique` » | `Next: answer questions` |
| | Empty | :206 | `Next: run /fusion_applique <name>` |
| `/fusion_applique` | `rapport-fusion.md` exists | :24 | `Next: done` |
| | `plan-fusion.md` absent | :25 | `Next: run /fusion_compare <name>` |
| | Blocking file, decision empty | :26 | `Next: answer blocking` |
| | Blocking file filled, invocation 1 or 3 | :27 | `Next: run /fusion_compare <name>` or `Next: run /fusion <name>` |
| | Fusionneur questions waiting | :28 | `Next: answer questions` |
| | Blocking file written | :210 | `Next: answer blocking` |
| | Questions written | :212-213 « answered, `/fusion_applique` again » | `Next: answer questions` |
| | Report written | :207 « The agent's own report, and nothing more » | `Next: done` (not stated) |
| `/audit_blocages` | Audit appended | :9-10, :193-194 « what to do about it is the Product Owner's » | `Next: done` (not stated) |
| `/audit_conventions` | Audit appended | :9-10, :210-212 | `Next: done` (not stated) |
| `/deploie` | A device missing | :80-82 « stop and say which one » | `Next: stop <device> missing` (not stated) |
| | Report | :114-118 « the report says what failed and stops there » | `Next: done` (not stated) |
| `/socle` | `PRODUIT_GLOBAL.md` exists | :36-38 | `Next: stop global already exists` (not stated) |
| | Scaffolding committed | :40-50 « report what the Product Owner still has to provide » | `Next: done` (the first command of a feature: not stated) |

**205 endings**, plus the shared « argument missing ». Every row above
is a separate ending, counted once.

### What the table cannot hold

**The grammar loses the second step.** Every « answer » ending says
what runs after: `/1_lexique` after product answers, `/6_convertit`
after technical ones, the same command again after a decision. For
example, cmd/1_lexique.md:265, cmd/3_decoupe.md:250,
cmd/6_convertit.md:450-454. `Next: answer questions` carries none of
it. Two endings name both forms at once (cmd/6_convertit.md:450-451)
and one line can hold only one.

**Endings with no next step stated** — named, not invented:

- **Filing failed:** /1_lexique :63, :120-121; /2_structure :148.
- **Root questions file holding `### Q`, « stop and say which »**
  (whether it waits on an answer or on an integration is not said):
  /3_decoupe :52-55; /3a_genre :54-57; /3b_nature :53-56;
  /4_grille :247-250; /5_reclasse :85-88; /6_convertit :64-67;
  /conventions :122-125; /fusion :141-145; /fusion_compare :53-57.
- **A file missing after the run:** /1_lexique :225;
  /2_structure :331-332; /3a_genre :229-230; /3b_nature :235-236;
  /6_convertit :229-231.
- **Faults of the run:** /6_convertit :283-287, :318, :320-323,
  :327-331, :333-335; /5_reclasse :144-149, :192-198;
  /9_controle :222-224.
- **Repeated defect, stopped:** /3a_genre :286 (second run);
  /3b_nature :298 (second run); /3_decoupe :236-238 (short list).
- **Value outside the tables**, « the tables have to carry it first » —
  who acts is not said: /3a_genre :285; /3b_nature :297.
- **No behaviour block:** /4_grille :132-134 — no relay row matches.
- **Split already cut, « a new cycle »:** /6_convertit :35-38 — how to
  open one is not said.
- **/7_lots:**
  - `blocked_verificateur.md`, « the step before it » (:186);
  - split holds, no `/8_code` named (:187);
  - defects remain (:188);
  - verdict refused, « the Product Owner decides » (:192).
- **/8_code:**
  - three failures (:282-284);
  - `redecoupage.md` gone (:711-712);
  - `N` lots reached with lots remaining (:518-520).
- **Prerequisite missing:** /9_controle :74-78, :121-122;
  /conventions :63-64; /diagnostique :22-25, :42-43;
  /fusion :56; /socle :36-38; /deploie :80-82.
- **Worktree still dirty:** /7_lots :316-317; /8_code :803-806;
  /9_controle :461-465; /diagnostique :193-197.
- **Normal ends with no next step:** /fusion_applique :207;
  /audit_blocages; /audit_conventions; /deploie :114-118;
  /socle :40-50.
- **Relay section gives none:** /fusion :304-305, where only
  :222-223 implies a rerun; /diagnostique :214, where only :12-13
  names `/7_lots`.
- **Shared:** the missing argument, in all 17 commands that take one.

**`stop.md`.** Only `/8_code` reads it (cmd/8_code.md:435-456; grep
`stop.md` in `.claude/`: 8_code.md and socle.md only). TECHNICAL_V1
§7's « stop at the next step » has no effect on the 19 other commands.
This note proposes no change: §7 is outside §8-§9.

---

## Changes to make

**Decide first** — the templates below depend on these:

- the language of option text (see A, *Language*);
- where a `Défaut:`'s source goes once `Défaut:` is an option's text
  (see A, *Défaut*);
- whether the `Next:` grammar gains a second step (see C).

### `.claude/agents/lexicographe.md`

- :310-314 and :524-527 — add `Options:` (the readings of :321-323) between `Question:` and `Answer:`.
- :449-452 — say whether a term swap inside an `Answer:` copied from an option also applies to the `Options:` line, or leaves it.
- :76-81 — blocking file: `Options:` at the end of `To resume`.

### `.claude/agents/redacteur.md`

- :284-290 — « four lines, no exception »: allow `Options:` between `Question:` and `Answer:`.
- :617-623 — `Défaut:` reading: « holds its own answer and what founds it »; « Five lines, not four » — align with the new `Défaut:`.
- :589 — « filled the `Answer:` fields by hand, in French » — align with the language decision.
- :363-383, :390-395 — blocking file: `Options:` at the end of `## To resume`, per entry at invocation 3.

### `.claude/agents/qualifieur.md`

- :192-198 — allow `Options:` (the genres in doubt) in the template.
- :202-203 — « Never suggest the answer »: reword so that options are not a suggestion.
- :258-277 — blocking file: `Options:` per `## Blocking N`, at the end of `## To resume`.

### `.claude/agents/classeur.md`

- :144-150 — allow `Options:` (the natures in doubt) in the template.
- :154-155 — « Never suggest the answer »: same rewording.
- :220-239 — blocking file: `Options:` per `## Blocking N`, at the end of `## To resume`.

### `.claude/agents/sondeur.md`

- :384-389 — « Four lines per question »: add `Options:`.
- :394-404 — `Défaut:` reduced to the verbatim text of one option; its source moved where the decision says.
- :453-454 — « never a suggested answer »: reword for `Options:`.
- :266-276 — invocation 3: `Options:` holding the two sides, still no `Défaut:`.
- :128-144 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/assembleur.md`

- :124-146 — accept `Options:` in « the shape of a question you read ».
- :148-157 — `Options:` travels with its question, never moved between merged questions.
- :258-270 — add `Options:` to the output template, « copied, word for word ».
- :67-83 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/convertisseur.md`

- :385-391 — technical template: `Options:` (the sides of « the choice »).
- :429-435 — product template: `Options:`.
- :495-499 — « a fifth breaks the shape every reader after you depends on »: amend.
- :601-617 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/architecte.md`

- :540-547 — « five lines »: add `Options:`; for `replacement`, the two choices of :563-564.
- :250-256 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/fusionneur.md`

- :111-117 — « four lines, no exception »: add `Options:` matching the resolutions of :447-459.
- :235-255 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/decoupeur.md`

- :134-150 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/diagnostiqueur.md`

- :95-111 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/cadreur.md`

- :190-206 — blocking file: `Options:` at the end of `## To resume`, in each appended block.

### `.claude/agents/detailleur.md`

- :328-350 and :547-559 — `Options:` at the end of each entry's `### To resume`.

### `.claude/agents/realisateur.md`

- :306-321 — `Options:` at the end of each entry's `### To resume`.

### `.claude/agents/concepteur.md`

- :146-162 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/testeur.md`

- :185-205 — blocking file: `Options:` at the end of `## To resume`.

### `.claude/agents/relecteur.md`

- :277-293 — blocking file: `Options:` at the end of `## To resume` — only the case that waits on the Product Owner (cmd/8_code.md:739).

### `.claude/commands/1_lexique.md`

- :41, :57, :59, :61, :63, :77-78, :99, :120-121, :225 — each stop ends on its `Next:` line (table C).
- :263-273 — the relay table carries its `Next:` line per row.

### `.claude/commands/2_structure.md`

- :98-101, :134, :135, :148, :150, :151, :153, :171, :199-200, :262-266, :331-332 — `Next:` per stop.
- :387-392 — `Next:` per relay row.

### `.claude/commands/3_decoupe.md`

- :39, :40, :49-50, :52-55, :81-82, :110-112, :236-238 — `Next:` per stop.
- :248-252 — `Next:` per relay row.

### `.claude/commands/3a_genre.md`

- :39, :49-52, :54-57, :125-128, :229-230 — `Next:` per stop.
- :280-288 — `Next:` per relay row.

### `.claude/commands/3b_nature.md`

- :38, :48-51, :53-56, :127-130, :235-236 — `Next:` per stop.
- :292-300 — `Next:` per relay row.

### `.claude/commands/4_grille.md`

- :61, :81-84, :93-96, :102-106, :132-134, :233, :247-250, :350-351, :365-367, :398, :500-503, :517, :544 — `Next:` per stop.
- :621-628 — `Next:` per relay row.

### `.claude/commands/5_reclasse.md`

- :66-67, :73-80, :85-88, :144-149, :192-198 — `Next:` per stop.
- :223 — `Next: run /6_convertit <name>`.

### `.claude/commands/6_convertit.md`

- :35-44, :54, :64-67, :229-231, :283-287, :318-335 — `Next:` per stop.
- :447-456 — `Next:` per relay row.

### `.claude/commands/7_lots.md`

- :75-85, :184-193, :244-248, :316-317 — `Next:` per ending.
- :334-365 — `Next:` per relay case.
- :187 — name what follows a split that holds.

### `.claude/commands/8_code.md`

- :85-99, :282-284, :318-319, :366-367, :447-451, :503-509, :606-611, :699-712, :734-739, :803-806 — `Next:` per ending.
- :820-834 — `Next:` per relay case.

### `.claude/commands/9_controle.md`

- :74-78, :121-122, :222-224, :461-465 — `Next:` per stop.
- :479-501 — `Next:` on the normal end.

### `.claude/commands/conventions.md`

- :63-64, :77-87, :122-125 — `Next:` per row.
- :291-302 — `Next:` per relay row.

### `.claude/commands/diagnostique.md`

- :22-25, :42-43, :193-197 — `Next:` per stop.
- :212-242 — `Next:` per relay case, including phase 2 done (:12-13).

### `.claude/commands/fusion.md`

- :54-73, :141-145 — `Next:` per stop row.
- :302-305 — `Next:` per phase that fired.

### `.claude/commands/fusion_compare.md`

- :22-29, :53-57 — `Next:` per test.
- :202-208 — `Next:` per relay row.

### `.claude/commands/fusion_applique.md`

- :22-28 — `Next:` per test.
- :205-213 — `Next:` per relay case, including the report written.

### `.claude/commands/audit_blocages.md`

- :138-194 — `Next: done` after the audit.

### `.claude/commands/audit_conventions.md`

- :162-212 — `Next: done` after the audit.

### `.claude/commands/deploie.md`

- :80-82 and :112-118 — `Next:` on the stop and on the report.

### `.claude/commands/socle.md`

- :36-38 and :40-50 — `Next:` on the stop and on the report.
