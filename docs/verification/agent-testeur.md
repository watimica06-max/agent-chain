# Vérification — `testeur.md`

**Inputs**

| | |
|---|---|
| Old | `.claude/agents/testeur.md` — **does not exist**. New agent (🆕 in `modifications.md`) |
| New | `.claude-new/agents/testeur.md` — 217 lines |
| Pass file | `docs/refonte/passes/testeur.md` — **does not exist** |
| `modifications.md` | section `# 🆕 testeur.md`, lines 889–938 — a table *Ce qu'il porte* and *La demande*; **no pass sheet** (no Passés / Écartés / Reportés lines) |

Line numbers below are those of the new file unless stated otherwise.

---

## A. Conformity

**Skipped — no pass file and no pass sheet.** There is no PASSÉ, ÉCARTÉ or
REPORTÉ defect to verify. What can be verified is the file against its
own spec; that is done at the top of B.

---

## B. The file against its spec

### B.1 — What *La demande* and the *Ce qu'il porte* table ask, and where it lands

| Asked (modifications.md) | Found (new file) | Verdict |
|---|---|---|
| Per lot, after the Concepteur and before the Codeur | l.3, l.32-33 "One invocation per lot, between the concepteur and the realisateur" | ✅ |
| One test per acceptance criterion, from the sheet and the interface files | l.16, l.58-64 (sheet `## Acceptance criteria`, `## Signatures`, the declarations), l.145 | ✅ |
| It cannot see the bodies — they do not exist yet | l.19-21 | ✅ |
| Each new test fails, the older ones pass | l.156-162, table of move 4 | ✅ |
| What red proves; a test passing on empty bodies asserts nothing; observed case | l.23-26, l.161 | ✅ |
| A passing new test is rewritten (table row) | l.164-165 | ✅ |
| An older test failing is a block, the Concepteur broke something (table row) | l.167-168 | ✅ — but see D.2 and D.3 |
| Why him: a test written against a body asserts what the body does (table row) | l.28-30 | ✅ |
| Recette: one line per behaviour no test can exercise — pure rendering, system dialog, sensor | l.139-140 (adds "a permission the platform grants"), l.170-173 | ✅ — the file says "per criterion" like the table, not "per behaviour" like *La demande* |
| What to look at, in the PO's words; not « vérifier B12 » | l.175-179 | ✅ |
| Each line names the state; otherwise the list cannot be ordered (table row, A4) | l.181-184 | ✅ — consistent with `9_controle.md` l.184-185 |
| He is the only one who knows why: he just tried | l.142-143 | ✅ |
| Written before coding, so the list exists even if a lot fails | Not stated as a rationale; guaranteed by the order (move 5 precedes the realisateur) | ✅ NOTE — the rationale is not in the file, no fix needed |
| Blocks on a criterion no test and no manual line can carry, never on a merely hard one (table row) | l.115-121 | ✅ — but see D.1 |
| Report `code/<lot>/tests.md`; every criterion in `## Tests` or `## Criteria with no test` (table row) | l.193-217 | ✅ |

Nothing the spec asks is missing. One wording drift only: *La demande*
says « une ligne par **comportement** », the table and the file say
"per **criterion**" — the table is the later formulation and the file
follows it.

### B.2 — What the file carries that neither the table nor *La demande* announces

Nothing here contradicts the spec; each item is listed so it has been
read once critically.

| Lines | Quote (abridged) | What it adds |
|---|---|---|
| l.4 | `tools: Read, Grep, Glob, Edit, Write, Bash` | Not in the spec; `Bash` is implied by "run the tests" |
| l.35-52 | path rules + file table (`fiche-executable.md`, `conception.md`, `tests.md`, `recette.md`) | Same pattern as `concepteur.md` l.31-47; all four paths match the files other agents name |
| l.56-72 | "What you read … Nothing else … You never read another lot's tests" | A closed reading list — see D.4 |
| l.76-89 | "What you never do" — no production code, no change of a declaration, never weaken a test, assert outcome not shape, one test one criterion, write in four places only | Guard rails not in the spec; coherent with the realisateur ("never touch a test", realisateur l.24) |
| l.93-121 | blocking file shape, four headings | Same shape as `concepteur.md` l.93-109, with `## Where` = "the criterion, and the sheet line" — see D.2 |
| l.133-143 | move-2 decision table, definition of *no* | The testable/not-testable rule — see D.1 |
| l.147-149 | "Named for what it asserts … the Relecteur pairs a test to a criterion on what the test asserts" | Consistent with `relecteur.md` l.328 |
| l.151-152 | "A test asserting two criteria leaves one of them unverifiable" | Not in spec |
| l.154 | "Call the declarations as the conception report places them" | Ties to `conception.md` `## Declared` |
| l.172-173 | `recette.md` "appended, never rewritten" | Not in spec — see D.7 |
| l.186-187 | "Nothing to add is a normal outcome — you write nothing" | Not in spec |
| l.208-210 | `## Outside the lot` in `tests.md` | Not in spec — see D.6 |
| l.212-213 | "`## Red` is what the realisateur and the Relecteur take as given — neither runs the tests again before writing" | Consistent with `realisateur.md` l.74-75 |

---

## C. Gestures against tools

Frontmatter tools: **Read, Grep, Glob, Edit, Write, Bash**.

| Gesture | Lines | Tool | Verdict |
|---|---|---|---|
| Read the sheet, `conception.md`, the declarations, the conventions | l.58-66 | Read | ✅ |
| Locate the file each declaration landed in | l.61-62, l.154 | Read of `conception.md` `## Declared` suffices | ✅ |
| Find "the rules the sheet names" (§n) in the conventions | l.65-66 | Grep, plausibly | ✅ |
| Write a new test file | l.145 | Write | ✅ |
| Add a test to an existing test file | l.145 | Edit — requires a prior Read of that file | ⚠️ collides with l.71 "You never read another lot's tests" — see D.4 |
| Run the tests | l.156 | Bash | ✅ tool present — ❌ **no command named, no scope**: the concepteur says "by the command the conventions name" (concepteur l.158-159), the realisateur lists exactly what its Bash may run (realisateur l.570-575). The testeur reads the conventions for "the rules marked `permanente`, and those the sheet names" (l.65-66) — nothing says the test command is among them. **TO FIX** — say where the command comes from, and bound `Bash` to it |
| Write `tests.md`, write `blocked_testeur.md` | l.95, l.194 | Write | ✅ |
| Append a line to `code/recette.md` | l.170-173 | Edit (Write when the file does not exist yet — unstated, see D.7) | ✅ |
| **Commit** | — | Bash present, **no gesture** | ❓ **Question** — the concepteur commits (concepteur l.170), the realisateur commits (realisateur l.568); the testeur has no move that commits its tests. They reach git only if the realisateur stages them — nothing in either file says so — and `8_code.md` l.95-96 builds the Relecteur's file list from "`git diff --name-only` between the lot's first commit and `HEAD`", which does not see an uncommitted test. Is the omission intended? |

**Tools no gesture uses**: `Grep` and `Glob` — no move names a search or
a listing. Harmless; NOTE.

---

## D. Internal coherence

### D.1 — l.115-117 vs l.138-140 · one phrase, two senses · **TO FIX**

> l.115-117 — "You block on a criterion you cannot turn into a test at all — one whose outcome is **not observable from outside the code**, and that no manual line can carry either."
>
> l.138-140 — "The test is *no* only when the outcome **cannot be observed from outside the running code** — a pure rendering, a system dialog, a sensor reading, a permission the platform grants."

The same phrase names the manual-list case in move 2 and the block case
in "When you cannot produce". Only the trailing clause "and that no
manual line can carry" separates them, and the block case has no
example — a rendering is not observable by a test yet is observable by
the Product Owner. As written, an agent reading l.116 alone would block
on exactly what l.139 sends to the manual list. Give the block case its
own wording and one example.

### D.2 — l.167-168 vs l.99-121 · a block the blocking section does not know · **TO FIX**

> l.167-168 — "One of the older ones fails — that is a block: the concepteur's declarations broke something that was working."
>
> l.115 — "You block on a criterion you cannot turn into a test at all" — the only block reason stated.
>
> l.103-105 — `## Where` — "<the criterion, and the sheet line that gives it>"

A regression block names no criterion and no sheet line: it fits neither
the stated reason nor the shape. Add the regression to the block
reasons, and let `## Where` carry "the test that fails, and the
declaration that broke it".

### D.3 — l.167-168 · a branch with no exit · ❓ question

The older test's failure is attributed categorically to the concepteur.
A lot that **modifies** an existing signature — the case the Relecteur
names, "On a modification, existence proves nothing — only the signature
says whether the lot did its work" (relecteur l.320-321) — breaks the
older tests that call the old signature, and that is the sheet doing its
work, not the concepteur breaking something. The testeur blocks (l.167),
the realisateur "never touches a test" (realisateur l.24). Who adapts an
older test a legitimate signature change made false? Is that always a
Product Owner decision?

### D.4 — l.71-72 vs l.145 + Edit · "read" in two senses · **TO FIX**

> l.71-72 — "You never read another lot's tests — what they assert is not your criterion."

When a previous lot's tests live in the file the new test belongs in
(same unit under test), adding a test means opening that file — `Edit`
requires a prior `Read`. Either "read" means "take as input for your
assertions", and the rule should say so, or the testeur must always
create a new file, and the rule should say that.

### D.5 — l.95 + `8_code.md` l.213-217 · the block branch leads nowhere on re-entry · 🔴 **BLOCKING**

> l.95 — "Write `code/<lot>/blocked_testeur.md` — do not merely say it."

The file has **no rule for a blocking file whose `## Decision` has been
filled**. The concepteur has one ("A blocking file the prompt names
carries a filled `## Decision` — apply it and carry on", concepteur
l.118-119); the realisateur and the relecteur apply it and rename it
numbered. `8_code.md` l.213-217 re-invokes the testeur with the same
prompt — "Working folder … Your lot" — and stops only on an *empty*
decision (8_code l.123-126). A re-run therefore meets the same criterion
with no instruction to look for the decision, and l.95 makes it **write
`blocked_testeur.md` again — over the one the Product Owner filled**. A
lot blocked once by the testeur cannot be unblocked through this file.

Same gap, smaller: nothing says what happens to the tests already
written when the block occurs (kept? `tests.md` written partially?), nor
what a re-run does with them — there is no `Reprise` as the realisateur
has (realisateur l.318-331).

### D.6 — l.208-210 · `## Outside the lot` rests on a field the sheet does not have · ❓ question

> l.208-210 — "`## Outside the lot` — <every file you touched that the sheet does not declare, or a dash>"

The sheet has five fields — `## Signatures`, `## Acceptance criteria`,
`## Dependencies`, `## Conventions`, `## Requests` (detailleur
l.229-258) — and **declares no file**. Read literally, every test file
the testeur creates is "outside the lot"; read loosely, none is. Does
`code/recette.md` count? The Relecteur checks `## Outside the lot`
against the diff (relecteur l.373-375), so the answer changes what it
finds. (The concepteur has the same problem, l.141 "the sheet's
`Modifies` or `Touches`" — fields the sheet does not carry; noted here
only because the testeur inherits it.)

### D.7 — l.170-173 · "at the split's root", and the first lot · NOTE

> l.170 — "Write the manual list, `code/recette.md`, at the split's root."

"Split" is not a term the file defines — it says "working folder"
everywhere else — and `code/recette.md` sits in `code/`, not at a root.
Also, "appended, never rewritten" (l.172-173) does not say that the
first lot of the split creates the file.

### D.8 — l.164-165 · the rewrite loop has one exit only · ❓ question

> l.164-165 — "One of yours passes — rewrite it. It asserts nothing, or it asserts something the empty body already satisfies."

The second cause is named but has no exit. A criterion an empty body
genuinely satisfies — "the list shows nothing when there is no record",
against a body that returns nothing — cannot be made red without
asserting on something beyond the criterion, which l.151 forbids. After
the rewrite still passes: manual list, block, or accept the green test?

### D.9 — l.156 · the test command · **TO FIX** (already in C)

"Run the tests" names no command and `Bash` is unbounded — the only
agent of the loop whose `Bash` is. See C.

### D.10 — Naming and counts · NOTE

- l.127 "Five moves" → moves 1 to 5 ✅. l.97 "four headings" → four ✅.
  Report: four sections, no count announced ✅.
- "Relecteur" is capitalised (l.148, l.212), "realisateur" and
  "concepteur" never are — style only, one sense each.
- l.16-17 "One test per acceptance criterion … it is the whole of your
  work" — the recette (move 5) and the report are also its work;
  rhetorical, no fix needed.
- l.1-6 — no `effort:` line, while its two peers of the loop carry one
  (`realisateur.md` high, `relecteur.md` medium); `concepteur.md` has
  none either. `CLAUDE.md` (new) l.86 says every agent carries both.
  Model `sonnet` matches `8_code.md` l.249-250 and the nine-opus list ✅.

---

## Summary

| Severity | Count | Ids |
|---|---|---|
| BLOCKING | 1 | D.5 — a decided `blocked_testeur.md` is never applied and gets overwritten on re-run |
| TO FIX | 4 | D.1, D.2, D.4, D.9/C (test command and `Bash` scope) |
| Questions | 4 | C (commit), D.3, D.6, D.8 |
| NOTE | 3 | D.7, D.10, B.1 rationale row |

A is empty by construction: no pass file, no pass sheet. The file
carries everything *La demande* and the table ask (B.1). What has never
been read critically is the block branch — D.1, D.2 and D.5 all sit
there.
