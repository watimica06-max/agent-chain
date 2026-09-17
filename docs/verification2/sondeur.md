# sondeur — verification 2

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | modifications.md L454 ↔ 4_grille.md L179/L299 | C10 is listed REPORTÉ (section order of the command) yet the change is there — `Git, before invoking` now precedes `The four invocations` and the git-after section was split off — so the `todo.md` entry describes work already done. |
| F02 | TO FIX | refonte | 1 | modifications.md L378-380 ↔ sondeur.md L398-400 | §3 is listed PASSÉ with a *défaut* grounded on « une règle transverse ou un motif déjà suivi », but the file admits the transverse rule as the only ground and forbids « the other blocks do it this way » — the pattern ground was dropped, not passed. |
| F03 | NOTE | refonte | 1 | passes/sondeur.md L508-511 ↔ sondeur.md L43 | C22 asked that the global invocation and a first-turn angle still read the product file whole; the file applies « always a list, never the file whole » to every invocation, so the global now locates its N blocks by N greps instead of one read. |
| F04 | NOTE | refonte | 2 | sondeur.md L48 ↔ sondeur.md L51-55 | « The prompt names two lists of blocks » heads a three-row table whose third row (out-of-scope) the global receives and invocation 3 receives none of, so the count is right for the angles only. |
| F05 | NOTE | refonte | 2 | sondeur.md L111 ↔ sondeur.md L119-121 | « Write the blocking file the prompt names you » is stated as the rule, but at invocations 1 and 2 the prompt names no blocking file unless a decision is filled, and the name is derived from `<out>` eight lines later — an agent obeying L111 at a fresh invocation 1 has no target. |
| F06 | TO FIX | refonte | 2 | sondeur.md L346-348 ↔ sondeur.md L419-431 | A feature block that does what an out-of-scope block excludes is « not your business » yet « goes to the Product Owner as an obligatory question naming both », and no `Block:` shape admits it — pass A takes one identifier, pass C takes `-`, and out-of-scope blocks reach the global only — so the case has no pass and no line to be written in. |
| F07 | NOTE | refonte | 2 | sondeur.md L81-82 ↔ sondeur.md L43 | Stop 1 is « a read that returned less than the file holds » while the reading rule forbids ever asking for the file, so taken literally every by-heading read qualifies; only the three observables that follow (truncation signalled, text ending mid-block, heading with no body) make the stop testable. |
| F08 | BLOCKING | refonte | 4 | sondeur.md L402-403 ↔ 4_grille.md L97-100 | The sondeur writes an accepted *défaut* as an empty `Answer:` (« empty means the Product Owner accepts the proposal »), and `/4_grille` stops on any `^Answer:$` hit in the latest root questions file without the `Défaut:` exception that `/1_lexique` L74-77 and `/2_structure` L29-31 carry — so a turn that produced one accepted *défaut* can never run the next grid turn, and the loop cannot close. |
| F09 | TO FIX | refonte | 4 | sondeur.md L398-400 ↔ GRILLE_CADRAGE_PRODUIT_V2.md L38-41 | The grid the agent reads whole grounds a *défaut* on « a transverse rule, or a pattern the file already follows … or the blocks that already follow the pattern », and the agent forbids exactly that ground — one sondeur following the grid writes what another following its file rejects, and the merge keeps both forms. |

Checked and found sound: the frontmatter (`Read`, `Grep`, `Write`) against every gesture, `Glob` removed with no listing gesture left; the five blocking-file names and the four prompts of `4_grille.md` against the agent's `<out>`, reading-order and invocation rules; the `Défaut:` line shape against `assembleur.md`, `redacteur.md` and `lexicographe.md`; `What pass A left you`, `C1.2`, `GRILLE_EXISTANT.md` E1–E4 and `PRODUIT_GLOBAL.md` as named.

| # | Status | Where | One line |
|---|---|---|---|
| A-§3 | other | `.claude-new/agents/sondeur.md:386–403` | (a) settled in favour of a separate `Défaut:` line with `Answer:` empty; (b) still a quotation ("the block and the words that found it"), not a paragraph reference |
| A-C6 | fixed | `.claude-new/agents/sondeur.md:203–211` | |
| A-C22 | fixed | `.claude-new/agents/sondeur.md:43, 180–182` | |
| A-C16 | fixed | `.claude-new/commands/4_grille.md:403–408` | |
| C20 | fixed | `.claude-new/commands/4_grille.md:500` | |
| B-1 | fixed | `.claude-new/agents/sondeur.md:44` | |
| B-2 | open | — | |
| B-3 | fixed | `.claude-new/agents/sondeur.md:158, 232` | |
| B-4 | fixed | `.claude-new/agents/sondeur.md:3` | |
| C — Glob unused | fixed | `.claude-new/agents/sondeur.md:4` | |
| C — Grep unnamed | fixed | `.claude-new/agents/sondeur.md:67–77` | |
| D-1 | fixed | `.claude-new/agents/sondeur.md:3, 24–30, 160–170` | |
| D-2 | fixed | `.claude-new/agents/sondeur.md:79–91` | |
| D-3 | fixed | `.claude-new/agents/sondeur.md:38–46` | |
| D-4 | fixed | `.claude-new/agents/sondeur.md:386, 402` | |
| D-5 | fixed | `.claude-new/agents/sondeur.md:306, 398–400` | |
| D-6 | fixed | `.claude-new/agents/sondeur.md:184` | |
| D-7 | fixed | `.claude-new/agents/sondeur.md:43, 180–182` | |
| D-8 | fixed | `.claude-new/agents/sondeur.md:54` | |
| D-9 | fixed | `.claude-new/agents/sondeur.md:289–291` | |
| D-10 | fixed | `.claude-new/agents/sondeur.md:119–123` · `.claude-new/commands/4_grille.md:51, 281, 289–291` | |
| D-11 | fixed | `.claude-new/agents/sondeur.md:247` | |
| D-12 | open | — | |
