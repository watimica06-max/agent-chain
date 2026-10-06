# PROCESS_ENTREES.md — les quatre entrées de la chaîne

> Document de pilotage, en français. Il décrit les quatre façons
> d'entrer dans la chaîne — `idees.md`, `/socle`, `/extrait`,
> `/diagnostique` — ce que chacune garantit à ce qui suit, et ce
> qu'elle laisse manquant. Il décrit en entier le seul agent que ces
> entrées invoquent, le Diagnostiqueur, en deux blocs, un par
> invocation. Tout protocole partagé est renvoyé par `→ MECANISMES
> §<nom>` au titre `###` exact de `PROCESS_MECANISMES.md` ; rien n'en
> est répété ici.

## Comment lire ce document

Chaque entrée est décrite sous la forme d'une commande — `Prend` ·
`Rend` · **Étapes** · **Git** · **La Product Owner intervient** ·
**Décisions** — plus deux sections propres aux entrées : **Ce qu'elle
garantit à la suite** et **Ce qu'elle laisse manquant**. `idees.md`
n'est pas une commande ; elle prend la même forme, ses étapes étant
celles du Product Owner et des deux premières commandes qui la
consomment. L'agent prend les neuf champs obligatoires plus
**Décisions** ; un champ vide est écrit `aucun`. `raison :` n'est
remplie que depuis une source ouverte — le fichier d'agent, le fichier
de commande, `docs/verification4/`, `docs/verification3/`,
`docs/verification2/`, `docs/verification/` — sinon `raison : à
retrouver` ; le statut suit la règle de `→ MECANISMES` (*Comment lire
une entrée*) : `éprouvée` seulement quand un fichier dit qu'un run l'a
exercée, `non éprouvée` pour toute décision de
`docs/verification4/plan.md`, `inconnu` sinon.

Un fait de disque, vérifié le jour de cette rédaction et rapporté parce
qu'il est auditable : `.claude/commands/` tient vingt fichiers et aucun
`extrait.md` ; `.claude/agents/` tient vingt fichiers et aucun
`extracteur.md` ; `.gitignore` du projet porte, lignes 18-19, les deux
lignes `docs/features/*/stop.md` et `docs/features/*/stop1.md` ;
`docs/PRODUIT_GLOBAL.md` (une ligne, `# Application`),
`docs/CURRENT_TECHNICAL_STATE.md` (2 305 lignes, dont `## Traps —
general` et `## Dead state`) et `docs/TECHNICAL_CONVENTIONS.md` existent ;
`docs/features/` existe et tient deux dossiers de feature,
`premiere-app/` et `premiere-app-2/` ;
`.claude/skills/technical-state-format/SKILL.md` existe.

---

# Entrée 1 — `idees.md`, l'idée libre

## `idees.md`

Prend: rien de la chaîne — le Product Owner crée `docs/features/<name>/`
et y écrit `idees.md` à la main, hors session, en français, en forme
libre. `<name>` est l'argument que chaque commande amont prendra.
Rend: `docs/features/<name>/idees.md`, le seul fichier du dossier de
feature qu'aucun agent n'a écrit, lu entier par le Lexicographe
(invocations 1 et 2) et par le Rédacteur (invocation 1), réécrit
terme à terme par le seul Lexicographe (invocation 2) (→ MECANISMES
§Disposition du dossier de feature, ligne `idees.md`).

**Étapes** — ce que l'entrée traverse avant que le fichier produit
existe ; les commandes elles-mêmes sont décrites dans
`PROCESS_AMONT.md`.

1. Le Product Owner écrit `idees.md`. Deux sortes de mots y coexistent
   et ne suivent pas la même règle : un texte affiché, entre
   guillemets, dans la langue où il s'affiche, gardé tel quel partout ;
   un concept, sans guillemets, quelle que soit la langue, rendu en
   anglais à partir du fichier produit (`lexicographe.md`, *The two
   kinds of word*). Un même mot peut être les deux — *"Démarrer"* le
   bouton et démarrer une course — et fait alors deux entrées du
   lexique.
2. `/1_lexique`, invocation 1 — Sweeping : le Lexicographe lit
   `idees.md` entier, écrit `lexique.md` et un fichier de questions,
   toujours, même vide (→ MECANISMES §lexique.md, §Fichier de
   questions — divergence). Le prompt porte `The idea file:
   docs/features/<name>/idees.md.` aux invocations 1 et 2 seulement.
3. `/1_lexique`, invocation 2 — Settling : le Lexicographe applique le
   fichier répondu à `idees.md` — un terme retiré remplacé à chaque
   occurrence hors guillemets, des guillemets ajoutés ou retirés à
   chaque occurrence quand la réponse tranche une citation — et rien
   d'autre : aucune phrase réécrite, aucune règle, précision ou exemple
   ajouté (`lexicographe.md`, *What you never do*). Puis invocation 1
   de nouveau, jusqu'à un `questions-lexicographe-NN.md` sans `### Q`.
4. `/2_structure`, invocation 1 — Structuring : le Rédacteur lit
   `idees.md`, `lexique.md` et l'index du global (→ MECANISMES
   §Lecture du global par l'index), et écrit `desc-produit.md`. La
   commande n'invoque 1 que si le plus haut
   `questions-lexicographe-NN.md`, à la racine ou sous
   `questions/lexicographe/`, ne tient aucun `### Q` — aucun nulle part,
   ou des entrées dedans → arrêt, `/1_lexique` d'abord — et si aucun
   `desc-produit.md` n'existe (`2_structure.md`, *How it runs*, deux
   dernières lignes de la table).
5. Après la transcription, plus personne n'ouvre `idees.md` : le
   Rédacteur à l'invocation 2 jamais (« it is transcribed; the answers
   revise what came of it »), le Convertisseur jamais, le Fusionneur
   jamais (« the raw text the upstream chain spent its whole loop
   correcting »), le Lexicographe aux invocations 3 et 4 jamais.
   `/1_lexique` s'arrête sur ses invocations 1 et 2 dès qu'un
   `desc-produit.md` existe et nomme `/3_decoupe` ; `/2_structure`
   s'arrête sur le même état et nomme le même pas.

**Git** — aucun geste propre à l'entrée. Le fichier, écrit hors
session, atteint le worktree par le commit `chore: answers` de
`/1_lexique` (`git add docs/features/<name>/`), avant la création du
worktree (→ MECANISMES §Git, avant l'invocation) ; non commité, il y
est invisible et le Lexicographe bloque sur *no idea file*.

**La Product Owner intervient** — elle crée `docs/features/<name>/` et
`idees.md` ; elle répond en français aux `Answer:` de chaque
`questions-lexicographe-NN.md` ; elle relance `/1_lexique` jusqu'au
fichier vide, puis `/2_structure`. Elle ne retouche jamais `idees.md`
après la première invocation 1 — rien ne l'interdit dans un fichier,
et rien ne le détecterait : voir *Ce qu'elle laisse manquant*.

**Ce qu'elle garantit à la suite**

- Au Lexicographe, invocation 1 : un fichier présent et non vide — ses
  deux seuls cas de blocage (`lexicographe.md`, *When you cannot
  produce*). Rien d'autre n'est testé.
- Au Rédacteur, invocation 1 : un vocabulaire réglé — le plus haut
  `questions-lexicographe-NN.md` sans `### Q` — et un `lexique.md`
  qui dit le terme qui tient et quelles chaînes sont des textes
  affichés (`redacteur.md`, *INVOCATION 1 — Structuring*, *Inputs*).
- Un seul sujet — *ce que ça fait en une phrase, sans « et »* ; deux
  sujets sans lien et le Rédacteur écrit `blocked_redacteur.md` (« Two
  features share no product file »).
- Rien de plus : pas de structure, pas de genre, pas de nature, pas
  d'attachement au global — le Rédacteur décompose une phrase en autant
  de sujets qu'elle porte de déclencheurs et de sorties, et cherche le
  titre du global par l'index (`redacteur.md`, mouvements 1 à 3).

**Ce qu'elle laisse manquant**

- Qui crée `docs/features/<name>/` : aucun fichier de commande ni
  d'agent ne le dit ; `/socle` crée `docs/features/` vide et s'arrête
  là. Un `<name>` sans dossier ne fait échouer aucun test nommé —
  `/1_lexique` cherche `blocked_lexicographe.md` par `Glob`, ne le
  trouve pas, invoque, et le Lexicographe bloque sur *no idea file*,
  ce qui crée le dossier par l'écriture du fichier de blocage.
- Le passage transcrit une fois : aucune commande ne compare `idees.md`
  au fichier produit après coup, et un `idees.md` modifié par le
  Product Owner après `/2_structure` n'est relu par personne — la
  correction passe par un fichier de questions, ou par un
  `bugfix-NN/` après le code.
- Un `idees.md` qui couvre deux features n'est détecté qu'au Rédacteur,
  après un ou plusieurs tours de `/1_lexique` faits sur les deux.
- Le fichier ne porte ni date ni numéro : `/4_grille` (L204-208) note
  qu'une intégration hors grille, `idees.md` compris, laisse survivre
  les marqueurs d'un tour antérieur — coût accepté, sonder deux fois.

**Décisions**

- Une idée en forme libre, en français · écartée : un gabarit à
  remplir · raison : « The Product Owner writes freely, and that is the
  point » (`lexicographe.md`, *Role*) ; « free-form and in French, that
  is the point » (`redacteur.md`, invocation 1) · inconnu
- Le vocabulaire réglé dans l'idée, avant le fichier produit, jamais
  après · écartée : régler les termes dans le fichier produit · raison :
  « a term changed then would leave sixty blocks carrying the old one »
  (`1_lexique.md`, *Which invocation*) ; « A term changed once sixty
  blocks carry it is sixty edits » (`2_structure.md`) · inconnu
- Le Lexicographe seul écrit dans `idees.md`, un terme à la fois ·
  écartée : lui laisser réécrire une phrase · raison : il dit ce que
  les termes peuvent vouloir dire, le Product Owner dit lequel tient ;
  une phrase réécrite serait un choix produit (`lexicographe.md`, *What
  you never do*) · inconnu
- L'idée transcrite une fois ; une seconde invocation 1 refusée par
  `/2_structure` · écartée : retranscrire sur demande · raison : « A
  second invocation 1 over an existing product file renumbers or
  duplicates every block — and every filed question then points at the
  wrong one » (`2_structure.md`) · inconnu
- Les textes affichés entre guillemets, les concepts sans · écartée :
  aucune marque, tout traduit · raison : les guillemets portent ce qui
  atteint l'écran caractère pour caractère ; un concept est rendu en
  anglais dès le fichier produit (`lexicographe.md`, *The two kinds of
  word*) · inconnu
- Un fichier d'idée, une feature · écartée : plusieurs sujets dans un
  fichier · raison : « Two features share no product file »
  (`redacteur.md`, invocation 1) · inconnu
- Aucun jugement de complétude à l'entrée · écartée : un agent qui
  relit l'idée pour ses trous · raison : « finding gaps is the
  sondeurs' work » (`redacteur.md`, mouvement 4) · inconnu

---

# Entrée 2 — `/socle`, l'application neuve

## /socle

Prend: aucun argument (`socle.md`, frontmatter sans `argument-hint` ;
→ MECANISMES §Frontmatter d'une commande — `allowed-tools: Read, Grep,
Glob, Edit, Write, Bash`, sans `Agent`).
Rend: `docs/PRODUIT_GLOBAL.md` à une ligne, `# Application` ;
`docs/features/` vide ; deux lignes dans `.gitignore` à la racine du
projet, `docs/features/*/stop.md` et `docs/features/*/stop1.md` ;
`docs/CURRENT_TECHNICAL_STATE.md` à une ligne, `# Technical state` ; un
commit `chore: scaffolding for the chain`, poussé ; un rapport disant
ce qu'il reste au Product Owner à fournir.

**Étapes**

1. Tester `docs/PRODUIT_GLOBAL.md` : présent → arrêt, rien n'est
   créé. Le fichier de commande énonce ce test après la liste des
   créations, mais il gouverne la commande entière (« This command is
   for a new application, and overwriting the global would lose every
   domain in it »).
2. Créer `docs/PRODUIT_GLOBAL.md` avec `# Application` pour seule ligne
   (→ MECANISMES §Lecture du global par l'index).
3. Créer `docs/features/` vide.
4. Ajouter à `.gitignore`, à la racine du projet, les deux lignes
   `docs/features/*/stop.md` et `docs/features/*/stop1.md` — ajoutées
   si absentes, jamais le fichier réécrit (→ MECANISMES §stop.md).
5. Créer `docs/CURRENT_TECHNICAL_STATE.md` avec `# Technical state`
   pour seule ligne (→ MECANISMES §Lecture de l'état technique).
6. Ne pas créer `docs/TECHNICAL_CONVENTIONS.md`, et le dire : l'Architecte
   l'écrit à `/conventions`, lancé à la main après `/6_convertit` et
   avant `/7_lots`.
7. Rapporter ce que le Product Owner doit encore fournir avant que la
   chaîne tourne de bout en bout : `docs/TECHNICAL_CONVENTIONS.md`, par
   `/conventions` et non à la main ; la compétence
   `technical-state-format`, chargée par le Réalisateur et l'Arbitre
   avant d'écrire dans l'état technique. Ni l'un ni l'autre ne bloque
   l'amont — seulement `/7_lots` et la suite. Le rapport finit sur
   `Next: manual écrire docs/features/<name>/idees.md, then run
   /1_lexique <name>` ; l'arrêt de l'étape 1 sur `Next: stop
   docs/PRODUIT_GLOBAL.md already exists` (→ MECANISMES §Ligne Next:).
8. Commit seul, `chore: scaffolding for the chain`, et push.

**Git** — → MECANISMES §Commit sans worktree : aucun agent, aucun
worktree, la commande écrit en place dans le dépôt principal et
commite ; un push qui échoue est rapporté, pas retenté.

**La Product Owner intervient** — elle lance `/socle` une fois, sur un
projet dont `docs/PRODUIT_GLOBAL.md` n'existe pas ; elle fournit ce que
le rapport nomme ; elle crée ensuite `docs/features/<name>/idees.md`
(entrée 1). Aucune question, aucun fichier de blocage : la commande
n'invoque personne.

**Ce qu'elle garantit à la suite**

- Au Rédacteur (invocation 1), au Fusionneur, au Sondeur (invocation
  3) : un global dont le seul titre est `# Application` — l'index
  greppé sur `^#` ne rend rien à couvrir, et le Fusionneur y lit
  `INIT` (→ MECANISMES §Les verbes du plan de fusion — ce qu'une
  phrase devient ; `/fusion` copie alors `desc-produit-fusion.md` sur
  le global avant d'invoquer). L'invocation 3 du Fusionneur teste le
  même titre seul pour savoir où écrire.
- Au Détailleur, au Réalisateur, au Diagnostiqueur : un état technique
  présent, dont les deux sections ouvertes `## Traps — general` et
  `## Dead state` n'existent pas encore au sortir de `/socle` — le
  fichier n'a que `# Technical state`, un grep du titre ne rend rien,
  la lecture bornée ne lit rien ; elles apparaissent quand le
  Réalisateur ou l'Arbitre y écrit, sous la compétence
  `technical-state-format` qui fixe ces deux titres (sur ce projet,
  après les lots codés, le fichier a 2 305 lignes et les porte, lignes
  1985 et 2297) ; au Réalisateur et à l'Arbitre, un fichier où écrire
  sous cette compétence.
- À `/8_code` : deux lignes de `.gitignore` qui gardent `stop.md` et
  `stop1.md` hors de tout commit — la commande les cherche dans le
  dépôt principal, jamais dans le worktree (→ MECANISMES §stop.md).
- À toute commande : `docs/features/` comme racine des dossiers de
  feature (→ MECANISMES §Disposition du dossier de feature).

**Ce qu'elle laisse manquant**

- `docs/TECHNICAL_CONVENTIONS.md` — l'Architecte, invocation 1, à
  `/conventions` (`PROCESS_AMONT.md` §architecte, invocation 1 — Deriving : la première dérivation du dépôt, §/conventions).
- `docs/features/<name>/` et `idees.md` — le Product Owner, entrée 1.
- Les quatre grilles de `.claude/grids/` — `GRILLE_CADRAGE_PRODUIT_V2.md`
  (Sondeur 1, 2), `GRILLE_EXISTANT.md` (Sondeur 3),
  `GRILLE_FERMETURE_TECHNIQUE.md` (Convertisseur, Diagnostiqueur 2),
  `GRILLE_CONVENTIONS.md` (Architecte) : `/socle` n'en crée aucune ;
  elles font partie de la chaîne, que le cockpit installe dans chaque
  application ; `CLAUDE.md` dit que la chaîne tourne sur plusieurs projets.
- `.claude/` entier, `.claude/scripts/grouper.py` compris : hors de
  `/socle`.
- La compétence `technical-state-format` : `/socle` la rapporte comme à
  fournir par le Product Owner ; sur ce projet elle est livrée avec
  `.claude/skills/`.
- `docs/features/` vide n'entre dans aucun commit : git ne suit pas un
  dossier vide. Le commit `chore: scaffolding for the chain` porte
  trois fichiers, pas quatre, et un clone n'a pas `docs/features/`
  avant la première feature.
- Le seul arrêt teste le global : un `docs/CURRENT_TECHNICAL_STATE.md`
  déjà présent sans global n'arrête rien, et le fichier de commande ne
  dit pas s'il est réécrit ou laissé.
- Sur ce projet, rien de ce que `/socle` crée ne manque au disque :
  `.gitignore` porte les deux lignes (18-19), les trois fichiers
  existent, et `docs/features/` tient déjà deux dossiers de feature —
  la vérification ne dit rien de plus sur le run qui les a posés.

**Décisions**

- Arrêt sur un global existant · écartée : réécrire le global · raison :
  « overwriting the global would lose every domain in it »
  (`socle.md`) · inconnu
- `.gitignore` en ajout, jamais réécrit · écartée : écrire le fichier ·
  raison : à retrouver · inconnu
- Ne pas créer `docs/TECHNICAL_CONVENTIONS.md` · écartée : un fichier
  vide à compléter · raison : l'Architecte l'écrit à `/conventions`,
  et à son invocation 1 il ne lit aucun fichier au nom de *convention*
  (→ MECANISMES §Lecture des conventions — divergence) · inconnu
- Deux scripteurs de l'état technique nommés — le Réalisateur dès le
  premier lot, l'Arbitre pour le piège de plateforme · écartée : le
  Réalisateur seul · raison : `docs/verification2/arbitre.md` F21 et
  `docs/verification2/plans/arbitre.md` (« Name the Arbitre in
  `socle.md` as a writer of `CURRENT_TECHNICAL_STATE.md` (traps) and a
  loader of the skill, beside the Réalisateur ») · inconnu
- Le Cadreur nommé comme non-lecteur de l'état technique · écartée :
  le nommer lecteur · raison : « it establishes what the code carries
  by grep » (`socle.md` ; → MECANISMES §Lecture de l'état technique)
  · inconnu
- Aucun agent, aucun worktree · écartée : un worktree systématique ·
  raison : → MECANISMES §Commit sans worktree · inconnu
- `stop.md` et `stop1.md` jamais commités, d'où les deux lignes ·
  écartée : les commiter · raison : « Neither is ever committed, which
  is why both are ignored » (`socle.md`) ; le fichier est créé dans le
  dépôt principal et n'atteint pas un worktree coupé avant lui (→
  MECANISMES §stop.md) · inconnu

---

# Entrée 3 — `/extrait`, la feature existante

## /extrait

**La commande n'existe pas dans la chaîne au jour de cette
refonte.** `Get-ChildItem .claude/commands` rend vingt fichiers, aucun
`extrait.md` ; `.claude/agents/` rend vingt fichiers, aucun
`extracteur.md` ; `CLAUDE.md` ne la liste pas dans sa table des
commandes, et le registre des agents de `→ MECANISMES §Frontmatter
d'un agent` ne porte aucun extracteur. Le brief de cette refonte la
nomme comme troisième entrée ; la carte des cinq documents de
`PROCESS_MECANISMES.md` ne la compte pas parmi les entrées et renvoie
à cette section pour ce qu'elle enregistre. Ce document dit ce qu'il y
a, et ne l'invente pas.

Prend: aucun.
Rend: aucun.

**Étapes** — aucune.

**Git** — aucun.

**La Product Owner intervient** — aucun.

**Ce que les dossiers de vérification en disent.** L'ancienne chaîne
portait un agent `extracteur` et une commande `/extrait` ; la refonte
les a supprimés. `docs/verification/renommages.md`, *Agent
`extracteur`* : « No `agents/extracteur.md`, no `commands/extrait.md`,
no occurrence of `extracteur` or `/extrait` in `.claude-new/` or
`docs-new/` … The `CLAUDE.md` command table L51 does not list it. »
`docs/verification/agent-diagnostiqueur.md` B′-2 : « The chain no
longer has an Extracteur ». `docs/verification/agent-fusionneur.md` :
« `CLAUDE.md` no longer lists an `extracteur` agent nor an `/extrait`
command ». `docs/verification2/fusionneur.md` F05 et B-1 : la
référence à l'Extracteur a été retirée du Fusionneur, « the Extracteur
is gone from the chain, and the line stands without it ». Le rôle que
l'Extracteur tenait — faire naître le global depuis un code existant —
est aujourd'hui tenu par le Fusionneur seul : le global naît de
`INIT` sur la première feature fusionnée (→ MECANISMES §Les verbes du
plan de fusion — ce qu'une phrase devient), et `/socle` le crée vide.

**Ce que la chaîne tient sous le mot « existant ».** Une recherche de
`extrait`, `extract`, `existant`, `GRILLE_EXISTANT` sous `.claude/`
rend une seule mécanique, qui n'est pas une extraction :

- `.claude/grids/GRILLE_EXISTANT.md` — la *grille de l'existant*. Elle
  ferme une feature **contre le produit déjà construit**, quand la
  grille de cadrage l'a fermée sur elle-même : elle tourne une fois,
  après que la grille de cadrage a rendu un fichier de questions vide,
  sur les seuls blocs qui portent une ligne `Global:`, chaque question
  étant posée à un bloc et à la section du global qu'il nomme,
  ensemble. Ce qu'elle lève est une arbitration — deux choses vraies à
  la fois qui ne peuvent rester toutes deux — jamais un manque, et
  chaque question porte un identifiant `E<n>.<m>` que celui qui répond
  recopie. Une arbitration répondue devient un bloc de la feature, y
  compris celui qui dit ce que devient la chose existante ; le
  Fusionneur le rapporte au global. Quatre parties : ce que le bloc
  prend et qu'autre chose tient déjà, ce que le bloc dit et que la
  section dit autrement, ce que la feature retire sans le dire, le test
  de clôture. Ses questions ne sont pas copiées ici.
- Qui la lit aujourd'hui : le Sondeur, invocation 3 — l'entrée courte
  ci-dessous, et rien de plus ici.
- Ce qui en découle ailleurs : `/5_reclasse` teste le plus haut
  `questions-existant-NN.md` sans `### Q` avant de reclasser ; le
  Rédacteur retire tous les marqueurs quand le fichier intégré a pour
  préfixe `existant` (→ MECANISMES §Marqueurs NEW et MODIFIED) ; le
  préfixe `existant` est un préfixe de grille, pas un agent
  (`redacteur.md` L136).

### sondeur, invocation 3 — ce que l'entrée `/extrait` en retient

Ce qui change : rien dans l'invocation — `/4_grille` l'invoque au
second temps, `PROCESS_AMONT.md` la décrit. Ce que cette entrée en
retient : la lecture de `GRILLE_EXISTANT.md` est la seule mécanique
de la chaîne sur l'existant — elle ferme une feature contre le global
déjà écrit, section nommée par section nommée, jamais contre le code ;
elle ne remplace pas l'extraction supprimée, et un comportement que le
code porte sans qu'aucune feature l'ait décrit lui reste invisible.
Description complète : `PROCESS_AMONT.md` §sondeur, invocation 3 — Existant : la feature contre ce qui est déjà bâti

Rien de cela ne prend une feature déjà codée pour en écrire le fichier
produit ou le global : l'entrée par extraction n'a, dans cette chaîne,
ni commande, ni agent, ni fichier de sortie.

**Ce qu'elle garantit à la suite** — rien.

**Ce qu'elle laisse manquant** — l'entrée entière. Un projet dont le
code existe avant la chaîne n'a aucune commande qui écrive
`docs/PRODUIT_GLOBAL.md` depuis ce code : `/socle` le crée à
`# Application`, et le Fusionneur le remplit feature après feature
depuis les fichiers produit. Un comportement que le code porte et
qu'aucune feature n'a décrit reste invisible au Sondeur 3 — sa grille
lit le global, pas le code — et au Diagnostiqueur, qui confirme un
manque que le Product Owner a listé et ne découvre rien.

**Décisions**

- Supprimer l'Extracteur et `/extrait` ; le global naît du Fusionneur ·
  écartée : garder un agent qui écrit le global depuis le code ·
  raison : à retrouver — les dossiers de vérification constatent la
  suppression (`docs/verification/renommages.md`, *Agent
  `extracteur`* ; `docs/verification/agent-diagnostiqueur.md` B′-2) et
  n'en portent pas le motif ; celui-ci est dans `docs/refonte/`, hors
  des sources de ce document · inconnu

---

# Entrée 4 — `/diagnostique`, le manque constaté

## /diagnostique

Prend: le nom du dossier de feature, obligatoire — sans lui la commande
demande et s'arrête (`argument-hint: "<feature folder name>"` ;
`allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Agent`, →
MECANISMES §Frontmatter d'une commande). Le dossier de travail est le
`bugfix-NN/` de numéro le plus haut dans `docs/features/<name>/`,
créé à la main par le Product Owner avec `bug-list.md` dedans ; pas de
dossier, ou pas de `bug-list.md` → la commande le dit et s'arrête, et
n'en crée jamais (→ MECANISMES §Dossier de travail).
Rend: `bugfix-NN/investigation/<id>.md`, un par manque investigué ;
`bugfix-NN/desc-bug.md`, le document technique du cycle de correction ;
le cas échéant `bugfix-NN/investigation/blocked_<id>.md` et
`bugfix-NN/blocked_diagnostiqueur.md` ; les renommages `-NN` des
fichiers de blocage appliqués ; un commit fusionné et poussé ; le
rapport de l'agent relayé, et *What to run next* : `/7_lots`.

**Étapes**

1. Lire `bug-list.md`, et seulement pour le scinder manque par manque
   — jamais pour juger, réécrire ou fusionner un manque (→ MECANISMES
   §Ce que l'orchestrateur lit, exception déclarée). Chaque manque ouvre
   sur son `G<n>` (`G01`, `G02`), écrit par le Product Owner, lu sur la
   ligne et jamais compté depuis la position ; un manque tiré d'un
   rapport de contrôle porte déjà son `(B<n>)` entre parenthèses en fin
   de première ligne (→ MECANISMES §Identifiants, lignes `G<n>` et
   `B<n>`). Un manque qui n'ouvre sur aucun `G<n>` → arrêt avant tout
   envoi, la ligne nommée.
2. Trier chaque manque de `bug-list.md` avant d'envoyer quoi que ce
   soit, sur ce que `investigation/` tient pour son identifiant — un
   `Glob` sur `investigation/*.md`, un fichier de blocage ouvert pour
   son seul `## Decision` (→ MECANISMES §États de « ## Decision » — ce
   qu'un fichier de blocage attend) — la première ligne qui correspond
   décide :

   | Pour `<id>` | Phase 1 |
   |---|---|
   | `investigation/blocked_<id>.md`, `## Decision` rempli | Envoyé, le fichier nommé au prompt — l'agent applique puis investigue |
   | `investigation/blocked_<id>.md`, `## Decision` vide | Sauté, relayé comme debout — rien n'a changé depuis qu'il a été écrit |
   | `investigation/<id>.md` existe | Sauté — un rapport existant est fait |
   | Rien | Envoyé |

   C'est ainsi qu'une seule investigation échouée est rejouée : le
   Product Owner remplit son fichier de blocage, relance la commande,
   et seul ce manque part. Une phase 1 qui n'envoie rien est normale.
3. Avant d'envoyer la phase 2, `Glob` `desc-bug.md` dans le dossier —
   ici, avant le commit et avant la phase 1 : il existe → ni la phase 2
   ni la phase 1 ne sont envoyées, aucun geste git, le fichier est
   relayé comme fait, et le pas suivant est `/7_lots`. Les tests des
   étapes 1 à 3 passent avant tout geste sur le dépôt.
4. Git avant l'invocation, → MECANISMES §Git, avant l'invocation :
   `git add docs/features/<name>/ && git commit -m "chore: answers"`
   — le Product Owner écrit `bug-list.md` hors session, et un worktree
   branche sur le dernier commit ; `git worktree add
   .claude/worktrees/<name> HEAD` ; entrée dans le worktree avant
   d'invoquer.
5. Phase 1 — un `Agent()` par manque à envoyer, tous dans un seul
   message (→ MECANISMES §Invocation d'un agent) :
   `subagent_type="diagnostiqueur"`, `model="sonnet"`,
   `description="investigate G01 <feature>"`, prompt `Bug-fix folder:
   docs/features/<name>/bugfix-NN/.` · `Invocation 1 —
   Investigation.` · `Gap G01: <le texte du manque, mot pour mot>.` ·
   `[Blocking file: investigation/blocked_G01.md — its ## Decision is
   filled.]` sur la seule première ligne de la table. Chaque appel porte
   un manque et son identifiant, rien des autres. Attendre chaque
   rapport avant la phase 2 ; un appel qui rend un fichier de blocage
   n'arrête pas les autres. Les appels ne se heurtent pas : chacun écrit
   `investigation/<id>.md`, son fichier et aucun autre.
6. Porte de la phase 2 — elle ne part que si chaque rapport existe. Un
   blocage de phase 1 la retient : un manque dont l'investigation a
   bloqué n'a pas de rapport, et l'invocation 2 ne ferait que bloquer à
   son tour sur un fichier auquel aucune décision ne peut fournir un
   rapport. Les identifiants bloqués sont rapportés depuis les propres
   résultats de la phase 1 — les appels qui ont rendu un fichier de
   blocage, et les manques sautés comme debout — et la commande
   s'arrête là.
   Cette porte vient après le commit et le worktree : elle lit les
   résultats de la phase 1. Quand la phase 1 n'envoie rien, elle ne
   repose que sur le tri ; le Git d'après le rapport referme alors le
   worktree comme à toute autre fin (étape 9).
7. Phase 2 — un `Agent()`, une fois que chaque rapport existe et
   qu'aucun `desc-bug.md` n'existe : `subagent_type="diagnostiqueur"`,
   `model="sonnet"`, `description="assemble <feature>"`, prompt
   `Bug-fix folder: docs/features/<name>/bugfix-NN/.` · `Invocation 2
   — Assembly.` · `[Blocking file: blocked_diagnostiqueur.md — its
   ## Decision is filled.]` seulement quand ce fichier est là avec un
   `## Decision` rempli. Ni `effort`, ni `run_in_background`, ni
   `isolation` (la phase 2 lit ce que la phase 1 a écrit) ; jamais une
   paraphrase du processus de l'agent.
8. Renommer, une fois que l'agent rapporte avoir appliqué la décision —
   le même geste pour les deux fichiers, dans le worktree, avant les
   cinq pas (→ MECANISMES §Renommage -NN — divergence) :
   `git mv investigation/blocked_<id>.md investigation/blocked_<id>-NN.md`
   et `git mv blocked_diagnostiqueur.md blocked_diagnostiqueur-NN.md`,
   `NN` le plus haut à côté plus un, `01` sans précédent, compté par
   fichier — parmi les `investigation/blocked_<id>-NN.md` de cet
   identifiant, parmi les `blocked_diagnostiqueur-NN.md` de la racine.
   Une décision remplie laissée au nom non numéroté renvoie le manque
   au run suivant, et `/audit_blocages` la liste comme encore ouverte.
9. Git à toute fin du run une fois le worktree créé, un arrêt compris —
   la phase 2 retenue, que la phase 1 ait envoyé des appels ou aucun —
   → MECANISMES §Git, après le rapport — les cinq pas ; jamais de
   `remove` forcé ; un `blocked_*.md` fusionne aussi.
10. Relayer, → MECANISMES §Forme d'un relais : le rapport de l'agent et
    rien de plus. Un fichier de blocage en phase 1 est
    `investigation/blocked_<id>.md` et les autres appels continuent ;
    en phase 2 c'est `blocked_diagnostiqueur.md` et la commande
    s'arrête. Une phase 2 non envoyée est expliquée : `desc-bug.md`
    existe → fait, `/7_lots` ; phase 2 retenue → la liste de chaque
    identifiant debout, depuis les résultats de la phase 1, jamais un
    identifiant tiré d'un blocage d'invocation 2 — il n'y en a pas. Un
    `## Decision` rempli → `/diagnostique` de nouveau. Le relais finit
    sur la ligne `Next:` de son issue, arrêts compris — `Next: run
    /7_lots <name>` quand la phase 2 a écrit `desc-bug.md`, `Next:
    answer blocking, then run /diagnostique <name>` sur un fichier de
    blocage (→ MECANISMES §Ligne Next:).

**Git** — `chore: answers` avant le worktree ; worktree depuis `HEAD`
local ; renommages dans le worktree avant les cinq pas ; cinq pas ; le
push fait partie de la fusion, un push qui échoue est rapporté. Tout →
MECANISMES §Git, avant l'invocation, §Git, après le rapport — les cinq
pas, §Renommage -NN — divergence. L'agent n'a pas `Bash` : c'est la
commande qui commite ses fichiers au pas 1.

**La Product Owner intervient** — avant : elle crée `bugfix-NN/`, le
numéro libre suivant, et y écrit `bug-list.md` à la main, un manque par
`G<n>`, en forme libre après l'identifiant — une phrase nommant ce qui
est faux et ce que ce devrait être, un comportement et non un fichier
(`diagnostiqueur.md`, *What a gap looks like*) ; un manque qu'elle
prend d'un `code/rapport-controle.md` garde son `(B<n>)` en fin de
première ligne (`9_controle.md`, *What you relay*). Pendant : elle
remplit le `## Decision` d'un `investigation/blocked_<id>.md` ou de
`blocked_diagnostiqueur.md`, et relance `/diagnostique`. Après : elle
lance `/7_lots`. Aucune question ne lui est posée dans ce cycle
(`diagnostiqueur.md`, mouvement 9 : « nobody answers a question in
this cycle »).

**Ce qu'elle garantit à la suite**

- À `/7_lots`, `/8_code`, `/9_controle` : un dossier de travail
  `bugfix-NN/` avec `desc-bug.md` à sa racine — le document technique
  du cycle, à la place de `spec-technique.md`, jamais les deux (→
  MECANISMES §Dossier de travail, §Fichiers de la conversion, second
  paragraphe).
- Au Cadreur : une entrée par porteur, chaque entrée ouvrant sur une
  ligne `Bearer:` — un symbole, ou `none` — dont il fait l'inventaire
  `## Symbols` et la couche de chaque lot ; un `(B<n>)` en fin de titre
  d'entrée qu'il copie dans l'`Anchor:` du lot (`cadreur.md`, *What a
  bug-fix cycle changes*) ; sur `Bearer: none`, la décision d'où la
  chose atterrit lui revient.
- Au Vérificateur et au Détailleur : un `# Preamble` de trois lignes
  `Intent:`, `Out of scope:`, `Dependencies:` — une ligne
  `Dependencies:` et pas de `Vocabulary` (`verificateur.md` L64 ;
  `detailleur.md` L629 : les termes sont ceux de la feature).
- À l'Arbitre : le document qui nomme le cycle où il se trouve
  (`arbitre.md` L64).
- Au Fusionneur, invocation 3 : `desc-bug.md`, jamais `bug-list.md` —
  un manque écarté n'a produit aucun code et reste dans `desc-bug.md`
  avec sa raison ; un `bugfix-*/` sans `desc-bug.md` et l'invocation ne
  tourne pas (`fusionneur.md`, invocation 3).
- À `/9_controle` : le `(B<n>)` conservé de `bug-list.md` au titre
  d'entrée, puis à l'`Anchor:` du lot, d'où la marque `carried` (→
  MECANISMES §Marque carried).
- Des entrées numérotées `§n.m` à l'écriture, jamais renumérotées, dans
  neuf sections toujours présentes (→ MECANISMES §Identifiants).

**Ce qu'elle laisse manquant**

- Aucun test de zéro entrée : `/7_lots` greppe `^### §` sur
  `spec-technique.md` seul (`7_lots.md` L72) ; un `desc-bug.md` dont
  chaque manque est écarté a neuf sections vides et un `## Gaps set
  aside` plein, et rien dans `/7_lots` ne l'arrête avant le Cadreur.
- Pas de `couverture.md`, pas de `tracabilite.md`, pas de
  `## Cross-cutting rules`, pas de `Consumes:` : le Cadreur ne lit
  aucune ligne `Consumes:` sur un cycle de correction, l'Architecte
  écrit `couverture.md` un niveau au-dessus, et `/audit_conventions`
  saute sa trouvaille 7 quand `couverture.md` trace vers
  `spec-technique.md` (`docs/verification4/plan.md` entrée 39).
- `## Gaps set aside` n'a aucun lecteur dans la chaîne : le Fusionneur
  lit des entrées, et une ligne de cette section n'en est pas ; le
  Product Owner seul la relit, et un manque écarté revient par un
  `bug-list.md` ultérieur si elle le reprend.
- Un manque que le Product Owner n'a pas listé n'existe pas : l'agent
  confirme, ne découvre pas — « You settle nothing. What belongs in the
  cycle is the Product Owner's call ».
- Ce que devient une investigation dont le rapport existe mais est
  faux : la ligne 3 de la table saute tout manque à rapport existant,
  et aucun geste n'invalide un rapport — le Product Owner supprime le
  fichier à la main, ou écrit un nouveau manque.
- Le numéro `NN` de `bugfix-NN/` : choisi par le Product Owner, jamais
  vérifié — deux dossiers de même numéro, ou un trou, ne sont testés
  nulle part ; `/fusion` (ligne 8, tous les `bugfix-*/` à la fois) et
  le Fusionneur (du plus ancien au plus récent) supposent l'ordre.

**Décisions**

- Un manque à rapport existant est sauté · écartée : rejouer chaque
  investigation à chaque lancement · raison : « an existing report is
  done; a re-run costs a full investigation » (`diagnostique.md`,
  *How it runs*) · inconnu
- Un manque dont le fichier de blocage tient un `## Decision` vide est
  sauté et relayé comme debout · écartée : le renvoyer et laisser
  l'agent s'arrêter · raison : une invocation perdue par lancement tant
  que le Product Owner n'a pas répondu
  (`docs/verification2/diagnostiqueur.md` F18 ;
  `docs/verification2/plans/conflits.md` 256) · inconnu
- La phase 2 retenue tant qu'un blocage de phase 1 tient · écartée :
  lancer la phase 2 et la laisser bloquer sur le rapport manquant ·
  raison : un blocage de phase 1 coûtait deux décisions, dont une qui
  ne décidait rien (`docs/verification2/chemins-aval.md` F12 ;
  `docs/verification2/plans/conflits.md` 257) · inconnu
- `Glob` `desc-bug.md` avant le commit et la phase 1 ; existant → rien
  n'est envoyé, relayé comme fait · écartée : laisser l'agent bloquer sur le fichier
  existant · raison : un blocage qu'aucune décision ne lève — l'agent
  n'a aucun outil qui supprime, rien ne dit à l'orchestration de le
  faire (`docs/verification2/diagnostiqueur.md` F07, F16 ;
  `docs/verification2/plans/conflits.md` 246) · inconnu
- La commande renomme les deux fichiers de blocage, par identifiant ·
  écartée : renommer `blocked_diagnostiqueur.md` seul · raison : un
  `investigation/blocked_<id>.md` appliqué gardait son `## Decision`
  rempli, la ligne de saut rejouait le manque à chaque lancement, et
  `/audit_blocages` le listait ouvert (`docs/verification2/fichiers.md`
  F05 ; `docs/verification2/diagnostiqueur.md` F17 ;
  `docs/verification2/plans/conflits.md` 255) · inconnu
- `G<n>` écrit par le Product Owner, lu sur la ligne ; un manque sans
  identifiant arrête · écartée : compter par position, avec une règle
  « un manque ajouté va à la fin » (Option 1) · raison : un manque
  inséré entre deux runs décalait les identifiants, un
  `investigation/G02.md` existant était sauté pour un manque qu'il ne
  décrit pas, et l'invocation 2 bloquait sur un écart qu'aucune
  décision ne lève (`docs/verification4/plan.md` entrée 40, item I,
  Option 2) · non éprouvée
- Le dossier `bugfix-NN/` et `bug-list.md` jamais créés par la
  commande · écartée : créer le dossier au premier lancement ·
  raison : à retrouver · inconnu
- Ni grille, ni Convertisseur, ni Fusionneur sur une correction ·
  écartée : repasser l'amont · raison : « the product already says
  what is expected, and a correction adds nothing to it »
  (`diagnostique.md`) · inconnu
- Un appel par manque, tous dans un message, chacun ne portant qu'un
  manque · écartée : un appel sur la liste entière · raison : « You
  never see the others, and nothing you write depends on them »
  (`diagnostiqueur.md`, invocation 1) ; un nom de fichier par
  identifiant pour que dix appels ne se heurtent pas (→ MECANISMES
  §Emplacement des fichiers de blocage) · inconnu
- Les identifiants bloqués relayés depuis les résultats de la phase 1,
  jamais depuis un blocage d'invocation 2 · écartée : lire le fichier
  de blocage de l'assemblage · raison : « there is none » quand la
  phase 2 est retenue (`diagnostique.md`, *What you relay* ;
  `docs/verification2/plans/conflits.md` 257) · inconnu
- `bug-list.md` lu par l'orchestrateur, seule lecture d'un contenu
  qu'il fait ici · écartée : passer le fichier entier à un agent qui le
  scinde · raison : dix écarts dans un seul contexte sont dix séries de
  greps qui s'accumulent, une investigation ne voit que son écart et
  rien de ce qu'elle cherche n'aide les autres ; la commande découpe la
  liste en écarts identifiés, un par appel, et passe le texte de chacun
  verbatim — elle les lit pour les distribuer, jamais pour les juger,
  les réécrire ou les fusionner (PROCESS_AVAL-avant-refonte.md
  L633-639, L892-896) · inconnu

---

### diagnostiqueur, invocation 1 — Investigation : confirmer un manque contre le code

Modèle: sonnet · effort medium · outils: Read, Grep, Glob, Write
Invoquée par: `/diagnostique`, phase 1 — un appel par manque à
envoyer, tous dans un seul message, après le tri sur `investigation/` ;
jamais par un autre agent ni une autre commande.
Lit: le manque, dans le prompt (`Gap G<n>: <texte>`), et son identifiant
· `docs/TECHNICAL_CONVENTIONS.md`, entier, avant de chercher, pour les
dossiers de code du projet (→ MECANISMES §Lecture des conventions —
divergence) · le code, par grep avec chemin, plus le corps de chaque
appelant du porteur au seul mouvement 5 (→ MECANISMES §Grep du code
avec chemin) · `docs/CURRENT_TECHNICAL_STATE.md`, ses seules sections
`## Traps — general` et `## Dead state`, par grep du titre puis lecture
bornée jusqu'au `## ` suivant (→ MECANISMES §Lecture de l'état
technique) · son propre fichier de blocage `investigation/blocked_<id>.md`
et les `-NN` réglés à côté, par un `Glob` `investigation/blocked_<id>*.md`
· jamais `bug-list.md`, jamais le fichier produit, le document
technique, le global, jamais un fichier d'une autre investigation.
Écrit: `investigation/<id>.md`, `<id>` l'identifiant du prompt — un
fichier, le sien seul · `investigation/blocked_<id>.md` quand produire
est impossible (forme 1, → MECANISMES §Fichier de blocage —
divergence).
Valeurs: écrit le verdict d'une investigation — trois valeurs, ce seul
agent les écrit, l'invocation 2 les lit :
- `missing` — rien ne fait le comportement
- `wrong` — quelque chose le fait, autrement que le manque le décrit
- `set aside` — quelque chose le fait comme décrit (`## Today` nomme le
  fichier et le symbole), ou rien ne se rapporte aux termes (`## Today`
  dit que rien n'a correspondu, `## Searched` porte les termes et les
  chemins), ou le comportement vit hors du dépôt — un environnement, une
  fiche de store, un réglage d'appareil (`## Today` dit où) ; jamais un
  manque confirmé sans porteur, qui reste `missing` ou `wrong`
Écrit les six titres d'un rapport — `## Verdict`, `## Bearer`,
`## Trigger`, `## Today`, `## Expected`, `## Searched` — les quatre du
milieu répétés une fois par porteur entre `## Verdict` et
`## Searched` ; `## Trigger` finit par `observed` ou `nothing observes
it`, jamais le déclencheur seul, et vaut `none — the behaviour is wrong
wherever it runs` sur un manque confirmé sans déclencheur ; sur `set
aside`, `## Bearer`, `## Trigger` et `## Expected` sont écrits vides,
jamais omis, et `## Today` porte la raison. Lit les états de
`## Decision` de son fichier (→ MECANISMES §États de « ## Decision » —
ce qu'un fichier de blocage attend). Lit le `G<n>` du prompt (→
MECANISMES §Identifiants).

**Gestes**

1. Chercher d'abord son propre fichier de blocage, par `Glob` — rien :
   continuer ; `## Decision` vide : s'arrêter et dire que le blocage
   tient ; rempli : l'appliquer à son propre manque, le dire dans le
   rapport, puis dérouler les mouvements 1 à 5 (→ MECANISMES §Reprise
   sur décision — divergence, variante B). Une décision qui nomme un
   autre manque n'est pas à appliquer.
2. Mouvement 1 — tourner le manque en termes de recherche : les mots
   du domaine, l'écran, la valeur produite ; lire les conventions pour
   les dossiers de code ; chercher chaque dossier, puis le manifeste,
   les fichiers de build et les ressources chacun à son chemin ; le
   test d'un fichier en portée : le changer changerait-il ce que
   l'application fait ; élargir deux fois — le terme exact, ses
   parties, ce qui le tiendrait — trois recherches, et s'arrêter là ;
   chercher les termes dans les deux sections de l'état technique — un
   piège enregistré ou un symbole mort qui porte les termes est nommé
   dans `## Today`, le symbole mort nourrit le mouvement 3, le verdict
   n'en change pas.
3. Mouvement 2 — confirmer : la table à cinq lignes qui donne
   `missing`, `wrong` ou `set aside` (voir `Valeurs`) ; un manque
   confirmé sans porteur au mouvement 3 reste `missing` ou `wrong`.
4. Mouvement 3 — localiser le porteur, et le déclencheur quand il y en
   a un : ce qui doit changer pour que le comportement change, quelle
   qu'en soit la forme ; l'unique contrainte, le reste dépend de lui et
   non l'inverse ; jamais deux noms pour une chose. Compter ce que la
   correction doit toucher : rien → une entrée `Bearer: none` ; un →
   une entrée ; plusieurs qui découlent l'un de l'autre → une entrée
   portée par celui dont les autres dépendent, la prose disant ce qui
   en découle ; plusieurs qui ne découlent pas → une entrée chacun,
   vingt sites d'une même omission sont vingt entrées. Un
   comportement à déplacer → `Bearer: none`, l'atterrissage est au
   Cadreur, et retirer ici puis mettre là est un manque, pas deux. Un
   appel manquant → le porteur est l'appelant. Une entrée exige un
   changement de son porteur et de rien d'autre ; l'unique exception,
   ce sans quoi le porteur ne peut pas changer ; ce qui peut changer
   pendant que le porteur reste est toujours un second bloc
   `## Bearer`, jamais une ligne de `## Expected`.
5. Mouvement 4 — grepper chaque chose que la correction nomme : là et
   atteignable depuis le porteur → rien ; ailleurs, hors de portée →
   une seconde exigence ; absente → une seconde exigence ; une
   signature qui ne convient pas est le cas le plus discret ; un
   déclencheur venu de l'extérieur — connexion, horloge, capteur,
   notification système — est rarement observé.
6. Mouvement 5 — lire le corps de chaque appelant contre le nouveau
   mécanisme, deux tests : ce qu'il tient aujourd'hui, le nouveau
   mécanisme l'accepte-t-il (ce qui casse) ; ce que le nouveau
   mécanisme lui tend, l'utilise-t-il (ce qui ne fait rien en silence —
   un type qui grossit passe le premier et rate le second). Une seconde
   exigence va dans `## Expected`, ou dans `## Trigger` quand c'est le
   déclencheur ; ce qui tient seul est un second bloc `## Bearer`.
7. Écrire `investigation/<id>.md`, six titres, `## Searched` avec les
   termes et les chemins même sur un manque confirmé, `## Today` et
   `## Expected` pleins — l'invocation 2 ne rouvrira pas le code.

**Branches** — le fichier de blocage trouvé : rien / vide / rempli
(geste 1). Le verdict : `missing` / `wrong` / `set aside` (mouvement
2). Le nombre de porteurs : aucun / un / plusieurs qui découlent /
plusieurs indépendants (mouvement 3). Une chose nommée : atteignable /
hors de portée / absente (mouvement 4). Un appelant : accepte ou non,
utilise ou non (mouvement 5). Bloquer ou écarter : un manque que le
code porte déjà, ou auquel rien ne se rapporte, est `set aside` et le
cycle continue ; bloquer est réservé à l'impossible à produire — ici,
un prompt qui ne nomme aucun manque.
**Échange** — écrit pour l'invocation 2 : `## Verdict`, chaque bloc
`## Bearer` avec ses `## Trigger`, `## Today`, `## Expected`, et
`## Searched` ; `## Today` est le seul titre copié dans `## Gaps set
aside`, `## Today` et `## Expected` sont ce que l'invocation 2 tourne
en entrée, `## Trigger` aussi quand il porte une exigence. Lit
d'un autre : rien — il ne voit aucune autre investigation, et ne pointe
jamais vers une autre entrée. Le rapport de fin dit la décision
appliquée, s'il y en a une (→ MECANISMES §Forme d'un relais).
**Bloque** — `investigation/blocked_<id>.md`, forme 1 : `## What
blocks`, `## Where`, `## To resume` — qui peut finir sur une liste
`Options:`, aucune quand la correction est une entrée manquante —,
`## Decision` vide ; le Product Owner répond à la main ; un blocage
arrête ce manque seul, les autres continuent, et l'invocation 2 verra
le rapport manquant. Jamais par prudence : le doute se signale dans le
rapport.

**Décisions**

- Trois recherches, deux élargissements, puis un verdict · écartée :
  élargir jusqu'à trouver · raison : « Widening further is guessing »
  (`diagnostiqueur.md`, mouvement 1) ; `docs/verification/agent-diagnostiqueur.md`
  D-15 sur le compte des élargissements · inconnu
- Le code lu par grep, jamais un fichier ouvert, sauf le corps des
  appelants au mouvement 5 · écartée : lire l'implémentation · raison :
  « you confirm a behaviour, you do not review an implementation » ;
  savoir si un appelant utilise ce qu'on lui tend ne se lit pas dans un
  grep (`docs/verification/agent-diagnostiqueur.md` D-9 ;
  `docs/verification2/plans/conflits.md` 253) · inconnu
- Chaque grep avec un chemin ; le manifeste, les fichiers de build et
  les ressources chacun au sien · écartée : un motif nu, ou les seuls
  dossiers des conventions · raison : un motif nu balaie `docs/` et la
  sortie de build ; les dossiers des conventions ne tiennent ni le
  manifeste ni les ressources, et une règle était violée sur chaque
  manque (`docs/verification2/diagnostiqueur.md` F11 ;
  `docs/verification2/plans/conflits.md` 250) · inconnu
- L'état technique comme aide de recherche, jamais comme verdict ; deux
  sections par grep du titre · écartée : le lire entier ; en faire un
  verdict · raison : l'entrée nommait deux sections d'un fichier de
  2 300 lignes sans dire comment les atteindre, et la lecture n'avait
  aucune issue (`docs/verification2/diagnostiqueur.md` F04, F10 ;
  `docs/verification2/plans/conflits.md` 245) · inconnu
- `set aside` pour un manque non confirmé, jamais pour un manque
  confirmé sans porteur · écartée : écarter ce qu'on ne place pas ·
  raison : « a behaviour that exists has something that governs it »,
  et l'atterrissage est une décision de découpage (`diagnostiqueur.md`,
  mouvement 3) · inconnu
- Un comportement hors du dépôt est `set aside` · écartée : le
  confirmer par déduction · raison : « you cannot confirm what you
  cannot read » — les quatre outils n'atteignent rien hors du dépôt
  (`diagnostiqueur.md` ; `docs/verification/agent-diagnostiqueur.md`,
  table C, question sur *a value fixed outside the code*) · inconnu
- `Bearer: none` sur un déplacement, l'atterrissage au Cadreur ·
  écartée : « the bearer is where it lands » · raison : deux règles
  contraires à trente lignes d'écart, et le Cadreur décide déjà où un
  `none` atterrit (`docs/verification/agent-diagnostiqueur.md` D-3 ;
  `docs/verification2/plans/conflits.md` 247) · inconnu
- Un porteur par entrée, plusieurs porteurs indépendants en plusieurs
  blocs `## Bearer` · écartée : une entrée couvrant plusieurs sites ·
  raison : « an entry covering several cannot be closed by observing
  one » ; le rapport n'avait aucune forme pour porter vingt porteurs
  (`docs/verification/agent-diagnostiqueur.md` D-1 ;
  `docs/verification2/plans/conflits.md` 252) · inconnu
- Une seconde exigence dans `## Expected` seulement quand le porteur ne
  peut pas changer sans elle ; sinon un second bloc `## Bearer` ·
  écartée : « une ligne de `## Expected` » pour ce qui appartient à une
  autre entrée · raison : ce que la règle disait appartenir ailleurs
  atterrissait dans l'entrée même dont il fallait le tenir
  (`docs/verification2/diagnostiqueur.md` F08 ;
  `docs/verification2/plans/conflits.md` 248) · inconnu
- `## Trigger` répété sous chaque `## Bearer` · écartée : un seul
  `## Trigger` par rapport · raison : un second porteur n'avait pas de
  déclencheur et ne pouvait finir par `observed`
  (`docs/verification2/diagnostiqueur.md` F13) · inconnu
- `## Today` porte la raison d'un `set aside`, `## Searched` les
  chemins · écartée : la raison nulle part · raison : aucun des six
  titres ne tenait la raison, et la liste des écartés s'écrivait depuis
  rien (`docs/verification2/diagnostiqueur.md` F12 ;
  `docs/verification2/plans/conflits.md` 251) · inconnu
- Les chemins de code relatifs à la racine du dépôt, comme `docs/` ;
  seuls les trois fichiers du dossier et les fichiers de blocage
  relatifs au dossier · écartée : tout relatif au dossier de
  correction · raison : `docs/TECHNICAL_CONVENTIONS.md` ne se résout
  pas depuis `bugfix-NN/`, et les exemples contredisaient la règle
  (`docs/verification/agent-diagnostiqueur.md` D-7 ;
  `docs/verification2/diagnostiqueur.md` F15) · inconnu
- `Glob` pour deux tests d'existence seulement, jamais sur le code ·
  écartée : `Glob` libre · raison : l'outil était donné et aucun geste
  ne le nommait (`docs/verification2/diagnostiqueur.md` F03 ;
  `docs/verification2/plans/conflits.md` 244) · inconnu
- Un blocage arrête ce manque seul · écartée : arrêter le run entier ·
  raison : une investigation ne voit que son écart, et rien de ce
  qu'elle cherche n'aide les autres ; la commande saute tout écart dont
  le rapport existe déjà, une reprise coûtant une investigation entière,
  et c'est ainsi qu'une seule investigation ratée se rejoue — le Product
  Owner remplit son fichier de blocage, relance la commande, et celle-là
  seule repart (PROCESS_AVAL-avant-refonte.md L636-639, L898-901) ·
  inconnu
- Une décision qui nomme un autre manque n'est pas appliquée · écartée :
  l'appliquer · raison : à retrouver · inconnu
- Ne jamais juger si un manque est légitime · écartée : filtrer la
  liste · raison : « the Product Owner decided that by listing it »
  (`diagnostiqueur.md`, *What you never do*) · inconnu

---

### diagnostiqueur, invocation 2 — Assembly : assembler les rapports en `desc-bug.md`

Modèle: sonnet · effort medium · outils: Read, Grep, Glob, Write
Invoquée par: `/diagnostique`, phase 2 — une fois, quand chaque rapport
existe et qu'aucun `desc-bug.md` n'existe ; jamais par un autre agent
ni une autre commande.
Lit: son propre fichier de blocage `blocked_diagnostiqueur.md` et ses
`-NN` réglés, par un `Glob` `blocked_diagnostiqueur*.md` · l'existence
de `desc-bug.md`, par `Glob` · `investigation/<id>.md` pour chaque
identifiant de `bug-list.md`, tous, entiers — jamais un `blocked_*.md`
de ce dossier · `bug-list.md`, entier, pour le `G<n>` de chaque manque,
l'ordre du Product Owner et le `(B<n>)` qu'un manque porte ·
`.claude/grids/GRILLE_FERMETURE_TECHNIQUE.md`, pour trois de ses
fermetures · jamais le code, jamais les conventions, jamais l'état
technique, jamais le fichier produit, le document technique ou le
global.
Écrit: `desc-bug.md`, une fois, jamais réécrit · `blocked_diagnostiqueur.md`
quand produire est impossible (forme 1).
Valeurs: lit les trois verdicts de l'invocation 1 (`missing`, `wrong`,
`set aside`) et les six titres d'un rapport. Écrit la nature de chaque
porteur, une des huit, une par entrée et jamais une par manque (→
MECANISMES §Les huit natures — la nature d'un bloc) ; une clé de texte
manquante n'a aucune nature et va sous §9 Text. Écrit les identifiants
`§n.m` (→ MECANISMES §Identifiants) et recopie `(B<n>)` en fin de titre
d'entrée. Lit trois fermetures de `GRILLE_FERMETURE_TECHNIQUE.md` — la
grille de clôture technique, dont les fermetures se lisent par nature
puis à travers les sections ; seules trois s'appliquent à un fichier de
bug, les autres lisent contre un fichier produit qu'il n'y a pas ou
portent sur une traduction qui n'a pas été faite :
- *Completeness* — une entrée qui laisse un cas ouvert
- *Resources* — une correction qui affiche quelque chose que rien ne
  porte
- *Agreement between entries* — deux entrées qui se contredisent sur un
  sujet
Lit les états de `## Decision` de son fichier (→ MECANISMES §États de
« ## Decision » — ce qu'un fichier de blocage attend).

**Gestes**

1. Chercher d'abord son propre fichier de blocage, par `Glob` — rien :
   continuer ; `## Decision` vide : s'arrêter, le blocage tient ;
   rempli : la décision ne remplace pas ce qui manque — refaire
   l'appariement en tête de l'assemblage, identifiants puis rapports ;
   tous là → assembler ; un manque encore → bloquer de nouveau en
   nommant lequel, une décision ne peut pas écrire un rapport, et le
   dire pour que l'orchestration sache quelle investigation renvoyer.
2. Aussitôt après, avant tout appariement, `Glob` `desc-bug.md` : il
   existe → s'arrêter, nommer le fichier, dire que ce qu'il tient est
   réglé — un arrêt, pas un blocage, sans fichier, sans appariement,
   sans lecture.
3. Lire tous les rapports et `bug-list.md` ; apparier par identifiant,
   jamais par position — chaque `G<n>` du fichier a son
   `investigation/G<n>.md`, aucun rapport ne nomme un identifiant que
   le fichier n'a pas ; un fichier manquant est une investigation qui
   n'a pas tourné, un manque sans `G<n>` est un manque que l'ensemble
   ne peut pas apparier → bloquer plutôt qu'assembler un ensemble
   partiel. Un rapport qui ne permet pas d'écrire une entrée est un
   blocage, pas une raison d'aller voir le code.
4. Mouvement 6 — donner à chaque bloc `## Bearer` d'un manque confirmé
   une nature parmi les huit — la nature du porteur, pas de ce qu'il
   appelle : une vue qui n'invoque pas un calcul est `presentation`, un
   calcul faux est `calculation`.
5. Mouvement 7 — écrire une entrée par bloc `## Bearer`, depuis
   `## Today` et `## Expected`, et depuis `## Trigger` quand l'exigence
   y est — un déclencheur finissant par `nothing observes it` est à
   construire ; chaque seconde exigence de `## Expected` entre dans
   l'entrée ; ce qui tient seul est une entrée à part. Prose : présent
   de l'indicatif, voix active, une phrase une règle, en anglais, deux
   phrases d'ordinaire — ce que le code fait, ce qu'il doit faire ;
   sans justification, sans référence à la formulation de
   `bug-list.md`.
6. Mouvement 8 — numéroter et ordonner : chaque entrée dans la section
   que sa nature nomme, ou §9 Text, dans l'ordre de `bug-list.md` ; rien
   n'est écrit sur disque encore.
7. Mouvement 9 — charger la grille et passer les trois fermetures ;
   une fermeture qui échoue est un blocage, pas une question ; écrire
   `desc-bug.md` seulement une fois les trois passées — une fermeture
   échouée ne laisse aucun fichier de bug, et le run d'après la
   décision repart des rapports sans `desc-bug.md` sur lequel
   s'arrêter.
8. Écrire `desc-bug.md` : `# Preamble` (un seul `#`) de trois lignes,
   `Intent: correcting the gaps reported on <feature>.`, `Out of scope:
   everything not listed below.`, `Dependencies: the whole feature,
   already built.` ; neuf sections toujours, vides comprises, dans
   l'ordre `## §1 Model` … `## §8 Access`, `## §9 Text` ; des entrées
   `### §n.m <titre>`, numérotées à l'écriture, jamais renumérotées,
   `(B<n>)` fermant le titre quand `bug-list.md` le portait entre
   parenthèses en fin de première ligne du manque — lu par cette forme
   et aucune autre ; sous chaque titre une ligne `Bearer: <symbole>`
   ou `Bearer: none — nothing in the project holds this behaviour
   today`, jamais omise, jamais qualifiée d'un compte ou d'un doute ;
   puis `## Gaps set aside`, une ligne par manque écarté avec son
   `## Today` copié pour raison, la section écrite même vide ; aucun
   marqueur `NEW`.

**Branches** — le fichier de blocage : rien / vide / rempli, et sur
rempli : tous les rapports là / un manquant (geste 1). `desc-bug.md` :
absent / présent (geste 2). L'appariement : complet / un fichier
manquant / un manque sans `G<n>` / un rapport orphelin (geste 3). La
nature : une des huit / §9 Text (mouvement 6). Les fermetures : les
trois passent / une échoue (mouvement 9). Un `(B<n>)` : en fin de
première ligne → recopié ; ailleurs → pas un identifiant.
**Échange** — lit de l'invocation 1 : les six titres de chaque rapport,
`## Today` pour la raison d'un écart, `## Trigger` pour une exigence.
Écrit pour le Cadreur : `Bearer:` sous chaque titre, `(B<n>)` dans le
titre, le `# Preamble` de trois lignes, les neuf sections ; pour le
Vérificateur et le Détailleur : `Dependencies:` sans `Vocabulary` ;
pour le Fusionneur (invocation 3) : les entrées, dont il tire ce qu'une
correction a réglé sur le produit ; pour `/9_controle`, par le Cadreur :
le `(B<n>)`. Le rapport de fin dit la lecture de `bug-list.md` ou
l'existence de `desc-bug.md`, et la décision appliquée (→ MECANISMES
§Forme d'un relais).
**Bloque** — `blocked_diagnostiqueur.md`, à la racine du dossier de
correction, forme 1 ; le Product Owner répond à la main ; quatre cas et
pas un de plus : un prompt qui ne nomme aucun manque (invocation 1), un
ensemble de rapports qui ne correspond pas à `bug-list.md` identifiant
pour identifiant, un rapport qui ne porte pas ce qu'une entrée exige,
une fermeture qui échoue. Un `desc-bug.md` existant est un arrêt, pas un
blocage.

**Décisions**

- `desc-bug.md` existant : un arrêt sans fichier, testé en tête ·
  écartée : un blocage, testé après les neuf mouvements · raison : un
  blocage que rien ne lève, et un assemblage entier fait avant le test
  qui le rend vain (`docs/verification2/diagnostiqueur.md` F05, F07,
  F16 ; `docs/verification2/plans/conflits.md` 246) · inconnu
- Apparier par identifiant, jamais par position · écartée : compter
  les fichiers contre les manques · raison : `docs/verification4/plan.md`
  entrée 40, item I · non éprouvée
- Bloquer plutôt qu'assembler un ensemble partiel · écartée : assembler
  ce qui est là · raison : « a gap silently dropped never comes back »
  (`diagnostiqueur.md`, invocation 2) · inconnu
- Les rapports seuls, jamais un `blocked_*.md` du dossier · écartée :
  compter tout `investigation/*.md` · raison : le dossier tient
  rapports, blocages debout et blocages réglés, et le compte tombait
  juste sur le cas même qu'il devait attraper
  (`docs/verification/agent-diagnostiqueur.md` D-6) · inconnu
- Le code jamais ouvert à l'invocation 2 · écartée : aller voir ce
  qu'un rapport ne dit pas · raison : « the reports carry everything;
  one that does not is a block » (`diagnostiqueur.md`, *What you never
  do*) · inconnu
- Une nature par bloc `## Bearer`, jamais par manque · écartée : une
  nature par manque · raison : un manque à porteur vue et porteur
  dépôt prenait une nature, et une entrée tombait dans la mauvaise
  section (`docs/verification2/diagnostiqueur.md` F09 ;
  `docs/verification2/plans/conflits.md` 249) · inconnu
- Le mouvement 7 porte l'exigence de `## Trigger` comme celle de
  `## Expected` · écartée : `## Today` et `## Expected` seuls · raison :
  une exigence classée sous `## Trigger` n'atteignait jamais
  `desc-bug.md`, et le Cadreur coupait un lot qui ne pouvait pas être
  construit (`docs/verification3/plan.md` entrée 40) · inconnu
- Trois fermetures de la grille, pas les autres · écartée : la grille
  entière · raison : *Traceability* et *Nothing dropped* lisent contre
  un fichier produit, et il n'y en a pas ; le reste porte sur une
  traduction non faite (`diagnostiqueur.md`, mouvement 9) · inconnu
- Une fermeture qui échoue bloque, ne questionne pas · écartée : un
  fichier de questions · raison : « nobody answers a question in this
  cycle » (`diagnostiqueur.md`) · inconnu
- `desc-bug.md` écrit une fois les trois fermetures passées, jamais
  avant · écartée : écrire les entrées puis fermer · raison : un
  blocage au mouvement 9 laissait un `desc-bug.md` sur lequel la reprise
  s'arrêtait (`docs/verification/agent-diagnostiqueur.md` D-5) · inconnu
- `# Preamble` à un seul `#` · écartée : `## Preamble` · raison : le
  Convertisseur dit que le `#` unique est ce qui distingue le préambule
  des sections que le Cadreur ne doit jamais couper
  (`docs/verification3/plan.md` entrée 39) · inconnu
- Un préambule de trois lignes, pas les quatre parties du document
  technique · écartée : les quatre titres, vides · raison : « A
  correction cycle has no vocabulary of its own and no cross-cutting
  rules: it inherits the feature's, and an empty heading would read as
  *nothing to settle here* » (`diagnostiqueur.md`) · inconnu
- Les neuf sections toujours, vides comprises · écartée : les seules
  sections non vides · raison : `desc-bug.md` prend la forme du document
  technique — préambule, neuf sections, entrées numérotées — parce que
  le Cadreur le découpe exactement comme une spec ; et une section vide
  est une information, pas un oubli : elle dit au Cadreur qu'il n'y a
  rien de cette nature — on part des neuf et on laisse vide, jamais
  l'inverse (PROCESS_AVAL-avant-refonte.md L689-691 ;
  PROCESS_AMONT-avant-refonte.md L667-669) · inconnu
- `Bearer:` jamais omise, `none` une valeur · écartée : une ligne
  absente pour *aucun* · raison : « an absent line reads as an entry
  nobody finished » (`diagnostiqueur.md`) ; le Cadreur consomme
  `Bearer: none` et en fait une production
  (`docs/verification/agent-diagnostiqueur.md` D-2, B′-3) · inconnu
- `(B<n>)` entre parenthèses en fin de première ligne du manque, et en
  fin de titre d'entrée · écartée : une forme libre, ou nulle part ·
  raison : aucun des deux côtés ne disait la forme, et un manque qui la
  portait autrement perdait la marque `carried` au contrôle suivant
  (`docs/verification3/plan.md` entrée 37, item G) · inconnu
- `## Gaps set aside` écrite même vide · écartée : omise quand rien
  n'est écarté · raison : son absence se lirait « l'agent n'a pas
  tourné » (`diagnostiqueur.md`) · inconnu
- Numérotées à l'écriture, jamais renumérotées · écartée : renuméroter
  après tri · raison : « a lot cites `§4.1`, and that citation has to
  hold » (`diagnostiqueur.md` ; → MECANISMES §Identifiants) · inconnu
- Aucun marqueur `NEW` · écartée : marquer comme le fichier produit ·
  raison : « nothing here goes through a grid » (`diagnostiqueur.md`)
  · inconnu
- Une décision sur ce fichier ne fournit jamais un rapport ; l'agent
  rebloque en nommant l'identifiant · écartée : l'assemblage avec un
  rapport en moins · raison : `docs/verification2/chemins-aval.md`
  F12 ; `docs/verification2/plans/conflits.md` 257 · inconnu

---

## Coutures

| Ce qui part | Ce qui arrive | Ce que le receveur vérifie | L'autre document |
|---|---|---|---|
| `docs/features/<name>/idees.md`, écrit à la main, en français, textes affichés entre guillemets | `/1_lexique`, invocation 1 puis 2 — le Lexicographe le lit entier, y remplace les termes retirés, ajoute ou retire des guillemets | Le Lexicographe bloque sur *no idea file* ou fichier vide ; la commande ne l'ouvre jamais ; le fichier atteint le worktree par `chore: answers` | `PROCESS_AMONT.md` |
| `idees.md` au vocabulaire réglé, `lexique.md` à côté, le plus haut `questions-lexicographe-NN.md` sans `### Q` | `/2_structure`, invocation 1 — le Rédacteur transcrit en `desc-produit.md`, une fois | `^### Q` sur le plus haut fichier du lexicographe, à la racine ou sous `questions/lexicographe/` ; aucun `desc-produit.md` ; le Rédacteur bloque sur deux sujets sans lien | `PROCESS_AMONT.md` |
| `docs/features/`, créé par `/socle` — vide au moment où `/socle` le pose, et hors commit, git ne suit pas un dossier vide ; sur ce projet il tient aujourd'hui `premiere-app/` et `premiere-app-2/` | Le Product Owner y crée `<name>/` ; chaque commande amont et aval dérive `docs/features/<name>/` de son argument (→ MECANISMES §Disposition du dossier de feature) | Rien — aucune commande ne teste l'existence du dossier de feature ; sur un `<name>` sans dossier, `/1_lexique` invoque et le Lexicographe bloque sur *no idea file* | `PROCESS_AMONT.md`, `PROCESS_AVAL.md` |
| `docs/PRODUIT_GLOBAL.md` à `# Application` (→ MECANISMES §Lecture du global par l'index) | Le Rédacteur (index `^#`), le Sondeur invocation 3 (sections nommées), le Fusionneur (invocations 1 et 3) | Le Fusionneur teste le seul titre : rien d'autre → `INIT`, et l'invocation 3 écrit dans `desc-produit-fusion.md` | `PROCESS_AMONT.md` |
| `docs/CURRENT_TECHNICAL_STATE.md` à `# Technical state` — l'état du fichier au sortir de `/socle`, avant tout lot (→ MECANISMES §Lecture de l'état technique) | Le Réalisateur et l'Arbitre y écrivent ; le Détailleur, le Réalisateur, le Diagnostiqueur (invocation 1, ce document) y lisent `## Traps — general` et `## Dead state` par grep puis lecture bornée | Tant qu'aucun lot n'a écrit, un grep de titre qui ne rend rien lit rien ; les deux titres existent une fois qu'un lot a écrit (`PROCESS_AVAL.md`, même ligne) ; la compétence `technical-state-format` chargée avant d'écrire | `PROCESS_AVAL.md`, `PROCESS_MECANISMES.md` |
| Les lignes `.gitignore` `docs/features/*/stop.md` et `docs/features/*/stop1.md` (→ MECANISMES §stop.md) | `/8_code`, mouvement 6, cherche `stop.md` dans le dépôt principal | Ajoutées si absentes ; ni l'un ni l'autre jamais commité ; aucun des deux présent n'est une erreur | `PROCESS_AVAL.md`, `PROCESS_MECANISMES.md` |
| `docs/TECHNICAL_CONVENTIONS.md` non créé par `/socle`, dit dans son rapport | `/conventions`, l'Architecte invocation 1 l'écrit depuis les deux documents de la feature | L'Architecte à l'invocation 1 ne lit aucun fichier au nom de *convention* ; tout l'aval le lit ensuite | `PROCESS_AMONT.md` → `PROCESS_AVAL.md` |
| `code/rapport-controle.md` de `/9_controle`, phase 5 — `## Intentions missing`, `## Doubts` relayés | Le Product Owner écrit `bugfix-NN/bug-list.md` à la main : un manque par `G<n>`, `(B<n>)` en fin de première ligne pour un manque pris du rapport | `/diagnostique` lit `G<n>` sur la ligne et s'arrête sur un manque sans ; le Diagnostiqueur (2) lit `(B<n>)` par cette forme seule | `PROCESS_AVAL.md` → ce document |
| `/8_code` : ce que le Contrôleur rapporte ne revient jamais par un blocage sur un lot fermé | Un `bug-list.md` et un cycle de correction | `/8_code` L755-757 ; aucune autre voie de retour | `PROCESS_AVAL.md` → ce document |
| `bugfix-NN/` comme dossier de travail, créé par le Product Owner (→ MECANISMES §Dossier de travail) | `/diagnostique` exige le dossier et `bug-list.md` ; `/7_lots`, `/8_code`, `/9_controle`, `/conventions` (second argument), `/audit_blocages`, `/audit_conventions` prennent le plus haut | Le plus haut `bugfix-NN/` par nom ; `desc-bug.md` à sa racine ; jamais créé par une commande | `PROCESS_AVAL.md`, `PROCESS_MECANISMES.md` |
| `bugfix-NN/desc-bug.md` — `# Preamble` de trois lignes, neuf sections, `### §n.m <titre> (B<n>)`, `Bearer:` sous chaque titre, `## Gaps set aside` | `/7_lots` — le Cadreur (inventaire par porteur, `Bearer: none` décidé avant de grouper, `(B<n>)` dans l'`Anchor:`), le Vérificateur (`Dependencies:`, pas de `Vocabulary`), le Détailleur (`Bearer:`, termes de la feature), l'Arbitre (nomme le cycle) | Aucun grep de `/7_lots` sur `desc-bug.md` — le test `^### §` porte sur `spec-technique.md` seul ; le Cadreur greppe `<<ASSUMED` et `[B`, absents ici | `PROCESS_AVAL.md` |
| `(B<n>)` en fin de titre d'entrée (→ MECANISMES §Identifiants, §Marque carried) | Le Cadreur le copie dans l'`Anchor:` du lot ; `/9_controle`, phase 1, marque `carried` ; le Contrôleur lit `(carried)` | La forme exacte, entre parenthèses, en fin de titre ; une entrée qui le perd laisse le bloc *missing* au contrôle suivant | `PROCESS_AVAL.md` |
| Chaque `bugfix-*/desc-bug.md` de la feature | `/fusion`, ligne 8 — le Fusionneur, invocation 3, du plus ancien au plus récent ; `/fusion_compare` s'arrête sur un `bugfix-*/` sans `questions-fusionneur-*` | Un `bugfix-*/` sans `desc-bug.md` → l'invocation ne tourne pas, jamais `bug-list.md` en repli ; les entrées seules sont pesées, pas `## Gaps set aside` | `PROCESS_AMONT.md` |
| `investigation/blocked_<id>.md`, `blocked_diagnostiqueur.md`, `## Decision` vide (→ MECANISMES §Fichier de blocage — divergence, §Emplacement des fichiers de blocage) | Le Product Owner remplit à la main ; `/audit_blocages` lit `investigation/` et la racine du dossier de travail | `/diagnostique` teste chaque `## Decision` par grep avant d'envoyer ; l'agent cherche le sien en premier (variante B) | `PROCESS_MECANISMES.md`, `PROCESS_ANNEXES.md` |
| Le `## Decision` rempli, nommé au prompt par `[Blocking file: … — its ## Decision is filled.]` (→ MECANISMES §Reprise sur décision — divergence) | L'agent l'applique à son manque (1) ou refait l'appariement (2), et le dit dans son rapport | `/diagnostique` renomme en `-NN` sur cette ligne, par identifiant et à la racine, avant les cinq pas | `PROCESS_MECANISMES.md` |
| Les lignes de prompt `Bug-fix folder:`, `Invocation 1 — Investigation.` / `Invocation 2 — Assembly.`, `Gap G<n>:` (→ MECANISMES §Invocation d'un agent, §Numéros d'invocation) | Le Diagnostiqueur aiguille sur elles, jamais sur le dossier | `model="sonnet"` concorde avec le frontmatter ; aucun `effort`, `isolation`, `run_in_background` | `PROCESS_MECANISMES.md` |
| `docs/TECHNICAL_CONVENTIONS.md` entier, à l'invocation 1 (→ MECANISMES §Lecture des conventions — divergence, §Grep du code avec chemin) | Le Diagnostiqueur en tire les dossiers de code à grepper | Chaque grep avec un chemin ; les conventions qui ne nomment aucun dossier n'ont pas de règle écrite chez lui | `PROCESS_MECANISMES.md`, `PROCESS_AMONT.md` |
| `.claude/grids/GRILLE_FERMETURE_TECHNIQUE.md`, trois fermetures nommées | Le Diagnostiqueur, invocation 2, mouvement 9 ; le Convertisseur en lit d'autres | Les titres `## Completeness`, `## Resources`, `## Agreement between entries` existent dans la grille | `PROCESS_AMONT.md` |
| `.claude/grids/GRILLE_EXISTANT.md` — la grille de l'existant, sans commande d'extraction | Le Sondeur, invocation 3, à `/4_grille` second temps ; `questions-existant-NN.md`, `blocked_existant.md` | Le plus haut `questions-existant-NN.md` sans `### Q` avant `/5_reclasse` | `PROCESS_AMONT.md` |
| Le commit `chore: scaffolding for the chain` poussé, sans worktree (→ MECANISMES §Commit sans worktree) | Le dépôt distant ; le `HEAD` local que tout worktree suivant branche | Un push qui échoue est rapporté | `PROCESS_MECANISMES.md` |

## Boucles

### Cycle de correction — du rapport de contrôle au global

Ouverte par: le Product Owner qui crée `docs/features/<name>/bugfix-NN/`
et y écrit `bug-list.md` — depuis un `code/rapport-controle.md` de
`/9_controle` (avec `(B<n>)`) ou depuis l'usage (sans)
Fermée par: aucun test dans la chaîne — la boucle se ferme quand le
Product Owner ne crée pas de `bugfix-NN+1/` ; le dernier `/9_controle`
d'un cycle relaie `## Intentions missing` et `## Doubts`, et elle
décide (`9_controle.md`, *What you relay*) ; côté global, `/fusion`
ligne 8 fait tourner le Fusionneur invocation 3 sur tous les
`bugfix-*/desc-bug.md` à la fois, une fois, et son fichier de questions
même vide dit que la passe a tourné
Plafond: aucun — `NN` n'est compté nulle part, et aucun fichier ne borne
le nombre de cycles
Au plafond: sans objet
Traverse: diagnostiqueur (1, 2), cadreur, verificateur, detailleur,
arbitre, architecte (3), concepteur, testeur, realisateur, relecteur,
controleur, fusionneur (3), redacteur (3, `code/decisions-produit.md`
par cycle) ; `/diagnostique`, `/7_lots`, `/8_code`, `/9_controle`,
`/conventions` (second argument), `/fusion` — ce document,
`PROCESS_AVAL.md`, `PROCESS_AMONT.md`

### Investigation bloquée → décision → seule cette investigation rejouée

Ouverte par: un Diagnostiqueur, invocation 1, qui écrit
`investigation/blocked_<id>.md` — les autres appels continuent, la
phase 2 est retenue, les identifiants debout sont relayés
Fermée par: chaque `G<n>` de `bug-list.md` a son `investigation/<id>.md`
et aucun `investigation/blocked_<id>.md` au nom non numéroté ne tient
un `## Decision` vide — la table de tri de `/diagnostique` n'envoie
plus rien et la phase 2 part ; le fichier appliqué est renommé `-NN`
Plafond: aucun — chaque tour est une décision du Product Owner ; un
manque rebloqué réécrit le même nom et le tour suivant s'y arrête
Au plafond: sans objet
Traverse: diagnostiqueur (1, 2) ; `/diagnostique` ; le Product Owner —
ce document, `PROCESS_MECANISMES.md` (*Blocage → décision → relance*)

### Balayage → réponse → règlement du vocabulaire, sur `idees.md`

Ouverte par: `/1_lexique`, invocation 1 — Sweeping, un
`questions-lexicographe-NN.md` tenant au moins un `### Q`
Fermée par: un `questions-lexicographe-NN.md` sans `### Q` à la racine
après une invocation 1 — le plus haut fichier du lexicographe, que
`/2_structure` teste avant son invocation 1 ; après une invocation 2,
`/1_lexique` relance 1
Plafond: aucun — chaque tour attend le Product Owner
Au plafond: sans objet
Traverse: lexicographe (1, 2), le Product Owner ; `/1_lexique`,
`/2_structure` — `PROCESS_AMONT.md` (description entière), ce document
(le fichier que la boucle réécrit)

## Inventaire

Agents décrits en entier : diagnostiqueur (invocation 1 — Investigation
; invocation 2 — Assembly).
Agents portés en entrée courte : sondeur, invocation 3 — sous la forme
`### sondeur, invocation 3 — ce que l'entrée /extrait en retient`,
parce qu'aucune commande de ce document ne l'invoque ; `/socle`
n'invoque personne, `/diagnostique` n'invoque que le Diagnostiqueur,
et aucun autre document ne l'invoque.
Commandes décrites : `/socle` ; `/diagnostique` ; `/extrait` (absente
de la chaîne, décrite comme telle).
Entrée décrite hors commande : `idees.md`.
Agents nommés ici et décrits ailleurs, sans entrée courte parce
qu'aucune commande de ce document ne les invoque : lexicographe,
redacteur (`PROCESS_AMONT.md`) ; cadreur, verificateur,
detailleur, arbitre, fusionneur invocation 3 (`PROCESS_AVAL.md`,
`PROCESS_AMONT.md`).
