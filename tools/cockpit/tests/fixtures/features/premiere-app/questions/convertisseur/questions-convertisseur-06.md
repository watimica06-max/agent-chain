# Questions — convertisseur, producing spec-technique.md

### Q1
Block: B19 — Editing profile settings
Question: the product gives bounds (500-2000m) for the expected kilometre distance but no starting value for a profile that has never been edited — what is the default value?
Answer: 1000 mètres.

Cette réponse a déjà été donnée dans questions-convertisseur-02, Q1 : elle n'a pas été reportée dans le bloc B19.

### Q2
Block: B12 — Reading and validating a pasted result
Question: the product names three of the pasted export's four columns (Time of Day, Diff, Time) and a fourth, unnamed, holding the segment label, but never states their left-to-right order, which positional parsing needs — what is that order?
Answer: De gauche à droite : le libellé du segment, l'heure du jour, le temps cumulé, la durée du segment.

La colonne de libellé s'appelle « Split » dans l'en-tête, et les trois suivantes « Time of Day », « Time » et « Diff ».

La lecture est positionnelle et non nominale : l'en-tête est ignoré quand il est présent, et son absence ne change rien. Une ligne comptant moins de quatre colonnes est une erreur de lecture.
