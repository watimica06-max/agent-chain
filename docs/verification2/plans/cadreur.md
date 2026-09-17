# cadreur — correction plan

Built against `.claude-new/agents/cadreur.md` (973 lines), the three
commands that name it (`7_lots.md`, `cycle.md`, `audit_conventions.md`),
`docs/verification2/cadreur.md` (both parts), `decisions.md`, and the
six thematic reports filtered on `cadreur`. Every line cited below was
opened in this round; the other side of every two-file `Where` is
quoted.

Findings that state one fact under several ids are decided once and
cross-referenced.

---

## The report's findings

### cadreur.md F01 — the never-do list restates rules

Verdict: confirmed — *moves 3 and 4 are not re-run* stands at L266-269,
L309-313, L863-864 and L935-936; the three-round ceiling at L24-27,
L260, L822-823 and L931-932; *do not argue with a defect* at L274,
L828-829 and L852-853.
Decision: State each rule once, in the section that owns it, and make
the never-do list point at that section instead of restating the rule.
Where: cadreur.md L266 ↔ modifications.md L947
Cited: modifications.md L946-948 — "Passés (25) — C1 · C2 · … · C21 ·
C22 · C23 · C24 · C25" (C21 counted as passed).
Owner: cadreur
Also in: —

### cadreur.md F02 — move 6 sends code files into `Modifies`

Verdict: confirmed — L524-525 "Every code file in a symbol's hit list
goes into the lot's `Modifies`, by name"; L753-754 "`Needs`, `Produces`
and `Modifies` carry symbols, and symbols only … never a file".
Decision: Move 6 sends the code files of a symbol's hit list — the
callers the agent knows only by path, since it never opens a file —
into `Touches`, by path; `Modifies` keeps the symbols the inventory
established; the cross-lot check on callers stays the one move 6's
table already makes (L569-573), and `Touches` is redefined as the
files a lot opens without declaring a symbol for them (callers, tests,
manifests).
Where: cadreur.md L524 ↔ modifications.md L962
Cited: modifications.md L962 — "`Modifies` mélangeait trois unités —
symboles, fichiers, lignes de manifeste … 🆕 **Champ `Touches`** pour
les fichiers qui ne déclarent rien".
Owner: cadreur
Follows: detailleur (`## Files`, see F19), verificateur (reads the five
fields; the meaning of `Touches` widens), 9_controle (greps the lot
list — unchanged fields, nothing to rewrite).
Also in: detailleur, verificateur
Weighed against: naming the caller's *symbol* in `Modifies` — it costs
one more grep per caller file (a declaration pattern the conventions
would have to name, per language) and the Détailleur then resolves it
back to a path; the path route costs nothing, the cadreur already holds
it from move 3.

### cadreur.md F03 — `[B?:` comes from no comment

Verdict: confirmed — the index's cadreur section (modifications.md
L939-970) does not name it.
Decision: No change to the agent for this finding — the stop is
justified by the Convertisseur, which writes that reference
(convertisseur.md L305 "`[B?: the weigh-in screen]`"); the index
records the addition; the stop itself is widened under passages-amont
F05 below.
Where: cadreur.md L397 ↔ modifications.md L946
Cited: modifications.md L946-948 lists C1–C25 and names no `[B?:`.
Owner: — (the refonte index)
Also in: convertisseur

### cadreur.md F04 — *How you find a numbered file* comes from no comment

Verdict: wrong — the report's own part 2 says otherwise: cadreur.md
(report) L52 "C — Glob unnamed | fixed | `agents/cadreur.md` L37-45".
The section answers a category-C comment. The second half — the round
count at L822 — is one fact with F18 and is decided there.

### cadreur.md F05 — dispatch row 1 fires on any filled `## Verdict`

Verdict: confirmed — L295 keys on "`architecte/cadreur.md` carries a
filled `## Verdict`"; L954-956 "Its `## Where` names a request, and the
Architecte answered in that request's `## Verdict`"; L223-225 keeps
answered requests in the file under fresh heading blocks.
Decision: Row 1 fires only when the request the blocking file's
`## Where` names carries a filled `## Verdict`; a request answered in
an earlier run lifts nothing. The same key settles D-23 (round one,
still open): a file holding one filled and one empty `## Verdict` is
read block by block, on the request `## Where` names.
Where: cadreur.md L295 ↔ cadreur.md L954
Owner: cadreur
Follows: 7_lots (L143-144 test "`architecte/cadreur.md` with an empty
/ a filled `## Verdict`" on the whole file; they key on the same
request).
Also in: —

### cadreur.md F06 — "D, then dispatch again on what remains"

Verdict: confirmed — L297 "**D**, then dispatch again on what remains";
L949 "You never rename the file"; nothing names which rows the second
dispatch skips, and L315-317 sends it to A only when no
`code/decoupage.md` exists — D-21 (round one, still open) asks what
happens when one does.
Decision: After D the second dispatch runs the rows below the two
blocking-file rows only — redécoupage, defects, none — and when none
matches but `code/decoupage.md` exists, the amended split goes to the
Vérificateur with moves 5 to 10 applied to the lots the decision
touched, never through A.
Where: cadreur.md L297 ↔ cadreur.md L949
Owner: cadreur
Also in: —

### cadreur.md F07 — a new block overwrites the decided file

Verdict: confirmed — L128 "Write `code/blocked_cadreur.md`" and L398
say the same on move 1; L949-952 "You never rename the file … The
command renames it, once you have reported": between D and the report,
a second block is written over the Product Owner's `## Decision`.
Decision: A block raised in the run that applied a decision is appended
as a fresh heading block below the decided one, never written over
it; dispatch and the command read the last `## Decision` in the file,
and the command renames the file only when that last one is filled and
reported applied.
Where: cadreur.md L128 ↔ cadreur.md L951
Owner: cadreur
Follows: 7_lots (L94-95 and L146 read "`## Decision` empty / filled"
on the whole file; they read the last one).
Also in: —

### cadreur.md F08 — `Modifies` holds files in move 6, symbols in *What you write*

Verdict: confirmed — one fact with F02 (L524-525 ↔ L753-754).
Decision: As F02.
Where: cadreur.md L524 ↔ cadreur.md L753
Owner: cadreur
Also in: detailleur, verificateur

### cadreur.md F09 — `round` names two things

Verdict: confirmed — L24 "One invocation per round of the split"; L798
"You do not go out between rounds".
Decision: `round` names one Vérificateur call and its correction only;
a cadreur invocation is a `run`, the word the file already uses at
L290.
Where: cadreur.md L24 ↔ cadreur.md L798
Owner: cadreur
Follows: 7_lots (L9-11, L130-132 "three rounds at most, which it
counts" — already the Vérificateur sense; nothing to rewrite unless the
new wording changes the term).
Also in: —

### cadreur.md F10 — a pointer to a section that does not exist

Verdict: confirmed — L331 "See *What a bug-fix cycle changes*"; L333
"**On a bug-fix cycle:**" is a bold line, not a heading.
Decision: Give the bug-fix material at L333 a heading and point L331 at
it.
Where: cadreur.md L331 ↔ cadreur.md L333
Owner: cadreur
Also in: —

### cadreur.md F11 — the never-do list forbids move 1's grep

Verdict: confirmed — L264-265 "Grep outside the code folders the
conventions name — never a bare pattern"; L397 "Grep `<<ASSUMED` and
`[B?:` in the technical document".
Decision: The never-do entry bounds code searches only; the technical
document is grepped by its own path at move 1.
Where: cadreur.md L264 ↔ cadreur.md L397
Owner: cadreur
Also in: —

### cadreur.md F12 — two units for the Vérificateur's ceiling

Verdict: confirmed — L106-107 "it counts … entries cited per block, not
symbols per lot"; L113-114 "its own ceilings say how many" lots a block
holds. The Vérificateur itself carries both: verificateur.md L453-454
"What the ceiling counts is entries cited, not lots" against L485 "Lots
per block" and L493 "The count is lots, never entries".
Decision: Name one unit in both cadreur sentences — the one the
Vérificateur's table carries, lots per block — and follow the
verificateur plan if it settles the other way.
Where: cadreur.md L106 ↔ cadreur.md L113
Owner: verificateur (its ceiling, its unit)
Follows: cadreur
Also in: verificateur

### cadreur.md F13 — "as it is on a bug fix", written inside the bug-fix section

Verdict: confirmed — L354-356 sit under "On a bug-fix cycle:" (L333);
the rule they mean is L79-80 in *What makes a lot*.
Decision: Point the sentence at the feature-cycle rule in *What makes a
lot* instead of at the section it sits in.
Where: cadreur.md L355 ↔ cadreur.md L333
Owner: cadreur
Also in: —

### cadreur.md F14 — "glob `code/` once" cannot see `architecte/cadreur.md`

Verdict: confirmed — L44-45 "glob `code/` once and route on what is
there"; L295 tests `architecte/cadreur.md`; L954-956 reads it.
Decision: The routing rule globs `architecte/` as well as `code/`.
Where: cadreur.md L44 ↔ cadreur.md L295
Owner: cadreur
Also in: —

### cadreur.md F15 — "see there" names no section

Verdict: confirmed — L145 "The third round did not converge — see
there"; the material is at L822-826, under *Then call the Vérificateur,
and wait*.
Decision: Name the section.
Where: cadreur.md L145 ↔ cadreur.md L822
Owner: cadreur
Also in: —

### cadreur.md F16 — two outcomes for a defect judged wrong

Verdict: confirmed — L828-829 "say so in that blocking file"; L852-853
"stop and report rather than re-cutting against it"; L149-151 "A stop
with no file is invisible to the command".
Decision: One outcome — the blocking file; the second passage says the
same or goes.
Where: cadreur.md L828 ↔ cadreur.md L852
Owner: cadreur
Also in: —

### cadreur.md F17 — the return row tests a `## Decision` the file never carries

Verdict: confirmed — L818 "A `code/blocked_verificateur.md` with an
empty `## Decision`".
Decision: The return row keys on the presence of
`code/blocked_verificateur.md` alone.
Where: cadreur.md L818 ↔ verificateur.md L206
Cited: verificateur.md L206-207 — "⚠️ **No `## Decision`** — 📌
**nothing here is the Product Owner's to settle**"; 7_lots.md L82-83 —
"it carries no `## Decision`, so no rename closes it".
Owner: cadreur
Also in: verificateur

### cadreur.md F18 — rounds counted on archived `code/sequence-NN.md`

Verdict: confirmed — L822-823 "The count is the number of archived
`code/sequence-NN.md` files plus the round you are in"; a grep of
`.claude-new/` for `sequence-NN` finds no writer outside cadreur.md.
Decision: The Vérificateur writes the round number in
`code/sequence.md` — the previous round's plus one when the previous
`## Defects` carried lines, `1` otherwise — and the Cadreur counts on
that line, never on archived files. (A redécoupage follows a converged
split, so it starts at 1; a take-back from cold follows a round with
defects, so it carries on — D-25's loss of the count at cold re-entry
closes with it.)
Where: cadreur.md L822 ↔ verificateur.md L96
Cited: verificateur.md L92-93 — "Save two, and only where a move says
so: `code/sequence.md` of the previous round, at move 5" — it reads the
previous round in place and writes over it.
Owner: verificateur (writes the file)
Follows: cadreur (L27, L822-826, L931-932 "counted on disk"), 7_lots
(L11, L131 keep "which it counts"; nothing to rewrite).
Also in: verificateur

### cadreur.md F19 — `## Files` copies `Modifies`, which carries no path

Verdict: confirmed — L753-754 "symbols only … never a file".
Decision: `## Files` is built from `Touches` (callers, tests, manifests
by path — F02) and from the file the Détailleur resolves for each
`Modifies` symbol by the grep it already runs (detailleur.md L562-563),
never by copying `Modifies`; the files a production lot creates are the
Concepteur's to declare — that half is passages-aval F01, carried by
the detailleur and concepteur plans.
Where: cadreur.md L753 ↔ detailleur.md L260
Cited: detailleur.md L259-260 — "`## Files` carries the lot's
`Modifies` and `Touches`, copied from `code/decoupage.md` — one path
per line, no distinction between the two."
Owner: detailleur (writes `## Files`)
Follows: cadreur (F02/F08), concepteur, testeur, realisateur, relecteur
(their checks key on `## Files` as paths — unchanged unit, but the
production-lot half rewrites their `## Outside the lot` tests).
Also in: detailleur, concepteur, testeur, realisateur, relecteur,
verificateur

### cadreur.md F20 — a refused verdict loops with the command

Verdict: confirmed — L961 "The request is refused → The block stands —
say so and go out"; the command then re-invokes on the same disk.
Decision: The Cadreur's report states the outcome on the blocking
file — decision applied, verdict applied, verdict refused, block
standing — and the command's return table stops and relays to the
Product Owner on a refused verdict instead of re-invoking.
Where: cadreur.md L961 ↔ 7_lots.md L144
Cited: 7_lots.md L144 — "`architecte/cadreur.md` with a **filled**
`## Verdict` → The Architecte has answered — invoke `cadreur`: the
verdict is what lifts its block"; L145 stops only on
"`code/blocked_cadreur.md` **alone**".
Owner: 7_lots (the rows)
Follows: cadreur (the report line — F22)
Also in: —

### cadreur.md F21 — a block lifted by a verdict is never closed

Verdict: confirmed — L960 "The rule is written → Carry on"; L949 "You
never rename the file"; the command renames only on an applied
decision.
Decision: The command renames `code/blocked_cadreur.md` on a block
lifted by a verdict exactly as on an applied decision, keyed on the
Cadreur's report line (F22).
Where: cadreur.md L960 ↔ 7_lots.md L146
Cited: 7_lots.md L146 — "The Cadreur reports it **applied** a decision
→ Rename the file … `git mv code/blocked_cadreur.md
code/blocked_cadreur-NN.md`".
Owner: 7_lots
Follows: cadreur
Also in: —

### cadreur.md F22 — no line tells the Cadreur to report the applied decision

Verdict: confirmed — L949-952 and L970-973 say the command renames
"once you have reported"; nothing in block D says what the report
carries; L923 and L926 give report lines for block C only.
Decision: The Cadreur's report names what it did with the blocking
file, in the four outcomes of F20.
Where: cadreur.md L970 ↔ 7_lots.md L146
Cited: 7_lots.md L146 — "The Cadreur reports it **applied** a
decision".
Owner: cadreur
Follows: 7_lots (F20, F21 key on that line)
Also in: —

### cadreur.md F23 — resuming a cadreur block through `/7_decoupe`

Verdict: confirmed — cycle.md L88 still routes "`cadreur` or
`verificateur` → `/7_decoupe`"; settled by decisions.md ("Moot.
`cycle.md` is deleted").
Decision: Apply decisions.md — delete `.claude-new/commands/cycle.md`;
nothing in cadreur.md to rewrite (a grep of `.claude-new/` for
`/cycle` and `cycle.md` finds no mention outside the file itself).
Where: cadreur.md L859 ↔ cycle.md L88
Cited: cycle.md L88 — "| 7 | A cycle agent's `blocked_*` with
`## Decision` filled | … `cadreur` or `verificateur` → `/7_decoupe` |".
Owner: commandes
Also in: commandes, verificateur (fichiers F09)

### cadreur.md D-13 — a blocking case absent from the list

Verdict: confirmed — L628 "cut a lot for it — or block, when no lot of
any layer can carry it"; the list at L135-147 does not carry that case
(the report's part 2 marks D-13 `other` for this reason).
Decision: Add the case to the blocking list, pointing at move 7's
second table.
Where: cadreur.md L628 ↔ cadreur.md L135
Owner: cadreur
Also in: —

D-21 and D-23, left `open` in part 2, close with F06 and F05
respectively; D-25 closes with F18.

---

## The thematic reports, filtered on `cadreur`

### renommages.md F01 — `## Files` told to copy `Modifies` one path per line

Verdict: confirmed — one fact with cadreur.md F19.
Decision: As cadreur.md F19.
Where: detailleur.md L259 ↔ cadreur.md L753
Cited: cadreur.md L753-754 — "`Needs`, `Produces` and `Modifies` carry
symbols, and symbols only. A name the code carries — never a file."
Owner: detailleur
Also in: detailleur, concepteur, testeur, realisateur, relecteur

### renommages.md F13 — the rename keyed on the Cadreur's report alone

Verdict: confirmed — 7_lots.md L100-103 "The Cadreur reports the split
holds and `code/redecoupage.md` can be archived → rename it yourself";
cadreur.md L926-927 "relay the Vérificateur's `## Redécoupage:
archivable` line … the command archives the file on it".
Decision: The command keys the rename on the `## Redécoupage:
archivable` line in `code/sequence.md`, read from disk; the Cadreur's
relay stays a courtesy, not the trigger.
Where: 7_lots.md L100 ↔ verificateur.md L472
Cited: verificateur.md L472-475 — "You have no tool that renames a
file, and neither has the Cadreur — the command does it, reading that
line."
Owner: 7_lots
Follows: cadreur (L926-927 no longer carry the trigger)
Also in: verificateur

### fichiers.md F08 — the return row tests an empty `## Decision`

Verdict: confirmed — one fact with cadreur.md F17; 7_lots.md L79-84
adds that the command `git rm`s the file before every run.
Decision: As cadreur.md F17.
Where: cadreur.md L818 ↔ 7_lots.md L79
Cited: 7_lots.md L79 — "First, remove `code/blocked_verificateur.md`
if it is there — `git rm`."
Owner: cadreur
Also in: verificateur

### fichiers.md F09 — `/cycle` resumes a `verificateur` block

Verdict: confirmed — settled by decisions.md, same reason as cadreur.md
F23.
Decision: As cadreur.md F23.
Where: cycle.md L88 ↔ verificateur.md L206
Cited: verificateur.md L206-207 — "No `## Decision` — nothing here is
the Product Owner's to settle".
Owner: commandes
Also in: commandes, verificateur

### fichiers.md F14 — no agent or command writes `code/sequence-NN.md`

Verdict: confirmed — one fact with cadreur.md F18.
Decision: As cadreur.md F18.
Where: cadreur.md L822 ↔ 7_lots.md L103
Cited: 7_lots.md L103 — "`git mv code/redecoupage.md
code/redecoupage-NN.md`" — the only archive the command makes.
Owner: verificateur
Also in: verificateur

### fichiers.md F16 — `/8_code` relays two headings not yet written

Verdict: confirmed — one fact with chemins-aval.md F02.
Decision: As chemins-aval.md F02.
Where: 8_code.md L352 ↔ cadreur.md L909
Cited: cadreur.md L907-909 — "Write both of these into
`code/redecoupage.md`, at the end: `## Ce qui revient`".
Owner: 7_lots
Also in: —

### chemins-aval.md F02 — the recurrence is relayed before it exists, then archived

Verdict: confirmed — 8_code.md L351-354 relays "the `## Ce qui revient`
and `## Ce que j'en fais` of `code/redecoupage.md` — the Cadreur wrote
them there at the end of its round", then L363 runs `/7_lots`; 7_lots.md
L103 renames the file; 7_lots.md L240-253 (*What you relay*) carries no
such line; cadreur.md L923 says it in its report only "when something
is on its third return".
Decision: `/7_lots` relays the two sections from `code/redecoupage.md`
before renaming it and `/8_code` drops its relay; the Cadreur states
them in its report on every redécoupage, not only a third return.
Where: 8_code.md L352 ↔ cadreur.md L907
Cited: cadreur.md L907 — "Write both of these into
`code/redecoupage.md`, at the end".
Owner: 7_lots
Follows: 8_code, cadreur (L923)
Also in: —

### chemins-aval.md F19 — the ceiling is per invocation

Verdict: confirmed — one fact with cadreur.md F18.
Decision: As cadreur.md F18.
Where: cadreur.md L822 ↔ verificateur.md L444
Cited: verificateur.md L444-445 — "Their blocks come from the previous
`code/sequence.md` — read its `## Blocks` section before you write over
the file."
Owner: verificateur
Also in: verificateur

### chemins-aval.md F22 — a re-cut lot keeps its number and its `verdict.md`

Verdict: confirmed — cadreur.md L884-885 "Every other lot is yours — the
one in hand included, whose code was dropped"; L891 gives the next free
number to lots *added* (L887) only; nothing gives a re-cut lot a fresh
one, so its `code/<lot>/verdict.md` and `## Attempts` stay.
Decision: A lot whose anchor or fields change on a redécoupage takes the
next free number like a lot added, and its old number is retired with
its `code/<lot>/` folder, so no verdict carries over to the new shape.
Where: 8_code.md L344 ↔ relecteur.md L157
Cited: relecteur.md L157-158 — "`## Attempts` carries the count the
verdict you replace held, plus one — `1` when there was no verdict."
Owner: cadreur
Follows: 8_code (L344-354 count and L375 stale sheets: a retired number
leaves the sequence), verificateur (L440-442 "coded ones keep the
blocks they ran in" — a retired number is not a coded one), relecteur
(nothing to rewrite: it reads the verdict of the number it is given).
Also in: relecteur

### passages-amont.md F05 — a `[B12: …]` left as a pending question is not caught

Verdict: confirmed — cadreur.md L397 greps `<<ASSUMED` and `[B?:` only;
L138-139 blocks on those two.
Decision: Move 1 and the blocking list stop on any `[B` reference left
in the document, not only `[B?:`.
Where: convertisseur.md L766 ↔ cadreur.md L392
Cited: convertisseur.md L766-767 — "Then, after move 4, grep `[B` in
the document — what remains is either a question you wrote, or a
reference you missed."
Owner: cadreur
Also in: convertisseur

### passages-amont.md F06 — `Consumes:` has no named reader in the split

Verdict: confirmed — cadreur.md never names `Consumes:`; move 5
(L476-486) derives `Needs` from the inventory alone.
Decision: Move 5 names each entry's `Consumes:` line as the source of
the direction of `Needs` between lots, beside the inventory.
Where: convertisseur.md L295 ↔ cadreur.md L753
Cited: convertisseur.md L275-277 — "No agent greps `Consumes:` — the
Cadreur reads each entry in full, and the direction it carries is what
keeps a screen's lot behind the lot that computes what it shows."
Owner: cadreur
Also in: convertisseur

### passages-aval.md F01 — `## Files` empty on a production lot (BLOCKING)

Verdict: confirmed — one fact with cadreur.md F19, widened to production
lots: `Modifies: —` and `Touches: —` give an empty `## Files`, and
every created file lands in `## Outside the lot` (concepteur.md L259,
realisateur.md L189, relecteur.md L386-388).
Decision: As cadreur.md F19 for the cadreur's side; the files a
production lot creates are declared by the Concepteur when it places
the symbols — the detailleur and concepteur plans carry that half.
Where: detailleur.md L259-265 ↔ cadreur.md L753-754
Cited: cadreur.md L753-754 — "`Needs`, `Produces` and `Modifies` carry
symbols, and symbols only … never a file."
Owner: detailleur
Follows: cadreur (F02/F08), concepteur, testeur, realisateur, relecteur
Also in: detailleur, concepteur, testeur, realisateur, relecteur

### passages-aval.md F03 — the return row matches no file the Vérificateur writes

Verdict: confirmed — one fact with cadreur.md F17.
Decision: As cadreur.md F17.
Where: cadreur.md L818 ↔ verificateur.md L206-208
Cited: verificateur.md L206-207 — "No `## Decision`".
Owner: cadreur
Also in: verificateur

### passages-aval.md F04 — the count on disk is always zero

Verdict: confirmed — one fact with cadreur.md F18.
Decision: As cadreur.md F18.
Where: cadreur.md L822-823 ↔ verificateur.md L105, 7_lots.md L101-103
Cited: verificateur.md L104-105 — "## What you write —
`code/sequence.md` — three headings"; 7_lots.md L103 — the only
`git mv` the command makes is on `redecoupage.md`.
Owner: verificateur
Also in: verificateur

---

## To settle

—

No finding above turns on intent, scope or user-facing behaviour. The
one structural fork — where caller files go (F02/F08/F19) — is decided
above with its alternative costed; if the detailleur or verificateur
plan decides the other way, the cadreur follows it.
