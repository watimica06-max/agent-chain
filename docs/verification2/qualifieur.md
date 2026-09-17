# qualifieur — verification 2

Section 1: no pass sheet exists for this agent; the index alone was held against the file. The previous round's `.claude/agents/qualifieur.md` does not exist — the agent is new, so every finding originates in the refonte.

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | qualifieur.md L140-141 ↔ modifications.md L118 | The index settles one doubt silently — *« is it transverse? »* → `comportement` — while the file settles *any* genre doubt that way, so a hesitation between `directive` and `référence` is also written `comportement` and sent to the classeur and the grid, which the index never asked for. |
| F02 | NOTE | refonte | 1 | qualifieur.md L88-91 ↔ modifications.md L60-62 | The file carries a third rule the index does not list — a block whose sentences call for two genres gets the genre of what it is mostly about — where the index records only the two rules added while writing, so the record of what was written is incomplete. |
| F03 | TO FIX | refonte | 3 | qualifieur.md L4 ↔ qualifieur.md L212-213 | The gesture is "one targeted edit per `Genre:` line", but every unqualified block carries the identical empty `Genre:` line, and `Edit` refuses a non-unique match; the file never says to anchor the edit on the block's heading, so the edit fails or the agent falls back on the whole-file rewrite L211 forbids. |
| F04 | NOTE | refonte | 3 | qualifieur.md L4 ↔ qualifieur.md L41-47 | The block runs "to the next heading of any level" and the agent must "load those, and no others", but no tool is named for finding where the block ends or for loading a window of lines; an agent that `Read`s the file to find the next heading has read it whole, against L41. |
| F05 | TO FIX | refonte | 2 | qualifieur.md L22-24 ↔ qualifieur.md L150-151 | The role says the classeur and the sondeurs "cannot refuse" a block, yet the asymmetry says a wrong `comportement` is "a choice the classeur and the sondeurs undo at no cost"; nothing downstream undoes it, so a directive filed as a behaviour keeps a nature, is converted and coded, and the cheap side of the asymmetry is not cheap. |
| F06 | TO FIX | refonte | 2 | qualifieur.md L90 ↔ qualifieur.md L145-147 | A two-genre block gets "the genre of what it is mostly about", so a block mostly `directive` with one behaviour sentence is filed `directive` and leaves the grid — exactly the silent hole L145-147 says never to open; the two rules pull the same block in opposite directions. |
| F07 | TO FIX | refonte | 2 | qualifieur.md L329 ↔ qualifieur.md L297-303 | On a `MODIFIED` block the agent must "ask again what fires it and what it produces", the very question step 1-2 forbid asking first because it "would call it `comportement` every time"; a rewritten `transverse` or `directive` is thus re-read as a behaviour on every change. |
| F08 | TO FIX | refonte | 2 | qualifieur.md L258-259 ↔ qualifieur.md L231-247, L267-271 | Several blocked blocks go in one file with "one `## Where` entry each", but the shape has one `## What blocks`, one `## To resume` and one `## Decision`, and the decision table is per block; with two blocks the Product Owner has one place to write two decisions and the agent cannot tell which block a genre applies to. |
| F09 | NOTE | refonte | 2 | qualifieur.md L131-133 ↔ qualifieur.md L113, L119 | `comportement` "usually has a trigger and an output — but so do most of the five above", while the same page says a `directive` has no trigger and a `référence` has none either; the agent is told the trigger test does not discriminate where its own descriptions say it does. |
| F10 | NOTE | refonte | 2 | qualifieur.md L288-289 ↔ qualifieur.md L51 | "You do not grep again" stands beside "Grep `^### B7 `"; unlike the classeur, the file never says the heading grep is a different grep and is the agent's, so a literal reading leaves it no permitted way to find a block but reading the file whole. |
| F11 | BLOCKING | refonte | 4 | qualifieur.md L270 ↔ 3a_genre.md L164-167 · 2_structure.md L120 | When the decision names a rewrite the agent leaves the line empty and "the block waits on the Rédacteur", but `/3a_genre` renames the blocking file to `blocked_qualifieur-NN.md` once the agent reports, and `/2_structure` looks for `blocked_qualifieur.md` — the rewrite route never finds its file, and the block stays unqualified with `/3a_genre` reporting a defect on every run. |
| F12 | TO FIX | refonte | 4 | qualifieur.md L143-145 ↔ 4_grille.md L140-146 | The asymmetry prices a rule wrongly called `comportement` at "one grid question too many", but a `transverse` filed that way is absent from the transverse list the sondeurs hold, so every block it reaches raises the gap the rule already answers, asked of the Product Owner by hand; the silent side is the cheap one only for the other four genres. |
| F13 | TO FIX | refonte | 4 | qualifieur.md L351-354 ↔ 3a_genre.md L216-222 | The per-block genre list is "the only place the Product Owner can see" a wrongly filed behaviour before the grid closes, but the command relays counts and changed genres only and says "nothing else is yours"; the list stops at the orchestrator and the Product Owner never sees it. |
| F14 | TO FIX | refonte | 4 | qualifieur.md L356-358 ↔ 3a_genre.md L227-235 | The agent reports blocks whose sentences call for two genres because "the decoupeur should have split it", but the command has no relay and no *next* row for that report, so the decoupeur is never sent back and the majority genre of F06 stands. |
| F15 | NOTE | refonte | 4 | qualifieur.md L188-189 ↔ 3a_genre.md L50-54, L68-70 | The agent expects the prompt to name its answered file, and the command names the highest one "when it holds at least one `### Q`" — but four rules later it stops on any root questions file holding a `### Q`; the answered-questions procedure of L186-205 runs only if the command ignores one of its own rules. |
| F16 | NOTE | refonte | 4 | qualifieur.md L273-274 ↔ CLAUDE.md L52 | A seventh value "would pass `/3a_genre`'s check and stop `/5_reclasse` two commands later" — from `/3a_genre` it is three commands later (`/3b_nature`, `/4_grille`, then `/5_reclasse`); L63 counts from `/3b_nature` and gets two, so the same distance is given two lengths. |

Checked and found sound: the six-genre table, the `transverse` test and its examples, the questions-file shape and numbering against `/3a_genre`, the blocking-file location and the three decision shapes against the command's *next* table, the `Genre:`/`Nature:` line order against the Rédacteur and `/3b_nature`, the `^Genre: comportement$` grep claim against `/4_grille` and `/5_reclasse`, and the frontmatter tool set (no `Glob`, no `Bash`) against "you never list a folder".

| # | Status | Where | One line |
|---|---|---|---|
| A4 | fixed | `agents/qualifieur.md` l.85–91 | |
| A8 | fixed | `agents/qualifieur.md` l.140–141 | |
| B1 | other | `agents/qualifieur.md` l.112–133 | The trigger/output definitions stay; `comportement` (l.130–133) now says most of the five share them, and PART 3 asks the subject first |
| B2 | fixed | `agents/qualifieur.md` l.140–151 | |
| B3 | open | `agents/qualifieur.md` l.140 | |
| B4 | open | `agents/qualifieur.md` l.219–220 | |
| B5 | fixed | `agents/qualifieur.md` l.333–336 | |
| B6 | fixed | `agents/qualifieur.md` l.44–52 | |
| B7 | fixed | `agents/qualifieur.md` l.54–66 | |
| B8 | fixed | `agents/qualifieur.md` l.264–274 | |
| B9 | fixed | `agents/qualifieur.md` l.254–262 | |
| B10 | fixed | `agents/qualifieur.md` l.351–354 | |
| C1 | fixed | `agents/qualifieur.md` l.4, l.51, l.166 | |
| D1 | fixed | `agents/qualifieur.md` l.297–317 | |
| D2 | fixed | `agents/qualifieur.md` l.314–317 | |
| D3 | moot | `agents/qualifieur.md` l.140–151 | The "you still raise it as a question" rule has gone; doubt 1 is now silent, so the asymmetry justifies what the agent does |
| D4 | fixed | `agents/qualifieur.md` l.143–144 | |
| D5 | fixed | `agents/qualifieur.md` l.88–91, l.356–358 | |
| D6 | fixed | `agents/qualifieur.md` l.264–274 | |
| D7 | fixed | `agents/qualifieur.md` l.254–262 | |
| D8 | fixed | `agents/qualifieur.md` l.323–325 | |
| D9 | fixed | `agents/qualifieur.md` l.3 | |
| D10 | fixed | `agents/qualifieur.md` l.80, l.312 | |
