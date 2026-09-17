# decoupeur.md — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | TO FIX | refonte | 1 | modifications.md L312 ↔ decoupeur.md L26-45 | C4 is listed ÉCARTÉ with the argument that the agent's stop on `**Clarification needed:**` is a different perimeter worth keeping, yet the paragraph is gone from the file (zero occurrences), so the index records as kept a rule that was removed. |
| F02 | TO FIX | refonte | 1 | modifications.md L313 ↔ decoupeur.md L124-126 | C9 is listed ÉCARTÉ, yet its ask is in the file — split blocks written first, the blocking file names the block stopped on, a rerun starts from there — so the index says the opposite of what the file holds. |
| F03 | NOTE | refonte | 1 | modifications.md L315 ↔ 3_decoupe.md L99-127 | C1 is listed REPORTÉ because reordering one command would create two forms, yet `/3_decoupe` was reordered (git section split and moved before the invocation), so either the index is stale or the two forms it wanted to avoid now exist. |
| F04 | NOTE | refonte | 1 | passes/decoupeur.md L335-360 ↔ 3_decoupe.md L69-70, L202-205 | C14 is listed PASSÉ but applied differently: the command still hands a first turn every block with no ceiling, and bounds the sweep after the fact by re-invoking on the short list twice at most. |
| F05 | NOTE | refonte | 1 | decoupeur.md L4 ↔ modifications.md L294-338 | `Glob` was removed from the tools between the two rounds, and no line of the index records it. |
| F06 | NOTE | refonte | 1 | decoupeur.md L186-190 ↔ modifications.md L294-338 | The edit-in-place rule — one targeted edit per block, never a whole write — is new and no comment or index line asks for it. |
| F07 | NOTE | refonte | 1 | decoupeur.md L61-67 ↔ modifications.md L54 | "A constraint the Product Owner imposed" was added to what nothing sets off, with a rule tied to the qualifieur's genre, and the index's only line for this file says it writes `Genre:` empty. |
| F08 | TO FIX | refonte | 2 | decoupeur.md L146-147 ↔ L149-151, L51 | The two-events-one-consequence sentence "sits whole in one block" and yet "carries two triggers" that "you split without rewording", so the agent cannot tell which of the two trigger blocks receives it, and whichever it picks breaks "a block carries one trigger". |
| F09 | TO FIX | refonte | 2 | decoupeur.md L92-96 ↔ L40-45 | Recognising a block "whose only trigger is the sequel of another block's" requires reading that other block, which a turn naming blocks forbids ("you read those blocks, not the file"), so on every later turn the rule and its report line cannot fire. |
| F10 | NOTE | refonte | 2 | decoupeur.md L153-156 ↔ L139-143 | The only blocking cause resumes by a rewording that is not the agent's, so a filled `## Decision` the prompt names gives the agent a decision it may not apply — the resume branch leads nowhere. |
| F11 | NOTE | refonte | 2 | decoupeur.md L37-38 ↔ L45 | The first turn is a prompt that "names none" at L37 and "a turn that names every block" at L45, so the one rule that allows a whole-file read hangs on a phrasing the file elsewhere says never occurs. |
| F12 | NOTE | refonte | 2 | decoupeur.md L197-199 ↔ L204, L233 | The enumeration of what each half carries omits `Global:`, the format example shows one unconditionally, and L233 makes it conditional, so an agent imitating the example adds a `Global:` line to halves whose original carried none. |
| F13 | TO FIX | refonte | 4 | decoupeur.md L248-249 ↔ 3_decoupe.md L193-218 | The agent must report every block whose only trigger is another block's sequel, and the command's relay has no row for it, so the one signal that two blocks carry one behaviour reaches nobody. |
| F14 | TO FIX | refonte | 4 | 3_decoupe.md L202-203 ↔ 3_decoupe.md L220, decoupeur.md L125-126 | A blocking file always comes with a short list (the agent stops on the block), and the command both re-invokes on the unreached blocks and "relay[s] it and stop[s]", so the orchestrator has two contradictory next steps on every block. |
| F15 | NOTE | unknown | 4 | 3_decoupe.md L39, L136, L151-157 ↔ 2_structure.md L191-194 | `/2_structure` consumes and renames `blocked_decoupeur.md` before `/3_decoupe` runs again, so the command's filled-Decision row, the prompt's third line and the post-run `git mv` never fire. |
| F16 | NOTE | pre-existing | 4 | decoupeur.md L217 ↔ redacteur.md L104-105 | The kept half of a `NEW` original becomes `MODIFIED` while the Rédacteur keeps `NEW` on a changed `NEW` block, a disagreement on marker meaning that costs nothing while `/4_grille` L114 takes the union of both greps. |
| F17 | NOTE | pre-existing | 4 | classeur.md L181, qualifieur.md L214 ↔ decoupeur.md L110 | Both say merging two blocks "is the decoupeur's" and the decoupeur says a merge "is not yours", so a merge belongs to no agent in the chain. |
| F18 | NOTE | refonte | 4 | decoupeur.md L126 ↔ 3_decoupe.md L77-91 | "A rerun starts from there" asserts the blocking file drives the rerun's list, but the command builds it from the marker greps alone and never reads the blocking file's block. |

Checked and found sound: the frontmatter against every gesture (section 3); C2, C3, C5, C6, C7, C8, C10, C11, C12, C13, C15, C16, C17 against the file and the command; the block form, the `Global:` line, the `## Decision` heading, the blocking-file location, the `/3a_genre` routing and the emptied `Genre:`/`Nature:` lines against redacteur, sondeur, qualifieur, classeur, 3a_genre and 3b_nature.

| # | Status | Where | One line |
|---|---|---|---|
| C3 | fixed | `.claude-new/agents/decoupeur.md:120–121` | |
| C8 | fixed | `.claude-new/commands/2_structure.md:120`, `.claude-new/agents/redacteur.md:533` | |
| C12 | open | — | |
| C14 | other | `.claude-new/commands/3_decoupe.md:69–70, 202–205` | No ceiling, no range, no sequential invocation on a first turn — instead a re-invocation on the blocks not reached, twice at most |
| C15 | moot | `.claude-new/commands/3_decoupe.md:51` | The NOTE asked nothing of this command — the `NN` rule belongs to the agents that write `questions-<agent>-NN.md`, per the report itself |
| C16 | fixed | `.claude-new/commands/3_decoupe.md:26–27` | |
| B-1 | fixed | `.claude-new/agents/decoupeur.md:61–63, 173–176` | |
| B-2 | open | — | |
| B-3 | open | — | |
| B-4 | open | — | |
| B-5 | fixed | `.claude-new/commands/3_decoupe.md:72–75`, `.claude-new/agents/redacteur.md:119–126` | |
| C-1 | fixed | `.claude-new/agents/decoupeur.md:186–190` | |
| C-2 | fixed | `.claude-new/agents/decoupeur.md:4` | |
| D-1 | fixed | `.claude-new/agents/decoupeur.md:139–147` | |
| D-2 | fixed | `.claude-new/agents/decoupeur.md:145–151` | |
| D-3 | fixed | `.claude-new/agents/decoupeur.md:61–63, 173–176` | |
| D-4 | moot | `.claude-new/agents/decoupeur.md` | The `Clarification needed` stop is gone from the agent; only the command's grep stops on it (`3_decoupe.md:44–47`), so no reply outcome and no relay row remain to write |
| D-5 | fixed | `.claude-new/agents/decoupeur.md:79` | |
| D-6 | fixed | `.claude-new/agents/decoupeur.md:92–96, 248–249` | |
| D-7 | fixed | `.claude-new/agents/decoupeur.md:120–121` | |
| D-8 | other | `.claude-new/agents/decoupeur.md:32, 45, 100, 173` | Line 32 now says "open", settling the read/read pair; "whole" still names the file at 45 and the block at 100 and 173 |
| D-9 | other | `.claude-new/agents/decoupeur.md:197–199, 212–218` | The `MODIFIED` exception is now stated inside the "Each" rule; the `NEW` original whose kept half is stamped `MODIFIED` is still unsettled |
| D-10 | moot | `.claude-new/agents/decoupeur.md:135–151` | D-1 is fixed, and the second paragraph now says outright that it does not block — the count of one case holds |
| D-11 | open | — | |
| D-12 | fixed | `.claude-new/commands/3_decoupe.md:202–205` | |
