# Cockpit de la chaîne

Une page locale pour répondre aux questions et aux fichiers de blocage,
voir la prochaine étape, et lancer les commandes — sans ouvrir les
fichiers à la main.

## Installer

Une fois, avec Python 3.12 :

    cd tools\cockpit
    pip install -r requirements.txt

## Lancer

Double-cliquer sur **`lancer.bat`** (ou son raccourci sur le bureau). Le
serveur démarre sans fenêtre et le navigateur s'ouvre sur
`http://127.0.0.1:8765/` ; s'il tourne déjà, seul le navigateur s'ouvre.
Ce qu'il écrivait dans la fenêtre noire va dans `logs/server.log`.

- **Fermer la page** (l'onglet ou le navigateur) n'arrête rien : un run continue.
- **La rouvrir** (le raccourci, ou l'adresse) la remet où en sont les choses : le run, son flux depuis le début, l'agent qui travaille, une autorisation qui attend.
- **Arrêter le cockpit** : Paramètres → « Arrêter le cockpit » ; si un run tourne, il demande d'abord, et le run est arrêté.

Dans une console, pour voir ce qu'il écrit : `python server.py --ouvrir`
(`Ctrl+C` l'arrête).

## Au démarrage

- **Les applications** (1.6) : le cockpit garde la liste des applications
  sur lesquelles vous travaillez, et l'une d'elles est **active** : tous
  les écrans travaillent sur elle. Au lancement, l'application active
  s'ouvre sur sa dernière feature. Sans application active, ou sans
  feature ouverte, l'écran « Applications » s'affiche.
- **Feature** : une feature de `docs/features/` de l'application active.
  Ses corrections `bugfix-NN/` sont sous « Correction », plus ici.
- **Dossiers ignorés** (1.5.1) : ceux d'une ancienne chaîne, que rien
  ne doit plus montrer — par application, dans `config.json`
  (`"ignored"`) ; une nouvelle application n'en a aucun. Un dossier ignoré et ses `bugfix-NN/` ne
  paraissent nulle part : ni dans la liste des features, ni sous
  « Correction », ni dans le scan, les Statistiques ou le Code.
  Paramètres → Dossiers montre la liste ; une case par dossier la
  modifie.
- **Récents** : les dernières paires, sous Paramètres → Dossiers.
  « Changer d'application » mène à l'écran « Applications ».

## Les écrans

**Applications** (1.6) — une ligne par application : son nom et son
dossier ; sa chaîne (**à jour**, **en retard**, **modifiée sur place**,
**absente**) ; sa feature et l'étape que le relevé du dossier y propose ;
ce qui vous y attend, en nombre de questions et de blocages ; son dernier
run (la commande, quand, comment il a fini) ; le nombre de fichiers non
commités dans son dossier — pour information, le cockpit n'y touche
jamais. Sur chaque ligne : « Ouvrir » (elle devient l'active),
« Renommer », « Retirer de la liste » (il demande d'abord ; le dossier
n'est pas touché, seule la liste change), et, quand sa chaîne n'est pas à
jour, « Installer » ou « Mettre à jour la chaîne ». En haut :
- **« Ajouter une application »** : la fenêtre de choix de Windows, ou le
  chemin collé. Il faut la racine d'un dépôt git ; un autre dossier est
  refusé, et la page dit pourquoi. Ajouter n'écrit rien dans le dossier.
  Un dépôt où la chaîne n'est pas encore installée s'ajoute aussi : il
  montre « chaîne absente », et sa ligne l'installe. L'ouvrir sur une
  feature demande `docs/features/`.
- **« Tout mettre à jour »** : installe la chaîne dans chaque application
  **en retard**, l'une après l'autre — le commit `chain: <id> <date>` et
  le push dans chacune, les mêmes refus qu'une à une. Seules les
  applications « en retard » sont mises à jour d'un coup : une chaîne
  « modifiée sur place » ou « absente » est listée avec sa raison et un
  bouton qui ouvre sa propre installation, laquelle demande avant de
  remplacer quoi que ce soit. Une application où une commande tourne est
  laissée, et c'est dit. À la fin, une ligne par application : mise à jour
  (avec le commit), laissée (pourquoi), en échec (l'erreur).

**La barre du haut** montre le nom de l'application active ; un clic
ouvre la liste courte pour en changer, sans passer par l'écran.

**Une commande à la fois** — toutes applications confondues : pendant
qu'une commande tourne dans une application, rien ne se lance dans aucune
autre. La barre du haut dit dans quelle application elle tourne, avec
« Arrêter » ; ailleurs, un bandeau le dit sur tous les écrans, et ses
demandes d'autorisation y arrivent aussi. Le tableau de bord d'une autre
application ne la montre pas comme la sienne.

**Le menu** — le bouton à trois traits, à gauche de la barre du haut,
ferme et rouvre le menu de côté ; l'espace de travail prend alors toute la
largeur. Le cockpit s'en souvient. Menu fermé, un point sur le bouton
signale qu'il y a quelque chose à répondre ou qu'une commande tourne.

**Où on en est ?** — le bouton, en haut de l'écran « Chaîne », relit le
dossier et revérifie la dernière ligne `Next:`. Le cockpit le fait aussi tout seul à
l'ouverture, après chaque run et après chaque enregistrement de réponses.

**Tableau de bord — Prochaine étape** — d'où elle vient est écrit à côté :
- **« dit par la chaîne »** : la ligne `Next:` du dernier relais. Juste
  après un run, elle est prise telle quelle ; ensuite, elle est vérifiée
  contre les fichiers.
- **« déduite du dossier »** : la première étape de la chaîne qui n'est
  pas faite, d'après les fichiers. Quand les fichiers contredisent la
  ligne `Next:`, elle est écartée et la page le dit : « Le dernier relais
  disait … ; les fichiers disent … » — et l'écart est écrit au journal
  du run.
« Pourquoi ? » montre la règle (`scan_rules.md`), les fichiers et les
lignes de la commande qui ont donné l'état.

**Chaîne** — la chaîne principale, une étape par commande, son état en
couleur et en mot : faite · t'attend · en cours · bloquée · à faire ·
inconnu. La prochaine étape ressort ; un clic sur « Lancer » la lance avec
la feature. Une autre étape demande confirmation, et certaines commandes
la demandent toujours (celles qui commitent ou déplacent des fichiers
avant un de leurs tests — la confirmation dit pourquoi). Une étape
« t'attend » ouvre « À répondre » filtré sur elle. L'étape qui tourne
montre le run dessous : l'agent, le texte, « Arrêter », « Continuer la
session ». L'étape de test porte « Déployer » (`/deploie`) et ce qu'il
faut tester, d'après `code/recette-ordonnee.md`.

**Chaîne → Code** — `/8_code` lot par lot : les lots passés sur le total,
en barre ; pendant un run, le lot en cours et l'agent qui y travaille, le
temps depuis le début et, dès que deux lots sont passés, ce qui reste
« ≈ 40 min » ; « Lancer /8_code », « Arrêter au prochain lot »,
« Arrêter maintenant ». Puis chaque lot, dans l'ordre de la séquence, par
bloc : son titre (l'`Anchor` de `code/decoupage.md`), son état — pas
commencé · entamé · en cours · passé · échoué · échoué 3 fois · annulé ·
bloqué · redécoupé · inconnu —, ses essais sur 3, les agents qui y ont
travaillé (temps, tokens lus, écrits), une marque quand l'Arbitre ou
l'Architecte est intervenu, et « À répondre » filtré sur lui quand un
blocage l'attend. Un clic ouvre le lot : sa fiche exécutable, son verdict
et les constats du Relecteur, ses commits et les fichiers qu'ils
changent, ses passages d'agent sur une ligne de temps. Chaque règle est
écrite dans `code_rules.md`. Pendant un run, les fichiers sont lus dans
son worktree, et relus quand un agent rend la main.

**Correction** — les `bugfix-NN/` de la feature, le plus récent d'abord,
chacun en chaîne de correction, avec les mêmes onglets « Amont » et
« Code ». Seul le plus haut se lance : les
commandes agissent sur lui. « Nouvelle correction » crée le `bugfix-NN/`
suivant et son `bug-list.md` vide, rien d'autre, et l'ouvre pour l'écrire
ici, tant que le diagnostic ne l'a pas lu.

**Notifications** — Paramètres → Notifications : une case par événement
(fin d'un run avec sa ligne `Next:` en clair, autorisation qui attend,
question ou blocage qui arrive pendant un run, erreur, plafond d'attente,
lot de `/8_code` qui passe ou échoue). Le navigateur demande l'autorisation
la première fois qu'une case est cochée. Elles ne viennent que quand
l'onglet du cockpit n'est pas devant ; un clic ramène l'onglet sur l'écran
concerné. Chacune nomme son application (« Belivo — /1_lexique x —
terminé »). Le titre de l'onglet compte ce qui vous attend et nomme
l'application active : « (2) Belivo — Cockpit ».

**Usage de l'abonnement** — sur le tableau de bord, deux jauges : la
fenêtre de 5 heures et la semaine. Pour chacune : le pourcentage utilisé,
ce qui reste, l'heure de réinitialisation et **quand la mesure a été
prise** (« mesuré il y a 12 min »). Elles se mettent à jour à la fin de
chaque run (le cockpit demande `/usage` à la session, sans appel au
modèle). Une mesure dont la fenêtre s'est réinitialisée depuis le dit :
ce n'est plus le chiffre du moment.

**Statistiques** — ce que `stats.sqlite` garde, lu en détail : par
application (l'active, ou toutes — chaque run garde la sienne ; ceux
d'avant 1.6 ont retrouvé la leur au démarrage), par
fonctionnalité (celle qui est ouverte, ou toutes) et par période
(aujourd'hui, 7 jours, 30 jours, tout), deux filtres dont le cockpit se
souvient. En bref ; l'usage des deux fenêtres dans le temps, les runs
marqués sous l'axe ; par commande, par agent, par fonctionnalité ; les
dix runs et les dix passages d'agent les plus coûteux, « inhabituel »
au-delà de deux fois la médiane des leurs ; l'historique des runs, un clic
ouvrant ses passages d'agent et le chemin de son journal ; une feature
choisie, « Par lot » : passages, temps, tokens et essais de chaque lot. Les tableaux se
trient sur chaque colonne. « ≈ 4 % de la fenêtre 5 h » : l'écart entre
la mesure du début du run et celle de sa fin — les limites comptent tout
ce que le compte a utilisé entre-temps, et se lisent au pour cent. Un
chiffre absent de la base est « inconnu » et n'entre dans aucune somme,
qui le dit. « Exporter » écrit les runs et les passages des filtres en
deux fichiers CSV, dans le dossier choisi.

**La chaîne de l'application** — les agents, les commandes, les scripts
et les grilles qu'une application lit viennent du dépôt de la chaîne, ce
dépôt-ci, à son dernier commit : on ne les change que là. Le tableau de
bord dit leur état en une ligne : **à jour** ; **en retard** (combien de
commits de la chaîne depuis l'installation, et lesquels) ; **modifiée sur
place** (les fichiers changés dans l'application) ; **absente** (jamais
installée). Pas à jour, un bandeau le dit sur tous les écrans, et lancer
une commande demande d'abord. Paramètres → Chaîne → « Installer / mettre
à jour la chaîne » copie les fichiers, retire ceux que la chaîne n'a plus,
écrit `.claude/chain-version.json`, commite ces seuls fichiers dans
l'application (`chain: <id> <date>`) et pousse. Il refuse pendant un run,
et tant qu'un fichier de la chaîne a des modifications non commitées dans
l'application ; il demande avant de remplacer un fichier changé sur place.
Les fichiers propres à l'application — son `/deploie` — ne sont jamais
touchés.

**Le diagnostic** — un par application, chacune sa pile (Gradle pour
l'une, Flutter pour l'autre) : quand l'application active n'en a pas, le
cockpit le lance une fois de lui-même et garde le résultat. Le tableau de bord ne
l'affiche que s'il a un échec ; Paramètres → Diagnostic le relance à la
demande.

**À répondre** — toutes les questions ouvertes et tous les blocages qui
vous attendent, dans un seul formulaire, **à gauche** ; **à droite**, le
document dont parle la question choisie, en lecture seule, le passage
surligné : chaque occurrence des termes (« 1 / 5 », précédente,
suivante), ou le bloc entier. Un terme de plusieurs mots est surligné
entier, jamais mot par mot. Les deux volets défilent chacun de son côté,
entre la barre du haut et la barre d'enregistrement : faire défiler le
document ne fait jamais quitter la question. Si le passage n'est pas dans le fichier, le
volet le dit. Ce que chaque question vise est écrit dans
`context_rules.md`. Au clavier : `1` à `6` choisissent une option, `T`
place le curseur dans le texte libre, `Échap` en sort, `Entrée` ou `↓`
passent à la question suivante, `↑` revient, `←` et `→` passent d'une
occurrence à l'autre dans le document, `Ctrl+S` enregistre. Les
touches ne font rien pendant la saisie d'un texte (sauf `Ctrl+S`).
Dans le formulaire :
- choisir une option, éventuellement avec une remarque ;
- ou écrire une réponse libre ;
- ou laisser « Plus tard ».
Le défaut proposé est pré-coché : le garder sans remarque laisse
`Answer:` vide, ce que la chaîne lit comme accepté. **Un seul bouton
« Enregistrer »** écrit tout, puis dit pour chaque entrée si elle est
enregistrée ou pourquoi elle ne l'est pas. Les fichiers que le cockpit
ne sait pas lire sont signalés en haut, jamais ignorés.

**Le run** — sous son étape, dans « Chaîne » ou « Correction » : la
commande qui tourne, l'agent actif, le texte au fil de l'eau. Une demande
d'autorisation apparaît en bandeau sur tous les écrans : « Autoriser » ou
« Refuser » ; la commande attend votre clic. « Arrêter maintenant »
interrompt le tour en cours. « Arrêter au prochain lot » (sur `/8_code`
seulement) écrit `stop.md` ; « Retirer stop.md » le renomme `stop1.md`.

Quand un agent rend la main, une ligne dit ce qu'il a consommé :
« Lexicographe — 4 min 12 s — 182 k lus (dont 160 k en cache), écrits :
à la fin du run ». Pendant le run, rien ne donne ce qu'un sous-agent
écrit. À la fin du run, ses totaux, écrits compris, et ce que chaque
agent a écrit : le chiffre de son modèle dans le total du run, quand il
est seul à l'avoir utilisé — ce qu'il a lu sur ce modèle doit tomber
exactement sur ce que le total en dit ; sinon « inconnu », jamais une
estimation. Deux agents sur le même modèle, ou l'orchestrateur sur le
modèle de l'agent : « inconnu » pour eux. Tout est gardé dans
`stats.sqlite` (hors git) ; les anciens journaux y sont chargés une fois
au démarrage du serveur, et les runs déjà gardés y retrouvent leurs
chiffres depuis leurs journaux.

Un blocage n'est jamais caché sur une supposition : quand le cockpit
devine qu'une entrée n'est peut-être pas à vous (un manque que `/8_code`
règle seul, un verdict de l'Architecte), elle reste dans « À répondre »
avec ce qu'il a vu.


## Ce que le cockpit ne fait jamais

- Il ne lance aucune commande que vous n'avez pas cliquée.
- Il ne remplace la ligne `Next:` que quand les fichiers la contredisent,
  et il le dit ; sa proposition porte toujours « déduite du dossier ».
  Il ne saute jamais une étape bloquée ou inconnue.
- Le relevé du dossier ne fait que lire : aucun appel à Claude, aucune
  commande git, aucune écriture.
- L'onglet « Code » ne fait que lire : les fichiers, `stats.sqlite`, et
  `git log` pour les commits d'un lot.
- Le volet du document ne fait que lire.
- Il n'écrit qu'où vous écrivez déjà : les champs `Answer:`, les
  `## Decision`, `## Décision du Product Owner` dans
  `code/redecoupage.md`, `stop.md`, et le `bug-list.md` d'une nouvelle
  correction — et, quand vous cliquez « Installer / mettre à jour la
  chaîne » ou « Tout mettre à jour », les fichiers de la chaîne dans
  l'application, leur commit et son push. Tout le reste est en lecture.
- Ajouter, renommer ou retirer une application ne change que sa liste,
  dans `config.json` : rien n'est écrit dans son dossier.
- Il ne touche jamais au travail non commité d'une application.
- Après chaque écriture, il relit le fichier avec le test de la commande ;
  si la commande le lirait encore comme sans réponse, il annule l'écriture
  et vous le dit.
- Il n'accorde aucune autorisation tout seul.
- Il n'écoute que sur cette machine (`127.0.0.1`).

S'il tombe en panne, rien n'est perdu : toutes les commandes se lancent
toujours depuis Claude Code, et les fichiers sont les mêmes.

## Tests

    pip install -r requirements-tests.txt
    python -m pytest
