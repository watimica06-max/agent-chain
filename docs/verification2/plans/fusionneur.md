# Plan — `fusionneur.md`

Built against `.claude-new/agents/fusionneur.md` (520 lines), the three
commands that invoke it (`fusion.md`, `fusion_compare.md`,
`fusion_applique.md`), the report `docs/verification2/fusionneur.md`
(both parts), `decisions.md`, and the thematic reports filtered to
`fusionneur` — six matching lines, all in `chemins-amont.md` (F21, F24,
F25) and `passages-amont.md` (F09, F10, F11); `renommages.md`,
`fichiers.md`, `chemins-aval.md`, `passages-aval.md` name it nowhere.

Every line cited below was opened in this pass. Line numbers are those
of the files as they stand today; where the report's differ (its L93-94
for the questions-file number is today's L88-89), today's are used.

Two findings were already settled in `decisions.md` — report F25 and
`passages-amont.md` F11 — and are carried here as decisions to apply,
never reopened.

---

## Verdicts at a glance

| Finding | Severity | Verdict | Entry |
|---|---|---|---|
| F01 – F08 | NOTE | confirmed | one grouped entry — the index |
| F09 | NOTE | overstated | no decision |
| F10 | TO FIX | confirmed | entry |
| F11 | TO FIX | confirmed | entry |
| F12 | TO FIX | confirmed | entry |
| F13 | TO FIX | confirmed | entry |
| F14 | NOTE | confirmed | entry — resolved through F23 |
| F15 | NOTE | confirmed | entry |
| F16 | NOTE | confirmed | entry |
| F17 | NOTE | confirmed | entry |
| F18 | NOTE | confirmed | entry |
| F19 · chemins-amont F24 | BLOCKING | confirmed | entry |
| F20 | BLOCKING | confirmed | entry |
| F21 · chemins-amont F21 | TO FIX | confirmed | entry |
| F22 · chemins-amont F25 | TO FIX | confirmed | entry |
| F23 | TO FIX | confirmed | entry |
| F24 · passages-amont F10 | TO FIX | confirmed | entry |
| F25 | QUESTION | confirmed | entry — `decisions.md` applied |
| passages-amont F09 | TO FIX | confirmed | entry |
| passages-amont F11 | QUESTION | confirmed | entry — `decisions.md` applied |

---

## Entries

### fusionneur.md F01 – F08 — the index understates what changed

Verdict: confirmed, each of the eight

| # | What was checked |
|---|---|
| F01 | `modifications.md` L806: « ses deux modifications ». `fusionneur.md` L3 announces « Three invocations »; L27-36 is built around `/9_controle` and the Rédacteur's fold-in |
| F02 | L88-89: « named by the prompt — the command has the fact, and you never list a folder to find it » — a hand-over the index does not mention |
| F03 | L176-179: « You resolve them yourself at invocation 2 … No other agent touches them » — not in the index |
| F04 | L191-193 (« writes that file and nothing else »), L200-204 (`## Invocation`, five headings), L289-290 (« The orchestration does it ») — none in the index |
| F05 | L240 and L383-387 name `Genre:` and `Global:` lines; the word « Extracteur » appears nowhere in the file — not in the index |
| F06 | L473-480: the `desc-produit-fusion.md` dependency and the « two say the same behaviour differently → a question » rule — not in the index |
| F07 | Neither « 250 » nor « Gaps set aside » appears in today's file; the index records no removal. The earlier state itself could not be checked — `.claude/` is out of bounds for this plan — so the finding stands on the index's silence alone |
| F08 | `modifications.md` L810 asks for the check « À l'`INSERT` »; L509-510 extends it to invocation 3 (« the title check applies here too ») — not in the index |

Decision: bring the `fusionneur.md` entry of `docs/refonte/modifications.md`
up to what the file changed — three invocations, the prompt-given
number, the self-resolved round-trip, the blocking file's fifth heading
and orchestration rename, the `Genre:`/`Global:` drop-list, invocation
3's dependency on `desc-produit-fusion.md`, the two removals, and the
title check at invocation 3.
Where: modifications.md L806-810 ↔ fusionneur.md L3, L27-36, L88-89, L176-179, L191-204, L240, L289-290, L383-387, L473-480, L509-510
Cited: modifications.md L806 — « ✅ **FAIT** — 📌 **ses deux modifications**, et ⚠️ **`commands/fusion.md` avec elles.** »
Owner: the index itself (`docs/refonte/modifications.md`) — no agent file changes
Also in: —

⚠️ **Whoever rewrites the entry applies this plan's decisions first** —
several of the lines above (L263, L383-391, L473-480) move again below,
and an index written before them would be stale on arrival.

---

### fusionneur.md F10 — a review that cannot happen

Verdict: confirmed
Decision: make the role statement agree with L431 — the report records what the merge did and is reviewed once it is done; the questions file, not the report, is the Product Owner's manual step before the global changes.
Where: fusionneur.md L24-25 ↔ fusionneur.md L431
Cited: L24-25 — « Your report is the Product Owner's last manual step before the global changes. » · L431 — « **Written after applying, never before.** »
Owner: fusionneur
Also in: —

📌 Part 2 lists D-11 as `fixed` at L24-25 — the wording moved, the
contradiction did not.

---

### fusionneur.md F11 — invocation 3 compares against a file it may not open

Verdict: confirmed
Decision: add `desc-produit-fusion.md` to invocation 3's inputs row, next to the `desc-bug.md` files that F25 puts there.
Where: fusionneur.md L473-480 ↔ fusionneur.md L263, L270
Cited: L263 — « | 3 | Bug-fix decisions | Every `bugfix-*/bug-list.md` of the feature · the global | … » · L270 — « **Load only what your invocation lists.** Not one file more. » · L473 — « You carry only what `desc-produit-fusion.md` does not already carry. »
Owner: fusionneur
Also in: —

---

### fusionneur.md F12 — the title question has no line and no resolution

Verdict: confirmed
Decision: give the title question its own line in the merge plan and its own resolution at invocation 2 — the section is renamed, or its title is kept — outside the three-row table that only knows rules.
Where: fusionneur.md L159-162, L359-361 ↔ fusionneur.md L136-149, L399-408
Cited: L136-137 — « **Five verbs only** — `REPLACE`, `INSERT`, `KEEP`, `DELETE`, `PENDING`. » · L401-405 — the three rows « The rule still holds / changed / no longer holds » · L407-408 — « An answer that resolves none of the three is ambiguous — it goes back as a new question » · L147-149 — « `[new block]` — that is what an answer about the title applies to »
Owner: fusionneur
Also in: —

📌 Part 2 lists D-1, D-2 and D-3 as `fixed` — the question is now
asked; what happens to its answer was never written.

---

### fusionneur.md F13 — an ambiguous answer has nowhere to go

Verdict: confirmed
Decision: list the next questions file among invocation 2's outputs; a run that writes one holding a question applies nothing and writes no report, and the next run returns to invocation 2 once it is answered.
Where: fusionneur.md L407-408 ↔ fusionneur.md L262, L91
Cited: L262 — « | 2 | Apply | … | The updated global · the merge report | » · L91-92 — « One file per invocation, carrying all your questions. The number advances once per invocation »
Owner: fusionneur
Follows: fusion.md, fusion_applique.md — they already carry the loop and change nothing: fusion.md L45 stops on « A root questions file with an empty `Answer:` », L50 sends « `plan-fusion.md` exists » to invocation 2; fusion_applique.md L26 stops on the same empty `Answer:`. ⚠️ **But both must pass invocation 2 its file number** — see F19.
Also in: —

Why « applies nothing »: fusion.md L44 and fusion_applique.md L24 stop
for good on `rapport-fusion.md` — a partial apply that wrote its report
would leave the ambiguous line pending for ever, and a partial apply
without a report would need the plan rewritten to say what was already
done. The Lexicographe uses the same mechanism (modifications.md
L795-800: « une réponse qui laisse le choix ouvert donne un nouveau
fichier de questions, jamais vide … c'est ce qui borne sa boucle »).

---

### fusionneur.md F14 — INIT reads a file invocation 2 does not list

Verdict: confirmed
Decision: resolved through F23 — once the command makes the copy, invocation 2's INIT step works on the global it was handed and the product file leaves the step; the inputs row then holds as written.
Where: fusionneur.md L383 ↔ fusionneur.md L262, L270
Cited: L383 — « **On `INIT`: copy the product file under `# Application`.** » · L262 — inputs « The merge plan · the questions file you wrote, answered · the global »
Owner: fusionneur
Also in: —

---

### fusionneur.md F15 — two drop-lists

Verdict: confirmed
Decision: keep one drop-list — block number, `Genre:` line, `Global:` line — and drop the `NEW` marker from L426-427, which the Rédacteur strips before the file reaches the Fusionneur.
Where: fusionneur.md L426-427 ↔ fusionneur.md L240, L385
Cited: L426-427 — « **Never carry a block's number or its `NEW` marker into the global.** » · L240 — « Carry over a block number, a `Genre:` line or a `Global:` line » · redacteur.md L706-708 — « **3. Strip every marker** — 🔴 **no `NEW`, no `MODIFIED` in the file you write.** ⚠️ **Nothing probes it**: it is read once, by the Fusionneur. »
Owner: fusionneur
Also in: —

---

### fusionneur.md F16 — the settled blocking files are read against L270

Verdict: confirmed
Decision: name the blocking files — the unnumbered one and the numbered ones — as standing inputs of every invocation, outside the « not one file more » rule.
Where: fusionneur.md L279-281, L295-296 ↔ fusionneur.md L270
Cited: L279-281 — « **First thing, every run: look for `blocked_fusionneur.md` in the feature folder.** 📌 **Several `blocked_fusionneur-NN.md` beside it are settled ones** — read them » · L270 — « **Load only what your invocation lists.** Not one file more. »
Owner: fusionneur
Also in: —

---

### fusionneur.md F17 — « never asked again » against « never open an earlier file »

Verdict: confirmed
Decision: let invocation 1 open the feature's own answered `questions-fusionneur-*` files, at the root or under `questions/fusionneur/`, and narrow L313-315 to the other agents' files.
Where: fusionneur.md L181-182 ↔ fusionneur.md L313-315
Cited: L181-182 — « **A question whose answer is recorded is never asked again** — re-asking would send the Product Owner back over what she has settled. » · L313-315 — « **Never open a questions file written before you** — those belong to the loops that ran earlier. ⚠️ **Invocation 2 reads the one you wrote, and it alone.** »
Owner: fusionneur
Also in: —

📌 The case is real on a feature with a correction cycle: invocation 3
asks and is answered before invocation 1 ever runs (fusion.md L47-51),
and the alternative — dropping L181-182 — costs the Product Owner a
question she has settled.

---

### fusionneur.md F18 — the title check has no hook in invocation 3

Verdict: confirmed
Decision: hang invocation 3's title check on the moment a kept line enters a section as a new block, since invocation 3 writes no `INSERT` line.
Where: fusionneur.md L156-157 ↔ fusionneur.md L509-510
Cited: L156-157 — « **At invocation 1, as you write the `INSERT` line** — 📌 **that is where you have the new block and the section's title side by side.** » · L509-510 — « by the same three levels as invocation 1 — 📌 **the title check applies here too** »
Owner: fusionneur
Also in: —

---

### fusionneur.md F19 · chemins-amont F24 — the number nobody passes

Verdict: confirmed
Decision: have `/fusion`, `/fusion_compare` and `/fusion_applique` compute the next `questions-fusionneur-NN` number — the highest at the root and under `questions/fusionneur/`, plus one, `01` when there is none — and pass it in the prompt the way `/3a_genre` and `/conventions` do, at every invocation, invocation 2 included (F13).
Where: fusionneur.md L88-89 ↔ fusion.md L157-162, fusion_compare.md L91-96, L45-46, fusion_applique.md L83-88
Cited: fusionneur.md L88-89 — « **Your number**: named by the prompt — 📌 **the command has the fact**, and you never list a folder to find it. » · fusion.md L161 — the whole prompt: « Feature folder: docs/features/<name>/. <Which invocation>. » (same at fusion_compare.md L95, fusion_applique.md L87) · fusion_compare.md L45-46 — « every `questions-fusionneur-NN.md` but the highest — the last one stays at the root, it carries the numbering » · 3a_genre.md L45-46 — « **Give the agent its questions file number in the prompt** — 📌 **the highest `questions-qualifieur-NN.md` in the root and in `questions/qualifieur/`** », L146 — « Your questions file number: NN. » · conventions.md L120-121 — « you give the agent its number in the prompt, counting the root and `questions/architecte/` »
Owner: fusion.md, fusion_compare.md, fusion_applique.md — they hold the fact and decide the prompt line
Follows: fusionneur — L88-89 stands; only the prompt template it expects gains the line. Part 2's D-13 (« neither states what the first run's number is ») closes with the `01` rule on the command side.
Also in: — (chemins-amont F24 names the agent, so it lands here and nowhere else)

---

### fusionneur.md F20 — a correction cycle never reaches invocation 1

Verdict: confirmed
Decision: make row 9 send to invocation 1 — it can only fire without `plan-fusion.md` — and leave row 10 as the sole route to invocation 2; rewrite L67-69, which affirms the wrong path.
Where: fusion.md L47-51, L58-61, L67-69 ↔ fusionneur.md L117, L377, L466-519
Cited: fusion.md L49 — « | 9 | `questions-fusionneur-NN.md`, answered — 📌 **empty, or its questions resolved** | **Fusionneur, invocation 2** | » · L67-68 — « **An empty one sends the next run to row 9, not back to row 7** » · L60-61 — « a correction cycle would go to invocation 2, which needs a plan no invocation wrote » · fusionneur.md L117 — « **The merge plan is what invocation 2 applies** — without it, the comparison would be redone from scratch. »
Owner: fusion.md
Follows: — (the agent changes nothing: L268 « With no question raised, invocation 2 follows immediately » holds once a plan exists)
Also in: commandes.md — chemins-amont F22 is the same defect, naming `fusion.md` alone

Walked after the change, on a feature with a `bugfix-*/` folder: row 8
→ invocation 3 writes an empty file → row 9 → invocation 1 writes the
plan and its file → row 5 stops, or row 10 → invocation 2. An answered
invocation-1 file always sits beside a plan, so row 10 covers it and
row 9 loses nothing.

📌 Part 2 lists D-9 as `other` for the same reason.

---

### fusionneur.md F21 · chemins-amont F21 — invocation 3 never applies its answers

Verdict: confirmed
Decision: give invocation 3 the step that applies its own answered questions file to the global and writes the next questions file — empty, or holding what an answer left ambiguous — and list that file among its inputs.
Where: fusion.md L47 ↔ fusionneur.md L263, L487-519
Cited: fusion.md L47 — « | 7 | 🔴 **`questions-fusionneur-NN.md` holding `### Q`, answered**, and no `plan-fusion.md` | **Fusionneur, invocation 3** | » · fusionneur.md L263 — inputs « Every `bugfix-*/bug-list.md` of the feature · the global » · L487 — « **Three moves.** » — read, sort, merge; none resolves an answer
Owner: fusionneur
Follows: — (fusion.md L47 already routes there and keeps its wording)
Also in: —

---

### fusionneur.md F22 · chemins-amont F25 — two commands never rename the blocking file

Verdict: confirmed
Decision: add to `/fusion_compare` and `/fusion_applique` the blocking-file test before invoking — an empty `## Decision` stops, a filled one is named to the agent — and the rename to `blocked_fusionneur-NN.md` once the agent reports having applied it, in the form `/fusion` already uses.
Where: fusionneur.md L289-290 ↔ fusion_compare.md L18-22, fusion_applique.md L18-27
Cited: fusionneur.md L289-290 — « **You never rename it** — 📌 **you have no tool that removes a file.** ⚠️ **The orchestration does it**, once you have reported. » · fusion_compare.md L20 — the only pre-test: « `desc-produit-fusion.md` absent → stop » · fusion_applique.md L24-26 — three tests: `rapport-fusion.md`, `plan-fusion.md`, an empty `Answer:` — no `blocked_*` · fusion.md L195-198 — « **The agent reports having applied a decision → rename its blocking file:** `git mv <folder>/blocked_<agent>.md <folder>/blocked_<agent>-NN.md` »
Owner: fusion_compare.md, fusion_applique.md
Follows: — (fusionneur L279-296 stands as written)
Also in: —

---

### fusionneur.md F23 — INIT is a whole-file copy the chain forbids

Verdict: confirmed
Decision: move the copy to the command — when `plan-fusion.md` holds `INIT` alone, `/fusion_applique` and `/fusion` copy `desc-produit-fusion.md` over the global before invoking, and invocation 2 strips what belongs to the feature file alone by targeted edits.
Where: fusionneur.md L383-391 ↔ fusion.md L79-84, redacteur.md L689-690
Cited: fusion.md L82-84 — « **The agent has no tool that copies** — ⚠️ **and a whole read followed by a whole write truncates in silence.** 🔴 **It amends the copy; you make it.** » · redacteur.md L689-690 — « **You never copy it yourself** — ⚠️ **you have no tool that copies**, and a whole read followed by a whole write truncates in silence. » · fusionneur.md L383 — « **On `INIT`: copy the product file under `# Application`.** »
Owner: fusion_applique.md, fusion.md — they decide the copy, as fusion.md L79-80 does for row 6
Follows: fusionneur — L383-391 rewritten around a global that already holds the copy
Also in: —

📌 The test « the plan holds `INIT` alone » is one grep, of the same
kind as the `Answer:` grep both commands already run (fusion_applique.md
L32-33, fusion.md L26-28) — counts, not content.

---

### fusionneur.md F24 · passages-amont F10 — a section nobody writes

Verdict: confirmed
Decision: drop the `## Questions set aside` skip; what was ruled out is kept out of the global by `Genre: hors périmètre`, which the Fusionneur now reads on every block (passages-amont F11 below).
Where: fusionneur.md L306-308 ↔ redacteur.md L40-45
Cited: fusionneur.md L306-307 — « **Skip the product file's closing section** — `## Questions set aside`. » · redacteur.md L42-45 — the whole structure: « `# Application` / `# Domaine : <nom>` / `## <Section>` / `### <Bloc>` », no closing section · a grep of every agent and command under `.claude-new/` for « Questions set aside » finds the Fusionneur's own L306-307 and nothing else; the only « set aside » section in the chain is the Diagnostiqueur's `## Gaps set aside` in `desc-bug.md` (diagnostiqueur.md L562)
Owner: fusionneur
Also in: —

📌 Part 2 lists D-14 as `fixed` at L306-308 — the rule was reworded
around a section that still does not exist.

---

### fusionneur.md F25 — what invocation 3 reads

Verdict: confirmed — and settled in `decisions.md`
Decision: apply decisions.md `fusionneur.md` F25 — invocation 3 reads every `bugfix-*/desc-bug.md`, never `bug-list.md`; one absent, invocation 3 does not run and says so, with no fall-back.
Where: fusionneur.md L263, L489 ↔ diagnostiqueur.md L34-36, L44, L560-562
Cited: fusionneur.md L489 — « **1. Read every `bugfix-*/bug-list.md` of the feature**, oldest folder first. » · diagnostiqueur.md L44 — « **The Product Owner creates the folder and writes `bug-list.md`** — 🔴 **you write everything else.** » · L560-562 — « **Then the gaps set aside**, with the reason their report gives: `## Gaps set aside` » · decisions.md L89 — « **Invocation 3 reads `desc-bug.md`, never `bug-list.md`.** », L99-100 — « `desc-bug.md` absent — 🔴 invocation 3 does not run, and says so. »
Owner: fusionneur — L3, L263, L487-507 (the three-row sort at L496-500 is written for a Product Owner's line and is re-read against a Diagnostiqueur's entry, which carries a bearer and a nature)
Follows: fusion.md — row 8 keeps testing the `bugfix-*/` folder (L48); the « does not run, and says so » outcome is the agent's report, relayed as any other
Also in: —

---

### passages-amont F09 — a `blocked_redacteur.md` row 3 cannot route

Verdict: confirmed
Decision: in row 3, route a filled `blocked_redacteur.md` to the Rédacteur's invocation 3 by its name — under `/fusion` the Rédacteur runs no other invocation.
Where: fusion.md L43, L46 ↔ redacteur.md L333-340
Cited: fusion.md L43 — « | 3 | A `blocked_*.md` with a filled `## Decision` | 📌 **The agent its name carries**, at the invocation its `## Invocation` line names | » · redacteur.md L340 — « **Its shape** — four headings, the last one left empty: » followed by `## What blocks`, no `## Invocation` · fusionneur.md L200 — « **Its shape** — five headings, the last one left empty: » with `## Invocation` first
Owner: fusion.md
Follows: —
Also in: redacteur plan — chemins-amont F23 (`fusion.md L43 ↔ redacteur.md L343`) is the same defect from the Rédacteur's side. ⚠️ **If that plan chooses instead to give the Rédacteur's blocking file an `## Invocation` heading, row 3 stands as written and this entry falls** — the two plans must pick one.

---

### passages-amont F11 — which genres enter the global

Verdict: confirmed — and settled in `decisions.md`
Decision: apply decisions.md `passages-amont.md` F11 — read `Genre:` on every block, at invocations 1 and 2, `INIT` included; `directive` and `hors périmètre` blocks never enter the global, `comportement`, `transverse`, `recette` and `référence` do; the `Genre:` line itself still does not carry over (L240, L385).
Where: fusionneur.md L337-353, L383-387, L240 ↔ redacteur.md L706-708, decisions.md L104-115
Cited: fusionneur.md L339-340 — « **The unit of merge is the descriptive sentence, never the whole block.** » — no genre test anywhere in invocation 1 · L383-387 — `Genre:` is met once, at `INIT`, only to be dropped · redacteur.md L706-708 — the fold-in strips « `NEW`, `MODIFIED` » and nothing else, so `Genre:` reaches the Fusionneur on every block · decisions.md L106 — « **The Fusionneur reads `Genre:` on every block**, not only at `INIT`. »
Owner: fusionneur
Follows: — (the Rédacteur already leaves the line in place; `desc-bug.md` carries natures, not genres, so invocation 3 is untouched)
Also in: —

📌 Under F23 the `INIT` copy is the command's: the genre filter then
runs as a strip on the copied global, block by block, alongside the
number/`Genre:`/`Global:` drop.

---

## Judged, no decision

### fusionneur.md F09 — `Glob` declared, never named

Verdict: overstated
Where: fusionneur.md L4 ↔ fusionneur.md L88-89, L279, L380, L489

The fact holds: `tools: Read, Grep, Glob, Edit, Write` (L4) and no
sentence names `Glob`. The consequence does not: L88-89 forbids listing
a folder **to find the number** — « you never list a folder to find
it » — not listing as such, and a declared tool needs no sentence to be
usable. The three gestures (L279 blocked files, L380 the filed questions
file, L489 the `bugfix-*/` folders) have the tool they need. NOTE is
already the floor; what remains is a wording nicety, not a gap in the
agent's means. No decision.

---

## Part 2 of the report — the previous round's statuses

| Item | Read against today's file |
|---|---|
| B-1 `moot` | Holds — « Extracteur » appears nowhere in the file |
| C `fixed` | Holds — L289-290 and fusion.md L195-202 agree; F22 covers the two commands that do not |
| D-1 to D-3 `fixed` | The question is asked (L159-162, L147-149); its answer has no reader — F12 |
| D-9 `other` | Confirmed as F20; the decision is above |
| D-11 `fixed` | The wording changed; the contradiction with L431 did not — F10 |
| D-12 `open` | ⚠️ **Not judged**: the report gives neither its text nor a location, and nothing in the reading list carries it |
| D-13 `other` | Confirmed as F19; the `01` rule on the command side closes it |
| D-14 `fixed` | The rule was reworded around a section nobody writes — F24 |
| D-6, D-7, D-8, D-10, D-15 `fixed` | Hold at the lines cited (L240/L383-388, L473-480, L510, L176-179, L53) |

---

## Order of application

The entries touch the same lines more than once; applied in this order
nothing is written twice:

1. **fusion.md** — F20 (rows 9-10, L67-69), passages-amont F09 (row 3), F19 (number in the prompt), F23 (`INIT` copy at row 10).
2. **fusion_compare.md** — F19 (number), F22 (blocking-file test and rename).
3. **fusion_applique.md** — F19 (number), F22 (blocking-file test and rename), F23 (`INIT` copy).
4. **fusionneur.md** — F25 and F11 (invocation 3's inputs and first move), F21 (invocation 3 on an answered file), passages-amont F11 (genre filter), F23/F14 (`INIT` step), F15 (one drop-list), F12 (title line and resolution), F13 (invocation 2's outputs), F16, F17, F18, F10, F24.
5. **modifications.md** — F01-F08, last, from the corrected file.

---

## To settle

Nothing. No confirmed finding turns on intent, scope or user-facing
behaviour that `decisions.md` has not already settled (F25,
passages-amont F11). Two choices made above are mechanics and are
flagged for the Product Owner's eye only:

- **F13** — an ambiguous answer at invocation 2 makes the run write a
  questions file and nothing else. The alternative (apply what is not
  ambiguous, hold the rest) needs the plan rewritten mid-way and a
  report that does not end the merge; both commands stop for good on
  `rapport-fusion.md`.
- **F17** — invocation 1 may read the feature's own answered
  `questions-fusionneur-*` files. The alternative (drop L181-182 for
  invocation 1) re-asks the Product Owner what invocation 3 settled.

⚠️ **One alignment, not a question**: passages-amont F09 is decided
here on the `fusion.md` side and in the redacteur plan on the
Rédacteur's side (chemins-amont F23) — whichever form that plan picks,
only one of the two is applied.
