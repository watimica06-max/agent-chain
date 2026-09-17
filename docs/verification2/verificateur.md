# Verification — `verificateur.md`

| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | NOTE | refonte | 1 | passes/verificateur.md L477-478 ↔ verificateur.md L485-494 | C17 is listed PASSÉ but applied differently than asked: the pass sheet asked one number per layer counting entries cited, the file's table and its rule count lots per block, and the index (modifications.md L1007) records the lots version as the correction. |
| F02 | NOTE | refonte | 1 | passes/verificateur.md L115-117, L137-138, L170 ↔ verificateur.md L69-87 | C3, C4 and C5 are listed PASSÉ but placed elsewhere than asked: C3 wanted the inventory in the Role path table and C4/C5 wanted the coded-lot rules inside the moves; all three sit under `What you read`. |
| F03 | NOTE | refonte | 1 | passes/verificateur.md L558-561 ↔ verificateur.md L24-25, L243-249, L287-288 | C20 is listed PASSÉ but the fresh-context rule still stands in Role and in Part 2 besides the never-do line, and the commentary "on a new application most needs look like that" survives at L287-288. |
| F04 | NOTE | pre-existing | 3 | verificateur.md L4 ↔ verificateur.md L57, L66-67, L69, L444-445 | Four partial reads name no tool (the preamble, the `## Ce qui est déjà codé` section, the `## Status` line, the previous `## Blocks`) where the entry-title read names grep, so an agent Reads the technical document whole to find its preamble and pays the read the file forbids. |
| F05 | TO FIX | refonte | 2 | verificateur.md L27-28 ↔ verificateur.md L93 | Every path is relative to the working folder, and `docs/TECHNICAL_CONVENTIONS.md` then resolves to `docs/features/<name>/docs/TECHNICAL_CONVENTIONS.md`, which does not exist, so the layer read at move 5 fails or the agent breaks the path rule to make it. |
| F06 | TO FIX | pre-existing | 2 | verificateur.md L453, L466 ↔ verificateur.md L485, L494 | Step 5b and the layer paragraph say the ceiling counts entries cited, the table header and L494 say lots and never entries, so two runs close blocks on different counts and the promise at L515-516 does not hold. |
| F07 | TO FIX | refonte | 2 | verificateur.md L57 ↔ verificateur.md L394-395 | The preamble is read "always" and on a `desc-bug.md` "there is none", so on a bug-fix the agent does not know whether to open it nor whether `Dependencies` settles what already exists. |
| F08 | NOTE | refonte | 2 | verificateur.md L93-94 ↔ verificateur.md L428-429 | The conventions are read for a section's layer "at move 5 too", but move 4's tie-break already keys on the layer of the lot just placed, so at move 4 the agent has no permitted source for it. |
| F09 | TO FIX | pre-existing | 2 | verificateur.md L503-504 ↔ verificateur.md L89-94 | On a bug-fix cycle the ceiling comes from a lot's layer "read from its bearer", but the reading list yields a layer for a section only and the code is forbidden, so the bug-fix ceiling has no input and the block size is guessed. |
| F10 | NOTE | refonte | 2 | verificateur.md L82 ↔ verificateur.md L444-445 | Coded lots head `## Order` "in the order they ran", but the previous `code/sequence.md` is opened for its `## Blocks` alone and `## Ce qui est déjà codé` is a bare list, so the order they ran in comes from nowhere the file names. |
| F11 | NOTE | refonte | 2 | verificateur.md L72 ↔ verificateur.md L141 | `surface` is defined as "a surface no lot builds" and also used for a coded lot whose verdict lost PASS, so the Cadreur reading the type is sent looking for an unbuilt operation where the fact is an unmerged lot. |
| F12 | NOTE | refonte | 2 | verificateur.md L105 ↔ verificateur.md L469-470 | `code/sequence.md` is announced with three headings and move 6 writes a fourth, `## Redécoupage: archivable`, so the announced shape and the written one differ on the very round the command reads for it. |
| F13 | TO FIX | unknown | 4 | verificateur.md L272-273 ↔ cadreur.md L753-754 | The `surface` kind crosses the operations the inventory lists against `Produces` and `Modifies`, which the Cadreur fills with symbols only, so the check collapses to the name crossing it says it is not and no `surface` can ever be raised. |
| F14 | TO FIX | refonte | 4 | verificateur.md L300-302 ↔ cadreur.md L573 | A caller one lot declares as the cascade of a changed contract is exempted from `overlap` when another lot modifies it for its own reasons, and the Cadreur calls that exact shape a defect to re-cut, so the Vérificateur waves through two lots touching one symbol. |
| F15 | TO FIX | refonte | 4 | verificateur.md L206 ↔ cadreur.md L818 | The Cadreur dispatches on "a `code/blocked_verificateur.md` with an empty `## Decision`" and the file never carries that heading, so the row that sends the Cadreur out without correcting never matches what is written. |
| F16 | TO FIX | unknown | 4 | verificateur.md L444-445 ↔ cadreur.md L822-823 | The Cadreur counts its rounds by archived `code/sequence-NN.md` files, the Vérificateur writes over `code/sequence.md` every round and nothing in `.claude-new/` archives it, so the count stays at one and the three-round bound never fires. |
| F17 | NOTE | refonte | 4 | verificateur.md L494 ↔ cadreur.md L106-107 | The Cadreur states that the Vérificateur counts entries cited per block while the Vérificateur's table counts lots, so whichever is right one file misdescribes the other. |
| F18 | TO FIX | refonte | 4 | verificateur.md L58, L394-395 ↔ diagnostiqueur.md L508-512 | `desc-bug.md` does carry a `## Preamble` (Intent, Out of scope, Dependencies) and no `Vocabulary`, so the `Vocabulary` read finds no heading on a bug-fix and the claim that there is no preamble is false. |
| F19 | QUESTION | unknown | 4 | verificateur.md L497-498 ↔ architecte.md L110-112 | The agent is sent to `docs/TECHNICAL_CONVENTIONS.md` for what the project calls the six role-named layers, and the Architecte's twelve sections take their titles from the grid with no instruction to map layers, so the mapping may not be there and every section takes the default ceiling. |
| F20 | NOTE | refonte | 4 | verificateur.md L111-114 ↔ 7_lots.md L31-32 | The command counts blocks from `code/sequence.md`'s headings while blocks are `block-N:` lines under one heading, so the relayed block count is three or four whatever the split. |
| F21 | NOTE | refonte | 4 | verificateur.md L206 ↔ 7_lots.md L247-249 | The command's general relay rule says the Product Owner fills `## Decision` of any `blocked_*.md` and the Cadreur reads it, which the Vérificateur's file never carries and the same command's row L147 already denies, so the orchestrator holds two instructions for one file. |
| F22 | NOTE | pre-existing | 4 | verificateur.md L206 ↔ cycle.md L88 | `cycle.md` routes a `verificateur` block "with `## Decision` filled" to `/7_decoupe`, a heading the file never carries and a command that does not exist, on a command `.claude-new/CLAUDE.md` L47-55 no longer lists. |
| F23 | NOTE | refonte | 4 | verificateur.md L462-463 ↔ cadreur.md L926 | The agent is asked to say in its report when a ceiling forced a block, and the Cadreur relays only the archivable line while `7_lots.md` L242-243 relays lots, blocks and defects, so the remark reaches nobody. |
| F24 | NOTE | unknown | 4 | verificateur.md L336 ↔ cadreur.md L572 | Move 2 says neither undeclared ordering shows in a `Needs` field, and the Cadreur declares the both-ends case as a need on the lot that removes the call, so the second kind arrives declared and L359-361 re-derives what `Needs` already says. |

Checked and found sound: the tools against the gestures (no `Edit`, no `Bash`, no rename asked of the agent); the eleven-word type list, the six kinds of move 1 and the two kinds of move 2 against their counts; C1, C2, C6–C16, C18, C19 and C21–C24 against the file and `7_lots.md`; `## Symbols`, `Anchor`, `(pre-existing)`, `called by`, the piece mark, `## Entries with no lot`, `^### §`, `## Ce qui est déjà codé`, `## Status` and the six layer names against the Cadreur, the Convertisseur, the Arbitre and the Relecteur.

| # | Status | Where | One line |
|---|---|---|---|
| C1 | fixed | `.claude-new/commands/7_lots.md:100–108` · `.claude-new/agents/cadreur.md:926–927` · `.claude-new/agents/verificateur.md:469–475` | |
| C3 | open | — | |
| C4 | other | `.claude-new/agents/verificateur.md:69–73` | The outcome now has a carrier (a `## Defects` line typed `surface`), but it still sits in the reading list, not in the move that handles coded lots |
| C5 | other | `.claude-new/agents/verificateur.md:75–83` | The table gained one row per move (2, 4, 5 split out), but it still sits under "What you read"; moves 1 and 3 say nothing about coded lots |
| C6 | other | `.claude-new/agents/verificateur.md:272–312, 334–335, 361, 368–374, 413–414` | Moves 1, 2 and 4 now name their type words; move 3's "badly cut" check (385–387) still carries no type |
| C9 | fixed | `.claude-new/agents/verificateur.md:147, 187–189` | |
| C10 | fixed | `.claude-new/agents/verificateur.md:269` | |
| C14 | fixed | `.claude-new/agents/verificateur.md:143, 368–370` | |
| C17 | fixed | `.claude-new/agents/verificateur.md:92–94, 497–498` | |
| C19 | fixed | `.claude-new/commands/7_lots.md:106–108` · `.claude-new/agents/verificateur.md:469–471` | |
| C20 | other | `.claude-new/agents/verificateur.md:24–25, 230–231, 243–249, 287–288` | "Rarer since he greps the code" and "These two checks protect the Détailleur" are gone; the fresh-context rule still stands in the Role (24–25) and in full at 243–249, and "on a new application most needs look like that" survives at 287–288 |
| C23 | open | — | |
| C24 | fixed | `.claude-new/commands/7_lots.md:45–75, 77, 186, 220–226` | |
| C25 | open | — | |
| B.1 | fixed | `.claude-new/agents/verificateur.md:263–265` | |
| B.2 | fixed | `.claude-new/agents/verificateur.md:118–119` | |
| B.3 | fixed | `.claude-new/agents/verificateur.md:120–122` | |
| B.4 | fixed | `.claude-new/agents/verificateur.md:143, 290–295` | |
| B.5 | fixed | `.claude-new/agents/verificateur.md:142, 280–282` | |
| B.6 | fixed | `.claude-new/agents/verificateur.md:323` | |
| B.7 | other | `.claude-new/agents/verificateur.md:453–454, 465–467, 485, 494` | The header "Lots per block" (485) and "The count is lots, never entries" (494) stand, but 453–454 now says "What the ceiling counts is entries cited, not lots" and 465–467 "you count entries per block" — the unit is stated both ways |
| B.8 | fixed | `.claude-new/agents/verificateur.md:199–200` | |
| C — "the conventions" read | fixed | `.claude-new/agents/verificateur.md:92–94` | |
| C — "say in your report that it can be archived" | fixed | `.claude-new/agents/verificateur.md:469–475` · `.claude-new/agents/cadreur.md:926–927` | |
| C — "say so in your report" (coded lot without PASS) | fixed | `.claude-new/agents/verificateur.md:71–73` | |
| D.1 | fixed | `.claude-new/agents/verificateur.md:469–475` · `.claude-new/agents/cadreur.md:926–927` · `.claude-new/commands/7_lots.md:100–103` | |
| D.2 | fixed | `.claude-new/agents/verificateur.md:269` | |
| D.3 | fixed | `.claude-new/agents/verificateur.md:118–119` | |
| D.4 | fixed | `.claude-new/agents/verificateur.md:432–434, 503–504, 510` | |
| D.5 | fixed | `.claude-new/agents/verificateur.md:92–94` | |
| D.6 | fixed | `.claude-new/agents/verificateur.md:82` | |
| D.7 | fixed | `.claude-new/agents/verificateur.md:147, 187–189` | |
| D.8 | fixed | `.claude-new/agents/cadreur.md:847–849` | |
| D.9 | fixed | `.claude-new/agents/verificateur.md:225–226, 420–423` | |
| D.10 | fixed | `.claude-new/agents/verificateur.md:334–335, 361` | |
| D.11 | fixed | `.claude-new/agents/verificateur.md:317` | |
| Q1 | fixed | `.claude-new/commands/7_lots.md:100–103` · `.claude-new/agents/cadreur.md:926–927` | |
| Q2 | fixed | `.claude-new/agents/verificateur.md:92–94` | |
| Q3 | fixed | `.claude-new/agents/verificateur.md:432, 503–504` · `.claude-new/agents/cadreur.md:78` | |
| Q4 | other | `.claude-new/commands/7_lots.md:45–75` · `.claude-new/agents/verificateur.md:24–25, 243–249` | C24 is now applied; C20 is applied in part only (see C20) — the recording question itself is not answered anywhere |
| Q5 | open | — | |
