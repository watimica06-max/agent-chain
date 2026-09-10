# Process amont — de l'idée au document technique

> Documentation de référence. Décrit la chaîne **idée produit →
> document technique exploitable par le Cadreur** — l'entrée du process
> aval, décrit dans `PROCESS_AVAL.md`.
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

## La frontière avec l'aval

**L'aval commence au document technique.** Tout ce qui précède est
l'amont, avec une différence de nature qu'il faut garder en tête tout
du long :

🔴 **L'aval n'a presque pas besoin du Product Owner une fois lancé.**
L'amont en a besoin à chaque tour — une idée informelle ne devient
précise que par les réponses qu'elle obtient. Ce n'est pas un défaut à
corriger, c'est la nature du travail. Mais ça interdit d'appliquer tel
quel le principe d'enchaînement silencieux de l'aval.

📌 **D'où la forme de tout l'amont** : une boucle de fichiers de
questions, remplis à la main, hors session, sur le temps du Product
Owner.

---

## Le principe qui tient toute la chaîne

🔴 **Un agent ne regarde jamais le dossier.** On lui nomme le fichier
qu'il lit, l'invocation qu'il est, les blocs qu'il traite. **La
commande a regardé ; lui ne regarde pas une seconde fois.**

**Trois défaillances que ça empêche :**

⚠️ **Un agent qui cherche ouvre ce qu'il ne doit pas lire.** La moitié
des interdits de la chaîne portent sur des fichiers voisins — un
fichier de questions d'un autre agent, `idees.md`, une version périmée
du document technique.

⚠️ **Un agent qui déduit son état d'un dossier se trompe de tour.**
Quatre invocations du Lexicographe se distinguent par ce qui traîne à
la racine ; c'est le rangement fait par les commandes qui les sépare,
et lui n'a aucun moyen de le savoir.

⚠️ **Un agent dont le dossier cible manque ne s'arrête pas — il
cherche.** Il liste, il tente un chemin absolu, il écrit à côté.
📌 **La commande crée le dossier avant d'invoquer**, et rien de tout ça
n'arrive.

🔴 **Corollaire** : ce que les commandes décident est aussi structurant
que ce que les agents font. Les deux sont documentés ici.

---

# LES AGENTS

*Neuf agents. Chacun existe parce qu'un agent voisin ne peut pas faire
son travail sans se contredire.*

---

## Le Lexicographe

**À quoi il sert** — 📌 **Le Product Owner écrit librement, et c'est
tout l'intérêt.** 🔴 **Une même chose y prend plusieurs noms** : un mot
anglais et un français, un terme et son abréviation, un mot pour deux
choses.

⚠️ **Rien en aval ne rattrape ça.** Le Rédacteur transcrit fidèlement —
🔴 **il porte l'ambiguïté dans soixante blocs**, et tous les agents
suivants en héritent. **Le Lexicographe la lève à la source, dans le
fichier d'idées lui-même.**

📌 **C'est le seul agent qui écrit dans `idees.md`.**

**Ce qui le déclenche** — 🔴 **Quatre invocations, deux boucles.**

| # | Ce qu'elle fait | Quand |
|---|---|---|
| 1 | Balaye les termes, lève les paires | Avant le fichier produit |
| 2 | Applique les réponses, écrit `lexique.md` | idem |
| 3 | Surveille les réponses de la grille | À chaque tour de grille |
| 4 | Corrige ces réponses, complète le lexique | idem |

    1 → questions → répondu → 2 → 1 → …          avant le produit
    3 → questions → répondu → 4                  à chaque tour

⚠️ **Un fichier de questions vide clôt l'une ou l'autre.**

🔴 **1 et 2 ne tournent plus une fois `desc-produit.md` écrit.** 📌 Un
terme changé alors laisserait soixante blocs portant l'ancien.

**Pourquoi 3 et 4 existent** — 🔴 **Les réponses du Product Owner
portent des mots que personne n'a balayés.** Deux balayages sur ces
réponses seules :

📌 **Un terme retiré** — un grep sur `lexique.md` le trouve. ⚠️ **Ce
n'est pas une question** : la décision est prise, l'invocation 4
remplace.

📌 **Un synonyme neuf** — un mot que le lexique ne porte nulle part,
désignant une chose qu'il porte déjà. 🔴 **C'est celui-là qui coûte** :
aucun grep ne l'attrape, et il entre dans le fichier produit comme
second nom d'une seule chose.

**Deux natures de mot, deux règles**

| | Écrit | Ce qu'il devient |
|---|---|---|
| **Un texte affiché** | Entre guillemets, dans sa langue | Reste tel quel, partout |
| **Un concept** | Sans guillemets | 🔴 **En anglais**, dès le fichier produit |

⚠️ **Un même mot peut être les deux** — le bouton *« Démarrer »* et le
concept *race start*. **Deux entrées, pas une.**

**Ce que porte `lexique.md`** — deux sections, `## Tranché` et
`## Non tranché`. 🔴 **Les termes retirés y sont écrits sous celui qui
tient** — ⚠️ **c'est ce qui rend le grep de l'invocation 3 possible.**
Les jeter les rendrait invisibles.

🔴 **Un terme tranché sans rival y va aussi** : le tour suivant grepe ce
fichier, et ce qui n'y est pas n'existe pas.

**La frontière** — 🔴 **Il propose une lecture, jamais un terme.**
📌 Trois lectures sont possibles — *deux noms d'une chose*, *deux choses
distinctes*, *une abréviation locale* — et dire laquelle il voit est
tout son travail. **Le vocabulaire appartient au Product Owner.**

🔴 **Il n'ouvre jamais le fichier produit**, à aucune invocation. 📌 Ce
qu'il dit est tranché ; ce qu'une réponse dit ne l'est pas.

---

## Le Rédacteur

**À quoi il sert** — Il transforme ce que le Product Owner écrit en
fichier produit structuré. 🔴 **C'est le seul agent qui écrit
`desc-produit.md`.**

🔴 **Il ne converse jamais.** Le Product Owner écrit hors ligne et
remplit les champs `Answer:` à la main. **Il transcrit, structure et
traduit.**

🔴 **Il ne tranche jamais rien de produit.** Ce qui manque devient une
question, pas une hypothèse.

**Ce qui le déclenche** — deux invocations :

| # | Entrées | Sortie |
|---|---|---|
| 1 — Structurer | `idees.md` · `lexique.md` · l'index du global | Le fichier produit |
| 2 — Intégrer | 🔴 **Le fichier de questions que le prompt nomme** · `lexique.md` · l'index du global | Le fichier produit, à jour |

📌 **L'invocation 2 sert tout fichier de questions rempli** — celui d'un
sondeur, du Convertisseur, du Fusionneur, le sien. **Même travail quel
que soit le demandeur.**

**Structurer, c'est quatre gestes** — 🔴 **et le premier porte tout le
reste.**

**Décomposer.** 🔴 **Ce que le Product Owner écrit est un flux, pas une
liste.** Une phrase peut porter cinq sujets.

🔴 **Un sujet est un déclencheur et une sortie.** Deux déclencheurs, ou
deux sorties, font deux sujets. ⚠️ **Lire ce qui déclenche, pas le
sujet grammatical** — une phrase qui s'ouvre sur ce que l'utilisateur
voit peut être déclenchée par un échec ou un minuteur.

🔴 **La forme que le Product Owner donne à son idée n'est pas la forme
de ses sujets.** ⚠️ **Une carte de navigation est le piège** : une seule
forme, autant de sujets que de chemins — la transcrire d'un bloc
enterre toutes les transitions sauf la première.

**Chercher le titre dans l'index du global**, par grep, sur tout
l'index et pas seulement les sections chargées. 🔴 **Un titre proche est
un doute, et un doute se lève par une lecture** : même déclencheur, même
sortie ?

**Ranger.** 📌 **Le déclencheur sépare les sujets** — un bloc par sujet,
sous le titre trouvé ou créé. 🔴 **Avec une ligne `Nature:` vide** :
📌 **c'est le Classeur qui la remplit**, après le Découpeur.

**Signaler ce qu'il ne comprend pas**, en place, dans le bloc :
`**Clarification needed:**` — 🔴 **et jamais parce qu'il détecte un
trou.** Chercher les trous est le travail des sondeurs.

**Les deux marqueurs** — 🔴 `NEW` sur tout bloc créé, `MODIFIED` sur
tout bloc changé, ⚠️ **qu'une question l'ait nommé ou non.**

📌 **Ce ne sont pas la même chose** : un bloc neuf n'a jamais été fermé ;
un bloc changé l'a été, contre un texte qui ne tient plus.

🔴 **Il efface tous les marqueurs avant d'écrire**, pour que seuls ceux
du tour en cours restent. ⚠️ **Sans marqueur, le bloc ne sera jamais
resondé** — c'est ce que les sondeurs et le Découpeur grepent.

**Intégrer, c'est se demander de chaque réponse où elle va** —
🔴 **l'identifiant de la question dit où elle s'applique, pas où elle
vit.** Une réponse à une question sur B7 devient un bloc à elle si son
déclencheur ou sa sortie diffère. **Même test qu'au geste 1** : même
déclencheur, même sortie ?

🔴 **La réponse qui contredit une phrase la remplace**, elle ne s'assied
pas à côté.

📌 **Une réponse dont la question portait `Block: -` est là d'où vient
le plus souvent un sujet neuf** — ⚠️ **elle a été posée de la
fonctionnalité, et rien en elle ne dit où elle atterrit.**

🔴 **Il marque chaque entrée intégrée** — `[integrated: B7]`, nommant
tous les blocs où il a écrit. **En dernier**, une fois toutes les passes
faites : un bloc créé en cours de route doit y figurer.

**La frontière** — avec le Découpeur : 🔴 **il scinde ce qu'une réponse
lui dit de scinder ; le Découpeur scinde ce qu'un bloc s'est révélé
porter.** Avec les sondeurs : il signale en place ce qu'il ne comprend
pas, eux cherchent ce que le document ne dit pas.

---

## Le Découpeur

**À quoi il sert** — 📌 **Le Rédacteur écrit un bloc depuis un
passage.** 🔴 **Un passage peut porter deux choses que rien ne déclenche
pareil** — le bloc se lit alors comme un sujet quand il en porte deux.

⚠️ **Rien en aval ne le rattrape.** 📌 **Les sondeurs sondent le bloc
comme un seul**, et ses propres réponses ferment les questions que son
autre moitié aurait levées. **Le trou disparaît sans que personne le
voie.**

**Ce qui le déclenche** — une invocation, entre `/2_structure` et
`/3b_nature`, **à chaque tour**. Sur les blocs `NEW` et `MODIFIED`, ou
sur tous au premier tour.

🔴 **Une ligne `**Clarification needed:**` dans un bloc nommé
l'arrête** — ⚠️ ce bloc a été transcrit sur une lecture que personne n'a
confirmée, et le découper figerait une forme qui va changer.

**La règle, une seule** — 🔴 **un bloc porte un déclencheur.**

📌 **Les valeurs que ce déclencheur peut prendre restent dedans** —
⚠️ **un déclencheur qui distingue trois cas donne un bloc à trois cas,
pas trois blocs.**

🔴 **Un autre déclencheur est un autre bloc.** ⚠️ **Deux données
différentes sont deux déclencheurs**, même quand la question posée de
chacune est la même.

📌 **Ce que rien ne déclenche est un bloc aussi** — une table de
référence, un catalogue de valeurs.

**La frontière** — 🔴 **Il déplace, il ne rédige pas.** Ni réécrire une
phrase, ni en ajouter une, ni en supprimer une, ni fusionner deux blocs.
🔴 **Chaque phrase du bloc découpé atterrit dans un bloc et un seul.**

🔴 **Il laisse `Nature:` vide sur chaque bloc qu'il écrit**, celui qui
garde le titre d'origine compris. ⚠️ **Un découpage laisse rarement deux
moitiés d'une seule nature** — 📌 **et une ligne vidée est ce qui dit au
Classeur de regarder.**

📌 **Pourquoi si étroit** : c'est l'un des trois agents qui touchent au
fichier produit, et le seul qui en déplace le texte. **Lui laisser
reformuler, c'est deux plumes sur un document dont la fusion se fait
phrase à phrase.**

---

## Le Classeur

**À quoi il sert** — 📌 **La nature d'un bloc décide deux choses en
aval.** 🔴 **Quelles questions la grille lui pose** — on ne demande pas à
un bloc `screen` ce qu'on demande à un bloc `persistence`. 🔴 **Et quelle
section du document technique le porte** — autrement dit, quelle couche
du code.

⚠️ **Une nature fausse ne se rattrape pas plus loin.** 📌 **La grille
ferme le bloc sur les mauvaises questions**, et la fermeture se lit comme
propre.

🔴 **Pourquoi il existe** : **le Rédacteur choisissait la nature sur
douze mots, le Convertisseur la re-dérivait sur douze définitions** —
⚠️ **ils divergeaient, et personne ne le voyait.** 📌 **Un seul juge
maintenant**, et le Convertisseur lit la ligne au lieu de la dériver.

**Ce qui le déclenche** — une invocation, entre `/3_decoupe` et
`/4_grille`, **à chaque tour.** 🔴 **Sur les blocs dont la ligne
`Nature:` est vide, et sur ceux marqués `MODIFIED`.**

📌 **C'est la ligne vide qui rend ça greppable** — 🔴 **le Rédacteur et
le Découpeur écrivent `Nature:` sans rien après, jamais ne l'omettent.**
⚠️ **Une ligne absente et une ligne oubliée se liraient pareil.**

**La règle** — 🔴 **la nature d'un bloc est ce qu'il produit, jamais ce
qui le déclenche.** 📌 **Un bloc qui produit un affichage est `screen`**,
même déclenché par un événement ; **une règle déclenchée par un capteur
prend la nature de ce qu'elle calcule.**

⚠️ **Un cas d'échec ne nomme pas une nature** — 📌 **une lecture locale
échoue aussi** : ce qui fait qu'un bloc est `external source` est d'où
la donnée vient.

🔴 **Une nature par bloc, toujours.** ⚠️ **Un bloc qui semble en vouloir
deux a été mal découpé** — 📌 **il le dit plutôt que de choisir.**

**Sur un bloc `MODIFIED` qui porte déjà une nature** — 🔴 **il repose la
question et compare.** 📌 **Même réponse, il ne change rien** ;
⚠️ **réponse différente, il écrit la nouvelle** — 🔴 **et ce bloc avait
été fermé par la grille sur les mauvaises questions**, ce que son
marqueur renvoie sonder.

**La frontière** — 🔴 **Il écrit cette ligne, et rien d'autre.** Ni une
phrase, ni un titre, ni un marqueur. 🔴 **Il ne découpe ni ne fusionne** :
c'est le Découpeur. 🔴 **Il ne remplit pas une ligne déjà remplie**, sauf
sur un bloc `MODIFIED`.

⚠️ **Hésiter n'est pas bloquer** : 📌 **un bloc dont il pèse la nature
entre deux prend celle que sa sortie nomme**, et il dit lesquelles il a
pesées. 🔴 **Il bloque quand aucune nature ne convient** — 📌 **ce qui
veut dire que le bloc porte deux sujets, ou aucun.**

---

## Le Sondeur

**À quoi il sert** — 📌 **Le fichier produit dit ce que
l'application fait.** 🔴 **Ce qu'il ne dit pas, le code le décidera** —
et personne ne saura qu'une décision a été prise.

**Il pose chaque question de la grille et écrit ce qui reste ouvert.**

**Ce qui le déclenche** — 🔴 **Trois sondeurs en parallèle, sur le même
document et la même grille, dans trois ordres de lecture différents** :
bloc par bloc, question par question, nature par nature.

📌 **L'union de ce qu'ils lèvent est la sortie du tour** — ⚠️ **pas ce
sur quoi ils s'accordent.**

🔴 **L'ordre de lecture est la seule chose qui les distingue**, et c'est
la commande qui le nomme. ⚠️ **Un ordre dont l'un dérive est un ordre
que personne n'a couvert.**

🔴 **Aucun ne lit la sortie d'un autre**, ni les questions d'un tour
précédent. 📌 **Son regard sur le document doit rester agnostique** — il
cesse de l'être dès qu'une question entre dans son contexte.

**Ce qu'il cherche** — 🔴 **un trou, et rien d'autre.** 📌 **Ce que le
document ne dit pas et que le code devra décider.** ⚠️ **Pas une règle
qu'il trouve étrange, pas une décision qu'il aurait prise autrement.**

**Chaque question de la grille a trois issues :** le bloc la ferme —
on passe ; le bloc la laisse ouverte — c'est un trou ; elle ne
s'applique pas ici — on passe.

🔴 **Fermée veut dire que la réponse est là, dans les termes que la
question demande** — ⚠️ **pas que le bloc traite le même sujet.**
📌 **S'il faut interpréter pour la trouver, elle n'y est pas.**

🔴 **En doute, il pose plutôt qu'il n'écarte** — 📌 une question écartée
à tort ne revient jamais ; une question de trop coûte une ligne.

**Quels blocs** — 🔴 **la passe A ne porte que sur les blocs que la
commande nomme.** ⚠️ **Les passes B et C tournent en entier, à chaque
tour** — 📌 **elles lisent le document tel qu'il est maintenant**, et ce
qui a changé dans un bloc change ce qui se croise.

**La frontière** — 🔴 **Il n'écrit jamais dans le fichier produit.**
🔴 **Il ne ferme jamais un trou de passe A parce qu'un autre bloc y
répond** — c'est le travail de la passe B, et d'elle seule.

**La ligne `Block:`** — 🔴 **des identifiants seuls, séparés par des
virgules.** ⚠️ **Un titre rend la ligne illisible à qui groupe par
bloc.** 📌 **Plusieurs identifiants quand le trou est entre deux blocs**,
`-` quand la question a été posée de la fonctionnalité.

---

## L'Assembleur

**À quoi il sert** — 📌 **Trois lectures d'un même document lèvent le
même trou sous deux formulations**, et le Product Owner y répondrait
deux fois.

⚠️ **Il supprime ce qui est demandé deux fois, et rien d'autre.**

**Ce qui le déclenche** — une invocation, après les trois sondeurs. 🔴
**La commande vérifie que les trois fichiers existent avant de
l'appeler** — ⚠️ une fusion à laquelle il manque une lecture est une
fusion dont personne ne peut se servir.

**Comment il compare** — 🔴 **bloc par bloc.** Il rassemble toutes les
questions dont la ligne `Block:` nomme `B7`, les compare entre elles,
puis passe au bloc suivant.

🔴 **Une question nommant deux blocs entre dans les deux groupes** —
⚠️ **un trou entre deux blocs est levé des deux côtés**, et ne le
comparer que dans un groupe laisse debout son jumeau dans l'autre.

🔴 **Jamais de comparaison entre groupes** — 📌 deux questions ne
partageant aucun bloc sont deux questions différentes, quoi qu'elles
disent.

**Le critère** — 🔴 **deux questions sont la même quand répondre à
l'une répond à l'autre.** ⚠️ **Répondre, pas formuler.** 📌 Trois
lectures lèvent un trou sous trois angles — l'une part de ce qu'une
table porte, l'autre de ce qu'un message promet, la troisième de ce
qu'une règle accepte. **Lire au-delà de l'angle, jusqu'à la réponse qui
fermerait.**

🔴 **En doute, garder les deux.** ⚠️ Un doublon coûte une réponse ; un
trou supprimé coûte une ligne de code fausse.

🔴 **Une question levée par un seul sondeur est gardée, toujours.**
📌 **C'est exactement ce pour quoi on en lance trois** — ⚠️ **l'accord
n'est pas le test.**

**La frontière** — 🔴 **Il n'ouvre pas le fichier produit.** 📌 **Il
compare des questions entre elles**, jamais à ce qui y répondrait.
🔴 **Il ne réécrit aucune question**, même pour la raccourcir. Quand
deux disent la même chose, il garde celle qui l'énonce le plus
précisément.

---

## Le Convertisseur

**À quoi il sert** — Il transforme le fichier produit en document
technique numéroté, celui que le Cadreur découpe en lots.

🔴 **Il ne tranche jamais rien.** Une contradiction entre blocs, une
question sans réponse : il signale, il ne comble pas.

🔴 **Il n'est pas le filet de la chaîne amont.** La grille de cadrage a
balayé les précisions manquantes et les références pendantes, autant de
passes qu'il l'a fallu. **Il lève ce qu'une lecture fraîche attrape, pas
ce qu'elle a déjà couvert.**

**Ce qui le déclenche** — deux invocations, séparées par un aller-retour
de questions.

| # | Ce qu'elle fait | Sortie |
|---|---|---|
| 1 — Fermer | Partie 1 de la grille de fermeture sur chaque bloc | Un fichier de questions · 🔴 **supprime le document technique s'il existe** |
| 2 — Produire | Partie 2, une fois toutes les sections remplies | `spec-technique.md` · `tracabilite.md` · un fichier de questions |

📌 **Deux, pas une** : ⚠️ **deux régimes différents.** La fermeture lit
sans écrire ; la production traduit en termes techniques.

🔴 **La grille de fermeture porte les tests, l'agent porte les gestes.**
Elle vit dans `docs/process/GRILLE_FERMETURE_TECHNIQUE.md`, en deux
parties — l'une à la fermeture, l'autre à la production. ⚠️ **À ne pas
confondre avec la grille de cadrage produit**, que les sondeurs
déroulent et qu'il n'ouvre jamais.

🔴 **Il lit la nature sur la ligne `Nature:` du bloc, il ne la re-dérive
jamais.** 📌 **Le Classeur l'a posée** — ⚠️ **et la grille a posé au bloc
les questions de cette nature** : un second avis ici fermerait le bloc
contre des questions que personne n'a posées. 📌 **Les douze lui servent
dans l'ordre où le document technique les prend.**

**Pourquoi l'invocation 1 supprime le document technique** — 🔴 **le
fichier produit a bougé depuis qu'il a été écrit.** Le laisser
enverrait l'invocation 2 en mise à jour ciblée sur un document qui ne
correspond plus.

**Deux régimes à l'invocation 2**, décidés par un seul test :

| `spec-technique.md` | Ce qu'il fait |
|---|---|
| Absent | Production complète |
| Présent | 🔴 **Mise à jour ciblée** — grep `<<ASSUMED`, remplacer chaque marque par sa réponse, ne toucher à rien d'autre |

**Ce qu'une question coûte** — 🔴 **la question à se poser est : sans
ça, puis-je écrire la règle du tout ?**

| La réponse | Ce qu'il fait |
|---|---|
| **Non** — la règle n'existe pas sans | Demander, **n'écrire aucun document**, et supprimer celui qui existe |
| **Oui, en supposant** | Demander, **et produire** — la supposition marquée sur place |

🔴 **La marque porte l'identifiant qui la lèvera** :
`<<ASSUMED questions-convertisseur-04 Q2: …>>`. 📌 **Elle dit que la
ligne est provisoire**, et où sa réponse viendra.

**Ce qui devient une entrée numérotée** — 🔴 **une règle ou une table.**

> **Une règle qu'on peut couper en deux règles complètes fait deux
> entrées. Une qu'on ne peut pas couper sans laisser un cas ouvert
> reste une.**

⚠️ **Une entrée n'est pas un bloc produit.** 📌 **Le fichier produit
sépare par déclencheur, pour fermer chaque comportement ; le document
technique sépare par ce qui reste complet seul.** **Un bloc peut donner
deux entrées, deux blocs une seule.**

🔴 **Numérotées à l'écriture, jamais renumérotées.** ⚠️ **Un lot cite
`§3.7`**, et cette citation doit tenir d'une exécution à l'autre — d'où
l'ordre de remplissage imposé, §1 à §12 puis l'ordre des blocs, sans
aucun tri par jugement.

📌 **Une section vide est une information**, pas un oubli : elle dit au
Cadreur qu'il n'y a rien de cette nature. **On part des douze et on
laisse vide, jamais l'inverse.**

**Le préambule** — 🔴 **il cadre, il ne produit aucun lot.** Entièrement
repris du fichier produit, rien de déduit.

🔴 **Une règle transversale contraint sans rien produire.** 📌 **Le
test** : si personne ne l'écrit, est-ce que le code manque quelque
chose ? **Oui → c'est une entrée numérotée**, pas un bloc de préambule.
Les tokens d'un thème, un catalogue de formats, une table de seuils
répondent oui.

📌 **Les dépendances du préambule viennent du Rédacteur, pas de lui** —
seul le Rédacteur a le global sous les yeux.

**`tracabilite.md`** — 🔴 **une ligne par bloc du fichier produit**, dans
l'ordre : son identifiant, son titre, les entrées qui portent au moins
une de ses règles, ou un tiret.

🔴 **Tous les blocs y figurent, ceux que rien ne porte compris** —
⚠️ **un tiret dit qu'on a cherché et rien trouvé ; une ligne absente ne
dit rien du tout.**

📌 **Il le sait en écrivant** : chaque entrée est écrite depuis des
blocs qu'il a sous les yeux. **Le fichier consigne ce qu'il a fait, ce
n'est pas une seconde passe.**

**La frontière** — 🔴 **Il ne groupe pas en unités de travail.** Le
Cadreur le fait, avec le document d'état sous les yeux et les symboles
grepés. **Un groupement fait ici déciderait pour lui, à l'aveugle.**

🔴 **Il ne lit jamais le code**, ni le global, ni `idees.md`, ni un
fichier de questions — sauf les entrées qu'une marque `<<ASSUMED`
nomme.

---

## L'Architecte

**À quoi il sert** — Il écrit `docs/TECHNICAL_CONVENTIONS.md`, le
fichier que chaque agent de code lit en entier avant d'écrire une
ligne.

🔴 **Il répond à *comment on code ici*, jamais à *quoi construire*.**
Le quoi vit dans le document technique.

🔴 **Une règle absente est une règle que personne ne réclamera.** Ce que
ce fichier ne dit pas, chaque lot le tranche seul, et deux lots le
tranchent différemment. **C'est le défaut qu'il existe pour empêcher.**

**Ce qui le déclenche** — trois invocations :

| # | Ce qu'elle fait | Entrées propres |
|---|---|---|
| 1 — Dériver | Écrit les conventions depuis les deux documents | `desc-produit.md` et `spec-technique.md` en entier · `tracabilite.md` |
| 2 — Intégrer | Transforme ses propres réponses en règles | Son fichier de questions, répondu |
| 3 — Demandes | Tranche ce qu'un agent de code a rencontré | `architecte/` · **le web · les fichiers de build** |

🔴 **Les invocations 1 et 2 tournent sur un dossier de fonctionnalité
seulement** — elles dérivent des deux documents d'une feature, et un
cycle de correction n'en a ni l'un ni l'autre. 📌 **L'invocation 3 tourne
sur l'un ou l'autre.**

⚠️ **`docs/TECHNICAL_CONVENTIONS.md` est partagé par tout le dépôt** —
un seul fichier, quel que soit le cycle.

🔴 **Il ne lit le code à aucune invocation** — ni source, ni schéma
généré, ni manifeste. ⚠️ **Pas même pour savoir ce qu'un outil
produit** : il nomme les outils, il ne les trouve pas.

**Pourquoi l'invocation 1 n'ouvre aucun fichier de conventions** — 🔴
**quel que soit son nom, y compris celui qu'une exécution antérieure de
lui-même a laissé.** 📌 **Il écrit les conventions qu'un projet suivra.**
Un projet qui en a déjà les a parce que quelqu'un a décidé ; **les
relire serait dériver de sa propre sortie.**

📌 **Les invocations 2 et 3 lisent celui en vigueur** — elles
l'amendent, et on n'amende pas ce qu'on n'a pas lu.

**Trois natures de manque, deux seulement sortent de l'agent :**

| Le manque | Ce qu'il en fait |
|---|---|
| **Couverture** — une question de comportement à laquelle le corpus ne répond nulle part | 🔴 **Il la lève.** La grille de cadrage a un trou |
| **Conjonction** — la question naît entre deux entrées, chacune complète seule | 🔴 **Il la lève.** Aucune grille n'aurait pu la voir |
| **Précision** — le comportement est tranché, à un grain plus grossier que le code | 📌 **Il tranche lui-même** et l'écrit |

⚠️ **Une conjonction est invisible en amont, et pas par négligence.**
Une grille de cadrage balaye sujet par sujet, et une arête entre deux
entrées n'est le sujet de personne — 🔴 **et le graphe qui nomme les
paires n'existe pas encore quand cette grille tourne.**

📌 **La troisième n'est pas un manque.** *Ce qui identifie un segment*,
une fois que le produit a dit ce que l'utilisateur voit, est une
décision technique. **La remonter ferait faire au produit un travail qui
n'est pas le sien.**

**`couverture.md`** — une ligne par entrée du document technique, dans
son ordre. 🔴 **`no rule` s'écrit en toutes lettres** : c'est ce qui
sépare une entrée qu'on a regardée d'une entrée qu'on a manquée.

📌 **Puis une seconde table, une ligne par règle** : son entrée de
grille, et si son test est mécanique ou une relecture. ⚠️ **C'est elle
qui rend vérifiable l'exigence que toute règle à test mécanique soit
câblée dans la commande de vérification.**

**Une règle qui en restreint une autre s'écrit dans les deux**, chacune
nommant l'autre. 📌 **Un agent lit la règle large, y trouve son cas, et
s'arrête.** 🔴 **Une restriction qu'il n'atteint jamais est une
restriction qui n'existe pas.**

**La frontière** — 🔴 **Il n'attend jamais le Product Owner** : il
tranche, il refuse, ou il bloque, et il sort. 📌 **Attendre est le
travail de l'Arbitre**, en aval.

⚠️ **À l'invocation 3 il ne bloque pas du tout** — le refus s'écrit dans
le `## Verdict` de la demande, parce que l'Arbitre tourne encore et
attend. 🔴 **Un fichier de blocage laisserait deux agents suspendus à la
même réponse.**

🔴 **Un verdict porte le texte de la règle, pas seulement son numéro** —
⚠️ **l'agent qui le lit n'ouvre pas le fichier de conventions**, il
recopie ce que le verdict dit.

📌 **Cet agent est à cheval sur les deux chaînes** : l'amont le dérive
une fois par feature, l'aval lui envoie des demandes lot après lot.

---

## Le Fusionneur

**À quoi il sert** — Il fusionne le fichier produit d'une
fonctionnalité dans le document produit global.

🔴 **Une révision modifie et remplace, elle n'ajoute jamais à côté.**
L'insertion reste le cas normal pour ce qui est nouveau.

📌 **Son rapport est le seul travail manuel du Product Owner de toute la
chaîne.**

**Ce qui le déclenche** — 🔴 **en dernier**, une fois la conversion
passée sans signalement.

⚠️ **Sinon le global décrirait un état que la spec ne produira jamais.**

| # | Ce qu'elle fait | Sortie |
|---|---|---|
| 1 — Comparer | Localise, compare, questionne. 🔴 **N'écrit rien dans le global** | `plan-fusion.md` · un fichier de questions |
| 2 — Appliquer | Applique le plan, transpose, écrit le rapport | Le global à jour · `rapport-fusion.md` |
| 3 — Décisions de correction | Lit les `bug-list.md` et dit lesquelles lignes sont du produit | Le global à jour · un fichier de questions |

📌 **Le plan de fusion est ce que l'invocation 2 applique** — sans lui,
la comparaison serait refaite de zéro.

**L'unité de fusion** — 🔴 **la phrase descriptive, jamais le bloc
entier.** ⚠️ **Une refonte remplace la structure d'une entrée, mais
certaines règles survivent** : un point d'entrée, un accès depuis un
autre écran, une règle de portée. **Remplacer en bloc les perd.**

**Trois niveaux de localisation** — la section par son titre, le bloc
par son titre dans la section, la phrase contre le bloc existant.
📌 **Le bloc borne la comparaison** : dix lignes, pas un document entier.
🔴 **C'est la seconde raison d'être de la règle « un bloc, un sujet ».**

⚠️ **C'est un travail de compréhension, pas de comparaison textuelle.**
*« Trois éléments maximum »* et *« le nombre ne dépasse pas cinq »*
décrivent la même règle avec d'autres mots — c'est un remplacement.

**Cinq verbes** — `REPLACE`, `INSERT`, `KEEP`, `DELETE`, `PENDING`.
🔴 **Une phrase qui ne tombe sous aucun veut dire que la comparaison
n'est pas finie.** 📌 **`INIT` est l'exception** : sur un global vide, le
plan est ce mot seul.

⚠️ **`DELETE` ne vient jamais de lui** — seulement d'une réponse
confirmant qu'une règle ne tient plus.

**Le seul cas qui appelle une question** — 🔴 **une règle du bloc
existant sans aucune correspondance dans le bloc nouveau.**
⚠️ **Le silence ne vaut pas suppression.**

**La transposition au présent descriptif** — 🔴 **toute marque de
changement disparaît à l'insertion.** Le fichier produit dit ce qui
change — *« un nouveau bouton en bas de la page »*. Le global dit ce qui
est. ⚠️ **Sans elle, un bouton resterait « nouveau » indéfiniment.**

🔴 **Ni le numéro de bloc ni le marqueur `NEW` n'entrent dans le
global** — là, un bloc n'a que son titre. **Sinon deux features
livreraient chacune leur `B7`.**

**Le rapport** — 🔴 **le Product Owner ne relit pas la fusion entière** :
le rapport lui dit où regarder. 📌 **Les sections inchangées y sont
listées** — ⚠️ **une section qu'on attendait et qui y figure est un
signal.**

**L'invocation 3, à part** — 🔴 **c'est le seul appel où la décision
n'est pas dans un fichier produit.** Une correction tranche parfois
quelque chose du produit, et rien ne le ramène. ⚠️ **Il lit ce qu'une
correction a établi et dit si c'est du produit.** 📌 **La plupart des
lignes sont techniques ; une liste entière sans rien à fusionner est le
résultat normal.**

🔴 **Une ligne sans section correspondante est une question**, jamais
une insertion qu'il décide seul.

**La frontière** — 🔴 **Il ne décide pas ce qui se fusionne** : la
décision a été prise quand le fichier produit a été structuré.
🔴 **Il ne touche ni au document technique ni au code.** ⚠️ **Le global
ne se révise pas pendant qu'un cycle aval tourne sur le même
périmètre.**

---

## L'Extracteur

**À quoi il sert** — 🔴 **Reprise d'une application existante sans
document global.** Il décrit ce que l'application **fait aujourd'hui**,
en lisant son code.

📌 **Sa sortie est de la documentation produit** : ce qu'un utilisateur
voit, les règles, les valeurs — jamais comment c'est construit.

**Ce qui le déclenche** — 🔴 **une passe par domaine**, plus une passe
application en tête et une passe finale de recâblage. **Une seule fois
dans la vie d'un projet.**

**Ce qu'il lit** — 🔴 **`docs/TECHNICAL_CONVENTIONS.md` en entier** :
c'est lui qui nomme les dossiers de code, les fichiers de langue et
l'emplacement de la carte route↔écran. 📌 **Cette carte est ce qui lui
dit si un écran est atteignable.**

🔴 **Jamais `CURRENT_TECHNICAL_STATE.md`** — il lit le code directement.
🔴 **Jamais les specs produit existantes** — le global décrit ce qui
**est**, pas ce qui était prévu.

**Le niveau de détail** — 🔴 **ce qui vient du thème va dans la section
thème, le reste est décrit.** Une couleur nommée depuis le thème n'est
pas une décision d'écran ; une valeur en dur en est une.

**Cinq balises greppables**, pour que le Product Owner les récupère par
script :

| Balise | Sens |
|---|---|
| `<<REF:name>>` | Référence vers un domaine pas encore extrait — résolue à la passe finale |
| `<<ORPHAN>>` | Écran ou service qui n'apparaît dans aucune route ni appel |
| `<<HARD_STYLE>>` | Valeur de style en dur au lieu du thème |
| `<<HARD_TEXT>>` | Texte affiché en dur au lieu des fichiers de langue |
| `<<DOUBT>>` | Ce qu'il n'a pas su interpréter |

📌 **Il ne tranche aucun de ces cas** — il décrit et il balise.

**La frontière** — 🔴 **Il ne corrige pas ce qui lui semble anormal.**
**Le comportement observé *est* l'état actuel** ; le décrire tel quel
est exactement ce qu'on veut. 🔴 **Il ne décrit pas ce qui n'est pas
implémenté.** 🔴 **Il ne nomme ni fichier, ni classe, ni méthode** —
c'est `CURRENT_TECHNICAL_STATE.md`.

🔴 **Il ajoute son domaine au global, il ne le réécrit jamais** — les
domaines déjà là ne sont pas les siens.

---

## Qui tourne sur quel modèle

*Porté par la frontmatter de chaque agent.*

| Opus | Sonnet |
|---|---|
| lexicographe · decoupeur · sondeur · convertisseur · architecte | redacteur · classeur · assembleur · fusionneur · extracteur |

📌 **Cinq portent `effort: high`** — redacteur, convertisseur,
fusionneur, architecte, extracteur. ⚠️ **Aucune commande ne le passe** —
le paramètre n'existe pas sur l'appel.

---

# LA GRILLE DE CADRAGE PRODUIT

*`docs/process/GRILLE_CADRAGE_PRODUIT_V2.md`. Les sondeurs la
déroulent ; aucun autre agent ne l'ouvre.*

🔴 **C'est un test de fermeture, pas une liste de sujets.** 📌 **Elle
génère ses questions depuis les blocs présents.** ⚠️ **Ce qu'elle ne
génère pas des blocs présents, elle ne le demande pas** — elle ne
grandit jamais d'imagination.

**Le critère de complétude** — 🔴 **un cadrage est complet quand rien ne
pend.** Chaque élément a un déclencheur nommé et un effet nommé ; chaque
nom qu'il cite pointe vers quelque chose de décrit, ou est défini sur
place. **Un nom sans rien derrière est un trou.**

## Trois passes, et elles lisent des choses différentes

🔴 **Une fermeture appartient à une passe, jamais aux deux.**

**Passe A — un bloc à la fois.** 📌 **Tout ce qu'un bloc ferme seul.**
⚠️ **On répond depuis ce bloc seul** — 🔴 **qu'un autre bloc porte la
réponse n'est pas la question de cette passe.**

Quatre parties : fermer le bloc (ce qui le déclenche, ce qu'il
consomme, ce qu'il produit, où il se dessine, ce qui départage une
égalité) — 🔴 **y compris le revers, posé même quand la réponse est
« rien »** : ce qui se passe quand le déclencheur cesse d'être vrai, ce
que devient ce qui a déjà été produit, s'il peut se redéclencher.
Puis rendre le bloc codable, **par les questions de sa nature et
d'elles seules**. Puis les blocs sans déclencheur. Puis le test de
clôture.

🔴 **Le test de clôture écrit tout nom que le bloc emploie, avec la
valeur que le bloc lui donne** — ⚠️ **même un nom qu'il ferme ici.**
📌 **La passe B a besoin de tous pour trouver un nom qui vaut deux
choses.**

⚠️ **Un nom n'est pas seulement ce qui porte un nom propre** : *« les
cinq lignes de zone »*, *« l'arc actif au repos »*, *« l'heure
affichée »* en sont.

**Passe B — les blocs les uns contre les autres.** 📌 **Tout ce qui
n'apparaît qu'en les mettant ensemble.**

🔴 **Elle lit les réponses de la passe A, jamais les blocs à nouveau.**
📌 **On rassemble une colonne à travers tous les blocs, puis on la
croise** — ⚠️ **jamais bloc par bloc**, ou on relit soixante fois ce
qu'une colonne montre d'un coup.

⚠️ **C'est ce qu'une chaîne n'atteint jamais.** 📌 **Une chaîne remonte
ce qui consomme et descend ce qui produit ; deux blocs qui partagent un
écran, ou un nom, ne font ni l'un ni l'autre** — 🔴 **seule une colonne
prise en entier les montre.**

🔴 **Chaque croisement pose la même question à sa réponse : est-ce que
le bloc change ?** ⚠️ **Inchangé → le fil se ferme**, et le bloc est
marqué *existant*. 🔴 **Changé → c'est un bloc à part entière, et
personne d'autre ne l'écrira.**

**Passe C — la fonctionnalité, une fois.** 📌 **Ce qu'aucun bloc ne
lève, parce que ça n'appartient à aucun.** 🔴 **Les seules questions
énumérées de la grille — courtes exprès.**

## Deux mécaniques qui traversent la grille

🔴 **Chaque question porte un identifiant** — `A1.3`, `A2.screen.2`,
`C1.6`. ⚠️ **Qui répond écrit cet identifiant, exactement** — 📌 c'est
ce qui rend les réponses d'un bloc comparables à celles d'un autre.

🔴 **Une catégorie écartée est déclarée écartée**, jamais sautée en
silence. ⚠️ **Une section sautée en silence et une section sans objet
se lisent pareil.**

---

# LES COMMANDES

*Ce que chacune décide, et pourquoi c'est elle qui décide.*

| Commande | Agent(s) | Ce qu'elle produit |
|---|---|---|
| `/1_lexique` | lexicographe | `lexique.md` · `questions-lexicographe-NN.md` · `idees.md` tranché |
| `/2_structure` | redacteur | `desc-produit.md` |
| `/3_decoupe` | decoupeur | `desc-produit.md`, blocs découpés |
| `/3b_nature` | classeur | `desc-produit.md`, natures posées |
| `/4_grille` | sondeur ×3, puis assembleur | `questions-sondeur-NN.md` |
| `/5_reclasse` | convertisseur, inv. 1 | `questions-convertisseur-NN.md` |
| `/6_convertit` | convertisseur, inv. 2 | `spec-technique.md` · `tracabilite.md` |
| `/conventions` | architecte | `TECHNICAL_CONVENTIONS.md` · `couverture.md` |
| `/fusion_compare` | fusionneur, inv. 1 | `plan-fusion.md` · questions |
| `/fusion_applique` | fusionneur, inv. 2 | Le global à jour · `rapport-fusion.md` |
| `/fusion` | fusionneur | Reprise, par table de routage |
| `/extrait` | extracteur, enchaîné | Le global entier, depuis le code |

📌 **La numérotation suit la chaîne, pas les agents** — elle donne
l'ordre d'exécution.

## `/1_lexique` — décide laquelle des quatre invocations

🔴 **Ce qui traîne à la racine du dossier décide.** 📌 **Le nom, jamais
le numéro.**

| À la racine | Invocation |
|---|---|
| Aucun fichier de questions | **1 — Balayage** |
| `questions-lexicographe` seul | **2 — Tranchage** |
| `questions-sondeur` seul | **3 — Surveillance** |
| Les deux | **4 — Correction** |

🔴 **Pourquoi c'est la commande** : ⚠️ **c'est le rangement fait par
`/2_structure` et `/4_grille` qui sépare ces quatre cas.** `/2_structure`
range le fichier du lexicographe, `/4_grille` range tout ce qui n'est
pas le sien. **L'agent ne voit pas cet état ; l'orchestrateur, si.**

🔴 **Elle décide aussi que `desc-produit.md` arrête 1 et 2, mais pas 3
et 4** — le vocabulaire se tranche avant le fichier produit, jamais
après.

## `/2_structure` — décide ce qui devient périmé

**Elle décide l'invocation** : sans fichier de questions à la racine,
1 ; avec un ou plusieurs, **quel que soit leur préfixe**, 2 sur le plus
haut numéro. ⚠️ **Un `Answer:` vide l'arrête**, et elle dit lesquelles
attendent.

🔴 **Et elle décide ce qui est à jeter.** Elle grepe `NEW` dans le
fichier produit : s'il y en a, elle supprime le document technique.

⚠️ **Le fichier produit a gagné un bloc**, et tout ce qui a été
construit depuis la version précédente est périmé — une mise à jour
ciblée corrigerait un document qui ne correspond plus.

📌 **`MODIFIED` seul ne déclenche rien** : ⚠️ **un bloc changé existe
toujours sous le même identifiant**, et une mise à jour ciblée
l'atteint.

🔴 **Pourquoi c'est la commande** : c'est la seule à voir à la fois le
marqueur et les fichiers d'aval. L'agent n'ouvre ni l'un ni l'autre.

## `/3_decoupe` — décide quels blocs regarder

**Premier tour** — aucun `questions-*.md` nulle part : 🔴 **tous les
blocs.** **Tours suivants** — l'union de deux greps, `NEW` et
`MODIFIED`.

⚠️ **Elle ne grepe pas le fichier de questions** — 🔴 **un bloc qu'une
réponse a touché porte `MODIFIED`**, et le second grep le trouve.

🔴 **Elle décide aussi de s'arrêter** sur un `Clarification needed` dans
le fichier produit.

**Elle compte, elle ne vérifie pas** — 🔴 **jamais lire un bloc pour
contrôler le travail.** 📌 **Les sondeurs sondent ce qu'il a produit ;
c'est ça qui attrape un mauvais découpage.**

## `/3b_nature` — décide s'il y a quelque chose à classer

**Deux greps, et l'union de ce qu'ils rendent** : 🔴 **`-B1 '^Nature:$'`
pour les blocs dont la nature est vide** — la ligne au-dessus de chaque
trouvaille porte le bloc — **et `MODIFIED` pour ceux dont la nature a pu
bouger avec eux.**

📌 **Ni l'un ni l'autre ne rend rien** → 🔴 **elle n'invoque pas.** ⚠️
**Elle le dit**, et passe à `/4_grille`.

📌 **Un bloc à nature remplie et sans marqueur a été classé à un tour
précédent**, et rien à son sujet n'a bougé depuis.

🔴 **Elle compte en sortie** : `-c '^Nature:$'` doit rendre zéro —
⚠️ **autre chose veut dire qu'un bloc est resté non classé**, et elle dit
lequel.

🔴 **Pourquoi c'est la commande** : 📌 **le Classeur ne grepe pas**, on
lui nomme ses blocs. ⚠️ **Et c'est la commande qui voit si le compte est
retombé à zéro** — l'agent ne relit pas son propre travail.

## `/4_grille` — décide les trois ordres et ce qui clôt la boucle

🔴 **Les trois appels `Agent(...)` partent dans un seul message.**
⚠️ **Trois messages les font tourner en série** — 📌 ils ne partagent
rien, et lancés ensemble le coût en temps est celui d'un seul sondeur.

**Elle décide les blocs de la passe A** — l'union de trois greps :
`^Block:` dans le dernier fichier de questions des sondeurs, `NEW` et
`MODIFIED` dans le fichier produit. 🔴 **Une question nommant deux blocs
les envoie tous les deux.** ⚠️ **Ça ne rétrécit que la passe A.**

**Elle décide que la fusion peut avoir lieu** : 🔴 **les trois fichiers
existent, sinon elle s'arrête** et dit lequel manque.

**Et elle clôt la boucle** : 🔴 **elle recopie le fichier fusionné en
`questions-sondeur-NN.md`**, renumérote à partir de `Q1`, retire la
section `## Merge` — ⚠️ une note de travail, pas une question.
📌 **Aucune question du tout → elle écrit le fichier vide. C'est ce qui
termine la boucle.**

🔴 **Elle crée `cadrage-produit/closed/` dans le worktree avant
d'invoquer** — ⚠️ un agent dont le dossier cible manque cherche au lieu
de s'arrêter.

## `/5_reclasse` et `/6_convertit` — ne décident rien d'autre que l'enveloppe

📌 **Elles nomment l'invocation, passent le dossier, et gèrent le
rangement et le git.** ⚠️ **Ce qui tourne ensuite n'y est pas** — c'est
l'agent qui le porte, dans sa table d'aller-retour.

## `/conventions` — décide l'invocation, et se porte garante du relais

🔴 **Elle parcourt la table du haut et s'arrête à la première ligne qui
correspond :** une demande à `## Verdict` vide → 3 ; un
`questions-architecte-NN.md` répondu → 2 ; rien de tel → 1.

📌 **Elle décide aussi le dossier de travail** — la feature, ou un
`bugfix-NN` pour l'invocation 3. ⚠️ **Chaque cycle porte son propre
`architecte/`**, et une demande se traite dans le cycle qui l'a levée.

🔴 **Elle s'arrête si `spec-technique.md` est absent** — l'agent en
dérive, et la boucle amont n'y est pas encore arrivée. ⚠️ **Sauf à
l'invocation 3**, qui juge une demande contre les conventions.

🔴 **Elle dit explicitement quand le fichier de questions porte des
questions.** ⚠️ **Une exécution qui a écrit une question sans le dire
est une exécution dont la question est perdue** — 📌 **le Product Owner
ne va pas fouiller le dossier.**

⚠️ **Elle se lance à la main** — 🔴 **`/cycle` ne l'appelle pas**, et le
câblage attend que la grille ait été mesurée sur un cycle réel.

## `/fusion_compare`, `/fusion_applique`, `/fusion`

📌 **Les deux premières sont une invocation chacune.**
🔴 **`/fusion_applique` range en plus tous les `questions-*.md` de la
racine une fois la fusion tenue** — **la branche de fusion s'arrête
là.**

📌 **`/fusion` est une table de routage à dix lignes**, parcourue du
haut, qui décide *où reprendre* : erreur si le fichier produit manque,
arrêt sur un blocage ou un `Answer:` vide, arrêt si `rapport-fusion.md`
existe — la fusion est faite — sinon l'invocation qui correspond.

🔴 **Une phase par exécution, jamais deux agents enchaînés** — chaque
arrêt rend la main au Product Owner.

## `/extrait` — décide la séquence, jamais le découpage

📌 **La liste des domaines est une décision produit, jamais dérivée de
l'arborescence** — 🔴 **sans elle, on n'extrait rien.** ⚠️ Un dossier
peut porter deux sujets, un sujet s'étaler sur trois dossiers.

**Trois temps** : la passe application, puis les domaines dans l'ordre
de la liste, puis le recâblage.

🔴 **Séquentiel, jamais parallèle** — 📌 **chaque domaine voit les
précédents et balise moins.** En parallèle, aucun ne verrait les autres
et la passe de recâblage deviendrait énorme.

📌 **Un seul worktree pour toutes les passes**, pas un par passe.
**Entre deux passes, elle grepe le titre du domaine dans le global** —
🔴 **sans ça, une passe ratée passe inaperçue et son domaine manque
simplement.**

**Sur échec elle continue** — 📌 les domaines sont indépendants, et elle
rapporte les domaines ratés à la fin.

## L'enveloppe git, commune à toutes

🔴 **Quatre gestes, dans cet ordre, avant d'invoquer :**

**1. Ranger** tout `questions-*.md` de la racine dont le préfixe n'est
pas celui de la phase, dans `questions/<agent>/`. 🔴 **Par `git mv`,
jamais par une lecture-réécriture** — ⚠️ **les agents ne doivent pas
ouvrir ces fichiers, et l'orchestrateur non plus.** 📌 **Le plus haut
numéro du préfixe courant reste à la racine** : il porte la
numérotation.

**2. Commiter le dossier de la fonctionnalité.** ⚠️ **Le Product Owner
remplit les `Answer:` à la main, hors session.** Un worktree part du
dernier commit — **des réponses non commitées y sont invisibles**, et
l'agent travaille sur un fichier périmé. *(Vu une fois : 186 lignes dans
le worktree, 195 dans le checkout principal.)*

**3. Créer le worktree depuis `HEAD` local**, et l'enregistrer.
⚠️ **Ne jamais laisser l'outillage choisir la base** — 🔴 **son défaut
est `origin/master`**, qui peut être plusieurs commits en retard.
*(Vu une fois : une invocation entière perdue.)*

**4. Entrer dans le worktree avant d'invoquer**, pas après un échec
d'écriture. 🔴 **Le harnais bloque les écritures d'un sous-agent tant
que la session n'est pas isolée** — ⚠️ **l'agent fait tout le travail
avant de découvrir qu'il ne peut pas l'enregistrer**, et l'invocation
entière est à refaire. *(Mesuré sur trois phases.)*

**Puis, une fois l'agent rentré** : `git merge --no-ff`, `git push`,
`git worktree remove`.

🔴 **Le push fait partie du merge, pas d'un après-coup.** Une phase qui
ne vit que sur la machine locale est perdue avec elle. ⚠️ **Un push qui
échoue se rapporte, il ne se contourne pas.**

🔴 **Merger avant de rendre la main, toujours** — ⚠️ **un `blocked_*.md`
merge aussi** : le Product Owner doit le voir.

---

# LA BOUCLE DU CYCLE

*Portée par la section **What to run next** de chaque commande.*

    /1_lexique  ⇄  questions            (invocations 1 et 2)
         │ vide
         ↓
    /2_structure ──→ /3_decoupe ──→ /3b_nature ──→ /4_grille
         ↑                                              │
         │                              des questions ──┤──→ /1_lexique (3 puis 4)
         │←─────────────────────────────────────────────┘            │
         │                                                            ↓
         │                                              (retour à /2_structure)
         │
         └── /4_grille vide ──→ /5_reclasse ──→ /6_convertit ──→ /conventions ──→ aval
                                                      │
                                             /fusion_compare ──→ /fusion_applique

**Les enchaînements, un par un :**

| Ce qui vient de se passer | Ensuite |
|---|---|
| `/1_lexique` 1 ou 3 a demandé quelque chose | Répondre, puis `/1_lexique` |
| `/1_lexique` 2 a tourné, et 1 ne trouve plus rien | `/2_structure` |
| `/1_lexique` 4 a tourné | `/2_structure` — 🔴 les réponses de la grille sont tranchées |
| `/2_structure` a signalé une clarification | 🔴 **Répondre, puis `/2_structure`** — rien en aval ne tourne tant qu'un signalement tient |
| `/2_structure` a écrit le fichier produit | `/3_decoupe` |
| `/3_decoupe` a tourné | `/3b_nature`, qu'il ait découpé ou non |
| `/3b_nature` a tourné, ou n'a rien eu à classer | `/4_grille` — 🔴 la grille pose à un bloc les questions de sa nature, et un bloc sans nature ne s'en verrait poser aucune |
| `/4_grille` a levé des questions | 🔴 **Répondre, puis `/1_lexique`** — il tranche le vocabulaire que ces réponses apportent, avant que le Rédacteur les lise |
| `/4_grille` est vide | `/5_reclasse` — le fichier produit est fermé |

**L'aller-retour du Convertisseur** — 🔴 **une réponse revient toujours
par `/2_structure` d'abord.** La suite dépend de ce qu'elle a changé :

| Après `/2_structure` | La route |
|---|---|
| Aucun `NEW` dans le fichier produit | 🔴 **Directement à l'invocation qui a demandé** |
| Un `NEW` est apparu | `/4_grille` → `/5_reclasse` → `/6_convertit` — 📌 un bloc neuf n'a jamais été fermé, ni classé |

⚠️ **La route longue repasse par `/5_reclasse`, qui supprime le document
technique** — 📌 l'invocation 2 le produit alors en entier plutôt que de
rapiécer un document périmé.

📌 **Les questions de l'invocation 2 créent rarement un bloc** : elles
affûtent une phrase qui existe déjà.

**Le critère d'arrêt, partout** — 🔴 **un fichier de questions
entièrement répondu, jamais un nombre d'itérations.** ⚠️ **Une question
dont la réponse est consignée ne se repose jamais.** 📌 **Qu'une réponse
fasse apparaître un nouveau problème est normal, pas un échec.**

---

# LES FICHIERS

## Ce que la chaîne produit, et qui l'écrit

| Fichier | Écrit par | Lu par |
|---|---|---|
| `idees.md` | Product Owner, hors ligne · **Lexicographe** pour les termes tranchés | Lexicographe, Rédacteur *(inv. 1)* |
| `lexique.md` | Lexicographe | Lexicographe, Rédacteur |
| `desc-produit.md` | **Rédacteur** · Découpeur *(découpes seules)* · Classeur *(la ligne `Nature:` seule)* | Sondeur, Convertisseur, Fusionneur, Architecte |
| `cadrage-produit/par-bloc.md` · `par-question.md` · `par-nature.md` | Les trois sondeurs | Assembleur |
| `cadrage-produit/questions.md` | Assembleur | La commande `/4_grille`, qui le recopie |
| `questions-<agent>-NN.md` | L'agent émetteur · **Product Owner** pour les réponses | Son émetteur, le Rédacteur |
| `spec-technique.md` | Convertisseur *(inv. 2)* | Architecte, **Cadreur** *(aval)* |
| `tracabilite.md` | Convertisseur *(inv. 2)* | Architecte *(inv. 1)* |
| `docs/TECHNICAL_CONVENTIONS.md` | **Architecte, seul** | Tous les agents de code, Extracteur |
| `couverture.md` | Architecte | Product Owner, une fois |
| `architecte/<demande>.md` | Les agents d'aval · **Architecte** pour le `## Verdict` | Architecte *(inv. 3)*, leur auteur |
| `plan-fusion.md` | Fusionneur *(inv. 1)* | Fusionneur *(inv. 2)*, elle seule |
| `docs/PRODUIT_GLOBAL.md` | Fusionneur · Extracteur | Rédacteur, Fusionneur — 🔴 **par l'index** |
| `rapport-fusion.md` | Fusionneur *(inv. 2)* | Product Owner |
| `blocked_<agent>.md` | L'agent · **Product Owner** pour la `## Decision` | L'agent, et l'orchestrateur pour cette seule ligne |
| `docs/process/GRILLE_*.md` | Product Owner, hors chaîne | Sondeur *(cadrage)* · Convertisseur *(fermeture)* · Architecte *(conventions)* |

**Où ils vivent** — 🔴 **un dossier par fonctionnalité**,
`docs/features/<nom>/`, créé par le Product Owner qui y dépose son
fichier d'idées. 📌 **Le global est `docs/PRODUIT_GLOBAL.md`**, à part :
il n'appartient à aucune feature.

🔴 **Noms fixes** — c'est ce qui permet aux commandes de n'avoir qu'un
seul argument : le nom du dossier.

## Comment le global se lit

🔴 **Par l'index, jamais en entier.** ⚠️ **Il dépasse 250 Ko.** Un grep
sur `^#` sort les titres — domaines, sections, blocs — quel que soit le
volume ; on ne charge ensuite que les sections dont on a besoin.

⚠️ **Un titre doit dire ce que sa section contient**, sinon l'index ne
sert à rien. **C'est le critère de qualité du global.**

🔴 **Il décrit l'état actuel, jamais l'historique.** Une entité révisée
n'accumule pas ses versions.

---

# LES MÉCANIQUES COMMUNES

*Inventées une fois, portées par presque tous les agents. Chacune
empêche une défaillance précise.*

## Le fichier de questions

🔴 **Quatre lignes par entrée, sans exception**, et la numérotation
repart à `Q1` dans chaque fichier :

    ### Q1
    Block: B7
    Question: <ce qui manque, énoncé directement>
    Answer:

🔴 **La ligne `Answer:` s'écrit vide et ne s'omet jamais** — c'est là
que le Product Owner écrit, à la main. **Une entrée sans elle est
inutilisable.**

📌 **Questions en anglais, réponses en français** — le Rédacteur traduit
en intégrant.

🔴 **Un trou, une question.** ⚠️ **Deux trous dans une entrée ne peuvent
pas être répondus séparément**, et une fusion ne peut pas les
distinguer.

📌 **C'est le seul fichier où un agent formule librement** — partout
ailleurs il transcrit ou range.

🔴 **Il ne propose jamais de réponse.** Formuler une hypothèse plausible
reviendrait à trancher une décision produit.

**La numérotation avance d'une invocation, jamais d'une question** —
📌 un fichier par invocation, portant toutes ses questions.

## Écrire la sortie même vide

🔴 **Un fichier de sortie s'écrit toujours, même sans contenu.** Un
fichier de questions vide dit *« rien à signaler »* ; son absence dit
*« l'agent n'a pas tourné »*. ⚠️ **L'orchestrateur ne peut pas
distinguer les deux autrement**, et laisserait le fichier précédent
passer pour le dernier.

## Les marqueurs `NEW` et `MODIFIED`

📌 **Ils disent quoi resonder au tour suivant.** 🔴 **Un bloc qu'aucun ne
nomme a été fermé au tour précédent et n'a pas bougé depuis.**

🔴 **Ils sont effacés avant chaque écriture** — seuls ceux du tour en
cours doivent rester. ⚠️ **Un bloc changé sans `MODIFIED` ne sera jamais
resondé.**

## Le signalement en place — `**Clarification needed:**`

📌 **Il transcrit une lecture plutôt que de s'arrêter** : le bloc reste
exploitable pendant que la lecture se confirme.

🔴 **Mais rien en aval ne tourne tant qu'un signalement tient.**
⚠️ **Le Découpeur et les sondeurs s'arrêtent dessus** — un bloc
transcrit sur une lecture non confirmée serait découpé ou fermé sur une
forme qui va changer.

📌 **Il vit dans le bloc, et le Rédacteur le retire en intégrant sa
réponse.**

## Les fichiers de blocage

🔴 **Un agent qui ne peut pas produire écrit un fichier**, il ne se
contente pas de le dire. ⚠️ **Un message dans une réponse se perd ; un
fichier reste.**

**Quatre titres** — ce qui bloque *(le fait, pas son interprétation)*,
où, ce qu'il faudrait pour reprendre, et 🔴 **`## Decision`, écrite
vide.** **C'est là que le Product Owner répond, et c'est le seul moyen
qu'un blocage se lève.**

⚠️ **Bloquer n'est pas signaler.** Un manque, une contradiction, une
question : ça part dans le fichier de questions et le cycle continue.
🔴 **On ne bloque que quand produire est impossible** — entrée absente,
fichier attendu introuvable, prémisse fausse qui invalide tout le
travail.

📌 **Ne jamais bloquer par excès de prudence.**

🔴 **La commande lit cette seule ligne `## Decision`** — vide, elle
s'arrête ; remplie, **elle nomme le fichier dans le prompt.** ⚠️ **Un
agent ne va jamais chercher un fichier de blocage lui-même** :
l'orchestrateur a regardé, et ne l'aurait pas appelé sur une décision
vide.

🔴 **Une fois appliqué, le fichier est renommé** en
`blocked_<agent>-NN.md`, ⚠️ **par `git mv`** : un fichier, sous un
nouveau nom. 🔴 **Jamais une copie, une note ou un fichier vide laissé à
l'ancien nom** — 📌 **tout ce qui reste au nom sans numéro se lit comme
un blocage encore debout**, et l'exécution suivante s'arrête dessus.

📌 **Les numérotés sont l'archive de ce sur quoi ce cycle a déjà
bloqué** — 🔴 **l'exécution suivante les lit.**

## Les chemins, dans un worktree

🔴 **Tout chemin qu'un agent lit ou écrit est relatif** —
`docs/features/…`, jamais `C:\…` ni `/…`. ⚠️ **Un chemin absolu pointe
hors de la session isolée**, et l'écriture échoue.

## Les marques greppables

📌 **Deux agents laissent des marques dans leur propre sortie**, pour
qu'un grep ou un script les récupère : `<<ASSUMED …>>` chez le
Convertisseur, les cinq balises de l'Extracteur.

🔴 **Une marque porte l'identifiant de ce qui la lèvera**, pas seulement
le fait qu'elle existe.

---

# CONTRADICTIONS RELEVÉES

*Points où deux fichiers ne disent pas la même chose. Non tranchés
ici.*

📌 **Six entrées ont été retirées**, tranchées dans les fichiers : le
modèle du Rédacteur, la forme de la ligne `Block:`, les invocations que
`/1_lexique` sait nommer, ce que `/fusion` enchaîne, ce que
`.claude/CLAUDE.md` dit des modèles, et `desc-par-nature.md` —
📌 **le Classeur pose la nature, le reclassement par nature reste au
Convertisseur, et le fichier ne revient pas.**

🟡 **La route longue du Convertisseur ne passe pas par `/3b_nature`.**
Son aller-retour dit qu'un `NEW` apparu renvoie à
`/4_grille` → `/5_reclasse` → `/6_convertit`. 🔴 **Mais un bloc neuf
porte une ligne `Nature:` vide** — ⚠️ **et la grille pose à un bloc les
questions de sa nature.** 📌 **Sans classement, elle ne lui en pose
aucune**, et le bloc traverse le tour fermé sur rien.

🟡 **Ce que `.claude/CLAUDE.md` dit de la grille de cadrage.** Il annonce
que le Rédacteur charge `GRILLE_CADRAGE_PRODUIT.md` par son nom ;
🔴 **le Rédacteur s'interdit d'ouvrir quoi que ce soit dans
`docs/process/`**, et la grille que les sondeurs déroulent est
`GRILLE_CADRAGE_PRODUIT_V2.md`. ⚠️ **Les deux fichiers coexistent dans
`docs/process/`**, et seul le second est celui que la chaîne lit.

🟡 **Deux résidus de l'arbitrage tranché**, et c'est sa mise en œuvre qui
n'a pas suivi, non la décision. 📌 **`/2_structure` supprime toujours
`desc-par-nature.md`** quand un `NEW` apparaît, et aucun agent ne
l'écrit. 📌 **Et l'invocation 1 du Convertisseur s'appelle toujours
*Closing* dans l'agent**, *« Reclassifying »* dans `/5_reclasse`.
