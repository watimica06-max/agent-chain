# agent-fusionneur — verification

**Read**: `.claude/agents/fusionneur.md` (old, 489 lines) · `.claude-new/agents/fusionneur.md`
(new, 504 lines) · `docs/refonte/passes/fusionneur.md` — **does not exist** (the section says
so: *"Pas de fiche de passe — l'analyse ne l'a pas atteint, comme l'Arbitre"*) ·
`docs/refonte/modifications.md` § `` # `fusionneur.md` `` (lines 804–843).

**What the section says**: two structural modifications on the agent, one on the command,
no pass sheet. "Ce qui a changé": (1) its source is `desc-produit-fusion.md`, never
`desc-produit.md`; (2) at `INSERT`, it checks that the section title still covers what the
section holds — otherwise a question, only on the sections it touches; (3)
`commands/fusion.md` gets a row 10: `desc-produit-fusion.md` absent → Rédacteur, invocation 3,
with the cycle order and the faithful copy when there is no decision. "La demande" spells
out (1) and (2) only.

Since no pass sheet exists, section A covers the three structural modifications only.
B, C and D are given full attention, as instructed. Line numbers are those of the **new**
file unless marked *old* or *cmd* (`.claude-new/commands/fusion.md`).

Cross-file facts used below, all read from `.claude-new/`: the Rédacteur's invocation 3
(`redacteur.md` 618–670) writes `desc-produit-fusion.md` as a copy of `desc-produit.md` with
the `code/decisions-produit.md` files folded in and **every marker stripped**; the Rédacteur's
block shape (`redacteur.md` 57–62) is `### B7 — title  MODIFIED` / `Genre:` / `Nature:` /
`Global: ## <section>`; `CLAUDE.md` no longer lists an `extracteur` agent nor an `/extrait`
command.

---

## A. Conformity

No pass sheet: no PASSÉ / ÉCARTÉ / REPORTÉ comment to verify. The three rows of
"Ce qui a changé" are verified against "La demande".

| # | Expected (La demande) | Found | Verdict |
|---|---|---|---|
| M1 — source | *"Une ligne : sa source devient `desc-produit-fusion.md` au lieu de `desc-produit.md`"* | Line 45: `| the product file | 🔴 **desc-produit-fusion.md** — ⚠️ **never desc-produit.md** |`. Every other mention in the file says "the product file" (31, 222, 249, 299, 377, 411) and resolves through the table. No stray `desc-produit.md` remains. | **Conforming** — one line, as asked, with a prohibition the demande did not ask for but that does not contradict it |
| M2 — title check at `INSERT` | When it adds a block to an existing section of the global, it looks whether the title still covers what the section holds; otherwise a question to the Product Owner (renaming is a product decision). Why: the global is read by its index only, a drifted title is a section the Rédacteur never opens, duplicate at the next merge, the defect grows alone. Only on the sections it touches. | Lines 155–169, new sub-part *"When you `INSERT` into a section that exists"*: the check (157–160), the question (159–160), the reason in the demande's own words (162–166), the scope *"Only the sections you touch — you never audit the others"* (168). | **Conforming on the text.** But the rule is placed under *Where questions files live* / the merge-plan shape (Part 1), and nothing says at which invocation it fires nor what the plan records while the question is open — see **D-2, D-3**. It also contradicts the count at line 352 — see **D-1** |
| M3 — `commands/fusion.md` row 10 | A row 10: `desc-produit-fusion.md` absent → Rédacteur, invocation 3; with the cycle order and the faithful copy when there is no decision | cmd 49: `| 10 | 🔴 **desc-produit-fusion.md absent** | **Rédacteur, invocation 3 — Merging** |`; old row 10 becomes row 11 (cmd 50). cmd 58–70: runs once before the merge; names every `code/decisions-produit.md` in cycle order, feature first then `bugfix-01`, `bugfix-02`, later cycle wins; no decisions file → faithful copy. | **Conforming.** Two lines of the command were not updated with it: cmd 9 still says *"chains three phases"* (now four), and cmd 56 *"A feature with no bug-fix cycle goes straight to row 10"* now points at the Rédacteur, not at the merge it used to mean — see **D-9** |

Nothing listed ÉCARTÉ or REPORTÉ.

---

## B. Unannounced changes

The diff old → new has exactly three hunks. Two are M1 and M2. The third:

| # | Line | Old | New | What it changes | Severity |
|---|---|---|---|---|---|
| B-1 | 379–380 (old 364–365) | *"📌 **The `Nature:` lines stay**: the global carries them, as the Extracteur writes them."* | *"📌 **The `Nature:` lines stay**: the global carries them."* | Drops the reference to the Extracteur. Not in the fusionneur section of `modifications.md`; it follows from a decision recorded elsewhere in that file (line 1569, § *Les documents de process*: *"L'Extracteur est cité et il est supprimé — le global naît maintenant du Fusionneur"*), and the new `CLAUDE.md` no longer lists the agent nor `/extrait`. Consistent with the chain, unannounced for this file. | **NOTE** |

No renumbering, no moved section, no rewritten table beyond the two announced ones. The
frontmatter (lines 1–7) is byte-identical, description included — see **D-4**.

---

## C. Gestures against tools

**Frontmatter tools** (line 4): `Read, Grep, Glob, Edit, Write`. No `Bash`.

### Gestures and their means

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Grep the global's `^#` index, load only the sections needed | 71–72, 253–254 | Grep + Read | has the means |
| Read the product file, the plan, its own questions file, every `bugfix-*/bug-list.md`, the settled `blocked_fusionneur-NN.md` | 249–251, 371–374, 474, 267–269 | Read | has the means |
| Find `blocked_fusionneur.md`, the highest `questions-fusionneur-NN.md` at root or in `questions/fusionneur/`, every `bugfix-*/` folder | 93–94, 267, 374, 474 | Glob | has the means |
| Write `plan-fusion.md`, the questions file, `rapport-fusion.md`, `blocked_fusionneur.md` | 122, 362, 421, 184 | Write | has the means |
| Targeted edits in the global — `REPLACE` / `INSERT` / `DELETE`, never a full rewrite | 389, 402 | Edit — with the *When `Edit` fails* recipe at 233–239 | has the means |
| On `INIT`, copy the product file under `# Application` | 377 | Read + Edit/Write (the global is then one line, so a full write is legitimate) | has the means |
| **Rename** `blocked_fusionneur.md` → `blocked_fusionneur-NN.md`, *"`git mv`, or the equivalent: one file, under a new name … never … a copy, not a note, not an empty file"* | 275–283 | **none** — no `Bash`, no delete/move tool. With `Write` it can create the numbered file; it cannot remove the unnumbered one, and overwriting it with nothing is exactly what 278–280 forbids. Line 282–283 then says the leftover *"reads as a block still standing, and the next run treats it as one"* — the agent is told that its only possible outcome is a standing block. | **BLOCKING** |

### Tools no gesture uses

None. `Read`, `Grep`, `Glob`, `Edit`, `Write` are each required by at least one gesture above.

---

## D. Internal coherence (new file alone)

| # | Line | Quote | Finding | Severity |
|---|---|---|---|---|
| D-1 | 352 vs 157–160 | 352: *"**One case calls for a question**: a rule in the existing block with no match at all in the new one."* — 157–160: *"a question for the Product Owner: renaming a section of the global is a product decision."* | Announced count no longer matches: since M2 there are two cases that call for a question. Line 350 *"You apply without asking in every case above"* still holds; 352 is the line to fix. | **TO FIX** |
| D-2 | 155–160 vs 247–251 | 155: *"When you `INSERT` into a section that exists"* … 159: *"a question for the Product Owner"* — 250: invocation 2's output is *"The updated global · the merge report"*, no questions file. | The check has no invocation. If it fires when the `INSERT` line is written (invocation 1), the plan needs a verb for it and none of the five (141) covers "inserted, title under question"; if it fires when the `INSERT` is applied (invocation 2), that invocation lists no questions file among its outputs. Either way the branch leads nowhere. Same gap already existed for 399–400 (*"it goes back as a new question"* at invocation 2) — M2 makes it load-bearing. | **TO FIX** |
| D-3 | 155–169 vs 132, 137, 152 | 155: *"the new block included"* — 132: `- INSERT: "Tapping it opens the activity entry screen."` (a sentence) — 137/152: `[new section]`, *"A new section is marked as such"*. | *`INSERT`* is used in two senses: in the plan it is a sentence-level verb; in M2 it is the insertion of a whole block into an existing section. The plan marks a new section but has no mark for a new block inside an existing section, so invocation 2 cannot tell from the plan when the title check is due. | **TO FIX** |
| D-4 | 3 vs 247–251, 460 | 3: *"Two invocations, separated by a question round-trip."* — 247–251: three rows; 460: *"## INVOCATION 3 — Bug-fix decisions"*. | Announced count does not match. Pre-existing (old line 3 identical), still true of the new file. | **TO FIX** |
| D-5 | 29–32 vs 462 | 29–32: *"**Last**, once the conversion has come through with no signal: `Rédacteur → product file → conversion → questions file fully answered → merge`"* — 462: *"Once per feature, after every bug-fix cycle has been coded."* | Two statements of when it runs. The chain at 31–32 stops at the conversion; 462 and the source at 45 (a file the Rédacteur writes *after* every correction cycle, `redacteur.md` 620–621) put it after coding and bug-fixing. The 31–32 chain is stale. | **TO FIX** |
| D-6 | 377–380, 228, 418–419 | 377–379: *"Drop what belongs to the feature file alone — the block numbers, the `NEW` markers, and its own `# Application`. The `Nature:` lines stay"* | Cross-file, but it governs what the agent copies into the global: its source now carries no marker at all (`redacteur.md` 663–664), so the `NEW` rule is dead, and it carries two lines the fusionneur file never names — `Genre:` and `Global: ## <section>` (`redacteur.md` 57–62). By 377–383 (*"Nothing else changes"*) both are copied into the global on `INIT`, and nothing says what an `INSERT` does with them either. A `Global:` line inside the global is a self-reference; `Genre:` may or may not belong there. **Question**: are `Genre:` and `Global:` to be dropped like the block numbers, or kept like `Nature:`? | **TO FIX** (as a question) |
| D-7 | 460–503 vs 45, 467–470 | 462–464: *"A correction sometimes settles something about the product, and nothing carries it back"* — 467: *"This is the one call where the decision is not in a product file."* | Cross-file, but it is the reason the invocation exists: something now does carry it back — the Rédacteur's invocation 3 folds every `code/decisions-produit.md` into `desc-produit-fusion.md`, which invocation 1 then reads (45), and `redacteur.md` 626–627 calls that *"the only route the product has at all"* on a correction cycle. Invocation 3 is a second route to the same global, from `bug-list.md` lines rather than from the Contrôleur's decisions, and the command runs it *before* the Rédacteur (cmd rows 9 → 10 → 11). **Question**: is invocation 3 still wanted, and if so which route wins when a bug-list line and a decisions-file entry describe the same behaviour differently? Note that the frontmatter's *"Two invocations"* (D-4) would be right without it. | **TO FIX** (as a question) |
| D-8 | 494–496 vs 155 | 494: *"Merge what you kept, by the same three levels as invocation 1 — section, block, sentence."* | Invocation 3 inserts into existing sections too, but M2 is written under the plan's shape and invocation 3 writes no plan. Does the title check apply at invocation 3? Nothing says. | **NOTE** (question) |
| D-9 | cmd 9, cmd 56 | cmd 9: *"This command chains three phases — the Fusionneur over the bug-fix lists, then its two merge invocations."* — cmd 56: *"A feature with no bug-fix cycle goes straight to row 10."* | Command side of M3. Four phases now; and row 10 is the Rédacteur, so the sentence at 56 is accidentally still true but no longer says what it meant (straight to the merge). Also pre-existing and unchanged: row 8 (cmd 47) can never fire, row 6 (cmd 45) matches first on the same test; and once row 9 has run, the questions file invocation 3 wrote — even empty — satisfies row 6, which sends the next run to invocation 2 with no `plan-fusion.md` and no `desc-produit-fusion.md`. **Question**: is that the intended path? | **TO FIX** (cmd 9) · question (routing) |
| D-10 | 174–175 | *"The Rédacteur integrates them, then hands back."* | The fusionneur's answers are resolved by the fusionneur itself at invocation 2 (391–397, `PENDING` → `KEEP`/`REPLACE`/`DELETE`); the command's rows 6–7 go straight from an answered file to invocation 2 and never invoke the Rédacteur; and the Rédacteur's ordinary integration targets `desc-produit.md`, which is *"never touched"* after invocation 3 (`redacteur.md` 641–643). What does the Rédacteur integrate, and into which file? | **NOTE** (question) |
| D-11 | 24–25 vs 174, 210–212 | 24: *"Your report is the Product Owner's only manual step in the whole chain."* — 174: *"who fills the `Answer:` fields by hand"* — 211: *"It is where the Product Owner answers, by hand"*. | "Only manual step" is contradicted twice in the same file. Pre-existing. | **NOTE** |
| D-12 | 162 vs 71–72 | 162: *"the global is read by its index alone"* — 71–72: *"The index first, never the whole file … then load only the sections you need."* | "Alone" means *found through* the index; 71 says the sections are then loaded. Same word, two readings, no real contradiction once M2's intent is understood. | **NOTE** |
| D-13 | 93–94 | *"the highest `questions-fusionneur-NN.md` found at the root, or in `questions/fusionneur/` if the root holds none, plus one."* | No rule for the first run — none anywhere. `01` is the obvious reading but is not written (the same gap the classeur report raised as C5). | **NOTE** |
| D-14 | 299–300 | *"`## Gaps set aside` on a bug-fix cycle"* | The agent runs once per feature at the very end (462), on `desc-produit-fusion.md`, which is a copy of the feature's product file. On which run would its product file be a bug-fix cycle's? Stale or a leftover from an earlier design. | **NOTE** (question) |
| D-15 | 53–58 | four consecutive `---` | Empty separators, a leftover of a removed sub-part. Cosmetic. Pre-existing. | **NOTE** |

### Section references and counts checked, all consistent

*"see Where questions files live, above"* (362) → section at 87 · *"the same three levels as
invocation 1"* (494) → table at 319–325 · *"Three moves"* (472) → 1, 2, 3 at 474/478/494 ·
*"four headings"* (192) → four at 194–206 · *"Five verbs"* (141) → five named · *"none of the
three"* (399) → three rows at 393–397.

---

## Summary

- **A**: the three announced modifications are applied as specified. M2 is applied to the
  letter of the demande but not wired into the procedure (D-1, D-2, D-3).
- **B**: one unannounced change, the Extracteur mention dropped at 380 — consistent with the
  chain, NOTE.
- **C**: one BLOCKING — the rename of a settled blocking file (275–283) has no tool that can
  perform it, and the file forbids every workaround `Write` allows.
- **D**: the two questions that matter most are D-6 (what happens to `Genre:` and `Global:`
  lines when the source is copied into the global) and D-7 (whether invocation 3 survives now
  that the Rédacteur's invocation 3 carries the bug-fix decisions through
  `desc-produit-fusion.md`).
