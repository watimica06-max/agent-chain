# Verdict — the chain, judged whole

Written against `docs/process/PROCESS_AMONT.md` and
`docs/process/PROCESS_AVAL.md`, at the level they describe: what each
agent is for, what it reads and writes, where the boundaries fall and
why. The agents, the grids and the commands were not read. Where a
judgement rests on something only an agent's file could show, it is
listed in section 7, not guessed here.

The three measures, in the order that prevails: **robustness** (gaps
between the idea and the code), **round trips** (decisions asked of the
person, turns between agents, retries), **tokens** (what is read, how
many times). Every judgement below names the one it moves. Where a
number or a frequency could not be observed from a description, it is
marked *(estimate)*.

This chain has run and produced code; `proposition.md` has not. That
asymmetry is respected: a role this chain has and mine lacks is a
lesson for mine, not a defect here. The reverse — a role mine has and
this chain lacks — is reported only where the process files give no
reason for its absence, or a reason that does not hold.

---

## 1. The chain, as a whole

**The shape holds, and it holds for reasons the process files state
and that survive scrutiny.** Five of them carry most of the weight.

*Everything is a file, and the person answers offline.* No agent
converses; a question is four fixed lines with an empty `Answer:`, and
an answer re-enters through one route. This is what makes a run
replayable and a decision traceable to a block. It is also what makes
the upstream slow — but the process says so itself, and prices it
correctly: the upstream needs the person at every turn by nature.

*A closed reading set per agent, decided by the command.* An agent is
told its file, its invocation and its blocks; it never looks at the
folder. The three failures this prevents (reading a neighbour's
questions, misreading the turn, wandering when a folder is missing) are
real and were observed. It also gives the chain a property my design
bought at a higher price: the state machine lives in the commands, and
the agents carry none of it.

*One judge per fact.* The nature of a block has one writer (Classeur);
the product file has one author (Rédacteur) and two narrow editors; the
conventions have one author (Architecte); the sequence has one
(Vérificateur); the verdict one (Relecteur). Where the chain found two
judges it removed one — the Convertisseur's closure, the Rédacteur's
nature. Every one of those removals is justified by an observed
divergence.

*The one who finds a defect never fixes it* — except the Cadreur, which
keeps its context because it has just cut what it is asked to re-cut,
and the exception is argued rather than slipped in.

*A closed vocabulary makes a sweep exhaustive.* Eight natures, a grid
with identifiers, nine sections, five verbs for the merge. Each closed
list is what lets a later agent say "I looked at every one" and be
checked on it.

**Where it breaks, and what the break costs.**

1. **The idea file is never read again after the Rédacteur structures
   it.** The Lexicographe reads it whole; the Rédacteur reads it whole
   and writes the entire product file from it in one invocation; from
   then on every agent reads `desc-produit.md` and nothing upstream of
   it. Nothing compares the two. The process says of the Lexicographe
   and the Découpeur that "rien en aval ne rattrape ça" — and it is
   true of the Rédacteur's own losses too, without being said. A
   sentence of the idea that reached no block leaves nothing to probe,
   nothing to convert, nothing to control: the Contrôleur "ferme la
   chaîne sur son point de départ", but its starting point is the
   product file, not the idea. **Robustness, and at the cheapest point
   to have caught it.**

2. **Lots are cut by layer, so no behaviour is ever proved end to end
   before the emulator.** A lot cites entries of one section; a section
   is a nature; a nature is a code layer. The process knows the
   consequence — "un contrat sans rien derrière compile, passe ses
   tests, et ne fait rien" — and answers it with the pieces-as-lots rule
   and the trigger→listener check in the Cadreur and the Détailleur.
   Those are checks on the split, not on the running code: the first
   test that exercises a trigger through to its outcome is the person's
   thumb. **Robustness** — the gap class that this chain finds last and
   pays most for. *(Estimate: how many emulator findings are of this
   class is not observable here; it is the class the shape cannot
   catch.)*

3. **Two autonomous loops have no ceiling.** A redecoupage
   (Arbitre → `/7_lots` → `/8_code` → the same lot) is bounded by
   nothing but the Cadreur's willingness to write "what it does about
   what recurs"; the process itself describes a fifth redecoupage that
   repeats the second. A Cadreur block plus a convention request goes to
   the Architecte "puis le Cadreur à nouveau", and if the Architecte
   refuses, nothing says what stops the Cadreur from writing the same
   pair again. **Round trips**, and in the worst case a run that ends
   when the person notices.

4. **The grid does not learn.** A product question that surfaces
   downstream — in the Architecte's *couverture* gap, in an Arbitre
   block the corpus cannot answer — is the record of a class the grid
   missed. It goes to the person and is answered; nothing writes the
   class back. The grid is edited by hand, "hors chaîne". The same
   breach is paid again on the next feature. **Robustness across
   features**, the measure the process cannot see from inside one
   cycle.

5. **Conventions are re-derived per feature without reading what
   exists.** The Architecte's invocation 1 opens no conventions file,
   "y compris celui qu'une exécution antérieure de lui-même a laissé",
   and runs once per feature on one repository-wide file. Every rule
   that invocation 3 added lot after lot during feature N is not an
   input to feature N+1's derivation. **Robustness** — this is exactly
   the defect the Architecte exists to prevent ("deux lots le tranchent
   différemment"), moved from lot scale to feature scale. Section 7
   names what would settle whether the agent departs from this.

6. **Every answer re-runs the whole route, and the grid's global pass
   re-reads every block every turn.** The process chose one route over
   a short one for a stated reason (a changed block may change nature)
   and accepts the cost explicitly. The cost is real: four Sondeurs,
   pass B and C over all blocks, the Lexicographe twice, per turn.
   **Tokens**; and **round trips** — the person launches six commands
   or `/cycle` for each answer file, and answers a fresh file per turn
   with no floor on the number of turns.

What is sound outweighs what breaks, and the breaks are of two kinds:
(1), (4), (5) are missing wires — cheap to add without moving a
boundary; (2) is the shape itself and cannot be corrected agent by
agent; (3) and (6) are bounds and costs the process already half-names.

---

## 2. The roles

Eighteen agents across the two files; the Architecte appears in both
and gets one line.

**Lexicographe — the role holds**
One thing (names of things the code will build), needed (the Rédacteur
transcribes ambiguity into sixty blocks, and nothing after it merges two
names), done by nobody else. Moves robustness up; costs round trips —
its own loop before the product file, plus two invocations on every
answer file thereafter. The process concedes its value "reste à
prouver"; the reasoning that it is cheaper than sixty ambiguous blocks
holds.

**Rédacteur — the role holds**
Transcribe, structure, translate, integrate — one skill, and the only
author of the product file. Holds because a second pen on the product
file breaks the sentence-level merge. Robustness. Its weakness is not
the role but its unchecked output (section 3, Coverage; section 4).

**Découpeur — the role holds**
One rule (one trigger per block), applied to what the Rédacteur could
not see in its own block. Separate context is what makes it a check;
"moves, never writes" is what keeps it from becoming a second author.
Robustness: a block carrying two triggers is probed as one and its
second hole disappears.

**Classeur — the role holds**
One judge for a line two agents used to derive differently. The nature
decides the grid's questions and the technical section, so a wrong one
"ferme le bloc sur les mauvaises questions" — robustness. Small enough
that merging it into the Découpeur would cost nothing in tokens, but
the Découpeur must stop on a `Clarification needed` and the Classeur
must not; keeping them apart is justified.

**Sondeur — the role holds; the three angles are an unproven cost**
Probing the grid is the closure mechanism, and it is one thing. The
global invocation (record, pass B, pass C) holds on its own reason: the
reading order does not change a column crossing. The three angle
invocations triple pass A's tokens on a bet the process itself marks "à
mesurer sur des cycles réels". Tokens up; robustness up by an amount
nobody has measured *(estimate: after turn 1, the by-question and
by-nature angles find little the by-block one misses)*.

**Assembleur — the role holds**
Needed because four readers raise one hole under four wordings; reads
question files only, so it cannot lose a hole by comparing to the
product file. Round trips down (the person answers once). Its "in doubt
keep both" rule prices the error correctly.

**Convertisseur — the role holds**
Four things the product file lacks (technical names, layers, `Consumes`,
executable phrasing), produced by nobody else, and the Cadreur cannot
cut without them. In this chain's shape — a whole technical document
before any lot — the role is load-bearing. Robustness: the section is
the lot's layer. *(My design ruled the document out; here it is what
the Cadreur's inventory stands on, and removing it would remove the
Cadreur's reason to exist.)*

**Architecte — the role holds**
"How we code here", never "what" — one thing, one file, one author.
Robustness: an absent rule is decided differently by two lots. Its
invocation 1 as described has the per-feature re-derivation defect
(section 4), but that is a wire, not the role.

**Fusionneur — the role holds**
Sentence-level merge into the global, and the one report the person
reads. Needed because the global is what the next Rédacteur greps and
the Extracteur builds. Robustness: a block-level replace loses surviving
rules; the process names the case. Invocation 3 (bug-list → product) is
the same skill on a different delta and belongs here.

**Extracteur — the role holds**
Once per project, code → product description, so that a taken-over
application has a global to merge into. Nobody else reads code to write
product. Robustness on the first feature of an existing app; zero cost
afterwards.

**Cadreur — the role holds**
Inventory, then cut, under three constraints; the only agent that sees
the whole technical document and greps the whole code. "Rien en aval ne
rattrape un lot coupé trop gros" — robustness. Keeping its context
across Vérificateur rounds is the right exception to the fresh-eyes
rule and is argued.

**Vérificateur — the role holds**
Judges a split it did not cut, on a fresh context each time, and
derives the sequence mechanically. The three defects it catches that
names alone cannot (unbuilt surface, undeclared caller, contract without
cascade) are its reason. Robustness. Tokens: up to three full readings
of the split per cycle — the price of independence, paid knowingly.

**Détailleur — the role holds**
Turns cited entries into signatures and criteria a coder needs no
judgement to build from; walks the whole block before writing so that
a redecoupage does not cost eight sheets twice. The two tests for
assertions that "disappear" are the sharpest rule in either file.
Robustness.

**Réalisateur — the role holds; should split on one seam** *(estimate)*
Coding a lot from a self-sufficient sheet is one thing and it is
needed. It also writes the tests for its own criteria and maintains the
technical state — both in the context that just chose an
interpretation. The tests seam is the one my design would move (section
3): a test written by the interpreter asserts the interpretation.
Whether this costs gaps is not observable from the description.

**Relecteur — the role holds**
Judges interpretation against the sheet, never mechanics, never source
fidelity — each exclusion names who already covers it. "Un lot, un
verdict" and the divergence naming are what drive the loop. Robustness.

**Arbitre — the role holds**
The one agent allowed to wait on the person, and the one test that
decides whether it may settle ("does the answer change a behaviour the
corpus describes?"). Needed because the Détailleur and the Réalisateur
must not settle, and the command must not decide. Round trips down: a
block that the corpus already answers never reaches the person.

**Contrôleur — the role holds**
Product → sheet, sentence by sentence, reading no code; the Relecteur
covers sheet → code. Nobody else confronts the product file after
conversion. Robustness. It closes the chain on the product file, which
is one step short of the idea (section 3).

**Diagnostiqueur — the role holds**
Confirms a listed gap against the code and writes it in the technical
document's form, so that the downstream runs unchanged. One
investigation per gap in its own context is right (greps do not help
each other). Round trips: a correction cycle skips the upstream
entirely, and the Fusionneur's invocation 3 is what pays for that
shortcut afterwards.

Not agents, but load-bearing: `/5_reclasse` (a grep-sort, correctly
kept out of any context), `/9_controle`'s map and grouping script, and
the command itself as the state machine.

---

## 3. The roles that are missing

Measured against `proposition.md`. For each: a hole (what goes wrong
without it) or a justified choice (the justification, and whether it
convinces).

**Coverage — prose against structured spec, per unit. A hole.**
Nothing in this chain reads `idees.md` after the Rédacteur. A sentence
lost at structuring produces no block, hence no question, no entry, no
sheet, no criterion — and the Contrôleur, reading the product file,
reports nothing missing. The process files give no reason for the
absence; the closest statement is that the Rédacteur "transcrit
fidèlement", which is asserted, not checked. Robustness. One Sonnet
invocation per feature reading two files would close it; it is the
cheapest check my design has and this chain lacks.

**Mapper — units, kinds, cross-references, transverse list. A
justified choice, convincing.**
The chain has no unit map because it does not need one: the Rédacteur
decomposes by trigger, the Classeur gives the kind, and pass B of the
grid finds cross-block dependencies by crossing columns of the record
over all blocks — a stronger instrument than a cross-reference table
drawn from one reading, since it re-runs every turn. The cost is
tokens (pass B on every block every turn), and it is stated.

**Locator — existing behaviour, `new / kept / changed`, before the
questions. A choice, half justified.**
Three agents share the role: the Rédacteur greps the global's index for
a near title; the Fusionneur compares the feature file against the
global and asks when an existing rule has no match; the Cadreur greps
the code at cutting time. What is missing is the *replacement*
question — "today X, the idea says Y, replace?" — asked before closure.
The Fusionneur runs after conversion and asks only about rules with no
correspondence; a rule with a correspondence is replaced without a
question ("une révision modifie et remplace"). The justification — the
person owns the global and wrote the idea knowing it — convinces on a
global that is true. On a global that has drifted from the code, the
conflict surfaces at `/7_lots`, after closure. Robustness, on existing
applications only.

**Tester before Coder — tests written by a context that never sees the
code. A justified choice, not fully convincing.**
The chain's answer is "un test par critère" plus the Relecteur
comparing tests to criteria. That is a check on the tests, made by a
fresh context, and it is cheaper by one invocation per lot. It is
weaker than a spec-only tester in one way: the Relecteur can see a test
that asserts less than the criterion only if it reads assertion
strength, and the process describes it reading interpretation and
bodies, not assertions. *(Estimate: the difference is real and small;
section 7 names what would settle it.)*

**Reviewer for invention — code no criterion asks for. A hole, small.**
The Relecteur's five points are about what the sheet promised: a
signature, a test per criterion, conventions, dead inputs. Code that
does more than the sheet — a helper that changes behaviour nobody
described — is caught only if it touched a file the lot did not declare
(the compte-rendu must list those). Invention inside declared files
passes. Robustness; frequency unobservable *(estimate: rare with a
sheet this prescriptive)*.

**A breach ledger that feeds the grid. A hole.**
My design's `grille.md` gains a line each time a product question
reaches coding. Here the equivalent events exist — the Architecte's
*couverture* gap, an Arbitre block whose answer changes described
behaviour — and are answered by the person, but no artefact records
the class the grid missed, and the grid is edited "hors chaîne". Every
feature pays the same missing class. Robustness over features.

**A manual-verification list handed to the person. A hole.**
She "tests on the emulator in her own time", unguided. The Contrôleur
writes what is missing, not what to look at; no agent writes which
intentions have no automated test. Round trips: gaps found by
wandering rather than by list. Cheap to add as a Contrôleur output —
its *douteux* list is half of it already.

**A Driver with no judgement, never invoking from inside an agent. A
justified choice, convincing for the downstream, with a cost.**
The process argues the four dialogues precisely: the caller keeps its
context and resumes, and a return through the command would hand the
turn back to the person. That holds. The cost is that a Cadreur holds
three Vérificateur rounds in one context, and that a Détailleur or
Réalisateur idles for twenty minutes on every product block while the
Arbitre polls a person who is "hors session" by design. Tokens neutral
(idle), round trips neutral, wall time paid on every downstream product
question *(estimate: the poll almost never catches her)*.

**Conventions from code samples on an existing application. A hole.**
The Architecte "ne lit le code à aucune invocation", and derives the
conventions from the product and technical documents alone. On a new
application that is the only source. On an existing one it writes how
to code without seeing how it is coded, and the Arbitre later greps
"the same problem solved elsewhere in the same code" — which is to say
the code's conventions are read, lot by lot, by the wrong agent. The
stated reason ("il nomme les outils, il ne les trouve pas") covers
tools, not style. Robustness; measured by the chain's own
`audit_conventions` as the number of rules added by requests.

**A global technical document — ruled out in mine, central here.**
Reported for symmetry: this chain has the artefact my design refused,
and uses it well (the Cadreur's inventory, the `Consumes` graph, one
section per layer). Its staleness risk is handled by freezing it once
the split exists and by the technical state. I would not call it a
defect here; I would call my own §7.5 answered by a working system.

---

## 4. The boundaries

Sweep first: every artefact the two files name, in the order they
introduce it, with its producer and its reader. Then one entry per
defect. Then the same for what an agent assumes rather than reads.

### The sweep

| # | Artefact | Producer | Reader | Verdict |
|---|---|---|---|---|
| 1 | `idees.md` | Product Owner; Lexicographe (settled terms) | Lexicographe; Rédacteur inv. 1 | wired; never re-read after inv. 1 — entry D1 |
| 2 | `questions-lexicographe-NN.md` | Lexicographe (new file each time) | Product Owner; Lexicographe; commands | wired |
| 3 | `lexique.md` — `## Tranché`, `## Non tranché`, retired terms under the kept one | Lexicographe | Lexicographe (grep at inv. 4); Rédacteur | wired |
| 4 | Two natures of word (quoted display text / unquoted concept in English) | Lexicographe | Rédacteur | wired |
| 5 | `desc-produit.md` | Rédacteur; Découpeur (splits); Classeur (`Nature:`) | Sondeur; `/5_reclasse`; Convertisseur inv. 2; Fusionneur; Architecte; Contrôleur (aval) | wired |
| 6 | The global's index (`grep ^#` on `PRODUIT_GLOBAL.md`) | Fusionneur / Extracteur (titles) | Rédacteur | wired; quality rests on titles — entry D13 |
| 7 | Block identifier `B7` | Rédacteur | Sondeur (`Block:`), Classeur, Convertisseur (`[B12: …]`, `<<ASSUMED B40>>`, `tracabilite.md`), Contrôleur | reader many; stability never stated — entry D2 |
| 8 | `Nature:` line, written empty | Rédacteur, Découpeur | Classeur; `/3b_nature` (count); `/5_reclasse` | wired |
| 9 | `**Clarification needed:**` | Rédacteur | `/3_decoupe`, Découpeur, Sondeur (stop); Rédacteur (removes) | wired |
| 10 | `NEW` / `MODIFIED` markers | Rédacteur | `/3_decoupe`, `/3b_nature`, `/4_grille` (greps); Classeur; `/5_reclasse` (strips) | wired; trusted on one side, distrusted on the other — entry D3; Découpeur's halves unmarked — entry D4 |
| 11 | `[integrated: B7]` | Rédacteur | nobody named | entry D5 |
| 12 | Rédacteur's questions file (written even when empty) | Rédacteur | `/2_structure` | wired |
| 13 | Classeur's questions file | Classeur | `/3b_nature` | wired |
| 14 | The eight natures (closed list) | process | Classeur, grid, Convertisseur, `/5_reclasse` | wired |
| 15 | Grid identifiers `A1.1`…, `B1.8`, `C1.7` | grid file | Sondeur (record) | wired; never on a question to the person — by design |
| 16 | `cadrage-produit/par-bloc.md`, `par-question.md`, `par-nature.md`, `global.md` | four Sondeurs | Assembleur; `/4_grille` (existence) | wired |
| 17 | `cadrage-produit/releve.md` | global Sondeur | itself (pass B, C) | wired; nobody else — see D6 |
| 18 | `cadrage-produit/blocked_<angle>.md`, `blocked_global.md` | a Sondeur | Product Owner; command | wired |
| 19 | `cadrage-produit/closed/` | created by `/4_grille` | nothing named writes or reads it | entry D7 |
| 20 | `cadrage-produit/questions.md` (with `## Merge`) | Assembleur | `/4_grille` (copies, renumbers, strips `## Merge`) | wired |
| 21 | `questions-sondeur-NN.md` | `/4_grille` | Product Owner; Lexicographe 3/4; Rédacteur 2 | wired |
| 22 | `Block:` line (ids only, `-` for feature-level) | Sondeur | Assembleur (groups); Rédacteur (where it lands) | wired; `-` is where new subjects come from — by design |
| 23 | `desc-par-nature.md` (markers stripped) | `/5_reclasse` | `/6_convertit` | wired |
| 24 | `convertisseur/<nature>-input.md` | `/6_convertit` | Convertisseur inv. 1; `/6_convertit` (byte compare) | wired |
| 25 | `convertisseur/<nature>.md`, `-notes.md`, `questions-<nature>.md` | Convertisseur inv. 1 | `/6_convertit`; Convertisseur inv. 2 | wired |
| 26 | `[B12: what is expected]` cross-section reference | Convertisseur inv. 1 | `/6_convertit` script (single entry) or inv. 2 | wired; block with zero entries unstated — minor, D8 |
| 27 | `<<ASSUMED B40: …>>` | Convertisseur inv. 1 | `/6_convertit` (re-run trigger) | wired |
| 28 | `spec-technique.md` — nine sections, `*(empty)*`, numbered entries, `Consumes:` / *Declared links*, preamble, *Singularity*, *Agreement between entries*, *Resources*, §9 Screen / Text | `/6_convertit` (assembly); Convertisseur inv. 2 | Architecte inv. 1; Cadreur (whole); Vérificateur, Détailleur (cited entries) | wired; preamble dependencies "come from the Rédacteur" via no named artefact — D9 |
| 29 | `tracabilite.md` | Convertisseur inv. 2 | Architecte inv. 1; `/9_controle` | wired |
| 30 | `questions-convertisseur-NN.md` | `/6_convertit` (merge) | Product Owner; Lexicographe; Rédacteur | wired; carries technical questions on the product route — D10 |
| 31 | `docs/TECHNICAL_CONVENTIONS.md` | Architecte only | Cadreur, Détailleur, Réalisateur, Relecteur, Arbitre (whole); Extracteur | wired; re-derived per feature blind — D11; Réalisateur reads it or reads the sheet — D12 |
| 32 | `couverture.md` (two tables; `no rule` spelled out; mechanical / reading per rule) | Architecte inv. 1 | Product Owner, once | second table has no agent reader — entry D14 |
| 33 | `questions-architecte-NN.md` | Architecte inv. 1 | Product Owner; Architecte inv. 2 | wired; a *coverage* gap goes to the person after closure — D15 |
| 34 | `architecte/<demande>.md` with `## Verdict` | Cadreur, Détailleur, Réalisateur, Arbitre; Architecte (verdict) | Architecte inv. 3; the author | wired; the asking lot is coded under the old rule — D16 |
| 35 | Verdict carries the rule's text, not its number | Architecte | the reader that does not open the conventions | wired |
| 36 | `plan-fusion.md` (five verbs, `INIT`) | Fusionneur inv. 1 | Fusionneur inv. 2 | wired |
| 37 | `docs/PRODUIT_GLOBAL.md` | Fusionneur; Extracteur | Rédacteur, Fusionneur (by index) | wired |
| 38 | `rapport-fusion.md` | Fusionneur inv. 2 | Product Owner | wired |
| 39 | `bug-list.md` | Product Owner | `/diagnostique` (splits); Diagnostiqueur inv. 2; Fusionneur inv. 3 | wired |
| 40 | Extracteur tags `<<REF>>`, `<<ORPHAN>>`, `<<HARD_STYLE>>`, `<<HARD_TEXT>>`, `<<DOUBT>>` | Extracteur | final pass (`REF`); Product Owner by script (others) | wired |
| 41 | `questions/<agent>/` (archived by `git mv`) | commands | agents (highest number) | wired |
| 42 | `blocked_<agent>.md` with `## Decision`; renamed `-NN` | agent; Product Owner; Arbitre (two of them) | agent; command (that line only); Arbitre (numbered ones) | rename vs delete contradiction — entry D17 |
| 43 | `docs/process/GRILLE_*.md` | Product Owner, off-chain | Sondeur; Convertisseur; Architecte | wired; never written by the chain — section 3 (ledger) |
| 44 | `desc-bug.md` (form of the technical document; carrier per entry) | Diagnostiqueur inv. 2 | Cadreur, Vérificateur, Détailleur | wired |
| 45 | `investigation/<id>.md` | Diagnostiqueur inv. 1 | Diagnostiqueur inv. 2 | wired |
| 46 | Symbol inventory (before cutting) | Cadreur | Vérificateur ("l'inventaire contre les lots") | no file named — entry D18 |
| 47 | `code/decoupage.md` (with anchors) | Cadreur | Vérificateur, Détailleur, Arbitre, `/9_controle` | wired |
| 48 | `code/sequence.md` (order, blocks, defects) | Vérificateur | command; Détailleur; Cadreur (defects) | wired |
| 49 | `code/<lot>/fiche-executable.md` | Détailleur | Réalisateur, Relecteur, Contrôleur | wired |
| 50 | `code/<lot>/compte-rendu.md` (build claim, out-of-lot files, request trace) | Réalisateur | Relecteur; next block's Détailleur (grep) | wired; the build claim has no independent execution — entry D19 |
| 51 | `code/<lot>/verdict.md` (PASS / FAIL minor / FAIL structural; divergence names lots; build line copied) | Relecteur | command; Réalisateur on FAIL; Arbitre (status) | wired |
| 52 | `code/<lot>/reprise_realisateur.md` (*En chantier*) | Réalisateur, stopping | next Réalisateur | wired |
| 53 | `code/redecoupage.md` (constraint, never solution) | Arbitre | Cadreur; Vérificateur (archives) | wired; loop unbounded — section 5 |
| 54 | `code/controle/<groupe>.md`, `code/rapport-controle.md` (numbered) | Contrôleur | Contrôleur inv. 2; Product Owner | wired; groups absent when `/8_code` calls — entry D20 |
| 55 | `docs/CURRENT_TECHNICAL_STATE.md` (two sections read whole, rest grepped) | Réalisateur | Détailleur, Réalisateur, Diagnostiqueur; "commande le Cadreur" | reader list contradicts prose — entry D21; falsified entries — D22 |
| 56 | `tracabilite-full.md` | `/9_controle` | grouping script | wired |
| 57 | `audit-blocages.md`, `audit-conventions.md` | orchestrator | itself | wired |
| 58 | `stop.md` / `stop1.md` | Product Owner | command, from the main checkout | wired |
| 59 | `bugfix-NN/` working folder | command | every downstream agent (passed as working folder) | wired; the Contrôleur never sees it — entry D23 |

### The defects

**D1 — The idea file has no reader after structuring.**
Rédacteur (inv. 1) → every agent downstream of `desc-produit.md`.
Robustness: a lost sentence is invisible to the whole chain, including
the Contrôleur. (Section 3, Coverage.)

**D2 — Block identifiers are assumed stable, and nothing says who
guarantees it.**
Rédacteur (creates, integrates, "efface tous les marqueurs avant
d'écrire") → Sondeur (`Block:`), Convertisseur (`[B12]`, `<<ASSUMED
B40>>`, `tracabilite.md`), Contrôleur (`/9_controle`'s map). Six
readers address blocks by number; the process never states that a
number, once given, is never reused or shifted, nor what happens to
`B7`'s number when an answer replaces its sentence with a new block.
Robustness if they shift (a question lands on the wrong block; a
traceability line points at the wrong intention). The Fusionneur strips
the numbers at merge precisely because two features would both have a
`B7` — so the chain knows numbers are local, but not that they are
stable within a feature. Section 7.

**D3 — Markers are trusted on one side of the chain and distrusted on
the other.**
Rédacteur (writes them) → `/3_decoupe`, `/3b_nature`, `/4_grille` (grep
them) versus `/6_convertit` (refuses them: "Pourquoi pas les marqueurs
— le Rédacteur les efface à chaque tour", and compares bytes instead).
The reason `/6_convertit` gives — a block changed two turns ago carries
none — is a reason about staleness, not about omission; but the
byte-compare it chose would also catch a MODIFIED the Rédacteur forgot,
and the three commands that trust the grep cannot. A forgotten
`MODIFIED` on a changed block is "un bloc qui ne sera jamais resondé"
by the process's own words, and nothing checks it. Robustness. The fix
the chain already owns (a byte diff of the product file between turns)
costs no agent.

**D4 — The Découpeur's new blocks may carry no marker.**
Découpeur (writes new blocks, "déplace, ne rédige pas") → `/4_grille`
(probes `NEW` or `MODIFIED` only, after turn 1). The process says the
Découpeur writes an empty `Nature:` on each block it creates and says
nothing of markers. If it writes none, a block split at turn 2 is
classified (empty `Nature:` is greppable) but never probed by the
angles — pass A is skipped on a block that "n'a jamais été sondé".
Robustness. Section 7.

**D5 — `[integrated: B7]` has a producer and no reader.**
Rédacteur → nobody named. Either a command checks that every answered
entry carries it (then the process should say so — it is the only
check that an answer was not dropped at integration) or it is a
token-cost with no consumer. Robustness if the first, tokens if the
second.

**D6 — The angles' pass A and the global's record are never
reconciled.**
Three angle Sondeurs (pass A on marked blocks, output: questions) ↔
global Sondeur (its own pass A on all blocks to build the record, then
B and C). Pass A is therefore run four times on marked blocks, and the
global's closure-test answers are never compared with the angles'. Not
a robustness defect (the union is the output, by design); a tokens
one — the fourth pass A is paid every turn on every block. *(Estimate:
the global's pass A is the largest single reading of the upstream.)*

**D7 — `cadrage-produit/closed/` is created and nothing is said to
fill or read it.**
`/4_grille` (creates it "before invoking") → no producer, no reader
named. Either an artefact the process forgot to describe (then the
next phase cannot check it) or a folder that survives from an earlier
design. Tokens if unused; robustness if something is written there
that nobody reads.

**D8 — A `[B12: …]` reference to a block that yielded no entry has no
stated outcome.**
Convertisseur inv. 1 → `/6_convertit` script / inv. 2. "Le bloc n'a
donné qu'une entrée → script; plusieurs → la transversale" — zero is
not covered. A block whose rules all went into the preamble, or a block
`tracabilite.md` marks with a dash, can be the target. Round trips if
it becomes a question; robustness if the reference is silently left.
Minor.

**D9 — The preamble's dependencies travel by no named artefact.**
Rédacteur ("seul le Rédacteur a le global sous les yeux") → Convertisseur
inv. 2 ("les dépendances du préambule viennent du Rédacteur"). The
product file's text outside blocks is the only candidate, and that text
is read by the Convertisseur inv. 2 and by nobody who probes. A
dependency stated there is neither classified nor questioned by the
grid. Robustness. Section 7.

**D10 — Technical questions from the Convertisseur travel the product
route.**
Convertisseur (questions) → Product Owner → Lexicographe → Rédacteur
(integrates into the product file) → … → Convertisseur. The route is
right for a product hole. A question that is technical — two natures
named one concept two ways, a cross-section reference the transversale
cannot choose — has no answerer on that route: the person cannot
arbitrate a technical name, and the Rédacteur has nowhere to write the
answer in a product file. Round trips (a whole turn of the upstream for
a naming choice), and robustness if the person answers a technical
question as if it were product. The Architecte's *précision* rule ("il
tranche lui-même") is the right home; nothing routes there from the
Convertisseur.

**D11 — The Architecte's invocation 1 re-derives repository-wide
conventions per feature, reading none of what exists.**
Architecte inv. 3 (adds rules lot after lot, feature N) → Architecte
inv. 1 (feature N+1: "n'ouvre aucun fichier de conventions … y compris
celui qu'une exécution antérieure de lui-même a laissé"; "l'amont le
dérive une fois par feature"; one file "partagé par tout le dépôt").
As described, feature N+1's derivation discards feature N's amendments,
and every coding agent of N+1 reads the result "en entier". The
justification ("les relire serait dériver de sa propre sortie") holds
for a first derivation and fails for the second: the amendments are
not its own output, they are settled requests. Robustness — the
cross-lot inconsistency the agent exists to prevent, at feature scale.
Section 7 names what would settle whether the command only runs
invocation 1 once per project.

**D12 — Who reads the conventions for the Réalisateur is said two
ways.**
Détailleur ("il lit les conventions en entier, le Réalisateur code
contre la fiche"; "une règle qu'il ne nomme pas est une règle que le
Réalisateur n'appliquera pas") ↔ the file table (`TECHNICAL_CONVENTIONS`
read by "Cadreur, Détailleur, Réalisateur, Relecteur, Arbitre — en
entier"). One of the two is what the agent does. If the sheet is the
carrier, a rule the Détailleur omitted is lost (robustness) and the
Réalisateur's whole-file reading is waste (tokens); if the whole file
is read, the Détailleur's naming is redundant (tokens). Section 7.

**D13 — The global's index is the Rédacteur's only instrument, and the
chain's only quality rule for it is a sentence.**
Fusionneur / Extracteur (write titles) → Rédacteur (greps `^#`, reads
"un titre proche"). "Un titre doit dire ce que sa section contient,
sinon l'index ne sert à rien — c'est le critère de qualité du global."
No agent checks it; the Fusionneur's five verbs do not include a title
verdict. A section whose title drifted from its content is a section
the Rédacteur never opens, and a duplicate block enters the global at
the next merge. Robustness on the global, slowly.

**D14 — `couverture.md`'s second table promises a wiring nobody does.**
Architecte inv. 1 (writes per rule whether its test is mechanical or a
reading — "c'est elle qui rend vérifiable l'exigence que toute règle à
test mécanique soit câblée dans la commande de vérification") → reader:
"Product Owner, une fois". No agent, no command, is named as the one
that wires a mechanical test or checks that it was wired. A rule
declared mechanical and never wired is a rule the Relecteur searches
for by reading — the process elsewhere says a reading check is
"ratification, pas détection". Robustness (a mechanical rule left to a
reading) and tokens (a table nobody consumes).

**D15 — A *coverage* gap found by the Architecte reaches the person
after the product was declared closed, by a file that does not re-enter
the route.**
Architecte inv. 1 ("il la lève — la grille de cadrage a un trou") →
`questions-architecte-NN.md` → Product Owner → Architecte inv. 2
("transforme ses propres réponses en règles"). A coverage gap is a
product hole by the process's own definition; its answer becomes a
*convention*, not a product sentence — it never reaches the product
file, the technical document, the global, or the grid. Robustness: the
behaviour is decided in a file the Fusionneur never reads, and the next
feature's grid has the same hole. Round trips: the person answers a
product question outside the product route.

**D16 — The lot that asks for a convention is coded under the old
rule, and nothing revisits it.**
Détailleur / Réalisateur ("écrivent la demande et continuent contre les
conventions telles qu'elles sont") → Architecte inv. 3 ("à la fin de
chaque lot … ainsi le lot suivant l'a") → Relecteur (checks the
conventions the sheet named — the old ones). The asking lot passes
review against the rule that existed; the rule written for it governs
only what follows. The process chose this to keep the lot atomic, and
it is a fair trade — but the divergence is unrecorded: neither the
verdict nor the technical state says "lot-03 predates rule R12".
Robustness at the next lot that touches the same file, and in
`audit_conventions`, which counts the rule without the lot it left
behind.

**D17 — A settled blocking file is renamed by one agent and deleted by
five.**
Reported by the process itself (contradiction 1). Consequence on a
boundary it does not draw: the Arbitre "lit les blocages déjà tranchés,
numérotés, avant de trancher — un blocage qui en suit un autre signifie
souvent que la réponse précédente était trop étroite". If the five
delete, the Arbitre's widening rule has nothing to read, and the same
narrow decision is taken twice. Round trips (a second block for the
same cause) and robustness (a narrow decision applied twice).

**D18 — The Cadreur's symbol inventory is an input to the Vérificateur
and is not a named file.**
Cadreur ("il ne coupe pas avant d'avoir écrit l'inventaire") →
Vérificateur ("il croise l'inventaire contre les lots"; fresh context
each time). If the inventory lives only in the Cadreur's context, the
Vérificateur cannot read it and its first defect class ("une surface
non construite") is checked against the lots' own declarations —
ratification. If it lives in `code/decoupage.md`, the file table should
say so. Robustness or nothing, depending on which. Section 7.

**D19 — The build and test result has one producer and no independent
execution.**
Réalisateur (runs analysis and tests, writes the claim) → Relecteur
("recopie ce que le compte rendu affirme du build — jamais vide") →
command (merges on PASS; the orchestrator's own rules forbid it to run
tests, on the argument that a clean merge produces identical code).
The claim is copied, never re-run. The process's reason for the
Relecteur not to re-check mechanics — "ratification, pas détection" —
is about a second *reading*; an execution is a different instrument
and would detect a misread runner output, a test skipped by a filter,
a suite green because it did not compile the new target. Robustness.
*(Estimate: rare per lot; one full-suite run after the last lot, by
the command, costs no agent tokens and would catch the cumulative
case.)*

**D20 — `/8_code` invokes the Contrôleur without the groups it
requires.**
Reported by the process (contradiction 3). Boundary reading: the group
list has a producer in `/9_controle` (map + script) and none in
`/8_code`; the Contrôleur "exige que le prompt nomme ses blocs et ses
fiches — ni l'un ni l'autre n'est déduit". As written, the end-of-cycle
control either does not run or runs on a prompt the agent refuses.
Robustness: the chain's closing check is the one that the chain's own
loop cannot launch.

**D21 — The technical state's reader list omits the agent the prose
says it commands.**
Réalisateur (writes) → "Détailleur, Réalisateur, Diagnostiqueur" (file
table) versus "Ce document commande le Cadreur : c'est contre lui qu'un
lot est déclaré production ou modification" (twice, in both files).
If the Cadreur reads it, the table is wrong (tokens: a whole document
read per cycle, undeclared); if it does not, production/modification is
declared from grep alone and the sentence is false (robustness: a
symbol the grep misses is declared new). Section 7.

**D22 — "Ce qu'un lot a rendu faux disparaît" requires a reading the
Réalisateur does not do.**
Réalisateur (reads two sections whole, greps the rest; writes after its
lot) → next Détailleur (reads it). An entry made false by the lot is
found only if the Réalisateur greps for it — and one cannot grep for a
rule one does not know applies, which is the process's own reason for
making two sections whole. A stale entry outside those two sections is
a signature the next Détailleur writes against something that no longer
exists — the exact divergence the Relecteur then reports, one block
later. Robustness, and a FAIL round paid for a document defect. Also
unstated: whether a fresh Réalisateur after a FAIL removes what the
failed attempt wrote there.

**D23 — A correction cycle's sheets live where the Contrôleur never
looks.**
Diagnostiqueur / Cadreur / Détailleur (in `bugfix-NN/code/`) →
Contrôleur (reads the feature's product file against "toutes les
fiches" — of the feature folder; "cycle de fonctionnalité seulement").
The Contrôleur's report becomes a bug list; the bug-fix cycle codes the
missing intentions; `/9_controle` re-run "pour comparer deux états"
still finds them missing, because their sheets are in another folder.
The loop that "ferme la chaîne sur son point de départ" cannot be
closed a second time. Robustness (the second report is false) or round
trips (the person reconciles by hand).

**D24 — Push is part of the merge in the process and occasional in
the orchestrator's instructions.**
Outside the two files, but placed in my context by the environment: the
process says "le push fait partie du merge, pas d'un après-coup — une
phase qui ne vit que sur la machine locale est perdue avec elle"; the
orchestrator's standing instructions say local `HEAD` is the reference
because "pushing is occasional". One of the two is what happens.
Robustness of the record, not of the code; named because it is a
boundary between the process and its executor, and the process cannot
see it.

### What an agent assumes rather than reads

**A1 — That every answer lands as text in the product file.**
Assumed by: Sondeur ("une question dont la réponse est consignée ne se
repose jamais"; "aucun ne lit les questions d'un tour précédent"),
Convertisseur ("une réponse lui parvient par le fichier produit").
Established by: the Rédacteur's integration — but an answer that
confirms the block as it stands changes no sentence, sets no marker,
and is consigned nowhere in the file. The next turn's angles do not
re-probe an unmarked block, so the question does not recur — until a
neighbouring answer marks it MODIFIED, when a Sondeur with no memory
asks it again. Round trips. *(Estimate: frequent on "keep as is"
answers.)*

**A2 — That the Rédacteur never forgets a marker.** See D3. Established
by nothing; checkable by a diff the chain already runs elsewhere.

**A3 — That block numbers are stable.** See D2.

**A4 — That the grid is complete.** Assumed by every agent downstream
of `/4_grille` ("Il n'est pas le filet de la chaîne amont" — said of
the Convertisseur and of the Détailleur). Established by: the person,
off-chain. The Architecte's *conjonction* class is admitted as
invisible to the grid by construction; a *couverture* gap is a grid
hole by definition. Neither writes back. Section 3, ledger.

**A5 — That the global is true.** Assumed by the Rédacteur (index grep
decides whether a subject exists) and the Fusionneur (compares against
it). Established by: the Extracteur once, then the Fusionneur after
each feature — and never by a comparison against the code afterwards.
Also: "Le global ne se révise pas pendant qu'un cycle aval tourne sur
le même périmètre" — a rule with no enforcer named. Robustness on the
second feature over the same screens.

**A6 — That the sheet is self-sufficient.** Assumed by the Réalisateur
("il ne lit ni le document technique, ni la liste des lots, ni la
séquence"). Established by: the Détailleur's walk and its rule to name
every applicable convention. Checkable: only by the Réalisateur
blocking — which is the designed signal, and it holds.

**A7 — That a symbol's name says what it is.** Assumed by the Cadreur
("il grepe, il n'ouvre jamais un fichier de code"), the Architecte
("ne lit le code à aucune invocation"), the Arbitre ("un fait sur le
code se grepe"). Established by: conventions on naming — written by an
agent that never reads the code. On a new application the chain names
everything, and the assumption is true by construction. On an existing
one it is the Diagnostiqueur's third widening and then "deviner".
Section 6, P4.

**A8 — That the person is not at the keyboard.** Assumed by the whole
upstream (offline answers) and contradicted by the Arbitre's
twenty-minute poll, which only pays off if she is. Both cannot be the
design's model of her. Round trips: the poll is wall time on every
downstream product block, and it stops anyway.

**A9 — That `N` lots per `/8_code` execution is a bound.** Assumed by
the command; it counts lots reviewed PASS. A redecoupage relaunch
resets nothing it counts and adds no PASS, so it bounds work, not
loops. Section 5.

---

## 5. The loops

Two natures are kept apart: a loop that waits for a person, and one
that runs alone. The stopping test is the field that matters.

### Loops that wait for a person

**U1 — Lexicographe, before the product file**
Between: Lexicographe inv. 1 → person → inv. 2 → inv. 1 …
In: inv. 1 raises at least one pair.
Stop: inv. 1's questions file is empty. Checkable — a file, written
even when empty.
Bound: none; "un terme tranché peut révéler une paire". The process
reports eight turns on one feature, half of which were on graphics and
label variants, and narrowed the scope in answer. Round trips.
Steps in: the person, every turn.

**U2 — Lexicographe on an answer file**
Between: inv. 3 → (person) → inv. 4.
In: any answered questions file of the grid or the Convertisseur.
Stop: inv. 4 has run. Checkable and mechanical — "après 3, toujours 4".
Bound: one pass per answer file, plus one person turn if inv. 3 asks.
Steps in: the person, only if inv. 3 asks.

**U3 — The Rédacteur's own signal**
Between: Rédacteur → person → Lexicographe 3/4 → Rédacteur inv. 2.
In: a non-empty Rédacteur questions file or a `Clarification needed`
in a block.
Stop: the Rédacteur's questions file is empty. Checkable.
Bound: none stated; in practice a clarification reads as one round.
Steps in: the person.

**U4 — The Classeur's question**
Between: Classeur → person → Lexicographe → Rédacteur (splits) →
Découpeur → Classeur.
In: a block whose two sentences produce two things.
Stop: the Classeur's questions file is empty and `grep -c '^Nature:$'`
returns zero. Checkable — the command counts.
Bound: none; each round is one block's split.
Steps in: the person.

**U5 — The grid turn — the loop that is the upstream**
Between: four Sondeurs → Assembleur → `/4_grille` → person →
Lexicographe 3/4 → Rédacteur 2 → Découpeur → Classeur → Sondeurs.
In: `questions-sondeur-NN.md` is not empty.
Stop: `/4_grille` finds no `NEW` or `MODIFIED` block and writes an
empty file. Checkable, by grep. Note what it does *not* test: that the
global pass B/C found nothing — it is not run when no block moved. The
test is therefore "nothing changed", not "nothing is open"; the two
coincide only if every answer lands as text (A1). Where an answer
lands as no change, the loop ends with the hole it asked about still
open in the text, and the Convertisseur "ne comble pas". *(Estimate: the
process's own rule "une réponse qui contredit une phrase la remplace"
covers most answers; the confirm-as-is answer is the residue.)*
Bound: none — "jamais un nombre d'itérations". Each turn re-runs pass
B/C over all blocks (tokens) and returns to the person (round trips).
Steps in: the person, every turn.

**U6 — The Convertisseur's questions**
Between: Convertisseur inv. 1/2 → `/6_convertit` → person → the same
route as U5 → `/5_reclasse` → `/6_convertit` (byte-diff decides which
natures re-run; every `<<ASSUMED` section re-runs).
In: `questions-convertisseur-NN.md` is not empty, or a section carries
`<<ASSUMED`.
Stop: the questions file is empty and no `<<ASSUMED` remains. Checkable
by grep.
Bound: none; and D10 — a technical question on this route has no
answerer, so a round can end with the same question asked again.
Steps in: the person.

**U7 — The Architecte's derivation**
Between: Architecte inv. 1 → person → inv. 2.
In: `questions-architecte-NN.md` carries questions.
Stop: an answered file has been integrated. Checkable. Whether inv. 2
may raise again is unstated — one round assumed.
Bound: none stated.
Steps in: the person — and D15: on a product hole, after closure.

**U8 — The merge**
Between: Fusionneur inv. 1 → person → inv. 2.
In: an existing rule with no correspondence in the new block.
Stop: `rapport-fusion.md` exists. Checkable — `/fusion`'s routing table.
Bound: one round by construction.
Steps in: the person, and she reads the report — the one manual step.

**U9 — A Sondeur block**
Between: a Sondeur → person (`## Decision`) → `/4_grille` again.
In: a blocking file per invocation.
Stop: the decision is filled. Checkable.
Bound: one.
Steps in: the person.

**U10 — Arbitre waiting on the person**
Between: Détailleur or Réalisateur → Arbitre → person → (the agent
resumes | stops) → `/8_code` again with the decision.
In: the corpus does not answer the block, or the answer would change a
described behaviour.
Stop: `## Decision` non-empty. Checkable — the caller tests emptiness,
and the Arbitre leaves it "exactement vide" otherwise.
Bound: twenty minutes of polling, then the agent stops (Détailleur:
block as is; Réalisateur: `reprise_realisateur.md`, compiling code
committed) and the command stops. Then the person fills, relaunches,
and the command "invoque l'agent qu'elle nomme". Bounded as a wait;
unbounded as a count — nothing limits how many product blocks one lot
may raise, one at a time, each a twenty-minute wait and a full stop.
Round trips. Each is also, by the process's own reasoning, a grid gap
nobody records (A4).
Steps in: the person.

**U11 — Cadreur block with a convention request**
Between: Cadreur (block + request) → `/7_lots` → Architecte inv. 3 →
Cadreur again.
In: a convention forbids what a lot requires.
Stop: the Cadreur no longer blocks. Checkable (no blocking file).
Bound: none stated. If the Architecte refuses ("une convention dit ce
que le projet a choisi"), the Cadreur "ne contourne jamais" and must
block again with the same pair; the process forbids re-asking under
another wording only to the Arbitre. This loop ends when the person
reads the third identical block. Round trips.
Steps in: the person, eventually.

**U12 — Contrôleur → correction cycle**
Between: Contrôleur → person (`bug-list.md`) → Diagnostiqueur → Cadreur
… → (`/9_controle` by hand).
In: intentions found nowhere.
Stop: none checkable — D23: the re-run cannot see the correction's
sheets, so the report never empties by this route. The process also
names a second exit ("une décision remplie … même sur un lot qui porte
déjà un PASS") whose producer — who writes a blocking file from a
control report — is not named.
Bound: none.
Steps in: the person, twice (list, then relaunch).

**U13 — Diagnostiqueur, one gap**
Between: Diagnostiqueur inv. 1 → person (decision) → `/diagnostique`
(that gap only).
In: an investigation blocks.
Stop: every gap of `bug-list.md` has a report — inv. 2 counts and
blocks if one is missing. Checkable.
Bound: one relaunch per gap.
Steps in: the person.

**U14 — `/8_code` execution**
Between: the command and the person.
In: `N` lots reviewed PASS, a `stop.md`, an empty decision, a lot failed
three times.
Stop: the list above. Checkable.
Bound: `N`; but A9 — `N` counts PASS lots, and a redecoupage adds none.
Steps in: the person relaunches.

### Loops that run alone

**A-1 — Cadreur ⇄ Vérificateur**
In: the sequence carries defects.
Stop: an empty defect list. Checkable — a section of `sequence.md`.
Bound: three rounds, counted by the Cadreur, then a blocking file
naming what did not converge. Sound; the Vérificateur's fresh context
each round is the price and it is stated.
Steps in: nobody; the person on the block.

**A-2 — Réalisateur ⇄ analysis and tests**
In: analysis or a test fails.
Stop: green. Checkable by the runner.
Bound: none stated — "par unité cohérente de travail", corrections
grouped. No count of attempts on one failure; a Réalisateur that cannot
make a test pass has only the Arbitre (a block) or its own stopping. A
test that cannot pass because the sheet is wrong is "un blocage" by
rule; a test that cannot pass because the Réalisateur misreads it is
bounded by nothing but its context. *(Estimate: the context is the
practical bound; it ends when the agent runs out of room, which is the
"ends when someone gets tired" shape.)* Tokens.
Steps in: nobody.

**A-3 — Réalisateur ⇄ Relecteur**
In: a FAIL (minor: fix the point; structural: redo the lot; a module
that does not compile is structural).
Stop: PASS. Checkable — `verdict.md`.
Bound: three retakes per lot, all FAIL kinds together, fresh Réalisateur
each time; then the command stops. Sound.
Steps in: nobody; the person after three.

**A-4 — Divergence → Détailleur**
In: a verdict names lots whose sheets a symbol divergence made false.
Stop: those sheets rewritten. Checkable by the command (the verdict
names them).
Bound: one rewrite per verdict; the rewritten sheets are then coded and
may diverge again — no count across verdicts, but each round codes a
lot, so it is bounded by A-3's count per lot. Sound.
Steps in: nobody.

**A-5 — Arbitre → Architecte**
In: a block that needs a convention.
Stop: a `## Verdict` written (rule text, or refusal). Checkable.
Bound: once, never twice; a refusal goes to the person. Sound; and the
Architecte writes no blocking file here so that two agents do not hang
on one answer — a boundary correctly drawn.
Steps in: nobody; the person on refusal.

**A-6 — Redecoupage — the loop without a ceiling**
Between: Arbitre (`code/redecoupage.md`) → the agent drops its work →
`/7_lots` (Cadreur, fresh cut of the uncoded lots; Vérificateur ×≤3) →
`/8_code` (sheets of uncoded lots deleted; Détailleur on the new block;
Réalisateur; Relecteur) → possibly the Arbitre again.
In: a block whose answer is "the split must make X possible".
Stop: no redecoupage file after the block is coded. Checkable only by
absence — there is no test that says "this redecoupage was the last".
Bound: none. The process's convergence mechanism is the Cadreur reading
the previous redecoupages and writing "ce qu'il en fait" — a
judgement, not a count. It names the failure mode itself ("le
cinquième redécoupage redit ce que le deuxième disait déjà") and
supplies no stop for it. `/8_code`'s `N` does not count it (A9);
`stop.md` is the person noticing. This is the loop that "ends when
someone gets tired", and it is the one that costs the most per turn:
a cut, up to three verifications, a block's sheets, a lot's code, a
review — every turn. Round trips (agent turns) and tokens.
Steps in: nobody, by design ("le Product Owner n'attend sur rien") —
which is exactly why it needs a ceiling the others do not.

**A-7 — Extracteur, domain after domain**
In: the domain list.
Stop: the list is exhausted; the rewiring pass has run. Checkable — the
command greps each domain's title between passes.
Bound: the list. On a failed domain "elle continue" and reports; the
re-run is by hand. Not a loop; listed because the file names it.
Steps in: the person, on failures.

**A-8 — `/cycle`**
In: a feature name.
Stop: any decision needed. Checkable by construction (a non-empty
questions file or a blocking file).
Bound: the chain's own.
Steps in: the person at every stop — it is a driver, and the process
says so.

---

## 6. What this chain takes for granted

Premises: what the chain never questions because its shape makes the
question unaskable. Some are sound; naming them is the work.

**P1 — The person answers files, offline, and never converses.**
Buys: a record per question, addressable by block; reproducible turns;
no agent that waits mid-sentence. Costs: round trips — every turn of
the upstream is a day, and a question the person would have settled in
one exchange costs a full route; a technical question on the product
route (D10) has no answerer at all. Without it: an agent that asks the
next question once it has the previous answer — hundreds of round trips
and no per-block record. The premise is sound; its cost is the
upstream's length, which the process accepts by name.

**P2 — Eight natures partition everything a program produces, and a
block's nature is at once its grid questions, its technical section
and its code layer.**
Buys: an exhaustive sweep (the Classeur, the Convertisseur per nature,
`/5_reclasse` by grep); one judge per block; the Cadreur's "one section
per lot". Costs: robustness in the shape of horizontal lots — a lot is
a layer, and the first end-to-end proof of a behaviour is the emulator
(section 1, break 2); and a block whose two sentences produce two
things must be split to fit the list, which is a product-file edit
forced by a technical taxonomy. Without it: lots cut by behaviour
across layers, each testable against a block; a technical document by
feature rather than by layer; and no closed vocabulary for the
Classeur — which the chain would have to replace with a coverage
argument it does not have. The trade is real in both directions; I
would not reverse it, but the cost lands on the measure that prevails.

**P3 — A whole-product technical document is written before the first
lot and frozen once cut.**
Buys: the Cadreur's inventory over the whole surface, `Consumes` as a
dependency graph, the Vérificateur's three defect classes, the
Contrôleur's traceability. Costs: tokens (the Convertisseur per nature
plus a transversale; the Cadreur reading it whole; the Architecte
reading it whole); and a rule with no exception — "un changement du
produit après le découpage appartient à un nouveau cycle" — so a
product answer that arrives during coding (U10) cannot update the
document the lots cite; the sheet carries the decision and the
technical document is silently behind it. Robustness of the record.
Without it: the shape of `proposition.md`, and the loss of the
Cadreur's reason to exist. The process's version is the one that has
run.

**P4 — Grep is knowledge: a symbol's name says what it is.**
Buys: agents that never open code files (Cadreur, Architecte, Arbitre
by grep, Détailleur by grep) and therefore never inherit an
implementation's reading; a bounded reading set on any code base.
Costs: robustness on an existing application whose names do not match
the product's terms — a `changed` symbol declared `new`, a caller not
found because "les appelants les plus proches ne déclarent rien de son
origine" (the process knows this case and answers with "grep the
name"); and conventions derived without ever seeing a line of the code
they govern (section 3). Without it: an agent that reads the functions
its greps hit — my Locator's "then the functions those hits sit in,
read whole" — at a cost of tokens per unit, once.

**P5 — Markers are memory: what is unmarked is closed and unchanged.**
Buys: every command narrows to what moved, by grep, with no diff and no
state file; the re-probing set shrinks turn after turn. Costs: a single
forgotten `MODIFIED` is a block never re-probed, with no detector
(D3); the Découpeur's halves depend on it (D4); and the confirm-as-is
answer leaves no trace (A1). Without it: a byte diff of the product
file between turns — which the chain already runs for the Convertisseur
— deciding what moved; markers would become a courtesy, not a
guarantee. Cheap; I would do it.

**P6 — The Rédacteur transcribes faithfully; the idea file is read
once.**
Buys: one whole-file reading of the idea instead of two or three;
every later agent works on a structured file. Costs: robustness — a
loss at structuring is invisible to everything after, including the
Contrôleur, and the Rédacteur is the only producer in the chain whose
output no separate context checks against its input (the Découpeur
checks form, not content; the Sondeurs probe what is there). Without
it: one Coverage invocation per feature after `/2_structure`, reading
`idees.md` and `desc-produit.md`, listing sentences with no block.
The cheapest robustness the chain does not buy.

**P7 — Closure is the grid answered; the grid is complete; the grid
is edited by hand.**
Buys: an enumerable, repeatable closure test; "une catégorie écartée est
déclarée écartée". Costs: a class the grid lacks is missed on every
feature until the person edits the file; the chain produces the
evidence (Architecte *couverture* gaps, Arbitre product blocks,
Contrôleur *douteux*) and writes none of it where the grid would read
it. Without it: a grid file that gains a line from each downstream
product question, with the block that proved it — the mechanism by
which "no decision left to the code" is approached rather than
asserted. Robustness across features.

**P8 — The command is the state machine, and it is an LLM session.**
Buys: agents that carry no state, whose reading sets are closed; a
folder that says what turn it is. Costs: the state logic (greps,
counts, byte compares, decision-line reads, routing tables) lives in
command files an LLM must follow exactly, and the process records the
cases where it did not (an absolute path, a stale base, an agent
invoked outside a worktree). Every one of those is a run lost, not a
gap in the code — round trips. Without it: a script, for the parts that
are greps and counts, and an LLM for nothing. The process is most of
the way there (`/5_reclasse`, `/9_controle`'s script, byte compares);
the remaining judgement in the commands is small and could be listed.

**P9 — A fresh context is a pair of eyes; independence costs tokens
and is worth them.**
Buys: the Vérificateur, the fresh Réalisateur on FAIL, the Sondeurs
that never read each other, the Contrôleur that never reads its own
previous report. Costs: tokens, stated each time. Sound; the one place
the premise is inverted (the Cadreur) is argued. I would keep every
instance.

**P10 — The sheet is self-sufficient, and the coder needs nothing
else.**
Buys: a Réalisateur with the smallest reading set in the chain and no
architecture to decide; a divergence that is always visible because
"improviser rendrait la divergence invisible". Costs: the Détailleur
must carry every applicable convention into the sheet (D12) and every
edge of every return; a sheet that omits one is a lot coded without it
and reviewed without it. Without it: a coder that reads the technical
document's cited entries — the Détailleur's job done twice. The premise
holds; D12 is the wire to check.

**P11 — Living documents stay true when the agent that changed the
code updates them.**
`CURRENT_TECHNICAL_STATE.md` by the Réalisateur; `PRODUIT_GLOBAL.md` by
the Fusionneur. Buys: a Cadreur and a Détailleur that read a description
of what exists rather than the code; a Rédacteur that greps an index
rather than a code base. Costs: the description drifts by exactly the
entries the updater did not know it made false (D22) and by the titles
nobody checks (D13); each drift is found one block or one feature later
as a divergence. Without it: agents that read the code — tokens per
lot, and no document to lie. The chain's answer — the Extracteur once,
the Diagnostiqueur by grep — is that the code stays the truth and the
documents are caches. Sound as long as a cache miss is cheap; D22 says
it costs a FAIL round.

**P12 — Product questions downstream are rare enough that each may
stop the command.**
Buys: a downstream that never converses and a person who "n'attend sur
rien". Costs: every downstream product block is a twenty-minute poll,
a stop, a relaunch (U10), and nothing learns from it (P7). Without it:
a queue — the Arbitre writes the question, the lot is skipped, the
sequence continues on lots that do not depend on it, and the person
answers a batch. The process's sequence already knows what depends on
what; the premise stops the whole run for one lot. Round trips.

**P13 — The whole product file fits one context wherever the chain
needs it whole.**
The Rédacteur writes it in one invocation; the global Sondeur records
every block every turn; the Fusionneur compares it whole; the Cadreur
reads the technical document whole; the Contrôleur reads all sheets
against all blocks (in groups, by script). The Convertisseur alone is
split by nature — "trois cents blocs fins ne se lit pas d'une traite".
Buys: no unit map, no per-unit files, one artefact. Costs: a ceiling
the process has met once (the Convertisseur) and will meet again at
the Rédacteur (write 300 blocks in one context) and the global Sondeur
(record 300 blocks, then cross columns) — and the failure mode of a
context that runs out is silent truncation, not a block. Without it:
units, and everything my design paid for them. The premise holds at
the sizes seen; it is the one that breaks by scale, not by logic.

**P14 — One chain fits every project.**
Buys: commands with one argument, no hardcoded path, the same agents on
a phone app and a watch app. Costs: none visible from the description;
the conventions file is where the project enters, and it is the
artefact with the most boundary defects here (D11, D12, D14, D16).
Named because it is why those defects matter more than their size.

---

## 7. What only the agents can settle

Each: the question, the file that would settle it, and what I would
conclude either way. This list is what the next phase carries into
each agent.

1. **Does the Découpeur write a marker on the blocks it creates?**
   `decoupeur.md`. Yes: D4 closes. No: a block split at turn ≥ 2 is
   classified but never probed by the angles — a re-probing hole, and
   the fix is one line.

2. **Does the Réalisateur read `TECHNICAL_CONVENTIONS.md` in full, or
   only what the sheet names?** `realisateur.md`, `detailleur.md`.
   Whole file: the Détailleur's naming is redundant (tokens) and the
   process's sentence about it is stale. Sheet only: every convention
   the Détailleur omits is silently unapplied (robustness), and the
   file table is wrong.

3. **Does the Cadreur read `CURRENT_TECHNICAL_STATE.md`?** `cadreur.md`.
   Yes: the AVAL file table is incomplete and the reading cost is
   undeclared. No: "ce document commande le Cadreur" is false, and
   production/modification is declared from grep alone — a `changed`
   symbol declared new on an existing app.

4. **Does the Architecte's invocation 1 run once per project or once
   per feature, and does it overwrite the shared file?** `architecte.md`
   and the `/conventions` command. Once per project: D11 dissolves.
   Once per feature, overwriting: every rule invocation 3 added during
   the previous feature is lost — the cross-feature inconsistency the
   agent exists to prevent.

5. **Where does the Cadreur's symbol inventory live, and does the
   Vérificateur read it from a file?** `cadreur.md`, `verificateur.md`.
   A section of `decoupage.md`: D18 closes. The Cadreur's context only:
   the Vérificateur's "surface non construite" check compares lots to
   lots — ratification.

6. **Are block identifiers stable across the Rédacteur's integration —
   never reused, never renumbered, a replaced block keeping its
   number?** `redacteur.md`. Yes: D2 closes. No or unstated: every
   `Block:` line, `[B12]` reference, `<<ASSUMED B40>>` and
   `tracabilite.md` line written before the integration may point at
   the wrong block.

7. **What does the Rédacteur write when an answer confirms a block as
   it stands?** `redacteur.md`. A trace in the block (a settled line, a
   marker): A1 closes and the Sondeur's no-memory rule is safe. Nothing:
   the question recurs whenever a neighbour marks the block, and the
   person answers it twice.

8. **Does the Relecteur compare a test's assertion to the criterion's
   outcome — or only count one test per criterion?** `relecteur.md`.
   Assertion strength: the chain's answer to "tester before coder"
   holds (section 3). Count only: a test that asserts "no crash" for a
   criterion that says "shows a dash" passes, and the Tester role is a
   real hole.

9. **Does the Relecteur flag a symbol or a branch no criterion asks
   for?** `relecteur.md`. Yes: invention is caught inside declared
   files. No: it is caught only by the out-of-lot file list, and the
   Reviewer-for-invention hole stands.

10. **Is text outside blocks in `desc-produit.md` probed by any
    Sondeur, and where do the preamble's dependencies live?**
    `sondeur.md`, `redacteur.md`, `convertisseur.md`. Probed: D9
    closes. Not probed: transverse rules and dependencies that
    constrain every block are the one part of the product file the
    grid never asks about.

11. **What is written to `cadrage-produit/closed/`, by whom, and who
    reads it?** `sondeur.md`. A named artefact with a reader: D7
    closes. Nothing: a folder from an earlier design, to remove from
    the command.

12. **Who reads `[integrated: B7]`?** `redacteur.md` and the
    `/2_structure` command. A check that every answer was integrated:
    it is the only such check and should be named. Nobody: tokens.

13. **Rename or delete a settled blocking file?** The five agent files
    the process names, against `cadreur.md`. Rename: the Arbitre's
    widening rule has its input. Delete: the Arbitre decides narrowly
    twice, and the "archive the next execution reads" does not exist.

14. **Does the Contrôleur (or `/9_controle`) read sheets from
    `bugfix-NN/code/`?** `controleur.md`, `/9_controle`. Yes: D23
    closes and the closing loop can be re-run. No: the second report
    is false by construction, and the loop U12 has no stop.

15. **When two natures name one concept two ways, does the transversale
    settle it or ask the person?** `convertisseur.md`. Settles: D10 is
    narrower (contradictions only). Asks: a technical choice travels a
    product route to someone who cannot make it.

16. **Does a fresh Réalisateur after a FAIL remove what the failed
    attempt wrote to `CURRENT_TECHNICAL_STATE.md`?** `realisateur.md`.
    Yes: D22 is only the unknown-entry case. No: every FAIL leaves an
    entry describing code that was thrown away, and the next block's
    Détailleur signs against it.

17. **Is there a bound on the Cadreur re-blocking with the same
    convention request after an Architecte refusal?** `cadreur.md`,
    `/7_lots`. Yes: U11 is bounded. No: the loop ends when the person
    reads the same block a third time.

18. **Does `/8_code` build the Contrôleur's groups, or call it without
    them?** `/8_code` and `controleur.md`. Builds them: contradiction 3
    is stale. Calls without: the end-of-cycle control does not run from
    the loop, and every feature's closing check is a manual command.

19. **Does the global Sondeur re-run pass A on every block to build the
    record, or reuse the angles' output?** `sondeur.md`. Re-runs: D6's
    token estimate stands — the largest reading of the upstream, every
    turn. Reuses: the angles' files are an input to the global, which
    contradicts "aucun ne lit la sortie d'un autre".

20. **Is `couverture.md`'s mechanical/reading table read by any command
    that wires a check?** `architecte.md`, `/conventions`. Yes: D14
    closes. No: a rule declared mechanical is enforced by a reading,
    and the table is a promise.

21. **Does the Détailleur, rewriting sheets after a divergence, re-walk
    the block first?** `detailleur.md`. Yes: the walk-before-write rule
    holds on rewrites. No: a rewritten sheet can contradict a sibling
    sheet the divergence did not name.

22. **Does the Réalisateur write tests before or after the bodies?**
    `realisateur.md`. Before, from the criteria: the tests assert the
    sheet, and the Tester hole narrows to assertion strength (item 8).
    After: they assert the code, and item 8 is the only guard.

23. **Does any agent or command diff the product file between turns?**
    `/3_decoupe`, `/4_grille`, `redacteur.md`. Yes: P5's cost is
    already paid for. No: a forgotten `MODIFIED` has no detector, and
    the cheapest robustness fix in the upstream is a byte compare the
    chain already knows how to do.

24. **Does the Architecte's invocation 3 record, in the verdict or the
    conventions, the lot that was coded before the rule?**
    `architecte.md`. Yes: D16 is a known divergence. No: the next lot
    touching the same file meets two styles with no note saying why.
