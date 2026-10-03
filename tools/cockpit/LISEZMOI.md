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
- **Dossier de travail** : une feature de `docs/features/`, ou l'un de ses
  `bugfix-NN/`.
- **Récents** : les dernières paires. Au lancement suivant, la dernière
  paire s'ouvre directement ; « Changer de dossier » revient ici.

## L'écran principal

**Prochaine étape** — ce que le dernier relais demande, en clair.
Si c'est une commande, son bouton est en surbrillance, l'argument
rempli : un clic la lance. Sinon, le texte seul. Dessous, toutes les
commandes, chacune avec son argument modifiable ; lancer une commande
que le relais n'a pas nommée demande une confirmation. Sans relais, rien
n'est en surbrillance.

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

**Run en cours** — la commande qui tourne, l'agent actif, le texte au fil
de l'eau. Une demande d'autorisation apparaît en carte : « Autoriser » ou
« Refuser » ; la commande attend votre clic. « Arrêter maintenant »
interrompt le tour en cours. « Arrêter au prochain lot » (sur `/8_code`
seulement) écrit `stop.md` ; « Retirer stop.md » le renomme `stop1.md`.

Fermer l'onglet n'arrête pas la commande ; rouvrir la page la retrouve.

## Ce que le cockpit ne fait jamais

- Il ne lance aucune commande que vous n'avez pas cliquée.
- Il ne décide jamais de la prochaine étape : il lit la ligne `Next:` du
  relais. Sans elle, il dit que la prochaine étape est inconnue.
- Il n'écrit qu'où vous écrivez déjà : les champs `Answer:`, les
  `## Decision`, `## Décision du Product Owner` dans
  `code/redecoupage.md`, et `stop.md`. Tout le reste est en lecture.
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
