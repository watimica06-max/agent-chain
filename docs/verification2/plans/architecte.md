# Plan — architecte

Built against `.claude-new/agents/architecte.md` (826 lines), the three
commands that invoke it (`conventions.md`, `7_lots.md`, `8_code.md`),
`docs/verification2/architecte.md` (both parts), `decisions.md`, and the
six thematic reports filtered on `architecte`. Every line number below
was opened in this worktree; every `Cited:` line is quoted from the
other side of the `Where`.

Findings owned by another agent are kept here only when the architecte
file, or a command that invokes it, has a line to change — or to state
that it has none.

---

## Verdicts at a glance

| Finding | Verdict | Decision below |
|---|---|---|
| architecte.md F01 | confirmed | yes |
| architecte.md F02 | confirmed | yes |
| architecte.md F03 | confirmed | yes |
| architecte.md F04 (+ B-4) | confirmed | yes |
| architecte.md F05 | confirmed | yes |
| architecte.md F06 | confirmed | yes |
| architecte.md F07 | confirmed | yes |
| architecte.md F08 | confirmed | yes |
| architecte.md F09 | confirmed | yes |
| architecte.md F10 | confirmed | yes |
| architecte.md F11 | confirmed | yes |
| architecte.md F12 | confirmed | yes |
| architecte.md F13 | confirmed | yes |
| architecte.md F14 | confirmed | yes |
| architecte.md F15 | confirmed | yes |
| architecte.md F16 | confirmed | yes |
| architecte.md F17 | confirmed | yes |
| architecte.md F18 | confirmed | yes |
| architecte.md F19 | confirmed | yes |
| architecte.md F20 | confirmed | yes — owner arbitre |
| architecte.md F21 | confirmed | **To settle** |
| architecte.md C5 · C-5 · D-2 | confirmed | yes |
| architecte.md B-2 | confirmed | yes |
| architecte.md B-6 | confirmed | yes |
| architecte.md D-5 | confirmed | yes |
| architecte.md D-22 | overstated | no |
| architecte.md C-6 · C-7 | overstated | no |
| fichiers.md F03 | confirmed | yes — owner 2_structure |
| fichiers.md F04 | confirmed | yes — owner 7_lots |
| chemins-amont.md F19 | confirmed | guard decided; wording **To settle** |
| chemins-aval.md F18 | confirmed | yes — owner audit_blocages |
| chemins-aval.md F24 | confirmed | yes — owner 8_code |
| passages-aval.md F10 | confirmed | yes — owner detailleur |
| passages-aval.md F14 | settled (decisions.md) | applied here |
| renommages.md F16 | settled (decisions.md) | applied here |

---

## Part 1 — the report's findings

### architecte.md F01 — C6 applied differently than asked

Verdict: confirmed
Decision: Record C6 in the pass sheet as applied in part, by design —
the `off-grid` mark stays on the rule as a fifth field, the entry
citations alone moved to the coverage line.
Where: docs/refonte/passes/architecte.md L190-192 ↔ architecte.md
L128, L195-198; docs/refonte/modifications.md L647-649 (C6 among
"Passés (27)")
Cited: passes/architecte.md L190-192 — "the mark and the citations live
in one place, the coverage line; the rule in the conventions file
carries nothing that says where it came from"
Cited: architecte.md L195-197 — "The rule itself carries it too, in the
conventions file — it is what tells a reader the grid did not ask for
this one."
Owner: the applier of this plan, in `docs/refonte/modifications.md` —
not the agent file, whose L195-197 states the reason and stands
Also in: —

The deviation is deliberate and reasoned in the file (L195-197); part 2
rows C6 and D-14 say "by design". What is wrong is the record, not the
file. Reversing the design is not decided here.

### architecte.md F02 — "a manifest" beside "a build file"

Verdict: confirmed
Decision: Drop "a manifest" from the never-open bullet, since L81 makes
the dependency manifest one of the build files.
Where: architecte.md L305-308 ↔ architecte.md L79-82
Cited: L305-306 — "Open a source file, a build file, a manifest or a
generated schema"
Cited: L79-81 — "The conventions file names the build files — the ones
the build tool and the analysers read to configure themselves, the
dependency manifest among them."
Owner: architecte
Also in: —

### architecte.md F03 — the commands' glob ignores an absent heading

Verdict: confirmed
Decision: Make every command's invocation-3 trigger read an absent
`## Verdict` heading as an empty one, as the agent's L696-698 does.
Where: architecte.md L696-698 ↔ 7_lots.md L143, L155-156; 8_code.md
L220-221; conventions.md L71
Cited: architecte.md L696-698 — "A request with no `## Verdict` heading
at all counts as empty — you add the heading and write under it"
Cited: 7_lots.md L155-156 — "glob `architecte/`. Any request with an
empty `## Verdict` → `architecte`, invocation 3."
Cited: 8_code.md L220-221 — "glob `architecte/`. Any request with an
empty `## Verdict` → `architecte`, invocation 3."
Cited: conventions.md L71 — "A request in `architecte/` with an empty
`## Verdict` | Invocation 3 — Requests"
Owner: 7_lots.md · 8_code.md · conventions.md (the commands hold the
glob; the agent's rule is the form and stands)
Follows: —
Also in: commandes.md, possibly — the finding names the agent, so it
is expected here

The report names 7_lots and 8_code only; conventions.md L71 carries the
same trigger and is added.

### architecte.md F04 — C19 justifications still in the file (+ B-4)

Verdict: confirmed
Decision: Drop the four justifications C19 named and the one B-4 named,
keeping each rule without its reason.
Where: passes/architecte.md L443-458 (C19) ↔ architecte.md L453-455,
L511-514, L685-687; docs/verification/agent-architecte.md L107-109
(B-4) ↔ architecte.md L131-133
Cited: passes/architecte.md L457-458 — "each rule stands without its
reason; the example is dropped or made general"
Cited: architecte.md L453-455 — "annotating every rule with its source
costs four hundred tokens read at every lot, for something no coding
agent uses"
Cited: architecte.md L511-512 — "A conjunction is invisible upstream,
and not through any carelessness."
Cited: architecte.md L685-687 — "and for good reason — here you are not
deriving a file, you are judging a claim about a platform"
Cited: agent-architecte.md L107-109 — "*a spec sheet cites `R30`, and
renumbering would point every citation at another rule…* C7's
Justification, in the rule."
Owner: architecte
Also in: —

Only the example (L516, "a record") was changed. NOTE severity holds:
the file works as it is; the cost is tokens at every opus invocation.

### architecte.md F05 — CMD2's example shows invocation 1 only

Verdict: confirmed
Decision: Show the invocation example in its four forms — 1 with the
questions file number, 2 naming the answered file (see F18), 3 with the
working folder taken from the second argument, 4 as 1.
Where: passes/architecte.md L518-534 (CMD2) ↔ conventions.md L169-177
Cited: passes/architecte.md L533-534 — "the invocation example shows
the invocation 3 form too"
Cited: conventions.md L174-175 — "prompt=\"Feature folder:
docs/features/<name>/. Invocation 1 — Deriving. Your questions file
number: NN.\""
Owner: conventions.md
Follows: architecte.md L344 ("The prompt says which one. It is never
inferred.") stands; nothing to change on the agent side
Also in: commandes.md, possibly

The argument half of CMD2 is done (conventions.md L18-20, L26-27); the
example half is not.

### architecte.md F06 — three changes missing from the index

Verdict: confirmed
Decision: Add three rows to the architecte index of
`docs/refonte/modifications.md`: the `## Invocation` field of the
blocking file, the rename of a settled blocking file moved to the
orchestration, and the report grown from three lines to five.
Where: docs/refonte/modifications.md L636-643 ↔ architecte.md L247,
L359, L377-378, L215
Cited: modifications.md L636-643 — eight rows: directives, invocation 4,
marking, `couverture.md`, gap kinds, insufficient answer,
`commands/conventions.md`, `commands/7_lots.md · 8_code.md`; none of
the three
Cited: architecte.md L247 — "`## Invocation` | The one that wrote this
file — 1, 2, 3 or 4"
Cited: architecte.md L377-378 — "You never rename it — you have no tool
that removes a file. The orchestration does it"
Owner: the applier of this plan, in `docs/refonte/modifications.md`
Also in: —

### architecte.md F07 — off-grid citations on the rule, or not

Verdict: confirmed
Decision: Align the never-do bullet and move 6 with *The coverage file*:
the rule carries `off-grid` and no entry citation; the citations go on
the `couverture.md` line.
Where: architecte.md L291-292, L442 ↔ architecte.md L195-198
Cited: L291-292 — "Write a rule the grid did not fire, unless it carries
`off-grid` and cites the entries that motivate it"
Cited: L442 — "Each cites the entries that state it, and carries
`off-grid`."
Cited: L195-198 — "The rule itself carries it too, in the conventions
file … Nothing else of its provenance goes there: no entry number, no
reason."
Owner: architecte
Also in: —

The grid's R3 (docs-new/process/GRILLE_CONVENTIONS.md L46-47, "It cites
the entries that motivate it and carries `off-grid`") reads either way;
the agent's L195-198 is what settles where the citation lives, and
move 7 (L453-455, "No provenance in it") agrees with it. The grid is
not touched — R4.

### architecte.md F08 — "you never wrote one at invocation 3"

Verdict: confirmed
Decision: Define what an Arbitre-called invocation 3 does with a root
`blocked_architecte.md` an orchestration-called run left: it neither
rewrites nor applies it, and refuses in the verdict any request the
block's cause still stops, naming the file.
Where: architecte.md L382-384 ↔ architecte.md L272-273, L350-364
Cited: L382-384 — "When the Arbitre called you, there is no blocking
file to find — it never writes one for you, and you never wrote one at
invocation 3."
Cited: L272-273 — "The orchestration called you | A blocking file, as
anywhere else — nobody is waiting on you"
Cited: L358 — "Empty | Write it again unchanged and stop" — which an
Arbitre-called run cannot do (L234-238, "you do not block")
Owner: architecte
Follows: arbitre.md L431-432 reads the refusal as it reads any other —
nothing to change
Also in: —

The case is reachable: 8_code L406-408 stops on the root file, but
move 4b (L164-170) does not check it before the next lot, so a
Détailleur or Réalisateur can call the Arbitre while it stands. See
chemins-aval.md F24 for the 8_code side.

### architecte.md F09 — invocation 3 on a `bugfix-NN/` has no `couverture.md`

Verdict: confirmed
Decision: On a `bugfix-NN/`, invocation 3 writes its `couverture.md`
line one level up, in the feature folder's file — where
`audit_conventions.md` L40-43 already looks for it — and the table row
names that file as the input.
Where: architecte.md L39-45, L330, L724-729 ↔ .claude-new/commands/
audit_conventions.md L40-43; conventions.md L76, L84-87
Cited: architecte.md L43-45 — "Invocations 1, 2 and 4 run on a feature
folder only … Invocation 3 runs on either."
Cited: architecte.md L724-726 — "A rule you add here gets its
`couverture.md` line too — the request's file name in the first column
instead of an entry"
Cited: audit_conventions.md L40-43 — "On a correction cycle it is not in
the working folder: the Architecte writes it when it derives the
conventions, and that runs on the feature folder. Look for it one
level up, at the feature folder's root, and use it from there."
Cited: conventions.md L85-86 — "`couverture.md` is written per
feature, so a second feature has none"
Owner: architecte
Follows: audit_conventions.md L91-92 reads the lot from the request's
file name ("`architecte/detailleur-lot-04.md`") — the first column of a
line written from a bugfix has to tell the cycle apart, and that command
reads it
Also in: —

Creating a second file in the bugfix was not chosen: the audit already
reads the feature's, and the conventions file the line traces is one
for the whole repository (L47-48).

### architecte.md F10 — two orders for the rule line

Verdict: confirmed
Decision: State the trigger mark's position once — as the third field
of the example at L121-122 — and drop "at the end of the line" at L140.
Where: architecte.md L119-128 ↔ architecte.md L140
Cited: L121-122 — "R12 · Every identifier that leaves a module is in
English · permanente · mechanical"
Cited: L140 — "`permanente` or `spécifique`, at the end of the line."
Owner: architecte
Follows: none — no reader keys on the field's position (grep of
`.claude-new/` for "end of the line", "fifth field", "off-grid" outside
this file: no hit); they match the word (`detailleur.md` L639-646,
`realisateur.md` L67, L95, `relecteur.md` L65, L349, `concepteur.md`
L63, `testeur.md` L67)
Also in: —

### architecte.md F11 — "Invocations 2 and 3 read the one in force"

Verdict: confirmed
Decision: Name invocation 4 in the never-open bullet's exception.
Where: architecte.md L296-297 ↔ architecte.md L98-99, L797
Cited: L296-297 — "Invocations 2 and 3 read the one in force: they
amend it"
Cited: L98-99 — "Invocations 2, 3 and 4 read the file in force — they
amend it, and you cannot amend what you have not read."
Owner: architecte
Also in: —

Closes part 2 row D-1 as well.

### architecte.md F12 — "at 4 it is integration only"

Verdict: confirmed
Decision: Drop the asymmetry: at invocation 4 the directives are
integrated at move 6b after moves 5 and 6 derive, exactly as at 1.
Where: architecte.md L600-601 ↔ architecte.md L797-799, L444-446
Cited: L600-601 — "at 1 you derive first, then integrate them; at 4 it
is integration only"
Cited: L797-799 — "Read the conventions file whole, then run moves 2 to
10 of invocation 1 — every one of them, on this feature's documents."
Owner: architecte
Also in: —

### architecte.md F13 — "a directive never becomes a question" and `replacement`

Verdict: confirmed
Decision: State the one exception where the absolute rule stands: a
directive is never a question, except the `replacement` question of
invocation 4 when a rule in force contradicts it.
Where: architecte.md L585-587 ↔ architecte.md L580, L552-555
Cited: L585-586 — "A directive never becomes a question. You block
instead"
Cited: L580 — "A rule in force contradicts it, at invocation 4 | You
raise it, `Kind: replacement`"
Owner: architecte
Also in: —

### architecte.md F14 — "looked up, never recalled — at every invocation"

Verdict: confirmed
Decision: Bound "at every invocation" to the invocations L72 grants the
web — 1, 3 and 4.
Where: architecte.md L477-478 ↔ architecte.md L72-73
Cited: L477-478 — "A fact about the platform is looked up, never
recalled — at every invocation."
Cited: L72-73 — "Invocations 1, 3 and 4 may read the web — a fact about
the platform is looked up, never recalled."
Owner: architecte
Also in: —

Granting invocation 2 the web was not chosen: L336-338 says an answer
is turned into a rule, not derived again. Should an answer need a
platform fact, that is a *precision* gap and gives a new questions file
(L620-625). See C5 · C-5 · D-2 for the table rows.

### architecte.md F15 — "four lines" and a five-line example

Verdict: confirmed
Decision: Keep one example, five lines, and say five.
Where: architecte.md L523-530 ↔ architecte.md L536-544
Cited: L524-525 — "One entry per question, four lines, numbering
restarting at Q1 in each file"
Cited: L540-544 — the second example: `### Q1` · `Block:` · `Kind:` ·
`Question:` · `Answer:`
Owner: architecte
Follows: conventions.md L35-36 greps `Answer:` and `^### Q` only —
nothing to change
Also in: —

### architecte.md F16 — five lines at most, one per coverage question

Verdict: confirmed
Decision: Make the cap a fixed part plus one line per `coverage`
question.
Where: architecte.md L215 ↔ architecte.md L222-223
Cited: L215 — "Five lines at most, and never the content of what you
wrote"
Cited: L222-223 — "Every `coverage` question, one line each — its
answer is a behaviour, and this line is the only thing that carries it
out."
Owner: architecte
Follows: conventions.md L213 relays "the agent's own report" —
nothing to change
Also in: —

### architecte.md F17 — a justification naming a check no move performs

Verdict: confirmed
Decision: Justify the invocation-3 coverage line by its real reader —
`audit_conventions.md` finding 1, which names the request from that
line — or drop the justification.
Where: architecte.md L728-729 ↔ architecte.md L460-461;
.claude-new/commands/audit_conventions.md L84-88
Cited: L728-729 — "Without it the rule has no provenance anywhere — and
the next invocation's coverage check finds a rule it cannot place."
Cited: L460-461 — "Check the coverage: every identifier of the technical
document appears exactly once in the first column."
Cited: audit_conventions.md L84-88 — "A rule the conventions carry and
`couverture.md` traces to no entry of the technical document came from
a request, not from the corpus. Name it, and name the request that
produced it."
Owner: architecte
Also in: —

### architecte.md F18 — invocation 2 has no permitted way to find its input

Verdict: confirmed
Decision: At invocation 2 the prompt names the answered
`questions-architecte-NN.md`, and the agent reads that file and no
other.
Where: conventions.md L169-177, L73 ↔ architecte.md L611-612, L101-102,
L557-559
Cited: conventions.md L174-175 — "Invocation 1 — Deriving. Your
questions file number: NN." — the only prompt form shown
Cited: conventions.md L73 — "A `questions-architecte-NN.md` at the
root, answered | Invocation 2 — Integrating"
Cited: architecte.md L611-612 — "Read the questions file you wrote —
that one among questions files, not another agent's."
Cited: architecte.md L101-102 — "Never list a folder to see what else
is there"
Owner: conventions.md (it holds the fact — it grepped the file at L35-36)
Follows: architecte.md L611-612 — the file it reads is the one the
prompt names
Also in: commandes.md, possibly; ties to F05

### architecte.md F19 — the prompt never says who called

Verdict: confirmed
Decision: The invocation-3 prompt carries who called — the Arbitre or
the orchestration — since the agent's block-or-refuse branch depends on
it and L344 forbids inferring.
Where: architecte.md L268-273, L344 ↔ arbitre.md L414-420; 8_code.md
L235-241; 7_lots.md L163-169
Cited: architecte.md L268-273 — "At invocation 3, it depends who called
you: The Arbitre called you | Never a blocking file … The orchestration
called you | A blocking file, as anywhere else"
Cited: architecte.md L344 — "The prompt says which one. It is never
inferred."
Cited: arbitre.md L418 — "prompt=\"Working folder: <the working folder>.
Invocation 3 — Requests.\""
Cited: 8_code.md L239 — "prompt=\"Working folder: <the working folder>.
Invocation 3 — Requests.\""
Cited: 7_lots.md L167 — same line
Owner: architecte (it states what the prompt names)
Follows: arbitre.md L418 · 8_code.md L239 · 7_lots.md L167 · the
invocation-3 form conventions.md gains under F05 — each adds the line
Also in: arbitre.md; commandes.md, possibly

### architecte.md F20 — the Arbitre names the wrong meaning for the block

Verdict: confirmed
Decision: The Arbitre's sentence says what the block is — a missing
input or a directive that cannot be placed — never "a rule nobody has
written".
Where: arbitre.md L264-265 ↔ architecte.md L253-259
Cited: arbitre.md L264-265 — "An Architecte block asks for a rule
nobody has written. You settle from what the corpus says; there, the
corpus says nothing."
Cited: architecte.md L253-259 — "You block in two cases, and no others:
An input you need is not there … A directive you cannot place without
changing it"
Owner: arbitre
Follows: architecte.md — nothing to change
Also in: arbitre.md

### architecte.md F21 — the grid's R4 route has no producer

Verdict: confirmed
Decision: —
Where: docs-new/process/GRILLE_CONVENTIONS.md L50-52 ↔ architecte.md
L294, L110-118, L232-277
Cited: GRILLE_CONVENTIONS.md L50-52 — "R4 — The Architecte never amends
the grid he applies. A missing form, or a form that keeps producing a
useless rule, goes back as a conventions request in `architecte/`."
Cited: architecte.md L294 — "Amend the grid you apply — the grid's `R4`"
Owner: —
Also in: —

The fact holds: no move of the agent writes a request, and the agent
is the one that answers requests. Which route replaces it is the
grid's text — the Product Owner's — see **To settle**.

---

## Part 2 — the earlier round's rows still marked `other` or `open`

### architecte.md C5 · C-5 · D-2 — the web in the invocation table

Verdict: confirmed
Decision: List the web among the inputs of rows 1 and 4 of the
invocation table, as L72-73 grants it.
Where: architecte.md L328, L331 ↔ architecte.md L72-73, L58-62
Cited: L328 — row 1 inputs: "`desc-produit.md` whole · `spec-technique.md`
whole, preamble included · `tracabilite.md`, for move 2 alone ·
`par-genre/directives.md` · the grid" — no web
Cited: L330 — row 3 inputs: "… the web · the build files · the grid"
Cited: L61-62 — "An input listed against another invocation stays
unopened, whatever your curiosity."
Owner: architecte
Also in: —

Read with L61-62, the table forbids at 1 and 4 what L72-73 grants.
The "platform practice, and that alone" bound the C5 row mentions could
not be verified against a C5 text this worktree holds in full
(passes/architecte.md L170-175 is a fragment); not decided.

### architecte.md B-2 — the same justification twice

Verdict: confirmed
Decision: Keep the wrong-recollection justification in one place.
Where: architecte.md L73-74 ↔ architecte.md L478-480
Cited: L73-74 — "A rule written from a wrong recollection is read by
every lot of every feature."
Cited: L478-480 — "A rule written from a wrong recollection at
invocation 1 is read by every lot of the feature, where one at
invocation 3 governs a single request."
Owner: architecte
Also in: — (ties to F14)

### architecte.md B-6 — "a directive she judges wrong, he changes himself"

Verdict: confirmed
Decision: One pronoun for the Product Owner throughout — she.
Where: architecte.md L569-570 ↔ architecte.md L565-566, L568
Cited: L568-570 — "It is her decision, and it does not travel the
questions route — a directive she judges wrong, he changes himself."
Owner: architecte
Also in: —

### architecte.md D-5 — "the third row is not one"

Verdict: confirmed
Decision: Say the second row is not a filter.
Where: architecte.md L708-709 ↔ architecte.md L713-717
Cited: L708-709 — "Put it through the two filters below — the third row
is not one"
Cited: L716 — second row: "Not this one | A tool checking it sets the
rule's test kind and nothing else"
Cited: L717 — third row: "It holds on one machine only | A path, an
environment variable"
Owner: architecte
Also in: —

### architecte.md D-22 — "no request with an empty `## Verdict`" at L681-682

Verdict: overstated
Why: L696-698 defines an absent heading as empty — "A request with no
`## Verdict` heading at all counts as empty — you add the heading and
write under it" — so L681-682 and L675-676 read through that definition
once the file is read whole. The residual cost is that the definition
comes fifteen lines after its first use; it is a NOTE on ordering, not
a hole, and the file's own line settles it. No decision.

### architecte.md C-6 · C-7 — implicit `Grep`, implicit `WebFetch`

Verdict: overstated
Why: the first round's own words — docs/verification/agent-architecte.md
L180-181, "Not a defect; a tool left implicit", and L183-184,
"Implicit, acceptable" — and the second round's part 1 finds the
frontmatter sound ("every tool used, every gesture tooled"). No
decision.

### architecte.md C19 · CMD2 · B-4 (open)

Covered by F04 (C19, B-4) and F05 (CMD2).

---

## Part 3 — the thematic reports

### fichiers.md F03 — a `NEW` block leaves `couverture.md` behind

Verdict: confirmed
Decision: Delete `couverture.md` with the three files `/2_structure`
already removes on a `NEW` block, so `/conventions` walks the rebuilt
document at invocation 4.
Where: .claude-new/commands/2_structure.md L164-175 ↔ conventions.md
L76-77, L89-91
Cited: 2_structure.md L167-169 — "rm -rf docs/features/<name>/par-genre/
docs/features/<name>/desc-par-nature.md
docs/features/<name>/spec-technique.md" — no `couverture.md`
Cited: 2_structure.md L173 — "all three are derived from the product
file"
Cited: conventions.md L77 — "It exists, and a `couverture.md` is there
| Nothing to do — say `/7_lots`"
Cited: conventions.md L89-91 — "`couverture.md` tells something else:
whether this feature has already been walked."
Owner: 2_structure.md
Follows: conventions.md — row 76 then routes to invocation 4 as
written; nothing to change. architecte.md — nothing to change
Also in: commandes.md, possibly

Cost accepted: invocation-3 request lines written into that
`couverture.md` before the `NEW` block are lost; at `/2_structure`
time no lot of the feature has been coded, so there are none.

### fichiers.md F04 — `/7_lots` files `questions-architecte-*.md`

Verdict: confirmed
Decision: Exempt `questions-architecte-*.md` from the filing in
`/7_lots`, as `/3a_genre`, `/4_grille` and `/6_convertit` do.
Where: 7_lots.md L47-51 ↔ conventions.md L57-58, L72; 6_convertit.md
L67-69
Cited: 7_lots.md L47-48 — "File away every root `questions-*.md`
first — the upstream loop is over and nothing downstream reads them"
Cited: conventions.md L57-58 — "Stop if a root
`questions-architecte-*.md` carries an empty `Answer:` — relay it."
Cited: 6_convertit.md L67-69 — "Never `questions-architecte-*.md` —
leave it at the root: it waits for `/conventions`, which is the only
command that reads it."
Owner: 7_lots.md
Follows: architecte.md — nothing to change
Also in: commandes.md, possibly

Stopping `/7_lots` on an unanswered file instead was not chosen: it
would hold the split on a question the conventions can carry later,
and the three sibling commands already settled the pattern.

### chemins-amont.md F19 — "back into the loop" sends the file through `/1_lexique`

Verdict: confirmed
Decision (guard only): `/1_lexique` and `/2_structure` never take a
`questions-architecte-*.md` as the answered file — it waits at the root
for `/conventions`, which 6_convertit.md L68-69 names as the only
command that reads it.
Where: conventions.md L225 ↔ 1_lexique.md L59-60, L64-65;
2_structure.md L149, L200-201; conventions.md L73; architecte.md
L646-649
Cited: conventions.md L225 — "It raised a product question | The
framing grid did not close the product — the Product Owner decides:
back into the loop, or corrected by hand"
Cited: 1_lexique.md L60 — "Another agent's questions file alone | 3 —
Watching"
Cited: 2_structure.md L200-201 — "At invocation 2, file the questions
file it integrated, into `questions/<agent>/`"
Cited: conventions.md L73 — the row that reads it: "A
`questions-architecte-NN.md` at the root, answered | Invocation 2"
Cited: architecte.md L646-649 — "The Product Owner answers it here all
the same — the command will not run you while an `Answer:` is empty.
What she writes is either the behaviour, or *voir produit* once she has
put it in the product file herself."
Owner: 1_lexique.md · 2_structure.md
Follows: conventions.md L225 — see **To settle**; architecte.md —
nothing to change
Also in: commandes.md, possibly

What "back into the loop" should mean is the Product Owner's — the
agent file (L646-649) describes only the by-hand route, and neither
route puts the behaviour into `spec-technique.md`. See **To settle**.

### chemins-aval.md F18 — an open root `blocked_architecte.md` is not listed

Verdict: confirmed
Decision: Glob the still-open blocking files in the same three places
as the numbered ones.
Where: audit_blocages.md L34-36 ↔ audit_blocages.md L26-29
Cited: L34 — "And `code/**/blocked_*.md` without a number — one still
standing."
Cited: L27-29 — "Three places: `code/**/`, the folder's own root
(`blocked_architecte`, `blocked_diagnostiqueur`), and
`investigation/`"
Owner: audit_blocages.md
Follows: architecte.md — nothing to change
Also in: commandes.md, possibly; diagnostiqueur.md

### chemins-aval.md F24 — nothing in `/8_code` closes `blocked_architecte.md`

Verdict: confirmed
Decision: Give `blocked_architecte.md` at the working folder's root the
treatment 8_code gives the other blocking files — checked before
invoking anything, renamed once the Architecte reports having applied
its decision, as conventions.md L147-154 does.
Where: 8_code.md L406-408 ↔ 8_code.md L164-175, L235-241;
conventions.md L147-154; architecte.md L352-353, L359, L377-378
Cited: 8_code.md L406-408 — "`blocked_architecte.md` at the working
folder's root — it blocks on a missing input, and the next lot's
Détailleur would run against conventions that were not amended"
Cited: 8_code.md L170 — "At the path it sits at — `code/<lot>/` for the
four agents of the loop, `code/` for the detailleur."
Cited: conventions.md L150 — "git mv <folder>/blocked_architecte.md
<folder>/blocked_architecte-NN.md"
Cited: architecte.md L359 — "Filled | Apply it, and say in your report
that you did — the orchestration renames the file, carry on"
Cited: architecte.md L352-353 — "Look for `blocked_architecte.md` in
the working folder before anything else." — the prompt need not name
it
Owner: 8_code.md
Follows: architecte.md — nothing to change; 7_lots.md L171-175 sends
the case to `/conventions` and needs no rename
Also in: commandes.md, possibly

The pre-check half is what makes F08's case unreachable from `/8_code`.

### passages-aval.md F10 — the sheet cites `§3 ·`, the rules are `R30`

Verdict: confirmed
Decision: The sheet's `## Conventions` names rules by their `R<n>`
number, as the Architecte numbers them and as the Relecteur and the
Réalisateur already report them.
Where: detailleur.md L250-253, L652 ↔ architecte.md L130-133;
relecteur.md L141, L349-351; realisateur.md L97, L159
Cited: detailleur.md L252-253 — "§3 · a rule needing the platform's
ambient handle is in the wrong module / §9 · the name of the rule, not
of the structure"
Cited: detailleur.md L652 — "Name the rule, never restate it — `§10 ·
no hardcoded string`."
Cited: architecte.md L131-133 — "a spec sheet cites `R30`, and
renumbering would point every citation at another rule with nothing
able to detect it"
Cited: relecteur.md L141 — "point 3 — R12, the identifier is not in
English"
Cited: realisateur.md L159 — "R18 — the identifier is in English"
Owner: detailleur
Follows: architecte.md — nothing to change (L116-117, "the coding
agents cite them" by number, is the form); relecteur, realisateur,
concepteur, testeur read "the rules the sheet names" and carry no `§`
example — nothing to change
Also in: detailleur.md; relecteur.md

### passages-aval.md F14 — "a product decision" in two rows (settled)

Verdict: settled — decisions.md, `passages-aval.md F14`
Decision: The *Not a convention* row no longer ends on "a product
decision"; the *doubt, or a product decision* row alone carries it.
Where: architecte.md L736-737 ↔ arbitre.md L431-432;
audit_conventions.md L124-126
Cited: architecte.md L736 — "Not a convention | Say where it belongs:
the code, the tooling, the machine, a product decision"
Cited: arbitre.md L431 — "Refused, and it says what would settle it |
Settle from that — the tooling, the code, an existing rule"
Cited: audit_conventions.md L124-126 — "A verdict that turns a request
down names where the thing goes — the code, the tooling, the machine, a
product decision."
Owner: architecte
Follows: audit_conventions.md L126 — its list of destinations drops "a
product decision" to match; arbitre.md L431-432 — already reads the two
rows apart, nothing to change
Also in: arbitre.md; commandes.md, possibly

### renommages.md F16 — the Concepteur writes an `architecte/` request (settled)

Verdict: settled — decisions.md, `renommages.md F16`
Decision: The Concepteur writes an `architecte/` request for a
placement the conventions do not settle, and meanwhile places the
symbol in the module of the one it depends on most.
Where: concepteur.md L189-196 ↔ 8_code.md L112; architecte.md
L657-666
Cited: concepteur.md L193-195 — "You write no conventions request — you
have no route to the Architecte. That line of your report is the route"
Cited: 8_code.md L112 — "Relay its `## Placements not settled by the
conventions` line when it carries one"
Cited: architecte.md L663-665 — "The orchestration, at the end of a
lot, on every request waiting in `architecte/`."
Owner: concepteur
Follows: 8_code.md L112 — the relay line changes to what the decision
says; architecte.md — nothing to change: it names no requester, and an
end-of-lot request from the Concepteur is picked up at 8_code move 7
like any other
Also in: concepteur.md; commandes.md, possibly

---

## To settle

### architecte.md F21 — who carries a missing form back to the grid

The grid's R4 (docs-new/process/GRILLE_CONVENTIONS.md L50-52) routes a
missing form "as a conventions request in `architecte/`". The Architecte
is the agent that answers requests, and no move of it writes one. The
grid is the Product Owner's text; the agent cannot amend it (L294).

| Option | What it costs |
|---|---|
| The Architecte writes `architecte/grille-<n>.md` | A request whose reader is the agent itself; the next invocation 3 would open it and have to refuse it (not a convention). The Product Owner reads it only if a command relays it — none does |
| The Architecte says it in its report | Cheapest; a report is read once and lost (the file's own argument at L594-595 against a report line for a directive) |
| The Architecte raises it in its questions file, a fifth `Kind:` | Reaches the Product Owner through `/conventions` L224; changes the four-word list at L546-547 and every reader of `Kind:` |
| Amend the grid's R4 to one of the above | The grid is the Product Owner's |

Decision: —

### chemins-amont.md F19 — what "back into the loop" means for a `coverage` answer

conventions.md L225 offers "back into the loop, or corrected by hand".
architecte.md L646-649 describes the by-hand route only (the behaviour
into the product file, `voir produit` in the answer). Neither route
carries the behaviour into `spec-technique.md`, which the split is cut
from.

| Option | What it costs |
|---|---|
| Keep "corrected by hand" alone, as L646-649 | The product file gains a block the technical document never sees; the conventions get no rule and no lot builds it — the gap the question found stays open in the code |
| Re-run the upstream loop from the block the Product Owner adds (`/3_decoupe` onward, through `/6_convertit`) | A full upstream turn per coverage question; `spec-technique.md` rebuilt, `couverture.md` then stale (see fichiers.md F03) |
| Let the Rédacteur integrate the answered `questions-architecte` file | The file also holds `conjunction`, `inconsistency` and `precision` answers, which are not product; and once filed under `questions/architecte/` the Architecte never reads them |

Decision: —

The guard (1_lexique and 2_structure never take the file as the
answered one) is decided above and does not depend on this.

---

## Not carried

- architecte.md F03's wording note that "conventions.md L71" was not in
  the report: added to the entry, same finding.
- passages-amont.md L19 names "architecte invocation 1" under *Sound*
  — not a finding.
- fichiers.md L24 names the agent under *Sound* — not a finding.
- No `/cycle` or `cycle.md` mention in architecte.md, conventions.md,
  7_lots.md or 8_code.md (decisions.md, `cadreur.md F23`): nothing to
  remove.
