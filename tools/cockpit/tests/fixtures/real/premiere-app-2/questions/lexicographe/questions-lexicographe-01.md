# Questions du lexicographe — premiere-app-2

Balayage de `idees.md` (invocation 1). Une entrée par paire relevée et
par doute de guillemets. Les questions sont en anglais, les réponses
s'écrivent en français dans le champ `Answer:`.

---

### Q1
Terms: atelier, STATION
Question: §2 writes "chacun suivi d'un atelier, dans un ordre fixe — SkiErg, Sled Push, Sled Pull, Burpee Broad Jump, Rameur, Farmers Carry, Sandbag Lunges, Wall Balls." and §A.3 writes "| `<Atelier> Out` | `STATION` du cycle n |". I read these as one same thing under two names — the French prose word and the segment constant. Is that right, or does `STATION` name something the word "atelier" does not cover?
Answer: Station

### Q2
Terms: kilomètre, RUN, tour
Question: §2 writes "1. le kilomètre de course", §A.3 writes "| `Rox In` | `RUN` du cycle n |", and §6.2 writes "| Haut | L'écart sur ce tour par rapport à la référence |". I read the three as one same segment — the running segment — named once in prose, once as a constant, once as "tour" in the delta wording. Is "tour" the same thing as "kilomètre", or does it name something else?
Answer: Un tour fait un kilometre, cette partie du l'hyrox peut se nommer RUN

### Q3
Terms: Roxzone, ROX_IN, ROX_OUT
Question: §2 writes "Entre la piste et les ateliers, la Roxzone : la zone de transition traversée à l'aller et au retour." then "2. la Roxzone vers l'atelier" and "4. la Roxzone vers la piste"; §A.3 writes "| `<Atelier> In` | `ROX_IN` du cycle n |" and "| `Rox Out` | `ROX_OUT` du cycle n |". I read "Roxzone" as the place that contains two distinct segments, `ROX_IN` and `ROX_OUT`, and not as a third name for either of them. Is that the reading?
Answer: Roxzone est la zone de transition, compose de 2 temps, le ROX_IN avant la station et ROX_OUT a la sortie de la station jusqua la reprise de la course

### Q4
Terms: transition
Question: §2 writes "la Roxzone : la zone de transition traversée à l'aller et au retour." and §6.2 writes "| Haut | Le temps écoulé dans la transition |", while §11 writes "**Une transition est atomique** : fermer le segment précédent et ouvrir le suivant se font en une seule écriture." I read one word carrying two meanings — the Roxzone segment, and the instant where one segment closes and the next opens. Are these two distinct things?
Answer: Roxzone est la zone de transition,compose de 2 temps, le ROX_IN avant la station et ROX_OUT a la sortie de la station jusqua la reprise de la course 

### Q5
Terms: bloc final, FINAL_BLOCK, trentième segment, Wall Balls
Question: §2 writes "30. le bloc final — Roxzone, Wall Balls, sprint vers la ligne", §6.2 writes "**Le trentième segment** — le bloc final, Roxzone puis Wall Balls puis sprint — est traité comme un atelier. Le nom affiché est Wall Balls", and §A.3 writes "| `Total time` | `FINAL_BLOCK` |". I read four names for the thirtieth segment: a prose name, a constant, an ordinal, and the label shown on the watch. Is "Wall Balls" here only the displayed label of that segment, the segment itself keeping the name "bloc final"?
Answer: Le 30eme segment correspond au dernier segment de la data a coller, c'est la station wall-ball, on peut transformer bloc final et final-block en gardant le mot station comme definit q1

### Q6
Terms: course
Question: §4.1 writes "Écran d'ouverture. Une carte par course : nom, date, temps total." while §2 writes "Une course Hyrox est identique partout : huit kilomètres de course, chacun suivi d'un atelier". I read one word carrying two meanings — the race as a recorded object, and the act of running. The chain writes concepts in English and would have to pick between two words. Are these two distinct things?
Answer: on garde la distinction entre une race pour lepreuve et run pour la partie course de la race

### Q7
Terms: segment
Question: §2 writes "**Une course est découpée en 30 segments.**" while §6.3 writes "Cinq segments de même taille suivant la courbure basse de l'écran, chacun d'une couleur." and §3.3 writes "| `arc-segment` | 25,6° par segment |". I read one word carrying two meanings — one of the thirty pieces of a race, and one of the five pieces of the heart-rate arc. Are these two distinct things?
Answer: ce sotn 2 choses differentes. les 5 segments sont des elements visuel sur lecrand e la montre alors que les 30 segments correspondent aux 30 moments de la course, il sreferent aux 30 lignes collees pour limportation des donnees

### Q8
Terms: référence, favori
Question: §4.1 writes "La course de référence porte une marque visible." and §5.3 writes "Le favori ne s'y change pas, une course ne s'y supprime ni ne s'y renomme." I read "favori" as a second name for the reference race, appearing once. Do they name one same thing?
Answer: meme terme

### Q9
Terms: mode veille, mode économie, affichage permanent
Question: §3.4 is titled "### 3.4 Mode veille" and lists "`arc-opacity-idle-dim` | 0,25 au lieu de 0,30"; §6.9 is titled "### 6.9 Affichage permanent" and writes "En mode économie, les valeurs sont visuellement atténuées." then "Rafraîchissement en mode économie : **dix secondes**"; §13.2 writes "| Fréquence cardiaque | Capteur | Continu, ou 10 s en veille |". I read "mode veille" and "mode économie" as one same dimmed state named twice, "affichage permanent" naming the feature that state belongs to. Is that right?
Answer: l'affichage permanent c'est la contraite daffichage, soit on est en mode attenue, qui correpsond aux mots veille et economie, soit en affichage normal

### Q10
Terms: activité, session d'exercice
Question: §6.5 writes "**Arrêter l'activité.** Avec confirmation." then "**Reprise d'activité en cours.** Même structure : titre, mention que l'activité en cours sera arrêtée", and §5.2 writes "*En cours* — indicateur d'activité et « Ne ferme pas l'application »." while §10 writes "**Une seule session d'exercice pour toute la course**". I read "activité" carrying three meanings — our own race, another application's exercise session, and the spinner of a running operation — and "session d'exercice" naming the system object. Are these distinct things?
Answer: la session dexercice correspond a ce qui se passe avec le systeme dactivite de la montre (samsung health par exemple), mais ca decrit la meme chose, le moment ou on a demarrer la course et lenregistrement

### Q11
Terms: seuil, borne, frontière
Question: §4.4 writes "Chaque seuil est la borne **basse** de sa zone" and "Cinq zones demandent quatre frontières : les deux extrémités sont ouvertes."; §8.4 writes "La bascule vers la zone supérieure demande de dépasser sa borne de **3 bpm**." and "L'hystérésis décale une frontière". I read three words for one same thing — the limit between two heart-rate zones. Do they name one same thing?
Answer:oui

### Q12
Terms: seuil
Question: §4.4 writes "**Quatre seuils de zone**, en pourcentage de la FC max.", §6.1 writes "Un relâchement avant le seuil annule le marquage et n'écrit rien.", and §13.1 writes "En mode économie, le seuil est celui de la cadence de rafraîchissement". I read one word carrying three meanings — a zone limit, the long-press duration, and the staleness delay. Are these distinct things?
Answer: les seuils de zone correspondent a ce que lon a definit Q11, le reste c'est le delais qu'il faut maintennir appuye pour passer a la station suivante

### Q13
Terms: reprise, reprendre
Question: §10 writes "*c'est notre propre course* → reprendre là où elle en était, ne pas redémarrer.", §6.5 writes "**Reprise d'activité en cours.**", §12 writes "**Reprise d'une activité en cours** — s'intercale entre « Lancer » et le démarrage de la course, uniquement si une autre application occupe le capteur d'exercice.", and §5.1 writes "un rappel sur l'écran d'accueil est la seule reprise, et c'est une action." I read the same word used for resuming our own race, for the screen that stops another application's activity, and for re-asking a permission. Are these distinct things?
Answer: demdemander la permission est different, les 2 autres sont la meme chose

### Q14
Terms: position
Question: §6.4 writes "| Bas | Le temps total écoulé et la position, « 14/30 » |" while §3.4 writes "| `dim-text` | Valeurs atténuées, position inchangée |" and §6.9 writes "**Aucune position ni aucune taille de texte ne change**". I read one word carrying two meanings — where the runner is in the thirty segments, and where an element sits on the screen. Are these two distinct things?
Answer: 2 choses differentes, le position 14/30 correspond a la position en temps reel dans la race, lautre position decrit l'emplacement dun element visuel sur la montre

### Q15
Terms: bloc
Question: §6.2 writes "Le bloc du bas ne change jamais : fréquence cardiaque et arc des zones." and §13.2 writes "Sans référence chargée, **quatre blocs disparaissent**", while §2 writes "30. le bloc final — Roxzone, Wall Balls, sprint vers la ligne". I read one word carrying two meanings — a region of the screen, and the thirtieth segment of the race. Are these two distinct things?
Answer: 2 choses differentes, tes definitions sont correctes

### Q16
Terms: écran, page
Question: §6.2 is titled "### 6.2 Page principale — trois états", §6.4 "### 6.4 Page Projection", §6.7 "### 6.7 Page de fin", while §5.2 is titled "### 5.2 Écran d'accueil" and §4 writes "Quatre écrans."; §6.6 mixes both — "page principale, Projection, Contrôle et écran de fin". I read "page" as reserved for what is reached by swiping during a race and "écran" for everything else, but "page de fin" and "écran de fin" name the same thing in two places. Is the distinction real, or is it one same thing under two names?
Answer: ce sont les memes choses

### Q17
Terms: écran
Question: §6.2 writes "L'écran fait 1,5 pouce en 480 × 480 et il est rond." and §3.1 writes "| `screen-black` | `#000000` | Fond de la montre — noir pur, OLED |", while §4.1 writes "Écran d'ouverture." I read one word carrying two meanings — the physical display of the device, and one screen of the application. Are these two distinct things?
Answer: 2 choses differentes, tes definitions sont correctes

### Q18
Terms: historique
Question: §5.2 writes "En faisant défiler : **Historique** et **Synchroniser**." while §4.4 writes "le maximum observé sur douze mois dans l'historique de santé du téléphone" and "La FC max se dérive de l'historique de fréquence cardiaque", and §7.3 writes "**le dernier facteur retenu, tous historiques confondus**". I read one word carrying two meanings — the list of the runner's own races, and the phone's health record read from outside. Are these distinct things?
Answer: 2 choses differentes, tes definitions sont correctes

### Q19
Terms: liste des courses, historique
Question: §4.1 is titled "### 4.1 Liste des courses" and writes "Une carte par course : nom, date, temps total."; §5.3 is titled "### 5.3 Historique" and writes "La liste des courses en version résumée : nom, date, temps total." I read one same list named twice, once per device — "liste des courses" on the phone, "Historique" on the watch. Is that one thing under two names, or two distinct things?
Answer: ce sont les meme choses

### Q20
Terms: écart, delta, avance, ahead, retard, behind
Question: §8 writes "Trois écarts distincts, à ne pas confondre" while §B.2 writes "| `delta` | signe + `m:ss` | `+1:12`, `−0:30`, `+0:00` |" and §3.1 writes "| `delta-zero` | `#726D63` | Écart nul — ni avance ni retard |" and "| `ahead` | `#4FAE72` | Avance — flèches, pictogrammes |". I read the English words as the token names of the concepts the prose names in French, §3 having stated "Jetons de conception, nommés en anglais." Is each pair one same thing?
Answer: oui

### Q21
Terms: allure, pace, vitesse
Question: §7 writes "l'allure est dérivée des capteurs de la montre" and §B.3 writes "| `pace` | `m:ss` + unité détachée | `6:00` `/km` |", while §7.1 writes "| `allure-lissee` | Moyenne glissante de la vitesse instantanée sur **10 secondes** |". I read "allure" and `pace` as one same thing, and "vitesse" as a different measure — an instantaneous speed the smoothing is computed on, never displayed as such. Is that the reading?
Answer: oui

### Q22
Terms: fréquence cardiaque, FC, FC max, bpm, battements par minute
Question: §4.4 writes "**Fréquence cardiaque maximale** — proposée automatiquement", §13.4 writes "| FC max | Maximum observé sur 12 mois, ou saisie manuelle |", §C.4 shows the displayed label "`Zones cardiaques (% FC max)`", §6.3 writes "Au-dessus, la fréquence en battements par minute." and §B.3 writes "| `hr` | entier + unité détachée | `168` `bpm` |". I read "FC" as the abbreviation of "fréquence cardiaque" and "bpm" as the abbreviation of "battements par minute", both reaching the screen in some places and used in prose in others. Is the abbreviation meant to appear on screen everywhere, or only in the places quoted?
Answer: oui il y a des abreviations, bpm est l'unite de mesure de la frequence cardiaque, utilisation uniquement la ou cest definit comme tel

### Q23
Terms: distance_attendue, Distance d'un kilomètre
Question: §4.4 writes "**Distance d'un kilomètre** — la `distance_attendue` du §7.2. 1000 m tant qu'elle n'a jamais été modifiée." and later in the same section "la distance attendue entre dans le facteur de correction et dans l'écart sur le tour", while §7.2 writes "k_mesuré = distance_attendue / distance_mesurée_sur_le_segment_RUN". I read one same setting named twice — a displayed label on the profile screen and an identifier in the formulas. Is that right?
Answer: oui

### Q24
Terms: allure-segment, allure-lissee, distance_attendue, k_mesuré, temps_projeté
Question: §3 writes "Jetons de conception, nommés en anglais." while the computation identifiers are written in French — "`allure-segment`", "`allure-lissee`", "`distance_attendue`", "`k_mesuré`", "`temps_projeté`". None of them reaches the screen. I read them as concepts, not as displayed texts, which the chain writes in English from the product file onward. Is that right, or must these identifiers stay written as they are?
Answer: tu as raison

### Q25
Terms: collage, import, résultat, export
Question: §4.3 is titled "### 4.3 Collage d'un résultat" and writes "On colle les quatre colonnes copiées depuis hyresult ; l'application vérifie et enregistre.", while the button is "Le bouton « Importer » reste inactif tant que la zone de collage, le nom ou la date ne sont pas renseignés." and §A.5 writes "Rien n'est écrit — jamais d'import partiel."; §4.3 also writes "l'export ne porte aucune date" and "les résultats officiels ne s'exportent pas". I read "collage" and "import" as one same operation named twice, and "résultat" and "export" as one same pasted table named twice. Is that the reading?
Answer: oui

### Q26
Terms: libellé, nom, point de passage, Split
Question: §A.2 writes "| `Split` | Libellé du point de passage | Identifie le segment |" and §C.5 writes "« <libellé> » n'est pas un point de passage attendu.", while §13.2 writes "| Libellé du dernier marquage | Journal des marquages |" on one line and "| Nom du segment, destination | Constante de domaine |" on another. I read "libellé" and "nom" naming one same thing for a segment, and "point de passage" and "Split" naming one same thing in the pasted table. Are these one thing each, or four distinct things?
Answer:one thing each

### Q27
Terms: marquage, avancement
Question: §6.1 writes "**Toute la surface de l'écran est le bouton d'avancement.**" and just below "**Une vibration** confirme chaque marquage pris en compte."; §12 writes "Depuis n'importe quelle page sauf Contrôle : appui long ──► segment suivant". I read "avancement" as the name of the button and "marquage" as the name of what it records — one gesture, two words. Do they name one same thing?
Answer: oui

### Q28
Terms: badge, pastille
Question: §4.1 writes "Badge `Référence` en `link` sur fond teinté", §4.2 writes "**Confirmation de suppression.** Pastille `!` sur fond `behind`", §4.4 writes "pastille carrée `zone-1` à `zone-5`", and §10 writes "Une pastille sur le cadran permet de revenir à l'application pendant toute la course." I read "pastille" carrying three meanings — a dialog icon, a colour swatch in the zone list, and the system indicator on the watch face — and "badge" naming a fourth, tinted-label element. Are these distinct things?
Answer: ce sont des choses distinctes, il faut revoir le vocabulaire pour etre plsu precis

### Q29
Terms: carte, encart
Question: §3.1 writes "| `surface-raised` | `#1C1A18` | Cartes, encarts, champs |", §4.1 writes "Une carte par course en `surface-raised`, `radius-card`", and §4.3 writes "puis un encart `surface-raised` montrant la ligne telle qu'elle a été lue en `behind`". I read one same raised container named twice, both carrying `surface-raised`. Do they name one same thing?
Answer: oui

### Q30
Terms: démarrage, Démarrer, lancement, Lancer
Question: §5.4 is titled "### 5.4 Démarrage, en deux temps" and its second step is "- **Lancement**, au coup de départ. Le chrono part"; §5.2 writes "- **Démarrer**, un gros bouton au centre." while §12 writes "s'intercale entre « Lancer » et le démarrage de la course" and §10 writes "Au démarrage, trois cas". I read "démarrage" carrying two meanings — the whole two-step sequence opened by the button "Démarrer", and the race start which §5.4 names "Lancement". Are these two distinct moments?
Answer:il y a 2 momement, le lancement de la sessions et le demarrage de la course, le lancement permet d'arriver dans le sas, faire chauffer le capteur Le lancement de la sessions avec le boutonn "lancer", le demarrage avec "demarrer", a modifier dans le corpus poru rendre coherent les 2 phases

### Q31
Terms: préparation, sas
Question: §5.4 writes "- **Préparation**, dans le sas. La session d'exercice s'ouvre, les capteurs montent en régime" and §12 writes "├── Démarrer ──────────►  Préparation (sas)". I read "sas" as the physical place and "Préparation" as the state of the application while in it — not two names for one thing. Is that the reading?
Answer:oui meme chose, cf q30

### Q32
Terms: arrivée estimée, estimation du temps d'arrivée, temps d'arrivée estimé
Question: §6.4 writes "| Centre, en gros | L'estimation du temps d'arrivée |", then "Temps d'arrivée estimé en `font-data`/`w-display`.", then "la mention « arrivée estimée » en `w-caption`/`text-tertiary`"; §8.2 is titled "### 8.2 Écart cumulé et arrivée estimée". I read one same value worded three ways, only "arrivée estimée" reaching the screen. Is that right?
Answer: oui

### Q33
Terms: Rameur, Row, Burpee Broad Jump, Burpee BJ, Farmers Carry, F. Carry, Sandbag Lunges, S. Lunges
Question: §2 lists the stations as "SkiErg, Sled Push, Sled Pull, Burpee Broad Jump, Rameur, Farmers Carry, Sandbag Lunges, Wall Balls." while §A.3 lists "`SkiErg` · `Sled Push` · `Sled Pull` · `Burpee BJ` · `Row` · `F. Carry` · `S. Lunges` · `Wall Balls`", and §A.3 adds "Quatre de ces huit noms ne correspondent pas aux noms de segments du domaine." §6.2 writes "| Nom de l'atelier | `font-label`, `w-label`, `text-tertiary`, lettres espacées, capitales |" and shows "`→ SkiErg`". I read the eight domain names as displayed texts — they reach the watch screen character for character — and the annexe A names as data read from hyresult, never displayed. On that reading "Rameur" is the only French one among eight displayed names. Which name is shown on the watch for that station?
Answer: Remplace rameur par Rowing pour avoir le noms complet des stations avec lerus diminutif associe

### Q34
Terms: Démarrer, Lancer, Quitter, Terminer, Historique, Synchroniser, Contrôle, Projection
Question: these appear bare and bold in the prose — "- **Démarrer**, un gros bouton au centre.", "Un bouton **Quitter** ferme la préparation", "Un bouton **Terminer** ramène à l'écran d'accueil." — and quoted as fixed texts in §C.4 — "| Accueil | `Démarrer` · `Historique` · `Synchroniser` · `⚠ Aucune référence` |", "| Fin | `Terminer` |". I read all of them as displayed texts written without quotes in the prose. "Projection" is the exception I cannot settle: §6.4 is titled "### 6.4 Page Projection" but §C.4 lists only "`arrivée estimée`" for that screen, so nothing shows the word. Is "Projection" a displayed title like "Contrôle", or a page name that never reaches the screen?
Answer: Projection est le nom donne a lecran qui durant la course affiche le temps darrive estime. Ce nest pas un bouton ni un texte

### Q35
Terms: Réf.
Question: §5.2 writes "« Réf. — Bordeaux 2025 · 1:37:25 »" and §C.2 writes "| `Réf. — <nom>` |", while §6.2 writes "| Temps de référence `Réf. 4:26` | `font-data`, `w-label`, `text-secondary` |". I read one same displayed prefix in two forms — with an em dash on the home screen, without one during a race. Are the two forms intended?
Answer:il faut harmoniser

### Q36
Terms: Référence, référence, Incomplète, incomplète, Historique, historique, Contrôle
Question: §4.1 writes "Badge `Référence` en `link` sur fond teinté, badge `Incomplète` en `behind-text` sur `behind-bg`" while the same section writes "La course de référence porte une marque visible." and "Une course incomplète est marquée comme telle"; §5.3 writes "Titre `Historique`" while §9 writes "l'historique résumé"; §6.5 writes "Titre `Contrôle`" while §6.6 writes "page principale, Projection, Contrôle et écran de fin". I read each of these words as being twice over — once a displayed text, once a concept — and therefore two entries rather than one. Is that right?
Answer:oui
