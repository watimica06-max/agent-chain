## Questions

### Q1
Block: B1 — Race segment structure
Question: What is the exact displayed name of each of the 30 segments, one by one?
Answer:

### Q2
Block: B6 — Race list screen
Question: What does the race list show while the races are being loaded, and what does it show if they cannot be read?
Answer:

### Q3
Block: B6 — Race list screen
Question: When the user returns to the list from a race detail, is the scroll position kept or reset to the top?
Answer:

### Q4
Block: B6 — Race list screen
Question: What is the constrained width of the empty state's explanation text?
Answer:

### Q5
Block: B7 — Race detail screen
Question: What does the race detail show while it is loading, and what does it show if the race cannot be read?
Answer:

### Q6
Block: B7 — Race detail screen
Question: How is each row's delta computed against the reference race, and what fixed width do the duration, cumulative and delta columns take?
Answer:

### Q7
Block: B9 — Renaming a race
Question: Is the rename field a dialog over the detail screen or a screen of its own?
Answer:

### Q8
Block: B11 — Paste-a-result screen
Question: What does the paste screen show between the tap on "Importer" and the preview or error screen?
Answer:

### Q9
Block: B11 — Paste-a-result screen
Question: Is the pasted text kept when the user leaves the paste screen entirely and comes back to it later?
Answer:

### Q10
Block: B12 — Reading and validating a pasted result
Question: What makes two pasted results the same race, and what happens when a result already imported is pasted again?
Answer:

### Q11
Block: B12 — Reading and validating a pasted result
Question: What are hyresult's four columns, in order, and which of them carries a segment's own duration?
Answer:

### Q12
Block: B14 — Saving an imported race
Question: Does the saved record store the race's date, and is it the start time computed by B12 or the day of the import?
Answer:

### Q13
Block: B15 — Paste error screen
Question: For each of the eight causes, what expected form is shown in ahead beside the row as read?
Answer:

### Q14
Block: B16 — Profile screen
Question: What happens to an inline field being edited when the user leaves the profile screen without it losing focus first?
Answer:

### Q15
Block: B17 — Deriving maximum heart rate
Question: When no maximum heart rate was ever obtained or entered, is the health history read again at a later opening of the profile?
Answer:

### Q16
Block: B18 — Zone ranges from maximum heart rate
Question: How is a fractional threshold turned into a whole bpm value — truncation, rounding, or ceiling?
Answer:

### Q17
Block: B19 — Editing profile settings
Question: What are the default values of the expected kilometre distance and of the maximum heart rate before anything is entered?
Answer:

### Q18
Block: B20 — Sensor permission request
Question: Where on the watch's home screen does the refused-permission reminder sit, and does it push the other blocks down?
Answer:

### Q19
Block: B21 — Waiting for the phone
Question: What does the "Réessayer" button on the waiting screen do?
Answer:

### Q20
Block: B23 — Watch history screen
Question: In what order are the watch history's rows shown, and what separates two races of the same date?
Answer:

### Q21
Block: B23 — Watch history screen
Question: What does the watch history show when no race has been received yet, and is it distinguished from the phone having no race at all?
Answer:

### Q22
Block: B25 — Starting when another app holds the sensor
Question: What happens when stopping the other app's activity fails after the user has confirmed?
Answer:

### Q23
Block: B26 — Resuming our own already-active race
Question: Which screen does a resumed race open on — the main race page directly, or the preparation screen?
Answer:

### Q24
Block: B30 — Projection page
Question: What does the Projection page show without a reference loaded, its cumulative delta and estimated arrival both being reference-derived?
Answer:

### Q25
Block: B32 — Undoing the last marking
Question: Does a reopened segment resume from its original opening instant, keeping the time already elapsed, or start a fresh one?
Answer:

### Q26
Block: B32 — Undoing the last marking
Question: What state does the undo button take right after an undo?
Answer:

### Q27
Block: B35 — Always-on display during the race
Question: What returns the display to power-save mode after a wrist raise or a screen touch, and after how long?
Answer:

### Q28
Block: B36 — allure-segment and allure-lissee
Question: What are the acceptable bounds of a computed pace, and what is displayed when the measured distance yields a value outside them?
Answer:

### Q29
Block: B37 — Computing the correction factor
Question: What bounds does the retained factor k itself carry, once blended and stored?
Answer:

### Q30
Block: B39 — Lap delta
Question: What does the lap delta show while allure-segment is in fallback, and when the reference holds no time for that segment?
Answer:

### Q31
Block: B40 — Cumulative delta and estimated arrival
Question: How is the current segment's own delta computed inside écart_cumulé when that segment is a station or a Roxzone?
Answer:

### Q32
Block: B40 — Cumulative delta and estimated arrival
Question: Is the estimated arrival a projected total duration or a time of day, and what does it show when the projection becomes absurd?
Answer:

### Q33
Block: B43 — Sending profile and reference to the watch
Question: What identifies one same race on the phone and on the watch, and which changes to it does the watch's copy follow?
Answer:

### Q34
Block: B44 — Receiving recorded races from the watch
Question: What identifies a race transferred from the watch, so that a confirmation lost after storage does not make the same race arrive twice?
Answer:

### Q35
Block: B45 — Exercise session lifecycle
Question: What does the watch-face complication display, and what does it show outside a race?
Answer:

### Q36
Block: B47 — Duration formats
Question: What does duration-segment show for a segment that does pass 60 minutes?
Answer:

### Q37
Block: B51 — Date formats
Question: Does a date's time read "09:14" or "9:14" — the worked form carries a leading zero that "h:mm" and B47's rule both deny?
Answer:

### Q38
Block: B61 — Connectivity permission denied
Question: On which device is the connectivity permission asked, and what does the watch show about it beyond "Aucune référence"?
Answer:

### Q39
Block: B6 — Race list screen
Question: Where does the insertion rank the list sorts on come from — a creation instant stored with each race, or something else?
Answer:

### Q40
Block: B43 — Sending profile and reference to the watch
Question: Does a successful pull from the watch update the same last-sync date as a push, and does that date read "hier" as B55 rules or only "aujourd'hui" as B51 rules?
Answer:

### Q41
Block: B37 — Computing the correction factor
Question: What reads the kilometre number stored with each retained factor?
Answer:

### Q42
Block: B38 — Starting factor and fallback
Question: How does a factor calibrated by a watch-recorded race reach the phone's profile, given that only races travel up and the next push fully replaces the watch's state?
Answer:

### Q43
Block: B21 — Waiting for the phone
Question: Before any profile has been received, does the watch show the waiting screen or the home screen with "Aucune référence"?
Answer:

### Q44
Block: B56 — Fixed text catalogue
Question: Which wording is the right one — "approche le téléphone de la montre." or "approche la montre du téléphone.", and "Reprise d'activité en cours" or "Une autre activité est en cours"?
Answer:

### Q45
Block: -
Question: Are backing up the races, exporting them, or moving them to a new phone in scope or out?
Answer:

### Q46
Block: -
Question: Does the app store any identifier — a device identifier for the pairing, an account, a user identity?
Answer:

### Q47
Block: -
Question: Does reading Health Services' distance and speed need a permission of its own, and what becomes of a race if it is permanently denied?
Answer:
