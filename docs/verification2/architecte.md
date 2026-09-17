# Architecte — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | passes/architecte.md L176-195 (C6) ↔ architecte.md L128, L195-198 | C6 is listed PASSÉ and asked that the rule in the conventions file carry nothing of its provenance, the mark and the citations living on the coverage line alone; the file keeps `off-grid` on the rule as a fifth field and moves only the entry citations off it, so the pass is applied differently than asked. |
| F02 | NOTE | pre-existing | 1 | passes/architecte.md L290-311 (C12) ↔ architecte.md L305-308 | C12 is listed PASSÉ, yet the *What you never do* bullet still lists "a manifest" beside "a build file" as a class of its own, the very reading C12 asked to remove once L81 made the manifest one of the build files. |
| F03 | NOTE | pre-existing | 1 | passes/architecte.md L390-403 (C16) ↔ 7_lots.md L155-156, 8_code.md L220-221 | C16 is listed PASSÉ; its agent half is there (L696-698) but its command half — "the same wording holds for the commands' glob" — is not: both commands still trigger invocation 3 on "a request with an empty `## Verdict`" and say nothing of an absent heading. |
| F04 | NOTE | pre-existing | 1 | passes/architecte.md L443-460 (C19) ↔ architecte.md L453-455, L511-514, L685-687 | C19 is listed PASSÉ and named four targets; only the example ("a segment" → "a record", L516) changed, while the four-hundred-tokens justification, the "not through any carelessness" paragraph and the invocation 3 "and for good reason" preamble stand verbatim. |
| F05 | NOTE | pre-existing | 1 | passes/architecte.md L518-536 (CMD2) ↔ conventions.md L170-176 | CMD2 is listed PASSÉ and asked that the invocation example show the invocation 3 form (working folder from the second argument); the example shows invocation 1 only. |
| F06 | NOTE | refonte | 1 | modifications.md L636-653 ↔ architecte.md L247, L359, L377-378 | Three changes are in the file and nowhere in the index: a `## Invocation` field added to the blocking file, the rename of a settled blocking file moved from the agent (`git mv` in the previous round) to the orchestration, and the report grown from three lines to five. |
| F07 | TO FIX | refonte | 2 | architecte.md L291-292 ↔ architecte.md L195-198 | *What you never do* still lets an off-grid rule stand when it "cites the entries that motivate it", while *The coverage file* forbids any entry number on the rule, so an off-grid rule is written with citations under one rule and without under the other. |
| F08 | TO FIX | refonte | 2 | architecte.md L382-384 ↔ architecte.md L272-273 | "You never wrote one at invocation 3" is contradicted by the table that has the orchestration-called invocation 3 write a blocking file like anywhere else, so an Arbitre-called run that finds a root `blocked_architecte.md` left by an earlier end-of-lot run has no rule for it. |
| F09 | TO FIX | refonte | 2 | architecte.md L39-45 ↔ architecte.md L330, L724-726 | Invocation 3 runs on a `bugfix-NN/` that holds no `couverture.md` (invocations 1 and 4 write it, on a feature folder only), yet every rule it adds "gets its `couverture.md` line too" and the table lists the file as an input, so on a correction cycle the line goes into a file that does not exist and nothing says whether to create it or skip it. |
| F10 | NOTE | refonte | 2 | architecte.md L124-128 ↔ architecte.md L140 | The rule line is "four fields, in this order" with the test kind last and `off-grid` fifth, and three lines later the trigger mark goes "at the end of the line", so two rule shapes are ordered and the Réalisateur's `permanente` filter reads one of them by luck. |
| F11 | NOTE | refonte | 2 | architecte.md L296-297 ↔ architecte.md L98, L797 | "Invocations 2 and 3 read the one in force" is the pre-invocation-4 wording left beside the new rule that 2, 3 and 4 read it, so the exception to the never-open bullet does not name the invocation that reads the file whole. |
| F12 | NOTE | refonte | 2 | architecte.md L600-601 ↔ architecte.md L797-799 | "At 4 it is integration only" while invocation 4 runs moves 2 to 10 of invocation 1, which derive (moves 5 and 6) before 6b integrates, so the sentence describes an invocation 4 the file does not define. |
| F13 | NOTE | refonte | 2 | architecte.md L585-587 ↔ architecte.md L580 | "A directive never becomes a question" stands two lines above the table row that turns a directive contradicted at invocation 4 into a `Kind: replacement` question, so the absolute rule and its one exception are not reconciled. |
| F14 | NOTE | refonte | 2 | architecte.md L477-478 ↔ architecte.md L72 | A platform fact is "looked up, never recalled — at every invocation" while the web is open to invocations 1, 3 and 4 only, so invocation 2 is ordered to look up what it has no permission to look up. |
| F15 | NOTE | refonte | 2 | architecte.md L523-525 ↔ architecte.md L536-544 | A question entry is "four lines" and the `Kind:` line makes it five, so the count and the second example disagree. |
| F16 | NOTE | refonte | 2 | architecte.md L215 ↔ architecte.md L222-223 | The report is "five lines at most" and carries "every `coverage` question, one line each", so a run raising two coverage questions cannot obey both. |
| F17 | NOTE | refonte | 2 | architecte.md L728-729 ↔ architecte.md L460-461 | The `couverture.md` line at invocation 3 is justified by "the next invocation's coverage check finds a rule it cannot place", but move 9 checks entries in the first column, never rules, so the justification names a check no move performs. |
| F18 | TO FIX | pre-existing | 4 | conventions.md L174-175 ↔ architecte.md L611-612, L101-102, L557 | The prompt carries only the number of the questions file to write; the answered file invocation 2 must read is named nowhere and listing the folder is forbidden, so invocation 2 has no permitted way to find its input. |
| F19 | TO FIX | pre-existing | 4 | arbitre.md L414-420 ↔ 8_code.md L235-240, architecte.md L268-273 | The Arbitre and the orchestration send a word-for-word identical prompt ("Working folder: … Invocation 3 — Requests."), while the agent's block-or-refuse branch "depends who called you", so the caller is a fact the prompt never carries and the two-agents-waiting case the file guards against is decided by guess. |
| F20 | NOTE | unknown | 4 | arbitre.md L264-265 ↔ architecte.md L253-257 | The Arbitre reads an Architecte block as "asks for a rule nobody has written" while the agent blocks on a missing input or an unplaceable directive only, so the one reader that names the block's meaning names the wrong one. |
| F21 | NOTE | unknown | 4 | docs-new/process/GRILLE_CONVENTIONS.md L50-52 (R4) ↔ architecte.md L294 | The grid's R4 sends a missing form "back as a conventions request in `architecte/`", and no move of the agent writes a request, so the grid's route for the case has no producer. |

Checked and found sound: the frontmatter (every tool used, every gesture tooled — Glob for `architecte/`, Grep for filled verdicts, WebSearch/WebFetch at 1, 3 and 4, no Bash, no rename); C1-C5, C7-C11, C13-C15, C17, C18, C20 (écarté) and CMD1, CMD3-CMD8 against the file and the three commands; the grid's names (Part A, V1-V10, V6, *The shape of the file*, twelve sections, Part B C1-C12, R2/R3), the natures of the coverage example, `tracabilite.md`'s shape, `par-genre/directives.md` written by `/5_reclasse`, the `## Verdict` heading written by all four requesters, the `permanente`/`spécifique` marks read by the Détailleur, Réalisateur, Relecteur, Concepteur and Testeur, and the `## Invocation` field read by `/conventions`.

| # | Status | Where | One line |
|---|---|---|---|
| C1 | fixed | `.claude-new/agents/architecte.md:295` | |
| C3 | fixed | `.claude-new/agents/architecte.md:402–411, 636–639, 219–221` · `.claude-new/commands/conventions.md:226` | |
| C5 | other | `.claude-new/agents/architecte.md:72–75, 477–481, 329, 332` | The web is opened to invocations 1, 3 and 4 (72–73), but the "holes filled from platform practice, and that alone" bound is absent, and table rows 1 and 4 still list no web among their inputs |
| C6 | other | `.claude-new/agents/architecte.md:128–129, 192–199, 292–293, 443` | The mark now sits on both the rule (fifth field, 128–129) and the coverage line by design, "nowhere else" withdrawn; 292–293 and 443 still have the rule cite the entries, which 197–198 forbids |
| C9 | fixed | `.claude-new/commands/conventions.md:97–100, 119–121, 174–175` · `.claude-new/agents/architecte.md:557–559` | |
| C12 | fixed | `.claude-new/agents/architecte.md:79–83, 701–704` | |
| C14 | fixed | `.claude-new/agents/architecte.md:331, 724–730` | |
| C18 | fixed | `.claude-new/agents/architecte.md:359–364, 381` | |
| C19 | open | — | |
| CMD1 | fixed | `.claude-new/commands/conventions.md:93–95, 119–121` | |
| CMD2 | open | — | |
| B-1 | fixed | `.claude-new/agents/architecte.md:209–210` | |
| B-2 | other | `.claude-new/agents/architecte.md:74–75, 478–481` | The sentence still stands at 478–481 and is now also at 74–75 |
| B-3 | other | `.claude-new/agents/architecte.md:119–127, 141, 155–158` | The Réalisateur sentence is replaced by an agent-neutral line deferring to each agent's own file (155–158); "at the end of the line" is now a field of the full rule-line example (119–127) |
| B-4 | open | — | |
| B-5 | fixed | `.claude-new/agents/architecte.md:620–625` | |
| B-6 | other | `.claude-new/agents/architecte.md:371, 374–375, 565–570` | "himself/his" became "herself/her", but 569–570 still reads "a directive she judges wrong, he changes himself" |
| B-7 | fixed | `.claude-new/agents/architecte.md:69–71, 76–83` | |
| B-8 | fixed | `.claude-new/agents/architecte.md:381` | |
| C-1 | fixed | `.claude-new/agents/architecte.md:359–360, 377–379` · `.claude-new/commands/conventions.md:148–154` | |
| C-2 | moot | `.claude-new/agents/architecte.md:377–379` · `.claude-new/commands/conventions.md:152` | The agent no longer renames the blocking file; the command does the `git mv` and computes `NN` |
| C-3 | fixed | `.claude-new/agents/architecte.md:79–87` | |
| C-4 | fixed | `.claude-new/commands/conventions.md:97–100, 175` · `.claude-new/agents/architecte.md:557–559` | |
| C-5 | other | `.claude-new/agents/architecte.md:72–73, 329, 332` | As D-2: the web is granted at 72–73 for 1, 3 and 4, while table rows 1 and 4 still list it under invocation 3 alone |
| C-6 | other | `.claude-new/agents/architecte.md:675–676` | `Grep` is now named once, at invocation 3 ("grep the folder for a filled one"); the other uses still read as reading |
| C-7 | open | — | |
| D-1 | other | `.claude-new/agents/architecte.md:43–45, 98, 296–298, 341–343, 346` | Four of the five counts now include invocation 4; 296–298 still says "Invocations 2 and 3 read the one in force" |
| D-2 | other | `.claude-new/agents/architecte.md:61–62, 72–73, 329, 332` | 72–73 grants the web at 1, 3 and 4 and the old bans at 69 and 552–555 are gone, but table rows 1 and 4 still list the web under invocation 3 alone, and 61–62 keeps an input listed against another invocation unopened |
| D-3 | fixed | `.claude-new/agents/architecte.md:234–239, 268–274, 772–778` | |
| D-4 | fixed | `.claude-new/agents/architecte.md:219–221, 546–548` | |
| D-5 | other | `.claude-new/agents/architecte.md:708–710, 717` | The heading now says "the two filters below — the third row is not one", but the row that says "Not this one" is the second (717); the third is a filter |
| D-6 | fixed | `.claude-new/agents/architecte.md:496–497, 536–548` | |
| D-7 | fixed | `.claude-new/agents/architecte.md:223–224, 643–654` | |
| D-8 | fixed | `.claude-new/agents/architecte.md:393, 444–452` | |
| D-9 | fixed | `.claude-new/agents/architecte.md:797–803` | |
| D-10 | fixed | `.claude-new/agents/architecte.md:580–581, 816–817` | |
| D-11 | fixed | `.claude-new/commands/conventions.md:97–100, 119–121, 175` | |
| D-12 | fixed | `.claude-new/agents/architecte.md:331, 724–730` | |
| D-13 | other | `.claude-new/agents/architecte.md:66–67, 305–309, 701–704` | "Somewhere" is bounded (701–704) and the manifest left 66–67, but the never-list at 305–306 still names "a manifest" beside "a build file", the exception at 307–309 covering it by inference only |
| D-14 | other | `.claude-new/agents/architecte.md:128–129, 192–199` | The mark is now on both the rule and the coverage line by design; "There, and nowhere else" withdrawn |
| D-15 | fixed | `.claude-new/agents/architecte.md:119–129` | |
| D-16 | fixed | `.claude-new/agents/architecte.md:421–425` | |
| D-17 | fixed | `.claude-new/agents/architecte.md:359–364` | |
| D-18 | fixed | `.claude-new/agents/architecte.md:620–625` | |
| D-19 | fixed | `.claude-new/agents/architecte.md:516` | |
| D-20 | fixed | `.claude-new/agents/architecte.md:215–226` | |
| D-21 | fixed | `.claude-new/agents/architecte.md:547, 552–556, 581` | |
| D-22 | other | `.claude-new/agents/architecte.md:675–676, 681–682, 696–699` | 675–676 now tests "filled → skip", which reads a missing heading as unfilled; 681–682 still says "no request with an empty `## Verdict`" |
