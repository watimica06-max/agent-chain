# Plan — controleur

Built against `.claude-new/agents/controleur.md`, `.claude-new/commands/9_controle.md`
(the only command that invokes it; `2_structure.md` L176 names it once, as a place
where a gap surfaces — nothing to correct), the report `docs/verification2/controleur.md`
(both parts), `docs/verification2/decisions.md`, and the six thematic reports filtered
to `controleur`. Every cited line was opened before its verdict; the other side of each
two-file `Where` is quoted in the entry.

Two of the fourteen settled questions name this agent — `controleur.md` F11 and F12 —
and are applied below as written. A third, `passages-aval.md` F15, lists `9_controle`
among the readers that must match the `PASS` prefix (9_controle.md L60, "no `verdict.md`
in PASS"): that is a command line, owned by the relecteur's plan and the commands plan,
and nothing in `controleur.md` reads a verdict. No entry below contradicts a decision.

The filter on the six thematic reports yields one finding beyond this agent's own
report: `fichiers.md` F10. The five that name `9_controle` and no agent
(chemins-aval F13, F14, F16 · passages-amont F08 · passages-aval F15) are not this
plan's.

Line numbers are those of the files as they stand today, in `.claude-new/`.

---

## Report `controleur.md`

### controleur.md F01 — the index counts the pass sheet under the wrong numbers

Verdict: confirmed
Decision: Realign the index's controleur section with the pass sheet's own numbering — its `C14` (script assembly, écarté) is pass `### 13`, its `C13` matches no pass comment, and pass `### 14` (never-do cleanup, `Edit` dropped) and `### 15` (feature folder) are applied in the file and counted nowhere — so that the passed count and the "no modification of the working file" line say what the file holds.
Where: modifications.md L1249-1258 ↔ passes/controleur.md L471-540
Cited: modifications.md L1243-1244 — "✅ **FAIT** — 📌 **aucune modification du fichier de travail** ; sa fiche de passe est passée."; L1248-1249 — "Passés (11) — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 · C15"; L1251 — "Écartés (1) — C14"; L1257 — "**C14** | Faire l'assemblage par un script"; L1258 — "**C11 · C12 · C13** | Le propriétaire du groupement, le worktree, les issues | 📌 **Sur `/9_controle` et `/8_code`**". passes/controleur.md L471-474 — "### 13 … Cible: Invocation 2 as a whole" (the script proposal, L486-489 "The assembly is a script beside `grouper.py`"); L502-505 — "### 14 … Cible: 'What you never do' — entries 'Relaunch anything' and 'Report a lot as failed'; 'When `Edit` fails'"; L540-543 — "### 15 … Cible: 'The files, in the working folder you were given'". controleur.md L4 — "tools: Read, Grep, Glob, Write" (pass 14's `Edit` drop, applied); L26-27 — "The files, in the feature folder the prompt names. 🔴 That folder holds `desc-produit.md` and `code/` — ⚠️ never a sub-folder of it." (pass 15, applied).
Owner: the index `docs/refonte/modifications.md` — `controleur.md` itself is unchanged by this entry
Also in: —

Part 2's open rows `A` (numbering question) and `B.2` (`Edit` dropped, "whether the sheet counts 14 as passé") are this finding; they close with it. Pass 13 is the only one the index sets aside, and it is set aside on the pass sheet's own doubt (L486-489 "I am not sure of this one") — the decision keeps that outcome, it renumbers it.

### controleur.md F02 — pass 14 applied except its last part

Verdict: confirmed
Decision: Finish pass `### 14` — drop the two "never this file" lines and their justifications at L66-71, which the reading rule at L55-57 already covers — and record the pass as applied under its own number in the index (F01); if the Product Owner kept those two lines on purpose, the index says so instead and the lines stay.
Where: passes/controleur.md L502-538 ↔ controleur.md L66-71
Cited: passes/controleur.md L529-533 — "The two justifications and the two 'never this file' lines go; the reading rule 'the blocks and sheets the prompt names, and nothing else' already covers them." controleur.md L66-67 — "🔴 **Never `idees.md`** — the raw text the upstream chain spent its whole loop correcting."; L69-71 — "🔴 **Never the code** — the Relecteur checked sheet against code. ⚠️ **Never the technical document, the lot list or the sequence**: you check the result of those transformations, not the transformations."; L55-57 — "`desc-produit.md` — 🔴 only the blocks your group names · The sheets your group names … 🔴 those, and no other".
Owner: controleur
Also in: —

"Never the code" at L69 stays: it is a never-do the body can violate (L97 repeats it) and pass 14 keeps it. Only `idees.md` and the technical document / lot list / sequence go.

### controleur.md F03 — the "How you find things" block is unrecorded

Verdict: confirmed
Decision: Record in the index's controleur section that L36-43 (the `^### B15 ` grep, the trailing space, "never a whole read to find a block") was added by the first verification round's correction `C` (tool no gesture names), since the section states the pass sheet alone was applied.
Where: controleur.md L36-43 ↔ modifications.md L1241-1275
Cited: controleur.md L38-40 — "🔴 **A block, by grep** — 📌 `grep '^### B15 '` in `desc-produit.md`, the space ending the number: ⚠️ **a grep on `B15` alone also hits `B150`.**"; L42-43 — "🔴 **Never a whole read to find a block**". modifications.md L1243-1244 — "aucune modification du fichier de travail ; sa fiche de passe est passée." — the section names the fifteen pass comments and nothing else. Part 2, row "C · tool no gesture names (`Grep`) | fixed | controleur.md:38-40" is where the block came from.
Owner: the index `docs/refonte/modifications.md` — the block itself is sound and stays
Also in: —

Same shape as `lexicographe.md` F02 in the lexicographe plan: the rule is right, the record is short.

### controleur.md F04 — C12 listed reported, already applied

Verdict: confirmed
Decision: Move C12 from the index's "Reportés" to its applied list, since both commands already carry its one-owner outcome.
Where: modifications.md L1256 ↔ 9_controle.md L53-55
Cited: modifications.md L1250 — "⚠️ **Reportés (3)** — C11 · C12 · C13"; L1258 — "Sur `/9_controle` et `/8_code`, que A4 et A5 réécrivent". 9_controle.md L53-55 — "🔴 **It runs on the main cycle and on every correction cycle.** ⚠️ **The Contrôleur runs on the main cycle alone**" — nothing in L42-58 says `/8_code` runs him. 8_code.md L12-14 — "📌 **It never invokes the Contrôleur** — 🔴 **he needs his blocks and his sheets named in the prompt**, and the grouping that names them lives in `/9_controle`."; L254-257 — "🔴 **You never invoke the Contrôleur** … 📌 **Say that `/9_controle` is what comes next** — 🔴 **run by hand, on both cycles.**"
Owner: the index `docs/refonte/modifications.md`
Also in: —

Part 2 already marks "C12 · NOTE | fixed" at `8_code.md:12-14, 254-255`; the index is the only side still saying otherwise.

### controleur.md F05 — the grep locates, nothing bounds the read

Verdict: confirmed
Decision: State how far the read that follows the grep goes — from the block's own heading to the line before the next block heading — and the bounded call that does it, so that "never a whole read" is a rule the agent can obey without choosing.
Where: controleur.md L38 ↔ controleur.md L42-43
Cited: L38 — "A block, by grep — `grep '^### B15 '` in `desc-produit.md`"; L42-43 — "🔴 **Never a whole read to find a block** — 📌 **the product file is the whole product**, and your group holds a handful of its blocks." — no line between them, and none in PART 3, says what is read once the heading's line is known; 5_reclasse.md L160-161 states the bound this file lacks: "A block runs from its `### B` line to the next heading of any level."
Owner: controleur
Also in: —

One grep of `^### B` gives every heading's line number at once; the bound of each block is the next one. That is the owner's form to write, not this plan's.

### controleur.md F06 — an absent field, two contradictory readings

Verdict: confirmed
Decision: Make a present partial a group that ran, whatever it lacks — a block absent from every field of a present partial goes under `## Doubts` naming the group and what the partial lacks (a field, the opening line) — and rewrite L237-238's reason to say that, since a group that did not run is told by the absent file (L289-292), never by an absent field.
Where: controleur.md L237-238 ↔ controleur.md L282, L289-292
Cited: L237-238 — "🔴 **Write the three fields even when empty.** An absent field reads as *this group did not run*."; L281 — "**A block no partial mentions, and its group did report** | 🔴 **Under `Doubtful`**"; L282 — "**A group named by the prompt whose partial is not there** | 🔴 **Every block it was given goes under `Doubtful`**"; L289-292 — "⚠️ **a group that ran and found nothing has an opening line; a group that did not run has no file at all.**" — a partial present with a field missing matches neither row.
Owner: controleur
Also in: —

Row 1 of the table already carries most of the outcome (a block no partial mentions, group reported → Doubts); what is missing is the sentence that a lacking field does not change the row, and the false reason at L238. F11 below adds the opening line to the same check.

### controleur.md F07 — an absent sheet: Doubtful at L85, Missing at L193

Verdict: confirmed
Decision: Say, at L85 or at L193, that a sheet named and not there is not a sheet observing nothing — the `Missing` fact at L190 needs every named sheet read, so the absent sheet's intentions are `Doubtful` and L193 governs only what a read sheet fails to observe.
Where: controleur.md L85 ↔ controleur.md L193
Cited: L85 — "🔴 **Every intention of the blocks it was to answer for goes under `Doubtful`**, naming the lot — 📌 **and the run carries on**"; L190 — "**Missing** | 🔴 **No signature and no criterion of your group's sheets observes the intention** — 📌 **that is something you can state**"; L193 — "⚠️ **An intention nothing observes is `Missing`** — 📌 **not a doubt.**"
Owner: controleur
Also in: —

The two rules do not send the same line to two fields once L190 is read with them — an unread sheet cannot be stated to observe nothing — but L193 alone reads the other way, and it is the sentence the agent meets last. One clause closes it. Not overstated: NOTE is the severity it carries.

### controleur.md F08 — "under `Doubtful`", a heading no file has

Verdict: confirmed
Decision: Route every line to the field by its heading — `## Doubts` — wherever the text sends a line somewhere (L85, L281, L282), and keep `Doubtful` only as the outcome's name in the L154-158 table, so that the place named is one the partial and the report carry.
Where: controleur.md L85, L281-282 ↔ controleur.md L227, L255
Cited: L85 — "goes under `Doubtful`, naming the lot"; L281 — "🔴 **Under `Doubtful`**"; L282 — "🔴 **Every block it was given goes under `Doubtful`**, naming the group"; L227 — "    ## Doubts"; L255-256 — "📌 **A partial that leaves you unable to write a line goes under `## Doubts`, naming the group**" — the same routing, written both ways in the same file. 9_controle.md L269-270 reads "the `## Doubts` and `## Intentions missing` sections" — the heading is the name the command keys on, so the heading stays.
Owner: controleur
Also in: —

### controleur.md F09 — "prose", one word for two things

Verdict: confirmed
Decision: Rename the register rule at L304 so it speaks of the lines' language (English, present indicative, active voice) and "no prose" at L233 keeps its meaning of no paragraphs.
Where: controleur.md L233 ↔ controleur.md L304
Cited: L233 — "🔴 **One line per entry, no prose.**"; L304 — "**Prose**: 🔴 **English, present indicative, active voice.**"
Owner: controleur
Also in: —

### controleur.md F10 — the unchanged block answers as a whole

Verdict: confirmed
Decision: Name the unchanged block (L195-197) as the one case where a block gets a single line, at L104 or at L195-197, so the never-do "answer for a whole block at once" and the example at L217 no longer contradict each other.
Where: controleur.md L104 ↔ controleur.md L217
Cited: L104 — "🔴 **Answer for a whole block at once** — one line per intention"; L217 — "    B9 Retention window — unchanged, nothing to build"; L195-197 — "⚠️ **A block describing what does not change** — an inherited rule, restated for context — carries no intention to find. Say so under found, with that reason." — sanctioned, but not said to be the exception.
Owner: controleur
Also in: —

### controleur.md F11 — the partial's opening `Blocks:` line has no reader

Verdict: confirmed
Decision: Apply `decisions.md` — give the opening line its reader at assembly move 3: the prompt's per-group list is authoritative, the opening line says which blocks the group actually treated, and a difference between the two is a line of the report naming the group, never a choice of one list over the other.
Where: controleur.md L205-209 ↔ controleur.md L246-248, L281-282
Cited: L205-209 — "🔴 **It opens with the blocks you were given**, one line, in this exact form — 📌 **that is what says a group ran and answered for none of them:** Blocks: B4, B5, B9, B12"; L246-249 — "🔴 **The prompt names the groups this run issued, and the blocks each was given — one line per group.** 📌 **That is your list to check against**"; L281-282 — the two rows of move 3, both keyed on the prompt's list and the file's presence, neither on the opening line; L289-292 credits the line again ("that is what tells the two cases apart") without a move that reads it. decisions.md L59-65 — "🔴 **The prompt's list is authoritative.** 📌 **The opening line says which blocks the group actually treated** — 🔴 **a gap between the two is a finding of the report**, ⚠️ **never a reason to pick one over the other.**"
Owner: controleur
Also in: —

Which field carries that line is the owner's form; `## Doubts` naming the group is where the neighbouring cases already go (L255-256, L281). No change to the `9_controle` prompt — it already carries the per-group list (9_controle.md L215-218).

### controleur.md F12 — the sheets a correction cycle wrote

Verdict: confirmed
Decision: Apply `decisions.md` — phase 1 of `/9_controle` marks `carried` the blocks a correction cycle built, like the four genres that produce no lot, and the mark gets a path from the map to the report: a place in the `tracabilite-full.md` format, a grouping that does not read a carried block as a block with no lot, and an invocation-1 line for it under `## Intentions found` with the cycle that built it as the reason.
Where: 9_controle.md L68-70 ↔ 8_code.md L25
Cited: 9_controle.md L68-70 — "📌 **An existing `rapport-controle.md` is not a reason to stop.** He writes the next free number beside it; that is how two states are compared."; L26 — "**A `bugfix-NN/`** | 📌 **Phases 4 to 6 only** — ⚠️ **the Contrôleur confronts a product file with the sheets built from it, and a correction cycle has neither**"; controleur.md L48 — "a spec sheet | `code/<lot>/fiche-executable.md`" under the feature folder (L26-27). decisions.md L69-76 — "🔴 **Mark `carried` the blocks a correction cycle built**, like the four genres that produce no lot. 📌 **They are not missing intentions** — ⚠️ **they were built, elsewhere**, and the map has to say so".
Owner: `9_controle` — phase 1 owns the map and decides the form of the mark
Follows: controleur (a `carried` block in its prompt or its map gets a found line, never a Missing one — today the file has no rule for the word); `.claude-new/scripts/grouper.py` (L36-37 "Any line without a lot reference is ignored. Blocks with no lot are kept as free fillers." — a `B12  carried` line is parsed at L51-55 as a block with no lot and lands in a group that reads no sheet for it)
Also in: —

⚠️ The path is missing already for the existing `carried`: 9_controle.md L130-131 says "mark those entries `carried`, never as a block with no lot", the format at L138-146 has no token for it ("its identifier, then the lots that build its entries … nothing else on the line"), L157-159 gives a dash to "a block whose entries no lot cites", and `controleur.md` never meets the word. The decision widens a mark that today reaches nobody. What identifies the blocks a correction cycle built is not settled — see `## To settle`.

### controleur.md F13 — `MODIFIED` reaches the agent with no instruction

Verdict: confirmed
Decision: Extend the L59-60 rule to both markers the Rédacteur leaves on a heading line — `NEW` and `MODIFIED` — ignored alike.
Where: controleur.md L59-60 ↔ redacteur.md L104
Cited: controleur.md L59-60 — "📌 **A title may end in `NEW`** — an upstream working marker. It is not part of the title; ignore it."; redacteur.md L99 — "🔴 **`MODIFIED` on every block you change** — ⚠️ **whether or not a question named it.**"; L104-105 — "marks every block of the file `MODIFIED` — 📌 **a block already carrying `NEW`** keeps `NEW`"; L59 — "    ### B7 — Rejecting invalid durations    MODIFIED". The markers live in `desc-produit.md`, the file the agent reads (controleur.md L55): 5_reclasse.md L167-168 strips them from the `desc-par-nature.md` copy only ("strip a trailing `NEW` or `MODIFIED` from the `### B` line"), and the Rédacteur strips them only when a grid turn ran (redacteur.md L119) — a `MODIFIED` set by the last integration of conversion answers is still there at `/9_controle`.
Owner: controleur
Also in: —

The `^### B15 ` grep is unaffected: both markers are trailing.

### controleur.md F14 — "criterion 2", a position on an unnumbered list

Verdict: confirmed
Decision: Cite a criterion by what the sheet carries — its text, or its opening words — never by a counted position, in the L215-216 example and wherever a found line names one.
Where: controleur.md L215-216 ↔ detailleur.md L232-237
Cited: controleur.md L215-216 — "    B4 Daily step panel — lot-07, criterion 2 / B5 Tapping the panel — lot-07, criterion 4"; detailleur.md L232-237 — "    ## Acceptance criteria — - Two entries of the same type 2h apart produce a single entry — - Two entries of the same type 4h apart produce two entries — …" an unnumbered bullet list. testeur.md L272 cites the same list by text — "<one line per criterion: the criterion, and the test that covers it>"; relecteur.md L140 counts it — "point 2 — criterion 3 has no test".
Owner: controleur
Also in: relecteur plan, if it takes up L140 — the same habit on the same list; detailleur plan, if it numbers the criteria at the source, in which case this line cites that number instead and the decision here is moot

The cheaper fix is on the reader: numbering the list at the Détailleur would touch four readers (concepteur, testeur, relecteur, controleur) for one example line. Citing the text is what the Testeur already does.

---

## Report `fichiers.md`

### fichiers.md F10 — `/8_code` credits the Contrôleur with a blocking file

Verdict: confirmed
Decision: Remove the Contrôleur from the 8_code.md L415-416 sentence — he writes no blocking file, and `/8_code` never invokes him — leaving the Relecteur alone in it.
Where: 8_code.md L415 ↔ controleur.md L75
Cited: 8_code.md L415-416 — "📌 **The Relecteur and the Contrôleur do not call it either** — 🔴 their blocks say something is missing, not something to settle."; controleur.md L75-78 — "## You never write a blocking file — 🔴 **Everything you find goes in your report**"; 8_code.md L254-255 — "🔴 **You never invoke the Contrôleur**". fichiers.md L24 confirms this is the residual: "no command or agent expects a Contrôleur blocking file beyond the residual sentence of F10".
Owner: `8_code` — the sentence is the command's; `controleur.md` is unchanged
Also in: — (the finding names an agent, so the commands plan does not carry it; the relecteur half of the sentence stands and is not this plan's)

---

## Residuals of part 2 marked `other`

Not numbered findings; each was re-read and holds. They are cheap, and two of them are the kind of duplicate the numbered findings above correct elsewhere.

### part 2 · D.12 — "no product file → stop and say so", twice

Verdict: confirmed
Decision: State the no-product-file stop once, and have the other place point to it.
Where: controleur.md L84 ↔ controleur.md L125-127
Cited: L84 — "**No product file** | 🔴 **Stop and say so, no file** — 📌 **the command checks the same thing before invoking you**"; L125-127 — "🔴 **A feature cycle only.** ⚠️ **No `desc-produit.md` in the folder the prompt names means you were invoked on a bug-fix cycle** — 📌 **stop and say so**".
Owner: controleur
Also in: —

### part 2 · D.1 — L160 narrower than the unit it names

Verdict: confirmed
Decision: Make L160 name the cut the way L143-145 defines it — a sentence, a table row, a list item, a branch — not "the sentence" alone.
Where: controleur.md L160 ↔ controleur.md L143-145
Cited: L160 — "📌 **Name the block and the sentence** when a block holds several."; L143-145 — "🔴 **The unit is the intention, never the whole block** — 📌 **a sentence carries one most of the time**, ⚠️ **but a table row, a list item and a branch of a flow are cuts too.**"
Owner: controleur
Also in: —

### part 2 · C1 NOTE — the Found/Missing boundary stated three times

Verdict: confirmed
Decision: — (no change asked by the report; the three statements — L154-158, L190-191, L193 — agree with each other once F07 is applied, and the F07 edit is the one that touches them)
Where: controleur.md L154-158 ↔ controleur.md L190-193
Owner: controleur
Also in: —

### part 2 · C5 NOTE — never stops on an assembly fault

Verdict: confirmed
Decision: — (the report asks no change and the file's behaviour — carry on, file under `## Doubts` — is what pass 5 endorses; F06 and F11 above complete the cases it files)
Where: controleur.md L85 ↔ controleur.md L254-256
Owner: controleur
Also in: —

---

## To settle

### What names, on a correction cycle, the block a lot built (from F12)

`decisions.md` settles that those blocks are marked `carried`. It does not say where phase 1 finds them, and no bugfix file names a product block: `bug-list.md` is free form (diagnostiqueur.md L51 — "**Free form** — a sentence naming what is wrong, and what it should be"), a `desc-bug.md` entry carries a `Bearer:` that is a code symbol (diagnostiqueur.md L254 — "Whatever answers it is the bearer, whatever its form"), and the bugfix folder has no `tracabilite.md`. The Contrôleur's own report is the one file of the chain that names blocks and feeds a bug list (9_controle.md L345-346).

| Option | What it costs |
|---|---|
| **a.** The bug list carries the `B<n>` of the report line it comes from, and the diagnosis carries it through to `desc-bug.md` and the lot list | One field on three files the Product Owner and two agents write — the join exists by construction; a gap she adds from use, with no block, stays unmarked |
| **b.** Phase 1 greps the bugfix sheets for `B<n>` | Nothing to add, but the Détailleur is not told to write the block id in a sheet, so the grep finds what happens to be there |
| **c.** Phase 1 marks `carried` every block the latest report listed as missing, when a later `bugfix-NN/` exists | Nothing to add, but a gap set aside at diagnosis (decisions.md L91-97) is marked built when it was not — the very case the decision forbids |

Decision: — (turns on what a correction cycle's files carry, and on who writes it)

### Whether the two "never this file" lines of L66-71 were kept on purpose (from F02)

The pass asked for their removal; the index records neither the pass nor a refusal. The plan decides to finish the pass (F02); if the Product Owner kept them deliberately, the index says "écarté" and F02 becomes a record entry only. Cost either way: two lines.

Decision: finish the pass, unless the Product Owner says otherwise — see F02
