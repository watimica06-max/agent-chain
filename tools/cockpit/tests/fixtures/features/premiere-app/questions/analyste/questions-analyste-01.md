### Q1
Block: B15 — Paste error screen
Question: the error panel shows "the faulty row" next to "the corrected row" — does the app actually propose an automatic correction of the pasted row, or is the faulty row simply shown twice (once labelled faulty, once labelled corrected) for emphasis, with no real correction logic anywhere?
Answer: Non. Aucune correction automatique n'existe. L'encart montre la ligne telle qu'elle a été lue, puis la forme attendue, à titre d'illustration. Aucun bouton ne l'applique : l'utilisatrice corrige sa sélection à la source et recolle. [integrated: B15]

### Q2
Block: B2 — Color tokens
Question: what is the exact color value (hex or RGB) of each named token — surface, surface-raised, screen-black, text-primary, text-body, text-secondary, text-tertiary, border, border-strong, ahead, ahead-text, ahead-bg, behind, behind-text, behind-bg, delta-zero, link, and zone-1 through zone-5?
Answer: surface #121110 · surface-raised #1C1A18 · screen-black #000000 · text-primary #F3EFE7 · text-body #C9C4BA · text-secondary #9A958C · text-tertiary #6F6A62 · border rgba(255,255,255,0.08) · border-strong rgba(255,255,255,0.25) · ahead #4FAE72 · ahead-text #7FCB9C · ahead-bg rgba(79,174,114,0.16) · behind #E2725F · behind-text #E2957F · behind-bg rgba(226,114,95,0.16) · delta-zero #726D63 · link #6FA3D8 · zone-1 #4A90D9 · zone-2 #35B0A4 · zone-3 #4CAF63 · zone-4 #E0A23A · zone-5 #E0503F [integrated: B2]

### Q3
Block: B3 — Typography tokens
Question: what font weight does each usage take — is font-label always the same weight for labels, titles and running text, or do titles/emphasis use a heavier weight than body text, and does font-data ever use a weight other than regular?
Answer: Trois graisses, jamais d'autres. 700 pour les titres, les valeurs et les libellés de bouton. 600 pour les libellés secondaires et les entrées de menu. 500 pour les unités détachées et les actions discrètes. font-data n'emploie que 700, quelle que soit la taille. [integrated: B3]

### Q4
Block: B4 — Shape, spacing and zone-arc tokens
Question: several screens describe a text element as "letter-spaced" (the CYCLE header in B7, badges in B22/B23, the station name in B28, "arrivée estimée" in B30, the Control title in B31) but no letter-spacing value or token is defined anywhere — what is the exact letter-spacing value, and is it a single fixed value or does it vary by text size?
Answer: L'espacement varie selon le rôle, pas selon la taille. 0,04em sur les libellés en capitales de taille normale, dont le numéro de zone. 0,06em sur les en-têtes de groupe et les mentions en capitales de petite taille — en-tête de cycle, nom d'atelier, « arrivée estimée », titre d'écran de la montre. 0,08em sur le titre Contrôle. Aucun espacement sur le texte courant et sur toute donnée chronométrée. [integrated: B4]

### Q5
Block: B5 — Idle display token variants
Question: "dim-text mutes values in place" names a token that is not among the color tokens listed in B2 — what exact color or opacity value does dim-text apply, and to which token(s) does it map (e.g. a dimmed variant of text-primary)?
Answer: dim-text n'est pas une couleur mais une opacité appliquée aux couleurs existantes : 0,55 sur text-primary et sur toute valeur chronométrée, 0,45 sur text-secondary et text-tertiary. Les couleurs de sens — ahead, behind, delta-zero — gardent leur teinte et prennent la même opacité 0,55. Aucun texte ne change de couleur, seulement d'opacité. [integrated: B5]

### Q6
Block: B6 — Race list screen
Question: cards sort by date, most recent first — when two races share the exact same date, what determines their relative order?
Answer: À date identique, la course ajoutée le plus récemment passe en premier — ordre d'insertion décroissant. Le critère est interne, jamais affiché. [integrated: B6]

### Q7
Block: B7 — Race detail screen
Question: for an incomplete race (stopped before its 30th segment), what does the detail screen show for the segments that were never reached — a dash, a hidden row, or something else?
Answer: Les trente lignes restent affichées, structure des cycles comprise. Pour un segment jamais atteint, la durée et le cumul portent un tiret et la colonne d'écart reste vide. Le total affiché est celui des segments réellement courus. [integrated: B7]

### Q8
Block: B8 — Setting a race as the reference
Question: when viewing the detail screen of the race that is already the current reference, does the "Définir comme référence" button still appear, and if tapped, what happens?
Answer: Le bouton est masqué quand la course consultée est déjà la référence. Il est masqué également quand la course est incomplète. [integrated: B8]

### Q9
Block: B10 — Deleting a race
Question: when the race being deleted is the current reference, what becomes of the "current reference" designation — does the app fall back to "no reference," or is deleting the reference race prevented or specially warned about?
Answer: La suppression est autorisée. La boîte de confirmation indique en plus que c'est la course de référence. Après suppression, aucune référence n'est désignée : l'application retombe sur l'état « aucune référence », et aucune course n'est choisie automatiquement. [integrated: B10]

### Q10
Block: B11 — Paste-a-result screen
Question: if "Importer" is tapped while the "Nom de la course" field is empty or otherwise invalid (per the name rule of block B54), what happens — is the button disabled until the name is valid, does an inline error appear, or does something else happen?
Answer: Le bouton Importer est désactivé tant que la zone de collage est vide ou que le nom l'est. Aucun message d'erreur : le bouton s'active dès que les deux champs sont remplis. [integrated: B11]

### Q11
Block: B12 — Reading and validating a pasted result
Question: an optional header row is ignored if present — what rule distinguishes a header row from a data row (e.g. non-numeric Time/Diff columns, a fixed set of known header labels, or something else)?
Answer: La première ligne est ignorée si sa quatrième colonne n'est pas un temps lisible. Une seule ligne peut être ignorée de cette façon ; si une autre ligne présente le même défaut, c'est une erreur de lecture. [integrated: B12]

### Q12
Block: B12 — Reading and validating a pasted result
Question: the reading state machine recognizes "Rox In" for Roxzone segments and station names through the mapping table — what label in the pasted data identifies a kilometre-run row?
Answer: Le libellé « Rox In » identifie le kilomètre du cycle, pour les cycles 1 à 7 — il marque l'entrée en Roxzone, donc la fin du kilomètre. Le kilomètre 8 est identifié par « Wall Balls In ». La table de correspondance complète est celle du bloc d'import. [integrated: B12]

### Q13
Block: B14 — Saving an imported race
Question: block B12 states that a successful reading "produces a recognized total time and a segment count" — does the saved race record also store each of the 30 individual segment durations (as needed to display the race detail screen, block B7, and to potentially serve as a reference race), or only the total and the count?
Answer: Les trente durées sont stockées, sans exception. Le temps total reconnu et le nombre de segments détectés ne servent qu'à l'aperçu avant enregistrement, et ne sont pas conservés comme tels : le total se recalcule par somme. [integrated: B14]

### Q14
Block: B15 — Paste error screen
Question: block B54 defines a generic dynamic text "Erreur de lecture — ligne <n>" (dropping the number when none is identifiable), but this exact wording does not match any of the eight specific titles in B15's failure catalogue — is this a distinct catch-all error state for a failure not covered by the catalogue, and if so what triggers it, or should it be removed as a leftover?
Answer: Reliquat, à supprimer. Le catalogue des huit messages couvre toutes les causes de rejet, et chacun porte déjà son propre titre. Aucun message générique n'est nécessaire. [integrated: B54]

### Q15
Block: B16 — Profile screen
Question: what UI mechanism is used to edit each profile setting (maximum heart rate, each zone percentage, expected kilometre distance, long-press duration) — an inline field, a dedicated dialog, a stepper, or something else?
Answer: La fréquence cardiaque maximale s'édite dans une boîte de saisie numérique, ouverte par le lien « Modifier ». Les quatre seuils de zone, la distance d'un kilomètre et la durée de l'appui long s'éditent dans un champ numérique en ligne sur l'écran, validé à la perte de focus. Aucun incrémenteur, aucun curseur. [integrated: B16]

### Q16
Block: B18 — Zone ranges from maximum heart rate
Question: the five zones each get a single percentage (50/60/70/80/90%) — how do these five values become each zone's bpm range? Is zone n bounded below by threshold n-1 and above by threshold n, with zone 1 open-ended below the first threshold and zone 5 open-ended above the last (matching the "< 94 bpm" / "> 150 bpm" extreme-zone wording in block B50)?
Answer: Quatre seuils, chacun étant la borne BASSE de sa zone. La zone n va du seuil n inclus au seuil n+1 exclu ; la zone 5 couvre tout ce qui est au-dessus du quatrième seuil ; la zone 1 couvre tout ce qui est en dessous du premier.

Les seuils par défaut sont 60, 70, 80 et 90 % de la fréquence cardiaque maximale. Le repos actif, que la littérature situe sous 50 %, est absorbé par la zone 1 plutôt que de former une catégorie à part : sur une course Hyrox cet état ne se produit pas pendant l'effort, et le distinguer ajouterait un réglage, un état visuel et un repli sans rien apporter.

Pour une fréquence maximale de 187 : zone 1 sous 112, zone 2 de 112 à 130, zone 3 de 131 à 149, zone 4 de 150 à 167, zone 5 à partir de 168.

Un segment de l'arc est donc toujours actif, quelle que soit la fréquence lue. Aucun cas sans zone n'existe.

L'écran de profil présente quatre réglages de seuil. Les plages présentées dans la maquette sont décalées d'un cran -- elles traitent chaque pourcentage comme une borne haute -- et sont à corriger. [integrated: B18]

### Q17
Block: B19 — Editing profile settings
Question: what are the valid bounds and type for each editable setting — maximum heart rate, each of the five zone percentages (including whether they must be strictly increasing from zone 1 to zone 5), the expected kilometre distance, and the long-press duration — and what happens when an out-of-bounds or invalid value is entered?
Answer: Fréquence cardiaque maximale : entier, de 100 à 230 bpm. Seuils de zone : quatre entiers, de 30 à 99 %, strictement croissants du premier au quatrième. Distance d'un kilomètre : entier, de 500 à 2000 m. Durée de l'appui long : entier, de 300 à 2000 ms. Une valeur hors bornes, non entière, ou qui romprait l'ordre croissant des seuils est refusée à la validation : le champ reprend sa valeur précédente et un message court indique la contrainte. [integrated: B19]

### Q18
Block: B20 — Sensor permission request
Question: if sensor permission, once granted, is later revoked from the system settings rather than through the app, does the app detect this on the next launch and fall back to the same permanently-refused behavior, or does it re-prompt?
Answer: L'autorisation est vérifiée à chaque lancement. Révoquée depuis les réglages système, elle produit exactement le même comportement qu'un refus initial : fréquence cardiaque et arc des zones en repli permanent, rappel sur l'écran d'accueil. Aucune nouvelle demande n'est déclenchée automatiquement ; le rappel de l'accueil ouvre le réglage système. [integrated: B20]

### Q19
Block: B22 — Home screen
Question: what does the watch's home screen show while "Synchroniser" is in progress, and what does it show on a sync failure — equivalent to the spinner/"Ne ferme pas l'application" and failure/"Réessayer" states described for the phone in block B16?
Answer: Les mêmes trois états que sur le téléphone, affichés sur l'écran d'accueil de la montre sans le quitter. En cours : indicateur d'activité et « Ne ferme pas l'application ». Échec : « Synchronisation impossible — approche le téléphone de la montre. » et « Réessayer ». Réussite : retour à l'accueil normal, avec la référence et l'historique à jour. [integrated: B22]

### Q20
Block: B24 — Preparing and launching a race
Question: if opening the exercise session failed and "Lancer" is tapped anyway, does the race start permanently without any sensor/distance data for its whole duration, or does tapping "Lancer" first retry opening the session?
Answer: Appuyer sur Lancer retente d'ouvrir la session. Si cette tentative échoue à son tour, la course démarre sans donnée de capteur pour toute sa durée. Aucune nouvelle tentative n'a lieu en cours de course. [integrated: B24]

### Q21
Block: B27 — Marking a segment
Question: what is the default long-press duration (in ms) before the user changes it in the profile settings (block B19)?
Answer: 700 ms. [integrated: B19]

### Q22
Block: B28 — Main page, adapting to the current segment
Question: segment 30 is described in block B1 as a single combined segment — Roxzone, Wall Balls, and the sprint to the finish line. Which of the three main-page display states (kilometre / station / Roxzone) applies to this segment, or does it need a display treatment of its own?
Answer: Il est traité comme un atelier. Le nom affiché est Wall Balls, le temps de référence est celui du bloc final de la course de référence, et le centre montre le temps écoulé depuis le début du bloc. Aucun quatrième état d'affichage n'est créé. [integrated: B28]

### Q23
Block: B34 — End-of-race screen
Question: block B58's navigation map states that stopping the race (block B33) also leads to the end-of-race screen, but B34 names only the 30th marking as its trigger — does the same end-of-race screen serve an early stop, and if so, how is the "final delta" computed for a race that never reached its 30th segment?
Answer: Oui, le même écran sert dans les deux cas. Pour une course arrêtée en route, l'écart final est l'écart cumulé au dernier segment fermé, et l'écran indique que la course est incomplète. Les segments jamais atteints n'entrent dans aucun calcul. [integrated: B34]

### Q24
Block: B36 — allure-segment and allure-lissee
Question: neither pace ever uses GPS or a location provider — what sensor or data source then produces the "distance covered" measurement that both paces, and the correction factor of block B37, depend on?
Answer: Health Services, par ses types de données de distance et de vitesse, dérivés des capteurs embarqués de la montre — accéléromètre et cadence de foulée. Aucune localisation n'intervient. C'est précisément parce que cette mesure est imprécise en intérieur que le facteur de correction existe. [integrated: B36]

### Q25
Block: B37 — Computing the correction factor
Question: a rejected k_mesuré "is recorded with the race" — is this rejection record ever shown to the user anywhere (race detail, a flag, a badge), or is it a purely internal record with no display?
Answer: Purement interne. Le rejet est conservé avec la course pour pouvoir réanalyser une calibration après coup, et n'apparaît sur aucun écran. [integrated: B37]

### Q26
Block: B41 — Trend arrow
Question: the arrow shows only above a 2% difference between allure-lissee and allure-segment — at exactly 2%, does the arrow show or not?
Answer: Strictement au-dessus de 2 %. À exactement 2 %, aucune flèche n'est affichée. [integrated: B41]

### Q27
Block: B42 — Zone switching hysteresis
Question: switching to the zone above requires "exceeding its boundary by 3bpm" — at exactly 3bpm over the boundary, does the switch happen, or does it require strictly more than 3bpm?
Answer: À exactement 3 bpm au-dessus de la borne, la bascule a lieu. Le seuil est inclusif dans les deux sens. [integrated: B42]

### Q28
Block: B43 — Sending profile and reference to the watch
Question: block B44 states that nothing syncs while a race is running on the watch — does this push (profile, reference, history) also refrain from sending while a race is running, or could it reach and alter the watch mid-race?
Answer: La montre refuse tout envoi entrant tant qu'une course est en cours, quel qu'en soit le contenu. Le téléphone traite ce refus comme un échec ordinaire et retentera à la prochaine liaison établie. Rien ne peut donc altérer l'état de la montre pendant une course. [integrated: B43]

### Q29
Block: B57 — Phone navigation map
Question: "the system back gesture returns to the list" — does this mean every screen's back gesture jumps directly to the race list regardless of depth (e.g. from the preview or the error screen), or does back step back one screen at a time through the normal path (preview → paste → list)?
Answer: Pas à pas, dans l'ordre inverse du chemin parcouru. Une exception : après un enregistrement réussi, l'écran de collage et l'aperçu sortent de la pile, et le retour depuis le détail de la course importée ramène à la liste. [integrated: B57]

### Q30
Block: B58 — Watch navigation map
Question: a leftward swipe is stated as "reserved for the system's own back gesture" on the race pages, but its effect is never described — what does the system back gesture actually do on the preparation screen, the main page, Projection, and Control during a race?
Answer: Le geste retour est désactivé pendant toute la course — sur la page principale, sur Projection, sur Contrôle et sur l'écran de fin. Quitter une course en cours par un geste accidentel n'est pas acceptable ; la seule sortie est le bouton d'arrêt. Sur l'écran de préparation et partout hors course, le geste retour fonctionne normalement. [integrated: B58]

### Q31
Block: Part 4 — What no chain reveals
Question: are calorie count, step count, cadence, or a GPS route/map display explicitly out of scope for this feature, given they are common expectations for a fitness-tracking watch app but are never mentioned?
Answer: Oui, tous hors périmètre : nombre de calories, nombre de pas, cadence de foulée affichée, altitude, et toute carte ou tracé de parcours. L'allure et la fréquence cardiaque sont les seules mesures physiologiques affichées. [integrated: B59]

### Q32
Block: Part 4 — What no chain reveals
Question: heart rate is sensitive health data. Beyond the OS-level sensor permission (block B20) and health-history permission (block B17), is a separate explicit consent step required within the app before collecting or storing heart-rate data?
Answer: Non. Les autorisations système suffisent. Aucune donnée cardiaque ne quitte les deux appareils : rien n'est transmis à un serveur, rien n'est partagé, rien n'est exporté. L'application n'ajoute aucune étape de consentement propre. [integrated: B60]

### Q33
Block: Part 4 — What no chain reveals
Question: what happens if the connectivity permission needed for phone-watch pairing (e.g. Bluetooth / companion device) is denied — is sync then permanently unavailable, and is this communicated to the user anywhere?
Answer: La synchronisation devient indisponible, et rien d'autre n'est affecté : les deux applications restent pleinement utilisables séparément. L'écran de profil du téléphone indique que l'autorisation manque, à la place de la date de dernière synchronisation, et propose de l'accorder. La montre, elle, affiche simplement « Aucune référence » tant qu'elle n'a rien reçu. [integrated: B61]

## Questions set aside

- Existing rules kept/changed/removed (Part 4): the global (`docs/PRODUIT_GLOBAL.md`) holds no domain content yet — this is the first feature structured, so there is no existing rule for it to touch.
