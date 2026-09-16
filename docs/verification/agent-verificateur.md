# Vérification — `verificateur.md`

Old: `.claude/agents/verificateur.md` · New: `.claude-new/agents/verificateur.md`
Pass file: `docs/refonte/passes/verificateur.md` (25 comments, `### 1` … `### 25`)
Section of `docs/refonte/modifications.md`: lines 975–1011 — pass sheet only
(Passés 24, Écartés 1 = C25, Reportés 0). **No "Ce qui a changé" table and
no "La demande"** for this agent: "aucune modification du fichier de
travail ; sa fiche de passe est passée". One note in the section: C17 was
resolved the other way round from the pass file (the Vérificateur counts
**lots** per block, the Cadreur counts symbols; the duplicate ceilings
table was removed from the Cadreur).

Line numbers below refer to the **new** agent file unless a path says
otherwise. C21–C24 target `.claude/commands/7_lots.md` and are checked
against `.claude-new/commands/7_lots.md`; C25 targets `cycle.md`.

Summary: 17 of 24 listed-as-passed defects are fixed as asked. **Four are
listed PASSÉ and not, or only partly, applied**: C20 (fresh-context rule
still stated three times, commentary still there), C24 (section order of
`7_lots.md` unchanged), C14 (double citation outside contract/piece still
unsettled), C9 (two new defects with no type in the closed list). **One is
fixed in the agent and broken at the hand-off**: C1/C19 — the agent no
longer renames `code/redecoupage.md` and says "the command does it", but no
command and no agent in `.claude-new/` does it, and `7_lots.md` still says
the Vérificateur archives it (BLOCKING — see A.C1 and D.1). The new file
also carries a broken heading (`# PART 3` glued to the previous
paragraph), a stale count ("seven kinds" for six), a self-contradicting
example, and a bug-fix layer rule stated both ways.

---

## A. Conformity

### C1 — renames vs tools; `Edit` unused · PASSÉ

- Expected: the renames the body asks for and the tools agree — either
  the agent gets a tool that moves/deletes, or the archiving and
  renumbering are done by a party that has one (Cadreur or command) and
  the body stops asking; `Edit` and its failure section go.
- Found in the agent: line 4 `tools: Read, Grep, Glob, Write` — `Edit`
  gone; "When `Edit` fails" section gone; blocking-file rename gone with
  C8; move 6 (lines 441–445): "say in your report that it can be
  archived … You have no tool that renames a file — the command does it,
  once you have reported."
- Found at the hand-off: **nobody does it.** `grep -rn 'redecoupage-NN\|archiv' .claude-new/` returns only: the agent itself; `cadreur.md:827` (reads the `-NN` files); `commands/8_code.md:272` (counts the `-NN` files to bound the loop); and `commands/7_lots.md:76–78`, which still reads "**the Vérificateur keeps them where they ran and archives the file when the sequence is written**" — the old behaviour. No `git mv code/redecoupage.md code/redecoupage-NN.md` exists anywhere in `.claude-new/`. Compare `7_lots.md:96`, where the same command does perform the equivalent rename for `blocked_cadreur.md`.
- Also: "say in your report" (line 441) has no carrier. The agent's report is read by the Cadreur (its caller); `cadreur.md:771–779` reads only `## Defects` in `code/sequence.md` and says nothing about relaying an archive signal; `7_lots.md` "What you read" (lines 31–36) reads `sequence.md`'s `## Defects` and headings and `decoupage.md`'s `## lot-` headings, nothing else. No file carries "can be archived".
- Verdict: **CONFORME in the agent file; BLOCKING at chain level.** After a
  redécoupage whose split holds, `code/redecoupage.md` stays on disk:
  `8_code.md:312` ("`code/redecoupage.md` still there → run `/7_lots`")
  then re-enters the split, and the Cadreur (`7_lots.md:59`, "Re-splits
  what coding sent back") re-splits a split that already holds. The count
  of `redecoupage-NN.md` that bounds the loop (`8_code.md:272`) never
  increments.

### C2 — `docs/` path rule · PASSÉ

- Expected: one path rule, every path relative to the working folder,
  nothing about the repository root.
- Found: old lines 33–35 removed; lines 27–31 keep the single rule.
- Verdict: **CONFORME.**

### C3 — inventory named with its file · PASSÉ

- Expected: the inventory named with the file that carries it, "in the
  path table of the Role section alongside the lot list and the
  sequence".
- Found: lines 82–84, in "What you read": "it sits at the head of
  `code/decoupage.md`, above the lots". The path table (lines 33–37) is
  unchanged and does not carry it. Matches `cadreur.md:681` (`## Symbols`
  first in `code/decoupage.md`).
- Verdict: **CONFORME on substance, placement differs** — NOTE.

### C4 — `## Status` read feeds no move · PASSÉ

- Expected: a move names the case and its outcome; "the chosen outcome
  sits in the move that handles coded lots, not in the reading list".
- Found: lines 70–72, in the reading list: "One that does not is not
  coded: order it with the rest, and say so in your report". The moves say
  nothing about it; the new "What a coded lot is to each move" table
  (lines 74–80) does not mention it either.
- Verdict: **PARTIEL — NOTE.** Outcome exists, sits where the comment said
  it should not. "Say so in your report" — same carrier problem as C1: no
  section of `sequence.md` receives it and the Cadreur reads `## Defects`
  only. Question: is a coded lot without PASS meant to be a `## Defects`
  line (which type?), or silently re-ordered?

### C5 — what a coded lot is to each move · PASSÉ

- Expected: each move states what a coded lot is to it — move 1:
  productions pre-existing for holes, later modification not an overlap,
  not re-examined for dead/surface; move 3: entries not re-confronted.
  "The rule lives where the check is, not in the reading list."
- Found: lines 74–80, a table under "What you read" with exactly that
  content for moves 1 and 3; row "2 · 4 · 5 — As those moves already
  say". Moves 1 and 3 themselves are unchanged on this point.
- Verdict: **CONFORME on content, placement differs** — NOTE. See D.6: the
  row for move 4 points at a move that says nothing about coded lots.

### C6 — closed defect vocabulary; first-field rule · PASSÉ

- Expected: one closed list of type names, one per kind the moves raise,
  stated where the format is given "and used by every move that raises a
  defect"; a rule for the first field on an entry or a set of lots.
- Found: lines 121–147 — eleven words with a definition table; first
  field: lot id, entry number when attached to an entry and no lot, one
  line per lot when several. Eleven types map to the moves: six at move 1
  (`surface hole overlap orphan dead cascade`), `merge` at move 2,
  `anchor section bearer` at move 3, `cycle` at move 4.
- Not done: the moves do not use the words. Move 1's headings are still
  "An unbuilt surface", "A production nobody calls", "A contract changed
  without its cascade" (lines 263, 295, 299); move 2 ends "they are one
  lot — say so as a defect" (line 347) without `merge`; move 3 says
  "badly cut" (line 369), "missing an anchor" (373), "Entries from two
  sections are a defect" (357) without `section`. Only the piece
  paragraph (line 308–309) and the move-4 table (397–398) use the words.
- Verdict: **CONFORME on the list; PARTIEL on "used by every move"** —
  TO FIX. A reader at move 3 has to infer that "badly cut" is `anchor`.

### C7 — verbatim quote set apart · PASSÉ

- Expected: third field carries a verbatim copy of the contested line, set
  apart from the correction by a fixed separator; examples show it.
- Found: lines 111–116 examples with `"…" >> …`; lines 147–152 the rule
  ("between quotes", `>>`, "the Cadreur searches for it").
- Verdict: **CONFORME.** But the first example contradicts itself — see
  D.3.

### C8 — resume protocol removed · PASSÉ

- Expected: blocking file says what is missing and where, stops, no
  `## Decision`, no resume protocol; Part 2's table, numbering,
  rename-or-delete and "run the six moves again" go.
- Found: lines 185–200 three headings, no `## Decision`; old Part 2
  section replaced by "You never resume from a blocking file" (lines
  248–256): "You never rename it, and you never look for one."
- Verdict: **CONFORME.** Consistent with `cadreur.md:775` ("Go out without
  correcting") and `7_lots.md:97` ("it carries no `## Decision`").

### C9 — unforeseen block/defect cases · PASSÉ

- Expected: each case has a named outcome — defect "(with its type from
  comment 6)" for a cited entry that does not exist and a lot citing
  nothing; block for no technical document, two documents, no inventory.
- Found: lines 174–183 — three block cases as asked; "Everything else is
  a defect — an entry a lot cites that the document does not hold, a lot
  citing no entry at all".
- Not done: neither of those two defects has a type in the closed list
  (lines 130–145). `anchor` is "entries do not describe what it
  announces"; `section` is "a bare section, or entries from two of them".
  A non-existent entry and an empty `Anchor:` fit neither, and line 128
  forbids any other word.
- Verdict: **PARTIEL — TO FIX.** Two named defects the format cannot
  carry.

### C10 — kind 6 merged into kind 7 · PASSÉ

- Expected: one kind (changed signature or contract whose lot declares no
  caller and no fulfiller); "the list says six kinds"; "module stops
  compiling" commentary goes.
- Found: "A caller no lot declares" removed; `cascade` definition (line
  140) reads "A changed signature or contract whose lot declares neither
  caller nor fulfiller".
- Not done: line 260 still says "**note seven kinds of defect**" — the
  move now lists six. "between them the module does not compile" survives
  at line 342–343 (move 2, not the target of C10 — but the same
  toolchain wording).
- Verdict: **PARTIEL — TO FIX** (the count). See D.2.

### C11 — piece exception named per kind · PASSÉ

- Expected: the exception stated under each kind it excepts, or names
  those kinds explicitly.
- Found: lines 308–315: "the exception to two of these kinds — `dead` and
  `orphan` … It is not an exception to `cascade`".
- Verdict: **CONFORME.**

### C12 — coded-lot rule as a dependency, not a position · PASSÉ

- Expected: expressed in move 4's terms — as a dependency or as a
  tie-break; a correcting lot that is not eligible is not placed first,
  and the file says so.
- Found: lines 329–335: "creates a dependency: every uncoded lot
  consuming that symbol needs it … Never a position — the order comes out
  of move 4's algorithm … A correcting lot that is not eligible is not
  placed first".
- Verdict: **CONFORME.**

### C13 — cascade caller is not an overlap · PASSÉ

- Expected: the overlap kind states that a caller declared as the cascade
  of a changed contract does not count as naming the symbol when another
  lot modifies that caller — or the format keeps cascade callers out of
  `Modifies` and the file says where they are read from.
- Found: lines 287–289: "Nor is a caller one lot declares as the cascade
  of a changed contract — another lot modifying that caller for its own
  reasons is the shape move 2 orders, not an overlap."
- Verdict: **CONFORME.** Question left open: where in `code/decoupage.md`
  is a cascade caller declared? `cadreur.md:706–714` shows `Produces: X
  (called by lot-05)` and a bare `Modifies:`; the agent does not say which
  field it reads a "declared cascade" from. Also see B.4 — the same
  paragraph gained `Needs` in the overlap test, which the comment did not
  ask for.

### C14 — bearer defined; section-level citation; double citation · PASSÉ

- Expected: (a) "bearer" defined or pointed at where the technical
  document defines it; (b) a section-level citation is a named defect
  kind; (c) two lots citing one entry outside the contract/piece case is
  either a named defect or explicitly not one.
- Found: (a) lines 360–361 "A bearer is the symbol a bug-fix entry
  attaches its correction to — the technical document names it on the
  entry" (matches `cadreur.md:311` `Bearer:`); (b) `section` type, line
  142. (c) **Nothing** — lines 351–352 still allow the contract/piece
  case and say nothing about any other double citation.
- Verdict: **PARTIEL — TO FIX** on (c).

### C15 — hole vs cycle at move 4 · PASSÉ

- Expected: distinguish a lot behind a hole from a lot in a cycle; a rule
  for the hole (e.g. treat the need as pre-existing for ordering); only a
  true cycle empties `## Order`.
- Found: lines 392–398 table: hole → "treat that need as pre-existing for
  ordering, so the rest of the sequence still comes out"; cycle → see
  below.
- Verdict: **CONFORME.**

### C16 — bug-fix tie-break · PASSÉ

- Expected: on a bug-fix cycle the tie-break is the lot list's own order,
  stated at move 4 next to the layer rule.
- Found: lines 412–414, exactly that.
- Verdict: **CONFORME.** But its premise "a lot has no layer" contradicts
  the ceilings paragraph — see D.4.

### C17 — ceilings: one number, unit, mapping, default · PASSÉ

- Expected (pass file): one number per layer **counting entries cited**,
  header says so; section-to-layer mapping stated or ceilings keyed on
  sections; a default; "indicative" sentence goes.
- Found: lines 453–468 — one number per layer (9/7/7/5/4), "Anything
  else 5", "indicative" sentence gone, framework words replaced by role
  names, "One number, not a range" (line 482).
- Unit: **lots, not entries** — line 464 "The count is lots, never
  entries." Opposite to the pass file; deliberate per modifications.md
  lines 1005–1009 ("Le Vérificateur compte les lots par bloc").
- Mapping: line 467–468 "the conventions say what this project calls
  them" — but the agent's reading list ends "🔴 Nothing else. Not the
  code, not the state document, not the product file" (lines 86–87) and
  never lists `docs/TECHNICAL_CONVENTIONS.md`. The section→layer mapping
  therefore rests on a file the agent may not open. The pass file's
  alternative (key the ceilings on the technical document's own section
  names) would have avoided this.
- Verdict: **CONFORME to modifications.md on the unit; TO FIX on the
  mapping** — a move resting on a fact nothing it reads gives it, the
  very defect C17 raised.

### C18 — where a coded lot's block is read from · PASSÉ

- Expected: name where the kept block comes from (previous
  `code/sequence.md`, read before it is rewritten) and that new blocks
  continue the numbering.
- Found: lines 424–427, exactly that.
- Verdict: **CONFORME.** Reading list not updated — see D.5.

### C19 — archive only on the closing round · PASSÉ

- Expected: the archive happens only on the run whose `## Defects` is
  empty; whoever performs the rename applies the same condition.
- Found: lines 441–451 "only when your `## Defects` section is empty …
  Never on a round that reports defects".
- Verdict: **CONFORME in the agent; BLOCKING at the hand-off** — same
  finding as C1: no performer, and `7_lots.md:76–78` still credits the
  Vérificateur with the archive.

### C20 — fresh-context rule once; commentary sentences go · PASSÉ

- Expected: the rule stated once where the rounds are introduced, with
  one line in "What you never do"; the four commentary sentences go.
- Found: **unchanged.** Rule still at three places — Role lines 24–25,
  "What you never do" lines 222–223, Part 2 lines 235–244 (the whole "Who
  invokes you" section, verbatim from old). Commentary still present:
  "Rarer since he greps the code" (line 272), "on a new application most
  needs look like that" (278–279), "These two checks protect the
  Détailleur" (380). Only "It shows when the module stops compiling" went,
  with kind 6 (C10).
- Verdict: **NON APPLIQUÉ — TO FIX.** Listed as passed in
  modifications.md.

### C21 — `7_lots.md` tests on the heading, not its content · PASSÉ

- Found: `.claude-new/commands/7_lots.md:58` "whose `## Defects` carries
  lines", `:91` "carries no line", `:92` "carries lines".
- Verdict: **CONFORME.**

### C22 — "say so in the prompt of both agents" · PASSÉ

- Found: `7_lots.md:71–73` "Say nothing about it in the prompt. The
  Cadreur dispatches on what sits on disk"; the two-line prompt excerpt is
  gone; `:164–166` unchanged and now the only rule.
- Verdict: **CONFORME.**

### C23 — Vérificateur block row; row for defects without a blocking file · PASSÉ

- Found: `7_lots.md:97` "Relay which file was missing — it carries no
  `## Decision`"; `:92` new row "`## Defects` carries lines, and no
  blocking file → Stop — relay the defects".
- Verdict: **CONFORME.** NOTE: `7_lots.md:224–227` ("If an agent returns a
  `blocked_*.md`: relay it and stop … The Product Owner fills
  `## Decision`") is generic and still covers the Vérificateur's file,
  which has none.

### C24 — `7_lots.md` section order · PASSÉ

- Expected: steps in running order — file away, commit, worktree, enter,
  invoke, read what came back, merge, push, remove.
- Found: heading order unchanged — `## How it runs` (45), `### Invocation
  parameters` (136), `## Git, in this mode` (170), with "Enter the
  worktree before invoking the agent" at line 196, still two sections
  after the invocation.
- Verdict: **NON APPLIQUÉ — TO FIX.** Listed as passed.

### C25 — `cycle.md` command names · ÉCARTÉ ("périmée")

- Expected: not applied.
- Found: `.claude-new/commands/cycle.md` identical to old on this point —
  `/1_structure`, `/2_grille`, `/7_decoupe` etc. still there; line 88
  still routes "`cadreur` or `verificateur` → `/7_decoupe`" on a filled
  `## Decision`.
- Verdict: **not applied, as recorded.** Question: "périmée" (obsolete)
  — obsolete because `cycle.md` is rewritten elsewhere? The new file is
  byte-identical to the old and still names a `verificateur` decision
  that C8 made impossible. If `cycle.md` is not rewritten in another
  section, C25 is not obsolete.

---

## B. Unannounced changes

Everything in the diff is covered by a comment except the following.

### B.1 — `# PART 3` heading glued to the previous line · TO FIX

- Old (lines 242–247): `🔴 **Delete the file once applied.** …` / blank /
  `---` / blank / `# PART 3 — What you do`.
- New (line 256): `from it. 🔴 **You never rename it, and you never look
  for one.**# PART 3 — What you do`
- What it changes: `# PART 3 — What you do` is no longer a heading — it is
  the tail of a paragraph. The `---` separator is gone too. The file's
  three-part structure announced at lines 11 and 227 loses its third
  part. Fallout of the C8 edit, not asked by it.

### B.2 — `hole` example rewritten · TO FIX

- Old (104–105): `lot-03 | hole | needs ActivityBudget, produced by no
  lot — add a lot for it, or declare it pre-existing`
- New (111–113): `lot-03 | hole | "Needs: ActivityBudget (pre-existing)"
  >> produced by no lot and not in the inventory — add a lot for it, or
  declare it pre-existing`
- What it changes: C7 asked for a visible quote; the quote chosen already
  carries `(pre-existing)`, and the expected correction is "declare it
  pre-existing". Under move 1's own definition (line 271–272, "a need no
  lot produces, and that the Cadreur did not mark *pre-existing*") this
  line is not a hole at all. See D.3.

### B.3 — `anchor` example rewritten · NOTE

- Old (106–107): `lot-05 | anchor | §4.1 describes storage, the lot
  announces a screen — re-anchor, or re-cut the lot`
- New (114–116): `lot-05 | anchor | "Anchor: §4.1 — Storing the entry" >>
  §4.1 describes storage, the lot announces a screen — re-anchor, or
  re-cut the lot`
- What it changes: adds the quoted `Anchor:` line, consistent with the
  Cadreur's format (`cadreur.md:709`). Fine.

### B.4 — overlap test now names `Needs` · TO FIX

- Old (272–273): "An overlap — two lots naming the same symbol, whether
  they produce or modify it."
- New (281–282): "An overlap — two lots naming the same symbol in
  `Needs`, `Produces` or `Modifies`, whether they produce or modify it."
- What it changes: read literally, two lots needing `ActivityEntry`, or a
  lot producing `X` and a lot needing `X`, now both "name the same symbol"
  in one of the three fields — the normal dependency shape becomes an
  overlap. The trailing "whether they produce or modify it" says the
  opposite. No comment asked for `Needs`; C13 asked to exclude a cascade
  caller, and `cadreur.md:64–65` states the rule as "neither in
  production nor in modification". The `Touches` exclusion (lines
  284–285) is a reasonable addition from `cadreur.md:718–725`.

### B.5 — `hole` defined twice, differently · NOTE

- Type table (line 136): "A need no lot produces **and the inventory does
  not carry**".
- Move 1 (lines 271–272, unchanged): "a need no lot produces, and that
  the Cadreur **did not mark *pre-existing***".
- What it changes: the inventory (`cadreur.md:681–702`) lists symbols
  something asks of; a pre-existing framework need is not there. "Not in
  the inventory" and "not marked pre-existing" are different tests, and
  the file now states both.

### B.6 — "the OS" → "the platform" · NOTE

- Old (299): "the OS, a device, the disk, the network".
- New (310): "the platform, a device, the disk, the network".
- Wording only.

### B.7 — ceilings table: column header and layer names · NOTE (covered by C17, noted for completeness)

- Old header `| Layer | Lots per block |` → new `| The layer | Lots per
  block |`; five framework layers → five role names plus "Anything else".
  The "Lots per block" header is now true (it was contradicted before);
  the pass file wanted the opposite unit — see A.C17.

### B.8 — `## Where` / third heading of the blocking file · NOTE (covered by C8)

- Old: `## Where` "<the lot, entry or file>", `## To resume`, `## Decision`.
- New: `## Where` "<the file, and what is missing in it>", `## What has
  to happen` "<which step has to run again>".
- For the block case "both technical documents in one folder" (line 179)
  nothing is missing; the placeholder does not fit that case.

---

## C. Gestures against tools

Frontmatter (line 4): `Read, Grep, Glob, Write`.

| Gesture | Lines | Tool | Verdict |
|---|---|---|---|
| Read `code/decoupage.md` in full | 56 | Read | ok |
| Read the technical document's preamble | 57–59 | Read | ok |
| Open each cited entry | 60, 349 | Read | ok |
| Grep `^### §` for entry titles | 61–62 | Grep | ok |
| Read `code/redecoupage.md` when there | 66–68 | Read (+ Glob to know it is there) | ok |
| Read `code/<lot>/verdict.md` `## Status` | 69–72 | Read | ok |
| Read previous `code/sequence.md` `## Blocks` | 424–425 | Read | ok — but not in the reading list (D.5) |
| Write `code/sequence.md` | 43, 98 | Write | ok |
| Write `code/blocked_verificateur.md` | 167 | Write | ok |
| Find the layer of a section from "the conventions" | 467–468 | Read — but the file is not in the reading list and line 86 says "Nothing else" | **gesture with no authorised input** (A.C17) |
| "Say in your report that it can be archived" | 441 | none — no file, no field; the caller reads `## Defects` only | **gesture with no carrier** (A.C1) |
| "Say so in your report" (coded lot without PASS) | 71–72 | same | **gesture with no carrier** (A.C4) |
| Rename `code/redecoupage.md` | — | correctly removed; the file says so at 444 | ok in the agent; nobody else does it (A.C1) |

Tools no gesture uses: none. `Glob` is implied by "when it is there"
(line 66) and the `-NN` numbering of `sequence.md` blocks; acceptable.

`Edit` removed — no move edits a file; every output is written whole.
Consistent.

---

## D. Internal coherence (new file alone)

### D.1 — Move 6 delegates to a party the file cannot name · BLOCKING (with A.C1)

- Line 444: "**You have no tool that renames a file** — 📌 **the command
  does it**, once you have reported."
- Line 441: "say in your report that it can be archived".
- The agent is invoked by the Cadreur (line 231), not by a command; its
  "report" reaches the Cadreur. The file names no field of
  `code/sequence.md` for the signal and no reader for it. Inside the file
  alone the branch leads nowhere; across the chain nobody performs the
  rename (A.C1).

### D.2 — "seven kinds" for six · TO FIX

- Line 260: "**1. Cross the inventory against the lots**, and note seven
  kinds of defect". The move lists six: surface (263), hole (271),
  overlap (281), orphan (291), dead (295), cascade (299). The type list
  (130–131) has six words for move 1. C10 asked "the list says six
  kinds".

### D.3 — the `hole` example is not a hole · TO FIX

- Lines 111–113: `"Needs: ActivityBudget (pre-existing)" >> produced by
  no lot and not in the inventory — add a lot for it, or declare it
  pre-existing`.
- Lines 271–272: a hole is "a need no lot produces, and that the Cadreur
  did not mark *pre-existing*". Line 277: "A framework type marked
  pre-existing is not a hole." The quoted line is marked pre-existing; the
  expected correction tells the Cadreur to do what the line already does.
  The file's only worked example of its format contradicts its own
  definition.

### D.4 — a bug-fix lot has no layer, and blocks are bounded by its layers · TO FIX

- Line 412: "⚠️ **On a bug-fix cycle a lot has no layer**".
- Line 431–432: "Add the next lot if it belongs to the same layer — on a
  bug-fix cycle, whatever its layer".
- Line 478–479: "There, group on contiguity alone, up to **the lowest
  ceiling among the layers the block holds**."
- Line 473–474: "The layer rule does not apply on a bug-fix cycle … Two
  fixes on one layer share no reading there".
- Either a bug-fix lot has a layer (then the tie-break at 412–414 rests on
  a false premise and the "lowest ceiling among the layers" is computable)
  or it has none (then 478–479 has no input). Question for the Cadreur's
  side: `cadreur.md:66–68` says "a lot's layer is the bearer's, whatever
  sections its entries come from … a bearer belongs to one layer, and
  that is what a block groups by" — the opposite of line 412 and of
  473–474.

### D.5 — a read the reading list forbids · TO FIX (minor)

- Line 424–425: "Their blocks come from the previous `code/sequence.md`
  — read its `## Blocks` section before you write over the file."
- Lines 54–87 "What you read" does not list `code/sequence.md`, and line
  86 closes with "🔴 **Nothing else.**" The same applies to "the
  conventions" at line 467 (A.C17).

### D.6 — coded-lot table points at a move that says nothing · TO FIX

- Line 80: "| **2 · 4 · 5** | 📌 **As those moves already say** |".
- Move 4 (lines 383–416) never mentions a coded lot. Step **a** "Take the
  lots whose needs are all pre-existing — they come first" would re-place
  coded lots (their needs are, by then, all in the tree). Nothing says
  coded lots sit at the head of `## Order` in the order they ran, and the
  algorithm runs on the rest — which is what move 2 (324–327, "a coded
  lot is behind") and move 5 (420–422, "walk from the first lot that is
  not coded") assume.

### D.7 — a `## Defects` line with no type for it · TO FIX (= A.C9)

- Line 128: "One of these words, and no other".
- Lines 181–183: "an entry a lot cites that the document does not hold, a
  lot citing no entry at all" are defects. No word in 130–145 fits either.

### D.8 — "the Cadreur corrects only the lots those defects name" vs an entry-numbered first field · QUESTION

- Line 124–125: first field is "the entry number when the defect attaches
  to an entry and to no lot" (`orphan`).
- `cadreur.md:802` "Fix only the lots named". An `orphan` line names no
  lot. Does the Cadreur's file handle a first field that is an entry
  number? Not this file's to settle, but this file introduced the shape.

### D.9 — empty `## Blocks` on a cycle discards kept blocks · QUESTION

- Line 400–402: on a cycle "leave `## Order` and `## Blocks` empty".
- Line 420–422: on a redécoupage "the coded ones keep the blocks they ran
  in — write them back unchanged".
- On a redécoupage round that finds a cycle among the uncoded lots, which
  wins? The next round reads "the previous `code/sequence.md`" (424) for
  the kept blocks — and finds them empty.

### D.10 — `merge` is a defect of move 2, which "records" · NOTE

- Line 321: "**2. Record what orders lots without declaring it.**"
- Line 346–347: "Where neither order works, they are one lot — say so as
  a defect."
- Move 2 is described as recording input for move 4; it also raises a
  defect. Not wrong, but the move's own heading does not say so, and the
  word `merge` does not appear there (A.C6).

### D.11 — "You judge the shape, not the count" survives its subject · NOTE

- Lines 304–306 were written for the pair kind 6 / kind 7 ("Whether four
  callers is the right number is the Cadreur's to know"). With kind 6
  gone, "the count" has nothing in the move that counts. Harmless.

### D.12 — References check · ok

- "See *Who invokes you*" (25) → section at 229. ok.
- "See *What you write*" (44) → section at 96. ok.
- "see *You never resume from a blocking file*" (200) → section at 248.
  ok.
- "see below" (432, 433) → ceilings table at 453. ok.
- "it surfaces at move 4" (275) → 383. ok.
- "the shape move 2 orders" (288) → 340–347. ok.
- "already raised at move 1" (397) → 271. ok.
- "# PART 3" (256) — exists as text, not as a heading (B.1).

---

## Open questions for the parent

1. Who renames `code/redecoupage.md` now? The agent says the command;
   `7_lots.md` says the agent; `8_code.md` counts the result. (A.C1,
   D.1)
2. C17: the unit was decided against the pass file (lots, not entries).
   Fine if deliberate — but the section→layer mapping now depends on the
   conventions, a file the agent is told not to read. (A.C17, D.5)
3. Does a bug-fix lot have a layer? The agent says no at move 4 and yes
   at move 5; the Cadreur says yes. (D.4)
4. C20 and C24 are recorded as passed and are not applied. Recording
   error, or a later pass that was lost?
5. C25 "périmée": is `cycle.md` rewritten in another section of
   modifications.md? Its new copy still routes a `verificateur`
   `## Decision` that no longer exists.
