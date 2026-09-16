# V2.5b — Handovers, downstream

READ-ONLY investigation. Nothing modified.

**Scope**: the eleven pairs the plan names, in `.claude-new/agents/`:
cadreur→verificateur · verificateur→detailleur · detailleur→concepteur
· concepteur→testeur · testeur→realisateur · realisateur→relecteur ·
relecteur→detailleur · relecteur→controleur · detailleur→arbitre ·
realisateur→arbitre · arbitre→architecte. Where a handover goes
through the orchestration rather than through a file, the command that
carries it — `.claude-new/commands/8_code.md`, `7_lots.md`,
`9_controle.md` — was read at the lines that do the carrying.

**Method**: `grep -n '^## '` on each agent, then the reading and
writing sections only — `## What you read` / `## What you write` (7 of
the 10), `## Where you work` (cadreur, arbitre, architecte), the
`| # | Invocation | Inputs | Output |` table (controleur, architecte).
The two agents with no `What you read` heading and a `What you write`
one at the end of PART 2 (concepteur, testeur) are 200 lines each and
were read whole — they have never run. Every agent of the ten carries
one of the three forms; none is missing. Line numbers refer to the
`.claude-new/` files.

For each pair: what the writer emits (section names, field names,
shape, values), what the reader expects, and the gap. The
`docs/verification/chemins-aval.md` findings (V2.4) are cited as
`V2.4 Fn` where a gap was already reported from the loop's side; this
report does not re-argue them.

Severity: **BLOCKING** — a section or field the reader expects and the
writer never emits, or a value the reader has no row for, on a path
the chain takes · **TO FIX** — writer and reader disagree on a shape,
a value, or a rule that governs the handover, and one of them has to
change · **NOTE** — a wrinkle, or a defect internal to one agent that
touches the handover.

---

## 0. Summary — the findings that matter most

| # | Pair | Finding | Severity |
|---|---|---|---|
| H1 | detailleur→concepteur · testeur · realisateur → relecteur | **The sheet declares no file, and four agents test on "the files the sheet declares"**. `fiche-executable.md` has five fields (L229–259): Signatures, Acceptance criteria, Dependencies, Conventions, Requests. The concepteur reads "the files the sheet says you touch" (L59, L137) and falls back on "the sheet's `Modifies` or `Touches`" (L141) — fields of `code/decoupage.md`, which it never opens (L62–63). The testeur (L210), the realisateur (L146–147, L166) and the relecteur (L373–376) all write or check `## Outside the lot` as "every file the sheet does not declare" — that is every file. Pre-existing in `.claude/` for the realisateur and relecteur; new for the concepteur and testeur | BLOCKING |
| H2 | verificateur→detailleur (via 8_code) · relecteur→detailleur | **The Détailleur's two modes are told apart by prompt wording no template fixes.** `8_code.md` has no `Agent()` block for the detailleur (L204–238 give the other four); L242 says "name the block", L129 says "say which lots". In normal mode a lot with a sheet and no PASS is *skipped* (detailleur L472); in propagation mode the same lot is *rewritten* (L661–673). A prompt naming a block and some lots without saying which mode is read as normal, and the propagation silently does not happen | TO FIX |
| H3 | detailleur→arbitre · realisateur→arbitre | **A `## Decision` that is filled but does not settle has no row on the caller's side.** The arbitre writes `Not settled here.` into `## Decision` (L169, L255 "never leave the field as you found it") and answers a multi-entry file partially (L139–140 "a file half-answered still moves the agent forward"). The detailleur (L333–335) and the realisateur (L276–278) test three cases — filled / filled and back to the split / empty — and apply a filled one. A refusal or a half-answer is *filled* | TO FIX |
| H4 | arbitre→architecte | **Five verdict outcomes on the writer, two rows on the reader.** The architecte writes *written* / *changed* / *already carried* / *not a convention — belongs elsewhere* / *doubt or product decision* (L592–596). The arbitre reads *a rule written or changed* → copy, *refused* → wait for the Product Owner (L409–410). *Already carried*, the case a request most often hits (L363–367 says so), falls under "refused" and costs a 20-minute wait for a rule that exists | TO FIX |
| H5 | realisateur→arbitre | **The realisateur's multi-lack blocking file has no shape.** L226–229: "a second lack … is added to the blocking file … one entry each, and the Arbitre answers both". Its shape (L237–251) is the single four-heading one. The arbitre knows the `## Blocking N` form from the detailleur alone (L129–131) | TO FIX |
| H6 | detailleur→arbitre | **A multi-stop blocking file has no folder.** The detailleur writes one file for stops on lot-04 and lot-07 (L477–495) at `code/<lot>/blocked_detailleur.md` — which `<lot>` is not said. The arbitre reads the folder as "what the block bears on" (L94–96); `8_code.md` L122–123 looks in `code/<lot>/` of the lot about to run | TO FIX |
| H7 | realisateur→relecteur | **A decision applied against the sheet has no field in the report.** Realisateur L455–456: "code against the decision and say so in your report" — the report's five fields (L133–157) have no place for it. The relecteur decides *divergence with a decision behind it* (propagation, L156–158) against *divergence with none* (FAIL structurel, L160–162) and reads no blocking file (L53–66 "nothing else") | TO FIX |
| H8 | testeur→realisateur | **The realisateur is told three times that it writes the tests and twice that it never touches one.** Frontmatter L3 ("write the code and the tests … Writes one test per acceptance criterion"), L52, L131 against L24 and L532. A Réalisateur that adds a test defeats the testeur's reason for existing (testeur L28–30) and the relecteur's point 2 cannot tell whose test it pairs | TO FIX |
| H9 | concepteur→testeur → cadreur (redécoupage) | **The concepteur's commit survives a return to the split.** The concepteur commits its empty declarations (L170); a redécoupage makes the realisateur drop *what it wrote* (L288–289) and the run merges the branch regardless (`8_code.md` L402). The next Cadreur re-cuts around symbols that now exist with empty bodies, and the next Détailleur's grep finds "a production that already exists" (detailleur L109–113) — a split defect, and a block | TO FIX |
| H10 | cadreur→verificateur | **The lot carries no layer, and the Vérificateur may not open the file that names them.** Order and blocks depend on a lot's layer (verificateur L408, L431, L453–467); the five lot fields (cadreur L709–713) carry none; "the conventions say what this project calls them" (L467) — and the reading list ends "Nothing else. Not the code, not the state document, not the product file" (L86), with no conventions file in it. Same sentence in the cadreur (L96), which does read them | TO FIX |
| H11 | cadreur→controleur (side of relecteur→controleur) | **`## Entries with no lot` never reaches the Contrôleur.** Cadreur L404: an entry already carried by the code goes there "otherwise the Contrôleur reads it as a gap". The controleur never opens the lot list (L64–66); `9_controle.md` phase 1 (L73–93) reads the `Anchor:` fields only and gives such a block a dash. Its intention is reported *Missing* | TO FIX |
| H12 | concepteur→testeur | **A criterion observable in a declaration alone can never be red.** The testeur must rewrite any new test that passes (L164–165). Against an empty declaration, a test on a data shape — a field's presence, a constructor's arity, an enum's members — passes. The "Data shapes and their storage" layer is one of the six, and the rule has no exit for it | TO FIX |
| H13 | relecteur→controleur · 8_code · realisateur | **A route that no longer exists is still described in the realisateur.** L458–461: "A blocking file can target a lot already carrying a PASS. The Contrôleur reports missing intentions … the verdict gets rewritten when the Relecteur runs again". The controleur writes no blocking file (L70–72); `8_code.md` L347–349: what the Contrôleur reports "never comes back this way" | NOTE |

The three never-exercised pairs the plan names are H1, H8, H9, H12 and
section 3–5 below. **None of them has a one-character section-name
gap** — the names match where the reader names one. The gaps are
fields the reader expects and the writer never carries (H1), a shape
undefined on one side (H5), and rules stated on one side that the
other side's files contradict (H8, H9).

---

## 1. cadreur → verificateur

**The carrier**: `code/decoupage.md`, and the call
`Agent(subagent_type="verificateur", prompt="Working folder: <…>.")`
(cadreur L754–768). Back: `code/sequence.md`, read at `## Defects`
(cadreur L771).

| What the cadreur writes | Line | What the verificateur reads | Line | Match |
|---|---|---|---|---|
| `## Symbols` inventory first, one line per thing asked, `— piece` mark | L681–699 | "`## Symbols` inventory comes first … sits at the head" | L82–84, L178 | ✅ |
| `## lot-NN` · `Anchor:` `§3.2 — title; §3.5 — title` | L707–709 | quotes `"Anchor: §4.1 — Storing the entry"`; `section` defect on a bare `§3` | L114, L131, L353–357 | ✅ |
| `Needs: X (pre-existing), Y (lot-02)` | L710 | `hole` — a need "the Cadreur did not mark *pre-existing*" | L272–274 | ✅ |
| `Produces: X (called by lot-05)` | L711 | `dead` — "its `Produces` field names no caller" | L298–300 | ✅ |
| `Modifies:` · `Touches:` | L712–713 | overlap on the first three, "`Touches` is not counted" | L284–285 | ✅ |
| `## Entries with no lot` | L664, L704 | "the `## Entries with no lot` list" | L63, L292 | ✅ exact |
| `## Conventions requests` | L704, L727–733 | not read | — | fine — the command reads it |
| `code/redecoupage.md` · appends `## Ce qui revient`, `## Ce que j'en fais` | L860–870 | reads `## Ce qui est déjà codé` only | L66–67 | ✅ — that section is the arbitre's (arbitre L333), same string |

**Back, `code/sequence.md`**: `## Order`, `## Blocks`, `## Defects` with
`lot | type | "verbatim" >> expected` (verificateur L98–116). The
cadreur reads `## Defects` (L771), corrects the lots named, and
"searches for" the quoted line (verificateur L152–155) — ✅. No
`sequence.md` and a `code/blocked_verificateur.md` → the cadreur goes
out (L775) — ✅, and `7_lots.md` L102 relays it.

**H10 — the layer.** The verificateur needs a layer per lot at move 4
(tie-break, L408–410) and move 5 (grouping and ceilings, L431–467). The
lot declares none; the layer is the section's (cadreur L64 "a lot
spanning two sections belongs to no layer"), and which layer a section
is comes from "the conventions" (verificateur L467) — a file its
reading list excludes (L86). Either the section→layer map is in the
technical document's preamble (which it reads, L56–58) and L467 is
wrong, or L86 is wrong. As written, two Vérificateurs may group
differently, which L481–483 says must never happen. **TO FIX.**

**NOTE** — inside the verificateur, move 5 says "what the ceiling
counts is entries cited, not lots" (L433) and, thirty lines on, "the
count is lots, never entries" (L464). The `## Blocks` the detailleur
receives depends on which one the agent follows.

**NOTE** — a second `## Ce qui est déjà codé` appears when the arbitre
appends to an existing `redecoupage.md` (arbitre L327–329); the
verificateur does not say it reads the last one. Moot while V2.4 F2
holds (nobody archives the file), real once it is fixed.

---

## 2. verificateur → detailleur

**The carrier**: `code/sequence.md` `## Blocks`, plus the block name in
the prompt (`8_code.md` L242).

| Writer | Line | Reader | Line | Match |
|---|---|---|---|---|
| `block-1: lot-01, lot-04` | L104–107 | "the orchestration names your block in the prompt; the sequence says which lots it holds" | L64–65 | ✅ |
| a block is "a contiguous slice of the sequence" | L470–471 | move 4 "an earlier lot **of this block** produces it" — needs the order inside the block | L601 | ✅ — the block line is in sequence order |
| `## Defects` non-empty | L109–116 | — | — | ✅ `8_code.md` L69–70 stops before invoking |
| on a cycle, `## Order` and `## Blocks` empty | L400–402 | — | — | ✅ same stop |
| coded lots keep their block, new blocks continue the numbering | L420–427 | "a sheet, and its verdict is `PASS` — never touched" | L471 | ✅ |

**H2 — no prompt template, two modes.** `8_code.md` gives an `Agent()`
block for the concepteur, testeur, realisateur and relecteur
(L204–238) and none for the detailleur; L242 says "name the block" and
L127–129 "say which lots". The detailleur's normal run *skips* a lot
with a sheet and no PASS (L472); its propagation run *rewrites* those
lots (L661–673) and is entered because "the prompt names the affected
lots" (L661). Nothing says what a prompt has to contain to be read as
one rather than the other. A propagation prompt read as a normal one
finds every lot of the block sheeted, skips them all, and hands back
with nothing rewritten — no error, no block. **TO FIX**: a template
per mode, or a token the detailleur tests on.

---

## 3. detailleur → concepteur — never exercised

**The carrier**: `code/<lot>/fiche-executable.md`, and the prompt
`Working folder: <…>. Your lot: <lot>.` (`8_code.md` L207–211;
concepteur L41–42 "the orchestration names your lot in the prompt" ✅).

| The sheet (detailleur L229–259) | The concepteur reads | Line | Match |
|---|---|---|---|
| `## Signatures` | "its `## Signatures` section above all" | L53–54 | ✅ exact |
| `## Dependencies` — `X — pre-existing` · `Y — produced by lot-02` (L249–250, L628) | "`## Dependencies` … a type marked *pre-existing* you never declare, and one *produced by* an earlier lot is already in the code" | L54–56, L130–132 | ✅ same two values |
| `## Acceptance criteria` | not read | — | fine |
| `## Conventions` — `§3 · …` (L254) | "those the sheet names" | L58 | ✅ (but see NOTE on `§` vs `R`) |
| `## Requests` | not read | — | fine |
| **no file field** | "the files the sheet says you touch" | L59, L137 | ❌ **H1** |
| **no `Modifies`, no `Touches`** | "put it where the sheet's `Modifies` or `Touches` points" | L141 | ❌ **H1** |
| **no file field** | "touch a file the sheet does not declare — say so and block instead" | L82–83 | ❌ **H1** — every file is undeclared |
| **no file field** | `## Outside the lot` — "every file you touched that the sheet does not declare, or a dash" | L190–192, L198 | ❌ **H1** — never a dash |

**H1 in full.** `Modifies` and `Touches` are lot fields in
`code/decoupage.md` (cadreur L712–722); the detailleur does not copy
them into the sheet (L229–259, and "absent by construction" L264–266
names nothing of the kind); the concepteur may not open the lot list
("nothing else … not another lot's sheet", L62–63 — the lot list is
not even named as forbidden, it is simply not an input). Three of the
concepteur's rules test on a field that does not exist: where a symbol
goes when the conventions do not settle it (L140–142 — the fallback
points at nothing), what it may touch (L82–83 — it may touch nothing),
and what it reports (L190–192 — it reports everything). The same holds
for the testeur (L88, L210), the realisateur (L146–147, L166 "it is
not in your `Modifies`") and the relecteur (L373–376, "check it against
the diff"). The realisateur and relecteur lines are unchanged from
`.claude/` — the gap predates the refonte and was never exercised
because the old chain did not run the check. **Fix on the writer's
side**: a `## Files` field in the sheet, copied from the lot's
`Modifies` and `Touches`, or the file paths the detailleur's grep found
for each symbol (it greps every one, L578–590).

**Also on this pair:**

- **The block route for an impossible signature has no return to the
  sheet.** The concepteur blocks on "a type the language does not
  have, a name it refuses" (L111–113), leaves `## Decision` to the
  Product Owner (L109), and "never changes a signature the sheet gives"
  (L77–78). The fix is the sheet's, and the sheet is rewritten only
  when `fiche-executable.md` is absent (`8_code.md` L76) or on a
  propagation prompt (H2). A decision the Product Owner writes into
  `blocked_concepteur.md` is applied by the concepteur (L118–119) —
  which then declares something the sheet does not say, and the
  relecteur's point 1 reads it as a divergence with no decision behind
  it (H7) → `FAIL structurel` → a fresh Réalisateur that "never writes
  a declaration" (L27–28). **TO FIX** — the decision has to reach the
  Détailleur, and nothing routes it there.
- The concepteur applies a decision "the prompt names" (L118–119) —
  the prompt template (`8_code.md` L207–211) has no slot for it, and
  `8_code.md` L342–343 "invoke the agent it names" says nothing about
  passing the file. V2.4 F4 covers the missing rename; this is the
  missing hand-in. **TO FIX.**
- "Four moves, in this order" (L125), five numbered (L127–170). NOTE.
- Signatures are written in the sheet's neutral notation (`→`,
  L231–236); the concepteur must write them "name for name, type for
  type, in that order" (L146–147). The notation carries no visibility,
  no nullability marker beyond a dash comment, no receiver kind
  (class, object, function): the concepteur takes these from the
  permanent conventions (L65–68). Consistent, if the conventions carry
  them. NOTE.
- The sheet's conventions example numbers rules `§3`, `§9`, `§10`
  (L254–255, L642); `docs/TECHNICAL_CONVENTIONS.md` numbers them `R1`,
  `R2`… and the architecte's verdict writes `R93` (L619). A Détailleur
  copying the example's form writes a number the three downstream
  agents "open" (relecteur L346) and do not find. NOTE.

---

## 4. concepteur → testeur — never exercised

**The carrier**: `code/<lot>/conception.md` and the declarations in
the tree.

| Concepteur writes (L176–192) | Testeur reads | Line | Match |
|---|---|---|---|
| `## Declared` — symbol and file | "which symbol landed in which file" | L61–62, L154 | ✅ (section not named by the reader — no name to mismatch) |
| `## Compile` — command and outcome | "and that the module compiles" | L62 | ✅ |
| `## Placements not settled by the conventions` | not read | — | fine |
| `## Outside the lot` | not read | — | fine — but see H1 |
| bodies empty or throwing *not implemented*, never a default (L150–153) | "every test you just wrote fails" | L161 | ✅ by construction — except H12 |
| commit (L170) | — | — | see H9 |

**H12 — a declaration-only criterion.** The testeur's rule: a new test
that passes "asserts nothing, or asserts something the empty body
already satisfies — rewrite it" (L164–165). A criterion of a
data-shape lot — *the entry carries a date and a duration*, *the enum
has three members* — is satisfied by the declaration, has no body to
be empty, and no rewrite makes it red. The testeur's only other exits
are the manual list (for the unobservable, L138–140 — this is
observable) and a block (for the untestable, L115–117 — this is
testable). **TO FIX**: a third outcome for a criterion the declaration
alone satisfies, recorded in `tests.md` so the relecteur's point 2 does
not count it as a gap.

**H9 — the concepteur's commit on a redécoupage.** The concepteur
commits (L170) before the testeur or the realisateur run. When the
realisateur's block sends the lot back to the split, it drops *what it
wrote* (L288–289, "commit nothing"); the concepteur's declarations are
already a commit on the branch, and `8_code.md` L402 merges the branch
before handing back, then L281 runs `/7_lots`. The Cadreur re-cuts
"the one in hand included, whose code was dropped" (cadreur L829–830)
— it was not; the Détailleur's walk greps the produced symbol
(L461–462) and finds it: "a production that already exists … the lot
was declared against a stale state document" (L109–113), a split
defect it must stop on. Same for a Détailleur block sending a block
back: the lots before it in the block are coded, but the concepteur
has not run on any lot yet at walk time — so this case is the
realisateur's alone. **TO FIX**: the realisateur's drop has to revert
the concepteur's commit too, or the arbitre's `## Ce qui ne l'est pas`
has to say the declarations stand and the Cadreur keep them.

**Also**: the testeur's tests are never committed (V2.4 F12). On this
pair it means the realisateur's move 9 "staging explicitly what belongs
to the lot" (L568) is the first chance the tests have of entering a
commit — and the realisateur "never touches a test" (L24). Whether
`git add` on an untracked test file is touching it is not said.

**NOTE** — the testeur reads "the declarations the concepteur wrote …
their signatures" (L63–64) directly from the code, and the sheet's
`## Signatures` (L60). If the two differ (the concepteur may not change
one, L77 — but H1's fallback may have placed it oddly), the testeur has
no rule for which wins.

---

## 5. testeur → realisateur — never exercised

**The carrier**: `code/<lot>/tests.md`, the tests in the tree, and
`code/recette.md`.

| Testeur writes (L196–210) | Realisateur reads | Line | Match |
|---|---|---|---|
| `## Red` — every new test failed, every older one passed | "its `## Red` line" | L74–75 | ✅ exact name |
| `## Tests` — criterion ↔ test | not read; move 5 runs the suite | L528–529 | ✅ |
| `## Criteria with no test` | not read by the realisateur; read by the relecteur | relecteur L331 | ✅ exact name |
| `## Outside the lot` | not read | — | H1 |
| `code/recette.md`, appended | not read; `9_controle.md` L170 | — | ✅ |

**H8 — who writes the tests.** Realisateur L3 (description): "to write
the code and the tests a spec sheet calls for … Writes one test per
acceptance criterion". L52: "You write the code, the tests, and
`code/<lot>/compte-rendu.md`". L131: "**The code and the tests**, then
…". Against L24 and L532: "You never touch a test". The Réalisateur
is a `sonnet` agent reading its own frontmatter first; three sentences
say the tests are its output. A Réalisateur that adds one test per
criterion beside the testeur's produces two tests per criterion, the
second written against the body (what testeur L28–30 exists to
prevent), and the relecteur's point 2 pairs "the test that observes
each" (L327) on whichever it finds. **TO FIX** — three stale
sentences.

**NOTE** — testeur L212–213: "`## Red` is what the realisateur and the
Relecteur take as given — neither runs the tests again before
writing". The realisateur runs them at moves 5 and 6 (L528, L544). The
sentence means *before writing code*; as read, it contradicts the
realisateur's loop.

**NOTE** — the realisateur's block on "a test you would have to change
to make it pass" (L532–535) goes to the arbitre with "either the
sheet's criterion is wrong, or the test reads it wrongly". The arbitre
reads "the lot's sheet and report" (L108) — not `tests.md`, not the
test. It settles a question about a test it cannot see.

---

## 6. realisateur → relecteur

**The carrier**: `code/<lot>/compte-rendu.md`, the commits, and the
prompt `Files the lot's commits changed: <the git diff list>`
(`8_code.md` L232–237).

| Realisateur writes (L133–157) | Relecteur reads | Line | Match |
|---|---|---|---|
| `## Symbols` — `X — created` · `Y — modified, now returns Z` | "the report's `## Symbols` list which says whether each was created or modified" | L307–314 | ✅ exact values |
| `## Outside the lot` — file and what was done, or a dash | "`## Outside the lot` names every file … or a dash. Check it against the diff" | L373–376 | ✅ name — ❌ H1 on the content |
| `## Build` — `analyze: clean` · `test: 47 passed` | "read the report's `## Build` claim first"; `## Verified` copies it | L301, L175–178, L356 | ✅ |
| `## State` — `Added:` `Removed:` | "`## State` names what went into the state document" | L356 | ✅ |
| `## Requests` — path or dash | "`## Requests` names the conventions requests the lot wrote, or a dash" | L356–357 | ✅ |
| "code against the decision and say so in your report" | — | — | ❌ **H7** — no field |
| commit, no message convention (L568) | prompt list from "the lot's first commit" (`8_code.md` L97–98) | — | see below |

**H7 — where a decision shows.** The relecteur's point 1 reports
"every divergence" (L307–308); the verdict then splits them: a
"signature changed by a decision the Réalisateur applied" goes to
`## Symbol divergences` and the status may be PASS (L156–158); one
"with no decision behind it" is a point-1 finding and `FAIL
structurel` (L160–162, L102). The relecteur reads the sheet, the four
reports, the changed files and the conventions — "nothing else"
(L53–66). The only trace of a decision is `code/<lot>/blocked_*-NN.md`
(not read) and "say so in your report" (realisateur L455–456) with no
field to say it in. As written, every decision-backed divergence is a
`FAIL structurel`, and a fresh Réalisateur applies the same decision
again (its resume reads the numbered files, L419–423). **TO FIX**: a
`## Decisions applied` field in the report, and the relecteur names it.

**The diff list.** `8_code.md` L97–98: "`git diff --name-only` between
the lot's first commit and `HEAD`". The lot's first commit is now the
concepteur's (L170); no commit message convention names a lot, on
either agent. Within one run the orchestration can note `HEAD` before
invoking the concepteur; on a lot resumed after a stop (`8_code.md`
L60–61, a FAIL retry in a later run) the first commit is in an
earlier run's history and nothing identifies it. The list then misses
the concepteur's files, and point 5 (L396–399 "on the changed files the
prompt names") does not see the declarations. **TO FIX** — a message
convention (`lot-NN:` prefix) or the first commit's SHA written where
the next run finds it.

**NOTE** — the relecteur's list is "the files the lot's commits
changed" and the testeur's tests are not committed (V2.4 F12): the
tests reach the relecteur's diff only if the realisateur's move 9
stages them. Point 2 (L323–329) then finds the tests by reading the
tree, not the list — it works, by accident of the reading order.

**NOTE** — `## Attempts` "carries the count the verdict you replace
held" (L144–145): the relecteur replaces a verdict it is not told to
read. V2.4 F5.

---

## 7. relecteur → detailleur

**The carrier**: `verdict.md` `## Symbol divergences`, read by
`8_code.md` (L127–129, L134–135), relayed in the prompt.

| Relecteur writes | Line | 8_code | Detailleur reads | Line | Match |
|---|---|---|---|---|---|
| `## Symbol divergences` — `<symbol> — returns X, sheet says Y — affects lot-04` or *affects none* | L133–135, L166–175 | "naming affected lots → detailleur on the block … say which lots in the prompt" (L127–129) | "the prompt names the affected lots — you read no verdict file" | L661–662 | ✅ |
| affected lots = that block's lots with no PASS whose sheet names the symbol | L166–175 | — | rewrites "only those sheets, against the signature the code actually carries — grep it" | L675–677 | ✅ — the new signature is not relayed, and does not need to be |
| the block line of `code/sequence.md`, one line | L166–167 | — | — | — | ✅ verificateur L104–107 |

**H2** applies here on the reader's side: the detailleur enters this
mode on prompt wording alone. **TO FIX** — see section 2.

**NOTE** — detailleur L670 "Moves 3 to 9" under a heading "The eight
moves" (L529) that numbers nine (L531–645). The propagation mode
names moves that the heading says do not exist.

**NOTE** — `8_code.md` L131–132 fires propagation "on the final verdict
only". A `PASS with reservation` is final; a `FAIL mineur` whose retry
passes yields a second verdict, and the first one's divergences are
overwritten (the relecteur writes the file whole, L113). If the retry
keeps the decision-backed signature, the second verdict carries the
same divergences — ✅. If it reverts it, the relecteur's point 1 finds
nothing and `## Symbol divergences` is empty — also ✅.

---

## 8. relecteur → controleur

**There is no file handover.** The controleur reads the product file's
blocks and the sheets the prompt names, "those, and no other" (L47–52,
L128 table), never a verdict, never the sequence (L64–66). What the
relecteur hands the controleur is the *gate*: `9_controle.md` L27–28
and L55–57 stop unless "every lot of `code/sequence.md` carries a
`verdict.md` in PASS".

| Relecteur writes `## Status` | Line | The gate reads | Match |
|---|---|---|---|
| `PASS` · `PASS with reservation` · `FAIL mineur` · `FAIL structurel`, "one of the four words, alone on its line" | L97–103, L191–192 | "in PASS" (`9_controle.md` L28, L55); "carrying PASS" (`8_code.md` L60); "still carries PASS" (verificateur L70) | ✅ as a prefix match; ⚠️ "one of the four words" — `PASS with reservation` is three words, and whether it *is* PASS for the three gates is nowhere said. NOTE |

**H11 — the entries with no lot.** The one thing the controleur cannot
see and the chain says it does: cadreur L404 sends an entry the code
already carries to `## Entries with no lot` "with that reason —
otherwise the Contrôleur reads it as a gap". The controleur does not
read the lot list (L64–66). `9_controle.md` phase 1 builds
block→lots from `tracabilite.md` and the `Anchor:` fields (L73–81);
a block whose entries no lot cites gets `—` (L85, L91–93) and "the
group carrying it reads no sheet for it". Its intentions are then
*Missing* — "no signature and no criterion of your group's sheets
observes the intention" (controleur L206) — and go to the register
(`9_controle.md` L200–201) and to a `bug-list.md` (`8_code.md`
L347–349). The reason the Cadreur wrote is read by nobody. **TO FIX**:
phase 1 reads `## Entries with no lot` and marks the block, or the
controleur's prompt carries it.

**NOTE (V2.4 F10)** — `9_controle.md` L200 reads "the `Doubtful` and
`Missing` fields" of the report; the controleur writes `## Intentions
missing` and `## Doubts` (L216–224), and its own invocation 2 says
"under `Doubtful`" (L268–271) for a heading it never writes.

**H13** — realisateur L458–461 describes a Contrôleur block on a
PASSed lot, answered by the Product Owner, lifted by a re-run of the
Relecteur. The controleur "never writes a blocking file" (L70), and
`8_code.md` L347–349 closes that route. Stale; a Réalisateur reading it
expects a file that cannot exist. NOTE — but it is a `🔴` rule, and the
Product Owner might follow it by hand.

---

## 9. detailleur → arbitre

**The carrier**: `code/<lot>/blocked_detailleur.md` and the call
`prompt="Working folder: <…>. Blocking file: code/<lot>/blocked_detailleur.md."`
(detailleur L315–322). The arbitre expects "two things: the working
folder, and the path of the blocking file inside it" (L68–69) — ✅.

| Detailleur writes | Line | Arbitre reads | Line | Match |
|---|---|---|---|---|
| `## What blocks` · `## Where` · `## To resume` · `## Decision` empty | L284–300 | "never touch `## What blocks`, `## Where` or `## To resume`"; writes `## Decision` only | L145–147, L142–143 | ✅ exact |
| several stops: `## Blocking 1 — lot-04` with `### What blocks` `### Where` `### To resume`, one `## Decision` | L477–495 | "several `## Blocking N` entries … one answer per blocking, numbered, under the single `## Decision`" | L129–133 | ✅ — the `###` level is not named by the reader; fine |
| the file sits in `code/<lot>/` — which lot, for several stops | L278, L477 | "each one's folder tells you what that block bears on … in a lot's folder — it bears on that lot" | L94–96 | ❌ **H6** |
| numbered `blocked_detailleur-NN.md` beside it | L412–414 | "blocking files already settled sit beside it, numbered. Read them" | L98–100 | ✅ |
| no sheet exists yet (walk first, L337–339) | — | "the lot's sheet and report — only when the block bears on a lot" | L108–109 | ⚠️ the arbitre is told the order may be missing (L105–106), not the sheet. NOTE |

**Back, `## Decision`** — the detailleur's three rows (L331–335)
against what the arbitre can leave:

| The arbitre leaves | Line | Detailleur row | Outcome |
|---|---|---|---|
| a three-part decision | L148–158 | Filled → apply, rename, detail | ✅ |
| "the lot goes back to the split", naming `code/redecoupage.md` | L350–352 | Filled, and it sends the lot back → write no sheet | ✅ — tested on wording here, on the file in the realisateur (L291–296); the detailleur's resume table (L424–426) then tests on the file. Two tests for one fact. NOTE |
| empty, after a 20-minute wait | L419–431 | Still empty → stop | ✅ |
| `Not settled here. <whose it is>` | L167–169, L254–256 | **Filled → apply** | ❌ **H3** |
| N answers of N+1, one "not yours" | L139–140 | **Filled → apply** | ❌ **H3** — the detailleur says "no decision is applied … until it comes back" (L497–499) and nothing about a partial return |

**H3 in full.** The arbitre is called only by the detailleur and the
realisateur (L234–241), so `Not settled here.` on a single-entry file
is reachable only through a product question — where L306 says *wait
for the Product Owner* and L419 *leave `## Decision` empty*. But L139
says, for one entry among several, "say so for that one, and settle
the others": the field is then partly filled, and L255 forbids leaving
it as found. The detailleur tests *filled* and applies it — it details
the block with one stop unanswered, meets it again in the walk, writes
a new blocking file, calls the arbitre again, which reads the settled
one beside it (L98–100) and waits again. Not a loop — a full wasted
round and, on a `sonnet` Réalisateur (same three rows, L275–278), a
lot coded against an answer that says it is not an answer. **TO FIX**:
either the arbitre never writes a refusal into `## Decision` of a file
that is its own (L255 is for files that are not), or the two callers
get a fourth row.

**H6 in full.** "One blocking file, with one entry per stop" (L477)
over lots 04 and 07, at `code/<lot>/blocked_detailleur.md` (L278).
Nothing says `<lot>` is the first stop's, the block's first lot, or
anything. The arbitre reads the folder as the block's bearer (L94–96)
and would treat the lot-07 entry as bearing on lot-04. `8_code.md`
L122–123 looks for an empty `## Decision` "in `code/<lot>/`" of the lot
about to run — lot-07 is invoked with lot-04's file unread if lot-04
was closed. The detailleur's own resume looks "for every lot of your
block" (L412–413) — ✅ for itself. **TO FIX**: name the folder (the
block's first lot), and tell the arbitre a `## Blocking N — lot-NN`
entry bears on the lot it names, not on the folder.

---

## 10. realisateur → arbitre

**The carrier**: `code/<lot>/blocked_realisateur.md`, same call shape
(L255–262) — ✅ with arbitre L68–69.

| Realisateur writes | Line | Arbitre reads | Line | Match |
|---|---|---|---|---|
| four headings, `## Decision` empty | L237–251 | same | L142–147 | ✅ |
| "a second lack … added to the blocking file … one entry each" — **no shape** | L226–229 | `## Blocking N` entries, "the Détailleur files everything one walk found" | L129–131 | ❌ **H5** |
| the report — written at move 8, after the block | L560, but L230 "say in your report what you did write" | "the lot's sheet and report" | L108 | ⚠️ the report may not exist when the arbitre runs. NOTE |
| `reprise_realisateur.md` on an empty return | L312–331 | not read — right, the arbitre has gone | — | ✅ `8_code.md` L105–107 relays it |

**Back, `## Decision`**: the realisateur's three rows (L275–278) — the
back-to-split row tests on `code/redecoupage.md` being there ✅ with
arbitre L327–352. `Not settled here.` and a partial answer: **H3**,
same as section 9, with a `sonnet` agent applying it.

**H5 in full.** The realisateur's second lack "never replaces the
first … one entry each, and the Arbitre answers both" (L226–229). Its
only shape is the four-heading one (L237–251). A Réalisateur that
appends a second `## What blocks` produces two headings of one name;
one that copies the detailleur's `## Blocking N` form has never seen
it (it does not read the detailleur). The arbitre expects the
`## Blocking N` form (L129) and nothing else. **TO FIX** — give the
realisateur the multi-entry shape, by reference or in full.

**NOTE** — the arbitre's platform-trap outcome writes into `## Traps`
of `CURRENT_TECHNICAL_STATE.md` itself (L364); the `technical-state-
format` skill says never write there without loading it, and the
arbitre has no `Skill` tool (L4). Not a handover of this pair, but the
realisateur then reads what the arbitre wrote (L513–516).

---

## 11. arbitre → architecte

**The carrier**: `architecte/arbitre-<lot>.md` and the call
`prompt="Working folder: <…>. Invocation 3 — Requests."` (arbitre
L392–400). The architecte: "the prompt says which one. It is never
inferred" (L293) — ✅; "or the Arbitre, which is blocked on one and is
waiting for you — its request is `architecte/arbitre-<lot>.md`"
(L537–540) — ✅ exact path; "the Arbitre reads its own back" (L543) —
✅.

| Arbitre writes | Line | Architecte reads | Line | Match |
|---|---|---|---|---|
| `## What I need` · `## Why the block cannot be settled without it` · `## Where I met it` · `## What I think it is` (add · update · remove) · `## Verdict` empty | L382–389 | requests "whose `## Verdict` is empty" — the other headings are not named | L563–567 | ✅ — the reader names only the field it tests; the same five headings in cadreur L187–191, detailleur L353–357, realisateur L355–359 |
| — | — | `## Verdict` — `Convention — R93 written.` + the rule's text · `R30 changed.` + text · *already carried*, number and text · *not a convention — where it belongs* · *doubt / product decision* | L590–596, L617–624 | see H4 |

**Back, `## Verdict`** — the arbitre's two rows (L407–410):

| Architecte outcome | Arbitre row | Outcome |
|---|---|---|
| `Convention — R93 written.` + text | "a rule written or changed" → copy number and text | ✅ |
| `R30 changed.` + new form | same | ✅ |
| *Already carried* — "cite the rule that carries it, by number and text" (L594) | neither — falls to "Refused" → wait 20 minutes → empty `## Decision` → the caller stops | ❌ **H4** — a settled question stops the lot |
| *Not a convention — belongs to the code / tooling / machine* (L595) | "Refused" → wait | ⚠️ *the code* is the arbitre's own move 2 (L281–288); it waits on the Product Owner for what it could settle. NOTE |
| *Not a convention — a product decision* · *a doubt* (L595–596) | "Refused" → wait | ✅ — that is what the wait is for |

**H4 in full.** The architecte's own text says the most frequent
request is "does rule X apply to my case?" — "11 of 25 were open
doors" (arbitre L369–373) — and its outcome is *already carried*
(L594), with number and text, exactly what the arbitre copies for a
written rule (L409). The arbitre's table does not know the word. On a
`opus` arbitre reading the intent, it probably copies; on the letter,
it polls for 20 minutes and leaves `## Decision` empty, the detailleur
stops the block (L335), and the Product Owner is asked to settle a
rule that is in the file. **TO FIX** — a third row: *already carried →
copy it*.

**NOTE** — the architecte's "what you report back" (L177–186) counts
files, rules, questions; for invocation 3 it never says *which
requests got which outcome*, and the arbitre re-reads the file (L405)
— ✅ nothing lost, the report is not the carrier.

**NOTE** — the architecte writes the conventions file mid-lot, inside
the arbitre's wait, in the same worktree as the running lot. `8_code.md`
L176–178 forbids invoking it "while a lot is running" for the
end-of-lot pass; the arbitre's call is the exception L164–165 names. ✅
consistent — one worktree, one writer.

---

## 12. What holds, pair by pair

| Pair | Section names | Field names | Values | Verdict |
|---|---|---|---|---|
| cadreur→verificateur | ✅ | ✅ | ✅ | H10 (layer), two NOTEs |
| verificateur→detailleur | ✅ | ✅ | ✅ | H2 (no template, two modes) |
| detailleur→concepteur | ✅ on the two read | ❌ files — H1 | ✅ dependencies | H1, block route, hand-in |
| concepteur→testeur | ✅ (unnamed) | — | ✅ | H12, H9 |
| testeur→realisateur | ✅ `## Red` | — | ✅ | H8 |
| realisateur→relecteur | ✅ five of five | ❌ decision — H7 | ✅ | H7, H1, diff list |
| relecteur→detailleur | ✅ via prompt | ✅ | ✅ | H2 |
| relecteur→controleur | gate only | — | ⚠️ *PASS with reservation* | H11, H13, V2.4 F10 |
| detailleur→arbitre | ✅ | ✅ | ❌ H3 | H3, H6 |
| realisateur→arbitre | ✅ | ❌ H5 | ❌ H3 | H3, H5 |
| arbitre→architecte | ✅ | ✅ | ❌ H4 | H4 |

**Where the three never-exercised pairs stand**: the section names
match everywhere a reader names one — the refonte wrote the concepteur
and the testeur against the sheet's real headings. What they inherit
is a field the sheet never had (H1), a redécoupage the concepteur's
commit does not survive (H9), a criterion the empty declaration
satisfies (H12), and a Réalisateur whose frontmatter still says it
writes the tests (H8). None is a typo; each is a rule written on one
side that the other side's file does not support.
