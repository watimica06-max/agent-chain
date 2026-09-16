# Décisions structurelles — chaîne d'agents

> 🔴 **La référence.** 📌 **Tout y est tranché, et tout est passé dans
> la chaîne** — ⚠️ **c'est contre ce fichier qu'on vérifie que ce qui
> a été écrit correspond à ce qui a été décidé.**
>
> **Sources de l'analyse** : `proposition.md` *(conception en
> aveugle)*, `verdict.md` *(jugement sur les PROCESS)*, et les
> dix-huit fiches de `passes/`.

## Comment le lire

| Section | Ce qu'elle porte |
|---|---|
| **A** | 🔴 **Les sept sujets instruits** — le genre, la fermeture contre l'existant, les tests avant le code, la recette, le registre, les deux niveaux de question, les règles transverses |
| **C** | 📌 **Les écartés**, avec leur raison |
| **R · F · U · D · P · Q** | 📌 **Le verdict, point par point** : ruptures, rôles manquants, boucles, défauts de frontière, prémisses, questions d'agents |

⚠️ **Une décision écartée garde sa raison** — 🔴 **ne pas la rouvrir
sans un cas observé.**

---

# A — Sujets instruits

## A1 · Le genre d'un passage du fichier d'idées
**Statut : tranché — le principe, les six genres, le placement et le
partage.** 📌 **Reste l'écriture, et trois vérifications.**

### Le principe

🔴 **Un passage du fichier d'idées qui n'est pas un comportement doit
pouvoir être reconnu comme tel et suivre son propre chemin**, au lieu
d'être forcé en bloc.

⚠️ **Aujourd'hui la chaîne n'a pas de case pour dire non.** Le Rédacteur
doit en faire un bloc, le Classeur doit lui trouver une nature, la
grille doit le sonder. 📌 **Personne ne peut refuser** — c'est pourquoi
le défaut est silencieux : rien ne se plaint, et des blocs vides
descendent jusqu'au code.

**Le cas observé :** `idees.md` §3.2 (typographie) est devenu B4, B5,
B6, tous `Nature: presentation`, sans déclencheur ni production. B5 est
même la *justification* de B4 (« un chrono ne change jamais de
largeur »), devenue un bloc de plus.

**Ce que ça coûte :** le Classeur choisit une nature faute de mieux ·
la grille sonde l'absence, la zone d'écran, le libellé — sans objet ·
le Convertisseur en fait des entrées §7 · le Cadreur en fait un lot qui
ne construit rien · **et l'Architecte, le vrai destinataire, ne les
reçoit jamais comme convention.**

### Genre ≠ nature

🔴 **La nature répond à *que produit ce bloc ?*** — huit réponses, et
elle suppose qu'il produit quelque chose.

🔴 **Le genre répond à *quelle sorte de passage est-ce ?*** — et il dit
si le passage a une nature. 📌 **Une directive n'en a aucune.**

### Les six genres, et leur aiguillage

| Genre | Ce que c'est | Où il va |
|---|---|---|
| **comportement** | Ce que le produit fait, montre ou refuse | Le fichier produit, en bloc — la chaîne telle qu'elle est |
| **directive** | Une contrainte technique que le Product Owner a tranchée | Les conventions du projet |
| **transverse** | Une règle qui vaut pour plusieurs blocs, sans en nommer aucun | Le fichier produit — 📌 **nommée aux Sondeurs pendant la boucle** *(la commande grepe `Genre:`)*, **partagée au Convertisseur après** |
| **référence** | Un catalogue, un tableau de formats que des comportements citent | La section Text du document technique, **directement** |
| **hors périmètre** | Ce que le Product Owner écarte | Le préambule — 📌 **et la grille sait ne pas le redemander** |
| **recette** | Ce que le Product Owner veut vérifier lui-même sur l'appareil | 🔴 **Sort de la chaîne** et lui revient après le code |

### Ce qu'il faut faire de chacun

**Comportement** — rien de nouveau.

**Directive** — elle atteint l'Architecte sans passer par le découpage
en blocs, et 🔴 **ne reçoit jamais de question**. ⚠️ **La contrepartie
est pour le Product Owner** : une directive qu'il juge fausse, il la
change lui-même — personne ne la discutera.

**Transverse** — elle reste dans le fichier produit, et la grille la lit
en même temps que les blocs concernés. 🔴 **Il faut donc savoir
lesquels** : c'est la seule vraie difficulté des six. **Sujet A7**, et
condition du niveau *défaut* (A6).

**Référence** — 🔴 **la section Text n'est alimentée par personne
aujourd'hui** : elle est écrite par la transversale du Convertisseur à
partir des libellés cités dans les écrans, jamais à partir d'un
catalogue. ⚠️ **Une annexe de formats n'a donc aucun chemin.**

**Hors périmètre** — le chemin existe (Rédacteur → préambule →
Cadreur) et fonctionne. 📌 **Le genre sert ailleurs** : la grille
redemande aujourd'hui ce que le Product Owner a déjà écarté (C1.2),
donc il répond deux fois. ⚠️ **Le mécanisme reste à trouver** — 🔴 **pas
une case par question** : voir C5.

**Recette** — 🔴 **elle ne produit rien : la transporter, c'est la faire
sonder, classer, convertir et découper pour rien.** Elle revient au
Product Owner après le code, avec ce que le Contrôleur signale
(**sujet A4**).

### Ce que les cinq genres non-comportement ont en commun

🔴 **Aucun n'a de déclencheur** — aucun n'aurait dû devenir un bloc, et
chacun est aujourd'hui sondé pour rien.

### Où le geste se place — tranché

**La séquence :**

| # | |
|---|---|
| 1 | Lexique |
| 2 | Le Rédacteur écrit les blocs |
| 3 | Le Découpeur affine |
| 4 | 🔴 **Une passe sur les genres** — un agent, une ligne `Genre:` par bloc |
| 5 | La passe sur les natures — 📌 **sur les seuls comportements** |
| 6 | Les Sondeurs |

🔴 **Le genre avant la nature** : seul un comportement a une nature.
📌 **Le Classeur cesse de chercher une nature à ce qui n'en a pas** —
le défaut B4/B5/B6 est réglé à la source.

🔴 **Le genre avant les Sondeurs** : la grille ne sonde que les
comportements, charge les transverses en contexte (A7), et sait ne pas
redemander le hors-périmètre.

📌 **Après le Découpeur, un bloc porte un seul sujet, donc un seul
genre** — ⚠️ **le cas de la phrase mixte disparaît de lui-même.**

### Poser le genre ≠ partager les fichiers

🔴 **Deux gestes distincts, à deux moments.**

**Poser le genre** — au point 4. 📌 **La ligne `Genre:` vit dans le
fichier maître**, et un grep suffit à tout ce qui en dépend pendant la
boucle. ⚠️ **Elle est reposée à chaque tour, comme la nature.**

**Partager en N fichiers** — 🔴 **après la boucle de la grille, quand le
fichier produit est figé.** 📌 **Porté par `/5_reclasse`** : elle fait
déjà un travail mécanique — grep, recopie, comptage — 🔴 **c'est un
geste de plus de la même nature, sans agent.**

**Les destinations :**

| Fichier | Qui le lit |
|---|---|
| Les comportements | La chaîne, telle qu'elle est |
| Les directives | L'Architecte |
| Les transverses | ⚠️ **Les Sondeurs aussi** — en contexte, jamais sondés (A7) |
| Les références | Le Convertisseur, pour la section Text |
| Le hors-périmètre | Le Convertisseur, pour le préambule |
| La recette | Le Product Owner, en fin de cycle (A4) |

🔴 **Les fichiers précédents sont supprimés à chaque partage** —
📌 **l'archivage n'a pas d'utilité ici.** ⚠️ **Ce sont des vues** : le
fichier maître reste la source, et un bloc mal genré n'est jamais
perdu.

### Le risque, et l'asymétrie qui le contient

⚠️ **Un bloc qui part n'est plus sondé** — 🔴 **une erreur de genre fait
disparaître un comportement de la chaîne, silencieusement.**

🔴 **D'où : dans le doute, `comportement`.** 📌 **Une règle mal classée
en comportement ne coûte qu'une question de trop ; mal classée
ailleurs, elle ferme à tort.** ⚠️ **Les deux erreurs ne coûtent pas la
même chose, et l'agent doit le savoir.**

### Ce qui reste à vérifier

- 📌 **Le Découpeur face à un bloc sans déclencheur** — son critère est
  « un déclencheur, une production ». ⚠️ **Que fait-il d'une directive ?**
- 📌 **La langue** — une recette rendue au Product Owner aura été
  traduite en anglais par le Rédacteur
- ⚠️ **Une justification devenue bloc** (B5 dans l'exemple) — 🔴 **la
  relation à ce qu'elle explique est perdue**, et le compte des
  directives est faux. **Problème du Rédacteur, pas du genre.**

### La frontière conventions / produit, posée avec le Product Owner

| | |
|---|---|
| **Conventions** | Ce qui vaut pour tout le projet, sans nommer d'écran : palette, familles et graisses, espacements, rayons, durées — **et la règle d'emploi d'un jeton** (`font-data` pour toute donnée chronométrée) |
| **Produit** | Ce qu'un écran fait de ces jetons, et toute règle qui nomme un écran |

⚠️ **Le sens d'un jeton reste du produit** — que « en avance » se dise
`ahead` est du vocabulaire (Lexicographe, puis fichier produit). Ce qui
va aux conventions, c'est comment ce jeton se nomme et se range dans le
code.

### Ce qui reste à construire

🔴 **Deux destinations sur six n'existent pas** : la directive vers les
conventions, et la règle transverse lue avec ses blocs (A7). 📌 **Le
sujet n'est pas « poser un genre », c'est « ouvrir ces
destinations ».**

**D'où vient l'idée :** le Mapper de `proposition.md`. 📌 **On ne
reprend ni son découpage en unités (**C4**), ni son tableau de
renvois** — le verdict juge notre passe B plus forte, puisqu'elle
recroise tout à chaque tour.

**Rebouclage :** D9, D14, D15 · C5 · A7 · A4.

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| 🆕 **Un agent du genre** | Pose une ligne `Genre:` par bloc, entre le Découpeur et le Classeur. Six genres. 🔴 **Deux sorties de doute** : sur le genre → `comportement` ; sur le périmètre d'une transverse → une question obligatoire |
| 🆕 **Sa commande** | Entre `/3_decoupe` et `/3b_nature`. 📌 **Son *What to run next*** : questions non vides → `/1_lexique` ; vides → `/3b_nature` |
| `.claude/commands/1_lexique.md` | 📌 **Accepte son fichier de questions** — la route unique |
| `.claude/commands/5_reclasse.md` | 🔴 **Porte le partage en N fichiers**, par script, après la boucle de grille. Supprime les fichiers précédents. Compte : autant de blocs en sortie qu'en entrée, aucun `Genre:` vide, aucun genre hors des six |
| `.claude/agents/classeur.md` | Ne pose une nature que sur les `comportement` |
| `.claude/agents/sondeur.md` · `commands/4_grille.md` | Ne sondent que les comportements ; 🔴 **chargent le fichier des transverses en contexte** ; savent ne pas redemander le hors-périmètre |
| `.claude/agents/convertisseur.md` · `commands/6_convertit.md` | 🔴 **Les transverses vont à toutes les invocations de nature** ; **les références et le hors-périmètre à la transversale** |
| `.claude/agents/architecte.md` | Reçoit le fichier des directives |
| `.claude/CLAUDE.md` | Inventaire des agents et des commandes |
| `docs/process/PROCESS_AMONT.md` | La séquence, les six genres, le partage |

---

## A2 · Fermer un comportement qui en modifie un existant
**Statut : tranché sur le *quoi*. 🔴 Le *comment* reste à écrire.**

### Le problème

📌 **Une description qui modifie l'existant part de lui sans le redire.**
« L'écart passe aussi en rouge au-delà de 30 secondes » suppose tout le
reste de l'écran. ⚠️ **La grille ne voit que la phrase et ferme sur elle
seule** — alors que le comportement réel est la phrase **plus** ce
qu'elle modifie.

🔴 **Et la grille pose déjà la question sans pouvoir y répondre** :
`C1.3` — « pour chaque règle existante que la fonctionnalité touche :
conservée, changée, retirée ? Le silence n'est pas un retrait. »
⚠️ **Le Sondeur ne lit que le fichier de la fonctionnalité et la
grille** ; son interdit est explicite.

📌 **Ce mécanisme existait dans la première mouture de la chaîne** — la
grille devait se passer contre le global. 🔴 **Il a été perdu au fil des
itérations** : ce n'est pas une idée à importer, c'est un mécanisme à
retrouver. *(L'idée vient du Locator de `proposition.md`, qui le fait
sur le code.)*

### Ce qu'on modifie

**1. Le Rédacteur transmet une information qu'il produit déjà.**
📌 **Il grepe l'index du global pour ranger chaque bloc** — donc il sait
si un bloc se rattache à quelque chose qui existe. 🔴 **Cette
information meurt aujourd'hui dans son contexte ; elle doit survivre.**
⚠️ **C'est un ajout à ce qu'il écrit, pas un geste de plus.**

**2. Un second temps de fermeture.**

| | |
|---|---|
| **Temps 1** | La grille actuelle, sur le fichier de la fonctionnalité seul, jusqu'au fichier de questions vide — 📌 **inchangée**, sauf peut-être à la marge |
| **Temps 2** | 🔴 **Nouveau** : sur les seuls blocs marqués, chargés avec la partie du global qu'ils touchent. **Après le temps 1, sans retour** |

**3. Une nouvelle grille à écrire.** 🔴 **Elle ne cherche pas ce que la
fonctionnalité laisse ouvert** — c'est le temps 1. **Elle cherche ce
qu'elle heurte** : une place, un nom, une ressource déjà occupés · une
règle qui en contredit une existante · 📌 **et l'inverse** : ce que la
fonctionnalité retire sans le dire.

📌 **Sa forme est celle de la passe B, sur un autre corpus** — au lieu
de croiser les blocs entre eux, elle croise les blocs de la
fonctionnalité avec ceux du global. ⚠️ **La forme a fait ses preuves ;
c'est le corpus qui change.**

**Le cas d'école :** le bouton va en bas à droite, et le global dit
qu'il y a déjà un bouton en bas à droite. 🔴 **La question est un
arbitrage** : que deviennent les deux ?

**4. Le Sondeur doit pouvoir lire le global.** 🔴 **Son interdit actuel
est explicite.** 📌 **À ouvrir pour le temps 2 seulement, et limité aux
sections concernées.**

### Ce qui ne change pas

📌 **Le fichier de la fonctionnalité accueille les blocs d'arbitrage**,
y compris ceux qui décrivent ce que devient l'existant — le Fusionneur
les portera au global, comme il le fait déjà. ⚠️ **Peu importe qu'ils
n'appartiennent pas à la fonctionnalité.** La route des réponses, le
Classeur, le Convertisseur : inchangés.

### Pourquoi le global, et non le code

🔴 **La question est une question produit** : elle porte sur
l'intention, et le code ne la dit pas — il faut l'interpréter, avec le
risque de classer *nouveau* ce qui est *modifié* (verdict P4).

📌 **Le global est écrit dans les mots du Product Owner, se lit par son
index** — un grep sur `^#`, puis on ne charge que les sections utiles —
🔴 **et il ne dérive pas** : le Fusionneur le met à jour à la fin de
chaque cycle et après les bugfix, **avant toute nouvelle
fonctionnalité**.

**Supprimer le global au profit du code : écarté.** 📌 Le Rédacteur s'en
sert pour retrouver un sujet, le Fusionneur pour la vue d'ensemble, et
c'est le seul endroit où le Product Owner relit son produit.

### Un second besoin, distinct — modifier plutôt que créer

⚠️ **Celui-là est de l'aval, et l'instrument est le code, pas le
global.** 📌 **Le Cadreur doit savoir qu'il modifie un écran existant,
le Détailleur qu'il change une signature au lieu d'en poser une neuve.**
🔴 **Le Cadreur grepe déjà le code** — **à vérifier quand on instruira
l'aval** : le fait-il assez tôt ?

### Limites assumées

- 🔴 **Le tri dépend du jugement du Rédacteur**, que personne ne
  vérifie. Un bloc mal rangé est un trou silencieux
- 📌 **Le grain — bloc ou section — dépend de ce que contient l'index du
  global**
- ⚠️ **Un arbitrage qui crée un bloc entièrement neuf** (« les deux
  boutons vont dans un menu ») **n'aura jamais été passé au temps 1**
- ⚠️ **Le global dit ce qui a été *décidé*, pas ce qui a été *codé*** —
  c'est au Contrôleur de fermer cet écart, et le verdict signale qu'il
  ne peut pas se lancer aujourd'hui (D20)

**Rebouclage :** D20 · ⚠️ **quelle invocation de la grille charge la section du global — à trancher à l'écriture.**

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/redacteur.md` | 🔴 **Transmettre le rattachement** : ce bloc se rattache à une section existante du global, ou non. **L'information existe déjà** (il grepe l'index), elle meurt dans son contexte |
| 🆕 **Une grille du temps 2** | Ce que la fonctionnalité **heurte** : une place, un nom, une ressource déjà occupés · une règle qui en contredit une existante · ce qu'elle retire sans le dire. 📌 **Forme de la passe B, corpus différent** |
| `.claude/agents/sondeur.md` | 🔴 **Ouvrir la lecture du global**, pour le temps 2 seulement, limitée aux sections concernées |
| `.claude/commands/4_grille.md` | Orchestre le temps 2 après le temps 1, sur les seuls blocs marqués, sans retour |
| `docs/process/PROCESS_AMONT.md` | Les deux temps, et pourquoi le global plutôt que le code |

---

## A3 · Les tests écrits avant le code
**Statut : tranché sur le *quoi*. 🔴 Le *comment* reste à écrire.**
*(D'où vient l'idée : le Designer et le Tester de `proposition.md`.)*

### Le problème, observé

🔴 **Des tests qui ne vérifiaient rien.** 📌 **Un test écrit après le
code, par le contexte qui a écrit le code, affirme ce que le code
fait** — écrit avant, par un contexte qui n'a lu que la spécification,
il affirme ce que la spécification dit.

📌 **Et le Relecteur ne le rattrape pas** : il compare des tests à des
critères en les lisant, et 🔴 **une lecture ratifie, elle ne détecte
pas** — le PROCESS le dit lui-même. Son travail est mince faute
d'instrument.

### Ce qu'on modifie

**Le codage d'un lot passe d'un contexte à trois** :

| | Ce qu'il fait |
|---|---|
| **Concepteur** | Nomme les symboles, écrit les fichiers d'interface avec des corps vides, 🔴 **compile**, commite |
| **Testeur** | Écrit un test par critère depuis la fiche et les interfaces — ⚠️ **il ne peut pas voir les corps, ils n'existent pas** — puis 🔴 **vérifie que chaque nouveau test échoue et que les anciens passent** |
| **Codeur** | Remplit les corps jusqu'à ce que les tests passent. 🔴 **Ne modifie jamais un test** |

**Trois contrôles mécaniques remplacent une lecture :**

| | Ce qu'il prouve |
|---|---|
| **La compilation des corps vides** | La signature tient dans le langage — ⚠️ **aujourd'hui elle vit en prose dans la fiche, et rien ne la compile avant le codage** |
| **Le test rouge** | Le test affirme quelque chose — 📌 **un test qui passe sur du vide n'affirme rien** ; aujourd'hui nos tests naissent verts |
| **Le test vert après codage** | Le code satisfait le critère |

**Le Relecteur** : 📌 **son point 2 et une partie du 4 deviennent
mécaniques et se font plus tôt.** 🔴 **Mais il reste** — ses points 1, 3
et 5 n'ont personne d'autre. ⚠️ **Le point 5 lit les corps** — il ne
devient pas mécanique. 📌 **Son trou demeure, et il est étroit** : il
attrape **le code mort du lot**, pas le code qui fait *plus* que le
critère **et qui sert**. *(F1, renversé.)*

### Le coût — estimé, pas mesuré

📌 **La génération ne bouge pas** : le même code et les mêmes tests sont
écrits. 🔴 **Le surcoût est uniquement ce qu'on relit.**

🔴 **Net : deux chargements complets de plus par lot** — Concepteur et
Testeur ajoutés, **et le Relecteur reste** *(F1, renversé)*.

📌 **Soit ≈ +30k jetons par lot sur une base estimée à 40–45k — de
l'ordre de +60 %.** **Sur 100 lots : ≈ 4,5M → 7,5M.** 🔴 **Ça n'explose
pas, et le gain de robustesse paie.**

⚠️ **Estimation sur des tailles que je n'ai pas mesurées** —
`TECHNICAL_CONVENTIONS.md`, une fiche réelle, les fichiers de code.
📌 **Chiffre à confirmer au premier cycle.**

🔴 **Le terme dominant est identifiable : les conventions, lues en
entier une fois de plus.** 📌 **Levier** : qu'un agent ne lise que la
partie qui le concerne — le Testeur n'a besoin que des conventions de
test. ⚠️ **Rejoint D12** : qui lit les conventions, et en entier ou non,
est dit de deux façons contradictoires.

**Décision du Product Owner : on met le process en place, et on
optimise les lectures ensuite.**

### Ce qui reste à trancher

- 🔴 **Qui compile les corps vides** — le Détailleur, à qui son fichier
  interdit aujourd'hui d'écrire du code, ou un agent de plus
- 🔴 **Le grain** — 📌 **chez lui, Concepteur et Testeur tournent par
  lot ; notre Détailleur tourne par bloc**, pour toute une série de lots

⚠️ **L'aval n'a pas tourné depuis la reconstruction** — le coût réel ne
se mesurera qu'au premier cycle.

**Rebouclage :** **F1** *(le Relecteur reste)* · **D14** *(le levier :
le Réalisateur ne lit plus tout le fichier de conventions)* ·
**D19** *(le test rouge est l'antidote partiel au résultat recopié)* ·
**A4** *(le Testeur écrit la recette)*.

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| 🆕 **Un agent Concepteur** | Nomme les symboles, écrit les interfaces à corps vides, 🔴 **compile**, commite |
| 🆕 **Un agent Testeur** | Un test par critère, depuis la fiche et les interfaces. 🔴 **Vérifie que chaque nouveau test échoue, et que les anciens passent** |
| `.claude/agents/realisateur.md` | Réduit au codage : remplit les corps jusqu'au vert. 🔴 **Ne modifie jamais un test** |
| `.claude/agents/relecteur.md` | 🔴 **Il reste** (F1). Son point 2 et une partie du 4 deviennent mécaniques ; **ses points 1, 3 et 5 demeurent** — ⚠️ **le 5 lit les corps** |
| `.claude/agents/detailleur.md` | 🔴 **À trancher** : qui compile les corps vides — lui, à qui son fichier interdit d'écrire du code, ou le Concepteur |
| `.claude/commands/8_code.md` | Orchestre trois contextes par lot au lieu d'un |
| `docs/process/PROCESS_AVAL.md` | Le découpage du codage, et le coût assumé *(≈ +60 %)* |

---

## A4 · La recette manuelle
**Statut : tranché sur le *quoi*. 🔴 Le *comment* reste à écrire.**
*(D'où vient l'idée : le Tester de `proposition.md`, qui écrit une ligne
par comportement qu'aucun test ne peut exercer.)*

### Le cas observé

📌 **Un fichier de tests manuels a existé, puis a été abandonné** — 🔴
**non parce qu'il était inutile, mais parce qu'il était impraticable** :
des milliers de tests dans tous les sens, non ordonnés, avec des
suppressions et des remises de données au milieu. ⚠️ **Le Product Owner
ne le faisait jamais.**

📌 **Aujourd'hui il teste sans guide.** Le Contrôleur écrit ce qui
manque, pas où regarder.

### Ce qu'on modifie

🔴 **Trois exigences, tirées de l'échec précédent :**

| | |
|---|---|
| **Ordonnée par état, pas par intention** | 📌 **Tout ce qui se vérifie sur une application vide, puis avec une course, puis avec plusieurs.** ⚠️ **Chaque remise à zéro coûte cher** : le moins possible, et annoncées |
| **Courte, donc filtrée** | 🔴 **Seulement ce qu'un test automatique n'a pas pu vérifier.** 📌 **Revérifier à la main un critère couvert par un test qui passe ne prouve rien** — c'est ce filtre qui sépare 40 lignes de 400 |
| **Une ligne = une chose à regarder** | 📌 **Dans les mots du Product Owner, avec ce qu'on attend.** ⚠️ **Pas « vérifier B12 »** mais « ouvrir la liste vide : un message dit de coller un résultat » |

### Qui l'écrit, et quand

🔴 **Construite au fil des lots**, par l'agent qui écrit les tests : il
est le seul à savoir pourquoi un comportement n'est pas testable — il
vient d'essayer. 📌 **Et il l'écrit avant le codage**, donc la liste
existe même si un lot échoue.

⚠️ **Pas par le Contrôleur** : il ne lit pas le code et ne sait pas ce
qui a été testé automatiquement.

🔴 **Assemblée et ordonnée à la fin**, une fois le Contrôleur passé —
📌 **c'est le moment où le Product Owner teste**, et ordonner par état
demande une vue d'ensemble que seul un agent de fin de chaîne possède.

**Rebouclage :** 🔴 **A3** — si les tests sont écrits avant le code,
l'agent qui tient cette liste existe ; sinon, elle revient au
Réalisateur. 📌 **A1** — le genre `recette` porte ce que le Product
Owner *veut* vérifier ; **ce sujet porte ce que la chaîne *n'a pas pu*
vérifier.** ⚠️ **La liste finale porte les deux.**

📌 **Ce que le Product Owner en fait** : un écart constaté devient une
`bug-list.md` pour un cycle de correction — **le chemin existe déjà.**

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| 🆕 **Testeur** *(A3)* | Une ligne par comportement qu'aucun test ne peut exercer : **ce qu'il faut regarder**, dans les mots du Product Owner. 📌 **Écrite avant le codage** |
| `.claude/commands/9_controle.md` | 🔴 **Assemble et ordonne la recette** — par état, pas par intention ; filtrée ; une ligne = une chose à regarder. ⚠️ **Deux sources** : les lignes du Testeur, **et le fichier `recette` du partage** *(A1)* — ce que le Product Owner voulait vérifier |
| `docs/process/PROCESS_AVAL.md` | La recette, et l'échec du fichier précédent *(impraticable, non ordonné)* |

---

## A5 · Le registre des questions produit échappées
**Statut : tranché. 🔴 Trois dépendances à traiter avec.**
*(D'où vient l'idée : le `grille.md` de `proposition.md`, qui gagne une
ligne à chaque question produit atteignant le codage. Rupture 4 et P7
du verdict.)*

### Le problème

🔴 **Une question produit qui surgit en aval prouve qu'une classe
manquait à la grille.** 📌 **Le Product Owner y répond, et le cas se
perd.** ⚠️ **La même faille est payée à chaque fonctionnalité** — la
grille s'édite à la main, hors chaîne.

### Ce qu'on ajoute

🔴 **Un registre, ramassé en fin de cycle par la commande du
Contrôleur.** 📌 **Deux sources :**

| La source | Où elle est en fin de cycle |
|---|---|
| Les *doutes* et les *intentions manquantes* | Le Contrôleur vient de les écrire |
| Les questions produit que l'Arbitre a rendues | Les fichiers de blocage — ✅ **D17 corrigé** |

🔴 **Les trous de couverture de l'Architecte n'y vont pas** — 📌 **le
registre sert pour l'aval**, où le Product Owner répond pour ne pas
bloquer et où le cas se perd. ⚠️ **Dans l'amont, il est déjà en train de
répondre à des questions, la chaîne en tête : un trou de grille se
corrige sur-le-champ, et il n'y aura pas de « plus tard ».** *(Décision
du Product Owner — voir D15.)*

🔴 **Elle ramasse, elle ne conclut pas.** Un fichier, un cas par ligne.
**Aucune classe proposée, aucune modification de la grille.** 📌 **C'est
le Product Owner qui en tire une classe quand une même forme revient
deux fois.**

📌 **Pourquoi en fin de cycle et non au fil de l'eau** : un cas isolé ne
dit rien ; dix cas ensemble laissent voir une forme.

### Le périmètre de la commande

🔴 **Elle rend trois choses au Product Owner, et rien d'autre** : **la
recette manuelle ordonnée** (A4), **ce registre**, et **les décisions
produit prises pendant le codage** *(ci-dessous)*. ⚠️ **Sans cette
limite, elle deviendrait un orchestrateur déguisé.**

📌 **Elle tourne sur le cycle principal et sur chaque cycle de
correction.** 🔴 **Le Contrôleur, lui, ne tourne que sur le cycle
principal** — un cycle de correction n'a pas de fichier produit, il n'y
a rien à confronter *(D23)*.

### Les décisions produit prises pendant le codage

🔴 **Le trou** : une question produit tranchée pendant le codage entre
dans une **fiche**, jamais dans le fichier produit ni dans le global.
⚠️ **Le global décrirait donc une application dont un comportement a été
décidé dans un fichier de blocage.** 📌 **Et c'est sur un cycle de
correction que ça compte le plus : il n'a aucun autre chemin vers le
produit.**

📌 **La source existe** : les `blocked_<agent>-NN.md`, conservés depuis
D17. **`/9_controle` les a déjà en main pour le registre.**

🔴 **Elle rend un fichier de décisions par cycle.**

### Comment ils rejoignent le produit

🔴 **`/fusion` invoque le Rédacteur, puis le Fusionneur** — **tout à la
fin, une fois tous les cycles de correction passés.** 📌 **Si un second
bugfix revient sur ce qu'un premier avait décidé, c'est la version
finale qui entre** — on ne consigne pas un état intermédiaire.

| | |
|---|---|
| **Le Rédacteur** | 🆕 **Une invocation de plus** : il lit `desc-produit.md` **et les N fichiers de décisions, dans l'ordre des cycles** — 🔴 **le fichier produit d'abord, puis bugfix-01, puis bugfix-02, chacun amendant l'état obtenu.** 📌 **Une seule invocation**, pour qu'il arbitre les contradictions entre cycles |
| **Ce qu'il écrit** | 🔴 **`desc-produit-fusion.md`** — une copie enrichie, **sans aucun marqueur**, dont le seul lecteur est le Fusionneur |
| **Le Fusionneur** | 📌 **Lit `desc-produit-fusion.md`** au lieu de `desc-produit.md`. **Une ligne dans son fichier** |

**Ce que le fichier séparé règle :** 🔴 **`desc-produit.md` n'est pas
modifié après le découpage** — ⚠️ **aucune exception à écrire dans
`/6_convertit`** · 📌 **aucun marqueur, par construction** · 📌
**l'historique reste lisible** : ce que l'amont a fermé, et ce qui a été
décidé après · 🔴 **et un cycle relancé sur cette fonctionnalité repart
d'un fichier intact.**

⚠️ **Aucune décision à intégrer ?** 🔴 **Le Rédacteur écrit quand même
le fichier, copie conforme** — 📌 **sinon le Fusionneur devrait choisir
sa source, et un agent qui choisit est un agent qui peut se tromper.**

📌 **Placement** : dans 99 % des cas la décision complète un bloc
existant — 🔴 **c'est le travail ordinaire de l'invocation 2 du
Rédacteur**, qui sait charger le bloc qui convient et en créer un quand
aucun titre ne couvre le sujet.

### Ce qu'on ne fait pas

- 🔴 **Aucun ajout automatique à la grille** — 📌 **le Product Owner
  perdrait le contrôle du process**
- 🔴 **L'Arbitre n'écrit rien de plus** : il ne lit ni le fichier
  produit ni les grilles, donc il ne peut pas nommer la classe
  manquante. 📌 **Le registre est un tas de cas, pas une analyse — et
  c'est suffisant**

### Les trois dépendances

- ✅ **D17 — corrigé.** 📌 **Les cinq agents (Contrôleur, Détailleur,
  Réalisateur, Relecteur, Vérificateur) disaient « supprime le fichier
  une fois appliqué »** alors que le PROCESS et le Cadreur disent
  « renomme, jamais supprime ». **Ils renomment désormais en
  `blocked_<agent>-NN.md`** — 🔴 **la source de l'Arbitre existe au
  moment de la collecte**
- ✅ **D20 — le verdict avait tort, et un vrai défaut était à côté.**
  📌 **`/8_code` n'invoque pas le Contrôleur et le dit en tête** ;
  ⚠️ **mais sa section *Where to resume* disait « va droit au
  Contrôleur » — elle se contredisait elle-même.** 🔴 **Corrigé** :
  elle s'arrête et annonce `/9_controle`
- **A4** — la recette manuelle est rendue par la même commande

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/commands/9_controle.md` | 🔴 **Ramasse le registre** : les *doutes* et *intentions manquantes* du Contrôleur, et les questions produit rendues par l'Arbitre. 📌 **Elle ramasse, elle ne conclut pas.** 🔴 **Rend aussi le fichier de décisions produit du cycle.** 📌 **Tourne sur le cycle principal et sur chaque bugfix ; le Contrôleur seulement sur le principal** |
| `.claude/agents/redacteur.md` | 🆕 **Une invocation de plus** : `desc-produit.md` + les N fichiers de décisions, dans l'ordre des cycles → **`desc-produit-fusion.md`**, sans marqueur. 📌 **Écrit même si aucune décision** |
| `.claude/agents/fusionneur.md` | 📌 **Lit `desc-produit-fusion.md`** au lieu de `desc-produit.md` |
| `.claude/commands/fusion*.md` | 🔴 **Invoque le Rédacteur, puis le Fusionneur** — tout à la fin, après tous les cycles de correction |
| `.claude/agents/arbitre.md` | 📌 **Rien** — il ne lit ni le produit ni les grilles, il ne peut pas nommer la classe manquante |
| `docs/process/PROCESS_AVAL.md` | Le registre, les décisions produit, et le périmètre fermé de la commande |

✅ **D17 et D20, ses deux dépendances, sont déjà corrigés dans la
chaîne.**

---

## A6 · Les questions à deux niveaux
**Statut : tranché. 🔴 Le *comment* reste à écrire.**
*(D'où vient l'idée : le Prober de `proposition.md`, et sa réponse au
coût de fermeture du produit.)*

### Le principe

🔴 **Trois cas, là où la chaîne n'en connaît que deux :**

| Ce que dit le corpus | Aujourd'hui | Demain |
|---|---|---|
| Il répond directement | 📌 **Aucune question** | Inchangé |
| Rien n'y répond | Une question | Une question **obligatoire** |
| 🔴 **Il n'y répond pas ici, mais une règle transverse ou un motif déjà suivi donne la réponse** | Une question, au même titre | 🔴 **Une question *défaut*** |

⚠️ **Le volume ne monte pas** — 📌 **il se répartit.** Une question déjà
réglée n'est toujours pas posée.

**Le cas type** : un écran affiche une durée ; la grille demande ce
qu'il montre quand elle est absente ; §13.1 dit « une absence s'affiche
par un tiret » sans nommer cet écran. 📌 **Aujourd'hui c'est une
question de plus, à laquelle le Product Owner répond pour la quinzième
fois.**

### La forme

🔴 **Une question *défaut* porte sa réponse pré-remplie et la référence
du paragraphe qui la fonde.** *(Condition posée par le Product
Owner.)*

📌 **Le silence vaut acceptation** — il n'écrit que là où la proposition
est fausse.

### Le risque, nommé

⚠️ **C5 a mesuré qu'un agent qui doit remplir remplit** — 🔴 **31
problèmes sur 40 fermés à tort.** 📌 **Un défaut est une case remplie
par l'agent** : le risque est le même, déplacé.

🔴 **Ce qui l'en distingue** : la réponse porte **sa citation**, et le
Product Owner la voit passer. ⚠️ **Le contrôle n'est plus un
formulaire, c'est lui** — 📌 **et il ouvre tous les fichiers de
questions.**

📌 **`proposition.md` en fait sa propre incertitude n°1** : si le
Product Owner survole, la garantie est tenue formellement et brisée en
pratique. **Ce qui la règlerait :** compter, sur plusieurs
fonctionnalités, les corrections demandées après l'émulateur dont la
cause est un défaut accepté. 🔴 **Si ce n'est pas proche de zéro, le
niveau *défaut* se restreint aux seules citations de règles
transverses**, et les motifs « que le fichier suit déjà » cessent de
compter.

**Rebouclage :** 🔴 **A7** — une règle transverse est la principale
source d'un défaut ; encore faut-il savoir laquelle concerne quel bloc.

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md` | 🔴 **La notion de niveau** : *obligatoire* et *défaut* |
| `.claude/agents/sondeur.md` | Écrit un défaut avec **sa réponse pré-remplie et la référence du paragraphe qui la fonde** |
| `.claude/agents/redacteur.md` | 🔴 **Un défaut sans réponse écrite vaut acceptation** — il intègre la proposition |
| `docs/process/PROCESS_AMONT.md` | Les trois cas, le risque hérité de C5, et la mesure qui restreindrait le niveau *défaut* |

---

## A7 · Les règles transverses
**Statut : tranché** — la définition, le rapprochement, le passage au
code, le changement d'une règle, les divergences, et le doute sur le
périmètre. 📌 **Reste l'écriture.**
*(Condition d'A6 : une règle transverse est la principale source d'un
défaut. Genre `transverse` d'A1.)*

### Le problème

📌 **Une règle transverse est écrite une fois et vaut pour beaucoup de
blocs.** 🔴 **Il faut savoir lesquels** :

| | |
|---|---|
| **Trop large** | Un défaut est proposé là où la règle ne s'applique pas — ⚠️ **le risque de C5 revient** |
| **Trop étroit** | La question est reposée, et **le bénéfice d'A6 disparaît** |

### La forme retenue

🔴 **Ce n'est pas au bloc de savoir quelle règle le concerne — c'est à
la règle de dire à quoi elle s'applique.**

📌 **Une règle transverse porte déjà son périmètre dans sa
formulation** : *« toute valeur absente s'affiche par un tiret »* dit
« toute valeur absente ». ⚠️ **Rien à deviner : il suffit de la lire.**

🔴 **Le rapprochement se fait au moment de la question**, par le
Sondeur, qui a le bloc et les règles transverses sous les yeux.

**Ce qu'il faut, et rien de plus :**

1. 📌 **Les règles transverses identifiables** — le genre `transverse`
   (A1)
2. 📌 **Le Sondeur les a dans son contexte**, en plus de son bloc
3. 🔴 **Aucune table de correspondance, aucun marquage bloc par bloc**

### Écarté

**Par nature** — *§13.1 vaut pour tous les blocs `presentation`.*
🔴 **Mécanique et vérifiable, mais trop large** : « une absence
s'affiche par un tiret » ne concerne pas tous les blocs de
présentation, seulement ceux qui affichent une valeur qui peut manquer.

### Coût et risque

📌 **Coût** : les règles transverses chargées par chaque invocation, à
chaque tour — de l'ordre de cent à deux cents lignes. ⚠️ **Modeste, et
ça remplace une table qu'il aurait fallu construire et tenir à jour.**

⚠️ **Risque** : le rapprochement est un jugement. 🔴 **Contenu par la
citation** — le Product Owner voit sur quoi le défaut s'appuie.

### Ce qu'est une règle transverse — tranché

🔴 **Son sujet est une catégorie, pas un objet du produit.**

📌 **Le test, en une question** : la règle peut-elle nommer le bloc
qu'elle concerne ? **Oui → elle appartient à ce bloc. Non, parce
qu'elle en concerne une catégorie entière → transverse.**

| | |
|---|---|
| « Une absence s'affiche par un tiret » | Sujet : *une absence* — **transverse** |
| « Un repli n'est pas une erreur » | Sujet : *un repli* — **transverse** |
| « L'horloge ne se replie jamais » | Sujet : *l'horloge*, un objet — 🔴 **pas transverse** |

⚠️ **Une section transverse du fichier d'idées ne contient pas que des
règles transverses** — le §13.1 mélange les deux.

**Ce qui rend le test applicable :** 📌 **c'est une question fermée**
— *nomme-t-elle un objet du produit ?* — **plus facile que « vaut-elle
pour plusieurs blocs ? »**, qui demande de compter.

🔴 **Et le doute penche vers « pas transverse ».** ⚠️ **Les deux
erreurs ne coûtent pas la même chose** : mal classée en bloc, une règle
coûte une question de trop ; mal classée en transverse, **elle ferme à
tort**. 📌 **L'agent doit le savoir.**

### Comment une règle transverse devient du code — tranché

🔴 **Elle ne descend pas en lot. Elle se scinde en deux, et c'est le
Convertisseur qui le fait** — 📌 **il sait déjà** : *« une règle
transverse contraint sans rien produire ; le test est : si personne ne
l'écrit, est-ce que le code manque quelque chose ? Oui → c'est une
entrée numérotée, pas une ligne de préambule »*.

| Ce que la règle donne | Où ça va |
|---|---|
| **Le morceau de code partagé** — un formateur : une fonction qui prend une valeur absente et rend ce qu'il faut afficher | 🔴 **Une entrée numérotée** — sans elle, le code manque quelque chose |
| **La contrainte « tout bloc soumis à ça l'applique »** | 📌 **Le préambule** — elle contraint les autres entrées sans rien produire |

🔴 **Le Détailleur lit le préambule et écrit le critère** sur chaque lot
concerné. ⚠️ **Même avec le formateur écrit, quelqu'un doit décider que
*cet écran-là* l'appelle.**

**Un lot dédié pour le formateur, jamais codé au premier besoin** —
📌 **la structure l'impose déjà et le permet, vérifié :**

- 🔴 *« deux lots ne touchent jamais le même symbole »* — le coder dans
  le lot du premier écran ferait que les suivants le modifient
- 📌 **`Needs:` / `Produces:`** — le Vérificateur en dérive l'ordre, le
  formateur avant ses appelants. ⚠️ **Codé au premier besoin, l'ordre
  dépendrait de quel écran arrive en premier** — 🔴 **la
  reproductibilité tombe**
- 📌 **Un formateur a des entrées et une sortie** : c'est ce qui se
  teste le mieux

📌 **Même motif que la *pièce*** du Cadreur, déjà résolu : un lot à
part, jamais replié dans celui qui l'utilise.

⚠️ **La forme du code est une décision technique** — 🔴 **le genre
`transverse` ne la décide pas.** Il dit seulement : *cette règle
contraint plusieurs blocs.*

### Les deux vérifications — faites

✅ **Le Détailleur lit le préambule — *« toujours, quel que soit ton
bloc »*.** 📌 **Le chemin existe** pour qu'une contrainte transverse
atteigne les critères d'acceptation.

✅ **Le Convertisseur a la mécanique.** 📌 **Chaque invocation de nature
écrit une section `## Preamble` dans ses notes** — *« ce que tes blocs
donnent au préambule : une règle transverse »* — **et la transversale
les assemble sans rien déduire.** 🔴 **Le test de partage est déjà
écrit** : *si personne ne l'écrit, le code manque-t-il quelque chose ?*

### 🔴 Mais le partage d'A1 casse ce chemin

⚠️ **Ça ne marche aujourd'hui que parce qu'une règle transverse est un
bloc comme les autres**, rangé sous une nature, donc lu par une
invocation. 🔴 **Avec le partage, elle quitte le fichier des
comportements — et plus aucune invocation de nature ne la reçoit.**

📌 **Le même problème vaut pour deux autres genres.** **Ce que le
partage doit garantir :**

| Le fichier | Va à |
|---|---|
| Les transverses | 🔴 **Toutes les invocations de nature** — elles en tirent leurs entrées *(le formateur)* et leurs lignes de préambule |
| Les références | L'invocation transversale — section Text |
| Le hors-périmètre | L'invocation transversale — préambule |

### Quand une règle transverse change — tranché

**Pendant la boucle de la grille** — ⚠️ **une réponse modifie la règle,
le Rédacteur la marque `MODIFIED` ; les blocs qui l'appliquent, eux, ne
sont pas marqués.** 🔴 **Ils ne sont donc pas resondés, et les défauts
proposés d'après l'ancienne version restent acquis** — 📌 **un bloc
fermé sur une règle qui n'existe plus.** ⚠️ **Même famille que D3** : le
marquage suit ce qui a été édité, pas ce qui a été invalidé.

🔴 **Décision : une règle transverse modifiée remarque tous les blocs.**
📌 **Brutal mais mécaniquement juste** — ⚠️ **l'alternative produit
exactement le défaut silencieux qu'on évite partout ailleurs.**

📌 **Pourquoi pas une trace du rapprochement** : ce serait la table de
correspondance qu'on a écartée. 🔴 **Et le cas devrait être rare** —
une règle transverse est écrite une fois et change peu.

**Après le découpage** — 📌 **la chaîne a déjà sa réponse** :
`/6_convertit` s'arrête si `code/decoupage.md` existe. **Un changement
du produit après le découpage appartient à un nouveau cycle.**

### Deux règles qui divergent — tranché

⚠️ **La contradiction n'existe pas dans le fichier des transverses** —
🔴 **elle n'apparaît que sur un bloc où les deux s'appliquent.** 📌 **La
passe B ne peut donc pas l'attraper** : elle croise des blocs, pas des
règles.

🔴 **C'est au moment du rapprochement, par le Sondeur** — 📌 **il a le
bloc et toutes les règles transverses sous les yeux, et il est déjà en
train de faire ce travail.**

| Le cas | Ce qu'il fait |
|---|---|
| **Transverse contre transverse** | 🔴 **Une question obligatoire, jamais un défaut** |
| **Transverse contre une règle du bloc** | 📌 **Le bloc l'emporte** — il est plus précis. ⚠️ **Ce n'est pas une contradiction, c'est une exception** — aucun défaut à proposer |

📌 **Le second cas est sans doute le plus fréquent** — *« l'horloge ne
se replie jamais »* est une règle du bloc de l'horloge, pas une règle
transverse.

### Quand la formulation ne dit pas le périmètre — tranché

⚠️ **La formulation n'est pas uniforme** — 📌 *« toute valeur absente »*
dit son périmètre, **d'autres règles non.**

🔴 **L'agent qui pose le genre a deux sorties de doute, et elles ne se
confondent pas :**

| Le doute | Ce qu'il fait |
|---|---|
| **« Est-ce transverse ? »** — la règle nomme-t-elle un objet du produit ? | 📌 **L'asymétrie s'applique** : dans le doute, `comportement` |
| **« À quoi s'applique-t-elle ? »** — elle est bien transverse, mais sa formulation ne dit pas assez son périmètre | 🔴 **Une question obligatoire au Product Owner** |

⚠️ **Le second ne se règle pas par l'asymétrie** — 📌 **la classer en
`comportement` ne résout rien** : elle n'a toujours pas de déclencheur.

📌 **La réponse ne modifie pas le produit, elle reformule la règle** —
*« le repli s'applique partout »* devient *« toute valeur qu'un capteur
ne fournit pas s'affiche en repli »*. **Même comportement, portée dite.**

📌 **La question suit la route habituelle** — réponse, `/1_lexique`,
`/2_structure`, et le Rédacteur réécrit la règle. ⚠️ **Elle est posée
avant le Classeur et avant les Sondeurs.**

---

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/sondeur.md` | 🔴 **Charge les règles transverses en contexte**, en plus de son bloc. **Le rapprochement se fait au moment de la question** |
| `.claude/agents/sondeur.md` | **Deux transverses qui divergent sur un bloc → une question obligatoire, jamais un défaut.** 📌 **Transverse contre règle du bloc → le bloc l'emporte**, aucun défaut |
| 🆕 **L'agent du genre** | 🔴 **Le test** : la règle nomme-t-elle un objet du produit ? Oui → pas transverse. **Dans le doute, pas transverse** |
| `.claude/agents/convertisseur.md` | 🔴 **Une règle transverse se scinde** : le morceau de code partagé devient **une entrée numérotée**, la contrainte va **au préambule** |
| `.claude/agents/redacteur.md` | 🔴 **Une transverse modifiée remarque tous les blocs** |
| ✅ `.claude/agents/detailleur.md` | **Rien** — il lit déjà le préambule, *« toujours, quel que soit ton bloc »* |
| ✅ `.claude/agents/cadreur.md` · `verificateur.md` | **Rien** — 📌 **le lot dédié du formateur marche avec les règles existantes** : *« deux lots ne touchent jamais le même symbole »*, `Needs:` / `Produces:` pour l'ordre. **Même motif que la *pièce***|

---

# C — Écartés pour l'instant

## C4 · Le découpage du fichier d'idées en unités
**Écarté** — 📌 187 blocs, 955 lignes, aucune troncature ; et
l'invocation 2 du Rédacteur cible déjà (grep, chargement par plage,
édition sur place), c'est-à-dire la règle même que la proposition
défend. 🔴 **Rouvert si** une troncature est observée.
⚠️ **La prémisse tient ailleurs, en deux endroits distincts** *(P13)* :
🔴 **le Rédacteur, en écriture** — 300 blocs dans une invocation — **et
l'invocation globale du Sondeur, en lecture** — elle relève tous les
blocs à chaque tour et ne peut pas cibler. 📌 **Ce ne sont pas les mêmes
limites, et rien ne dit laquelle viendra en premier.**

## C1 · Pas de document technique global
**Écarté** — 🔴 **il le retire lui-même** dans `verdict.md` §3 : « je
considère mon §7.5 répondu par un système qui fonctionne ». Notre
`spec-technique.md` est jugé bien utilisé (inventaire du Cadreur,
graphe `Consumes`, une section par couche).

## C3 · Le contrôle de perte entre `idees.md` et `desc-produit.md`
*(le Coverage de `proposition.md`)*
**Écarté** — 🔴 aucun bug observé ne vient d'une perte au Rédacteur
(ils viennent de fermetures incomplètes et de pertes en aval), **et
c'est un filet**. 📌 Ce qui plaidait pour : le Rédacteur est le seul
producteur dont la sortie n'est comparée à son entrée par aucun
contexte séparé. 🔴 **Rouvert si** un bug se révèle être une phrase
d'`idees.md` qui n'a produit aucun bloc.

## C5 · Le relevé par classe — une case par question de la grille
*(le Prober de `proposition.md`)*
**Écarté — 🔴 mesuré, et le résultat est l'inverse de l'intention.**

📌 **Essayé** : l'agent devait écrire sa réponse à chaque question,
même trouvée dans le document — ≈ 1 000 lignes à remplir.

🔴 **Résultat : il a rempli au lieu de chercher.** 5 % de « non
répondu » contre 29 % sans formulaire ; **31 problèmes sur 40 fermés à
tort**. Vrais problèmes trouvés : **42** avec le relevé, **68** sans,
**140** avec trois angles en parallèle.

⚠️ **La leçon dépasse le Sondeur** : 🔴 **exiger d'un modèle une trace
exhaustive transforme la recherche en remplissage.** 📌 **Ce qui
vérifie, ce n'est pas un formulaire — c'est que trois lecteurs
différents ne ratent pas les mêmes choses.**

📌 **Distinction qui tient** : les relevés que la chaîne garde
(`couverture.md`, `tracabilite.md`, le rapport du Contrôleur)
enregistrent ce qui a été **produit**, pas ce qui a été **cherché**.

## C2 · Les lots coupés par comportement, pas par couche
*(rupture 2 et P2 du verdict : aucun comportement n'est prouvé de bout
en bout avant l'émulateur)*
**Écarté — 🔴 l'alternative a été essayée, et le découpage par couche
gagne.**

📌 **Essayé** : un tout premier agent codait une fonctionnalité
entière, toutes couches en une passe. 🔴 **Moins efficace** — un agent
qui traverse trois couches doit tenir trois jeux de conventions, trois
façons de nommer, et décider où placer chaque chose ; un agent qui code
une couche a une tâche bornée. 📌 **Et ça correspond à la façon dont on
développe réellement.**

⚠️ **`proposition.md` écarte le découpage par couche en une phrase,
sans l'avoir essayé** — 🔴 **le verdict ne renverserait pas notre choix
non plus** : les huit natures achètent le balayage exhaustif, le
Convertisseur par nature, le reclassement par grep, « une section par
lot ».

**Ce qui reste vrai du diagnostic** : 📌 **le premier moment où un
comportement s'exécute entièrement, c'est sur l'appareil.** ⚠️ **Ce
n'est pas un défaut du découpage, c'est sa conséquence** — 🔴 **et elle
a deux remèdes qui n'y touchent pas : A3** (des tests qui affirment
vraiment quelque chose, couche par couche) **et A4** (une recette
dirigée).

📌 **Ce que la chaîne oppose déjà** : le Cadreur traite la *pièce*
comme un lot à part, jamais repliée dans celui qui déclare le
contrat — *« un contrat sans rien derrière compile, passe ses tests, et
ne fait rien »* — et se demande, sur chaque production, ce qui doit
l'appeler.

# R — Les six ruptures du verdict (section 1)

| # | La rupture | État |
|---|---|---|
| 1 | Le fichier d'idées n'est plus jamais relu | **Écarté — C3** |
| 2 | Les lots coupés par couche | **Écarté — C2** |
| 3 | Deux boucles autonomes sans plafond | ⚠️ **Rupture 3 écartée, mais A-6 la rouvre et la tranche** |
| 4 | La grille n'apprend pas | **Tranché — A5** |
| 5 | Les conventions redérivées sans lire ce qui existe | **Tranché — Rupture 5** |
| 6 | Chaque réponse rejoue toute la route | **Clos — Rupture 6** |

## Rupture 3 · Les boucles sans plafond
**Écarté — 🔴 aucune n'est autonome, et c'est déjà ce qui se passe.**

📌 **Le redécoupage passe par le Product Owner à chaque tour** — il
relance `/7_lots`, puis `/8_code`. ⚠️ **Ce n'est pas « un run qui finit
quand la personne le remarque »** : elle le remarque forcément.

📌 **Et le Cadreur a déjà son mécanisme de convergence** — il lit les
redécoupages précédents pour *ce qui revient*, écrit *ce qu'il en
fait*, et **signale au Product Owner dès le troisième retour**. 🔴 **Son
fichier nomme le risque lui-même** : *« sans ça, tu coupes à nouveau
autour du même point, et le cinquième redécoupage dit ce que le
deuxième disait déjà »*.

🔴 **Aucun cas de boucle emballée observé** — critère n°3.

⚠️ **Mais cet écart était partiellement faux, et la section U le
corrige :** 🔴 **A-6, le redécoupage, ne passe pas par le Product
Owner** — *« il n'attend sur rien »* pendant `/8_code`. **Tranché en
A-6** : arrêt au troisième. 📌 **Et la seconde boucle — Cadreur plus
demande de convention — est tranchée en U11** : un refus de l'Architecte
arrête la commande.

## Rupture 5 · Les conventions redérivées sans lire ce qui existe
**Statut : tranché. 🔴 Reste l'écriture.**

### Le défaut, vérifié

📌 **`/conventions` tourne après `/6_convertit`, donc une fois par
fonctionnalité.** 🔴 **Sa table dit : ni requête, ni questions
répondues → invocation 1** — et l'invocation 1 s'interdit d'ouvrir tout
fichier de conventions, *« y compris celui qu'une exécution antérieure
de toi-même a laissé »*.

🔴 **À la fonctionnalité N+1, elle redérive tout sans lire ce qui y
est** — ⚠️ **toutes les règles que l'invocation 3 a ajoutées lot après
lot pendant la fonctionnalité N sont perdues.** 📌 **C'est le défaut que
l'Architecte existe pour empêcher**, déplacé du lot à la
fonctionnalité.

**Sa justification ne tient qu'à moitié** — *« relire serait dériver de
sa propre sortie »* : ✅ **juste pour une première dérivation** ;
❌ **faux ensuite**, car les règles de l'invocation 3 ne sont pas sa
sortie libre, **ce sont des demandes tranchées, venues de lots réels.**

### Ce qu'on modifie

🔴 **Trois choses, et rien d'autre :**

| | |
|---|---|
| **`/conventions`** | 📌 **Teste l'existence de `TECHNICAL_CONVENTIONS.md`** — ⚠️ **en dernière ligne de sa table**, à la place de *« rien de tout ça »* : sinon elle passerait devant une requête ou des questions à intégrer |
| **Une invocation de plus** | 📌 **Les conventions existent : elle les lit, balaie la grille, et n'ajoute que ce que le fichier ne couvre pas** |
| **L'interdit de lecture** | 🔴 **Restreint à l'invocation 1** |

📌 **Le reste ne bouge pas** — première dérivation inchangée, mécanisme
des demandes par l'Arbitre inchangé.

**`couverture.md`** : 📌 **la nouvelle invocation en produit une pour sa
seule fonctionnalité.** 🔴 **Elle sert à vérifier qu'aucune entrée n'a
échappé au balayage** — c'est suffisant.

### Compléter ou remplacer — la distinction qui compte

| Le cas | Ce qui se passe |
|---|---|
| **Compléter** — la règle ne couvrait pas ce que la fonctionnalité apporte | ✅ **Automatique, sans question.** 📌 **Le code existant reste conforme** : il ne connaissait pas ce cas |
| **Remplacer** — l'ancienne disait X, la nouvelle dit Y | 🔴 **Signalé au Product Owner, jamais fait seul** |

⚠️ **Pourquoi remplacer ne peut pas être automatique** : **tout le code
déjà écrit suit X.** 📌 **Le Relecteur ne relit que le lot en cours**,
les fiches déjà écrites nomment l'ancienne règle, et **le code neuf
suivrait Y pendant que l'ancien suit X** — 🔴 **l'incohérence même que
l'Architecte existe pour empêcher.**

📌 **Ce qu'il signale** : la règle en place, ce que la fonctionnalité
exige, et ce qui a été codé sous l'ancienne. 🔴 **La décision appartient
au Product Owner** — reprendre le code ancien coûte du temps, le
laisser divergent coûte de la cohérence.

⚠️ **Fréquence inconnue** — 📌 **une convention est une règle de projet,
une nouvelle fonctionnalité devrait rarement la contredire.** 🔴 **On
observe, et on traitera autrement si le cas revient souvent.**
*(Décision du Product Owner.)*

**Rebouclage :** ⚠️ **D16 du verdict** — le même défaut à l'échelle du
lot : le lot qui demande une convention est codé sous l'ancienne règle,
et la divergence n'est consignée nulle part.

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/commands/conventions.md` | 🔴 **Teste l'existence de `TECHNICAL_CONVENTIONS.md`** — ⚠️ **en dernière ligne de sa table**, jamais avant une requête ou des questions à intégrer |
| `.claude/agents/architecte.md` | 🆕 **Une invocation de plus** : les conventions existent, elle les lit, balaie la grille, **n'ajoute que ce que le fichier ne couvre pas**. 🔴 **L'interdit de lecture est restreint à l'invocation 1.** 📌 **`couverture.md` pour la seule fonctionnalité.** 🔴 **Compléter : automatique. Remplacer : signalé au Product Owner** |
| `docs/process/PROCESS_AMONT.md` | La dérivation incrémentale, et la distinction compléter / remplacer |

---

## Rupture 6 · Chaque réponse rejoue toute la route
**Clos — 🔴 trois coûts distincts, deux traités, un laissé ouvert avec
sa condition.**

**1. Six commandes par fichier de réponses** — 📌 **c'est le prix de la
règle « une phase par exécution, jamais deux agents enchaînés »**, et
elle rend chaque arrêt visible. 🔴 **`/cycle` existe pour ça** —
⚠️ **pas encore utilisée : le process n'est pas stabilisé.**
*(Product Owner.)*

**2. Le nombre de tours** — 📌 **le vrai coût, parce que chaque tour
demande une réponse.** ✅ **A6 s'y attaque directement** : une question
réglée par une règle transverse devient un défaut, donc rien à écrire.
🔴 **Moins de questions, donc moins de tours** — une réponse crée
elle-même de nouvelles questions.

**3. Le travail refait à chaque tour** — 📌 **les trois angles sont déjà
ciblés sur les blocs marqués.** 🔴 **La passe globale ne l'est pas** :
elle relève tous les blocs à chaque tour, parce que la passe B a besoin
de tout croiser.

⚠️ **Le seul des trois sans remède.** 📌 **C5 a écarté le relevé
conservé** (mesuré : il détruit la qualité) ; **C4 l'a noté comme le
point où la taille cassera.** 🔴 **À 187 blocs ça passe ; c'est
l'invocation la plus lourde de la chaîne, répétée à chaque tour.**

📌 **Une piste, qui rouvre C5** : ne recroiser que les colonnes
touchées — ⚠️ **mais il faudrait conserver le relevé précédent pour les
comparer.**

🔴 **Laissé ouvert avec sa condition** : **le jour où la passe globale
tronque ou devient trop lente**, on y revient avec un cas.

---

### Ce que ça change

📌 **Rien dans les fichiers.** 🔴 **`/cycle` existe pour le premier
coût** — ⚠️ **pas encore utilisée : le process n'est pas stabilisé.**
📌 **Le troisième coût — la passe globale qui relève tout à chaque
tour — reste ouvert** avec sa condition : *le jour où elle tronque ou
devient trop lente.*

---

# F — Les rôles manquants du verdict (section 3)

| Le rôle | Verdict | Où on en est |
|---|---|---|
| **Coverage** — prose contre blocs | Un trou | **Écarté — C3** |
| **Mapper** — unités et renvois | Choix justifié | **Confirmé** — seul le genre est retenu, A1 |
| **Locator** — nouveau/conservé/modifié | À moitié justifié | **Traité — A2** |
| **Tester avant le Coder** | Pas pleinement convaincant | **Retenu — A3** |
| **Recette manuelle** | Un trou | **Tranché — A4** |
| **Registre qui nourrit la grille** | Un trou | **Tranché — A5** |
| **Reviewer pour l'invention** | Un trou, petit | **F1 — renversé, il reste** |
| **Conventions tirées du code** | Un trou | **Écarté — F2** |
| **Driver sans jugement** | Justifié, avec un coût | **Écarté — F3** |
| **Document technique global** | Il le retire lui-même | **Écarté — C1** |

## F1 · Le Relecteur
🔴 **RENVERSÉ — il ne saute pas.** ⚠️ **La décision de le supprimer
reposait sur une lecture incomplète de sa checklist, de mon fait.**

📌 **Ses cinq points, relus dans son fichier :**

| | |
|---|---|
| **1** | Les symboles correspondent à ce que la fiche promettait, **signature comprise** |
| **2** | Un test par critère, **apparié sur ce que le test affirme, pas sur son nom** |
| **3** | Les conventions que la fiche nomme, **celles qu'un grep tranche** |
| **4** | Les champs du rapport — la compilation du module, **et `## Outside the lot`** : chaque fichier touché que la fiche ne déclare pas, **vérifié contre le diff** |
| **5** | Rien de ce que le lot écrit n'est **inutilisé par le lot lui-même** — 🔴 **il lit le corps**, là où le point 1 ne lit que la signature |

🔴 **A3 ne reprend que le point 2 et une partie du 4.** 📌 **Les points
1, 3 et 5 restent sans personne d'autre.**

⚠️ **Le trou de l'invention est plus étroit qu'annoncé** : 📌 **le point
5 attrape le code mort du lot** — 🔴 **mais il exclut explicitement *« ce
que rien n'utilise »***, un autre lot pouvant y accéder. **Ce qui
échappe : du code qui fait plus que le critère et qui sert.**

⚠️ **Conséquence sur le coût d'A3** : 🔴 **deux chargements de plus par
lot, pas un** — de l'ordre de **+60 %** et non +30 %. 📌 **Accepté par
le Product Owner**, à mesurer au premier cycle.

## F2 · Les conventions tirées du code
**Écarté — 🔴 le mécanisme actuel est meilleur, et c'est un choix
délibéré.**

📌 **L'Arbitre cherche dans le code comment le problème a été résolu
ailleurs, et remonte l'information à l'Architecte, qui écrit la
règle.** 🔴 **L'Architecte décide, l'Arbitre observe.**

⚠️ **Le verdict dit « lues par le mauvais agent »** — 🔴 **c'est au
contraire la bonne séparation** : un agent qui lirait du code pour en
déduire un style **hériterait de ce style, y compris de ce qu'il a de
mauvais.** 📌 **Ce qui remonte, ce sont des cas concrets ; l'Architecte
en tire une règle.**

📌 **Reste vrai, mais sans objet ici** : le mécanisme ne s'enclenche
qu'à partir du moment où un lot bute — ⚠️ **sur une application
existante reprise, les conventions s'écrivent sans connaître le style
en place.** 🔴 **Ce cas ne se présente pas** : les projets partent de
zéro et le global naît du Fusionneur.

## F3 · Le sondage de vingt minutes de l'Arbitre
**Écarté — 🔴 le verdict a compté le coût sans compter le gain.**

📌 **Mécanisme mis en place par le Product Owner, délibérément.**
🔴 **Sur une session de jour, il répond vite, et le Détailleur ou le
Réalisateur reprend avec tout son contexte** — ⚠️ **sans le sondage, il
faudrait un agent frais qui recharge tout et refait le chemin.**

📌 **Le coût réel est faible** : l'agent attend, il ne consomme rien.
**De nuit, vingt minutes de temps de mur sur un cycle qui dure des
heures.**

⚠️ **Le verdict y voit une incohérence** — *« la chaîne suppose la
personne hors session, le sondage suppose le contraire »* — 🔴 **alors
que c'est une chaîne qui s'adapte aux deux cas.** 📌 **Son estimation
« le sondage ne l'attrape presque jamais » est marquée *(estimate)* :
une supposition, pas une mesure.**

---

# U — Les boucles du verdict (section 5)

| # | La boucle | État |
|---|---|---|
| U1 | Lexicographe, avant le fichier produit | **Écarté** — 📌 **la convergence est un chantier à part** *(`todo.md`)* |
| U2 | Lexicographe sur un fichier de réponses | ✅ **Saine** — test mécanique, bornée |
| U3 | Le signalement du Rédacteur | ✅ **Saine** — test vérifiable ; chaque tour passe par le Product Owner |
| U4 | La question du Classeur | ✅ **Saine** — test mécanique *(la commande compte)*. ⚠️ **N'existe pas encore** : décision d'A1 |
| U5 | Le tour de grille | **Écarté — U5** |
| U6 | Les questions du Convertisseur | ✅ **Réglée par D10** — deux routes ; test vérifiable par grep |
| U7 | La dérivation de l'Architecte | **Tranché — U7** |
| U8 | La fusion | ✅ **Saine** — bornée par construction, un tour |
| U9 | Le blocage d'un Sondeur | ✅ **Saine** — borne d'un tour, test vérifiable |
| U10 | L'Arbitre attend le Product Owner | **Tranché — U10** |
| U11 | Le Cadreur bloqué avec une demande de convention | **Tranché — U11** |
| U12 | Contrôleur → cycle de correction | ✅ **Réglée par D23** · ✅ **sa seconde sortie corrigée — U12** |
| U13 | Diagnostiqueur, un écart | ✅ **Saine** — bornée par la liste, l'invocation 2 compte |
| U14 | L'exécution de `/8_code` | **Écarté — U14** |
| A-1 | Cadreur ⇄ Vérificateur | ✅ **Vérifié dans `cadreur.md`** — *« trois tours au plus, que tu comptes »*, en tête de son fichier |
| A-2 | Réalisateur ⇄ analyse et tests | **Tranché — A-2** |
| A-3 | Réalisateur ⇄ Relecteur | ✅ **Vérifié dans `8_code.md`** — *« trois reprises au plus par lot, tous types de FAIL confondus »* |
| A-4 | Divergence → Détailleur | ✅ **Vérifié dans `8_code.md`** — le Détailleur réécrit les seules fiches que le verdict nomme, **puis elles sont codées comme n'importe quel lot** : bornées par A-3 |
| A-5 | Arbitre → Architecte | ✅ **Saine pour l'Arbitre** — un refus s'écrit dans le `## Verdict`, *« l'Arbitre est encore en cours et prend la suite »*. ⚠️ **Le cas du Cadreur est différent — voir U11** |
| A-6 | Le redécoupage | **Tranché — A-6** |
| A-7 | Extracteur | ⚠️ **Caduque** — l'agent est supprimé |
| A-8 | `/cycle` | 📌 **Périmée** — non utilisée tant que le process n'est pas stabilisé |

## U1 · La boucle du Lexicographe
**Écarté — 🔴 une borne couperait au mauvais endroit ; le vrai sujet est
la convergence.**

📌 **Test vérifiable** — un fichier écrit même vide. ⚠️ **Aucune
borne**, avec la raison : *un terme tranché peut révéler une paire.*

🔴 **Pourquoi pas de borne** : 📌 **la boucle passe par le Product Owner
à chaque tour** — il voit la courbe descendre. ⚠️ **Une borne
arbitraire fermerait le vocabulaire sur un trou** — arrêter au cinquième
tour d'une fonctionnalité qui en demande sept. 📌 **Et le vrai remède a
déjà été appliqué : la portée, pas le comptage** *(16, 9, 4, 4, 3)*.

🔴 **Le sujet réel est la convergence, et il est ouvert** — voir
`todo.md`, *la convergence du lexique*. ⚠️ **Un fichier vide ne prouve
pas que le vocabulaire est tranché** : il prouve que ce balayage-là n'a
rien trouvé.

## U5 · Le tour de grille
**Écarté — 🔴 « rien n'a changé » et « rien n'est ouvert » coïncident
ici.**

📌 **Le grief du verdict** : le test d'arrêt est *aucun bloc marqué*,
donc *rien n'a changé* — ⚠️ **et la passe globale ne tourne pas quand
aucun bloc n'a bougé.** 🔴 **La boucle pourrait se fermer sur un tour
où personne n'a rien regardé.**

🔴 **L'argument qui l'écarte** *(Product Owner)* : **si un tour n'a rien
trouvé, le tour suivant sur le même fichier ne trouverait rien non
plus.** ⚠️ **Le faire tourner serait payer un balayage pour confirmer un
résultat déjà connu** — 📌 **et s'il donnait un autre résultat, c'est un
problème de convergence, qu'un tour de plus ne résoudrait pas.**

📌 **La nuance qui manquait** : **aucun bloc marqué veut dire que le
Rédacteur n'a rien écrit** — 🔴 **le fichier est littéralement identique
à celui que le tour précédent a balayé.** **Il n'y a rien de nouveau à
regarder.**

✅ **Et A6 traite le résidu que le verdict nommait** : une réponse
confirmative n'aurait pas dû être une question — **c'est un défaut.**

## U7 · La dérivation de l'Architecte
**Tranché — 🔴 il manque la sortie quand une réponse ne suffit pas.**

📌 **Vérifié** : l'invocation 2 a **deux gestes** — lire le fichier
répondu, et *« transformer chaque réponse en règle »*. 🔴 **Rien ne dit
ce qu'elle fait si une réponse ne lui suffit pas.**

⚠️ **Elle doit produire une règle, donc elle en produira une** — sur une
réponse qui ne la fonde pas. 📌 **Le cas est plausible** : une réponse
produit qui ne tranche pas assez pour écrire une règle vérifiable —
🔴 **c'est le sens même de sa fermeture *Precision***.

**Le cas concret** : *« on affiche un message d'erreur »*. **Quel
message, où, sous quelle forme ?** ⚠️ **Aujourd'hui, soit elle invente,
soit elle écrit une règle vague.**

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/architecte.md` | 🔴 **Une réponse qui laisse le choix ouvert donne un nouveau fichier de questions, jamais vide** — 📌 **le même mécanisme que le Lexicographe**, qui existe déjà dans la chaîne |
| `.claude/commands/conventions.md` | 📌 **Son *What to run next*** : un nouveau fichier → répondre, puis `/conventions` |

📌 **Et c'est ce qui donne sa borne à U7** : 🔴 **la boucle s'arrête
quand l'invocation 2 n'écrit pas de nouveau fichier.** ⚠️ **Aujourd'hui
elle est réputée faire un tour, sans que ce soit dit.**

## U10 · Un lot qui soulève plusieurs manques
**Tranché — 🔴 optimiser quand c'est possible, jamais une contrainte.**

📌 **Le grief du verdict** : le sondage de vingt minutes est **borné
comme attente, non borné comme compte.** 🔴 **Rien ne limite combien de
manques un seul lot peut soulever, un par un** — chacun avec son arrêt
complet. ⚠️ **Distinct de F3**, qui justifie l'attente elle-même.

🔴 **Le principe, posé par le Product Owner** : **un arrêt reste un
arrêt, et plusieurs arrêts successifs sont légitimes quand le travail
l'impose.** 📌 **Mais c'est dommage de ne pas optimiser quand on peut.**

### Le Détailleur — grouper, avec les dépendances dites

📌 **Sa mécanique le permet déjà** : 🔴 *« tu n'as écrit aucune fiche à
ce stade — la marche vient avant les gestes »*. **Il parcourt tout son
bloc avant d'écrire**, donc il voit ses manques pendant cette marche.

🔴 **Il va au bout de son raisonnement, relève tout, et écrit un seul
fichier de blocage à plusieurs entrées.** 📌 **Chaque entrée porte son
manque et sa question** — ⚠️ **et, quand il le voit, ce dont elle
dépend** : *« celle-ci n'a de sens que si la précédente est tranchée
ainsi »*.

📌 **Le Product Owner répond à ce qui est pertinent et laisse vide le
reste.** **Un arrêt au lieu de cinq.**

### Le Réalisateur — avancer sur ce qui est indépendant

🔴 **Il bute, il regarde ce qui lui reste à faire, et il continue sur ce
qui ne dépend pas du manque.** 📌 **Il ne s'arrête que quand plus rien
n'est faisable.**

⚠️ **Deux points à border :** 📌 **ce qu'il a codé entre-temps est
conservé** — c'est déjà `reprise_realisateur.md`, du code qui compile et
commité. 🔴 **Et un second manque découvert en avançant s'ajoute au
fichier de blocage, il ne le remplace pas** — sinon on perd le premier,
ou on refait un tour.

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/detailleur.md` | 🔴 **Un fichier de blocage à plusieurs entrées**, écrit au bout de la marche. 📌 **Chaque entrée dit ce dont elle dépend, quand il le voit** |
| `.claude/agents/realisateur.md` | 🔴 **Sur un manque, il continue ce qui n'en dépend pas** et ne s'arrête que quand plus rien n'est faisable. 📌 **Un second manque s'ajoute au fichier, il ne le remplace pas** |

### Ce qui reste hors de portée

⚠️ **Deux manques réellement indépendants que le Réalisateur découvre à
deux moments éloignés** — 📌 **deux arrêts, et c'est irréductible.**

## U11 · Le Cadreur bloqué avec une demande de convention
**Tranché — 🔴 un refus n'est pas un blocage, et `/7_lots` ne le couvre
pas.**

📌 **Le chemin, vérifié** : le Cadreur écrit un blocage **et** une
demande, puis sort. `/7_lots` invoque l'Architecte, puis relance le
Cadreur.

🔴 **La frontière est délibérée et bien tenue** : `/7_lots` *« n'invoque
jamais l'Arbitre »* — ⚠️ **ce sur quoi le Cadreur et le Vérificateur
bloquent est mécanique**, et *« une convention se tranche là où les
conventions s'écrivent »*. 📌 **L'Arbitre le dit de son côté aussi**, et
prévoit même le cas où un tel blocage lui parviendrait par erreur.

⚠️ **Le trou** : 📌 **la commande s'arrête si l'Architecte *bloque***
— *« il demande une règle que personne n'a écrite »* — 🔴 **mais pas
s'il *refuse*.** **Un refus s'écrit dans le `## Verdict` de la demande,
l'Architecte sort normalement, et le Cadreur est relancé devant
exactement le même problème.** 📌 **Il ne contourne jamais une
convention : il rebloque à l'identique.**

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/commands/7_lots.md` | 🔴 **Lire le `## Verdict` de la demande après l'Architecte.** 📌 **Un refus est traité comme un blocage** — elle s'arrête et rend la main, avec la raison du refus et ce que l'Architecte dit qui trancherait |

📌 **Une ligne de plus dans une table qui existe déjà** — ⚠️ **aucune
frontière déplacée.** 🔴 **Et c'est le principe de la chaîne : un agent
qui ne peut pas produire ne réessaie pas, il rend la main.**

## U12 · La seconde sortie — un blocage sur un lot en PASS
✅ **Corrigé dans `/8_code` — une justification fausse retirée.**

📌 **Ce que disait la commande** : une décision remplie n'est pas un
arrêt, **y compris sur un lot qui porte déjà un PASS** — *« le
Contrôleur signale des intentions manquantes après que tous les lots
ont été relus, et un blocage est la façon dont elles reviennent »*.

🔴 **Aucun agent n'écrit ce blocage.** Le Contrôleur écrit un rapport ;
**rien ne transforme une intention manquante en `blocked_<agent>.md`
sur un lot précis.**

⚠️ **Et ça contredisait D23** : ce qui manque après le Contrôleur passe
par une `bug-list.md` et un cycle de correction — 📌 **plus explicite,
il repart du produit, et il ne rouvre pas un lot clos.**

✅ **La règle reste, la raison fausse part.** 📌 **Une décision remplie
sur un lot en PASS vient d'un blocage laissé en suspens**, pas du
Contrôleur — 🔴 **et la commande le dit maintenant.**

## U14 · Le décompte de `/8_code`
**Écarté — 🔴 `N` n'a jamais été une borne de boucle.**

📌 **`N` est le nombre de lots que le Product Owner demande à coder dans
cette exécution**, un par défaut. ⚠️ **C'est un paramètre, pas un
plafond.**

🔴 **Et la commande traite explicitement le cas** : *« ton compte de
lots continue aussi — il ne repart pas. `N` compte les lots relus PASS
dans cette exécution, et un redécoupage n'en a relu aucun. »*

📌 **C'est une décision, pas un oubli** : un redécoupage ne fait avancer
aucun lot, **donc il ne consomme pas le quota.** ⚠️ **Sans ça, demander
trois lots et tomber sur un redécoupage rendrait la main après un
seul.**

🔴 **Ce qui borne `/8_code`, c'est le Product Owner**, qui la relance.

⚠️ **Ce qui reste vrai se reporte sur A-6** : 📌 **un redécoupage ne
consomme pas `N`**, donc **une suite de redécoupages peut tourner
indéfiniment à l'intérieur d'une seule exécution.**

## A-2 · Le Réalisateur qui piétine sur un test
**Tranché — 🔴 on lui ouvre une sortie, on ne pose pas de seuil.**

📌 **Le geste 6 dit *« jusqu'à ce que les deux passent »***, sans
compter les tentatives. 🔴 **Deux cas** : **la fiche est fausse** — c'est
un blocage par règle, donc borné ; **le Réalisateur lit mal son test** —
⚠️ **borné par rien d'autre que son contexte.**

### Pourquoi ce n'est pas grave

📌 **A-3 le borne** : trois reprises par lot, un Réalisateur neuf à
chaque fois, puis la commande s'arrête.

📌 **Et une borne au nombre de tentatives couperait mal** — 🔴 **certains
tests demandent cinq itérations légitimes** ; compter les tentatives
punit ce cas-là.

⚠️ **Le chiffre du geste 6 est instructif** : *41 exécutions sur 149
n'ont rien trouvé, mesuré sur dix étapes.* 📌 **La consigne « par unité
cohérente, jamais par édition » vient d'une mesure.**

### Ce qu'on ajoute

🔴 **Il bloque quand deux tentatives de suite échouent pour la même
raison.** 📌 **Pas une durée — un fait observable** : il voit sa sortie
de test, il sait si c'est la même erreur.

📌 **Le critère distingue les deux cas** : **il progresse** — chaque
tentative change l'erreur, il continue ; **il piétine** — la même erreur
revient, et une tentative de plus ne changera rien.

⚠️ **Le cas attrapé** : il a mal compris ce que le test attend. **Il
modifie son code, l'erreur ne bouge pas, parce que le problème est dans
sa lecture.**

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/realisateur.md` | 🔴 **Une sortie de plus dans *When you cannot produce*** : deux tentatives de suite qui échouent pour la même raison. 📌 **Un blocage ordinaire**, avec la sortie du test et ce qu'il croyait faire |

⚠️ **Aucun cas observé** — 🔴 **mais ça ne crée aucun contrôle** : **ça
ouvre une sortie à un agent qui n'en a pas.** 📌 **Ce n'est pas un
filet : ça ne rattrape le travail de personne.**

## A-6 · Le redécoupage
**Tranché — 🔴 une borne, portée par la commande.**
⚠️ **Rouvre Rupture 3**, que j'avais écartée en disant *« la boucle
passe par le Product Owner »* — 📌 **faux pour celle-ci : elle tourne
seule.**

### Ce qui existe déjà, et qui est bon

📌 **Le Cadreur lit tous les redécoupages précédents** et cherche ce
qui revient : **le même symbole** *(la frontière est au mauvais
endroit)*, **la même entrée** *(elle porte plus d'une nature)*, **le
même genre de défaut** *(c'est le critère de coupe qui est faux)*.

📌 **Il écrit `## Ce qui revient` et `## Ce que j'en fais`** — 🔴 *« le
second champ est ce qui fait converger »* — **et il le signale au
Product Owner dès le troisième retour.**

🔴 **Le fichier nomme lui-même le mode d'échec** : *« le cinquième
redécoupage redit ce que le deuxième disait déjà »*.

### Ce qui manque

⚠️ **Tout cela est un jugement. Aucun compte, aucun arrêt.**

🔴 **Et personne n'intervient, par construction** — *« le Product Owner
n'attend sur rien »* pendant `/8_code`. 📌 **La boucle tourne donc à
l'intérieur d'une exécution**, et **U14 confirme qu'un redécoupage ne
consomme pas `N`.**

⚠️ **Chaque tour est le plus cher de la chaîne** : une coupe, jusqu'à
trois vérifications, les fiches d'un bloc, le code d'un lot, une
relecture.

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/commands/8_code.md` | 🔴 **Au troisième redécoupage d'une même exécution, elle s'arrête et rend la main**, avec le `## Ce qui revient` du Cadreur |

**Trois raisons :** 📌 **le Cadreur signale déjà le troisième retour** —
⚠️ **mais dans un rapport lu après coup, pas en s'arrêtant** · 📌 **trois
est le chiffre de la chaîne** : trois tours Cadreur ⇄ Vérificateur,
trois reprises par lot · 🔴 **un quatrième redécoupage dit rarement
autre chose que le troisième** — le Cadreur l'écrit lui-même.

📌 **Ce n'est pas un contrôle de plus** : **la commande compte ce que
l'agent signale déjà.**

---

# D — Défauts de frontière du verdict (section 4)

📌 **Le balayage du verdict est solide** : 59 artefacts, chacun avec son
producteur, ses lecteurs et un verdict. 🔴 **44 sont sains ; 24 défauts
en sortent.**

| # | État |
|---|---|
| D1 | **Écarté** — voir C3 |
| D2 | **Écarté** |
| D3 · D4 | **Traités** — couverts par A6 |
| D5 | ✅ **Corrigé dans la chaîne** |
| D6 | **Écarté** |
| D7 · D8 | **Écartés** |
| D9 | **Écarté** |
| D10 | **Tranché** |
| D11 | **Tranché** — voir Rupture 5 |
| D12 | **Traité** — voir D14 |
| D13 · D14 · D15 | **Tranchés** |
| D16 | **Écarté** — ✅ une ligne ajoutée à `audit_conventions` |
| D17 | ✅ **Corrigé dans la chaîne** |
| D18 · D19 | **Écartés** |
| D20 · D21 · D22 | ✅ **Corrigés dans la chaîne** |
| D23 · D24 | **Tranchés** |

⚠️ **Deux entrées du balayage sont caduques** — l'artefact 40 et la
mention de l'Extracteur : **il est supprimé de la chaîne.**

## D2 · Les identifiants de bloc
**Écarté — 🔴 la règle existe, le verdict ne l'a pas vue** *(il n'a lu
que les PROCESS)*.

📌 **Le Rédacteur** : *« numérotation assignée à l'écriture, jamais
réassignée — le fichier de questions adresse les blocs par numéro »*.
📌 **Le Découpeur** : *« numérote à partir du plus haut — jamais
réutiliser un numéro, même un que le découpage a retiré »*, et une
moitié garde le titre et le numéro d'origine quand elle porte ce que ce
titre nommait.

📌 **Le cas du verdict** — `B7` dont une réponse remplace la phrase :
**le bloc est édité sur place et marqué `MODIFIED`**, donc `B7` reste
`B7` avec un contenu neuf. ⚠️ **`tracabilite.md` est refaite à chaque
conversion**, donc aucune trace ancienne ne pointe à faux.

🔴 **À noter** : **`PROCESS_AMONT` ne dit pas que les identifiants sont
stables**, alors que six lecteurs s'en servent.

## D3 · Les marqueurs, et la réponse qui ne change rien
**Traité — 🔴 couvert par A6.**

**D4 est faux** — 📌 **le Découpeur marque bien ses blocs** : `NEW` sur
ceux qu'il crée, `MODIFIED` sur celui qui garde le titre d'origine,
*« quelque chose pointait déjà vers lui »*.

**D3 est mal cadré** — ⚠️ **`/6_convertit` compare des octets non par
défiance, mais parce que le Rédacteur efface les marqueurs à chaque
tour** : un bloc changé deux tours plus tôt n'en porte plus.
📌 **Besoin différent, pas incohérence.** 🔴 **Le risque réel — un
`MODIFIED` oublié, sans détecteur — reste, mais aucun cas n'est
observé** *(critère n°3)* **et un contrôle serait un filet.**

**Le vrai cas, A1 du verdict** — 📌 **une réponse « oui, c'est ça » ne
change rien, ne marque rien, ne s'inscrit nulle part.** 🔴 **Le bloc
confirmé est valide et n'a pas à repasser** — ⚠️ **mais dès qu'un bloc
voisin est marqué, la passe B repose la même question.**

🔴 **A6 le règle en amont** : 📌 **une question à laquelle le Product
Owner répondrait « oui, c'est ça » est exactement celle que le Sondeur
aurait dû poser comme un *défaut*** — **il ne répond rien, le cycle
inutile disparaît.**

⚠️ **Résidu assumé** : un défaut accepté n'est écrit nulle part, donc
reproposé au tour suivant. 📌 **Quelques lignes à parcourir, rien à
écrire** — ⚠️ **la seule gêne est de croire sa réponse perdue.**

📌 **Piste pour plus tard, si ça devient pénible** : l'Assembleur
retirerait un défaut déjà accepté sur un bloc inchangé. 🔴 **C'est dans
son rôle** — il ne compare que des questions entre elles, jamais au
fichier produit. ⚠️ **Optimisation, pas correction — à instruire sur un
cas réel.**


📌 **Listés pour ne pas les perdre. Aucun n'est instruit.**

| # | Le défaut |
|---|---|
| D20 | `/8_code` invoque le Contrôleur sans les groupes qu'il exige — **le contrôle de fin de chaîne ne peut pas se lancer** |
| D23 | Les fiches d'un cycle de correction sont hors du dossier que le Contrôleur lit — le second rapport est faux |
| D3 · D4 · A1 | Un `MODIFIED` oublié = un bloc jamais resondé, **sans détecteur** ; les blocs du Découpeur peut-être sans marqueur ; une réponse « on garde tel quel » ne laisse aucune trace |
| D10 | Une question technique du Convertisseur voyage sur la route produit, où personne ne peut y répondre |
| D19 | Le résultat des tests est recopié, jamais rejoué |
| D2 | Rien ne garantit la stabilité des identifiants de bloc, que six lecteurs utilisent |
| D11 · D12 · D14 · D16 | Les conventions : redérivées par fonctionnalité sans lire les amendements ; qui les lit dit deux choses ; un test mécanique déclaré et jamais câblé ; le lot demandeur codé sous l'ancienne règle |
| D13 | Le titre d'une section du global n'est vérifié par personne |
| D17 | Un blocage tranché est renommé par un agent et supprimé par cinq |
| D5 · D7 · D8 · D18 · D21 · D22 · D24 | Producteurs sans lecteur, lecteurs sans producteur, cas non couverts |
| Ruptures 3 et 5 | Deux boucles autonomes sans plafond · l'Architecte redérive sans lire ce qu'il a lui-même ajouté |

## D5 · `[integrated: B7]`
✅ **Corrigé dans la chaîne — la marque est retirée du Rédacteur.**

📌 **Elle était écrite à chaque intégration et personne ne la lisait**
*(`/2_structure` range le fichier par `git mv`, sans le lire)*.

🔴 **Et lui donner un lecteur l'aurait aggravée** : ⚠️ **une marque à
poser sur chaque entrée est une case à remplir** — 📌 **C5 a mesuré ce
que ça produit** : l'agent remplit au lieu de traiter. **La marque
certifierait un travail non fait, et on croirait avoir un contrôle.**

📌 **Ce qu'on perd : rien d'effectif.** ⚠️ **Le risque réel — une
réponse sautée à l'intégration — n'avait pas davantage de détecteur
avec la marque.** 🔴 **S'il se matérialise**, le remède sera une
comparaison mécanique du fichier produit avant/après, du type de celle
de `/6_convertit` — **jamais une case à cocher.**

📌 **`cycle.md` s'en servait** pour deviner l'état d'un fichier de
questions — ⚠️ **elle est périmée**, et le rangement rend le test
obsolète : **un fichier intégré est rangé aussitôt, donc sa présence à
la racine dit qu'il attend.**

## D6 · La passe A faite quatre fois
**Écarté — 🔴 le recouvrement est une relecture, pas une passe A
refaite ; et le remède rouvrirait C5.**

📌 **Ce que fait la globale** : six lignes par bloc — `A1.1` à `A1.4`,
`A1.9`, `A4` — 🔴 **sans questionner** : *« tu relèves, tu ne
questionnes pas ; les trous de la passe A sont le travail des angles »*.

📌 **Ce que font les angles** : **toute** la passe A — `A1.5` à `A1.8`,
`A2` par nature, `A3`, `A4` en entier — **et ils cherchent les trous.**

🔴 **Donc ce n'est pas quatre fois le même travail.** ⚠️ **Le
recouvrement réel** : sur un bloc marqué, la globale relit ce que les
angles viennent de lire et ré-extrait six réponses qu'ils ont
formulées sans les écrire — **puisqu'ils n'écrivent que les trous.**

📌 **Sur un tour où cinq blocs ont bougé, la globale relit 187 blocs de
toute façon** — c'est son objet. **Les cinq relus en double sont
marginaux.**

🔴 **Et le remède est interdit** : faire écrire le relevé par les angles,
c'est leur demander une trace exhaustive — ⚠️ **exactement ce que C5 a
mesuré et écarté.**

📌 **Ce qui coûte vraiment, c'est le relevé complet à chaque tour** —
🔴 **et c'est C4 et Rupture 6, pas D6.**

## D7 · `cadrage-produit/closed/`
**Écarté — 🔴 le dossier a un producteur et un usage.**

📌 **`/4_grille` y range les six fichiers du tour précédent** — les
quatre sorties des sondeurs, le relevé, le fichier fusionné — **par
`git mv`, numérotés.** 🔴 **Même mécanisme que `questions/<agent>/`** :
l'espace de travail du tour reste propre.

📌 **Personne ne les relit, et c'est normal** — ce sont des archives.

✅ **`PROCESS_AMONT` corrigé** : il ne décrivait que la création du
dossier, avec une raison fausse *(« un agent dont le dossier cible
manque cherche au lieu de s'arrêter »)* — ⚠️ **aucun agent n'y écrit,
c'est la commande seule.** 📌 **C'est pourquoi le verdict a cru le
dossier orphelin.**

## D8 · Un renvoi vers un bloc sans entrée
**Écarté — 🔴 le cas est couvert, aux deux endroits.**

📌 **La commande** : *« une entrée → écris le numéro. **Plusieurs, un
tiret, ou aucune ligne → laisse-les** »* — l'invocation 2 s'en charge.

📌 **L'agent** : *« ce qui reste nomme un bloc qui en a donné plusieurs,
**ou aucune** »*, puis *« aucune ne porte ce qui est attendu, ou la
ligne est un tiret → **une question**, laisse les crochets »*. 🔴 **Avec
sa raison** : une référence qui nomme une cible sans qu'elle réponde de
ce qu'on attend est pire que pas de référence.

⚠️ **Le verdict a raison sur le PROCESS**, qui ne décrit que les deux
premiers cas — 🔴 **faux sur les fichiers.**

### 📌 Un motif, sur les huit premiers défauts instruits

🔴 **Cinq étaient faux parce que le PROCESS est moins précis que les
agents** — D2, D4, D7, D8, et D20 en partie. ⚠️ **Ce n'est pas un
défaut du verdict** : c'est ce que son cadrage lui imposait. 📌 **Mais
ça dit quelque chose des PROCESS.**

## D9 · Les dépendances du préambule
**Écarté — 🔴 le verdict s'est trompé d'artefact.**

📌 **Ce que dit le Convertisseur** : les dépendances du préambule
viennent des **références marquées *existing*** — ⚠️ **pas de phrases
hors blocs.**

📌 **Ce que fait le Rédacteur** : quand un bloc pointe vers quelque
chose, il nomme la destination et **la marque *existing* si elle est
déjà au global** — *« Le bouton Pas mène à l'écran de saisie des pas —
existing »*.

🔴 **L'artefact existe, il est nommé, et il vit dans un bloc** — donc
**la grille le sonde comme les autres.** ⚠️ **Le verdict supposait qu'il
voyageait par le texte hors blocs, et en tirait que rien n'était
sondé.**

### Ce qui reste vrai, et qui compte plus

⚠️ **La marque *existing* dépend du grep de l'index du global par le
Rédacteur** — 🔴 **le même grep sur lequel A2 repose entièrement**, et
dont **D13** dit que personne ne vérifie les titres.

📌 **Le texte hors blocs existe bien** — intention, vocabulaire,
hors-périmètre — **lu par le Convertisseur pour son préambule, sondé
par personne.** ✅ **Le hors-périmètre reçoit un genre et une
destination avec A1** ; 📌 **le reste n'a pas à être sondé : ce ne sont
pas des comportements.**

## D10 · Les questions techniques du Convertisseur
**Statut : tranché. 🔴 Reste l'écriture, et un calibrage sur cas
réels.**

### Le défaut

📌 **Une question du Convertisseur voyage par la route produit** — le
Product Owner, `/1_lexique`, le Rédacteur. 🔴 **Une question *technique*
n'a personne pour y répondre sur cette route** : ⚠️ **le Product Owner
ne peut pas arbitrer un nom technique, et le Rédacteur n'a nulle part
où écrire la réponse dans un fichier produit.**

📌 **Vérifié** : la forme de ses questions porte `Block:`, *« les blocs
que la réponse changera — le Rédacteur intègre par bloc »*. ⚠️ **Une
question technique n'a pas de bloc.**

🔴 **Aucun cas observé** — le Convertisseur n'a pas tourné depuis la
refonte.

### 🔴 Ce qu'on ne fait pas

⚠️ **« Il tranche seul les choix techniques » : refusé par le Product
Owner.** 📌 **Un arbitrage qui change profondément la nature de
l'application doit pouvoir être validé.**

### Ce qu'on modifie — deux routes

📌 **Le Convertisseur peut écrire deux fichiers par exécution :**

| Le fichier | La route |
|---|---|
| **`questions-convertisseur-NN.md`** — questions produit | 🔴 **Boucle longue** : Product Owner, `/1_lexique`, `/2_structure`, toute la chaîne |
| **Un fichier de questions techniques** — 🔴 **nom hors du motif `questions-*.md`**, pour que la boucle longue ne le détecte pas | 📌 **Boucle courte** : Product Owner, puis `/6_convertit` |

| Ce qu'il écrit | Ce qu'on fait |
|---|---|
| Technique seul | Répondre, puis `/6_convertit` |
| Produit seul | Boucle longue |
| **Les deux** | 🔴 **Boucle longue** — et à son retour, **il intègre les deux fichiers** |

📌 **Pourquoi la boucle courte est légitime** : une réponse technique ne
modifie pas le fichier produit, **donc rien en amont n'a à être
rejoué.** ⚠️ **C'est une exception explicite à la route unique** — à
dire, puisqu'elle contredit *« toute réponse repasse par
`/1_lexique` »*.

### Où la réponse s'écrit

🔴 **Nulle part.** 📌 **Elle est appliquée à la réécriture** : la
section concernée est refaite avec la réponse sous les yeux. ⚠️ **Aucune
trace à maintenir dans `spec-technique.md`.**

📌 **Sur quelle invocation relancer : sans objet** — `/6_convertit`
décide déjà par comparaison d'octets, et la transversale tourne de
toute façon.

### La frontière — ce qu'il tranche, ce qu'il pose

⚠️ **Il tranche déjà énormément** : il nomme, range, reformule en règles
exécutables. 🔴 **Lui faire poser tous ses choix produirait des
centaines de questions.**

🔴 **Le critère : la réversibilité.**

> 📌 **Un choix qui peut être défait plus tard sans toucher au produit
> se tranche seul. Un choix qui, une fois pris, contraint ce que
> l'application pourra faire, se pose.**

| | |
|---|---|
| **Il tranche** | Renommer un symbole · ranger une règle dans une section plutôt qu'une autre · choisir une comparaison |
| **Il pose** | 🔴 **Décider que deux concepts distingués par le Product Owner n'en font qu'un — ou l'inverse.** ⚠️ **Tout le code qui suit repose dessus** |

⚠️ **Le critère est un jugement, et rien ne le calibre** — 🔴 **personne
ne sait quelles questions techniques il produira.** 📌 **On pose le
mécanisme et une frontière prudente, puis on regarde le premier
cycle** : zéro question, on aura construit pour rien sans que ça coûte ;
cinquante, on resserre.

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/convertisseur.md` | 🆕 **Un second fichier de questions, techniques**, au nom hors du motif `questions-*.md`. 🔴 **La frontière : réversibilité** — ce qui se défait sans toucher au produit, il le tranche ; ce qui contraint ce que l'application pourra faire, il le pose |
| `.claude/commands/6_convertit.md` | 🔴 **Le routage à trois cas** : technique seul → boucle courte · produit seul → boucle longue · les deux → boucle longue, et il intègre les deux au retour |
| `docs/process/PROCESS_AMONT.md` | ⚠️ **L'exception explicite à la route unique** — une réponse technique ne repasse pas par `/1_lexique` |

---

## D13 · Les titres du global
**Statut : tranché. 🔴 Reste l'écriture.**

### Le défaut

📌 **Le PROCESS énonce le critère** : *« un titre doit dire ce que sa
section contient, sinon l'index ne sert à rien — c'est le critère de
qualité du global »*. 🔴 **Le Fusionneur, seul agent qui écrit dans le
global, n'a que cinq verbes — `REPLACE`, `INSERT`, `KEEP`, `DELETE`,
`PENDING`. Aucun ne porte sur un titre.**

### Pourquoi ça compte

🔴 **Le global se lit uniquement par son index**, et deux mécanismes en
dépendent : 📌 **le Rédacteur y cherche un titre proche pour ranger un
bloc** ; 🔴 **A2 — le tri de ce qui touche à l'existant repose
entièrement sur ce rangement.**

⚠️ **Un titre qui a dérivé, c'est une section que le Rédacteur n'ouvre
jamais.** 📌 **Il croit le sujet absent, crée une section neuve, et le
doublon entre au global à la fusion suivante** — 🔴 **le défaut
s'aggrave tout seul.**

📌 **Le mécanisme de dérive est certain** : une section reçoit des blocs
au fil des fonctionnalités ; **le titre a été écrit pour le contenu
d'origine, et personne ne le rouvre.**

### Ce qu'on modifie

🔴 **Quand le Fusionneur ajoute un bloc à une section existante —
`INSERT` — il regarde si le titre couvre encore ce que la section
contient.** 📌 **Sinon, une question pour le Product Owner** : renommer
une section du global est une décision produit.

**Trois raisons pour que ce soit lui :** 📌 **il est le seul à écrire
dans le global** · **il a la section sous les yeux au moment d'y
insérer** · 🔴 **il ne le ferait que sur les sections qu'il touche —
le coût est proportionnel au changement.**

⚠️ **Aucun cas observé** — le global vient de naître. 🔴 **Mais ce
défaut ne se voit qu'après plusieurs fonctionnalités, et il aura alors
déjà produit des doublons.**

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/fusionneur.md` | 🔴 **À l'`INSERT` dans une section existante, il regarde si le titre couvre encore ce qu'elle contient.** 📌 **Sinon, une question au Product Owner** — renommer une section du global est une décision produit |
| `docs/process/PROCESS_AMONT.md` | Le critère de qualité du global, et qui l'applique |

---

## D14 · Vérifier que les conventions sont appliquées
**Statut : tranché. 🔴 Reste l'écriture.**
*(Parti de D14 — `couverture.md` promet un câblage que personne ne
fait. Le sujet a été ouvert bien plus large par le Product Owner.)*

### Le besoin, mesuré

🔴 **9 défauts sur 21 violent une règle écrite, lue, et non
appliquée.** 📌 **Trois causes**, et elles n'appellent pas le même
remède :

| | |
|---|---|
| **Jamais appliquée** | 24 attentes, **zéro bornée** |
| **Appliquée inégalement** | 🔴 **Le motif dominant** — la règle correcte ailleurs dans le même fichier, absente sur le chemin nominal |
| **Satisfaite à la lettre** | L'exception ne traverse pas *en étant levée*, elle traverse *en étant transportée* dans le `Result` |

⚠️ **Et un mécanisme d'aggravation** : 🔴 **une règle enfreinte une
fois est prise pour modèle** — et le fichier documente la violation
comme un choix délibéré.

### Ce que les quatre investigations ont établi

| | |
|---|---|
| **Mécanisation** | Sur 91 règles : **13 câblables** · **27 vérifiables par un lecteur sur un lot** · **11 hors de portée d'un lot** |
| **Déclencheur** | **50 permanentes** · 28 spécifiques · 13 qui n'ont rien à faire là |
| **Utilité de la grille** | 🔴 **34 entrées sur 70 enfoncent des portes ouvertes** — 12 arbitrages, 24 corrections |
| **Règles hors grille** | Sur 25 ajoutées par demande : **11 portes ouvertes**, 8 arbitrages, 6 corrections. 🔴 **8 des 18 restrictions restreignent une règle elle-même hors grille — le fichier grandit par empilement** |

📌 **Apport décisif du Product Owner** : les 34 portes ouvertes viennent
probablement de trois causes historiques corrigées depuis — un document
technique déconnecté du produit, un Détailleur qui ratait des choses,
Sonnet là où il fallait Opus. 🔴 **On ne peut le prouver qu'en retirant
et en observant.**

### Les six modifications, et où elles se portent

| # | Où | Quoi |
|---|---|---|
| **1** | `docs/process/GRILLE_CONVENTIONS.md` | 🔴 **Retirer les 34 entrées porte ouverte**, garder les 36. 📌 **Archiver les retirées** avec leur texte et la raison — **pour pouvoir remettre, pas pour se souvenir** |
| **2** | `.claude/agents/architecte.md` | 🔴 **Chaque règle porte son déclencheur** : *permanente* (un geste ordinaire de code, dans n'importe quel lot) ou *spécifique* (ce que ce lot fait en particulier). 📌 **C'est lui qui sait ce qui déclenche une règle** |
| **3** | `.claude/agents/realisateur.md` | 🔴 **Il ne lit plus tout le fichier** : les permanentes en entier, plus celles que la fiche nomme. ⚠️ **Avec l'emphase — ce sont les plus importantes de tout ce qu'il lit.** 📌 **Sa contradiction actuelle disparaît** : il dit aujourd'hui *« applique tout le fichier »* et *« tiens ce que la fiche nomme »* |
| **4** | `.claude/agents/relecteur.md` | 🔴 **Il ne saute pas** (F1 renversé). 📌 **Son point 3 s'étend** : les conventions que la fiche nomme **et les permanentes**, puisqu'elles s'appliquent partout |
| **5** | `.claude/agents/arbitre.md` | 🔴 **Il trie ce qui remonte** — voir la table ci-dessous |
| **6** | `.claude/agents/architecte.md` | 🔴 **Retirer la seconde table de `couverture.md`.** 📌 **Son seul contenu utile — mécanique ou revue — est déjà dans le fichier de conventions, et il y est juste.** ⚠️ **La table est fausse sur 22 liens sur 68.** 📌 **La première table reste** : c'est le contrôle de balayage de l'Architecte |

**Le tri de l'Arbitre :**

| La demande apporte | Où ça va |
|---|---|
| **Un arbitrage** — deux choix défendables, deux lots divergeraient | Les conventions |
| **Un piège de plateforme indevinable avant le test rouge** | 🔴 **`## Traps`**, pas les conventions |
| **« La règle X s'applique-t-elle à mon cas ? »** | 🔴 **Rien** — c'est une question de lecture, pas un manque |
| **Une règle devenue fausse** | Les conventions, en remplacement — ⚠️ **et c'est D5 : le Product Owner arbitre** |

📌 **Pourquoi `## Traps` est la bonne destination d'un piège** : 🔴 **le
Réalisateur le lit en entier, toujours** — *« tu ne peux pas greper une
règle dont tu ignores qu'elle s'applique à toi »* — ⚠️ **alors qu'une
convention n'est tenue que si la fiche la nomme.**

### Ce qui reste ouvert, assumé

🔴 **20 règles permanentes que personne ne garantit appliquées.**
📌 **Le rangement ne résout pas l'attention** — ⚠️ **on a réduit trois
fois, on n'a pas résolu.**

📌 **Une piste non instruite** : les 20 permanentes se regroupent en
**huit sortes de gestes**, dont une pèse huit règles — **le code qui
sort de lui-même** (un autre thread, un autre process, le disque, une
ressource système). 🔴 **Huit vigilances se tiennent ; vingt règles
numérotées, non.** ⚠️ **Réorganiser le fichier par geste est un travail
réel** — à ne faire que si le resserrement ne suffit pas.

📌 **Au passage** : aucune règle conservée ne se déclenche sur un
`catch`. **Les deux qui portaient sur le geste d'attraper sont des
portes ouvertes** ; ce qui survit porte sur **où la faute va ensuite**.

**Rebouclage :** 🔴 **`todo.md`** — le cycle de vie du fichier de
conventions et de `## Traps` : ni l'un ni l'autre ne se vide.

### Ce que ça change

📌 **Les six modifications sont déjà dans la table ci-dessus** —
🆕 **grille resserrée**, `architecte.md` *(marquage + seconde table
retirée)*, `realisateur.md`, `relecteur.md`, `arbitre.md`.

---

## D15 · Un trou de couverture répondu hors de la route produit
**Statut : tranché. 🔴 Reste l'écriture.**

### Le défaut

📌 **L'Architecte trouve une question de comportement à laquelle le
corpus ne répond nulle part.** 🔴 **Par définition de la chaîne, c'est
un trou de la grille de cadrage — le produit n'était pas fermé.**

⚠️ **Aujourd'hui il te la pose, et son invocation 2 « transforme ses
propres réponses en règles »** — 🔴 **une décision de comportement
devient une convention.** 📌 **Elle n'atteint ni le fichier produit, ni
le document technique, ni le global** : le Fusionneur ne lira jamais ce
fichier, **et le global décrira une application dont un comportement
est décidé ailleurs.**

### Le mécanisme — aucun raccourci

🔴 **La chaîne n'invente pas de chemin de secours. Elle signale.**

1. 📌 **L'Architecte poursuit son travail jusqu'au bout** — toutes ses
   questions, toutes ses règles. ⚠️ **Rien ne bloque : le travail fait
   n'est pas perdu**
2. 🔴 **Une question qui se révèle être du produit est marquée comme
   telle**, distinctement des autres
3. 🔴 **Il ne la transforme jamais en convention, à aucune
   invocation** — **c'est le seul interdit**
4. 📌 **Le Product Owner trie** : soit c'est du produit et le cycle
   repart, soit ce n'en était pas une — il la supprime ou répond
   qu'elle se traite autrement, et l'Architecte reprend normalement

### Ce que ça demande à son fichier

🔴 **Séparer deux de ses trois sortes de manques**, qu'il traite
aujourd'hui de la même façon : 📌 **une *conjonction* est une question
qu'aucune grille ne pouvait voir — légitime** ; 🔴 **une *couverture*
est un trou de grille.**

⚠️ **Dans le doute entre *couverture* et *précision*, il pose plutôt
que de trancher** — 📌 **le coût d'une fausse alerte est une lecture,
celui d'un faux négatif est un comportement décidé hors produit.**

### Le pari, explicite

📌 **Le mécanisme existe pour ne jamais servir.** 🔴 **S'il sert
souvent, c'est la grille de cadrage qu'il faut reprendre, pas le
mécanisme.** ⚠️ **Et remettre dans la boucle coûte un cycle entier —
c'est le prix de la robustesse.**

🔴 **Rien ne va au registre d'A5** — voir là-bas.

### Ce que ça change

| Fichier | Ce qu'il faut |
|---|---|
| `.claude/agents/architecte.md` | 🔴 **Séparer *couverture* et *conjonction***, qu'il traite aujourd'hui de la même façon. 📌 **Une question produit est marquée comme telle**, distinctement. 🔴 **Jamais transformée en convention, à aucune invocation.** ⚠️ **Il poursuit son travail jusqu'au bout — rien ne bloque.** 📌 **Dans le doute entre *couverture* et *précision*, il pose** |
| `docs/process/PROCESS_AMONT.md` | Le mécanisme, et le pari : il existe pour ne jamais servir |

---

## D16 · Le lot codé sous l'ancienne règle
**Écarté — 🔴 la trace existe, par deux chemins.** ✅ **Une ligne
ajoutée à `audit_conventions`.**

📌 **Le verdict admet que le compromis est bon** — garder le lot
atomique. 🔴 **Son grief : la divergence ne serait consignée nulle
part.**

⚠️ **Faux, deux fois :** 📌 **le fichier de demande porte le lot dans
son nom** — `architecte/detailleur-lot-04.md` — **et la fiche du lot
porte une section `## Requests` qui le nomme**, avec sa raison : *« sans
elle, personne ne sait qu'une demande a été écrite »*.

📌 **Et `audit_conventions` s'en sert déjà** : son constat 1 nomme la
règle **et la demande qui l'a produite**, et la demande nomme le lot.

### Ce qui manquait vraiment, et c'est petit

🔴 **Personne ne faisait le pas de plus** : *ce lot a été codé sous
l'ancienne règle — va-t-il le rester ?*

✅ **Ajouté au constat 1 de `audit_conventions`** : nommer le lot, dire
qu'il a été codé sous la règle telle qu'elle était, **et laisser le
Product Owner décider.** 📌 **Même nature que le « remplacer » de
Rupture 5** — reprendre coûte du temps, laisser divergent coûte de la
cohérence.

## D18 · L'inventaire des symboles du Cadreur
**Écarté — 🔴 il a un fichier, et le Vérificateur le lit.**

📌 **Le Cadreur écrit `code/decoupage.md` : l'inventaire des symboles,
puis la liste des lots.** 🔴 **Un seul fichier**, dit en toutes lettres
dans ses lectures et ses écritures, **écrit avant la coupe** — *« ne
coupe pas avant que l'inventaire soit écrit »*.

📌 **Le Vérificateur lit `code/decoupage.md`** : il a donc bien
l'inventaire, et son croisement n'est pas une ratification.

✅ **`PROCESS_AVAL` corrigé** : sa table des fichiers disait
*« `code/decoupage.md` (avec les ancres) »* sans mentionner
l'inventaire. ⚠️ **Même motif que D7 et D8 — le PROCESS est moins
précis que les agents.**

## D19 · Le résultat du build, jamais rejoué
**Écarté — 🔴 mesuré et abandonné dans une version antérieure ; et un
contrôle sans suite n'est pas un contrôle.**

📌 **Le verdict propose une exécution indépendante** : le Réalisateur
lance les tests et écrit le résultat, le Relecteur le recopie, personne
ne relance.

🔴 **Essayé dans la toute première version** — un reviewer rejouait les
tests après le Réalisateur. ⚠️ **Aucune divergence, jamais** : du temps
perdu à refaire des tests déjà bons. 📌 **Le mécanisme actuel est ce qui
reste de cette mesure** — le Réalisateur écrit le résultat brut, il ne
peut pas tricher, le Relecteur vérifie qu'il est vert.

🔴 **Et une exécution en fin de bloc ne mène nulle part** *(objection du
Product Owner)* : **un test qui vire au rouge demanderait de savoir
quel lot a cassé quoi, de rouvrir un lot déjà PASS, de relancer un
Réalisateur, de refaire passer le Relecteur.** ⚠️ **Une boucle entière,
sans agent pour la porter** — 📌 **proposer un contrôle sans dire ce
qu'on fait de son résultat est exactement ce que la méthode interdit.**

📌 **A3 renforce le mécanisme plutôt qu'il ne le remplace** : le test
rouge prouve que le test affirme quelque chose, le test vert que le
code le satisfait — **deux exécutions par deux contextes différents, au
moment où elles servent.** 🔴 **Un troisième passage n'ajouterait rien.**

📌 **Des trois cas du verdict** — sortie mal lue, test écarté par un
filtre, suite verte sur une cible non compilée — **le dernier est déjà
couvert** : le Relecteur échoue structurellement un lot dont le module
ne compile pas. ⚠️ **Les deux autres n'ont jamais été observés.**

## D21 · « Ce document commande le Cadreur »
✅ **Corrigé dans `PROCESS_AVAL` — la phrase était fausse, deux fois.**

📌 **Vérifié : le Cadreur ne lit pas `CURRENT_TECHNICAL_STATE.md`.**
Son fichier ne le mentionne nulle part. 🔴 **Il tranche production /
modification par grep**, contre son propre inventaire de symboles.

🔴 **Et c'est le bon choix** : 📌 **le code est la vérité, ce document
est un cache** — un cache qui aurait dérivé ferait déclarer *production*
un symbole qui existe. ⚠️ **Et il est écrit par le Réalisateur, avec les
mêmes mots que le grep du Cadreur** : il ne corrigerait pas mieux la
limite de P4 *(le grep est la connaissance)*.

📌 **Corrigé aux deux endroits** : la liste des lecteurs est
Détailleur, Réalisateur suivant, Diagnostiqueur.

## D22 · « Ce qu'un lot a rendu faux disparaît »
✅ **Corrigé dans `realisateur.md`.**

📌 **La consigne était bonne, elle n'était pas outillée.** 🔴 **Le
Réalisateur ne lit en entier que deux sections** — et l'argument qui
justifie cette lecture, *« on ne peut pas greper une règle dont on
ignore qu'elle s'applique »*, **vaut exactement contre la consigne.**

⚠️ **Une consigne qu'on ne peut pas tenir est pire qu'une consigne
bornée** : la première donne l'illusion d'une garantie, la seconde dit
où elle s'arrête.

**Ce qui est écrit maintenant :** 📌 **il cherche dans ce qu'il a
touché** — ses symboles, ses fichiers édités, grepés dans le document.
🔴 **Une entrée rendue fausse ailleurs par ricochet n'est pas à lui de
la trouver** — elle le sera par le prochain qui la lira.

✅ **Et le cas FAIL, que le verdict signalait non traité** : sur un
*FAIL structurel*, le Réalisateur neuf grepe les symboles du lot dans
l'état technique et **retire ce que la tentative échouée y avait
écrit**, avant d'écrire la sienne. ⚠️ **Sans ça, deux entrées
coexistent pour un même lot.**

📌 **La phrase « ce document commande le Cadreur » est aussi retirée
d'ici** — voir D21.

## D23 · Le Contrôleur et les cycles de correction
**Tranché — 🔴 on n'étend pas. ✅ `PROCESS_AVAL` corrigé.**

📌 **Le défaut est réel** : les fiches d'un `bugfix-NN/` ne sont dans
aucune carte bloc → lots, donc un second passage redirait les mêmes
manques.

🔴 **Mais on ne l'étend pas, pour deux raisons :**

⚠️ **Le Contrôleur est un filet** — 📌 **l'étendre au bugfix, c'est un
filet sur un filet.**

🔴 **Et il n'y a rien à confronter** : un `desc-bug.md` décrit des
écarts observés, **pas des intentions.** 📌 **Le Contrôleur fait
*produit → fiche*, et un cycle de correction n'a pas de produit.**

### Ce que son rôle vaut, mesuré

📌 **Sur l'application de test** : 20 écarts au premier tour, puis
**sept sessions de correction de 20 à 30 bugs chacune**, trouvés à la
main dans l'application. 🔴 **Il a attrapé de l'ordre de 10 % de ce qui
manquait.**

⚠️ **C'est cohérent avec son périmètre** : il vérifie qu'une intention
a une fiche qui la porte — **pas que le code fait ce que la fiche dit**
*(le Relecteur)*, **ni que l'application se comporte comme prévu**.
📌 **Ce qui reste à trouver à la main, c'est A4** — la recette dirigée.

### Pourquoi on le garde quand même

📌 **Décision du Product Owner** : 🔴 **coût marginal, une invocation en
fin de cycle**, et il rattrape en première intention ce qui aurait pu
passer. ⚠️ **Et sa commande porte désormais deux autres livrables** —
la recette dirigée (A4) et le registre (A5) : **même s'il ne trouve
rien, la commande a une raison d'exister.**

✅ **Corrigé dans `PROCESS_AVAL`** : la phrase *« pour comparer deux
états »*, à trois endroits — 🔴 **elle promettait une comparaison que la
commande interdit.** 📌 **Et `/8_code` ne lance pas le Contrôleur**,
conformément à D20.

## D24 · Le push, dans le merge ou occasionnel
**Tranché — 🔴 le PROCESS a raison ; la contradiction est ailleurs.**

📌 **Le PROCESS dit** : *« le push fait partie du merge, pas d'un
après-coup — une phase qui ne vit que sur la machine locale est perdue
avec elle »*. ⚠️ **Les instructions permanentes de l'orchestrateur
disent que pousser est occasionnel.**

✅ **Confirmé par le Product Owner** : 🔴 **commit, merge, push, dans
cet ordre, le plus souvent possible** — pour avoir des sauvegardes et
pouvoir revenir en arrière.

📌 **`HEAD` local reste la bonne référence** — ⚠️ **mais pour la raison
inverse de celle qui est écrite** : il est fiable **parce que** tout est
poussé, non parce que pousser serait occasionnel. 🔴 **Seule la
justification est à ajuster**, dans les instructions d'orchestration —
hors de la chaîne.

📌 **Seul défaut du verdict situé hors des deux PROCESS** — *« une
frontière entre le process et son exécutant, que le process ne peut pas
voir »*.

---

# P — Les prémisses du verdict (section 6)

📌 **Ce que la chaîne ne met jamais en question parce que sa forme rend
la question impossible à poser.** 🔴 **Les quatorze ont été rouvertes
une par une** — ⚠️ **aucune n'appelle de modification propre** : elles
renvoient à des sujets déjà tranchés, ou sont écartées avec leur
condition.

| # | La prémisse | Sort |
|---|---|---|
| **P1** | La personne répond par fichiers, hors ligne, jamais en conversation | **Saine** — 📌 **déjà relâchée là où ça compte** : le sondage de vingt minutes de l'Arbitre *(F3)*. ⚠️ **Le coût — la longueur de l'amont — est attaqué par A6 et le chantier lexique** |
| **P2** | Huit natures partitionnent tout, et la nature est à la fois grille, section et couche | **Saine** — **C2**. 📌 **Le second coût — un bloc scindé pour entrer dans la liste — n'est pas dû à la taxonomie** : **un déclencheur, une production** est une règle produit, pas technique |
| **P3** | Un document technique gelé au découpage | **Écartée** — 🔴 **le Contrôleur ne lit jamais `spec-technique.md`** : il compare `desc-produit.md` aux fiches. 📌 **Et un lot en PASS est clos** : le Cadreur ne peut pas le rouvrir. ⚠️ **Résidu** : un lot non codé dont une entrée aurait été rendue fausse — jamais observé |
| **P4** | Le grep est la connaissance | **Saine chez nous** — 🔴 **le coût n'existe que sur du code écrit ailleurs** ; les projets partent de zéro, nommés par les conventions de l'Architecte. 📌 **A2** *(le global pour la question produit)* · **F2** *(un agent qui lit du code hérite du style)*. **Rouverte si la chaîne reprend du code d'un tiers** |
| **P5** | Les marqueurs sont la mémoire | **Écartée** — **D3 · D4 · A6**. 📌 **Piste identifiée et peu coûteuse** : une comparaison d'octets bloc par bloc, *« les marqueurs deviendraient une courtoisie »*. ⚠️ **Aucun cas observé** |
| **P6** | Le Rédacteur transcrit fidèlement | **Écartée** — **C3**. 📌 **Le partage d'A1 ajoute une étape, mais elle est mécanique** : `/5_reclasse` compte les blocs et s'arrête si le compte ne tombe pas |
| **P7** | La grille est complète et s'édite à la main | **Saine, délibérée** — 🔴 **le Product Owner veut garder le contrôle du process**. 📌 **A5 conserve la matière** ; ⚠️ **le coût subsiste** : entre le manque et l'ajout, chaque fonctionnalité paie la même faille |
| **P8** | La commande est la machine d'état, et c'est une session de modèle | **Écartée** — 📌 **les trois échecs observés sont des erreurs d'environnement**, qu'un script n'empêche pas. ⚠️ **Deux artefacts à tenir d'accord coûtent plus qu'ils ne rapportent.** 🔴 **La règle : on scripte un geste mécanique *dont une erreur coûte cher*** — pas parce qu'il est mécanique |
| **P9** | Un contexte neuf est une paire d'yeux | 🔴 **La mieux tenue** — **C5** *(42 contre 140, mesuré)* et **A3** s'appuient dessus. 📌 **L'inversion chez le Cadreur est argumentée** : il tient le compte des trois tours |
| **P10** | La fiche se suffit à elle-même | **Atténuée, et c'est voulu** — 🔴 **D14** : le Réalisateur lit aussi les permanentes, **parce que le Détailleur ne peut pas nommer ce qu'il n'a pas prévu.** 📌 **Le cœur tient** : aucune architecture à décider. ⚠️ **À vérifier à l'écriture** : la formulation dans `PROCESS_AVAL` |
| **P11** | Les documents vivants restent vrais | **Saine** — **D22** *(borné)* · **D13**. ⚠️ **La dérive subsiste et coûte un tour de FAIL** — 📌 **mais l'alternative est P4 renversée.** ✅ **Sa formulation est caduque** : elle cite l'Extracteur, supprimé |
| **P12** | Les questions produit en aval sont assez rares pour arrêter la commande | **Écartée, pas définitivement** — 📌 **U10 traite l'intérieur du lot** ; 🔴 **la file au niveau du lot reste une optimisation réelle.** ⚠️ **Ce qui retient** : sauter un lot peut rendre ses fiches caduques, et une réponse produit peut envoyer au redécoupage. **A5 donne de quoi le mesurer** |
| **P13** | Tout le fichier produit tient dans un contexte | **Écartée** — **C4**. 🔴 **Deux plafonds distincts, pas un** : le Rédacteur en **écriture** à 300 blocs, la globale en **lecture**. 📌 **Le mode d'échec est une troncature silencieuse** — déjà rencontré une fois, chez le Convertisseur |
| **P14** | Une seule chaîne pour tout projet | 🔴 **Saine, et la plus structurante** — 📌 **c'est elle qui explique pourquoi les défauts du fichier de conventions comptent plus que leur taille**, et **le Product Owner l'a invoquée pour écarter l'outillage spécifique à une plateforme** |

### Ce que ça change

📌 **Deux corrections de formulation dans `PROCESS_AVAL`**, sorties de
la relecture des prémisses :

| Fichier | Ce qu'il faut |
|---|---|
| `docs/process/PROCESS_AVAL.md` | 🔴 **P10 est atténuée par D14** — ⚠️ **la formulation dit que la fiche se suffit à elle-même** ; **le Réalisateur lit aussi les conventions permanentes.** 📌 **Ce qui reste vrai : aucune architecture à décider** |
| `docs/process/PROCESS_AVAL.md` | 🔴 **P11 cite l'Extracteur**, supprimé de la chaîne — 📌 **le global naît maintenant du Fusionneur**, ce qui rend la prémisse plus solide : **plus aucun document ne naît du code** |

### Une règle pour la suite

🔴 **Tirée de P8** : **on scripte un geste mécanique dont une erreur
coûte cher** — 📌 **pas parce qu'il est mécanique.** ⚠️ **Deux artefacts
à tenir d'accord — la commande et son script — coûtent plus qu'ils ne
rapportent quand l'erreur est bénigne.**

---

# Q — Ce que seuls les agents pouvaient trancher (section 7)

📌 **Les vingt-quatre questions que le verdict laissait ouvertes**, la
phase 2 n'ayant lu que les PROCESS. 🔴 **Toutes ont été répondues en
ouvrant les fichiers.**

| # | La question | La réponse |
|---|---|---|
| 1 | Le Découpeur marque-t-il les blocs qu'il crée ? | ✅ **Oui** — `NEW`, et `MODIFIED` sur celui qui garde le titre. **D4 clos** |
| 2 | Le Réalisateur lit-il tout le fichier de conventions ? | 🔴 **Les deux, et c'est la contradiction** — *« applique tout »* et *« tiens ce que la fiche nomme »*. **D12 → D14** |
| 3 | Le Cadreur lit-il `CURRENT_TECHNICAL_STATE.md` ? | ✅ **Non** — il tranche par grep. **D21 : la phrase du PROCESS était fausse, corrigée** |
| 4 | L'invocation 1 de l'Architecte : par projet ou par fonctionnalité ? | 🔴 **Par fonctionnalité, et elle écrase** — **Rupture 5**, tranchée : une invocation incrémentale |
| 5 | Où vit l'inventaire des symboles du Cadreur ? | ✅ **Dans `code/decoupage.md`**, que le Vérificateur lit. **D18 clos** |
| 6 | Les identifiants de bloc sont-ils stables ? | ✅ **Oui**, énoncé chez le Rédacteur **et** le Découpeur. **D2 clos** |
| 7 | Que fait le Rédacteur d'une réponse confirmative ? | 🔴 **Rien** — aucune ligne de sa table ne couvre le cas. **D3 : réglé en amont par A6** |
| 8 | Le Relecteur compare-t-il l'assertion au critère ? | ✅ **Oui** — *« apparié sur ce que le test affirme, jamais sur son nom »*. **F1 renversé : il reste** |
| 9 | Signale-t-il un symbole ou une branche qu'aucun critère ne demande ? | ⚠️ **Partiellement** — 📌 **son point 5 attrape le code mort du lot**, mais exclut *« ce que rien n'utilise »*. 🔴 **Ce qui échappe : du code qui fait plus que le critère et qui sert** |
| 10 | Le texte hors blocs est-il sondé ? | 🔴 **Non** — mais **D9 : le verdict s'était trompé d'artefact**, les dépendances voyagent par les marques *existing*, dans les blocs |
| 11 | Qui écrit dans `cadrage-produit/closed/` ? | ✅ **`/4_grille`**, six fichiers par tour, par `git mv`. **D7 clos** |
| 12 | Qui lit `[integrated: B7]` ? | ✅ **Personne** — **D5 : la marque est retirée** |
| 13 | Renommer ou supprimer un blocage tranché ? | 🔴 **Les deux se disaient** — **D17 : les cinq agents renomment désormais** |
| 14 | Le Contrôleur lit-il les fiches d'un `bugfix-NN/` ? | ✅ **Non** — **D23 : on n'étend pas.** 📌 **Mais `/9_controle` tourne sur les deux** *(A5)* |
| 15 | Deux natures qui nomment un concept de deux façons : trancher ou demander ? | 🔴 **D10, tranché** : deux routes, la technique boucle sur le Convertisseur |
| 16 | Un Réalisateur neuf retire-t-il ce que la tentative échouée avait écrit ? | 🔴 **Non** — **D22 : corrigé**, il grepe les symboles du lot avant d'écrire |
| 17 | Y a-t-il une borne au Cadreur qui rebloque après un refus ? | 🔴 **Non** — **U11 : un refus arrête `/7_lots`** |
| 18 | `/8_code` construit-elle les groupes du Contrôleur ? | ✅ **Elle ne l'invoque pas** — **D20 : sa contradiction interne corrigée** |
| 19 | La globale refait-elle la passe A, ou réutilise-t-elle les angles ? | ✅ **Elle relève elle-même**, sans questionner. **D6 : le recouvrement est une relecture, pas une passe A** |
| 20 | La table mécanique/revue est-elle lue par une commande qui câble ? | ✅ **Non** — **D14 : la seconde table est retirée** |
| 21 | Le Détailleur re-parcourt-il le bloc avant de réécrire des fiches ? | ✅ **Oui** — *« écrire une fiche avant d'avoir parcouru tout le bloc »* est dans ses interdits, **sans exception**. Le risque du verdict est écarté |
| 22 | Le Réalisateur écrit-il ses tests avant ou après les corps ? | 🔴 **Après** — **A3 : les tests passent à un contexte qui n'a jamais vu de corps** |
| 23 | Un agent compare-t-il le fichier produit entre deux tours ? | ✅ **Oui, `/6_convertit`**, par octets — 📌 **mais par nature, pas par bloc.** **P5 : piste identifiée, sans cas** |
| 24 | L'invocation 3 consigne-t-elle le lot codé avant la règle ? | ✅ **Oui, par deux chemins** — le nom du fichier de demande et le `## Requests` de la fiche. **D16 : une ligne ajoutée à `audit_conventions`** |

📌 **Aucune question ne reste ouverte.** 🔴 **Sur vingt-quatre, le
verdict s'est trompé sept fois** — toujours parce qu'il ne lisait que
les PROCESS : **D2, D4, D6, D7, D8, D9, D18**. ⚠️ **Ce n'est pas un
défaut du verdict, c'est ce que son cadrage lui imposait** — 📌 **mais
ça dit que les PROCESS sont moins précis que les agents.**

---

# Où voir ce qui a été passé

📌 **`modifications.md`** — 🔴 **une section par fichier de la chaîne** :
ce qui a changé, la fiche de passe *(passés, écartés, reportés)*, et la
demande d'origine de chaque modification.

⚠️ **Ce fichier-ci porte les décisions** ; **l'autre porte ce qui en a
été fait.**
