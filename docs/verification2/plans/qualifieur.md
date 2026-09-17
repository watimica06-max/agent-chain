# Plan — qualifieur

Built against `.claude-new/agents/qualifieur.md` (366 lines), the two
commands that name it (`3a_genre.md`, `2_structure.md`), its report
`docs/verification2/qualifieur.md`, `decisions.md`, and the five hits
the six thematic reports carry for it (`renommages.md` F10,
`passages-amont.md` F03, `chemins-amont.md` F03, F04, F06).

None of the fourteen settled questions in `decisions.md` bears on this
agent. No verdict below is `stale` or `wrong`: the agent is new to the
refonte, and every line the report cites reads today as the report
describes it.

Three findings form one knot — the blocking file whose decision names a
rewrite (`qualifieur.md` F11, `chemins-amont.md` F03/F04,
`renommages.md` F10). They are decided once, under F11, and the others
point at it.

Two questions turn on process intent and go to `## To settle`: whether
a *transverse-or-behaviour* doubt stays silent (F12), and how a
two-genre block gets back to the decoupeur (F14, with F06 hanging on
it).

---

## The report's findings

### qualifieur.md F01 — the index records one silent doubt, the file settles all

Verdict: confirmed
Decision: —
Where: qualifieur.md L140-141 ↔ modifications.md L118
Owner: whoever maintains `modifications.md`
Also in: —

The file side holds — L140-141: "**The doubt you settle** — 🔴 **which
genre?** 📌 **`comportement`, and no question.**" — any doubt between
any two genres is written `comportement` silently. The other side,
`modifications.md` L118, is outside this plan's reading list and I did
not open it, so I cannot quote what the index says and do not decide.
Note that the file's rule is itself under `## To settle` 1 (F12): if the
silent doubt is narrowed to the *transverse* case, the file comes to
match what the report says the index records.

### qualifieur.md F02 — the majority-genre rule is not in the index

Verdict: confirmed
Decision: —
Where: qualifieur.md L88-91 ↔ modifications.md L60-62
Owner: whoever maintains `modifications.md`
Also in: —

The file side holds — L88-91: "**Give it the genre of what it is mostly
about, and name it in your report**". The index side is
`modifications.md`, not opened for the reason given under F01. Note
that the rule itself may go: `## To settle` 2 (F14) decides whether a
two-genre block blocks instead, and F06 rewrites the rule if it stays.

### qualifieur.md F03 — a targeted `Edit` on an empty `Genre:` line cannot be unique

Verdict: confirmed
Decision: Say that the edit is anchored on the block's heading line together with the `Genre:` line below it, never on the `Genre:` line alone.
Where: qualifieur.md L4 ↔ qualifieur.md L211-213
Owner: qualifieur
Also in: classeur plan — same gesture on `Nature:` (classeur.md L179 "one targeted edit per `Nature:` line"), where the anchor needs the heading and the `Genre:` line both, since every unfilled behaviour carries the identical `Genre: comportement` / `Nature:` pair.

Cited: qualifieur.md L4 — "tools: Read, Grep, Edit, Write"; L212-213 —
"📌 **one targeted edit per `Genre:` line**, never a rewrite". Every
unqualified block carries the same two characters after `Genre:`
(nothing), and `Edit` refuses a match that is not unique; the heading
(`### B<n> — <title>`) is what is unique, and L46-48 already place
`Genre:` "directly under it".

### qualifieur.md F04 — no named way to load a block without reading the file whole

Verdict: confirmed
Decision: Name the mechanism that loads one block — the line numbers of the headings from a grep, then a read of the window between the block's heading and the next heading — so that "load those, and no others" has a tool behind it.
Where: qualifieur.md L4 ↔ qualifieur.md L41-47
Owner: qualifieur
Also in: classeur plan — classeur.md L44-51 carries the same delimitation and the same silence.

Cited: L41-42 — "📌 **You never read it whole.** 🔴 **The prompt names
the blocks to look at** — ⚠️ **load those, and no others.**"; L46-47 —
"From its `### B<n> — <title>` heading to the next heading of any
level." The tool set (L4) has `Grep` and `Read`; a numbered grep on
`^#` gives both bounds, and `Read` takes an offset and a limit — the
file just never says so.

### qualifieur.md F05 — "undo at no cost" is not what the classeur and the sondeurs do

Verdict: confirmed
Decision: Replace the claim that downstream undoes a wrong `comportement` with what downstream actually does with it — the classeur blocks when the block produces nothing, which is a Product Owner round-trip, and the sondeurs probe the rest and find nothing to ask.
Where: qualifieur.md L22-24 ↔ qualifieur.md L150-151
Owner: qualifieur
Also in: —

Cited: L22-24 — "**The Rédacteur turns every passage into a block, the
Classeur gives it a nature, the grid probes it** — 🔴 **and nobody can
refuse.**"; L150-151 — "a choice the classeur and the sondeurs undo at
no cost." The classeur's own text says what it does instead —
classeur.md L223-225: "🔴 **You block when no nature fits at all** — 📌
**which means the block produces nothing.**" — a blocking file, not an
undo, and a directive that reads as having an output (a font on the
clock) does not even reach that: it gets a nature. `3a_genre.md`
L192-194 makes the same "caught by what follows" claim and is corrected
by the same fact — see `Follows`.

Follows: 3a_genre — L192-194 "A wrong genre is caught by what follows —
the classeur finds no nature for a block that produces nothing, and the
grid probes what it left in" keys on the same claim and says the same
thing once the qualifieur's justification is made true.

### qualifieur.md F06 — majority genre versus the silent hole

Verdict: confirmed
Decision: File a two-genre block `comportement` whenever one of the two genres it calls for is `comportement`; the majority rule applies only between two genres that are both outside the grid.
Where: qualifieur.md L90 ↔ qualifieur.md L145-147
Owner: qualifieur
Also in: —

Cited: L90-91 — "📌 **Give it the genre of what it is mostly about, and
name it in your report**"; L145-147 — "🔴 **A behaviour wrongly called
anything else leaves the file the grid reads, and is never probed
again** — a silent hole." The decision is the file's own asymmetry
applied to the case L90 forgot. ⚠️ **It stands only if `## To settle` 2
keeps the majority rule at all** — a two-genre block that blocks
instead has no genre to choose.

### qualifieur.md F07 — the `MODIFIED` re-check asks the forbidden question first

Verdict: confirmed
Decision: On a `MODIFIED` block that already carries a genre, run the same procedure as on an empty one — subject first, steps 1 to 4 — and compare the genre it yields with the one carried; drop "what fires it and what it produces" as the re-check's question.
Where: qualifieur.md L329 ↔ qualifieur.md L297-303
Owner: qualifieur
Also in: —

Cited: L329 — "🔴 **Ask again what fires it and what it produces, and
compare.**"; L297-298 — "🔴 **Ask what its subject is** — ⚠️ **before
asking what fires it.**"; L302-303 — "asking about those first would
call it `comportement` every time." A rewritten `transverse` or
`directive` re-read by trigger and output is re-filed `comportement`
on every change, exactly the reading the procedure was built to avoid.

### qualifieur.md F08 — several blocked blocks, one `## Decision`

Verdict: confirmed
Decision: Adopt the classeur's blocking-file shape — a `## Blocking N` title per blocked block with the four headings repeated under each — so that every blocked block has its own `## Decision`.
Where: qualifieur.md L258-259 ↔ qualifieur.md L231-247, L267-271
Owner: qualifieur
Also in: classeur plan and redacteur plan — `passages-amont.md` F01 (classeur.md L197 ↔ redacteur.md L531: the Rédacteur reads one `## Decision`), which is the reader side of this same shape.

Cited: L258-259 — "📌 **Several blocked blocks go in one blocking
file** — 🔴 **one `## Where` entry each.**"; L231-247 — one `## What
blocks`, one `## To resume`, one `## Decision`; L267-271 — the decision
table is per block ("A genre among the six → Write it"). The classeur
already has the shape — classeur.md L196-197: "🔴 **a `## Blocking N`
title per blocked block, then four headings**, the last one left
empty" — and L233-234: "🔴 **the four headings repeated for each**".

Follows: 3a_genre — its pre-check (L34-40 "Its `## Decision` is empty →
Stop") tests one heading; with `## Blocking N` it has several to test,
and one empty among them is a block still standing. redacteur — reads
each `## Blocking N`'s decision, not the first (`passages-amont.md`
F01, decided in the classeur/redacteur plans).

### qualifieur.md F09 — "most of the five" have a trigger, says the page that says two do not

Verdict: confirmed
Decision: Name the two of the five that read as having a trigger and an output — `transverse` and `recette` — instead of "most", and keep the reason the subject is asked first.
Where: qualifieur.md L131-133 ↔ qualifieur.md L113, L119
Owner: qualifieur
Also in: —

Cited: L131-133 — "📌 **It usually has a trigger and an output** — ⚠️
**but so do most of the five above**"; L113 — "🔴 **It has no trigger
and produces nothing.**" (`directive`); L119 — "🔴 **It has no trigger
either**" (`référence`); and `hors périmètre` (L122-125) has none by
its own description. Two of five — L302 (`transverse` "usually has a
trigger and an output too") and L310-311 (`recette` "reads as a trigger
and an output") — is not "most", and those two are exactly the ones
the procedure orders before `comportement`.

### qualifieur.md F10 — "you do not grep again" beside "grep `^### B7 `"

Verdict: confirmed
Decision: Say, as the classeur does, that the orchestrator's grep is the one on empty lines and markers and that finding a block by its heading is a different grep, the agent's own.
Where: qualifieur.md L288-289 ↔ qualifieur.md L51
Owner: qualifieur
Also in: —

Cited: L288-289 — "⚠️ **Never inferred from the folder** — 📌 the
orchestrator grepped, you do not grep again."; L51 — "🔴 **Grep
`^### B7 ` — the space ends the number.**" The classeur carries the
missing sentence — classeur.md L273-274: "🔴 **you do not grep for those
again.** ⚠️ **Finding a block by its heading is another grep, and it is
yours.**"

### qualifieur.md F11 — a rewrite decision: the file is renamed before the Rédacteur sees it

Verdict: confirmed
Decision: Number the blocking file in the command that consumed its decision — `/3a_genre` renames `blocked_qualifieur.md` only when the agent reports having written the genre the decision named; when it reports that the block waits on the Rédacteur, the file stays at its unnumbered name for `/2_structure`, which renames it after the Rédacteur applies it.
Where: qualifieur.md L270 ↔ 3a_genre.md L164-167 · 2_structure.md L120
Owner: 3a_genre
Also in: classeur plan (the same route at 3b_nature.md L161-163 ↔ L236, per `chemins-amont.md` F04), redacteur plan (`chemins-amont.md` F03, `renommages.md` F10), commandes plan if either of those lands there.

Cited: qualifieur.md L270 — "**The block is to be rewritten or
removed** | 🔴 **Leave the line empty** — ⚠️ **say in your report that
the block waits on the Rédacteur**"; 3a_genre.md L164-167 — "🔴 **A
blocking file you named is filed:** git mv
docs/features/<name>/blocked_qualifieur.md
docs/features/<name>/blocked_qualifieur-NN.md" — unconditional;
2_structure.md L120 — "🔴 **A `blocked_decoupeur.md`,
`blocked_qualifieur.md` or `blocked_classeur.md` with a filled
`## Decision`** | **2 — Integrating** | 🔴 **That file**". And the relay
row that sends the Product Owner there — 3a_genre.md L231 — "A
`## Decision` names a rewrite | 🔴 **`/2_structure`** — 📌 **it names
the blocking file to the Rédacteur**". Renamed, the file matches
nothing in L120, and the genre stays empty with L233 sending `/3a_genre`
round again. The command cannot tell the two cases apart by reading the
decision (L42: "Read that one heading, nothing else"), so it keys on
the agent's report — which L270 already makes it say.

Follows: qualifieur — the report line "the block waits on the
Rédacteur" (L270) becomes the value the command keys on, and has to be
said in those terms every time. 2_structure — L191-194 renames only
`blocked_decoupeur.md` after applying; it renames whichever of the
three it applied (`chemins-amont.md` F03). 3b_nature — the same
unconditional rename at L161-163, for `blocked_classeur.md`.

### qualifieur.md F12 — the price of a silent `transverse`

Verdict: confirmed
Decision: Correct the stated price of a rule wrongly called `comportement` — for a `transverse` it is not one grid question too many but the rule missing from the list the sondeurs hold, so every block it reaches raises the gap by hand; whether that doubt stays silent is `## To settle` 1.
Where: qualifieur.md L143-145 ↔ 4_grille.md L138-146
Owner: qualifieur
Also in: —

Cited: qualifieur.md L143-145 — "📌 **A rule wrongly called
`comportement` costs one grid question too many** — the sondeurs probe
it and find nothing to ask."; 4_grille.md L139-140 — "🔴 **A second
grep, `grep -B1 '^Genre: transverse$'`** — 📌 **and their identifiers go
in every sondeur's prompt, as a list of their own.**"; L142-144 — "a
question a transverse rule already answers becomes a *défaut*, not a
gap the Product Owner has to close by hand." A `transverse` filed
`comportement` is not in that grep, so it is not beside the sondeurs,
and the *défaut* route does not fire for it. The price statement is
false for that genre whatever the policy; the policy itself is not
mine.

### qualifieur.md F13 — the per-block genre list stops at the orchestrator

Verdict: confirmed
Decision: Relay the agent's per-block genre list to the Product Owner in `/3a_genre`'s report, beside the counts.
Where: qualifieur.md L351-354 ↔ 3a_genre.md L216-222
Owner: 3a_genre
Also in: —

Cited: qualifieur.md L351-354 — "🔴 **And the genre you gave each
block, one line each.** ⚠️ **A behaviour wrongly filed as anything else
leaves the file the grid reads, and nobody downstream catches it** — 📌
**that list is the only place the Product Owner can see one before the
grid closes.**"; 3a_genre.md L218-222 — "📌 **How many blocks were
qualified**, which changed genre, and how many questions. 🔴 **Nothing
else is yours**: no reading of what a block says." Relaying a list the
agent wrote is not reading a block; the "nothing else" line has to make
room for it or the agent's stated purpose for the list is void.

Follows: qualifieur — none to rewrite; the list already exists at
L351.

### qualifieur.md F14 — a two-genre block has no way back to the decoupeur

Verdict: confirmed
Decision: — (see `## To settle` 2)
Where: qualifieur.md L356-358 ↔ 3a_genre.md L227-235
Owner: 3a_genre for the route, qualifieur for what it does meanwhile
Also in: decoupeur plan, if the route chosen sends the block there.

Cited: qualifieur.md L356-358 — "📌 **And any block whose sentences
called for two genres** — 🔴 **by identifier, with the two you read.**
⚠️ **The decoupeur should have split it**, and nothing else would show
it."; 3a_genre.md L227-235 — seven *next* rows, none for that report.
The decoupeur does own the split — decoupeur.md L65-67: "📌 **the
qualifieur gives a genre per block**, and a constraint left inside a
behaviour would take the behaviour's." But `/3_decoupe` looks only at
`NEW` and `MODIFIED` blocks (3_decoupe.md L81-82), and the qualifieur
may not set a marker (qualifieur.md L209). A route needs a mechanism
that does not exist yet, and choosing one is a cost question for the
Product Owner.

### qualifieur.md F15 — the answered file at the root: named, or a stop

Verdict: confirmed
Decision: Look for the agent's answered file under `questions/qualifieur/` only, and keep the stop on any root file holding a `### Q` — a qualifieur file still at the root has not been through `/1_lexique` and `/2_structure`, which is where its answers are integrated and the file is put away.
Where: qualifieur.md L188-189 ↔ 3a_genre.md L50-54, L68-70
Owner: 3a_genre
Also in: classeur plan (3b_nature.md L51 ↔ L67, same two rules), commandes plan if `chemins-amont.md` F06 lands there.

Cited: 3a_genre.md L50-54 — "📌 **The highest `questions-qualifieur-NN.md`,
at the root or under `questions/qualifieur/`** — ⚠️ **the root first**:
a file answered and not yet filed sits there … ⚠️ **name it in the
prompt when it holds at least one `### Q`.**"; L68-70 — "🔴 **Grep
`^### Q` in each before touching it** — 📌 **a file holding questions is
not yours to file** … 🔴 **Stop and say which.**" One state, two
outcomes. The route settles which: the relay row L234 sends an answered
file through `/1_lexique`, and `/2_structure` L200-201 files "the
questions file it integrated, into `questions/<agent>/`" — so the
prompt template at L148 naming only the `questions/qualifieur/` path is
the one that matches the designed route. The qualifieur's side
(L188-189, "the prompt names the questions file you wrote last turn")
needs no change.

Follows: qualifieur — none; the prompt still names one file.

### qualifieur.md F16 — "two commands later", counted from two places

Verdict: confirmed
Decision: Give the distance from `/3a_genre` correctly — `/5_reclasse` is three commands on — or name `/5_reclasse` without counting.
Where: qualifieur.md L273-274 ↔ CLAUDE.md L52
Owner: qualifieur
Also in: —

Cited: qualifieur.md L273-274 — "📌 **it would pass `/3a_genre`'s check
and stop `/5_reclasse` two commands later.**"; L61-63 — counts from
`/3b_nature` and `/4_grille` and gets two; `.claude-new/CLAUDE.md` L52 —
"`/1_lexique` · `/2_structure` · `/3_decoupe` · `/3a_genre` ·
`/3b_nature` · …" with `/4_grille` and `/5_reclasse` on L53-54 — from
`/3a_genre` the count is three.

---

## The thematic reports' findings

### renommages.md F10 — a filled blocking file consumed by two commands

Verdict: confirmed
Decision: Same as `qualifieur.md` F11 — the command that consumed the decision renames the file; `/3a_genre` and `/3b_nature` rename only on a genre or a nature written, `/2_structure` renames whichever of the three it applied.
Where: 2_structure.md L120 ↔ 3b_nature.md L38 (and 3a_genre.md L40)
Owner: 3a_genre and 3b_nature for the conditional rename, 2_structure for the rename after applying
Also in: classeur plan, redacteur plan.

Cited: 2_structure.md L120 — "🔴 **A `blocked_decoupeur.md`,
`blocked_qualifieur.md` or `blocked_classeur.md` with a filled
`## Decision`** | **2 — Integrating**"; 3a_genre.md L40 — "Its
`## Decision` is filled | 📌 **Name it in the prompt**"; 3b_nature.md
L38 — the same row for `blocked_classeur.md`; 2_structure.md L191-192 —
"🔴 **A `blocked_decoupeur.md` it applied is renamed**" and no other.
Whichever of the two runs first today, either the rewrite never fires
(renamed by `/3a_genre`) or the file is named twice (left by
`/2_structure`).

### passages-amont.md F03 — the Rédacteur credits the vocabulary to the qualifieur

Verdict: confirmed
Decision: Credit the vocabulary to the lexicographe.
Where: redacteur.md L323 ↔ lexicographe.md L181
Owner: redacteur
Also in: redacteur plan.

Cited: redacteur.md L321-323 — "🔴 **Write anything in `lexique.md` but
an `en anglais` line** — ⚠️ **never an entry, never a term**: the
vocabulary is the qualifieur's". Nothing in `qualifieur.md` names
`lexique.md` or a term; L36-39 list what it reads and the lexicon is
not there. No change on the qualifieur's side.

### chemins-amont.md F03 — only the decoupeur's file is renamed after a rewrite

Verdict: confirmed
Decision: Same as `qualifieur.md` F11 — `/2_structure` renames whichever of the three blocking files it named to the Rédacteur, once applied.
Where: 2_structure.md L120 ↔ 2_structure.md L191
Owner: 2_structure
Also in: redacteur plan, classeur plan.

Cited: 2_structure.md L191-194 — "🔴 **A `blocked_decoupeur.md` it
applied is renamed** — `blocked_decoupeur-NN.md`, the highest in the
folder plus one." — the other two are not mentioned, and row L120
fires on them again on every later run.

### chemins-amont.md F04 — the numbered file that `/2_structure` cannot find

Verdict: confirmed
Decision: Same as `qualifieur.md` F11.
Where: 3a_genre.md L164 ↔ 2_structure.md L120
Owner: 3a_genre
Also in: classeur plan (3b_nature.md L161 ↔ L236).

Cited: as under F11. This is the command-side statement of the same
defect.

### chemins-amont.md F06 — root-first, or stop on a root file

Verdict: confirmed
Decision: Same as `qualifieur.md` F15.
Where: 3a_genre.md L52 ↔ 3a_genre.md L68
Owner: 3a_genre
Also in: classeur plan (3b_nature.md L51 ↔ L67).

Cited: as under F15. The finding adds that "the prompt template only
ever names the `questions/qualifieur/` path" — 3a_genre.md L147-148:
"<Plus: your answered questions file:
docs/features/<name>/questions/qualifieur/questions-qualifieur-NN.md.>"
— which is the side F15 keeps.

---

## To settle

### 1. A *transverse-or-behaviour* doubt — silent, or a question (F12, F01, F05)

The file settles every genre doubt as `comportement` without a question
(L140-141), and the report's part 2 records that the earlier "you still
raise it as a question" rule was removed on purpose (D3: "doubt 1 is now
silent"). F12 shows the price given for that silence is false for one
genre: a `transverse` filed `comportement` is absent from the list
`/4_grille` hands the sondeurs (4_grille.md L139-140), so the rule is
not beside them and every block it reaches raises the gap as a question
the Product Owner answers by hand, once per block.

| Option | What it costs |
|---|---|
| **Keep the silence as it is** — any doubt → `comportement` | A `transverse` in doubt is probed as a behaviour, and its rule is asked of the Product Owner on every block it reaches; with F13 relayed she sees the per-block genre list and can catch it, by hand, before `/3b_nature` |
| **Ask on the `transverse` doubt only** — the four other doubts stay silent | One question per such doubt, answered before `/3b_nature`; the *dozens of questions* D3 feared came from asking on every doubt, and the `transverse` doubt is the one whose silent side is not cheap |
| **Default the doubt to `transverse`** | Never — a behaviour filed `transverse` is not probed (4_grille.md L142), the silent hole L145-147 names |

The plan stops here for F12's policy; its price statement is corrected
whichever option is taken.

### 2. A two-genre block — how it gets back to the decoupeur (F14, F06, F02)

The qualifieur reports a block whose sentences call for two genres, and
gives it the majority genre meanwhile (L88-91). Nothing sends it back:
`/3a_genre` has no *next* row for that report (L227-235), `/3_decoupe`
looks only at `NEW` and `MODIFIED` blocks (3_decoupe.md L81-82), and
the qualifieur may not set a marker (L209). The decoupeur does own the
split (decoupeur.md L65-67).

| Option | What it costs |
|---|---|
| **The qualifieur blocks on it** — `blocked_qualifieur.md`, decision, `/2_structure` names it to the Rédacteur, who rewrites with `MODIFIED`, then `/3_decoupe` splits | One Product Owner round-trip per such block; consistent with 2_structure.md L120 ("all three block on something only a rewrite of the block settles") and with F11's route; the majority rule (L88-91) and F06 go away |
| **Keep the majority genre and the report, add a relay row** | The Product Owner learns of it and nothing runs; the block is coded under one genre with a constraint inside it — the outcome decoupeur.md L66-67 names as the reason the split exists; F06's rule then has to stand |
| **A `/3a_genre` next row that runs `/3_decoupe` on the named blocks** | `/3_decoupe` needs a way to take a block list it does not grep for — a new parameter on a command that today takes a feature name only; the qualifieur's report becomes the command's input |

The plan stops here for F14; F06's decision holds only under the second
or third option.
