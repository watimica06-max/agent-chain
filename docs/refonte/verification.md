# Refonte verification — investigation plan

**28 investigations, two waves.** Wave 2 starts once wave 1 is done.

🔴 **Every investigation is READ-ONLY.** Each writes one report under
`docs/verification/` and changes nothing else.

## Setup

The rebuilt chain sits in `.claude-new/` and `docs-new/`, beside the
current `.claude/` and `docs/`.

🔴 **Read what you need, never a folder whole.** 📌 **The chain is
828 KB** — ⚠️ **each investigation below says what to grep and what to
open.**

## Which file is authoritative

| File | What it is |
|---|---|
| `docs/refonte/passes/<agent>.md` | 🔴 **The defects, as analysed** — authoritative for wave 1 |
| `docs/refonte/modifications.md` | 📌 **What was applied, discarded, deferred, and the spec of each structural change.** ⚠️ **It states what I claim to have done — that is what is being checked** |
| `docs/refonte/sujets.md` | 🔴 **The structural decisions.** 📌 **Not loaded in wave 1** — it is checked once, whole, by V2.7 |

---

# Wave 1 — one investigation per agent, 20 in parallel

`lexicographe` · `redacteur` · `decoupeur` · `qualifieur` · `classeur` ·
`sondeur` · `assembleur` · `convertisseur` · `architecte` ·
`fusionneur` · `cadreur` · `verificateur` · `detailleur` ·
`concepteur` · `testeur` · `realisateur` · `relecteur` · `arbitre` ·
`controleur` · `diagnostiqueur`

```
READ-ONLY. Modify nothing. Write one file:
docs/verification/agent-<agent>.md

Read:
1. .claude/agents/<agent>.md        — old
2. .claude-new/agents/<agent>.md    — new
3. docs/refonte/passes/<agent>.md   — the defect analysis. 🔴 Six agents
   have none: concepteur, testeur, arbitre, fusionneur, diagnostiqueur,
   qualifieur. ⚠️ For those, skip section A and give B, C and D your full
   attention — nobody has ever read them critically.
4. docs/refonte/modifications.md — 🔴 **your section only**: `grep -n '^# '` returns
   24 headings; read from yours to the next. The file is 75 KB, a
   section about 5. 📌 Two agents share one section:
   `# \`classeur.md\` · \`decoupeur.md\``.

Your section of docs/refonte/modifications.md is laid out like this:
- A table, "Ce qui a changé" — one row per structural modification and
  the file it touches
- "Sa fiche de passe" — three lines: Passés (N), Écartés (N),
  Reportés/Partiellement passés (N), each listing comment numbers, then
  a table giving the reason for every discarded or deferred one
- "La demande" — the full spec of each structural modification, as
  written before it was applied. This is what you verify against.
- Some agents have no "La demande": they had no structural
  modification, only a pass sheet.

The comment numbers link to the pass file, but the prefixes differ:
modifications.md writes C1, C2, C3 while most pass files head their
comments `### 1`, `### 2`. Match on the number. Two exceptions:
architecte.md uses `### C1` and convertisseur.md uses `### c.1`.

Answer four questions, in this order.

A. CONFORMITY
For every defect modifications.md lists as PASSÉ: open the pass file,
read the defect as analysed, then verify in the new file that it is
fixed — and fixed the way the pass file asked, not approximately.
For every defect listed as ÉCARTÉ or REPORTÉ: verify it was NOT applied.
Report each as: defect id, expected, found, verdict.

B. UNANNOUNCED CHANGES
Diff old against new. For every difference that matches neither a defect
in the pass file nor a structural modification in modifications.md:
quote both versions and state what it changes. Include renumberings,
moved sections, reworded rules, rewritten tables.

C. GESTURES AGAINST TOOLS
List the frontmatter tools. For every gesture the agent must perform,
verify it has the means. Report both directions: a gesture with no tool,
and a tool no gesture uses.

D. INTERNAL COHERENCE
In the new file alone: a reference to a section that does not exist · a
term used in two senses · a rule contradicted elsewhere in the file · an
announced count that does not match ("the eight moves" followed by
nine) · a procedure branch that leads nowhere.

Report format: one finding per entry — line number, quote, severity
(BLOCKING / TO FIX / NOTE). If you cannot settle a point, write it as a
question rather than a verdict.
```

---

# Wave 2 — thematic, 8 in parallel

## V2.1 — Renames

```
READ-ONLY. Write docs/verification/renommages.md

For each name below, grep all of .claude-new/ and docs-new/ and answer:
1. Who writes it?
2. Who reads it?
3. Does the old name survive anywhere?

New or changed names:
- `Touches` field of a lot (new, beside `Modifies`)
- `## Findings`, `## Attempts` of a verdict (new)
- `## Declared` of a conception report (new)
- `Genre:`, `Global:` lines of a block (new)
- `Défaut:` line of a question (new)
- `en anglais :` line of a lexicon entry (new)
- `par-genre/` and its six files (new)
- `GRILLE_EXISTANT.md`, `GRILLE_CONVENTIONS_RETIREES.md` (new)
- `desc-produit-fusion.md` (new)
- `code/recette.md`, `code/recette-ordonnee.md` (new)
- `code/registre-questions.md`, `code/decisions-produit.md` (new)
- `technique-<nature>.md` of the Convertisseur (new)
- `questions-existant-NN.md` (new)
- Grid question `C1.3` moved to `E3.1`; `C1.4`–`C1.7` renumbered
  `C1.3`–`C1.6`

Removed names — report any surviving occurrence:
`[integrated:]` · the second table of `couverture.md` · agent
`extracteur` · `blocked_controleur` · `blocked_verificateur` carrying a
`## Decision`
```

## V2.2 — File writers and readers

```
READ-ONLY. Write docs/verification/fichiers.md

Census every file the chain produces and consumes.

🔴 Do not read the chain whole — it is 828 KB. Work by grep:
1. Two passes, then take the union — neither alone is complete:
   `grep -rhoE '\`[^\`]*\.md\`' .claude-new/ docs-new/ | tr -d '\`' | sort -u`
   catches the names written in prose (about 168),
   `grep -rhoE '[a-zA-Z0-9_<>/.-]+\.md' .claude-new/ docs-new/ | sort -u`
   catches those inside code blocks, where backticks are absent.
   ⚠️ Discard the fragments the second pass produces — a name must have
   a stem before `.md`.
2. For each name, `grep -rn` it across .claude-new/ and docs-new/, and
   read only the hit lines and their surroundings.
3. Open a file in full only when the hits do not settle who writes it.

One line per file: who writes it, who reads it, at what point of the
cycle.

Then report three anomalies:
- A file written that nobody reads
- A file read that nobody writes
- A file written by two agents with no stated order

Check specifically that nothing still expects: the Contrôleur's
blocking file, the Vérificateur's blocking file, the second table of
`couverture.md`.
```

## V2.3 — Paths and loops, upstream

```
READ-ONLY. Write docs/verification/chemins-amont.md

Scope: /1_lexique, /2_structure, /3_decoupe, /3a_genre, /3b_nature,
/4_grille, /5_reclasse, /6_convertit, /conventions, /fusion,
/fusion_compare, /fusion_applique.

For each command, enumerate every possible state of the folder when it
is launched, and verify each has a written outcome. A state with no
routing line is a hole.

For each loop: what terminates it? Report any exit condition that is
unreachable, and any loop that can restart on itself.

Check specifically:
- An empty questions file · an unanswered one · two at the root
- A blocking file with an empty decision · a filled one · an already
  numbered one
- The second closing pass: it fires when the first returns an empty
  file, and must run once only
- The Convertisseur's short loop (technical questions) against its long
  loop (product questions)
- The Architecte's invocation 4: how does the command know to run it
  rather than invocation 1?

Trace three end-to-end scenarios and say where each stops: a first
feature on an empty project · a feature on a project that already has
some · a correction cycle.
```

## V2.4 — Paths and loops, downstream

```
READ-ONLY. Write docs/verification/chemins-aval.md

Scope: /7_lots, /8_code, /9_controle, /deploie, /diagnostique,
/audit_blocages, /audit_conventions.

Same work: every state, every outcome, every loop and what terminates
it.

Check specifically:
- The per-lot loop of /8_code chains five agents (detailleur,
  concepteur, testeur, realisateur, relecteur). What happens if each
  blocks, one by one?
- The attempt counter: where does it live, who writes it, who
  increments it, what happens if it is missing?
- The escalation to opus after two `Cause: reasoning`
- The return to the split: who writes it, who reads it, when is it
  archived, and the stop at the third
- The Cadreur's three rounds with the Vérificateur
- /9_controle: six phases, three of which do not run on a correction
  cycle. Do the other three actually run?

Trace three scenarios: a lot that passes first time · a lot that fails
three times · a redécoupage mid-block.
```

## V2.5a — Handovers, upstream

```
READ-ONLY. Write docs/verification/passages-amont.md

For each consecutive pair, verify that what the first writes matches
exactly what the second expects: same section names, same field names,
same shape, same possible values. Cite the writer's line and the
reader's line. A one-character gap in a section name is BLOCKING.

🔴 Read only the sections that say what the agent reads and writes.
⚠️ The heading is not the same in every agent — three forms coexist:
- `## What you read` and `## What you write` — 9 agents of 20
- `## Where you work` — a table of paths, used by cadreur,
  convertisseur, lexicographe
- The invocation table under `## INVOCATION n`, or a `| # | Invocation |
  Inputs | Output |` table — used by redacteur, fusionneur,
  diagnostiqueur, and every multi-invocation agent

📌 `grep -n '^## '` the agent first, pick the headings that apply, then
read those ranges. 🔴 An agent where none of the three forms appears is
itself a finding — report it rather than skipping it.

Pairs:
lexicographe→redacteur · redacteur→decoupeur · decoupeur→qualifieur ·
qualifieur→classeur · classeur→sondeur · sondeur→assembleur ·
assembleur→redacteur · redacteur→convertisseur ·
convertisseur→architecte · convertisseur→cadreur ·
9_controle→redacteur · redacteur→fusionneur

Never exercised, check hardest: 9_controle→redacteur
```

## V2.5b — Handovers, downstream

```
READ-ONLY. Write docs/verification/passages-aval.md

Same work and same reading rule as V2.5a.

Pairs:
cadreur→verificateur · verificateur→detailleur · detailleur→concepteur
· concepteur→testeur · testeur→realisateur · realisateur→relecteur ·
relecteur→detailleur · relecteur→controleur · detailleur→arbitre ·
realisateur→arbitre · arbitre→architecte

Never exercised, check hardest: detailleur→concepteur ·
concepteur→testeur · testeur→realisateur
```

## V2.6 — Reading budget

```
READ-ONLY. Write docs/verification/budget.md

Estimate what one invocation loads, per agent, and report those at risk.

🔴 Read only the sections that say what the agent reads, then measure
the target files with `wc -c`. Never open an agent whole.

⚠️ The heading differs between agents — `## What you read` (9 of 20),
`## Where you work` (a table of paths), or the invocation table under
`## INVOCATION n`. 📌 `grep -n '^## '` first, then read the ranges that
apply. 🔴 Report any agent where none of them appears.

Priority:
- Realisateur and Relecteur now read every rule marked `permanente` of
  the conventions file, whole
- Sondeurs load the transverse blocks beside their own
- Convertisseur reads three split files beside its blocks
- Architecte, invocation 4, reads the whole conventions file
- Controleur, at assembly, reads every partial

For each: how many lines, and does it hold? Compare to what the agent
read before. Report any agent now reading twice as much, even if it
still holds.
```

## V2.7 — Transfer from the decisions to the index

```
READ-ONLY. Write docs/verification/transfert.md

Read both files whole: docs/refonte/sujets.md and
docs/refonte/modifications.md.

sujets.md holds the structural decisions, one per heading, in the form
`## <ID> · <title>` — A1 to A7, C1 to C5, Rupture 3/5/6, F1 to F3, U1 to
U14, A-2, A-6, D1 to D24, P1 to P14, Q.

modifications.md holds what was done with them. It rarely cites the
identifiers: match by meaning, not by string.

For every heading of sujets.md, answer:
1. Is the subject SETTLED or DISCARDED in sujets.md?
2. If settled: does modifications.md carry it — as a modification, or in
   an agent's pass sheet?
3. If it carries it: does what modifications.md asks match what
   sujets.md decided? Quote both.

Report three classes:
- LOST — settled in sujets.md, absent from modifications.md. This is
  what the investigation exists to find: nothing else can see it.
- DISTORTED — present but asking for something other than what was
  decided.
- DISCARDED BUT APPLIED — discarded in sujets.md, yet modifications.md
  carries it.

For each, quote the sujets.md heading and line, and what
modifications.md says or fails to say.
```

---

# Git, in this mode

🔴 **One worktree for the whole campaign**, created before the first
invocation and merged once at the end. ⚠️ **Not one per
investigation**: each writes a distinct file, and twenty-eight merges
buy nothing.

**Before invoking anything:**

```
git worktree add ../verif-<date> -b verification/<date>
cd ../verif-<date>
mkdir -p docs/verification
```

🔴 **Enter the worktree before invoking, not after a write fails** — 📌
**the harness blocks a subagent's writes until the session is
isolated.** ⚠️ **Measured on this project: the agent does the full job,
cannot write, and the whole invocation is redone.**

🔴 **Create `docs/verification/` inside the worktree** before the first
agent runs — 📌 **an agent that has to create its own folder sometimes
writes beside it instead.**

❌ **Never pass `isolation`** — 📌 **the agents read the same files and
write different ones.**

**Once every report is written:**

```
git add docs/verification/
git commit -m "Verification campaign <date>"
cd <main checkout root>
git merge --no-ff -b verification/<date>
git push
git worktree remove ../verif-<date>
```

🔴 **The commit is yours** — 📌 **the agents have no Bash.**

🔴 **The push is part of the merge, not an afterthought.** ⚠️ **A
campaign that sits only on the local machine is lost with it.**

⚠️ **A worktree holding uncommitted files refuses a plain remove** — 🔴
**never force it**: say what is left there and stop.

📌 **Merge even when reports are missing** — 🔴 **what was written is
worth keeping**, and say which are missing.

---

# After the reports

🔴 **Read them together, triage, fix in one pass.** ⚠️ **No fixing as
the reports land** — two concurrent edits on one file lose each other.

📌 **Order**: wave 1 BLOCKING findings first.
