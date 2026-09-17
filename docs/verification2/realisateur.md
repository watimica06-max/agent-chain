# realisateur — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L1114 ↔ realisateur.md L425 | C1 is recorded as *« `git mv` et `git restore` ajoutés »*, but the whitelist gained `git restore` only — the rename moved to the orchestration (L508), so the index describes a change the file does not carry. |
| F02 | TO FIX | pre-existing | 1 | modifications.md L1115 ↔ realisateur.md L524 | C5 is PASSÉ on *three* triggers, yet the third — a verdict judged wrong — still reads *« stop and report rather than coding against it »*; the block wording reached two of the three. |
| F03 | NOTE | pre-existing | 1 | modifications.md L1096 ↔ realisateur.md L229 | C8 is PASSÉ but only its placement half landed (move 1 blocks on an unplaced declaration); the boundary *« by effect on the code »* between a mid-lot block and an end-of-lot request is stated nowhere, and the block triggers at L229-232 name no missing convention. |
| F04 | NOTE | refonte | 1 | modifications.md L1105 ↔ realisateur.md L215 | C9 is ÉCARTÉ (*« c'est le Testeur qui décide »*), yet the wrong-sheet triggers now carry *« a criterion no test can be made to read »* — the very case C9 asked to route there. |
| F05 | NOTE | refonte | 1 | modifications.md L1106 ↔ 8_code.md L463 | C3, C13, C14, C16 and C17 are REPORTÉ *« à passer avec A3 »*, but their `/8_code` side is already in place (L463-466, L164-175, L48-51, L142-157, L12-14) while the agent side (L385/L475, L503) is untouched — the index is stale on all five. |
| F06 | NOTE | refonte | 1 | modifications.md L1085 ↔ realisateur.md L364 | The index lists four modifications and mentions nowhere that the reprise lookup and rename (previous file L396-405) were removed from Part 2, while the reprise is still written at L364. |
| F07 | NOTE | refonte | 1 | modifications.md L1085 ↔ realisateur.md L258 | Also absent from the index: the multi-entry `## Blocking N` shape (L258-270), the `Not settled here.` row (L504), *« the orchestration renames the file »* (L505-509) and the rewritten wrong-sheet trigger list (L215-216). |
| F08 | TO FIX | pre-existing | 3 | realisateur.md L66 ↔ realisateur.md L551 | Three bounded reads name no tool for locating what they bound — the `permanente` rules (L66-70), the rules the sheet cites by `§n` (L97-98), and the two sections of the state document (L551-552, forbidden whole at L452) — so an agent obeying `Read` opens each file whole and breaks the rule it was given. |
| F09 | TO FIX | refonte | 2 | realisateur.md L258 ↔ realisateur.md L272 | The blocking file is *« one `## Blocking N` per stop… one `## Decision` at the end »* with `###` entries, then *« The headings of an entry »* shows `##` headings and a `## Decision` inside each entry — an agent following the second shape hands the Arbitre a file with two `## Decision` headings, and its `Edit` anchored on that heading fails on *Found N matches*. |
| F10 | TO FIX | refonte | 2 | realisateur.md L317 ↔ realisateur.md L362 | *« Some numbers answered, others not → stop on the entries they do not cover »* leads nowhere: the empty-decision section covers *« Still empty »* only, no file is named for the stop, and the next run's table (L505) reads a partly filled `## Decision` as *Filled* — the unanswered entry is applied as nothing and archived by the rename. |
| F11 | TO FIX | pre-existing | 2 | realisateur.md L385 ↔ realisateur.md L475 | *« never commit what does not [compile]… say in `En chantier` what you left uncommitted »* against *« Leave a dirty working tree behind you, whatever the reason »* — the reprise's key field describes code the agent is forbidden to leave, and the orchestration refuses to remove the worktree it leaves. |
| F12 | NOTE | pre-existing | 2 | realisateur.md L388 ↔ realisateur.md L370 | *« The `## Decision` heading is written empty, and never omitted »* sits under the reprise shape, which has no such heading — read literally, the reprise gets a `## Decision` the Product Owner is then told to fill. |
| F13 | TO FIX | refonte | 2 | realisateur.md L366 ↔ realisateur.md L493 | The reprise is written *« for a fresh Réalisateur… this file is all it gets »*, but Part 2 has no case for it: nothing tells the fresh run to read `Non fait` or `En chantier`, so it starts from move 1 and meets the half-written code at the build — exactly what the field exists to prevent. |
| F14 | TO FIX | refonte | 2 | realisateur.md L320 ↔ realisateur.md L366 | A blocked run writes its report (L320), but the run that resumes after an empty decision gets *« your sheet, the blocking file… and this file »* — not that report — so its move 8 rewrites `## Symbols` from what it alone coded, and the Relecteur reads the blocked run's symbols as promised-and-absent. |
| F15 | TO FIX | pre-existing | 2 | realisateur.md L229 ↔ realisateur.md L398 | A convention missing on *how* the code is written — which layer owns a mapping, what a kind of symbol is built on — is neither a wrong sheet (L229-232) nor a condition of running (L398-402): no branch covers it, and the agent either invents the rule or files a request settled after the code is merged. |
| F16 | NOTE | refonte | 2 | realisateur.md L336 ↔ realisateur.md L226 | *« Nothing you wrote is a new file »* is contradicted by L226: the blocking file the agent wrote is a new, untracked file — harmless only because `/8_code` commits everything before `/7_lots`, which L352-355 does not know. |
| F17 | NOTE | pre-existing | 2 | realisateur.md L31 ↔ realisateur.md L515 | *« One invocation per lot »* against a fresh Réalisateur on every FAIL (L515) and on every empty decision (L366) — *invocation* is used in two senses, and the count is false in words. |
| F18 | TO FIX | pre-existing | 4 | realisateur.md L556 ↔ detailleur.md L224 | The state-document grep (L124, L542, L556) and `## Outside the lot` (L194) key on *« every symbol the sheet lists as modified »* and *« your `Modifies` »*, but the sheet has no `Modifies` field and its `## Signatures` mark nothing created or modified (`## Files` merges Modifies and Touches *« no distinction »*, L259-260) — the grep that feeds move 7 has no input. |
| F19 | TO FIX | pre-existing | 4 | realisateur.md L79 ↔ arbitre.md L396 | The Arbitre files a trap under a subject heading believing *« the Réalisateur reads it whole, always »*, while the Réalisateur reads two sections and greps only the symbols it modifies — a trap on a symbol the lot consumes without modifying (its `## Dependencies`) is read by nobody. |
| F20 | NOTE | refonte | 4 | realisateur.md L136 ↔ arbitre.md L403 | *« the Arbitre — which writes its `## Traps` section »* names a heading the state document does not have (`## Traps — general` or a subject's `###`, skill L65-72; the Arbitre says so at L403). |
| F21 | TO FIX | pre-existing | 4 | realisateur.md L50 ↔ 8_code.md L295 | The FAIL path rests on a fact nothing gives: the command says *« a fresh realisateur, with the verdict »* (L138) but its only prompt shape carries the folder, the lot and a reprise, and the agent's Part 2 looks for the blocking file alone — a fresh run that is not told it resumes a FAIL codes from move 1 and spends an attempt without reading the point reported. |
| F22 | TO FIX | refonte | 4 | realisateur.md L215 ↔ testeur.md L274 | *« a criterion no test can be made to read »* is a wrong-sheet block for the Réalisateur, but the testeur already filed that criterion under `## Criteria with no test` and the Relecteur handles it (relecteur.md L340) — the block costs an Arbitre round trip on a case already recorded. |
| F23 | NOTE | refonte | 4 | realisateur.md L364 ↔ 8_code.md L170 | Nobody archives the reprise any more: the agent no longer renames it, the command renames `blocked_<agent>.md` only — a consumed `reprise_realisateur.md` stays and is named in every later prompt on that lot, a FAIL retry included. |
| F24 | NOTE | pre-existing | 4 | realisateur.md L503 ↔ 8_code.md L169 | *« A `## Decision` still empty → Call the Arbitre on it »* covers a case the command now intercepts before invoking (*« Stop — invoking again re-raises the same block »*); the row is dead, and if ever reached it re-polls the Product Owner for twenty minutes. |
| F25 | NOTE | refonte | 4 | realisateur.md L533 ↔ detailleur.md L401 | The Détailleur still holds *« Decide where the code goes — the Réalisateur does, from the conventions »* while the Réalisateur now *« places nothing: the concepteur did »* — a stale fact about this agent in its producer's file. |
| F26 | NOTE | pre-existing | 4 | realisateur.md L568 ↔ detailleur.md L630 | Move 4 takes the intra-lot order from *« the sheet's `## Dependencies` field »*, but that field lists only the types the lot consumes and does not produce (*« A type this lot produces has no line »*) — the order among the lot's own symbols is the agent's to work out, which L569 says it does not decide. |

Sound: modifications 1-4 and C2, C4, C6, C7, C10, C11, C15, C18 as recorded; the Arbitre prompt and decision shape; `## Red`, `## Declared`, `## Files`, `## Conventions`, `## What governed the code, besides the sheet` and the report fields the Relecteur reads; the `code/redecoupage.md` test on both sides; the shell whitelist against every gesture; `sonnet` in frontmatter, command and CLAUDE.md; no framework word left.

| # | Status | Where | One line |
|---|---|---|---|
| M1 | fixed | `.claude-new/agents/realisateur.md:3`, `:54`, `:143`, `:229-230`, `:455-456` | |
| M2 | fixed | `.claude-new/agents/realisateur.md:94-95` | |
| C1 | fixed | `.claude-new/agents/realisateur.md:425-427`, `:462-463`, `:335-338` | |
| C2 | moot | `.claude-new/agents/realisateur.md:315`, `:505`, `:508-509` | The agent no longer renames the blocking file — the orchestration does; the paragraph carrying the placeholder is gone |
| C4 | fixed | `.claude-new/agents/realisateur.md:144`, `:156-160`, `:176-183` | |
| C5 | other | `.claude-new/agents/realisateur.md:215-217`, `:580-581`, `:524-525` | The sheet and regression triggers now name the block; the verdict trigger (L524-525) still says "stop and report" |
| C6 | fixed | `.claude-new/agents/realisateur.md:115-118`, `:606` | |
| C7 | fixed | `.claude-new/agents/architecte.md:150-153`; `.claude-new/agents/realisateur.md:66-70` | |
| C8 | fixed | `.claude-new/agents/realisateur.md:533-539`, `:417-418` | |
| C10 | fixed | `.claude-new/agents/realisateur.md:601` | |
| C11 | fixed | `.claude-new/agents/realisateur.md:516-517`, `:521` | |
| C15 | fixed | `.claude-new/agents/realisateur.md:506` | |
| C18 | fixed | `.claude-new/agents/realisateur.md:3`, `:164`, `:201-203`, `:589` | |
| B-1 | fixed | `.claude-new/agents/realisateur.md:134-137` | |
| B-2 | other | `.claude-new/agents/realisateur.md:123-128`, `:555-557` | The second grep target (files edited) is gone, move 3's grep is the one pass; the ricochet exclusion stays |
| C-1 | fixed | `.claude-new/agents/realisateur.md:425-427`, `:462-463` | |
| C-2 | moot | `.claude-new/agents/realisateur.md:335-358` | The back-to-split branch no longer renames, writes no report and no reprise — nothing is left in the tree |
| D-1 | fixed | `.claude-new/agents/realisateur.md:3` | |
| D-2 | fixed | `.claude-new/agents/realisateur.md:521` | |
| D-3 | fixed | `.claude-new/agents/realisateur.md:54`, `:143`, `:229-230`, `:455-456` | |
| D-4 | fixed | `.claude-new/agents/realisateur.md:462-463` | |
| D-5 | fixed | `.claude-new/agents/realisateur.md:606` | |
| D-6 | moot | `.claude-new/agents/realisateur.md:508-509` | The rename rule left the agent; no `blocked_…-NN.md` target is written here any more |
| D-7 | fixed | `.claude-new/agents/realisateur.md:533-539` | |
| D-8 | fixed | `.claude-new/agents/realisateur.md:506` | |
| D-9 | fixed | `.claude-new/agents/realisateur.md:123-125`, `:555-557` | |
| D-10 | other | `.claude-new/agents/realisateur.md:215-217`, `:524-525` | The sheet trigger names the block; the verdict trigger still reads "stop and report" against L229 "Blocking is not reporting" |
| D-11 | fixed | `.claude-new/agents/realisateur.md:258-270` | |
| D-12 | fixed | `.claude-new/agents/realisateur.md:94-95` | |
| D-13 | fixed | `.claude-new/agents/realisateur.md:201-203` | |
| D-14 | fixed | `.claude-new/agents/realisateur.md:503` | |
| D-15 | fixed | `.claude-new/agents/realisateur.md:215-217` | |
| D-16 | fixed | `.claude-new/agents/realisateur.md:320-322` | |
| D-18 | fixed | `.claude-new/agents/realisateur.md:589` | |
