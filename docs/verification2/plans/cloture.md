# Clôture — wave 4

Read-only. Built from `docs/verification2/plans/conflits.md` (the
consolidated table), against the corrected files in `.claude-new/`.

---

## 1 — The script, on everything

**Bare invocation, as the prompt writes it** — `python3` is not on
this machine's PATH (`python`, 3.12.10, runs it). Its default glob is
`.claude/agents/*.md` + `.claude/commands/*.md` — 🔴 **the chain
before the refonte, which no wave of this campaign touched**
(`git log 652beef..HEAD -- .claude/` is empty; last commit there is
`dafd2ec`, before the campaign). Every line it returns, verbatim:

    .claude/agents\arbitre.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\architecte.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\controleur.md
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\detailleur.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\diagnostiqueur.md
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\fusionneur.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between

    .claude/agents\realisateur.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\relecteur.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    .claude/agents\verificateur.md
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      empty separator    two rules, nothing between
      trailing rule      the file ends on a separator

    36 findings across 35 files.

📌 **All 36 are stacked `---` separators** (a run of two to nine with
nothing between, or one closing the file) in the old chain — not
introduced by a correction, since nothing wrote there.

**On the corrected chain** — every file wave 3 wrote, passed
explicitly (`.claude-new/agents/*.md`, `.claude-new/commands/*.md`,
`.claude-new/CLAUDE.md`):

    0 findings across 41 files.

---

## 2 — Replay what spans two files

Seven `BLOCKING`, seventeen `TO FIX` whose `Where` names two files.
Each read against the corrected files in `.claude-new/`, plus the four
shapes around what wave 3 touched (rule stated twice, dangling
cross-reference, entry lost from a list, one site of three).

| # | Status | Where | One line |
|---|---|---|---|
| 142 | `gone` | 6_convertit.md L94-97, L353-369 ↔ convertisseur.md L401-403, L656 | *Git, before invoking* now says "Never a `technique-*.md`, answered or not … it is filed in *Once it has run*, after the nature has run on it"; *Once it has run* files it into `closed/` after the invocation wrote its section, and keeps it at its name after a `No` or a block; the agent reads it "by its path, when there is one" |
| 148 | `gone` | fusion.md L47-51, L55-58 ↔ fusionneur.md L524-530 | Rows 7 (answered `### Q`, no plan → inv. 3), 9 (answered or empty, no plan → inv. 1), 10 (plan → inv. 2), then "Row 10 is the only route to invocation 2 … row 9 sends the run to the compare"; the agent's invocation 3 runs "once more on each answered questions file it wrote" |
| 158 | `gone` | 4_grille.md L102-111 ↔ sondeur.md L394-403 | The stop is on "an entry whose `Answer:` is empty and that carries no `Défaut:` line"; the exemption is stated with its test, `^Answer:\s*$` with no `Défaut:` above it in the same entry; the sondeur's line sits between `Question:` and `Answer:` as the command expects; `/2_structure` L35-36, L171-177 carries the same test |
| 162 | `gone` | 8_code.md L510-531 ↔ 7_lots.md L66-74, L268-273 | "Then close your worktree, before running `/7_lots`": commit, merge `--no-ff`, push, remove, in that order; then "open a fresh worktree from the merged `HEAD`"; `/7_lots` still creates its own from `HEAD` and removes it once the split holds |
| 266 | `gone` | fusionneur.md L99-104 ↔ fusion.md L127-133, L200; fusion_compare.md L68-72, L122; fusion_applique.md L53-58, L124 | All three commands compute "the highest `questions-fusionneur-NN.md` at the root and under `questions/fusionneur/` together, plus one" and carry `Questions file number: <NN>` in the prompt; `/fusion` says "at every one of its invocations", inv. 2 included; the agent: "named by the prompt … you never list a folder to find it" |
| 327 | `gone` | detailleur.md L252-284, L445-446 ↔ cadreur.md L822-829; concepteur.md L57-60, L114-116, L203-205, L300, L324-326; testeur.md L63-69, L334-335; realisateur.md L67-70, L83, L218-220; relecteur.md L453-457 | `## Files` = the lot's `Touches`, "never a file the lot creates"; `Touches` = existing files only, "the Concepteur places the symbol and names the file"; `## Declared` in `conception.md` names every created file; the three `## Outside the lot` checks test "neither `## Files` nor `## Declared`"; the detailleur's never-do names the Concepteur; concepteur L203: "`## Files` narrows nothing" |
| 328 | `gone` | arbitre.md L164, L172-180 ↔ 8_code.md L52-54, L232-240; detailleur.md L386, L472-487; realisateur.md L544-545; audit_blocages.md L114-118 | "Never write a placeholder under it: an empty number is the signal"; `Not settled here.` kept in the arbitre and in the realisateur's resume row, gone from the detailleur; `/8_code` 4b has the third row "Some numbers answered, others not … Stop, and do not rename", counted "against the `## Blocking N` headings"; the detailleur applies the answered ones after the Arbitre hands back |
| 53 | `gone` | assembleur.md L159-161, L173-175 ↔ sondeur.md L380-390, L461-462 | "An empty file is a file with no `### Q` and no prose — that one test … the zero-byte file a sondeur writes when it found nothing passes it"; the stop's example is "a `### Q` heading lacking the lines under it"; the sondeur's shape opens on `### Q1` with no file heading, and "Write the file even with no question in it" |
| 56 | `gone` | 4_grille.md L52, L464 ↔ assembleur.md L4, L36, L60 | Prompt carries `docs/features/<name>/blocked_assembleur.md`; the agent (tools `Read, Write`, no Glob) writes it "in the feature folder" and the row at L52 names the root |
| 243 | `standing` | docs/refonte/modifications.md L1601, L1603-1611 ↔ diagnostiqueur.md; diagnostique.md | Not touched: L1601 still reads ``| `diagnostiqueur.md` | ⚠️ **Pas de fiche**, et rien du fichier de travail |``, and the `## Commandes` table (L1603-1611) has no `diagnostique.md` row. 📌 Owner is `index`, which no wave-3 invocation carried — every `index`-owned line of the table is in the same state |
| 246 | `gone` | diagnostiqueur.md L80-82, L87-89, L478-483 ↔ diagnostique.md L133-138, L201-202 | The block list stays at "four cases"; "An existing `desc-bug.md` at invocation 2 stops you without a blocking file"; the command globs it before phase 2, "It exists → do not issue phase 2: relay it as done", and names `/7_lots` as the next step |
| 255 | `gone` | diagnostique.md L209-221 ↔ diagnostiqueur.md L160-170, L178-179 | "rename it once the agent reports having applied it — the same gesture for both files", `git mv investigation/blocked_<id>.md investigation/blocked_<id>-NN.md`, `NN` counted per identifier; the agent: "You never rename it … The orchestration does it" |
| 257 | `gone` | diagnostique.md L126-132, L201-207 ↔ diagnostiqueur.md L185-200 | "A phase-1 block withholds it … Report the blocked identifiers from your own phase-1 results"; the relay names both sources (blocking-file returns, gaps skipped as standing) and "never an identifier taken from an invocation-2 block: there is none"; the agent's inv. 2 blocks again on a missing report and says "never by a decision on this file" |
| 267 | `gone` | fusionneur.md L531-533, L557-560, L594-604 ↔ fusion.md L49 | Inputs list "your answered questions file at the root, when there is one"; "Two runs of one invocation" — moves 1-3, or move 4 alone on the answered file; output "the next questions file — written even when empty"; `/fusion` row 7 routes the answered file to inv. 3 |
| 268 | `gone` | fusion_compare.md L20-33, L159-163 ↔ fusion_applique.md L20-36, L161-165; fusion.md L44-45, L241-244 | Both siblings test `blocked_fusionneur.md` (empty → stop; filled but another invocation's → stop, naming the right command; filled and its own → in the prompt) and rename on the report, in `/fusion`'s form |
| 269 | `gone` | fusion_applique.md L89-101 ↔ fusion.md L161-175; fusionneur.md L425-436 | Both commands: "`plan-fusion.md` holds `INIT` alone → copy the product file over the global, in the worktree, before invoking"; `/fusion` bounds it to row 10 or row 3 naming inv. 2; the agent: "the command copied … You never copy it yourself" and strips the drop-list by targeted edits |
| 270 | `gone` | fusionneur.md ↔ redacteur.md | `Questions set aside` appears nowhere in `.claude-new/` |
| 329 | `gone` | arbitre.md L136-141 ↔ detailleur.md L326-350; realisateur.md L299-320 | The shape is stated once in the arbitre ("one `## Blocking N` per stop, even when there is only one, its three headings as `###` under it, and one `## Decision` at the end"); detailleur and realisateur each carry "Its shape — one `## Blocking N` per stop, even when …" with the `###` headings; the realisateur's old duplicate shape (L272-288) is gone, and the arbitre's L129-130/L180 with it |
| 331 | `gone` | 7_lots.md L35-38, L129-132, L297-302 ↔ cadreur.md L993-1012; 8_code.md | `/7_lots` reads both sections "before you rename it" and relays them "on every redécoupage"; the Cadreur: "State both sections in your report, on every redécoupage"; `/8_code` no longer names either section |
| 333 | `gone` | verificateur.md L78-82, L96-101, L120-125 ↔ cadreur.md L897-903; 7_lots.md | `Round: N` is the first line of `code/sequence.md`, "previous plus one when its `## Defects` carried lines; `1` otherwise"; the Cadreur "counts its rounds on that line, never on files … nothing archives `code/sequence.md`"; the Vérificateur reads the previous file's round line and `## Defects` state on every run; no `sequence-NN` anywhere in the chain |
| 335 | `gone` | architecte.md L118-125 ↔ detailleur.md L259-260, L288-291, L703-705; relecteur.md L413-417; realisateur.md L114 | "the coding agents cite a rule by its `R<n>`, and by nothing else"; the sheet example shows two `spécifique` rules under `## Conventions`; "The form is the Architecte's, never yours"; the Relecteur checks "the rules the sheet's `## Conventions` names, by their `R<n>` number" |
| 336 | `gone` | realisateur.md L71-77, L110-115 ↔ architecte.md L141-142 | "A `Grep` on `permanente` in the file finds the first — the word anywhere on the rule line, never a position"; fallback kept ("No rule carries the marker — read the file whole"); the Architecte says only "the third field, where the example above puts it"; "at the end of the line" appears nowhere |
| 340 | `gone` | testeur.md L171-172, L275-280, L343-344 ↔ 8_code.md L124, L413; realisateur.md L84-87; relecteur.md L389-390, L399 | "If the criterion it asserted is gone too — the sheet removes the behaviour — that is a block, `code/<lot>/blocked_testeur.md`"; the report line is gone ("A criterion the sheet removes has no line here — it is a block"); the green-by-declaration tests keep their `## Red` naming, read by realisateur and relecteur as the one exception |
| 341 | `gone` | redacteur.md L362-387, L751 ↔ fusionneur.md L237; fusion.md L45; 2_structure.md L30-31, L113-126 | "five headings, the last one left empty", `## Invocation` first; "`/2_structure` reads it to hand a 1 or a 2 back to you, `/fusion` a 3"; `/2_structure` stops on a 3 ("it is `/fusion`'s"); `/fusion` row 3 stands as written and routes on the line |

**Count**: 23 `gone` · 1 `standing` · 0 `moved`.

📌 **The one `standing` (#243) is not a correction that failed** — it is
a line no wave-3 invocation was given: the table's `index` owner has no
agent. The same holds for the other `index`-owned rows (#1-6, #21,
#26, #52, #62, #98, #100 …), single-file and outside this replay.

---

**Met on the way, named by no BLOCKING — noted, not pursued:** the
arbitre's new shape rule reads "One shape for every blocking file,
whoever wrote it … The agents that write one match this shape"
(arbitre.md L136-141), while the concepteur, testeur and relecteur
files (concepteur.md L145, testeur.md L184, relecteur.md L279) keep
their four `##` headings with no `## Blocking N` — consistent as long
as "every blocking file" is read as the two the Arbitre is ever given
(detailleur, realisateur), which is what C3's `Follows` says.
