# Vérification — context budget, one invocation per agent

What one invocation loads, agent by agent, for the 20 agents of
`.claude-new/agents/` ("now") against the 17 of `.claude/agents/`
("before"). Read only the sections that say what each agent reads
(`## What you read`, `## Where you work`, the `## INVOCATION n` tables
and the reading moves they open on); every target file was measured
with `wc -l` / `wc -c` on the files this repository holds today. Line
numbers are the **new** file's unless stated.

**Conversion used**: 1 token ≈ 4 bytes of this English markdown
(emoji-heavy lines cost more, so the token figures are floors).
**Window assumed**: 200 K tokens. **Holds** = the input stays under
≈ 100 K tokens, leaving the other half for the agent's own tool
traffic, reasoning and output. **Heavy** = 40–60 K tokens of input:
holds, but a bigger feature or a longer state document eats the margin.
Every figure counts the agent's own `.md` (its system prompt) first.

**The three headings.** `## What you read`: arbitre, architecte,
concepteur, contrôleur, détailleur, réalisateur, relecteur, testeur,
vérificateur (9 of 20). `## Where you work` with a path table:
arbitre, architecte, assembleur, cadreur, classeur, convertisseur,
découpeur, lexicographe, qualifieur, sondeur. An invocation table:
architecte, contrôleur, diagnostiqueur, fusionneur, rédacteur;
convertisseur and lexicographe carry `## INVOCATION n` sections with
the reads in their first move; the sondeur's are `## Invocation n`,
lower case. 🔴 **No agent lacks all three** — none to report.

---

## A. The files, measured

| File | Lines | Bytes | Who loads it whole |
|---|---|---|---|
| `docs/TECHNICAL_CONVENTIONS.md` | 612 | 30 679 | Cadreur, Détailleur, Arbitre, Architecte inv 2–4, Diagnostiqueur inv 1 |
| — its 91 rules, `permanente` share (estimate, see B1) | ≈ 340–430 | ≈ 17 000–21 500 | Concepteur, Testeur, Réalisateur, Relecteur |
| `docs/CURRENT_TECHNICAL_STATE.md` | 2 305 | 141 089 | nobody by rule — Diagnostiqueur inv 1 names it without a restriction |
| — `## Traps — general` + `## Dead state` | 321 | 19 330 | Détailleur, Réalisateur |
| `docs/PRODUIT_GLOBAL.md` | 1 | 15 | nobody (index by grep; "runs past 250 KB" is the design figure) |
| `docs-new/process/GRILLE_CONVENTIONS.md` (old: 880 / 38 242) | 594 | 25 447 | Architecte, every invocation |
| `docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md` (old: 376 / 15 072) | 393 | 15 991 | Sondeur inv 1, 2 |
| `docs-new/process/GRILLE_EXISTANT.md` (new) | 111 | 4 647 | Sondeur inv 3 |
| `docs-new/process/GRILLE_FERMETURE_TECHNIQUE.md` | 274 | 10 818 | Convertisseur inv 1, 2; Diagnostiqueur inv 2 |
| `premiere-app/desc-produit.md` — 61 blocks, ≈ 9 lines / 865 B each | 563 | 52 747 | Sondeur (first turn, and inv 2 always), Architecte inv 1, 4, Convertisseur inv 2, Rédacteur inv 3 |
| `premiere-app-2/desc-produit.md` — 183 blocks | 955 | 60 230 | same agents, next feature |
| `premiere-app/spec-technique.md` (preamble: 35 lines / 1 113 B) | 1 136 | 54 483 | Cadreur, Arbitre, Architecte inv 1, 4, Convertisseur inv 2; Vérificateur in effect (every cited entry) |
| `premiere-app/desc-par-nature.md` → `convertisseur/<nature>-input.md` | 380 | 51 566 | one nature each: 2–14 blocks, ≈ 2–13 KB |
| `premiere-app/code/decoupage.md` | 320 | 14 382 | Cadreur (writes), Vérificateur, Arbitre |
| `bugfix-06/code/decoupage.md` | 729 | 40 763 | same, correction cycle |
| `bugfix-06/desc-bug.md` | 413 | 47 055 | Cadreur, Arbitre, Vérificateur (entries) |
| `premiere-app/code/lot-*/fiche-executable.md` (45) | avg 62, max 155 | avg 3 090, max 9 349 | Réalisateur, Relecteur, Concepteur, Testeur, Arbitre, Contrôleur inv 1 |
| `bugfix-06/code/lot-*/fiche-executable.md` (55) | avg 116, max 421 | avg 6 050, max 20 634 | same |
| `code/lot-*/compte-rendu.md` | avg 22, max 50 | avg 470, max 3 655 | Relecteur, Arbitre |
| `bugfix-06/…/blocked_*.md` (25) | avg 66, max 110 | avg 3 430 | Arbitre |
| `bugfix-06/architecte/*.md` (21 requests) | 1 547 | 77 225 | Architecte inv 3, all of them per call |
| `bugfix-06/investigation/*.md` (66) | 3 664 | 180 186 | Diagnostiqueur inv 2 |
| `bugfix-06/bug-list.md` · `bugfix-07/bug-list.md` | 585 · 775 | 33 877 · 39 862 | Diagnostiqueur inv 2; Fusionneur inv 3 (all seven: 1 646 / 89 200) |
| `premiere-app-2/idees.md` | 1 543 | 69 284 | Lexicographe inv 1, 2; Rédacteur inv 1 |
| `premiere-app-2/lexique.md` (`## Tranché` 1 230 lines ≈ 68 KB) | 1 593 | 88 627 | Lexicographe every invocation; Rédacteur inv 1, 2 |
| `premiere-app-2/questions/lexicographe/*.md` (15 files) | 5–427 | 1 281–26 972 | Lexicographe inv 2, 4 |
| `premiere-app/questions-sondeur-01.md` (merged) · raw 3 sondeurs | 951 · 1 451 | 36 322 · 54 857 | Assembleur (raw), Lexicographe inv 3, Rédacteur inv 2 (merged) |
| `premiere-app/tracabilite.md` · `tracabilite-full.md` · `couverture.md` | 85 · 67 · 141 | 5 566 · 4 290 · 5 469 | Architecte, Contrôleur (via grouper) |
| `premiere-app/code/rapport-controle-0N.md` (4, whole-feature) | 74–84 | 5 135–8 247 | reference for the partials' size |
| Kotlin: 331 files, largest test 1 217 lines ≈ 50 KB | 40 653 | 1 743 492 | "the code you touch": 20–70 KB per lot |
| Build files (`build.gradle.kts`, `settings`, `libs.versions.toml`, app-phone) | — | 9 291 | Architecte inv 3 |

Agent files, before → now (bytes): réalisateur 18 379 → 22 597 ·
relecteur 11 344 → 16 035 · sondeur 9 377 → 15 423 · convertisseur
20 918 → 28 226 · architecte 21 732 → 29 923 · cadreur 32 418 → 37 301
· lexicographe 14 576 → 21 743 · rédacteur 20 037 → 26 916 · classeur
8 624 → 12 712 · découpeur 6 090 → 9 211 · assembleur 5 817 → 9 078 ·
détailleur 23 606 → 27 470 · vérificateur 16 864 → 19 291 · arbitre
14 097 → 16 397 · fusionneur 16 676 → 17 405 · contrôleur 11 714 →
12 046 · diagnostiqueur 21 201 (identical) · concepteur 7 038, testeur
7 603, qualifieur 11 091 (new). 📌 **Every rewritten agent grew 3–65 %
before it reads a single file** — the sondeur by 64 %, the assembleur
by 56 %.

---

## B. The five priorities

### B1. Réalisateur and Relecteur — every `permanente` rule, whole

**What the text says.** réalisateur.md:66-71 — the rules marked
`permanente`, whole, plus those the sheet's `## Conventions` names;
relecteur.md:61-62 the same, and :343 "every rule marked `permanente`,
whatever the sheet says". Before: réalisateur.md (old):58 named
`docs/TECHNICAL_CONVENTIONS.md` with no restriction, then :71-74 "the
sheet's `## Conventions` names the rules bearing on this lot — open
each one"; relecteur.md (old):56 named the file with no restriction at
all.

🔴 **The marker does not exist yet.** `grep -ci permanente
docs/TECHNICAL_CONVENTIONS.md` → 0. The file carries 91 numbered rules
in 12 sections and none ends in `permanente` or `spécifique`; only
architecte.md:116-124 defines the marker, and only its invocation 4
(or a fresh derivation) would write it. Until then the instruction
resolves to *nothing*, and the four agents that carry it will fall back
to reading the file whole — which is what the Relecteur already did.

**How many lines, once marked.** The definition (architecte.md:120: an
await, a disk access, a catch, an identifier written — fired by an
ordinary act of writing code, in any lot) covers most of §5 Interface
contracts (69 lines), §6 Errors and failure (128), §7 State, resources
and effects (78), §10 Tests (64), §11 Naming (31), §9 Diagnostics
(16), and part of §4 Structure (60). §1 Governance, §2 Verification,
§3 Boundaries, §8 Configuration, §12 Dependencies (157 lines) are
mostly `spécifique`. **Estimate: 55–70 % of the rules, ≈ 340–430
lines, ≈ 17–21.5 KB, ≈ 4.5–5.5 K tokens.** ⚠️ **In practice the whole
file**: the permanent rules are scattered through 12 sections and a
single `Read` of 612 lines is how an agent gets them — so the practical
figure is 30 679 B ≈ 7.7 K tokens, marker or no marker.

**What the sheet named before.** Sampled `## Conventions` sections:
bugfix-06 lot-20 names 28 distinct rules (40 lines / 2 136 B of
paraphrase in the sheet itself), lot-39 28, lot-05 9; feature lots 12
and 30 name none by number. Opening 9–28 rules of ≈ 6.7 lines each =
60–190 lines ≈ 3–9.5 KB.

**Réalisateur, one lot** (agent 22.6 KB + sheet + conventions +
`conception.md` ≈ 1–2 KB + `tests.md` `## Red` line + state document
two sections 19.3 KB + the code touched 20–70 KB):

| | Typical lot (sheet 6 KB, code 40 KB) | Worst measured (sheet 20.6 KB, code 70 KB) |
|---|---|---|
| Now, strict (permanente ≈ 20 KB) | ≈ 110 KB ≈ 27 K tokens | ≈ 155 KB ≈ 39 K tokens |
| Now, practical (file whole 30.7 KB) | ≈ 120 KB ≈ 30 K | ≈ 165 KB ≈ 41 K |
| Before (agent 18.4 KB, 9–28 rules ≈ 6 KB) | ≈ 92 KB ≈ 23 K | ≈ 137 KB ≈ 34 K |
| Ratio | **1.2×** (conventions portion alone: 2–3×) | 1.15× |

**Holds.** Plus the `technical-state-format` skill and the gradle
output it reads at moves 5–6, both unchanged.

**Relecteur, one lot** (agent 16 KB + sheet + `compte-rendu` ≈ 1 KB +
`conception.md` + `tests.md` ≈ 3 KB + the files the prompt names 20–70
KB + conventions; on a divergence, one line of `sequence.md` and the
block's non-PASS sheets, say 3 × 6 KB):

| | Typical | Worst |
|---|---|---|
| Now | ≈ 86 KB ≈ 22 K tokens | ≈ 165 KB (with divergence) ≈ 41 K |
| Before (agent 11.3 KB, conventions whole) | ≈ 89 KB ≈ 22 K | ≈ 137 KB ≈ 34 K |
| Ratio | **1.0×** | 1.2× |

**Holds.** The Relecteur read the conventions whole before; naming the
permanent rules narrows the instruction and changes the load by
nothing.

**Concepteur and Testeur** (new, same rule at concepteur.md:57-58 and
testeur.md:65-66): agent 7–7.6 KB + the two sheet sections it names
(3–15 KB) + permanente ≈ 20 KB (30.7 practical) + `conception.md` +
the files/declarations it touches (10–40 KB) ≈ **40–90 KB ≈ 10–23 K
tokens each. Holds.** No "before" — the Réalisateur did both jobs.

### B2. Sondeurs — the transverse blocks beside their own

sondeur.md:38-53: the blocks to probe (`Genre: comportement`, named by
the prompt) plus **the transverse blocks, held beside them, every
turn** (4_grille.md:146: "every turn, whatever moved"), plus the grid
whole. Before (old :36-41): the product file **whole** on every
invocation — the old table said "Whole, to its last line", and old
:130-133 only narrowed later turns to the `NEW`/`MODIFIED` blocks.

🔴 **No block carries `Genre:` today** (`grep -c '^Genre:'` → 0 in
both features; the qualifieur is new), so the transverse count is an
estimate from the titles: B2–B5 (tokens), B29, B46, B52–B54 and the
format/text blocks B47–B51, B55–B56 read as category rules — **12–18
of 61 blocks, ≈ 110–160 lines, ≈ 10–14 KB.**

| Invocation | Now | Before | Ratio |
|---|---|---|---|
| Inv 1, first turn (every block) | agent 15.4 + grid 16 + file 52.7 = **≈ 84 KB ≈ 21 K** (premiere-app-2: ≈ 92 KB) | 9.4 + 15 + 52.7 = 77 KB | 1.1× |
| Inv 1, later turn (5 moved blocks ≈ 4.5 KB) | 15.4 + 16 + 4.5 + transverse 12 = **≈ 48 KB ≈ 12 K** | 9.4 + 15 + 4.5 = 29 KB | **1.7×** — the product-file part alone 3.7× |
| Inv 2, global (every block, always) | ≈ 84 KB, then writes the record (61 × 7 lines ≈ 430 lines ≈ 20 KB) | 77 KB | 1.1× |
| Inv 3, existant (new) | 15.4 + `GRILLE_EXISTANT` 4.6 + blocks with a `Global:` line + the global's named sections (0 today; ≈ 20–60 KB on a 250 KB global) = **≈ 30–120 KB** | — | — |

**Holds, all four.** ⚠️ **The later-turn angle is the one that grew
most in ratio (1.7×) and least in bytes (+19 KB)**: the transverse
blocks are a fixed cost every turn pays, and on premiere-app-2 (183
blocks, 60 KB) the same share is ≈ 15–20 KB.

### B3. Convertisseur — three split files beside its blocks

convertisseur.md:48-63: inv 1 reads `convertisseur/<nature>-input.md`
and `par-genre/transverses.md` (its constraint half, :113, :135);
inv 2 adds `par-genre/references.md` and `par-genre/hors-perimetre.md`
(:52-53 "invocation 2 only"), the technical document in full, every
notes file, the product file's text outside the blocks, and the grid.
Before (old :46-56): the blocks and the grid at inv 1; the document,
the notes, the product text and the grid at inv 2.

⚠️ **One inconsistency bears on the budget**: 5_reclasse.md:86 routes
`par-genre/references.md` to "the Convertisseur — its Text section",
i.e. the text-nature invocation 1, while convertisseur.md:52 says
invocation 2 only. The text invocation may load it (+ ≈ 8 KB).

`par-genre/` does not exist yet; sizes are the blocks' own, sorted:
transverses ≈ 10–14 KB, references (B47–B51, B55–B56, ≈ 8 blocks)
≈ 6–8 KB, hors-perimetre ≈ 1–2 KB (no such block today).

| Invocation | Now | Before | Ratio |
|---|---|---|---|
| Inv 1, one nature (screen, 14 blocks ≈ 12 KB — the largest) | agent 28.2 + grid 10.8 + blocks 12 + transverses 12 = **≈ 63 KB ≈ 16 K** | 20.9 + 10.8 + 12 = 44 KB | **1.4×** |
| Inv 1, a small nature (2 blocks ≈ 2 KB) | ≈ 53 KB | 34 KB | 1.6× |
| Inv 2, transversal | 28.2 + document 54.5 + 9 notes ≈ 15 + product text (practically the file, 52.7) + transverses 12 + references 8 + hors-perimetre 2 + grid 10.8 = **≈ 183 KB ≈ 46 K** — then writes preamble, `tracabilite.md`, entries | 20.9 + 54.5 + 15 + 52.7 + 10.8 = 154 KB | 1.2× |

**Holds.** Inv 2 is **heavy** (46 K tokens in, one of the four
heaviest of the set) and was already so; the three files add 22 KB to
it. Nine inv 1 calls run at once and each carries the same 12 KB of
transverse rules — 9 × 12 KB of duplicated context, not a per-call
risk.

### B4. Architecte, invocation 4 — the whole conventions file

architecte.md:277 (table) and :659-661: inv 4 = inv 1's inputs
(`desc-produit.md` whole, `spec-technique.md` whole, `tracabilite.md`,
`par-genre/directives.md`, the grid) **plus `TECHNICAL_CONVENTIONS.md`
whole**, then writes only what the file does not cover. Before: no
invocation 4; inv 1 read the two documents and the old, longer grid
(880 lines / 38 KB against 594 / 25 KB now).

| Invocation | Now | Before | Ratio |
|---|---|---|---|
| Inv 1, deriving | agent 29.9 + grid 25.4 + product file 52.7 + document 54.5 + tracabilite 5.6 + directives (new, ≈ 2–5 KB) = **≈ 172 KB ≈ 43 K** — then writes the conventions (≈ 30 KB) + `couverture.md` + questions | 21.7 + 38.2 + 52.7 + 54.5 + 5.6 = 173 KB | 1.0× (the grid shrank as much as the agent grew) |
| Inv 2, integrating | 29.9 + questions 5–20 + conventions 30.7 + couverture 5.5 + grid 25.4 = ≈ 97–112 KB ≈ 26 K | ≈ 90–105 KB | 1.1× |
| Inv 3, requests (bugfix-06: 21 files) | 29.9 + requests 77.2 + conventions 30.7 + couverture 5.5 + grid 25.4 + build files 9.3 + web = **≈ 178 KB ≈ 45 K** | ≈ 183 KB (old grid) | 1.0× |
| **Inv 4, completing** | inv 1 + conventions 30.7 = **≈ 203 KB ≈ 51 K tokens**, then writes additions + `couverture.md` + questions | — (inv 1: 173 KB) | **1.18× inv 1** |

**Holds — heavy.** Inv 4 is the largest input of the downstream chain
(≈ 51 K tokens, a quarter of the window) and every one of its parts
grows with the project: the next feature's product file is already 60
KB, and the conventions file gains a rule per settled request (91 rules
today, 21 requests in bugfix-06 alone). At 250 KB of inputs it still
holds; the margin is the output it must then produce on top.

⚠️ **Inv 3 re-reads every request in `architecte/`, settled ones
included** (:544 "glob it, that folder alone", :558 "read them all
before settling one" — the empty-`## Verdict` test needs each file
open). In bugfix-06 that is 21 files / 77 KB per call, and each lot's
end-of-lot call pays it again. Unchanged from before, but the largest
single re-read of the downstream loop.

### B5. Contrôleur, at assembly — every partial

controleur.md:243-247: read the partial of each group the prompt names
— never a `code/controle/` file it does not name — and check the block
list it gives; :245-246 never a sheet or the product file. Before (old
:283-284): "read every `code/controle/*.md`, and nothing else". The
grouper is byte-identical between `.claude/scripts/` and
`.claude-new/scripts/`, and `9_controle` invokes it the same way, so
the group count is the same before and now.

Run on `premiere-app/tracabilite-full.md` with `--auto`: **13 groups
selected** (budget 33 block-equivalents, 3–4 sheets and 3–7 blocks
each, lot-30 duplicated).

| Invocation | Now | Before | Ratio |
|---|---|---|---|
| Inv 1, one group (4 sheets avg 3.1 KB, 5 blocks ≈ 4.5 KB) | agent 12 + 12.4 + 4.5 = **≈ 29 KB ≈ 7 K**; worst group (4 × 9.3 KB) ≈ 54 KB | 11.7 + same ≈ 29 KB | 1.0× |
| Inv 2, assembly (13 partials) | 12 + 13 × (4–8 KB) = **≈ 64–116 KB ≈ 16–29 K tokens** + the block list in the prompt | 11.7 + the same 13 files | 1.0× |

**Holds.** The partial size is an estimate: one line per intention,
found ones included (:283-285), for 4–7 blocks of ≈ 9 sentences —
50–90 lines / 4–8 KB each; the four whole-feature reports on disk
(74–84 lines, 5–8 KB) listed far less. The naming of groups and the
block list is a filter, not an addition: it removes a stale partial's
bytes from the read. The doubling rule does not fire.

---

## C. The other fifteen

| Agent · invocation | What one call loads (now) | ≈ KB | ≈ K tokens | Before | Ratio | Verdict |
|---|---|---|---|---|---|---|
| **Cadreur** A (:345-353) | agent 37.3 + document whole 54.5 (bugfix-06: 47) + conventions whole 30.7 + greps 10–30; C adds every `redecoupage-NN.md` | 133–153 | 33–38 | 32.4 + same = 128–148 | 1.04× | Holds — the risk is the lifetime: it stays up through three Vérificateur rounds and writes 14–41 KB |
| **Vérificateur** (:54-73) | agent 19.3 + `decoupage.md` whole 14.4 (bugfix-06: 40.8) + preamble 1.1 + every cited entry, in effect the document minus orphans ≈ 50 + title grep + `## Status` lines | 85–112 | 21–28 | 16.9 + same | 1.03× | Holds |
| **Détailleur**, one block (:62-84, :544-548) | agent 27.5 + sequence 1 + decoupage restricted + `## Symbols` 5–15 + preamble 1.1 + cited entries 5–20 + state two sections 19.3 + conventions whole 30.7 + greps 10–30; then writes 3–6 sheets (bugfix-06 avg 6 KB, max 20.6) | 100–145 | 25–36 | 23.6 + same (old :60-64 also checked `## Defects`) | 1.03× | Holds — long-lived across Arbitre round trips |
| **Arbitre** (:90-122, unchanged text) | agent 16.4 + blocking file 3.4 (max 6) + earlier settled ones 0–10 + decoupage 14–41 + sequence 1 + document whole 54.5/47 + sheet 3–21 + report 0.5–4 + conventions whole 30.7 + greps | 125–175 | 31–44 | 14.1 + same | 1.02× | Holds — heavy end; the document and the conventions are read whole for one question |
| **Diagnostiqueur** inv 1 (:132, file identical) | agent 21.2 + conventions 30.7 + `CURRENT_TECHNICAL_STATE.md` **with no section named** + greps | 62 (state grepped) — **≈ 200 (state read whole)** | 16 — **50** | identical | 1.0× | Holds, but 🔴 **the only agent that names the 141 KB state document without a restriction** (Détailleur and Réalisateur say "two sections"). Read whole, it is 35 K tokens for one gap, times 66 gaps |
| **Diagnostiqueur** inv 2 (:417-418) | agent 21.2 + every investigation (bugfix-06: 66 files, 180.2) + `bug-list.md` 33.9 + grid 10.8; then writes `desc-bug.md` 47 | **≈ 246** | **≈ 62 in, 12 out** | identical | 1.0× | **Holds with the least margin of the whole set.** Unchanged — a pre-existing risk. bugfix-07's list is 775 lines / 40 KB; ≈ 100 gaps at the same report size (2.7 KB) reaches ≈ 340 KB ≈ 85 K tokens |
| **Fusionneur** inv 1 (:249) | agent 17.4 + final product file 53–60 + the global's matched sections (0 today; ≈ 20–60 on a 250 KB global) | 70–135 | 18–34 | 16.7 + same | 1.0× | Holds |
| **Fusionneur** inv 2 | agent + plan 10–20 + answered questions + global sections | 50–100 | 12–25 | same | 1.0× | Holds |
| **Fusionneur** inv 3 (:251) | agent + every `bugfix-*/bug-list.md` (7: 89.2) + global sections | 106–170 | 27–42 | same | 1.0× | Holds — heavy; the bug lists only accumulate |
| **Rédacteur** inv 1 (:396-403) | agent 26.9 + `idees.md` 69.3 + `lexique.md` 88.6 + global index (grep); then writes the product file 53–60 + questions | **≈ 185** | **≈ 46 in, 15 out** | 20 + same = 178 | 1.04× | Holds — heavy, third heaviest input; driven by the lexicon's growth (1 593 lines after 15 question files) |
| **Rédacteur** inv 2 (:500-525) | agent 26.9 + one questions file 1–37 + lexique 88.6 + product file by grep + a handful of blocks 5–10 | 122–163 | 30–41 | 20 + same | 1.05× | Holds |
| **Rédacteur** inv 3, merging (:634-636, new) | agent 26.9 + `desc-produit.md` whole 53–60 + every decisions file named (1–8 cycles, size unknown, say 5–20 each); then writes the 53–60 KB copy | 90–250 | 22–62 | — | — | Holds; a copy done by Read + Write costs the file twice |
| **Lexicographe** inv 1, 2nd sweep on (:236-237) | agent 21.7 + `idees.md` 69.3 + `## Tranché` ≈ 68; writes a questions file up to 27 | ≈ 159 | ≈ 40 | 14.6 + same = 152 | 1.05× | Holds — heavy |
| **Lexicographe** inv 2 (:341-342) | agent 21.7 + questions file ≤ 27 + `idees.md` 69.3 + `lexique.md` **whole** 88.6; then edits both | **≈ 206** | **≈ 52** | old :229 "the questions file, and it alone beside the idea file", :232 "against `## Tranché`" → 14.6 + 27 + 69.3 + 68 = 179 (110 if `## Tranché` was grepped) | 1.15× (1.9× against the grep reading) | **Holds — second heaviest input of the set**, and the lexicon grows every turn |
| **Lexicographe** inv 3 (:396-430) | agent + an answered questions file (sondeur's merged: 36.3) + `lexique.md` whole 88.6 | ≈ 147 | ≈ 37 | 14.6 + same | 1.05× | Holds — heavy |
| **Lexicographe** inv 4 (:487) | agent + own questions file + the answered file + lexique 88.6 | ≈ 150 | ≈ 38 | same | 1.05× | Holds — heavy |
| **Assembleur** (:23-37, 4_grille: 4 files) | agent 9.1 + three angles' + the global's questions files (first turn ≈ 1 451 lines / 54.9 raw; later turns a few KB); writes the merge (36.3) | ≈ 64 | ≈ 16 | 5.8 + same | 1.05× | Holds |
| **Classeur** (:28-43) | agent 12.7 + the named blocks (first turn: all 61 = 52.7; premiere-app-2: 60.2) + own answered questions file (new, ≈ 1.3) + a blocking file | 15–74 | 4–19 | 8.6 + same | 1.06× | Holds |
| **Qualifieur** (:30-43, new) | agent 11.1 + the named blocks (first turn: the file, 52.7–60.2) + own answered questions file | 15–72 | 4–18 | — | — | Holds |
| **Découpeur** (:26-51) | agent 9.2 + the named blocks **by line range** (grep `^### B` then ranges — new :40-46); first turn: the file whole 52.7–60.2 | first turn 62–70; later turn 12–20 | 15–17 · 3–5 | 6.1 + named blocks (no range rule — in practice the file whole, 53–60) | first turn 1.05×; **later turn ≈ 0.3×** | Holds — the one agent that reads less than before |
| **Sondeur, Convertisseur, Architecte, Contrôleur, Réalisateur, Relecteur, Concepteur, Testeur** | see part B | | | | | |

---

## D. What to report

**Reading twice as much — none, on the strict reading; three on a
portion.** No agent's full invocation reaches 2× its former load. The
closest:

1. **Sondeur, later-turn angle: 1.7× overall** (29 → 48 KB), and
   **3.7× on the product-file portion** (4.5 → 17 KB): the transverse
   blocks are read every turn whatever moved (4_grille.md:146). Small
   in bytes; the doubling is real on what the agent actually probes.
2. **Réalisateur: 2–3× on the conventions portion** (6 → 17–21 KB
   strict), 1.2× overall. Practically 1.0× — a `Read` of the 612-line
   file is how the scattered permanent rules get read, and that is what
   the file cost before.
3. **Lexicographe inv 2: 1.15× — or 1.9× if the old "against
   `## Tranché`" was a grep** (110 → 206 KB). Now the whole lexicon is
   read by rule (:341).

**Heavy, holds — the five largest inputs, in order:**

| Rank | Invocation | ≈ KB in | ≈ K tokens | Changed? |
|---|---|---|---|---|
| 1 | Diagnostiqueur inv 2, assembly (bugfix-06 scale) | 246 | 62 | no — pre-existing |
| 2 | Lexicographe inv 2, settling (premiere-app-2 scale) | 206 | 52 | +15 % |
| 3 | **Architecte inv 4, completing** | 203 | 51 | new invocation |
| 4 | Rédacteur inv 1, structuring | 185 | 46 | +4 % |
| 5 | Convertisseur inv 2, transversal | 183 | 46 | +20 % |

None crosses the 100 K-token line. Every one of them grows with the
project rather than with the feature: the lexicon (88.6 KB and rising
by a question file per turn), the conventions file (a rule per settled
request), the investigations (one per listed gap), the global (design
figure 250 KB).

**At risk, by the text rather than by the numbers:**

- 🔴 **`permanente` is a marker no rule carries yet** (0 hits in
  `docs/TECHNICAL_CONVENTIONS.md`). Four new reading instructions
  (concepteur.md:57, testeur.md:65, réalisateur.md:66, relecteur.md:62)
  select on it; until architecte inv 4 marks the 91 rules, they select
  nothing, and each agent decides alone whether that means "nothing" or
  "everything".
- 🔴 **Diagnostiqueur inv 1 names `CURRENT_TECHNICAL_STATE.md` with no
  section** (diagnostiqueur.md:132) — the one agent that does. Read
  whole it is 141 KB ≈ 35 K tokens per gap, 66 gaps per cycle.
- ⚠️ **Architecte inv 3 re-reads every request in `architecte/` at
  every call**, settled ones included (:544, :558): 21 files / 77 KB in
  bugfix-06, paid at the end of every lot that raised one.
- ⚠️ **5_reclasse.md:86 vs convertisseur.md:52** — `references.md`
  goes to the text nature at inv 1 by the command, to inv 2 only by the
  agent. Whichever wins, ≈ 8 KB.
- ⚠️ **The agent files themselves**: the sondeur's system prompt grew
  64 %, the assembleur's 56 %, the lexicographe's 49 %, the
  découpeur's 51 %, the classeur's 47 %. On the small upstream calls
  (assembleur, classeur, découpeur later turn, sondeur later turn) the
  agent file is now the largest thing in context.

**No agent lacks a reading section** — all 20 carry `## What you
read`, a `## Where you work` table, or an invocation table.
