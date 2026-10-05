# Questions — lexicographe — tour 10

Balayage de `idees.md` après les neuf tours tranchés. Les termes ci-dessous
n'ont été ni posés ni notés dans `lexique.md` ; ceux que `## Tranché` règle
n'ont pas été reposés. Questions en anglais, réponses en français.

### Q1
Terms: écran non interactif, mode atténué
Question: §10 says "Quand l'écran n'est pas interactif, les données sont livrées par paquets plutôt qu'en continu." Everywhere else the reduced state of the watch is named "mode atténué" (§3.4, §6.9, §13.1, §13.2 — "Continu, ou 10 s en mode atténué"). Is the screen "not interactive" the same state as the mode atténué — one thing, with §10 naming it by what the platform calls it — or a distinct state (the platform can deliver batched data outside the mode atténué, or the mode atténué can be on while the screen is still interactive)? I read them as one same state named twice: §13.2 gives the fréquence cardiaque a 10 s update "en mode atténué", which is the batched delivery §10 describes.
Answer: Une seule chose, et §13.2 le prouve en donnant à la fréquence cardiaque une cadence de dix secondes « en mode atténué » — c'est très exactement la livraison par paquets que §10 décrit.

**Mode atténué** le nomme. §10 devient : « En mode atténué, les données sont livrées par paquets plutôt qu'en continu. »

📌 « Écran non interactif » est le vocabulaire de la plateforme, pas celui du produit. Le garder ferait dépendre une consigne d'un mot que le document n'a jamais défini — et qu'il faudrait alors relier au mode atténué pour être compris.

### Q2
Terms: Référence synchronisée, référence chargée
Question: §13.2 gives "Référence synchronisée" as the provenance of the temps de référence du segment, once. The state of the watch having received the reference is settled as "référence chargée" (§5.2 "Sans référence chargée", §13.2 consigne "Sans référence chargée, quatre blocs disparaissent"). Is the "référence synchronisée" the same thing as the référence chargée — the reference as the watch holds it after an envoi descendant — or does "synchronisée" name something else (the act of the last synchronisation as a source, like "Dernière synchronisation" in §13.3)? I read them as one same thing, the provenance column naming the loaded reference by the way it arrived.
Answer: Une seule chose : la référence telle que la montre la détient après un envoi descendant.

**Référence chargée** la nomme, forme déjà employée deux fois — et c'est celle qui permet aux deux lignes de se répondre : la provenance dit d'où vient la donnée, la consigne juste en dessous dit ce qui arrive quand elle manque. Deux noms pour un état rendraient ce lien illisible.

§13.2 devient « Référence chargée ».

⚠️ À distinguer de « Dernière synchronisation » (§13.3), qui est bien une autre provenance : là, c'est l'événement qui est la source, pas la donnée qu'il a apportée.

### Q3
Terms: indisponible, en repli
Question: §13.2, row "Distance mesurée", column Repli: "Allure indisponible". Elsewhere an allure that cannot be shown is "en repli" (§7.1 "sous 50 mètres mesurés dans le segment, allure-segment est en repli", "sous 3 secondes de données, elle est en repli" ; §8.3 "tant que l'une des deux allures est en repli"), and the next row of §13.2 gives allure-segment's own repli as `—:—`. Is "Allure indisponible" the allure en repli — the same state, named once by another word — or a distinct state (the allure cannot even be computed, as opposed to computed but not shown)? I read them as one same state: a distance mesurée absente puts the allure en repli, and §13.2 is describing that consequence. "Synchronisation indisponible" (§4.4, displayed text) is another matter and is not asked.
Answer: Un seul état, et la ligne décrit une conséquence, pas une seconde chose.

**En repli** le nomme, forme déjà employée trois fois par §7.1 et §8.3 — et la ligne suivante de ce même tableau donne à `allure-segment` un repli `—:—`, ce qui achève de le montrer.

§13.2 devient « Allure en repli ».

La distinction que tu envisages — calculée mais non montrée, ou pas calculable du tout — n'existe nulle part dans le document : le repli est toujours le fait de ne pas montrer, quelle qu'en soit la cause.

### Q4
Terms: pourcentage, seuil
Question: §4.4 defines "Quatre seuils de zone, en pourcentage de la fréquence cardiaque maximale", then the rendering says each zone line shows "libellé, pourcentage et plage" and "La zone 1 n'a pas de pourcentage à elle — elle commence là où le premier seuil s'arrête". §B.4 lists the format "Pourcentage de zone | entier + espace insécable + % | 60 %" beside "Plage de zone", "Durée de l'appui long". Is the "pourcentage" the seuil de zone itself as it is displayed — one same datum, named by its unit in the rendering and in the format table — or a distinct datum? I read them as one same thing: the seuil is the value, "%" is its unit, and the zone line shows the seuil of the zone it opens.
Answer: Une seule donnée : le **seuil**. Le pourcentage en est l'unité, comme `bpm` l'est de la fréquence cardiaque.

§4.4 et §B.4 restent lisibles tels quels — « en pourcentage de la fréquence cardiaque maximale » dit l'unité, « Pourcentage de zone » nomme un format par son unité, ce que fait aussi « Durée de l'appui long » avec ses millisecondes.

Le rendu gagne en revanche à nommer la valeur : « carré de couleur, libellé, seuil et plage » plutôt que « pourcentage et plage », et « La zone 1 n'a pas de seuil à elle » — ce qui est d'ailleurs plus exact, puisque c'est bien un seuil qui lui manque, pas une unité.

### Q5
Terms: ajoutée, créée
Question: §4.1: "À date identique, la course ajoutée le plus récemment passe en premier — le critère est interne, jamais affiché." §4.4 says "Une course déjà créée est figée", and the lexicon records that "créée" covers both origins, import and montre, without being a term. Does "ajoutée" in §4.1 name the same event — the course entering the base locale, whether by import or by envoi montant — or only the import, since "ajout" is settled as the bouton d'ajout that opens the import screen (§4.1, §4.4)? I read "ajoutée" as the same event as "créée", covering both origins, because the tie-break must order watch courses as well as imported ones ; the word borrows from "bouton d'ajout" but does not mean the button.
Answer: Ni l'un ni l'autre n'est un terme : ce sont des participes, ils ne nomment aucune entité. Les deux phrases restent lisibles telles quelles, et « ajoutée » couvre bien les deux origines — le départage l'impose, puisqu'il doit ordonner deux courses de la montre à date identique aussi bien que deux imports.

📌 La question en cache une autre, celle-là sur une donnée que le code devra construire. Trier « la course ajoutée le plus récemment » suppose **un ordre d'insertion** — un identifiant croissant, ou l'instant d'écriture en base. §4.1 le désigne aujourd'hui par une périphrase et le qualifie de critère interne, mais ne le nomme pas.

C'est cette donnée qui mérite une entrée, pas le participe.

### Q6
Terms: complète, incomplète
Question: §9: "L'envoi montant se fait en morceaux. La course n'apparaît sur le téléphone que complète ; un envoi interrompu reprend depuis le début." The mark "incomplète" is settled as the mark of a course arrêtée (§6.7, §6.8, §4.1). Does "complète" in §9 mean entirely transferred — all its morceaux received, whatever the course's mark — or the opposite of the mark, so that a course arrêtée and marquée incomplète would not appear on the phone? I read it as entirely transferred, one word carrying another meaning than the mark: the sentence is about the envoi, and a course incomplète has to reach the phone to be listed (§4.1 "Une course incomplète est marquée comme telle"). "la référence complète avec ses 30 segments" (§9) and the displayed "Le collage est incomplet", "un résultat Hyrox complet" (§C.5) are read the same way — complete data, not the mark.
Answer: Un autre sens, et la lecture est juste : §9 parle de l'envoi, pas de la marque.

**Complète** y signifie entièrement transférée. Une course arrêtée doit atteindre le téléphone pour y figurer, et §4.1 dit précisément qu'elle y est marquée incomplète — les deux phrases seraient contradictoires sous l'autre lecture.

Les trois autres emplois que tu cites vont dans le même sens : la référence complète avec ses 30 segments, le collage incomplet, un résultat Hyrox complet. Tous disent une donnée entière ou tronquée, jamais une marque.

📌 Une précision vaut d'être ajoutée à §9, pour que la phrase ne puisse plus se lire autrement : « La course n'apparaît sur le téléphone qu'entièrement transférée ».

### Q7
Terms: flèche de tendance, flèche
Question: "flèche" is settled without rival, and in seventeen places it is the flèche de tendance — the up or down arrow beside the allure (§3.1, §6.2, §7.1, §8.3, §13.2, §15). One place uses the word for something else: §6.2, rendering of the destination — "Destination `→ SkiErg` | font-label, w-value — la flèche seule à 0,85 d'opacité, le nom en text-primary à pleine opacité" — where the flèche is the `→` character of the displayed destination. Are these two distinct things sharing a word, like "segment", "position" and "ligne" already do — an element with its own colour and state on one side, a character of a displayed text on the other? I read them as two distinct things: one is masked, coloured `ahead` or `behind`, and has a direction; the other is a glyph that never changes and belongs to the text `→ SkiErg`.
Answer: Pas deux termes : un terme et un caractère.

**Flèche de tendance** nomme un élément que le code construit — une direction, une couleur de sens, une zone morte, un masquage.

Le `→` de §6.2 n'est rien de tout cela : c'est un caractère à l'intérieur de la chaîne `→ SkiErg`, qui vit dans les ressources. Le code n'en construit rien, ne le colore pas, ne le masque pas.

Le rapprochement avec « segment », « position » et « ligne » ne tient donc pas : ces trois-là portent deux choses réelles chacune, ici il n'y en a qu'une.

§6.2 se reformule pour que le mot n'y figure plus : « le caractère `→` à 0,85 d'opacité, le nom en `text-primary` à pleine opacité ». La flèche de tendance reste alors la seule flèche du document.

### Q8
Terms: cercle, pilule
Question: §4.1 rendering: "icône profil et bouton `+` alignés à droite, cercles de 36–38 dp bordés border-strong". The lexicon settles "pilule" as the shape of every button — "aucun bouton d'une autre forme n'existe dans le document" — with `radius-pill` at half the height. Is the bouton d'ajout's "cercle" a pilule whose width equals its height — one same shape, described by its outline here — or a distinct shape, a third one beside pilule pleine and pilule bordée? I read it as one same shape: a 36 dp circle is what `radius-pill` produces on a square button, and the two elements are "bordés border-strong" like a pilule bordée.
Answer: Une seule forme. Un cercle est ce que `radius-pill` produit sur un bouton carré : la moitié de la hauteur d'un carré de 36 dp donne un rayon de 18 dp, donc un disque.

La lecture est confirmée par le rendu lui-même — les deux éléments sont « bordés `border-strong` », exactement comme une pilule bordée.

§4.1 reste lisible tel quel : il décrit la géométrie obtenue, il n'introduit pas une troisième forme. Écrire « pilules de 36–38 dp » sur des boutons carrés serait plus exact et moins clair.

### Q9
Terms: retour, geste de retour du système
Question: In the watch diagram of §12, "retour" stands alone twice: "Préparation │ └── retour ──► Accueil" and "écran Historique ──► retour ──► Accueil". The lexicon settles "geste de retour du système" as the full form and "geste de retour" as its reprise. From Historique, the geste is the only way back ; from Préparation, §5.4 gives the button « Quitter » and §6.6 says the geste also works there. Is "retour" alone in the diagram a second reprise of the geste de retour du système, or the generic act of coming back to the previous screen, by whatever means — the geste or a button? I read it as the generic act, not the geste: under Préparation the arrow must cover « Quitter », which the diagram draws nowhere else. "retour automatique à l'écran principal" (§6.1, §12) and "retour écran principal" after the bouton d'annulation (§12) are read as the same generic act and are not asked.
Answer: L'acte générique, et l'argument est décisif : sous Préparation, la flèche doit couvrir « Quitter », que le diagramme ne dessine nulle part ailleurs.

**Retour** nomme donc le fait de revenir à l'écran précédent, par quelque moyen que ce soit — un geste ou un bouton. Il ne se confond pas avec le **geste de retour du système**, qui est l'un de ces moyens.

Les deux flèches de §12 restent telles quelles, et « retour automatique à l'écran principal » comme « retour écran principal » portent le même sens générique.

⚠️ Une nuance mérite d'être notée : depuis l'écran Historique, ce retour générique n'a qu'un seul moyen, le geste. Le diagramme est juste, mais il ne le dit pas — et §5.3 ne mentionne aucun bouton pour en sortir.
