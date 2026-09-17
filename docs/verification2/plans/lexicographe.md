# Plan — lexicographe

Built against `.claude-new/agents/lexicographe.md`, `.claude-new/commands/1_lexique.md`,
`.claude-new/commands/2_structure.md`, the report `docs/verification2/lexicographe.md`
(both parts), `docs/verification2/decisions.md`, and the six thematic reports filtered
to `lexicographe`. Every cited line was opened before its verdict; the other side of
each two-file `Where` is quoted in the entry.

None of the fourteen settled questions of `decisions.md` names the lexicographe or
`/1_lexique`; none of the entries below contradicts one.

---

## Report `lexicographe.md`

### lexicographe.md F01 — description written twice

Verdict: confirmed
Decision: Remove the duplicated clause from the frontmatter description so the registry entry states the third-and-fourth-invocation role once.
Where: lexicographe.md L3 ↔ modifications.md L22-23
Cited: modifications.md L22-23 — "aucune modification du fichier de travail *(sauf la ligne `en anglais`, décidée en séance)*"
Owner: lexicographe
Also in: —

L3 reads "…settle them in place and write the lexicon the chain reads afterwards; then on every answered questions file of the grid or of the conversion, to catch the words those answers bring, raise the ones that could name one same thing, and once answered, settle them in place and write the lexicon the chain reads afterwards; then on every answered questions file of the grid or of the conversion, to catch the words those answers bring." — the clause from "then on every answered questions file" onward is present twice.

### lexicographe.md F02 — numbering rule changed without a record

Verdict: confirmed
Decision: Keep the rule — root and `questions/lexicographe/` counted together is the only count that cannot collide once `/2_structure` has filed a file — and record the change in the index's lexicographe section.
Where: lexicographe.md L110-113 ↔ modifications.md L22-23
Cited: modifications.md L22-23 — "aucune modification du fichier de travail *(sauf la ligne `en anglais`, décidée en séance)*"; 2_structure.md L86-87 — "git mv docs/features/<name>/questions-lexicographe-NN.md docs/features/<name>/questions/lexicographe/"
Owner: the index `docs/refonte/modifications.md` — `lexicographe.md` itself is unchanged
Also in: —

The index states no change to the working file; L110-113 carries one. The rule is sound, so the correction is to the record, not to the rule.

### lexicographe.md F03 — invocation 3 sweeps the `Défaut:` line, unrecorded

Verdict: confirmed
Decision: Keep the move — an accepted proposal enters the product as an answer does — and record it in the index's lexicographe section.
Where: lexicographe.md L417-423 ↔ modifications.md L22-23
Cited: modifications.md L22-23 — "aucune modification du fichier de travail *(sauf la ligne `en anglais`, décidée en séance)*"
Owner: the index `docs/refonte/modifications.md` — `lexicographe.md` unchanged here; what the move lacks is F06
Also in: —

### lexicographe.md F04 — doubts into `## Non tranché`, unrecorded

Verdict: confirmed
Decision: Keep the widening — the command counts `## Non tranché` after every invocation, and a doubt written elsewhere is invisible to it — and record it in the index as the first round's D.6.
Where: lexicographe.md L104, L454-458 ↔ passes/lexicographe.md L72-79
Cited: passes/lexicographe.md L74-77 — "the lexicon has a named place for the inventory… distinct from the place for what awaits an answer; invocation 3 compares against both" (a comparison, not a write); 1_lexique.md L196-199 — "check `lexique.md` exists, and grep the lines under `## Non tranché`: what still waits on an answer… That section alone"; report Part 2 L35 — "D.6 | fixed | lexicographe.md 454–458"
Owner: the index `docs/refonte/modifications.md` — `lexicographe.md` unchanged
Also in: —

The widening came from the first round's correction D.6, not from the pass sheet, which is why C1 does not ask for it. It is what F07 is short of on the output side.

### lexicographe.md F05 — a meaning-scoped retirement re-merged by invocation 3

Verdict: confirmed
Decision: Give the `## Tranché` entry a way to say a replacement holds for one meaning only, and exempt such an entry from invocation 3's blanket swap — a retired term met in an answer under a scoped entry is raised as a question, never swapped.
Where: lexicographe.md L375-380 ↔ lexicographe.md L431-439, L140-155
Cited: L378-380 — "you swap the occurrences that carry that meaning, and them alone… Which occurrences carry which meaning is the answer's to say"; L431-433 — "Each term on a `remplace :` line of `lexique.md`, grepped in the answers and swapped for the entry it sits under"; L438-439 — "A retired term found is not a question: the decision is made"; L140-155 — the shape shows `remplace : atelier` and no scoped variant
Owner: lexicographe
Follows: redacteur — it writes its `en anglais` line "on its `## Tranché` entry" (redacteur.md L167-170), and a scoped entry carries two concepts, one per meaning
Also in: redacteur

Which meaning an occurrence carries is the Product Owner's to say (L378-380); invocation 3 cannot swap it on a grep, and the shape as written gives it no way to know the entry is scoped.

### lexicographe.md F06 — the accepted `Défaut:` line is swept but cannot be written

Verdict: confirmed
Decision: Extend to the `Défaut:` line of an entry whose `Answer:` is empty what invocations 3 and 4 do to an answer — the retired-term swap, the quote fix, the settling of 4 — and widen the write permission of L66-68 to that line.
Where: lexicographe.md L417-420 ↔ lexicographe.md L66-68, L431-433, L523-524
Cited: L417-420 — "And the `Défaut:` line of every entry whose `Answer:` is empty. Silence accepted that proposal, so its terms entered the product exactly as an answer's do"; L66-68 — "Write anywhere but… at invocations 3 and 4 — the answered file's `Answer:` fields"; L431-433 — "grepped in the answers and swapped"; L523-524 — "Replace, in the answered file's answers"
Owner: lexicographe
Follows: — (the Rédacteur integrates the line as it stands, redacteur.md L572-577, "you integrate the proposed answer as if he had written it"; the sondeur writes it, sondeur.md L386-391; neither changes)
Also in: —

The retired-term half will rarely fire — a `Défaut:` is "the transverse block, quoted in its own words" (sondeur.md L394-395), i.e. product-file vocabulary already settled — but the quotes half is live: a label proposed unquoted reaches the Rédacteur as a concept. The inconsistency between L417-420 and L66-68 stands whichever half fires.

### lexicographe.md F07 — invocation 3's outputs omit `## Non tranché`

Verdict: confirmed
Decision: Name `## Non tranché` in invocation 3's "What you write" and in its Outputs line, as the table at L104 and the body at L454-458 already do.
Where: lexicographe.md L104 ↔ lexicographe.md L504-509
Cited: L104 — "`lexique.md`, its `## Relevé` and `## Non tranché` updated"; L504-506 — "`lexique.md`, its `## Relevé` carrying the domain terms the answers brought"; L508-509 — "`lexique.md`, its `## Relevé` updated"
Owner: lexicographe
Also in: —

### lexicographe.md F08 — invocation 4 "adds" where invocation 2 "moves"

Verdict: confirmed
Decision: Make invocation 4's move 3 move each settled term out of `## Non tranché` into `## Tranché`, as invocation 2 does.
Where: lexicographe.md L549-552 ↔ lexicographe.md L191-193, L397-400, L457
Cited: L549-550 — "Add each settled term to `lexique.md`"; L191-193 — "A term leaves it when an answer settles it, and nothing else empties it"; L397-400 — "you move each answered term out of `## Non tranché` and into `## Tranché`"; L457-458 — "invocation 4 is told to move a term that was never there"
Owner: lexicographe
Also in: —

With F04's widening in place, invocation 3 does write doubts under `## Non tranché`; only invocation 4 can empty them, and it is told to add, not to move. The command's count (1_lexique.md L196-199) then reports a settled pair as waiting.

### lexicographe.md F09 — the readers list is short by one

Verdict: confirmed
Decision: Name invocation 2 among the lexicon's readers.
Where: lexicographe.md L211-212 ↔ lexicographe.md L103, L354
Cited: L211-212 — "by the Rédacteur, and by your own invocations 1, 3 and 4"; L354 — "Read the questions file, the idea file, and `lexique.md`"
Owner: lexicographe
Also in: —

### lexicographe.md F10 — a sweep protects terms no sweep can meet

Verdict: confirmed
Decision: Drop the rule that a sweep preserves the terms an answer brought; keep `(réponse)` as the mark of a term no count backs.
Where: lexicographe.md L199-204, L285-287 ↔ lexicographe.md L36-37, 1_lexique.md L87-91
Cited: 1_lexique.md L87-90 — "A `desc-produit.md` in the folder does not stop 3 or 4… It stops 1 and 2: the vocabulary is settled before the product file exists, never after"; L397-400 — invocation 2 "touch[es] nothing else" in the lexicon, so it adds no `## Relevé` term; L476-477 and L549-552 — 3 and 4 are the invocations that add `(réponse)` terms
Owner: lexicographe
Also in: —

The only invocations that add a `(réponse)` term run after `desc-produit.md` exists, and no sweep runs after that. The rule at L199-201 and L285-287 governs nothing; it only suggests to a reader a loop that does not exist.

### lexicographe.md F11 — `/1_lexique` row 61 launches invocation 4 on an empty file

Verdict: confirmed
Decision: Add to `/1_lexique`'s invocation table the row "another agent's file and a `questions-lexicographe` with no `### Q`" → invoke nothing, say `/2_structure`.
Where: 1_lexique.md L61 ↔ lexicographe.md L105, L515-517
Cited: 1_lexique.md L57 and L59 carry "with no `### Q`" guards, L61 — "Another agent's, and `questions-lexicographe` | **4 — Correcting**" — carries none; lexicographe.md L105 — "runs only when 3 asked something"; L515-517 — "You run only when invocation 3 asked something… an empty questions file ends the turn"
Owner: 1_lexique
Follows: — (the agent already says it; 2_structure.md L95-97 already knows the pair reads as a fourth and files the lexicographe's file first)
Also in: chemins-amont F01 is the same defect — this plan

### lexicographe.md F12 — the `en anglais` line under a `## Relevé` term

Verdict: confirmed
Decision: Define, in the lexicon's shape, the `en anglais` sub-line under a `## Relevé` line, and have invocation 4 carry that line onto the `## Tranché` entry it writes for such a term.
Where: lexicographe.md L163-166, L176-177 ↔ redacteur.md L167-170
Cited: redacteur.md L169-170 — "and on its `## Relevé` line when the term was never questioned: the lexicographe's third invocation reads that line to catch a second English rendering"; lexicographe.md L176-177 — "he writes it on a concept you settled, the first time he renders it"; L163-166 — `## Relevé` shows bare "course — 113" lines and no sub-line
Owner: lexicographe — it owns the file's shape
Follows: redacteur — L167-170 names the two places it writes; once the term is settled, the entry it reads from is the `## Tranché` one ("When the entry already carries one, you take it", L178-179), so the carry-over is what keeps that rule true
Also in: redacteur (passages-amont F02 is the same defect, from the Rédacteur's side)

Invocation 2 needs nothing: it runs before the product file exists, and no `en anglais` line exists yet.

### lexicographe.md F13 — "the vocabulary is the qualifieur's"

Verdict: confirmed
Decision: Name the lexicographe as the vocabulary's owner in the Rédacteur's never-do list.
Where: redacteur.md L318-320 ↔ lexicographe.md L3
Cited: redacteur.md L318-320 — "Write anything in `lexique.md` but an `en anglais` line — never an entry, never a term: the vocabulary is the qualifieur's"; `.claude-new/agents/qualifieur.md` — no occurrence of "vocabul", "lexique" or "lexicographe" (grep)
Owner: redacteur
Also in: redacteur (passages-amont F03 is the same defect)

Nothing changes in `lexicographe.md`.

---

## Report `lexicographe.md`, Part 2 — first-round rows still open

### lexicographe.md A/C3 — "one occurrence of each" against "every occurrence"

Verdict: confirmed
Decision: Align L314-316 with L323-334 — every occurrence, grouped under the meaning read.
Where: lexicographe.md L314-316 ↔ lexicographe.md L323-334
Cited: L314-315 — "the entry shows the two meanings apart — one occurrence of each, with its sentence"; L323-324 — "Every occurrence, grouped under the meaning you read it in"; L378-380 relies on the second — "it can, because the question listed them all, grouped"
Owner: lexicographe
Also in: —

### lexicographe.md A/C15 · B.1 · B.2 — open, not judged

The report lists them `open` with no `Where` and no text; the first-round report is not in this plan's reading list. Not judged here. Wave 2 should take them from the first-round report or drop them.

### D.1–D.10, A/C14(b), A/C14 adjacent, B.3 — spot-checked

Each cited line exists and carries the content the row describes (L402-403, L450-451, L378-383, L431-439, L104, L454-458, L549-550, L202-204, L531-534, L87-89 in the agent; L82-83, L93-95, L246-247 in `1_lexique.md`). Whether each fully answers what the first round asked cannot be judged without that report; nothing seen contradicts the `fixed` status.

---

## Thematic reports, filtered to `lexicographe`

### chemins-amont.md F01 — row 61 without its `### Q` guard

Verdict: confirmed
Decision: Same as lexicographe.md F11 — one defect, one row to add.
Where: 1_lexique.md L61 ↔ lexicographe.md L105
Cited: see F11
Owner: 1_lexique
Also in: lexicographe.md F11, this plan

### chemins-amont.md F02 — `/2_structure` files an answered, unapplied lexicographe file

Verdict: confirmed
Decision: `/2_structure` files the lexicographe's questions file only when it holds no `### Q`; a file holding entries — answered or not — stops the command with `/1_lexique` as the next step.
Where: 2_structure.md L79-87 ↔ 1_lexique.md L189-194
Cited: 2_structure.md L79-83 — "Grep it for an empty `Answer:` before touching it — one hit and you stop… Nothing waiting → file it"; 2_structure.md L89-90 — "A file put away in `questions/lexicographe/` is read by no command"; 1_lexique.md L189-192 — "After 2 or 4, file the lexicographe's questions file it applied, into `questions/lexicographe/`, inside the worktree before the merge"
Owner: 2_structure
Follows: — (1_lexique files only after 2 or 4 and changes nothing; the lexicographe's L115-117 already treats an answered file as a record)
Also in: fichiers.md F17 is the same defect — this plan

A lexicographe file at the root is, by construction, one of three things: waiting (empty `Answer:`), answered and not yet applied (2 or 4 has not run — L189 files it only afterwards), or empty of entries (the loop ended, or 3 asked nothing). Only the third may be filed; the current test lets the second through.

### chemins-amont.md F30 — a resumed run that blocks again is filed away as applied

Verdict: confirmed
Decision: Before filing the named blocking file away, the command tells a block written anew from the one it named — a `## Decision` empty again is a new block: relay it and stop, file nothing.
Where: 1_lexique.md L178-186 ↔ lexicographe.md L72-73, L80, L85
Cited: lexicographe.md L72-73 — "Write a blocking file — `blocked_lexicographe.md`, in the feature folder"; L80 — "Decision | Written empty — the Product Owner answers by hand"; L85 — "A blocked run writes the blocking file and nothing else"; 1_lexique.md L178-181 — "A blocking file you named is filed: git mv …blocked_lexicographe.md …blocked_lexicographe-NN.md"
Owner: 1_lexique
Follows: — (the agent writes the same name; an empty `## Decision` after the run is what tells the two apart, and it already writes it empty)
Also in: the report says "same pattern in every command" — wave 2 should merge this with the same finding in the other plans; it is not specific to the lexicographe

### fichiers.md F17 — `/2_structure` files before `/1_lexique` has applied

Verdict: confirmed
Decision: Same as chemins-amont.md F02.
Where: 2_structure.md L83 ↔ 1_lexique.md L58, L189
Cited: see chemins-amont.md F02; 1_lexique.md L58 — "`questions-lexicographe` alone | **2 — Settling**" is the invocation the file was waiting for
Owner: 2_structure
Also in: chemins-amont.md F02, this plan

### passages-amont.md F02 — `en anglais :` under `## Relevé`, lost at settlement

Verdict: confirmed
Decision: Same as lexicographe.md F12 — define the sub-line in the `## Relevé` shape and carry it onto the `## Tranché` entry invocation 4 writes.
Where: lexicographe.md L181 ↔ redacteur.md L192
Cited: redacteur.md L169-170 (see F12); lexicographe.md L181-184 — "nothing else keeps the English word… invisible to invocation 3, which never opens the product file"
Owner: lexicographe
Follows: redacteur
Also in: lexicographe.md F12, this plan; redacteur

### passages-amont.md F03 — the vocabulary credited to the qualifieur

Verdict: confirmed
Decision: Same as lexicographe.md F13.
Where: redacteur.md L323 ↔ lexicographe.md L181
Cited: see F13
Owner: redacteur
Also in: lexicographe.md F13, this plan; redacteur

The line at passages-amont.md L18 is a "checked and found sound" list, not a finding; nothing to judge.

---

## To settle

None. No entry above turns on intent, scope or user-facing behaviour: F05 and F06 apply a principle the agent file already states (L378-380, L417-420) to the one place each fails to reach; the rest are alignments between two lines of the same chain.
