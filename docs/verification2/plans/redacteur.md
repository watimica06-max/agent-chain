# Plan — `redacteur.md`

Base: `.claude-new/agents/redacteur.md` at local `HEAD`, worktree
`correction-2026-09-17`. Line numbers are that file's unless another
file is named.

Findings judged: `redacteur.md` F01–F22, the four `other` rows of its
part 2, and the thematic-report findings that name the redacteur
(`chemins-amont` F23 · `fichiers` F06 · `passages-amont` F01, F02, F03,
F04, F08, F09, F10, F11). Findings that describe one defect are
grouped under one entry.

`cycle.md` L86 and L88 name the redacteur; per `decisions.md`
(`cadreur.md` F23) the command is deleted and nothing here builds on
it.

---

## Entries

### redacteur F01 · redacteur F14 · passages-amont F02 — the `en anglais :` line on `## Relevé`

Verdict: confirmed
Decision: Write the `en anglais :` line on the `## Tranché` entry
alone — drop the `## Relevé` clause at L169-170 and the sentence
spliced into it.
Where: redacteur.md L168-173 ↔ modifications.md L205-208 ↔
lexicographe.md L176-177, L199-200, L285-287
Owner: redacteur
Also in: lexicographe plan (passages-amont F02)

Cited: modifications.md L205-207 — « Quand il rend un concept en
anglais pour la première fois, il écrit le mot retenu dans l'entrée
`## Tranché` de ce concept ».
Cited: lexicographe.md L176-177 — "The `en anglais` line is the
Rédacteur's, and his alone — he writes it on a concept you settled".
Cited: lexicographe.md L199-200 — "A sweep rebuilds what it found from
the idea file"; L285-287 — "`## Relevé`: every term you found, with
its count. You rebuild what comes from the idea file". The `## Relevé`
shape at L162-166 is one line per term, no sub-line.

Three files agree on `## Tranché`; the redacteur alone extends to
`## Relevé`, where the lexicographe's rebuild wipes the line. Its
compare at lexicographe.md L464-466 reads `en anglais` lines wherever
they survive, so nothing on that side changes. The residual gap the
extension aimed at goes to *To settle*.

### redacteur F02 — strip on `existant` and `convertisseur`

Verdict: overstated
No decision.

`existant` — wrong as a defect: 4_grille.md L269-279 invokes
`subagent_type="sondeur"`, "Invocation 3 — Existant", writing
`questions-existant-NN.md` — it is a grid file by the sheet's own
criterion (passes/redacteur.md L86-88: "a file from the grid … means a
turn ran on the current markers — strip, then re-mark").

`convertisseur` — real, and NOTE: the sheet names no such prefix, but
its principle holds. 6_convertit runs only once the grid has closed,
and 4_grille.md L167-170 says the markers of a closed turn stay
("An empty one is integrated by nobody, so the markers stay") — so
every marker present when a convertisseur file is integrated was
consumed by a grid turn, and stripping it is what the sheet asks.
Nothing to apply.

### redacteur F03 — the invocation-2 route on a `blocked_*` file, absent from the index

Verdict: confirmed
Decision: Leave the route as it stands — nothing to apply in the
agent.
Where: modifications.md L143 ↔ redacteur.md L527-542
Owner: —
Also in: —

Cited: qualifieur.md L266-267 — "The block is to be rewritten or
removed → Leave the line empty — say in your report that the block
waits on the Rédacteur"; 2_structure.md L120 carries the same row. The
route is what three agents' `## To resume` need; its absence from the
index is the index's.

### redacteur F04 — "it runs past 250 KB" removed, unmentioned

Verdict: confirmed
Decision: Leave L414-416 as it stands — nothing to apply.
Where: modifications.md L143 ↔ redacteur.md L414-416
Owner: —
Also in: —

L414-416 reads "it is the whole product, and you need a handful of
sections" — the rule stands without the figure.

### redacteur F05 — the sentence lists two lines, the example carries four

Verdict: confirmed
Decision: Make the sentence at L56-57 list every line the example at
L59-62 shows — identifier, `Genre:`, `Nature:`, `Global:` when the
block attaches, marker when it moved.
Where: redacteur.md L56-57 ↔ redacteur.md L59-62
Owner: redacteur
Also in: —

### redacteur F06 — "only when a grid turn ran" against the `convertisseur` row

Verdict: confirmed
Decision: Reword L119 so the rule covers both rows of its table — a
turn that consumed the markers, grid or conversion — matching L553-555.
Where: redacteur.md L119 ↔ redacteur.md L125, L553-555
Owner: redacteur
Also in: —

Cited: L553-555 — "strip both only when the file you integrate comes
from the grid or the conversion". The table at L124-125 and step 1 at
L553 agree; only the sentence at L119 excludes the conversion.

### redacteur F07 — two absolute prohibitions against invocation 3's strip

Verdict: confirmed
Decision: Carve invocation 3 out of the two rules at L323-325 — the
file it writes carries no marker, by L707-708.
Where: redacteur.md L323-325 ↔ redacteur.md L707-708
Owner: redacteur
Also in: —

### redacteur F08 — invocation 3's inputs against what it opens

Verdict: confirmed
Decision: Make `desc-produit-fusion.md` the file invocation 3 reads
and edits — in the inputs row at L385 and at L674 — drop
`desc-produit.md` from what it opens, and reword L668 so that
`decisions-produit.md` is the only source of decisions, not the only
artefact opened.
Where: redacteur.md L385 ↔ redacteur.md L668, L674, L687, L391
Owner: redacteur
Also in: —

Cited: fusion.md L79-84 — the command copies `desc-produit.md` to
`desc-produit-fusion.md` before invoking; L681 — "The product file
itself is never touched"; L315-316 — "invocation 3 works on a copy the
command made". Reading `desc-produit.md` at invocation 3 serves
nothing the copy does not.

### redacteur F09 — row 3 reads `lexique.md`, declares no `en anglais` output

Verdict: confirmed
Decision: Declare `lexique.md`, its `en anglais` lines, among row 3's
outputs, as rows 1 and 2 do.
Where: redacteur.md L385 ↔ redacteur.md L168-180
Owner: redacteur
Also in: —

L179-180 — "When the entry already carries one, you take it" — is why
row 3 reads the lexicon; a decision can also bring a first rendering.

### redacteur F10 — a `NEW` block changed on a strip-none turn

Verdict: confirmed
Decision: State the precedence once, for every case — a block carrying
`NEW` keeps `NEW` alone when changed — instead of inside the
transverse rule only.
Where: redacteur.md L99-100 ↔ redacteur.md L103-105
Owner: redacteur
Also in: —

4_grille.md L119-120 takes the union of both greps, so either spelling
reaches the grid; the fix is for two readers to write the same thing.

### redacteur F11 — what "found" means at move 2

Verdict: confirmed — settled by `decisions.md` (`redacteur.md` F11)
Decision: Apply the decision — `Global:` is written when move 2's
same-trigger test said yes, never on a title match; rewrite L83-85 so
a shared title makes no attachment, and a section created after a No
never takes a global's title.
Where: redacteur.md L83-85 ↔ redacteur.md L457-458, L442-451
Owner: redacteur
Also in: —

Cited: decisions.md L146-149 — "The same trigger, never a title that
resembles another. A close title says nothing — two sections can carry
the same name and describe two different behaviours." L245-246
("Grep before creating — a title close to an existing one creates a
duplicate") already forbids the case L83-85 describes.

### redacteur F12 — "on either branch", three branches, no file named

Verdict: confirmed
Decision: Name the questions file as where what is still missing is
said, and drop "either branch" — three branches lead there.
Where: redacteur.md L655-657 ↔ redacteur.md L541
Owner: redacteur
Also in: —

### redacteur F13 — `grep -B1 '^Global: '` returns the `Nature:` line

Verdict: confirmed
Decision: Keep the block shape; fix the lookup in `/4_grille` so it
reaches the heading three lines above `Global:`, as `/3b_nature` does
for `Nature:`.
Where: redacteur.md L59-62 ↔ 4_grille.md L257-258
Owner: 4_grille.md
Also in: —

Cited: 4_grille.md L257-258 — "Which blocks — `grep -B1 '^Global: '`
in `desc-produit.md`". Cited: 3b_nature.md L96 — "`grep -B2
'^Nature:$'` … two lines above each hit is the heading: `Genre:` sits
between". The shape `### B` / `Genre:` / `Nature:` / `Global:` is
written identically at redacteur.md L59-62 and decoupeur.md L201-204,
and `passages-amont.md` L17 found it sound across seven files; the
one wrong reader is the grep.

### redacteur F15 — the `/fusion` template names no decisions file

Verdict: overstated
No decision.

Real: fusion.md L156-163 carries `<Which invocation>` and no slot for
the decisions files. Not TO FIX: fusion.md L91-93 — "Name it every
`code/decisions-produit.md` that `/9_controle` produced, in cycle
order — the feature's own first, then `bugfix-01`, then `bugfix-02`" —
is the instruction the finding says is missing. An orchestrator that
skips it skips the command, not the template. NOTE: the template
lacks a slot the paragraph above it requires.

### redacteur F16 · chemins-amont F23 · passages-amont F09 · fichiers F06 — no `## Invocation` heading in `blocked_redacteur.md`

Verdict: confirmed
Decision: Add an `## Invocation` heading to the redacteur's blocking
file — five headings, as the fusionneur's — so `/fusion` row 3 routes
it and `/2_structure` can tell an invocation-3 block from its own.
Where: redacteur.md L343-359 ↔ fusion.md L43 ↔ fusionneur.md L200-205
Owner: redacteur
Also in: —

Cited: fusion.md L43 — "A `blocked_*.md` with a filled `## Decision` |
The agent its name carries, at the invocation its `## Invocation` line
names". Cited: fusionneur.md L200-203 — "Its shape — five headings …
`## Invocation` / <the one that wrote this file: 1, 2 or 3>";
architecte.md L247 carries the same heading. The redacteur's shape at
L343-359 has four.

Follows: 2_structure.md — its test at L103-110 names any filled
`blocked_redacteur.md` in an invocation-1/2 prompt; with the heading,
one written at invocation 3 belongs to `/fusion`, not to it. Note:
fichiers F06's second half ("sent to Integrating by `/2_structure`
L120") is not what L120 says — that row names the decoupeur's,
qualifieur's and classeur's files, not the redacteur's; the first
half stands.

### redacteur F17 — `/2_structure` renames the decoupeur's file alone

Verdict: confirmed
Decision: Have `/2_structure` rename every blocking file the run
applied — `blocked_decoupeur.md`, `blocked_qualifieur.md`,
`blocked_classeur.md` — not the decoupeur's alone.
Where: redacteur.md L531-535 ↔ 2_structure.md L191-194 ↔ 3a_genre.md
L34-38, 3b_nature.md L33-37
Owner: 2_structure.md
Also in: —

Cited: 2_structure.md L191-192 — "A `blocked_decoupeur.md` it applied
is renamed — `blocked_decoupeur-NN.md`"; nothing for the other two,
though L120 routes all three. The mechanism is not a stop but a loop:
3a_genre.md L38 — "Its `## Decision` is filled | Name it in the
prompt" — hands the already-applied file to the qualifieur, whose
L266-267 sends the block back to the Rédacteur. Severity stands.

### redacteur F18 — the template's `Read:` line has no blocking-file value

Verdict: confirmed
Decision: Give the `Read:` line of the `/2_structure` template a
third value, the blocking file row L120 names.
Where: redacteur.md L527-529 ↔ 2_structure.md L149, L120
Owner: 2_structure.md
Also in: —

Cited: 2_structure.md L149 — "Read: <idees.md, or
questions-<agent>-NN.md>."; L120 — "That file — all three block on
something only a rewrite of the block settles".

### redacteur F19 — a block created at invocation 3 has no nature

Verdict: confirmed
Decision: —  (see *To settle*)
Where: redacteur.md L702-705 ↔ fusionneur.md L386-387
Owner: —
Also in: —

Cited: fusionneur.md L386-387 — "The `Nature:` lines stay — the global
carries them". L703-705 sends a subject no title covers through the
four moves, which write an empty `Nature:` (L455); no classeur runs
after `/fusion`. Which side gives is a scope question.

### redacteur F20 · passages-amont F01 — one `## Decision` per `## Blocking N`

Verdict: confirmed
Decision: Have the redacteur apply every `## Decision` the file
carries, one under each `## Blocking N`; have `/2_structure` test that
each of them is filled before naming the file, and stop on any empty
one.
Where: redacteur.md L527-529, L537 ↔ classeur.md L196-199, L234-235 ↔
2_structure.md L120-121
Owner: redacteur
Also in: classeur plan (passages-amont F01)

Cited: classeur.md L234-235 — "Several blocked blocks go in one
blocking file — the four headings repeated for each, under a
`## Blocking N` title. One `## Decision` per block: they are not
settled together." Cited: 2_structure.md L120 — "with a filled
`## Decision`". The qualifieur's shape (qualifieur.md L259-260, "one
`## Where` entry each") keeps one `## Decision`, so the reader has two
shapes to read, not one to impose.

Follows: 2_structure.md (the test at L120-121).

### redacteur F21 — `/6_convertit` says every marker is stripped on each turn

Verdict: confirmed
Decision: Align the justification at 6_convertit.md L141-142 with the
prefix rule; the conclusion it founds stays.
Where: redacteur.md L119-126 ↔ 6_convertit.md L141-143
Owner: 6_convertit.md
Also in: —

Cited: 6_convertit.md L141-143 — "the Rédacteur strips every marker on
each turn, and a block changed two turns of the grid ago carries none
by now". Under L124-126 it strips on a grid or conversion file only;
by the time the conversion runs the grid has closed, so the block
still carries none — the reason is stale, the fact is not.

### redacteur F22 — "the only agent that writes the product file"

Verdict: confirmed
Decision: Reword the frontmatter claim to what holds — the only agent
that writes and rewrites the blocks' prose; three others write a line
or split.
Where: redacteur.md L3 ↔ decoupeur.md L3, qualifieur.md L3
Owner: redacteur
Also in: —

Cited: decoupeur.md L3 — "Writes in the product file, splits only,
never rewrites a sentence"; qualifieur.md L3 — "Writes that line in
the product file".

### passages-amont F03 — the vocabulary credited to the qualifieur

Verdict: confirmed
Decision: Name the lexicographe as the vocabulary's owner at L322.
Where: redacteur.md L320-322 ↔ lexicographe.md L176-181
Owner: redacteur
Also in: —

Cited: redacteur.md L322 — "the vocabulary is the qualifieur's";
lexicographe.md L176 — "The `en anglais` line is the Rédacteur's, and
his alone" — the rest of the lexicon is the lexicographe's, and
qualifieur.md L3 gives that agent genres.

### passages-amont F04 — the lexicon opened "by convention"

Verdict: wrong
No decision.

Cited: redacteur.md L383-384 — rows 1 and 2 list `lexique.md` and the
global among their inputs; L391 — "Load only what your invocation
lists". The lexicon is opened by the inputs row, not by convention.
2_structure.md L154-155 ("the agent opens that one and no other")
follows "Name the file, always" and reads on the questions file; loose
as a sentence, it contradicts nothing the agent does.

### passages-amont F08 — the decisions line's shape, and its language

Verdict: confirmed
Decision: Fix in `/9_controle` how the block is written on a
decisions line — the identifier first, in a form the redacteur greps —
and say at invocation 3 that a decision is translated as an answer is
at invocation 2.
Where: 9_controle.md L305-306 ↔ redacteur.md L674-705, L544
Owner: 9_controle.md
Also in: —

Cited: 9_controle.md L305-306 — "Write `code/decisions-produit.md` —
one decision per line, with the block it bears on when the file names
one." Invocation 2 says "you transcribe, translate and file" (L544);
invocation 3 (L661-714) says nothing of language, and its source is
the French `## Decision` of a blocking file.

Follows: redacteur (reads the identifier as written; translates).

### passages-amont F10 — `## Questions set aside`, written by nobody

Verdict: confirmed
Decision: Nothing on the redacteur's side — the section does not exist
and the redacteur adds none; the fusionneur drops the rule.
Where: fusionneur.md L306-308 ↔ redacteur.md L41-46, L661-714
Owner: fusionneur
Also in: fusionneur plan

Cited: fusionneur.md L306-308 — "Skip the product file's closing
section — `## Questions set aside`. It records what was ruled out".
The product-file structure at L41-46 has no such section, and
invocation 3 creates none.

### passages-amont F11 — which genres enter the global

Verdict: confirmed — settled by `decisions.md` (`passages-amont.md` F11)
Decision: Keep every genre in `desc-produit-fusion.md`, as L698 does;
the Fusionneur reads `Genre:` on every block and filters per the
decision.
Where: redacteur.md L698-708 ↔ fusionneur.md L336, L385-386
Owner: fusionneur
Also in: fusionneur plan

Cited: decisions.md L106 — "The Fusionneur reads `Genre:` on every
block, not only at `INIT`". The redacteur's copy has to carry the
`Genre:` lines for that read — it strips markers only (L707-708), so
nothing changes on this side.

---

## Part 2 of the report — the `other` rows

### redacteur B.8 — the *existing* mark, "still stated as fact"

Verdict: wrong
No decision.

Cited: convertisseur.md L115 — "Dependencies | The references marked
*existing*"; L121-122 — "dependencies are the references a block marks
*existing*". What L223-226 states is what the convertisseur does.

### redacteur D.4 — a decision invocation 3 cannot place

Verdict: confirmed
Decision: Give invocation 3 the blocking file as the route move 4
would take — a decision it cannot place or read goes into
`blocked_redacteur.md`, Invocation 3, never into a flag in the copy
and never into a questions file.
Where: redacteur.md L262-266 ↔ redacteur.md L703-705, L474-495 ↔
fusion.md L42-43
Owner: redacteur
Also in: —

Cited: fusion.md L42-43 — rows 2 and 3 read a `blocked_*.md`; no row
reads a redacteur questions file, and L262-264 forbids one at
invocation 3. Move 4 (L474-482) writes a flag that "halts everything
downstream" (L493) — in the copy, the Fusionneur would carry it into
the global. Depends on F16 (the `## Invocation` heading).

### redacteur D.7 — a block created at pass a row 3 has no `Global:`

Verdict: confirmed
Decision: Send a block created at pass a row 3 through moves 2 and 3
— index lookup, `Global:` line when the same-trigger test says yes —
as a pass-d block is.
Where: redacteur.md L598 ↔ redacteur.md L442-458, L650-651
Owner: redacteur
Also in: —

L598 — "It becomes a block of its own, with an empty `Genre:` and an
empty `Nature:`" — names no `Global:`; L650-651 applies the four moves
to pass d only.

### redacteur D.9 — the readers of the markers, listed short

Verdict: confirmed
Decision: Name the qualifieur and the classeur among the readers of
the markers at L116 and L323-325, as L71-73 already does.
Where: redacteur.md L116, L323-325 ↔ redacteur.md L71-73 ↔ 3b_nature.md
L98
Owner: redacteur
Also in: —

Cited: 3b_nature.md L98 — "`grep '^### .*MODIFIED'` | The blocks
changed last turn, whose nature may have moved with them".

## Part 2 of the report — the `open` rows

C18, B.2, B.6, D.1 · note, D.14, D.15, D.16, D.17 carry no text in
the report and their source is outside this plan's reading list. Not
judged here; they stand as the report leaves them.

---

## To settle

### redacteur F19 — a block created at invocation 3, and its `Nature:`

A subject no title covers, brought by a decisions file at invocation 3,
becomes a block with an empty `Nature:` (L455, L703-705); no classeur
runs after `/fusion`, and the fusionneur keeps `Nature:` lines in the
global (fusionneur.md L386-387).

| Option | Cost |
|---|---|
| The redacteur creates no block at invocation 3 — a decision with no block to land in goes to `blocked_redacteur.md` (D.4's route) | A `/fusion` stop for every such decision; the Product Owner names the block |
| The block enters the global with an empty `Nature:` | The global carries a block with no nature, for whoever reads that line there |
| The fusionneur drops an empty `Nature:` line at merge | A fusionneur rule; the global then carries blocks with and without the line |

Decision: —

### redacteur F01 — the residual gap the `## Relevé` clause aimed at

With the line on `## Tranché` alone, a term never questioned — present
in `## Relevé` only — rendered in English by the redacteur has no
recorded rendering; the lexicographe's compare (lexicographe.md
L464-466) cannot catch a second English rendering brought by a later
answer. The index asked for `## Tranché` alone, and this plan applies
it; whether the gap is worth a lexicographe change is not this plan's.

| Option | Cost |
|---|---|
| Leave it — `## Tranché` alone, as the index asks | A second English rendering of an unquestioned term goes uncaught |
| The lexicographe defines a sub-line under `## Relevé` and preserves it across rebuilds | A lexicographe change on two rules (L162-166 shape, L285-287 rebuild); the redacteur then writes there too |

Decision: —
