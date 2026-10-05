
### Q1
Block: B1 — Race segment structure
Question: What happens when a segment lookup does not find the expected value (index out of range, missing segment)?
Answer:

### Q2
Block: B1 — Race segment structure
Question: Can the 30-segment race structure change after delivery (e.g. a new official race format), and if so, are comparisons already computed with the old structure recomputed?
Answer:

### Q3
Block: B1 — Race segment structure
Question: What is the "official race clock" this segment breakdown is said to match — is it an external reference, or something the app itself models?
Answer:


### Q4
Block: B2 — Color tokens
Question: What should happen when a screen references a color token name that is not in this list — a default value, an error, or is it impossible by construction?
Answer:

### Q5
Block: B2 — Color tokens
Question: Can these color token values change after delivery (e.g., an alternate theme), and if so, is anything already computed or displayed with the old values recomputed?
Answer:


### Q6
Block: B3 — Typography tokens
Question: What happens when a screen needs a font size or weight that is not in these lists (watch px scale, phone dp scale, or the three weights)?
Answer:

### Q7
Block: B3 — Typography tokens
Question: Can these typography token values (families, weights, sizes) change after delivery, and if so, is content already rendered with the old values recomputed?
Answer:

### Q8
Block: B3 — Typography tokens
Question: What is the contrasting term for "secondary" (600-weight labels) and "low-emphasis" (500-weight actions) — i.e., what counts as "primary" or higher-emphasis?
Answer:


### Q9
Block: B4 — Shape, spacing and zone-arc tokens
Question: Is applying these shape/spacing/letter-spacing tokens mandatory for every matching component, or can a component override them locally?
Answer:

### Q10
Block: B4 — Shape, spacing and zone-arc tokens
Question: What happens when a component looks up one of these tokens and it is not defined — a default value, an error, or is that case impossible by construction?
Answer:

### Q11
Block: B4 — Shape, spacing and zone-arc tokens
Question: Can these token values change after delivery, and if so, is anything already rendered with the old values recomputed?
Answer:


### Q12
Block: B5 — Idle display token variants
Question: What screen(s) and area(s) exactly display the idle variant values — the block only says "the race screens" (plural, unspecified)?
Answer:

### Q13
Block: B5 — Idle display token variants
Question: What becomes of the dimmed text and arc values when idle display mode stops being active?
Answer:

### Q14
Block: B5 — Idle display token variants
Question: Are the idle dim values recomputed on every render, or held some other way, once produced?
Answer:

### Q15
Block: B5 — Idle display token variants
Question: What triggers idle display mode itself, and can it be entered again after ending?
Answer:

### Q16
Block: B5 — Idle display token variants
Question: Which screen(s) or element(s) exactly consult these idle token values?
Answer:

### Q17
Block: B5 — Idle display token variants
Question: What happens if one of these idle token values (dim-text opacity, arc-width-dim, arc-width-active-dim, arc-opacity-idle-dim) is missing or cannot be found?
Answer:

### Q18
Block: B5 — Idle display token variants
Question: Can these idle token values change after delivery, and if so, is anything computed with the old values recomputed?
Answer:

### Q19
Block: B5 — Idle display token variants
Question: Where are the base values this block declines from (arc-width=13, arc-width-active=33, arc-opacity-idle=0.30) and the referenced tokens (text-primary, text-secondary, text-tertiary, ahead, behind, delta-zero) defined?
Answer:

### Q20
Block: B5 — Idle display token variants
Question: Do the cited names (text-primary, text-secondary, text-tertiary, ahead, behind, delta-zero, arc-width, arc-width-active, arc-opacity-idle) point to something described elsewhere, or are they marked as existing?
Answer:


### Q21
Block: B6 — Race list screen
Question: What happens to the race list screen when the user navigates away from it (does the effect undo, persist, or persist until cleared)?
Answer:

### Q22
Block: B6 — Race list screen
Question: When the screen is left, is the displayed race list kept, recomputed, or discarded?
Answer:

### Q23
Block: B6 — Race list screen
Question: When the user returns to the race list screen, does it restore its earlier state (e.g. scroll position) or is it rebuilt clean?
Answer:

### Q24
Block: B6 — Race list screen
Question: What does tapping the profile icon do, and what does tapping a race card do?
Answer:

### Q25
Block: B6 — Race list screen
Question: What does the race list screen show while loading and if loading the races fails?
Answer:

### Q26
Block: B6 — Race list screen
Question: When the system rebuilds the race list screen, what is kept from what the user had in progress and what is rebuilt from source?
Answer:

### Q27
Block: B6 — Race list screen
Question: What determines that a race is "the" reference race, what determines that a race is "incomplete", and what colour is the Reference badge's tinted background?
Answer:

### Q28
Block: B6 — Race list screen
Question: The empty state's explanation text sits "on a constrained width" — constrained relative to what (screen width, a fixed margin, something else)?
Answer:


### Q29
Block: B7 — Race detail screen
Question: What user action or event brings the user to the race detail screen?
Answer:

### Q30
Block: B7 — Race detail screen
Question: What happens to the race detail screen when the user navigates away from it?
Answer:

### Q31
Block: B7 — Race detail screen
Question: When the user leaves the race detail screen, is the displayed race data kept, recomputed, or discarded?
Answer:

### Q32
Block: B7 — Race detail screen
Question: Can the race detail screen be reopened for the same race, and if so, in what state does it come back?
Answer:

### Q33
Block: B7 — Race detail screen
Question: What does each of the three actions ("Définir comme référence", "Renommer", "Supprimer") do when activated?
Answer:

### Q34
Block: B7 — Race detail screen
Question: What does the race detail screen show when there is no data, while loading, or on failure?
Answer:

### Q35
Block: B7 — Race detail screen
Question: When the system rebuilds the race detail screen, what is kept from what the user has in progress, and what is rebuilt from its source?
Answer:

### Q36
Block: B7 — Race detail screen
Question: Is "the reference race" an attribute of this screen itself, or does it depend on a mechanism defined elsewhere?
Answer:

### Q37
Block: B7 — Race detail screen
Question: Which block describes how a race becomes "the reference" (the mechanism behind the "Définir comme référence" action)?
Answer:


### Q38
Block: B8 — Setting a race as the reference
Question: What becomes of the reference designation if the race record or the reference mechanism's structure changes (e.g. the referenced race is deleted, or the storage of the reference mark changes)?
Answer:


### Q39
Block: B9 — Renaming a race
Question: What area/position does the renaming field occupy on the race's detail screen (modal overlay, inline replacement, bottom sheet, or something else)?
Answer:

### Q40
Block: B9 — Renaming a race
Question: What does tapping "Annuler" do exactly (discard the typed changes and close the field, revert to the previous display, something else)?
Answer:

### Q41
Block: B9 — Renaming a race
Question: If the stored name's structure changes, what happens to the name field of existing records?
Answer:


### Q42
Block: B10 — Deleting a race
Question: What screen or area does the deletion confirmation ("behind") appear on or over?
Answer:

### Q43
Block: B10 — Deleting a race
Question: What happens when the user taps "Annuler" in the deletion confirmation?
Answer:

### Q44
Block: B10 — Deleting a race
Question: If the race data structure changes, what happens to already-stored (deleted or existing) race records?
Answer:


### Q45
Block: B11 — Paste-a-result screen
Question: What navigation or user action brings the user to this screen?
Answer:

### Q46
Block: B11 — Paste-a-result screen
Question: What happens to the pasted text and the race name if the user leaves this screen without tapping "Importer"?
Answer:

### Q47
Block: B11 — Paste-a-result screen
Question: Is the pasted text and the entered race name kept, recomputed, or deleted when the user leaves the screen?
Answer:

### Q48
Block: B11 — Paste-a-result screen
Question: If the user reopens this screen, does it resume its previous state or start clean?
Answer:

### Q49
Block: B11 — Paste-a-result screen
Question: What does the screen show during import processing (loading) and if the import fails (e.g. invalid pasted content)?
Answer:

### Q50
Block: B11 — Paste-a-result screen
Question: When the system rebuilds this screen, is the pasted text and the entered race name kept, or is the screen rebuilt empty?
Answer:

### Q51
Block: B11 — Paste-a-result screen
Question: What are the exact four columns expected in the text copied from hyresult, and what is hyresult exactly?
Answer:

### Q52
Block: B11 — Paste-a-result screen
Question: The paste field is described as "tall" — tall compared to what reference?
Answer:


### Q53
Block: B12 — Reading and validating a pasted result
Question: What is the exact column order of the pasted export (which position holds the station name, Time of Day, Diff and Time columns), and specifically which of these is "the fourth column" used for header detection?
Answer:

### Q54
Block: B12 — Reading and validating a pasted result
Question: After a reading (successful or failed) is produced and passed to B13 or B15, is that result kept, recomputed, or discarded — and when?
Answer:

### Q55
Block: B12 — Reading and validating a pasted result
Question: Can the user retry the import after a failed reading, and is the previously pasted text or reading state retained or cleared when they do?
Answer:

### Q56
Block: B12 — Reading and validating a pasted result
Question: What makes two pasted results the same import (deduplication criterion), and what happens to the second one when it is detected?
Answer:

### Q57
Block: B12 — Reading and validating a pasted result
Question: What exact sequence of station labels constitutes "the cycle's expected order" that a valid paste must follow?
Answer:


### Q58
Block: B13 — Preview before saving
Question: What happens to the previously recognized total time and segment count when the user returns to the paste screen via "Corriger" — are they kept, recomputed, or discarded?
Answer:

### Q59
Block: B13 — Preview before saving
Question: When a new successful reading occurs after using "Corriger", does this preview screen start from a clean state or resume the previously displayed values?
Answer:

### Q60
Block: B13 — Preview before saving
Question: What does this screen show while "Enregistrer" is saving the race (loading state), and if the save fails?
Answer:

### Q61
Block: B13 — Preview before saving
Question: If the system rebuilds this screen (e.g., after being backgrounded), is anything on it kept, or is it fully rebuilt from B12's result?
Answer:

### Q62
Block: B13 — Preview before saving
Question: What is the exact wording of the title (p-title) shown on this screen?
Answer:


### Q63
Block: B14 — Saving an imported race
Question: Can the user return to the preview and tap "Enregistrer" again after a race has already been saved, and if so, does this create a duplicate record?
Answer:

### Q64
Block: B14 — Saving an imported race
Question: If the stored structure of a race record changes later, what happens to races already saved by this block?
Answer:


### Q65
Block: B15 — Paste error screen
Question: When two anomalies could apply at once, does the display order follow the fixed order of causes in the table, or the order of the rows in the pasted data?
Answer:

### Q66
Block: B15 — Paste error screen
Question: If a failed reading occurs again after a first error was shown, does the screen start from a clean state or does anything carry over from the previous attempt?
Answer:

### Q67
Block: B15 — Paste error screen
Question: What does this screen show when there is no data yet, while it is loading, or when the detected anomaly matches none of the eight listed causes?
Answer:

### Q68
Block: B15 — Paste error screen
Question: When the system rebuilds this screen, what is kept from what the user has in progress, and what is rebuilt from its source?
Answer:

### Q69
Block: B15 — Paste error screen
Question: What are "behind", "ahead", "font-data", "surface-raised" and "p-body/text-secondary" — where are these visual terms defined?
Answer:

### Q70
Block: B15 — Paste error screen
Question: Which block or screen is "the paste screen" that "Revenir au collage" returns to?
Answer:


### Q71
Block: B16 — Profile screen
Question: What happens if the user navigates away from the profile screen while a sync is in progress, or while the HR max dialog is open?
Answer:

### Q72
Block: B16 — Profile screen
Question: What is shown for the profile settings (HR max, zone thresholds, km distance, long-press duration) when they have no value yet or are still loading — only the sync in-progress/failure states are specified?
Answer:

### Q73
Block: B16 — Profile screen
Question: When the system rebuilds the profile screen, what is kept (e.g. in-progress input) versus rebuilt from source?
Answer:


### Q74
Block: B17 — Deriving maximum heart rate
Question: Can the automatic proposal of maximum heart rate be triggered again after the first opening — for example if permission is granted later, or the profile is reset or recreated — or is it strictly a one-time event?
Answer:

### Q75
Block: B17 — Deriving maximum heart rate
Question: What happens when the phone's health history returns an invalid value (e.g. an implausible or out-of-range heart rate) rather than being empty, inaccessible, or permission-refused?
Answer:


### Q76
Block: B18 — Zone ranges from maximum heart rate
Question: What triggers the (re)computation of the zone ranges — a change to the maximum heart rate, a change to a threshold, opening a screen, or something else?
Answer:

### Q77
Block: B18 — Zone ranges from maximum heart rate
Question: On which screen, and in which area of it, are the computed zone ranges displayed?
Answer:

### Q78
Block: B18 — Zone ranges from maximum heart rate
Question: When the maximum heart rate or a threshold changes after ranges were already computed, what happens to the previously computed ranges — kept, recomputed, or deleted?
Answer:

### Q79
Block: B18 — Zone ranges from maximum heart rate
Question: When the calculation runs again, does it start clean or resume from an earlier computed state?
Answer:

### Q80
Block: B18 — Zone ranges from maximum heart rate
Question: What happens when the thresholds are not strictly increasing (e.g. a later threshold rounds to the same or a lower bpm value than an earlier one) — is this prevented, and if not, what does the resulting zone become?
Answer:

### Q81
Block: B18 — Zone ranges from maximum heart rate
Question: What is the "arc segment" that is always active — what does it look like, and on which screen/area does it appear?
Answer:


### Q82
Block: B19 — Editing profile settings
Question: On which screen and in which area does the editing of a profile setting (maximum heart rate, zone threshold, distance_attendue, long-press duration) take place?
Answer:

### Q83
Block: B19 — Editing profile settings
Question: If the profile's data structure changes, what happens to the values already stored for existing profiles?
Answer:

### Q84
Block: B19 — Editing profile settings
Question: Can a profile setting be stored incomplete, and if so, does it then hold an absence or an empty value?
Answer:

### Q85
Block: B19 — Editing profile settings
Question: What is "the profile" that these settings are saved to — is it described or defined elsewhere?
Answer:


### Q86
Block: B20 — Sensor permission request
Question: What exact position/area does the home-screen reminder occupy on the home screen?
Answer:

### Q87
Block: B20 — Sensor permission request
Question: When sensor permission becomes granted after having been refused or revoked, does the fallback state end immediately or only at the next app launch?
Answer:

### Q88
Block: B20 — Sensor permission request
Question: Is there a way back to the "granted" state from "revoked" or "permanently refused", and if so how is it detected by the app?
Answer:


### Q89
Block: B21 — Waiting for the phone
Question: Can the waiting screen reappear after the profile has already been received once (e.g. after a disconnection), and if so, does it resume from an earlier state or reset clean?
Answer:

### Q90
Block: B21 — Waiting for the phone
Question: What does the retry button do when tapped?
Answer:

### Q91
Block: B21 — Waiting for the phone
Question: What does this screen show while a retry is in progress, or if the retry fails?
Answer:

### Q92
Block: B21 — Waiting for the phone
Question: What becomes of this screen (any state in progress) when the system rebuilds it?
Answer:

### Q93
Block: B21 — Waiting for the phone
Question: What is a "profile" here — what does it contain, and is it an existing concept described elsewhere?
Answer:


### Q94
Block: B22 — Home screen
Question: What event causes the Home screen to be displayed (app launch, return navigation, or something else)?
Answer:

### Q95
Block: B22 — Home screen
Question: What happens if the user leaves the Home screen or closes the application while a synchronization is in progress?
Answer:

### Q96
Block: B22 — Home screen
Question: What does tapping "Démarrer" do, and what does tapping "Historique" do?
Answer:

### Q97
Block: B22 — Home screen
Question: What is kept and what is rebuilt on the Home screen when the system rebuilds it (e.g. after the process is killed and restored)?
Answer:

### Q98
Block: B22 — Home screen
Question: Is "the current reference" (name and duration shown at the top of the Home screen) something this screen sets itself, or is it always provided from elsewhere?
Answer:

### Q99
Block: B22 — Home screen
Question: Which block or feature is responsible for loading/setting "the current reference" that the Home screen displays?
Answer:


### Q100
Block: B23 — Watch history screen
Question: What action or event triggers the display of the watch history screen?
Answer:

### Q101
Block: B23 — Watch history screen
Question: In what order are races listed on the watch history screen, and what breaks a tie when two races share the same ordering key?
Answer:

### Q102
Block: B23 — Watch history screen
Question: What happens when the user leaves the watch history screen?
Answer:

### Q103
Block: B23 — Watch history screen
Question: What becomes of the rendered race list once the user leaves the screen — kept, recomputed, or deleted?
Answer:

### Q104
Block: B23 — Watch history screen
Question: Can the watch history screen be reopened, and if so is its earlier state restored or does it rebuild clean?
Answer:

### Q105
Block: B23 — Watch history screen
Question: What happens when the user taps a race row on the watch history screen?
Answer:

### Q106
Block: B23 — Watch history screen
Question: What is shown on the watch history screen when there is no race data, while loading, or on failure?
Answer:

### Q107
Block: B23 — Watch history screen
Question: When the system rebuilds the watch history screen, what is kept from what the user had in progress, and what is rebuilt from source?
Answer:


### Q108
Block: B24 — Preparing and launching a race
Question: What becomes of the already-opened exercise session and the warming-up sensors when the user taps "Quitter" during preparation?
Answer:

### Q109
Block: B24 — Preparing and launching a race
Question: When "Démarrer" is tapped again after a "Quitter", does the preparation resume from its earlier state (session, reference check, heart rate) or does it start clean?
Answer:


### Q110
Block: B25 — Starting when another app holds the sensor
Question: What area or layout does the "Reprise d'activité en cours" screen occupy — a full screen, or an overlay on top of another screen?
Answer:

### Q111
Block: B25 — Starting when another app holds the sensor
Question: If the other app releases the sensor on its own while the confirmation is being shown (before the user responds), what happens to the confirmation?
Answer:

### Q112
Block: B25 — Starting when another app holds the sensor
Question: After canceling, if the user attempts to start the race again, can this confirmation be triggered again, and does it start from a clean state?
Answer:

### Q113
Block: B25 — Starting when another app holds the sensor
Question: What happens if the user takes no action on the confirmation (no response, or a timeout)?
Answer:

### Q114
Block: B25 — Starting when another app holds the sensor
Question: What is the exact wording of the mention stating that the running activity will be stopped?
Answer:


### Q115
Block: B26 — Resuming our own already-active race
Question: What happens when the condition that triggered the resume (active session belonging to our own race) stops being true afterwards?
Answer:

### Q116
Block: B26 — Resuming our own already-active race
Question: What becomes of the resumed race state afterward — is it kept, recomputed, or deleted?
Answer:

### Q117
Block: B26 — Resuming our own already-active race
Question: Can this resume mechanism fire again (e.g. another app restart during the same race), and if so what happens?
Answer:

### Q118
Block: B26 — Resuming our own already-active race
Question: What are all the states this transition can be in, and which states can reach which others?
Answer:


### Q119
Block: B27 — Marking a segment
Question: What happens when the segment being marked is the last one of the race — is there a next segment to open, or does a different mechanism apply?
Answer:

### Q120
Block: B27 — Marking a segment
Question: What does "secondary page" mean for the 8-second auto-return timeout — is it the same set as "every race page except Control", or a different set of pages?
Answer:


### Q121
Block: B28 — Main page, adapting to the current segment
Question: What happens to the previously displayed segment's values (delta, elapsed time, destination) once a new segment starts — are they kept, recomputed, or discarded?
Answer:

### Q122
Block: B28 — Main page, adapting to the current segment
Question: What happens when the user taps the actionable surface (the dot indicator) on the main page?
Answer:

### Q123
Block: B28 — Main page, adapting to the current segment
Question: What does the main page show during a loading state, or on a general failure, beyond the two documented cases of missing reference and missing heart-rate reading?
Answer:

### Q124
Block: B28 — Main page, adapting to the current segment
Question: When the system rebuilds the main page (e.g. app restart), what is kept from what the user had in progress, and what is rebuilt from source?
Answer:

### Q125
Block: B28 — Main page, adapting to the current segment
Question: Where are the style tokens used in this block (font-data, w-display, text-primary, arc-segment, arc-gap, etc.) and the "loaded reference" concept defined?
Answer:


### Q126
Block: B29 — Data freshness on the race pages
Question: Which specific area(s) of the race pages does this freshness rule apply to?
Answer:

### Q127
Block: B29 — Data freshness on the race pages
Question: When a new sensor reading arrives after the fallback state has been triggered, does the display resume showing live values immediately?
Answer:

### Q128
Block: B29 — Data freshness on the race pages
Question: What happens to an already-displayed fallback (dash / hidden block) once the missing data becomes available again — is it replaced automatically?
Answer:

### Q129
Block: B29 — Data freshness on the race pages
Question: Can the fallback state be triggered again after it clears, and does it resume from where it left off or start from a clean state?
Answer:

### Q130
Block: B29 — Data freshness on the race pages
Question: Is the sensor-derived value's "fallback" the same dash/hidden-block treatment defined for a missing value, or a distinct display?
Answer:

### Q131
Block: B29 — Data freshness on the race pages
Question: What is the refresh cadence of power-save mode, to confirm it matches the stated 10-second staleness threshold?
Answer:


### Q132
Block: B30 — Projection page
Question: What closes the Projection page (e.g. swiping back), and what happens then?
Answer:

### Q133
Block: B30 — Projection page
Question: When the user leaves the Projection page, are the displayed delta, arrival time, elapsed time and position values kept, recomputed, or discarded on return?
Answer:

### Q134
Block: B30 — Projection page
Question: What does the Projection page show when there is no data, while loading, or on failure?
Answer:

### Q135
Block: B30 — Projection page
Question: When the system rebuilds the Projection screen, what is kept from what the user had in progress, and what is rebuilt from its source?
Answer:

### Q136
Block: B30 — Projection page
Question: What exactly does "total elapsed time" measure (start point, format), and what do the two numbers in the position indicator (e.g. "14/30") represent?
Answer:


### Q137
Block: B31 — Control page
Question: What happens when the user leaves the Control screen (is there a back gesture, and to where)?
Answer:

### Q138
Block: B31 — Control page
Question: What becomes of the Control screen's displayed content after the user leaves it — kept, recomputed, or deleted?
Answer:

### Q139
Block: B31 — Control page
Question: Can the Control screen be reopened after being left, and does it resume its earlier state or start clean?
Answer:

### Q140
Block: B31 — Control page
Question: What does the Control screen show with no data, while loading, or on failure?
Answer:

### Q141
Block: B31 — Control page
Question: What becomes of the Control screen's state when the system rebuilds it — what is preserved and what is rebuilt from source?
Answer:


### Q142
Block: B32 — Undoing the last marking
Question: When determining "the last marking" to undo, what breaks a tie between two markings that would otherwise be equally last?
Answer:

### Q143
Block: B32 — Undoing the last marking
Question: What happens to the undone marking's data — is it deleted, kept but hidden, or recomputed?
Answer:

### Q144
Block: B32 — Undoing the last marking
Question: After undoing the very last remaining marking (leaving zero markings), does the undo button return to its disabled state?
Answer:


### Q145
Block: B33 — Stopping the race
Question: What happens when the user taps "Annuler" in the stop confirmation dialog — does the dialog simply close with the race continuing unaffected, or something else?
Answer:

### Q146
Block: B33 — Stopping the race
Question: Can "Arrêter l'activité" be triggered again for a subsequent race once a previous race has already been stopped and saved as incomplete, or does some state need resetting first?
Answer:

### Q147
Block: B33 — Stopping the race
Question: In the transition's state model, what state is reached if the user cancels the confirmation (taps "Annuler") instead of confirming — is it the same "running" state as before, or something else?
Answer:


### Q148
Block: B34 — End-of-race screen
Question: What is the exact wording of the message shown when a race is stopped before its 30th segment (the block only says "the screen states that the race is incomplete")?
Answer:

### Q149
Block: B34 — End-of-race screen
Question: What does this screen show while its data (total time, delta, date/time) is loading, and if that fails?
Answer:

### Q150
Block: B34 — End-of-race screen
Question: When the system rebuilds this screen, is it rebuilt entirely from the saved race data, or is there any in-progress state on it to preserve?
Answer:


### Q151
Block: B35 — Always-on display during the race
Question: Which screen does this always-on/power-save behaviour draw on, and what area of it does the dimming occupy?
Answer:

### Q152
Block: B35 — Always-on display during the race
Question: What happens to the always-on/power-save behaviour when the race ends?
Answer:

### Q153
Block: B35 — Always-on display during the race
Question: What becomes of the dimmed display state once the race ends — kept, reset, or cleared?
Answer:

### Q154
Block: B35 — Always-on display during the race
Question: Within that screen, is the whole screen dimmed in power-save, or only a named area — and which area?
Answer:

### Q155
Block: B35 — Always-on display during the race
Question: What does this display show with no data, while loading, or on failure?
Answer:

### Q156
Block: B35 — Always-on display during the race
Question: When the system rebuilds this screen, what is kept from what the user has in progress, and what is rebuilt from source?
Answer:

### Q157
Block: B35 — Always-on display during the race
Question: What are the active-state (full-refresh) values for the arc and the text that the power-save arc ("thinner", "more transparent") and text ("muted") are being compared against?
Answer:


### Q158
Block: B36 — allure-segment and allure-lissee
Question: What happens to allure-segment and allure-lissee when the current segment stops being a RUN segment (ends or changes type) — does the displayed value freeze, get hidden, reset, or something else?
Answer:

### Q159
Block: B36 — allure-segment and allure-lissee
Question: Once a segment ends, is the last computed allure-segment/allure-lissee value kept, recomputed, or deleted?
Answer:

### Q160
Block: B36 — allure-segment and allure-lissee
Question: Below the fallback thresholds (under 50 m covered for allure-segment, under 3 seconds of data for allure-lissee), what value or state is shown or used instead of the normal computation?
Answer:

### Q161
Block: B36 — allure-segment and allure-lissee
Question: If the Health Services distance or speed data is missing or unavailable, what does allure-segment/allure-lissee do?
Answer:

### Q162
Block: B36 — allure-segment and allure-lissee
Question: What is the acceptable range of the computed pace output (e.g. behaviour at zero speed / division by zero, minimum and maximum values)?
Answer:


### Q163
Block: B37 — Computing the correction factor
Question: What is the value or source of distance_attendue (the expected distance used to compute k_mesuré) — is it always the nominal distance of one kilometre, or does it vary by course or kilometre marker?
Answer:


### Q164
Block: B38 — Starting factor and fallback
Question: Which screen and area display the pace and the "factor of 1 is never flagged" behaviour described in this block?
Answer:

### Q165
Block: B38 — Starting factor and fallback
Question: When several factors are computed during the same race, what determines which one becomes "the last factor retained" if they would otherwise tie?
Answer:

### Q166
Block: B38 — Starting factor and fallback
Question: If the structure holding the profile's starting factor changes, what happens to the previously stored value?
Answer:

### Q167
Block: B38 — Starting factor and fallback
Question: Where are "imported race", "watch-recorded race" and the "screen" showing pace defined?
Answer:


### Q168
Block: B59 — Measured and displayed physiological data
Question: Are pace and heart rate each mandatory to display, or optional (e.g. when no heart-rate sensor is available)?
Answer:

### Q169
Block: B59 — Measured and displayed physiological data
Question: Which screen or mechanism consults this scope rule on displayed physiological measures?
Answer:

### Q170
Block: B59 — Measured and displayed physiological data
Question: Can the list of allowed/excluded physiological measures change after delivery (e.g. adding calorie tracking later)?
Answer:


### Q171
Block: B39 — Lap delta
Question: Where, and on which screen/area, is the lap delta (écart) shown to the user, if at all?
Answer:

### Q172
Block: B39 — Lap delta
Question: What happens to the lap delta calculation and its displayed value when the segment stops being a RUN segment?
Answer:

### Q173
Block: B39 — Lap delta
Question: When the RUN segment ends, is the last produced écart kept, recomputed, or deleted?
Answer:

### Q174
Block: B39 — Lap delta
Question: On the next RUN segment, does the lap delta calculation start clean or resume from an earlier state?
Answer:

### Q175
Block: B39 — Lap delta
Question: What does the calculation do if allure-segment or temps_référence_du_segment is missing or unavailable?
Answer:

### Q176
Block: B39 — Lap delta
Question: What is the acceptable range of values for écart (sign, minimum, maximum), beyond the floor stated on temps_projeté?
Answer:


### Q177
Block: B40 — Cumulative delta and estimated arrival
Question: What happens to écart_cumulé and arrivée once there is no more marking and no current segment (course finished) — are they kept, frozen, or cleared?
Answer:

### Q178
Block: B40 — Cumulative delta and estimated arrival
Question: When the current segment's real time exactly equals its reference time, does it count as "exceeded" (use real time) or "not yet exceeded" (use reference time)?
Answer:

### Q179
Block: B40 — Cumulative delta and estimated arrival
Question: What happens to the calculation if the real time or the reference time of a segment is missing?
Answer:

### Q180
Block: B40 — Cumulative delta and estimated arrival
Question: What are the acceptable bounds or range of values for écart_cumulé and for arrivée?
Answer:

### Q181
Block: B40 — Cumulative delta and estimated arrival
Question: Where are "temps réel", "temps de référence", "segment (clos / en cours / à venir)", "temps écoulé" and "pointage" defined?
Answer:

### Q182
Block: B40 — Cumulative delta and estimated arrival
Question: Which described block (or "existing" status) do "temps réel", "temps de référence", the segment states, "temps écoulé" and "pointage" point to?
Answer:


### Q183
Block: B41 — Trend arrow
Question: What event or condition triggers (re-)evaluation of the trend arrow — e.g., every time allure-lissee or allure-segment updates, or on screen render?
Answer:

### Q184
Block: B41 — Trend arrow
Question: On which screen, and in which area of that screen, does the trend arrow appear?
Answer:

### Q185
Block: B41 — Trend arrow
Question: The 2% difference threshold between allure-lissee and allure-segment — relative to which value is this percentage computed (allure-lissee, allure-segment, or their average)?
Answer:

### Q186
Block: B41 — Trend arrow
Question: When allure-lissee is slower than allure-segment by more than 2%, what does the arrow show (a downward arrow, or something else)?
Answer:


### Q187
Block: B42 — Zone switching hysteresis
Question: Does the ±3bpm hysteresis apply simultaneously to both boundaries adjacent to the active zone (the one above and the one below), or to only one boundary at a time?
Answer:


### Q188
Block: B43 — Sending profile and reference to the watch
Question: Among races that could fall right at the 20-most-recent cutoff, what breaks a tie (e.g. same date)?
Answer:

### Q189
Block: B43 — Sending profile and reference to the watch
Question: What happens if the link between the two devices is lost while a push is in progress — does a partial state land on the watch, or is the push atomic?
Answer:

### Q190
Block: B43 — Sending profile and reference to the watch
Question: What does the user see on the phone and on the watch while a push is in progress (before success or failure is known)?
Answer:

### Q191
Block: B43 — Sending profile and reference to the watch
Question: What identifies one same race as seen from the phone and from the watch, so that a deletion on the phone is recognized as the same race on the watch?
Answer:

### Q192
Block: B43 — Sending profile and reference to the watch
Question: Which blocks describe the profile, the reference race, the summarized history, the link between the two devices, and the button that forces the push?
Answer:


### Q193
Block: B44 — Receiving recorded races from the watch
Question: On which screen and area does a received race appear to the user on the phone?
Answer:

### Q194
Block: B44 — Receiving recorded races from the watch
Question: What does the user see on the phone while a race transfer is in progress, and what is shown if it fails?
Answer:

### Q195
Block: B44 — Receiving recorded races from the watch
Question: What identifies one same race as seen from both the watch and the phone, and what closed list of changes to the reference and history triggers an update of the watch's mirrored copy?
Answer:

### Q196
Block: B44 — Receiving recorded races from the watch
Question: What is the size or content of a transfer chunk, and what criterion defines a transfer attempt as failed?
Answer:

### Q197
Block: B44 — Receiving recorded races from the watch
Question: What do the reference and history become on the watch once they are transmitted to it?
Answer:


### Q198
Block: B61 — Connectivity permission denied
Question: On which watch screen, and in which area, does "Aucune référence" appear?
Answer:

### Q199
Block: B61 — Connectivity permission denied
Question: When the connectivity permission becomes granted again, what happens to the message and to the "Autoriser" action on the profile screen?
Answer:

### Q200
Block: B61 — Connectivity permission denied
Question: When the connectivity permission becomes granted again, does the "Synchroniser avec la montre" button become active again, and does the watch stop showing "Aucune référence"?
Answer:


### Q201
Block: B45 — Exercise session lifecycle
Question: Which screen displays the running race clock and the "not interactive" state during the race, and what area does it occupy?
Answer:

### Q202
Block: B45 — Exercise session lifecycle
Question: After the exercise session closes, is the completed session record kept, recomputed, or deleted?
Answer:

### Q203
Block: B45 — Exercise session lifecycle
Question: When a new exercise session starts after a previous one has closed, does it begin clean or resume from an earlier state?
Answer:

### Q204
Block: B45 — Exercise session lifecycle
Question: How long does a completed exercise session's data live, and what becomes of it after that period?
Answer:

### Q205
Block: B45 — Exercise session lifecycle
Question: Which screen is referred to as "not interactive" during the race — is it the preparation screen or a distinct race-tracking screen?
Answer:


### Q206
Block: B60 — Heart-rate data consent
Question: Who or what consults this consent convention (i.e., what mechanism checks B20/B17 before collection is triggered)?
Answer:

### Q207
Block: B60 — Heart-rate data consent
Question: What happens when the OS-level sensor permission (B20) or health-history permission (B17) is not granted — is heart-rate collection simply skipped, and is this stated anywhere?
Answer:

### Q208
Block: B60 — Heart-rate data consent
Question: Can this no-consent-step convention change after delivery (e.g., a future export feature), and if so, what happens to data already collected under the old policy?
Answer:


### Q209
Block: B46 — Monotonic timing and recovery
Question: What happens to the race clock and its segments when the race ends (the last segment closes) — does timing stop, is a final duration recorded, anything else?
Answer:

### Q210
Block: B46 — Monotonic timing and recovery
Question: If the stored structure for segments changes later, what happens to existing recorded segment durations and opening instants?
Answer:


### Q211
Block: B47 — Duration formats
Question: On which screen and in which area is each duration format (duration-segment, duration-total, duration-elapsed) displayed?
Answer:

### Q212
Block: B47 — Duration formats
Question: What does the text show when the duration value to format is absent?
Answer:

### Q213
Block: B47 — Duration formats
Question: What consults or uses these three duration formats — which screens or elements are the "list columns" mentioned for duration-total?
Answer:

### Q214
Block: B47 — Duration formats
Question: What happens when a duration to format does not match any of the three named types (duration-segment, duration-total, duration-elapsed)?
Answer:

### Q215
Block: B47 — Duration formats
Question: Can these duration formats change after delivery, and if so, is anything already displayed with the old format recomputed?
Answer:

### Q216
Block: B47 — Duration formats
Question: What are the "list columns" that duration-total's format is meant to keep aligned?
Answer:


### Q217
Block: B48 — Delta format
Question: What is displayed for the delta when its value is absent or unavailable?
Answer:

### Q218
Block: B48 — Delta format
Question: Which screens or blocks consult this delta formatting convention?
Answer:

### Q219
Block: B48 — Delta format
Question: Is the absence of a delta to format a default case, an error, or impossible by construction?
Answer:

### Q220
Block: B48 — Delta format
Question: Can this delta formatting convention change after delivery, and if so, is anything already displayed recomputed?
Answer:

### Q221
Block: B48 — Delta format
Question: What is "delta" exactly — what does it represent and where is it computed?
Answer:

### Q222
Block: B48 — Delta format
Question: What are the exact colors for the three cases — ahead, behind, and delta-zero?
Answer:


### Q223
Block: B49 — Pace, heart rate, position and zone formats
Question: On which screen(s) and in which area(s) are the pace, heart rate, position and zone values displayed using these formats?
Answer:

### Q224
Block: B49 — Pace, heart rate, position and zone formats
Question: What does the pace, heart rate, position or zone display show when the underlying value is absent (e.g. no data yet)?
Answer:

### Q225
Block: B49 — Pace, heart rate, position and zone formats
Question: Which screens or components consult these pace/hr/position/zone format rules?
Answer:

### Q226
Block: B49 — Pace, heart rate, position and zone formats
Question: Are pace, heart rate, position and zone the only metric types these format rules apply to, or can another metric type require formatting not covered here?
Answer:

### Q227
Block: B49 — Pace, heart rate, position and zone formats
Question: Can these format conventions change after delivery, and if so, what happens to values already displayed under the old format?
Answer:

### Q228
Block: B49 — Pace, heart rate, position and zone formats
Question: Where are the pace, heart rate, position and zone values themselves defined (which block computes or provides them), and where is the "text-secondary" style token defined?
Answer:


### Q229
Block: B50 — Settings and range formats
Question: On which screen(s) and in which area(s) is text formatted this way displayed?
Answer:

### Q230
Block: B50 — Settings and range formats
Question: What does the formatted text become when the underlying value is absent?
Answer:

### Q231
Block: B50 — Settings and range formats
Question: Who or what consults these formats?
Answer:

### Q232
Block: B50 — Settings and range formats
Question: What happens if a value to format is missing or invalid (e.g. non-integer, negative)?
Answer:

### Q233
Block: B50 — Settings and range formats
Question: Can these formats change after delivery, and if so is anything already displayed recomputed?
Answer:


### Q234
Block: B51 — Date formats
Question: On which screen(s) and in which area(s) are these formatted dates displayed?
Answer:

### Q235
Block: B51 — Date formats
Question: What is shown when there is no date value to format (e.g., before a race has a date, or before any sync has happened)?
Answer:

### Q236
Block: B51 — Date formats
Question: Which screens or elements consult these date formats?
Answer:

### Q237
Block: B51 — Date formats
Question: What is shown if the date to format is invalid or does not match any of the three described cases?
Answer:

### Q238
Block: B51 — Date formats
Question: Can these date formats change after delivery (e.g., a different language or abbreviation)?
Answer:


### Q239
Block: B52 — Rounding rule
Question: What event or moment triggers this truncation/computation (e.g. rendering a screen, a timer tick, session completion)?
Answer:

### Q240
Block: B52 — Rounding rule
Question: On which screen and area is the truncated duration displayed?
Answer:

### Q241
Block: B52 — Rounding rule
Question: When the (unnamed) trigger stops being true, does the displayed truncated value revert, persist, or persist until something clears it?
Answer:

### Q242
Block: B52 — Rounding rule
Question: Can this rounding/truncation computation be set off again after it has run once, and from what state?
Answer:

### Q243
Block: B52 — Rounding rule
Question: What happens when a value this computation needs is missing (e.g. no prior cumulative total exists for the first segment)?
Answer:

### Q244
Block: B52 — Rounding rule
Question: What values can the truncated output take, and which are acceptable (e.g. can a segment show 0 seconds, can it ever be negative)?
Answer:

### Q245
Block: B52 — Rounding rule
Question: Does "a delta is computed on millisecond values, then truncated only at display" describe the same segment computation already stated (difference of two truncated totals), or a different computation — and if different, what is it for?
Answer:


### Q246
Block: B53 — Text resource rules
Question: This block states a rule that applies to all text resources but names no specific label of its own — is a label expected to be attached to this block, or does it purely set a global rule with no label?
Answer:

### Q247
Block: B53 — Text resource rules
Question: For the rule this block sets, what does a text resource become if its underlying value is absent?
Answer:

### Q248
Block: B53 — Text resource rules
Question: What happens when a resource key expected to exist is missing at runtime — a default, an error, or is this impossible by construction?
Answer:

### Q249
Block: B53 — Text resource rules
Question: Can the resource files change after the app is delivered (e.g. through an update), and if so, is anything already computed with the old values recomputed?
Answer:


### Q250
Block: B54 — Dynamic texts and fallbacks
Question: On which screen and in which area does each of these dynamic texts appear (reference badge, sync status line, delete confirmation, zone row, cancel-segment control)?
Answer:

### Q251
Block: B54 — Dynamic texts and fallbacks
Question: Which block defines "the reference" whose name is shown in "Réf. — <nom>", and which block defines the closed segment named in "Annuler : <segment fermé>"?
Answer:

### Q252
Block: B54 — Dynamic texts and fallbacks
Question: What is the width or character limit of "its slot" against which a race name is judged "too long" before being truncated?
Answer:


### Q253
Block: B55 — Relative date wording
Question: What piece of data (timestamp) does this wording apply to, and where does it come from?
Answer:

### Q254
Block: B55 — Relative date wording
Question: On which screen(s) and area(s) is this relative date wording displayed?
Answer:

### Q255
Block: B55 — Relative date wording
Question: Is the displayed relative-date text recomputed every time it is shown, or kept as-is once generated?
Answer:

### Q256
Block: B55 — Relative date wording
Question: What is displayed when no date/time value is available to format?
Answer:

### Q257
Block: B55 — Relative date wording
Question: Which screen(s) or feature(s) consult/use this relative date wording?
Answer:

### Q258
Block: B55 — Relative date wording
Question: What is displayed for a future date (later than today), a case not covered by the three stated rules?
Answer:

### Q259
Block: B55 — Relative date wording
Question: Can these wording rules change after delivery?
Answer:


### Q260
Block: B56 — Fixed text catalogue
Question: What happens if a text from this catalogue is missing at runtime (default value, error, or is this impossible by construction)?
Answer:

### Q261
Block: B56 — Fixed text catalogue
Question: Can these fixed texts change after delivery (e.g. wording update, localisation), and if so, is anything computed from them recomputed?
Answer:


### Q262
Block: B57 — Phone navigation map
Question: When returning to the paste screen via "Corriger" or "Revenir au collage", does it show the previously entered content or does it start clean?
Answer:

### Q263
Block: B57 — Phone navigation map
Question: From the race detail screen, where do "set as reference", "rename", and "delete" lead — do they stay on the detail screen, or does one of them (e.g. delete) navigate back to the list?
Answer:

### Q264
Block: B57 — Phone navigation map
Question: What is the exact wording of the delete confirmation, or is it a reused confirmation pattern defined elsewhere?
Answer:


### Q265
Block: B58 — Watch navigation map
Question: What happens to the navigation state (current screen) when the watch app is closed or sent to the background?
Answer:

### Q266
Block: B58 — Watch navigation map
Question: What happens to the user's progress in the journey (current page/segment) after the app is closed — is it kept, reset, or does the app return to the last screen shown?
Answer:

### Q267
Block: B58 — Watch navigation map
Question: If the user denies the permission request at first launch, what happens next — a retry, a blocked state, or does the journey proceed anyway?
Answer:

### Q268
Block: B58 — Watch navigation map
Question: Does the 8-second inactivity rule on a "secondary page" apply to Control (which is otherwise excluded from the long-press rule)? What exactly defines a "profile" in "no profile has ever been received"? And is the "system gesture" used to leave Historique the same gesture as the "back gesture" described elsewhere in this block?
Answer:


### Q269
Block: B14 — Saving an imported race / B46 — Monotonic timing and recovery
Question: Which block stores a race's date, since B14 stores only the name and 30 segment durations, B46 does not list a date among what it writes, yet B6, B7, B23 and B51 all consume a race's date?
Answer:

### Q270
Block: B18 — Zone ranges from maximum heart rate
Question: Does the active zone-arc segment shown on screen come from B18's direct zone lookup or from B42's hysteresis-adjusted zone, given both blocks describe producing it?
Answer:

### Q271
Block: B17 — Deriving maximum heart rate / B19 — Editing profile settings
Question: When the user manually enters a maximum heart rate through B17's field, does that entry go through B19's validation (100-230 bpm bounds), or is B17's manual-entry write a separate, unvalidated path?
Answer:

### Q272
Block: B37 — Computing the correction factor
Question: What block reads or displays the rejection record (k_mesuré outside [0.70, 1.40]) that B37 stores with the race but never shows?
Answer:

### Q273
Block: B28 — Main page, adapting to the current segment / B30 — Projection page
Question: Do the main page (B28) and the Projection page (B30) apply B29's data-freshness fallback (dash or hidden block after 10 seconds without a sensor reading) to the sensor values they display, since neither lists B29 among what it reads?
Answer:

### Q274
Block: B28 — Main page, adapting to the current segment
Question: Does the main page (B28) apply B35's power-save dimmed display state, since B28 does not list B35 among what it reads?
Answer:

### Q275
Block: B26 — Resuming our own already-active race
Question: At what moment does B26 write the arbitration outcome that B45 reads at session start, since B26's "Writes at" is empty?
Answer:

### Q276
Block: B6 — Race list screen
Question: Does the race list card include the reference-setting button that B8 shows or hides on it, since B6's card composition (name, date, total time, badges) does not mention a button?
Answer:

### Q277
Block: B20 — Sensor permission request / B22 — Home screen
Question: Where on the home screen does B20's permission reminder sit, since B22's full layout (reference line, "Démarrer" button, "Historique" and "Synchroniser" pills) does not name a reminder zone?
Answer:

### Q278
Block: -
Question: Does this feature build on an existing app or an existing set of product rules, and if so, for each rule it touches, is it kept, changed, or removed?
Answer:
