# Plan — `decoupeur.md`

Built against `.claude-new/agents/decoupeur.md` (253 lines) and the four
commands that name it: `3_decoupe.md` (read whole), `2_structure.md`
L110-130 and L185-200, `3a_genre.md` L95-125, `3b_nature.md` L95-120.

Where a finding rests on the refonte index, the index was opened
(`docs/refonte/modifications.md` L297-300, L308-321) and so was the
first-round report (`docs/verification/agent-decoupeur.md`), since the
second-round report's part 2 keys every fixed line on its identifiers.

One fact frames seven of the eighteen findings: the refonte index
(`modifications.md`) is a record closed before round 1; every gap between
it and the file dates from the round-1 corrections, and Wave 3 writes
into `.claude-new/` only (`correction.md` L290). No entry below asks an
agent to edit the index.

---

## decoupeur.md F01 — C4 listed ÉCARTÉ, the stop is gone

Verdict: confirmed
Decision: — (see `## To settle`)
Where: modifications.md L318 ↔ decoupeur.md (no occurrence of `Clarification needed`)
Owner: —
Also in: —

Cited: modifications.md L318 — "**C4** | Retirer de l'agent l'arrêt sur
`Clarification needed` | 🔴 **Ce n'est pas un filet, c'est un périmètre
différent** — la commande grepe **tout le fichier**, l'agent regarde
**ses blocs**. 📌 **Et si la commande change, l'agent tient encore**"

`grep 'Clarification needed' .claude-new/agents/decoupeur.md` returns
nothing; the only stops are the four commands' greps (`3_decoupe.md`
L44-47, `3a_genre.md` L63, `3b_nature.md` L62, `4_grille.md` L76). The
removal came out of round 1 D-4 (`docs/verification/agent-decoupeur.md`
L144-150: the stop's only outcome was a reply, which the file says gets
lost), and the second-round report records it as moot (L44). The index
records the opposite choice, with a robustness reason the Product Owner
endorsed. Restoring the stop or recording its removal is a choice on
scope — settled below, not here.

---

## decoupeur.md F02 — C9 listed ÉCARTÉ, its ask is in the file

Verdict: confirmed
Decision: Keep the rule at L124-126 as it stands; nothing to apply in `.claude-new/` — the index line is stale and lies outside the campaign's write perimeter; relay it to the Product Owner with F03 and F04.
Where: modifications.md L319 ↔ decoupeur.md L124-126
Owner: — (relay)
Also in: —

Cited: modifications.md L319 — "**C9** | Ce que deviennent les autres
blocs quand un bloque | 📌 **Vrai, mais marginal** — ⚠️ **avec une seule
cause de blocage désormais, le cas est rare**"

decoupeur.md L124-126: "What you have already split is written first —
never held back. The blocking file names the block you stopped on, and
a rerun starts from there." Round 1 asked for exactly this
(`docs/verification/agent-decoupeur.md` L51: "nothing says whether the
split blocks were written back before the stop"), and the report's part
2 lists D-7 fixed at L120-121. C9 was set aside as marginal, not as
wrong; the file holding the rule contradicts no intent. The index is
the only side out of date.

---

## decoupeur.md F03 — C1 listed REPORTÉ, the command was reordered

Verdict: confirmed
Decision: Nothing to apply in `.claude-new/` — the reordering is chain-wide, so the "two forms" the index feared do not exist; the index line is stale, relay it.
Where: modifications.md L321 ↔ 3_decoupe.md L99-125
Owner: — (relay)
Also in: —

Cited: modifications.md L321 — "**C1** | L'ordre des sections de la
commande | ⚠️ **Reporté au `todo.md`** — 🔴 **les neuf commandes du cycle
partagent cette structure**, en corriger une seule créerait deux formes"

`3_decoupe.md` L99 "## Git, before invoking" now precedes L127 "## The
invocation", and L173 "## Git, once it has reported" follows — the order
C1 asked for (`docs/refonte/passes/decoupeur.md` C1, "the run reads in
execution order"). `grep -l '## Git, before invoking'
.claude-new/commands/*.md` returns fifteen files — every command that
invokes an agent. One form, not two.

---

## decoupeur.md F04 — C14 listed PASSÉ, applied in another form

Verdict: confirmed
Decision: Keep the re-invocation form — no ceiling, no range; nothing to apply in `.claude-new/`; the index line needs a caveat, relay it.
Where: passes/decoupeur.md L335-360 ↔ 3_decoupe.md L69-70, L202-205
Owner: — (relay)
Also in: —

Cited: passes/decoupeur.md L350-357 — "the command bounds what one
invocation is given (a range of blocks, sequential invocations on the
same file, each taking the highest number afresh …), and the agent's
report names the blocks it looked at, so the orchestrator compares that
list with what it named without opening a block. I was unsure of the
ceiling; the file has to hold one"

`3_decoupe.md` L69-70: "every block. Name none in the prompt." L202-205:
"A short list: invoke the decoupeur again on the blocks it did not
reach, and nothing else. Twice at most — still short at the second, stop
and say which blocks were never looked at". What C14 wanted — a sweep
that cannot fall short in silence — holds: the agent's list (decoupeur.md
L239-244) is the signal, the re-invocation the bound, and the second
short list stops the command. The ceiling C14 was itself unsure of is
not needed for that. The report's part 2 already records C14 as "other"
(L31).

---

## decoupeur.md F05 — `Glob` removed, unrecorded

Verdict: wrong
Where: decoupeur.md L4 ↔ modifications.md L294-338

The removal is recorded, in the round that asked for it:
`docs/verification/agent-decoupeur.md` L114 — "**C-2 · `Glob` — no
gesture uses it** — NOTE. … Nothing in the file globs. Either the tool
is surplus, or … probably surplus" — and the second-round report's own
part 2, L40: "C-2 | fixed | `.claude-new/agents/decoupeur.md:4`". The
refonte index closed before round 1 and could not carry a round-1
correction. `tools: Read, Grep, Edit, Write` at L4 matches every gesture
in the file (the report's section 3 says the same, L24).

---

## decoupeur.md F06 — the edit-in-place rule, unasked

Verdict: wrong
Where: decoupeur.md L186-190 ↔ modifications.md L294-338

A comment asks for it, verbatim: `docs/verification/agent-decoupeur.md`
L112 — "**C-1 · Edit vs Write on the product file** — NOTE. … a `Write`
of the product file would then truncate it to what it loaded. `Edit` is
the only tool that fits, and the file does not say so. … a line saying
'by Edit, never by rewriting the file' would close it." The
second-round report records it: L39 "C-1 | fixed |
`.claude-new/agents/decoupeur.md:186–190`".

---

## decoupeur.md F07 — "a constraint the Product Owner imposed", unasked

Verdict: wrong
Where: decoupeur.md L61-67 ↔ modifications.md L54

Two facts in the finding are false. "The index's only line for this
file" — modifications.md L297-300 is a second one: "sa règle disait déjà
qu'un catalogue est un bloc à part, mais **ses gestes n'avaient aucun
réceptacle** pour les phrases que rien ne déclenche. 🔴 **Corrigé** — le
geste 1 en fait une liste, le geste 2 en fait un bloc." And the
constraint's place in the rule was asked: `docs/verification/agent-decoupeur.md`
L61-66 (B-1, TO FIX: "the rule and the move must list the same things")
and L137-142 (D-3, TO FIX, same ask); the report's part 2 records both
fixed at L61-63 and L173-176 (L34, L43). The rule's tie to the
qualifieur's genre is the chain's own design — `qualifieur.md` L85-88:
"One block, one genre. The decoupeur ran before you, and a block carries
one subject: one trigger, or what nothing fires at all."

---

## decoupeur.md F08 — one block, two triggers, no home for the sentence

Verdict: confirmed
Decision: Restore the refonte's answer to C6 — two events with one identical consequence are one trigger with two values, and the criterion is the consequence, not the number of sentences; drop the paragraph that counts them as two, and qualify the two-pieces-of-data rule with "when what follows each differs".
Where: decoupeur.md L145-151 ↔ decoupeur.md L51, L53-55, L57-59, L220-221
Owner: decoupeur
Also in: —

Cited: decoupeur.md L146-147 — "The sentence sits whole in one block,
and there is nothing impossible about it." L149-151 — "by *What a
trigger is*, two pieces of data are two triggers — but both are in your
hands, and you split without rewording anything." L51 — "A block carries
one trigger." L220-221 — "Every sentence of the block you split lands in
one of the new blocks, and in one only."

The four lines cannot all hold: a sentence carrying two triggers that
sits whole in one block gives that block two triggers, and moving it to
one of the two trigger blocks strips the rule from the other datum. The
contradiction dates from the round-1 fix of D-2
(`docs/verification/agent-decoupeur.md` L129-135), which objected to a
count "turning on punctuation" — a fair objection — and was closed by
flipping the count to two instead of re-grounding the count on the
consequence. The refonte had settled it the other way (L35: "lines
133–136 settle the identical-consequence question (one trigger)"). One
trigger, whether written as one sentence or two, answers D-1 (nothing to
split, nothing blocks), D-2 (the count no longer depends on grammar) and
this finding, and matches L53-55 ("a trigger telling three cases apart
gives one block with three cases"). The qualifier on L57-59 is what
keeps "two pieces of data are two triggers" from contradicting it.

---

## decoupeur.md F09 — the sequel-block rule needs a block you may not read

Verdict: confirmed
Decision: State that the judgement is made on the named block alone — its only trigger is an event of the kind a trigger produces (a response, a screen filled) and the block holds no event that produces it; no other block is opened, and the report names only the block looked at.
Where: decoupeur.md L92-96 ↔ decoupeur.md L40-45, L248-249
Owner: decoupeur
Also in: —

Cited: decoupeur.md L92-93 — "A block whose only trigger is the sequel
of another block's — the Rédacteur wrote the response as a block of its
own." L40 — "When it names blocks, you read those blocks, not the file."

The report severity is higher than the defect: the criterion is
decidable from the block itself — L79-81 defines a trigger within the
block ("an event no trigger of this block produced"), and L84-87 says a
response is a sequel by nature — and the report line asks the identifier
of the block looked at, not of the other one. What the text lacks is the
statement that no other block is needed; as worded, "another block's"
sends the agent looking for one.

---

## decoupeur.md F10 — the resume branch leads nowhere

Verdict: confirmed
Decision: Remove the agent's resume-on-a-filled-decision branch and the "plus a blocking file, when it names one" reading exception — a filled `blocked_decoupeur.md` is consumed by `/2_structure`, and the agent meets only the `MODIFIED` block that rewrite produced.
Where: decoupeur.md L153-156, L32-33 ↔ decoupeur.md L139-143; 3_decoupe.md L39, L136, L151-157; 2_structure.md L120, L191-194; redacteur.md L533
Owner: 3_decoupe (the blocking file's state machine is the command's)
Also in: — (F15 and chemins-amont F05 below are the same decision from the command's side)

Cited: decoupeur.md L153-154 — "A blocking file the prompt names carries
a filled `## Decision` — it says what was settled, and you resume with
it." L141 — "You may not reword it into two". 2_structure.md L120 — "A
`blocked_decoupeur.md`, `blocked_qualifieur.md` or `blocked_classeur.md`
with a filled `## Decision` | **2 — Integrating** | That file — all three
block on something only a rewrite of the block settles, and rewriting is
yours". redacteur.md L533 — "`blocked_decoupeur.md` | A sentence carries
two triggers — the decision says how to say it in two".

The only blocking cause resumes by a rewording (L142-143), which the
Rédacteur applies and files (2_structure.md L191-194). The agent's
branch would receive a decision it may not apply, and block again on
the same sentence.

Follows: decoupeur (drops L153-156 and the exception at L32-33; keeps
L114, since it still writes the file).

---

## decoupeur.md F11 — a first turn that "names none" and "names every block"

Verdict: confirmed
Decision: One phrasing for the first turn — the prompt says "every block", as the command's own template already does — and the agent's three lines key on that one form.
Where: decoupeur.md L37-38, L45, L162-164 ↔ 3_decoupe.md L69-70, L135
Owner: 3_decoupe (writes the prompt)
Also in: —

Cited: 3_decoupe.md L69-70 — "every block. Name none in the prompt."
L135 — "Look at these blocks: <B7, B28 — or: every block>."

The command contradicts itself before the agent does: L70 names none,
L135 writes "every block". The agent inherits both — L37 "On a first turn
it names none", L45 "Only a turn that names every block is read whole",
L162-164 "or none at all on a first turn".

Follows: decoupeur.

---

## decoupeur.md F12 — `Global:` in the example, not in the enumeration

Verdict: confirmed
Decision: Name `Global:` in the enumeration of what each half carries, as conditional on the original carrying one, and make the example say it shows a block whose original carried one.
Where: decoupeur.md L197-199 ↔ decoupeur.md L204, L230-233
Owner: decoupeur
Also in: —

Cited: decoupeur.md L197-199 — "Each block you produce carries a title,
an empty `Genre:`, an empty `Nature:` and `NEW`". L204 — "Global: ##
Activity screen". L233 — "The original carried none, the halves carry
none."

---

## decoupeur.md F13 — the sequel report reaches nobody

Verdict: confirmed
Decision: Add a relay row — the identifiers the agent reports as sequel blocks are relayed to the Product Owner as they stand, with no change to the next step.
Where: decoupeur.md L248-249 ↔ 3_decoupe.md L193-218
Owner: 3_decoupe
Also in: —

Cited: decoupeur.md L248-249 — "And any block whose only trigger is
another block's sequel — by identifier: you left it alone, and the two
carry one behaviour." 3_decoupe.md L193-218 carries the counts (L195),
the list comparison (L197-208) and the next-step table (L213-216) — no
row for that report.

Who acts on the signal is the merge question — `## To settle`, F17.
The relay row does not wait on it: without the row the report is lost
whatever the answer.

---

## decoupeur.md F14 — a blocking file always comes with a short list

Verdict: confirmed
Decision: On a blocking file, no re-invocation — the short list is expected, the file is relayed and the command stops; the re-invocation rule applies to a short list that comes with no blocking file.
Where: 3_decoupe.md L202-203 ↔ 3_decoupe.md L220, decoupeur.md L125-126
Owner: 3_decoupe
Also in: —

Cited: decoupeur.md L125-126 — "The blocking file names the block you
stopped on, and a rerun starts from there." 3_decoupe.md L202-203 — "A
short list: invoke the decoupeur again on the blocks it did not reach,
and nothing else." L220 — "If it returns `blocked_decoupeur.md`: relay it
and stop."

---

## decoupeur.md F15 — `/2_structure` consumes the file first

Verdict: confirmed
Decision: Same as F10 — `/3_decoupe` stops on any `blocked_decoupeur.md` at the unnumbered name (empty: fill it; filled: `/2_structure` first), and drops the prompt's third line and the post-run rename, which `/2_structure` L191 already does.
Where: 3_decoupe.md L39, L136, L151-157 ↔ 2_structure.md L191-194
Owner: 3_decoupe
Also in: —

Cited: 2_structure.md L191-194 — "A `blocked_decoupeur.md` it applied is
renamed — `blocked_decoupeur-NN.md`, the highest in the folder plus one.
Left at the unnumbered name it reads as a block still standing, and
`/3_decoupe` stops on it." 3_decoupe.md L39 — "Its `## Decision` is
filled | Name it in the prompt". L153-154 — "git mv
docs/features/<name>/blocked_decoupeur.md
docs/features/<name>/blocked_decoupeur-NN.md".

Follows: decoupeur (F10).

---

## decoupeur.md F16 — the kept half of a `NEW` original becomes `MODIFIED`

Verdict: confirmed
Decision: The kept half keeps the original's marker — `NEW` stays `NEW`, anything else becomes `MODIFIED` — aligned on the Rédacteur's rule.
Where: decoupeur.md L217 ↔ redacteur.md L104-105
Owner: decoupeur
Also in: redacteur (reads only — its rule is the one adopted)

Cited: redacteur.md L104-105 — "a block already carrying `NEW` keeps
`NEW`, which says more." decoupeur.md L217 — "It then carries `MODIFIED`,
not `NEW`."

The reason at L212-215 for keeping the number ("something already points
at that number") does not carry the marker with it: nothing has probed a
`NEW` block yet, so nothing was closed against it, and `MODIFIED` on it
says a closure was undone that never happened. Costs nothing today —
`4_grille.md` L114-118, `3a_genre.md` L101, `3b_nature.md` L98 and
`3_decoupe.md` L79-82 take the union — and stops costing nothing the
day a reader distinguishes them. Open since the pass file (round 1 D-9,
report L49).

---

## decoupeur.md F17 — a merge belongs to no agent

Verdict: confirmed
Decision: The qualifieur and the classeur stop attributing a merge to the decoupeur — their never-do line says a split or a merge is not theirs, without naming an owner; who merges is settled below.
Where: classeur.md L181, qualifieur.md L214 ↔ decoupeur.md L110
Owner: decoupeur (its L110 is the rule the two others contradict)
Also in: qualifieur, classeur

Cited: classeur.md L181 — "Split a block, or merge two — that is the
decoupeur's". qualifieur.md L214 — "Split a block, or merge two — that
is the decoupeur's". decoupeur.md L110 — "Merge two blocks — that is not
yours".

Follows: qualifieur, classeur.

---

## decoupeur.md F18 — "a rerun starts from there"

Verdict: confirmed
Decision: Stop saying the blocking file drives the rerun — the markers, which a grid turn alone strips, are what bring every block not reached back into the next turn's list; with F10 applied the rerun is an ordinary turn.
Where: decoupeur.md L126 ↔ 3_decoupe.md L77-91, L72-75
Owner: decoupeur
Also in: —

Cited: 3_decoupe.md L72-75 — "The markers are still there, whatever
earlier turns did — the Rédacteur strips them only once a grid turn has
consumed them. So they say nothing about what you have already looked
at, and every block is yours until the grid has run." L90-91 — "a block
an answer touched carries `MODIFIED`, and the second grep finds it."

The outcome the sentence promises holds — the unreached blocks still
carry their markers — but by the greps, not by the file. The halves
written before the stop carry `NEW`/`MODIFIED` too and are looked at
again: harmless, each carries one trigger.

---

## chemins-amont.md F05 — two commands claim one filled `blocked_decoupeur.md`

Verdict: confirmed
Decision: Same as F10 and F15 — the filled file is `/2_structure`'s alone; `/3_decoupe` stops on it and says so.
Where: 3_decoupe.md L39 ↔ 3_decoupe.md L215, decoupeur.md L141
Owner: 3_decoupe
Also in: —

Cited: 3_decoupe.md L215 — "Fill its `## Decision`, then `/2_structure`
— it blocks on a sentence carrying two triggers, and rewording is the
Rédacteur's. `/3_decoupe` again afterwards". decoupeur.md L141 — "You
may not reword it into two, you may not drop it, and it cannot sit in
two blocks."

Follows: decoupeur (F10).

---

## chemins-amont.md F03 — only the decoupeur's file is renamed

Verdict: confirmed
Decision: `/2_structure` renames whichever of the three blocking files it applied, not only `blocked_decoupeur.md`.
Where: 2_structure.md L120 ↔ 2_structure.md L191-194
Owner: 2_structure
Also in: redacteur, qualifieur, classeur (renommages.md F10 carries the same fact, accented "Découpeur")

Cited: 2_structure.md L191-192 — "A `blocked_decoupeur.md` it applied is
renamed — `blocked_decoupeur-NN.md`, the highest in the folder plus
one." L120 names all three files as invocation 2's input.

Nothing in the decoupeur's own text changes — the entry is here because
the filter caught the file name. The decoupeur is neither Owner nor
Follows.

---

## Not carried

The report's part 2 leaves five round-1 items `open` (C12, B-2, B-3,
B-4, D-11) and three `other` (C14, D-8, D-9). C14 is F04 and D-9 is F16
above. The six others produced no second-round finding — B-2 a
justification paragraph, B-3 extra wording, B-4 an unchanged
description, C12 an example's vocabulary, D-8 "read" in two senses,
D-11 a fact about the caller — and this plan does not reopen them.

`passages-amont.md` L17 lists the decoupeur among the files whose block
shape and genre/nature values were checked and found sound — nothing to
do.

---

## To settle

### F01 — the `Clarification needed` stop: restore it, or record its removal

The refonte kept the stop in the agent (index L318: the command greps
the whole file, the agent its blocks — "si la commande change, l'agent
tient encore"). Round 1 found its only outcome was a reply the file
itself says gets lost (D-4), and the correction removed it. The two
records now disagree, and the choice is scope: does the agent carry a
guard of its own against a `Clarification needed` line, or does it rely
on the command's grep (`3_decoupe.md` L44-47)?

| Option | What it costs |
|---|---|
| **A — restore the stop, with a blocking file as its outcome** | A second blocking cause in a file built around one (L135-137, round 1 D-10); a `To resume` that routes to `/2_structure` like the first; the command's relay row already covers a blocking file (L215), so no new row. The guard holds if a command ever drops its grep. |
| **B — record the removal** | An index line to amend in `docs/refonte/modifications.md`, outside this campaign's perimeter. The agent has no guard of its own; a `Clarification needed` line reaches it only if the command's grep is dropped, and would then go unsplit to the qualifieur. |

### F17 — who merges two blocks

The decoupeur reports a block whose only trigger is another block's
sequel (L92-96, L248-249) and may not merge (L110); the qualifieur and
the classeur name the decoupeur as the merger (settled above: they stop
doing so). After F13 the signal reaches the Product Owner. Who acts on
it is a question of chain scope.

| Option | What it costs |
|---|---|
| **A — the Rédacteur merges, on a Product Owner decision** | A route: the relayed identifiers become a decision the Rédacteur applies as a rewrite (it already rewrites on a filled `## Decision`, redacteur.md L527-540); the merged block carries `MODIFIED`, the retired number is a reference to redirect. Fits the Rédacteur's role as the only writer of the product file. |
| **B — nobody merges; the double probe is accepted** | Zero text beyond F13's relay row and F17's rewording. The grid probes one behaviour twice, and the two blocks' answers can diverge; the sondeur has no rule for that. |
