| # | Severity | Origin | Section | Where | Finding |
|---|---|---|---|---|---|
| F01 | TO FIX | refonte | 1 | modifications.md L1284 ↔ arbitre.md L219-222 | The index records one write outside the blocking file — the trap — while the file declares three (`CURRENT_TECHNICAL_STATE.md`, `code/redecoupage.md`, a request in `architecte/`), so the index understates what the Arbitre writes. |
| F02 | NOTE | refonte | 1 | modifications.md L1283 ↔ arbitre.md L371-379 | The index says three of the four destinations skip the Architecte; the file sends the "rule now wrong" case to the Product Owner and then to the Architecte, so only two skip it — applied more narrowly than recorded. |
| F03 | NOTE | refonte | 1 | modifications.md L1283 ↔ arbitre.md L391-393 | The index names `## Traps` as the trap's destination; the file places it under `## Traps — general` or the subject's `###` and states that `## Traps` is not a heading — applied differently from the record. |
| F04 | NOTE | refonte | 1 | arbitre.md L148 ↔ modifications.md L1276-1285 | The Contrôleur was dropped from the blocks that are not the Arbitre's (L148, L260) and the index does not mention it. |
| F05 | NOTE | refonte | 1 | arbitre.md L429-431 ↔ modifications.md L1276-1285 | Two Verdict outcomes were added — "a rule already carries it", "refused, and it says what would settle it" — and the index does not mention them. |
| F06 | NOTE | refonte | 1 | arbitre.md L4 ↔ modifications.md L1276-1285 | `Bash` and `Skill` entered the tools, with the sleep-only rule at L443-446, and the index does not mention them. |
| F07 | NOTE | pre-existing | 3 | arbitre.md L100 ↔ arbitre.md L4 | "Its `## Status` line only" names no tool, and `Read` opens the whole verdict, so an agent that obeys the tool reads every coded lot's verdict whole; `Grep` is the tool and is never named for it. |
| F08 | NOTE | pre-existing | 3 | arbitre.md L4 ↔ arbitre.md L32 | `Glob` has no stated use anywhere in the body, yet the settled files "numbered beside it" and every lot's `verdict.md` (L348) can only be found by it — the agent guesses a `-NN` name and a miss reads as none. |
| F09 | TO FIX | refonte | 2 | arbitre.md L165-167 ↔ arbitre.md L181 | An unanswered entry is "a number with no answer" in one place and a number "simply absent" in the other, so the caller's test "some numbers answered, others not" has two shapes to read. |
| F10 | TO FIX | refonte | 2 | arbitre.md L173-176 ↔ arbitre.md L441-456 | On a multi-entry file the Arbitre settles the other entries, yet the wait branch orders "Leave `## Decision` empty and poll" and "stop, leaving `## Decision` empty" — whether the settled answers go in before the poll or after the 20 minutes, and what the poll tests on a half-filled field, is unwritten. |
| F11 | TO FIX | pre-existing | 2 | arbitre.md L441-462 ↔ arbitre.md L379 | The wait on the Product Owner describes only the empty outcome — nothing says what the Arbitre does when the poll finds her answer — and the new "rule in force that is now wrong" row needs that answer in `## What I need`, so that row leads nowhere. |
| F12 | NOTE | pre-existing | 2 | arbitre.md L82 ↔ arbitre.md L88 | "The blocking file the prompt names, and no other" is followed six lines later by an order to read the settled ones beside it. |
| F13 | NOTE | refonte | 2 | arbitre.md L402 ↔ arbitre.md L218 | The request is named `architecte/arbitre-<lot>.md` and asked "once for one block", but a multi-entry file carries entries on several lots, so which lot names the file and whether two entries needing a rule mean two requests is undefined. |
| F14 | NOTE | pre-existing | 2 | arbitre.md L193 ↔ arbitre.md L337-355 | "English, like every file the agents read" is contradicted by the French headings of `code/redecoupage.md`, a file the Cadreur reads. |
| F15 | TO FIX | refonte | 4 | arbitre.md L84-86 ↔ detailleur.md L284-285 | The Détailleur now writes `code/blocked_detailleur.md` at the split's root with entries on named lots (`## Blocking 1 — lot-04`, L295), so the folder test — root means "the split as a whole, and no lot exists yet" — misreads every Détailleur block and the lot's sheet (L98) is never opened. |
| F16 | TO FIX | refonte | 4 | arbitre.md L176 ↔ 8_code.md L168-170 | The missing number is what "says that entry still waits", but the orchestration tests `## Decision` on empty or filled only and renames a filled file once applied — and the Détailleur's re-run table (detailleur.md L437-439) has no half-answered row — so an entry handed to the Product Owner is archived unanswered. |
| F17 | TO FIX | pre-existing | 4 | arbitre.md L460-462 ↔ audit_blocages.md L112-115 | The audit expects a product question handed back to read "not settled here" with the behaviour it turned on, but the Arbitre writes nothing at all for a product question, so the audit's finding 4 never sees one. |
| F18 | NOTE | refonte | 4 | realisateur.md L135 ↔ arbitre.md L391-393 | The Réalisateur is told the Arbitre writes a `## Traps` section, the heading the Arbitre says does not exist, so the Réalisateur looks for a section that is never written. |
| F19 | NOTE | refonte | 4 | arbitre.md L129-130 ↔ detailleur.md L292-293 | The `##` single-entry shape the Arbitre still reads is one neither caller declares — both write `## Blocking N` "even when there is only one" (realisateur.md L258-259) — and survives only in realisateur.md L274-286, against its own L264-266. |
| F20 | NOTE | refonte | 4 | arbitre.md L159-160 ↔ realisateur.md L251-253 | The multi-entry file is attributed to the Détailleur alone, while the Réalisateur also adds a second lack to its own file. |
| F21 | NOTE | refonte | 4 | arbitre.md L388 ↔ socle.md L43 | `socle.md` names the Réalisateur as the only loader of `technical-state-format` and, at L28, the Arbitre as a reader of `CURRENT_TECHNICAL_STATE.md`, while the Arbitre now loads the skill and writes into the file. |

No pass sheet exists for `arbitre.md`; section 1 was worked against the index alone (`modifications.md` L1276-1318, plus U10 at L1019-1020).
Sound: the Architecte contract (prompt, `architecte/arbitre-<lot>.md`, empty `## Verdict`, refusal carrying what would settle it, verdict carrying rule text), the `code/redecoupage.md` hand-off to the Cadreur and 8_code, `code/<lot>/verdict.md` `## Status`, the `spec-technique.md`/`desc-bug.md` names, the `Bash` bound to `sleep`, the Détailleur's and Réalisateur's invocation prompts.

| # | Status | Where | One line |
|---|---|---|---|
| B1 | fixed | `agents/arbitre.md:173-176` · `agents/detailleur.md:346` | |
| B2 | fixed | `agents/arbitre.md:378` | |
| B3 | fixed | `agents/arbitre.md:379` | |
| B4 | fixed | `agents/arbitre.md:371-372` | |
| B5 | fixed | `agents/arbitre.md:157` | |
| C1 | fixed | `agents/arbitre.md:4`, `agents/arbitre.md:388-389` | |
| C2 | fixed | `agents/arbitre.md:113-114` | |
| C3 | fixed | `agents/arbitre.md:4`, `agents/arbitre.md:443-446` | |
| D1 | fixed | `agents/arbitre.md:377`, `agents/arbitre.md:391-393` | |
| D2 | fixed | `agents/arbitre.md:123-126`, `agents/arbitre.md:219-222` | |
| D3 | fixed | `agents/arbitre.md:371-372` | |
| D4 | fixed | `agents/arbitre.md:317`, `agents/arbitre.md:378` | |
| D5 | fixed | `agents/arbitre.md:379` | |
| D6 | fixed | `agents/arbitre.md:165-167`, `agents/arbitre.md:173-181`, `agents/arbitre.md:215-217` · `agents/detailleur.md:346` | |
| D7 | fixed | `agents/arbitre.md:173-176` | |
| D8 | fixed | `agents/arbitre.md:113-114` | |
| D9 | fixed | `agents/arbitre.md:128-130` | |
| D10 | fixed | `agents/arbitre.md:427-432` | |
| D11 | fixed | `agents/arbitre.md:384` | |
| D12 | moot | `agents/arbitre.md:162-163`, `agents/arbitre.md:238-239` | Nothing was asked — the note recorded a check, and it still holds: one `## Decision` per file, the anchor rule unchanged |
