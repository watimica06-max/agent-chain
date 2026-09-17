# controleur.md — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | TO FIX | refonte | 1 | modifications.md L1249-1258 ↔ passes/controleur.md L471-540 | The index's C14 (ÉCARTÉ, assembly by script) is the pass sheet's `### 13`, and its C13 (REPORTÉ, on the commands) matches no pass comment, so pass `### 14` (never-do cleanup, `Edit` removed) and `### 15` (feature folder), both applied in the file, are counted under numbers that do not say so and the eleven-passed count is short by one. |
| F02 | NOTE | refonte | 1 | passes/controleur.md L502-538 ↔ controleur.md L66-71 | Pass `### 14` is applied except for its last part: the two "never this file" lines (`idees.md`, the technical document / lot list / sequence) it asked to remove with their justifications still stand, while the `Edit` tool, its section and the two never-do entries went. |
| F03 | NOTE | refonte | 1 | controleur.md L36-43 ↔ modifications.md L1241-1275 | The "How you find things" block (grep `^### B15 `, never a whole read to find a block) is new to the file and listed nowhere in the index's section, which says the pass sheet alone was applied. |
| F04 | NOTE | refonte | 1 | modifications.md L1256 ↔ 9_controle.md L53-55 | C12 is listed REPORTÉ to the command rewrite, yet its change is already there: `9_controle` L42-58 no longer says `/8_code` runs the Contrôleur and `8_code` L12-14, L254-257 say one owner, so the index under-reports what the file holds. |
| F05 | NOTE | refonte | 3 | controleur.md L38 ↔ controleur.md L42-43 | The grep that locates a block is named but nothing bounds the read that follows it (no "to the next heading" rule, no offset/limit), so an agent that obeys "never a whole read" still has to choose how far to read and may read the file to its end. |
| F06 | TO FIX | refonte | 2 | controleur.md L237-238 ↔ controleur.md L282, L289-292 | An absent field "reads as this group did not run" while, thirty lines later, a group that did not run "has no file at all"; the assembly's table has a row only for a partial that is not there, so a partial present with a field missing has no outcome and the assembler decides alone. |
| F07 | NOTE | refonte | 2 | controleur.md L85 ↔ controleur.md L193 | A sheet named and absent sends every intention of its blocks under Doubtful, while "an intention nothing observes is Missing, not a doubt" — with the sheet unreadable nothing observes those intentions, and the two rules send the same lines to two fields. |
| F08 | NOTE | pre-existing | 2 | controleur.md L85, L281-282 ↔ controleur.md L227, L255 | The assembler is told to file blocks "under `Doubtful`" while the only heading the partials and the report carry is `## Doubts`, so the place named is one no file has. |
| F09 | NOTE | pre-existing | 2 | controleur.md L233 ↔ controleur.md L304 | "No prose" forbids paragraphs in the entries and "Prose: English, present indicative" governs their register — one word for two things, in the same output. |
| F10 | NOTE | pre-existing | 2 | controleur.md L104 ↔ controleur.md L217 | The never-do "Answer for a whole block at once" is contradicted by the example line "B9 Retention window — unchanged, nothing to build", which answers for a whole block, and the passage that sanctions it (L195-197) does not say it is the one exception. |
| F11 | QUESTION | refonte | 2 | controleur.md L205-209 ↔ controleur.md L246-248, L281-282 | The partial's opening `Blocks:` line is credited with telling a silent group from an absent one, but the assembly tells them apart by the file's presence and checks the prompt's per-group list, so the opening line has no reader and no rule says which list wins when the two differ. |
| F12 | QUESTION | pre-existing | 4 | 9_controle.md L68-70 ↔ 8_code.md L25 | A later report is "how two states are compared", yet the sheets a correction cycle writes sit under `bugfix-NN/code/` where neither the command (L26: "a correction cycle has neither") nor the agent (L48, `code/<lot>/` of the feature folder) looks, so a re-run after a correction cycle reports the same intentions missing and compares nothing. |
| F13 | NOTE | pre-existing | 4 | controleur.md L59-60 ↔ redacteur.md L104 | The agent is told a title may end in `NEW` and to ignore it; the Rédacteur also leaves `MODIFIED` on the heading line of `desc-produit.md`, which the rule does not name, so that marker reaches the agent with no instruction. |
| F14 | NOTE | pre-existing | 4 | controleur.md L215-216 ↔ detailleur.md L232-237 | The example cites "lot-07, criterion 2" as if criteria were numbered, while the sheet's `## Acceptance criteria` is an unnumbered bullet list, so the number is a position the agent counts and a reader of the report cannot check without counting the same way. |

Checked and found sound: the tool line (Read, Grep, Glob, Write) against every gesture, with no `Bash` and no rename left; the two `9_controle` prompts against the inputs both invocations require (folder, invocation, group, blocks, sheets, groups issued, blocks per group); the field names `## Intentions missing` / `## Doubts` against `9_controle` phase 5, the `### B<n> — <title>` heading and the `^### B15 ` grep against the classeur and the Rédacteur, and `fiche-executable.md` with `## Signatures` / `## Acceptance criteria` against the Détailleur.

| # | Status | Where | One line |
|---|---|---|---|
| A · numbering question (C_n vs pass `### n`) | open | — | |
| C1 · TO FIX | fixed | `.claude-new/agents/controleur.md:229-231` | |
| C1 · NOTE | other | `.claude-new/agents/controleur.md:154-158, 190-191, 193` | The repeated "mentions without observing" sentence went from 193; the boundary is still stated three times |
| C2 | fixed | `.claude-new/agents/controleur.md:143, 175` | |
| C4 | fixed | `.claude-new/agents/controleur.md:62-64, 85` | |
| C5 · NOTE (never stops on an assembly fault) | other | `.claude-new/agents/controleur.md:85, 254-256` | No change was asked; the file still carries on and files under Doubtful, as the sheet endorses |
| C5 · question (`8_code` naming a Contrôleur blocking file) | moot | `.claude-new/commands/8_code.md:12-14, 254-255` | `8_code.md` names no Contrôleur blocking file any more and never invokes him |
| C8 | fixed | `.claude-new/commands/9_controle.md:194` | |
| C9 | fixed | `.claude-new/commands/9_controle.md:32-33` | |
| C10 | fixed | `.claude-new/commands/9_controle.md:149-155` | |
| C12 · NOTE | fixed | `.claude-new/commands/8_code.md:12-14, 254-255` | |
| C14 | other | `.claude-new/agents/controleur.md:4, 66-71, 93-105` | Three more of pass 14's items applied — the two never-do entries and the Cadreur sentence are gone, `Edit` stays out — but the two "Never …" lines keep their justifications at 66-71, and the sheet still lists C14 as the script comment, écarté |
| C15 | fixed | `.claude-new/agents/controleur.md:26-27, 34, 125-126` | |
| B.1 | fixed | `.claude-new/agents/controleur.md:131` | |
| B.2 | open | — | |
| B.3 | fixed | `.claude-new/agents/controleur.md:91` | |
| C · tool no gesture names (`Grep`) | fixed | `.claude-new/agents/controleur.md:38-40` | |
| C · group → blocks mapping by elimination | fixed | `.claude-new/agents/controleur.md:246-249` | |
| D.1 | other | `.claude-new/agents/controleur.md:143, 160` | One 🔴 rule on the unit remains (143); line 160 still says "the block and the sentence" where 144-145 make a row or a list item a cut too |
| D.2 | fixed | `.claude-new/agents/controleur.md:175` | |
| D.3 | fixed | `.claude-new/agents/controleur.md:229-231` | |
| D.4 | fixed | `.claude-new/agents/controleur.md:116` | |
| D.5 | fixed | `.claude-new/agents/controleur.md:205-209` | |
| D.6 | fixed | `.claude-new/agents/controleur.md:246-249` · `.claude-new/commands/9_controle.md:215-218` | |
| D.7 | fixed | `.claude-new/agents/controleur.md:254-256` | |
| D.8 | fixed | `.claude-new/agents/controleur.md:258, 277` | |
| D.9 | fixed | `.claude-new/agents/controleur.md:62-64, 85` | |
| D.10 | fixed | `.claude-new/agents/controleur.md:166-169, 193` | |
| D.11 | fixed | `.claude-new/agents/controleur.md:93-105` | |
| D.12 | other | `.claude-new/agents/controleur.md:51, 91, 84, 125-127` | The triple `---` and the missing separator are gone; "no product file → stop and say so" still stands twice |
