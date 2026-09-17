# Plan — `detailleur.md`

Built against `.claude-new/agents/detailleur.md`, the four commands that
name the agent (`8_code.md` — the only one that invokes it; `cycle.md` L82,
`audit_blocages.md` L105 and L156, `audit_conventions.md` L92 — each names
it once, none invokes it), `docs/verification2/detailleur.md` (both parts),
`docs/verification2/decisions.md`, and the lines of the six thematic
reports that name the Détailleur (`renommages.md` F01, F02, F04, F06, F07,
F16 · `chemins-aval.md` F03, F10, F20, F23 · `passages-aval.md` F01, F02,
F05, F10, F11, F15; `fichiers.md`, `chemins-amont.md` and
`passages-amont.md` name it nowhere).

Every cross-file line quoted below was opened in `.claude-new/`. Findings
F01-F10 cite the index, `docs/refonte/modifications.md` L1013-1082, and the
pass file `docs/refonte/passes/detailleur.md`; those ranges were opened too.

`docs/verification2/plans/concepteur.md` existed when this plan was
written and decides `passages-aval.md` F01 / `renommages.md` F02 (the
`## Files` field) the same way this plan does — see F20 below.

**Settled questions applied here, not reopened:**

- `passages-aval.md` F15 — every reader matches the `PASS` prefix; the
  Détailleur is one of the five readers named. Applied at F15 below.
- `renommages.md` F16 — the Concepteur writes an `architecte/` request like
  the Détailleur. Nothing of the Détailleur moves; entry below for the
  record.
- `cadreur.md` F23 — `cycle.md` is deleted, every mention of `/cycle` goes.
  `cycle.md` L82 ("A `blocked_detailleur`, `_realisateur` or `_relecteur`
  → STOP") disappears with the file. `detailleur.md` mentions neither
  `/cycle` nor `cycle.md` (grep: no hit). Nothing to do here.

---

## Part 1 — the index (`docs/refonte/modifications.md`)

The index's `detailleur.md` section (L1013-1082) records one modification,
U10, and the pass (18 passed, 3 deferred, 0 dropped). It names none of the
five refonte additions F01-F05 list. Each was checked in the file.

### detailleur.md F01 — `## Files` absent from the index

Verdict: confirmed
detailleur.md L244-248 show the field in the sheet's shape; L259-265 carry
its rule ("`## Files` carries the lot's `Modifies` and `Touches`…"). The
index's section (L1013-1082) has one row, U10, and the pass table; no word
on `## Files`.
Decision: Add the field to the index's `detailleur.md` section, with the
rule F20 settles for it (the index records the field as it will read, not
as it reads today).
Where: modifications.md L1013-1082 ↔ detailleur.md L244-248, L259-265
Owner: the index — a record, not an agent; no line of `detailleur.md` moves
for this
Also in: —

### detailleur.md F02 — move 9's `spécifique` / `permanente` split

Verdict: confirmed
detailleur.md L638-646: "Every rule … marked `spécifique` that bears on
what this lot touches … Never a `permanente` one". modifications.md L638
names the mark in the Architecte's section ("`permanente` ou `spécifique`
sur chaque règle"); the Détailleur's section says nothing of what move 9
does with it.
Decision: Record in the index's `detailleur.md` section that move 9 names
the `spécifique` rules only, the `permanente` ones being read whole by the
Réalisateur.
Where: modifications.md L1013-1082 ↔ detailleur.md L638-646
Owner: the index
Also in: —

### detailleur.md F03 — the empty-body row

Verdict: confirmed
detailleur.md L109: "A production that exists **with an empty body** — Not
a contradiction — a concepteur declared it before the block came back from
a redécoupage". Absent from the index's section.
Decision: Record the row in the index — it is the Concepteur's existence
reaching the Détailleur's contradiction table, a cascade of the refonte.
Where: modifications.md L1013-1082 ↔ detailleur.md L109
Owner: the index
Also in: —

### detailleur.md F04 — the `Not settled here.` row

Verdict: confirmed
detailleur.md L438 carries the row; the index does not. But F22 below
shows the row never fires for a Détailleur file and removes it.
Decision: Nothing to record once F22 removes the row; if F22 is not
applied, record the row.
Where: modifications.md L1013-1082 ↔ detailleur.md L438
Owner: the index — after F22
Also in: —

### detailleur.md F05 — the `desc-bug.md` rule of move 3

Verdict: confirmed
detailleur.md L558-560: "A `desc-bug.md` has none — the terms are the
feature's, already in the code. A signature never renames what the feature
already calls something." Absent from the index's section.
Decision: Record the rule in the index.
Where: modifications.md L1013-1082 ↔ detailleur.md L558-560
Owner: the index
Also in: —

### detailleur.md F06 — C1 applied differently from what the pass asked

Verdict: confirmed
passes/detailleur.md L60-62 asked for "one rule: a settled file is renamed
to its numbered form and never deleted" — on the agent's side. The file
says the opposite of who does it: detailleur.md L443-444 "You never rename
it — you have no tool that removes a file. The orchestration does it, once
you have reported"; and 8_code.md L170-173 carries the rename ("The rename
is yours, never the agent's — none of the five has a tool that removes a
file"). The design as it stands is coherent (the agent's tools, L4, include
neither Bash nor a rename); only the index's "passed" is inexact.
Decision: Record in the index that C1 was met by moving the rename to the
orchestration (8_code move 4b), not by the agent-side rule the pass asked
for.
Where: passes/detailleur.md L50-66 ↔ detailleur.md L443-444, 8_code.md
L170-173
Owner: the index
Also in: —

### detailleur.md F07 — "two of three" in the index, "one of three" in the file

Verdict: confirmed
modifications.md L1038: "deux de ses trois causes de blocage n'apparaissent
qu'au grep". detailleur.md L460: "One of your three block causes shows only
in a grep". Neither count survives F14, which realigns the file's
enumeration with move 4's stop table.
Decision: Bring the index's C4 line to whatever count F14 leaves in the
file.
Where: modifications.md L1038 ↔ detailleur.md L460
Owner: the index — after F14
Also in: —

### detailleur.md F08 — C8 half applied: the forward reference stays

Verdict: confirmed
The report's citation is off: the C8 comment sits at passes/detailleur.md
L214-234 (L237-252 is the next comment, on the code folders). C8 asked:
"move 4 names two greps per symbol … ; move 2 loses its forward reference"
(L229-231). Move 4 has the two greps (detailleur.md L580-581 "And grep it
on `docs/CURRENT_TECHNICAL_STATE.md` too — two greps per symbol, not
one"); move 2 still reads (L546-547) "Those two only — the rest of that
file you grep, symbol by symbol".
Decision: Drop the forward reference at move 2; move 4 carries the rule.
Where: passes/detailleur.md L214-234 ↔ detailleur.md L546-547, L580-581
Owner: detailleur
Also in: —

### detailleur.md F09 — C17 passed, and `## Files` shows three `.kt` paths

Verdict: confirmed
passes/detailleur.md L416-436 (C17): "the same three rows with neutral
shapes"; the signature table at detailleur.md L152-156 was neutralised, and
the `## Files` example added later (L246-248) reads
`activity/ActivityReconciliationService.kt`, `activity/ActivityEntry.kt`,
`ActivityReconciliationServiceTest.kt`.
Decision: Apply C17 to the `## Files` example — paths with no platform
extension, or the rule alone (F20 rewrites this example's content anyway).
Where: passes/detailleur.md L416-436 ↔ detailleur.md L246-248
Owner: detailleur
Also in: —

### detailleur.md F10 — C19, C20, C21 deferred, and applied in `8_code.md`

Verdict: confirmed
modifications.md L1027-1031: the three deferred "à passer avec A3". The
three changes are in 8_code.md: L103-106 "The test is on the lot, never on
the block" (C19); L395-397 "A Détailleur reporting that its block waits on
the split — `code/redecoupage.md` still there → run `/7_lots`; gone → the
blocking file was never closed" (C20); L12-14 "It never invokes the
Contrôleur" (C21).
Decision: Mark the three applied in the index, through `8_code.md`.
Where: modifications.md L1027-1031 ↔ 8_code.md L103-106, L395-397, L12-14
Owner: the index
Also in: —

---

## Section 2 and 3 — the file against itself

### detailleur.md F13 — "five fields", six shown

Verdict: confirmed
L221-222: "one per lot of the block — five fields". The shape L224-257
shows `## Signatures`, `## Acceptance criteria`, `## Dependencies`,
`## Files`, `## Conventions`, `## Requests` — six.
Decision: Make the count match the shape (six), or drop the count.
Where: detailleur.md L221-222 ↔ L224-257
Owner: detailleur
Also in: —

### detailleur.md F14 — three block causes, and move 4 orders more stops

Verdict: confirmed
L288-290 enumerate three: "an ambiguous rule … a grep that contradicts the
lot's declaration … a missing input". Move 4 adds: L571-574 "The
conventions name no code folder — you block"; L590 "Not found, and a lot of
an earlier block was to produce it — You block"; L592 "Not found, and none
of the above — Stop. The lot list is wrong, or the sequence put this block
too early". L460 counts "One of your three block causes shows only in a
grep" — at least three do (L103, L590, L592).
Decision: Make the enumeration at L288-290 and the count at L460 agree
with move 4's stop table — every stop the agent may take is in the list,
and the number said to show only in a grep is the number the table gives.
Where: detailleur.md L288-290, L460 ↔ L103, L571-574, L590, L592
Owner: detailleur
Also in: — (F07 follows in the index)

### detailleur.md F15 — divergence mode runs moves 3-9 with no entry opened

Verdict: confirmed
L525-526: "Moves 1 and 2 run once, in the walk — moves 3 to 9 run per lot
of the block." L680-681: "The walk — No — the coded lot's code is the
ground, not the entries; Moves 3 to 9 — On the named lots only." Move 3
(L552) works "for each rule those entries describe"; move 7 (L628) writes
the criteria; move 2's two state sections are read in the walk only
(L541-542). In divergence mode nothing opens the entries and nothing reads
the traps.
Decision: In divergence mode, run moves 1 and 2 on the named lots before
moves 3-9 — the code is the ground for the signature, the entries stay the
ground for the criteria.
Where: detailleur.md L525-526 ↔ L680-681, L552, L628
Owner: detailleur
Also in: —

### detailleur.md F16 — a partially filled `## Decision` has no PART 2 row

Verdict: confirmed
L346: "Some numbers answered, others not — Apply the answered ones — stop
on the entries they do not cover." PART 2 L434-441 has rows for "still
empty", "`Not settled here.`", "filled", "filled + sending back" — none for
a number left empty. Cited: arbitre.md L165-167 — "A number with no answer
is an entry still waiting — that is how a product question holds up one
entry and not the file. Never write a placeholder under it: an empty number
is the signal." And 8_code.md L170: rename "once the agent reports having
applied it".
Decision: Add the PART 2 row — a `## Decision` with a number left empty is
a standing block: apply the answered numbers if they were not (their lots
carry a sheet after the first application, and the ordinary skip covers
them), stop on the rest, and report which numbers wait and that the file is
not to be renamed. The orchestration renames only on a report that every
number was applied.
Where: detailleur.md L346 ↔ L434-441, arbitre.md L165-167, 8_code.md L170
Owner: detailleur (the row and the report line)
Follows: 8_code — the rename in move 4b keys on "every number applied",
never on "applied"; arbitre — nothing, its signal stands
Also in: arbitre.md (renommages F07, passages-aval F11), commandes.md
carries nothing of this (an agent is named)

### detailleur.md F17 — "You never block on this" beside its exception

Verdict: confirmed
L378-379: "You never block on this. Write the signature against the
conventions as they stand, and carry on." L576-578: "That is the one
conventions request you block on — every other one you write and carry
on". The exception is stated once, at move 4, and the general rule is left
whole.
Decision: Qualify the rule at L378 with the one exception move 4 names.
Where: detailleur.md L378-379 ↔ L571-578
Owner: detailleur
Also in: —

### detailleur.md F18 — `Settle <lot>` on a call that settles a block's file

Verdict: confirmed
L330: `description="Settle <lot>"`; L332: `Blocking file:
code/blocked_detailleur.md` — one file per block, one `## Blocking N` per
lot (L473-475).
Decision: The description names the block.
Where: detailleur.md L330 ↔ L332, L473-475
Owner: detailleur
Also in: —

### detailleur.md F19 — a filled decision on an unnamed lot: leave, or apply

Verdict: confirmed
L668-670: "A filled decision on a lot the prompt does not name — leave it:
you rewrite only the named ones, and the next ordinary run applies it."
L679: PART 2 runs in divergence mode ("Yes — a standing block is still a
block"). L439: "A `## Decision` filled — Apply it, and say in your report
that you did — the orchestration renames the file." The two rows read the
same file the same run.
Decision: Qualify PART 2's "filled" row for divergence mode — apply only a
decision bearing on a lot the prompt names; leave the others and say in the
report that they were not applied, so move 4b does not rename.
Where: detailleur.md L668-670 ↔ L439, L679
Owner: detailleur
Follows: 8_code — L188 puts `code/blocked_detailleur.md` in the divergence
prompt "its decision is filled"; the rename after that call waits for a
report saying the decision was applied, which this mode may not give
Also in: —

### detailleur.md F11 — `Edit` granted, no gesture names it

Verdict: confirmed
L4: `tools: Read, Grep, Glob, Edit, Write, Agent`. Every production is a
Write (L55, L284, L366); the only mention is the failure section L415-421.
Divergence mode (L682, L684-685) rewrites lines shared across sheets —
"a symbol two sheets share is rewritten the same way in both" — which is
the one gesture an Edit fits.
Decision: Keep `Edit` and bound it: the sheets of the lots a divergence
prompt names (and, after F21, the sheet a `Cause: sheet` prompt names);
everything else is a Write.
Where: detailleur.md L4 ↔ L415-421, L682-685
Owner: detailleur
Also in: —

### detailleur.md F12 — the verdict's `## Status` line, and the tool that reads it

Verdict: confirmed
L45: "a lot's verdict — `code/<lot>/verdict.md` — its `## Status` line, to
know a lot is coded". L467-468 key on it. No gesture names how; a Read
opens `## Findings` (relecteur.md L138-142 puts it in the same file), which
8_code.md L201-202 keeps from itself for the same reason. `What you read`
(L60-89) does not list the verdict at all (report D-3, below).
Decision: Name the gesture — a Grep of `## Status` on `code/<lot>/verdict.md`
with its following line, never a Read — and list the verdict in `What you
read` with that restriction.
Where: detailleur.md L45, L467-468 ↔ L60-89
Owner: detailleur
Also in: —

---

## Section 4 — against the other files

### detailleur.md F20 — `## Files` from `Modifies`, which carries no file

Verdict: confirmed — BLOCKING holds
L259-262: "`## Files` carries the lot's `Modifies` and `Touches`, copied
from `code/decoupage.md` — one path per line"; L265: "A dash when the lot
creates everything it touches."
Cited: cadreur.md L753-754 — "`Needs`, `Produces` and `Modifies` carry
symbols, and symbols only. A name the code carries — never a file."
cadreur.md L749-750 (example lot-01): `Modifies: —`, `Touches: —`.
Cited: concepteur.md L57-58 — "its `## Files` names every file the lot
owns: where each declaration goes"; L186-187 — "The sheet's `## Files`
narrows it — a symbol goes in one of those files"; L112-115 — "Touch a file
the sheet's `## Files` does not name … then name it in `## Outside the
lot`". testeur.md L58-59 — "its `## Files` names every file the lot owns:
where your tests go". realisateur.md L189-191 and relecteur.md L386-388 —
`## Outside the lot` is every file `## Files` does not name.
So the field can hold at most `Touches`, is a dash on every production lot,
and every file the lot creates is "outside the lot" for four readers.
Decision: `## Files` names every file the lot owns, built by the Détailleur
— for each `Modifies` symbol the file move 4's grep found it in; each
`Touches` path as given; for each `Produces` symbol, and for the test file
of the lot's criteria, the file the conventions place a symbol of that kind
in (a rule the Architecte marks `permanente`, architecte.md L150-152, and
the Détailleur reads the conventions whole, L77-80). A placement the
conventions leave unsettled takes the Détailleur's existing route (an
`architecte/` request, L366-380, carry on) and the file of the symbol it
depends on most, named as such in `## Requests`. The dash at L265 goes: a
lot always owns a file. L401-402 ("Decide where the code goes — the
Réalisateur does") goes with it — placement is read from the conventions
by the Détailleur, and the Concepteur picks within `## Files`.
Same decision as `plans/concepteur.md` passages-aval F01.
Where: detailleur.md L259-265, L401-402 ↔ cadreur.md L753-754,
concepteur.md L57-58, L112-115, L186-192, testeur.md L58-59, realisateur.md
L189-191, relecteur.md L386-388
Owner: detailleur (writes the field)
Follows: concepteur — L186-192 hold once the list is complete; its
fallback (L189-192) applies only to a symbol `## Files` cannot hold, which
renommages F16 reworks anyway; cadreur — nothing, `Modifies` stays
symbols; testeur, realisateur, relecteur — their `## Files` tests hold as
written once the field is complete; each re-reads its own line against the
new definition
Also in: cadreur.md, concepteur.md, testeur.md, realisateur.md,
relecteur.md

### renommages.md F01 — same field, the symbol/path mismatch

Verdict: confirmed
Same lines (detailleur.md L259 ↔ cadreur.md L753).
Decision: As F20.
Where: detailleur.md L259 ↔ cadreur.md L753
Owner: detailleur
Also in: cadreur.md

### renommages.md F02 · passages-aval.md F01 — same field, the dash

Verdict: confirmed
Same lines (detailleur.md L265 ↔ concepteur.md L186; passages-aval adds
testeur.md L58-59, realisateur.md L189-190, relecteur.md L386-388).
Decision: As F20.
Where: detailleur.md L259-265 ↔ concepteur.md L186-190
Owner: detailleur
Also in: concepteur.md, testeur.md, realisateur.md, relecteur.md,
cadreur.md

### renommages.md F04 — "the sheet does not declare", spliced

Verdict: confirmed
realisateur.md L189-191: "`## Outside the lot` names every file you wrote
in that the sheet's `## Files` does not name — ⚠️ the sheet does not
declare, and what you did to it — or a dash." Two half-rules in one
sentence. detailleur.md L261-262 quotes the readers' phrase — "without this
field, « a file the sheet does not declare » is every file" — and holds
once the readers say it one way.
Decision: The Réalisateur states one rule, keyed on `## Files`; the
Détailleur's quotation at L261-262 follows the wording the readers keep.
Where: realisateur.md L189-191 ↔ detailleur.md L261-262
Owner: realisateur
Follows: detailleur (L261-262, the quoted phrase)
Also in: realisateur.md

### detailleur.md F21 · passages-aval.md F02 · chemins-aval.md F03 — `Cause: sheet` reaches no Détailleur

Verdict: confirmed — passages-aval's BLOCKING holds
Cited: relecteur.md L167-169 — "`sheet` says the fault is upstream: the
block goes back to the Détailleur, never to a fresh Réalisateur"; L405-407
— "a sheet with no criteria is a `FAIL structurel`, `Cause: sheet` … The
orchestration sends the block back to the Détailleur." 8_code.md L138: "On
FAIL → a fresh `realisateur`" — no row on `## Cause`; the Cause-reading at
L42 serves escalation only (L159-162). detailleur.md L467-468: a lot with a
sheet and no PASS is skipped; divergence mode (L659-662) fires on
`## Symbol divergences` only (8_code.md L177-179). realisateur.md L519: the
FAIL table has `mineur` and `structurel`, nothing on the cause.
Decision: The loop routes a FAIL whose `## Cause` is `sheet` to the
Détailleur, not to a fresh Réalisateur — counted as an attempt like any
FAIL — and the Détailleur gets a prompt form that names the lot whose
sheet the review found false: on it, the skip of L467-468 does not apply,
moves 1-9 run on that lot from the entries, and the agent reads that lot's
`verdict.md` `## Findings` lines (the only time it reads more than
`## Status`) to know what the review found. The sheets of the other lots
stay as they are.
Where: relecteur.md L167-169, L405-407 ↔ 8_code.md L138, detailleur.md
L467-468, L659-662, realisateur.md L519
Owner: 8_code (the route is the loop's move 4)
Follows: detailleur — the prompt form and what it runs on it; relecteur —
L168-169 and L407 say what the orchestration does, and say it the way
8_code does it (the lot's sheet goes back, not "the block"); realisateur —
L519's table says a `Cause: sheet` FAIL never reaches it; concepteur and
testeur — their skip on `conception.md` / `tests.md` (8_code.md L112-113)
must not skip a lot whose sheet was rewritten; see `## To settle` for the
declarations and tests already committed against the false sheet
Also in: relecteur.md, realisateur.md, concepteur.md, testeur.md;
commandes.md carries nothing of this (agents are named)

### detailleur.md F22 — the `Not settled here.` row never fires

Verdict: confirmed
detailleur.md L438: "A `## Decision` reading `Not settled here.` — Nothing
was settled — the Arbitre says whose it is: stop, and relay that line."
Cited: arbitre.md L147-153 — "When a block is not yours — a Relecteur's or
an Architecte's — say so in `## Decision` and stop: `Not settled here.
<whose it is, and why>`"; L249-251 — "`detailleur` — ✅ It calls you;
`realisateur` — ✅ It calls you". A Détailleur file is always the Arbitre's;
the phrase is never written on one. A product question leaves the number
empty instead (arbitre.md L165-167).
Decision: Remove the row; PART 2 keeps "still empty" (a number or the whole
field) as the case where nothing was settled. realisateur.md L505 carries
the same dead row — not named by this finding, flagged for its plan.
Where: detailleur.md L438 ↔ arbitre.md L147-153, L249-251
Owner: detailleur
Also in: — (chemins-aval F20 below, same phrase seen from 8_code)

### chemins-aval.md F20 — 8_code re-invokes on a decision that is not filled

Verdict: confirmed
8_code.md L50-51: "Whether its `## Decision` is filled, nothing more of
it"; L167-170: empty → stop, filled → name it and rename after "applied".
A number left empty (arbitre.md L165) reads as filled; the Détailleur is
re-invoked on opus and stops at L346 / the F16 row every run. The
`Not settled here.` half falls with F22.
Decision: 8_code counts the numbered answers under `## Decision` against
the `## Blocking N` headings of `code/blocked_detailleur.md`; a heading
with no answer is a standing block — stop and relay, never invoke.
Where: 8_code.md L50-51, L167-170 ↔ arbitre.md L165-167, detailleur.md
L346, L434-441
Owner: 8_code
Follows: detailleur — F16's row and report line are what the command
relies on when it did invoke
Also in: arbitre.md; commandes.md carries nothing of this

### renommages.md F07 · passages-aval.md F11 — the half-answered file archived as settled

Verdict: confirmed
Same lines as F16 and chemins-aval F20 (arbitre.md L165-167 ↔ 8_code.md
L167-170, detailleur.md L346, L434-441).
Decision: As F16 (the Détailleur's row and report) and chemins-aval F20
(the command's count); the Arbitre's signal stands.
Where: arbitre.md L165-167 ↔ detailleur.md L346, L434-441, 8_code.md
L167-170
Owner: detailleur for its row, 8_code for its test
Also in: arbitre.md

### renommages.md F06 — the Arbitre's single-entry shape never arrives

Verdict: confirmed
Cited: arbitre.md L129-130 — "`##` in a single-entry file, `###` under
each `## Blocking N` in a multi-entry one." detailleur.md L292-293: "one
`## Blocking N` per stop, even when there is only one"; the shape at
L295-307 puts `###` under it. realisateur.md L258-268: the same rule and
the same shape.
Decision: The Arbitre drops the single-entry shape — every file it reads
carries `## Blocking N` with `###` beneath, one entry or several.
Where: arbitre.md L129-130 ↔ detailleur.md L292-307, realisateur.md
L258-268
Owner: arbitre
Follows: — (the two writers already write the one shape)
Also in: arbitre.md, realisateur.md

### passages-aval.md F05 — a file at `code/` read as bearing on the split as a whole

Verdict: confirmed
Cited: arbitre.md L84-86 — "In the split's own folder — the block bears on
the split as a whole, and no lot exists yet. In a lot's folder — it bears
on that lot"; L97-98 — "The lot's sheet and report — only when the block
bears on a lot". detailleur.md L284-285 files at "the split's root, not
under a lot"; L295 heads each entry `## Blocking 1 — lot-04`. The lots
exist (the walk runs on a cut sequence, L62-63), and a lot in the block can
carry a sheet the Arbitre would need — L353-355 (sheets written before a
move-4 stop stay) and L468 (a sheet with no PASS, skipped).
Decision: The Arbitre reads a `code/blocked_detailleur.md` as bearing on
the lots its `## Blocking N — lot-NN` headings name, and opens those lots'
inputs where they exist; the Détailleur makes the lot in the heading a
rule, not only the example's shape.
Where: arbitre.md L84-86, L97-98 ↔ detailleur.md L284-285, L292-295
Owner: arbitre (its reading rule)
Follows: detailleur — L292-293 states the `— lot-NN` suffix as mandatory
on every `## Blocking N`
Also in: arbitre.md

### detailleur.md F23 · passages-aval.md F10 — the `## Conventions` example: wrong kind, wrong key

Verdict: confirmed
detailleur.md L252-253: "§3 · a rule needing the platform's ambient handle
is in the wrong module" and "§9 · the name of the rule, not of the
structure"; L652: "`§10 · no hardcoded string`". L644: "Never a
`permanente` one".
Cited: architecte.md L150-152 — "Three kinds are always `permanente` —
where a kind of symbol lives, the commands that compile, analyse and test,
and the states a lot may be delivered in"; L144 — `permanente` fires on
"an identifier written". Module placement and naming are of those kinds;
so is a string rule an ordinary act of writing fires. architecte.md
L131-132 — "a spec sheet cites `R30`, and renumbering would point every
citation at another rule"; relecteur.md L141 — "point 3 — R12, the
identifier is not in English". The sheet keys `§<section>` where the
Architecte and the Relecteur key `R<rule>`.
Decision: The example lines and L652 cite rules by `R<n>`, and show rules
of the `spécifique` kind (a named module, a boundary, a technology —
architecte.md L145). The form is the Architecte's; the Détailleur follows
it.
Where: detailleur.md L250-254, L652 ↔ architecte.md L131-132, L144-152,
relecteur.md L141
Owner: architecte (owns the rule key); detailleur applies it to its example
and its L652 illustration
Follows: relecteur — nothing, it already reports `R12`; passages-aval F10
cites relecteur.md L372-373, which on reading is the "another module red"
rule and carries no `§` — nothing there to move
Also in: architecte.md, relecteur.md

### detailleur.md F24 — `audit_blocages.md` shows the file under a lot

Verdict: confirmed
audit_blocages.md L156: `code/lot-31/blocked_detailleur-01.md`.
detailleur.md L284-285: "at the split's root, not under a lot"; 8_code.md
L170: renamed "at the path it sits at — … `code/` for the detailleur". The
glob at audit_blocages.md L34 (`code/**/blocked_*.md`) still finds it.
Decision: The example reads `code/blocked_detailleur-01.md`.
Where: audit_blocages.md L156 ↔ detailleur.md L284-285, 8_code.md L170
Owner: the command `audit_blocages.md` — no agent line moves
Also in: — (an agent is named, so not `commandes.md`; the command's own
plan, if any, carries it)

### chemins-aval.md F10 — a Relecteur block re-invokes, and stops the lot next pass

Verdict: confirmed
8_code.md L418-422: a Relecteur block naming the sheet missing → "`detailleur`
on the block"; the report → a fresh `realisateur`. Move 4b L169: `## Decision`
empty → stop. relecteur.md L232-234: "You never retire it — the orchestration
does it, once the verdict is written." The rename of 4b fires on "applied"
(L170), which the Relecteur never reports. On the next pass the lot stops on
its own block.
Decision: 8_code retires a `blocked_relecteur.md` when it invokes the agent
its table names on it — the block was acted on, not decided. Nothing of the
Détailleur moves: it is invoked on the block as in move 1.
Where: 8_code.md L169-170, L418-422 ↔ relecteur.md L232-234
Owner: 8_code
Follows: relecteur — L232-234 say when the orchestration retires it, and
say what 8_code does
Also in: relecteur.md, realisateur.md

### chemins-aval.md F23 — the Réalisateur has no "redecoupage.md gone" row

Verdict: confirmed
detailleur.md L440-441: two rows — "`code/redecoupage.md` is still there →
Stop"; "gone → The split was redone — detail the block, and say in your
report that the decision was applied". realisateur.md L500-506: one row,
"still there → Stop", none for gone.
Decision: The Réalisateur gains the row the Détailleur has. Nothing of the
Détailleur moves.
Where: realisateur.md L500-506 ↔ detailleur.md L440-441
Owner: realisateur
Also in: realisateur.md

### passages-aval.md F15 — `PASS with reservation` — settled

Verdict: confirmed
relecteur.md L110: "PASS with reservation — A point passes, but is worth
noting for what follows". detailleur.md L45 "to know a lot is coded" and
L467 "its verdict is `PASS`" read the word, not the prefix.
Decision (settled, decisions.md): the Détailleur matches the `PASS` prefix
on `## Status` — a reserved lot is coded, its sheet is never touched.
Where: detailleur.md L45, L467 ↔ relecteur.md L110
Owner: relecteur (writes the verdict); detailleur applies the prefix rule
at L45 and L467
Also in: relecteur.md, verificateur.md; 8_code and 9_controle through
their agents' plans

### renommages.md F16 — the Concepteur's route to the Architecte — settled

Verdict: confirmed
concepteur.md L193-196: "You write no conventions request — you have no
route to the Architecte." detailleur.md L366-380 is the route the decision
extends to it.
Decision (settled, decisions.md): the Concepteur writes an `architecte/`
request like the Détailleur. Nothing of the Détailleur moves; its request
shape (L366-373) is the model.
Where: concepteur.md L193-196 ↔ detailleur.md L366-380
Owner: concepteur
Also in: concepteur.md; 8_code L112 (the relay line) through the
concepteur's plan

---

## Part 2 of the report — rows left `other`

### detailleur.md D-3 — `What you read` omits the verdict

Verdict: confirmed
L60-89 list eight inputs and close at L86 "Nothing else"; L45 and L467-468
read `code/<lot>/verdict.md`. L672 now says "you read no divergence verdict
file", so the two no longer collide — the omission in the list stands.
Decision: As F12 — list the verdict, restricted to its `## Status` line by
grep (and, after F21, the `## Findings` of the one lot a `Cause: sheet`
prompt names).
Where: detailleur.md L60-89 ↔ L45, L467-468
Owner: detailleur
Also in: —

### detailleur.md D-7 — the lot a walk-time request is filed under

Verdict: confirmed
L571-574: the code-folder block is raised in the walk, "before any lot",
with "write the request and the blocking file". L366: the request is
`architecte/detailleur-<lot>.md`. audit_conventions.md L92 reads the lot
from that name ("the request file carries it in its name,
`architecte/detailleur-lot-04.md`"). No lot is named for a request the
walk writes. L378's "You never block on this" is F17.
Decision: A request written in the walk is filed under the first lot of the
block in the sequence — the whole block waits on it, and the audit's
"coded under the rule as it stood" holds for every lot after.
Where: detailleur.md L571-574, L366 ↔ audit_conventions.md L92
Owner: detailleur
Also in: —

Rows marked `fixed` and `moot` were spot-checked where a finding above
touches them (B-1/D-4/D-5/D-6 at L443-444, C-2 at L571-578, D-2/D-18 at
L460, D-15 at L525-526, D-16 at L668-670, D-17 at L353-355) and hold.

---

## To settle

Not mine — a choice the findings do not make and the settled list does not
cover. `Decision` left empty.

### The declarations and tests committed against a sheet the review found false

F21 sends a `Cause: sheet` lot back to the Détailleur. By then the
Concepteur has committed declarations "exactly the signature the sheet
gives" (concepteur.md L200-201) and the Testeur one test per criterion —
both against the false sheet, both in the code. `plans/concepteur.md`
raises the same question for a re-cut lot ("The declarations of a re-cut
lot, already in the code"); the answer should be one.

| Option | Cost |
|---|---|
| The orchestration deletes `conception.md` and `tests.md` and reverts the lot's commits before re-invoking | Git surgery in `8_code`; the three agents rerun from clean code |
| The orchestration deletes the two reports only; the Concepteur and the Testeur rewrite what they find | Their "declare only what is missing" rules must read a stale declaration as one to rewrite — the opposite of what they say |
| The Détailleur rewrites the sheet against the declarations as committed (divergence-style), not from the entries | Cheapest; wrong by construction — the declarations are what the false sheet produced |

Decision: —
