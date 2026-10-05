# Questions — lexicographe, tour 13

Balayage de `idees.md`, `## Tranché` lu d'abord. Quatre paires que les
douze tours n'ont pas posées ; aucun guillemet douteux nouveau.

### Q1
Terms: profil (l'écran), profil (la donnée)
Question: One word, two things? I read "profil" as naming both the phone screen and the set of data the phone sends to the watch. The screen: §4.4 is titled "Profil", "l'écran de profil affiche « Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé. »" (§4.4), "Même principe sur le téléphone, depuis le profil." (§5.2), "Exactement le comportement du bouton « Autoriser » du profil (§4.4)" (§5.1), the node "Profil" of the phone diagram (§12), "Proposée au premier affichage du profil" (§13.4), the rows "Profil" of §C.4. The data: "Le facteur initial d'une course est **le dernier facteur retenu, toutes courses confondues**, conservé dans le profil." (§7.3), "Le facteur est stocké **dans le profil**, pas rattaché à une course" (§7.3), "un envoi unique contenant le profil, la référence complète avec ses 30 segments, et la liste des courses résumée." (§9), "s'affiche à la place de l'accueil tant qu'aucun profil n'a été reçu." (§12), "Fréquence cardiaque + profil" and "Profil au départ, puis calcul en fin de RUN" (§13.2, colonne Provenance), and the displayed text "envoyer ton profil" (§5.1, §C.4). The watch receives the data and never shows the screen, so the two never meet on the same device — yet the code will name both. The lexicon holds "profil — retenu, sans rival", which settles the word against rivals, not the two meanings. Do you read them as two distinct things under one word, the context sufficing — as for "segment", "position", "ligne", "écran" — or as two things to hold apart, as "Historique" (the watch screen) was held apart from "liste des courses résumée" (the data it shows) at tour 8? The lexicon needs to say which, so the Rédacteur writes one concept or two.
Answer: Deux choses à tenir à part, comme Historique et liste des courses résumée.

Le critère tranche : le code construit les deux, et séparément. L'écran est une destination de navigation ; la donnée est ce qui part dans l'envoi descendant, se stocke des deux côtés, et porte le facteur de correction. La montre construit la seconde et ne connaîtra jamais la première.

**Profil** reste à la donnée — c'est elle qui circule, se stocke et se lit dans les deux applications, et c'est elle que le lexique doit nommer d'un mot court.

L'écran devient **écran Profil**, nommé en entier partout où il est nommé, comme les six écrans du tour 8.

§4.4 garde son titre de section, §5.2 devient « depuis l'écran Profil », §12 nomme le nœud « écran Profil », §13.4 « au premier affichage de l'écran Profil », §C.4 conserve ses lignes « Profil » — la colonne y nomme des écrans, le contexte est posé.

📌 Que les deux ne se rencontrent jamais sur le même appareil est vrai, mais ne suffit pas : le Rédacteur écrit un seul document pour les deux applications.

### Q2
Terms: supprimer, effacer
Question: Two distinct things, or one under two verbs? §4.2: "C'est le seul endroit de l'application où une course se supprime." §5.3: "une course ne s'y supprime ni ne s'y renomme." §9: "La montre n'efface une course qu'après confirmation explicite de réception. Elle réapparaît ensuite dans la liste des courses résumée descendante." — one occurrence of "effacer" in the whole file. I read them as two distinct things: the suppression is the user's act, on the phone, in Détail d'une course, and the course ceases to exist on both devices; what §9 calls "effacer" is the watch clearing its own copy of a course once the phone has confirmed it holds it — the course survives, on the phone, and comes back to the watch in the resumed list. Under a single verb, the consigne of §4.2 ("le seul endroit … où une course se supprime") would read as contradicted by §9, where the watch removes a course on its own. §9 also says of a suppression's effect on the watch: "Une course supprimée sur le téléphone disparaît de la montre à l'envoi suivant." — and the displayed text "La course disparaîtra aussi de l'historique sur la montre." — "disparaître" as the visible consequence, which I read as prose, not a third operation. Do you confirm two operations, each with its own word?
Answer: Deux opérations distinctes, chacune avec son verbe, et c'est la consigne de §4.2 qui l'impose.

**Supprimer** — l'acte de l'utilisatrice, sur le téléphone, dans Détail d'une course. La course cesse d'exister, des deux côtés.

**Effacer** — la montre retire sa propre copie une fois la réception confirmée. La course survit sur le téléphone et revient à la montre dans la liste des courses résumée descendante.

Sous un seul verbe, « le seul endroit de l'application où une course se supprime » deviendrait faux : §9 décrit exactement un autre endroit où une course disparaît de la montre.

**Disparaître** est bien de la prose, et le reste : c'est la conséquence visible d'une suppression, pas une troisième opération. §9 l'emploie comme le texte affiché « La course disparaîtra aussi de l'historique sur la montre ».

### Q3
Terms: mise à jour, rafraîchissement
Question: Two distinct things, or one? "Mise à jour" is the column of the three tables of §13 and the section's title, "Provenance, mise à jour, repli"; its cells say when a datum takes a new value — "Continu", "À chaque marquage", "Après chaque RUN", "À chaque synchronisation", and for the fréquence cardiaque "Continu, ou 10 s en mode atténué" (§13.2). "Rafraîchissement" appears twice: "Rafraîchissement en mode atténué : **dix secondes**, et non la valeur par défaut d'une fois par minute." (§6.9) and "En mode atténué, le délai de péremption est celui de la cadence de rafraîchissement, soit 10 secondes également." (§13.1). I read them as two distinct things: the mise à jour is a property of each datum — the moment its value changes; the rafraîchissement is the cadence at which the screen is redrawn in mode atténué, one value for the whole display, which the code sets against the platform's default. They coincide on the fréquence cardiaque in mode atténué — §10 says "En mode atténué, les données sont livrées par paquets plutôt qu'en continu" — which is where the cell "10 s en mode atténué" could be read either way: the datum's own cadence or the display's. Do you confirm two things — the datum's update and the display's refresh — so that the Rédacteur does not write one word for both?
Answer: Deux choses distinctes, et le code construit les deux séparément.

**Mise à jour** — une propriété de chaque donnée : le moment où sa valeur change. Elle varie d'une ligne à l'autre des tableaux de §13.

**Rafraîchissement** — la cadence à laquelle l'écran est redessiné en mode atténué. Une seule valeur pour tout l'affichage, posée contre le défaut de la plateforme.

La cellule que tu signales — « Continu, ou 10 s en mode atténué » — est bien la mise à jour de la fréquence cardiaque, et si elle vaut dix secondes, c'est parce que le rafraîchissement la borne : une donnée ne peut pas changer à l'écran plus souvent que l'écran ne se redessine.

C'est une conséquence, pas une identité. Les deux valeurs coïncident ici et pourraient cesser de coïncider — le rafraîchissement est un réglage, la mise à jour une observation.

### Q4
Terms: erreur, échec de lecture
Question: One same thing under two words? §4.3: "En cas d'erreur, le message indique la ligne qui pose problème." — the only bare "erreur" that names the import's refusal in prose. Elsewhere the file says "échec": "si une autre présente la même anomalie, c'est un échec de lecture." (§A.4), "Un échec nomme la ligne fautive." (§A.5), "Un échec de lecture est un cas normal" (§A.6), "Ces huit causes couvrent tous les échecs" (§C.5); and the diagram of §12 branches on "succès │ échec". The lexicon holds "échec de lecture — retenu, l'import refusé, en prose", retiring "erreur de lecture" in prose and keeping "erreur" only in the names "Écran d'erreur" and "Messages d'erreur d'import". I read "En cas d'erreur" as that same échec de lecture, said with the retired word in a form the grep did not catch — not a broader case: the inactive "Importer" button is handled without any message ("Aucun message : l'écran empêche plutôt qu'il ne refuse."), and "Un repli n'est pas une erreur." (§13.1) is the common word, unrelated to the import. Do you confirm one same thing, so the prose of §4.3 follows the settled term — or does "erreur" there cover something the échec de lecture does not?
Answer: Une seule chose, et c'est **échec de lecture**.

§4.3 devient : « En cas d'échec de lecture, le message indique la ligne qui pose problème. »

Ta démonstration est complète : le bouton « Importer » inactif est traité sans message, donc « erreur » ne couvre là rien de plus large que le refus de l'import.

**Erreur** garde ses deux emplois légitimes : les noms — Écran d'erreur, Messages d'erreur d'import — et le mot courant de §13.1, « Un repli n'est pas une erreur », qui ne parle pas de l'import.

📌 Cette occurrence est la trace du renommage du tour 3 : le grep cherchait « erreur de lecture » et la forme nue lui a échappé. Il vaudrait de vérifier de même les autres termes retirés en deux mots — leur forme nue a pu survivre ailleurs.
