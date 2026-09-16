# agent-architecte — verification

**Read**: `.claude/agents/architecte.md` (old, 538 lines) · `.claude-new/agents/architecte.md`
(new, 686 lines) · `docs/refonte/passes/architecte.md` (20 agent comments `### C1` … `### C20`,
8 command comments `### CMD1` … `### CMD8`) · `docs/refonte/modifications.md`
§ `` # `architecte.md` `` (lines 629–803).

**What the section says**: six structural modifications ("La demande" §1–§6: the directives
file · invocation 4 *Completing* · `permanente`/`spécifique` marking · second table of
`couverture.md` removed · coverage vs conjunction separated · an insufficient answer gives a new
questions file) plus two command rows. Pass sheet: **Passés (27)** C1–C19, CMD1–CMD8 —
**Écartés (1)** C20 — **Partiellement passés (0)**.

CMD1–CMD8 target the command files, not the agent. They were spot-checked in
`.claude-new/commands/conventions.md`, `7_lots.md`, `8_code.md` since the sheet lists them as
passed; findings on those files are marked *cmd*. Line numbers below are those of the **new**
agent file unless marked *old* or *cmd*.

Two cross-file facts used below: `par-genre/directives.md` is written by `/5_reclasse`
(cmd 5_reclasse 85, "a genre with no block gets an empty file, never no file"); the
`permanente` marker is read by `realisateur.md` 67, `concepteur.md` 58, `testeur.md` 66,
`relecteur.md` 62.

---

## A. Conformity

### Structural modifications ("La demande")

| § | Expected | Found | Verdict |
|---|---|---|---|
| 1 Directives | Read at derivation and at the incremental invocation; never questioned; four-row integration table (same → nothing · broader → merge, its words win · nothing → new rule · contradicts → directive wins, said in the report); never reworded; "derive first, then integrate" at 1, pure integration at 4 | Section *The directives*, lines 467–491: the four rows verbatim (479–484), "never question" (473), "never reword … place, merge, number" (486–488), invocations 1 and 4 (490–491). Table rows 1 and 4 list the file (274, 277). | **Conforming on the text.** But no move of invocation 1 performs the integration — see D-8 — and row 4 of the directives table collides with invocation 4's own replace rule — see D-10 |
| 2 Invocation 4 | Reads the file whole, walks the grid, adds only what is not covered; reading ban restricted to invocation 1; `couverture.md` for this feature alone; complete = automatic, replace = raised, with the three things named | Section *INVOCATION 4 — Completing*, lines 648–684, all of it. Table row 4 (277). | **Conforming.** Which of invocation 1's ten moves it runs is unsaid — see D-9 |
| 3 Marking | Each rule carries `permanente` or `spécifique`; the two definitions; "he is the one who knows" | Lines 114–125: the two rows in the spec's words, "at the end of the line" (116), "You are the only one who knows what fires a rule" (123). | **Conforming.** The placement ("end of the line") and the Réalisateur sentence (124–125) go beyond the spec — B-3 |
| 4 Second table removed | The rule → grid entry / mechanical-or-review table goes; the first table stays; test kind lives on the rule in the conventions file | Lines 165–168: *"One table, and one only. A rule's test kind … is written in the conventions file itself, on the rule"*. Old lines 135–144 gone. First table kept (146–152). | **Conforming.** The form of the test kind on the rule is not given — D-15 |
| 5 Coverage vs conjunction | Coverage marked a product question, distinctly, never turned into a convention at any invocation; carry on to the end; in doubt between coverage and precision, raise | Lines 409, 414–432: all five points. Invocation 2 line 526–527 restates the ban. | **Conforming on the text.** How the mark is written in the four-line entry is unsaid (D-6); where the answer goes at invocation 2 is unsaid (D-7) |
| 6 Insufficient answer | A new questions file, never empty; same mechanism as the Lexicographe; it bounds the loop | Lines 505–513, table row 2 output (275). | **Conforming** |

### Comments listed PASSÉ — agent file

| # | Expected (pass file, *Ce qu'il faut*) | Found (new file) | Verdict |
|---|---|---|---|
| C1 | Grid rules and conventions rules told apart; **every** reference to a grid rule says it is the grid's | Line 239: *"the grid's `R2`"*. Line 333–334: *"except under the grid's `R3`"*. **Line 240 unchanged**: *"Amend the grid you apply — R4"*. Conventions rules (R12, R30, R74, R93) untouched, correctly. | **Partially conforming — TO FIX**: one of the three grid references still bare (240) |
| C2 | The file says what the N column carries and from which document; grid entries have one name throughout | Lines 149–155: examples now `model · persistence · presentation · access`; *"The second column is the entry's nature, as the technical document's section carries it."* G-numbers gone with the second table; part B entries are "C1 to C12" (358) everywhere. | **Conforming** |
| C3 | (a) a third kind — inconsistency of the corpus — whose answer lands upstream; (b) invocation 2 knows what to do with it: nothing in the conventions file, **the coverage line records** that the entry was corrected or that the question stands; (c) the command relays that kind as something to fix in the technical document; (d) move 2's two cases stated so that one reading remains | (a) row *Inconsistency*, line 411. (b) lines 521–524: nothing in the conventions file, said in the report — **no coverage line**. (c) cmd conventions 188–193: relay table has a *product question* row, **no inconsistency row**. (d) **line 341–342 unchanged**: *"a block whose line carries a dash, or an entry that line names nowhere"* — still reads two ways. Also lines 181–182 and 459–460 still say *"coverage or conjunction"* (D-4). | **Half applied — TO FIX**: (a) done, (b) without the coverage line, (c) not in the command, (d) not done |
| C4 | Move 4 states the class — every anomaly part A names for its reading — with the three as instances, or says the three are exhaustive | Lines 353–356: *"every anomaly part A names for its reading, 📌 a cycle in V2, numbers that disagree in V5, diverging pairs in V7"*. | **Conforming.** Markup broken — D-16 |
| C5 | One standard for a platform fact, whichever invocation; if lookup, invocation 1 may look up the holes it fills from platform practice **and that alone**; if recall, the asymmetry is stated and invocation 3's reason goes | Lines 400–403: *"A fact about the platform is looked up, never recalled — at every invocation."* The lookup branch was chosen, **but** line 69 (*"Invocation 3 reads the build files and the web, and only it"*), lines 552–555 (*"This invocation alone may read the web … Everywhere else those are forbidden"*) and table row 1 (no web among the inputs) all stand unchanged. Nothing says "the holes filled from platform practice, and that alone". | **Applied in one place, contradicted in three — BLOCKING** (see D-2). Also the sentence lifted from the pass's *Justification* now sits in the rule text (401–403), against C19 |
| C6 | The `off-grid` mark and the citing entries live in one place — the coverage line; the rule in the conventions file carries nothing that says where it came from | Lines 160–163: *"carries `off-grid` at the end of its line, with the entries that motivate it. There, and nowhere else — the conventions file carries no provenance"*. **But** move 6 unchanged, line 374: *"Each cites the entries that state it, and carries `off-grid`"* (the subject is the rule); *What you never do* unchanged, lines 237–238: *"unless it carries `off-grid` and cites the entries"*. | **Partially conforming — TO FIX**: the two passages that put the mark on the rule are still there (D-14) |
| C7 | One sequence for the whole file; allocated once, never reused, never shifted; a later rule takes the next number whatever section; a withdrawn rule keeps its number and says so | Lines 106–112, all four points. Invocation 4 row: *"Next free number"* (673). | **Conforming** |
| C8 | The walk repeats for the missing entries alone; files already written are amended, not rewritten | Lines 385–386: *"back to move 5 for those entries alone. The files already written are amended, never rewritten."* | **Conforming** |
| C9 | The prompt names the number (the command has the fact) — or the never-list rule carves out the glob | Lines 462–463: *"The prompt names your number — the command has the fact, and you never list a folder to find it."* Old fallback `questions/architecte/` gone. **cmd conventions 100–105**: the prompt example is *"Feature folder: docs/features/<name>/. Invocation 1 — Deriving."* — **no number**; no line of the command says to pass one; cmd 133–134 still says the highest file at the root *"carries the numbering"*. | **Agent side conforming; the fact it relies on is not given — BLOCKING at run time** (D-11). The number is needed at invocations 1, 2 (new file, 506) and 4 (277) |
| C10 | "Alone" is among questions files — not the other agents' — and the table's three other inputs stand | Lines 501–503, exactly that. | **Conforming** |
| C11 | A new questions file, numbered like invocation 1's, listed among invocation 2's outputs and counted in the report | Table row 2 output (275); move 2 (505–508). Report line 181 (*"How many questions you raised"*) is generic enough to count it. | **Conforming** |
| C12 | "Build files" named in universal terms — the files the build tool and the analysers read to configure themselves, the manifest among them; "somewhere" bounded to that class plus the conventions file in force | Lines 70–73: the definition, verbatim. **Line 568–570 unchanged**: *"does the project already declare it somewhere?"* — not bounded. Lines 65–66 and 251–252 still forbid *"a manifest"* in the same breath. | **Half applied — TO FIX**: definition yes, bound no (D-13) |
| C13 | One line true at both invocations: a rule the project chose is a convention whether or not a tool can check it; a tool's checking it sets the test kind and nothing else; what is refused is what the platform imposes or holds on one machine | Line 582: the filter row replaced by *"⚠️ Not this one — A tool checking it sets the rule's test kind and nothing else — a rule the project chose is a convention whether or not a tool can check it"*. | **Conforming in substance.** The heading still says *"three filters"* (575) and the table now holds a row that is not a filter — D-5 |
| C14 | Move 5 adds the new rule's line to the second table and a first-table line naming the request — **or** `couverture.md` leaves invocation 3's inputs; "one reader, once" corrected | Second table gone (§4). Table row 3 now lists `couverture.md` as **input and output** (276). Readers corrected: *"the Product Owner, and you — at invocations 2, 3 and 4"* (170–171). **No move of invocation 3 (557–638) reads or writes `couverture.md`**; the file's shape (one line per entry of the technical document, 146–147) has no slot for a request-motivated rule. | **Partially conforming — TO FIX**: the pass's defect ("declared an input and touched by no move") is now "declared an input and an output and touched by no move" (D-12) |
| C15 | The conventions file absent at 2 or 3 is a block, *To resume* = run `/conventions` invocation 1; at 3 when the Arbitre called, the refusal in the verdict says the same; "mandatory-sections file" replaced by the path | Lines 209–219: all three, *"docs/TECHNICAL_CONVENTIONS.md"* named, invocation 4 added. | **Conforming.** Line 218 says *"At invocation 3, where a block is forbidden"* as if the whole invocation forbade it — D-3 |
| C16 | An absent `## Verdict` heading counts as empty; the agent adds the heading and writes under it | Lines 564–566, exactly that. | **Conforming** |
| C17 | Within invocation 3 a request has two exits — settled or refused; a block exists for a missing input only | Lines 630–634: *"You settle or you refuse — and you go out. Never a blocking file here: a missing input is the only thing you ever block on, and it is not a request."* | **Conforming.** Three passages now describe the invocation-3 block in three shades — D-3 |
| C18 | Either a move names what it does with the record, or the numbered files are history and declared unread; **and** the *Filled → Apply it* row says what applying a decision to a missing-input block means | Line 319: *"The numbered ones are history — you never read them."* Row 309 unchanged: *"Apply it, rename it … carry on"* — nothing says what applying means. | **Half applied — TO FIX** (D-17) |
| C19 | Each rule stands without its reason (move 7's "four hundred tokens"; the conjunction paragraph; invocation 3's "and for good reason"); the "segment" example dropped or made general | Line 439: *"What identifies a record"* — generalised. **Unchanged**: 376–378 (*"costs four hundred tokens read at every lot"*), 434–437 (the conjunction paragraph), 552–555 (*"and for good reason — here you are not deriving a file…"*). **Added**: new justifications at 107–109, 401–403, 422–424, 676–679. | **Only the example applied — TO FIX**, or reclassify as *partiellement passé*: the justification half, which the pass calls the only measure claimed, was not done and the pattern grew |

### Comments listed PASSÉ — command files (spot check)

| # | Expected | Found (cmd) | Verdict |
|---|---|---|---|
| CMD1 | Terminal state from presence; integrated file leaves the root; rows for "nothing asked" and "all integrated"; row 1 fires only on a feature not derived — presence test on `couverture.md` | conventions 66–76: eight rows in that order, `couverture.md` test (74–75), invocation 4 row (75); 83–86: integrated file leaves the root. | **Conforming.** cmd 133–134 (*"every `questions-architecte-*.md` but the highest — the last one stays at the root, it carries the numbering"*) contradicts 83–86 within the command — NOTE, for the command's own verification |
| CMD2 | Feature folder from the first argument; second names the `bugfix-NN` | conventions 18–20, 27. | **Conforming.** The invocation example shows invocation 1 only; the comment asked for the invocation 3 form too (cmd 100–105) — NOTE |
| CMD3 | The empty-`Answer:` test is a grep; the reading rule says grep yes, opening no | conventions 33–38: *"plus two greps … `Answer:` lines with nothing after them, and `^### Q` … Counts, never content"*. | **Conforming** |
| CMD4 | commit, merge, push, remove — in every command invoking an agent without Bash | conventions 161–164: `git add` and `git commit` inside the worktree, the reason given. | **Conforming** (7_lots/8_code not re-read for this line) |
| CMD5 | First row: a block with an empty decision → relay and stop; the relay names the file | conventions 69, 183–184. | **Conforming** |
| CMD6 | One line per outcome — questions → answer, re-run; none/integrated → `/7_lots`; blocked → fill, re-run | conventions 186–193: four rows, plus the product-question row. | **Conforming.** No row for an *inconsistency* answer — C3(c) |
| CMD7 | The root is a third place for a blocking file; move outcomes written | 8_code 315–320: *"two places: `code/<lot>/blocked_<agent>.md` for the five agents of the loop, and `blocked_architecte.md` at the working folder's root"*; move 7 outcomes 180–185. | **Conforming** (the count matches its own list; the `code/blocked_<agent>.md` place of the old command is no longer listed — a fact for 8_code's own verification) |
| CMD8 | The row says a block from this agent means a missing input, the conventions file first, and what to run; the refusal outcome named | 7_lots 121–125: *"It blocks on a missing input, the conventions file first of all — not on the request … Say to run `/conventions`."* Row 94: a filled verdict → invoke `cadreur`. | **Conforming**. No bound on the block → architecte → block loop (U11) — outside this agent |

### Comment listed ÉCARTÉ

| # | Expected | Found | Verdict |
|---|---|---|---|
| C20 | Grid read by part per invocation — **not** applied | Lines 54–56 unchanged: *"`docs/process/GRILLE_CONVENTIONS.md`, in full, at every invocation"*; the table has no part column. | **Correctly NOT applied** |

---

## B. Unannounced changes

Every hunk of the diff was matched against C1–C19 and §1–§6. What remains:

**B-1 — line 146–147 (old), dropped.** Old: *"📌 One reader: the Product Owner, once. 🔴 It
carries no rule text — the conventions file holds those."* New (170–171): *"📌 Its readers: the
Product Owner, and you — at invocations 2, 3 and 4, to know which entries are already
covered."* C14 asked for the reader line to be corrected; **the "carries no rule text" rule
was deleted with it**, and nothing asked for that. What it changes: nothing now stops a coverage
line from quoting a rule. NOTE.

**B-2 — lines 401–403, added.** *"🔴 A rule written from a wrong recollection at invocation 1
is read by every lot of the feature, where one at invocation 3 governs a single request."* This
is the pass's *Justification* field for C5, promoted to a 🔴 rule. Not a fix C5 asked for;
against C19's direction. NOTE.

**B-3 — lines 116 and 124–125, added.** *"at the end of the line"* — §3 said nothing of where
the marker goes; a placement decided here. *"🔴 The Réalisateur reads every `permanente` rule,
whatever its lot, and only the `spécifique` ones its sheet names"* — a statement about another
agent, true of `realisateur.md` 67 (and `concepteur.md` 58, `testeur.md` 66, unnamed here), not
in §3. What it changes: this file now carries a fact it does not own, and it goes stale if the
Réalisateur changes. NOTE.

**B-4 — lines 107–109, added.** *"⚠️ a spec sheet cites `R30`, and renumbering would point
every citation at another rule with nothing able to detect it."* C7's *Justification*, in the
rule. Same pattern as B-2. NOTE.

**B-5 — lines 509–513, added.** *"⚠️ An answer you cannot found a verifiable rule on is such an
answer — 📌 « an error message is shown » does not say which, where, in what form. 🔴 You never
write a rule your own `Precision` closure would refuse."* §6 said "une réponse qui ne la fonde
pas"; the criterion is a reasonable reading of it, but *"`Precision` closure"* is a term that
exists nowhere else in the file (the table row is *"Precision — Settle it yourself"*). What it
changes: introduces a name with no referent (D-18). NOTE.

**B-6 — lines 470–486.** The Product Owner is *"himself"*, *"his decision"*, *"he judges"*,
*"what he settled"* — the first gendered references in the file; `CLAUDE.md` says *"She
launches a command"*. Carried over from the French spec ("il"). NOTE.

**B-7 — line 72–73.** Old: *"and only it — see there for why."* New: *"and only it. 🔴 The
build files are … 📌 the dependency manifest among them. ⚠️ That class, and nothing beyond it —
see there for why."* The C12 insertion split the old sentence; *"see there for why"* now hangs
off *"nothing beyond it"*, whose "why" is not at invocation 3 (the definition's reason is nowhere).
NOTE, cosmetic.

**B-8 — line 319, reflowed.** The C18 change collapsed a three-line paragraph into one long
line (the only line of the file over 80 columns). NOTE, cosmetic.

Nothing else in the diff falls outside the pass or the six modifications. No section moved; no
table was rewritten beyond what C2, C13, C14 and §1–§2 asked.

---

## C. Gestures against tools

**Frontmatter** (line 4): `Read, Grep, Glob, WebSearch, WebFetch, Edit, Write`. No `Bash`, no
`Agent`.

### Gestures with no tool

**C-1 — BLOCKING (pre-existing, never flagged) — line 309–314.** *"rename it
`blocked_architecte-NN.md`"* … *"🔴 Renaming means renaming — ⚠️ `git mv`, or the equivalent:
one file, under a new name. 📌 Never write the numbered one and leave something at the old
name — not a copy, not a note, not an empty file."* With `Write` and `Edit` alone the agent can
create the numbered file and can empty or overwrite the old one; it cannot remove it. The rule
forbids every state the tools can reach. Same rule, same tool list, in `detailleur.md`,
`diagnostiqueur.md`, `fusionneur.md`, `relecteur.md` (and `realisateur.md`, which has Bash) —
a chain-wide question: does the harness rename on the agent's behalf, or is "the equivalent"
meant to be done by the command? If neither, the resume path cannot be walked.

**C-2 — TO FIX — line 309, 303–304.** *"rename it `blocked_architecte-NN.md`"* — which `NN`?
*"Several `blocked_architecte-NN.md` beside it are settled ones"* — and line 319: *"you never
read them"*. Finding the next number needs a listing (forbidden, 88–91, except `architecte/`
at invocation 3) or the prompt (which names nothing of the sort). Compare `classeur`'s rule
"highest in the folder plus one, `01` when none". No means given.

**C-3 — TO FIX — lines 70–73, 253–254, 552–553.** *"Invocation 3 may open the build files, and
them alone"* — *"the ones the build tool and the analysers read to configure themselves"*. The
class is named; its instances are not. Locating them needs a `Glob` at the repository root,
which lines 88–91 and 244–246 forbid (*"Invocation 3 lists `architecte/`, and nothing else"*).
Question: is the agent expected to know the file names per platform (`pubspec.yaml`,
`analysis_options.yaml` …) and `Read` them by path, blind to whether they exist?

**C-4 — see D-11 — line 462–463.** *"The prompt names your number"* — the command's prompt
does not. A fact with no source, at three invocations.

### Gestures whose tool is forbidden by the text

**C-5 — see D-2.** `WebSearch`/`WebFetch` are in the frontmatter for all invocations; line 400
requires lookup *"at every invocation"*; lines 69 and 552–555 forbid the web outside invocation
3. The tool is there; two rules say opposite things about using it.

### Tools no gesture names

**C-6 — NOTE.** `Grep` — no move names it. Plausible uses exist (move 2 of invocation 3
*"does the project already declare it somewhere?"*; invocation 3 move 4 *"a rule that already
carries it"*; the directives table *"A rule already says the same"*; invocation 4 *"what the
file does not already cover"*), but every one of them is phrased as reading, not searching. Not
a defect; a tool left implicit.

**C-7 — NOTE.** `WebFetch` — line 572–573 says *"A platform's own documentation settles in one
search"*; nothing says to fetch a page. Implicit, acceptable.

### Gestures with a tool — checked, fine

`Read` by path (88); `Glob` of `architecte/` (546–547); `Write` of the conventions file,
`couverture.md`, the questions file, the blocking file (97, 146, 199, 446); `Edit` at 2, 3, 4
with the *When `Edit` fails* section (258–264); `Edit` to add a `## Verdict` heading (565);
`Read` of `par-genre/directives.md` (469).

---

## D. Internal coherence

**D-1 — TO FIX — invocation 4 not propagated.** Lines 43–45: *"Invocations 1 and 2 run on a
feature folder only … Invocation 3 runs on either"* — 4 unmentioned. Line 85: *"Invocations 2
and 3 read the file in force"* — 4 reads it whole (277, 660). Lines 242–243: *"Invocations 2 and
3 read the one in force: they amend it"* — same. Line 292: *"Invocation 2 runs only when
invocation 1 asked something"* — or 4 (277), or 2 itself (275). Lines 286–288: *"a rule that
needs a feature's documentation … is a rule invocation 1 owed"* — or 4. Five stale counts of the
invocations.

**D-2 — BLOCKING — the web.** Line 400–401: *"⚠️ A fact about the platform is looked up, never
recalled — 📌 at every invocation."* Line 69: *"📌 Invocation 3 reads the build files and the web,
and only it."* Lines 552–555: *"⚠️ This invocation alone may read the web and the project's build
files. 📌 Everywhere else those are forbidden."* Table row 1 and row 4: no web among the inputs.
A rule and its opposite, both marked. An agent at invocation 1 filling a hole from "the
platform's own practice" (361–362) has no permitted way to obey line 400.

**D-3 — TO FIX — when invocation 3 may block.** Line 191: *"At invocation 3, when the Arbitre
called you, you do not block"* (the Arbitre case only). Lines 209–211: a block at *"invocations
2, 3 and 4"* on a missing conventions file. Line 218: *"At invocation 3, where a block is
forbidden, the refusal in the verdict says the same"* (the whole invocation). Lines 631–632:
*"Never a blocking file here: a missing input is the only thing you ever block on, and it is not
a request"* (never here — yet a missing input may occur here). Which is it when the orchestration,
not the Arbitre, invokes 3 and the conventions file is absent: a blocking file (209–211, and
cmd 7_lots 121 expects one) or a refusal in every verdict (218)?

**D-4 — TO FIX — two kinds where there are three.** Lines 181–182: *"How many questions you
raised, and of which kind — coverage or conjunction."* Lines 459–460: *"Each entry says which
kind of gap it is — coverage or conjunction."* Line 405: *"Four kinds of gap, and only three
leave this agent"* — coverage, conjunction, inconsistency (409–411). An inconsistency entry
cannot say its kind under 459–460, and the report cannot count it under 181–182.

**D-5 — TO FIX — "three filters".** Line 575: *"Put it through the three filters."* Table
579–583: row 1 a filter, row 2 *"⚠️ Not this one"*, row 3 a filter. Two filters and a row that
says it is not one, under a heading *"It is not a convention when"*.

**D-6 — TO FIX — the product-question mark has no form.** Line 419: *"You mark it as a
product question, distinctly from the others"*. The entry shape (450–453) is four lines —
`### Qn`, `Block:`, `Question:`, `Answer:` — and 459–460 adds *"Each entry says which kind of gap
it is"* without saying where. Where does *product question* go, in what words? The command
relays *"a product question"* (cmd 190) and would need to grep it.

**D-7 — TO FIX — a branch that leads nowhere.** Lines 526–527: *"An answer to a coverage
question is not a rule either — it is a behaviour, and it belongs to the product file."* No move
of invocation 2 carries it anywhere — not the report (unlike the inconsistency answer, 523–524),
not the coverage line, not a file. And cmd conventions 57–58 stops the run while any `Answer:` is
empty, so the Product Owner must answer the product question **in this file, in French** before
invocation 2 can run at all — after which the answer sits in a file nothing reads. Question: is
the intended route "the Product Owner puts the behaviour in the product file by hand and the
architecte question is answered *voir produit*"? If so, say it; if not, what carries it?

**D-8 — TO FIX — "Ten moves" and the directives.** Line 331: *"Ten moves, in this order."*
Lines 490–491: *"at 1 you derive first, then integrate them"*. None of the ten (333–390)
integrates the directives. Before move 7's write or after? Before move 9's check (so a directive
rule appears in `couverture.md`) or after? Do directive rules get a coverage line at all — the
first column is *"entry of the technical document"* and a directive is not one? Does a directive
rule carry `permanente`/`spécifique`? An eleventh move with no place.

**D-9 — TO FIX — invocation 4's procedure.** Lines 660–662: *"walk part B of the grid on this
feature's documents, as invocation 1 does"*. Part B is move 5. Are moves 2 (tracabilite), 3
(readings V1–V10 — part A), 4 (anomalies), 6 (off-grid), 9 (coverage check), 10 (questions
file) run too? Row 4 lists `tracabilite.md` and *"a questions file"* among its inputs/outputs,
which implies moves 2 and 10 at least. Nothing says.

**D-10 — TO FIX — two rules for one case.** Directives table, line 484: *"A rule contradicts
it — 🔴 The directive wins — ⚠️ and you say so in your report"* — at invocation 4 too (490–491).
Invocation 4 table, line 674: *"A rule in force says the opposite of what this feature needs —
🔴 You never replace it yourself — 📌 you raise it"*, and 676–679 say why (code already coded
under the old rule). A directive of feature N+1 that contradicts a rule in force at invocation 4
is exactly the replace case. Does the directive win, or is it raised? Line 484's reason (*"your
grid produced something the Product Owner refuses"*) is also false at 4 when the rule was a
settled request from a lot.

**D-11 — BLOCKING (cross-file) — the questions-file number.** Line 462–463: *"🔴 The prompt
names your number — 📌 the command has the fact, and you never list a folder to find it."* cmd
conventions 100–105: the prompt is *"Feature folder: docs/features/<name>/. Invocation 1 —
Deriving."*; no line of the command computes or passes a number; cmd 133–134 still says the
highest file left at the root *"carries the numbering"* — for whom, if the agent may not look?
The same number is needed at invocation 2 (506: *"numbered like invocation 1's"*) and 4 (277).
An agent that obeys 463 has no number; one that disobeys it lists the folder.

**D-12 — TO FIX — `couverture.md` at invocation 3.** Table row 3 (276): input **and** output
*"`couverture.md`, updated"*. Moves 1–5 of invocation 3 (559–638): no read, no write of it. And
the file's definition (146–147: *"One line per entry of the technical document, in its order"*)
has no line shape for a rule a request motivated. What line would invocation 3 add, and where?

**D-13 — TO FIX — "somewhere".** Line 568–570: *"does the project already declare it
somewhere?"* — the bound C12 asked for (the build-file class plus the conventions file) is not
here, though the class is defined at 70–73. Lines 65–66 (*"not a manifest"*) and 251–252
(*"a build file, a manifest"*) still forbid what 71 includes among the build files; the
exception at 253–254 resolves it only by inference.

**D-14 — TO FIX — `off-grid`, two places.** Lines 160–163: *"carries `off-grid` at the end of
its line [in `couverture.md`] … There, and nowhere else."* Line 374 (move 6): *"Each cites the
entries that state it, and carries `off-grid`"* — "each" is a rule. Lines 237–238: *"Write a
rule the grid did not fire, unless it carries `off-grid` and cites the entries"* — the rule
carries it. Line 180: *"how many carry `off-grid`"* — rules carry it. One 🔴 says nowhere else;
three lines say on the rule.

**D-15 — NOTE — the rule line's tail.** Line 116: `permanente`/`spécifique` *"at the end of
the line"*. Lines 165–167: the test kind *"is written in the conventions file itself, on the
rule"* — no form, no place. Two things at the end of a rule line, one of them shapeless. What
does a rule line look like in full? No example in the file.

**D-16 — NOTE — broken markup.** Lines 353–356: *"🔴 \*\*every anomaly part A names for its
reading\*\*, 📌 \*\*a cycle in V2, numbers that disagree in V5, diverging pairs in V7. 🔴
\*\*You name the anomaly and the identifiers. You never write the answer.\*\*"* — the 📌 span's
`**` is closed by the `**` before *You name*, leaving *You name … answer.* unbolded and a
trailing `**` orphaned.

**D-17 — NOTE — "Apply it" applies nothing.** Line 309: *"Filled — Apply it, rename it
`blocked_architecte-NN.md`, carry on."* Every block this agent may raise is a missing input
(209–211); a `## Decision` on a missing input is at most "it is there now" or "run
`/conventions`". C18 asked the row to say what applying means; it does not.

**D-18 — NOTE — a term with no referent.** Line 512–513: *"your own `Precision` closure"*.
`Precision` is a table row (412); "closure" appears nowhere else. Read as "the rule you would
apply to a precision gap" it works; as a named thing it points at nothing.

**D-19 — NOTE — "The third kind is not a gap".** Line 439, unchanged from the old file where
there were three kinds. With four kinds (405), the non-gap is the fourth (412).

**D-20 — NOTE — "Three lines, no more".** Line 177: the report is three lines. Line 484: *"and
you say so in your report"* (a directive overrode a rule). Lines 523–524: *"you say in your
report what has to be fixed upstream"* (an inconsistency answer). Two new report lines, one
cap unchanged.

**D-21 — NOTE — invocation 4's question has no kind.** Line 674: a contradicting rule is
*"raised"* — in the questions file, presumably (277). Under 459–460 every entry says its kind;
none of the four (409–412) is "a rule in force contradicts what this feature needs". Also line
678–679 asks the entry to say three things, which the four-line shape (450–453) does not hold.

**D-22 — NOTE — `## Verdict` heading added, but "Every request gets a verdict".** Lines
564–566 (add the heading) and 626–628 (every request gets one) agree; fine. Listed only because
line 549–550 (*"no request with an empty `## Verdict` — say so and stop"*) predates C16 and would
read a heading-less request as "no request" — the two lines should use the same test.

---

## Summary

- **BLOCKING**: D-2 (web lookup required at every invocation, forbidden outside 3), D-11 with
  C-4 (the number the prompt must carry, and does not), C-1 (rename without a rename tool —
  pre-existing, chain-wide, never examined).
- **Listed passé but half done**: C1 (R4), C3 (move 2 wording, the coverage line, the command
  relay), C6 (two passages still put `off-grid` on the rule), C12 ("somewhere"), C14 (no move
  writes `couverture.md` at 3), C18 ("Apply it"), C19 (the justifications — only the example was
  done, and four new justifications were added).
- **New contradictions the six modifications introduced**: D-3 (three shades of the invocation-3
  block), D-8 (directives have no move at invocation 1), D-9 (invocation 4's procedure), D-10
  (directive wins vs never replace), D-7 (the coverage answer goes nowhere).
- **Correctly not applied**: C20.
