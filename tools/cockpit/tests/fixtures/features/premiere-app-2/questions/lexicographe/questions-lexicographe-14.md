# Questions lexicographe — tour 14

Balayage de `idees.md` après les treize tours tranchés, `## Tranché`
lu d'abord. Les formes nues des termes retirés en deux mots ont été
grep, comme le tour 13 le demandait : aucune n'est restée dans le sens
retiré. Trois doutes.

### Q1
Terms: trentième segment, station Wall Balls
Question: §6.2 reads "**Le trentième segment** — la station Wall Balls, Roxzone puis Wall Balls puis sprint — est traité comme une station." `## Tranché` lists "trentième segment" among the terms that "station Wall Balls" replaces, yet it still stands here, in bold, with the retained term in apposition right after it. Tours 12 and 13 noted it without asking. I read two possible things. Either the ordinal is here a description, not a name — §2 numbers the segments and gives "30." to this one, so "trentième" is its number the way "le huitième RUN" is a number, and the sentence keeps it as the subject that the apposition then names; under that reading nothing changes and the lexicon records the exception. Or it is the retired term still in place, to be replaced — but a bare swap gives "La station Wall Balls — la station Wall Balls, Roxzone puis Wall Balls puis sprint —", so the apposition would have to go too, which is a rewrite I do not do on my own. I read the first: a number in apposition to the name, in one sentence only. Which one holds?
Answer: La première lecture. « Trentième » est un numéro, pas un nom.

§2 numérote les trente segments et donne « 30. » à celui-ci ; le code construit un index, pas un terme. C'est le même statut que « le huitième RUN », que personne ne songerait à retirer au profit de « RUN ».

La phrase reste telle quelle, apposition comprise : le numéro est le sujet, le nom le désigne.

📌 C'est l'entrée du lexique qui se corrige : « trentième segment » n'est pas un rival de « station Wall Balls », c'est sa désignation par le rang. Elle sort de la liste des termes remplacés.

### Q2
Terms: nom libre, nom, nom généré
Question: §14 reads "Une course est identifiée par son nom libre." — one occurrence of "nom libre" in the whole file. Everywhere else the course's name is "nom" (retained: the name of a segment, a station, a checkpoint, a course), and the watch's name is "nom généré" (retained: formed from date and time). "libre" is never used elsewhere. I read "nom libre" as the same thing as "nom", the adjective saying only that the name is free text as opposed to a division — Pro, Doubles, Relay — which is what that line of §14 excludes. But the adjective can also be read as the opposite of "généré": the name the user types on the phone, at import or by "Renommer", as a distinct datum from the name the watch generates. If that second reading holds, the file would carry two kinds of name, and only one of them has a term. Which do you read: one same thing, or a distinct datum?
Answer: Une seule chose. Il n'existe qu'un champ nom sur une course.

Le nom généré en est une valeur par défaut, pas un second datum : §C.2 le dit en une phrase — sur la montre, le nom est généré automatiquement — et « Renommer » écrit dans le même champ. Le code construit un seul nom, quelle qu'en soit l'origine.

L'adjectif porte le contraste avec les divisions — Pro, Doubles, Relay — que §14 écarte deux lignes plus haut : le contexte le donne, le mot n'a pas à le répéter.

§14 devient : « Une course est identifiée par son nom. »

### Q3
Terms: total, temps total
Question: §11 reads "Le total est la somme des segments ; un segment n'est jamais le total moins les autres." and §B.6 reads "sans quoi la somme des segments ne retombe pas sur le total." — three bare occurrences of "total", where the rest of the file says "temps total" (retained: the time of a finished race) and, during the race, "temps total écoulé" (retained). §A.1 also captions the sample "Total 1:37:25". The two settled terms split what "total" alone does not: in §11 the rule is that a segment is measured, never deduced, and the total is the sum — that is the temps total of a race once written, not the running temps total écoulé, which the monotonic chrono measures on its own. I read "total" here as the bare form of "temps total", a reprise in a section that never posed the full form — the same case as "temps écoulé" bare, which tour 8 retired because it did not say which of two. Is "total" the same thing as "temps total", to be written in full, or a common noun of arithmetic — the sum — that names no datum?
Answer: La forme nue de **temps total**, à écrire en entier.

C'est le cas de « temps écoulé » au tour 8 : une forme qui ne dit pas laquelle des deux, dans une section qui n'a jamais posé la forme longue. §11 et §B.6 la prennent donc, et la légende de §A.1 aussi — « Temps total 1:37:25 ».

Ce n'est pas un nom commun d'arithmétique : la règle de §11 porte sur une donnée précise, celle qu'un segment ne doit jamais servir à déduire. La somme, elle, est nommée par le verbe — « le temps total est la somme des segments ».

📌 Deux règles générales éviteraient la plupart des questions de ce type, et celle-ci en est la septième depuis le tour 3 :

Toute forme courte d'un terme est admise **en reprise seulement** — jamais en première mention d'un passage, jamais dans un tableau, un diagramme ou un catalogue, qui n'ont pas de passage.

Un mot n'est un terme que s'il nomme **ce que le code construit** — une donnée, un état, un événement, une entité, un écran. Les autres sont du français et ne s'inscrivent pas.
