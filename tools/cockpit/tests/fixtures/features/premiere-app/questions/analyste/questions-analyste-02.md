### Q1
Block: B10 — Deleting a race
Question: after the deletion is confirmed, which screen does the app show — does it return to the race list, or something else?
Answer: Retour à la liste des courses. Le détail qu'on quittait décrivait la course supprimée : il ne peut pas rester affiché. [integrated: B10]

### Q2
Block: B14 — Saving an imported race
Question: can two races share the same name, or must the name entered on import be unique among existing races — and if it must be unique, what happens when the user enters one already in use?
Answer: Aucune contrainte d'unicité. Deux courses peuvent porter le même nom ; la date les distingue dans la liste. Rien n'est refusé, rien n'est signalé. [integrated: B14]

### Q3
Block: B28 — Main page, adapting to the current segment
Question: the destination arrow during a Roxzone ("→ SkiErg", "→ Run 3") is rendered at "reduced-opacity" — what is the exact opacity value, or which token does it reference?
Answer: Opacité 0,85, appliquée à la flèche seule. Le nom de la destination reste en text-primary à pleine opacité. [integrated: B28]

### Q4
Block: B42 — Zone switching hysteresis
Question: when there is no heart-rate reading at all (sensor permanently in fallback per block B20, or before any reading arrives), what does the zone arc show — no segment marked active, all five at idle style, or some other distinct treatment?
Answer: Aucun segment n'est marqué actif : les cinq restent au style atténué, et la valeur en battements par minute affiche un tiret. C'est le repli défini pour une donnée capteur absente, et non une zone particulière.

À distinguer du cas où une fréquence est lue : toute valeur lue tombe alors dans une zone, il n'y a jamais de fréquence connue sans zone correspondante. [integrated: B28, B42]

### Q5
Block: B61 — Connectivity permission denied
Question: if the connectivity permission is granted and later revoked from the system settings, is this detected the same way block B20 detects a revoked sensor permission (checked at every launch, falling back to the same unavailable-sync state), or is B61's behavior only triggered by an initial refusal?
Answer: Même traitement exactement : l'autorisation est vérifiée à chaque lancement, et une révocation depuis les réglages système produit le même état qu'un refus initial — synchronisation indisponible, mention sur l'écran de profil à la place de la date de dernière synchronisation. Aucune nouvelle demande n'est déclenchée automatiquement. [integrated: B61]

### Q6
Block: Part 4 — What no chain reveals
Question: when a profile setting changes — maximum heart rate, a zone threshold, the expected kilometre distance, or the long-press duration — does it apply retroactively to already-recorded races (e.g. recomputing what zone a past reading falls in, or a stored correction factor), or only from the next race onward?
Answer: Aucun réglage ne s'applique rétroactivement. Une course enregistrée est figée : ses durées, son facteur de correction et ses mesures cardiaques ne sont jamais recalculés.

Chaque réglage prend effet à partir de la course suivante. La fréquence cardiaque maximale et les seuils de zone déterminent l'arc affiché en course, la distance attendue entre dans le calcul du facteur de correction et de l'écart sur le tour, la durée de l'appui long agit sur le marquage.

Une conséquence à retenir : un réglage modifié sur le téléphone n'atteint la montre qu'à la synchronisation suivante. Modifier sa fréquence maximale juste avant de partir, sans synchroniser, laisse la montre travailler avec l'ancienne valeur. [integrated: B19]

## Questions set aside

- Existing rules kept/changed/removed (Part 4): the global (`docs/PRODUIT_GLOBAL.md`) still holds no domain content — no existing rule for this feature to touch.
