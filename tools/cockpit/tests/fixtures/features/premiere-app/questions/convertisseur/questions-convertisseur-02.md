# Questions — convertisseur — 02

### Q1
Block: B19 — Editing profile settings
Question: what is the expected kilometre distance (distance_attendue) before it has ever been edited in the profile — is there a default value, and if so what is it?
Answer: 1000 mètres. C'est la valeur du réglage tant qu'il n'a jamais été modifié, et celle sur laquelle repose le facteur de correction au premier calcul.

### Q2
Block: B14 — Saving an imported race
Question: how is the calendar date of an imported race determined, given hyresult's export (block B12) only yields a time of day (Time of Day minus Diff), with no date field?
Answer: Elle est saisie à l'import. L'export ne porte aucune date, et rien ne permet de la déduire : l'écran de collage reçoit donc un champ « Date de la course », à côté du champ de nom.

Le champ est pré-rempli avec la date du jour et se modifie par un sélecteur de date standard. La date du jour n'est qu'une commodité : une course importée est presque toujours antérieure, et la valeur pré-remplie doit être corrigée.

Le bouton « Importer » reste inactif tant que la zone de collage, le nom ou la date ne sont pas renseignés — la règle actuelle ne mentionne que les deux premiers, elle est à étendre.

Une date postérieure au jour même est refusée.

La maquette de l'écran de collage ne comporte pas ce champ : elle est à corriger.

### Q3
Block: B19 — Editing profile settings
Question: what is the exact wording of the message shown when a profile setting value is rejected at validation (out of bounds, non-integer, or breaking the zone-threshold order)?
Answer: Un message par cause de rejet, sous le champ concerné. Dans tous les cas, le champ reprend sa valeur précédente.

Hors bornes : « Valeur attendue entre <min> et <max>. » — les bornes citées sont celles du réglage : 100 à 230 pour la fréquence cardiaque maximale, 30 à 99 % pour un seuil de zone, 500 à 2000 m pour la distance d'un kilomètre, 300 à 2000 ms pour la durée de l'appui long.

Valeur non entière : « Nombre entier attendu. »

Ordre des seuils rompu : « Chaque seuil doit être supérieur au précédent. »
