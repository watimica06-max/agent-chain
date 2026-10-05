# Application

# Domain: Race

## Structure

### B1 — Race segment structure
Nature: model

A Hyrox race follows a fixed sequence: eight one-kilometre runs, each followed by a station, in a fixed order — SkiErg, Sled Push, Sled Pull, Burpee Broad Jump, Row, Farmers Carry, Sandbag Lunges, Wall Balls. The Roxzone, the transition area, is crossed on the way to each station and on the way back.

A race is divided into 30 segments. Each of the first seven cycles holds four segments: the kilometre run, the Roxzone toward the station, the station, the Roxzone back toward the track — 28 segments in all. The eighth kilometre is segment 29. The final block — Roxzone, Wall Balls, sprint to the finish line — is segment 30.

This breakdown matches the official race clock. An imported race and a race recorded by the watch compare segment by segment, without reconstruction.

# Domain: Design System

## Colors

### B2 — Color tokens
Nature: model

The theme defines a fixed set of color tokens, named in English, that every screen description refers to by name rather than by raw value: surface / surface-raised for the phone's backgrounds, screen-black for the watch's pure OLED background; text-primary, text-body, text-secondary and text-tertiary for decreasing emphasis; border and border-strong for separators and outlines; ahead / ahead-text / ahead-bg for a lead over the reference, behind / behind-text / behind-bg for a deficit, delta-zero for no difference; link for links; zone-1 through zone-5 for the five heart-rate zones, following a blue-to-red scale.

Exact values: surface #121110, surface-raised #1C1A18, screen-black #000000, text-primary #F3EFE7, text-body #C9C4BA, text-secondary #9A958C, text-tertiary #6F6A62, border rgba(255,255,255,0.08), border-strong rgba(255,255,255,0.25), ahead #4FAE72, ahead-text #7FCB9C, ahead-bg rgba(79,174,114,0.16), behind #E2725F, behind-text #E2957F, behind-bg rgba(226,114,95,0.16), delta-zero #726D63, link #6FA3D8, zone-1 #4A90D9, zone-2 #35B0A4, zone-3 #4CAF63, zone-4 #E0A23A, zone-5 #E0503F.

The ahead and behind colors are never used alone: a sign and an arrow always accompany them.

## Typography

### B3 — Typography tokens
Nature: model

Two type families cover the whole app: font-label (IBM Plex Sans) for labels, titles and running text, and font-data (IBM Plex Mono, tabular figures) for every timed value — its fixed-width digits keep a running clock from changing width as it counts.

Three weights cover every usage, never others: 700 for titles, values and button labels; 600 for secondary labels and menu entries; 500 for detached units and low-emphasis actions. font-data only ever uses 700, at any size.

The watch defines its own size scale in pixels on a 480×480 screen: w-display (110) for the central clock or pace on the main race page, w-display-sm (80) for the end-of-race total time, w-value (48) for heart rate and the Roxzone destination, w-value-sm (40) for Roxzone elapsed time, w-badge (37) for the delta badge, w-title (33) for out-of-race screen titles, w-label (24) for units and secondary mentions, w-label-sm (20) for the bpm unit, w-caption (18) for the zone number.

The phone defines its own scale in dp: p-title (22) for a screen title, p-value (20) for a race's total time, p-body (15) for running text, p-label (13) for setting labels, p-data (12.5) for segment rows, p-caption (11) for dates, mentions and badges.

## Shapes and spacing

### B4 — Shape, spacing and zone-arc tokens
Nature: model

radius-pill (half the height) shapes primary buttons and badges, radius-card (12) shapes cards, panels and fields, radius-chip (14) shapes delta badges. The spacing scale space-xs/s/m/l/xl (4·8·12·20·32) sets gutters. Radii and spacing are expressed in dp on the phone; on the watch they are multiplied by 1.83 to stay within the 480×480 frame of the w-* scale.

The heart-rate zone arc draws five concentric arcs at the watch face, sharing the screen's center, equal angular length, cut ends: arc-radius 229px (95% of the screen radius), arc-span 140° total centered on the bottom of the face, arc-segment 25.6° per segment, arc-gap 3° between segments, arc-width 13px for the four inactive segments, arc-width-active 33px for the active segment, arc-opacity-idle 0.30, arc-opacity-active 1. The active segment thickens toward the inside, its outer edge aligned with the four others; its radius equals arc-radius + arc-width/2 − arc-width-active/2.

The target device is a Galaxy Watch Ultra, a 1.5-inch 480×480 screen, running Wear OS 5 with One UI Watch 6, upgradable to Wear OS 6.

Letter-spacing varies by role, not by size: 0.04em on normal-size uppercase labels, including the zone number; 0.06em on group headers and small-size uppercase mentions — the cycle header, the station name, "arrivée estimée," the watch's out-of-race screen titles; 0.08em on the Control title. Running text and any timed value carry no letter-spacing.

## Idle display mode

### B5 — Idle display token variants
Nature: model

The idle display mode declines the race screens without moving any element: dim-text applies an opacity rather than a color change — 0.55 on text-primary and on any timed value, 0.45 on text-secondary and text-tertiary; the meaning colors ahead, behind and delta-zero keep their hue and take the same 0.55 opacity; no text ever changes color, only opacity; arc-width-dim (7, instead of 13) and arc-width-active-dim (22, instead of 33) thin the zone arc; arc-opacity-idle-dim (0.25, instead of 0.30) darkens it further. The arc lightens by thinning, not by a geometry change: segments stay full, just thinner and darker.

# Domain: Race Library

## Race list

### B6 — Race list screen
Nature: screen

The race list is the app's opening screen: one card per race, showing its name, date and total time; the current reference race carries a visible mark. Cards sort by date, most recent first; when two races share the same date, the one added most recently comes first — an internal, insertion-order criterion, never shown. A header button opens the paste-a-result screen. An empty list shows a message directing the user to paste a result from hyresult. An incomplete race is marked as such on its card.

Rendering: surface background. Header: p-title title in text-primary, profile icon and + button aligned right, 36–38dp circles bordered border-strong. Each card: surface-raised, radius-card; name in p-body/text-primary at left, total time in p-value/font-data at right, date in p-caption/text-secondary under the name. A Reference badge in link on a tinted background and an Incomplete badge in behind-text on behind-bg, both p-caption, radius-chip.

Empty state: centered block — title in p-title, explanation in p-body/text-secondary on a constrained width, a "Coller un résultat" pill button bordered border-strong.

## Race detail

### B7 — Race detail screen
Nature: screen

The race detail screen lists the 30 segments in order, each with its duration and cumulative time, visually grouped by cycle (kilometre, Roxzone, station, Roxzone). A delta column against the reference race is shown unless the race being viewed is itself the reference, or no reference exists.

All 30 rows always display, cycle grouping included. For a segment never reached, duration and cumulative time show a dash and the delta column stays empty; the total shown is the sum of the segments actually run.

Rendering: header shows the race name in p-title, date in p-caption/text-secondary, total time in p-value/font-data, and the current reference's badge in link. Three actions sit in a row under the header: "Définir comme référence" as a filled button, "Renommer" as a bordered button, "Supprimer" as plain text in behind.

Segments are grouped by cycle, each group preceded by a "CYCLE n" header in p-caption/text-tertiary with letter-spacing. Each row: name in p-data/text-primary, duration and cumulative time in font-data/text-secondary, delta in font-data colored ahead, behind, or delta-zero when it is nil — columns aligned to a fixed width.

## Managing a race

### B8 — Setting a race as the reference
Nature: persistence

Tapping "Définir comme référence" in a race's detail screen makes it the current reference; the previous reference loses the mark. The button is hidden, neither on the list card nor in the detail screen, when the race is incomplete or when it is already the current reference.

### B9 — Renaming a race
Nature: persistence

Tapping "Renommer" in a race's detail screen opens a field pre-filled with the current name; saving updates the stored name. The name rule of Text and Formats (block B54) applies: never empty, 40 characters maximum.

Rendering: bordered radius-card field, pre-filled with the current name, "Annuler" and "Enregistrer" buttons.

### B10 — Deleting a race
Nature: persistence

Tapping "Supprimer" in a race's detail screen asks for confirmation before deleting it. This is the only place in the app where a race is deleted. The deletion reaches the watch at the next push (block B43): a race deleted on the phone disappears from the watch's history. Deleting the current reference race is allowed; afterward no reference is designated — the app falls back to the "no reference" state, and no race is chosen automatically. Once the deletion is confirmed, the app returns to the race list: the detail screen it left described the deleted race and cannot remain displayed.

Rendering: confirmation shows a "!" badge on behind, a title naming the race, and the message "Suppression définitive. La course disparaîtra aussi de l'historique sur la montre." — when the race is the current reference, the sentence "C'est la course de référence. Après suppression, plus aucune course ne servira de comparaison." is inserted before it — "Annuler" bordered and "Supprimer" filled behind.

# Domain: Result Import

## Pasting a result

### B11 — Paste-a-result screen
Nature: screen

The user pastes the four columns copied from hyresult into a text area, names the race, and taps "Importer." Entry is by pasted text only — official results are never exported as a file, so no file picker is offered. The "Importer" button stays disabled while the paste area is empty or the name is empty, and becomes active as soon as both are filled; no inline error appears.

Rendering: a tall multiline paste field, radius-card, bordered border, placeholder text in text-tertiary. Below it, the "Nom de la course" field. A full-width "Importer" pill button.

### B12 — Reading and validating a pasted result
Nature: external source

Tapping "Importer" reads the pasted text as hyresult's official export: columns separated by a tab or by any run of multiple spaces (station names themselves contain single spaces); the first row is skipped as a header when its fourth column is not a readable time — only one row may be skipped this way, a second row with the same defect is a reading error; the number of time components sets the scale (two components = m:ss, three = h:mm:ss, and the Time column may switch scale partway through the table); the start time equals the first row's Time of Day minus its Diff.

Reading follows a state machine over the seven-cycle pattern, never a label search: "Rox In" appears seven times identically and identifies the kilometre row for cycles 1 to 7 — it marks the entry into the Roxzone, so the end of that kilometre — and the cycle number comes from the station name that follows it; "Wall Balls In" identifies kilometre 8 and switches the reading to its terminal mode. Station names map to domain segment names through an explicit table, never by string comparison: SkiErg, Sled Push and Sled Pull keep their name; Burpee BJ maps to Burpee Broad Jump; Row maps to Rameur; F. Carry maps to Farmers Carry; S. Lunges maps to Sandbag Lunges; Wall Balls keeps its name.

A paste is accepted only when three conditions hold: exactly 30 data rows; the running sum of Diff values matches the Time column on every row; the labels follow the cycle's expected order. Any other outcome fails, naming the first faulty row encountered; nothing is written — an import is never partial.

The format comes from an external site and may change its labels, abbreviations or column order without notice; a reading failure is a normal outcome, never a crash and never an approximate interpretation.

A successful reading produces a recognized total time and a segment count, read next by the preview (block B13). A failed reading produces the faulty row's number and the matching message (block B15).

### B13 — Preview before saving
Nature: screen

A successful reading (block B12) shows a preview of the recognized total time and segment count before anything is saved. "Corriger" returns to the paste screen keeping the pasted text; "Enregistrer" saves the race.

Rendering: a "✓" badge on ahead, p-title title, two label/value lines — "Temps total reconnu" and "Segments détectés" — label in text-secondary, value in font-data p-value. "Corriger" bordered, "Enregistrer" filled.

### B14 — Saving an imported race
Nature: persistence

Tapping "Enregistrer" in the preview creates a new race record under the entered name and opens its detail screen directly — never the race list. The record stores all 30 segment durations without exception; the recognized total time and segment count from block B12 serve only the preview and are not stored as such — the total recomputes by summing the segments. An imported race never produces a pace correction factor (block B38): only watch-recorded races calibrate it. No uniqueness constraint applies to the name: two races can share the same name, distinguished in the list by their date. Nothing is refused, nothing is signaled.

### B15 — Paste error screen
Nature: screen

A failed reading (block B12) shows one message at a time — the first anomaly found, read in order — naming the problem and locating the row, followed by a sentence saying what to do:

| Cause | Title | Explanation |
|---|---|---|
| Empty paste | "Rien à lire" | "Colle les quatre colonnes copiées depuis hyresult." |
| Fewer than four columns | "Colonnes manquantes — ligne <n>" | "Chaque ligne doit contenir quatre colonnes. Copie le tableau entier, en-tête compris." |
| Unreadable time | "Format de temps invalide — ligne <n>" | "Le temps doit être au format m:ss. Remplace l'espace par un deux-points." |
| Fewer than 30 segments | "<n> segments sur 30" | "Le collage est incomplet. Copie le tableau entier, de la première ligne jusqu'à « Total time »." |
| More than 30 segments | "<n> segments au lieu de 30" | "Le collage contient des lignes en trop. Copie uniquement le tableau des temps." |
| Unrecognized label | "Libellé inconnu — ligne <n>" | "« <libellé> » n'est pas un point de passage attendu. Vérifie que tu as copié un résultat Hyrox complet." |
| Label out of sequence | "Ordre inattendu — ligne <n>" | "« <libellé> » n'est pas à sa place dans la course. Copie le tableau sans le trier ni le réorganiser." |
| Inconsistent cumulative time | "Temps incohérents — ligne <n>" | "Le cumul ne correspond pas à la somme des temps. Vérifie que la ligne n'a pas été modifiée." |

"<libellé>" repeats the value read as-is, truncated to 20 characters. "Revenir au collage" always returns to the paste screen, keeping the pasted text.

Rendering: a "!" badge on behind, a title naming the faulty row, the explanation in p-body/text-secondary, then a surface-raised panel showing the row as read in behind and, as illustration, its expected form in ahead, both in font-data. No control applies the illustrated form: the user corrects the selection at its source and pastes again.

# Domain: Profile

## Settings

### B16 — Profile screen
Nature: screen

The profile screen opens from an icon in the race list's header, next to the add button. It holds four settings — maximum heart rate, the four zone thresholds, the expected kilometre distance, and the long-press duration — plus a sync button and the date of the last successful sync.

Maximum heart rate is edited in a numeric entry dialog opened by the "Modifier" link. The four zone thresholds, the kilometre distance and the long-press duration are each edited in an inline numeric field on the screen, validated on loss of focus. No stepper, no slider.

Rendering: HR max in p-value/font-data followed by its unit in p-caption/text-secondary, with "Maximum observé sur 12 mois · Modifier" underneath, the link in link color. The five zones as rows: a square zone-1..zone-5 swatch, a label, a percentage and a bpm range in font-data/text-secondary, columns aligned. The two numeric settings as label/value rows. A full-width bordered pill "Synchroniser avec la montre" button, with the last success date under it in p-caption/text-tertiary.

Sync states: in progress shows a spinning icon and "Ne ferme pas l'application"; failed shows a message in behind and a "Réessayer" button.

### B17 — Deriving maximum heart rate
Nature: external source

On first opening the profile, the app proposes a maximum heart rate read from the phone's health history: the highest value observed over the past twelve months. The value is editable by hand. No formula derives it from age — age is neither known nor requested — and neither Samsung Health's own zone configuration nor its own HR max is reachable by a third-party app.

When the health history is empty, inaccessible, or its permission is refused, the value is never guessed: the field stays to be filled in by hand, and the zone ranges (block B18) stay hidden until it is. A value entered by hand is never overwritten by a later automatic reading, and a higher value observed later is never flagged. The health history is read on the phone only.

### B18 — Zone ranges from maximum heart rate
Nature: calculation

Four thresholds bound the five zones, each threshold being the low bound of its zone: zone n runs from threshold n included to threshold n+1 excluded; zone 5 covers everything above the fourth threshold; zone 1 covers everything below the first. The default thresholds are 60, 70, 80 and 90% of the maximum heart rate.

For a maximum heart rate of 187: zone 1 under 112, zone 2 from 112 to 130, zone 3 from 131 to 149, zone 4 from 150 to 167, zone 5 from 168 up.

One arc segment is therefore always active, whatever the heart rate read; there is no reading without a zone. The profile screen presents four threshold settings (block B16). The ranges stay hidden while the maximum heart rate is unknown.

### B19 — Editing profile settings
Nature: persistence

Editing the maximum heart rate, a zone threshold, the expected kilometre distance (distance_attendue, used in the pace correction of block B37), or the long-press duration saves the new value to the profile.

Bounds: maximum heart rate is an integer from 100 to 230 bpm; the four zone thresholds are integers from 30 to 99%, strictly increasing from the first to the fourth; the kilometre distance is an integer from 500 to 2000m; the long-press duration is an integer from 300 to 2000ms, defaulting to 700ms. A value out of bounds, non-integer, or breaking the thresholds' increasing order is rejected at validation: the field reverts to its previous value and a short message states the constraint.

None of these settings apply retroactively: a recorded race is frozen — its durations, its correction factor and its heart-rate measurements are never recomputed. Each setting takes effect from the next race onward: the maximum heart rate and the zone thresholds determine the zone arc shown during a race (block B42), the expected distance enters the correction factor (block B37) and the lap delta (block B39), and the long-press duration governs marking (block B27). A setting changed on the phone reaches the watch only at the next sync (block B43): changing the maximum heart rate right before leaving, without syncing, leaves the watch working with the previous value.

# Domain: Watch Home

## First launch

### B20 — Sensor permission request
Nature: transition

On first launch, the watch asks once for access to its sensors, with a sentence explaining what it is for. A refusal leaves the app usable: the clock, segments and deltas keep working, while heart rate and the zone arc stay permanently in fallback. Permission is checked again at every subsequent launch; if it was revoked from the system settings, the same fallback applies. The request is never repeated automatically, after the first refusal or after a later revocation; a reminder on the home screen asks the system for the permission again, and if the system no longer offers that request — a permanent refusal or a revoked permission — it opens the app's permissions page in the system settings instead.

Rendering: title in w-title, explanation in w-label/text-secondary, a pill action button. Screens centered, text on three lines maximum.

### B21 — Waiting for the phone
Nature: screen

Until a profile has been received, the watch shows a waiting screen instead of the home screen: "En attente du téléphone," with a retry button.

## Home

### B22 — Home screen
Nature: screen

From top to bottom: the current reference, small — "Réf. — Bordeaux 2025 · 1:37:25," or "Aucune référence" when none is loaded; a large "Démarrer" button, active even without a reference; scrolling reveals "Historique" and "Synchroniser." "Synchroniser" is an action, not a screen: it triggers the sync push and pull (blocks B43/B44) and shows the result in place, going through the same three states as the phone (block B16), without leaving the home screen: in progress shows an activity indicator and "Ne ferme pas l'application"; failure shows "Synchronisation impossible — approche le téléphone de la montre." and "Réessayer"; success returns to the normal home screen with the reference and history up to date.

Rendering: reference line "Réf. — <name>" in w-label/text-secondary, time under it in font-data; without a reference, a "⚠ Aucune référence" badge in behind-text on behind-bg, radius-chip. "Démarrer" as a full-width pill, bordered and not filled: 2px border in text-primary, 7%-opacity text-primary fill, label in text-primary. Under it, "Historique" and "Synchroniser" as pills bordered border-strong, label in text-body.

## History

### B23 — Watch history screen
Nature: screen

The watch shows the race list in summary — name, date, total time. The segment-by-segment detail exists only on the phone. The watch is read-only on the whole configuration: no favorite change, no rename, no delete happens here.

Rendering: "Historique" title in w-label/text-tertiary, letter-spaced. One row per race: name in w-label/text-primary, date and total time on the next line in font-data/text-secondary.

## Starting a race

### B24 — Preparing and launching a race
Nature: transition

Tapping "Démarrer" opens the preparation screen (the sas): the exercise session opens, the sensors warm up, and the app checks whether a reference is loaded; heart rate shows during the wait. A "Quitter" button closes the preparation and returns to the home screen. Tapping "Lancer" starts the clock and opens the first segment; nothing is recorded before the clock starts. If opening the exercise session fails, the preparation screen stays displayed with heart rate in fallback, and "Lancer" stays active; tapping it retries opening the session. If that attempt fails too, the race starts without sensor data for its whole duration — no further retry happens once the race is running.

Rendering: "Fréquence cardiaque" label in w-caption/text-tertiary, value in font-data/w-display-sm. "Référence chargée · <name>" badge in ahead-text on ahead-bg. "Lancer" as a filled pill, "Quitter" as plain text in text-secondary.

### B25 — Starting when another app holds the sensor
Nature: transition

The device allows only one exercise session at a time, across all apps. If another app already holds it when the race starts, the watch asks for confirmation, stating that the other activity will be stopped. Continuing stops that activity and starts ours; canceling returns without starting.

Rendering ("Reprise d'activité en cours"): title, a mention that the running activity will be stopped, "Annuler" bordered and "Continuer" filled.

### B26 — Resuming our own already-active race
Nature: transition

If the exercise session already active at start belongs to our own race (the app restarted mid-race), the race resumes from the state stored in the local database rather than restarting; the sensor session itself is not restarted either.

# Domain: Race Tracking

## Interaction

### B27 — Marking a segment
Nature: transition

The whole screen is the advance button on every race page except Control: a long press anywhere — at least 700ms by default, adjustable in the profile settings (block B19) — marks the current segment as finished and opens the next one. A vibration confirms every marking taken into account. The app returns automatically to the main page after each marking, and after 8 seconds without interaction on a secondary page.

The segment's time is taken at the moment the finger touches the screen, not at release; releasing before the threshold cancels the marking and writes nothing. A slide of more than 20px during the press cancels the marking too — the gesture becomes a page swipe instead. No minimum delay separates two markings. Vibration: one short pulse confirms a marking, two short pulses signal a cancellation, nothing plays during the press itself.

## Main page

### B28 — Main page, adapting to the current segment
Nature: screen

The bottom block never changes: heart rate and the zone arc. The top and center adapt to the segment in progress.

During a kilometre: top shows the lap's delta against the reference (block B39); center, large, shows allure-segment (block B36) in min/km with a trend arrow (block B41). The comparison is lap by lap, not cumulative — a reference of 6:30 on this kilometre against a 6:00 run shows a 30-second lead.

During a station: top shows the reference's time on this station; center, large, shows the elapsed time since the station started. No delta is computed.

During a Roxzone: top shows the elapsed transition time; center, large, shows the next step — "→ SkiErg" for a station, "→ Run 3" for a kilometre. No delta is computed; a Roxzone's timing is never presented as underperformance.

Segment 30 — the combined Roxzone, Wall Balls and finish sprint (block B1) — is treated as a station: the displayed name is Wall Balls, the reference time is the reference race's final combined block, and the center shows the elapsed time since the block started. No fourth display state exists.

Without a reference loaded, four blocks disappear across the race pages: the reference time, the lap delta, the cumulative delta and the estimated arrival (block B30). The page is not reorganized — the remaining blocks keep their position.

The watch face is 1.5 inches on a round 480×480 screen: at most three legible blocks at once, never four.

Rendering (common to the three states): screen-black background, the three blocks spaced evenly with a 12%-of-diameter margin at top and 11% at bottom. A 9px dot in rgba(255,255,255,0.35), centered 6% from the top, signals the surface is actionable; no button is drawn. Delta badge: font-data, w-badge, radius-chip, ahead-text on ahead-bg or behind-text on behind-bg. Central clock or pace: font-data, w-display, text-primary, single line height. "/km" unit: font-label, w-label, text-secondary. Trend arrow: ahead or behind, aligned under the unit. Station name: font-label, w-label, text-tertiary, letter-spaced capitals. Reference time "Réf. 4:26": font-data, w-label, text-secondary. Roxzone time: font-data, w-value-sm, text-primary. Destination "→ SkiErg": font-label, w-value, arrow at 0.85 opacity; the destination name itself stays text-primary at full opacity. Heart rate: font-data, w-value, text-primary. "bpm" unit: w-label-sm, text-secondary. Zone number: w-caption, text-tertiary, letter-spaced. Without any heart-rate reading — sensor in permanent fallback, or before the first reading arrives — no zone arc is marked active: all five keep the idle style, and the heart-rate value shows a dash instead of a number. The unit and trend arrow stack to the right of the clock, aligned on its baseline; heart rate, its unit and the zone number form one centered block above the arc.

Five zone arcs of arc-segment each (block B4), separated by arc-gap, spanning arc-span centered on the bottom of the face, at arc-radius, cut ends. The current zone's arc takes arc-width-active and arc-opacity-active; the four others keep arc-width and arc-opacity-idle. Switching zone follows the hysteresis of block B42.

### B29 — Data freshness on the race pages
Nature: model

A missing value is never shown as zero: "+0:00" means "tied," not "unknown" — absence shows a dash or hides its block instead. A sensor-derived value stops updating without warning: past 10 seconds without a new reading in normal display mode, it returns to its fallback rather than keeping its last value; in power-save mode the same 10-second threshold applies, matching the refresh cadence. A fallback is never an error: no message, no interruption. The clock itself never falls back — it is always available.

## Projection page

### B30 — Projection page
Nature: screen

Swiping right from the main page opens Projection: top shows the cumulative delta since the start (block B40); center, large, shows the estimated arrival time (block B40); bottom shows the total elapsed time and the position, "14/30." The long press to mark a segment stays active on this page.

Rendering: delta badge at top, same tokens as the main page. Estimated arrival in font-data/w-display. Under it, "arrivée estimée" in w-caption/text-tertiary, letter-spaced. At the bottom, elapsed time and position on one line in font-data/w-label/text-secondary.

## Control page

### B31 — Control page
Nature: screen

Swiping right from Projection opens Control, the only race page where the surface is not the advance button. It holds two actions: undoing the last marking (block B32) and stopping the activity (block B33).

Rendering: "Contrôle" title in w-label/text-tertiary, letter-spaced. The undo button as a full-width filled pill naming the reopened segment. "Arrêter l'activité" under it, plain text in behind, less prominent than the undo button.

### B32 — Undoing the last marking
Nature: transition

Tapping the undo button on Control reopens the segment that the last marking closed; the button names that segment. Undo is single-level and only ever touches the last marking, with no time limit. Before the first marking of the race, the button is disabled.

### B33 — Stopping the race
Nature: transition

Tapping "Arrêter l'activité" on Control asks for confirmation before stopping. Confirming cuts the clock and every measurement, and saves the race as it stands, marked incomplete; an incomplete race can never become the reference (block B8). Leaving the app does not stop the running session — only this action does.

Rendering (confirmation): title, a mention that the race will be saved as it stands and marked incomplete, "Annuler" bordered and "Arrêter" filled behind.

## End of race

### B34 — End-of-race screen
Nature: screen

The 30th marking, or stopping the race early (block B33), both end it on this same screen. The screen shows the total time, the final delta against the reference, and the race's automatic name — its date and time. For a race stopped before its 30th segment, the final delta is the cumulative delta at the last closed segment, and the screen states that the race is incomplete; segments never reached enter no calculation. Saving is automatic, without confirmation. "Terminer" returns to the home screen. Without a reference loaded, the final delta is hidden instead of shown.

Rendering: a centered block — total time in font-data/w-display-sm, final delta badge under it, then date and time in font-data/w-caption/text-tertiary. "Terminer" at the bottom.

## Always-on display

### B35 — Always-on display during the race
Nature: screen

The screen stays visible through the whole race without raising the wrist. Power-save mode dims the display using the idle tokens of block B5 — thinner, more transparent arc, muted text — without moving or resizing anything. Refresh in power-save mode happens every 10 seconds rather than the device's default once-per-minute. Forcing the screen to full brightness at all times is excluded. Values stay shown, dimmed, rather than replaced with a dash as the platform's own guidance recommends — a deliberate choice. Full refresh resumes on a wrist raise as well as on a screen touch.

# Domain: Pace & Distance

## The two paces

### B36 — allure-segment and allure-lissee
Nature: calculation

allure-segment is the distance covered since the current segment started, divided by the time elapsed since it started; it is the value shown at the center of the main page and the base of the lap delta (block B39). allure-lissee is a 10-second rolling average of instantaneous speed; it is never displayed, only used to orient the trend arrow (block B41). Both are multiplied by the current correction factor (block B37) before being converted to minutes per kilometre.

Neither pace ever uses GPS or a location provider: distance covered comes from Health Services' distance and speed data types, themselves derived from the watch's own accelerometer and stride cadence. allure-segment resets to zero at every marking — it only ever covers the current segment — and is computed only on RUN segments. allure-lissee uses whatever data is available while its 10-second window is not yet full, and falls back under 3 seconds of data. allure-segment falls back under 50 meters covered in the segment.

## Correction factor

### B37 — Computing the correction factor
Nature: calculation

At the end of each kilometre: k_mesuré = distance_attendue ÷ distance measured on that RUN segment; k = 0.6 × k_mesuré + 0.4 × k_précédent. The last kilometre weighs 0.6 against 0.4 for the factor already in effect; at the first calculation of a race, k_précédent is the starting value (block B38). A k_mesuré outside [0.70, 1.40] is rejected: the factor in effect is kept, and the rejection is recorded with the race — a purely internal record, kept to allow re-analysing a calibration afterward, shown on no screen. A zero or missing measured distance produces no factor at all.

The factor never applies retroactively: a closed segment's stored duration is never recalculated — only the displayed pace is corrected, starting from the next kilometre. The factor applies to both paces (block B36). Each retained factor is stored with the race, along with the kilometre number it came from.

### B38 — Starting factor and fallback
Nature: persistence

A race's starting correction factor is the last factor ever retained, across the whole history, kept in the profile as a single value updated at the end of every race. If none has ever been retained, the starting factor is 1 and the displayed pace is uncorrected.

An imported race never produces a factor — only watch-recorded races calibrate it. If every factor computed during a race was rejected by the guard-rail (block B37), the profile's value stays unchanged. Deleting a race never changes the factor. A factor of 1 is never flagged on screen.

## Scope

### B59 — Measured and displayed physiological data
Nature: model

Pace and heart rate are the only physiological measures displayed. Calorie count, step count, displayed stride cadence, altitude, and any route or map of the course are out of scope: none of them is measured, computed or shown anywhere in the app.

# Domain: Comparison

## Lap delta

### B39 — Lap delta
Nature: calculation

temps_projeté = distance_attendue ÷ allure-segment; écart = temps_projeté − temps_référence_du_segment. It recomputes continuously, at the same cadence as the pace, and only ever uses allure-segment, never allure-lissee. The projected time never drops below the time already elapsed in the segment. This delta exists only on RUN segments.

## Cumulative delta and arrival

### B40 — Cumulative delta and estimated arrival
Nature: calculation

écart_cumulé = the sum of (real time − reference time) over closed segments, plus the current segment's own delta. arrivée = elapsed time + the remainder of the current segment + the sum of the reference times of the segments still to come. The current segment counts its reference time until that time is exceeded, then its real time once exceeded; upcoming segments always count their reference time, unweighted. Both recompute at every marking, and the current segment's share recomputes continuously.

## Trend arrow

### B41 — Trend arrow
Nature: calculation

The arrow compares allure-lissee to allure-segment. At or below a 2% difference between the two, no arrow shows; only strictly above 2% does it show. The arrow points up when allure-lissee is faster than allure-segment — that is, when the minutes-per-kilometre figure is decreasing. No arrow shows while either pace is in fallback.

## Heart-rate zone hysteresis

### B42 — Zone switching hysteresis
Nature: calculation

Switching to the zone above requires reaching its boundary plus 3bpm; switching back down requires dropping to 3bpm below that same boundary — the threshold is inclusive in both directions. Without a heart-rate reading, no zone is active. Any reading obtained always falls within a zone: there is never a known heart rate without a corresponding zone. When a reading resumes after a period with none, the zone is established anew by the plain thresholds of block B18, without hysteresis; hysteresis then applies again to subsequent readings relative to this newly established zone. The hysteresis shift applies only to the boundary between the active zone and its immediate neighbor; every other boundary applies at its plain threshold. A reading whose raw value falls in a zone two or more boundaries away from the active one moves the displayed zone directly to that zone, without passing through the zones in between.

# Domain: Sync

## Sending to the watch

### B43 — Sending profile and reference to the watch
Nature: synchronisation

A single push carries the profile, the full reference race with its 30 segments, and the summarized history, capped at the 20 most recent races — the reference itself always goes in full. It triggers automatically as soon as the link between the two devices is established, and can be forced by a button on the phone. The push fully replaces the watch's state: no merge, no comparison — a race deleted on the phone disappears from the watch at the next push.

The watch refuses any incoming push while a race is running on it, whatever it carries; the phone treats the refusal as an ordinary failure and retries at the next connection established. Nothing can therefore alter the watch's state during a race.

The result — success, failure, and the date of the last success — is visible on both devices, rendered on the phone in block B16 and on the watch in block B22.

## Receiving from the watch

### B44 — Receiving recorded races from the watch
Nature: synchronisation

Only races recorded by the watch travel up to the phone; the phone never sends races to the watch, only the reference and history. Transfer happens in chunks, automatically as soon as the link is established, or forced from the watch. A race appears on the phone only once the transfer is complete; an interrupted transfer resumes from the start. The watch erases a race only after the phone confirms it was received, and the race stays in the watch's own descending history until then. A failed attempt is retried at the next established link, never retried in between.

Nothing syncs while a race is running: an absent or dead phone has no effect on the clock.

## Connectivity permission

### B61 — Connectivity permission denied
Nature: access

Denying the connectivity permission needed to pair the phone and the watch leaves sync permanently unavailable, without affecting anything else: both apps stay fully usable on their own. The phone's profile screen shows "Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé." in place of the last-sync date, with the action "Autoriser" just below it. Tapping "Autoriser" asks the system for the permission again; if the system no longer offers that request — a permanent refusal or a revoked permission — the app opens its own permissions page in the system settings instead. The "Synchroniser avec la montre" button stays displayed but inactive as long as the permission is missing. The watch shows "Aucune référence" for as long as it has received nothing. The permission is checked at every launch, exactly as block B20 checks the sensor permission: revoking it later from the system settings produces the same state as an initial refusal. Nothing requests it automatically again.

# Domain: Sensors

## Exercise session

### B45 — Exercise session lifecycle
Nature: lifecycle

One exercise session covers the whole race, opened at the preparation screen and closed at the end; the 30 segment markings are recorded inside it, not as separate sessions. The system allows only one exercise session at a time across every app, arbitrated at start by blocks B25 and B26.

Each sensor data type's availability is checked before it is relied on — it varies by device. A missing sensor reading is a normal case; the clock keeps running regardless. While the screen is not interactive, sensor data arrives in batches rather than continuously. A complication on the watch face returns to the app throughout the race.

## Health data privacy

### B60 — Heart-rate data consent
Nature: access

Collecting and storing heart-rate data relies on the OS-level sensor permission (block B20) and health-history permission (block B17) alone; the app adds no consent step of its own. No heart-rate data ever leaves the phone and the watch: nothing is sent to a server, shared, or exported.

# Domain: Timing

## Monotonic timing

### B46 — Monotonic timing and recovery
Nature: persistence

The race clock is monotonic, unaffected by a system clock change; the real wall-clock time is recorded only once, at the start. A segment's duration is always measured, never deduced — the total is the sum of the segments, never the total minus the others. A transition is atomic: closing the previous segment and opening the next happen in a single write.

A race in progress survives an app restart: the current segment's opening instant is written to the database at the moment of marking, and on restart the segment resumes from that instant.

# Domain: Text & Formats

## Durations

### B47 — Duration formats
Nature: text

duration-segment reads m:ss for a segment's duration, always under the hour. duration-total reads h:mm:ss for a race's total time, keeping the hour group even at zero — "0:52:18" — so list columns align. duration-elapsed reads m:ss under 60 minutes, then h:mm:ss once the hour has passed. None of the three shows a leading zero on its first group: "6:36," never "06:36."

## Deltas

### B48 — Delta format
Nature: text

delta reads a sign followed by m:ss. The sign is always present, even at zero: "+0:00." Positive or nil gives "+," negative gives "−" — the minus sign is the character U+2212, never the ASCII hyphen. Color, not a different format, distinguishes the three cases: ahead, behind, or delta-zero at zero. A delta past the hour stays in m:ss — "+72:14," never "+1:12:14."

## Pace, heart rate, position

### B49 — Pace, heart rate, position and zone formats
Nature: text

pace reads m:ss with a detached "/km" unit. hr reads an integer with a detached "bpm" unit. position reads "n/30," no spaces. zone reads "Zone n." A unit is always its own element, smaller and in text-secondary, never concatenated to the value.

## Settings and ranges

### B50 — Settings and range formats
Nature: text

A zone percentage reads an integer, a non-breaking space, then "%" — "50 %." A zone range reads its bounds separated by an en dash — "94–112 bpm." An extreme zone reads an operator and a space — "< 94 bpm," "> 150 bpm." A distance reads an integer, a space, then "m," with no thousands separator — "1000 m." A press duration reads an integer, a space, then "ms" — "700 ms."

## Dates

### B51 — Date formats
Nature: text

A race's date reads day, abbreviated month, year — "12 avr. 2026." A date with time appends " · " and "h:mm" — "12 avr. 2026 · 09:14." The last sync date reads relatively when it falls today — "aujourd'hui à 09:02."

## Rounding

### B52 — Rounding rule
Nature: calculation

Durations are stored in milliseconds and displayed to the second by truncation, never by rounding. A segment's displayed duration is computed as the difference between two truncated cumulative totals, never by truncating the segment's own duration — otherwise the segments would not sum to the displayed total. A delta is computed on millisecond values, then truncated only at display.

## Resource rules

### B53 — Text resource rules
Nature: text

No visible string is ever hard-coded, on either app: every one comes from a resource file. The app ships a single language, French; no other locale exists and no switching mechanism is built. The phone and the watch keep separate resource files — a key present on both sides is duplicated, never shared. An interpolated value is always passed as a resource parameter, never concatenated into the string.

## Dynamic texts and fallbacks

### B54 — Dynamic texts and fallbacks
Nature: text

"Réf. — <nom>" shows the reference's name, replaced entirely by the "⚠ Aucune référence" badge when none is loaded. "Référence chargée · <nom>" hides its line without a reference. "Annuler : <segment fermé>" names the reopened segment, its button disabled before the first marking. "Dernière synchronisation réussie : <date>" reads "Jamais synchronisé" before any success. "Supprimer « <nom> » ?" — the name is never empty. "Zone <n>" hides its row without a heart-rate reading. The eight titles of the failure catalogue (block B15) cover every rejection cause; no generic catch-all reading-error text exists beyond them.

A race name is never empty: the entry field rejects an empty value once its leading and trailing spaces are trimmed; on the watch, the name is generated automatically. A name is capped at 40 characters at entry. Displayed, a name too long for its slot is truncated at the end with an ellipsis, never wrapped onto more than one line. A watch-generated race name follows the date-and-time format of block B51 — "12 avr. 2026 · 09:14."

## Relative dates

### B55 — Relative date wording
Nature: text

Today reads "aujourd'hui à 09:02." Yesterday reads "hier à 09:02." Anything earlier reads the full date and time — "14 sept. 2025 à 09:02."

## Fixed texts

### B56 — Fixed text catalogue
Nature: text

Watch, outside the race: permission screen — "Autoriser l'accès au capteur cardiaque" · "Nécessaire pour afficher ta fréquence et tes zones pendant la course." · "Autoriser"; refused-permission reminder — "⚠ Capteur cardiaque non autorisé"; waiting for the phone — "En attente du téléphone" · "Ouvre l'application sur ton téléphone pour envoyer ton profil." · "Réessayer"; home — "Démarrer" · "Historique" · "Synchroniser" · "⚠ Aucune référence"; empty history — "Aucune course" · "Synchronise depuis le téléphone."; preparation — "Fréquence cardiaque" · "Lancer" · "Quitter."

Watch, during the race: Projection — "arrivée estimée"; Control — "Contrôle" · "Arrêter l'activité"; stop confirmation — "Arrêter l'activité ?" · "Elle sera enregistrée telle quelle, marquée incomplète." · "Annuler" · "Arrêter"; resume-activity dialog — "Une autre activité est en cours" · "Elle sera arrêtée pour démarrer le suivi Hyrox." · "Annuler" · "Continuer"; end — "Terminer."

Phone: list — "Mes courses" · "Référence" · "Incomplète"; empty list — "Aucune course encore" · "Colle un résultat officiel depuis hyresult pour importer ta première course." · "Coller un résultat"; detail — "Définir comme référence" · "Renommer" · "Supprimer"; delete confirmation — "Suppression définitive. La course disparaîtra aussi de l'historique sur la montre." · "Annuler" · "Supprimer"; rename — "Renommer la course" · "Nom" · "Annuler" · "Enregistrer"; paste — "Coller un résultat" · "Colle ici les colonnes copiées depuis hyresult…" · "Nom de la course" · "ex. Marseille 2026" · "Importer"; preview — "Aperçu avant enregistrement" · "Temps total reconnu" · "Segments détectés" · "Corriger" · "Enregistrer"; error — block B15's message catalogue, plus "Revenir au collage"; profile — "Profil" · "Fréquence cardiaque maximale" · "Maximum observé sur 12 mois" · "Modifier" · "Zones cardiaques (% FC max)" · "Distance d'un kilomètre" · "Durée de l'appui long" · "Synchroniser avec la montre"; sync — "Ne ferme pas l'application" · "Synchronisation impossible — approche la montre du téléphone." · "Réessayer."

# Domain: Navigation

## Phone

### B57 — Phone navigation map
Nature: journey

From the race list: tapping a card opens its detail; the header's profile icon opens the profile, whose "Synchroniser" is an action on the spot; the header's "+" button, or the empty list's own button, opens the paste screen. From paste, "Importer" leads to the preview on success or to the error screen on failure; the preview's "Corriger" returns to paste, its "Enregistrer" opens the detail of the newly imported race; the error screen's "Revenir au collage" returns to paste. From detail: set as reference, rename, or delete (with confirmation). The system back gesture steps back one screen at a time, in reverse of the path taken — except that after a successful save, the paste screen and the preview leave the stack, so back from the imported race's detail returns directly to the list.

## Watch

### B58 — Watch navigation map
Nature: journey

First launch: the permission request, then waiting for the phone, then the home screen. From home: "Démarrer" opens the preparation screen, whose "Quitter" returns home, and whose "Lancer" opens the race, intercalated by the sensor-conflict dialog (block B25) only when another app holds the sensor; "Historique" opens the summarized list, returned from by the system gesture; "Synchroniser" is an action on the spot.

During the race, pages chain forward only, by a rightward swipe: main page, then Projection, then Control — no page answers a leftward swipe. The system back gesture itself is disabled throughout the race — on the main page, Projection, Control and the end screen — since an accidental gesture must never exit a running race; the stop action is the only way out. Outside a race, and on the preparation screen, the back gesture works normally. From any page but Control, a long press marks the next segment and returns to the main page automatically, as does 8 seconds of inactivity on a secondary page. Control's undo returns to the main page; its stop action opens a confirmation, then the end screen. The 30th marking also opens the end screen directly. The end screen's "Terminer" returns to the home screen.

Two screens are conditional: the sensor-conflict dialog appears only between "Lancer" and the race's start, only if another app occupies the sensor; the phone-waiting screen replaces the home screen only as long as no profile has ever been received.
