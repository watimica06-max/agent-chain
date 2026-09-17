# Plan — sondeur

Base: `.claude-new/agents/sondeur.md` and the five commands naming it
(`4_grille.md`, `3_decoupe.md`, `3b_nature.md`, `5_reclasse.md`,
`cycle.md`), read at the worktree's `HEAD`. Line numbers are those
files' as read today.

`cycle.md` L88 and L93 name the sondeur — moot: `decisions.md`
(`cadreur.md` F23) deletes the file. Neither `sondeur.md` nor
`4_grille.md` mentions `/cycle`; nothing to strike on this side.

---

## sondeur.md — the report's own findings

### sondeur.md F01 — C10 listed deferred, already applied

Verdict: confirmed
Cited: modifications.md L454 — « **C10** | L'ordre des sections de la
commande | ⚠️ **Reporté au `todo.md`**, avec les neuf commandes » ·
4_grille.md L179 `## Git, before invoking`, L299 `## The four
invocations`, L461 `## Git, once it has reported` · renommages.md L22 —
« `## Git, before invoking` / `## Git, once it has reported` in every
agent-invoking command » (sound). No `todo.md` exists in the tree.
Decision: Record C10 as applied in `modifications.md` (L448 « Reportés
(1) » and the L454 row); no agent or command file changes.
Where: modifications.md L448-454 ↔ 4_grille.md L179/L299/L461
Owner: the refonte record (`docs/refonte/modifications.md`) — no agent
Also in: —

### sondeur.md F02 — §3's « motif déjà suivi » ground dropped, listed passed

Verdict: confirmed — the cited lines are off: §3's table sits at
modifications.md L387-398, the row at L395.
Cited: modifications.md L395 — « Il n'y répond pas ici, mais une règle
transverse ou un motif déjà suivi donne la réponse | Une question
**défaut** » · sondeur.md L398-400 — « A transverse rule is the only
ground. Never *the other blocks do it this way* — a pass A question
stands on its block alone, and closing it because others settle it is
pass B's. »
Decision: — (see `## To settle`, item 1: same question as F09)
Where: modifications.md L395 ↔ sondeur.md L398-400
Owner: sondeur (if the agent side moves) · the grid (if the grid side
moves)
Also in: —

### sondeur.md F03 — the global locates N blocks by N greps

Verdict: confirmed
Cited: passes/sondeur.md L510-512 — « The global invocation and a
first-turn angle read the file whole; a later-turn angle reads the
blocks the prompt names » · sondeur.md L43 — « always a list, never
the file whole » · sondeur.md L180-182 — « even when it says *every
behaviour block*, it lists them » · 4_grille.md L368 — « every
behaviour block: <list> ».
Decision: Change nothing — keep the list rule at every invocation; the
agent and the command agree, the list arrives in file order (the
`grep -B1` of 4_grille.md L107 returns it), and the previous round
recorded A-C22 as fixed on exactly this form. The pass file is a
record, not a target.
Where: passes/sondeur.md L510-512 ↔ sondeur.md L43
Owner: sondeur — no line changes
Also in: —

### sondeur.md F04 — « two lists » heading a three-row table

Verdict: confirmed
Cited: sondeur.md L48 — « The prompt names two lists of blocks » ·
L51-55 — three rows, the third « At the global invocation only » ·
4_grille.md L272-282 — invocation 3's prompt carries neither a
transverse nor an out-of-scope list; L369-370 — the global's carries
both; L318/L334/L350 — the angles' carry the transverse list only.
Decision: Drop the count and say, row by row, which invocations receive
each list (transverse: 1 and 2 · out-of-scope: 2 only · invocation 3:
the blocks with the global section each names).
Where: sondeur.md L48 ↔ sondeur.md L51-55
Owner: sondeur
Also in: — (4_grille.md already matches; no change)

### sondeur.md F05 — « the blocking file the prompt names you » at a fresh invocation 1

Verdict: confirmed
Cited: sondeur.md L111 — « Write the blocking file the prompt names
you » · L119-121 — « At invocations 1 and 2 it is
`<out>/blocked_<your name>.md` » · 4_grille.md L321-322 — the angle's
prompt names only `Write to …/cadrage-produit/par-bloc.md` and, when a
decision is filled, `<Plus: …/blocked_par-bloc.md …>`; L47-50 — the
command's table expects `cadrage-produit/blocked_par-bloc.md` etc.
Decision: State the target once, before the imperative — at
invocations 1 and 2 the name is derived from the output path
(`<out>/blocked_<your name>.md`), at invocation 3 the prompt gives
it — so that L111 never points at a name the prompt did not write.
Where: sondeur.md L111 ↔ sondeur.md L119-123
Owner: sondeur
Also in: — (4_grille.md's five names and the invocation-3 prompt
already resolve; no change)

### sondeur.md F06 — a feature block contradicting an out-of-scope block has no pass and no `Block:` shape

Verdict: confirmed
Cited: sondeur.md L346-348 — « A block of the feature that does what
one of them excludes is not your business — it is a contradiction of
the product, and it goes to the Product Owner as an obligatory question
naming both » · L421-422 — « One identifier for a pass A gap — always
one » · L424-425 — « Several for a pass B crossing » · L430-431 —
« `Block: -` for a pass C question » · L55 — out-of-scope blocks « At
the global invocation only » · 4_grille.md L152-153 — « their
identifiers go in the global invocation's prompt only ». The analogue
already in the file: invocation 3, sondeur.md L265-268 — « its `Block:`
line names the feature's block — never a block of the global » and
L275 — « Say which section of the global the question stands against,
in the question's own words ».
Decision: Give the case a home — the global invocation raises it as an
obligatory question whose `Block:` line carries the feature block
alone and whose text names the out-of-scope block, on the invocation-3
model; add that case to *The `Block:` line*; strike « not your
business ».
Where: sondeur.md L346-348 ↔ sondeur.md L409-435
Owner: sondeur
Also in: — (one identifier of the feature is the shape every reader
of `Block:` already accepts; no change on the assembleur or the
redacteur)

### sondeur.md F07 — stop 1 phrased on « the file »

Verdict: confirmed
Cited: sondeur.md L81-82 — « A read that returned less than the file
holds » · L43 — « always a list, never the file whole » · L69 — « read
from there to the next heading » · passes/sondeur.md L513-514 — « The
"empty or short" stop (comment 4) applies to what was read. »
Decision: Restate stop 1 on what was asked for — the heading to the
next heading, or the global section at invocation 3 — with the three
observables (truncation signalled, text ending mid-block, heading with
no body) as the test; drop « the file holds ».
Where: sondeur.md L81-86 ↔ sondeur.md L43/L69
Owner: sondeur
Also in: —

### sondeur.md F08 — an accepted *défaut* stops the next grid turn

Verdict: confirmed — BLOCKING holds: the loop cannot close on a turn
that produced one accepted *défaut*.
Cited: sondeur.md L402-403 — « `Answer:` stays empty, as always. Empty
means the Product Owner accepts the proposal — written, it replaces
it. » · 4_grille.md L97-100 — « The latest questions file at the root
is answered and integrated. A `grep '^Answer:$'` on it — one hit and
you stop » · 4_grille.md L444-447 — the merged file is copied to the
root as `questions-sondeur-NN.md`, so the *défaut* entries are in the
file the test reads. The `Défaut:` shape itself is settled (report
Part 2, A-§3 (a)) and not reopened here.
Decision: Exempt an entry carrying a `Défaut:` line from the
`^Answer:$` stop in `/4_grille`, the way the finding says `/1_lexique`
and `/2_structure` do (their lines are outside this plan's reading
list and were not opened).
Where: sondeur.md L402-403 ↔ 4_grille.md L97-100
Owner: `4_grille.md` — the commands' corrector. Sondeur: no line
changes (the field's meaning stays as L402-403 says).
Also in: — ⚠️ the commands plan keeps only findings naming no agent,
so this one lands nowhere else: the `4_grille.md` change is carried by
this entry alone.

### sondeur.md F09 — the grid grounds a *défaut* on a pattern, the agent forbids it

Verdict: confirmed — against the refonte's grid,
`docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md` (the copy at
`docs/process/GRILLE_CADRAGE_PRODUIT_V2.md`, which sondeur.md L44
names, holds no *défaut*, *transverse* or *pattern* at all).
Cited: docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md L38 — « **Défaut**
| A transverse rule, or a pattern the file already follows, answers it.
The proposal is written with what founds it, and silence accepts it »
· L40-41 — « A *défaut* always carries its ground — the transverse
block quoted in its own words, or the blocks that already follow the
pattern. » · sondeur.md L398-400 — « A transverse rule is the only
ground. Never *the other blocks do it this way* ».
Decision: — (see `## To settle`, item 1)
Where: sondeur.md L398-400 ↔ docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md L38-41
Owner: sondeur (agent side) · the grid (grid side) — whichever item 1
settles
Also in: —

---

## The thematic reports, filtered to the sondeur

### fichiers.md F07 — the audit does not see `cadrage-produit/blocked_*-NN.md`

Verdict: confirmed
Cited: 4_grille.md L431-434 — « A blocking file you named is filed, in
the folder it sits in: `git mv …/cadrage-produit/blocked_par-bloc.md
…/cadrage-produit/blocked_par-bloc-NN.md` » · L289-292 —
`blocked_existant.md` renamed `blocked_existant-NN.md` at the feature
root.
Decision: — `audit_blocages.md` L27 is outside this plan's reading list
(the command does not name the sondeur) and was not opened; the
sondeur's side is verified, the audit's is not. Whatever the fix, it
lands in `audit_blocages.md`, not in `sondeur.md` or `4_grille.md`.
Where: audit_blocages.md L27 ↔ 4_grille.md L433
Owner: `audit_blocages.md` — the commands' corrector
Also in: convertisseur.md (the finding names it too) — ⚠️ the commands
plan will not carry it (it names two agents)

### fichiers.md F12 — `/3_decoupe` files a root questions file without the `### Q` guard

Verdict: confirmed on the `/3_decoupe` side
Cited: 3_decoupe.md L49-51 — « File every root `questions-*.md`, by
`git mv` » with no guard before it; the command's only prior check is
`Clarification needed` (L44). An answered, not yet integrated
`questions-sondeur-NN.md` or `questions-existant-NN.md` at the root is
filed by it.
Decision: — the guard's form is the siblings' (3a_genre.md L68,
3b_nature.md L66, 5_reclasse.md L74 per the finding); 3a_genre.md is
outside this plan's reading list and 3b_nature.md L66 / 5_reclasse.md
L74 were not confirmed as carrying it. The sondeur changes nothing
either way.
Where: 3_decoupe.md L49 ↔ 3a_genre.md L68
Owner: `3_decoupe.md` — the commands' corrector
Also in: —

### fichiers.md F13 — `releve.md` has no reader outside the run that writes it

Verdict: confirmed
Cited: sondeur.md L222-223 — « Pass B, from the record alone — never
the blocks again. Gather one column across every block, then cross
it. » · 4_grille.md L371 — « Write the record to
…/cadrage-produit/releve.md » · L400 — « check the four questions files
exist, and the record » · L205-206 — archived to `closed/` with the
five others.
Decision: Change nothing — keep the record as a written file: it is
what pass B reads (L222), writing it is what makes « from the record
alone » checkable, and A-C6 (report Part 2) recorded it as the applied
fix. Its cost is one write per turn.
Where: 4_grille.md L371 ↔ sondeur.md L222
Owner: sondeur — no line changes
Also in: —

### chemins-amont.md F08 — two unnumbered blocking files in one turn

Verdict: confirmed
Cited: 4_grille.md L41-43 — « the four sondeurs run at once » · L54-58
— the table's three rows: « None », « One, its `## Decision` empty »,
« One, its `## Decision` filled »; nothing for two or more. L63-64 —
« A sondeur's decision → that reading alone ».
Decision: Make the table hold any number — every unnumbered file with
an empty `## Decision` stops the command and is named; every filled one
is named in its own reading's prompt, those readings run together, and
the merge waits for all of them.
Where: 4_grille.md L42 ↔ 4_grille.md L54-58
Owner: `4_grille.md` — the commands' corrector. Sondeur: no line
changes (each reading already writes its own file, L119-121).
Also in: —

### chemins-amont.md F09 — the second time's re-run stops on « nothing closed the turn »

Verdict: confirmed
Cited: 4_grille.md L181-184 — before invoking, « file every root
`questions-*.md` » — the empty `questions-sondeur-NN.md` that closed the
first time leaves the root on the run that then blocks in
`blocked_existant.md` · L162-165 — « What closes the first time is a
`questions-sondeur-NN.md` at the root holding no `### Q` » · L173-175 —
« Neither grep returns anything, and no empty file at the root → stop
and say so » · L289-291 — « Its decision filled, `/4_grille` runs the
second time again ». The fix's model is already in the file: L253-254
tests `questions-existant-NN.md` « anywhere, at the root or in
`questions/existant/` ».
Decision: Anchor the first-time closure test on the highest-numbered
`questions-sondeur-NN.md` being empty wherever it sits — root or
`questions/sondeur/` — the way L253-254 already tests
`questions-existant`; the same anchoring settles F10 below.
Where: 4_grille.md L162-175 ↔ 4_grille.md L181/L253-254/L289-291
Owner: `4_grille.md` — the commands' corrector. Sondeur: no line
changes.
Also in: —

### chemins-amont.md F10 — a sibling command files the closure's evidence away

Verdict: confirmed
Cited: 3_decoupe.md L49-51 — « File every root `questions-*.md` » ·
4_grille.md L162-165 — the closure evidenced by the empty file « at the
root » · L173-175 — no empty file at the root → stop · 5_reclasse.md
L50-54 — « a `questions-sondeur-NN.md` holding no `### Q`, at the root
or filed, and … a `questions-existant-NN.md` too. Neither there … →
stop: say to run `/4_grille` ».
Decision: Same as chemins-amont F09 — test the closure on the filed
file too; once `/4_grille` reads « root or filed », a hand-run
`/3_decoupe` between the closure and the second time no longer
deadlocks. No change to `/3_decoupe`.
Where: 4_grille.md L162 ↔ 3_decoupe.md L49
Owner: `4_grille.md` — the commands' corrector
Also in: —

### chemins-amont.md F12 — `/5_reclasse`'s closure test is unanchored and its attach condition untestable

Verdict: confirmed
Cited: 5_reclasse.md L50-54 — « A `questions-sondeur-NN.md` holding no
`### Q`, at the root or filed, and — when the feature attaches to the
global — a `questions-existant-NN.md` too. Neither there, or one
holding questions → stop » — read as written, an earlier turn's
answered file « holding questions » stops it, and the attach condition
names no grep · 4_grille.md L261-263 — when no block carries
`Global:`, « write `questions-existant-NN.md` empty, commit and push
without a worktree » — so the second time always leaves one, attached
or not · L444-447 — `NN` is the highest in `questions/sondeur/` plus
one, so the latest is the highest-numbered.
Decision: Anchor `/5_reclasse` on the highest-numbered
`questions-sondeur-NN.md` and the highest-numbered
`questions-existant-NN.md`, each present and holding no `### Q`, root
or filed — and drop the attach condition: `/4_grille` L261-263 writes
the existant file empty even when nothing attaches.
Where: 5_reclasse.md L50-54 ↔ 4_grille.md L261-263/L444-447
Owner: `5_reclasse.md` — the commands' corrector. Sondeur: no line
changes.
Also in: —

### renommages.md L22 · passages-amont.md L18

Sound in both reports; no finding to judge.

---

## To settle

### 1. The *défaut*'s second ground — « a pattern the file already follows » (F02, F09)

The refonte's §3 (modifications.md L395) and its grid
(docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md L38-41) give a *défaut*
two grounds: a transverse rule, or a pattern the file already follows.
The agent (sondeur.md L398-400) keeps the first and forbids the second,
with a reason: a pass A question « stands on its block alone » (L332-333,
L399-400), and under the C22 reading rule an angle reads only the blocks
the prompt names (L43, L63-65) — on a later turn, the blocks that follow
the pattern are ones it may not open. One sondeur reads the grid whole
(L44) and the other rule is in its own file; the merge cannot tell the
two forms apart.

This is a process-design choice on which questions the Product Owner
answers by hand and which she accepts by silence; it is not decided
here. Two options:

| Option | What changes | What it costs |
|---|---|---|
| (a) Transverse rule only — align the grid L38-41 and §3 to the agent | `docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md` L38-41 (and modifications.md L395, as record) | A gap a same-file pattern would have grounded becomes an obligatory question: more lines for the Product Owner to write. It is the only option consistent with the C22 reading as applied (an angle cannot see the pattern's blocks) |
| (b) Both grounds — restore the pattern in the agent | sondeur.md L398-400, L306 (the two-row table), L394-396 | Contradicts L63-65 and L332-333; an angle on a later turn cannot read the blocks that carry the pattern, so only the global could ground it — and the global does not run pass A (L169, L219-220). Would need the reading rules reopened |

Related, same lines, not blocking: §3 (modifications.md L397-398) asks
for « la référence du paragraphe qui la fonde »; the agent quotes the
words (L391, L394-395). Report Part 2 A-§3 (b) records it as `other`.
Whichever option wins, say which of the two forms the `Défaut:` line
carries.

---

## Not verified — flagged to whoever assembles the plans

- Report Part 2 lists **B-2** and **D-12** as `open` with no location
  and no text; neither is in this plan's reading list, so they are
  neither judged nor planned here.
- **fichiers.md F07** and **F12** carry `Decision: —` because their
  other side (`audit_blocages.md`, `3a_genre.md`) is outside this
  plan's reading list. Both name an agent, so the commands plan will
  not pick them up either; they need an owner.
- **sondeur.md F08** is BLOCKING and its fix is in `4_grille.md`; for
  the same reason it is carried by this plan only.
- sondeur.md L44 names `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md`; the
  grid that carries the *défaut* level lives today at
  `docs-new/process/…`. Not a finding of the report — noted in case the
  rollout does not move `docs-new/` over `docs/`.
