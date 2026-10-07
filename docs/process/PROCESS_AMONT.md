# PROCESS_AMONT.md — de l'idée à `spec-technique.md`, plus `/conventions` et la fusion

> Document de pilotage, en français. Il décrit les douze commandes qui
> mènent d'`idees.md` au document technique, dérivent les conventions et
> fusionnent le fichier produit dans le global — `/1_lexique`,
> `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`,
> `/5_reclasse`, `/6_convertit`, `/conventions`, `/fusion`,
> `/fusion_compare`, `/fusion_applique` — et les dix agents qu'elles
> invoquent : lexicographe, redacteur, decoupeur, qualifieur, classeur,
> sondeur, assembleur, convertisseur, architecte, fusionneur. Tout
> protocole partagé est défini dans `PROCESS_MECANISMES.md` et pointé par
> `→ MECANISMES §<nom>` ; il n'est jamais redit ici. Les mécanismes à un
> seul utilisateur que `MECANISMES` renvoie à ce document sont décrits
> dans le bloc de leur agent ou de leur commande.

## Comment lire une entrée

Une commande : `Prend` · `Rend` · **Étapes** (dans l'ordre) · **Git** ·
**La Product Owner intervient** · **Décisions**. Un agent : neuf champs
(`Modèle` / `effort` / `outils` · `Invoquée par` · `Lit` · `Écrit` ·
`Valeurs` · **Gestes** · **Branches** · **Échange** · **Bloque**) plus
**Décisions** — un bloc par invocation quand deux invocations ne lisent
ou n'écrivent pas la même chose. Un champ vide est écrit `aucun`, jamais
omis. `outils` reprend la ligne `tools:` du frontmatter mot pour mot ;
`effort aucun` quand le frontmatter n'en porte pas.

Une décision : `<la décision> · écartée : <l'alternative> · raison : <…> ·
<statut>`. `raison :` n'est remplie que depuis une source ouverte —
l'agent, la commande, `docs/verification4/`, `docs/verification3/`,
`docs/verification2/` — sinon `raison : à retrouver`. Le statut est
`éprouvée` quand un fichier dit qu'un run l'a exercée, `non éprouvée`
quand la campagne dit qu'elle a été tranchée et jamais exécutée (toute
décision de `docs/verification4/plan.md`, appliquée le 2026-09-21),
`inconnu` sinon.

Les quatre grilles — `.claude/grids/GRILLE_CADRAGE_PRODUIT_V2.md`,
`GRILLE_EXISTANT.md`, `GRILLE_FERMETURE_TECHNIQUE.md`,
`GRILLE_CONVENTIONS.md` — sont des entrées, pas des agents : le bloc de
l'agent qui en lit une dit à quoi elle sert et comment elle se lit, jamais
ses questions.

## Le parcours nominal

| Ordre | Commande | Agent, invocation | Ce qu'elle laisse |
|---|---|---|---|
| 1 | `/1_lexique`, en boucle | lexicographe 1 puis 2, jusqu'à un `questions-lexicographe-NN.md` vide | `lexique.md`, `idees.md` réglé |
| 2 | `/2_structure` | redacteur 1 | `desc-produit.md`, `questions-redacteur-NN.md` |
| 3 | `/3_decoupe` | decoupeur | les blocs à un déclencheur |
| 4 | `/3a_genre` | qualifieur | la ligne `Genre:` de chaque bloc, `questions-qualifieur-NN.md` |
| 5 | `/3b_nature` | classeur | la ligne `Nature:` de chaque `comportement`, `questions-classeur-NN.md` |
| 6 | `/4_grille`, en boucle | sondeur 1 (trois à la fois) et 2, puis assembleur ; au second temps, sondeur 3 seul | `questions-sondeur-NN.md`, puis `questions-existant-NN.md` — un vide de chaque ferme |
| — | chaque tour de réponses | `/1_lexique` (lexicographe 3, 4) → `/2_structure` (redacteur 2) → `/3_decoupe` → `/3a_genre` → `/3b_nature` → `/4_grille` | |
| 7 | `/5_reclasse` | aucun | `par-genre/*.md`, `desc-par-nature.md` |
| 8 | `/6_convertit`, en boucle | convertisseur 1 (une par nature, à la fois) puis 2 | `spec-technique.md`, `tracabilite.md`, `questions-convertisseur-NN.md` ; une question technique revient en boucle courte, une question produit repart par `/1_lexique` |
| 9 | `/conventions`, à la main | architecte 1 (ou 4, ou 2, ou 3) | `docs/TECHNICAL_CONVENTIONS.md`, `couverture.md`, `questions-architecte-NN.md` |
| — | `/7_lots`, `/8_code`, `/9_controle` | → `PROCESS_AVAL.md` | `code/decisions-produit.md` par cycle |
| 10 | `/fusion`, à la main, une fois par feature | redacteur 3, puis fusionneur 3 sur les `bugfix-*/`, puis fusionneur 1 et 2 par sa table | `desc-produit-fusion.md`, `plan-fusion.md`, `docs/PRODUIT_GLOBAL.md`, `rapport-fusion.md` |
| 10 bis | `/fusion_compare` puis `/fusion_applique` | fusionneur 1 ; fusionneur 2 | le même plan, le même global, le même rapport — `/6_convertit` les nomme comme branche possible |

---

# Les commandes

## /1_lexique

**Prend** : `<feature folder name>`, obligatoire ; l'état de la racine de
`docs/features/<name>/` (un `ls`) ; `idees.md` (invocations 1 et 2) ;
`lexique.md` quand il existe ; `blocked_lexicographe.md` quand il existe ;
un grep `^### Q` sur chaque `questions-*.md` de la racine et un grep
`^Answer:\s*$` sans `Défaut:` dessus ; l'existence de `desc-produit.md`.

**Rend** : `lexique.md` créé ou mis à jour ; un nouveau
`questions-lexicographe-NN.md` (toujours à 1 et 3, seulement si une
réponse laisse le choix ouvert à 2 et 4) ; `idees.md` réglé (2) ; le
fichier répondu d'un autre agent, ses termes retirés remplacés (3, 4) ;
`blocked_lexicographe.md` renommé `-NN` ; le fichier appliqué classé sous
`questions/lexicographe/` ; le rapport de l'agent, le compte des lignes
sous `## Non tranché`, le compte des `^### Q`, la table *What to run
next*.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. Tester `blocked_lexicographe.md` (→ MECANISMES §États de « ## Decision » — ce qu'un fichier de blocage attend) : absent → continuer ; `## Decision` vide → arrêt ; rempli → le nommer dans le prompt. Ce titre seul est lu.
3. Choisir l'invocation sur les noms des fichiers de la racine, jamais sur leur numéro, `questions-architecte-*.md` compté dans aucune ligne et laissé en place :

   | La racine tient | Invocation |
   |---|---|
   | aucun fichier de questions | `1 — Sweeping` |
   | `questions-lexicographe` seul, sans `### Q` | rien : la boucle est finie, dire `/2_structure` |
   | `questions-lexicographe` seul | `2 — Settling` |
   | le fichier d'un autre agent seul, sans `### Q` | rien : rien à surveiller, dire `/2_structure` |
   | le fichier d'un autre agent seul | `3 — Watching` |
   | le fichier d'un autre agent et `questions-lexicographe` sans `### Q` | rien : 3 n'a rien demandé, dire `/2_structure` |
   | le fichier d'un autre agent et `questions-lexicographe` | `4 — Correcting` |
   | deux fichiers d'autres agents | arrêt : un classement a échoué, nommer les fichiers |

   Le fichier de l'autre agent est *the answered file*, quel que soit son préfixe.
4. Une `Answer:` vide sans `Défaut:` dans le même entrée → arrêt, les questions nommées (→ MECANISMES §Test d'une question sans réponse).
5. `desc-produit.md` présent arrête 1 et 2 et nomme `/3_decoupe` ; il n'arrête ni 3 ni 4.
6. Ne rien classer avant d'avoir choisi ; tout autre fichier à la racine → arrêt, sans le déplacer.
7. → MECANISMES §Git, avant l'invocation, message `chore: answers`.
8. Invoquer (→ MECANISMES §Invocation d'un agent) : `subagent_type="lexicographe"`, `model="opus"`, `description="Sweep <name>'s vocabulary"` ; le prompt porte `The idea file: docs/features/<name>/idees.md.` à 1 et 2 seulement, `The lexicon: docs/features/<name>/lexique.md.` quand il existe, `Invocation <N — nom>.`, `The questions file to apply: docs/features/<name>/questions-lexicographe-NN.md.` à 2 et 4, `The answered file: docs/features/<name>/questions-<agent>-NN.md.` à 3 et 4, `<Plus: blocked_lexicographe.md, its decision is filled.>`, `Write to docs/features/<name>/.`.
9. Après le rapport, re-grepper le `## Decision` de `blocked_lexicographe.md` : encore rempli → celui qu'on a nommé, appliqué, renommé `blocked_lexicographe-NN.md` (→ MECANISMES §Renommage -NN — divergence) ; vide de nouveau → un bloc neuf, relayé, rien classé.
10. Après 2 ou 4, `git mv` du `questions-lexicographe-NN.md` appliqué vers `questions/lexicographe/`, dans le worktree ; un nouveau fichier écrit par l'agent reste à la racine.
11. Après chaque invocation : `lexique.md` existe, et les lignes sous `## Non tranché` sont comptées (cette section seule). Après 1 ou 3 : compter `^### Q` dans le nouveau fichier. Après 2 ou 4 : dire s'il en a écrit un, et combien d'entrées. Un fichier manquant arrête la commande.
12. → MECANISMES §Git, après le rapport — les cinq pas.
13. Relayer (→ MECANISMES §Forme d'un relais) : la table à neuf lignes — fichier de blocage → remplir puis `/1_lexique` ; 1 a demandé → répondre puis `/1_lexique` ; 1 n'a rien demandé → `/2_structure` ; 2 a écrit un fichier → répondre puis `/1_lexique` ; 2 n'en a pas écrit → `/1_lexique` ; 3 a demandé → répondre puis `/1_lexique` ; 3 n'a rien demandé → `/2_structure` ; 4 a écrit → répondre puis `/1_lexique` ; 4 n'a pas écrit → `/2_structure`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` avant ; worktree depuis `HEAD` ; les cinq pas après. Les lignes *Invoke nothing* de l'étape 3 ne disent rien d'un commit ni d'un push — cette commande n'est pas dans → MECANISMES §Commit sans worktree.

**La Product Owner intervient** : elle écrit `idees.md` ; elle remplit les `Answer:` de `questions-lexicographe-NN.md` en français ; elle remplit le `## Decision` de `blocked_lexicographe.md` ; elle relance la commande selon la table de l'étape 13.

**Décisions**

- Le vocabulaire est réglé avant que le fichier produit existe (1 et 2 arrêtés par `desc-produit.md`) · écartée : régler un terme après coup · raison : un terme changé ensuite laisserait soixante blocs avec l'ancien (`/1_lexique`, *Which invocation*) · inconnu.
- 3 et 4 tournent à chaque tour de grille et de conversion, avant `/2_structure` · écartée : intégrer les réponses sans balayage · raison : les réponses portent des mots que personne n'a balayés, et un synonyme neuf n'est attrapé par personne (`lexicographe.md`, invocation 3) · inconnu.
- Après 2, relancer 1 · écartée : passer à `/2_structure` · raison : un terme réglé peut découvrir une paire que le premier balayage ne voyait pas (`/1_lexique`) · inconnu.
- 4 ne tourne que si 3 a demandé quelque chose · écartée : 4 systématique · raison : 3 a déjà remplacé ce que le lexique retire (`lexicographe.md`) ; une relance après « 3 asked nothing » coûtait un appel opus et un cycle git (`docs/verification2/lexicographe.md` F11) · inconnu.
- La commande lit un grep `### Q` du fichier de questions pour choisir, et ne classe rien avant · écartée : classer d'abord · raison : classer avant déciderait sur le fichier même qui dit l'invocation (`/1_lexique`, *Git, before invoking*) · inconnu.
- Sur l'arrêt « `desc-produit.md` présent », nommer `/3_decoupe` · écartée : nommer `/2_structure` · raison : `/2_structure` s'arrête sur le même état et les deux commandes se renvoyaient l'une à l'autre (`docs/verification3/plan.md` entrée 53) · inconnu.
- Une relance par erreur après « 4 wrote none » relance 3, sans marqueur d'état · écartée : un marqueur laissé par 4 · raison : un run par erreur coûte une invocation et ne casse rien (`docs/verification3/plan.md` entrée 54, item H, Option 1) · inconnu.
- Re-grep du `## Decision` après le rapport, avant de renommer · écartée : renommer sur la seule ligne *applied* · raison : un run repris peut rebloquer sous le même nom (`/1_lexique`, *Once it has reported*) · inconnu.

## /2_structure

**Prend** : `<feature folder name>` ; un `ls` de la racine avant et après ; un grep `^### Q` sur un `questions-lexicographe-NN.md` de la racine ; un grep `^### Q` sur le plus haut `questions-lexicographe-NN.md`, racine ou `questions/lexicographe/` ; les titres `## Invocation` et `## Decision` de `blocked_redacteur.md` ; chaque `## Decision` d'un `blocked_decoupeur.md`, `blocked_qualifieur.md` ou `blocked_classeur.md` (`grep -A2 '^## Decision$'`) ; le grep `^Answer:\s*$` sans `Défaut:` du fichier à intégrer ; les greps `^### .*NEW` et `^### .*MODIFIED` de `desc-produit.md` avant et après ; l'existence de `code/decoupage.md` ; un grep `Clarification needed`.

**Rend** : `desc-produit.md` créé (1) ou modifié (2) ; `questions-redacteur-NN.md` ; les lignes `en anglais :` de `lexique.md` ; les fichiers de blocage renommés `-NN` ; le fichier intégré classé ; la suppression de `par-genre/`, `desc-par-nature.md`, `spec-technique.md`, `couverture.md` selon la table de l'étape 9 ; ou le refus, qui ne rend rien.

**Étapes**

1. Un `questions-lexicographe-NN.md` à la racine : `### Q` → arrêt, dire `/1_lexique`. La racine seule est gardée, jamais le dossier classé. Puis `blocked_redacteur.md` : absent → continuer ; `## Invocation` 3 → arrêt, il est à `/fusion` ; 1 ou 2 et `## Decision` vide → arrêt ; 1 ou 2 et rempli → le nommer (→ MECANISMES §Valeurs de « ## Invocation » — qui a écrit ce fichier de blocage). Ces deux tests passent avant tout geste sur le dépôt.
2. Le fichier du lexicographe sans `### Q` → `git mv` vers `questions/lexicographe/` (→ MECANISMES §Classement des fichiers de questions). C'est le premier geste qui change le dépôt : les étapes 3 à 5 lisent la racine après ce classement, elles restent après lui, et aucune ligne ne défait le `git mv` quand elles s'arrêtent.
3. Choisir l'invocation, première ligne qui correspond, `questions-architecte-*.md` compté dans aucune :

   | La racine tient | Invocation | Ce qu'on nomme |
   |---|---|---|
   | un fichier de questions avec `### Q`, tout préfixe | `2 — Integrating` | ce fichier |
   | plus d'un fichier de questions | arrêt : un classement a échoué | — |
   | un `blocked_decoupeur.md`, `blocked_qualifieur.md` ou `blocked_classeur.md`, chaque `## Decision` rempli | `2 — Integrating` | ce fichier |
   | l'un des trois avec un `## Decision` vide | arrêt, le `## Blocking N` qui attend nommé | — |
   | un fichier de questions sans `### Q` | rien : dire `/3_decoupe` | — |
   | aucun fichier de questions, pas de `desc-produit.md` | `1 — Structuring` | `idees.md` |
   | aucun fichier de questions, un `desc-produit.md` | arrêt ; grep `Clarification needed` d'abord : un hit → le drapeau tient sans fichier pour le lever, jamais `/3_decoupe` ; aucun → dire `/3_decoupe` | — |

4. Invocation 1 exige un vocabulaire réglé : le plus haut `questions-lexicographe-NN.md`, racine ou classé, sans `### Q` ; aucun nulle part, ou des entrées → arrêt, dire `/1_lexique`.
5. Une `Answer:` vide sans `Défaut:` → arrêt (→ MECANISMES §Test d'une question sans réponse).
6. → MECANISMES §Git, avant l'invocation, `chore: answers` — après tous les tests des étapes 1 à 5.
7. Invoquer : `subagent_type="redacteur"`, `model="sonnet"`, `description="Structure <name>"` ; prompt `Feature folder: docs/features/<name>/.`, `Invocation <1 — Structuring | 2 — Integrating>.`, `Read: <idees.md | questions-<agent>-NN.md | blocked_<decoupeur|qualifieur|classeur>.md>.`, `<Plus: blocked_redacteur.md, its decision is filled.>`.
8. Refaire les deux greps de marqueurs : les titres que le second ajoute sont ceux du run.
9. Tester `code/decoupage.md` :

   | `code/decoupage.md` | Le run | Ce qu'on fait |
   |---|---|---|
   | existe | a créé un `NEW` | le refus : rien commité, rien fusionné, `git worktree remove --force`, le dossier est comme le run l'a trouvé ; dire quel bloc la réponse a créé et que le fichier est à placer par la Product Owner ; rien d'autre ne tourne |
   | existe | a changé, sans créer | rien supprimé ; dire qu'un changement du produit appartient à un nouveau cycle |
   | absent | a créé un `NEW` | `rm -rf par-genre/ desc-par-nature.md spec-technique.md couverture.md` |
   | absent | a changé, sans créer | `couverture.md` seul |
   | l'un ou l'autre | ni l'un ni l'autre | rien |

10. Renommer `blocked_redacteur.md` en `-NN` ; renommer celui des trois fichiers de blocage qu'on a nommé, `blocked_<agent>-NN.md`. Un fichier de blocage que le run vient d'écrire : rien n'est classé.
11. À l'invocation 2, `git mv` du fichier intégré vers `questions/<agent>/` ; sur la ligne du fichier de blocage, le `questions-<agent>-NN.md` vide qui l'accompagnait est classé de même. Le nouveau fichier du Rédacteur reste seul à la racine.
12. Vérifier que `questions-redacteur-NN.md` a été écrit ; manquant → arrêt.
13. → MECANISMES §Git, après le rapport — les cinq pas — tout arrêt fusionne d'abord, sauf le refus.
14. Relayer, première ligne : refus → rien ne tourne ; fichier de blocage → remplir, `/2_structure` ; questions → répondre puis `/1_lexique` ; fichier vide → `/3_decoupe`. Un fichier de blocage qui attendait à la racine pendant l'intégration est dit, quelle que soit la ligne. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; cinq pas ; le refus seul ne commite rien et retire le worktree de force.

**La Product Owner intervient** : elle répond aux questions en français ; elle remplit les `## Decision` ; sur un refus, elle place elle-même la réponse (un nouveau cycle) ; sur un drapeau sans fichier, elle retrouve le fichier.

**Décisions**

- Les lignes « fichier de questions » avant les lignes « fichier de blocage » · écartée : le blocage d'abord · raison : le Rédacteur appliquant la décision écrit son propre fichier de questions à côté du fichier répondu, et le run suivant s'arrête sur deux (`/2_structure` ; `docs/verification3/plan.md` entrée 5+6) · inconnu.
- La ligne « fichier vide → rien » sous les lignes de blocage · écartée : au-dessus · raison : une décision remplie à côté d'un fichier vide bouclerait sur « rien à intégrer » (`docs/verification3/plan.md` entrée 5+6) · inconnu.
- Le fichier vide à côté du fichier de blocage est classé avec le run · écartée : le laisser à la racine · raison : deux fichiers à la racine arrêtent le run suivant sur un classement raté (`docs/verification4/plan.md` entrée 2) · non éprouvée.
- Le refus d'intégrer un bloc `NEW` une fois le découpage fait · écartée : un cycle `bugfix-NN` ; un mode « ajout » du Convertisseur · raison : un bloc `NEW` après le découpage n'atteint aucun lot et le document n'est pas réécrit sous les lots (`docs/verification3/plan.md` entrée 11, item A, Option 3) · inconnu.
- Quatre dérivés supprimés sur `NEW`, `couverture.md` seul sur `MODIFIED` · écartée : ne rien supprimer · raison : un `spec-technique.md` sans le bloc serait découpé et le trou remonterait au Contrôleur ; un `couverture.md` survivant dit à `/conventions` que la feature a été parcourue ; un bloc changé est une section reconvertie, donc un document rebâti (`/2_structure`, *Why* ; `docs/verification3/plan.md` entrée 50) · inconnu.
- Le refus ne commite ni ne fusionne, `git worktree remove --force` · écartée : les cinq pas · raison : rien à transmettre, le dossier de feature est tel que le run l'a trouvé (`/2_structure`, *The refusal*) · inconnu.
- Invocation 1 une seule fois · écartée : retranscrire l'idée · raison : une seconde invocation 1 renumérote ou double chaque bloc, et chaque question classée pointe alors sur le mauvais (`/2_structure`) · inconnu.
- La garde `### Q` sur le fichier lexicographe de la racine seul, le test de vocabulaire sur le plus haut où qu'il soit · écartée : une seule lecture · raison : un fichier classé tient les entrées que `/1_lexique` a appliquées, et une garde le lisant s'arrêterait sur un vocabulaire réglé après l'invocation 4 (`docs/verification3/plan.md` entrée 19) · inconnu.
- Le fichier nommé, toujours · écartée : l'agent cherche · raison : l'agent ouvre ce fichier et aucun autre (`/2_structure`) · inconnu.

## /3_decoupe

**Prend** : `<feature folder name>` ; le `## Decision` de `blocked_decoupeur.md` ; un grep `Clarification needed` ; un grep `^### Q` sur chaque `questions-*.md` de la racine ; l'existence de `desc-produit.md` (un glob) ; l'existence d'un `questions-sondeur-*.md` où que ce soit ; les greps `^### .*NEW` et `^### .*MODIFIED` ; un grep `^### B` compté avant et après ; la liste des blocs que l'agent rapporte avoir regardés.

**Rend** : `desc-produit.md` avec ses blocs scindés ; `blocked_decoupeur.md`, laissé au nom non numéroté ; les fichiers de questions de la racine classés ; le compte de blocs avant et après ; la table *What to run next*.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. `blocked_decoupeur.md` : absent → continuer ; `## Decision` vide → arrêt ; rempli → arrêt aussi, `/2_structure` doit tourner d'abord — le decoupeur ne voit jamais ce fichier, le prompt ne le nomme pas.
3. `desc-produit.md` absent → arrêt : `/2_structure` n'a pas tourné.
4. Grep `Clarification needed` dans `desc-produit.md` : un hit → arrêt, les blocs nommés, `/2_structure` d'abord (→ MECANISMES §Marque Clarification needed).
5. La garde `### Q` puis le classement de chaque `questions-*.md` de la racine, `questions-architecte-*.md` excepté (→ MECANISMES §Classement des fichiers de questions). Tous les tests sont passés : le classement est le premier geste qui change le dépôt.
6. Quels blocs : aucun `questions-sondeur-*.md` nulle part → *every block*, ces mots dans le prompt ; sinon l'union des greps `^### .*NEW` et `^### .*MODIFIED`, jamais le fichier de questions. Aucun → invoquer personne, commiter ce que le classement a déplacé et pousser, sans worktree (→ MECANISMES §Commit sans worktree).
7. → MECANISMES §Git, avant l'invocation, `chore: answers`.
8. Invoquer : `subagent_type="decoupeur"`, `model="opus"`, `description="Split <name>"` ; prompt `The product file: docs/features/<name>/desc-produit.md.`, `Look at these blocks: <B7, B28 — ou : every block>.`
9. Comparer la liste des blocs que l'agent dit avoir regardés avec la liste nommée. Liste courte sans fichier de blocage → réinvoquer sur les blocs non atteints, dans le worktree, deux fois au plus. Liste courte avec `blocked_decoupeur.md` → pas de réinvocation, les blocs gardent leurs marqueurs.
10. Grep `^### B` et compter : avant, et après la dernière invocation. Un compte égal est normal.
11. → MECANISMES §Git, après le rapport — les cinq pas.
12. Relayer : combien avant, combien après ; une liste encore courte après la seconde invocation, les blocs jamais regardés nommés ; la table — fichier de blocage → remplir puis `/2_structure`, puis `/3_decoupe` ; un bloc dont le seul déclencheur est une suite → son identifiant relayé, l'étape suivante ne change pas, personne ne fusionne ; sinon → `/3a_genre`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; cinq pas ; sans bloc marqué, commit et push en place.

**La Product Owner intervient** : elle remplit le `## Decision` de `blocked_decoupeur.md` ; elle fusionne à la main deux blocs qu'une suite sépare, quand cela la gêne.

**Décisions**

- Tous les blocs tant que la grille n'a pas tourné une fois · écartée : les marqueurs dès le premier tour · raison : le Rédacteur ne retire les marqueurs qu'une fois un tour de grille les a consommés, ils ne disent rien de ce qui a déjà été regardé (`/3_decoupe`, *Which blocks it looks at*) · inconnu.
- Le balayage entier prouvé par la liste rapportée contre la liste nommée · écartée : ouvrir un bloc pour vérifier · raison : la commande ne peut pas ouvrir un bloc ; la liste contre la liste est la seule preuve (`decoupeur.md`, *What you report*) · inconnu.
- La réinvocation dans le worktree, avant les cinq pas, deux fois au plus · écartée : après la fusion · raison : le worktree est fusionné et retiré ; une invocation hors worktree perd l'écriture entière (`docs/verification3/plan.md` entrée 20) · inconnu.
- Un `blocked_decoupeur.md` rempli arrête cette commande et renvoie à `/2_structure` · écartée : le nommer au decoupeur · raison : il bloque sur une phrase à deux déclencheurs, et reformuler est au Rédacteur ; `/2_structure` le renomme après la réécriture (`/3_decoupe`) · inconnu.
- Un bloc dont le seul déclencheur est une suite est relayé, jamais fusionné · écartée : fusionner les deux blocs · raison : aucun agent ne fusionne ; les deux blocs portent un comportement que la grille sonde deux fois, et la Product Owner fusionne à la main (`/3_decoupe`, `decoupeur.md`) · inconnu.
- Jamais lire un bloc pour vérifier la scission · écartée : relire · raison : les sondeurs sondent ce qu'il a produit, c'est ce qui attrape une mauvaise scission (`/3_decoupe`) · inconnu.

## /3a_genre

**Prend** : `<feature folder name>` ; chaque `## Decision` de `blocked_qualifieur.md` ; un grep `Clarification needed` ; un grep `^### Q` par `questions-*.md` de la racine ; le plus haut `questions-qualifieur-NN.md` sous `questions/qualifieur/` et son grep `^### Q` ; `grep -B1 '^Genre:$'` et `grep '^### .*MODIFIED'` ; après le run, `grep -c '^Genre:$'` et `^### Q` dans le fichier écrit.

**Rend** : la ligne `Genre:` de chaque bloc nommé ; `questions-qualifieur-NN.md` ; `blocked_qualifieur.md` renommé ou laissé ; la liste par bloc du genre donné, relayée.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. `blocked_qualifieur.md` : absent → continuer ; un `## Decision` vide → arrêt, le `## Blocking N` nommé ; tous remplis → le nommer.
3. `Clarification needed` → arrêt.
4. La garde `### Q` sur chaque `questions-*.md` de la racine, le sien compris, `questions-architecte-*.md` excepté ; puis le classement.
5. Le numéro dans le prompt : le plus haut `questions-qualifieur-NN.md` sous `questions/qualifieur/` plus un, `01` sans (→ MECANISMES §Numéro du fichier de questions — divergence).
6. Le fichier répondu : le plus haut sous `questions/qualifieur/` qui tient un `### Q` est nommé.
7. Quels blocs : l'union de `grep -B1 '^Genre:$'` (la ligne au-dessus du hit est le titre) et de `grep '^### .*MODIFIED'` ; troisième déclencheur, le fichier répondu de l'étape 6, sans bloc listé. Rien des trois → invoquer personne, commit et push sans worktree.
8. → MECANISMES §Git, avant l'invocation.
9. Invoquer : `subagent_type="qualifieur"`, `model="sonnet"`, `description="Qualify <name>"` ; prompt `The product file: docs/features/<name>/desc-produit.md.`, `<Look at these blocks: B7, B62, B63.>` (absente quand les greps n'ont rien rendu), `Your questions file number: NN.`, `<Plus: your answered questions file: docs/features/<name>/questions/qualifieur/questions-qualifieur-NN.md.>`, `<Plus: blocked_qualifieur.md, every ## Decision is filled.>`.
10. Renommer `blocked_qualifieur.md` en `-NN` seulement si le rapport dit avoir écrit le genre que chaque décision nomme ; le laisser si le rapport dit qu'un bloc *waits on the Rédacteur* ou qu'une décision nomme une valeur hors des six (→ MECANISMES §Reprise sur décision — divergence).
11. Tout arrêt fusionne d'abord. `grep -c '^Genre:$'` : zéro attendu ; sinon dire quels blocs.
12. Vérifier `questions-qualifieur-NN.md` écrit ; compter `^### Q`.
13. → MECANISMES §Git, après le rapport — les cinq pas.
14. Relayer : combien qualifiés, lesquels ont changé de genre, combien de questions, la liste par bloc telle que l'agent l'écrit ; la table — fichier de blocage → remplir puis `/3a_genre`, ou la ligne que la décision suit ; blocage et questions ensemble → répondre d'abord puis `/1_lexique`, la décision ensuite ; chaque `## Decision` nomme une réécriture → `/2_structure`, puis `/3_decoupe`, puis retour ici, jamais `/1_lexique` ; un fichier mixte tourne `/3a_genre` d'abord ; un genre hors liste → rien ne tourne ; compte `^Genre:$` non nul sans fichier de blocage → `/3a_genre` une fois encore, pas jusqu'à ce que ça s'efface ; questions → répondre puis `/1_lexique` ; fichier vide ou rien à qualifier → `/3b_nature`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; cinq pas ; sans invocation, commit et push en place.

**La Product Owner intervient** : elle répond aux questions ; elle remplit chaque `## Decision` ; elle compte elle-même le second run de la ligne « une fois encore » ; elle voit la répétition de la route à deux genres et peut scinder le bloc dans la décision.

**Décisions**

- Le troisième déclencheur, le fichier répondu classé · écartée : les deux greps seuls · raison : une réponse nommant un genre seul ne change aucun bloc — pas de `MODIFIED`, pas de ligne vide — et n'atterrissait nulle part (`docs/verification3/plan.md` entrée 13) · inconnu.
- Le renommage clé sur la ligne du rapport, jamais sur la décision · écartée : lire la décision · raison : le grep dit rempli ou vide, jamais ce qu'une décision dit ; renommé ici, le fichier ne correspond plus à ce que `/2_structure` cherche, et le genre reste vide sans rien pour l'expliquer (`/3a_genre`, *Once it has reported*) · inconnu.
- « Une fois encore, pas jusqu'à ce que ça s'efface » sans compteur sur disque · écartée : un état lu par le run suivant · raison : une ligne vide laissée ni par un bloc ni par une décision est un défaut du run, un troisième run le répéterait ; le compte est à la Product Owner (`docs/verification3/plan.md` entrée 55, item I, Option 1) · inconnu.
- Un fichier mixte (genres et réécritures) tourne `/3a_genre` d'abord, puis `/2_structure`, `/3_decoupe`, retour ; pas de branche `/1_lexique` · écartée : `/2_structure` direct puis `/1_lexique` · raison : les décisions de genre d'un fichier mixte étaient perdues, et la branche `/1_lexique` tombait sur un arrêt — le Lexicographe n'a rien à surveiller sur une réécriture (`docs/verification4/plan.md` entrée 6) · non éprouvée.
- Blocage et questions ensemble : répondre d'abord, décision ensuite · écartée : décision d'abord · raison : les deux finissent chez le Rédacteur ; `/2_structure` prend le fichier répondu et laisse le fichier de blocage pour son run suivant (`docs/verification3/plan.md` entrée 5+6) · inconnu.
- La route à deux genres peut se répéter sur le même bloc · écartée : un plafond · raison : chaque tour est une décision qu'elle écrit, elle voit la répétition, et une décision qui dit comment scinder règle la question (`docs/verification3/plan.md` entrée 56, item J, Option 1) · inconnu.
- Un genre hors liste : rien ne tourne · écartée : le qualifieur l'écrit · raison : les tables doivent le porter d'abord ; une septième valeur passerait ce contrôle et arrêterait `/5_reclasse` trois commandes plus loin (`/3a_genre`, `qualifieur.md`) · inconnu.
- La liste par bloc relayée · écartée : un compte seul · raison : un comportement classé autrement quitte le fichier que la grille lit, et personne en aval ne l'attrape (`/3a_genre`) · inconnu.

## /3b_nature

**Prend** : `<feature folder name>` ; chaque `## Decision` de `blocked_classeur.md` ; un grep `Clarification needed` ; la garde `### Q` ; le plus haut `questions-classeur-NN.md` sous `questions/classeur/` ; `grep -B2 '^Nature:$'` filtré sur `Genre: comportement` ; `grep -B1 '^Nature: '` gardé aux blocs dont le `Genre:` n'est pas `comportement` ; `grep '^### .*MODIFIED'`.

**Rend** : la ligne `Nature:` de chaque comportement nommé, vidée sur un bloc qui a quitté `comportement` ; `questions-classeur-NN.md` ; `blocked_classeur.md` renommé ou laissé ; la liste par bloc.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. `blocked_classeur.md` : absent → continuer ; un `## Decision` vide → arrêt ; tous remplis → le nommer.
3. `Clarification needed` → arrêt.
4. Garde `### Q` et classement, `questions-architecte-*.md` excepté.
5. Le numéro dans le prompt : le plus haut sous `questions/classeur/` plus un.
6. Le fichier répondu : le plus haut sous `questions/classeur/` avec `### Q`, nommé.
7. Quels blocs : `grep -B2 '^Nature:$'` (deux lignes au-dessus, le titre ; `Genre:` entre), gardé aux `Genre: comportement` ; plus `grep -B1 '^Nature: '` gardé aux blocs dont le genre n'est pas `comportement` — leur nature est à vider ; plus `^### .*MODIFIED` ; troisième déclencheur, le fichier répondu. Rien → invoquer personne, commit et push sans worktree.
8. → MECANISMES §Git, avant l'invocation.
9. Invoquer : `subagent_type="classeur"`, `model="sonnet"`, `description="Class <name>"` ; prompt `The product file: docs/features/<name>/desc-produit.md.`, `<Look at these blocks: …>`, `Your questions file number: NN.`, `<Plus: your answered questions file: docs/features/<name>/questions/classeur/questions-classeur-NN.md.>`, `<Plus: blocked_classeur.md, every ## Decision is filled.>`.
10. Renommer `blocked_classeur.md` seulement si le rapport dit avoir écrit la nature que chaque décision nomme ; laisser sur *waits on the Rédacteur* ou une valeur hors des huit.
11. Tout arrêt fusionne d'abord. `grep -B2 '^Nature:$'` gardé aux `comportement` : zéro attendu — jamais un `-c '^Nature:$'` nu.
12. Vérifier `questions-classeur-NN.md` écrit ; compter `^### Q`.
13. Cinq pas.
14. Relayer : combien classés, lesquels ont changé de nature, combien de questions, la liste par bloc, les blocs bloqués, et les deux lignes du rapport sur un fichier de blocage nommé (qui attend le Rédacteur, quelle décision nomme une valeur hors des huit) ; la table à huit lignes, symétrique de `/3a_genre` : fichier de blocage → `/3b_nature` ; blocage et questions → répondre puis `/1_lexique` ; chaque décision une réécriture → `/2_structure`, `/3_decoupe`, `/3a_genre`, retour ; hors liste → rien ; un `comportement` à `Nature:` vide sans fichier de blocage → une fois encore ; questions → `/1_lexique` ; vide ou rien → `/4_grille`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; cinq pas ; sans invocation, commit et push en place.

**La Product Owner intervient** : comme pour `/3a_genre`.

**Décisions**

- Les blocs sortis de `comportement` avec une nature sont nommés pour être vidés · écartée : laisser la ligne · raison : les vues par genre que `/5_reclasse` bâtit copient le bloc tel quel, et une nature périmée voyage avec (`/3b_nature`, *Which blocks it looks at*) · inconnu.
- Le compte des vides restreint aux `comportement` · écartée : `-c '^Nature:$'` nu · raison : un bloc d'un autre genre garde une `Nature:` vide pour de bon, et le compte nu rapporterait un défaut à chaque run (`/3b_nature`) · inconnu.
- Le troisième déclencheur · écartée : les deux greps seuls · raison : la même que `/3a_genre` (`docs/verification3/plan.md` entrée 14) · inconnu.
- Le renommage sur la ligne du rapport, « une fois encore », réponse avant décision, hors liste → rien · écartée : les mêmes alternatives que `/3a_genre` · raison : les mêmes sources (`docs/verification3/plan.md` entrées 5+6, 55) · inconnu.
- La branche `/1_lexique` retirée de la ligne « chaque décision une réécriture » · écartée : la garder · raison : `docs/verification4/plan.md` entrée 6 · non éprouvée.
- Le pointeur d'arrêt nomme les cinq pas · écartée : trois pas nommés · raison : `docs/verification4/plan.md` entrée 26 · non éprouvée.
- La liste par bloc relayée · écartée : un compte seul · raison : rien en aval n'attrape une mauvaise nature, les sondeurs la prennent comme donnée (`/3b_nature`, `classeur.md`) · inconnu.

## /4_grille

**Prend** : `<feature folder name>` ; le `## Decision` de six fichiers de blocage (→ MECANISMES §Emplacement des fichiers de blocage) : `cadrage-produit/blocked_par-bloc.md`, `blocked_par-question.md`, `blocked_par-nature.md`, `blocked_global.md`, `blocked_existant.md` à la racine, `blocked_assembleur.md` à la racine ; un grep `Clarification needed` ; `grep -B1 '^Nature:$'` filtré sur `comportement` ; le dernier `questions-*.md` de la racine, `questions-architecte-*.md` excepté, testé `^Answer:\s*$` sans `Défaut:` ; `grep -B1 '^Genre: comportement$'`, `grep -B1 '^Genre: transverse$'`, `grep -B1 '^Genre: hors périmètre$'` ; `^### .*NEW` et `^### .*MODIFIED` ; le plus haut `questions-sondeur-NN.md` et le plus haut `questions-existant-NN.md`, racine ou classés, et leur grep `^### Q` ; `grep -B3 '^Global: '` ; l'existence des quatre fichiers de questions et du relevé sous `cadrage-produit/` ; le rapport de l'assembleur (ses quatre comptes, un fichier manquant).

**Rend** : `cadrage-produit/par-bloc.md`, `par-question.md`, `par-nature.md`, `global.md`, `releve.md`, `questions.md` (→ MECANISMES §Fichiers du cadrage) ; `questions-sondeur-NN.md` à la racine, copie octet pour octet ou vide ; `questions-existant-NN.md` au second temps, écrit par le sondeur ou vide par la commande ; les six fichiers du tour précédent sous `cadrage-produit/closed/<fichier>-NN.md` ; les marqueurs retirés des lignes `### B` sur le tour qui écrit un `questions-sondeur-NN.md` vide ; les fichiers de blocage renommés ; la table *What to run next*.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. Tester les six noms, tous — plusieurs peuvent tenir à la fois : aucun → continuer ; un `## Decision` vide → arrêt, tous ceux qui tiennent nommés ; tous remplis → chacun nommé dans le prompt de sa seule lecture, et ces lectures seules invoquées, ensemble. La décision de l'assembleur → la fusion seule, sur les quatre fichiers encore en place ; les fichiers des lectures qui n'ont pas bloqué restent où ils sont, ne sont pas classés. Si les marqueurs ont changé entre-temps, c'est un tour neuf : les quatre tournent.
3. `Clarification needed` → arrêt.
4. Deux greps : chaque `Genre: comportement` a une `Nature:` remplie, sinon arrêt, `/3b_nature` ; le dernier fichier de questions de la racine est répondu (`^Answer:\s*$` sans `Défaut:`), sinon arrêt — `questions-architecte-*.md` lu comme absent.
5. Quels blocs, pour les angles : `grep -B1 '^Genre: comportement$'` ; premier tour (aucun `questions-sondeur-*.md` nulle part) → tous ; aucun bloc → invoquer personne, commit et push sans worktree, dire que la feature ne porte aucun comportement ; tours suivants → l'union `NEW` ∪ `MODIFIED`, identifiant = ce qui suit `### ` jusqu'au premier espace. Les trois angles reçoivent la même liste ; le global reçoit tous les comportements, chaque tour. Les blocs `transverse` vont dans les quatre prompts comme liste à part ; les `hors périmètre` dans le seul prompt global.
6. Le test de clôture du premier temps, avant les greps de marqueurs : le plus haut `questions-sondeur-NN.md`, racine ou `questions/sondeur/`, sans `### Q`, **et** aucun marqueur sur une ligne `### B` → premier temps clos, passer au second ; vide et un marqueur → le premier temps rouvre sur les blocs marqués seuls ; aucun marqueur et le plus haut tient un `### Q` → classé sous `questions/sondeur/` : écrire le `questions-sondeur-NN.md` suivant vide, sans agent, puis le second temps ; à la racine : arrêt, `/1_lexique` et `/2_structure` d'abord.
7. Git avant : garde `### Q` et classement (pas sur un tour qui relance la fusion seule ni une lecture seule) ; les six fichiers du tour précédent → `cadrage-produit/closed/<fichier>-NN.md` ; `chore: answers` ; sur un tour de second temps, pas de worktree encore ; sinon → MECANISMES §Git, avant l'invocation, puis `mkdir -p docs/features/<name>/cadrage-produit/closed` dans le worktree.
8. Le second temps, une fois le premier clos. A-t-il déjà tourné ? Le plus haut `questions-existant-NN.md`, racine ou `questions/existant/` : aucun → continuer ; vide → fini, rien écrire ; `### Q` et classé → écrire le suivant vide sans agent, commit et push sans worktree. Quels blocs : `grep -B3 '^Global: '` ; rien → `questions-existant-NN.md` vide, commit et push sans worktree ; sinon le worktree, puis une invocation : `subagent_type="sondeur"`, `model="opus"`, `description="Cross <name> against the global"`, prompt `The product file: …`, `The grid: .claude/grids/GRILLE_EXISTANT.md.`, `The global: docs/PRODUIT_GLOBAL.md.`, `Invocation 3 — Existant.`, `These blocks, with the global section each names:` une ligne `<B12 → ## Section title>` par bloc, `Write to docs/features/<name>/questions-existant-NN.md.` (`NN` = le plus haut sous `questions/existant/` plus un), `Your blocking file, if you cannot produce: docs/features/<name>/blocked_existant.md.`, `<Plus: that same file, its decision is filled.>`. Pas de fusion : une lecture, un fichier. `blocked_existant.md` → relayer, arrêt ; renommé `-NN` une fois la décision appliquée.
9. Les quatre invocations du premier temps, dans un seul message, et attendre les quatre : trois `Invocation 1 — Angle` ne différant que par `Your reading order:` et le fichier de sortie (→ MECANISMES §Ordres de lecture des sondeurs — ce qui distingue les trois angles), `description="Probe <name>, by block | by question | by nature"`, prompt `The product file:`, `The grid: .claude/grids/GRILLE_CADRAGE_PRODUIT_V2.md.`, `Pass A on these blocks: <list>.`, `The transverse blocks, to hold beside them: <list — or: none>.`, `Your reading order: …`, `Write to docs/features/<name>/cadrage-produit/par-<angle>.md.`, `<Plus: …/blocked_par-<angle>.md, its decision is filled.>` ; une `Invocation 2 — Global: every behaviour block: <list>.`, `description="Record and cross <name>"`, avec `The out-of-scope blocks: <list — or: none>.`, `Write the record to …/cadrage-produit/releve.md.`, `Write to …/cadrage-produit/global.md.`, `<Plus: …/blocked_global.md, its decision is filled.>`.
10. Avant la fusion : un `cadrage-produit/blocked_*.md` ou `blocked_existant.md` non numéroté → pas de fusion, pas de fichier à la racine, relayer et arrêt. Puis les quatre fichiers et le relevé existent ; pour chaque manquant : son fichier de blocage à côté → relayer, arrêt ; ni l'un ni l'autre → arrêt, dire quelle lecture n'a rien produit, relancer `/4_grille`.
11. Invoquer l'assembleur : `subagent_type="assembleur"`, `model="sonnet"`, `description="Merge the four readings of <name>"`, prompt `Merge, in docs/features/<name>/cadrage-produit/:` puis les quatre noms, `Write to docs/features/<name>/cadrage-produit/questions.md.`, `<Plus: docs/features/<name>/blocked_assembleur.md, its decision is filled.>`.
12. L'assembleur rapporte un fichier manquant → arrêt, relancer ; rien en dessous ne tourne.
13. Renommer chaque fichier de blocage nommé, dans son dossier, `-NN` = le numéro du tour, celui du `questions-sondeur-NN.md` du tour ; un tour sans fichier prend le numéro qu'il aurait pris ; les six `closed/` prennent le même (→ MECANISMES §Renommage -NN — divergence).
14. `cp cadrage-produit/questions.md docs/features/<name>/questions-sondeur-NN.md`, `NN` = le plus haut sous `questions/sondeur/` plus un. Aucune question → écrire le fichier vide. Sur ce tour, retirer par script un `NEW` ou `MODIFIED` final de chaque ligne `### B` de `desc-produit.md`, une édition par ligne, dans le worktree.
15. → MECANISMES §Git, après le rapport — les cinq pas.
16. Relayer : combien de questions par lecture et combien la fusion a gardées, du rapport de l'assembleur seul ; la table — un sondeur a bloqué → remplir puis `/4_grille`, ces lectures seules ; l'assembleur a bloqué → la fusion seule ; premier temps avec questions → répondre puis `/1_lexique` ; premier temps vide → `/4_grille`, le second temps tourne ; second temps avec questions → répondre puis `/1_lexique`, une arbitration devient un bloc ; second temps vide, ou déjà fini → `/5_reclasse`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; un worktree seulement quand un agent va écrire ; cinq pas ; sur les tours sans agent, → MECANISMES §Commit sans worktree, le fichier vide ajouté.

**La Product Owner intervient** : elle répond aux `questions-sondeur-NN.md` et `questions-existant-NN.md` en français, le silence acceptant une `Défaut:` ; elle remplit chaque `## Decision` ; elle relance `/1_lexique` sur un fichier répondu.

**Décisions**

- Les trois angles reçoivent la même liste ; le global lit chaque comportement, chaque tour · écartée : le global sur les blocs marqués · raison : un bloc changé change ses croisements avec chaque autre (`/4_grille`, *Which blocks the angles probe*) · inconnu.
- Seuls les `comportement` sont sondés · écartée : tout genre · raison : un autre genre n'a ni déclencheur ni sortie, les questions de la grille ne s'y appliquent pas (`/4_grille`) · inconnu.
- Les `transverse` à chaque sondeur, chaque tour ; les `hors périmètre` au global seul · écartée : ne pas les passer · raison : une question qu'une règle transverse répond déjà devient une *défaut* ; `C1.2` est une question de la passe C, celle du global, et sans les blocs exclus la grille redemande ce qu'elle a déjà écrit (`/4_grille`) · inconnu.
- Sur une décision levée, seule la lecture qui a bloqué retourne · écartée : tout relancer · raison : relancer remplacerait les entrées mêmes contre lesquelles la décision fut écrite, jusqu'à trois invocations opus pour le même résultat (`/4_grille`, *Before anything else*) · inconnu.
- La clôture du premier temps testée sur le plus haut fichier, racine ou classé · écartée : la racine seule · raison : une commande voisine classe le fichier vide, et un test sur la racine lirait une grille close comme cassée (`/4_grille` ; `docs/verification3/plan.md` entrées 4 et 16) · inconnu.
- Jamais « aucun marqueur » seul comme clôture · écartée : les marqueurs seuls · raison : un marqueur dit qu'un bloc a bougé, pas que la grille a tourné ; un test sur les marqueurs seuls ferait tourner la grille sans fin (`/4_grille`) · inconnu.
- Le second temps une fois, après le premier clos, en une invocation · écartée : trois ordres de lecture · raison : un seul corpus à croiser ; trois ordres liraient le global trois fois (`/4_grille`, *The second time*) · inconnu.
- Un `questions-existant-NN.md` classé avec `### Q` → le suivant écrit vide sans agent · écartée : relancer le sondeur · raison : ses réponses sont passées par `/1_lexique` et `/2_structure` ; `/5_reclasse` teste le plus haut de chaque nom et un fichier classé tenant des questions ne ferme rien (`docs/verification3/plan.md` entrée 4) · inconnu.
- Une liste de comportements vide → invoquer personne · écartée : quatre sondeurs opus sur rien · raison : `docs/verification4/plan.md` entrée 29 · non éprouvée.
- Une lecture manquante sans fichier de blocage → arrêt et relance, pas de fusion à trois · écartée : fusionner ce qui est là · raison : une fusion à laquelle manque une lecture est une fusion que personne ne peut croire (`/4_grille`, `assembleur.md`) · inconnu.
- Un fichier manquant pour l'assembleur est une faute du run à réparer, pas une décision · écartée : un fichier de blocage · raison : rien là n'est à trancher par la Product Owner (`assembleur.md`, *Where you work*) · inconnu.
- La copie `cp` octet pour octet · écartée : réécrire par lecture · raison : cinquante entrées réécrites en contexte, c'est là qu'une est perdue ou reformulée (`/4_grille`, *Once it has reported*) · inconnu.
- Un fichier vide écrit sans agent aux clôtures · écartée : rien écrire · raison : c'est l'évidence que `/5_reclasse` teste (`/4_grille`) · inconnu.

## /5_reclasse

**Prend** : `<feature folder name>` ; le plus haut `questions-sondeur-NN.md` et le plus haut `questions-existant-NN.md`, racine ou classés, et leur `^### Q` ; `^### .*NEW`, `^### .*MODIFIED` ; `grep -c '^Genre:$'` ; `grep -B1 '^Nature:$'` filtré sur `comportement` ; la garde `### Q` ; `desc-produit.md`, pour copier ses blocs (`grep -B1 '^Genre: <genre>$'`, chaque bloc de son `### B` au titre suivant) ; `par-genre/comportements.md`, qu'il vient d'écrire.

**Rend** : les six fichiers `par-genre/comportements.md`, `transverses.md`, `directives.md`, `references.md`, `hors-perimetre.md`, `recette.md`, remplacés entiers ; `desc-par-nature.md` à la racine, remplacé entier ; le commit `chore: product file by nature` poussé ; les comptes par genre et par nature.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. La grille a clos : les deux plus hauts fichiers présents et sans `### Q`, où qu'ils soient, et aucun marqueur sur une ligne `### B` ; sinon arrêt, dire `/4_grille`.
3. `grep -c '^Genre:$'` doit rendre zéro ; sinon dire quels blocs, `/3a_genre`, arrêt. Chaque `comportement` a une nature ; sinon `/3b_nature`, arrêt.
4. Garde `### Q` et classement, `questions-architecte-*.md` excepté.
5. Le tri par genre : supprimer les six fichiers précédents ; un grep par genre, `grep -B1 '^Genre: <genre>$'` accents compris ; chaque bloc copié par script du `### B` au titre suivant de tout niveau ; un genre sans bloc → fichier vide ; un `Genre:` hors des six → dire quel bloc, arrêt sans écrire. Le nom de fichier est le genre au pluriel, sans accent, un tiret pour l'espace. Compter `^### B` dans les six et dans `desc-produit.md` : égaux, sinon arrêt sans commit.
6. Le tri par nature : `desc-par-nature.md` depuis `par-genre/comportements.md`, jamais depuis le fichier produit ; `# Product file by nature`, puis les huit natures dans l'ordre `model`, `persistence`, `calculation`, `transition`, `external exchange`, `synchronisation`, `presentation`, `access`, un `## <nature>` chacune, `*(none)*` sous une nature vide ; sous chacune, chaque bloc dont la `Nature:` la porte, dans l'ordre du fichier produit, copié par script, son marqueur `NEW` ou `MODIFIED` retiré de la ligne `### B` ; une `Nature:` hors des huit → arrêt sans écrire. Compter `^### B` dans `desc-par-nature.md` et dans `comportements.md` : égaux, sinon arrêt sans commit.
7. → MECANISMES §Commit sans worktree, `chore: product file by nature`, push.
8. Relayer : combien de blocs par genre, puis par nature ; `/6_convertit`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : pas de worktree ; commit et push en place.

**La Product Owner intervient** : aucun.

**Décisions**

- Les vues réécrites entières à chaque run · écartée : une mise à jour incrémentale · raison : un bloc changé peut avoir changé de genre ou de nature, et un fichier gardé le rangerait sous l'ancien (`/5_reclasse`) · inconnu.
- Le fichier produit reste le maître, les vues sont dérivées · écartée : les vues comme source · raison : un bloc rangé sous le mauvais genre n'est jamais perdu, le run suivant le remet (`/5_reclasse`) · inconnu.
- Les deux fichiers de clôture exigés, que la feature s'attache ou non au global · écartée : `questions-existant-NN.md` facultatif · raison : le second temps écrit ce fichier vide quand aucun bloc ne porte `Global:`, son absence dit qu'il n'a jamais tourné (`/5_reclasse`) · inconnu.
- Le tri par nature bâti sur `comportements.md`, pas sur le fichier produit · écartée : le fichier produit · raison : seul un comportement a une nature (`/5_reclasse`) · inconnu.
- Les marqueurs retirés des copies, jamais du fichier produit · écartée : les garder · raison : `/6_convertit` compare ces blocs par octets aux derniers traduits, et un marqueur qui vient ou part se lirait comme un changement (`/5_reclasse`) · inconnu.
- Une copie par script, jamais retapée · écartée : retaper · raison : un bloc retapé est un bloc qui a pu changer, et rien en aval ne le verrait (`/5_reclasse`) · inconnu.
- Deux comptes croisés, arrêt sans commit sur un écart · écartée : faire confiance · raison : un écart est un bloc sans genre, copié deux fois, perdu ou doublé (`/5_reclasse`) · inconnu.
- `comportements.md` lu par le second mouvement seul · écartée : le Convertisseur le lit · raison : le Convertisseur lit `convertisseur/<nature>-input.md` (`docs/verification3/plan.md` entrée 47) · inconnu.
- La commande tourne sur une feature sans comportement et écrit `par-genre/recette.md` · écartée : s'arrêter avant · raison : l'arrêt d'une feature sans rien à bâtir est à `/7_lots`, qui dit où vit `recette.md` (`docs/verification4/plan.md` entrée 30, F13) · non éprouvée.

## /6_convertit

**Prend** : `<feature folder name>` ; l'existence de `code/decoupage.md`, `par-genre/`, `desc-par-nature.md` ; le `## Decision` de chaque `convertisseur/blocked_<nature>.md` et `blocked_transversal.md` non numéroté ; la garde `### Q` ; la part de chaque nature dans `desc-par-nature.md` (les lignes sous `## <nature>` jusqu'au `## ` suivant), comparée par `cmp` ou `diff -q` à `convertisseur/<nature>-input.md` ; l'existence de `convertisseur/<nature>.md`, son grep `<<ASSUMED` ; `convertisseur/technique-<nature>.md` et `technique-transversal.md`, greppés `### Q` et `^Answer:\s*$` ; le plus haut `questions/convertisseur/questions-convertisseur-NN.md` ; `spec-technique.md` (ouvre sur `# Preamble`, greps `<<ASSUMED` et `[B`) ; `tracabilite.md` (existence, première colonne contre les identifiants de `desc-produit.md`) ; les `## Trace` des `convertisseur/*-notes.md` pour résoudre ; `convertisseur/questions-<nature>.md`, `questions-transversal.md` (existence, copie).

**Rend** : `convertisseur/<nature>-input.md` ; `convertisseur/closed/questions-<nature>-NN.md`, `closed/technique-<nature>-NN.md` ; `spec-technique.md` assemblé, ses références à cible unique résolues ; `questions-convertisseur-NN.md` à la racine, fusion renumérotée ou vide ; les fichiers de blocage renommés ; les fichiers du Convertisseur (→ MECANISMES §Fichiers de la conversion) ; la table *What to run next*.

**Étapes**

1. Sans argument, demander et s'arrêter. `code/decoupage.md` existe → arrêt, un changement du produit appartient à un nouveau cycle. `par-genre/` absent, ou `desc-par-nature.md` absent → arrêt, `/5_reclasse`.
2. Les fichiers de blocage, fichier par fichier : aucun → continuer ; un `## Decision` vide → arrêt, tous nommés ; remplis → chacun nommé dans le prompt de sa nature, `blocked_transversal.md` dans celui de l'invocation 2.
3. La garde `### Q` sur chaque `questions-*.md` de la racine, `questions-architecte-*.md` excepté : un fichier qui tient des questions → arrêt, le fichier nommé.
4. Quelles natures tournent — pour chacune des huit, plusieurs lignes peuvent s'appliquer, la nature tourne une fois et son prompt porte la ligne de chaque ligne qui a matché :

   | Ce qu'on trouve | La nature |
   |---|---|
   | sa part ne tient aucun bloc | ne tourne nulle part ; `<nature>.md`, `<nature>-input.md`, `<nature>-notes.md` supprimés dans le worktree, plus bas ; sa section écrite vide |
   | sa part diffère de `convertisseur/<nature>-input.md`, ou ce fichier est absent | tourne |
   | `convertisseur/<nature>.md` absent, et sa part a changé | tourne |
   | `convertisseur/<nature>.md` porte `<<ASSUMED`, et sa part a changé | tourne |
   | `convertisseur/technique-<nature>.md` répondu — un `### Q` et aucun `^Answer:\s*$` | tourne, quoi qu'aient fait ses blocs ; le fichier nommé dans son prompt |
   | l'une des deux précédentes, part identique à l'octet, et `technique-<nature>.md` tient un `^Answer:\s*$` | attend — ne tourne pas |
   | l'une des deux, part identique, et aucun `technique-<nature>.md` avec `^Answer:\s*$` | tourne ; le plus haut `questions/convertisseur/questions-convertisseur-NN.md` nommé dans son prompt |
   | `convertisseur/blocked_<nature>.md` porte un `## Decision` rempli | tourne |
   | rien de tout cela | gardée telle quelle |

   Aucune nature ne tourne : `spec-technique.md` existe, ouvre sur `# Preamble`, sans `<<ASSUMED` ni `[B`, `tracabilite.md` là, aucune nature qui ne tourne nulle part n'a de fichier à supprimer, aucune nature en attente, `technique-transversal.md` absent ou avec `^Answer:\s*$`, `blocked_transversal.md` sans décision remplie → le document tient : rien n'est classé, rien commité, aucun worktree, aller au relais (étape 13). Tous ces tests passent avant le premier geste sur le dépôt.

   Puis Git avant : classement des `questions-*.md` de la racine (`questions-architecte-*.md` excepté) ; chaque `convertisseur/questions-*.md` du dernier run → `convertisseur/closed/questions-<nature>-NN.md`, numéro libre suivant ; jamais un `technique-*.md` ; `chore: answers` ; worktree depuis `HEAD` ; `convertisseur/closed/` créé dans le worktree. Dans le worktree, les fichiers des natures qui ne tournent nulle part sont supprimés, et la part de chaque nature qui tourne est copiée dans `convertisseur/<nature>-input.md`. Aucune nature ne tourne, et le document ne tient pas → l'assemblage (étape 6) — un `technique-transversal.md` répondu force l'assemblage et l'invocation 2, qui le nomme.
5. Les invocations de nature, dans un seul message : `subagent_type="convertisseur"`, `model="opus"`, `description="Convert <name>, <nature>"`, prompt `Feature folder: docs/features/<name>/.`, `Invocation 1 — Nature: <nature>.`, `<Plus: convertisseur/technique-<nature>.md, its question is answered.>`, `<Plus: questions/convertisseur/questions-convertisseur-NN.md, its answers changed no block — the mark's answer is there.>`, `<Plus: convertisseur/blocked_<nature>.md, its decision is filled.>`. Attendre toutes. Puis un grep des `convertisseur/blocked_*.md` neufs non numérotés : chacun est bloqué, tous rapportés, aller à l'étape 11 — tout arrêt fusionne d'abord. Puis chaque nature a écrit `convertisseur/questions-<nature>.md`, et `<nature>-notes.md` quand elle a écrit sa section ; `technique-<nature>.md` n'est écrit que sur une question technique ; un fichier manquant arrête, la nature nommée.
6. L'assemblage : chaque nature dont la part tient des blocs a son `convertisseur/<nature>.md`, et aucune n'attend → assembler `spec-technique.md` entier, les neuf sections dans l'ordre `## §1 Model` … `## §8 Access`, `## §9 Text`, chaque `§1`–`§8` copié par script de son fichier, une nature sans bloc et toujours `§9` en `*(empty)*`, jamais une section omise, pas de préambule ; sinon rien assemblé, `spec-technique.md` supprimé, invocation 2 sautée, aller à l'étape 10, la nature sans section ou en attente nommée.
7. Les références à une cible : dans `spec-technique.md`, jamais dans les fichiers de nature, chaque `[B<n>: …]` dont la ligne `## Trace` du bloc, dans le `*-notes.md` qui la tient, porte une seule entrée → ce numéro à la place des crochets ; plusieurs, un tiret ou pas de ligne → laissé. Un `]` sur une autre ligne → faute du run, arrêt, fusion d'abord (→ MECANISMES §Marques <<ASSUMED et [B).
8. Invocation 2, chaque fois qu'un document a été assemblé : `description="Convert <name>, transversal"`, prompt `Feature folder: …`, `Invocation 2 — Transversal.`, `<Plus: convertisseur/technique-transversal.md, its question is answered.>`, `<Plus: convertisseur/blocked_transversal.md, its decision is filled.>`.
9. Après : `convertisseur/questions-transversal.md` existe, sinon arrêt. `tracabilite.md` contre ce fichier : là → complet ; manquant et un `### Q` dans `questions-transversal.md` ou dans `technique-transversal.md` → le *No* de l'invocation 2, pas une faute ; manquant et vide → faute, arrêt, fusion d'abord. Un `<<ASSUMED` à côté d'un fichier technique répondu → la nature n'a pas appliqué sa réponse, relancer depuis l'étape 5, une fois. `grep '\[B'` : ce qui reste à côté d'un fichier de questions vide → relancer l'invocation 2 une fois. Comparer les identifiants des titres de `desc-produit.md` à la première colonne de `tracabilite.md` : un manquant ou un en trop → faute (→ MECANISMES §tracabilite.md).
10. Les questions : fusionner dans le `questions-convertisseur-NN.md` suivant à la racine (le plus haut sous `questions/convertisseur/` plus un) les fichiers écrits ce run, les natures dans l'ordre des sections puis `questions-transversal.md`, chaque entrée copiée, renumérotée depuis `Q1` ; jamais un `technique-*.md` ; aucune → fichier vide.
11. Renommer chaque fichier de blocage nommé, `convertisseur/blocked_<nature>-NN.md` ; chaque fichier technique répondu nommé dans un prompt et dont l'invocation a écrit ce pour quoi il existe (la section, ou `tracabilite.md`) → `convertisseur/closed/technique-<nature>-NN.md`, après un grep `^Answer:\s*$` — un hit est une question neuve, le fichier reste.
12. → MECANISMES §Git, après le rapport — les cinq pas.
13. Relayer : quelles natures ont tourné (et lesquelles sur une part inchangée), gardées, en attente ; combien de questions ; combien de `<<ASSUMED` ; la table, première ligne qui matche, la ligne « en attente » au-dessus de la dernière, la ligne *No* de l'invocation 2 s'ajoutant à celle qui a matché : fichier de blocage seul → remplir puis `/6_convertit` ; blocage et questions techniques seules → répondre, remplir, `/6_convertit` ; blocage et questions produit → remplir, répondre, `/1_lexique` ; techniques seules → répondre puis `/6_convertit` ; produit, seules ou avec techniques → répondre puis `/1_lexique` ; une nature attend → répondre puis `/6_convertit` ; fichier vide ou document qui tient (jamais sans `# Preamble` ni sans `tracabilite.md`) → `/conventions` puis `/7_lots`, `/fusion_compare` pouvant brancher ici. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; cinq pas ; tout arrêt fusionne d'abord — sept natures ont écrit dans le worktree.

**La Product Owner intervient** : elle répond à `questions-convertisseur-NN.md` (boucle longue, par `/1_lexique`) et, en place, aux `convertisseur/technique-<nature>.md` et `technique-transversal.md` (boucle courte) ; elle remplit chaque `## Decision`.

**Décisions**

- Une reconversion par nature, sur les parts qui ont changé ou marquées `<<ASSUMED` · écartée : tout réécrire à chaque run · raison : une invocation opus par nature pour un résultat connu (`/6_convertit`, *Which natures run*) · inconnu.
- La comparaison par octets de la part, pas les marqueurs · écartée : les marqueurs · raison : le Rédacteur les retire dès qu'un tour de grille ou de conversion les a consommés ; un bloc changé deux tours plus tôt n'en porte plus (`/6_convertit`) · inconnu.
- L'arrêt sur `code/decoupage.md` · écartée : reconvertir · raison : un lot cite les entrées par numéro, réécrire une section la renumérote sous le lot (`/6_convertit`) · inconnu.
- Un fichier technique répondu fait tourner la nature quoi qu'aient fait ses blocs · écartée : la ligne « part changée » seule · raison : une réponse technique ne change aucun bloc, sans cette ligne elle attendrait pour toujours (`/6_convertit`) · inconnu.
- Le Convertisseur lit son propre fichier de questions répondu quand la réponse n'a changé aucun bloc · écartée : le Rédacteur écrit la confirmation dans le bloc · raison : le même écart sur le même texte marqué à chaque run ; le Qualifieur fait déjà l'exception (`docs/verification3/plan.md` entrée 15, item B, Option 1) · inconnu.
- Plusieurs lignes qui matchent → un run, chaque ligne dans le prompt · écartée : le fichier à la seule ligne « part identique » · raison : une ligne omise est une réponse que l'invocation ne voit jamais (`docs/verification4/plan.md` entrée 9) · non éprouvée.
- Une nature en attente est un troisième état, et rien n'est assemblé tant qu'une attend · écartée : assembler avec la marque · raison → MECANISMES §Fichiers de la conversion (`docs/verification4/plan.md` entrée 30, F18) · non éprouvée.
- Les références à cible unique résolues par script avant l'invocation 2 · écartée : tout laisser à l'invocation 2 · raison : une entrée ne laisse rien à juger (`/6_convertit`, *The references with one target*) · inconnu.
- L'invocation 2 chaque fois qu'un document a été assemblé · écartée : seulement au premier assemblage · raison : une section réécrite a pu renuméroter ses entrées, chaque référence est à résoudre à neuf (`/6_convertit`) · inconnu.
- Les questions techniques jamais fusionnées, répondues en place · écartée : les fusionner · raison : elles sont techniques, la boucle courte les ramène sans rejouer l'amont (`/6_convertit`, `convertisseur.md`) · inconnu.
- La boucle courte, exception à « toute réponse repasse par `/1_lexique` » · écartée : tout par `/1_lexique` · raison : une réponse technique n'apporte aucun vocabulaire produit et ne touche aucun bloc (`/6_convertit`, *What you relay*) · inconnu.
- La table des blocages lue fichier par fichier · écartée : « un » fichier · raison : plusieurs peuvent tenir à la fois, un par nature bloquée (`docs/verification3/plan.md` entrée 51) · inconnu.
- La ligne « en attente » gagne sur la dernière ligne du relais · écartée : sans règle de première correspondance · raison : une nature en attente fait écrire un fichier vide, et le run matchait deux lignes (`docs/verification3/plan.md` entrée 52) · inconnu.
- Une marque encore là après la relance est une faute, une relance jamais deux · écartée : relancer jusqu'à ce qu'elle tombe · raison : une marque après la relance est une faute du run, rapportée comme un fichier manquant (`/6_convertit`) · inconnu.
- La commande tourne sur une nature vide et sur une feature sans comportement · écartée : s'arrêter · raison : le seul endroit où la question « y a-t-il quelque chose à bâtir » est répondable, et elle écrit le `tracabilite.md` que `/9_controle` exige (`docs/verification4/plan.md` entrée 30, F13) · non éprouvée.

## /conventions

**Prend** : `<feature folder name>`, premier argument ; un second argument facultatif nommant un `bugfix-NN`, que `argument-hint` ne dit pas (→ MECANISMES §Frontmatter d'une commande) ; l'existence de `spec-technique.md`, `couverture.md`, `docs/TECHNICAL_CONVENTIONS.md`, `questions-architecte-*.md` à la racine ; deux greps sur ce dernier — des lignes `Answer:` sans rien après, et `^### Q` ; le `## Decision` et la ligne `## Invocation` de `blocked_architecte.md` du dossier de travail ; pour chaque requête de `architecte/`, si son `## Verdict` est rempli — un bloc sans titre `## Verdict` compte pour vide (→ MECANISMES §Requête de conventions — divergence).

**Rend** : `docs/TECHNICAL_CONVENTIONS.md` ; `couverture.md` à la racine de la feature ; `questions-architecte-NN.md` ; les verdicts sous `architecte/` ; `blocked_architecte.md` renommé ; le fichier intégré classé sous `questions/architecte/` ; la liste `git status --porcelain docs/features/<name>/` et un `wc -l` du fichier de questions.

**Étapes**

1. Sans argument, demander et s'arrêter. Le dossier de feature se dérive du premier argument seul. `spec-technique.md` absent → arrêt, sauf pour l'invocation 3.
2. Marcher la table du haut, première ligne qui matche :

   | Le dossier tient | Ce qu'on invoque |
   |---|---|
   | `blocked_architecte.md` à `## Decision` vide | rien — relayer, arrêt |
   | `blocked_architecte.md` rempli | l'invocation que sa ligne `## Invocation` nomme, le fichier nommé dans le prompt |
   | une requête de `architecte/` à `## Verdict` vide ou sans titre `## Verdict` | `3 — Requests` |
   | un second argument nomme un `bugfix-NN`, et aucune ligne au-dessus | rien à invoquer, `/8_code` continue ; les lignes en dessous sont celles du dossier de feature |
   | `questions-architecte-NN.md` à la racine avec une `Answer:` vide | rien — dire quelles questions attendent |
   | `questions-architecte-NN.md` à la racine, répondu | `2 — Integrating`, le fichier nommé |
   | pas de `docs/TECHNICAL_CONVENTIONS.md` | `1 — Deriving` |
   | il existe, et pas de `couverture.md` à la racine de la feature | `4 — Completing` |
   | `questions-architecte-NN.md` à la racine sans `### Q` | rien — le classer et commiter sans worktree, dire `/7_lots` |
   | il existe, et un `couverture.md` | rien — dire `/7_lots` |
   | rien de tout cela | rien — dire `/7_lots` |

3. Le numéro dans le prompt : le plus haut `questions-architecte-NN.md`, racine et `questions/architecte/` ensemble, plus un.
4. Git avant : garde `### Q` sur les `questions-*.md` de la racine dont le préfixe n'est pas `architecte`, puis leur classement ; chaque `questions-architecte-*.md` de la racine sans `### Q` → `questions/architecte/` ; jamais un fichier intégré, qui a quitté la racine dans le worktree ; `chore: answers` ; worktree depuis `HEAD`.
5. Invoquer : `subagent_type="architecte"`, `model="opus"`, `description="conventions <feature>"` ; un des quatre prompts — `Working folder: docs/features/<name>/. Invocation 1 — Deriving. Your questions file number: NN.` · `… Invocation 2 — Integrating. Answered file: questions-architecte-NN.md. Your questions file number: NN.` · `Working folder: <the working folder>. Invocation 3 — Requests. Called by the orchestration.` · `… Invocation 4 — Completing. Your questions file number: NN.` — plus le nom de `blocked_architecte.md` sur la forme que sa ligne `## Invocation` nomme (→ MECANISMES §Valeurs de « Called by » — qui a invoqué l'Architecte).
6. Le rapport dit une décision appliquée → `git mv <folder>/blocked_architecte.md <folder>/blocked_architecte-NN.md`, dans le worktree.
7. Après l'invocation 2, `git mv` du fichier intégré vers `questions/architecte/`, dans le worktree ; un nouveau fichier écrit par l'agent reste à la racine.
8. Les cinq pas, le merge en `git merge --no-ff -m "<message>" <commit id>` (→ MECANISMES §Git, après le rapport — les cinq pas).
9. Relayer le rapport et l'invocation qui a tourné, le fichier de blocage s'il y en a un ; la table — questions → répondre puis `/conventions` ; une `conjunction` → le cas ordinaire, née entre deux entrées complètes qu'aucune grille ne pouvait voir ensemble, répondre puis `/conventions`, la réponse devient une règle et `couverture.md` porte sa ligne (`conventions.md` L296) ; un `replacement` → une règle en vigueur dit le contraire de ce que la feature exige et des lots codés la suivent, remplacer une règle en vigueur est à la Product Owner : répondre — changer la règle, ou s'y conformer — puis `/conventions` ; les lots que la question nomme comme codés sous l'ancienne, elle les fait rentrer par `/diagnostique` (`bug-list.md` dans un `bugfix-NN/`), la chaîne n'a pas d'autre retour dans des lots codés (`conventions.md` L300) ; une question produit → la Product Owner corrige le fichier produit à la main, le comportement se bâtit au cycle suivant, aucun tour amont ne rejoue ; une `inconsistency` → le document technique est faux, l'entrée dite, la correction est dans `/6_convertit` ; une `forme` → la grille manque une forme, la Product Owner l'amende elle-même, `couverture.md` dit ce qu'il en advient ; fichier de blocage → remplir puis `/conventions` ; rien demandé ou tout intégré → `/7_lots`. Puis `git status --porcelain docs/features/<name>/`, une ligne par fichier, et `wc -l` sur le fichier de questions pour dire s'il tient des questions. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; renommage et classement dans le worktree, avant les cinq pas ; sur la ligne « sans `### Q` », → MECANISMES §Commit sans worktree.

**La Product Owner intervient** : elle lance la commande à la main, entre `/6_convertit` et `/7_lots`, et avec un second argument sur un `bugfix-NN` ; elle répond à `questions-architecte-NN.md` (pour une `coverage`, le comportement ou *voir produit*) ; elle corrige le fichier produit sur une question produit ; elle amende `GRILLE_CONVENTIONS.md` sur une `forme` ; elle remplit le `## Decision` de `blocked_architecte.md`.

**Décisions**

- Le test d'existence porte sur le fichier de conventions, jamais sur `couverture.md` · écartée : tester `couverture.md` · raison : `couverture.md` est écrit par feature ; un test dessus enverrait chaque feature sauf la première par l'invocation 1, qui écrit le fichier à neuf et perd chaque règle ajoutée depuis (`/conventions`, *Which invocation*) · inconnu.
- `couverture.md` absent → invocation 4, ce qui rend la commande idempotente · écartée : pas d'invocation 4 · raison : `couverture.md` dit si cette feature a déjà été parcourue (`/conventions`) · inconnu.
- La ligne « fichier vide » sous les deux lignes `couverture.md` · écartée : au-dessus · raison : un `couverture.md` manquant envoie d'abord à l'invocation 4, et le fichier vide restant est classé par ce même run (`docs/verification4/plan.md` entrée 10) · non éprouvée.
- Une question de feature sans réponse n'arrête plus une requête d'un `bugfix-NN` · écartée : l'arrêt en tête · raison : la ligne de la table, sous celles de l'invocation 3, est où un fichier non répondu arrête (`docs/verification4/plan.md` entrée 28) · non éprouvée.
- Le fichier architecte vide classé avant d'invoquer · écartée : le laisser · raison : laissé à la racine, il matchait sa ligne à chaque run et répondait `/7_lots` pour toujours (`docs/verification3/plan.md` entrée 21) · inconnu.
- Le renommage sous *Git, once it has reported*, après le rapport · écartée : sous *Git, before invoking* · raison : `docs/verification3/plan.md` entrée 48 · inconnu.
- Les invocations 1, 2 et 4 sur le dossier de feature seul · écartée : sur un `bugfix-NN` · raison : les conventions se dérivent des deux documents d'une feature, et un cycle de correction n'a ni l'un ni l'autre (`/conventions`) · inconnu.
- Lancée à la main, aucune commande ne l'enchaîne · écartée : `/6_convertit` ou `/7_lots` l'enchaîne · raison : elle se tient entre les deux et la Product Owner la lance là (`/conventions`, *When it runs*) · inconnu.
- Le `git status --porcelain` et le `wc -l` relayés · écartée : le rapport seul · raison : un run qui a écrit une question sans le dire est un run dont la question est perdue, la Product Owner ne va pas chercher (`/conventions`, *What you relay*) · inconnu.
- Une question produit : corrigée à la main, bâtie au cycle suivant · écartée : rejouer un tour amont · raison : la grille de cadrage n'a pas fermé le produit, et le comportement est un nouveau comportement (`/conventions`) · inconnu.
- Une ligne du relais pour `forme` · écartée : la ranger sous « questions » · raison : `docs/verification3/plan.md` entrée 9 · inconnu.
- La commande énumère cinq issues nommées — question produit, `conjunction`, `inconsistency`, `forme`, `replacement` — et sur un `replacement` renvoie les lots codés sous l'ancienne règle à `/diagnostique` (`conventions.md` L300 ; → MECANISMES §Les cinq Kind: — la sorte d'une question de l'Architecte) · écartée : la voie de requête de l'Arbitre (`arbitre.md` L409, invocation 3) · raison : l'`Answer:` resterait vide et `conventions.md` L81 bloquerait chaque run suivant ; le contrat du fichier de questions devrait changer · non éprouvée.

## /fusion

**Prend** : `<feature folder name>` ; l'existence de `desc-produit.md`, `rapport-fusion.md`, `desc-produit-fusion.md`, `plan-fusion.md`, d'un dossier `bugfix-*/`, d'un `questions-fusionneur-*` où que ce soit ; le `## Invocation` et le `## Decision` de `blocked_redacteur.md` et `blocked_fusionneur.md` ; une `Answer:` vide d'un fichier de questions de la racine, `questions-architecte-*.md` excepté ; un grep `^### Q` de `questions-fusionneur-NN.md` ; le grep `INIT` de `plan-fusion.md` ; chaque `code/decisions-produit.md` que `/9_controle` a produit, la feature puis chaque `bugfix-NN/`, par leur existence.

**Rend** : `desc-produit-fusion.md`, copie faite par la commande puis amendée par le Rédacteur (invocation 3) ; `plan-fusion.md`, `questions-fusionneur-NN.md`, `rapport-fusion.md`, `docs/PRODUIT_GLOBAL.md` selon la phase ; les fichiers de blocage renommés ; la ligne de la table qui a tiré.

**Étapes**

1. Sans argument, demander et s'arrêter. Une seule phase par run, jamais deux agents enchaînés.
2. Marcher la table, première ligne qui matche :

   | # | Test | Ce qu'on fait |
   |---|---|---|
   | 1 | `desc-produit.md` absent | erreur, arrêt |
   | 2 | `blocked_redacteur.md` dont `## Invocation` dit 3, ou `blocked_fusionneur.md`, à `## Decision` vide | arrêt, relayer |
   | 3 | l'un des deux, rempli | l'agent que son nom porte, à l'invocation que sa ligne nomme, le fichier nommé ; le Rédacteur reçoit aussi les fichiers de décisions |
   | 4 | `rapport-fusion.md` existe | arrêt, la fusion est faite |
   | 5 | un fichier de questions de la racine à `Answer:` vide, `questions-architecte-*.md` excepté | arrêt, relayer |
   | 6 | `desc-produit-fusion.md` absent | redacteur, `3 — Merging` |
   | 7 | `questions-fusionneur-NN.md` avec `### Q`, répondu, et pas de `plan-fusion.md` | fusionneur, invocation 3 |
   | 8 | un dossier `bugfix-*/`, et aucun `questions-fusionneur-*` nulle part | fusionneur, invocation 3 |
   | 9 | `questions-fusionneur-NN.md`, répondu ou vide, et pas de `plan-fusion.md` | fusionneur, invocation 1 |
   | 10 | `plan-fusion.md` existe | fusionneur, invocation 2 |
   | 11 | sinon | fusionneur, invocation 1 |

   Tout autre `blocked_*.md` à la racine arrête la marche, la commande à qui il est nommée — un `blocked_redacteur.md` à `## Invocation` 1 ou 2 est à `/2_structure`.
3. Une ligne qui invoque a tiré (3, ou 6 à 11) : d'abord la garde `### Q` sur les `questions-*.md` de la racine dont le préfixe n'est ni `fusionneur` ni `architecte` → un fichier qui tient des questions arrête, nommé — avant la copie de la ligne 6 et avant tout geste git. Puis, la ligne 6 a tiré : `cp docs/features/<name>/desc-produit.md docs/features/<name>/desc-produit-fusion.md`, puis invoquer — dans cet ordre.
4. Git avant : classement de chaque fichier dont le préfixe n'est pas celui de la phase qui va tourner, `questions-architecte-*.md` laissé, et de chaque fichier de ce préfixe sauf le plus haut, qui porte la numérotation ; sur une ligne Fusionneur, le numéro = le plus haut `questions-fusionneur-NN.md`, racine et `questions/fusionneur/` ensemble, plus un ; `chore: answers` ; worktree depuis `HEAD`.
5. Sur `INIT` : l'invocation 2 va tourner (ligne 10, ou 3 la nommant) et `plan-fusion.md` ne tient que le mot `INIT` → `cp docs/features/<name>/desc-produit-fusion.md docs/PRODUIT_GLOBAL.md` dans le worktree, avant d'invoquer ; tout autre plan, pas de copie.
6. Invoquer : `subagent_type="<redacteur | fusionneur>"`, `model="sonnet"`, `description="<phase> <feature>"`, prompt `Feature folder: docs/features/<name>/. <Which invocation>.` puis `[Questions file number: <NN>.]` sur chaque Fusionneur, `[Decisions files, in cycle order: <path>, <path>.]` sur chaque Rédacteur (omise sans fichier de décisions), `[Blocking file: <folder>/blocked_<agent>.md, its ## Decision filled.]` sur la ligne 3.
7. Le rapport dit une décision appliquée → `git mv <folder>/blocked_<agent>.md <folder>/blocked_<agent>-NN.md` dans le worktree.
8. Les cinq pas.
9. Relayer le rapport et la ligne qui a tiré. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; les deux `cp` sont dans le worktree et commités au pas 1 ; cinq pas.

**La Product Owner intervient** : elle lance la commande une fois par feature, après `/9_controle` de chaque cycle ; elle répond aux `questions-fusionneur-NN.md` ; elle remplit les `## Decision` ; sur un run après la fusion, non prévu, elle restaure à la main l'ancien global depuis git et met de côté `rapport-fusion.md`, `plan-fusion.md` et chaque `questions-fusionneur-*.md`.

**Décisions**

- Une phase par run, jamais deux agents enchaînés · écartée : enchaîner · raison : chaque arrêt rend la main à la Product Owner, et le run suivant reprend la table (`/fusion`, *How it runs*) · inconnu.
- Le Rédacteur (ligne 6) avant toute ligne Fusionneur · écartée : le Fusionneur d'abord · raison : il écrit la source que le Fusionneur lit, un Fusionneur au-dessus tournerait sur un fichier absent (`/fusion`) · inconnu.
- La ligne 8 avant toute ligne d'invocation 1 · écartée : après · raison : placée après, *Otherwise* enverrait une feature avec `bugfix-*/` droit à la comparaison, et ce que les corrections ont réglé n'atteindrait jamais le global (`/fusion`) · inconnu.
- La ligne 8 tire une fois, sur l'absence de tout `questions-fusionneur-*` · écartée : sur le dernier `bugfix-NN` · raison : le Fusionneur écrit un fichier même vide, et sa présence dit que la passe a tourné ; les dossiers `bugfix-*/` ne disparaissent jamais (`/fusion`) · inconnu.
- La ligne 7 teste `### Q` · écartée : `questions-fusionneur` seul · raison : sans ce test la ligne 7 tirerait sur sa propre sortie vide, pour toujours (`/fusion`) · inconnu.
- La copie du fichier produit par la commande, la ligne testant l'absence de la copie · écartée : le Rédacteur copie · raison : il n'a pas d'outil qui copie, et une lecture entière suivie d'une écriture entière tronque en silence ; copier avant le test ferait ne jamais tirer la ligne (`/fusion`, `redacteur.md`) · inconnu.
- Sans fichier de décisions, une copie fidèle tout de même · écartée : sauter la ligne 6 · raison : le Fusionneur ne doit jamais choisir sa source (`/fusion`, `redacteur.md` invocation 3) · inconnu.
- Les lignes 2 et 3 sur les deux fichiers de blocage que la commande route, tout autre arrête · écartée : router tout `blocked_*.md` · raison : un blocage amont ne se règle jamais d'ici ; la ligne 3 nomme les fichiers de décisions comme la ligne 6 (`docs/verification3/plan.md` entrée 36) · inconnu.
- Sur une première feature, l'invocation 3 écrit dans la copie, pas dans le global · écartée : sauter la ligne 8 ; réordonner la table · raison : une ligne dans le global ferait ne jamais tirer `INIT`, et la feature serait comparée phrase à phrase à un global presque vide ; sauter la ligne perdrait ce que la copie ne porte pas (`docs/verification3/plan.md` entrée 34, item E, Option 1) · inconnu.
- Aucun run après la fusion ; s'il en faut un, la Product Owner restaure l'ancien global à la main et met de côté le rapport, le plan et les fichiers de questions · écartée : une relance sur un `bugfix-NN` plus récent que le rapport · raison : la comparaison attend un global que la feature n'a pas encore atteint, et tournerait contre sa propre fusion (`docs/verification3/plan.md` entrée 35, item F, Option 1 ; `/fusion`) · inconnu.
- La garde `### Q` passe avant la copie de la ligne 6 et avant le classement, les préfixes `fusionneur` et `architecte` exceptés · écartée : classer sans garde ; la garde après la copie · raison : `docs/verification4/plan.md` entrée 32 ; un arrêt sur la garde laissait la copie, et la ligne 6, qui teste son absence, ne tirait plus jamais (`tools/cockpit/scan_rules.md` §2) · non éprouvée.
- Le plus haut `questions-fusionneur-NN.md` reste à la racine · écartée : le classer · raison : il porte la numérotation (`/fusion`) · inconnu.

## /fusion_compare

**Prend** : `<feature folder name>` ; l'existence de `desc-produit-fusion.md`, `rapport-fusion.md`, `plan-fusion.md`, d'un `bugfix-*/`, d'un `questions-fusionneur-*` ; le `## Decision` et le `## Invocation` de `blocked_fusionneur.md` ; la garde `### Q`.

**Rend** : `plan-fusion.md`, `questions-fusionneur-NN.md` ; `blocked_fusionneur.md` renommé.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. Six tests dans l'ordre, arrêt au premier : `desc-produit-fusion.md` absent → `/fusion` d'abord ; `blocked_fusionneur.md` à `## Decision` vide → relayer ; rempli et `## Invocation` 2 ou 3 → pas à cette commande, `/fusion_applique` pour 2, `/fusion` pour 3 ; `rapport-fusion.md` existe → la fusion est faite ; `plan-fusion.md` existe → `/fusion_applique` ; un `bugfix-*/` et aucun `questions-fusionneur-*` → `/fusion`, la passe des corrections n'a pas tourné. Un `blocked_fusionneur.md` rempli à `## Invocation` 1 → nommé dans le prompt.
3. Git avant : garde `### Q`, préfixes `architecte` et `fusionneur` exceptés — un `### Q` dans le fichier du Fusionneur est son état normal, l'attente est le test de `/fusion`, une `Answer:` vide ; classement de chaque `questions-*.md` dont le préfixe n'est pas `fusionneur`, `questions-architecte-*.md` laissé, et de chaque `questions-fusionneur-NN.md` sauf le plus haut ; le numéro = le plus haut, racine et `questions/fusionneur/` ensemble, plus un ; `chore: answers` ; worktree depuis `HEAD`.
4. Invoquer : `subagent_type="fusionneur"`, `model="sonnet"`, `description="Compare <feature>"`, prompt `Feature folder: docs/features/<name>/. Invocation 1 — Compare and question. Questions file number: <NN>.`, `[Blocking file: docs/features/<name>/blocked_fusionneur.md, its ## Decision filled.]`.
5. Décision appliquée → `git mv` en `-NN` dans le worktree, avant les cinq pas.
6. Les cinq pas.
7. Relayer : fichier de blocage → remplir puis `/fusion_compare` ; un `### Q` → répondre puis `/fusion_applique` ; vide → `/fusion_applique`. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; renommage dans le worktree ; cinq pas.

**La Product Owner intervient** : elle choisit cette branche plutôt que `/fusion` ; elle répond au fichier de questions ; elle remplit le `## Decision`.

**Décisions**

- Trois portes ajoutées — rapport, plan, passe des corrections non tournée · écartée : les trois premiers tests seuls · raison : `docs/verification4/plan.md` entrée 11 · non éprouvée.
- Le renommage avant les cinq pas, dans le worktree · écartée : après · raison : `docs/verification4/plan.md` entrée 12 · non éprouvée.
- La garde `### Q` laisse le fichier du Fusionneur · écartée : l'y soumettre · raison : le plus haut reste à la racine par construction, et un `### Q` y est son état normal (`docs/verification4/plan.md` entrée 31) · non éprouvée.
- Un `blocked_fusionneur.md` d'une autre invocation renvoie à sa commande · écartée : le nommer ici · raison : la ligne `## Invocation` route le fichier (`/fusion_compare` ; → MECANISMES §Valeurs de « ## Invocation » — qui a écrit ce fichier de blocage) · inconnu.

## /fusion_applique

**Prend** : `<feature folder name>` ; l'existence de `rapport-fusion.md`, `plan-fusion.md` ; le `## Decision` et le `## Invocation` de `blocked_fusionneur.md` ; une `Answer:` vide d'un `questions-fusionneur-*.md` de la racine ; le grep `INIT` de `plan-fusion.md`.

**Rend** : `docs/PRODUIT_GLOBAL.md` mis à jour ; `rapport-fusion.md` ; ou le `questions-fusionneur-NN.md` suivant seul ; `blocked_fusionneur.md` renommé ; tous les fichiers de questions de la racine classés une fois le rapport écrit.

**Étapes**

1. Sans argument, demander et s'arrêter.
2. Cinq tests dans l'ordre : `rapport-fusion.md` existe → arrêt ; `plan-fusion.md` absent → `/fusion_compare` ; `blocked_fusionneur.md` vide → relayer ; rempli et `## Invocation` 1 ou 3 → `/fusion_compare` pour 1, `/fusion` pour 3 ; un `questions-fusionneur-*.md` de la racine à `Answer:` vide → relayer lesquelles. Un fichier rempli à `## Invocation` 2 → nommé.
3. Le numéro : le plus haut `questions-fusionneur-NN.md`, racine et classés, plus un — l'invocation 2 en a besoin sur une réponse ambiguë. `chore: answers` ; worktree depuis `HEAD`.
4. Sur `INIT` seul dans le plan → `cp docs/features/<name>/desc-produit-fusion.md docs/PRODUIT_GLOBAL.md` dans le worktree ; tout autre plan, pas de copie.
5. Invoquer : `subagent_type="fusionneur"`, `model="sonnet"`, `description="Apply <feature>"`, prompt `Feature folder: docs/features/<name>/. Invocation 2 — Apply. Questions file number: <NN>.`, `[Blocking file: …, its ## Decision filled.]`.
6. Décision appliquée → `git mv` en `-NN` dans le worktree.
7. Les cinq pas.
8. Une fois `rapport-fusion.md` écrit : `git mv` de chaque `questions-*.md` de la racine vers `questions/<agent>/`, `questions-architecte-*.md` excepté, et commiter les déplacements. Pas de rapport → rien classé : le fichier reste à la racine pour la Product Owner et les tests du run suivant.
9. Relayer : fichier de blocage → relayer, arrêt ; un `### Q` → répondre, `/fusion_applique` de nouveau. Le relais finit sur la ligne `Next:` de son issue, arrêts compris (→ MECANISMES §Ligne Next:).

**Git** : `chore: answers` ; worktree depuis `HEAD` ; le `cp` et le renommage dans le worktree ; cinq pas ; le classement final commité après.

**La Product Owner intervient** : elle répond à un fichier de questions écrit sur une réponse ambiguë ; elle remplit le `## Decision` ; elle lit `rapport-fusion.md` une fois le global changé.

**Décisions**

- La copie sur `INIT` faite par la commande · écartée : l'agent copie · raison : il n'a pas d'outil qui copie, et une lecture entière suivie d'une écriture entière tronque en silence ; il retire de la copie ce qui n'appartient qu'au fichier de feature (`/fusion_applique`, `fusionneur.md`) · inconnu.
- Tout classé une fois le rapport écrit, rien sans rapport · écartée : classer à chaque run · raison : un run qui a écrit une question ou un fichier de blocage n'a rien appliqué, et le fichier reste où la Product Owner répond (`/fusion_applique`, *Filing away*) · inconnu.
- L'invocation 2 reçoit un numéro · écartée : aucun · raison : sur une réponse ambiguë elle écrit le fichier de questions suivant et rien d'autre (`/fusion_applique`) · inconnu.
- Le renommage avant les cinq pas · écartée : après · raison : fait après le commit, il reste hors de la fusion et laisse l'arbre sale pour le pas 5 (`/fusion_applique`) · inconnu.

---

# Les agents

Le frontmatter de chacun (→ MECANISMES §Frontmatter d'un agent), les lignes fixes de son prompt (→ MECANISMES §Invocation d'un agent), le numéro de son invocation (→ MECANISMES §Numéros d'invocation), ses chemins (→ MECANISMES §Chemins relatifs) et son fichier de blocage (→ MECANISMES §Fichier de blocage — divergence, §Emplacement des fichiers de blocage) sont définis là et seulement là.

### lexicographe, invocation 1 — Sweeping : balayer les termes de l'idée et lever les paires

Modèle: opus · effort aucun · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/1_lexique`, quand la racine ne tient aucun fichier de questions et que `desc-produit.md` n'existe pas ; de nouveau après chaque invocation 2.
Lit: `idees.md` entier ; `lexique.md` à partir du second balayage, son `## Tranché` d'abord ; le `blocked_lexicographe.md` que le prompt nomme.
Écrit: `lexique.md` — `## Relevé` reconstruit depuis l'idée, `## Non tranché` ; un nouveau `questions-lexicographe-NN.md`, toujours, même vide, numéroté par lui-même (racine et `questions/lexicographe/` ensemble, préfixe propre) ; `blocked_lexicographe.md`.
Valeurs: les deux sortes de mot — un texte affiché, entre guillemets, dans sa langue, gardé tel quel ; un concept, sans guillemets, en anglais à partir du fichier produit — lues et écrites par lui seul ; les quatre lectures d'une paire, écrites dans `Question:`, et celles qui conviennent à l'entrée proposées en `Options:`, en français — *les deux nomment une même chose* · *deux choses distinctes* · *l'un est l'abréviation de l'autre, en un seul endroit* · *un terme porte deux sens* ; les trois sections de `lexique.md` (→ MECANISMES §lexique.md), écrites ; la ligne `Terms:` du fichier de questions (→ MECANISMES §Fichier de questions — divergence), écrite.

**Gestes**
1. Depuis le second balayage, lire `## Tranché` : ce qu'il règle n'est jamais redemandé, même si l'idée montre encore les deux termes.
2. Balayage 1, les termes du domaine — donnée, événement, état, entité, vue — avec leur compte, jusqu'aux termes vus une fois ; pas l'aspect d'une vue, pas les variantes d'un texte affiché, pas la prose.
3. Balayage 2, les paires : une langue contre l'autre, deux termes d'une langue, un terme à deux sens ; chaque terme du balayage 1 comparé ; une graphie, une ponctuation, une forme grammaticale n'est pas une paire ; les deux phrases citées.
4. Balayage 3, les guillemets : un terme qui se lit comme un texte affiché sans guillemets, ou l'inverse.
5. Écrire `## Relevé` et `## Non tranché` ; jamais `## Tranché`.
6. Une entrée par paire et par guillemet douteux, `Terms:` puis la lecture proposée en question ; pour un terme à deux sens, chaque occurrence avec sa phrase groupée sous le sens lu, en une seule question.

**Branches** — aucun fichier d'idée, ou vide → blocage. Rien trouvé → le fichier de questions vide, ce qui ferme la boucle.
**Échange** — écrit `## Non tranché` que `/1_lexique` greppe ; écrit `Terms:` que le Product Owner lit ; lit `## Tranché` que l'invocation 2 écrit.
**Bloque** — `blocked_lexicographe.md`, quatre champs en table (forme 1, en table) ; un run bloqué n'écrit ni fichier de questions ni lexique ; le Product Owner répond.

**Décisions**
- Le lexicographe ne choisit jamais un terme, il propose une lecture · écartée : trancher lui-même · raison : la Product Owner possède le vocabulaire, une lecture est tout ce qu'il peut établir (`lexicographe.md`, *What you never do*, invocation 1) · inconnu.
- Un terme à deux sens fait une seule question, toutes ses occurrences groupées · écartée : une occurrence par sens · raison : c'est la seule forme dont la réponse peut nommer des occurrences (`lexicographe.md`, invocation 1) · inconnu.
- Un run bloqué n'écrit rien d'autre · écartée : écrire le fichier de questions quand même · raison : la commande lit la racine pour choisir l'invocation, et un fichier vide laissé là dirait la boucle close, le balayage ne tournerait jamais (`lexicographe.md`, *When you cannot produce*) · inconnu.
- Il n'ouvre jamais le fichier produit, à aucune invocation · écartée : le lire · raison : ce qu'il dit est réglé, ce qu'une réponse dit ne l'est pas (`lexicographe.md`) · inconnu.

### lexicographe, invocation 2 — Settling : appliquer les réponses à l'idée et régler le lexique

Modèle: opus · effort aucun · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/1_lexique`, quand `questions-lexicographe-NN.md` est seul à la racine avec un `### Q`, répondu.
Lit: `questions-lexicographe-NN.md` que le prompt nomme ; `idees.md` ; `lexique.md` ; le fichier de blocage nommé. Ces trois et rien d'autre.
Écrit: `idees.md`, les termes retirés remplacés hors guillemets, les guillemets ajoutés ou retirés ; `lexique.md`, chaque terme réglé déplacé de `## Non tranché` vers `## Tranché`, une entrée scopée finissant par `dans ce sens seulement` sur un sens renommé ; un nouveau `questions-lexicographe-NN.md` seulement si une réponse laisse le choix ouvert, jamais vide ; `blocked_lexicographe.md`.
Valeurs: `## Tranché` (`remplace :`, `dans ce sens seulement`, un texte affiché avec ses guillemets et sa langue, le concept à côté) — écrit ; la ligne `en anglais :` — jamais touchée, elle est au Rédacteur.

**Gestes**
1. Lire les réponses les unes contre les autres et contre `## Tranché` ; deux qui ne peuvent tenir ensemble font une question, ni l'une ni l'autre n'est appliquée.
2. Remplacer chaque terme retiré partout dans l'idée, sauf entre guillemets ; puis grepper chaque terme retiré : aucun hors guillemets, sauf où la réponse le garde.
3. Une réponse sur un guillemet ajoute ou retire les guillemets à chaque occurrence — le seul changement admis au-delà d'un remplacement de terme.
4. Une réponse renommant un sens seul remplace les occurrences de ce sens, celles que la réponse place, ou le groupement proposé si elle ne le touche pas.
5. Une réponse gardant deux termes ne change rien dans l'idée, et entre dans le lexique.
6. Mettre à jour `lexique.md` sans le réécrire : chaque entrée d'un tour antérieur reste ; les termes retirés sont écrits, pas supprimés.
7. Une réponse qui laisse le choix ouvert repart dans un nouveau fichier, jamais dans celui appliqué.

**Branches** — une réponse ouverte → un nouveau fichier de questions, et `/1_lexique` retourne à 2 ; aucune → la commande relance 1.
**Échange** — écrit `remplace :` que l'invocation 3 greppe ; écrit l'entrée scopée que l'invocation 3 lit pour ne pas remplacer ; écrit `## Tranché` que le Rédacteur lit et sur lequel il pose `en anglais :`.
**Bloque** — `blocked_lexicographe.md`, mêmes champs ; le Product Owner répond.

**Décisions**
- Un terme retiré entre guillemets reste · écartée : remplacer partout · raison : le texte atteint l'écran caractère pour caractère, et changer un mot dedans change ce que l'utilisateur lit (`lexicographe.md`, invocation 2) · inconnu.
- Une entrée scopée pour un sens renommé · écartée : un remplacement global · raison : le sens d'une occurrence est au Product Owner, pas à un grep ; sans la forme scopée, l'invocation 3 re-fusionnait les deux sens que la réponse venait de séparer (`docs/verification2/lexicographe.md` F05 ; `lexicographe.md`) · inconnu.
- Jamais un fichier de questions vide à 2 et 4 · écartée : un fichier toujours · raison : vide à la racine il se lirait comme attendant d'être appliqué (`lexicographe.md`, *Your questions file*) · inconnu.
- Le lexique mis à jour, jamais réécrit · écartée : le réécrire · raison : un terme passe de section en section, le tour suivant greppe ce fichier (`lexicographe.md`) · inconnu.

### lexicographe, invocation 3 — Watching : balayer les réponses d'un autre agent

Modèle: opus · effort aucun · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/1_lexique`, quand le fichier répondu d'un autre agent est seul à la racine avec un `### Q` — à chaque tour de la grille et de la conversion, `desc-produit.md` présent ou non.
Lit: le fichier répondu que le prompt nomme — ses `Answer:` et la `Défaut:` de chaque entrée à `Answer:` vide, chaque `Question:` comme contexte, jamais balayée ; `lexique.md` entier, `## Tranché` et `## Relevé` ; le fichier de blocage nommé.
Écrit: le fichier répondu, ses termes retirés remplacés dans les `Answer:` et les `Défaut:` acceptées ; `lexique.md`, `## Relevé` avec les termes du domaine que les réponses apportent, marqués `(réponse)`, `## Non tranché` avec chaque doute ; un nouveau `questions-lexicographe-NN.md`, toujours, même vide ; `blocked_lexicographe.md`.
Valeurs: `(réponse)` dans `## Relevé` — écrit ; l'entrée scopée — lue, jamais remplacée sur grep.

**Gestes**
1. Une entrée à `Answer:` remplie et `Défaut:` : balayer la réponse, jamais la défaut refusée.
2. Remplacer d'abord ce que le lexique retire : chaque terme d'une ligne `remplace :`, greppé dans les réponses et les défauts acceptées, remplacé par l'entrée qu'il porte, sauf entre guillemets ; cette ligne seule, jamais `en anglais :`, `retenu aussi`, une abréviation.
3. Une ligne `remplace :` finissant par `dans ce sens seulement` n'est jamais remplacée : chaque occurrence est une question, groupée par sens, que l'invocation 4 applique.
4. Balayage 1 : un mot que le lexique ne porte nulle part et qui désigne ce qu'il porte, `en anglais :` compris ; chaque doute sous `## Non tranché` ; un terme nouveau n'est pas une question mais entre dans `## Relevé`.
5. Balayage 2 : les guillemets, même test qu'à 1.
6. Écrire le fichier de questions, même vide.

**Branches** — rien demandé → le fichier vide finit le tour, 4 ne tourne pas ; quelque chose → 4 après réponse.
**Échange** — lit `Défaut:` que le sondeur écrit ; écrit `## Non tranché` que `/1_lexique` compte ; laisse le fichier répondu au Rédacteur (invocation 2).
**Bloque** — `blocked_lexicographe.md` ; le Product Owner répond.

**Décisions**
- La `Défaut:` d'une entrée à `Answer:` vide est balayée comme une réponse · écartée : les `Answer:` seules · raison : le silence a accepté la proposition, ses termes entrent dans le produit comme ceux d'une réponse, et deux agents plus loin écriraient la même chose de deux façons (`lexicographe.md`, invocation 3 ; `docs/verification2/lexicographe.md` F06) · inconnu.
- Chaque doute sous `## Non tranché` · écartée : `## Relevé` seul · raison : le compte de la commande ne le verrait pas, et 4 serait envoyé déplacer un terme jamais là (`lexicographe.md` ; `docs/verification2/lexicographe.md` F07) · inconnu.
- `## Relevé` comme base du balayage, y compris les termes sans rival · écartée : `## Tranché` seul · raison : un terme qui n'a jamais eu de rival est exactement celui qu'une réponse renomme (`lexicographe.md`) · inconnu.
- La `Question:` lue comme contexte, jamais éditée ni balayée · écartée : balayer tout le fichier · raison : une réponse est une réplique et désigne par sa question ; un autre agent a écrit la question (`lexicographe.md`) · inconnu.

### lexicographe, invocation 4 — Correcting : appliquer ses propres réponses au fichier répondu

Modèle: opus · effort aucun · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/1_lexique`, quand le fichier répondu d'un autre agent et un `questions-lexicographe-NN.md` avec `### Q` sont à la racine ensemble — seulement quand 3 a demandé.
Lit: `questions-lexicographe-NN.md` nommé ; le fichier répondu nommé ; `lexique.md` ; le fichier de blocage nommé.
Écrit: le fichier répondu, les termes que ses réponses règlent remplacés dans les `Answer:` et les `Défaut:` acceptées, guillemets ajustés, jamais une `Question:` ; `lexique.md`, chaque terme réglé déplacé vers `## Tranché`, les termes apportés dans `## Relevé` ; un nouveau `questions-lexicographe-NN.md` seulement sur une réponse ouverte ; `blocked_lexicographe.md`.
Valeurs: les mêmes qu'à 2, écrites.

**Gestes**
1. Remplacer, dans les réponses et les défauts acceptées, chaque terme que ses propres questions règlent — et ceux-là seuls, 3 ayant déjà remplacé ce que le lexique retire ; un sens renommé, les occurrences que la réponse place.
2. Une réponse ouverte repart dans un nouveau fichier.
3. Mettre à jour `lexique.md` comme à 2 ; une question sur le terme d'une entrée scopée quitte `## Non tranché` sans rien ajouter.

**Branches** — une réponse ouverte → nouveau fichier, retour à 4 ; aucune → `/2_structure`.
**Échange** — laisse le fichier répondu propre au Rédacteur.
**Bloque** — `blocked_lexicographe.md`.

**Décisions**
- 4 applique ses réponses seules · écartée : refaire le remplacement du lexique · raison : 3 l'a fait ; refaire déplacerait ce qui n'est plus là (`lexicographe.md`, invocation 4) · inconnu.

### redacteur, invocation 1 — Structuring : transcrire l'idée en fichier produit

Modèle: sonnet · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/2_structure`, quand aucun fichier de questions n'est à la racine et que `desc-produit.md` n'existe pas, sur un vocabulaire réglé.
Lit: `idees.md` ; `lexique.md` ; `docs/PRODUIT_GLOBAL.md` par son index, puis une section proche pour le test (→ MECANISMES §Lecture du global par l'index) ; `blocked_redacteur.md` nommé. Jamais un fichier de questions, jamais la grille.
Écrit: `desc-produit.md` (→ MECANISMES §En-tête d'un bloc produit) ; `lexique.md`, une ligne `en anglais :` sous l'entrée `## Tranché` d'un concept rendu pour la première fois ; `questions-redacteur-NN.md`, toujours, numéroté par lui-même ; `blocked_redacteur.md` (forme 2).
Valeurs: `NEW` sur chaque bloc créé (→ MECANISMES §NEW / MODIFIED — ce qui a bougé depuis le dernier tour), écrit ; `Genre:` et `Nature:` vides, écrites ; `Global: ## <section>` écrite quand le test dit oui, absente sinon ; la marque *existing* en fin de référence, écrite quand un titre de l'index nomme la destination ; `Block:` du fichier de questions, écrite, `-` pour la feature.

**Gestes**
1. Décomposer chaque passage en sujets — un déclencheur, une sortie ; ce qui déclenche, pas le sujet grammatical ; une carte de navigation vaut autant de sujets que de chemins.
2. Grepper l'index du global pour un titre couvrant le sujet ; un titre proche → charger la section, même déclencheur et même sortie ? oui → réutiliser le titre et écrire `Global:` ; non → créer, sans jamais reprendre un titre du global après un non.
3. Classer un bloc par sujet, `Genre:` et `Nature:` vides ; une sortie différente sur un déclencheur partagé fait son bloc ; numéro attribué à l'écriture, jamais réattribué, local à la feature.
4. Ce qu'il ne comprend pas : transcrire une lecture et poser `**Clarification needed:**` en fin de bloc, doublée d'une entrée du fichier de questions (→ MECANISMES §Marque Clarification needed) ; une contradiction de la Product Owner : la phrase la plus tardive transcrite, le bloc marqué, la question levée.
5. Réconcilier dans le bloc les deux descriptions d'un élément — un qualificatif et une valeur sont un seul énoncé.
6. Marquer *existing* une destination qu'un titre de l'index nomme, sans charger de section.
7. Écrire `en anglais :` sur un concept réglé rendu pour la première fois ; prendre la ligne existante sinon ; rien pour un concept sans entrée `## Tranché`.

**Branches** — l'idée couvre deux sujets sans lien (*ce qu'il fait en une phrase, sans « et »*) → blocage, deux features ne partagent pas un fichier produit.
**Échange** — écrit `Global:` que `/4_grille` greppe au second temps et que le sondeur 3 lit ; écrit *existing* que le Convertisseur lit pour `## Dependencies` ; écrit `en anglais :` que le Lexicographe lit à l'invocation 3 ; écrit `**Clarification needed:**` que quatre commandes greppent.
**Bloque** — `blocked_redacteur.md`, `## Invocation` 1 puis quatre titres ; le Product Owner répond, `/2_structure` le nomme.

**Décisions**
- Il ne converse jamais, ne décide aucune matière produit · écartée : combler un manque · raison : une lecture plausible règle une décision produit (`redacteur.md`, *Role*) · inconnu.
- La marque *existing* posée sur l'index seul, jamais en chargeant une section · écartée : vérifier en lisant · raison : l'index est ce qu'il a, une marque posée autrement est une supposition ; le Convertisseur en fait une dépendance du préambule (`redacteur.md`, *Outgoing references are marked*) · inconnu.
- `Global:` sur le test *même déclencheur, même sortie*, jamais sur un titre seul · écartée : sur le titre · raison : deux sections peuvent porter un nom et décrire deux comportements ; la grille du second temps ferme un bloc avec sa section en face (`redacteur.md`) · inconnu.
- Il n'ouvre jamais un autre dossier de feature · écartée : s'en inspirer · raison : sa forme ou ses mots porteraient ce produit dans celui-ci (`redacteur.md`, *What you never do*) · inconnu.
- La ligne `en anglais :` est la sienne, sur `## Tranché` seul · écartée : le Lexicographe l'écrit ; ajouter une entrée · raison → MECANISMES §lexique.md · inconnu.
- Ce qui est hérité et inchangé n'est pas réécrit · écartée : redire retention, export, consentement · raison : le global les porte déjà, ils n'apparaissent que s'ils changent (`redacteur.md`) · inconnu.

### redacteur, invocation 2 — Integrating : intégrer un fichier répondu ou une décision de réécriture

Modèle: sonnet · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/2_structure`, sur un fichier de questions avec `### Q` de tout préfixe sauf `architecte`, ou sur un `blocked_decoupeur.md`, `blocked_qualifieur.md` ou `blocked_classeur.md` dont chaque `## Decision` est rempli.
Lit: le fichier que le prompt nomme, et lui seul — jamais `idees.md`, jamais un second fichier de questions ; `lexique.md` ; le global par son index ; `desc-produit.md` par ses titres et les blocs nommés (→ MECANISMES §Lecture d'un bloc par grep) ; `blocked_redacteur.md` nommé.
Écrit: `desc-produit.md`, les blocs nommés édités en place, `MODIFIED` sur chaque bloc changé, `NEW` sur chaque bloc créé, les marqueurs retirés ou non selon le préfixe ; `lexique.md`, lignes `en anglais :` ; `questions-redacteur-NN.md`, toujours ; `blocked_redacteur.md`.
Valeurs: la table des préfixes qui retirent les marqueurs — lue par lui seul : `sondeur` et `existant` (la grille) et `convertisseur` (la conversion) → tout retirer puis marquer ce que ce tour touche ; `qualifieur`, `classeur`, `redacteur` → marquer, ne rien retirer ; les préfixes `lexicographe`, `architecte`, `fusionneur` ne figurent dans aucune ligne — `/2_structure` nomme « tout préfixe » ; `Défaut:` du sondeur, lue comme une réponse quand `Answer:` est vide ; `MODIFIED` sur tout le fichier quand un bloc `Genre: transverse` change — le seul genre qu'il lit.

**Gestes**
1. Retirer `NEW` et `MODIFIED` par une édition par ligne de titre, seulement si le préfixe du fichier est `sondeur`, `existant` ou `convertisseur`.
2. Grepper `^###`, charger par plage les seuls blocs que les réponses nomment.
3. Sur un fichier de blocage : lire chaque `## Decision` ; une décision nommant un genre ou une nature n'est pas la sienne, le bloc reste ; une décision de réécriture → le bloc réécrit avec `MODIFIED` ; les quatre passes ne s'appliquent pas.
4. Passe a : chaque réponse — `Défaut:` intégrée comme écrite quand `Answer:` est vide, une `Answer:` écrite la remplace — retire la `**Clarification needed:**` dont la formulation correspond ; même déclencheur et sortie → une phrase du bloc, ou remplace celle qu'elle contredit ; déclencheur ou sortie différent → un bloc à part par les mouvements 2 et 3 de l'invocation 1 ; le bloc en tient plusieurs → scission.
5. Passe b : scinder — l'original garde numéro et titre, les nouveaux prennent les numéros libres suivants, `Genre:` et `Nature:` vides partout, `Global:` recopiée sur chaque moitié ; grepper le numéro de l'original dans le fichier et mettre à jour chaque bloc qui le cite.
6. Passe c : chaque moitié porte un déclencheur ; sinon passe a de nouveau.
7. Passe d : une réponse apporte-t-elle un sujet qu'aucun titre ne couvre — sur la liste des titres, jamais en chargeant ; `Block: -` est la source la plus fréquente ; rien → l'index du global n'est pas ouvert.

**Branches** — un fichier de blocage nommé au lieu d'un fichier de questions → réécriture seule ; un sujet nouveau → les quatre mouvements de l'invocation 1.
**Échange** — lit `Défaut:` du sondeur ; lit les `## Decision` du decoupeur, du qualifieur, du classeur ; écrit `MODIFIED` que le qualifieur, le classeur, le sondeur, le decoupeur greppent ; retire les marqueurs que `/4_grille` a consommés.
**Bloque** — `blocked_redacteur.md`, `## Invocation` 2 ; `/2_structure` le nomme.

**Décisions**
- Les marqueurs retirés seulement sur un préfixe de grille ou de conversion · écartée : retirer à chaque intégration · raison → MECANISMES §Marqueurs NEW et MODIFIED · inconnu.
- Un bloc `transverse` changé marque tout le fichier · écartée : ne marquer que lui · raison : rien ne relie une règle transverse aux blocs qu'elle atteint, et sans marqueur ce que la grille a réglé sur l'ancienne formulation tiendrait ; brutal et voulu, une règle transverse change rarement (`redacteur.md`, *The two markers*) · inconnu.
- Le fichier produit jamais lu entier · écartée : le lire · raison : des centaines de lignes pour une poignée de blocs (`redacteur.md`, *How you load the product file*) · inconnu.
- Une décision de genre ou de nature n'est pas la sienne · écartée : écrire la ligne · raison : l'agent qui a bloqué écrit la ligne à son run suivant (`redacteur.md`, invocation 2) · inconnu.
- Le même travail quel que soit l'agent qui a demandé · écartée : un mode par préfixe · raison : « same work whoever asked » (`redacteur.md`, PART 2) · inconnu.

### redacteur, invocation 3 — Merging : plier les décisions produit dans la copie

Modèle: sonnet · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/fusion`, ligne 6 (`desc-produit-fusion.md` absent) ou ligne 3 (`blocked_redacteur.md` à `## Invocation` 3, rempli) — une fois, avant le Fusionneur.
Lit: `desc-produit-fusion.md`, copié par la commande ; chaque `code/decisions-produit.md` que le prompt nomme, dans l'ordre des cycles — la feature, puis `bugfix-01`, `bugfix-02` ; `lexique.md` ; le global par son index ; `blocked_redacteur.md` nommé. Jamais `desc-produit.md`.
Écrit: `desc-produit-fusion.md` en place, tous marqueurs retirés ; `lexique.md`, lignes `en anglais :` ; `blocked_redacteur.md`, `## Invocation` 3, un `## Blocking N` par décision non placée, un `## Decision` chacun. Jamais un fichier de questions.
Valeurs: la ligne d'un fichier de décisions — l'identifiant `B<n>` ou un tiret, deux espaces, la décision en français (→ MECANISMES §Identifiants) — lue.

**Gestes**
1. Ouvrir la copie ; ne jamais la copier lui-même.
2. Plier chaque fichier de décisions dans l'ordre nommé, une décision plus tardive gagnant sur une antérieure — dit dans le rapport, pas une question ; chaque ligne lue comme écrite, traduite comme une réponse à l'invocation 2, placée dans un bloc existant par la liste des titres, ou un bloc neuf par les quatre mouvements de l'invocation 1.
3. Une décision non placée ou illisible → une entrée de `blocked_redacteur.md`, le pliage continue ; sur la réinvocation, plier ces décisions seules.
4. Retirer chaque `NEW` et `MODIFIED` de la copie, même sans fichier de décisions.

**Branches** — aucun fichier de décisions → la copie, marqueurs retirés, telle quelle.
**Échange** — lit `code/decisions-produit.md` que `/9_controle` écrit (`PROCESS_AVAL.md`) ; écrit la copie que le Fusionneur lit à ses invocations 1 et 3.
**Bloque** — `blocked_redacteur.md`, `## Invocation` 3, entrées `## Blocking N` ; le Product Owner répond ; `/fusion` ligne 3 le nomme, avec les fichiers de décisions.

**Décisions**
- Les décisions de codage passent par `code/decisions-produit.md`, jamais par le fichier produit · écartée : les écrire dans `desc-produit.md` · raison : le fichier produit est ce que l'amont a fermé, et un cycle relancé doit le retrouver tel quel ; sur un cycle de correction c'est la seule route du produit (`redacteur.md`, invocation 3) · inconnu.
- Le pliage continue après un blocage, une entrée par décision · écartée : s'arrêter à la première · raison : la copie est complète sauf ce que le fichier nomme, et la réinvocation plie celles-là seules (`redacteur.md` ; `docs/verification3/plan.md` entrée 36) · inconnu.
- Jamais un fichier de questions à 3 · écartée : en écrire un · raison : `/fusion` routerait sur un fichier qui n'y signifie rien (`redacteur.md`, *The shape of a questions file*) · inconnu.
- Jamais un drapeau dans la copie · écartée : `**Clarification needed:**` · raison : le Fusionneur le porterait dans le global (`redacteur.md`) · inconnu.
- Aucun marqueur dans la copie · écartée : les garder · raison : rien ne la sonde, elle est lue une fois par le Fusionneur (`redacteur.md`) · inconnu.

### decoupeur — scinder les blocs qui portent plus d'un déclencheur

Modèle: opus · effort aucun · outils: Read, Grep, Edit, Write
Invoquée par: `/3_decoupe`, à chaque tour entre `/2_structure` et `/3a_genre` ; une seconde fois dans le même run sur les blocs non atteints.
Lit: `desc-produit.md` — les blocs nommés par plage, après un grep `^### B` ; entier seulement quand le prompt dit *every block*. Rien d'autre, jamais un fichier de blocage.
Écrit: `desc-produit.md`, une édition par bloc remplacé ; `blocked_decoupeur.md` à côté du fichier produit (forme 1, quatre titres `##`).
Valeurs: `NEW` sur chaque bloc produit sauf celui qui garde titre et numéro, qui garde son marqueur — écrit ; `Genre:` et `Nature:` vides sur chaque bloc écrit, `Global:` recopiée — écrites ; le critère du déclencheur, lu par lui seul : ce qui doit arriver pour que les phrases tiennent — action, événement, seuil, donnée entrante, temps, état d'une donnée nommée ; un événement qu'un déclencheur du bloc produit n'est pas un second déclencheur mais sa suite ; deux événements à conséquence identique sont deux valeurs d'un déclencheur ; ce que rien ne déclenche — constante, table, catalogue — est un bloc à part.

**Gestes**
1. Lire chaque bloc nommé entier ; lister ses déclencheurs et les phrases de chacun, puis les phrases que rien ne déclenche.
2. Un déclencheur, un bloc, ses phrases rassemblées d'où qu'elles viennent ; les phrases que rien ne déclenche font un bloc à part.
3. Éditer en place, un bloc à la fois ; numéroter depuis le plus haut du grep `^### B`, jamais un numéro réutilisé ; le bloc qui porte ce que le titre nommait garde titre, numéro et marqueur ; chaque phrase atterrit dans un seul bloc.
4. Un bloc dont le seul déclencheur est une suite : laissé, dit dans le rapport par son identifiant.
5. Rapporter tous les blocs regardés, ceux scindés et en quoi, les blocs à suite.

**Branches** — une phrase porte deux déclencheurs à conséquences différentes → blocage, ce qui est déjà scindé écrit d'abord ; les blocs non atteints gardent leurs marqueurs.
**Échange** — écrit `NEW` que le qualifieur, le classeur et les sondeurs greppent ; sa liste de blocs regardés est ce que `/3_decoupe` compare.
**Bloque** — `blocked_decoupeur.md`, `## Decision` vide ; le Product Owner répond ; `/2_structure` le nomme au Rédacteur, jamais `/3_decoupe` au decoupeur.

**Décisions**
- Il ne réécrit, n'ajoute, ne supprime aucune phrase · écartée : reformuler · raison : il déplace, il ne reformule pas ; une phrase à deux déclencheurs est une réécriture amont (`decoupeur.md`, *What you never do*) · inconnu.
- Il ne fusionne jamais deux blocs · écartée : fusionner une suite avec son déclencheur · raison : aucun agent ne fusionne ; il n'ouvre pas un bloc non nommé pour trouver celui que la suite suit (`decoupeur.md`) · inconnu.
- Le critère est la conséquence, pas le nombre d'événements · écartée : un bloc par événement · raison : un déclencheur qui distingue trois cas donne un bloc à trois cas (`decoupeur.md`, *The rule*) · inconnu.
- Ce que rien ne déclenche fait son bloc · écartée : le laisser dans le comportement · raison : le qualifieur donne un genre par bloc, une contrainte laissée dans un comportement prendrait le sien ; un catalogue serait sondé sous les questions du déclencheur (`decoupeur.md`) · inconnu.
- `## Decision` en titre `##`, jamais en table · écartée : la table · raison : `/3_decoupe` et `/2_structure` greppent `^## Decision$` (`docs/verification3/plan.md` entrée 63) · inconnu.

### qualifieur — écrire la ligne `Genre:` de chaque bloc nommé

Modèle: sonnet · effort aucun · outils: Read, Grep, Edit, Write
Invoquée par: `/3a_genre`, à chaque tour, sur les blocs à `Genre:` vide, les `MODIFIED`, ou sur son fichier répondu seul.
Lit: `desc-produit.md`, les blocs nommés par leur titre (`grep '^### B7 '`) et une lecture bornée ; son `questions/qualifieur/questions-qualifieur-NN.md` répondu nommé ; `blocked_qualifieur.md` nommé. Jamais le fichier entier.
Écrit: la ligne `Genre:` des blocs nommés, une édition ancrée sur le titre et la ligne `Genre:` ensemble ; `questions-qualifieur-NN.md` à la racine, toujours, numéro reçu du prompt ; `blocked_qualifieur.md` (forme 3, `## Blocking N`).
Valeurs: les six genres — écrits, en minuscules, accents et espace compris (→ MECANISMES §Les six genres — le genre d'un bloc) ; `MODIFIED` — lu ; le test pour `transverse`, lu par lui seul : la règle peut-elle nommer le bloc qu'elle concerne ? oui → ce bloc ; non, parce qu'elle concerne une catégorie → `transverse` ; l'asymétrie des deux doutes, lue par lui seul : entre `comportement` et l'un de `directive`, `référence`, `hors périmètre`, `recette`, il tranche `comportement` en silence ; entre `comportement` et `transverse`, toujours une question, la ligne disant `comportement` en attendant ; une `transverse` dont la formulation ne dit pas sa portée, toujours une question, la ligne disant `transverse`.

**Gestes**
1. Appliquer d'abord chaque réponse de son fichier répondu au bloc qu'elle nomme, si elle tient encore ; sinon dériver à neuf ; ne jamais redemander sur un bloc dont la réponse vient d'être appliquée.
2. Par bloc : le sujet d'abord ; une catégorie → `transverse` ; sinon l'un des quatre autres — `recette` avant `comportement` ; sinon `comportement`, quoi qu'il ait ou lui manque.
3. Sur un `MODIFIED` déjà genré, refaire 2 par le sujet et comparer ; différent → écrire, et le dire.
4. Un bloc qui quitte `comportement` avec une `Nature:` remplie : la ligne n'est pas touchée, le bloc nommé dans le rapport pour le classeur.
5. Sur un fichier de blocage nommé : un genre parmi les six → l'écrire ; réécriture ou retrait → ligne vide, *waits on the Rédacteur* dans le rapport ; un genre hors des six → ligne vide, dit.
6. Rapporter les comptes, la liste par bloc, les blocs bloqués, les identifiants des blocs questionnés.

**Branches** — aucun genre ne convient, ou deux conviennent parce que le bloc n'a pas été scindé → une entrée de blocage, la ligne vide, les autres blocs traités, le fichier de questions écrit.
**Échange** — lit `## Decision` que le Product Owner remplit ; écrit *waits on the Rédacteur* que `/3a_genre` clé ; écrit `Genre: comportement` que `/3b_nature`, `/4_grille`, `/5_reclasse` greppent.
**Bloque** — `blocked_qualifieur.md`, un `## Blocking N` par bloc ; le Product Owner répond ; une réécriture passe par `/2_structure`.

**Décisions**
- Le sujet avant le déclencheur · écartée : déclencheur et sortie d'abord · raison : une règle transverse a d'ordinaire déclencheur et sortie, lue ainsi elle serait `comportement` à chaque fois (`qualifieur.md`, PART 3) · inconnu.
- L'asymétrie : quatre doutes tranchés en silence vers `comportement`, deux toujours demandés · écartée : une question par doute · raison : un faux `comportement` est le côté que l'aval voit — le classeur bloque, les sondeurs ne trouvent rien ; un comportement classé autrement quitte le fichier que la grille lit, trou silencieux ; l'asymétrie est fausse pour `transverse`, absent de la liste de `/4_grille`, une question avant `/3b_nature` contre une par bloc après (`qualifieur.md`, *Your questions*) · inconnu.
- La ligne écrite même sur un doute · écartée : la laisser vide · raison : vide, le bloc lui revient pour redemander (`qualifieur.md`) · inconnu.
- L'édition ancrée sur titre et `Genre:` ensemble · écartée : la ligne seule · raison : chaque ligne vide est identique, une correspondance non unique est refusée (`qualifieur.md`, *What you never do*) · inconnu.
- Un bloc à deux genres bloque, jamais un genre choisi · écartée : le genre majoritaire · raison : il enverrait un comportement hors de la grille (`qualifieur.md`, *The six genres*) · inconnu.
- Il ne juge jamais une directive · écartée : la contester · raison : la Product Owner l'a réglée, il dit que c'en est une (`qualifieur.md`) · inconnu.

### classeur — écrire la ligne `Nature:` de chaque comportement nommé

Modèle: sonnet · effort aucun · outils: Read, Grep, Edit, Write
Invoquée par: `/3b_nature`, à chaque tour, sur les comportements à `Nature:` vide, les `MODIFIED`, les blocs sortis de `comportement` avec une nature, ou son fichier répondu seul.
Lit: `desc-produit.md`, les blocs nommés par leur titre, bornés ; son `questions/classeur/questions-classeur-NN.md` répondu nommé ; `blocked_classeur.md` nommé.
Écrit: la ligne `Nature:`, une édition sur la plage titre → `Nature:` ; `questions-classeur-NN.md`, toujours, numéro reçu ; `blocked_classeur.md` (forme 3).
Valeurs: les huit natures — écrites, en minuscules, l'espace gardé (→ MECANISMES §Les huit natures — la nature d'un bloc) ; `Genre: comportement` — lu, la seule valeur de genre qu'il lit ; les frontières entre natures, lues par lui seul — model · persistence : ce que la donnée est, ou ce qu'elle devient en stockage ; calculation · transition : une valeur, ou un état du domaine, l'état d'une vue étant `presentation` ; presentation · external exchange : l'utilisateur reçoit, ou un autre système ; external exchange · synchronisation : un sens, ou les deux côtés ; access · external exchange : un droit dans l'application, ou une permission de la plateforme ; access · calculation : un droit, pas une valeur ; presentation · tout autre : une action de l'utilisateur est un déclencheur, le bloc prend la nature de ce que l'action produit, la réponse visible n'est pas une seconde sortie ; les trois doutes, lus par lui seul — deux phrases produisent deux choses ; une sortie donnable à deux natures ; une frontière qui ne tranche pas.

**Gestes**
1. Appliquer d'abord chaque réponse de son fichier répondu au bloc qu'elle nomme, ouvert même hors liste ; une réponse qui ne règle pas → nouvelle question citant la réponse ; deux réponses laissant le même doute → blocage, les deux citées.
2. Par bloc : ce qu'il produit, dans les mots de la colonne *It produces*, huit réponses possibles ; la nature qui le produit ; la ligne écrite ; tout doute → une entrée, la ligne écrite tout de même — pour deux sorties, celle que le titre nomme.
3. Un bloc nommé dont le `Genre:` n'est plus `comportement` : sa ligne vidée, même plage.
4. Un `MODIFIED` déjà classé : redemander et comparer ; différent → écrire, et le dire.
5. Sur un fichier de blocage : une nature parmi les huit → l'écrire ; réécriture ou retrait → ligne vide, *waits on the Rédacteur* ; hors des huit → ligne vide, dit.
6. Rapporter comptes, liste par bloc, blocs questionnés, blocs bloqués, et les deux lignes qu'un fichier de blocage nommé appelle.

**Branches** — aucune nature ne convient (le bloc ne produit rien), les huit manquent quelque chose, deux réponses ont laissé le même doute → une entrée de blocage ; les autres blocs traités.
**Échange** — écrit `Nature:` que `/4_grille` passe aux sondeurs par nature, que `/5_reclasse` trie, que le Convertisseur lit sans la redériver ; lit la réponse citée dans sa propre `Question:` du tour précédent.
**Bloque** — `blocked_classeur.md`, un `## Blocking N` par bloc ; le Product Owner répond.

**Décisions**
- Au moindre doute, une question, jamais un choix silencieux · écartée : l'asymétrie du qualifieur · raison : une mauvaise nature n'est pas rattrapée, la grille ferme le bloc sur les mauvaises questions et la clôture paraît propre (`classeur.md`, *Role*, *Your questions*) · inconnu.
- La nature est ce que le bloc produit, jamais ce qui le déclenche · écartée : la nature du déclencheur · raison : une action de l'utilisateur est un déclencheur ; un cas d'échec, un capteur, une planification ne nomment pas une nature (`classeur.md`, *The eight natures*) · inconnu.
- La réponse visible à une action n'est pas une seconde sortie · écartée : un doute à scinder · raison : le bloc prend la nature de ce que l'action produit, il n'est pas mal scindé (`classeur.md`, dernière frontière) · inconnu.
- Deux réponses laissant le même doute → blocage · écartée : une troisième question · raison : la question n'est pas la bonne, une troisième la reposerait (`classeur.md`, *Your answered questions*) · inconnu.
- La nouvelle question cite la réponse qu'elle suit · écartée : renvoyer au fichier classé · raison : ce fichier n'est plus nommé, le seul fichier nommé au tour suivant doit porter les deux réponses (`classeur.md`) · inconnu.
- Huit réponses énumérées avant de choisir · écartée : une liste plus courte · raison : une liste courte ferait prendre la plus proche avant de regarder les huit (`classeur.md`, PART 3) · inconnu.

### sondeur, invocation 1 — Angle : la passe A de la grille de cadrage, trois à la fois, un ordre de lecture chacun

Modèle: opus · effort aucun · outils: Read, Grep, Write
Invoquée par: `/4_grille`, premier temps, trois appels dans un seul message, sur les blocs qui ont bougé — ou sur une seule lecture, celle dont la décision vient d'être levée. Les trois ne diffèrent que par `Your reading order:` et le fichier de sortie ; un bloc ici, trois exécutions.
Lit: `desc-produit.md`, les blocs de `Pass A on these blocks:` par leur titre, jamais le fichier entier ; les blocs de `The transverse blocks, to hold beside them:`, tenus à côté ; `.claude/grids/GRILLE_CADRAGE_PRODUIT_V2.md` entière ; le fichier de blocage nommé. Jamais un autre sondeur, jamais un tour précédent.
Écrit: `cadrage-produit/par-bloc.md` (ordre *block by block, in the document's order*), ou `par-question.md` (*question by question*), ou `par-nature.md` (*by nature*) — le chemin que `Write to` nomme, toujours, même vide ; `<out>/blocked_par-bloc.md`, `blocked_par-question.md` ou `blocked_par-nature.md`, dérivé du chemin de sortie.
Valeurs: les trois ordres de lecture — lus (→ MECANISMES §Ordres de lecture des sondeurs — ce qui distingue les trois angles) ; `Genre: comportement` et `transverse` — lus par la liste, jamais greppés ; `NEW` / `MODIFIED` hors de sa liste — ignorés ; `Block:` à un identifiant, `Défaut:` — écrits ; les passes de la grille, lues par lui seul — la grille de cadrage est un test de clôture qui génère ses questions depuis les blocs présents, en trois passes qui lisent des choses différentes : **passe A**, un bloc à la fois, tout ce qu'un bloc ferme seul (A1 fermer le bloc — amont, aval, l'inverse, au-delà de sa sortie ; A2 le rendre codable, par nature ; A3 les blocs sans déclencheur ; A4 le test de clôture) ; **passe B**, les blocs les uns contre les autres, ce qui ne se voit qu'à deux ; **passe C**, la feature une fois. Une clôture appartient à une seule passe ; chaque question porte un identifiant (`A1.3`, `A2.presentation.2`, `C1.5`) que le relevé reprend et qu'une question posée au Product Owner ne cite jamais ; l'angle ne joue que la passe A.

**Gestes**
1. Deux arrêts avant d'écrire : une lecture qui rend moins que demandé (troncature signalée, texte coupé, titre sans corps, rien) ; un identifiant de la liste absent du fichier — la liste est la seule autorité.
2. Suivre l'ordre de lecture exactement ; probe la liste, rien d'autre.
3. Pour chaque question de la passe A portée à un bloc, l'un de trois : le bloc la règle dans ses termes → rien ; il la laisse ouverte → un écart ; elle ne s'applique pas (présuppose une entrée, une donnée, un écran que le bloc n'a pas, ou la grille la borne à une autre nature) → rien, la sortie la plus étroite.
4. Un écart devient une question obligatoire, ou une *défaut* si une règle transverse tenue à côté y répond — la règle citée dans `Défaut:` ; deux règles transverses opposées → obligatoire ; une règle transverse contre une règle du bloc → le bloc gagne, rien.
5. Écrire une entrée par écart — un écart, une question, jamais deux écarts dans une entrée : deux écarts dans une entrée ne peuvent être répondus séparément, et la fusion ne les distingue pas (la règle vaut à chaque invocation qui écrit des questions) — quatre lignes, `Block:` à un seul identifiant, `Défaut:` en cinquième quand elle existe, plus un bloc `Options:` facultatif entre `Question:` et `Défaut:` ou `Answer:`, seul ajout admis (→ MECANISMES §Fichier de questions — divergence) ; en anglais, sans identifiant de grille, sans réponse suggérée dans la `Question:` — les propositions en `Options:`, en français, aucune marquée préférée, le texte de `Défaut:` avant ` — ` reprenant l'une mot pour mot ; le fichier même vide.

**Branches** — un écart qui ne se voit que contre un autre bloc n'est pas à lui : passe B ; ne jamais fermer un écart parce qu'un autre bloc le règle.
**Échange** — écrit `Défaut:` que l'assembleur copie, que le Lexicographe balaie et que le Rédacteur intègre ; écrit le fichier que l'assembleur fusionne.
**Bloque** — `<out>/blocked_<nom>.md`, forme 1 ; un run bloqué n'écrit pas de fichier de questions ; le Product Owner répond ; `/4_grille` relance cette lecture seule.

**Décisions**
- Trois lectures de la même liste, dans trois ordres · écartée : une seule lecture · raison → MECANISMES §Fichiers du cadrage · inconnu.
- « Ne s'applique pas » est la sortie la plus étroite, tout le reste est ouvert · écartée : écarter sur bon sens · raison : c'est la seule issue qui congédie une question sans rien écrire, et un écart parti par là ne revient jamais ; dans le doute, demander (`sondeur.md`, PART 3) · inconnu.
- Réglé veut dire répondu dans les termes de la question, pas le même sujet traité · écartée : interpréter · raison : s'il faut interpréter pour trouver, ce n'est pas là (`sondeur.md`) · inconnu.
- Une *défaut* n'a qu'un fondement, une règle transverse, jamais « les autres blocs font ainsi » · écartée : le motif des autres blocs · raison : une question de passe A tient sur son bloc seul, fermer par les autres est la passe B (`sondeur.md`, *A défaut*) · inconnu.
- Il ne lit jamais la sortie d'un autre sondeur ni ne dévie de son ordre · écartée : se coordonner · raison : un ordre dont on dévie est un ordre que personne n'a couvert ; les quatre écrivent des fichiers différents et ne partagent rien (`sondeur.md`, `/4_grille`) · inconnu.
- Un identifiant nommé absent du fichier arrête · écartée : l'ignorer · raison : la commande a greppé un fichier qui a changé depuis (`sondeur.md`, *Two things stop you*) · inconnu.

### sondeur, invocation 2 — Global : le relevé de chaque comportement, puis les passes B et C

Modèle: opus · effort aucun · outils: Read, Grep, Write
Invoquée par: `/4_grille`, premier temps, dans le même message que les trois angles, sur chaque comportement, chaque tour.
Lit: `desc-produit.md`, chaque bloc de `every behaviour block:` par son titre ; les blocs transverses et `The out-of-scope blocks:` ; `GRILLE_CADRAGE_PRODUIT_V2.md` entière, dont la liste *What pass A left you* qui dicte les colonnes du relevé ; le fichier de blocage nommé.
Écrit: `cadrage-produit/releve.md` — un `## B<n>` par bloc dans l'ordre du fichier, une ligne par identifiant de croisement que la grille liste, dans son ordre, `—` quand rien ; `cadrage-produit/global.md`, ses questions, même vide ; `cadrage-produit/blocked_global.md`.
Valeurs: `Genre: comportement`, `transverse`, `hors périmètre` — lus par les listes ; `Block:` à plusieurs identifiants pour un croisement, `Block: -` pour la passe C, un identifiant pour une contradiction avec un bloc hors périmètre — écrits ; `C1.2`, lue par lui seul : la question de la passe C que les blocs hors périmètre répondent, non reposée sur ce qu'ils couvrent, posée sur ce qu'ils ne couvrent pas.

**Gestes**
1. Le relevé : pour chaque bloc, les réponses que la passe B croise, colonnes prises de la grille, jamais de mémoire ; une ligne à `—` jamais sautée ; enregistrer sans questionner.
2. La passe B depuis le relevé seul, une colonne rassemblée sur tous les blocs puis croisée — jamais les blocs de nouveau.
3. La passe C, une fois, sur la feature ; les blocs hors périmètre répondent `C1.2` ; un bloc de la feature qui fait ce qu'un bloc hors périmètre exclut est une contradiction, question obligatoire, `Block:` au bloc de la feature, le bloc exclu nommé dans les mots de la question, jamais une *défaut*.
4. Écrire `global.md`, même vide.

**Branches** — les mêmes arrêts avant écriture qu'à l'invocation 1.
**Échange** — écrit `releve.md` que `/4_grille` archive ; écrit `global.md` que l'assembleur fusionne.
**Bloque** — `cadrage-produit/blocked_global.md` ; rien d'autre écrit.

**Décisions**
- La passe B depuis le relevé, jamais les blocs · écartée : relire les blocs · raison : une colonne rassemblée montre en une fois ce que soixante relectures montreraient (`sondeur.md`, invocation 2 ; grille, *What pass A left you*) · inconnu.
- Les colonnes du relevé prises de la grille · écartée : une liste dans l'agent · raison : un croisement ajouté à la grille est une colonne que le relevé doit porter, un exemple figé vieillirait (`sondeur.md`) · inconnu.
- Une contradiction avec un bloc hors périmètre est au global et obligatoire · écartée : une *défaut* · raison : la Product Owner règle lequel des deux tient ; le global seul tient les blocs exclus (`sondeur.md`, *The out-of-scope blocks beside you*) · inconnu.

### sondeur, invocation 3 — Existant : la feature contre ce qui est déjà bâti

Modèle: opus · effort aucun · outils: Read, Grep, Write
Invoquée par: `/4_grille`, second temps, seule, une fois le premier temps clos, quand au moins un bloc porte `Global:`.
Lit: `desc-produit.md`, les blocs de `These blocks, with the global section each names:` ; `.claude/grids/GRILLE_EXISTANT.md` entière ; `docs/PRODUIT_GLOBAL.md`, les seules sections que les lignes `Global:` nomment, par grep du titre, une section chargée une fois (→ MECANISMES §Lecture du global par l'index) ; `blocked_existant.md` nommé.
Écrit: `questions-existant-NN.md` à la racine, le chemin du prompt, même vide ; `blocked_existant.md`, le chemin du prompt.
Valeurs: `Block:` à un identifiant, le bloc de la feature qui heurte, jamais un bloc du global — écrit ; jamais de `Défaut:` ; les deux côtés de l'arbitrage en `Options:`, en français ; la grille de l'existant, lue par lui seul : un test de clôture sur ce que la feature *heurte*, non sur ce qu'elle laisse ouvert — E1 ce que le bloc prend et qu'autre chose tient déjà, E2 ce que le bloc dit et que la section dit autrement, E3 ce que la feature retire sans le dire, E4 le test de clôture, une passe de E1 à E3 pour chaque bloc à `Global:` contre sa propre section ; chaque question est un arbitrage, deux choses vraies à la fois qui ne peuvent rester.

**Gestes**
1. Porter chaque question de la grille au bloc et à la section qu'il nomme, ensemble ; ni l'un ni l'autre ne répond seul.
2. Une question par collision, la section du global nommée dans les mots de la question ; jamais proposer qui gagne.
3. Écrire le fichier, même vide.

**Branches** — un bloc attaché à rien n'est pas nommé : rien à heurter.
**Échange** — lit `Global:` que le Rédacteur écrit ; écrit `questions-existant-NN.md` que `/1_lexique` puis `/2_structure` intègrent et que `/5_reclasse` teste.
**Bloque** — `blocked_existant.md` à la racine ; `/4_grille` relance le second temps, le fichier nommé, et le renomme `-NN`.

**Décisions**
- Jamais de *défaut* ici · écartée : proposer · raison : ce que le corpus tient est précisément ce qui est en conflit (`sondeur.md`, invocation 3) · inconnu.
- Seules les sections nommées, jamais le global entier · écartée : le lire · raison : le global dépasse 250 Ko, et ce à quoi aucun bloc ne s'attache ne peut être heurté (`GRILLE_EXISTANT.md`, E4 ; `sondeur.md`) · inconnu.
- `Block:` au bloc de la feature, jamais un bloc du global · écartée : l'identifiant du global · raison : la chaîne n'adresse pas le global par identifiant, le numéro ne passe pas dans le global (`sondeur.md`, `redacteur.md`) · inconnu.

### assembleur — fusionner les quatre fichiers de questions en un

Modèle: sonnet · effort aucun · outils: Read, Write
Invoquée par: `/4_grille`, une fois les quatre sondeurs du premier temps rapportés et leurs quatre fichiers présents ; seule sur une décision levée de `blocked_assembleur.md`.
Lit: `cadrage-produit/par-bloc.md`, `par-question.md`, `par-nature.md`, `global.md`, entiers ; le fichier de blocage nommé. Jamais le fichier produit, jamais la grille.
Écrit: `cadrage-produit/questions.md`, renuméroté de `Q1` dans l'ordre des identifiants de `Block:`, `Block: -` en dernier, tout copié mot pour mot, `Défaut:` et `Options:` avec leur question, jamais déplacées ni fondues, `Answer:` vide ; `blocked_assembleur.md`.
Valeurs: `Block:` — lu et copié ; la seule ligne qu'il écrit jamais, celle qu'un `## Decision` rempli donne à une question implaçable ; le test de fusion, lu par lui seul — dans un groupe, deux questions sont une quand répondre à l'une répond à l'autre ; on garde la couvrante, celle dont la réponse ferme l'autre, la formulation ne tranche que quand chacune ferme l'autre ; dans le doute, les deux ; un fichier vide est un fichier sans `### Q` et sans prose.

**Gestes**
1. Un fichier manquant → arrêt, le fichier nommé dans le rapport, rien sur disque — ce n'est pas un blocage.
2. Une question sans `Block:` lisible, ou un fichier qui n'est ni vide ni une liste de questions en forme (de la prose, un `### Q` sans ses lignes) → blocage.
3. Grouper bloc par bloc, sur tous les fichiers ; une ligne à plusieurs identifiants entre dans chaque groupe ; une question gardée une fois ; dropée seulement contre une jumelle dont `Block:` nomme chacun de ses blocs ; `Block: -` fusionnés à la fin ; jamais entre groupes.
4. Une `Défaut:` sur la question qu'on droperait garde les deux ; jamais déplacée.
5. Écrire le fichier, même vide, sauf blocage ou arrêt ; le rapport porte `Files merged:`, `Questions in:`, `Questions out:`, `Dropped as duplicates:`.

**Branches** — un blocage nommé donne le `Block:` d'une question implaçable, écrite comme la décision le dit.
**Échange** — écrit `questions.md` que `/4_grille` copie ; son rapport à quatre comptes est ce que `/4_grille` relaie.
**Bloque** — `blocked_assembleur.md` à la racine ; un run bloqué n'écrit pas de fichier de questions ; le Product Owner répond ; `/4_grille` relance la fusion seule.

**Décisions**
- Ne dropper que ce qu'une réponse fermerait deux fois, jamais un écart levé une fois · écartée : garder ce qui fait consensus · raison : l'union de ce que les lectures lèvent est la sortie, l'accord n'est pas le test (`assembleur.md`) · inconnu.
- Jamais réécrire, jamais fusionner deux questions en une phrase · écartée : condenser · raison : le fichier est ce que le Product Owner répond, et sa seule lectrice devrait le retoucher (`assembleur.md`) · inconnu.
- Une question à plusieurs blocs n'est pas dropée contre une à un bloc · écartée : dropper sur le recouvrement · raison : un bloc disparaîtrait du fichier et qui place par `Block:` ne le toucherait jamais (`assembleur.md`, *How you merge*) · inconnu.
- Un fichier manquant est un arrêt sans fichier, pas un blocage · écartée : bloquer · raison : rien n'est à trancher par le Product Owner, c'est l'orchestration qui répare (`assembleur.md`, *Where you work*) · inconnu.
- De la prose sans `### Q` est un arrêt · écartée : la lire comme vide · raison : un sondeur qui écrit au lieu de classer rapporte peut-être une trouvaille mal formée ; une question perdue coûte un cycle (`assembleur.md`) · inconnu.
- Les comptes dans le rapport, pas dans le fichier · écartée : un en-tête dans `questions.md` · raison : la commande devrait le retirer avant la Product Owner, une édition de contenu qu'elle ne peut faire (`assembleur.md`, *The count goes in your report*) · inconnu.

### convertisseur, invocation 1 — Nature : écrire la section d'une nature

Modèle: opus · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/6_convertit`, une fois par nature qui tourne, toutes dans un seul message.
Lit: `convertisseur/<nature>-input.md`, ses blocs, entiers, une fois ; les titres de `desc-produit.md` par grep ; `.claude/grids/GRILLE_FERMETURE_TECHNIQUE.md` ; `convertisseur/technique-<nature>.md` répondu quand le prompt le nomme ; `questions/convertisseur/questions-convertisseur-NN.md` quand le prompt le nomme ; `convertisseur/blocked_<nature>.md` nommé. Jamais le fichier produit entier, jamais une autre nature, jamais `par-genre/transverses.md`, jamais le global.
Écrit: `convertisseur/<nature>.md`, la section entière à chaque fois, `## §<n> <Title>` puis `### §n.m <titre>` dans l'ordre des blocs, chaque entrée finissant par `Consumes:` (→ MECANISMES §Ligne Consumes:), les références hors section en `[B<n>: <ce qu'on en attend>]` ou `[B?: <titre>]` (→ MECANISMES §Marques <<ASSUMED et [B) ; `convertisseur/<nature>-notes.md` — `## Trace` une ligne par bloc, ses entrées ou un tiret ; `## Preamble` les références marquées *existing* ; `convertisseur/questions-<nature>.md`, toujours ; `convertisseur/technique-<nature>.md`, sur une question technique ; `convertisseur/blocked_<nature>.md`.
Valeurs: les huit natures et leurs sections §1–§8 — lues, la nature reçue du prompt, jamais redérivée (→ MECANISMES §Les huit natures — la nature d'un bloc) ; `<<ASSUMED B<n>: …>>` — écrit ; `Block:` d'une question produit, `Entries:` d'une question technique — écrits ; `blocking` · `assumed` · `misplaced`, écrits dans le rapport par lui seul, aucune commande ne les lit : `blocking` — sans la réponse la règle n'existe pas, ni section ni notes, la question écrite ; `assumed` — la règle s'écrit en supposant, produite et marquée ; `misplaced` — la règle appartient à une autre couche, laissée hors de la section, marquée en fin de section ; le test de réversibilité, lu par lui seul — un choix qu'on peut défaire sans toucher le produit, il le règle (renommer, comment couper une règle en entrées et où la placer dans sa section, une comparaison, deux noms pour une entité) ; un choix qui contraint ce que l'application pourra faire, il le demande (deux concepts distingués fusionnés, ou l'inverse) ; les fermetures *by nature* de la grille de fermeture technique, lues par lui seul — *Traceability* (peut-on pointer la phrase produit d'où la règle suit ; ce qu'il faudrait ajouter est une question), *Nothing dropped* (chaque phrase de chaque bloc est dans une entrée), *Completeness* (aucun cas laissé ouvert), *What a nature owes* ; jouées sur la section une fois écrite, jamais en écrivant.

**Gestes**
1. Lire ses blocs, et son fichier de questions répondu quand nommé, avant d'écrire ; une réponse est ce qui lève la marque posée au tour précédent, le bloc lisant comme avant.
2. Écrire la section : reformuler en règle exécutable sans rien décider de neuf ; une entrée, une règle ou une table, coupée en deux quand deux règles complètes en sortent ; jamais un numéro hors de sa section.
3. Écrire les notes.
4. Jouer les fermetures *by nature* ; chaque échec traité par *What a question costs* — `blocking`, `assumed`, `misplaced`.
5. Écrire le fichier de questions, toujours ; une question technique dans `technique-<nature>.md`, `Entries:` à la place de `Block:` ; une `**Clarification needed:**` survivante est un signal.

**Branches** — un `No` (`blocking`) → ni section ni notes, la question seule ; une règle d'une autre couche → hors section, `<<ASSUMED B<n>: …>>` en fin de section, la question demandant ce que fait la règle, jamais quelle couche ; un titre que le produit nomme sans identifiant → `[B?: <titre>]`, `Block:` au bloc qui référence.
**Échange** — écrit `## Trace` que `/6_convertit` et l'invocation 2 lisent pour résoudre et pour `tracabilite.md` ; écrit `## Preamble` que l'invocation 2 lit pour `## Dependencies` ; lit *existing* que le Rédacteur écrit ; écrit `<<ASSUMED` que `/6_convertit` greppe et sur lequel le Cadreur s'arrête.
**Bloque** — `convertisseur/blocked_<nature>.md`, forme 1 ; un blocage finit l'invocation, rien d'autre écrit ; une décision ne réécrit jamais le fichier produit.

**Décisions**
- Il ne règle jamais une matière produit, il n'est pas le filet de l'amont · écartée : corriger en passant · raison : la grille a balayé, le classeur a classé ; il traduit ce qu'ils ont fermé (`convertisseur.md`, *Role*) · inconnu.
- Une nature par invocation, la section entière réécrite · écartée : patcher une section · raison : jamais une section laissée par un run antérieur ; une section est renumérotée à chaque écriture, avant le découpage seulement (`convertisseur.md`, *Numbering*, mouvement 2) · inconnu.
- Jamais un numéro hors de sa section, une référence entre crochets avec l'attente · écartée : deviner le numéro voisin · raison : jusqu'à huit sections s'écrivent en même temps ; un `[B12]` nu laisse deviner qui résout (`convertisseur.md`, *A reference to another section*) · inconnu.
- Un `No` n'écrit ni section ni notes · écartée : écrire et supprimer · raison : jamais une section qu'on supprimera, ni des notes nommant des entrées inexistantes ; la commande n'assemble rien (`convertisseur.md`, *What a question costs*) · inconnu.
- Une question technique et une question produit ne voyagent pas par la même route · écartée : un seul fichier · raison : une réponse technique ne change aucun bloc, rien en amont n'est rejoué ; c'est un choix que la Product Owner doit valider, non qu'elle ne peut pas (`convertisseur.md`, *Two kinds of question*) · inconnu.
- Une seule marque `<<ASSUMED`, pour une attente produit comme technique · écartée : deux marques · raison : ce qu'elle dit au Cadreur est le même, *cette entrée attend* ; laquelle est dans le fichier de questions (`convertisseur.md`) · inconnu.
- La question d'une règle mal placée demande ce que fait la règle, pas la couche · écartée : demander la couche · raison : la Product Owner ne peut arbitrer une couche, et une question qu'elle ne peut répondre coûte un tour (`convertisseur.md`, *A rule that belongs to another layer*) · inconnu.
- Il ne groupe rien en unités de travail · écartée : préparer les lots · raison : le Cadreur groupe avec l'état et les symboles sous les yeux, un groupement ici déciderait pour lui à l'aveugle (`convertisseur.md`) · inconnu.
- Les choix réglés dits dans le rapport, jamais dans le document · écartée : une note dans l'entrée · raison : une entrée est quatre lignes ou une règle, le bloc `Options:` seul ajout admis, une autre ligne casse la forme que chaque lecteur attend (`convertisseur.md`) · inconnu.

### convertisseur, invocation 2 — Transversal : le préambule, §9 Text, les références, la traçabilité

Modèle: opus · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/6_convertit`, chaque fois qu'un document a été assemblé, une fois.
Lit: `spec-technique.md` entier ; chaque `convertisseur/*-notes.md` ; `par-genre/transverses.md`, `references.md`, `hors-perimetre.md` ; les titres du fichier produit ; `GRILLE_FERMETURE_TECHNIQUE.md` ; `convertisseur/technique-transversal.md` nommé ; `convertisseur/blocked_transversal.md` nommé.
Écrit: `spec-technique.md` complété — `# Preamble` et ses quatre parties `## Intent and vocabulary`, `## Out of scope`, `## Cross-cutting rules`, `## Dependencies`, écrites même vides (→ MECANISMES §Fichiers de la conversion) ; les entrées de la moitié code des règles transverses, au numéro libre suivant de la section de leur couche ; `## §9 Text` depuis `references.md` ; l'entrée *Resources* ; les crochets restants résolus ; `convertisseur/transversal-record.md` (`## Trace`, `## Preamble`, pour les blocs transverses et de référence) ; `tracabilite.md` (→ MECANISMES §tracabilite.md) ; `convertisseur/questions-transversal.md`, toujours ; `technique-transversal.md` sur une question technique ; `blocked_transversal.md`.
Valeurs: les six genres par les trois fichiers `par-genre/` qu'il lit — `transverse`, `référence`, `hors périmètre` — trois valeurs sur six, les trois autres jamais lues ; `Consumes: ## Cross-cutting rules` — écrit ; la scission d'une règle transverse, lue par lui seul — le test : si personne ne l'écrit, manque-t-il quelque chose au code ? oui → une entrée numérotée dans la section de sa couche (la pièce partagée : un formateur, une comparaison) ; et la contrainte (*chaque bloc soumis l'applique*) sous `## Cross-cutting rules` ; une règle sans code ne donne que la contrainte ; les neuf sections — §1 Model, §2 Persistence, §3 Calculation, §4 Transition, §5 External exchange, §6 Synchronisation, §7 Presentation, §8 Access, §9 Text — §9 sans nature, écrite par lui seul ; les fermetures *across sections* de la grille, lues par lui seul — *Declared links* (chaque référence, celles que la commande a résolues comprises), *Singularity*, *Agreement between entries* (le document entier, un balayage), *Resources* (la seule qui écrit : une entrée que rien ne porte et dont le produit a réglé le contenu, en fin de section, numéro suivant, avec sa `Consumes:`, et son numéro sur la `Consumes:` de chaque entrée qui en a besoin).

**Gestes**
1. Lire le document et chaque fichier de notes.
2. Le préambule, quatre sources, rien de déduit : les titres du produit ; `hors-perimetre.md` entier ; la moitié contrainte de chaque bloc de `transverses.md` ; les lignes `## Preamble` des notes.
3. 2b : scinder chaque règle transverse, écrire sa moitié code comme entrée dans la section de sa couche ; écrire le record entier — `## Trace` l'entrée ou un tiret, `## Preamble` le bloc dont la contrainte est sous `## Cross-cutting rules`. 2c : §9 Text depuis `references.md`, une entrée par table ou catalogue, ses lignes dans le record ; les clés des libellés cités sont à *Resources*.
4. Résoudre ce qui reste entre crochets par la ligne `## Trace` du bloc — les notes pour un comportement, le record pour un transverse ou une référence — l'entrée qui porte ce que les crochets attendent ; sinon, dans l'ordre : la ligne `## Preamble` (résolu au nom de la partie, `## Dependencies` ou `## Cross-cutting rules`), tenir pour le mouvement 4, ou une question, les crochets laissés ; un `[B?: …]` laissé ; un comportement sans `## Trace` ni `## Preamble` est une faute de l'invocation 1, dite, les crochets laissés.
5. Jouer les fermetures *across sections* une fois sur le document entier ; *Resources* écrit ; tout le reste touché est une référence, jamais une règle réécrite.
6. Grep `[B` après le mouvement 4 : ce qui reste est une question écrite ou une référence manquée.
7. `tracabilite.md`, une ligne par bloc, tous, dans l'ordre du produit.
8. Le fichier de questions, toujours ; le rapport dit tout comportement sans ligne de trace ni de préambule.

**Branches** — un `No` ici → ni préambule ni traçabilité, la question écrite, arrêt.
**Échange** — écrit `## Cross-cutting rules` que le Cadreur ne coupe jamais et que `/9_controle` nomme pour un `transverse` ; écrit `tracabilite.md` que `/6_convertit` compare, que l'Architecte lit au mouvement 2, que `/9_controle` lit en phase 1 ; écrit les `Consumes:` que le Cadreur lit pour `Needs` et l'Architecte comme graphe.
**Bloque** — `convertisseur/blocked_transversal.md` ; rien d'autre écrit.

**Décisions**
- La scission des règles transverses à l'invocation 2 seule · écartée : chaque nature scinde · raison : huit natures écriraient huit fois la même contrainte, deux pourraient réclamer une règle ou aucune ; un lecteur, un scripteur — coût et unicité, non impossibilité (`convertisseur.md`, *A transverse rule splits in two*) · inconnu.
- Le record sous un nom qui n'est pas `-notes.md` · écartée : `transversal-notes.md` · raison : la commande résout les cibles uniques depuis `*-notes.md` avant le run, et un record d'un run précédent résoudrait vers un numéro pas encore écrit (`convertisseur.md`, 2b) · inconnu.
- Jamais résoudre vers une cible qui ne répond pas de ce qu'on attend · écartée : le numéro le plus proche · raison : un crochet laissé arrête le découpage, un mauvais numéro se lit comme réglé (`convertisseur.md`, mouvement 3) · inconnu.
- Il ne réécrit jamais une règle d'une invocation de nature · écartée : corriger en passant · raison : il redéciderait à l'aveugle ce qu'une nature a décidé avec ses blocs devant elle ; une règle qu'il trouve fausse est une question (`convertisseur.md`, *What you never do*) · inconnu.
- Un tiret dans `tracabilite.md` pour un bloc sans entrée, jamais une ligne absente · écartée : ne lister que les blocs à entrées · raison → MECANISMES §tracabilite.md · inconnu.
- Le rapport ne nomme jamais la commande suivante · écartée : la suggérer · raison : dire ce qu'on a trouvé, pas quoi en faire (`convertisseur.md`, *What you report*) · inconnu.

### architecte — ce qui vaut pour ses quatre invocations

L'Architecte est décrit en entier ici parce que `/conventions` l'invoque en premier dans un parcours nominal (invocation 1 ou 4, avant `/7_lots`) ; `/7_lots`, `/8_code` et l'Arbitre invoquent son invocation 3 plus tard, et `PROCESS_AVAL.md` en porte l'entrée courte (`### architecte — invocation depuis /7_lots`, `… depuis /8_code`, `… depuis arbitre`). Ce qui vaut pour les quatre :

- Il lit `.claude/grids/GRILLE_CONVENTIONS.md` en entier à chaque invocation. La grille est un test de dérivation, pas un catalogue : ni le fichier produit ni le document technique ne tiennent une convention, et ce qu'il cherche est où deux entrées pourraient se bâtir différemment. Elle se lit en trois temps — *How this grid is applied*, sept règles R1–R7 (R1 un déclencheur que le corpus ne satisfait pas n'écrit rien ; R2 un trou que les deux documents ne remplissent pas n'écrit rien, une question à la place ; R3 une règle hors grille est permise et marquée `off-grid` ; R4 il n'amende jamais la grille, une forme manquante est une question `Kind: forme` ; R5 une liste ne permet jamais ce qu'elle omet ; R6 une forme à deux clauses citées est deux règles ; R7 une règle qui en resserre une autre s'écrit dans les deux) ; *Part A — Readings*, dix lectures V1–V10 établies une fois sur le corpus, qui ne produisent aucune règle et nourrissent la partie B (V1 les natures non vides et leur compte, V2 le graphe `Consumes:` agrégé par nature et son acyclicité, V3 les racines et les entrées consommées par plus de cinq, V4 le lexique, V5 l'accord des nombres, V6 la couverture croisée bloc ↔ entrée dans les deux sens, jouée avant tout, V7 les paires d'entrées consommant une même entrée avec des attentes divergentes, V8 les quantités à unité, échelle, identité, V9 les sources ambiantes, V10 les écritures déclarées avant retour) ; *The shape of the file* ; *Part B — Rule entries*, douze sections C1–C12 (gouvernance, vérification, frontières, structure et direction des dépendances, contrats d'interface, erreurs, état et effets, configuration et secrets, diagnostics, tests, nommage et langue, dépendances et versions), chaque entrée portant question, déclencheur, forme à trous `< >`, test ; trente-sept entrées — les trente-six restées après le retrait, plus G12.6 venue depuis, qui porte ce que tenait G12.1 de l'archive, restée retirée — une trentaine de règles attendues.
- `docs/TECHNICAL_CONVENTIONS.md` : douze sections numérotées dans l'ordre de la grille, une section vide écrite, jamais omise ; chaque règle `R<n> · <règle> · <permanente | spécifique> · <mechanical | review>`, `off-grid` en cinquième champ ; une seule séquence de numéros, jamais réattribuée, une règle retirée garde son numéro (→ MECANISMES §permanente / spécifique — ce qui déclenche une règle, §Identifiants). `mechanical` · `review` — le quatrième champ, écrit par lui seul, lu par personne qui l'énumère : `mechanical` quand un outil nommé en C12 le vérifie, `review` sinon ; `off-grid` — le cinquième, écrit par lui seul : une règle que la grille n'a pas tirée, ses entrées motivantes sur sa ligne de `couverture.md`, jamais sur la règle. Trois sortes sont toujours `permanente` : où vit une sorte de symbole, les commandes qui compilent, analysent, testent, les états de livraison d'un lot — la grille tire les deux dernières toujours, par G2.1, et la table de G4.4 dit où va le code de chaque module. La structure du projet, chaque fait une fois, dans la section qui possède sa sorte : en C2 la table des commandes de G2.1 — `compile`, `test`, `analyse`, une ligne `assemble <module>` par module application —, chacune lancée telle qu'écrite depuis la racine du dépôt, un lot livrable seulement quand toutes sortent à 0 ; en C4 la table des modules de G4.4 — nom, sorte (`application`, `library`, `plain code`), sur quoi il tourne, ses dépendances, son espace de noms, son dossier de code, son dossier de test, l'identifiant d'application d'un module application ; en C12 la table de versions de G12.6 — le langage, le système de build et comment il s'obtient, la chaîne d'outils, les niveaux de plateforme là où elle en a, le framework de test, les fichiers de build. Une règle dont la forme est une table la porte sous sa ligne, son numéro tient chaque rangée. Ces trois règles sont le seul endroit où il nomme une commande, un dossier, un fichier de build. Sur quoi tourne chaque module est au produit, lu dans le corpus, jamais choisi : un corpus qui ne nomme rien laisse G4.4 non écrite, et tout trou qui en découle — une question `coverage`, R2, son `Block:` nommant `G4.4` ; le reste est son appel, une directive qui en nomme un le règle, placée au mouvement 6b.
- `couverture.md`, à la racine de la feature même sur un `bugfix-NN/` : une ligne par entrée du document technique dans son ordre — `§n.m   <nature>   → R12, R33` ou `→ no rule` écrit en toutes lettres, `; Q1` pour une question ; ses mentions, écrites et relues par lui seul : `corrigé` · `question ouverte` (ce qu'est devenue une `inconsistency`), `grille amendée` · `question ouverte` (une `forme`), `requête` (une règle née d'une requête, le nom du fichier de requête en première colonne, `— Request N` ou le préfixe `bugfix-NN/`), `directive` (une règle née d'une directive, le bloc en première colonne), `no rule`. Une seule table, aucun texte de règle, aucune sorte de test.
- `questions-architecte-NN.md` à la racine du dossier de travail, cinq lignes par entrée, `Kind:` entre `Block:` et `Question:` (→ MECANISMES §Les cinq Kind: — la sorte d'une question de l'Architecte), plus un bloc `Options:` facultatif entre `Question:` et `Answer:`, seul ajout admis — des propositions, aucune marquée préférée (→ MECANISMES §Fichier de questions — divergence) ; le numéro reçu du prompt, il ne liste jamais un dossier.
- Le web aux invocations 1, 3 et 4 : un fait de plateforme est cherché, jamais rappelé. Le code à aucune invocation ; les fichiers de build à la seule invocation 3, ceux que les conventions nomment — la table de versions de G12.6 —, jamais globés.
- Le rapport : quatre lignes au plus plus une par question `coverage` — les fichiers écrits, combien de règles et combien `off-grid`, combien de questions et de quelle sorte (zéro dit), chaque `coverage` en une ligne, une directive qui a écrasé une règle, une `inconsistency` à corriger en amont, une `forme`, un `replacement` et dans quel sens.
- Il ne bloque que dans deux cas : une entrée manquante (pas de document technique, un document sans entrée, et aux invocations 2, 3, 4 pas de `docs/TECHNICAL_CONVENTIONS.md` — le pire, son `## To resume` étant « run `/conventions`, invocation 1 ») ; une directive qu'il ne peut placer sans la changer. Jamais quand l'Arbitre l'appelle. Sur reprise, il cherche `blocked_architecte.md` d'abord ; `## Decision` vide → réécrit inchangé, arrêt ; rempli → appliqué, dit ; sur une directive, la décision est soit la directive reformulée, placée telle quelle, soit la règle en entier, écrite telle quelle — aucune ne change le fichier produit (→ MECANISMES §Reprise sur décision — divergence, variante B).

**Décisions communes**
- La grille lue entière, à chaque invocation, et jamais amendée · écartée : une grille dans l'agent · raison : la grille tient les lectures et les entrées, l'agent tient les mouvements ; R4, un amendement est une question `forme` que la Product Owner applique (`architecte.md`, *What you read* ; `GRILLE_CONVENTIONS.md` R4 ; `docs/verification4/plan.md` entrée 20) · non éprouvée.
- Aucun outil `Bash`, aucun code lu, jamais un dossier listé sauf `architecte/` à 3 · écartée : lire le code pour savoir ce qu'un outil produit · raison : il nomme les outils, il ne les trouve pas ; ce qu'il trouverait en listant est ce qu'il ne doit pas lire (`architecte.md`) · inconnu.
- Le web plutôt que la mémoire · écartée : rappeler · raison : une règle écrite d'un faux souvenir est lue par chaque lot de chaque feature (`architecte.md`) · inconnu.
- Il n'attend jamais la Product Owner · écartée : sonder · raison : il règle, refuse ou bloque, et sort ; l'attente est le travail de l'Arbitre (`architecte.md`, *What you never do*) · inconnu.
- Aucune provenance dans le fichier de conventions, tout dans `couverture.md` ; une seule table · écartée : deux tables ; la sorte de test dans la couverture · raison : une règle citée en deux fichiers vieillit dans l'un ; la sorte de test est sur la règle, où est son lecteur (`architecte.md`, *The coverage file*) · inconnu.
- La structure du projet déclarée par trois entrées, chacune dans la section qui possède sa sorte — les commandes en C2 (G2.1), la table des modules en C4 (G4.4), la table de versions en C12 (G12.6) — et tirées toujours · écartée : une section nouvelle qui répète C2, C4 ou C12 ; une seule commande de vérification ; une liste de noms de modules · raison : des conventions écrites sans elles ont nommé des modules jamais construits et une commande de vérification qui n'existait pas, rien ne les confrontant à un vrai projet ; ce sur quoi tourne un module reste au produit, un trou du corpus est une question, jamais un défaut (`GRILLE_CONVENTIONS.md` G2.1, G4.4, G12.6 ; `architecte.md`, *The project's structure*) · non éprouvée.
- `no rule` écrit en toutes lettres · écartée : une ligne absente · raison : c'est ce qui sépare une entrée regardée d'une entrée manquée (`architecte.md`) · inconnu.
- Une directive qu'il ne peut placer bloque, jamais une question · écartée : une question ; une ligne de rapport · raison : une directive vit dans un bloc et le changer est au Rédacteur, une réponse ici n'atteindrait aucun bloc ; un rapport est lu une fois et perdu, alors que la règle non vérifiable serait lue par chaque lot (`architecte.md`, *The directives*) · inconnu.

### architecte, invocation 1 — Deriving : la première dérivation du dépôt

Modèle: opus · effort high · outils: Read, Grep, Glob, WebSearch, WebFetch, Edit, Write
Invoquée par: `/conventions`, quand `docs/TECHNICAL_CONVENTIONS.md` n'existe pas ; prompt `Working folder: docs/features/<name>/. Invocation 1 — Deriving. Your questions file number: NN.`
Lit: `desc-produit.md` entier ; `spec-technique.md` entier, préambule compris ; `tracabilite.md`, pour le mouvement 2 seul ; `par-genre/directives.md` ; le web ; la grille ; `blocked_architecte.md` nommé. Aucun fichier de conventions, sous aucun nom — pas `TECHNICAL_CONVENTIONS.md`, pas un fichier au nom de *convention*, *rule*, *guideline*, pas un que lui-même a laissé.
Écrit: `docs/TECHNICAL_CONVENTIONS.md` à neuf ; `couverture.md` ; `questions-architecte-NN.md`, toujours, même vide ; `blocked_architecte.md`, `## Invocation` 1.
Valeurs: les six genres — lus dans `desc-produit.md`, `comportement` et `référence` pour le tiret qui lève `inconsistency`, `directive`, `hors périmètre`, `recette`, `transverse` pour le tiret qui ne lève rien ; les huit natures — lues, seconde colonne de `couverture.md` ; `Kind:` — écrit, `coverage`, `conjunction`, `inconsistency`, `forme` (jamais `replacement` ici) ; les quatre sortes d'écart, lues par lui seul — coverage, une question de comportement que le corpus ne répond nulle part, marquée question produit ; conjunction, entre deux entrées complètes, le long d'une arête de `Consumes:` ; inconsistency, le corpus se contredit ; precision, réglée à un grain plus fin que le produit — il la règle lui-même, la seule qui ne sort pas.

**Gestes**
1. Charger la grille ; aucune forme hors grille, sauf R3.
2. Apparier les deux documents par `tracabilite.md` : un bloc `comportement` ou `référence` à ligne en tiret → `inconsistency` (le document ne porte pas ce que le produit demandait) ; une entrée qu'aucune ligne ne nomme → `inconsistency` (le document porte ce que le produit n'a pas demandé) ; un tiret d'un autre genre ne lève rien ; sans `tracabilite.md`, apparier sur les titres et le dire dans le fichier de questions.
3. Établir V1 à V10, V6 exclue (le mouvement 2 l'a faite) — brouillon, sans lecteur.
4. Lever chaque anomalie que la partie A nomme (un cycle en V2, des nombres qui divergent en V5, des paires en V7) — l'anomalie et les identifiants, jamais la réponse.
5. Marcher la partie B, C1 à C12 : chaque entrée dont le déclencheur tire, ses trous remplis depuis une lecture, la pratique de la plateforme ou son propre appel ; un trou que rien ne remplit n'écrit rien, une question.
6. Les règles hors grille, quand le corpus énonce ce que le code doit honorer et qu'aucune entrée n'en fait une règle ; `off-grid`, ses entrées sur sa ligne de couverture.
7. 6b : intégrer `par-genre/directives.md` — une règle dit la même chose → rien ; plus large ou voisine → fusion, ses mots gagnent ; rien ne la couvre → une règle, `permanente` ou `spécifique`, sa ligne de couverture au bloc avec `directive` ; une règle la contredit → la directive gagne, dit dans le rapport ; ne se place pas → blocage.
8. Écrire le fichier de conventions, sans provenance.
9. Écrire `couverture.md`, une ligne par entrée dans l'ordre.
10. Vérifier la couverture : chaque identifiant du document exactement une fois ; un manquant → retour au mouvement 5 pour ces entrées seules, les fichiers amendés.
11. Le fichier de questions, toujours ; le rapport.

**Branches** — une `coverage` ne devient jamais une règle : levée, marquée, le travail continue jusqu'au bout ; dans le doute entre coverage et precision, lever.
**Échange** — lit `tracabilite.md`, `Consumes:`, *existing* du Convertisseur ; lit `par-genre/directives.md` de `/5_reclasse` ; écrit le fichier que tout l'aval lit (→ MECANISMES §Lecture des conventions — divergence).
**Bloque** — `blocked_architecte.md`, forme 2 ; le Product Owner répond ; `/conventions` le nomme sur la forme que `## Invocation` dit.

**Décisions**
- Aucun fichier de conventions ouvert à l'invocation 1 · écartée : comparer, vérifier la forme · raison : lire ce qu'un autre a décidé serait dériver de sa propre sortie ; la grille et les deux documents sont tout ce dont il dérive (`architecte.md`, *What you read*) · inconnu.
- Le tiret ne questionne que sur `comportement` et `référence` · écartée : chaque tiret · raison → MECANISMES §tracabilite.md (`docs/verification3/plan.md` entrée 31) · inconnu.
- La coverage est une question produit, jamais une règle · écartée : régler le comportement dans les conventions · raison : par définition la grille de cadrage n'a pas fermé le produit ; un comportement décidé ici n'atteint ni fichier produit ni global (`architecte.md`, *A coverage gap is a product question*) · inconnu.
- Il règle lui-même le choix technique, jamais un comportement · écartée : demander chaque choix · raison : le produit dit ce que fait l'application, le document ce qui doit exister, le choix suit des deux plus la pratique de la plateforme (`architecte.md`, *What you settle, and what you ask*) · inconnu.
- Les directives intégrées après les règles hors grille, avant l'écriture · écartée : d'abord · raison : une directive peut fusionner avec une règle que l'un ou l'autre a produite (`architecte.md`, 6b) · inconnu.
- Il ne questionne jamais une directive · écartée : la contester · raison : c'est sa décision, une directive qu'elle juge fausse, elle la change elle-même (`architecte.md`, *The directives*) · inconnu.

### architecte, invocation 2 — Integrating : tourner les réponses en règles

Modèle: opus · effort high · outils: Read, Grep, Glob, WebSearch, WebFetch, Edit, Write
Invoquée par: `/conventions`, sur un `questions-architecte-NN.md` répondu à la racine ; prompt `… Invocation 2 — Integrating. Answered file: questions-architecte-NN.md. Your questions file number: NN.`
Lit: le fichier répondu que le prompt nomme, et lui seul ; `docs/TECHNICAL_CONVENTIONS.md` ; `couverture.md` ; la grille ; `blocked_architecte.md` nommé. Ni le fichier produit ni le document technique, ni le web.
Écrit: le fichier de conventions, mis à jour ; `couverture.md`, mise à jour ; un nouveau `questions-architecte-NN.md` seulement si une réponse laisse le choix ouvert, jamais vide ; `blocked_architecte.md`, `## Invocation` 2.
Valeurs: `Kind:` — lu, chaque sorte route sa réponse ; `corrigé` · `question ouverte` · `grille amendée` — écrits dans `couverture.md`.

**Gestes**
1. Lire le fichier répondu.
2. Une réponse qui laisse le choix ouvert — dont on ne peut fonder une règle vérifiable, *une erreur est montrée* sans dire laquelle — repart dans un nouveau fichier ; c'est ce qui borne la boucle.
3. Chaque autre réponse devient une règle dans la section que la grille lui donne, et une ligne de couverture ; sauf : une `inconsistency` → aucune règle, la correction est dans le document technique, `couverture.md` note l'entrée et `corrigé` ou `question ouverte`, le rapport dit quoi corriger en amont ; une `coverage` → aucune règle, c'est un comportement, la réponse est le comportement ou *voir produit*, nommée dans le rapport ; une `forme` → aucune règle, ni dans la grille, `couverture.md` note ce que `Block:` nommait et `grille amendée` ou `question ouverte`, nommée dans le rapport ; un `replacement` → jamais une règle au numéro libre suivant (l'ancienne resterait en vigueur à côté), deux issues selon la réponse : elle change la règle → la règle en vigueur est changée en place, numéro gardé, le geste *R30 changed* de l'invocation 3, sa ligne de `couverture.md` porte le numéro ; elle garde la règle → aucune règle, le document technique est faux comme pour une `inconsistency`, `couverture.md` note `corrigé` ou `question ouverte` ; le rapport dit laquelle — sur *garde*, quoi corriger en amont ; sur *change*, les lots nommés qui suivent l'ancienne forme jusqu'à leur retour par `/diagnostique` (`architecte.md` L689-708).

**Branches** — aucune réponse ouverte → la boucle finit ; sinon un fichier de plus. Un `replacement` : deux issues, changer la règle en place ou n'écrire rien, jamais une règle nouvelle.
**Échange** — lit ce que le Product Owner a répondu ; écrit les lignes de couverture que l'invocation 4 relit pour savoir ce qui est couvert.
**Bloque** — `blocked_architecte.md`, `## Invocation` 2, sur une entrée manquante — le fichier de conventions d'abord.

**Décisions**
- Les deux documents ne sont pas rouverts · écartée : redériver · raison : une réponse devient une règle, elle n'est pas redérivée ; ce qu'il en fallait, l'invocation 1 l'a demandé (`architecte.md`, PART 2) · inconnu.
- Une réponse infondable est une non-réponse, jamais une règle à grain plus fin · écartée : compléter · raison : il n'écrit jamais une règle qu'il devrait régler plus fin pour l'appliquer — un écart de précision fait de la réponse une non-réponse (`architecte.md`, invocation 2) · inconnu.
- `forme` exemptée comme `inconsistency` et `coverage` · écartée : une règle · raison : `docs/verification3/plan.md` entrée 9 · inconnu.
- Le devenir d'une `inconsistency` et d'une `forme` écrit dans `couverture.md` · écartée : le rapport seul · raison : sans ligne sur disque rien ne dit que le document fut trouvé incohérent, et l'invocation suivante repasserait la même entrée (`architecte.md`) · inconnu.
- Un `replacement` répondu change la règle en place ou n'écrit rien, jamais une règle nouvelle · écartée : la voie de requête de l'Arbitre (`arbitre.md` L409, invocation 3) ; le défaut d'avant, une règle au numéro libre suivant · raison : l'`Answer:` resterait vide et `conventions.md` L81 bloquerait chaque run suivant, le contrat du fichier de questions devrait changer ; une règle nouvelle laisse l'ancienne en vigueur à côté, deux règles qui se contredisent (`architecte.md` L689-708) · non éprouvée.

### architecte, invocation 3 — Requests : régler les requêtes de conventions

Modèle: opus · effort high · outils: Read, Grep, Glob, WebSearch, WebFetch, Edit, Write
Invoquée par: `/conventions`, sur une requête de `architecte/` à `## Verdict` vide, avec `Called by the orchestration.`, sur le dossier de feature ou le `bugfix-NN/` du second argument ; aussi par `/7_lots`, `/8_code` et l'Arbitre — → `PROCESS_AVAL.md` §architecte — invocation depuis /7_lots, §architecte — invocation depuis /8_code, §architecte — invocation depuis l'arbitre. Prompt `Working folder: <the working folder>. Invocation 3 — Requests. Called by <the orchestration | the Arbitre>.`
Lit: `architecte/` du dossier de travail, globé — ce dossier seul — chaque fichier entier ; `docs/TECHNICAL_CONVENTIONS.md` ; `couverture.md` de la feature, un niveau au-dessus sur un `bugfix-NN/` ; le web ; les fichiers de build que les conventions nomment ; la grille. Ni le fichier produit ni le document technique.
Écrit: le fichier de conventions, mis à jour ; `couverture.md`, une ligne par règle ajoutée, `requête` où serait la nature, `architecte/<fichier> — Request N` ou `bugfix-NN/architecte/<fichier>` en première colonne ; le `## Verdict` de chaque bloc de requête, sous son `# Request N`, jamais en fin de fichier — le titre ajouté quand il manque ; `blocked_architecte.md`, `## Invocation` 3, seulement sur `Called by the orchestration.` (→ MECANISMES §Requête de conventions — divergence).
Valeurs: `Called by` — lu (→ MECANISMES §Valeurs de « Called by » — qui a invoqué l'Architecte) ; les cinq titres d'une requête — lus ; les issues d'un verdict, écrites par lui seul et lues par l'agent qui a écrit la requête — `Convention — R93 written.` puis le texte ; une convention qui en resserre une autre, écrite dans les deux, la large nommant l'étroite ; `Already carried`, la règle par numéro et texte ; `Not a convention`, où cela va (le code, l'outillage, la machine) ; un doute ou une décision produit, dit dans le verdict ; `R30 changed.` avec la nouvelle forme ; les deux filtres — la plateforme l'impose : pas une convention ; ne tient que sur une machine : pas une convention ; un outil qui la vérifie ne fait que fixer la sorte de test.

**Gestes**
1. Lire chaque fichier du dossier et tous ses blocs avant d'en régler un ; deux requêtes portent souvent une règle.
2. Traiter chaque bloc à `## Verdict` vide ou sans titre, jamais un fichier sauté tant qu'un de ses blocs est vide ; un bloc réglé n'est jamais rouvert.
3. Chercher, dans l'ordre : la plateforme l'impose-t-elle ; un outil que le projet pourrait nommer le vérifie-t-il déjà ; le projet le déclare-t-il déjà, dans les conventions ou les fichiers de build qu'elles nomment. Chercher, pas rappeler.
4. Les deux filtres ; une règle qui le porte déjà sous une autre forme.
5. Régler et écrire : la règle dans le fichier, sa ligne de couverture, le verdict avec numéro et texte ; une règle qui resserre, écrite dans les deux ; refus compris — chaque requête reçoit un verdict.

**Branches** — `Called by the Arbitre.` → jamais un fichier de blocage, un refus va dans le verdict, une entrée manquante aussi ; un `blocked_architecte.md` trouvé à la racine n'est pas à traiter, une requête que sa cause arrête encore est refusée en le nommant. `Called by the orchestration.` → un fichier de blocage sur une entrée manquante, personne n'attend. Aucun dossier, aucune requête vide → dit, arrêt, issue normale.
**Échange** — lit `## What I need`, `## Why the lot cannot proceed`, `## Where I met it`, `## What I think it is` que le Cadreur, le Détailleur, le Concepteur, le Réalisateur, l'Arbitre écrivent (`PROCESS_AVAL.md`) ; écrit `## Verdict` que ces agents relisent et que le Cadreur lit sur `# Request N` ; écrit les lignes que `/audit_conventions` nomme.
**Bloque** — `blocked_architecte.md` seulement sur `Called by the orchestration.` ; `/conventions` et `/8_code` le lisent, `## Invocation` 3.

**Décisions**
- Il décide si c'est une convention du tout · écartée : écrire ce que la requête demande · raison : une requête n'est pas une licence à écrire n'importe quoi ; une règle suit la grille comme une autre (`architecte.md`, invocation 3) · inconnu.
- Les blocs réglés un par un, jamais un fichier sauté · écartée : sauter un fichier à verdict rempli · raison → MECANISMES §Requête de conventions — divergence (`docs/verification3/plan.md` entrée 30) · inconnu.
- Le verdict sous le `# Request N` qu'il répond · écartée : en fin de fichier · raison : le `## Where` du fichier de blocage nomme ce `N`, et le Cadreur lit le verdict là (`architecte.md` ; `docs/verification3/plan.md` entrée 8) · inconnu.
- Le texte de la règle dans le verdict, pas le numéro seul · écartée : le numéro · raison : l'agent qui le lit n'ouvre pas les conventions, il copie ce que dit le verdict (`architecte.md`) · inconnu.
- Une règle qui resserre s'écrit dans les deux · écartée : l'étroite seule · raison : un agent lit la règle large, trouve son cas et s'arrête ; une restriction qu'il n'atteint jamais n'existe pas (`architecte.md` ; grille R7) · inconnu.
- Les fichiers de build lus à 3 seulement, ceux que les conventions nomment · écartée : globber le dépôt · raison : elle répond aux requêtes d'outillage ; sans règle qui les nomme, il répond sans eux et le dit — une règle à ajouter (`architecte.md`, *What you read*) · inconnu.
- Jamais un fichier de blocage quand l'Arbitre appelle · écartée : bloquer · raison : deux agents attendraient la même réponse ; l'Arbitre tourne encore et reprend le refus (`architecte.md`, *When you cannot produce*) · inconnu.
- La ligne de couverture d'une règle de requête · écartée : aucune provenance · raison : `/audit_conventions` nomme chaque règle qu'un cycle a ajoutée par la requête qui l'a produite (`architecte.md`, mouvement 5) · inconnu.

### architecte, invocation 4 — Completing : compléter un fichier qui existe, pour une feature nouvelle

Modèle: opus · effort high · outils: Read, Grep, Glob, WebSearch, WebFetch, Edit, Write
Invoquée par: `/conventions`, quand `docs/TECHNICAL_CONVENTIONS.md` existe et qu'aucun `couverture.md` n'est à la racine de la feature ; prompt `… Invocation 4 — Completing. Your questions file number: NN.`
Lit: `docs/TECHNICAL_CONVENTIONS.md` entier ; `desc-produit.md` ; `spec-technique.md` ; `tracabilite.md` ; `par-genre/directives.md` ; le web ; la grille ; `blocked_architecte.md` nommé.
Écrit: le fichier de conventions, ajouté, jamais réécrit ; `couverture.md`, pour cette feature seule ; `questions-architecte-NN.md`, toujours, même vide ; `blocked_architecte.md`, `## Invocation` 4.
Valeurs: `Kind: replacement` — écrit ici seulement : une règle en vigueur dit le contraire de ce que la feature exige, la question dit trois choses — la règle en vigueur, ce que la feature exige, ce qui a été codé sous l'ancienne — et demande le choix, changer la règle ou s'y conformer, en nommant les lots codés sous l'ancienne (`architecte.md` L560-567, L897-901) ; ses deux options sont exactement `Changer la règle` et `Se conformer à la règle` ; les autres `Kind:` comme à 1 ; les genres et les natures comme à 1.

**Gestes**
1. Lire le fichier de conventions entier ; charger la grille et le fichier — chaque règle de la partie B est vérifiée contre ce que le fichier tient avant d'écrire.
2. Les mouvements 2 à 10 de l'invocation 1, tous, sur les documents de cette feature ; n'écrire que ce que le fichier ne couvre pas, au numéro libre suivant, dans la section de la grille.
3. Une règle en vigueur contredit ce que la feature exige, ou une directive → jamais remplacée, une question `replacement` qui demande le choix et nomme les lots codés sous l'ancienne.

**Branches** — la seule différence avec 1 : le mouvement 1 lit le fichier, et une contradiction est levée au lieu de tranchée.
**Échange** — écrit `couverture.md` de la feature, ce qui rend `/conventions` idempotent ; lit les règles ajoutées lot par lot par l'invocation 3.
**Bloque** — `blocked_architecte.md`, `## Invocation` 4 ; sans fichier de conventions, `## To resume` dit `/conventions` invocation 1.

**Décisions**
- Jamais redérivé à neuf · écartée : réécrire · raison : chaque règle que l'invocation 3 a ajoutée lot après lot serait perdue — l'incohérence entre features que l'agent existe pour empêcher (`architecte.md`, invocation 4) · inconnu.
- L'interdiction de lecture de l'invocation 1 ne s'applique pas · écartée : la garder · raison : les règles ajoutées lot par lot ne sont pas sa propre sortie, ce sont des requêtes réglées de vrais lots (`architecte.md`) · inconnu.
- Une contradiction est levée en `replacement`, jamais remplacée · écartée : remplacer · raison : chaque lot déjà codé suit l'ancienne règle, les fiches la nomment, et le code neuf suivrait la nouvelle (`architecte.md`, *Completing, and replacing*) · inconnu.
- `couverture.md` pour cette feature seule · écartée : une couverture du dépôt · raison : elle prouve que le parcours a atteint chaque entrée de ce document, rien d'autre (`architecte.md`) · inconnu.

### fusionneur, invocation 1 — Compare and question : le plan de fusion

Modèle: sonnet · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/fusion` (lignes 9, 11, ou 3 la nommant) ou `/fusion_compare` ; prompt `Feature folder: docs/features/<name>/. Invocation 1 — Compare and question. Questions file number: <NN>.` et le fichier de blocage rempli.
Lit: `blocked_fusionneur.md` et les `blocked_fusionneur-NN.md` d'abord, à chaque run ; `desc-produit-fusion.md`, jamais `desc-produit.md`, jamais `idees.md` ; `docs/PRODUIT_GLOBAL.md` par son index, puis section, bloc, phrase ; ses propres `questions-fusionneur-*` répondus, racine ou classés — jamais ceux d'un autre agent.
Écrit: `plan-fusion.md` ; `questions-fusionneur-NN.md`, toujours, même vide ; `blocked_fusionneur.md`, `## Invocation` 1 (forme 2).
Valeurs: les verbes du plan — écrits, `REPLACE`, `INSERT`, `KEEP`, `PENDING`, jamais `DELETE` à 1, `INIT` seul sur un global à `# Application` (→ MECANISMES §Les verbes du plan de fusion — ce qu'une phrase devient) ; les marques `[new block]`, `[new section]`, la ligne de titre `PENDING … title` — écrites ; les six genres — lus, `comportement`, `transverse`, `recette`, `référence` entrent, `directive` et `hors périmètre` jamais ; les trois niveaux de localisation, lus par lui seul — la section par son titre dans le global, le bloc par son titre dans la section, la phrase contre le bloc existant, quelques lignes.

**Gestes**
1. Le global ne tient que `# Application` → le plan est `INIT`, aucune question.
2. Sinon, le genre d'abord : un bloc `directive` ou `hors périmètre` est sauté entier.
3. Phrase par phrase du nouveau bloc contre l'existant : même chose dite autrement → `REPLACE` ; identique → `KEEP` ; sans correspondant → `INSERT` ; c'est une compréhension, pas une comparaison de texte.
4. Deux cas font une question, jamais appliqués : une règle de l'existant sans correspondant dans le nouveau (le silence n'est pas une suppression) → `PENDING questions-fusionneur-NN Qn: "…"` ; un titre de section qui ne couvre plus ce qu'elle tient une fois le `[new block]` entré → la ligne de titre.
5. Une question dont la réponse est enregistrée dans un fichier répondu n'est jamais reposée.
6. Le plan, section par section, bloc par bloc, une ligne par phrase ; le fichier de questions, même vide.

**Branches** — `INIT` → pas de comparaison ; sinon le plan complet ou `PENDING`.
**Échange** — lit la copie que le Rédacteur (3) et lui-même (3) ont écrite ; écrit le plan que l'invocation 2 applique et le mot `INIT` que `/fusion` et `/fusion_applique` greppent.
**Bloque** — `blocked_fusionneur.md` ; rien d'autre écrit, pas même un fichier vide ; le Product Owner répond.

**Décisions**
- L'unité de fusion est la phrase, jamais le bloc · écartée : remplacer le bloc · raison : une refonte remplace la structure, mais des règles survivent — une entrée, un accès, une portée (`fusionneur.md`, *Sentence by sentence*) · inconnu.
- Jamais `DELETE` de l'invocation 1 · écartée : supprimer ce qui n'a pas de correspondant · raison : le silence n'est pas une suppression ; la suppression vient d'une réponse confirmant qu'une règle ne tient plus (`fusionneur.md`) · inconnu.
- La question de titre posée quand un bloc neuf entre · écartée : l'ignorer · raison : le global se lit par son index seul ; un titre qui a dérivé est une section que le Rédacteur n'ouvre jamais, il crée un doublon, et le défaut grandit seul (`fusionneur.md`, *When you place a new block*) · inconnu.
- Seules les sections touchées, jamais un audit des autres · écartée : auditer le global entier · raison : trois niveaux de localisation — la section par son titre, le bloc par son titre dans la section, la phrase contre le bloc existant — et le bloc borne la comparaison : dix lignes, pas un document entier ; le global dépasse 250 Ko et se lit par l'index, jamais en entier (PROCESS_AMONT-avant-refonte.md L825-828, L1376-1378) · inconnu.
- Il ne décide rien de ce qui fusionne · écartée : juger · raison : réglé quand le fichier de feature fut structuré ; il applique et observe ce qui reste ouvert (`fusionneur.md`, *Role*) · inconnu.

### fusionneur, invocation 2 — Apply : appliquer le plan et écrire le rapport

Modèle: sonnet · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/fusion` (ligne 10, ou 3 la nommant) ou `/fusion_applique` ; prompt `… Invocation 2 — Apply. Questions file number: <NN>.`
Lit: ses fichiers de blocage d'abord ; `plan-fusion.md` ; le fichier de questions que ses lignes `PENDING` nomment, répondu — à la racine d'abord, puis `questions/fusionneur/` ; le global par son index ; sur `INIT`, le global tel que la commande l'a copié, bloc par bloc pour `Genre:`.
Écrit: `docs/PRODUIT_GLOBAL.md`, par éditions ciblées, jamais réécrit entier ; `rapport-fusion.md`, après avoir appliqué ; **ou**, sur une réponse ambiguë, le `questions-fusionneur-NN.md` suivant seul et le plan dont les `PENDING` encore ouverts nomment ce fichier — rien au global, pas de rapport ; `blocked_fusionneur.md`, `## Invocation` 2.
Valeurs: `PENDING` résolu en `KEEP`, `REPLACE`, `DELETE` — écrit ; la liste de retrait, lue par lui seul — le numéro de bloc, la ligne `Genre:`, la ligne `Global:`, une `Nature:` vide ; une `Nature:` remplie reste ; `directive` et `hors périmètre` retirés entiers ; le rapport à quatre champs, écrit par lui seul — `## New sections`, `## Merged sections` (remplacé, gardé, inséré par bloc), `## Deleted sections`, `## Unchanged sections`, une ligne par élément, daté, jamais modifié.

**Gestes**
1. Sur `INIT` : retirer de la copie, bloc par bloc, ce que la liste de retrait nomme et chaque bloc `directive` ou `hors périmètre` ; rien d'autre ne change ; fini.
2. Sinon, chaque `PENDING` contre sa réponse : la règle tient → `KEEP` ; a changé → `REPLACE` ; ne tient plus → `DELETE` ; la ligne de titre à part — le titre couvre encore → la ligne quitte le plan ; un nouveau titre → le `## <Section>` renommé, le `[new block]` dessous.
3. Une réponse qui ne résout rien → le fichier de questions suivant, chaque réponse ambiguë restituée avec ce qu'elle laisse ouvert ; ce run n'applique rien.
4. Appliquer par éditions ciblées ; une section neuve dans son domaine après celles de même nature, un domaine créé s'il manque ; toute marque de changement disparaît à l'insertion ; un bloc entre avec son titre seul.
5. Le rapport, après.

**Branches** — `INIT` ; réponse ambiguë ; application.
**Échange** — lit la copie faite par `/fusion` ou `/fusion_applique` sur `INIT` ; écrit `rapport-fusion.md` que les trois commandes testent et que le Product Owner lit.
**Bloque** — `blocked_fusionneur.md` ; ni plan, ni questions, ni rapport.

**Décisions**
- Sur une réponse ambiguë, rien au global, pas de rapport, un fichier de questions seul · écartée : interpréter · raison : une réponse qui ne résout aucune des issues repart, jamais interprétée ; le rapport dit qu'elle a tourné (`fusionneur.md`, invocation 2) · inconnu.
- Le global jamais réécrit entier · écartée : le réécrire · raison : les titres sont les ancres qui rendent les éditions ciblées possibles (`fusionneur.md`) · inconnu.
- Le rapport écrit après, jamais avant, daté, jamais modifié · écartée : avant ; tenu à jour · raison : il enregistre ce que la fusion a fait, et la Product Owner le lit une fois le global changé (`fusionneur.md`) · inconnu.
- La copie sur `INIT` faite par la commande · écartée : par lui · raison → `/fusion`, `/fusion_applique` · inconnu.

### fusionneur, invocation 3 — Bug-fix decisions : ce qu'une correction a réglé du produit

Modèle: sonnet · effort high · outils: Read, Grep, Glob, Edit, Write
Invoquée par: `/fusion`, ligne 8 (un `bugfix-*/` et aucun `questions-fusionneur-*`) ou ligne 7 (son fichier répondu, sans plan), ou ligne 3 ; prompt `… Invocation 3. Questions file number: <NN>.`
Lit: ses fichiers de blocage d'abord ; le global, testé d'abord pour `# Application` seul ; chaque `bugfix-*/desc-bug.md`, du plus ancien dossier au plus récent, tous avant de fusionner — jamais `bug-list.md` ; `desc-produit-fusion.md` ; son fichier de questions répondu à la racine, quand il y en a un.
Écrit: le global, mis à jour — **ou** `desc-produit-fusion.md` sur une première feature ; le `questions-fusionneur-NN.md` suivant, toujours, même vide ; `blocked_fusionneur.md`, `## Invocation` 3.
Valeurs: les trois issues d'une entrée de `desc-bug.md`, lues par lui seul — un symbole manquant, une dépendance absente, un mauvais support → rien, technique ; l'application se comporte autrement que le global ne décrit → fusionner ; l'application fait ce que le global ne décrit nulle part → fusionner ; le test est le lecteur, pas la formulation.

**Gestes**
1. Tester le global avant de lire un `desc-bug.md` : plus que `# Application` → écrire dans le global ; `# Application` seul → écrire dans `desc-produit-fusion.md`, jamais dans le global ; un bloc placé là ne porte pas de `Genre:`.
2. Sans fichier répondu à la racine — les trois mouvements : lire chaque `desc-bug.md` ; par entrée, dit-elle quelque chose de ce que fait l'application ; fusionner ce qui est gardé, par les trois niveaux, la vérification de titre et la transposition au présent ; ne porter que ce que la copie ne porte pas déjà — le Rédacteur y a plié chaque `decisions-produit.md` ; deux formulations d'un même comportement → une question nommant les deux ; une ligne sans section correspondante → une question, jamais une insertion seule.
3. Avec un fichier répondu tenant `### Q` — le quatrième mouvement seul : chaque réponse appliquée par éditions ciblées, la ligne où la réponse la place, la section renommée ou gardée, le comportement choisi remplaçant l'autre ; une réponse ambiguë → le fichier suivant.
4. Le fichier de questions, même vide.

**Branches** — un `bugfix-*/` sans `desc-bug.md` → ne tourne pas, le dit, jamais `bug-list.md` ; un fichier sans rien à fusionner est l'issue normale, le fichier vide écrit tout de même.
**Échange** — lit `desc-bug.md` que le Diagnostiqueur écrit (`PROCESS_ENTREES.md`) ; lit la copie que le Rédacteur 3 a pliée ; écrit dans la copie que l'invocation 1 lira sur `INIT`.
**Bloque** — `blocked_fusionneur.md`, `## Invocation` 3.

**Décisions**
- `desc-bug.md`, jamais `bug-list.md` · écartée : lire la liste de la Product Owner · raison : un manque mis de côté par le diagnostic n'a produit aucun code, le porter au global décrirait un comportement que l'application n'a pas (`fusionneur.md`, invocation 3) · inconnu.
- Sur une première feature, écrire dans la copie · écartée : sauter la passe ; réordonner `/fusion` · raison : une ligne dans le global ferait ne jamais tirer `INIT` (`docs/verification3/plan.md` entrée 34, item E, Option 1) · inconnu.
- Ne porter que ce que la copie ne porte pas · écartée : tout porter · raison : une décision prise en codant est déjà en route par `decisions-produit.md` (`fusionneur.md`) · inconnu.
- Le seul appel où la décision n'est pas dans un fichier produit — il dit si une entrée est produit · écartée : le Rédacteur trie · raison : un `desc-bug.md` ne porte aucune décision (`fusionneur.md`, *What you never do*) · inconnu.
- Deux runs d'une invocation : trois mouvements, ou le quatrième seul · écartée : rejouer les trois · raison : les trois ont tourné quand le fichier fut écrit (`fusionneur.md`) · inconnu.

---

## Coutures

| Ce qui part | Ce qui arrive | Ce que le receveur vérifie | L'autre document |
|---|---|---|---|
| `idees.md`, écrit à la main par le Product Owner, en français, libre | `/1_lexique` le nomme au lexicographe (invocations 1, 2), qui le lit entier et y écrit les termes réglés ; `/2_structure` le nomme au Rédacteur (invocation 1) | `/1_lexique` : aucun test, le lexicographe bloque sur un fichier absent ou vide ; `/2_structure` : pas de `desc-produit.md`, et le plus haut `questions-lexicographe-NN.md` sans `### Q` | `PROCESS_ENTREES.md` |
| `docs/features/`, racine posée par `socle.py` (vide à ce moment, hors commit), puis `docs/features/<name>/` avec `idees.md` dedans — écrit par le cockpit pour la première fonctionnalité, à la création de l'application, à la main par le Product Owner pour les suivantes (→ MECANISMES §Disposition du dossier de feature) | Les douze commandes de ce document dérivent `docs/features/<name>/` de leur premier argument et le passent aux dix agents par `Feature folder:`, `The product file:`, `The idea file:`, `Write to` | Rien — aucune commande ne teste l'existence du dossier ; sur un `<name>` sans dossier, `/1_lexique` cherche `blocked_lexicographe.md` par `Glob`, invoque, et le Lexicographe bloque sur *no idea file*, l'écriture du fichier de blocage créant le dossier | `PROCESS_ENTREES.md` |
| `docs/PRODUIT_GLOBAL.md`, créé par `socle.py` avec `# Application` pour seule ligne | Le Rédacteur (1, 2, 3) et le Fusionneur (1, 2, 3) le lisent par l'index, le sondeur 3 par les sections que `Global:` nomme ; le Fusionneur seul y écrit, `INIT` le remplace par copie | Le Fusionneur teste `# Application` seul (première feature) ; `/fusion` et `/fusion_applique` greppent `INIT` dans le plan | `PROCESS_ENTREES.md` |
| `spec-technique.md` ouvrant sur `# Preamble`, sans `<<ASSUMED` ni `[B`, avec `tracabilite.md` à côté — `/6_convertit` dit « le document tient » | `/conventions` (l'Architecte 1 ou 4 dérive), puis `/7_lots` (le Cadreur greppe et coupe) | `/conventions` : l'existence, sauf pour l'invocation 3 ; `/7_lots` : `^### §`, zéro entrée → aucun découpage, le contenu vit dans `par-genre/recette.md` et `## Cross-cutting rules`, puis `/fusion` ; le Cadreur greppe `<<ASSUMED` et `[B` et bloque sur une occurrence | `PROCESS_AVAL.md` |
| `tracabilite.md`, une ligne par bloc, identifiant, titre, entrées ou tiret | L'Architecte (1 et 4, mouvement 2) pour l'appariement ; `/9_controle` (phase 1) pour `tracabilite-full.md` | L'Architecte : un tiret sur `comportement` ou `référence` seulement lève `inconsistency` ; `/9_controle` : les blocs `comportement` par grep plus tout bloc dont la ligne porte une entrée | `PROCESS_AVAL.md` |
| `.claude/grids/GRILLE_FERMETURE_TECHNIQUE.md`, installée avec la chaîne — `socle.py` ne la crée pas, le cockpit la copie dans l'application avec les agents | Le Convertisseur, invocation 1, joue ses fermetures *by nature* (`## Traceability`, `## Nothing dropped`, `## Completeness`, `## What a nature owes`) sur sa section écrite ; l'invocation 2 joue les *across sections* (`## Declared links`, `## Singularity`, `## Agreement between entries`, `## Resources`) sur le document entier ; le Diagnostiqueur (invocation 2, mouvement 9) en lit trois — `## Completeness`, `## Resources`, `## Agreement between entries` — sur `desc-bug.md`, pas les mêmes ni le même fichier | Les titres `##` existent dans la grille ; le chemin depuis la racine du dépôt, jamais depuis le dossier de feature (→ MECANISMES §Chemins relatifs) ; une fermeture qui échoue est une question chez le Convertisseur, un blocage chez le Diagnostiqueur | `PROCESS_ENTREES.md` |
| `.claude/grids/GRILLE_EXISTANT.md`, installée avec la chaîne — la grille de l'existant, qui ferme une feature contre le produit déjà construit ; aucune commande d'extraction ne l'accompagne | `/4_grille`, second temps, la nomme au sondeur (`The grid: .claude/grids/GRILLE_EXISTANT.md.`, `Invocation 3 — Existant.`) sur les seuls blocs à ligne `Global:`, chacun avec la section du global qu'il nomme ; le sondeur la lit entière et en porte chaque question au bloc et à sa section ensemble | Le second temps ne part qu'une fois le premier clos ; aucun bloc à `Global:` → `questions-existant-NN.md` écrit vide sans agent ; le plus haut `questions-existant-NN.md` sans `### Q`, racine ou classé, est ce que `/5_reclasse` teste ; jamais de `Défaut:` dans ce fichier | `PROCESS_ENTREES.md` |
| L'absence de `docs/TECHNICAL_CONVENTIONS.md` — `socle.py` ne le crée pas et l'imprime parmi ce que l'application fournit, « par /conventions, jamais à la main » ; la carte « À fournir avant le code » du cockpit le montre ✗ tant qu'il manque | `/conventions` : la ligne « pas de `docs/TECHNICAL_CONVENTIONS.md` » de sa table → `1 — Deriving`, l'Architecte l'écrit à neuf depuis `desc-produit.md`, `spec-technique.md` et la grille | Le test porte sur l'existence de ce fichier seul, jamais sur `couverture.md` ; à l'invocation 1 l'Architecte n'ouvre aucun fichier au nom de *convention*, *rule* ou *guideline* (→ MECANISMES §Lecture des conventions — divergence) ; `/conventions` lancée à la main, rien ne l'enchaîne | `PROCESS_ENTREES.md` |
| `docs/TECHNICAL_CONVENTIONS.md`, écrit par l'Architecte, douze sections, règles `R<n>` à quatre champs dans cet ordre — le numéro, la règle, `permanente` ou `spécifique`, `mechanical` ou `review` — plus `off-grid` en cinquième champ sur une règle hors grille (`architecte.md`, *What a rule line looks like*) | Le Cadreur (entier — il bloque sans fichier), le Détailleur, l'Arbitre, le Diagnostiqueur, les trois agents de lot et le Relecteur (les `permanente` et les `R<n>` de la fiche) ; `/audit_conventions` | Le mot `permanente` sur la ligne ; aucune règle marquée → tout lire ; les dossiers de code que les conventions nomment pour le grep (→ MECANISMES §Lecture des conventions — divergence, §Grep du code avec chemin) | `PROCESS_AVAL.md`, `PROCESS_ANNEXES.md` |
| `couverture.md` à la racine de la feature, une ligne par entrée, `no rule` écrit | L'Architecte 3 invoqué depuis `/7_lots`, `/8_code`, l'Arbitre y ajoute une ligne par règle de requête, `bugfix-NN/architecte/<fichier>` en première colonne ; `/audit_conventions` la cherche un niveau au-dessus du dossier de travail ; `/2_structure` la supprime sur un `NEW` ou un `MODIFIED` | `/conventions` teste son existence pour l'invocation 4 ; `/audit_conventions` : à quel document elle trace | `PROCESS_AVAL.md`, `PROCESS_ANNEXES.md` |
| Une requête `architecte/<agent>-<lot>.md`, `architecte/cadreur.md` (`# Request N` empilés), `architecte/arbitre-*.md`, à `## Verdict` vide ou sans titre `## Verdict`, écrite par le Cadreur, le Détailleur, le Concepteur, le Réalisateur, l'Arbitre | `/conventions` (invocation 3, `Called by the orchestration.`, sur le dossier de travail du second argument) ; aussi `/7_lots`, `/8_code`, l'Arbitre → entrées courtes de `PROCESS_AVAL.md` | Un bloc sans titre `## Verdict` compte pour vide ; le verdict sous le `# Request N` ; le texte de la règle dedans | `PROCESS_AVAL.md` |
| `Called by the orchestration.` / `Called by the Arbitre.` dans le prompt de l'invocation 3 | L'Architecte : fichier de blocage possible, ou refus dans le verdict | Jamais déduit (→ MECANISMES §Valeurs de « Called by » — qui a invoqué l'Architecte) | `PROCESS_AVAL.md`, `PROCESS_MECANISMES.md` |
| `blocked_architecte.md` à la racine du dossier de travail, `## Invocation` 3, écrit sur un appel de l'orchestration | `/8_code` le lit : `## Invocation` 3 → nommé au prompt du mouvement 7, renommé après ; une autre invocation → arrêt, `/conventions` | La ligne `## Invocation`, le `## Decision` | `PROCESS_AVAL.md` |
| Le second argument `bugfix-NN` de `/conventions`, et l'existence d'une requête dans `bugfix-NN/architecte/` | `/conventions` route l'invocation 3 sur ce dossier de travail ; sans requête, « rien à invoquer, `/8_code` continue » | Une requête à `## Verdict` vide dans ce dossier | `PROCESS_AVAL.md` |
| `code/decoupage.md`, écrit par le Cadreur | `/2_structure` (refus d'un `NEW`, rien supprimé sur un `MODIFIED`) et `/6_convertit` (arrêt) testent son existence | L'existence seule, jamais le contenu | `PROCESS_AVAL.md` |
| `desc-produit.md` fermé — `Genre:` sur chaque bloc, `Nature:` sur chaque comportement, aucun marqueur — et `par-genre/recette.md` | `/9_controle` (phase 1, `grep -B1 '^Genre: comportement$'` ; phase 4, `par-genre/recette.md`) et le Contrôleur (les blocs par titre) | Le genre par grep ; les blocs nommés ; les marqueurs ignorés | `PROCESS_AVAL.md` |
| `code/decisions-produit.md`, un par cycle, écrit par `/9_controle` (phase 6) — identifiant `B<n>` ou tiret, deux espaces, la décision en français, même vide | `/fusion` les nomme au Rédacteur (invocation 3), la feature puis chaque `bugfix-NN` dans l'ordre ; il les traduit et les plie dans `desc-produit-fusion.md` | L'existence par cycle ; l'ordre nommé ; sans fichier, une copie fidèle ; une ligne lue comme écrite | `PROCESS_AVAL.md` |
| `bugfix-NN/desc-bug.md`, écrit par le Diagnostiqueur (invocation 2), une entrée par porteur, `# Preamble`, neuf sections, `## Gaps set aside` | Le Fusionneur (invocation 3), depuis `/fusion` ligne 8, du plus ancien dossier au plus récent | Un `bugfix-*/` sans `desc-bug.md` → ne tourne pas ; `bug-list.md` jamais lu | `PROCESS_ENTREES.md` |
| Un `blocked_<agent>.md` au nom non numéroté, `## Decision` vide, écrit par l'un des dix agents (`blocked_lexicographe.md`, `blocked_redacteur.md`, `blocked_decoupeur.md`, `blocked_qualifieur.md`, `blocked_classeur.md`, les six de `/4_grille`, `convertisseur/blocked_*.md`, `blocked_architecte.md`, `blocked_fusionneur.md`) | Le Product Owner remplit `## Decision` à la main | La commande greppe `## Decision` avant d'invoquer, nomme le fichier rempli, renomme sur la ligne *applied* (→ MECANISMES §Fichier de blocage — divergence, §Reprise sur décision — divergence, §Renommage -NN — divergence) | `PROCESS_MECANISMES.md` |
| Un `questions-<agent>-NN.md` à la racine, `Answer:` vides, écrit par le lexicographe, le Rédacteur, le qualifieur, le classeur, `/4_grille` (sondeur, existant), `/6_convertit` (convertisseur), l'Architecte, le Fusionneur ; `convertisseur/technique-<nature>.md` | Le Product Owner répond en français ; le silence accepte une `Défaut:` | `^Answer:\s*$` sans `Défaut:` ; `^### Q` ; le classement sous `questions/<agent>/` ; l'exception `questions-architecte-*.md` (→ MECANISMES §Fichier de questions — divergence, §Test d'une question sans réponse, §Classement des fichiers de questions) | `PROCESS_MECANISMES.md` |
| `questions-architecte-NN.md` à la racine du dossier de feature, écrit par l'Architecte (invocation 1 ou 4) et laissé en place par `/7_lots` — qui classe tout autre `questions-*.md` sans la garde `### Q` — comme par toute commande du cycle (→ MECANISMES §Classement des fichiers de questions, *L'exception architecte*) | `/conventions` seul : une `Answer:` vide → arrêt, les questions dites ; répondu → `2 — Integrating`, le fichier nommé, classé sous `questions/architecte/` après ; sans `### Q` → classé avant d'invoquer, commit sans worktree, `/7_lots` dit | Les lignes `Answer:` sans rien après (l'Architecte n'écrit jamais de `Défaut:`) et `^### Q` ; le numéro du fichier suivant compte la racine et `questions/architecte/` ensemble | `PROCESS_AVAL.md` (§/7_lots), `PROCESS_MECANISMES.md` |
| `desc-produit.md` fermé par la grille — aucune ligne `### B` portant `NEW` ni `MODIFIED` (retirés par script par le tour de `/4_grille` qui écrit le `questions-sondeur-NN.md` vide), `Genre:` sur chaque bloc, `Nature:` sur chaque `comportement` — et les deux plus hauts `questions-sondeur-NN.md` et `questions-existant-NN.md`, racine ou classés, sans `### Q` (→ MECANISMES §Marqueurs NEW et MODIFIED) | `/5_reclasse` (étapes 2 et 3) : sur ces trois tests il écrit `par-genre/*.md` et `desc-par-nature.md` ; sinon il s'arrête et nomme `/4_grille`, `/3a_genre` ou `/3b_nature` | `grep '^### .*NEW'` et `grep '^### .*MODIFIED'` sur `desc-produit.md` ; `^### Q` sur le plus haut fichier de chaque préfixe, où qu'il soit ; `grep -c '^Genre:$'` à zéro et chaque `comportement` à `Nature:` remplie | `PROCESS_MECANISMES.md` |
| `questions/qualifieur/questions-qualifieur-NN.md` et `questions/classeur/questions-classeur-NN.md`, le plus haut de chaque dossier, classé par `/2_structure` après intégration (→ MECANISMES §Classement des fichiers de questions, *Ce qu'on rouvre*) | `/3a_genre` (étape 6) et `/3b_nature` (étape 6) le nomment à leur agent — `<Plus: your answered questions file: …>` — comme troisième déclencheur, sans bloc listé ; le qualifieur et le classeur l'appliquent au bloc que chaque réponse nomme avant de dériver (geste 1) | Le grep `^### Q` sur le plus haut classé de son seul préfixe ; le fichier vide que l'agent écrit à ce run, classé ensuite, est le plus haut et fait taire le déclencheur ; jamais un fichier de la racine | `PROCESS_MECANISMES.md` |
| Les `blocked_*-NN.md` de toute la chaîne amont — à la racine de la feature, sous `cadrage-produit/`, sous `convertisseur/` | `/audit_blocages` seul, à la main, sur le cycle de la feature (le dossier de travail est alors la racine de la feature) : il lit `cadrage-produit/`, `convertisseur/`, la racine du dossier de travail. `/9_controle` ne les lit pas : sa phase 5 ne lit que `## Doubts` et `## Intentions missing` du dernier `code/rapport-controle*.md` et les `code/blocked_*-NN.md`, `code/<lot>/blocked_*-NN.md` du dossier de travail ; les fichiers classés sous `questions/<agent>/` ne sont relus par personne en aval (→ MECANISMES §Classement des fichiers de questions) | Les `-NN` seuls ; un fichier non numéroté est listé sous `### Still open`, jamais tenu pour lu | `PROCESS_ANNEXES.md` |
| Le `model` du frontmatter de chaque agent amont, et l'absence de `Bash` chez les dix | Le `model=` de chaque `Agent()` des douze commandes ; le pas 1 des cinq pas Git commite ce qu'ils écrivent | → MECANISMES §Frontmatter d'un agent, §Git, après le rapport — les cinq pas | `PROCESS_MECANISMES.md` |

## Boucles

### Lexique → réponses → lexique, avant le fichier produit

Ouverte par: `/1_lexique`, invocation 1, qui écrit un `questions-lexicographe-NN.md` tenant un `### Q`
Fermée par: une invocation 1 écrit un `questions-lexicographe-NN.md` sans `### Q` ; `/1_lexique` le voit seul à la racine et nomme `/2_structure` ; `/2_structure` teste que le plus haut `questions-lexicographe-NN.md`, racine ou classé, ne tient aucun `### Q` avant l'invocation 1 du Rédacteur
Plafond: aucun — après chaque 2, un 1 tourne de nouveau
Au plafond: sans objet
Traverse: lexicographe (1, 2), le Product Owner ; `/1_lexique`, `/2_structure` — ce document (description entière), `PROCESS_ENTREES.md` (§idees.md, le fichier que la boucle réécrit ; sa boucle *Balayage → réponse → règlement du vocabulaire, sur `idees.md`*)

### Tour de la grille — première fois

Ouverte par: `/4_grille`, premier temps, qui copie un `cadrage-produit/questions.md` tenant un `### Q` en `questions-sondeur-NN.md`
Fermée par: le plus haut `questions-sondeur-NN.md`, racine ou `questions/sondeur/`, ne tient aucun `### Q` **et** aucune ligne `### B` de `desc-produit.md` ne porte `NEW` ni `MODIFIED` — testé par `/4_grille` avant les greps de marqueurs, et par `/5_reclasse` ; le fichier vide est écrit par le run (copie d'un `questions.md` vide, ou sans agent quand les réponses n'ont changé aucun bloc), et ce run retire les marqueurs par script
Plafond: aucun — chaque tour est un fichier que le Product Owner répond ; un tour dont les réponses créent ou changent un bloc rouvre sur les blocs marqués seuls
Au plafond: sans objet ; un bloc changé après la clôture par une intégration d'`idees.md` ou d'un fichier `existant` ou `convertisseur` rouvre le premier temps, sonder deux fois est le côté accepté
Traverse: sondeur (1, 2), assembleur, lexicographe (3, 4), redacteur (2), decoupeur, qualifieur, classeur ; `/4_grille`, `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/5_reclasse`

### Tour de la grille — seconde fois, et le ping-pong `/5_reclasse` ↔ `/4_grille`

Ouverte par: `/4_grille` une fois le premier temps clos, invocation 3 du sondeur sur les blocs à `Global:`, qui écrit `questions-existant-NN.md` tenant un `### Q` ; ou `/5_reclasse` qui s'arrête faute des deux fichiers de clôture et renvoie à `/4_grille`
Fermée par: le plus haut `questions-existant-NN.md`, racine ou `questions/existant/`, présent et sans `### Q` — écrit par le sondeur 3 quand rien ne heurte, par `/4_grille` sans agent quand aucun bloc ne porte `Global:` ou quand le plus haut classé tient un `### Q` (ses réponses intégrées) ; alors `/5_reclasse` trouve les deux fichiers vides et aucun marqueur, et écrit ses vues
Plafond: aucun — une réponse au second temps repasse par `/1_lexique` et `/2_structure`, marque des blocs, rouvre le premier temps, puis le second dit son dernier mot en écrivant vide sans agent
Au plafond: sans objet ; un `questions-existant-NN.md` classé tenant un `### Q` ne ferme rien, sans le fichier vide `/5_reclasse` renverrait à un second temps qui dit être fini — c'est le fichier vide écrit sans agent qui coupe le ping-pong
Traverse: sondeur (3), lexicographe (3, 4), redacteur (2) ; `/4_grille`, `/5_reclasse`, `/1_lexique`, `/2_structure`

### Question → réponse → intégration, l'amont

Ouverte par: un `questions-<agent>-NN.md` tenant un `### Q` à la racine — du Rédacteur, du qualifieur, du classeur, de `/4_grille`, de `/6_convertit` (produit) (→ MECANISMES §Fichier de questions — divergence)
Fermée par: `/1_lexique` (3 puis 4, si 3 a demandé) puis `/2_structure` (redacteur 2) l'intègre et le classe sous `questions/<agent>/` ; puis `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille` jusqu'à un tour vide — le test : plus aucun fichier tenant un `### Q` à la racine, et le tour suivant vide
Plafond: aucun
Au plafond: sans objet
Traverse: → MECANISMES §Question → réponse → intégration ; ici lexicographe (3, 4), redacteur (2), decoupeur, qualifieur, classeur, sondeur, assembleur, convertisseur ; `/1_lexique` à `/4_grille`, `/6_convertit`

### Genre ou nature → décision de réécriture → retour

Ouverte par: le qualifieur ou le classeur écrit une entrée `## Blocking N` (aucun genre, deux genres ; aucune nature, les huit manquent, deux réponses au même doute), et le Product Owner y décide une réécriture ou un retrait
Fermée par: `/3a_genre` ou `/3b_nature` relit le rapport (*waits on the Rédacteur*) et laisse le fichier ; `/2_structure` nomme le fichier au Rédacteur (2) qui réécrit avec `MODIFIED` et renomme `-NN` ; `/3_decoupe`, `/3a_genre` (et `/3b_nature`) repassent sur le bloc et écrivent la ligne ; le test : le fichier de blocage porte un `-NN` et `grep -c '^Genre:$'` (ou les `comportement` à `Nature:` vide) rend zéro
Plafond: aucun compté nulle part — une réécriture qui tient encore deux genres rebloque sur le même bloc
Au plafond: chaque tour est une décision que le Product Owner écrit, la répétition est visible à elle, et une décision qui dit comment scinder règle le bloc (`docs/verification3/plan.md` entrée 56)
Traverse: qualifieur, classeur, redacteur (2), decoupeur ; `/3a_genre`, `/3b_nature`, `/2_structure`, `/3_decoupe`

### Conversion — boucle courte et boucle longue

Ouverte par: `/6_convertit` : une nature écrit `convertisseur/technique-<nature>.md` avec un `^Answer:\s*$` (courte), ou la commande écrit un `questions-convertisseur-NN.md` tenant un `### Q` (longue), ou l'invocation 2 écrit `technique-transversal.md` ou `questions-transversal.md` avec question ; la marque `<<ASSUMED` tient dans le document
Fermée par: courte — le fichier technique répondu (`### Q`, aucun `^Answer:\s*$`) fait retourner la nature, la section réécrite sans `<<ASSUMED`, le fichier classé sous `convertisseur/closed/` ; longue — la réponse passe par `/1_lexique`, `/2_structure`, `/3_decoupe`, `/3a_genre`, `/3b_nature`, `/4_grille`, `/5_reclasse`, puis `/6_convertit` compare la part à l'octet et retourne la nature (ou la nomme sur son fichier de questions répondu quand la part n'a pas changé) ; le test final : `questions-convertisseur-NN.md` vide, `spec-technique.md` ouvrant sur `# Preamble` sans `<<ASSUMED` ni `[B`, `tracabilite.md` là, aucune nature en attente
Plafond: aucun — une marque encore là après la relance d'une nature sur un fichier répondu est une faute du run, relancée une fois, jamais deux
Au plafond: au-delà de la relance unique, arrêt rapporté comme un fichier manquant
Traverse: convertisseur (1, 2), lexicographe (3, 4), redacteur (2), decoupeur, qualifieur, classeur, sondeur, assembleur ; `/6_convertit`, `/1_lexique` à `/5_reclasse`

### Conventions — questions de l'Architecte

Ouverte par: l'Architecte (1 ou 4) écrit un `questions-architecte-NN.md` tenant un `### Q` ; toute autre commande le laisse à la racine
Fermée par: le Product Owner répond ; `/conventions` invoque l'invocation 2, qui tourne chaque réponse en règle ou en ligne de couverture, et classe le fichier ; l'invocation 2 n'écrit un nouveau fichier que sur une réponse ouverte — le test : aucun `questions-architecte-NN.md` à la racine avec un `### Q`
Plafond: aucun — c'est le mécanisme du Lexicographe, la boucle finit quand 2 n'écrit rien
Au plafond: sans objet ; une `coverage` est corrigée par le Product Owner dans le fichier produit à la main et bâtie au cycle suivant, aucun tour amont ne rejoue ; une `forme` amende la grille par sa main
Traverse: architecte (1, 2, 4) ; `/conventions` ; le Product Owner ; `GRILLE_CONVENTIONS.md`

### Requête → verdict → règle, vue de `/conventions`

Ouverte par: un agent aval écrit une requête sous `architecte/` du dossier de travail à `## Verdict` vide (→ MECANISMES §Requête de conventions — divergence)
Fermée par: l'Architecte 3 écrit `## Verdict` sous le `# Request N`, la règle dans `docs/TECHNICAL_CONVENTIONS.md`, sa ligne de `couverture.md` ; `/conventions` (second argument), `/7_lots`, `/8_code` globent `architecte/` pour un verdict vide ou absent
Plafond: une requête par invocation pour l'Arbitre ; aucun pour les autres
Au plafond: → MECANISMES §Requête → verdict → règle
Traverse: architecte (3) ; `/conventions` ; cadreur, detailleur, concepteur, realisateur, arbitre ; `/7_lots`, `/8_code` — `PROCESS_AVAL.md`, `PROCESS_MECANISMES.md`

### Le blocage du Cadreur, vu de `/conventions`

Ouverte par: le Cadreur écrit `code/blocked_cadreur.md` dont `## Where` vaut `architecte/cadreur.md — Request N`, la requête à `## Verdict` vide (`PROCESS_AVAL.md`, même boucle)
Fermée par: l'Architecte 3 écrit le `## Verdict` sous ce `# Request N` — depuis `/7_lots` (table de sortie), ou à la main depuis `/conventions` (ligne « une requête de `architecte/` à `## Verdict` vide », sur le dossier de feature, ou sur le `bugfix-NN/` du second argument) ; puis `/7_lots` réinvoque le Cadreur, qui rapporte *verdict applied* et le fichier est renommé `-NN` — le test est celui de `PROCESS_AVAL.md`
Plafond: une invocation d'Architecte par requête ; `/conventions` ne réinvoque jamais le Cadreur — c'est `/7_lots`, relancé à la main
Au plafond: un verdict refusé laisse la boucle ouverte ; le Product Owner remplit `## Decision` et relance `/7_lots` (`PROCESS_AVAL.md`)
Traverse: architecte (3) ; `/conventions` — `PROCESS_AVAL.md` (cadreur, `/7_lots`), `PROCESS_MECANISMES.md` (`§Blocage → décision → relance`)

### Fusion — questions du Fusionneur

Ouverte par: le Fusionneur (1) écrit `plan-fusion.md` avec des `PENDING` et un `questions-fusionneur-NN.md` tenant un `### Q` ; ou le Fusionneur (3) écrit un tel fichier ; ou le Fusionneur (2) en écrit un sur une réponse ambiguë
Fermée par: le Product Owner répond ; `/fusion` (lignes 7, 10) ou `/fusion_applique` invoque l'invocation 3 (quatrième mouvement) ou 2, qui résout chaque `PENDING` et écrit `rapport-fusion.md` ; le test : `rapport-fusion.md` existe — `/fusion` ligne 4, `/fusion_compare` et `/fusion_applique` s'arrêtent dessus pour de bon
Plafond: aucun — une réponse ambiguë refait un fichier
Au plafond: sans objet ; un cycle `bugfix-NN` codé après la fusion n'a aucune route : la Product Owner restaure l'ancien global et met de côté le rapport, le plan et les fichiers de questions à la main
Traverse: redacteur (3), fusionneur (1, 2, 3) ; `/fusion`, `/fusion_compare`, `/fusion_applique` ; le Product Owner — ce document seul. Ce que la ligne 8 lit (`bugfix-*/desc-bug.md`, `PROCESS_ENTREES.md`) et ce que la ligne 6 nomme (`code/decisions-produit.md`, `PROCESS_AVAL.md`) sont des coutures (→ `## Coutures`), pas des tours de cette boucle : aucun run de `/9_controle` ni de `/diagnostique` ne suit une question du Fusionneur

### Cycle de correction → fusion

Ouverte par: un `bugfix-NN/` que `/diagnostique` a ouvert, codé par `/7_lots` et `/8_code`, contrôlé par `/9_controle` qui écrit `bugfix-NN/code/decisions-produit.md`
Fermée par: `/fusion` ligne 6 nomme chaque `decisions-produit.md` au Rédacteur (3), et ligne 8 le Fusionneur (3) lit chaque `desc-bug.md` ; le test : un `questions-fusionneur-*` existe quelque part (la passe a tourné), puis `rapport-fusion.md`
Plafond: aucun — chaque `bugfix-NN` est une décision du Product Owner d'ouvrir un cycle ; la fusion tourne une fois, après le dernier
Au plafond: sans objet
Traverse: diagnostiqueur, cadreur, verificateur, detailleur, arbitre, concepteur, testeur, realisateur, relecteur, controleur, redacteur (3), fusionneur (3) ; `/diagnostique`, `/7_lots`, `/8_code`, `/9_controle`, `/fusion` — `PROCESS_ENTREES.md`, `PROCESS_AVAL.md`

### Blocage → décision → relance, l'amont

Ouverte par: l'un des dix agents écrit son `blocked_<agent>.md`
Fermée par: → MECANISMES §Blocage → décision → relance ; ici les variantes : `blocked_decoupeur.md` levé par `/2_structure` et non par `/3_decoupe` ; `blocked_qualifieur.md` et `blocked_classeur.md` levés par leur commande sur un genre ou une nature, par `/2_structure` sur une réécriture ; les six de `/4_grille` relançant la seule lecture qui a bloqué, au numéro du tour ; `blocked_redacteur.md` et `blocked_fusionneur.md` routés par `## Invocation` ; `blocked_architecte.md` par `## Invocation` entre `/conventions` et `/8_code`
Plafond: aucun
Au plafond: sans objet
Traverse: les dix agents ; les douze commandes ; `/8_code` pour `blocked_architecte.md` — `PROCESS_MECANISMES.md`, `PROCESS_AVAL.md`

## Inventaire

Agents décrits en entier : lexicographe (invocations 1, 2, 3, 4) · redacteur (1, 2, 3) · decoupeur · qualifieur · classeur · sondeur (1 — les trois angles en un bloc, 2, 3) · assembleur · convertisseur (1, 2) · architecte (1, 2, 3, 4, plus le bloc commun) · fusionneur (1, 2, 3).

Agents portés en entrée courte : aucun — l'Architecte (invocation 3) est porté en entrée courte dans `PROCESS_AVAL.md` depuis `/7_lots`, `/8_code` et l'arbitre ; aucun agent d'un autre document n'est invoqué ici.

Commandes décrites : `/1_lexique` · `/2_structure` · `/3_decoupe` · `/3a_genre` · `/3b_nature` · `/4_grille` · `/5_reclasse` · `/6_convertit` · `/conventions` · `/fusion` · `/fusion_compare` · `/fusion_applique`.

Mécanismes à un seul utilisateur que `MECANISMES` renvoie ici, et où ils sont : `blocking` · `assumed` · `misplaced` → §convertisseur, invocation 1 ; `mechanical` · `review` · `off-grid`, les mentions de `couverture.md`, V1–V10, C1–C12, R1–R7 → §architecte, bloc commun ; les passes A, B, C et `C1.2` → §sondeur, invocations 1 et 2 ; les fermetures de `GRILLE_FERMETURE_TECHNIQUE.md` → §convertisseur, invocations 1 et 2 ; `## Tranché`, les trois balayages, les quatre lectures d'une paire, `remplace :`, `dans ce sens seulement` → §lexicographe ; la table des préfixes → §redacteur, invocation 2 ; le test pour `transverse` et l'asymétrie → §qualifieur ; les frontières et les trois doutes → §classeur ; le critère du déclencheur → §decoupeur ; le test de fusion → §assembleur ; la réversibilité, la scission d'une règle transverse, les neuf sections → §convertisseur ; la table des natures qui tournent → §/6_convertit ; la table de routage à onze lignes, les trois niveaux, la liste de retrait, le rapport à quatre champs → §/fusion, §fusionneur ; la table à onze lignes de `/conventions` → §/conventions.
