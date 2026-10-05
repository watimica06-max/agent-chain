# Questions — lexicographe — 06

Tour 5 — settling. The twenty-three answers of
`questions-lexicographe-05.md` are applied to `idees.md` and recorded in
`lexique.md`. Two of them leave one spot each open; those two spots come
back here, unchanged in the idea file until answered.

Questions in English, answers in French.

### Q1
Terms: Liens, texte seul, `link`
Question: Q13 retires "lien" for "texte seul", and adds that the `link` token does not change, since a token names a colour and not a component. The token table of §3.1 still reads `| link | #6FA3D8 | Liens |` — the Usage column carries the retired word. I read that column as describing what the colour is for, so I could not swap it for "Textes seuls" without saying something false: « Supprimer » and « Quitter » are textes seuls too, and they wear `behind` and `text-secondary`, not `link`. Does the Usage column stay "Liens", as part of the token row that does not change, or does it take another wording — and if so, which reading of the colour's role is it meant to carry?
Answer: La colonne ne reste pas « Liens », et ne devient pas non plus « Textes seuls » — tu as raison sur les deux points.

Elle est fausse aujourd'hui, pour une raison que la question ne soulève pas : `link` ne colore pas que des liens. Il porte le texte « Modifier » (§4.4), mais aussi le badge « Référence » de la liste des courses (§4.1) et celui de l'en-tête du détail (§4.2). Deux emplois sur trois ne sont pas des liens.

Le rôle réel de cette couleur est d'être **le seul accent du thème** : ni une couleur de sens, ni un gris de texte, ni une couleur de zone.

L'usage devient : **« Accent — action « Modifier », badge « Référence » »**.

### Q2
Terms: Dernière synchronisation, date de la dernière synchronisation réussie
Question: Q22 settles "date de la dernière synchronisation réussie" in full, everywhere. §B.5 has a row `| Dernière synchronisation | relatif si le jour même | aujourd'hui à 09:02 |` in the Usage column of the date-format table; that row names the same datum — the date shown under the sync button — but "Dernière synchronisation" was not among the terms of Q22, so I left it as written. The two occurrences of §13.3, as a provenance, name the synchronisation event and not the date, and are not in question. Does "partout" reach the §B.5 row, so that it reads "Date de la dernière synchronisation réussie", or is the short form admitted as the Usage label of a format?
Answer: Oui, « partout » atteint cette ligne. §B.5 devient **« Date de la dernière synchronisation réussie »**.

C'est le même raisonnement qu'en Q20 du tour précédent, où la forme courte « Durée d'appui » a été refusée dans §B.4 : une colonne de tableau qui a la place n'est pas un emplacement contraint, et rien n'y pousse à abréger.

Écrire « Dernière synchronisation » seul y laisserait de surcroît croire à une donnée distincte, alors que la ligne décrit le format de la date — celle qui ne s'écrit qu'après une synchronisation réussie.

Les deux occurrences de §13.3 nomment bien l'événement et non la date : elles ne changent pas.


