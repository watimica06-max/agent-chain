# Relecteur — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | TO FIX | refonte | 1 | modifications.md L1190-1207 ↔ passes/relecteur.md L358-520 | The index's C11, C13 and C15 describe the pass sheet's ### 12, ### 14 and ### 16, so from C11 on the index is off by one and its deferred C14 and C17 match no comment — ### 14 and ### 17 are applied in the file while the index reads them as deferred. |
| F02 | NOTE | refonte | 1 | relecteur.md L149-150, L171-174 ↔ modifications.md L1175-1240 | The verdict's `## Causes so far` field appears in no index entry and no pass comment, so the record does not say where it came from. |
| F03 | NOTE | refonte | 1 | passes/relecteur.md L541-543 ↔ relecteur.md L419-422 | ### 17 asked for a symbol named by neither the sheet nor the report's `## Symbols` to be a finding; the file counts the sheet alone and rejects the report, with a reason of its own — applied differently than asked. |
| F04 | NOTE | refonte | 1 | passes/relecteur.md L456-461 ↔ relecteur.md L404-407 | ### 14 asked for the outcome of a sheet lacking any section the checklist depends on; the file settles the missing criteria only, and a sheet with no `## Signatures` or no `## Conventions` still has no stated outcome. |
| F05 | NOTE | refonte | 1 | passes/relecteur.md L433-436 ↔ relecteur.md L66-68 | ### 13 asked for the conventions file to be read by section only; the file adds a whole-file read whenever no rule carries `permanente`, which re-opens the whole-file load the comment removed. |
| F06 | NOTE | refonte | 3 | relecteur.md L4 ↔ relecteur.md L60-61, L80-82, L194 | Four reads are bounded to "one line, never the file" without naming Grep as the tool, so an agent obeying Read opens the sequence and the other verdicts whole and breaks the bound. |
| F07 | TO FIX | refonte | 2 | relecteur.md L114 ↔ relecteur.md L115 | "One of two words, and no other" is followed by three, so the rule announces a count its own list breaks and a reader cannot tell which word is the extra. |
| F08 | TO FIX | refonte | 2 | relecteur.md L115-116 ↔ relecteur.md L176-178 | `reasoning` is defined once as a calculation badly conducted and once as a sheet "read wrongly", which is what `understanding` names, so the label the orchestration escalates to opus on is assigned two ways. |
| F09 | TO FIX | refonte | 2 | relecteur.md L312-315 ↔ relecteur.md L157-160, L171-174, L207-210 | The head-rule verdict is listed with five fields and omits `## Verified` and `## Causes so far`, so on a red build the field the file says must never be empty is absent and the cause history the orchestration escalates on is dropped. |
| F10 | TO FIX | refonte | 2 | relecteur.md L60-61 ↔ relecteur.md L171-173 | The old verdict is read "its `## Attempts` line alone" while `## Causes so far` must be "copied from the verdict you replace", so the copy cannot be made without breaking the read bound. |
| F11 | NOTE | refonte | 2 | relecteur.md L112 ↔ relecteur.md L404-405 | `FAIL structurel` is "one of two things, never a count" and a sheet with no criteria is a third, so the table is no longer the definition it claims to be. |
| F12 | NOTE | pre-existing | 2 | relecteur.md L110 ↔ relecteur.md L124-155 | `PASS with reservation` promises a note "for what follows" and the seven fields have no place for it, so the reservation is written nowhere and reaches nobody. |
| F13 | NOTE | pre-existing | 2 | relecteur.md L46-47 ↔ relecteur.md L105-119 | The verdict's shape is sent to *The verdict*, which holds the status table; the shape lives under *What you write*. |
| F14 | TO FIX | refonte | 2 | relecteur.md L409-411 ↔ relecteur.md L340-342 | A criterion "not listed under `## Tests`" is declared uncovered, which includes every criterion in `## Criteria with no test` that L340 declares not a gap, so a literal reader fails every lot that has a manual-list criterion. |
| F15 | NOTE | refonte | 2 | relecteur.md L404-416 ↔ relecteur.md L317-346 | The no-criteria, disabled-test and removed-symbol rules governing points 1 and 2 sit after point 4, so they are read after the points they decide have run. |
| F16 | NOTE | refonte | 2 | relecteur.md L58-59, L340 ↔ relecteur.md L236-239 | Point 2 rests on `tests.md` and point 4 on `conception.md`, and blocking is bounded to "no sheet, no report", so a lot missing either file has no stated outcome. |
| F17 | NOTE | pre-existing | 2 | relecteur.md L114 ↔ relecteur.md L124-155 | `## Cause` is named "on a FAIL" and `## Findings` "names every point that failed", and nothing says what either carries on a PASS, so two of the seven mandatory fields have no defined content on the normal path. |
| F18 | NOTE | refonte | 2 | relecteur.md L41 ↔ relecteur.md L295, L298 | "The report" is `compte-rendu.md` throughout and "your report" at L295 is the agent's return message, so one word names the Réalisateur's file and the Relecteur's answer. |
| F19 | TO FIX | refonte | 4 | relecteur.md L167-169, L407 ↔ 8_code.md L41-43, L138-144 | The agent promises that `Cause: sheet` sends the block to the Détailleur "never to a fresh Réalisateur", and `/8_code` routes every FAIL to a fresh Réalisateur and reads `## Cause` for escalation only, so a lot with a defective sheet is recoded three times against the same sheet and then stops on the Product Owner. |
| F20 | NOTE | refonte | 4 | relecteur.md L162-165 ↔ realisateur.md L520 | `## Findings` names every failed point so the fresh Réalisateur fixes them all, and the Réalisateur's FAIL mineur row says "fix the point reported", singular, so a literal reader fixes one of several. |

Checked and found sound: the removed `Edit` tool leaves no editing, renaming or shell gesture behind; every field and file the agent names in the report, the sheet, `conception.md`, `tests.md` and `code/sequence.md`'s `## Blocks` line exists under that name in realisateur, detailleur, concepteur, testeur and verificateur; the `/8_code` prompt carries the folder, the lot and the changed-file list the agent requires.

| # | Status | Where | One line |
|---|---|---|---|
| C1 | fixed | `.claude-new/agents/relecteur.md:4, 232–234, 295–298` · `.claude-new/commands/8_code.md:170–172` | |
| C2 | fixed | `.claude-new/agents/relecteur.md:238–239` | |
| C4 | fixed | `.claude-new/agents/relecteur.md:99–101, 192–201` | |
| C5 | fixed | `.claude-new/agents/relecteur.md:54–57, 184–190` · `.claude-new/agents/realisateur.md:156, 176–182` | |
| C7 | fixed | `.claude-new/agents/relecteur.md:326–327, 369, 399–400` | |
| C8 | fixed | `.claude-new/agents/relecteur.md:114–116` · `.claude-new/commands/8_code.md:159–160` | |
| C12 | other | `.claude-new/agents/relecteur.md:275` | The guard left the verdict section; the never-do bullet "Fall to structurel by default for an isolated gap" stays |
| C13 | fixed | `.claude-new/agents/relecteur.md:349–357` | |
| C14 | other | `.claude-new/agents/relecteur.md:167–169, 404–407` | The agent now yields `FAIL structurel`, `Cause: sheet`, "the orchestration sends the block back to the Détailleur" — `/8_code` has no branch on that cause: move 4 (138–139) still sends every FAIL to a fresh realisateur |
| B-1 | open | — | |
| B-2 | fixed | `.claude-new/agents/relecteur.md:386–392` | |
| B-3 | open | `.claude-new/agents/relecteur.md:136` | |
| B-4 | open | `.claude-new/agents/relecteur.md:154–155` | |
| B-5 | fixed | `.claude-new/agents/relecteur.md:295–298` | |
| B-6 | fixed | `.claude-new/agents/relecteur.md:340–345` | |
| B-7 | other | `.claude-new/agents/relecteur.md:353` | Nothing was asked; "Open each" now sits under the rewritten two-scope point 3 (349–351), its two antecedents stated in one sentence |
| B-8 | fixed | `.claude-new/agents/relecteur.md:417–429` | |
| C-2 | fixed | `.claude-new/agents/relecteur.md:232–234, 295–298` · `.claude-new/commands/8_code.md:170–172` | |
| C-3 | fixed | `.claude-new/agents/relecteur.md:54–57, 184–190` · `.claude-new/agents/realisateur.md:176–182` | |
| C-4 | fixed | `.claude-new/agents/relecteur.md:387–389` | |
| C-5 | fixed | `.claude-new/agents/relecteur.md:409–412` | |
| C-6 | fixed | `.claude-new/agents/relecteur.md:387–392` | |
| C-7 | fixed | `.claude-new/agents/relecteur.md:4` | |
| C-8 | fixed | `.claude-new/agents/relecteur.md:82–83` | |
| D-1 | fixed | `.claude-new/agents/relecteur.md:232–234, 295–298` · `.claude-new/commands/8_code.md:170–172` | |
| D-2 | fixed | `.claude-new/agents/relecteur.md:99–101, 192–201` | |
| D-3 | fixed | `.claude-new/agents/relecteur.md:349–357` | |
| D-4 | fixed | `.claude-new/agents/relecteur.md:369, 399–400` | |
| D-5 | other | `.claude-new/agents/relecteur.md:167–169, 327, 404–407` | Status, cause category and point 1's row are there; the route exists in the agent's words only — `/8_code` reads `## Cause` (42) and branches on nothing but `reasoning` (159), never on `sheet` |
| D-6 | other | `.claude-new/agents/relecteur.md:306–310, 380–384` | "Run the five checks from the start" is gone; point 4 still restates the own-module-red rule the head rule already closes |
| D-7 | fixed | `.claude-new/agents/relecteur.md:114–116, 146, 150` · `.claude-new/commands/8_code.md:159, 325–326` | |
| D-8 | fixed | `.claude-new/agents/relecteur.md:312–315` | |
| D-9 | fixed | `.claude-new/agents/relecteur.md:386–392` | |
| D-10 | fixed | `.claude-new/agents/relecteur.md:419–422` | |
| D-11 | fixed | `.claude-new/agents/relecteur.md:344–345` | |
| D-12 | other | `.claude-new/agents/relecteur.md:275` | Same as C12: one of the two guards removed, the never-do bullet stays |
| D-13 | fixed | `.claude-new/agents/relecteur.md:288–289, 295–298` | |
| D-14 | fixed | `.claude-new/commands/8_code.md:129–132, 149–151` | |
| D-15 | fixed | `.claude-new/agents/relecteur.md:280–283` | |
| D-16 | other | `.claude-new/agents/relecteur.md:74–78` | The exception now follows "Nothing else" directly and lists its three bounded inputs, still as its own paragraph rather than in the same sentence |
