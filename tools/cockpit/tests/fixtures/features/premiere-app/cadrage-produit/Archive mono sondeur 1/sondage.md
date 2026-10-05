# Sondage — premiere-app

## Answers

B1.A1.1 | nothing fires it — fixed reference structure, consulted; A3 applies
B1.A1.2 | nothing: the sequence is defined in the block
B1.A1.3 | the ordered 30-segment breakdown, its segment kinds, the 8 stations in order
B1.A1.4 | displays nothing itself
B1.A1.5 | no tie possible — positions fixed 1 to 30
B1.A1.6 | no trigger, nothing to undo
B1.A1.7 | constant, kept
B1.A1.8 | consulted freely, holds no state
B1.A2.model.1 | exactly 30 ordered segments; kinds km run, Roxzone, station, final combined block; stations SkiErg, Sled Push, Sled Pull, Burpee Broad Jump, Row, Farmers Carry, Sandbag Lunges, Wall Balls
B1.A2.model.2 | mandatory — every race holds all 30 positions
B1.A3.1 | cycles 1–7 = run, Roxzone out, station, Roxzone back (segments 1–28); segment 29 = km 8; segment 30 = Roxzone + Wall Balls + finish sprint
B1.A3.2 | the pasted-result reading, the watch recording, the segment-by-segment comparison
B1.A3.3 | impossible by construction — the 30 positions always exist
B1.A3.4 | declared fixed — the official Hyrox sequence, no variant provided for
B1.A4.1 | names: Hyrox race, eight 1km runs, the 8 stations, Roxzone, cycle, segment 29, segment 30, official race clock, imported race, watch-recorded race — settled here except the official race clock
B1.A4.2 | gap: the 30 segments are counted but never named one by one, only the 8 stations are
B1.A4.3 | "fixed order" = the order listed; "matches the official race clock" = that clock; "without reconstruction" = against rebuilding from another breakdown — closed

B2.A1.1 | nothing fires it — token table, consulted; A3 applies
B2.A1.2 | nothing
B2.A1.3 | the named colour values used by every rendering
B2.A1.4 | displays nothing itself
B2.A1.5 | no order produced
B2.A1.6 | no trigger, nothing to undo
B2.A1.7 | constant
B2.A1.8 | consulted freely
B2.A2.model.1 | one hex or rgba value per token; the set is closed, every value given
B2.A2.model.2 | all mandatory, no optional token, no fallback value
B2.A3.1 | surface #121110, surface-raised #1C1A18, screen-black #000000, text-primary #F3EFE7, text-body #C9C4BA, text-secondary #9A958C, text-tertiary #6F6A62, border rgba(255,255,255,0.08), border-strong rgba(255,255,255,0.25), ahead #4FAE72, ahead-text #7FCB9C, ahead-bg rgba(79,174,114,0.16), behind #E2725F, behind-text #E2957F, behind-bg rgba(226,114,95,0.16), delta-zero #726D63, link #6FA3D8, zone-1 #4A90D9, zone-2 #35B0A4, zone-3 #4CAF63, zone-4 #E0A23A, zone-5 #E0503F
B2.A3.2 | every screen description, phone and watch
B2.A3.3 | impossible by construction — screens refer only to this closed set
B2.A3.4 | declared fixed; colours enter no computation, nothing to recompute
B2.A4.1 | names: the 22 tokens with their values, plus the sign and arrow that always accompany ahead/behind
B2.A4.2 | the sign points at B48, the arrow at B41 — both described blocks
B2.A4.3 | "decreasing emphasis" = primary > body > secondary > tertiary; border-strong vs border; blue-to-red = zone-1..5 — values given, closed

B3.A1.1 | nothing fires it — type scale, consulted; A3 applies
B3.A1.2 | nothing
B3.A1.3 | the families, weights and sizes used by every rendering
B3.A1.4 | displays nothing itself
B3.A1.5 | no order produced
B3.A1.6 | no trigger, nothing to undo
B3.A1.7 | constant
B3.A1.8 | consulted freely
B3.A2.model.1 | font-label = IBM Plex Sans, font-data = IBM Plex Mono tabular; weights 700/600/500 only, font-data 700 only; watch px on 480×480, phone dp
B3.A2.model.2 | mandatory — every text carries a family, a weight and a size from these scales
B3.A3.1 | watch w-display 110, w-display-sm 80, w-value 48, w-value-sm 40, w-badge 37, w-title 33, w-label 24, w-label-sm 20, w-caption 18; phone p-title 22, p-value 20, p-body 15, p-label 13, p-data 12.5, p-caption 11
B3.A3.2 | every rendering description, phone and watch
B3.A3.3 | impossible by construction — both scales are closed
B3.A3.4 | declared fixed — "three weights, never others", each scale complete
B3.A4.1 | names: font-label, font-data, the three weights, the nine w-* and six p-* sizes, each with its usage — all settled here
B3.A4.2 | each size names its bearer (central clock, end-of-race total, heart rate, Roxzone destination, delta badge, titles, units, bpm, zone number, screen title, race total, running text, setting labels, segment rows, dates) — all described elsewhere
B3.A4.3 | "tabular figures keep a clock from changing width" = against proportional digits; every size is an absolute value — closed

B4.A1.1 | nothing fires it — shape, spacing and arc scale, consulted; A3 applies
B4.A1.2 | nothing
B4.A1.3 | radii, spacings, arc geometry, letter-spacings, the target device
B4.A1.4 | displays nothing itself; the arc it defines is drawn by B28
B4.A1.5 | no order produced
B4.A1.6 | no trigger, nothing to undo
B4.A1.7 | constant
B4.A1.8 | consulted freely
B4.A2.model.1 | radius-pill = half the height, radius-card 12, radius-chip 14; space-xs/s/m/l/xl 4/8/12/20/32 dp, ×1.83 on the watch; letter-spacing 0.04/0.06/0.08em
B4.A2.model.2 | all mandatory; letter-spacing nil on running text and on any timed value
B4.A3.1 | arc-radius 229px, arc-span 140° centred low, arc-segment 25.6°, arc-gap 3°, arc-width 13, arc-width-active 33, arc-opacity-idle 0.30, arc-opacity-active 1; active radius = arc-radius + arc-width/2 − arc-width-active/2
B4.A3.2 | every rendering description; the arc values by B28 and B5
B4.A3.3 | impossible by construction — the set is closed
B4.A3.4 | declared fixed, tied to the 480×480 Galaxy Watch Ultra frame
B4.A4.1 | names: radius-pill, radius-card, radius-chip, space-xs/s/m/l/xl, the eight arc-* values, the ×1.83 multiplier, the three letter-spacing roles, Galaxy Watch Ultra / Wear OS 5 / One UI Watch 6 — all settled here
B4.A4.2 | the letter-spacing roles name their bearers: cycle header, station name, "arrivée estimée", watch out-of-race titles, Control title, zone number — each described in its block
B4.A4.3 | "95% of the screen radius", "thickens toward the inside, outer edge aligned with the four others", "to stay within the 480×480 frame" — each comparison carries its term

B5.A1.1 | nothing fires it — variant table read when the display dims; A3 applies
B5.A1.2 | nothing
B5.A1.3 | the dimmed opacities and thinned arc widths used by B35
B5.A1.4 | displays nothing itself; it restyles the race screens in place
B5.A1.5 | no order produced
B5.A1.6 | no trigger, nothing to undo
B5.A1.7 | constant
B5.A1.8 | consulted freely
B5.A2.model.1 | 0.55 on text-primary, any timed value and ahead/behind/delta-zero; 0.45 on text-secondary and text-tertiary; arc-width-dim 7, arc-width-active-dim 22, arc-opacity-idle-dim 0.25
B5.A2.model.2 | mandatory in idle mode; nothing moves, resizes or changes colour
B5.A3.1 | the six values above, replacing arc-width 13, arc-width-active 33, arc-opacity-idle 0.30
B5.A3.2 | the always-on display of B35, over the race screens
B5.A3.3 | impossible by construction — every dimmed token has its normal counterpart
B5.A3.4 | declared fixed
B5.A4.1 | names: dim-text, the two opacities, arc-width-dim, arc-width-active-dim, arc-opacity-idle-dim, the race screens, the meaning colours — all settled with values
B5.A4.2 | the race screens point at B28/B30/B31, the tokens at B2 and B4
B5.A4.3 | "instead of 13", "instead of 33", "instead of 0.30" give the other term; "lightens by thinning, not by geometry" = segments stay full — closed

B6.A1.1 | opening the app, and every return to the list
B6.A1.2 | each race's name, date, total time and completeness, the current reference designation, the insertion rank
B6.A1.3 | the sorted card list or the empty state, and entry into detail, profile and paste
B6.A1.4 | phone, whole screen: header on top, cards below, or the centred empty block
B6.A1.5 | date descending, then most recently added first — internal insertion order, never shown
B6.A1.6 | leaving closes the screen, no effect survives
B6.A1.7 | nothing produced beyond the display
B6.A1.8 | yes, cleanly — the list is read again at each return
B6.A2.screen.1 | p-title title, profile icon and + button in 36–38dp bordered circles; per card name, total time, date, Reference badge, Incomplete badge; card opens detail, icon opens profile, + opens paste
B6.A2.screen.2 | gap: the empty state is given, but not what shows while loading or if the races cannot be read
B6.A2.screen.3 | gap: nothing is entered here, but whether the scroll position survives a return from a detail is not stated
B6.A4.1 | names: race name, date, total time, the visible reference mark, Reference badge, Incomplete badge, header title, profile icon, + button, empty title, explanation, "Coller un résultat" — settled except the profile icon's glyph
B6.A4.2 | badges give colour and shape, wordings come from B56, destinations from B57, incompleteness from B33 — all described
B6.A4.3 | gap: "most recent first" and "added most recently" carry their term, but "a constrained width" names no value

B7.A1.1 | tapping a race card in the list, or saving an imported race
B7.A1.2 | the race's 30 durations and cumulative times, its name, date, total, reference status; the reference race's segment times
B7.A1.3 | the header, the three actions, the 30 rows grouped by cycle, the delta column
B7.A1.4 | phone, whole screen: header block, action row under it, grouped segment list below
B7.A1.5 | rows follow segment order 1 to 30 — no tie possible
B7.A1.6 | leaving closes the screen, no effect survives
B7.A1.7 | nothing produced beyond the display
B7.A1.8 | yes, cleanly — re-read at each opening
B7.A2.screen.1 | name, date, total, reference badge; "Définir comme référence" filled, "Renommer" bordered, "Supprimer" in behind; per row name, duration, cumulative, delta; CYCLE n headers
B7.A2.screen.2 | gap: unreached segments show a dash and an empty delta, but nothing states the loading state or a read failure
B7.A2.screen.3 | nothing is in progress here — rename and delete open their own confirmations
B7.A4.1 | names: race name, date, total time, reference badge, the three actions, CYCLE n header, segment name, duration, cumulative time, delta column, the dash, the reference race, the total shown
B7.A4.2 | gap: the delta column's own rule is never given (real minus reference, on which segment), and "columns aligned to a fixed width" names no width
B7.A4.3 | "unless the race is itself the reference, or no reference exists" carries its terms; "the sum of the segments actually run" is stated — closed

B8.A1.1 | tapping "Définir comme référence" in a race's detail
B8.A1.2 | the designated race, its completeness, the current reference designation
B8.A1.3 | that race becomes the current reference, the previous one loses the mark, the button hides
B8.A1.4 | the detail screen's action row, and the Reference badge on the list card
B8.A1.5 | one reference at a time, no ordering
B8.A1.6 | the designation persists until another race is set or the reference is deleted
B8.A1.7 | kept — the previous reference stays a race, only its mark goes
B8.A1.8 | yes, cleanly — setting another race replaces the designation
B8.A2.persistence.1 | stored — a single current-reference designation, not recomputed
B8.A2.persistence.2 | not applicable — the designation is a single value, present or absent
B8.A3 | not applicable — a user action fires it
B8.A4.1 | names: "Définir comme référence", the current reference, the previous reference, the mark, an incomplete race, the list card, the detail screen
B8.A4.2 | the mark points at B6's Reference badge, incompleteness at B33, the no-reference state at B10 — all described
B8.A4.3 | "already the current reference" and "incomplete" both carry their term — closed

B9.A1.1 | tapping "Renommer" in a race's detail
B9.A1.2 | the race's current name, the text entered
B9.A1.3 | the stored name replaced by the entered one
B9.A1.4 | gap: over the detail screen — the block does not say whether it is a dialog or a screen of its own
B9.A1.5 | no order produced
B9.A1.6 | "Annuler" leaves the stored name untouched
B9.A1.7 | the previous name is replaced, not kept
B9.A1.8 | yes, cleanly — renaming again starts from the current name
B9.A2.persistence.1 | stored — the entered name replaces the previous one
B9.A2.persistence.2 | not applicable — a name is never empty, so nothing partial can be stored
B9.A3 | not applicable — a user action fires it
B9.A4.1 | names: "Renommer", the pre-filled field, the current name, "Annuler", "Enregistrer", the name rule of B54
B9.A4.2 | the name rule points at B54, which gives never-empty and 40 characters — described
B9.A4.3 | "pre-filled with the current name", "40 characters maximum" — carry their terms

B10.A1.1 | tapping "Supprimer" in a race's detail, then confirming
B10.A1.2 | the race, its name, whether it is the current reference
B10.A1.3 | the race deleted, possibly no reference left, the return to the list, its removal from the watch at the next push
B10.A1.4 | a confirmation over the detail screen: "!" badge, title naming the race, message, two buttons
B10.A1.5 | no order produced
B10.A1.6 | "Annuler" leaves everything as it was
B10.A1.7 | the race and its segments are deleted; the correction factor is untouched
B10.A1.8 | not on the same race — it no longer exists
B10.A2.persistence.1 | stored — the deletion is written, and mirrored to the watch at the next push
B10.A2.persistence.2 | not applicable — a deletion leaves nothing partial
B10.A3 | not applicable — a user action fires it
B10.A4.1 | names: "Supprimer", the confirmation, the "!" badge, the race name, the two sentences, "Annuler", the no-reference state, the next push, the watch history, the race list
B10.A4.2 | the push points at B43, the no-reference state at B22's "Aucune référence", the list at B6 — all described
B10.A4.3 | "the only place in the app where a race is deleted", "no race is chosen automatically" — carry their terms

B11.A1.1 | tapping the + button in the list header, or the empty list's own button
B11.A1.2 | the pasted text and the entered race name
B11.A1.3 | the two entered values, and the reading of B12 when "Importer" is tapped
B11.A1.4 | phone, whole screen: tall paste field on top, name field under it, full-width "Importer" at the bottom
B11.A1.5 | no order produced
B11.A1.6 | emptying either field disables "Importer" again
B11.A1.7 | the entered text stays in place; "Corriger" and "Revenir au collage" come back to it
B11.A1.8 | yes — pasting again replaces the previous text
B11.A2.screen.1 | multiline paste field with placeholder, "Nom de la course" field, "Importer" pill; disabled while either is empty, active once both are filled, no inline error
B11.A2.screen.2 | gap: nothing states what the screen shows while the paste is being read
B11.A2.screen.3 | gap: the text survives "Corriger" and "Revenir au collage", but nothing says whether it survives leaving the screen altogether
B11.A4.1 | names: the four columns copied from hyresult, the paste field, its placeholder, the name field, "Importer", the disabled state
B11.A4.2 | the wordings point at B56, the reading at B12, the failure at B15 — all described
B11.A4.3 | "stays disabled while empty", "active as soon as both are filled", "no file picker since results are never exported as a file" — carry their terms

B12.A1.1 | tapping "Importer" on the paste screen
B12.A1.2 | the pasted text: its rows, its four columns, the Time of Day, Diff and Time values, the station labels
B12.A1.3 | on success the 30 segment durations, the recognized total, the segment count, the start time; on failure the first faulty row's number and its cause
B12.A1.4 | displays nothing itself — B13 and B15 display its outcome
B12.A1.5 | rows keep the pasted order, checked against the expected cycle order
B12.A1.6 | nothing is written until "Enregistrer", so a failed reading leaves no trace
B12.A1.7 | the recognized values are handed to the preview and dropped if the user corrects
B12.A1.8 | yes, cleanly — each tap re-reads the whole text
B12.A2.external source.1 | a failure names the first faulty row and its cause, nothing is written, an import is never partial; a label or column change at the source is a normal reading failure, never a crash, never an approximate interpretation
B12.A2.external source.2 | gap: nothing identifies a result already imported — pasting the same result twice is not addressed
B12.A3 | not applicable — a user action fires it
B12.A4.1 | names: the four columns, the tab or multi-space separator, the skipped header row, m:ss and h:mm:ss scales, Time of Day, Diff, Time, "Rox In", "Wall Balls In", the mapping table, the three acceptance conditions
B12.A4.2 | gap: the four columns are read by position but never named in order, and the block never says which column carries a segment's own duration
B12.A4.3 | "only one row may be skipped this way", "a second row with the same defect is an error", "exactly 30 data rows", "the running sum matches the Time column on every row" — carry their terms

B13.A1.1 | a successful reading by B12
B13.A1.2 | the recognized total time and the segment count
B13.A1.3 | the preview display, then a return to paste or the save of B14
B13.A1.4 | phone, whole screen: "✓" badge, title, two label/value lines, two buttons
B13.A1.5 | no order produced
B13.A1.6 | "Corriger" returns to the paste screen with the text kept
B13.A1.7 | the recognized values are dropped unless "Enregistrer" is tapped
B13.A1.8 | yes — a new reading shows a new preview
B13.A2.screen.1 | "Temps total reconnu" and "Segments détectés" with their values; "Corriger" bordered returns to paste, "Enregistrer" filled saves
B13.A2.screen.2 | the screen exists only on a successful reading, so it never shows empty; a failure opens B15 instead
B13.A2.screen.3 | the pasted text is kept and found again on the paste screen; nothing else is in progress here
B13.A4.1 | names: the "✓" badge, the title, the two labels, the recognized total, the segment count, "Corriger", "Enregistrer"
B13.A4.2 | the values point at B12, the save at B14, the wordings at B56 — all described
B13.A4.3 | "before anything is saved" carries its term — closed

B14.A1.1 | tapping "Enregistrer" in the preview
B14.A1.2 | the 30 segment durations read by B12 and the name entered on the paste screen
B14.A1.3 | a new race record, and the opening of its detail screen
B14.A1.4 | displays nothing itself — it opens B7
B14.A1.5 | no order produced
B14.A1.6 | once saved the race persists; only B10 removes it
B14.A1.7 | the 30 durations are kept; the recognized total and count are not stored
B14.A1.8 | yes — importing again creates another race, even under the same name
B14.A2.persistence.1 | stored: the name and the 30 durations; the total is recomputed by summing them
B14.A2.persistence.2 | not applicable — an imported race always holds its 30 segments, and nothing is written on a failure
B14.A3 | not applicable — a user action fires it
B14.A4.1 | names: the new race record, the entered name, the 30 durations, the recomputed total, the detail screen, the correction factor never produced, the date that distinguishes same-named races
B14.A4.2 | gap: the stored record never includes a date, though the block distinguishes same-named races "by their date" and B12 computes a start time
B14.A4.3 | "never the race list", "without exception", "no uniqueness constraint", "only watch-recorded races calibrate it" — carry their terms

B15.A1.1 | a failed reading by B12
B15.A1.2 | the cause of the first anomaly, the faulty row's number, the label read
B15.A1.3 | one message — title and explanation — the row as read, its expected form, and the return to the paste screen
B15.A1.4 | phone, whole screen: "!" badge, title, explanation, then a surface-raised panel holding the two rows
B15.A1.5 | one message at a time — the first anomaly found, reading in order
B15.A1.6 | "Revenir au collage" returns to the paste screen with the text kept
B15.A1.7 | nothing was written, so nothing is undone
B15.A1.8 | yes — each failed reading shows its own message
B15.A2.screen.1 | the eight cause/title/explanation rows of the catalogue, the row as read in behind, its expected form in ahead, "Revenir au collage"; no control applies the illustrated form
B15.A2.screen.2 | an empty paste is itself a catalogued cause, "Rien à lire"; the screen only ever shows on a failure
B15.A2.screen.3 | the pasted text is kept and found again on the paste screen; nothing else is in progress here
B15.A4.1 | names: the eight causes with their exact titles and explanations, "<n>", "<libellé>" truncated to 20 characters, the row as read, its expected form, "Revenir au collage"
B15.A4.2 | gap: an expected form is shown as illustration for every cause but is never given for any of them
B15.A4.3 | "one message at a time, the first anomaly found, read in order", "truncated to 20 characters" — carry their terms

B16.A1.1 | tapping the profile icon in the race list header
B16.A1.2 | the stored maximum heart rate, the four thresholds, the kilometre distance, the long-press duration, the last successful sync date, the sync state
B16.A1.3 | the settings display, the edits handed to B19, the sync triggered by its button
B16.A1.4 | phone, whole screen: HR max block, five zone rows, two setting rows, the sync button with the last-success date under it
B16.A1.5 | zones display in order 1 to 5 — no tie possible
B16.A1.6 | leaving closes the screen; the stored settings stay
B16.A1.7 | saved values persist; the sync state is transient
B16.A1.8 | yes, cleanly — the screen re-reads the profile
B16.A2.screen.1 | HR max with "Maximum observé sur 12 mois · Modifier" opening a numeric dialog; the four thresholds, the distance and the press duration in inline fields validated on loss of focus, no stepper, no slider; a "Synchroniser avec la montre" button
B16.A2.screen.2 | the zone ranges stay hidden while HR max is unknown; sync in progress shows "Ne ferme pas l'application", failure a message in behind with "Réessayer"
B16.A2.screen.3 | gap: an inline field validates on loss of focus, but nothing says what becomes of a half-edited field when the screen is left
B16.A4.1 | names: the four settings, "Modifier", the five zone rows with swatch, label, percentage and bpm range, the sync button, the last successful sync date, the three sync states
B16.A4.2 | the ranges point at B18, the bounds at B19, the derivation at B17, the sync at B43, the wordings at B56 and B54 — all described
B16.A4.3 | "Maximum observé sur 12 mois" carries its window; "columns aligned" and "full-width" carry their frame — closed

B17.A1.1 | opening the profile for the first time
B17.A1.2 | the phone's health history over the past twelve months, and its permission
B17.A1.3 | a proposed maximum heart rate, or no value at all
B17.A1.4 | the profile screen's HR max field
B17.A1.5 | the highest value observed wins — equal values change nothing
B17.A1.6 | a value entered by hand is never overwritten by a later automatic reading
B17.A1.7 | kept — a higher value observed later is never flagged
B17.A1.8 | gap: nothing says whether the automatic reading is attempted again at a later opening when no value was ever obtained or entered
B17.A2.external source.1 | empty, inaccessible or refused history: no value is guessed, the field stays to be filled by hand, the zone ranges stay hidden
B17.A2.external source.2 | not applicable — a single value is read, the highest over twelve months, not a set of records to reconcile
B17.A3 | not applicable — opening the profile fires it
B17.A4.1 | names: the phone's health history, the twelve months, the highest value, the hand-entered value, Samsung Health's own zones and HR max, the permission
B17.A4.2 | the ranges point at B18, the field at B16, the bounds at B19 — all described
B17.A4.3 | "the highest value observed over the past twelve months", "never overwritten by a later automatic reading", "read on the phone only" — carry their terms

B18.A1.1 | a maximum heart rate becoming known, and any change to it or to a threshold
B18.A1.2 | the maximum heart rate and the four threshold percentages
B18.A1.3 | the five zone ranges in bpm, and the zone matching any reading
B18.A1.4 | the profile screen's five zone rows; the arc of B28 uses the zone it yields
B18.A1.5 | no order produced — the five zones are contiguous and disjoint
B18.A1.6 | without a known maximum heart rate the ranges are hidden
B18.A1.7 | recomputed whenever HR max or a threshold changes, and never applied to a recorded race
B18.A1.8 | yes — a pure computation, repeatable
B18.A2.calculation.1 | gap: zone n runs from threshold n included to threshold n+1 excluded, zone 1 below the first, zone 5 above the fourth, defaults 60/70/80/90% — but nothing says how a fractional threshold becomes a whole bpm, and the worked example on 187 matches neither plain truncation nor plain ceiling
B18.A2.calculation.2 | without a maximum heart rate no range exists and the rows stay hidden
B18.A2.calculation.3 | output is a zone 1 to 5, always exactly one; no reading falls outside, none falls in two
B18.A3 | not applicable — a known or changed maximum heart rate fires it
B18.A4.1 | names: the four thresholds, the five zones, the defaults, the worked example on 187, the always-active arc segment, the four threshold settings, the hidden ranges
B18.A4.2 | the settings point at B16, their bounds at B19, the arc at B28, the switching rule at B42 — all described
B18.A4.3 | "included" and "excluded" name the boundary's side; "everything above the fourth", "everything below the first" — carry their terms

B19.A1.1 | validating an edited setting on the profile screen
B19.A1.2 | the entered value, the setting's bounds, the other three thresholds for the ordering check
B19.A1.3 | the saved value, or a rejection with the field reverted and a short message
B19.A1.4 | the profile screen's field being edited, with the message beside it
B19.A1.5 | no order produced — the thresholds' order is a constraint, not a sort
B19.A1.6 | a rejected value leaves the stored one untouched
B19.A1.7 | recorded races keep their durations, factor and heart-rate measurements — nothing is recomputed
B19.A1.8 | yes — a setting can be edited again at any time
B19.A2.persistence.1 | gap: stored in the profile with bounds HR max 100–230 bpm, thresholds 30–99% strictly increasing, distance 500–2000 m, press duration 300–2000 ms — but only the press duration is given a default value; the kilometre distance and the maximum heart rate have none
B19.A2.persistence.2 | the maximum heart rate may be absent — the profile then holds no value at all, not a zero, and the ranges stay hidden
B19.A3 | not applicable — a user validation fires it
B19.A4.1 | names: the four settings, their bounds, the increasing order, distance_attendue, the rejection message, the next race, the next sync
B19.A4.2 | the effects point at B42, B37, B39, B27 and B43 — all described
B19.A4.3 | "strictly increasing from the first to the fourth", "from the next race onward", "only at the next sync" — carry their terms

B20.A1.1 | the first launch of the watch app, and the check made at every later launch
B20.A1.2 | the system's sensor permission state
B20.A1.3 | granted: heart rate and the zone arc work; refused: permanent fallback plus a home-screen reminder that re-asks or opens the settings page
B20.A1.4 | gap: the reminder sits "on the home screen" but its place there is never given, and B22's rendering does not carry it
B20.A1.5 | no order produced
B20.A1.6 | a revocation from the system settings produces the same fallback as an initial refusal
B20.A1.7 | the refusal is kept — the request is never repeated automatically
B20.A1.8 | only through the reminder: it asks the system again, or opens the app's permissions page when the system no longer offers the request
B20.A2.transition.1 | the first launch asks; every later launch checks; a tap on the reminder re-asks
B20.A2.transition.2 | states: never asked, granted, refused, permanently refused or revoked; never-asked leads to granted or refused; refused leads to granted only through the reminder or the settings page; in every state the clock, segments and deltas keep working
B20.A3 | not applicable — a launch fires it
B20.A4.1 | names: the request sentence, the pill action button, the reminder, the permanent fallback, the system permissions page, heart rate, the zone arc
B20.A4.2 | the wordings point at B56, the fallback at B29 and B28, the arc at B4 — all described
B20.A4.3 | "leaves the app usable" = clock, segments and deltas keep working; "never repeated automatically"; "text on three lines maximum" — carry their terms

B21.A1.1 | launching the watch app while no profile has ever been received
B21.A1.2 | whether a profile has been received
B21.A1.3 | the waiting screen shown in place of the home screen, and a retry
B21.A1.4 | watch, whole screen, replacing the home screen
B21.A1.5 | no order produced
B21.A1.6 | once a profile arrives the home screen takes its place
B21.A1.7 | nothing produced beyond the display
B21.A1.8 | yes — it shows again at every launch until a profile arrives
B21.A2.screen.1 | gap: "En attente du téléphone" with a retry button, but nothing says what the retry does — ask the phone, re-check the link, or re-read the local state
B21.A2.screen.2 | the screen is itself the no-data state; no loading or failure state is distinguished
B21.A2.screen.3 | nothing is in progress on this screen
B21.A4.1 | names: "En attente du téléphone", its explanation, "Réessayer", the received profile, the home screen
B21.A4.2 | the profile points at B43's push, the home screen at B22, the wordings at B56 — all described
B21.A4.3 | "until a profile has been received", "instead of the home screen" — carry their terms

B22.A1.1 | reaching the watch home — at launch once a profile exists, or on leaving a race or a secondary screen
B22.A1.2 | the current reference's name and total time, the history, the sync state and its last success
B22.A1.3 | the reference line, the three actions, and the sync push and pull that "Synchroniser" fires
B22.A1.4 | watch, whole screen: reference line on top, "Démarrer" under it, "Historique" and "Synchroniser" revealed by scrolling
B22.A1.5 | no order produced here
B22.A1.6 | leaving the home screen closes it; a sync result shows in place without leaving it
B22.A1.7 | nothing produced beyond the display and the sync it triggers
B22.A1.8 | yes, cleanly — returned to after every race and every secondary screen
B22.A2.screen.1 | "Réf. — <name>" with its time, a full-width "Démarrer" active even without a reference, "Historique" opening the list, "Synchroniser" acting in place
B22.A2.screen.2 | without a reference a "⚠ Aucune référence" badge; in progress an activity indicator with "Ne ferme pas l'application"; on failure "Synchronisation impossible — approche le téléphone de la montre." with "Réessayer"
B22.A2.screen.3 | a sync in progress is the only thing in progress, and it completes in place — the screen warns not to close the app
B22.A4.1 | names: "Réf. — <name>", the reference's total time, "⚠ Aucune référence", "Démarrer", "Historique", "Synchroniser", the three sync states, the failure sentence
B22.A4.2 | points at B43 and B44's sync, B16's three states, B54's dynamic text, B23's history — all described
B22.A4.3 | "active even without a reference", "bordered and not filled", "the same three states as the phone" — carry their terms

B23.A1.1 | tapping "Historique" on the watch home screen
B23.A1.2 | the summarized history received from the phone: name, date, total time
B23.A1.3 | the list display only — the watch changes nothing here
B23.A1.4 | watch, whole screen: title then one row per race
B23.A1.5 | gap: the block gives no order for the rows and no tie-break between two races of the same date
B23.A1.6 | leaving returns to the home screen
B23.A1.7 | nothing produced beyond the display
B23.A1.8 | yes, cleanly
B23.A2.screen.1 | "Historique" title, per row the name then date and total time on the next line; no action at all
B23.A2.screen.2 | gap: the block states no empty state and no not-yet-received state, though B56 carries an "Aucune course" wording it never claims
B23.A2.screen.3 | nothing is in progress on this screen
B23.A4.1 | names: "Historique", the race name, the date, the total time, the phone-only segment detail, the read-only rule
B23.A4.2 | points at B43's cap of 20, B44's received races, B51's date format, B56's wordings — all described
B23.A4.3 | "in summary" against the phone's segment-by-segment detail; "read-only on the whole configuration" lists what it excludes — no favorite change, no rename, no delete — closed

B24.A1.1 | tapping "Démarrer" on the watch home screen
B24.A1.2 | the sensors' availability and readings, whether a reference is loaded
B24.A1.3 | the exercise session opened, the heart rate shown, and on "Lancer" the clock started and the first segment opened
B24.A1.4 | watch, whole screen: heart-rate block, reference badge, "Lancer", "Quitter"
B24.A1.5 | no order produced
B24.A1.6 | "Quitter" closes the preparation and returns home
B24.A1.7 | nothing is recorded before the clock starts
B24.A1.8 | yes — "Démarrer" opens the preparation again
B24.A2.transition.1 | "Démarrer" opens it, "Lancer" starts the race, "Quitter" leaves it
B24.A2.transition.2 | states: preparing with the session open; preparing with the session failed and heart rate in fallback, "Lancer" still active and retrying; running — a second failure starts the race without sensor data for its whole duration, with no further retry
B24.A3 | not applicable — a user action fires it
B24.A4.1 | names: the preparation screen (the sas), the exercise session, the sensors warming up, "Fréquence cardiaque" and its value, "Référence chargée · <name>", "Lancer", "Quitter"
B24.A4.2 | the session points at B45, the conflict at B25, the resumption at B26, the first segment at B28, the missing badge at B54 — all described
B24.A4.3 | "nothing is recorded before the clock starts", "stays active", "no further retry once the race is running" — carry their terms

B25.A1.1 | starting the race while another app already holds the exercise session
B25.A1.2 | the system's exercise-session ownership
B25.A1.3 | a confirmation; continuing stops the other activity and starts ours, cancelling returns without starting
B25.A1.4 | watch, a confirmation between "Lancer" and the race's start
B25.A1.5 | no order produced
B25.A1.6 | cancelling leaves the other activity running and our race unstarted
B25.A1.7 | nothing produced on a cancel
B25.A1.8 | yes — tapping "Lancer" again asks again
B25.A2.transition.1 | tapping "Lancer" while another app holds the session
B25.A2.transition.2 | gap: the states are session-held-elsewhere, continued and cancelled, but nothing says what happens when stopping the other activity fails
B25.A3 | not applicable — a user action fires it
B25.A4.1 | names: the confirmation title, the mention that the running activity will be stopped, "Annuler", "Continuer", the one-session-at-a-time rule
B25.A4.2 | the rule points at B45, the wordings at B56, the start at B24 — all described
B25.A4.3 | "only one exercise session at a time, across all apps" carries its term — closed

B26.A1.1 | starting while the active exercise session belongs to our own race — the app restarted mid-race
B26.A1.2 | the session's owner, and the race state stored in the local database
B26.A1.3 | the race resumed from the stored state; neither the race nor the sensor session restarts
B26.A1.4 | gap: the block never names the screen the resumed race lands on
B26.A1.5 | no order produced
B26.A1.6 | not applicable — a resumption is not undone; only B33 ends the race
B26.A1.7 | the closed segments and the current segment's opening instant are kept
B26.A1.8 | yes — every restart mid-race resumes the same way
B26.A2.transition.1 | launching or starting while our own session is active
B26.A2.transition.2 | states: our session active → resume; another app's session → B25; no session → the normal start of B24
B26.A3 | not applicable — a start fires it
B26.A4.1 | names: the exercise session, our own race, the local database state, the restart
B26.A4.2 | the stored state points at B46, the conflict at B25, the start at B24 — all described
B26.A4.3 | "rather than restarting", "the sensor session itself is not restarted either" — carry their terms

B27.A1.1 | a long press anywhere on a race page other than Control
B27.A1.2 | the press-duration setting, the touch instant, the finger's movement during the press
B27.A1.3 | the current segment closed and the next opened, a vibration, a return to the main page
B27.A1.4 | every race page but Control — the whole surface is the button, signalled by a 9px dot
B27.A1.5 | no order produced — segments close in their fixed sequence
B27.A1.6 | releasing before the threshold cancels the marking and writes nothing; a slide over 20px cancels it and becomes a page swipe
B27.A1.7 | a closed segment keeps its duration; only B32 reopens the last one
B27.A1.8 | yes — no minimum delay separates two markings
B27.A2.transition.1 | the touch reaching the threshold without release and without a slide over 20px
B27.A2.transition.2 | states: pressing, cancelled by an early release or a slide, marked; one short pulse confirms, two signal a cancellation, nothing plays during the press itself
B27.A3 | not applicable — a user gesture fires it
B27.A4.1 | names: the whole screen as button, the 700ms default, the profile setting, the vibration patterns, the automatic return to the main page, the 8-second inactivity return, the 20px slide, the touch instant
B27.A4.2 | the setting points at B19, the pages at B28, B30 and B31, Control's exclusion at B31 — all described
B27.A4.3 | "at least 700ms by default", "more than 20px", "after 8 seconds without interaction", "at the moment the finger touches, not at release" — carry their terms

B28.A1.1 | opening a race, and every segment change — it is the page shown by default
B28.A1.2 | the current segment and its kind, the lap delta, allure-segment, the trend arrow, the reference's segment time, the elapsed time, the next step's name, the heart rate and its zone
B28.A1.3 | the three blocks displayed, adapted to the segment in progress
B28.A1.4 | watch, whole screen: top block, centre block, bottom block holding heart rate and the zone arc
B28.A1.5 | no order produced
B28.A1.6 | at each marking the page re-adapts to the new segment
B28.A1.7 | nothing produced beyond the display
B28.A1.8 | yes — returned to after every marking and after 8 idle seconds
B28.A2.screen.1 | run: lap delta on top, allure-segment large with its trend arrow and "/km"; station: the reference's time on top, elapsed time large; Roxzone: transition time on top, the next step large; segment 30 shown as a station named Wall Balls; bottom always heart rate, "bpm", the zone number and the five arcs
B28.A2.screen.2 | without a reference four blocks disappear without the page being reorganised; without a reading the heart rate shows a dash and no arc segment is active
B28.A2.screen.3 | nothing is entered here; the page returns to its own state after a marking or 8 idle seconds
B28.A4.1 | names: the three display states, the lap delta, allure-segment, "/km", the trend arrow, "Réf. 4:26", the Roxzone time, "→ SkiErg" and "→ Run 3", heart rate, "bpm", the zone number, the five arcs, the 9px dot, the four blocks that disappear
B28.A4.2 | points at B39, B36, B41, B4, B42, B29, B30 — all described
B28.A4.3 | "large" = w-display; "at most three legible blocks at once, never four"; "a Roxzone's timing is never presented as underperformance"; "no fourth display state exists" — carry their terms

B29.A1.1 | nothing fires it — a display convention read by the race pages; A3 applies
B29.A1.2 | nothing of its own; it governs values produced elsewhere
B29.A1.3 | the fallback rule for every displayed value
B29.A1.4 | it governs the race pages, occupying no area of its own
B29.A1.5 | no order produced
B29.A1.6 | no trigger, nothing to undo
B29.A1.7 | constant
B29.A1.8 | consulted freely
B29.A2.model.1 | the freshness threshold is 10 seconds in both display modes; a fallback is a dash or a hidden block, never a zero
B29.A2.model.2 | mandatory for every sensor-derived value; the clock is excluded — it never falls back
B29.A3.1 | 10 seconds without a new reading, in normal and in power-save mode; "+0:00" means tied, never unknown; absence shows a dash or hides its block; a fallback raises no message and interrupts nothing
B29.A3.2 | the race pages of B28 and B30, and the end screen of B34
B29.A3.3 | impossible by construction — a value is either fresh or in fallback
B29.A3.4 | declared fixed
B29.A4.1 | names: the 10-second threshold, the dash, the hidden block, "+0:00", the fallback, the clock that never falls back
B29.A4.2 | the pages point at B28 and B30, the delta format at B48, the refresh cadence at B35 — all described
B29.A4.3 | "past 10 seconds", "matching the refresh cadence", "a fallback is never an error" — carry their terms

B30.A1.1 | swiping right from the main page
B30.A1.2 | the cumulative delta, the estimated arrival, the total elapsed time, the position
B30.A1.3 | the three blocks displayed; the long press still marks a segment here
B30.A1.4 | watch, whole screen: delta badge on top, arrival large in the centre, elapsed time and position at the bottom
B30.A1.5 | no order produced
B30.A1.6 | a marking or 8 idle seconds returns to the main page
B30.A1.7 | nothing produced beyond the display
B30.A1.8 | yes — swiping right from the main page reopens it
B30.A2.screen.1 | delta badge, estimated arrival, "arrivée estimée", elapsed time and "14/30"; the long press marks a segment
B30.A2.screen.2 | gap: the block never says what Projection shows without a reference, though its top and centre both derive from one
B30.A2.screen.3 | nothing is in progress; the page is left automatically after a marking or 8 idle seconds
B30.A4.1 | names: the cumulative delta, the estimated arrival, "arrivée estimée", the total elapsed time, the position "14/30", the long press
B30.A4.2 | points at B40, B27, B49, B48 — all described
B30.A4.3 | "since the start", "total elapsed time" — carry their terms

B31.A1.1 | swiping right from Projection
B31.A1.2 | whether a marking has been made, and the name of the segment the last marking closed
B31.A1.3 | the two actions displayed: undo and stop
B31.A1.4 | watch, whole screen: "Contrôle" title, undo pill, stop text under it
B31.A1.5 | no order produced
B31.A1.6 | an undo returns to the main page; the stop opens its confirmation
B31.A1.7 | nothing produced beyond the display
B31.A1.8 | yes — reached again by swiping right from Projection
B31.A2.screen.1 | "Contrôle" title, a full-width filled undo pill naming the reopened segment, "Arrêter l'activité" in behind; the surface is not the advance button here
B31.A2.screen.2 | before the first marking the undo button is disabled; no other empty state applies
B31.A2.screen.3 | nothing is in progress on this page
B31.A4.1 | names: "Contrôle", the undo button, the segment it names, "Arrêter l'activité"
B31.A4.2 | points at B32, B33, B54's "Annuler : <segment fermé>" — all described
B31.A4.3 | "the only race page where the surface is not the advance button", "less prominent than the undo button" — carry their terms

B32.A1.1 | tapping the undo button on Control
B32.A1.2 | the last marking and the segment it closed
B32.A1.3 | that segment reopened as the current one, and the return to the main page
B32.A1.4 | the Control page's undo button, which names the segment
B32.A1.5 | no order produced — only the last marking is ever touched
B32.A1.6 | gap: nothing says whether the reopened segment resumes from its original opening instant or starts a fresh one
B32.A1.7 | gap: the button is disabled before the first marking, but its state right after an undo is never stated
B32.A1.8 | single-level: only the last marking, with no time limit
B32.A2.transition.1 | tapping the undo button on Control
B32.A2.transition.2 | states: no marking yet, with the button disabled; a marking available to undo; the segment reopened — undo being single-level, no second consecutive undo is described
B32.A3 | not applicable — a user action fires it
B32.A4.1 | names: the undo button, the last marking, the reopened segment, the disabled state, the absent time limit
B32.A4.2 | points at B27's marking, B31's page, B54's label — all described
B32.A4.3 | "single-level", "only ever the last marking", "no time limit", "before the first marking" — carry their terms

B33.A1.1 | tapping "Arrêter l'activité" on Control and confirming
B33.A1.2 | the race as it stands: its closed segments and its clock
B33.A1.3 | the clock and every measurement cut, the race saved and marked incomplete, the end screen opened
B33.A1.4 | a confirmation over Control, then the end screen
B33.A1.5 | no order produced
B33.A1.6 | "Annuler" leaves the race running
B33.A1.7 | closed segments are kept; segments never reached enter no calculation
B33.A1.8 | no — the race is over; a new one starts from the home screen
B33.A2.transition.1 | the confirmed stop
B33.A2.transition.2 | states: running, confirmation open, stopped and saved incomplete; leaving the app does not stop the session — only this action does
B33.A3 | not applicable — a user action fires it
B33.A4.1 | names: "Arrêter l'activité", the confirmation, the incomplete mark, the saved race, the ban on an incomplete reference
B33.A4.2 | points at B8's ban, B34's end screen, B56's wordings — all described
B33.A4.3 | "as it stands", "can never become the reference", "only this action does" — carry their terms

B34.A1.1 | the 30th marking, or a confirmed stop
B34.A1.2 | the total time, the final delta, the date and time, whether the race is incomplete
B34.A1.3 | the end screen, the automatic save, the automatic name, and the return home on "Terminer"
B34.A1.4 | watch, whole screen: centred block, "Terminer" at the bottom
B34.A1.5 | no order produced
B34.A1.6 | "Terminer" returns home; the race is already saved
B34.A1.7 | the saved race is kept and travels to the phone at the next link
B34.A1.8 | no — a new race starts from the home screen
B34.A2.screen.1 | total time, final delta badge, the race's automatic name as date and time, "Terminer"
B34.A2.screen.2 | without a reference the final delta is hidden; for a race stopped early the delta is the cumulative delta at the last closed segment and the screen states the race is incomplete
B34.A2.screen.3 | nothing is in progress; saving is automatic, without confirmation
B34.A4.1 | names: the total time, the final delta, the automatic name (date and time), the incomplete mention, "Terminer"
B34.A4.2 | points at B40, B54's generated name, B51's format, B33, B22's home — all described
B34.A4.3 | "at the last closed segment", "segments never reached enter no calculation", "without confirmation" — carry their terms

B35.A1.1 | the display going idle during a race
B35.A1.2 | the idle tokens of B5 and the values already displayed
B35.A1.3 | the dimmed race screens, refreshed every 10 seconds
B35.A1.4 | the race screens themselves, unchanged in layout
B35.A1.5 | no order produced
B35.A1.6 | gap: full refresh resumes on a wrist raise or a screen touch, but nothing says what returns the display to power-save afterwards
B35.A1.7 | values stay shown, dimmed, never replaced by a dash
B35.A1.8 | yes — the mode alternates throughout the race
B35.A2.screen.1 | the same screens dimmed: thinner and more transparent arc, muted text, nothing moved or resized
B35.A2.screen.2 | values stay shown rather than hidden; B29's fallback rules apply unchanged, at the same 10-second threshold
B35.A2.screen.3 | nothing is in progress; the race keeps running through the mode change
B35.A4.1 | names: power-save mode, the idle tokens, the 10-second refresh, the device's once-a-minute default, the wrist raise, the screen touch, the excluded full brightness
B35.A4.2 | points at B5's dim tokens, B29's freshness, B28's pages — all described
B35.A4.3 | "every 10 seconds rather than once per minute", "dimmed rather than replaced with a dash, a deliberate choice", "forcing full brightness is excluded" — carry their terms

B36.A1.1 | a race running — both paces recompute continuously, allure-segment on RUN segments only
B36.A1.2 | Health Services' distance and speed data, the time since the segment started, the current correction factor
B36.A1.3 | allure-segment, displayed and feeding the lap delta; allure-lissee, never displayed, feeding the trend arrow
B36.A1.4 | allure-segment at the centre of the main page; allure-lissee draws nowhere
B36.A1.5 | no order produced
B36.A1.6 | outside a RUN segment allure-segment is not computed; it resets to zero at every marking
B36.A1.7 | not kept — both are instantaneous, recomputed continuously
B36.A1.8 | yes — every segment starts them afresh
B36.A2.calculation.1 | allure-segment = distance since the segment started ÷ time since it started; allure-lissee = 10-second rolling average of instantaneous speed; both multiplied by the correction factor, then converted to minutes per kilometre
B36.A2.calculation.2 | allure-lissee uses a partial window and falls back under 3 seconds of data; allure-segment falls back under 50 metres covered in the segment
B36.A2.calculation.3 | gap: no bound is given on a computed pace — nothing says what is displayed if the measured distance yields an absurd minutes-per-kilometre value
B36.A3 | not applicable — a running race fires it
B36.A4.1 | names: allure-segment, allure-lissee, the 10-second window, the 3-second floor, the 50-metre floor, Health Services' distance and speed, the accelerometer and stride cadence, the correction factor
B36.A4.2 | points at B37, B39, B41, B28, B29 — all described
B36.A4.3 | "never uses GPS or a location provider", "only ever covers the current segment", "computed only on RUN segments" — carry their terms

B37.A1.1 | the end of each kilometre — a RUN segment being closed
B37.A1.2 | distance_attendue, the distance measured on that RUN segment, the factor in effect
B37.A1.3 | a new k, or a rejection recorded with the race; the corrected pace from the next kilometre on
B37.A1.4 | it draws nothing — only the corrected pace shows, on B28
B37.A1.5 | no order produced
B37.A1.6 | a rejected k_mesuré leaves the factor in effect unchanged
B37.A1.7 | closed segments keep their stored durations — nothing is recalculated
B37.A1.8 | yes — once per kilometre
B37.A2.calculation.1 | k_mesuré = distance_attendue ÷ measured distance; k = 0.6 × k_mesuré + 0.4 × k_précédent; at the first calculation k_précédent is the starting factor of B38; a zero or missing distance produces no factor
B37.A2.calculation.2 | a missing or zero measured distance produces no factor and leaves the one in effect
B37.A2.calculation.3 | gap: k_mesuré is guarded to [0.70, 1.40] but no bound is stated on the blended k that is retained, stored and carried into the next race
B37.A3 | not applicable — the end of a kilometre fires it
B37.A4.1 | names: k_mesuré, k, k_précédent, distance_attendue, the [0.70, 1.40] guard, the recorded rejection, the kilometre number stored with each factor
B37.A4.2 | points at B38's starting value, B36's paces, B19's distance setting — all described
B37.A4.3 | "0.6 against 0.4", "outside [0.70, 1.40]", "never applies retroactively", "shown on no screen" — carry their terms

B38.A1.1 | the end of a race, which updates it; and the start of a race, which reads it
B38.A1.2 | the last factor retained across the whole history
B38.A1.3 | the starting correction factor of the next race
B38.A1.4 | it draws nothing — a factor of 1 is never flagged on screen
B38.A1.5 | a single value, no ordering
B38.A1.6 | if every factor of a race was rejected, the stored value stays unchanged
B38.A1.7 | kept — deleting a race never changes it
B38.A1.8 | yes — updated at the end of every race
B38.A2.persistence.1 | stored in the profile as a single value, not recomputed from history
B38.A2.persistence.2 | when none has ever been retained the value is absent and the starting factor is 1, the pace uncorrected
B38.A3 | not applicable — the start and end of a race fire it
B38.A4.1 | names: the starting factor, the last factor retained, the profile, the value 1, the imported race that never calibrates
B38.A4.2 | points at B37, B14, B10, B36 — all described
B38.A4.3 | "the last factor ever retained, across the whole history", "only watch-recorded races calibrate it" — carry their terms

B59.A1.1 | nothing fires it — a scope statement, consulted; A3 applies
B59.A1.2 | nothing
B59.A1.3 | the exclusion list that bounds every screen
B59.A1.4 | it draws nothing, by definition
B59.A1.5 | no order produced
B59.A1.6 | no trigger, nothing to undo
B59.A1.7 | constant
B59.A1.8 | consulted freely
B59.A2.model.1 | two measures are in scope, pace and heart rate; five things are out: calorie count, step count, displayed stride cadence, altitude, any route or map
B59.A2.model.2 | the exclusion is absolute — none of the five is measured, computed or shown anywhere
B59.A3.1 | in: pace, heart rate. Out: calorie count, step count, displayed stride cadence, altitude, route or map of the course
B59.A3.2 | every screen of both apps
B59.A3.3 | impossible by construction — nothing outside the two is displayed
B59.A3.4 | declared fixed
B59.A4.1 | names: pace, heart rate, calories, steps, stride cadence, altitude, route or map
B59.A4.2 | pace points at B36, heart rate at B18 and B42; stride cadence feeds B36 internally but is never displayed — all described
B59.A4.3 | "the only physiological measures displayed" carries its term; "none of them is measured, computed or shown anywhere" — closed

B39.A1.1 | a RUN segment in progress — it recomputes at the pace's cadence
B39.A1.2 | distance_attendue, allure-segment, the reference's time for that segment, the time already elapsed in it
B39.A1.3 | temps_projeté and the lap delta shown at the top of the main page
B39.A1.4 | the top block of the main page, during a kilometre
B39.A1.5 | no order produced
B39.A1.6 | outside a RUN segment the delta does not exist
B39.A1.7 | not kept — recomputed continuously, replaced at the next segment
B39.A1.8 | yes — each kilometre computes its own
B39.A2.calculation.1 | temps_projeté = distance_attendue ÷ allure-segment; écart = temps_projeté − temps_référence_du_segment; temps_projeté never drops below the time already elapsed
B39.A2.calculation.2 | gap: nothing says what the lap delta shows while allure-segment is in fallback, nor when the reference holds no time for that segment
B39.A2.calculation.3 | a signed duration, floored by the elapsed time, formatted by B48; no upper bound is stated
B39.A3 | not applicable — a RUN segment in progress fires it
B39.A4.1 | names: temps_projeté, écart, distance_attendue, allure-segment, temps_référence_du_segment, the elapsed-time floor
B39.A4.2 | points at B36, B19, B28, B48 — all described
B39.A4.3 | "never drops below the time already elapsed", "only ever uses allure-segment, never allure-lissee", "only on RUN segments" — carry their terms

B40.A1.1 | a race in progress — at every marking, and continuously for the current segment's share
B40.A1.2 | the closed segments' real and reference times, the current segment's elapsed and reference time, the reference times of the segments still to come
B40.A1.3 | écart_cumulé and arrivée, both shown on Projection
B40.A1.4 | the Projection page: delta badge on top, arrival in the centre
B40.A1.5 | no order produced
B40.A1.6 | without a reference both blocks disappear
B40.A1.7 | not kept — recomputed at every marking
B40.A1.8 | yes — at every marking
B40.A2.calculation.1 | gap: écart_cumulé adds "the current segment's own delta", but that delta exists only on RUN segments — nothing gives the current segment's share on a station or a Roxzone
B40.A2.calculation.2 | without a reference the blocks are hidden rather than computed
B40.A2.calculation.3 | gap: écart_cumulé is a signed duration, but nothing says whether arrivée is a projected total duration or a time of day, and no bound is given either way
B40.A3 | not applicable — a race in progress fires it
B40.A4.1 | names: écart_cumulé, arrivée, the closed segments, the current segment's remainder, the segments still to come, the crossover at the reference time
B40.A4.2 | points at B39, B30, B48, B34's final delta — all described
B40.A4.3 | "until that time is exceeded, then its real time once exceeded", "always count their reference time, unweighted" — carry their terms

B41.A1.1 | a RUN segment with both paces available
B41.A1.2 | allure-lissee and allure-segment
B41.A1.3 | an arrow up, an arrow down, or none
B41.A1.4 | the main page, aligned under the "/km" unit
B41.A1.5 | no order produced
B41.A1.6 | at or below a 2% difference no arrow shows
B41.A1.7 | not kept — recomputed with the paces
B41.A1.8 | yes, continuously
B41.A2.calculation.1 | compare allure-lissee to allure-segment: strictly above 2% difference an arrow shows, up when allure-lissee is the faster — the minutes-per-kilometre figure decreasing — down otherwise; at or below 2%, nothing
B41.A2.calculation.2 | no arrow while either pace is in fallback
B41.A2.calculation.3 | three outputs — up, down, none; the 2% boundary belongs to "none"
B41.A3 | not applicable — a RUN segment fires it
B41.A4.1 | names: the arrow, the 2% threshold, allure-lissee, allure-segment, the fallback
B41.A4.2 | points at B36, B28's placement, B2's ahead and behind colours — all described
B41.A4.3 | "at or below 2%", "only strictly above 2%", "faster — that is, the figure decreasing" — carry their terms

B42.A1.1 | a new heart-rate reading arriving
B42.A1.2 | the reading, the four thresholds, the currently active zone
B42.A1.3 | the active zone, and the arc segment drawn active
B42.A1.4 | the zone arc and zone number at the bottom of the race pages
B42.A1.5 | no order produced
B42.A1.6 | without a reading no zone is active
B42.A1.7 | the active zone persists until a reading crosses a shifted boundary
B42.A1.8 | yes — at every reading; after a gap the zone is established anew by the plain thresholds
B42.A2.calculation.1 | up: the boundary plus 3bpm, inclusive; down: 3bpm below that same boundary, inclusive; only the boundary between the active zone and its immediate neighbour is shifted, every other applies plain; a reading two or more boundaries away moves straight to that zone
B42.A2.calculation.2 | no reading, no active zone; on resumption the plain thresholds of B18 apply, then hysteresis again
B42.A2.calculation.3 | output is one zone of 1 to 5, or none while there is no reading; any reading obtained always falls in exactly one
B42.A3 | not applicable — a heart-rate reading fires it
B42.A4.1 | names: the 3bpm shift, the boundary, the active zone, the immediate neighbour, the plain thresholds, the arc segment
B42.A4.2 | points at B18's thresholds, B4's arc, B28's rendering, B29's fallback — all described
B42.A4.3 | "plus 3bpm", "3bpm below that same boundary", "inclusive in both directions", "two or more boundaries away" — carry their terms

B43.A1.1 | the link between the two devices being established, or the sync button on the phone
B43.A1.2 | the profile, the reference race with its 30 segments, the summarized history capped at the 20 most recent races
B43.A1.3 | the watch's state fully replaced, and a success or failure with the date of the last success
B43.A1.4 | the phone's profile screen and the watch's home screen
B43.A1.5 | the history keeps the 20 most recent races; the tie between two races of the same date is not restated here
B43.A1.6 | a refusal while a race runs is treated as an ordinary failure, retried at the next connection established
B43.A1.7 | the watch's previous state is replaced wholesale, never merged
B43.A1.8 | yes — at every connection established, and on demand
B43.A2.synchronisation.1 | no divergence rule is needed: the push replaces, with no merge and no comparison
B43.A2.synchronisation.2 | in progress with "Ne ferme pas l'application", failure with "Réessayer", success with the date — on both devices
B43.A2.synchronisation.3 | gap: nothing says what identifies one same race on both sides, so a renamed or re-designated race cannot be matched to its copy, and the list of changes a mirrored copy follows is never closed
B43.A3 | not applicable — an established link or a button fires it
B43.A4.1 | names: the push, the profile, the reference race in full, the summarized history, the cap of 20, the forcing button, the refusal during a race, the last success date
B43.A4.2 | points at B16, B22, B10's deletion, B19's settings — all described
B43.A4.3 | "capped at the 20 most recent", "the reference itself always goes in full", "fully replaces", "whatever it carries" — carry their terms

B44.A1.1 | the link being established, or a sync forced from the watch
B44.A1.2 | the races recorded by the watch, with their segments
B44.A1.3 | those races stored on the phone, then erased from the watch after its confirmation
B44.A1.4 | the sync states of B16 and B22; a received race appears in the list of B6
B44.A1.5 | the watch keeps its own descending history until erasure
B44.A1.6 | an interrupted transfer resumes from the start; a failed attempt waits for the next link
B44.A1.7 | a race stays on the watch until the phone confirms it was received
B44.A1.8 | yes — at every link established
B44.A2.synchronisation.1 | no divergence: races travel one way only, the phone never sends races to the watch
B44.A2.synchronisation.2 | the same three states as B43 on both devices; a race appears on the phone only once its transfer is complete
B44.A2.synchronisation.3 | gap: nothing identifies a transferred race, so a confirmation lost after storage cannot be told from a transfer never made, and nothing prevents the same race arriving twice
B44.A3 | not applicable — an established link or a forced sync fires it
B44.A4.1 | names: the chunked transfer, the completion condition, the phone's confirmation, the watch's descending history, the retry at the next link
B44.A4.2 | points at B43's push, B34's saved race, B6's list — all described
B44.A4.3 | "only once the transfer is complete", "resumes from the start", "never retried in between" — carry their terms

B61.A1.1 | the connectivity permission being denied, and the check made at every launch
B61.A1.2 | the system's nearby-devices permission state
B61.A1.3 | sync permanently unavailable, a message with "Autoriser" on the profile screen, the sync button inactive
B61.A1.4 | the phone's profile screen, in place of the last-sync date; the watch's home shows "Aucune référence"
B61.A1.5 | no order produced
B61.A1.6 | a later revocation produces the same state as an initial refusal
B61.A1.7 | both apps stay fully usable; nothing else is affected
B61.A1.8 | only through "Autoriser", which re-asks the system or opens the app's permissions page
B61.A2.access.1 | the user alone grants or denies it; the app never asks again automatically
B61.A2.access.2 | without it sync never runs: the phone keeps its races, the watch keeps working with what it already has
B61.A3 | not applicable — a denial and each launch fire it
B61.A4.1 | names: the connectivity permission, the message, "Autoriser", the inactive sync button, "Aucune référence", the check at every launch
B61.A4.2 | gap: the block never says on which device the permission is asked, nor what the watch itself shows about it beyond "Aucune référence"
B61.A4.3 | "exactly as block B20 checks the sensor permission", "stays displayed but inactive", "for as long as it has received nothing" — carry their terms

B45.A1.1 | the preparation screen opening the session; it closes at the end of the race
B45.A1.2 | the sensor data types available on the device, and their readings
B45.A1.3 | one session covering the race and holding the 30 markings; batched readings while the screen is not interactive
B45.A1.4 | it draws nothing itself; a complication on the watch face returns to the app
B45.A1.5 | no order produced
B45.A1.6 | the session closes at the end of the race; leaving the app does not close it
B45.A1.7 | the markings recorded inside it are kept with the race
B45.A1.8 | yes — one session per race, arbitrated at start by B25 and B26
B45.A2.lifecycle.1 | the session lives from the preparation screen to the end of the race; what it produced stays with the recorded race, which travels to the phone and is then erased from the watch
B45.A3 | not applicable — the preparation screen fires it
B45.A4.1 | names: the exercise session, the 30 markings, the one-session-at-a-time rule, the per-data-type availability check, the batches, the complication
B45.A4.2 | gap: the complication is named but nothing says what it displays, nor where its content comes from
B45.A4.3 | "one session covers the whole race", "not as separate sessions", "only one at a time across every app", "in batches rather than continuously" — carry their terms

B60.A1.1 | nothing fires it — a privacy rule consulted wherever heart rate is collected; A3 applies
B60.A1.2 | nothing of its own; it governs the two OS permissions
B60.A1.3 | the rule that no heart-rate data leaves the two devices and that no consent step is added
B60.A1.4 | it draws nothing — the app adds no consent screen
B60.A1.5 | no order produced
B60.A1.6 | no trigger, nothing to undo
B60.A1.7 | constant
B60.A1.8 | consulted freely
B60.A2.access.1 | the user sees her own heart-rate data on both devices; nothing else reads it, and the app adds no step to change that
B60.A2.access.2 | someone refusing the OS permissions gets the fallback of B20 and the hand-filled field of B17
B60.A3.1 | two permissions govern collection — the sensor permission of B20 and the health-history permission of B17; nothing is sent to a server, shared, or exported
B60.A3.2 | every place heart rate is collected, stored or displayed, and the sync between the devices
B60.A3.3 | impossible by construction — the rule has no lookup
B60.A3.4 | declared fixed
B60.A4.1 | names: the sensor permission, the health-history permission, the absent consent step, the no-export rule
B60.A4.2 | points at B20 and B17 — both described
B60.A4.3 | "relies on … alone", "no heart-rate data ever leaves the phone and the watch" — carry their terms

B46.A1.1 | the start of a race and every marking
B46.A1.2 | the monotonic clock, the wall-clock time at the start, the stored opening instant
B46.A1.3 | each segment's measured duration, the atomic transition write, the state a restart resumes from
B46.A1.4 | it draws nothing itself
B46.A1.5 | segments follow their fixed order — no tie
B46.A1.6 | a system clock change has no effect on the race clock
B46.A1.7 | kept — the total is the sum of the segments, never the total minus the others
B46.A1.8 | yes — a restart resumes the current segment from its stored instant
B46.A2.persistence.1 | stored: the wall-clock start recorded once, each segment's measured duration, the current segment's opening instant; the total is recomputed by summing
B46.A2.persistence.2 | a race in progress holds only its closed segments and the current opening instant — the segments not reached hold nothing, not a zero
B46.A3 | not applicable — a start or a marking fires it
B46.A4.1 | names: the monotonic clock, the wall-clock start, the measured duration, the atomic transition, the stored opening instant, the restart
B46.A4.2 | points at B26's resumption, B52's rounding, B27's marking — all described
B46.A4.3 | "unaffected by a system clock change", "always measured, never deduced", "in a single write" — carry their terms

B47.A1.1 | nothing fires it — a format convention, consulted; A3 applies
B47.A1.2 | a duration in milliseconds
B47.A1.3 | the three duration renderings
B47.A1.4 | wherever a duration shows: the list, the detail rows, the race pages, the end screen
B47.A1.5 | no order produced
B47.A1.6 | no trigger, nothing to undo
B47.A1.7 | constant
B47.A1.8 | consulted freely
B47.A2.text.1 | gap: duration-segment m:ss "always under the hour", duration-total h:mm:ss keeping the hour group at zero, duration-elapsed m:ss then h:mm:ss past the hour, none with a leading first-group zero — but nothing says what duration-segment shows if a segment does pass 60 minutes
B47.A2.text.2 | an absent duration shows a dash — B7 for a segment never reached, B29 on the race pages
B47.A3.1 | duration-segment "6:36"; duration-total "0:52:18"; duration-elapsed m:ss under 60 minutes then h:mm:ss
B47.A3.2 | the race list, the detail rows, the race pages, the end screen
B47.A3.3 | impossible by construction — every displayed duration is one of the three
B47.A3.4 | declared fixed
B47.A4.1 | names: duration-segment, duration-total, duration-elapsed, the hour group kept at zero, the absent leading zero
B47.A4.2 | points at B52's truncation, B6 and B7's columns — all described
B47.A4.3 | "always under the hour", "even at zero", "so list columns align", "never 06:36" — carry their terms

B48.A1.1 | nothing fires it — a format convention, consulted; A3 applies
B48.A1.2 | a signed duration in milliseconds
B48.A1.3 | the delta rendering and its colour case
B48.A1.4 | every delta badge and the detail screen's delta column
B48.A1.5 | no order produced
B48.A1.6 | no trigger, nothing to undo
B48.A1.7 | constant
B48.A1.8 | consulted freely
B48.A2.text.1 | a sign then m:ss, the sign always present — "+0:00"; "+" for positive or nil, "−" U+2212 for negative; past the hour still m:ss, "+72:14"
B48.A2.text.2 | an absent delta is never shown as "+0:00": the column stays empty or the block is hidden
B48.A3.1 | one format, three colour cases: ahead when positive, delta-zero at zero, behind when negative
B48.A3.2 | the detail screen's delta column, the main page and Projection badges, the end screen
B48.A3.3 | impossible by construction — a delta is positive, nil or negative
B48.A3.4 | declared fixed
B48.A4.1 | names: the sign, U+2212, "+0:00", "+72:14", the three colours
B48.A4.2 | points at B2's ahead, behind and delta-zero, and at B7, B28, B30, B34 — all described
B48.A4.3 | "even at zero", "never the ASCII hyphen", "colour, not a different format, distinguishes the three cases" — carry their terms

B49.A1.1 | nothing fires it — a format convention, consulted; A3 applies
B49.A1.2 | a pace, a heart rate, a position, a zone number
B49.A1.3 | their renderings, each with its detached unit
B49.A1.4 | the main page, Projection, the profile's zone rows
B49.A1.5 | no order produced
B49.A1.6 | no trigger, nothing to undo
B49.A1.7 | constant
B49.A1.8 | consulted freely
B49.A2.text.1 | pace m:ss with a detached "/km"; hr an integer with a detached "bpm"; position "n/30" without spaces; zone "Zone n"
B49.A2.text.2 | without a reading the heart rate shows a dash (B28) and the zone row is hidden (B54)
B49.A3.1 | the four formats above, plus the rule that a unit is always its own element, smaller and in text-secondary
B49.A3.2 | the race pages and the profile screen
B49.A3.3 | impossible by construction — the four cover every value they format
B49.A3.4 | declared fixed
B49.A4.1 | names: pace, "/km", hr, "bpm", the position "n/30", "Zone n", the detached unit
B49.A4.2 | points at B3's sizes, B2's text-secondary, B28's placement — all described
B49.A4.3 | "smaller and in text-secondary", "never concatenated to the value", "no spaces" — carry their terms

B50.A1.1 | nothing fires it — a format convention, consulted; A3 applies
B50.A1.2 | a zone percentage, a zone range, a distance, a press duration
B50.A1.3 | their renderings
B50.A1.4 | the profile screen's zone rows and setting rows
B50.A1.5 | no order produced
B50.A1.6 | no trigger, nothing to undo
B50.A1.7 | constant
B50.A1.8 | consulted freely
B50.A2.text.1 | "50 %" with a non-breaking space; "94–112 bpm" with an en dash; "< 94 bpm" and "> 150 bpm" with a space after the operator; "1000 m" with no thousands separator; "700 ms"
B50.A2.text.2 | while the maximum heart rate is unknown the ranges are hidden rather than formatted (B18)
B50.A3.1 | the five formats above, each with its worked form
B50.A3.2 | the profile screen only
B50.A3.3 | impossible by construction — every value it formats is one of the five
B50.A3.4 | declared fixed
B50.A4.1 | names: the percentage, the range, the two extreme forms, the distance, the press duration
B50.A4.2 | points at B16's rows, B18's ranges, B19's bounds — all described
B50.A4.3 | "an operator and a space", "no thousands separator" — carry their terms

B51.A1.1 | nothing fires it — a format convention, consulted; A3 applies
B51.A1.2 | a date, and optionally a time
B51.A1.3 | the three date renderings
B51.A1.4 | the race cards, the detail header, the watch history, the last-sync line, the watch's generated names
B51.A1.5 | no order produced
B51.A1.6 | no trigger, nothing to undo
B51.A1.7 | constant
B51.A1.8 | consulted freely
B51.A2.text.1 | gap: "12 avr. 2026", then " · " and "h:mm" for a date with time — but the worked form "09:14" carries a leading zero that "h:mm" and B47's no-leading-zero rule both deny
B51.A2.text.2 | before any successful sync the last-sync line reads "Jamais synchronisé" (B54)
B51.A3.1 | day, abbreviated month, year; the same with " · " and the time; the relative form "aujourd'hui à 09:02" when the date falls today
B51.A3.2 | the race list, the detail header, the watch history, the profile's last-sync line, the watch's generated race names
B51.A3.3 | impossible by construction — every date shown takes one of the three forms
B51.A3.4 | declared fixed
B51.A4.1 | names: "12 avr. 2026", "12 avr. 2026 · 09:14", "aujourd'hui à 09:02", the abbreviated month
B51.A4.2 | points at B55's relative wording, B54's generated name, B16's last-sync line — all described
B51.A4.3 | "when it falls today" carries its term — closed

B52.A1.1 | nothing fires it — a rounding convention applied at every display; A3 applies
B52.A1.2 | a duration in milliseconds, or two cumulative totals
B52.A1.3 | the displayed second, and the displayed segment duration
B52.A1.4 | every displayed duration and delta
B52.A1.5 | no order produced
B52.A1.6 | no trigger, nothing to undo
B52.A1.7 | the stored milliseconds are never altered
B52.A1.8 | consulted freely
B52.A2.calculation.1 | truncate to the second, never round; a segment's displayed duration is the difference of two truncated cumulative totals; a delta is computed on milliseconds and truncated only at display
B52.A2.calculation.2 | a missing duration is not truncated — it shows a dash
B52.A2.calculation.3 | output is a whole second, never negative for a duration, signed for a delta; the displayed segments always sum to the displayed total
B52.A3.1 | truncation to the second, everywhere, with no exception
B52.A3.2 | every screen showing a duration or a delta
B52.A3.3 | impossible by construction — every stored value is a millisecond count
B52.A3.4 | declared fixed
B52.A4.1 | names: the millisecond storage, the truncation, the two truncated cumulative totals, the displayed total
B52.A4.2 | points at B47, B48, B7's columns — all described
B52.A4.3 | "by truncation, never by rounding", "never by truncating the segment's own duration", "otherwise the segments would not sum to the displayed total" — carry their terms

B53.A1.1 | nothing fires it — a resourcing rule, consulted; A3 applies
B53.A1.2 | every visible string of both apps
B53.A1.3 | the rule: resource files, one language, separate files per device, parameters rather than concatenation
B53.A1.4 | it governs every screen and occupies none
B53.A1.5 | no order produced
B53.A1.6 | no trigger, nothing to undo
B53.A1.7 | constant
B53.A1.8 | consulted freely
B53.A2.text.1 | it carries no label of its own — it rules that no visible string is hard-coded and that every interpolated value is a resource parameter
B53.A2.text.2 | not applicable — it holds no value that could be absent
B53.A3.1 | a single language, French; no other locale and no switching mechanism; phone and watch keep separate files, a key present on both is duplicated
B53.A3.2 | every screen of both apps
B53.A3.3 | impossible by construction — the catalogues of B54 and B56 close the set of strings
B53.A3.4 | declared fixed
B53.A4.1 | names: the resource file, French, the absent locale switch, the duplicated key, the resource parameter
B53.A4.2 | points at B56's catalogue and B54's dynamic texts — both described
B53.A4.3 | "never shared", "never concatenated into the string" — carry their terms

B54.A1.1 | nothing fires it — a catalogue of dynamic texts and their fallbacks, consulted; A3 applies
B54.A1.2 | the interpolated values: the reference's name, the closed segment, the sync date, the race name, the zone number
B54.A1.3 | each text with its value, or its stated replacement
B54.A1.4 | the watch home, the preparation screen, Control, the profile, the delete confirmation, the race pages, the rename field
B54.A1.5 | no order produced
B54.A1.6 | no trigger, nothing to undo
B54.A1.7 | constant
B54.A1.8 | consulted freely
B54.A2.text.1 | "Réf. — <nom>", "Référence chargée · <nom>", "Annuler : <segment fermé>", "Dernière synchronisation réussie : <date>", "Supprimer « <nom> » ?", "Zone <n>"
B54.A2.text.2 | no reference: the "⚠ Aucune référence" badge replaces the first and the second's line hides; before the first marking the undo button is disabled; before any success "Jamais synchronisé"; without a reading the zone row hides; a name is never empty
B54.A3.1 | the six dynamic texts with their fallbacks, plus the name rules: never empty once trimmed, 40 characters at entry, truncated with an ellipsis on a single line when displayed, auto-generated on the watch as "12 avr. 2026 · 09:14"
B54.A3.2 | the watch home, the preparation screen, Control, the profile, the delete confirmation, the race pages, the rename field
B54.A3.3 | impossible by construction — every dynamic text states its own fallback
B54.A3.4 | declared fixed
B54.A4.1 | names: the six dynamic texts, the eight failure titles of B15, the name rules, the watch-generated name, the ellipsis
B54.A4.2 | points at B15's catalogue, B51's format, B9's field, B22's badge — all described
B54.A4.3 | "replaced entirely", "hides its line", "never empty", "truncated at the end, never wrapped onto more than one line", "no generic catch-all beyond them" — carry their terms

B55.A1.1 | nothing fires it — a wording convention for relative dates, consulted; A3 applies
B55.A1.2 | a date and time, compared with today
B55.A1.3 | one of three wordings
B55.A1.4 | the profile's last-sync line
B55.A1.5 | no order produced
B55.A1.6 | no trigger, nothing to undo
B55.A1.7 | constant
B55.A1.8 | consulted freely
B55.A2.text.1 | "aujourd'hui à 09:02", "hier à 09:02", "14 sept. 2025 à 09:02"
B55.A2.text.2 | before any sync the line reads "Jamais synchronisé" (B54)
B55.A3.1 | today, yesterday, anything earlier — the three wordings above
B55.A3.2 | the profile screen's last-sync line
B55.A3.3 | impossible by construction — the three cases cover every date
B55.A3.4 | declared fixed
B55.A4.1 | names: "aujourd'hui", "hier", the full date and time, the "à" separator
B55.A4.2 | points at B51's date format and B16's line — both described
B55.A4.3 | "anything earlier" carries its term — closed

B56.A1.1 | nothing fires it — the fixed string catalogue, consulted; A3 applies
B56.A1.2 | nothing
B56.A1.3 | the exact wording of every fixed text of both apps
B56.A1.4 | every screen named in the catalogue
B56.A1.5 | no order produced
B56.A1.6 | no trigger, nothing to undo
B56.A1.7 | constant
B56.A1.8 | consulted freely
B56.A2.text.1 | the wordings are given verbatim, screen by screen, in three groups: the watch outside the race, the watch during the race, the phone
B56.A2.text.2 | not applicable — these texts carry no interpolated value; the dynamic ones belong to B54
B56.A3.1 | watch out of race: permission, refused-permission reminder, waiting for the phone, home, empty history, preparation; watch in race: Projection, Control, stop confirmation, resume-activity dialog, end; phone: list, empty list, detail, delete confirmation, rename, paste, preview, error plus "Revenir au collage", profile, sync — all as quoted in the block
B56.A3.2 | every screen block, which names its texts by their place rather than repeating them
B56.A3.3 | impossible by construction — a screen showing a text absent here would fall outside the catalogue
B56.A3.4 | declared fixed
B56.A4.1 | names: every quoted string of the three groups, settled verbatim here
B56.A4.2 | points at B15's eight titles and at each screen block — all described
B56.A4.3 | no comparison is made — the catalogue states its values outright

B57.A1.1 | any navigation action on the phone
B57.A1.2 | the current screen, the action taken, the stack behind it
B57.A1.3 | the destination screen, and the stack as it stands after a successful save
B57.A1.4 | it governs the phone's screens and occupies none of its own
B57.A1.5 | no order produced
B57.A1.6 | the back gesture steps back one screen at a time, in reverse of the path taken
B57.A1.7 | after a successful save the paste screen and the preview leave the stack
B57.A1.8 | yes — the map holds for every pass through it
B57.A2.journey.1 | a card opens its detail; the profile icon opens the profile, whose "Synchroniser" acts on the spot; "+" or the empty list's button opens paste; "Importer" leads to the preview on success or the error screen on failure; "Corriger" and "Revenir au collage" return to paste; "Enregistrer" opens the new race's detail
B57.A2.journey.2 | back steps one screen at a time; from the imported race's detail it returns directly to the list, the paste screen and the preview having left the stack
B57.A3 | not applicable — a user action fires it
B57.A4.1 | names: the list, the detail, the profile, the paste screen, the preview, the error screen, the back gesture, the stack after saving, the three detail actions
B57.A4.2 | points at B6, B7, B11, B13, B15, B16, B8, B9, B10 — all described
B57.A4.3 | "in reverse of the path taken", "except that after a successful save" — carry their terms

B58.A1.1 | any navigation action on the watch
B58.A1.2 | the current screen, the gesture, whether a race is running
B58.A1.3 | the destination screen, or the gesture ignored
B58.A1.4 | it governs the watch's screens and occupies none of its own
B58.A1.5 | the race pages chain forward only: main page, Projection, Control
B58.A1.6 | outside a race and on the preparation screen the back gesture works normally; during a race it is disabled everywhere
B58.A1.7 | a running race is never left by a gesture — the stop action is the only way out
B58.A1.8 | yes — the map holds at every launch
B58.A2.journey.1 | first launch: permission, then waiting for the phone, then home; "Démarrer" opens the preparation, "Lancer" the race, intercalated by the conflict dialog only when another app holds the sensor; "Historique" opens the list; "Synchroniser" acts on the spot; a long press or 8 idle seconds returns to the main page; Control's undo returns to the main page, its stop opens a confirmation then the end screen; the 30th marking opens the end screen; "Terminer" returns home
B58.A2.journey.2 | the back gesture is disabled on the main page, Projection, Control and the end screen; "Quitter" leaves the preparation; no page answers a leftward swipe
B58.A3 | not applicable — a user action fires it
B58.A4.1 | names: the three race pages, the rightward swipe, the disabled back gesture, the two conditional screens, "Quitter", "Terminer", the 8-second return
B58.A4.2 | points at B20, B21, B22, B24, B25, B27, B31, B33, B34 — all described
B58.A4.3 | "forward only", "no page answers a leftward swipe", "only as long as no profile has ever been received", "only if another app occupies the sensor" — carry their terms

B1.1 | gap: the insertion rank B6 sorts on is consumed by no other block and produced by none — nothing says a race stores its creation instant; every other input has a named origin, external or internal (health history B17, Health Services distance and speed B36, the pasted text B12, the system permissions B20/B61)
B1.2 | gap: the last-sync date is written by B43's push, but B44's pull is a sync too and B22 shows one result for both — and its relative wording is ruled twice, B51 giving only "today" where B55 adds "hier" and the full form
B1.3 | gap: the kilometre number B37 stores with each retained factor is read by no block; B37's recorded rejections are declared internal and kept for later analysis, so they alone are written for nobody by design
B1.4 | gap: B38's correction factor is updated in the profile at the end of every watch race, yet B44 sends only races up to the phone and B43's push "fully replaces the watch's state" — the factor a race calibrated is overwritten by the phone's own value at the next push
B1.5 | gap: on the watch's first screen three blocks claim the same area — B21 replaces the home screen with "En attente du téléphone" until a profile is received, B22 shows the home with a "⚠ Aucune référence" badge, and B61 says the watch shows "Aucune référence" for as long as it has received nothing
B1.6 | see B2.1 — the names gathered across the blocks are crossed there
B2.1 | gap: two names carry two values — the sync failure sentence reads "approche le téléphone de la montre." in B22 and "approche la montre du téléphone." in B56, and the sensor-conflict dialog is titled "Reprise d'activité en cours" in B25's rendering and "Une autre activité est en cours" in B56

C1.1 | only from now on, and stated three times: B19 freezes a recorded race's durations, factor and heart-rate measurements, B37's factor never recalculates a closed segment, B52 fixes display only
C1.2 | out of scope though one might think them in: calories, steps, displayed stride cadence, altitude, route or map (B59); GPS and any location provider (B36); file import (B11); segment detail on the watch, and any rename, delete or reference change from it (B23); a second language (B53); forced full brightness (B35) — gap: nothing says whether backing up, exporting or moving the races to a new phone is in or out
C1.3 | no pre-existing rule is touched: this document describes the whole application, first delivery, and every rule it names is defined in it
C1.4 | terms to settle before writing: segment against station and cycle (B1), reference race against reference time of a segment (B8/B39), incomplete (B33 stopped early, B7 segments never reached), marking (B27), allure-segment against allure-lissee (B36), lap delta against cumulative delta and final delta (B39/B40/B34), correction factor k against starting factor (B37/B38), push against pull (B43/B44) — all defined in the document
C1.5 | displayed terms are the product's, in French, from resource files (B53); the internal names — allure-segment, allure-lissee, distance_attendue, k_mesuré, k_précédent, temps_projeté, écart_cumulé, RUN, and every design token — appear on no screen
C1.6 | health data: heart rate and the phone's health history, governed by the OS permissions alone with no consent step of the app's own, never leaving the two devices (B60, B17, B20). Location: none collected — no GPS, no location provider, no route or map (B36, B59). Biometrics: none beyond heart rate. gap: identifiers are never addressed — nothing says whether pairing the phone and the watch stores a device identifier, or whether any account or user identity exists
C1.7 | gap: three permissions are named with a permanent-denial path each — the watch's sensor permission (B20: heart rate and arc in permanent fallback, clock and segments unaffected), the phone's health-history permission (B17: HR max filled by hand, zone ranges hidden), the connectivity permission (B61: sync permanently unavailable, both apps usable) — but B36 draws distance and speed from Health Services, and nothing says whether that needs a permission of its own nor what a race becomes if it is refused

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
