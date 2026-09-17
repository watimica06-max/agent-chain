# Vérification 2 — `redacteur.md`

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | TO FIX | refonte | 1 | modifications.md L208 ↔ redacteur.md L168-173 | Item 4 applied wider than asked: the index puts the `en anglais :` line on the `## Tranché` entry alone, the file also sends it to the term's `## Relevé` line "when the term was never questioned", spliced mid-sentence so the rule now reads "…invisible to it in `lexique.md`, as an `en anglais :` line". |
| F02 | NOTE | refonte | 1 | passes/redacteur.md L87 ↔ redacteur.md L124-125 | C1 applied wider than asked: the sheet strips markers on grid files (`sondeur-*`) only, the file also strips on the `existant` and `convertisseur` prefixes, which neither the sheet nor the index names. |
| F03 | NOTE | refonte | 1 | modifications.md L143 ↔ redacteur.md L527-542 | The index's redacteur section never mentions the invocation-2 route on a `blocked_decoupeur.md`, `blocked_qualifieur.md` or `blocked_classeur.md`, which the file adds with its own table and rewrite rule. |
| F04 | NOTE | refonte | 1 | modifications.md L143 ↔ redacteur.md L414-416 | The index does not mention the removal of "it runs past 250 KB" from the global-index rule. |
| F05 | NOTE | refonte | 2 | redacteur.md L56-57 ↔ redacteur.md L59-62 | The sentence announces "an identifier, a nature and, when it moved, a marker" while the example under it carries a `Genre:` and a `Global:` line too, so a reader who takes the sentence as the list writes neither. |
| F06 | TO FIX | refonte | 2 | redacteur.md L119 ↔ redacteur.md L125 | "You strip the markers only when a grid turn ran on them" excludes the `convertisseur` row of its own table (and L553 "from the grid or the conversion"), so a reader following the sentence strips nothing on a conversion file and the consumed markers send the grid back over blocks it already closed. |
| F07 | NOTE | refonte | 2 | redacteur.md L323-325 ↔ redacteur.md L707-708 | "What you never do" forbids a changed block without `MODIFIED` and a created one without `NEW` with no carve-out for invocation 3, which strips every marker, so two absolute rules stand and a reader keeping the list hands the Fusionneur a marked file. |
| F08 | TO FIX | refonte | 2 | redacteur.md L385 ↔ redacteur.md L668, L687 | Invocation 3's inputs row names `desc-produit.md`, `lexique.md` and the global, the body calls `decisions-produit.md` "the only artefact you open" and then opens `desc-produit-fusion.md`, which no input lists, so under "Load only what your invocation lists" (L391) the file it must edit is off limits. |
| F09 | NOTE | refonte | 2 | redacteur.md L385 ↔ redacteur.md L168 | Row 3 takes `lexique.md` as input but declares no `en anglais` output while the recording rule fires on any first English rendering, so a concept a decision brings at invocation 3 is either written where the row does not declare or left unrecorded. |
| F10 | NOTE | refonte | 2 | redacteur.md L99-100 ↔ redacteur.md L103-105 | On a strip-none turn a `NEW` block an answer changes has no outcome: "`MODIFIED` on every block you change" against "a block already carrying `NEW` keeps `NEW`" stated for the transverse case only, so two readers write `NEW MODIFIED` or `NEW`. |
| F11 | QUESTION | refonte | 2 | redacteur.md L83-85 ↔ redacteur.md L457-458 | A section created with a global's title after move 2's test said No is an attachment by L83 but gets no `Global:` line by move 3 ("when move 2 found one"), and whether "found" means a title match or a same-trigger match decides whether the existant turn ever sees the block. |
| F12 | NOTE | pre-existing | 2 | redacteur.md L655-657 ↔ redacteur.md L541 | "On either branch" now spans three branches (blocking file, pass d empty, pass d found) and "invocation 2 says what is still missing" points at the section it sits in, so nothing names the questions file as the place where what is missing is said. |
| F13 | TO FIX | refonte | 4 | redacteur.md L59-62 ↔ 4_grille.md L257 | The redacteur writes `Global:` third under the title, after `Genre:` and `Nature:`, so `grep -B1 '^Global: '` returns the `Nature:` line and never the `### B` heading, and the existant invocation is handed no identifier to probe. |
| F14 | TO FIX | refonte | 4 | redacteur.md L169-170 ↔ lexicographe.md L176, L199 | The lexicographe places the `en anglais` line on a settled concept and rebuilds `## Relevé` at every sweep, so a word written on a `## Relevé` line is wiped and the compare at lexicographe.md L464 never sees it — the second rendering the rule exists to catch goes through. |
| F15 | TO FIX | refonte | 4 | redacteur.md L674-676 ↔ fusion.md L161 | The `/fusion` prompt template carries "Which invocation" and nothing else, so an orchestrator copying it names no `decisions-produit.md`, and the agent, forbidden to look for itself, writes a faithful copy with no decision folded in. |
| F16 | TO FIX | refonte | 4 | redacteur.md L343-359 ↔ fusion.md L43 | `/fusion` routes a filled `blocked_*.md` "at the invocation its `## Invocation` line names" and the redacteur's blocking file has no such heading, so a block raised at invocation 3 sends the orchestrator to a line that does not exist. |
| F17 | TO FIX | refonte | 4 | redacteur.md L533-535 ↔ 2_structure.md L191 | After the redacteur applies a `blocked_qualifieur.md` or `blocked_classeur.md`, `/2_structure` renames only `blocked_decoupeur.md`, so the other two stay at the unnumbered name and `/3a_genre` (L34) or `/3b_nature` (L33) stops on a block already settled. |
| F18 | NOTE | refonte | 4 | redacteur.md L527-529 ↔ 2_structure.md L149 | The `/2_structure` template's `Read:` line offers `idees.md` or `questions-<agent>-NN.md` while row L120 names a blocking file, so the orchestrator improvises the line on that route. |
| F19 | NOTE | refonte | 4 | redacteur.md L702-705 ↔ fusionneur.md L387 | A block created at invocation 3 by the four moves carries an empty `Nature:` that no classeur ever fills, and the fusionneur keeps `Nature:` lines in the global, so the global ends up carrying a block with no nature. |
| F20 | NOTE | refonte | 4 | redacteur.md L528 ↔ classeur.md L196-199 | The classeur's blocking file carries one `## Decision` per `## Blocking N` while the redacteur reads "its `## Decision`" as one and `/2_structure` L120 tests one filled heading, so a file with two blockings and one decision is sent whole and applied in part. |
| F21 | NOTE | refonte | 4 | redacteur.md L119-126 ↔ 6_convertit.md L141-142 | `/6_convertit` still says the Rédacteur strips every marker on each turn; the conclusion it founds (a block changed two grid turns ago carries none) still holds under the prefix rule, so nothing breaks. |
| F22 | NOTE | pre-existing | 4 | redacteur.md L3 ↔ decoupeur.md L3 | The frontmatter calls it "the only agent that writes the product file" while the decoupeur, qualifieur and classeur each declare writing in it, a false fact to a reader of the registry. |

Checked and found sound: section 3 (five tools, each with a gesture, no `Bash`); C2, C3, C4, C6, C7, C8, C9 present as asked and C5, C17, C18 absent; the `Défaut:` shape against sondeur.md L386-392, `code/decisions-produit.md` against 9_controle.md L305-308, the *existing* mark against convertisseur.md L115-123, the copy against fusion.md L79-84, C10–C16 in 2_structure.md.

| # | Status | Where | One line |
|---|---|---|---|
| C15 (NOTE) | fixed | `.claude-new/commands/2_structure.md:173` | |
| C18 (NOTE) | open | — | |
| A.2 · 2 (NOTE) | fixed | `.claude-new/agents/redacteur.md:572–574` | |
| B.2 | open | — | |
| B.4 | fixed | `.claude-new/agents/redacteur.md:119–125` | |
| B.5 | fixed | `.claude-new/agents/redacteur.md:121–125` | |
| B.6 | open | — | |
| B.8 | other | `.claude-new/agents/redacteur.md:223–226` | The cadreur is dropped and the claim now names one reader, the convertisseur, and one effect, a preamble dependency — still stated as fact |
| C · copy (TO FIX) | fixed | `.claude-new/agents/redacteur.md:687–691` · `.claude-new/commands/fusion.md:75–84` | |
| D.1 | fixed | `.claude-new/agents/redacteur.md:3` | |
| D.1 · note | open | — | |
| D.2 | fixed | `.claude-new/agents/redacteur.md:387–392` | |
| D.3 | fixed | `.claude-new/agents/redacteur.md:385` | |
| D.4 | other | `.claude-new/agents/redacteur.md:262–265` | The rule now reads "at invocations 1 and 2, never at invocation 3"; the branch for a decision the agent cannot place is still absent — l.263 asserts it raises none while l.703–705 sends a new subject through the four moves, move 4 included |
| D.5 | fixed | `.claude-new/agents/redacteur.md:313–316, 687–691` · `.claude-new/commands/fusion.md:79` | |
| D.6 | fixed | `.claude-new/agents/redacteur.md:598, 609–612` | |
| D.7 | other | `.claude-new/agents/redacteur.md:457–458, 613–614` | Written at move 3 and inherited by every half of a split; pass a row 3 (l.598) still creates a block with no `Global:` line |
| D.8 | fixed | `.claude-new/agents/redacteur.md:103–105` | |
| D.9 | other | `.claude-new/agents/redacteur.md:119–125` | The "an agent that read them" criterion is gone, replaced by a prefix table; the two lists at l.116 and l.323 still name neither the qualifieur nor the classeur |
| D.10 | fixed | `.claude-new/agents/redacteur.md:572–578` | |
| D.11 | fixed | `.claude-new/agents/redacteur.md:703` | |
| D.12 | fixed | `.claude-new/agents/redacteur.md:666–670, 674–676` | |
| D.13 | fixed | `.claude-new/agents/redacteur.md:256–260` | |
| D.14 | open | — | |
| D.15 | open | — | |
| D.16 | open | — | |
| D.17 | open | — | |
