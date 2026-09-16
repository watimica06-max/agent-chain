# Ce qui a été passé dans la chaîne — par fichier

> 📌 **Tout est fait.** 🔴 **Ce fichier est l'index de la
> vérification** — ⚠️ **il n'est pas la référence** : il dit ce que
> j'affirme avoir fait, et c'est précisément ce qu'on contrôle.
>
> **Les références sont `sujets.md`** *(les décisions)* **et
> `refonte/passes/<agent>.md`** *(les défauts)*.

## Comment lire une section d'agent

| | |
|---|---|
| **Ce qui a changé** | 📌 **Une table** — chaque modification et le fichier qu'elle touche |
| **Sa fiche de passe** | 🔴 **Passés · Écartés · Reportés**, par numéro, avec la justification de chaque écarté |
| **La demande** | 🔴 **La spécification de chaque modification**, telle qu'elle a été écrite avant de la passer — 📌 **c'est contre elle qu'on vérifie** |

---

# `lexicographe.md`

✅ **FAIT** — 📌 **aucune modification du fichier de travail** *(sauf la
ligne `en anglais`, décidée en séance)*.

## Sa fiche de passe — 17 commentaires

📌 **Passés (14)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 ·
C11 · C12 · C13 · C14

🔴 **Écartés (2)** — C15 · C16

⚠️ **Reportés (1)** — C17

| # | Le sujet | Pourquoi |
|---|---|---|
| **C15** | Les deux comptes de `lexique.md` | 📌 **Devenu sans objet** — le comptage de `retenu` avait déjà été retiré ; un texte affiché n'en porte pas |
| **C16** | Sauter un balayage quand le fichier d'idées n'a pas changé | ⚠️ **Le lexique, lui, a changé** — et c'est une entrée du balayage. 📌 **La fiche se disait elle-même incertaine** |
| **C17** | Un balayage qui ne tient plus dans le contexte | 📌 **Reporté** — 🔴 **`## Relevé`, créé pour une autre raison, est déjà l'infrastructure du remède** : comparer le relevé au lieu du fichier. **Une ligne à changer le jour venu** |

---

# 🆕 `qualifieur.md`

✅ **ÉCRIT ET CÂBLÉ.** 📌 **L'agent, sa commande `/3a_genre`, et ses
cinq cascades sont passés dans la chaîne.**

**Ce qui a été fait, pour mémoire :**

| Fichier | Ce qui a changé |
|---|---|
| 🆕 `agents/qualifieur.md` | L'agent, sur la forme du Classeur |
| 🆕 `commands/3a_genre.md` | Sa commande, sur la forme de `/3b_nature` |
| `agents/redacteur.md` | 🔴 **Écrit `Genre:` vide** à côté de `Nature:`, aux deux endroits qui décrivent la forme d'un bloc |
| `agents/decoupeur.md` | 🔴 **Idem** — et il laisse les deux vides sur chaque moitié |
| `commands/3_decoupe.md` | Renvoie vers `/3a_genre`, aux deux endroits |
| `commands/3b_nature.md` | 🔴 **Ne garde que les blocs `Genre: comportement`** ; tourne entre `/3a_genre` et `/4_grille` |
| `agents/classeur.md` | 📌 **Sait que tout bloc qu'on lui nomme porte `Genre: comportement`** |
| `CLAUDE.md` | Inventaire, table des commandes, liste des `subagent_type` |

⚠️ **Deux règles ajoutées en écrivant, qui n'étaient pas prévues** :
🔴 **la raison d'une directive n'est pas une seconde directive** — *« des
chiffres à chasse fixe, pour qu'un chrono ne change jamais de largeur »*
explique la règle au-dessus, elle n'en est pas une ; 🔴 **un
comportement refusé n'est pas du hors-périmètre** — *« l'appui ne fait
rien »* est un comportement.

---

## La demande

📌 **Conservé ici pour pouvoir le relire sans ouvrir l'agent.** 📌 **Sa commande :
`/3a_genre`**, entre `/3_decoupe` et `/3b_nature`.

⚠️ **`3a` plutôt qu'une renumérotation** — 🔴 **l'insertion coûte une
ligne ; renuméroter coûterait une relecture de toutes les commandes et
de tous les renvois.**

## Son rôle

Il pose une ligne `Genre:` sur chaque bloc du fichier produit, entre le
Découpeur et le Classeur. **Rien d'autre.**

📌 **Pourquoi avant le Classeur** : seul un comportement a une nature.
Sans lui, le Classeur cherche une nature à des passages qui n'en ont
pas — et il en trouve une, faute de pouvoir dire non.

📌 **Pourquoi après le Découpeur** : un bloc y porte alors un seul
sujet, donc un seul genre. Une phrase qui portait deux genres a déjà
été scindée.

## Les six genres

| Genre | Ce que c'est |
|---|---|
| `comportement` | Ce que le produit fait, montre ou refuse |
| `directive` | Une contrainte technique que le Product Owner a tranchée — un moyen imposé, pas un comportement |
| `transverse` | Une règle dont **le sujet est une catégorie, pas un objet du produit** |
| `référence` | Un catalogue, un tableau de formats que des comportements citent |
| `hors périmètre` | Ce que le Product Owner écarte explicitement |
| `recette` | Ce qu'il veut vérifier lui-même sur l'appareil |

## Le test du genre `transverse`

🔴 **La règle peut-elle nommer le bloc qu'elle concerne ?**
**Oui → elle appartient à ce bloc. Non, parce qu'elle en concerne une
catégorie entière → transverse.**

| | |
|---|---|
| « Une absence s'affiche par un tiret » | Sujet : *une absence* — **transverse** |
| « Un repli n'est pas une erreur » | Sujet : *un repli* — **transverse** |
| « L'horloge ne se replie jamais » | Sujet : *l'horloge*, un objet — **pas transverse** |

⚠️ **Une section transverse du fichier d'idées ne contient pas que des
règles transverses.**

## Ses deux sorties de doute

| Le doute | Ce qu'il fait |
|---|---|
| **« Est-ce transverse ? »** | 🔴 **Dans le doute, `comportement`** |
| **« À quoi s'applique-t-elle ? »** — elle est transverse, mais sa formulation ne dit pas son périmètre | 🔴 **Une question obligatoire au Product Owner** |

🔴 **L'asymétrie doit être écrite dans l'agent** : une règle mal classée
en `comportement` coûte une question de trop ; mal classée ailleurs,
**elle quitte le fichier des comportements et n'est plus jamais
sondée** — un trou silencieux.

⚠️ **Le second doute ne se règle pas par l'asymétrie** : classer en
`comportement` ne donne pas de déclencheur à la règle. 📌 **La réponse
ne modifie pas le produit, elle reformule la règle** — *« le repli
s'applique partout »* devient *« toute valeur qu'un capteur ne fournit
pas s'affiche en repli »*.

## Son fichier de questions

📌 **Même mécanique que les autres agents du cycle** : écrit à chaque
passage, même vide. Vide → on passe ; non vide → retour à
`/1_lexique`.

---

# `redacteur.md`

## La demande

### 1. Transmettre le rattachement au global

🔴 **Il grepe déjà l'index du global pour ranger chaque bloc.** Cette
information — *ce bloc se rattache à une section existante, ou non* —
**meurt dans son contexte. Elle doit survivre dans le fichier
produit.**

📌 **C'est un ajout à ce qu'il écrit, pas un geste de plus.**

⚠️ **Pourquoi** : la grille doit fermer un bloc qui modifie l'existant
**avec la section du global sous les yeux**. Sans ce marquage, elle ne
sait pas lesquels le nécessitent.

**La forme** — 🔴 **une ligne `Global:` sur le bloc**, à côté de
`Genre:` et `Nature:` :

    ### B12 — Le bouton Pas
    Genre: comportement
    Nature: presentation
    Global: ## Activity screen

🔴 **La section du global, pas le bloc** — 📌 **même si l'index en porte
les titres.** **Trois raisons** : **c'est la section qui répond aux
questions de la grille** — *où se place le bouton, dans quels états
apparaît-il* — et la réponse est dans l'écran entier ; ⚠️ **un titre de
bloc est plus volatil qu'un titre de section**, le Fusionneur peut le
renommer à l'`INSERT` ; 📌 **et le Sondeur charge par section de toute
façon.**

🔴 **La ligne est absente quand le bloc ne se rattache à rien** — ⚠️
**absente, jamais vide** : une ligne vide se lirait comme un
rattachement oublié.

⚠️ **Le rattachement ne tient pas à la réutilisation d'un titre** — 📌
**une section neuve du fichier de fonctionnalité qui porte le même titre
qu'une section du global est un rattachement**, et la ligne le dit.

## 2. Un défaut sans réponse écrite vaut acceptation

🔴 **Une question de niveau *défaut* porte une réponse pré-remplie et sa
citation.** Le Product Owner n'écrit que s'il n'est pas d'accord.

📌 **À l'intégration : pas de réponse écrite → il intègre la
proposition** comme si elle avait été répondue.

## 3. Une règle transverse modifiée remarque tous les blocs

🔴 **Quand une réponse modifie une règle transverse, tous les blocs sont
marqués.**

⚠️ **Pourquoi** : les blocs qu'elle concerne n'ont pas bougé, donc ils
ne sont pas marqués, donc ils ne sont pas resondés — **et les défauts
proposés d'après l'ancienne version restent acquis.**

📌 **Brutal, mais l'alternative serait une table de correspondance
bloc ↔ règle transverse, qui n'existe pas.** Le cas doit être rare :
une règle transverse est écrite une fois et change peu.

## 4. Écrire la traduction anglaise dans le lexique

🔴 **Quand il rend un concept en anglais pour la première fois, il écrit
le mot retenu dans l'entrée `## Tranché` de ce concept**, sur une ligne
`en anglais :`.

    STATION — retenu
      remplace : atelier
      en anglais : station

🔴 **Quand l'entrée porte déjà un mot anglais, il le reprend** — il ne
choisit pas à nouveau.

⚠️ **Pourquoi** : 🔴 **rien ne garde aujourd'hui le mot qu'il a choisi.**
📌 **Deux intégrations peuvent rendre un même concept français par deux
mots anglais** — *course* → `race`, puis `run`. **Un second nom pour une
chose, créé après que le vocabulaire a été tranché**, et invisible à
l'invocation 3 du Lexicographe, qui n'ouvre jamais le fichier produit.

**Les trois cas, et rien d'autre :**

| Le concept | Ce qu'il fait |
|---|---|
| Au lexique, avec un mot anglais | 🔴 **Il le reprend** |
| Au lexique, sans mot anglais | 📌 **Il traduit et écrit la ligne** — celle-là seulement |
| **Absent du lexique** | 🔴 **Il traduit et n'écrit rien** |

🔴 **Il n'ajoute jamais d'entrée au lexique.** ⚠️ **Un terme que le
Lexicographe n'a pas relevé n'y a pas sa place** — 📌 **sinon le
Rédacteur devient un second juge du vocabulaire, et le lexique gonfle de
termes que personne n'a balayés.**

📌 **Et ça ne laisse pas de trou** : l'invocation 3 du Lexicographe
ajoute désormais à `## Relevé` les termes qu'une réponse apporte.
**Tout concept du fichier produit vient du fichier d'idées ou d'une
réponse**, et les deux sont relevés.

⚠️ **Une entrée de plus dans sa liste d'écritures** — 🔴 **cette ligne,
et elle seule.**

✅ **Déjà écrit côté Lexicographe** : la ligne `en anglais` est dans la
forme du lexique, avec la mention qu'elle appartient au Rédacteur et que
le Lexicographe n'y touche jamais.

## 5. Une invocation de plus — `desc-produit-fusion.md`

🆕 **Une troisième invocation**, lancée par `/fusion`, **tout à la fin,
après tous les cycles de correction.**

**Elle lit** : `desc-produit.md`, et les N fichiers de décisions produit
rendus par `/9_controle` — celui du cycle principal, puis `bugfix-01`,
puis `bugfix-02`.

**Elle écrit** : `desc-produit-fusion.md` — une copie enrichie,
**sans aucun marqueur**, dont le seul lecteur est le Fusionneur.

🔴 **Dans l'ordre des cycles** : le fichier produit d'abord, puis chaque
fichier de décisions amendant l'état obtenu. 📌 **Une seule
invocation**, pour qu'il arbitre les contradictions entre cycles.

🔴 **Aucune décision à intégrer ? Il écrit quand même le fichier, copie
conforme.** ⚠️ **Sinon le Fusionneur devrait choisir sa source.**

📌 **Placement d'une décision** : dans presque tous les cas elle
complète un bloc existant — c'est le travail ordinaire de son
invocation 2.

⚠️ **`desc-produit.md` n'est jamais modifié** — c'est ce qui permet à
cette invocation de tourner après le découpage sans violer l'interdit
de `/6_convertit`.

---

## Sa fiche de passe — 18 commentaires

📌 **Passés (15)** — C1 · C2 · C3 · C4 · C6 · C7 · C8 · C9 · C10 · C11 ·
C12 · C13 · C14 · C15 · C16

🔴 **Écartés (3)** — C5 · C17 · C18

⚠️ **Reportés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **C5** | La marque `[integrated:]` posée sur chaque entrée | 🔴 **Caduc** — la marque a été retirée de la chaîne *(D5)* : personne ne la lisait, et lui donner un lecteur aurait fait d'une case à remplir une incitation à certifier un travail non fait |
| **C17 · C18** | Le routage de `cycle.md` | ⚠️ **`cycle.md` est périmée** et ne doit pas être traitée — décision du Product Owner |

---

# `classeur.md` · `decoupeur.md`

✅ **FAIT** — voir la table du Qualifieur.

✅ **La vérification est faite** : sa règle disait déjà qu'un catalogue
est un bloc à part, mais **ses gestes n'avaient aucun réceptacle** pour
les phrases que rien ne déclenche. 🔴 **Corrigé** — le geste 1 en fait
une liste, le geste 2 en fait un bloc.

📌 **Les deux agents sont terminés**, fiche de passe comprise.

---

## La fiche de passe du Découpeur — 17 commentaires

📌 **Passés (13)** — C2 · C3 · C5 · C6 · C7 · C8 · C10 · C11 · C12 ·
C13 · C14 · C15 · C16

🔴 **Écartés (3)** — C4 · C9 · C17

⚠️ **Reportés (1)** — C1

| # | Le sujet | Pourquoi |
|---|---|---|
| **C4** | Retirer de l'agent l'arrêt sur `Clarification needed` | 🔴 **Ce n'est pas un filet, c'est un périmètre différent** — la commande grepe **tout le fichier**, l'agent regarde **ses blocs**. 📌 **Et si la commande change, l'agent tient encore** |
| **C9** | Ce que deviennent les autres blocs quand un bloque | 📌 **Vrai, mais marginal** — ⚠️ **avec une seule cause de blocage désormais, le cas est rare** |
| **C17** | Comparer le fichier produit entre deux tours | 🔴 **C'est P5**, écarté : aucun cas observé, et une comparaison d'octets ne dit pas **quels** blocs ont bougé |
| **C1** | L'ordre des sections de la commande | ⚠️ **Reporté au `todo.md`** — 🔴 **les neuf commandes du cycle partagent cette structure**, en corriger une seule créerait deux formes |

## La fiche de passe du Classeur — 14 commentaires

📌 **Passés (13)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C11 ·
C12 · C13 · C14 — 🔴 **tous appliqués en double sur le Qualifieur**,
qui copie sa forme

🔴 **Écartés (0)**

⚠️ **Partiellement passés (1)** — C10

| # | Le sujet | Ce qu'on en a gardé |
|---|---|---|
| **C10** | Retirer du rapport ce qu'il a questionné | 🔴 **Son point principal contredit C11**, qui a raison : **personne en aval n'attrape une nature fausse** — vérifié, le Sondeur ignore jusqu'à l'existence de la nature. 📌 **Son point secondaire retenu** : le rapport nomme les blocs questionnés, **pas pourquoi** — le fichier de questions le porte |

---

# `sondeur.md`

✅ **FAIT** — 📌 **les cinq modifications, la fiche de passe *(18
commentaires sur 22)*, la grille du temps 2 et l'invocation *Existant*
sont passées.**

**Ce qui a changé, pour mémoire :**

| Fichier | Ce qui a changé |
|---|---|
| `agents/sondeur.md` | Deux listes de blocs · le rapprochement transverse · les deux niveaux de question et la forme `Défaut:` · 🆕 **invocation 3 — *Existant*** |
| 🆕 `docs/process/GRILLE_EXISTANT.md` | La grille du temps 2 — E1 à E4 |
| `docs/process/GRILLE_CADRAGE_PRODUIT_V2.md` | *The two levels of a question* |
| `commands/4_grille.md` | Deux greps sur `Genre:` · les deux listes dans les quatre prompts · 🆕 **le second temps**, son déclenchement, son invocation, son routage |
| `agents/decoupeur.md` | 🔴 **Porte la ligne `Global:` sur chaque moitié** — ⚠️ **trouvé à la vérification** : sans ça, une moitié n'est jamais vue par le second temps |

⚠️ **Deux commentaires écartés** : l'identifiant de grille dans les
questions *(l'Assembleur déduplique par le sens, pas par la
formulation)* et la grille lue par section *(marginal, et l'en-tête
commun se perdrait)*.

---

## La demande

## 1. Ne sonder que les comportements

🔴 **Les blocs dont le `Genre:` n'est pas `comportement` ne sont pas
sondés.**

📌 **Il ne filtre pas lui-même** — ⚠️ **`/4_grille` lui nomme les blocs
à sonder**, comme `/3b_nature` le fait pour le Classeur. 🔴 **Il lit
`desc-produit.md`**, jamais un fichier de partage : **le partage tourne
après la boucle, quand le fichier est figé.**

## 2. Charger les règles transverses en contexte

🔴 **En plus de ses blocs, il charge les blocs `Genre: transverse`** —
📌 **`/4_grille` les lui nomme aussi**, par le même grep.

📌 **Il ne les sonde pas.** Elles servent au rapprochement : quand une
question de grille se pose sur un bloc, il regarde si une règle
transverse y répond déjà.

🔴 **Le rapprochement se fait au moment de la question** — **aucune
table de correspondance, aucun marquage bloc par bloc.** Une règle
transverse porte son périmètre dans sa formulation.

## 3. Écrire un défaut avec sa citation

🔴 **Trois cas au lieu de deux :**

| Ce que dit le corpus | Ce qu'il écrit |
|---|---|
| Il répond directement | **Rien** |
| Rien n'y répond | Une question **obligatoire** |
| Il n'y répond pas ici, mais une règle transverse ou un motif déjà suivi donne la réponse | Une question **défaut** |

🔴 **Une question *défaut* porte sa réponse pré-remplie et la référence
du paragraphe qui la fonde.** Le silence vaut acceptation.

⚠️ **Le volume ne monte pas, il se répartit** — une question déjà réglée
n'est toujours pas posée.

## 4. Deux règles qui divergent

| Le cas | Ce qu'il fait |
|---|---|
| **Transverse contre transverse**, sur un même bloc | 🔴 **Une question obligatoire, jamais un défaut** |
| **Transverse contre une règle du bloc** | 📌 **Le bloc l'emporte** — il est plus précis. Aucun défaut à proposer |

## 5. Lire le global, au temps 2 seulement

🔴 **Son interdit de lecture s'ouvre pour le second temps de
fermeture** — et **seulement pour les sections du global que ses blocs
touchent**, jamais le fichier entier.

🔴 **Une invocation dédiée** — 📌 **une troisième, à côté de l'angle et
de la globale** : *Existant*.

⚠️ **Pourquoi pas les trois angles** : leurs trois ordres de lecture
n'ont aucun sens ici — **il n'y a qu'un corpus à croiser**, et ce serait
trois fois la même lecture du global.

⚠️ **Pourquoi pas la globale** : elle relève **tous** les blocs ; le
temps 2 n'en touche qu'une partie. **Deux jeux de règles dans une
invocation.**

🔴 **La vraie raison** : **le temps 2 ne se déclenche pas au même
moment.** 📌 **Il démarre quand le temps 1 a rendu un fichier vide** —
donc quand les quatre autres invocations ne tournent plus. ⚠️ **Le loger
dans une invocation existante lui donnerait une condition de
déclenchement différente de celle de son hôte.**

**Ce qu'elle lit** : les blocs portant une ligne `Global:`, et les
sections du global qu'ils nomment. 📌 **Rien d'autre.**

**Ce qu'elle écrit** : son propre fichier de questions. ⚠️ **Pas de
fusion** — l'Assembleur ne fusionne que les quatre du temps 1.

---

## Sa fiche de passe — 22 commentaires

📌 **Passés (18)** — C1 · C3 · C4 · C5 · C6 · C7 · C8 · C11 · C12 · C13 ·
C14 · C15 · C16 · C17 · C18 · C19 · C20 · C22

🔴 **Écartés (3)** — C2 · C9 · C21 *(caduc)*

⚠️ **Reportés (1)** — C10

| # | Le sujet | Pourquoi |
|---|---|---|
| **C2** | Lire la grille par section | 📌 **La grille est bien sectionnée par passe**, mais ⚠️ **le gain est de ~4 Ko** contre le risque de sauter l'en-tête commun. 🔴 **Piste notée si la grille double de taille** |
| **C9** | Un champ portant l'identifiant de grille | 🔴 **L'Assembleur déduplique par le sens, pas par la formulation** — vérifié dans son fichier. ⚠️ **Deux angles trouvent le même trou par deux questions de grille différentes** : comparer les identifiants les séparerait à tort |
| **C10** | L'ordre des sections de la commande | ⚠️ **Reporté au `todo.md`**, avec les neuf commandes |
| **C21** | Le routage de `cycle.md` | 📌 **Périmée** |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C1 · C22** | 🔴 **Un angle ne lit plus que les blocs qu'on lui nomme** — ⚠️ **il lisait le fichier produit entier pour n'en sonder que quelques-uns**, alors que sa propre règle dit qu'une question de passe A tient sur son bloc seul |
| **C7** | 🔴 **« Ne s'applique pas » n'avait aucun test** — 📌 **c'est la seule sortie qui écarte une question sans rien écrire**, et un trou qui part par là ne revient jamais |
| **C8** | 🔴 **Un trou de passe A nomme un seul bloc** — ⚠️ **deux angles écrivaient le même trou comme `B9` et `B7, B9`**, et la fusion gardait les deux |
| **C17** | 🔴 **Une reprise après blocage n'invoque que la lecture bloquée** — 📌 **trois invocations Opus étaient refaites sur un fichier produit inchangé** |
| **C6** | 🔴 **La grille possède la liste des colonnes du relevé** — ⚠️ **l'agent la redisait**, et `A1.9` a dû être ajouté aux deux endroits |
| **C19** | 🔴 **Le fichier de questions est copié, jamais réécrit** — ⚠️ **la commande renumérotait et retirait une section d'un fichier qu'elle n'a pas le droit de lire** |

---

# 🆕 La grille du temps 2

✅ **ÉCRITE** — `docs/process/GRILLE_EXISTANT.md`, quatre sections :
**E1** ce que le bloc prend et qui est déjà pris · **E2** ce qu'il dit
et que la section dit autrement · **E3** ce que la fonctionnalité
retire sans le dire · **E4** le test de clôture.

⚠️ **Cinq de ses sept questions n'ont aucun cas observé** — voir
`todo.md`, *les cinq questions non fondées*. 🔴 **À retirer si le
premier cycle n'en déclenche aucune.**

✅ **`C1.3` de la grille V2 en est sortie** — *« pour chaque règle
existante que la fonctionnalité touche : conservée, changée,
retirée ? »*. 📌 **Le Sondeur ne pouvait pas y répondre**, il ne lisait
pas le global. **Devenue `E3.1`**, et `C1.4` à `C1.7` renumérotées.

---

## La demande

🔴 **Elle ne cherche pas ce que la fonctionnalité laisse ouvert** —
c'est le travail de la grille de cadrage. **Elle cherche ce qu'elle
heurte :**

- une place, un nom, une ressource **déjà occupés** ;
- une règle qui en **contredit** une existante ;
- **et l'inverse** : ce que la fonctionnalité retire sans le dire.

📌 **Sa forme est celle de la passe B de la grille de cadrage**, sur un
autre corpus : au lieu de croiser les blocs entre eux, elle croise les
blocs de la fonctionnalité avec les sections du global qu'ils touchent.

**Le cas d'école** : le bouton va en bas à droite, et le global dit
qu'il y a déjà un bouton en bas à droite. 🔴 **La question est un
arbitrage** : que deviennent les deux ?

📌 **Les réponses deviennent des blocs du fichier de la fonctionnalité**,
y compris ceux qui décrivent ce que devient l'existant. Le Fusionneur
les portera au global.

---

# `assembleur.md`

✅ **FAIT** — 📌 **aucune modification du fichier de travail ; sa fiche
de passe est entièrement passée (8 sur 8).**

| Ce qui a changé | |
|---|---|
| **La règle de départage** | 🔴 **On garde la question dont la réponse ferme l'autre**, jamais la plus étroite — ⚠️ **son propre exemple était le contre-cas** |
| **Une question multi-blocs** | 🔴 **N'est écartée que contre une jumelle qui nomme tous ses blocs** — sinon un bloc disparaît du fichier |
| **La forme d'entrée** | 📌 **Dite en entier**, ligne `Défaut:` comprise — ⚠️ **et un défaut ne migre jamais vers la question gardée** |
| **Ce qui l'arrête** | 🔴 **Une question qu'il ne peut pas placer, un fichier qui n'est pas une liste de questions** — 📌 **jamais un choix silencieux** |
| **Ses outils** | `Read, Write` — ⚠️ **`Grep` et `Glob` retirés** : ils ouvraient l'accès à `closed/` |
| **Le `## Merge`** | 📌 **Sort du fichier de questions, va dans son rapport** — 🔴 **son seul lecteur devait l'en retirer** |
| `commands/4_grille.md` | 🔴 **Les blocages sont contrôlés avant la fusion** · **une reprise sur son blocage relance la fusion seule** |

---

## Sa fiche de passe — 8 commentaires

📌 **Passés (8)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8

🔴 **Écartés (0)**

⚠️ **Partiellement passés (0)**

---

# `convertisseur.md`

## La demande

### 1. Recevoir les fichiers du partage

| Ce qu'il reçoit | Quelle invocation |
|---|---|
| **Les transverses** | 🔴 **Toutes les invocations de nature** — elles en tirent leurs entrées et leurs lignes de préambule |
| **Les références** | L'invocation transversale — section Text |
| **Le hors-périmètre** | L'invocation transversale — préambule |

⚠️ **Sans ça, le partage casse un chemin qui marche aujourd'hui** :
une règle transverse est actuellement un bloc comme les autres, donc
rangée sous une nature, donc lue. Après le partage, elle quitte le
fichier des comportements.

📌 **La section Text n'est alimentée par personne aujourd'hui** — elle
est écrite à partir des libellés cités dans les écrans, jamais à partir
d'un catalogue. **Le fichier des références lui donne sa source.**

## 2. Une règle transverse se scinde en deux

🔴 **Il sait déjà le faire** — son test : *si personne ne l'écrit, le
code manque-t-il quelque chose ?*

| Ce que la règle donne | Où ça va |
|---|---|
| **Le morceau de code partagé** — un formateur : une fonction qui prend une valeur absente et rend ce qu'il faut afficher | 🔴 **Une entrée numérotée** |
| **La contrainte « tout bloc soumis à ça l'applique »** | 📌 **Le préambule** |

⚠️ **Sans l'entrée numérotée, le Cadreur n'a rien à découper**, et le
formateur n'existe pas.

## 3. Un second fichier de questions, techniques

🆕 **Il peut écrire deux fichiers par exécution :**

| Le fichier | Ce qu'il porte |
|---|---|
| `questions-convertisseur-NN.md` | Les questions **produit** |
| 🆕 **Un fichier de questions techniques** | 🔴 **Au nom hors du motif `questions-*.md`**, pour que la boucle longue ne le détecte pas |

🔴 **La frontière : la réversibilité.**

> **Un choix qui peut être défait plus tard sans toucher au produit se
> tranche seul. Un choix qui, une fois pris, contraint ce que
> l'application pourra faire, se pose.**

| | |
|---|---|
| **Il tranche** | Renommer un symbole · ranger une règle dans une section plutôt qu'une autre · choisir une comparaison |
| **Il pose** | 🔴 **Décider que deux concepts que le Product Owner distinguait n'en font qu'un — ou l'inverse** |

📌 **La réponse à une question technique ne s'écrit nulle part** : elle
est appliquée à la réécriture de la section.

⚠️ **La frontière n'est calibrée par aucun cas réel.** 📌 **À regarder au
premier cycle** : zéro question technique, on aura construit pour rien ;
cinquante, on resserre.

---

## Sa fiche de passe — 20 commentaires

📌 **Passés (19)** — c.1 · c.2 · c.3 · c.4 · c.5 · c.6 · c.7 · c.8 ·
c.9 · c.11 · c.12 · c.13 · c.14 · c.15 · c.16 · c.17 · c.18 · c.19 ·
c.20

🔴 **Écartés (1)** — c.10

⚠️ **Partiellement passés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **c.10** | Lire la grille par groupe | 📌 **La grille est sectionnée** *(`# By nature`, `# Across sections`)*, mais ⚠️ **l'en-tête et `# Running it` sont communs** : un agent qui lit « sa section » peut les manquer. 🔴 **Même raison que C2 chez le Sondeur** |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **c.14** | 🔴 **Tout arrêt fusionne d'abord** — ⚠️ **sept natures avaient écrit leurs sections dans le worktree**, et un *« go no further »* les perdait toutes, le fichier de blocage compris |
| **c.1** | 🔴 **La branche « Non » est rencontrée en écrivant, pas après** — 📌 **l'agent écrivait une section entière pour la détruire**, et laissait des notes nommant des entrées disparues |
| **c.15** | 🔴 **Une nature dont l'entrée n'a pas bougé attend, elle ne tourne pas** — ⚠️ **elle relisait les mêmes blocs pour reposer la même question** |
| **c.6 · c.7** | 🔴 **L'invocation 2 lit le préambule et attend le geste 4 avant de questionner** — 📌 **elle posait une question dont elle écrivait la réponse un geste plus tard** |
| **c.2** | 🔴 **Une règle d'une autre couche ne devient jamais une entrée** — 📌 **et la question porte sur ce que la règle fait**, pas sur la couche, que le Product Owner ne peut pas arbitrer |
| **c.8** | 🔴 **Le préambule a quatre titres fixes** — ⚠️ **le Cadreur devait le distinguer des sections**, et l'Architecte y trouver les dépendances |

---

# `architecte.md`

✅ **FAIT** — 📌 **les six modifications du fichier de travail, et sa
fiche de passe (27 sur 28).**

| Ce qui a changé | |
|---|---|
| **Les directives** | 🔴 **`par-genre/directives.md`, lu aux invocations 1 et 4** — 📌 **jamais questionné**, et ses mots l'emportent en cas de fusion. ⚠️ **Une règle qui le contredit : la directive gagne, et il le dit** |
| 🆕 **Invocation 4 — *Completing*** | 🔴 **Le fichier existe : elle le lit, balaie la grille, n'ajoute que ce qu'il ne couvre pas.** 📌 **Compléter : automatique. Remplacer : signalé** — ⚠️ **tout le code déjà écrit suit l'ancienne règle** |
| **Le marquage** | 🔴 **`permanente` ou `spécifique` sur chaque règle** — 📌 **lui seul sait ce qui déclenche une règle** |
| **`couverture.md`** | 🔴 **Seconde table retirée** — 📌 **le genre de test vit sur la règle elle-même**, là où son lecteur est. ⚠️ **La colonne `N` était indéfinie : c'est la nature de l'entrée** |
| **Les genres de manque** | 🔴 **Quatre au lieu de trois** : couverture · conjonction · **incohérence du corpus** *(la réponse corrige le document technique)* · précision. 📌 **Une couverture est marquée question produit, jamais transformée en règle** |
| **Une réponse insuffisante** | 🔴 **Donne un nouveau fichier de questions** — 📌 **et c'est ce qui borne la boucle** |
| `commands/conventions.md` | 🔴 **Huit lignes de routage**, un état terminal, le test sur `couverture.md`, le commit avant le merge, le routage relayé |
| `commands/7_lots.md` · `8_code.md` | 📌 **Ce qu'un blocage de l'Architecte signifie**, et sa troisième place |

## Sa fiche de passe — 28 commentaires

📌 **Passés (27)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 ·
C11 · C12 · C13 · C14 · C15 · C16 · C17 · C18 · C19 · CMD1 · CMD2 ·
CMD3 · CMD4 · CMD5 · CMD6 · CMD7 · CMD8

🔴 **Écartés (1)** — C20

⚠️ **Partiellement passés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **C20** | Lire la grille par partie | 📌 **La grille est partitionnée**, mais ⚠️ **l'en-tête est commun** et le gain marginal. 🔴 **Même raison que C2 chez le Sondeur et c.10 chez le Convertisseur** |

⚠️ **Le plus grave était CMD1** : 🔴 **rien ne disait que le travail
était fini**, donc tout appel ultérieur retombait sur l'invocation 1 —
📌 **qui réécrit le fichier de zéro et perd chaque règle ajoutée
depuis.**

🔴 **Et C7 était critique** : la numérotation n'avait aucune règle. ⚠️
**Une fiche cite `R30`**, et une renumérotation aurait pointé chaque
citation vers une autre règle, sans que rien puisse le voir.

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **CMD1** | 🔴 **Rien ne disait que le travail était fini** — ⚠️ **tout appel ultérieur retombait sur l'invocation 1**, qui réécrit le fichier de zéro et perd chaque règle ajoutée depuis. 📌 **Huit lignes de routage, et un test sur `couverture.md`** |
| **C7** | 🔴 **La numérotation des règles n'avait aucune règle** — ⚠️ **une fiche cite `R30`**, et une renumérotation aurait pointé chaque citation vers une autre règle sans que rien puisse le voir |
| **C3** | 🔴 **Un quatrième genre de manque** — 📌 **une incohérence du corpus**, dont la réponse corrige le document technique et non le fichier de conventions |
| **C13** | 🔴 **Un outil qui vérifie ne disqualifie plus une règle** — ⚠️ **l'invocation 3 refusait comme « outillage » ce que l'invocation 1 écrivait** |
| **C5** | 🔴 **Un fait sur la plateforme se cherche, à toute invocation** — ⚠️ **l'invocation 1 le rappelait de mémoire**, et sa règle est lue par tous les lots |
| **C15** | 🔴 **Le fichier de conventions absent est un blocage** — 📌 **inventer un fichier d'une règle sans sections est ce que tous les lots liraient** |

---

## La demande

## 1. Recevoir le fichier des directives

🔴 **Une directive est une contrainte technique que le Product Owner a
tranchée.** Elle atteint l'Architecte **sans passer par le découpage en
blocs**, et **ne reçoit jamais de question.**

📌 **Exemple** : *« deux familles de police et pas d'autres, `font-data`
pour toute donnée chronométrée »*.

⚠️ **La contrepartie est pour le Product Owner** : une directive qu'il
juge fausse, il la change lui-même — personne ne la discutera.

**Quand il le lit** — 🔴 **à la dérivation et à l'invocation
incrémentale.** 📌 **La dérivation écrit le fichier, et une directive
est une contrainte de départ** ; ⚠️ **l'incrémentale aussi**, car une
fonctionnalité neuve peut apporter une directive sur un projet qui a
déjà ses conventions.

**Ce qu'il en fait** — 🔴 **le même travail d'intégration que pour
n'importe quelle règle**, avec ses cas :

| Ce qu'il trouve | Ce qu'il fait |
|---|---|
| **Une règle dit déjà la même chose** | 📌 **Rien** — la directive est satisfaite |
| **Une règle dit quelque chose de plus large ou de voisin** | 🔴 **Fusion** : la directive précise la règle, et **ses termes l'emportent** |
| **Rien ne la couvre** | 🔴 **Une règle neuve**, dans la section de grille qui convient |
| **Une règle la contredit** | 🔴 **La directive gagne** — ⚠️ **et il le dit** : sa grille a produit quelque chose que le Product Owner refuse |

📌 **En dérivation, beaucoup tomberont dans le premier cas** — il dérive
d'abord, puis intègre les directives. 📌 **En incrémentale, c'est de
l'intégration pure.**

🔴 **Il ne reformule pas ce que le Product Owner a tranché.** 📌 **Il
place, il fusionne, il identifie — il ne réécrit pas.** ⚠️ **S'il ne
peut pas placer une directive sans la changer, c'est une question.**

## 2. Une invocation incrémentale

🆕 **Quand `TECHNICAL_CONVENTIONS.md` existe déjà** : elle le lit,
balaie la grille, **et n'ajoute que ce que le fichier ne couvre pas.**

🔴 **L'interdit de lecture est restreint à l'invocation 1.** Sa raison —
*« relire serait dériver de sa propre sortie »* — vaut pour une première
dérivation, **pas pour les suivantes** : les règles ajoutées lot après
lot ne sont pas sa sortie libre, ce sont des demandes tranchées.

📌 **`couverture.md` pour la seule fonctionnalité.**

| Le cas | Ce qu'elle fait |
|---|---|
| **Compléter** — la règle ne couvrait pas ce que la fonctionnalité apporte | ✅ **Automatique** |
| **Remplacer** — l'ancienne disait X, la nouvelle dit Y | 🔴 **Signalé au Product Owner, jamais fait seul** |

⚠️ **Pourquoi remplacer ne peut pas être automatique** : tout le code
déjà écrit suit X, les fiches nomment l'ancienne règle, et le code neuf
suivrait Y. 📌 **Il signale : la règle en place, ce que la
fonctionnalité exige, et ce qui a été codé sous l'ancienne.**

## 3. Marquer chaque règle : permanente ou spécifique

🔴 **Chaque règle qu'il écrit porte son déclencheur.**

| | |
|---|---|
| **permanente** | Un geste ordinaire de code la déclenche, dans n'importe quel lot — un `await`, un accès disque, un `catch`, un identifiant écrit. **L'agent qui code est le seul à savoir que le geste va avoir lieu** |
| **spécifique** | Ce que ce lot fait en particulier la déclenche — un module, une frontière, une technologie. **Quelqu'un qui sait à quoi sert le lot peut la nommer d'avance** |

📌 **C'est lui qui sait ce qui déclenche une règle.**

## 4. Retirer la seconde table de `couverture.md`

🔴 **La table *règle → entrée de grille, mécanique ou revue* est
retirée.**

📌 **Personne ne la lit** — aucun agent, aucune commande ne câble ni ne
vérifie. ⚠️ **Et elle est fausse** : 22 liens sur 68 désignent la
mauvaise entrée.

📌 **Son seul contenu utile — mécanique ou revue — est déjà dans le
fichier de conventions**, où l'Architecte annote *« vérifié par
relecture, aucun outil ne fait ce contrôle »*. **Et il y est juste.**

✅ **La première table reste** : c'est son contrôle de balayage.

## 5. Séparer *couverture* et *conjonction*

🔴 **Aujourd'hui il les traite de la même façon.**

| | |
|---|---|
| **conjonction** | Une question qu'aucune grille ne pouvait voir — **légitime** |
| **couverture** | 🔴 **Un trou de la grille de cadrage** : le produit n'était pas fermé |

🔴 **Sur une couverture :** il la **marque comme question produit**,
distinctement des autres, **et ne la transforme jamais en convention, à
aucune invocation.**

📌 **Il poursuit son travail jusqu'au bout** — toutes ses questions,
toutes ses règles. ⚠️ **Rien ne bloque : le travail fait n'est pas
perdu.** Le Product Owner trie après.

⚠️ **Dans le doute entre *couverture* et *précision*, il pose** — le
coût d'une fausse alerte est une lecture, celui d'un faux négatif est un
comportement décidé hors produit.

## 6. Une réponse qui ne suffit pas

🔴 **Son invocation d'intégration a deux gestes : lire le fichier
répondu, et transformer chaque réponse en règle.** ⚠️ **Rien ne dit ce
qu'elle fait si une réponse ne lui suffit pas** — elle produira donc une
règle sur une réponse qui ne la fonde pas.

🔴 **À ajouter : une réponse qui laisse le choix ouvert donne un nouveau
fichier de questions, jamais vide.** 📌 **Même mécanisme que le
Lexicographe.**

📌 **Et c'est ce qui borne sa boucle** : elle s'arrête quand
l'intégration n'écrit pas de nouveau fichier.

---

# `fusionneur.md`

✅ **FAIT** — 📌 **ses deux modifications**, et ⚠️ **`commands/fusion.md`
avec elles.**

| Ce qui a changé | |
|---|---|
| **Sa source** | 🔴 **`desc-produit-fusion.md`**, jamais `desc-produit.md` |
| **À l'`INSERT`** | 🔴 **Il vérifie que le titre de la section couvre encore ce qu'elle contient** — 📌 **sinon, une question** : renommer une section du global est une décision produit. ⚠️ **Seulement les sections qu'il touche** |
| `commands/fusion.md` | 🆕 **Une ligne 10** : `desc-produit-fusion.md` absent → **Rédacteur, invocation 3**. 📌 **Avec l'ordre des cycles**, et la copie conforme quand il n'y a aucune décision |

⚠️ **Pas de fiche de passe** — 📌 **l'analyse ne l'a pas atteint**, comme
l'Arbitre.

---

## La demande

## 1. Lire `desc-produit-fusion.md`

📌 **Une ligne** : sa source devient `desc-produit-fusion.md` au lieu de
`desc-produit.md`.

## 2. Vérifier le titre d'une section à l'`INSERT`

🔴 **Quand il ajoute un bloc à une section existante du global, il
regarde si le titre couvre encore ce qu'elle contient.** 📌 **Sinon,
une question au Product Owner** — renommer une section du global est une
décision produit.

⚠️ **Pourquoi** : le global se lit **uniquement par son index**. Un
titre qui a dérivé est une section que le Rédacteur n'ouvre jamais — il
croit le sujet absent, crée une section neuve, et le doublon entre au
global à la fusion suivante. 🔴 **Le défaut s'aggrave tout seul.**

📌 **Il est le seul à écrire dans le global, il a la section sous les
yeux, et il ne le fait que sur celles qu'il touche.**

---

# 🆕 `concepteur.md`

✅ **ÉCRIT** — 📌 **20 agents dans la chaîne.**

| Ce qu'il porte | |
|---|---|
| **Son geste** | 🔴 **Il écrit les déclarations de la fiche avec des corps vides, et il compile** — 📌 **puis il commite** |
| **Ce que ça prouve** | 🔴 **La signature tient dans le langage** — ⚠️ **aujourd'hui elle vit en prose, et une signature impossible est découverte par le Réalisateur au milieu de son travail** |
| **Ce qu'il lit** | 📌 **La fiche, les conventions `permanente` en entier**, et les fichiers que la fiche déclare |
| **Ce qu'il ne fait jamais** | 🔴 **Aucun corps, aucun test, aucune signature modifiée** — 📌 **une signature qu'il ne peut pas écrire est un blocage** |
| ⚠️ **Ajouté en écrivant** | 🔴 **Un corps vide lève *not implemented*, il ne retourne pas une valeur par défaut** — 📌 **sinon le test rouge du Testeur pourrait passer dessus** |
| **Son rapport** | `code/<lot>/conception.md` — 📌 **les symboles et leur fichier, la compilation, les fichiers touchés hors fiche** |

---

## La demande

**Par lot**, avant le Testeur et le Codeur :

- il nomme les symboles ;
- il écrit les fichiers d'interface **avec des corps vides** ;
- 🔴 **il compile** ;
- il commite.

⚠️ **Ce que ça prouve** : la signature tient dans le langage.
📌 **Aujourd'hui elle vit en prose dans la fiche, et rien ne la compile
avant le codage** — une signature impossible est découverte par le
Réalisateur au milieu de son travail.

## Pourquoi lui, et pas le Détailleur

🔴 **L'argument est le grain.** 📌 **Le Détailleur travaille par bloc** —
une série de lots d'un coup. **S'il écrivait les interfaces, il
produirait du code pour des lots qui ne seront codés que bien plus
tard**, et qu'un redécoupage peut supprimer entre-temps.

⚠️ **Sa règle existe pour ça** : *« tu n'as écrit aucune fiche à ce
stade — c'est ce qui fait qu'un retour au découpage ne coûte que la
lecture »*. 🔴 **Lui faire écrire du code détruirait cette propriété.**

📌 **Le Concepteur tourne par lot**, au moment où le lot est codé — et
l'interdit du Détailleur reste intact.

---

# 🆕 `testeur.md`

✅ **ÉCRIT.**

| Ce qu'il porte | |
|---|---|
| **Son geste** | 🔴 **Un test par critère d'acceptation**, contre des interfaces dont les corps n'existent pas |
| **Les deux vérifications** | 🔴 **Chaque nouveau test échoue** — 📌 **c'est ce qui dit qu'il affirme quelque chose** — **et chaque ancien passe** |
| **Quand l'un des siens passe** | 🔴 **Il le réécrit** — ⚠️ **il n'affirme rien, ou affirme ce qu'un corps vide satisfait déjà** |
| **Quand un ancien échoue** | 🔴 **C'est un blocage** — le Concepteur a cassé quelque chose |
| **Pourquoi lui** | 📌 **Un test écrit contre un corps déjà écrit affirme ce que ce corps fait**, pas ce que le critère demande. ⚠️ **Il n'a jamais vu le corps** |
| **La recette (A4)** | 🔴 **Une ligne par critère qu'aucun test ne peut exercer** — 📌 **ce qu'il faut regarder et ce qu'on attend, dans les mots du Product Owner.** 🔴 **Chaque ligne nomme l'état** dans lequel l'application doit être — ⚠️ **sans quoi la liste ne peut pas être ordonnée** |
| **Ce qui le fait bloquer** | 🔴 **Un critère qu'aucun test ni aucune ligne manuelle ne peut porter** — ⚠️ **jamais un critère seulement difficile** |
| **Son rapport** | `code/<lot>/tests.md` — 📌 **et tout critère figure soit dans `## Tests`, soit dans `## Criteria with no test`** |

⚠️ **La raison écrite dans l'agent** : *« tu es celui qui vient
d'essayer »* — 🔴 **c'est ce qui fait que la décision *testable ou non*
lui appartient**, et à personne d'autre.

---

## La demande

**Par lot**, après le Concepteur et avant le Codeur :

- il écrit **un test par critère d'acceptation**, depuis la fiche et les
  fichiers d'interface ;
- ⚠️ **il ne peut pas voir les corps — ils n'existent pas encore** ;
- 🔴 **il vérifie que chaque nouveau test échoue, et que les anciens
  passent.**

📌 **Ce que le test rouge prouve** : le test affirme quelque chose. **Un
test qui passe sur des corps vides n'affirme rien.** ⚠️ **Cas observé :
des tests qui ne vérifiaient rien.**

## Il écrit aussi la recette

🔴 **Une ligne par comportement qu'aucun test ne peut exercer** — un
rendu pur, une boîte de dialogue système, un capteur.

📌 **Ce qu'il écrit** : **ce qu'il faut regarder**, dans les mots du
Product Owner. ⚠️ **Pas *« vérifier B12 »*** mais *« ouvrir la liste
vide : un message dit de coller un résultat »*.

📌 **Il est le seul à savoir pourquoi un comportement n'est pas
testable : il vient d'essayer.** Et il l'écrit **avant le codage**, donc
la liste existe même si un lot échoue.

---

# `cadreur.md`

✅ **FAIT** — 📌 **aucune modification du fichier de travail** ; sa fiche
de passe est passée.

## Sa fiche de passe — 26 commentaires

📌 **Passés (25)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 ·
C11 · C12 · C13 · C14 · C15 · C16 · C17 · C18 · C19 · C20 · C21 · C22 ·
C23 · C24 · C25

🔴 **Écartés (1)** — C26

⚠️ **Partiellement passés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **C26** | Le routage de `cycle.md` | 📌 **Périmée** — décision du Product Owner |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C11** | 🔴 **`Modifies` mélangeait trois unités** — symboles, fichiers, lignes de manifeste. ⚠️ **Or la règle *deux lots ne touchent jamais le même symbole* s'y vérifie** : un fichier dans un lot et un symbole qu'il porte dans un autre était une collision invisible. 🆕 **Champ `Touches`** pour les fichiers qui ne déclarent rien |
| **C15** | 🔴 **Une ligne du geste 6 s'appuyait sur un ordre qu'elle ne produisait pas** — elle déclare maintenant le besoin qui le crée |
| **C2** | 🔴 **Il devait renommer son fichier de blocage sans avoir d'outil qui supprime** — 📌 **c'est la commande qui renomme** |
| **C9** | 🔴 **La taille d'un lot se mesurait en blocs, et celle d'un bloc en lots** — 📌 **le test est le nombre de symboles déclarés**, plafonné par couche |
| **C6** | 🔴 **La liste des blocages n'était pas la liste** — neuf cas, énoncés une fois, et **tous écrivent le fichier** |
| **C20** | 🔴 **Kotlin sorti des règles** *(`ViewModel`, Room, `when`)* — 📌 **c'est P14** |

⚠️ **Ce qui le concerne ailleurs** : 🔴 **A-6**, l'arrêt au troisième
redécoupage — 📌 **porté par `/8_code`**, pas par lui. **Son `## Ce qui
revient` devient ce que la commande relaie en s'arrêtant.**

---

# `verificateur.md`

✅ **FAIT** — 📌 **aucune modification du fichier de travail** ; sa fiche
de passe est passée.

## Sa fiche de passe — 25 commentaires

📌 **Passés (24)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 ·
C11 · C12 · C13 · C14 · C15 · C16 · C17 · C18 · C19 · C20 · C21 · C22 ·
C23 · C24

🔴 **Écartés (1)** — C25

⚠️ **Partiellement passés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **C25** | Le routage de `cycle.md` | 📌 **Périmée** |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C8** | 🔴 **Tout le protocole de reprise disparaît** — ⚠️ **son unique cause de blocage est une panne de l'étape précédente**, qu'aucune décision ne lève. 📌 **On demandait au Product Owner d'écrire une décision que personne ne lirait**, et le fichier n'a plus de `## Decision` |
| **C19** | 🔴 **Le redécoupage était archivé à chaque tour** — ⚠️ **aux tours 2 et 3 l'agent ne savait plus quels lots étaient codés**, et les réordonnait comme s'ils ne l'étaient pas. 📌 **Archivé au seul tour qui ferme la boucle**, et par la commande |
| **C6** | 🔴 **Les types de défaut ont un vocabulaire fermé** — onze mots. ⚠️ **Le Cadreur corrige *seulement les lots que les défauts nomment*** : un défaut qu'il ne peut ni situer ni classer coûtait un tour |
| **C5** | 🔴 **Ce qu'un lot codé est, pour chaque geste** — ⚠️ **un lot corrigeant un lot codé était un recouvrement au geste 1 et la forme attendue au geste 2** |
| **C1** | 🔴 **Il devait renommer trois fichiers sans outil qui supprime** — 📌 **et `Edit` lui était accordé sans qu'aucun geste ne l'utilise** |
| **C15** | 🔴 **Un trou n'est pas un cycle** — ⚠️ **un lot derrière un trou n'est jamais éligible non plus**, et l'ordre entier était vidé pour une marque manquante |

⚠️ **C17 a produit une correction chez le Cadreur** : 🔴 **les deux
agents portaient la même table de plafonds, avec des nombres
différents.** 📌 **Le Vérificateur compte les lots par bloc** ; **le
Cadreur compte les symboles d'un lot** — ⚠️ **la table en double est
retirée de chez lui.**

---

# `detailleur.md`

✅ **FAIT** — 📌 **sa modification (U10), et sa fiche de passe.**

| Ce qui a changé | |
|---|---|
| **U10 — le blocage à plusieurs entrées** | 🔴 **Un seul fichier, une entrée `## Blocking N` par arrêt** — 📌 **il va au bout de sa marche.** ⚠️ **L'Arbitre est appelé une fois**, et aucune décision n'est appliquée avant qu'il ait répondu |
| ⚠️ **Cascade** | 🔴 **L'Arbitre sait lire ce fichier** : il répond à chaque entrée, numérotées, sous un seul `## Decision` — 📌 **et les lit toutes avant d'en trancher une**, puisqu'une entrée dit souvent ce dont elle dépend |

## Sa fiche de passe — 21 commentaires

📌 **Passés (18)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 ·
C11 · C12 · C13 · C14 · C15 · C16 · C17 · C18

⚠️ **Reportés (3)** — C19 · C20 · C21

🔴 **Écartés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **C19 · C20 · C21** | Le bloc partiel, l'issue sans ligne, le Contrôleur | 📌 **Tous trois sur `/8_code`**, que **A3** va réécrire — 🔴 **à passer avec elle**, plutôt que de toucher deux fois la même commande |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C4** | 🔴 **La marche grepe désormais** — ⚠️ **deux de ses trois causes de blocage n'apparaissent qu'au grep**, qui tournait après les premières fiches : *« tu n'as écrit aucune fiche à ce stade »* était faux |
| **C10** | 🔴 **Un symbole qu'un lot d'un bloc *antérieur* devait produire et qui est absent du code est un blocage** — ⚠️ **ce lot est codé et relu** : le symbole n'existe pas, ou porte un autre nom |
| **C3** | 🔴 **Un lot qui porte déjà une fiche** — 📌 **`PASS` : jamais touché · sans `PASS` : il passe son tour**, car le lot suivant est peut-être sur le point d'en consommer la signature |
| **C13** | 🔴 **`## Dependencies` a son geste** — ⚠️ **aucun geste ne l'écrivait**, son contenu se déduisait des tables |
| **C7 · C12** | 🔴 **Le geste 2 sort de la boucle par lot** ; **le geste 5 ne tourne que sur ce que l'inventaire ne place pas** |
| **C17** | 🔴 **Kotlin sorti des exemples** — 📌 **c'est P14** |

⚠️ **Vérification demandée par le Product Owner, et elle a payé** :
🔴 **aucun champ de la fiche ne se déplace vers le Concepteur ou le
Testeur** — 📌 **ils consomment les signatures et les critères, ils ne
les produisent pas.** ⚠️ **Mais elle a révélé une erreur fraîche** : le
Concepteur lisait une section `## Symbols` de la fiche, **qui n'existe
pas** — le champ s'appelle `## Signatures`. 📌 **Corrigé dans les deux
agents neufs.**

---

## La demande

## 1. Un blocage à plusieurs entrées

🔴 **Il va au bout de sa marche, relève tout, et écrit un seul fichier
de blocage à plusieurs entrées.**

📌 **Sa mécanique le permet déjà** : *« tu n'as écrit aucune fiche à ce
stade — la marche vient avant les gestes »*.

📌 **Chaque entrée porte son manque et sa question** — ⚠️ **et, quand il
le voit, ce dont elle dépend** : *« celle-ci n'a de sens que si la
précédente est tranchée ainsi »*.

🔴 **Ce n'est pas une contrainte** : un arrêt reste un arrêt, et
plusieurs arrêts successifs sont légitimes quand le travail l'impose.
📌 **Mais c'est dommage de ne pas optimiser quand on peut.**

## Ce qui ne change pas

🔴 **Il n'écrit toujours pas de code.** 📌 **C'est le Concepteur qui
écrit les interfaces et les compile**, par lot — ⚠️ **parce que le
Détailleur travaille par bloc**, et qu'écrire du code pour des lots
qu'un redécoupage peut supprimer coûterait ce que sa règle protège.

---

# `realisateur.md`

✅ **FAIT** — 📌 **ses quatre modifications, et sa fiche de passe.**

| Ce qui a changé | |
|---|---|
| **1 — Réduit au codage** | 🔴 **Il remplit les corps jusqu'à ce que les tests passent** — 📌 **il ne nomme plus, ne déclare plus, n'écrit plus de test.** ⚠️ **Un test qu'il faudrait changer pour passer est un blocage** |
| **2 — Les conventions** | 🔴 **Les `permanente` en entier**, plus celles que la fiche nomme — 📌 **et l'emphase** : ce sont les plus importantes de tout ce qu'il lit |
| **3 — Avancer sur ce qui reste** | 🔴 **Il continue sur ce qui ne dépend pas du manque** — 📌 **il s'arrête quand plus rien n'est faisable.** ⚠️ **Un second manque s'ajoute au fichier, il ne le remplace pas** |
| **4 — Il piétine** | 🔴 **Deux tentatives de suite qui échouent pour la même raison** — 📌 **un fait observable, pas une durée** |

## Sa fiche de passe — 18 commentaires

📌 **Passés (11)** — C1 · C2 · C4 · C5 · C6 · C7 · C8 · C10 · C11 ·
C15 · C18

🔴 **Écartés (1)** — C9

⚠️ **Reportés (6)** — C3 · C12 · C13 · C14 · C16 · C17

| # | Le sujet | Pourquoi |
|---|---|---|
| **C9** | Un critère qu'aucun test ne couvre | 🔴 **Caduc avec A3** — 📌 **c'est le Testeur qui décide qu'un critère n'est pas testable**, et il le porte à la recette |
| **C3 · C12 · C13 · C14 · C16 · C17** | L'arbre sale, les trois reprises, le compteur de retries, le Contrôleur | 📌 **Tous sur `/8_code`**, que **A3** réécrit — 🔴 **à passer avec elle** |

📌 **C7 et C10 étaient déjà réglés** par les modifications 2 et 4.

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C1** | 🔴 **Sa liste blanche shell ne permettait aucun de ses propres gestes** — ⚠️ **ni renommer, ni supprimer, ni jeter un arbre de travail.** 📌 **`git mv` et `git restore` ajoutés** |
| **C5** | 🔴 **« stop and report » à ses trois déclencheurs de blocage** — ⚠️ **une régression notée au rapport n'arrête rien** : l'orchestration s'arrête sur un `blocked_*.md`, et le lot fusionnait avec |
| **C15** | 🔴 **Le retour au découpage se lit sur un fichier, jamais sur la prose d'une décision** — ⚠️ **sa branche la plus destructrice** *(« jette tout ce que tu as écrit »)* **tenait à une lecture de texte libre** |
| **C6** | 🔴 **Il grepe le document d'état par symbole** — 📌 **un piège classé sous un sujet et les entrées que son lot rend fausses** n'étaient dans aucune des deux sections ouvertes |
| **C4** | 🔴 **Le rapport devient un geste** — 📌 **neuf gestes au lieu de huit** |

---

## La demande

## 1. Réduit au codage

🔴 **Il remplit les corps jusqu'à ce que les tests passent.** 📌 **Il ne
modifie jamais un test.**

📌 **Ce qui lui est retiré** : nommer les symboles et écrire les
interfaces (le Concepteur), écrire les tests (le Testeur).

## 2. Ne plus lire tout le fichier de conventions

🔴 **Il lit les règles marquées `permanente`, en entier, plus celles que
la fiche nomme.**

⚠️ **Sa contradiction actuelle disparaît** : il dit aujourd'hui
*« applique `TECHNICAL_CONVENTIONS.md` à tout ce que tu écris »* **et**
*« la section `## Conventions` de la fiche nomme les règles »*.

🔴 **Avec l'emphase** : les permanentes sont **les plus importantes de
tout ce qu'il lit** — plus que les pièges, plus que l'état technique.

📌 **Pourquoi** : le Détailleur ne peut nommer que ce qu'il a prévu. Une
règle déclenchée par un geste ordinaire — toute attente, tout accès
disque — il ne sait pas d'avance qu'elle s'appliquera.

⚠️ **Cas observé** : 24 attentes dans le dépôt, **zéro bornée**, alors
que la règle était écrite et lue.

## 3. Avancer sur ce qui ne dépend pas du manque

🔴 **Quand il bute, il regarde ce qui lui reste à faire et continue sur
ce qui ne dépend pas du manque.** 📌 **Il ne s'arrête que quand plus
rien n'est faisable.**

🔴 **Un second manque découvert en avançant s'ajoute au fichier de
blocage, il ne le remplace pas.**

## 4. Une sortie de plus : il piétine

🔴 **Il bloque quand deux tentatives de suite échouent pour la même
raison.**

📌 **Pas une durée — un fait observable** : il voit sa sortie de test,
il sait si c'est la même erreur. **Il progresse** → chaque tentative
change l'erreur, il continue. **Il piétine** → une tentative de plus ne
changera rien.

⚠️ **Le cas attrapé** : il a mal compris ce que le test attend, il
modifie son code, et l'erreur ne bouge pas.

---

# `relecteur.md`

✅ **FAIT** — 📌 **ses deux modifications, et sa fiche de passe.**

| Ce qui a changé | |
|---|---|
| **Point 2** | 📌 **Devient largement mécanique** — 🔴 **le Testeur a déjà écrit un test par critère et vérifié qu'il échoue.** ⚠️ **Un critère dans `## Criteria with no test` n'est pas un manque** |
| **Point 3** | 🔴 **Élargi aux règles `permanente`**, quoi que dise la fiche |
| **Point 4** | 📌 **Allégé** — ⚠️ **que le module compile est prouvé par l'exécution** |

## Sa fiche de passe — 17 commentaires

📌 **Passés (12)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C11 · C12 ·
C13 · C15 · C16

⚠️ **Reportés (5)** — C8 · C9 · C10 · C14 · C17

🔴 **Écartés (0)**

| # | Le sujet | Pourquoi |
|---|---|---|
| **C8 · C9 · C10 · C14 · C17** | L'escalade Opus, le plafond des trois tentatives, ses blocages qui arrêtent sur le Product Owner | 📌 **Tous sur `/8_code`** — 🔴 **à passer avec elle** |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C2 · C3** | 🔴 **Il n'avait aucune source pour savoir ce que le lot avait changé** — ⚠️ **on ne grepe pas un commit**, et son point 4 reposait donc sur rien. 📌 **Le prompt lui nomme les fichiers**, calculés par l'orchestration |
| **C11** | 🔴 **`FAIL structurel` se définissait par un *nombre* de points en échec** — 📌 **il se définit par *ce qui* échoue** : le module rouge, ou un symbole promis absent |
| **C7** | 🔴 **Le verdict ne nommait qu'un manquement** — ⚠️ **un fresh Réalisateur allait corriger un tiers du lot.** 📌 **Un champ `## Findings` les nomme tous** |
| **C13** | 🔴 **Les cas vides passaient** — ⚠️ **une fiche sans critère donnait `PASS` au point 2 par construction** |
| **C15** | 🔴 **Il lit la revendication de compilation en premier** — 📌 **il grepait chaque symbole d'un module qui n'avait jamais compilé** |

---

## La demande

🔴 **Il ne saute pas.** Ses cinq points restent, dont trois qu'aucun
autre mécanisme ne reprend.

## Ce qui change

**Son point 2** — *un test par critère* — devient largement mécanique :
le Testeur écrit un test par critère et vérifie qu'il échoue puis
passe. 📌 **Une partie de son point 4 aussi** : que le module compile et
que les tests tournent est prouvé par l'exécution.

**Son point 3 s'étend** : il vérifie les conventions que la fiche
nomme **et les règles marquées `permanente`**, puisqu'elles
s'appliquent partout.

## Ce qui reste entier

| | |
|---|---|
| **1** | Les symboles correspondent à ce que la fiche promettait, **signature comprise** |
| **3** | Les conventions — **élargi** |
| **4** | `## Outside the lot` : chaque fichier touché que la fiche ne déclare pas, **vérifié contre le diff** |
| **5** | Rien de ce que le lot écrit n'est inutilisé **par le lot lui-même** — 🔴 **il lit le corps** |

⚠️ **Le trou assumé** : du code qui fait **plus** que le critère **et
qui sert**. Son point 5 attrape le code mort, mais exclut
explicitement *« ce que rien n'utilise »*.

---

# `controleur.md`

✅ **FAIT** — 📌 **aucune modification du fichier de travail** ; sa fiche
de passe est passée.

## Sa fiche de passe — 15 commentaires

📌 **Passés (11)** — C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 · C9 · C10 ·
C15

🔴 **Écartés (1)** — C14

⚠️ **Reportés (3)** — C11 · C12 · C13

| # | Le sujet | Pourquoi |
|---|---|---|
| **C14** | Faire l'assemblage par un script | ⚠️ **La fiche se dit elle-même incertaine** — 🔴 **et ça change la forme de la commande.** 📌 **Écarté ; à rouvrir si l'assemblage se révèle infidèle** |
| **C11 · C12 · C13** | Le propriétaire du groupement, le worktree, les issues | 📌 **Sur `/9_controle` et `/8_code`**, que **A4** et **A5** réécrivent |

**Les plus structurants :**

| # | Ce qui a changé |
|---|---|
| **C1** | 🔴 **`Missing` était inatteignable** — ⚠️ **« une intention que tu ne peux pas rattacher va sous *doutes* »** routait tout vers le doute. 📌 **Les deux se distinguent par un fait** : rien ne l'observe → `Missing` |
| **C6** | 🔴 **L'assemblage ne voyait pas un groupe muet** — ⚠️ **il détectait un trou entre `B6` et `B8`, jamais les derniers blocs ni un groupe entier sans fichier.** 📌 **Le prompt lui donne les groupes et la liste des blocs** |
| **C7** | 🔴 **Les partiels d'un tour précédent survivaient** — ⚠️ **l'assemblage mélangeait deux états** |
| **C3 · C4 · C5** | 🔴 **Son mécanisme de blocage disparaît entièrement** — 📌 **ses deux causes vont au rapport** |
| **C2** | 🔴 **L'unité est l'intention, jamais le bloc** — 📌 **une phrase nommant deux observables donne deux lignes** |

⚠️ **Cascade à passer avec `/9_controle`** : 🔴 **la commande doit
nommer les groupes du tour et la liste des blocs** dans le prompt de
l'assemblage.

---

# `arbitre.md`

✅ **FAIT** — 📌 **sa modification unique** ; ⚠️ **pas de fiche de
passe**, l'analyse ne l'a pas atteint.

| Ce qui a changé | |
|---|---|
| **Le tri de ce qui remonte** | 🔴 **Quatre destinations, dont trois ne vont pas à l'Architecte** : un arbitrage → l'Architecte · un piège de plateforme → **`## Traps`**, qu'il écrit lui-même · *« la règle X couvre-t-elle mon cas ? »* → **rien**, c'est une question de lecture · une règle devenue fausse → l'Architecte, et **le Product Owner arbitre** |
| **Ses interdits** | 📌 **Jamais une règle dans `TECHNICAL_CONVENTIONS.md`** — 🔴 **sa seule écriture hors fichier de blocage est un piège** |
| ⚠️ **Ajouté avec U10** | 🔴 **Il sait lire un fichier de blocage à plusieurs entrées** — 📌 **une réponse par `## Blocking N`, et il les lit toutes avant d'en trancher une** |

📌 **La mesure qui fonde le tri est dans l'agent** : **sur 25 règles
ajoutées par demande, 11 sont des portes ouvertes** — ⚠️ **et 8 des 18
restrictions restreignent une règle elle-même ajoutée par demande.**

---

## La demande

## Trier ce qui remonte

🔴 **Aujourd'hui tout ce qui remonte devient une convention, faute
d'ailleurs où aller.**

| La demande apporte | Où ça va |
|---|---|
| **Un arbitrage** — deux choix défendables, deux lots divergeraient | Les conventions |
| **Un piège de plateforme indevinable avant le test rouge** | 🔴 **`## Traps` de `CURRENT_TECHNICAL_STATE.md`** |
| **« La règle X s'applique-t-elle à mon cas ? »** | 🔴 **Rien** — c'est une question de lecture, pas un manque |
| **Une règle devenue fausse** | Les conventions, en remplacement — ⚠️ **et le Product Owner arbitre** |

📌 **Pourquoi `## Traps` pour un piège** : le Réalisateur le lit **en
entier, toujours** — *« tu ne peux pas greper une règle dont tu ignores
qu'elle s'applique à toi »* — alors qu'une convention n'est tenue que si
la fiche la nomme.

⚠️ **Cas observé** : sur 25 règles ajoutées par demande, **11 sont des
portes ouvertes** — surtout des réponses à *« la règle précédente
s'applique-t-elle à mon cas ? »* — **et 8 des 18 restrictions
restreignent une règle elle-même ajoutée par demande.** 🔴 **Le fichier
grandit par empilement.**

---

# Les commandes

## 🆕 `3a_genre.md`

**Entre `/3_decoupe` et `/3b_nature`.** Invoque le Qualifieur sur
les blocs marqués, ou sur tous au premier tour.

**Son *What to run next*** : questions non vides → `/1_lexique` ; vides
→ `/3b_nature`.

## `1_lexique.md`

📌 **Accepte le fichier de questions du Qualifieur**, comme celui
de tout autre agent du cycle.

## `4_grille.md`

- 🔴 **Deux greps sur `Genre:` dans `desc-produit.md`** : les
  `comportement` à sonder, **et les `transverse` à charger en
  contexte.** 📌 **Elle les nomme dans le prompt**, comme elle nomme
  déjà les blocs marqués.
- 🔴 **Orchestrer le temps 2**, après que le temps 1 a rendu un fichier
  vide : sur les seuls blocs marqués comme touchant l'existant, avec
  les sections du global qu'ils touchent. **Sans retour au temps 1.**

## `5_reclasse.md`

✅ **FAIT** — 📌 **deux gestes mécaniques, dans cet ordre : le partage
par genre, puis le tri par nature** *(qui existait déjà)*.

| Ce qui a changé | |
|---|---|
| **Le partage** | 🔴 **Six fichiers sous `par-genre/`**, un grep par genre, copie par script |
| **Le tri par nature** | 🔴 **Part désormais de `par-genre/comportements.md`**, jamais du fichier produit — 📌 **seul un comportement a une nature** |
| **Les contrôles d'entrée** | 🔴 **Aucune ligne `Genre:` vide** ; **tout comportement a une nature** — ⚠️ **un bloc d'un autre genre a une `Nature:` vide, et c'est juste** |
| **Les comptes** | 📌 **Les six fichiers contre le fichier produit** ; **puis `desc-par-nature.md` contre les comportements** |
| **Les fichiers précédents** | 🔴 **Supprimés avant chaque partage** — ⚠️ **un genre sans bloc reçoit un fichier vide**, jamais pas de fichier |
| `commands/2_structure.md` | ✅ **`par-genre/` entre dans l'invalidation** quand un `NEW` apparaît |

---

### La demande

| Fichier | Qui le lit |
|---|---|
| Les comportements | Le Convertisseur, une invocation par nature |
| Les transverses | 🔴 **Toutes les invocations de nature du Convertisseur** |
| Les directives | L'Architecte |
| Les références | Le Convertisseur — section Text |
| Le hors-périmètre | Le Convertisseur — préambule |
| La recette | Le Product Owner, rendue par `/9_controle` |

⚠️ **Pas les Sondeurs** — 🔴 **le partage tourne après leur boucle.**
📌 **Pendant la boucle, `/4_grille` leur nomme les blocs par un grep sur
`Genre:` dans `desc-produit.md`.**

🔴 **Les fichiers précédents sont supprimés à chaque partage** — ce sont
des vues, le fichier maître reste la source.

📌 **Elle compte** : autant de blocs en sortie qu'en entrée, aucune
ligne `Genre:` vide, aucun genre hors des six. **Sinon elle s'arrête.**

## `6_convertit.md`

- **Passer les fichiers du partage aux bonnes invocations.**
- 🔴 **Le routage des questions techniques, à trois cas :**

| Ce qu'il écrit | Ce qu'on fait |
|---|---|
| Technique seul | Répondre, puis `/6_convertit` — **boucle courte** |
| Produit seul | **Boucle longue** |
| Les deux | **Boucle longue** — et il intègre **les deux fichiers** à son retour |

⚠️ **Exception explicite à la route unique** : une réponse technique ne
repasse pas par `/1_lexique`. **À dire**, puisque ça contredit *« toute
réponse repasse par `/1_lexique` »*.

## `conventions.md`

- 🔴 **Tester l'existence de `TECHNICAL_CONVENTIONS.md`** — ⚠️ **en
  dernière ligne de sa table**, jamais avant une requête en attente ou
  des questions à intégrer.
- **Son *What to run next*** : un nouveau fichier de questions →
  répondre, puis `/conventions`.

## `7_lots.md`

🔴 **Lire le `## Verdict` de la demande après l'Architecte.** 📌 **Un
refus est traité comme un blocage** — elle s'arrête et rend la main,
avec la raison du refus et ce que l'Architecte dit qui trancherait.

⚠️ **Pourquoi** : elle s'arrête déjà si l'Architecte **bloque**, mais
pas s'il **refuse**. Un refus laisse le Cadreur devant exactement le
même problème, et il ne contourne jamais une convention : **il rebloque
à l'identique.**

## `8_code.md`

✅ **FAIT** — 📌 **la boucle passe de trois agents par lot à cinq.**

| Ce qui a changé | |
|---|---|
| **A3 — les trois contextes** | 🔴 **Concepteur → Testeur → Réalisateur**, chacun attendant le précédent. ⚠️ **Un blocage de l'un arrête le lot** |
| **Le test du geste 1** | 🔴 **Porte sur le lot, plus sur le bloc** — ⚠️ **un bloc à moitié détaillé passait le test** |
| **Le Relecteur** | 🔴 **Reçoit la liste des fichiers changés**, par `git diff` — 📌 **il ne peut pas greper un commit** |
| **Le compteur de tentatives** | 🔴 **Sur disque, dans `## Attempts`** — ⚠️ **un tour interrompu repartait de zéro.** 📌 **Le Relecteur écrit ce champ** |
| **L'escalade** | 🔴 **Deux `Cause: reasoning` → la troisième tentative sur `opus`** |
| **A-6** | 🔴 **Arrêt au troisième redécoupage**, avec le `## Ce qui revient` du Cadreur relayé |
| **Le Contrôleur** | 🔴 **Les deux passages périmés retirés** — 📌 **elle ne l'invoque jamais** |

---

## La demande

- **Orchestrer trois contextes par lot** au lieu d'un : Concepteur,
  Testeur, Codeur.
- 🔴 **Au troisième redécoupage d'une même exécution, elle s'arrête et
  rend la main**, avec le `## Ce qui revient` du Cadreur.

⚠️ **Pourquoi** : cette boucle ne passe par personne, par construction,
et chaque tour est le plus cher de la chaîne — une coupe, jusqu'à trois
vérifications, les fiches d'un bloc, le code d'un lot, une relecture.
📌 **Le Cadreur signale déjà le troisième retour, mais dans un rapport
lu après coup.**

## `9_controle.md`

✅ **FAIT** — 📌 **six phases au lieu de trois.**

| Ce qui a changé | |
|---|---|
| **Phase 4 — la recette** | 🔴 **Deux sources** : les lignes du Testeur et le fichier `recette` du partage. 📌 **Ordonnée par état**, chaque remise à zéro annoncée — ⚠️ **une ligne sans état va à la fin** |
| **Phase 5 — le registre** | 🔴 **Doutes et intentions manquantes du Contrôleur, plus les questions produit de l'Arbitre** — 📌 **elle ramasse, elle ne conclut pas** |
| **Phase 6 — les décisions produit** | 🔴 **`code/decisions-produit.md`, écrit même vide** — 📌 **lu par le Rédacteur à `/fusion`, invocation 3** |
| **Sa portée** | 📌 **Cycle principal et chaque cycle de correction** — ⚠️ **le Contrôleur, lui, ne tourne que sur le principal** |
| ⚠️ **Cascade du Contrôleur** | 🔴 **Le prompt d'assemblage nomme les groupes du tour et la liste des blocs** · **`code/controle/` est vidé avant** |
| **Son relais** | 📌 **Les quatre fichiers, par nom** |

---

## La demande

🔴 **Elle rend trois choses au Product Owner, et rien d'autre.**

**1. La recette manuelle, assemblée et ordonnée**

| | |
|---|---|
| **Ordonnée par état, pas par intention** | Tout ce qui se vérifie sur une application vide, puis avec une course, puis avec plusieurs. ⚠️ **Chaque remise à zéro coûte cher** : le moins possible, et annoncées |
| **Courte, donc filtrée** | 🔴 **Seulement ce qu'un test automatique n'a pas pu vérifier** |
| **Une ligne = une chose à regarder** | Dans les mots du Product Owner, avec ce qu'on attend |

📌 **Deux sources** : les lignes du Testeur, **et le fichier `recette`
du partage** — ce que le Product Owner voulait vérifier lui-même.

⚠️ **Cas observé** : un fichier de tests manuels a existé et a été
abandonné — **non parce qu'il était inutile, mais parce qu'il était
impraticable** : des milliers de tests non ordonnés, avec des
suppressions et des remises de données au milieu.

**2. Le registre des questions produit échappées**

📌 **Deux sources** : les *doutes* et *intentions manquantes* du
Contrôleur, et les questions produit rendues par l'Arbitre — dans les
`blocked_<agent>-NN.md`.

🔴 **Elle ramasse, elle ne conclut pas.** Un fichier, un cas par ligne.
**Aucune classe proposée, aucune modification de la grille.**

📌 **Pourquoi en fin de cycle** : un cas isolé ne dit rien ; dix cas
ensemble laissent voir une forme.

**3. Les décisions produit prises pendant le codage**

🔴 **Une question produit tranchée pendant le codage entre dans une
fiche, jamais dans le fichier produit ni dans le global.**

📌 **Elle rend un fichier de décisions par cycle**, que le Rédacteur
intégrera à `desc-produit-fusion.md`.

**Portée**

📌 **Elle tourne sur le cycle principal et sur chaque cycle de
correction.** 🔴 **Le Contrôleur, lui, ne tourne que sur le cycle
principal** — un cycle de correction n'a pas de fichier produit, il n'y
a rien à confronter.

## `fusion*.md`

🔴 **Invoque le Rédacteur, puis le Fusionneur** — **tout à la fin, une
fois tous les cycles de correction passés.**

📌 **Pourquoi tout à la fin** : si un second bugfix revient sur ce qu'un
premier avait décidé, c'est la version finale qui entre. **On ne
consigne pas un état intermédiaire.**

## `CLAUDE.md`

**L'inventaire** : les agents et les commandes, avec le Qualifieur, le
Concepteur et le Testeur.

---

# Les grilles

## `GRILLE_CADRAGE_PRODUIT_V2.md`

🔴 **La notion de niveau sur chaque question** : *obligatoire* et
*défaut*.

## `GRILLE_CONVENTIONS.md`

🔴 **Retirer les 34 entrées classées porte ouverte**, garder les 36 —
12 arbitrages, 24 corrections.

📌 **Archiver les retirées** avec leur texte et la raison — **pour
pouvoir remettre, pas pour se souvenir.**

⚠️ **Où elles sont concentrées** : C2, C3 et C4 — vérification,
frontières, structure — **12 portes ouvertes sur 16**, presque aucune
correction.

⚠️ **Ce que le retrait est** : une hypothèse à vérifier. Les défauts
qu'on leur attribuait viennent probablement de trois causes
historiques corrigées depuis. 🔴 **On retire, on fait tourner, et on
remet ce qui manque — avec un cas cette fois.**

---

# Les documents de process

## `PROCESS_AMONT.md`

Le genre et le partage · les deux temps de fermeture · les questions à
deux niveaux · les règles transverses · la dérivation incrémentale des
conventions · les deux routes du Convertisseur · les titres du global ·
le trou de couverture marqué comme question produit.

## `PROCESS_AVAL.md`

Le découpage du codage en trois contextes et son coût *(≈ +60 %)* · la
recette · le registre et les décisions produit · le périmètre fermé de
`/9_controle`.

**Deux corrections de formulation :**

- 🔴 **La fiche ne se suffit plus tout à fait** — le Réalisateur lit
  aussi les conventions permanentes. 📌 **Ce qui reste vrai : aucune
  architecture à décider.**
- 🔴 **L'Extracteur est cité et il est supprimé** — le global naît
  maintenant du Fusionneur.

---

# Reprise par fichier

📌 **La vue qu'on lit pour savoir ce qui reste.** ✅ **Une coche : le
fichier est terminé** — modifications et fiche de passe.

## Agents

| Fichier | Reste à faire |
|---|---|
| ✅ `lexicographe.md` | — |
| ✅ `qualifieur.md` 🆕 | — |
| ✅ `redacteur.md` | — |
| ✅ `decoupeur.md` · `classeur.md` | — |
| ✅ `sondeur.md` | — |
| ✅ `assembleur.md` | — |
| ✅ `convertisseur.md` | — |
| ✅ `architecte.md` | — |
| ✅ `fusionneur.md` | — ⚠️ **pas de fiche** |
| ✅ 🆕 `concepteur.md` | — |
| ✅ 🆕 `testeur.md` | — |
| ✅ `detailleur.md` | — ⚠️ **C19–C21 reportés avec `/8_code`** |
| ✅ `realisateur.md` | — ⚠️ **C3, C12–C14, C16, C17 reportés avec `/8_code`** |
| ✅ `relecteur.md` | — ⚠️ **C8–C10, C14, C17 reportés avec `/8_code`** |
| ✅ `arbitre.md` | — ⚠️ **pas de fiche** |
| ✅ `cadreur.md` | — |
| ✅ `verificateur.md` | — |
| ✅ `controleur.md` | — ⚠️ **C11–C13 reportés avec `/9_controle`** |
| `diagnostiqueur.md` | ⚠️ **Pas de fiche**, et rien du fichier de travail |

## Commandes

| Fichier | Reste à faire |
|---|---|
| ✅ `1_lexique` · `2_structure` · `3_decoupe` · `3a_genre` 🆕 · `3b_nature` · `4_grille` · `5_reclasse` · `6_convertit` · `conventions` | — |
| ✅ `7_lots.md` | — |
| ✅ `8_code.md` | — 📌 **A3, A-6, et les 12 commentaires reportés** |
| ✅ `9_controle.md` | — 📌 **A4, A5, et la cascade du Contrôleur** |
| ✅ `fusion.md` · `fusion_compare.md` · `fusion_applique.md` | — 📌 **les deux dernières ne nomment pas le fichier produit** : l'agent le trouve par sa table |
| `CLAUDE.md` | ✅ **Fait** |

## Grilles

| Fichier | Reste à faire |
|---|---|
| ✅ `GRILLE_EXISTANT.md` 🆕 · `GRILLE_CADRAGE_PRODUIT_V2.md` | — |
| `GRILLE_CONVENTIONS.md` | 🔴 **Retirer les 34 entrées porte ouverte**, archiver |

## Documents de process

| Fichier | Reste à faire |
|---|---|
| `PROCESS_AMONT.md` · `PROCESS_AVAL.md` | 🔴 **Tout** — à faire en dernier, quand la chaîne est stable |

---

