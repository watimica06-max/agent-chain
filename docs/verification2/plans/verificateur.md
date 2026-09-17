# Plan — `verificateur.md`

Base: `.claude-new/agents/verificateur.md` (517 lines) as read on
2026-09-17. Short names below: `verificateur.md`, `cadreur.md`,
`arbitre.md`, `diagnostiqueur.md`, `architecte.md`, `relecteur.md` are
`.claude-new/agents/…`; `7_lots.md`, `cycle.md` are
`.claude-new/commands/…`; `passes/verificateur.md` and
`modifications.md` are `docs/refonte/…`.

Read: the agent file; `7_lots.md` and `cycle.md` (the only two
commands naming it); `docs/verification2/verificateur.md` (both parts);
`docs/verification2/decisions.md`; the six thematic reports filtered on
`verificateur`; and, for every two-file `Where`, the cited lines of the
other file.

Three decisions below pull several findings together, so they are
stated once and referenced:

- **The layer of a section is matched on what the section is about**
  (`decisions.md` F19) — no conventions read remains. Closes F19,
  and with it F05 and F08.
- **The block ceiling counts lots.** Closes F01, F06, F17.
- **The `## Status` read of coded lots goes.** Closes F11, one quarter
  of F04, and the Vérificateur's share of `passages-aval.md` F15.

---

## `verificateur.md` — the report's findings

### verificateur.md F01 — C17 applied as lots where the sheet asked entries

Verdict: confirmed
Decision: Keep lots as the unit — it is what the index records as the
applied correction and what the table's numbers were set against — and
remove every sentence that says entries (see F06).
Where: `passes/verificateur.md` L477-478 ↔ `verificateur.md` L485, L494
Cited: `passes/verificateur.md` L477-478 — "One number per layer,
counting entries cited, and the table's header says so."
Cited: `modifications.md` L1007 — "Le Vérificateur compte les lots par
bloc ; le Cadreur compte les symboles d'un lot"
Owner: verificateur
Also in: cadreur (F17)

📌 The pass sheet's stated defect was the duplication ("lots versus
entries", L466-467), not the unit; the index chose lots, gave its reason
(L494-495: a block is what the Détailleur holds, and it holds lots), and
nothing since reopened it.

### verificateur.md F02 — C3, C4, C5 placed under `What you read`

Verdict: confirmed
Decision: Add the inventory to the Role path table (L39-43) with the
file that carries it; move the coded-lot rules (L66-84) into the moves
they govern, one rule per move.
Where: `passes/verificateur.md` L115-117, L137-138, L170 ↔
`verificateur.md` L39-43, L66-87
Cited: `passes/verificateur.md` L115-117 — "The inventory is named with
the file that carries it, in the path table of the Role section
alongside the lot list and the sequence."
Cited: `passes/verificateur.md` L170 — "The rule lives where the check
is, not in the reading list."
Owner: verificateur
Also in: —

📌 L69-73 (the `## Status` read) is not moved: it goes (F11).

### verificateur.md F03 — C20: the fresh-context rule three times, commentary at L287-288

Verdict: confirmed
Decision: State the fresh-context rule once, in *Who invokes you*
(L243-249), keep the one never-do line (L230-231), drop L24-25's
sentence and the clause "and on a new application most needs look like
that" at L287-288.
Where: `passes/verificateur.md` L558-561 ↔ `verificateur.md` L24-25,
L230-231, L243-249, L287-288
Cited: `passes/verificateur.md` L558-560 — "The fresh-context rule
stated once, where the rounds are introduced, with one line in 'What
you never do'. The commentary sentences go"
Owner: verificateur
Also in: —

### verificateur.md F04 — four partial reads name no tool

Verdict: confirmed
Decision: Name the gesture and its bound for each partial read that
remains — the preamble (L57), `## Ce qui est déjà codé` (L66-67), the
previous sequence's sections (L444-445) — on the pattern L61-62 already
uses for the entry titles.
Where: `verificateur.md` L4 ↔ `verificateur.md` L57, L66-67, L444-445
Owner: verificateur
Also in: —

📌 The fourth read, `## Status` (L69), goes with F11. ⚠️ A whole Read of
the technical document opens entries no lot cites, which L96-97
forbids — the preamble read is the one that costs most without a bound.

### verificateur.md F05 — `docs/TECHNICAL_CONVENTIONS.md` under the working-folder rule

Verdict: confirmed
Decision: Resolved by F19 — the conventions read goes, and the path
with it; align L36's example (`docs/features/…`) with L27-28 so the file
carries one path rule.
Where: `verificateur.md` L27-28, L36 ↔ `verificateur.md` L93
Cited: `cadreur.md` L50-52 — "A path starting with `docs/` is relative
to the repository root, not to the working folder — the conventions
are shared by the whole project." *(the rule the file would need if
the read stayed)*
Owner: verificateur
Also in: —

### verificateur.md F06 — the ceiling counts entries at L453 and L466, lots at L485 and L494

Verdict: confirmed
Decision: Lots (F01) — rewrite L453-454 and L465-467 to say lots;
L485 and L494-495 stand.
Where: `verificateur.md` L453-454, L465-467 ↔ `verificateur.md` L485,
L494-495
Owner: verificateur
Also in: cadreur (F17)

### verificateur.md F07 — the preamble read "always" and "there is none" on a bug-fix

Verdict: confirmed
Decision: The preamble is read on both documents; say that on
`desc-bug.md` it carries `Dependencies` and no `Vocabulary` (see F18),
and that the naming reference there is the feature's own terms as the
entries and bearers name them.
Where: `verificateur.md` L57-59 ↔ `verificateur.md` L394-395
Owner: verificateur
Also in: —

### verificateur.md F08 — the layer needed at move 4, read only at move 5

Verdict: confirmed
Decision: Resolved by F19 — no conventions read remains; the layer is
matched on the section's subject, available at move 4 and move 5
alike; L92-94 keeps only the previous `code/sequence.md`.
Where: `verificateur.md` L92-94 ↔ `verificateur.md` L428-429
Owner: verificateur
Also in: —

### verificateur.md F09 — the bearer's layer has no input on a bug-fix

Verdict: confirmed
Decision: On a bug-fix cycle the lot list states each lot's layer — the
bearer's, which the Cadreur establishes from the code (`cadreur.md`
L77-78) — and the Vérificateur reads it there at moves 4 and 5.
Where: `verificateur.md` L432-434, L503-504 ↔ `verificateur.md` L89-94
Cited: `cadreur.md` L77-78 — "on a `desc-bug.md` — the unit is the
bearer, and a lot's layer is the bearer's, whatever sections its
entries come from."
Owner: cadreur
Follows: verificateur (L432-434, L503-504 name the source)
Also in: cadreur

📌 The Cadreur chooses where it sits. ⚠️ The lot's five fields are what
every downstream reader keys on (`passages-aval.md` L21); the bearer's
line in `## Symbols`, read by the Cadreur and the Vérificateur alone,
is the place that changes no other reader.

### verificateur.md F10 — "in the order they ran" comes from nowhere

Verdict: confirmed
Decision: The previous `code/sequence.md` is read for its `## Order`
as well as its `## Blocks` (L444-445); coded lots keep the relative
order they hold there.
Where: `verificateur.md` L82 ↔ `verificateur.md` L444-445
Cited: `arbitre.md` L346-348 — "## Ce qui est déjà codé — <every lot
whose verdict.md carries PASS>" *(a list; no order stated)*
Owner: verificateur
Also in: —

### verificateur.md F11 — a coded lot without PASS typed `surface`

Verdict: confirmed
Decision: Drop the `## Status` read and the `surface` line (L69-73):
the coded set is the Arbitre's list as written, and the Cadreur checks
PASS on its own side.
Where: `verificateur.md` L72 ↔ `verificateur.md` L141
Cited: `arbitre.md` L348 — "<every lot whose verdict.md carries PASS>"
Cited: `cadreur.md` L877-878 — "A lot whose `code/<lot>/verdict.md`
carries PASS is closed."
Owner: verificateur
Also in: —

⚠️ Kept as a defect, the line burns rounds: the Cadreur has no
correction for it (the lot list marks nothing as coded), so the
Vérificateur would raise it again, up to the third round and a
`blocked_cadreur.md`. 📌 The pass sheet's C4 allowed "or the read goes"
(`passes/verificateur.md` L137).

### verificateur.md F12 — three headings announced, a fourth written

Verdict: confirmed
Decision: Announce `## Redécoupage: archivable` in *What you write*
(L105-122) as the conditional fourth heading, with the condition move 6
states.
Where: `verificateur.md` L105 ↔ `verificateur.md` L469-470
Owner: verificateur
Also in: — (`renommages.md` F12 is the same finding, below)

### verificateur.md F13 — `surface` has no test the lot fields can run

Verdict: confirmed
Decision: State the test — an operation is covered when a lot names
its symbol in `Produces` or `Modifies` **and** cites an entry the
inventory lists against that operation; uncovered otherwise.
Where: `verificateur.md` L272-273 ↔ `cadreur.md` L753-754
Cited: `cadreur.md` L753-754 — "`Needs`, `Produces` and `Modifies`
carry symbols, and symbols only."
Cited: `cadreur.md` L734 — "One line per thing asked of it, with the
entries that ask."
Owner: verificateur
Also in: —

📌 The inventory already carries what the test needs (L721-732: each
operation with its entries). No change on the Cadreur's side.

### verificateur.md F14 — the cascade-caller exemption from `overlap`

Verdict: confirmed
Decision: Delete the exemption at L300-302 — two lots naming one
symbol in `Produces` or `Modifies` is an `overlap` whatever the reason,
as the Cadreur's own rule says.
Where: `verificateur.md` L300-302 ↔ `cadreur.md` L573
Cited: `cadreur.md` L573 — "Another lot modifies it for its own reasons
| A defect — two lots would touch one symbol; re-cut"
Owner: verificateur
Also in: —

### verificateur.md F15 — the Cadreur keys on a `## Decision` the file never carries

Verdict: confirmed
Decision: The Cadreur's first return row keys on the presence of
`code/blocked_verificateur.md`, nothing more; the file's shape (L191-207)
stands.
Where: `verificateur.md` L206 ↔ `cadreur.md` L818
Cited: `cadreur.md` L818 — "A `code/blocked_verificateur.md` with an
empty `## Decision` | Go out without correcting"
Owner: cadreur
Also in: cadreur (`fichiers.md` F08, `passages-aval.md` F03)

### verificateur.md F16 — nothing archives `code/sequence-NN.md`

Verdict: confirmed
Decision: The Cadreur archives the round's `code/sequence.md` as
`code/sequence-NN.md` (a copy, by Read and Write — three short
headings) before it calls the Vérificateur again; the Vérificateur
keeps writing over `code/sequence.md`, and its L444-445 read of the
previous round is unchanged.
Where: `verificateur.md` L444-445 ↔ `cadreur.md` L822-823
Cited: `cadreur.md` L822-823 — "The count is the number of archived
`code/sequence-NN.md` files plus the round you are in"
Cited: `cadreur.md` L40 — the only other mention of `code/sequence-*.md`
in `.claude-new/`; `7_lots.md` L103 and L146 rename `redecoupage.md` and
`blocked_cadreur.md` only.
Owner: cadreur
Also in: cadreur (`chemins-aval.md` F19, `passages-aval.md` F04)

⚠️ For the Cadreur's plan: the archive accumulates across redécoupages,
so a count on every `sequence-*.md` file would reach three on a later
split's first round — the count has to be bounded to the current split.

### verificateur.md F17 — the Cadreur says the Vérificateur counts entries

Verdict: confirmed
Decision: Lots (F01) — rewrite `cadreur.md` L106-107 to say lots per
block.
Where: `verificateur.md` L494 ↔ `cadreur.md` L106-107
Cited: `cadreur.md` L106-107 — "but it counts something else: entries
cited per block, not symbols per lot."
Owner: verificateur
Follows: cadreur
Also in: cadreur

### verificateur.md F18 — `desc-bug.md` carries a preamble, without `Vocabulary`

Verdict: confirmed
Decision: With F07 — L394-395 says the preamble is there, carries
`Dependencies` and no `Vocabulary`; L58 no longer promises a
`Vocabulary` on both documents.
Where: `verificateur.md` L58, L394-395 ↔ `diagnostiqueur.md` L508-512
Cited: `diagnostiqueur.md` L508-512 — "## Preamble / Intent: correcting
the gaps reported on <feature>. / Out of scope: everything not listed
below. / Dependencies: the whole feature, already built."
Owner: verificateur
Also in: —

### verificateur.md F19 — six layers against twelve sections

Verdict: confirmed
Decision: Apply `decisions.md` F19 — the Vérificateur matches each
section of the technical document to a layer on what the section is
about, never on a title; no match takes the default row and the report
says which section did; the conventions read (L92-94, L497-498) goes.
Where: `verificateur.md` L497-498 ↔ `architecte.md` L110-112
Cited: `architecte.md` L110-112 — "twelve numbered sections, in the
grid's order — titles and framing lines are in the grid"
Cited: `decisions.md` L169-172 — "Match on what the section is about,
never on its title. No match, the default row — and the agent says so"
Owner: verificateur
Also in: —

📌 The pass sheet offered this route itself (`passes/verificateur.md`
L480-482: "or the ceilings are keyed on the sections as the technical
document names them, which removes the mapping").

### verificateur.md F20 — the command counts blocks from headings

Verdict: confirmed
Decision: `7_lots.md` counts the `block-N:` lines under `## Blocks`.
Where: `verificateur.md` L111-114 ↔ `7_lots.md` L31-32
Cited: `7_lots.md` L31-32 — "its `## Defects` section, to know whether
the split holds, and its headings, to count the blocks."
Owner: 7_lots
Also in: —

### verificateur.md F21 — two relay rules for one file in `7_lots.md`

Verdict: confirmed
Decision: The general relay rule (`7_lots.md` L247-249) excepts
`blocked_verificateur.md` the way L251-253 already excepts the
Architecte case — row L147 is the rule for it.
Where: `verificateur.md` L206 ↔ `7_lots.md` L147, L247-249
Cited: `7_lots.md` L247-249 — "If an agent returns a `blocked_*.md`:
relay it and stop, naming the file. The Product Owner fills
`## Decision`, and the Cadreur reads it on its next run."
Owner: 7_lots
Also in: —

### verificateur.md F22 — `cycle.md` resumes a Vérificateur block through `/7_decoupe`

Verdict: confirmed
Decision: Settled by `decisions.md` (`cadreur.md` F23, `fichiers.md`
F09) — `cycle.md` is deleted and the row goes with it; the Vérificateur
changes nothing.
Where: `verificateur.md` L206 ↔ `cycle.md` L88
Cited: `cycle.md` L88 — "`cadreur` or `verificateur` → `/7_decoupe`"
Cited: `decisions.md` L26-30 — "`cycle.md` is deleted … Remove every
mention of `/cycle` and `cycle.md` wherever you meet one."
Owner: commandes
Also in: cadreur, commandes

⚠️ `cycle.md` is still on disk in `.claude-new/commands/` at the time
of writing; the deletion is the decision, not yet a fact.

### verificateur.md F23 — the ceiling remark reaches nobody

Verdict: confirmed
Decision: Carry it — the Cadreur relays the remark as it relays the
archivable line, and `7_lots.md` relays it with lots, blocks and
defects.
Where: `verificateur.md` L462-463 ↔ `cadreur.md` L926-927,
`7_lots.md` L242-243
Cited: `cadreur.md` L926-927 — "And relay the Vérificateur's
`## Redécoupage: archivable` line, when it wrote one"
Cited: `7_lots.md` L242-243 — "how many lots, how many blocks, and any
defect left. Nothing else is yours"
Owner: verificateur
Follows: cadreur, 7_lots
Also in: cadreur

📌 The remark is the only signal for calibrating ceilings "no cycle has
been run against" (L461-462); dropping it is the cheaper fix, and loses
that.

### verificateur.md F24 — the both-ends case arrives declared as a need

Verdict: confirmed
Decision: Move 2's second kind is read from the need the Cadreur
declares on the lot that removes the call, not derived; L336 and
L354-361 say so, and the `merge` on "neither order works" is raised
only when the anchors show it (the Vérificateur reads no code).
Where: `verificateur.md` L336, L354-361 ↔ `cadreur.md` L572
Cited: `cadreur.md` L572 — "Another lot removes the call as part of its
own change | Declare a need on that lot — it has to run first, and
nothing else would order them"
Owner: verificateur
Also in: —

---

## The thematic reports, filtered on `verificateur`

### renommages.md F12 — three headings announced, a fourth written

Verdict: confirmed
Decision: Same as `verificateur.md` F12.
Where: `verificateur.md` L104-105 ↔ `verificateur.md` L469
Owner: verificateur
Also in: —

### renommages.md F13 — the rename keyed on the Cadreur's report alone

Verdict: confirmed
Decision: `7_lots.md` keys the rename on the `## Redécoupage:
archivable` line in `code/sequence.md`, a file it already opens
(L31-32); the Cadreur's relay stays as a courtesy, and `verificateur.md`
L473-475 already describes that.
Where: `7_lots.md` L100-103 ↔ `verificateur.md` L472-475
Cited: `7_lots.md` L100-101 — "The Cadreur reports the split holds and
`code/redecoupage.md` can be archived → rename it yourself"
Owner: 7_lots
Also in: —

### fichiers.md F08 — the Cadreur's row against a file `git rm`'d and without `## Decision`

Verdict: confirmed
Decision: Same as `verificateur.md` F15 — presence alone. 📌 With the
heading test gone, the row matches first, and the Cadreur no longer
reads a stale `code/sequence.md` as the round's result.
Where: `cadreur.md` L818 ↔ `7_lots.md` L79, `verificateur.md` L206
Cited: `7_lots.md` L79 — "First, remove `code/blocked_verificateur.md`
if it is there — `git rm`."
Owner: cadreur
Also in: cadreur

### fichiers.md F09 — resuming a Vérificateur block through `/cycle`

Verdict: confirmed
Decision: Settled by `decisions.md` — moot, `cycle.md` is deleted
(same as `verificateur.md` F22).
Where: `cycle.md` L88 ↔ `verificateur.md` L206
Owner: commandes
Also in: commandes

### chemins-aval.md F19 — the round count on files nothing archives

Verdict: confirmed
Decision: Same as `verificateur.md` F16.
Where: `cadreur.md` L822 ↔ `verificateur.md` L444
Owner: cadreur
Also in: cadreur

### passages-aval.md F03 — the file that comes back matches no row

Verdict: confirmed
Decision: Same as `verificateur.md` F15.
Where: `cadreur.md` L818 ↔ `verificateur.md` L206-208
Owner: cadreur
Also in: cadreur

### passages-aval.md F04 — the three-round cap never reached from cold

Verdict: confirmed
Decision: Same as `verificateur.md` F16.
Where: `cadreur.md` L822-823 ↔ `verificateur.md` L105, `7_lots.md`
L101-103
Owner: cadreur
Also in: cadreur

### passages-aval.md F15 — `PASS with reservation` against "carries PASS"

Verdict: confirmed
Decision: Settled by `decisions.md` — every reader matches the `PASS`
prefix. For the Vérificateur it is moot once the `## Status` read goes
(F11); should that read stay, L70 says prefix.
Where: `relecteur.md` L110 ↔ `verificateur.md` L70
Cited: `relecteur.md` L110 — "**PASS with reservation** | A point
passes, but is worth noting for what follows"
Owner: relecteur
Follows: verificateur (only if L70 stays)
Also in: relecteur, detailleur, 8_code, 9_controle

### Not this agent's

- **`chemins-aval.md` F12** — names `diagnostique.md` and
  `diagnostiqueur.md`; `7_lots.md` L79's removal of
  `blocked_verificateur.md` is cited as the model to copy, and nothing
  in `verificateur.md` changes. Lands in the Diagnostiqueur's plan.
- The `Sound:` lines of `chemins-aval.md` L31-32 and
  `passages-aval.md` L21 name the agent and raise nothing.

---

## The report's second part — corrections still `open` or `other`

📌 Every one of them is carried by an entry above; none gets an entry
of its own.

| Status line | Carried by |
|---|---|
| C3 open · C4 other · C5 other | F02 (C4's read goes with F11) |
| C6 other — move 3's "badly cut" check carries no type | ⚠️ **Not in the report's findings.** L385-387 is the `anchor` kind (L147: "A lot's entries do not describe what it announces"); the word is stated at L147 and not repeated at L385-387. Owner: verificateur — name the type there, with F02's move rewrite. |
| C17 fixed · B.7 other | F01, F06 |
| C20 other · Q4 other | F03 |
| C23 open | ⚠️ The report's first part lists C23 among "found sound" (L30) and its second part lists it `open` (L45). `7_lots.md` L142 and L147 carry the two rows C23 asked for; what remains is the general relay rule — F21. |
| C25 open | F22 — `cycle.md` deleted |
| Q5 open | F07, F18, F19 |

---

## To settle

— Nothing. Every finding above turns on mechanics the files already
record: the unit of the ceiling on `modifications.md` L1007, the layer
matching on `decisions.md` F19, the `cycle.md` rows on `decisions.md`
`cadreur.md` F23. ⚠️ Two decisions reverse a refonte placement rather
than a wording, and are flagged where they sit: F11 (the `## Status`
read goes — C4 allowed it) and F19 (the conventions read goes — C17
offered it).
