# Plan — commandes

The twenty-first plan. Built against `.claude-new/commands/*.md` and
`.claude-new/CLAUDE.md`, from the six thematic reports read whole.

**Which findings land here.** Every row of the six reports was tested
against the twenty agent names of `.claude-new/agents/` — the same
`Select-String -Pattern '<agent>'` filter the twenty other plans were
built on, case-insensitive, unaccented. Twenty-two rows name no agent
and land in no other plan:

| Report | Findings kept |
|---|---|
| `renommages.md` | F14, F15 |
| `fichiers.md` | — *(every row names an agent)* |
| `chemins-amont.md` | F07, F11, F13, F15, F16, F17, F18, F20, F22, F26, F27, F28, F29 |
| `chemins-aval.md` | F01, F13, F14, F15, F16, F17, F21 |
| `passages-amont.md` | — *(every row names an agent)* |
| `passages-aval.md` | — *(every row names an agent)* |

⚠️ **One caveat on the filter**: `chemins-aval.md` F21 names *the
Réalisateur* with its accent, which `realisateur` does not match — it
lands here and nowhere else, and the Réalisateur is a `Follows` on it.

Twenty-two findings, twenty-two `confirmed`. None is stale, none is
wrong: every cited line reads today as the report describes it — two
exceptions on line numbers alone, noted in place (`audit_conventions.md`
has moved since the reports were written; the substance holds at the
lines cited below). Twenty-one carry a decision; one (`renommages.md`
F15) carries none, because the file it bears on may not be opened.

Two questions the reports settled apply here: `chemins-amont.md` F16
(its decision is copied from `decisions.md`) and `cadreur.md` F23 /
`fichiers.md` F09, which retire `cycle.md` — the deletion itself is
`renommages.md` F14 below.

One question met while building the plan is not in `decisions.md` and
goes to `## To settle` at the end.

---

## renommages.md

### renommages.md F14 — `cycle.md` survives, naming commands that do not exist

Verdict: confirmed
Decision: Delete `.claude-new/commands/cycle.md`, and remove every
mention of `/cycle` and `cycle.md` from the new chain.
Where: cycle.md L1, L9-10 ↔ .claude-new/CLAUDE.md L49-57
Cited: cycle.md L9-10 — "**This command chains the cycle's own
commands** — `/1_structure`, `/2_grille`, `/3_reclasse`,
`/4_convertit`, `/7_decoupe`"
Cited: .claude-new/CLAUDE.md L51 — "| `/socle` · `/diagnostique` | see
each | **Outside the cycle** — set up, enter on a bug |" — the commands
table L49-57 has no `/cycle` row: the file is registered nowhere and
still answers a typed `/cycle`.
Owner: commandes — the file is removed, not rewritten
Also in: cadreur (cadreur.md F23, moot on this deletion), verificateur
(fichiers.md F09, moot on this deletion)

`decisions.md` already rules it: "`cycle.md` is deleted — the command
is gone and so is the row. Remove every mention of `/cycle` and
`cycle.md` wherever you meet one." A grep of `.claude-new/` today finds
`/cycle` and `cycle.md` in `cycle.md` alone — the deletion is the whole
job. `stop1.md` keeps its two readers (`socle.md` L17-20, `8_code.md`
L215-217) and needs no creator: `8_code.md` L216-217 says "Neither
being there is not an error".

---

### renommages.md F15 — the process documents still say "`/cycle` ne l'appelle pas"

Verdict: confirmed
Decision: —
Where: PROCESS_AMONT.md L1210 ↔ PROCESS_AVAL.md L1010
Owner: the Product Owner — `docs/process/` is her own
Also in: —

Not verified: `CLAUDE.md` forbids opening anything in `docs/process/`
("Reading one puts discarded reasoning into your context"), and a
`Select-String` on the file is a read of it. The finding is
`confirmed` by default — no citation contradicts it — and gets no
decision: the two documents are the Product Owner's, no agent of the
chain applies a change to them, and this plan may not open them to
decide one. Relay to her that once F14 removes `/cycle`, the two
sentences the report cites describe a command that no longer exists.

---

## chemins-amont.md

### chemins-amont.md F07 — "run again" on an empty line has no cap

Verdict: confirmed
Decision: Cap the *run again* on a line left empty at one more run —
as `/3_decoupe` caps its partial sweep — and stop, naming the blocks,
when the second run leaves one empty too.
Where: 3a_genre.md L233 ↔ 3b_nature.md L238
Cited: 3a_genre.md L233 — "The `^Genre:$` count is non-zero and no
blocking file explains it → Say which blocks, and run `/3a_genre`
again"
Cited: 3b_nature.md L238 — "A block carrying `Genre: comportement`
still has an empty `Nature:`, and no blocking file explains it → Say
which, and run `/3b_nature` again"
Cited: 3_decoupe.md L203-205 — "📌 **Twice at most** — ⚠️ **still short
at the second, stop and say which blocks were never looked at**"
Owner: 3a_genre and 3b_nature — the same row in both
Also in: —

Severity stands at NOTE: the row is a relay to the Product Owner, who
runs the command by hand — the unbounded loop is hers to break, not an
agent's. The cap gives her a stop with the blocks named instead.

---

### chemins-amont.md F11 — a closed grid re-run stops on a wrong diagnosis

Verdict: confirmed
Decision: Make the stop at L173 tell a closed grid from a run that
wrote nothing — the second time already run is the closed case — and
name the next step in each.
Where: 4_grille.md L173-175 ↔ 5_reclasse.md L203
Cited: 4_grille.md L173-175 — "Neither grep returns anything, and no
empty file at the root → 🔴 **stop and say so**: nothing moved and
nothing closed the turn — ⚠️ **a run produced no questions file at
all.**"
Cited: 4_grille.md L253-255 — "Has it already run? 📌 **A
`questions-existant-NN.md` anywhere, at the root or in
`questions/existant/`** — ⚠️ **one and the second time is over**" — the
test exists, but sits after the stop.
Cited: 5_reclasse.md L79 — "File every root `questions-*.md`" — and
L203 — "📌 `/6_convertit`." Once `/5_reclasse` has filed the empty
`questions-sondeur`, no marker and no empty file remain, and L173
fires on a grid that is closed, not broken.
Owner: 4_grille
Also in: sondeur (chemins-amont.md F09, F10 — the same L162-175 block,
on the states before the second time)

---

### chemins-amont.md F13 — the answered technical file is filed before the row that fires on it

Verdict: confirmed
Decision: File an answered `technique-<nature>.md` into `closed/` only
after the nature has run on it — in *Once it has run* — never in *Git,
before invoking*.
Where: 6_convertit.md L78-83 ↔ 6_convertit.md L131, L171
Cited: 6_convertit.md L78-80 — "**And every `convertisseur/questions-*.md`
the last run wrote**, into `convertisseur/closed/`, each under the next
free number — 📌 **and every answered `technique-<nature>.md` with
them**"
Cited: 6_convertit.md L131 — "🔴 **Its `convertisseur/technique-<nature>.md`
holds an answered question** | 🔴 **Runs** — […] 📌 **Name the file in its
prompt**" — and L171, the prompt line that names
`convertisseur/technique-<nature>.md`, a path L78-83 has just emptied.
Owner: 6_convertit
Also in: convertisseur (fichiers.md F01 — the same defect, from the
agent's side)
Follows: convertisseur — what it does with the answered file it is
named (keeps it, or writes a new one over it) has to hold with the
moment the command now files it.

BLOCKING stands: the short loop L361 promises never applies an answer.

---

### chemins-amont.md F15 — a blocking file with product questions skips the long loop

Verdict: confirmed
Decision: Route the *blocking file and questions together* row by the
kind of question — product questions take the long loop of L362
whatever else waits, with the decision filled before it; `/6_convertit`
directly only when every question is technical.
Where: 6_convertit.md L360 ↔ 6_convertit.md L362, L62
Cited: 6_convertit.md L360 — "**A blocking file and questions
together** | 🔴 **Answer the questions first**, then fill the decision,
then `/6_convertit`"
Cited: 6_convertit.md L362 — "**Product questions, alone or with
technical ones** | 📌 **Answer them, then `/1_lexique`** — 🔴 **the long
loop.**"
Cited: 6_convertit.md L62 — "🔴 **Move every root `questions-*.md`:**"
— no `### Q` guard: the answered product questions are filed
unintegrated on the very rerun L360 sends the Product Owner to.
Owner: 6_convertit
Also in: — (the filing without a guard is chemins-amont.md F27 below;
its fix closes the loss, this one closes the route)

---

### chemins-amont.md F16 — a nature waiting on a product answer that changed no block

Verdict: confirmed
Decision: Add the outcome `decisions.md` settles — a product answer
that changed no block leaves the nature kept and the document
standing: the nature does not run, its part stays as it is, and the
turn closes with a relay row that says so.
Where: 6_convertit.md L132 ↔ 6_convertit.md L363
Cited: 6_convertit.md L132 — "Either of the two, **its part
byte-identical, and no answered technical file** | 📌 **Waits** — 🔴 **it
does not run.**"
Cited: 6_convertit.md L363 — "**A nature is waiting** on an unanswered
technical question | 🔴 **Answer it, then `/6_convertit`**" — the only
*waiting* row, and it covers the technical case alone.
Owner: 6_convertit
Also in: —

Settled by `decisions.md` (chemins-amont.md F16): "An answer that
changes no block leaves the document standing. That is an outcome, not
a wait — a relay row was missing, not a rule." ⚠️ **One thing the
decision does not say** — what becomes of the `<<ASSUMED` mark the
section still carries — is in `## To settle`, and this entry stops
where it bites.

---

### chemins-amont.md F17 — the nature re-run has no cap

Verdict: confirmed
Decision: Cap the re-run of a nature that did not apply its technical
answer at once, as invocation 2's re-run is, and report a second miss
as a fault of the run.
Where: 6_convertit.md L271-273 ↔ 6_convertit.md L279-280
Cited: 6_convertit.md L271-273 — "An `<<ASSUMED` mark left beside an
answered technical file is a nature that did not apply its answer —
⚠️ **say which, and run it again.**"
Cited: 6_convertit.md L279-280 — "say so, and run invocation 2 once
more. 📌 **Once, never twice.**"
Owner: 6_convertit
Also in: —

---

### chemins-amont.md F18 — a `bugfix-NN` argument with nothing pending has no outcome

Verdict: confirmed
Decision: Give the walk an outcome for a `bugfix-NN` second argument
that holds no request with an empty `## Verdict` — nothing to invoke,
said as such, with `/8_code` named as what carries on.
Where: conventions.md L76 ↔ conventions.md L26-27
Cited: conventions.md L76 — "**It exists, and no `couverture.md` at the
working folder's root** | 🔴 **Invocation 4 — Completing** — ⚠️ **on a
feature folder only**: 📌 **a `bugfix-NN` carries no technical document
of its own to walk**" — the row matches a bugfix folder (it never
holds a `couverture.md`) and forbids itself in the same cell.
Cited: conventions.md L26-27 — "📌 **Invocation 3 runs where the
request was written** — the feature folder, or a `bugfix-NN/` inside
it. **A second argument names it.**"
Owner: conventions
Also in: —

---

### chemins-amont.md F20 — routing on a line the reading list does not grant

Verdict: confirmed
Decision: Grant the reading list the two headings the walk keys on —
whether `## Decision` is filled, and the `## Invocation` line — of
`blocked_architecte.md`, and nothing more of it.
Where: conventions.md L70 ↔ conventions.md L33-38
Cited: conventions.md L70 — "🔴 **A `blocked_architecte.md` with a
filled `## Decision`** | 📌 **The invocation its `## Invocation` line
names**"
Cited: conventions.md L33-38 — "**Whether the files are there** —
`spec-technique.md`, `couverture.md`, `docs/TECHNICAL_CONVENTIONS.md`,
and `questions-architecte-*.md` at the root — 🔴 **plus two greps on
that last one** […] ⚠️ **Counts, never content**"
Cited: architecte.md L247 — "| `## Invocation` | 🔴 **The one that
wrote this file — 1, 2, 3 or 4** |" — the line exists on the agent's
side; only the command's permission to read it is missing.
Owner: conventions
Also in: —

---

### chemins-amont.md F22 — invocation 3's empty file sends the merge to invocation 2 with no plan

Verdict: confirmed
Decision: Fire rows 9 and 10 only when `plan-fusion.md` exists; an
empty or resolved `questions-fusionneur-NN.md` with no plan is
invocation 3's, and routes to invocation 1.
Where: fusion.md L49 ↔ fusion.md L61, fusionneur.md L262-263
Cited: fusion.md L49 — "| 9 | `questions-fusionneur-NN.md`, answered —
📌 **empty, or its questions resolved** | **Fusionneur, invocation 2**
|"
Cited: fusion.md L61 — "a correction cycle would go to invocation 2,
which needs a plan no invocation wrote." — the case the row order is
said to prevent, and row 9 fires on it after row 8's pass.
Cited: fusionneur.md L262-263 — "| 2 | Apply | The merge plan · **the
questions file you wrote**, answered · the global |" and "| 3 |
Bug-fix decisions | Every `bugfix-*/bug-list.md` of the feature · the
global | The updated global · a questions file |" — invocation 3
writes a questions file and no plan; invocation 2 needs the plan.
Owner: fusion
Also in: fusionneur (chemins-amont.md F21 — row 7, the answered case
of the same file)
Follows: fusionneur — what invocation 1 does with an answered
invocation-3 file at the root is the fusionneur plan's F21; this
decision only stops the empty one from reaching invocation 2.

BLOCKING stands: a correction cycle's merge never reaches
invocation 1.

---

### chemins-amont.md F26 — `/fusion_compare` relays no next step

Verdict: confirmed
Decision: Add a *what to run next* table — questions to answer, then
`/fusion_applique`; an empty file, `/fusion_applique` at once; a
blocking file, its decision then `/fusion_compare` again.
Where: fusion_compare.md L131-132 ↔ 1_lexique.md L93-95
Cited: fusion_compare.md L131-132 — "The agent's own report, and
nothing more. 🔴 **Nothing else is yours**: no phase chain."
Cited: 1_lexique.md L94-95 — "⚠️ **A stop that names no next step
leaves the Product Owner to guess.**"
Owner: fusion_compare
Also in: —

---

### chemins-amont.md F27 — five commands file a questions file without the `### Q` guard

Verdict: confirmed
Decision: Put the `### Q` guard of `/3a_genre` in front of the filing
step of `/3_decoupe`, `/4_grille`, `/6_convertit`, `/conventions` and
`/fusion_compare` — a root file holding questions stops the command,
naming it, and is never filed.
Where: 3_decoupe.md L49 · 4_grille.md L181 · 6_convertit.md L62 ·
conventions.md L110 · fusion_compare.md L36 ↔ 3a_genre.md L68-70
Cited: 3a_genre.md L68-70 — "🔴 **Grep `^### Q` in each before touching
it** — 📌 **a file holding questions is not yours to file**: ⚠️ **it
waits on an answer, or its answers were never integrated.** 🔴 **Stop
and say which.**"
Cited: 3_decoupe.md L49 — "🔴 **File every root `questions-*.md`**, by
`git mv`:" · 4_grille.md L181 — "🔴 **Before invoking, file every root
`questions-*.md`:**" · 6_convertit.md L62 — "🔴 **Move every root
`questions-*.md`:**" · conventions.md L110-111 — "🔴 **File away every
root `questions-*.md` whose prefix is not `architecte`:**" ·
fusion_compare.md L36-37 — "🔴 **Before invoking, move every root
`questions-*.md` whose prefix is not `fusionneur`:**" — none of the
five greps `### Q` first.
Owner: the five commands, each its own filing step
Also in: sondeur (fichiers.md F12), lexicographe (fichiers.md F17,
chemins-amont.md F02), architecte (fichiers.md F04, chemins-amont.md
F19) — the same loss, seen from each file's writer

`/4_grille` keeps its own L97-100 test (the latest root file answered)
beside the guard: an answered file still holds `### Q` until the
Rédacteur integrates it, and the guard is what keeps it at the root
until then.

---

### chemins-amont.md F28 — `/2_structure` can structure on a vocabulary still open

Verdict: confirmed
Decision: Make `/2_structure` refuse invocation 1 until the lexicon
loop has closed — the latest `questions-lexicographe-NN.md`, at the
root or filed, holding no `### Q`.
Where: 1_lexique.md L243 ↔ 2_structure.md L119
Cited: 1_lexique.md L243 — "| 2 wrote none | 📌 `/1_lexique` again — 🔴
a settled term can uncover a pair |" — and L189-194: the applied file
is filed and 2 wrote none, so the root holds no lexicographe file.
Cited: 2_structure.md L119 — "| No questions file, **and no
`desc-produit.md`** | **1 — Structuring** | `idees.md` |" — an empty
root is exactly what the open loop leaves.
Cited: 1_lexique.md L87-91 — "⚠️ **It stops 1 and 2**: the vocabulary
is settled before the product file exists, never after — a term
changed then would leave sixty blocks carrying the old one."
Owner: 2_structure
Also in: —

The loop closes on one evidence only — invocation 1 asking nothing
writes an empty `questions-lexicographe-NN.md` (1_lexique.md L57,
L201-202, L241) — and that file is the highest-numbered one whenever
the loop is closed. The guard reads that, and also stops a
`/2_structure` run before `/1_lexique` ever ran.

---

### chemins-amont.md F29 — the `NEW` grep is unanchored

Verdict: confirmed
Decision: Anchor `/2_structure`'s `NEW` grep on the title line, as
`/3_decoupe` and `/4_grille` anchor theirs.
Where: 2_structure.md L164-165 ↔ 3_decoupe.md L81, L84
Cited: 2_structure.md L164-165 — "🔴 **Did the run create a `NEW`
block?** 📌 **Grep `NEW` in `desc-produit.md`** — ⚠️ **and only then:**"
Cited: 3_decoupe.md L81 — "| `grep '^### .*NEW'` | The blocks created
since the last turn |" — and L84-85: "🔴 **Anchored on the title
line.** ⚠️ **A bare `NEW` matches prose inside a block**"
Owner: 2_structure
Also in: —

---

## chemins-aval.md

### chemins-aval.md F01 — `/7_lots` run from inside the `/8_code` worktree

Verdict: confirmed
Decision: Close the loop's own worktree before running `/7_lots` —
commit, merge, push, remove — then open a fresh one from the merged
`HEAD` and carry on the loop from there.
Where: 8_code.md L365-366, L86 ↔ 7_lots.md L64, L224
Cited: 8_code.md L365-366 — "**Then run `/7_lots` on this working
folder**, and wait for it. ⚠️ **Then carry on your loop**" — issued
from the worktree of L86, `git worktree add .claude/worktrees/<name>
HEAD`.
Cited: 7_lots.md L64 — "    git worktree add .claude/worktrees/<name>
HEAD" — the same path and branch the loop is sitting in; and L224 —
"`git merge --no-ff <branch>` from the main checkout root" — a merge
the loop's branch never receives.
Owner: 8_code
Also in: cadreur (fichiers.md F16, chemins-aval.md F02 — the relay of
`## Ce qui revient` sits on the same move), realisateur (chemins-aval.md
F25 — "the worktree is about to be removed", realisateur.md L352,
becomes true under this decision)
Follows: 7_lots — none of its text changes; it creates and removes its
own worktree as it does today. realisateur — its L352 reason now holds;
the realisateur plan's F25 entry reads against this decision.

BLOCKING stands. L366's intent — "you do not hand back, and the Product
Owner is not waiting on anything" — is kept: the loop resumes by
itself on the re-cut sequence, which it now reads from the merged
`HEAD`.

---

### chemins-aval.md F13 — phase 4 reads `par-genre/recette.md` under the wrong folder

Verdict: confirmed
Decision: Read `par-genre/recette.md` at the feature folder's root —
one level up from a `bugfix-NN/` working folder — as `/audit_conventions`
does for `couverture.md`.
Where: 9_controle.md L239-240, L18 ↔ 5_reclasse.md L96, L112
Cited: 9_controle.md L239-240 — "🔴 **Two sources**: 📌
**`code/recette.md`**, the lines the testeur wrote lot by lot, **and
`par-genre/recette.md`**" — under L18, "📌 **Every path below is
relative to it**", the working folder.
Cited: 5_reclasse.md L96-97 — "**Six files, under `par-genre/` in the
feature folder, replaced whole:**" — and L112: "| `par-genre/recette.md`
| 🔴 **The Product Owner**, handed back by `/9_controle` |" — the file
lives at the feature root and nowhere else.
Cited: audit_conventions.md L40-43 — "🔴 **On a correction cycle it is
not in the working folder** […] ⚠️ **Look for it one level up**, at the
feature folder's root, and use it from there." — the report cites this
rule at L243; the file has moved since, and the rule reads today at
L40-43.
Owner: 9_controle
Also in: —

---

### chemins-aval.md F14 — `/9_controle` takes the working folder where every other downstream command derives it

Verdict: confirmed
Decision: Derive the working folder from the feature name — the highest
`bugfix-NN/` in it, the feature folder otherwise — as `/7_lots`,
`/8_code` and `/audit_conventions` do, and drop the path argument.
Where: 9_controle.md L15-16 ↔ 8_code.md L25-26, L257-258
Cited: 9_controle.md L15-16 — "**The argument is the working folder** —
`docs/features/<name>/`, or `docs/features/<name>/bugfix-NN/`." —
against its own L4, `argument-hint: "<feature folder name>"`, and L12.
Cited: 8_code.md L25-26 — "🔴 **The working folder is the highest
`bugfix-NN/` in it, if there is one; the feature folder itself
otherwise.**" — and L257-258: "📌 **Say that `/9_controle` is what comes
next** — 🔴 **run by hand, on both cycles.**" — no word that the
argument changes shape on a correction cycle.
Owner: 9_controle
Also in: —
Follows: 8_code — its L257 relay then names `/9_controle <feature>`
without a path to build; audit_conventions.md L15-17 already carries
the same rule and changes nothing.

The chain's order makes the derivation safe: `/9_controle` on the main
cycle runs before any `bug-list.md` exists, so before any `bugfix-NN/`
does.

---

### chemins-aval.md F15 — `/deploie` declares Bash and writes PowerShell

Verdict: confirmed
Decision: Declare in `allowed-tools` the tool the three commands are
written for — the PowerShell tool — instead of Bash.
Where: deploie.md L3 ↔ deploie.md L35-44
Cited: deploie.md L3 — "allowed-tools: Bash"
Cited: deploie.md L35-36 — "🔴 **In PowerShell the variable goes on its
own line, before the command**" — and L38-44: `$env:ANDROID_SERIAL =
"<phone identifier>"`, `.\gradlew :app-phone:installDebug`,
`Remove-Item Env:\ANDROID_SERIAL` — Git Bash rejects all three.
Owner: deploie
Also in: —

The file's own sentence at L35 fixes which side gives way: the
commands are PowerShell by design, the tool line is the error. This
environment exposes a `PowerShell` tool beside `Bash`; ⚠️ **if the
harness the command runs under has none**, the alternative is the
same three commands in Bash syntax — one or the other, never the
present pair.

---

### chemins-aval.md F16 — a register "of every cycle" written under a per-cycle folder

Verdict: confirmed
Decision: Keep one register per feature, at the feature folder's root
and outside any `bugfix-NN/`, so that every cycle appends to the same
file.
Where: 9_controle.md L284-285, L287 ↔ 9_controle.md L15-18
Cited: 9_controle.md L284-285 — "⚠️ **Append, never overwrite**: the
file is the record of every cycle, not of this one." — and L287:
"**Write `code/registre-questions.md`.**"
Cited: 9_controle.md L15-18 — "**The argument is the working folder**
[…] 📌 **Every path below is relative to it.**" — `code/` under a
`bugfix-NN/` is a fresh folder each correction cycle.
Owner: 9_controle
Also in: —

No other command or agent reads `registre-questions.md` (a grep of
`.claude-new/` finds it in `9_controle.md` alone), so the move touches
one file. `code/decisions-produit.md` stays per cycle — `fusion.md`
L91-92 reads it "in cycle order", which is what a per-cycle file is for.

---

### chemins-aval.md F17 — the no-coverage skip names the wrong finding

Verdict: confirmed
Decision: Make the skip without `couverture.md` name findings 1, 4
and 7, and keep finding 6 running.
Where: audit_conventions.md L48-50 ↔ audit_conventions.md L131-133,
L138-139
Cited: audit_conventions.md L48-49 — "⚠️ **Absent from both** — 🔴
**findings 1, 4 and 6 cannot be made.**"
Cited: audit_conventions.md L131-133 — "**6. A rule already reported,
still unchanged.** 🔴 **Your earlier passes name rules by their
identifier** — 📌 **`TECHNICAL_CONVENTIONS.md` is read every pass**" —
earlier passes and the conventions file, no `couverture.md`.
Cited: audit_conventions.md L138-139 — "**7. A rule the split never
meets.** 🔴 **No lot's `Anchor` cites the entry `couverture.md` traces
it to.**" — the one that cannot be made without it.
Owner: audit_conventions
Also in: —

The report cites L251 ↔ L341; the file is 212 lines today and the two
passages read at L48-50 and L131-139. The substance is unchanged.

---

### chemins-aval.md F21 — an attempt that committed nothing has no route

Verdict: confirmed
Decision: Route an attempt that committed nothing as a FAIL — move 4
applies, a fresh Réalisateur runs — and give the verdict the
orchestrator writes a `## Status` the Réalisateur's FAIL table has a
row for.
Where: 8_code.md L129-132 ↔ 8_code.md L138, realisateur.md L521-522
Cited: 8_code.md L129-132 — "📌 **An empty list means the realisateur
committed nothing** — 🔴 **that counts as a failed attempt, and the
Relecteur is not invoked.** ⚠️ **Increment `## Attempts` yourself
then**"
Cited: 8_code.md L138 — "**4.** On FAIL → a **fresh `realisateur`**,
with the verdict" — keyed on a FAIL no one wrote, and on a first
attempt there is no verdict to increment into.
Cited: realisateur.md L521-522 — "| **FAIL mineur** | Fix the point
reported […] **amend the report**" / "| **FAIL structurel** | Take the
lot back from move 1" — two rows, both keyed on a status the
orchestrator's verdict does not carry, and the first on a report that
does not exist.
Owner: 8_code
Also in: —
Follows: realisateur — its FAIL table gains the row for that verdict:
no report to amend, no code to fix, the lot from move 1.

---

## To settle

### The `<<ASSUMED` mark of a nature whose product answer changed no block

`decisions.md` settles chemins-amont.md F16 as an outcome — the nature
does not run, its part stays, the document stands. ⚠️ **It says nothing
of the mark the section still carries.** The Convertisseur marks an
entry waiting on a product answer with `<<ASSUMED B40: …>>`
(convertisseur.md L464-466), the mark "is lifted by writing the section
again" (L468-470), and the Cadreur stops on the first one
(convertisseur.md L32, passages-amont.md F05). So the document the
decision calls *standing* still stops `/7_lots`.

Three ways out, none this plan's to pick:

| Option | What it costs |
|---|---|
| The command reruns the nature to lift the mark, part unchanged | One opus invocation for a known result — exactly the cost 6_convertit.md L132 refuses; and the agent, reading the same blocks, may write the same mark again |
| The command lifts the mark by script, keeping the assumed line | The assumption stands as a rule nobody validated — the answer said *the blocks are right as they are*, which is not the same as *the assumed line is right* |
| The Convertisseur writes no `<<ASSUMED` for a product question — the pending block is visible in the questions file alone | The Cadreur loses the inline signal that an entry waits; `<<ASSUMED` becomes technical-only, and convertisseur.md L388-390 ("one mark, not two") is reversed |

Decision: —

The F16 entry above applies what `decisions.md` settled and stops
here; the Owner of this question is whoever the Product Owner names,
across `6_convertit`, `convertisseur` and `cadreur`.
