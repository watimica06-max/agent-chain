# Verification — `fusionneur.md`

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L3, L24-36 | The index says "two modifications", but the description now announces three invocations and "When you run" was rewritten around `/9_controle` and the Rédacteur's fold-in, so the record understates what the file changed. |
| F02 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L93-94 | The questions file number is now "named by the prompt", where the previous file computed it from the folder, and the index does not mention that hand-over. |
| F03 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L176-179 | The round-trip now has the Fusionneur resolve the answers itself and removes the Rédacteur from it, a change the index does not list. |
| F04 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L191-193, L200-204, L287-290 | The blocking file gained a fifth `## Invocation` heading, a "writes that file and nothing else" rule, and the self-rename was replaced by "the orchestration does it", none of which the index records. |
| F05 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L240, L383-387 | The INIT drop-list and the "never do" list switched from `NEW` marker to `Genre:` and `Global:` lines and dropped the Extracteur reference, unmentioned by the index. |
| F06 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L473-480 | Invocation 3 gained a dependency on `desc-produit-fusion.md` and the folded-in `decisions-produit.md`, with a new "same behaviour said twice" question rule, which the index does not list. |
| F07 | NOTE | refonte | 1 | modifications.md L806 ↔ fusionneur.md L265, L306-308 | The "250 KB" fact and the `## Gaps set aside` alternative were removed, silently as far as the index goes. |
| F08 | NOTE | refonte | 1 | modifications.md L810 ↔ fusionneur.md L509-510 | Modification 2 was asked for the `INSERT` line of invocation 1 and was also extended to invocation 3, which the index does not say. |
| F09 | NOTE | unknown | 3 | fusionneur.md L4 ↔ fusionneur.md L279, L380, L489 | `Glob` is declared but never named, while three gestures (finding the blocked files, the filed questions file, every `bugfix-*/bug-list.md`) need it, and L94 says "you never list a folder", so the agent has no stated way to locate those files. |
| F10 | TO FIX | refonte | 2 | fusionneur.md L24-25 ↔ fusionneur.md L431 | The report is called the Product Owner's "last manual step before the global changes", yet it is "written after applying, never before", so the role statement describes a review that cannot happen. |
| F11 | TO FIX | refonte | 2 | fusionneur.md L473-480 ↔ fusionneur.md L263, L270 | Invocation 3 must carry only what `desc-produit-fusion.md` "does not already carry" and question when the two disagree, but that file is not in its inputs and L270 forbids loading one file more, so the rule cannot be applied. |
| F12 | TO FIX | refonte | 2 | fusionneur.md L159-162, L359-361 ↔ fusionneur.md L399-405, L136-149 | A title question has no plan line among the five verbs and its answer matches none of the three resolutions of invocation 2, so a "rename the section" answer is sent back as ambiguous and no rule ever renames the section. |
| F13 | TO FIX | pre-existing | 2 | fusionneur.md L407-408 ↔ fusionneur.md L262, L91 | An ambiguous answer "goes back as a new question" at invocation 2, whose outputs list no questions file and whose numbering rule gives one file per invocation, so that question has nowhere to be written. |
| F14 | NOTE | pre-existing | 2 | fusionneur.md L383 ↔ fusionneur.md L262, L270 | On `INIT` invocation 2 copies the product file, which is not among its listed inputs while L270 forbids loading anything more. |
| F15 | NOTE | refonte | 2 | fusionneur.md L426-427 ↔ fusionneur.md L240, L385 | Two drop-lists coexist: L426 forbids a block number or `NEW` marker, L240/L385 a block number, `Genre:` or `Global:` line, so the old rule stands beside the new and neither names the full set. |
| F16 | NOTE | pre-existing | 2 | fusionneur.md L279-281, L296 ↔ fusionneur.md L270 | The settled `blocked_fusionneur-NN.md` must be read on every run, while "load only what your invocation lists, not one file more" excludes them. |
| F17 | NOTE | pre-existing | 2 | fusionneur.md L181-182 ↔ fusionneur.md L313-315 | "A question whose answer is recorded is never asked again" cannot be honoured at invocation 1, which is forbidden to open any earlier questions file. |
| F18 | NOTE | refonte | 2 | fusionneur.md L156-157 ↔ fusionneur.md L509-510 | The title check fires "at invocation 1, as you write the `INSERT` line", yet invocation 3 writes no plan and is told the check "applies here too", so where it hangs in invocation 3 is undefined. |
| F19 | BLOCKING | refonte | 4 | fusionneur.md L93-94 ↔ fusion.md L156-160, fusion_compare.md L88-92, fusion_applique.md L79-83 | The questions file number is "named by the prompt — the command has the fact", but none of the three commands passes a number (unlike `3a_genre`, `3b_nature`, `conventions`), and fusion_compare L28-30 still keeps the highest file at the root "it carries the numbering", so the agent has no number and is forbidden to derive one. |
| F20 | BLOCKING | refonte | 4 | fusion.md L47-49 ↔ fusionneur.md L377, L466-519 | After invocation 3 writes its questions file, row 9 (empty or resolved) sends the next run to invocation 2 with no `plan-fusion.md` and row 7 (answered `### Q`) back to invocation 3, so a feature with a `bugfix-*/` folder never reaches invocation 1 and invocation 2 blocks on a missing plan. |
| F21 | TO FIX | refonte | 4 | fusion.md L47 ↔ fusionneur.md L263, L487-519 | Row 7 re-invokes invocation 3 on its own answered questions file, but invocation 3 lists only the bug-lists and the global as inputs and has no step that resolves an answer, so the answers are never applied. |
| F22 | TO FIX | refonte | 4 | fusionneur.md L289-290 ↔ fusion_compare.md L16-21, fusion_applique.md L16-24 | The agent relies on "the orchestration" to rename an applied blocking file, but `/fusion_compare` and `/fusion_applique` neither test for `blocked_fusionneur.md` nor rename it, so a decision applied under those commands leaves the file standing and the next run stops on it. |
| F23 | TO FIX | pre-existing | 4 | fusionneur.md L383 ↔ fusion.md L80-82, redacteur.md L689-690 | INIT orders a whole-file copy of the product file into the global, which the chain elsewhere declares the agent has no tool for and which "truncates in silence", so a first feature is merged by the gesture the rest of the chain forbids. |
| F24 | TO FIX | pre-existing | 4 | fusionneur.md L306-307 ↔ redacteur.md L40-45 | No agent writes a `## Questions set aside` section in the product file, so the skip rule names a section that does not exist and whatever closing section the file does carry is not excluded. |
| F25 | QUESTION | pre-existing | 4 | fusionneur.md L489 ↔ diagnostiqueur.md L44, L560-562 | Invocation 3 reads the Product Owner's raw `bug-list.md` rather than the Diagnostiqueur's `desc-bug.md`, so gaps the diagnosis set aside as already correct or unfound are weighed for merge as if they had been coded. |

Section 1 was worked against the index alone: no pass sheet exists for this agent, so no `C<n>` ↔ `### <n>` numbering could be compared.
Checked and found sound: the two listed modifications are present as asked (L46, L154-170); every announced count (five verbs, four lines, five headings, three levels, three moves, two cases) matches; the blocking file's `## Invocation` heading matches fusion.md row 3; the global's path and `# Application`-only initial state match socle.md; the model passed by the commands matches the frontmatter; no `Bash`.

| # | Status | Where | One line |
|---|---|---|---|
| B-1 | moot | `.claude-new/agents/fusionneur.md` 387–388 | The note asked for nothing — the Extracteur is gone from the chain, and the line stands without it |
| C — rename of the settled blocking file | fixed | `.claude-new/agents/fusionneur.md` 289–290 · `.claude-new/commands/fusion.md` 195–202 | |
| D-1 | fixed | `.claude-new/agents/fusionneur.md` 359–361 | |
| D-2 | fixed | `.claude-new/agents/fusionneur.md` 156–157, 147–149 | |
| D-3 | fixed | `.claude-new/agents/fusionneur.md` 147–149 | |
| D-4 | fixed | `.claude-new/agents/fusionneur.md` 3 | |
| D-5 | fixed | `.claude-new/agents/fusionneur.md` 29–33 | |
| D-6 | fixed | `.claude-new/agents/fusionneur.md` 383–388, 240 | |
| D-7 | fixed | `.claude-new/agents/fusionneur.md` 473–480 · `.claude-new/commands/fusion.md` 46–56 | |
| D-8 | fixed | `.claude-new/agents/fusionneur.md` 510 | |
| D-9 | other | `.claude-new/commands/fusion.md` 9–11, 46–51, 67–73 | cmd 9 says four phases and the specific row now precedes the general one, but the routing question is settled by affirming the path it asked about — an empty invocation-3 file goes to row 9, invocation 2, which cmd 58–61 and agent 117 say needs a plan no invocation wrote |
| D-10 | fixed | `.claude-new/agents/fusionneur.md` 176–179 | |
| D-11 | fixed | `.claude-new/agents/fusionneur.md` 24–25 | |
| D-12 | open | — | |
| D-13 | other | `.claude-new/agents/fusionneur.md` 88–89 | The agent no longer computes its number — the prompt names it — but neither the agent nor the command's prompt template (cmd 161) states what the first run's number is |
| D-14 | fixed | `.claude-new/agents/fusionneur.md` 306–308 | |
| D-15 | fixed | `.claude-new/agents/fusionneur.md` 53 | |
