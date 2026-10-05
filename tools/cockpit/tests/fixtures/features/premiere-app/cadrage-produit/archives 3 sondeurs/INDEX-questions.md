## Answers

B1.1          | date de course : consommée par B6, B7, B23, B51 ; ni B14 ("fiche de course" = nom + 30 durées, pas de date) ni B46 (produit durée segment/total/instant d'ouverture, pas de date) ne la produisent — gap: aucun bloc ne produit explicitement un champ « date de course ».
B1.1          | permission d'accès à l'historique de santé : consommée par B17 et B60 ; état système (OS), externe à la feature — non produite dans l'index, et n'a pas à l'être.
B1.1          | permission capteurs (OS) : consommée par B20 et B60 ; état système (OS), externe à la feature — non produite dans l'index, et n'a pas à l'être.
B1.2          | segment d'arc actif / zone affichée : B18 produit "segment d'arc actif reflétant la zone de la lecture courante" (sans hystérésis) et B42 produit "zone active" (avec hystérésis ±3bpm) ; B28 ne consomme que B42 pour l'affichage — gap: deux mécanismes distincts revendiquent la même sortie.
B1.2          | fréquence cardiaque max (profil) : écrite par B17 ("préremplissage automatique... ou saisie manuelle ultérieure de l'utilisateur") et par B19 (validation par bornes 100–230bpm) — gap: chevauchement non résolu entre les deux écritures.
B1.2          | temps total de la course : calculé par B14 ("recalculé par somme des durées stockées, jamais stocké") et par B46 ("total = sum of the segments, never the total minus the others") — même règle dans les deux blocs, cohérent.
B1.3          | rejet (k_mesuré hors [0.70,1.40], B37) : stocké avec la course, explicitement "non affiché" — aucun bloc de l'index ne le lit — gap: pas de consommateur pour cette donnée stockée.
B1.3          | repli/tiret pour valeur capteur obsolète (B29) : ni B28 ni B30 ne citent B29 parmi ce qu'ils consomment, alors qu'ils affichent des valeurs capteur — gap: lien de consommation absent entre B29 et les pages de course.
B1.3          | état d'affichage atténué du mode économie d'énergie (B35) : B28 (page principale, seul écran de course décrivant son rendu en détail) ne cite pas B35 parmi ce qu'il consomme — gap: lien de consommation absent entre B35 et B28.
B1.4          | B45 lit "arbitration outcome from B25/B26" à l'ouverture de la séance d'exercice ; B26 a "Writes at | —" (vide) — gap: aucun moment d'écriture documenté pour la sortie que B45 doit lire.
B1.5          | écran de détail de course — ligne d'actions : B7 définit la zone (en-tête / ligne d'actions / liste de segments) ; B8 ("Définir comme référence"), B9 (renommer) et B10 ("Supprimer") y placent chacun une action — cohérent avec B56 (trois libellés nommés), coexistence.
B1.5          | carte de la liste des courses : B6 énumère le contenu de la carte (nom/date/temps total + badges) sans bouton ; B8 produit un état affiché/masqué de bouton sur cette même carte — gap: bouton absent de la composition de carte décrite par B6.
B1.5          | écran d'accueil (montre) : B20 place un rappel de permission sur l'écran d'accueil ("zone non précisée") ; B22 détaille toute la disposition de cet écran (ligne de référence, bouton "Démarrer", pastilles "Historique"/"Synchroniser") sans zone de rappel — gap: zone de rappel absente de la disposition B22.
B1.5          | écran profil (téléphone) — zone de date de dernière synchronisation : B16 y affiche la date, B61 y affiche un message d'indisponibilité quand la permission de connectivité manque — deux états mutuellement exclusifs de la même zone, cohérent.
B1.6          | voir B2.1 — au-delà des instances qui y sont relevées, la colonne Names ne fait apparaître aucune autre valeur contradictoire pour un même nom.
B2.1          | délai d'inactivité (page secondaire) = 8 secondes : défini à l'identique en B27 et en B58, cohérent.
B2.1          | Segment 30 (fusion Roxzone + Wall Balls + sprint, affiché sous le nom "Wall Balls") : défini à l'identique en B1 et en B28, cohérent.

## Questions

### Q1
Block: B14 — Saving an imported race / B46 — Monotonic timing and recovery
Question: Which block stores a race's date, since B14 stores only the name and 30 segment durations, B46 does not list a date among what it writes, yet B6, B7, B23 and B51 all consume a race's date?
Answer:

### Q2
Block: B18 — Zone ranges from maximum heart rate
Question: Does the active zone-arc segment shown on screen come from B18's direct zone lookup or from B42's hysteresis-adjusted zone, given both blocks describe producing it?
Answer:

### Q3
Block: B17 — Deriving maximum heart rate / B19 — Editing profile settings
Question: When the user manually enters a maximum heart rate through B17's field, does that entry go through B19's validation (100-230 bpm bounds), or is B17's manual-entry write a separate, unvalidated path?
Answer:

### Q4
Block: B37 — Computing the correction factor
Question: What block reads or displays the rejection record (k_mesuré outside [0.70, 1.40]) that B37 stores with the race but never shows?
Answer:

### Q5
Block: B28 — Main page, adapting to the current segment / B30 — Projection page
Question: Do the main page (B28) and the Projection page (B30) apply B29's data-freshness fallback (dash or hidden block after 10 seconds without a sensor reading) to the sensor values they display, since neither lists B29 among what it reads?
Answer:

### Q6
Block: B28 — Main page, adapting to the current segment
Question: Does the main page (B28) apply B35's power-save dimmed display state, since B28 does not list B35 among what it reads?
Answer:

### Q7
Block: B26 — Resuming our own already-active race
Question: At what moment does B26 write the arbitration outcome that B45 reads at session start, since B26's "Writes at" is empty?
Answer:

### Q8
Block: B6 — Race list screen
Question: Does the race list card include the reference-setting button that B8 shows or hides on it, since B6's card composition (name, date, total time, badges) does not mention a button?
Answer:

### Q9
Block: B20 — Sensor permission request / B22 — Home screen
Question: Where on the home screen does B20's permission reminder sit, since B22's full layout (reference line, "Démarrer" button, "Historique" and "Synchroniser" pills) does not name a reminder zone?
Answer:
