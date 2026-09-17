# Plan — assembleur

Built against `.claude-new/agents/assembleur.md` and the one command
that invokes it, `.claude-new/commands/4_grille.md`. The six thematic
reports carry no finding naming the assembleur — the single hit
(`passages-amont.md` L18) is in the *sound* list.

Ten findings, ten `confirmed`. None is stale, none is wrong: every
cited line reads today as the report describes it. Severities are kept
as reported. Two pairs interact — F03/F10 share L146-147, and F06's
fix removes the practical risk F04 describes — and their decisions are
written to hold together.

---

### assembleur.md F01 — the never-dropped rule, stated three times

Verdict: confirmed
Decision: State the never-dropped rule once, in the merge test, and
have the Role line and the forbidden line point at the gap, not at the
reading that raised it.
Where: assembleur.md L20-22, L44-46, L230-233 ↔
docs/refonte/passes/assembleur.md L110-115
Cited: passes/assembleur.md L110-115 — "one reading, stated once: the
file a question came from is not part of the test; […] the forbidden
line should say "a gap raised once", not "a sondeur alone"."
Cited: assembleur.md L44-46 — "Drop a question because only one
reading raised it — 📌 two questions of one reading that one answer
closes are still one question"
Owner: assembleur
Also in: —

The rider makes the three statements consistent, so nothing is wrong
today — the NOTE stands at NOTE. What C3 asked and did not get is the
single statement.

---

### assembleur.md F02 — a rule the index does not carry

Verdict: confirmed
Decision: Add the rule "a blocked run writes no questions file, not
even an empty one" to the `assembleur.md` index table in
`docs/refonte/modifications.md`.
Where: docs/refonte/modifications.md L517-525 ↔ assembleur.md L57-59,
L270-271
Cited: modifications.md L517-525 — seven rows: *La règle de
départage · Une question multi-blocs · La forme d'entrée · Ce qui
l'arrête · Ses outils · Le `## Merge` · `commands/4_grille.md`* — none
names the questions file a blocked run does not write.
Cited: assembleur.md L57-59 — "A blocked run writes that file and
nothing else — ⚠️ no questions file, not even an empty one."
Owner: assembleur — the same hand that applies this plan; the target
is a record file, not an agent file
Also in: —

---

### assembleur.md F03 — a heading is both *empty* and *a stop*

Verdict: confirmed
Decision: Define *empty* by the one test (no `### Q`, no prose) and
restrict the stop's example to a `### Q` heading that lacks its lines,
so that no file matches both.
Where: assembleur.md L146-147 ↔ assembleur.md L158-159
Cited: L146-147 — "An empty file is a file with no `### Q` and no
prose — 🔴 a heading, a blank line, nothing else."
Cited: L158-159 — "A file that is neither empty nor a list of
questions in that shape — 📌 a sondeur's prose, a heading with no entry
under it."
Owner: assembleur
Also in: —

TO FIX stands: the word *heading* names a file title on one line and a
`### Q` entry on the other, and a file holding only a title is empty
under L146 and a stop under L159. Apply together with F10, which
touches the same L146-147.

---

### assembleur.md F04 — a missing file has no defined outcome

Verdict: confirmed
Decision: Make a missing input file a stop that writes no
`blocked_assembleur.md` and no questions file — the report names the
file — and give `4_grille.md` the relay row for it.
Where: assembleur.md L32-33 ↔ assembleur.md L54, L83-85 ↔
4_grille.md L400-408
Cited: L32-33 — "A file that is missing stops you — 📌 say which."
Cited: L83-85 — "A question you cannot place, a file out of shape —
those are the two stops of PART 3, and they are what you block on. 🔴
You block only when merging is impossible."
Cited: 4_grille.md L408 — "No blocking file either | 🔴 Stop — 📌 say
which reading produced nothing, and to run `/4_grille` again"
Owner: assembleur
Follows: 4_grille — its *Once it has reported* section gains the row
"the assembleur reports a missing file → stop, say which, `/4_grille`
again", on the model of L408
Also in: —

Why not a blocking file: its `## Decision` is where the Product Owner
answers, and a missing input is an orchestration fault, not hers to
settle — the L494 resume ("the merge alone runs, on the four files
still standing") could not even run on it. NOTE stands at NOTE:
`4_grille.md` L400 checks existence before invoking, and F06's fix
closes the one path that reaches this case today.

---

### assembleur.md F05 — resuming on a question that cannot be placed

Verdict: confirmed
Decision: On resume, take the `Block:` value from the blocking file's
`## Decision`, merge the question as if it carried that line, and have
`## To resume` ask for that value — settled by `decisions.md`.
Where: assembleur.md L87-90 ↔ assembleur.md L155-156, L190, L259-260
Cited: L87-88 — "A blocking file the prompt names carries a filled
`## Decision` — 🔴 it says what was settled, and you resume with it."
Cited: L190 — "you may not edit a `Block:` line to merge them."
Cited: L259-260 — "Everything else is copied as written — ⚠️ you
rephrase nothing"
Cited: decisions.md L13-20 — "The decision carries the value of the
`Block:` line, and the agent writes it. […] L190 forbids editing a
`Block:` line *to merge two questions* — not writing one the decision
gives you. […] `## To resume` asks for the value, not for an opinion."
Owner: assembleur
Also in: —

The carve-out has to reach L259-260 as well as L190: the copied-as-
written rule is the second line a reader would hold against writing
that value.

---

### assembleur.md F06 — the blocking file named without its path

Verdict: confirmed
Decision: Name the blocking file by its full path in the assembleur
prompt, as every sondeur prompt does.
Where: 4_grille.md L423 ↔ 4_grille.md L52, L322 ↔ assembleur.md L4,
L54, L99-100
Cited: 4_grille.md L423 — "<Plus: blocked_assembleur.md, its decision
is filled.>" under the header L417 "Merge, in
docs/features/<name>/cadrage-produit/:"
Cited: 4_grille.md L52 — "`blocked_assembleur.md`, at the feature
folder's root | The assembleur"
Cited: 4_grille.md L322 — "<Plus:
docs/features/<name>/cadrage-produit/blocked_par-bloc.md, its decision
is filled.>"
Cited: assembleur.md L4 — "tools: Read, Write"
Owner: 4_grille
Follows: assembleur — none of its text changes; L54 "in the feature
folder" already matches L52
Also in: —

TO FIX stands: with no Glob, a read under `cadrage-produit/` fails,
and L32-33 turns a filled decision into a missing file.

---

### assembleur.md F07 — the merge-alone exception in the wrong tense

Verdict: confirmed
Decision: State the exception in the tense of the turn about to run —
a turn resuming on `blocked_assembleur.md` — and have it cover every
previous-turn `cadrage-produit/` file, not "four".
Where: 4_grille.md L197-198 ↔ 4_grille.md L63-71, L200-206, L494
Cited: L197-198 — "Not on a turn that re-ran the merge alone — 🔴
those four files are what it just read, and filing them would take
them from under it."
Cited: L200-206 — "Otherwise, the previous turn's six
`cadrage-produit/` files: git mv …/par-bloc.md …/closed/par-bloc-NN.md
📌 The same for `par-question.md`, `par-nature.md`, `global.md`,
`releve.md` and `questions.md`."
Cited: L64-65 — "The assembleur's → the merge alone, on the four files
still standing"
Owner: 4_grille
Also in: —

TO FIX stands: L66-71 ("leave them in place, do not file them") is
written for a sondeur's resume, so L197 is the only line guarding the
assembleur's, and it reads as past. The six-file `git mv` also names
`releve.md`, which the exception's "four" would let through.

---

### assembleur.md F08 — five names, six rows

Verdict: confirmed
Decision: Make the announced count match the table.
Where: 4_grille.md L41 ↔ 4_grille.md L47-52
Cited: L41 — "Five names, one per invocation this command runs"
Cited: L47-52 — six rows: `blocked_par-bloc.md`,
`blocked_par-question.md`, `blocked_par-nature.md`, `blocked_global.md`,
`blocked_existant.md`, `blocked_assembleur.md`
Owner: 4_grille
Also in: —

---

### assembleur.md F09 — what four empty files close

Verdict: confirmed
Decision: Correct the claim to what four empty files actually end —
the first time's loop, never the product file.
Where: assembleur.md L36-37 ↔ 4_grille.md L496, L498
Cited: assembleur.md L36-37 — "Every file empty is how the grid says
the product file is closed."
Cited: 4_grille.md L496 — "First time — its questions file is empty |
📌 `/4_grille` again — 🔴 the second time runs"
Cited: 4_grille.md L498 — "Second time — it is empty, or had already
run | 📌 `/5_reclasse` — 🔴 the product file is closed"
Owner: assembleur
Also in: —

---

### assembleur.md F10 — an empty file the producer never writes

Verdict: confirmed
Decision: Drop the "a heading, a blank line" gloss and keep the test
alone, so that the zero-byte file the sondeur writes is the empty file
the assembleur counts.
Where: assembleur.md L146-147 ↔ sondeur.md L376-379, L447-448
Cited: sondeur.md L376-379 — the output shape is `### Q1 / Block: B7 /
Question: … / Answer:` and nothing above it
Cited: sondeur.md L447-448 — "Write the file even with no question in
it — 📌 its absence would read as *this sondeur did not run*."
Owner: assembleur
Also in: — (the sondeur's side is an unspecified empty file; whether
the sondeur plan carries a twin was not checked — its report is
outside this plan's reading list)

Same lines as F03: one edit serves both.

---

## To settle

Nothing. No finding turns on intent, scope or user-facing behaviour:
F04 and F05 were the two that could have, and F05 is settled by
`decisions.md` while F04 is orchestration mechanics whose one
defensible outcome is given above.
