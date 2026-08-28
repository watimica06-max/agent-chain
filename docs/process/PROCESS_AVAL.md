# Process aval — du document technique au code

> Documentation de référence. Décrit la chaîne **document technique →
> code**, dérivée des phases réelles d'un développement.
>
> 📌 **L'amont** — de l'idée au document technique — vit dans
> `PROCESS_AMONT.md`.
>
> 🔴 **Aucun agent ne lit ce document.** Il dit pourquoi les agents sont
> construits comme ils le sont, y compris des règles envisagées puis
> écartées.

---

## Trois principes

### 1. Un rôle se justifie par une des deux raisons seulement

**(a) Contexte incompatible** — les documents que deux travaux exigent
ne peuvent pas cohabiter sans dégrader la qualité.

**(b) Indépendance du regard** — juger son propre jugement ne
fonctionne pas.

🔴 **Tout le reste va ensemble.** Un humain lit, décide et écrit d'un
même mouvement ; découper sans l'une de ces deux raisons ajoute du coût
sans rien garantir.

⚠️ La raison (a) est **circonstancielle** — elle dépend du volume, donc
du dimensionnement des lots. La raison (b) est **structurelle**.

### 2. Boucle de vérification, pas filet

**Une boucle** — l'agent vérifie son propre travail avant de rendre. Il
a déjà le contexte : ça ne coûte presque rien.

**Un filet** — un autre agent revérifie. Ça coûte une invocation, un
chargement, un regard qui doit tout reconstruire.

🔴 **Le filet ne se justifie que là où l'auto-vérification est
structurellement impossible** : quand il faudrait juger son propre
jugement.

*Un agent peut vérifier qu'il a écrit dans le bon fichier, au bon
format, avec les bons champs — c'est mécanique. Il ne peut pas vérifier
que son code fait ce qui était demandé : il a choisi son
interprétation.*

⚠️ **Chaque contrôle ajouté doit nommer ce qu'aucun autre ne fait
déjà.** Sinon c'est de la ratification, pas de la détection.

### 3. Un fichier est écrit une fois

Écrit par un seul acteur, à un seul moment, et **plus modifié ensuite**.

*Trois fichiers ont grossi jusqu'à devenir inexploitables — 88 Ko,
276 Ko, un doublement — tous parce que plusieurs acteurs y ajoutaient
au fil de l'eau.*

---

## Les agents

| # | Agent | Justification | Fréquence |
|---|---|---|---|
| 1 | **Cadreur** — découpage | (a) contexte de specs | une fois |
| 2 | **Vérificateur** — contrôle du découpage | (b) regard indépendant | une fois |
| 3 | **Détailleur** — signatures et critères | (a) contexte de code | **par bloc** |
| 4+5 | **Réalisateur** — code et état | (a) contexte de code | par lot |
| 6 | **Relecteur** — verdict | (b) regard indépendant | par lot |
| 7 | **Contrôleur** — intention produit vs fiches | (a) + (b) | une fois, à la fin |
| 8 | *Product Owner* — test | — | une fois, à la fin |

**Deux invocations par lot**, plus une par bloc. Les phases 1, 2 et 7
tournent une fois pour tout le document technique ; le test humain une
fois à la fin.

📌 **Six agents au lieu de quatre, mais le plan disparaît** et le
Réalisateur ne décide plus d'architecture.

---

## Les fichiers

| Document | Écrit par | Lu par |
|---|---|---|
| `spec-technique.md` | en amont | Cadreur (tout), Vérificateur et Détailleur (sections ancrées) |
| `CURRENT_TECHNICAL_STATE.md` | Réalisateur | Cadreur, Détailleur |
| `TECHNICAL_CONVENTIONS.md` | hors process | Détailleur, Réalisateur, Relecteur |
| Liste des lots + ancres | Cadreur | Vérificateur, Détailleur |
| Séquence + blocs | Vérificateur | orchestration, Détailleur |
| Fiche exécutable d'un lot | Détailleur | Réalisateur, Relecteur |
| Compte rendu | Réalisateur | Relecteur, bloc suivant |
| Verdict | Relecteur | orchestration |
| Rapport d'écarts | Contrôleur | Product Owner |

⚠️ **Ce qui disparaît** : le plan comme artefact — il comblait le vide
entre un périmètre vague et le code, et ce vide est désormais comblé
par la fiche exécutable. Et toute validation intermédiaire.

### La liste des lots

**Produite par** le Cadreur. **Lue par** le Vérificateur et le
Détailleur.

📌 **Pourquoi elle existe** : elle transforme un document par nature en
unités livrables, chacune ancrée dans sa source. Sans elle, le
Détailleur devrait découper et détailler en même temps.

| Bloc | Contenu |
|---|---|
| Identifiant du lot | `lot-01`, `lot-02`… — 🔴 **depuis 1 dans chaque feature**, pas de continuité entre features |
| Ancre | la section précise du document technique dont le lot découle |
| Besoins | symboles requis, produits par un lot antérieur ou préexistants |
| Productions | symboles que ce lot va créer |
| Modifications | symboles existants dont ce lot change la signature ou le comportement |

**Structure** : cinq champs par lot, un lot après l'autre — pas de
prose entre eux, pas de section d'introduction récapitulative.

**Absent par construction** : aucune règle métier, aucun verbatim de
spec — l'ancre les remplace. Aucune signature ni critère d'acceptation
— c'est le travail du Détailleur.

---

### La séquence et les blocs

**Produite par** le Vérificateur. **Lue par** l'orchestration et le
Détailleur.

📌 **Pourquoi elle existe** : c'est elle qui dit dans quel ordre coder,
et où couper les blocs. 🔴 **Le seul artefact qui pilote la boucle.**

| Bloc | Contenu |
|---|---|
| Ordre d'exécution | les lots, dans l'ordre dérivé de leurs dépendances déclarées |
| Défauts constatés | trous, cycles, ancre incohérente avec son lot |
| Regroupement en blocs | les lots groupés par partage de lecture, dans l'ordre |

**Structure** : la séquence est une liste ordonnée d'identifiants de
lot, rien de plus — la justification est déjà dans la fiche du Cadreur,
pas à répéter. Les défauts ont trois champs : quel lot, quel type,
quelle correction attendue — un défaut par ligne.

**Absent par construction** : règle métier, signature — le Vérificateur
constate la structure, il ne produit rien du contenu.

🔴 **C'est le seul artefact de la liste qui pilote la boucle**, pas
seulement lu par un agent : c'est lui qui dit à l'orchestrateur quel
bloc invoquer, dans quel ordre. Le format n'en change pas — une liste
ordonnée reste une liste ordonnée — mais ce rôle doit être explicite
quand les instructions de l'orchestrateur seront écrites.

---

### La fiche exécutable

**Produite par** le Détailleur, une par lot. **Lue par** le
Réalisateur, le Relecteur et le Contrôleur.

📌 **Pourquoi elle existe** : elle comble le vide entre une règle
produit et du code. C'est elle qui remplace le plan de l'ancien
process.

| Bloc | Contenu |
|---|---|
| Signatures | noms de classe, méthodes, types — complets ou absents |
| Critères d'acceptation | dérivés de la section ancrée |
| Dépendances | symboles déjà produits dont ce lot a besoin |

**Structure** : trois champs, chacun répond à une question précise.
**Absent par construction** : citation de la spec, justification du
découpage.

### Le compte rendu

**Produit par** le Réalisateur, un par lot. **Lu par** le Relecteur et
le Détailleur du bloc suivant.

📌 **Pourquoi il existe** : il déclare ce qui a été réellement produit,
et c'est cette déclaration que le contrôle de divergence compare aux
symboles promis.

| Bloc | Contenu |
|---|---|
| Symboles | ceux créés **et** ceux modifiés, à comparer à ceux promis |
| Build | résultat d'analyze et de test |
| État | ce qui a été ajouté ou retiré de `CURRENT_TECHNICAL_STATE.md` |
| Convention, si pertinent | proposition — jamais une modification directe du fichier partagé |

**Structure** : un champ, une réponse.
**Absent par construction** : justification des choix — elle est dans
la fiche du Détailleur, pas à répéter.

### Le rapport d'écarts

**Produit par** le Contrôleur, une fois par cycle. **Lu par** le
Product Owner.

📌 **Pourquoi il existe** : il ferme la chaîne sur son point de départ.
Sans lui, une intention perdue entre le produit et la fiche ne se
découvrirait qu'à l'usage.

| Bloc | Contenu |
|---|---|
| Intentions retrouvées | La liste, une ligne chacune — le bloc produit et la fiche qui le porte |
| Intentions absentes | Le bloc produit, et ce qu'il décrivait |
| Doutes | Ce qu'il n'a pas su trancher |

🔴 **Une ligne par entrée, pas de prose.** Il est lu une fois par le
Product Owner.

📌 **Les intentions retrouvées y figurent** — leur absence de la liste
serait ambiguë : traitée, ou oubliée ?

### Le verdict

**Produit par** le Relecteur, un par lot. **Lu par** l'orchestration.

📌 **Pourquoi il existe** : il décide si le lot passe, et si un échec
se corrige seul ou relance tout le lot. 🔴 **C'est aussi lui qui porte
la reprise** — le prochain lot est le premier de la séquence sans
verdict PASS.

**Un fichier par lot** : `code/<lot>/verdict.md`.

| Bloc | Contenu |
|---|---|
| Statut | PASS · PASS avec réserve · FAIL mineur · FAIL structurel |
| Cause, si FAIL | compréhension du lot · limite de raisonnement — alimente le seuil de passage à Opus |
| Divergences de symbole | lesquelles, et quel lot elles affectent |

**Structure** : un item par ligne — grepable pour l'agrégation.
**Absent par construction** : reformulation du lot, récit de ce qui a
été vérifié.

### Les fichiers de blocage

🔴 **Un agent qui ne peut pas produire écrit un fichier**, il ne se
contente pas de le dire.

**Un nom par agent** — `blocked_cadreur.md`, `blocked_verificateur.md`,
`blocked_detailleur.md`, `blocked_realisateur.md`,
`blocked_relecteur.md`, `blocked_controleur.md`.

| Bloc | Contenu |
|---|---|
| Ce qui bloque | Le fait constaté, pas son interprétation |
| Où | Le lot, le bloc, ou l'entrée concernée |
| Ce qu'il faudrait pour reprendre | Une décision, une correction en amont, une entrée absente |
| Décision | 🔴 **Écrit vide** — Khatya y répond à la main |

🔴 **Un blocage n'est pas un cul-de-sac.** Chaque agent cherche ses
propres blocages en premier geste : décision vide → il rebloque,
décision remplie → il l'applique et supprime le fichier.

📌 **Chacun a sa méthode d'application** — le Détailleur écrit sa fiche
contre la décision plutôt que contre l'entrée, le Réalisateur
code contre elle et le dit dans son compte rendu, le Vérificateur
rejoue ses quatre gestes depuis le début.

⚠️ **Bloquer n'est pas signaler.** Un défaut, une divergence, un écart :
ça part dans la sortie normale et le cycle continue. 🔴 **On ne bloque
que quand produire est impossible** — spec ambiguë pour le Détailleur,
fiche fausse pour le Réalisateur, trou ou cycle pour le Vérificateur.

📌 **Ne jamais bloquer par excès de prudence.** Le doute se signale.

### Écrire la sortie même vide

🔴 **Un fichier de sortie s'écrit toujours, même sans contenu.** Un
rapport d'écarts vide dit *« rien trouvé »* ; son absence dit *« l'agent
n'a pas tourné »*. L'orchestration ne peut pas distinguer les deux
autrement.

### Le principe commun à tous

**Prose** : ces fichiers sont lus par des agents, pas par le Product
Owner. 🔴 **En anglais**, comme tout fichier destiné à un agent —
⚠️ **sauf les libellés d'interface**, cités dans leur langue
d'affichage.

🔴 **Présent de l'indicatif, voix active.** *« Le lot produit… »* —
jamais « il faudra », jamais « on pourrait ».

🔴 **Un champ, une réponse.** Ce qui ne répond pas au champ n'y est pas.

**Interdits** : le futur, le conditionnel, la justification d'un choix
— elle est dans le fichier de l'agent qui l'a fait, pas ici.

⚠️ **Nommer les symboles exactement**, jamais approximativement. Une
signature reformulée de mémoire est la première cause de divergence.

🔴 **Pas de plafond de longueur.** Déjà écarté pour les blocs, même
logique ici : une limite en lignes est arbitraire et contredit notre
propre critère.

📌 **Ce qui prévient la dérive, c'est la structure à champs fixes.**
Rien n'invite à développer au-delà de ce que chaque champ demande — pas
parce qu'on l'interdit, mais parce qu'il n'y a nulle part où mettre du
superflu.

---

## Le mécanisme d'état projeté

**Le Cadreur peut découper tous les lots d'un coup, sans attendre
qu'aucun soit exécuté.**

Chaque lot déclare deux choses :
- **ce dont il a besoin** — ce qui doit exister avant
- **ce qu'il va produire** — le service créé, la table ajoutée, la route

Le lot B se découpe en sachant que A aura créé `XService`. C'est de
l'**état projeté**, et il suffit.

### D'où vient alors la péremption

Pas du temps qui passe. **De la divergence entre ce qu'un lot a promis
et ce qu'il a livré.**

Deux causes :
- le lot a fait autrement que prévu
- **un autre travail est passé entre-temps** et a pris ce que le lot
  suivant comptait utiliser

### Le contrôle qui en découle

**Pas « le code a-t-il bougé »** — trop large, et c'est ce qui coûte
cher aujourd'hui.

**Mais « les lots dont je dépends ont-ils livré ce qu'ils
annonçaient »** — quelques vérifications ciblées, nommées d'avance.

📌 Cela suppose que le Réalisateur **écrive ce qu'il a réellement
produit**, pas seulement ce qu'il a fait.

### Où la divergence se détecte

**Le Relecteur compare les symboles promis à ceux réellement créés.**
Noms et signatures — pas le comportement, il le juge par ailleurs. Un
grep par symbole, dans une invocation qui a lieu de toute façon.

🔴 **L'alternance bloc par bloc réduit la surface d'erreur à presque
rien.** Le Détailleur des providers écrit ses signatures *après* que
les services aient été codés : il lit ce qui existe, pas ce qui était
promis. **Une divergence ne peut donc contaminer que les lots d'un même
bloc**, détaillés ensemble avant d'être codés.

- **Conforme** → on enchaîne.
- **Divergence dans le bloc courant** → les lots non encore codés du
  bloc sont corrigés avant d'être réalisés.
- **Divergence découverte plus tard** → elle ne touche pas les blocs
  suivants, qui seront détaillés sur le code réel.

📌 *C'est ce qui manque aujourd'hui : un step a ajouté une bottom
sheet, personne n'a mis à jour les steps suivants, et le compte est
devenu faux plusieurs steps plus loin. Ici, le Détailleur du bloc
suivant l'aurait vu en lisant le code.*

---

## Les agents en détail

### Le Cadreur

**Entrées** — `spec-technique.md` · `docs/CURRENT_TECHNICAL_STATE.md`

📌 **Les conventions de découpage sont dans ce fichier même** — ce sont
des propriétés du process, pas du projet.

**Sortie** — la liste des lots

#### Les six gestes, dans cet ordre

**1. Grep `<<ASSUMED`** — 🔴 **une seule occurrence bloque.** Le
marqueur dit qu'une règle est provisoire.

**2. Lire le document technique en entier, préambule d'abord.** 📌
C'est le seul agent qui le lit tout. ⚠️ **Son `Out of scope` dit ce que
la feature ne touche pas** — jamais de lot pour ce qui y figure.

**3. Inventorier les symboles.** Parcourir chaque entrée et noter,
pour chaque symbole nommé, **tout ce qu'on lui demande** — une
opération, un champ lu, un libellé cité. 🔴 **C'est l'union qui
compte** : une repository dont l'entrée créatrice décrit quatre
écritures et dont les écrans demandent trois lectures porte sept
opérations.

⚠️ **Un libellé donné en toutes lettres est un symbole** — la clé qui
le porte.

📌 **L'inventaire s'écrit dans `decoupage.md`, avant les lots.**

**4. Section par section, grouper les entrées en lots.**

**5. Nommer besoins, productions et modifications**, puis greper chacun
dans le document d'état. ⚠️ **Non trouvé mais marqué `existant` dans le
préambule → besoin préexistant** : le document d'état n'est pas
exhaustif.

**6. Citer les entrées que chaque lot prend** — toutes d'une seule
section.

🔴 **Produire et modifier ne sont pas la même chose.** Un lot qui
change un symbole existant le déclare en modification, jamais en
production — le document d'état dit lesquels existent. ⚠️ **Sur une
correction ou une évolution, un lot ne produit souvent rien** : il ne
fait que modifier.

🔴 **Un type du framework n'est jamais une production.** Le projet
l'utilise, il ne le construit pas. ⚠️ **Sur une application neuve,
presque tous les types en sont** — le code est vide et le document
d'état avec lui.

🔴 **Pour chaque déclencheur nommé, quel symbole l'observe ?** Il entre
dans les modifications du lot, même si aucune entrée ne le nomme.
⚠️ **Ce qui réagit à un événement l'observe rarement** — un écran ne
voit pas la navigation qui l'a quitté.

🔴 **Une entrée qui dit quand une règle s'applique nomme aussi un
déclencheur** — un événement système, ou un moment dans un flux que le
code contrôle. *« À la fin de chaque kilomètre »*, *« dès que le lien
est établi »* : **le lot qui porte ce moment déclare la règle en
besoin.** 📌 **Une règle que personne n'appelle est du code mort.**

🔴 **Nommer ce qui appelle chaque production** — un lot, ou quelque
chose hors du découpage : une route, le framework, le système.

#### Ce qui fait un lot

**Une unité livrable** — l'application reste cohérente une fois qu'il
est passé. ⚠️ **Ce critère ne suffit pas à découper** : plusieurs
découpages le satisfont.

**Trois contraintes le resserrent :**

🔴 **Un lot cite des entrées, jamais un `§3` nu.** Une entrée, ou
plusieurs quand elles décrivent une seule chose à construire.

🔴 **Et jamais sur deux natures.** `§3.1` et `§9.2` ne cohabitent pas
dans un lot : il n'appartiendrait à aucune couche.

🔴 **Deux lots ne touchent jamais le même symbole**, ni en production
ni en modification. Leurs changements se recouvriraient sans que rien
ne le détecte. 📌 **Le même fichier, en revanche, est permis** — ce
n'est pas un conflit.

🔴 **Un lot tient dans un contexte sain.** Les plafonds par couche :

| Couche | Lots par bloc | Ce qu'un lot ajoute en lecture |
|---|---|---|
| Modèles, migrations | **8-10** | Presque rien — les tables tiennent dans un fichier |
| Services | **6-8** | Sa section de spec, quelques greps |
| Repositories | **6-8** | Le modèle qu'il porte |
| Providers | **4-6** | Le service consommé, sa signature |
| Écrans | **3-4** | Providers, routes, clés ARB, navigation |

⚠️ **Ce sont des plafonds indicatifs, pas des cibles**, et ils bornent
un bloc — que le Vérificateur formera. Le Cadreur s'en sert pour
calibrer ses lots : dix services relevant d'une même section tiennent
ensemble ; s'ils viennent de six sections, ils feront six lots.

📌 **Une entrée qui décrit une seule chose donne un lot d'une
entrée.**

🔴 **C'est la phase qui détermine tout le reste** — un lot trop gros
rend sa réalisation impossible dans un contexte sain.

#### Ce qu'il ne fait jamais

- 🔴 **Recopier une règle du document technique.** L'ancre la remplace :
  le Détailleur ouvre les entrées citées et lit la source, jamais une
  reformulation
- 🔴 **Ancrer un lot sur un `§3` nu, ou sur deux natures**
- 🔴 **Fusionner en cascade** — une passe, sur les déclarations du
  geste 4
- 🔴 **Lire le code** — il lit le document d'état, pas les fichiers
- 🔴 **Écrire une signature ou un critère d'acceptation** — c'est le
  Détailleur

---

### Le Vérificateur

**Entrées** — la liste des lots · **les sections qu'elles ancrent**,
ouvertes une par une. Rien d'autre.

**Sortie** — la séquence, les défauts constatés, et **les blocs pour le
Détailleur**

#### Les quatre gestes, dans cet ordre

**1. Croiser l'inventaire contre les lots**, et noter quatre sortes de
défaut : une surface non construite, un trou, un recouvrement, **et une
production que personne n'appelle**.

🔴 **La surface non construite est le contrôle que les noms seuls ne
permettent pas.** Un lot qui a besoin de `RaceRepository` et un lot qui
le produit se croisent parfaitement ; que l'un écrive et l'autre lise
ne se voit que sur l'inventaire.

📌 **Sur une production inappelée, il vérifie qu'un appelant est
nommé**, pas qu'il est juste — le Cadreur connaît le framework, lui
non.

⚠️ **Une modification crée aussi une dépendance.** Un lot qui consomme
un symbole qu'un autre modifie doit venir après lui — sinon il code
contre l'ancienne signature.

🔴 **Deux lots ne modifient jamais le même symbole.** C'est un défaut
de découpage : leurs changements se recouvriraient sans que rien ne le
détecte.

🔴 **Un cycle est un défaut, pas un blocage.** Le Vérificateur le
signale, laisse l'ordre et les blocs vides, et le Cadreur redécoupe.

**2. Ouvrir chaque entrée citée**, une par une, et confronter :

🔴 **Les entrées citées sont-elles d'une seule section ?** `§3.1`,
jamais `§3`. **Plusieurs sont légitimes** — un lot groupe ce qui
construit une chose. ⚠️ **Des entrées de deux sections sont un
défaut.**

🔴 **Décrivent-elles ce que le lot annonce ?**

🔴 **Ce que le lot déclare produire correspond-il à ce qu'elle
décrit ?** Un lot annonçant un service là où la spec décrit deux choses
à construire est mal découpé.

📌 **Ces deux contrôles protègent le Détailleur.** Une ancre fausse ou
un lot incohérent produirait une fiche fausse — et une fiche fausse
contamine tout un bloc.

**3. Dériver l'ordre** des déclarations de dépendance. 📌 **Ce n'est
pas un ordonnancement** : il découle mécaniquement, il ne se décide
pas.

**4. Regrouper en blocs** — voir ci-dessous.

🔴 **C'est lui qui regroupe parce qu'il a l'ordre.** Un bloc doit être
contigu dans la séquence — sinon on détaillerait ensemble des lots
qu'on ne peut pas coder à la suite. ⚠️ **Le Cadreur ne peut pas
grouper** : il voit les lots, il n'a pas encore leur ordre
d'exécution.

**La taille d'un bloc** — le critère est le **partage des lectures**,
borné par les plafonds par couche que porte le Cadreur.

🔴 **Les plafonds comptent des lots, pas leur poids.** Un lot citant
cinq entrées en pèse cinq — le compter par entrée citée.

🔴 **Entre lots éligibles au même moment, prendre celui dont la couche
est celle du lot précédent.** Rien qui corresponde → l'ordre de la
liste. **Le départage est mécanique**, donc reproductible.

⚠️ **Estimations dérivées d'un raisonnement, pas de mesures.** Ce dont
on est sûr est l'ordre : un écran coûte plus par unité qu'un modèle,
parce qu'il dépend de tout ce qui précède. **À calibrer** — le
Détailleur rapporte son contexte en fin de bloc ; trois ou quatre blocs
suffiront.

📌 **Regard indépendant sur le découpage** — justifié par (b), pas par
le contexte.

#### Ce qu'il ne fait jamais

- 🔴 **Corriger un découpage** — il constate, le Cadreur reprend
- 🔴 **Lire au-delà de la section ancrée.** S'il en a besoin pour
  comprendre un lot, c'est que le découpage est mauvais — un défaut à
  signaler, pas à corriger
- 🔴 **Écrire une signature ou du code**
- 🔴 **Laisser passer un cycle** — c'est un blocage, pas un défaut

---

### Le Détailleur

**Entrées** — la liste des lots, restreinte à son bloc *(la séquence
dit lesquels)* · le préambule du document technique · **les
entrées que leurs lots citent** · `CURRENT_TECHNICAL_STATE.md`
· les comptes rendus des lots déjà codés, **grepés jamais ouverts** ·
`TECHNICAL_CONVENTIONS.md`, **en entier** · **le code, en grep
uniquement**

⚠️ **Le code sert à confirmer l'existence d'un symbole, jamais à
comprendre une règle.** Un grep, pas une lecture de fichier — le
document d'état ne suffit pas : c'est un inventaire, il ne prouve pas
qu'un type existe.

📌 **Il ouvre les entrées de son bloc, pas le document entier.**

⚠️ **Le Vérificateur a lu les mêmes — ce n'est pas un doublon.** Il y
cherchait si l'ancre pointe juste ; le Détailleur y cherche la règle à
traduire en signature.

📌 **Les conventions se lisent en entier** : le nommage est la part
visible, mais le découpage en modules et les interdits contraignent une
signature tout autant.

**Sortie** — les fiches exécutables des lots du bloc

#### Les six gestes, par lot du bloc

**1. Ouvrir chaque entrée que le lot cite** — 🔴 **un lot
en cite souvent plusieurs**, et elles décrivent une seule chose à
construire.

**2. Lire les deux sections ouvertes du document d'état** — pièges
généraux et état mort, en entier. 🔴 **On ne peut pas greper une règle
dont on ignore qu'elle s'applique.** 📌 **Un piège change une
signature.**

**3. Pour chaque règle décrite, dériver une signature** — voir
ci-dessous. 📌 **Les conventions de nommage s'appliquent ici**, et le
`Vocabulary` du préambule fixe les termes.

**4. Greper chaque symbole avant de l'écrire.** 🔴 **Tout type employé
doit exister, venir du framework, ou être produit par ce bloc** —
confirmé par grep, jamais de mémoire.

🔴 **Toute recherche de code cible `lib/`.** Sans chemin, elle ratisse
`docs/` et `build/`, et remonte de vieux plans comme du code.

📌 **Un symbole trouvé : d'où vient-il ?** Un second grep dans les
comptes rendus du cycle. **Une occurrence** → un lot antérieur l'a
créé, le réutiliser. **Aucune** → il précède le cycle.

⚠️ **Si le grep contredit ce que le lot déclare**, voir plus bas.

**5. Écrire la signature**, une fois chaque type confirmé.

**6. Écrire les critères d'acceptation** — voir ci-dessous.

📌 **Une invocation par bloc, pas par lot** : le deuxième lot coûte
moins que le premier, il partage les lectures.

#### Production ou modification

🔴 **Le lot l'a déjà déclaré.** Le Cadreur a tranché, le Détailleur
applique :

| Déclaré comme | Ce qu'il écrit |
|---|---|
| **Production** | La signature du symbole à créer |
| **Modification** | La signature **après** changement, et ce qui change |

⚠️ **Si le grep contredit la déclaration** — un symbole déclaré en
production qui existe déjà, ou l'inverse — il le signale et s'arrête.
C'est un défaut de découpage, pas une décision à prendre ici.

📌 **La modification est le cas normal sur une application
existante.**

#### Dériver une signature d'une règle

**Une signature dit ce qui entre, ce qui sort, et sous quel nom.**

**Ce qui entre** — ce dont la règle a besoin et qu'elle ne peut pas
obtenir seule.

**Ce qui sort** — ce que la règle produit, sous un type qui **exprime
toutes ses issues**. 🔴 **Une règle à trois issues ne retourne pas un
booléen**, ni un booléen accompagné d'un effet de bord.

⚠️ **Une règle qui ne produit rien mais change un état** : la signature
dit ce qu'elle change ; le critère porte sur l'état après.

🔴 **La signature dit ce que vaut le retour aux limites** — absence,
vide, borne, unité, ordre. **Un type ne porte pas ça**, et deux lots
peuvent nommer le même symbole en en attendant deux choses
différentes.

**Le nom** — celui de la règle, dans le vocabulaire du produit, jamais
celui de la structure. `reconcile`, pas `processEntries`.

#### Écrire un critère d'acceptation

**Un critère est une observation vérifiable après coup** : quoi
observer, et ce qu'on doit voir.

🔴 **Trois propriétés, toutes obligatoires :**

| Propriété | Ce qu'elle exclut |
|---|---|
| **Observable** de l'extérieur du code | *« la fenêtre vaut 3 h »* — c'est l'implémentation |
| **Décidable** — deux personnes, même verdict | *« l'affichage est correct »* |
| **Attribuable** à ce lot | un critère qui échoue à cause d'un autre lot |

**Combien il en faut** : chaque comportement décrit par la section
ancrée doit être observable par au moins un critère.

⚠️ **Comportement, pas cas.** Un calcul à trois issues en demande
trois ; un écran, un par état affiché ; une migration, un sur ce que
deviennent les données existantes.

**Plus ce que la section nomme comme limite** — entrée absente, valeur
hors bornes, source indisponible.

🔴 **Un critère qu'on ne peut pas écrire comme un test n'est pas un
critère.** Si tu ne sais pas quoi observer, la règle est ambiguë : tu
t'arrêtes et tu remontes.

📌 **Pas de critère de non-régression.** *« Rien d'autre n'a changé »*
n'est ni décidable ni attribuable — c'est le Relecteur qui le voit, sur
le diff.

📌 **Ce qui pourrait rendre sa fiche fausse** — mauvaise ancre, lot
incohérent avec sa source — a été écarté par le Vérificateur avant lui.

#### Ce qu'il ne fait jamais

- 🔴 **Trancher une règle ambiguë** — *il n'est pas le filet de la
  chaîne amont*
- 🔴 **Employer un type sans l'avoir confirmé par grep**
- 🔴 **Recopier la règle dans la fiche** — elle vit dans la section
  ancrée
- 🔴 **Décider si un symbole se crée ou se modifie** — le lot le
  déclare, il applique
- Écrire du code

📌 **Le bloc est détaillé, puis codé, puis on passe au bloc suivant.**
Le Détailleur du bloc « providers » écrit ses signatures **après** que
les services aient été codés — il ne travaille plus sur des promesses,
mais sur ce qui existe. ⚠️ **La divergence ne peut donc survenir qu'à
l'intérieur d'un bloc**, entre lots détaillés ensemble. C'est une
surface d'erreur beaucoup plus petite.

---

### Le Réalisateur

**Entrées** — **la fiche exécutable du lot** *(signatures, critères,
dépendances)* · `TECHNICAL_CONVENTIONS.md` ·
`CURRENT_TECHNICAL_STATE.md`, **deux sections seulement** · le code
qu'il touche

**Sorties** — le code et les tests · le compte rendu, **incluant ce
qu'il a réellement produit**

🔴 **Pas de plan.** Le Détailleur a produit les signatures : il n'y a
plus d'architecture à décider.

#### Les huit gestes, dans cet ordre

**1. Déterminer où le code va**, à partir des conventions et des
symboles que la fiche demande. 🔴 **La fiche dit quoi écrire, les
conventions disent où** — le Détailleur ne décide pas de
l'emplacement.

**2. Lire les fichiers concernés**, et ceux qui portent les symboles
que la fiche déclare modifiés. 🔴 **Toute recherche de code cible
`lib/`** — sans chemin, elle ratisse `docs/` et `build/`.

**3. Lire les deux sections ouvertes du document d'état** — pièges
généraux et état mort, en entier. 📌 **Un piège change comment il
écrit, pas quoi** — et la fiche ne le dira pas.

**4. Implémenter dans l'ordre des dépendances de la fiche.** 📌 Il ne
le décide pas — le Détailleur l'a établi.

**5. Écrire un test par critère d'acceptation.** 🔴 **La correspondance
est directe** : un critère sans test est un critère non couvert. C'est
ce qui rend le lot vérifiable — le Relecteur compare les tests aux
critères, pas à une intention.

⚠️ **Sur une modification, des tests existants deviennent faux** — ils
vérifient l'ancien comportement. 🔴 **Il les adapte au nouveau, il ne
les supprime pas.** Un test retiré est un comportement qui cesse d'être
vérifié.

📌 **Un test qui échoue sans porter sur le lot** signale une régression :
il s'arrête et remonte, il ne le modifie pas.

**6. Lancer l'analyse statique et les tests** — jusqu'à ce que les deux
passent.

🔴 **Par bloc cohérent de travail, jamais par édition.** Un fichier et
ses tests, une couche, un écran et son provider : terminer, puis
vérifier. *(Mesuré sur dix steps : 41 relances sur 149 sans aucun
échec entre les deux ; une séquence a enchaîné 16 analyses propres
pendant que la même invocation écrivait encore.)*

🔴 **Grouper les corrections aussi.** Quand une exécution remonte
plusieurs échecs, les corriger tous, puis relancer une fois.

**7. Mettre à jour l'état projeté** — voir ci-dessous.

**8. Commiter**, en indexant explicitement ce qui appartient au lot.

#### Quand il reprend un lot en FAIL

**Un FAIL déclenche un Réalisateur neuf**, jamais celui qui a écrit le
code.

**Entrées** — les mêmes, **plus le verdict**.

**FAIL mineur** : corriger le point signalé, relancer l'analyse et les
tests, réécrire le compte rendu. 🔴 **Ne pas revisiter le reste du
lot.**

**FAIL structurel** : reprendre le lot depuis le geste 1.

⚠️ **Il ne discute pas le verdict.** S'il le juge faux, il s'arrête et
remonte plutôt que de coder contre.

#### Quand la fiche est fausse

🔴 **Il ne la corrige pas.** Une signature qui ne compile pas, un type
qui n'existe pas, une dépendance vers un lot non encore réalisé : il
s'arrête et remonte.

⚠️ **Improviser rendrait la divergence invisible** — le code
s'écarterait de la fiche sans que rien ne le signale. Le Détailleur a
produit la fiche, le Vérificateur aurait dû attraper l'erreur : c'est
en amont qu'elle se corrige.

#### Ce qu'il ne fait jamais

- 🔴 **Corriger une fiche fausse** — il s'arrête et remonte
- 🔴 **Décider d'une architecture** — les signatures sont posées
- 🔴 **Lancer l'analyse ou les tests par édition** — par bloc cohérent
- 🔴 **Écrire un test qui ne correspond à aucun critère**
- 🔴 **Discuter un verdict** — il corrige, ou il s'arrête

🔴 **C'est ici que le volume mord** — mesuré à ~440k si tout cohabite,
au-dessus de la zone de dégradation (~400k). ⚠️ Le volume dépend
entièrement de la taille du lot : c'est la variable d'ajustement, pas
le découpage en rôles.

---

#### La mise à jour de l'état — même invocation

**Le document d'état est `docs/CURRENT_TECHNICAL_STATE.md`**, unique
pour tout le projet.

🔴 **Charger le skill `technical-state-format` avant d'y écrire**,
jamais sans. C'est ce qui a évité sa dérive.

**Ce qui y entre** : un service, un provider, un mécanisme qu'un autre
lot pourrait reconstruire · une table, une route, une cascade · un
piège · un état mort.

🔴 **Ce que le lot a rendu faux disparaît** — une entrée n'est jamais
« modifiée par lot-03 ».

📌 **Appartient au Réalisateur**, dans la même invocation : il sait ce
qu'il vient de produire, ça ne coûte presque rien.

⚠️ **Ce document commande le Cadreur.** S'il ment, tout le découpage
suivant repose sur du faux.

---

### Le Relecteur

**Entrées** — **la fiche exécutable du lot** · le code produit · le
compte rendu · `docs/TECHNICAL_CONVENTIONS.md`

**Sortie** — le verdict : ce qui manque, et toute divergence de symbole

#### La checklist — quatre points, dans cet ordre

**1. Les symboles du lot correspondent à ce qui était promis.** Un grep
chacun. 🔴 **Toute divergence se signale**, même quand le code
fonctionne.

| Déclaré comme | Ce qu'il vérifie |
|---|---|
| **Production** | Le symbole existe, avec la signature de la fiche |
| **Modification** | Le symbole a **la nouvelle** signature, pas l'ancienne |

⚠️ **Sur une modification, l'existence ne prouve rien** — le symbole
existait déjà. Seule la signature dit si le lot a fait son travail.

**2. Un test par critère d'acceptation.** ⚠️ **La correspondance est
directe** — un critère sans test est un manque constatable, pas une
appréciation.

**3. Les conventions tiennent** sur ce que le lot a touché.

**4. Les autres champs du compte rendu tiennent** — l'analyse et les
tests passent, ce qui est entré dans le document d'état est nommé, une
proposition de convention ou un tiret. 📌 **Le point 1 a déjà couvert
les symboles.**

#### Ce qu'il ne vérifie pas

🔴 **La cohérence du lot avec sa source** — le Vérificateur l'a
confirmée en amont.

🔴 **La mécanique** — analyse statique, tests lancés, fichiers
présents : la boucle du Réalisateur les couvre.

📌 **Il juge l'interprétation, pas l'exécution.**

#### Le verdict

| Verdict | Quand |
|---|---|
| **PASS** | Les quatre points passent |
| **PASS avec réserve** | Un point passe, mais mérite d'être noté pour la suite |
| **FAIL mineur** | Un point échoue, isolé — correction ciblée, pas de relecture complète |
| **FAIL structurel** | Le lot ne fait pas ce que la fiche demande, ou plusieurs points échouent ensemble |

⚠️ **Ne jamais tomber sur structurel par défaut** pour un manquement
isolé.

#### Ce qu'il ne fait jamais

- 🔴 **Corriger lui-même** — il constate, un agent frais corrige
- 🔴 **Revérifier la cohérence du lot avec sa source** — le
  Vérificateur l'a faite
- 🔴 **Revérifier la mécanique** — la boucle du Réalisateur la couvre
- 🔴 **Tomber sur structurel par défaut** pour un manquement isolé

📌 **Une divergence ne menace que les lots non codés du même bloc** —
voir "Où la divergence se détecte".

🔴 **Justifié par (b) uniquement.** Ne peut jamais être le Réalisateur.

#### Relecture par lot, jamais par bloc

🔴 **Agent frais pour toute correction** — jamais celui qui a relu.
*(18 tours et 0,66M mesurés contre un agent repris qui recharge son
contexte.)*

🔴 **Chaque lot est relu à sa réalisation, pas en fin de bloc.** Sinon
une erreur sur le premier lot ne serait découverte qu'après que sept
autres aient été codés dessus — exactement ce que l'alternance bloc par
bloc évite déjà en amont.

⚠️ **Pas de vérification croisée entre les lots d'un bloc terminé.**
Ce serait un filet, pas une boucle. Si le Cadreur a bien groupé, les
lots d'un bloc partagent leur section de spec — une divergence entre
eux signale un mauvais découpage, pas un mauvais code. **À revoir si
l'usage montre des incohérences récurrentes.**

---

### Le Contrôleur

*Une fois par cycle, quand toutes les fiches existent.*

**Entrées** — le fichier produit de la fonctionnalité · toutes les
fiches exécutables

**Actions** — pour chaque bloc du fichier produit, trois issues :

| Issue | Ce qu'il écrit |
|---|---|
| **Retrouvée** | Le bloc, et la fiche qui la porte |
| **Absente** | Le bloc, et ce qu'il décrivait |
| **Douteuse** | Le bloc, et ce qui l'empêche de trancher |

📌 **Une fiche porte souvent plusieurs blocs** — un lot groupe les
entrées qui construisent une seule chose. ⚠️ **Confronter bloc par
bloc quand même** : une fiche qui couvre quatre blocs peut en rater un
cinquième.

🔴 **Le critère : l'intention est-elle observable dans une signature ou
dans un critère d'acceptation ?** Pas dans la prose d'une fiche — une
fiche qui *mentionne* un bouton sans qu'aucun critère ne l'observe ne
porte pas l'intention.

📌 **Sur une correction ou une évolution, l'intention se retrouve
surtout dans les critères** — les signatures existaient déjà. Un
comportement corrigé se lit dans ce qui doit être observable après, pas
dans un symbole créé.

🔴 **Il ne tranche pas un doute.** Une intention qu'il n'arrive pas à
rattacher part en douteuse, jamais en absente.

#### Ce qu'il ne fait jamais

- 🔴 **Lire le code** — le Relecteur couvre fiche → code
- 🔴 **Juger la qualité d'une fiche** — présence ou absence, rien
  d'autre
- 🔴 **Trancher un doute**
- 🔴 **Relancer quoi que ce soit** — le Product Owner décide

**Sortie** — le rapport d'écarts : ce qui est décrit et ne se retrouve
nulle part

🔴 **Justifié par (a) et (b).** Il raisonne en intentions produit, pas
en lots — contexte incompatible avec le Vérificateur, qui raisonne en
séquence et en ancres. Et celui qui a converti, découpé ou détaillé ne
peut pas constater qu'il a perdu quelque chose en route.

📌 **Le Relecteur couvre fiche → code, le Contrôleur couvre produit →
fiche.** Les deux mis bout à bout ferment la chaîne, sans qu'aucun
agent relise du code complet.

🔴 **Rien ne repart en automatique.** Le Product Owner lit le rapport
et décide s'il devient un fichier d'écarts pour le cycle bug fix.

⚠️ **Le coût de la découverte tardive est assumé** : les fiches
n'existent toutes qu'à la fin, à cause de l'alternance bloc par bloc.
Découvrir une intention perdue plus tôt supposerait de détailler tous
les blocs d'avance — ce que l'alternance interdit délibérément.

---

### Le Product Owner — hors boucle

**Entrées** — l'application complète · le rapport d'écarts

**Sortie** — OK, ou ce qui cloche

📌 Ce qu'aucun test ne dit : est-ce que ça a l'air juste, est-ce que le
parcours est fluide, est-ce que le texte est bon.

---

## Modèle par agent

**Cadreur, Vérificateur — Opus, systématique.** Ils décident de la
structure entière ; une erreur ici se propage à tout le document
technique. Le coût reste faible en absolu : une invocation chacun par
document technique, pas par lot.

**Détailleur, Réalisateur — Sonnet, sans exception.** 🔴 **Pas de
plancher par couche ni par type d'action.** L'ancienne matrice de
risque (LOW/MEDIUM/HIGH) a été construite sur des steps traversant
plusieurs couches ; on ne sait pas si ses planchers restent justifiés
sur un lot mono-couche, isolé. Plutôt que deviner un nouveau plancher,
on mesure.

**Relecteur — Sonnet.** Sa checklist reste une vérification contre
critères, pas de la conception.

**Contrôleur — Sonnet.** Il constate une présence ou une absence, il ne
juge ni la qualité ni la conception. ⚠️ **À réévaluer si les faux
négatifs apparaissent** — reconnaître qu'une fiche porte bien une
intention formulée autrement est de la compréhension, pas de la
comparaison.

### Comment le modèle du code s'ajuste, à l'usage

**Le Relecteur qualifie la cause de chaque FAIL structurel** — erreur
de compréhension du lot, ou limite de raisonnement (calcul mal conduit,
cascade mal anticipée). Seule la seconde justifierait Opus.

**Un seuil déclenche l'ajustement** : un type de lot ayant accumulé
plusieurs FAIL structurels attribués au raisonnement passe en Opus par
défaut pour ce type. *(Seuil non fixé — à poser sur les premières
observations.)*

⚠️ **Le premier document technique tourne sans filet de risque.** Une
migration complexe ou un calcul critique s'exécute en Sonnet comme le
reste, et une éventuelle limite de raisonnement se découvre après coup,
pas avant. C'est le compromis accepté : mesurer plutôt que supposer.

📌 **Ce pari se joue sur une application de test dédiée**, pas sur
l'application en production — ce qui rend le risque acceptable pendant
que le process s'éprouve.

---

## Mode opératoire

### Où vivent les fichiers

**Le même dossier que l'amont** : `docs/features/<nom>/`, dans un
sous-dossier `code/`.

    spec-technique.md         ← entrée, produite en amont
    desc-produit.md           ← lu par le Contrôleur, produit en amont

    code/
      decoupage.md            Cadreur
      sequence.md             Vérificateur
      rapport-controle.md     Contrôleur
      blocked_<agent>.md      Cadreur, Vérificateur, Contrôleur

      lot-01/
        fiche-executable.md   Détailleur
        compte-rendu.md       Réalisateur
        verdict.md            Relecteur
        blocked_<agent>.md    Détailleur, Réalisateur, Relecteur

📌 **Un dossier par lot** — ses trois fichiers vivent ensemble, et un
lot se lit d'un coup d'œil.

🔴 **La reprise en découle** : le prochain lot est le premier de la
séquence dont le dossier n'a pas de `verdict.md` en PASS.

🔴 **Noms fixes** — c'est ce qui permet aux commandes de n'avoir qu'un
seul argument : le nom de la feature.

    /8_code panneau-calories 3

### Deux commandes

Chacune porte son propre mode — comme `/start_creating`.

### `/7_decoupe <feature>`

**Cadreur → Vérificateur**, jusqu'à zéro défaut constaté.

🔴 **Trois tours maximum.** Un défaut signalé renvoie au Cadreur avec
la liste des défauts ; au troisième tour sans convergence,
l'orchestrateur s'arrête et rend la main.

**Sortie** : la séquence et les blocs. 📌 **C'est la pause naturelle** —
tout est décidé, rien n'est codé.

### `/8_code <feature> [N]`

**Par défaut, un lot.** `N` en demande davantage.

⚠️ **Le compteur porte sur les lots relus PASS**, pas sur les
invocations : le Détailleur passe quand un bloc neuf commence, sans
entrer dans le décompte.

**Reprise** — 🔴 **le prochain lot est le premier de la séquence sans
verdict PASS.** Une lecture, pas un scan : la séquence porte l'ordre et
les blocs.

**La boucle, par lot** :

1. Si le bloc du lot n'a pas de fiches → **Détailleur** sur ce bloc
2. **Réalisateur** → **Relecteur**
3. FAIL → Réalisateur neuf, avec le verdict. 🔴 **Trois reprises
   maximum** par lot, tous types de FAIL confondus
4. ⚠️ **Si le verdict nomme des lots affectés par une divergence** →
   Détailleur sur le bloc, pour réécrire leurs fiches seulement
5. Lot suivant

**Quand tous les lots ont un PASS** → **Contrôleur**, puis arrêt.

### Où il s'arrête et rend la main

🔴 **Un `blocked_*.md`**, quel qu'il soit — 📌 **à deux endroits** :
`code/blocked_<agent>.md` pour le Cadreur, le Vérificateur et le
Contrôleur, `code/<lot>/blocked_<agent>.md` pour les trois autres.

🔴 **Le Vérificateur signale un défaut au troisième tour** — le
découpage ne converge pas.

🔴 **Un lot échoue trois fois.**

🔴 **`N` lots ont été relus PASS.**

🔴 **Le Contrôleur a fini** — le rapport d'écarts est à lire.

⚠️ **Sinon il ne s'arrête jamais.** Un FAIL isolé, un bloc terminé, une
correction qui passe : il continue.

### Où une pause est impossible

📌 **Une pause n'est sûre que là où un artefact est complet.**

| Entre | Pourquoi non |
|---|---|
| Détailleur et Réalisateur, dans un bloc | Le Détailleur produit toutes les fiches du bloc en une invocation |
| Réalisateur et Relecteur | Le code existe, non relu — l'état est indéterminé |
| Une correction et sa relecture | Le lot n'a ni PASS ni FAIL |

---

## Les trois cas d'entrée

📌 **La chaîne aval ne voit qu'un document technique.** L'origine — une
feature neuve, une évolution, une correction — se décide en amont et ne
compte plus ici.

| Cas | Ce qu'il produit en aval |
|---|---|
| **Feature neuve** | Surtout des productions |
| **Évolution** | Un mélange de productions et de modifications |
| **Correction** | Presque uniquement des modifications |

🔴 **Un seul mécanisme les couvre** : un lot déclare ce qu'il produit
*et* ce qu'il modifie, et le Relecteur vérifie l'existence des
premières, la nouvelle signature des secondes.

⚠️ **Rien d'autre ne change.** Pas de mode, pas de branche — la
différence est de proportion, pas de nature.

---

## Questions ouvertes

🟡 **Calibrer les tailles de bloc** — les valeurs par couche sont des
estimations. Le Détailleur rapporte son contexte de fin ; trois ou
quatre blocs diront si elles tiennent.

🟡 **Poser le seuil de passage à Opus** sur le code — non fixé,
à déterminer sur les premiers FAIL structurels qualifiés par le
Relecteur.
