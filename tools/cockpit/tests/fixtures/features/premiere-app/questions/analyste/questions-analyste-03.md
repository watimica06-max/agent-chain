### Q1
Block: B10 — Deleting a race
Question: what is the exact wording of the sentence added to the deletion confirmation when the race being deleted is the current reference?
Answer: La confirmation garde son texte habituel, et une phrase s'intercale avant lui :

« C'est la course de référence. Après suppression, plus aucune course ne servira de comparaison. »
« Suppression définitive. La course disparaîtra aussi de l'historique sur la montre. »

Le titre et les deux boutons ne changent pas. [integrated: B10]

### Q2
Block: B42 — Zone switching hysteresis
Question: when a heart-rate reading resumes after a period with none (the zone shown as inactive per the fallback), does the new reading enter a zone by the plain thresholds of block B18, or does the hysteresis still apply relative to the zone that was active before the reading was lost?
Answer: Par les seuils simples, sans hystérésis. La zone est établie à neuf sur la première lecture qui revient, puis l'hystérésis s'applique de nouveau à partir de cette zone.

L'hystérésis sert à empêcher l'oscillation entre deux lectures successives. Après une interruption, la zone précédente n'est plus une voisine : la fréquence a pu changer beaucoup entre-temps, et s'y référer afficherait une zone périmée. [integrated: B42]

### Q3
Block: B61 — Connectivity permission denied
Question: what is the exact wording of the message shown on the profile screen in place of the last-sync date when the connectivity permission is missing, and of the action offered there to grant it?
Answer: Sur l'écran de profil, à la place de la date de dernière synchronisation :

« Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé. »

Et l'action, juste en dessous : « Autoriser ».

Le bouton « Synchroniser avec la montre » reste affiché mais inactif tant que l'autorisation manque. [integrated: B61]

## Questions set aside

- Existing rules kept/changed/removed (Part 4): the global (`docs/PRODUIT_GLOBAL.md`) still holds no domain content — no existing rule for this feature to touch.
