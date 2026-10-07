# PROCESS_MECANISMES.md — ce que toute la chaîne partage

> Document de pilotage, en français. Il décrit les protocoles qu'au
> moins deux agents ou deux commandes emploient sous la même forme, et
> les ensembles de valeurs fermés que plus d'un agent touche. Un
> protocole à un seul utilisateur n'est pas ici : il est renvoyé, en fin
> de document, au document de parcours qui le porte.

## Carte des cinq documents

| Document | Ce qu'il tient |
|---|---|
| `PROCESS_MECANISMES.md` | Ce document. Le fichier de blocage, le fichier de questions, `stop.md`, la forme d'un relais et sa ligne `Next:`, le renommage `-NN` et l'archivage, l'invocation d'un agent et son frontmatter, les sections Git et worktree, les protocoles de lecture, la disposition du dossier de feature, les ensembles de valeurs fermés. Il énonce aussi, une fois pour les cinq, le périmètre d'audit. |
| `PROCESS_ENTREES.md` | Les trois entrées de la chaîne — `idees.md`, `socle.py` (le script que le cockpit lance à la création d'une application, `/socle` jusqu'au cockpit 1.7), `/diagnostique` — ce que chacune garantit à ce qui suit, et ce qu'elle laisse manquant. Une quatrième, `/extrait`, n'existe pas : ni commande, ni agent, absente de `CLAUDE.md` — la carte ne la nomme pas comme entrée, parce qu'une carte qui nomme une commande que personne ne peut lancer trompe son lecteur ; mais le fait qu'elle a été retirée, et comment le global naît à sa place (`INIT` du Fusionneur sur la première feature fusionnée), est ce que la section enregistre → `PROCESS_ENTREES.md` §/extrait. |
| `PROCESS_AMONT.md` | De l'idée à `spec-technique.md` : `/1_lexique` à `/6_convertit`, plus `/conventions` et la fusion (`/fusion`, `/fusion_compare`, `/fusion_applique`). Les agents lexicographe, redacteur, decoupeur, qualifieur, classeur, sondeur, assembleur, convertisseur, fusionneur, architecte. |
| `PROCESS_AVAL.md` | De `spec-technique.md` au code fusionné : `/batir`, `/7_lots`, `/8_code`, `/9_controle`. Les agents batisseur, cadreur, verificateur, detailleur, arbitre, concepteur, testeur, realisateur, relecteur, controleur. |
| `PROCESS_ANNEXES.md` | Hors périmètre d'audit : ce qui ne change aucun artefact que la chaîne produit. |

**Les trois marques de lien**, chacune réservée à un seul usage :

| Marque | Ce qu'elle lie | Où elle s'écrit |
|---|---|---|
| `→ MECANISMES §<nom>` | Une définition partagée. `<nom>` est le titre `###` exact de la section de ce document ; la définition vit ici et nulle part ailleurs. | En ligne, dans la phrase qui en a besoin, dans les quatre documents de parcours. |
| `## Coutures` | Une passation qui franchit la frontière d'un document. Une ligne par passation, sous la forme `\| Ce qui part \| Ce qui arrive \| Ce que le receveur vérifie \| L'autre document \|`. Une couture est écrite des deux côtés. | Section obligatoire en fin de chacun des quatre documents du périmètre. |
| `## Boucles` | Une boucle qui traverse plusieurs agents et plusieurs commandes. Une entrée par boucle : `Ouverte par`, `Fermée par`, `Plafond`, `Au plafond`, `Traverse`. Une boucle qui franchit deux documents est écrite dans les deux. `aucune` quand il n'y en a pas. | Section obligatoire en fin de chacun des quatre documents du périmètre, à côté de `## Coutures`. |
| `### <agent> — invocation depuis <commande>` | Un agent invoqué depuis deux côtés : décrit en entier dans le document de la commande qui l'invoque en premier dans un parcours nominal, porté en entrée courte dans l'autre — `Ce qui change :` et `Description complète : <document> §<agent>`. Jamais une seconde description entière, jamais un simple pointeur. | Dans le document de parcours qui ne porte pas la description entière. |

## Périmètre d'audit

Quatre documents sont audités : `PROCESS_MECANISMES.md`, `PROCESS_ENTREES.md`, `PROCESS_AMONT.md`, `PROCESS_AVAL.md`. Un seul ne l'est pas : `PROCESS_ANNEXES.md`.

Le critère est unique : une annexe change aucun artefact que la chaîne produit. Ce qui y figure est vérifié au fichier, jamais supposé — `/deploie` (fourni par chaque application, la chaîne n'en porte aucun), `/audit_blocages` et `/audit_conventions` (lisent et rapportent dans `audit-blocages.md` et `audit-conventions.md`, que rien dans la chaîne ne relit), `.claude/scripts/coherence.py`, `docs/process/GRILLE_CONVENTIONS_RETIREES.md`. `.claude/scripts/grouper.py` n'est pas une annexe, et voici l'argument, tenu ici seul : `/9_controle` l'appelle en phase 2 (`.claude/commands/9_controle.md`, ligne 232 : `python .claude/scripts/grouper.py docs/features/<name>/tracabilite-full.md --auto`) et prend son regroupement tel qu'imprimé (ligne 238 : « Take the grouping it prints, unchanged. Never regroup by hand, never override the budget ») ; chaque ligne `G<n>` qu'il imprime devient les lignes `Group:`, `Blocks:` et `Sheets:` d'une invocation du Contrôleur (lignes 267-269), dont la sortie est `code/controle/<group>.md` puis, à l'assemblage, `code/rapport-controle.md`. Sa sortie façonne donc un rapport que la chaîne garde ; il appartient à `PROCESS_AVAL.md` §/9_controle — confronter le fichier produit à toutes les fiches, qui décrit ce qu'il fait — son entrée, sa sortie, ce que la commande en prend sans y toucher — et ne redit pas cet argument.

Ce périmètre, et cet argument, sont énoncés ici et nulle part ailleurs dans les cinq documents : les autres documents y renvoient par `→ MECANISMES §Périmètre d'audit`.

## Comment lire une entrée

Un protocole : `Utilisé par:` nomme tous ses utilisateurs, agents et commandes — jamais un seul. Vient ensuite sa description, assez complète pour le reconstruire (fichiers, chemins, sections, champs, à l'orthographe exacte des fichiers source), puis ce qu'il coûte et ce qui a été écarté : `raison :` n'est remplie que depuis une source ouverte — l'agent, la commande, `docs/verification4/`, `docs/verification3/`, `docs/verification2/` — sinon `raison : à retrouver` ; le statut est `éprouvée` quand le fichier ou le dossier de campagne dit qu'un run l'a exercée, `non éprouvée` quand la campagne dit qu'elle a été tranchée et jamais exécutée (toute décision de `docs/verification4/plan.md`, appliquée le 2026-09-21, aucun run depuis), `inconnu` sinon.

Un ensemble fermé : `Écrit par:`, `Lu par:`, `Les valeurs:` — toutes, une par ligne, avec son test. Un lecteur qui en énumère moins que le scripteur est dit : `Divergence : <agent> n'énumère que …`.

Une section dont le titre porte `— divergence` décrit un mécanisme que deux utilisateurs emploient sous des formes différentes : chaque variante est décrite, et la section ne prétend pas à un protocole unique.

---

# Les agents et leur invocation

### Frontmatter d'un agent

Utilisé par: les vingt et un agents ; `CLAUDE.md` ; toutes les commandes qui invoquent (`/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/batir`, `/7_lots`, `/8_code`, `/9_controle`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique`) ; les quatre agents qui en invoquent un autre (cadreur, detailleur, realisateur, arbitre).

Chaque fichier `.claude/agents/<agent>.md` ouvre sur un frontmatter YAML à cinq clés au plus : `name`, `description`, `tools`, `model`, `effort`. `tools` est la liste des outils que le harnais donne à l'agent — un agent sans `Bash` ne commite rien, un agent sans `Glob` ne liste aucun dossier, un agent sans `Agent` n'invoque personne. `model` vaut `opus` ou `sonnet` et c'est cette valeur, jamais une autre, que le `model=` de l'appel reprend. `effort` est facultatif ; son absence sur un agent qui copie ou classe est voulue.

| Agent | `tools` | `model` | `effort` |
|---|---|---|---|
| lexicographe | Read, Grep, Glob, Edit, Write | opus | aucun |
| redacteur | Read, Grep, Glob, Edit, Write | sonnet | high |
| decoupeur | Read, Grep, Edit, Write | opus | aucun |
| qualifieur | Read, Grep, Edit, Write | sonnet | aucun |
| classeur | Read, Grep, Edit, Write | sonnet | aucun |
| sondeur | Read, Grep, Write | opus | aucun |
| assembleur | Read, Write | sonnet | aucun |
| convertisseur | Read, Grep, Glob, Edit, Write | opus | high |
| fusionneur | Read, Grep, Glob, Edit, Write | sonnet | high |
| diagnostiqueur | Read, Grep, Glob, Write | sonnet | medium |
| architecte | Read, Grep, Glob, WebSearch, WebFetch, Edit, Write | opus | high |
| batisseur | Read, Grep, Glob, Edit, Write, Bash | sonnet | aucun |
| cadreur | Read, Grep, Glob, Edit, Write, Agent | opus | high |
| verificateur | Read, Grep, Glob, Write | opus | high |
| detailleur | Read, Grep, Glob, Edit, Write, Agent | opus | high |
| arbitre | Read, Grep, Glob, Edit, Write, Bash, Skill, Agent | opus | high |
| concepteur | Read, Grep, Glob, Edit, Write, Bash | sonnet | aucun |
| testeur | Read, Grep, Glob, Edit, Write, Bash | sonnet | aucun |
| realisateur | Read, Grep, Glob, Edit, Write, Bash, Skill, Agent | sonnet | high |
| relecteur | Read, Grep, Glob, Write | sonnet | medium |
| controleur | Read, Grep, Glob, Write | sonnet | high |

Ce que la table établit : neuf agents sur `opus` (arbitre, architecte, cadreur, convertisseur, decoupeur, detailleur, lexicographe, sondeur, verificateur — la liste de `CLAUDE.md` concorde) ; cinq agents portent `Bash` (arbitre, batisseur, concepteur, testeur, realisateur) et eux seuls commitent ou lancent une commande ; quatre portent `Agent` (cadreur, detailleur, arbitre, realisateur) ; deux portent `Skill` (arbitre, realisateur — la compétence `technical-state-format`, chargée avant toute écriture dans `docs/CURRENT_TECHNICAL_STATE.md`) ; un seul lit le web (architecte). Aucun agent n'a d'outil qui renomme ou supprime un fichier hors du `Bash` des cinq, et le shell de ces cinq est borné (→ `### Bash des agents — divergence`).

Le registre des agents est figé à l'ouverture de session : un fichier ajouté ou renommé sous `.claude/agents/` est invisible jusqu'au redémarrage (`CLAUDE.md`).

Coût et écarté : `effort` sur tous les agents · écarté : la règle d'un `effort` obligatoire · raison : `effort` est réservé aux agents dont le travail est un jugement, son absence sur un agent qui copie une signature ou classe une question est voulue (`CLAUDE.md`, *Model assignment* ; `docs/verification2/concepteur.md` B-7, moot) · inconnu. Une liste `tools` large par défaut · écarté : donner `Bash` à un agent qui n'en a pas l'usage · raison : `docs/verification3/fichiers.md` F01 — les fichiers d'un agent sans shell restent non commités si la commande ne le fait pas ; c'est la commande qui commite, pas l'agent qu'on équipe · inconnu.

### Frontmatter d'une commande

Utilisé par: les dix-neuf commandes de la chaîne.

Chaque `.claude/commands/<commande>.md` ouvre sur `description`, `allowed-tools` et `argument-hint`. Les seize commandes qui invoquent un agent portent `allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent` ; `/5_reclasse` : `Read, Grep, Glob, Write, Bash` ; `/audit_blocages` et `/audit_conventions` : `Read, Grep, Glob, Edit, Write`. `argument-hint` vaut `"<feature folder name>"` partout sauf `/8_code` (`"<feature folder name> [N]"`) ; `/conventions` lit un second argument nommant un `bugfix-NN` bien que son `argument-hint` n'en dise rien. Le premier argument est obligatoire : sans lui la commande demande et s'arrête ; `$ARGUMENTS` porte les deux quand il y en a deux, et le dossier de feature se dérive du premier seul.

Coût et écarté : aucun écart connu · raison : à retrouver · inconnu.

### Invocation d'un agent

Utilisé par: `CLAUDE.md` ; `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/batir`, `/7_lots`, `/8_code`, `/9_controle`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique` ; cadreur, detailleur, realisateur, arbitre.

L'outil est `Agent`, au schéma strict — une clé inconnue est rejetée. Quatre paramètres sont passés, jamais d'autre :

| Paramètre | Valeur |
|---|---|
| `subagent_type` | Le nom du fichier d'agent : `lexicographe` · `redacteur` · `decoupeur` · `qualifieur` · `classeur` · `sondeur` · `assembleur` · `convertisseur` · `architecte` · `fusionneur` · `diagnostiqueur` · `batisseur` · `cadreur` · `verificateur` · `detailleur` · `concepteur` · `testeur` · `realisateur` · `relecteur` · `arbitre` · `controleur` |
| `model` | Ce que le frontmatter de l'agent dit, `opus` ou `sonnet`. Une exception : le troisième realisateur d'un lot dont `## Causes so far` porte deux fois `reasoning` est passé en `opus` (`/8_code`) |
| `description` | Trois à cinq mots, pour le suivi de contexte — `"Sweep <name>'s vocabulary"`, `"Detail block-2 sheets"`, `"Requests <the working folder>"` |
| `prompt` | Les entrées de l'agent et les paramètres de l'appel, rien d'autre — jamais une paraphrase du processus de l'agent, de ses entrées, de ses vérifications, de son format de sortie |

Ce qui n'est jamais passé : `effort` (frontmatter seulement), `isolation` (chaque appel brancherait à neuf et ne verrait pas ce que la phase précédente a écrit), `run_in_background` (l'outil est asynchrone dans cet environnement et notifie à la fin ; on attend la notification), `mode`, `team_name`. `name` est facultatif et rend l'agent adressable pendant qu'il tourne.

Le prompt est fait de lignes à forme fixe, que l'agent lit et sur lesquelles il aiguille :

| Ligne | Qui la porte |
|---|---|
| `Feature folder: docs/features/<name>/.` | redacteur, convertisseur, controleur, fusionneur, architecte (invocations 1, 2, 4) |
| `Working folder: <the working folder>.` | batisseur, cadreur, verificateur, detailleur, arbitre, architecte (invocation 3), concepteur, testeur, realisateur, relecteur |
| `Conventions: <commit>.` · `Blocking file: blocked_batisseur.md.` | batisseur |
| `Bug-fix folder: docs/features/<name>/bugfix-NN/.` | diagnostiqueur |
| `The product file: docs/features/<name>/desc-produit.md.` | decoupeur, qualifieur, classeur, sondeur |
| `The idea file:` · `The lexicon:` · `The grid:` · `The global:` | lexicographe ; sondeur |
| `Invocation <N> — <nom>.` | Tout agent à plusieurs invocations (→ `### Numéros d'invocation`) |
| `Look at these blocks: <liste>` ou `every block` | decoupeur (les mots *every block* sont sa clé), qualifieur, classeur |
| `Pass A on these blocks:` · `every behaviour block:` · `The transverse blocks, to hold beside them:` · `The out-of-scope blocks:` · `Your reading order:` · `Write to` · `Write the record to` | sondeur |
| `These blocks, with the global section each names:` · `Your blocking file, if you cannot produce:` | sondeur, invocation 3 |
| `Your questions file number: NN.` · `Questions file number: <NN>.` | qualifieur, classeur, architecte, fusionneur |
| `Your answered questions file:` · `The answered file:` · `The questions file to apply:` · `Answered file:` | qualifieur, classeur, lexicographe, architecte |
| `Merge, in docs/features/<name>/cadrage-produit/: …` | assembleur |
| `Called by the orchestration.` · `Called by the Arbitre.` | architecte, invocation 3 |
| `Gap G01: <texte>` | diagnostiqueur, invocation 1 |
| `Your lot: <lot>.` · `Your block: <block>.` | concepteur, testeur, realisateur, relecteur ; detailleur |
| `Mode: divergence.` · `Affected lots:` · `Findings: <copié>` | detailleur |
| `Verdict: code/<lot>/verdict.md.` | realisateur, sur une reprise après FAIL seulement |
| `Files the lot's commits changed: <liste>` | relecteur |
| `Blocking file: code/…` | arbitre |
| `Group:` · `Blocks:` (avec `(carried)`) · `Sheets:` · `Groups issued this run:` · `Blocks per group, one line each:` | controleur |
| `Decisions files, in cycle order:` | redacteur, invocation 3 |
| La ligne du fichier de blocage rempli | Tout agent qu'on relance sur décision — → `### Reprise sur décision — divergence` |

La ligne du fichier de blocage prend deux graphies selon la commande : `<Plus: <chemin>/blocked_<agent>.md, its decision is filled.>` (les commandes amont, `/8_code`, `/4_grille`) et `[Blocking file: <chemin>/blocked_<agent>.md — its ## Decision is filled.]` (`/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique`) ; `/8_code` écrit `<Plus: Blocking file: blocked_architecte.md, its decision is filled.>` pour l'Architecte. L'agent lit dans les deux cas « le fichier de blocage que le prompt nomme ».

Plusieurs appels indépendants partent dans un seul message (les quatre sondeurs de `/4_grille`, les natures de `/6_convertit`, les manques de `/diagnostique`, les groupes de `/9_controle`) ; en plusieurs messages ils tourneraient en série. La commande attend chacun avant d'aller plus loin.

Coût et écarté : un appel par invocation, la commande recalculant l'état du dossier entre deux · écarté : passer `isolation` · raison : l'isolation brancherait chaque appel à neuf et une phase ne verrait pas ce que la précédente a écrit (`CLAUDE.md`, *Agent invocation* ; `docs/verification2/correction.md`, *Git, in this mode*) · inconnu. Attendre la notification · écarté : `run_in_background` · raison : le paramètre peut ne pas exister et l'outil notifie de lui-même (`CLAUDE.md`) · inconnu. Ne rien paraphraser du processus · écarté : redire à l'agent ce qu'il doit faire · raison : une paraphrase entre en concurrence avec les instructions que l'agent lit dans son propre fichier (`/7_lots`, *How it runs*) · inconnu.

### Numéros d'invocation

Utilisé par: chaque agent à plusieurs invocations et la commande qui le nomme.

L'invocation est toujours dite par le prompt, jamais déduite du dossier — l'orchestrateur a regardé, l'agent ne regarde pas deux fois. La ligne vaut `Invocation <N> — <nom>` ; un agent à une seule invocation n'en porte pas.

| Agent | Invocations, telles que le prompt les nomme | Qui les nomme |
|---|---|---|
| lexicographe | `1 — Sweeping` · `2 — Settling` · `3 — Watching` · `4 — Correcting` | `/1_lexique` |
| redacteur | `1 — Structuring` · `2 — Integrating` · `3 — Merging` | `/2_structure` (1, 2) · `/fusion` (3) |
| decoupeur · qualifieur · classeur · assembleur | une seule | `/3_decoupe` · `/3a_genre` · `/3b_nature` · `/4_grille` |
| sondeur | `1 — Angle` (trois à la fois, un par ordre de lecture) · `2 — Global` · `3 — Existant` | `/4_grille` |
| convertisseur | `1 — Nature: <nature>` (une par nature, à la fois) · `2 — Transversal` | `/6_convertit` |
| fusionneur | `1 — Compare and question` · `2 — Apply` · `3` (*Bug-fix decisions* dans le fichier de l'agent) | `/fusion_compare` (1) · `/fusion_applique` (2) · `/fusion` (1, 2, 3 par sa table de routage) |
| architecte | `1 — Deriving` · `2 — Integrating` · `3 — Requests` · `4 — Completing` | `/conventions` (1 à 4) · `/7_lots`, `/8_code`, arbitre (3) |
| diagnostiqueur | `1 — Investigation` (un appel par manque) · `2 — Assembly` | `/diagnostique` |
| cadreur | une seule ; aiguille elle-même sur les blocs A, B, C, D d'après le disque | `/7_lots` |
| verificateur · arbitre | une seule | cadreur · detailleur et realisateur |
| detailleur | mode ordinaire ; `Mode: divergence` sur cette ligne seule | `/8_code` |
| concepteur · testeur · realisateur · relecteur | une par lot | `/8_code` |
| controleur | `1 — Confront` (un par groupe) · `2 — Assembly` | `/9_controle` |

Deux invocations d'un même agent ne lisent ni n'écrivent la même chose ; les documents de parcours les décrivent en blocs séparés.

Coût et écarté : le numéro dans le prompt · écarté : l'agent déduit son invocation de ce qu'il trouve · raison : « never inferred from the folder — the orchestrator looked, you do not look again », dans chaque agent à invocations · inconnu.

### Appel d'agent à agent

Utilisé par: cadreur (→ verificateur) ; detailleur (→ arbitre) ; realisateur (→ arbitre) ; arbitre (→ architecte) ; `CLAUDE.md`.

Quatre agents portent `Agent` et l'emploient dans un seul dialogue chacun : le Cadreur invoque `verificateur` (`model="opus"`, `description="Check split <the working folder>"`, prompt `Working folder: <the working folder>.`), jusqu'à trois fois sur un découpage, un Vérificateur neuf à chaque tour ; le Détailleur et le Réalisateur invoquent `arbitre` (`model="opus"`, `description="Settle <block>"` / `"Settle <lot>"`, prompt `Working folder: …` puis `Blocking file: code/blocked_detailleur.md` / `code/<lot>/blocked_realisateur.md`) sur le fichier qu'ils viennent d'écrire ; l'Arbitre invoque `architecte` (`model="opus"`, `description="Requests <the working folder>"`, prompt `Working folder: …. Invocation 3 — Requests. Called by the Arbitre.`) une fois par invocation. L'appelant garde son contexte, attend sans borne — pas de sondage, pas de délai — et lit ce que l'appelé a écrit sur disque : `## Defects` de `code/sequence.md`, `## Decision` du fichier de blocage, `## Verdict` de la requête. Ce que l'appelé retourne en message n'est qu'un accusé. Tout autre appel passe par l'orchestrateur ; aucun agent n'invoque personne d'autre.

Coût et écarté : un dialogue tenu dans le contexte de l'appelant · écarté : router chaque échange par l'orchestrateur · raison : mesuré, un sous-agent qui invoque garde son contexte et reprend après (`CLAUDE.md`, *Agent invocation*) ; le Cadreur corrige contre le découpage qu'il a encore en tête (`cadreur.md`, *Then call the Vérificateur, and wait*) · éprouvée. Attente sans borne · écarté : un délai · raison : on attend un agent, pas une personne ; seule l'attente du Product Owner est cadencée, et seul l'Arbitre la fait (`CLAUDE.md`) · inconnu.

### Chemins relatifs

Utilisé par: les vingt agents ; `CLAUDE.md` ; toutes les commandes créant un worktree.

Tout chemin qu'un agent lit ou écrit est relatif — `docs/features/…`, jamais `C:\…` ni `/…` — parce que l'agent tourne dans un worktree dont la racine n'est pas celle du projet ; un chemin absolu pointe sur le dépôt principal, hors de la session isolée, et l'écriture échoue. Deux racines coexistent : un chemin qui commence par `docs/` ou `.claude/` est relatif à la racine du dépôt (`docs/TECHNICAL_CONVENTIONS.md`, `docs/CURRENT_TECHNICAL_STATE.md`, `docs/PRODUIT_GLOBAL.md`, `.claude/grids/GRILLE_*.md`) ; tout autre chemin est relatif au dossier que le prompt nomme (`Feature folder:`, `Working folder:`, `Bug-fix folder:`). Le Diagnostiqueur ajoute que les emplacements du code — le fichier d'un porteur, un dossier cherché, un manifeste — sont eux aussi relatifs à la racine du dépôt ; le Concepteur, que les fichiers de code qu'il écrit le sont, seuls `code/<lot>/…` étant sous le dossier de travail.

Coût et écarté : deux racines à tenir · écarté : un chemin absolu · raison : l'écriture sort de la session isolée et échoue (`CLAUDE.md`, *Worktrees*) · inconnu.

### Dossier de travail

Utilisé par: `/7_lots`, `/8_code`, `/9_controle`, `/audit_blocages`, `/audit_conventions`, `/conventions` (invocation 3), `/diagnostique` ; `/batir` (l'exception : le dossier de feature, toujours) ; batisseur, cadreur, verificateur, detailleur, arbitre, architecte, concepteur, testeur, realisateur, relecteur, diagnostiqueur.

Le dossier de travail est le `bugfix-NN/` de numéro le plus haut dans `docs/features/<name>/` s'il en existe un, le dossier de feature lui-même sinon. Un cycle de correction garde tout ce qu'il produit dans son propre dossier, à la même structure : le document technique à la racine — `spec-technique.md` pour une feature, `desc-bug.md` pour une correction, jamais les deux — et `code/` à côté, plus `architecte/`. Les commandes aval dérivent le dossier du nom de feature et passent le dossier de travail dans le prompt, jamais le dossier de feature ; l'agent reconnaît le cycle au document qu'il y trouve. Deux fichiers restent à la racine du dossier de feature quel que soit le dossier de travail : `par-genre/recette.md` et `registre-questions.md` ; `couverture.md` aussi, que l'Architecte écrit sur la feature et que `/audit_conventions` cherche un niveau au-dessus. `/9_controle` lit les phases 1 à 3 sur le dossier de feature et 4 à 6 sur le dossier de travail. `/diagnostique` exige le `bugfix-NN/` et son `bug-list.md`, créés à la main par le Product Owner, et n'en crée jamais.

Coût et écarté : deux dossiers à distinguer sur un cycle de correction · écarté : un seul dossier par feature · raison : un cycle de correction est un cycle aval entier, avec son propre document technique et son propre `code/` — `spec-technique.md` et `desc-bug.md` n'existent jamais ensemble, le dossier qui porte les deux est un défaut sur lequel le Cadreur s'arrête ; le cycle garde donc tout ce qu'il produit dans son propre dossier, à la même structure, et c'est le dossier de travail qu'on passe, jamais le dossier de feature, car sur une correction ils diffèrent et l'agent lirait le mauvais (PROCESS_AVAL-avant-refonte.md L26-29, L883-890) · inconnu.

---

# Les fichiers de blocage

### Fichier de blocage — divergence

Utilisé par: lexicographe, redacteur, decoupeur, qualifieur, classeur, sondeur, assembleur, convertisseur, fusionneur, architecte, diagnostiqueur, batisseur, cadreur, verificateur, detailleur, concepteur, testeur, realisateur, relecteur (dix-neuf scripteurs ; l'arbitre en remplit le `## Decision`, le controleur n'en écrit jamais) ; toutes les commandes qui invoquent.

Le noyau commun : quand produire est impossible — une entrée manquante, un fichier nommé absent, une prémisse fausse, une signature inécrivable — l'agent écrit un fichier `blocked_<nom>.md` à un emplacement fixé d'avance (→ `### Emplacement des fichiers de blocage`), au lieu de seulement le dire : un message de réponse se perd, un fichier non. Bloquer n'est pas signaler : un doute, une lacune, une contradiction vont dans le fichier de questions et le cycle continue ; on ne bloque jamais par prudence. Le titre `## Decision` est écrit vide et jamais omis — c'est là que le Product Owner répond à la main, et c'est ce que les commandes greppent (`grep -A2 '^## Decision$'`). L'agent ne renomme jamais son fichier ; la commande le fait une fois que l'agent a rapporté avoir appliqué la décision (→ `### Renommage -NN — divergence`). Le fichier de blocage est fusionné et poussé comme le reste : le Product Owner doit le voir.

Cinq formes coexistent, et un lecteur qui les confond se trompe :

**Forme 1 — quatre titres, un bloc par fichier.** `## What blocks` (le fait, en une phrase), `## Where` (le bloc, la section, le fichier, le symbole), `## To resume` (la décision ou la correction attendue), `## Decision` (vide). Scripteurs : decoupeur, sondeur, assembleur, convertisseur, diagnostiqueur, batisseur, cadreur, concepteur, testeur, relecteur — le batisseur sans `Options:`, et sur un outil de build introuvable son `## To resume` est un tutoriel en français, pas à pas, qui finit sur ce qu'il faut écrire sous `## Decision`. Le lexicographe énonce les quatre mêmes champs (`What blocks`, `Where`, `To resume`, `Decision`) sous forme de table, sans montrer le `##` — `/1_lexique` greppe pourtant `## Decision` ; c'est le défaut que `docs/verification3/plan.md` entrée 63 a corrigé chez le decoupeur, et que le fichier du lexicographe présente encore. Le Cadreur, quand son fichier existe déjà avec un `## Decision` rempli, n'écrit pas par-dessus : il ajoute un jeu neuf des quatre titres en dessous, et la commande lit le dernier `## Decision` du fichier.

**Forme 2 — cinq titres, `## Invocation` en tête.** `## Invocation` (1, 2 ou 3 ; 1 à 4 pour l'architecte), puis les quatre de la forme 1. Scripteurs : redacteur, fusionneur, architecte. La ligne route le fichier : le redacteur a trois invocations et un seul nom de fichier, et `/2_structure` lit 1 ou 2, `/fusion` lit 3 ; `/fusion_compare` et `/fusion_applique` lisent celle du fusionneur ; `/conventions` et `/8_code` celle de l'architecte. Le redacteur, à l'invocation 3, ajoute des `## Blocking N` sous l'unique `## Invocation`, les quatre titres répétés sous chacun, un `## Decision` par entrée.

**Forme 3 — `## Blocking N` par bloc bloqué, quatre titres `##` sous chacun.** Un `## Decision` par entrée ; les entrées ne sont pas tranchées ensemble. Scripteurs : qualifieur, classeur. Un bloc qui bloque n'arrête pas le run : les autres blocs nommés sont traités, le fichier de questions est écrit, seules les lignes impossibles restent vides. Les commandes (`/2_structure`, `/3a_genre`, `/3b_nature`) testent chaque `## Decision`.

**Forme 4 — `## Blocking N` par arrêt, trois titres `###`, un seul `## Decision` numéroté à la fin.** `## Blocking N — lot-NN` (le suffixe de lot obligatoire chez le detailleur, absent chez le realisateur), `### What blocks`, `### Where`, `### To resume`, puis un `## Decision` unique où l'Arbitre répond sous le numéro de chaque entrée (`N.` puis trois parties). Scripteurs : detailleur (`code/blocked_detailleur.md`, tout ce qu'une marche a trouvé, d'un coup), realisateur (`code/<lot>/blocked_realisateur.md`, chaque manque ajouté en continuant). Un arrêt neuf sur un fichier déjà rempli s'ajoute en `## Blocking N` suivant, avant le `## Decision` existant, jamais une réécriture ; l'Arbitre numérote sa réponse sous les précédentes. Lecteur unique de cette forme : l'arbitre ; `/8_code` la teste en comptant `^## Blocking ` contre les lignes numérotées sous `## Decision`.

**Forme 5 — trois titres, sans `## Decision`.** `## What blocks`, `## Where`, `## What has to happen`. Scripteur : verificateur (`code/blocked_verificateur.md`). Rien n'y est à trancher : la lecture précédente doit être refaite ; `/7_lots` le supprime par `git rm` avant de relancer le Cadreur, `/8_code` s'arrête dessus et renvoie à `/7_lots`.

**`Options:` — la fin de `To resume`, formes 1 à 4.** Le corps de `## To resume` (`### To resume` en forme 4) peut finir sur une liste, jamais sous un titre à elle :

    ## To resume
    <la décision ou la correction attendue>
    Options:
    - <une proposition, une phrase entière, en français>
    - <une autre>

De deux à six propositions, en français — une option choisie devient la décision du Product Owner mot pour mot ; aucune n'ouvre sur un numéro suivi d'un point (`1.`, `2.`), qu'en forme 4 on compterait comme une réponse sous `## Decision`. Facultative, et absente quand la correction est une entrée manquante. Scripteurs : les dix-huit des formes 1 à 4 — jamais le verificateur, dont la forme 5 n'a ni `## Decision` ni `To resume`. Ce qui diverge : le lexicographe et l'architecte la disent dans la ligne `To resume` de leur table de champs ; en forme 3 et chez le redacteur à l'invocation 3, une liste par entrée, au bout de chaque `## To resume` ; en forme 4, chaque `### To resume` peut porter la sienne ; le Cadreur en met une à chaque jeu de titres ajouté sous un `## Decision` rempli, et aucune sur un blocage de conventions, que le verdict de l'Architecte lève ; le Relecteur, aucune sur un blocage qui nomme manquant le rapport, la fiche, `conception.md` ou `tests.md` — l'acte de `/8_code` y répond ; le qualifieur et le classeur y écrivent les formes que prend la décision — un genre parmi les six, ou le bloc réécrit ou retiré ; une nature parmi les huit, une réécriture ou un retrait, une nature hors des huit.

Ce que le fichier de blocage entraîne diverge aussi : un run bloqué n'écrit rien d'autre — ni fichier de questions, ni section, ni plan — chez le lexicographe, le sondeur, l'assembleur, le convertisseur, le fusionneur ; le qualifieur et le classeur écrivent leur fichier de questions quand même ; le concepteur et le testeur écrivent d'abord leur rapport (`## Declared` et `## Compile`, `## Tests` et `## Red`), puis le fichier, puis commitent le tout ; le realisateur écrit son rapport (`## Build` disant que rien n'a passé) et commite ce qui compile ; le redacteur, à l'invocation 3, continue le pliage ; le cadreur écrit le fichier dans chacun de ses cas de blocage, un arrêt sans fichier étant invisible à la commande. L'assembleur distingue le blocage de l'arrêt sur fichier manquant, qui n'écrit rien ; le diagnostiqueur, l'arrêt sur `desc-bug.md` existant ; le controleur ne bloque jamais et met tout dans son rapport.

Qui répond au `## Decision` : le Product Owner à la main, par défaut ; l'Arbitre pour les deux fichiers de forme 4, le Product Owner ensuite s'il n'a pas pu ; le `## Verdict` de l'Architecte pour un blocage du Cadreur dont `## Where` nomme `architecte/cadreur.md — Request N` (le `## Decision` reste vide) ; l'acte de `/8_code` pour un blocage du Relecteur sur ce qu'il nomme manquant (rapport, fiche, `conception.md`, `tests.md`), le Product Owner sur toute autre chose.

Coût et écarté : cinq formes pour un même mécanisme · écarté : une forme unique · raison : à retrouver · inconnu. Écrire le fichier plutôt que le dire · écarté : un signalement en réponse · raison : « a message in a reply gets lost; a file does not » (decoupeur, qualifieur, classeur, assembleur, convertisseur, diagnostiqueur, entre autres) · inconnu. `## Decision` toujours présent et vide · écarté : le champ omis ou en table · raison : les commandes greppent `^## Decision$` et ne trouveraient pas un champ de table (`decoupeur.md` ; `docs/verification3/plan.md` entrée 63) · inconnu. Une entrée en attente sans numéro (forme 4) · écarté : un numéro vide ou une note *waiting* · raison : `/8_code` compte les lignes numérotées, et un numéro vide se lirait comme une réponse (`docs/verification3/plan.md` entrées 3 et 7) · inconnu. Une option qui n'ouvre jamais sur `N.` · écarté : une liste numérotée · raison : « the answers under `## Decision` are counted by their `N.` lines » (`realisateur.md` ; `detailleur.md` : « it would be counted as an answer ») · inconnu.

### Emplacement des fichiers de blocage

Utilisé par: les dix-neuf agents qui bloquent ; `/audit_blocages` ; chaque commande qui teste un fichier de blocage avant d'invoquer.

| Scripteur | Chemin, relatif au dossier de feature ou de travail | Forme |
|---|---|---|
| lexicographe | `blocked_lexicographe.md` | 1 (en table) |
| redacteur | `blocked_redacteur.md` | 2 |
| decoupeur | `blocked_decoupeur.md`, à côté du fichier produit | 1 |
| qualifieur | `blocked_qualifieur.md` | 3 |
| classeur | `blocked_classeur.md` | 3 |
| sondeur, invocation 1 | `cadrage-produit/blocked_par-bloc.md` · `cadrage-produit/blocked_par-question.md` · `cadrage-produit/blocked_par-nature.md` — dérivés du chemin de sortie du prompt | 1 |
| sondeur, invocation 2 | `cadrage-produit/blocked_global.md` | 1 |
| sondeur, invocation 3 | `blocked_existant.md`, à la racine de la feature, donné par le prompt | 1 |
| assembleur | `blocked_assembleur.md` | 1 |
| convertisseur | `convertisseur/blocked_<nature>.md` (invocation 1) · `convertisseur/blocked_transversal.md` (invocation 2) | 1 |
| fusionneur | `blocked_fusionneur.md` | 2 |
| architecte | `blocked_architecte.md`, à la racine du dossier de travail — jamais quand l'Arbitre l'appelle : le refus va dans `## Verdict` | 2 |
| diagnostiqueur | `investigation/blocked_<id>.md` (invocation 1, `<id>` le `G<n>` du manque) · `blocked_diagnostiqueur.md` (invocation 2) | 1 |
| batisseur | `blocked_batisseur.md`, à la racine du dossier de feature | 1 |
| cadreur | `code/blocked_cadreur.md` | 1, empilé |
| verificateur | `code/blocked_verificateur.md` | 5 |
| detailleur | `code/blocked_detailleur.md`, à la racine du découpage, jamais sous un lot | 4 |
| concepteur · testeur · realisateur · relecteur | `code/<lot>/blocked_concepteur.md` · `code/<lot>/blocked_testeur.md` · `code/<lot>/blocked_realisateur.md` · `code/<lot>/blocked_relecteur.md` | 1 · 1 · 4 · 1 |

Six noms distincts pour `/4_grille` parce que quatre sondeurs tournent à la fois et qu'un nom partagé laisserait l'un écraser l'autre ; un nom par identifiant pour `/diagnostique` pour la même raison. `/audit_blocages` lit cinq lieux : `code/**/`, `cadrage-produit/`, `convertisseur/`, la racine du dossier de travail, `investigation/`.

Coût et écarté : un nom par scripteur et par invocation parallèle · écarté : un nom partagé · raison : les sondeurs et les investigations tournent en parallèle et s'écraseraient (`/4_grille`, `diagnostiqueur.md`) · inconnu.

### Reprise sur décision — divergence

Utilisé par: tous les agents qui bloquent, sauf le decoupeur et le verificateur ; toutes les commandes qui invoquent.

Le noyau commun : la commande teste le fichier de blocage avant d'invoquer (→ `### États de « ## Decision » — ce qu'un fichier de blocage attend`) ; vide, elle s'arrête et relaie ; rempli, elle nomme le fichier dans le prompt ; l'agent applique la décision à l'élément que `## Where` nomme, et dit dans son rapport qu'il l'a appliquée — la commande renomme sur cette ligne. L'agent ne renomme jamais.

**Variante A — l'agent ne cherche jamais son fichier.** Il ne lit que celui que le prompt nomme ; l'orchestrateur a vérifié et ne l'aurait pas appelé sur une décision vide. Agents : lexicographe, redacteur, qualifieur, classeur, sondeur, assembleur, convertisseur, concepteur, testeur. Le decoupeur ne voit jamais son fichier : `/3_decoupe` ne le nomme pas, `/2_structure` le nomme au Rédacteur qui applique la réécriture.

**Variante B — l'agent cherche son fichier en premier, à chaque run.** Il regarde son propre fichier non numéroté et lit les `-NN` réglés à côté, qui disent ce qui a déjà été tranché ; vide, il s'arrête et dit que l'orchestration n'aurait pas dû l'invoquer (detailleur, realisateur) ou que le blocage tient toujours (fusionneur, diagnostiqueur, relecteur, architecte — qui réécrit le fichier inchangé) ; rempli, il applique et le dit. Agents : fusionneur, diagnostiqueur, cadreur (table de dispatch, dernier `## Decision` du fichier), detailleur, realisateur, relecteur, architecte. Le realisateur ajoute deux lignes : `Not settled here.` → rien n'est tranché, arrêt et relais ; décision *retour au découpage* → `code/redecoupage.md` encore là, arrêt ; disparu, le découpage a été refait, on continue. Le detailleur tient les mêmes deux lignes de retour au découpage, sans `Not settled here.`. L'architecte appelé par l'Arbitre n'agit pas sur un `blocked_architecte.md` trouvé à la racine.

Ce qui suit l'application diverge encore : `/3a_genre` et `/3b_nature` renomment seulement si le rapport dit avoir écrit le genre ou la nature que chaque décision nomme, et laissent le fichier au nom non numéroté quand le rapport dit qu'un bloc *waits on the Rédacteur* ou qu'une décision nomme une valeur hors table ; `/8_code` refait le test de forme après le rapport et ne renomme pas si un `## Blocking N` sans numéro ou un `## Decision` vide est apparu ; `/7_lots` clé sur les quatre termes du Cadreur (→ `### Les quatre termes du Cadreur — l'issue sur son fichier de blocage`).

Coût et écarté : la reprise portée par le prompt (A) ou par le disque (B) · écarté : une forme unique · raison : à retrouver · inconnu. Relire les `-NN` réglés (B) · écarté : les ignorer · raison : un blocage qui suit un autre signifie souvent que la première réponse était trop étroite (arbitre, cadreur, detailleur) · inconnu. Un agent qui trouve un `## Decision` vide s'arrête sans rappeler l'Arbitre · écarté : le rappeler · raison : un blocage laissé debout est l'arrêt de l'orchestration, et rappeler l'Arbitre re-poserait ce qu'il n'a pas pu trancher (`detailleur.md`, `realisateur.md`) · inconnu.

### Renommage -NN — divergence

Utilisé par: `/1_lexique`, `/2_structure`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/batir`, `/7_lots`, `/8_code`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique` ; `/audit_blocages` (lit les `-NN`) ; tout agent de variante B (lit les `-NN`).

**Forme standard.** Une fois que l'agent a rapporté avoir appliqué la décision, la commande fait `git mv <dossier>/blocked_<x>.md <dossier>/blocked_<x>-NN.md`, dans le worktree, avant les cinq pas Git ; `NN` est le plus haut `blocked_<x>-NN.md` du même dossier plus un, `01` quand il n'y en a pas, compté par nom de fichier et par dossier. Un fichier laissé au nom non numéroté se lit comme un blocage encore debout, et le run suivant s'y arrête — ce qu'un blocage neuf doit précisément faire. Le même geste sert à `code/<lot>/reprise_realisateur.md` (`/8_code`, une fois que le Réalisateur dit l'avoir consommé) et à `code/redecoupage.md` (`/7_lots`, sur la ligne `## Redécoupage: archivable` de `code/sequence.md`, lue au fichier et retirée après l'archive).

**Variante `/4_grille`.** `NN` n'est pas le plus haut plus un : c'est le numéro du tour, celui que prend le `questions-sondeur-NN.md` du tour ; les six fichiers `cadrage-produit/closed/*-NN.md` prennent le même. Un tour qui n'a produit aucun fichier de questions prend le numéro qu'il aurait pris. `blocked_existant.md` suit la forme standard (`blocked_existant-NN.md`).

**Ce qui n'est pas renommé.** `code/blocked_verificateur.md` : `git rm` par `/7_lots`, il n'a pas de `## Decision`. `blocked_decoupeur.md` : `/3_decoupe` ne renomme rien ; `/2_structure` renomme après la réécriture du Rédacteur, comme les fichiers du qualifieur et du classeur qu'il a nommés. Un fichier que le run vient d'écrire : `/2_structure` ne classe rien quand le Rédacteur a bloqué ; `/8_code` laisse au nom non numéroté un fichier où un blocage neuf est apparu pendant le run qui appliquait le précédent.

**Autres archivages par numéro, même geste.** `convertisseur/questions-<nature>.md` → `convertisseur/closed/questions-<nature>-NN.md` (`/6_convertit`, avant d'invoquer, numéro libre suivant) ; `convertisseur/technique-<nature>.md` et `technique-transversal.md` → `convertisseur/closed/technique-<nature>-NN.md` après que l'invocation a écrit ce pour quoi le fichier était nommé, et jamais s'il porte un `^Answer:\s*$` neuf ; `code/redecoupage.md` → `code/redecoupage-NN.md` (`/7_lots`) ; `code/rapport-controle.md` → le Contrôleur écrit lui-même le numéro libre suivant à côté, sans jamais renommer ni ouvrir l'ancien.

Coût et écarté : le renommage tenu par la commande · écarté : par l'agent · raison : aucun agent n'a d'outil qui renomme ou supprime un fichier (chaque agent de variante B ; `/7_lots`, `/8_code`) · inconnu. Le renommage avant les cinq pas · écarté : après · raison : fait après le commit, le renommage reste hors de la fusion et laisse l'arbre sale pour le pas 5 (`/fusion_applique` ; `docs/verification4/plan.md` entrée 12) · non éprouvée. Second test de forme après le rapport (`/8_code`) · écarté : renommer sur la ligne *applied* seule · raison : un blocage levé dans le run même serait archivé comme réglé (`docs/verification4/plan.md` entrée 15 ; la règle que `/7_lots` avait déjà) · non éprouvée.

### Trace de la décision appliquée — divergence

Utilisé par: concepteur, testeur, realisateur, relecteur, et les autres agents qui reprennent ; `/8_code` ; relecteur (lecteur).

L'agent dit qu'il a appliqué une décision, et la commande renomme sur cette trace ; où la trace s'écrit diverge : le Concepteur dans le champ `## Decision applied` de `code/<lot>/conception.md` ; le Testeur dans le champ `## Decision applied` de `code/<lot>/tests.md` ; le Réalisateur sous `## What governed the code, besides the sheet` de `code/<lot>/compte-rendu.md`, le fichier nommé tel qu'il s'appelle au moment de l'écriture (`blocked_realisateur.md`, sans numéro) ; tous les autres dans leur rapport de fin (le Relecteur : dans son message de clôture, *le rapport* désignant chez lui `compte-rendu.md`). Dans les trois champs, un tiret vaut « aucune décision appliquée ». Le Relecteur lit les deux premiers et le troisième pour distinguer une signature décidée d'une signature dérivée ; `/8_code` lit les trois champs et les rapports.

Coût et écarté : trois champs et un rapport · écarté : un champ unique · raison : `tests.md` n'avait pas de champ, et la ligne tombait dans un titre que rien ne lit (`docs/verification4/plan.md` entrée 5) · non éprouvée.

---

# Les fichiers de questions

### Fichier de questions — divergence

Utilisé par: lexicographe, redacteur, qualifieur, classeur, sondeur, assembleur, convertisseur, fusionneur, architecte (scripteurs) ; redacteur (invocation 2), lexicographe (invocations 3 et 4), assembleur, fusionneur (invocations 2 et 3), architecte (invocation 2), convertisseur (fichiers répondus), qualifieur et classeur (leur propre fichier répondu) (lecteurs) ; toutes les commandes amont, `/conventions`, `/fusion`, `/fusion_compare`, `/fusion_applique` (greps `^### Q`, `^Answer:\s*$`).

Le noyau commun : une entrée par question, ouverte sur `### Q<n>`, numérotée depuis `Q1` dans chaque fichier ; une ligne `Question:` énoncée directement, sans préambule ni justification — le seul endroit où un agent formule librement ; une ligne `Answer:` écrite vide et jamais omise, où le Product Owner répond à la main ; les questions en anglais, les réponses en français ; jamais une réponse suggérée dans la ligne `Question:` — les propositions vont dans `Options:`, aucune marquée préférée, seule une `Défaut:` en nomme une. Le fichier est écrit même vide — un fichier vide dit que rien n'attend, un fichier absent dit que l'agent n'a pas tourné — chez le lexicographe (1 et 3), le redacteur (1 et 2), le qualifieur, le classeur, le sondeur, l'assembleur, le convertisseur, le fusionneur (1 et 3), l'architecte (1 et 4). Il n'est écrit que si une réponse laisse le choix ouvert chez le lexicographe (2 et 4), le fusionneur (2, et alors rien d'autre n'est écrit), l'architecte (2) ; jamais chez le redacteur à l'invocation 3. Un fichier répondu est une archive : on n'écrit jamais dans un fichier qui existe — toujours un nouveau.

La deuxième ligne diverge, et c'est elle que le lecteur groupe :

| Ligne | Scripteurs | Ce qu'elle porte |
|---|---|---|
| `Block: <identifiants>` | redacteur, qualifieur, classeur, sondeur, assembleur, convertisseur (questions produit), fusionneur, architecte | Identifiants seuls, séparés par des virgules, jamais un titre ; `Block: -` quand la question porte sur la feature (pass C du sondeur, ou le redacteur sur la feature) ; plusieurs pour un croisement de pass B ; jamais `B?`. L'architecte y écrit une entrée, `§3.2 — Reconciling two real entries`, ou une entrée de grille pour `forme` |
| `Terms: <termes, séparés par des virgules>` | lexicographe | Ce que la réponse tranche |
| `Entries: <numéros ou références entre crochets>` | convertisseur, questions techniques (`convertisseur/technique-<nature>.md`) | Les entrées que la réponse changera, ou la nature quand aucune n'existe encore |
| `Kind: <une des cinq>` — cinquième ligne, entre `Block:` et `Question:` | architecte | → `### Les cinq Kind: — la sorte d'une question de l'Architecte` |
| `Folder: <dossier>` — entre `Block:` et `Question:` | sondeur (invocation 1, sur les seules questions de `A1.10` et `A1.11`) ; l'assembleur la copie sans jamais l'ajouter, la retirer ni la déplacer, et une `Folder:` sur la question qu'il écarterait garde les deux | La question demande un fichier, et la ligne nomme le dossier où il va, depuis la racine du dépôt : `docs/features/<name>/donnees/` ou `docs/donnees/` (→ `### Lecture des données externes`) ; c'est elle qui permet au cockpit d'offrir « Joindre un fichier ». `Answer:` nomme le fichier comme son index le nomme ; le redacteur (invocation 2) le nomme dans le bloc, par son chemin |
| `Défaut: <réponse proposée> — <le bloc transverse et ses mots>` — entre `Question:` et `Answer:` | sondeur (invocations 1 et 2, jamais 3) ; l'assembleur la copie sans jamais l'ajouter, la retirer ni la déplacer | Une réponse que le corpus porte déjà ; `Answer:` vide vaut acceptation, une `Answer:` écrite la remplace. Le lexicographe balaie une `Défaut:` acceptée comme une réponse ; le redacteur l'intègre comme si elle avait été écrite. Sa forme reste `<réponse> — <source>` ; le texte avant ` — ` reprend une option mot pour mot |

**`Options:` — les propositions, facultatives.** Toute entrée peut porter, entre `Question:` et `Défaut:` — ou `Answer:` quand il n'y a pas de `Défaut:` —, un bloc :

    Options:
    - <une proposition, une phrase entière, en français>
    - <une autre>

De deux à six propositions, en français alors que la `Question:` reste en anglais — une option choisie devient la réponse mot pour mot ; aucune n'ouvre sur un numéro suivi d'un point ; une question ouverte n'en a pas. Le compte de lignes qu'un agent annonce pour une entrée (« four lines », « five lines ») admet ce bloc et la ligne `Folder:`, rien d'autre. Scripteurs : lexicographe, redacteur, qualifieur, classeur, sondeur, convertisseur (questions produit et techniques), fusionneur, architecte ; l'assembleur la copie avec sa question, mot pour mot, sans jamais en écrire, en retirer, en juger, ni la déplacer ou la fondre d'une question à l'autre — la question gardée garde la sienne. Ce qui diverge : le lexicographe y met les lectures d'une paire qui conviennent à l'entrée, et un remplacement de terme atteint `Answer:` et la `Défaut:` acceptée, jamais `Options:` — aucun lecteur ne lit `Options:` une fois la réponse écrite ; le qualifieur et le classeur y listent les genres ou les natures en doute, sans en marquer un préféré ; le sondeur, à l'invocation 3, y met les deux côtés de l'arbitrage, toujours sans `Défaut:` ; la question `replacement` de l'architecte porte exactement `Changer la règle` et `Se conformer à la règle` ; le fusionneur n'y met que les réponses sans mots neufs — pour une phrase `PENDING`, la règle tient (`KEEP`) ou ne tient plus (`DELETE`) ; pour un titre, le titre couvre toujours la section — jamais un `REPLACE` ni un titre neuf, dont la formulation est la réponse libre.

Les lecteurs : le redacteur (invocation 2) sert tout fichier rempli quel qu'en soit le préfixe, sauf `questions-architecte-*.md` ; le lexicographe (3 et 4) balaie les champs `Answer:` et les `Défaut:` acceptées, jamais une ligne `Question:` ; l'assembleur lit les quatre fichiers de `cadrage-produit/` entiers et en écrit un seul ; le fusionneur relit ses propres fichiers répondus ; l'architecte (2) lit celui que le prompt nomme ; le convertisseur lit son fichier technique répondu et, quand la réponse n'a changé aucun bloc, le plus haut `questions/convertisseur/questions-convertisseur-NN.md` nommé au prompt ; le qualifieur et le classeur lisent leur propre dernier fichier, nommé au prompt, avant de dériver. Aucune commande ne lit une entrée : elle compte `^### Q` et teste `Answer:`.

Coût et écarté : `Answer:` vide et jamais omise · écarté : un champ ajouté par le Product Owner · raison : une entrée sans elle est inutilisable (redacteur, qualifieur, classeur, sondeur, convertisseur, fusionneur, architecte) · inconnu. Un fichier écrit même vide · écarté : rien quand rien n'est demandé · raison : l'absence se lirait comme un passage qui n'a pas tourné, et un fichier vide est ce qui ferme une boucle (`/1_lexique`, `/4_grille`, `/6_convertit`, `/fusion`) · inconnu. `Défaut:` accepté par le silence · écarté : une réponse obligatoire partout · raison : le corpus porte déjà la réponse, et la ligne épargne au Product Owner d'écrire ce qu'elle a déjà écrit (`sondeur.md`) · inconnu. Des `Options:` en français sous une question en anglais · écarté : des options dans la langue de la question · raison : « an option chosen becomes the answer word for word », et les réponses sont en français (redacteur, sondeur, convertisseur, entre autres) · inconnu.

### Numéro du fichier de questions — divergence

Utilisé par: lexicographe, redacteur, qualifieur, classeur, fusionneur, architecte, convertisseur, sondeur ; `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/conventions`, `/fusion`, `/fusion_compare`, `/fusion_applique`.

Le fichier s'appelle `questions-<agent>-NN.md`, à la racine du dossier de feature (`questions-architecte-NN.md` à la racine du dossier de travail). `NN` est le plus haut numéro de son propre préfixe trouvé à la racine et sous `questions/<agent>/` ensemble, plus un, `01` quand il n'y en a aucun ; le préfixe d'un autre agent à la racine ne compte pas. Le numéro avance une fois par invocation, jamais par question.

Qui le calcule diverge : le lexicographe et le redacteur (ils ont `Glob`) le comptent eux-mêmes ; le qualifieur, le classeur, l'architecte, le fusionneur le reçoivent dans le prompt (`Your questions file number: NN.` / `Questions file number: <NN>.`) parce qu'ils ne listent aucun dossier — le qualifieur et le classeur n'ont pas `Glob`, l'architecte et le fusionneur s'interdisent de lister ; le sondeur et le convertisseur ne numérotent jamais : la commande copie ou fusionne leurs fichiers de travail dans le `questions-sondeur-NN.md` / `questions-existant-NN.md` / `questions-convertisseur-NN.md` suivant, `NN` comptant sous `questions/<agent>/` plus un, la racine n'en tenant plus. `/4_grille` et `/6_convertit` écrivent ce fichier vide, sans agent, quand rien n'a été demandé.

Coût et écarté : le numéro dans le prompt pour quatre agents · écarté : chaque agent compte · raison : le qualifieur et le classeur n'ont pas `Glob` ; l'architecte ne liste pas un dossier pour ne pas y trouver ce qu'il ne doit pas lire (`architecte.md`, *What you read*) · inconnu.

### Test d'une question sans réponse

Utilisé par: `/1_lexique`, `/2_structure`, `/4_grille`, `/6_convertit` (fichiers techniques), `/conventions`, `/fusion` (ligne 5), `/fusion_applique`.

Une entrée attend une réponse quand sa ligne `Answer:` est vide — `^Answer:\s*$` — et qu'aucune ligne `Défaut:` ne la précède dans la même entrée ; une `Answer:` vide sous une `Défaut:` est une réponse. Une entrée qui attend arrête la commande, qui dit lesquelles. `/6_convertit` teste `^Answer:\s*$`, comme tout autre lecteur, sur `convertisseur/technique-<nature>.md` pour dire qu'une nature attend ; `/conventions` teste des lignes `Answer:` sans rien après (l'architecte n'écrit jamais de `Défaut:`) ; `/4_grille` teste le dernier fichier de la racine, `questions-architecte-*.md` excepté.

Coût et écarté : un test à deux conditions · écarté : `Answer:` vide seul · raison : la ligne `Défaut:` existe pour que le silence accepte (`/1_lexique`, `/2_structure`, `/4_grille`) · inconnu. L'exception architecte sur la porte de `/4_grille` · écarté : sans exception · raison : un tour de grille s'arrêtait sur un fichier que seul `/conventions` lit (`docs/verification4/plan.md` entrée 8) · non éprouvée.

### Classement des fichiers de questions

Utilisé par: `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`, `/7_lots`, `/conventions`, `/fusion`, `/fusion_compare`, `/fusion_applique`.

Un fichier de questions ne reste à la racine que le temps d'attendre sa réponse ou son intégration ; le suivant écrit doit y être seul, sinon la commande suivante ne sait pas lequel attend. Chaque commande du cycle classe les fichiers de la racine qu'elle ne lit pas, par `git mv docs/features/<name>/questions-<agent>-NN.md docs/features/<name>/questions/<agent>/`, en créant `questions/<agent>/` s'il manque — `git mv`, jamais une lecture-réécriture : ni l'agent ni la commande n'ouvrent ces fichiers. Rien à classer est l'issue normale.

**La garde `### Q`.** Avant de toucher un fichier de la racine dont le préfixe n'est pas `architecte`, la commande greppe `^### Q` : un fichier qui tient des questions attend une réponse ou n'a pas été intégré, et n'est pas à classer — arrêt, le fichier nommé. Commandes qui portent la garde : `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`, `/conventions`, `/fusion` (préfixes `fusionneur` et `architecte` exceptés), `/fusion_compare` (mêmes deux exceptions). `/7_lots` classe sans garde : la boucle amont est finie. `/1_lexique` classe seulement, après coup, le fichier du lexicographe qu'il a appliqué ; `/2_structure` classe le `questions-lexicographe-NN.md` de la racine sans `### Q` avant de choisir, puis le fichier intégré et, sur la ligne du fichier de blocage, le fichier vide qui l'accompagnait ; `/fusion_applique` classe tout une fois `rapport-fusion.md` écrit.

**L'exception architecte.** `questions-architecte-*.md` reste à la racine : seul `/conventions` le lit, et il le classe lui-même — l'intégré après l'invocation 2, le vide sans `### Q` avant d'invoquer. Toute autre commande lit la racine comme s'il n'y était pas. `/fusion` et `/fusion_compare` gardent aussi à la racine le plus haut `questions-fusionneur-NN.md`, qui porte la numérotation.

**Ce qu'on rouvre sous `questions/<agent>/`.** Classé, un fichier n'est plus lu par aucune commande — sauf : `questions/qualifieur/` et `questions/classeur/`, dont le plus haut est nommé à l'agent quand il tient un `### Q` (`/3a_genre`, `/3b_nature`) ; `questions/convertisseur/`, dont le plus haut est nommé à une nature dont la partie n'a pas changé (`/6_convertit`) ; `questions/lexicographe/`, dont le plus haut est greppé pour `### Q` par `/2_structure` (vocabulaire réglé) ; `questions/sondeur/` et `questions/existant/`, dont le plus haut est testé pour la clôture de la grille (`/4_grille`, `/5_reclasse`) ; `questions/fusionneur/` et `questions/architecte/`, comptés pour le numéro ; `questions/fusionneur/`, relu par le fusionneur (invocation 2, le fichier que les lignes `PENDING` nomment). Classer un fichier qui tient encore des questions perd ses réponses pour de bon.

Coût et écarté : un classement à chaque commande · écarté : les laisser à la racine · raison : le suivant doit être seul à la racine pour être reconnu (chaque commande amont) · inconnu. La garde `### Q` · écarté : classer sans lire · raison : un fichier répondu et non intégré serait rangé et ses réponses perdues (`/3_decoupe` ; `docs/verification4/plan.md` entrée 32 pour `/fusion`) · non éprouvée. L'exception architecte · écarté : le classer comme les autres · raison : deux commandes le rangeaient là où personne ne le lit (`docs/verification3/plan.md` entrées 17 et 18) · inconnu.

---

# Les relais

### Forme d'un relais

Utilisé par: les vingt agents ; toutes les commandes.

**Ce qu'un agent rend à l'orchestrateur.** Un rapport de fin, en message, que la commande relaie sans le relire. Lignes sur lesquelles une commande clé : *applied* — l'agent dit avoir appliqué la décision du fichier nommé (chaque agent qui reprend), et la commande renomme ; la liste des blocs regardés, tous, contre la liste nommée (decoupeur — une liste courte est un balayage partiel, réinvoqué au plus deux fois) ; la liste par bloc du genre ou de la nature donnée, les blocs bloqués, et les mots *waits on the Rédacteur* ou une valeur hors table (qualifieur, classeur) ; les quatre comptes `Files merged:` · `Questions in:` · `Questions out:` · `Dropped as duplicates:` (assembleur) ; les mots `blocking` · `assumed` · `misplaced` par question, les choix techniques tranchés, le nombre de questions techniques (convertisseur) ; un des quatre termes sur le fichier de blocage, les sections `## Ce qui revient` et `## Ce que j'en fais`, la remarque du Vérificateur sur un plafond (cadreur) ; quatre lignes au plus et une par question `coverage` (architecte) ; *consumed the reprise*, *the lot goes back to the split* (realisateur) ; la remarque sur un plafond et la ligne `## Redécoupage: archivable` (verificateur) ; la lecture de `bug-list.md` ou l'existence de `desc-bug.md` (diagnostiqueur) ; le fichier manquant, sans compte (assembleur). Jamais un jugement, jamais le nom de la commande suivante — le convertisseur le dit en toutes lettres.

**Ce que l'orchestrateur rend au Product Owner.** Le rapport de l'agent tel quel, les fichiers que le run a écrits ou renommés, ce que ses greps ont compté (blocs avant et après, questions, marques `<<ASSUMED`), et une table *What to run next* — indications pour le Product Owner, que la commande relaie et ne lance pas ; `first match wins` quand la table le dit. Deux lignes reviennent partout : « Nothing else is yours » — pas de lecture de ce qu'une question ou un bloc dit, pas de chaîne de phases ; « If it returns a `blocked_*.md`: relay it and stop » — le fichier nommé, le `## Decision` à remplir, la commande à relancer. Le relais finit sur une ligne `Next:` (→ `### Ligne Next:`).

Coût et écarté : un relais sans lecture · écarté : l'orchestrateur résume ce qu'il lit · raison : le Product Owner répond aux questions, pas l'orchestrateur ; relayer une liste écrite par l'agent n'est pas lire un bloc (`/1_lexique`, `/3a_genre`) · inconnu.

### Ligne Next:

Utilisé par: les dix-neuf commandes de la chaîne — `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`, `/batir`, `/7_lots`, `/8_code`, `/9_controle`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique`, `/audit_blocages`, `/audit_conventions` ; `CLAUDE.md` (*The `Next:` line*, la grammaire) ; l'application cockpit, lectrice (`docs/app/TECHNICAL_V1.md` §9).

Chaque relais finit sur une ligne, et une seule, dans cette grammaire — les arrêts compris, un arrêt étant un relais aussi :

    Next: run /<command> <arguments>
    Next: answer <questions | blocking | questions and blocking>[, then run /<command> <arguments>]
    Next: manual <what the Product Owner does>[, then run /<command> <arguments>]
    Next: stop <reason>
    Next: done

C'est la dernière ligne du relais, rien après elle. `run` nomme la commande à lancer ; `answer` dit ce qui attend le Product Owner — les questions, le `## Decision`, ou les deux — et la commande qui suit ; `manual` dit le geste qui est le sien (une décision sous `## Décision du Product Owner` de `code/redecoupage.md`, lire le rapport de contrôle et décider d'une bug-list) ; `stop` donne la raison (`Next: stop argument missing`, un classement qui a échoué, une valeur hors table) ; `done` dit l'étape finie (`/audit_blocages`, `/audit_conventions` toujours ; la fusion écrite). Une commande qui ne connaît pas la suite imprime `Next: stop <reason>`, jamais une supposition. `CLAUDE.md` donne la grammaire et rien d'autre ; chaque commande donne ses valeurs, issue par issue — une colonne `Next:` à sa table *What to run next*, ou la ligne écrite à l'arrêt qui la produit. L'application cockpit lit cette ligne, et elle seule, pour désigner la commande suivante ; sans ligne `Next:`, elle dit la suite inconnue et montre le relais entier.

Coût et écarté : une ligne à grammaire fermée en fin de chaque relais · écarté : laisser l'application lire la table *What to run next* ou deviner la suite · raison : `Next: stop <reason>` est ce que la chaîne imprime quand elle ne sait pas, et l'application ne comble jamais ce manque (`CLAUDE.md`, *The `Next:` line* ; `docs/app/TECHNICAL_V1.md` §9) · inconnu.

### stop.md

Utilisé par: `socle.py` ; `/8_code`.

`docs/features/<name>/stop.md`, créé à la main par le Product Owner dans le dépôt principal — jamais dans le worktree, coupé avant lui. `/8_code` le cherche au mouvement 6, à la fin de chaque lot, dans le dépôt principal : présent, la commande s'arrête là, le lot fini fusionné et poussé, et dit combien de lots restent ; absent, lot suivant. `stop1.md` est la forme désarmée : le Product Owner renomme l'un en l'autre pour arrêter et reprendre ; aucun des deux présent n'est une erreur. `socle.py` ajoute à `.gitignore` les lignes `docs/features/*/stop.md` et `docs/features/*/stop1.md` — aucun des deux n'est jamais commité, même quand une commande fait `git add docs/features/<name>/` dans le dépôt principal. Un `## Decision` rempli pendant un run vif prend le chemin inverse : dans le worktree, où l'Arbitre le sonde ; un `## Decision` écrit dans le dépôt principal n'atteint aucun agent du worktree.

Coût et écarté : deux fichiers, deux lieux · écarté : un seul lieu pour `stop.md` et le `## Decision` · raison : un fichier créé dans le dépôt principal n'atteint pas un worktree coupé avant lui, et l'inverse pour la décision (`/8_code`, mouvement 6 ; `docs/verification3/plan.md` entrée 28) · inconnu.

---

# Git et worktree

### Git, avant l'invocation

Utilisé par: `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/batir`, `/7_lots`, `/8_code`, `/9_controle`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique` ; `CLAUDE.md`.

Avant ces gestes, et avant le classement, chaque test de précondition de la commande : le premier geste qui change le dépôt (`git mv`, copie, commit, worktree) et le premier agent ne viennent qu'après. Trois commandes gardent un test après ce geste, parce qu'il lit ce que le geste ou une phase produit : `/2_structure` (la racine après le classement), `/9_controle` (la carte que la phase 1 écrit), `/diagnostique` (la porte de la phase 2) — le cockpit demande toujours confirmation pour les deux dernières (`tools/cockpit/scan_rules.md` §2) ; plus pour `/2_structure` depuis la 1.4.3 : ses trois arrêts après le classement ne laissent que le fichier vide du lexicographe classé, un état que la commande suivante lit juste.

Trois gestes, dans cet ordre, une fois le classement des fichiers de questions fait :

1. Commit du dossier de feature : `git add docs/features/<name>/ && git commit -m "chore: answers"` — le Product Owner remplit `Answer:`, `## Decision` et `bug-list.md` à la main hors session, et un worktree branche sur le dernier commit : une réponse non commitée y est invisible. Rien à commiter est l'issue normale. Le message diverge par commande : `chore: answers` (amont, `/conventions`, `/diagnostique`, `/fusion*`), `chore: pre-build` (`/batir`), `chore: pre-split` (`/7_lots`), `chore: pre-code` (`/8_code`), `chore: pre-control` (`/9_controle`).
2. Création du worktree depuis le `HEAD` local, et enregistrement : `git worktree add .claude/worktrees/<name> HEAD` — jamais l'outillage ne choisit la base, dont le défaut est `origin/master`, qui peut être plusieurs commits derrière le local. Un seul worktree par run (`/8_code`), pas un par lot.
3. Entrée dans le worktree avant d'invoquer, pas après un échec d'écriture : le harnais bloque les écritures d'un sous-agent tant que la session n'est pas isolée. Dans le worktree, la commande crée les dossiers cibles qui manquent (`cadrage-produit/closed`, `convertisseur/closed`) — un agent dont le dossier cible manque cherche au lieu de s'arrêter.

Aucune branche, jamais : le worktree reste sur le `HEAD` détaché où `git worktree add` le crée, aucun `-b` n'apparaît dans la commande, et l'orchestrateur ne crée de branche ni dans le worktree ni pour lui (`CLAUDE.md` §Worktrees). Le pas 3 des cinq pas fusionne le commit du worktree par son identifiant ; ses commits restent atteignables jusqu'au pas 5, qui vient après la fusion.

Deux commandes sautent le worktree quand rien n'est à invoquer : `/4_grille` au second temps (le grep `Global:` d'abord) et les branches « invoke nothing » de `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/conventions` (→ `### Commit sans worktree`).

Coût et écarté : le commit avant le worktree · écarté : brancher sur l'arbre de travail · raison : vu une fois, 186 lignes dans le worktree contre 195 dans le dépôt principal (`/2_structure`, `/4_grille`, `/fusion_compare`, `/fusion_applique`) · éprouvée. `HEAD` local · écarté : laisser l'outillage brancher · raison : vu une fois, une invocation entière perdue sur une base en retard (`CLAUDE.md` ; `/1_lexique`, `/2_structure`, `/3_decoupe`) · éprouvée. Aucune branche · écarté : une branche nommée par l'orchestrateur · raison : vu une fois, aucune ligne ne définissait `<branch>`, le run en a inventé une, l'a trouvée prise par un run antérieur et en a inventé une seconde (`lexique-premiere-app-3-s2`, `tools/cockpit/logs/2026-10-06-111521-1_lexique.jsonl`) · non éprouvée. Entrer avant d'invoquer · écarté : entrer après l'échec · raison : mesuré sur trois phases, l'agent fait tout le travail, ne peut pas écrire, et l'invocation est refaite (`CLAUDE.md` ; `/2_structure`, `/diagnostique`) · éprouvée. Le grep avant le worktree (`/4_grille`) · écarté : le worktree d'abord · raison : un run qui n'invoque personne ne doit créer aucun worktree (`docs/verification3/plan.md` entrée 49) · inconnu.

### Git, après le rapport — les cinq pas

Utilisé par: `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/7_lots`, `/8_code`, `/9_controle`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique` ; `CLAUDE.md`.

Cinq pas, dans cet ordre, une fois que le dernier agent a rapporté — et à toute fin du run une fois le worktree créé, un arrêt compris (`/6_convertit`, `/9_controle` et `/diagnostique` le disent dans leur section git) :

1. `git add` et `git commit` dans le worktree — les agents sans `Bash` ne commitent rien, et les renommages, classements, copies et retraits que la commande a faits sont dans l'arbre, pas dans un commit ; `git merge` prend le commit du worktree, pas ses fichiers, et `git worktree remove` refuse un arbre sale. `/7_lots` et `/8_code` énumèrent ce qui est hors du dossier de feature et que le `git add` doit atteindre : les requêtes sous `architecte/`, `docs/TECHNICAL_CONVENTIONS.md` et `couverture.md` (l'Architecte, invocation 3), `docs/CURRENT_TECHNICAL_STATE.md` (les pièges de l'Arbitre). Les trois agents à `Bash` de `/8_code` ont commité leur propre travail seul.
2. Lecture de l'identifiant du commit du worktree, `git -C <path> rev-parse HEAD`, puis sortie du worktree — une session isolée dans un worktree ne peut pas émettre une commande git contre le dépôt principal : la fusion émise de l'intérieur est refusée.
3. `git merge --no-ff -m "<message>" <commit id>` depuis la racine du dépôt principal, le même dans les quinze commandes — `<commit id>` celui que le pas 2 a lu, `<message>` qui se lit `Merge /<command> <name>` (`CLAUDE.md`).
4. `git push` — le push fait partie de la fusion ; une phase qui reste sur la machine locale est perdue avec elle. Un push qui échoue (dépôt distant divergé, pas de réseau) est rapporté, ni retenté ni contourné : la fusion tient localement.
5. `git worktree remove <path>`.

Fusionner avant de rendre la main, toujours — un `blocked_*.md` fusionne aussi, le Product Owner doit le voir ; une phase dont la sortie reste dans un commit non fusionné est invisible à la suivante, et un worktree qui tient un commit non fusionné ne se nettoie jamais seul. Un arbre encore sale après le pas 1 refuse un `remove` simple : jamais de force — dire ce qui reste et s'arrêter, car ce qui reste est ce que le pas 1 n'a pas indexé, une faute du run, jamais de l'agent (`/7_lots`, `/8_code`, `/9_controle`, `/diagnostique`). Tout arrêt sur défaut passe d'abord par les cinq pas (`/2_structure`, `/3a_genre`, `/3b_nature`, `/6_convertit`) — une exception, le refus de `/2_structure` d'intégrer un bloc `NEW` après le découpage, qui ne commite rien et fait `git worktree remove --force`. `/8_code` fait les cinq pas au retour au découpage avant de lancer `/7_lots`, puis rouvre un worktree neuf depuis le `HEAD` fusionné.

Coût et écarté : le commit par la commande, au pas 1 · écarté : rapporter les fichiers non commités comme faute de l'agent · raison : le Relecteur, le Détailleur et l'Architecte n'ont pas de shell, et le fichier même sur lequel `/8_code` reprend n'atteignait pas `HEAD` (`docs/verification3/fichiers.md` F01, `plan.md` entrées 2 et 22) · inconnu. La sortie du worktree au pas 2 · écarté : fusionner de l'intérieur · raison : une session isolée s'est vu refuser une commande git visant le dépôt principal (`docs/verification3/plan.md` entrée 62) · éprouvée. L'énumération des fichiers hors feature (`/7_lots`, `/8_code`) · écarté : `git add` borné au dossier de feature · raison : un `git add` borné comme le commit d'avant-run laissait l'arbre sale et le pas 5 refusait (`docs/verification4/plan.md` entrée 18) · non éprouvée. Jamais de force · écarté : `--force` · raison : forcer détruit ce que le pas 1 n'a pas indexé (`/7_lots`, `/8_code`) · inconnu.

### Commit sans worktree

Utilisé par: `/5_reclasse` ; `socle.py` ; `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/conventions` sur leur branche « invoke nothing ».

Quand aucun agent ne tourne, la commande écrit en place dans le dépôt principal et commite : `/5_reclasse` commite le dossier de feature sous `chore: product file by nature` et pousse ; `socle.py`, que le cockpit lance à la création d'une application, commite seul sous `chore: scaffolding for the chain` et ne pousse pas — le cockpit pousse, et dit un push qui échoue ; les commandes du cycle qui n'ont rien à invoquer commitent ce que le classement a déplacé, s'il y a quelque chose, et poussent — `/4_grille` y ajoute le `questions-sondeur-NN.md` ou `questions-existant-NN.md` vide qu'il écrit sans agent, `/conventions` le fichier architecte vide qu'il classe. Un push qui échoue est rapporté, pas retenté.

Coût et écarté : pas de worktree sans agent · écarté : un worktree systématique · raison : un run qui n'invoque personne n'a rien à isoler (`docs/verification3/plan.md` entrée 49) · inconnu.

### Bash des agents — divergence

Utilisé par: batisseur, concepteur, testeur, realisateur, arbitre ; `/8_code` (lit leurs commits), `/batir`.

Cinq agents portent `Bash`, chacun sur une liste blanche, et rien d'autre — pas de recherche, pas de listing, pas d'attente, pas de fusion, pas de branche, pas de push, pas de worktree ; pour trouver quelque chose, `Grep` et `Glob`, bornés au dépôt, jamais une recherche shell qui parcourt la machine :

| Agent | Ce que son `Bash` lance |
|---|---|
| concepteur | `git add`, `git commit`, `git status`, et la commande de compilation que les conventions nomment — ou, à défaut, la tâche de compilation par défaut de l'outil de build sur le module |
| testeur | `git add`, `git commit`, `git status`, la commande de test que les conventions nomment — ou la tâche de test par défaut de l'outil de build sur le module —, et `cp` d'un fichier que `## Test data` de la fiche liste vers le dossier de test, au mouvement 3 |
| realisateur | `git add`, `git commit`, `git status`, `git restore`, les commandes d'analyse statique et de test que les conventions nomment — ou leurs tâches par défaut —, et `cp` d'un fichier que `## Resources` de la fiche liste vers le dossier de ressources, au mouvement 5 ; une commande à la fois, au premier plan, jamais en arrière-plan avec sondage |
| arbitre | `sleep` entre deux lectures du fichier de blocage, pendant l'attente du Product Owner — rien d'autre |
| batisseur | `git add`, `git commit`, `git status`, chaque commande de la table de G2.1 telle qu'écrite, précédée de `time` ; et pour obtenir les outils de build : la commande qui obtient le système de build comme G12.6 le dit, un téléchargement depuis la source officielle d'un outil de build, l'extraction d'une archive dans le cache de ces outils, l'outil officiel de la plateforme pour ses composants — jamais un installeur système, des droits élevés, une licence acceptée à la place du Product Owner |

Le repli est le même pour les trois agents de lot : la tâche par défaut de l'outil de build dont `## Compile` du rapport de conception montre la commande, et le rapport nomme la commande qui a tourné, celle des conventions ou le repli.

Coût et écarté : un shell borné · écarté : un shell libre · raison : une recherche shell parcourt la machine entière et une commande qui ne finit pas ne rend jamais la main ; deux builds lancés en parallèle se disputent le même verrou (`realisateur.md`, *Your shell*) · inconnu.

### Commit d'un lot

Utilisé par: concepteur, testeur, realisateur ; `/8_code` ; relecteur (lit la liste que `/8_code` en dérive).

Chacun des trois agents commite son propre travail, lot par lot, dans le worktree de `/8_code` : `git status` d'abord, puis un `git add` explicite de ce qui est au lot — les déclarations, les fichiers que le module exigeait et `code/<lot>/conception.md` ; les tests, `code/<lot>/tests.md` et `code/recette.md` ; les corps, `code/<lot>/compte-rendu.md` et `docs/CURRENT_TECHNICAL_STATE.md` — et jamais une requête sous `architecte/`, que la commande commite hors de tout commit de lot. Le message est `<working folder>/<lot>: <what the commit carries>` — `<working folder>` étant le dossier de travail du prompt, en chemin sous `docs/features/` : `premiere-app-3`, `premiere-app-3/bugfix-01` — sur chaque commit, run bloqué compris ; c'est par ce sujet seul que `/8_code` trouve les commits du lot — jamais `--grep`, qui lit le corps, jamais ce que le commit indexe : une reprise qui ne touche que du code est au lot. La recherche part du commit qui a ajouté le `code/decoupage.md` en vigueur (`git log -1 --diff-filter=A --format=%H -- docs/features/<working folder>/code/decoupage.md`), que seul un premier découpage crée — un redécoupage le modifie et garde ses lots `PASS` après lui ; puis du dernier `Revert "<working folder>/<lot>: ` après lui, s'il y en a un ; la liste est `git log --reverse --format='%H %s' <base>..HEAD` filtrée sur le sujet `<working folder>/<lot>: `, pour la liste de fichiers du Relecteur (`git diff --name-only <first>^ HEAD`) et pour les reverts (`git revert --no-edit <sha>`, une liste unique sur plusieurs lots, du plus récent au plus ancien). Un run bloqué commite quand même ce qu'il a écrit — un worktree non commité ne peut pas être fusionné — et ce commit compte comme premier commit du lot. Le Réalisateur commite `docs/CURRENT_TECHNICAL_STATE.md` seul, sous `trap: <what it says>`, quand l'Arbitre y a écrit un piège pendant son appel, avant son propre mouvement 7 ; il ne commite rien quand le lot retourne au découpage, et `git restore` ce qui ne compile pas avant de s'arrêter sur une décision vide. `HEAD` avant et après le Réalisateur, égal, est la tentative vide.

Coût et écarté : un préfixe de message par lot · écarté : chercher les commits autrement · raison : c'est ce qui permet le revert d'un lot et le diff du Relecteur, qui ne peut pas grepper un commit (`/8_code` ; `docs/verification3/plan.md` entrée 23) · inconnu. La requête hors du commit de lot · écarté : commitée avec le lot · raison : un revert supprimait la requête, et une règle déjà écrite ne traçait plus vers rien (`docs/verification4/plan.md` entrée 4, F02) · non éprouvée. Le piège commité à part sous `trap:` · écarté : accepter qu'il soit revert avec le lot · raison : le lot recodé rencontrait le même test rouge et rappelait l'Arbitre (`docs/verification4/plan.md` entrée 4, item B) · non éprouvée.

---

# La lecture

### Ce que l'orchestrateur lit

Utilisé par: toutes les commandes ; `CLAUDE.md`.

L'orchestrateur lit des greps et des titres, jamais un contenu : un `ls` de la racine, `^### Q` compté, `^Answer:\s*$`, `-A2 '^## Decision$'`, `^## Invocation`, `^### .*NEW`, `^### .*MODIFIED`, `-B1 '^Genre:$'`, `-B2 '^Nature:$'`, `-B1 '^Genre: comportement$'`, `-B3 '^Global: '`, `Clarification needed`, `^### B`, `^### §`, `<<ASSUMED`, `[B`, `^## lot-`, `## Defects`, `## Status` et les quatre autres champs d'un verdict, `## Redécoupage: archivable`, `^## Décision du Product Owner`, `## Verdict`, l'existence d'un fichier par `Glob`, une comparaison d'octets (`cmp`, `diff -q`). Il ne lit jamais une entrée de questions, un bloc, une entrée technique, un fichier de blocage au-delà des titres nommés, `docs/CURRENT_TECHNICAL_STATE.md`, ni rien sous `docs/process/` — ce dernier étant les documents du Product Owner, où se trouvent des règles écartées. Il ne restaure jamais un fichier depuis l'historique git et ne lit pas cet historique pour expliquer un run. Chaque commande énonce sa propre liste de lecture sous *What you read*. Deux exceptions déclarées : `/5_reclasse` lit `desc-produit.md` pour copier ses blocs, jamais pour les juger ; `/diagnostique` lit `bug-list.md` pour le scinder manque par manque ; `/7_lots` lit `## Ce qui revient` et `## Ce que j'en fais` pour les relayer ; `/9_controle` copie les lignes `## Findings` d'un `PASS with reservation`.

Coût et écarté : lire par grep · écarté : ouvrir les fichiers · raison : le Product Owner répond aux questions, pas l'orchestrateur ; la documentation du code n'est pas la sienne — il dispatche (`CLAUDE.md`, *What you read* ; `/1_lexique`, `/2_structure`) · inconnu. Jamais `docs/process/` · écarté : les ouvrir · raison : y lire met du raisonnement écarté dans le contexte (`CLAUDE.md`) · inconnu.

### Lecture d'un bloc par grep

Utilisé par: redacteur, decoupeur, qualifieur, classeur, sondeur, controleur ; `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/9_controle`.

Un bloc se trouve par son titre, jamais par son identifiant seul : `grep '^### B7 '`, l'espace fermant le nombre — `B7` seul touche aussi `B70`. Un grep de `^#` (ou `^### B`) avec numéros de ligne donne la ligne de chaque titre, et le bloc court de son titre à la ligne avant le titre suivant de tout niveau ; la lecture est bornée — `Read(offset, limit)` sur cette fenêtre — jamais le fichier entier, sauf le tour du decoupeur dont le prompt dit *every block*. Le dernier bloc va jusqu'à la fin du fichier. La commande dérive l'identifiant de ce qui suit `### `, jusqu'au premier espace.

Coût et écarté : un grep et une fenêtre · écarté : lire le fichier produit entier · raison : le fichier produit est le produit entier et l'agent en tient une poignée de blocs ; un grep sur `B7` touche `B70` (qualifieur, classeur, sondeur, controleur) · inconnu.

### Grep du code avec chemin

Utilisé par: cadreur, detailleur, realisateur, diagnostiqueur, concepteur.

Toute recherche dans le code porte un chemin — `Grep(pattern, path: "<folder>")`, jamais un motif nu — sur les dossiers de code que `docs/TECHNICAL_CONVENTIONS.md` nomme, et leurs dossiers de test quand on cherche des appelants ; le manifeste, les fichiers de build et les ressources chacun à son chemin. Un motif nu balaie `docs/` et la sortie de build, et rend d'anciens plans et du code généré comme s'ils étaient la base de code. Les conventions ne nomment aucun dossier : le Détailleur bloque et écrit la requête, les autres n'ont pas de règle écrite. Le Cadreur greppe le document technique par son propre chemin, une fois, au mouvement 1. Le Cadreur, le Détailleur, l'Arbitre et le Diagnostiqueur greppent sans ouvrir un fichier de code — un grep dit qu'un symbole existe, jamais ce que son implémentation fait ; le Diagnostiqueur lit un corps au seul mouvement 5, celui de chaque appelant du porteur.

Coût et écarté : un chemin obligatoire · écarté : un motif nu · raison : il balaie `docs/` et la sortie de build (cadreur, detailleur, realisateur, diagnostiqueur) · inconnu. Grep sans ouvrir · écarté : lire le fichier · raison : on établit ce qu'un symbole est, pas ce qu'il fait (cadreur, detailleur, arbitre) · inconnu.

### Lecture de l'état technique

Utilisé par: detailleur, realisateur, diagnostiqueur (lecteurs) ; realisateur, arbitre (scripteurs) ; `socle.py` (le crée) ; `CLAUDE.md` et les commandes (ne l'ouvrent jamais).

`docs/CURRENT_TECHNICAL_STATE.md`, unique pour le projet, créé par `socle.py` avec `# Technical state` pour seule ligne. Personne ne le lit entier : deux sections ouvertes, `## Traps — general` et `## Dead state`, trouvées par un grep du titre puis un `Read` borné jusqu'au `## ` suivant — on ne peut pas grepper une règle qu'on ne sait pas s'appliquer à soi — puis des greps par symbole : le Détailleur pour chaque symbole d'une signature (deux greps par symbole, code et état), le Réalisateur pour les symboles marqués *modified* et ceux de `## Dependencies`, le Diagnostiqueur pour ses termes de recherche comme aide, jamais comme verdict. Le Réalisateur y écrit à la fin de chaque lot (`## State` de son rapport en rend compte), l'Arbitre y place un piège de plateforme sous `## Traps — general` ou sous le `###` du sujet qui le possède — `## Traps` seul n'est pas un titre de ce fichier ; tous deux chargent la compétence `technical-state-format` avant d'écrire. Le Cadreur ne l'ouvre pas : il établit ce que le code porte par grep. `## Traps — general`, `## Dead state` : titres que le fichier de format fixe, pas ce document.

Coût et écarté : deux sections puis des greps · écarté : le fichier entier · raison : « you cannot grep a rule you do not know applies to you » pour les sections ; le reste est trouvé par symbole (detailleur, realisateur, arbitre) · inconnu. Deux scripteurs · écarté : le Réalisateur seul · raison : un piège de plateforme qu'un test rouge révèle est tenu partout où un lot lit, quand une convention n'est tenue que si la fiche la nomme (`arbitre.md`, *When a rule would settle it*) · inconnu.

### Lecture des conventions — divergence

Utilisé par: cadreur, detailleur, arbitre, architecte, diagnostiqueur, concepteur, testeur, realisateur, relecteur ; `/audit_conventions`.

`docs/TECHNICAL_CONVENTIONS.md`, un seul fichier pour tout le dépôt, écrit par le seul Architecte. Deux lectures :

**Entier.** Le Cadreur (le découpage de modules borne un lot), le Détailleur (le module, les couches, les interdictions bornent une signature), l'Arbitre, l'Architecte aux invocations 2, 3 et 4 — jamais à la 1, ni ce fichier ni aucun fichier au nom de *convention*, *rule* ou *guideline* ; le Diagnostiqueur (invocation 1, pour les dossiers à fouiller) ; `/audit_conventions` à chaque passe.

**Les `permanente` entières, plus celles que la fiche nomme.** Le Concepteur, le Testeur, le Réalisateur (un `Grep` sur `permanente`, le mot n'importe où sur la ligne de règle), le Relecteur — chacun ouvre chaque `R<n>` de `## Conventions` de la fiche. Aucune règle ne porte le marqueur : lire le fichier entier — l'Architecte ne l'a pas encore dérivé, et un filtre qui ne trouve rien n'est pas un fichier sans règle.

Un agent qui trouve une convention fausse écrit une requête dans `architecte/` (→ `### Requête de conventions — divergence`), jamais une édition du fichier ; `CLAUDE.md` interdit à l'orchestrateur de le modifier sans le signaler.

Coût et écarté : deux portées · écarté : tout le monde lit tout · raison : les `permanente` sont tirées par un acte ordinaire d'écriture qu'aucune fiche ne peut nommer d'avance, les `spécifique` par ce que le lot fait, que le Détailleur nomme (`architecte.md`, *Every rule carries what triggers it*) · inconnu.

### Lecture du global par l'index

Utilisé par: redacteur, fusionneur, sondeur (invocation 3).

`docs/PRODUIT_GLOBAL.md`, hors du dossier de feature, créé par `socle.py` avec `# Application` pour seule ligne. Il se lit par son index — un grep des titres sur `^#` — puis les seules sections nécessaires, jamais le fichier entier : le Rédacteur cherche un titre couvrant un sujet et charge une section proche pour le test *même déclencheur, même sortie* ; le Fusionneur localise section, bloc, phrase ; le Sondeur charge les sections que les lignes `Global:` de ses blocs nomment, une section une fois. Le Fusionneur seul y écrit ; le Rédacteur jamais.

Coût et écarté : l'index d'abord · écarté : lire le global entier · raison : c'est le produit entier, et une poignée de sections suffit (redacteur, fusionneur, sondeur) · inconnu.

### Lecture des données externes

Utilisé par: le Product Owner (scripteur des fichiers et de leurs index) ; sondeur (invocation 1), redacteur (invocations 1 et 2), convertisseur (invocations 1 et 2), detailleur, testeur, realisateur (lecteurs) ; assembleur (copie la ligne `Folder:`) ; architecte et batisseur (la colonne `Resource folder` de G4.4).

**Le cas.** L'investigation du 7 octobre 2026 l'a constaté : une seule entrée de grille demandait une instance réelle de ce que l'application lit du dehors — `A2.external exchange.3` —, et pour les seuls blocs de nature `external exchange` : un bloc classé autrement n'était jamais interrogé. La réponse revenait en texte dans un `Answer:`, et aucun agent ne lisait un fichier déposé dans un dossier — chacun lit une liste fixe. Le Testeur inventait toute valeur qu'un critère ne donne pas : aucune donnée réelle n'atteignait un test.

**Deux sortes, un format.** `.claude/formats/donnees.md`, la seule source, que l'installation apporte avec le reste de `.claude/formats/`. Les **données de référence** — une instance réelle de ce que le code doit lire ou comprendre, dont la structure se décide hors de l'application : l'export d'un autre service, les données d'un site, ce qu'un appareil envoie, un fichier ou un texte que l'utilisateur apporte ; elles servent à écrire la spécification et les tests, jamais livrées, copiées sans retouche — dans `docs/features/<name>/donnees/`. Les **données embarquées** — les fichiers que l'application elle-même utilise quand elle tourne : un jeu d'images, une table — dans `docs/donnees/`. La sorte est celle du dossier, jamais un champ. Chaque dossier porte un index, `donnees.md` : `# Données`, puis une entrée par fichier — `## <nom>` tel que sur le disque, `What:`, `Source:`, `Date:` (`AAAA-MM-JJ`), `Private:` (`yes` ou `no`). Le Product Owner l'écrit, à la main ou aidé du cockpit ; aucun agent n'écrit dans un dossier `donnees/`. Un document cite un fichier par son chemin depuis la racine du dépôt, et le chemin porte la sorte. `Private: yes` : le fichier se lit comme un autre, mais aucune de ses valeurs n'est copiée dans un document de la chaîne — fichier produit, document technique, fiche, question, rapport — qui en décrit la forme et le nomme ; les copies qu'un lot en fait sont des fichiers, pas des documents.

**Le parcours.** La grille demande, pour tout bloc quelle que soit sa nature : `A1.10`, une instance réelle des données dont la structure se décide ailleurs ; `A1.11`, les fichiers que l'application embarque — `A3.1` garde les valeurs qu'un bloc écrit en toutes lettres, un fait en un seul endroit. La question porte `Folder:` (→ `### Fichier de questions — divergence`). Le Rédacteur nomme le fichier dans le bloc, par son chemin, sans redire son format. Le Convertisseur décrit le format depuis le fichier, jamais depuis la prose, et le cite sur une ligne `Data:` avant `Consumes:`. Le Détailleur reporte chaque chemin des lignes `Data:` de ses entrées sous `## Test data` (`docs/features/…`) ou `## Resources` (`docs/donnees/…`) de la fiche. Le Testeur copie les fichiers de `## Test data` dans le dossier de test du module (G4.4) et en tire les valeurs qu'il aurait inventées ; le Réalisateur copie ceux de `## Resources` dans le dossier de ressources du module — la colonne `Resource folder` de G4.4, que l'Architecte remplit et que le Bâtisseur crée comme les autres.

**Lus par nom, jamais par dossier.** Chaque agent lit ce que sa propre liste nomme, et rien n'est trouvé en parcourant un dossier `donnees/` : un fichier que l'index ne nomme pas n'existe pas pour la chaîne. Le sondeur (1) lit les deux index entiers, jamais un fichier ; le redacteur (1, 2) les deux index, jamais un fichier ; le convertisseur les deux index et les fichiers que ses blocs citent ; le detailleur les seules lignes `Data:` de ses entrées, ni index ni fichier ; le testeur les fichiers de `## Test data` ; le realisateur ceux de `## Resources`. Un index absent ne nomme aucun fichier ; une entrée dont le fichier manque est une entrée manquante, que chaque agent traite comme ses instructions traitent une entrée manquante.

Coût et écarté : la lecture par nom · écarté : un agent qui parcourt le dossier · raison : chaque agent lit une liste fixe, et un fichier trouvé par un listing entrerait sans que personne l'ait nommé (`.claude/formats/donnees.md`, §3) · non éprouvée. Deux entrées pour toute nature · écarté : `A2.external exchange.3` seule · raison : un bloc qui consomme des données venues d'ailleurs, classé autrement, n'était jamais interrogé (`GRILLE_CADRAGE_PRODUIT_V2.md`, *What it takes from files*) · non éprouvée. Le format décrit depuis le fichier · écarté : depuis la prose du bloc · raison : deux descriptions d'un format sont deux sources, et la prose serait lue à la place du fichier (`redacteur.md`, `convertisseur.md`) · non éprouvée. La sorte portée par le dossier · écarté : un champ de l'index · raison : un fichier déplacé d'un dossier à l'autre change de sorte, sans champ à tenir d'accord (`.claude/formats/donnees.md`, §1) · non éprouvée. Ni le Rédacteur ni le Détailleur n'ouvrent un fichier de données · écarté : chaque agent lit l'index et ses fichiers · raison : le Rédacteur nomme et le Convertisseur décrit — un Rédacteur qui lirait le fichier en redirait le format dans la prose ; le chemin d'une ligne `Data:` porte la sorte, et le Détailleur n'a rien d'autre à en apprendre (`redacteur.md`, `detailleur.md`) · non éprouvée.

---

# Les artefacts partagés

### Disposition du dossier de feature

Utilisé par: les vingt agents ; les dix-huit commandes.

`docs/features/<name>/` — `<name>` est l'argument de chaque commande. Tout ce qui suit est relatif à ce dossier ; un `bugfix-NN/` reprend la partie aval sous lui.

| Chemin | Scripteur | Lecteurs |
|---|---|---|
| `idees.md` | le Product Owner ; le lexicographe (invocation 2, termes remplacés) | lexicographe (1, 2), redacteur (1) |
| `lexique.md` | lexicographe ; redacteur (lignes `en anglais :`) | lexicographe, redacteur ; `/1_lexique` (grep `## Non tranché`) |
| `desc-produit.md` | redacteur, decoupeur (blocs), qualifieur (`Genre:`), classeur (`Nature:`), `/4_grille` (retrait des marqueurs à la clôture) | tout l'amont ; convertisseur (titres), architecte (1, 4), `/9_controle`, controleur |
| `questions-<agent>-NN.md` · `questions/<agent>/` | → `### Numéro du fichier de questions — divergence`, `### Classement des fichiers de questions` | |
| `blocked_<agent>.md` · `blocked_<agent>-NN.md` | → `### Emplacement des fichiers de blocage` | |
| `cadrage-produit/par-bloc.md` · `par-question.md` · `par-nature.md` · `global.md` · `releve.md` | sondeur (invocations 1 et 2) | assembleur (les quatre premiers) ; `releve.md` par le seul sondeur global |
| `cadrage-produit/questions.md` | assembleur | `/4_grille` (copie en `questions-sondeur-NN.md`) |
| `cadrage-produit/closed/<fichier>-NN.md` · `cadrage-produit/blocked_*.md` | `/4_grille` ; sondeur | `/audit_blocages` |
| `par-genre/comportements.md` · `transverses.md` · `directives.md` · `references.md` · `hors-perimetre.md` · `recette.md` | `/5_reclasse`, remplacés entiers | `/5_reclasse` (second mouvement) ; convertisseur (2) ; architecte (1, 4) ; convertisseur (2) ; convertisseur (2) ; `/9_controle` (phase 4) |
| `desc-par-nature.md` | `/5_reclasse` | `/6_convertit` |
| `convertisseur/<nature>-input.md` · `<nature>.md` · `<nature>-notes.md` · `questions-<nature>.md` · `technique-<nature>.md` · `transversal-record.md` · `questions-transversal.md` · `technique-transversal.md` · `blocked_<nature>.md` · `blocked_transversal.md` · `closed/` | `/6_convertit` (`-input`, `closed/`) ; convertisseur | convertisseur, `/6_convertit`, `/audit_blocages` |
| `spec-technique.md` | `/6_convertit` (assemblage), convertisseur (2, préambule, §9, références) | cadreur, verificateur, detailleur, architecte, `/7_lots`, `/conventions`, `/audit_conventions` |
| `tracabilite.md` | convertisseur (2) | `/6_convertit`, architecte, `/9_controle` |
| `couverture.md` | architecte (1, 3, 4) — à la racine de la feature, même sur un `bugfix-NN/` | architecte, `/conventions`, `/2_structure` (suppression), `/audit_conventions` |
| `architecte/<agent>-<lot>.md` · `architecte/cadreur.md` · `architecte/arbitre-<lot>-blocking-N.md` · `architecte/arbitre-block-N-blocking-N.md` | → `### Requête de conventions — divergence` | |
| `code/decoupage.md` · `code/sequence.md` · `code/redecoupage.md` · `code/redecoupage-NN.md` | → `### Fichiers du découpage` | |
| `code/blocked_cadreur.md` · `code/blocked_verificateur.md` · `code/blocked_detailleur.md` | cadreur, verificateur, detailleur | → `### Emplacement des fichiers de blocage` |
| `code/<lot>/fiche-executable.md` · `conception.md` · `tests.md` · `compte-rendu.md` · `verdict.md` · `reprise_realisateur.md` · `blocked_<agent>.md` | → `### Fichiers d'un lot` | |
| `code/recette.md` | testeur, en ajout, jamais réécrit | `/9_controle` (phase 4) |
| `code/controle/<group>.md` · `code/rapport-controle.md` (`-NN`) | controleur (1 ; 2) | controleur (2) ; `/9_controle` (phase 5) |
| `tracabilite-full.md` · `code/recette-ordonnee.md` · `registre-questions.md` · `code/decisions-produit.md` | `/9_controle` (phases 1, 4, 5, 6) | `/9_controle` (phase 2, `grouper.py`), le Product Owner, le Product Owner, redacteur (3) |
| `desc-produit-fusion.md` · `plan-fusion.md` · `rapport-fusion.md` | `/fusion` (copie), redacteur (3), fusionneur (3) ; fusionneur (1) ; fusionneur (2) | fusionneur ; `/fusion`, `/fusion_compare`, `/fusion_applique` |
| `bugfix-NN/bug-list.md` · `bugfix-NN/investigation/<id>.md` · `bugfix-NN/desc-bug.md` | le Product Owner ; diagnostiqueur (1) ; diagnostiqueur (2) | `/diagnostique`, diagnostiqueur ; fusionneur (3) ; cadreur, verificateur, detailleur, arbitre |
| `donnees/donnees.md` · `donnees/<fichier>` | le Product Owner, jamais un agent (→ `### Lecture des données externes`) | sondeur (1, l'index), redacteur (1, 2, l'index), convertisseur (l'index, les fichiers que ses blocs citent), testeur (les fichiers de `## Test data`) |
| `stop.md` · `stop1.md` | le Product Owner, jamais commités | `/8_code` |
| `audit-blocages.md` · `audit-conventions.md` | `/audit_blocages`, `/audit_conventions`, en ajout | eux-mêmes |

Hors du dossier : `docs/PRODUIT_GLOBAL.md`, `docs/TECHNICAL_CONVENTIONS.md`, `docs/CURRENT_TECHNICAL_STATE.md`, `docs/donnees/donnees.md` et `docs/donnees/<fichier>` (le Product Owner ; sondeur 1, redacteur 1 et 2, convertisseur, realisateur), `.claude/formats/donnees.md`, `.claude/grids/GRILLE_CADRAGE_PRODUIT_V2.md` (sondeur 1, 2), `.claude/grids/GRILLE_EXISTANT.md` (sondeur 3), `.claude/grids/GRILLE_FERMETURE_TECHNIQUE.md` (convertisseur, diagnostiqueur 2), `.claude/grids/GRILLE_CONVENTIONS.md` (architecte) ; `.claude/worktrees/<name>` ; `.claude/scripts/grouper.py` ; `.gitignore`.

Coût et écarté : un dossier par feature, tout dedans · écarté : des fichiers hors feature · raison : un dossier par fonctionnalité, créé par le Product Owner qui y dépose son fichier d'idées, à noms fixes — c'est ce qui permet aux commandes de n'avoir qu'un seul argument, le nom du dossier ; seul le global vit à part, il n'appartient à aucune feature (PROCESS_AMONT-avant-refonte.md L1366-1372) · inconnu.

### En-tête d'un bloc produit

Utilisé par: redacteur, decoupeur (structure) ; qualifieur (`Genre:`), classeur (`Nature:`) ; sondeur, convertisseur, fusionneur, architecte, controleur, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/9_controle` (lecteurs).

Le fichier produit s'ordonne `# Application` (une fois), `# Domaine : <nom>`, `## <Section>`, `### <Bloc>` — sans troisième niveau. Chaque bloc ouvre sur `### B<n> — <titre>`, suivi du marqueur `NEW` ou `MODIFIED` en fin de ligne quand il a bougé, puis `Genre:` sur la ligne suivante, `Nature:` sur la suivante, `Global: ## <section du global>` quand le bloc s'attache à une section du global — absente, jamais vide, quand il ne s'attache à rien — puis ses phrases, jusqu'au titre suivant de tout niveau. Le Rédacteur et le Découpeur écrivent `Genre:` et `Nature:` vides sur tout bloc qu'ils créent — jamais omis, la ligne vide est ce qui se greppe ; le Qualifieur remplit `Genre:` avec l'une des six valeurs, le Classeur `Nature:` avec l'une des huit, en minuscules, accents compris, rien d'autre sur la ligne, par une édition ancrée sur la ligne de titre (la seule unique). Un bloc d'un genre autre que `comportement` garde `Nature:` vide pour de bon ; un bloc qui quitte `comportement` voit sa nature vidée par le Classeur. Le numéro est local à la feature, jamais réattribué, jamais réutilisé même retiré ; il ne passe pas dans le global. La ligne `**Clarification needed:** …` en fin de bloc est un drapeau du Rédacteur (→ `### Marque Clarification needed`).

Coût et écarté : des lignes vides plutôt qu'absentes · écarté : omettre `Genre:` et `Nature:` quand rien n'est su · raison : une ligne absente et une ligne oubliée se lisent pareil, et chaque agent greppe les vides (`redacteur.md`) · inconnu. `Global:` absente plutôt que vide · écarté : la ligne vide · raison : une vide se lirait comme un attachement oublié (`redacteur.md`) · inconnu.

### Marqueurs NEW et MODIFIED

Utilisé par: redacteur, decoupeur (scripteurs) ; redacteur (invocations 2 et 3), `/4_grille`, `/5_reclasse` (retrait) ; `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, qualifieur, classeur, sondeur, controleur (lecteurs).

Un marqueur trailing sur la ligne `### B` : `NEW` sur tout bloc créé (par l'idée, une réponse, une scission — le Découpeur le met sur chaque moitié neuve, la moitié qui garde le titre et le numéro gardant le marqueur d'origine), `MODIFIED` sur tout bloc changé, qu'une question l'ait nommé ou non ; un bloc `NEW` qui change reste `NEW` seul ; un bloc `Genre: transverse` changé marque tout le fichier `MODIFIED`. Les commandes greppent `^### .*NEW` et `^### .*MODIFIED`, ancrés sur la ligne de titre — un `NEW` nu touche de la prose. Qui retire : le Rédacteur, à l'invocation 2, tout marqueur, seulement quand le fichier intégré a pour préfixe `sondeur`, `existant` ou `convertisseur` (un tour de grille ou de conversion l'a consommé) — jamais sur `qualifieur`, `classeur`, `redacteur` ; le Rédacteur à l'invocation 3, tout marqueur de la copie ; `/4_grille`, par script, sur le tour qui écrit un `questions-sondeur-NN.md` vide ; `/5_reclasse`, sur les copies de `desc-par-nature.md` seulement, le fichier produit gardant les siens. Le Qualifieur et le Classeur refont leur lecture sur un bloc `MODIFIED` ; le Sondeur ignore un marqueur hors de sa liste ; le Contrôleur ignore les deux.

Coût et écarté : deux marqueurs, retirés seulement par un tour consommateur · écarté : retirer à chaque intégration · raison : retirer un `NEW` qu'aucun tour de grille n'a vu laisse le bloc jamais sondé (`redacteur.md`, *The two markers*) · inconnu. Le retrait par `/4_grille` à la clôture · écarté : accepter le trou ou faire demander le Rédacteur · raison : sans lui un bloc créé après la clôture atteignait le Convertisseur sans être sondé, et le test de clôture devient « fichier vide et aucun marqueur » (`docs/verification4/plan.md` entrée 7, item C) · non éprouvée.

### Marque Clarification needed

Utilisé par: redacteur (scripteur) ; `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, convertisseur (lecteurs).

Une ligne `**Clarification needed:** <ce qui est flou, et ce qui a été transcrit à la place>` en fin du bloc concerné, écrite par le Rédacteur quand il ne comprend pas un passage ou une réponse — il transcrit une lecture plutôt que de s'arrêter — doublée d'une entrée dans son fichier de questions, même formulation, `Block:` nommant le bloc. Il la retire à l'invocation 2, quand une réponse dont la question correspond arrive. Un grep de `Clarification needed` dans `desc-produit.md` arrête `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille` (« `/2_structure` first ») et, sans fichier de questions à la racine, `/2_structure` lui-même (le drapeau tient sans fichier pour le lever : le fichier est au Product Owner à retrouver). Le Convertisseur lit une ligne survivante comme un signal.

Coût et écarté : un drapeau en place plus une question · écarté : un arrêt du Rédacteur · raison : le bloc reste utilisable pendant que la lecture est confirmée ; rien en aval ne tourne tant qu'un drapeau tient (`redacteur.md`, mouvement 4) · inconnu. L'arrêt de `/2_structure` sur un drapeau sans fichier · écarté : renvoyer à `/3_decoupe` · raison : les deux commandes se renvoyaient l'une à l'autre sans fin (`docs/verification4/plan.md` entrée 27) · non éprouvée.

### lexique.md

Utilisé par: lexicographe (scripteur) ; redacteur (une ligne) ; `/1_lexique` (grep).

`docs/features/<name>/lexique.md`, trois sections toujours, dans l'ordre : `## Tranché` (une entrée par question répondue, les termes retirés sous celle qui tient sur une ligne `remplace : …`, une entrée scopée finissant par `dans ce sens seulement`, un texte affiché entre guillemets avec sa langue et le concept à côté), `## Non tranché` (ce qui attend une réponse, une ligne chacun), `## Relevé` (chaque terme du domaine avec son compte, `(réponse)` pour un terme qu'une réponse a apporté). Le lexicographe le met à jour sans jamais le réécrire ; le Rédacteur y écrit une seule chose, une ligne `en anglais : <mot>` sous l'entrée `## Tranché` d'un concept qu'il rend pour la première fois (deux lignes pour une entrée scopée), et prend la ligne existante sinon — jamais une entrée, jamais un terme, jamais sur une ligne de `## Relevé`. `/1_lexique` greppe les lignes sous `## Non tranché` après chaque invocation ; `/2_structure` teste l'existence du vocabulaire réglé ailleurs (le plus haut `questions-lexicographe-NN.md` sans `### Q`).

Coût et écarté : un fichier unique, trois sections · écarté : un fichier par tour · raison : un terme passe d'une section à l'autre plutôt que d'un fichier à l'autre, et le tour suivant greppe ce fichier (`lexicographe.md`) · inconnu. La ligne `en anglais` au Rédacteur · écarté : le Lexicographe l'écrit · raison : rien d'autre ne garde le mot anglais, et deux intégrations rendraient un concept de deux façons, invisibles au lexicographe qui n'ouvre jamais le fichier produit (`lexicographe.md`, `redacteur.md`) · inconnu.

### Fichiers du cadrage

Utilisé par: sondeur, assembleur ; `/4_grille` ; `/audit_blocages`.

Sous `cadrage-produit/` : les trois angles écrivent `par-bloc.md`, `par-question.md`, `par-nature.md` (pass A, chacun dans son ordre de lecture), le global écrit `global.md` (passes B et C) et le relevé `releve.md` (une section `## B<n>` par bloc, une ligne par identifiant de croisement de la grille, `—` quand rien) ; l'assembleur fusionne les quatre fichiers de questions en `questions.md`, renuméroté de `Q1` dans l'ordre des identifiants de `Block:`, `Block: -` en dernier, tout copié mot pour mot, la ligne `Défaut:` et la liste `Options:` avec leur question ; `/4_grille` copie `questions.md` octet pour octet (`cp`) en `questions-sondeur-NN.md` à la racine, puis, au tour suivant, déplace les six fichiers en `cadrage-produit/closed/<fichier>-NN.md`. Le sondeur de l'invocation 3 écrit directement `questions-existant-NN.md` à la racine, sans fusion. Un sondeur qui bloque n'écrit pas de fichier de questions ; la commande distingue lecture bloquée et lecture manquante par le fichier présent.

Coût et écarté : quatre fichiers puis une fusion · écarté : une seule lecture · raison : la même lacune revient sous deux formulations, et l'union de ce que les lectures lèvent est la sortie, pas leur accord (`sondeur.md`, `assembleur.md`) · inconnu. `releve.md` archivé · écarté : ne pas l'archiver · raison : une trace de ce que la passe B a croisé, à côté des questions produites (`docs/verification4/plan.md` entrée 24, item E) · non éprouvée.

### Fichiers de la conversion

Utilisé par: convertisseur ; `/6_convertit` ; cadreur, verificateur, detailleur, architecte, `/7_lots`, `/conventions` (lecteurs de `spec-technique.md`).

`spec-technique.md`, à la racine de la feature, remplacé entier par `/6_convertit` : `# Preamble` (un seul `#`) avec ses quatre parties `## Intent and vocabulary`, `## Out of scope`, `## Cross-cutting rules`, `## Dependencies`, écrites même vides ; puis neuf sections `## §1 Model` … `## §8 Access`, `## §9 Text`, chacune copiée de `convertisseur/<nature>.md` ou écrite `*(empty)*`, jamais omise ; des entrées `### §n.m <titre>` numérotées à la suite dans chaque section, chacune finissant par une ligne `Consumes:` (→ `### Ligne Consumes:`), précédée d'une ligne `Data: <chemin>, <chemin>.` quand l'entrée est bâtie sur un fichier de données (→ `### Lecture des données externes`). `desc-bug.md` reprend la même forme sur un cycle de correction (`# Preamble` de trois lignes `Intent:`, `Out of scope:`, `Dependencies:` ; neuf sections ; chaque entrée ouvrant sur `Bearer:` ; `## Gaps set aside` en fin). Les fichiers de travail : `convertisseur/<nature>-input.md` (la partie de `desc-par-nature.md`, copiée par la commande, comparée par octets au run suivant), `<nature>.md` (la section), `<nature>-notes.md` (`## Trace` — une ligne par bloc, ses entrées ou un tiret, deux espaces au moins entre colonnes — et `## Preamble` — les références marquées *existing*), `transversal-record.md` (mêmes deux titres, pour les blocs transverses et de référence), `questions-<nature>.md` / `questions-transversal.md`, `technique-<nature>.md` / `technique-transversal.md`, `closed/`. `<nature>` prend un tiret pour l'espace dans un nom de fichier (`external-exchange`). La commande résout par script toute référence `[B<n>: …]` dont le bloc a donné une seule entrée dans `## Trace`, avant l'invocation 2.

Coût et écarté : une section par nature, écrite à part et assemblée par script · écarté : un seul agent sur tout le document · raison : un fichier produit de trois cents blocs fins ne se lit pas d'une traite, et la section d'une entrée est la couche de son lot ; le Classeur a posé la nature, le Convertisseur la lit sans la redériver ; en parallèle aucune nature ne connaît les numéros des autres, d'où le renvoi `[B12: ce qu'on en attend]` résolu par script quand le bloc n'a donné qu'une entrée et par la transversale sinon — l'attente écrite réduit le jugement, le remplacement mécanique le supprime là où il n'y a rien à juger ; les natures partent dans un seul message et la commande assemble les neuf sections par script (PROCESS_AMONT-avant-refonte.md L607-619, L1177-1182) · inconnu. Pas d'assemblage tant qu'une nature attend · écarté : assembler avec la marque dedans · raison : deux phrases de la commande se contredisaient, et un document sur disque avec une question en attente coûtait une invocation opus par relance (`docs/verification4/plan.md` entrée 30, F18, item F) · non éprouvée.

### tracabilite.md

Utilisé par: convertisseur (scripteur) ; `/6_convertit`, architecte, `/9_controle` (lecteurs).

À la racine de la feature, écrit par l'invocation 2 du Convertisseur : une ligne par bloc du fichier produit, dans son ordre — l'identifiant, le titre, puis ses entrées ou un tiret — deux espaces au moins entre colonnes, rien d'autre, pas d'en-tête ; tout bloc y figure, ceux sans entrée compris. `/6_convertit` compare sa première colonne aux identifiants des titres de `desc-produit.md` (un manquant ou un en trop est une faute du run) et teste sa présence comme preuve que le document tient ; l'Architecte (invocations 1 et 4, mouvement 2 — l'invocation 4 rejoue les mouvements 2 à 10 de la 1) y lit la correspondance bloc → entrées et lève `inconsistency` sur un tiret d'un bloc `comportement` ou `référence` seulement ; `/9_controle` (phase 1) en tire bloc → entrées pour `tracabilite-full.md`, qui reprend la forme — identifiant, deux espaces, `lot-NN` séparés par des virgules ou un tiret, puis le mot `carried` — et que `grouper.py` parse.

Coût et écarté : un tiret plutôt qu'une ligne absente · écarté : ne lister que les blocs à entrées · raison : un tiret dit que quelqu'un a regardé ; une ligne absente ne dit rien (`convertisseur.md`, mouvement 5) · inconnu. Le tiret non questionné hors `comportement` et `référence` · écarté : questionner tout tiret · raison : chaque dérivation demandait au Product Owner des blocs qui n'ont produit aucune entrée à dessein (`docs/verification3/plan.md` entrée 31) · inconnu.

### Ligne Consumes:

Utilisé par: convertisseur (scripteur) ; cadreur, architecte (lecteurs).

Dernière ligne de chaque entrée du document technique : `Consumes: §3.2, §1.4.` — les entrées dont celle-ci a besoin ; `Consumes: —` quand aucune ; `## Cross-cutting rules` nommé en place d'un numéro pour une règle transversale ; `[B12: …]` en attente de résolution à l'invocation 1. Personne ne la greppe : le Cadreur la lit dans chaque entrée et en tire le sens de `Needs` entre lots (le lot d'un écran reste derrière le lot qui calcule ce qu'il montre) ; l'Architecte la lit comme un graphe, une arête étant où chercher une conjonction.

Coût et écarté : une ligne sur chaque entrée, `—` compris · écarté : ligne absente quand rien n'est consommé · raison : une ligne absente et une entrée qui n'a besoin de rien se liraient pareil (`convertisseur.md`) · inconnu.

### Marques <<ASSUMED et [B

Utilisé par: convertisseur (scripteur) ; `/6_convertit`, cadreur (lecteurs).

`<<ASSUMED B40: <ce qui est supposé>>>` en ligne, greppable, dans l'entrée qu'il qualifie (ou en fin de section pour une règle d'une autre couche), portant le bloc que la réponse changera ; une seule marque, qu'elle attende une réponse produit ou technique. `[B12: <ce qu'on en attend>]` pour une référence hors de sa section, `[B?: <titre>]` quand aucun titre ne porte le bloc ; chacune sur une seule ligne, le `]` ou `>>` sur la même. La marque est levée en réécrivant la section, jamais retouchée. `/6_convertit` greppe `<<ASSUMED` (une nature qui en porte et dont la partie a changé, ou dont le fichier technique est répondu, retourne ; une marque laissée après un rerun est une faute) et `[B` (ce qui reste à côté d'un fichier de questions vide est une référence manquée). Le Cadreur greppe les deux au mouvement 1 et bloque sur une seule occurrence.

Coût et écarté : une marque en ligne · écarté : une note en fin de document · raison : la commande résout par script, ligne par ligne, et un `]` sur la ligne suivante serait à demi remplacé (`convertisseur.md`, *What a question costs*) · inconnu.

### Requête de conventions — divergence

Utilisé par: batisseur, cadreur, detailleur, concepteur, realisateur, arbitre (scripteurs) ; architecte (invocation 3, écrit `## Verdict`) ; `/batir`, `/7_lots`, `/8_code` (glob sur `## Verdict` vide) ; `/audit_conventions` ; cadreur (lit le verdict que son `## Where` nomme).

Un agent qui manque d'une règle écrit une requête dans `architecte/` du dossier de travail, dossier créé s'il manque, avec cinq titres — `## What I need`, `## Why the lot cannot proceed`, `## Where I met it`, `## What I think it is` (add · update · remove), `## Verdict` laissé vide — décrivant ce qui manque, jamais la règle : l'Architecte seul sait si c'est une convention. Les formes divergent :

| Scripteur | Fichier | Particularités |
|---|---|---|
| batisseur | `architecte/batisseur.md`, à la racine du dossier de feature | Requêtes empilées, chacune ouvrant sur `# Request N`, comme le cadreur ; un trou ou une contradiction dans les tables de G2.1, G4.4, G12.6, ou deux versions qu'elles imposent et qui ne vont pas ensemble ; sous `## Why the lot cannot proceed`, le lot est le build ; jamais de fichier de blocage à côté — `/batir` invoque l'Architecte et réinvoque le Bâtisseur, qui ne relève jamais un besoin qu'un bloc répondu porte déjà ; la requête n'est jamais dans le commit du Bâtisseur |
| cadreur | `architecte/cadreur.md` | Requêtes empilées, chacune ouvrant sur `# Request N` (`1` puis le numéro libre suivant) ; une requête peut s'accompagner d'un `code/blocked_cadreur.md` dont `## Where` vaut `architecte/cadreur.md — Request N`, et c'est le `## Verdict` de cette requête qui lève le blocage |
| detailleur | `architecte/detailleur-<lot>.md`, suffixe `-2` pour une seconde sur le même lot ; une requête de la marche est classée sous le premier lot du bloc | Ne bloque jamais dessus — sauf l'absence de dossiers de code dans les conventions ; la fiche nomme la requête sous `## Requests` |
| concepteur | `architecte/concepteur-<lot>.md`, suffixe `-2` | Un placement que les conventions ne règlent pas ; ne bloque jamais, place en attendant dans le module de la dépendance la plus forte et le dit sous `## Where I met it` |
| realisateur | `architecte/realisateur-<lot>.md`, suffixe | Une condition d'exécution que rien n'énonce ; la requête est ce que seule la vérification a exigé, le blocage ce qui change le code ; nommée sous `## Requests` du rapport |
| arbitre | `architecte/arbitre-<lot>-blocking-N.md` (pour `code/<lot>/blocked_realisateur.md`) · `architecte/arbitre-block-N-blocking-N.md` (pour `code/blocked_detailleur.md`), `N` après `blocking` la plus basse `## Blocking N` que la requête réunit ; suffixe `-NN` si le nom est déjà pris par un verdict rempli — un lot bloque plus d'une fois, un nom par lot écrasait la requête précédente | Second titre `## Why the block cannot be settled without it` ; une seule requête par invocation, réunissant chaque entrée qui a besoin d'une règle ; l'Architecte est appelé aussitôt et le verdict copié — numéro et texte — dans `## Decision` |

L'Architecte (invocation 3) ouvre chaque fichier du dossier, règle chaque bloc de requête dont `## Verdict` est vide — un bloc sans titre `## Verdict` compte pour vide, il ajoute le titre — et écrit le verdict sous le `# Request N` qu'il répond, jamais en fin de fichier ; le verdict porte le texte de la règle, pas seulement son numéro (`Convention — R93 written.` puis le texte ; `R30 changed.` ; `Already carried` ; `Not a convention` avec où cela va ; un refus). Une règle ajoutée reçoit sa ligne dans `couverture.md` de la feature, le nom du fichier de requête (et `— Request N`, ou le préfixe `bugfix-NN/`) en première colonne, `requête` où serait la nature. `/7_lots` (une fois le découpage tenu) et `/8_code` (à la fin de chaque lot, jamais pendant) invoquent l'Architecte une fois sur toutes les requêtes à verdict vide, `Called by the orchestration.` ; l'Arbitre l'invoque `Called by the Arbitre.`, et alors l'Architecte n'écrit jamais de fichier de blocage — le refus va dans le verdict.

Coût et écarté : la requête sans blocage, sauf le Cadreur quand la réponse change ce que le lot déclare · écarté : bloquer sur chaque règle manquante · raison : un fichier de blocage coûte un aller-retour au Product Owner pour ce que l'Architecte règle de toute façon (`concepteur.md`, `detailleur.md`) · inconnu. Un identifiant `# Request N` par requête empilée · écarté : un `## Where` nommant le fichier · raison : ni le Cadreur ni `/7_lots` ne pouvaient dire quel verdict lève le blocage (`docs/verification3/plan.md` entrée 8) · inconnu. Les blocs réglés un par un, jamais le fichier sauté · écarté : sauter un fichier dont un verdict est rempli · raison : la seconde requête d'un fichier réglé n'était jamais répondue (`docs/verification3/plan.md` entrée 30) · inconnu. Le texte de la règle dans le verdict · écarté : le numéro seul · raison : l'agent qui lit le verdict n'ouvre pas les conventions et copie ce que le verdict dit (`architecte.md`, invocation 3) · inconnu.

### Fichiers du découpage

Utilisé par: cadreur, verificateur, arbitre (scripteurs) ; le Product Owner (`## Décision du Product Owner`) ; `/7_lots`, `/8_code`, detailleur, relecteur, realisateur, `/9_controle`, `/audit_conventions` (lecteurs).

**`code/decoupage.md`** — écrit par le Cadreur : un inventaire `## Symbols` en tête (un symbole par bloc, une ligne par chose demandée avec les entrées qui la demandent ; `— piece` pour une pièce ; sur un cycle de correction `— bearer, <couche>` sur la ligne d'un porteur) ; puis un `## lot-NN` par lot avec cinq champs — `Anchor:` (les entrées citées avec leur titre, `§3.2 — <titre>; §3.5 — <titre>`, toutes d'une section, plus `(B<n>)` sur un cycle de correction), `Needs:` (symboles, `(pre-existing)` ou `(lot-NN)`), `Produces:` (symboles, avec qui les appelle : `(called by lot-05)`, `(mounted by the system)`), `Modifies:` (symboles), `Touches:` (fichiers par chemin : appelants, tests, manifeste, fichiers de build ; `—`) — et, en fin, `## Entries with no lot`, une ligne par entrée non citée, `§4.7 — <raison>` (→ `### Les trois formes de « Entries with no lot » — pourquoi une entrée n'a pas de lot`). Pas de prose entre lots. Numéros de lot à partir de 1 par feature, jamais réutilisés. Lecteurs : le Vérificateur (entier), le Détailleur (les lots de son bloc et `## Symbols`), `/7_lots` (les titres `## lot-`), `/9_controle` (les lignes `Anchor:` et `## Entries with no lot`), `/audit_conventions` (les lignes `Anchor`), `/2_structure` et `/6_convertit` (son existence : le découpage est fait, plus de reconversion).

**`code/sequence.md`** — écrit par le Vérificateur, réécrit à chaque tour, jamais archivé : `Round: N` en première ligne (le numéro du précédent plus un quand son `## Defects` portait des lignes, `1` sinon), `## Order` (les identifiants de lot, ordonnés), `## Blocks` (`block-1: lot-01, lot-04`), `## Defects` (une ligne par défaut, trois champs séparés par `|` : le lot ou l'entrée, le type, `"<ligne citée mot pour mot>" >> <attendu>`), et `## Redécoupage: archivable` sur un redécoupage dont `## Defects` est vide. Lecteurs : le Cadreur (`## Defects`, `Round:` — trois tours au plus, comptés sur cette ligne), `/7_lots` (`## Defects`, `block-N:`, la ligne archivable qu'il retire après le `git mv`), `/8_code` (l'ordre, les blocs, `## Defects` non vide arrête), le Détailleur (les lots de son bloc), le Relecteur (la ligne de bloc de son lot, par grep, sur une divergence), le Vérificateur du tour suivant (le précédent, entier).

**`code/redecoupage.md`** — écrit par l'Arbitre quand le découpage lui-même est faux, ajouté en fin s'il existe : `## Ce qui bloque`, `## Où`, `## Ce qui est déjà codé` (chaque lot dont `verdict.md` porte `PASS`), `## Ce qui ne l'est pas`, `## Ce que le découpage doit permettre` (la contrainte, jamais la solution) — titres en français, gardés tels quels. Le Cadreur (bloc C) le lit entier avec les `code/redecoupage-NN.md` à côté et y ajoute `## Ce qui revient` et `## Ce que j'en fais` ; le Product Owner y écrit `## Décision du Product Owner` après un troisième retour ; le Vérificateur en lit `## Ce qui est déjà codé` ; `/7_lots` en relaie les deux sections du Cadreur puis le renomme `code/redecoupage-NN.md` ; `/8_code` compte les archivés au-dessus du plus haut portant `^## Décision du Product Owner`, plus celui en place — trois arrête ; le Réalisateur et le Détailleur testent sa présence pour savoir si le découpage a été refait.

Coût et écarté : `Round:` compté sur le fichier · écarté : un compte en contexte ou sur des fichiers · raison : une reprise à froid n'a pas de contexte et rien n'archive `code/sequence.md` (`cadreur.md`, `verificateur.md`) · inconnu. Une décision achète un tour · écarté : remettre le compte à zéro · raison : `docs/verification4/plan.md` entrée 19, item D, Option 1 · non éprouvée. `## Décision du Product Owner` nommé au Product Owner et au Cadreur · écarté : un titre que seul `/8_code` connaît · raison : le compte ne se remettait jamais à zéro, le titre n'étant nommé à personne (`docs/verification4/plan.md` entrée 3) · non éprouvée. Les titres français de `redecoupage.md` · écarté : l'anglais comme partout · raison : le Cadreur ajoute sous eux et `/7_lots` les relaie par ces noms (`arbitre.md`, *Prose*) · inconnu.

### Fichiers d'un lot

Utilisé par: detailleur, concepteur, testeur, realisateur, relecteur (scripteurs) ; concepteur, testeur, realisateur, relecteur, controleur, arbitre, cadreur, detailleur, `/8_code`, `/9_controle` (lecteurs).

Sous `code/<lot>/`, un fichier par agent, chacun à champs fixes, chacun lu par les suivants :

| Fichier | Scripteur | Champs | Lecteurs |
|---|---|---|---|
| `fiche-executable.md` | detailleur, une par lot du bloc | `## Signatures` (chaque symbole ouvrant sur `created` ou `modified`, et ce que vaut le retour aux bords), `## Acceptance criteria` (une liste non numérotée), `## Dependencies` (`<type> — pre-existing` ou `— produced by lot-NN`), `## Files` (le `Touches` du lot, un chemin par ligne, `—`), `## Test data` et `## Resources` (chaque chemin des lignes `Data:` des entrées citées, rangé par où il pointe — `docs/features/…` ou `docs/donnees/…` —, `—`), `## Conventions` (`R<n> · <texte>`, les `spécifique` seules, `—`), `## Requests` (les requêtes écrites, `—`) | concepteur, testeur, realisateur, relecteur (les trois sections que la checklist exige : `## Signatures`, `## Acceptance criteria`, `## Conventions`), controleur, arbitre ; `/8_code` (existence), detailleur (relecture en divergence) |
| `conception.md` | concepteur | `## Declared` (un symbole par ligne, sa marque, le fichier créé ou existant), `## Compile` (la commande et son issue), `## Decision applied` (le fichier ou `—`), `## Outside the lot` (`—` ou la liste) | testeur, realisateur, relecteur, `/8_code` |
| `tests.md` | testeur | `## Tests` (critère et test), `## Criteria with no test`, `## Red` (la commande, chaque test neuf rouge, chaque test laissé vert par la déclaration seule, les anciens passés), `## Created` (le fichier de test créé, les copies des fichiers de `## Test data`, `—`), `## Decision applied`, `## Outside the lot` | realisateur, relecteur, `/8_code` |
| `compte-rendu.md` | realisateur, amendé sur une reprise, jamais réécrit depuis le code | `## Symbols` (chaque symbole et sa marque), `## Outside the lot`, `## What governed the code, besides the sheet` (le fichier de blocage, les `R<n>`, `—`), `## Build`, `## State` (`Added:`, `Removed:`), `## Resources` (chaque fichier de `## Resources` de la fiche et le chemin de sa copie, `—`), `## Requests` | relecteur, `/8_code`, detailleur (grep `**/compte-rendu.md`, jamais ouvert), arbitre, realisateur suivant |
| `verdict.md` | relecteur, remplacé au même chemin | `## Status`, `## Attempts` (le précédent plus un, `1` sans précédent), `## Verified` (la réclamation de `## Build`, copiée), `## Findings` (une ligne par point, ou par réserve ; `—`), `## Cause`, `## Causes so far` (toutes, dans l'ordre), `## Symbol divergences` (symbole, écart, lots touchés ou *affects none* ; `—`) | `/8_code` (cinq champs), `/9_controle` (`## Status`, les réserves de `## Findings`), detailleur (`## Status` par grep), arbitre (`## Status`), cadreur (PASS = lot fermé), relecteur suivant (`## Attempts`, `## Causes so far`), realisateur (sur `Verdict:`) |
| `reprise_realisateur.md` | realisateur, sur une décision restée vide | `## Reprise` : `Fait`, `Non fait`, `Bloqué sur`, `En chantier` | realisateur suivant ; `/8_code` (nommé au prompt, renommé après) |

Tout lecteur de `## Status` apparie le préfixe `PASS` : `PASS with reservation` est un lot codé. `/8_code` supprime `fiche-executable.md`, `conception.md`, `tests.md`, `compte-rendu.md` sur une cause `sheet` (le verdict reste : son `## Attempts` est le compte) et les cinq avec `verdict.md` sur un retour au découpage ; chaque lecteur tolère leur absence.

Coût et écarté : un fichier par agent, à champs fixes · écarté : un rapport libre · raison : « the report is the only trace the orchestration keeps of the lot » (`relecteur.md`, point 4) · inconnu. `compte-rendu.md` dans les listes de suppression · écarté : hors liste · raison : un rapport survivant faisait réutiliser au Détailleur un symbole que le revert avait retiré (`docs/verification4/plan.md` entrée 4, F01) · non éprouvée.

### Fichiers déclarés d'un lot

Utilisé par: detailleur (`## Files`), concepteur (`## Declared`), testeur (`## Created`), realisateur (`## Resources`) — scripteurs ; concepteur, testeur, realisateur (`## Outside the lot`), relecteur (vérificateur).

Quatre listes déclarent les fichiers d'un lot : `## Files` de la fiche (les fichiers existants que le lot ouvre sans déclarer de symbole, copiés du `Touches`), `## Declared` du rapport de conception (les fichiers où chaque déclaration a atterri, créés ou existants — personne ne connaît le chemin d'un fichier créé avant que le Concepteur place le symbole), `## Created` du rapport de test (le fichier de test créé quand celui des tests n'existait pas, et la copie de chaque fichier de `## Test data`), `## Resources` du rapport du Réalisateur (la copie de chaque fichier de `## Resources` de la fiche, dans le dossier de ressources du module). Un fichier dans l'une des quatre est déclaré. Chacun des trois agents de lot à `Bash` écrit sous `## Outside the lot` tout fichier qu'il a touché et qu'aucune des quatre ne nomme — une décision l'a autorisé, ou le module ne compilait pas sans — ou un tiret ; le Relecteur vérifie les trois `## Outside the lot` ensemble contre la liste de fichiers que le prompt lui donne (le diff depuis le premier commit du lot) : un fichier changé et nommé nulle part est un changement que personne ne peut attribuer.

Coût et écarté : quatre listes plus un champ par agent · écarté : une liste unique · raison : le fichier créé par le Testeur tombait sous `## Outside the lot` par sa propre définition (`docs/verification3/plan.md` entrée 42) · inconnu. Une copie de données déclarée par l'agent qui la fait · écarté : la ranger sous `## Outside the lot` · raison : une copie que la fiche demande est le travail du lot, pas un écart (`testeur.md`, `realisateur.md`) · non éprouvée.

### Identifiants

Utilisé par: tous les agents ; toutes les commandes.

| Forme | Ce qu'elle nomme | Qui l'attribue | Qui la greppe |
|---|---|---|---|
| `B<n>` | Un bloc du fichier produit ; `B7` ≠ `B70`, l'espace du titre ferme le nombre | redacteur, decoupeur (jamais réattribué) | tout l'amont ; `(B<n>)` en fin de première ligne d'un manque de `bug-list.md`, repris dans le titre d'entrée de `desc-bug.md`, dans l'`Anchor:` du lot, puis lu par `/9_controle` pour marquer `carried` |
| `§n` · `§n.m` | Une section, une entrée du document technique ; jamais `§3` seul dans un `Anchor` | convertisseur (par nature, dans l'ordre des blocs), diagnostiqueur ; numéroté à l'écriture, jamais renuméroté après le découpage | cadreur, verificateur (`^### §`), detailleur, architecte (`couverture.md`), `/7_lots`, `/9_controle`, `/audit_conventions` |
| `lot-NN` | Un lot ; à partir de 1 par feature, le libre suivant pour un ajout, gardé sur une recoupe | cadreur | verificateur, `/7_lots`, `/8_code`, detailleur, relecteur, `/9_controle`, `9_controle`'s `tracabilite-full.md` |
| `block-N` | Un bloc de lots dans `## Blocks` | verificateur | detailleur (son bloc), `/8_code`, arbitre (`arbitre-block-N-blocking-N.md`) |
| `Q<n>` | Une question, à partir de `Q1` par fichier | chaque scripteur de fichier de questions ; l'assembleur et `/6_convertit` renumérotent | le Product Owner ; `PENDING questions-fusionneur-04 Q3` dans un plan |
| `R<n>` | Une règle des conventions, une séquence pour tout le fichier, jamais réutilisé ni décalé, gardé si retiré | architecte | detailleur, realisateur, relecteur, arbitre, `/audit_conventions` |
| `# Request N` | Une requête empilée dans `architecte/cadreur.md` | cadreur | cadreur (`## Where`), architecte, `/7_lots` |
| `## Blocking N` (`— lot-NN`) | Une entrée d'un fichier de blocage à plusieurs entrées | qualifieur, classeur, redacteur (3), detailleur, realisateur | arbitre, `/8_code`, `/2_structure`, `/3a_genre`, `/3b_nature`, `/9_controle` |
| `G<n>` | Un manque de `bug-list.md` (`G01`), écrit par le Product Owner, lu et jamais compté — et, sans rapport, un groupe de `/9_controle` (`G1`, tel que `grouper.py` l'imprime) | le Product Owner ; `grouper.py` | `/diagnostique`, diagnostiqueur ; controleur |
| `NN` | Un numéro de fichier : questions, blocages archivés, `bugfix-NN`, `redecoupage-NN`, `rapport-controle-NN`, `closed/*-NN` | → `### Renommage -NN — divergence` | |

Coût et écarté : des identifiants stables, jamais réattribués · écarté : renuméroter · raison : un fichier de questions adresse un bloc par numéro, un lot cite une entrée par numéro, et une citation doit tenir (`redacteur.md`, `convertisseur.md`, `cadreur.md`) · inconnu. `G<n>` écrit par le Product Owner · écarté : compté par position · raison : un manque inséré entre deux runs décalait les identifiants (`docs/verification4/plan.md` entrée 40, item I) · non éprouvée.

### Marque carried

Utilisé par: `/9_controle` (scripteur, dans `tracabilite-full.md` et le prompt) ; controleur (lecteur).

`/9_controle` marque `carried` un bloc dont une entrée porte, sous `## Entries with no lot`, la raison `already carried by the code`, ou dont l'identifiant figure en `(B<n>)` dans une ligne `Anchor:` d'un `bugfix-NN/code/decoupage.md` — le mot après les lots ou après le tiret sur la ligne de `tracabilite-full.md`, et `(carried)` après l'identifiant dans la ligne `Blocks:` du prompt de l'invocation 1, jamais dans celle de l'invocation 2. Le Contrôleur confronte un bloc marqué comme un autre, intention par intention : trouvée avec une fiche, ou trouvée avec la marque pour raison, jamais `Missing` ; une ligne unique sous `## Intentions found` quand aucune de ses fiches n'en porte une intention. Le script `grouper.py` ne conserve pas la marque : elle est relue dans `tracabilite-full.md` au moment d'écrire les prompts.

Coût et écarté : la marque sur le bloc, jamais sur l'intention · écarté : par intention · raison : le Contrôleur distingue les deux, pas la commande (`/9_controle`, phase 1 c ; `docs/verification3/plan.md` entrée 59) · inconnu.

---

# Les ensembles fermés

### Les six genres — le genre d'un bloc

Écrit par: qualifieur (la ligne `Genre:`) ; le Product Owner (une décision nommant un genre, écrite par le qualifieur)
Lu par: redacteur, decoupeur (la ligne vide) ; classeur (`comportement`) ; sondeur (`comportement`, `transverse`, `hors périmètre`) ; convertisseur (par les fichiers de `par-genre/`) ; fusionneur ; architecte ; `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/9_controle`
Les valeurs — la ligne vaut `Genre: ` puis le nom, en minuscules, accents et espace compris, rien d'autre :
- `comportement` — ce que le produit fait, montre ou refuse ; le cas commun, atteint par élimination ; le seul genre qui a une nature et le seul que la grille sonde ; `/3b_nature`, `/4_grille`, `/5_reclasse`, `/9_controle` greppent `^Genre: comportement$` ; fichier `par-genre/comportements.md`
- `directive` — un moyen imposé par le Product Owner (bibliothèque, stockage, format, police), sans déclencheur ni sortie ; lu par l'Architecte dans `par-genre/directives.md` ; n'entre jamais dans le global
- `transverse` — une règle dont le sujet est une catégorie, pas un objet du produit ; tenu à côté des blocs sondés ; scindé par l'invocation 2 du Convertisseur en une entrée et une contrainte de `## Cross-cutting rules` ; un bloc `transverse` changé marque tout le fichier `MODIFIED` ; fichier `par-genre/transverses.md`
- `référence` — un catalogue, une table de formats que les comportements citent ; §9 Text du document technique ; fichier `par-genre/references.md` ; un tiret de traçabilité y lève `inconsistency` comme sur un comportement
- `hors périmètre` — ce que le Product Owner met de côté explicitement ; nommé au seul sondeur global ; `## Out of scope` du préambule ; fichier `par-genre/hors-perimetre.md` ; n'entre jamais dans le global
- `recette` — ce que le Product Owner veut vérifier elle-même sur l'appareil ; fichier `par-genre/recette.md`, source de la phase 4 de `/9_controle`

Une valeur hors des six arrête `/5_reclasse` ; un qualifieur qui la reçoit en décision laisse la ligne vide et le dit. Le fichier de `par-genre/` prend le pluriel, sans accent, un tiret pour l'espace. Divergence : aucune — chaque lecteur qui énumère en nomme six (fusionneur, architecte, `/5_reclasse`, `/9_controle`) ; les autres ne lisent qu'une ou trois valeurs et le disent.

### Les huit natures — la nature d'un bloc

Écrit par: classeur (la ligne `Nature:`) ; diagnostiqueur (la nature d'un porteur, invocation 2)
Lu par: sondeur (ordre de lecture par nature), convertisseur (une invocation par nature, une section par nature), cadreur (une section par nature), architecte (`couverture.md`, seconde colonne), `/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`, `/9_controle`
Les valeurs — la ligne vaut `Nature: ` puis le nom, en minuscules, l'espace gardé (`external exchange`, jamais `external-exchange` dans le bloc ; le tiret n'apparaît que dans un nom de fichier ou de section de commande) ; dans cet ordre, qui est celui des sections §1 à §8 :
- `model` — ce qu'une donnée est : entité, champs, relations ; §1 Model
- `persistence` — ce que devient une donnée en stockage : gardée, combien de temps, purgée ; §2 Persistence
- `calculation` — une valeur dérivée d'entrées ; §3 Calculation
- `transition` — un changement d'état du domaine, sur un événement ; §4 Transition
- `external exchange` — une donnée qui traverse vers ou depuis un autre système, à sens unique, permission de plateforme comprise ; §5 External exchange
- `synchronisation` — deux copies d'une même donnée, chacune modifiable, remises ensemble ; §6 Synchronisation
- `presentation` — ce que l'utilisateur voit ou reçoit, par tout canal, et la réponse visible à chaque action ; §7 Presentation
- `access` — un droit d'agir dans l'application, accordé ou refusé ; §8 Access

Un bloc prend la nature de ce qu'il produit, jamais de ce qui le déclenche ; une action de l'utilisateur est un déclencheur, jamais une nature. Une valeur hors des huit arrête `/5_reclasse` ; un classeur qui la reçoit en décision laisse la ligne vide et le dit. Divergence : aucune — `/5_reclasse`, `/6_convertit`, convertisseur, cadreur, diagnostiqueur nomment les huit.

### NEW / MODIFIED — ce qui a bougé depuis le dernier tour

Écrit par: redacteur, decoupeur
Lu par: `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, qualifieur, classeur, sondeur, controleur
Les valeurs — en fin de ligne `### B`, une seule à la fois :
- `NEW` — un bloc créé, jamais fermé par la grille ; un `NEW` qui change reste `NEW`
- `MODIFIED` — un bloc changé, fermé une fois sur un texte qui ne tient plus
- rien — un bloc déjà regardé et immobile depuis

→ `### Marqueurs NEW et MODIFIED` pour qui les retire.

### États de « ## Decision » — ce qu'un fichier de blocage attend

Écrit par: le Product Owner (à la main) ; arbitre (les fichiers du detailleur et du realisateur) ; architecte (`## Verdict` en lieu de `## Decision` pour un blocage du Cadreur sur requête)
Lu par: toutes les commandes qui invoquent ; tout agent de reprise (→ `### Reprise sur décision — divergence`) ; `/audit_blocages`
Les valeurs — le test dépend de la forme du fichier :
- vide, forme à quatre ou cinq titres — `grep -A2 '^## Decision$'` ne rend qu'une ligne blanche, le titre suivant ou la fin de fichier : le blocage tient, la commande s'arrête et relaie ; l'Architecte réécrit son fichier inchangé
- remplie, forme à quatre ou cinq titres — n'importe quoi sous le titre : la commande nomme le fichier au prompt ; un bloc, une réponse, rien à compter
- vide sous chaque `## Blocking N`, forme 3 — chaque `## Decision` testé un par un ; un seul vide arrête (`/2_structure`, `/3a_genre`, `/3b_nature`) ; une décision peut nommer un genre ou une nature (écrit par l'agent), une réécriture ou un retrait (la ligne reste vide, le bloc *waits on the Rédacteur*, le fichier reste au nom non numéroté pour `/2_structure`), une valeur hors table (ligne vide, rien ne tourne)
- numérotée complète, forme 4 — chaque `## Blocking N` a sa ligne `N.` sous l'unique `## Decision` (grep `^## Blocking ` contre les lignes numérotées) : remplie
- numérotée partielle, forme 4 — moins de numéros que de titres : l'agent a appliqué les répondus et s'est arrêté sur les autres ; la commande s'arrête sans renommer ; le numéro absent est le signal, jamais un numéro vide ni une note ; le detailleur l'énumère à la reprise — un `## Blocking N` sans numéro dessous est un blocage encore debout, il s'arrête (`detailleur.md` L491)
- `Not settled here. <whose it is, and why>` — l'Arbitre sur un blocage qui n'est pas le sien (Relecteur, Architecte, Cadreur avec requête) ; le Réalisateur s'arrête et relaie la ligne. Pas une divergence : la valeur n'atteint ni le Détailleur ni `/8_code` — l'Arbitre ne l'émet que sur un bloc dont `Written by` n'est ni detailleur ni realisateur (`arbitre.md` L172-177, L275-281) ; le fichier du Détailleur est le sien, et aucun des cinq fichiers que 4b lit ne peut la porter, `/8_code` n'invoquant jamais l'Arbitre (`8_code.md` L733)
- une décision qui renvoie le lot au découpage — testée par la présence de `code/redecoupage.md`, jamais par les mots de la décision (realisateur, detailleur, `/8_code`)
- le `## Verdict` d'une requête, forme 1 empilée du Cadreur — `## Decision` reste vide ; rempli sur le `# Request N` que `## Where` nomme, il lève le blocage (cadreur, `/7_lots`) ; refusé, le blocage tient et le Product Owner décide
- absent — forme 5 du Vérificateur : rien n'est à trancher

### Valeurs de « ## Invocation » — qui a écrit ce fichier de blocage

Écrit par: redacteur (1, 2, 3), fusionneur (1, 2, 3), architecte (1, 2, 3, 4)
Lu par: `/2_structure` (redacteur : 1 ou 2 est le sien, 3 est à `/fusion`), `/fusion` (redacteur 3 ; fusionneur, l'invocation que la ligne nomme), `/fusion_compare` (fusionneur 1 ; 2 ou 3 renvoyés), `/fusion_applique` (fusionneur 2 ; 1 ou 3 renvoyés), `/conventions` (architecte, l'invocation nommée), `/8_code` (architecte 3 seule ; une autre renvoie à `/conventions`)
Les valeurs : `1`, `2`, `3`, et `4` pour le seul architecte — chacune nommant une invocation du même agent (→ `### Numéros d'invocation`).

### Valeurs de « Called by » — qui a invoqué l'Architecte

Écrit par: `/7_lots`, `/8_code`, `/conventions` ; arbitre
Lu par: architecte, invocation 3
Les valeurs :
- `Called by the orchestration.` — personne n'attend ; un manque d'entrée donne `blocked_architecte.md`
- `Called by the Arbitre.` — l'Arbitre attend et lit son verdict ; jamais de fichier de blocage, le refus va dans `## Verdict` ; un `blocked_architecte.md` trouvé à la racine n'est pas à traiter

Jamais déduit : la ligne est toujours dans le prompt.

### created / modified — la marque d'un symbole

Écrit par: cadreur (`Produces` → `created`, `Modifies` → `modified`) ; detailleur (copie la marque en tête de chaque ligne de `## Signatures`)
Lu par: concepteur (`## Declared`, même marque ; un `modified` est édité en place, jamais déclaré à côté ni lu comme un nom pris), realisateur (`## Symbols`, même marque ; grep des `modified` dans l'état technique), relecteur (compare la marque de la fiche à celle du rapport ; un `modified` déclaré `created` a été écrit à côté de l'ancien), testeur (adapte un test que `modified` a rendu faux)
Les valeurs :
- `created` — le symbole n'existe pas et le lot le produit ; le test : la grep ne le trouve pas, ou le trouve avec un corps vide laissé par un Concepteur avant retour au découpage
- `modified` — le symbole existe et le lot le change ; la signature écrite est celle d'après ; son corps repart au `not implemented` comme un neuf (`docs/verification4/plan.md` entrée 1, item A, Option 1) ; le test : le symbole porte la nouvelle signature, pas l'ancienne

### permanente / spécifique — ce qui déclenche une règle

Écrit par: architecte (troisième champ de chaque ligne `R<n> · <règle> · <déclencheur> · <vérification>`)
Lu par: concepteur, testeur, realisateur, relecteur (les `permanente` entières), detailleur (nomme les `spécifique` sous `## Conventions`)
Les valeurs :
- `permanente` — un acte ordinaire d'écriture ou de livraison de code la déclenche, dans tout lot ; trois sortes le sont toujours : où vit une sorte de symbole, les commandes qui compilent, analysent et testent, les états dans lesquels un lot peut être livré — la grille tire les deux dernières toujours, par la table des commandes de G2.1 en C2 ; lue entière par chaque agent de lot
- `spécifique` — ce que ce lot fait en particulier la déclenche (un module, une frontière, une technologie) ; nommée d'avance dans la fiche par le Détailleur, ou tenue par personne

Le quatrième champ (`mechanical` · `review`) et le cinquième (`off-grid`) n'ont qu'un scripteur et aucun lecteur qui les énumère → renvoyés.

### Les quatre statuts d'un verdict — l'issue d'une revue

Écrit par: relecteur (`## Status`, un des quatre mots, seul sur sa ligne)
Lu par: `/8_code`, `/9_controle`, detailleur, arbitre, cadreur (préfixe `PASS`) ; realisateur (`FAIL mineur`, `FAIL structurel`, `## Status` absent)
Les valeurs :
- `PASS` — les cinq points passent ; le lot est codé et fermé
- `PASS with reservation` — un point passe mais vaut d'être noté ; la réserve va dans `## Findings`, une ligne par point ; son lecteur est `/9_controle`, qui la relaie au Product Owner ; codé pour tout lecteur du préfixe
- `FAIL mineur` — tout le reste, quel que soit le nombre de constats ; une correction ciblée par un Réalisateur neuf, une re-revue entière
- `FAIL structurel` — le module du lot rouge ou ses tests non lancés (première règle de tête), une section manquante de la fiche (`Cause` `sheet`), ou un symbole promis absent ou divergent sans décision (point 1) ; le lot est repris du mouvement 1

Tout lecteur apparie le préfixe `PASS`. Divergence : aucune — `PASS` et `PASS with reservation` n'atteignent pas le realisateur : il n'est invoqué sur un verdict que sur FAIL (`8_code.md` L240, L547-549), et une reprise sur décision remplie passe le fichier de blocage, jamais `Verdict:` (`8_code.md` L74-78, L538-543) ; `/8_code` dit que `FAIL mineur` et `FAIL structurel` sont un seul FAIL pour elle, la forme étant celle du Réalisateur, et branche sur `## Cause` seul (`8_code.md` L244-248).

### Les trois causes d'un FAIL — d'où vient la faute

Écrit par: relecteur (`## Cause`, la catégorie seule ; `## Causes so far`, toutes, dans l'ordre)
Lu par: `/8_code` (`sheet` → revert et Détailleur ; `reasoning` deux fois → `opus` ; `understanding` → la reprise ordinaire, sur `sonnet`) ; realisateur (`sheet` → arrêt ; `understanding` ou `reasoning` → rien au-delà de la ligne du statut) ; relecteur suivant (copie)
Les valeurs :
- `understanding` — la fiche lue de travers ; aussi la cause d'une revue arrêtée sur un build rouge
- `reasoning` — la fiche bien lue, le raisonnement qui en part manqué ; la seule qui justifie `opus`, au seuil de deux occurrences dans `## Causes so far`
- `sheet` — la faute est en amont, dans la fiche ; `## Findings` dit ce que la fiche manque ; `/8_code` revert les commits du lot, supprime quatre fichiers, relance le Détailleur en mode ordinaire avec `Findings:` et `Your lot:` — jamais un Réalisateur ; cela compte comme une tentative ; sur un lot qui n'est pas le dernier codé, tous les lots suivants tombent avec lui

Divergence : aucune — le realisateur énumère les trois : `understanding` ou `reasoning`, rien au-delà de la ligne du statut, la cause est à l'orchestration (`realisateur.md` L605) ; `/8_code` énumère les trois : `understanding` est la reprise ordinaire sur `sonnet`, ni le revert ni le changement de modèle (`8_code.md` L321-324).

### Les onze types de défaut — ce que le Vérificateur constate

Écrit par: verificateur (deuxième champ de chaque ligne de `## Defects`)
Lu par: cadreur (les onze, une table type → correction, appliquée au lot ou à l'entrée que le premier champ nomme) ; `/7_lots`, `/8_code` (`## Defects` vide ou non, jamais les types)
Les valeurs :
- `surface` — une opération de l'inventaire qu'aucun lot ne produit ni ne modifie
- `hole` — un besoin qu'aucun lot ne produit et que le Cadreur n'a pas marqué `(pre-existing)`
- `overlap` — deux lots nommant un même symbole dans `Produces` ou `Modifies`, ou citant une même entrée hors du cas contrat-et-pièce
- `orphan` — une entrée que nul lot ne cite ni ne déclare sous `## Entries with no lot`
- `dead` — une production que nul lot n'a besoin et dont `Produces` ne nomme aucun appelant
- `cascade` — un contrat modifié dont le lot ne déclare ni réalisant ni appelant
- `anchor` — des entrées qui ne décrivent pas ce que le lot annonce, une entrée absente du document, ou aucune citée
- `section` — un `§3` nu, ou des entrées de deux sections
- `bearer` — deux lots nommant un même porteur (cycle de correction)
- `cycle` — des lots qui ont besoin l'un de l'autre ; `## Order` et `## Blocks` restent vides pour la partie non codée
- `merge` — deux lots qui n'en font qu'un, sur les seules ancres

Divergence : aucune — le cadreur énumère les onze, une ligne par type avec sa correction (`cadreur.md` L965-981, *The defects it reports* ; `section` sur `spec-technique.md` seul, `bearer` sur `desc-bug.md` seul).

### Les cinq Kind: — la sorte d'une question de l'Architecte

Écrit par: architecte (ligne `Kind:` de `questions-architecte-NN.md`)
Lu par: architecte (invocation 2) ; `/conventions` (table *What to run next*)
Les valeurs :
- `coverage` — une question de comportement que le corpus ne répond nulle part ; une question produit ; sa réponse n'est jamais une règle, le Product Owner corrige le fichier produit à la main — sauf celle dont le `Block:` nomme `G4.4`, ce sur quoi tourne l'application : l'invocation 2 en écrit la structure du projet
- `conjunction` — la question naît entre deux entrées complètes, le long d'une arête de `Consumes:` ; sa réponse devient une règle
- `inconsistency` — le corpus se contredit (un tiret de traçabilité sur un `comportement` ou une `référence`, une entrée que nulle ligne ne nomme, deux nombres) ; sa réponse corrige le document technique, `couverture.md` note `corrigé` ou `question ouverte`
- `replacement` — invocation 4 : une règle en vigueur dit le contraire de ce que la feature exige, et des lots codés suivent l'ancienne ; la question demande le choix — changer la règle, ou s'y conformer — et nomme les lots codés sous l'ancienne ; sa réponse n'est jamais une règle nouvelle : la règle en vigueur est changée en place (numéro gardé) et sa ligne de `couverture.md` porte son numéro, ou rien n'est écrit et `couverture.md` note `corrigé` ou `question ouverte` comme pour une `inconsistency` ; les lots nommés reviennent par `/diagnostique`
- `forme` — la grille manque une forme, ou une forme produit une règle inutile ; sa réponse amende la grille, par le Product Owner, `couverture.md` note `grille amendée` ou `question ouverte`

Divergence : aucune — l'architecte route les cinq à l'invocation 2 (`architecte.md` L653-708 : `inconsistency` L653-662, `coverage` L664-674, `forme` L676-687, `replacement` L689-708 ; la question posée avec son choix, L560-567 et L897-901) ; `/conventions` énumère cinq issues nommées — « a product question » (`coverage`), `conjunction` (`conventions.md` L296), `inconsistency` (L298), `forme` (L299), `replacement` (L300).

### Les trois formes de « Entries with no lot » — pourquoi une entrée n'a pas de lot

Écrit par: cadreur (la raison ouvre la ligne, après le tiret ; la prose suit une virgule)
Lu par: `/9_controle` (phase 1 b, les mots d'ouverture seuls)
Les valeurs :
- `already carried by the code` — le mouvement 3 a trouvé le symbole portant déjà ce que l'entrée demande ; la seule forme lue comme construite : la marque `carried`
- `carried by §…` — d'autres entrées la construisent, chacune nommée ; ses lots sont les leurs
- `nothing to build` — une attribution ou une frontière ; ni lot ni marque

Jamais une quatrième forme, jamais la première sur une entrée que le code ne porte pas.

### Les quatre termes du Cadreur — l'issue sur son fichier de blocage

Écrit par: cadreur (une ligne de son rapport)
Lu par: `/7_lots` (renomme et relaie sur cette ligne)
Les valeurs :
- `decision applied` — un `## Decision` rempli appliqué au découpage ; le fichier est renommé si son dernier `## Decision` est rempli, laissé et relayé comme debout si un bloc neuf s'est ajouté en dessous
- `verdict applied` — une règle écrite par l'Architecte, et coupé contre elle ; renommé
- `verdict refused` — la requête refusée ; le blocage tient, `/7_lots` relaie au Product Owner et ne réinvoque pas
- `block standing` — un `## Decision` vide que rien ne lève ; relayé

### built / blocked — l'issue d'un squelette

Écrit par: batisseur (ligne `## Status:` de `docs/BUILD_REPORT.md`, le rapport de l'application, réécrit entier à chaque run)
Lu par: `/batir` (à chaque retour du Bâtisseur) ; `/7_lots` (avant de couper, avec le commit de `## Conventions`)
Les valeurs :
- `built` — chaque commande de G2.1 est sortie à 0, chaque paquet `assemble` a été trouvé, chaque dossier de G4.4 et chaque fichier de build de G12.6 existent et déclarent ce que les tables disent ; `/batir` → `/7_lots` ; `/7_lots` coupe, si le commit de `## Conventions` est celui que `git log -1 --format=%H -- docs/TECHNICAL_CONVENTIONS.md` donne
- `blocked` — tout le reste, une requête en attente comprise ; `/batir` aiguille sur ce qui est à côté (fichier de blocage, requête) ; `/7_lots` renvoie à `/batir`, comme sur un rapport absent ou un autre commit

Divergence : aucune — les deux lecteurs énumèrent les deux valeurs.

### Les verbes du plan de fusion — ce qu'une phrase devient

Écrit par: fusionneur (invocation 1, `plan-fusion.md` ; invocation 2 résout `PENDING`)
Lu par: fusionneur (invocation 2) ; `/fusion`, `/fusion_applique` (le seul mot `INIT`, par grep)
Les valeurs — une ligne par phrase sous `### <bloc>`, sous `## <section>` :
- `REPLACE: "…" → "…"` — la même chose dite autrement
- `INSERT: "…"` — sans correspondant
- `KEEP: "…"` — identique
- `DELETE: "…"` — jamais de l'invocation 1 : seulement sur une réponse confirmant qu'une règle ne tient plus
- `PENDING questions-fusionneur-NN Qn: "…"` — en attente d'une réponse ; sous un titre de section, finissant par le mot `title`, la question de titre, une au plus, où un `[new block]` entre
- `INIT` — seul, sans ligne en dessous : un global qui ne tient que `# Application` ; la commande copie `desc-produit-fusion.md` sur `docs/PRODUIT_GLOBAL.md` avant d'invoquer, et l'agent retire ce qui n'appartient qu'au fichier de feature

Marques hors verbe : `[new block]`, `[new section]`.

### Plafonds par couche — ce qu'un lot et un bloc peuvent porter

Écrit par: cadreur (symboles par lot), verificateur (lots par bloc)
Lu par: cadreur (se borne, rapporte un lot coupé maladroitement), verificateur (groupe, rapporte un bloc qu'il n'aurait pas coupé ainsi), `/7_lots` (relaie la remarque au Product Owner, qui déplace les plafonds)
Les valeurs — six couches, mêmes noms, même ligne par défaut ; une section du document technique est appariée à une couche sur ce dont elle parle, jamais sur son titre, et une section sans couche prend la ligne par défaut, dite dans le rapport :

| Couche | Symboles par lot (`Needs` + `Produces` + `Modifies`) — cadreur | Lots par bloc — verificateur |
|---|---|---|
| Data shapes and their storage | 4 | 9 |
| Domain rules | 6 | 7 |
| What reads and writes storage | 6 | 7 |
| What holds a screen's state | 8 | 5 |
| What the user sees | 10 | 4 |
| Anything else | 6 | 5 |

Un point de départ, pas une mesure : aucun cycle n'a été mené contre eux. Un nombre, jamais une fourchette. Sur un cycle de correction le Vérificateur groupe par contiguïté seule, au plus bas plafond des couches présentes.

### Ordres de lecture des sondeurs — ce qui distingue les trois angles

Écrit par: `/4_grille` (ligne `Your reading order:` du prompt)
Lu par: sondeur, invocation 1
Les valeurs — la seule ligne qui diffère entre les trois angles, et le nom du fichier de sortie qui va avec :
- `block by block, in the document's order` — chaque question de grille portée à un bloc avant le suivant → `cadrage-produit/par-bloc.md`
- `question by question` — une question portée à chaque bloc, puis la suivante → `cadrage-produit/par-question.md`
- `by nature` — les blocs d'une nature côte à côte, chacun par toutes les questions, puis la nature suivante → `cadrage-produit/par-nature.md`

### Found / Missing / Doubtful — le sort d'une intention

Écrit par: controleur (invocation 1, les trois champs `## Intentions found`, `## Intentions missing`, `## Doubts` de `code/controle/<group>.md` ; invocation 2 les fusionne dans `code/rapport-controle.md`)
Lu par: controleur (invocation 2, sans rejuger) ; `/9_controle` (phase 5 : `## Doubts` et `## Intentions missing` du dernier rapport)
Les valeurs :
- trouvée (`## Intentions found`) — un critère ou une signature l'observe, la fiche nommée ; ou `unchanged, nothing to build` ; ou `carried, built by a correction cycle`
- manquante (`## Intentions missing`) — aucune signature ni critère des fiches du groupe ne l'observe ; un fait, pas un doute ; jamais sur un bloc marqué `carried`
- douteuse (`## Doubts`) — un critère peut l'observer sans que la fiche dise lequel ; une fiche nommée absente ; à l'assemblage, un bloc que nul partiel ne mentionne, un écart entre la ligne `Blocks:` d'un partiel et celle du prompt, un groupe sans partiel

### Rouge / vert par la déclaration seule — l'état d'un test neuf

Écrit par: testeur (sous `## Red` de `code/<lot>/tests.md` — la commande qui a tourné, puis une ligne par test neuf rouge, puis une ligne par test laissé vert ou un tiret, puis que chaque test ancien passe ; mouvement 4)
Lu par: realisateur (un test nommé vert n'est pas à rendre vert ; `## Red` est ce qu'il prend pour acquis sans relancer les tests) ; relecteur (point 2 : un test nommé vert par déclaration est le test de son critère ; il ne lance aucun test)
Les valeurs — chaque test neuf est l'un ou l'autre, jamais un troisième :
- rouge — le test échoue contre le corps qui jette *not implemented* ; le test : il appelle un corps, et tout ce qui appelle un corps lève ; un test neuf qui passe en appelant un corps est réécrit, il n'affirme rien
- vert par la déclaration seule — le test affirme une déclaration seule (la présence d'un champ, l'arité d'un constructeur, les membres d'une enum) et le critère est tenu par la déclaration ; le test : il passe sans appeler un corps ; laissé vert, jamais affaibli pour le rendre rouge, et nommé sous `## Red` — un vert non nommé se lit comme un test qui n'affirme rien

Un test ancien n'entre pas dans cet ensemble : il passe, ou il échoue sur le *not implemented* et le Réalisateur le rend vert, ou il est adapté à une signature `modified`. Divergence : aucune — les deux lecteurs lisent les deux états (`realisateur.md`, *What you read* ; `relecteur.md`, point 2).

---

## Renvoyés aux documents de parcours

Un seul utilisateur : décrit dans le document de l'agent ou de la commande qui le porte, pas ici.

- `missing` · `wrong` · `set aside` — le verdict d'une investigation ; le diagnostiqueur seul (invocation 1 écrit, invocation 2 lit) → `PROCESS_ENTREES.md` §diagnostiqueur, invocation 1 — Investigation : confirmer un manque contre le code, §diagnostiqueur, invocation 2 — Assembly : assembler les rapports en `desc-bug.md`
- `## Verdict` · `## Bearer` · `## Trigger` (finissant par `observed`, `nothing observes it` ou `none — …`) · `## Today` · `## Expected` · `## Searched` — les six titres d'un rapport `investigation/<id>.md` → `PROCESS_ENTREES.md` §diagnostiqueur, invocation 1 — Investigation : confirmer un manque contre le code
- `blocking` · `assumed` · `misplaced` — les trois mots du rapport du Convertisseur ; aucune commande ne les lit → `PROCESS_AMONT.md` §convertisseur, invocation 1 — Nature : écrire la section d'une nature, §convertisseur, invocation 2 — Transversal : le préambule, §9 Text, les références, la traçabilité
- `mechanical` · `review` · `off-grid` — les quatrième et cinquième champs d'une règle ; l'architecte seul → `PROCESS_AMONT.md` §architecte — ce qui vaut pour ses quatre invocations
- `corrigé` · `question ouverte` · `grille amendée` · `requête` · `directive` · `no rule` — les mentions de `couverture.md` ; l'architecte seul les écrit et seul les énumère en les relisant (invocations 2, 3, 4) ; `/audit_conventions` lit aussi `couverture.md`, ligne par ligne, pour l'entrée que chaque règle trace (constats 1, 4 et 7 — une règle tracée à aucune entrée vient d'une requête), sans jamais lire ces mots comme des valeurs (`audit_conventions.md`, *What you read*, *couverture.md*) → `PROCESS_AMONT.md` §architecte — ce qui vaut pour ses quatre invocations ; `PROCESS_ANNEXES.md` §/audit_conventions — lire ce que les conventions ont gagné pendant un cycle et rapporter ce que cela coûte
- V1 à V10, C1 à C12, `R2`, `R3`, `R4` — les lectures et entrées de `GRILLE_CONVENTIONS.md` ; l'architecte seul → `PROCESS_AMONT.md` §architecte — ce qui vaut pour ses quatre invocations
- Pass A, B, C et `C1.2` — les passes de `GRILLE_CADRAGE_PRODUIT_V2.md` ; le sondeur seul → `PROCESS_AMONT.md` §sondeur, invocation 1 — Angle : la passe A de la grille de cadrage, trois à la fois, un ordre de lecture chacun, §sondeur, invocation 2 — Global : le relevé de chaque comportement, puis les passes B et C
- Les fermetures de `GRILLE_FERMETURE_TECHNIQUE.md` par nature et à travers les sections ; le convertisseur (le diagnostiqueur en lit trois nommées, pas les mêmes) → `PROCESS_AMONT.md` §convertisseur, invocation 1 — Nature : écrire la section d'une nature, §convertisseur, invocation 2 — Transversal : le préambule, §9 Text, les références, la traçabilité ; `PROCESS_ENTREES.md` §diagnostiqueur, invocation 2 — Assembly : assembler les rapports en `desc-bug.md`
- `## Tranché` déplacement des termes, les trois balayages, les quatre lectures d'une paire, `remplace :`, `dans ce sens seulement` — le lexicographe seul → `PROCESS_AMONT.md` §lexicographe, invocation 1 — Sweeping : balayer les termes de l'idée et lever les paires, §lexicographe, invocation 2 — Settling : appliquer les réponses à l'idée et régler le lexique, §lexicographe, invocation 3 — Watching : balayer les réponses d'un autre agent, §lexicographe, invocation 4 — Correcting : appliquer ses propres réponses au fichier répondu
- La table des préfixes qui retirent les marqueurs (`sondeur`, `existant`, `convertisseur` contre `qualifieur`, `classeur`, `redacteur`) — le redacteur seul → `PROCESS_AMONT.md` §redacteur, invocation 2 — Integrating : intégrer un fichier répondu ou une décision de réécriture
- Le test pour `transverse` et l'asymétrie des deux doutes — le qualifieur seul → `PROCESS_AMONT.md` §qualifieur — écrire la ligne `Genre:` de chaque bloc nommé
- Les frontières entre natures et les trois doutes — le classeur seul → `PROCESS_AMONT.md` §classeur — écrire la ligne `Nature:` de chaque comportement nommé
- Le critère du déclencheur et de la suite — le decoupeur seul → `PROCESS_AMONT.md` §decoupeur — scinder les blocs qui portent plus d'un déclencheur
- Le test de fusion « répondre à l'une répond à l'autre », la question couvrante gardée — l'assembleur seul → `PROCESS_AMONT.md` §assembleur — fusionner les quatre fichiers de questions en un
- Le test de réversibilité (ce que le Convertisseur tranche, ce qu'il demande), la scission d'une règle transverse, les neuf sections — le convertisseur seul → `PROCESS_AMONT.md` §convertisseur, invocation 1 — Nature : écrire la section d'une nature, §convertisseur, invocation 2 — Transversal : le préambule, §9 Text, les références, la traçabilité
- La table de `/6_convertit` sur quelles natures tournent (huit lignes, plusieurs pouvant s'appliquer, `cmp`/`diff -q`) → `PROCESS_AMONT.md` §/6_convertit
- La table de routage à onze lignes de `/fusion`, les trois niveaux de localisation, la liste de retrait (`Genre:`, `Global:`, `Nature:` vide, le numéro), le rapport de fusion à quatre champs → `PROCESS_AMONT.md` §/fusion, §fusionneur, invocation 1 — Compare and question : le plan de fusion, §fusionneur, invocation 2 — Apply : appliquer le plan et écrire le rapport
- La table à onze lignes de `/conventions` → `PROCESS_AMONT.md` §/conventions
- Les dix mouvements du Cadreur, les cinq déclarations d'un symbole, les pièces et les écouteurs, les blocs A/B/C/D → `PROCESS_AVAL.md` §cadreur — couper le document technique en lots livrables, puis tenir la boucle avec le Vérificateur
- Les six mouvements du Vérificateur, l'algorithme d'ordre et le départage mécanique → `PROCESS_AVAL.md` §verificateur — vérifier qu'un découpage tient et produire la séquence
- La marche du bloc, les neuf mouvements, le mode divergence, la dérivation d'une signature et les trois propriétés d'un critère → `PROCESS_AVAL.md` §detailleur, mode ordinaire — écrire les fiches exécutables d'un bloc, §detailleur, mode divergence — réécrire les fiches qu'une divergence a rendues fausses
- Le test unique de l'Arbitre, les trois mouvements, les quatre destinations d'une règle manquante, le sondage du Product Owner (toutes les 2 minutes de 0 à 10, toutes les 5 de 10 à 20, arrêt à 20) → `PROCESS_AVAL.md` §arbitre — remplir le `## Decision` d'un fichier de blocage du Détailleur ou du Réalisateur
- Les cinq points de la checklist et ses deux règles de tête → `PROCESS_AVAL.md` §relecteur — juger un lot contre sa fiche et écrire le verdict
- Les six mouvements du Testeur, le test laissé vert par la déclaration seule, `code/recette.md` → `PROCESS_AVAL.md` §testeur — écrire un test par critère, avant les corps, et vérifier qu'il est rouge
- Les cinq mouvements du Concepteur et le corps `not implemented` → `PROCESS_AVAL.md` §concepteur — déclarer les signatures de la fiche, corps `not implemented`, et compiler
- Les neuf mouvements du Réalisateur, la reprise après FAIL, deux échecs identiques de suite → `PROCESS_AVAL.md` §realisateur — première passe sur un lot : remplir les corps jusqu'à ce que les tests passent, §realisateur, reprise après FAIL — corriger ce que le verdict nomme
- Les mouvements 1 à 7 de `/8_code`, le compte de trois tentatives (`## Attempts`), la tentative vide, le retour au découpage à trois → `PROCESS_AVAL.md` §/8_code — coder les lots en attente d'un découpage, un par un
- Les six phases de `/9_controle`, `grouper.py`, le tri par état de `recette-ordonnee.md`, la forme de `decisions-produit.md` (identifiant, deux espaces, une ligne par décision) → `PROCESS_AVAL.md` §/9_controle — confronter le fichier produit à toutes les fiches
- Les cinq lieux et les cinq trouvailles de `/audit_blocages`, les sept trouvailles de `/audit_conventions` → `PROCESS_ANNEXES.md`
- `docs/PRODUIT_GLOBAL.md` à `# Application`, `docs/CURRENT_TECHNICAL_STATE.md` à `# Technical state` — ce que `socle.py` crée → `PROCESS_ENTREES.md` §socle.py

---

## Coutures

| Ce qui part | Ce qui arrive | Ce que le receveur vérifie | L'autre document |
|---|---|---|---|
| Un `blocked_<agent>.md` au nom non numéroté, `## Decision` vide (→ `### Fichier de blocage — divergence`) | Le Product Owner remplit `## Decision` à la main, dans le dépôt principal entre deux runs, dans le worktree pendant un run vif | La commande qui l'invoque teste le `## Decision` par grep avant d'invoquer : `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/6_convertit`, `/conventions`, `/diagnostique`, `/fusion`, `/fusion_compare`, `/fusion_applique` | `PROCESS_AMONT.md`, `PROCESS_ENTREES.md` |
| Le même, aval : `code/blocked_cadreur.md`, `code/blocked_detailleur.md`, `code/<lot>/blocked_*.md`, `blocked_architecte.md` | Le Product Owner, ou l'Arbitre pour les deux fichiers de forme 4 | `/7_lots` (dernier `## Decision` ; le `## Verdict` que `## Where` nomme), `/8_code` (4b : vide, partiel, rempli par forme) | `PROCESS_AVAL.md` |
| Le `## Decision` rempli, nommé au prompt (→ `### Reprise sur décision — divergence`) | L'agent l'applique à ce que `## Where` nomme et écrit *applied* dans son rapport ou dans `## Decision applied` / `## What governed the code, besides the sheet` | La commande renomme en `-NN` sur cette ligne, et pas sur une autre ; `/3a_genre`, `/3b_nature`, `/8_code` retestent avant de renommer | `PROCESS_AMONT.md`, `PROCESS_AVAL.md`, `PROCESS_ENTREES.md` |
| Un `questions-<agent>-NN.md` à la racine, `Answer:` vides (→ `### Fichier de questions — divergence`) | Le Product Owner répond en français, à la main | `/1_lexique` (invocation 3 puis 4 sur le fichier répondu), `/2_structure` (invocation 2 l'intègre et le classe), `/4_grille` et `/2_structure` (test `^Answer:\s*$` sans `Défaut:`) | `PROCESS_AMONT.md` |
| `questions-architecte-NN.md` à la racine, laissé par toute commande | `/conventions`, invocation 2 ; classé après | `/conventions` teste `Answer:` vide et `^### Q` ; toute autre commande lit la racine comme s'il n'y était pas | `PROCESS_AMONT.md` |
| `convertisseur/technique-<nature>.md`, `questions/convertisseur/questions-convertisseur-NN.md` répondus | `/6_convertit` les nomme à la nature ; le Convertisseur les lit | `^Answer:\s*$` absent, `### Q` présent ; classé dans `convertisseur/closed/` après application | `PROCESS_AMONT.md` |
| `questions/qualifieur/` et `questions/classeur/`, le plus haut avec `### Q` | `/3a_genre`, `/3b_nature` le nomment à leur agent (troisième déclencheur) | Le grep `^### Q` sur le plus haut classé ; le fichier vide suivant de l'agent fait taire le déclencheur | `PROCESS_AMONT.md` |
| `questions-fusionneur-NN.md` répondu | `/fusion` (lignes 7, 9), `/fusion_applique` ; le Fusionneur relit ses propres fichiers | `Answer:` vide → arrêt ; `### Q` n'arrête pas `/fusion_compare` | `PROCESS_AMONT.md` |
| `stop.md` créé dans le dépôt principal (→ `### stop.md`) | `/8_code`, mouvement 6, fin de lot | Présence dans le dépôt principal, jamais dans le worktree | `PROCESS_AVAL.md` |
| Les lignes `.gitignore` de `stop.md` et `stop1.md` | `socle.py` les ajoute si absentes | Jamais commités | `PROCESS_ENTREES.md` |
| Le commit `chore: scaffolding for the chain` de `socle.py` — en place dans le dépôt principal, sans worktree, poussé par le cockpit quand l'application a un dépôt distant (→ `### Commit sans worktree`) | Le `HEAD` local depuis lequel chaque commande qui invoque crée son worktree (→ `### Git, avant l'invocation`, pas 2) | `git worktree add .claude/worktrees/<name> HEAD`, jamais une base choisie par l'outillage ; un push qui échoue est rapporté, ni retenté ni contourné, et le commit tient localement | `PROCESS_ENTREES.md` |
| Le `model` du frontmatter (→ `### Frontmatter d'un agent`) | Le `model=` de chaque `Agent()` | Concorde avec le frontmatter ; l'exception `opus` du troisième realisateur | tous |
| `Bash` absent du frontmatter | Le pas 1 des cinq pas Git : la commande commite ce que l'agent a écrit | `git status` avant le `remove` ; jamais de force | tous |
| Un worktree créé depuis `HEAD` par la commande (→ `### Git, avant l'invocation`) | Chaque agent écrit en chemins relatifs, dans ce worktree | Un chemin absolu échoue | tous |
| Le commit `<working folder>/<lot>: …` du concepteur, du testeur, du realisateur (→ `### Commit d'un lot`) | `/8_code` en dérive la liste du Relecteur et les reverts ; `HEAD` avant/après pour la tentative vide | Le préfixe exact ; les requêtes `architecte/` hors du commit ; `trap:` pour le piège | `PROCESS_AVAL.md` |
| `Called by the orchestration.` / `Called by the Arbitre.` (→ `### Valeurs de « Called by » — qui a invoqué l'Architecte`) | L'Architecte, invocation 3 | Jamais déduit ; fichier de blocage ou refus en verdict selon la ligne | `PROCESS_AMONT.md`, `PROCESS_AVAL.md` |
| Une requête `architecte/*.md` à `## Verdict` vide (→ `### Requête de conventions — divergence`) | `/7_lots` (le découpage tenu), `/8_code` (fin de lot), l'Arbitre (aussitôt) invoquent l'Architecte | Un bloc sans titre `## Verdict` compte pour vide ; le verdict sous le `# Request N` ; le texte de la règle dedans | `PROCESS_AVAL.md`, `PROCESS_AMONT.md` |
| `code/redecoupage.md` écrit par l'Arbitre (→ `### Fichiers du découpage`) | `/8_code` compte, revert, ferme le worktree, lance `/7_lots` ; le Cadreur bloc C | Présence du fichier, `^## Décision du Product Owner` pour le compte | `PROCESS_AVAL.md` |
| `## Redécoupage: archivable` dans `code/sequence.md` | `/7_lots` renomme `code/redecoupage.md` et retire la ligne | La ligne lue au fichier, pas au rapport | `PROCESS_AVAL.md` |
| `desc-produit.md` fermé, sans marqueur, `questions-sondeur-NN.md` et `questions-existant-NN.md` vides (→ `### Marqueurs NEW et MODIFIED`) | `/5_reclasse` écrit `par-genre/` et `desc-par-nature.md` | Les greps `^### .*NEW`, `^### .*MODIFIED`, `^### Q` sur les deux plus hauts | `PROCESS_AMONT.md` |
| `spec-technique.md` avec `# Preamble`, sans `<<ASSUMED` ni `[B`, `tracabilite.md` à côté (→ `### Fichiers de la conversion`, `### Marques <<ASSUMED et [B`) | `/conventions` (l'Architecte dérive) puis `/7_lots` (le Cadreur greppe et coupe) | Le grep du Cadreur au mouvement 1 ; `^### §` par `/7_lots` — zéro entrée arrête sans découpage | `PROCESS_AMONT.md` → `PROCESS_AVAL.md` |
| `tracabilite.md` (→ `### tracabilite.md`) | L'Architecte (invocations 1 et 4, mouvement 2) ; `/9_controle` (phase 1) | Première colonne contre les titres de `desc-produit.md` ; un tiret ne lève `inconsistency` que sur `comportement` et `référence` | `PROCESS_AMONT.md`, `PROCESS_AVAL.md` |
| `code/decisions-produit.md` par cycle (→ `### Identifiants`, `B<n>`) | Le Rédacteur, invocation 3, nommé par `/fusion` dans l'ordre des cycles | Une décision par ligne, l'identifiant d'abord ou un tiret, en français | `PROCESS_AVAL.md` → `PROCESS_AMONT.md` |
| `(B<n>)` en fin de première ligne d'un manque de `bug-list.md` | Le Diagnostiqueur le copie dans le titre d'entrée, le Cadreur dans l'`Anchor:`, `/9_controle` marque `carried` (→ `### Marque carried`) | La forme exacte, entre parenthèses, en fin de première ligne | `PROCESS_ENTREES.md` → `PROCESS_AVAL.md` |
| `docs/CURRENT_TECHNICAL_STATE.md` créé par `socle.py` (→ `### Lecture de l'état technique`) | Le Réalisateur et l'Arbitre y écrivent, le Détailleur, le Réalisateur et le Diagnostiqueur y lisent deux sections puis des greps | La compétence `technical-state-format` chargée avant d'écrire | `PROCESS_ENTREES.md`, `PROCESS_AVAL.md` |
| `docs/TECHNICAL_CONVENTIONS.md` écrit par l'Architecte (→ `### Lecture des conventions — divergence`, `### permanente / spécifique`) | Tout l'aval le lit, entier ou par `permanente` et `R<n>` ; `/audit_conventions` | Le mot `permanente` sur la ligne ; sans marqueur, tout lire | `PROCESS_AMONT.md` → `PROCESS_AVAL.md` |

## Boucles

### Blocage → décision → relance

Ouverte par: un agent qui écrit un `blocked_<agent>.md` au nom non numéroté (→ `### Fichier de blocage — divergence`), relayé et arrêté par la commande
Fermée par: l'agent rapporte avoir appliqué le `## Decision` rempli, et la commande fait `git mv` en `-NN` — le fichier n'existe plus au nom non numéroté (→ `### Renommage -NN — divergence`)
Plafond: aucun — chaque tour est une décision que le Product Owner écrit ; l'Arbitre borne sa seule attente à 20 minutes ; le Cadreur seul a un plafond, une décision par tour au-delà du troisième (`PROCESS_AVAL.md`)
Au plafond: sans objet ; un bloc qui rebloque sur le même point s'ajoute en `## Blocking N` suivant ou en jeu de titres suivant, et la répétition est visible au Product Owner
Traverse: les dix-huit agents qui bloquent, l'Arbitre, l'Architecte ; toutes les commandes qui invoquent — `PROCESS_ENTREES.md`, `PROCESS_AMONT.md`, `PROCESS_AVAL.md`

### Question → réponse → intégration

Ouverte par: un agent qui écrit un `questions-<agent>-NN.md` tenant au moins un `### Q` (→ `### Fichier de questions — divergence`)
Fermée par: le fichier répondu passe par `/1_lexique` (invocations 3, 4) puis `/2_structure` (invocation 2) et est classé sous `questions/<agent>/` ; ou, pour un `questions-architecte-NN.md`, par `/conventions` (invocation 2) ; pour un `questions-fusionneur-NN.md`, par `/fusion_applique` ou `/fusion` (invocation 2, 3) ; pour un `technique-<nature>.md`, par `/6_convertit` (la boucle courte, sans `/1_lexique`) — le test : plus aucun fichier tenant un `### Q` à la racine, et le plus haut fichier de l'agent vide (`/4_grille`, `/5_reclasse`, `/1_lexique`, `/2_structure`, `/conventions`)
Plafond: aucun — chaque tour attend le Product Owner ; un fichier vide ferme
Au plafond: sans objet
Traverse: lexicographe, redacteur, qualifieur, classeur, sondeur, assembleur, convertisseur, fusionneur, architecte ; `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, `/6_convertit`, `/conventions`, `/fusion`, `/fusion_compare`, `/fusion_applique` — `PROCESS_AMONT.md`

### Requête → verdict → règle

Ouverte par: un agent qui écrit une requête sous `architecte/` à `## Verdict` vide (→ `### Requête de conventions — divergence`)
Fermée par: l'Architecte (invocation 3) écrit le `## Verdict` sous la requête, et la règle éventuelle dans `docs/TECHNICAL_CONVENTIONS.md` avec sa ligne de `couverture.md` ; le test : aucun bloc de requête à `## Verdict` vide ou absent dans `architecte/` (glob par `/batir`, `/7_lots`, `/8_code`)
Plafond: une requête par invocation pour l'Arbitre, jamais deux fois sous une autre formulation ; trois invocations de l'Architecte par run pour `/batir` ; aucun pour les autres
Au plafond: l'Arbitre attend le Product Owner ou tranche depuis ce que le refus nomme
Traverse: batisseur, cadreur, detailleur, concepteur, realisateur, arbitre, architecte ; `/batir`, `/7_lots`, `/8_code`, `/conventions` (invocation 3 par le second argument), `/audit_conventions` — `PROCESS_AVAL.md`, `PROCESS_AMONT.md`

## Inventaire

Agents décrits en entier : aucun.
Agents portés en entrée courte : aucun.
Commandes décrites : aucune.

Protocoles tenus ici, un par ligne :
- Frontmatter d'un agent
- Frontmatter d'une commande
- Invocation d'un agent
- Numéros d'invocation
- Appel d'agent à agent
- Chemins relatifs
- Dossier de travail
- Fichier de blocage — divergence
- Emplacement des fichiers de blocage
- Reprise sur décision — divergence
- Renommage -NN — divergence
- Trace de la décision appliquée — divergence
- Fichier de questions — divergence
- Numéro du fichier de questions — divergence
- Test d'une question sans réponse
- Classement des fichiers de questions
- Forme d'un relais
- Ligne Next:
- stop.md
- Git, avant l'invocation
- Git, après le rapport — les cinq pas
- Commit sans worktree
- Bash des agents — divergence
- Commit d'un lot
- Ce que l'orchestrateur lit
- Lecture d'un bloc par grep
- Grep du code avec chemin
- Lecture de l'état technique
- Lecture des conventions — divergence
- Lecture du global par l'index
- Lecture des données externes
- Disposition du dossier de feature
- En-tête d'un bloc produit
- Marqueurs NEW et MODIFIED
- Marque Clarification needed
- lexique.md
- Fichiers du cadrage
- Fichiers de la conversion
- tracabilite.md
- Ligne Consumes:
- Marques <<ASSUMED et [B
- Requête de conventions — divergence
- Fichiers du découpage
- Fichiers d'un lot
- Fichiers déclarés d'un lot
- Identifiants
- Marque carried

Ensembles fermés tenus ici, un par ligne :
- Les six genres — le genre d'un bloc
- Les huit natures — la nature d'un bloc
- NEW / MODIFIED — ce qui a bougé depuis le dernier tour
- États de « ## Decision » — ce qu'un fichier de blocage attend
- Valeurs de « ## Invocation » — qui a écrit ce fichier de blocage
- Valeurs de « Called by » — qui a invoqué l'Architecte
- created / modified — la marque d'un symbole
- permanente / spécifique — ce qui déclenche une règle
- Les quatre statuts d'un verdict — l'issue d'une revue
- Les trois causes d'un FAIL — d'où vient la faute
- Les onze types de défaut — ce que le Vérificateur constate
- Les cinq Kind: — la sorte d'une question de l'Architecte
- Les trois formes de « Entries with no lot » — pourquoi une entrée n'a pas de lot
- Les quatre termes du Cadreur — l'issue sur son fichier de blocage
- Les verbes du plan de fusion — ce qu'une phrase devient
- Plafonds par couche — ce qu'un lot et un bloc peuvent porter
- Ordres de lecture des sondeurs — ce qui distingue les trois angles
- Found / Missing / Doubtful — le sort d'une intention
- Rouge / vert par la déclaration seule — l'état d'un test neuf
