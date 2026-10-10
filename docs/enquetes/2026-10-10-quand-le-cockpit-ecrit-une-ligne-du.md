# Enquête — Quand le cockpit écrit une ligne du journal de cycle, quel nom d'ordinateur y met-il, et d'où vient ce nom ?

- Date : 10/10/2026 à 21:43
- Ordinateur : ordinateur
- Cible : la chaîne et le cockpit
- Modèle : claude-opus-5-5 (celui des commandes de la chaîne)
- Coût : 165 603 tokens lus · 4 135 écrits · 46 s · ≈ 0,29 $ en équivalent API

Écrite par le cockpit. L'enquête a lu, rien de plus : aucun fichier modifié, aucune commande autre que de lecture. Aucun agent de la chaîne ne lit ce dossier.

## La question

Quand le cockpit écrit une ligne du journal de cycle, quel nom d'ordinateur y met-il, et d'où vient ce nom ?

## La réponse

**En bref**

Le cockpit écrit le surnom que vous avez donné à l'ordinateur dans Paramètres → « Cet ordinateur » (par exemple « travail » ou « perso »). Si vous n'en avez pas donné, il écrit simplement « ordinateur ». Il n'écrit jamais le vrai nom de la machine sur le réseau, pour que ce nom ne se retrouve pas sur GitHub.

**Ce que j'ai trouvé**

- **Une colonne pour l'ordinateur.** Le journal de cycle est un tableau, et sa deuxième colonne s'appelle « Ordinateur » (`tools/cockpit/journal.py:42-43`). Le fichier est enregistré dans le dépôt de l'application, puis envoyé sur GitHub (`tools/cockpit/journal.py:5-8`).
- **Ce qui est écrit quand une commande se termine.** À la fin d'une commande, le cockpit écrit sa ligne avec `computer=state.computer_label`, c'est-à-dire le nom retenu pour cet ordinateur (`tools/cockpit/server.py:1803-1804`). La fonction qui fabrique la ligne met ce nom dans la colonne, et met « ordinateur » s'il manque (`tools/cockpit/journal.py:325`, `tools/cockpit/journal.py:84`).
- **D'où vient ce nom.** C'est le surnom choisi dans Paramètres → « Cet ordinateur ». Sans surnom, c'est « ordinateur » (`tools/cockpit/state.py:397-400`, `tools/cockpit/state.py:49`). Le code le dit en toutes lettres : « jamais son nom réseau, qui serait publié sur GitHub » (`tools/cockpit/journal.py:81-83`, `tools/cockpit/state.py:389-391`).
- **Où le surnom est gardé.** Dans `config.json`, le fichier de réglages du cockpit sur cet ordinateur (`tools/cockpit/state.py:43`, `tools/cockpit/state.py:409`). Ce fichier n'est pas envoyé dans git (`.gitignore:4`), donc chaque ordinateur garde le sien.
- **Les règles du surnom.** 40 caractères au plus, et pas de « | », parce que ce signe sert à séparer les colonnes du tableau (`tools/cockpit/state.py:402-407`).
- **Quand on vous le demande.** Une seule fois : au premier lancement d'une commande qui écrit dans un dépôt alors qu'aucun surnom n'est donné (`tools/cockpit/server.py:2021-2029`, `tools/cockpit/server.py:1719`). Si vous répondez « Plus tard », c'est « ordinateur » qui est écrit (`tools/cockpit/server.py:2032-2033`). Le mode d'emploi le confirme et précise que les lignes déjà écrites ne sont pas modifiées après coup (`tools/cockpit/LISEZMOI.md:635-640`).
- **Les lignes reconstituées du passé (avant la version 1.20).**
  - Quand la ligne est reconstituée à partir des statistiques de cet ordinateur, elle prend le même surnom (`tools/cockpit/server.py:1951`, `tools/cockpit/journal.py:834`, `tools/cockpit/journal.py:878`).
  - Quand elle est reconstituée à partir de l'historique git seul, la colonne indique « inconnu » (`tools/cockpit/journal.py:925`).
- **Aucune lecture du nom réseau.** J'ai cherché dans le code du cockpit les moyens habituels de lire le nom réseau de la machine. Je n'en ai trouvé aucun pour le journal : les seuls « hostname » trouvés concernent des adresses web, dans `tools/cockpit/phone.py:51-83`.
- **Sur cet ordinateur.** Le fichier `tools/cockpit/config.json` ne contient pas de réglage « computer ». Aucun surnom n'y est donc enregistré pour l'instant, et une nouvelle ligne porterait « ordinateur ».

**Ce que je n'ai pas pu établir**

- **Ce que faisait la version 1.20.** Je n'ai pas pu vérifier si, avant la version 1.21, le cockpit écrivait le nom réseau de la machine. Le seul indice est le commentaire « 1.21 » dans le code, mais ce n'est pas une preuve. Pour comparer, il faudrait lire le contenu des anciennes versions dans l'historique git, et les outils dont je dispose ici ne me permettent pas de lire cet historique.
- **Les journaux déjà publiés.** Pour la même raison, je ne sais pas si des lignes déjà écrites contiennent un nom réseau. Elles se trouvent dans les dépôts des applications, pas dans ce dossier.

**Ce que je conseille d'en faire**

**Enquêter plus loin** : ouvrir les fichiers `journal.md` déjà écrits dans les dépôts des applications et regarder la colonne « Ordinateur ». Comme les lignes déjà écrites ne sont jamais modifiées, un nom réseau écrit avant la 1.21 y serait toujours visible sur GitHub.
