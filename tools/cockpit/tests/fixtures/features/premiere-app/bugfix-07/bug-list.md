- ## D1 — Le chronomètre ne tourne pas

  **Ce qui est constaté.** Une course lancée est bien créée en base —
  `id=1`, `origin=RECORDED`, `completion=INCOMPLETE`,
  `currentSegmentIndex=1`, `currentSegmentOpenedAt=367663073`, ses 30
  segments présents avec `durationMs` à `NULL`. Mais `lastKnownNow`
  n'avance jamais : aucun tick n'est émis pour la durée de vie de la
  course. Le temps écoulé, l'allure et tout ce qui en dérive restent
  figés à leur valeur initiale.

  **Pourquoi ce défaut existe.** `raceTicker.start()` n'apparaît qu'à un
  seul endroit de tout le module, vérifié par grep sur
  `app-wear/src/main` : `ExerciseSessionManager.kt:89`, à l'intérieur de
  `registerReadingsAndStartTicker()`. Cette fonction n'est appelée que
  depuis `ExerciseSessionManager.open()`, et seulement sur les issues
  `Started` ou `AlreadyOwned` (`:69-79`). Comme `startExerciseSession()`
  renvoie `Failed` — voir D2 — la fonction n'est jamais atteinte, et le
  ticker ne démarre pas.

  Le défaut n'est pas l'ordre des appels, c'est le couplage lui-même. Le
  chronomètre a été rangé dans le chemin de la session d'exercice parce
  que les deux démarrent au même moment dans le cas nominal, et rien
  dans le découpage n'a distingué « ce qui mesure le temps » de « ce qui
  lit les capteurs ». Structurellement, le chrono partage désormais le
  point de démarrage et le mode d'échec de la session capteur.

  C'est une violation directe du cadrage, qui pose que le chronomètre ne
  dépend d'aucun capteur, qu'une donnée capteur manquante est un cas
  nominal, et que le chrono ne se replie jamais. Aucune règle numérotée
  des conventions ne le couvre — c'est une règle produit, et aucun
  critère d'acceptation n'observait le cas « session refusée, course
  chronométrée quand même ».

  **Comment le corriger.** Sortir `raceTicker.start()` de
  `registerReadingsAndStartTicker()` et le rattacher au démarrage de
  l'horloge de course, c'est-à-dire au même endroit que
  `recordingRepository.startClock(...)` dans
  `RaceLaunchController.retryAndLaunch` — qui, lui, démarre déjà
  « regardless of that retry's outcome » et respecte donc le cadrage.
  Symétriquement, l'arrêt du ticker suit la fin de course, jamais la
  fermeture de session.

  Le ticker doit également démarrer sur le chemin de reprise à froid,
  qui court-circuite la préparation — voir D6.

  Un test doit couvrir le cas nominal du cadrage : session d'exercice en
  échec, course lancée, temps écoulé qui progresse.

- ## D2 — `ACTIVITY_RECOGNITION` n'est déclarée nulle part

  **Ce qui est constaté.** Le log système de la montre porte, deux fois,
  juste après la liaison au service Health Services :

  ```
  W/WHS_PermissionPolicy: Permissions verification failed
  W/WHS_PermissionPolicy: java.lang.SecurityException:
    com.mgilli.hyroxtracker doesn't have permission to access
    android.permission.ACTIVITY_RECOGNITION
  ```

  En amont, Health Services retire un à un les types de données :
  `I/DOPermission: ACTIVITY_RECOGNITION permission not satisfied for
  whs.lap.distance.m`, puis `whs.workout.speed.current.mps`, et une
  quinzaine d'autres.

  **Pourquoi ce défaut existe.** `android.permission.ACTIVITY_RECOGNITION`
  n'existe nulle part dans le dépôt — vérifié par grep sur les `*.xml`,
  les `*.kt` et les `*.md`. Ni le manifeste, ni le code, ni la
  documentation ne la mentionnent. C'est pourtant la permission que
  Health Services exige pour `ExerciseClient` ; sans elle,
  `startExerciseAsync()` est refusé.

  Le manifeste de `:app-wear` déclare `VIBRATE`, `BLUETOOTH_CONNECT`,
  `BODY_SENSORS` avec `maxSdkVersion="35"`, et
  `health.READ_HEART_RATE`. Ces quatre-là sont corrects : `dumpsys`
  confirme que `READ_HEART_RATE` est accordée, et l'absence de
  `BODY_SENSORS` de la liste est le comportement attendu sur SDK 36 —
  `sensorPermissionFor()` bascule bien sur `READ_HEART_RATE` au-delà de
  l'API 36.

  La permission manquante est donc la seule, et elle manque parce que le
  manifeste n'est produit par aucun lot : il ne figure ni dans une
  signature, ni dans un critère d'acceptation. C'est le même défaut de
  fond que les points d'entrée absents des deux modules — un artefact
  nécessaire au fonctionnement qui n'est ni un symbole Kotlin ni un
  critère observable, et que la chaîne ne contrôle nulle part.

  **Comment le corriger.** Déclarer `ACTIVITY_RECOGNITION` au manifeste
  de `:app-wear`, et intégrer sa demande à l'exécution au parcours
  d'autorisation existant — `SensorPermissionManager`,
  `SensorPermissionScreen`, `SensorPermissionSystemImpl` — sans créer un
  second parcours en parallèle. La permission est de niveau dangereux :
  la déclarer ne suffit pas, elle doit être accordée par l'utilisatrice.

  🔴 **Ne pas corriger ce défaut seul.** Il masque actuellement D3 et
  D4 : dès que la permission passera, la souscription sera atteinte,
  demandera des types invalides, et gèlera le sas. Les trois se
  corrigent ensemble.

- ## D3 — Les capacités sont lues sur le mauvais client

  **Ce qui est constaté.** `ExerciseSessionManager.kt:121` appelle
  `readingsSource.register(system.availableDataTypes())`.
  `availableDataTypes()` lit les capacités d'**`ExerciseClient`**
  (`ExerciseSessionSystemImpl.kt:87`), tandis que
  `SensorReadingsSource` enregistre ses callbacks sur
  **`MeasureClient`** (`SensorModule.kt:37`). Deux clients distincts,
  deux jeux de capacités distincts.

  `MeasureClient.getCapabilitiesAsync()` n'est appelé nulle part —
  vérifié par grep sur tout `app-wear/src/main`. `DataType.DISTANCE` et
  `DataType.SPEED`, qui ne sont pas des types mesurables par
  `MeasureClient`, sont demandés quand même
  (`SensorReadingsSource.kt:117-122`).

  **Pourquoi ce défaut existe.** L'architecture répartit la lecture des
  capteurs entre deux clients de Health Services, et le code traite les
  deux comme s'ils n'en formaient qu'un. La vérification préalable
  existe, elle porte simplement sur le mauvais objet : on interroge A
  pour s'autoriser un appel sur B.

  C'est une violation de R33, seconde phrase : *« ce dont un appel a
  besoin pour tourner — une permission, le créneau de session, un type
  de donnée, le lien entre appareils — est vérifié avant, pas rattrapé
  après »*. La forme du geste est là, l'objet est faux — ce qui est
  précisément le genre d'erreur qu'une relecture de conformité valide,
  puisqu'un appel à `getCapabilitiesAsync()` est bien présent avant le
  `register`.

  Aucun test ne pouvait l'attraper : les deux clients sont remplacés par
  des doubles en test, et un double ne distingue pas les capacités de
  l'un de celles de l'autre.

  **Comment le corriger.** Faire porter la vérification sur le client
  qui exécute : `MeasureClient.getCapabilitiesAsync()` avant tout
  `registerMeasureCallback`, et ne demander que les types que ce client
  déclare mesurables. La fréquence cardiaque en fait partie ; la
  distance et la vitesse relèvent de `ExerciseClient` et sont livrées
  par le flux de la session, pas par une mesure ponctuelle.

  Cela implique de séparer les deux chemins de données : ce qui vient de
  la session d'exercice, et ce qui vient d'une mesure ponctuelle. Le
  code les mélange aujourd'hui derrière la seule
  `SensorReadingsSource`.

- ## D4 — `registerOne()` peut suspendre sans fin

  **Ce qui est constaté.** `SensorReadingsSource.registerOne()`
  (`:87-110`) est un `suspendCancellableCoroutine` autour de
  `registerMeasureCallback`. La coroutine ne reprend que sur
  `onRegistered` ou `onRegistrationFailed`. Si la plateforme n'appelle
  ni l'un ni l'autre — le cas documenté d'un type non mesurable par ce
  client — l'attente est infinie.

  `register()` boucle en séquence sur les types (`:59-63`), donc **un
  seul type muet gèle toute la fonction**, donc `open()`, donc
  `openPreparation()`, donc `PreparationViewModel.uiState` reste `null`
  pour la durée de vie du ViewModel.

  **Pourquoi ce défaut existe.** R19 exige que toute attente atteignable
  depuis une frontière publique porte un timeout. Le rapport
  d'investigation générale a mesuré la conformité à cette règle :
  **zéro sur vingt-quatre**. Aucun `await()` du dépôt n'en porte, et les
  deux seuls `withTimeoutOrNull` du projet bornent des lectures
  internes, pas des appels sortants.

  Ce n'est donc pas un oubli isolé mais une règle qui n'a jamais produit
  le moindre effet. Elle ne porte aucune mention *« Checked by review »*
  et se présente comme mécanisable, alors qu'aucun outil de R65 ne la
  vérifie — ni lint, ni detekt s'il était installé.

  🔴 **Ce chemin n'est pas atteint aujourd'hui**, uniquement parce que
  l'échec de D2 survient plus tôt et empêche d'y arriver. Il le sera dès
  que la permission sera déclarée. Corriger D2 sans D3 et D4 remplace un
  écran vide par un gel complet — un état strictement pire, puisque
  l'application ne répond plus du tout.

  **Comment le corriger.** Borner l'attente de `registerOne()` par un
  timeout, et traiter le dépassement comme un échec d'enregistrement de
  ce type : le type est écarté, les autres continuent d'être demandés,
  et l'échec est journalisé.

  Le même traitement s'impose sur les deux autres attentes non bornées
  identifiées : les `deferred.await()` des systèmes de permission, où un
  dialogue jamais répondu — activité détruite avant le callback —
  suspend la coroutine pour toute la vie du processus.

  Le balayage complet des 24 attentes est un chantier distinct : voir
  D11.

- ## D5 — `MainRacePageScreen` n'a aucun plancher de rendu

  **Ce qui est constaté.** L'écran principal de course s'affiche
  entièrement noir. L'application ne plante pas : la fenêtre fait
  480 × 480, une frame est rendue, `reportDrawFinished` passe, le focus
  arrive. L'écran est composé, il ne contient rien.

  **Pourquoi ce défaut existe.** `MainRacePageScreen` (`:58-96`) est un
  `ScalingLazyColumn` sur `DesignTokens.Color.screenBlack` avec quatre
  items, tous conditionnels. Une course démarre au segment 1, et
  `SegmentBlueprint.typeAt(1)` donne `(1-1) % 4 == 0` → **RUN**. Dans
  `computeState()`, sur un RUN sans capteur ni référence :

  | Item | Valeur | Rendu |
  |---|---|---|
  | `stationLabel` | `null` — codé en dur, un RUN n'a pas de libellé | rien |
  | `top` | `Hidden` — `referenceRace == null` | rien |
  | `center` | `Pace(Fallback, None)` → `sensorText` rend `null` | rien |
  | `heartRate` | `Fallback` → `sensorText` rend `null` | rien |

  Quatre `?.let` sautés, sur un fond noir.

  Chaque repli est correct pris isolément : masquer une valeur absente
  est ce que le cadrage demande. **Aucun critère d'acceptation ne dit ce
  qui se passe quand les quatre se replient en même temps.** Le
  Détailleur écrit un critère par comportement observable ; la
  combinaison de tous les replis n'est le comportement de personne.

  Le segment 1 est le pire cas possible : pour `STATION` et `FINAL`,
  `center` vaut `SegmentElapsed(...)` et affiche toujours un texte ; les
  `ROXZONE` affichent `TransitionElapsed` et `NextStep`. **Une course
  commence exactement sur le seul type de segment qui peut ne rien
  afficher** — 8 segments sur 30 sont des RUN, dont le premier.

  🔴 **Ce défaut a une cause propre et suffisante.** Même avec des
  capteurs parfaitement fonctionnels, une course lancée sans course de
  référence chargée afficherait un écran vide pendant tout le premier
  segment, jusqu'au premier échantillon de distance. Il est indépendant
  de D1, D2, D3 et D4.

  **Comment le corriger.** Poser un plancher de rendu : aucune
  combinaison d'états ne produit une page vide.

  - Le **nom du segment** est affiché sur tous les types, RUN compris.
    Il ne dépend d'aucun capteur et d'aucune référence.
  - Une allure en `Fallback` s'affiche avec **le repli déjà défini**,
    `—:—`, suivi de son unité — jamais masquée.
  - Une fréquence en `Fallback` s'affiche `—`, l'arc des zones
    entièrement atténué.

  ⚠️ Aucune valeur par défaut chiffrée. Le cadrage interdit de remplacer
  une donnée absente par zéro : une allure `0:00` se lirait comme une
  mesure réelle. Les replis existants de l'annexe des formats sont les
  seuls admis.

  Un test doit composer la page sur un segment RUN sans aucune donnée
  disponible et vérifier qu'au moins le nom du segment et les deux
  replis sont rendus. C'est le cas qu'aucun critère ne couvrait.

- ## D6 — La session capteur n'est jamais rouverte à la reprise

  **Ce qui est constaté.** Après avoir lancé une course, quitté
  l'application et y être revenue, l'écran reste vide indéfiniment. Le
  vide n'est pas transitoire : aucune donnée n'arrivera jamais, quel que
  soit le temps d'attente.

  **Pourquoi ce défaut existe.** `ExerciseSessionManager.open()` n'est
  appelé que depuis `RaceLaunchController`, donc uniquement par le
  chemin de l'écran de préparation. Or l'enregistrement des capteurs et
  le démarrage du ticker sont tous deux à l'intérieur de `open()`, dans
  `registerReadingsAndStartTicker()`.

  Le chemin de reprise à froid — initialiseur paresseux de
  `WatchRaceNavigator` (`:47-63`), `raceInProgress()` vrai, `current`
  écrit directement à `MAIN` — **court-circuite entièrement
  `openPreparation()`**. Aucune session Health Services n'est ouverte,
  aucun capteur enregistré, aucun tick émis.

  La décision produit sur `PreparationState.Resuming` est pourtant
  correctement appliquée : `PreparationViewModel.applyState()`
  (`:180-182`) fait `navigator.launchRace()` sans afficher d'écran, ce
  qui est exactement ce qui avait été décidé. Le défaut n'est pas là.
  Il est dans le fait que la reprise à froid n'emprunte même pas ce
  chemin : elle écrit `MAIN` avant que `PreparationViewModel` n'existe.

  Autrement dit, il y a **deux chemins de reprise** — celui qui passe
  par la préparation et rouvre la session, et celui qui va directement à
  `MAIN` et ne rouvre rien — et un seul a été traité.

  **Comment le corriger.** Rattacher l'ouverture de la session à
  l'existence d'une course en cours, et non au passage par un écran. Le
  chemin qui écrit `MAIN` directement doit rouvrir la session comme le
  fait `RaceLaunchController.reopenOrphanedSession()`, qui existe déjà
  et journalise correctement chaque issue.

  Une fois D1 corrigé, le ticker ne dépendra plus de la session ; le
  chrono repartira donc à la reprise même si la session échoue. Mais les
  capteurs, eux, resteront muets tant que ce défaut-ci n'est pas traité.

- ## D7 — Sept échecs avalés sans une ligne de journal

  **Ce qui est constaté.** L'échec de `startExerciseAsync()` — une
  `SecurityException` nommant explicitement la permission manquante —
  est capturé et transformé en `Failed` sans qu'aucune trace ne soit
  écrite. Le buffer `crash` de la montre est vide et le processus a
  survécu : la preuve que l'exception a bien été avalée là.

  Le message existe côté système, sous le tag `WHS_PermissionPolicy`.
  Il est donc invisible à qui filtre le journal sur sa propre
  application — ce qui est le geste normal de diagnostic.

  **Pourquoi ce défaut existe.** Sept sites avalent un échec sans le
  journaliser :

  | Fichier:ligne | Ce qui est perdu |
  |---|---|
  | `ExerciseSessionSystemImpl.kt:61-63` | échec de démarrage de session |
  | `ExerciseSessionSystemImpl.kt:69-71` | échec de fin de session |
  | `ExerciseSessionSystemImpl.kt:81-83` | échec de mode de livraison |
  | `SensorReadingsSource.kt:77-79` | échec de désinscription |
  | `SensorReadingsSource.kt:57-65` | `register()` rend `false`, jamais journalisé |
  | `ExerciseSessionManager.kt:121` | le booléen de `register()` est jeté sans être lu |
  | `RaceLaunchController.kt:97-103` | `Failed` → `OpenFailed`, sans log |

  R79 exige qu'un échec qu'un appelant ne peut ni porter dans un état
  qu'il possède, ni propager à son propre appelant, soit écrit au
  journal au niveau ERROR, en nommant l'opération et la faute. R34 exige
  qu'un appelant recevant un échec agisse dessus — lire une issue et ne
  rien changer n'est pas agir.

  Le plus instructif : `RaceLaunchController` journalise correctement à
  `:78` et `:92`, dans `reconcileResumedSession()` et
  `reopenOrphanedSession()`, en citant R79. **La règle est connue,
  comprise et appliquée dans le même fichier** — elle manque précisément
  sur le chemin nominal. Ce n'est pas une doctrine, c'est un oubli
  répété là où l'attention se relâche.

  Aucun outil ne vérifie R79, R34 ni R30. Le rapport d'investigation
  générale a compté neuf appelants qui lisent un échec et ne font rien.

  **Comment le corriger.** Journaliser en ERROR sur les sept sites, en
  nommant l'opération et la faute. Faire lire le booléen rendu par
  `readingsSource.register()` plutôt que le jeter.

  ⚠️ R54 interdit qu'une donnée attachée à une personne apparaisse dans
  un message de journal — fréquence, zone, durée, allure, nom ou date de
  course. Un log d'échec nomme l'opération et l'exception, jamais la
  valeur.

  Cette correction est celle qui aurait fait tenir toute l'investigation
  dans une seule ligne : un `Log.e` à
  `ExerciseSessionSystemImpl.kt:61-63` aurait mis la `SecurityException`
  et le nom de la permission sous les yeux, à la seconde où l'on entrait
  dans le sas.

- ## D8 — Une session morte est indiscernable d'un capteur lent

  **Ce qui est constaté.** L'écran du sas affiche le libellé
  « Fréquence cardiaque » sans aucune valeur, indéfiniment. Rien
  n'indique que la session d'exercice a échoué : l'écran est
  rigoureusement identique à ce qu'il montrerait si la session avait
  réussi et que le capteur n'avait simplement pas encore parlé.

  **Pourquoi ce défaut existe.** Trois mécanismes se cumulent.

  `PreparationUiState` déclare `heartRateText: String?` dans **`Ready`
  comme dans `OpenFailed`** (`:13` et `:22`), et
  `PreparationScreen.kt:42-48` rend `OpenFailed` par **le même
  `ReadyContent`** que `Ready`, avec les mêmes libellés. Donc
  `Ready(heartRateText = null)` et `OpenFailed(heartRateText = null)`
  produisent des pixels identiques. L'échec est représenté dans le type
  sans être distinguable à l'écran — ni pour l'utilisatrice, ni pour un
  test. C'est la violation de R87.

  `PreparationViewModel.mutableUiState` part de `null` (`:74`) et
  `PreparationScreen.kt:32` rend `null -> Unit`. « Rien collecté pour
  l'instant » et « la source a échoué en première émission » partagent
  donc le même rendu : le vide. C'est la violation de R88, que R76
  aggrave — un `.catch` ne réabonne pas son amont, une seule émission
  d'échec termine le flow, et `openPreparation()` n'est alors plus
  jamais appelé.

  Enfin `ExerciseSessionOpenResult` distingue bien `DeviceSlotTaken`,
  mais **le refus de permission tombe dans `Failed`**, fourre-tout
  indistinct de toute autre panne. R36 exige qu'un refus d'accès soit un
  état déclaré, jamais une absence silencieuse de données.

  Le même trou existe côté `MAIN` : `MainRacePageUiState` n'a aucun état
  « capteur indisponible », et `SensorValueDisplay.Fallback` couvre
  indifféremment « pas encore de donnée » et « il n'y en aura jamais ».
  **Il n'existe aucun état, dans tout le module, capable de porter la
  phrase « la session d'exercice a échoué ».**

  **Comment le corriger.** Donner au refus de permission son propre cas
  dans `ExerciseSessionOpenResult`, distinct de `Failed`. Porter cet
  échec jusqu'aux états d'écran : `PreparationUiState` et
  `MainRacePageUiState` doivent avoir un cas qui ne se rend pas comme
  `Ready`, et qui soit atteignable dès la première émission — pas
  seulement après un premier succès.

  Ce que l'écran en dit relève d'une décision produit : tant qu'aucune
  clé de texte n'existe, R80 impose de ne pas emprunter une clé écrite
  pour autre chose, et le journal de R79 est alors tout le rapport.

- ## D9 — `ProfileRepository.observe()` : un `.catch` qui n'émet rien

  **Ce qui est constaté.** Défaut armé, non déclenché à ce jour. Il ne
  se manifestera qu'au premier échec du DAO.

  **Pourquoi ce défaut existe.** `ProfileRepositoryImpl.kt:108` porte un
  `.catch { Log.e(...) }` **sans `emit`**. Le flow se termine alors sans
  aucune émission.

  Le contrat déclaré de `observe()` — « émet le profil par défaut »
  avant toute synchronisation — n'est donc pas tenu en cas d'échec. Or
  deux appelants font `.first()` dessus : `WatchApp`, dans les branches
  `MAIN` et `PROJECTION`, et `NavigationModule:45` pour
  `profileAlreadySynced`. Un `.first()` sur un flow terminé sans
  émission lève `NoSuchElementException`, non rattrapée, dans le scope
  de `WatchRaceNavigator` qui n'a pas de handler.

  Le `.catch` est commenté comme conforme à R33. **La règle a été lue,
  citée, et mal appliquée** : R75 interdit nommément le catch silencieux
  qui n'émet rien, et exige qu'une frontière en `Flow` émette un échec
  de son propre type déclaré.

  Le rapport d'investigation générale a mesuré la conformité sur les
  frontières en `Flow` : **une sur huit**, et c'est la seule qui
  n'atteint pas l'extérieur du processus.

  **Comment le corriger.** Faire émettre au `.catch` une valeur d'échec
  du type déclaré par la frontière, jamais rien. Remplacer les deux
  `.first()` par une lecture qui traite explicitement le cas d'échec, ou
  les borner — R19 s'applique aussi ici.

- ## D10 — Cinq destinations sur huit peuvent ne rien rendre

  **Ce qui est constaté.** Défaut armé. Non déclenché aujourd'hui parce
  que la course et le profil sont bien présents en base — mais le
  mécanisme est en place.

  **Pourquoi ce défaut existe.** `WatchApp` (`MainActivity.kt:188-289`)
  dispatche sur `navigator.current`. Le `when` **est exhaustif** sur les
  huit destinations : aucune branche manquante, aucun `else` vide. Le
  trou est un cran plus bas.

  | Destination | Rend toujours ? |
  |---|---|
  | `SENSOR_PERMISSION`, `WAITING_FOR_PHONE`, `HOME` | oui — état non-nullable |
  | `PREPARATION` | non — `null -> Unit` |
  | `MAIN`, `PROJECTION` | non — `if` sans `else` sur `race` et `profile` |
  | `CONTROL` | non — `if` sans `else` sur `race` |
  | `END` | non — `if` sans `else` |

  Le motif est identique dans les quatre dernières : un `produceState`
  dont la valeur de départ est `null`, un `if` qui teste la non-nullité,
  et **rien** dans le cas contraire. La valeur initiale ne correspond à
  aucun écran.

  R35 pose qu'une transition non nommée est une erreur déclarée, jamais
  un no-op silencieux. Quatre `if` sans `else` sont quatre no-op
  silencieux.

  **Comment le corriger.** Donner un plancher à chaque branche : un état
  de chargement pendant que le `produceState` se résout, et un état
  d'erreur si la lecture échoue — les deux distincts l'un de l'autre,
  conformément à R88.

- ## D11 — R19 : vingt-quatre attentes, aucun timeout

  **Ce qui est constaté.** Aucun `await()` du dépôt ne porte de timeout.
  Les deux seuls `withTimeoutOrNull` du projet, dans
  `NavigationModule:44` et `:49`, bornent des lectures internes et non
  des appels sortants.

  **Pourquoi ce défaut existe.** R19 exige qu'aucune attente non bornée
  ne soit atteignable depuis une frontière publique, et que toute
  attente sur un appareil, un store ou la couche de données porte un
  timeout. Le rapport d'investigation générale a mesuré la conformité :
  **zéro sur vingt-quatre**.

  Ce n'est donc pas un oubli mais une règle qui n'a jamais produit le
  moindre effet sur le code. Elle ne porte pas la mention *« Checked by
  review »* et se présente comme mécanisable, alors qu'aucun outil de
  R65 ne la vérifie.

  Deux de ces attentes sont réellement infinies, et non simplement
  longues : les `deferred.await()` des systèmes de permission, où une
  activité détruite avant le callback du dialogue suspend la coroutine
  pour toute la vie du processus. `registerOne()` en est une troisième —
  traitée à part en D4, parce qu'elle se déclenchera à la correction de
  D2.

  **Comment le corriger.** Un balayage à part, sur les vingt-quatre
  sites, avec une durée choisie par nature d'appel : une lecture de
  capacités, un envoi sur la couche de données et un dialogue de
  permission n'ont pas les mêmes ordres de grandeur.

  Le dépassement se traite comme un échec ordinaire de l'appel, et suit
  alors les règles de D7 et D8 : journalisé, porté dans un état
  distinct.

  📌 `MessageChannel` (`core-sync`) est le seul modèle correct du dépôt
  sur tout le reste — `try`, `catch (CancellationException) { throw }`,
  `catch (Exception) { log ; valeur d'échec }`. Il ne lui manque que le
  timeout. C'est la forme à répliquer partout ailleurs.

- ## D12 — `WearableLinkStateSource` : quatre appels, quatre règles

  **Ce qui est constaté.** L'application plantait en boucle au démarrage
  sur `DUPLICATE_CAPABILITY`. Défaut distinct des précédents : il touche
  `:core-sync` et les deux applications, pas seulement la montre.

  **Pourquoi ce défaut existe.**
  `DataLayerCapabilitySource.localNodeId()` appelle
  `capabilityClient.addLocalCapability(CAPABILITY_NAME).await()` sans
  traiter le cas où la capability est déjà enregistrée. Or elle persiste
  dans Play Services par couple (paquet, capability) : le premier
  lancement passe, **tous les suivants échouent**, et l'`ApiException`
  remonte jusqu'à tuer l'application.

  Quatre appels du même fichier violent chacun quatre règles : R33
  (l'échec est jeté au lieu d'être rendu comme valeur), R33 seconde
  phrase (rien ne vérifie l'enregistrement préexistant), R31
  (l'`ApiException` de Play Services sort de `:core-sync` telle quelle),
  R19 (aucun timeout). Deux d'entre eux ignorent en plus le `Task`
  retourné par `addListener` et `removeListener` : leur échec est
  invisible.

  🔴 **Le fichier documente la violation comme un choix délibéré**
  (`:53-55`) : *« a registration failure propagates as a thrown
  exception from `localNodeId()`, the same way `reachableNodeIds()`
  already lets its own Task failure propagate »*. Une violation
  antérieure a servi de modèle à la suivante — alors que R1 pose que le
  fichier de conventions l'emporte sur le code existant. C'est le
  mécanisme le plus coûteux relevé sur tout ce cycle.

  Le motif « un état durable rend le second appel invalide » se retrouve
  à quatre autres endroits, dont un seul est correctement traité : le
  créneau de session d'exercice, où `ExerciseTrackedStatus` est lu avant
  chaque tentative. **C'est exactement la forme que
  `addLocalCapability` aurait dû prendre.**

  **Comment le corriger.** Absorber `DUPLICATE_CAPABILITY`, qui est le
  résultat normal d'un second lancement et non une erreur — toute autre
  exception continuant de remonter. Rendre les échecs de la couche de
  liaison non fatals : appareil non appairé, service indisponible,
  version obsolète doivent produire un état « liaison absente », jamais
  une exception non rattrapée.

  Supprimer le commentaire `:53-55` en même temps que le code qu'il
  justifie. Laissé en place, il fera à nouveau doctrine.

  Ajouter un test sur le second appel à `localNodeId()`, qui ne doit pas
  lever.

- ## D13 — `watch-history.db` sans migration ni repli

  **Ce qui est constaté.** Défaut en dormance. Aucun échec à ce jour,
  parce que la version du schéma n'a jamais changé.

  **Pourquoi ce défaut existe.** La base est déclarée en `version = 1`
  dans `RepositoryModule` (phone `:64`, wear `:69`), **sans
  `addMigrations` ni `fallbackToDestructiveMigration`**. Le jour où
  `RaceHistoryEntryEntity` changera, la première requête lèvera
  `IllegalStateException: A migration from 1 to 2 was required but not
  found` — sur **toute installation existante, jamais sur une
  installation neuve**.

  C'est le motif exact du défaut D12, sous une autre forme : un état
  durable qui rend invalide un usage ultérieur, invisible en
  développement puisque chaque réinstallation repart de zéro.

  Par contraste, `hyrox-tracker.db` est couverte par
  `fallbackToDestructiveMigration()` — ce qui évite le plantage au prix
  d'une perte de données, et constitue une décision produit qui n'a
  jamais été prise explicitement.

  **Comment le corriger.** Décider, pour chacune des deux bases, ce
  qu'une évolution de schéma doit faire : migrer, ou repartir de zéro.
  Pour `watch-history.db`, dont le contenu est un cache reconstruit à
  chaque synchronisation descendante, la destruction est probablement
  acceptable — mais c'est à écrire, pas à laisser au défaut de
  configuration.

  ⚠️ R8 interdit de modifier une migration déjà livrée ou son schéma
  exporté ; un changement structurel en ajoute une nouvelle.

- ## D14 — Le même jeton de navigation, deux traitements

  **Ce qui est constaté.** Un `PendingIntent` posé sur le cadran par la
  complication survit à une mise à jour de l'application. Si le nom de
  destination qu'il porte n'existe plus, le comportement dépend
  entièrement du chemin par lequel il arrive.

  **Pourquoi ce défaut existe.** Deux entrées lisent le même extra, et
  une seule s'en méfie.

  | Chemin | Ligne | Sur un nom inconnu |
  |---|---|---|
  | Reprise à chaud | `MainActivity.onNewIntent:150` | `WatchDestination.valueOf(extra)` — 🔴 **jette** |
  | Lancement à froid | `MainActivity.tappedDestination:167` | `entries.find { it.name == extra }` — ✅ rend `null` |

  Le second cite R32 dans son KDoc. Le premier ne le cite pas et ne
  l'applique pas. **La règle est connue, appliquée à un endroit sur
  deux**, sur la même donnée entrante.

  Un `PendingIntent` est un état durable, au même titre que la capacité
  GMS de D12 et la base de D13 : il est écrit par une version et lu par
  la suivante. Aucun lot ne déclare le couple des deux chemins — chacun
  a été écrit dans son propre périmètre.

  **Comment le corriger.** Faire porter au chemin de reprise à chaud la
  même lecture tolérante que le chemin à froid : un jeton inconnu rend
  `null` et laisse la destination courante inchangée. La conversion
  entrante est écrite une fois et partagée par les deux entrées, plutôt
  que dupliquée.

  Un test doit poser un extra portant un nom qui n'existe pas, sur les
  deux chemins.

- ## D15 — La complication tourne hors de toute activité

  **Ce qui est constaté.** `onComplicationRequest` peut être appelé
  alors que l'application n'a jamais été lancée : le système interroge
  la source de données du cadran indépendamment de tout écran.

  **Pourquoi ce défaut existe.** Le service injecte
  `WatchRaceNavigator`, dont le premier accès déclenche l'initialiseur
  paresseux — donc les lectures Room de `NavigationModule`, `.first()`
  compris. Ce chemin s'exécute hors de tout cycle de vie d'activité,
  sans `MainActivity`, et sans qu'aucun écran ne puisse rendre un état
  d'échec.

  Le défaut n'est pas propre à la complication : il élargit la surface
  d'un chemin déjà fragile. Un échec de source y produit une exception
  dans un service système, là où sur un écran il produirait au moins un
  état vide observable.

  Aucun lot ne déclare ce point d'entrée. Comme le manifeste de D2 et
  les points d'entrée des deux modules, c'est un artefact que la chaîne
  ne contrôle nulle part : ni signature, ni critère d'acceptation.

  **Comment le corriger.** Ce point se corrige avec D9 et D10 — une
  source qui émet son échec, et un état qui le porte. Ce qui lui est
  propre est de ne pas dépendre d'un écran pour exister : la source de
  complication rend une donnée vide plutôt que de laisser une exception
  sortir du service.

- ## D16 — Les deux services d'écoute qui jettent leur issue

  **Ce qui est constaté.** Deux entrées inverses — celles par lesquelles
  le système ou l'autre appareil parlent à l'application — lisent un
  résultat et le laissent tomber.

  | Fichier:ligne | Ce qui disparaît |
  |---|---|
  | `ProfileSyncListenerService.kt:53` | L'issue d'`applyIncoming(...)` : `Refused` et `Failure` disparaissent sans log |
  | `WatchRaceComplicationDataSourceService.kt:47` | `findInProgress().getOrNull()` — un échec du store se lit comme « pas de course » |

  **Pourquoi ce défaut existe.** Les deux autres services d'écoute du
  dépôt sont conformes : `RecordedRaceListenerService` encapsule son
  décodage et journalise ses deux échecs ; `RecordedRaceAckListenerService`
  traite `BufferUnderflowException` et journalise l'échec d'`acknowledge`.
  **La forme correcte existe, à côté, dans le même dossier.**

  Le second cas est plus grave que le premier : la complication s'efface
  silencieusement du cadran, et rien ne dit pourquoi. C'est le même
  `getOrNull()` que D5 relève dans `WatchApp`, sur le même appel.

  **Comment le corriger.** Journaliser l'issue en ERROR dans les deux
  cas, sur le modèle des deux services conformes. La complication rend
  une donnée vide plutôt qu'un `null` indistinct — voir D15, dont c'est
  le même point d'entrée.

- ## D17 — Trois appels hors de tout `try`

  **Ce qui est constaté.** Trois appels sortants s'exécutent sans
  protection, dans des fichiers qui en appliquent une partout ailleurs.

  | Fichier:ligne | Appel | Ce qui traverse |
  |---|---|---|
  | `ExerciseSessionSystemImpl.kt:45` | `getCurrentExerciseInfoAsync().await()` | Le `try` commence ligne 52 |
  | `PlatformModule.kt:43` | `HealthConnectClient.getOrCreate(context)` | Jette depuis un `@Provides` Hilt |
  | `HrPermissionSystemImpl.kt:32` | `getGrantedPermissions()` | Aucun `try` sur ce chemin |

  **Pourquoi ce défaut existe.** Le deuxième est le plus dangereux : une
  exception levée dans un `@Provides` casse la construction du graphe
  d'injection, au démarrage du téléphone, hors de tout écran capable de
  l'afficher. Le statut du SDK est pourtant vérifié juste avant, ligne
  39 — **la garde est là, l'appel qu'elle protège est en dehors.**

  Comme pour D3, la forme du geste est présente et l'objet est faux :
  une relecture de conformité voit un contrôle avant l'appel.

  **Comment le corriger.** Faire entrer les trois appels dans le `try`
  qui les concerne. Pour `PlatformModule`, la sentinelle existe déjà —
  `getSdkStatus` rend `null` sur échec ; `getOrCreate` doit rendre la
  même sentinelle plutôt que de jeter.

- ## D18 — L'exception de la dépendance voyage dans le `Result`

  **Ce qui est constaté.** Les trois dépôts qui exposent des surfaces
  `suspend` font `withContext(IO) { runCatching { … } }`. Le `Result`
  ne jette pas — mais il **porte la `SQLiteException` brute**.

  **Pourquoi ce défaut existe.** R31 demande qu'une exception de
  dépendance ne traverse pas la frontière du module. Ici elle ne la
  traverse pas en étant levée : elle la traverse **en étant
  transportée**. Le `runCatching` satisfait la lettre de la règle, pas
  ce qu'elle protège.

  ⚠️ **Aucun appelant ne s'en aperçoit** tant qu'il se contente de
  `fold` sur l'échec sans lire son type — ce que tous font aujourd'hui.
  Le jour où l'un d'eux inspecte la cause, il dépend du moteur de base
  de données depuis un module qui ne le déclare pas.

  **Comment le corriger.** Convertir en échec déclaré du domaine, comme
  `RaceQueryFailure` le fait déjà pour les flows — `observeAll()` et
  `observeReference()` montrent la forme attendue dans le même fichier.

- ## D19 — Deux attentes que rien ne peut débloquer

  **Ce qui est constaté.** Les deux systèmes de permission suspendent
  sur `deferred.await()` après avoir lancé un dialogue système.

  | Fichier:ligne | Attente |
  |---|---|
  | `ConnectivityPermissionSystemImpl.kt:57-58` | `launcher.launch()` puis `await()` |
  | `SensorPermissionSystemImpl.kt:87-90` | `lifecycle.withResumed { launch }` puis `await()` |

  **Pourquoi ce défaut existe.** Si l'activité est détruite avant que le
  callback n'arrive, la coroutine ne reprend jamais : **l'attente dure
  toute la vie du processus.** Le `withResumed` du second traite la
  fenêtre de lancement, pas l'absence de réponse.

  C'est le cas de R19 le plus concret du dépôt, et il est atteignable au
  démarrage des deux applications — `HomeViewModel.init:58` et
  `ProfileViewModel.init:122`.

  📌 **`registerOne()` de D4 est le même motif**, sur un callback de
  plateforme au lieu d'un dialogue.

  **Comment le corriger.** Borner l'attente, et traiter le dépassement
  comme un refus non prononcé — un état distinct de « refusé » et de
  « accordé », que le parcours d'autorisation sait déjà représenter.

  ⚠️ **Ne pas confondre avec un refus.** Un dialogue sans réponse n'est
  pas un refus : le reproposer est légitime, alors que reproposer après
  un refus explicite ne l'est pas.

- ## D20 — Trois lectures disque sur le thread de l'appelant

  **Ce qui est constaté.** Les quatre stores `SharedPreferences` font
  `getBoolean`, `getString` et `edit().apply()` — **aucune méthode n'est
  `suspend`.**

  **Pourquoi ce défaut existe.** `SharedPreferences` lit le disque au
  premier accès, sur le thread qui appelle. R24 l'interdit. Les stores
  ont été écrits comme des accesseurs simples, et rien dans leur
  signature ne dit qu'ils touchent le disque.

  📌 **Aucun symptôme observé** — les fichiers sont petits et le premier
  accès arrive tôt. Le défaut est déclaré ici parce qu'il est réel et
  systématique, pas parce qu'il se manifeste.

  **Comment le corriger.** Rendre les surfaces `suspend` et déplacer
  l'accès sur le répartiteur d'entrées-sorties, comme les dépôts Room le
  font déjà.

- ## D21 — Deux ouvertures d'écran système sans garde

  **Ce qui est constaté.** `SensorPermissionSystemImpl.kt:105-110` et
  `ConnectivityPermissionSystemImpl.kt:73-79` appellent
  `activity.startActivity(intent)` pour ouvrir les réglages système.
  **`ActivityNotFoundException` n'est pas traitée.**

  **Pourquoi ce défaut existe.** L'écran de réglages visé n'existe pas
  sur tous les appareils ni toutes les versions. R33 demande de vérifier
  ce dont un appel a besoin avant de le faire ; ici rien ne vérifie que
  l'intention est résoluble.

  **Comment le corriger.** Résoudre l'intention avant de la lancer, et
  traiter l'absence comme un cas nominal — l'utilisatrice reste sur
  l'écran, avec une indication de ce qu'elle doit faire à la main.
