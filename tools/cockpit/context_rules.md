# Context rules — what a question is about

Cockpit 1.4. « À répondre » shows, beside the focused question, the
document it points to and the passage, highlighted. `context.py` reads
the target from the writer's own instructions — never a guess. A writer
whose target its instructions do not give shows no context, and the pane
says why. Read-only: the pane never writes.

Paths are relative to `.claude/` (`agents/…`, `commands/…`). The
document is relative to the folder the root questions file sits in.
`test_context.py` checks that each cited line still says what its rule
reads in it.

---

## 1. One row per writer

The writer is read from the file's name: `questions-<agent>-NN.md` at
the root, or `convertisseur/technique-<nature>.md`.

| Rule | File | Writer | Key | Points to | Document | Lines |
|---|---|---|---|---|---|---|
| `CTX-LEX12` | `questions-lexicographe-NN.md`, alone at the root | lexicographe, invocations 1-2 | `Terms:` | every occurrence of each term | `idees.md` | agents/lexicographe.md:311 · agents/lexicographe.md:318 · agents/lexicographe.md:103 · commands/1_lexique.md:158 |
| `CTX-LEX34` | `questions-lexicographe-NN.md`, beside one other agent's file | lexicographe, invocations 3-4 | `Terms:` | every occurrence of each term in the `Answer:` fields, and in the `Défaut:` line of an entry whose `Answer:` is empty | the other agent's file — *the answered file* | agents/lexicographe.md:539 · agents/lexicographe.md:440 · agents/lexicographe.md:445 · commands/1_lexique.md:62 · commands/1_lexique.md:65 |
| `CTX-RED` | `questions-redacteur-NN.md` | redacteur | `Block:` | the `### B<n>` section of each block named | `desc-produit.md` | agents/redacteur.md:315 · agents/redacteur.md:34 · agents/redacteur.md:338 |
| `CTX-GEN` | `questions-qualifieur-NN.md` | qualifieur | `Block:` | the same | `desc-produit.md` | agents/qualifieur.md:197 · agents/qualifieur.md:204 · commands/3a_genre.md:169 |
| `CTX-NAT` | `questions-classeur-NN.md` | classeur | `Block:` | the same | `desc-produit.md` | agents/classeur.md:148 · agents/classeur.md:155 · commands/3b_nature.md:171 |
| `CTX-GRI` | `questions-sondeur-NN.md` | sondeur, inv. 1-2, merged by the assembleur, copied by `/4_grille` | `Block:` | the same | `desc-produit.md` | agents/sondeur.md:399 · agents/sondeur.md:471 · agents/assembleur.md:140 · commands/4_grille.md:568 · commands/4_grille.md:388 |
| `CTX-EXI` | `questions-existant-NN.md` | sondeur, invocation 3 | `Block:` | the feature's block — never one of the global | `desc-produit.md` | agents/sondeur.md:280 · agents/sondeur.md:281 · commands/4_grille.md:388 · commands/4_grille.md:395 |
| `CTX-CNV` | `questions-convertisseur-NN.md` | convertisseur, product questions, merged by `/6_convertit` | `Block:` | the same | `desc-produit.md` | agents/convertisseur.md:476 · agents/convertisseur.md:487 · agents/convertisseur.md:58 · commands/6_convertit.md:363 · commands/6_convertit.md:375 |
| `CTX-TEC` | `convertisseur/technique-<nature>.md` | convertisseur, technical questions | `Entries:` | the `§n.m` heading of each entry named | `convertisseur/<nature>.md` — its own section; `spec-technique.md` for `technique-transversal.md` | agents/convertisseur.md:427 · agents/convertisseur.md:436 · agents/convertisseur.md:438 · agents/convertisseur.md:60 · agents/convertisseur.md:66 · agents/convertisseur.md:336 |
| `CTX-ARC` | `questions-architecte-NN.md` | architecte | `Block:` | the `§n.m` heading of each entry named | `spec-technique.md` | agents/architecte.md:579 · agents/architecte.md:367 · agents/architecte.md:614 |
| `CTX-FUS` | `questions-fusionneur-NN.md` | fusionneur | `Block:` | the `### B<n>` section of each block named | `desc-produit-fusion.md` — 🔴 never `desc-produit.md` | agents/fusionneur.md:116 · agents/fusionneur.md:47 |

The writers are the eleven of `docs/app/analyse-v1.md` §A: the
assembleur and `/4_grille` write the sondeur's shape, `/6_convertit`
the convertisseur's — one row each above.

---

## 2. What has no context, and says so

| Case | Why | Lines |
|---|---|---|
| `Block: -` (any `Block:` writer) | « the question is about the feature and not about a block » — nothing to point at | agents/redacteur.md:344 · agents/sondeur.md:482 · agents/assembleur.md:142 |
| A lexicographe file beside **two** other agents' files | `/1_lexique` stops there — which file was swept is not said | commands/1_lexique.md:63 |
| An architecte question naming a grid entry, no `§` — a `forme` question, or the `coverage` question G4.4 raises when the corpus names nothing the application runs on | « its `Block:` names the grid entry », « its `Block:` naming `G4.4` » — the grid is the Product Owner's, outside the feature | agents/architecte.md:614 · agents/architecte.md:178 |
| A technical question whose `Entries:` holds only bracket references, or names the nature | « or the nature, when no entry exists yet »; a bracket is « outside » the section | agents/convertisseur.md:436 · agents/convertisseur.md:337 |
| A fusionneur title question | its `Block:` shape is the block's (agents/fusionneur.md:116); a title is a section of the global, and no rule names how the entry points to it | agents/fusionneur.md:174 |
| A file of an agent no row names (`questions-<agent>-NN.md` of an agent the chain does not have) | no instruction gives its target | — |

**Every writer of §1 has a target.** No writer of the eleven is left
without context; only the cases of §2 are, entry by entry.

---

## 3. How a passage is found

- **Terms** — `Terms:` is split on its commas, and only there (« carries
  the terms, comma-separated », agents/lexicographe.md:318). Each term is
  matched **as a whole**: its words in order, case ignored, any run of
  spaces or one line break between two words — never a single word of a
  multi-word term. Whole words: `atelier` never matches `ateliers`. Where
  two terms start at the same place, the longer wins: `bloc final`, not
  `bloc`. Several occurrences → « 1 / 5 », previous and next, `←` and `→`.
- **A block** — the heading `#… B<n>` (the title and a marker after it
  allowed), down to the next heading of the same level or higher.
- **An entry** — the heading `#… §n.m`, down to the next heading of the
  same level or higher.
- **Not found** — the document is missing, or holds none of what the
  entry names: the pane says so, plainly, and shows nothing highlighted.
