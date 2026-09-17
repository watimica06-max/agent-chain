# Assembleur — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L529 ↔ assembleur.md L44-46, L20-22, L230-233 | C3 asked for one reading "stated once" with the forbidden line reworded to "a gap raised once"; the line keeps "only one reading raised it" with a rider appended, and the same rule is stated three times, so the pass is applied differently than asked. |
| F02 | NOTE | refonte | 1 | modifications.md L516-526 ↔ assembleur.md L57-59, L270-271 | The rule "a blocked run writes no questions file, not even an empty one" is new in the file and appears neither in the index table nor in the pass sheet, so the index does not tell the whole truth about what changed. |
| F03 | TO FIX | refonte | 2 | assembleur.md L146-147 ↔ assembleur.md L158-159 | "A heading, a blank line, nothing else" is an empty file at L146 and "a heading with no entry under it" is a stop at L159, so a sondeur file holding only a heading is both counted as empty and blocked on, and two runs of the merge diverge on it. |
| F04 | NOTE | refonte | 2 | assembleur.md L32-33 ↔ assembleur.md L83-85, L54 | A missing file "stops you — say which" while blocking demands a file and L83 names only the two PART 3 stops as what is blocked on, so the missing-file case has no defined outcome (report or `blocked_assembleur.md`); it costs nothing today because `4_grille.md` L400 checks existence before invoking. |
| F05 | QUESTION | refonte | 2 | assembleur.md L87-88 ↔ assembleur.md L155-156, L190, L259-260 | A resume "with" a settled decision on an unplaceable question requires writing a `Block:` line the agent never read, which L190 and L259 forbid; the file does not say whether the Product Owner corrects the sondeur file by hand or the agent applies the decision, so the resume path leads nowhere as written. |
| F06 | TO FIX | unknown | 4 | 4_grille.md L423 ↔ assembleur.md L54, L99-100 | The assembleur prompt names the blocking file as bare `blocked_assembleur.md` under a header "in docs/features/<name>/cadrage-produit/" while every sondeur prompt carries a full path, and the agent has no Glob; a read at the wrong folder makes it a "missing file" and the agent stops again on a decision already filled. |
| F07 | TO FIX | refonte | 4 | 4_grille.md L197-198 ↔ 4_grille.md L63-71, L494 | The exception "not on a turn that re-ran the merge alone" sits under "Git, before invoking" in the past tense, so an orchestrator can read it as applying after the merge and file the four `cadrage-produit/` files before re-running the assembleur, which then reads nothing. |
| F08 | NOTE | unknown | 4 | 4_grille.md L41 ↔ 4_grille.md L47-52 | "Five names, one per invocation" heads a table of six rows, the assembleur's being the sixth, so the check the orchestrator runs before the merge is announced one name short. |
| F09 | NOTE | pre-existing | 4 | assembleur.md L36-37 ↔ 4_grille.md L496, L498 | "Every file empty is how the grid says the product file is closed" is no longer true: an empty first-time file starts the second time, and only the second time closes the file, so the agent carries a stale fact about the loop it feeds. |
| F10 | NOTE | refonte | 4 | assembleur.md L146-147 ↔ sondeur.md L376-379, L449-450 | The empty file is described as "a heading, a blank line" while the sondeur's output shape carries no file heading and its empty file is unspecified; a zero-byte file still passes "no `### Q` and no prose", so the gloss describes a file the producer never writes. |

Sound: C1, C2, C4, C5, C6, C7, C8 present as asked; frontmatter `Read, Write` matches every gesture, no unused tool; `Block:` and `Défaut:` shapes match the sondeur's writer and the Rédacteur's reader; the prompt's four file names, output path, and the report-based counts match the command.

| # | Status | Where | One line |
|---|---|---|---|
| C3 | fixed | `.claude-new/agents/assembleur.md` lines 3, 20–21, 44–46 | |
| C6 (NOTE) | fixed | `.claude-new/commands/4_grille.md` lines 396–398, 410–411 | |
| C7 (NOTE, `<out>` vs file path) | fixed | `.claude-new/agents/assembleur.md` lines 237–238 · `.claude-new/commands/4_grille.md` line 422 | |
| C7 (TO FIX, counts source) | fixed | `.claude-new/commands/4_grille.md` lines 484–486 | |
| C8 (NOTE) | fixed | `.claude-new/commands/4_grille.md` lines 197–200 | |
| B.1 | fixed | `.claude-new/agents/assembleur.md` lines 20–21, 44 | |
| B.3 | moot | `.claude-new/agents/assembleur.md` lines 283–285 | The note asked for nothing ("Fine"); the paragraph stands unchanged. |
| C (NOTE, resume overwrite) | moot | `.claude-new/agents/assembleur.md` lines 57–59, 270–271 | The note concluded "No gap"; nothing was asked and the rules it rests on are unchanged. |
| D.1 | fixed | `.claude-new/agents/assembleur.md` lines 44–46, 230–233 | |
| D.2 | fixed | `.claude-new/agents/assembleur.md` lines 146–151, 158–159 | |
| D.3 | fixed | `.claude-new/agents/assembleur.md` lines 161–163 | |
| D.4 | fixed | `.claude-new/agents/assembleur.md` lines 183–184 | |
| D.5 (QUESTION) | fixed | `.claude-new/agents/assembleur.md` lines 187–190 | |
| D.6 (QUESTION) | fixed | `.claude-new/agents/assembleur.md` lines 142–144 | |
| D.7 | fixed | `.claude-new/agents/assembleur.md` lines 254–257 | |
| D.8 | fixed | `.claude-new/agents/assembleur.md` line 3 | |
