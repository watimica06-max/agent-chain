# Plan — `concepteur.md`

Built against `.claude-new/agents/concepteur.md`, `.claude-new/commands/8_code.md`
(the only command that names the agent), `docs/verification2/concepteur.md`
(both parts), `docs/verification2/decisions.md`, and the lines of the six
thematic reports that name the concepteur (`renommages.md` F02, F08, F16 ·
`chemins-aval.md` F06, F09 · `passages-aval.md` F01, F06; `fichiers.md`,
`chemins-amont.md` and `passages-amont.md` name it nowhere).

Every cross-file line quoted below was opened in `.claude-new/`. The
`plans/` folder was empty when this plan was written, so `Also in` names the
plans by their agent or by `commandes.md`.

One settled question bears on this agent and is applied here, not reopened:
`renommages.md` F16 — the Concepteur writes an `architecte/` request like the
Détailleur and the Réalisateur, places the symbol meanwhile in the module of
the one it depends on most, and says so in its report.

---

## Part 1 — the index

### concepteur.md F01 — the index omits the `## Placements…` field

Verdict: confirmed
The report's line reference is off by three: the `Son rapport` row is
`modifications.md` L855, not L852 — "*les symboles et leur fichier, la
compilation, les fichiers touchés hors fiche*". Three items; the file's
report has four headings (concepteur.md L247-261), and the fourth is the one
8_code.md L112 relays.
Decision: Bring the index's `Son rapport` row to the fields the report carries
once this plan is applied (F07 adds one, renommages F16 changes what the
`## Placements…` field says).
Where: modifications.md L855 ↔ concepteur.md L245-261
Owner: the index (`docs/refonte/modifications.md`) — a record, not an agent;
no line of `concepteur.md` moves for this
Also in: —

### concepteur.md F02 — "il nomme les symboles"

Verdict: confirmed
`modifications.md` L863 (not L859): "*il nomme les symboles*". The file
forbids it: L109-111 "Declare a symbol the sheet does not name, beyond what
the language requires to compile"; L200-201 "Exactly the signature the sheet
gives — name for name, type for type". The names come from the Détailleur's
`## Signatures` (detailleur.md L224-230, L626 "Write the signature in the
sheet").
Decision: Keep the transcription rule in `concepteur.md`; record in the index
that "nomme" was applied as "writes the symbols the sheet names", the naming
being the Détailleur's.
Where: modifications.md L863 ↔ concepteur.md L109-111, L200-201
Owner: the index — no agent line moves
Also in: —

### concepteur.md F03 — the blocking protocol is absent from the index

Verdict: confirmed
`modifications.md` L844-887 carries no word on `blocked_concepteur.md`, the
resumption on a filled `## Decision`, or the resume from `conception.md`;
concepteur.md L120-165 carries all three.
Decision: Add the blocking protocol to the index's record, after F06, F07 and
F11 below have reshaped it — not before, or the record would describe the
defective version.
Where: modifications.md L844-887 ↔ concepteur.md L120-165
Owner: the index — no agent line moves
Also in: —

---

## Part 3 — tools

### concepteur.md F04 — `git status` granted, never used

Verdict: confirmed
L94 grants it; moves 1-5 (L171-239) name `git add`, `git commit` and the
compile command, never `git status`. Move 5 says "staging explicitly what
belongs to the lot" (L237) without saying how the agent sees what the
worktree holds.
Decision: Give `git status` its gesture at move 5 — the check, before
staging, of what the worktree holds, so that the declarations and the report
are staged and nothing else is.
Where: concepteur.md L94 ↔ concepteur.md L237-239
Owner: concepteur
Also in: — (testeur.md L92 grants the same shell; whether its move 6 L255
uses it is the testeur plan's to judge)

### concepteur.md F05 — no tool finds the `permanente` marker

Verdict: overstated
Real: no grep gesture is named on the conventions file — L75-77 bounds grep
to "a symbol … on the code folders the conventions name". But the finding's
premise, that a marker filter needs a tool, is not in the file: L62-63 asks
for "the rules marked `permanente`, whole" from a file the agent reads
(L62), L64-66 has it read the file whole when no rule carries the marker,
and L85-88 makes the permanent rules "the most important thing you read".
The marker is met by reading, and the reading path reaches it either way.
Below NOTE — nothing to change.

---

## Part 2 — the block, the resume, the report

### concepteur.md F06 — the block path writes no report the resume rule can read

Verdict: confirmed
L122 "Write `code/<lot>/blocked_concepteur.md`"; L125-128 "Then commit what
you wrote, the blocking file with it — the declarations that landed" — the
report is never ordered. L251-253: `## Compile` holds "the command, and that
it passed" — no wording for a run that stopped on a red compile (L223-232)
or before compiling. L162-165 then reads `## Declared` from "a
`code/<lot>/conception.md` already there … a run of yours that blocked", a
file no blocked run writes. The next run redeclares everything the first one
committed — the duplicate-symbol error L164-165 warns of.
Decision: On a block, write `conception.md` before the blocking file —
`## Declared` listing what landed, `## Compile` naming the command and its
outcome (passed, failed on what, or not run), the two other fields as they
stand — commit it with the declarations, and have the resumed run rewrite
the report whole once it compiles green.
Where: concepteur.md L120-128 ↔ concepteur.md L162-165, L251-253
Owner: concepteur
Follows: 8_code — its skip on `conception.md` (L112) must no longer fire on
a lot with a standing block, see F11; testeur — none: 8_code L119-120 stops
the lot on a block, so no testeur reads a `conception.md` whose `## Compile`
did not pass, and testeur.md L61-62 ("that the module compiles") holds.
Cited: 8_code.md L119-120 — "A blocking file from any of the three stops the
lot there — the two after it do not run."
Also in: commandes.md (F11, chemins-aval F06, passages-aval F06), testeur.md
(same shape: testeur.md L132-134 resumes from a `tests.md` "a run of yours
that blocked")

### concepteur.md F07 — "say in your report" has nowhere to land

Verdict: confirmed
L158 "Say in your report that you applied it — the orchestration renames the
file"; L245-261 fixes four headings; L269-270 "Nothing else in the report —
no judgement on the sheet, no summary". The orchestration's rename (8_code.md
L170 "rename it once the agent reports having applied it") keys on a
sentence the report cannot carry.
Decision: Add a field to `conception.md` that names the decision applied
(the blocking file) or a dash — the place where "say in your report" lands,
what the orchestration's rename keys on, and what legitimises a declared
signature that diverges from the sheet (see renommages F08 below).
Where: concepteur.md L158 ↔ concepteur.md L245-270
Owner: concepteur
Follows: relecteur — L184-186 accepts only the Réalisateur's field, see
renommages F08; 8_code — 4b L170 says what the rename keys on, and the new
field is that
Also in: relecteur.md, commandes.md, testeur.md (testeur.md L128-130 carries
the same "say in your report" against a fixed-heading report — the testeur
plan's to judge)

### renommages.md F08 — a Concepteur-applied decision reads as drift

Verdict: confirmed
Cited: relecteur.md L184-186 — "The decision is in the report's `## What
governed the code, besides the sheet` — that field, and nothing else, makes
a divergence legitimate." And L188-190: "A signature that diverges and that
field does not account for … makes the status `FAIL structurel`." L180-182
scopes `## Symbol divergences` to "a signature changed by a decision the
Réalisateur applied". A Concepteur block is exactly a signature that cannot
be written as the sheet gives it (L148-150); the decision that lifts it
changes the signature, and the Réalisateur's field never sees it.
Decision: Same field as F07 — the Relecteur reads it alongside the
Réalisateur's to legitimise a divergence and to fill `## Symbol
divergences`, the propagation of 8_code move 5 following as for a
Réalisateur-applied decision.
Where: concepteur.md L158 ↔ relecteur.md L180-190
Owner: concepteur (the field); relecteur decides how it reads it
Follows: relecteur (L180-190), 8_code (move 5 L177-179 names the verdict's
`## Symbol divergences` only — unchanged if the Relecteur fills it from both
fields)
Also in: relecteur.md, commandes.md

### concepteur.md F08 — "empty bodies" in two senses

Verdict: confirmed
The deliverable is "empty bodies" at L3, L15, L198 and 8_code.md L112
("Writes the declarations with empty bodies"); L204-205 forbids "an empty
body, never a default value — both are bodies the testeur's red test could
pass on". testeur.md L19-20 and L23-24 use the term in the deliverable
sense too ("declarations with empty bodies", "passes against an empty
body").
Decision: Settle one meaning — the deliverable is a body that throws *not
implemented*; a body with nothing in it is the forbidden thing — and stop
calling the deliverable "empty" wherever it is named.
Where: concepteur.md L3, L15, L198 ↔ concepteur.md L204-207
Owner: concepteur
Follows: 8_code (L112), testeur (L19-20, L23-24)
Also in: commandes.md, testeur.md

### concepteur.md F09 — "the lot's first commit" on a resumed run

Verdict: confirmed
L125-126 commits on block; L237-239 "It is the lot's first commit, and the
Relecteur's file list is the diff from it". 8_code.md L124-125: "`git diff
--name-only` between the lot's first commit and `HEAD`"; relecteur.md L390:
"the diff starts at the concepteur's commit". On a resumed lot the first
commit is the blocked run's — still the right start for the diff, so the
Relecteur's list is whole; only the claim at L238 is false.
Decision: Say the lot's first commit is the blocked run's when there was
one, and that the resumed run's commit is not the first — the diff still
starts at the earliest.
Where: concepteur.md L125-126 ↔ concepteur.md L237-239
Owner: concepteur
Follows: — (8_code L125 and relecteur L390 are written on "the lot's first
commit" / "the concepteur's commit" and hold for both runs)
Also in: —
Note: nothing in `concepteur.md` or `8_code.md` says how the orchestration
finds "the lot's first commit" — no commit-message rule exists. Not a
finding of this round; carried to `## To settle`.

### concepteur.md F10 — a symbol with no file to fall back on

Verdict: confirmed
L189-191: "put it in the file of `## Files` holding the symbol it depends on
most". detailleur.md L265: "A dash when the lot creates everything it
touches" — a lot of new files has a dash there, and the branch has no
outcome. Settled by renommages F16, which moves the fallback from a file of
`## Files` to a module: "Meanwhile it places the symbol in the module of the
one it depends on most, and says so in its report" (decisions.md L162-163).
A module exists whether or not the file does — `## Dependencies` says where
every type comes from (detailleur.md L630-633).
Decision: Apply renommages F16 — the fallback is the module of the symbol it
depends on most, never a file of `## Files`; the request to the Architecte
carries the rule that is missing.
Where: concepteur.md L189-191 ↔ detailleur.md L265, decisions.md L153-164
Owner: concepteur
Also in: — (the residual — a symbol depending on nothing — is in
`## To settle`)

### renommages.md F16 — no route to the Architecte

Verdict: confirmed
L193-196: "You write no conventions request — you have no route to the
Architecte … the orchestration relays it, and the Product Owner has the
rule added." 8_code.md L112 relays the line to the Product Owner. Settled
by decisions.md L153-164: the Concepteur writes an `architecte/` request.
Cited: architecte.md L672-673 — invocation 3 reads "`architecte/` in the
working folder — glob it, that folder alone" and L663-664 treats "every
request waiting in `architecte/`": a Concepteur request needs no change on
the Architecte's side. realisateur.md L404-410 gives the request's shape
and folder.
Decision: Apply the settled decision — the Concepteur writes an
`architecte/` request for a placement the conventions do not settle, places
the symbol meanwhile in the module of the one it depends on most, and names
both the placement and the request in its report; the relay to the Product
Owner goes.
Where: concepteur.md L189-196, L255-257 ↔ 8_code.md L112, architecte.md
L663-673
Owner: concepteur
Follows: 8_code (L112 — the relay line goes; move 7 L219-221 already collects
the request at the end of the lot); relecteur — none required by this
decision (its `## Requests` check L366-368 is on the Réalisateur's report and
L398-400 on the sheet; whether the Concepteur's report joins that check is
the relecteur plan's to judge)
Also in: commandes.md, relecteur.md

---

## Part 4 — the command

### concepteur.md F11 — the skip on `conception.md` blocks the resume

Verdict: confirmed
8_code.md L112: "skipped when `code/<lot>/conception.md` is there"; 4b
L164-170 runs "Before invoking anything on a lot" and, on a filled decision,
"Name it in the agent's prompt". Once F06 has the blocked run write its
report, the skip fires and the decision-filled prompt of L277-283 never
runs; as the file stands today the skip never fires and the run redeclares
everything.
Decision: Skip the concepteur only when `conception.md` is there and no
unnumbered `blocked_concepteur.md` sits beside it — a lot with a standing
block goes through 4b, which stops on an empty decision and runs the agent
on a filled one.
Where: 8_code.md L112 ↔ concepteur.md L162-165
Owner: 8_code
Follows: concepteur — L162-165 stands and becomes reachable; nothing else to
rewrite once F06 is applied
Also in: commandes.md, testeur.md (same pair, 8_code L113 ↔ testeur.md
L132-134)

### chemins-aval.md F06 — same pair, seen from the command

Verdict: confirmed
Same lines as F11 (8_code.md L112 ↔ concepteur.md L162-165), extended to the
testeur (L113 ↔ testeur.md L132-134). One decision, above.
Decision: As F11.
Where: 8_code.md L112-113 ↔ concepteur.md L162-165, testeur.md L132-134
Owner: 8_code
Follows: concepteur (F06), testeur
Also in: commandes.md, testeur.md

### passages-aval.md F06 — same pair, seen from the passages

Verdict: confirmed
Same lines again. The finding's "both agents write that report on a run
that blocked" is true of the intent (L162-165) and false of the procedure
(L120-128 never orders it) — F06 fixes the procedure, F11 the skip.
Decision: As F06 and F11.
Where: 8_code.md L112-113 ↔ concepteur.md L162-165, testeur.md L132-134
Owner: concepteur (the report on block), 8_code (the skip)
Follows: testeur
Also in: commandes.md, testeur.md

### chemins-aval.md F09 — `conception.md` survives a redécoupage

Verdict: confirmed
8_code.md L379-382 deletes "`code/<lot>/fiche-executable.md`, for every lot
with no `verdict.md` carrying PASS" and nothing else; L112-113 skip the
concepteur on `conception.md` and the testeur on `tests.md`. A re-cut lot
keeps both, and its Réalisateur fills bodies declared against the old
sheet.
Decision: Delete `conception.md` and `tests.md` with the sheet, for every lot
with no PASS, when the split comes back.
Where: 8_code.md L379-382 ↔ 8_code.md L112-113
Owner: 8_code
Follows: — (no line of `concepteur.md` keys on it)
Also in: commandes.md, testeur.md
Note: the declarations those lots committed to the code survive too
(realisateur.md L335-337: "the concepteur committed the declarations, the
testeur the tests"). The finding does not go there; carried to
`## To settle`.

### concepteur.md F12 — `Unit`, a Kotlin type in a multi-project chain

Verdict: confirmed
L207 "a body with no return does not compile outside a `Unit`";
CLAUDE.md L78-79 "Never hardcode a path — the chain runs on several
projects." The rule is right; the type naming it is one language's.
Decision: State the rule without a language's type — a body that returns
nothing does not compile where the signature returns a value.
Where: concepteur.md L207 ↔ CLAUDE.md L78-79
Owner: concepteur
Also in: —

---

## The sheet's `## Files` — two findings the Concepteur follows

### passages-aval.md F01 — `## Files` is a dash on a production lot

Verdict: confirmed
Cited: detailleur.md L259-262 — "`## Files` carries the lot's `Modifies`
and `Touches`, copied from `code/decoupage.md`"; L265 — "A dash when the
lot creates everything it touches". cadreur.md L753-754 — "`Needs`,
`Produces` and `Modifies` carry symbols, and symbols only. A name the code
carries — never a file." So `## Files` can hold at most `Touches`, and on a
lot that creates its files it is a dash. Three readers read it otherwise:
concepteur.md L57-58 "its `## Files` names every file the lot owns: where
each declaration goes"; testeur.md L58-59 "names every file the lot owns:
where your tests go"; realisateur.md L63-64 "names every file the lot
owns". And every file created lands in three `## Outside the lot` fields
(concepteur L259-261, realisateur L189-191, relecteur L386-391).
Decision: Align the writer to its three readers — `## Files` names every
file the lot owns, the ones it creates included, derived by the Détailleur
from the conventions' placement rules; `Modifies`/`Touches` are an input to
it, not its content.
Where: detailleur.md L259-265 ↔ concepteur.md L57-58, L186-191, L259-261
Owner: detailleur (writes the field); cadreur upstream for what the lot list
carries
Follows: concepteur — L57-58 and L186 hold as written once the field is
complete; L112-115 and L259-261 (`## Outside the lot`) then mean what they
say; testeur, realisateur, relecteur likewise
Also in: detailleur.md, cadreur.md, testeur.md, realisateur.md,
relecteur.md

### renommages.md F02 — same field, same gap

Verdict: confirmed
Same lines (detailleur.md L265 ↔ concepteur.md L186); same three readers.
Decision: As passages-aval F01.
Where: detailleur.md L265 ↔ concepteur.md L186
Owner: detailleur
Follows: concepteur, testeur, realisateur
Also in: detailleur.md, testeur.md, realisateur.md

---

## Part 2 of the report — rows left `other` or `open`

| Row | Verdict | |
|---|---|---|
| D-7 | confirmed | It is F06 + F11; decided above |
| D-11 — no `permanente` marker in `TECHNICAL_CONVENTIONS.md` | stale | architecte.md L140: "`permanente` or `spécifique`, at the end of the line" on every rule; L150-152 make "where a kind of symbol lives, the commands that compile, analyse and test" always `permanente`. The marker exists once the Architecte has derived the file; concepteur.md L64-66 covers the interim. Nothing to decide |
| D-12 — no compile-only task in the conventions | stale | architecte.md L150-152: the compile command is a rule the Architecte writes; concepteur.md L215-221 says what to do when the command it names also runs the tests, and to record which ran in `## Compile`. Nothing to decide |
| Cross-file — 8_code L96-97 "the `realisateur` commits inside it, lot by lot. That is his; you do not commit for him" | confirmed | Three agents commit per lot: concepteur.md L237 (move 5), testeur.md L255 (move 6), the realisateur. The line names one. Decision: name the three. Owner: 8_code. Also in: commandes.md, testeur.md |

Rows marked `fixed` and `moot` in the report were spot-checked where a
finding above touches them (A-5/D-8 at L17-18 and L204-207, D-4 at
L125-128, D-13 at L237-239, C-Bash at L92-98) and hold.

---

## To settle

Not mine — each turns on a choice the findings do not make and the settled
list does not cover. `Decision` left empty on every one.

### A symbol that depends on nothing, in a lot of only-new files

renommages F16 gives the fallback "the module of the one it depends on
most". A symbol with no dependency at all — a root type, a constant holder
— has none.

| Option | Cost |
|---|---|
| Place it in the module the lot's other symbols land in, and say so | Cheapest; wrong for a lot whose every symbol is placeless — the request to the Architecte still goes, so the rule arrives at the end of the lot |
| Block on it | A blocking file to the Product Owner for a placement the Architecte settles at move 7 anyway |

Decision: —

### The declarations of a re-cut lot, already in the code

chemins-aval F09 deletes the re-cut lot's `conception.md`; its declarations
were committed (concepteur.md L237, realisateur.md L335-337) and stay in the
code. The Concepteur of the new lot meets symbols already declared — under
old signatures.

| Option | Cost |
|---|---|
| The orchestration reverts the re-cut lots' commits before `/7_lots` | Git surgery in the command; clean code for the new split |
| The new lot's Concepteur edits what it finds, the old declaration counted as its own | Its L162-165 rule ("declare only what is missing") would have to read a stale declaration as one to rewrite, the opposite of what it says |
| Leave them; the Relecteur's `## Outside the lot` catches what nobody owns | The stale declarations belong to no lot and no sheet; the Vérificateur's "no `PASS`" reading is untouched but the code carries symbols no sheet promises |

Decision: —

### How the orchestration finds "the lot's first commit"

8_code L124-125 diffs from "the lot's first commit"; relecteur L390 from
"the concepteur's commit"; no file prescribes a commit message that names
the lot, and the Concepteur's shell (L94) allows `git commit` with no
wording rule. Not a finding of this round.

| Option | Cost |
|---|---|
| A commit-message rule for the three committing agents (`<lot>: …`) | One line in three agent files; the orchestration greps `git log` for it — a Bash gesture 8_code does not list today |
| The orchestration notes the `HEAD` sha before invoking the concepteur, per lot | No agent change; the sha lives in the run's memory and a run restarted mid-lot loses it — the same trap 8_code L153-157 names for `## Attempts` |

Decision: —
