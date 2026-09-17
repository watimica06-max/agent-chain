# Plan — `arbitre.md`

Base: `.claude-new/agents/arbitre.md` (463 lines), local HEAD.

Commands read: the five that name the Arbitre — `7_lots.md` L177,
`8_code.md` L231, L340, L410, `9_controle.md` L271, L289, L301,
`audit_blocages.md` L92-94, L114, `socle.md` L28. None invokes it:
`7_lots.md` L177 and `8_code.md` L410 both say the orchestration never
does; only the Détailleur (detailleur.md L327-333) and the Réalisateur
(realisateur.md L298-304) call it.

Not opened: the `technical-state-format` skill — it sits under
`.claude/`, off-limits. Two entries below (F03, F18) depend on the trap
heading it defines and say so.

Cluster: F09, F10, F16, F17, renommages F07, passages-aval F11 and
chemins-aval F20 are one defect seen from seven sides — what a
handed-back `## Decision` looks like, and what its readers test on. F17
carries the decision; the others cite it.

---

## Findings of `docs/verification2/arbitre.md`

### arbitre.md F01 — the index records one write, the file declares three

Verdict: confirmed
Decision: Correct the index entry so it records the three writes outside the blocking file.
Where: modifications.md L1284 ↔ arbitre.md L219-222
Owner: `docs/refonte/modifications.md` (the index) — no agent line changes
Also in: —

Cited: modifications.md L1284 — "🔴 **sa seule écriture hors fichier de
blocage est un piège**". arbitre.md L220-222 — "Your three writes
outside a blocking file: a trap in `CURRENT_TECHNICAL_STATE.md`,
`code/redecoupage.md`, and a request in `architecte/`". The agent side
is the accurate one: `8_code.md` L340 relies on `code/redecoupage.md`
and the report lists the Architecte contract as sound.

### arbitre.md F02 — three destinations skip the Architecte, or two

Verdict: confirmed
Decision: Correct the index summary to two destinations that skip the Architecte.
Where: modifications.md L1283 ↔ arbitre.md L371-379
Owner: `docs/refonte/modifications.md` (the index)
Also in: —

Cited: modifications.md L1283 — "Quatre destinations, dont trois ne
vont pas à l'Architecte". arbitre.md L371-372 — "two of the four
answers do not go to the Architecte". The index's own table contradicts
its summary: L1303 sends the rule-now-wrong case to "Les conventions,
en remplacement — et le Product Owner arbitre".

### arbitre.md F03 — `## Traps` as the trap's destination

Verdict: confirmed
Decision: Align the index line on the heading the `technical-state-format` skill defines; arbitre.md L391-393 is the side to keep if the skill confirms it.
Where: modifications.md L1283 ↔ arbitre.md L391-393
Owner: `docs/refonte/modifications.md` (the index)
Also in: —

Cited: modifications.md L1283 — "un piège de plateforme → **`## Traps`**,
qu'il écrit lui-même". arbitre.md L391-393 — "`## Traps — general` when
several subjects meet it, under the subject's own `###` heading when
one owns it. `## Traps` alone is not a heading of that file." Not
verified: which heading the skill actually defines — whoever applies
opens it first. Same dependency as F18.

### arbitre.md F04 — the Contrôleur dropped, index silent

Verdict: confirmed
Decision: Record in the index that the Contrôleur is no longer named among the blocks that are not the Arbitre's.
Where: arbitre.md L148 ↔ modifications.md L1276-1285
Owner: `docs/refonte/modifications.md` (the index)
Also in: —

Cited: arbitre.md L148-149 — "When a block is not yours — a Relecteur's
or an Architecte's". The index entry L1276-1285 has no line for it. The
agent side holds: the table at L247-251 covers it with "Anything else →
No", and `8_code.md` L415-416 says "The Relecteur and the Contrôleur do
not call it either".

### arbitre.md F05 — two Verdict outcomes added, index silent

Verdict: confirmed
Decision: Record the two added outcomes in the index.
Where: arbitre.md L429-431 ↔ modifications.md L1276-1285
Owner: `docs/refonte/modifications.md` (the index)
Also in: —

Cited: arbitre.md L429 — "A rule already carries it — The commonest
outcome"; L431 — "Refused, and it says what would settle it — Settle
from that". Both match the Architecte's own outcome table
(architecte.md L735 "Already carried", L737 "Not a convention — Say
where it belongs"); nothing on the agent side to change.

### arbitre.md F06 — `Bash` and `Skill` entered the tools, index silent

Verdict: confirmed
Decision: Record in the index that `Bash` (bound to `sleep`) and `Skill` (for `technical-state-format`) entered the tools.
Where: arbitre.md L4 ↔ modifications.md L1276-1285
Owner: `docs/refonte/modifications.md` (the index)
Also in: —

Cited: arbitre.md L4 — "tools: Read, Grep, Glob, Edit, Write, Bash,
Skill, Agent"; L443-444 — "that is the only command your `Bash` runs".
Whether `Bash` stays at all depends on To settle 1.

### arbitre.md F07 — `## Status` line only, no tool named

Verdict: confirmed
Decision: Name Grep as the tool that reads the `## Status` line, and match it on the `PASS` prefix.
Where: arbitre.md L100 ↔ arbitre.md L4
Owner: arbitre
Also in: —

Cited: arbitre.md L100-101 — "`code/<lot>/verdict.md`, its `## Status`
line only — only when the split itself is what is wrong"; L348 —
"every lot whose verdict.md carries PASS". The prefix match is
decisions.md `passages-aval.md` F15 ("Every reader matches the `PASS`
prefix"); the Arbitre is a reader that list did not name, and L348
reads as an exact match.

### arbitre.md F08 — `Glob` has no stated use

Verdict: confirmed
Decision: Say that Glob finds the settled `-NN` files beside the blocking file and every lot's `verdict.md`.
Where: arbitre.md L4 ↔ arbitre.md L32
Owner: arbitre
Also in: —

Cited: `Glob` appears at L4 only; L32-33 "Its blocking files already
settled sit beside it, numbered" and L88 name no tool; L348 needs every
lot's verdict. The numbering scheme is the orchestration's
(`8_code.md` L170 "`NN`: the highest in that folder plus one").

### arbitre.md F09 — an unanswered entry has two shapes

Verdict: confirmed
Decision: Give the unsettled entry one shape — its number present, carrying the hand-back line of F17 — at L165-167, L181 and L216-217.
Where: arbitre.md L165-167 ↔ arbitre.md L181
Owner: arbitre
Follows: detailleur (L346 "Some numbers answered, others not"), realisateur (L318, same row)
Also in: detailleur, realisateur

Cited: arbitre.md L165-167 — "A number with no answer is an entry still
waiting … an empty number is the signal"; L181 — "on a multi-entry one,
its number is simply absent"; L216-217 — "the same exception is a
number with no answer". Three lines, two shapes. The callers' row
survives either shape but must name the one kept.

### arbitre.md F10 — multi-entry file and the wait branch

Verdict: confirmed
Decision: Write the settled numbers into `## Decision` before any wait begins; the wait — if it is kept, see To settle 1 — bears on the handed-back numbers only and changes nothing already written.
Where: arbitre.md L173-176 ↔ arbitre.md L441-456
Owner: arbitre
Also in: —

Cited: arbitre.md L173-174 — "settle the others and write no answer
under that number"; L441 — "Leave `## Decision` empty and poll the
blocking file"; L456 — "stop, leaving `## Decision` empty". The second
and third lines describe a single-entry file only.

### arbitre.md F11 — the wait has no found-answer branch, and the rule-now-wrong row leads nowhere

Verdict: confirmed
Decision: —
Where: arbitre.md L441-462 ↔ arbitre.md L379
Owner: arbitre
Also in: —

Cited: arbitre.md L379 — "The Product Owner first … Then the Architecte,
with her answer in `## What I need`"; L441-462 describe the empty
outcome alone — no row for the poll finding her answer. Not decided
because the route depends on whether the poll exists at all: see To
settle 1, which carries both options and what this row needs under
each.

### arbitre.md F12 — "no other", then "read the settled ones beside it"

Verdict: confirmed
Decision: Reword L82 so that "no other" excludes only other open blocking files; the settled numbered ones are read.
Where: arbitre.md L82 ↔ arbitre.md L88
Owner: arbitre
Also in: —

Cited: arbitre.md L82 — "The blocking file the prompt names, and no
other."; L88-89 — "Blocking files already settled sit beside it,
numbered. Read them". L32-34 says the same as L88.

### arbitre.md F13 — `architecte/arbitre-<lot>.md` on a multi-entry file

Verdict: confirmed
Decision: Make it one request per invocation, gathering every entry that needs a rule, and name the file by the blocking file's scope — the block for `code/blocked_detailleur.md`, the lot for `code/<lot>/blocked_realisateur.md`.
Where: arbitre.md L402 ↔ arbitre.md L218
Owner: arbitre
Follows: architecte (L666 keys the Arbitre's request on `architecte/arbitre-<lot>.md`)
Also in: architecte

Cited: arbitre.md L402 — "Write `architecte/arbitre-<lot>.md`"; L218 —
"Ask the Architecte twice for one block"; architecte.md L665-666 — "Or
the Arbitre, which is blocked on one and is waiting for you — its
request is `architecte/arbitre-<lot>.md`". A `code/blocked_detailleur.md`
carries entries on several lots (detailleur.md L284-285), so `<lot>`
names nothing there.

### arbitre.md F14 — "English" against the French headings of `code/redecoupage.md`

Verdict: confirmed
Decision: Say at L193 that the rule bears on prose, and that a file's headings follow the contract that names them.
Where: arbitre.md L193 ↔ arbitre.md L337-355
Owner: arbitre
Also in: —

Cited: arbitre.md L193 — "English, like every file the agents read";
L337-354 — `## Ce qui bloque`, `## Où`, `## Ce qui est déjà codé`,
`## Ce qui ne l'est pas`, `## Ce que le découpage doit permettre`. The
headings are a shared contract: cadreur.md L907-913 appends `## Ce qui
revient` and `## Ce que j'en fais` to the same file, and `8_code.md`
L349-350 relays them by those names. Translating them would touch three
files for a NOTE; the sentence at L193 is what to narrow.

### arbitre.md F15 — the folder test misreads every Détailleur block

Verdict: confirmed
Decision: Key what a block bears on to the entry's heading (`## Blocking N — lot-NN`) and the file's author, never to the folder; open the lot's sheet and report whenever the entry names a lot.
Where: arbitre.md L84-86 ↔ detailleur.md L284-285
Owner: arbitre
Follows: detailleur (the `— lot-NN` suffix at L292 becomes a contract to keep, and an entry without one bears on the split as a whole)
Also in: detailleur (as passages-aval F05)

Cited: detailleur.md L284-285 — "Write `code/blocked_detailleur.md` —
at the split's root, not under a lot: it may carry stops on several";
L292 — "## Blocking 1 — lot-04". arbitre.md L84-86 — "In the split's
own folder — the block bears on the split as a whole, and no lot exists
yet"; L98-99 — "The lot's sheet and report — only when the block bears
on a lot".

### arbitre.md F16 — a half-answered file is archived unanswered

Verdict: confirmed
Decision: Make every reader key on the hand-back line of F17, never on filled-or-empty: `/8_code` 4b renames only when no entry carries it and stops the run, relaying, when one does; the Détailleur's and the Réalisateur's after-call and PART 2 tables gain the half-answered state.
Where: arbitre.md L176 ↔ 8_code.md L168-170
Owner: arbitre (the field's form)
Follows: 8_code (L50-51, L167-170, L406-416, L428-429), detailleur (L343-347, L434-441), realisateur (L314-319, L500-506)
Also in: detailleur, realisateur (as renommages F07, passages-aval F11)

Cited: 8_code.md L169 — "Filled → Name it in the agent's prompt, and
rename it once the agent reports having applied it"; L50-51 — "Whether
its `## Decision` is filled, nothing more of it". detailleur.md L346 —
"Some numbers answered, others not → Apply the answered ones — stop on
the entries they do not cover", and its PART 2 table L434-441 has no
such row; realisateur.md L318 and L500-506 likewise. arbitre.md L176 —
"the missing number is what says that entry still waits".

### arbitre.md F17 — a product question handed back writes nothing

Verdict: confirmed
Decision: Hand a product question back with a line in `## Decision` — `Not settled here.`, who settles it, and the behaviour it turns on — at file level or under the entry's number, and drop the rule that an empty field or an absent number is the signal (L165-167, L178-187, L215-217, L456-462).
Where: arbitre.md L460-462 ↔ audit_blocages.md L112-115
Owner: arbitre
Follows: detailleur (L347 "Still empty" row becomes the hand-back row; L438 already has it), realisateur (L318, L505 same), 8_code (4b test; L428-429 "The Product Owner fills `## Decision`" becomes: replaces the line), 9_controle (L271 unchanged — it gains the trace it reads), audit_blocages (L112-115 unchanged — it is what the line serves)
Also in: detailleur, realisateur

Cited: audit_blocages.md L112-114 — "A `## Decision` opening on *not
settled here*. Quote the reason it gives, and nothing more — the
Arbitre wrote which behaviour it turned on, or what the corpus does not
say." arbitre.md L460-462 — "do not write anything into `## Decision`,
not even a note. An empty field is what the caller tests on." The
Arbitre already has the line's form at L151-153 for a block that is not
its own; both callers' PART 2 tables already stop on it (detailleur.md
L438, realisateur.md L505); only the empty-field rule isolates the
product question from every reader that expects a trace.

⚠️ This reverses a rule the refonte wrote on purpose (L183-187,
L456-462, index D6/D7). If wave 2 keeps the empty field instead: F09,
F16, renommages F07 and passages-aval F11 must then key the
orchestration's rename on the caller's report rather than the file, and
audit_blocages finding 4 stays blind to every product question.

### arbitre.md F18 — the Réalisateur looks for a `## Traps` section

Verdict: confirmed
Decision: Align realisateur.md L135 on the heading the `technical-state-format` skill defines — the one arbitre.md L391-393 names, if the skill confirms it.
Where: realisateur.md L135 ↔ arbitre.md L391-393
Owner: arbitre (loads the skill and writes the trap)
Follows: realisateur
Also in: realisateur

Cited: realisateur.md L134-135 — "and the Arbitre — which writes its
`## Traps` section"; arbitre.md L393 — "`## Traps` alone is not a
heading of that file". Not verified: the skill itself (under
`.claude/`). Same dependency as F03.

### arbitre.md F19 — the `##` single-entry shape no caller writes

Verdict: confirmed
Decision: Keep one blocking-file shape — `## Blocking N` with `###` headings and one `## Decision`, even for one entry: the Réalisateur drops its second shape, the Arbitre drops the `##` single-entry reading at L129-130 and the "single-entry file" wording at L180.
Where: arbitre.md L129-130 ↔ detailleur.md L292-293
Owner: realisateur (its L272-286 is the stray shape)
Follows: arbitre, detailleur (nothing to change — L292-293 already states the shape)
Also in: realisateur (as renommages F05, passages-aval F13), detailleur (as renommages F06)

Cited: detailleur.md L292-293 — "one `## Blocking N` per stop, even when
there is only one, and one `## Decision` at the end, whatever the
count"; realisateur.md L258-259 — the same sentence, then L272-286 —
"The headings of an entry: ## What blocks … ## Decision <left empty>".
arbitre.md L129-130 — "`##` in a single-entry file, `###` under each
`## Blocking N` in a multi-entry one."

### arbitre.md F20 — the multi-entry file attributed to the Détailleur alone

Verdict: confirmed
Decision: Attribute the multi-entry file to both callers.
Where: arbitre.md L159-160 ↔ realisateur.md L251-253
Owner: arbitre
Also in: —

Cited: realisateur.md L251-253 — "A second lack you meet while carrying
on is added to the blocking file — it never replaces the first. One
entry each, and the Arbitre answers both." arbitre.md L159-160 — "the
Détailleur files everything one walk found, at once."

### arbitre.md F21 — `socle.md` names the Réalisateur as the only loader

Verdict: confirmed
Decision: Name the Arbitre in `socle.md` as a writer of `CURRENT_TECHNICAL_STATE.md` (traps) and a loader of the skill, beside the Réalisateur.
Where: arbitre.md L388 ↔ socle.md L43
Owner: socle (command)
Also in: — (the commands plan does not carry it: the finding names this agent)

Cited: socle.md L27-28 — "The Réalisateur writes into it from the first
lot, and the Détailleur, the Diagnostiqueur and the Arbitre read it";
L42-43 — "the `technical-state-format` skill, which the Réalisateur
loads before writing". arbitre.md L388-389 — "Load the
`technical-state-format` skill before writing to it"; L377 — "write it
there yourself".

---

## Findings of the thematic reports

### renommages.md F05 — the Réalisateur's blocking file has two shapes

Verdict: confirmed
Decision: Same as arbitre.md F19.
Where: realisateur.md L258 ↔ realisateur.md L274
Owner: realisateur
Follows: arbitre
Also in: realisateur

Cited: realisateur.md L258-259 and L272-286, quoted under F19.

### renommages.md F06 — the single-entry shape never reaches the Arbitre

Verdict: confirmed
Decision: Same as arbitre.md F19.
Where: arbitre.md L130 ↔ detailleur.md L292
Owner: realisateur
Follows: arbitre
Also in: detailleur

### renommages.md F07 — the waiting entry is archived as settled

Verdict: confirmed
Decision: Same as arbitre.md F16 and F17.
Where: arbitre.md L165 ↔ 8_code.md L170
Owner: arbitre
Follows: 8_code, detailleur, realisateur
Also in: detailleur

Cited: 8_code.md L169-170 and detailleur.md L434-441, quoted under F16.
BLOCKING in the report; the decision under F16/F17 is what closes it.

### fichiers.md F16 — the relay of `## Ce qui revient` reads headings not yet written

Verdict: confirmed
Decision: Relay the two sections after `/7_lots` returns, from the archived `code/redecoupage-NN.md`.
Where: 8_code.md L352 ↔ cadreur.md L909
Owner: 8_code (command)
Follows: — (the Arbitre's template L337-355 is right not to carry them)
Also in: cadreur; commands (as chemins-aval F02, which names no agent)

Cited: 8_code.md L349-351 — "Relay the `## Ce qui revient` and `## Ce
que j'en fais` of `code/redecoupage.md` — the Cadreur wrote them there
at the end of its round", placed before L365 "Then run `/7_lots`";
cadreur.md L907 — "Write both of these into `code/redecoupage.md`, at
the end"; 7_lots.md L98-99 — "git mv code/redecoupage.md
code/redecoupage-NN.md".

### chemins-aval.md F11 — the poll runs inside the worktree

Verdict: confirmed
Decision: —
Where: arbitre.md L441 ↔ 8_code.md L204
Owner: arbitre
Also in: —

Cited: 8_code.md L204-206 — "from the main checkout, never from a
worktree: a worktree holds a copy frozen at its creation and would
never see a file created after it"; L93-94 — "One worktree for the
whole run … Enter it before invoking anything". arbitre.md L441 —
"Leave `## Decision` empty and poll the blocking file". The blocking
file exists only in the worktree, uncommitted, and nobody can tell the
Product Owner a question is pending while the orchestrator is blocked
on the chain. Whether the wait survives is To settle 1.

### chemins-aval.md F20 — `Not settled here.` reads as filled

Verdict: confirmed
Decision: Same as arbitre.md F16 — `/8_code` 4b keys on the hand-back line, and a file carrying it stops the run instead of re-invoking.
Where: 8_code.md L50 ↔ arbitre.md L153
Owner: arbitre
Follows: 8_code
Also in: —

Cited: 8_code.md L50-51 — "Whether its `## Decision` is filled, nothing
more of it"; detailleur.md L438 — "A `## Decision` reading `Not settled
here.` → Nothing was settled … stop, and relay that line".

### passages-aval.md F05 — lot-level blocks settled without the lot's inputs

Verdict: confirmed
Decision: Same as arbitre.md F15.
Where: arbitre.md L84-86, L98-99 ↔ detailleur.md L284-285, L295
Owner: arbitre
Follows: detailleur
Also in: detailleur

### passages-aval.md F11 — the half-answered file is archived

Verdict: confirmed
Decision: Same as arbitre.md F16 and F17.
Where: arbitre.md L165-167 ↔ detailleur.md L346, L434-441, 8_code.md L167-170
Owner: arbitre
Follows: detailleur, realisateur, 8_code
Also in: detailleur

### passages-aval.md F13 — two Réalisateur shapes, one keyed by the Arbitre

Verdict: confirmed
Decision: Same as arbitre.md F19.
Where: realisateur.md L258, L272-286 ↔ arbitre.md L129-130
Owner: realisateur
Follows: arbitre
Also in: realisateur

### passages-aval.md F14 — "a product decision" in two Architecte rows

Verdict: confirmed
Decision: Apply decisions.md — the Architecte's *Not a convention* row no longer ends on "a product decision"; the Arbitre keys its two refusal rows on the two wordings: *Not a convention — here is where it belongs* → settle from that, *This is a product decision* → hand back to the Product Owner.
Where: architecte.md L736-737 ↔ arbitre.md L431-432
Owner: architecte
Follows: arbitre (L431-432)
Also in: architecte

Cited: architecte.md L736 — "Not a convention — Say where it belongs:
the code, the tooling, the machine, a product decision"; L737 — "A
doubt, or a product decision — Say so in the verdict". arbitre.md L431
— "Refused, and it says what would settle it — Settle from that";
L432 — "Refused, and nothing else would settle it — Wait for the
Product Owner". Settled by decisions.md `passages-aval.md` F14; not
reopened.

---

## To settle

### 1. The twenty-minute wait on the Product Owner

Findings: chemins-aval F11, arbitre.md F10, F11; touches F06.

The Arbitre polls the blocking file for twenty minutes (arbitre.md
L439-462), a mechanism `CLAUDE.md` L146 names on purpose — "Only a wait
on the Product Owner is polled, and only the `arbitre` does it". It
runs inside the `/8_code` worktree, on a file that exists nowhere else
and that nobody can point the Product Owner to while the chain is
blocked (8_code.md L93-94, L204-206). Whether it stays is a matter of
intent.

**A. Remove the wait.** The Arbitre hands back at once with the line of
F17; the caller stops; the orchestrator relays (8_code.md L428-429);
the Product Owner answers in `## Decision`; the next `/8_code` applies
it (8_code.md L437-439, already written). Costs: `CLAUDE.md` L146 and
the Arbitre's description at L3 ("otherwise waits for the Product
Owner"), L439-462, L223-224, L178-181 rewritten; `Bash` leaves the
tools (F06); detailleur.md L347 and realisateur.md L318 lose "and the
Product Owner has not either". The *rule in force that is now wrong*
row (L379) then needs a route across two runs: who writes the
`architecte/` request once her answer is in the file — the caller that
applies it cannot, the Arbitre is not re-invoked on a filled field.
Saves twenty minutes per product question.

**B. Keep the wait.** It ends empty every time unless the Product Owner
watches the worktree by herself: twenty minutes per product question,
per run. F11 then needs its found-answer branch written (apply her
answer; for L379, write the `architecte/` request with it and call the
Architecte). Whether the uncommitted blocking file even reaches the
main checkout after the stop is an `/8_code` matter (L463-466), outside
this plan.

Decision: —
