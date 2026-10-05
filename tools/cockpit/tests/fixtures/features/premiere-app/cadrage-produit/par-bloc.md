### Q1
Block: B1 — Race segment structure
Question: What is the exact name of each of the 30 segments, one by one, as stored and as displayed — including the two Roxzone segments of a cycle and the eight run segments?
Answer:

### Q2
Block: B2 — Color tokens
Question: Which token colors a control that is displayed but inactive (the disabled "Importer" button, the disabled undo button, the inactive "Synchroniser avec la montre" button)?
Answer:

### Q3
Block: B2 — Color tokens
Question: Does the app follow the system's light/dark setting, or does it always render this single dark palette whatever the system is set to?
Answer:

### Q4
Block: B3 — Typography tokens
Question: Are IBM Plex Sans and IBM Plex Mono shipped inside the apps, or taken from the device when present?
Answer:

### Q5
Block: B3 — Typography tokens
Question: What line height applies to each type size, on the phone and on the watch?
Answer:

### Q6
Block: B3 — Typography tokens
Question: Do the phone's dp sizes and the watch's px sizes follow the system's font-size accessibility setting, or stay fixed at the declared values?
Answer:

### Q7
Block: B4 — Shape, spacing and zone-arc tokens
Question: What happens on a Wear OS watch whose screen is not 480×480 — is the app refused, or are the w-* and arc values scaled, and by what rule?
Answer:

### Q8
Block: B4 — Shape, spacing and zone-arc tokens
Question: What is the phone's target — minimum Android version, and the screen sizes the dp scale is designed for?
Answer:

### Q9
Block: B5 — Idle display token variants
Question: Do the badge backgrounds ahead-bg and behind-bg take the 0.55 opacity in idle mode, or do only the foreground meaning colors dim?
Answer:

### Q10
Block: B5 — Idle display token variants
Question: What becomes of the 9px actionable dot (rgba(255,255,255,0.35)) in idle mode — unchanged, dimmed, or hidden?
Answer:

### Q11
Block: B6 — Race list screen
Question: What color is the "tinted background" behind the Reference badge?
Answer:

### Q12
Block: B6 — Race list screen
Question: What does the screen show between opening and the races being available to display?
Answer:

### Q13
Block: B6 — Race list screen
Question: What is the exact diameter of the header's profile and + circles, "36–38dp" giving two values?
Answer:

### Q14
Block: B7 — Race detail screen
Question: Is a row's delta the difference between the two segments' durations, or the difference between the two cumulative times at that segment?
Answer:

### Q15
Block: B7 — Race detail screen
Question: Under which group headers do segments 29 and 30 fall, the first seven cycles holding four segments each?
Answer:

### Q16
Block: B7 — Race detail screen
Question: Is the header's reference badge shown only when the race being viewed is the current reference, or on every race's detail screen?
Answer:

### Q17
Block: B8 — Setting a race as the reference
Question: What does the detail screen show immediately after "Définir comme référence" is tapped — the button disappearing in place, the badge appearing, a confirmation message, or a return to the list?
Answer:

### Q18
Block: B9 — Renaming a race
Question: What does the user see when the field's trimmed content is empty and "Enregistrer" is tapped — a disabled button, a message, or a silent refusal?
Answer:

### Q19
Block: B11 — Paste-a-result screen
Question: Is a name made only of spaces treated as empty for the purpose of enabling the "Importer" button?
Answer:

### Q20
Block: B11 — Paste-a-result screen
Question: Are the pasted text and the entered name kept when the user leaves this screen other than through "Importer" — system back, or the app backgrounded — and comes back?
Answer:

### Q21
Block: B12 — Reading and validating a pasted result
Question: What are the four columns, in the order they are expected, and which position holds the label, the Time of Day, the Diff and the Time?
Answer:

### Q22
Block: B12 — Reading and validating a pasted result
Question: Which source rows produce the two Roxzone segments of each cycle, given that "Rox In" identifies the kilometre row and the station name follows it — the full row-to-segment mapping for the 30 rows?
Answer:

### Q23
Block: B12 — Reading and validating a pasted result
Question: How are blank lines in the pasted text treated — a trailing newline, or an empty line between rows?
Answer:

### Q24
Block: B13 — Preview before saving
Question: What exact form does the "Segments détectés" value take — "30", "30/30", or another?
Answer:

### Q25
Block: B14 — Saving an imported race
Question: What date does an imported race carry on its list card and detail header, and does the start time computed in the reading get stored for that purpose?
Answer:

### Q26
Block: B15 — Paste error screen
Question: In which order are the eight causes tested, so that "the first anomaly found" is determined between a per-row cause and a whole-table cause such as the segment count?
Answer:

### Q27
Block: B15 — Paste error screen
Question: What does the surface-raised row panel show for the causes that name no row — empty paste, fewer than 30 segments, more than 30 segments?
Answer:

### Q28
Block: B16 — Profile screen
Question: What is the exact label of each of the five zone rows?
Answer:

### Q29
Block: B16 — Profile screen
Question: What does the maximum-heart-rate entry dialog contain — its title, its field label, its buttons?
Answer:

### Q30
Block: B16 — Profile screen
Question: What becomes of an inline numeric field being edited when the user leaves the profile screen before the field loses focus — validated, or discarded?
Answer:

### Q31
Block: B17 — Deriving maximum heart rate
Question: Which health source is read on the phone for the twelve-month maximum?
Answer:

### Q32
Block: B17 — Deriving maximum heart rate
Question: When is the automatic reading attempted again after a first opening that found nothing, the value being said never to overwrite a hand-entered one by "a later automatic reading"?
Answer:

### Q33
Block: B17 — Deriving maximum heart rate
Question: Is the proposed value written to the profile as soon as it is read, or only once the user validates it?
Answer:

### Q34
Block: B17 — Deriving maximum heart rate
Question: At what moment is the health-history permission requested on the phone, and with what wording?
Answer:

### Q35
Block: B18 — Zone ranges from maximum heart rate
Question: How is a percentage of the maximum heart rate converted to an integer bpm threshold — rounded to the nearest, or truncated?
Answer:

### Q36
Block: B19 — Editing profile settings
Question: What is the exact wording of the short message shown for each rejection — out of bounds, non-integer, and thresholds not strictly increasing?
Answer:

### Q37
Block: B21 — Waiting for the phone
Question: What does the retry button do?
Answer:

### Q38
Block: B23 — Watch history screen
Question: In what order are the races listed, and what separates two races sharing the same date?
Answer:

### Q39
Block: B25 — Starting when another app holds the sensor
Question: What happens if the other activity cannot be stopped after the user taps "Continuer"?
Answer:

### Q40
Block: B26 — Resuming our own already-active race
Question: Which screen does the app open on relaunch when a race is resumed — the main race page directly, or the home screen?
Answer:

### Q41
Block: B27 — Marking a segment
Question: Is anything shown on screen while the finger is held down before the threshold is reached?
Answer:

### Q42
Block: B28 — Main page, adapting to the current segment
Question: Where does the station name sit during a station, the page holding three blocks — top, center, bottom — of which top is the reference time and center the elapsed time?
Answer:

### Q43
Block: B28 — Main page, adapting to the current segment
Question: What does the center show during a kilometre while allure-segment is in fallback, under 50 meters covered?
Answer:

### Q44
Block: B29 — Data freshness on the race pages
Question: For each value that can be absent — heart rate, zone number, pace, trend arrow, lap delta, cumulative delta, estimated arrival, reference time — which shows a dash and which hides its block?
Answer:

### Q45
Block: B30 — Projection page
Question: Is the estimated arrival a total race duration or a time of day, and in which of the declared formats is it written?
Answer:

### Q46
Block: B32 — Undoing the last marking
Question: What becomes of the time already elapsed in the segment that the undone marking had opened, and from which instant does the reopened segment's clock continue?
Answer:

### Q47
Block: B33 — Stopping the race
Question: What is saved when the race is stopped before any segment has been marked?
Answer:

### Q48
Block: B34 — End-of-race screen
Question: Does the automatic name carry the date and time of the race's start or of its end?
Answer:

### Q49
Block: B35 — Always-on display during the race
Question: Which screens keep the always-on display — the main page only, or Projection, Control and the end-of-race screen as well?
Answer:

### Q50
Block: B36 — allure-segment and allure-lissee
Question: Between which two values is a computed pace acceptable, and what is displayed when it falls outside them?
Answer:

### Q51
Block: B37 — Computing the correction factor
Question: What does the record of a rejection hold — the kilometre number, the rejected k_mesuré, the measured distance?
Answer:

### Q52
Block: B38 — Starting factor and fallback
Question: Does a race stopped early update the profile's stored factor with the last factor it retained?
Answer:

### Q53
Block: B39 — Lap delta
Question: What does the lap delta show while allure-segment is in fallback?
Answer:

### Q54
Block: B40 — Cumulative delta and estimated arrival
Question: What is "the current segment's own delta" when the current segment is a station or a Roxzone, no delta being computed there?
Answer:

### Q55
Block: B41 — Trend arrow
Question: The 2% difference is measured relative to which of the two paces?
Answer:

### Q56
Block: B42 — Zone switching hysteresis
Question: Is the zone computed on each raw heart-rate reading as it arrives, or on a smoothed value?
Answer:

### Q57
Block: B43 — Sending profile and reference to the watch
Question: What does the push carry in place of the reference race when no race is designated as reference on the phone?
Answer:

### Q58
Block: B43 — Sending profile and reference to the watch
Question: What identifies one same race on the phone and on the watch?
Answer:

### Q59
Block: B44 — Receiving recorded races from the watch
Question: What does a transferred race carry besides its segment durations — heart-rate measurements, correction factors, the incomplete mark, the automatic name?
Answer:

### Q60
Block: B44 — Receiving recorded races from the watch
Question: What does the phone do when it receives a race it already holds, the watch not having got the confirmation for the first transfer?
Answer:

### Q61
Block: B61 — Connectivity permission denied
Question: Does the watch app need its own connectivity permission, and what does it show if that one is denied?
Answer:

### Q62
Block: B45 — Exercise session lifecycle
Question: What does the watch-face complication display?
Answer:

### Q63
Block: B45 — Exercise session lifecycle
Question: What heart-rate data is retained with a race — a series, a maximum, an average — and how long does it live?
Answer:

### Q64
Block: B60 — Heart-rate data consent
Question: Is the exercise session written back to the phone's or the watch's health platform, or does the app keep it in its own storage only?
Answer:

### Q65
Block: B46 — Monotonic timing and recovery
Question: What happens to a race in progress when the watch reboots, the monotonic clock restarting at that moment?
Answer:

### Q66
Block: B47 — Duration formats
Question: What does duration-segment show for a segment that does exceed the hour?
Answer:

### Q67
Block: B51 — Date formats
Question: Does the time part read "9:14" or "09:14", the format being written "h:mm" and the example "09:14"?
Answer:

### Q68
Block: B51 — Date formats
Question: What is the abbreviation of each of the twelve months?
Answer:

### Q69
Block: B52 — Rounding rule
Question: How is a pace value rounded to m:ss for display — truncated like a duration, or rounded?
Answer:

### Q70
Block: B54 — Dynamic texts and fallbacks
Question: Is the stored race name the trimmed value or the value as typed, when it carries leading or trailing spaces?
Answer:

### Q71
Block: B2 — Color tokens
Question: Is the arrow said to always accompany ahead and behind present on the phone's delta column, on the race delta badge and on the end-of-race delta badge, where none is described — or is the rule limited to the running pace?
Answer:

### Q72
Block: B22 — Watch home screen / B56 — Fixed text catalogue
Question: Does the watch's sync failure text read "approche le téléphone de la montre." or "approche la montre du téléphone."?
Answer:

### Q73
Block: B51 — Date formats / B55 — Relative date wording
Question: Does a date with time read "12 avr. 2026 · 09:14" or "14 sept. 2025 à 09:02" — which of the two separators applies, and to which fields does each apply?
Answer:

### Q74
Block: B50 — Settings and range formats
Question: Is the upper bound printed in a zone range the next threshold or the next threshold minus one — "94–112 bpm" against zone ranges bounded 112 to 130 then 131 to 149 — and does the extreme zone read "> 150 bpm" when 150 belongs to that zone?
Answer:

### Q75
Block: B43 — Sending profile and reference to the watch
Question: Does a push that fully replaces the watch's state erase the races the watch recorded and has not yet had confirmed by the phone?
Answer:

### Q76
Block: B12 — Reading and validating a pasted result
Question: Does the pasted table include the "Total time" row the error message tells the user to copy up to, and is it counted among the 30 data rows or discarded?
Answer:

### Q77
Block: B22 — Watch home screen
Question: Where on the watch's home screen does the refused-sensor-permission reminder sit, relative to the reference line, "Démarrer", "Historique" and "Synchroniser"?
Answer:

### Q78
Block: B22 — Watch home screen
Question: Where does the watch show the date of the last successful sync?
Answer:

### Q79
Block: B23 — Watch history screen
Question: Does the watch's history list the races recorded on the watch and not yet transferred alongside the summarized history received from the phone, and are the two distinguished?
Answer:

### Q80
Block: B43 — Sending profile and reference to the watch
Question: When the link is already established, does a change made on the phone — a new reference, a rename, a deletion, an edited setting — push immediately, or wait for the next link establishment or the button?
Answer:

### Q81
Block: B31 — Control page
Question: How does the user leave the Control page back to the main page, no page answering a leftward swipe and the surface not being the advance button here — does the 8-second inactivity return apply to Control?
Answer:

### Q82
Block: B6 — Race list screen
Question: What total time does an incomplete race's card show, and is it distinguished from a complete race's total?
Answer:

### Q83
Block: B29 — Data freshness on the race pages
Question: Does sensor data arriving in batches while the screen is not interactive count as a new reading for the 10-second fallback threshold?
Answer:

### Q84
Block: B17 — Deriving maximum heart rate
Question: What happens when the value read from the health history falls outside the 100–230 bpm bounds the profile enforces?
Answer:

### Q85
Block: B1 — Race segment structure
Question: Is the fifth station named "Row" or "Rameur" on screen, the race structure naming it Row and the import mapping it to Rameur?
Answer:

### Q86
Block: B11 — Paste-a-result screen
Question: How is the "Rien à lire" empty-paste error reached, the "Importer" button being disabled while the paste area is empty?
Answer:

### Q87
Block: B37 — Computing the correction factor
Question: What happens to the correction factor retained at the end of a kilometre when the marking that closed that kilometre is undone?
Answer:

### Q88
Block: B21 — Waiting for the phone
Question: Does the watch show the waiting screen or the home screen with "Aucune référence" when the phone's connectivity permission is denied and no profile has ever been received?
Answer:

### Q89
Block: B5 — Idle display token variants
Question: "Idle" names both the power-save display mode and the resting state of the four non-active arc segments — are these two names or one?
Answer:

### Q90
Block: -
Question: Are Hyrox formats other than the individual race — doubles, relay, pro — in scope, the model holding one fixed 30-segment sequence?
Answer:

### Q91
Block: -
Question: Does either app collect analytics, usage statistics or crash reports?
Answer:

### Q92
Block: -
Question: Does either app post a notification — sync result, race in progress — and is the notification permission requested?
Answer:

### Q93
Block: -
Question: Is the race history backed up off the device, and what does the user find after a reinstall or on a new phone?
Answer:

### Q94
Block: -
Question: What guides a first-time user on the phone to set the maximum heart rate, nothing on the race list pointing to the profile and the watch waiting for that profile?
Answer:

### Q95
Block: -
Question: Is screen-reader support in scope, and what does each icon-only control announce?
Answer:

### Q96
Block: -
Question: How are the phone and the watch paired, and what happens when more than one watch is paired to the phone?
Answer:
