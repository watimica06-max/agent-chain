# Application

# Domaine : Design system

## Colors

### B1 — Color tokens
Nature: presentation
The application defines a fixed set of color tokens shared by both apps. `surface` is the phone's general background and `surface-raised` the background of cards and fields. `screen-black`, pure black, is the watch's background — the watch uses an OLED screen. `text-primary` carries values and titles, `text-body` carries running text, `text-secondary` carries units, dates and labels, `text-tertiary` carries mentions and cycle headers. `border` marks separators and card outlines, `border-strong` marks button outlines. `ahead` and `ahead-text` on `ahead-bg` mark being ahead of pace — arrows and badges. `behind` and `behind-text` on `behind-bg` mark being behind pace. `delta-zero` marks a null gap, neither ahead nor behind. `link` is the single accent color, used for the "Modify" action and the "Reference" badge. `zone-1` through `zone-5` mark the five heart rate zones.

### B2 — Ahead/behind pairing
Nature: presentation
`ahead` and `behind` are never used alone: wherever they color an element, a sign and an arrow accompany them.

### B3 — Heart rate zone color scale
Nature: presentation
The five heart rate zone colors follow the blue-to-red scale of heart rate, from `zone-1` to `zone-5`.

## Typography

### B4 — Font families
Nature: presentation
Two font families are used, and no other. `font-label` (IBM Plex Sans) carries labels, titles and running text. `font-data` (IBM Plex Mono, fixed-width digits) carries every timed value.

### B5 — Fixed-width digits
Nature: presentation
`font-data` renders digits at fixed width: a running clock never changes width as it updates.

### B6 — Font weights
Nature: presentation
Three font weights are used, and no other: 700 for titles, values and button labels, 600 for secondary labels, 500 for detached units and standalone texts. `font-data` uses only 700, at every size.

### B7 — Watch type scale
Nature: presentation
On the watch, on a 480 × 480 screen, in pixels:

| Token | Size | Usage |
|---|---|---|
| `w-display` | 110 | Clock or pace at the center of the main screen |
| `w-display-sm` | 80 | Total time on the end screen |
| `w-value` | 48 | Heart rate, Roxzone destination |
| `w-value-sm` | 40 | Segment elapsed time in Roxzone |
| `w-badge` | 37 | Gap in a badge |
| `w-title` | 33 | Titles of screens outside the race |
| `w-label` | 24 | Units, secondary notes |
| `w-label-sm` | 20 | The `bpm` unit |
| `w-caption` | 18 | Zone number |

### B8 — Phone type scale
Nature: presentation
On the phone, in dp:

| Token | Size | Usage |
|---|---|---|
| `p-title` | 22 | Screen title |
| `p-value` | 20 | Total time of a race |
| `p-body` | 15 | Running text |
| `p-label` | 13 | Setting labels |
| `p-data` | 12.5 | Segment lines |
| `p-caption` | 11 | Dates, notes, badges |

### B9 — Letter spacing
Nature: presentation
Letter spacing follows the role of a text, not its size. It is 0.04em on normal-size uppercase labels, including the zone number. It is 0.06em on cycle headers and small uppercase mentions — cycle header, station name, "arrivée estimée", watch screen title. It is 0.08em on the Control screen title. Neither running text nor any timed value carries letter spacing.

## Shapes and spacing

### B10 — Shape and spacing tokens
Nature: presentation
`radius-pill` is half the height of the element it rounds, used on buttons and badges. `radius-card` is 12, used on cards and fields. `radius-chip` is 14, used on gap badges. `space-xs`, `space-s`, `space-m`, `space-l`, `space-xl` are 4, 8, 12, 20 and 32, used as gutters.

### B11 — Unit conversion between phone and watch
Nature: presentation
Radii and spacing are expressed in dp on the phone. On the watch they are multiplied by 1.83 to stay within the 480 × 480 frame of the `w-*` scales.

### B12 — Heart rate zone arc geometry
Nature: presentation
The heart rate zone arc is five concentric segments centered on the screen, of equal angular length, with cut-off ends. On a 480 × 480 screen: `arc-radius` is 229 (95% of the screen radius), `arc-span` is 140° total, centered on the bottom of the screen, `arc-segment` is 25.6° per segment, `arc-gap` is 3° between two segments, `arc-width` is 13 for the four inactive segments, `arc-width-active` is 33 for the active segment, `arc-opacity-idle` is 0.30, `arc-opacity-active` is 1.

### B13 — Active arc segment thickening
Nature: presentation
The active arc segment thickens toward the inside, its outer edge aligned with that of the other four. Its radius is `arc-radius + arc-width/2 − arc-width-active/2`.

## Dimmed mode

### B14 — Dimmed mode scope
Nature: presentation
Dimmed mode declines the screens shown during a race without changing any position.

### B15 — Dimmed mode tokens
Nature: presentation
`dim-text` is an opacity laid over the existing colors, not a color of its own: 0.55 on `text-primary` and on every timed value, 0.45 on `text-secondary` and `text-tertiary`. The three color-of-meaning tokens — `ahead`, `behind`, `delta-zero` — keep their hue and take the same 0.55 opacity. No text changes color in dimmed mode, only opacity. `arc-width-dim` is 7 instead of 13 for the inactive arc segments, `arc-width-active-dim` is 22 instead of 33, `arc-opacity-idle-dim` is 0.25 instead of 0.30.

### B16 — Dimmed arc thinning
Nature: presentation
In dimmed mode the arc lightens by thinning: the segments stay solid, only thinner and darker. The geometry does not change.

---

# Domaine : Race structure

## Segment sequence

### B17 — The eight stations, in order
Nature: model
A Hyrox race is identical everywhere: eight RUN segments, each followed by a station, in a fixed order — SkiErg, Sled Push, Sled Pull, Burpee Broad Jump, Rowing, Farmers Carry, Sandbag Lunges, Wall Balls. Between the track and a station, the Roxzone is the transition zone crossed on the way there and on the way back.

### B18 — Thirty segments
Nature: model
A race is split into 30 segments. Each of the first seven cycles holds four segments in order: the RUN, the Roxzone toward the station (ROX_IN), the station, the Roxzone back to the track (ROX_OUT) — 28 segments in total. Then segment 29 is the eighth RUN, and segment 30 is the station Wall Balls, which itself covers the Roxzone, Wall Balls, then the sprint to the finish line.

### B19 — Segmentation matches official timing
Nature: model
This split matches the official timing. An imported race and a race recorded by the watch compare segment by segment, without reconstruction.

---

# Domaine : Race list

## Phone race list screen

### B20 — Race list content
Nature: presentation
The race list is the phone's opening screen, "Mes courses". One card per race shows its name, date and total time. The race set as reference carries the "Référence" badge. A race stopped in progress carries the "Incomplète" badge, and its card offers no "Set as reference" action.

### B21 — Race list sort order MODIFIED
Nature: presentation
Races are sorted by date, the most recent first. At an identical date, the race with the higher entry rank comes first — the entry rank is internal, never displayed.

### B166 — Entry rank written on entry into the local database NEW
Nature: persistence
The entry rank is written once, at the moment a race enters the local database, whichever its origin — an import or a watch-to-phone send.

### B22 — Empty race list
Nature: presentation
An empty race list shows "Aucune course encore" and "Colle un résultat officiel depuis hyresult pour importer ta première course.", with a "Coller un résultat" button that opens the result import screen.

### B23 — Race list header actions
Nature: presentation
The race list header carries a profile icon and an add button, both aligned to the right. The add button opens the result import screen. The profile icon opens the Profile screen.

### B24 — Race list rendering
Nature: presentation
Background `surface`. Header: title in `p-title`/`text-primary`, profile icon and `+` button as 36–38 dp circles bordered `border-strong`. Each race is a card in `surface-raised`, `radius-card`: name in `p-body`/`text-primary` on the left, total time in `p-value`/`font-data` on the right, date in `p-caption`/`text-secondary` under the name. The "Référence" badge is `link` on a tinted background, the "Incomplète" badge is `behind-text` on `behind-bg`, both in `p-caption`, `radius-chip`.

### B25 — Empty race list rendering
Nature: presentation
A centered block: title in `p-title`, note in `p-body`/`text-secondary` on a constrained width, "Coller un résultat" button as a bordered pill in `border-strong`.

## Watch History screen

### B26 — History screen content
Nature: presentation
The watch's History screen shows the summarized race list: name, date, total time, one line per race. The per-segment breakdown exists only on the phone.

### B27 — History screen is read-only MODIFIED
Nature: presentation
No entry and no setting exists on the watch: it is read-only on the whole configuration. The reference is not changed there, and a race is neither deleted nor renamed there.

### B167 — History screen navigation NEW
Nature: presentation
The History screen is reached from the home screen and exits only through the system back gesture — no button leads out of it.

### B28 — Empty History screen
Nature: presentation
An empty History screen shows "Aucune course" and "Synchronise depuis le téléphone."

### B29 — History screen rendering
Nature: presentation
Title "Historique" in `w-label`/`text-tertiary`, letters spaced. One line per race: name in `w-label`/`text-primary`, date and total time on the next line in `font-data`/`text-secondary`.

---

# Domaine : Race detail

## Segment breakdown

### B30 — Segment breakdown content
Nature: presentation
The race detail screen lists the 30 segments in order, each with its duration and its cumulative time, grouped visually by cycle (RUN, Roxzone, station, Roxzone).

### B31 — Incomplete race breakdown
Nature: presentation
All thirty lines stay displayed even for an incomplete race, cycle structure included: a segment never reached shows an em dash `—` for both its duration and its cumulative time, and its gap cell stays empty. The total time shown is that of the closed segments only.

### B32 — Gap column
Nature: presentation
A gap column against the reference is shown whenever the race under view is not itself the reference.

### B33 — Segment breakdown rendering
Nature: presentation
Segments are grouped by cycle, each group preceded by a "CYCLE n" header in `p-caption`/`text-tertiary`, letters spaced. Each line: name in `p-data`/`text-primary`, duration and cumulative time in `font-data`/`text-secondary`, gap in `font-data` colored `ahead`, `behind`, or `delta-zero` when it is null — columns aligned at fixed width.

## Race header and actions

### B34 — Race detail header content
Nature: presentation
The header shows the race's name, date, total time, and the badge of the reference currently set, if this race carries it.

### B35 — Race actions availability
Nature: presentation
Three actions sit under the header: "Définir comme référence", "Renommer", "Supprimer" — existing only for the first, "Définir comme référence" is hidden when the race under view is already the reference, and hidden also when it is incomplete. An incomplete race can never become the reference.

### B36 — Race header rendering
Nature: presentation
Header: name in `p-title`, date in `p-caption`/`text-secondary`, total time in `p-value`/`font-data`, badge of the current reference in `link`. The three actions sit in a row under the header: "Définir comme référence" as a full pill, "Renommer" as a bordered pill, "Supprimer" as text-only `behind`.

### B37 — Deleting a race
Nature: persistence
A race is deleted only from the race detail screen — nowhere else in the application. Deletion asks for confirmation. Deleting the reference race is allowed: the confirmation says so, and after deletion no race serves as reference any more — the application falls back to the no-reference state and does not pick another race in its place. Once deletion is confirmed, the application returns to the race list, since the detail screen being left described the race just deleted.

### B38 — Delete confirmation rendering
Nature: presentation
A "!" status icon on `behind`, a title naming the race, a note stating that deletion is final and also removes the race from the watch's history, then "Annuler" as a bordered button and "Supprimer" as a full `behind` button. When the race is the reference, an extra sentence — "C'est la course de référence. Après suppression, plus aucune course ne servira de comparaison." — is inserted before the usual note. The title and the two buttons do not change.

### B39 — Renaming a race
Nature: presentation
The rename dialog is a bordered field, `radius-card`, pre-filled with the current name, with "Annuler" and "Enregistrer" buttons.

---

# Domaine : Result import

## Paste and validate

### B40 — Import screen content
Nature: presentation
The result import screen holds a text area and an "Importer" button. The user pastes the four columns copied from hyresult; the application validates and saves them.

### B168 — Race name entry NEW
Nature: presentation
The race name is entered on this screen.

### B169 — Race date entry NEW
Nature: presentation
The race date is entered here too: the pasted result carries no date, and nothing lets one be deduced from it. The date field is pre-filled with today's date, for convenience only — an imported race is almost always older, and the pre-filled value is meant to be corrected. It is changed through a standard date picker whose range stops at today: a later date cannot be chosen, so no message exists for that case. No lower bound applies.

### B42 — Import button gating
Nature: presentation
The "Importer" button stays inactive as long as the text area, the name or the date is not filled in. No message accompanies this: the screen prevents rather than refuses.

### B43 — Text entry only
Nature: presentation
Entry happens only by pasted text, never by a file picker: official results are not exported as files.

### B44 — Landing on the imported race
Nature: presentation
After a successful save, the application lands on the detail screen of the imported race, not on the race list. The import screen and the preview screen leave the navigation stack at that point: going back from the imported race's detail screen returns to the race list.

### B45 — Import screen rendering
Nature: presentation
Text area: a tall multiline field, `radius-card`, bordered `border`, placeholder text in `text-tertiary`. Below it, the "Nom de la course" field, then the "Date de la course" field. "Importer" button full width, pill.

### B46 — Preview screen
Nature: presentation
A successful parse shows a preview before saving: a "✓" status icon on `ahead`, title "Aperçu avant enregistrement", then two label/value lines — "Temps total reconnu" and "Segments détectés" — label in `text-secondary`, value in `font-data`/`p-value`. Buttons "Corriger" (bordered, returns to the import screen) and "Enregistrer" (full).

## Result format

### B47 — Pasted result structure
Nature: external exchange
The pasted result is four tab-separated columns: `Split` names the checkpoint, `Time of Day` gives the time of day, `Time` gives the cumulative time since the start, `Diff` gives the segment's duration — this is the value stored.

### B48 — Checkpoint mapping table
Nature: external exchange
The cycle repeats seven times, then the format changes. `Rox In` maps to the RUN of cycle n. `<Station> In` maps to ROX_IN of cycle n. `<Station> Out` maps to the station of cycle n. `Rox Out` maps to ROX_OUT of cycle n. `Wall Balls In` maps to the RUN of cycle 8. `Total time` maps to the station of cycle 8. Station names appear in the pasted result as `SkiErg`, `Sled Push`, `Sled Pull`, `Burpee BJ`, `Row`, `F. Carry`, `S. Lunges`, `Wall Balls`, four of which differ from the segment names used elsewhere in the application — the mapping table is explicit, never derived by comparing strings.

### B49 — Reading the pasted result
Nature: external exchange
Reading runs a state machine on the cycle, not a search by name: `Rox In` appears seven times identically, and the cycle number comes from the station that follows it; `Wall Balls In` switches reading into its terminal mode. A header line is discarded if present — the first line is dropped when its fourth column is not a readable time; only one line may be dropped this way, and a second line showing the same anomaly is a read failure. The separator is a tab, or any run of multiple spaces — station names contain single spaces only. The number of components in a time value sets its scale: two components read as `m:ss`, three as `h:mm:ss`, and the `Time` column may switch scale partway through a result. The start time of day is the first line's `Time of Day` minus its `Diff`.

### B50 — Import validation
Nature: external exchange
An import is accepted only when three conditions hold together: exactly 30 data lines are present, the sum of `Diff` values matches `Time` at every line, and the checkpoint names follow the expected cycle order. A failure names the faulting line. Nothing is written on a failure — there is never a partial import.

### B51 — Result format fragility
Nature: external exchange
This format comes from an external site: names, abbreviations and column order can change there. A read failure is a normal case — never a crash, never an approximate interpretation.

## Import errors

### B52 — Read failure message structure
Nature: presentation
A read failure shows a fixed structure: a title naming the problem and locating the line, then a sentence saying what to do. Only one message is shown at a time — that of the first anomaly found in reading order. No generic message exists: eight causes cover every failure, each with its own title, with no catch-all fallback behind them.

### B53 — Read failure causes and messages
Nature: presentation

| Cause | Title | Note |
|---|---|---|
| Empty paste | `Rien à lire` | `Colle les quatre colonnes copiées depuis hyresult.` |
| Fewer than four columns | `Colonnes manquantes — ligne <n>` | `Chaque ligne doit contenir quatre colonnes. Copie le tableau entier, en-tête compris.` |
| Unreadable time | `Format de temps invalide — ligne <n>` | `Le temps doit être au format m:ss. Remplace l'espace par un deux-points.` |
| Fewer than 30 segments | `<n> segments sur 30` | `Le collage est incomplet. Copie le tableau entier, de la première ligne jusqu'à « Total time ».` |
| More than 30 segments | `<n> segments au lieu de 30` | `Le collage contient des lignes en trop. Copie uniquement le tableau des temps.` |
| Unrecognized name | `Libellé inconnu — ligne <n>` | `« <libellé> » n'est pas un point de passage attendu. Vérifie que tu as copié un résultat Hyrox complet.` |
| Name out of sequence | `Ordre inattendu — ligne <n>` | `« <libellé> » n'est pas à sa place dans la course. Copie le tableau sans le trier ni le réorganiser.` |
| Inconsistent cumulative time | `Temps incohérents — ligne <n>` | `Le cumul ne correspond pas à la somme des temps. Vérifie que la ligne n'a pas été modifiée.` |

`<libellé>` reproduces the value as read, truncated to 20 characters if needed. The button is always "Revenir au collage", and the pasted text is kept.

### B54 — Error screen rendering
Nature: presentation
A "!" status icon on `behind`, a title naming the faulting line, a note in `p-body`/`text-secondary`, then a `surface-raised` card showing the line as it was read, in `behind`, and the expected form, in `ahead`, both in `font-data`. This card illustrates the problem only: no automatic correction exists and no button applies one — the user corrects the source and pastes again.

---

# Domaine : Profile and settings

## Settings

### B55 — Four settings
Nature: model
The Profile screen holds four settings: maximum heart rate, four zone thresholds, the expected distance of one kilometer (`distance_attendue`), and the long-press duration.

### B56 — Maximum heart rate proposal
Nature: calculation
Maximum heart rate is proposed automatically, as the highest value observed over twelve months in the phone's health history, and can be changed manually.

### B57 — Zone thresholds
Nature: model
Four zone thresholds are set as a percentage of maximum heart rate, defaulting to 60, 70, 80 and 90%. Each threshold is the lower bound of its zone: zone n runs from threshold n, included, to threshold n+1, excluded. Zone 1 covers everything under the first threshold, zone 5 covers everything at or above the fourth. Five zones need four thresholds, so both ends of the scale stay open. For a maximum heart rate of 187: zone 1 is under 112, zone 2 is 112 to 130, zone 3 is 131 to 149, zone 4 is 150 to 167, zone 5 is 168 and above.

### B58 — Active recovery absorbed into zone 1
Nature: model
Active recovery, which the literature places under 50%, is absorbed into zone 1 rather than forming a separate category: this state does not occur during the effort of a Hyrox race, and distinguishing it would add a setting, a visual state and a fallback for no benefit.

### B170 — Expected distance default NEW
Nature: model
The expected distance of one kilometer defaults to 1000 m as long as it has never been changed.

### B171 — Long-press duration default NEW
Nature: model
The long-press duration defaults to 700 ms.

### B60 — Setting bounds
Nature: presentation
Each setting is bounded and must be an integer: maximum heart rate from 100 to 230 bpm, a zone threshold from 30 to 99% and strictly greater than the previous threshold, the expected distance from 500 to 2000 m, the long-press duration from 300 to 2000 ms. A value outside its bounds, non-integer, or breaking the ascending order of thresholds is refused on validation: the field reverts to its previous value and a short note under the field states the constraint — "Valeur attendue entre <min> et <max>.", "Nombre entier attendu.", "Chaque seuil doit être supérieur au précédent."

### B61 — No retroactive application
Nature: persistence
No setting applies retroactively. A race already created is frozen: its durations, its correction factor and its heart rate measurements are never recalculated. Each setting takes effect from the next race — maximum heart rate and the thresholds drive the arc shown during a race, the expected distance enters the correction factor and the RUN gap, the long-press duration governs marking. A setting changed on the phone reaches the watch only at the next sync: changing maximum heart rate just before leaving, without syncing, leaves the watch working with the old value.

### B62 — Health history is phone-only, no age formula
Nature: calculation
Neither the heart rate zones configured in Samsung Health nor the maximum heart rate are reachable through a third-party application: maximum heart rate is derived from the health history, the zones are computed. No formula on age applies — maximum heart rate is the highest value observed over twelve months, and age is neither known nor asked for. The derivation from the health history runs on the phone only.

### B172 — Maximum heart rate entry NEW
Nature: presentation
Maximum heart rate is edited in a numeric entry box, opened by "Modifier", shown as text-only `link`.

### B63 — Settings entry method MODIFIED
Nature: presentation
The zone thresholds, the expected distance and the long-press duration are edited in an inline numeric field on the screen, validated on loss of focus. No stepper and no slider is used for any of them.

### B64 — Settings screen rendering
Nature: presentation
Maximum heart rate in `p-value`/`font-data`, followed by its unit in `p-caption`/`text-secondary`, with under it the note "Maximum observé sur 12 mois" and the text-only "Modifier" in `link`. The five zones as rows: color square in `zone-1` through `zone-5`, label, threshold and range in `font-data`/`text-secondary`, columns aligned. Zone 1's row has no threshold of its own — it starts where the first threshold stops — and shows only its range. The two numeric settings sit as label/value rows. "Synchroniser avec la montre" button, full width, bordered pill, with under it the date of the last successful sync in `p-caption`/`text-tertiary`.

## Sync trigger and status

### B65 — Sync states on the Profile screen
Nature: presentation
"Synchroniser avec la montre" shows three states. In progress: a progress indicator and "Ne ferme pas l'application". On failure: a message in `behind` and a "Réessayer" button.

## Nearby devices permission

### B66 — Missing permission blocks sync only
Nature: external exchange
Without the nearby-devices permission, sync becomes unavailable and nothing else is affected: both applications stay fully usable on their own.

### B67 — Missing permission rendering
Nature: presentation
In place of the date of the last successful sync, the Profile screen shows "Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé.", and just under it the "Autoriser" action. The "Synchroniser avec la montre" button stays visible, inactive as long as the permission is missing. The watch itself says nothing particular about it: it shows "⚠ Aucune référence" as long as it has received nothing.

### B68 — Requesting the permission
Nature: external exchange
"Autoriser" first asks the system for the permission; if the system no longer shows the request dialog — a final refusal or a revoked permission — it opens the application's system settings page instead. The system itself indicates whether the request can still be shown: always routing to system settings would force a detour when a simple dialog would do.

### B69 — Permission re-checked on open
Nature: external exchange
The permission is checked every time the application opens. Revoked from system settings, it produces exactly the same state as an initial refusal, and no new request is triggered automatically.

## Health history permission

### B163 — Missing health history permission leaves manual entry NEW
Nature: external exchange
Without the health-history access permission, maximum heart rate cannot be derived from the health history; entering it manually stays possible.

### B164 — Requesting the health history permission NEW
Nature: external exchange
The health-history access permission is requested the first time the application needs the derivation of maximum heart rate, never when the application opens. The request first asks the system; if the system no longer shows the request dialog — a final refusal or a revoked permission — it opens the application's system settings page instead, exactly like the "Autoriser" action of the Profile screen (B68).

### B165 — Missing health history permission rendering NEW
Nature: presentation
When the health-history access permission is refused and the system no longer allows a new request, the Profile screen shows a mention explaining why the application needs the permission, with a button that opens the application's system settings page.

---

# Domaine : Watch onboarding and home

## First launch

### B70 — First launch sequence
Nature: presentation
On first launch, the watch first asks for sensor access permission, once, with a note explaining what it is for. It then waits for the phone: "Ouvre l'application sur ton téléphone pour envoyer ton profil.", with a button to retry.

### B71 — Sensor permission refused
Nature: external exchange
If sensor access permission is refused, the application stays usable: the clock, segments and gaps work; heart rate and the zone arc fall back permanently. The request is never replayed on its own — a reminder on the home screen is the only way to relaunch it, and it is an action, not automatic.

### B72 — Sensor permission reminder MODIFIED
Nature: external exchange
The reminder first asks the system for the permission; if the system no longer shows the request dialog — a final refusal or a revoked permission — it opens the application's system settings page instead, exactly like the "Autoriser" action of the Profile screen (B68).

### B173 — Sensor permission re-checked on open NEW
Nature: external exchange
The permission is checked every time the application opens; revoked from system settings rather than refused in the application, it produces exactly the same behavior as an initial refusal, and no new request is triggered automatically.

### B73 — First launch rendering
Nature: presentation
Title in `w-title`, note in `w-label`/`text-secondary`, action button as a pill. Screens are centered, text on three lines at most.

## Home screen

### B74 — Home screen content
Nature: presentation
From top to bottom: the current reference, small — "Réf. Bordeaux 2025 · 1:37:25" — or, without a loaded reference, "⚠ Aucune référence"; a large "Lancer" button at the center; and, on scrolling, "Historique" and "Synchroniser". "Lancer" stays active even without a loaded reference.

### B75 — Synchroniser action on the home screen
Nature: presentation
"Synchroniser" is an action, not a screen: it triggers a sync and shows the result of the sync in place, without leaving the home screen — the same principle as on the phone, from the Profile screen.

### B76 — Sync states on the watch home screen
Nature: presentation
Sync shows three states, displayed on the home screen without leaving it. In progress: a progress indicator and "Ne ferme pas l'application". On failure: "Synchronisation impossible — approche le téléphone de la montre." and "Réessayer". On success: return to the normal home screen, with the reference and the race list up to date.

### B77 — Home screen rendering
Nature: presentation
Reference at the top: "Réf. <nom>" in `w-label`/`text-secondary`, time below in `font-data`. Without a reference, a "⚠ Aucune référence" badge in `behind-text` on `behind-bg`, `radius-chip`. "Lancer" button as a full-width pill, bordered and not filled: a 2 px border in `text-primary`, a `text-primary` fill at 7% opacity, label in `text-primary`. Below it, "Historique" and "Synchroniser" as pills bordered `border-strong`, label in `text-body`.

## Launch and start

### B78 — Two-stage launch MODIFIED
Nature: transition
Launching happens in two stages. Preparation, at launch: the exercise session opens, the sensors ramp up, the application checks whether it has a reference — heart rate shows during the wait. Starting, at the starter's signal: the clock starts and the first segment opens. As long as the clock has not started, nothing is recorded.

### B174 — Quitter closes preparation NEW
Nature: presentation
A "Quitter" button closes preparation and returns to the home screen.

### B79 — Exercise session opens at preparation
Nature: external exchange
The exercise session opens at preparation, not at starting: the heart rate sensor needs this delay to lock on. The clock starts only at starting.

### B80 — Exercise session open failure and retry
Nature: external exchange
If opening the exercise session fails, preparation stays displayed with heart rate in fallback, and "Démarrer" stays active. Pressing "Démarrer" then retries opening the session. If that attempt also fails, the race starts and runs its whole duration without sensor data — no further attempt is made once the race is in progress.

### B81 — No pause during a race
Nature: transition
No pause exists. The only way to stop a race in progress is the stop button, on the Control screen.

### B82 — Preparation screen rendering
Nature: presentation
Label "Fréquence cardiaque" in `w-caption`/`text-tertiary`, value in `font-data`/`w-display-sm`. Badge "Référence chargée · <nom>" in `ahead-text` on `ahead-bg`. "Démarrer" button as a full pill, "Quitter" as text-only `text-secondary`.

---

# Domaine : Race in progress (watch)

## Interaction principles

### B83 — Whole screen is the mark button
Nature: presentation
The whole screen surface is the button for marking a segment, on every race screen except the Control screen. The long press works anywhere on the surface.

### B84 — Marking timing
Nature: transition
A segment closes at the instant the finger touches the screen, not at release. A release before the long-press duration records nothing. A drag of more than 20 px during the press records nothing: the gesture becomes a screen change instead. No minimum delay applies between two marks.

### B85 — Marking feedback
Nature: presentation
A vibration confirms every mark taken into account: a single short pulse validates a mark, two short pulses confirm a cancellation. Nothing vibrates during the press itself.

### B86 — Return to the main screen
Nature: presentation
The application returns automatically to the main screen after each mark, and after 8 seconds without interaction on a secondary screen.

## Main screen

### B87 — Main screen fixed bottom block
Nature: presentation
The main screen's bottom block never changes: heart rate and the heart rate zone arc. Only the top and the center adapt to the current segment.

### B88 — Main screen during a RUN
Nature: presentation
During a RUN, the top shows the RUN gap against the reference for this RUN, the center shows the segment pace (`allure-segment`) in minutes per kilometer with a trend arrow, and the bottom shows heart rate and the zone arc. The comparison is RUN by RUN, not cumulative: if the reference took 6:30 on this RUN and the current pace is 6:00, the screen shows 30 seconds ahead.

### B89 — Main screen during a station
Nature: presentation
During a station, the top shows the reference's time on this station, the center shows the segment's elapsed time, and the bottom shows heart rate and the zone arc. No gap is computed during a station.

### B90 — Main screen during a Roxzone
Nature: presentation
During a Roxzone, the top shows the segment's elapsed time, the center shows the destination — "→ SkiErg" for a station, "→ Run 3" for a RUN — and the bottom shows heart rate and the zone arc. No gap is computed during a Roxzone.

### B91 — Segment 30 treated as a station
Nature: presentation
Segment 30 — station Wall Balls, covering the Roxzone, Wall Balls, then the sprint — is treated as a station on the main screen: the name shown is "Wall Balls", the reference time is that of the Wall Balls station in the reference race, and the center shows the segment's elapsed time. No fourth screen state is created for it.

### B92 — Three states only
Nature: presentation
The main screen shows three blocks at most: the watch's screen is 1.5 inch, round, at 480 × 480, and a fourth readable block does not fit.

### B93 — Main screen rendering
Nature: presentation
Background `screen-black`. The three blocks are spaced evenly down the screen, with an inner margin of 12% at the top and 11% at the bottom of the diameter. An actionability dot of 9 px in `rgba(255,255,255,0.35)`, centered at 6% from the top, signals that the surface is actionable — no button is drawn. Gap badge: `font-data`, `w-badge`, `radius-chip`, `ahead-text` on `ahead-bg` or `behind-text` on `behind-bg`. Central clock or pace: `font-data`, `w-display`, `text-primary`, single line height. The `/km` unit: `font-label`, `w-label`, `text-secondary`. Trend arrow: `ahead` or `behind`, aligned under the unit. Station name: `font-label`, `w-label`, `text-tertiary`, letters spaced, uppercase. Reference time "Réf. 4:26": `font-data`, `w-label`, `text-secondary`. Segment elapsed time: `font-data`, `w-value-sm`, `text-primary`. Destination "→ SkiErg": `font-label`, `w-value` — the `→` character at 0.85 opacity, the name in `text-primary` at full opacity. Heart rate: `font-data`, `w-value`, `text-primary`. `bpm` unit: `w-label-sm`, `text-secondary`. Zone number: `w-caption`, `text-tertiary`, letters spaced. The unit and the trend arrow stack to the right of the clock, aligned on its baseline. Heart rate, its unit and the zone number form one centered block, above the arc.

## Heart rate zone arc

### B94 — Heart rate zone arc rendering
Nature: presentation
Five arc segments of equal size follow the low curve of the screen, one color each, `zone-1` to `zone-5`, of `arc-segment` each, separated by `arc-gap`, covering `arc-span` centered on the bottom of the screen, at radius `arc-radius`, cut off net. The active zone's segment takes `arc-width-active` and `arc-opacity-active`; the four others keep `arc-width` and `arc-opacity-idle`. Above the arc, heart rate shows in beats per minute.

## Projection screen

### B95 — Projection screen content
Nature: presentation
The Projection screen shows the cumulative gap since the start at the top, the estimated arrival time at the center, and the total elapsed time with the race position ("14/30") at the bottom. The long press to mark a segment stays active on this screen.

### B96 — Projection screen rendering
Nature: presentation
Cumulative gap badge at the top, same tokens as on the main screen. Estimated arrival in `font-data`/`w-display`, with under it "arrivée estimée" in `w-caption`/`text-tertiary`, letters spaced. At the bottom, total elapsed time and position on a single line in `font-data`/`w-label`/`text-secondary`.

## Control screen

### B97 — Control screen actions
Nature: presentation
The Control screen holds two buttons: "Annuler : <segment fermé>", which cancels the last mark and names the segment it reopens — for instance "Annuler : Roxzone → SkiErg" — and "Arrêter l'activité", which opens a stop confirmation. This is the only screen where the surface is not the mark button.

### B98 — Cancellation scope
Nature: transition
Cancellation goes one level deep and undoes only the last mark, with no time limit.

### B99 — Stopping the race MODIFIED
Nature: transition
Stopping cuts the clock and the measurements.

### B175 — Leaving the application stops nothing NEW
Nature: external exchange
An exercise session keeps running when the application is not on screen: leaving the application stops nothing.

### B100 — Control screen rendering
Nature: presentation
Title "Contrôle" in `w-label`/`text-tertiary`, letters spaced. Cancellation button as a full-width filled pill naming the segment concerned. "Arrêter l'activité" below it, as text-only `behind`, less prominent than the first button.

### B101 — Stop confirmation rendering
Nature: presentation
Title, a note stating the race will be recorded as it stands and marked incomplete, then "Annuler" bordered and "Arrêter" full `behind`.

### B102 — Exercise session resume confirmation
Nature: presentation
If another application holds an exercise session in progress when this one tries to start, the watch asks for confirmation, with the same structure: title, a note stating the session in progress will be stopped, "Annuler" and "Continuer".

## Navigation during the race

### B103 — Race screen navigation
Nature: presentation
During a race, the main screen leads to the Projection screen leads to the Control screen, both by a swipe to the right; no screen exists to the left.

### B104 — System back gesture disabled during the race
Nature: presentation
The system back gesture, normally a swipe from the left edge, is inactive throughout the whole race — main screen, Projection, Control and the end screen. Leaving a race in progress by an accidental gesture is not acceptable: the stop button is the only way out. On the preparation screen and everywhere outside a race, the gesture works normally.

## End screen

### B105 — End screen content
Nature: presentation
After the thirtieth mark, the race ends. The end screen shows the total time, the final gap against the reference, and the race's generated name — its date and time.

### B176 — Automatic recording NEW
Nature: persistence
Recording is automatic, without confirmation.

### B177 — Terminer button NEW
Nature: presentation
A "Terminer" button returns to the home screen.

### B107 — End screen for a stopped race
Nature: presentation
The same end screen serves a race stopped in progress: its final gap is the cumulative gap at the last closed segment, and the screen states that the race is incomplete. Segments never reached enter no calculation.

### B108 — Stopped race recording
Nature: persistence
A race stopped in progress is recorded as it stands and marked incomplete.

### B109 — End screen rendering
Nature: presentation
A centered block: total time in `font-data`/`w-display-sm`, final gap badge under it, then date and time in `font-data`/`w-caption`/`text-tertiary`. "Terminer" button at the bottom.

## Permanent display and dimmed rendering

### B110 — Screen stays on during the race MODIFIED
Nature: presentation
The screen stays visible throughout the race, without needing to raise the wrist.

### B178 — Dimmed mode shows values dimmed, not hidden NEW
Nature: presentation
In dimmed mode, values are visually dimmed rather than hidden — this departs from the platform's own recommendation, which would show a dash instead; here values that change live stay displayed, dimmed.

### B179 — Dimmed mode refresh cadence NEW
Nature: presentation
In dimmed mode the screen refreshes every 10 seconds, not the platform's default of once a minute. The screen stays forced on is excluded — brightness follows the platform, only the refresh cadence is raised. The screen stays very largely black; the arc lightens by thinning (B16).

### B180 — Dimmed mode exit NEW
Nature: presentation
The display returns to normal both on raising the wrist and on touching the screen.

### B112 — Dimmed rendering
Nature: presentation
`dim-text` and the `*-dim` arc variants (B15) apply. No text position and no text size changes — only the arc's thickness and the opacities vary. The actionability dot stays visible.

---

# Domaine : Pace and distance

## Segment pace and smoothed pace

### B113 — The two paces
Nature: calculation
The race happens indoors, where GPS is unusable: pace is derived from the watch's sensors, never from GPS or any location provider. `allure-segment` is the distance measured since the start of the segment divided by the segment's elapsed time; it is shown at the center of the main screen and is the basis of the RUN gap. `allure-lissee` is a running average of instantaneous speed over 10 seconds; it is never displayed and serves only to orient the trend arrow. Both are multiplied by the current correction factor, then converted to minutes per kilometer.

### B114 — Segment pace scope and reset
Nature: calculation
`allure-segment` is reset to zero at every mark: it bears only on the current segment, and it is computed only on RUN segments.

### B115 — Segment pace fallback
Nature: calculation
Under 50 meters measured within the segment, `allure-segment` is in fallback.

### B116 — Smoothed pace fallback
Nature: calculation
As long as the 10-second window for `allure-lissee` is not full, the calculation runs on what is available; under 3 seconds of data, it is in fallback.

## Correction factor

### B117 — Correction factor formula
Nature: calculation
At the end of each RUN: `k_mesuré = distance_attendue / distance_mesurée_sur_le_segment_RUN`, then `k = 0.6 × k_mesuré + 0.4 × k_précédent`, weighting the last RUN at 0.6 against 0.4 for the current factor. At the first calculation, `k_précédent` is the initial factor.

### B118 — Correction factor safety bound
Nature: calculation
A `k_mesuré` outside the interval [0.70; 1.40] is rejected: the current factor is kept, and the rejection is recorded with the race. This record is purely internal, serving only to re-analyze a calibration afterward — it appears on no screen.

### B119 — No factor on missing distance
Nature: calculation
A measured distance of zero or absent produces no factor.

### B120 — Correction factor never retroactive
Nature: calculation
The correction factor never applies retroactively: the durations of segments already closed are not recalculated. Only the displayed pace is corrected, starting from the next RUN. The factor applies to both paces (B113). Each retained factor is kept with the race, together with the number of the RUN it came from.

## Initial factor and fallback

### B121 — Initial factor source
Nature: calculation
A race's initial factor is the last factor retained across every race, kept in the profile. If a factor has already been retained, it becomes the initial factor and pace is corrected from the first RUN. If none has ever been retained, the initial factor is 1 and pace is shown uncorrected.

### B122 — Correction factor storage and scope MODIFIED
Nature: persistence
The correction factor is stored in the profile, not attached to a race: a single value, updated at the end of each race. If every factor of a race was rejected by the safety bound (B118), the profile's value stays unchanged.

### B181 — Imported race produces no factor NEW
Nature: calculation
An imported race produces no factor — only races recorded by the watch feed the calibration.

### B182 — Deleting a race leaves the factor unchanged NEW
Nature: persistence
Deleting a race does not change the factor.

### B183 — Factor of 1 not signaled NEW
Nature: presentation
A factor of 1 is not signaled on screen.

---

# Domaine : Gaps and heart rate zones

## RUN gap

### B123 — RUN gap formula
Nature: calculation
`temps_projeté = distance_attendue / allure-segment`, then `écart = temps_projeté − temps_référence_du_segment`. This exists only on RUN segments, is recalculated continuously at the cadence of pace, and rests on `allure-segment`, never on `allure-lissee`. The projected time never drops below the segment's elapsed time.

## Cumulative gap and estimated arrival

### B124 — Cumulative gap and arrival formula
Nature: calculation
`écart_cumulé = Σ (temps_réel − temps_référence) sur les segments fermés + écart par segment du segment en cours`. `arrivée = temps_écoulé + reste_du_segment_en_cours + Σ temps_référence des segments à venir`. The current segment counts toward its reference time as long as it is not overrun, then toward its actual duration once overrun. Upcoming segments count toward their reference time, unweighted. Both are recalculated at every mark, and continuously for the part of the current segment.

## Trend arrow

### B125 — Trend arrow behavior
Nature: calculation
The trend arrow compares `allure-lissee` to `allure-segment` (B113). A dead zone of 2% applies: under 2% of gap between the two paces, no arrow shows — the arrow needs strictly more than 2%, and at exactly 2% nothing shows. The arrow points up when `allure-lissee` is faster than `allure-segment`, meaning the minutes-per-kilometer figure decreases. No arrow shows while either pace is in fallback.

## Heart rate zone determination

### B126 — Zone hysteresis
Nature: calculation
Switching to the zone above requires crossing its threshold by 3 bpm; returning to the zone below requires dropping 3 bpm under that same threshold. The threshold is inclusive both ways: at exactly 3 bpm, the switch happens. Hysteresis shifts a threshold, it does not cap the speed of change: only the threshold between the active zone and its immediate neighbor is shifted, so a measurement that crosses two thresholds at once shows directly the zone containing the raw value, without passing through the intermediate zones — this is a real change of effort, not an oscillation, and delaying it would show a false zone.

### B127 — Zone reset after an interruption
Nature: calculation
After an interruption of measurements, the zone is established from scratch on the first measurement that returns, using the plain thresholds without hysteresis; hysteresis applies again from that new zone onward — heart rate may have changed a lot meanwhile, and referring to the earlier zone would show a stale one.

### B128 — Zone coverage and no-heart-rate state
Nature: calculation
Every measured heart rate falls into a zone: both ends of the threshold scale are open, so an arc segment is always active as soon as a value is measured, however low or high it is. Without heart rate, no zone is active — this is the only case with no active zone.

## Physiological measures

### B162 — Only pace and heart rate are shown
Nature: presentation
Pace and heart rate are the only physiological measures displayed anywhere in the application — no calorie count, no step count, no stride cadence, no altitude is shown.

## Roxzone note

### B129 — Roxzone gap is never framed as underperformance
Nature: presentation
A Roxzone's duration depends on the venue's layout — from 1 second to 1 min 33 depending on the station. A Roxzone gap is never presented as underperformance.

---

# Domaine : Watch-phone sync

## Content and triggering

### B130 — What each direction carries
Nature: synchronisation
Each sync direction carries exactly one thing. The phone-to-watch send is a single transmission holding the profile, the full reference race with its 30 segments, and the summarized race list. The watch-to-phone send carries only the races recorded by the watch.

### B131 — Sync triggering MODIFIED
Nature: synchronisation
Sync triggers automatically as soon as the connection between the two devices is established, in both directions.

### B184 — Forced sync from the phone NEW
Nature: synchronisation
A button on the phone forces it.

### B132 — Racing without a loaded reference
Nature: calculation
Without a loaded reference, the watch times a race normally, without a gap and without an estimated arrival.

## Transfer behavior

### B133 — Phone-to-watch send replaces state fully
Nature: synchronisation
The phone-to-watch send fully replaces the watch's state: no merge, no comparison. A race deleted on the phone disappears from the watch at the next send.

### B134 — Summarized race list is bounded
Nature: synchronisation
The summarized race list sent to the watch is bounded to the 20 most recent races. The reference always goes in full.

### B135 — Watch-to-phone send is chunked
Nature: synchronisation
The watch-to-phone send happens in chunks. A race appears on the phone only once entirely transferred; an interrupted send resumes from the start.

### B136 — Watch erases only after acknowledgment
Nature: synchronisation
The watch erases its own copy of a race only after explicit acknowledgment of receipt. It then reappears in the next summarized race list sent down to the watch.

### B137 — Failed sync retry
Nature: synchronisation
A failed sync attempt is retried at the next established connection, with no retry in between.

### B138 — No sync during a race
Nature: synchronisation
Nothing syncs during a race. A phone that is absent or out of battery has no effect on the clock.

---

# Domaine : Sensors

## Exercise session management

### B139 — One exercise session per race
Nature: external exchange
A single exercise session covers the whole race, opened at preparation and closed at the end of the race. The 30 segments are marks recorded inside it.

### B140 — Single exercise session across apps
Nature: external exchange
The platform allows only one exercise session at a time, across every application. At the start of a race, three cases apply: another application holds the session — confirmation is asked, stating that the session in progress will be stopped (B102); it is our own race's session — it resumes where it stood, its state coming from the local database, not from the exercise session; nothing is in progress — it starts normally.

### B141 — Sensor data availability check
Nature: external exchange
Availability of each type of sensor data is checked before relying on it, since it varies by device. A missing sensor reading is a normal case: the clock keeps running regardless.

### B142 — Dimmed mode sensor delivery
Nature: external exchange
In dimmed mode, sensor data is delivered in batches rather than continuously.

### B143 — System shortcut back to the app
Nature: presentation
A system shortcut on the watch face returns to the application throughout the race.

## Data privacy

### B144 — Heart rate data never leaves the devices
Nature: external exchange
No heart rate data leaves the two devices: nothing is sent to a server, nothing is shared, nothing is exported. The system permissions suffice — the application adds no consent step of its own.

---

# Domaine : Timing

## Clock rules

### B145 — Monotonic clock MODIFIED
Nature: calculation
Timing is monotonic, insensitive to a system clock change.

### B185 — Start time recorded once NEW
Nature: persistence
The start time is recorded only once.

### B146 — Segments are measured, never deduced
Nature: calculation
A segment's duration is measured, never deduced: total time is the sum of the segments, and a segment is never the total time minus the others.

### B147 — Marking is atomic
Nature: transition
A mark is atomic: closing the previous segment and opening the next happen in a single write.

### B148 — Race survives an application restart
Nature: persistence
A race in progress survives an application restart. The opening instant of the current segment is written to the local database at each mark; on restart, the segment resumes from that instant.

---

# Domaine : Data freshness

## General fallback rules

### B149 — Absence is never zero
Nature: presentation
An absent value is never shown as zero — `+0:00` means a null gap, not an unknown one. Absence shows as an em dash `—`, matching the shape of the value it replaces, or as the block being hidden.

### B150 — Staleness delay
Nature: calculation
A stale value is never frozen silently. Beyond 10 seconds without a new reading, in normal display, a sensor-derived value — heart rate, distance — returns to fallback rather than keeping its last received value. In dimmed mode, the staleness delay is that of the refresh cadence, 10 seconds as well.

### B151 — Fallback is not an error
Nature: presentation
A fallback is not an error: no message, no interruption accompanies it.

### B152 — The clock never falls back
Nature: calculation
The clock never falls back to a placeholder value, unlike other timed data.

---

# Domaine : Display formats

## Durations

### B153 — Duration formats
Nature: presentation

| Format | Pattern | Usage | Example |
|---|---|---|---|
| `duration-segment` | `m:ss` | A segment's duration — always under an hour | `6:36`, `0:01` |
| `duration-total` | `h:mm:ss` | Total time of a finished race | `1:37:25`, `0:52:18` |
| `duration-elapsed` | `m:ss` under 60 min, `h:mm:ss` from 60:00 on | Total elapsed time during a race | `52:10`, then `1:02:10` |

No leading zero on the first group: `6:36`, never `06:36`. `duration-total` keeps the hour group even at zero — `0:52:18` — to align columns in a list. `duration-elapsed` shows it only once the hour has passed.

### B154 — Rounding rules
Nature: calculation
Durations are stored in milliseconds and displayed to the second, by truncation, never by rounding. A segment's displayed duration is computed as the difference of two truncated cumulative times, never by truncating its own duration — otherwise the sum of segments would not match the total time. A gap is computed on millisecond values, then truncated for display.

## Gaps

### B155 — Gap format
Nature: presentation
`delta` is a sign followed by `m:ss`, for instance `+1:12`, `−0:30`, `+0:00`. The sign is always present, including at zero: positive or null gives `+`, negative gives `−`. The negative sign is the minus character `−` (U+2212), never the ASCII hyphen. Color distinguishes the three cases — `ahead`, `behind`, or `delta-zero` at zero — the format itself stays unique. A gap beyond an hour stays in `m:ss`: `+72:14`, not `+1:12:14`.

## Pace, heart rate, position

### B156 — Pace, heart rate, position and zone formats
Nature: presentation

| Format | Pattern | Example |
|---|---|---|
| `pace` | `m:ss` + detached unit | `6:00` `/km` |
| `hr` | integer + detached unit | `168` `bpm` |
| `position` | `n/30`, no spaces | `14/30` |
| `zone` | `Zone n` | `Zone 4` |

The unit is a distinct element, smaller and in `text-secondary`, never concatenated to the value.

## Settings and ranges

### B157 — Setting and range formats
Nature: presentation

| Data | Format | Example |
|---|---|---|
| Zone percentage | integer + non-breaking space + `%` | `60 %` |
| Zone range | bounds separated by an en dash | `112–130 bpm` |
| Extreme zone | operator + space | `< 112 bpm`, `≥ 168 bpm` |
| Distance | integer + space + `m`, no thousands separator | `1000 m` |
| Long-press duration | integer + space + `ms` | `700 ms` |

The two extreme-zone operators are not symmetric, and that is intended: a threshold belongs to the zone it opens (B57). Zone 1 stops strictly before the first threshold; zone 5 starts at the fourth threshold, included.

## Dates

### B158 — Date formats
Nature: presentation

| Usage | Format | Example |
|---|---|---|
| A race's date | day, abbreviated month, year | `12 avr. 2026` |
| Date and time | date + `·` + `h:mm` | `12 avr. 2026 · 09:14` |
| Date of the last successful sync | relative if same day | `aujourd'hui à 09:02` |

### B159 — Relative date form
Nature: presentation
Same day: `aujourd'hui à 09:02`. The day before: `hier à 09:02`. Beyond that: `14 sept. 2025 à 09:02`.

---

# Domaine : Text resources

## Text rules

### B160 — No hardcoded strings, French only
Nature: presentation
No visible string is hardcoded, on either application: everything goes through resource files. A single language is provided, French — no other locale is shipped, and no switching mechanism exists. The two applications hold separate resource files: a key present on both sides is duplicated, never shared. Interpolated values are passed as resource parameters, never concatenated.

## Text length and uniqueness

### B161 — Race name constraints MODIFIED
Nature: model
A race name is never empty: entry refuses an empty value once surrounding spaces are trimmed. The maximum length is 40 characters, enforced on entry. No uniqueness constraint applies — two races may share a name, since the date tells them apart in the list; nothing is refused, nothing is signaled.

### B186 — Race name display truncation NEW
Nature: presentation
At display, a name too long for its slot is truncated at the end with an ellipsis, never wrapped onto multiple lines.

### B187 — Generated name for a watch-recorded race NEW
Nature: calculation
A race recorded by the watch gets a generated name following the date-and-time format (B158): `12 avr. 2026 · 09:14`.
