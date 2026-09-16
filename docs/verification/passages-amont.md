# Verification V2.5a — Handovers, upstream

**Scope**: twelve consecutive pairs of the rebuilt chain, `.claude-new/`.
For each, what the first agent writes against what the second expects —
section names, field names, shape, possible values. Only the sections
that say what an agent reads and writes were opened (`grep -n '^## '`
first, then the ranges). Commands were opened only where the handover
goes through one (`/1_lexique`, `/2_structure`, `/3a_genre`,
`/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`, `/9_controle`,
`/fusion`, `/8_code`). `docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md`
was grepped for its nature names and record identifiers, nothing more.

Line numbers are those of the **new** file. `W` = the writer's line,
`R` = the reader's line. Severity: **BLOCKING** — a name or shape gap
that makes the handover fail, or a file the reader is named that
nobody writes · **TO FIX** — a mismatch the reader survives by luck or
by prose · **NOTE** — stale wording, a field written that nobody reads,
an inconsistency inside one agent.

**Summary — 12 pairs, 3 BLOCKING, 7 TO FIX, 12 NOTE.**

| Pair | Verdict |
|---|---|
| lexicographe → redacteur | ✅ matches · 2 NOTE |
| redacteur → decoupeur | ✅ matches · 1 NOTE |
| decoupeur → qualifieur | ✅ matches |
| qualifieur → classeur | TO FIX ×3 (no spelling rule for `Genre:` · `/3b_nature`'s `-B1` lands on `Genre:`, not the heading · its `grep -c '^Nature:$'` can never reach zero) |
| classeur → sondeur | ✅ matches — eight nature names identical in classeur, grid, convertisseur |
| sondeur → assembleur | ✅ matches |
| assembleur → redacteur | **BLOCKING** (a `Défaut:` accepted by silence is stopped by every empty-`Answer:` gate before the Rédacteur) · TO FIX (the Rédacteur never names the `Défaut:` field) · 1 NOTE |
| redacteur → convertisseur | ✅ matches · 2 NOTE (`Intent and vocabulary` has no source; `technique-<nature>.md` has no reader — cross-ref `renommages.md`) |
| convertisseur → architecte | ✅ matches · 1 NOTE |
| convertisseur → cadreur | TO FIX (an unresolved `[B…]` reference is not in the Cadreur's stop list) · 2 NOTE (`Consumes:` and `## Cross-cutting rules` read by nobody by name) |
| 9_controle → redacteur | **BLOCKING ×2** (on a correction cycle the file lands in the feature's `code/` and overwrites the main cycle's; the working folder it gathers from is undefined) · TO FIX (`/8_code` says nothing runs after a bug-fix cycle, `/9_controle` says it runs on every one) · 1 NOTE |
| redacteur → fusionneur | TO FIX (`Genre:` and `Global:` lines have no fate on merge) · 2 NOTE |

**Agents where none of the three heading forms appears**: none. Every
agent of the twelve pairs carries `## Where you work` (lexicographe,
decoupeur, qualifieur, classeur, sondeur, assembleur, convertisseur,
cadreur, architecte) or an invocation table (redacteur L369-373,
sondeur L133-136, convertisseur L537-540, architecte L272-276,
fusionneur L247-251, cadreur L273-279) or `## What you read` /
`## What you write` (architecte L52, L95; decoupeur L177; qualifieur
L259; classeur L279; sondeur L266; assembleur L213). The
`## What you report` heading of decoupeur L218 and qualifieur L267 is
a fourth form, not listed in the brief — it holds no file, only the
reply.

---

## 1. lexicographe → redacteur

| | |
|---|---|
| **Writes** | `idees.md` settled (W `lexicographe.md` L389) · `lexique.md` with three sections `## Tranché` / `## Non tranché` / `## Relevé` (W L133-166, example L140-166) · `questions-lexicographe-NN.md`, entries `### Qn` / `Terms:` / `Question:` / `Answer:` (W L109, L294-298) |
| **Reads** | `idees.md` · `lexique.md` (R `redacteur.md` L371, L396-398) · writes back an `en anglais :` line on a `## Tranché` entry (R L163-170) |

**Section name** — `## Tranché`: W L140, L168 ↔ R L165. Identical.

**Entry shape** — W L141-142 `STATION — retenu` / `  remplace : atelier`
↔ R L167-169 same two lines, then `  en anglais : station`. W L155
shows `en anglais : closed segment` in the same position. Identical.

**Who owns the line** — W L176-180: *"The `en anglais` line is the
Rédacteur's, and his alone … You never write it, and you never touch
it"* ↔ R L308-310: *"Write anything in `lexique.md` but an `en anglais`
line — never an entry, never a term"*. Both sides agree; R L180-182 adds
*"you add no entry"*, matching W L184-186.

**The questions file** — W L294-298 carries `Terms:`, not `Block:`.
It never reaches the Rédacteur: `/2_structure` L44-52 files it into
`questions/lexicographe/` before choosing the invocation, and
`/1_lexique` L53-58 routes a `questions-lexicographe` file to
invocation 2 of the lexicographe. ✅.

**1-A — `redacteur.md` L123-125.** NOTE. *"Any other answered file —
your own, the qualifieur's, the classeur's, **the lexicographe's** —
means no turn ran."* The Rédacteur is told how to treat the
lexicographe's answered file, but no command ever names it one
(`/2_structure` L44-52 files it first). Dead branch, not a defect —
but if it ever ran, the file has no `Block:` line and pass a (L529-531,
*"Each answer goes to a block"*) would have nothing to key on.

**1-B — `redacteur.md` L163-165 against `lexicographe.md` L195-201,
L430-432.** NOTE. The Rédacteur writes `en anglais :` *"on its
`## Tranché` entry"*. A term that was swept and never questioned lives
in `## Relevé` only (W L195-197) and has no `## Tranché` entry, so no
line is ever written for it — while lexicographe invocation 3 counts on
that line to detect a second English rendering (W L430-432, *"an
`en anglais` line tells you the word the product file actually uses"*).
The guard covers only the terms that were once questioned.

---

## 2. redacteur → decoupeur

| | |
|---|---|
| **Writes** | Block heading `### B7 — <title>    MODIFIED` with `Genre:` / `Nature:` / `Global: ## <section>` directly under (W `redacteur.md` L59-62, L64-68, L75-80) · markers `NEW` / `MODIFIED` on the heading line (W L96-100) · `**Clarification needed:**` as the block's last line (W L462-466) |
| **Reads** | `^### B` for titles and ranges (R `decoupeur.md` L40-44) · `NEW` / `MODIFIED` named by the prompt (R L36-38, L147-149) · `**Clarification needed:**` stops it (R L48-51) · `Global:` carried onto every half (R L208-213) |

**Heading grep** — R L41 `^### B` ↔ W L59 `### B7 — …`. ✅.
`/3_decoupe` L76-77 greps `^### .*NEW` / `^### .*MODIFIED`, anchored
on the heading where W L96-100 puts the marker. ✅.

**Flag string** — W L465 `**Clarification needed:**` ↔ R L48
`**Clarification needed:**`. Identical, bold included.

**What the Découpeur writes back** — R L179-186: `Genre:` empty,
`Nature:` empty, `NEW`, `Global:` copied — the same four lines W L59-62
defines. The original keeps its number and takes `MODIFIED` (R L195-201)
— consistent with W L99-100.

**2-A — `redacteur.md` L563 and L574 against L64-66.** NOTE (internal to
the Rédacteur, but the Découpeur and the Qualifieur inherit it). The
general rule L64-66 says *"`Genre:` and `Nature:` empty on every block
you create — the original of a split included"*. Pass a's table L563
says *"a block of its own, with an empty `Nature:`"* and pass b step 3
L574 says *"Each block gets an empty `Nature:`, the original included"*
— `Genre:` is dropped from both. A Rédacteur following the pass text
leaves the original's `Genre:` filled after a split; `/3a_genre` L78-80
still names it through `MODIFIED`, so the Qualifieur re-derives it
(qualifieur L249-253) — the chain survives, the text does not agree
with itself.

---

## 3. decoupeur → qualifieur

| | |
|---|---|
| **Writes** | Halves with `Genre:` empty, `Nature:` empty, `NEW` (W `decoupeur.md` L179-186, L203-207); the original with `MODIFIED` (W L200) |
| **Reads** | Blocks *"whose `Genre:` line is empty, and those marked `MODIFIED`"* (R `qualifieur.md` L224-226); `/3a_genre` L77-79 greps `^Genre:$` and `MODIFIED` |

**Empty line** — W L203: *"Leave `Genre:` and `Nature:` empty on every
block you write"* — a line written as `Genre:` with nothing after it ↔
`/3a_genre` L77 `grep -B1 '^Genre:$'`, and L88-89 says exactly that:
*"the Rédacteur and the decoupeur write `Genre:` with nothing after
it, never omit it."* ✅.

**`-B1` lands on the heading** — W L179-181 puts `Genre:` directly
under `### B62 …`, so the line above the hit is the heading, as
`/3a_genre` L77 says. ✅ (compare 4-B below, where the same trick fails
for `Nature:`).

**Marker on the original** — W L200 `MODIFIED` ↔ `/3a_genre` L78
`MODIFIED`, and R L249 *"On a block marked `MODIFIED` whose line already
carries a genre"*. ✅.

No finding.

---

## 4. qualifieur → classeur

| | |
|---|---|
| **Writes** | *"In the product file, the `Genre:` line, and nothing else"* (W `qualifieur.md` L261); six values in the table W L48-56: `comportement` · `directive` · `transverse` · `référence` · `hors périmètre` · `recette` |
| **Reads** | *"Every block the prompt names carries `Genre: comportement`"* (R `classeur.md` L34-37); `/3b_nature` L78 keeps only `Genre: comportement`; `/4_grille` L106 `grep -B1 '^Genre: comportement$'`, L139 `'^Genre: transverse$'`; `/5_reclasse` L90 `grep -B1 '^Genre: <genre>$'`; `redacteur.md` L103 `Genre: transverse` |

**Value** — `comportement` (W L51) ↔ R L34, `/3b_nature` L78,
`/4_grille` L106. `transverse` (W L53) ↔ `/4_grille` L139, `redacteur.md`
L103. Identical strings.

**4-A — `qualifieur.md`, no line.** TO FIX. The Qualifieur has no rule
on the form of the line it writes. The Classeur has one (`classeur.md`
L52-60: *"`Nature: ` and the nature's name, spelled exactly as the
table spells it, lower case, nothing else on the line. Not
`Nature: Model`, not `Nature: external-exchange` …"*), and it exists
because three readers grep the exact string. The `Genre:` line has more
exact-string readers than `Nature:` — `/3b_nature` L78, `/4_grille`
L106 and L139 (both anchored `$`), `/5_reclasse` L90 (anchored `$`,
and L98-99 stops on a value outside the six), `classeur.md` L34 — and no
rule saying `Genre: comportement`, lower case, nothing after it. A
`Genre: Comportement` or `Genre: comportement (fires on tap)` drops the
block out of the grid, silently for the first (a block never named is a
block never probed, `sondeur.md` L54-56), noisily for `/5_reclasse`.
The Classeur's paragraph L52-60 should exist in the Qualifieur, for
`Genre:`, with the six spellings — accents (`référence`) and the space
in `hors périmètre` included, since `/5_reclasse` L90 greps them as
written in the table.

**4-B — `3b_nature.md` L77.** TO FIX. *"`grep -B1 '^Nature:$'` — the
blocks whose nature is empty — the line above each hit carries the
block."* It does not: W `redacteur.md` L59-62 and `decoupeur.md`
L179-181 put `Genre:` between the heading and `Nature:`, and
`classeur.md` L49-50 says so (*"`Genre:` and `Nature:` sit directly
under it"*). `-B1` returns the `Genre:` line, which is what L78 then
filters on — so the filter works, but the command never sees the
identifier it has to name in the prompt. `/4_grille` L87-88 uses the
same `-B1` and only filters, never names. `-B2` is what gives the
heading. Same command, same file: `/3a_genre` L77 `grep -B1
'^Genre:$'` is right, because `Genre:` sits directly under the heading.

**4-C — `3b_nature.md` L130-132 against `qualifieur.md` L58-59.** NOTE.
*"Grep `-c '^Nature:$'` in `desc-produit.md`. Zero is what you
expect."* But W L58-59: *"Only a `comportement` has a nature"* — every
`directive`, `transverse`, `référence`, `hors périmètre` and `recette`
block keeps its `Nature:` line empty for good (`redacteur.md` L64-68
writes it on every block, `classeur.md` L36-37 never touches those
blocks). The count is zero only on a feature with no block of another
genre; otherwise L131-132 reports *"a block was left unclassed"* and
L209 sends `/3b_nature` round again, every time. The check has to
filter on `Genre: comportement` as L77-78 does.

---

## 5. classeur → sondeur

| | |
|---|---|
| **Writes** | `Nature: <name>`, one of eight, lower case, exact spelling (W `classeur.md` L52-60, table L69-79): `model` · `persistence` · `calculation` · `transition` · `external exchange` · `synchronisation` · `presentation` · `access` |
| **Reads** | Blocks named by the prompt, every one `Genre: comportement` (R `sondeur.md` L47-52); the grid *"scopes [a question] to a nature the block does not carry"* (R L223-224); the third angle reads *"by nature"* (`/4_grille` L245-251) |

**Values** — the eight names of W L71-78 ↔
`docs-new/process/GRILLE_CADRAGE_PRODUIT_V2.md` L129-138 (`model`,
`persistence`, `calculation`, `transition`, `external exchange`,
`synchronisation`, `presentation`, `access`) ↔ `convertisseur.md`
L82-89 (same eight, same spelling, same order). Identical, the
British `synchronisation` and the space in `external exchange`
included. ✅.

**Gate before the sondeurs** — `/4_grille` L87-90 stops when a
`comportement` block has an empty `Nature:`, which is what W L57-60
(*"a line left empty would send the block back"*) and W L113-116
(*"Still write its `Nature:` line"*) guarantee. ✅.

**The record's identifiers** — not from the Classeur, but checked on
the way: `sondeur.md` L170-177 writes `A1.1`, `A1.2`, `A1.3`, `A1.4`,
`A1.9`, `A4` ↔ grid L264-274 lists `A1.1`–`A1.4`, `A1.9` and `A4`.
Identical.

No finding.

---

## 6. sondeur → assembleur

| | |
|---|---|
| **Writes** | `<out>/<your name>.md` (W `sondeur.md` L268-269), entries `### Qn` / `Block:` / `Question:` / `Answer:` (W L271-274); a *défaut* adds `Défaut: <proposal> — <what founds it>` between `Question:` and `Answer:` (W L279-287); `Block:` is identifiers comma-separated or `-` (W L303-309) |
| **Reads** | The files the prompt names, whole (R `assembleur.md` L88-92); shape `### Q1` / `Block:` / `Question:` / `Answer:` (R L103-108); `Block:` *"identifiers, comma-separated, or `-` — nothing else, ever"* (R L110-112); `Défaut:` *"between `Question:` and `Answer:`"* (R L114-120) |

**Field names** — `Block:` / `Question:` / `Défaut:` / `Answer:`, four
for four, same order, same accent on `Défaut`. ✅.

**`Block:` values** — W L305-307 `B7` · `B12, B15` · `-` ↔ R L110-112.
✅. R L138-140 stops on any other value — nothing in W produces one.

**File names** — W L268 *"where `<out>` and the name are the prompt's"*
↔ `/4_grille` L217-253 *"Write to docs/features/<name>/cadrage-produit/par-nature.md"* (and `par-bloc.md`, `par-question.md`, `global.md`), L262-263 the record to `releve.md`; the Assembleur is named the four at `/4_grille` L313-321. ✅.

**Empty file** — W L335-336 writes it even empty ↔ R L34-36 *"An empty
file is a sondeur that found nothing — it counts"*, R L126-127 *"a file
with no `### Q`"*. ✅.

No finding.

---

## 7. assembleur → redacteur

| | |
|---|---|
| **Writes** | `<out>/questions.md` (W `assembleur.md` L215), entries copied word for word, `Défaut:` travelling with its question (W L217-229), numbering restarted at `Q1` (W L231); *"nothing else in that file"* (W L237-238) |
| **Between** | `/4_grille` L342-347 copies `cadrage-produit/questions.md` byte for byte to `questions-sondeur-NN.md` at the root |
| **Reads** | *"the questions file the prompt names"* (R `redacteur.md` L372, L500-501); `Block:` to land each answer (R L529-531, L565-567); `Block: -` (R L289-290, L577-580); an entry *"marked défaut"* (R L539-542); strips markers because the file comes *"from the grid"* (R L118-121, L520-522) |

**Entry shape** — `### Qn` / `Block:` / `Question:` / `Answer:` ↔ R
L259-262 shows the same four lines as its own. ✅. Several identifiers
(W copies `B12, B15`) ↔ R L281 *"Several identifiers when the question
sits between blocks"*. ✅. `Block: -` ↔ R L289, L577. ✅.

**7-A — `2_structure.md` L94-95, `1_lexique.md` L70, `4_grille.md`
L97 against `sondeur.md` L279-290 and `assembleur.md` L114-120.**
**BLOCKING.** A *défaut* is, by design, an entry whose `Answer:` stays
empty: W `sondeur.md` L294-295 *"`Answer:` stays empty, as always.
Empty means the Product Owner accepts the proposal"*; the Assembleur
copies it so (W L228-229, L235). The Rédacteur is written for it
(R L539-542: *"No `Answer:` written means the Product Owner accepted it
— you integrate the proposed answer as if he had written it"*). But the
file never reaches it: `/1_lexique` L70 *"A file with an empty `Answer:`
→ stop"*, `/2_structure` L94-95 *"If it carries an empty `Answer:` —
stop, and say which questions are waiting"*, and `/4_grille` L97 on the
next turn. Every gate reads an accepted *défaut* as an unanswered
question. The turn cannot close unless the Product Owner writes an
answer into every *défaut* — which is exactly what the mechanism was
meant to spare (W `sondeur.md` L297-300). Already reported as BLOCKING
in `renommages.md` (summary, §A); this is the handover it breaks.
The gates need to skip an empty `Answer:` that follows a `Défaut:` line.

**7-B — `redacteur.md` L539.** TO FIX. *"An entry marked *défaut*
carries its own answer, with the paragraph that founds it."* The field
is `Défaut:` (W `sondeur.md` L286, `assembleur.md` L118); the Rédacteur
names it in italics, lower case, without the colon, and nowhere gives
the line's shape (`Défaut: <proposal> — <what founds it>`). A reader
that greps the entry for its fields finds `Block:`, `Question:`,
`Défaut:`, `Answer:` — and the instruction speaks of a mark it cannot
match. One word: *"An entry carrying a `Défaut:` line …"*.

**7-C — `redacteur.md` L118-121, L520-522.** NOTE. The strip-markers
rule keys on provenance — *"from the grid or from the conversion"* —
and the only signal the Rédacteur has is the prefix of the file the
prompt names (`questions-<agent>-NN.md`, L35). The prefixes in play are
`sondeur`, `existant`, `convertisseur`, `qualifieur`, `classeur`,
`redacteur`; L123-125 lists the four that mean *"strip nothing"* by
agent name, but never says that `sondeur` and `existant` are *"the
grid"* and `convertisseur` *"the conversion"*. `existant` in particular
(`/4_grille` L184, the second time) is a grid file whose name says
nothing about the grid. A two-line table, prefix → strip or not, closes
it.

---

## 8. redacteur → convertisseur

| | |
|---|---|
| **Writes** | `desc-produit.md` — blocks with `Nature:` (W `redacteur.md` L59-62), `Global:` (W L75-80), headings `# Application` / `# Domaine : <nom>` / `## <Section>` / `### <Bloc>` (W L41-46) |
| **Between** | `/5_reclasse` L78-99 splits by `Genre:` into `par-genre/{comportements,transverses,directives,references,hors-perimetre,recette}.md`, L111-125 builds `desc-par-nature.md` from `comportements.md`; `/6_convertit` L115-141 copies each nature's part to `convertisseur/<nature>-input.md` |
| **Reads** | `convertisseur/<nature>-input.md`, `par-genre/transverses.md`, `par-genre/references.md` (inv. 2), `par-genre/hors-perimetre.md` (inv. 2), the product file's headings by grep (R `convertisseur.md` L48-62); *"A block's nature is on its `Nature:` line — the classeur wrote it; read it, never derive it again"* (R L74-76) |

**File names** — R L50 `par-genre/transverses.md` ↔ `/5_reclasse` L84;
R L51 `references.md` ↔ L86; R L52 `hors-perimetre.md` ↔ L87. Identical,
including the unaccented `hors-perimetre` for the genre `hors
périmètre`. ✅. R L49 `<nature>-input.md` ↔ `/6_convertit` L123, L141.
✅. R L65-66 `<nature>` = the name with a hyphen for the space
(`external-exchange`) ↔ `/6_convertit` L118 `convertisseur/external-exchange.md`.
✅.

**Block copy** — `/5_reclasse` L90-91 copies each block *"from its
`### B` line to the next heading of any level"*, so the Convertisseur's
input carries the heading, `Genre:`, `Nature:` and `Global:` lines. R
L74-76 reads `Nature:` from it. ✅.

**The way back** — R L343-347 writes `### Qn` / `Block:` / `Question:` /
`Answer:` (*"The Rédacteur integrates by block"*, L351-352); `/6_convertit`
L277-284 merges the nature files and `questions-transversal.md` into
`questions-convertisseur-NN.md`, copied as written; the Rédacteur reads
it at invocation 2 as *"from the conversion"* (L119-121). Shape
identical to the Rédacteur's own L259-262. ✅.

**8-A — `convertisseur.md` L110-112 against `redacteur.md` L41-46.**
NOTE. The preamble's first part, *"Intent, vocabulary — the product
file's text outside the blocks"*, has no writer: the Rédacteur's
structure L41-46 has headings and blocks and nothing between them
(invocation 1 files every subject as a block, L441-443). The part will
be written empty every time (R L128-129 allows it). Harmless, but the
Convertisseur's invocation 2 reads *"the product file, its text outside
the blocks"* (L540) for nothing.

**8-B — `convertisseur.md` L292-298, L318-325.** NOTE (cross-reference).
The technical question file `convertisseur/technique-<nature>.md`
(shape `Entries:` / `Question:` / `Answer:`, *"no `Block:`"*) *"comes
back to you, and to nobody else"* — and `/6_convertit` L277-284 merges
*"the natures in section order, then `questions-transversal.md`"*,
never a `technique-*.md`; no other command greps the name. Reported as
BLOCKING in `renommages.md` (summary, §A) — not re-counted here. It is
worth saying that its shape is right *not* to be merged: an `Entries:`
line with no `Block:` would stop the Assembleur (L138-140) and give the
Rédacteur's pass a nothing to land on.

---

## 9. convertisseur → architecte

| | |
|---|---|
| **Writes** | `spec-technique.md` — `# Preamble` with `## Intent and vocabulary` / `## Out of scope` / `## Cross-cutting rules` / `## Dependencies` (W `convertisseur.md` L119-127), then `## §1` … `## §9` with `### §n.m` entries (W L155-172, L176-178) · `tracabilite.md`: `B1   Race segment structure          §1.1`, one line per block in file order, `—` when none (W L672-687) |
| **Between** | `/5_reclasse` L85 writes `par-genre/directives.md` for the Architecte |
| **Reads** | `desc-produit.md` whole · `spec-technique.md` whole, *"preamble included"* · `tracabilite.md` for move 2 · `par-genre/directives.md` · the grid (R `architecte.md` L274); move 2: *"`tracabilite.md` … holds that correspondence — one line per product block, the entries carrying its rules after it"* (R L335-339); *"A block whose line carries a dash, or an entry that line names nowhere, is a question"* (R L341-343); `couverture.md` *"one line per entry of the technical document"* — `§1.1   model   → R12` (R L146-151) |

**`tracabilite.md`** — W L672-676 identifier, title, entries, dash ↔ R
L337-343 reads exactly that: one line per block, entries after it, a
dash. ✅. R L345-346 handles its absence.

**Entry identifiers** — W L176-178 `§3`, then `§3.1` ↔ R L148-151
`§1.1`, `§2.5` in `couverture.md`'s first column, and R L383-385 checks
every identifier appears once. ✅.

**Section-to-nature** — R L154 *"The second column is the entry's
nature, as the technical document's section carries it"* ↔ W L80-88
one section per nature, nature named in the table. ✅ (§9 Text carries
none, W L90; the coverage line for a §9 entry has no defined second
column — a gap of one cell, not raised).

**Directives** — R L274 `par-genre/directives.md` ↔ `/5_reclasse` L85.
✅.

**9-A — `architecte.md` L446-453.** NOTE (adjacent, not this pair). The
Architecte's questions file is `questions-architecte-NN.md` at the
working folder's root, with `Block: §3.2 — Reconciling two real
entries` — an entry number, a dash and a title on the line every other
agent restricts to identifiers (`redacteur.md` L277-279, `assembleur.md`
L110-112). It is meant for the Architecte's own invocation 2
(`/conventions` L72) and never for the Rédacteur — but it sits at the
feature root under the `questions-<agent>-NN.md` name that
`/2_structure` L83 treats as *"One, any prefix → 2 — Integrating"*, and
that `/3a_genre` L64-66, `/4_grille` L362-364 and `/6_convertit` L74
`git mv` away into `questions/<agent>/`, where `/conventions` L35, L57
no longer looks for it. Paths investigation's matter; flagged here
because its `Block:` value would break the Rédacteur's pass a if it ever
reached it.

---

## 10. convertisseur → cadreur

| | |
|---|---|
| **Writes** | as §9 above; plus `Consumes:` as the last line of every entry, `—` when nothing (W `convertisseur.md` L223-233, L574-575); `<<ASSUMED B40: …>>` on one line (W L384-391); an unresolved reference `[B12: …]` or `[B?: …]` left in brackets (W L241-249, L261-267, L642-645) |
| **Reads** | `spec-technique.md` *"in full, preamble first"*, its `Out of scope` (R `cadreur.md` L347-349, L377-378); stops on `<<ASSUMED` (R L118, L372-374), on unnumbered sections (R L117); cuts by section §1–§9 (R L419-426) |

**Section names** — R L419-426 `§1 Model` … `§9 Text` ↔ W L80-88 same
nine titles, same numbers. ✅.

**Preamble heading** — W L124 `## Out of scope` ↔ R L349, L378 `Out of
scope`. ✅ (the `##` is not quoted by the reader, but the name is).

**`<<ASSUMED`** — W L384-386 `<<ASSUMED B40: …>>` ↔ R L372 `<<ASSUMED`.
✅.

**Numbering** — W L176-178 ↔ R L117 *"A document whose sections are not
numbered"* stops, R L63-64, L218 *"never a bare `§3`"*. ✅.

**10-A — `cadreur.md` L114-125 against `convertisseur.md` L261-267.**
TO FIX. The Convertisseur leaves a reference it cannot resolve in
brackets on purpose — `[B?: the weigh-in screen]` (W L261-264), or a
`[B12: …]` whose block gave several entries and none carrying what is
expected (W L642-645) — and says why: *"the command's grep for `[B`
would never see it, and the Cadreur would read it as settled"* (W
L266-267). The Cadreur's stop list L114-125 has `<<ASSUMED` (L118) and
not `[B`; its move 1 (L372) greps `<<ASSUMED` alone. `/6_convertit`
L261-265 greps `[B` after invocation 2 and either rerolls once or calls
it a question — but a question is answered on a later turn, and
`/7_lots` (L23, L93-125) checks neither `[B` nor `<<ASSUMED` before
invoking the Cadreur. So a `[B?: …]` left beside an open question is
exactly the case the Convertisseur warned about: the Cadreur reads
past it. One more line in L114-125 — *"A document still carrying a
`[B` reference"* — and one more grep at move 1.

**10-B — `convertisseur.md` L223-236.** NOTE. *"`Consumes:` — the last
line of every entry … This is what gives the direction of dependencies.
A screen showing a computed value never copies the rule — without the
line, nothing ties them."* No downstream agent names the line: the
Cadreur (grep clean) derives `Needs` / `Produces` / `Modifies` from the
code by grep (L347-353, L710-715), the Vérificateur, Détailleur,
Concepteur, Réalisateur and Relecteur do not mention it; the only other
occurrence in the chain is `architecte.md` L437, which says the graph
*"does not exist yet when [the framing] grid runs"*. Written on every
entry, read by the Cadreur only as prose inside *"in full"*.

**10-C — `convertisseur.md` L125, L143.** NOTE. `## Cross-cutting
rules` — *"without the constraint, nothing says which entries are bound
by it"* (W L151-152) — is read by nobody by name (grep clean across
agents and commands; `## Dependencies` hits in `concepteur.md` L55 and
`detailleur.md` L247 are the sheet's own section). The Cadreur reads the
preamble whole and cites `Out of scope` alone.

---

## 11. 9_controle → redacteur — never exercised

| | |
|---|---|
| **Writes** | `code/decisions-produit.md` — *"one decision per line, with the block it bears on when the file names one"*, gathered from *"the `blocked_<agent>-NN.md` files of the working folder"*, *"every `## Decision` that settles what the application does"* (W `9_controle.md` L200-203, L219-221, written at L227-228, *"The Rédacteur reads it at `/fusion`, invocation 3"* L230-231); *"One file per cycle, for the Rédacteur"* (W L43); *"It runs on the main cycle and on every correction cycle"* (W L45); *"Always the feature folder itself, never a `bugfix-NN/` … Every path below is relative to it"* (W L17-21); relayed as `code/decisions-produit.md` (W L281) |
| **Between** | `/fusion` L49, L58-66: row 10, *"Name it every `code/decisions-produit.md` that `/9_controle` produced, in cycle order — the feature's own first, then `bugfix-01`, then `bugfix-02`"* |
| **Reads** | *"`desc-produit.md`, and every decisions file the prompt names — in the order it names them: the feature's own, then `bugfix-01`'s, then `bugfix-02`'s"* (R `redacteur.md` L634-637); folds each into a copy, *"a later cycle that revised what an earlier one decided wins"* (R L651-652); lands a decision *"read against the title list, as pass a does"* (R L658-661); writes `desc-produit-fusion.md` (R L639-640, L670) |

**Name of the file** — W L227, L281 `code/decisions-produit.md` ↔
`/fusion` L64 `code/decisions-produit.md`. Identical. The Rédacteur
itself names no file: it takes *"every decisions file the prompt
names"* (R L634) — consistent with `/fusion` naming them.

**Shape** — W L227-228 gives no format beyond *"one decision per line"*;
R L658-661 reads each decision as prose against the title list. Nothing
to mismatch: the reader keys on nothing. ✅ as a handover — see 11-D
for what that costs.

**11-A — `9_controle.md` L17-21 against L43-45, L227, and `fusion.md`
L64-66.** **BLOCKING.** Three lines of `/9_controle` cannot all hold:
L45 *"It runs on the main cycle and on every correction cycle"*, L43
*"One file per cycle"*, and L17-21 *"Always the feature folder itself,
never a `bugfix-NN/` … Every path below is relative to it"*. The
command's only argument is the feature name (L4 `argument-hint:
"<feature folder name>"`, L12-13). Run after `bugfix-01`, it writes
`docs/features/<name>/code/decisions-produit.md` — the same path the
main cycle wrote — and overwrites the feature's own decisions with the
correction cycle's. `/fusion` L64-66 then names *"the feature's own
first, then `bugfix-01`"* — two files, of which only one path exists,
carrying only the last cycle's content. The Rédacteur (R L634-637) is
named a `bugfix-01/code/decisions-produit.md` nobody wrote, and folds a
`code/decisions-produit.md` that no longer holds the feature's own
decisions. Nothing in `redacteur.md` says what it does when a named
decisions file is missing. Compare `/8_code` L25-32, which resolves
*"the working folder is the highest `bugfix-NN/` in it, if there is
one"* and makes every path relative to that — the rule `/9_controle`
needs for phases 5 and 6.

**11-B — `9_controle.md` L200-203, L219-221.** **BLOCKING** (same root
as 11-A, distinct effect). Phase 5 gathers *"the product questions the
Arbitre handed back, in the `blocked_<agent>-NN.md` files of the working
folder"* and phase 6 *"from the `blocked_<agent>-NN.md` files"*. The
command never defines *"the working folder"* — L17-21 says every path
is the feature folder's, and on a correction cycle (L52-53 *"phases 1 to
3 do not run. The other two deliverables do"*) the blocking files it
must gather sit under `bugfix-NN/code/<lot>/` (`detailleur.md` L278,
`realisateur.md` L276, L464: `code/<lot>/blocked_<agent>-NN.md`). Read
literally, a correction-cycle run gathers the feature cycle's files
again and writes them as the correction cycle's decisions. Read
charitably, it has no way to pick the `bugfix-NN/`. Either way, the
decisions of a correction cycle — *"On a correction cycle it is the
only route the product has at all"*, R `redacteur.md` L631-632 — never
reach `desc-produit-fusion.md`. Also: no glob depth. `blocked_<agent>-NN.md`
files live one level down (`code/<lot>/`) for the Détailleur and the
Réalisateur and at `code/` for the Cadreur (`cadreur.md` L108); the
phrase *"of the working folder"* reads as the root.

**11-C — `8_code.md` L190-193 against `9_controle.md` L45.** TO FIX.
`/8_code`, at the end of a bug-fix cycle: *"On a bug-fix cycle — the
working folder carries `desc-bug.md` — nothing comes next: the
Contrôleur compares the product file to the sheets, and there is none
here."* `/9_controle` L45-53: it runs on every correction cycle, the
Contrôleur alone does not, phases 4 to 6 do. The Product Owner is told
by one command that nothing follows, by the other that a file the
Rédacteur will need at `/fusion` is still to be produced. `/8_code`
L190 should say `/9_controle` comes next on both cycles, since L45 is
what `/fusion` L64-66 relies on.

**11-D — `9_controle.md` L227-228 against `arbitre.md` L145-157 and
`detailleur.md` L287-299.** NOTE. *"one decision per line, with the
block it bears on when the file names one"*. A blocking file's
headings are `## What blocks` / `## Where` / `## To resume` /
`## Decision` (`detailleur.md` L287-299), and `## Where` is *"the lot,
section or file"* — a `§` entry or a lot, never a `B` identifier; the
Arbitre's `## Decision` (L150-157) is three prose parts, no field. So
*"when the file names one"* is *never*, and every line of
`decisions-produit.md` reaches the Rédacteur without a block. R
L658-661 copes — it reads each against the title list — but the
Rédacteur is told at L636 the files arrive *"in cycle order"* and at
L651-652 to let a later cycle *"win"* over an earlier decision on the
same point; with no block on the line, *"the same point"* is a
judgement on prose across two files. A `§` entry on the line (which
`## Where` does carry) would let `tracabilite.md` map it to a block.
Pending 11-A, moot.

---

## 12. redacteur → fusionneur

| | |
|---|---|
| **Writes** | `desc-produit-fusion.md` — a copy of `desc-produit.md` with decisions folded in, *"no `NEW`, no `MODIFIED`"* (W `redacteur.md` L639-640, L663-664), written even with nothing to fold (W L666-668); blocks keep `### B<n> — <title>`, `Genre:`, `Nature:`, `Global:` (W L59-62 — nothing in invocation 3 strips them) |
| **Reads** | *"the product file — `desc-produit-fusion.md`, never `desc-produit.md`"* (R `fusionneur.md` L44-46); *"The final product file"* (R L249); locates by section title, block title, sentence (R L316-322); on `INIT` *"Drop … the block numbers, the `NEW` markers, and its own `# Application`. The `Nature:` lines stay"* (R L377-380); *"Never carry a block's number or its `NEW` marker into the global"* (R L418-419) |

**File name** — W L639 `desc-produit-fusion.md` ↔ R L45. Identical.
`/fusion` L49 row 10 runs the Rédacteur when it is absent, L58-59
*"once, before the merge ever starts"*. ✅.

**Markers** — W L663-664 strips both ↔ R L378, L418 expect none. ✅
(R names `NEW` only; `MODIFIED` is gone by W L663 anyway).

**Structure** — W L41-46 `# Application` / `# Domaine : <nom>` /
`## <Section>` / `### <Bloc>` ↔ R L74-80 *"identical to the feature
file's"*, same four lines. ✅.

**12-A — `fusionneur.md` L377-380 against `redacteur.md` L59-62,
L75-80.** TO FIX. On `INIT` the Fusionneur drops three things — numbers,
`NEW`, `# Application` — and keeps `Nature:`. Every block also carries
`Genre:` (W L59-62) and, when attached, `Global: ## <section>` (W
L75-80). Neither is named. `Genre:` is harmless if it stays, and
possibly useful. `Global:` is not: it *"names the section of the global
this block attaches to"* (W L75) — inside the global it points at
itself, and the Rédacteur's next feature reads the global by its
`^#` index (W L135-136) and *"grep[s] the index to file the block"* (W
L77), so a `Global:` line that survived a merge is noise at best and a
false attachment at worst. On a non-`INIT` merge (R L389-411, targeted
edits sentence by sentence) the lines are never mentioned, so a newly
inserted section carries whatever the Fusionneur copied. Two words at
L378: *"the `Genre:` and `Global:` lines"* — kept or dropped, but said.

**12-B — `fusionneur.md` L299-301.** NOTE. *"Skip the product file's
closing section — `## Questions set aside`, or `## Gaps set aside` on a
bug-fix cycle."* `## Questions set aside` has no writer in the chain
(grep clean across agents and commands); `## Gaps set aside` is written
by the Diagnostiqueur into `desc-bug.md` (`diagnostiqueur.md` L527),
which the Fusionneur never reads (R L249-251: invocation 3 reads
`bug-list.md`, not `desc-bug.md`). Stale instruction, no effect.

**12-C — `fusionneur.md` L27-32 against `redacteur.md` L625-632.** NOTE.
The Fusionneur's own account of when it runs — *"Rédacteur → product
file → conversion → questions file fully answered → merge"* — omits the
step that produces its input: the Rédacteur's invocation 3, which
`/fusion` L49-59 runs before anything else. The table L44-46 has the
right file; the sentence above it describes the old route.

---

## Summary by severity

**BLOCKING (3)**

| # | Where | What |
|---|---|---|
| 7-A | `2_structure.md` L94-95 · `1_lexique.md` L70 · `4_grille.md` L97 | An accepted `Défaut:` has an empty `Answer:` by design (`sondeur.md` L294-295); every gate before the Rédacteur stops on it. The Rédacteur's rule for it (L539-542) is unreachable. (Also in `renommages.md`.) |
| 11-A | `9_controle.md` L17-21 vs L43-45, L227 · `fusion.md` L64-66 | On a correction cycle `code/decisions-produit.md` is written into the feature folder, overwriting the main cycle's; the `bugfix-NN/code/decisions-produit.md` that `/fusion` names to the Rédacteur is never written. |
| 11-B | `9_controle.md` L200-203, L219-221 | *"the working folder"* is undefined in a command whose every path is the feature folder's; the blocking files of a correction cycle (`bugfix-NN/code/<lot>/blocked_*-NN.md`) are out of its reach, and no glob depth is given. |

**TO FIX (7)**

| # | Where | What |
|---|---|---|
| 4-A | `qualifieur.md` (absent) | No form-of-the-line rule for `Genre:`; five exact-string readers (`3b_nature` L78, `4_grille` L106, L139, `5_reclasse` L90, `classeur` L34). The Classeur's L52-60 is the model. |
| 4-B | `3b_nature.md` L77 | `grep -B1 '^Nature:$'` returns the `Genre:` line, not the heading; `-B2` is needed to name the block. |
| 7-B | `redacteur.md` L539 | *"marked *défaut*"* — the field is `Défaut:`; its shape is never given. |
| 10-A | `cadreur.md` L114-125, L372 | `[B` is not a stop; the Convertisseur (L266-267) leaves `[B?: …]` precisely so that it is. `/7_lots` checks neither `[B` nor `<<ASSUMED`. |
| 11-C | `8_code.md` L190-193 vs `9_controle.md` L45 | *"nothing comes next"* after a bug-fix cycle, against *"runs on every correction cycle"*. |
| 12-A | `fusionneur.md` L377-380 | `Genre:` and `Global:` lines have no fate on merge; `Global:` inside the global is a self-reference the next Rédacteur can misread. |
| 4-C | `3b_nature.md` L130-132 | `grep -c '^Nature:$'` expects zero; non-`comportement` blocks keep an empty `Nature:` for good, so the check fails on any feature that has one and L209 loops. |

**NOTE (12)**: 1-A, 1-B, 2-A, 7-C, 8-A, 8-B (cross-ref), 9-A, 10-B,
10-C, 11-D, 12-B, 12-C.

**Matches confirmed, character for character**: `## Tranché` and the
`en anglais :` line (lexicographe ↔ redacteur) · `**Clarification
needed:**` (redacteur ↔ decoupeur, ↔ `/3_decoupe` L44, `/3a_genre`
L58) · `Genre:` / `Nature:` / `Global:` under `### B<n> —` (redacteur ↔
decoupeur ↔ qualifieur ↔ classeur) · `Genre: comportement` and `Genre:
transverse` (qualifieur ↔ classeur, sondeur, `/4_grille`, `/5_reclasse`,
redacteur) · the eight nature names (classeur ↔ grid ↔ convertisseur) ·
`A1.1`–`A1.4`, `A1.9`, `A4` (sondeur ↔ grid) · `### Qn` / `Block:` /
`Question:` / `Défaut:` / `Answer:` (sondeur ↔ assembleur ↔ redacteur ↔
convertisseur) · `par-genre/{transverses,references,hors-perimetre,directives,recette}.md`
(`/5_reclasse` ↔ convertisseur, architecte, `/9_controle`) ·
`convertisseur/<nature>-input.md` with `external-exchange` (`/6_convertit`
↔ convertisseur) · `§1 Model` … `§9 Text`, `§n.m`, `## Out of scope`,
`<<ASSUMED` (convertisseur ↔ cadreur) · `tracabilite.md` line shape
(convertisseur ↔ architecte ↔ `/9_controle` phase 1) ·
`code/decisions-produit.md` (`/9_controle` ↔ `/fusion`) ·
`desc-produit-fusion.md` and the four-level structure (redacteur ↔
fusionneur).
