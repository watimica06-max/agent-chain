# Vérification — transfer from `sujets.md` to `modifications.md`

Read: `docs/refonte/sujets.md` (2334 lines) and
`docs/refonte/modifications.md` (1629 lines), both whole. For every
heading of `sujets.md` — A1–A7, C1–C5, Rupture 3/5/6, F1–F3, U1–U14 and
A-1…A-8, D1–D24, P1–P14, Q1–Q24 — the questions were: settled or
discarded; if settled, carried by `modifications.md`; if carried, does
the demand match the decision. Matching is by meaning:
`modifications.md` almost never cites an identifier.

Summary: **57 subjects examined — 26 settled with something to pass,
19 discarded, 12 already corrected in the chain or with nothing to
pass.** Found — **2 LOST** (the grid *knowing not to re-ask the
out-of-scope* · the *push justification* in the orchestrator's
instructions) · **1 DISTORTED, narrow** (a directive *"ne reçoit jamais
de question"*, yet the Architecte asks one when it cannot place it
unchanged) · **0 DISCARDED BUT APPLIED** · **4 notes** (one demand
carried but marked *not done* under a header saying *"Tout est fait"*;
an internal tension of `sujets.md` that `modifications.md` resolved one
way; a wording tension "three things / four files"; three open checks
never closed).

---

## LOST — settled in `sujets.md`, absent from `modifications.md`

### L-1 · A1 — the grid knows not to re-ask what the Product Owner discarded

**`sujets.md`, `## A1 · Le genre d'un passage du fichier d'idées`.**
Settled three times over:

- L69, the six-genres table: *« **hors périmètre** | Ce que le Product
  Owner écarte | Le préambule — 📌 **et la grille sait ne pas le
  redemander** »*
- L124-126, *« Où le geste se place — tranché »*: *« 🔴 **Le genre avant
  les Sondeurs** : la grille ne sonde que les comportements, charge les
  transverses en contexte (A7), et sait ne pas redemander le
  hors-périmètre. »*
- L217, *« Ce que ça change »*: *« `.claude/agents/sondeur.md` ·
  `commands/4_grille.md` | Ne sondent que les comportements ; 🔴
  **chargent le fichier des transverses en contexte** ; savent ne pas
  redemander le hors-périmètre »*

`sujets.md` itself flags the *how* as open — L92-95: *« la grille
redemande aujourd'hui ce que le Product Owner a déjà écarté (C1.2), donc
il répond deux fois. ⚠️ **Le mécanisme reste à trouver** — 🔴 **pas une
case par question** : voir C5. »* — but the *what* is in the settled
table, alongside the two other Sondeur duties that were passed.

**`modifications.md`.** Nothing. The Sondeur section (L339-467) lists
*« les cinq modifications »*: (1) only `comportement` blocks, (2)
transverses in context, (3) a `Défaut:` with its citation, (4) two
diverging rules, (5) the global at time 2. The `4_grille.md` section
(L1335-1343) has *« Deux greps sur `Genre:` … les `comportement` à
sonder, et les `transverse` à charger en contexte »* — no third grep,
no mention of `hors périmètre`. The `5_reclasse.md` table (L1369) routes
the out-of-scope file to *« Le Convertisseur — préambule »* only. The
Sondeur therefore still sees neither the `hors périmètre` blocks nor
the preamble, and C1.2 of the grid still fires on them.

### L-2 · D24 — the push justification in the orchestrator's instructions

**`sujets.md`, `## D24 · Le push, dans le merge ou occasionnel`**
(L2217-2237). Status *« Tranché »*:

> *« ✅ **Confirmé par le Product Owner** : 🔴 **commit, merge, push, dans
> cet ordre, le plus souvent possible** … 📌 **`HEAD` local reste la
> bonne référence** — ⚠️ **mais pour la raison inverse de celle qui est
> écrite** : il est fiable **parce que** tout est poussé, non parce que
> pousser serait occasionnel. 🔴 **Seule la justification est à
> ajuster**, dans les instructions d'orchestration — hors de la
> chaîne. »*

**`modifications.md`.** Nothing. Its only `CLAUDE.md` entry (L1516-1519)
is *« L'inventaire : les agents et les commandes, avec le Qualifieur, le
Concepteur et le Testeur »*; the Qualifieur table (L58) adds *« liste
des `subagent_type` »*. No file section mentions the push. And the
current `.claude/CLAUDE.md` at `HEAD` still carries the wording D24
overturned, L6-8: *« Local `HEAD` is the reference … It sits several
commits behind: pushing is occasional. »*

`sujets.md` says *« hors de la chaîne »*, and `modifications.md` is
*« une section par fichier de la chaîne »* — which is probably why it
was never listed. It is nonetheless a settled change with no trace
anywhere.

---

## DISTORTED — present, but asking for something other than what was decided

### X-1 · A1 — a directive *« ne reçoit jamais de question »*, yet the Architecte asks one

**`sujets.md`, A1, L77-79:**

> *« **Directive** — elle atteint l'Architecte sans passer par le
> découpage en blocs, et 🔴 **ne reçoit jamais de question**. ⚠️ **La
> contrepartie est pour le Product Owner** : une directive qu'il juge
> fausse, il la change lui-même — personne ne la discutera. »*

**`modifications.md`, `architecte.md` · La demande · 1**, L715-717:

> *« 🔴 **Il ne reformule pas ce que le Product Owner a tranché.** 📌
> **Il place, il fusionne, il identifie — il ne réécrit pas.** ⚠️ **S'il
> ne peut pas placer une directive sans la changer, c'est une
> question.** »*

The two agree on everything else — L636 *« jamais questionné, et ses
mots l'emportent en cas de fusion »*, L709 *« Une règle la contredit →
La directive gagne — et il le dit »*. The distortion is narrow: the
question is about *placement*, and exists so the Architecte does not
silently rewrite what it cannot fit. But it is a question addressed to
the Product Owner on a directive, which A1 rules out without exception
— *« personne ne la discutera »*. To be settled: is *"I cannot place it
without changing it"* an allowed exception, or must the Architecte
place it verbatim and say so in its report instead?

---

## DISCARDED BUT APPLIED — discarded in `sujets.md`, yet carried

None found. Checked each discard against the pass sheets and the
demands:

| Discarded | What could have reintroduced it | Result |
|---|---|---|
| **C4** units of the idea file | — | Nothing splits `idees.md` |
| **C1** no global technical document | — | `spec-technique.md` untouched |
| **C3** loss control idea file → product file | Découpeur C17 *« Comparer le fichier produit entre deux tours »* | Écarté as P5, L320 — consistent. The `/5_reclasse` count (L1379) is A1's product-file count, not an idea-file coverage |
| **C5** the per-class record | Sondeur C7 *« "Ne s'applique pas" n'avait aucun test »* | Adds a criterion, not a form to fill — consistent |
| **C2** lots by behaviour | — | Nothing |
| **Rupture 3** loops without a cap | A-6, U11 | `sujets.md` itself reopens it there; applied as settled |
| **Rupture 6** cost 3, the global pass | Sondeur C17 *« Une reprise après blocage n'invoque que la lecture bloquée »* | A resume optimisation, not a kept record — consistent with *« Rien dans les fichiers »* |
| **F2** conventions from the code | Arbitre *« un piège de plateforme → `## Traps`, qu'il écrit lui-même »* | A trap, not a rule; conventions still written by the Architecte only (L1284) |
| **F3** the twenty-minute poll | — | Arbitre unchanged on it |
| **U1** a bound on the Lexicographe | Lexicographe C16 / C17 | Écarté / reporté, L37-38 — consistent |
| **U5** the grid turn | — | Nothing forces a turn on an unchanged file |
| **U14** `N` as a loop bound | `8_code` *« compteur de tentatives sur disque »* | That is A-3's three retries, already in the chain |
| **D3 · D4** a `MODIFIED` detector | Découpeur C17 | Écarté — consistent |
| **D6** the global pass redone | — | No angle writes the record |
| **D19** tests replayed | Relecteur point 4 *« que le module compile est prouvé par l'exécution »* | Lighter, not a third run — consistent |
| **D16** lot under the old rule | — | Only the `audit_conventions` line, as decided |
| **D1, D2, D7, D8, D9, D18** | — | Nothing |
| **P3, P5, P6, P8, P12, P13** | Contrôleur C14 *« Faire l'assemblage par un script »* écarté | Consistent with the P8 rule *« on scripte un geste mécanique dont une erreur coûte cher »*; `/5_reclasse` scripts a count, which is that case |

---

## Also observed — not one of the three classes

### N-1 · D14 modification 1 is carried but marked *not done*, under *« Tout est fait »*

`sujets.md` D14, L1951: *« 🔴 **Retirer les 34 entrées porte ouverte**,
garder les 36. 📌 **Archiver les retirées** … »* — settled.

`modifications.md` carries the demand (L1530-1545, identical wording)
but the *« Reprise par fichier »* table says, L1619: *« `GRILLE_CONVENTIONS.md`
| 🔴 **Retirer les 34 entrées porte ouverte**, archiver »* — no check
mark. The file's header, L3: *« 📌 **Tout est fait.** »*. One of the two
is wrong. Same situation for `PROCESS_AMONT.md` · `PROCESS_AVAL.md`,
L1625: *« 🔴 **Tout** — à faire en dernier »* — every `docs/process/`
line of every *« Ce que ça change »* table in `sujets.md` is pending,
and that is stated, so it is not lost; but it is not *« fait »* either.

### N-2 · A1 — *the transverses file* vs *a grep on `Genre:`*: `sujets.md` says both, `modifications.md` picked one

`sujets.md` A1 says, in the settled table L217: *« chargent **le
fichier des transverses** en contexte »* — and at L150: *« Les
transverses | ⚠️ **Les Sondeurs aussi** — en contexte »*, the files
being those of the partage. But the same section says the partage runs
*after* the loop: L67 *« nommée aux Sondeurs pendant la boucle *(la
commande grepe `Genre:`)*, partagée au Convertisseur après »*, L139-140
*« Partager en N fichiers — 🔴 après la boucle de la grille, quand le
fichier produit est figé »*.

`modifications.md` resolves it the second way — Sondeur L369-372: *« 🔴
**Il lit `desc-produit.md`**, jamais un fichier de partage : **le partage
tourne après la boucle** »*; `5_reclasse` L1372-1374: *« ⚠️ **Pas les
Sondeurs** — 🔴 **le partage tourne après leur boucle.** »*. This is
the only reading under which the sequence at L111-118 holds. Not a
distortion — the internal tension is in `sujets.md`, at L150 and L217.

### N-3 · A5 — *« trois choses, et rien d'autre »* vs *« les quatre fichiers »*

`sujets.md` A5, L540-543: *« 🔴 **Elle rend trois choses au Product
Owner, et rien d'autre** : la recette manuelle ordonnée (A4), ce
registre, et les décisions produit … ⚠️ **Sans cette limite, elle
deviendrait un orchestrateur déguisé.** »*

`modifications.md` `9_controle.md`, L1456: *« **Son relais** | 📌 **Les
quatre fichiers, par nom** »* — the Contrôleur's report being the
fourth, which the command already returned before A5. The demand at
L1462 keeps *« trois choses … et rien d'autre »*. Wording only; the
limit A5 draws is against orchestrating, which the command does not do.

### N-4 · Three checks `sujets.md` left open and nothing closed

Not settled, so not LOST — listed because nothing in `modifications.md`
says they were looked at:

| Where | The check | What `modifications.md` says |
|---|---|---|
| A1, L174-175 | *« **La langue** — une recette rendue au Product Owner aura été traduite en anglais par le Rédacteur »* | Nothing. The `en anglais` line (Rédacteur #4, L205-247) is about the lexicon, not about handing the `recette` file back in the Product Owner's language |
| A2, L308-312 | *« 🔴 **Le Cadreur grepe déjà le code** — **à vérifier quand on instruira l'aval** : le fait-il assez tôt ? »* | Cadreur, L941: *« aucune modification du fichier de travail »*; nothing says the check was made |
| A3, L395-397 · A4 | *« Chiffre à confirmer au premier cycle »* — and D10 L1843-1847, GRILLE_EXISTANT L477-479 | Deferred to the first cycle in both files, by design |

The other two A1 checks were closed: *« Le Découpeur face à un bloc sans
déclencheur »* → L298-301 *« ses gestes n'avaient aucun réceptacle …
Corrigé »*; *« Une justification devenue bloc »* → Qualifieur L60-63
*« la raison d'une directive n'est pas une seconde directive »*.

---

## Settled and carried faithfully — the roll

For the record, each settled subject and where `modifications.md`
carries it. Quotes only where the match needed one.

| Subject | Where carried | Match |
|---|---|---|
| **A1** genre agent, six genres, two doubt exits, asymmetry | `qualifieur.md` L42-139 | ✅ — asymmetry L124-127, doubt table L117-122 identical to `sujets.md` L895-898 |
| **A1** `/3a_genre` between `/3_decoupe` and `/3b_nature`, routing | L1322-1328 | ✅ |
| **A1** `/1_lexique` accepts its question file | L1330-1333 | ✅ |
| **A1** `/5_reclasse` splits by genre, deletes previous, counts | L1345-1380 | ✅ — *« Supprimés avant chaque partage »*, *« autant de blocs en sortie qu'en entrée, aucune ligne `Genre:` vide, aucun genre hors des six »* |
| **A1** Classeur only on `comportement` | L56-57 | ✅ |
| **A1** Convertisseur: transverses to every nature, références and hors-périmètre to the transversal | L543-549, L1384 | ✅ |
| **A1** Architecte receives the directives file | L636, L683-717 | ✅ (see X-1 for the one clause) |
| **A1** `Genre:` re-posed each turn | L1324-1325 *« sur les blocs marqués, ou sur tous au premier tour »* | ✅ |
| **A2** Rédacteur transmits the attachment | `Global:` line, L147-182 | ✅ — *section, not block* is within L318 *« Le grain … dépend de ce que contient l'index »* |
| **A2** grid of time 2 | `GRILLE_EXISTANT.md` E1-E4, L470-508 | ✅ — *déjà pris · contredit · retire sans le dire*; passe-B form on another corpus |
| **A2** Sondeur reads the global, time 2 only, touched sections only | L410-437, invocation 3 *Existant* | ✅ — also settles L326 *« quelle invocation … à trancher à l'écriture »* |
| **A2** `/4_grille` runs time 2 after time 1, marked blocks only, no return | L1341-1343 | ✅ |
| **A3** Concepteur | L844-885 | ✅ — names, empty bodies, compiles, commits; *not implemented* body added |
| **A3** Testeur | L889-935 | ✅ — one test per criterion, new fail / old pass |
| **A3** Réalisateur reduced, never edits a test | L1089, L1124-1130 | ✅ |
| **A3** Relecteur stays; 2 and part of 4 mechanical; 1, 3, 5 remain | L1177-1237 | ✅ |
| **A3** who compiles — *à trancher* | L873-885, L1076-1079 | ✅ settled: the Concepteur, by lot; Détailleur still writes no code |
| **A3** `/8_code` three contexts per lot | L1418-1422 | ✅ |
| **A4** Testeur writes the recette line before coding | L900, L924-935 | ✅ — adds *« chaque ligne nomme l'état »* |
| **A4** `/9_controle` assembles, orders by state, filters, two sources | L1451, L1464-1478 | ✅ |
| **A5** registre: doubts + missing intentions + Arbitre's product questions; collects, does not conclude | L1452, L1480-1490 | ✅ — Architecte coverage holes excluded, as L523-528 |
| **A5** decisions file per cycle, even empty | L1453 `code/decisions-produit.md` | ✅ |
| **A5** scope: main + each bugfix; Contrôleur main only | L1454, L1500-1505 | ✅ |
| **A5** Rédacteur invocation 3 → `desc-produit-fusion.md`, order of cycles, one invocation, copy when nothing | L249-274 | ✅ verbatim |
| **A5** Fusionneur reads `desc-produit-fusion.md` | L811, L822-825 | ✅ |
| **A5** `/fusion` invokes Rédacteur then Fusionneur at the very end | L813, L1507-1514 | ✅ — mechanism: line 10, file absent → invocation 3 |
| **A5** Arbitre: nothing | Arbitre section carries D14/U10 only | ✅ |
| **A5** D17, D20 already corrected | `8_code` L1428 *« Les deux passages périmés retirés »* | ✅ |
| **A6** grid: the two levels | L351, L1525-1528 | ✅ |
| **A6** Sondeur writes a `Défaut:` with pre-filled answer and reference | L387-401 | ✅ — three-case table identical to L644-648 |
| **A6** Rédacteur: silence is acceptance | L184-190 | ✅ |
| **A7** Sondeur: transverses in context, matching at question time, no table | L374-385 | ✅ |
| **A7** diverging rules | L403-408 | ✅ identical to L878-881 |
| **A7** genre test and *doubt → not transverse* | L102-127 | ✅ |
| **A7** Convertisseur splits a transverse rule in two | L560-571 | ✅ |
| **A7** Rédacteur: a modified transverse re-marks every block | L192-203 | ✅ |
| **A7** Détailleur, Cadreur, Vérificateur: nothing | Cadreur/Vérificateur *« aucune modification du fichier de travail »*; Détailleur carries U10 only | ✅ |
| **A7** scope question before Classeur and Sondeurs | Qualifieur L135-139, `/3a_genre` routing | ✅ |
| **Rupture 5** `/conventions` tests file existence, last line | L1399-1401 | ✅ |
| **Rupture 5** incremental invocation, read ban restricted to invocation 1, `couverture.md` per feature, complete / replace | L637, L719-739 | ✅ |
| **F1** Relecteur stays | L1212-1213 | ✅ |
| **U7** insufficient answer → new question file; `/conventions` routing | L641, L788-800, L1402-1403 | ✅ |
| **U10** Détailleur multi-entry blocking file with dependencies | L1019, L1058-1072 | ✅ — cascade to the Arbitre L1020, L1285 |
| **U10** Réalisateur continues on what does not depend; second gap appended | L1091, L1151-1158 | ✅ |
| **U11** `/7_lots` reads the `## Verdict`; a refusal is a stop | L1405-1414 | ✅ |
| **U12** already corrected in `/8_code` | not re-listed | — nothing to pass; not re-verifiable from these two files after the `/8_code` rewrite |
| **A-2** Réalisateur blocks after two identical failures | L1092, L1160-1171 | ✅ |
| **A-6** `/8_code` stops at the third re-split, relays `## Ce qui revient` | L1427, L1436-1443; Cadreur L969-971 | ✅ |
| **D10** Convertisseur second, technical question file; reversibility frontier; `/6_convertit` three-case routing; explicit exception | L573-599, L1385-1395 | ✅ verbatim |
| **D13** Fusionneur checks the title at `INSERT`, touched sections only | L812, L827-840 | ✅ |
| **D14** 2 · Architecte marks `permanente` / `spécifique` | L638, L741-750 | ✅ |
| **D14** 3 · Réalisateur reads permanentes + named, with emphasis | L1090, L1132-1149 | ✅ |
| **D14** 4 · Relecteur point 3 extended | L1182, L1222-1224 | ✅ |
| **D14** 5 · Arbitre sorts what comes up | L1283-1284, L1295-1316 | ✅ table identical to L1960-1965 |
| **D14** 6 · second table of `couverture.md` removed, first kept | L639, L752-765 | ✅ |
| **D14** 1 · grid: remove 34 | L1530-1545 | carried, **not done** — N-1 |
| **D15** Architecte separates *couverture* / *conjonction*, marks, never converts, continues, doubt → asks | L640, L767-786 | ✅ — four kinds of gap, the fourth (*incohérence du corpus*) from pass sheet C3 |
| **D23** not extended; Contrôleur main cycle only | L1454, L1503-1505 | ✅ |
| **D24** | — | **LOST** — L-2 |
| **P10, P11** two `PROCESS_AVAL` wording fixes | L1564-1570 | carried, pending with the process documents |
| **D5, D7, D16, D17, D18, D20, D21, D22** *« corrigé dans la chaîne »* before this pass | D20 in `8_code` L1428; D5 in Rédacteur C5 L289 | — nothing to pass |
| **Q1–Q24** | — | all answered by opening the files; no modification of their own, routed to the subjects above |

---

## Counting

| | |
|---|---|
| Headings and table rows examined | 57 (A1–A7 · C1–C5 · R3/R5/R6 · F1–F3 · U1–U14 + A-1…A-8 · D1–D24 · P1–P14 · Q as one) |
| Settled with something to pass | 26 |
| Carried and matching | 23 |
| Carried, marked not done | 1 (D14-1, grid) — N-1 |
| LOST | 2 — A1 *hors-périmètre not re-asked*, D24 *push justification* |
| DISTORTED | 1, narrow — A1 directive *« jamais de question »* |
| DISCARDED BUT APPLIED | 0 |
