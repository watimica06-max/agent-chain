### B1 — Race segment structure

Consumes  | —
Produces  | le découpage d'une course en 30 segments ordonnés (structure de référence), utilisé pour la comparaison segment par segment entre une course importée et une course enregistrée par la montre
Draws on  | —
Names     | Roxzone = zone de transition traversée à l'aller et au retour de chaque station, SkiErg = station 1, Sled Push = station 2, Sled Pull = station 3, Burpee Broad Jump = station 4, Row = station 5, Farmers Carry = station 6, Sandbag Lunges = station 7, Wall Balls = station 8 (fusionnée avec Roxzone et le sprint dans le segment 30), segment = une des 30 divisions fixes d'une course, cycle = un des 7 premiers groupes de 4 segments (course, Roxzone aller, station, Roxzone retour), official race clock = référence externe que ce découpage est dit « matcher » (non définie dans ce bloc), imported race = course importée comparée segment par segment à la course montre, race recorded by the watch = course enregistrée par la montre comparée segment par segment à la course importée
Reads at  | —
Writes at | —

### B2 — Color tokens

Consumes  | —
Produces  | color tokens: surface, surface-raised, screen-black, text-primary, text-body, text-secondary, text-tertiary, border, border-strong, ahead, ahead-text, ahead-bg, behind, behind-text, behind-bg, delta-zero, link, zone-1, zone-2, zone-3, zone-4, zone-5
Draws on  | —
Names     | surface = #121110, surface-raised = #1C1A18, screen-black = #000000, text-primary = #F3EFE7, text-body = #C9C4BA, text-secondary = #9A958C, text-tertiary = #6F6A62, border = rgba(255,255,255,0.08), border-strong = rgba(255,255,255,0.25), ahead = #4FAE72, ahead-text = #7FCB9C, ahead-bg = rgba(79,174,114,0.16), behind = #E2725F, behind-text = #E2957F, behind-bg = rgba(226,114,95,0.16), delta-zero = #726D63, link = #6FA3D8, zone-1 = #4A90D9, zone-2 = #35B0A4, zone-3 = #4CAF63, zone-4 = #E0A23A, zone-5 = #E0503F
Reads at  | À chaque rendu d'écran qui référence un jeton par son nom
Writes at | —

### B3 — Typography tokens

Consumes  | —
Produces  | —
Draws on  | —
Names     | font-label=IBM Plex Sans (labels, titres, texte courant) ; font-data=IBM Plex Mono, chiffres tabulaires (valeurs chronométrées) ; poids 700=titres/valeurs/libellés de bouton ; poids 600=libellés secondaires/entrées de menu ; poids 500=unités détachées/actions à faible emphase ; w-display=110px (horloge/allure centrale, écran principal de course) ; w-display-sm=80px (temps total fin de course) ; w-value=48px (fréquence cardiaque, destination Roxzone) ; w-value-sm=40px (temps écoulé Roxzone) ; w-badge=37px (badge delta) ; w-title=33px (titres écrans hors course) ; w-label=24px (unités, mentions secondaires) ; w-label-sm=20px (unité bpm) ; w-caption=18px (numéro de zone) ; p-title=22dp (titre d'écran) ; p-value=20dp (temps total de course) ; p-body=15dp (texte courant) ; p-label=13dp (libellés de réglage) ; p-data=12.5dp (lignes de segment) ; p-caption=11dp (dates, mentions, badges)
Reads at  | —
Writes at | —

### B4 — Shape, spacing and zone-arc tokens

Consumes  | —
Produces  | radius-pill=moitié de la hauteur, radius-card=12, radius-chip=14, space-xs=4, space-s=8, space-m=12, space-l=20, space-xl=32, multiplicateur échelle montre=1.83, arc-radius=229px, arc-span=140°, arc-segment=25.6°, arc-gap=3°, arc-width=13px, arc-width-active=33px, arc-opacity-idle=0.30, arc-opacity-active=1, rayon segment actif=arc-radius+arc-width/2−arc-width-active/2, letter-spacing=0/0.04em/0.06em/0.08em, spécification appareil cible (Galaxy Watch Ultra 1.5" 480×480, Wear OS 5/One UI Watch 6, upgradable Wear OS 6)
Draws on  | Cadran de la montre (watch face) — zone de l'arc de fréquence cardiaque, centrée en bas de l'écran, span 140°, rayon 229px depuis le centre de l'écran
Names     | radius-pill=moitié de la hauteur, radius-card=12, radius-chip=14, space-xs=4, space-s=8, space-m=12, space-l=20, space-xl=32, w-* scale multiplicateur=1.83, arc-radius=229px, arc-span=140°, arc-segment=25.6°, arc-gap=3°, arc-width=13px, arc-width-active=33px, arc-opacity-idle=0.30, arc-opacity-active=1, rayon segment actif=arc-radius+arc-width/2−arc-width-active/2, letter-spacing labels majuscules taille normale (dont numéro de zone)=0.04em, letter-spacing en-têtes de groupe/mentions majuscules taille réduite (en-tête de cycle, nom de station, « arrivée estimée », titres écrans hors course montre)=0.06em, letter-spacing titre Control=0.08em, letter-spacing texte courant/valeurs chronométrées=0, appareil cible=Galaxy Watch Ultra 1.5" 480×480 Wear OS 5/One UI Watch 6 upgradable Wear OS 6
Reads at  | —
Writes at | —

### B5 — Idle display token variants

Consumes  | arc-width (13), arc-width-active (33), arc-opacity-idle (0.30), text-primary, text-secondary, text-tertiary, timed value, ahead, behind, delta-zero
Produces  | dim-text opacity (0.55 on text-primary/timed value, 0.45 on text-secondary/text-tertiary), meaning-colors opacity (0.55 on ahead/behind/delta-zero), arc-width-dim (7), arc-width-active-dim (22), arc-opacity-idle-dim (0.25)
Draws on  | —
Names     | dim-text = applique une opacité (0.55 ou 0.45) plutôt qu'un changement de couleur ; arc-width-dim = 7 (au lieu de 13) ; arc-width-active-dim = 22 (au lieu de 33) ; arc-opacity-idle-dim = 0.25 (au lieu de 0.30)
Reads at  | Quand le mode d'affichage idle est actif
Writes at | Quand le mode d'affichage idle est actif
</content>
</invoke>

### B6 — Race list screen

Consumes  | race name, race date, race total time, reference-race flag, race-completeness (incomplete) flag
Produces  | race card list display, header display, empty-state display, opening of the paste-a-result screen
Draws on  | Race list screen (self) — header area, card area, empty-state area
Names     | Race list screen = this block (app's opening screen); card = one per race, shows name/date/total time + badges; reference race (current reference race) = race shown with visible mark / Reference badge (criterion undefined — gap); incomplete race = race shown with Incomplete badge (criterion undefined — gap); insertion-order criterion = internal tie-breaker for same-date races, most recently added first, never shown; paste-a-result screen = screen opened by the header button; hyresult = external source the user pastes a result from; surface, surface-raised, radius-card, p-title, p-body, p-value, font-data, p-caption, text-primary, text-secondary, link, behind-text, behind-bg, radius-chip, border-strong = design-system style tokens
Reads at  | app launch / when the race list screen opens
Writes at | —

### B7 — Race detail screen

Consumes  | course consultée (nom, date, 30 segments avec durée et temps cumulé), course de référence actuelle (pour le delta), statut de référence de la course consultée
Produces  | affichage de l'écran de détail de course (en-tête, ligne d'actions, liste de 30 segments groupés par cycle avec deltas)
Draws on  | Race detail screen — pleine page (en-tête, ligne d'actions, liste de segments)
Names     | course consultée = course affichée avec ses 30 segments/durée/temps cumulé ; course de référence = course servant de base au calcul du delta (mécanisme non défini ici, gap) ; référence actuelle = statut de la course affiché via un badge ; cycle = groupe {kilometre, Roxzone, station, Roxzone} ; segment = élément avec nom, durée et temps cumulé, rattaché à un cycle ; delta = écart entre le temps cumulé de la course consultée et celui de la référence au même segment, coloré ahead/behind/delta-zero ; total = somme des durées des segments effectivement courus
Reads at  | au moment de l'affichage de l'écran (course sélectionnée et référence actuelle)
Writes at | —

### B8 — Setting a race as the reference

Consumes  | the tapped race, the race currently holding the reference mark (previous reference), the tapped race's completion status, whether the tapped race is already the current reference
Produces  | reference mark set on the tapped race, reference mark removed from the previous reference, button shown/hidden state on the race detail screen, button shown/hidden state on the race list card
Draws on  | race detail screen — "Définir comme référence" button; race list screen — list card action area
Names     | current reference = the race designated by this mechanism as reference; "Définir comme référence" = the button's exact label; incomplete = the race's completion status gating the button's visibility; list card = the race's representation on the race list screen; detail screen = the race's detail screen
Reads at  | the moment the user taps "Définir comme référence"
Writes at | the moment that tap is processed

### B9 — Renaming a race

Consumes  | nom actuel (pré-remplissage), nouveau nom saisi par l'utilisateur, règle de nom du bloc B54 (jamais vide, 40 caractères maximum)
Produces  | nom stocké de la course (mis à jour)
Draws on  | écran de détail de la course — champ de renommage (zone précise non nommée)
Names     | écran de détail de la course = écran existant où le renommage est déclenché ; nom actuel = nom actuellement stocké de la course, utilisé pour le pré-remplissage ; nouveau nom = valeur saisie par l'utilisateur dans le champ ; nom stocké = champ persisté de la course, mis à jour à l'enregistrement ; règle de nom (B54) = jamais vide, 40 caractères maximum ; « Annuler » = libellé du bouton d'annulation ; « Enregistrer » = libellé du bouton d'enregistrement ; champ bordered radius-card = style visuel du champ de saisie
Reads at  | à l'ouverture du champ de renommage (pré-remplissage avec le nom actuel)
Writes at | à l'appui sur « Enregistrer »

### B10 — Deleting a race

Consumes  | la course affichée dans l'écran de détail (celle visée par la suppression), la course de référence actuelle
Produces  | confirmation (badge "!", titre, message, boutons Annuler/Supprimer), suppression définitive de la course, état "aucune référence" (si la course supprimée était la référence), retour à l'écran liste des courses, donnée à propager à la montre au prochain push (B43)
Draws on  | écran détail de course (bouton Supprimer) ; confirmation sur "behind" (zone non précisée) ; écran liste des courses (retour après confirmation)
Names     | Supprimer (détail) = bouton déclenchant la demande de confirmation ; Annuler = bouton bordé de la confirmation (comportement non précisé) ; Supprimer (confirmation) = bouton rempli confirmant la suppression définitive ; confirmation = boîte avec badge "!", titre nommant la course, message de suppression définitive (+ phrase référence si applicable), boutons Annuler/Supprimer ; course de référence actuelle = concept existant déterminant la variante du message et le retour à "aucune référence" ; état "aucune référence" = état existant vers lequel bascule l'app après suppression de la référence ; B43 = bloc existant du prochain push vers la montre ; behind = zone/écran d'affichage de la confirmation (non défini ici)
Reads at  | à l'appui sur "Supprimer" dans l'écran de détail (affichage confirmation) et à la confirmation (vérification si la course est la référence actuelle)
Writes at | à la confirmation de la suppression (appui sur "Supprimer" dans la boîte de confirmation)

### B11 — Paste-a-result screen

Consumes  | Texte collé (quatre colonnes copiées depuis hyresult), nom de la course saisi par l'utilisateur
Produces  | Affichage de l'écran (champ de collage, champ « Nom de la course », bouton « Importer »), état actif/inactif du bouton « Importer », déclenchement du mécanisme d'import au tap
Draws on  | Écran « Paste-a-result screen » (le bloc est l'écran entier) — pas de zone d'un autre écran
Names     | hyresult = source externe des résultats copiés ; « quatre colonnes » = format du texte copié depuis hyresult ; « Nom de la course » = champ de saisie du nom ; « Importer » = bouton d'action pilule pleine largeur ; radius-card = style de coin/bordure du champ de collage ; bordered = style de bordure du champ de collage ; text-tertiary = couleur du texte de placeholder
Reads at  | À chaque saisie/modification du texte collé ou du nom (pour évaluer l'état du bouton), et au tap sur « Importer »
Writes at | À l'affichage initial (état vide, bouton désactivé) et à chaque changement de contenu des deux champs

### B12 — Reading and validating a pasted result

Consumes  | texte collé (export hyresult) ; colonnes du tableau : nom de station, Time of Day, Diff, Time (ordre exact non précisé — gap) ; ligne d'en-tête optionnelle (1ère ligne)
Produces  | succès : temps total reconnu, nombre de segments (consommés par B13) ; échec : numéro de la ligne fautive, message correspondant (consommé par B15)
Draws on  | —
Names     | "hyresult's official export" = format de collage (colonnes séparées par tabulation ou suite d'espaces multiples, règle d'en-tête, règle d'échelle m:ss/h:mm:ss, règle d'heure de départ) ; "Rox In" = repère marquant la fin du kilomètre pour les cycles 1 à 7 ; "Wall Balls In" = repère du kilomètre 8, bascule en mode terminal ; table de correspondance station→segment : SkiErg=SkiErg, Sled Push=Sled Push, Sled Pull=Sled Pull, Burpee BJ=Burpee Broad Jump, Row=Rameur, F. Carry=Farmers Carry, S. Lunges=Sandbag Lunges, Wall Balls=Wall Balls ; "ligne fautive" = première ligne violant une des trois conditions d'acceptation (30 lignes, somme des Diff conforme, ordre des libellés conforme) ; "temps total reconnu" et "nombre de segments" = sorties du succès ; "message correspondant" = sortie de l'échec, texte défini par B15 ; B13 = aperçu, consommateur du succès ; B15 = bloc consommateur de l'échec
Reads at  | au tap sur "Importer"
Writes at | à la lecture réussie (l'import est atomique, jamais partiel — ce qui implique une écriture uniquement en cas de succès)

### B13 — Preview before saving

Consumes  | Temps total reconnu (issu de B12), nombre de segments détectés (issu de B12), texte collé conservé (depuis l'écran de collage)
Produces  | Affichage de l'aperçu (badge ✓, titre, deux lignes label/valeur, boutons « Corriger »/« Enregistrer »), changement d'état retour à l'écran de collage, déclenchement du mécanisme d'enregistrement de la course
Draws on  | Écran B13 (Preview before saving) — écran entier
Names     | « Temps total reconnu » = label de la valeur du temps total reconnu, « Segments détectés » = label du nombre de segments détectés, « Corriger » = bouton retour à l'écran de collage avec texte collé conservé, « Enregistrer » = bouton déclenchant l'enregistrement de la course, « la course » = entité enregistrée sur Enregistrer
Reads at  | Quand B12 produit une lecture réussie
Writes at | Quand « Enregistrer » est pressé (enregistre la course) ; quand « Corriger » est pressé (retour à l'écran de collage)

### B14 — Saving an imported race

Consumes  | nom saisi, 30 durées de segment
Produces  | fiche de course (nom + 30 durées de segment), navigation vers l'écran de détail de la course, absence de facteur de correction d'allure pour une course importée
Draws on  | Écran de détail de la course (ouvert en plein écran, directement) ; liste des courses (citée par exclusion — jamais ouverte)
Names     | « Enregistrer » = bouton déclencheur situé dans l'aperçu ; nom saisi = nom donné à la nouvelle fiche de course ; 30 durées de segment = intégralement stockées sans exception ; fiche de course = enregistrement créé (nom + 30 durées, total non stocké) ; temps total reconnu (bloc B12) = sert uniquement à l'aperçu, non stocké ; nombre de segments reconnu (bloc B12) = sert uniquement à l'aperçu, non stocké ; total = recalculé par somme des durées stockées, jamais stocké comme tel ; facteur de correction d'allure (bloc B38) = jamais produit pour une course importée ; courses enregistrées par la montre = seules à calibrer le facteur de correction d'allure ; écran de détail de la course = ouvert directement après l'enregistrement ; liste des courses = jamais ouverte après l'enregistrement ; nom de la course = aucune contrainte d'unicité, distinction par la date dans la liste
Reads at  | Au moment de l'appui sur « Enregistrer » : lit le nom saisi et les 30 durées de segment depuis l'aperçu
Writes at | Au moment de l'appui sur « Enregistrer » : écrit la nouvelle fiche de course

### B15 — Paste error screen

Consumes  | cause identifiée par B12, position <n> de la ligne fautive, libellé <libellé> (le cas échéant), contenu brut de la ligne fautive, texte précédemment collé
Produces  | badge "!", titre du message, texte d'explication, panneau ligne lue / forme attendue, retour de navigation vers l'écran de collage (texte collé conservé)
Draws on  | écran d'erreur de collage (plein écran) — zones behind / ahead
Names     | "Rien à lire" = titre (Empty paste), "Colle les quatre colonnes copiées depuis hyresult." = explication (Empty paste), "Colonnes manquantes — ligne <n>" = titre (Fewer than four columns), "Chaque ligne doit contenir quatre colonnes. Copie le tableau entier, en-tête compris." = explication, "Format de temps invalide — ligne <n>" = titre (Unreadable time), "Le temps doit être au format m:ss. Remplace l'espace par un deux-points." = explication, "<n> segments sur 30" = titre (Fewer than 30 segments), "Le collage est incomplet. Copie le tableau entier, de la première ligne jusqu'à « Total time »." = explication, "<n> segments au lieu de 30" = titre (More than 30 segments), "Le collage contient des lignes en trop. Copie uniquement le tableau des temps." = explication, "Libellé inconnu — ligne <n>" = titre (Unrecognized label), "« <libellé> » n'est pas un point de passage attendu. Vérifie que tu as copié un résultat Hyrox complet." = explication, "Ordre inattendu — ligne <n>" = titre (Label out of sequence), "« <libellé> » n'est pas à sa place dans la course. Copie le tableau sans le trier ni le réorganiser." = explication, "Temps incohérents — ligne <n>" = titre (Inconsistent cumulative time), "Le cumul ne correspond pas à la somme des temps. Vérifie que la ligne n'a pas été modifiée." = explication, "<libellé>" = valeur lue telle quelle, tronquée à 20 caractères, "Revenir au collage" = action, retour à l'écran de collage, texte collé conservé, B12 = source de la lecture en échec (pointeur nu), "the paste screen" = destination du retour (non identifié par numéro dans ce bloc), "behind" = zone (non définie dans ce bloc), "ahead" = zone (non définie dans ce bloc), "font-data" = style typographique (non défini dans ce bloc), "surface-raised" = style de panneau (non défini dans ce bloc), "p-body/text-secondary" = style de texte (non défini dans ce bloc)
Reads at  | au moment où B12 produit une lecture en échec
Writes at | à l'affichage de l'écran, et au tap sur "Revenir au collage"

### B16 — Profile screen

Consumes  | FC max, 4 seuils de zone, distance kilométrique attendue, durée de l'appui long, date du dernier sync réussi, état de sync courant
Produces  | FC max mise à jour, seuils de zone mis à jour, distance kilométrique mise à jour, durée d'appui long mise à jour, déclenchement du mécanisme de synchronisation montre, affichage écran profil, icône d'entrée dans le header de la liste des courses
Draws on  | Écran liste des courses — zone header (icône, à côté du bouton d'ajout) ; Écran profil (ce bloc) — sections FC max / zones / réglages / bouton de sync
Names     | FC max = valeur numérique éditée via dialogue "Modifier" ; seuils de zone (zone-1..zone-5) = pourcentage + plage bpm par zone, édités inline ; distance kilométrique attendue = champ numérique inline ; durée de l'appui long = champ numérique inline ; date du dernier sync réussi = affichée sous le bouton de sync ; état de sync = en cours / échoué
Reads at  | À l'ouverture de l'écran (valeurs courantes des réglages, date de dernier sync, état de sync)
Writes at | À la perte de focus du champ (seuils de zone, distance, durée d'appui long), à la confirmation du dialogue (FC max), au déclenchement du bouton de synchronisation (état de sync)

### B17 — Deriving maximum heart rate

Consumes  | Historique de santé du téléphone (FC max sur 12 mois), statut de la permission d'accès à l'historique de santé
Produces  | Valeur de FC max proposée/éditable dans le profil, état d'affichage des zones B18 (masqué/visible)
Draws on  | Écran profil — champ de FC max (zone B18 juste en dessous)
Names     | FC max = valeur proposée depuis l'historique de santé (max sur 12 mois) ou saisie à la main, éditable ; Historique de santé du téléphone = source de lecture de la FC, lue localement sur le téléphone uniquement ; Fenêtre de 12 mois = période de recherche du maximum observé ; Permission d'accès à l'historique de santé = condition d'accès (accordée/refusée) ; Zones de fréquence cardiaque (bloc B18) = affichage conditionné au remplissage de la FC max ; Configuration des zones de Samsung Health / FC max de Samsung Health = existantes mais inaccessibles à une app tierce ; Âge = explicitement non utilisé (ni connu ni demandé)
Reads at  | À la première ouverture du profil
Writes at | À la première ouverture du profil (préremplissage automatique du champ), ou lors d'une saisie manuelle ultérieure de l'utilisateur

### B18 — Zone ranges from maximum heart rate

Consumes  | FC maximale (profil), quatre seuils de zone (%, bloc B16, défaut 60/70/80/90), lecture FC courante (pour le segment d'arc actif)
Produces  | cinq plages de zones (bornes bpm), segment d'arc actif reflétant la zone de la lecture courante, masquage des plages tant que la FC max est inconnue
Draws on  | —
Names     | seuils par défaut = 60/70/80/90 % de FC max (réglables en B16) ; zone1 = < seuil1 ; zone2 = [seuil1, seuil2) ; zone3 = [seuil2, seuil3) ; zone4 = [seuil3, seuil4) ; zone5 = ≥ seuil4 ; seuil_n = arrondi(%_n × FCmax) ; segment d'arc = toujours un segment actif reflétant la zone de la lecture FC courante
Reads at  | —
Writes at | —

### B19 — Editing profile settings

Consumes  | nouvelle valeur saisie pour le réglage édité (fréquence cardiaque max, seuil de zone, distance_attendue, durée d'appui long), valeur précédente du réglage
Produces  | réglage de profil mis à jour (fréquence cardiaque max, seuil de zone, distance_attendue, durée d'appui long) enregistré ; en cas de rejet : retour du champ à sa valeur précédente, message bref de contrainte
Draws on  | —
Names     | fréquence cardiaque max = entier, 100–230 bpm ; seuil de zone (quatre) = entier, 30–99%, strictement croissant du 1er au 4e ; distance_attendue (distance attendue au kilomètre) = entier, 500–2000m, utilisée dans la correction d'allure (B37) ; durée d'appui long = entier, 300–2000ms, par défaut 700ms ; profil = destination de l'enregistrement (non décrite dans ce bloc) ; course enregistrée = entité figée dont les durées, le facteur de correction et les mesures de fréquence cardiaque ne sont jamais recalculés
Reads at  | à la validation, quand l'utilisateur soumet une valeur éditée (comparaison aux bornes/à l'ordre) ; valeur précédente lue pour la restauration
Writes at | à la validation, quand la valeur éditée passe les contrôles de bornes/ordre — enregistrée immédiatement dans le profil (effective à partir de la prochaine course, et n'atteint la montre qu'à la prochaine synchronisation, B43)

### B20 — Sensor permission request

Consumes  | état courant de la permission capteurs (système), indicateur que le système peut encore proposer la demande
Produces  | écran de demande de permission, état de fallback (heart rate, zone arc), rappel sur l'écran d'accueil, nouvelle demande système de permission, ouverture de la page des réglages système de l'app
Draws on  | écran de demande de permission — plein écran, centré, titre + explication + bouton pill, texte ≤ 3 lignes ; écran d'accueil — rappel (zone non précisée)
Names     | permission capteurs = état système (accordée / refusée / révoquée / refusée définitivement) ; écran de demande de permission = écran dédié décrit dans ce bloc ; fallback = état dégradé permanent pour heart rate et zone arc lorsque la permission n'est pas accordée ; rappel écran d'accueil = invite persistante tant que la permission n'est pas accordée ; page des réglages système = écran système ouvert en dernier recours
Reads at  | à chaque lancement de l'app ; à l'appui sur le rappel de l'écran d'accueil
Writes at | au premier lancement (affichage de la demande) ; à chaque lancement suivant si l'état a changé (mise à jour du fallback) ; à l'appui sur le rappel (déclenche la demande système ou ouvre les réglages)

### B21 — Waiting for the phone

Consumes  | État de réception du profil (reçu / non reçu)
Produces  | Affichage de l'écran d'attente, texte « En attente du téléphone », bouton de nouvelle tentative, remplacement de l'écran d'accueil
Draws on  | Écran de la montre — écran d'attente du téléphone (plein écran, remplace l'écran d'accueil)
Names     | profil = donnée reçue du téléphone (contenu non décrit ici) ; écran d'accueil = écran normal affiché une fois le profil reçu ; écran d'attente du téléphone = cet écran ; bouton de nouvelle tentative = élément de cet écran (action non décrite) ; texte « En attente du téléphone » = libellé affiché sur cet écran
Reads at  | Au moment où la montre s'apprête à afficher l'écran d'accueil (vérification de la réception du profil)
Writes at | À l'affichage de l'écran d'attente, dès que le profil manque

### B22 — Home screen

Consumes  | la référence courante (nom, durée) ; l'état du push/pull de synchronisation (B43/B44)
Produces  | affichage de la ligne de référence ou du badge « Aucune référence » ; bouton « Démarrer » ; pastilles « Historique » et « Synchroniser » ; déclenchement du push/pull de synchronisation (B43/B44) ; les 3 états affichés de la synchronisation (en cours, échec, succès)
Draws on  | écran Home (B22), pleine page, de haut en bas
Names     | « la référence courante » = nom + durée (ou absence) affichés en tête ; « Démarrer » = bouton plein-largeur, actif même sans référence ; « Historique » = pastille menant à la section Historique ; « Synchroniser » = pastille déclenchant B43/B44 avec 3 états (en cours / échec / succès)
Reads at  | à l'affichage de l'écran d'accueil (référence courante) ; au tap sur « Synchroniser »
Writes at | à l'issue de la synchronisation : succès (référence et historique mis à jour) ou échec (message + « Réessayer » affichés)

### B23 — Watch history screen

Consumes  | Liste des courses existantes : nom, date, temps total (par course)
Produces  | Affichage de l'écran historique de la montre (titre « Historique » + lignes de course : nom, date, temps total)
Draws on  | Écran historique de la montre (B23) — zone : écran entier (titre + liste des courses)
Names     | Historique = texte du titre de l'écran ; w-label/text-tertiary = style du titre ; w-label/text-primary = style du nom de course ; font-data/text-secondary = style de la ligne date/temps total ; letter-spaced = attribut de style du titre
Reads at  | Au moment de l'affichage de l'écran d'historique
Writes at | —

### B24 — Preparing and launching a race

Consumes  | état "référence chargée", résultat d'ouverture de la séance d'exercice, valeur de fréquence cardiaque (capteurs)
Produces  | écran de préparation (le sas), affichage fréquence cardiaque (normal/repli), badge "Référence chargée · <name>", ouverture de la séance d'exercice, préchauffage des capteurs, démarrage du chronomètre, ouverture du premier segment, état course avec/sans données capteur, retour à l'écran d'accueil, mécanisme de relance d'ouverture de séance
Draws on  | Écran de préparation (le sas) — zone fréquence cardiaque, zone badge de référence, bouton "Lancer", contrôle "Quitter"
Names     | le sas = écran de préparation ; Démarrer = bouton (accueil) qui ouvre le sas ; Lancer = pill pleine qui démarre le chronomètre et le premier segment ; Quitter = texte simple qui ferme le sas et revient à l'accueil ; Fréquence cardiaque = libellé de la valeur de fréquence cardiaque ; Référence chargée · <name> = badge indiquant une référence chargée ; référence = donnée externe chargée utilisée pour la comparaison (non définie ici)
Reads at  | à l'ouverture du sas, à chaque tap sur "Lancer" ou "Quitter", et automatiquement lors de l'échec d'ouverture de la séance
Writes at | au tap sur "Démarrer" (ouverture du sas/séance), au tap sur "Lancer" (démarrage ou relance), au tap sur "Quitter" (fermeture, retour accueil)

### B25 — Starting when another app holds the sensor

Consumes  | sensor-lock status (held by another app), user's confirmation choice (Continuer / Annuler)
Produces  | confirmation screen "Reprise d'activité en cours", stopping of the other app's activity, starting of our race, return without starting
Draws on  | Screen "Reprise d'activité en cours" (area not specified)
Names     | "Reprise d'activité en cours" = title of the confirmation screen; "Annuler" = cancel button label, bordered style; "Continuer" = confirm button label, filled style; "the sensor" = the device's single concurrent exercise-session slot; "another app" = any other app currently holding that slot; "the race" = the exercise session this app is starting
Reads at  | at the moment the race starts (when the sensor-lock status is checked)
Writes at | at the moment the user responds to the confirmation (Continuer or Annuler)

### B26 — Resuming our own already-active race

Consumes  | Session d'exercice déjà active au démarrage, appartenance de cette session à notre propre course, état de course stocké dans la base de données locale
Produces  | Reprise de la course depuis l'état stocké en base locale, session capteur non redémarrée
Draws on  | —
Names     | exercise session = la session d'exercice déjà active au démarrage de l'app ; our own race = la course à laquelle appartient cette session active ; state stored in the local database = l'état de course persisté utilisé pour la reprise ; sensor session = la session capteur associée à la course, non redémarrée
Reads at  | Au démarrage de l'app
Writes at | —

### B27 — Marking a segment

Consumes  | geste tactile (contact, durée de maintien, glissement), seuil d'appui long (réglages du profil, B19), segment courant, page affichée (exclusion de Control)
Produces  | segment courant marqué terminé, segment suivant ouvert, heure du segment, vibration (confirmation / annulation), retour automatique à la page principale
Draws on  | —
Names     | seuil d'appui long = 700ms par défaut, réglable via B19 ; seuil de glissement d'annulation = 20px ; délai d'inactivité (page secondaire) = 8 secondes ; page exclue = Control ; vibration de confirmation = une pulsation courte ; vibration d'annulation = deux pulsations courtes ; zone d'appui = écran entier
Reads at  | à l'instant du contact du doigt (heure du segment), et en continu pendant l'appui (durée de maintien, glissement)
Writes at | à l'instant où le seuil de maintien est atteint, sans relâchement ni glissement excessif avant ce moment

### B28 — Main page, adapting to the current segment

Consumes  | B39 (delta du tour vs référence), B36 (allure-segment), B41 (flèche de tendance), B1 (bloc combiné final pour le segment 30), B30 (arrivée estimée), B4 (arcs de zone), B42 (hystérésis de changement de zone), lecture de fréquence cardiaque, statut « référence chargée », delta cumulé, temps écoulé du segment en cours, nom de l'étape suivante
Produces  | Affichage bloc haut (badge delta / temps de référence / temps de transition), affichage bloc centre (allure + flèche / temps écoulé / destination), affichage bloc bas (FC, bpm, numéro de zone, 5 arcs de zone), pastille de zone actionnable
Draws on  | Écran principal de course (cadran rond 480×480, 1,5 pouce) — bloc haut, bloc centre, bloc bas, zone de la pastille actionnable
Names     | font-data = police du badge delta, du temps de référence et de la FC ; w-badge = poids du badge delta ; radius-chip = rayon du badge delta ; ahead-text/ahead-bg = style du badge en avance ; behind-text/behind-bg = style du badge en retard ; w-display = poids de l'horloge/allure centrale ; text-primary = couleur du texte central et de la FC ; font-label = police des libellés (unité, nom de station, destination) ; w-label = poids de l'unité "/km" et du nom de station ; text-secondary = couleur de l'unité et du temps de référence ; text-tertiary = couleur du nom de station ; w-value-sm = poids du temps de Roxzone ; w-value = poids de la destination ; w-label-sm = poids de l'unité "bpm" ; w-caption = poids du numéro de zone ; arc-segment/arc-gap/arc-span/arc-radius = géométrie des arcs de zone ; arc-width-active/arc-opacity-active = style de l'arc de la zone courante ; arc-width/arc-opacity-idle = style des arcs inactifs ; Segment 30 = bloc combiné Roxzone + Wall Balls + sprint final, affiché sous le nom "Wall Balls"
Reads at  | En continu pendant la course, avec rafraîchissement à chaque changement de segment (et en continu pour la fréquence cardiaque)
Writes at | À chaque changement de segment (haut/centre) et en continu pour le bloc bas (FC et arc de zone)

### B29 — Data freshness on the race pages

Consumes  | Valeur à afficher sur les pages de course, horodatage de la dernière lecture capteur, mode d'affichage (normal / économie d'énergie), heure courante
Produces  | Affichage en tiret ou masquage du bloc (valeur absente), état de repli silencieux pour une valeur capteur obsolète, affichage continu et sans repli de l'horloge
Draws on  | Écran : pages de course — Zone : non précisée
Names     | Valeur absente = tiret ou bloc masqué (jamais zéro/« +0:00 ») ; repli (fallback) = état déclenché après 10s sans nouvelle lecture capteur, sans message ni interruption (contenu exact non précisé) ; mode d'affichage normal = seuil de 10s ; mode économie d'énergie = seuil de 10s aligné sur sa cadence de rafraîchissement (valeur non donnée) ; horloge = toujours disponible, jamais de repli
Reads at  | Au moment de l'affichage/rafraîchissement des pages de course, et en continu pour comparer la dernière lecture capteur au seuil de 10 secondes
Writes at | Au moment où une valeur est absente à l'affichage, ou dès que le seuil de 10 secondes sans nouvelle lecture est atteint

### B30 — Projection page

Consumes  | delta cumulé depuis le début (bloc B40), heure d'arrivée estimée (bloc B40), temps total écoulé, position ("14/30"), mécanisme d'appui long pour marquer un segment (existant, repris de la page principale)
Produces  | affichage de la page Projection, badge delta (haut), heure d'arrivée estimée (centre, grande), légende "arrivée estimée" (sous l'heure d'arrivée), ligne temps écoulé + position (bas)
Draws on  | écran Projection — zone haute (badge delta), zone centrale (heure d'arrivée estimée), zone basse (temps écoulé + position)
Names     | Projection = page/écran défini par ce bloc ; main page = écran existant (référencé, non défini ici) ; delta cumulé depuis le début = valeur du bloc B40 ; heure d'arrivée estimée = valeur du bloc B40 ; temps total écoulé = non défini (gap A4.1) ; position ("14/30") = non défini (gap A4.1) ; appui long pour marquer un segment = mécanisme existant, repris de la page principale ; badge delta = élément visuel, mêmes tokens que la page principale ; font-data/w-display = token typographique ; w-caption/text-tertiary = token typographique ; font-data/w-label/text-secondary = token typographique
Reads at  | à l'ouverture de la page Projection (swipe droite depuis la page principale), en continu pendant l'affichage
Writes at | —

### B31 — Control page

Consumes  | nom du segment rouvert par l'annulation (cf. B32)
Produces  | affichage de l'écran Contrôle (titre "Contrôle", bouton d'annulation nommé, texte "Arrêter l'activité") ; déclenchement de B32 (annulation) ou B33 (arrêt) selon l'action choisie
Draws on  | écran Contrôle (lui-même) — zone : titre en haut, bouton d'annulation pleine largeur, texte d'arrêt en dessous
Names     | Control = cet écran (défini ici) ; Projection = écran d'origine du swipe (existant, pointeur) ; B32 = bloc d'annulation du dernier marquage (pointeur) ; B33 = bloc d'arrêt de l'activité (pointeur) ; le segment rouvert = nom affiché sur le bouton d'annulation (valeur définie par B32) ; l'activité = l'activité de course en cours (existante) ; w-label/text-tertiary = jeton de style du titre (existant)
Reads at  | à l'ouverture de Contrôle (swipe droite depuis Projection)
Writes at | —

### B32 — Undoing the last marking

Consumes  | dernier marquage (concept existant), segment fermé par ce marquage (état existant)
Produces  | segment rouvert (changement d'état), suppression/annulation du dernier marquage, libellé/état du bouton "annuler" mis à jour
Draws on  | écran Control — bouton "annuler"
Names     | "bouton annuler" (Control) = bouton qui rouvre le segment fermé par le dernier marquage ; "dernier marquage" = le marquage le plus récent effectué (pré-existant, non défini ici) ; "segment" = élément fermé par un marquage, rouvert par l'annulation (pré-existant, non défini ici) ; "annulation à un seul niveau" = ne touche jamais qu'au dernier marquage, jamais en cascade
Reads at  | à l'appui (tap) sur le bouton "annuler"
Writes at | immédiatement lors de l'annulation (réouverture du segment, retrait du dernier marquage, mise à jour du bouton)

### B33 — Stopping the race

Consumes  | tap sur « Arrêter l'activité » (Control), choix de confirmation (« Annuler » ou « Arrêter »), chronomètre en cours, mesures en cours
Produces  | affichage du dialogue de confirmation, arrêt du chronomètre, arrêt de toutes les mesures, course sauvegardée en l'état marquée incomplète
Draws on  | Control — bouton « Arrêter l'activité » ; Control — dialogue de confirmation (titre, mention, boutons « Annuler »/« Arrêter »)
Names     | « Arrêter l'activité » = bouton sur Control déclenchant la demande de confirmation ; « Annuler » = bouton bordé de la confirmation ; « Arrêter » = bouton plein de la confirmation, positionné derrière « Annuler », dont la confirmation déclenche l'arrêt effectif ; « incomplète » = statut donné à une course arrêtée avant sa fin, qui ne peut jamais devenir la référence ; « la référence » = notion définie au bloc B8
Reads at  | au moment où l'utilisateur appuie sur « Arrêter l'activité » puis confirme par « Arrêter »
Writes at | au moment où l'utilisateur confirme par « Arrêter » dans le dialogue de confirmation

### B34 — End-of-race screen

Consumes  | temps total de la course, delta cumulé au dernier segment clôturé (par rapport à la référence), présence/absence d'une référence chargée, date et heure courantes, statut de fin de course (30e pointage atteint ou arrêt anticipé via B33)
Produces  | affichage du temps total, affichage du badge de delta final (masqué si pas de référence), mention "course incomplète" (arrêt anticipé), affichage du nom automatique (date et heure), sauvegarde automatique de la course, navigation vers l'écran d'accueil (action "Terminer")
Draws on  | Écran de fin de course (ce bloc) — bloc centré : temps total en haut, badge delta en dessous, date/heure en dessous, bouton "Terminer" en bas
Names     | temps total = durée totale de la course ; delta final = delta cumulé par rapport à la référence au dernier segment clôturé (le 30e si la course est complète) ; nom automatique = date et heure de la course ; "Terminer" = bouton de retour à l'écran d'accueil ; référence = performance de référence chargée (existant) ; bloc B33 = mécanisme d'arrêt anticipé de la course (existant)
Reads at  | au moment où la course se termine (30e pointage atteint, ou arrêt anticipé via B33)
Writes at | au même moment (sauvegarde automatique dès l'affichage de l'écran) ; puis à l'appui sur "Terminer" (navigation vers l'accueil)

### B35 — Always-on display during the race

Consumes  | Idle tokens of block B5, device's default refresh rate (once per minute), power-save mode state, wrist-raise event, screen-touch event, platform guidance to show a dash on an absent value
Produces  | Dimmed display state (thinner/transparent arc, muted text, values kept rather than dashed), power-save refresh cadence of 10 seconds, full-refresh resumption
Draws on  | —
Names     | Power-save mode = dims the display using B5's idle tokens (thinner/transparent arc, muted text) and refreshes every 10 seconds; Full refresh = the non-dimmed display and default refresh cadence, resumed on wrist raise or screen touch; Idle tokens of B5 = thinner, more transparent arc and muted text (reference to B5); Device's default = once-per-minute refresh; Platform's own guidance = replacing absent values with a dash (not followed here)
Reads at  | Continuously through the race — every 10 seconds while in power-save, and on each wrist raise or screen touch
Writes at | On entering power-save (dimming begins), every 10 seconds while in power-save (refresh), on wrist raise (full refresh), on screen touch (full refresh)

### B36 — allure-segment and allure-lissee

Consumes  | distance covered since segment start, time elapsed since segment start, instantaneous speed, correction factor (B37), segment type (RUN/non-RUN), Health Services distance data type, Health Services speed data type, watch accelerometer data, watch stride cadence data, marking event
Produces  | allure-segment (pace, min/km, displayed), allure-lissee (pace, min/km, never displayed), display at main-page center, input to lap delta (B39), input to trend-arrow orientation (B41)
Draws on  | main page — center (allure-segment only; allure-lissee draws nowhere)
Names     | allure-segment = distance covered since current segment started ÷ time elapsed since it started, × correction factor, converted to min/km; allure-lissee = 10-second rolling average of instantaneous speed, × correction factor, converted to min/km
Reads at  | continuously, on each recomputation, while the current segment is a RUN segment
Writes at | continuously, on each recomputation (display update, feed to B39 and B41); reset to zero at each marking

### B37 — Computing the correction factor

Consumes  | distance_attendue, distance mesurée (segment RUN), k_précédent, valeur de départ (bloc B38)
Produces  | k_mesuré (intermédiaire), k (facteur de correction retenu, stocké avec la course et le numéro de kilomètre), rejet (enregistrement interne stocké avec la course, non affiché)
Draws on  | —
Names     | k_mesuré = distance_attendue ÷ distance mesurée ; k = 0.6×k_mesuré + 0.4×k_précédent ; k_précédent = facteur en effet avant ce calcul (= valeur de départ du bloc B38 au premier calcul d'une course) ; distance_attendue = distance attendue pour le kilomètre (non définie dans ce bloc) ; distance mesurée = distance mesurée sur le segment RUN ; rejet = enregistrement interne conservé avec la course quand k_mesuré est hors [0.70,1.40], non affiché ; numéro de kilomètre = index du kilomètre associé au facteur retenu
Reads at  | À la fin de chaque kilomètre parcouru sur un segment RUN
Writes at | Immédiatement après le calcul, à la fin du kilomètre (stockage du facteur retenu ou du rejet avec la course)

### B38 — Starting factor and fallback

Consumes  | factor(s) computed during the race and evaluated by the guard-rail (B37), profile's current starting factor value
Produces  | profile's starting correction factor (single stored value), starting factor for the next race, uncorrected pace when factor = 1
Draws on  | —
Names     | correction factor = last factor ever retained across the whole history, default 1 if none ever retained; starting factor = correction factor used to begin a race; guard-rail = rejection mechanism described in B37; imported race = a race that never produces a factor; watch-recorded race = a race that calibrates the factor; profile = storage holding the single factor value
Reads at  | end of every race
Writes at | end of every race (when a factor is retained)

### B59 — Measured and displayed physiological data

Consumes  | —
Produces  | —
Draws on  | —
Names     | Pace = mesure physiologique affichée (une des deux seules) ; Heart rate = mesure physiologique affichée (une des deux seules) ; Calorie count = exclue, jamais mesurée/calculée/affichée ; Step count = exclue, jamais mesurée/calculée/affichée ; Displayed stride cadence = exclue, jamais mesurée/calculée/affichée ; Altitude = exclue, jamais mesurée/calculée/affichée ; Route or map of the course = exclu, jamais mesuré/calculé/affiché
Reads at  | —
Writes at | —

### B39 — Lap delta

Consumes  | distance_attendue, allure-segment, temps_référence_du_segment, temps déjà écoulé dans le segment, cadence de recalcul de l'allure, type de segment (RUN)
Produces  | temps_projeté, écart
Draws on  | —
Names     | temps_projeté = distance_attendue ÷ allure-segment (plancher : jamais < temps déjà écoulé du segment) ; écart = temps_projeté − temps_référence_du_segment ; allure-segment = valeur d'allure utilisée par ce calcul, jamais allure-lissee ; RUN = type de segment sur lequel ce delta existe
Reads at  | à chaque recalcul, à la cadence de l'allure, uniquement sur segment RUN
Writes at | à chaque recalcul, en continu, sur segment RUN

### B40 — Cumulative delta and estimated arrival

Consumes  | temps réel (par segment), temps de référence (par segment), segments clos, segment en cours, segments à venir, temps écoulé, reste du segment en cours, pointage (marking)
Produces  | écart_cumulé, arrivée
Draws on  | —
Names     | écart_cumulé = somme des (temps réel − temps de référence) sur les segments clos + l'écart propre du segment en cours ; arrivée = temps écoulé + reste du segment en cours + somme des temps de référence des segments à venir ; temps réel = non défini dans ce bloc ; temps de référence = non défini dans ce bloc ; segment (clos / en cours / à venir) = non défini dans ce bloc ; temps écoulé = non défini dans ce bloc ; pointage (marking) = non défini dans ce bloc
Reads at  | À chaque pointage, et en continu pendant le segment en cours
Writes at | À chaque pointage (recalcul complet), en continu pour la part du segment en cours

### B41 — Trend arrow

Consumes  | allure-lissee, allure-segment, état fallback de chacune
Produces  | flèche de tendance (orientée vers le haut, ou masquée)
Draws on  | —
Names     | allure-lissee = allure comparée à allure-segment, flèche vers le haut si elle est plus rapide ; allure-segment = allure de référence pour la comparaison ; fallback = état de l'une des allures qui masque la flèche ; flèche de tendance = indicateur produit par la comparaison
Reads at  | —
Writes at | —

### B42 — Zone switching hysteresis

Consumes  | lecture FC brute (bpm), zone active courante (état précédent), seuils bruts des zones (bloc B18)
Produces  | zone active/affichée (changement d'état)
Draws on  | —
Names     | zone active = zone FC actuellement affichée (sortie de ce bloc), seuils bruts = seuils de zone définis au bloc B18 (référence, non redéfinis ici), hystérésis = règle de bascule ±3bpm définie par ce bloc
Reads at  | à chaque nouvelle lecture de fréquence cardiaque
Writes at | à chaque nouvelle lecture de fréquence cardiaque (bascule de zone ou établissement à neuf après une coupure)

### B43 — Sending profile and reference to the watch

Consumes  | profile, reference race (30 segments), summarized history (capped at 20 most recent races), link between the two devices established, button press on the phone
Produces  | watch's state (profile + reference race + history, fully replaced), synchronisation result (success/failure + date of last success)
Draws on  | B16 (phone), B22 (watch)
Names     | profile = data pushed to the watch as part of the state; reference race = full race with 30 segments, always sent in full; summarized history = history capped at the 20 most recent races; watch's state = profile + reference race + summarized history, fully replaced on each push; result = success/failure + date of last success; link between the two devices = connection state that can trigger the push
Reads at  | at push time (link established, or button pressed on the phone)
Writes at | at push time (watch's state written); result updated after each push attempt

### B44 — Receiving recorded races from the watch

Consumes  | courses enregistrées par la montre non confirmées, historique descendant de la montre, état de la liaison (établie), commande de forçage depuis la montre
Produces  | course disponible sur le téléphone, confirmation de réception envoyée à la montre, effacement de la course côté montre
Draws on  | —
Names     | la montre = appareil source des courses ; le téléphone = appareil récepteur des courses ; une course = enregistrement d'activité par la montre ; la référence = donnée envoyée du téléphone vers la montre (contenu non décrit ici) ; l'historique = donnée envoyée du téléphone vers la montre (contenu non décrit ici) ; la liaison = connexion établie entre montre et téléphone (déclencheur) ; un chunk = unité de transfert (taille non précisée) ; un transfert interrompu = transfert n'ayant pas atteint sa fin, repris de zéro ; une tentative échouée = transfert non abouti, retenté à la prochaine liaison ; l'historique descendant de la montre = liste locale des courses de la montre, dans l'ordre décroissant, tant que non confirmées reçues ; l'horloge = chronomètre de course, non affecté par l'état du téléphone
Reads at  | automatiquement dès l'établissement de la liaison, ou sur forçage manuel depuis la montre
Writes at | une fois le transfert complet (apparition côté téléphone) ; à la confirmation de réception (effacement côté montre)

### B61 — Connectivity permission denied

Consumes  | état de la permission de connectivité (accordée / refusée / révoquée), disponibilité de la demande système de permission
Produces  | message "Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé.", action "Autoriser", état inactif du bouton "Synchroniser avec la montre", affichage "Aucune référence" sur la montre, ouverture de la page des réglages système de l'app
Draws on  | écran profil (téléphone) — zone de la date de dernière synchronisation ; écran montre — zone non précisée
Names     | permission de connectivité = permission nécessaire pour appairer le téléphone et la montre ; téléphone = appareil existant, utilisable seul ; montre = appareil existant, utilisable seule ; écran profil = écran existant du téléphone ; date de dernière synchronisation = élément existant, remplacé par le message et l'action "Autoriser" quand la permission manque ; "Autoriser" = action qui redemande la permission au système, ou ouvre la page de réglages de permissions de l'app si le système ne propose plus la demande ; bouton "Synchroniser avec la montre" = bouton existant, affiché mais inactif tant que la permission manque ; "Aucune référence" = texte affiché par la montre tant qu'elle n'a rien reçu ; bloc B20 = bloc cité comme vérifiant la permission capteur de la même façon (à chaque lancement)
Reads at  | à chaque lancement de l'app (vérification de la permission) ; lors de l'appui sur "Autoriser" (vérifie si le système propose encore la demande)
Writes at | à chaque lancement de l'app (mise à jour de l'affichage selon l'état de la permission) ; lors de l'appui sur "Autoriser" (déclenche une nouvelle demande système ou ouvre les réglages)

### B45 — Exercise session lifecycle

Consumes  | 30 segment markings, sensor data per type (availability-checked), arbitration outcome from B25/B26
Produces  | exercise session record (spans whole race, holds the 30 segment markings), continued race clock despite missing sensor reading, watch-face complication's return to the app throughout the race
Draws on  | Preparation screen (opening) — screen/area for the running clock and non-interactive state not named
Names     | exercise session = one per race, opened at preparation screen, closed at race end, holds all 30 segment markings, only one at a time across every app; 30 segment markings = recorded inside the session, not as separate sessions; preparation screen = where the session opens; B25, B26 = blocks arbitrating the single-session rule at start; sensor data type = availability checked before reliance, varies by device; missing sensor reading = normal case, clock unaffected; clock = keeps running regardless of missing sensor readings; the screen (non-interactive) = while true, sensor data arrives in batches rather than continuously; watch face complication = returns to the app throughout the race
Reads at  | At session start: the B25/B26 arbitration outcome and each sensor data type's availability. Continuously while open: incoming sensor data batches and segment-marking events.
Writes at | Opens the session at the preparation screen; writes each of the 30 segment markings into it as they occur; closes the session at the end of the race.

### B60 — Heart-rate data consent

Consumes  | Permission capteur OS (B20), permission historique santé (B17)
Produces  | Garantie que la FC ne quitte jamais le téléphone/la montre (pas de serveur, partage, export) ; absence d'étape de consentement applicative propre
Draws on  | —
Names     | heart-rate data = ne quitte jamais le téléphone/la montre (pas de serveur, partage, export) ; consentement applicatif = aucun (repose uniquement sur B20 + B17) ; block B20 = permission capteur OS (référence) ; block B17 = permission historique santé (référence)
Reads at  | —
Writes at | —

### B46 — Monotonic timing and recovery

Consumes  | Real wall-clock time at race start, monotonic clock readings during a segment, current segment's opening instant (read from DB on restart)
Produces  | Segment's measured duration, race total (sum of segment durations), current segment's opening instant (written to DB), resumed segment state after restart
Draws on  | —
Names     | race clock = monotonic, unaffected by system clock changes; real wall-clock time = recorded once, at the start; segment's duration = measured, never deduced; total = sum of the segments, never the total minus the others; transition = closing the previous segment and opening the next, atomic, single write; current segment's opening instant = timestamp written to DB at each transition; app restart = event that triggers resuming the current segment from its stored opening instant
Reads at  | At app restart (reads the stored opening instant); continuously via the monotonic clock while a segment runs
Writes at | At each transition (single atomic write closing the previous segment and opening the next, including the opening instant)

### B47 — Duration formats

Consumes  | durée d'un segment (duration-segment), temps total d'une course (duration-total), temps écoulé (duration-elapsed)
Produces  | texte formaté d'une durée (m:ss ou h:mm:ss) selon le type : duration-segment, duration-total, duration-elapsed
Draws on  | —
Names     | duration-segment = format m:ss, toujours sous l'heure ; duration-total = format h:mm:ss, groupe des heures conservé même à zéro (ex. "0:52:18") ; duration-elapsed = format m:ss sous 60 minutes puis h:mm:ss au-delà ; règle commune = pas de zéro initial sur le premier groupe (ex. "6:36")
Reads at  | —
Writes at | —

### B48 — Delta format

Consumes  | delta
Produces  | texte delta formaté (signe + m:ss), couleur associée au cas (avance / retard / nul)
Draws on  | —
Names     | delta = valeur numérique signée (écart de temps, non définie dans ce bloc) ; ahead = cas où delta est positif ou nul, signe "+" ; behind = cas où delta est négatif, signe "−" (U+2212) ; delta-zero = cas où delta vaut zéro, texte "+0:00" ; format = signe suivi de m:ss, toujours en m:ss même au-delà d'une heure (ex. "+72:14")
Reads at  | —
Writes at | —

### B49 — Pace, heart rate, position and zone formats

Consumes  | pace value, hr (heart rate) value, position value, zone value
Produces  | formatted pace display (M:SS + "/km"), formatted hr display (integer + "bpm"), formatted position display ("n/30"), formatted zone display ("Zone n")
Draws on  | —
Names     | pace = M:SS value + detached "/km" unit (unit smaller, text-secondary); hr = integer value + detached "bpm" unit (unit smaller, text-secondary); position = "n/30" no spaces; zone = "Zone n"; /km = unit text for pace; bpm = unit text for hr; text-secondary = style applied to unit text (smaller, secondary)
Reads at  | —
Writes at | —

### B50 — Settings and range formats

Consumes  | zone percentage value, zone range bounds, extreme zone operator and bound, distance value, press duration value
Produces  | zone percentage text, zone range text, extreme zone text, distance text, press duration text
Draws on  | —
Names     | zone percentage = integer+NBSP+"%" ; zone range = bound–bound+space+"bpm" ; extreme zone = operator+space+integer+space+"bpm" ; distance = integer+space+"m" ; press duration = integer+space+"ms"
Reads at  | —
Writes at | —

### B51 — Date formats

Consumes  | date de course (sans heure), date de course avec heure, date de dernière synchronisation, jour courant (pour comparer à "aujourd'hui")
Produces  | texte formaté "jj mmm. aaaa", texte formaté "jj mmm. aaaa · h:mm", texte formaté "aujourd'hui à h:mm"
Draws on  | —
Names     | date de course = date sans heure d'une course (jour, mois abrégé, année) ; date de course avec heure = date de course + " · " + h:mm ; date de dernière synchronisation = date de la dernière synchro, affichée "aujourd'hui à h:mm" si elle tombe le jour même, sinon au format standard ; aujourd'hui = jour courant du système
Reads at  | Au moment où une date de course ou de synchronisation doit être affichée
Writes at | —

### B52 — Rounding rule

Consumes  | duration values (ms), cumulative total values (ms)
Produces  | displayed duration truncated to the second (total); segment's displayed duration = difference of two truncated cumulative totals
Draws on  | —
Names     | duration = value stored in milliseconds; cumulative total = running sum of durations, truncated to the second for display; segment = span between two cumulative totals, displayed as the difference of their truncated values; delta = value computed on millisecond values then truncated only at display (referent unclear, see Q7)
Reads at  | at display time (reads the stored raw millisecond value)
Writes at | —

### B53 — Text resource rules

Consumes  | —
Produces  | Convention — aucune chaîne codée en dur, toute chaîne vient d'un fichier de ressources ; convention — application mono-langue (français), sans bascule ; convention — fichiers de ressources séparés téléphone/montre, clé dupliquée jamais partagée ; convention — valeur interpolée toujours passée en paramètre de ressource, jamais concaténée
Draws on  | —
Names     | fichier de ressources = source unique de toute chaîne visible ; français = seule langue de l'app ; téléphone = plateforme avec son propre fichier de ressources ; montre = plateforme avec son propre fichier de ressources ; paramètre de ressource = mécanisme de passage d'une valeur interpolée
Reads at  | —
Writes at | —

### B54 — Dynamic texts and fallbacks

Consumes  | État chargé/absent de la référence (et son nom), nom du segment fermé, date de la dernière synchronisation réussie, nom de la course à supprimer, indice de zone <n> et présence d'une lecture FC, cause de rejet (catalogue B15), texte saisi pour le nom de course, date/heure courante au format B51
Produces  | Libellé affiché ou son repli pour chaque texte listé, nom de course validé (trimé, ≤ 40 caractères) ou rejet de saisie, nom de course généré automatiquement sur la montre
Draws on  | —
Names     | nom (course/référence) = jamais vide, ≤ 40 caractères, tronqué en fin avec ellipse si trop long pour son emplacement ; segment fermé = nom cité, non défini ici ; date (dernière synchro) = date de dernier succès, sinon "Jamais synchronisé" ; n (zone) = indice de zone FC ; B15 = catalogue des huit titres de rejet, couvre toute cause de rejet ; B51 = format date-heure "12 avr. 2026 · 09:14"
Reads at  | À chaque affichage/rendu de l'élément concerné (badge référence, ligne synchro, dialogue de suppression, ligne de zone, bouton annuler)
Writes at | À la validation de la saisie du nom de course, et à la génération du nom sur la montre

### B55 — Relative date wording

Consumes  | —
Produces  | Texte de date relative affiché ("aujourd'hui à HH:MM" / "hier à HH:MM" / date complète "D mmm. AAAA à HH:MM")
Draws on  | —
Names     | "aujourd'hui à HH:MM" = formulation pour le jour même, "hier à HH:MM" = formulation pour la veille, date complète "D mmm. AAAA à HH:MM" = formulation pour toute date antérieure à hier
Reads at  | —
Writes at | —

### B56 — Fixed text catalogue

Consumes  | Catalogue de messages du bloc B15 (écran d'erreur téléphone)
Produces  | Textes fixes affichés — Montre hors course : permission screen ("Autoriser l'accès au capteur cardiaque" / "Nécessaire pour afficher ta fréquence et tes zones pendant la course." / "Autoriser"), refused-permission reminder ("⚠ Capteur cardiaque non autorisé"), waiting for the phone ("En attente du téléphone" / "Ouvre l'application sur ton téléphone pour envoyer ton profil." / "Réessayer"), home ("Démarrer" / "Historique" / "Synchroniser" / "⚠ Aucune référence"), empty history ("Aucune course" / "Synchronise depuis le téléphone."), preparation ("Fréquence cardiaque" / "Lancer" / "Quitter.") — Montre pendant la course : Projection ("arrivée estimée"), Control ("Contrôle" / "Arrêter l'activité"), stop confirmation ("Arrêter l'activité ?" / "Elle sera enregistrée telle quelle, marquée incomplète." / "Annuler" / "Arrêter"), resume-activity dialog ("Une autre activité est en cours" / "Elle sera arrêtée pour démarrer le suivi Hyrox." / "Annuler" / "Continuer"), end ("Terminer.") — Téléphone : list ("Mes courses" / "Référence" / "Incomplète"), empty list ("Aucune course encore" / "Colle un résultat officiel depuis hyresult pour importer ta première course." / "Coller un résultat"), detail ("Définir comme référence" / "Renommer" / "Supprimer"), delete confirmation ("Suppression définitive. La course disparaîtra aussi de l'historique sur la montre." / "Annuler" / "Supprimer"), rename ("Renommer la course" / "Nom" / "Annuler" / "Enregistrer"), paste ("Coller un résultat" / "Colle ici les colonnes copiées depuis hyresult…" / "Nom de la course" / "ex. Marseille 2026" / "Importer"), preview ("Aperçu avant enregistrement" / "Temps total reconnu" / "Segments détectés" / "Corriger" / "Enregistrer"), error (catalogue du bloc B15 + "Revenir au collage"), profile ("Profil" / "Fréquence cardiaque maximale" / "Maximum observé sur 12 mois" / "Modifier" / "Zones cardiaques (% FC max)" / "Distance d'un kilomètre" / "Durée de l'appui long" / "Synchroniser avec la montre"), sync ("Ne ferme pas l'application" / "Synchronisation impossible — approche la montre du téléphone." / "Réessayer.")
Draws on  | Montre — permission screen, refused-permission reminder, waiting-for-phone screen, home screen, empty-history screen, preparation screen (hors course) ; Projection area, Control area, stop-confirmation dialog, resume-activity dialog, end screen (pendant la course). Téléphone — list screen, empty-list state, detail screen, delete-confirmation dialog, rename dialog, paste screen, preview screen, error state, profile screen, sync screen.
Names     | permission screen = "Autoriser l'accès au capteur cardiaque" / "Nécessaire pour afficher ta fréquence et tes zones pendant la course." / "Autoriser" ; refused-permission reminder = "⚠ Capteur cardiaque non autorisé" ; waiting for the phone = "En attente du téléphone" / "Ouvre l'application sur ton téléphone pour envoyer ton profil." / "Réessayer" ; home = "Démarrer" / "Historique" / "Synchroniser" / "⚠ Aucune référence" ; empty history = "Aucune course" / "Synchronise depuis le téléphone." ; preparation = "Fréquence cardiaque" / "Lancer" / "Quitter." ; Projection = "arrivée estimée" ; Control = "Contrôle" / "Arrêter l'activité" ; stop confirmation = "Arrêter l'activité ?" / "Elle sera enregistrée telle quelle, marquée incomplète." / "Annuler" / "Arrêter" ; resume-activity dialog = "Une autre activité est en cours" / "Elle sera arrêtée pour démarrer le suivi Hyrox." / "Annuler" / "Continuer" ; end = "Terminer." ; list = "Mes courses" / "Référence" / "Incomplète" ; empty list = "Aucune course encore" / "Colle un résultat officiel depuis hyresult pour importer ta première course." / "Coller un résultat" ; detail = "Définir comme référence" / "Renommer" / "Supprimer" ; delete confirmation = "Suppression définitive. La course disparaîtra aussi de l'historique sur la montre." / "Annuler" / "Supprimer" ; rename = "Renommer la course" / "Nom" / "Annuler" / "Enregistrer" ; paste = "Coller un résultat" / "Colle ici les colonnes copiées depuis hyresult…" / "Nom de la course" / "ex. Marseille 2026" / "Importer" ; preview = "Aperçu avant enregistrement" / "Temps total reconnu" / "Segments détectés" / "Corriger" / "Enregistrer" ; error = catalogue du bloc B15 + "Revenir au collage" ; profile = "Profil" / "Fréquence cardiaque maximale" / "Maximum observé sur 12 mois" / "Modifier" / "Zones cardiaques (% FC max)" / "Distance d'un kilomètre" / "Durée de l'appui long" / "Synchroniser avec la montre" ; sync = "Ne ferme pas l'application" / "Synchronisation impossible — approche la montre du téléphone." / "Réessayer."
Reads at  | —
Writes at | —

### B57 — Phone navigation map

Consumes  | Importer outcome (success/failure), identity of the newly imported race, navigation path taken, whether the save succeeded (post-save stack exception)
Produces  | navigation to detail, navigation to profile, navigation to paste screen, navigation to preview, navigation to error screen, return to paste screen, return to list, removal of paste screen and preview from the stack after a successful save
Draws on  | —
Names     | race list = screen listing races; card = list item opening a race's detail; header's profile icon = control opening profile; Synchroniser = profile action, "an action on the spot" (no navigation); header's "+" button = control opening paste screen; empty list's own button = control opening paste screen; paste screen = screen for pasting; Importer = paste action leading to preview (success) or error screen (failure); preview = screen shown after a successful import parse; error screen = screen shown after a failed import parse; Corriger = preview action returning to paste; Enregistrer = preview action opening the newly imported race's detail; Revenir au collage = error screen action returning to paste; detail = screen for one race; set as reference = detail action; rename = detail action; delete = detail action, requires confirmation; confirmation = confirmation step for delete (wording not given); system back gesture = steps back one screen at a time, reversed relative to path taken, except paste and preview leave the stack after a successful save
Reads at  | at each navigation action (tap or system back gesture)
Writes at | at each screen transition (when the navigation stack changes)

### B58 — Watch navigation map

Consumes  | résultat de la demande de permission, statut « profil déjà reçu », statut « capteur occupé par une autre application », action Démarrer, action Quitter, action Lancer, action Historique, action Synchroniser, action Terminer, action annuler (Control), action stop (Control), réponse à la confirmation d'arrêt, geste balayage droit, geste retour système, geste appui long, geste système de sortie d'Historique, délai d'inactivité (8 s), compteur de pointages (jusqu'au 30e)
Produces  | transition vers l'écran d'attente téléphone, transition vers l'accueil, transition vers la préparation, transition vers le dialogue de conflit capteur (B25), transition vers la page principale de course, transition vers Projection, transition vers Control, transition vers la confirmation d'arrêt, transition vers l'écran de fin, transition vers Historique, désactivation du geste retour pendant la course, retour automatique à la page principale
Draws on  | —
Names     | Démarrer = bouton d'accueil ouvrant la préparation ; Quitter = bouton de préparation retournant à l'accueil ; Lancer = bouton de préparation ouvrant la course (via B25 si conflit capteur) ; Historique = bouton d'accueil ouvrant la liste résumée ; Synchroniser = action sur place depuis l'accueil ; Terminer = bouton de l'écran de fin retournant à l'accueil ; sensor-conflict dialog = dialogue B25, intercalé entre Lancer et le début de course si un autre app occupe le capteur ; phone-waiting screen = écran remplaçant l'accueil tant qu'aucun profil n'a jamais été reçu ; main page = première page de course ; Projection = deuxième page de course ; Control = troisième page de course ; end screen = écran atteint via stop+confirmation ou 30e pointage ; balayage droit = fait avancer main→Projection→Control ; geste retour système = désactivé sur main, Projection, Control et l'écran de fin ; appui long = depuis toute page sauf Control, marque le segment suivant et revient à la page principale ; 8 s d'inactivité = sur une page secondaire, revient à la page principale ; annuler (Control) = revient à la page principale ; stop (Control) = ouvre une confirmation puis l'écran de fin ; 30e pointage = ouvre directement l'écran de fin ; profil = statut déterminant l'affichage de l'écran d'attente téléphone (non défini plus précisément dans ce bloc)
Reads at  | au lancement de l'application, et à chaque action, geste, délai ou seuil de pointages survenant pendant la session
Writes at | immédiatement après l'action, le geste, le délai ou le seuil de pointages qui déclenche la transition

