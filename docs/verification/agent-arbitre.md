# agent-arbitre — verification

**Read**: `.claude/agents/arbitre.md` (old, 401 lines) · `.claude-new/agents/arbitre.md`
(new, 442 lines) · `docs/refonte/passes/arbitre.md` — **does not exist** (the section says
so: *"pas de fiche de passe, l'analyse ne l'a pas atteint"*) ·
`docs/refonte/modifications.md` § `` # `arbitre.md` `` (lines 1276–1319), plus the U10 rows
of § `` # `detailleur.md` `` (lines 1019–1020, 1051–1066) that the arbitre section cites.

**What the section says**: three rows in "Ce qui a changé" — (1) the four-way sort of what
comes back up, three destinations of which do not go to the Architecte; (2) a new
prohibition: never a rule into `TECHNICAL_CONVENTIONS.md`, its one write outside a
blocking file is a trap; (3) added with U10: it can read a multi-entry blocking file, one
answer per `## Blocking N`, all read before any is settled. "La demande" spells out (1)
only — the sort table, the `## Traps` rationale and the 25/11/18/8 measurement. (2) and (3)
have no demand text beyond their summary row (for (3), the "Cascade" row of the detailleur
section).

Since no pass sheet exists, section A covers the three structural modifications only.
B, C and D are given full attention, as instructed. Line numbers are those of the **new**
file unless marked *old*.

Cross-file facts used below, all read from `.claude-new/` or `docs/`: the Détailleur's
multi-entry shape (`detailleur.md` 478–494) is `## Blocking N — lot-XX` holding `### What
blocks` / `### Where` / `### To resume` as **h3**, then one `## Decision` at the end; its
post-return table (`detailleur.md` 331–335) has three rows — Filled / Filled and back to the
split / Still empty — and no row for a partly filled field; the Réalisateur's blocking file
(`realisateur.md` 233–250) is single-entry; `docs/CURRENT_TECHNICAL_STATE.md` has no
`## Traps` heading — the section is `## Traps — general` (line 1985); the
`technical-state-format` skill says *"Load before writing to that file, never write to it
without"* and routes a trap owned by one subject under that subject's `###`, not under
`## Traps — general`; the Réalisateur carries `Skill` in its tools and loads that skill
(`realisateur.md` 4, 109), the Arbitre carries neither; the Architecte's invocation 3
(`architecte.md` 531–640) issues four verdict kinds — rule written/changed, already
carried, not a convention, doubt or product decision — and *"never waits for the Product
Owner"*.

The diff old → new is exactly three hunks (new 127–140, 208–210, 356–380), one per row of
"Ce qui a changé". Nothing else moved: no renumbering, no section relocation, no table
rewritten outside those hunks, frontmatter identical.

---

## A. Conformity

No pass sheet, so no C-numbered defects. The three structural modifications are checked
against their demand text where one exists, and against their summary row otherwise.

| Modification | Expected (modifications.md) | Found (new file) | Verdict |
|---|---|---|---|
| **(1) Sort — row "arbitrage"** | *"Un arbitrage — deux choix défendables, deux lots divergeraient → Les conventions"* | 363: *"An arbitration — two choices equally defensible, and two lots would choose differently → The Architecte — that is what a convention is for"* | **Conform.** "The Architecte" for "les conventions" is the same destination — the Architecte is the only writer of that file. |
| **(1) Sort — row "piège"** | *"Un piège de plateforme indevinable avant le test rouge → `## Traps` de `CURRENT_TECHNICAL_STATE.md`"*; summary row adds *"qu'il écrit lui-même"* | 364: *"A platform trap nobody could guess before a red test → `## Traps` of `CURRENT_TECHNICAL_STATE.md` — write it there yourself, and settle the block with it"* | **Conform to the demand.** The demand's own section name `## Traps` does not exist in the target file — see D1. |
| **(1) Sort — row "la règle X"** | *"« La règle X s'applique-t-elle à mon cas ? » → Rien — c'est une question de lecture, pas un manque"* | 365: *"« Does rule X apply to my case? » → Nothing — it is a question of reading, not a missing rule: answer it from the rule and settle"* | **Conform**, with an addition (*"answer it from the rule and settle"*) not in the demand — see B2. |
| **(1) Sort — row "règle devenue fausse"** | *"Une règle devenue fausse → Les conventions, en remplacement — et le Product Owner arbitre"* | 366: *"A rule in force that is now wrong → The Architecte, as a replacement — and it is the Product Owner who arbitrates: say so"* | **Conform**, with an addition (*"say so"*) not in the demand and with no destination — see B3, D5. |
| **(1) Sort — intro** | Summary row: *"Quatre destinations, dont trois ne vont pas à l'Architecte"*. Demand table: two of four rows go to *"Les conventions"* | 358–359: *"three of the four answers do not go to the Architecte"* | **Conform to the summary row, not to the demand's table.** Two rows (363, 366) go to the Architecte, so two — not three — do not. The miscount is in the summary row and was transcribed. See D3. |
| **(1) Sort — rationale "Pourquoi `## Traps`"** | *"le Réalisateur le lit en entier, toujours — « tu ne peux pas greper une règle dont tu ignores qu'elle s'applique à toi » — alors qu'une convention n'est tenue que si la fiche la nomme"* | 375–378, same three clauses | **Conform.** |
| **(1) Sort — "Cas observé"** | *"sur 25 règles ajoutées par demande, 11 sont des portes ouvertes — surtout des réponses à « la règle précédente s'applique-t-elle à mon cas ? » — et 8 des 18 restrictions restreignent une règle elle-même ajoutée par demande. Le fichier grandit par empilement."* | 368–373: *"Measured: on 25 rules added by request, 11 were open doors — mostly « does the previous rule cover my case? » — and 8 of the 18 restrictions restrict a rule itself added by request. The file grows by stacking."* Preceded by the demand's opening sentence, *"everything that comes back becomes a convention today, for want of anywhere else to go"*. | **Conform.** The section says *"la mesure qui fonde le tri est dans l'agent"* — it is. |
| **(1) Sort — "once" kept** | Old 338–339: *"Ask the Architecte for it — once"* | 380: same sentence, now after the table and the two rationale paragraphs | **Conform** — the fall-through for rows 1 and 4. Its placement no longer says which rows it applies to — see D4. |
| **(2) Prohibition** | Summary row only: *"Jamais une règle dans `TECHNICAL_CONVENTIONS.md` — sa seule écriture hors fichier de blocage est un piège"* | 208–210: *"Write a rule into `TECHNICAL_CONVENTIONS.md` — that is the Architecte's file. Your one write outside a blocking file is a trap, in `## Traps` of `CURRENT_TECHNICAL_STATE.md`"* | **Conform to the summary row, literally.** The claim "one write outside a blocking file" is false within the file itself — see D2. |
| **(3) U10 cascade** | Cascade row (`modifications.md` 1020): *"il répond à chaque entrée, numérotées, sous un seul `## Decision` — et les lit toutes avant d'en trancher une, puisqu'une entrée dit souvent ce dont elle dépend"*; arbitre row (1285): *"une réponse par `## Blocking N`, et il les lit toutes avant d'en trancher une"* | 129–137: *"A blocking file may carry several `## Blocking N` entries — the Détailleur files everything one walk found, at once. You answer each of them, numbered, under the single `## Decision` — one answer per blocking, and none left out. Read them all before answering any — an entry often says what it depends on, and settling the second changes what the first means."* | **Conform.** Attribution to the Détailleur alone is right: the Réalisateur's file stays single-entry. Lines 139–140 go beyond the cascade row — see B1. |

Nothing listed as ÉCARTÉ or REPORTÉ for this agent; nothing to verify as not applied.

---

## B. Unannounced changes

The three hunks each carry one or two sentences that no row of "Ce qui a changé" and no
line of "La demande" asks for.

**B1** — line 139–140, inside hunk (3). **TO FIX** (see D6 for the consequence).
> New: *"🔴 One of them is not yours — 📌 say so for that one, and settle the others. ⚠️ A file half-answered still moves the agent forward."*
> Old: nothing.
Neither the cascade row nor the U10 demand says what to do when one entry cannot be
settled. This sentence decides it — partial fill — and the caller's rules do not know that
outcome (see D6).

**B2** — line 365, inside hunk (1). **NOTE.**
> New: *"Nothing — it is a question of reading, not a missing rule: **answer it from the rule and settle**"*
> Demand: *"Rien — c'est une question de lecture, pas un manque"*
The added clause turns a destination into a gesture. Reasonable, but it sits under a section
whose premise is *"The corpus says nothing"* (356) — see D4.

**B3** — line 366, inside hunk (1). **TO FIX** (see D5).
> New: *"The Architecte, as a replacement — and it is the Product Owner who arbitrates: **say so**"*
> Demand: *"Les conventions, en remplacement — et le Product Owner arbitre"*
"Say so" names no place — the request file? `## Decision`? the report? — and no reader.

**B4** — line 358–359, inside hunk (1). **NOTE** (the count itself is D3).
> New: *"🔴 First, ask what the need really is — 📌 three of the four answers do not go to the Architecte:"*
> Demand: no intro sentence; the summary row supplies *"dont trois ne vont pas à l'Architecte"*.
An intro was needed; the count it carries comes from the summary row, not the demand.

**B5** — line 127–140, placement. **NOTE.**
The multi-entry block is inserted as the **first** thing under `## What you write`, before
the section's governing sentence (142: *"The `## Decision` field of the blocking file you were
given, and nothing else in it"*). It refers to *"the single `## Decision`"* (133) before the
section has introduced the field. It is also headed by bold text (`**A file with several
blockings**`), not a heading, while the file's other sub-blocks are `##`. No row asked for
this placement; moving it after line 162 would read in order.

No other difference: `diff -u` old → new shows exactly the three hunks above. No
renumbering, no moved section, no reworded rule, no rewritten table outside them. The
frontmatter (name, description, tools, model, effort) is byte-identical.

---

## C. Gestures against tools

Frontmatter: `tools: Read, Grep, Glob, Edit, Write, Agent` (line 4, unchanged).

**Gestures → tools**

| Gesture | Line | Tool | Status |
|---|---|---|---|
| Read the blocking file, the settled ones beside it, the split, the order, the technical document, the lot's sheet and report, `verdict.md` `## Status`, `TECHNICAL_CONVENTIONS.md` in full | 92–116 | `Read` | Covered |
| Find the numbered settled blocking files beside it; find every `code/<lot>/verdict.md`; check whether `code/redecoupage.md` and `architecte/` already exist | 98, 110, 320, 382 | `Glob` | Covered |
| Grep the code to confirm a fact | 118, 204, 295–296 | `Grep` | Covered |
| Fill `## Decision` (an existing empty heading) | 142, 167, 409 | `Edit` | Covered — and `When Edit fails` (221–226) is written for it |
| Create `code/redecoupage.md`, or append a section when it exists | 320–322 | `Write` / `Edit` | Covered |
| Create `architecte/arbitre-<lot>.md` | 382 | `Write` | Covered |
| Call the Architecte and wait | 393–403 | `Agent` | Covered |
| **Write a trap into `## Traps` of `CURRENT_TECHNICAL_STATE.md`** | 209–210, 364 | `Edit` exists — but `Edit` requires the file to have been `Read` first, and 120 forbids reading it (*"Nothing else"*); and the project rule for that file (`technical-state-format` skill: *"never write to it without"* loading it) needs `Skill`, which the Arbitre does not carry | **Gesture with no means — see C1, C2** |
| **Poll the blocking file every 2 then 5 minutes, up to 20 minutes** | 419–424 | No tool waits: no `Bash` (`sleep`), no `Monitor`. `Read` can re-read but nothing paces it | **Gesture with no means — pre-existing, see C3** |

**C1** — line 209–210 and 364. **TO FIX.**
> *"write it there yourself"* — into `CURRENT_TECHNICAL_STATE.md`.
The Réalisateur, the other writer of that file, carries `Skill` and is told to load
`technical-state-format` before writing (`realisateur.md` 4, 109). The Arbitre has no
`Skill` tool and no instruction to load the skill. Either add `Skill` to the tools and the
load instruction next to line 364, or state that the Arbitre writes a trap without the
format the skill imposes — which the skill's description forbids.

**C2** — line 120 versus 364. **TO FIX** (also D8).
> 120: *"🔴 Nothing else. Not the product file, not `docs/process/`, not another lot's code."*
`CURRENT_TECHNICAL_STATE.md` is not in the reading list, and `Edit` needs a prior `Read`.
An agent obeying 120 cannot place a trap under a heading it has never opened. Add the file
to "What you read", scoped to the trap case.

**C3** — line 419–424. **NOTE**, pre-existing (identical in old 378–383). Question rather
than verdict: with `Read, Grep, Glob, Edit, Write, Agent` only, how does the Arbitre wait two
minutes between two reads? Nothing in the toolset sleeps or schedules. If the harness
provides no pacing, the 0–20-minute table is aspirational and the wait collapses to
"re-read once, then stop". Not introduced by the refonte; flagged because C asks for every
gesture.

**Tools → gestures**

Every one of the six tools is used by at least one gesture above. No idle tool.

---

## D. Internal coherence (new file alone)

**D1** — line 210, 364, 375. **TO FIX.**
> *"`## Traps` of `CURRENT_TECHNICAL_STATE.md`"*
No such heading exists in the target file; the section is `## Traps — general`, and the
format rule for that file routes a trap owned by one subject under that subject's `###`
heading, with `## Traps — general` reserved for what several subjects share. The rationale at
375–378 (*"the Réalisateur reads it whole, always"*) is true of `## Traps — general` only —
the Détailleur and the Réalisateur read that section and `## Dead state` whole, and grep the
rest. Naming the real heading, and the subject-owned alternative, is what the writer needs.
The demand itself wrote `## Traps`; the error is inherited, still an error in the file.

**D2** — line 209–210. **TO FIX.**
> *"Your one write outside a blocking file is a trap, in `## Traps` of `CURRENT_TECHNICAL_STATE.md`"*
Contradicted by 320 (*"Write `code/redecoupage.md`"*) and 382 (*"Write
`architecte/arbitre-<lot>.md`"*) — two other writes outside a blocking file, both kept from
the old file. A reader taking 209 as the rule would refuse the two writes the procedure
depends on. The sentence is a literal transcription of the summary row; the row is wrong
about the file.

**D3** — line 358–359. **TO FIX.**
> *"three of the four answers do not go to the Architecte"*
The table that follows sends row 1 (363) and row 4 (366) to the Architecte. Two of four do
not (364, 365). Announced count does not match the table.

**D4** — line 304 versus 356–380. **TO FIX.**
> 304: *"Nothing, and a rule would settle it → 🔴 Call the Architecte — see below"*
> 356: *"The corpus says nothing, and a convention would."* then 358: *"three of the four answers do not go to the Architecte"*
The move-3 table still names the Architecte as the unconditional answer to that row; the
section it points to now says the Architecte is one destination of four. And row 3 of the
sort (365: *"answer it from the rule and settle"*) presupposes a rule exists — which
contradicts the section's premise *"the corpus says nothing"* and duplicates move 1
(276–285: conventions first, *"a rule that allows the blocked state is an answer"*). Two
fixes: reword 304 to *"see below"* without prejudging the destination; and either drop row 3
or present it as *"you should have found it at move 1 — go back"*. Line 380 (*"Ask the
Architecte for it — once"*) follows the table without saying it applies to rows 1 and 4
only.

**D5** — line 366. **TO FIX.** Question rather than verdict on the mechanism.
> *"The Architecte, as a replacement — ⚠️ and it is the Product Owner who arbitrates: say so"*
Say so **where** — in `## What I need` of the request, in `## Decision`, in the report? And
then what? The Architecte's invocation 3 never waits for the Product Owner and issues a
verdict or a refusal; the Arbitre's post-return table (407–410) has *"Refused → Wait for the
Product Owner"*, and that wait ends in an empty `## Decision` the caller stops on. So the
branch "rule now wrong" runs: request → refusal → 20-minute poll → stop. Nobody replaces the
rule. Is the intended flow that the Arbitre waits for the Product Owner **first**, then
asks the Architecte for the replacement with her answer in hand? The line does not say.

**D6** — line 139–140 versus 24–26, 171–174, 419, 429–435. **TO FIX** — possibly BLOCKING
depending on how often a walk mixes a product question with technical ones; question left
open below.
> 139: *"One of them is not yours — say so for that one, and settle the others. A file half-answered still moves the agent forward."*
> 171: *"When you waited for the Product Owner and got nothing, leave `## Decision` exactly as you found it — empty. That is the one case where the field stays untouched: the agent that called you tests on it, and anything written there would read as an answer."*
> 429: *"That empty field is the signal"*
In a Détailleur file with, say, three entries, one of which turns on a behaviour: the
Arbitre must settle entries 1 and 3 (139), and must leave the field empty for entry 2
(419, 429). Both cannot hold. If it writes for 1 and 3, the field is filled, the signal is
lost, and the caller's table (Filled → apply, rename, detail the block) details the block
with entry 2 unsettled. If it writes *"waits for the Product Owner"* against entry 2, that
is exactly what 171–174 forbid. The file offers no third option — a procedure branch that
leads nowhere. Question: is the intended rule "a product question among the entries makes the
whole file wait" (then 139 must say so), or "a numbered `## Decision` may carry an explicitly
empty entry" (then 171–174 and the caller's test must change)?

**D7** — line 139 versus 24 and 164. **TO FIX** (same sentence as D6, distinct defect).
> 24: *"What the user sees is not yours"* — a product question, handed back untouched.
> 164: *"When a block is not yours — a Relecteur's, a Contrôleur's, an Architecte's — say so in `## Decision`"* — a mis-routed block, answered *"Not settled here"*.
> 139: *"One of them is not yours"*
"Not yours" carries two senses in the file, with opposite gestures (empty field versus
written refusal). At 139 it is inside a file the Détailleur wrote, so the 164 sense cannot
apply — every entry is from a caller that is yours — and only the 24 sense remains, whose
gesture is the one 139 does not allow. The sentence is also phrased as an assertion (*"One
of them is not yours"*) where a condition is meant (*"When one of them…"*).

**D8** — line 120 versus 364. **TO FIX** (the reading side of C2).
> 120: *"🔴 Nothing else."*
> 364: *"write it there yourself"*
A file the agent must write into is absent from the exhaustive reading list. Same root as
C2; listed here because it is a contradiction inside the file regardless of tooling.

**D9** — line 145 versus 129. **NOTE.**
> 145: *"Never touch `## What blocks`, `## Where` or `## To resume`"*
In a multi-entry file those are `###` headings under each `## Blocking N` (the Détailleur's
shape). The intent survives; the heading level named does not match the file the rule now
also covers.

**D10** — line 407–410. **NOTE**, pre-existing (old 366–369).
> *"A rule written or changed → Copy…"* / *"Refused → Wait for the Product Owner"*
The Architecte's invocation 3 returns four verdict kinds: written or changed, already
carried (cites number and text), not a convention (says where it belongs), doubt or
product decision. "Already carried" fits row 1 in practice; "not a convention — it belongs
in the code / the tooling" fits neither row and would be read as a refusal, sending a
tooling answer to a 20-minute Product Owner wait. Not introduced by the refonte.

**D11** — line 369–372. **NOTE**, question.
> *"on 25 rules added by request, 11 were open doors … and 8 of the 18 restrictions restrict a rule itself added by request"*
Is "18 restrictions" counted over the whole conventions file, or over the 25? If over the
25, 11 + 18 exceeds 25 unless the two categories overlap. The sentence is copied from the
demand verbatim; it reads as an internal inconsistency to an agent that has not seen the
measurement. One clause (*"of the file's 18 restrictions"*) would settle it.

**D12** — line 133 versus 226. **NOTE.**
> 226: *"Found N matches → anchor on `## Decision` with the line above it"*
Still valid: the multi-entry shape keeps a single `## Decision`. Recorded as checked, no
defect.

---

## Summary

- **A**: the three structural modifications are applied as their rows describe; the sort
  table follows the demand line for line. Two of the transcribed claims are wrong about the
  file they now sit in — the "three of four" count (D3) and the "one write outside a
  blocking file" (D2) — and both come from the summary rows, not from the demand.
- **B**: three unannounced sentences, all inside the announced hunks — the half-answered
  file (B1), "answer it from the rule and settle" (B2), "say so" (B3). No change outside
  the three hunks.
- **C**: the new trap-writing gesture has no means as written — no `Skill` for the format
  the project imposes on that file (C1), and a reading rule that forbids opening it (C2).
  The polling wait has never had a tool that paces it (C3, pre-existing).
- **D**: the section name `## Traps` does not exist (D1); the multi-entry rule collides with
  the empty-field signal the whole Product-Owner wait rests on (D6, D7); the "rule now
  wrong" branch ends nowhere (D5); move 3's table and the sort disagree about the Architecte
  (D4).

**Severity count**: BLOCKING 0 (D6 could be, see its question) · TO FIX 12 entries — B1,
B3, C1, C2, D1, D2, D3, D4, D5, D6, D7, D8 — of which B1/D6/D7 share one fix and C2/D8
another, so nine distinct corrections · NOTE 8 — B2, B4, B5, C3, D9, D10, D11, D12.
