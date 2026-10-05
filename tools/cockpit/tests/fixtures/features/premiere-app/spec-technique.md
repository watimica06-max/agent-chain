# Technical document — premiere-app

> Produced from `desc-par-nature.md` and `desc-produit.md`. Preamble
> frames the work; sections §1–§12 are what the Cadreur cuts into lots.

## Preamble

### Intent

Two companion apps track a solo Hyrox race: a phone app that stores
race history and a Wear OS watch app that records a race live, the two
kept in sync. A race breaks down into 30 timed segments (§1.1); the
watch measures them as they happen, the phone also accepts an official
result pasted from the hyresult website (§5.1). Every race can be
compared, segment by segment, against a designated reference race.

### Out of scope

Pace and heart rate are the only physiological measures ever computed
or displayed. Calorie count, step count, displayed stride cadence,
altitude, and any route or map of the course are never measured,
computed or shown anywhere in either app. *(product: B59)*

### Cross-cutting rules

None declared valid everywhere beyond what each section states on its
own subject.

### Dependencies

None. This is the feature's first build; no existing element is
referenced.

---

## §1 Model

### §1.1 Race and segment structure

A `Race` is divided into 30 ordered `Segment`s, indexed 1–30, following
a fixed 8-station Hyrox sequence: SkiErg, Sled Push, Sled Pull, Burpee
Broad Jump, Row, Farmers Carry, Sandbag Lunges, Wall Balls.

Segments group into 8 cycles. Cycles 1–7 hold 4 segments each, in
order: `RUN` (the kilometre), `ROXZONE_OUT` (transition toward the
station), `STATION`, `ROXZONE_IN` (transition back toward the track)
— indices 1–4, 5–8, …, 25–28. Segment 29 is the 8th `RUN`. Segment 30
is a `FINAL` segment combining the Roxzone, Wall Balls and the finish
sprint into one measured block.

Each segment carries a `durationMs` and a `cumulativeMs` (§3.7 for how
the displayed value is derived from these). A segment never reached
carries neither. This breakdown matches the official race clock
exactly: an imported race (§5.1) and a watch-recorded race (§4.3) are
comparable segment by segment, with no reconstruction step between the
two sources.

### §1.2 Design tokens

One shared token set — colors, typography, shapes/spacing, and their
idle-mode variants — feeds every screen section (§9) by name. It ships
once per platform (phone dp-based, watch px-based) and needs no rule
to derive its values; §9 subsections reference it by token name rather
than repeating values.

**Color** — `surface`, `surface-raised` (phone backgrounds),
`screen-black` (watch OLED background); `text-primary`, `text-body`,
`text-secondary`, `text-tertiary` (decreasing emphasis); `border`,
`border-strong`; `ahead` / `ahead-text` / `ahead-bg` (lead over
reference), `behind` / `behind-text` / `behind-bg` (deficit),
`delta-zero` (no difference); `link`; `zone-1`…`zone-5` (heart-rate
zones, blue-to-red).

| Token | Value | Token | Value |
|---|---|---|---|
| surface | #121110 | ahead | #4FAE72 |
| surface-raised | #1C1A18 | ahead-text | #7FCB9C |
| screen-black | #000000 | ahead-bg | rgba(79,174,114,0.16) |
| text-primary | #F3EFE7 | behind | #E2725F |
| text-body | #C9C4BA | behind-text | #E2957F |
| text-secondary | #9A958C | behind-bg | rgba(226,114,95,0.16) |
| text-tertiary | #6F6A62 | delta-zero | #726D63 |
| border | rgba(255,255,255,0.08) | link | #6FA3D8 |
| border-strong | rgba(255,255,255,0.25) | zone-1…zone-5 | #4A90D9, #35B0A4, #4CAF63, #E0A23A, #E0503F |

`ahead` and `behind` never render alone: a sign (§10.1) and a trend
arrow (§3.6) always accompany them.

**Typography** — two families: `font-label` (IBM Plex Sans; labels,
titles, running text) and `font-data` (IBM Plex Mono, tabular figures;
every timed value, always weight 700, any size). Three weights only:
700 (titles, values, button labels), 600 (secondary labels, menu
entries), 500 (detached units, low-emphasis actions).

Watch scale (px, 480×480 face): `w-display` 110, `w-display-sm` 80,
`w-value` 48, `w-value-sm` 40, `w-badge` 37, `w-title` 33, `w-label`
24, `w-label-sm` 20, `w-caption` 18.

Phone scale (dp): `p-title` 22, `p-value` 20, `p-body` 15, `p-label`
13, `p-data` 12.5, `p-caption` 11.

Letter-spacing: 0.04em on normal-size uppercase labels (including the
zone number, §9.12); 0.06em on group headers and small-size uppercase
mentions (cycle header §9.2, station name §9.12, "arrivée estimée"
§9.13, watch out-of-race titles); 0.08em on the Control title (§9.14).
Running text and any `font-data` value carry no letter-spacing.

**Shape and spacing** — `radius-pill` (half the element's height;
primary buttons, badges), `radius-card` 12 (cards, panels, fields),
`radius-chip` 14 (delta badges). Spacing scale `space-xs/s/m/l/xl` =
4/8/12/20/32. Expressed in dp on the phone; multiplied by 1.83 on the
watch to stay within its 480×480 frame.

Zone arc geometry (watch only, consumed by §9.12): `arc-radius` 229px
(95% of screen radius), `arc-span` 140° total, centered on the bottom
of the face, `arc-segment` 25.6° per zone, `arc-gap` 3° between zones,
`arc-width` 13px (inactive), `arc-width-active` 33px (active),
`arc-opacity-idle` 0.30, `arc-opacity-active` 1. The active segment's
radius = `arc-radius` + `arc-width`/2 − `arc-width-active`/2 (thickens
inward, outer edge aligned with the others).

Target device: Galaxy Watch Ultra, 1.5″ round 480×480 OLED, Wear OS 5
/ One UI Watch 6, upgradable to Wear OS 6.

**Idle display variants** (power-save mode, consumed by §9.16):
`dim-text` — opacity only, never a color change: 0.55 on
`text-primary` and any timed value, 0.45 on `text-secondary` and
`text-tertiary`; `ahead`/`behind`/`delta-zero` keep hue, take 0.55
opacity. `arc-width-dim` 7 (vs 13), `arc-width-active-dim` 22 (vs 33),
`arc-opacity-idle-dim` 0.25 (vs 0.30) — the arc thins and darkens, it
never changes geometry beyond width.

### §1.3 Sensor-derived value freshness

Any sensor-derived displayed value (heart rate §9.12, pace §9.12)
carries a 10-second freshness window, in both normal and power-save
display mode (the same 10s matches the power-save refresh cadence of
§9.16). Past 10 seconds without a new reading, the value returns to
its fallback state rather than keeping its last reading. A fallback
state is never an error — no message, no interruption — and renders
as a dash (§9.12), never as zero: a `+0:00` delta means "tied," not
"unknown" (§10.1's delta format). The race clock itself carries no
freshness window — it is always available (§2.3).

---

## §2 Persistence

### §2.1 Race record operations

`Race` fields: `id`, `name` (string, 1–40 chars trimmed, never empty
— §10.3's name rule), `date`, `origin` (`imported` | `recorded`),
`isReference` (bool), `completion` (`complete` | `incomplete` —
watch-recorded only; an imported race is always `complete`), 30
`Segment`s (§1.1), `retainedFactors[]` and `rejectedCalibrations[]`
(§3.3), and, while `origin = recorded` and not yet ended, the
in-progress fields of §2.3.

**Set as reference** — writing `isReference = true` on one race clears
it on whichever race previously held it; at most one race is the
reference at a time. Consumes §9.2's visibility rule for when the
control that triggers this is shown.

**Rename** — writes `name`, validated by §10.3's name rule (1–40 chars
trimmed, never empty).

**Delete** — removes the `Race` record. The only entry point is §9.2's
detail screen. Deleting the reference race clears `isReference`
app-wide with no automatic replacement — the app falls back to a
"no reference" state (consumed by §9.1, §9.9, §9.12, §9.13, §9.15,
§9.18). The deletion propagates to the watch at the next push (§6.1).

**Save an imported race** — creates a new `Race` with `origin =
imported`, `completion = complete`, and all 30 `Segment.durationMs`
values from §5.1's reading. The recognized total time and segment
count of §5.1/§9.4 are not stored; the race's total is always the sum
of its segments. No factor is retained for this race (§3.3 runs on
`recorded` races only). No uniqueness constraint on `name` — two races
may share one, distinguished by `date` in §9.1's list.

### §2.2 Profile persistence

Single `Profile` record, fields: `hrMaxBpm` (int, 100–230, unset until
derived by §5.2 or entered by hand), `zoneThresholds[4]` (int %,
30–99, strictly increasing, default 60/70/80/90 — §3.1),
`expectedDistanceM` (int, 500–2000, default 1000), `longPressMs`
(int, 300–2000, default 700), `correctionFactor` (float, §3.3's
starting `k`, default 1, updated at the end of every `recorded` race),
`lastSyncSuccessAt` (nullable timestamp, consumed by §9.6, §9.9).

Editing `hrMaxBpm`, one `zoneThresholds` entry, `expectedDistanceM` or
`longPressMs` validates and writes the new value; on any bound
violation, non-integer input, or a threshold order break, the field
reverts to its previous value and §10.1's constraint message shows.

None of these apply retroactively — a saved `Race`'s segments,
retained factors and heart-rate readings are frozen. Each setting
takes effect from the next `recorded` race onward: `hrMaxBpm` and
`zoneThresholds` feed §3.1 (zone arc, §9.12), `expectedDistanceM` feeds
§3.3 and §3.4, `longPressMs` feeds §4.3. A setting changed on the
phone without a sync (§6.1) leaves the watch working with its
previous copy.

`correctionFactor` updates only when §3.3 retains at least one factor
during a `recorded` race; if every candidate that race computed was
rejected, the stored value is unchanged. Deleting a race (§2.1) never
changes it. A value of 1 carries no visible flag (§9.6).

### §2.3 Race clock persistence and recovery

The race clock is monotonic — unaffected by a system clock change —
and the wall-clock start time is written once, at the race's start.
Each `Segment.durationMs` is measured directly, never derived by
subtracting the others from the total. Closing a segment and opening
the next are one atomic write.

While `origin = recorded` and the race has not ended, the `Race`
record additionally carries `currentSegmentIndex` and
`currentSegmentOpenedAt`, written at the instant of every marking
(§4.3). On an app restart mid-race, the segment resumes counting from
`currentSegmentOpenedAt` rather than restarting (consumed by §4.2's
resume path).

---

## §3 Calculation

### §3.1 Heart-rate zone determination

Four thresholds (`zoneThresholds[4]`, §2.2) bound five zones: zone *n*
runs from threshold *n* (included) to threshold *n+1* (excluded); zone
5 covers everything above the fourth threshold; zone 1 everything
below the first. Defaults 60/70/80/90% of `hrMaxBpm`. Example at
`hrMaxBpm = 187`: zone 1 < 112, zone 2 [112, 130], zone 3 [131, 149],
zone 4 [150, 167], zone 5 ≥ 168. Every heart-rate reading obtained
falls in exactly one zone — there is no reading without a zone.

Switching zone applies hysteresis: moving to the zone above requires
reaching its boundary + 3bpm; moving back down requires dropping to
3bpm below that same boundary — inclusive both ways. The shift applies
only to the boundary between the active zone and its immediate
neighbor; every other boundary uses its plain threshold. When a
reading resumes after a gap with none, the zone is re-established from
the plain thresholds, with no hysteresis for that first reading;
hysteresis resumes on the readings after it. A reading landing two or
more zones away from the active one jumps the displayed zone directly
there, without crossing the zones in between.

Without a heart-rate reading (permanently, per §4.1's fallback, or
before the first reading of a race), no zone is active — rendered per
§9.12/§1.2's idle arc style, value shown as a dash (§1.3).

### §3.2 Pace calculation

`allure-segment` = distance covered since the current segment started
÷ time elapsed since it started. Displayed at the center of §9.12's
main page and the base of §3.4's lap delta. Resets to zero at every
marking (§4.3) — it only ever covers the current segment — and is
computed only on `RUN` segments. Falls back under 50m covered in the
segment.

`allure-lissee` = a 10-second rolling average of instantaneous speed.
Never displayed; feeds only §3.6's trend arrow. Uses whatever data is
available while its 10s window is not yet full; falls back under 3s of
data.

Both are multiplied by the current correction factor `k` (§3.3) before
conversion to min/km. Neither ever uses GPS or a location provider:
distance comes from Health Services' distance/speed data types,
themselves derived from the watch's accelerometer and stride cadence
(§5.3).

### §3.3 Correction factor

At the end of each kilometre (`RUN` segment closing): `k_mesuré =
expectedDistanceM ÷ distance measured on that segment`; `k = 0.6 ×
k_mesuré + 0.4 × k_précédent`, where `k_précédent` is the factor in
effect before this kilometre — `Profile.correctionFactor` (§2.2) at
the first calculation of a race.

A `k_mesuré` outside [0.70, 1.40] is rejected: the factor in effect is
kept unchanged, and the attempt is appended to
`Race.rejectedCalibrations[]` (§2.1) — kilometre number and the
rejected `k_mesuré` value — an internal record only, shown on no
screen, kept to allow re-analysing a calibration afterward. A zero or
missing measured distance produces no candidate at all — the previous
factor carries forward unchanged into the next kilometre's
`k_précédent`.

The factor never applies retroactively: a closed segment's stored
`durationMs` is never recalculated; only the displayed pace (§3.2)
corrects from the next kilometre on. Each retained factor is appended
to `Race.retainedFactors[]` (§2.1) with the kilometre number it came
from, and also overwrites `Profile.correctionFactor` (§2.2) so the
next race starts from it. An imported race (§2.1) never runs this
calculation.

### §3.4 Lap delta

`temps_projeté = expectedDistanceM ÷ allure-segment` (§3.2);
`écart = temps_projeté − temps_référence_du_segment` (the reference
race's stored duration for this segment index, §1.1/§2.1). Recomputes
continuously at pace-refresh cadence, using `allure-segment` only,
never `allure-lissee`. `temps_projeté` never drops below the time
already elapsed in the segment. Exists only on `RUN` segments —
consumed by §9.12 (kilometre display state) and §3.5.

### §3.5 Cumulative delta and estimated arrival

`écart_cumulé` = Σ(real time − reference time) over closed segments,
plus the current segment's own delta (§3.4 on a `RUN` segment; real
time minus reference time once the reference time is exceeded, the
reference time's own count until then, on any other segment type).

`arrivée` = elapsed time + remainder of the current segment + Σ
reference times of segments still to come (each counted unweighted,
i.e. at its stored reference duration). Both recompute at every
marking (§4.3), the current segment's own share recomputing
continuously. Consumed by §9.12 (top block), §9.13 (Projection page)
and §9.15 (end-of-race final delta).

### §3.6 Trend arrow

Compares `allure-lissee` to `allure-segment` (§3.2). At or below a 2%
difference, no arrow shows; strictly above 2%, it shows — pointing up
when `allure-lissee` is faster (the min/km figure decreasing), down
otherwise. No arrow while either pace is in fallback. Consumed by
§9.12.

### §3.7 Duration and delta truncation

Durations are stored in milliseconds (§2.1, §2.3) and displayed to the
second by truncation, never rounding. A segment's displayed
`durationMs`-derived value is the difference between two truncated
cumulative totals, never a truncation of the segment's own raw value —
otherwise displayed segments would not sum to the displayed total. A
delta is computed on millisecond values and truncated only at the
point of display. Consumed by §9.2, §9.12, §9.13, §9.15, §10.1.

---

## §4 Transition

### §4.1 Sensor permission (watch)

On first launch, the watch requests sensor access once, showing
§10.4's explanation. A refusal leaves the app usable: the clock,
segments and deltas keep working (§4.3, §9.12); heart rate and the
zone arc (§3.1, §9.12) stay permanently in fallback. Checked again at
every subsequent launch; a later revocation from system settings
produces the same fallback. Never auto-repeated after a refusal or
revocation: §9.9's home-screen reminder re-requests it, or — if the
system no longer offers that request — opens the app's own permissions
page in system settings.

### §4.2 Race launch sequence

Tapping "Démarrer" (§9.9) opens the preparation screen (§9.11): the
exercise session opens (§5.3), sensors warm up, heart rate shows
during the wait, and the app checks whether a reference is loaded.
"Quitter" closes it, returning to §9.9. Tapping "Lancer" starts the
monotonic clock (§2.3) and opens segment 1; nothing is recorded before
the clock starts.

If opening the exercise session fails, the preparation screen stays
displayed with heart rate in fallback and "Lancer" stays active;
tapping it retries the open. A second failure starts the race without
sensor data for its whole duration — no further retry once running.

If another app already holds the device's single exercise-session slot
when the race starts, §9.11's sensor-conflict dialog asks for
confirmation, naming that the other activity will be stopped.
Continuing stops it and starts ours; canceling returns without
starting.

If the exercise session already active at start belongs to our own
race (the app restarted mid-race), the race resumes from
`Race.currentSegmentIndex` / `currentSegmentOpenedAt` (§2.3) instead of
restarting; the sensor session itself is not restarted either.

### §4.3 Marking a segment

The whole screen is the advance control on every race page except
Control (§9.14): a long press of at least `Profile.longPressMs`
(§2.2, default 700ms) anywhere marks the current segment finished and
opens the next. The segment's `durationMs` boundary is taken at
touch-down, not release. Releasing before the threshold cancels the
marking, writing nothing. A slide of more than 20px during the press
cancels the marking too, becoming a page swipe instead (§8). No
minimum delay between two markings.

Vibration: one short pulse confirms a marking taken into account, two
short pulses signal a cancellation, nothing plays during the press
itself. Auto-return to the main page after a marking, and after 8s of
inactivity on a secondary page, is §8.1's rule.

### §4.4 Undoing the last marking

Tapping §9.14's undo control reopens the segment the last marking
closed, restoring it to in-progress; the control names that segment
(§10.3's dynamic label). Single-level — only ever touches the most
recent marking — with no time limit. Disabled before the race's first
marking (§9.14).

### §4.5 Stopping the race

Tapping §9.14's stop control opens a confirmation (§9.14). Confirming
cuts the clock and every measurement and saves the race as it stands
with `completion = incomplete` (§2.1); an incomplete race can never
hold `isReference = true` (§2.1). Leaving the app does not stop the
running exercise session — only this action does. Ends on §9.15's
screen.

---

## §5 External source

### §5.1 Parsing and validating a pasted result

Reads the text pasted into §9.3's field as hyresult's official export:
4 columns, in the order — segment label (header "Split"), time of day
(header "Time of Day"), cumulated time (header "Time"), segment
duration (header "Diff") — separated by a tab or by a run of multiple
spaces (station names themselves contain single spaces). Parsing is
positional, never by header name. A row with fewer than 4 columns is a
reading error.

The first row is skipped as a header when its 4th column does not
parse as a time value; a second row with the same defect is a reading
error, not a second skip. The number of time components in a value
sets its scale (2 = m:ss, 3 = h:mm:ss); the time column may switch
scale partway through the table. The race's start time = first row's
time-of-day − its diff.

Reading runs a state machine over the 7-cycle pattern, never a label
search: the label "Rox In" appears identically 7 times and identifies
the kilometre row closing cycles 1–7 (entry into the Roxzone; the
cycle number comes from the station name that follows it); "Wall
Balls In" identifies kilometre 8's row and switches the machine to its
terminal mode. Station labels map to §1.1's segment names via a fixed
table, never string comparison:

| hyresult label | Segment name |
|---|---|
| SkiErg | SkiErg |
| Sled Push | Sled Push |
| Sled Pull | Sled Pull |
| Burpee BJ | Burpee Broad Jump |
| Row | Rameur |
| F. Carry | Farmers Carry |
| S. Lunges | Sandbag Lunges |
| Wall Balls | Wall Balls |

A paste is accepted only when: exactly 30 data rows; the running sum
of diff values matches the time column on every row; labels follow the
cycle's expected order. Any other outcome fails on the first faulty
row encountered, writing nothing — never a partial import (§2.1). A
reading failure is a normal outcome, never a crash, never an
approximate interpretation, since the source format may change labels,
abbreviations or column order without notice.

Output: on success, a recognized total time and segment count, read by
§9.4; on failure, the faulty row number and the matching cause,
mapped to §9.5/§10.4's catalogue.

### §5.2 Deriving maximum heart rate from health history

On first opening §9.6, proposes `hrMaxBpm` = the highest value observed
in the phone's health history over the past 12 months, editable by
hand; no age-based formula (age is neither known nor requested), and
neither Samsung Health's own zone configuration nor its own HR max is
reachable by a third-party app. Read on the phone only.

When the history is empty, inaccessible, or its permission refused,
`hrMaxBpm` is never guessed — it stays unset until entered by hand, and
§9.6/§3.1's zone ranges stay hidden until then. A hand-entered value is
never overwritten by a later automatic reading; a higher later reading
is never flagged.

### §5.3 Exercise session and sensor data availability

One exercise session covers a whole `recorded` race, opened at §9.11's
preparation screen and closed at §9.15's end screen; the 30 markings
(§4.3) are recorded inside it, not as separate sessions. The device
allows one exercise session at a time across all apps, arbitrated at
start by §4.2.

Each sensor data type's availability is checked before it is relied
on — it varies by device. A missing sensor reading is a normal case;
the clock (§2.3) keeps running regardless. While the screen is not
interactive, sensor data arrives in batches rather than continuously.

---

## §6 Synchronisation

### §6.1 Sending profile and reference to the watch

A single push carries `Profile` (§2.2), the full reference `Race` with
its 30 segments (§1.1/§2.1), and a summarized history capped at the 20
most recent races — each entry `{name, date, totalTime}` (§9.10's
fields) — the reference itself always going in full. Triggers
automatically once the device link is established, or on demand from
§9.6's button. Fully replaces the watch's state: no merge, no
comparison — a race deleted on the phone (§2.1) is gone from the watch
after the next push.

The watch refuses any incoming push while a race is running on it,
whatever it carries; the phone treats the refusal as an ordinary
failure, retried at the next established connection. The watch's state
is therefore never altered mid-race.

Result (success / failure / last-success date) is visible on both
devices — §9.6 on the phone, §9.9 on the watch.

### §6.2 Receiving recorded races from the watch

Only watch-recorded races (§2.1, `origin = recorded`) travel up to the
phone; the phone never sends races to the watch beyond the reference
and history of §6.1. Transfer happens in chunks, automatically once
the link is established, or on demand from the watch. A race appears
on the phone only once its transfer completes; an interrupted transfer
resumes from the start. The watch erases its copy only after the phone
confirms receipt — until then it stays in the watch's own descending
history. A failed attempt retries at the next established link only,
never retried in between. Nothing syncs while a race is running: an
absent or dead phone has no effect on the clock (§2.3).

---

## §7 Background work

*(empty)*

---

## §8 Journey

### §8.1 Return to main page after marking or inactivity

From any race page but Control (§9.14), a marking (§4.3) returns the
watch to the main page (§9.12) automatically. The same return fires
after 8 seconds without interaction on a secondary page (Projection
§9.13, Control §9.14). Referenced by §8.3 rather than restated.

### §8.2 Phone navigation map

From §9.1 (race list): a card opens §9.2 (detail); the header's
profile icon opens §9.6, whose "Synchroniser" is an in-place action
(§6.1); the header's "+" or the empty-list action opens §9.3 (paste).
From §9.3, "Importer" leads to §9.4 on success or §9.5 on failure;
§9.4's "Corriger" returns to §9.3, its "Enregistrer" opens the new
race's §9.2 directly; §9.5's "Revenir au collage" returns to §9.3.
From §9.2: set as reference, rename, or delete (with confirmation) —
all in place (§2.1). The system back gesture steps back one screen at
a time, in reverse of the path taken — except that after a successful
import save, §9.3 and §9.4 leave the stack: back from the new race's
§9.2 returns directly to §9.1.

### §8.3 Watch navigation map

First launch: §4.1's permission request, then §9.8 (waiting for the
phone, shown only until a profile has ever been received), then §9.9
(home). From §9.9: "Démarrer" opens §9.11 (preparation), whose
"Quitter" returns to §9.9 and whose "Lancer" opens the race —
intercalated by §9.11's sensor-conflict dialog only when another app
holds the sensor (§4.2); "Historique" opens §9.10, returned from by the
system gesture; "Synchroniser" is an in-place action (§6.1/§6.2).

During the race, pages chain forward only, by a rightward swipe: main
(§9.12), then Projection (§9.13), then Control (§9.14) — no page
answers a leftward swipe. The system back gesture is disabled
throughout the race — on §9.12, §9.13, §9.14 and §9.15 — since an
accidental gesture must never exit a running race; stopping (§4.5) is
the only way out. Outside a race, and on §9.11, the back gesture works
normally. §8.1's auto-return rule applies from any page but Control.
§9.14's undo returns to §9.12; its stop action opens a confirmation,
then §9.15. The 30th marking also opens §9.15 directly. §9.15's
"Terminer" returns to §9.9.

---

## §9 Screen

### §9.1 Race list screen (phone)

Opening screen: one card per race — `name`, `date`, `totalTime`
(§1.1/§3.7) — the reference race (§2.1) carrying a visible mark. Cards
sort by `date` descending; ties break by insertion order, an internal
criterion never shown. Header button opens §9.3. Empty state directs
to pasting a result. An `incomplete` race (§2.1) is marked as such.

Rendering: `surface` background. Header: `p-title`/`text-primary`,
profile icon and "+" aligned right, 36–38dp circles, `border-strong`.
Card: `surface-raised`, `radius-card`; name `p-body`/`text-primary`
left, total `p-value`/`font-data` right, date `p-caption`/
`text-secondary` under the name. Reference badge: `link` on tinted
background, `p-caption`, `radius-chip` (text: §10.4
`phone.race_list.reference_badge`). Incomplete badge: `behind-text` on
`behind-bg`, same shape (text: §10.4
`phone.race_list.incomplete_badge`).

Empty state: centered — title `p-title`, explanation `p-body`/
`text-secondary` on a constrained width, "Coller un résultat" pill,
bordered `border-strong` (§10.4 `phone.race_list.empty_*`).

Consumes: §1.1, §2.1, §3.7, §10.4.

### §9.2 Race detail screen (phone)

Lists the 30 segments in order with `durationMs` and `cumulativeMs`
(§1.1/§3.7), grouped visually by cycle. Delta column (§3.4/§1.1's
reference comparison) shown unless this race is itself the reference
or none exists. All 30 rows always render, grouping included; a
segment never reached shows a dash for duration/cumulative and an
empty delta cell; the header total is the sum of segments actually
run.

Header: race `name` `p-title`, `date` `p-caption`/`text-secondary`,
total `p-value`/`font-data`, reference badge `link` (§9.1's badge
style). Three actions in a row: "Définir comme référence" filled
(§2.1's set-as-reference — hidden, neither here nor on §9.1's card,
when `completion = incomplete` or `isReference = true` already),
"Renommer" bordered (opens rename dialog, §2.1's rename — bordered
`radius-card` field pre-filled with `name`, "Annuler"/"Enregistrer"),
"Supprimer" plain text `behind` (opens delete confirmation, §2.1's
delete — "!" badge on `behind`, title naming the race, body §10.4
`phone.delete_confirm.body`; when `isReference = true`, §10.4
`phone.delete_confirm.reference_notice` is inserted before it;
"Annuler" bordered, "Supprimer" filled `behind`).

Cycle group header: "CYCLE n" `p-caption`/`text-tertiary`,
letter-spaced (§1.2). Row: name `p-data`/`text-primary`, duration and
cumulative `font-data`/`text-secondary`, delta `font-data` colored
`ahead`/`behind`/`delta-zero`; columns fixed-width aligned.

Consumes: §1.1, §1.2, §2.1, §3.4, §3.7, §10.1, §10.3, §10.4.

### §9.3 Paste-a-result screen (phone)

Pastes the 4 hyresult columns into a text area, names the race, sets
the race's date, taps "Importer" (§5.1). Entry is pasted text only —
no file picker, since official results are never exported as a file.
"Importer" stays disabled while the paste area, the name field, or the
date field is empty, active as soon as all three are filled; no inline
validation error.

Below the name field, a "Date de la course" field: a standard date
picker, prefilled with today's date, selectable range ending at today
(no future date; no lower bound). Today's value is a convenience
only — an imported race is almost always earlier, and the prefilled
value is expected to be corrected.

Rendering: tall multiline field, `radius-card`, `border`, placeholder
`text-tertiary` (§10.4 `phone.paste.placeholder`). Below it, the name
field (§10.4 `phone.paste.name_label`/`name_placeholder`), then the
date field, "Date de la course". Full-width "Importer" pill (§10.4
`phone.paste.action`).

Consumes: §5.1, §10.4.

### §9.4 Import preview screen (phone)

On §5.1's successful reading, shows the recognized total time and
segment count before anything is saved. "Corriger" returns to §9.3
keeping the pasted text; "Enregistrer" triggers §2.1's save.

Rendering: "✓" badge on `ahead`, `p-title` title, two label/value
lines (labels `text-secondary`, values `font-data`/`p-value`) —
§10.4 `phone.preview.total_label`/`segments_label`. "Corriger"
bordered, "Enregistrer" filled (§10.4 `phone.preview.correct`/`save`).

Consumes: §5.1, §2.1, §10.4.

### §9.5 Paste error screen (phone)

On §5.1's failed reading, shows exactly one message — the first
anomaly, in reading order — naming the cause and the row, with a
corrective sentence. Causes, in the order §5.1 evaluates them:

| Cause | Catalogue entry (§10.4) |
|---|---|
| Empty paste | `phone.paste_error.empty` |
| Fewer than 4 columns | `phone.paste_error.missing_columns` |
| Unreadable time value | `phone.paste_error.invalid_time` |
| Fewer than 30 segments | `phone.paste_error.too_few` |
| More than 30 segments | `phone.paste_error.too_many` |
| Unrecognized label | `phone.paste_error.unknown_label` |
| Label out of sequence | `phone.paste_error.out_of_sequence` |
| Inconsistent cumulative time | `phone.paste_error.inconsistent_time` |

The `{label}` parameter repeats the value read as-is, truncated to 20
characters. "Revenir au collage" always returns to §9.3, keeping the
pasted text (§10.4 `phone.paste_error.back`).

Rendering: "!" badge on `behind`, title naming the faulty row,
explanation `p-body`/`text-secondary`, then a `surface-raised` panel
showing the row as read in `behind` and, as illustration, its expected
form in `ahead`, both `font-data`. No control applies the illustrated
form — the user corrects at the source and pastes again.

Consumes: §5.1, §10.4.

### §9.6 Profile screen (phone)

Opens from the icon next to §9.1's "+". Holds `hrMaxBpm`, the 4
`zoneThresholds`, `expectedDistanceM`, `longPressMs` (§2.2), a sync
button and `lastSyncSuccessAt` (§2.2/§6.1).

`hrMaxBpm` edits via a numeric dialog opened by "Modifier". The other
three fields edit inline, validated on focus loss. No stepper, no
slider.

Zone ranges (§3.1) render as 5 rows — swatch `zone-1`…`zone-5`, label,
percentage and bpm range `font-data`/`text-secondary`, aligned columns
— and stay hidden while `hrMaxBpm` is unset (§5.2).

Rendering: HR max `p-value`/`font-data` + unit `p-caption`/
`text-secondary`, "Maximum observé sur 12 mois · Modifier" underneath
(link in `link` color; §10.4 `phone.profile.hr_max_source`/
`hr_max_edit`). Two numeric settings as label/value rows (§10.4
`phone.profile.distance_label`/`press_duration_label`). Full-width
bordered pill "Synchroniser avec la montre" (§10.4
`phone.profile.sync_action`), last-success date underneath
(`p-caption`/`text-tertiary`, §10.3's relative-date template, or §10.4
`phone.profile.sync_unavailable`/`sync_allow_action` in place of it
when the connectivity permission is denied — §11.2).

Sync states: in progress — spinning icon + §10.4
`phone.sync.in_progress`; failed — message in `behind` (§10.4
`phone.sync.failure`) + "Réessayer" (§10.4 `phone.sync.retry`).

Consumes: §2.2, §3.1, §5.2, §6.1, §9.18/§11.2, §10.1, §10.3, §10.4.

### §9.7 Sensor permission screen (watch)

Rendering for §4.1's request: title `w-title`, explanation
`w-label`/`text-secondary` (§10.4 `watch.permission.*`), a pill action
button, centered, text on 3 lines maximum.

Consumes: §4.1, §10.4.

### §9.8 Waiting-for-phone screen (watch)

Shown instead of §9.9 until a profile has ever been received (§6.1):
title "En attente du téléphone" with a retry button (§10.4
`watch.waiting.*`).

Consumes: §6.1, §10.4.

### §9.9 Home screen (watch)

Top to bottom: the reference line — small, `name`+`totalTime` (§2.1),
or the "no reference" badge when none is loaded (§2.1); a large
"Démarrer" button, active regardless; on scroll, "Historique" and
"Synchroniser." "Synchroniser" is an in-place action, not a screen: it
triggers §6.1/§6.2 and shows the result without leaving this screen,
through the same 3 states as §9.6: in progress — activity indicator +
§10.4 `watch.sync.in_progress`; failure — §10.4 `watch.sync.failure` +
retry; success — returns to the normal state with reference and
history current.

Rendering: reference line `w-label`/`text-secondary` + time
`font-data` (§10.3 `watch.home.reference_line`); without a reference,
"⚠ Aucune référence" badge `behind-text` on `behind-bg`, `radius-chip`
(§10.4 `watch.home.no_reference` — also shown for as long as the
connectivity permission is denied, §11.2). "Démarrer": full-width
pill, bordered not filled — 2px `text-primary` border, 7%-opacity
`text-primary` fill, `text-primary` label (§10.4 `watch.home.start`).
"Historique"/"Synchroniser": pills bordered `border-strong`,
`text-body` label (§10.4 `watch.home.history`/`sync`).

Consumes: §2.1, §6.1, §6.2, §9.18/§11.2, §10.3, §10.4.

### §9.10 Watch history screen

Race list in summary — `name`, `date`, `totalTime` (§6.1's summarized
entries). Segment-by-segment detail exists only on the phone (§9.2).
Read-only: no favorite change, no rename, no delete here.

Rendering: title `w-label`/`text-tertiary`, letter-spaced (§10.4
`watch.history.*` for the empty state). Row: name `w-label`/
`text-primary`, date+total on the next line `font-data`/
`text-secondary`.

Consumes: §6.1, §10.4.

### §9.11 Preparation and sensor-conflict screens (watch)

Preparation (the sas, §4.2): heart rate label `w-caption`/
`text-tertiary`, value `font-data`/`w-display-sm` (§10.4
`watch.prep.hr_label`). Reference-loaded badge `ahead-text` on
`ahead-bg` (§10.3 `watch.prep.reference_loaded`). "Lancer" filled pill,
"Quitter" plain text `text-secondary` (§10.4 `watch.prep.launch`/
`quit`).

Sensor-conflict dialog ("Reprise d'activité en cours," §4.2): title, a
mention that the running activity will be stopped, "Annuler" bordered,
"Continuer" filled (§10.4 `watch.resume_dialog.*`).

Consumes: §4.2, §10.3, §10.4.

### §9.12 Main race page (watch)

Bottom block never changes: heart rate and the zone arc (§3.1). Top
and center adapt to the segment type (§1.1):

- `RUN`: top — lap delta (§3.4); center, large — `allure-segment`
  (§3.2) in min/km with the trend arrow (§3.6). Comparison is lap by
  lap, not cumulative.
- `STATION` (including segment 30, `FINAL`, treated as a station: name
  shown as "Wall Balls," reference time = the reference race's segment
  30 duration): top — the reference race's time on this
  station/segment (§1.1/§2.1); center, large — elapsed time since the
  segment started. No delta.
- `ROXZONE_OUT` / `ROXZONE_IN`: top — elapsed transition time; center,
  large — the next step ("→ SkiErg" for a station, "→ Run 3" for a
  kilometre). No delta; a Roxzone's timing never renders as
  underperformance.

Without a reference loaded (§2.1), 4 blocks disappear across all race
pages: reference time, lap delta, cumulative delta (§9.13), estimated
arrival (§9.13) — remaining blocks keep their position, the page is
not reorganized. At most 3 legible blocks at once on the 480×480 face,
never 4.

Rendering: `screen-black` background, 3 blocks spaced evenly, 12%
margin top / 11% bottom. 9px dot `rgba(255,255,255,0.35)`, centered 6%
from top, signals the actionable surface — no drawn button (§4.3).
Delta badge: `font-data`, `w-badge`, `radius-chip`,
`ahead-text`/`ahead-bg` or `behind-text`/`behind-bg`. Central
clock/pace: `font-data`, `w-display`, `text-primary`, single line.
"/km" unit: `font-label`, `w-label`, `text-secondary` (§10.1). Trend
arrow: `ahead`/`behind`, under the unit. Station name: `font-label`,
`w-label`, `text-tertiary`, letter-spaced capitals. Reference time:
`font-data`, `w-label`, `text-secondary`. Roxzone time: `font-data`,
`w-value-sm`, `text-primary`. Destination: `font-label`, `w-value`,
arrow at 0.85 opacity, name at full opacity. Heart rate: `font-data`,
`w-value`, `text-primary`; "bpm" unit `w-label-sm`/`text-secondary`
(§10.1). Zone number: `w-caption`, `text-tertiary`, letter-spaced
(§10.1's `zone` format). Without a heart-rate reading — permanent
fallback (§4.1) or before the first reading — no arc segment is
active: all 5 idle, value is a dash (§1.3).

Zone arc: 5 arcs of `arc-segment` each (§1.2), separated by
`arc-gap`, spanning `arc-span` centered bottom, at `arc-radius`, cut
ends. Active zone: `arc-width-active`/`arc-opacity-active`; others:
`arc-width`/`arc-opacity-idle`. Switching follows §3.1's hysteresis.

Consumes: §1.1, §1.2, §1.3, §2.1, §3.1, §3.2, §3.4, §3.6, §4.1, §4.3,
§9.13, §10.1.

### §9.13 Projection page (watch)

Reached by a rightward swipe from §9.12 (§8.3). Top — cumulative delta
since start (§3.5); center, large — estimated arrival (§3.5); bottom —
total elapsed time and position, "n/30" (§10.1's `position` format).
§4.3's long-press marking stays active here.

Rendering: delta badge, same tokens as §9.12. Arrival `font-data`/
`w-display`. Under it, "arrivée estimée" `w-caption`/`text-tertiary`,
letter-spaced (§10.4 `watch.projection.eta_label`). Bottom: elapsed
time + position, one line, `font-data`/`w-label`/`text-secondary`.

Consumes: §3.5, §4.3, §8.3, §10.1, §10.4.

### §9.14 Control page (watch)

Reached by a rightward swipe from §9.13 (§8.3) — the only race page
where the surface is not the advance control. Two actions: undo
(§4.4) and stop (§4.5).

Undo control: full-width filled pill naming the segment §4.4 would
reopen (§10.3 `watch.control.undo_label`); disabled before the race's
first marking. Stop control: plain text `behind`, less prominent than
undo, under it (§10.4 `watch.control.stop`). Title "Contrôle"
`w-label`/`text-tertiary`, letter-spaced (§10.4 `watch.control.title`).

Stop confirmation (§4.5): title, a mention that the race will be saved
as-is and marked incomplete, "Annuler" bordered, "Arrêter" filled
`behind` (§10.4 `watch.stop_confirm.*`).

Consumes: §4.4, §4.5, §8.3, §10.3, §10.4.

### §9.15 End-of-race screen (watch)

Reached on the 30th marking or on §4.5's early stop (§8.3). Shows
total time, final delta (§3.5, or the cumulative delta at the last
closed segment for an early stop — segments never reached enter no
calculation), and the race's automatic name (§10.3's watch-generated
name, date+time). An early-stopped race states it is incomplete.
Saving (§2.1) is automatic, no confirmation. "Terminer" returns to
§9.9 (§8.3). Without a reference loaded, the final delta is hidden,
not shown (§2.1).

Rendering: centered — total time `font-data`/`w-display-sm`, final
delta badge under it, then date+time `font-data`/`w-caption`/
`text-tertiary`. "Terminer" at the bottom (§10.4 `watch.end.finish`).

Consumes: §2.1, §3.5, §4.5, §8.3, §10.3, §10.4.

### §9.16 Always-on / power-save display (watch)

The screen stays visible through the whole race without a wrist raise.
Power-save mode dims using §1.2's idle tokens — thinner, more
transparent arc, muted text — without moving or resizing anything.
Refresh in power-save mode: every 10 seconds (matching §1.3's
freshness window), rather than the device's default once-per-minute.
Forcing full brightness at all times is excluded. Values stay shown,
dimmed, rather than replaced with a dash as platform guidance
recommends — a deliberate departure. Full refresh resumes on a wrist
raise or a screen touch. Applies across §9.12, §9.13, §9.14.

Consumes: §1.2, §1.3.

### §9.17 Watch-face complication

A complication on the watch face returns to the app throughout the
race (an entry point back into whichever race page is current, §8.3).

Consumes: §8.3.

### §9.18 Connectivity-permission-denied screen states

While the connectivity permission (§11.2) is denied: §9.6 shows §10.4
`phone.profile.sync_unavailable` in place of the last-sync date, with
`phone.profile.sync_allow_action` just below it, and its
"Synchroniser avec la montre" button stays displayed but inactive.
§9.9 shows `watch.home.no_reference` for as long as it has received
nothing (§6.1 never having run).

Consumes: §9.6, §9.9, §11.2, §10.4.

---

## §10 Text

### §10.1 Display formats

`duration-segment`: m:ss, always under the hour. `duration-total`:
h:mm:ss, hour group kept even at zero ("0:52:18," so list columns
align). `duration-elapsed`: m:ss under 60 minutes, then h:mm:ss past
the hour. None of the three shows a leading zero on its first group
("6:36," never "06:36").

`delta`: sign + m:ss; the sign is always present, even at zero
("+0:00"). Positive or nil → "+", negative → "−" (U+2212, never the
ASCII hyphen). Color (`ahead`/`behind`/`delta-zero`, §1.2), not a
format change, distinguishes the three cases. Past the hour, stays in
m:ss ("+72:14," never "+1:12:14").

`pace`: m:ss + detached "/km" unit. `hr`: integer + detached "bpm"
unit. `position`: "n/30," no spaces. `zone`: "Zone n." A unit is
always its own element, smaller, `text-secondary`, never concatenated
to the value.

`zone-percentage`: integer + non-breaking space + "%" ("50 %").
`zone-range`: bounds separated by an en dash ("94–112 bpm").
`zone-range-extreme`: operator + space ("< 94 bpm," "> 150 bpm").
`distance`: integer + space + "m," no thousands separator ("1000 m").
`press-duration`: integer + space + "ms" ("700 ms").

`date`: day, abbreviated month, year ("12 avr. 2026"). `date-time`:
`date` + " · " + "h:mm" ("12 avr. 2026 · 09:14"). Relative wording —
today: "aujourd'hui à 09:02"; yesterday: "hier à 09:02"; earlier: the
full `date-time`.

Consumed by §1.2 (colors), §3.7 (source values), and every §9
subsection rendering a timed, delta, pace, hr, position, zone, range,
distance, press-duration or date value.

### §10.2 Resource file conventions

No visible string is ever hard-coded on either platform — every one
comes from a resource file. Single language, French; no other locale,
no switching mechanism. Phone and watch keep separate resource files —
a key present on both sides is duplicated, never shared, even for
identical wording. An interpolated value is always passed as a
resource parameter, never string-concatenated.

### §10.3 Dynamic text templates

| Key | Template | Used by |
|---|---|---|
| `watch.home.reference_line` | "Réf. — {name}" — replaced entirely by `watch.home.no_reference` when none is loaded | §9.9 |
| `watch.prep.reference_loaded` | "Référence chargée · {name}" — line hidden without a reference | §9.11 |
| `watch.control.undo_label` | "Annuler : {segment}" — control disabled before the first marking | §9.14 |
| `phone.profile.last_sync` | "Dernière synchronisation réussie : {date}" | §9.6 |
| `phone.profile.last_sync_never` | "Jamais synchronisé" — shown before any success | §9.6 |
| `phone.delete_confirm.title` | "Supprimer « {name} » ?" — `name` is never empty | §9.2 |
| `phone.profile.zone_row` | "Zone {n}" — row hidden without a heart-rate reading | §9.6 |
| `watch.race_name.generated` | `date-time` format (§10.1) — "12 avr. 2026 · 09:14" | §2.1, §9.15 |

The 8 titles of §9.5/§10.4's failure catalogue cover every rejection
cause; no generic catch-all reading-error text exists beyond them.

**Name rule** (`phone.race_detail`/`watch.race_name`): a race name is
never empty — the phone's entry field rejects an empty value once
leading/trailing spaces are trimmed; the watch generates its name
automatically via `watch.race_name.generated`. Capped at 40 characters
at entry (§2.1). Displayed, a name too long for its slot truncates at
the end with an ellipsis, never wraps past one line.

### §10.4 Fixed text catalogue

**Watch, outside the race**

| Key | Value |
|---|---|
| `watch.permission.title` | "Autoriser l'accès au capteur cardiaque" |
| `watch.permission.explanation` | "Nécessaire pour afficher ta fréquence et tes zones pendant la course." |
| `watch.permission.action` | "Autoriser" |
| `watch.permission.reminder` | "⚠ Capteur cardiaque non autorisé" |
| `watch.waiting.title` | "En attente du téléphone" |
| `watch.waiting.explanation` | "Ouvre l'application sur ton téléphone pour envoyer ton profil." |
| `watch.waiting.retry` | "Réessayer" |
| `watch.home.start` | "Démarrer" |
| `watch.home.history` | "Historique" |
| `watch.home.sync` | "Synchroniser" |
| `watch.home.no_reference` | "⚠ Aucune référence" |
| `watch.history.empty_title` | "Aucune course" |
| `watch.history.empty_action` | "Synchronise depuis le téléphone." |
| `watch.prep.hr_label` | "Fréquence cardiaque" |
| `watch.prep.launch` | "Lancer" |
| `watch.prep.quit` | "Quitter" |

**Watch, during the race**

| Key | Value |
|---|---|
| `watch.projection.eta_label` | "arrivée estimée" |
| `watch.control.title` | "Contrôle" |
| `watch.control.stop` | "Arrêter l'activité" |
| `watch.stop_confirm.title` | "Arrêter l'activité ?" |
| `watch.stop_confirm.body` | "Elle sera enregistrée telle quelle, marquée incomplète." |
| `watch.stop_confirm.cancel` | "Annuler" |
| `watch.stop_confirm.confirm` | "Arrêter" |
| `watch.resume_dialog.title` | "Une autre activité est en cours" |
| `watch.resume_dialog.body` | "Elle sera arrêtée pour démarrer le suivi Hyrox." |
| `watch.resume_dialog.cancel` | "Annuler" |
| `watch.resume_dialog.confirm` | "Continuer" |
| `watch.end.finish` | "Terminer" |
| `watch.sync.in_progress` | "Ne ferme pas l'application" |
| `watch.sync.failure` | "Synchronisation impossible — approche le téléphone de la montre." |

**Phone**

| Key | Value |
|---|---|
| `phone.race_list.title` | "Mes courses" |
| `phone.race_list.reference_badge` | "Référence" |
| `phone.race_list.incomplete_badge` | "Incomplète" |
| `phone.race_list.empty_title` | "Aucune course encore" |
| `phone.race_list.empty_body` | "Colle un résultat officiel depuis hyresult pour importer ta première course." |
| `phone.race_list.empty_action` | "Coller un résultat" |
| `phone.race_detail.set_reference` | "Définir comme référence" |
| `phone.race_detail.rename` | "Renommer" |
| `phone.race_detail.delete` | "Supprimer" |
| `phone.delete_confirm.body` | "Suppression définitive. La course disparaîtra aussi de l'historique sur la montre." |
| `phone.delete_confirm.reference_notice` | "C'est la course de référence. Après suppression, plus aucune course ne servira de comparaison." |
| `phone.delete_confirm.cancel` | "Annuler" |
| `phone.delete_confirm.confirm` | "Supprimer" |
| `phone.rename.title` | "Renommer la course" |
| `phone.rename.field_label` | "Nom" |
| `phone.rename.cancel` | "Annuler" |
| `phone.rename.save` | "Enregistrer" |
| `phone.paste.title` | "Coller un résultat" |
| `phone.paste.placeholder` | "Colle ici les colonnes copiées depuis hyresult…" |
| `phone.paste.name_label` | "Nom de la course" |
| `phone.paste.name_placeholder` | "ex. Marseille 2026" |
| `phone.paste.action` | "Importer" |
| `phone.preview.title` | "Aperçu avant enregistrement" |
| `phone.preview.total_label` | "Temps total reconnu" |
| `phone.preview.segments_label` | "Segments détectés" |
| `phone.preview.correct` | "Corriger" |
| `phone.preview.save` | "Enregistrer" |
| `phone.paste_error.back` | "Revenir au collage" |
| `phone.profile.title` | "Profil" |
| `phone.profile.hr_max_label` | "Fréquence cardiaque maximale" |
| `phone.profile.hr_max_source` | "Maximum observé sur 12 mois" |
| `phone.profile.hr_max_edit` | "Modifier" |
| `phone.profile.zones_label` | "Zones cardiaques (% FC max)" |
| `phone.profile.distance_label` | "Distance d'un kilomètre" |
| `phone.profile.press_duration_label` | "Durée de l'appui long" |
| `phone.profile.sync_action` | "Synchroniser avec la montre" |
| `phone.profile.sync_unavailable` | "Synchronisation indisponible — l'accès aux appareils à proximité n'est pas autorisé." |
| `phone.profile.sync_allow_action` | "Autoriser" |
| `phone.sync.in_progress` | "Ne ferme pas l'application" |
| `phone.sync.failure` | "Synchronisation impossible — approche la montre du téléphone." |
| `phone.sync.retry` | "Réessayer." |

**§9.5's failure catalogue** (title / body, `{n}` = row number,
`{label}` = the value read, truncated to 20 characters):

| Key | Title | Body |
|---|---|---|
| `phone.paste_error.empty` | "Rien à lire" | "Colle les quatre colonnes copiées depuis hyresult." |
| `phone.paste_error.missing_columns` | "Colonnes manquantes — ligne {n}" | "Chaque ligne doit contenir quatre colonnes. Copie le tableau entier, en-tête compris." |
| `phone.paste_error.invalid_time` | "Format de temps invalide — ligne {n}" | "Le temps doit être au format m:ss. Remplace l'espace par un deux-points." |
| `phone.paste_error.too_few` | "{n} segments sur 30" | "Le collage est incomplet. Copie le tableau entier, de la première ligne jusqu'à « Total time »." |
| `phone.paste_error.too_many` | "{n} segments au lieu de 30" | "Le collage contient des lignes en trop. Copie uniquement le tableau des temps." |
| `phone.paste_error.unknown_label` | "Libellé inconnu — ligne {n}" | "« {label} » n'est pas un point de passage attendu. Vérifie que tu as copié un résultat Hyrox complet." |
| `phone.paste_error.out_of_sequence` | "Ordre inattendu — ligne {n}" | "« {label} » n'est pas à sa place dans la course. Copie le tableau sans le trier ni le réorganiser." |
| `phone.paste_error.inconsistent_time` | "Temps incohérents — ligne {n}" | "Le cumul ne correspond pas à la somme des temps. Vérifie que la ligne n'a pas été modifiée." |

---

## §11 Access

### §11.1 Heart-rate data consent

Collecting and storing heart-rate data relies solely on the OS-level
sensor permission (§4.1) and health-history permission (§5.2) — no
consent step of the app's own. No heart-rate data ever leaves the
phone and the watch: nothing sent to a server, shared, or exported.

### §11.2 Connectivity permission denial

Denying the connectivity permission needed to pair the devices leaves
sync (§6.1/§6.2) permanently unavailable, without affecting anything
else — both apps stay fully usable on their own. Screen effects on
both devices are §9.18's. Tapping the phone's "Autoriser" (§9.6/§9.18)
re-requests the permission; if the system no longer offers that
request — a permanent refusal or a revoked permission — the app opens
its own permissions page in system settings instead. Checked at every
launch, exactly as §4.1 checks the sensor permission: a later
revocation from system settings produces the same state as an initial
refusal. Never auto-re-requested.

Consumes: §4.1, §6.1, §6.2, §9.18.

---

## §12 Lifecycle

*(empty)*
