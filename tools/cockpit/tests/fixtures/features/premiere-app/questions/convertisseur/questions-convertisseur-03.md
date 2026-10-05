# Questions — convertisseur — 03

### Q1
Block: B14 — Saving an imported race
Question: on the paste screen's new race-date field, is a date later than today refused by bounding the date picker's selectable range to today (the future date cannot be selected at all), or by accepting the selection and rejecting it afterward with a validation message?
Answer: En bornant le sélecteur : la plage sélectionnable s'arrête au jour même, une date postérieure ne peut pas être choisie. Aucun message de validation n'existe pour ce cas, puisqu'il ne peut pas se produire.

C'est la même logique que le bouton « Importer » inactif tant qu'un champ manque : l'écran de collage empêche plutôt qu'il ne refuse.

Aucune borne basse. Une date ancienne, même absurde, n'a d'autre effet que de ranger la course en bas de la liste.
