# Questions du lexicographe — premiere-app-2

**Tour 1 — traité.** Les 36 entrées du premier balayage ont reçu une
réponse ; elles ont été appliquées à `idees.md` et leurs décisions sont
inscrites dans `lexique.md`, section `## Tranché`.

**Tour 2 — traité.** Les dix entrées ci-dessous ont reçu une réponse ;
elles ont été appliquées à `idees.md` et leurs décisions sont inscrites
dans `lexique.md`, section `## Tranché`. Une seule entrée nouvelle en
est ressortie — les deux sens de « cadran », signalés par la réponse Q6
elle-même — et elle attend le balayage du tour suivant, sous
`## Non tranché`.

---

### Q1
Terms: transition
Question: your answer to Q3/Q4 settled "Roxzone" as the zone de
transition, made of the two distinct moments ROX_IN and ROX_OUT, and
that is now written down. §11 still writes "**Une transition est
atomique** : fermer le segment précédent et ouvrir le suivant se font
en une seule écriture." I read this second use as another thing
entirely — the instant one segment closes and the next opens, which is
not a Roxzone and happens at every one of the thirty markings. Is it a
distinct thing, and does it keep the word "transition"?
Answer: Oui, c'est une autre chose — mais elle a déjà un nom, et ce n'est pas un renommage à inventer.

§11 décrit ce que le **marquage** enregistre. Le lexique a tranché « marquage — retenu, remplace : avancement (le bouton et ce qu'il enregistre sont une seule chose) », et le paragraphe lui-même emploie déjà le mot quatre lignes plus bas : « L'instant d'ouverture du segment courant est écrit en base au marquage ».

« Transition » reste donc à la Roxzone seule.

§11 devient : « Un marquage est atomique : fermer le segment précédent et ouvrir le suivant se font en une seule écriture. »

### Q2
Terms: activité, indicateur d'activité
Question: your answer to Q10 settled "session d'exercice" as the name
of the exercise the watch opens, and "activité" now points at it. §5.2
still writes "*En cours* — indicateur d'activité et « Ne ferme pas
l'application »." I read that one as a third thing — the spinner shown
while a synchronisation runs, which has nothing to do with an exercise
session. Is it a distinct thing, and does it keep the word "activité" ?
Answer: Oui, troisième chose, et elle ne garde pas le mot.

Le témoin qui tourne pendant une synchronisation s'appelle **indicateur de progression**. « Progression » est libre dans le lexique ; « activité » reste à la session d'exercice, et les deux textes affichés « Arrêter l'activité » et « Une autre activité est en cours » ne changent pas.

§5.2 devient : « *En cours* — indicateur de progression et « Ne ferme pas l'application ». »

### Q3
Terms: seuil
Question: your answer to Q12 settled "seuil" for a heart-rate zone
limit and sent the long press to "durée de l'appui long". §13.1 still
writes "Au-delà de **10 secondes** sans nouvelle mesure en mode normal,
une donnée issue d'un capteur — fréquence cardiaque, distance — repasse
au repli [...] En mode atténué, le seuil est celui de la cadence de
rafraîchissement". I read this third use as the staleness delay, a
distinct thing; keeping the word "seuil" there would give one word two
meanings again. Is it distinct, and does it keep "seuil" ?
Answer: Oui, distinct, et il ne garde pas le mot.

Le délai au-delà duquel une mesure cesse d'être affichée s'appelle **délai de péremption**.

« Seuil » reste aux bornes des zones, « borne » aux limites d'un réglage, « durée de l'appui long » à l'autre emploi. « Délai » est libre, et « péremption » est déjà le mot que le lexique emploie pour décrire ce concept.

§13.1 devient : « [...] repasse au repli. En mode atténué, le délai de péremption est celui de la cadence de rafraîchissement. »

### Q4
Terms: reprise, rappel
Question: your answer to Q13 settled that resuming our own race and the
screen that stops another application's session are one same thing —
"reprise" — and that re-asking a permission is something else. §5.1
still writes "La demande n'est jamais rejouée d'elle-même — un rappel
sur l'écran d'accueil est la seule reprise, et c'est une action." That
sentence names the permission thing twice, "rappel" and "reprise". I
read "rappel" as the one that holds there, "reprise" being now taken.
Is that right?
Answer: Oui, c'est « rappel » qui tient.

Le lexique le dit déjà : « la relance d'une demande d'autorisation est une autre chose ». « Rappel » est libre, et §5.1 l'emploie déjà.

Reformuler pour que « reprise » n'y figure plus : « La demande n'est jamais rejouée d'elle-même — un rappel sur l'écran d'accueil est le seul moyen de la relancer, et c'est une action. »

### Q5
Terms: collage, import
Question: your answer to Q25 confirmed that "collage" and "import" name
one same operation. Both words reach the screen — « Coller un
résultat » and « Revenir au collage » on one side, « Importer » on the
other — so the displayed texts settle nothing: the operation still
needs one name in the prose and in the code. Which of the two names it?
Answer: **Import** nomme l'opération, dans la prose comme dans le code. « Collage » disparaît de la prose.

Le tour 1 a établi qu'il s'agit d'une seule opération : garder deux mots la contredirait. « Import » couvre tout le geste — coller, valider, enregistrer — là où « collage » ne décrit que la saisie. Il est déjà partout dans le corpus : « course importée », « une course importée est presque toujours antérieure ».

Les trois textes affichés ne changent pas : « Coller un résultat », « Revenir au collage », « Importer ». C'est le même cas que « Historique ».

### Q6
Terms: badge, pastille
Question: your answer to Q28 said these are distinct things and that
the vocabulary has to be made more precise. I read four elements
carrying those two words: the tinted text label (« Référence »,
« Incomplète », the delta badge), the round icon at the top of the
confirmation dialogs (`!`, `✓`), the small square colour swatch on each
of the five zone lines of the profile, and the system indicator on the
watch face that returns to the application. Which name does each of the
four take?
Answer: Le compte est juste, mais le problème est plus large : dans le corpus, « pastille » nomme **trois** de ces quatre éléments, pas un seul.

**Badge** — l'étiquette de texte teintée : « Référence », « Incomplète », l'écart sur les écrans de course. Toujours du texte, toujours sur fond teinté, `radius-chip`.

**Pastille** — l'icône ronde en tête des confirmations : `!` sur `behind`, `✓` sur `ahead`. Jamais de texte, toujours un symbole.

**Carré de couleur** — le repère qui précède chaque ligne de zone sur l'écran de profil, écrit aujourd'hui « pastille carrée ».

**Raccourci système** — l'élément que le système affiche pendant une course et qui ramène à l'application, écrit aujourd'hui « pastille sur le cadran ». Il n'appartient pas à l'application : c'est le système qui le dessine.

Une entrée manque au balayage : **« cadran » porte deux sens**. Le cercle de l'écran, dans la géométrie de l'arc — « cinq arcs concentriques au cadran », « centré sur le bas du cadran » — et la face de la montre, dans « une pastille sur le cadran ». À traiter au tour suivant.

### Q7
Terms: carte, encart
Question: your answer to Q29 confirmed that "carte" and "encart" name
one same raised container — `surface-raised`, `radius-card`. Neither
word reaches the screen, so nothing settles which one holds: §3.1 lists
both, §4.1 uses "carte" for a race in the list, §4.3 uses "encart" for
the boxed sample line. Which of the two names it?
Answer: **Carte** nomme le conteneur en relief, partout. « Encart » disparaît.

Le jeton s'appelle déjà `radius-card`. « Encart » ne subsiste qu'à deux endroits, pour la boîte qui illustre la ligne erronée — le même conteneur qu'une carte de course.

§4.3 devient « une carte `surface-raised` montrant la ligne erronée », et « L'encart est une illustration » devient « Cette carte est une illustration ».

### Q8
Terms: Réf.
Question: your answer to Q35 said the two displayed forms have to be
harmonised — « Réf. — Bordeaux 2025 · 1:37:25 » on the home screen,
« Réf. 4:26 » during a race. Both are displayed texts, so the form is
yours to fix, not mine. Which one holds — the em dash everywhere, or no
dash anywhere?
Answer: **Sans tiret, partout.** « Réf. Bordeaux 2025 · 1:37:25 » sur l'accueil, « Réf. 4:26 » pendant une course.

C'est le contexte le plus contraint qui décide : sur un écran d'un pouce et demi, en course, en `w-label`, deux caractères de moins valent mieux qu'une ponctuation soignée. Et le lexique applique déjà cette logique à « arrivée estimée » — seule forme affichée.

### Q9
Terms: lancement
Question: your answer to Q30 settled "lancement" as the opening of the
exercise session, by the button « Lancer », and "démarrage" as the
start of the race, by « Démarrer ». §4.4 and §5.1 both write
"L'autorisation est vérifiée à chaque lancement", where "lancement"
means the application being opened — a third thing, neither a session
nor a race. I read it as distinct. Is that right, and does it keep the
word "lancement" ?
Answer: Oui, troisième chose — mais elle ne prend pas de nom du tout.

Nommer cette chose créerait un conflit de plus : « ouverture » est déjà employé dans la définition de « lancement » — l'ouverture de la session d'exercice — et dans le titre §5.1, « Première ouverture ».

La phrase se reformule sans terme : « L'autorisation est vérifiée chaque fois que l'application s'ouvre. » Une tournure verbale ne crée pas de terme et ne peut donc pas entrer en conflit.

§4.4 et §5.1 prennent cette forme. « Lancement » reste à la session d'exercice, « démarrage » à la course.

### Q10
Terms: station Wall Balls, STATION
Question: your answer to Q5 said the thirtieth segment is the Wall
Balls station and that "bloc final" and `FINAL_BLOCK` are to be
transformed keeping the word "station". I applied it: §2 now reads "30.
la station Wall Balls — Roxzone, Wall Balls, sprint vers la ligne", and
§A.3 maps `Total time` to `STATION` du cycle 8. I read this as the
right transformation, the segment keeping inside it the Roxzone and the
sprint that §2 describes. Is that the reading?
Answer: Oui, c'est bien la lecture.

Le segment ne change pas de contenu : il contient toujours la Roxzone d'entrée, les Wall Balls et le sprint vers la ligne. Seul son nom change, et c'est le nom de ce qui s'y fait d'essentiel.

Deux conséquences à vérifier :

L'écran principal traite ce segment **comme une station** — nom en haut, temps écoulé au centre. C'était déjà la décision, et elle devient plus naturelle avec ce nom.

Le découpage compte huit cycles, le dernier n'en portant que deux segments : RUN 8 puis la station Wall Balls. Le total reste de trente. Toute formule qui supposait « sept cycles complets puis un bloc final » est à relire.
