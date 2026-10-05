# Questions du lexicographe — premiere-app-2 — tour 3

Troisième balayage de `idees.md`, après application des tours 1 et 2.
Une entrée par paire et par doute de guillemets ; le détail des
occurrences est sous `## Non tranché` de `lexique.md`.

---

### Q1
Terms: cadran
Question: your Q6 answer of round 2 flagged this one. The word carries
two things: the disc of the screen used as the geometric frame of the
arc — "cinq arcs concentriques au cadran", "centré sur le bas du
cadran" (§3.3, §6.3) — and the face of the watch where the system
draws its shortcut — "Un raccourci système sur le cadran permet de
revenir à l'application" (§10). I read them as two distinct things:
the first belongs to the application's drawing, the second to the
system. Are they distinct, and which of the two keeps "cadran"?
Answer: Oui, deux choses distinctes.

**Cadran** reste à la face de la montre, celle où le système dessine son raccourci (§10). C'est le terme grand public de Wear OS, on ne le contrôle pas.

La géométrie de l'arc emploie **l'écran**, dont les deux sens sont déjà distingués au lexique.

⚠️ §3.3 demande une réécriture, pas une substitution : « cinq arcs concentriques au cadran, même centre que l'écran » deviendrait redondant. Écrire « cinq arcs concentriques, centrés sur l'écran ». §3.3 et §6.3 : « centré sur le bas de l'écran ».

### Q2
Terms: pictogramme rotatif, indicateur de progression
Question: round 2 settled "indicateur de progression" for the spinner
shown while a synchronisation runs, and §5.2 now reads "*En cours* —
indicateur de progression". The phone side, §4.4, still reads
"*En cours* — pictogramme rotatif et « Ne ferme pas l'application »".
I read "pictogramme rotatif" as the same thing on the other device — a
rival the sweep missed. Is it one same thing?
Answer: Oui, une seule chose. **Indicateur de progression**, des deux côtés ; « pictogramme rotatif » (§4.4) disparaît.

### Q3
Terms: échouée, échec, réussite, succès
Question: the synchronisation states are named twice. §4.4 writes
"*Échouée* — message en `behind`", §5.2 writes "*Échec* —" and
"*Réussite* — retour à l'accueil normal", §12 writes "succès, échec, et
date de la dernière réussite" and the navigation diagram "succès │ échec".
I read one same set of three states — running, failed, succeeded —
named with two words each. Is that right?
Answer: Oui, trois états, un nom chacun : **en cours**, **échec**, **réussite**. « Échouée » (§4.4) et « succès » (§12) disparaissent.

⚠️ Une des occurrences citées n'appartient pas à cet ensemble. Dans le diagramme téléphone de §12, « succès │ échec » qualifie le résultat de l'**import** — « Importer » mène à l'Aperçu ou à l'écran d'erreur —, pas celui d'une synchronisation. Même paire de mots, deux contextes. Elle prend la même forme, mais ce n'est pas le même état.

### Q4
Terms: destination, prochaine étape
Question: the centre of the main screen during a Roxzone is called
"La prochaine étape : `→ SkiErg`" in the §6.2 table and "Destination
`→ SkiErg`" in the rendering table just below; §3.2 says "destination
de Roxzone" and §13.2 "Nom du segment, destination". I read one same
thing — what the runner is heading to — with "destination" in three
places and "prochaine étape" in one. Is it one same thing?
Answer: Oui, une seule chose. **Destination**, forme déjà majoritaire ; « prochaine étape » (§6.2) disparaît.

### Q5
Terms: zone courante, zone active, segment actif
Question: §6.3 writes "Le segment de la zone courante est plus épais",
§8.4 writes "le seuil entre la zone active et sa voisine immédiate". I
read "zone courante" and "zone active" as one same thing — the zone the
last heart-rate reading falls in — and "segment actif" as a distinct
thing, the arc element that draws it (§3.3, §6.3, §13.2). Is that the
reading?
Answer: Oui, c'est la lecture.

**Zone active** — la zone où tombe la mesure. « Zone courante » (§6.3) disparaît.
**Segment actif** — l'élément d'arc qui la dessine, distinct et conservé.

Les deux mots se répondent, ce qui rend le lien visible : le segment actif dessine la zone active.

### Q6
Terms: segment en cours, segment courant
Question: §6.2, §7.1 and §8.2 write "segment en cours" ; §11 writes
"L'instant d'ouverture du segment courant est écrit en base au
marquage". I read one same thing, the open segment. Is it?
Answer: Oui, une seule chose. **Segment en cours**, forme déjà majoritaire ; « segment courant » (§11) disparaît.

### Q7
Terms: départ, démarrage, coup de départ
Question: round 1 settled "démarrage" as the start of the race, by the
button « Démarrer ». The file also writes "départ" nine times for what
looks like the same instant: "L'écart cumulé depuis le départ" (§6.4),
"ouverte au départ, fermée à l'arrivée" (§10), "L'heure réelle n'est
enregistrée qu'une fois, au départ" (§11), "Profil au départ" (§13.2),
and §5.4 "**Démarrage**, au coup de départ. Le chrono part". I can read
it two ways: "départ" is the same instant as "démarrage", seen as a
point in time rather than as an action ; or "départ" is the real-world
gun and "démarrage" the application's answer to it, two things. Which
is it, and does "départ" stay?
Answer: C'est la première lecture : le même instant, vu comme un point dans le temps plutôt que comme une action.

**Départ** nomme l'instant, **démarrage** l'action qui le déclenche, **coup de départ** ce qui se passe dans la salle. Les trois restent, ils ne désignent pas la même facette.

🔴 Cette clarification révèle une contradiction à corriger, indépendante du vocabulaire. §10 écrit « une seule session d'exercice pour toute la course, ouverte au départ, fermée à l'arrivée », alors que §5.4 pose que « la session d'exercice s'ouvre à la préparation, pas au démarrage ». Si « départ » est l'instant du démarrage, les deux se contredisent. §10 devient : « ouverte à la préparation, fermée à l'arrivée ».

### Q8
Terms: écart final, écart cumulé
Question: the lexicon lists three distinct écarts — sur le RUN, cumulé,
par segment. §6.7 adds "l'écart final à la référence" and then says
"Son écart final est l'écart cumulé au dernier segment fermé" ; §13.3
lists "écart final" as a datum of the end screen. I read "écart final"
not as a fourth écart but as the écart cumulé frozen at the moment the
race ends — one same measure, at one moment. Is that right, and does
that moment keep a name of its own?
Answer: Oui, ce n'est pas un quatrième écart : c'est l'écart cumulé figé, et « écart final » reste le nom de cette valeur-là.

⚠️ Le moment ne peut pas s'appeler l'arrivée. §6.7 applique le même écart final à une course arrêtée en route, qui n'arrive jamais. Le moment est **la fin de la course**, terminée ou arrêtée.

### Q9
Terms: annuler, annulation
Question: "annuler" names two things. §6.1 : "Un relâchement avant la
durée de l'appui long annule le marquage et n'écrit rien", "Un
glissement de plus de 20 px pendant l'appui annule le marquage" — a
press that never records anything. §6.5 : "**Annuler le dernier
marquage.**", "L'annulation est à un seul niveau et porte sur le dernier
marquage" — the undo of a recorded marking. The vibration consigne of
§6.1, "deux impulsions brèves à l'annulation d'un marquage", could mean
either. I read two distinct things under one word, and the vibration
line as ambiguous between them. Are they distinct, which one vibrates
twice, and do both keep "annuler"?
Answer: Oui, deux choses distinctes, et une seule garde le mot.

**Annulation** reste à l'annulation d'un marquage enregistré (§6.5). C'est elle qui vibre deux fois.

Un relâchement avant la durée de l'appui long, ou un glissement de plus de 20 px, **n'enregistre rien** — il n'y a donc rien à annuler, et rien à confirmer par une vibration. §6.1 se reformule en ce sens.

📌 Un troisième emploi existe, que le balayage n'a pas relevé : « Annuler » est aussi le bouton de toutes les boîtes de confirmation — suppression, renommage, arrêt, reprise de session. C'est un texte affiché, il ne change pas.

### Q10
Terms: chrono, chronomètre, chronométrage, chrono officiel
Question: "chrono" appears on twelve lines — "Le chrono part", "Chrono
ou allure au centre", "Le chrono ne se replie jamais" — and
"chronomètre" on three — "Le chronomètre ne démarre qu'au démarrage"
(§5.4), "Chronomètre monotone" (§13.2). §11 is titled "Chronométrage".
§2 writes "Ce découpage est celui du chrono officiel". I read "chrono"
as the abbreviation of "chronomètre", the two naming one same thing —
the running timer — ; "chronométrage" as the activity of timing ; and
"chrono officiel" as another thing, the official race timing that
hyresult publishes. Is that the reading, and does the abbreviation stay
in prose?
Answer: La lecture est juste sur les trois sens, mais l'abréviation l'emporte, et l'inverse poserait problème.

**Chrono** reste en prose. Les trois « chronomètre » (§5.4, §13.2) passent à chrono.
**Chronométrage** reste pour l'activité, et garde le titre §11.
**Chronométrage officiel** remplace « chrono officiel » (§2).

⚠️ Le motif : §9 emploie « chronomètre » comme **verbe** — « la montre chronomètre normalement ». Imposer le substantif créerait une collision entre le nom et le verbe dans le même document.

### Q11
Terms: envoi, transfert montant, remontée, synchronisation
Question: §9 writes "un envoi unique" and "L'envoi descendant" for the
phone-to-watch direction, "Le transfert montant se fait en morceaux"
for the watch-to-phone direction ; §13.4 writes "À chaque import ou
remontée" ; §5.2 writes "elle déclenche l'envoi". I read
"synchronisation" as the whole, "envoi" as the downward direction, and
"transfert montant" and "remontée" as one same thing, the upward
direction. Is that right, and do both upward words stay?
Answer: **Synchronisation** nomme l'ensemble, **envoi descendant** et **envoi montant** les deux directions. Un seul mot, distingué par l'adjectif ; « transfert montant » et « remontée » disparaissent.

📌 §5.2 est imprécis et se corrige au passage : « elle déclenche l'envoi » devient « elle déclenche la synchronisation ». Depuis la montre, Synchroniser échange dans les deux sens.

### Q12
Terms: facteur de départ, facteur initial, valeur initiale
Question: §7.3 is titled "Valeur initiale et repli", opens with "Le
facteur de départ d'une course est le dernier facteur retenu", and its
table column reads "Facteur initial" ; §7.2 writes "`k_précédent` est
la valeur initiale". I read three names for one same thing — the
correction factor a race starts with. Is it one same thing?
Answer: Oui, une seule chose. **Facteur initial**.

« Facteur de départ » et « valeur initiale » disparaissent ; le titre §7.3 devient « Facteur initial et repli ».

### Q13
Terms: interrompue, arrêtée en route, incomplète
Question: §6.8 is titled "Course interrompue" and its body reads "Une
course arrêtée en route est enregistrée telle quelle et marquée
incomplète" ; §6.7 also writes "une course arrêtée en route" ; §5.4
writes "Le seul moyen d'interrompre une course est le bouton d'arrêt".
I read "interrompue" and "arrêtée en route" as one same event — the
runner stopping the race before the thirtieth marking — and
"incomplète" as the mark the recorded race carries afterwards, a
distinct thing. Is that the reading?
Answer: Oui, c'est la lecture.

L'événement est **l'arrêt**, la course est **arrêtée** — « arrêt » étant déjà tranché sans rival. « Interrompue » disparaît : le titre §6.8 devient « Course arrêtée », et §5.4 « la seule façon d'arrêter une course est le bouton d'arrêt ».

**Incomplète** reste, et désigne autre chose : la marque que porte la course enregistrée.

### Q14
Terms: cumul, temps cumulé
Question: §4.2 writes "leur durée et leur temps cumulé", then "en durée
comme en cumul" and "durée et cumul" ; §A.2 writes "Temps cumulé depuis
le départ" ; §C.5 writes "Cumul incohérent". I read "cumul" as the
abbreviation of "temps cumulé", one same thing. Is it, and does the
short form stay in prose?
Answer: Oui, une seule chose. **Temps cumulé** en prose.

La forme courte reste admise là où la place le commande — en-têtes de colonne, §B.6 — et dans le texte affiché « Cumul incohérent », qui ne change pas.

### Q15
Terms: durée, temps réel
Question: the measured time of a segment is "Durée du segment" in §A.2
("C'est la valeur stockée"), "durée" throughout §4.2 and §B, and
"temps_réel" in the §8.2 formula and "Temps réel vs référence" in
§13.2. I read "temps réel" and "durée" as one same measure, the actual
time spent in a segment — as opposed to its reference time. Is it one
same thing?
Answer: Oui, une seule mesure. **Durée**.

§13.2 devient « Durée vs référence », et §8.2 « puis pour sa durée une fois dépassé ». `temps_réel` reste tel quel dans la formule : c'est un identifiant de calcul, au même titre qu'`allure-segment`.

### Q16
Terms: horodatage, date et heure, nom automatique, nom généré
Question: §6.7 writes "le nom automatique de la course — sa date et son
heure" ; §13.3 lists "Temps total, écart final, horodatage" ; §C.2
writes "Le nom généré d'une course enregistrée par la montre suit le
format date et heure". I read "horodatage" and "date et heure" as one
same datum, and "nom automatique" and "nom généré" as one same thing —
that datum used as the race's name. Is that right?
Answer: Oui, c'est la lecture.

**Date et heure** nomme la donnée ; « horodatage » (§13.3) disparaît.
**Nom généré** nomme le nom ; « nom automatique » (§6.7) disparaît — « automatique » est déjà pris par la synchronisation et le retour d'écran.

### Q17
Terms: fréquence, fréquence cardiaque, fréquence maximale, fréquence cardiaque maximale, FC
Question: round 1 retired "FC" and "FC max" for "fréquence cardiaque"
and "fréquence cardiaque maximale". The short form "fréquence" alone
still stands in four places — "la fréquence en repli" (§5.4), "La
fréquence, son unité et le numéro de zone" (§6.2), "la fréquence en
battements par minute" (§6.3), "La fréquence a pu changer" (§8.4) — and
"fréquence maximale" twice in §4.4. Two "FC" remain in the §13.2 table :
"FC + profil", "Suit la FC". I read "fréquence" and "fréquence maximale"
as abbreviations of the retained terms, and the two "FC" as leftovers
of the retired one. Are the short forms accepted in prose, or do they
take the full term ; and are the two "FC" to be replaced?
Answer: La forme courte est admise **en reprise seulement** : « fréquence cardiaque » à la première mention d'un passage, « la fréquence » ensuite. Même règle pour « fréquence maximale ».

Écrire la forme complète trois fois dans « La fréquence, son unité et le numéro de zone » n'aiderait personne.

### Q18
Terms: mode normal, affichage normal, plein régime
Question: the lexicon names the opposite of "mode atténué" as
"affichage normal". §13.1 writes "sans nouvelle mesure en mode normal",
§6.9 writes "Retour au plein régime au lever de poignet". I read three
names for one same state. Is it one same thing?
Answer: Oui, un seul état. **Affichage normal**, déjà au lexique ; « mode normal » (§13.1) et « plein régime » (§6.9) disparaissent.

### Q19
Terms: référence courante, référence en cours, référence chargée
Question: §4.2 writes "badge de la référence courante", §5.2 "La
référence en cours" and "Sans référence chargée", §13.2 "Sans référence
chargée". I read "courante" and "en cours" as one same thing — the race
currently set as reference — and "chargée" as the watch's state of
having received it, which in practice designates the same race. Are
they one thing, or is "chargée" a distinct state?
Answer: Deux choses.

**Référence en cours** — celle qui est désignée. « Référence courante » (§4.2) disparaît.

**Chargée** reste, et désigne autre chose : l'état de la montre de l'avoir reçue. Une référence peut être en cours sur le téléphone sans être chargée sur la montre — c'est exactement ce que dit « Sans référence chargée ».

📌 Le mot est d'ailleurs affiché : « Référence chargée · <nom> » figure au catalogue des textes fixes.

### Q20
Terms: capteur d'exercice, exercice, session d'exercice
Question: round 1 settled "session d'exercice". §12 writes "uniquement
si une autre application occupe le capteur d'exercice" ; §10 writes "Le
système n'autorise qu'un exercice à la fois" and "une autre application
occupe la place". I read all three as the same thing — the system's
single exercise slot — "capteur d'exercice" being a slip, since what is
occupied is not a sensor. Is that right?
Answer: Oui, les trois désignent la même chose, et « capteur d'exercice » est bien un lapsus : ce qui est occupé n'est pas un capteur.

**Session d'exercice** partout. §12 devient « uniquement si une autre application a une session d'exercice en cours », §10 « Le système n'autorise qu'une session d'exercice à la fois ».

### Q21
Terms: mapping, table de correspondance
Question: §4.3 writes "Format, mapping, validation et échantillon
réel", §A.3 is titled "Mapping des noms" and its consigne writes "La
table de correspondance est explicite, jamais déduite". I read one same
thing — the table from pasted names to segments — in English and in
French. Is it one same thing?
Answer: Oui, une seule chose, et le français l'emporte. **Table de correspondance**.

Le titre §A.3 devient « Table de correspondance des noms » ; « mapping » disparaît de §4.3 et de §A.3.

### Q22
Terms: lecture, mesure
Question: a value delivered by a sensor is "une lecture" in §8.4 ("une
lecture qui en franchit deux", "la première lecture qui revient") and
"une mesure" in §13.1 ("sans nouvelle mesure"), §6.5 ("coupe le chrono
et les mesures") and §4.4 ("ses mesures cardiaques"). "Lecture" also
has a second sense, reading the pasted result (§A.4 "Lecture", "erreur
de lecture"). I read "lecture" and "mesure" as one same thing in the
sensor sense, and the import sense as a distinct thing. Is that the
reading?
Answer: Oui, c'est la lecture.

Côté capteur, une seule chose : **mesure**. « Lecture » ne garde que le sens de l'import, et n'a donc plus qu'un sens.

⚠️ Le verbe suit : §8.4 écrit « Toute fréquence lue tombe dans une zone » et « dès qu'une valeur est lue ». À reformuler en « toute fréquence mesurée », « dès qu'une valeur est mesurée ».

### Q23
Terms: erreur de lecture, échec de lecture, rejet
Question: the refused import is "Erreur de lecture" in the §12
diagram, "c'est une erreur de lecture" in §A.4, "Un échec de lecture
est un cas normal" in §A.6, "Un échec nomme la ligne fautive" in §A.5,
and "tous les rejets" in §C.5. I read one same thing under three
names. Is it?
Answer: Oui, une seule chose sous trois noms — mais la répartition n'est pas celle qu'on pourrait croire.

**Échec de lecture** nomme l'événement, en prose. « Rejet » (§C.5) disparaît, et « cause de rejet » devient « cause d'échec ».

📌 « Erreur de lecture » n'est **pas** un texte affiché : §C.5 liste huit titres et aucun ne porte ce nom. C'est le nom de l'écran, qui devient **écran d'erreur** — forme déjà employée en §4.3 et au catalogue des textes fixes.

### Q24
Terms: liste résumée, liste des courses résumée
Question: §12 writes "Liste résumée", §9 "la liste des courses
résumée", §5.3 "La liste des courses en version résumée". I read
"liste résumée" as the abbreviation of "liste des courses résumée",
one same thing — the watch's list. Is it, and does the short form stay?
Answer: Oui, une seule chose. **Liste des courses résumée** à la première mention d'un passage, **liste résumée** en reprise. Même règle qu'en Q17.

§5.3 « en version résumée » prend la forme retenue.

### Q25
Terms: marque visible, badge, marquée, marquage
Question: §4.1 writes "La course de référence porte une marque visible"
and "Une course incomplète est marquée comme telle" ; §6.5, §6.8 and
§C.4 write "marquée incomplète". I read "marque visible" as the badge
« Référence » the lexicon settled, and "marquée" as the plain verb for
flagging a race — distinct from "marquage", the retained term for the
long press. Is "marque visible" the badge, and is "marquée" to be read
apart from "marquage" ?
Answer: Oui sur le premier point : « marque visible » est bien le badge. §4.1 devient « porte le badge « Référence » ».

⚠️ Non sur le second, et il ne faut pas y toucher. « Marquée incomplète » figure dans un **texte affiché** — « Elle sera enregistrée telle quelle, marquée incomplète. » Modifier la prose créerait une divergence entre ce qui est écrit et ce qui s'affiche.

**Marquer** au sens de signaler reste donc, et cohabite avec **marquage**, comme « segment », « position » et « écran » cohabitent déjà avec eux-mêmes.

### Q26
Terms: ligne
Question: one word, several things : a row of the pasted result
("ligne <n>", "Exactement 30 lignes de données", §A.5, §C.5), a row of
the detail screen ("Les trente lignes restent affichées", "Chaque
ligne : nom en `p-data`", §4.2), a row of the watch list ("Une ligne
par course", §5.3), and the finish line ("sprint vers la ligne", §2). I
read the first two as the ones the product handles, distinct from each
other. Are they distinct, and do both keep "ligne" ?
Answer: Les deux premiers sens sont bien ceux que le produit manipule, mais ce sont des rangées dans les deux cas — d'un résultat collé, d'un écran de détail, de la liste de la montre. Le contexte suffit : un seul sens, **une rangée**.

📌 Un troisième sens existe, que le balayage n'a pas relevé : la ligne de texte en mise en page — « texte sur trois lignes maximum », « sur une seule ligne », « jamais réduit sur plusieurs lignes », le jeton « Lignes de segment ». Il reste, et « ligne » porte donc **deux sens distingués**, comme « segment » et « position ».

La ligne d'arrivée, elle, disparaît : §2 devient « sprint vers l'arrivée ».

### Q27
Terms: bpm, battements par minute, min/km, minutes par kilomètre
Question: two units are written in two forms each. §6.3 writes "la
fréquence en battements par minute", §8.4 and §4.4 write "3 bpm",
"230 bpm" ; §7.1 and §8.3 write "minutes par kilomètre", §6.2 and §15
write "min/km". `bpm` and `/km` are the displayed forms. I read each
pair as one same unit, long and short. Is that right, and which form
holds in prose ?
Answer: Oui pour `bpm`, et la règle du lexique s'applique : **battements par minute** en prose, `bpm` dans les textes affichés seulement.

⚠️ Non pour l'autre paire, et c'est une erreur de prémisse : la forme **affichée** n'est pas `min/km` mais `/km` — l'unité est détachée de la valeur, `6:00` `/km`.

« min/km » n'est donc ni la forme longue ni la forme affichée : c'est une abréviation de prose sans statut. Elle disparaît. **Minutes par kilomètre** en prose, `/km` à l'écran.

### Q28
Terms: heure de départ, heure réelle
Question: §11 writes "L'heure réelle n'est enregistrée qu'une fois, au
départ" ; §A.2 and §A.4 write "heure de départ". I read one same datum —
the wall-clock time at which the race started. Is it?
Answer: Oui, une seule donnée. **Heure de départ**.

§11 devient « L'heure de départ n'est enregistrée qu'une fois. » — plus court et plus clair, le complément étant devenu redondant.

### Q29
Terms: Lancer, Historique, Synchroniser, Quitter, Démarrer, Terminer, Contrôle, Wall Balls
Question: these reach the screen character for character and the
lexicon lists them as displayed texts, yet the file writes them in
bold without quotes — "**Lancer**, un gros bouton au centre",
"**Historique** et **Synchroniser**" (§5.2), "Un bouton **Quitter**",
"**Démarrer** demeure actif" (§5.4), "Bouton **Terminer**" (§6.7) — or
bare : "le titre Contrôle" (§3.2), "Le nom affiché est Wall Balls"
(§6.2), and Lancer, Historique, Synchroniser, Démarrer in the §12
diagrams. I read them all as displayed texts lacking their quotes. Is
that the reading?
Answer: Déjà tranché au tour 1.

### Q30
Terms: `Référence`, `Incomplète`, `CYCLE n`, `Historique`, `Contrôle`, `Réf. 4:26`, `→ SkiErg`, `14/30`, `RUN`, `STATION`, `ROX_IN`, `ROX_OUT`
Question: backticks carry three kinds of thing in the file — tokens
(`surface`), identifiers (`allure-segment`), and displayed texts :
"Badge `Référence`", "badge `Incomplète`" (§4.1), "en-tête `CYCLE n`"
(§4.2), "Titre `Historique`" (§5.3), "Titre `Contrôle`" (§6.5),
"`Réf. 4:26`", "`→ SkiErg`" (§6.2), "Position `14/30`" (§13.2). And the
reverse : `RUN`, `STATION`, `ROX_IN`, `ROX_OUT` (§7.1, §8.1, §A.3) are
concepts — the displayed form of a RUN is "Run 3", of a station its
name — yet they carry the same mark. I read the first group as
displayed texts and the second as concepts, both mis-marked. Is that
the reading, and should the displayed ones carry « » ?
Answer: Déjà tranché au tour 1.

### Q31
Terms: « Aucune référence », « ⚠ Aucune référence »
Question: one displayed text, two forms. Without the sign : "elle
affiche « Aucune référence »" (§4.4), "Sans référence chargée :
« Aucune référence »" (§5.2), "Badge « Aucune référence »" (§13.3).
With it : "un badge « ⚠ Aucune référence »" (§5.2 rendering), §C.2,
§C.4. The same question as round 2's Q8 on « Réf. » : which form
reaches the screen ?
Answer: **Avec le signe**, partout : « ⚠ Aucune référence ».

C'est un badge d'alerte et le signe porte l'alerte ; sans lui, il se lit comme une mention ordinaire. §4.4, §5.2 et §13.3 prennent cette forme.

### Q32
Terms: « Ouvre l'application sur ton téléphone pour envoyer ton profil »
Question: §5.1 writes it without a final period, §C.4 with one — "Ouvre
l'application sur ton téléphone pour envoyer ton profil." A displayed
text is one string, character for character. Which form holds ?
Answer: Même texte.
