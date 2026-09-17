# cadreur — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | pre-existing | 1 | cadreur.md L266 ↔ modifications.md L947 | C21 is listed PASSÉ, yet "moves 3 and 4 are not re-run" still stands at L266, L309, L863 and L935, the three-round ceiling at L24, L260, L822 and L931, "do not argue with a defect" at L274, L828 and L852 — the never-do list is still a second statement, not the index the comment asked for. |
| F02 | TO FIX | pre-existing | 1 | cadreur.md L524 ↔ modifications.md L962 | C11 is listed PASSÉ but was applied only in *What you write* and move 8: move 6 still sends "every code file in a symbol's hit list" into `Modifies` by name. |
| F03 | NOTE | refonte | 1 | cadreur.md L397 ↔ modifications.md L946 | Move 1 and the blocking list now grep and block on a `[B?:` reference; none of the 26 comments asks for it and the index does not mention the change. |
| F04 | NOTE | refonte | 1 | cadreur.md L37 ↔ modifications.md L946 | The section *How you find a numbered file* and the round count "archived `code/sequence-NN.md` files plus the round you are in" (L822) come from no comment and the index does not mention them. |
| F05 | TO FIX | refonte | 2 | cadreur.md L295 ↔ cadreur.md L954 | Dispatch row 1 fires on any filled `## Verdict` in `architecte/cadreur.md`, while block D says the block's `## Where` must name that request; an answered request kept from an earlier run (L223-225) then lifts every later block, a third-round one included, with a verdict that never answered it. |
| F06 | TO FIX | refonte | 2 | cadreur.md L297 ↔ cadreur.md L949 | "D, then dispatch again on what remains" re-reads the same table with the decided file still on disk (you never rename it), so the row that just fired matches again and nothing says which rows the second dispatch skips. |
| F07 | TO FIX | refonte | 2 | cadreur.md L128 ↔ cadreur.md L951 | A block raised after D in the same run (move 1, a third round) writes `code/blocked_cadreur.md` over the file that still holds the Product Owner's `## Decision`, before the command has renamed it: the decision is lost and the new block is what gets archived as settled. |
| F08 | TO FIX | pre-existing | 2 | cadreur.md L524 ↔ cadreur.md L753 | Move 6 puts code files into `Modifies` by name; *What you write* says `Modifies` carries symbols only, never a file: the collision rule the split rests on is checked on a field whose unit the agent cannot settle. |
| F09 | NOTE | refonte | 2 | cadreur.md L24 ↔ cadreur.md L798 | "One invocation per round of the split" against "you do not go out between rounds": `round` names the Vérificateur loop in one place and a cadreur invocation in the other, so a reader cannot tell whether three rounds means three invocations. |
| F10 | NOTE | refonte | 2 | cadreur.md L331 ↔ cadreur.md L333 | "See *What a bug-fix cycle changes*" points at a section that does not exist; the material sits under "On a bug-fix cycle:" two lines below, unnamed. |
| F11 | NOTE | refonte | 2 | cadreur.md L264 ↔ cadreur.md L397 | The never-do entry forbids any grep outside the code folders the conventions name, and move 1 greps the technical document: the first move of every run breaks the list an agent reads last. |
| F12 | NOTE | refonte | 2 | cadreur.md L106 ↔ cadreur.md L113 | The Vérificateur is said to count "entries cited per block, not symbols per lot", then "its own ceilings say how many" lots a block holds: two units for one ceiling in seven lines. |
| F13 | NOTE | refonte | 2 | cadreur.md L355 ↔ cadreur.md L333 | "A blocking case, as it is on a bug fix" is written inside the bug-fix section itself, so the sentence compares the case to itself and the feature-cycle rule it meant (L79) is not what it points to. |
| F14 | NOTE | refonte | 2 | cadreur.md L44 ↔ cadreur.md L295 | "Glob `code/` once and route on what is there" cannot see `architecte/cadreur.md`, which the first dispatch row tests; a reader who obeys the glob rule never reaches row 1. |
| F15 | NOTE | refonte | 2 | cadreur.md L145 ↔ cadreur.md L822 | "The third round did not converge — see there" names no section. |
| F16 | NOTE | pre-existing | 2 | cadreur.md L828 ↔ cadreur.md L852 | "Do not argue with a defect" is given two outcomes — say so in the blocking file at L829, "stop and report" at L853 — and the second is a stop with no file, which L149-151 says is invisible to the command. |
| F17 | TO FIX | refonte | 4 | cadreur.md L818 ↔ verificateur.md L206 | The return row tests a `code/blocked_verificateur.md` "with an empty `## Decision`", and the Vérificateur's file carries no `## Decision` heading (7_lots.md L83 says the same): the row never matches as written and the cadreur reads a `code/sequence.md` that is not there. |
| F18 | TO FIX | refonte | 4 | cadreur.md L822 ↔ verificateur.md L96 | The round count is "archived `code/sequence-NN.md` files plus the round you are in", and nothing in `.claude-new/` archives one — the Vérificateur reads the previous round's `code/sequence.md` in place, 7_lots.md renames only `redecoupage.md`: the on-disk term is always zero, the ceiling is per invocation, and a take-back from cold (B) restarts at round one. |
| F19 | TO FIX | refonte | 4 | cadreur.md L753 ↔ detailleur.md L260 | `Modifies` carries symbols only, never a file, and the Détailleur copies `Modifies` and `Touches` into `## Files` as "one path per line": a symbol name is not a path, and the downstream checks keyed on `## Files` never match it. |
| F20 | TO FIX | refonte | 4 | cadreur.md L961 ↔ 7_lots.md L144 | On a refused verdict the cadreur "says so and goes out"; the command's row "filled `## Verdict` → invoke `cadreur`" then fires again on the same disk: the two loop until the orchestrator breaks off, and no row relays the refusal to the Product Owner. |
| F21 | TO FIX | refonte | 4 | cadreur.md L960 ↔ 7_lots.md L146 | A block lifted by an accepted verdict is never closed: the cadreur never touches the file (L949) and the command renames only when the cadreur "reports it applied a decision", so `code/blocked_cadreur.md` stays with an empty `## Decision`, every later run re-applies the verdict through dispatch row 1, and every audit lists a block still standing. |
| F22 | NOTE | refonte | 4 | cadreur.md L970 ↔ 7_lots.md L146 | The command's rename is triggered by the cadreur "reporting it applied a decision", and no line of the cadreur says to state that in its report. |
| F23 | QUESTION | pre-existing | 4 | cadreur.md L859 ↔ cycle.md L88 | cycle.md still resumes a cadreur block through `/7_decoupe`, which is not in `.claude-new/commands/`; the index discards C26 as obsolete by decision — is cycle.md itself retired, or does the route still have to read `/7_lots`? |

Sound: section 3 whole — every tool has a gesture (Glob L39, Grep L384, Read L372, Edit L278, Write L128, Agent L804) and no gesture lacks one; C1–C10, C12–C20, C22–C25 found in place, C26 absent as the index says, `C<n>` ↔ `### <n>` aligned.
Sound across the chain: `code/<lot>/verdict.md`, `## Redécoupage: archivable`, the defect's first field and `orphan`, the six layer names, `code/redecoupage.md` written by the Arbitre, 9_controle reading `## Entries with no lot`, both `Working folder:` prompts, `architecte/cadreur.md` in audit_conventions.

| # | Status | Where | One line |
|---|---|---|---|
| C1 | fixed | `agents/cadreur.md` L24-27, L293-300, L946-947 | |
| C3 | fixed | `agents/cadreur.md` L295, L954-961 | |
| C4 | fixed | `agents/cadreur.md` L159-164, L219-221 | |
| C6 | fixed | `agents/cadreur.md` L323-326, L600 | |
| C7 | fixed | `agents/cadreur.md` L239-240, L464-467, L693-694, L354-356 | |
| C9 | fixed | `agents/cadreur.md` L86-87 | |
| C10 | fixed | `agents/cadreur.md` L607-609 | |
| C11 | fixed | `agents/cadreur.md` L524-525, L530-533, L650-651 | |
| C13 | fixed | `agents/cadreur.md` L440, L790-791 | |
| C14 | fixed | `agents/cadreur.md` L426-434, L484-486, L511-536 | |
| C17 | fixed | `agents/cadreur.md` L628, L676-681 | |
| C19 | fixed | `agents/cadreur.md` L309-313, L834-837, L863-864, L931-936 | |
| C20 | fixed | `agents/cadreur.md` L544-549 | |
| C21 | other | `agents/cadreur.md` L515-517 | The "measured: five test files" anecdote is gone; the duplicated rules stay (three rounds L27/L260/L822/L931, unbounded wait L259/L811, argue with a defect L274/L828/L852, moves 3-4 not re-run L266/L309/L863/L935, blocking file first L302/L942) and the file grew 906 → 973 lines |
| C22 | fixed | `agents/cadreur.md` L264-269 | |
| B-1 | fixed | `agents/cadreur.md` L101-107 | |
| B-2 | fixed | `agents/cadreur.md` L105-107 | |
| B-3 | moot | `agents/cadreur.md` L113-117 | The note asked for no change; both sentences stand as recorded |
| C — Glob unnamed | fixed | `agents/cadreur.md` L37-45 | |
| D-1 | fixed | `agents/cadreur.md` L24-27 | |
| D-2 | fixed | `agents/cadreur.md` L86-87 | |
| D-3 | fixed | `agents/cadreur.md` L191-193, L295, L954-961 | |
| D-4 | fixed | `agents/cadreur.md` L323-326 | |
| D-5 | fixed | `agents/cadreur.md` L354-356 | |
| D-6 | fixed | `agents/cadreur.md` L333 | |
| D-7 | fixed | `agents/cadreur.md` L266-269, L309-313, L863-864, L935-936 | |
| D-8 | fixed | `agents/cadreur.md` L264-269 | |
| D-9 | fixed | `agents/cadreur.md` L511-536 | |
| D-10 | fixed | `agents/cadreur.md` L426-429 | |
| D-11 | fixed | `agents/cadreur.md` L478-479 | |
| D-12 | fixed | `agents/cadreur.md` L607-609 | |
| D-13 | other | `agents/cadreur.md` L628 | The row now carries a test and says "block" instead of "report", but the case — an entry no lot of any layer can carry — is still absent from the blocking list L135-147 |
| D-14 | fixed | `agents/cadreur.md` L600 | |
| D-15 | fixed | `agents/cadreur.md` L524-525, L650-651, L759-762 | |
| D-16 | fixed | `agents/cadreur.md` L790-791 | |
| D-17 | fixed | `agents/cadreur.md` L219-221 | |
| D-18 | fixed | `agents/cadreur.md` L949-952, L970-973 | |
| D-19 | fixed | `agents/cadreur.md` L270, L879 | |
| D-20 | fixed | `agents/cadreur.md` L299 | |
| D-21 | open | — | |
| D-22 | moot | `agents/cadreur.md` L818 | The row no longer tests for the absence of `code/sequence.md` — it tests only `code/blocked_verificateur.md` with an empty `## Decision`, so what the Vérificateur does to the old sequence no longer matters to it |
| D-23 | open | — | |
| D-24 | fixed | `agents/cadreur.md` L161-162 | |
| D-25 | fixed | `agents/cadreur.md` L822-826 | |
