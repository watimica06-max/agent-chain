# Questions — lexicographe — tour 11

Retour d'une réponse du tour 10 qui laisse un choix ouvert. Les neuf
paires de `questions-lexicographe-10.md` sont tranchées et appliquées ;
la réponse à sa Q5 ouvre une entrée qu'elle ne nomme pas. Questions en
anglais, réponses en français.

### Q1
Terms: ordre d'insertion, la course ajoutée le plus récemment
Question: Your answer to Q5 of round 10 says the tie-break of §4.1 — "À date identique, la course ajoutée le plus récemment passe en premier — le critère est interne, jamais affiché" — rests on a datum the code will have to build, "un ordre d'insertion — un identifiant croissant, ou l'instant d'écriture en base", and that this datum deserves an entry, not the participle. §4.1 names it by a periphrasis only; the lexicon carries no term for it, and I do not choose one. What I can establish is what the entry would cover: one datum per course, written once when the course enters the base locale — by import or by envoi montant, both, since the tie-break orders watch courses as well as imported ones — never displayed, never edited, and read only to order two courses of the same date. I read it as one same datum whichever way it is implemented, an ordering key on the course's entry into the base — the identifier and the write instant being two ways to hold it, not two data. Is that the datum you want the entry for, and by which name does the vocabulary hold it — the term you give it is what the Rédacteur will carry, and §4.1 keeps its periphrasis unless you say the term goes into the sentence?
Answer: Oui, c'est bien cette donnée, et ta description en fixe exactement la portée : une valeur par course, écrite une fois à son entrée dans la base locale, quelle qu'en soit l'origine, jamais affichée, jamais modifiée, lue seulement pour départager deux courses de même date.

Le nom : **rang d'entrée**.

« Ordre d'insertion » nommait le classement plutôt que la donnée qui le permet, et « insertion » est du vocabulaire de base de données, que le fichier d'idées ne parle nulle part ailleurs. « Rang d'entrée » dit ce que la valeur est — une position dans la suite des entrées — et reprend « entrer dans la base locale », qui est déjà la formulation du document.

Sur l'implémentation, ta lecture est juste et elle est même la raison d'être de l'entrée : identifiant croissant ou instant d'écriture sont deux façons de tenir la même donnée. Le lexique nomme ce qu'il faut tenir, pas comment.

**Le terme entre dans §4.1**, et la phrase y gagne : « À date identique, la course au rang d'entrée le plus élevé passe en premier — le rang d'entrée est interne, jamais affiché. »

📌 Une conséquence à porter avec l'entrée : le rang d'entrée doit être écrit **sur toute course**, importée comme reçue de la montre. Une course sans rang ne pourrait pas être départagée, et c'est le genre d'oubli qui ne se voit que le jour où deux courses partagent une date.
