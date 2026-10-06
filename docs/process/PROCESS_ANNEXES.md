# PROCESS_ANNEXES.md — hors périmètre d'audit

> Document de pilotage, en français. Il décrit ce qui, dans le dépôt,
> tourne à côté de la chaîne sans changer aucun artefact qu'elle
> produit : trois commandes lancées à la main, un script de contrôle des
> fichiers de la chaîne, un document d'archive. Le critère et le
> périmètre sont énoncés une fois pour les cinq documents
> → `MECANISMES §Périmètre d'audit` ; ce document ne les redit pas, il
> applique le critère à chaque candidat, au fichier, et donne le
> verdict avec sa preuve.

Ce document n'a ni `## Coutures` ni `## Boucles` : il est hors du
périmètre, et rien de ce qu'il décrit n'est franchi par une passation
que la chaîne vérifie. Il se ferme sur `## Inventaire`.

Les numéros de ligne cités sont ceux des fichiers au `HEAD` local du
2026-09-21 (`.claude/commands/deploie.md`, `audit_blocages.md`,
`audit_conventions.md`, `.claude/scripts/coherence.py`, `grouper.py`,
`docs/process/GRILLE_CONVENTIONS_RETIREES.md`).

---

# Les six candidats — verdict au fichier

La recherche d'appelants a été faite sur `.claude/commands/*.md`,
`.claude/agents/*.md` et `.claude/CLAUDE.md`, par le nom de chaque
candidat ; les trente derniers messages de commit (`git log --oneline
-30`, et jusqu'à deux cents en arrière) ne nomment aucun des six.

| Candidat | Ce qu'il lit | Ce qu'il écrit ou imprime | Qui l'appelle dans la chaîne | Sa sortie façonne-t-elle un document ou un rapport que la chaîne garde ? | Verdict |
|---|---|---|---|---|---|
| `.claude/scripts/grouper.py` | `tracabilite-full.md` | Sur la sortie standard : les groupes `G<n>` | `/9_controle`, phase 2 | Oui — l'argument, → `MECANISMES §Périmètre d'audit` | **hors annexe — appartient à `PROCESS_AVAL.md`** §/9_controle |
| `.claude/commands/deploie.md` | `adb devices -l` (ligne 13) ; rien dans le dépôt | Rien dans le dépôt ; un rapport en message, une ligne par appareil (lignes 61-62) ; deux installations sur deux appareils par `gradlew installDebug` | Personne — `CLAUDE.md` ligne 59 le range « outside the chain, run by hand » ; aucune commande ni aucun agent ne le nomme | Non — il n'écrit aucun fichier, il installe ce que le dépôt contient | **annexe** |
| `.claude/commands/audit_blocages.md` | Les `blocked_*-NN.md` et `blocked_*.md` de cinq lieux du dossier de travail (lignes 26-39) ; `audit-blocages.md` de ses passes antérieures (ligne 44) | `audit-blocages.md` à la racine du dossier de travail, en ajout (ligne 140) | Personne — ligne 9-10 : « No command calls it » ; `/diagnostique` ligne 242 le cite pour dire qu'un fichier non renommé y sera listé « still open », ce n'est pas un appel | Non — voir l'argument ci-dessous | **annexe** |
| `.claude/commands/audit_conventions.md` | `architecte/*.md`, `docs/TECHNICAL_CONVENTIONS.md` entier, `couverture.md`, les entrées du document technique que `couverture.md` nomme, les lignes `Anchor` de `code/decoupage.md`, ses passes antérieures (lignes 26-63) | `audit-conventions.md` à la racine du dossier de travail, en ajout (ligne 164) | Personne — lignes 9-10 ; `/9_controle` ligne 15 le cite comme exemple de dérivation des dossiers, `architecte.md` ligne 779 le cite pour justifier la ligne de `couverture.md` ; ni l'un ni l'autre n'est un appel | Non — voir l'argument ci-dessous | **annexe** |
| `.claude/scripts/coherence.py` | `.claude/agents/*.md` et `.claude/commands/*.md`, ou le fichier passé en argument (lignes 165-171) | Sur la sortie standard, les défauts trouvés ; code de sortie 1 s'il en trouve (ligne 184). Il ne modifie aucun fichier | Personne dans la chaîne — aucune commande, aucun agent, pas `CLAUDE.md` ; ses appelants sont les campagnes de correction (`docs/verification2/correction.md` lignes 379 et 412) | Non — il vérifie la forme des fichiers de la chaîne, pas un artefact qu'elle produit | **annexe** |
| `docs/process/GRILLE_CONVENTIONS_RETIREES.md` | — (un document) | — | Personne — aucun agent, aucune commande ; nommé une fois, par `.claude/grids/GRILLE_CONVENTIONS.md` lignes 580-582 | Non — l'Architecte ne le lit pas, et rien n'en dérive une règle | **annexe** |

**L'argument sur les deux rapports d'audit.** `audit-blocages.md` et
`audit-conventions.md` sont écrits dans le dossier de feature, sous le
dossier de travail, et y restent : rien ne les ignore dans `.gitignore`,
et le commit d'avant-run de la commande suivante (`git add
docs/features/<name>/`, → `MECANISMES §Git, avant l'invocation`) les
emporte. On pourrait donc dire que la chaîne les *garde*. Le critère
est autre : une annexe change aucun artefact que la chaîne produit. Or
la chaîne ne produit pas ces deux fichiers — les deux commandes disent
« No command calls it » (`audit_blocages.md` ligne 9,
`audit_conventions.md` ligne 9) — et ne les consomme pas : le seul
lecteur de chacun est sa propre passe suivante (lignes 44-45 et 54-56 ;
lignes 62-63 et 72-74), et le Product Owner
(`docs/verification/fichiers.md` lignes 59-60 : « `/audit_blocages`
next pass; PO »). Aucun agent, aucune autre commande ne les ouvre. Les
deux commandes s'interdisent en outre de changer ce qu'elles lisent
(`audit_blocages.md` lignes 200-207 ; `audit_conventions.md` lignes
218-224). Un fichier que rien dans la chaîne n'écrit ni ne lit, posé à
côté des artefacts de la chaîne et porté par le commit suivant, est un
rapport pour le Product Owner, pas un artefact de la chaîne. Un lecteur
qui tient que tout ce qui est sous `docs/features/<name>/` est artefact
de la chaîne conclura autrement ; il devra alors dire quel agent ou
quelle commande change de comportement selon ce que ces rapports
contiennent — la recherche n'en trouve aucun.

---

# Renvoyé à PROCESS_AVAL.md

### grouper.py — hors annexe

Le verdict est dans la table ci-dessus ; l'argument — la commande, la
ligne, ce que sa sortie façonne — est tenu une fois, → `MECANISMES
§Périmètre d'audit` ; ce qu'il fait est décrit dans `PROCESS_AVAL.md`
§/9_controle. Rien de cela n'est repris ici.

Un seul fait le concerne dans ce document, parce qu'il touche aussi
`coherence.py` : la graphie de l'interpréteur. Jusqu'au 2026-09-22,
`9_controle.md` ligne 232 et la docstring de `grouper.py` ligne 34
écrivaient `python3` ; sur cet hôte Windows, `python3 --version` ne
répond pas (l'alias `WindowsApps` renvoie au Store) et c'est `python`
qui répond (`docs/verification/chemins-aval.md` lignes 591-592). Les
deux graphies ont été passées à `python` en phase 7 — le shebang de
`grouper.py` (ligne 1, `#!/usr/bin/env python3`) est resté, il ne sert
pas sur cet hôte.

---

# Les commandes

Les trois commandes de ce document partagent quatre traits, vérifiés
au fichier de chacune : elles n'invoquent aucun agent
(`audit_blocages.md` ligne 7 et 206, `audit_conventions.md` ligne 7 et
223 ; `deploie.md` n'a pas `Agent` dans `allowed-tools`, ligne 3) ;
elles sont lancées à la main par le Product Owner, jamais par une autre
commande ; elles n'ont pas `Bash` (→ `MECANISMES §Frontmatter d'une
commande`) et ne commitent donc rien ; elles ne créent pas de worktree.
Leur place dans la table de `CLAUDE.md` (lignes 58-59) vient de
`docs/verification4/plan.md` entrée 23 : avant, la ligne « anything else
is an ordinary request » les faisait traiter comme une demande sans
workflow.

### /deploie — installer les deux applications sur le téléphone et la montre, et dire ce qui s'est passé

Prend : rien — pas d'`argument-hint` (frontmatter, lignes 1-4) ; le
dépôt tel qu'il est sur le disque.
Rend : un rapport en message, une ligne par appareil — le module,
l'identifiant, build passé ou non (lignes 61-62) ; en dernière ligne
`Next: done`, ou `Next: stop <device> missing` sur un appareil absent
(`deploie.md`, *1. Find the devices* et *3. Report* — ajoutés après le
`HEAD` de référence ; → `MECANISMES §Ligne Next:`). Rien dans le dépôt.

**Étapes**
1. `adb devices -l` ; identifier chaque appareil par son modèle, jamais
   par sa position dans la liste : le téléphone `model:SM_S928B`, la
   montre `model:SM_L705F` (lignes 13-21). L'identifiant est la
   première colonne ; celui de la montre change à chaque redémarrage du
   débogage sans fil et se relit à chaque run, jamais de mémoire ni
   d'un rapport antérieur (lignes 23-25).
2. Un appareil manque : s'arrêter et dire lequel ; ne pas installer
   l'autre seul (lignes 27-29).
3. Par l'outil `PowerShell`, jamais `Bash` (lignes 35-36) ; la variable
   sur sa propre ligne, avant la commande (lignes 38-39) :
   `$env:ANDROID_SERIAL = "<phone identifier>"` puis
   `.\gradlew :app-phone:installDebug` ; `$env:ANDROID_SERIAL = "<watch
   identifier>"` puis `.\gradlew :app-wear:installDebug` ; enfin
   `Remove-Item Env:\ANDROID_SERIAL` (lignes 41-47). Une commande à la
   fois, au premier plan, attendue (ligne 49).
4. Effacer la variable à la fin, quoi qu'il soit arrivé (ligne 54).
5. Rapporter : nommer toute erreur, n'en corriger aucune ; une
   installation échouée est un résultat (lignes 64-65).

**Git** : aucun — la commande ne lit ni n'écrit le dépôt, ne commite
pas, ne crée pas de worktree.

**La Product Owner intervient** : elle lance la commande, à la main ;
elle branche les deux appareils ; elle lit le rapport. Rien d'autre.

**Décisions**
- Identifier par le modèle, jamais par la position · écarté : la
  position dans la liste d'`adb` · raison : l'identifiant de la montre
  change à chaque redémarrage du débogage sans fil, et la liste n'a pas
  d'ordre garanti (`deploie.md` lignes 15-16, 23-25) · inconnu.
- Les deux appareils ou rien · écarté : installer celui qui est là ·
  raison : un téléphone mis à jour contre une vieille build de montre
  échoue d'une façon qui se lit comme un défaut de code (lignes
  27-29) · inconnu.
- L'outil `PowerShell`, jamais `Bash` · écarté : `allowed-tools: Bash`,
  ce que le fichier portait · raison : Git Bash rejette `$env:`,
  `.\gradlew` et `Remove-Item` ; les commandes sont PowerShell par
  construction, la ligne d'outil était l'erreur
  (`docs/verification2/plans/commandes.md`, *chemins-aval F15* ;
  `deploie.md` lignes 35-36) ; `docs/verification3/chemins-aval.md`
  ligne 26 et `docs/verification4/chemins-aval.md` ligne 25 le lisent
  « sound » au fichier · inconnu.
- Une commande à la fois, au premier plan · écarté : lancer en
  arrière-plan et sonder · raison : deux runs se disputent le même
  verrou, et un shell que personne n'attend continue après la fin
  (lignes 49-52) · inconnu.
- Effacer `ANDROID_SERIAL` à la fin, quoi qu'il arrive · écarté : la
  laisser · raison : laissée, elle envoie la commande suivante de la
  session au mauvais appareil (lignes 54-55) · inconnu.
- Installer, rapporter, ne rien corriger · écarté : corriger une erreur
  de build · raison : une installation échouée est un résultat, le
  rapport dit ce qui a échoué et s'arrête (lignes 6-7, 64-65) · inconnu.
- Aucun agent · écarté : un agent d'installation ·
  raison : à retrouver · inconnu.

Ce que le fichier ne règle pas, relevé par la première campagne
(`docs/verification/chemins-aval.md` lignes 679-681) et jamais tranché
depuis : la montre qui échoue après un téléphone réussi laisse
exactement l'état que les lignes 27-29 voulaient éviter, et le rapport
en est la seule trace ; `adb` absent du `PATH` n'a pas d'issue écrite ;
deux appareils du même modèle n'ont pas de règle.

### /audit_blocages — lire les fichiers de blocage réglés d'un cycle et rapporter ce qui revient de l'un à l'autre

Prend : le nom du dossier de feature, obligatoire (lignes 12-13) ; le
dossier de travail en est dérivé, → `MECANISMES §Dossier de travail`
(lignes 15-18) — une correction s'audite à part de la feature. Tout
chemin est relatif au dossier de travail (ligne 20).
Rend : `audit-blocages.md` à la racine du dossier de travail, en ajout
(ligne 140) ; un relais qui finit toujours sur `Next: done` — l'audit
ne change rien et n'appelle aucune commande —, ou `Next: stop argument
missing` sans argument (`audit_blocages.md`, l'en-tête et la fin de
*What you write* — ajoutés après le `HEAD` de référence ; →
`MECANISMES §Ligne Next:`).

**Étapes**
1. Lire `audit-blocages.md` s'il existe : ses `## Files read`, une
   sous-section par passe, donnent les fichiers à sauter ; ses
   constats antérieurs se lisent en entier — un motif se voit d'une
   passe à l'autre (lignes 44-45, 54-60).
2. Trouver tout `blocked_*-NN.md` en cinq lieux — `code/**/`,
   `cadrage-produit/`, `convertisseur/`, la racine du dossier de
   travail, `investigation/` (lignes 26-31 ; les emplacements, →
   `MECANISMES §Emplacement des fichiers de blocage`) — et sauter ceux
   que `## Files read` nomme déjà.
3. Trouver tout `blocked_*.md` sans numéro, aux mêmes cinq lieux : le
   lire, le lister sous `### Still open`, ne jamais l'écrire dans
   `## Files read` — une passe ultérieure le relira une fois qu'il
   portera une décision (lignes 36-42).
4. Rien d'autre n'est lu : ni le code, ni les fiches, ni les rapports
   (lignes 47-48).
5. Chercher cinq trouvailles (lignes 64-134) :
   1. ce qui revient — deux blocs nommant un même symbole, fichier ou
      module sont un constat ; le nom est pris dans `## Where` de
      chaque bloc, jamais dans ce dont les blocs parlent ; un nom déjà
      vu dans un `### Names carried by more than one block` d'une
      passe antérieure fait groupe avec lui, la passe qui l'a nommé en
      premier est dite ;
   2. une décision qui ne nomme rien sur quoi elle repose — ni une
      règle par son identifiant, ni une entrée par son numéro, ni un
      symbole où le même problème est déjà réglé ; une mention sans
      identifiant ne compte pas ; les blocs réglés avant l'existence
      de l'Arbitre sont dits une fois et passés ; une décision rendue
      (« not settled here ») ne cite rien et n'est pas de ce constat ;
   3. un bloc qui demande quelque chose hors de portée de son auteur —
      `## To resume` lu à la lettre, contre la liste de ce que chaque
      agent possède : le Cadreur le découpage, le Vérificateur son
      ordre, le Détailleur une fiche, le Concepteur ses déclarations,
      le Testeur ses tests, le Réalisateur le code d'un lot, le
      Relecteur son verdict ;
   4. ce qui a été rendu — un `## Decision` ouvrant sur *not settled
      here* ; la raison qu'il donne est citée, rien d'ajouté ;
   5. deux décisions demandant des formes différentes, sur des blocs
      qui partagent un nom — seulement là ; un nom qui s'étend sur deux
      passes fait rouvrir les blocs antérieurs qu'il nomme, seul cas où
      un fichier de `## Files read` est relu.
6. Écrire : à la première passe, le titre `# Audit of blocks — <working
   folder>` et les deux titres `## Files read` et `## Pass 1` ; sinon,
   ajouter `## Pass <n>` — `n` compté depuis la dernière passe du
   fichier, sans date — et sa sous-section `### Pass <n>` sous
   `## Files read` (lignes 143-172). Six sous-titres sous la passe :
   `### Still open`, `### Names carried by more than one block`,
   `### Decisions resting on nothing`, `### Blocks asking outside their
   author's reach`, `### Handed back`, `### Decisions asking for
   different shapes` (lignes 164-169). Un titre sans rien porte un
   tiret (lignes 174-176). Un constat par ligne, trois parties séparées
   par ` | ` : `<what you found> | <the blocks> | <the field, quoted>`,
   la première ouvrant sur le nom, la règle ou le symbole (lignes
   178-185) ; sous `### Still open`, un chemin par ligne (ligne 187).
   Un constat sans champ cité n'en est pas un (lignes 190-191).

**Git** : aucun — la commande n'a pas `Bash` (ligne 3) ; `audit-blocages.md`
reste dans l'arbre de travail du dépôt principal jusqu'au commit
d'avant-run de la commande suivante du cycle, qui l'emporte avec le
dossier de feature.

**La Product Owner intervient** : elle lance la commande, à la main,
quand elle le veut (ligne 9) ; elle lit le rapport ; ce qu'il faut en
faire est à elle — la commande ne recommande rien et ne corrige rien
(lignes 193-194).

**Décisions**
- Cinq lieux, jamais `code/**/` seul · écarté : un glob sur `code/**/`
  · raison : quatre familles manquées, et l'audit rapporterait qu'une
  feature n'a bloqué sur rien (lignes 33-34) ; `convertisseur/` est le
  cinquième lieu depuis `docs/verification3/plan.md` entrée 12 ; les
  fichiers encore ouverts cherchés aux mêmes lieux depuis
  `docs/verification2/plans/architecte.md`, *chemins-aval F18* · inconnu.
- Grouper sur les noms de `## Where`, jamais sur le sujet · écarté :
  grouper sur ce dont les blocs parlent · raison : c'est un jugement,
  et deux blocs sur *un contrat élargi* peuvent ne partager aucun nom ;
  le nom exact est ce qu'une passe ultérieure apparie (lignes 66-76) ·
  inconnu.
- Ajouter, jamais réécrire · écarté : réécrire le fichier · raison :
  les passes antérieures sont l'archive (lignes 140-141) · inconnu.
- Sauter ce que `## Files read` nomme · écarté : tout relire · raison :
  c'est ce qui rend la passe bon marché à répéter (ligne 58) · inconnu.
- Un fichier ouvert jamais dans `## Files read` · écarté : le compter
  lu · raison : il n'est pas fini, et une passe ultérieure doit le
  relire une fois la décision écrite (lignes 41-42) · inconnu.
- Un numéro de passe, pas de date · écarté : dater la passe · raison :
  la commande n'a pas d'horloge, et c'est l'ordre qui compte (lignes
  143-145) · inconnu.
- Un titre vide porte un tiret · écarté : omettre le titre · raison : un
  titre vide dit *regardé, rien trouvé*, son absence dit *pas regardé*
  (lignes 174-176) · inconnu.
- Un constat sans champ cité est laissé · écarté : le garder ·
  raison : à retrouver · inconnu.
- La liste des possessions (constat 3) nomme le Concepteur et le
  Testeur · écarté : cinq agents · raison : un bloc du Réalisateur
  demandant une déclaration ou un test ne pouvait pas être classé hors
  de portée (`docs/verification4/plan.md` entrée 38) · non éprouvée.
- Le constat 4 lit un `## Decision` ouvrant sur *not settled here* ·
  écarté : un `## Decision` laissé vide pour une question produit ·
  raison : l'Arbitre n'écrivait rien pour une question produit, et le
  constat 4 n'en voyait jamais une
  (`docs/verification2/plans/arbitre.md`, *arbitre F17*) · inconnu.
- Ne rien recommander, ne rien corriger, ne juger aucune décision ·
  écarté : dire si la décision était bonne · raison : la commande
  rapporte ce que les blocs disent, ce qu'il faut en faire est au
  Product Owner (lignes 193-194, 204-205) · inconnu.
- Aucun agent · écarté : un agent auditeur · raison : à retrouver ·
  inconnu.

Ce que le fichier ne règle pas, relevé par la première campagne
(`docs/verification/chemins-aval.md` lignes 708-711) et jamais tranché
depuis : rien sur le disque ne distingue un bloc réglé avant
l'existence de l'Arbitre d'un bloc réglé après — pas de date, pas
d'auteur dans la forme du fichier — et la passe devine.

### /audit_conventions — lire ce que les conventions ont gagné pendant un cycle et rapporter ce que cela coûte

Prend : le nom du dossier de feature, obligatoire (lignes 12-13) ; le
dossier de travail en est dérivé, → `MECANISMES §Dossier de travail`
(lignes 15-17). Les chemins commençant par `docs/` sont relatifs à la
racine du dépôt, les autres au dossier de travail (lignes 19-20, →
`MECANISMES §Chemins relatifs`).
Rend : `audit-conventions.md` à la racine du dossier de travail, en
ajout (ligne 164) ; un relais qui finit toujours sur `Next: done` —
l'audit ne change rien et n'appelle aucune commande —, ou `Next: stop
argument missing` sans argument (`audit_conventions.md`, l'en-tête et
la fin de *What you write* — ajoutés après le `HEAD` de référence ; →
`MECANISMES §Ligne Next:`).

**Étapes**
1. Lire `audit-conventions.md` s'il existe : ses `## Requests read`
   donnent les requêtes à sauter ; ses constats antérieurs se lisent en
   entier (lignes 62-63, 72-79).
2. Lire toute requête `architecte/*.md` (→ `MECANISMES §Requête de
   conventions — divergence`) que `## Requests read` ne nomme pas, avec
   son `## Verdict` ; une requête à verdict vide est listée sous
   `### Requests still untreated` et jamais écrite dans `## Requests
   read` (lignes 26-34).
3. Lire `docs/TECHNICAL_CONVENTIONS.md` en entier, à chaque passe —
   c'est lui qui change (lignes 36, 76-77 ; → `MECANISMES §Lecture des
   conventions — divergence`).
4. Lire `couverture.md` — quelle entrée chaque règle a produite. Sur
   une correction, il n'est pas dans le dossier de travail : le
   chercher un niveau au-dessus, à la racine du dossier de feature
   (lignes 38-46). Absent des deux : les constats 1, 4 et 7 ne peuvent
   pas être faits, chacun le dit sous son titre — *no coverage file* —
   et les autres sont faits (lignes 48-51).
5. Lire du document technique les seules entrées que `couverture.md`
   nomme, une à la fois, pour le constat 4 — dans le document que
   `couverture.md` trace, qui peut être le `spec-technique.md` de la
   feature et non le `desc-bug.md` du cycle (lignes 53-57).
6. Lire les lignes `Anchor` des lots de `code/decoupage.md`, pour le
   constat 7 seul (lignes 59-60 ; → `MECANISMES §Fichiers du
   découpage`). Rien d'autre : ni le code, ni les fiches (lignes 65-66).
7. Chercher sept trouvailles (lignes 85-158) :
   1. ce que le cycle a ajouté — une règle des conventions que
      `couverture.md` ne trace à aucune entrée du document technique
      vient d'une requête ; nommer la règle, la requête, et le lot que
      le nom du fichier de requête porte (`architecte/detailleur-lot-04.md`,
      ou `bugfix-NN/architecte/…` en première colonne sur une
      correction) ; dire que ce lot a été codé sous la règle telle
      qu'elle était, et que la règle écrite pour lui ne gouverne que ce
      qui suit — le Product Owner décide si cela reste ainsi ;
   2. une règle qu'aucun lot ne peut suivre dans sa propre portée — un
      lot produit ou change les symboles de `Produces` et `Modifies` et
      ouvre les fichiers de `Touches` ; une règle qui demande au-delà
      ne peut pas être obéie, et le blocage vient bien plus tard, au
      détail ;
   3. deux règles d'une même section de `TECHNICAL_CONVENTIONS.md`
      demandant des formes différentes — contredire, c'est l'une
      ordonnant ce que l'autre interdit ; dire à quelle entrée chacune
      trace ;
   4. une règle qui lie une chose que son entrée ne nomme pas — ouvrir
      l'entrée que `couverture.md` donne ; une règle qui dit en termes
      de code ce que l'entrée dit en termes de comportement n'est pas
      un constat ;
   5. ce qui a été refusé, et où cela va — un verdict qui refuse nomme
      où la chose va (le code, l'outillage, la machine) ; le citer,
      rien de plus ;
   6. une règle déjà rapportée, inchangée — dite une fois de plus, sous
      le même titre, marquée *standing since pass `<n>`* ;
   7. une règle que le découpage ne rencontre jamais — aucun `Anchor`
      de lot ne cite l'entrée que `couverture.md` lui trace ;
      seulement quand les deux côtés nomment un même document, sinon
      le constat est sauté et dit sous son titre — *coverage and split
      on different documents*.
8. Écrire : à la première passe, `# Audit of conventions — <working
   folder>`, `## Requests read` et `## Pass 1` ; sinon `## Pass <n>` et
   sa sous-section `### Pass <n>` sous `## Requests read` (lignes
   167-195). Huit sous-titres : `### Requests still untreated`,
   `### Rules the cycle added`, `### Rules no lot can follow in its own
   scope`, `### Contradictions`, `### Rules binding what their entry
   does not mention`, `### Refused, and where they belong`,
   `### Standing since an earlier pass`, `### Rules the split never
   meets` (lignes 186-193). Un titre vide porte un tiret (ligne 198).
   Un constat par ligne : `<the rule's identifier> | <what you found> |
   <what it rests on>` — l'identifiant d'abord, la troisième partie
   nommant une entrée, une requête ou une seconde règle (lignes
   200-206) ; sous `### Requests still untreated`, un chemin par ligne
   (ligne 208).

**Git** : aucun — pas de `Bash` (ligne 3) ; `audit-conventions.md`
attend le commit d'avant-run de la commande suivante, comme
`audit-blocages.md`.

**La Product Owner intervient** : elle lance la commande à la main
(ligne 9) ; elle lit le rapport ; elle décide, sur le constat 1, si le
lot codé sous l'ancienne règle reste tel quel (lignes 97-100). La
commande n'édite jamais `TECHNICAL_CONVENTIONS.md` — c'est à
l'Architecte, et seulement par une requête (lignes 210-212).

**Décisions**
- `couverture.md` cherché un niveau au-dessus sur une correction ·
  écarté : le chercher dans le dossier de travail seul · raison :
  l'Architecte l'écrit quand il dérive les conventions, ce qui tourne
  sur le dossier de feature ; les règles qu'il trace tiennent toujours,
  le fichier de conventions étant partagé par tout le projet (lignes
  40-46) · inconnu.
- Sans `couverture.md`, les constats 1, 4 et 7 sont sautés · écarté : 1,
  4 et 6, ce que le fichier disait · raison : le constat 6 repose sur
  les passes antérieures et `TECHNICAL_CONVENTIONS.md` seuls, le
  constat 7 est celui qui repose sur `couverture.md`
  (`docs/verification2/chemins-aval.md` F17 ; lignes 48-51) · inconnu.
- Le constat 7 sauté quand `couverture.md` et les `Anchor` tracent à
  deux documents · écarté : le faire quand même · raison : sur une
  correction, `code/decoupage.md` ancre sur `desc-bug.md` quand
  `couverture.md` trace à `spec-technique.md`, et chaque règle se lisait
  « never met » (`docs/verification4/plan.md` entrée 39) · non éprouvée.
- Le constat 2 lit les fichiers dans `Touches` et les symboles dans
  `Produces` et `Modifies` · écarté : les fichiers dans `Modifies` ·
  raison : `Needs`, `Produces` et `Modifies` portent des symboles
  seulement, jamais un fichier (`docs/verification3/plan.md` entrée 61,
  citant `cadreur.md`) · inconnu.
- Le constat 1 nomme le lot et dit qu'il a été codé sous la règle
  telle qu'elle était · écarté : compter la règle sans le lot ·
  raison : la ligne est la seule trace du lot codé sous l'ancienne
  règle — la décision D16 de la refonte, appliquée comme « only the
  `audit_conventions` line » (`docs/verification/transfert.md` ligne
  141) · inconnu.
- `TECHNICAL_CONVENTIONS.md` relu à chaque passe · écarté : le sauter
  comme les requêtes déjà lues · raison : il change, et c'est le point
  de l'audit (lignes 76-77) · inconnu.
- Ajouter, jamais réécrire ; sauter ce que `## Requests read` nomme ;
  une requête non traitée jamais dans `## Requests read` ; un numéro,
  pas de date ; un titre vide porte un tiret · écarté : leurs
  contraires · raison : les mêmes que pour `/audit_blocages` (lignes
  29-34, 72-74, 164-168, 198) · inconnu.
- Ne rien recommander, ne jamais éditer les conventions, ne pas juger
  si une règle est bonne · écarté : corriger la règle · raison : le
  fichier est à l'Architecte, et seulement par une requête ; l'audit dit
  si une règle peut être suivie, sur quoi elle repose et si elle se
  déclenche (lignes 210-212, 221-222) · inconnu.
- Aucun agent · écarté : un agent auditeur · raison : à retrouver ·
  inconnu.

Ce que le fichier ne règle pas, relevé par la première campagne
(`docs/verification/chemins-aval.md` lignes 727-730) et jamais tranché
depuis : `architecte/cadreur.md` ne porte aucun lot dans son nom, et
`arbitre-<lot>.md` en porte un sous un autre préfixe ; le constat 1 ne
dit pas quoi écrire pour une requête sans lot.

---

# Les scripts

### coherence.py — vérifier mécaniquement la forme des fichiers d'agent et de commande

**Ce qu'il vérifie.** La docstring (lignes 2-16) l'annonce : la classe
de défaut qu'une édition introduit et qu'une relecture voit rarement —
gras non fermé, renvoi mort, compte annoncé qui ne tient plus, numéros
de mouvement en collision, fragment orphelin, ligne répétée, « tools no
gesture names ». Le code (fonction `check`, lignes 54-161) porte douze
étiquettes de constat, imprimées telles quelles :

| Étiquette | Ce qu'elle attrape | Lignes |
|---|---|---|
| `frontmatter` | Une valeur de frontmatter contenant `: ` sans guillemets | 59-67 |
| `table row` | Une ligne ouvrant sur `\|` qui ne se ferme pas sur `\|` | 69-72 |
| `unclosed bold` | Un paragraphe où `**` est en nombre impair, les `code spans` retirés d'abord ; un bloc indenté de quatre espaces est du code, pas de la prose (`paragraphs`, lignes 35-42) | 74-78 |
| `dead reference` | Un `see *…*` dont la cible n'est ni un titre `#` ni une ligne en gras seul ; `below`, `there`, `above` exceptés | 80-87 |
| `count` | `**<nombre en lettres> moves|passes|headings**` contre ce qui suit jusqu'au titre suivant — les `**N.** ` comptés pour `moves` et `passes`, les `    ## ` pour `headings` ; les autres mots (`fields`, `questions`, `filters`, `shapes`, `sources`, `parts`, `invocations`, `places`, `greps`, `reads`, `lines`) sont reconnus mais pas comptés | 89-108 |
| `move numbers` | Dans une suite de `**N.**` entre deux titres, un numéro répété ou un trou ; `2b`, `4b` sont des insertions, pas des numéros | 110-127 |
| `orphan fragment` | Un paragraphe ouvrant sur `and`, `or`, `but`, `which`, `that`, `so` | 129-133 |
| `lowercase opening` | Un marqueur 🔴 ⚠️ 📌 suivi d'un gras ouvrant sur une minuscule, hors une liste de mots admis (`a`, `an`, `the`, `you`, `never`, `every`, …) | 134-140 |
| `empty separator` | Deux `---` sans rien entre eux | 142-144 |
| `trailing rule` | Un fichier qui finit sur `---` | 146-148 |
| `repeated line` | Deux lignes identiques de plus de vingt caractères, l'une sous l'autre | 150-154 |
| `typo` | Trois fautes de frappe que la chaîne a déjà faites — deux graphies de *the*, une de *and* — énumérées dans `TYPOS` (ligne 32) ; les mots ne sont pas recopiés ici, le script les signalerait dans ce document même | 156-159 |

Un lecteur peut vérifier ceci : la docstring annonce « tools no gesture
names », et aucune des douze étiquettes ne compare la liste `tools` du
frontmatter aux gestes du fichier — le contrôle annoncé n'est pas écrit.

**Sa ligne de commande.** `python .claude/scripts/coherence.py` sans
argument vérifie tous les `agents/*.md` et `commands/*.md` du dossier
qui contient `scripts/` — quel que soit son nom, jamais un `.claude/`
fixé (lignes 12-13, 22-24 : `ROOT` est le parent du parent du script ;
c'est ce qui l'a fait tourner sur `.claude-new/` pendant les
campagnes). Avec des arguments, chaque argument est un chemin existant
ou, sinon, un chemin relatif à ce dossier (`agents/x.md`, lignes
165-168). Il imprime, par fichier fautif, le chemin puis une ligne par
constat, `<étiquette> <détail>`, et termine par `<n> finding(s) across
<m> files.` (lignes 173-183).

**Son code de sortie.** 1 si un constat au moins, 0 sinon (ligne 184) —
« so it can gate a commit » (ligne 15). Au `HEAD` local du 2026-09-21 :
`0 findings across 40 files.`, code 0 — vingt agents et vingt commandes.

**Qui le lance, et quand.** Aucune commande de la chaîne, aucun agent,
pas `CLAUDE.md` — la recherche ne le trouve que dans sa propre
docstring. Aucun commit parmi les deux cents derniers ne le nomme. Ses
appelants sont les prompts des campagnes de correction : chaque agent
correcteur le lance sur son propre fichier après chaque édition, pas à
la fin (`docs/verification2/correction.md` ligne 379 : « Run `python3
.claude-new/scripts/coherence.py <your file>` after every edit »), et
la clôture de la campagne le lance sur tout, une fois que tous ont
rapporté, en attendant zéro (`docs/verification2/correction.md` lignes
412-416 : « The chain returned zero before wave 3 — anything here was
introduced by a correction »). Il n'entre dans aucun hook, aucun
commit, aucune commande de cycle.

**La graphie.** La docstring écrit `python` (lignes 9-10) ; les prompts
de campagne écrivaient `python3` (`docs/verification2/correction.md`
lignes 379 et 412, cette dernière avec des antislashs Windows) ; sur
cet hôte `python3` ne répond pas et c'est `python` qui répond — la
chaîne écrit `python` partout depuis la phase 7. Même point que pour
`grouper.py`.

**Décisions**
- Un contrôle par script, après chaque édition · écarté : une relecture
  seule · raison : il attrape un gras cassé ou une ligne perdue pendant
  que l'édition est encore en tête ; une correction sur cinq laissait
  quelque chose derrière elle (`docs/verification2/correction.md`
  lignes 379-381 ; `coherence.py` lignes 4-7 ; les campagnes 2, 3 et 4
  l'ont lancé) · éprouvée.
- Le dossier vérifié est celui qui porte `scripts/`, quel que soit son
  nom · écarté : `.claude/` en dur · raison : la chaîne a vécu sous
  `.claude-new/` pendant les campagnes (lignes 12-13, 22-24) · éprouvée.
- Code de sortie 1 sur constat · écarté : toujours 0 · raison : pour
  pouvoir barrer un commit (ligne 15) — ce qu'aucun hook ne fait ·
  inconnu.
- Les blocs indentés exclus, les `code spans` retirés avant de compter
  les `**` · écarté : compter tout · raison : à retrouver · inconnu.
- Trois fautes de frappe en dur · écarté : un correcteur général ·
  raison : « words this chain has got wrong before » (ligne 31) ·
  inconnu.

---

# Les fichiers

### GRILLE_CONVENTIONS_RETIREES.md — les trente-quatre entrées retirées de la grille des conventions, avec leur texte, pour pouvoir les remettre

**Ce qu'il tient.** Trente-quatre des soixante-dix entrées de la partie
B de `.claude/grids/GRILLE_CONVENTIONS.md`, retirées, avec leur texte
entier (lignes 3-5). Une explication du retrait (lignes 7-22) : chaque
entrée a été mesurée — sa *Question* lue seule, une réponse écrite à
froid, puis la *Form* comparée — et classée en trois classes : *open
door* (34 — la réponse à froid rencontre la Form, l'entrée prescrit ce
qui aurait été fait de toute façon), *correction* (24 — la Form
attrape une vraie erreur), *arbitration* (12 — deux choix défendables).
Les trente-quatre sont les portes ouvertes ; trois causes historiques
sont avancées, toutes corrigées depuis — un document technique
déconnecté du produit, un Détailleur qui manquait des choses, Sonnet où
Opus était requis — et « that can only be proved by withdrawing them
and watching » (lignes 18-22). Puis les entrées, chacune sous la forme
de la grille — `**G<n>.<m>** · *Question* · *Trigger*`, `- **Form**`,
`- **Test**` — sous les titres `## C2 — Verification`, `## C3 —
Boundaries`, `## C5 — Interface contracts`, `## C9 — Diagnostics`,
`## C12 — Dependencies and versions`, plus `G1.3` avant tout titre
(lignes 35-38) et `G7.8`, `G8.3` entre deux séparateurs sans titre
(lignes 257-275). Les entrées : G1.3 ; G2.2, G2.3 ; G3.1, G3.2, G3.3 ;
G4.2, G4.3, G4.5, G4.6, G4.7, G4.8, G4.9 ; G5.2, G5.3, G5.4, G5.9,
G5.10 ; G6.1, G6.3, G6.5 ; G7.1, G7.2, G7.3, G7.7, G7.8 ; G8.3 ; G9.1 ;
G10.2, G10.3, G10.4, G10.5 ; G11.3 ; G12.1. Un lecteur peut vérifier
que les G4 sont classés sous le titre C3 et les G6, G7 sous le titre C5
— les titres de section ne suivent pas la numérotation.

**Quand en remettre une.** Un lot décide quelque chose que l'entrée
aurait réglé, et le décide mal — c'est le signal, jamais une lecture
qui trouve l'entrée sensée : chacune l'est, c'est ce qui en a fait une
porte ouverte (lignes 26-29). On remet le texte tel qu'il est, dans sa
section (ligne 31). `GRILLE_CONVENTIONS.md` lignes 587-590 dit la même
chose de son côté : « A rule the file no longer produces is not a gap to
fill … Put an entry back only when a lot decides wrong what it would
have settled — see the archive ».

**Qui le lit.** Personne dans la chaîne : aucun agent, aucune commande
ne le nomme ; l'Architecte, seul lecteur de `GRILLE_CONVENTIONS.md`,
n'a pas ce fichier dans sa liste de lecture ; `/conventions` et
`/audit_conventions` ne le nomment pas. Il est nommé une fois, par
`GRILLE_CONVENTIONS.md` lignes 580-582 (« The grid held seventy entries
until thirty-four were withdrawn — `GRILLE_CONVENTIONS_RETIREES.md`
holds them, with their text and the reason »). La première campagne
l'a établi (`docs/verification/fichiers.md` lignes 198-200, A4 : « no
agent reads it. PO's own document » ; `docs/verification/renommages.md`
ligne 216 : « Read by nobody … consistent with its own header »).
L'orchestrateur a interdiction d'ouvrir `docs/process/` (`CLAUDE.md`,
*What you never do*). Son lecteur est le Product Owner, quand un lot
décide mal.

**Pourquoi il est gardé.** « To be able to put them back — not to
remember them » (lignes 3-5) : le texte exact d'une entrée est ce qui
permet de la remettre sans la réécrire, et le retrait est une
expérience dont le fichier est le témoin — les trois causes avancées
« can only be proved by withdrawing them and watching ». Sans lui, une
entrée remise serait réécrite de mémoire, et la grille ne saurait plus
ce qu'elle a mesuré.

**Verdict.** Annexe : aucun agent ne le lit, aucune règle n'en dérive,
et le remettre une entrée est un geste du Product Owner sur
`GRILLE_CONVENTIONS.md` — c'est alors la grille qui change, pas ce
fichier, et ce changement-là relève de `PROCESS_AMONT.md`
§architecte — ce qui vaut pour ses quatre invocations, qui dit comment la grille est lue.

**Décisions**
- Garder le texte entier des entrées retirées · écarté : une liste
  d'identifiants, ou rien · raison : pour pouvoir les remettre telles
  quelles, pas pour s'en souvenir (lignes 3-5, 31) · inconnu.
- Remettre sur un lot qui décide mal, jamais sur une lecture · écarté :
  remettre une entrée trouvée sensée · raison : chacune est sensée,
  c'est ce qui en a fait une porte ouverte (lignes 26-29) · inconnu.
- Hors de la liste de lecture de l'Architecte · écarté : le lui donner
  avec la grille · raison : à retrouver · inconnu.

---

## Inventaire

Commandes décrites : `/deploie`, `/audit_blocages`, `/audit_conventions`.

Scripts décrits : `.claude/scripts/coherence.py`.

Fichiers décrits : `docs/process/GRILLE_CONVENTIONS_RETIREES.md`.

Candidats renvoyés ailleurs, avec leur destination :
- `.claude/scripts/grouper.py` → `PROCESS_AVAL.md` §/9_controle — confronter le fichier produit à toutes les fiches — appelé
  à `.claude/commands/9_controle.md` ligne 232, ses groupes imprimés
  forment les invocations du Contrôleur.

Agents décrits en entier : aucun.
Agents portés en entrée courte : aucun.
