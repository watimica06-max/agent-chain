# detailleur.md — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L1013-1082 ↔ detailleur.md L244-248, L259-265 | The sheet gained a `## Files` field with its own rule, and the index lists no comment for it. |
| F02 | NOTE | refonte | 1 | modifications.md L1013-1082 ↔ detailleur.md L638-646 | Move 9 now keeps `spécifique` rules and drops `permanente` ones where the old file kept the 🔴 ones, and the detailleur section of the index says nothing of it (only the architecte section, L638, names the mark). |
| F03 | NOTE | refonte | 1 | modifications.md L1013-1082 ↔ detailleur.md L109 | The contradiction table gained a row for a production found with an empty body, and the index does not mention it. |
| F04 | NOTE | refonte | 1 | modifications.md L1013-1082 ↔ detailleur.md L438 | PART 2 gained a row for a `## Decision` reading `Not settled here.`, and the index does not mention it. |
| F05 | NOTE | refonte | 1 | modifications.md L1013-1082 ↔ detailleur.md L558-560 | Move 3 gained a rule for a `desc-bug.md` with no `Vocabulary`, and the index does not mention it. |
| F06 | NOTE | refonte | 1 | passes/detailleur.md L50-66 ↔ detailleur.md L443-444 | C1 is listed PASSÉ, but applied differently: the pass asked for one agent-side rule (rename to the numbered form, never delete), the file instead says the agent never renames and the orchestration does. |
| F07 | NOTE | refonte | 1 | modifications.md L1038 ↔ detailleur.md L460 | C4 is listed PASSÉ with "two of its three block causes show only at grep", and the file says "One of your three block causes shows only in a grep". |
| F08 | NOTE | pre-existing | 1 | passes/detailleur.md L237-252 ↔ detailleur.md L546-547 | C8 is listed PASSÉ, but only half applied: move 4 gained its two greps, and move 2 still carries the forward reference "the rest of that file you grep, symbol by symbol" the comment asked to remove. |
| F09 | NOTE | refonte | 1 | passes/detailleur.md L416-436 ↔ detailleur.md L246-248 | C17 is listed PASSÉ (one platform's vocabulary out of the examples), yet the refonte added a `## Files` example made of three `.kt` paths. |
| F10 | NOTE | unknown | 1 | modifications.md L1027-1031 ↔ 8_code.md L103-106, L395-397, L12 | C19, C20 and C21 are listed REPORTÉ, and the three changes are in `8_code.md` (test on the lot, row for a block waiting on the split, Contrôleur never invoked). |
| F11 | NOTE | pre-existing | 3 | detailleur.md L4 ↔ detailleur.md L415-421 | `Edit` is in the tools and no gesture names it — every production is a Write — so the only thing it stands for is the failure section, and nothing says what it may and may not touch. |
| F12 | NOTE | refonte | 3 | detailleur.md L45 ↔ detailleur.md L467-468 | The walk keys on a lot's verdict being `PASS`, read from "its `## Status` line", and no tool is named for that one line — a Read opens the whole verdict, `## Findings` included, which nothing bounds. |
| F13 | TO FIX | refonte | 2 | detailleur.md L221-222 ↔ detailleur.md L224-257 | The sheet is announced as "five fields" and the shape shows six (`## Files` was added without the count), so an agent that trusts the count drops one. |
| F14 | NOTE | pre-existing | 2 | detailleur.md L288-290 ↔ detailleur.md L571-574, L590, L592 | The block causes are enumerated as three, and move 4 orders three more stops (no code folder in the conventions, a symbol an earlier block promised, a symbol nothing places), so "one of your three shows only in a grep" undercounts what the walk's grep is there to catch. |
| F15 | TO FIX | refonte | 2 | detailleur.md L525-526 ↔ detailleur.md L680-681 | Divergence mode runs moves 3 to 9 and not the walk, yet moves 1 and 2 run "in the walk" — so move 3 derives signatures from "those entries" and move 7 rewrites criteria from their assertions with no entry opened, and the state document's traps are never read. |
| F16 | TO FIX | refonte | 2 | detailleur.md L346 ↔ detailleur.md L434-441 | After a partial answer the agent "applies the answered ones and stops on the rest", but PART 2 has no row for a partially filled `## Decision`: on the next run it reads as filled, is applied and reported applied, and the orchestration archives the file with entries still unanswered. |
| F17 | NOTE | refonte | 2 | detailleur.md L378 ↔ detailleur.md L576-578 | "You never block on this" stands unqualified beside the new "that is the one conventions request you block on", an old rule left whole next to its exception. |
| F18 | NOTE | refonte | 2 | detailleur.md L330 ↔ detailleur.md L332 | The Arbitre call is described as `Settle <lot>` while the file it settles is the block's, `code/blocked_detailleur.md`, with one entry per lot — the description names a unit the call no longer has. |
| F19 | NOTE | refonte | 2 | detailleur.md L668-670 ↔ detailleur.md L439, L679 | In divergence mode a filled decision on an unnamed lot is left, yet PART 2 runs in that mode and its row says a filled `## Decision` is applied — the same file, the same run, two instructions. |
| F20 | BLOCKING | refonte | 4 | detailleur.md L259-265 ↔ cadreur.md L753-757, concepteur.md L57-58, L112, L186-187 | `## Files` is "the lot's `Modifies` and `Touches`, one path per line", but `Modifies` carries symbols and never a file, and a production lot has both at a dash — so the sheet's `## Files` is a dash exactly when the Concepteur needs it to place a new declaration, and every file the lot creates becomes "a file the sheet does not declare" for the three agents of the loop and the Relecteur (relecteur.md L386-387). |
| F21 | TO FIX | refonte | 4 | relecteur.md L168-169, L405-407 ↔ detailleur.md L468, L659-662 | The Relecteur sends a `Cause: sheet` failure "back to the Détailleur", but the ordinary mode skips every lot that has a sheet and divergence mode fires only on `## Symbol divergences` (8_code.md L177-179) — no run of the agent ever rewrites a sheet the review found false, and `8_code.md` has no row for that cause either. |
| F22 | NOTE | refonte | 4 | detailleur.md L438 ↔ arbitre.md L147-153, L249-251 | The Arbitre writes `Not settled here.` only on a block that is not his (a Relecteur's or an Architecte's) and takes every Détailleur file as his own, so the PART 2 row for that phrase never fires. |
| F23 | NOTE | refonte | 4 | detailleur.md L250-254 ↔ architecte.md L144, L150-152, detailleur.md L644 | Both lines of the `## Conventions` example — where a symbol lives, how a symbol is named — are of the kinds the Architecte marks `permanente`, which move 9 says never to name, so the example illustrates what the rule forbids. |
| F24 | NOTE | refonte | 4 | audit_blocages.md L156 ↔ detailleur.md L284-285 | The audit's example lists `code/lot-31/blocked_detailleur-01.md`, a depth the agent never writes at (its file sits at `code/`), so its glob still finds the file (L34) but the example points a reader to the wrong place. |

Sound: the block-level blocking file and its `## Blocking N` / single `## Decision` shape against the Arbitre; the divergence prompt (`Mode:`, `Your block:`, `Affected lots:`) and the orchestration-side rename against `8_code.md`; the `Bearer:` line, the preamble's `Dependencies`, the `## Symbols` inventory, the report's `## Symbols` and the verdict's `## Status` against their producers.

| # | Status | Where | One line |
|---|---|---|---|
| B-1 | moot | `.claude-new/agents/detailleur.md:443` | The rename paragraph carrying `blocked_<agent>-NN.md` is gone: the agent never renames, the orchestration does |
| B-2 | moot | `.claude-new/agents/detailleur.md:443` | Both numbering formulas are gone with the rename rule; the orchestration numbers the file |
| B-3 | fixed | `.claude-new/agents/detailleur.md:523` | |
| C-1 | fixed | `.claude-new/agents/detailleur.md:443` | |
| C-2 | fixed | `.claude-new/agents/detailleur.md:571` | |
| D-1 | fixed | `.claude-new/agents/detailleur.md:523` | |
| D-2 | fixed | `.claude-new/agents/detailleur.md:460` | |
| D-3 | other | `.claude-new/agents/detailleur.md:672` | 672 now says *divergence* verdict, so read/not-read no longer collide; `What you read` (60–89) still omits `verdict.md` and closes with `Nothing else` while rows 45 and 467 read it |
| D-4 | moot | `.claude-new/agents/detailleur.md:443` | The placeholder sat in the rename paragraph, which is removed; no `<agent>` spelling remains |
| D-5 | moot | `.claude-new/agents/detailleur.md:443` | Neither numbering rule remains; the agent no longer renames |
| D-6 | moot | `.claude-new/agents/detailleur.md:443` | The three rename passages are replaced by one rule: the orchestration renames |
| D-7 | other | `.claude-new/agents/detailleur.md:571` | 571–578 now say block, whole block, blocking file as the mechanism, exception stated; 378 still reads *You never block on this* unqualified, and the `<lot>` a walk-time request is filed under is unstated |
| D-8 | fixed | `.claude-new/agents/detailleur.md:284` | |
| D-9 | fixed | `.claude-new/agents/detailleur.md:292` | |
| D-10 | fixed | `.claude-new/agents/detailleur.md:403` | |
| D-11 | fixed | `.claude-new/agents/detailleur.md:590` | |
| D-12 | fixed | `.claude-new/agents/detailleur.md:457` | |
| D-13 | fixed | `.claude-new/agents/detailleur.md:589` | |
| D-14 | fixed | `.claude-new/agents/detailleur.md:633` | |
| D-15 | fixed | `.claude-new/agents/detailleur.md:525` | |
| D-16 | fixed | `.claude-new/agents/detailleur.md:668` | |
| D-17 | fixed | `.claude-new/agents/detailleur.md:353` | |
| D-18 | fixed | `.claude-new/agents/detailleur.md:460` | |
