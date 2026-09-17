# lexicographe — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | lexicographe.md L3 ↔ modifications.md L22-23 | The frontmatter description was changed — its "then on every answered questions file…" clause is now written twice end to end — and the index names no comment or session decision behind it, so the registry entry the orchestrator reads says the same thing twice. |
| F02 | NOTE | refonte | 1 | lexicographe.md L110-113 ↔ modifications.md L27-29 | The numbering rule changed from "the root, or the archive if the root holds none" to "root and archive together, own prefix only" — a change no passed comment asks for and the index does not mention. |
| F03 | NOTE | refonte | 1 | lexicographe.md L417-423 ↔ modifications.md L27-29 | Invocation 3 now sweeps the `Défaut:` line of every unanswered entry — a new move no comment of the pass sheet asks for and the index does not list. |
| F04 | NOTE | refonte | 1 | lexicographe.md L104, L454-458 ↔ passes/lexicographe.md L72-79 | Invocation 3 now writes its doubts into `## Non tranché`, where C1 only asked it to compare against `## Relevé`; the index records this widening nowhere. |
| F05 | TO FIX | refonte | 2 | lexicographe.md L375-380 ↔ L431-439 | Invocation 2 retires a term for one of its meanings only and the `## Tranché` shape has no way to say so, so invocation 3's blanket rule — every `remplace :` term swapped, "the decision is made" — re-merges in the answers the two meanings the answer had just told apart. |
| F06 | TO FIX | refonte | 2 | lexicographe.md L417-420 ↔ L66-68, L431-433 | Invocation 3 must sweep an accepted `Défaut:` line whose terms "entered the product exactly as an answer's do", but the retired-term swap runs on the answers alone and the write list allows only `Answer:` fields, so a retired term or an unquoted label in an accepted proposal reaches the Rédacteur unchanged. |
| F07 | TO FIX | refonte | 2 | lexicographe.md L104 ↔ L504-509 | The invocation table says 3 updates `## Non tranché`, but invocation 3's own "What you write" and its Outputs line name `## Relevé` only, so an agent following its section leaves the doubts out of the lexicon, the command's count of what waits sees nothing, and invocation 4 is sent to move a term that was never there — the failure L457 itself warns of. |
| F08 | NOTE | pre-existing | 2 | lexicographe.md L549-552 ↔ L191-193, L457 | Invocation 4's move 3 says "add each settled term to `lexique.md`" where invocation 2 says "move it out of `## Non tranché`", so a settled pair can stay listed under `## Non tranché` and be counted by the command as still waiting after its answer was applied. |
| F09 | NOTE | refonte | 2 | lexicographe.md L211-212 ↔ L354 | The lexicon's reader list names invocations 1, 3 and 4 while invocation 2 now reads it too, so the one statement of who reads the file is short by one. |
| F10 | NOTE | refonte | 2 | lexicographe.md L199-204, L285-287 ↔ L36-37 | The rule that a sweep keeps the `(réponse)` terms of `## Relevé` governs a case that cannot occur — only invocations 3 and 4 add them, after the product file exists, and invocation 1 never runs again — so the rule and its marker are dead weight in the sweep. |
| F11 | TO FIX | refonte | 4 | 1_lexique.md L61 ↔ lexicographe.md L105, L515-517 | The command's row "another agent's file and `questions-lexicographe` → 4" carries no "with `### Q`" guard, so a `/1_lexique` rerun after 3 asked nothing (both files at the root, the relay saying `/2_structure`) invokes an invocation the agent is told never to run, at the cost of an opus call and a commit/worktree/merge/push cycle. |
| F12 | NOTE | refonte | 4 | lexicographe.md L176-177 ↔ redacteur.md L169-170 | The lexicographe says the Rédacteur writes `en anglais` "on a concept you settled" while the Rédacteur also writes it under a `## Relevé` line of a never-questioned term, so the lexicographe's description of its own file misses a line shape it will find there. |
| F13 | NOTE | refonte | 4 | redacteur.md L320-322 ↔ lexicographe.md L3 | The Rédacteur's never-do list says "the vocabulary is the qualifieur's" while the vocabulary agent is the lexicographe and `qualifieur.md` says nothing of vocabulary, so the one reader of the lexicon is pointed to the wrong owner of it. |

Checked and found sound: C1–C14 each present as asked, C15–C17 absent as recorded, `C<n>` ↔ `### <n>` aligned; the five frontmatter tools each carry a gesture and every gesture has its tool; the command's prompt slots, `## Non tranché` count, `^### Q` count and relay rows, the `Question:`/`Answer:` shape of every producer's questions file, and the convertisseur's separate `technique-*.md` route.

| # | Status | Where | One line |
|---|---|---|---|
| A/C3 | other | `.claude-new/agents/lexicographe.md` 314–334 | 323–334 now lists every occurrence, grouped and tagged by section (`§B3`), but 314–316 still says "one occurrence of each, with its sentence" |
| A/C14(b) | fixed | `.claude-new/commands/1_lexique.md` 93–95 | |
| A/C14 adjacent | fixed | `.claude-new/commands/1_lexique.md` 82–83, 246–247 | |
| A/C15 | open | — | |
| B.1 | open | — | |
| B.2 | open | — | |
| B.3 | moot | `.claude-new/agents/lexicographe.md` 211–212 | The note asked nothing — it recorded a correct change, unchanged |
| D.1 | fixed | `.claude-new/agents/lexicographe.md` 402–403 | |
| D.2 | fixed | `.claude-new/agents/lexicographe.md` 450–451 | |
| D.3 | fixed | `.claude-new/agents/lexicographe.md` 378–383 | |
| D.4 | fixed | `.claude-new/agents/lexicographe.md` 431–439 | |
| D.5 | fixed | `.claude-new/agents/lexicographe.md` 104 | |
| D.6 | fixed | `.claude-new/agents/lexicographe.md` 454–458 | |
| D.7 | fixed | `.claude-new/agents/lexicographe.md` 549–550 | |
| D.8 | fixed | `.claude-new/agents/lexicographe.md` 202–204 | |
| D.9 | fixed | `.claude-new/agents/lexicographe.md` 531–534 | |
| D.10 | fixed | `.claude-new/agents/lexicographe.md` 87–89 | |
