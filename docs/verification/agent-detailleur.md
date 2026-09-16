# Vérification — `detailleur.md`

Files read: `.claude/agents/detailleur.md` (old, 599 lines),
`.claude-new/agents/detailleur.md` (new, 681 lines),
`docs/refonte/passes/detailleur.md`, `docs/refonte/modifications.md`
lines 1013–1082 (`# detailleur.md`). Cross-checks by grep only:
`.claude-new/agents/{arbitre,relecteur,realisateur,verificateur}.md`,
`.claude-new/commands/{7_lots,8_code}.md`.

Line numbers below are those of the **new** file unless marked *old*.

Pass sheet, as modifications.md states it: **Passés (18)** C1–C18 ·
**Reportés (3)** C19–C21 (all on `/8_code`, to pass with A3) ·
**Écartés (0)**. Structural modification: **U10** (one blocking file
with several entries) and its cascade on the Arbitre. The pass file
also carries one unnumbered conditional comment (under "D12", move 8
"Every 🔴 rule"), which modifications.md does not list.

---

## A. Conformity

| # | Expected (pass file) | Found (new file) | Verdict |
|---|---|---|---|
| **C1** | One rule: a settled file is renamed to its numbered form, never deleted; the second passage ("Delete the file once applied") goes, its concern being already met two paragraphs above | Lines 444–449: "Delete" replaced by "Rename the file once applied, by `git mv`, to `blocked_<agent>-NN.md` — the highest number beside it, plus one. Never delete it…". Contradiction gone | **Fixed in substance, approximate in form.** The pass asked for *one* rule; the file now states it three times (row 421, lines 425–435, lines 444–449). Two side effects: the placeholder `blocked_<agent>-NN.md` in a file that elsewhere writes `blocked_detailleur-NN.md` (333, 414, 421), and two numbering formulas — "next free number" (421) vs "highest number beside it, plus one" (445). See D-4, D-5, D-6 |
| **C2** | An observable test for "the split has been redone" (`code/redecoupage.md` gone), and a rule for the redone case: rename to numbered form, detail the block | Lines 422–423: two rows, "and `code/redecoupage.md` is still there → Stop" / "and gone → the split was redone — rename the file to its numbered form and detail the block" | **Fixed as asked.** Cross-check holds: the Vérificateur archives `code/redecoupage.md` when the sequence is written (verificateur.md new ~449), and `/8_code` new 311–313 has the matching stop row |
| **C3** | An explicit rule in the walk for a lot that already carries a sheet: PASS → never touched; no PASS → skipped or rewritten, one of the two stated | Lines 467–473: table — PASS → never touched · no PASS → skip · no sheet → write | **Fixed as asked** (skip chosen, matching `/8_code` new 300–302). Consequence not handled: knowing "its verdict is PASS" requires reading `code/<lot>/verdict.md`, which "What you read" does not list and the divergence mode forbids — see D-3 |
| **C4** | (a) The walk greps, per lot, the symbol the lot declares produced or modified, on the code folders. (b) A sentence for the residual case — a stop found at move 4 on a later lot: the sheets already written stand; the command deletes them if the split changes | (a) Lines 461–465: present. (b) **Absent** — nothing in PART 3 says what becomes of sheets already written when a stop surfaces at move 4 | **Half applied.** (b) is missing; "you have written no sheet at this point" (337) stays false for the residual case, which is exactly what the comment was about. The new sentence also says "two of your three block causes" — a count the file's own list of causes (281–283) does not support, see D-2 |
| **C5** | Pass file: one blocking file *per lot*, Arbitre called once *per file* sequentially, no decision applied until all are back, one back-to-split ends the invocation | Lines 475–508: **one** file with `## Blocking N` entries, Arbitre called **once**, no decision applied until it returns, one back-to-split ends the invocation | **Conforms to U10** ("La demande" §1), which deliberately supersedes C5's one-file-per-lot shape. The Arbitre side of the cascade is in place (arbitre.md new 129–140). What neither U10 nor the file settles: **where** the single file lives when the stops span several lots — see D-8 |
| **C6** | Drop the `## Defects` clause of the `code/sequence.md` bullet (the cleaner option), or give it the blocking-file form | Lines 64–65: clause removed | **Fixed as asked** (drop) |
| **C7** | Move 2 runs once, in the walk or just before the per-lot loop; the per-lot list starts at move 3 | Line 544–545: move 2 keeps its place and number inside "The eight moves, per lot of the block", with "once, before the per-lot loop: they do not change between lots" added | **Fixed in substance, not in form.** The read is now once. But the list still starts at 1 under a heading that says "per lot", and move 1 too is fully done by the walk (513–514 "You have already read what move 1 opens") — the per-lot list effectively starts at 3 and the file does not say so |
| **C8** | Move 4 names two greps per symbol (code folders + state document); move 2 loses its forward reference | Lines 574–575: "grep it on `docs/CURRENT_TECHNICAL_STATE.md` too — two greps per symbol, not one". Lines 549–550: move 2 still says "the rest of that file you grep, symbol by symbol" | **Half applied.** The two greps are there; the forward reference in move 2 was kept. Not contradictory now, merely said twice |
| **C9** | A foreseen fallback when the conventions name no code folder: a conventions request, or a stop. Not a bare grep | Lines 571–572: "that is a conventions request, and the lot waits on it. Never a bare grep instead" | **Fixed, but the fix contradicts another rule.** "the lot waits on it" collides with "You never block on this … carry on" (362–363), and no mechanism exists for the wait — see D-7 |
| **C10** | For a producer in an earlier block, "not found" is a stop / blocking file naming the lot that promised it; the "earlier lot" row stays only for the same block | Lines 584–585: row split in two — "earlier lot **of this block** → legitimate" / "a lot **of an earlier block** was to produce it → A block … Name the lot that promised it" | **Fixed as asked.** Note the pass file itself observed the same-block row is already covered by the row above it (583); the redundancy was kept — D-13 |
| **C11** | Move 5's primary grep scoped to the working folder's `code/` | Line 607: `Grep(pattern: "<symbol>", path: "code/", glob: "**/compte-rendu.md")` | **Fixed as asked** |
| **C12** | Move 5 runs only on a found symbol that `## Symbols` does not place | Lines 602–604 | **Fixed as asked.** The sentence that results is hard to parse (three dashes, two verbs) — cosmetic |
| **C13** | A move writes `## Dependencies` from the classification of moves 4 and 5: one line per type the signature uses and the lot does not produce, with provenance | Lines 625–631: new move 8, exactly that; former move 8 becomes 9 | **Fixed as asked.** The renumbering was not carried to the section heading — D-1 |
| **C14** | Divergence mode as a list against the normal run: PART 2 yes; no re-walk; moves 3–8 on named lots; diverged symbol from code by grep; plus reading the block's other uncoded sheets; lots from the prompt; the verdict file not an input **or** in the on-disk table | Lines 661–675: prompt names the lots, "you read no verdict file"; table: PART 2 yes · walk no · moves 3 to 9 on named lots · other uncoded sheets read; rewrite against the code by grep | **Fixed as asked** — except that the pass's *or* was applied on both sides: the verdict is now both "not read" (661) and in the on-disk table as read for its `## Status` (45). D-3 |
| **C15** | Every file the agent touches has an on-disk row: the report at least, the verdict if it stays an input | Lines 44–45: rows for `compte-rendu.md` ("grepped, never opened") and `verdict.md` ("its `## Status` line, to know a lot is coded") | **Fixed as asked**, with the D-3 consequence |
| **C16** | Moves 3 and 7 name the section instead of "see below" | Lines 556, 623 | **Fixed as asked** |
| **C17** | The Written / Not enough table and the `§3` example in neutral shapes — a nullable stream, a list, a signed duration — or the rule alone | Lines 157–158 neutralised ("a nullable stream of the entity", "a stream of a list"); line 254 `Context` → "the platform's ambient handle". Line 159 still `delta(a, b): Long` … `Long` alone | **Two rows of three.** The pass file named `Long` explicitly among the platform vocabulary and asked for "a signed duration"; the third row is unchanged. Minor |
| **C18** | Remove the justification passages: "The second kind is the one that goes missing … no calculation fails without it"; "Why nothing first…" and the paragraph after; "The Vérificateur read these same sections — not a duplicate"; "The sheet says it, it does not decide it" (keeping the "eight lots twice" arithmetic if C4 is applied) | Lines 190–193, 519–525, 91–93, 151–153: **all four passages unchanged.** No diff hunk touches them | **Not applied, though listed PASSÉ.** The record and the file disagree. The defect itself is tokens-only; the mismatch in the record is the finding |
| **C19–C21** | Reportés — on `/8_code`, to pass with A3 | Nothing in `detailleur.md` corresponds, correctly. `/8_code` new lines 76–79 and 311–313 show C19 and C20 applied there | **Consistent** with "to pass with A3": deferred out of this file, not discarded |
| **D12 (unnumbered, conditional)** | Move 8 (now 9) "Every 🔴 rule" drops every unmarked convention if the Réalisateur codes from the sheet alone; conditional on item 2 | Line 633–634 unchanged: "Every 🔴 rule". realisateur.md new 66–67 reads "the rules marked `permanente`, whole, and those the sheet's `## Conventions` names" | **Not listed, not applied — consistent.** Question: the Réalisateur's threshold is the `permanente` mark; the Détailleur's filter is the 🔴 mark. Is a convention that carries neither mark reachable by anyone? Not mine to settle |

---

## B. Unannounced changes

Every hunk of the diff maps to a numbered comment or to U10. Nothing
was moved, no section renumbered, no table rewritten beyond what the
comments asked. Three sub-hunk deviations, none announced:

| # | Old | New | What it changes | Severity |
|---|---|---|---|---|
| B-1 | *old* 444: "🔴 **Delete the file once applied.**" | 445: "…to `blocked_<agent>-NN.md`" | A generic placeholder where the file elsewhere writes `blocked_detailleur-NN.md`. The identical paragraph sits in realisateur.md:464 and relecteur.md:289 — a shared paragraph pasted into three agents without instantiating the name. Read literally, a reader could produce a file named `blocked_<agent>-03.md` | NOTE |
| B-2 | *old* 422: "rename it `blocked_detailleur-NN.md`, next free number" (kept at 421) | 445: "the highest number beside it, plus one" | Two numbering rules. They differ when the sequence has a gap (`-01`, `-03` present: next free is 02, highest+1 is 04). Either is fine; two is one too many | NOTE |
| B-3 | *old* 476: "## The eight moves, per lot of the block" (unchanged at 529) | Moves now run 1–9 | An unannounced consequence of C13: the count in the heading is false. See D-1 | TO FIX |

Nothing else. In particular the frontmatter (description, tools,
model, effort) is byte-identical.

---

## C. Gestures against tools

Frontmatter tools: **Read, Grep, Glob, Edit, Write, Agent.** No Bash.

**Gestures with a tool**

| Gesture | Lines | Tool |
|---|---|---|
| Read sequence, lot list, preamble, cited entries, state-document sections, conventions whole, blocking files, other uncoded sheets | 64–83, 412–415, 544–550, 671 | Read |
| Grep code folders per symbol, with a path | 461, 565–566 | Grep (`path`) |
| Grep the state document per symbol | 574 | Grep |
| Grep the reports with `path` + `glob` | 607 | Grep (both parameters exist; the fallback at 609 "if `glob` is not available" is dead but harmless) |
| Look for `blocked_detailleur.md` / `-NN.md`, check `code/redecoupage.md` presence | 412–415, 422–423 | Glob |
| Write the sheet, the blocking file, the `architecte/` request ("create the folder if it is not there" — Write creates parents) | 229, 278, 350–351 | Write |
| Rewrite a sheet in divergence mode | 673 | Edit / Write ("When `Edit` fails", 398–404, serves this) |
| Invoke the Arbitre, wait | 315–323 | Agent |

**Gestures with no tool**

| # | Gesture | Lines | Finding | Severity |
|---|---|---|---|---|
| C-1 | **Rename a file** — "`git mv`, or the equivalent: one file, under a new name. Never write the numbered one and leave something at the old name — not a copy, not a note, not an empty file" | 421, 423, 425–428, 444–449 | No Bash, and Read/Write/Edit can neither move nor delete a file. With this toolset the only "equivalent" is Write the numbered copy and leave the original — which lines 426–428 forbid in so many words, and which line 430 says re-blocks the next run. The Réalisateur, given the same paragraph, has Bash; this agent does not. The rule is mandatory on three rows of PART 2 (421, 423, 444) and one of the Arbitre table (333). **The agent cannot do what four 🔴 rules require.** Pre-existed in the old file (old 425), but the new file leans on it harder (C1, C2 both resolve into "rename") | BLOCKING |
| C-2 | **"the lot waits on it"** (a conventions request for a missing code folder) | 571–572 | A wait with no counterpart: the agent may invoke nothing but the Arbitre (391–392), and the Architecte is reached only through the orchestration at the end of a lot or through the Arbitre. No blocking file is written, so `/8_code` has no row for it either. Also in D-7 | TO FIX |

**Tools no gesture uses**

None strictly. `Edit` is reached only by the divergence rewrite (a
whole-sheet `Write` would do as well) and by the "When `Edit` fails"
section that exists for it. `Glob` is used for file discovery. Nothing
to remove.

---

## D. Internal coherence (new file alone)

| # | Line | Quote | Finding | Severity |
|---|---|---|---|---|
| D-1 | 529 | "## The eight moves, per lot of the block" | Nine moves follow (531–633); line 670 itself says "Moves 3 to 9". Announced count does not match | TO FIX |
| D-2 | 462 | "Two of your three block causes show only in a grep" | The file's own list of causes (281–283) is: an ambiguous rule · a grep contradicting the declaration · a missing input. Only one of those is grep-based. The "three" is the pass file's count (which paired the grep contradiction with "a type nobody declares", 594–595), not this file's. And the walk grep — "the symbol it declares as produced or modified" — catches the declaration contradiction, but does it catch an undeclared type the signature *consumes*? Signatures are not derived in the walk. Question rather than verdict: does the walk grep reach both grep-based causes, as the sentence claims? | TO FIX |
| D-3 | 45 vs 661–662 vs 62–89 | 45: "a lot's verdict — its `## Status` line, to know a lot is coded" · 661: "🔴 you read no verdict file" · 88: "🔴 Nothing else." | The verdict is read (45, and needed by 471 "its verdict is `PASS`"), not read (661), and absent from "What you read", whose closing rule excludes it. Three statements, two compatible at most. Likely intent: 661 means *the divergence verdict*; it does not say so | TO FIX |
| D-4 | 445 | "`blocked_<agent>-NN.md`" | Elsewhere `blocked_detailleur-NN.md` (333, 414, 421). Same file name under two spellings | NOTE |
| D-5 | 421 vs 445 | "next free number" / "the highest number beside it, plus one" | Two numbering rules for one rename (differ on a gap) | NOTE |
| D-6 | 425–435 and 444–449 | "Renaming is what closes it — never delete it. The numbered ones are the record…" / "Never delete it, never leave anything at the unnumbered name: the numbered ones are the record…" | The same rule, twice in one section, plus row 421. C1 asked for one | NOTE |
| D-7 | 571–572 vs 362–363 | 571: "that is a conventions request, and the lot waits on it" · 362: "You never block on this. Write the signature against the conventions as they stand, and carry on." | A conventions request now has two behaviours: carry on (362) and wait (571). Nothing says how a lot waits (no file, no agent to call, no `/8_code` row), nor which `<lot>` the request `architecte/detailleur-<lot>.md` names when the missing folder is met in the walk (461), before any lot is being detailed — the walk needs the folder too, so it is the whole block, not "the lot", that cannot proceed. On a fresh project with a hand-written conventions file this is the first branch the agent hits, and it leads nowhere | TO FIX |
| D-8 | 477–494 vs 278, 321, 412–413 | 477: "One blocking file, with one entry per stop" · 278: "Write `code/<lot>/blocked_detailleur.md`" · 321: `Blocking file: code/<lot>/blocked_detailleur.md.` | Every path to the blocking file carries one `<lot>`; a file holding "Blocking 1 — lot-04" and "Blocking 2 — lot-07" has no stated home. Consequences: the Arbitre prompt names one lot; PART 2's per-lot scan finds it only under whichever lot it was filed in; the numbered record of a block on lot-07 ends up in lot-04's folder; `/8_code` 4b looks "in `code/<lot>/`" of the *current* lot. Question: does the multi-entry file go under the first lot that stopped, or somewhere else? | TO FIX |
| D-9 | 287–301 vs 480–494 | Single shape: `## What blocks / ## Where / ## To resume / ## Decision` · Multi shape: `## Blocking N` → `### What blocks / ### Where / ### To resume`, then `## Decision` | Two shapes for one file; not stated whether a single stop uses the first or the second with N=1. The Arbitre accepts both (arbitre.md new 129), so nothing breaks, but PART 2's "read them" (415) and `/9_controle`'s gathering meet two layouts | NOTE |
| D-10 | 387 vs 669 (and 3, 337) | 387: "🔴 Write a sheet before walking the whole block" (never do) · 669: "The walk — ⚠️ No" · 3: "Walks the whole block before writing any sheet" | The divergence mode writes sheets without walking; the never-do and the description forbid it without exception. The pass file flagged this exact literal reading; the never-do was not amended | TO FIX |
| D-11 | 585 | "🔴 **A block** — that lot is coded and reviewed" | "block" as *blocking*, in a table whose other rows use "block" as *group of lots* (583, 584: "of this block"). The double sense pre-exists (389, 439, 668), but here both senses sit three rows apart | NOTE |
| D-12 | 461 vs 565–572 | 461: "one grep of the symbol … on the code folders" | The walk is described (and run) before move 4 tells the reader which folders those are and what to do when the conventions name none. A forward reference without a pointer | NOTE |
| D-13 | 583 vs 584 | "Not found, and a lot of this block produces it — Legitimate" / "Not found, and an earlier lot **of this block** produces it — Legitimate" | The second row is a subset of the first (the pass file said so). Kept | NOTE |
| D-14 | 625–628 vs 586 | 628: provenance is "*pre-existing*, or *produced by lot-NN*" · 586: a type "from the framework or a declared dependency" is legitimate | Which of the two labels does a framework type take in `## Dependencies`? Neither fits it literally. Question | NOTE |
| D-15 | 544–545 vs 455–459, 513–514 | 544: "once, before the per-lot loop" · 513: "Nothing stops you → detail them all … You have already read what move 1 opens" | Move 2 is now block-invariant but sits neither in the walk nor clearly after it: "before the per-lot loop" could be read as inside the walk (the walk *is* what runs before the loop). Since "a trap changes a signature" (552), should a trap that stops a lot surface in the walk? Question | NOTE |
| D-16 | 667–668 vs 421 | 668: "PART 2 — Yes — a standing block is still a block" · 421: "A `## Decision` filled → Apply it" | In divergence mode, a filled decision on a lot the prompt does not name has nowhere to be applied (only named lots are rewritten, 673). Edge case, unstated | NOTE |
| D-17 | 337–339 | "You have written no sheet at this point — the walk comes before the moves" | Still false for the residual case (a stop at move 4 on a later lot) that C4(b) asked to cover and that is not covered. Same finding as A/C4 | TO FIX |
| D-18 | 462–465 | "*« you have written no sheet at this point »* is false" | The sentence quotes line 337 to say it *was* false and the walk grep makes it true — but see D-17: it remains false for the residual case. A rule justified by a claim the file does not fully secure | NOTE |

---

## Summary

- **Conformity**: 14 of the 18 listed PASSÉ are fixed as asked (C2, C3,
  C5-as-U10, C6, C10, C11, C12, C13, C14, C15, C16, plus C1, C9, C17
  fixed in substance with a residue). **Three are half applied** — C4
  (no residual-case sentence), C7 (list not restarted at 3), C8 (move 2
  keeps the forward reference) — and **C18 is not applied at all**
  though listed PASSÉ. The three Reportés are correctly absent from
  this file. U10 is in place on both sides (Détailleur and Arbitre).
- **Unannounced**: none at hunk level; three wording side effects
  (B-1 placeholder, B-2 second numbering rule, B-3 stale "eight").
- **Tools**: one BLOCKING — the mandatory `git mv` rename (four 🔴
  rules) has no tool behind it: no Bash, and Read/Write/Edit can
  neither move nor delete. One TO FIX — a lot that "waits" on a
  conventions request with nothing to wait on.
- **Coherence**: seven TO FIX, the sharpest being D-3 (verdict read /
  not read / not listed), D-7 (conventions request both "carry on" and
  "wait"), D-8 (a multi-entry blocking file with no stated path) and
  D-1 ("eight moves", nine listed).
