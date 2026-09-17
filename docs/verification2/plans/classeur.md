# classeur — plan de correction (verification 2)

**Inputs read**: `.claude-new/agents/classeur.md`; the four commands the
grep hit — `3b_nature.md`, `2_structure.md`, `3a_genre.md`,
`5_reclasse.md`; `docs/verification2/classeur.md` (both parts);
`docs/verification2/decisions.md`; the six thematic reports filtered on
`classeur` (four hits: `renommages.md` F10, F11; `chemins-amont.md` F03;
`passages-amont.md` F01 — nothing in `fichiers.md`, `chemins-aval.md`,
`passages-aval.md`). Where a finding names a second file, that file was
opened at the cited lines: `agents/redacteur.md`,
`docs/refonte/modifications.md`, `docs/refonte/passes/classeur.md`.

**Line numbers** are those of the files as they stand today in
`.claude-new/`.

**Owner / Follows**: `Owner` decides the form; `Follows` rewrites its
own lines to match. Where the form is a command's (dispatch, filing,
rename), the command is the owner and the agent follows.

**Every finding below is `confirmed`.** No finding was found stale,
wrong or overstated: each was re-read in the current files and holds
at the severity the report gives it.

---

## Part 1 — the seventeen findings of the report

### classeur.md F01 — the index omits the emptying case

Verdict: confirmed
Cited: modifications.md L57 — "`agents/classeur.md` | 📌 **Sait que
tout bloc qu'on lui nomme porte `Genre: comportement`**"; classeur.md
L267 — "🔴 **Its `Genre:` is no longer `comportement`** | 📌 **Empty its
line**".
Decision: Once F05 is applied, add to the index entry (and the pass
sheet) the second case the file carries — a named block that left
`comportement`, whose `Nature:` line the agent empties.
Where: docs/refonte/modifications.md L57 ↔ agents/classeur.md L267,
L295-300
Owner: classeur
Also in: —

### classeur.md F02 — a « tap → state change + visible feedback » block

Verdict: confirmed — 🔴 **settled by `decisions.md` `classeur.md` F02**.
Cited: passes/classeur.md L76-78 — "a user action is a trigger; the
block takes the nature of what the action produces, and only the part
the user sees is `presentation`"; classeur.md L93 — "A block that
describes only what the user perceives is `presentation` — 🔴 **one that
describes both is badly split**, and that is doubt 1".
Decision: Apply the settled decision — rewrite the `presentation ·
anything else` frontier (L93) so the block takes the nature of what the
action produces, is `presentation` only when it describes the perceived
part alone, and is never sent to doubt 1 for describing both; and bound
doubt 1 (L103-106, L115) so the visible response that accompanies what
an action produces is not a second output.
Where: agents/classeur.md L93, L103-106, L115 ↔
docs/refonte/passes/classeur.md L74-79
Owner: classeur
Also in: —

### classeur.md F03 — C5 met by another mechanism than the one listed

Verdict: confirmed
Cited: passes/classeur.md L139-140 — "the number is the highest
`questions-classeur-NN` wherever it is found, plus one; none anywhere
means `01`"; 3b_nature.md L44-47 — "Give the agent its questions file
number in the prompt … It never lists a folder to find it — it has no
`Glob`"; classeur.md L125 — "The prompt names your number — the command
has the fact"; frontmatter L4 carries no `Glob`.
Decision: Record in the pass sheet and the index that C5 was met by
moving the numbering rule into `/3b_nature` and removing `Glob` from
the agent, which receives `NN` in the prompt.
Where: docs/refonte/passes/classeur.md L139-141 ↔ commands/3b_nature.md
L44-47, agents/classeur.md L125
Owner: classeur
Also in: —

### classeur.md F04 — the targeted edit has no unique anchor

Verdict: confirmed — L179 reads "one targeted edit per `Nature:` line"
and names no anchor; an empty `Nature:` line is repeated on every
unclassed block, and L47-55 give the delimitation for reading only.
Decision: State that the edit spans from the block's heading through
its `Nature:` line — the only unique span — for filling, rewriting
(`MODIFIED`) and emptying alike.
Where: agents/classeur.md L179 ↔ L47-55, L59-60, L298
Owner: classeur
Also in: —

### classeur.md F05 — "every named block is `comportement`" vs. the emptying case

Verdict: confirmed
Cited: 3b_nature.md L97 — the command does name those blocks: "Plus
`grep -B1 '^Nature: '` kept to the blocks whose `Genre:` is **not**
`comportement` | 📌 **Name those too**"; classeur.md L34-37 — "Every
block the prompt names carries `Genre: comportement` … A block of any
other genre is not yours, and the command does not name it".
Decision: Rewrite L34-37 so the prompt's list is the behaviours plus the
blocks that left `comportement` while still carrying a nature — the ones
whose line is emptied — and keep L267 and L295-300 as the procedure.
Where: agents/classeur.md L34-37 ↔ L267, L295-300; commands/3b_nature.md
L97
Owner: classeur
Follows: — (`/3b_nature` L97 already names them)
Also in: —

### classeur.md F06 — a third cause of blocking, outside the enumeration

Verdict: confirmed — L169 "Twice on one block, and you block instead";
L224-225 "You block when no nature fits at all — which means the block
produces nothing", then "Or that the eight miss something" (L225-227).
Decision: Add the third cause — one block, two answers leaving the same
doubt open — to *When you cannot produce* beside the two it lists, with
what its `## To resume` asks for (the nature, or the rewrite).
Where: agents/classeur.md L169-172 ↔ L223-227
Owner: classeur
Also in: —

### classeur.md F07 — "both answers" when the agent holds one file

Verdict: confirmed — L146 "The prompt names the questions file you wrote
last turn"; L171-172 "Say both answers in the blocking file"; the first
answer sits in a file filed a turn earlier that the prompt never names
(3b_nature.md L144-145 names one path).
Decision: Make the follow-up question (L166-167) quote the answer it
follows, so that the one file the prompt names carries both answers, and
bound L171 to what that file holds. Rejected: naming two files in the
prompt — `/3b_nature` names one, and the agent's rule that it opens what
it is named would have to bend.
Where: agents/classeur.md L146, L166-167 ↔ L171-172
Owner: classeur
Also in: —

### classeur.md F08 — an empty `## Decision` beside a filled one

Verdict: confirmed — L233-235 "Several blocked blocks go in one blocking
file … One `## Decision` per block"; L253-254 "the orchestrator checked,
and would not have called you on an empty decision" — singular.
Decision: Keep the guarantee at L253-254 and state it for every entry —
the agent is never named a file in which any `## Decision` is empty —
the command enforcing it (F13).
Where: agents/classeur.md L233-235 ↔ L253-254; commands/3b_nature.md
L38-39
Owner: 3b_nature (the dispatch rule)
Follows: classeur L253-254
Also in: —

### classeur.md F09 — three ordered report lines the report section drops

Verdict: confirmed — L237 (name the blocked blocks), L246 (waits on the
Rédacteur), L247 (a value outside the eight) versus *Then report*
L319-331, which lists counts, per-block natures and asked identifiers.
Decision: Fold the three lines into *Then report*, as items of the
report beside the counts.
Where: agents/classeur.md L237, L246-247 ↔ L319-331
Owner: classeur
Also in: — (the command side is F15)

### classeur.md F10 — the description names the wrong predecessor

Verdict: confirmed — L3 "MUST BE USED after the decoupeur"; L35 "the
qualifieur ran before you".
Decision: Make the description name the qualifieur as the agent that
runs before.
Where: agents/classeur.md L3 ↔ L35
Owner: classeur
Also in: —

### classeur.md F11 — who splits a block the agent asked about

Verdict: confirmed — L115 "Whether the Rédacteur splits it"; L181
"Split a block, or merge two — that is the decoupeur's".
Decision: Align L181 with L115 — a split that follows one of the
agent's answers is the Rédacteur's, integrating that answer; the
decoupeur's split is by trigger and never from a question.
Where: agents/classeur.md L115 ↔ L181
Owner: classeur
Also in: —

### classeur.md F12 — the answered file's path, and two rules of the command against it

Verdict: confirmed
Cited: 3b_nature.md L49-53 — "The highest `questions-classeur-NN.md`,
at the root or under `questions/classeur/` — ⚠️ **the root first**";
L67-69 — "Grep `^### Q` in each before touching it — a file holding
questions is not yours to file … Stop and say which"; L71-72 — "Filed,
it is read by no command again"; 2_structure.md L89-92 — "unlike
`questions/qualifieur/` and `questions/classeur/`, which `/3a_genre`
and `/3b_nature` reopen to give their agent its own last file";
2_structure.md L200-201 — "At invocation 2, file the questions file it
integrated, into `questions/<agent>/`".
Decision: Make the answered file `/3b_nature` names always the highest
under `questions/classeur/` — where `/2_structure` files it at
integration — dropping the root-first clause (L49-53) and the post-run
filing (L58-60), exempting `questions/qualifieur/` and
`questions/classeur/` from "read by no command again" (L71-72), and
keeping L67-69 as the stop on a root file whose answers were never
integrated.
Where: agents/classeur.md L146 ↔ commands/3b_nature.md L49-53, L58-60,
L67-69, L71-72; commands/2_structure.md L89-92, L200-201
Owner: 3b_nature
Follows: classeur L146 — holds as written: "last turn's" is the highest
filed, since the agent writes a file on every run
Also in: — (the twin at `3a_genre.md` L50-61, L72-73 belongs to the
qualifieur's plan)

### classeur.md F13 — one `## Decision` per entry, one heading read

Verdict: confirmed
Cited: 3b_nature.md L38 — "Its `## Decision` is empty | 🔴 **Stop**";
2_structure.md L121 — "One of the three with an **empty** `## Decision`
| 🔴 **Stop**"; classeur.md L233-235 — "the four headings repeated for
each … One `## Decision` per block".
Decision: Test every `## Decision` heading of the file — any empty, the
command stops; all filled, it names the file — in `/3b_nature` and in
`/2_structure`.
Where: agents/classeur.md L233-235 ↔ commands/3b_nature.md L38-39,
commands/2_structure.md L120-121
Owner: 3b_nature, 2_structure
Follows: classeur L253-254 (F08)
Also in: — (same finding as `renommages.md` F11, below)

### classeur.md F14 — the emptying rule's stated reason is false

Verdict: confirmed
Cited: 5_reclasse.md L64-67 — "every block carrying `Genre:
comportement` has a filled `Nature:` … One hit and you stop"; L69-70 —
"A block of any other genre carries an empty `Nature:`, and that is
right"; L172-173 — "A `Nature:` value that is not one of the eight —
say which block, and stop"; L135-137 — the sort reads
`par-genre/comportements.md`, "never from the product file". Nothing
stops on a filled nature under another genre. classeur.md L299-300 —
"a later command stops on a filled line under any other genre";
3b_nature.md L97 — "`/5_reclasse` stops on a filled one".
Decision: Keep the emptying rule; drop the claim that `/5_reclasse`
stops on it, at L298-300 and at 3b_nature.md L97, and ground the rule
on what is true — the genre views copy the block as it stands
(5_reclasse.md L117), so a stale nature travels with it.
Where: agents/classeur.md L298-300 ↔ commands/5_reclasse.md L64-70,
L172-173; commands/3b_nature.md L97
Owner: classeur
Follows: 3b_nature L97
Also in: —

### classeur.md F15 — the relay list drops what the routing table keys on

Verdict: confirmed
Cited: 3b_nature.md L223-226 — "How many blocks were classed, which
changed nature, and how many questions — and the per-block list …
Nothing else is yours"; L234-237 — the routing table reads "A
`## Decision` names a rewrite" and "names a nature outside the list".
Decision: Add to the relay list the blocked blocks' names and the two
decision-shape lines the agent reports — the routing table keys on them,
and the rename rule (F16) will too.
Where: agents/classeur.md L237, L246-247 ↔ commands/3b_nature.md
L223-227, L234-237
Owner: 3b_nature
Follows: classeur (F09)
Also in: —

### classeur.md F16 — renamed before `/2_structure` can read it

Verdict: confirmed
Cited: 3b_nature.md L161-164 — "A blocking file you named is filed:
`git mv … blocked_classeur.md … blocked_classeur-NN.md`";
2_structure.md L120 — the row fires on "`blocked_classeur.md` with a
filled `## Decision`", the unnumbered name; classeur.md L246 — "say in
your report that the block waits on the Rédacteur".
Decision: Make `/3b_nature` rename the file only when the agent reports
no block waiting on the Rédacteur; otherwise it leaves the file at its
unnumbered name for `/2_structure` — see `renommages.md` F10 for the
whole lifecycle.
Where: agents/classeur.md L246 ↔ commands/3b_nature.md L161-164,
commands/2_structure.md L120
Owner: 3b_nature
Follows: classeur — L246 stands as written
Also in: redacteur.md, qualifieur.md (through `renommages.md` F10)

### classeur.md F17 — the block form omits the `Global:` line

Verdict: confirmed
Cited: redacteur.md L59-62 — the block form is "`### B7 — Rejecting
invalid durations    MODIFIED` / `Genre:` / `Nature:` / `Global: ##
Activity screen`"; classeur.md L50-51 — "`Genre:` on the next line,
`Nature:` on the one after, then the block's sentences".
Decision: Add the optional `Global:` line, after `Nature:`, to the block
form the agent is given.
Where: agents/classeur.md L49-51 ↔ agents/redacteur.md L59-62
Owner: classeur
Also in: —

---

## Part 2 — the thematic findings naming the classeur

### renommages.md F10 — one blocking file, two consuming commands

Verdict: confirmed
Cited: 2_structure.md L120 — "A `blocked_decoupeur.md`,
`blocked_qualifieur.md` or `blocked_classeur.md` with a filled
`## Decision` | **2 — Integrating** | That file"; 2_structure.md
L191-192 — "A `blocked_decoupeur.md` it applied is renamed" — the
other two are not; 3b_nature.md L39 — "Its `## Decision` is filled |
Name it in the prompt"; L161-164 — renamed after the run; classeur.md
L246 — "Leave the line empty — say in your report that the block waits
on the Rédacteur".
Decision: Give the file one consumer at a time, in the order the relay
already states — `/3b_nature` first, where the Classeur applies the
nature decisions and leaves the rewrite blocks empty and reported, and
the command renames the file only when no block waits on the Rédacteur;
then `/2_structure`, which hands it to the Rédacteur for the rewrite
decisions and renames it after — each reader applying only the
decisions of its shape.
Cost accepted: in the reversed order (`/2_structure` before
`/3b_nature`) on a file mixing both shapes, the nature decisions are
renamed away and asked again — one round trip, in a case the relay
table never orders.
Where: commands/2_structure.md L120, L191-194 ↔ commands/3b_nature.md
L39, L161-164; agents/classeur.md L246; agents/redacteur.md L531-539
Owner: 3b_nature, 2_structure (the lifecycle)
Follows: classeur — L246 stands; redacteur L531-539 — every
`## Decision`, rewrite decisions only (see `passages-amont.md` F01)
Also in: redacteur.md, decoupeur.md, qualifieur.md

### renommages.md F11 — the multi-entry file and "that one heading"

Verdict: confirmed — the same fact as `classeur.md` F13: classeur.md
L234 "the four headings repeated for each"; 3b_nature.md L37-39 read a
single `## Decision`.
Decision: As F13 — the command tests every `## Decision`; any empty, it
stops.
Where: agents/classeur.md L233-235 ↔ commands/3b_nature.md L37-39
Owner: 3b_nature
Follows: classeur L253-254
Also in: —

### chemins-amont.md F03 — `/2_structure` renames only the Découpeur's file

Verdict: confirmed
Cited: 2_structure.md L191-194 — "A `blocked_decoupeur.md` it applied is
renamed — `blocked_decoupeur-NN.md` … Left at the unnumbered name it
reads as a block still standing"; nothing renames `blocked_classeur.md`
or `blocked_qualifieur.md`, and L120 fires on the unnumbered name.
Decision: Make `/2_structure` rename `blocked_classeur.md` and
`blocked_qualifieur.md` after the Rédacteur applies them, as it does the
Découpeur's — the last reader renames (see `renommages.md` F10).
Where: commands/2_structure.md L120 ↔ L191-194
Owner: 2_structure
Follows: —
Also in: redacteur.md, qualifieur.md

### passages-amont.md F01 — the Rédacteur reads one `## Decision`

Verdict: confirmed
Cited: redacteur.md L531-533 — "The file the prompt names may be a
blocking file instead of a questions file — its `## Decision` carries
what to do"; L537 — "You rewrite what the decision names, and nothing
else"; classeur.md L196-197 — "a `## Blocking N` title per blocked
block, then four headings"; L233-235 — "One `## Decision` per block".
Decision: Make the Rédacteur read every `## Decision` of the file, one
per `## Blocking N`, rewrite what each rewrite decision names, and leave
untouched a block whose decision names a nature — that one is the
Classeur's.
Where: agents/classeur.md L196-235 ↔ agents/redacteur.md L531-539
Owner: redacteur
Follows: classeur — its file shape stands
Also in: redacteur.md, decoupeur.md, qualifieur.md

---

## Part 3 — the report's second table

The report's status table lists six first-round items still `open`
(B-1, B-3, B-4, B-6, B-8, B-14). Their first-round text is not among
this plan's inputs, so they get no verdict here. Where the line the
table cites falls under an entry above, that entry covers it: B-1
(L253) under F08/F13; B-4 (L93) under F02; B-14 (L237) under F09/F15;
B-8 (L50) under F17. B-3 (L80) and B-6 (L41) are not restated by any
finding of this round and stay as the report marks them.

---

## To settle

**The `/2_structure` table when a filled `blocked_classeur.md` and an
answered questions file sit at the root together.** Met while building
`renommages.md` F10; not in `decisions.md`. The relay of `/3b_nature`
(L235) sends the Product Owner to fill the decision, answer the
questions, then `/1_lexique` and `/2_structure` — at which point the
table at 2_structure.md L117-125 has row L120 (the blocking file) above
row L124 (the questions file): the Rédacteur is handed the blocking
file, the answered questions file stays at the root beside the
Rédacteur's own new one, and the next command stops on "more than one"
(L125). Pre-existing, and not the classeur's to settle.

| Option | Cost |
|---|---|
| The Rédacteur takes both in one invocation — the blocking file and the questions file | One more input to its invocation 2; its rule "never a second questions file" (L527-528) has to admit a blocking file beside the questions file |
| Two runs of `/2_structure`, the blocking file first, and the relay says so | A run whose only output is a rewrite; the questions file waits one command longer; row L125 has to tolerate the Rédacteur's fresh file beside the waiting one |
| The relay orders the questions before the decision, so the two never meet at the root | The blocked block is asked about a turn later; no command change, but the `/3b_nature` relay row L235 reverses its order |

Decision: —
