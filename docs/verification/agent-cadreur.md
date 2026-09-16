# Vérification — `cadreur.md`

Read: `.claude/agents/cadreur.md` (old, 812 lines),
`.claude-new/agents/cadreur.md` (new, 906 lines),
`docs/refonte/passes/cadreur.md` (26 comments), `docs/refonte/modifications.md`
§ `# cadreur.md` (lines 939-974). The section carries no "La demande" —
the pass file's *Ce qu'il faut* is what each PASSÉ is verified against.
C2, C3 and C23-C26 also name `7_lots.md` and `cycle.md`; both were
diffed old against new for those points only. Line numbers below are
the **new** file's unless stated.

The pass sheet claims **25 passés, 1 écarté (C26), 0 partiel**. Found:
**13 passés as asked · 9 partiel · 1 not applied (C21) · 1 écarté
confirmed · 2 passés (C23, C25) — command side.** The claim of zero
partial does not hold.

---

## A. CONFORMITY

| # | Expected (pass file, *Ce qu'il faut*) | Found in the new file | Verdict |
|---|---|---|---|
| **C1** | One exhaustive dispatch table in one place: empty Decision → stop; filled → apply then dispatch again (may be A when no `code/decoupage.md`); "no ten moves after D" only when a split exists; drop or qualify "one invocation per cycle" | L275-276 two rows added (empty → Stop; filled → D then dispatch again). L288 "On B or C" (D dropped). L293-295 "After D … may be A". **But** L24 still "One invocation per cycle"; block D keeps its own three-row table L887-891, so there are still two dispatch tables | **PARTIEL** — TO FIX |
| **C2** | The agent stops demanding a rename its tools cannot do; either the command renames or the agent gets the tool | L891 "Apply it, and say in your report that you did"; L893-896 "You never rename the file … The command renames it". `7_lots.md` new L96: `git mv … NN` row. Leftover: L904-906 "Renaming is what closes it — never delete it" now addressed to an agent that neither renames nor can delete | **PASSÉ** (stale tail, see D-18) |
| **C3** | The agent knows what lifts a conventions block: on entry, a blocking file whose `## Where` names a request with a filled `## Verdict` is lifted by that verdict (accepted → carry on; refused → block stands); command tests an empty `## Verdict`, not the file's presence | Command side done (`7_lots.md` L93-94 test empty/filled Verdict; L94 "invoke cadreur: the verdict is what lifts its block"). **Agent side absent**: no passage reads `## Verdict` back — `grep -n Verdict` gives only L191 (the heading in the template) and L202 (do not reopen an answered file). L169-171 still says `## Decision` "is the only way this block ever lifts". Part 2 L275: Decision empty → **Stop**. So the run the command launches after the Architecte stops on arrival, exactly the dead end C3 describes | **NOT APPLIED on the agent** — BLOCKING |
| **C4** | One observable criterion separating block from fast path | L138-143 table: "answer changes what the lot declares → Block + request / answer only sanctions what the lot declares in full → request alone". L119-121 blocking list carries it. **But** the old un-observable test survives at L197-199 ("Can you finish without it? Yes … No …") — two tests for one fork | **PARTIEL** — TO FIX |
| **C5** | A rule for a second request in one run, and for a file whose `## Verdict` is already filled; `## Conventions requests` names what the rule produces | L201-204: one file, one heading block per need; an answered file is never reopened, new block below | **PASSÉ** (see D-question on a file holding one filled and one empty Verdict) |
| **C6** | The blocking cases enumerated once, in the owning section; the moves point back at it; the two-documents case writes the file | L112-126: nine bullets, count matches modifications.md ("neuf cas"). L128 "Every one of them writes the file". Move 1 L372-374, move 9 L643-644, third round L779-781 write the file. **But** L301-302 still "a folder carrying the two is a defect; stop and say so" — no file; and move 7 L566 "A blocker — the rule cannot be built" names no file and no section | **PARTIEL** — TO FIX |
| **C7** | The one-section rule carries its exception where it is stated (move 10 and the never-do entry); a bearer spanning two layers is a blocking case, not an assumption | Exception added at L66-69 under *What makes a lot*, and in the blocking list L125-126. **Not** at move 4 L428, move 10 L656, never-do L218 — the three places C7 named remain absolute. L330-331 still "A single bearer never spans two layers" — the assumption C7 asked to remove, now contradicting L68-69 | **PARTIEL** — TO FIX |
| **C8** | Two rows for §1 and §2, each its own unit, or a declared exception | L419-420: "§1 Model — one lot per entity" / "§2 Persistence — one lot per table, with its migration — it needs the entity's lot" | **PASSÉ** |
| **C9** | One observable bound per lot, counted from what the lot declares, ceiling per layer in that unit; the block table stays with the vérificateur | L80-91: table of symbol ceilings per layer; "the measure is the count of symbols in `Needs`, `Produces`, `Modifies`". L93-94 blocks are the Vérificateur's. **But** L75-78, kept from the old text, still introduces the table with "What follows bounds a block … You use it to calibrate a lot's size, never to group" — the table now bounds a lot, not a block | **PASSÉ**, intro stale — TO FIX (D-2) |
| **C10** | Four fields, or the fifth named and shown; if the fifth is a name or layer, move 7's identifier goes there | Fifth field is `Touches` (L713), so "five fields" L703 now counts. Move 7 L573-574 "Its identifier says what it is" still writes into no field — lots are `## lot-NN` | **PARTIEL** — TO FIX |
| **C11** | One unit for `Modifies`, or two fields — symbols vs files declaring no symbol; collision rule on the first | L713-725: `Touches` added, `Needs/Produces/Modifies` symbols only, collision checked on the first three. L491 "Every symbol the grep returns" (was "file"). **But** no move writes into `Touches`: move 6 L477-479 (tests), L496-499 (file-name symbols → "name the tests") and move 8 L615 ("The lot carries the declaration") still route to `Modifies`/the lot without naming `Touches` | **PARTIEL** — TO FIX |
| **C12** | Pointer names move 7 | L394 "Move 7 says how you find them" | **PASSÉ** |
| **C13** | Already-carried case lands in `## Entries with no lot` with that reason; "is a defect" decided or dropped; the "section yields no lot" line is that list or goes | L404: goes in `## Entries with no lot`, reason "already carried by the code"; "is a defect" dropped. **But** L747-748 "Write the file even when a section yields no lot — say so with a line" kept, against L738 "No prose between lots" | **PARTIEL** — TO FIX |
| **C14** | Move 3 greps once, on code **and test** folders, keeps the hit list; move 6 classifies, greps again only for new names | L446-453 added under move 5: keep the hit list, move 6 classifies. **But** move 3 L396 "Grep each symbol as you note it" says nothing of test folders (L361-362 counts them only "when you are looking for callers" — move 6); and move 6 still reads "**Grep** the callers" L474, "**Search** the test folders too" L478-479, "**Grep** the symbol's name" L481, "**Grep** what it declares instead" L498, "**Grep** the fulfilments too" L502 — the second grep C14 removes is still instructed five times | **PARTIEL** — TO FIX |
| **C15** | Row 2 produces the order it relies on: a need on the removing lot | L538 "Declare a need on that lot — it has to run first"; L544-547 rewritten around that need | **PASSÉ** |
| **C16** | Bound the test to what a hit shows; default = modification when the grep does not settle | L523-533: "does the hit show…", "A hit that does not settle it is declared a modification", the conservative side | **PASSÉ** |
| **C17** | Listener cut like a piece (own lot when another layer, cites the trigger entry, needs the rule); move 7's third row names the cut/report test, "report" = blocking file | L639-644 listener rule as asked, blocker writes the file. **But** move 7 third row L593 unchanged: "cut a lot for it, or report the split cannot carry this entry" — no test, and "report" is in none of the nine blocking cases | **PARTIEL** — TO FIX |
| **C18** | A row for the vérificateur having blocked: go out without correcting | L775 row added, header "What came back" | **PASSÉ** |
| **C19** | C ends as A does (vérificateur called, rounds counted); moves 5-10 apply to added/changed lots, 3-4 not re-run; never-do says the same | Never-do rewritten L246-249. L789-792 "Blocks B and C end here too". **But** the statement sits in A's *Then call the Vérificateur* subsection — block C itself (L821-878) still says nothing; block B L816-817 still "the ten moves are not re-run" and Part 2 L288 "you do not run block A's ten moves", both now at odds with "moves 5 to 10 apply" | **PARTIEL** — TO FIX |
| **C20** | Look-alike rule and framework-type rule in universal terms; layer table by role | L466-468 "state holder of the platform, a storage annotation, a base component". L80-87 layers by role. L510 "An exhaustive match on the type". **But** the same sentence continues "every exhaustive `when` on it stops compiling" L511, and L515 "the name is written in the `when`" — modifications.md claims `when` is out; it is in twice | **PARTIEL** — TO FIX |
| **C21** | Each rule once, never-do list as index; the "measured" anecdotes and "why" sentences go | Nothing removed. File grew 812 → 906 lines. Still present: "measured: five test files" L487; three-round ceiling L24-26, L238, L779-781; unbounded wait L237, L768-769; blocking-file-first L270, L883; "Read it in full" L347, L377; "do not argue with a defect" L254, L783, L805; "no ten moves on B/C" L246-249, L288-291, L816-817 | **NOT APPLIED** — TO FIX (listed passé; it is not) |
| **C22** | The two body rules enter the never-do list | L241 product file rule as a bullet; L243-244 bare-grep rule added — **not as a list item**, and L246-249 likewise: the list is broken into three fragments, L249 carries the orphaned indentation of the old bullet | **PASSÉ in substance**, TO FIX formatting |
| **C23** | (command) One rule on the redécoupage prompt | `7_lots.md` new L71-73: "Say nothing about it in the prompt"; the "both agents" sentence removed | **PASSÉ** |
| **C24** | (command) The on-disk table lists the blocking-file states; "always produces a split" scoped | New L47-48 "in every state but one"; L54-55 two blocking-file rows | **PASSÉ** |
| **C25** | (command) Reading list names where the counts come from | New L31-36: sequence headings for blocks, `## lot-` headings for lots | **PASSÉ** |
| **C26** | ÉCARTÉ — cycle.md routing | `cycle.md` old and new identical on `/7_decoupe`, `/1_structure` … (L9-10, L88, L93-94) | **NOT APPLIED — as required** |

---

## B. UNANNOUNCED CHANGES

Every hunk of the diff maps to a comment above. Three contents inside
those hunks are not asked for by any comment:

**B-1 — L82-87, the ceiling values.** NOTE.
Old: `Models, migrations 8-10 · Services 6-8 · Repositories 6-8 · Providers 4-6 · Screens 3-4` (lots per block).
New: `Data shapes 4 · Domain rules 6 · Reads/writes storage 6 · Screen state 8 · What the user sees 10 · Anything else 6` (symbols per lot).
C9 asked for the unit, not the numbers; the numbers come from nowhere in the pass file. Question: are they the same ceilings the new `verificateur.md` L284 counts on, and where were they measured?

**B-2 — L87, the `Anything else` row.** NOTE.
A catch-all layer with a ceiling of 6. Neither C9 nor C20 asked for it; the old table had no default. Harmless, but the Vérificateur's "A section matching none takes the default" (its L468) suggests the two files were aligned on purpose — say so, or the row reads as invented.

**B-3 — L93-94 and L96-97.** NOTE.
"How many lots a block holds is not yours — the Vérificateur forms the blocks, and its own ceilings say how many" / "The layers are named by role — the conventions say what this project calls them." New sentences implied by C9 and C20 but not written there. Consistent with both; recorded for completeness.

No renumbering, no moved section, no rewritten table beyond the ones the comments name. The old L258 "Which cycle is this?" block is byte-identical — which is the source of D-4 and D-5.

---

## C. GESTURES AGAINST TOOLS

Frontmatter L4: `Read, Grep, Glob, Edit, Write, Agent`.

| Gesture | Where | Tool | Verdict |
|---|---|---|---|
| Read the technical document, the conventions, `## Defects`, `code/redecoupage.md` and its `-NN` siblings, settled `blocked_cadreur-NN.md` | L347-352, L771, L827-828, L883-885 | Read | has it |
| Grep `<<ASSUMED`; grep every symbol with a path | L372, L359-360, L396 | Grep | has it |
| "Look at what is on disk" (dispatch); find the `-NN` files; find `verdict.md` carrying PASS | L270, L827, L884, L832 | Glob | has it — 🔴 never named in the text; and `verdict.md` has no stated location (see D-19) |
| Write `code/decoupage.md`, `code/blocked_cadreur.md`, `architecte/cadreur.md` (creating the folder) | L679, L108, L183-185 | Write | has it (Write creates parent folders) |
| Correct only the lots named; append a heading block below a filled `## Verdict`; append `## Ce qui revient` / `## Ce que j'en fais` to `code/redecoupage.md`; apply a decision to a lot | L777, L202-204, L860-870, L898 | Edit | has it; *When `Edit` fails* L258-264 covers the two failure modes |
| Invoke `verificateur`, wait unbounded | L759-769 | Agent | has it; template passes `model="opus"`, which matches the Vérificateur's frontmatter per CLAUDE.md |
| "Say in your report that you did" (D), "say it in your report too" (C) | L891, L876 | final message | no tool needed |
| Rename `code/blocked_cadreur.md` | — | — | **removed** (C2); L893-896 says so explicitly. No gesture needs Bash |

**Tool no gesture uses:** none — all six are consumed. Glob is
consumed only implicitly ("look at what is on disk", "beside it");
nothing tells the agent that finding a `-NN` file is a Glob and not a
Read of a name it has to guess. NOTE.

**Gesture with no tool:** none in the new file. The one in the old
file (rename, `git mv`) is gone.

---

## D. INTERNAL COHERENCE (new file alone)

**D-1 — L24 · BLOCKING with D-3, else TO FIX**
> "📌 **One invocation per cycle**, and you last the whole of it."
False by the file's own Part 2 (L273-279: four re-entry blocks) and by
block B ("`/7_lots` was run again by hand"). C1 asked to drop or
qualify it; it stands unchanged.

**D-2 — L75-78 against L80-91 · TO FIX**
> "⚠️ **What follows bounds a block** — the group of lots the Détailleur
> will handle in one invocation, and which the **Vérificateur** forms,
> not you. You use it to calibrate a lot's size, never to group."
What follows is a table of symbol ceilings **per lot** (L80-91), and
L93-94 then says block sizes are not the agent's. The introduction
describes the table that was removed.

**D-3 — L147-148 · L169-171 · L275 · BLOCKING**
> L147-148: "a blocking file with a request beside it goes to the
> Architecte and brings you back"
> L169-171: "The `## Decision` heading … is the only way this block ever
> lifts."
> L275: "`code/blocked_cadreur.md` with `## Decision` **empty** → 🔴
> **Stop** — say the blocking file still stands"
A procedure branch that leads nowhere: the agent is "brought back" after
the Architecte, finds its own file with an empty Decision (the Architecte
writes only `## Verdict` in `architecte/cadreur.md`, its L616-622), and
stops. The command's new row 94 ("the verdict is what lifts its block")
describes an agent this file does not contain. This is C3.

**D-4 — L128 against L301-302 · TO FIX**
> L128: "📌 **Every one of them writes the file.**"
> L301-302: "a folder carrying the two is a defect; stop and say so."
The first bullet of the blocking list (L115) is this very case. The
passage that meets it still stops without a file — the exact stop L128-130
calls "invisible to the command".

**D-5 — L66-69 against L330-331 · TO FIX**
> L68-69: "A bearer whose entries would put it in two layers is a
> blocking case — ⚠️ **never a fact you declare impossible.**"
> L331: "**A single bearer never spans two layers.**"
The rule and the assumption it was written to replace, both in force.

**D-6 — L307 · NOTE**
> "**Three differences, listed here and nowhere else**"
The section then states six 🔴 paragraphs (L311-334), and the
bug-fix exception is now also stated at L66-69 and L125-126. Both the
count and the "nowhere else" are false. Pre-existing on the count,
newly false on the place.

**D-7 — L246-249 against L288-291 and L816-817 · TO FIX**
> L246-249: "moves 5 to 10 apply to every lot you add or change; moves 3
> and 4 are not re-run"
> L288: "On B or C, you do not run block A's ten moves."
> L816-817: "the ten moves are not re-run"
Three statements of one rule with two contents. A reader at block B
obeys "not re-run" and adds a lot with no callers grepped — the defect
C19 names.

**D-8 — L241-249 · TO FIX (format)**
The never-do list breaks at L243: "🔴 **Grep outside the code folders…**"
and L246 "🔴 **Re-cut the whole document…**" are paragraphs, not
`- ` items; L249 "  first split, and re-cutting buries…" keeps the
indentation of a bullet that no longer exists. Rendered, the list ends
at L241 and a second list starts at L250.

**D-9 — L446-449 against L474, L478-479, L481, L498, L502 · TO FIX**
> L446-449: "Move 6 classifies those hits … and greps again only for a
> name the inventory does not hold"
> L474: "**6. Grep the callers of every symbol declared modified.**"
Move 6's heading and four of its rules still order the grep that the
added paragraph forbids.

**D-10 — L396 against L361-362 and L446-449 · TO FIX**
> L396: "🔴 **Grep each symbol as you note it.**"
> L361-362: "Their test folders count as code folders **when you are
> looking for callers**."
If move 6 no longer greps (L446-449), the only hit list is move 3's,
and move 3 is never told to sweep the test folders. Tests — "the ones
that break first" — are in nobody's grep.

**D-11 — L440-441 against L431-432 and L639-640 · TO FIX (count)**
> L440-441: "moves 6 to 9 add to these declarations, **and one of them
> adds lots**."
> L431-432: "**Move 7 adds lots** this table does not describe — the
> pieces."
Move 9 now adds lots too (L639-640, "its own lot when it belongs to
another layer"). "One of them" is two, and move 4's pointer names one.

**D-12 — L573-574 · TO FIX**
> "⚠️ **Its identifier says what it is** — the contract's name plus what
> realises it."
No field of a lot holds an identifier (L707-713: `## lot-NN`, Anchor,
Needs, Produces, Modifies, Touches). C10 is open.

**D-13 — L593 · TO FIX**
> "cut a lot for it, **or report the split cannot carry this entry**"
"Report" is in none of the nine blocking cases (L115-126) and names no
file; nothing chooses between the two outcomes. C17's second half.

**D-14 — L566 · NOTE**
> "🔴 **A blocker** — the rule cannot be built"
Names neither the file nor *When you cannot produce*, unlike move 9
(L643-644 "the blocking file, like every other"). L128 covers it in
principle; the pointer C6 asked for is missing here.

**D-15 — L713-725 against moves 6 and 8 · TO FIX**
> L718-719: "🔴 **`Touches` carries the files a lot has to open that
> declare no symbol of its own** — a test file, a manifest, a build
> file."
Defined in *What you write*; written by no move. Move 6 L477-479 sends
tests to the caller search, L491-494 everything "into the lot's
`Modifies`"; L498-499 "name the tests that use those" names no field;
move 8 L615 "The lot carries the declaration" names no field. A reader
following the moves fills `Modifies` and leaves `Touches: —`.

**D-16 — L747-748 against L738 · TO FIX**
> L738: "🔴 **No prose between lots**"
> L747-748: "Write the file even when a section yields no lot — say so
> with a line."
C13 asked that this line become the `## Entries with no lot` list or
go. Both rules stand.

**D-17 — L197-199 against L138-143 · TO FIX**
> L197-199: "📌 **Can you finish without it?** **Yes** — write the
> request and carry on … **No** — write `blocked_cadreur.md` as well."
The un-observable test C4 replaced, kept beside its replacement. Two
tests for one fork; the section the blocking list points to (L120-121
"see *When the conventions fall short*") holds the old one, the new
table sits in *When you cannot produce*.

**D-18 — L904-906 · NOTE**
> "⚠️ **Renaming is what closes it** — 🔴 **never delete it.**"
Addressed to an agent that, three paragraphs earlier (L893-896), "never
rename[s] the file" and has no tool that deletes. Stale tail of the old
block D.

**D-19 — L832, L250 · NOTE**
> "A lot whose `verdict.md` carries PASS is closed."
The file's location is never given (per lot? under `code/`?). The
agent has Glob and can find it, but has to guess the pattern.

**D-20 — L278 against L773-777 · TO FIX**
> L278: "`## Defects` in `code/sequence.md` → **B**"
The new Vérificateur writes `code/sequence.md` "even with no defect — an
empty `## Defects` section says the split holds" (its L160-161). The
dispatch row tests presence, not content, so every `/7_lots` re-run on a
clean split enters B. The command's own table (new L57) says "whose
`## Defects` **carries lines**"; the agent's does not.

**D-21 — L293-295 against L898-899 and L273-279 · question**
> L293-295: "After D, you dispatch again — and that may be A, when no
> `code/decoupage.md` exists"
> L898-899: "How you apply it — to the lot or entry `## Where` names,
> then cut the rest as usual."
When a split **does** exist, no defects, no redécoupage: after D the
table's remaining rows give "None of these → A — a first split" over an
existing split. Is "cut the rest as usual" meant to mean "call the
Vérificateur on the amended split" (a round, counted) rather than the
ten moves? Nothing says which, and L246-249 forbids the second reading
only for B and C.

**D-22 — L775 · question**
> "**No `code/sequence.md`, and a `code/blocked_verificateur.md`**"
On a B or C round an older `code/sequence.md` is on disk from the
previous split. If the Vérificateur blocks without removing it, the
row's first condition is false and the agent reads the old
`## Defects`. Does the new Vérificateur delete or overwrite the sequence
before blocking? (`verificateur.md`'s to settle; the row's test should
not depend on it.)

**D-23 — L201-204 · question**
> "write the new need under a fresh heading block, below."
A file then holds one filled and one empty `## Verdict`. The command's
rows 93 ("with an **empty** `## Verdict`") and 94 ("with a **filled**
`## Verdict`") both match it. Which wins? Not the agent's to fix, but
the agent's rule is what creates the state.

**D-24 — L140-141 · NOTE (format)**
> `| | |` / `|---|---|`
A table with two empty header cells. Renders as an empty header row.

**D-25 — L24-26 against L810-814 · question (pre-existing)**
"Three rounds at most, which you count" — block B enters "from cold …
nothing in context". The count is lost at every cold re-entry; a split
can be checked three rounds per hand-run of `/7_lots` without bound.
Not raised by the pass file; noted since C19 now sends B through the
same loop explicitly.

---

## Summary

- **BLOCKING (1):** C3 / D-3 — the Architecte round still dead-ends on
  the agent's side; the command was fixed, the agent was not.
- **TO FIX (16):** C1 tail (D-1), D-2, D-4, D-5, D-7, D-8, D-9, D-10,
  D-11, D-12, D-13, D-15, D-16, D-17, D-20, plus C20's two `when` and
  C21 (not applied — the sheet's "25 passés" counts it).
- **NOTE (7):** B-1, B-2, B-3, D-6, D-14, D-18, D-19, D-24, Glob unnamed.
- **Questions (4):** D-21, D-22, D-23, D-25.
- **Écarté confirmed:** C26 — `cycle.md` untouched.

Pattern across the partials: every fix was **added** at one place and
the old wording was **left** at the others (C4, C6, C7, C13, C14, C19,
C20, C21). The new file is the old file plus patches, which is the
opposite of what C21 asked and the source of eight of the sixteen
contradictions above.
