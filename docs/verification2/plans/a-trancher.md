# À trancher — the `## To settle` sections of the twenty-one plans

Recopied from `docs/verification2/plans/*.md`, one entry per question,
in plan order. `Decision:` is the Product Owner's.

Plans whose `## To settle` holds nothing: `assembleur`, `cadreur`,
`fusionneur`, `lexicographe`, `testeur`, `verificateur`.

---

### arbitre 1 — The twenty-minute wait on the Product Owner

Findings: chemins-aval F11, arbitre.md F10, F11; touches F06.

Question: The Arbitre polls the blocking file for twenty minutes (arbitre.md L439-462), a mechanism `CLAUDE.md` L146 names on purpose — "Only a wait on the Product Owner is polled, and only the `arbitre` does it". It runs inside the `/8_code` worktree, on a file that exists nowhere else and that nobody can point the Product Owner to while the chain is blocked (8_code.md L93-94, L204-206). Whether it stays is a matter of intent.

Options:

**A. Remove the wait.** The Arbitre hands back at once with the line of F17; the caller stops; the orchestrator relays (8_code.md L428-429); the Product Owner answers in `## Decision`; the next `/8_code` applies it (8_code.md L437-439, already written). Costs: `CLAUDE.md` L146 and the Arbitre's description at L3 ("otherwise waits for the Product Owner"), L439-462, L223-224, L178-181 rewritten; `Bash` leaves the tools (F06); detailleur.md L347 and realisateur.md L318 lose "and the Product Owner has not either". The *rule in force that is now wrong* row (L379) then needs a route across two runs: who writes the `architecte/` request once her answer is in the file — the caller that applies it cannot, the Arbitre is not re-invoked on a filled field. Saves twenty minutes per product question.

**B. Keep the wait.** It ends empty every time unless the Product Owner watches the worktree by herself: twenty minutes per product question, per run. F11 then needs its found-answer branch written (apply her answer; for L379, write the `architecte/` request with it and call the Architecte). Whether the uncommitted blocking file even reaches the main checkout after the stop is an `/8_code` matter (L463-466), outside this plan.

Where: arbitre.md L3, L178-181, L223-224, L379, L439-462 ↔ CLAUDE.md L146; 8_code.md L93-94, L204-206, L428-429, L437-439, L463-466; detailleur.md L347; realisateur.md L318

Decision:

---

### architecte F21 — who carries a missing form back to the grid

Question: The grid's R4 (docs-new/process/GRILLE_CONVENTIONS.md L50-52) routes a missing form "as a conventions request in `architecte/`". The Architecte is the agent that answers requests, and no move of it writes one. The grid is the Product Owner's text; the agent cannot amend it (L294).

Options:

| Option | What it costs |
|---|---|
| The Architecte writes `architecte/grille-<n>.md` | A request whose reader is the agent itself; the next invocation 3 would open it and have to refuse it (not a convention). The Product Owner reads it only if a command relays it — none does |
| The Architecte says it in its report | Cheapest; a report is read once and lost (the file's own argument at L594-595 against a report line for a directive) |
| The Architecte raises it in its questions file, a fifth `Kind:` | Reaches the Product Owner through `/conventions` L224; changes the four-word list at L546-547 and every reader of `Kind:` |
| Amend the grid's R4 to one of the above | The grid is the Product Owner's |

Where: docs-new/process/GRILLE_CONVENTIONS.md L50-52 ↔ architecte.md L294, L546-547, L594-595; conventions.md L224

Decision:

---

### architecte chemins-amont F19 — what "back into the loop" means for a `coverage` answer

Question: conventions.md L225 offers "back into the loop, or corrected by hand". architecte.md L646-649 describes the by-hand route only (the behaviour into the product file, `voir produit` in the answer). Neither route carries the behaviour into `spec-technique.md`, which the split is cut from.

Options:

| Option | What it costs |
|---|---|
| Keep "corrected by hand" alone, as L646-649 | The product file gains a block the technical document never sees; the conventions get no rule and no lot builds it — the gap the question found stays open in the code |
| Re-run the upstream loop from the block the Product Owner adds (`/3_decoupe` onward, through `/6_convertit`) | A full upstream turn per coverage question; `spec-technique.md` rebuilt, `couverture.md` then stale (see fichiers.md F03) |
| Let the Rédacteur integrate the answered `questions-architecte` file | The file also holds `conjunction`, `inconsistency` and `precision` answers, which are not product; and once filed under `questions/architecte/` the Architecte never reads them |

The guard (1_lexique and 2_structure never take the file as the answered one) is decided above and does not depend on this.

Where: conventions.md L225 ↔ architecte.md L646-649

Decision:

---

### classeur renommages F10 — the `/2_structure` table when a filled `blocked_classeur.md` and an answered questions file sit at the root together

Question: Met while building `renommages.md` F10; not in `decisions.md`. The relay of `/3b_nature` (L235) sends the Product Owner to fill the decision, answer the questions, then `/1_lexique` and `/2_structure` — at which point the table at 2_structure.md L117-125 has row L120 (the blocking file) above row L124 (the questions file): the Rédacteur is handed the blocking file, the answered questions file stays at the root beside the Rédacteur's own new one, and the next command stops on "more than one" (L125). Pre-existing, and not the classeur's to settle.

Options:

| Option | Cost |
|---|---|
| The Rédacteur takes both in one invocation — the blocking file and the questions file | One more input to its invocation 2; its rule "never a second questions file" (L527-528) has to admit a blocking file beside the questions file |
| Two runs of `/2_structure`, the blocking file first, and the relay says so | A run whose only output is a rewrite; the questions file waits one command longer; row L125 has to tolerate the Rédacteur's fresh file beside the waiting one |
| The relay orders the questions before the decision, so the two never meet at the root | The blocked block is asked about a turn later; no command change, but the `/3b_nature` relay row L235 reverses its order |

Where: 3b_nature.md L235 ↔ 2_structure.md L117-125; redacteur.md L527-528

Decision:

---

### commandes chemins-amont F16 — The `<<ASSUMED` mark of a nature whose product answer changed no block

Question: `decisions.md` settles chemins-amont.md F16 as an outcome — the nature does not run, its part stays, the document stands. ⚠️ **It says nothing of the mark the section still carries.** The Convertisseur marks an entry waiting on a product answer with `<<ASSUMED B40: …>>` (convertisseur.md L464-466), the mark "is lifted by writing the section again" (L468-470), and the Cadreur stops on the first one (convertisseur.md L32, passages-amont.md F05). So the document the decision calls *standing* still stops `/7_lots`.

Options: Three ways out, none this plan's to pick:

| Option | What it costs |
|---|---|
| The command reruns the nature to lift the mark, part unchanged | One opus invocation for a known result — exactly the cost 6_convertit.md L132 refuses; and the agent, reading the same blocks, may write the same mark again |
| The command lifts the mark by script, keeping the assumed line | The assumption stands as a rule nobody validated — the answer said *the blocks are right as they are*, which is not the same as *the assumed line is right* |
| The Convertisseur writes no `<<ASSUMED` for a product question — the pending block is visible in the questions file alone | The Cadreur loses the inline signal that an entry waits; `<<ASSUMED` becomes technical-only, and convertisseur.md L388-390 ("one mark, not two") is reversed |

The F16 entry above applies what `decisions.md` settled and stops here; the Owner of this question is whoever the Product Owner names, across `6_convertit`, `convertisseur` and `cadreur`.

Where: convertisseur.md L32, L388-390, L464-466, L468-470 ↔ 6_convertit.md L132; decisions.md (chemins-amont.md F16)

Decision:

---

### concepteur renommages F16 — A symbol that depends on nothing, in a lot of only-new files

Question: renommages F16 gives the fallback "the module of the one it depends on most". A symbol with no dependency at all — a root type, a constant holder — has none.

Options:

| Option | Cost |
|---|---|
| Place it in the module the lot's other symbols land in, and say so | Cheapest; wrong for a lot whose every symbol is placeless — the request to the Architecte still goes, so the rule arrives at the end of the lot |
| Block on it | A blocking file to the Product Owner for a placement the Architecte settles at move 7 anyway |

Where: concepteur.md ↔ decisions.md (renommages F16)

Decision:

---

### concepteur chemins-aval F09 — The declarations of a re-cut lot, already in the code

Question: chemins-aval F09 deletes the re-cut lot's `conception.md`; its declarations were committed (concepteur.md L237, realisateur.md L335-337) and stay in the code. The Concepteur of the new lot meets symbols already declared — under old signatures.

Options:

| Option | Cost |
|---|---|
| The orchestration reverts the re-cut lots' commits before `/7_lots` | Git surgery in the command; clean code for the new split |
| The new lot's Concepteur edits what it finds, the old declaration counted as its own | Its L162-165 rule ("declare only what is missing") would have to read a stale declaration as one to rewrite, the opposite of what it says |
| Leave them; the Relecteur's `## Outside the lot` catches what nobody owns | The stale declarations belong to no lot and no sheet; the Vérificateur's "no `PASS`" reading is untouched but the code carries symbols no sheet promises |

Where: concepteur.md L162-165, L237 ↔ realisateur.md L335-337

Decision:

---

### concepteur — How the orchestration finds "the lot's first commit"

Question: 8_code L124-125 diffs from "the lot's first commit"; relecteur L390 from "the concepteur's commit"; no file prescribes a commit message that names the lot, and the Concepteur's shell (L94) allows `git commit` with no wording rule. Not a finding of this round.

Options:

| Option | Cost |
|---|---|
| A commit-message rule for the three committing agents (`<lot>: …`) | One line in three agent files; the orchestration greps `git log` for it — a Bash gesture 8_code does not list today |
| The orchestration notes the `HEAD` sha before invoking the concepteur, per lot | No agent change; the sha lives in the run's memory and a run restarted mid-lot loses it — the same trap 8_code L153-157 names for `## Attempts` |

Where: 8_code.md L124-125, L153-157 ↔ relecteur.md L390; concepteur.md L94

Decision:

---

### controleur F12 — What names, on a correction cycle, the block a lot built

Question: `decisions.md` settles that those blocks are marked `carried`. It does not say where phase 1 finds them, and no bugfix file names a product block: `bug-list.md` is free form (diagnostiqueur.md L51 — "**Free form** — a sentence naming what is wrong, and what it should be"), a `desc-bug.md` entry carries a `Bearer:` that is a code symbol (diagnostiqueur.md L254 — "Whatever answers it is the bearer, whatever its form"), and the bugfix folder has no `tracabilite.md`. The Contrôleur's own report is the one file of the chain that names blocks and feeds a bug list (9_controle.md L345-346).

Options:

| Option | What it costs |
|---|---|
| **a.** The bug list carries the `B<n>` of the report line it comes from, and the diagnosis carries it through to `desc-bug.md` and the lot list | One field on three files the Product Owner and two agents write — the join exists by construction; a gap she adds from use, with no block, stays unmarked |
| **b.** Phase 1 greps the bugfix sheets for `B<n>` | Nothing to add, but the Détailleur is not told to write the block id in a sheet, so the grep finds what happens to be there |
| **c.** Phase 1 marks `carried` every block the latest report listed as missing, when a later `bugfix-NN/` exists | Nothing to add, but a gap set aside at diagnosis (decisions.md L91-97) is marked built when it was not — the very case the decision forbids |

(turns on what a correction cycle's files carry, and on who writes it)

Where: diagnostiqueur.md L51, L254 ↔ 9_controle.md L345-346; decisions.md L91-97

Decision:

---

### controleur F02 — Whether the two "never this file" lines of L66-71 were kept on purpose

Question: The pass asked for their removal; the index records neither the pass nor a refusal.

Options: The plan decides to finish the pass (F02); if the Product Owner kept them deliberately, the index says "écarté" and F02 becomes a record entry only. Cost either way: two lines.

The plan writes: finish the pass, unless the Product Owner says otherwise — see F02.

Where: controleur.md L66-71

Decision:

---

### convertisseur 1 — Who reads `par-genre/transverses.md`

Findings: F02, F19, passages-amont F07; F10, F11, D-16 depend on it.

Question: 🔴 **The demand (modifications.md L547) says every nature invocation; the file (convertisseur.md L146-147) says invocation 2 alone, and `/5_reclasse` L102 still says every nature.** The correction between rounds chose the file's route on two grounds (L149-153): a transverse block carries an empty `Nature:` line, so a nature invocation would have to derive one; and eight invocations would write the same constraint eight times.

⚠️ **The first ground does not hold as stated**: invocation 2 places the code half *« in the section of its layer »* (L178-179), which is the same derivation, made by an invocation that has no blocks in front of it. The second ground is real.

Options:

| Route | What it costs |
|---|---|
| **A — every nature invocation reads it** (the demand) | Each nature writes the transverse entries of its layer with its own numbering and its own `## Trace` line — F10 and F11 dissolve, D-16 becomes a re-sourcing. ⚠️ Each nature has to judge which transverse rules are its layer's: two natures can both claim one, or none; the constraint half needs one writer (invocation 2, from the file) or it is written up to eight times. Eight opus contexts each load the file. |
| **B — invocation 2 alone** (the file as written) | One reader, one writer of the constraint half. ⚠️ Invocation 2 numbers entries in sections it did not write (F07), derives their layer blind, and needs the record F10 and F11 add so that references to a transverse block resolve and `tracabilite.md` stays complete. The index row and `/5_reclasse` L102 must be corrected to say so (F02, F19). |

📌 **Whichever route is chosen**, F02, F19 and passages-amont F07 get their decision from it; F10, F11 and D-16 stand as written under B and are voided or re-shaped under A.

Where: docs/refonte/modifications.md L547 ↔ convertisseur.md L146-147, L149-153, L178-179; 5_reclasse.md L102

Decision:

---

### convertisseur 2 — Where a leftover `[B<n>: …]` is caught — decided above, flagged here

Question: F22 decides the Cadreur greps `[B`. 📌 **The alternative** — invocation 2 turning a leftover bracket into an `<<ASSUMED` mark — keeps the Cadreur's grep as it is but loses the reference's expectation text, which is what resolves it later (L292-294). Not a product matter; the decision is taken, and the cadreur plan may take the other side — flagged so the merge sees both.

Options: F22's decision (the Cadreur greps `[B`) — or the alternative above, at the cost of the reference's expectation text (L292-294).

Where: convertisseur.md L292-294 ↔ cadreur.md (F22, passages-amont F05)

Decision:

---

### decoupeur F01 — the `Clarification needed` stop: restore it, or record its removal

Question: The refonte kept the stop in the agent (index L318: the command greps the whole file, the agent its blocks — "si la commande change, l'agent tient encore"). Round 1 found its only outcome was a reply the file itself says gets lost (D-4), and the correction removed it. The two records now disagree, and the choice is scope: does the agent carry a guard of its own against a `Clarification needed` line, or does it rely on the command's grep (`3_decoupe.md` L44-47)?

Options:

| Option | What it costs |
|---|---|
| **A — restore the stop, with a blocking file as its outcome** | A second blocking cause in a file built around one (L135-137, round 1 D-10); a `To resume` that routes to `/2_structure` like the first; the command's relay row already covers a blocking file (L215), so no new row. The guard holds if a command ever drops its grep. |
| **B — record the removal** | An index line to amend in `docs/refonte/modifications.md`, outside this campaign's perimeter. The agent has no guard of its own; a `Clarification needed` line reaches it only if the command's grep is dropped, and would then go unsplit to the qualifieur. |

Where: docs/refonte/modifications.md L318 ↔ decoupeur.md L135-137; 3_decoupe.md L44-47, L215

Decision:

---

### decoupeur F17 — who merges two blocks

Question: The decoupeur reports a block whose only trigger is another block's sequel (L92-96, L248-249) and may not merge (L110); the qualifieur and the classeur name the decoupeur as the merger (settled above: they stop doing so). After F13 the signal reaches the Product Owner. Who acts on it is a question of chain scope.

Options:

| Option | What it costs |
|---|---|
| **A — the Rédacteur merges, on a Product Owner decision** | A route: the relayed identifiers become a decision the Rédacteur applies as a rewrite (it already rewrites on a filled `## Decision`, redacteur.md L527-540); the merged block carries `MODIFIED`, the retired number is a reference to redirect. Fits the Rédacteur's role as the only writer of the product file. |
| **B — nobody merges; the double probe is accepted** | Zero text beyond F13's relay row and F17's rewording. The grid probes one behaviour twice, and the two blocks' answers can diverge; the sondeur has no rule for that. |

Where: decoupeur.md L92-96, L110, L248-249 ↔ redacteur.md L527-540; qualifieur.md L214; classeur.md L181

Decision:

---

### detailleur F21 — The declarations and tests committed against a sheet the review found false

Question: F21 sends a `Cause: sheet` lot back to the Détailleur. By then the Concepteur has committed declarations "exactly the signature the sheet gives" (concepteur.md L200-201) and the Testeur one test per criterion — both against the false sheet, both in the code. `plans/concepteur.md` raises the same question for a re-cut lot ("The declarations of a re-cut lot, already in the code"); the answer should be one.

Options:

| Option | Cost |
|---|---|
| The orchestration deletes `conception.md` and `tests.md` and reverts the lot's commits before re-invoking | Git surgery in `8_code`; the three agents rerun from clean code |
| The orchestration deletes the two reports only; the Concepteur and the Testeur rewrite what they find | Their "declare only what is missing" rules must read a stale declaration as one to rewrite — the opposite of what they say |
| The Détailleur rewrites the sheet against the declarations as committed (divergence-style), not from the entries | Cheapest; wrong by construction — the declarations are what the false sheet produced |

Where: detailleur.md (F21) ↔ concepteur.md L200-201; testeur.md

Decision:

---

### diagnostiqueur F10 — the state document is read, and nothing follows

Verdict: confirmed
Where: diagnostiqueur.md L138 ↔ L238-246
Cited: L138 — "`docs/CURRENT_TECHNICAL_STATE.md` — 📌 its `## Traps — general` and `## Dead state` sections, to see whether the gap is a trap already recorded"; L238-246 — the verdict table has five rows, none on a recorded trap; moves 1 to 5 (L205-377) never name the state document.
Owner: diagnostiqueur

Question: The previous round's D-16 gave the input a purpose and left the outcome unwritten; what the Product Owner wants from that reading is not in any file this plan read.

Options: Three options, with what each costs:

| Option | What it costs |
|---|---|
| **Drop the input** — invocation 1 reads the conventions and the code only | A gap the state document already records as a trap or as dead state is investigated from nothing; the Détailleur reads the state document later in any case. F04 becomes moot. |
| **Keep it as a search aid** — a recorded trap or dead symbol is named in `## Today` (and, for dead state, feeds move 3's bearer search); the verdict is unchanged | A reach gesture (F04) and one line under `## Today`; the cheapest outcome that uses the reading. |
| **Keep it as a verdict input** — a gap recorded as a trap is `set aside` with the state document as its reason | Wrong on its face: a recorded trap is a known pitfall, not a fix; the gap stands regardless. Listed only because it is the reading L138's wording invites. |

F04's decision applies only under the second option.

Where: diagnostiqueur.md L138 ↔ L205-377, L238-246

Decision:

---

### qualifieur 1 — A *transverse-or-behaviour* doubt — silent, or a question (F12, F01, F05)

Question: The file settles every genre doubt as `comportement` without a question (L140-141), and the report's part 2 records that the earlier "you still raise it as a question" rule was removed on purpose (D3: "doubt 1 is now silent"). F12 shows the price given for that silence is false for one genre: a `transverse` filed `comportement` is absent from the list `/4_grille` hands the sondeurs (4_grille.md L139-140), so the rule is not beside them and every block it reaches raises the gap as a question the Product Owner answers by hand, once per block.

Options:

| Option | What it costs |
|---|---|
| **Keep the silence as it is** — any doubt → `comportement` | A `transverse` in doubt is probed as a behaviour, and its rule is asked of the Product Owner on every block it reaches; with F13 relayed she sees the per-block genre list and can catch it, by hand, before `/3b_nature` |
| **Ask on the `transverse` doubt only** — the four other doubts stay silent | One question per such doubt, answered before `/3b_nature`; the *dozens of questions* D3 feared came from asking on every doubt, and the `transverse` doubt is the one whose silent side is not cheap |
| **Default the doubt to `transverse`** | Never — a behaviour filed `transverse` is not probed (4_grille.md L142), the silent hole L145-147 names |

The plan stops here for F12's policy; its price statement is corrected whichever option is taken.

Where: qualifieur.md L140-141, L145-147 ↔ 4_grille.md L139-140, L142

Decision:

---

### qualifieur 2 — A two-genre block — how it gets back to the decoupeur (F14, F06, F02)

Question: The qualifieur reports a block whose sentences call for two genres, and gives it the majority genre meanwhile (L88-91). Nothing sends it back: `/3a_genre` has no *next* row for that report (L227-235), `/3_decoupe` looks only at `NEW` and `MODIFIED` blocks (3_decoupe.md L81-82), and the qualifieur may not set a marker (L209). The decoupeur does own the split (decoupeur.md L65-67).

Options:

| Option | What it costs |
|---|---|
| **The qualifieur blocks on it** — `blocked_qualifieur.md`, decision, `/2_structure` names it to the Rédacteur, who rewrites with `MODIFIED`, then `/3_decoupe` splits | One Product Owner round-trip per such block; consistent with 2_structure.md L120 ("all three block on something only a rewrite of the block settles") and with F11's route; the majority rule (L88-91) and F06 go away |
| **Keep the majority genre and the report, add a relay row** | The Product Owner learns of it and nothing runs; the block is coded under one genre with a constraint inside it — the outcome decoupeur.md L66-67 names as the reason the split exists; F06's rule then has to stand |
| **A `/3a_genre` next row that runs `/3_decoupe` on the named blocks** | `/3_decoupe` needs a way to take a block list it does not grep for — a new parameter on a command that today takes a feature name only; the qualifieur's report becomes the command's input |

The plan stops here for F14; F06's decision holds only under the second or third option.

Where: qualifieur.md L88-91, L209 ↔ 3a_genre.md L227-235; 3_decoupe.md L81-82; decoupeur.md L65-67; 2_structure.md L120

Decision:

---

### realisateur F11 — what the reprise leaves in the tree

Verdict: confirmed
Cited: realisateur.md L385-386 — "📌 **Commit what compiles before you stop** — 🔴 **never commit what does not.** ⚠️ **Say in `En chantier` what you left uncommitted.**"
Cited: realisateur.md L475 — "- 🔴 **Leave a dirty working tree behind you**, whatever the reason"
Cited: 8_code.md L463-466 — "⚠️ **A worktree with uncommitted files refuses a plain remove** — 🔴 **never force it**: 📌 **say what is left there, and stop.** ⚠️ **An agent handed back leaving work uncommitted is a fault of that agent**"
Cited: passes/realisateur.md C3 — "Either the half-written piece is committed on the lot, flagged in `En chantier` as not compiling, or it is removed before the commit and `En chantier` says what was undone — I lean to the first, since the whole point of the reprise is not to redo it."
Owner: realisateur
Follows: 8_code (its removal step, either way)

Question: The three lines cannot all hold. The next run opens a fresh worktree from `HEAD`, so uncommitted code is unreachable to it whatever `En chantier` says — the only choice is between the two options the comment sheet names.

Options:

| Option | What it costs |
|---|---|
| **Commit the half-written piece, flagged in `En chantier` as not compiling** — the reviewer's lean | `HEAD` no longer compiles: the next lot's Concepteur, in its own worktree, cannot compile its declarations (8_code.md L112: *"Writes the declarations with empty bodies and compiles"*), and the Testeur's older tests cannot run. Every lot after the block is stopped until the Product Owner answers. |
| **`git restore` the non-compiling piece before stopping; `En chantier` says what was written and undone, and where** | The half-written code is lost; the next run redoes it from a description. `HEAD` compiles, the worktree is clean, L475 and the command's removal step hold as written. |

The second option is consistent with every 🔴 rule now in force (L385 *never commit what does not compile*, L475, 8_code L463-466) and with the Concepteur's and Testeur's commits, which always compile. The first is the reviewer's explicit lean and buys the work back at the cost of a `HEAD` that no lot after it can build on. The choice is the Product Owner's; the plan stops here on it, and F13's `En chantier` handling follows whichever is chosen.

Where: realisateur.md L385-386 ↔ realisateur.md L475; 8_code.md L112, L463-466; docs/refonte/passes/realisateur.md C3

Decision:

---

### realisateur chemins-aval F08 — the dropped lot's declarations and tests stay committed

Verdict: confirmed
Cited: realisateur.md L335-338 — "🔴 **Drop what you wrote** — 📌 **`git restore` on the files you edited.** ⚠️ **Nothing you wrote is a new file**: the concepteur committed the declarations, the testeur the tests"
Cited: testeur.md L231 — "| **Anything else** | 🔴 **A block** — 📌 **the declarations broke something the sheet does not touch** |"
Owner: 8_code (the re-split handling)
Follows: realisateur (no change either way — its restore covers its own edits), concepteur, testeur

Question: The Réalisateur's part is right as written: it can only restore what it edited. What stays is the Concepteur's throwing declarations and the Testeur's red tests of a lot that no longer exists, and the next lot's Testeur blocks on them.

Options: Three ways out, none this plan's to pick:

| Option | What it costs |
|---|---|
| **The orchestration reverts the dropped lot's commits** (`git revert` of the Concepteur's and Testeur's commits) before `/7_lots` | The orchestrator's Bash is for git and this is git; but a revert of a mid-history commit can conflict with the lots coded after it in the same run, and the orchestrator does not resolve conflicts. |
| **The re-cut lot's Concepteur removes the declarations and tests the old lot left**, from the old `conception.md` and `tests.md` (chemins-aval F09 deletes them — they would have to survive as an input instead) | The Concepteur gains a delete gesture it does not have today, and a reading of files from a lot that is not its. |
| **The Testeur's *older test fails* row gains an exception** for tests of a lot the split dropped | Red tests and throwing bodies stay in the tree indefinitely; every later Testeur has to know the list of dropped lots. |

The first is the cheapest in rules and the riskiest in git; the choice sits with the commandes plan and the Product Owner.

Where: realisateur.md L335-338 ↔ testeur.md L228-232; 8_code.md L357-366

Decision:

---

### redacteur F19 — a block created at invocation 3, and its `Nature:`

Question: A subject no title covers, brought by a decisions file at invocation 3, becomes a block with an empty `Nature:` (L455, L703-705); no classeur runs after `/fusion`, and the fusionneur keeps `Nature:` lines in the global (fusionneur.md L386-387).

Options:

| Option | Cost |
|---|---|
| The redacteur creates no block at invocation 3 — a decision with no block to land in goes to `blocked_redacteur.md` (D.4's route) | A `/fusion` stop for every such decision; the Product Owner names the block |
| The block enters the global with an empty `Nature:` | The global carries a block with no nature, for whoever reads that line there |
| The fusionneur drops an empty `Nature:` line at merge | A fusionneur rule; the global then carries blocks with and without the line |

Where: redacteur.md L455, L703-705 ↔ fusionneur.md L386-387

Decision:

---

### redacteur F01 — the residual gap the `## Relevé` clause aimed at

Question: With the line on `## Tranché` alone, a term never questioned — present in `## Relevé` only — rendered in English by the redacteur has no recorded rendering; the lexicographe's compare (lexicographe.md L464-466) cannot catch a second English rendering brought by a later answer. The index asked for `## Tranché` alone, and this plan applies it; whether the gap is worth a lexicographe change is not this plan's.

Options:

| Option | Cost |
|---|---|
| Leave it — `## Tranché` alone, as the index asks | A second English rendering of an unquestioned term goes uncaught |
| The lexicographe defines a sub-line under `## Relevé` and preserves it across rebuilds | A lexicographe change on two rules (L162-166 shape, L285-287 rebuild); the redacteur then writes there too |

Where: redacteur.md (F01) ↔ lexicographe.md L162-166, L285-287, L464-466

Decision:

---

### relecteur F19 — The route of `Cause: sheet` (relecteur.md F19 · passages-aval.md F02 · chemins-aval.md F03)

Question: The promise is the relecteur's (L167-169: the block goes back to the Détailleur, never to a fresh Réalisateur) and the first round asked for it (C14, D-5); nothing carries it. Three shapes, none of them the relecteur's to pick — each puts a mode on a different agent and decides what a wrong sheet costs.

Options:

| Option | What it takes | What it costs |
|---|---|---|
| **A — delete and re-detail** | `/8_code` deletes the lot's `fiche-executable.md`, `conception.md` and `tests.md` on `Cause: sheet` and runs the Détailleur on the block in its ordinary mode, which writes the missing sheet (move 1) | The Détailleur reads no verdict (detailleur.md L672-673) and rewrites from the same entries — it can reproduce the defect; the declarations and tests the lot already put in the worktree stay there, and the Concepteur "declares only what is missing" (concepteur.md L163-164) against a sheet that changed |
| **B — a third Détailleur mode** | `Mode: sheet` on one lot, fed the verdict's `## Findings`, rewriting that sheet from the entries; `/8_code` then invalidates `conception.md` and `tests.md` | A new mode in the Détailleur and a new prompt in `/8_code`; the same leftover code as A; and whether `## Attempts` restarts on the rewritten sheet has to be said |
| **C — stop on the Product Owner** | `Cause: sheet` is relayed like an "anything else" block (8_code.md L422); the relecteur's L167-169 is rewritten to say the orchestration stops | Every wrong sheet costs a human round trip; no new mechanism, and no agent rewrites a sheet nobody has judged |

Whichever is chosen, realisateur.md L519-520 (two rows, no `sheet`) and relecteur.md L167-169, L407 follow it.

Where: relecteur.md L167-169, L407 ↔ detailleur.md L672-673; concepteur.md L163-164; 8_code.md L422; realisateur.md L519-520

Decision:

---

### relecteur F12 — Who reads a reservation

Question: `decisions.md` keeps `PASS with reservation` and settles that it counts as coded. The entry above gives the note a place (`## Findings`); nobody is named to read it, and `/8_code` L200-201 says it never reads `## Findings`.

Options:

| Option | What it costs |
|---|---|
| **Keep the row, no reader** | The note is written for nothing — the pass sheet's ### 10 (passes/relecteur.md L328-335) named exactly that |
| **Give it a reader** — the Détailleur of the next block, or the Contrôleur at `/9_controle` | A new input on that reader, and a rule on what a reservation changes for it |
| **Drop the row** | Reopens the premise of a settled question — the Product Owner's, not this plan's |

Where: relecteur.md (F12) ↔ 8_code.md L200-201; docs/refonte/passes/relecteur.md L328-335

Decision:

---

### sondeur 1 — The *défaut*'s second ground — « a pattern the file already follows » (F02, F09)

Question: The refonte's §3 (modifications.md L395) and its grid (docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md L38-41) give a *défaut* two grounds: a transverse rule, or a pattern the file already follows. The agent (sondeur.md L398-400) keeps the first and forbids the second, with a reason: a pass A question « stands on its block alone » (L332-333, L399-400), and under the C22 reading rule an angle reads only the blocks the prompt names (L43, L63-65) — on a later turn, the blocks that follow the pattern are ones it may not open. One sondeur reads the grid whole (L44) and the other rule is in its own file; the merge cannot tell the two forms apart.

This is a process-design choice on which questions the Product Owner answers by hand and which she accepts by silence; it is not decided here.

Options:

| Option | What changes | What it costs |
|---|---|---|
| (a) Transverse rule only — align the grid L38-41 and §3 to the agent | `docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md` L38-41 (and modifications.md L395, as record) | A gap a same-file pattern would have grounded becomes an obligatory question: more lines for the Product Owner to write. It is the only option consistent with the C22 reading as applied (an angle cannot see the pattern's blocks) |
| (b) Both grounds — restore the pattern in the agent | sondeur.md L398-400, L306 (the two-row table), L394-396 | Contradicts L63-65 and L332-333; an angle on a later turn cannot read the blocks that carry the pattern, so only the global could ground it — and the global does not run pass A (L169, L219-220). Would need the reading rules reopened |

Related, same lines, not blocking: §3 (modifications.md L397-398) asks for « la référence du paragraphe qui la fonde »; the agent quotes the words (L391, L394-395). Report Part 2 A-§3 (b) records it as `other`. Whichever option wins, say which of the two forms the `Défaut:` line carries.

Where: docs/refonte/modifications.md L395, L397-398; docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md L38-41 ↔ sondeur.md L43-44, L63-65, L169, L219-220, L306, L332-333, L391, L394-396, L398-400
