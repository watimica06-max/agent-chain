# Process amont — de l'idée au document technique

> Documentation de référence. Décrit la chaîne **idée produit →
> document technique exploitable par le Cadreur** — l'entrée du process
> aval, décrit dans `PROCESS_AVAL.md`.
>
> 🔴 **Aucun agent ne lit ce document.** Il dit pourquoi les agents sont
> construits comme ils le sont, y compris des règles envisagées puis
> écartées.

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

---

## Les agents

*Chacun est détaillé plus bas, "Les agents en détail".*

### 1. Analyste

**Recueille l'idée du Product Owner et produit le fichier descriptif de
la fonctionnalité.** Deux invocations : structuration — qui traite
aussi les réponses — et recherche des angles morts.

**Connaît le document produit global** — sans lui, il demanderait *"que
doit contenir cet écran ?"* là où la vraie question est *"l'écran
existe, qu'est-ce que tu changes ?"*.

⚠️ **Aucun dialogue** — le Product Owner écrit hors ligne, l'Analyste
transcrit. Le cycle peut s'étaler sur plusieurs jours.

### 2. Convertisseur

📌 **Il applique `docs/process/GRILLE_FERMETURE_TECHNIQUE.md`** — huit
fermetures en deux parties : nature et cohérence sur le fichier
produit, puis traçabilité, unicité, accord entre entrées, liens
déclarés, ressources et complétude sur le document technique.
🔴 **La grille porte les tests, l'agent porte les gestes.**

**Ferme le fichier produit sous l'angle technique, puis produit le
document technique** pour le Cadreur. Deux invocations, séparées par un
ping-pong de questions avec l'Analyste.

📌 **Deux, pas une** : la première signale et attend tes réponses, la
seconde traduit une fois le ping-pong clos.

### 3. Fusionneur

**Fusionne le fichier produit dans le document global, et produit un
rapport de fusion.** Deux invocations, séparées par un ping-pong de
questions comme pour le Convertisseur.

🔴 **Ce rapport est le seul travail manuel du Product Owner** de toute
la chaîne.

---

### 4. Diagnostiqueur — cycle bug fix

**Confronte un fichier d'écarts au document global** et produit un
fichier produit ne portant que les écarts confirmés.

📌 **Il n'intervient que sur une correction de défaut** — voir "Les
quatre points d'entrée".

---

### 5. Extracteur — reprise d'une application existante

**Construit le document global depuis le code**, quand il n'existe pas.
Une invocation par domaine.

📌 **Il n'intervient qu'une fois**, à la reprise d'un projet déjà codé.

---

## Les fichiers

| Fichier | Écrit par | Lu par |
|---|---|---|
| **Fichier d'idées** | Product Owner, hors ligne | Analyste |
| **Fichier d'écarts** *(bug fix)* | Product Owner, hors ligne | Diagnostiqueur |
| **Fichier produit d'une fonctionnalité** | Analyste — ou Diagnostiqueur en cycle bug fix | Analyste, Convertisseur, Fusionneur |
| **Document produit global** | Fusionneur | Analyste, Product Owner |
| **Document technique** | Convertisseur | Cadreur *(process aval)* |
| **Plan de fusion** | Fusionneur, 1ʳᵉ invocation | Fusionneur, 2ᵉ invocation |
| **Fichier de questions** | Convertisseur ou Fusionneur *(questions)*, Product Owner *(réponses)* | Son émetteur, Analyste, Product Owner |
| **Rapport de fusion** | Fusionneur | Product Owner |
| **Grille de cadrage produit** | Khatya, hors chaîne | Analyste, 2ᵉ invocation |
| **Grille de fermeture technique** | Khatya, hors chaîne | Convertisseur, les deux invocations |

📌 **Le fichier d'idées n'a aucun format** — c'est le seul de la chaîne.
Le structurer est le travail de l'Analyste.

**Noms sur disque et emplacement** : voir "Mode opératoire".

📌 **Les deux premiers partagent la même structure** — décrite ci-après
une seule fois. C'est ce qui rend la fusion mécanique au niveau
structurel. Le troisième est d'une autre nature : structuré par couche
technique.

### Le fichier d'idées

**Écrit par** le Product Owner, hors ligne. **Lu par** l'Analyste.

🔴 **Aucun format, aucune règle de prose, écrit en français** — c'est
tout l'intérêt. Le structurer et le traduire est le travail de
l'Analyste.

📌 **C'est le seul document français de la chaîne.**

**Aucune limite de volume non plus.** Un domaine riche produit un
fichier riche : plusieurs centaines de lignes couvrant un seul domaine
est un cas normal, pas un signal de mauvais découpage.

📌 **Le seul critère est celui du domaine** : *ce que la feature fait,
en une phrase, sans « et »*. Si elle en demande deux, ce sont deux
cycles.

**Structure suggérée, non imposée** : écrire par sujet plutôt qu'en flux
continu — un paragraphe par écran, par règle, par mécanisme. L'Analyste
décompose de toute façon, mais il se trompera moins.

### Les deux fichiers produit

**Produits par** l'Analyste — ou le Diagnostiqueur en cycle bug fix —
*(fichier d'une fonctionnalité)* et le Fusionneur *(document global)*.
**Lus par** tous les agents amont et le Product Owner.

| Bloc | Contenu |
|---|---|
| Arborescence | Application, puis domaines |
| Sections | Un sujet produit — écran, fonctionnalité, mécanisme |
| Blocs | Un sujet chacun, avec son identifiant et sa nature |

**Prose courte et descriptive, structure fixe et greppable.**

🔴 **Structure identique pour les deux** — sinon la fusion devrait
traduire, et ce serait le seul travail de la chaîne que personne ne
relit.

#### L'arborescence : application, domaines

**Application** — ce qui ne dépend d'aucune fonctionnalité :
authentification, langues, thème, politique de confidentialité.

**Domaines** — un par ensemble fonctionnel cohérent, chacun avec ses
sections.

**Critère de création d'un domaine** : un ensemble dont on peut dire ce
qu'il fait en une phrase, sans « et ».

🔴 **Convention de niveaux, fixe** — c'est elle qui rend l'index
greppable :

    # Application            une fois, en tête du fichier
    # Domaine : <nom>        un par domaine
    ## <Section>
    ### <Bloc>

📌 **`#` pour l'application comme pour les domaines** : l'application
n'est pas leur parent, c'est un pair qui porte le transverse. **L'index
s'extrait sur `^#`** — les quatre niveaux d'un coup, ou `^##` pour les
seules sections.

**Aucun ordre imposé entre les sections d'un domaine.** Le document se
lit par l'index, pas linéairement.

⚠️ **Pas de troisième niveau**, même sur un domaine volumineux.

🔴 **Un ensemble à cheval sur plusieurs domaines est un domaine**, qui
consomme les autres — un tableau de bord n'appartient pas aux domaines
qu'il affiche.

📌 **Dans le fichier d'une fonctionnalité**, seuls les domaines touchés
apparaissent — jamais l'arborescence complète.

#### La structure interne

**Une section regroupe ce qui parle du même sujet produit** — un écran,
une fonctionnalité, un mécanisme.

**Un bloc = un sujet.** Un comportement, une règle, un paramètre, un
écran. Si un bloc parle de deux choses, on le sépare en deux blocs.

🔴 **La séparation vient du produit, jamais de la technique.** La
nature se pose ensuite.

**Chaque bloc porte un identifiant et une nature**

    ### B7 — Rejecting invalid durations
    Nature: external source

    An entry whose duration is negative or over 24 hours is ignored: it
    appears nowhere and produces no message.

**Le numéro est local au fichier d'une fonctionnalité**, attribué à
l'écriture et jamais réattribué — il sert au fichier de questions à
désigner un bloc précis, et à rien d'autre.

🔴 **Il ne passe jamais dans le global.** Le Fusionneur ne le reprend
pas : dans le global, un bloc n'a que son titre. Sinon deux features
livreraient chacune leur `B7`.

📌 **C'est le titre qui porte l'identité durable**, repris du document
global quand le bloc y existe déjà — voir ci-dessous.

**Les natures possibles** sont celles des douze sections du document
technique : model · persistence · calculation · transition ·
external source · synchronisation · background work · journey ·
screen · text · access · lifecycle.

⚠️ **Un bloc de plusieurs natures porte deux sujets** — le séparer.
🔴 **Si c'est ambigu, l'Analyste pose la question**, autant
de fois qu'il le faut. Jamais deux natures sur un bloc.

#### Les règles d'écriture des fichiers produit

**La prose**

🔴 **Présent de l'indicatif, voix active.** *« L'écran affiche… »* —
jamais *« il faudra afficher »* ni *« l'écran devrait »*.

🔴 **Une phrase = une règle.** C'est ce qui rend la fusion phrase à
phrase possible.

**Interdits** : le futur, le conditionnel, l'impératif, le vocabulaire
du changement — « nouveau », « désormais », « au lieu de ». ⚠️ **Et la
justification** : une règle qui a besoin d'être expliquée doit être
reformulée.

**Nommer les choses comme l'utilisateur les voit**, jamais par les
identifiants du code.

🔴 **Tout s'écrit en anglais**, comme partout dans la chaîne d'agents.
⚠️ **Sauf les libellés cités** : un texte affiché se décrit dans sa
langue d'affichage.

📌 **Le fichier d'idées est le seul document français** — le Product
Owner l'écrit, l'Analyste traduit en structurant. Il traduit de même
les réponses du fichier de questions.

📌 **Quatre agents écrivent dans ces fichiers** — Analyste,
Diagnostiqueur, Extracteur, Fusionneur. Sans règle explicite, quatre
styles, et la fusion phrase à phrase ne reconnaîtrait plus les mêmes
règles.

**Créer une section**

**Un titre nomme ce dont la section parle**, tel qu'un humain le
désignerait — *« Écran d'ajout d'activité »*, pas *« Ajout »* ni un nom
de classe.

🔴 **Chercher avant de créer.** Un titre proche mais différent crée un
doublon que rien ne rattrapera.

**Créer quand aucune section existante ne traite ce sujet** — pas
quand le sujet est nouveau dans la feature.

**Créer un domaine**

🔴 **Même critère que partout** : un ensemble dont on dit ce qu'il fait
en une phrase, sans « et ».

⚠️ **C'est rare.** Une section nouvelle se range presque toujours dans
un domaine existant ; créer un domaine suppose que la feature
introduise un ensemble fonctionnel entier.

📌 **En cas de doute, ranger dans l'existant** — un domaine de trop
fragmente le global durablement.

**Les titres sont repris du document global**

🔴 **Avant de créer une section, l'Analyste consulte le
global.** Si une section traite déjà ce sujet, il **reprend son titre à
l'identique**. Sinon, il en crée une.

**Même mécanisme au niveau du bloc** : si le bloc révise une règle
existante, il reprend le titre du bloc du global. Sinon, nouveau titre.

⚠️ **S'il n'est pas sûr qu'une section existante corresponde, il
demande.** Deux sections proches sous des noms différents produiraient
deux entrées là où il n'y en a qu'une.

**Ce que ça donne à la fusion** : titre connu → fusion dans l'entrée
existante ; titre nouveau → insertion, rangée par cohérence — les
écrans avec les écrans.

🔴 **Deux niveaux d'identifiant, pas trois.** Un identifiant dit *où*
fusionner, jamais *quoi remplacer à l'intérieur*.

📌 **Le contenu se fusionne par compréhension** — c'est ce que le
rapport de fusion soumet au Product Owner.

**Les références sortantes sont marquées**

Quand un bloc renvoie à autre chose — un écran, une donnée, un état,
une règle — la destination est **nommée**, et 🔴 **marquée comme
existante si elle est déjà dans le global** :

> *« Le bouton Pas redirige vers l'écran de saisie des pas —
> existant. »*

📌 **C'est l'Analyste qui pose ce marqueur** : il est le seul
à voir le global. Sans lui, le Convertisseur signalerait un faux
manque, n'ayant aucun moyen de savoir que l'écran existe.

⚠️ **Une référence à l'existant n'empêche pas sa révision dans le même
fichier.** Le bloc renvoie à l'écran existant ; une autre section peut
le réviser — les deux coexistent sans conflit.

**Ce qui n'a pas à figurer**

🔴 **Ce qui est hérité et inchangé ne se réécrit pas.** Si la politique
de confidentialité, la rétention ou le consentement ne bougent pas, ils
n'apparaissent pas dans le fichier d'une feature — le global les porte
déjà.

**Ils n'y figurent que s'ils changent** — et c'est alors une section à
fusionner comme une autre.

#### Comment le document global se lit

🔴 **Par l'index, jamais en entier.** Extraire la liste des titres —
domaines, sections, blocs — coûte un grep quel que soit le volume du
fichier.

**Tout agent qui le lit charge donc :**

1. **L'index systématiquement** — quelques dizaines de lignes
2. **Les seules sections dont il a besoin**, identifiées depuis l'index

⚠️ **Un titre doit dire ce que sa section contient**, sinon l'index ne
sert à rien. C'est le critère de qualité du global.

📌 **Cette règle vaut pour les trois agents qui le lisent** — Analyste,
Fusionneur, Diagnostiqueur. Elle rend la lecture indépendante de la
taille du document.

#### Ce qui est propre au document global

**Il est vivant** — modifié fonctionnalité après fonctionnalité. Seul
document du process à échapper au principe *« un fichier est écrit une
fois »*. ⚠️ C'est le profil qui a produit trois fichiers devenus
inexploitables : plusieurs écritures, sans contrôle systématique.

🔴 **Il décrit l'état actuel, jamais l'historique.** Une entité révisée
n'accumule pas ses versions : la description antérieure disparaît,
remplacée par la nouvelle.

🔴 **Il ne se révise pas pendant qu'un cycle aval tourne sur le même
périmètre.** Une ancre posée par le Cadreur pointe vers un contenu qui
peut être remplacé en cours de route — le référent disparaît sans
laisser de trace.

⚠️ **Non éprouvé** — une révision urgente peut survenir pendant un
développement.

---

### Le fichier d'écarts — cycle bug fix

**Écrit par** le Product Owner, hors ligne. **Lu par** le
Diagnostiqueur.

🔴 **Sous les titres du document global** — section et bloc — pour que
la comparaison soit mécanique.

    ## Activity screen
    ### Add button
    Observed: absent

**Vocabulaire de constat, fermé** — un agent ne devine pas ce qu'un
raccourci veut dire :

| Constat | Sens |
|---|---|
| `absent` | Ne s'affiche nulle part, ne se déclenche jamais |
| `different` | Présent, mais ne correspond pas à la description |
| `conditional` | Présent dans certains cas seulement, alors qu'il devrait l'être partout — ou l'inverse |

⚠️ **Préciser le contexte quand il compte** : quel écran, quel état,
quelles conditions d'observation.

---

#### 5. Extracteur — reprise d'une application existante

**Construit le document global depuis le code**, quand il n'existe pas.
Une invocation par domaine.

📌 **Il n'intervient qu'une fois**, à la reprise d'un projet déjà codé.

---

## Les fichiers de travail

*Produits en cours de chaîne, datés, jamais modifiés après leur
dernière écriture — ils documentent ce que les agents ont compris et
restent consultables pour du debug de process.*

#### Le plan de fusion

**Produit par** la première invocation du Fusionneur. **Lu par** la
seconde, elle seule.

| Bloc | Contenu |
|---|---|
| Décisions par phrase | Cinq verbes : `REPLACE` · `INSERT` · `KEEP` · `DELETE` · `PENDING` |
| Phrases en attente | `PENDING`, avec l'identifiant de leur question |

⚠️ **`DELETE` ne vient jamais du Fusionneur** — seulement d'une réponse
confirmant qu'une règle ne tient plus.

🔴 **Il ne réécrit rien** — il consigne des décisions, le texte reste
dans le fichier produit et le global.

#### Le fichier de questions

**Produit par** le Convertisseur *(première invocation, ou seconde en
cas de contradiction)* ou par le Fusionneur *(première invocation)*.
**Répondu par** le Product Owner. **Lu par** son émetteur et
l'Analyste.

| Bloc | Contenu |
|---|---|
| Identifiant | Pour que la réponse revienne au bon endroit |
| Bloc concerné | Son numéro et son titre |
| Question | Ce qui manque, formulé |
| Réponse | Vide à la création — **remplie à la main par le Product Owner**, en français |

    ### Q3
    Block: B7 — Rejecting invalid durations
    Question: what happens to an entry whose duration is zero?
    Answer:

📌 **Questions en anglais, réponses en français** — l'Analyste traduit
en intégrant.

**Une question par entrée**, jamais groupées.

**Prose** : la question formulée directement, sans préambule ni
justification. 🔴 **C'est le seul fichier où un agent formule
librement** — partout ailleurs il transcrit ou range.

📌 **Quand il vient de l'invocation 2 de l'Analyste**, le fichier se
termine par la liste des questions écartées. 🔴 **Elle reste là** : le
fichier produit ne la porte pas.

🔴 **L'Analyste marque chaque entrée qu'il a intégrée** —
`[integrated: Bn]`, nommant le bloc où il a écrit. C'est ce qui permet
à l'émetteur de vérifier la clôture sans comparer deux versions du
fichier produit.

🔴 **La réponse est consignée aux deux endroits** : ici, sous forme
brute, et dans le bloc du fichier produit, intégrée en phrase
descriptive. ⚠️ **Ce n'est pas une duplication qui peut diverger** —
l'une nourrit l'autre, et le Convertisseur vérifie les deux.

🔴 **Il ne propose jamais de réponse.** Formuler une hypothèse plausible
reviendrait à trancher une décision produit.

📌 **Une question disparaît quand sa réponse est consignée dans le
fichier produit** — pas quand son champ *Réponse* est rempli.

---

### Les fichiers de blocage

🔴 **Un agent qui ne peut pas produire écrit un fichier**, il ne se
contente pas de le dire. Un message dans une réponse se perd ; un
fichier reste.

**Un nom par agent** — `blocked_analyste.md`, `blocked_convertisseur.md`,
`blocked_fusionneur.md`, `blocked_diagnostiqueur.md`,
`blocked_extracteur.md` — dans le dossier de la feature.

| Bloc | Contenu |
|---|---|
| Ce qui bloque | Le fait constaté, pas son interprétation |
| Où | Section, bloc, ou fichier concerné |
| Ce qu'il faudrait pour reprendre | Une décision, une correction en amont, une donnée absente |

⚠️ **Bloquer n'est pas signaler.** Un manque, une contradiction, une
question : ça part dans le fichier de questions et le cycle continue.
🔴 **On ne bloque que quand la production est impossible** — entrée
absente, fichier attendu introuvable, prémisse fausse qui invalide tout
le travail.

📌 **Ne jamais bloquer par excès de prudence.** Le doute se signale, il
ne bloque pas.

### Écrire la sortie même vide

🔴 **Un fichier de sortie s'écrit toujours, même sans contenu.** Un
fichier de questions vide dit *« rien à signaler »* ; son absence dit
*« l'agent n'a pas tourné »*. L'orchestrateur ne peut pas distinguer
les deux autrement.

---

### Document technique

**Produit par** le Convertisseur. **Lu par** le Cadreur.

| Bloc | Contenu |
|---|---|
| Préambule | Ce qui cadre — jamais découpé en lots |
| §1 à §12 | Le travail, par nature |

**Structuré par nature de travail, pas par écran ni par
fonctionnalité.** C'est ce qui permet au Cadreur de découper par
couche sans décider d'architecture — il ne lit pas le code, il ne peut
découper mécaniquement que si la spec sépare déjà les natures.

**Sections numérotées**, stables : elles servent d'ancres aux lots. Un
titre peut être renommé, un numéro non.

#### La structure interne

🔴 **Le préambule cadre, les sections décrivent le travail.** Un
contenu qui ne produit aucun lot n'est pas une section.

**Préambule — jamais découpé en lots**

| Contenu | Ce que le Cadreur en fait |
|---|---|
| Intention du domaine, en une phrase | Critère pour trancher un doute |
| Vocabulaire | Lève les ambiguïtés de lecture |
| Hors périmètre explicite | L'empêche de découper ce qui n'est pas demandé |
| Règles d'interface valables partout | Contraignent chaque lot d'écran, sans être un lot |
| Dépendances vers d'autres domaines | Alimentent les besoins déclarés |

**Sections — chacune produit des lots**

| Section | Contenu |
|---|---|
| §1 Model | Entités, champs, contraintes, relations |
| §2 Persistence | Stockage, index, migrations de schéma |
| §3 Calculation | Règles avec entrées et sortie, ordre de résolution entre règles |
| §4 Transition | Changements de statut, sur quel événement |
| §5 External source | Imports, API, capteurs, permissions, hors ligne |
| §6 Synchronisation | Entre appareils, avec un serveur, résolution de conflits |
| §7 Background work | Tâches planifiées, notifications, événements système |
| §8 Journey | Séquences d'écrans, branches, conditions de passage |
| §9 Screen | Contenu, états, interactions, navigation |
| §10 Text | Libellés, messages, langues |
| §11 Access | Qui voit et fait quoi, rôles, partage |
| §12 Lifecycle | Compte, export, suppression, consentements |

📌 **Une section vide est une information**, pas un oubli : elle dit au
Cadreur qu'il n'y a rien à faire de cette nature. On part de la liste
complète et on laisse vide, jamais l'inverse.

⚠️ **Sur une application entière**, une seule numérotation devient
ingérable — plusieurs domaines produiraient cinquante règles en §3. La
hiérarchie devient alors `§Activités.3`, `§Repas.3`.

#### Les règles d'écriture du document technique

**La prose**

🔴 **Présent de l'indicatif, comme dans les fichiers produit — mais la
précision prime sur la lisibilité.** Types, bornes, ordres explicites.

🔴 **Une règle qui laisse un cas indéterminé n'est pas écrite.** C'est
le critère : le Cadreur et le Détailleur doivent pouvoir en tirer un
lot sans rien décider.

⚠️ **Ici on nomme techniquement**, pas comme l'utilisateur voit les
choses — c'est l'inverse des fichiers produit.

**Une règle vit dans une seule section**

🔴 **Jamais de duplication entre sections — on référence.** Une règle
répétée à deux endroits diverge tôt ou tard.

🔴 **Et toute dépendance se déclare, même sans duplication.** Une
section qui a besoin d'une autre pour fonctionner la référence : la
donnée qu'elle lit, le calcul dont elle affiche le résultat, la clé de
texte qu'elle utilise, l'entité qu'elle persiste.

⚠️ **C'est ce qui donne l'ordre d'exécution.** Un écran qui affiche une
valeur calculée n'a aucune raison de recopier la règle — donc la seule
interdiction de duplication ne déclencherait rien, et le Cadreur
coderait l'écran avant son calcul.

📌 **Effet secondaire** : une section qui ne dépend de rien et dont
rien ne dépend est suspecte — isolée à tort, ou dépendances non
déclarées. Le Vérificateur le voit mécaniquement.

**La section propriétaire est celle qui répond à "d'où vient ce
comportement", pas "où il se voit".** Une règle de calcul appartient
aux calculs même si elle produit un affichage. Une contrainte de champ
appartient à la persistance même si elle se manifeste à la saisie.

**Syntaxe** : le numéro de section entre parenthèses, à l'endroit où la
règle est mentionnée — *« Créée par la règle de réconciliation
(§3.2). »* Une seule forme, pour que le Cadreur les extraie
mécaniquement.

**Cas éprouvés :**
- *Répartition calorique par repas* — vient d'une règle de calcul →
  §3. Le modèle et l'écran référencent.
- *Signaux passifs de capteurs* — viennent d'une source → §5. Le
  calcul de seuil et la transition référencent.
- *Bornes d'un champ* — viennent du modèle → §1. L'écran référence
  pour afficher l'erreur.
- *Décisions en attente* — l'entité vient de la règle qui la crée →
  §3. Le modèle référence.
- *Matrice d'interaction entre deux domaines* — appartient au domaine
  qui **l'applique**, jamais à ceux qu'elle concerne. Sinon les deux
  se référencent mutuellement et le Cadreur détecte un cycle.

📌 **Les références sont le mécanisme d'ordonnancement.** Un lot
d'affichage qui référence une section de calcul en dépend — c'est ce
que le Cadreur utilise pour ordonner, pas une commodité de lecture.

---

### Le rapport de fusion

**Produit par** le Fusionneur. **Lu par** le Product Owner.

| Bloc | Contenu |
|---|---|
| Sections nouvelles | Créées de toutes pièces |
| Sections fusionnées | Ce qui a été remplacé, ce qui a été conservé |
| Sections supprimées | S'il y en a |
| Sections inchangées | La liste — si une section attendue y figure, c'est un signal |

🔴 **Le Product Owner ne relit pas la fusion entière** : le rapport lui
dit où regarder. C'est le seul domaine où personne d'autre ne peut
juger.

📌 **Artefact ponctuel, daté, jamais modifié.** Un log au sens strict —
relu par aucun agent, il ne fait partie d'aucune chaîne.

**Prose** : une ligne par élément, pas de rédaction. Il est lu une fois
par le Product Owner, jamais parsé.

## Les agents en détail

### L'Analyste

**Une feature à la fois, de périmètre borné.** 🔴 Si le recueil produit
deux domaines sans lien — au sens du critère : *ce qu'il fait en une
phrase, sans « et »* — **il le signale** : ce sont deux features.

#### Deux invocations

🔴 **Une invocation par jeu d'entrées.** Des entrées différentes
signifient un contexte propre — chacune se charge de ce dont elle a
besoin, et de rien d'autre.

| # | Invocation | Entrées | Sortie |
|---|---|---|---|
| 1 | Structuration | Le fichier d'idées **ou** le dernier fichier de questions · le document global | Le fichier produit |
| 2 | Grille | Le fichier produit · la grille de cadrage · le document global · le dernier fichier de questions, **grepé seulement** | Le fichier de questions suivant |

🔴 **Aucune ne dialogue.** Le Product Owner écrit son fichier d'idées
hors ligne et remplit les champs *Réponse* à la main. L'Analyste
transcrit et structure — il ne converse jamais.

📌 **L'invocation 1 sert aussi les questions du Convertisseur et du
Fusionneur** — mêmes entrées, même travail.

#### Invocation 1 — Structuration

**Entrées** : le fichier d'idées du Product Owner — 🔴 **format
totalement libre**, c'est tout l'intérêt · le document global, pour
reprendre les titres existants. ⚠️ **Pas la grille** — elle n'intervient
qu'en invocation 2.

**Lecture du global** : l'index d'abord, puis les seules sections
utiles — voir "Comment le document global se lit". 📌 **Le Product
Owner peut nommer des sections** s'il sait déjà lesquelles sont
touchées ; sinon l'agent les identifie depuis l'index.

**Trois gestes, dans cet ordre, sur chaque passage du fichier
d'idées :**

**1. Décomposer.** 🔴 **Ce que le Product Owner dit est un flux, pas une
liste.** Une seule phrase peut contenir cinq sujets.

🔴 **Un sujet est un déclencheur et une sortie.** Lire le passage en
demandant : qu'est-ce qui déclenche ceci, et qu'est-ce que ça produit ?
**Deux déclencheurs, ou deux sorties, font deux sujets.**

⚠️ **Lire ce qui déclenche, pas le sujet grammatical.** Une phrase qui
s'ouvre sur ce que l'utilisateur voit peut être déclenchée par un
échec, un minuteur, ou un événement ailleurs.

**2. Chercher le titre dans l'index du global.** 🔴 **Un grep, jamais
une relecture.** Si le titre existe, il est repris ; sinon, il est
créé.

⚠️ **Ce grep porte sur tous les titres de l'index**, pas seulement sur
les sections chargées — c'est ce qui rattrape un conflit dans une
section qu'on n'avait pas prévu de toucher.

**3. Ranger.** Un bloc par sujet, sous le titre trouvé ou créé, **avec
la nature que sa sortie lui donne**.

🔴 **Le déclencheur sépare les sujets, la sortie nomme leur nature.** Un
bloc qui produit un affichage est `screen`, même déclenché par un
événement ; un bloc qui produit autre chose prend la nature de ce qu'il
produit.

🔴 **Une sortie différente sépare aussi, à déclencheur partagé.** Une
exception greffée sur une règle — *« sauf quand… »* — produit souvent
autre chose que la règle : c'est un bloc à part.

📌 **Numérotation** : attribuée à l'écriture, jamais réattribuée — le
fichier de questions désigne les blocs par leur numéro.

🔴 **Chaque bloc créé porte `NEW` sur sa ligne de titre.** L'invocation
2 le grepe pour savoir lesquels fermer ; l'invocation 1 efface tous les
marqueurs en premier geste, puis marque ce qu'elle crée.

**Quand il ne comprend pas** : 🔴 **il le signale sur place, jamais
parce qu'il détecte un trou** — la grille n'intervient pas ici.

**Le signalement vit dans le bloc concerné**, en fin de bloc :
`**Clarification needed:** <ce qui est flou, et ce qu'il a transcrit>`.
📌 **Il transcrit une lecture plutôt que de s'arrêter** — le bloc reste
exploitable.

**Cycle du marqueur** : l'invocation 2 le convertit en question avant
même de dérouler la grille, l'invocation 1 le retire une fois la
réponse intégrée, le Convertisseur vérifie qu'il n'en survit aucun.

**Quand le Product Owner se contredit** : la dernière version
s'applique, et **il signale ce qu'il a remplacé**. Jamais
silencieusement.

**Toujours en modification ciblée** : il ajoute le bloc concerné ou
modifie celui qui change, jamais le fichier entier. Les titres de
section et de bloc sont les ancres qui le permettent.

**Si le fichier d'idées couvre deux sujets sans lien** — au sens du
critère : *ce qu'il fait en une phrase, sans « et »* — 🔴 **il s'arrête
et écrit un fichier de blocage.** Deux features ne partagent pas un
fichier produit.

**Sortie** : le fichier produit, au format. ⚠️ Incomplet à ce stade, et
c'est normal.

#### Invocation 2 — Recherche des angles morts

**Entrées** : le fichier produit · `docs/process/GRILLE_CADRAGE_PRODUIT.md`
· le document global · le dernier fichier de questions, 🔴 **grepé,
jamais lu** — son regard sur le fichier produit doit rester agnostique.
⚠️ **Pas l'idée brute** — elle est déjà transcrite.

**Sortie** : le fichier de questions, terminé par la liste des
questions écartées :

    ## Questions set aside

    - Synchronisation: no block of that nature
    - Paid access: the feature touches no plan limit

📌 **Par catégorie quand toute la catégorie l'est**, par question
sinon. Une ligne chacune.

⚠️ **Elle ne touche pas au fichier produit** — les réponses arrivent en
invocation 1.

🔴 **Déclenchée par le Product Owner**, jamais de sa propre initiative.

**Ce qu'il fait** : applique les parties 1, 2 et 5 de la grille aux
blocs du fichier produit, puis la partie 4 une fois sur la feature.

🔴 **Quels blocs** : tous au premier tour, **puis seulement ceux qu'une
réponse a touchés ou créés.** Il les trouve par deux greps :
`^Block:` dans le dernier fichier de questions, et `NEW` dans le
fichier produit.

🔴 **Un grep, jamais un `Read`**, quelle que soit la taille du fichier
de questions : son regard sur le fichier produit doit rester agnostique,
et il cesse de l'être dès qu'une question entre dans son contexte.

📌 **`NEW` marque les blocs créés au tour précédent.** L'invocation 1
efface tous les marqueurs en premier geste, puis marque ce qu'elle
crée — d'un fichier d'idées, d'une scission, ou d'un sujet qu'aucun
bloc ne couvrait.

📌 **Un bloc qu'aucune réponse n'a touché a été fermé au tour
précédent.** Le refermer serait un filet sous la grille : si elle
laisse passer quelque chose, on corrige la grille, on ne la relance
pas.

🔴 **La grille génère les questions, elle ne les contient pas.** Il ne
balaie pas une liste — il ferme chaque bloc et note ce qui ne se ferme
pas.

| Issue | Ce qu'il en fait |
|---|---|
| Déjà répondue | Par le bloc lui-même, ou par le document global |
| Trou | Posée au Product Owner |
| Sans objet | Écartée — consignée en fin du fichier de questions |

⚠️ **Seules les questions du bloc 4 peuvent être sans objet.** Les
questions de fermeture s'appliquent toujours : un bloc a toujours un
déclencheur, un effet et un état éteint, même si la réponse est
« rien ».

**Comment il juge « sans objet »** : la question ne s'applique que si
la feature touche ce qu'elle interroge. Une question de synchronisation
est sans objet si aucun bloc ne porte cette nature.

📌 **Le tri se fait donc sur les natures présentes dans le fichier**,
pas sur une impression — c'est vérifiable.

🔴 **En cas de doute, il pose la question plutôt que d'écarter.** Une
nature peut être absente parce qu'elle a été oubliée au recueil.

**Comment il pose** : par groupes cohérents, un bloc de grille à la
fois. Ni une par une, ni toutes d'un coup.

📌 **La grille est un outil de contrôle, pas un questionnaire.** Il
arrive avec une liste de trous identifiés, jamais avec 150 questions.

⚠️ **Itératif** : une réponse peut ouvrir un nouveau bloc de questions.
Décider qu'une feature stocke des données ouvre tout le cycle de vie.

**Critère d'arrêt de la boucle 2↔3** : toute question retenue a sa
réponse dans le fichier produit — qu'elle vienne du recueil ou d'une
question posée. 📌 **Vérifiable sur le fichier**, pas un jugement.

#### Invocation 3 — Intégration des réponses

*Déclenchée par un fichier de questions — de l'invocation 2, du
Convertisseur ou du Fusionneur.*

**Entrées** : le fichier produit · le fichier de questions. ⚠️ **Ni la
grille, ni le document global** — il ne fait que répondre.

📌 **Le Product Owner a rempli les champs *Réponse* à la main.**
L'Analyste ne tranche rien — il transcrit.

**Ce qu'il fait** : pour chaque réponse, la transformer en phrase
descriptive et 🔴 **l'intégrer au bloc concerné**, via l'identifiant.

⚠️ **Si une réponse est ambiguë**, il ne peut pas reprendre le Product
Owner en cours : il ajoute une entrée au fichier de questions, champ
*Réponse* vide.

**Sorties** : le fichier produit à jour · le fichier de questions, ses
entrées traitées.

#### Cahier des charges

📌 **Entre deux sessions, il relit le fichier produit.** C'est son
état, pas sa mémoire — un cycle peut s'étaler sur plusieurs jours.

**Entrées** — voir "Deux invocations" : chaque invocation charge son
propre jeu. ⚠️ **Jamais** le code, `CURRENT_TECHNICAL_STATE.md` ni le
document technique.

**Sortie** — le fichier produit de la fonctionnalité.

**Ce qu'il ne fait jamais**
- 🔴 Dérouler la grille comme un questionnaire
- 🔴 Trancher une décision produit à la place du Product Owner
- 🔴 Mettre deux natures sur un bloc, ou deux features dans un fichier
- Écrire dans le document global — c'est le Fusionneur

---

### Le Convertisseur

#### La grille de fermeture technique

**Il applique `docs/process/GRILLE_FERMETURE_TECHNIQUE.md`** — huit
fermetures en deux parties. 🔴 **La grille porte les tests, l'agent
porte les gestes.**

| Partie | Quand | Ce qu'elle ferme |
|---|---|---|
| 1 | En fermant le produit | Nature · cohérence entre blocs |
| 2 | En produisant | Traçabilité · unicité · accord entre entrées · liens déclarés · ressources · complétude |

**Une fermeture qui échoue est un signalement.**

🔴 **Ce qui n'en est pas un** : un bloc laconique mais complet (*« la
fenêtre vaut 3 heures »* suffit), une précision que la grille de
cadrage a déjà balayée, un bloc portant deux sujets — l'amont s'en
charge — et **jamais un jugement de pertinence produit**.

📌 **Il ne pose jamais une question produit.** Il ne demande pas où va
un bouton — il constate qu'une destination nommée n'a pas de
description.

📌 **Plus un marqueur de clarification survivant** : une
`**Clarification needed:**` restée dans le fichier produit est une
question sans réponse.

#### Le cycle de conversion

**Première invocation — fermeture**

Elle applique la partie 1 de la grille à chaque bloc et produit **un
seul fichier** : le fichier de questions, chaque question portant
l'identifiant du bloc qu'elle bloque.

🔴 **Elle n'écrit aucun contenu technique.** Elle ferme, et signale ce
qui ne ferme pas.

🔴 **Il ne tranche jamais.** Décision produit absente, précision
manquante, contradiction interne : il signale, il ne comble pas. *Il
n'est pas le filet de la chaîne amont.*

🔴 **Un problème ne bloque jamais le reste.** L'élément est marqué, le
reclassement continue jusqu'au bout. *Un signalement par problème
produirait un aller-retour par problème — et les réponses
s'influencent : trancher les bornes d'une donnée change ce qu'on répond
sur une autre.*

**Le ping-pong**

Le fichier de questions part au Product Owner, qui remplit les champs
*Réponse* à la main. L'Analyste les intègre ensuite aux blocs du
fichier produit — invocation 1.

🔴 **Une question dont la réponse est consignée ne se repose jamais.**
Le critère d'arrêt est le fichier de questions entièrement répondu, pas
un nombre d'itérations.

⚠️ **Si une réponse fait apparaître un nouveau problème**, il rejoint
le fichier de questions au tour suivant. C'est normal, pas un échec.

📌 **Ce qui remonte ici aurait dû être tranché en amont.** Un
signalement est le signe que la grille de cadrage n'a pas posé la
question, ou que le Product Owner n'y a pas répondu — pas que le
Convertisseur est trop strict.

**Première invocation, en terminant** : 🔴 **elle supprime le document
technique s'il existe.** Le fichier produit a bougé depuis qu'il a été
écrit, et le laisser enverrait la seconde invocation en mise à jour
ciblée sur un document qui ne correspond plus.

**Seconde invocation — production**

🔴 **Elle regarde d'abord si le document technique existe.**

| État | Ce qu'elle fait |
|---|---|
| Absent | Production complète |
| Présent | 🔴 **Mise à jour ciblée** — grep `<<ASSUMED`, remplacer chaque marque par sa réponse, ne toucher à rien d'autre |

**En production complète**, elle reprend le fichier produit à jour, qui
porte les réponses, et le lit en entier.

🔴 **Ici elle reformule** — c'est sa valeur. *« La donnée la plus
fiable gagne »* devient une règle exécutable : quel ordre de priorité,
quelle comparaison. ⚠️ **Deux régimes, deux invocations** : le
reclassement range sans toucher au contenu, la production traduit en
termes techniques.

🔴 **Elle ne décide rien de neuf.** Elle rend explicite ce que le bloc
dit implicitement — la fermeture *Traçabilité* trace la limite.

**Ce qu'une question coûte** :

| Sans cette information | Ce qu'elle fait |
|---|---|
| La règle n'existe pas | Elle demande, **n'écrit aucun document**, et supprime celui qui existe |
| La règle s'écrit en supposant | Elle demande, **et produit** — la supposition marquée sur place |

🔴 **La marque porte la question qui la lèvera** :
`<<ASSUMED questions-convertisseur-04 Q2: …>>`. ⚠️ **Le Cadreur bloque
sur une seule** — une règle provisoire ne se découpe pas.

**Le préambule se remplit avant les sections**, entièrement repris du
fichier produit :

| Bloc du préambule | D'où il vient |
|---|---|
| Intention, vocabulaire, hors périmètre | Les sections de même objet du fichier produit |
| Règles transversales | Les blocs déclarés valables partout |
| Dépendances | Les références marquées *existantes* |

🔴 **Une règle transversale contraint sans rien produire.** Un jeu de
valeurs que le code doit écrire quelque part **produit**, même si tout
le document le référence.

📌 **Le test** : si personne ne l'écrit, est-ce que le code manque
quelque chose ? **Oui → c'est une entrée numérotée**, pas un bloc de
préambule. Les tokens d'un thème, un catalogue de formats, une table de
seuils répondent oui.

⚠️ **Rien n'y est déduit** — tout est transcrit.

**Ce qui devient une entrée numérotée** : 🔴 **une règle ou une
table.** Une règle a des entrées et une sortie ; une table est un jeu
de valeurs que le code doit écrire quelque part.

> **Une règle qu'on peut couper en deux règles complètes fait deux
> entrées. Une qu'on ne peut pas couper sans laisser un cas ouvert
> reste une.**

⚠️ **Une entrée n'est pas un bloc produit.** Le fichier produit sépare
par déclencheur ; le document technique sépare par ce qui reste complet
seul. **Un bloc peut donner deux entrées, deux blocs une seule.**

🔴 **Il ne groupe pas en unités de travail.** Le Cadreur le fait, avec
le document d'état sous les yeux. **Un groupement fait ici déciderait
pour lui, à l'aveugle.**

**Ordre de remplissage** : les sections dans l'ordre §1 → §12 ; à
l'intérieur, les entrées suivent l'ordre des blocs dont elles viennent.
📌 **Aucun tri par jugement** — les citations du Cadreur casseraient
d'une exécution à l'autre.

🔴 **Elle signale toute contradiction que le reclassement aurait
introduite.** C'est sa raison d'être — un contexte frais voit ce que le
premier passage ne pouvait pas voir. Un signalement à ce stade renvoie
au ping-pong.

---

#### Cahier des charges

**Entrées**
- **Les deux invocations** : `GRILLE_FERMETURE_TECHNIQUE.md`
- **Première invocation** : le fichier produit de la fonctionnalité
- **Seconde invocation** : le fichier produit à jour, qui porte les
  réponses. **Ou le document technique seul**, sur une mise à jour
  ciblée

⚠️ **Rien d'autre** : ni le code, ni `CURRENT_TECHNICAL_STATE.md`
*(c'est le Cadreur qui le lit)*, ni la grille de cadrage, ni le
document produit global *(c'est l'Analyste et le Fusionneur)*.

🔴 **Jamais `idees.md`**, jamais un fichier de questions — sauf les
entrées qu'une marque `<<ASSUMED` nomme, sur une mise à jour ciblée.

**Actions — première invocation**
- Lire le fichier produit en entier, une fois — jamais partiellement :
  une règle de calcul peut être décrite dans une section d'écran, et
  inversement
- Lancer la partie 1 de la grille de fermeture sur chaque bloc — une
  fermeture qui échoue est signalée, le bloc n'est pas classé
- Reclasser les autres selon leur nature
- Supprimer le document technique s'il existe

**Actions — seconde invocation**
- 🔴 **Regarder d'abord si le document technique existe** — présent :
  mise à jour ciblée sur les `<<ASSUMED` et rien d'autre
- Remplir le préambule, repris du fichier produit
- Remplir les sections dans l'ordre §1 → §12 ; à l'intérieur, les
  entrées dans l'ordre des blocs dont elles viennent
- 🔴 **Lancer la partie 2 de la grille une fois toutes les sections
  remplies** — pas en écrivant : une section grandit, et ce qu'elle
  consomme n'apparaît qu'une fois debout

**Sorties — première invocation**

| Fichier | Contenu |
|---|---|
| Fichier de questions | Une question par problème, portant l'identifiant de l'élément qu'elle bloque |

**Sorties — seconde invocation** : le document technique, **et un
fichier de questions dans tous les cas** — même vide. 📌 **Son absence
se lirait comme *« cette invocation n'a pas tourné »*.**

| Bloc | Contenu |
|---|---|
| Préambule | Intention, vocabulaire, hors périmètre, règles transversales, dépendances |
| §1 à §12 | Le travail, par nature — sections vides incluses |

**Structure** — sections numérotées, jamais seulement titrées : elles
servent d'ancres. Une section sans contenu est écrite vide, pas omise.

**Ce qu'il ne fait jamais**
- 🔴 Trancher une décision produit, même triviale
- 🔴 Écrire dans le document produit global
- 🔴 Décider qu'un service, une table ou un écran est nécessaire — le
  découpage appartient au Cadreur
- 🔴 Dupliquer une règle entre deux sections
- Lire le code

📌 **Les dépendances du préambule viennent de l'Analyste, pas de lui.**
Écrire *"ce domaine alimente le calcul de dépense énergétique totale"*
suppose de savoir que ce calcul existe ailleurs — seul l'Analyste a le
document produit global sous les yeux. La grille pose
la question ; le Convertisseur transcrit la réponse.

---

### Le Fusionneur

**Une révision modifie et remplace, elle n'ajoute jamais à côté.**
L'insertion reste le cas normal pour ce qui est nouveau.

#### Quand il intervient

**En dernier**, après que la conversion a abouti sans signalement :

`Analyste → fichier produit → conversion → si le fichier de questions
est entièrement répondu → fusion`

⚠️ **Sinon le global décrirait un état que la spec ne produira
jamais** — une conversion qui bloque laisserait la documentation en
avance sur la réalité.

#### Le cycle du Fusionneur

**Première invocation — comparer et questionner.** Il localise,
compare, et produit **deux fichiers** : le **plan de fusion** — pour
chaque phrase, remplacement, rien ou insertion — et le **fichier de
questions**. 🔴 **Il n'écrit rien dans le global à ce stade.**

📌 **Le plan de fusion est ce que la seconde invocation applique** —
sans lui, la comparaison serait refaite de zéro.

**Le ping-pong** — le fichier part à l'Analyste, qui l'intègre une fois
répondu par le Product Owner. Même canal, même mécanique que pour le
Convertisseur.

**Seconde invocation — appliquer**, une fois le fichier entièrement
répondu. Puis le rapport. 📌 **Sans question, il enchaîne immédiatement.**

#### Comment il localise et compare

**Phrase par phrase, dans le périmètre d'un bloc**

🔴 **L'unité de fusion est la phrase descriptive, jamais le bloc
entier.** Une refonte remplace la structure d'une entrée, mais
certaines règles survivent — un point d'entrée, un accès depuis un
autre écran, une règle de portée. Remplacer en bloc les perd.

**Trois niveaux de localisation :**

| Niveau | Comment |
|---|---|
| Section | Par son titre, repris du global |
| Bloc | Par son titre, dans la section |
| Phrase | Comparée au bloc existant, quelques lignes |

📌 **Le bloc borne la comparaison.** Chercher une règle dans dix lignes
n'est pas la chercher dans un document entier — c'est ce qui rend la
fusion fiable, et c'est une seconde raison d'être de la règle « un
bloc, un sujet ».

**Pour chaque phrase du bloc nouveau, contre le bloc existant :**

| Cas | Action |
|---|---|
| Elle décrit la même chose, autrement | Remplacement |
| Elle décrit la même chose, à l'identique | Rien |
| Aucune correspondance | Insertion |

⚠️ **C'est un travail de compréhension, pas de comparaison textuelle.**
*« Trois éléments maximum »* et *« le nombre ne dépasse pas cinq »*
décrivent la même règle avec des mots différents — c'est un
remplacement, pas une insertion.

**Transposer au présent descriptif** — voir "Les règles d'écriture des
fichiers produit"

🔴 **Toute marque de changement disparaît à l'insertion.** Le fichier
produit dit ce qui change — *« un nouveau bouton en bas de la page »*.
Le global dit ce qui est — *« un bouton en bas de la page »*.

⚠️ « Nouveau », « désormais », « au lieu de », « on ajoute » : ce
vocabulaire sert à coder, pas à décrire un état. Sans cette
transposition, un bouton resterait « nouveau » indéfiniment.

**Quand il demande**

🔴 **Il applique sans question dans tous les cas ci-dessus.** La
décision d'ajouter ou de réviser a été prise à l'invocation 1 de
l'Analyste.

**Un seul cas appelle une question** : une règle du bloc existant sans
aucune correspondance dans le bloc nouveau. ⚠️ **Le silence ne vaut pas
suppression** — elle survit peut-être, ou n'a pas été discutée. Il
demande plutôt que d'interpréter.

**Où il écrit**

**Modification ciblée, section par section.** 🔴 Jamais de réécriture
intégrale du global : les titres sont les ancres qui le permettent.

**Une section nouvelle se place dans son domaine**, à la suite des
sections de même nature — les écrans avec les écrans. ⚠️ **Si le
domaine n'existe pas**, il en crée un au niveau domaines.

#### Cahier des charges

**Entrées**
- **Première invocation** : le fichier produit final · le document
  global
- **Seconde invocation** : le plan de fusion · son fichier de
  questions, répondu · le document global

⚠️ **Rien d'autre** : ni le document technique, ni le code.

**Actions — première invocation**
- Localiser : section par son titre, puis bloc par son titre
- Dans un bloc localisé, phrase par phrase : remplacement, rien, ou
  insertion
- 🔴 **Ne rien écrire dans le global** — produire le fichier de
  questions pour toute règle existante sans correspondance

**Actions — seconde invocation**, le fichier de questions répondu
- Appliquer les décisions, en modification ciblée
- Transposer au présent descriptif — retirer toute marque de changement
- Écrire le rapport, **après application**

**Sorties**
- **Première invocation** : le plan de fusion · le fichier de questions
- **Seconde invocation** : le document global à jour · le rapport de
  fusion, daté

**Ce qu'il ne fait jamais**
- 🔴 Décider ce qui se fusionne — la décision est dans le fichier
  produit
- 🔴 Supprimer une règle par omission
- 🔴 Remplacer un bloc entier quand seules quelques phrases changent
- 🔴 Conserver le vocabulaire du changement dans le global
- 🔴 Reprendre le numéro d'un bloc ou sa marque `NEW` — dans le global,
  un bloc n'a que son titre
- Toucher au document technique

### Le Diagnostiqueur

*Cycle bug fix uniquement. Une seule invocation.*

**Entrées** : le fichier d'écarts · le document global. ⚠️ **Pas le
code** — il constate un écart déclaré, il ne l'explique pas. C'est
l'aval qui investiguera.

**Ce qu'il fait**, bloc par bloc :

| Cas | Action |
|---|---|
| Le titre existe et décrit le comportement attendu | **Écart confirmé** — il produit un bloc au format produit portant **ce que le global exige**, pas ce qui a été observé |
| Le titre existe mais décrit autre chose | **Écarté** — révision produit, pas correction |
| Le titre n'existe pas | **Écarté** — le cas n'a jamais été cadré |

📌 **Sa sortie est riche même si le fichier d'écarts est pauvre** : il
recopie la règle complète du global, pas le constat — donc au format et
dans la prose du global — voir "Les règles d'écriture des fichiers
produit".

#### Cahier des charges

**Entrées** — le fichier d'écarts · le document global. ⚠️ **Rien
d'autre** : ni le code, ni `CURRENT_TECHNICAL_STATE.md`, ni le document
technique.

**Sorties** — `desc-produit.md` avec les seuls écarts confirmés · la
liste des écarts écartés, avec leur raison.

🔴 **Chaque bloc porte `NEW` sur sa ligne de titre** — tous sont neufs,
et la passe de grille grepe ce marqueur.

**Ce qu'il ne fait jamais**
- 🔴 Expliquer un écart — c'est l'aval qui investigue
- 🔴 Reprendre le constat observé plutôt que la règle du global
- 🔴 Écrire dans le document global
- 🔴 Traiter un écart dont le titre n'existe pas au global

---

### L'Extracteur

*Reprise d'une application existante sans document global. Une
invocation par domaine, plus une passe application et une passe
finale.*

**Entrées** : le code du domaine · les fichiers de langue ·
`lib/app/router.dart`, la carte route↔écran. ⚠️ **Ni les documents
produit existants** — il décrirait des décisions non implémentées — **ni
`CURRENT_TECHNICAL_STATE.md`**, qui est un inventaire technique.

**Sortie** : des sections au format du global — blocs, natures, titres.
🔴 **Prose et création de titres** : voir "Les règles d'écriture des
fichiers produit".

#### Ce qu'il décrit

| Objet | Ce qu'il en tire |
|---|---|
| Écran | Ce qui s'affiche, les libellés depuis les fichiers de langue, les conditions, ce que fait chaque action |
| Service | La règle, ses entrées, sa sortie, ses valeurs |
| Entité | Ses champs, leurs types et bornes |
| Source externe | Ce qui est lu, avec quelles priorités |

**Niveau de détail** : 🔴 **ce qui vient du thème va dans la section
thème, le reste est décrit.** Une couleur nommée depuis le thème n'est
pas une décision d'écran ; une valeur écrite en dur dans le widget en
est une.

⚠️ **Une valeur en dur qui devrait venir du thème** est décrite quand
même — le global décrit l'actuel — et signalée.

#### Les passes

**Une passe par domaine.** 📌 Si le découpage du code ne suit pas les
domaines produit, le Product Owner indique quels dossiers correspondent
à quel domaine.

**Une passe application**, séparée — authentification, thème, langues,
rétention : ce que le code porte sans appartenir à un domaine. 📌 **Elle
se range en tête du fichier**, avant les domaines.

**Ordre des sections dans un domaine** : celui de leur apparition dans
le code. ⚠️ Sans consigne, deux passes sur le même domaine produiraient
deux ordres.

**Une passe finale de recâblage.** 🔴 Une référence vers un domaine pas
encore extrait porte une balise `<<REF:name>>` ; la passe finale les
résout toutes.

#### Ce qu'il signale

🔴 **Tout signalement porte une balise greppable**, pour être récupéré
par script :

| Balise | Sens |
|---|---|
| `<<REF:name>>` | Référence vers un domaine pas encore extrait — résolue à la passe finale |
| `<<ORPHAN>>` | Écran ou service qui n'apparaît dans aucune route ni appel |
| `<<HARD_STYLE>>` | Valeur de style en dur qui devrait venir du thème |
| `<<HARD_TEXT>>` | Texte affiché en dur au lieu des fichiers de langue |
| `<<DOUBT>>` | Ce qu'il n'a pas su interpréter |

📌 **Il ne tranche aucun de ces cas** — il décrit et signale.

⚠️ **Les trois du milieu ne sont pas des décisions produit**, ce sont
des anomalies techniques croisées en lisant. Le Product Owner les
récupère par script et les envoie en aval — elles ne passent pas par le
cycle bug fix.

#### Ce qu'il ne fait jamais

- 🔴 Justifier — le global décrit, il n'explique pas
- 🔴 Corriger ce qui lui semble anormal : **le comportement observé est
  l'état actuel**, le décrire tel quel est exactement ce qu'on veut —
  il peut le signaler par balise, jamais le réécrire
- 🔴 Décrire ce qui n'est pas implémenté
- 🔴 Nommer un fichier, une classe, une méthode — c'est
  `CURRENT_TECHNICAL_STATE.md`

---

## Mode opératoire

**Les cinq agents vivent dans `.claude/agents/`**, comme ceux de
l'aval.

### Les quatre points d'entrée

| Cas | Comment on entre |
|---|---|
| **Feature sur application existante** | Le cas nominal — cycle complet, `/1_structure` à `/6_fusionne` |
| **Application neuve** | `/socle` crée l'arborescence et un global vide. Puis **un cycle par domaine** — le premier remplit le global, les suivants le voient comme une application existante |
| **Correction d'un défaut** | 🔴 **Deux cas à distinguer avant d'entrer** — voir ci-dessous |
| **Reprise d'une application existante** | Aucun global — `/extrait` le construit depuis le code, un domaine à la fois, puis les cycles normaux s'appliquent |

**Découper une application neuve en domaines** : le critère est le même
que partout — *ce que le domaine fait, en une phrase, sans « et »*.
⚠️ **Pas de liste type** : ranger un produit dans des cases génériques
le déformerait. Les découpages fréquents — authentification et compte,
réglages, un domaine par objet métier, tableau de bord — sont des
exemples, pas un modèle.

**Correction d'un défaut** — un cycle à part, avec son propre agent.

**Le Product Owner écrit un fichier d'écarts** — voir "Le fichier
d'écarts" pour sa structure.

**La chaîne** : `/diagnostique` → `/3_reclasse` → *(`/1_structure` si
questions)* → `/4_convertit` → chaîne aval.

🔴 **Le Fusionneur ne tourne pas** — le global est la référence, il ne
change pas. Ni la grille, ni les deux invocations de l'Analyste : il
n'y a aucune décision produit à obtenir.

⚠️ **L'invocation 1 de l'Analyste reste dans la boucle** : si le
Convertisseur pose des questions, c'est elle qui intègre les réponses
au `desc-produit.md`.

---

### Une commande par invocation

🔴 **Aucune commande n'en appelle une autre.** Le Product Owner
déclenche chacune à la main — il n'y a jamais deux agents enchaînés
sans son intervention.

⚠️ **Une exception : `/extrait`.** L'extraction ne prend aucune
décision produit — l'Extracteur décrit et balise, rien n'attend
d'arbitrage entre deux domaines. La commande déclenche **un mode de
`.claude/CLAUDE.md`** qui enchaîne : passe application, puis les
domaines dans l'ordre, puis la passe de recâblage.

📌 **Séquentiel, pas parallèle** : chaque domaine voit les précédents,
donc balise moins. En parallèle, aucun ne verrait les autres et la
passe de recâblage deviendrait énorme.

**Ce que le Product Owner fournit** : la liste ordonnée des domaines
avec leurs dossiers de code. L'orchestrateur ne la devine pas.

| Commande | Agent | Ce qu'elle produit |
|---|---|---|
| `/socle` | — *(script)* | L'arborescence et un global vide, pour une application neuve |
| `/extrait` | Extracteur, orchestré | Le global entier, depuis le code — reprise d'une application existante |
| `/diagnostique` | Diagnostiqueur | `desc-produit.md` — cycle bug fix uniquement |
| `/1_structure` | Analyste | `desc-produit.md` — depuis `idees.md`, ou depuis le dernier fichier de questions |
| `/2_grille` | Analyste | `questions-analyste-NN.md` |
| `/3_reclasse` | Convertisseur | `questions-convertisseur-NN.md` |
| `/4_convertit` | Convertisseur | `spec-technique.md` |
| `/5_compare` | Fusionneur | `plan-fusion.md`, `questions-fusionneur-NN.md` |
| `/6_fusionne` | Fusionneur | global à jour, `rapport-fusion.md` |

📌 **La numérotation suit la chaîne**, pas les agents — elle donne
l'ordre d'exécution.

**Les commandes qui bouclent** — `/1_structure` et `/2_grille` — se
relancent simplement tant qu'il reste des questions. Idem pour
`/5_compare` et `/1_structure`.

### Modèles

🔴 **Tout en Sonnet au démarrage**, sans exception — aucune mesure ne
justifie Opus aujourd'hui.

⚠️ **Trois phases sont les candidates si la qualité ne suit pas** :

| Phase | Ce qu'elle demande |
|---|---|
| Analyste, invocation 1 | Décomposer un flux libre en sujets et poser une nature — une mauvaise décomposition se propage jusqu'au code |
| Convertisseur, invocation 2 | Reformuler une règle produit en règle exécutable |
| Fusionneur, invocation 1 | Reconnaître que deux formulations décrivent la même règle |

📌 **Les autres phases sont mécaniques** — trier sur des natures
présentes, transcrire, appliquer un plan, vérifier trois points.

### Faire grandir la grille

📌 **La grille n'énumère pas les cas.** Ce qu'elle ne génère pas depuis
les blocs présents, elle ne le demande pas. Elle ne grandit jamais
d'imagination — seulement quand une passe réelle a laissé passer
quelque chose.

| Partie | Ce qui l'a fait grandir |
|---|---|
| **1 — fermer le bloc** | Le voisinage. *Une chaîne remonte ce qui consomme et descend ce qui produit ; un voisin ne fait ni l'un ni l'autre — aucune fermeture ne l'atteignait.* |
| **2 — rendre le bloc codable** | L'exhaustivité. *Une règle découpant un intervalle a laissé ses bornes indéfinies pendant quatre passes.* |
| **4 — ce qu'aucune chaîne ne révèle** | Un trou constaté en aval — un `blocked.md`, une question produit remontée à l'implémentation |
| **5 — test de clôture** | Le nom défini sur place. *Un texte affiché, une dimension et un élément existant ont traversé la chaîne sans jamais être définis.* |

🔴 **La partie 3 n'a jamais grandi** — les éléments sans déclencheur
sont rares et leur cadrage tient.

⚠️ **Quatre points de croissance sur un seul cycle.** Le prochain doit
en produire moins ; s'il en produit autant, le test de clôture n'est
pas le bon instrument.

### Où vivent les fichiers

**Un dossier par feature** : `docs/features/<nom>/`, créé par le
Product Owner, qui y dépose son fichier d'idées.

    idees.md · ecarts-constates.md · desc-produit.md
    plan-fusion.md · spec-technique.md
    rapport-fusion.md

    questions-<agent>-01.md…      à la racine, le cycle en cours
    questions/<agent>/            les cycles clos, un dossier par agent

🔴 **Les fichiers de questions portent le nom de leur émetteur** —
`questions-analyste-01.md`, `questions-convertisseur-01.md`,
`questions-fusionneur-01.md`.

**Chaque agent, avant d'écrire :** il range dans `questions/<agent>/`
tout fichier de la racine dont le préfixe n'est pas le sien, cherche
son dernier — à la racine, sinon dans son propre dossier — et écrit à
la racine au numéro suivant.

⚠️ **Un agent ne lit jamais un fichier qui n'est pas le sien.**

📌 **Le process aval travaille dans le même dossier**, sous
`code/` — voir `PROCESS_AVAL.md`.

🔴 **Noms fixes** — c'est ce qui permet aux commandes de n'avoir qu'un
seul argument : le nom du dossier.

    /1_structure partage-familial

**Le document produit global** : `docs/PRODUIT_GLOBAL.md`, à la racine
— permanent, il n'appartient à aucune feature.

## Questions ouvertes

*Des points que l'usage n'a pas encore tranchés.*

🟡 **Stabilité de l'identifiant d'entrée** dans le document global.
Moins critique depuis que la fusion se décide à la structuration —
c'est le Product Owner qui désigne l'entrée à réviser, pas un agent qui
la retrouve.

🟡 **Tenue de la règle de séquencement** — que se passe-t-il si une
révision produit est nécessaire pendant qu'un cycle aval tourne ?
