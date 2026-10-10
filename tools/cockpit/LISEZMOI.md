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
- **Arrêter le cockpit** : Paramètres → « Arrêter le cockpit » ; si un run tourne, il demande d'abord, et le run est arrêté. L'écran « Le cockpit est arrêté » reste ensuite (1.9.1) : la page ne se reconnecte plus d'elle-même.

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
- **GitHub** (1.12) : le dépôt de la chaîne (agent-chain) est récupéré
  depuis GitHub ; s'il était en retard, il est mis à jour — en avance
  rapide seulement — et un bandeau dit « Nouvelle version du cockpit et de
  la chaîne récupérée — « Mettre à jour le cockpit » la met en service. »,
  avec ce bouton (1.14). Chaque application de la liste est récupérée
  aussi, en arrière-plan.
- **La consommation** (1.17) : mesurée au démarrage, en arrière-plan —
  voir « Consommation » plus bas. L'écran d'accueil la mesure de nouveau
  quand la dernière mesure a plus de 15 minutes.

## Les écrans

**L'écran d'accueil — Applications** (1.6, 1.9 ; un tableau depuis la
1.11) — une ligne par application : son nom et son dossier ; sa chaîne (**à jour**, **en
retard**, **modifiée sur place**, **absente**) ; sa feature et l'étape que
le relevé du dossier y propose ; ce qui vous y attend, en nombre de
questions et de blocages ; son dernier run (la commande, quand, comment il
a fini) ; **GitHub** (1.12) — où ce dépôt en est face à GitHub, et en
dessous le nombre de fichiers non commités dans son dossier ; une commande qui y tourne,
« en cours », avec « Arrêter ». Un clic sur la ligne l'ouvre sur son
tableau de bord, comme « Ouvrir ». Son petit menu « ⋯ » : « Renommer », « Retirer de la
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
- **« Ajouter depuis GitHub »** (1.12) : sur le second ordinateur, une
  application qui est déjà sur GitHub — l'adresse du dépôt et le dossier
  parent ; elle y est clonée (`core.longpaths=true` réglé dans le clone),
  puis ajoutée à la liste comme « Ajouter » le fait. Un dossier qui existe
  et n'est pas vide est refusé.
- **« Ajouter une application »** : la fenêtre de choix de Windows, ou le
  chemin collé. Il faut la racine d'un dépôt git ; un autre dossier est
  refusé, et la page dit pourquoi. Ajouter ne touche à aucun fichier du
  dossier ; 1.12 : il règle `core.longpaths=true` dans sa configuration git.
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

**Le menu de côté et la barre du haut** (1.9 ; 1.11), dans une
application. Le menu, sur toute la hauteur à gauche : l'application et sa
feature en tête ; ses écrans en trois groupes — Pilotage (Tableau de bord,
À répondre, Chaîne, Correction), Projet (Données, Déploiement), Mesure
(Statistiques, Journal — 1.20, Enquêtes — 1.21) ; en bas, Paramètres et **« Applications »**, qui ramène à
l'accueil. La barre du haut est un chemin — l'application / sa feature
(un clic ouvre la liste des features) / l'écran —, puis, à droite, le mode
et la commande qui tourne. **Une commande
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

**Le menu** — le bouton à gauche de la barre du haut ferme et rouvre le
menu de côté ; l'espace de travail prend alors toute la
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

**Chaîne** — la chaîne principale, une frise d'étapes, une par commande,
son état en icône, en couleur et en mot : faite (✓) · t'attend (la main
levée) · en cours (▶) · bloquée (le sens interdit) · à faire (son numéro) ·
inconnu (le point d'interrogation, en pointillé). La prochaine étape ressort ; un clic sur « Lancer » la lance avec
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

**Données** (1.10) — les fichiers que la chaîne ne peut pas inventer
(`.claude/formats/donnees.md`). Deux onglets : **« De l'application »**,
`docs/donnees/` — ce que l'application embarque et livre ; **« De la
fonctionnalité »**, le `donnees/` de la feature active — des instances
réelles de ce qu'elle lit, dont la spécification et les tests partent,
jamais livrées. Chaque onglet montre une carte par entrée de l'index — le
fichier, ce que c'est, d'où il vient, sa date, privé ou non — et « Aperçu »
montre à côté les premières lignes d'un fichier texte, ou l'image. **« Joindre des
fichiers »** ouvre la fenêtre de choix, plusieurs fichiers à la fois : chacun
est copié tel quel dans le dossier, et son entrée s'ouvre à remplir (la date
du jour par défaut). « Modifier » une entrée ; « Retirer » demande, et le
fichier part avec son entrée. **« Enregistrer »** écrit l'index au format,
commite le dossier (`donnees: …`) et pousse ; refusé pendant qu'une commande
tourne dans l'application. **Privé** : le fichier va dans `.gitignore` et
n'est jamais commité — ni lui, ni les copies que les lots en feront ; un
fichier déjà commité sort de l'index de git, et la page dit qu'il reste dans
l'historique, comme les copies déjà commitées. Un fichier privé ne passe
donc jamais d'un ordinateur à l'autre : sur celui qui ne l'a pas, son entrée
dit **« pas sur cet ordinateur »**, et « Enregistrer » la garde (1.12) ; un
fichier non privé absent du disque est toujours refusé. Dans « À répondre », une
question qui demande un fichier (sa ligne `Folder:`) offre **« Joindre un
fichier »** : le fichier va dans le dossier qu'elle nomme, son entrée
s'ouvre à remplir, et la réponse nomme le fichier ; ses autres options
restent.

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
qu'on n'en a pas écrit un. Une cible ajoutée tout de suite après
l'ouverture de l'onglet reste (1.12.2) : une seconde lecture du profil,
arrivée après, ne remet plus le formulaire à zéro.

**À fournir avant le code** (1.7) n'est plus : la chaîne apporte la
compétence et le format du profil, `/conventions` écrit les conventions,
et « Construire le projet » dit, dans « Chaîne », ce qui manque encore.

**Chaîne → Code** — `/8_code` lot par lot : les lots passés sur le total,
en barre ; pendant un run, le lot en cours et l'agent qui y travaille, le
temps depuis le début et, dès que deux lots sont passés, ce qui reste
« ≈ 40 min » ; « Lots à coder » et « Lancer /8_code », « Arrêter au
prochain lot », « Arrêter maintenant ». Puis chaque lot, dans l'ordre de la séquence, par
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
ordre : l'apparence (1.11), puis, chacun avec sa ligne d'explication, le
mode de permission, la consommation (1.17), les notifications, l'accès depuis le téléphone
(1.15), les dossiers ignorés, « État de l'ordinateur » (1.16), « Version du cockpit » (1.14), « Arrêter le cockpit ». La version de la chaîne est sous
« Chaîne → Version », le profil de déploiement sous « Déploiement →
Profil », la feature dans la barre du haut, l'application sur l'accueil.

**Apparence** (1.11) — Paramètres → Apparence, « Thème : Auto / Clair /
Sombre ». Auto, le défaut, suit le réglage de l'ordinateur ; Clair ou
Sombre l'imposent, sur tous les écrans. Le choix est gardé par le
navigateur, comme les notifications et le menu. Toutes les couleurs et
toutes les tailles de la page sont des variables CSS, en tête de
`static/index.html` ; le thème sombre redéfinit les mêmes. Les icônes sont
des SVG dessinés pour le cockpit, dans la page elle-même : rien ne vient
d'internet.

**Notifications** — Paramètres → Notifications : une case par événement
(fin d'un run avec sa ligne `Next:` en clair, autorisation qui attend,
question ou blocage qui arrive pendant un run, erreur, plafond d'attente,
lot de `/8_code` qui passe ou échoue). Le navigateur demande l'autorisation
la première fois qu'une case est cochée. Elles ne viennent que quand
l'onglet du cockpit n'est pas devant ; un clic ramène l'onglet sur l'écran
concerné. Chacune nomme son application (« Belivo — /1_lexique x —
terminé »). Le titre de l'onglet compte ce qui vous attend et nomme
l'application active : « (2) Belivo — Cockpit ».

**Usage de l'abonnement** — sur le tableau de bord et sur l'écran
d'accueil (1.17), deux jauges : la fenêtre de 5 heures et la semaine. Pour
chacune : le pourcentage utilisé, ce qui reste, l'heure de
réinitialisation et **quand la mesure a été prise** (« mesuré il y a
12 min ») et d'où elle vient — pendant un run, en fin de run (le cockpit
demande `/usage` à la session, sans appel au modèle), ou mesure du
cockpit. Une mesure dont la fenêtre s'est réinitialisée depuis le dit :
ce n'est plus le chiffre du moment.

**Consommation** (1.17) — la consommation, mesurée et bornée :

- **La mesure.** Au démarrage du cockpit, à l'ouverture de l'écran
  d'accueil si la dernière mesure a plus de 15 minutes, avant un
  lancement dans le même cas, et sur « Mesurer maintenant » : le plus
  petit appel qui fasse dire à Claude Code où en sont les deux fenêtres —
  une phrase courte, le modèle le plus léger (`haiku`), un seul tour, sans
  outil, sans réglage, sans serveur MCP, dans un dossier temporaire à lui
  (`%TEMP%\cockpit-mesure`), jamais celui d'une application. Claude Code
  répond par un `RateLimitEvent` qui donne les deux fenêtres et leur
  réinitialisation ; s'il ne le donnait pas, `/usage` est demandé dans la
  même session. Son coût est enregistré dans `stats.sqlite` comme celui
  d'un run, marqué `kind = 'mesure'` — « (mesure d'usage) » dans les
  Statistiques —, son journal est `logs/<date>-mesure.jsonl`. Sous les
  jauges : la dernière mesure, son âge et ce qu'elle a coûté — ou, si
  elle a échoué (Claude Code pas connecté, hors ligne), pourquoi. Une
  mesure qui échoue ne bloque jamais rien : les jauges gardent la
  précédente, avec son âge.
- **Les seuils.** Paramètres → Consommation : un seuil d'**alerte** et un
  seuil de **blocage**, pour la fenêtre de 5 heures et pour la semaine —
  quatre nombres, 90 % chacun par défaut, gardés dans `config.json`
  (`"usage_thresholds"`). L'alerte atteinte : un bandeau fort sur chaque
  écran, téléphone compris, avec la fenêtre, son niveau et sa
  réinitialisation. Le blocage atteint : le bandeau passe au rouge, et
  aucune commande ne se lance — « Lancer » (et « Continuer la session »)
  demande alors une confirmation qui nomme le niveau ; « Lancer quand
  même » passe outre, et c'est noté dans le journal du cockpit
  (`logs/server.log`) et dans `logs/consommation.log`. Le niveau est la
  dernière mesure ; avant un lancement, une mesure de plus de 15 minutes
  est refaite d'abord. Une fenêtre réinitialisée depuis sa mesure
  n'alerte ni ne bloque.
- **Ce qu'une commande coûtera.** À côté de chaque bouton « Lancer » :
  « ≈ 4 % de la fenêtre · ≈ 1 % de la semaine » — la médiane de ce que
  ses runs passés ont pris (le même calcul que les Statistiques : la
  première mesure du run et son `/usage` de fin, jamais à travers une
  réinitialisation) ; ceux de l'application quand elle en a trois, sinon
  ceux de toutes les applications ; « coût : inconnu » en dessous de
  trois. La bulle dit sur combien de runs.

**Pilote automatique** (1.18) — sur le tableau de bord, ordinateur et
téléphone. Un **programme** lance l'étape que le cockpit propose, commande
après commande, tant que personne n'est nécessaire, en mode de permission
Auto quel que soit le réglage de Paramètres. Un seul programme à la fois,
dans une application, sur cet ordinateur ; il agit sur la feature ouverte
quand il a été créé.

- **Le lancer.** Trois réglages prêts — « Maintenant, jusqu'à ce qu'on ait
  besoin de moi », « Cette nuit, 1 h – 7 h », « Pendant 2 heures » —,
  les programmes enregistrés, et « Programme complet… », le formulaire
  entier. Démarrage : maintenant, à une heure, ou dans un créneau (il
  démarre à son début — tout de suite si on y est déjà — et sa fin est une
  borne). Un démarrage plus tard dit « L'ordinateur doit rester allumé et
  réveillé jusque-là. » ; un programme pas encore démarré survit à un
  redémarrage du cockpit (gardé dans `config.json`).
- **Les bornes**, chacune facultative, combinées librement — **la
  première atteinte l'arrête** : une heure de fin, une durée, un nombre de
  lots codés, un nombre de commandes, un niveau de la fenêtre de 5 heures
  ou de la semaine, et une **étape à atteindre** : « S'arrêter avant » une
  étape du flux, ou « S'arrêter une fois faite » — une liste des étapes,
  dans l'ordre du flux, celles de la correction ouverte comprises. Les
  bornes sont regardées avant chaque commande : une commande commencée va
  à son terme.
- **Il s'arrête toujours** sur : des questions ou un blocage pour vous ;
  une étape pour une personne (les réponses, la bug-list, le test final, la
  recette) ; une erreur ou une commande interrompue ; le seuil de blocage
  de 1.17 (jamais de « Lancer quand même » dans un programme) ; un blocage
  de « État de l'ordinateur » ; une application « divergé » ; une chaîne
  pas à jour ; et avant `/9_controle` et `/diagnostique`, sauf si
  « Laisser tourner /9_controle et /diagnostique » est coché. Aucune étape
  de test intermédiaire : il s'arrête à l'étape de test finale, et ne
  lance jamais `/deploie` ni `/fusion`. Chaque commande passe par les
  mêmes vérifications qu'un clic (GitHub d'abord, 1.12).
- **Le code.** `/8_code` est lancé pour **un lot à la fois** ; entre deux
  lots, le programme regarde ses bornes, la consommation et un arrêt
  demandé. « Nombre de lots codés » est la borne qui remplace « Lots à
  coder » (qui reste pour un lancement à la main).
- **Attendre une réinitialisation.** Avant chaque commande : si son
  estimation (1.17) ferait passer la fenêtre de 5 heures au-delà du seuil
  de blocage, et que la fenêtre se réinitialise dans les bornes du
  programme, il attend la réinitialisation — il le dit, avec l'heure —,
  mesure de nouveau et continue. Réinitialisation au-delà des bornes, ou
  inconnue : il s'arrête et dit pourquoi. Pour la semaine, il s'arrête.
- **L'arrêter.** « Arrêter après la commande en cours » (« après le lot en
  cours » pour `/8_code` : le cockpit pose `stop.md` là où la commande le
  lit, et le retire à la fin du run) ; « Arrêter maintenant », comme
  aujourd'hui ; « Annuler le programme » avant son démarrage. Depuis
  l'ordinateur ou le téléphone. Le bouton « Pilote : … » de la barre du
  haut, sur chaque écran, ramène au panneau.
- **Ce qu'il dit.** Pendant qu'il tourne ou attend : ce qu'il fait, ce
  qu'il attend, ses bornes en mots (« S'arrête à 7 h ou après 4 lots
  encore. »). Une notification au téléphone (1.15) quand il démarre, quand
  il se met à attendre une réinitialisation, et quand il s'arrête — avec
  la raison ; aucune à la fin de chacune de ses commandes. À la fin, un
  résumé : commandes lancées, lots codés, consommation prise (la somme de
  ce que chaque run a pris), pourquoi il s'est arrêté — gardé dans
  `stats.sqlite` (table `programmes`, et chaque run porte son programme),
  montré sous le panneau et dans Statistiques → « Programmes du pilote
  automatique ».
- Tant qu'un programme est actif, « Mettre à jour le cockpit » et le
  redémarrage de lui-même attendent sa fin.

**Statistiques** — ce que `stats.sqlite` garde, lu en détail : par
application (l'active, ou toutes — chaque run garde la sienne ; ceux
d'avant 1.6 ont retrouvé la leur au démarrage), par
fonctionnalité (celle qui est ouverte, ou toutes) et par période
(aujourd'hui, 7 jours, 30 jours, tout), deux filtres dont le cockpit se
souvient. En bref ; l'usage des deux fenêtres dans le temps, les runs
marqués sous l'axe ; par commande, par agent, par fonctionnalité ; les
dix runs et les dix passages d'agent les plus coûteux, « inhabituel »
au-delà de deux fois la médiane des leurs ; l'historique des runs, un clic
ouvrant ses passages d'agent et le chemin de son journal ; en bas,
« Journaux bruts » et « Ouvrir le dossier » (1.9.1) : le dossier des
journaux — runs, déploiements, `server.log`, `next-ecarte.jsonl` ; une feature
choisie, « Par lot » : passages, temps, tokens et essais de chaque lot. Les tableaux se
trient sur chaque colonne. « ≈ 4 % de la fenêtre 5 h » : l'écart entre
la mesure du début du run et celle de sa fin — les limites comptent tout
ce que le compte a utilisé entre-temps, et se lisent au pour cent. Un
chiffre absent de la base est « inconnu » et n'entre dans aucune somme,
qui le dit. « Exporter » écrit les runs et les passages des filtres en
deux fichiers CSV, dans le dossier choisi.

**Journal** (1.20) — le journal de cycle : pour la feature ouverte, et pour
chacune de ses corrections, ce qui s'est passé étape par étape. Il remplace
les notes prises à la main.

- **Une ligne par commande**, à la fin de chaque run lancé depuis le
  cockpit — un clic, une commande d'un programme, « Continuer » —, ajoutée
  à `docs/features/<feature>/journal.md` (le `bugfix-NN/journal.md` d'une
  correction) : la date et l'heure, l'ordinateur (son nom court, 1.21 —
  Paramètres → « Cet ordinateur »), la commande, sa durée,
  son coût (tokens lus et écrits, part de la fenêtre de 5 heures et de la
  semaine), son issue (fait · questions · blocage · à la main · erreur ·
  pas connecté · arrêté · sans Next…), ce qu'elle propose ensuite, les
  fichiers de questions et de blocage qu'elle a créés, son programme, et
  une note (« lancé quand même », « suite de session », l'erreur). Un
  tableau markdown, lisible sur GitHub tel quel, que le cockpit relit ; son
  format est écrit dans `tools/cockpit/journal.py`, nulle part ailleurs.
  **Aucun agent de la chaîne ne le lit**, et aucun ne le reçoit à lire.
- **Commité et poussé** : `journal: <commande> — <issue>`, le journal seul,
  poussé comme les autres commits du cockpit (1.12) — les deux ordinateurs
  voient tout. Un push qui échoue (hors ligne) part au lancement suivant,
  avec « non envoyé ».
- **Le relais reste celui de la chaîne.** Le commit du journal fait bouger
  HEAD, et la règle G-HEAD écarte un relais quand HEAD a bougé sans run du
  cockpit. Le cockpit sait ce que son commit a touché : le relais mémorisé
  sur l'ancien HEAD est reporté sur le commit du journal
  (`State.carry_relay_heads`) — et seulement lui ; G-HEAD garde tout son
  sens pour tout autre commit, et `decide.py` ne lance toujours aucune
  commande git. De même pour la reconstitution et le rapport.
- **Jamais avalé par `chore: answers`.** Avant tout lancement, tout
  « Enregistrer », toute installation (là où le cockpit synchronise avec
  GitHub), la ligne du dernier run est écrite et commitée d'abord ; une
  ligne restée non commitée (un commit qui a échoué) l'est alors seule,
  `journal: lignes en attente`. Avalée quand même — une commande lancée
  hors du cockpit —, elle est sans effet : le relevé, « À répondre » et
  « Envoyer mes réponses » ne la lisent pas.
- **Ce que le journal calcule** : à partir des lignes, de l'historique git
  du dossier et, sur cet ordinateur, des statistiques et des journaux de
  run — chaque fichier de questions (quand il est arrivé, quand il a été
  répondu, donc le temps qu'elle a pris ; combien de questions, de quel
  agent) ; chaque fichier de blocage (arrivé, décidé, réglé — renommé
  `-NN` —, et par qui quand on peut le dire : l'Arbitre quand la décision
  est dans le commit d'un agent, le Product Owner quand elle est dans un
  `chore: answers` ou un `chore: pre-…`, « inconnu » sinon) ; les
  programmes, leurs arrêts et leurs raisons ; les « Lancer quand même ».
- **Points à creuser**, en haut de l'écran, chacun avec sa raison : une
  commande en erreur ou pas connectée ; plusieurs fichiers de blocage du
  même agent dans le cycle ; un run qui a pris plus de deux fois sa part
  habituelle de la fenêtre de 5 heures (l'estimation de 1.17) ; la même
  commande lancée trois fois de suite sans que l'étape proposée bouge ; un
  programme arrêté sur une erreur. Les seuils : Paramètres → Journal de
  cycle.
- **L'écran** : le cycle, les filtres (questions, blocages, erreurs), les
  totaux, le pas à pas par étape, par étape en tableau, « Son temps »,
  les programmes. Sur le téléphone : « Plus » → « Journal », en lecture
  seule.
- **« Reconstituer le passé »** : les lignes des runs d'avant le journal —
  d'après les statistiques et les journaux de run de cet ordinateur, et
  d'après git seul pour le reste (chaque `Merge /<commande>`, et le commit
  d'un agent qui a créé un fichier de questions ou de blocage ; durée et
  coût « inconnu ») —, montrées d'abord, écrites et commitées une fois sur
  confirmation.
- **« Rapport de fin de cycle »** : sur demande, et proposé sur le tableau
  de bord quand la dernière étape de la feature est faite —
  `rapport-cycle.md` dans le dossier du cycle : durée, coût, questions et
  blocages par étape, où est passé son temps, ce qui a échoué, les points à
  creuser. Montré d'abord, commité sur confirmation seulement.
- **« Enquêter sur ce point »** (1.21), sur chaque point à creuser : voir
  « Enquêtes ».

**Enquêtes** (1.21) — une question, en français, sur l'application ou sur
la chaîne et le cockpit : une enquête lit, et seulement lit, et répond pour
une lectrice qui n'est pas technicienne.

- **« Nouvelle enquête »** : la question ; la cible — **l'application**
  ouverte (son dossier) ou **la chaîne et le cockpit** (le dossier
  d'agent-chain, `C:\Dev\chaine`) — ; le modèle — par défaut celui des
  commandes de la chaîne — celui que nomment les réglages de Claude Code
  (le projet, puis l'utilisateur), que le formulaire dit, et que le cockpit
  passe à l'enquête : elle ne charge aucun réglage, et sans lui elle
  tournerait sur le modèle par défaut de Claude Code —, ou un autre pour
  cette enquête. Elle a sa
  route à elle (`/api/enquetes/start`, pas `/api/run`), comme les
  installations de 1.16. **Une à la fois, comme tout run** : refusée tant
  qu'une commande tourne, et une commande, une mise à jour du cockpit,
  attendent sa fin ; le seuil de blocage de 1.17 s'applique (« Lancer quand
  même » noté dans `consommation.log`) ; le pilote automatique n'en lance
  jamais — un programme attend la fin d'une enquête en cours.
- **Lecture seule, imposée par le cockpit** — pas demandée au modèle.
  L'enquête n'a que des outils de lecture : Read, Grep, Glob, et un shell —
  PowerShell sur Windows, que Claude Code y donne, ou Bash là où Git Bash
  est réglé pour lui —, ni Write,
  ni Edit, ni NotebookEdit, ni outil du web, ni agent, ni serveur MCP, ni
  réglage chargé. Chaque appel d'outil passe deux fois par la même règle
  (`enquete.gate`) : le crochet PreToolUse, que Claude Code exécute avant
  tout outil quel que soit le mode de permission, et la fonction de
  permission. Une commande shell ne passe que si chacune de ses commandes
  est une de celles-ci — dans Bash :

  | Commande | Pour |
  |---|---|
  | `git log`, `git show`, `git diff`, `git status`, `git blame`, `git grep` | lire l'historique — avant la sous-commande, seuls `--no-pager` et `-C <dossier>` ; jamais `--output`, `--ext-diff`, `git grep -O` |
  | `ls`, `find` | lister — `find` sans `-delete`, `-exec`, `-execdir`, `-ok`, `-okdir`, `-fprint`, `-fprint0`, `-fprintf`, `-fls` |
  | `cat`, `head`, `tail`, `wc`, `stat` | lire un fichier — `tail` sans `-f` |
  | `grep`, `egrep`, `fgrep`, `rg` | chercher — `rg` sans `--pre` |
  | `sort`, `uniq`, `cut` | ranger ce qu'une autre lit — `sort` sans `-o`, `uniq` sans fichier de sortie |
  | `pwd`, `cd`, `basename`, `dirname`, `realpath` | se repérer |

  Dans PowerShell, la même règle, sous ses noms :

  | Commande | Pour |
  |---|---|
  | `git log`, `git show`, `git diff`, `git status`, `git blame`, `git grep` | lire l'historique, comme ci-dessus |
  | `Get-ChildItem` (`gci`, `ls`, `dir`), `Get-Item` (`gi`), `Test-Path` | lister |
  | `Get-Content` (`gc`, `cat`, `type`) | lire un fichier — sans `-Wait` |
  | `Select-String` (`sls`), `findstr` | chercher |
  | `Measure-Object`, `Sort-Object`, `Select-Object`, `Format-List`, `Format-Table`, `Out-String` | compter, ranger, mettre en forme |
  | `Get-Location` (`pwd`), `Set-Location` (`cd`), `Resolve-Path`, `Split-Path` | se repérer |

  Reliées par `|`, `&&`, `||` ou `;` ; `2>/dev/null` (`2>$null` dans
  PowerShell) et `2>&1` permis.
  Refusé : toute autre commande, une substitution (`$(…)`, `` ` ``, `$`
  hors apostrophes), une redirection vers un fichier, `&`, une variable
  posée, un bloc (`{ … }`, `( … )`, `@( … )`), plusieurs lignes. Une commande refusée l'est avec sa raison ;
  l'écran la montre en rouge, et le rapport les liste.
- **Ce qu'on demande au modèle** : répondre en français, pour une lectrice
  qui n'est pas technicienne ; citer `fichier:ligne` pour chaque
  affirmation ; dire ce qui n'a pas pu être établi ; finir par « Ce que je
  conseille d'en faire » — enquêter plus loin, une correction, ou rien.
- **Le rapport** : `docs/enquetes/<date>-<sujet>.md` dans le dépôt qu'il
  concerne — la question, la réponse, le modèle, le coût (tokens lus et
  écrits, durée, équivalent API), la date, l'ordinateur —, commité
  `enquete: <question>` et poussé (règles de 1.12 ; le relais de la chaîne
  reporté sur ce commit, comme pour le journal). Listé sur l'écran avec son
  coût ; lisible sur le téléphone (« Plus » → « Enquêtes », en lecture
  seule). Une enquête arrêtée ou en erreur n'écrit rien.
- **Pas de redémarrage pour un rapport.** Un commit dans `C:\Dev\chaine`
  fait bouger son HEAD, que 1.16 lit comme « nouveau code du cockpit ».
  Des commits qui ne touchent que `docs/enquetes/` ne redémarrent pas le
  serveur et n'affichent pas « pas encore en service » ; ceux que l'autre
  ordinateur a poussés sont récupérés en silence quand l'écran s'ouvre.
- **D'un problème à une enquête** : « Enquêter sur ce point », sur chaque
  point à creuser du Journal et sur un run fini en erreur — la question
  est écrite (ce qui s'est passé, où, les fichiers et le journal de run à
  regarder), la cible choisie (la chaîne et le cockpit) ; rien ne part
  avant qu'elle l'ait relue et lancée.
- **D'une enquête à la suite**, selon sa cible :
  - **la chaîne ou le cockpit** : « Préparer un prompt de correction » — un
    second appel (sans outil, un tour) écrit un prompt dans la forme de
    ceux de la conversation de conception, enregistré à côté du rapport
    (`…-prompt.md`), marqué **« À relire dans la conversation de conception
    avant de lancer »**, commité et poussé. **Aucun bouton ne le lance** :
    une correction de la chaîne ou du cockpit passe toujours par la
    conversation de conception.
  - **l'application** : un comportement de l'application se corrige par un
    cycle de correction, pour que ses documents restent vrais. « Ajouter à
    la liste de bugs » — un second appel écrit l'entrée d'après le rapport
    (ce qu'on observe, où, ce qui est attendu), au format que lit le
    Diagnostiqueur (`.claude/agents/diagnostiqueur.md`, « What a gap looks
    like » : un `G<n>` qui ouvre l'écart, puis ce qui ne va pas et ce qui
    devrait être) — `G03 Sur l'écran de course : … Elle devrait …`. Elle la
    lit, la change si besoin ; **rien n'est écrit avant « Ajouter »**. Elle
    va dans le `bug-list.md` de la correction ouverte (le `bugfix-NN/` le
    plus haut, tant que `desc-bug.md` n'y est pas), ou d'une nouvelle,
    créée alors — par le même code que « Correction ».

**Cet ordinateur** (Paramètres, 1.21) — le nom court qu'écrivent le journal
de cycle et les rapports d'enquête : « travail », « perso ». **Jamais le nom
de l'ordinateur sur le réseau**, qui partirait sur GitHub. Demandé une fois,
au premier run qui écrit dans un dépôt sans qu'il soit donné ; « Plus tard »
écrit « ordinateur ». Gardé dans `config.json`. Les lignes déjà écrites
restent telles qu'elles sont.

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

**État de l'ordinateur** (1.16 ; « Outils sur cet ordinateur » jusqu'à la
1.15) — tout ce qui doit être présent et à jour pour que la chaîne tourne
bien sur cet ordinateur, une ligne par point : son état, **sa règle**, quand
il a été vérifié, et sa réparation, d'un clic — jamais dans PowerShell.

- **Le cockpit** : le serveur face au code sur le disque, agent-chain face
  à GitHub, les dépendances Python.
- **Claude Code** : le programme que le SDK lance vraiment (celui livré
  avec le SDK d'abord, sinon `claude.exe`), sa version face au minimum du
  SDK ; connecté ou non (`claude auth status`, avec ce même programme).
- **git et GitHub** : git, l'identité des commits, Git Credential Manager,
  les identifiants GitHub (`git credential-manager github list`, puis
  `git push --dry-run --porcelain` sur agent-chain), GitHub joignable,
  `core.longpaths` d'agent-chain.
- **Android et builds** : Java, Gradle ou Flutter (le diagnostic de
  l'application ouverte, quand elle en a), adb, sdkmanager, le SDK
  Android (ANDROID_HOME), l'émulateur et scrcpy (facultatifs).
- **Chaque application** : GitHub, la chaîne installée, `BUILD_REPORT`
  face aux conventions, `core.longpaths`.

Les règles :

| Point | Règle | Ce qu'un blocage arrête |
|---|---|---|
| Claude Code pas connecté | bloque | chaque lancement, « Installer avec Claude » |
| Le Claude Code du SDK absent ou sous son minimum | bloque | les lancements |
| Dépendances Python manquantes | se répare seul (pip au démarrage), signale un échec | — |
| Serveur plus ancien que le code sur le disque | se répare seul quand rien ne tourne (redémarrage), signale pendant un run | — |
| agent-chain en retard sur GitHub | se répare seul (récupéré), signale « pas encore en service » | — |
| La chaîne d'une application en retard | signale, demandé au lancement | — |
| Application « divergé » | bloque | lancement, installation, « Enregistrer » |
| Identifiants GitHub absents | bloque ce qui pousse, signale pour un lancement | push, installation, « Envoyer » |
| Commits non envoyés | signale, toujours visible, jamais en vert | — |
| GitHub injoignable | signale ; bloque l'installation de la chaîne tant qu'il dure | installations |
| Identité git absente | bloque | tout ce qui commite |
| core.longpaths | se répare seul, agent-chain compris | — |
| Java, Gradle, adb, sdkmanager, SDK | signale ; bloque « Bâtir » et l'écran Déploiement | ces deux-là |
| émulateur, scrcpy | facultatif | — |
| BUILD_REPORT plus ancien que les conventions | signale (« Bâtir » proposé à nouveau) | — |

Une identité que git **devine** (sans `user.name` ni `user.email`) est
signalée, jamais bloquante : git commite avec elle ; « Régler » la fixe.

**Quand c'est vérifié** : au démarrage du cockpit, à l'ouverture de
l'écran, après chaque réparation, et juste avant une action pour ce qui la
bloque (Claude Code avant un lancement, les identifiants GitHub avant un
push — revérifiés s'ils datent de plus de cinq minutes). Chaque ligne dit
quand elle l'a été. « Vérifier maintenant » relance tout, le diagnostic de
l'application ouverte compris.

**Le badge** : sur l'accueil et dans la barre du haut, « Ordinateur :
bloqué » ou « à voir » quand un point bloque ou attend quelque chose de
vous ; l'accueil montre ces points avec leur réparation. Le téléphone
montre le même résumé et dit « Réparer sur l'ordinateur » : aucune
réparation ne se fait depuis lui.

**Les réparations** :

- **« Se connecter à Claude »** : `claude auth login` avec le programme
  du SDK, sans fenêtre — il n'en a pas besoin. La page de connexion
  s'ouvre dans le navigateur ; si elle affiche un code, il se colle dans
  le cockpit, qui le transmet. Puis `claude auth status`.
- **« Se connecter à GitHub »** : `git credential-manager github login
  --browser`, sans fenêtre, puis le push à blanc sur agent-chain.
- **« Régler »** : `core.longpaths`, et l'identité git (un nom, un
  e-mail, dans la configuration globale).
- **« Redémarrer le cockpit »** : le redémarrage de la 1.14, sans rien
  récupérer, avec le PATH tel que Windows l'a maintenant. `lancer.bat`,
  quand un cockpit répond déjà, compare le commit dont il est parti au
  code sur le disque ; plus ancien, il lui demande de redémarrer avant
  d'ouvrir la page.
- **« Installer avec Claude »**, pour un outil absent : une session
  Claude avec la consigne de cet outil — l'installer, puis prouver qu'il
  répond —, puis la vérification, et un redémarrage du cockpit si le PATH a
  changé. Jamais sans Claude Code connecté.
- **« Installer les dépendances »**, **« Installer / Mettre à jour Claude
  Code »**.

Les sessions de connexion et d'installation sont refusées pendant un run.

**Deux façons d'installer** (décidé le 10 octobre). Toute installation que
le cockpit mène commence par une question :

- **Rapide** — vous acceptez d'avance les étapes et les licences ; le
  cockpit fait tout sans redemander. Avant le départ, une ligne nomme ce
  qui sera installé et les licences acceptées ; une licence que cette
  ligne ne nommait pas est refusée, et l'installation s'arrête. Après, le
  compte rendu liste ce qui a été installé et chaque licence acceptée.
- **Pas à pas** — une carte pour chaque étape et chaque licence, montrée
  en entier : vous acceptez ou refusez. Une licence refusée arrête
  l'installation.

Le choix par défaut : Paramètres → État de l'ordinateur →
« Installations : Demander à chaque fois / Rapide / Pas à pas »
(« Demander » au départ). Aucun des deux modes ne passe outre la fenêtre
d'administrateur de Windows (UAC), ni une connexion dans le navigateur
(Claude, GitHub) : le cockpit le dit avant de commencer. Chaque
installation reste dans `logs/installations.jsonl` — le mode, ce qui a été
installé, chaque licence acceptée.

**GitHub — toujours d'accord** (1.12). Le Product Owner travaille sur les
mêmes applications depuis deux ordinateurs, jamais en même temps. Le
cockpit récupère chaque dépôt (`git fetch`) et dit où il en est :
**à jour** ; **en retard** (GitHub a des commits que cet ordinateur n'a
pas) ; **non envoyé** (cet ordinateur a des commits que GitHub n'a pas) ;
**divergé** (les deux) ; **GitHub injoignable** ; **sans GitHub** (un
dépôt sans dépôt distant). C'est calculé à l'ouverture du cockpit, à
l'ouverture d'une application, avant chaque lancement, après chaque run et
après chaque action git du cockpit — et montré sur la ligne de l'accueil,
et dans la barre du haut de l'application ouverte quand ce n'est pas
« à jour ».
- **Avant chaque lancement** — une commande, « Enregistrer » dans
  Données, le profil de déploiement, une installation ou une mise à jour
  de la chaîne : **en retard**, il récupère (`git pull --ff-only`) puis
  lance ; si git refuse parce qu'il écraserait un fichier non commité, rien
  ne se lance et la page dit lequel. **Divergé** : rien ne se lance,
  « Réconcilier » est proposé. **GitHub injoignable** : il lance, et dit
  que l'état n'est pas vérifié. **Non envoyé** : il envoie d'abord
  (`git push`), puis lance.
- **Après chaque run** : la fin du run dit si GitHub a ses commits ; un
  push de fin de run refusé y est écrit en clair, avec « Envoyer » ou
  « Réconcilier ». **Non envoyé** devient une alerte, sur le tableau de
  bord et sur la ligne, avec **« Envoyer »** ; un push refusé récupère de
  nouveau et montre le nouvel état.
- **« Réconcilier »** (divergé) : `git pull --rebase=merges` — les commits
  d'ici sont rejoués après ceux de GitHub, puis envoyés ; 1.12.1 : chaque
  fusion d'une commande (`Merge /<commande> …`) reste une fusion, avec son
  sujet. Sur un conflit, il
  annule (`git rebase --abort`) : le dépôt revient tel qu'il était, et la
  page dit quels fichiers sont en conflit — une session Claude Code ouverte
  sur l'application le réglera. Refusé tant que des fichiers suivis ont des
  modifications non commitées.
- **« Récupérer »** (1.14), sur la ligne de l'accueil et sur le tableau de
  bord, quand l'application est **en retard** : prendre la version de
  GitHub sans rien lancer — le même `git pull --ff-only` qu'avant un
  lancement, refusé de la même façon (un fichier non commité qu'il
  écraserait est nommé ; **divergé** renvoie à « Réconcilier »), et refusé
  pendant qu'une commande ou un déploiement y tourne. Ensuite, son état
  GitHub et l'état de sa chaîne sont recalculés : le bloc de la chaîne
  montre ce qui vient d'être récupéré — une chaîne installée sur l'autre
  ordinateur, par exemple.
- **« Envoyer mes réponses »**, sur « À répondre » et sur la ligne, quand
  le dossier de la feature a des modifications non commitées : le même
  commit que la prochaine commande ferait — `docs/features/<feature>/`,
  `chore: answers` — puis le push. La commande qui suit ne trouve rien à
  commiter, ce que chacune lit comme normal, et continue.
- **Jamais** de `--force`, de reset, de stash, ni de commit de fusion fait
  par le cockpit ; jamais de demande de mot de passe : un push ou un clone
  refusé faute d'identifiants GitHub le dit.
- **Hors du cockpit**, une commande lancée depuis Claude Code n'a aucune
  de ces vérifications : aucune commande de la chaîne n'a changé.

**« Mettre à jour le cockpit »** (1.14). Le cockpit tourne depuis le dépôt
agent-chain de cet ordinateur, et c'est ce dépôt qu'il installe dans les
applications. Quand le cockpit ou la chaîne change sur l'autre ordinateur,
celui-ci prend la nouvelle version sans terminal :
- **L'état**, en tête de l'écran d'accueil quand il n'est pas « à jour » :
  **« Nouvelle version du cockpit disponible »** — agent-chain en retard
  sur GitHub, vu par une récupération (`git fetch`) au démarrage et à
  l'ouverture de l'écran d'accueil (au plus une par minute) ; ou
  **« Nouvelle version du cockpit récupérée — pas encore en service »** —
  agent-chain a déjà les commits (le pull du démarrage) mais le serveur
  tourne encore sur l'ancien code. Dessous, le sujet de chaque commit que
  ce cockpit n'a pas encore. Paramètres → « Version du cockpit » dit la
  même chose, avec la version et le commit qui tournent.
- **Le bouton « Mettre à jour le cockpit »**, là, dans Paramètres et dans
  le bandeau du démarrage :
  1. refusé tant qu'une commande tourne — ou « Tout mettre à jour », un
     déploiement, une création — et il le dit ;
  2. `git pull --ff-only` dans agent-chain ; refusé, le fichier nommé, si
     git écraserait un fichier non commité ; **divergé** : refusé, et
     « Réconcilier » proposé comme pour une application ;
  3. si `tools/cockpit/requirements.txt` a changé depuis le commit sur
     lequel le serveur a démarré : `python -m pip install --user -r` ce
     fichier ; s'il échoue, tout s'arrête là, avec l'erreur de pip — le
     bouton réessaie ;
  4. le redémarrage, tout seul — voir ci-dessous. La page se recharge
     d'elle-même sur le nouveau serveur.
- **Le redémarrage.** L'ancien serveur choisit un port libre, le port
  d'essai, et démarre le nouveau comme `lancer.bat` le fait (`pythonw
  server.py`, sinon `python server.py`), détaché, sans `--ouvrir`, avec
  `--relais <port d'essai>` et les `--config`, `--stats`, `--journaux` de
  l'ancien. Le nouveau démarre entièrement — imports, `config.json`,
  statistiques — et répond d'abord sur le port d'essai seulement.
  L'ancien interroge ce port (`/api/ping`, un autre pid) jusqu'à
  60 secondes : **pas de réponse**, ou le nouveau s'arrête avant, il
  l'arrête, continue de tourner et dit pourquoi — le code de sortie et la
  fin de ce que le nouveau a écrit (`logs/relais-<port d'essai>.log`). **Une réponse** :
  l'ancien s'arrête, comme « Arrêter le cockpit » ; le nouveau prend le
  port du cockpit dès qu'il est libre (jusqu'à 30 secondes), puis ferme le
  port d'essai. Pendant ce temps la page montre « Redémarrage du
  cockpit… », interroge `/api/ping`, et se recharge dès qu'un autre serveur
  y répond. Aucune commande ne se lance pendant la mise à jour.

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
Sous une question qui porte des lignes `Occurrences:` (les endroits du
texte où la réponse s'appliquera), **« Où dans le texte »** les montre,
repliées : un clic les ouvre. Elles ne font pas partie de la question.
Le défaut proposé est pré-coché : le garder sans remarque laisse
`Answer:` vide, ce que la chaîne lit comme accepté. **Un seul bouton
« Enregistrer »** écrit tout, puis dit pour chaque entrée si elle est
enregistrée ou pourquoi elle ne l'est pas. Les fichiers que le cockpit
ne sait pas lire sont signalés en haut, jamais ignorés.

**Expliquer** (1.19) — sous chaque question, sur l'ordinateur et le
téléphone : une explication courte, en français courant — ce que la
question demande, pourquoi c'est important pour l'utilisateur de
l'application, ce que change chaque option, les mots techniques définis
en une ligne, 150 mots au plus. **Jamais une recommandation** : ni
préférence, ni « en général », ni défaut à choisir — la consigne donnée au
modèle l'interdit (`explain.py`, `INSTRUCTION`), la décision est la vôtre.

- Ce qu'elle lit, et rien d'autre, tout dans la demande : la question, ses
  options et son `Défaut:` — jamais ses lignes `Occurrences:` ; le passage que nomme sa ligne `Block:`, pris
  comme le volet de droite le montre ; les entrées de `## Tranché` de
  `lexique.md` dont les termes sont dans la question ou ses options —
  jamais le fichier entier. Sans bloc trouvé (ou sans ligne `Block:`), elle
  le dit, et explique à partir de la question seule ; la ligne sous
  l'explication dit d'après quoi elle a été faite.
- L'appel est celui de la mesure de 1.17 : le modèle le plus léger, un
  tour, sans outil ni serveur MCP, dans un dossier temporaire à lui. 60 s
  au plus, puis il le dit ; « Annuler » pendant qu'il tourne. Son coût est
  enregistré dans `stats.sqlite`, marqué `kind = 'explication'`
  (« (explication) » dans les Statistiques), son journal
  `logs/<date>-explication.jsonl`. Le seuil de blocage de 1.17 vaut comme
  pour un lancement, « Lancer quand même » compris.
- Gardée par le cockpit pour la question (dans `stats.sqlite`, jamais dans
  le dépôt de l'application) : repliée sous la question une fois lue, un
  appui l'ouvre aussitôt, sans nouvel appel ; « Réexpliquer » la redemande.
  Dès que le fichier de la question change — une réponse écrite dedans
  comprise —, elle est oubliée.

**Le run** — sous son étape, dans « Chaîne » ou « Correction » : la
commande qui tourne, l'agent actif, le texte au fil de l'eau. Une demande
d'autorisation apparaît en bandeau sur tous les écrans : « Autoriser » ou
« Refuser » ; la commande attend votre clic — que la page se rafraîchisse
pendant le clic ne le perd plus (1.12.2). « Arrêter maintenant »
interrompt le tour en cours. « Arrêter au prochain lot » (sur `/8_code`
seulement) écrit `stop.md`, et le cockpit le renomme `stop1.md` à la fin du
run (1.18) ; « Retirer stop.md » reste pour un `stop.md` posé à la main.

**Lots à coder** (1.9.1) — à côté du bouton de l'étape « Coder les lots »,
et dans « Chaîne → Code » : combien de lots `/8_code` code d'affilée, 1 par
défaut, au plus les lots pas encore faits quand le cockpit les connaît. À
1, la commande part telle quelle (`/8_code <feature>`) ; au-dessus, avec
le nombre (`/8_code <feature> 3`). « Arrêter au prochain lot » arrête
alors après le lot en cours.

**Les journaux** (1.9.1) — partout où le chemin du journal d'un run ou
d'un déploiement s'affiche (le flux, « Fin du run », « Derniers runs »,
un run ouvert dans « Statistiques », « Sortie complète »), c'est un lien :
il ouvre son dossier sur cet ordinateur, le fichier sélectionné.

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

## Sur le téléphone (1.13)

La même page, sous 720 px de large : le téléphone pilote, l'ordinateur
construit, déploie et règle. Au-dessus de 720 px, rien ne change.

- **Cinq onglets en bas**, sous le pouce, à la place du menu de côté :
  Tableau, À répondre (avec son nombre), Chaîne (un point quand une
  commande tourne, rouge quand une autorisation attend), Données, Plus.
  La barre du haut garde l'application, la fonctionnalité — un toucher la
  change — et la commande qui tourne.
- **« Plus »** : changer d'application ou de fonctionnalité, l'état GitHub
  et le mode, puis une ligne « Sur l'ordinateur » par écran qui y reste.
- **Sur le téléphone** : la liste des applications ; le tableau de bord
  entier, « Envoyer » et « Réconcilier » compris ; « À répondre » entier —
  le document d'une question s'ouvre par « Voir le document », la barre
  « Enregistrer » reste au-dessus des onglets, « Joindre un fichier »
  propose l'appareil photo ou les fichiers ; l'étape proposée se lance
  avec les mêmes confirmations, et quand c'est `/8_code`, « Lots à coder »
  est à côté du bouton ; un run se suit dans « Chaîne », avec « Arrêter au
  prochain lot » et « Arrêter maintenant » ; une autorisation monte du bas
  de l'écran, par-dessus n'importe quel écran ; « Données » : la liste,
  l'aperçu sous elle, « Joindre » ; « Chaîne » en lecture.
- **Sur l'ordinateur** — et le téléphone le dit à leur place : Correction,
  Déploiement, Statistiques, Paramètres, Nouvelle application, ajouter une
  application, installer ou mettre à jour la chaîne, Renommer et Retirer
  de la liste, les audits, et chaque « Lancer » de Chaîne. Les questions
  et les blocages d'une correction passent par « À répondre », et le
  tableau de bord propose ses étapes ; écrire sa bug-list et en ouvrir
  une nouvelle restent sur l'ordinateur.
- **L'écran d'accueil du téléphone** : la page a un manifeste et ses
  icônes, pour s'y ajouter ; atteinte par l'adresse Tailscale (1.15), elle
  a aussi son service worker — elle s'installe comme une application — et
  les notifications. Voir « Téléphone » juste en dessous.

## Téléphone (1.15)

Le cockpit tourne sur cet ordinateur ; Tailscale relie l'ordinateur et le
téléphone en réseau privé, et `tailscale serve` présente le cockpit en
HTTPS à l'adresse Tailscale de l'ordinateur. Rien n'est ouvert sur
internet : seuls les appareils de votre compte Tailscale voient cette
adresse. Le serveur du cockpit, lui, n'écoute toujours que sur
`127.0.0.1` ; c'est Tailscale qui lui transmet les demandes du téléphone.

**Une fois, pour mettre en place**

1. Sur l'ordinateur : installer Tailscale (tailscale.com/download), et se
   connecter avec son compte.
2. Sur le téléphone : installer l'application Tailscale (App Store ou
   Play Store), se connecter avec **le même compte**, et la laisser
   connectée.
3. Dans la console Tailscale (login.tailscale.com → DNS) : MagicDNS
   activé — il l'est d'office — et « HTTPS Certificates » activé. Si ce
   n'est pas fait, la commande de l'étape 4 le propose elle-même.
4. Sur l'ordinateur, dans un terminal (PowerShell), le cockpit lancé :

       tailscale serve --bg 8765

   `8765` est le port du cockpit (celui de `--port` si vous en avez donné
   un autre). `--bg` laisse le service en place, même après un redémarrage
   de l'ordinateur, jusqu'à `tailscale serve reset`. L'aide de la commande
   le dit ainsi : « Expose an HTTP server running at 127.0.0.1:3000 in the
   background: `tailscale serve --bg 3000` » — `tailscale serve --help`
   l'affiche pour la version installée.
5. L'adresse : `tailscale serve status` la montre, de la forme
   `https://<ordinateur>.<tailnet>.ts.net`, suivie de
   `proxy http://127.0.0.1:8765`.
6. Dans le cockpit, sur l'ordinateur : Paramètres → **« Accès depuis le
   téléphone »** — coller l'adresse, choisir un **code d'accès** (au moins
   6 caractères), cocher, « Enregistrer ».

**Sur le téléphone**

- Ouvrir l'adresse dans le navigateur, Tailscale connecté. Le cockpit
  demande le code, **une seule fois** : il pose ensuite un cookie valable
  400 jours, que seul ce navigateur garde.
- L'ajouter à l'écran d'accueil — iPhone : Safari → Partager → « Sur
  l'écran d'accueil » ; Android : menu → « Installer l'application ».
- Paramètres → Notifications → **« Sur ce téléphone »** → « Activer sur ce
  téléphone », puis « Essayer ». Sur iPhone, les notifications ne viennent
  qu'au cockpit ouvert depuis l'écran d'accueil (iOS 16.4 ou plus récent).
  Elles arrivent même le cockpit fermé sur le téléphone : une autorisation
  qui attend ; un run qui se termine — fini, arrêté ou en erreur — ; un run
  qui se termine en vous laissant des questions ou un blocage. Un toucher
  ouvre le cockpit sur l'écran concerné : l'étape du run, ou « À répondre ».
  Les notifications du navigateur de l'ordinateur (1.5) ne changent pas.

**Ce qui protège l'accès**

- Une demande venue par Tailscale n'est acceptée que si son adresse est
  celle de Paramètres, le réglage coché ; puis seulement avec le cookie
  que donne le code. Celles de l'ordinateur ne demandent jamais de code.
- Le code est gardé chiffré (PBKDF2) dans `config.json`, jamais réaffiché ;
  en taper un nouveau le remplace.
- Cinq codes faux de suite : l'accès depuis le téléphone est refusé quinze
  minutes, même au bon code, et l'ordinateur l'affiche en bandeau rouge.
- **« Déconnecter le téléphone »** (Paramètres) : tous les cookies donnés ne
  valent plus rien, et les abonnements aux notifications sont retirés —
  le téléphone redemandera le code.
- L'adresse, le code et la déconnexion se règlent sur l'ordinateur
  seulement ; le téléphone n'y a pas accès.

**Arrêter** : décocher « Accès depuis le téléphone » ferme l'accès tout de
suite ; `tailscale serve reset` retire le service de Tailscale.


## Ce que le cockpit ne fait jamais

- Il ne lance aucune commande que vous n'avez pas cliquée — un programme
  du pilote automatique (1.18) compte pour un clic : il lance les étapes
  proposées, dans ses bornes, et s'arrête dès qu'on a besoin de vous. Son seul appel
  à Claude de lui-même est la mesure de la consommation (1.17) : une
  phrase, le modèle le plus léger, sans outil, dans un dossier à lui.
- Une enquête (1.21) ne fait que lire, et c'est le cockpit qui l'impose ;
  il ne lance jamais une correction de la chaîne ou du cockpit — son prompt
  passe par la conversation de conception —, et n'écrit une entrée de bug
  qu'une fois qu'elle l'a confirmée.
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
  le profil », `.claude/deploy.json`, son commit et son push ; 1.21, les
  rapports d'enquête et leurs prompts dans `docs/enquetes/`, et l'entrée de
  bug que vous avez confirmée. Tout le reste est en lecture.
- « Déploiement » ne lance que les commandes du profil, quand vous
  cliquez ; il n'installe, ne lance, n'associe ni ne connecte rien sur un
  appareil sans un clic. Les noms de vos appareils restent dans
  `config.json`, jamais dans l'application.
- Ajouter, renommer ou retirer une application ne change que sa liste,
  dans `config.json` : aucun fichier de son dossier n'est écrit — Ajouter
  règle seulement `core.longpaths=true` dans sa configuration git (1.12).
- Avec GitHub (1.12), il récupère, envoie, et réconcilie par un rebase
  qui garde les fusions déjà faites (1.12.1) — jamais de `--force`, de
  reset, de stash, ni de commit de fusion à lui ; « Envoyer mes réponses » ne commite que le dossier de la feature.
- « Mettre à jour le cockpit » (1.14) ne fait qu'un `git pull --ff-only`
  dans agent-chain, `pip install --user` quand ses dépendances ont changé,
  et le redémarrage ; un nouveau serveur qui ne répond pas est arrêté, et
  l'ancien continue.
- « Nouvelle application » n'écrit que dans le dossier qu'elle crée, neuf
  ou vide, et ne le supprime jamais ; elle ne force jamais un dépôt
  distant qui contient déjà des commits. Elle ne reprend qu'une création
  qu'elle a commencée : une application existante n'est jamais touchée.
- Il ne touche jamais au travail non commité d'une application — sauf
  « Envoyer mes réponses », qui commite le dossier de la feature comme la
  prochaine commande l'aurait fait.
- Après chaque écriture, il relit le fichier avec le test de la commande ;
  si la commande le lirait encore comme sans réponse, il annule l'écriture
  et vous le dit.
- Il n'accorde aucune autorisation tout seul, et n'accepte aucune licence
  sans votre accord — donné d'avance (« Rapide ») ou une par une (« Pas à
  pas ») (1.16).
- Il ne vous déconnecte jamais de Claude Code ni de GitHub ; « État de
  l'ordinateur » ne fait que lire, sauf `core.longpaths`, qu'il règle, et
  ce que vous réparez d'un clic (1.16).
- Il n'écoute que sur cette machine (`127.0.0.1`). Le téléphone (1.15)
  passe par Tailscale, à l'adresse et avec le code que vous avez choisis ;
  rien n'est ouvert sur internet.

S'il tombe en panne, rien n'est perdu : toutes les commandes se lancent
toujours depuis Claude Code, et les fichiers sont les mêmes.

## Tests

    pip install -r requirements-tests.txt

Deux façons de les lancer, depuis `tools/cockpit/` :

- **La suite rapide** — tout, sauf les tests qui pilotent le navigateur
  sans fenêtre (Edge par Playwright). Pendant un changement, après
  chaque étape :

      python -m pytest -n 8 --dist worksteal -m "not navigateur"

- **La suite complète** — tout, navigateur compris. À la fin d'une
  version, avant de la livrer :

      python -m pytest -n 8 --dist worksteal

`-n 8` lance huit processus de test à la fois (pytest-xdist) : sur cet
ordinateur, c'est le meilleur réglage mesuré — à 4 la suite prend plus
longtemps, à 12 aussi, chaque test attendant alors ses processus git.
Chaque test garde son propre dossier temporaire et ses propres ports ;
aucun n'attend la fin d'un autre. Un test qui pilote le navigateur porte
la marque `navigateur`, posée d'elle-même (`tests/conftest.py`).

Les dépôts git de test (« GitHub » et les deux ordinateurs) sont construits
une fois par lancement, puis copiés pour chaque test (`tests/copies.py`) :
un test pousse vers sa propre copie, jamais vers le modèle, et la suite
échoue si un modèle a changé.
