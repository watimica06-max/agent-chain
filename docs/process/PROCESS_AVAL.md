# Process aval — du document technique au code

> Documentation de référence. Décrit la chaîne **document technique →
> code**.
>
> 📌 **L'amont** — de l'idée au document technique — vit dans
> `PROCESS_AMONT.md`. ⚠️ **Ce qu'il porte n'est pas redit ici** : la
> forme des fichiers de questions, celle des fichiers de blocage,
> l'enveloppe git des commandes, les trois invocations de l'Architecte
> qui dérivent les conventions.
>
> 🔴 **Aucun agent ne lit ce document.** Il dit pourquoi les agents sont
> construits comme ils le sont — les décisions, pas leurs gestes.
> ⚠️ **Il ne recopie ni un agent ni une commande** : ceux-là vivent dans
> `.claude/agents/` et `.claude/commands/`, et les redire ici les ferait
> diverger.
>
> **Le test** : quelqu'un qui a ce document et pas les agents doit
> pouvoir les réécrire, parce qu'il comprend ce que chaque règle
> empêche.

---

## La frontière avec l'amont

**L'aval commence au document technique.** 🔴 **Il en existe deux
formes, jamais ensemble** : `spec-technique.md` sur un cycle de
fonctionnalité, `desc-bug.md` sur un cycle de correction. **Le dossier
qui porte les deux est un défaut** ; le Cadreur s'arrête dessus.

📌 **Tout le reste est identique** — même découpage, même séquence,
mêmes fiches, même boucle.

🔴 **L'aval n'a presque pas besoin du Product Owner une fois lancé.**
L'amont en a besoin à chaque tour ; ici une commande code plusieurs
lots d'affilée sans que personne réponde à rien. ⚠️ **C'est ce qui
autorise l'enchaînement silencieux** que l'amont s'interdit.

---

## Ce qui distingue l'aval

🔴 **Un sous-agent peut en appeler un autre.** ⚠️ **En amont, tout passe
par la commande.** 📌 **Ici quatre dialogues existent**, et ils sont la
structure même de la chaîne — voir *Les quatre dialogues*.

**Pourquoi** : 📌 **l'appelant garde son contexte pendant que l'appelé
tourne, et reprend derrière lui.** 🔴 **Un aller-retour par la commande
rendrait la main au Product Owner** à chaque tour, et perdrait ce que
l'appelant avait en tête.

🔴 **Une attente sur un agent n'a pas de borne ; une attente sur le
Product Owner est sondée.** ⚠️ **Un agent finit toujours** — le
sonder n'apprend rien et coûte des appels. 📌 **Une personne peut ne
pas être au clavier** : l'Arbitre sonde le fichier de blocage pendant
vingt minutes, de plus en plus espacé, puis s'arrête.

🔴 **Le découpage peut revenir sans intervention humaine.** ⚠️ **Un lot
en cours de codage peut renvoyer au Cadreur** — l'Arbitre écrit ce
qu'il faut, la commande relance le découpage et **poursuit sa boucle**.
📌 **Le Product Owner n'attend sur rien.**

🔴 **Un Réalisateur qui s'éteint laisse de quoi reprendre.**
`reprise_realisateur.md` dit ce qui est fait, ce qui reste, ce qui est
à moitié écrit. ⚠️ **Sans lui, le suivant recommence le lot.**

---

## Le principe qui tient toute la chaîne

🔴 **Un agent constate, un autre corrige — jamais le même.**

📌 **Trois fois dans la chaîne** : le Vérificateur constate, le Cadreur
corrige ; le Relecteur constate, un Réalisateur neuf corrige ;
l'Arbitre tranche, l'agent bloqué applique.

⚠️ **Juger son propre jugement ne fonctionne pas.** 📌 **Un agent peut
vérifier qu'il a écrit dans le bon fichier, au bon format** — c'est
mécanique. 🔴 **Il ne peut pas vérifier que son code fait ce qui était
demandé** : il a choisi son interprétation.

**Le corollaire, et il est cher** : 🔴 **un contexte frais là où il faut
un regard neuf.** ⚠️ **Le Vérificateur est rappelé jusqu'à trois fois
sur un même découpage, chaque fois sans mémoire du tour précédent** —
📌 **il doit juger un découpage qu'il n'a pas coupé**, et c'est tout ce
pour quoi il existe. **Un FAIL amène de même un Réalisateur neuf**,
jamais celui qui a écrit le code.

🔴 **Et l'inverse, tout aussi délibéré** : **le Cadreur, lui, garde son
contexte à travers les tours.** 📌 **Il vient de couper ce qu'on lui
reproche**, et corriger contre ce qu'il a en tête ne coûte rien.

🔴 **Un agent ne cherche jamais dans le dossier** — on lui nomme son
lot, son bloc, son fichier de blocage. 📌 **La commande a regardé.**
⚠️ **Un agent dont le dossier cible manque ne s'arrête pas : il
cherche**, liste, tente un chemin absolu.

---

# LES AGENTS

*Neuf agents. Sept portent la chaîne, deux la partagent avec l'amont ou
avec un autre point d'entrée.*

---

## Le Cadreur

**À quoi il sert** — Il transforme le document technique en **lots** :
des unités livrables que le reste de la chaîne code une à une.

🔴 **Il coupe, il ne recopie jamais.** Un lot **cite** les entrées dont
il découle — 📌 **la citation remplace le verbatim.**

🔴 **C'est la phase qui détermine tout ce qui suit.** ⚠️ **Rien en aval
ne rattrape un lot coupé trop gros.**

**Ce qui le déclenche** — 🔴 **une invocation par cycle, et il dure tout
le cycle.** 📌 **Quatre entrées possibles**, et ce qui est sur le disque
dit laquelle :

| Ce qu'il trouve | Ce qu'il fait |
|---|---|
| Un fichier de blocage à `## Decision` remplie | Il l'applique, puis reprend par le cas qui suit |
| `code/redecoupage.md` | 🔴 **Le codage l'a renvoyé** — les lots codés sont clos |
| Des défauts dans la séquence | 🔴 **Il ne corrige que les lots nommés** |
| Rien de tout ça | Un premier découpage |

🔴 **Sur les trois derniers cas, il ne rejoue pas le découpage
complet.** ⚠️ **Ces gestes coupent un premier découpage** — 📌 **il
greperait, lirait, inventorierait et regrouperait avant d'atteindre le
lot pour lequel on l'a rappelé, et ce lot n'y survivrait pas.**

**Ce qui fait un lot** — 📌 **une unité livrable ne suffit pas à
couper** : plusieurs découpages la satisfont. **Trois contraintes
resserrent :**

🔴 **Un lot cite les entrées d'une seule section.** ⚠️ **Un lot à cheval
sur deux sections n'appartient à aucune couche.**

🔴 **Deux lots ne touchent jamais un même symbole.** 📌 **Le même
fichier est permis** — ce n'est pas un conflit.

🔴 **Un lot tient dans un contexte sain.** 📌 **Le test** : un lot si
gros que quatre de son espèce ne tiendraient pas dans un bloc est trop
gros.

**L'inventaire d'abord, le découpage ensuite** — 🔴 **il ne coupe pas
avant d'avoir écrit l'inventaire des symboles**, sinon il grouperait
contre une surface qu'il n'a pas vue.

📌 **Pour chaque symbole, tout ce qu'on lui demande**, avec les entrées
qui le demandent. 🔴 **Un symbole nommé dans onze entrées est noté onze
fois** — ce qui compte est l'union. **Puis un grep** : ce que le code
porte aujourd'hui contre ce que les entrées demandent, **et l'écart est
ce qu'il faut construire.**

🔴 **Il grepe, il n'ouvre jamais un fichier de code.** 📌 **Il établit
ce qu'un symbole est, pas ce que son implémentation fait.**

**Ce que le découpage doit rattraper, et que rien d'autre ne
verrait** — 📌 **trois catégories n'apparaissent dans aucune entrée :**

🔴 **Les appelants.** Un contrat qui change casse ce qui l'appelle, ce
qui le remplit, et ce qui doit lui ressembler. ⚠️ **Les tests sont des
appelants.** 🔴 **On grepe le nom, jamais ce qui déclare d'où le symbole
vient** — 📌 **les appelants les plus proches ne déclarent rien de son
origine, et ce sont eux qui cassent en premier.**

🔴 **Les pièces.** 📌 **Une règle qui nomme un acteur hors du programme
a besoin d'une pièce pour l'atteindre** — l'OS, un capteur, le disque,
le réseau, une horloge. ⚠️ **Aucune entrée n'en nomme une.**
🔴 **La pièce est un lot à part**, jamais repliée dans celui qui déclare
le contrat : **deux couches.** ⚠️ **Un contrat sans rien derrière
compile, passe ses tests, et ne fait rien.**

🔴 **Les déclarations hors du code.** Une permission, un service, une
bibliothèque, un point d'entrée : **chacune vit dans un fichier que
rien dans le code ne nomme**, et aucun grep sur un symbole ne la
trouve.

**Et les déclencheurs** — 🔴 **pour chaque déclencheur qu'une entrée
nomme, quel symbole l'écoute ?** ⚠️ **Ce qu'un déclencheur atteint est
rarement ce qui l'écoute.** 📌 **Une règle que personne n'appelle est du
code mort**, si bien construite soit-elle.

**Toute entrée est citée ou déclarée sans lot** — 🔴 **une entrée qui
n'est ni l'un ni l'autre est un oubli, pas une décision**, et rien en
aval ne sait les distinguer.

**Sur un cycle de correction** — 🔴 **chaque entrée nomme son porteur**,
et **le groupement se fait par porteur, même à travers les sections.**
📌 **Le symbole existe déjà**, donc des entrées sans rapport peuvent
atterrir dessus. ⚠️ **Un porteur `none` est décidé avant tout
groupement** — deux `none` peuvent atterrir sur un même symbole, et
grouper avant de décider ferait construire deux fois la même chose.

**La frontière** — 🔴 **il ne groupe pas les lots en blocs** : c'est le
Vérificateur, qui a l'ordre d'exécution. 🔴 **Il n'écrit ni signature ni
critère** : c'est le Détailleur. 🔴 **Il n'invoque que le
Vérificateur.**

---

## Le Vérificateur

**À quoi il sert** — Il vérifie qu'un découpage tient, et **il produit
la séquence sur laquelle tout le cycle tourne.**

🔴 **Il constate, il ne corrige jamais.** Un défaut repart au Cadreur.

🔴 **La séquence est le seul artefact qui pilote la boucle** — c'est
elle qui dit à la commande quel lot invoquer, et dans quel ordre.

**Ce qui le déclenche** — 🔴 **le Cadreur l'appelle**, jusqu'à trois
fois sur un même découpage, ⚠️ **chaque fois sur un contexte frais.**
📌 **Il ne cherche pas ce qu'un tour précédent de lui-même a signalé** :
il vérifie le découpage qu'il a devant lui.

**Ce qu'il croise** — 🔴 **l'inventaire contre les lots**, et sept
espèces de défaut en sortent. **Trois méritent d'être comprises :**

📌 **Une surface non construite** — une opération que l'inventaire
liste et qu'aucun lot ne produit ni ne modifie. 🔴 **C'est le contrôle
que les noms seuls ne peuvent pas faire** : un lot qui a besoin d'un
dépôt et un lot qui le produit se croisent parfaitement ; **que l'un
écrive et que l'autre lise ne se voit qu'ici.**

📌 **Un appelant qu'aucun lot ne déclare** — ⚠️ **il n'apparaît pas
comme un trou** : rien n'en a besoin, rien ne le produit, et le
découpage se lit comme complet. 🔴 **Il se voit quand le module cesse
de compiler**, dans un lot qui ne touche ni l'un ni l'autre bout.

📌 **Un contrat changé sans sa cascade** — ⚠️ **un contrat existe pour
être rempli et appelé** : un lot qui en change un et ne déclare ni l'un
ni l'autre n'a rien grepé.

🔴 **Il juge la forme, pas le compte.** ⚠️ **Que quatre appelants soit
le bon nombre est au Cadreur de le savoir** ; 📌 **qu'un contrat changé
n'en déclare aucun est un défaut visible.**

**Ce qui ordonne sans se déclarer** — 🔴 **deux choses n'apparaissent
dans aucun champ de besoin.** 📌 **Une modification crée une
dépendance** : un lot qui consomme un symbole qu'un autre modifie passe
après. 📌 **Deux lots qui changent les deux bouts d'un même appel sont
ordonnés aussi** — ⚠️ **entre eux le module ne compile pas**, et rien ne
le déclare. 🔴 **Celui qui laisse l'appel valide passe devant.**

**L'ordre se dérive, il ne se décide pas** — 📌 **les lots dont tous les
besoins préexistent d'abord, puis ceux qui deviennent éligibles, et
ainsi de suite.** 🔴 **Un lot qui ne devient jamais éligible est dans un
cycle** — ⚠️ **un défaut, pas un blocage**, et l'ordre reste vide : sans
ordre, il n'y a rien à grouper.

🔴 **La départage est mécanique**, pour que deux exécutions donnent la
même séquence.

**Les blocs** — 📌 **une tranche contiguë de la séquence**, d'une seule
couche. 🔴 **Le critère est la lecture partagée** : des lots qui ouvrent
les mêmes entrées et le même code vont ensemble. ⚠️ **Les plafonds
comptent les entrées citées, pas les lots** — 📌 **ce qu'un bloc coûte
est ce qu'il ouvre.**

⚠️ **La règle de couche saute sur un cycle de correction** : 📌 **deux
corrections d'une même couche n'y partagent aucune lecture** — chacune
ouvre son entrée, grepe son symbole. 🔴 **On groupe alors sur la
contiguïté seule.**

**La frontière** — 🔴 **il n'ouvre jamais une entrée qu'aucun lot ne
cite.** ⚠️ **En avoir besoin pour comprendre un lot signifie que le
découpage est mauvais** — 📌 **c'est un défaut à signaler, pas à
combler.**

---

## Le Détailleur

**À quoi il sert** — Il transforme les règles des entrées qu'un lot
cite en **signatures et critères d'acceptation** : la fiche depuis
laquelle un Réalisateur code sans rien décider.

🔴 **Il ne tranche rien.** ⚠️ **Une entrée qui laisse une règle ambiguë
l'arrête** — 📌 **il n'est pas le filet de la chaîne amont.**

🔴 **Une fiche fausse contamine tout un bloc** — d'où la règle qui
gouverne tous ses gestes : **tout symbole est confirmé par grep avant
d'être écrit.**

**Ce qui le déclenche** — 🔴 **une invocation par bloc, pas par lot.**
📌 **C'est ce qui fait exister le bloc** : les lots d'un bloc partagent
leurs lectures, et les détailler ensemble les paie une fois.

**Il parcourt tout le bloc avant d'écrire une seule fiche** —
⚠️ **il cherche une seule chose : ce qui l'empêcherait de détailler,
sur n'importe quel lot.**

📌 **Pourquoi rien d'abord, plutôt que ce qu'il peut** : 🔴 **une fiche
n'est gardée que si le découpage tient.** ⚠️ **Un bloc renvoyé au
découpage perd toutes ses fiches non codées** — 📌 **détailler huit lots
pour les perdre avec les deux qui bloquaient, c'est huit lots détaillés
deux fois.**

🔴 **Et ce qui l'arrête se voit dans les entrées, qu'il ouvre de toute
façon** — **parcourir d'abord ne coûte aucune lecture.**

**Ce qu'une signature doit dire** — 📌 **ce qui entre, ce qui sort, et
sous quel nom.** 🔴 **Mais surtout ce que le retour vaut aux bords** :
l'absence, le vide, une borne, une unité, un ordre. ⚠️ **Un type ne
porte pas ça**, et deux lots peuvent nommer le même symbole en en
attendant deux choses différentes.

📌 **Une règle à trois issues ne renvoie pas un booléen**, ni un booléen
plus un effet de bord.

**Ce qu'un critère d'acceptation doit être** — 📌 **une observation
vérifiable après coup**, à trois propriétés : **observable de
l'extérieur du code**, **décidable** — deux personnes, même verdict —
et **attribuable à ce lot.**

🔴 **Toute assertion des entrées citées doit être observable par au
moins un critère** — ⚠️ **pas tout comportement, toute assertion.**

🔴 **Et la seconde espèce d'assertion est celle qui disparaît** : 📌 **ce
qu'une entrée affirme sans rien produire** — une chose présente,
absente, constante, placée par rapport à une autre, de telle forme,
comptée, interdite. ⚠️ **Ça se lit comme une description plutôt que
comme du travail**, parce que rien n'est calculé — 📌 **et c'est
exactement ce dont personne ne remarquera l'absence**, puisque aucun
calcul n'échoue sans.

📌 **Deux tests attrapent ça** : *le code pourrait-il satisfaire tous
mes critères et contredire quand même cette phrase ?* et *mes critères
relus sans l'entrée disent-ils que cet élément existe ?*

🔴 **Un déclencheur a un critère sur ce qu'il atteint**, pas seulement
sur son existence — ⚠️ **un déclencheur construit et branché sur rien se
lit comme construit.** 📌 **Ce qu'il atteint vit souvent dans une autre
entrée** : il l'ouvre aussi.

🔴 **Un critère qu'on ne peut pas écrire en test n'est pas un
critère.** ⚠️ **Ne pas savoir quoi observer signifie que la règle est
ambiguë** : il s'arrête.

**Il nomme les conventions qui portent sur le lot** — 🔴 **il lit les
conventions en entier, le Réalisateur code contre la fiche.** ⚠️ **Une
règle qu'il ne nomme pas est une règle que le Réalisateur
n'appliquera pas, et que le Relecteur ne saura pas chercher.**

**La frontière** — 🔴 **il ne décide pas si un symbole est créé ou
modifié** : le lot l'a déclaré, il applique. ⚠️ **Si le grep contredit
la déclaration, c'est un défaut de découpage**, pas une décision à
prendre ici. 🔴 **Il ne décide pas où le code va** : le Réalisateur le
tire des conventions.

---

## Le Réalisateur

**À quoi il sert** — Il code un lot, depuis sa fiche.

🔴 **Aucun plan.** 📌 **Le Détailleur a produit les signatures : il ne
reste aucune architecture à décider.**

🔴 **Un test par critère d'acceptation.** ⚠️ **C'est ce qui rend le lot
vérifiable** — le Relecteur compare les tests aux critères.

**Ce qui le déclenche** — 📌 **une invocation par lot**, et **un
Réalisateur neuf sur un FAIL**, jamais celui qui a écrit le code.

| Le verdict | Ce qu'il fait |
|---|---|
| **FAIL mineur** | Corriger le point signalé, 🔴 **sans revisiter le reste du lot** |
| **FAIL structurel** | Reprendre le lot depuis le début |

**La fiche est autosuffisante** — 🔴 **il ne lit ni le document
technique, ni la liste des lots, ni la séquence.** ⚠️ **Si la fiche ne
suffit pas, elle est fausse**, et c'est un blocage.

🔴 **Il ne corrige jamais une fiche fausse.** ⚠️ **Improviser rendrait
la divergence invisible** — le code s'écarterait de la fiche sans que
rien le signale.

**Ce qu'il déclare hors de son lot** — 🔴 **tout fichier touché que la
fiche ne déclare pas, et ce qu'il en a fait.** 📌 **Une décision l'a
autorisé, ou il ne pouvait pas compiler sans** — ⚠️ **dans les deux cas
ce n'est pas dans ses modifications, et personne d'autre ne sait qu'il
l'a fait.** 🔴 **Une correction laissée hors de ce champ est une
correction que personne ne peut attribuer.**

**Il tient l'état technique à jour** — 📌 **ce qui mérite une place** :
un service, un mécanisme qu'un autre lot pourrait reconstruire, une
table, une route, une cascade, un piège, un état mort. 🔴 **Ce que son
lot a rendu faux disparaît** — une entrée n'est jamais *« modifiée par
lot-03 »*. 📌 **Ses lecteurs sont le Détailleur, le Réalisateur
suivant et le Diagnostiqueur.**

**Sa discipline de vérification** — 🔴 **analyse et tests par unité
cohérente de travail, jamais par édition.** *(41 exécutions sur 149
n'ont rien trouvé, mesuré sur dix étapes.)* 🔴 **Les corrections se
groupent aussi** : plusieurs échecs, on corrige tout, puis on relance
une fois.

🔴 **Son shell est réduit à `git add`, `commit`, `status` et les
commandes d'analyse et de test que les conventions nomment.**
⚠️ **Rien d'autre du tout** — 📌 **chercher se fait par `Grep`, qui est
borné au dépôt ; une recherche shell parcourt la machine, et celle qui
ne finit pas ne rend jamais la main.**

🔴 **Une commande à la fois, au premier plan, et il l'attend.**
⚠️ **Jamais en arrière-plan avec sondage** : deux exécutions d'un même
build se disputent le même verrou, et un shell que personne n'attend
continue après lui.

**La frontière** — 🔴 **il ne fusionne pas, ne crée pas de branche, ne
touche pas un worktree** : c'est l'orchestration. 🔴 **Il ne modifie
jamais les conventions** : il écrit une demande. 🔴 **Il ne discute pas
un verdict** : il corrige, ou il s'arrête.

---

## Le Relecteur

**À quoi il sert** — Il juge un lot contre sa fiche, et **il écrit le
verdict qui pilote la boucle.**

🔴 **Il constate, il ne corrige jamais.**

🔴 **Il juge l'interprétation, pas l'exécution** — 📌 **la boucle du
Réalisateur couvre la mécanique.**

**Ce qu'il ne vérifie pas, et pourquoi** — 🔴 **que le lot corresponde à
sa source** : le Vérificateur l'a confirmé en amont. 🔴 **La mécanique**
— analyse, tests, fichiers présents : la boucle du Réalisateur les
couvre. ⚠️ **Chaque contrôle ajouté doit nommer ce qu'aucun autre ne
fait déjà**, sinon c'est de la ratification, pas de la détection.

**Cinq points, et deux méritent d'être compris :**

📌 **Sur une modification, l'existence ne prouve rien** — 🔴 **seule la
signature dit si le lot a fait son travail.**

📌 **Le dernier point lit le corps, pas la signature** : 🔴 **ce que le
lot reçoit et ne lit jamais, ce qu'on lui rend et qu'il jette, ce qu'il
remplit et ne consulte pas.** ⚠️ **Un symbole qui porte la signature de
la fiche peut n'en rien faire.**

⚠️ **Pas ce que rien n'utilise** — 📌 **un autre lot, un contrat, une
clé de ressource peuvent l'atteindre, et aucun n'est devant lui.**

**Le champ vérifié** — 🔴 **il recopie ce que le compte rendu affirme du
build**, en une ligne. ⚠️ **Jamais vide** : 📌 **un champ vide se lit
comme *personne n'a regardé le build***, et c'est ainsi qu'un lot dont
le module n'a jamais compilé passe.

🔴 **Le module du lot qui ne compile pas est un FAIL structurel**,
quelle que soit la raison donnée. ⚠️ **Son code n'a jamais été exécuté
et ses tests n'ont jamais été des tests** : **le lot n'a rien
démontré**, et une correction ciblée ne démontrerait rien non plus.

**Ce qui fait repartir la boucle** — 🔴 **une divergence de symbole ne
menace que les lots non codés du même bloc** : 📌 **les blocs suivants
seront détaillés sur le code réel.** ⚠️ **Il nomme ces lots dans le
verdict** — leurs fiches ont été écrites contre une signature que le
code ne porte pas, et sont fausses.

🔴 **Une divergence est signalée même quand le code marche.**

**La frontière** — 🔴 **un lot, un verdict**, jamais un bloc entier.

---

## L'Arbitre

**À quoi il sert** — Il remplit le champ `## Decision` d'un fichier de
blocage, **pour que l'agent qui l'a écrit puisse continuer.**

🔴 **Il ne tranche presque rien de lui-même.** 📌 **Presque tout blocage
a déjà sa réponse quelque part dans le corpus** — une convention, une
entrée du document technique, ou le même problème résolu ailleurs dans
le même code. **Son travail est de trouver cette réponse, pas d'en
inventer une.**

**Le test, un seul** — 🔴 **votre réponse change-t-elle un comportement
que le corpus décrit ?**

📌 **Oui** — elle trancherait ce que la personne qui utilise
l'application obtient. **Il rend la main.**
📌 **Non** — une signature, un module, un ordre entre lots, un type,
une portée. **Il tranche.**

⚠️ **La ligne n'est pas à quel point ça sonne technique.** 📌 **Savoir
si un total est masqué ou affiché quand il ne peut pas être calculé est
une question produit**, si profond dans le code qu'elle surgisse.
**Savoir lequel de deux modules porte un adaptateur est à lui**, si
architectural que ça paraisse.

**Ce qui le déclenche** — 🔴 **le Détailleur et le Réalisateur
l'appellent, et eux seuls.** 📌 **Un blocage par invocation.** ⚠️ **Ils
tournent encore pendant qu'il travaille**, et lisent le champ dès qu'il
sort.

🔴 **Le Cadreur et le Vérificateur ne l'appellent pas** — ⚠️ **ce sur
quoi ils bloquent est mécanique** : un document manquant, une liste
illisible, une convention qui interdit ce qu'un lot exige. 📌 **Et la
dernière va à l'Architecte.**

🔴 **Un blocage du Relecteur ou du Contrôleur dit que quelque chose
manque** — ⚠️ **rien ne s'y tranche** : l'agent qui le devait doit
retourner.

**Ce qu'une décision porte** — 📌 **trois parties** : ce que l'agent
fait, ce sur quoi ça repose, et **ce à quoi ça ne s'étend pas.**
🔴 **La troisième est ce qui empêche une décision de se répandre** —
⚠️ **un lot à qui on dit de corriger un site d'appel corrigera tous
ceux qu'il rencontre**, sauf si la décision dit où s'arrêter.

📌 **Les blocages déjà tranchés sont à côté, numérotés** — 🔴 **il les
lit avant de trancher** : ⚠️ **un blocage qui en suit un autre signifie
souvent que la réponse précédente était trop étroite.** 📌 **Il tranche
plus large cette fois, et dit ce que la précédente avait manqué.**

**Quatre issues** — trancher · demander une règle à l'Architecte ·
renvoyer au découpage · attendre le Product Owner. **Les trois
dernières sont détaillées plus bas.**

**La frontière** — 🔴 **il ne dit jamais comment couper** : 📌 **il nomme
ce qui doit devenir possible, le Cadreur décide comment.** ⚠️ **Une
contrainte écrite comme une solution lui prend son travail.**

🔴 **Il ne répond jamais de mémoire** : un fait sur le code se grepe.

---

## Le Contrôleur

**À quoi il sert** — Il vérifie que **chaque intention du fichier
produit est portée par une fiche.**

🔴 **Il ferme la chaîne sur son point de départ.** ⚠️ **Une intention
perdue entre le produit et la fiche ne referait surface qu'à l'usage.**

📌 **Le Relecteur couvre fiche → code. Lui couvre produit → fiche.**

**Ce qui le déclenche** — 📌 **une fois, quand toutes les fiches
existent.** 🔴 **Deux invocations** : une par groupe de blocs que la
commande nomme, puis une pour assembler leurs rapports partiels.

🔴 **Cycle de fonctionnalité seulement.** ⚠️ **Pas de fichier produit
sur un cycle de correction** — il n'y a rien à confronter.

**L'unité est la phrase** — 🔴 **jamais le bloc entier.** 📌 **Un bloc
qui porte onze intentions demande onze réponses** — ⚠️ **sept critères
sur onze n'est pas une intention trouvée.**

📌 **Un bloc qui se lit comme un sujet peut en porter beaucoup** : une
carte de navigation est un bloc, et chaque chemin dedans est une
intention.

**Le critère** — 🔴 **l'intention est-elle observable dans une signature
ou dans un critère d'acceptation ?** ⚠️ **Pas dans la prose d'une
fiche** : 📌 **une fiche qui *mentionne* un bouton sans qu'aucun critère
l'observe ne porte pas l'intention.**

🔴 **Une intention qui joint deux choses demande un critère sur la
jointure.** 📌 *« L'icône de l'en-tête ouvre le profil »* n'est pas
portée par un critère qui dit que la méthode du navigateur change son
état : **ça observe la méthode, pas ce qui l'appelle.**

⚠️ **Tout bloc qui nomme ce qui déclenche un comportement se lit ainsi**
— 📌 **la chose déclenchée peut être construite et observée, et rien ne
l'atteindre.**

**La frontière** — 🔴 **il ne lit pas le code** : le Relecteur a couvert
fiche → code. 🔴 **Il ne tranche aucun doute** : une intention qu'il ne
peut pas rattacher va sous *douteux*, jamais sous *manquant*.
🔴 **Il ne relance rien** — 📌 **le Product Owner lit le rapport et
décide** s'il devient une liste d'écarts pour un cycle de correction.

⚠️ **Il n'écrase jamais un rapport antérieur** — 📌 **il en écrit un
nouveau, numéroté.** 🔴 **Il n'en ouvre aucun non plus** : ce qu'une
exécution antérieure a conclu l'arrêterait de chercher.

---

## L'Architecte — partagé avec l'amont

📌 **Ses invocations 1 et 2 appartiennent à l'amont** — voir
`PROCESS_AMONT.md`. **Ce qui suit est sa face aval.**

**Ce qui le déclenche ici** — 🔴 **l'invocation 3, sur les demandes qui
attendent dans `architecte/`.** 📌 **Deux choses l'appellent** : la
commande, à la fin d'un lot ou une fois le découpage tenu — ou
**l'Arbitre**, qui est bloqué sur une demande et l'attend.

📌 **Il ne les traite pas différemment** : il les lit toutes, les
tranche toutes, écrit chaque verdict.

🔴 **Il lit toutes les demandes avant d'en trancher une** — 📌 **deux
demandes portent souvent une seule règle**, et deviennent un seul
changement.

**Ce qu'il refuse** — 🔴 **une convention dit ce que le projet a
choisi.** 📌 **Trois choses n'en sont pas** : ce que la plateforme
impose — il n'y a pas d'autre voie ; ce qu'un outil vérifie ou pourrait
vérifier ; ce qui ne tient que sur une machine.

⚠️ **Cette invocation seule peut lire le web et les fichiers de
build** — 📌 **partout ailleurs c'est interdit**, et pour de bonnes
raisons : **ici il ne dérive pas un fichier, il juge une affirmation
sur une plateforme**, et ça se cherche plutôt que ça ne se sait.

🔴 **Un verdict porte le texte de la règle, pas seulement son numéro** —
⚠️ **l'agent qui le lit n'ouvre pas le fichier de conventions**, il
recopie ce que le verdict dit.

🔴 **Il n'attend jamais le Product Owner** : il tranche, il refuse, ou
il bloque, et il sort. ⚠️ **Et quand l'Arbitre l'a appelé, il ne bloque
pas du tout** — 📌 **le refus s'écrit dans le `## Verdict` de la
demande**, parce que l'Arbitre tourne encore. 🔴 **Un fichier de blocage
laisserait deux agents suspendus à la même réponse.**

---

## Le Diagnostiqueur — le point d'entrée d'un cycle de correction

**À quoi il sert** — Il **confirme un écart signalé contre le code**,
et le décrit assez précisément pour qu'il soit découpé en lots.

🔴 **Il ne tranche rien** : ce qui entre dans le cycle est la décision
du Product Owner — **elle l'a listé, il confirme qu'il existe.**
🔴 **Il ne corrige rien** : il localise et décrit.

**Ce qui le déclenche** — 🔴 **deux invocations, et la première tourne
autant de fois qu'il y a d'écarts**, toutes lancées ensemble.

📌 **Pourquoi découper** : dix écarts dans un seul contexte, ce sont dix
séries de greps qui s'accumulent. **Une investigation ne voit que son
écart**, et rien de ce qu'elle cherche n'aide les autres.

⚠️ **L'assemblage n'ouvre jamais le code** — 🔴 **les rapports portent
tout.** **Un rapport qui ne suffit pas à écrire une entrée est un
blocage.**

**Ce qu'une investigation établit** — 📌 **un écart est écrit en
comportement, pas en noms** : *« le facteur de correction n'est jamais
calculé »* ne nomme rien qui existe. 🔴 **Il en dérive les termes**, puis
cherche en élargissant. **Il s'arrête après le troisième
élargissement** — ⚠️ **au-delà, c'est deviner.**

🔴 **Un comportement ne vit pas que dans les fichiers source.** 📌 **Le
test** : *changer ce fichier changerait-il ce que l'application fait ?*
⚠️ **Un comportement absent des sources n'est pas un comportement
absent** : quelque chose de déclaré et jamais utilisé, un défaut qui
s'applique parce que rien ne le surcharge, une valeur fixée hors du
code.

**Le porteur** — 🔴 **la question est : qu'est-ce qui doit changer pour
que le comportement change ?** 📌 **Ce qui y répond est le porteur,
quelle que soit sa forme.** ⚠️ **Ne jamais demander de quelle espèce de
chose il s'agit.**

🔴 **La contrainte : le reste dépend de lui, pas l'inverse.** 📌 **Sur un
appel manquant, le porteur est l'appelant** — c'est là que le code
change.

🔴 **Un porteur par entrée.** ⚠️ **Vingt sites d'un même oubli sont
vingt entrées**, et la prose de chacune ne nomme que son site.
📌 **Le volume n'est pas une raison de grouper** : **une entrée qui en
couvre plusieurs ne peut pas être close en en observant une.**

⚠️ **Une exception, étroite** : 📌 **déplacer un comportement d'un
endroit à un autre est un seul écart** — 🔴 **entre les deux moitiés le
comportement n'existe nulle part**, et un correctif qui laisse le
projet dans cet état n'est pas livrable.

**Les seconds manques** — 🔴 **il confirme ce que le correctif exige,
pas seulement ce qui manque.** 📌 **Et il relit chaque appelant contre
le nouveau mécanisme**, sur deux tests : *ce qu'il porte aujourd'hui,
le nouveau mécanisme l'accepte-t-il ?* et *ce que le nouveau mécanisme
lui tend, s'en sert-il ?*

📌 **Le premier attrape ce qui casse ; le second ce qui ne fait rien en
silence.** 🔴 **Un type qui grossit passe le premier et rate le
second** — rien ne cesse de compiler, et personne ne lit le champ.

**La frontière** — 🔴 **il ne juge pas si un écart est légitime** : le
Product Owner l'a décidé en le listant. 🔴 **Il ne lit pas le code
au-delà d'un grep** : il confirme un comportement, il ne relit pas une
implémentation. 🔴 **`desc-bug.md` prend la forme du document
technique** — préambule, neuf sections, entrées numérotées — 📌 **parce
que le Cadreur le découpe exactement comme une spec.**

---

## Qui tourne sur quel modèle

*Porté par la frontmatter de chaque agent.*

| Opus | Sonnet |
|---|---|
| cadreur · verificateur · detailleur · arbitre · architecte | realisateur · relecteur · controleur · diagnostiqueur |

📌 **La ligne de partage** : 🔴 **décide-t-il une structure dont tout le
reste dépend ?** **Le Cadreur décide le découpage entier ; le Détailleur
écrit les signatures sur lesquelles tout un bloc est construit.**
📌 **Le Réalisateur et le Relecteur travaillent contre une fiche déjà
écrite.**

---

# LES QUATRE DIALOGUES

*🔴 **Un sous-agent en appelle un autre**, et c'est ce qui distingue
l'aval. ⚠️ **Aucun autre appel n'existe** — tout le reste passe par la
commande.*

| Appelant | Appelé | Sur quoi | Combien |
|---|---|---|---|
| **Cadreur** | Vérificateur | Le découpage qu'il vient de couper | 🔴 **Trois tours au plus**, qu'il compte |
| **Détailleur** | Arbitre | Un fichier de blocage à décision vide | Un par blocage |
| **Réalisateur** | Arbitre | Idem | Un par blocage |
| **Arbitre** | Architecte | Une demande de convention | 🔴 **Une fois, jamais deux** |

**Ce que chaque issue produit :**

**Cadreur ⇄ Vérificateur** — 📌 **des défauts vides** : le découpage
tient, le Cadreur sort. 📌 **Des défauts** : il corrige **les seuls lots
nommés** et rappelle. ⚠️ **Encore des défauts au troisième tour** : il
écrit un fichier de blocage nommant ce qui n'a pas convergé et sort.
🔴 **Il ne discute pas un défaut** — s'il le juge faux, il le dit dans
ce fichier plutôt que de recouper contre.

**Détailleur / Réalisateur → Arbitre** — 🔴 **ce que l'Arbitre rend est
un accusé de réception ; la réponse est dans le champ `## Decision`**,
qu'ils relisent.

| Le champ | Le Détailleur | Le Réalisateur |
|---|---|---|
| **Rempli** | Applique et détaille le bloc — 📌 le parcours tient encore | Applique et **reprend où il s'était arrêté** — 📌 il n'a rien perdu |
| **Renvoie au découpage** | 🔴 **N'écrit aucune fiche** | 🔴 **Jette tout ce qu'il a écrit**, ne commite rien |
| **Toujours vide** | S'arrête, le bloc en l'état | Écrit `reprise_realisateur.md` et s'arrête |

**Arbitre → Architecte** — 📌 **une règle écrite ou changée** : il en
recopie le numéro **et le texte** dans sa décision. 📌 **Refusée** : il
attend le Product Owner. 🔴 **Une demande refusée ne repart pas à
l'Architecte sous une autre formulation.**

**Les deux régimes d'attente**

🔴 **Attendre un agent n'a pas de borne** — ⚠️ **ni sondage, ni délai.**
📌 **Un agent finit toujours** : le sonder n'apprend rien et coûte des
appels.

🔴 **Attendre le Product Owner est sondé, et borné** — 📌 **deux minutes
d'écart au début, cinq ensuite, et rien au bout de vingt minutes
arrête.** ⚠️ **Une personne peut ne pas être au clavier.**

🔴 **Le champ reste alors exactement vide** — ⚠️ **c'est le seul cas où
l'Arbitre n'y touche pas.** 📌 **C'est ce vide que l'appelant teste**, et
n'importe quoi d'écrit là se lirait comme une réponse.

---

# LA BOUCLE DU CODAGE

## Lot par lot

    ┌─ nouveau bloc ? ──→ Détailleur (tout le bloc, d'un coup)
    │                          │
    │                     Réalisateur ──→ Relecteur ──→ verdict.md
    │                          ↑              │
    │                          └── FAIL ──────┤  🔴 3 reprises au plus
    │                                         │
    │              divergence nommant des lots ┤ ──→ Détailleur, ces fiches seules
    │                                         │
    │                    stop.md présent ? ────┤ ──→ arrêt demandé
    └──────────────── lot suivant ←───────────┘

    tous les lots en PASS  ──→  Contrôleur  ──→  fin

🔴 **Le prochain lot est le premier de la séquence sans `verdict.md` en
PASS.** 📌 **Une lecture, pas un balayage** — la séquence porte l'ordre.

**Ce qui fait repartir la boucle — quatre choses, et une seule
s'arrête :**

**1. Un FAIL** — 🔴 **un Réalisateur neuf, avec le verdict.**
📌 **Trois reprises au plus par lot**, tous types de FAIL confondus.
⚠️ **Un FAIL isolé n'arrête pas la commande.**

**2. Une divergence** — 🔴 **le verdict nomme les lots dont les fiches
sont devenues fausses**, et le Détailleur les réécrit, **celles-là
seules.** ⚠️ **Les lots codés gardent les leurs** : elles décrivent ce
qui a été construit.

**3. Un redécoupage** — 🔴 **sans intervention humaine.** 📌 **L'Arbitre
a écrit `code/redecoupage.md`**, l'agent s'est arrêté, **la commande
relance le découpage et poursuit sa boucle.** ⚠️ **Le Product Owner
n'attend sur rien.**

🔴 **Les fiches de tout lot non codé sont périmées** — 📌 **écrites
contre l'ancien découpage, elles sont supprimées.** ⚠️ **Un Détailleur
qui trouve une fiche ne la réécrit pas**, et détaillerait contre un lot
qui a changé de forme.

📌 **Le compte de lots ne repart pas** — 🔴 **un redécoupage n'en a
relu aucun.**

**4. `stop.md`** — 📌 **le Product Owner l'a posé pour arrêter
proprement.** 🔴 **Il se lit depuis le checkout principal, jamais depuis
un worktree** : ⚠️ **un worktree porte une copie figée à sa création et
ne verrait jamais un fichier créé après.** 📌 **`stop1.md` est sa forme
désarmée** — on renomme pour arrêter, on renomme en sens inverse pour
reprendre.

⚠️ **Un arrêt n'est pas un échec** : le lot qui vient de finir est
fusionné et poussé, rien n'est perdu.

## Ce que le redécoupage laisse intact

🔴 **Un lot dont le verdict porte PASS est clos.** ⚠️ **Ses entrées, ses
symboles et son numéro restent exactement tels quels** — 📌 **son code
est fusionné**, et changer ce qu'il déclarait décrirait quelque chose
qui n'est pas là.

🔴 **Là où un lot codé doit changer, on ajoute un lot** — 📌 **un lot qui
modifie ce qu'un précédent a construit**, déclarant ces symboles en
modifications comme n'importe quels autres.

🔴 **Un lot codé est derrière, quoi qu'il consomme** — ⚠️ **l'ordre dans
lequel il a tourné est un fait, pas un plan**, et rien ne peut le
mettre plus tard. 📌 **Un lot qui modifie ce qu'un lot codé a construit
passe en premier parmi ce qui reste.**

## Ce qui fait converger un redécoupage

🔴 **Le Cadreur lit les redécoupages précédents pour ce qui revient.**

📌 **Le même symbole deux ou trois fois** — la frontière est au mauvais
endroit, et recouper autour renverra une quatrième. 📌 **La même
entrée** — elle porte plus d'une nature, et aucune coupe le long d'elle
ne tiendra. 📌 **La même espèce de défaut** — ce qui est faux est le
critère de coupe, pas cette coupe-ci.

🔴 **Il écrit ce qu'il en fait**, et c'est ce champ qui fait
converger. ⚠️ **Sans lui, il recoupe autour du même point**, et le
cinquième redécoupage redit ce que le deuxième disait déjà.

## Les demandes de convention, entre deux lots

🔴 **À la fin de chaque lot, jamais pendant qu'un tourne.** 📌 **Le
fichier de conventions est ce que lit chaque agent du bloc suivant**, et
⚠️ **deux worktrees qui l'écrivent en même temps en perdent un.**

🔴 **À la fin du lot, pas du bloc.** ⚠️ **Une règle tranchée en fin de
bloc est tranchée après tous les lots qu'elle aurait dû gouverner** —
📌 **ainsi le lot suivant l'a.**

🔴 **Une seule invocation, quel que soit le nombre de demandes** —
⚠️ **jamais une par fichier** : il les lit toutes avant d'en trancher
une, et deux invocations écriraient le fichier de conventions en même
temps.

📌 **Une demande que l'Arbitre a levée en cours de lot est déjà
tranchée** — son verdict est rempli, et ce geste la saute.

---

# LES COMMANDES

*Ce que chacune décide, et pourquoi c'est elle qui décide.*

| Commande | Agents | Ce qu'elle produit |
|---|---|---|
| `/diagnostique` | diagnostiqueur | `desc-bug.md` — entrée d'un cycle de correction |
| `/7_lots` | cadreur *(qui appelle le vérificateur)* | Le découpage et la séquence |
| `/8_code` | detailleur · realisateur · relecteur · architecte · controleur | Le code, lot par lot |
| `/9_controle` | controleur | Le rapport d'intentions |
| `/conventions` | architecte | `TECHNICAL_CONVENTIONS.md` · `couverture.md` |
| `/deploie` | — *(script)* | Les deux applications sur les appareils |
| `/audit_blocages` · `/audit_conventions` | — *(l'orchestrateur seul)* | Deux rapports d'audit |

🔴 **Le dossier de travail est le `bugfix-NN/` le plus haut s'il en
existe un ; le dossier de la fonctionnalité sinon.** 📌 **Un cycle de
correction garde tout ce qu'il produit dans son propre dossier**, et la
structure est la même des deux côtés.

⚠️ **On passe le dossier de travail, jamais le dossier de la
fonctionnalité** — 🔴 **sur un cycle de correction ils diffèrent**, et
l'agent lirait le mauvais.

## `/diagnostique` — décide ce qui n'est pas à refaire

📌 **Elle découpe `bug-list.md` en écarts identifiés, un par appel**,
et passe le texte de chacun **verbatim**. 🔴 **Elle les lit pour les
distribuer, jamais pour les juger, les réécrire ou les fusionner.**

🔴 **Elle saute tout écart dont le rapport existe déjà** — ⚠️ **une
reprise coûte une investigation entière.** 📌 **C'est ainsi qu'une seule
investigation ratée se rejoue** : le Product Owner remplit son fichier
de blocage, relance la commande, et celle-là seule repart.

📌 **Un blocage en phase 1 n'annule pas la phase 2** — 🔴 **l'assemblage
compte les rapports contre `bug-list.md` et bloque de lui-même s'il en
manque un**, en nommant l'identifiant.

## `/7_lots` — décide ce que le Cadreur trouve, jamais ce qu'il fait

📌 **Une seule invocation.** 🔴 **Elle ne lance pas le Vérificateur et
elle ne boucle pas** — le Cadreur s'en charge.

🔴 **Elle ne dit rien dans le prompt de ce qui l'a rappelé** —
📌 **défauts ou redécoupage, le Cadreur les trouve seul**, et une
paraphrase entrerait en concurrence avec ses propres instructions.

**L'exception** : 📌 **un `code/redecoupage.md` est nommé dans le prompt
des deux agents** — ⚠️ **des lots sont déjà codés et fusionnés**, et
écraser leurs entrées décrirait quelque chose qui n'est pas dans
l'arbre.

**Ce qu'elle décide en sortie** :

| Ce qu'elle trouve | Ce qu'elle fait |
|---|---|
| Une séquence sans défaut | 🔴 **Le découpage tient** — elle traite les demandes en attente, puis s'arrête |
| Un blocage du Cadreur **et** une demande de convention | 📌 **L'Architecte, puis le Cadreur à nouveau** |
| Un blocage du Cadreur seul | 🔴 **Arrêt** — le Product Owner remplit la décision |

🔴 **Elle n'invoque jamais l'Arbitre.** 📌 **Ce sur quoi le Cadreur et
le Vérificateur bloquent est mécanique**, et rien de tout ça ne se règle
en regardant le corpus.

⚠️ **Un blocage au troisième tour n'est pas un échec de la commande** —
🔴 **le découpage ne converge pas, et c'est au Product Owner de
décider.**

## `/8_code` — décide où reprendre, et quand s'arrêter

🔴 **Elle décide où reprendre** : le premier lot de la séquence sans
verdict en PASS. 📌 **Aucun lot** — tous en PASS — **le Contrôleur, puis
fin.**

⚠️ **Des défauts non vides l'arrêtent** : le découpage n'a jamais été
corrigé.

🔴 **Elle décide quand s'arrêter, et la liste est courte** : un blocage
à décision vide · un lot qui échoue trois fois · `N` lots relus en
PASS · le Contrôleur qui a fini · `stop.md`. ⚠️ **Sinon elle ne
s'arrête jamais** — un FAIL isolé, un bloc terminé, une correction qui
passe : elle continue.

🔴 **Elle n'invoque jamais l'Arbitre.** 📌 **Le Détailleur et le
Réalisateur l'appellent eux-mêmes**, l'attendent, et ne s'arrêtent que
si le champ est revenu vide. ⚠️ **Un blocage qui lui parvient y est
déjà passé** — le renvoyer demanderait deux fois.

📌 **Une décision remplie n'est pas un arrêt** : elle invoque l'agent
qu'elle nomme, sur le lot qu'elle nomme. ⚠️ **Même sur un lot qui porte
déjà un PASS** — 🔴 **le Contrôleur signale les intentions manquantes
après que tous les lots ont été relus, et un blocage est la façon dont
elles reviennent.**

🔴 **Quand elle s'arrête sur un blocage, les demandes de convention
attendent** — ⚠️ **ne pas invoquer l'Architecte sur un lot qui n'a pas
fini** : ce qu'il demande peut changer avec la décision.

🔴 **Le compte porte sur les lots relus PASS**, pas sur les invocations
— 📌 **le Détailleur tourne à chaque nouveau bloc sans entrer dans le
compte.**

🔴 **Le Contrôleur ne tourne que si tous les lots de la séquence sont en
PASS**, pas seulement ceux de cette exécution — ⚠️ **il compare le
fichier produit à *toutes* les fiches**, et une fiche manquante lui
ferait signaler une intention comme absente.

## `/9_controle` — décide le groupement, et ne le décide pas seule

🔴 **`/8_code` ne lance pas le Contrôleur** — elle s'arrête une fois le
dernier lot passé et annonce cette commande. 📌 **C'est ici, et
seulement ici, qu'il tourne.**

🔴 **Sur le dossier de la fonctionnalité, jamais sur un `bugfix-NN/`** —
⚠️ **un cycle de correction n'a ni fichier produit ni traçabilité : il
n'y a rien à confronter.** 📌 **Et le Contrôleur n'est pas relancé après
un cycle de correction** : les lots d'un bugfix ne sont dans aucune
carte, son rapport redirait les mêmes manques.

**Elle construit la carte bloc → lots elle-même**, sans agent : 📌 **la
traçabilité donne bloc → entrées, les ancres du découpage donnent
entrée → lots**, et le croisement des deux donne la carte. 🔴 **Chaque
bloc y figure**, un tiret quand aucun lot ne cite ses entrées.

🔴 **Puis un script groupe, et le groupement se prend tel quel.**
⚠️ **Jamais de regroupement à la main, jamais de budget forcé** — 📌 **le
découpage doit être reproductible depuis la même entrée.**

🔴 **Elle s'arrête si un lot de la séquence n'est pas en PASS** — 📌 **il
lirait un jeu de fiches incomplet et signalerait une intention comme
manquante quand elle est seulement pas encore écrite.**

📌 **Un rapport existant n'est pas une raison de s'arrêter** — il en
écrit un numéroté à côté. ⚠️ **C'est une archive, pas une
comparaison.**

## `/conventions` — hors de la boucle, lancée à la main

📌 **Après `/6_convertit`, avant `/7_lots`** — 🔴 **le Cadreur lit les
conventions en entier ; elles doivent exister quand il le fait.**

⚠️ **`/cycle` ne l'appelle pas** — 📌 **le câblage attend que la grille
ait été mesurée sur un cycle réel.**

📌 **Le reste de cette commande appartient à l'amont** — voir
`PROCESS_AMONT.md`.

## `/deploie` — installe, et ne corrige rien

🔴 **Chaque appareil est identifié par son modèle, jamais par sa place
dans la liste.** ⚠️ **L'identifiant de la montre change à chaque
redémarrage du débogage sans fil** — 🔴 **relu à chaque exécution,
jamais de mémoire ni d'un rapport précédent.**

🔴 **Un appareil manquant arrête tout.** ⚠️ **Ne jamais installer
l'autre seul** : 📌 **un téléphone mis à jour contre une vieille version
de la montre échoue d'une manière qui se lit comme un défaut de code.**

🔴 **Une installation ratée est un résultat** — le rapport dit ce qui a
échoué et s'arrête là.

## `/audit_blocages` et `/audit_conventions` — l'orchestrateur seul

📌 **Aucun agent, aucune commande ne les appelle.** 🔴 **Elles lisent et
elles rapportent ; elles ne changent rien.**

🔴 **Elles s'ajoutent, elles ne réécrivent jamais** — 📌 **chaque passe
note les fichiers qu'elle a lus, et la suivante les saute.** ⚠️ **C'est
ce qui les rend peu chères à répéter.** 🔴 **Mais chacune relit ses
propres constats en entier** : 📌 **un motif se voit à travers les
passes, et une passe seule ne le verrait pas.**

**Ce que l'audit des blocages cherche** — 🔴 **des noms, jamais des
sujets.** 📌 **Deux blocages qui nomment un même symbole, fichier ou
module sont un constat** — ⚠️ **grouper sur ce dont les blocages parlent
serait un jugement**, et deux blocages tous deux *« sur un contrat
élargi »* peuvent ne partager aucun nom.

📌 **Puis ce qui compte vraiment** : 🔴 **une décision qui ne nomme rien
sur quoi elle repose** — ni règle, ni entrée, ni symbole où le même
problème est déjà résolu. ⚠️ **N'en nommant aucun, elle a inventé
quelque chose.**

**Ce que l'audit des conventions cherche** — 📌 **ce que le cycle a
ajouté** : une règle que la couverture ne trace à aucune entrée vient
d'une demande, pas du corpus. ⚠️ **C'est une règle que personne n'a lue
avant qu'elle ne lie tous les lots.**

📌 **Et ce qu'une règle coûte** : 🔴 **une règle qu'aucun lot ne peut
suivre dans sa propre portée** — elle demande ce qu'un lot ne peut pas
fournir seul, et le blocage arrive bien plus tard, au détaillage.
🔴 **Une règle que le découpage ne rencontre jamais** — ⚠️ **elle coûte
une lecture à chaque lot et n'attrape rien.**

⚠️ **Aucune recommandation, aucune correction.** 🔴 **Elles rapportent
ce que les fichiers disent** ; quoi en faire est au Product Owner.

---

# LES FICHIERS

| Fichier | Écrit par | Lu par |
|---|---|---|
| `spec-technique.md` · `desc-bug.md` | L'amont · **Diagnostiqueur** *(inv. 2)* | Cadreur *(en entier)*, Vérificateur et Détailleur *(les entrées citées)* |
| `bug-list.md` | Product Owner, hors ligne | Diagnostiqueur *(inv. 2)*, Fusionneur *(amont)* |
| `investigation/<id>.md` | Diagnostiqueur *(inv. 1)* | Diagnostiqueur *(inv. 2)* |
| `code/decoupage.md` — 📌 **l'inventaire des symboles, puis la liste des lots** | **Cadreur** | Vérificateur *(qui croise l'inventaire contre les lots)*, Détailleur, Arbitre, `/9_controle` |
| `code/sequence.md` | **Vérificateur** | 🔴 **La commande**, le Détailleur, le Cadreur *(ses défauts)* |
| `code/<lot>/fiche-executable.md` | **Détailleur** | Réalisateur, Relecteur, Contrôleur |
| `code/<lot>/compte-rendu.md` | **Réalisateur** | Relecteur · **grepé** par le Détailleur du bloc suivant |
| `code/<lot>/verdict.md` | **Relecteur** | 🔴 **La commande**, le Réalisateur *(sur FAIL)*, l'Arbitre *(son statut seul)* |
| `code/<lot>/reprise_realisateur.md` | Réalisateur, en s'éteignant | Le Réalisateur suivant |
| `code/redecoupage.md` | **Arbitre** | Cadreur, Vérificateur *(qui l'archive)* |
| `code/controle/<groupe>.md` | Contrôleur *(inv. 1)* | Contrôleur *(inv. 2)* |
| `code/rapport-controle.md` | Contrôleur *(inv. 2)* | Product Owner |
| `architecte/<demandeur>.md` | Cadreur · Détailleur · Réalisateur · Arbitre — **`## Verdict` par l'Architecte** | Architecte *(inv. 3)*, leur auteur |
| `docs/TECHNICAL_CONVENTIONS.md` | **Architecte, seul** | Cadreur, Détailleur, Réalisateur, Relecteur, Arbitre — 🔴 **en entier** |
| `docs/CURRENT_TECHNICAL_STATE.md` | **Réalisateur** | Détailleur, Réalisateur, Diagnostiqueur |
| `tracabilite-full.md` | 🔴 **La commande `/9_controle`** | Le script de groupement |
| `audit-blocages.md` · `audit-conventions.md` | 🔴 **L'orchestrateur** | Lui-même, passe après passe |
| `blocked_<agent>.md` | L'agent · **Product Owner** pour la `## Decision` · **Arbitre** pour deux d'entre eux | L'agent, l'Arbitre, la commande *(cette ligne seule)* |
| `stop.md` | Product Owner, à la main | 🔴 **La commande, depuis le checkout principal** |

📌 **Deux fichiers pilotent la boucle** : 🔴 **la séquence dit quel lot
vient**, **le verdict dit s'il est passé.** ⚠️ **Tout le reste est lu
par un agent ; ces deux-là sont lus par la commande.**

## Ce que l'état technique fait de particulier

🔴 **Il est vivant** — le seul fichier de la chaîne aval qu'un agent
réécrit lot après lot. 📌 **Il décrit ce qui existe, jamais l'histoire
de ce qui a existé** : ⚠️ **ce qu'un lot a rendu faux disparaît.**

🔴 **Deux de ses sections se lisent en entier, le reste se grepe** —
📌 **les pièges généraux et l'état mort** : ⚠️ **on ne peut pas greper
une règle dont on ignore qu'elle s'applique à soi**, et c'est pour ça
que ce sont des sections et non des entrées.

📌 **Un piège change une signature** pour le Détailleur, **et la façon
d'écrire** pour le Réalisateur.

🔴 **Le Cadreur ne le lit pas** — ⚠️ **un lot est déclaré production ou
modification contre le code, par grep, jamais contre ce document.**
📌 **C'est le principe de la chaîne** : le code est la vérité, ce
document est un cache. **Un cache qui aurait dérivé ferait déclarer
*production* un symbole qui existe.**

---

# LES MÉCANIQUES PROPRES À L'AVAL

*📌 **La forme des fichiers de blocage, l'écriture d'une sortie même
vide, les chemins relatifs en worktree et l'enveloppe git des commandes
vivent dans `PROCESS_AMONT.md`.** Ce qui suit est ce que l'aval y
ajoute.*

## Le blocage passe d'abord par l'Arbitre

🔴 **Un Détailleur ou un Réalisateur qui bloque ne s'arrête pas là** :
📌 **il écrit son fichier, appelle l'Arbitre, et attend.** ⚠️ **Un
blocage qui atteint la commande y est déjà passé.**

📌 **Les autres agents n'ont pas ce recours** : 🔴 **ce sur quoi le
Cadreur et le Vérificateur bloquent est mécanique**, et 🔴 **un blocage
du Relecteur ou du Contrôleur dit que quelque chose manque** — l'agent
qui le devait doit retourner.

## Une décision peut renvoyer au découpage

🔴 **C'est la seule issue qui traverse toute la chaîne à rebours.**
📌 **L'Arbitre écrit ce que le découpage doit permettre** — ⚠️ **la
contrainte, jamais la solution.**

🔴 **Le champ qui compte est le dernier, et c'est celui qu'on rate** :
📌 **nommer ce qui doit devenir possible, jamais comment couper pour
l'obtenir.**

## Les demandes de convention, quatre demandeurs

🔴 **Quatre agents en écrivent** — le Cadreur, le Détailleur, le
Réalisateur, l'Arbitre. 📌 **Tous décrivent ce qui leur manque, jamais
la règle elle-même** : ⚠️ **ils ne savent pas si c'en est une**,
l'Architecte le sait.

🔴 **Trois d'entre eux ne bloquent jamais dessus** : le Détailleur et le
Réalisateur écrivent la demande et continuent contre les conventions
telles qu'elles sont. 📌 **Le Cadreur est l'exception** : ⚠️ **une
convention qui interdit ce qu'un lot exige l'arrête**, et il écrit
alors **deux fichiers** — le blocage, et la demande à côté. 🔴 **C'est
leur présence conjointe que la commande lit** pour savoir s'il faut
passer par l'Architecte ou rendre la main.

⚠️ **Le Cadreur ne contourne jamais** — 📌 **ni en coupant le lot
autrement, ni en déclarant moins que ce qu'il exige.** 🔴 **Les
conventions ont été écrites avant le découpage, et le découpage est ce
qui montre ce qu'elles ont manqué.**

## Une demande laisse une trace dans ce que son auteur écrit

🔴 **Le Cadreur la nomme dans son découpage, le Détailleur dans sa
fiche, le Réalisateur dans son compte rendu.** ⚠️ **Sans ça, une
demande écrite en passant est invisible** : 📌 **le Détailleur ne laisse
aucun rapport, et ce champ est sa seule trace.**

## La reprise d'un Réalisateur éteint

🔴 **Quand la décision revient vide, il écrit `reprise_realisateur.md`
et s'arrête.** 📌 **Un Réalisateur neuf reprendra le lot avec sa fiche,
le fichier de blocage une fois rempli, et ce fichier.** ⚠️ **Il n'a rien
de son contexte** — ce fichier est tout ce qu'il obtient.

🔴 **Le champ qui compte est *En chantier*** — ⚠️ **du code à moitié
écrit et non nommé est du code que le suivant découvre au build.**

📌 **Il commite ce qui compile avant de s'arrêter** — 🔴 **jamais ce qui
ne compile pas** — et dit dans ce champ ce qu'il a laissé non commité.

⚠️ **Rien de tout ça quand la décision renvoie au découpage** :
🔴 **le lot va changer de forme**, et une reprise décrirait un lot qui
n'existe plus.

---

# CONTRADICTIONS RELEVÉES

*Points où deux fichiers, ou un fichier avec lui-même, ne disent pas la
même chose. Non tranchés ici.*

🟡 **Renommer ou supprimer un fichier de blocage appliqué.** Cinq
agents — Vérificateur, Détailleur, Réalisateur, Relecteur, Contrôleur —
disent **les deux dans le même fichier** : *« applique-la, puis renomme
en `blocked_<agent>-NN.md` »*, puis, quelques lignes plus bas,
*« 🔴 supprime le fichier une fois appliqué »*. 🔴 **Le Cadreur dit
l'inverse explicitement** : *« renommer est ce qui le clôt — ne le
supprime jamais »*. ⚠️ **Les fichiers numérotés sont décrits partout
comme l'archive de ce sur quoi le cycle a déjà bloqué, que l'exécution
suivante lit** — ce qui ne tient que si on renomme.

🟡 **Ce que `/7_lots` écrase.** La commande annonce qu'elle **produit
toujours un découpage** et qu'un `code/decoupage.md` existant est
écrasé — *« la commande est le déclencheur, jamais l'état du
dossier »*, la seule exception nommée étant un `code/redecoupage.md`.
🔴 **Le Cadreur, lui, traite une reprise à froid sur des défauts** :
*« ne corrige que les lots nommés »*, et **les dix gestes ne sont pas
rejoués.** ⚠️ **Deux comportements pour un même appel.**

🟡 **Renommer ou supprimer : tranché.** 📌 **Les cinq agents renomment
désormais**, comme le Cadreur et comme le PROCESS le décrivent —
📌 **les fichiers numérotés sont l'archive que l'exécution suivante
lit**, et A5 en fait la source d'un registre.

🟡 **Comment `/8_code` invoque le Contrôleur : tranché.** 📌 **Elle ne
l'invoque pas.** ⚠️ **Elle se contredisait elle-même** : son en-tête
disait *« elle n'invoque jamais le Contrôleur — il a besoin de ses
blocs et de ses fiches, que ni l'un ni l'autre ne se déduit »*, et sa
section *Where to resume* disait *« va droit au Contrôleur »*. 🔴 **La
seconde est corrigée** : tous les lots en PASS, la commande s'arrête et
annonce `/9_controle`. 📌 **La machinerie des groupes vit là, et
seulement là.**

📌 **Un point vérifié, et il tient** : les modèles annoncés par
`.claude/CLAUDE.md` — neuf agents en `opus`, dont `arbitre`, `cadreur`,
`detailleur` et `verificateur` pour l'aval — correspondent exactement
aux frontmatters, et aux modèles que `/7_lots` et `/8_code` passent.
