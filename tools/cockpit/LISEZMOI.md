# Cockpit de la chaîne

Une page locale pour répondre aux questions et aux fichiers de blocage,
voir la prochaine étape, et lancer les commandes — sans ouvrir les
fichiers à la main.

## Installer

Une fois, avec Python 3.12 :

    cd tools\cockpit
    pip install -r requirements.txt

## Lancer

Double-cliquer sur **`lancer.bat`**. Le serveur démarre et le navigateur
s'ouvre sur `http://127.0.0.1:8765/`. Pour l'arrêter : fermer la fenêtre
noire, ou `Ctrl+C` dedans.

Sans le `.bat` : `python server.py --ouvrir`.

## Au démarrage

- **Dossier de l'application** : « Parcourir… » ouvre la fenêtre de choix
  de Windows ; si elle ne s'ouvre pas, coller le chemin dans le champ.
- **Feature** : une feature de `docs/features/`. Ses corrections
  `bugfix-NN/` sont sous « Correction », plus ici.
- **Récents** : les dernières paires. Au lancement suivant, la dernière
  paire s'ouvre directement ; « Changer d'application » revient ici.

## Les écrans

**Où on en est ?** — le bouton de la barre du haut relit le dossier et
revérifie la dernière ligne `Next:`. Le cockpit le fait aussi tout seul à
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

**Correction** — les `bugfix-NN/` de la feature, le plus récent d'abord,
chacun en chaîne de correction. Seul le plus haut se lance : les
commandes agissent sur lui. « Nouvelle correction » crée le `bugfix-NN/`
suivant et son `bug-list.md` vide, rien d'autre, et l'ouvre pour l'écrire
ici, tant que le diagnostic ne l'a pas lu.

**À répondre** — toutes les questions ouvertes et tous les blocages qui
vous attendent, dans un seul formulaire :
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

Fermer l'onglet n'arrête pas la commande ; rouvrir la page la retrouve.

## Ce que le cockpit ne fait jamais

- Il ne lance aucune commande que vous n'avez pas cliquée.
- Il ne remplace la ligne `Next:` que quand les fichiers la contredisent,
  et il le dit ; sa proposition porte toujours « déduite du dossier ».
  Il ne saute jamais une étape bloquée ou inconnue.
- Le relevé du dossier ne fait que lire : aucun appel à Claude, aucune
  commande git, aucune écriture.
- Il n'écrit qu'où vous écrivez déjà : les champs `Answer:`, les
  `## Decision`, `## Décision du Product Owner` dans
  `code/redecoupage.md`, `stop.md`, et le `bug-list.md` d'une nouvelle
  correction. Tout le reste est en lecture.
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
