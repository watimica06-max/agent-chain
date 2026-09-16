# V2.4 — Paths and loops, downstream

READ-ONLY investigation. Nothing modified.

**Scope**: `/7_lots`, `/8_code`, `/9_controle`, `/deploie`,
`/diagnostique`, `/audit_blocages`, `/audit_conventions`, as they stand
in `.claude-new/commands/`, and the agents those commands or their
agents invoke: `cadreur`, `verificateur`, `detailleur`, `concepteur`,
`testeur`, `realisateur`, `relecteur`, `arbitre`, `architecte`
(invocation 3), `controleur`, `diagnostiqueur`.

**Method**: every command read whole; of each agent, the frontmatter,
the *What you read / What you write / When you cannot produce / When
you resume* sections, and the moves a loop turns on. Line numbers refer
to the `.claude-new/` files. `docs/refonte/modifications.md` was opened
only for the `8_code` / `7_lots` section (lines 1405–1436), to know what
the attempt counter and the third-redécoupage stop were meant to be.

Severity: **BLOCKING** — a loop that cannot terminate, a state with no
outcome that the chain will hit, or an exit that is unreachable ·
**TO FIX** — a rule the files contradict or leave one step short ·
**NOTE** — a wrinkle worth knowing, not a hole.

---

## 0. Summary — the findings that matter most

| # | Where | Finding | Severity |
|---|---|---|---|
| F1 | `7_lots.md` L93–94 · `cadreur.md` L272–281 | The Architecte round-trip never lifts a Cadreur block: the Cadreur stops on an empty `## Decision` before reading any verdict → `/7_lots` re-invokes it for ever | BLOCKING |
| F2 | `7_lots.md` L75–78 · `verificateur.md` L437–441 · `8_code.md` L311–313 | Nobody archives `code/redecoupage.md`: the command says the Vérificateur does, the Vérificateur says the command does, and the command has no row for it → `/8_code` ↔ `/7_lots` cycle | BLOCKING |
| F3 | `8_code.md` L281–284, L361–379 · `7_lots.md` L172–214 | `/7_lots` run from inside `/8_code` creates a second worktree of the same name from a `HEAD` that holds none of the lots coded this run — the Vérificateur then sees no `PASS` and the Cadreur may re-cut coded lots | BLOCKING |
| F4 | `8_code.md` (no rule) · `detailleur.md` L4 · `relecteur.md` L4, L204–206 · `concepteur.md`, `testeur.md` (no rule) | A lot-level blocking file with a filled `## Decision` is never renamed: two of the five agents lack the tool, two lack the rule, the command has no step → re-applied on every later run, invisible to `/9_controle` phases 5–6 | BLOCKING |
| F5 | `8_code.md` L109–120, L351 · `relecteur.md` L53–69, L144–147 | The attempt counter: the Relecteur must read the verdict it replaces but its reading list excludes it; the "committed nothing" attempt increments nothing; "three retries" vs "fails three times" differ by one; a missing `## Attempts` has no outcome; a lot that reached the cap has no exit | TO FIX |
| F6 | `8_code.md` L118–120, L253–254 · `relecteur.md` L105–109, L154 | Escalation to `opus`: `## Cause` is overwritten at each verdict, so "twice" exists only in the run's memory, which L112 forbids; the token `reasoning` is never defined by the writer | TO FIX |
| F7 | `8_code.md` L272–279 · `cadreur.md` L859–878 | The third-redécoupage stop counts on-disk numbers (across runs) where the spec says "of this run", is off by one on "the highest number", and relays a `## Ce qui revient` that the third round never wrote | TO FIX |
| F8 | `8_code.md` L81–93, L60–61 | Resuming a lot that already has `conception.md` / `tests.md` re-runs the concepteur and the testeur "on every lot" — no test like move 1's on the sheet | TO FIX |
| F9 | `9_controle.md` L17–21, L45–53, L198–231 | The correction-cycle branch is unreachable: the command has no test that says it is on one, always works in the feature folder, and phases 4–6 read the feature's `code/` | BLOCKING |
| F10 | `9_controle.md` L198–203 · `controleur.md` L212–227, L266 | Phase 5 reads `Doubtful` and `Missing`; the agent writes `## Doubts` and `## Intentions missing` | TO FIX |
| F11 | `diagnostique.md` L156–165 · `diagnostiqueur.md` L4, L148–192 | A phase-2 block can only be lifted by a decision the agent says cannot lift it; the agent cannot rename what it applies | TO FIX |
| F12 | `testeur.md` L125–190 | The testeur never commits — its tests sit uncommitted; the realisateur's `git restore` on a redécoupage, and the worktree removal at the end of the run, both meet them | TO FIX |

---

## 1. `/7_lots`

### 1.1 States at launch, and their outcome

The command says the folder state is not its to read (L47–51) — the
Cadreur dispatches on disk (`cadreur.md` L272–281). Both tables were
crossed.

| On disk | Command | Cadreur | Outcome written? |
|---|---|---|---|
| No `spec-technique.md` and no `desc-bug.md` | invokes | blocks, `code/blocked_cadreur.md` (L115) | yes — row L95, stop |
| Both documents | invokes | blocks (L115, L301) | yes |
| No `docs/TECHNICAL_CONVENTIONS.md` | invokes | blocks (L116) | yes — but `## To resume` says run `/conventions`, and the command's row L95 says the Product Owner fills `## Decision`. A decision cannot make a file appear. **NOTE** |
| Nothing in `code/` | invokes | block A | yes |
| `code/sequence.md`, `## Defects` empty, no other file | invokes (L47: "produces a split in every state but one") | dispatch table L272–281: none of the four → **A — a first split** | **TO FIX**: the command says one state produces no split (L48) and never says which; the Cadreur re-cuts a split that holds. Presumably the "one state" is the empty-Decision block, but a clean `sequence.md` re-launched by hand also re-cuts everything |
| `code/sequence.md` with `## Defects` lines | invokes | **B** — take-back from cold | yes |
| `code/redecoupage.md` | invokes | **C** | yes — see F2 for what happens after |
| `code/redecoupage.md` **and** defects | invokes | **C** wins (L283–286) | yes |
| `code/blocked_cadreur.md`, `## Decision` empty | invokes | stops (L279) | yes — row L95, stop |
| `code/blocked_cadreur.md`, `## Decision` filled | invokes | **D**, then dispatch again | yes — the command renames (L96) |
| `code/blocked_cadreur.md` empty **and** `architecte/cadreur.md` empty verdict | `architecte` inv. 3, then `cadreur` | see 1.3 | **F1** |
| `code/blocked_verificateur.md` left from an earlier run | invokes | ignores it — never looks for one (`verificateur.md` L254–256) | **TO FIX** — see 1.4 |
| `blocked_architecte.md` at the root, `## Decision` empty | L121–125: stop, say run `/conventions` | — | yes |
| `blocked_architecte.md` with a filled `## Decision` | no row | — | **NOTE**: the Architecte applies it on its next invocation 3 (`architecte.md` L300–312); the command's "pending requests" step will invoke it only if a request has an empty verdict. If the block was on the conventions file itself, the PO ran `/conventions` and the file is stale. No outcome, but no loop |

### 1.2 The loop: the Cadreur's three rounds with the Vérificateur

**Who counts**: the Cadreur, in its own context (`cadreur.md` L23–26,
L779–780). It "lasts the whole of it" and does not go out between
rounds (L755–757). The command does not loop (`7_lots.md` L84–86).

**Each round**: a fresh `verificateur` (L787–788), which "never looks
for what an earlier round of yourself reported" (`verificateur.md`
L224–225, L235–245).

**Exits, all reachable within the Cadreur**:

| Return | Exit | Written at |
|---|---|---|
| `## Defects` empty | out, split holds | `cadreur.md` L775 |
| `## Defects` lines, round < 3 | correct the named lots, call again | L776 |
| `## Defects` lines, round = 3 | `code/blocked_cadreur.md` naming what would not converge, out | L779–781 |
| no `sequence.md` **and** `blocked_verificateur.md` | out without correcting | L773 |

**Termination holds** — the counter is in one context for the whole
run, and every branch of the table exits. Three remarks:

- **NOTE** — the exit "no `sequence.md` and a `blocked_verificateur.md`"
  (L773) is written for round 1. In round 2 or 3 a `sequence.md` from
  the previous round is already on disk (the Vérificateur writes over
  it, L421–422), so the first half of the condition is false; the Cadreur
  would fall to "`## Defects` carries some" on a stale file and correct
  against last round's defects. Unlikely (the Vérificateur blocks on a
  missing lot list or inventory, which existed in round 1), but the
  condition should be on the blocking file alone.
- **NOTE** — after a third-round block, the PO fills `## Decision`,
  `/7_lots` runs again, D applies it, then dispatch finds `## Defects`
  → B → a fresh three rounds. Each decision buys three rounds; there is
  no cap on the number of decisions. That is PO-gated, so acceptable —
  but the Cadreur "never argues with a defect" (L246, L783–785) and the
  PO has no written way to overrule a defect she judges wrong: B
  corrects the lots the defects name, the Vérificateur raises the same
  defect, and the third round blocks again. The decision can only
  change the split, never the verdict on it.
- The `blocked_cadreur.md` of the third round sits beside a
  `sequence.md` carrying defects. Command rows L92 ("defects, and no
  blocking file") and L95 ("`blocked_cadreur.md` alone") are both
  phrased as exclusive, so the state *defects + blocking file* matches
  neither literally. The intent (stop, relay the block) is clear from
  L99–101. **NOTE**.

### 1.3 The Architecte round-trip — F1, BLOCKING

`7_lots.md` L93–94:

> `code/blocked_cadreur.md` **and** `architecte/cadreur.md` with an
> **empty** `## Verdict` → invoke `architecte`, invocation 3, then
> invoke `cadreur` again
> `architecte/cadreur.md` with a **filled** `## Verdict` → invoke
> `cadreur`: the verdict is what lifts its block

`cadreur.md` L272–281, PART 2, first thing every run:

> `code/blocked_cadreur.md` with `## Decision` **empty** → **Stop** —
> say the blocking file still stands

The Cadreur never reads `architecte/cadreur.md` on resume — `grep -n
verdict cadreur.md` returns the request template (L191), "a file
already there whose `## Verdict` is filled is answered — you never
reopen it" (L202), and two lines about `verdict.md` (L250, L832).
Nothing lifts its block but a `## Decision`, and the Architecte writes
verdicts, not decisions (`architecte.md` L191–195).

Trace: Cadreur blocks with request → command invokes Architecte →
verdict filled → command invokes Cadreur → Cadreur stops on empty
`## Decision` → command reads disk: `blocked_cadreur.md` +
`architecte/cadreur.md` filled → row L94 → invoke Cadreur → … The
table has no first-match rule and row L95 ("alone") does not apply
since the request is beside it.

Two ways out, both unwritten: the command copies the verdict into
`## Decision` (it is the only one with the tool and the standing), or
the Cadreur's dispatch checks `architecte/cadreur.md` before stopping.

`modifications.md` L1405–1413 asks for one more thing here — a
*refused* verdict is to be treated as a block and relayed — and does not
mark it done. The new `7_lots.md` does not distinguish refused from
written (L94: any filled verdict → invoke `cadreur`). With F1 fixed by
copying the verdict into `## Decision`, a refusal copied there would
send the Cadreur to re-block identically, so the refusal branch has to
be written either way. **TO FIX**.

### 1.4 `blocked_verificateur.md` — TO FIX

The Vérificateur's block carries no `## Decision` and "nothing resumes
from it… you never rename it" (`verificateur.md` L248–256). The command
stops and says the step before has to run again (L97). On that next
run the Cadreur ignores the file, the Vérificateur never looks for one,
a `sequence.md` is written — and the command's hand-back table still has
row L97 matching the stale file. Row L91 (clean `sequence.md`) and L97
both match; the table declares no order. Nothing ever removes the file:
the Vérificateur has no tool, the Cadreur has no tool, the command has
no step. Same shape as the `redecoupage.md` archive (F2) — one
mechanical file with no owner for its retirement.

`cycle.md` L88 (row 7) still routes a `verificateur` block "with
`## Decision` filled" — a state that cannot exist. Out of scope (V2.3),
noted for the crossing.

### 1.5 Git — NOTE

L172–214 files the `questions-*.md`, commits, creates
`.claude/worktrees/<name>`, and merges before handing back. Clean on a
stand-alone run. What happens when `/8_code` calls it is F3, under
`/8_code`.

---

## 2. `/8_code`

### 2.1 States at launch

| On disk | Outcome | Written at |
|---|---|---|
| No `code/sequence.md` | none — L38 reads it, L60 reads the order. Nothing says what to do without one | **TO FIX** (say: run `/7_lots`) |
| `## Defects` not empty | stop, run `/7_lots` | L69–70 |
| Every lot `PASS` | stop, `/9_controle` next (feature) / nothing (bug fix) | L63–67, L186–193 |
| `stop.md` at the feature root | L137: checked at move 6 only, i.e. after a lot. A run launched with `stop.md` already there codes one lot first | **NOTE** — `/cycle` checks it first (L79 row 1); this command does not |
| A lot with no `verdict.md` | first such lot is next | L60 |
| A lot with `verdict.md` FAIL, `## Attempts` < cap | "first with no PASS" → this lot; then move 1 (sheet exists) → move 2 **three agents on every lot** | **F8** — see 2.4 |
| A lot with `verdict.md` FAIL, `## Attempts` at cap | same rule picks it; nothing says stop before invoking | **F5(e)** — see 2.3 |
| `code/<lot>/blocked_*.md`, `## Decision` empty | stop, decision still to write | L122–125 (4b) |
| `code/<lot>/blocked_*.md`, `## Decision` filled | invoke the agent it names on the lot it names, even on a PASS lot | L342–345 — and then **F4** |
| `code/redecoupage.md` present | L311–313: run `/7_lots` — but only "a Détailleur reporting…" triggers that reading; the file itself is not in the launch tests | **NOTE** — with F2 fixed this row matters: a `redecoupage.md` on disk at launch means the last run stopped between the Arbitre and `/7_lots`. Say so explicitly |
| `blocked_architecte.md` at the root, empty | stop | L315–320 |
| `code/<lot>/reprise_realisateur.md` | name it in the Réalisateur's prompt | L105–107 |
| `architecte/*.md` with empty `## Verdict`, at launch | nothing until the end of the first lot (L152–154) | **NOTE** — "the pending requests wait for the next run, on the block they belong to" (L180–181) — so the first lot of this run is coded against conventions a request from the previous run was meant to amend |
| No `code/<lot>/fiche-executable.md` | `detailleur` on the block | L76–79 |

### 2.2 The per-lot loop — five agents, blocking one by one

Moves as written: **1** détailleur (if no sheet) · **2** concepteur →
testeur → réalisateur · **3** relecteur · **4** FAIL → fresh réalisateur
· **4b** empty-decision check · **5** divergences → détailleur · **6**
`stop.md` · **7** `architecte` inv. 3.

**If the Détailleur blocks.** It writes `code/<lot>/blocked_detailleur.md`
and calls the Arbitre itself (`detailleur.md` L310–341). Three returns:

| `## Decision` | Détailleur | Command |
|---|---|---|
| filled | applies, "renames", details the block (L335) | never sees a block. **F4**: the Détailleur has no Bash (L4), no tool deletes a file; "git mv, or the equivalent" (L425) has no equivalent in Read/Grep/Glob/Edit/Write/Agent. The file stays at the unnumbered name with a filled decision |
| filled, sends back to the split | writes no sheet, stops (L336) | "When the split comes back" L267–305 → `/7_lots`, then carry on. **F2, F3** |
| empty (Arbitre waited 20 min, L417–437) | stops, block as it stands (L337) | 4b on the next run → stop, relay. PO fills → next run L342 invokes the Détailleur → applies → cannot rename → **F4** |

Terminates within the run. Across runs, F4 makes the filled file
permanent: every later `/8_code` reads L342–345 ("a filled `## Decision`
is not a stop — invoke the agent it names… even on a lot already
carrying a PASS") and re-invokes the Détailleur on that lot before
anything else. The Détailleur re-applies, skips lots with sheets
(L467–472), and reports. Not infinite, but one wasted opus invocation
per run for the rest of the feature, and `/9_controle` phases 5–6 and
`/audit_blocages` never see the decision as settled (they read
`blocked_<agent>-NN.md`; the audit lists the file under *Still open*
for ever).

**If the Concepteur blocks.** Writes `code/<lot>/blocked_concepteur.md`
(L88–121). Does **not** call the Arbitre — the Arbitre would refuse it
anyway (`arbitre.md` L234–240: only `detailleur` and `realisateur`). The
command: "a blocking file from any of the three stops the lot there"
(L92–93) → "any other block → relay and stop, the PO fills
`## Decision`" (L334–335). So a compiler-level fact — "a type the
language does not have, a name it refuses" (L108–110) — goes straight to
a Product Owner who "does not code" (`CLAUDE.md` L40). **TO FIX** at
design level: either the Arbitre takes concepteur/testeur blocks, or
the command routes them back to the Détailleur (whose sheet is what is
wrong). On resume: the concepteur reads a filled decision **only when
the prompt names the file** (L119–121: "you never look for one
yourself"), and the command's template (L207–212) names no file. So
L342 "invoke the agent it names" reaches a concepteur that does not
know it was blocked → it redeclares from the sheet → blocks again on the
same signature. **BLOCKING for that path** (folded into F4 in the
summary since one fix — the command naming the file and renaming it —
covers both). And nobody renames it.

**If the Testeur blocks.** Writes `code/<lot>/blocked_testeur.md`
(L93–123). No Arbitre. No PART 2 at all: the testeur has no rule about a
blocking file on resume, neither looking for one nor being told one.
Same path as the concepteur, one rule shorter. **BLOCKING for that
path** (same fix as F4). Its own block cases: a criterion no test and no
manual line can carry (L111–115), and "one of the older tests fails"
(L167–168) — that second one is interesting: see F12, a dropped lot's
red tests are exactly what makes the *next* lot's testeur block here.

**If the Réalisateur blocks.** Writes the file, carries on with what
does not depend on it (L219–235), calls the Arbitre (L253–284):

| `## Decision` | Réalisateur | Command |
|---|---|---|
| filled | applies, `git mv` (it has Bash, L570), carries on | sees a report, invokes the Relecteur. Clean |
| filled + `code/redecoupage.md` | drops what it wrote, commits nothing, renames the block, stops (L286–308) | `/7_lots` — **F2, F3**, and see F12 for what "drop" leaves behind |
| empty | writes `reprise_realisateur.md`, commits what compiles, stops (L310–342) | 4b next run → stop. PO fills → L342 → Réalisateur with the reprise named in the prompt (L105–107) → resumes. Clean |

**If the Relecteur blocks.** Only "when there is nothing to judge — no
sheet, no report, or no code committed" (L208–211). No Arbitre (the
command says so, L327–328). Command: "any other block → relay and stop,
PO fills `## Decision`". The Relecteur "never retires it — the
orchestration does it, once the verdict is written" (L204–206). The
orchestration has no such step. **F4.** And the sensible answer to
"no report" — run the Réalisateur again — is not written; the PO is
asked for a decision on a mechanical absence, and on the next run L342
sends that decision to the Relecteur, which "applies it, then runs the
five checks" (L286) on a lot that still has no report.

**Net**: of the five, only the Réalisateur's block round-trips cleanly
across runs. The Détailleur's works within a run and leaks a permanent
file. The Concepteur's, Testeur's and Relecteur's have no resume path
that the files describe end to end.

### 2.3 The attempt counter — F5

**Where it lives**: `## Attempts` of `code/<lot>/verdict.md` (`8_code.md`
L112–114; `relecteur.md` L121–123, L144–147).

**Who writes it**: the Relecteur, on every verdict including PASS
(L194–195), as "the count the verdict you replace held, plus one — `1`
when there was no verdict" (L144–145).

**Who increments**: the Relecteur alone, by reading the previous verdict.

**Findings**:

- **(a)** The Relecteur's reading list (L53–69) does not include
  `code/<lot>/verdict.md`, and closes with "Nothing else" (L68). L144
  requires reading it. Internal contradiction; an agent that obeys L68
  writes `1` every time. **TO FIX**.
- **(b)** "An empty list means the realisateur committed nothing — that
  counts as a failed attempt, and the Relecteur is not invoked"
  (L102–103). The only writer of the count is not invoked, so the
  attempt is counted nowhere on disk. L112 forbids counting in memory.
  A Réalisateur that commits nothing three times is retried for ever.
  Also: in the five-agent loop the concepteur commits before the
  Réalisateur runs (`concepteur.md` L170), so a diff "between the lot's
  first commit and HEAD" is never empty — the rule is dead as written,
  and if "first commit" means the Réalisateur's, nothing identifies it
  (no commit-message convention anywhere; `grep -rn 'first commit'`
  finds only L98). **TO FIX** both ways.
- **(c)** The cap. L109–110: "Three retries maximum per lot". L351: "A
  lot fails three times". With `## Attempts` = number of verdicts, three
  retries is four verdicts (1 + 3), three failures is three. The
  command never states the number it compares `## Attempts` to. **TO
  FIX**: one number, one comparison ("stop when `## Attempts` reads N
  and `## Status` is a FAIL").
- **(d)** Missing `## Attempts` (a Relecteur that omitted the field, or
  a verdict written by the old three-agent chain): no rule. The command
  reads "three lines" (L41–43) and says nothing about a line not there.
  **TO FIX**: treat as `0`, or as a Relecteur fault — either, written.
- **(e)** No exit for a lot at the cap. L351 stops the run. The next
  `/8_code` picks "the first lot with no PASS" (L60) — the same lot —
  and either stops again on the count (if the orchestrator honours it
  before invoking, which no row says) or re-runs the loop (if it reads
  move 4 as applying only after a FAIL *in this run*). Either way the
  sequence is stuck: no lot after it can run ("a read, not a scan"),
  and the PO has no written gesture — delete the verdict? write a
  blocking file? send it to the split? — that reopens it. **TO FIX**:
  say what the PO does, and what the command does on launch when the
  count is at the cap.
- **(f)** `## Attempts` survives a redécoupage. L295–298 delete the
  stale *sheets* of uncoded lots; the FAIL `verdict.md`, `conception.md`,
  `tests.md`, `compte-rendu.md` of the lot in hand stay. If the Cadreur
  keeps its number (it may: "every other lot is yours", L837; only a
  *reused* number is forbidden, L252), the reshaped lot's first verdict
  reads `## Attempts` = old + 1. **TO FIX**: delete the lot folder's
  artefacts with the sheet, or say the Relecteur restarts at 1 when the
  sheet is newer than the verdict.

### 2.4 The escalation to `opus` — F6

`8_code.md` L118–120: "`Cause: reasoning` twice on one lot → the third
realisateur is passed `opus`". L253–254 repeats it.

- The Relecteur writes `## Cause` as "the category alone" (L154), one
  verdict file, replaced each time. The previous cause is gone from
  disk the moment the second verdict is written. "Twice" can only be
  known by the run's memory — which L112–116 rules out for the count
  sitting one line above it. A run restarted after a stop cannot
  escalate. **TO FIX**: either `## Cause` accumulates (one line per
  attempt — L108–109 already says "the threshold is set on the
  accumulated causes", which reads like an accumulation nobody
  specified), or the escalation is on `## Attempts` alone.
- The token. The Relecteur names the two categories as "understanding
  of the lot, or limit of reasoning" (L105–107) and gives `understanding`
  as the example value (L137). The word the command greps for,
  `reasoning`, is never fixed as the value of the second. **TO FIX**:
  two tokens, written in the verdict template.
- The form: the command writes `Cause: reasoning` (an inline field);
  the verdict has `## Cause` as a heading with the value beneath.
  Cosmetic; a reader that greps `Cause: reasoning` finds nothing.
  **NOTE**.
- Timing: "the third realisateur" — the first retry is the second
  Réalisateur, so two `reasoning` verdicts can only exist once the
  second Réalisateur has failed; the third then runs on `opus`. With
  the cap at three *retries* that leaves one more sonnet retry after
  the opus one; with the cap at three *failures* the opus attempt is
  the last. F5(c) decides which. **NOTE**.

### 2.5 Resuming a lot mid-way — F8

Move 2 says "three agents, in this order, on **every** lot" (L81–93).
Move 1 carefully tests on the sheet ("a block half-detailed would pass
a test on the block", L76–79). No such test exists for
`conception.md` or `tests.md`. Every time a lot is picked up with those
files already there — a FAIL verdict from a previous run, a
`reprise_realisateur.md`, a `stop.md` on the last lot of a run — the
literal reading re-runs the concepteur (which "writes the declarations
with empty bodies", `concepteur.md` L143–151, over symbols whose bodies
the Réalisateur has committed) and the testeur (which finds its new
tests *passing* against real bodies and must "rewrite" them, L157–160).
Within a run, move 4 says "on FAIL → a fresh realisateur" and skips
the two; across runs, nothing does. **TO FIX**: move 2 needs the same
shape as move 1 — the concepteur when there is no `conception.md`, the
testeur when there is no `tests.md`.

### 2.6 The return to the split — F2, F3, F7

**Who writes `code/redecoupage.md`**: the Arbitre (`arbitre.md`
L311–352), appending a section if the file exists (L320–322), then
writing "back to the split" in `## Decision` and naming the file
(L349–352). The Cadreur adds `## Ce qui revient` / `## Ce que j'en
fais` at the end of the same file (`cadreur.md` L859–878).

**Who reads it**: the Réalisateur — the file, not the decision's
wording, is its test (L290–297) · the Détailleur, on resume (L422–423) ·
`/8_code`, by presence (L267–268, L311–313) · the Cadreur, block C, in
full plus every `redecoupage-NN.md` (L824–828) · the Vérificateur, its
`## Ce qui est déjà codé` section (L66–72).

**Who archives it** — nobody:

- `7_lots.md` L75–78: "the Vérificateur keeps them where they ran and
  **archives the file** when the sequence is written".
- `verificateur.md` L437–441: "say in your report that it can be
  archived — and only when your `## Defects` section is empty. **You
  have no tool that renames a file — the command does it**, once you
  have reported."
- `7_lots.md` hand-back table L89–97: no row renames `redecoupage.md`.
  The only rename in the command is `blocked_cadreur.md` (L96).
- The Cadreur has no Bash either (L4).

Consequence: `code/redecoupage.md` stays after the re-split. Back in
`/8_code` (L281–289): next lot = first without PASS → the lot in hand,
whose `blocked_detailleur.md` or `blocked_realisateur.md` carries the
split decision. If it was the Détailleur: L342 → Détailleur → resume
table L422 "sending back to the split, **and `code/redecoupage.md` is
still there** → Stop, say the block is waiting on it" → command L311–312
"`code/redecoupage.md` still there → run `/7_lots`" → Cadreur block C
again, on a split it has just redone, appending nothing new but
re-running the three rounds → back to `/8_code` → same. If it was the
Réalisateur: its resume table L431 stops on "a decision sending the lot
back to the split" without even testing the file, so it stops for
ever. **BLOCKING** either way. Also: since the file is never numbered,
the Cadreur's "read every `redecoupage-NN.md` beside it" (L824–828)
never finds any, and the Arbitre's sections accumulate in the one file
instead — the count in F7 is then always zero.

**The count at the third — F7.** `8_code.md` L272–279: "Count the
redécoupages of this run — `code/redecoupage-NN.md` in the folder, the
highest number. At the third, you stop instead of running `/7_lots`.
Relay the Cadreur's `## Ce qui revient`."

- "of this run" vs. the highest `NN` on disk: the numbers, once
  archiving exists, persist across runs. The spec (`modifications.md`
  L1433–1435: "au troisième redécoupage d'une même exécution") wants
  the run's own count. Either the command counts in memory (the one
  case the spec asks for it) or it counts the disk and the words "of
  this run" go. **TO FIX**.
- Off by one: with `-01` and `-02` archived and a fresh `redecoupage.md`
  written, the highest number is 2 and this is the third. With the
  file not yet archived (F2), the highest number is whatever the last
  run left. Say the comparison: "highest `NN` ≥ 2 and a new
  `redecoupage.md`" or "highest `NN` = 3". **TO FIX**.
- `## Ce qui revient` is written by the Cadreur in block C — i.e. by the
  `/7_lots` the command has just decided *not* to run. The third
  `redecoupage.md` holds only the Arbitre's section. What can be relayed
  is the second redécoupage's `## Ce qui revient`, in `redecoupage-02.md`
  — which says what came back twice, not three times. **TO FIX**: either
  run `/7_lots` a third time and stop after it (the Cadreur then reports
  the pattern itself, L877–878), or relay the Arbitre's `## Ce qui
  bloque` of the third and the Cadreur's `## Ce qui revient` of the
  second, named as such.
- After the stop at the third, `redecoupage.md` stays unnumbered, the
  lot's block stays filled, and the next `/8_code` finds the same state
  and stops again (or loops, F2). There is no written exit — the PO
  "decides" (L278–279) but nothing says what her decision looks like on
  disk. **TO FIX**.

**Nested `/7_lots` — F3.** `8_code.md` L281–284: "run `/7_lots` on this
working folder, and wait for it. Then carry on your loop — you do not
hand back." `/8_code` is inside `.claude/worktrees/<name>` with the
Réalisateur's commits for the lots of this run, unmerged (L378–388
merge "when the run ends"). `/7_lots` L181–198 commits the feature
folder, then `git worktree add .claude/worktrees/<name> HEAD` — same
path (collision), and `HEAD` of the main checkout, which holds none of
this run's `verdict.md` files or code. The Vérificateur inside that
worktree reads `## Ce qui est déjà codé` and checks each lot's
`verdict.md` "still carries PASS… one that does not is not coded: order
it with the rest" (L69–72): every lot coded this run reads as uncoded.
The Cadreur may then re-cut them ("a lot whose `verdict.md` carries
PASS is closed" — none does, from where it stands). Then `/7_lots`
merges its branch (L200–204) while `/8_code`'s branch is still open,
and `/8_code` "carries on" in a worktree that has not seen the new
split. **BLOCKING**. The fix is one sentence in either file: when
invoked from `/8_code`, `/7_lots` skips its git section and runs in the
caller's worktree.

### 2.7 Other findings in `/8_code`

- L9 "runs `detailleur`, `realisateur` and `relecteur`" — five agents
  (L316 says so). L204 "The three agents of a lot" heads four
  invocation blocks. **TO FIX** (counts).
- L41–43 reads three verdict lines; L134–135 "You read two fields of a
  verdict — `## Status` and `## Symbol divergences`, and nothing else."
  Four fields are read. **TO FIX**.
- L337 "When you stop on a block, move 6 has not run — a request
  waiting in `architecte/`…": the Architecte step is move 7; move 6 is
  `stop.md`. **TO FIX**.
- L97–98 the diff "between the lot's first commit and HEAD": no commit
  message convention exists in `concepteur.md`, `realisateur.md` or
  `TECHNICAL_CONVENTIONS.md` as read by grep; across a restart the
  orchestrator cannot find the lot's first commit. **TO FIX** (a
  `<lot>:` prefix, or the concepteur's report carrying the SHA).
- L109 "a fresh `realisateur`, with the verdict": the template
  (L222–229) does not pass the verdict; the Réalisateur's PART 2 says
  "inputs: the same, plus the verdict" (L472–474) but has no "first
  thing, look for `verdict.md`" like it has for the blocking file. It
  works if the Réalisateur globs its lot folder; nothing says so.
  **NOTE** (V2.5b territory).
- L186–193 vs `9_controle.md` L45: `/8_code` says on a bug-fix cycle
  "nothing comes next"; `/9_controle` says it "runs on every correction
  cycle". One of them is wrong — see F9.
- L295–298 delete stale sheets: the orchestrator has Bash, fine. But
  the Détailleur it then invokes finds `blocked_detailleur.md` with the
  split decision and `redecoupage.md` — if archived — gone: L423
  "rename to its numbered form and detail the block" → F4 again (no
  tool).
- What "drop what you wrote" leaves — **F12**. The concepteur
  committed its declarations (L170); the testeur committed nothing
  (its five moves, L125–190, end on the manual list); the Réalisateur
  runs `git restore` (L570–571) on its own edits. After a redécoupage
  the branch holds committed empty-body declarations of a lot that no
  longer exists, and the working tree holds the testeur's red tests
  either as untracked files (never restored) or, if the Réalisateur
  staged them, as part of what it dropped. If they survive, the next
  lot's testeur blocks on "one of the older ones fails" (L167–168);
  if the worktree ends with untracked files, `git worktree remove`
  refuses and the command stops without removing (L390–393). Either
  way the Vérificateur's grep finds symbols in the tree that no PASS
  lot produced. **TO FIX**: the testeur commits (it has Bash), and the
  redécoupage path says who reverts the concepteur's and testeur's
  commits — or the Cadreur is told the stubs are there.

---

## 3. `/9_controle`

### 3.1 States at launch

| On disk | Outcome | Written at |
|---|---|---|
| No argument | ask, stop | L12–13 |
| No `desc-produit.md` | stop | L49–50 |
| A lot of `code/sequence.md` without a PASS verdict | stop, name it | L55–57 |
| `rapport-controle*.md` present | not a stop; next free number | L59–61 |
| A `bugfix-NN/` beside the feature | **no test** | **F9** |
| `code/controle/` with partials of an earlier run | emptied before phase 3 | L133–134 |
| No `tracabilite.md` | phase 1a reads it; no outcome without it | **TO FIX** — `architecte.md` L279 knows it "may not be there"; this command does not |
| No `code/recette.md` (no testeur line ever written — `testeur.md` L188–189 writes nothing rather than a line) | phase 4 reads it; no outcome | **NOTE** — write `recette-ordonnee.md` from `par-genre/recette.md` alone, and say the file was absent |
| No `par-genre/recette.md` | same | **NOTE** |
| No `blocked_<agent>-NN.md` anywhere | phases 5–6 produce empty files; L230–231 says write phase 6 even empty, phase 5 does not say | **NOTE** |

### 3.2 Six phases, three of which do not run on a correction cycle — F9

What the file says:

- L17–19: "Always the feature folder itself, never a `bugfix-NN/`… a
  correction cycle has neither." L21: "Every path below is relative to
  it."
- L45–47: "It runs on the main cycle and on every correction cycle. The
  Contrôleur runs on the main cycle alone."
- L52–53: "On a correction cycle — phases 1 to 3 do not run. The other
  two deliverables do."
- L67: "**Three phases.**" — followed by six.
- L203, L211: phase 5 reads "the `blocked_<agent>-NN.md` files of the
  **working folder**" — a term this command never defines (the others
  define it as the highest `bugfix-NN/`; this one forbids exactly that).

**Do the other three run?** Not as a correction-cycle branch, because
the branch cannot be entered: the command reads "only whether
`desc-produit.md` is there, and whether every lot of `code/sequence.md`
carries a `verdict.md` in PASS" (L27–28). Both are true of the feature
folder whether or not a `bugfix-03/` sits beside it. Nothing tests for
a `bugfix-NN/`, nothing says "the highest one is the working folder",
so the orchestrator has no fact that says *this is a correction cycle*.
It runs all six phases on the feature folder — the Contrôleur included,
re-confronting the feature's sheets — and phases 4–6 read
`code/recette.md`, `code/blocked_*-NN.md` and the feature's
`rapport-controle*.md`, i.e. the feature cycle's files, never the
correction cycle's `bugfix-NN/code/…` where the testeur (working folder,
`testeur.md` L52, L170) and the Arbitre (working folder) wrote them.
The three deliverables of the correction cycle are never produced from
the correction cycle's data. **BLOCKING** for the correction-cycle
claim; the main cycle is unaffected.

Two more counts in the same passage: "three things" (L36) are the
manual list, the register and the decisions — the control report is
not among them — so "the other **two** deliverables" (L53) should be
three; and `/8_code` L190–193 tells the PO that on a bug-fix cycle
nothing comes next. **TO FIX**: one command file says `/9_controle`
runs after a correction cycle, one says it does not; pick one, and if
it runs, give it the working-folder rule and a test.

### 3.3 Phases 1–3 (main cycle)

- Phase 1: two greps, the crossing, `tracabilite-full.md` at the
  feature root. The script's `parse()` (`grouper.py` L47–56) accepts
  `B59  —` (a block with no lot), as L91–93 needs. Consistent.
- Phase 2: `--auto` exists (`grouper.py` L220). `python3` on this
  Windows host is usually `python`; a question, not a finding.
- Phase 3: one Contrôleur per group, then assembly with the group list
  and the block list (L153–158) — `controleur.md` L239–247, L262–276
  expects exactly that. The Contrôleur "never writes a blocking file"
  (L70–84) so this phase has one exit: it reports. No loop.
- `controleur.md` L57–59 "a merged lot leaves no folder at all; you
  will not see it" — nothing in `/8_code` removes a lot folder after
  merge, and this command's own L27–28 needs every lot's `verdict.md`.
  Stale sentence in the agent (V1 scope), harmless here.

### 3.4 Phases 4–6

- **Phase 5 field names — F10.** L199–200 reads "the `Doubtful` and
  `Missing` fields of `code/rapport-controle*.md`". The Contrôleur
  writes `## Intentions found`, `## Intentions missing`, `## Doubts`
  (L212–227), and its own assembly text says "Under `Doubtful`"
  (L266, L268) — the agent is inconsistent with itself, and the command
  matches neither heading. **TO FIX** in both.
- **Phase 5 sources**: "the product questions the Arbitre handed back,
  in the `blocked_<agent>-NN.md` files" — with F4, the files that hold
  a handed-back-then-answered decision are never numbered, so the
  register misses exactly the cases it exists for. Fixed by F4.
- **Phase 6**: "gather them from the `blocked_<agent>-NN.md` files… every
  `## Decision` that settles what the application does". Same
  dependency on F4. Also: `/fusion` L64–69 reads
  `code/decisions-produit.md` "in cycle order — the feature's own first,
  then `bugfix-01`…" — it expects one per `bugfix-NN/code/`, which F9
  says is never written there.
- **Relay** L274–281: `code/rapport-controle-NN.md` — the first report
  is `code/rapport-controle.md` with no number (`controleur.md`
  L253–255). **NOTE**.

---

## 4. `/diagnostique`

### 4.1 States

| On disk | Outcome | Written at |
|---|---|---|
| No `bugfix-NN/` or no `bug-list.md` | stop, never create | L22–25 |
| `investigation/<id>.md` exists | skip the gap | L48–50 |
| `investigation/blocked_<id>.md`, `## Decision` filled | re-run that gap | L48–54 |
| `investigation/blocked_<id>.md`, `## Decision` empty, no report | **not skipped** — the skip rule tests the report, not the block → re-investigated → same block again, at "a full investigation" each time (L50) | **TO FIX** |
| `desc-bug.md` already there (phase 2 done) | no rule — phase 1 issues nothing, phase 2 runs again and rewrites `desc-bug.md`. On a folder whose `/7_lots` has run, that overwrites the document the split cites | **TO FIX** (stop when `desc-bug.md` exists, or say it is meant to be regenerated) |
| `blocked_diagnostiqueur.md`, `## Decision` empty | phase 2 → agent stops (L159) | see F11 |
| `blocked_diagnostiqueur.md`, `## Decision` filled | agent applies, recounts | see F11 |

### 4.2 Loops — F11

Phase 1 is a fan-out; a block in one call "does not stop the others"
(L71–73). Phase 2 counts reports against `bug-list.md` and blocks if one
is missing (L160–161). Both terminate.

The re-run is where it breaks. After a phase-2 block on a missing
`G03`:

1. The PO fills `investigation/blocked_G03.md`. `/diagnostique` again:
   phase 1 re-runs G03 (report written); phase 2 invokes the agent;
   `diagnostiqueur.md` L148–160: `blocked_diagnostiqueur.md` with
   `## Decision` empty → "**Stop.** Nothing changed". Phase 2 never
   runs again unless the PO also writes a decision into a file whose
   own rule says "the decision does not replace what is missing… a
   missing report is fixed by re-running its investigation, not by a
   decision" (L178–188). The command's relay (L160–165) tells the PO
   to re-run the investigation and nothing about the second file.
   **TO FIX**: either the command retires `blocked_diagnostiqueur.md`
   when every report exists, or the agent's resume rule says "empty
   decision, but every report now present → assemble".
2. If she writes one anyway: the agent "applies it, then renames it
   with `-NN` appended" (L160) — its tools are `Read, Grep, Glob,
   Write` (L4): no Edit, no Bash, no rename, no delete. The file stays
   at the unnumbered name with a filled decision; the next run applies
   it again. Same for `investigation/blocked_<id>.md` at phase 1.
   **TO FIX** (same family as F4; the command has Bash and could
   rename on the agent's report, as `/7_lots` does for the Cadreur).

---

## 5. `/deploie`

No loop. States:

| State | Outcome | Written at |
|---|---|---|
| a device missing | stop, say which, install nothing | L27–29 |
| both present | phone, then watch, then clear the variable | L33–52 |
| phone build fails | "the report says what failed and stops there" (L61–62) — so the watch is not installed, and the PO is left with an old phone build against… the old watch build. Fine. But if the **watch** install fails after the phone succeeded, the state is the one L27–29 wanted to avoid ("a phone updated against an old watch build"), and the report is the only trace | **NOTE** — say it in the report |
| `adb` absent / not on PATH | no outcome | **NOTE** |
| two phones | "identify by model, never by position" — two of the same model has no rule | **NOTE** |

**Tool vs. gesture**: `allowed-tools: Bash` (L3); the commands are
PowerShell (`$env:ANDROID_SERIAL = …`, `Remove-Item Env:\…`, `.\gradlew`,
L38–44) and L35 says "In PowerShell the variable goes on its own
line". The Bash tool here is Git Bash; `$env:X = "y"` is a syntax error
there. Either the allowed tool is `PowerShell` or the lines are
`ANDROID_SERIAL=… ./gradlew …`. **TO FIX** — unless `allowed-tools:
Bash` maps to the PowerShell tool in this harness, in which case say
so; I cannot settle it from the files.

---

## 6. `/audit_blocages`

No loop; append-only; each pass reads what earlier passes did not. Terminates by construction. Findings:

- L26–33: reads `code/**/blocked_*-NN.md` and unnumbered
  `code/**/blocked_*.md`. `blocked_architecte-NN.md` sits at the working
  folder's **root** (`architecte.md` L199), and `blocked_diagnostiqueur`
  / `investigation/blocked_<id>` outside `code/` too. The glob misses
  them. **NOTE** — the audit is "what the blocks say"; if those blocks
  count, widen the glob.
- L98–101, finding 3's owner list — Cadreur, Vérificateur, Détailleur,
  Réalisateur, Relecteur — omits the concepteur and the testeur, whose
  blocks now exist in the same folders. **TO FIX** (count of agents,
  again).
- L86–88 "blocks settled before the Arbitre existed carry no such
  citation — say so once": no way to tell them apart on disk (no date,
  no author line in the block shape). The auditor will guess. **NOTE**.
- With F4, every lot-level block that was answered by a decision stays
  unnumbered → the audit lists it under *Still open* on every pass,
  never reads it into `## Files read`, and never audits its decision.
  Fixed by F4.

---

## 7. `/audit_conventions`

No loop; append-only. Findings:

- L48–50: "Absent from both — findings **1, 4 and 6** cannot be made."
  Finding 6 (L131–136) is "a rule already reported, still unchanged"
  and needs no `couverture.md`; finding **7** (L138–146) is "a rule the
  split never meets — no lot's `Anchor` cites the entry `couverture.md`
  traces it to" and does. Should read 1, 4 and 7. **TO FIX**.
- L88–92: "the request file carries [the lot] in its name,
  `architecte/detailleur-lot-04.md`" — `architecte/cadreur.md` carries no
  lot (`cadreur.md` L183), `arbitre-<lot>.md` carries one under another
  prefix. Say what to write for a request with no lot. **NOTE**.
- L40–47 correction cycle: `couverture.md` looked for one level up.
  Consistent with the Architecte (feature folder, inv. 1 and 4).
- L58–59 finding 7 reads `code/decoupage.md` of the working folder —
  on a correction cycle that is the bug-fix split, whose anchors cite
  `desc-bug.md` entries, while `couverture.md` traces to
  `spec-technique.md` entries (L52–56 says as much). Every rule then
  reads as "never met by the split". **TO FIX**: finding 7 is
  feature-cycle only, or reads the feature's `decoupage.md`.

---

## 8. Cross-cutting

- **The rename problem (F4 family).** Every agent file carries the same
  paragraph — "rename it `blocked_<agent>-NN.md`… `git mv`, or the
  equivalent… anything left at the unnumbered name reads as a block
  still standing". Of the agents that resume from a decision:
  `realisateur` (Bash) can; `cadreur` says the command does it, and
  `/7_lots` L96 does; `detailleur`, `relecteur`, `diagnostiqueur`,
  `architecte` (`Read, Grep, Glob, WebSearch, WebFetch, Edit, Write`)
  cannot and no command does it for them; `concepteur` and `testeur`
  have Bash but no rule. The whole record that `/9_controle` phases 5–6
  and `/audit_blocages` read is built from the numbered files. One
  sentence in `/8_code` (and one in `/diagnostique`, one in
  `/7_lots` for `blocked_architecte`) — "when the agent reports it
  applied a decision, `git mv` the file to the next free number" —
  closes the family; `/7_lots` L96 is the model.
- **Who may spawn whom** (`CLAUDE.md` L133–139): Cadreur→Vérificateur,
  Détailleur→Arbitre, Réalisateur→Arbitre, Arbitre→Architecte. Matches
  the frontmatters (`Agent` in `cadreur`, `detailleur`, `realisateur`,
  `arbitre`; absent from `concepteur`, `testeur`, `relecteur`,
  `verificateur`, `architecte`, `controleur`). The Arbitre's wait on
  the PO (L417–437, "every 2 minutes… every 5 minutes… nothing at 20
  minutes") has no timer tool in `Read, Grep, Glob, Edit, Write, Agent`
  (L4) — V1's finding, but it is the one bounded wait the downstream
  loop relies on: with no way to wait, the Arbitre returns at once with
  an empty field, and every product question costs a full stop. **NOTE**
  here, BLOCKING in `agent-arbitre.md` if not already there.
- `CLAUDE.md` L108 lists `verificateur · detailleur · realisateur ·
  relecteur · controleur · arbitre` twice in `subagent_type`; L122–127
  shows `detailleur` invoked with `model="sonnet"` while `8_code.md`
  L248 and the frontmatter say `opus`. **NOTE** (out of scope, seen in
  passing).
- The `/cycle` stop table (L82, row 3) names `blocked_detailleur`,
  `_realisateur`, `_relecteur` and not `_concepteur`, `_testeur`; row 7
  routes `cadreur` or `verificateur` decisions to a `/7_decoupe` that
  does not exist. V2.3's scope; noted for the crossing.

---

## 9. Three scenarios

### 9.1 A lot that passes first time

Feature folder, `sequence.md` clean, `lot-03` first without PASS, in
`block-2` whose sheets are not written.

1. `/8_code <feature>` — commits the folder, `git worktree add
   .claude/worktrees/<feature> HEAD`, enters it. Reads `sequence.md`.
   No `code/lot-03/fiche-executable.md` → **détailleur** (opus) on
   block-2: walks the block, writes every sheet of the block (skipping
   none, none exist), no block. *(4b before it: no `blocked_*.md`.)*
2. **concepteur** (sonnet): declarations, compile, `conception.md`,
   commit. **testeur**: one test per criterion, all red, older green,
   `tests.md`, a line in `code/recette.md` if a criterion is manual —
   **no commit** (F12: the tests are untracked at this point).
   **réalisateur**: bodies, analysis and tests green, technical state,
   `compte-rendu.md`, commit "staging explicitly what belongs to the
   lot" — whether that includes the testeur's untracked files is not
   said; assume yes.
3. Orchestrator computes `git diff --name-only <first commit>..HEAD` —
   has to know the concepteur's commit; within the run it can take
   `HEAD` before step 2 (memory, unwritten). **relecteur**: five
   checks, `verdict.md` with `## Status PASS`, `## Attempts 1` (no
   previous verdict — and L68 forbade looking, F5(a), harmless here),
   `## Cause` empty, `## Symbol divergences` none.
4. Move 4: no FAIL. Move 5: no divergences. Move 6: `stop.md` checked
   from the main checkout — absent. Move 7: glob `architecte/` — a
   request from the Détailleur with an empty verdict → **architecte**
   inv. 3, once. `N` = 1 reached → run ends: `git merge --no-ff`, push,
   `git worktree remove` — succeeds only if the testeur's files were
   committed by the réalisateur (F12).
5. Relay: lot-03 PASS, 1 lot of the block remains.

**Terminates.** Everything on this path is written except the
identification of the lot's first commit and the fate of the testeur's
files.

### 9.2 A lot that fails three times

Same start; `lot-03` has a sheet from the previous scenario's block.

1. Move 2 runs the three agents (first pass, no `conception.md`, no
   F8 issue yet). Relecteur: `FAIL mineur`, `## Attempts 1`, `## Cause
   understanding`.
2. Move 4: fresh **réalisateur** (sonnet) — L109 "with the verdict";
   the template does not pass it, the agent's L472–485 expects it.
   Fixes the point, amends the report, commits. Relecteur (diff from
   first commit): `FAIL mineur` again, `## Attempts 2` — provided it
   read the verdict it replaces (F5(a)). `## Cause reasoning` — or
   `limit of reasoning`, F6: the token is not fixed.
3. Move 4 again: second `reasoning`? The first verdict said
   `understanding`; the orchestrator remembers (not on disk, F6). Not
   twice → sonnet. Suppose the third verdict: `FAIL structurel`,
   `## Attempts 3`, `## Cause reasoning`.
4. Now: three failures (L351) — stop; or three *retries* not yet
   exhausted (L109: attempt 3 was retry 2) — one more, on opus since
   `reasoning` now stands twice (if the orchestrator's memory says so).
   F5(c) decides. Say the run stops at `## Attempts 3`. L351–352: look
   for `stop.md` too. Merge, push, remove worktree. Relay.
5. The PO reads the verdict. What now? Nothing written. Next
   `/8_code`: L60 picks lot-03 again. L41–43 reads `## Attempts 3`,
   `## Status FAIL structurel`. No row says "at the cap on launch →
   stop without invoking". Reading move 4 as a per-run rule, the
   orchestrator runs move 2 — three agents on every lot (F8): the
   concepteur over bodies that exist, the testeur over tests that now
   pass, then a réalisateur, then `## Attempts 4`… Reading L112–116 as
   intended (the count is on disk precisely so a restart does not reset
   it), it stops at once and the sequence is frozen on lot-03 for good:
   no lot after it runs, and the only agent that can change the split
   — the Arbitre — is reached only through a Détailleur's or
   Réalisateur's block, which needs an invocation that the cap forbids.

**Does not terminate cleanly.** The exit exists in one direction (the
run stops) and not in the other (the PO cannot reopen, redirect or skip
the lot by any written gesture). F5(e), F6, F8.

### 9.3 A redécoupage mid-block

`block-2` = `lot-03, lot-04, lot-05`; lot-03 PASS; lot-04 in hand.

1. Move 2: concepteur commits stubs for lot-04; testeur writes red
   tests (uncommitted); réalisateur finds that lot-04 cannot compile
   without a symbol lot-05 produces → `blocked_realisateur.md`, calls
   the **arbitre** (opus).
2. Arbitre: the split is wrong → writes `code/redecoupage.md` (five
   sections; `## Ce qui est déjà codé: lot-01, lot-02, lot-03`), writes
   in `## Decision` "back to the split, see code/redecoupage.md".
3. Réalisateur re-reads: filled + `redecoupage.md` present → `git
   restore` its edits, commits nothing, `git mv` its block to
   `blocked_realisateur-01.md`, stops. The concepteur's stub commit
   stays in the branch; the testeur's red tests stay in the working
   tree, untracked (F12).
4. Orchestrator (L267–279): no `redecoupage-NN.md` on disk → first of
   this run. Deletes `code/lot-04/fiche-executable.md` and
   `code/lot-05/fiche-executable.md` (L295–298); leaves
   `code/lot-04/{conception,tests}.md` (F5(f)). Runs `/7_lots` (L281).
5. `/7_lots`, as written, commits the feature folder and creates
   `.claude/worktrees/<feature>` from the main checkout's `HEAD` —
   collision with the worktree it is already in, and a `HEAD` where
   lot-03's `verdict.md` and code do not exist (F3). Suppose instead
   the orchestrator runs it in place. **cadreur** (opus): dispatch →
   `redecoupage.md` → block C. Reads it and every `redecoupage-NN.md`
   (none). lot-01..03 closed; lot-04, lot-05 re-cut as lot-06, lot-07
   (next free numbers) or kept; writes `## Ce qui revient: rien`,
   `## Ce que j'en fais: rien de récurrent` at the end of
   `redecoupage.md`. Calls **verificateur** (opus): reads `## Ce qui
   est déjà codé`, checks lot-01..03 verdicts say PASS, keeps their
   blocks, orders and groups the rest, `## Defects` empty, "says in its
   report that it can be archived" (L437). Cadreur goes out.
6. `/7_lots` hand-back: clean `sequence.md` → pending requests → stop,
   report. **Nobody renames `redecoupage.md`** (F2). `/7_lots` merges
   its branch (in the nested case, mid-`/8_code`).
7. Back in `/8_code` L286–289: first lot without PASS — lot-04's folder
   still exists (with a FAIL-less but present `conception.md`, and
   `blocked_realisateur-01.md`), but if the Cadreur renumbered, the
   sequence names lot-06. No sheet → **détailleur** on block-3 (or
   wherever lot-06 landed). PART 2 first: looks for
   `blocked_detailleur.md` in every lot of the block — none. Details.
   Then concepteur on lot-06: the branch already holds lot-04's stubs
   with names that may collide with lot-06's signatures (F12).
   Testeur: "every test that was there before passes" — lot-04's red
   tests, if still in the tree, fail → **`blocked_testeur.md`** on
   lot-06 (L167–168), no Arbitre, no resume rule → relay to the PO.
   If the Cadreur kept the number lot-04 instead: the Réalisateur's
   resume table L431 — "a `## Decision` sending the lot back to the
   split → Stop, the split has not been redone" — reads the *numbered*
   `blocked_realisateur-01.md`? No: L419–421 looks for the unnumbered
   file only, which was renamed in step 3, so it carries on. But the
   `## Attempts` of any surviving verdict carries over (F5(f)).
8. Had the block been the **Détailleur's** (a walk that found the split
   wrong): after `/7_lots` the Détailleur is re-invoked (L342), finds
   `blocked_detailleur.md` with the split decision and `redecoupage.md`
   **still there** (F2) → "Stop, the split has not been redone" (L422)
   → `/8_code` L311–312 → `/7_lots` → Cadreur block C on the same file →
   Vérificateur → clean → `/8_code` → Détailleur → stop → … **Infinite.**

**Terminates only by the Réalisateur's path and only if the
orchestrator improvises the archive and the nested git.** On the
Détailleur's path it cycles. F2, F3, F7, F12.

---

## 10. Questions I could not settle from the files

- Does `allowed-tools: Bash` in a command file map to the PowerShell
  tool in this harness? `/deploie` depends on the answer.
- Is `git diff --name-only <first commit>..HEAD` meant to be computed
  from memory within a run (the `HEAD` before the concepteur ran)? If
  so, say it and say what a restarted run does.
- Is the "one state" in which `/7_lots` "produces no split" (L48) the
  empty-decision block, or a clean `sequence.md`? The Cadreur's dispatch
  re-cuts on the latter.
- Was `/9_controle` meant to run after a correction cycle at all?
  `8_code.md` L190–193 and `9_controle.md` L45 disagree, and `fusion.md`
  L64–69 expects the correction cycle's `decisions-produit.md` to exist.
