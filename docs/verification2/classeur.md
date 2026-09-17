# classeur — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L57 ↔ classeur.md L267 | The index records only that the Classeur knows every named block carries `Genre: comportement`; the file also carries the opposite case — a named block whose genre is no longer `comportement`, whose line it empties (L267, L295-300) — and no entry of the index or the pass sheet mentions that change. |
| F02 | QUESTION | refonte | 1 | passes/classeur.md L74-79 ↔ classeur.md L93 | C2 asked that a user-action block take the nature of what the action produces, with only the perceived part `presentation`; it was applied as a frontier that declares a block describing both a product and a visible response badly split and sends it to doubt 1, so every "tap → state change + feedback" block becomes a Product Owner question — the round-trip cost C2 cited as its defect. |
| F03 | NOTE | refonte | 1 | passes/classeur.md L139-141 ↔ 3b_nature.md L44-47 | C5 asked the agent to hold the numbering rule (highest `questions-classeur-NN` anywhere, plus one, `01` if none); it was applied by moving the rule into the command and removing `Glob` from the agent, which now receives its number in the prompt (L125) — a different mechanism than the one listed as passed. |
| F04 | NOTE | refonte | 3 | classeur.md L4 ↔ classeur.md L179 | "One targeted edit per `Nature:` line" names no anchor, and an empty `Nature:` is not unique in the product file, so an `Edit` on the bare line fails on ambiguity or, with replace-all, fills every empty block at once; the heading and `Genre:` lines have to be part of the edit and nothing says so. |
| F05 | TO FIX | refonte | 2 | classeur.md L34-37 ↔ classeur.md L267 | L34-37 state that every block the prompt names carries `Genre: comportement` and that the command names no other, while L267 and L295-300 give a procedure for a named block whose genre is no longer `comportement`; an agent holding the first rule skips or re-classes the block instead of emptying its line. |
| F06 | TO FIX | refonte | 2 | classeur.md L169 ↔ classeur.md L223-227 | L169 adds a third cause of blocking (the same doubt left open by two answers) while L223-227 still enumerate blocking as "no nature fits at all" and say "a doubt is a question", so the two rules contradict on the case they share. |
| F07 | TO FIX | refonte | 2 | classeur.md L146 ↔ classeur.md L171 | The prompt names one answered file, last turn's, yet L171 orders both answers into the blocking file, and the first answer sits in a file filed a turn earlier that the agent is never given — it can only paraphrase it from its own question text. |
| F08 | TO FIX | refonte | 2 | classeur.md L233-235 ↔ classeur.md L253-254 | One blocking file may hold several `## Decision` headings settled separately, yet L254 assumes the agent is never called on an empty decision; an entry still open beside a filled one has no rule — the agent either waits, re-blocks it, or treats it as settled. |
| F09 | NOTE | refonte | 2 | classeur.md L237 ↔ classeur.md L319-331 | Three rules order things into the report — the blocked blocks' names (L237), "waits on the Rédacteur" (L246), "cannot write a value outside the eight" (L247) — and the report section that closes the file lists counts, per-block natures and asked identifiers only, so the agent following that section drops them. |
| F10 | NOTE | refonte | 2 | classeur.md L3 ↔ classeur.md L35 | The description says the agent runs after the decoupeur while L35 says the qualifieur ran before it; the description is what the orchestrator sees when picking the agent, and it now names the wrong predecessor. |
| F11 | NOTE | pre-existing | 2 | classeur.md L115 ↔ classeur.md L181 | Doubt 1's answer settles "whether the Rédacteur splits it" while L181 says splitting "is the decoupeur's"; two agents are named as the one that splits, and the questions file's reader is left to guess which. |
| F12 | TO FIX | refonte | 4 | classeur.md L146 ↔ 3b_nature.md L49-53 / L67-69 | The command names the root answered file in the prompt (L49-53), then stops before invoking on any root questions file holding `### Q` (L67-69) — which an answered file always does — so the agent's whole answered-questions path (L144-172) is reached only by breaking one of the command's two rules; L71-72 further say a filed file is read by no command again, against L50 naming one under `questions/classeur/`. |
| F13 | TO FIX | refonte | 4 | classeur.md L233-235 ↔ 3b_nature.md L38-39 | The agent writes one `## Decision` per blocked block and the command reads "its `## Decision`" as a single heading (also 2_structure.md L120-121), so a file with one filled and one empty decision is either named to the agent half-settled or stops the command with a filled decision unread. |
| F14 | NOTE | refonte | 4 | classeur.md L300 ↔ 5_reclasse.md L64-70 | The agent is told a later command stops on a filled `Nature:` under a non-`comportement` genre; `/5_reclasse` stops only on an empty line under `comportement` and on a value outside the eight, so the emptying rule's stated reason is false (3b_nature.md L97 carries the same claim). |
| F15 | NOTE | refonte | 4 | classeur.md L246-247 ↔ 3b_nature.md L223-227 | The two report lines the agent must write on a decision it cannot apply, and the blocked blocks' names (L237), are not in the command's relay list, which ends "Nothing else is yours"; they are produced and dropped, and the Product Owner learns of a block waiting on the Rédacteur only from the routing table. |
| F16 | NOTE | refonte | 4 | classeur.md L246 ↔ 3b_nature.md L161-164 | When a rewrite decision comes through `/3b_nature`, the command files the blocking file as `blocked_classeur-NN.md` after the agent reports, and `/2_structure` (L120) looks only for the unnumbered name, so the block the agent reports as "waiting on the Rédacteur" reaches no Rédacteur unless the Product Owner ran `/2_structure` first. |
| F17 | NOTE | refonte | 4 | classeur.md L49-51 ↔ redacteur.md L59-62 | The block form the agent is given ends "`Nature:` on the one after, then the block's sentences", while the Rédacteur writes an optional `Global:` line between them; harmless for the one line the agent edits, but the delimitation it is told is not the one written. |

Checked and found sound: C1, C3, C4, C7, C8, C9, C10 (partial), C11–C14 present as listed; the C<n>/### <n> numbering matches across index and pass sheet; every tool in the frontmatter has a gesture and every gesture a tool, the removed `Glob` has no surviving listing gesture; the counts "eight", "three doubts", "four lines", "four headings", "three shapes" all match; the command's prompt carries the five inputs the agent's rules name.

| # | Status | Where | One line |
|---|---|---|---|
| C3 | fixed | agents/classeur.md:78, 91 | |
| C5 | moot | agents/classeur.md:125 | The agent no longer numbers its file — the prompt carries `NN`, and the command computes it with the `01` clause (commands/3b_nature.md:43–46) |
| C12 | fixed | commands/3b_nature.md:172 | |
| B-1 | open | agents/classeur.md:253 | |
| B-2 | other | agents/classeur.md:78, 91 | The third phrasing stays, now in both rows — C3's alignment met by moving the frontier row to it |
| B-3 | open | agents/classeur.md:80 | |
| B-4 | open | agents/classeur.md:93 | |
| B-5 | moot | agents/classeur.md:125 | The number rule is gone — the prompt names `NN` |
| B-6 | open | agents/classeur.md:41 | |
| B-7 | fixed | agents/classeur.md:63–66 | |
| B-8 | open | agents/classeur.md:50 | |
| B-9 | fixed | agents/classeur.md:143 | |
| B-11 | other | agents/classeur.md:166–172 | The follow-up question stays as a third exit, now capped — two unsettled answers on one block and the agent blocks |
| B-12 | fixed | agents/classeur.md:260 | |
| B-13 | fixed | agents/classeur.md:249–251 | |
| B-14 | open | agents/classeur.md:237 | |
| B-15 | fixed | agents/classeur.md:324 | |
| B-16 | fixed | agents/classeur.md:329 | |
| D-1 | fixed | agents/classeur.md:182 | |
| D-2 | fixed | agents/classeur.md:184 · 153 · 269 | |
| D-3 | fixed | agents/classeur.md:196 · 233 | |
| D-4 | fixed | agents/classeur.md:50 · commands/3b_nature.md:95 | |
| D-5 | fixed | agents/classeur.md:78, 91 | |
| D-6 | fixed | agents/classeur.md:324 | |
| D-7 | other | agents/classeur.md:3 | The conditional "when a block produces two different things" is gone ("on every run, empty or not"); still silent on the answered file and the `Genre:` precondition |
| D-8 | fixed | agents/classeur.md:272–274 | |
| D-9 | fixed | agents/classeur.md:93 | |
| D-10 | fixed | agents/classeur.md:247 | |
| D-11 | moot | agents/classeur.md:125 | Same as C5 — the numbering rule left the agent |
| D-12 | fixed | agents/classeur.md:169 | |
