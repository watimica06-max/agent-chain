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

- **L'écran d'accueil** (1.9) : le cockpit s'ouvre toujours là, jamais
  directement sur un tableau de bord — une carte par application de la
  liste. Un clic sur une carte l'ouvre sur son tableau de bord : elle
  devient l'application **ouverte**, et tous les écrans travaillent sur
  elle, sur sa dernière feature. Une application sans feature ouverte
  propose d'en choisir une.
- **Feature** : une feature de `docs/features/` de l'application active.
  Ses corrections `bugfix-NN/` sont sous « Correction », plus ici.
- **Dossiers ignorés** (1.5.1) : ceux d'une ancienne chaîne, que rien
  ne doit plus montrer — par application, dans `config.json`
  (`"ignored"`) ; une nouvelle application n'en a aucun. Un dossier ignoré et ses `bugfix-NN/` ne
  paraissent nulle part : ni dans la liste des features, ni sous
  « Correction », ni dans le scan, les Statistiques ou le Code.
  Paramètres → Dossiers ignorés montre la liste ; une case par dossier la
  modifie.
- **Changer de feature** : la feature, dans la barre du haut, ouvre la
  liste des features de l'application.

## Les écrans

**L'écran d'accueil — Applications** (1.6, 1.9) — une carte par
application : son nom et son dossier ; sa chaîne (**à jour**, **en
retard**, **modifiée sur place**, **absente**) ; sa feature et l'étape que
le relevé du dossier y propose ; ce qui vous y attend, en nombre de
questions et de blocages ; son dernier run (la commande, quand, comment il
a fini) ; le nombre de fichiers non commités dans son dossier — pour
information, le cockpit n'y touche jamais ; une commande qui y tourne,
« en cours », avec « Arrêter ». Un clic sur la carte l'ouvre sur son
tableau de bord. Son petit menu « ⋯ » : « Renommer », « Retirer de la
liste » (il demande d'abord ; le dossier n'est pas touché, seule la liste
change). Quand sa chaîne n'est pas à jour, « Installer » ou « Mettre à
jour la chaîne ». Pas de menu de côté sur cet écran : il appartient à une
application ouverte. En haut :
- **« Nouvelle application »** (1.7, 1.9) : une page à elle, toute la
  largeur, avec « Retour » vers l'accueil. Elle crée une application de rien,
  jusqu'à `/1_lexique`, sans appeler Claude. Un seul écran : son nom ; son
  dossier — le dossier parent (la fenêtre de choix, `C:\Dev\` d'abord) et
  le nom du dossier, proposé d'après le nom (minuscules, tirets), le chemin
  complet affiché ; un dossier qui existe et n'est pas vide est refusé ;
  votre fichier d'idées (`.md` ou `.txt`, la fenêtre de choix ou le chemin
  collé), montré en lecture seule avant que rien ne soit créé ; le nom de
  la première fonctionnalité (minuscules, chiffres, tirets) ; et, si vous
  voulez, l'adresse d'un dépôt GitHub que vous avez créé **vide** (sans
  README, sans `.gitignore`, sans licence). Sans dépôt, rien n'est poussé,
  et les commandes de la chaîne diront leurs push en échec jusqu'à ce
  qu'on en ajoute un. Un récapitulatif, puis « Créer ». Chaque étape
  s'affiche ✓ ou ✗ : le dossier et son dépôt git (branche `master`, un
  `.gitignore`) ; le dépôt distant — s'il contient déjà des commits, tout
  s'arrête là, rien n'est forcé ; la chaîne, premier commit du dépôt ; le
  socle (`.claude/scripts/socle.py`, que la chaîne apporte : le global, le
  dossier des features, l'état technique, `chore: scaffolding for the
  chain`) ; votre fichier d'idées, copié tel quel en
  `docs/features/<fonctionnalité>/idees.md` et commité (`feat: … —
  idées`) ; enfin l'application dans la liste, active, ouverte sur sa
  feature, et le tableau de bord propose `/1_lexique`. Chaque commit est
  poussé quand il y a un dépôt distant. **Une étape qui échoue** arrête la
  création, dit laquelle et pourquoi, et propose « Reprendre », qui
  continue depuis elle : chaque étape regarde ce qui est déjà là et ne le
  refait pas. Le cockpit ne supprime jamais le dossier qu'il a créé : il
  dit ce qu'il contient. Une création arrêtée reste proposée, sur sa page
  et sur l'accueil, même après un redémarrage du cockpit ; « Abandonner »
  la retire de la liste, le dossier reste tel quel. Une création finie
  ouvre le tableau de bord de la nouvelle application.
- **« Ajouter une application »** : la fenêtre de choix de Windows, ou le
  chemin collé. Il faut la racine d'un dépôt git ; un autre dossier est
  refusé, et la page dit pourquoi. Ajouter n'écrit rien dans le dossier.
  Un dépôt où la chaîne n'est pas encore installée s'ajoute aussi : il
  montre « chaîne absente », et sa carte l'installe. L'ouvrir sur une
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

**La barre du haut** (1.9), dans une application : son nom, sa feature
(un clic ouvre la liste des features), le mode ; et, à droite, sur tous
ses écrans, **« Applications »**, qui ramène à l'accueil. **Une commande
qui tourne continue** : elle vit dans le serveur, pas dans la page, et
l'arrêter perdrait son travail. Partir le dit une fois par run :
« Une commande tourne dans <application> : elle continue. Tu la retrouves
en rouvrant <application>. » — et sa carte dit « en cours », avec son
« Arrêter ».

**Une commande à la fois** — toutes applications confondues : pendant
qu'une commande tourne dans une application, rien ne se lance dans aucune
autre. Ouvrir une autre application reste permis — pour lire, pour
répondre ; y lancer est refusé, et le bouton dit où la commande tourne. La
barre du haut dit dans quelle application elle tourne, avec « Arrêter » ;
ailleurs, un bandeau le dit sur tous les écrans, et ses demandes
d'autorisation y arrivent aussi. Le tableau de bord d'une autre
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
session ». L'étape de test porte « Déployer », qui ouvre l'écran
« Déploiement » (1.8), et ce qu'il faut tester, d'après
`code/recette-ordonnee.md`. Le `/deploie` propre à l'application, quand
elle en a un, se lance depuis « Déploiement → Déployer », en bas (1.9).

**Ce qu'aucune étape ne lance** (1.9) — « Paramètres → Commandes » n'est
plus. En bas de l'onglet « Amont » de « Chaîne », un bloc **« Audits »** :
`/audit_blocages` et `/audit_conventions`, chacun avec sa ligne de
description, lancés sur la feature ouverte — et, s'il y en a, les autres
commandes de l'application qu'aucune étape ne lance. L'étape « Fusionner
dans le global » porte ses deux moitiés, `/fusion_compare` et
`/fusion_applique`, à lancer seules. Une commande que le dernier relais
n'a pas nommée demande d'abord.

**Construire le projet** — l'étape de `/batir`, entre « Établir les
conventions » et « Découper en lots » : le Bâtisseur construit le squelette
que les conventions déclarent (les tables de G2.1, G4.4 et G12.6) et prouve
qu'il se construit. Son rapport est celui de l'application,
`docs/BUILD_REPORT.md`, un pour toutes les features et toutes les
corrections. Faite quand il dit `## Status: built` depuis le commit qui a
changé les conventions en dernier — le test même de `/7_lots` ; à faire
de nouveau dès que les conventions changent, tant que le découpage n'est
pas coupé — ensuite `/8_code` ne le teste plus, et elle reste faite ; t'attend
quand le Bâtisseur a laissé un `blocked_batisseur.md` sans décision.
« Pourquoi ? » montre la ligne de statut du rapport et son commit. Une fois
construit, les commandes du rapport s'affichent sous l'étape, chacune avec
son résultat et sa durée, puis les cibles du profil de déploiement. Sur un
outil de build introuvable, son blocage est un tutoriel : « À répondre »
le montre étape par étape — les commandes à taper et les chemins mis à
part — et « fait » y est déjà choisi : il reste à le suivre, puis à
enregistrer. Les demandes du Bâtisseur à l'Architecte (`architecte/`) ne
sont jamais là : l'Architecte y répond.

**Déploiement** (1.8) — construire l'application active et l'installer là
où elle tourne, sans Claude, puis la regarder tourner. Ce qu'il faut
construire et où l'installer est le **profil de déploiement** de
l'application, `.claude/deploy.json` : une liste de **cibles** —
« Téléphone », « Montre », « Site » —, chacune avec son type, la commande
qui la construit, et ce que son type demande. Le contrat de ce fichier est
`.claude/formats/deploy-profile.md`, un exemple par type. Deux types aujourd'hui :
**android** (des appareils par adb : en USB, en Wi-Fi, des émulateurs) et
**commande** (une commande lancée sur cet ordinateur : un serveur web, un
programme, un script). Un autre type viendra en ajoutant un adaptateur :
l'écran ne montre que ce que chaque adaptateur dit savoir faire. Trois
onglets, et un quatrième, « Profil » (1.9) :
- **Destinations** — les appareils, groupés par type, en cartes : le nom
  que vous leur donnez (« Renommer », gardé par le cockpit sous le numéro
  de série de l'appareil, qui ne change pas entre USB et Wi-Fi), le
  modèle, montre, téléphone ou émulateur, la version d'Android, la
  batterie, USB ou Wi-Fi, l'état. **Non autorisé** : une ligne dit quoi
  accepter sur l'appareil. **Hors ligne** : le rebrancher. Un appareil qui
  disparaît reste, grisé, « déconnecté », avec sa dernière adresse Wi-Fi et
  « Reconnecter ». Rafraîchi toutes les quelques secondes, et par
  « Rafraîchir ». Sur un appareil : « Journal », « Capture d'écran »
  (affichée dans la carte), « Afficher l'écran » (scrcpy, quand il est
  installé ; sinon, où le trouver), « Lancer » et « Arrêter »
  l'application. **Wi-Fi** : « Associer » (l'adresse IP, le port et le
  code à six chiffres que l'appareil affiche), « Connecter » (l'adresse et
  le port de connexion), et où trouver tout cela sur Wear OS. **Le port de
  connexion change chaque fois que le débogage sans fil redémarre** : il
  faut alors reconnecter avec le nouveau ; l'association, elle, reste. Ce
  qu'adb trouve seul sur le réseau est listé, prêt à connecter.
  **Émulateurs** : les appareils virtuels d'Android Studio, « Démarrer ».
  Pour une cible « commande », une seule destination : « cet ordinateur »,
  avec « Arrêter » et « Ouvrir » (son adresse) quand elle tourne.
- **Déployer** — d'abord le commit du dépôt principal, et s'il a des
  fichiers non commités (le build part de ce qui est sur le disque, eux
  compris). Puis les cibles, une case chacune, et sous chacune les
  destinations que son type propose (une cible « téléphone » n'est pas
  proposée sur la montre) ; le choix est gardé par application.
  « Construire et installer » : par cible, son build une fois, puis sur
  chaque destination son installation, puis son lancement. Chaque étape
  ✓ ou ✗ avec sa durée ; un échec montre la fin de sa sortie ; la sortie
  complète va dans `tools/cockpit/logs/deploy-….log`. Un build qui échoue
  saute les installations de sa cible ; une installation qui échoue sur un
  appareil n'empêche pas les autres. **Refusé pendant qu'une commande de
  la chaîne tourne dans la même application** : le build ferait la course
  avec son merge — l'écran dit laquelle. Et l'inverse : une commande ne se
  lance pas pendant qu'un déploiement construit dans son application. Le
  déploiement tourne dans le cockpit, comme un run : fermer la page ne
  l'arrête pas, et une notification dit quand il finit.
- **Journal** — une destination à la fois, son journal en direct : pour
  Android, `adb logcat` réduit aux processus de l'application, suivi quand
  elle redémarre ; pour une commande, sa sortie. **Les crashs ressortent**
  — Android : `FATAL EXCEPTION`, `ANR in` et la pile dessous ; commande :
  une trace Python, une ligne qui commence par une erreur ou une
  exception —, listés en haut avec leur heure, et une notification quand
  l'onglet n'est pas devant. Pause, Effacer, un filtre, « Enregistrer »
  (le journal entier, dans `tools/cockpit/logs/`), « Copier le crash »
  (prêt à donner à Claude : l'appareil, l'heure, ses lignes).

**Déploiement → Profil** (1.8 ; sous Paramètres jusqu'à la 1.9) — le
profil de l'application ouverte :
ses cibles, à modifier, ajouter, retirer ; les champs montrés sont ceux du
type choisi, chacun avec ce qu'il veut dire. « Enregistrer le profil »
écrit `.claude/deploy.json`, le commite seul dans l'application
(`deploy: profil`) et pousse. Refusé pendant qu'un run ou un déploiement
tourne dans l'application. Une application neuve n'a pas de profil tant
qu'on n'en a pas écrit un.

**À fournir avant le code** (1.7) n'est plus : la chaîne apporte la
compétence et le format du profil, `/conventions` écrit les conventions,
et « Construire le projet » dit, dans « Chaîne », ce qui manque encore.

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

**Paramètres** (1.9) — ce qui appartient au cockpit lui-même, dans cet
ordre, chacun avec sa ligne d'explication : le mode de permission, les
notifications, les dossiers ignorés, « Outils sur cet ordinateur »,
« Arrêter le cockpit ». La version de la chaîne est sous « Chaîne →
Version », le profil de déploiement sous « Déploiement → Profil », la
feature dans la barre du haut, l'application sur l'accueil.

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

**La chaîne de l'application** — les agents, les commandes, les scripts,
les grilles, les formats et la compétence `technical-state-format`
qu'une application lit viennent du dépôt de la chaîne, ce dépôt-ci, à son
dernier commit : on ne les change que là. Une application qui avait sa
propre copie de la compétence : l'installation demande avant de la
remplacer. Le tableau de
bord dit leur état en une ligne : **à jour** ; **en retard** (combien de
commits de la chaîne depuis l'installation, et lesquels) ; **modifiée sur
place** (les fichiers changés dans l'application) ; **absente** (jamais
installée). Pas à jour, un bandeau le dit sur tous les écrans, et lancer
une commande demande d'abord. Chaîne → Version (1.9 ; sous Paramètres
jusque-là) → « Installer / mettre à jour la chaîne » copie les fichiers, retire ceux que la chaîne n'a plus,
écrit `.claude/chain-version.json`, commite ces seuls fichiers dans
l'application (`chain: <id> <date>`) et pousse. Il refuse pendant un run,
et tant qu'un fichier de la chaîne a des modifications non commitées dans
l'application ; il demande avant de remplacer un fichier changé sur place.
Sous Windows, chaque installation et chaque mise à jour règle aussi
`core.longpaths=true` dans le dépôt de l'application (le sien, jamais le
réglage global) : un build dans un worktree écrit des chemins plus profonds
que la limite de Windows, et le retrait du worktree échouerait dessus à
moitié fait. `socle.py` le règle aussi à la création.
Les fichiers propres à l'application — son `/deploie` — ne sont jamais
touchés.

**Outils sur cet ordinateur** (le diagnostic) — il vérifie que les outils
dont les builds et les commandes de l'application ont besoin — Java,
Gradle ou Flutter, adb, Claude Code, git — sont installés et répondent. Un
par application, chacune sa pile (Gradle pour l'une, Flutter pour
l'autre) : quand l'application ouverte n'en a pas, le cockpit le lance une
fois de lui-même et garde le résultat. Le tableau de bord ne l'affiche que
s'il a un ✗ ; Paramètres → Outils sur cet ordinateur le relance à la
demande. Il dit aussi (1.8) si scrcpy et l'émulateur Android sont là, ✓ ou
« non trouvé » : tous deux facultatifs, jamais une alerte.

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
  l'application, leur commit et son push ; quand vous cliquez « Enregistrer
  le profil », `.claude/deploy.json`, son commit et son push. Tout le reste
  est en lecture.
- « Déploiement » ne lance que les commandes du profil, quand vous
  cliquez ; il n'installe, ne lance, n'associe ni ne connecte rien sur un
  appareil sans un clic. Les noms de vos appareils restent dans
  `config.json`, jamais dans l'application.
- Ajouter, renommer ou retirer une application ne change que sa liste,
  dans `config.json` : rien n'est écrit dans son dossier.
- « Nouvelle application » n'écrit que dans le dossier qu'elle crée, neuf
  ou vide, et ne le supprime jamais ; elle ne force jamais un dépôt
  distant qui contient déjà des commits. Elle ne reprend qu'une création
  qu'elle a commencée : une application existante n'est jamais touchée.
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
